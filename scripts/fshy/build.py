#!/usr/bin/env python3
"""build.py: dossier/ -> the fshy store (SQLite): the local store for scripts/fr, and the public projection.

usage:
  python scripts/fshy/build.py                       # local store of HEAD: .tmp/fshy/local-<HEAD 12>-s<F>.db
  python scripts/fshy/build.py --public OUT.db       # public store only (projection and leak scan)
  python scripts/fshy/build.py --check               # build the public store to .tmp, verify accounting and leaks

The JSON in dossier/ is the truth; every output here is derived and never committed. The public wiki, its API
and its Worker are built in the public repository Azathothas/fshy.ajam.dev from the export of the public
store (its publish/export.py reads a checkout of this repository); this repository keeps the projection,
because its rules name what they remove.
Exit codes: 0 ok, 1 a check failed, 2 usage.
"""
import argparse
import collections
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import derive  # noqa: E402
import entity  # noqa: E402
import project  # noqa: E402

# STORE_FORMAT names the local store's file (.tmp/fshy/local-<HEAD 12>-s<STORE_FORMAT>.<SCHEMA_VERSION>.db, fr.py
# store_format): raise it when the local store's tables change while schema.sql does not, so an old file is never read
# as the new format. A store is built once per commit and never replaced (fr.py ensure_store).
STORE_FORMAT = 1
SCHEMA_VERSION = "3"  # 2 added record.self_hosted, 3 added ledger.op
# The public repository builds its store from the export with its own copy of schema.sql and refuses a
# schema_version it does not know. A change of schema.sql here must bump SCHEMA_VERSION; test_fr.py fails until
# SCHEMA_SHA256 is the sha256 of the new schema.sql (LF line endings), so the bump cannot be forgotten.
SCHEMA_SHA256 = "137caaa17bb43881a95fda0c986b497ed6e9c6f193ae8274ba77784f5ab91858"
TIMES = collections.OrderedDict()
# the records whose usd_month is below a monthly list price they state (derive.price_violations); --check fails on any
PRICE_VIOLATIONS = []
_T = [time.perf_counter()]


def lap(name):
    t = time.perf_counter()
    TIMES[name] = round(t - _T[0], 2)
    _T[0] = t


def git_info(repo):
    def run(*a):
        try:
            return subprocess.run(["git", "-C", repo] + list(a), capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    commit = os.environ.get("WORKERS_CI_COMMIT_SHA") or run("rev-parse", "HEAD")
    when = run("log", "-1", "--format=%ct")
    # UTC, never the committer's offset: a time zone in a published file says where the committer was
    when = dt.datetime.fromtimestamp(int(when), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if when.isdigit() else ""
    return commit, when


def load(repo):
    recs = []
    base = os.path.join(repo, "dossier")
    for topic in sorted(os.listdir(base)):
        d = os.path.join(base, topic)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn.endswith(".generated.json"):
                continue
            b = open(os.path.join(d, fn), "rb").read()
            o = json.loads(b.decode("utf-8"))
            recs.append({"rid": "%s/%s" % (o["topic"], o["slug"]), "path": "dossier/%s/%s" % (topic, fn),
                         "sha": hashlib.sha256(b).hexdigest(), "raw": o, "text": b.decode("utf-8")})
    return recs


CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]+")


def fts_text(s):
    """Index text: CJK runs also emitted as overlapping bigrams (the same rule as site/worker/text.js in the public
    repository Azathothas/fshy.ajam.dev)."""
    def rep(m):
        t = m.group(0)
        return t + " " + (" ".join(t[i:i + 2] for i in range(len(t) - 1)) if len(t) > 1 else t)
    return CJK.sub(rep, s)


URLISH = re.compile(r"^(?:https?:|probe:)")


def build(repo, out_db, target, as_of_date=None):
    rules = json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8"))
    commit, commit_time = git_info(repo)
    as_of = dt.date.fromisoformat(as_of_date) if as_of_date else (
        dt.date.fromisoformat(commit_time[:10]) if commit_time else dt.datetime.now(dt.timezone.utc).date())
    recs = load(repo)
    lap("load")

    proj = project.Projector(rules, [r["raw"] for r in recs])
    lap("templates")
    P, tallies, strip_log, unknowns, excluded = {}, collections.Counter(), [], [], []
    total_leaves = 0
    for r in recs:
        n = project.count_leaves(r["raw"])
        total_leaves += n
        if proj.excluded(r["raw"], r["rid"]):
            tallies["excluded"] += n
            excluded.append(r["rid"])
            strip_log.append((r["rid"], "$", "X01", "(whole record)"))
            continue
        o, t, s, u = proj.project(r["rid"], r["raw"])
        if sum(t.values()) != n:
            raise SystemExit("accounting: %s has %d leaves but %d dispositions" % (r["rid"], n, sum(t.values())))
        tallies.update(t)
        P[r["rid"]] = o
        strip_log.extend((r["rid"],) + x for x in s)
        unknowns.extend((r["rid"],) + x for x in u)
    if sum(tallies.values()) != total_leaves:
        raise SystemExit("accounting: %d leaves, %d dispositions" % (total_leaves, sum(tallies.values())))
    lap("project")

    psl = entity.PSL()
    ENT, REC_EID = entity.resolve(P, repo, psl)
    lap("entities")

    RAW = {r["rid"]: r for r in recs}
    fx = derive.fx_table([r["raw"] for r in recs])
    fresh = derive.Freshness(repo)
    dup, rel_edges = derive.parse_relations(repo)
    for rid, o in P.items():  # records may name their canonical sibling in extras.duplicate_of
        d = (RAW[rid]["raw"].get("extras") or {}).get("duplicate_of")
        if isinstance(d, str) and rid not in dup:
            m = re.fullmatch(r"(?:dossier/)?(?:([a-z0-9-]+)/)?([a-z0-9-]+)(?:\.json)?", d.strip())
            if m:
                cand = "%s/%s" % (m.group(1) or o["topic"], m.group(2))
                if cand in P and cand != rid:
                    dup[rid] = cand
                    rel_edges.append((rid, cand, "duplicate_of"))
    rows, ev_rows, lim_rows, claim_rows, leaf_rows, fts = [], [], [], [], [], []
    price_viol = []
    unk_extra = []
    lid = 0
    aliases_by_eid = collections.defaultdict(set)
    for rid in P:
        for a in record_aliases(P[rid]):
            aliases_by_eid[REC_EID[rid]].add(a)
    for rno, rid in enumerate(sorted(P), 1):
        o = P[rid]
        raw = RAW[rid]["raw"]
        idn = derive.identity(raw, rules)
        fr = fresh.of(RAW[rid]["path"], raw, as_of)
        ev = o.get("evidence") or []
        dates = sorted(e.get("date") for e in ev if isinstance(e, dict) and e.get("date"))
        iface = [t for t in (o.get("interface") or []) if t != "unknown"]
        if not iface:
            unk_extra.append((rid, "$.interface", "interface-unknown", "S-IFACE"))
        eg = o.get("egress") or {}
        terms = eg.get("terms") or ""
        metered = None if (not terms or re.match(r"(?i)not (published|assessed|stated)", terms)) else (1 if eg.get("metered") else 0)
        if metered is None:
            unk_extra.append((rid, "$.egress.metered", "egress-unknown", "S-EGRESS"))
        if idn["identity_basis"] != "stated":
            unk_extra.append((rid, "$.identity_cost.kind", "identity-defaulted", "S-IDENT"))
        read_date = dates[-1] if dates else None
        cl = derive.claims_for(rid, o, read_date, fx)
        claim_rows.extend(cl)
        usd_month, usd_tb = derive.headline_prices(cl)
        price_viol.extend(derive.price_violations(rid, cl, usd_month))
        summ = re.sub(r"\s+", " ", (o.get("free_tier") or {}).get("stated") or "").strip()
        summ = (summ[:157] + "...") if len(summ) > 160 else (summ or None)
        hf = derive.free_allowance(o, summ, raw)
        if hf is not None:
            claim_rows.append((rid, "$.free_tier", "has-free-tier", float(hf), None, None, None, None, None, "ok"))
        lmin = lid + 1
        for p, v in project.leaves(o):
            if v is None:
                continue
            lid += 1
            if isinstance(v, bool):
                typ, val = "bool", "true" if v else "false"
            elif isinstance(v, (int, float)):
                typ, val = "num", json.dumps(v)
            elif isinstance(v, str):
                typ, val = "text", v
            else:
                typ, val = ("object" if isinstance(v, dict) else "array"), json.dumps(v)
            leaf_rows.append((lid, rno, project.jpath(p), typ, val))
        for i, e in enumerate(ev):
            if not isinstance(e, dict):
                continue
            u = e.get("url")
            kind = None if u is None else ("probe" if u.startswith("probe:") else ("archive" if "archive.org" in u else "http"))
            ev_rows.append((rid, i, u, kind, e.get("date"), e.get("proved"), None))
        for i, lm in enumerate(o.get("limits") or []):
            if isinstance(lm, dict):
                lim_rows.append((rid, i, lm.get("kind"), lm.get("value"), lm.get("source"),
                                 1 if lm.get("kind") == o.get("binding") else 0))
        url = o.get("url") or next((e.get("url") for e in ev if isinstance(e, dict)
                                    and isinstance(e.get("url"), str) and e["url"].startswith("http")), None)
        h, _ = entity.host_path(url)
        fts.append((rno,) + fts_columns(o, url, sorted(aliases_by_eid[REC_EID[rid]]), ENT[REC_EID[rid]]))
        rows.append({
            "rid": rid, "rno": rno, "topic": o["topic"], "slug": o["slug"], "eid": REC_EID[rid], "provider": o.get("provider"),
            "url": url, "domain": psl.registrable(h) if h else None, "category": o.get("category"),
            "tier": o.get("tier"), "verdict": o["verdict"], "vorder": derive.VORDER[o["verdict"]],
            "grp": derive.GROUP.get(o["verdict"], "rejected"), "self_hosted": 1 if raw.get("self_hosted") is True else 0,
            "confidence": o.get("confidence"),
            "binding": o.get("binding"), **idn, "crypto": derive.crypto_flag(raw),
            "free_unit": "none" if o["verdict"] == "paid-only" else (o.get("free_tier") or {}).get("unit"), "free_metered_on": (o.get("free_tier") or {}).get("metered_on"),
            "egress_metered": metered, "per_object_bytes": (o.get("per_object_cap") or {}).get("bytes"),
            "retention_days": (o.get("retention") or {}).get("days"), "interfaces": ",".join(iface) or None,
            "verified_at": o.get("verified_at"), "verified_basis": fr["basis"], "checked_on": fr["checked_on"],
            "stale_on": fr["stale_on"], "limit_days": fr["limit_days"], "evidence_budget_days": fr["evidence_budget_days"],
            "evidence_newest": dates[-1] if dates else None, "evidence_oldest": dates[0] if dates else None,
            "n_evidence": len(ev), "usd_month": usd_month, "usd_per_tb_month": usd_tb, "summary": summ,
            "duplicate_of": dup.get(rid), "n_unknown": 0, "n_withheld": 0, "lid_min": lmin, "lid_max": lid,
            "doc": json.dumps(o, ensure_ascii=False, separators=(",", ":")), "sha256": RAW[rid]["sha"], "path": RAW[rid]["path"],
        })
    all_unknown = {}
    for rid, path, cls, rule in unknowns + unk_extra:
        all_unknown.setdefault((rid, path), (rid, path, cls, rule))
    nunk = collections.Counter(k[0] for k in all_unknown)
    nwith = collections.Counter(r[0] for r in strip_log)
    for row in rows:
        row["n_unknown"] = nunk[row["rid"]]
        row["n_withheld"] = nwith[row["rid"]]
    lap("derive")

    # duplicate disagreement (same entity, topic and core name)
    drift_rows = []
    grp = collections.defaultdict(list)
    for row in rows:
        grp[(row["eid"], row["topic"], entity.core_name(row["provider"]))].append(row)
    edges = list(rel_edges)
    for k, ms in grp.items():
        if len(ms) < 2:
            continue
        for a in ms:
            for b in ms:
                if a["rid"] < b["rid"]:
                    edges.append((a["rid"], b["rid"], "same-product"))
                    for f in ("verdict", "identity_kind"):
                        if a[f] != b[f] and not (dup.get(a["rid"]) == b["rid"] or dup.get(b["rid"]) == a["rid"]):
                            drift_rows.append(("duplicate-disagrees", a["rid"], b["rid"], f, a[f], b[f], None))
    # a record mentions another by its path (dossier/<topic>/<slug>.json) or, after the public projection, by its id
    ridref = re.compile(r"(?<![\w./:-])(%s)/([a-z0-9][a-z0-9-]*)(?![\w-])" % "|".join(
        re.escape(t) for t in sorted({k.split("/")[0] for k in P}, key=len, reverse=True)))
    for rid, o in P.items():
        text = json.dumps(o, ensure_ascii=False)
        for m in list(derive.DOSSREF.finditer(text)) + list(ridref.finditer(text)):
            dst = "%s/%s" % m.groups()
            if dst != rid and dst in P:
                edges.append((rid, dst, "mentions"))
    hist_rows, hist_links = derive.parse_history(repo, lambda s, fp: proj.clean_prose(s, fp))
    ledger_rows = derive.parse_ledger(repo)
    if target == "public":
        # a history entry is published as its date, status, title and linked records only. The body, the
        # supersedes header and the confidence line are the story of how a claim changed: process narrative
        # by design, and it names this repository's files, sessions and people. They stay in this repository.
        # the id of an entry is its file in this repository (history/<when>/<name>.md), and the name is the story
        # of the entry; the public id is the time and an ordinal (2026-10-22T030702Z-1). An entry whose title is
        # neutral and that links no published record says nothing a reader can use, so it is not published
        pub_ids = public_hids(hist_rows)
        kept = []
        for h in hist_rows:
            title = public_title(h, hist_links, P, rules)
            if title != h[4] and not any(a == h[0] and b in P for a, b in hist_links):
                continue
            kept.append((pub_ids[h[0]], h[1], h[2], None, title, None, None))
        keep_ids = {pub_ids[h[0]] for h in hist_rows} & {k[0] for k in kept}
        hist_links = [(pub_ids[a], b) for a, b in hist_links if a in pub_ids and pub_ids[a] in keep_ids]
        hist_rows = kept
        # the public change log is when, which record and field, what the row did (op), the rung and the evidence
        # URL; the old and new values were never projected, so they stay in this repository. The evidence URL takes
        # the same URL rules as a record's evidence: a broker URL becomes its origin, a scratch or seed pointer is
        # withheld
        ledger_rows = [(l[0], l[1], l[2], None, None, l[5], proj.rewrite_url(l[6])[0] if l[6] else None, l[7], None, None,
                        l[10]) for l in ledger_rows if l[1] in P]
    cap_rows = derive.captures(repo)
    if target == "public":
        # a capture is public when a reader can fetch its URL; a probe file or a directory listing kept in this
        # repository has a private path and a private name, so the public table holds the web captures only
        cap_rows = [(c[0], c[1], None, c[3]) for c in cap_rows if re.match(r"https?://", c[0])]
    capset = {c[0]: c[2] for c in cap_rows}
    ev_rows = [e[:6] + (capset.get(e[2]),) for e in ev_rows]
    lap("relations")

    # ------------------------------------------------------------------ write
    if os.path.exists(out_db):
        os.remove(out_db)
    os.makedirs(os.path.dirname(os.path.abspath(out_db)), exist_ok=True)
    db = sqlite3.connect(out_db)
    db.execute("PRAGMA page_size=4096")
    db.execute("PRAGMA journal_mode=OFF")
    db.execute("PRAGMA synchronous=OFF")
    if target == "local":
        # an index or FTS sort that spills goes to SQLite's temporary files in the system temp folder, outside .tmp/;
        # in memory there is nothing to leave behind when a build is killed (LIO6-01)
        db.execute("PRAGMA temp_store=MEMORY")
    db.executescript(open(os.path.join(HERE, "schema.sql"), encoding="utf-8").read())
    cols = ["rid", "rno", "topic", "slug", "eid", "provider", "url", "domain", "category", "tier", "verdict", "vorder", "grp",
            "self_hosted", "confidence", "binding", "identity_kind", "identity_basis", "needs_card", "needs_phone", "needs_id",
            "needs_institution", "country", "crypto", "free_unit", "free_metered_on", "egress_metered", "per_object_bytes",
            "retention_days", "interfaces", "verified_at", "verified_basis", "checked_on", "stale_on", "limit_days",
            "evidence_budget_days", "evidence_newest", "evidence_oldest", "n_evidence", "usd_month", "usd_per_tb_month",
            "summary", "duplicate_of", "n_unknown", "n_withheld", "lid_min", "lid_max", "doc", "sha256", "path"]
    db.executemany("INSERT INTO record (%s) VALUES (%s)" % (",".join(cols), ",".join("?" * len(cols))),
                   [tuple(r[c] for c in cols) for r in rows])
    db.executemany("INSERT INTO leaf VALUES (?,?,?,?,?)", leaf_rows)
    db.executemany("INSERT INTO evidence VALUES (?,?,?,?,?,?,?)", ev_rows)
    db.executemany("INSERT INTO limit_row VALUES (?,?,?,?,?,?)", lim_rows)
    db.executemany("INSERT OR REPLACE INTO claim VALUES (?,?,?,?,?,?,?,?,?,?)", claim_rows)
    db.executemany("INSERT INTO fx VALUES (?,?,?,?)", [(c, d, v[0], v[1]) for (c, d), v in sorted(fx.items())])
    db.executemany("INSERT INTO unknown VALUES (?,?,?,?)", sorted(all_unknown.values()))
    db.executemany("INSERT OR IGNORE INTO edge VALUES (?,?,?)", sorted(set(edges)))
    db.executemany("INSERT INTO drift VALUES (?,?,?,?,?,?,?)", drift_rows)
    db.executemany("INSERT OR REPLACE INTO history VALUES (?,?,?,?,?,?,?)", hist_rows)
    db.executemany("INSERT OR IGNORE INTO history_link VALUES (?,?)", [l for l in hist_links if l[1] in P])
    db.executemany("INSERT INTO ledger VALUES (?,?,?,?,?,?,?,?,?,?,?)", ledger_rows)
    db.executemany("INSERT INTO capture VALUES (?,?,?,?)", cap_rows)
    self_hosted = {r["rid"] for r in rows if r["self_hosted"]}
    for eid, e in ENT.items():
        # best_vorder ranks the vendor in a name search: the best verdict of its hosted records, so a self-hosted
        # record never lifts its vendor; the best of all its records only when every record is self-hosted
        hosted = [m for m in e["members"] if m not in self_hosted]
        db.execute("INSERT INTO entity VALUES (?,?,?,?,?,?,?,?)",
                   (eid, e["name"], e["domain"], e["how"], ",".join(e["topics"]), len(e["members"]),
                    min(derive.VORDER[P[m]["verdict"]] for m in (hosted or e["members"])), e["review"]))
        al = {(e["name"], "name")}
        for m in e["members"]:
            al.add((P[m].get("provider") or "", "provider"))
            al.add((m.split("/")[1], "slug"))
            for a in record_aliases(P[m]):
                al.add((a, "alias"))
        if e["domain"]:
            al.add((e["domain"], "domain"))
        db.executemany("INSERT OR IGNORE INTO alias VALUES (?,?,?)", [(eid, a, k) for a, k in sorted(al) if a])
    db.executemany("INSERT INTO vocab VALUES (?,?,?,?)", derive.vocab_rows(rules))
    db.executemany("INSERT INTO text_fts (docid, name, offer, limits, egress, identity, access, notes, evidence, extras)"
                   " VALUES (?,?,?,?,?,?,?,?,?,?)", fts)
    if target == "local":
        db.executescript("""
CREATE TABLE raw (rid TEXT PRIMARY KEY, path TEXT, doc TEXT NOT NULL) WITHOUT ROWID;
CREATE TABLE strip_log (rid TEXT NOT NULL, path TEXT NOT NULL, rule TEXT NOT NULL, before TEXT);
CREATE INDEX strip_log_rid ON strip_log (rid);
CREATE INDEX strip_log_rule ON strip_log (rule);
""")
        db.executemany("INSERT INTO raw VALUES (?,?,?)", [(r["rid"], r["path"], r["text"]) for r in recs])
        db.executemany("INSERT INTO strip_log VALUES (?,?,?,?)", strip_log)
    lap("write")
    rule_counts = collections.Counter(s[2] for s in strip_log)
    counts = {"records_in": len(recs), "records": len(P), "excluded": len(excluded), "entities": len(ENT),
              "leaves": total_leaves, "dispositions": dict(tallies), "public_leaves": len(leaf_rows),
              "evidence": len(ev_rows), "limits": len(lim_rows), "claims": len(claim_rows), "unknown": len(all_unknown),
              "drift": len(drift_rows), "history": len(hist_rows), "ledger": len(ledger_rows), "fts_rows": len(fts),
              "templates": len(proj.templates), "price_violations": len(price_viol)}
    PRICE_VIOLATIONS[:] = price_viol
    meta = {"schema_version": SCHEMA_VERSION, "target": target, "commit": commit, "commit_time": commit_time,
            "as_of": as_of.isoformat(), "psl_version": psl.version,
            "rules_sha256": hashlib.sha256(open(os.path.join(HERE, "rules", "projection.json"), "rb").read()).hexdigest(),
            "counts": json.dumps(counts, sort_keys=True), "strip_rule_counts": json.dumps(dict(sorted(rule_counts.items())))}
    db.executemany("INSERT INTO meta VALUES (?,?)", sorted(meta.items()))
    db.commit()
    db.execute("INSERT INTO text_fts(text_fts) VALUES('optimize')")
    db.commit()
    if target != "local":
        # VACUUM copies the whole database into a temporary file in the system temp folder and back: about three
        # times the store's size in writes, outside .tmp/. The local store is new and written with journal_mode=OFF,
        # so it has little free space to reclaim, and a build killed during a VACUUM would leave a file no wipe
        # reaches (LIO6-01). The public store is built once, in CI or by the merge session, and is compacted.
        db.execute("VACUUM")
    db.close()
    lap("optimize")
    return counts, rule_counts


FTS_COLUMNS = ("name", "offer", "limits", "egress", "identity", "access", "notes", "evidence", "extras")


def _texts(v):
    for _, x in project.leaves(v):
        if isinstance(x, str) and x and not URLISH.match(x):
            yield x


def fts_columns(o, url, aliases, ent):
    """One row of text_fts: the record's prose grouped into the FTS_COLUMNS, CJK expanded."""
    g = lambda k: o.get(k)
    cols = {
        "name": [g("provider"), g("slug"), g("category"), g("tier"), ent["name"], ent["domain"] or "", url or ""] + list(aliases),
        "offer": list(_texts([g("free_tier"), g("per_object_cap"), g("retention"), g("price_per_tb_month")])),
        "limits": list(_texts([g("limits"), g("limits_note"), g("binding_note")])),
        "egress": list(_texts(g("egress"))),
        "identity": list(_texts(g("identity_cost"))),
        "access": list(_texts([g("interface"), g("interface_detail"), g("tooling"), g("endpoint")])),
        "notes": list(_texts([g("notes"), g("reliability_note"), g("chaining"), g("confidence_note")])),
        "evidence": [e.get("proved") or "" for e in (g("evidence") or []) if isinstance(e, dict)],
        "extras": list(_texts(g("extras"))),
    }
    return tuple(fts_text(" ".join(x for x in cols[c] if x)) for c in FTS_COLUMNS)


def record_aliases(o):
    """extras.aliases of a record when it is a list of names. A string there is a note (debrid/mixdebrid holds a
    sentence), and iterating it gave one alias per character, a blank one among them."""
    al = (o.get("extras") or {}).get("aliases")
    return [a.strip() for a in al if isinstance(a, str) and a.strip()] if isinstance(al, list) else []


def public_hids(hist_rows):
    """{private hid: public hid}. The public hid is the entry's time, from its folder (history/<when>/) or its When
    field, and an ordinal among the entries of that second, in the order of their private ids."""
    seen, out = collections.Counter(), {}
    for h in sorted(hist_rows, key=lambda r: r[0]):
        m = re.match(r"^history/(\d{4}-\d\d-\d\dT\d{6}Z)/", h[0])
        when = m.group(1) if m else re.sub(r"[:]", "", (h[1] or "undated"))
        seen[when] += 1
        out[h[0]] = "%s-%d" % (when, seen[when])
    return out


def public_title(h, links, P, rules):
    """The public title of a history entry: its own title when that title states a technical fact, else its status,
    date and the published records it links. A title that narrates the research, its documents or its people is
    process narrative, and the public history carries none."""
    rule = rules.get("history_title")
    title = h[4]
    if not rule or not re.search(rule["narrative_re"], title or ""):
        return title
    rids = sorted({r for hid, r in links if hid == h[0] and r in P})
    status = (h[2] or "changed").capitalize()
    date = (h[1] or "")[:10] or "an undated entry"
    if not rids:
        return "%s on %s" % (status, date)
    if len(rids) <= 3:
        recs = ", ".join(rids)
    else:
        more = len(rids) - 3
        recs = "%s and %d more record%s" % (", ".join(rids[:3]), more, "" if more == 1 else "s")
    return rule["neutral"].format(status=status, date=date, records=recs)


def leak_scan(db_path):
    rules = json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8"))
    rx = re.compile("|".join("(?:%s)" % p for p in rules["leak_scan"]))
    hits = []
    db = sqlite3.connect(db_path)
    rid_of = dict(db.execute("SELECT rno, rid FROM record"))  # leaf.rno -> rid; a range join here took 245 s
    for rno, path, val in db.execute("SELECT rno, path, value FROM leaf WHERE type='text'"):
        rid = rid_of.get(rno)
        m = rx.search(val)
        if m:
            hits.append(("%s %s" % (rid, path), val[max(0, m.start() - 60): m.end() + 40]))
    # every other text cell of every other table: a table the scan does not read is a table that can leak. record.doc
    # is the record as projected (its leaves are scanned above) and record.path is the store's pointer to the source
    # file, which publish/export.py drops
    for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'text_fts%' "
                           "AND name NOT IN ('leaf', 'raw', 'strip_log')"):
        cols = [c[1] for c in db.execute("PRAGMA table_info(%s)" % t)]
        for row in db.execute("SELECT * FROM %s" % t):
            for col, val in zip(cols, row):
                if isinstance(val, str) and not (t == "record" and col in ("doc", "path")):
                    m = rx.search(val)
                    if m:
                        hits.append(("%s.%s %s" % (t, col, row[0]), val[max(0, m.start() - 60): m.end() + 40]))
    # a key of a published record that is a research label (wave2, lane4_..., census_rows) is a leak by name
    prx = re.compile("|".join("(?:%s)" % p for p in rules.get("leak_scan_paths", [])) or "(?!)")
    for rno, path in db.execute("SELECT DISTINCT rno, path FROM leaf"):
        if prx.search(path):
            hits.append(("%s %s" % (rid_of.get(rno), path), "a published key names the research process"))
    # the public history is the date, status, title and linked records of an entry; any body is a leak
    if dict(db.execute("SELECT key, value FROM meta")).get("target") == "public":
        hrx = re.compile(rules["history_title"]["narrative_re"]) if rules.get("history_title") else None
        for (hid,) in db.execute("SELECT hid FROM history"):
            if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d{6}Z-\d+", hid or ""):
                hits.append(("history %s" % hid, "a public history id is not its time and an ordinal"))
        for (hid,) in db.execute("SELECT DISTINCT hid FROM history_link"):
            if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d{6}Z-\d+", hid or ""):
                hits.append(("history_link %s" % hid, "a public history id is not its time and an ordinal"))
        for hid, title in db.execute("SELECT hid, title FROM history"):
            if hrx and title and hrx.search(title) and not re.match(r"^[A-Z][a-z]+ on (?:\d{4}-\d\d-\d\d|an undated entry)(?:: |$)", title):
                hits.append(("history %s" % hid, "a public history title narrates the research: " + title[:100]))
        for hid, conf, sup, body in db.execute("SELECT hid, confidence, supersedes, body FROM history "
                                               "WHERE confidence IS NOT NULL OR supersedes IS NOT NULL OR body IS NOT NULL"):
            hits.append(("history %s" % hid, "a public history row carries a confidence, supersedes or body"))
    db.close()
    return hits


def personal_scan(recs, rules):
    """The personal e-mail addresses and phone numbers in the source value of every published field.

    The token rules P8 and P9 hide such a detail in the output, so the source would keep it and nobody would see it.
    This scan fails the build on it instead (rules personal_scan in projection.json). A field the projection drops, and
    a record it excludes, is not published and is not read. -> [(key, context)]"""
    spec = rules.get("personal_scan")
    if not spec:
        return []
    pats = [(p["id"], re.compile(p["re"])) for p in spec["patterns"]]
    proj = project.Projector(rules, [])
    hits = []
    for r in recs:
        if proj.excluded(r["raw"], r["rid"]):
            continue
        for p, v in project.leaves(r["raw"]):
            if not isinstance(v, str) or not v:
                continue
            if any(proj.drop_rule(project.folded(p[:i])) for i in range(1, len(p) + 1)):
                continue
            for pid, rx in pats:
                m = rx.search(v)
                if m:
                    hits.append(("%s %s %s" % (r["rid"], project.jpath(p), pid), v[max(0, m.start() - 40): m.end() + 30]))
    return hits


def research_checkout(repo):
    """True in the one checkout where all research runs (git config rq.researchCheckout true, set by the merge session)."""
    try:
        r = subprocess.run(["git", "-C", repo, "config", "--get", "rq.researchCheckout"], capture_output=True, text=True,
                           timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.stdout.strip().lower() == "true"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(HERE, "..", "..")))
    ap.add_argument("--local", default=None, help="local store path (default: a new store file of HEAD, "
                    ".tmp/fshy/local-<HEAD 12>-s<F>.db, built under the build lock)")
    ap.add_argument("--public", default=None, help="write the public store to this path")
    ap.add_argument("--as-of", default=None, help="date for freshness arithmetic (default: commit date)")
    ap.add_argument("--check", action="store_true", help="build the public store to .tmp, verify, exit")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true", help="--public: build even when an input has uncommitted changes")
    a = ap.parse_args(argv)
    repo = os.path.abspath(a.repo)
    if research_checkout(repo) and not os.environ.get("CI"):
        # every form writes a store file of its own (local, public, or the gate's --check), and --public runs git status,
        # which can rewrite the shared index; the agents of the research checkout read the one store of HEAD that
        # scripts/fr builds once under the build lock (F-05). CI may run the gate over a marked tree, as gate.sh allows
        print("build: this is the research checkout (git config rq.researchCheckout is true). A research agent never "
              "builds a store by hand: scripts/fr builds the one store of HEAD once, under the build lock, and every "
              "agent reads it. --check is a gate check, and --public is a publish step: they run in CI or in an own "
              "clone (AGENTS.md section 2 rule 14).", file=sys.stderr)
        return 2
    tmp = os.path.join(repo, ".tmp", "fshy")
    report = {}
    if a.public and not a.allow_dirty:
        # the public store says which commit it is; an uncommitted edit would be published under that commit
        r = subprocess.run(["git", "-C", repo, "status", "--porcelain", "--", "dossier", "history", "registry",
                            "sources/MANIFEST.tsv", "scripts/fshy"], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            print("build: --public refuses a tree with uncommitted changes to its inputs; commit them, or build "
                  "from a clean checkout of the commit to publish:\n%s" % r.stdout.rstrip()[:1500], file=sys.stderr)
            return 1
    if a.public or a.check:
        pub = a.public or os.path.join(tmp, "public.db")
        counts, rc = build(repo, pub, "public", a.as_of)
        report["public"] = counts
        hits = leak_scan(pub)
        hits += personal_scan(load(repo), json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8")))
        report["leaks"] = len(hits)
        for rid, text in PRICE_VIOLATIONS[:40]:
            print("PRICE %s: %s" % (rid, text), file=sys.stderr)
        if PRICE_VIOLATIONS:
            print("price check: %d record(s) with a usd_month below the monthly price they state; nothing is published"
                  % len(PRICE_VIOLATIONS), file=sys.stderr)
            report["times"] = TIMES
            print(json.dumps(report, default=str))
            return 1
        if hits:
            for k, ctx in hits[:40]:
                print("LEAK %s: ...%s..." % (k, ctx.replace("\n", " ")), file=sys.stderr)
            print("leak scan: %d hit(s); nothing is published" % len(hits), file=sys.stderr)
            report["times"] = TIMES
            print(json.dumps(report, default=str))
            return 1
    elif a.local:
        counts, rc = build(repo, a.local, "local", a.as_of)
        report["local"] = counts
        report["path"] = a.local
    else:
        # the store of HEAD, built once under the build lock and never replaced (fr.py ensure_store)
        import fr
        loc = fr.ensure_store(repo, force=True)
        report["path"] = loc
    report["times"] = TIMES
    report["total_s"] = round(sum(TIMES.values()), 2)
    if not a.quiet:
        print(json.dumps(report, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
