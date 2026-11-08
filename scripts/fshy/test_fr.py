#!/usr/bin/env python3
"""test_fr.py: selftest for fr. Every write runs on a copy of a few dossier records in a temporary
repository; the real dossier/, history/ and registry/ are only read.

usage:
  python scripts/fshy/test_fr.py           # unit checks, writer round-trip over dossier/, writes on a copy, MCP
  python scripts/fshy/test_fr.py --real    # also read-only commands against the real store, with output sizes
  python scripts/fshy/test_fr.py -v        # print every check

Exit codes: 0 every check passed, 1 a check failed, 2 usage.
"""
import argparse
import datetime as dt
import difflib
import glob
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FR = os.path.join(HERE, "fr.py")
sys.path.insert(0, HERE)
import fr  # noqa: E402
import primer  # noqa: E402

FAILS = []
VERBOSE = [False]
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")


def check(name, cond, detail=""):
    if not cond:
        FAILS.append(name)
    if VERBOSE[0] or not cond:
        print("%s  %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + str(detail)[:300]) if detail and not cond else ""))
    return cond


def run(repo, *args, stdin=None):
    p = subprocess.run([sys.executable, FR, "--repo", repo] + list(args), capture_output=True, text=True,
                       encoding="utf-8", input=stdin, timeout=600)
    return p.returncode, p.stdout, p.stderr


def rb(path):
    with open(path, "rb") as f:
        return f.read()


def ledger_lines(repo):
    p = os.path.join(repo, "history", "ledger.jsonl")
    return open(p, encoding="utf-8").read().splitlines() if os.path.exists(p) else []


# ---------------------------------------------------------------------------------------------- units

def units():
    ok, bad = [], []
    for q in ("SELECT 1", "select count(*) from record;", "SELECT 'delete me; drop' AS w",
              "WITH x AS (SELECT 1 AS a) SELECT a FROM x", "SELECT 1 -- DROP TABLE record\n",
              "SELECT name FROM pragma_table_info('record')", "EXPLAIN SELECT 1", "VALUES (1)"):
        try:
            fr.guard_sql(q, 50)
            ok.append(q)
        except fr.Fail as e:
            bad.append((q, str(e)))
    check("sql guard accepts read-only statements", not bad, bad)
    refused = []
    for q in ("DELETE FROM record", "SELECT 1; DROP TABLE record", "PRAGMA table_info(record)",
              "ATTACH 'x.db' AS y", "WITH x AS (SELECT 1) DELETE FROM record", "SELECT 1; SELECT 2",
              "UPDATE record SET verdict='dead'", "SELECT * FROM record /* ok */ ; INSERT INTO meta VALUES (1,2)",
              "CREATE TEMP TABLE t (a)", "WITH x AS (SELECT 1) REPLACE INTO meta VALUES ('a','b')"):
        try:
            fr.guard_sql(q, 50)
            refused.append(q)
        except fr.Fail:
            pass
    check("sql guard refuses writes, pragmas and second statements", not refused, refused)
    check("sql guard appends LIMIT on its own line", fr.guard_sql("SELECT 1 -- note", 7) == ("SELECT 1 -- note\nLIMIT 7", True))
    check("sql guard keeps an explicit LIMIT", fr.guard_sql("SELECT 1 LIMIT 3;", 7) == ("SELECT 1 LIMIT 3", False))
    for q in ("SELECT 'open", "SELECT 1 /* open", "SELECT [open"):
        try:
            fr.guard_sql(q, 7)
            check("sql guard refuses an unterminated literal: %s" % q, False)
        except fr.Fail:
            check("sql guard refuses an unterminated literal: %s" % q, True)

    check("fts query: CJK run becomes bigrams", fr.fts_query("百度网盘") ==
          "百度 度网 网盘", fr.fts_query("百度网盘"))
    check("fts query: prefixes and quoted punctuation", fr.fts_query("Hetzner s3-compatible no") ==
          'hetzner* "s3-compatible" no', fr.fts_query("Hetzner s3-compatible no"))
    check("fts query: operators and quotes are neutralised", fr.fts_query('OR "x" -y NEAR') == 'or x "-y" near*',
          fr.fts_query('OR "x" -y NEAR'))
    rep = [("stor stor stor stor", "stor*"), ('gpu hours gpu "gpu" hours', "gpu* hours*"), ("a-b a-b", '"a-b"'),
           ("Hetzner hetzner", "hetzner*"), ("ab ab abc ABC", "ab abc*"), ('"x" x x', "x"),
           ('x-y "x-y" x_y', '"x-y" "x_y"'), ("百度网盘 百度网盘", "百度 度网 网盘")]
    check("fts query: a repeated term is kept once, the first copy in place", [fr.fts_query(a) for a, _ in rep] ==
          [b for _, b in rep], [(a, fr.fts_query(a), b) for a, b in rep if fr.fts_query(a) != b])

    # a ledger row's title, as the Worker's worklist changes gives it (LEDGER_TITLE_SQL of site/worker/api.js)
    cases = [(('"a"', '"b"', "set", "$.notes", None), '"a" -> "b"'), ((None, "x", None, None, None), " -> x"),
             ((None, None, "confirm", "$.verified_at", "https://a"), fr.LEDGER_TITLE["confirm"]),
             ((None, None, "append_evidence", None, "https://a"), "evidence row added"),
             ((None, None, None, "$.notes", None), fr.LEDGER_NO_OP["field"]),
             ((None, None, "later_op", None, "https://a"), fr.LEDGER_NO_OP["url"]),
             ((None, None, None, None, None), fr.LEDGER_NO_OP["none"])]
    bad = [(a, fr.ledger_title(*a), want) for a, want in cases if fr.ledger_title(*a) != want]
    check("ledger title: the values, else the op, else the shape of the row", not bad, bad)
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "history", "ledger", "run1"))
        with open(os.path.join(d, "history", "ledger.jsonl"), "w", encoding="utf-8") as f:
            f.write(json.dumps({"at": "2026-10-30T00:00:00Z", "rid": "storage/a", "path": "$.notes", "old": "x",
                                "new": "y", "reason": "amend"}) + "\n")
        with open(os.path.join(d, "history", "ledger", "run1", "u01.jsonl"), "w", encoding="utf-8") as f:
            f.write(json.dumps({"at": "2026-10-31T00:00:00Z", "op": "append_evidence", "rid": "storage/a",
                                "evidence": {"url": "https://a"}}) + "\n")
        import derive
        got = [(r[1], r[10]) for r in derive.parse_ledger(d)]
    check("ledger op: a unit line carries its op, a line of fr amend has none", got ==
          [("storage/a", None), ("storage/a", "append_evidence")], got)

    # the fuzzy tier counts each distinct query word once and runs for at most 8 distinct words (rank.js)
    nidx = fr.name_index([("nato", "alpha bravo charlie delta echo foxtrot golf hotel india"), ("cf", "cloudflare")])
    nato8 = "alphaa bravo charlie delta echo foxtrot golf hotel"
    cases = [(nato8 + " india", {}), (nato8, {"nato": 30}), (nato8 + " hotel india", {}),
             ("alphaa alphaa alphaa " + nato8[7:], {"nato": 30}), (" ".join(["cloudfare"] * 9), {"cf": 30}),
             ("cloudfare nato", {}), ("***", {})]
    bad = [(q, fr.score_names(nidx, q), want) for q, want in cases if fr.score_names(nidx, q) != want]
    check("name scores: a repeated word counts once, and 9 distinct words get no fuzzy tier", not bad, bad)

    check("path: quoted key", fr.parse_jpath('$.extras."NAT Start".price') == ["extras", "NAT Start", "price"])
    check("path: index", fr.parse_jpath("$.limits[2].value") == ["limits", 2, "value"])
    check("path: bare dotted", fr.parse_jpath("free_tier.stated") == ["free_tier", "stated"])
    try:
        fr.parse_jpath("$.a..b")
        check("path: malformed is refused", False)
    except fr.Fail as e:
        check("path: malformed is refused", e.code == 2)
    check("jpath round trip", fr.jpath(fr.parse_jpath('$.extras."NAT Start".price')) == '$.extras."NAT Start".price')

    # matchinfo 'pcnalx' for one phrase, nine columns, hits in name (col 0) and notes (col 6)
    def blob(col, tf=2, df=5):
        c = 9
        mi = [1, c, 100] + [10] * c + [10] * c
        x = [0] * (3 * c)
        x[3 * col], x[3 * col + 1], x[3 * col + 2] = tf, tf * df, df
        return struct.pack("@%dI" % len(mi + x), *(mi + x))
    sn, so = fr.bm25(blob(0)), fr.bm25(blob(6))
    check("bm25: a name hit outranks the same hit in notes, by the weight ratio 4:1",
          sn > so > 0 and abs(sn / so - 4.0) < 1e-9, (sn, so))
    check("bm25: matched columns", fr.matched_cols(blob(6)) == "notes")
    check("edit distance is plain Levenshtein, as in the Worker", fr.lev("hetzner", "hetzne", 1) == 1 and
          fr.lev("hetzenr", "hetzner", 2) == 2 and fr.lev("kitten", "sitting", 2) == 3)
    check("hosted first: a stable partition that keeps each part's order",
          fr.hosted_first(["s1", "h1", "s2", "h2", "h3"], lambda x: x.startswith("s")) == ["h1", "h2", "h3", "s1", "s2"])

    class Names:  # the three reads name_scores makes, with entity e-tool self-hosted in every record
        _names = None

        def q(self, sql, args=()):
            return [("e-box", "Acme Box"), ("e-tool", "Acme")] if "alias" in sql else [("e-box", 3), ("e-tool", 0)]

        def self_hosted(self):
            return set(), {"e-tool"}
    check("an entity whose every record is self-hosted comes after every other entity, even on an exact name",
          [e for e, _, _ in fr.name_scores(Names(), "acme")] == ["e-box", "e-tool"], fr.name_scores(Names(), "acme"))
    # a name lookup resolves by score first: the exact self-hosted vendor, not the hosted prefix match listed above it
    got = fr.resolve_entity(fr.name_scores(Names(), "acme"))
    check("fr entity NAME resolves to the best-scoring entity, even when it is wholly self-hosted",
          got is not None and got[0] == "e-tool" and got[2] == "exact", got)
    check("a hosted entity wins a name lookup only on a tied score",
          fr.resolve_entity([("hosted", 60, "prefix"), ("self", 60, "prefix")])[0] == "hosted" and
          fr.resolve_entity([("hosted", 30, "fuzzy"), ("self", 100, "exact")])[0] == "self" and
          fr.resolve_entity([]) is None)
    check("best_vorder: the best hosted verdict, else the best of all, else None",
          [fr.best_vorder(m) for m in ([(0, 1), (6, 0)], [(0, 1), (3, 1)], [(2, 0), (1, 0), (0, 1)], [(5, 0)], [])]
          == [6, 0, 1, 5, None])


def writer_roundtrip():
    files = sorted(glob.glob(os.path.join(REPO, "dossier", "*", "*.json")))
    bad, n = [], 0
    for p in files:
        text = rb(p).decode("utf-8")
        root = fr.parse_spans(text)
        v = json.loads(text)
        if fr.dump_preserving(text, root, v) != text:
            bad.append(os.path.relpath(p, REPO))
        v["evidence"].append({"url": "https://example.org/selftest", "date": "2026-10-01", "proved": "selftest row"})
        out = fr.dump_preserving(text, root, v)
        if not fr.same(json.loads(out), v):
            bad.append(os.path.relpath(p, REPO) + " (modified)")
        n += 1
    check("writer reproduces all %d dossier files byte-for-byte, and a changed copy reads back equal" % n,
          n > 0 and not bad, bad[:5])


# a worked query that lists record ids, and the first key of its ORDER BY (the twin of publish/test_publish.py)
LISTS_RIDS = re.compile(r"^SELECT (?:\w+\.)?rid\b")
SELF_HOSTED_FIRST = re.compile(r"\bORDER BY (?:\w+\.)?self_hosted\b")
LIMIT_TAIL = re.compile(r"\s+LIMIT \d+\s*$")


def primer_order_checks():
    """Every worked query of the primer that lists record ids sorts on self_hosted first, so a reader who pages it or
    raises its LIMIT still gets every hosted row before a self-hosted one."""
    lists = [(what, sql) for what, sql in primer.EXAMPLES if LISTS_RIDS.match(sql)]
    bad = [what for what, sql in lists if not SELF_HOSTED_FIRST.search(sql)]
    check("each worked query of the primer that lists record ids sorts on self_hosted first (%d queries)" % len(lists),
          lists and not bad, bad)


def primer_checks(db_paths):
    primer_order_checks()
    for p in db_paths:
        if not os.path.exists(p):
            continue
        t = primer.text(p)
        # the budget holds the primer of the real store: its tables (ledger.op since schema 3), its vocabularies, and
        # the worked queries that it shares with the public primer (publish/primer.py), which the export compares
        check("primer under 7,600 characters (%s): %d" % (os.path.basename(p), len(t)), len(t) <= 7600, len(t))
        check("primer is ASCII apart from the CJK example (%s)" % os.path.basename(p),
              all(ord(c) < 128 or "一" <= c <= "鿿" for c in t))
        db = primer.connect(p)
        try:
            errs, order = [], []
            cols = {r[1] for r in db.execute("SELECT * FROM pragma_table_info('record')")}
            sh = {r for (r,) in db.execute("SELECT rid FROM record WHERE self_hosted = 1")} \
                if "self_hosted" in cols else set()
            for what, sql in primer.EXAMPLES:
                try:
                    db.execute(sql).fetchall()
                    if LISTS_RIDS.match(sql):
                        # the whole list, without its LIMIT: a hosted row is never below a self-hosted one
                        flags = [r[0] in sh for r in db.execute(LIMIT_TAIL.sub("", sql))]
                        if flags != sorted(flags):
                            order.append(what)
                except Exception as e:  # noqa: BLE001
                    errs.append((what, str(e)))
                try:
                    fr.guard_sql(sql, 50)
                except fr.Fail as e:
                    errs.append((what, "guard: %s" % e))
            check("primer examples run and pass the guard (%s)" % os.path.basename(p), not errs, errs)
            check("primer examples list every hosted row first, without their LIMIT (%s, %d self-hosted records)"
                  % (os.path.basename(p), len(sh)), not order, order)
        finally:
            db.close()


# ---------------------------------------------------------------------------------------------- copy

def pick_records():
    files = sorted(glob.glob(os.path.join(REPO, "dossier", "*", "*.json")))
    rid = lambda p: "%s/%s" % (os.path.basename(os.path.dirname(p)), os.path.basename(p)[:-5])
    styles = {}
    for p in files:
        b = rb(p)
        o = json.loads(b.decode("utf-8"))
        crlf = b"\r\n" in b
        ind = fr.file_style(b.decode("utf-8"))[1]
        key = "crlf" if crlf else ("ind1" if ind == 1 else None)
        if key and key not in styles:
            styles[key] = rid(p)
        if "documented" not in styles and o.get("confidence") == "documented" and not crlf and ind == 2:
            styles["documented"] = rid(p)
    want = {"lf2": "storage/hetzner-storage-box", "inline": "ip-proxy/proxyseller-isp-proxy",
            "dead": "storage/hetzner-storage-box-bx21", "dup": "storage/hetzner-storage-box-bx41"}
    for k, r in want.items():
        if os.path.exists(os.path.join(REPO, "dossier", r + ".json")):
            styles[k] = r
    extra = [rid(p) for p in files if "/storage/" in p.replace("\\", "/")][:12]
    return styles, sorted(set(list(styles.values()) + extra))


def make_copy(rids):
    tmp = tempfile.mkdtemp(prefix="fr-selftest-")
    for r in rids:
        src = os.path.join(REPO, "dossier", r + ".json")
        dst = os.path.join(tmp, "dossier", r + ".json")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
    d = os.path.join(tmp, "scripts", "dossier")
    os.makedirs(d)
    for f in ("schema.json", "validate.py", "staleness.py", "staleness.policy.json"):
        shutil.copyfile(os.path.join(REPO, "scripts", "dossier", f), os.path.join(d, f))
    os.makedirs(os.path.join(tmp, "registry"))
    with open(os.path.join(tmp, "registry", "entities.tsv"), "wb") as f:
        f.write(b"rid\teid\tname\treason\n")
    with open(os.path.join(tmp, "registry", "relations.tsv"), "wb") as f:
        f.write(b"src\tkind\tdst\tevidence_url\tdate\treason\n")
    os.makedirs(os.path.join(tmp, "history"))
    return tmp


def diff_lines(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    removed, added = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            removed += a[i1:i2]
            added += b[j1:j2]
    return removed, added


def writes(tmp, styles):
    ev = ["--evidence", "https://example.org/selftest", "--date", dt.datetime.now(dt.timezone.utc).date().isoformat(),
          "--proved", "selftest: the page states the new value"]
    path = lambda r: os.path.join(tmp, "dossier", r + ".json")
    nfiles = lambda: len(glob.glob(os.path.join(tmp, "dossier", "*", "*.json")))

    code, out, err = run(tmp, "verify")
    check("verify builds the copy's store", code == 0 and "rebuilt" in out, out + err)
    n0 = nfiles()

    # --- amend: minimal diff on a 2-space LF record, ledger written, store rebuilt
    a = styles["lf2"]
    before = rb(path(a)).decode("utf-8")
    old_stated = json.loads(before)["free_tier"]["stated"]
    code, out, err = run(tmp, "amend", a, "$.free_tier.stated", "1 TB (BX11) selftest value", *ev, "--reason", "selftest")
    after = rb(path(a)).decode("utf-8")
    check("amend exits 0", code == 0, out + err)
    removed, added = diff_lines(before.splitlines(), after.splitlines())
    tgt = [l for l in before.splitlines() if '"stated": ' + json.dumps(old_stated, ensure_ascii=False) in l]
    check("amend diff is minimal: only the value line and the evidence tail change",
          tgt and tgt[0] in removed and len(removed) <= 2 and all(l.strip() == "}" for l in removed if l != tgt[0])
          and 6 <= len(added) <= 7 and sum(1 for l in added if '"url": "https://example.org/selftest"' in l) == 1,
          (removed, added))
    check("amend keeps every untouched line byte-identical",
          all(l in after.splitlines() for l in before.splitlines() if l not in removed))
    check("amend prints a diff summary and a commit subject under 100 characters",
          "commit subject: " in out and all(len(l) < 117 for l in out.splitlines() if l.startswith("commit subject"))
          and not re.search(r"commit subject: .*\.$", out, re.M), out)
    check("amend rebuilds the store after writing", "store rebuilt" in out, out)
    lg = ledger_lines(tmp)
    rec = json.loads(lg[-1]) if lg else {}
    check("amend appends one ledger line with the contract keys",
          len(lg) == 1 and list(rec)[:8] == ["at", "rid", "path", "old", "new", "rung", "evidence", "reason"]
          and rec["old"] == old_stated and rec["path"] == "$.free_tier.stated" and STAMP.match(rec["at"]), lg)

    # --- same amend again: no change, nothing written
    code, out, err = run(tmp, "amend", a, "$.free_tier.stated", "1 TB (BX11) selftest value", *ev, "--no-rebuild")
    check("repeating an amend writes nothing", code == 0 and "no change" in out and rb(path(a)).decode("utf-8") == after
          and len(ledger_lines(tmp)) == 1, out + err)

    # --- CRLF and 1-space files keep their style
    for key, ind in (("crlf", None), ("ind1", 1)):
        if key not in styles:
            check("a %s record exists to test" % key, False)
            continue
        r = styles[key]
        b0 = rb(path(r))
        code, out, err = run(tmp, "amend", r, "$.chaining", "selftest chaining sentence", *ev, "--no-rebuild")
        b1 = rb(path(r))
        t1 = b1.decode("utf-8")
        o1 = json.loads(t1)
        if key == "crlf":
            check("CRLF record stays CRLF throughout", code == 0 and b1.count(b"\n") == b1.count(b"\r\n") and
                  b1.endswith(b"\r\n") == b0.endswith(b"\r\n"), out + err)
        else:
            check("1-space record keeps 1-space indent", code == 0 and
                  t1 == json.dumps(o1, indent=1, ensure_ascii=False) + "\n", out + err)

    # --- inline objects survive an unrelated amend
    if "inline" in styles:
        r = styles["inline"]
        t0 = rb(path(r)).decode("utf-8")
        inl = [l for l in t0.splitlines() if l.strip().startswith("{") and l.strip().endswith(("}", "},"))]
        code, out, err = run(tmp, "amend", r, "$.reliability_note", "selftest reliability", *ev, "--no-rebuild")
        t1 = rb(path(r)).decode("utf-8")
        check("single-line objects stay single-line", code == 0 and inl and all(l in t1.splitlines() for l in inl),
              out + err)

    # --- validation failure, refusals and dry run leave the file and the ledger untouched
    nl = len(ledger_lines(tmp))
    b0 = rb(path(a))
    code, out, err = run(tmp, "amend", a, "$.free_tier.unit", "parsecs", *ev, "--no-rebuild")
    check("an invalid value exits 1 and writes nothing", code == 1 and rb(path(a)) == b0 and
          len(ledger_lines(tmp)) == nl and "validate" in err, (code, err))
    for p, v in (("$.stale", "true"), ("$.stale_checked_at", '"2026-10-01T00:00:00.000Z"'), ("$.nonsense", "1"),
                 ("$.verified_at", '"2026-10-01T00:00:00.000Z"'), ("$.slug", '"x"')):
        code, out, err = run(tmp, "amend", a, p, v, *ev, "--no-rebuild")
        check("refused path %s exits 2 and writes nothing" % p, code == 2 and rb(path(a)) == b0, (code, err))
    code, out, err = run(tmp, "amend", a, "$.reliability_note", "dry run text", *ev, "--dry-run")
    check("dry run shows the diff and writes nothing", code == 0 and "dry run" in out and rb(path(a)) == b0 and
          len(ledger_lines(tmp)) == nl, out + err)
    code, out, err = run(tmp, "amend", a, "$.free_tier.stated", "x", "--evidence", "ftp://x", "--date", "2026-10-01",
                         "--proved", "selftest proved", "--no-rebuild")
    check("a non-http evidence URL is refused", code == 2 and rb(path(a)) == b0, err)
    code, out, err = run(tmp, "amend", a, "$.free_tier.stated", "x", "--evidence", "https://example.org", "--date",
                         "2999-01-01", "--proved", "selftest proved", "--no-rebuild")
    check("a future evidence date is refused", code == 2 and rb(path(a)) == b0, err)

    # --- rung: lowered, never raised
    if "documented" in styles:
        r = styles["documented"]
        code, out, err = run(tmp, "amend", r, "$.reliability_note", "selftest rung", *ev, "--rung", "reported",
                             "--no-rebuild")
        o = json.loads(rb(path(r)).decode("utf-8"))
        check("a weaker rung lowers confidence", code == 0 and o["confidence"] == "reported", out + err)
        lr = json.loads(ledger_lines(tmp)[-1])
        check("the ledger line records the lowered confidence", lr.get("also", {}).get("$.confidence") ==
              ["documented", "reported"], lr)
    conf_a = json.loads(rb(path(a)).decode("utf-8"))["confidence"]
    code, out, err = run(tmp, "amend", a, "$.retention.stated", "selftest retention", *ev, "--rung", "measured",
                         "--no-rebuild")
    check("a stronger rung never raises confidence", code == 0 and
          json.loads(rb(path(a)).decode("utf-8"))["confidence"] == conf_a, out + err)
    b0 = rb(path(a))
    code, out, err = run(tmp, "amend", a, "$.confidence", "measured", *ev, "--no-rebuild")
    check("raising confidence by path needs a rung that strong", code == 2 and rb(path(a)) == b0, err)

    # --- --verified, extras with a quoted key
    code, out, err = run(tmp, "amend", a, '$.extras."NAT Start".price', "5", *ev, "--verified", "--no-rebuild")
    o = json.loads(rb(path(a)).decode("utf-8"))
    va = o.get("verified_at", "")
    age = (dt.datetime.now(dt.timezone.utc) - dt.datetime.strptime(va, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=dt.timezone.utc)).total_seconds() if STAMP.match(va) else 1e9
    check("--verified writes the machine clock in UTC with milliseconds", code == 0 and 0 <= age < 600, (va, err))
    check("an extras path with a quoted key is created as a number", o["extras"].get("NAT Start") == {"price": 5})

    # --- dead
    r = styles["dead"]
    code, out, err = run(tmp, "dead", r, "--cause", "free-tier-removed", "--observed", "2026-10-20", "--evidence",
                         "https://example.org/gone", "--proved", "selftest: the plan page returns 404", "--no-rebuild")
    o = json.loads(rb(path(r)).decode("utf-8"))
    check("dead sets the verdict and extras.death", code == 0 and o["verdict"] == "dead" and
          o["extras"]["death"] == {"on": "2026-10-20", "cause": "free-tier-removed"} and
          o["evidence"][-1]["url"] == "https://example.org/gone", out + err)
    check("dead deletes nothing", nfiles() == n0)
    lr = json.loads(ledger_lines(tmp)[-1])
    check("dead writes a ledger line", lr["rid"] == r and lr["path"] == "$.verdict" and lr["new"] == "dead", lr)

    # --- relate and entity-set
    d = styles["dup"]
    rel = ["--evidence", "https://example.org/same", "--date", "2026-10-20", "--reason", "selftest: the same plan page"]
    code, out, err = run(tmp, "relate", d, "duplicate_of", r, *rel, "--no-rebuild")
    rows = open(os.path.join(tmp, "registry", "relations.tsv"), encoding="utf-8").read().splitlines()
    check("relate appends one row", code == 0 and len(rows) == 2 and rows[1].split("\t")[:3] ==
          [d, "duplicate_of", r] and len(rows[1].split("\t")) == 6, (out, err, rows))
    code, out, err = run(tmp, "relate", d, "duplicate_of", r, *rel, "--no-rebuild")
    check("relate refuses a repeated row", code == 1, err)
    code, out, err = run(tmp, "relate", r, "duplicate_of", d, *rel, "--no-rebuild")
    check("relate refuses a duplicate_of cycle", code == 1, err)
    code, out, err = run(tmp, "entity-set", a, "selftest-vendor", "--name", "Selftest Vendor", "--reason",
                         "selftest: pin to a test entity", "--no-rebuild")
    rows = open(os.path.join(tmp, "registry", "entities.tsv"), encoding="utf-8").read().splitlines()
    check("entity-set appends one row", code == 0 and rows[-1].split("\t") ==
          [a, "selftest-vendor", "Selftest Vendor", "selftest: pin to a test entity"], (out, err, rows))

    # --- add
    newrid = "storage/fr-selftest-provider"
    code, out, err = run(tmp, "add", newrid, "--provider", "Hetzner Selftest", "--url", "https://www.hetzner.com/x",
                         "--evidence", "https://www.hetzner.com/x", "--date", "2026-10-20", "--proved",
                         "selftest: the page exists", "--no-rebuild")
    p = path(newrid)
    o = json.loads(rb(p).decode("utf-8")) if os.path.exists(p) else {}
    check("add writes a schema-valid skeleton", code == 0 and o.get("confidence") == "unverified" and
          o.get("interface") == ["unknown"] and o["extras"]["placeholders"] and not fr.validate_record(tmp, o),
          out + err)
    check("add names similar existing entities", "hetzner" in out.lower() and "entity" in out, out)
    code, out, err = run(tmp, "add", newrid, "--provider", "x", "--url", "https://example.org", "--evidence",
                         "https://example.org", "--date", "2026-10-20", "--proved", "selftest proved", "--no-rebuild")
    check("add refuses an existing rid", code == 1, err)

    # --- the store sees all of it after one rebuild
    code, out, err = run(tmp, "verify")
    check("verify rebuilds after writes", code == 0 and "rebuilt" in out, out + err)
    q = lambda s: json.loads(run(tmp, "sql", s, "--json")[1])["rows"]
    check("the store carries the relation as duplicate_of", q("SELECT duplicate_of FROM record WHERE rid='%s'" % d)
          == [[r]])
    check("the store carries the entity override", q("SELECT eid FROM record WHERE rid='%s'" % a) == [["selftest-vendor"]])
    check("the store carries the ledger", q("SELECT count(*) FROM ledger")[0][0] == len(ledger_lines(tmp)))
    check("the store carries the new record", q("SELECT verdict FROM record WHERE rid='%s'" % newrid) == [["trial-only"]])

    # --- a self-hosted record is the last resort: every list puts it after every hosted one
    first = q("SELECT rid, provider, eid FROM record WHERE topic='storage' AND duplicate_of IS NULL "
              "ORDER BY vorder, rid LIMIT 1")
    sh, prov, eid = first[0] if first else (None, None, None)
    code, out, err = run(tmp, "amend", sh, "$.self_hosted", "true", *ev, "--no-rebuild")
    check("amend sets self_hosted and the schema takes it", code == 0 and
          json.loads(rb(path(sh)).decode("utf-8")).get("self_hosted") is True, out + err)
    code, out, err = run(tmp, "amend", sh, "$.self_hosted", '"yes"', *ev, "--no-rebuild")
    check("self_hosted takes a boolean only", code == 1 and "validate" in err, (code, err))
    run(tmp, "verify")
    check("the store carries self_hosted", q("SELECT rid FROM record WHERE self_hosted = 1") == [[sh]])
    check("entity.best_vorder is the best verdict of the hosted records once one record is self-hosted",
          q("SELECT best_vorder FROM entity WHERE eid='%s'" % eid) ==
          q("SELECT min(vorder) FROM record WHERE eid='%s' AND self_hosted = 0" % eid),
          q("SELECT rid, vorder, self_hosted FROM record WHERE eid='%s'" % eid))
    check("entity.best_vorder: hosted records only, all records only when every one is self-hosted",
          q(BEST_VORDER_BAD) == [[0]], q(BEST_VORDER_BAD))
    for name, args in (("filter", ["filter", "--topic", "storage", "--limit", "200"]),
                       ("filter by price, descending, NULL kept", ["filter", "--topic", "storage", "--sort",
                                                                   "usd_per_tb_month", "--order", "desc", "--keep-null",
                                                                   "--limit", "200"]),
                       ("filter by provider", ["filter", "--sort", "provider", "--limit", "200"]),
                       ("search by its own name", ["search", prov or "x", "--limit", "50"]),
                       ("entity", ["entity", eid or "x", "--limit", "200"]),
                       ("worklist stale", ["worklist", "stale", "--forecast-days", "3650", "--limit", "200"])):
        code, out, err = run(tmp, *args, "--json")
        o = json.loads(out) if code == 0 else {}
        cols = o.get("columns", [])
        rows = o.get("rows", [])
        flags = [r[cols.index("self_hosted")] for r in rows] if "self_hosted" in cols else []
        rids = [r[0] for r in rows]
        check("%s lists the self-hosted record after every hosted one" % name,
              sh in rids and flags[rids.index(sh)] == "yes" and flags == sorted(flags, key=lambda f: f == "yes")
              and len(rows) >= 2, (out[:300], err))
    # the worklists and cites that carry no self_hosted column: their rids, read against the store, are hosted first
    db = sqlite3_ro(fr.store_file(tmp))
    try:
        shs = {r for (r,) in db.execute("SELECT rid FROM record WHERE self_hosted = 1")}
    finally:
        db.close()
    for name, args, col in (("worklist unknown", ["worklist", "unknown", "--limit", "200"], 0),
                            ("worklist held", ["worklist", "held", "--limit", "200"], 0),
                            ("worklist unparsed", ["worklist", "unparsed", "--limit", "200"], 0),
                            ("worklist drift", ["worklist", "drift", "--limit", "200"], 1),
                            ("cites", ["cites", "https://", "--limit", "200"], 0)):
        code, out, err = run(tmp, *args, "--json")
        rows = json.loads(out).get("rows", []) if code == 0 else None
        flags = [r[col] in shs for r in rows or ()]
        check("%s lists every hosted record's rows before a self-hosted record's" % name,
              rows is not None and flags == sorted(flags), (code, err[:200], flags[:20]))
    st = fr.Store(fr.store_file(tmp), tmp)
    try:
        for srt in ("vorder", "usd_per_tb_month"):
            n = {"sort": srt, "sql": "SELECT rid, %s FROM record WHERE topic='storage'" % srt}
            rows = fr.need_rows(st, n)
            flags = [r[fr.CARD_COLS.index("self_hosted") + 1] for r in rows]
            check("a need sorted by %s lists the self-hosted row after every hosted row, ranked or not" % srt,
                  len(rows) >= 2 and flags[-1] == "yes" and flags.count("yes") == 1, flags)
    finally:
        st.close()

    # --- reads on the copy
    code, out, err = run(tmp, "sql", "DELETE FROM record")
    check("sql DELETE is refused with exit 1", code == 1 and "read-only" in err, (code, err))
    code, out, err = run(tmp, "search", "hetzner")
    check("search returns cards with a matched column", code == 0 and out.startswith("rid\tprovider") and
          "\tmatched\n" in out.split("\n", 1)[0] + "\n" and re.search(r"^# \d+ of \d+ rows", out, re.M), out + err)
    code, out, err = run(tmp, "get", a, "--detail", "full")
    check("get --detail full lists JSON paths", code == 0 and "$.free_tier.stated\t" in out, out[:300] + err)
    code, out, err = run(tmp, "get", a, "--raw", "--json")
    check("get --raw returns the source JSON", code == 0 and json.loads(out)[a]["extras"]["NAT Start"] == {"price": 5})
    code, out, err = run(tmp, "history", a)
    check("history shows the ledger lines", code == 0 and out.count("\tledger\t") >= 3, out + err)
    code, out, err = run(tmp, "filter", "--sort", "usd_per_tb_month", "--limit", "3", "--json")
    o = json.loads(out) if code == 0 else {}
    check("a price sort reports the NULL exclusion", any(n.startswith("excluded for NULL usd_per_tb_month")
                                                         for n in o.get("notes", [])), out + err)
    for k in ("stale", "drift", "changes", "unparsed", "unknown", "held"):
        code, out, err = run(tmp, "worklist", k, "--limit", "3")
        check("worklist %s runs" % k, code == 0 and re.search(r"^# \d+ of \d+ rows", out, re.M), out + err)
    for args in (["need"], ["need", "free-storage-no-card"], ["strip", "report"], ["strip", "review"],
                 ["evidence", a], ["cites", "example.org"], ["entity", "hetzner"], ["help"]):
        code, out, err = run(tmp, *args)
        check("fr %s runs" % " ".join(args), code == 0 and out.strip(), (out[:200], err))
    code, out, err = run(tmp, "get", "nope")
    check("a malformed rid in get is reported, not a crash", code in (0, 1, 2) and "Traceback" not in err, err)

    # --- MCP on the copy
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search", "arguments": {"q": "hetzner"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "sql", "arguments": {"query": "DROP TABLE record"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "ping"},
            {"jsonrpc": "2.0", "id": 6, "method": "no/such"}]
    code, out, err = run(tmp, "mcp", stdin="".join(json.dumps(m) + "\n" for m in msgs) + "not json\n")
    resp = {}
    for ln in out.splitlines():
        o = json.loads(ln)
        resp[o.get("id")] = o
    check("mcp answers every request and no notification", code == 0 and sorted(k for k in resp if k) == [1, 2, 3, 4, 5, 6]
          and None in resp, out[:400] + err)
    check("mcp initialize echoes the protocol", resp.get(1, {}).get("result", {}).get("protocolVersion") == "2025-06-18")
    names = [t["name"] for t in resp.get(2, {}).get("result", {}).get("tools", [])]
    check("mcp lists the 8 read tools", names == ["help", "search", "filter", "get", "entity", "need", "sql", "worklist"],
          names)
    r3 = resp.get(3, {}).get("result", {})
    check("mcp search returns TSV text", not r3.get("isError") and r3["content"][0]["text"].startswith("rid\t"), r3)
    check("mcp sql refuses DROP as a tool error", resp.get(4, {}).get("result", {}).get("isError") is True, resp.get(4))
    check("mcp unknown method is -32601", resp.get(6, {}).get("error", {}).get("code") == -32601, resp.get(6))
    check("mcp bad JSON is -32700", resp.get(None, {}).get("error", {}).get("code") == -32700, resp.get(None))


# entities whose best_vorder is not the best verdict of their hosted records (of all records when none is hosted)
BEST_VORDER_BAD = ("SELECT count(*) FROM entity e WHERE e.best_vorder IS NOT (SELECT coalesce(min(CASE WHEN "
                   "r.self_hosted = 0 THEN r.vorder END), min(r.vorder)) FROM record r WHERE r.eid = e.eid)")


PARITY_JS = r"""
const rank = await import(process.argv[1]);
const text = await import(process.argv[2]);
let d = '';
for await (const x of process.stdin) d += x;
const c = JSON.parse(d);
const idx = rank.buildNameIndex(c.aliases);
process.stdout.write(JSON.stringify({
  norm: c.norm.map((s) => text.normalize(s)),
  tokens: c.norm.map((s) => text.tokens(text.normalize(s))),
  match: c.norm.map((s) => text.ftsMatch(s)),
  bm25: c.blobs.map((a) => { const r = rank.bm25(new Uint8Array(new Uint32Array(a).buffer)); return [r.score, r.matched.join(',')]; }),
  lev: c.lev.map(([a, b, m]) => rank.editDistance(a, b, m)),
  names: c.queries.map((q) => rank.scoreNames(idx, q).map((h) => [h.eid, h.score]).sort((x, y) => y[1] - x[1] || (x[0] < y[0] ? -1 : 1))),
  order: typeof rank.sortEntities !== 'function' ? null : c.queries.map((q) => rank.sortEntities(
    rank.scoreNames(idx, q).map((h) => ({ eid: h.eid, score: h.score })), (e) => c.best_vorder[e] ?? 99,
    (e) => c.self_hosted.includes(e)).map((h) => [h.eid, h.score])),
}));
"""


GUARD_JS = r"""
import { readFileSync } from 'node:fs';
const g = await import(process.argv[1]);
const cases = JSON.parse(readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(cases.map((s) => {
  try { const r = g.guard(s, 51); return ['ok', r.sql, r.appendedLimit]; } catch (e) { return ['err']; }
})));
"""

GUARD_CASES = [
    "SELECT 1", "select * from record", "SELECT 1;", "SELECT 1; DROP TABLE x", "  with x as (select 1) select * from x",
    "VALUES (1)", "EXPLAIN SELECT 1", "PRAGMA table_info(record)", "SELECT * FROM pragma_table_info('record')",
    "INSERT INTO x VALUES (1)", "select replace('a','b','c')", "select 'drop table' as s", "select \"delete\" from record",
    "select [update] from record", "select 1 -- drop\n", "select 1 /* insert */", "select 1 /* unterminated",
    "select 'unterminated", "select 1 limit 5", "select 1 LIMIT 5;", "SELECT\u00e9INSERT FROM x",
    "select 1 where x=\u00e9drop", "select \u0645delete from record", "\ufeffselect 1", "", "   ", "\ufeff",
    "select 1\u0000", "attach database 'x' as y", "select temp from record", "select * from record where rid like 'a;b'",
    "select 1   \n\n", "select 1 \ufeff", "\u0085select 1", "select 1\u0085", "select 1;\u0085", "select 1\u0085;", "\x1cselect 1", "with recursive r(n) as (select 1 union all select n+1 from r) select n from r",
]


PIN_FILE = os.path.join(HERE, "public.lock")


def public_pin():
    """The commit of Azathothas/fshy.ajam.dev that fr.py must match (scripts/fshy/public.lock)."""
    for ln in open(PIN_FILE, encoding="utf-8"):
        m = re.match(r"^commit ([0-9a-f]{40})\s*$", ln)
        if m:
            return m.group(1)
    raise SystemExit("%s has no 'commit <40 hex>' line" % PIN_FILE)


def public_worker():
    """-> (the Worker folder at the pinned commit, or None, and a note). The public checkout is $FSHY_PUBLIC (CI
    checks out the pin there), else a checkout named fshy.ajam.dev beside this one. When that checkout is at another
    commit and holds the pinned one, the Worker files of the pin are read from git into .tmp/fshy/; the checkout
    itself is never changed. When it does not hold the pin, the parity check cannot run on the right code."""
    root = os.path.abspath(os.environ.get("FSHY_PUBLIC") or os.path.join(os.path.dirname(REPO), "fshy.ajam.dev"))
    pin = public_pin()
    wk = os.path.join(root, "site", "worker")  # absolute: node takes it as a file URI
    g = lambda *a: subprocess.run(["git", "-C", root] + list(a), capture_output=True)
    if not os.path.isdir(root):
        return None, "no public checkout at %s; parity not run (set FSHY_PUBLIC, or clone it beside this one)" % root
    head = g("rev-parse", "HEAD")
    if head.returncode != 0:
        return (wk if os.path.isdir(wk) else None), ("%s is not a git checkout, so its commit is unknown; its files are "
                                                     "compared as they are, not as the pin %s" % (root, pin[:10]))
    head = head.stdout.decode().strip()
    if head == pin:
        return wk, "public checkout %s at the pin %s" % (root, pin[:10])
    if g("cat-file", "-e", pin + "^{commit}").returncode != 0:
        return None, ("the public checkout %s is at %s and does not hold the pinned commit %s (scripts/fshy/public.lock); "
                      "git -C %s fetch origin, or set FSHY_PUBLIC to a checkout of the pin" % (root, head[:10], pin[:10], root))
    out = os.path.join(REPO, ".tmp", "fshy", "public-pin-" + pin[:12], "site", "worker")
    names = g("ls-tree", "-r", "--name-only", pin, "site/worker").stdout.decode().split()
    for n in names:
        dst = os.path.join(REPO, ".tmp", "fshy", "public-pin-" + pin[:12], *n.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(g("show", "%s:%s" % (pin, n)).stdout)
    return out, "the pinned commit %s read from %s (its checkout is at %s)" % (pin[:10], root, head[:10])


def public_file(rel):
    """A file of the public repository at the pinned commit, or None: from git when the public checkout holds the
    pin, else from the checkout itself when it is at the pin (CI) or is not a git checkout."""
    root = os.path.abspath(os.environ.get("FSHY_PUBLIC") or os.path.join(os.path.dirname(REPO), "fshy.ajam.dev"))
    pin = public_pin()
    r = subprocess.run(["git", "-C", root, "show", "%s:%s" % (pin, rel)], capture_output=True)
    if r.returncode == 0:
        return r.stdout.decode("utf-8")
    p = os.path.join(root, *rel.split("/"))
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def contract_parity():
    """The export contract has three copies in this repository, and a change to one of them passes here and stops
    the next publish. Compare them with the pinned public commit, so the merge session sees it first (R3-A-09)."""
    nocomment = lambda t: "\n".join(ln for ln in t.replace("\r\n", "\n").splitlines() if not ln.lstrip().startswith("--"))
    pub = public_file("publish/schema.sql")
    if pub is None:
        print("skip  contract parity: no public publish/schema.sql at the pin")
        return
    own = open(os.path.join(HERE, "schema.sql"), encoding="utf-8").read()
    check("contract parity: schema.sql equals the public publish/schema.sql at the pin (comment lines aside)",
          nocomment(own) == nocomment(pub))
    pub = public_file("publish/rules/needs.json")
    own = open(os.path.join(HERE, "rules", "needs.json"), encoding="utf-8").read()
    check("contract parity: rules/needs.json equals the public publish/rules/needs.json at the pin",
          pub is not None and json.loads(own) == json.loads(pub))
    pub = public_file("publish/rules/topics.json")
    enum = json.load(open(os.path.join(REPO, "scripts", "dossier", "schema.json"), encoding="utf-8"))["properties"]["topic"]["enum"]
    ids = [t["id"] for t in json.loads(pub)["topics"]] if pub else []
    check("contract parity: the topic enum of scripts/dossier/schema.json equals the public publish/rules/topics.json "
          "at the pin (a new topic lands there first)", sorted(enum) == sorted(ids), sorted(set(enum) ^ set(ids)))
    api = public_file("site/worker/api.js") or ""
    words = {}
    for name in ("LEDGER_TITLE", "LEDGER_NO_OP"):
        m = re.search(r"export const %s = \{(.*?)\n\};" % name, api, re.S)
        words[name] = dict(re.findall(r"(\w+): '([^']*)'", m.group(1))) if m else None
    if words["LEDGER_TITLE"] is None:
        print("skip  ledger titles: the public site/worker/api.js at the pin has no LEDGER_TITLE")
    else:
        check("ledger titles: LEDGER_TITLE and LEDGER_NO_OP of fr.py equal site/worker/api.js at the pin",
              words == {"LEDGER_TITLE": fr.LEDGER_TITLE, "LEDGER_NO_OP": fr.LEDGER_NO_OP}, words)


def fixture_parity(wk, note):
    """site/worker/test/parity.json at the pin: inputs and the JavaScript outputs; the Python twins give the same."""
    fx_path = os.path.join(wk, "test", "parity.json")
    if not os.path.exists(fx_path):
        print("skip  parity fixture: site/worker/test/parity.json is absent at the pinned public commit (%s); the "
              "live comparison below still runs" % note)
        return
    import build
    fx = json.load(open(fx_path, encoding="utf-8"))
    t, r = fx["text"], fx["rank"]
    def same(name, rows):
        bad = [x for x in rows if not x[0]]
        check("parity fixture: %s, %d cases" % (name, len(rows)), not bad, [x[1:] for x in bad][:3])
    same("normalize", [(fr.norm(a) == b, a, fr.norm(a), b) for a, b in t["normalize"]])
    same("tokens", [(fr.tokens(fr.norm(a)) == b, a, b) for a, b in t["tokens"]])
    same("MATCH strings", [(fr.fts_query(a) == b, a, fr.fts_query(a), b) for a, b in t["ftsMatch"]])
    same("index text", [(build.fts_text(a) == b, a, build.fts_text(a), b) for a, b in t["ftsText"]])
    same("edit distance", [(fr.lev(a, b, m) == want, a, b, m, want) for a, b, m, want in r["editDistance"]])
    same("fuzz budget", [(fr.fuzz_budget(a) == want, a, want) for a, want in r["fuzzBudget"]])
    rows = []
    for c in r["bm25"]:
        blob = struct.pack("@%dI" % len(c["matchinfo"]), *c["matchinfo"])
        score = fr.bm25(blob, c["weights"])
        cols = [x for x in (fr.matched_cols(blob) or "").split(",") if x]
        rows.append((abs(score - c["score"]) <= 1e-9 * max(1, abs(c["score"])) and cols == c["matched"], score, c["score"], cols, c["matched"]))
    same("BM25", rows)
    idx = fr.name_index([(a["eid"], a["alias"]) for a in r["names"]["aliases"]])
    rows = []
    for q, want in r["names"]["cases"]:
        got = [[e, sc] for e, sc in sorted(fr.score_names(idx, q).items(), key=lambda kv: (-kv[1], kv[0]))]
        rows.append((got == want, q, got[:4], want[:4]))
    same("name scores", rows)
    if "hostedFirst" in r:
        same("hosted first", [(fr.hosted_first(items, lambda x: x in set(sh)) == want, items, sh, want)
                              for items, sh, want in r["hostedFirst"]])
    if "entityOrder" in r:
        rows = []
        for c in r["entityOrder"]:
            got = [e for e, _ in fr.sort_entities([tuple(h) for h in c["hits"]], lambda e: c["best_vorder"].get(e, 99),
                                                  lambda e: e in set(c["self_hosted"]))]
            rows.append((got == c["order"], c["hits"], got, c["order"]))
        same("entity order", rows)
    if "bestVorder" in r:
        # [[[vorder, self_hosted], ...], want]: the Python twin of rank.bestVorder
        same("best verdict of an entity", [(fr.best_vorder([tuple(x) for x in members]) == want, members,
                                            fr.best_vorder([tuple(x) for x in members]), want)
                                           for members, want in r["bestVorder"]])
    if "entityResolve" in r:
        # {hits, best_vorder, self_hosted, eid}: the entity a name lookup resolves to (rank.resolveEntity)
        rows = []
        for c in r["entityResolve"]:
            ranked = fr.sort_entities([tuple(h) for h in c["hits"]], lambda e: c["best_vorder"].get(e, 99),
                                      lambda e: e in set(c["self_hosted"]))
            hit = fr.resolve_entity(ranked)
            got = hit[0] if hit else None
            rows.append((got == c["eid"], c["hits"], got, c["eid"]))
        same("entity a name resolves to", rows)
    gl = fx.get("guard_lists")
    if gl is not None:
        mine = {"banned": sorted(fr.FORBIDDEN), "odd_space_codes": sorted(fr.ODD_SPACE_CODES),
                "max_sql_chars": fr.MAX_SQL_CHARS, "allowed_functions": sorted(fr.ALLOWED_FUNCTIONS),
                "not_functions": sorted(fr.NOT_FUNCTIONS), "max_width": fr.MAX_WIDTH,
                "printf_refused": sorted(fr.PRINTF_REFUSED)}
        theirs = {k: (sorted(v) if isinstance(v, list) else v) for k, v in gl.items()}
        diff = sorted(k for k in set(mine) | set(theirs) if mine.get(k) != theirs.get(k))
        check("parity fixture: the guard lists (banned, odd white space, functions, widths) equal the twin's", not diff, diff)
    rows = []
    for c in fx["guard"]:
        try:
            run, appended = fr.guard_sql(c["sql"], c["limit"])
            got = ["ok", run, appended]
        except fr.Fail:
            got = ["err"]
        rows.append((got == c["result"], c["sql"], got, c["result"]))
    same("SQL guard", rows)


def worker_parity(db_path):
    """Run the Worker's own text.js, rank.js and guard.js under node on the inputs fr sees, and compare."""
    import pathlib
    import shutil as sh
    node = sh.which("node")
    # the Worker lives in the public repository; a checkout of it beside this one, or $FSHY_PUBLIC, enables the
    # check. CI sets FSHY_REQUIRE_PARITY=1, so there a skip is a failure.
    wk, note = public_worker()
    if wk and os.path.exists(os.path.join(wk, "rank.js")):
        print("      worker parity on %s" % note)
        fixture_parity(wk, note)
        contract_parity()
    if not node or not wk or not os.path.exists(os.path.join(wk, "rank.js")) or not os.path.exists(db_path):
        why = note if not wk else "node, %s or the store %s is absent" % (wk, db_path)
        if os.environ.get("FSHY_REQUIRE_PARITY"):
            check("worker parity runs (FSHY_REQUIRE_PARITY)", False, why)
        else:
            print("skip  worker parity (%s)" % why)
        return
    if os.path.exists(os.path.join(wk, "guard.js")):
        p = subprocess.run([node, "--input-type=module", "-e", GUARD_JS, pathlib.Path(wk, "guard.js").as_uri()],
                           input=json.dumps(GUARD_CASES), capture_output=True, text=True, encoding="utf-8", timeout=120)
        if check("worker parity: node ran guard.js", p.returncode == 0, p.stderr[-400:]):
            js = [tuple(x) for x in json.loads(p.stdout)]
            py = []
            for s in GUARD_CASES:
                try:
                    run, appended = fr.guard_sql(s, 51)
                    py.append(("ok", run, appended))
                except fr.Fail:
                    py.append(("err",))
            diff = [(s, a, b) for s, a, b in zip(GUARD_CASES, py, js) if a != b]
            check("worker parity: the SQL guard on %d statements" % len(GUARD_CASES), not diff, diff[:3])
    strs = ["Hetzner Storage Box", "  Baidu   Pan  ", "百度网盘 Baidu", "Café Étude STRASSE",
            "Straße", "Ｈｅｔｚｎｅｒ", "s3-compatible OR \"x\" -y NEAR", "a\tb  c",
            "云", "R2 object storage", "ovh*", "こんにちは world", "가나다"]
    queries = ["hetzner", "hetzne", "hetzenr", "storage box", "百度", "baidu pan", "s3", "backblaze b2",
               "ovh", "cloudflare r2", "free gpu", "oracle cloud free tier",
               # vendors with a self-hosted record beside hosted ones, and wholly self-hosted ones
               "openlist", "jfrog", "drone", "mattermost", "sonatype", "rclone", "frp", "headscale", "tunnel"]
    lev = [["hetzner", "hetzne", 1], ["hetzenr", "hetzner", 2], ["kitten", "sitting", 2], ["", "abc", 1],
           ["百度", "百", 1]]
    db = sqlite3_ro(db_path)
    try:
        aliases = [{"eid": e, "alias": a, "kind": k} for e, a, k in db.execute("SELECT eid, alias, kind FROM alias")]
        blobs = []
        for mq in ("hetzner*", "storage* box*", "百度", "free* gpu*"):
            for (b,) in db.execute("SELECT matchinfo(text_fts, 'pcnalx') FROM text_fts WHERE text_fts MATCH ? LIMIT 25",
                                   (mq,)):
                blobs.append(list(struct.unpack("@%dI" % (len(b) // 4), b)))
        best_vorder = dict(db.execute("SELECT eid, best_vorder FROM entity"))
        all_sh = [e for (e,) in db.execute("SELECT eid FROM record GROUP BY eid HAVING min(self_hosted) = 1")]
        st = fr.Store(db_path, REPO)
        py_order = [[[e, s] for e, s, _ in fr.name_scores(st, q)] for q in queries]
        py_names = [sorted(o, key=lambda t: (-t[1], t[0])) for o in py_order]
        st.close()
    finally:
        db.close()
    payload = json.dumps({"norm": strs, "aliases": aliases, "blobs": blobs, "lev": lev, "queries": queries,
                          "best_vorder": best_vorder, "self_hosted": all_sh})
    p = subprocess.run([node, "--input-type=module", "-e", PARITY_JS, pathlib.Path(wk, "rank.js").as_uri(),
                        pathlib.Path(wk, "text.js").as_uri()], input=payload, capture_output=True, text=True,
                       encoding="utf-8", timeout=300)
    if not check("worker parity: node ran rank.js and text.js", p.returncode == 0, p.stderr[-400:]):
        return
    js = json.loads(p.stdout)
    check("worker parity: normalize", [fr.norm(s) for s in strs] == js["norm"],
          [(a, b) for a, b in zip([fr.norm(s) for s in strs], js["norm"]) if a != b])
    check("worker parity: tokens", [fr.tokens(fr.norm(s)) for s in strs] == js["tokens"])
    check("worker parity: MATCH strings", [fr.fts_query(s) for s in strs] == js["match"],
          [(a, b) for a, b in zip([fr.fts_query(s) for s in strs], js["match"]) if a != b])
    pyb = [[fr.bm25(struct.pack("@%dI" % len(a), *a)), fr.matched_cols(struct.pack("@%dI" % len(a), *a))] for a in blobs]
    check("worker parity: BM25 on %d real matchinfo rows" % len(blobs), len(blobs) > 10 and all(
        abs(a[0] - b[0]) < 1e-9 * max(1, abs(b[0])) and a[1] == b[1] for a, b in zip(pyb, js["bm25"])),
        [(a, b) for a, b in zip(pyb, js["bm25"]) if abs(a[0] - b[0]) > 1e-9][:3])
    check("worker parity: edit distance", [fr.lev(a, b, m) for a, b, m in lev] == js["lev"])
    diff = [(q, a[:5], b[:5]) for q, a, b in zip(queries, py_names, js["names"]) if a != b]
    check("worker parity: name scores for %d queries" % len(queries), not diff, diff[:2])
    if js.get("order") is None:
        print("skip  worker parity: entity order (the pinned rank.js has no sortEntities)")
    else:
        diff = [(q, a[:6], b[:6]) for q, a, b in zip(queries, py_order, js["order"]) if a != b]
        check("worker parity: the entity order of fr.name_scores equals rank.sortEntities for %d queries"
              % len(queries), not diff, diff[:2])


def sqlite3_ro(path):
    import sqlite3
    from urllib.request import pathname2url
    return sqlite3.connect("file:%s?mode=ro" % pathname2url(os.path.abspath(path)), uri=True)


def real(sizes):
    cmds = [["search", "hetzner"], ["search", "百度"],
            ["filter", "--topic", "storage", "--no-card", "--sort", "usd_per_tb_month", "--limit", "5"],
            ["need", "inference-no-card-no-phone"], ["worklist", "stale", "--forecast-days", "30", "--limit", "5"],
            ["get", "storage/hetzner-storage-box", "--detail", "full"], ["help"], ["entity", "hetzner"],
            ["sql", "SELECT verdict, count(*) FROM record GROUP BY verdict"]]
    for c in cmds:
        code, out, err = run(REPO, *c)
        check("real: fr %s" % " ".join(c), code == 0 and out.strip(), err)
        sizes.append((" ".join(c), len(out)))
    code, out, err = run(REPO, "sql", "DELETE FROM record")
    check("real: fr sql DELETE refused", code == 1 and "read-only" in err, err)
    if os.path.exists(os.path.join(REPO, "history", "ledger.jsonl")):
        pass
    code, out, err = run(REPO, "mcp", stdin=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
        "name": "search", "arguments": {"q": "hetzner", "limit": 5}}}) + "\n")
    check("real: mcp search", code == 0 and json.loads(out)["result"]["content"][0]["text"].startswith("rid\t"), err)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--real", action="store_true", help="also run read-only commands against the real store")
    ap.add_argument("--keep", action="store_true", help="keep the temporary copy")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    VERBOSE[0] = a.verbose
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    marker = subprocess.run(["git", "-C", REPO, "config", "--get", "rq.researchCheckout"], capture_output=True,
                            text=True).stdout.strip().lower()
    if marker == "true" and os.environ.get("RQ_SELFTEST_IN_CHECKOUT") != "1":
        # it copies records and scripts into a temporary folder and builds stores for minutes: CI on the pushed head
        # or an own clone runs it, never the research checkout (LIO5-01)
        print("test_fr: this is the research checkout (git config rq.researchCheckout is true). The selftest copies "
              "records into a temporary folder and runs for minutes, so it runs in CI on the pushed head or in an own "
              "clone, never here (AGENTS.md section 2 rule 14). RQ_SELFTEST_IN_CHECKOUT=1 overrides this.",
              file=sys.stderr)
        return 2
    import hashlib
    import build
    got = hashlib.sha256(open(os.path.join(HERE, "schema.sql"), "rb").read().replace(b"\r\n", b"\n")).hexdigest()
    check("schema.sql is the schema of SCHEMA_VERSION %s (a changed schema bumps the version and SCHEMA_SHA256 in "
          "build.py)" % build.SCHEMA_VERSION, got == build.SCHEMA_SHA256, got)
    units()
    writer_roundtrip()
    styles, rids = pick_records()
    tmp = make_copy(rids)
    real_before = {p: rb(p) for p in [os.path.join(REPO, "dossier", r + ".json") for r in rids]}
    real_ledger = os.path.exists(os.path.join(REPO, "history", "ledger.jsonl")) and \
        rb(os.path.join(REPO, "history", "ledger.jsonl"))
    try:
        writes(tmp, styles)
        # the store of the real checkout's HEAD, where fr itself keeps it (fr.ensure_store), built once under the build
        # lock; a fresh clone has none yet, and the parity check needs the real one (more than 10 matchinfo rows). A
        # store that cannot be built fails here rather than skipping the real-store checks.
        real_db = fr.ensure_store(REPO)
        tmp_db = fr.store_file(tmp)
        if check("real store: built at %s" % os.path.relpath(real_db or "", REPO), bool(real_db) and os.path.exists(real_db),
                 real_db):
            worker_parity(real_db)
            db = sqlite3_ro(real_db)
            try:
                bad = db.execute(BEST_VORDER_BAD).fetchone()[0]
            finally:
                db.close()
            check("real store: entity.best_vorder is the best verdict of the hosted records", bad == 0, bad)
        primer_checks([p for p in (tmp_db, real_db, os.path.join(REPO, ".tmp", "fshy", "public.db")) if p])
    finally:
        if a.keep:
            print("kept", tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    check("the real records were not touched", all(rb(p) == b for p, b in real_before.items()))
    check("the real ledger was not touched", (os.path.exists(os.path.join(REPO, "history", "ledger.jsonl")) and
                                              rb(os.path.join(REPO, "history", "ledger.jsonl"))) == real_ledger)
    sizes = []
    if a.real:
        real(sizes)
        for c, n in sizes:
            print("size  %6d chars  fr %s" % (n, c))
    print("%s: %d failed" % ("FAIL" if FAILS else "PASS", len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
