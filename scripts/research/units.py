"""Runs and units: open a run, show planning context, plan units with leases, render lane briefs, lint a
lane workspace, collect receipts, report status. Harness-agnostic: lanes are told to read a file.

A run is a folder, .tmp/<run>/, and a git ref, refs/heads/rq/<run>, that exists only as objects: no worktree. A lane
reads a record as the run holds it with `scripts/rq show RUN RID`; lint and plan read it from the ref."""
import collections
import functools
import glob
import json
import os
import re
import sqlite3
import sys

import state
import track
from common import (BASE, CAUSES, DONE_PHASES, KINDS, LADDER, OPS, REPO, RELATIONS, RID_RE, SHA_RE, Fail, TreeView,
                    capture_kind, claim_numbers, fetch, fr, fshy, git, is_ancestor, missing_numbers, probe_targets,
                    quote_found, read_capture, read_json, read_jsonl, rev, run_dir, stamp, stamp_ms, status_paths, today,
                    extra_worktrees, short_ref, upstream, upstream_shadowed, utf8_problem, validate_in, write_json)

TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
RUN_KINDS = ["research", "expand", "verify", "amend", "reconcile", "maintain"]
RQ = "scripts/rq"
QUEUE_FILE_RE = re.compile(r"^queue/[A-Za-z0-9][A-Za-z0-9._-]*\.json$")
QUEUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


# ---------------------------------------------------------------------------------------------- runs

def slugify(s, n=40):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:n].strip("-") or "x"


def load_run(run, repo=REPO):
    r = read_json(os.path.join(run_dir(run, repo), "run.json"))
    if not r:
        raise Fail("no run %s (scripts/rq status lists runs)" % run, 2)
    return r


def save_run(r, repo=REPO):
    write_json(os.path.join(run_dir(r["run"], repo), "run.json"), r)


def unit_dir(run, uid, repo=REPO):
    return os.path.join(run_dir(run, repo), "units", uid)


def load_unit(run, uid, repo=REPO):
    u = read_json(os.path.join(unit_dir(run, uid, repo), "unit.json"))
    if not u:
        raise Fail("no unit %s in run %s" % (uid, run), 2)
    return u


def save_unit(u, repo=REPO):
    write_json(os.path.join(unit_dir(u["run"], u["id"], repo), "unit.json"), u)


def units_of(run, repo=REPO):
    out = []
    for p in sorted(glob.glob(os.path.join(run_dir(run, repo), "units", "*", "unit.json"))):
        out.append(read_json(p))
    return out


def all_runs(repo=REPO):
    """Every run folder of this checkout: .tmp/*/run.json."""
    out = []
    for p in sorted(glob.glob(os.path.join(repo, ".tmp", "*", "run.json"))):
        r = read_json(p, None)
        if isinstance(r, dict) and r.get("run"):
            out.append(r)
    return out


def topics(repo=REPO):
    """The topics of main's schema: a topic added on main is open before the checkout's next scripts/rq sync."""
    return schema_of(repo)["properties"]["topic"]["enum"]


def ref_of(run):
    return "refs/heads/rq/" + run


def run_tree(run, repo=REPO):
    """The run branch as it is now, read from git objects (no worktree). A missing ref is made again only where that
    loses nothing: from the base in phase opening or open (an open killed after the folder), or from origin/rq/<run>
    before the merge. Never from the base after a unit was integrated or the run landed: a ref that a merge deleted
    made again at the base would show the run's records as the base had them (G-01)."""
    tip = rev(repo, ref_of(run))
    if tip:
        return TreeView(repo, tip)  # the view from the commit: one rev-parse, not two (LIO7-03)
    if not tip:
        r = load_run(run, repo)
        remote = rev(repo, "refs/remotes/origin/rq/%s" % run)
        if r.get("phase") in ("opening", "open") and r.get("base"):
            git(repo, "update-ref", ref_of(run), r["base"], "")
        elif remote and r.get("phase") not in DONE_PHASES:
            git(repo, "update-ref", ref_of(run), remote, "")
        else:
            raise Fail("run %s (phase %s) has no branch rq/%s here or on origin; a merged run is read on main "
                       "(scripts/rq report %s)" % (run, r.get("phase"), run, run), 1)
    return TreeView(repo, ref_of(run))


def open_run(kind, topic, details, repo=REPO, no_issue=False, research_issue=None):
    """The run's ref first (an id collision stops here, before anything is written), then the folder, registered in
    the transaction that checks for a drain or a wipe, then run.json in phase `opening`, then the claim, then phase
    `open`. A run left in `opening` by a kill is closed with scripts/rq close RUN --reason "..."."""
    if kind not in RUN_KINDS:
        raise Fail("kind must be one of %s" % ", ".join(RUN_KINDS), 2)
    if topic not in topics(repo):
        raise Fail("topic must be one of %s" % ", ".join(topics(repo)), 2)
    import secrets
    # the random part keeps apart two parents that open the same kind and topic in one minute
    run = "%s-%s-%s-%s" % (stamp().replace("-", "").replace(":", "")[:13].replace("T", "-"), kind, topic, secrets.token_hex(2))
    d = run_dir(run, repo)
    if os.path.exists(d):
        raise Fail("run %s exists already" % run, 1)
    fetch(repo, [BASE])
    up = upstream(repo)
    head = git(repo, "rev-parse", "HEAD")
    if not is_ancestor(repo, head, up):
        raise Fail("the checkout's HEAD %s is not in %s: the research checkout stays on %s and moves only with the merge "
                   "session's scripts/rq sync (AGENTS.md section 2 rule 14). No run opens on a feature branch"
                   % (head[:10], short_ref(up), BASE), 1)
    behind = git(repo, "rev-list", "--count", "%s..%s" % (head, up), check=False)
    base = git(repo, "rev-parse", up)
    # an empty old value refuses an existing ref: a collision of two run ids stops here
    git(repo, "update-ref", ref_of(run), base, "")
    try:
        state.register_folder(repo, run, "run", holder="pid %d" % os.getpid())
    except Fail:
        git(repo, "update-ref", "-d", ref_of(run), base)
        raise
    r = {"run": run, "kind": kind, "topic": topic, "request": details.strip(), "created": stamp(), "base": base,
         "phase": "opening", "issue": None, "branch": "rq/" + run, "rounds": 0}
    save_run(r, repo)
    from common import test_stop
    test_stop("open")  # the selftest's kill after the ref and run.json: rq close closes a run left in opening
    if research_issue:
        # the claim comes before phase open: a taken issue leaves a run in `opening`, which close gives back. run.json
        # names the issue first, so rq close gives back a claim that a kill during the claim left on GitHub
        from common import SETTINGS, utc_now
        r["claiming"] = int(research_issue)
        save_run(r, repo)
        info = {}
        try:
            written, msg = track.claim(int(research_issue), run, int(SETTINGS.get("claim_hours", 24)), utc_now(), repo,
                                       topic, info=info)
        except Fail:
            r["phase"] = "closed"
            r["closed"] = {"at": stamp(), "reason": "the claim of issue #%s was refused" % research_issue}
            save_run(r, repo)
            git(repo, "update-ref", "-d", ref_of(run), base, check=False)
            raise
        r["research_issue"] = int(research_issue)
        r.pop("claiming", None)
        r["claim"] = msg
        if "per_topic" in info:
            r["per_topic_issue"] = bool(info["per_topic"])
    r["phase"] = "open"
    if behind and behind != "0":
        r["head_behind"] = int(behind)
    save_run(r, repo)
    if not no_issue:
        r["issue"] = track.open_issue(r, repo)
        save_run(r, repo)
    return r


def reconcile_merged(repo=REPO, fetched=False):
    """A run in review whose local tip is in origin/main has merged, also when a merge session merged it in its own
    clone: its leases and pending new records go. Its phase stays in-review until rq merge (or the wipe after the
    `rq merged:` comment) sets it, so a merge that stopped half-way is still found. -> the runs released."""
    runs = {r[1] for r in state.leases(repo, live=False)} | {p[0] for p in state.pending(repo)}
    cand = []
    for run in sorted(runs):
        try:
            r = read_json(os.path.join(run_dir(run, repo), "run.json"), None)
        except Fail:
            r = None
        if isinstance(r, dict) and r.get("phase") == "in-review":
            cand.append(run)
    if not cand:
        return []
    if not fetched:
        fetch(repo, [BASE])
    up = upstream(repo)
    out = []
    for run in cand:
        tip = rev(repo, ref_of(run))
        if tip and is_ancestor(repo, tip, up):
            state.release(repo, run)
            out.append(run)
    return out


# ---------------------------------------------------------------------------------------------- context

def store_db(repo=REPO):
    """The shared store of the checkout's HEAD: built once for the machine, under a lock, and read by every agent
    (scripts/fshy/fr.py ensure_fresh). No run builds a store of its own."""
    m = fr()
    p = m.ensure_store(repo)
    con = sqlite3.connect("file:%s?mode=ro" % p.replace("\\", "/"), uri=True)
    _OPEN.append(con)
    return con


_OPEN = []


def close_stores():
    """Close every store connection this process opened: an open one holds the store file, and a folder that holds
    it cannot be removed on Windows (the selftest's clone)."""
    while _OPEN:
        try:
            _OPEN.pop().close()
        except Exception:
            pass


def context(topic, repo=REPO):
    """What a parent needs to plan a run on a topic, in about 15 lines."""
    db = store_db(repo)
    q = lambda s, a=(): db.execute(s, a).fetchall()
    out = ["# context for %s (store built from %s)" % (topic, q("SELECT value FROM meta WHERE key='commit'")[0][0][:10])]
    grp = q("SELECT grp, count(*) FROM record WHERE topic=? GROUP BY grp ORDER BY 2 DESC", (topic,))
    out.append(("records: " + ", ".join("%s %d" % g for g in grp) + "; total %d" % sum(g[1] for g in grp)) if grp
               else "records: none yet (the first record the integrator writes makes dossier/%s/)" % topic)
    cats = q("SELECT lower(category), count(*) FROM record WHERE topic=? AND grp='usable' GROUP BY 1 ORDER BY 2 DESC LIMIT 8", (topic,))
    out.append("usable categories: " + ("; ".join("%s %d" % c for c in cats) if cats else "none yet"))
    soon = q("SELECT count(*) FROM record WHERE topic=? AND stale_on <= date('now','+14 day')", (topic,))[0][0]
    stale_now = q("SELECT count(*) FROM record WHERE topic=? AND stale_on <= date('now')", (topic,))[0][0]
    inh = q("SELECT count(*) FROM record WHERE topic=? AND verified_basis='inherited' AND grp='usable'", (topic,))[0][0]
    unp = q("SELECT count(DISTINCT rid) FROM claim WHERE parse='unparsed' AND rid LIKE ?", (topic + "/%",))[0][0]
    drift = q("SELECT count(*) FROM drift WHERE subject LIKE ?", (topic + "/%",))[0][0]
    try:
        held = q("SELECT count(DISTINCT rid) FROM strip_log WHERE rule LIKE '%-held' AND rid LIKE ?", (topic + "/%",))[0][0]
    except sqlite3.Error:
        held = 0
    out.append("worklists: stale now %d, stale within 14 d %d, usable but inherited (never re-checked) %d, "
               "unparsed numbers %d records, duplicate disagreements %d, held clauses %d records"
               % (stale_now, soon, inh, unp, drift, held))
    out.append("  generate verify units from them: %s plan RUN --from-worklist stale|inherited|unparsed|held|drift --batch 6 "
               "(every row of the worklist, in units of --batch records, all started at once)" % RQ)
    # the registered sources, the queue and BRIEF.md as main holds them: the checkout's HEAD moves only with
    # scripts/rq sync, so its working tree can list a queue item that main has answered already (G-11)
    mv = main_view(repo)
    srcs = []
    for fn, (mode, oid) in sorted(((mv.listdir("scripts/sources") if mv else None) or {}).items()):
        if not fn.endswith("aggregators.tsv"):
            continue
        for row in parse_tsv(mv.blob(oid).decode("utf-8")):
            if (row.get("topic") or "compute") == topic and row.get("status") == "active":
                srcs.append("%s %s (last diff %s, missing %s; list scripts/sources/%s)" % (
                    row["slug"], row["url"], row.get("last_diff"), row.get("missing"), fn))
    out.append("registered sources for discovery slices (%d):" % len(srcs))
    out += ["  " + s for s in srcs[:12]] + (["  ... %d more" % (len(srcs) - 12)] if len(srcs) > 12 else [])
    qu = []
    for fn, (mode, oid) in sorted(((mv.listdir("queue") if mv else None) or {}).items()):
        if fn.endswith(".json"):
            try:
                qu.append(json.loads(mv.blob(oid).decode("utf-8")))
            except ValueError:
                pass
    qu = [u for u in qu if isinstance(u, dict) and u.get("topic") == topic]
    out.append("queued units for this topic (%d): %s" % (len(qu), "; ".join("%s %s" % (u["id"], u["question"][:70]) for u in qu[:6])))
    bb = mv.read("BRIEF.md") if mv else None
    brief = (bb.decode("utf-8") if bb else open(os.path.join(repo, "BRIEF.md"), encoding="utf-8").read()).split("\n")
    # only the lines that point into the topic (the generated table row, a cited record or document), not prose
    hits = [ln.strip()[:150] for ln in brief if ("docs/%s/" % topic) in ln or ("dossier/%s/" % topic) in ln][:6]
    out.append("BRIEF.md lines that point into %s (%d):" % (topic, len(hits)))
    out += ["  " + h for h in hits]
    live = state.leases(repo)
    out.append("live leases on other runs: %d" % len([l for l in live if l[0].split(":", 2)[1:2] and topic in l[0]]))
    return "\n".join(out)


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        return parse_tsv(f.read())


def parse_tsv(text):
    rows, hdr = [], None
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        c = ln.rstrip("\r").split("\t")
        if hdr is None:
            hdr = c
            continue
        rows.append(dict(zip(hdr, c)))
    return rows


# ---------------------------------------------------------------------------------------------- planning

def validate_unit_spec(spec, topic, view=None):
    kind = spec.get("kind")
    if kind not in KINDS or kind == "audit":
        raise Fail("unit kind must be one of %s" % ", ".join(k for k in KINDS if k != "audit"), 2)
    if not (spec.get("question") or "").strip():
        raise Fail("every unit needs a question", 2)
    sc = spec.get("scope") or {}
    rids = sc.get("rids") or []
    for r in rids:
        if not RID_RE.match(r):
            raise Fail("bad rid %r" % r, 2)
        if view is not None and not view.exists("dossier/%s.json" % r):
            raise Fail("no record %s (dossier/%s.json on the run branch); scripts/fr search NAME finds the rid" % (r, r), 2)
    qfs = spec.get("queue_files")
    if qfs is not None:
        if not isinstance(qfs, list) or not all(isinstance(q, str) and QUEUE_FILE_RE.match(q) and ".." not in q for q in qfs):
            raise Fail("queue_files holds only queue/ID.json files: %r" % (qfs,), 2)
        for q in qfs:
            if view is not None and not view.exists(q):
                raise Fail("no queue file %s" % q, 2)
    new = sc.get("new") or {}
    if kind == "discover":
        if not (new.get("names") or new.get("slice")):
            raise Fail("a discover unit needs scope.new.names or scope.new.slice", 2)
        new.setdefault("topic", spec.get("topic") or topic)
    elif not rids:
        raise Fail("a %s unit needs scope.rids" % kind, 2)
    return spec


def existing_names(repo, topic):
    db = store_db(repo)
    return db.execute("SELECT rid, provider FROM record WHERE topic=?", (topic,)).fetchall()


UNIT_DONE = ("integrated", "reverted", "superseded", "abandoned")


def bring_main(r, view, specs, repo=REPO):
    """Before a plan leases anything: when main changed a record a unit names, or the record folder of a topic a
    discover unit drafts into, since the run branch last took main (another run merged), merge main into the run
    branch in git objects. The caller holds the run lock; view advances. -> a note, or None."""
    rids = sorted({x for sp in specs for x in ((sp.get("scope") or {}).get("rids") or []) if isinstance(x, str)})
    tops = sorted({((sp.get("scope") or {}).get("new") or {}).get("topic") or sp.get("topic")
                   for sp in specs if sp.get("kind") == "discover"} - {None})
    if not (rids or tops):
        return None
    fetch(repo, [BASE])
    upc = rev(repo, upstream(repo))
    if not upc or is_ancestor(repo, upc, view.commit):
        return None
    mv = TreeView(repo, upc)
    paths = ["dossier/%s.json" % x for x in rids] + ["dossier/%s" % t for t in tops]
    moved = [p for p in paths if mv.entry(p) != view.entry(p)]
    if not moved:
        return None
    import land
    land.merge_into(repo, r, view, view.commit, upc, "main", again="plan")
    return "main changed %s since this run took it; merged main into rq/%s in git objects before planning" % (
        ", ".join(moved[:4]) + (" and %d more" % (len(moved) - 4) if len(moved) > 4 else ""), r["run"])


def plan(run, specs, repo=REPO):
    r = load_run(run, repo)
    have = units_of(run, repo)
    n = len(have)
    made, problems = [], []
    known = None
    view = run_tree(run, repo)
    if any("max_captures" in (s or {}) for s in specs):  # an old plan field, ignored
        problems.append("max_captures is ignored: there is no page budget (AGENTS.md section 2 rule 15)")
    # a run in review whose tip is in main has merged: its leases go before this plan takes keys (L-20)
    reconcile_merged(repo)
    # what another run merged since this run's base is brought in first, so the lanes read the record as main holds it
    # and integrate's compare-and-set runs against it (G-04)
    note = bring_main(r, view, [dict(sp, topic=sp.get("topic") or r["topic"]) for sp in specs], repo)
    if note:
        problems.append(note)
    # every unit is checked before any is leased, so a plan file with one bad unit plans nothing (R3-B-17)
    checked = []
    for spec in specs:
        spec = dict(spec)
        spec.pop("max_captures", None)  # ignored: there is no page budget
        spec.setdefault("topic", r["topic"])
        if r.get("per_topic_issue") and spec["topic"] != r["topic"]:
            # an issue run once for each topic: each topic's bullets belong to that topic's run and claim (W5-01)
            raise Fail("issue #%s is run once for each topic, and this run claimed it for %s: plan only the bullets whose "
                       "topic is %s or that name none. The %s bullet %r belongs to a run of topic %s (scripts/rq open "
                       "KIND %s \"...\" --issue %s)" % (r.get("research_issue"), r["topic"], r["topic"], spec["topic"],
                                                       (spec.get("question") or "")[:60], spec["topic"], spec["topic"],
                                                       r.get("research_issue")), 2)
        validate_unit_spec(spec, r["topic"], view)
        checked.append(spec)
    done_units = {u["id"] for u in have if u["status"] in UNIT_DONE}
    for spec in checked:
        n += 1
        uid = "u%02d" % n
        u = {"id": uid, "run": run, "kind": spec["kind"], "topic": spec["topic"], "question": spec["question"].strip(),
             "scope": spec.get("scope") or {}, "seeds": spec.get("seeds") or [],
             "origin": spec.get("origin") or "parent", "status": "planned", "created": stamp()}
        for k in ("leads", "issue", "queue_id"):  # an intake item: the reporter's links and the public issue it answers
            if spec.get(k):
                u[k] = spec[k]
        if u["kind"] == "discover" and u["scope"].get("new", {}).get("names"):
            known = known or existing_names(repo, u["topic"])
            for name in u["scope"]["new"]["names"]:
                # whole words of the provider name, whole hyphen parts of the slug: "Tebi" is not "hastebin"
                word = re.compile(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(name.lower()))
                part = re.compile(r"(?:^|[/-])%s(?:-|$)" % re.escape(slugify(name)))
                hits = [rid for rid, prov in known if word.search((prov or "").lower()) or part.search(rid)]
                if hits:
                    problems.append("%s: %r looks like existing %s; a draft for it will be merged as corroboration "
                                    "or turned into a conflict" % (uid, name, ", ".join(hits[:3])))
        try:
            u["fence"] = state.acquire(repo, run, u, done_units)
        except Fail as e:
            problems.append("%s not planned: %s" % (uid, e))
            n -= 1
            continue
        # the queue files the unit answers, before its brief: the brief lists each one's question (W4-02)
        if spec.get("queue_file"):
            u["queue_file"] = spec["queue_file"]
        if spec.get("queue_files"):
            u["queue_files"] = list(spec["queue_files"])
        d = unit_dir(run, uid, repo)
        for sub in ("captures", "new", "probe", "tmp"):
            os.makedirs(os.path.join(d, sub), exist_ok=True)
        save_unit(u, repo)
        write_brief(u, repo)
        made.append(u)
    r["phase"] = "planned"
    save_run(r, repo)
    if made:
        track.comment(r, "planned %d unit(s):\n%s" % (len(made), "\n".join(
            "- `%s` %s: %s" % (u["id"], u["kind"], u["question"][:140]) for u in made)), repo)
    return made, problems


def from_worklist(run, kind, topic, batch=6, repo=REPO):
    """Verify units from a worklist of the shared store, --batch records each. Every row of the worklist is planned:
    there is no unit budget and no unit cap, and every unit starts at once (AGENTS.md section 2 rule 15; W5-11)."""
    db = store_db(repo)
    q = lambda s, a=(): [x[0] for x in db.execute(s, a).fetchall()]
    t = topic + "/%"
    if kind == "stale":
        rids = q("SELECT rid FROM record WHERE rid LIKE ? AND grp<>'dead' ORDER BY self_hosted, stale_on, vorder", (t,))
        question = "Re-check these records against their sources; confirm what still holds and correct what changed."
    elif kind == "inherited":
        rids = q("SELECT rid FROM record WHERE rid LIKE ? AND verified_basis='inherited' AND grp='usable' "
                 "ORDER BY self_hosted, vorder, stale_on", (t,))
        question = "These usable records were never re-checked against the live service: re-read each offer, " \
                   "capture the page, confirm or correct the free tier, identity and limits."
    elif kind == "unparsed":
        rids = q("SELECT DISTINCT c.rid FROM claim c JOIN record r USING (rid) WHERE c.rid LIKE ? AND c.parse='unparsed' "
                 "AND r.grp IN ('usable','paid','trial') ORDER BY r.self_hosted, r.vorder", (t,))
        question = "These records state quotas or prices no number could be parsed from: re-read the source and restate " \
                   "each as a number with its unit and period, quoted."
    elif kind == "held":
        rids = q("SELECT s.rid FROM strip_log s JOIN record r ON r.rid = s.rid WHERE s.rule LIKE '%-held' AND s.rid LIKE ? "
                 "GROUP BY s.rid ORDER BY r.self_hosted, r.vorder, s.rid", (t,))
        question = "These records mix a technical number with process or terms wording: restate the technical content " \
                   "as a clean value from a captured source; move nothing narrative into a field."
    elif kind == "drift":
        # pairs that share a record are one unit: two units on one record would be refused by its lease; a self-hosted
        # subject's pairs come last, and its pairs stay together for the grouping
        pairs = db.execute("SELECT d.subject, d.other, d.field, d.a, d.b FROM drift d LEFT JOIN record r ON r.rid = d.subject "
                           "WHERE d.subject LIKE ? ORDER BY coalesce(r.self_hosted, 0), d.subject, d.other", (t,)).fetchall()
        groups, left = [], 0
        for a, b, f, va, vb in pairs:
            hit = [g for g in groups if a in g["rids"] or b in g["rids"]]
            g = {"rids": {a, b}, "lines": ["%s and %s disagree on %s (%s vs %s)" % (a, b, f, va, vb)]}
            if len(set().union(g["rids"], *[h["rids"] for h in hit])) > max(batch, 2):
                left += 1  # the group would be too large for one unit; the pair waits for a later run
                continue
            for h in hit:
                g["rids"] |= h["rids"]
                g["lines"] = h["lines"] + g["lines"]
                groups.remove(h)
            groups.append(g)
        specs = [{"kind": "reconcile", "question": "These records disagree: " + "; ".join(g["lines"]) + ". Decide from captured "
                  "sources which are one offer (relate duplicate_of) and which are two, and correct the wrong value.",
                  "scope": {"rids": sorted(g["rids"])}} for g in groups]
        made, problems = plan(run, specs, repo)
        if left:
            problems.append("%d drift pair(s) left for a later run (a group larger than --batch)" % left)
        return made, problems
    else:
        raise Fail("worklist must be stale, inherited, unparsed, held or drift", 2)
    specs = []
    for i in range(0, len(rids), batch):
        chunk = rids[i:i + batch]
        if chunk:
            specs.append({"kind": "verify", "question": question, "scope": {"rids": chunk}})
    return plan(run, specs, repo)


# ---------------------------------------------------------------------------------------------- briefs

def schema_of(repo=REPO, view=None):
    """The schema of a tree: the run branch's for a lane brief (integrate validates against it), else main's. Research
    never moves the checkout's HEAD, so the working tree's copy can be older than both."""
    v = view if view is not None else main_view(repo)
    b = v.read("scripts/dossier/schema.json") if v is not None else None
    return json.loads(b.decode("utf-8")) if b else read_json(os.path.join(repo, "scripts", "dossier", "schema.json"))


_MAIN_VIEWS = {}


def main_view(repo=REPO):
    """origin/main (main without a remote) as git objects, one view per process and commit: topics, the queue, the
    registered sources and BRIEF.md are read from main, not from the checkout's working tree (G-11)."""
    c = rev(repo, upstream(repo))
    if not c:
        return None
    if (repo, c) not in _MAIN_VIEWS:
        _MAIN_VIEWS[(repo, c)] = TreeView(repo, c)
    return _MAIN_VIEWS[(repo, c)]


def vocab(repo=REPO, view=None):
    s = schema_of(repo, view)
    p = s["properties"]
    rows = [("verdict", p["verdict"]["enum"]), ("confidence (rung)", p["confidence"]["enum"]),
            ("identity_cost.kind", p["identity_cost"]["properties"]["kind"]["enum"]),
            ("limits[].kind", p["limits"]["items"]["properties"]["kind"]["enum"]),
            ("binding", p["binding"]["enum"]),
            ("interface[]", p["interface"]["items"]["enum"]),
            ("free_tier.unit", p["free_tier"]["properties"]["unit"]["enum"]),
            ("free_tier.metered_on", p["free_tier"]["properties"]["metered_on"]["enum"])]
    return "\n".join("- `%s`: %s" % (k, ", ".join("`%s`" % x for x in v)) for k, v in rows)


@functools.lru_cache(maxsize=None)
def example_record(topic, repo=REPO):
    """A record to copy the shape from: a clean one of the topic (usable, measured or documented, 8 to 15 evidence
    rows, no row in the baseline, so no known rule violation), or, for a topic with no record yet, one of another
    topic. The largest record is a poor model: it carries extras and narrative that a draft must not copy. Computed
    once per topic and process: a plan of ten units opens the store and reads the baseline once, not ten times."""
    import checks
    db = store_db(repo)
    base = checks.load_baseline(repo)
    dirty = {k.split("|")[0] for keys in base.values() for k in keys}
    q = ("SELECT rid, path FROM record WHERE %s grp='usable' AND confidence IN ('measured','documented') "
         "AND n_evidence BETWEEN 8 AND 15 ORDER BY n_evidence DESC, rid")
    for rid, path in db.execute(q % "topic=? AND", (topic,)).fetchall():
        if rid not in dirty:
            return "`%s`" % path
    q2 = ("SELECT path FROM record WHERE %s grp='usable' AND confidence IN ('measured','documented') "
          "ORDER BY n_evidence DESC LIMIT 1")
    row = db.execute(q2 % "topic=? AND", (topic,)).fetchone()
    if row:
        return "`%s`" % row[0]
    row = next(((path,) for rid, path in db.execute(q % "", ()).fetchall() if rid not in dirty), None)
    other = row[0] if row else "dossier/domains-dns/desec.json"
    return ("`%s`. No record of `%s` exists yet: copy that shape, set `topic` to `%s` and replace every value. "
            "The integrator makes the folder `dossier/%s/`" % (other, topic, topic, topic))


def registered_lists(repo=REPO):
    """(slug, url, list file) of every list registered in scripts/sources/*aggregators*.tsv on main."""
    mv = main_view(repo)
    if mv is None:
        return []
    key = (repo, mv.commit)
    if key not in _LISTS:
        rows = []
        for fn, (mode, oid) in sorted((mv.listdir("scripts/sources") or {}).items()):
            if "aggregators" in fn and fn.endswith(".tsv"):
                rows += [(r.get("slug"), r.get("url"), fn) for r in parse_tsv(mv.blob(oid).decode("utf-8")) if r.get("slug")]
        _LISTS[key] = rows
    return _LISTS[key]


_LISTS = {}


def scope_text(u):
    sc = u["scope"]
    lines = []
    if sc.get("rids"):
        lines += ["  - `%s` (read it as this run holds it: `%s show %s %s`)" % (r, RQ, u["run"], r) for r in sc["rids"]]
    new = sc.get("new") or {}
    if new.get("names"):
        lines.append("  - new `%s` records for: %s" % (new.get("topic"), ", ".join(new["names"])))
    if new.get("slice"):
        lines.append("  - new `%s` records found in the slice: %s" % (new.get("topic"), new["slice"]))
    if u["kind"] == "discover":
        lines.append("  - changes to existing records only if they are listed above; otherwise use `open_question`")
    return "\n".join(lines)


def queued_text(u, repo=REPO):
    """The queued questions a unit answers and its own question does not already carry: a plan file that names
    queue_files hands the lane only the parent's question, and the integrator takes those files out of the queue with
    the unit's commit, so the brief names each one (W4-02)."""
    files = list(dict.fromkeys(list(u.get("queue_files") or []) + ([u["queue_file"]] if u.get("queue_file") else [])))
    if not files:
        return ""
    view = run_tree(u["run"], repo)
    rows = []
    for rel in files:
        qid = rel[len("queue/"):-len(".json")] if rel.startswith("queue/") and rel.endswith(".json") else rel
        b = view.read(rel) if QUEUE_FILE_RE.match(rel or "") and ".." not in rel else None
        try:
            q = json.loads(b.decode("utf-8")) if b else {}
        except ValueError:
            q = {}
        text = " ".join(str(q.get("question") or "").split())
        if qid in u["question"] or (text and text in " ".join(u["question"].split())):
            continue  # the question already carries it (a queue item, or items a plan joined)
        rows.append("  - `%s`: %s" % (rel, text or "(the file is not on the run branch; its question is unknown)"))
    if not rows:
        return ""
    return ("\n- **Queued questions this unit answers:** the integrator takes these files out of the queue with your "
            "work. Answer each one, or add an `open_question` whose `question` names its id:\n" + "\n".join(rows))


def fix_section(fix):
    """The end of a brief that brief --fix rewrites: the problems a previous attempt left."""
    return ("\n## Fix these problems first\n\nA previous attempt left these problems. Fix each one, run the lint again, "
            "then rewrite the receipt.\n\n" + "\n".join("- " + p for p in fix) + "\n")


def write_brief(u, repo=REPO, fix=None):
    d = unit_dir(u["run"], u["id"], repo)
    rel = os.path.relpath(d, repo).replace("\\", "/")
    t = open(os.path.join(TEMPLATES, "lane.md"), encoding="utf-8").read()
    seeds = ", ".join(u["seeds"]) or ("your own search (`TMPDIR=%s/tmp sh scripts/broker/broker.sh search \"...\" --tsv`)"
                                     % rel)
    named = [(slug, fn) for slug, url, fn in registered_lists(repo)
             if any(sd == slug or (url and url.rstrip("/") in sd) for sd in u["seeds"])]
    if named:
        # the one line of a log.md that the parent reads (docs/research-protocol.md sections 2 and 5)
        seeds += ("; these seeds name the registered list(s) %s: write the list's covered and missing counts as the first "
                  "line of your log.md, as `covered N missing M`; the parent records them on the run branch"
                  % ", ".join("`%s` (scripts/sources/%s)" % x for x in named))
    if u.get("leads"):
        seeds += ("; the public report names these pages, which are a reporter's leads and never evidence on their own: "
                  "find the first-party page on the provider's own domain before you record a value: " + ", ".join(u["leads"]))
    text = t.format(run=u["run"], uid=u["id"], kind=u["kind"], topic=u["topic"], question=u["question"] + queued_text(u, repo),
                    scope=scope_text(u), seeds=seeds, workspace=rel, show_cmd="%s show %s" % (RQ, u["run"]),
                    capture_cmd="%s capture --lane %s" % (RQ, rel), check_cmd="%s capture --lane %s --check" % (RQ, rel),
                    lint_cmd="%s lint %s %s" % (RQ, u["run"], u["id"]), today=today(), now=stamp_ms(),
                    causes=", ".join(CAUSES), relations=", ".join(RELATIONS), vocab=vocab(repo, run_tree(u["run"], repo)),
                    example_record=example_record(u["topic"], repo))
    if fix:
        text += fix_section(fix)
    with open(os.path.join(d, "brief.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return os.path.join(rel, "brief.md")


def lane_instruction(u, repo=REPO):
    rel = os.path.relpath(unit_dir(u["run"], u["id"], repo), repo).replace("\\", "/")
    return "Read %s/brief.md and do exactly what it says. Reply with the path of %s/receipt.json and nothing else." % (rel, rel)


# ---------------------------------------------------------------------------------------------- lint

_PROJ = {}


def projector(repo=REPO):
    if "p" not in _PROJ:
        p = os.path.join(repo, "scripts", "fshy", "rules", "projection.json")
        rules = read_json(p if os.path.exists(p) else os.path.join(REPO, "scripts", "fshy", "rules", "projection.json"))
        _PROJ["p"] = fshy("project").Projector(rules, [])
    return _PROJ["p"]


NARRATIVE_CLASSES = ("narrative", "personal")


def narrative_rules(repo=REPO):
    """The rule ids C20 counts: the clause rules of class narrative or personal, and the pre-rewrites. A rule of
    class pointer (a path of a private file of this repository, such as a stored copy in sources/p/) is applied
    by the projection, which withholds it from the public build, and is not counted: a private record that cites
    the private evidence store is correct here. A legal rule is not counted either."""
    if "ids" not in _PROJ:
        rules = projector(repo).rules
        ids = {r["id"] for r in rules["clause_rules"] if r["class"] in NARRATIVE_CLASSES}
        ids |= {r["id"] for r in rules.get("pre_rewrite", [])}
        _PROJ["ids"] = ids
    return _PROJ["ids"]


def narrative_leaves(value, path="$.notes", repo=REPO):
    """-> [(leaf path, leaf value, rule, text)] for every string leaf holding process narrative or personal
    wording (projection rules of class narrative or personal). Evidence quotes are vendor text and exempt."""
    out = []
    counted = narrative_rules(repo)

    def walk(v, p):
        if isinstance(v, dict):
            for k, x in v.items():
                if k != "quote":
                    walk(x, "%s.%s" % (p, k))
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, "%s[%d]" % (p, i))
        elif isinstance(v, str):
            _, log = projector(repo).clean_prose(v, re.sub(r"\[\d+\]", "[]", p).lstrip("$."))
            for rule, before in log:
                if rule.split("-")[0] in counted:
                    out.append((p, v, rule, before))
                    break
    walk(value, path)
    return out


def narrative_hits(value, path="$.notes", repo=REPO):
    return ["%s: %s (%s)" % (p, rule, before[:80]) for p, _, rule, before in narrative_leaves(value, path, repo)]


def check_evidence(ev, lane, repo, where, view=None):
    """An evidence row a lane proposes: an http row cites a page capture, a probe: row cites a probe record
    registered with `rq capture --probe`; both carry a quote found in the text they cite."""
    probs = []
    if not isinstance(ev, dict):
        return ["%s: evidence must be an object" % where]
    url = ev.get("url") or ""
    if not re.match(r"^(https?://|probe:)", url):
        probs.append("%s: evidence.url must be http(s):// or probe:" % where)
    d = ev.get("date") or ""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", d) or d > today():
        probs.append("%s: evidence.date must be YYYY-MM-DD and not in the future" % where)
    if len((ev.get("proved") or "").strip()) < 8:
        probs.append("%s: evidence.proved must say what the source established" % where)
    if url.startswith(("http", "probe:")):
        probe = url.startswith("probe:")
        cap, quote = ev.get("capture") or "", ev.get("quote") or ""
        how = ("%s capture %s --lane WS --probe RECORD.json" % (RQ, url)) if probe else ("%s capture" % RQ)
        if not SHA_RE.match(cap):
            probs.append("%s: evidence.capture must be the sha256:... printed by %s" % (where, how))
        elif not quote.strip():
            probs.append("%s: evidence.quote is empty" % where)
        else:
            text = read_capture(cap, repo, lane, view)
            if text is None:
                probs.append("%s: capture %s is not in this workspace, sources/c/ or sources/p/, or its text no longer "
                             "hashes to its name (capture or register it again)" % (where, cap[:20]))
            else:
                verdict, score = quote_found(quote, text)
                if verdict == "miss":
                    probs.append("%s: quote not found in capture %s (best %.2f): %r" % (where, cap[:20], score, quote[:80]))
                if probe and capture_kind(cap, repo, lane, view) != "probe":
                    probs.append("%s: a probe: row cites a probe record; register it with %s" % (where, how))
                elif probe and url not in probe_targets(cap, repo, lane, view):
                    probs.append("%s: %s is not a target that probe record %s was registered for (%s); register it "
                                 "with %s" % (where, url, cap[:20], ", ".join(probe_targets(cap, repo, lane, view)) or "none", how))
    return probs


def measured_problem(op, where):
    """`measured` rests on a stored probe record: the op's evidence is a probe: row with a capture."""
    ev = op.get("evidence") if isinstance(op.get("evidence"), dict) else {}
    wants = op.get("rung") == "measured" or (op.get("op") == "set" and op.get("path") == "$.confidence"
                                            and op.get("new") == "measured")
    if wants and not ((ev.get("url") or "").startswith("probe:") and SHA_RE.match(ev.get("capture") or "")):
        return ["%s: measured needs a probe: evidence row that cites a probe record registered with "
                "%s capture probe:TARGET --lane WS --probe RECORD.json; otherwise propose documented or reported" % (where, RQ)]
    if op.get("op") == "set" and op.get("path") == "$.confidence" and op.get("new") == "measured" and op.get("rung") != "measured":
        return ["%s: a set of $.confidence to measured needs rung measured" % where]
    return []


def record_of(view, rid):
    """A record as the run branch holds it, parsed; None when the branch has no such record."""
    b = view.read("dossier/%s.json" % rid) if rid else None
    return json.loads(b.decode("utf-8")) if b is not None else None


def drop_matches(rows, op):
    """The places of the evidence rows a drop_evidence names: its url, and its capture (a row with no capture when the
    op names none)."""
    url, cap = op.get("url"), op.get("capture") or None
    return [i for i, e in enumerate(rows or []) if isinstance(e, dict) and e.get("url") == url
            and (e.get("capture") or None) == cap]


def drop_target(before, current, op):
    """The evidence row a drop_evidence takes out. It is found among the rows of the record as the unit found it
    (before, which `rq show` lists; an index counts there), then in the record as it is now (current), which earlier
    operations of the unit may have changed. -> (row, its place in current, None), or (None, None, why it names no
    row)."""
    rid = op.get("rid")
    what = "url %s and %s" % (op.get("url"), ("capture %s" % str(op["capture"])[:20]) if op.get("capture") else "no capture")
    hits = drop_matches(before, op)
    if not hits:
        return None, None, "no evidence row of %s has %s (`%s show RUN %s` lists its rows)" % (rid, what, RQ, rid)
    idx = op.get("index")
    if idx is not None and (isinstance(idx, bool) or not isinstance(idx, int) or idx not in hits):
        return None, None, "index %r is not a row of %s with %s (those rows are at %s)" % (
            idx, rid, what, ", ".join(map(str, hits)))
    if idx is None and len(hits) > 1:
        return None, None, ("%d evidence rows of %s have %s: add index, the place of the row to drop in the record's "
                            "evidence list, counting from 0 (one of %s)" % (len(hits), rid, what, ", ".join(map(str, hits))))
    row = before[hits[0] if idx is None else idx]
    for i, e in enumerate(current or []):
        if e == row:
            return row, i, None
    return None, None, "the evidence row of %s with %s is dropped already by an earlier operation of this unit" % (rid, what)


# the files a lane or an auditor writes by hand and the harness reads as UTF-8 text
LANE_TEXT = ("changes.jsonl", "receipt.json", "verdicts.jsonl")


def lint_unit(u, repo=REPO, need_receipt=False, view=None):
    d = unit_dir(u["run"], u["id"], repo)
    # a file that is not UTF-8 is a named problem that brief --fix sends back, never a crash of collect or the score
    enc = {n: utf8_problem(os.path.join(d, n)) for n in LANE_TEXT}
    probs, ops = [p for p in enc.values() if p], []
    rows = [] if enc["changes.jsonl"] else read_jsonl(os.path.join(d, "changes.jsonl"))
    scope_rids = set(u["scope"].get("rids") or [])
    m = fr()
    view = view if view is not None else run_tree(u["run"], repo)
    for i, op in enumerate(rows, 1):
        w = "changes.jsonl line %d" % i
        if "_bad" in op:
            probs.append("%s: not JSON (%s)" % (w, op["_bad"]))
            continue
        kind = op.get("op")
        if kind not in OPS:
            probs.append("%s: op must be one of %s" % (w, ", ".join(OPS)))
            continue
        ops.append(op)
        if kind in ("set", "confirm", "append_evidence", "drop_evidence", "dead"):
            rid = op.get("rid") or ""
            if rid not in scope_rids:
                probs.append("%s: %s is not in this unit's scope" % (w, rid or "(no rid)"))
            elif not view.exists("dossier/%s.json" % rid):
                probs.append("%s: no record %s" % (w, rid))
        if kind in ("set", "confirm", "append_evidence", "dead", "relate"):
            probs += check_evidence(op.get("evidence"), d, repo, w, view)
        if kind in ("set", "confirm") and op.get("rung") not in LADDER:
            probs.append("%s: rung must be one of %s" % (w, ", ".join(LADDER)))
        if kind in ("set", "confirm"):
            probs += measured_problem(op, w)
        if kind == "confirm":
            paths = op.get("paths")
            cur = record_of(view, op.get("rid")) if RID_RE.match(op.get("rid") or "") else None
            unread = op.get("unread")
            if unread is not None and not (isinstance(unread, list) and all(isinstance(x, str) and x for x in unread)):
                probs.append("%s: unread is a list of the field names you did not re-read" % w)
            if not isinstance(paths, list) or not paths:
                probs.append("%s: confirm needs paths, the fields you re-read (a confirm re-dates the whole record)" % w)
            elif cur is not None:
                for pth in paths:
                    try:
                        if m.get_path(cur, m.parse_jpath(pth)) is m.ABSENT:
                            probs.append("%s: confirm path %s is not in the record" % (w, pth))
                    except Exception as e:
                        probs.append("%s: confirm path %r: %s" % (w, pth, e))
        if kind == "set":
            try:
                segs = m.parse_jpath(op.get("path") or "")
                if segs[0] in ("topic", "slug", "verified_at", "stale", "stale_checked_at", "evidence"):
                    probs.append("%s: %s is not settable (use confirm to re-date, append_evidence and drop_evidence for evidence)" % (w, segs[0]))
            except Exception as e:
                probs.append("%s: %s" % (w, e))
            if "new" not in op:
                probs.append("%s: set needs new" % w)
            if not (op.get("reason") or "").strip():
                probs.append("%s: set needs a reason" % w)
            nv = op.get("new")
            if isinstance(nv, str) and isinstance(op.get("evidence"), dict):
                ev = op["evidence"]
                miss = missing_numbers(nv, ev.get("quote") or "", read_capture(ev.get("capture") or "sha256:0", repo, d, view) or "")
                if miss and not (op.get("derived") or "").strip():
                    probs.append("%s: number(s) %s in the new value appear in neither the quote nor the capture; "
                                 "quote them or add derived" % (w, ", ".join("%g" % x for x in miss[:5])))
            probs += ["%s: narrative in a field: %s" % (w, h) for h in narrative_hits(nv, op.get("path") or "$", repo)]
        if kind == "dead":
            if op.get("cause") not in CAUSES:
                probs.append("%s: cause must be one of %s" % (w, ", ".join(CAUSES)))
        if kind == "drop_evidence":
            rid = op.get("rid") if isinstance(op.get("rid"), str) else ""
            if not RID_RE.match(rid):
                probs.append("%s: drop_evidence needs rid, the record's id topic/slug" % w)
            if not isinstance(op.get("url"), str) or not op["url"].strip():
                probs.append("%s: drop_evidence needs url, the url of the row to drop as the record holds it" % w)
            if op.get("capture") is not None and not (isinstance(op["capture"], str) and SHA_RE.match(op["capture"])):
                probs.append("%s: drop_evidence capture is the row's sha256:..., or absent when the row has none" % w)
            if not isinstance(op.get("reason"), str) or not op["reason"].strip():
                probs.append("%s: drop_evidence needs a reason: why the row is wrong (it goes to the ledger)" % w)
            if "evidence" in op:
                probs.append("%s: drop_evidence names its row with url and capture; the row that replaces it is an "
                             "append_evidence (or the evidence of a set or confirm) of the same unit" % w)
            cur = record_of(view, rid) if RID_RE.match(rid) and isinstance(op.get("url"), str) else None
            if cur is not None:
                why = drop_target(cur.get("evidence") or [], cur.get("evidence") or [], op)[2]
                if why:
                    probs.append("%s: %s" % (w, why))
        if kind == "relate":
            if op.get("kind") not in RELATIONS:
                probs.append("%s: kind must be one of %s" % (w, ", ".join(RELATIONS)))
            if op.get("src") not in scope_rids and op.get("dst") not in scope_rids:
                probs.append("%s: relate needs src or dst in scope" % w)
        if kind == "open_question" and not (op.get("question") or "").strip():
            probs.append("%s: open_question needs a question" % w)
        if kind == "add_record":
            if u["kind"] != "discover":
                probs.append("%s: add_record only in discover units" % w)
            probs += lint_draft(op.get("draft") or "", u, d, repo, w, view)
    if not probs:
        probs += simulate(ops, d, repo, view)
    if enc["receipt.json"]:
        # read with the bad bytes replaced: the unit is invalid (a receipt is there), not running (no receipt)
        try:
            with open(os.path.join(d, "receipt.json"), encoding="utf-8", errors="replace") as f:
                rec = json.load(f)
        except ValueError:
            rec = None
        rec = rec if isinstance(rec, dict) and rec else {"status": "unreadable"}
    else:
        rec = read_json(os.path.join(d, "receipt.json"))
    if need_receipt:
        if not rec:
            probs.append("receipt.json is missing")
        elif rec.get("status") not in ("done", "partial", "blocked"):
            probs.append("receipt.json: status must be done, partial or blocked")
    return probs, ops, rec


HINTS = {"C10": "; add a `confirm` whose `paths` list the fields your evidence proves (it re-dates the record; "
                "name in `unread` the fields of the brief's confirm row that you did not re-read)",
         "C07": "; free_tier.unit and the stated text must use the same unit system",
         "C15": "; write the price with its ISO 4217 code, for example EUR 3.20",
         "C09": "; binding must name a kind that one limits[] row has",
         "C19": "; confidence measured needs a probe result",
         "C21": "; every http evidence row needs capture and quote",
         "C01": "; a qualifying verdict needs a free tier or a recurring credit; with neither, the verdict is paid-only",
         "C03": "; in storage and netdisk-pan, qualifies needs a probe of the read path; without one, qualifies-with-caveat",
         "C18": "; behind an institution, a national ID or a country phone, the verdict is qualifies-with-caveat at best"}


def simulate(ops, d, repo=REPO, view=None):
    """Apply the unit's record operations to a copy of each record as the run branch holds it, then run the run
    tree's schema and the record's error rules against the run tree's baseline, as the integrator will. The lane sees
    the problem while it can still fix it."""
    import checks
    m = fr()
    base = checks.baseline_of(view)
    recs, dropped, out = {}, set(), []
    for op in ops:
        rid = op.get("rid")
        if op.get("op") not in ("set", "confirm", "append_evidence", "drop_evidence", "dead") or not RID_RE.match(rid or ""):
            continue
        if rid not in recs:
            cur = record_of(view, rid)
            if cur is None:
                continue
            recs[rid] = cur
        rec = recs[rid]
        if op["op"] == "drop_evidence":
            row, at, why = drop_target((record_of(view, rid) or {}).get("evidence") or [], rec.get("evidence") or [], op)
            if why:
                out.append("%s: %s" % (rid, why))
            else:
                del rec["evidence"][at]
                dropped.add(rid)
            continue
        try:
            if op["op"] == "set":
                import integrate
                segs = m.parse_jpath(op["path"])
                cur = m.get_path(rec, segs)
                conf = rec.get("confidence") if rec.get("confidence") in LADDER else "unverified"
                if not (cur is not m.ABSENT and m.same(cur, op.get("new"))) and not integrate.is_placeholder(rec, segs, cur):
                    if ("old" in op and not (cur is not m.ABSENT and m.same(cur, op["old"]))) or \
                            LADDER.index(op.get("rung")) < LADDER.index(conf):
                        continue  # the integrator makes this a conflict and writes nothing
                m.set_path(rec, segs, op.get("new"))
            elif op["op"] == "confirm":
                rec["verified_at"] = m.utc_stamp_ms()
            elif op["op"] == "dead":
                rec["verdict"] = "dead"
        except Exception:
            continue
        ev = op.get("evidence")
        if isinstance(ev, dict):
            rec.setdefault("evidence", []).append({k: ev[k] for k in ("url", "date", "proved", "capture", "quote") if k in ev})
    for rid in sorted(dropped):
        lost = checks.uncited_sources(record_of(view, rid), recs[rid])
        if lost:
            out.append("%s: your changes would leave %s, which a field names as its source, with no evidence row; %s"
                       % (rid, ", ".join(lost), checks.UNCITED_HINT))
    for rid, rec in sorted(recs.items()):
        for e in validate_in(view, rec)[:3]:
            out.append("%s would not validate after your changes: %s %s" % (rid, e.get("path"), e.get("message")))
        for rule, key, det in checks.record_violations(dict(rec, _rid=rid), repo, narrative=False, lane=d, view=view):
            if checks.is_error(rule, key) and key not in base.get(rule, set()):
                out.append("%s: your changes would add rule %s (%s): %s%s" % (rid, rule, checks.RULES[rule][1], det, HINTS.get(rule, "")))
        orig = record_of(view, rid)
        if checks.binding_missing(rec) and not checks.binding_missing(orig):
            # a set that raises the rung to documented or measured on a record with no binding (W4-01)
            out.append("%s: your changes would fail the gate's binding check: %s" % (rid, checks.BINDING_HINT))
        was = set(checks.self_hosted_problems(orig, rid, repo))
        for why in checks.self_hosted_problems(rec, rid, repo):
            if why not in was:
                # a set of the category or of self_hosted that the gate's selfhosted check would fail (W5-03)
                out.append("%s: your changes would fail the gate's selfhosted check: %s. %s" % (rid, why, checks.SELF_HOSTED_HINT))
    return out


def lint_draft(draft, u, d, repo, w, view):
    probs = []
    p = os.path.join(d, draft)
    if not draft.startswith("new/") or not os.path.exists(p):
        return ["%s: draft %s not found under new/" % (w, draft)]
    try:
        rec = json.loads(open(p, encoding="utf-8").read())
    except ValueError as e:
        return ["%s: draft is not JSON: %s" % (w, e)]
    topic, fn = draft.split("/")[1], os.path.basename(draft)
    if rec.get("topic") != topic or rec.get("slug") + ".json" != fn:
        probs.append("%s: draft topic/slug must match its path new/<topic>/<slug>.json" % w)
    if topic != u["scope"].get("new", {}).get("topic", u["topic"]):
        probs.append("%s: draft topic %s is outside this unit's scope" % (w, topic))
    for e in validate_in(view, rec)[:5]:
        probs.append("%s: schema %s %s" % (w, e.get("path"), e.get("message")))
    for i, ev in enumerate(rec.get("evidence") or []):
        probs += check_evidence(ev, d, repo, "%s evidence[%d]" % (w, i), view)
    import checks
    if checks.binding_missing(rec):
        probs.append("%s: %s" % (w, checks.BINDING_HINT))
    for why in checks.self_hosted_problems(rec, "%s/%s" % (topic, rec.get("slug"))):
        # self-hosted software is the last resort and sorts last only when it is marked (AGENTS.md rule 9; W5-03)
        probs.append("%s: %s. %s" % (w, why, checks.SELF_HOSTED_HINT))
    if rec.get("confidence") == "measured" and not any(
            isinstance(e, dict) and (e.get("url") or "").startswith("probe:") for e in rec.get("evidence") or []):
        probs.append("%s: confidence measured needs a probe: evidence row that cites a probe record registered with "
                     "%s capture probe:TARGET --lane WS --probe RECORD.json" % (w, RQ))
    # the same error rules the integrator applies to a draft, narrative included, so lint and integrate agree
    for rule, key, det in checks.record_violations(dict(rec, _rid="%s/%s" % (topic, rec.get("slug"))), repo, lane=d, view=view):
        if checks.is_error(rule, key):
            probs.append("%s: rule %s (%s): %s%s" % (w, rule, checks.RULES[rule][1], det, HINTS.get(rule, "")))
    return probs


# ---------------------------------------------------------------------------------------------- collect, status

def audit_todo(run, repo=REPO):
    """-> (integrated units that no auditor took yet, audit units not scored yet). A unit that left no claim to
    audit is marked audit_none by `rq audit` and is not listed (W2-01)."""
    us = units_of(run, repo)
    unaudited = [u for u in us if u["kind"] != "audit" and u["status"] == "integrated" and u.get("commit")
                 and not u.get("audited_by") and not u.get("audit_none")]
    unscored = [u for u in us if u["kind"] == "audit" and not u.get("scored") and u["status"] != "superseded"]
    return unaudited, unscored


def collect(run, repo=REPO):
    r = load_run(run, repo)
    rows, ready = [], 0
    view = run_tree(run, repo)
    for u in units_of(run, repo):
        if u["status"] in ("integrated", "reverted", "superseded", "abandoned") or (u["kind"] == "audit" and u.get("scored")):
            rows.append((u["id"], u["status"], "", ""))
            continue
        probs, ops, rec = lint_unit(u, repo, need_receipt=True, view=view)
        st = (rec or {}).get("status") if rec else "missing"
        u["status"] = "ready" if not probs and rec else ("invalid" if rec else "running")
        u["problems"] = probs
        u["receipt"] = rec
        save_unit(u, repo)
        if u["status"] == "ready":
            ready += 1
        rows.append((u["id"], u["status"], "%s %d ops" % (st, len(ops)), "%d problem(s)" % len(probs)))
    # collect moves a run forward from open or planned only: an integrated run whose audit lanes are collected stays
    # integrated (section 10), and a run in review that a send-back gave new units stays in review (W2-03)
    if r.get("phase") in ("open", "planned", "collected"):
        r["phase"] = "collected"
    save_run(r, repo)
    return rows, ready


def status(run=None, repo=REPO):
    if run:
        r = load_run(run, repo)
        out = ["run %s  phase %s  research issue %s  run issue %s  branch %s%s" % (
            r["run"], r["phase"], "#%s" % r["research_issue"] if r.get("research_issue") else "none",
            "#%s" % r["issue"] if r.get("issue") else "none (no gh, or --no-issue)", r.get("branch"),
            "  pull request %s" % r["pr"] if r.get("pr") else "")]
        for u in units_of(run, repo):
            rec = u.get("receipt") or {}
            out.append("  %s %-9s %-10s %s" % (u["id"], u["kind"], u["status"], (rec.get("summary") or u["question"])[:90]))
        return "\n".join(out)
    out = []
    for r in all_runs(repo):
        us = units_of(r["run"], repo)
        c = collections.Counter(u["status"] for u in us)
        out.append("%s  %-10s units %d (%s)  research issue %s  last change %s" % (
            r["run"], r["phase"], len(us), ", ".join("%s %d" % kv for kv in sorted(c.items())),
            "#%s" % r["research_issue"] if r.get("research_issue") else "none", last_change(run_dir(r["run"], repo))))
    for p in sorted(glob.glob(os.path.join(repo, ".tmp", "rq", "runs", "*", "run.json"))):
        r = read_json(p, {}) or {}
        out.append("%s  %-10s LEGACY run of the old harness (.tmp/rq/runs/): let it land, or scripts/rq close %s "
                   "--reason \"...\"" % (r.get("run"), r.get("phase"), r.get("run")))
    out += health(repo)
    return "\n".join(out) or "no runs"


def last_change(d):
    """The UTC time of the newest file under a folder (a session that died shows no change for lease_hours)."""
    t = 0.0
    for root, _, files in os.walk(d):
        for f in files:
            try:
                t = max(t, os.path.getmtime(os.path.join(root, f)))
            except OSError:
                pass
    if not t:
        return "-"
    import datetime as dt
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def health(repo=REPO):
    """The state of the research checkout, after the runs: a session that broke rule 14 by hand shows up here."""
    from common import has_remote, now_ts, research_checkout
    out = []
    head = git(repo, "rev-parse", "HEAD", check=False)
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD", check=False)
    up = upstream(repo)
    behind = git(repo, "rev-list", "--count", "HEAD..%s" % up, check=False) if has_remote(repo) else "-"
    changed = status_paths(repo, "--untracked-files=no")
    # an untracked file outside .tmp/ (which is ignored) is a file a session wrote against rule 14; it can stop the
    # merge session's sync (LIO3-03)
    stray = git(repo, "ls-files", "--others", "--exclude-standard", "--directory", check=False).splitlines()
    # the main working tree is not counted: a clean research checkout has no linked worktree (LW7-07)
    wts = extra_worktrees(repo)
    marker = research_checkout(repo)
    out.append("checkout: HEAD %s on %s, %s commit(s) behind %s, %d tracked file(s) differ from HEAD, %d untracked "
               "outside .tmp/, %d linked worktree(s); rq.researchCheckout %s" % (
                   (head or "-")[:10], branch or "-", behind or "0", short_ref(up), len(changed), len(stray), len(wts),
                   "true" if marker else "is not set (an own clone, or a checkout nobody prepared)"))
    if head and rev(repo, up) and not is_ancestor(repo, head, up):
        out.append("  HEAD is not in %s (a feature branch): no run opens here; the research checkout stays on %s and "
                   "moves only with the merge session's scripts/rq sync" % (short_ref(up), BASE))
    shadow = upstream_shadowed(repo)
    if shadow:
        out.append("  a ref shadows main's short name (%s): the harness reads the full refnames, but a hand-typed git "
                   "command reads the wrong commit; a merge session deletes that ref" % shadow)
    if changed:
        out.append("  tracked changes (AGENTS.md section 2 rule 14: no research agent changes tracked files): " +
                   ", ".join(changed[:8]))
    if stray:
        out.append("  untracked outside .tmp/ (AGENTS.md section 2 rule 14: every file an agent makes goes under "
                   ".tmp/<id>/): " + ", ".join(stray[:8]))
    for path, br in wts:
        # .claude/ is ignored, so the stray check never sees a subagent's isolation worktree (LIO7-01)
        out.append("  worktree against rule 14: %s [%s]" % (path, br))
    now = now_ts()
    ls = state.leases(repo)
    work = [l for l in ls if l[5] == "work"]
    held = [l for l in ls if l[5] == "held"]
    review = [l for l in ls if l[5] == "review"]
    out.append("leases: %d live work lease(s), %d held by integrated units, %d review lease(s)" % (
        len(work), len(held), len(review)))
    for run in sorted({l[1] for l in review}):
        r = read_json(os.path.join(run_dir(run, repo), "run.json"), {}) or {}
        out.append("  review leases of %s (%d), landed %s" % (run, sum(1 for l in review if l[1] == run),
                                                            r.get("landed_at") or r.get("pr") or "-"))
    live, idle = session_folders(repo)
    out.append("session folders: %d live, %d idle (no change for %d hours)" % (len(live), len(idle), state.LEASE_HOURS))
    for what in ("drain", "wiping"):
        c = state.control(repo, what)
        if c:
            out.append("%s: pid %s since %s %s" % (what, c[0], c[1], c[2] or ""))
    try:
        p = fr().store_file(repo)
        out.append("store of HEAD: %s" % (os.path.relpath(p, repo).replace("\\", "/") if p else
                                          "missing (the first scripts/fr call builds it once, about two minutes)"))
    except Exception as e:
        out.append("store of HEAD: unknown (%s)" % e)
    return out


# ---------------------------------------------------------------------------------------------- session folders

def session_folders(repo=REPO):
    """-> (live, idle) session folder ids. Live: not ended and a file in it changed within lease_hours. Idle: not
    ended and no change for lease_hours (a session that died)."""
    from common import now_ts
    live, idle = [], []
    for fid, kind, created, holder_, ended in state.folders(repo, "session"):
        if ended:
            continue
        d = os.path.join(repo, ".tmp", fid)
        newest = 0.0
        for root, _, files in os.walk(d):
            for f in files:
                try:
                    newest = max(newest, os.path.getmtime(os.path.join(root, f)))
                except OSError:
                    pass
        if not newest:
            try:
                newest = os.path.getmtime(d)
            except OSError:
                newest = 0.0
        (live if now_ts() - newest < state.LEASE_HOURS * 3600 else idle).append(fid)
    return live, idle


def session_id(arg):
    """The folder id from what a session may pass: the printed `.tmp/session-<id>/`, `session-<id>` or the bare <id>."""
    a = (arg or "").replace("\\", "/").strip().strip("/")
    a = a.rsplit("/", 1)[-1]
    return a if a.startswith("session-") else "session-" + a


def folder_session(repo=REPO, end=None, take=None, listing=False):
    import secrets
    end = session_id(end) if end else end
    take = session_id(take) if take else take
    if listing:
        live, idle = session_folders(repo)
        ended = [f[0] for f in state.folders(repo, "session") if f[4]]
        return ["%s\tlive" % f for f in live] + ["%s\tidle" % f for f in idle] + ["%s\tended" % f for f in ended]
    if end:
        if not any(f[0] == end for f in state.folders(repo, "session")):
            raise Fail("no session folder %s (scripts/rq folder session --list)" % end, 2)
        state.end_folder(repo, end)
        return ["session folder .tmp/%s/ ended; a merge session's wipe no longer waits for it" % end]
    if take:
        if not any(f[0] == take for f in state.folders(repo, "session")):
            raise Fail("no session folder %s (scripts/rq folder session --list)" % take, 2)
        state.take_folder(repo, take, "pid %d" % os.getpid())
        return [".tmp/%s/" % take]
    fid = "session-%s-%s" % (stamp().replace("-", "").replace(":", "")[:13].replace("T", "-"), secrets.token_hex(2))
    state.register_folder(repo, fid, "session", holder="pid %d" % os.getpid())
    os.makedirs(os.path.join(repo, ".tmp", fid, "captures"), exist_ok=True)
    return [".tmp/%s/" % fid]
