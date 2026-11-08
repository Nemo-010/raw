"""rq integrate: the only writer. Applies lane proposals on the run branch rq/<run>, with git plumbing.

For each unit in order, for each proposed operation: scope and fence, evidence (capture and quote),
narrative lint, value-level compare-and-set against the record as it is now, the supersession table,
dedupe of new records into corroboration, a format-preserving validated write through fr, the record's
error rules, a ledger line, and one commit per unit. Anything not decidable mechanically becomes a
conflict, and conflicts become reconcile units. No model is involved.

There is no worktree. The run branch is read through a TreeView; a unit's writes are an Overlay of changes on it,
committed with commit_on against the commit they were read from, and the view advances after each commit. The run
lock keeps a second writer of the run out. A unit that stops half-way leaves the ref where it was. A unit's leases
stay until the run's pull request is merged or closed, and a record it creates is leased to it too.
"""
import collections
import difflib
import json
import os
import re
import subprocess
import sys

import checks
import state
import units
from common import (LADDER, REPO, Fail, Overlay, RefMoved, RefNotMoved, append_jsonl, commit_on, core_name, domain_of,
                    fr, git, json_bytes, norm_url, other_tier, parse_jsonl, promote_files, read_jsonl, rev, run_dir,
                    run_lock, stamp, stamp_ms, test_stop, today, validate_in, write_jsonl)

UNCHECKED = re.compile(r"not re-checked|no page was read|inherit|not verified|not re-established", re.I)
PLACEHOLDER = re.compile(r"^\s*(not stated|not recorded|not published|not assessed|unknown|unverified|none recorded|"
                         r"not applicable|n/a|no data|tbd)\b", re.I)


def ev_row(ev):
    row = {"url": ev["url"], "date": ev["date"], "proved": ev["proved"].strip()}
    if ev.get("capture"):
        row["capture"] = ev["capture"]
    if ev.get("quote"):
        row["quote"] = ev["quote"].strip()
    return row


def add_evidence(rec, ev):
    row = ev_row(ev)
    evl = rec.setdefault("evidence", [])
    if not any(isinstance(e, dict) and e.get("url") == row["url"] and e.get("date") == row["date"]
               and e.get("quote") == row.get("quote") and e.get("proved") == row["proved"] for e in evl):
        evl.append(row)
        return True
    return False


def newest_date(rec):
    ds = [e.get("date") or "" for e in rec.get("evidence") or [] if isinstance(e, dict)]
    return max(ds) if ds else ""


def is_placeholder(rec, segs, cur):
    m = fr()
    if cur is m.ABSENT or cur is None or cur == "" or cur == []:
        return True
    if isinstance(cur, str) and PLACEHOLDER.match(cur):
        return True
    if segs[0] == "identity_cost" and checks.DEFAULTED.search((rec.get("identity_cost") or {}).get("detail") or ""):
        return True
    return False


def ledger_rel(run, unit):
    return "history/ledger/%s/%s.jsonl" % (run, unit)


class Ledger:
    """One file per unit, history/ledger/<run>/<unit>.jsonl, so one unit's lines never touch another's file.
    A line carries what an undo needs: the old value (absent: true when there was none) and whether the
    evidence row was added by this unit (added: true) or was already there. The lines go into the unit's overlay,
    after the lines the tip already holds (a unit reopened with --fix keeps its earlier lines)."""
    def __init__(self, ov, run):
        self.ov, self.run = ov, run

    def line(self, unit, op, rid, path=None, old=None, new=None, rung=None, ev=None, reason=None, added=False, unread=None,
             dropped=None, index=None):
        o = collections.OrderedDict([("at", stamp_ms()), ("run", self.run), ("unit", unit), ("op", op), ("rid", rid)])
        if path is not None:
            o["path"] = path
            o["old"] = None if old is fr().ABSENT else old
            o["new"] = new
            if old is fr().ABSENT:
                o["absent"] = True
        if rung:
            o["rung"] = rung
        if ev:
            o["evidence"] = ev_row(ev)
            if added:
                o["added"] = True
        if dropped is not None:
            # the row a drop_evidence took out, verbatim, and its place: the history keeps it, and an undo puts it back
            o["evidence"] = dropped
            o["index"] = index
        if reason:
            o["reason"] = reason
        if unread:
            o["unread"] = list(unread)
        rel = ledger_rel(self.run, unit)
        self.ov.set(rel, (self.ov.read(rel) or b"") + (json.dumps(o, ensure_ascii=False) + "\n").encode("utf-8"))


def ledger_lines(view, run, unit=None):
    """The run's ledger lines from a commit (the run branch, or main after the merge)."""
    out = []
    for name, (mode, oid) in sorted((view.listdir("history/ledger/%s" % run) or {}).items()):
        if mode != "40000" and name.endswith(".jsonl") and (unit is None or name == unit + ".jsonl"):
            out += parse_jsonl(view.blob(oid).decode("utf-8"))
    return out


class DedupeIndex:
    """The records of a topic, read once per integrate through the run tree (one ls-tree, records parsed by blob id),
    with every record this integrate writes added to it (IO-07)."""

    def __init__(self, view):
        self.view = view
        self.topics = {}

    def records(self, topic):
        if topic not in self.topics:
            recs = {}
            for name, (mode, oid) in (self.view.listdir("dossier/" + topic) or {}).items():
                if mode == "40000" or not name.endswith(".json") or name.endswith(".generated.json"):
                    continue
                try:
                    recs["%s/%s" % (topic, name[:-5])] = json.loads(self.view.blob(oid).decode("utf-8"))
                except ValueError:
                    continue
            self.topics[topic] = recs
        return self.topics[topic]

    def add(self, rid, rec):
        self.records(rid.split("/")[0])[rid] = rec


def deep_urls(draft, dom):
    # a shared page is the same offer only on the vendor's own domain: a forum thread, an aggregator list or
    # a review site is cited by many vendors and says nothing about identity
    return {norm_url(e.get("url")) for e in draft.get("evidence") or [] if isinstance(e, dict)
            and (e.get("url") or "").startswith("http") and urlpath_depth(e.get("url")) >= 2 and dom
            and domain_of(e.get("url")) == dom}


def find_duplicate(index, ov, draft):
    """An existing record that is the same offer: same slug, or same topic and domain with a near name, or a
    shared deep evidence URL. A record whose tier differs from the draft's (both name one) is another offer by name
    and by URL alike: the schema's `tier` makes two tiers of one provider two records. -> rid or None."""
    topic, slug = draft["topic"], draft["slug"]
    if ov.exists("dossier/%s/%s.json" % (topic, slug)):
        return "%s/%s" % (topic, slug)
    dom = domain_of(draft.get("url") or "")
    name = core_name(draft.get("provider"))
    deep = deep_urls(draft, dom)
    for rid, rec in sorted(index.records(topic).items()):
        if other_tier(draft.get("tier"), rec.get("tier")):
            continue
        if dom and domain_of(rec.get("url") or "") == dom and name and \
                difflib.SequenceMatcher(None, name, core_name(rec.get("provider"))).ratio() >= 0.8:
            return rid
        if deep and domain_of(rec.get("url") or "") == dom and \
                deep & {norm_url(e.get("url")) for e in rec.get("evidence") or [] if isinstance(e, dict)}:
            return rid
    return None


def find_pending(repo, run, draft):
    """A record that another live run created for the same offer and that main does not have yet (G-02): the same
    slug, or the matches of find_duplicate, where a different tier is another offer. -> (run, rid) or None."""
    topic, slug = draft["topic"], draft["slug"]
    dom = domain_of(draft.get("url") or "")
    name = core_name(draft.get("provider"))
    deep = deep_urls(draft, dom)
    for orun, rid, t, d, core, s, urls, tier in state.pending(repo, topic, other_than=run):
        if s != slug and other_tier(draft.get("tier"), tier):
            continue
        if s == slug or (dom and d == dom and name and core and difflib.SequenceMatcher(None, name, core).ratio() >= 0.8) \
                or (deep and dom == d and deep & set(urls)):
            return orun, rid
    return None


def urlpath_depth(u):
    from urllib.parse import urlsplit
    return len([s for s in urlsplit(u or "").path.split("/") if s])


def record_text(view, rid, old_text, root, rec):
    """The dry run of fr's writer: validate with the run tree's own schema and validate.py, and serialise with every
    untouched byte kept. -> the new text; nothing is written to the disk."""
    m = fr()
    errs = validate_in(view, rec)
    if errs:
        msg = "; ".join("%s %s: %s" % (e.get("path"), e.get("keyword"), e.get("message")) for e in errs[:6])
        raise Fail("%s would not validate, nothing written: %s" % (rid, msg), 1)
    text = m.dump_preserving(old_text, root, rec)
    if not m.same(json.loads(text), rec):
        raise Fail("internal: the serialised record does not read back equal; nothing written", 1)
    return text


def subject(run, uid, rest):
    """The subject of a unit's commit: the whole run id, so `git log --grep RUN` and a reader find it; commit_on cuts
    only the tail of the line to 100 bytes (W3-07)."""
    return "rq %s %s: %s" % (run, uid, rest)


# an integrate commit's text after the "rq RUN UID: " head; an undo's is "undone, ..." (G3-05)
APPLIED_RE = re.compile(r"^\d+ applied, ")


def unit_commit(run, uid, subj):
    """True when a first-parent subject is the commit integrate made for this unit (not its undo). The subject of
    an older harness carried run[-30:]."""
    for head in ("rq %s %s: " % (run, uid), "rq %s %s: " % (run[-30:], uid)):
        if subj.startswith(head):
            return bool(APPLIED_RE.match(subj[len(head):]))
    return False


def conflict_rid(c):
    op = c.get("op") or {}
    return op.get("rid") or (c.get("current") or {}).get("rid")


def mark_handled(run, rids, repo=REPO):
    """The open conflicts on these records have a reconcile unit now (G3-02)."""
    p = os.path.join(run_dir(run, repo), "conflicts.jsonl")
    if not os.path.exists(p):
        return
    rows = read_jsonl(p)
    for c in rows:
        # a torn line names no record and no reconcile unit can settle it: it is closed here, so it does not stay
        # open for good (G7-08)
        if not c.get("handled") and (not usable_conflict(c) or conflict_rid(c) in rids):
            c["handled"] = True
    write_jsonl(p, rows)


def drop_attempt_lines(path, attempt):
    """Take back the conflicts that one attempt of a unit logged: a retry logs them again, once."""
    if not attempt or not os.path.exists(path):
        return
    rows = read_jsonl(path)
    keep = [c for c in rows if c.get("attempt") != attempt]
    if len(keep) != len(rows):
        write_jsonl(path, keep)


def lease_created(repo, run, u, created):
    """A record a unit created is leased to it and listed in pending_new, so another run cannot change it, and
    another run's draft of the same offer becomes a conflict, until this run merges."""
    if not created:
        return
    foreign = state.add_keys(repo, run, u["id"], ["rid:" + rid for rid, _ in created], u.get("fence"))
    for k, hrun, hunit in foreign:
        # another run holds this record (it was created on main after this run's base, and that run verifies it): the
        # lease stays with that run, and the two meet as a conflict that this run's reconcile settles (G2-09)
        append_jsonl(os.path.join(run_dir(run, repo), "conflicts.jsonl"), {
            "run": run, "unit": u["id"], "at": stamp(), "op": {"op": "add_record", "rid": k[4:]},
            "why": "the record %s that this unit created is leased by run %s unit %s; settle it after that run lands"
                   % (k[4:], hrun, hunit), "current": {"rid": k[4:], "run": hrun}})
    for rid, rec in created:
        dom = domain_of(rec.get("url") or "")
        state.add_pending(repo, run, rid, rec.get("topic"), dom, core_name(rec.get("provider")), rec.get("slug"),
                          deep_urls(rec, dom), rec.get("tier") if isinstance(rec.get("tier"), str) else None)


def recover_attempt(repo, run, u, conflicts_path):
    """A unit left with an attempt: integrate was killed between its commit and the save of the unit (G-10). When the
    first-parent history of rq/<run> since the attempt's commit holds this unit's commit, the unit is integrated with
    it; otherwise the conflict lines of that attempt are taken back and the unit runs again. -> True when it landed."""
    a = u.get("attempt")
    if not a:
        return False
    log = git(repo, "log", "--first-parent", "--format=%H %s", "%s..%s" % (a["old"], units.ref_of(run)), check=False)
    for ln in log.splitlines():
        sha, _, subj = ln.partition(" ")
        if unit_commit(run, u["id"], subj):
            # the records the unit created are leased first, and only then is the unit saved without its attempt, the
            # order of the main path: a kill between the two leaves the attempt for the next integrate (G2-02)
            from common import TreeView
            v = TreeView(repo, sha)
            created = []
            for l in ledger_lines(v, run, u["id"]):
                if l.get("op") == "add_record":
                    b = v.read("dossier/%s.json" % l["rid"])
                    if b:
                        created.append((l["rid"], json.loads(b.decode("utf-8"))))
            lease_created(repo, run, u, created)
            state.hold_unit(repo, run, u["id"])
            # the rejects, the conflict count and the tally of that attempt were saved in it before its commit
            # (G3-01)
            u.update(a.get("result") or {})
            u["commit"] = sha
            u["status"] = "integrated"
            u.pop("attempt", None)
            units.save_unit(u, repo)
            return True
    drop_attempt_lines(conflicts_path, a.get("id"))
    u.pop("attempt", None)
    units.save_unit(u, repo)
    return False


def integrate(run, repo=REPO, only=None):
    r = units.load_run(run, repo)
    with run_lock(run, repo):
        if r.get("phase") == "in-review":
            import land
            land.update_branch(r, repo, "integrate")
        conflicts_path = os.path.join(run_dir(run, repo), "conflicts.jsonl")
        recovered = []
        for u in units.units_of(run, repo):
            if not u.get("attempt"):
                continue
            was = u.get("status")
            # an attempt of a unit that is no longer ready (a collect re-linted it, or an abandon of an older harness):
            # its commit may still be on the branch, and a commit on the branch is counted and audited, never dropped
            # with the attempt (G4-01; G3-05 dropped it)
            if recover_attempt(repo, run, u, conflicts_path):
                note = "integrated (recovered: its commit was on the branch)"
                if was != "ready":
                    u.pop("abandoned", None)
                    units.save_unit(u, repo)
                    # its lease may have gone with the abandon: take back the keys no other run holds
                    foreign = state.add_keys(repo, run, u["id"], state.lease_keys(u), u.get("fence"))
                    note = ("integrated (recovered: its commit was on the branch; it was %s%s)"
                            % (was, ", and %s is leased by another run" % ", ".join(k for k, _, _ in foreign)
                               if foreign else ""))
                recovered.append((u["id"], note, dict(u.get("tally") or {}), len(u.get("rejects") or [])))
        view = units.run_tree(run, repo)
        report = recovered + _integrate(r, run, view, conflicts_path, repo, only)
        r = units.load_run(run, repo)
        r["phase"] = "integrated" if r.get("phase") in ("open", "planned", "collected", "integrated") else r.get("phase")
        units.save_run(r, repo)
    return report, read_jsonl(conflicts_path)


def _integrate(r, run, view, conflicts_path, repo, only):
    m = fr()
    base = checks.baseline_of(view)
    index = DedupeIndex(view)
    report = []
    all_units = units.units_of(run, repo)
    done_units = {x["id"] for x in all_units if x["status"] in units.UNIT_DONE}
    for u in all_units:
        if only and u["id"] not in only:
            continue
        # a lease-lost unit is taken again: its lane's work is finished, and its lease is let again when no other run
        # holds its scope now
        if u["status"] not in ("ready", "lease-lost") or u["kind"] == "audit":
            continue
        lane = units.unit_dir(run, u["id"], repo)
        probs, ops, rec_ = units.lint_unit(u, repo, need_receipt=True, view=view)
        tally = collections.Counter()
        rejects, conflicts = [], []
        if probs:
            u["status"], u["problems"] = "invalid", probs
            units.save_unit(u, repo)
            report.append((u["id"], "invalid", dict(tally), len(probs)))
            continue
        relet = None
        if not state.holds(repo, run, u):
            # the work lease expired while the lane worked (lease_hours from the plan): let it again to this unit when
            # no other run took a key since. A record that changed meanwhile meets the compare-and-set of each `set`
            fence, foreign = state.relet(repo, run, u, done_units)
            if foreign:
                u["status"] = "lease-lost"
                u["problems"] = ["lease lost: scope " + state.holder_text(f) for f in foreign]
                units.save_unit(u, repo)
                report.append((u["id"], "lease lost: scope %s. Run scripts/rq integrate %s again when the holder lets "
                               "go (another run merges or closes; a unit of this run is integrated or abandoned), or "
                               "give the unit up with scripts/rq abandon %s %s --reason \"...\""
                               % ("; scope ".join(state.holder_text(f) for f in foreign), run, run, u["id"]), {}, 0))
                continue
            relet = "its work lease had expired and was let again (fence %d)" % fence
            u["fence"] = fence
            u.pop("problems", None)
            u["status"] = "ready"
            u.setdefault("relet", []).append(stamp())
            units.save_unit(u, repo)
        attempt = {"old": view.commit, "at": stamp(), "id": "%s-%s" % (u["id"], stamp_ms())}
        u["attempt"] = attempt
        units.save_unit(u, repo)
        changes = {}
        ov = Overlay(view, changes)
        led = Ledger(ov, run)
        created = []
        try:
            touched = {}  # rid -> [path, original text, spans, working doc, done]

            def doc(rid):
                if rid not in touched:
                    p = "dossier/%s.json" % m.check_rid(rid)
                    text = ov.text(p)
                    if text is None:
                        raise Fail("no record %s on the run branch" % rid, 1)
                    touched[rid] = [p, text, m.parse_spans(text), json.loads(text), []]
                return touched[rid][3]

            def conflict(op, why, current=None):
                c = {"run": run, "unit": u["id"], "at": stamp(), "why": why, "op": op, "attempt": attempt["id"]}
                if current is not None:
                    c["current"] = current
                conflicts.append(c)
                append_jsonl(conflicts_path, c)
                tally["conflict"] += 1

            for op in ops:
                kind = op["op"]
                try:
                    if kind in ("set", "confirm") and units.measured_problem(op, "op"):
                        rejects.append((op, "measured needs a probe: evidence row that cites a stored probe record"))
                        continue
                    if kind == "set":
                        rid = op["rid"]
                        rec = doc(rid)
                        segs = m.parse_jpath(op["path"])
                        cur = m.get_path(rec, segs)
                        new = op["new"]
                        ev = op["evidence"]
                        rung = op["rung"]
                        conf = rec.get("confidence") if rec.get("confidence") in LADDER else "unverified"
                        if cur is not m.ABSENT and m.same(cur, new):
                            if add_evidence(rec, ev):
                                touched[rid][4].append(("append_evidence", op, None, True))
                            tally["corroborated"] += 1
                            continue
                        if not is_placeholder(rec, segs, cur):
                            if "old" in op and not (cur is not m.ABSENT and m.same(cur, op["old"])):
                                conflict(op, "the value changed after the lane read it", cur)
                                continue
                            if LADDER.index(rung) < LADDER.index(conf):
                                conflict(op, "weaker rung (%s) than the record (%s)" % (rung, conf), cur)
                                continue
                            if ev["date"] < newest_date(rec) and rung == conf:
                                conflict(op, "older evidence (%s) than the record's newest (%s) at the same rung"
                                         % (ev["date"], newest_date(rec)), cur)
                                continue
                        m.set_path(rec, segs, new)
                        added = add_evidence(rec, ev)
                        touched[rid][4].append(("set", op, cur, added))
                        tally["applied"] += 1
                    elif kind == "confirm":
                        rid = op["rid"]
                        rec = doc(rid)
                        added = add_evidence(rec, op["evidence"])
                        old = rec.get("verified_at", m.ABSENT)
                        rec["verified_at"] = m.utc_stamp_ms()
                        touched[rid][4].append(("confirm", op, old, added))
                        tally["confirmed"] += 1
                        # a confirm with nothing left unread is a re-check: a basis that says the record was inherited
                        # or not re-checked is no longer true (staleness.py and the store read it), so it says so now
                        ex = rec.get("extras")
                        if (not op.get("unread") and isinstance(ex, dict)
                                and UNCHECKED.search(str(ex.get("verified_at_basis") or ""))):
                            oldb = ex["verified_at_basis"]
                            ex["verified_at_basis"] = "checked against the live service on %s" % today()
                            touched[rid][4].append(("basis", op, oldb, False))
                    elif kind == "append_evidence":
                        rid = op["rid"]
                        if add_evidence(doc(rid), op["evidence"]):
                            touched[rid][4].append(("append_evidence", op, None, True))
                            tally["evidence"] += 1
                    elif kind == "drop_evidence":
                        # the row is found in the record as the unit found it (an index counts there), and taken out of
                        # the record as it is now; the ledger line keeps the row and its reason
                        rid = op["rid"]
                        rec = doc(rid)
                        before = json.loads(touched[rid][1]).get("evidence") or []
                        row, at, why = units.drop_target(before, rec.get("evidence") or [], op)
                        if why:
                            rejects.append((op, why))
                            continue
                        del rec["evidence"][at]
                        touched[rid][4].append(("drop_evidence", op, row, at))
                        tally["dropped"] += 1
                    elif kind == "dead":
                        rid = op["rid"]
                        rec = doc(rid)
                        old = rec.get("verdict")
                        rec["verdict"] = "dead"
                        rec.setdefault("extras", {})["death"] = {"on": op.get("observed") or op["evidence"]["date"], "cause": op["cause"]}
                        added = add_evidence(rec, op["evidence"])
                        touched[rid][4].append(("dead", op, old, added))
                        tally["dead"] += 1
                    elif kind == "relate":
                        # one file per unit; the store reads registry/relations.tsv and registry/relations.d/*.tsv
                        path = "registry/relations.d/%s-%s.tsv" % (run, u["id"])
                        row = "\t".join([op["src"], op["kind"], op["dst"], op["evidence"]["url"], op["evidence"]["date"],
                                         re.sub(r"\s+", " ", op.get("reason") or "")])
                        known = "".join(ov.text(p) or "" for p in ["registry/relations.tsv"] +
                                        ["registry/relations.d/" + n for n in ov.names("registry/relations.d")])
                        have = ov.text(path) or "src\tkind\tdst\tevidence_url\tdate\treason\n"
                        if "\t".join([op["src"], op["kind"], op["dst"]]) + "\t" not in known:
                            ov.set(path, have.rstrip("\n") + "\n" + row + "\n")
                            led.line(u["id"], "relate", op["src"], reason="%s %s" % (op["kind"], op["dst"]), ev=op["evidence"])
                            units_promote(op["evidence"], lane, ov)
                        tally["related"] += 1
                    elif kind == "open_question":
                        q = {"id": "%s-%s-q%02d" % (run, u["id"], tally["questions"] + 1), "kind": "verify" if op.get("rids") else "discover",
                             "topic": op.get("topic") or u["topic"], "question": op["question"].strip(), "why": op.get("why"),
                             "scope": {"rids": op["rids"]} if op.get("rids") else {"new": {"topic": op.get("topic") or u["topic"], "slice": op["question"][:80]}},
                             "origin": "%s/%s" % (run, u["id"]), "created": stamp()}
                        ov.set("queue/%s.json" % q["id"], json_bytes(q))
                        tally["questions"] += 1
                    elif kind == "add_record":
                        draft = json.loads(open(os.path.join(lane, op["draft"]), encoding="utf-8").read())
                        dup = find_duplicate(index, ov, draft)
                        held = None
                        if dup:
                            h = state.holder(repo, "rid:" + dup)
                            # the same run's integrated units hold its records until the merge: that is this branch
                            if h and not (h[0] == run and (h[1] == u["id"] or h[1] in done_units)):
                                held = h
                        if held:
                            conflict(op, "a draft for %s, which %s/%s holds; settle it after that unit lands" % (dup, held[0], held[1]),
                                     {"rid": dup})
                            continue
                        if not dup:
                            other = find_pending(repo, run, draft)
                            if other:
                                conflict(op, "run %s adds this offer as %s; settle it after %s merges" % (other[0], other[1], other[0]),
                                         {"rid": other[1], "run": other[0]})
                                continue
                        if dup:
                            rec = doc(dup)
                            same_key = all(m.same(rec.get(k), draft.get(k)) for k in ("verdict",)) and \
                                (rec.get("identity_cost") or {}).get("kind") == (draft.get("identity_cost") or {}).get("kind")
                            if same_key:
                                for e in draft.get("evidence") or []:
                                    if add_evidence(rec, e):
                                        touched[dup][4].append(("append_evidence", {"evidence": e, "op": "append_evidence"}, None, True))
                                tally["corroborated"] += 1
                            else:
                                conflict(op, "a draft for an offer the corpus already holds as %s, with different verdict or identity" % dup,
                                         {"rid": dup, "verdict": rec.get("verdict"), "identity": (rec.get("identity_cost") or {}).get("kind")})
                            continue
                        rid = "%s/%s" % (draft["topic"], draft["slug"])
                        path = "dossier/%s.json" % rid
                        mv = units.main_view(repo)
                        if mv is not None and mv.commit != view.commit and mv.exists(path) and not ov.exists(path):
                            # main holds this record since the run's base (another run merged it): adding it here
                            # would meet main as an add/add conflict at land (G2-09)
                            conflict(op, "a draft for %s, which main holds since this run's base; land merges main in, "
                                         "and a reconcile unit adds this draft's evidence to it" % rid, {"rid": rid})
                            continue
                        errs = validate_in(view, draft)
                        if errs:
                            rejects.append((op, "draft does not validate: %s" % errs[0].get("message")))
                            continue
                        if checks.binding_missing(draft):
                            # the gate's binding check, which the schema leaves to the gate (W4-01)
                            rejects.append((op, "draft names no binding: %s" % checks.BINDING_HINT))
                            continue
                        viol = [v for v in checks.record_violations(dict(draft, _rid=rid), repo, lane=lane, view=view)
                                if checks.is_error(v[0], v[1])]
                        if viol:
                            rejects.append((op, "draft breaks %s" % ", ".join(sorted({v[0] for v in viol}))))
                            continue
                        for e in draft.get("evidence") or []:
                            units_promote(e, lane, ov)
                        ov.set(path, json.dumps(draft, ensure_ascii=False, indent=2) + "\n")
                        index.add(rid, draft)
                        created.append((rid, draft))
                        led.line(u["id"], "add_record", rid, reason="new record")
                        tally["added"] += 1
                except Fail as e:
                    rejects.append((op, str(e)))
                except (KeyError, ValueError, TypeError) as e:
                    rejects.append((op, "malformed operation: %s" % e))
            # write each touched record once: validate, then the record's error rules against the baseline
            written = collections.Counter()
            for rid, (p, text, root, rec, done) in sorted(touched.items()):
                if not done:
                    continue
                try:
                    new_text = record_text(view, rid, text, root, rec)
                except Fail as e:
                    rejects += [(d[1], "record would not validate: %s" % e) for d in done]
                    tally["rejected-record"] += 1
                    continue
                viol = [(ru, k) for ru, k, _ in checks.record_violations(dict(rec, _rid=rid), repo, lane=lane, view=view)
                        if checks.is_error(ru, k) and k not in base.get(ru, set())]
                if checks.binding_missing(rec) and not checks.binding_missing(json.loads(text)):
                    # a change that raises the rung of a record with no binding fails the gate's binding check (W4-01)
                    rejects += [(d[1], "the change would fail the gate's binding check: %s" % checks.BINDING_HINT)
                                for d in done]
                    tally["rejected-record"] += 1
                    continue
                if viol:
                    rejects += [(d[1], "the change would add rule violation(s) %s" % ", ".join(sorted({v[0] for v in viol}))) for d in done]
                    tally["rejected-record"] += 1
                    continue
                lost = checks.uncited_sources(json.loads(text), rec)
                if lost:
                    # a field still names the page as its source, and no evidence row would cite it any more
                    rejects += [(d[1], "the change would leave %s, which a field names as its source, with no evidence "
                                       "row: %s" % (", ".join(lost), checks.UNCITED_HINT)) for d in done]
                    tally["rejected-record"] += 1
                    continue
                ov.set(p, new_text)
                index.add(rid, rec)
                for d in done:
                    op = d[1]
                    written[d[0]] += 1
                    if "evidence" in op:
                        units_promote(op["evidence"], lane, ov)
                    if d[0] == "set":
                        led.line(u["id"], "set", rid, op["path"], d[2], op["new"], op.get("rung"), op["evidence"], op.get("reason"), d[3])
                    elif d[0] == "dead":
                        led.line(u["id"], "dead", rid, "$.verdict", d[2], "dead", None, op["evidence"], op.get("cause"), d[3])
                    elif d[0] == "basis":
                        led.line(u["id"], "basis", rid, "$.extras.verified_at_basis", d[2],
                                 rec["extras"]["verified_at_basis"], None, None, "a confirm with no field left unread")
                    elif d[0] == "confirm":
                        led.line(u["id"], "confirm", rid, "$.verified_at", d[2], rec["verified_at"], op.get("rung"), op["evidence"],
                                 ", ".join(op.get("paths") or []), d[3], unread=op.get("unread"))
                    elif d[0] == "drop_evidence":
                        led.line(u["id"], "drop_evidence", rid, reason=op["reason"].strip(), dropped=d[2], index=d[3])
                    else:
                        led.line(u["id"], "append_evidence", rid, ev=op["evidence"], added=True)
            tally["rejected"] += len(rejects)
            removed = dict(u.get("queue_removed") or {})
            for qrel in queue_files_of(u):
                # only a queue file leaves the run branch here; never a record or any other path
                if units.QUEUE_FILE_RE.match(qrel or "") and ".." not in qrel and ov.exists(qrel):
                    # the queued question this unit answered leaves the queue with the unit's commit; its text is kept
                    # in the unit, so an undo puts it back (W4-03)
                    removed[qrel] = ov.text(qrel)
                    ov.remove(qrel)
            u["rejects"] = [{"op": o, "why": w} for o, w in rejects]
            u["conflicts"] = len(conflicts)
            u["tally"] = dict(tally)
            if removed:
                u["queue_removed"] = removed
            # the outcome is saved inside the attempt before the commit: a kill between the commit and the save of the
            # unit leaves it for recover_attempt, which would otherwise lose the rejects (G3-01)
            attempt["result"] = {"rejects": u["rejects"], "conflicts": u["conflicts"], "tally": u["tally"]}
            if removed:
                attempt["result"]["queue_removed"] = removed
            units.save_unit(u, repo)
            # the dropped evidence rows, when there are any, come second, inside the 100 bytes of the subject: a unit
            # that only dropped rows does not read as one that changed nothing. APPLIED_RE reads only the first count
            counts = "%d applied, %s%d confirmed, %d added, %d rejected, %d conflicts" % (
                written["set"], ("%d dropped, " % written["drop_evidence"]) if written["drop_evidence"] else "",
                written["confirm"], tally["added"], tally["rejected"], tally["conflict"])
            # commit_on cuts the subject to 100 bytes; the body keeps every count
            subj = subject(run, u["id"], counts) + "\n\n" + counts + "\n"
            new = commit_on(repo, units.ref_of(run), view.commit, changes, subj, view=view)
            test_stop("commit_on")  # the selftest's kill between the commit and the save of the unit (G-10)
            if new != view.commit:
                view.advance(new, changes)
                u["commit"] = new
            # the records the unit created are leased before the unit is saved without its attempt: a kill between
            # the two leaves the attempt, and recover_attempt leases them again (G-06)
            lease_created(repo, run, u, created)
            # its scope stays leased until the run merges or closes, however long it waits for land (G5-02)
            state.hold_unit(repo, run, u["id"])
            u.pop("attempt", None)
            u["status"] = "integrated"
            units.save_unit(u, repo)
            # a later unit of this call may dedupe onto a record this unit holds: that is the same branch
            done_units.add(u["id"])
            report.append((u["id"], "integrated (%s)" % relet if relet else "integrated", dict(tally), len(rejects)))
        except Exception as e:
            if not isinstance(e, (RefNotMoved, RefMoved)) and rev(repo, units.ref_of(run)) not in (None, attempt["old"]):
                # the unit's commit is on the branch and only its state was not saved (a refused rename on Windows):
                # unit.json still holds the attempt, the conflict lines stay, and the next integrate settles the unit
                # with recover_attempt (G-05)
                u["attempt"] = attempt
                report.append((u["id"], "committed, state not saved: %s; run scripts/rq integrate %s again"
                               % (str(e)[:120], run), {}, 0))
                continue
            # a unit that stops half-way leaves no write behind: the ref has not moved, the conflicts it logged are
            # taken back (a retry logs them again, once), and the unit goes back to its lane with the reason
            drop_attempt_lines(conflicts_path, attempt["id"])
            u.pop("attempt", None)
            if isinstance(e, (RefNotMoved, RefMoved)):
                # the ref could not be moved (a lock, or another writer): the unit is not at fault, so it stays ready
                # and the next integrate takes it; the units after it would meet the same ref, so this call stops
                # (G2-06)
                units.save_unit(u, repo)
                report.append((u["id"], "ready, not integrated: %s" % str(e)[:600], {}, 0))
                break
            u["status"], u["problems"] = "invalid", ["the integrator stopped on this unit and wrote nothing: %s" % e]
            units.save_unit(u, repo)
            report.append((u["id"], "invalid: %s" % str(e)[:120], {}, 1))
            continue
    return report


def queue_files_of(u):
    """The queue files a unit answers: the list a plan joined (queue_files), or the one file of a queue item."""
    return list(dict.fromkeys(list(u.get("queue_files") or []) + ([u["queue_file"]] if u.get("queue_file") else [])))


def undo_unit(run, uid, why, repo=REPO, view=None):
    """Undo one integrated unit on the run branch from its own ledger lines, newest first, as one commit.

    A value is restored only where the record still holds what the unit wrote; a value a later unit has
    changed since is left alone and returned, so it can go to reconcile. Evidence rows are removed only
    when this unit added them, and a row the unit dropped goes back to its place unless the record holds it again.
    Captures stay in sources/c/ and probe records in sources/p/ (content-addressed;
    another record may cite one). The caller holds the run lock; view advances to the new commit.
    -> (undone, skipped)."""
    m = fr()
    view = view if view is not None else units.run_tree(run, repo)
    changes = {}
    ov = Overlay(view, changes)
    led = Ledger(ov, run)
    docs, undone, skipped = {}, 0, []

    def doc(rid):
        if rid not in docs:
            p = "dossier/%s.json" % rid
            text = ov.text(p)
            docs[rid] = [p, text, m.parse_spans(text), json.loads(text)]
        return docs[rid][3]

    for l in reversed(ledger_lines(view, run, uid)):
        op, rid = l.get("op"), l.get("rid")
        if op in ("undo", "undo_skipped", "relate"):
            continue
        if op == "add_record":
            p = "dossier/%s.json" % rid
            if ov.exists(p):
                ov.remove(p)
                docs.pop(rid, None)
                led.line(uid, "undo", rid, reason="%s: the record this unit added is removed from the run branch" % why)
                undone += 1
            continue
        if not ov.exists("dossier/%s.json" % rid):
            continue
        rec = doc(rid)
        if op == "drop_evidence":
            row = l.get("evidence")
            evl = rec.setdefault("evidence", [])
            if isinstance(row, dict) and not any(isinstance(e, dict) and e == row for e in evl):
                at = l.get("index")
                evl.insert(at if isinstance(at, int) and 0 <= at <= len(evl) else len(evl), row)
                led.line(uid, "undo", rid, reason="%s: the evidence row this unit dropped is back" % why)
                undone += 1
            continue
        if l.get("path"):
            segs = m.parse_jpath(l["path"])
            cur = m.get_path(rec, segs)
            if cur is not m.ABSENT and m.same(cur, l.get("new")):
                if l.get("absent"):
                    # the unit created this key or appended this list item; lines run newest first, so an
                    # appended item is the list's last one when its turn comes
                    parent = m.get_path(rec, segs[:-1]) if len(segs) > 1 else rec
                    if isinstance(parent, dict):
                        parent.pop(segs[-1], None)
                    elif isinstance(parent, list) and segs[-1] == len(parent) - 1:
                        parent.pop()
                    else:
                        skipped.append({"rid": rid, "path": l["path"], "wrote": l.get("new"), "now": cur})
                        continue
                else:
                    m.set_path(rec, segs, l.get("old"))
                if op == "dead" and isinstance(rec.get("extras"), dict):
                    rec["extras"].pop("death", None)
                    if not rec["extras"]:
                        rec.pop("extras")
                led.line(uid, "undo", rid, l["path"], cur, l.get("old"), reason=why)
                undone += 1
            elif op != "confirm":
                skipped.append({"rid": rid, "path": l["path"], "wrote": l.get("new"),
                                "now": None if cur is m.ABSENT else cur})
        if l.get("added") and l.get("evidence"):
            row = l["evidence"]
            evl = rec.get("evidence") or []
            for i, e in enumerate(evl):
                if isinstance(e, dict) and all(e.get(k) == row.get(k) for k in ("url", "date", "proved", "quote", "capture")):
                    del evl[i]
                    undone += 1
                    break
    for rid, (p, text, root, rec) in sorted(docs.items()):
        ov.set(p, record_text(view, rid, text, root, rec))
    for s in skipped:
        # in the undo commit itself: a score killed before it saved the target reads these back (G2-07)
        led.line(uid, "undo_skipped", s["rid"], s["path"], s["wrote"], s["now"],
                 reason="%s: a later unit changed this value since; it is not undone" % why)
    rel = "registry/relations.d/%s-%s.tsv" % (run, uid)
    if ov.exists(rel):
        ov.remove(rel)
        undone += 1
    # the queue as it was before the unit: the questions it answered go back (W4-03), and the open questions it filed
    # leave with it, since the queued re-run asks them again (W4-08)
    u = units.load_unit(run, uid, repo) if os.path.exists(os.path.join(units.unit_dir(run, uid, repo), "unit.json")) else {}
    removed = dict(u.get("queue_removed") or {})
    missing = [q for q in queue_files_of(u) if q not in removed]
    if missing and u.get("commit"):
        # a unit integrated before its unit.json kept the removed text: the queue file is read from the parent of its
        # commit, the tree it was taken out of
        from common import TreeView
        try:
            before = TreeView(repo, u["commit"] + "^")
        except Fail:
            before = None
        for qrel in missing:
            b = before.read(qrel) if before is not None and units.QUEUE_FILE_RE.match(qrel or "") else None
            if b:
                removed[qrel] = b.decode("utf-8")
    for qrel, text in sorted(removed.items()):
        if text is not None and units.QUEUE_FILE_RE.match(qrel or "") and ".." not in qrel and not ov.exists(qrel):
            ov.set(qrel, text)
            undone += 1
    prefix = "%s-%s-q" % (run, uid)
    for name in ov.names("queue"):
        if name.startswith(prefix) and re.match(r"^\d{2}\.json$", name[len(prefix):]):
            ov.remove("queue/" + name)
            undone += 1
    new = commit_on(repo, units.ref_of(run), view.commit, changes, subject(run, uid, "undone, %s" % why), view=view)
    if new != view.commit:
        view.advance(new, changes)
    return undone, skipped


def units_promote(ev, lane, ov):
    cap = (ev or {}).get("capture")
    if cap:
        _, files = promote_files(cap, lane, ov)
        for p, data in files.items():
            ov.set(p, data)


def state_release_unit(repo, run, u):
    state.release_unit(repo, run, u["id"])


def usable_conflict(c):
    """A conflicts.jsonl row that names its op: a line that a kill cut in the middle of append_jsonl reads as
    {"_bad": ...} and is skipped, never indexed (G7-08)."""
    return isinstance(c, dict) and "_bad" not in c and isinstance(c.get("op"), dict)


def reconcile_specs(run, repo=REPO):
    """Turn this run's open conflicts into reconcile unit specs (one per record)."""
    by_rid = collections.defaultdict(list)
    bad = 0
    for c in read_jsonl(os.path.join(run_dir(run, repo), "conflicts.jsonl")):
        if c.get("handled"):
            continue
        if not usable_conflict(c):
            bad += 1
            continue
        op = c["op"]
        rid = op.get("rid") or (c.get("current") or {}).get("rid")
        if rid:
            by_rid[rid].append(c)
    specs = []
    for rid, cs in sorted(by_rid.items()):
        lines = []
        for c in cs:
            op = c["op"]
            ev = op.get("evidence") or {}
            lines.append("%s %s: proposed %s (evidence %s, capture %s, quote %r); now %s. Why it did not apply: %s" % (
                op.get("op"), op.get("path") or op.get("draft") or "", json.dumps(op.get("new"), ensure_ascii=False)[:160],
                ev.get("url"), (ev.get("capture") or "")[:20], (ev.get("quote") or "")[:120],
                json.dumps(c.get("current"), ensure_ascii=False)[:160], c.get("why") or "not recorded"))
        specs.append({"kind": "reconcile", "topic": rid.split("/")[0],
                      "question": "Settle these disagreements on %s from captured sources (re-capture the pages if needed). "
                                  "Propose the correct value with set, or confirm the current one:\n" % rid + "\n".join("  - " + x for x in lines),
                      "scope": {"rids": [rid]}, "origin": "conflict"})
    if bad:
        print("rq: %d line(s) of .tmp/%s/conflicts.jsonl are not whole JSON (a write cut by a kill) and were skipped; "
              "the next plan --conflicts marks them handled" % (bad, run), file=sys.stderr)
    return specs
