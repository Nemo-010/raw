#!/usr/bin/env python3
"""fr: query and amend the f-research corpus; also a stdio MCP server over the same reads.

usage:
  fr help                                   the primer: schema, vocabularies, worked queries
  fr search WORDS [--topic T] [--grp G]     names first, then BM25 full text
  fr filter [--topic T] [--no-card] [--sort usd_per_tb_month] ...
  fr get RID... [--detail card|full] [--fields F] [--raw]
  fr entity ID-OR-NAME                      a vendor and its records
  fr need [ID]                              best-per-need lists (rules/needs.json)
  fr sql "SELECT ..."                       guarded read-only SQL
  fr worklist stale|drift|changes|unparsed|unknown|held
  fr evidence RID | fr cites URL-PART | fr history RID
  fr strip report | fr strip review [--rule ID] [--sample N]
  fr verify [--force]                       the store of HEAD: build it once when it is missing (--force: a new file, own clone only)
  fr amend RID PATH VALUE --evidence URL --date D --proved TEXT [--rung R] [--verified]
  fr add TOPIC/SLUG --provider NAME --url URL --evidence URL --date D --proved TEXT
  fr dead RID --cause C --observed D --evidence URL --proved TEXT
  fr relate SRC KIND DST --evidence URL --date D --reason TEXT
  fr entity-set RID EID [--name NAME] --reason TEXT
  fr mcp                                    serve help/search/filter/get/entity/need/sql/worklist on stdio

Global options (before or after the command): --json, --repo DIR, --db FILE, --width N, --no-rebuild.
Output is TSV: a header row, clipped cells, and '# ' footer lines. --json gives
{columns, rows, truncated, total, notes}. Every list of records (search, filter, need, entity, cites and
every worklist but changes, which is a log in time order) puts a self-hosted record (record.self_hosted = 1)
after every hosted one and keeps its own order inside each part. The JSON in dossier/ is the truth: write commands edit
it in place, validate it against scripts/dossier/schema.json, and append to history/ledger.jsonl.
Nothing is ever deleted and nothing is committed.

The store is one file per commit, .tmp/fshy/local-<HEAD 12>-s<F>.db, built once under .tmp/fshy/build.lock and read by
every process; a build never replaces a file another process may hold open. In the research checkout (git config
rq.researchCheckout true) the store of HEAD is fresh when its file exists, and the five write commands refuse: a
record changes there only through a run (AGENTS.md section 2 rule 14).
Exit codes: 0 ok, 1 a defect or a refused write, 2 usage.
"""
import argparse
import collections
import datetime as dt
import difflib
import hashlib
import importlib.util
import json
import math
import os
import re
import sqlite3
import struct
import subprocess
import sys
import time
import unicodedata
from urllib.request import pathname2url

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
# before the first local import: bytecode under .tmp/rq/pycache, and no git process may rewrite the shared index
os.environ["GIT_OPTIONAL_LOCKS"] = "0"
os.environ["PYTHONPYCACHEPREFIX"] = os.path.join(DEFAULT_REPO, ".tmp", "rq", "pycache")
sys.pycache_prefix = os.environ["PYTHONPYCACHEPREFIX"]
sys.path.insert(0, HERE)

FTS_COLUMNS = ("name", "offer", "limits", "egress", "identity", "access", "notes", "evidence", "extras")
FTS_WEIGHTS = (4.0, 2.0, 1.5, 1.5, 1.5, 1.0, 1.0, 0.7, 0.5)
K1, B = 1.2, 0.75
CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]+")
LADDER = ["unverified", "inferred", "reported", "documented", "measured"]  # weakest first
VERDICTS = ["qualifies", "qualifies-with-caveat", "trial-only", "paid-only", "fails-identity", "fails-egress",
            "fails-quota", "dead"]
GROUPS = ["usable", "trial", "paid", "rejected", "dead"]
CAUSES = ["dead-service", "registration-closed", "free-tier-removed", "revoked", "acquired"]
RELATIONS = ["duplicate_of", "variant_of", "successor_of", "same_offer_as"]
SORTS = ["vorder", "usd_month", "usd_per_tb_month", "stale_on", "provider", "verified_at"]
WORKLISTS = ["stale", "drift", "changes", "unparsed", "unknown", "held"]
# The title of a ledger row that holds no old or new value (a public store): what the row did, by its op. A row with no
# op (a store of schema_version 2 or older, or a line of fr amend) or an op not named here gets the title of its shape:
# LEDGER_NO_OP["field"] when it names a field, "url" when it names only a source, "none" when it names neither. The
# twin of LEDGER_TITLE, LEDGER_NO_OP and LEDGER_TITLE_SQL of site/worker/api.js in the public repository.
LEDGER_TITLE = {
    "set": "amended; the old and the new value are not published",
    "basis": "amended; the old and the new value are not published",
    "confirm": "confirmed on its source; only the check date changed",
    "dead": "marked dead",
    "undo": "an earlier change undone",
    "undo_skipped": "undo skipped; the value did not change",
    "append_evidence": "evidence row added",
    "drop_evidence": "evidence row removed",
    "relate": "relation to another record added",
    "add_record": "record added",
}
LEDGER_NO_OP = {
    "field": "amended; the old and the new value are not published",
    "url": "evidence row or relation changed; the row does not say how",
    "none": "record changed; the row names no field",
}


def ledger_op(st):
    """The op column of the ledger, or NULL in a store of schema_version 2 or older, which has none."""
    return "op" if any(r[1] == "op" for r in st.q("PRAGMA table_info(ledger)")) else "NULL"


def ledger_title(old, new, op, path, url):
    """What a ledger row did: 'old -> new' when the store holds the values (the local store), else the title of its op,
    else the title of its shape (the Worker's worklist changes)."""
    if old is not None or new is not None:
        return "%s -> %s" % (old if old is not None else "", new if new is not None else "")
    if op in LEDGER_TITLE:
        return LEDGER_TITLE[op]
    return LEDGER_NO_OP["field" if path else "url" if url else "none"]
REFUSED_PATHS = {"stale": "computed by staleness.py, never written by hand",
                 "stale_checked_at": "computed by staleness.py, never written by hand",
                 "topic": "it is half of the rid; a rename needs a history entry and a new file",
                 "slug": "it is half of the rid; a rename needs a history entry and a new file",
                 "verified_at": "use --verified, which reads the machine clock"}
RID_RE = re.compile(r"^[a-z0-9-]+/[a-z0-9]+(?:-[a-z0-9]+)*$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^(?:https?://\S+|probe:\S+)$")
# rebuild inputs under scripts/fshy that are not read by the local build
NOT_BUILD_INPUTS = {"fr.py", "primer.py", "test_fr.py", "README.md"}

CARD_COLS = ["rid", "provider", "verdict", "self_hosted", "confidence", "identity", "card", "phone", "usd_month",
             "usd_per_tb_month", "stale_on", "summary"]
CARD_SQL = ("r.rid, r.provider, r.verdict, CASE r.self_hosted WHEN 1 THEN 'yes' ELSE 'no' END, r.confidence, "
            "coalesce(r.identity_kind, '?') || CASE WHEN coalesce(r.identity_basis, 'stated') <> 'stated' THEN '?' ELSE '' END, "
            "CASE r.needs_card WHEN 1 THEN 'yes' WHEN 0 THEN 'no' ELSE '?' END, "
            "CASE r.needs_phone WHEN 1 THEN 'yes' WHEN 0 THEN 'no' ELSE '?' END, "
            "r.usd_month, r.usd_per_tb_month, r.stale_on, r.summary")
WIDTH = {"summary": 120, "proved": 160, "before": 240, "value": 240, "url": 120, "what": 160, "title": 120}


class Fail(Exception):
    """A refusal or a defect: printed as 'fr: message' with its exit code."""

    def __init__(self, msg, code=1):
        Exception.__init__(self, msg)
        self.code = code


def utc_now():
    return dt.datetime.now(dt.timezone.utc)


def utc_stamp_ms():
    n = utc_now()
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (n.microsecond // 1000)


def today():
    return utc_now().date()


# ====================================================================== output

def fmt_num(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        return ("%.4f" % v).rstrip("0").rstrip(".")
    return str(v)


def cell(v, width):
    if v is None:
        return ""
    if isinstance(v, (bytes, bytearray)):
        s = "<%d bytes>" % len(v)
    elif isinstance(v, (int, float)):
        s = fmt_num(v)
    elif isinstance(v, (dict, list)):
        s = json.dumps(v, ensure_ascii=False)
    else:
        s = str(v)
    s = s.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    if width and len(s) > width:
        s = s[:max(1, width - 3)] + "..."
    return s


class Table:
    def __init__(self, columns, rows, total=None, offset=0, notes=None, widths=None, title=None, more=False):
        self.more = more  # more rows exist but were not counted (sql)
        self.columns = list(columns)
        self.rows = [list(r) for r in rows]
        self.total = len(self.rows) + offset if total is None else total
        self.offset = offset
        self.notes = list(notes or [])
        self.widths = widths or {}
        self.title = title

    @property
    def truncated(self):
        return self.more or self.offset + len(self.rows) < self.total

    def footer(self):
        n = len(self.rows)
        if self.more:
            line = "# %d rows; more exist" % n
        elif self.truncated:
            line = "# %d of %d rows; offset=%d for more" % (n, self.total, self.offset + n)
        elif self.offset:
            line = "# %d of %d rows (offset %d)" % (n, self.total, self.offset)
        else:
            line = "# %d of %d rows" % (n, self.total)
        if self.title:
            line += "; " + self.title
        return [line] + ["# " + x for x in self.notes]

    def tsv(self, width=80):
        out = ["\t".join(self.columns)]
        ws = [self.widths.get(c, WIDTH.get(c, width)) if width else 0 for c in self.columns]
        for r in self.rows:
            out.append("\t".join(cell(v, w) for v, w in zip(r, ws)))
        return "\n".join(out + self.footer()) + "\n"

    def obj(self):
        rows = []
        for r in self.rows:
            rows.append([(cell(v, WIDTH["summary"]) if c == "summary" and isinstance(v, str) else v)
                         for c, v in zip(self.columns, r)])
        o = {"columns": self.columns, "rows": rows, "truncated": self.truncated,
             "total": None if self.more else self.total,
             "notes": self.notes}
        if self.title:
            o["title"] = self.title
        return o


class Text:
    def __init__(self, text, data=None):
        self.text = text
        self.data = data if data is not None else {"text": text}

    def tsv(self, width=80):
        return self.text if self.text.endswith("\n") else self.text + "\n"

    def obj(self):
        return self.data


class Multi:
    """Several tables in one answer (get --detail full, history); each keeps its own footer."""

    def __init__(self, parts, data):
        self.parts = parts
        self.data = data

    def tsv(self, width=80):
        return "\n".join(p.tsv(width) for p in self.parts)

    def obj(self):
        return self.data


def render(out, as_json, width):
    if as_json:
        return json.dumps(out.obj(), ensure_ascii=False, default=str) + "\n"
    return out.tsv(width)


# ====================================================================== store

def _rq():
    """The research harness's common module: FileLock, the git allowlist, the research-checkout marker."""
    d = os.path.join(DEFAULT_REPO, "scripts", "research")
    if d not in sys.path:
        sys.path.insert(0, d)
    import common
    return common


STORE_RE = re.compile(r"^local-([0-9a-f]{12}|nogit)-s([0-9a-z.]+?)(?:-(\d{8}T\d{6}(?:\d{6})?Z))?\.db$")


def store_format():
    """F of the store file name: build.STORE_FORMAT and the schema version, read from build.py's text (cheaper than
    importing it). A change of the store's tables raises one of them, so an old file is never read as the new format."""
    try:
        with open(os.path.join(HERE, "build.py"), encoding="utf-8") as f:
            t = f.read()
    except OSError:
        return "0"
    a = re.search(r"^STORE_FORMAT\s*=\s*(\d+)", t, re.M)
    b = re.search(r"^SCHEMA_VERSION\s*=\s*\"?(\w+)\"?", t, re.M)
    return "%s.%s" % (a.group(1) if a else "0", b.group(1) if b else "0")


# One answer per command line: main() turns it on, so one `scripts/fr get|search|entity` starts one git process for
# HEAD and one for the marker, not one per call (LIO7-03). A library caller (the harness in one process, the tests)
# keeps no memo, because HEAD can move between its calls.
_MEMO = None


def _memo(key, fn):
    if _MEMO is None:
        return fn()
    if key not in _MEMO:
        _MEMO[key] = fn()
    return _MEMO[key]


def head12(repo):
    def get():
        try:
            r = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return "nogit"
        h = r.stdout.strip()
        return h[:12] if r.returncode == 0 and re.match(r"^[0-9a-f]{40,64}$", h) else "nogit"
    return _memo(("head", os.path.abspath(repo)), get)


def research_checkout(repo):
    def get():
        try:
            r = subprocess.run(["git", "-C", repo, "config", "--get", "rq.researchCheckout"], capture_output=True,
                               text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return False
        return r.stdout.strip().lower() == "true"
    return _memo(("marker", os.path.abspath(repo)), get)


def store_dir(repo):
    return os.path.join(repo, ".tmp", "fshy")


def store_files(repo, head=None):
    """The complete store files of this commit and format, newest first."""
    head = head or head12(repo)
    fmt = store_format()
    out = []
    d = store_dir(repo)
    for n in os.listdir(d) if os.path.isdir(d) else []:
        m = STORE_RE.match(n)
        if m and m.group(1) == head and m.group(2) == fmt:
            p = os.path.join(d, n)
            try:
                out.append((os.stat(p).st_mtime, n, p))
            except OSError:
                pass
    return [p for _, _, p in sorted(out, reverse=True)]


def store_file(repo):
    """The store of HEAD that readers use, or None when it is missing."""
    got = store_files(repo)
    return got[0] if got else None


def store_path(repo, db=None):
    """--db when given; else the store of HEAD (the name a build writes when there is none yet)."""
    if db:
        return os.path.abspath(db)
    return store_file(repo) or os.path.join(store_dir(repo), "local-%s-s%s.db" % (head12(repo), store_format()))


_STORES = []


def close_stores():
    while _STORES:
        try:
            _STORES.pop().close()
        except Exception:
            pass


def ensure_store(repo, force=False, quiet=True):
    """The path of the store of HEAD, built once for the machine when it is missing (or, outside the research checkout,
    older than an input). The build runs under .tmp/fshy/build.lock, which waits with no deadline; after it has the
    lock, a process checks again and uses the store another process built. A build writes a new file and renames it to
    a name no reader has open: a store is never replaced. A wipe in progress refuses the build."""
    rc = research_checkout(repo)
    cur = store_file(repo)
    if cur and not force and (rc or not store_age(repo, cur)):
        return cur
    c = _rq()

    def told(holder):
        sys.stderr.write("fr: waiting for the store build of %s\n" % (holder or "another process"))
    with c.FileLock(os.path.join(store_dir(repo), "build.lock"), wait=True, what="the store build", on_wait=told):
        cur = store_file(repo)
        if cur and not force and (rc or not store_age(repo, cur)):
            return cur
        sp = os.path.join(repo, ".tmp", "rq", "state.db")
        if os.path.exists(sp):
            import state as rqstate
            w = rqstate.control(repo, "wiping")
            rqstate.close_all()
            if w:
                raise Fail("a merge session is wiping .tmp/ (pid %s since %s); run the command again after it" % (w[0], w[1]), 1)
        head, fmt = head12(repo), store_format()
        name = os.path.join(store_dir(repo), "local-%s-s%s.db" % (head, fmt))
        if os.path.exists(name) or not rc:
            # microseconds: two builds in one second (a fast build, then a write) never share a name, so a store is
            # never replaced
            name = os.path.join(store_dir(repo), "local-%s-s%s-%s.db" % (head, fmt, utc_now().strftime("%Y%m%dT%H%M%S%fZ")))
        if not quiet:
            sys.stderr.write("fr: building %s once for this commit; about two minutes\n" % os.path.relpath(name, repo))
        counts, secs = rebuild(repo, name)
        with open(os.path.join(store_dir(repo), "builds.log"), "a", encoding="utf-8", newline="\n") as f:
            f.write("%s\t%s\t%.1f\t%s\n" % (utc_now().strftime("%Y-%m-%dT%H:%M:%SZ"), head, secs, os.path.basename(name)))
        # the older files of this clone go when nothing holds them; a delete of an open file fails on Windows and is
        # left for the next build (rq sync deletes the stores of other commits in the research checkout)
        for p in store_files(repo, head)[1:] + ([] if rc else _other_stores(repo, head)):
            try:
                os.remove(p)
            except OSError:
                pass
        return name


def _other_stores(repo, head):
    d = store_dir(repo)
    out = []
    for n in os.listdir(d) if os.path.isdir(d) else []:
        m = STORE_RE.match(n)
        if m and m.group(1) != head:
            out.append(os.path.join(d, n))
    return out


def prune_stores(repo):
    """rq sync: delete the store files of other commits that nothing holds. -> how many went."""
    n = 0
    for p in _other_stores(repo, head12(repo)):
        try:
            os.remove(p)
            n += 1
        except OSError:
            pass
    return n


def newest_input(repo):
    """(mtime, path) of the newest file the local build reads."""
    best = [0.0, None]

    def see(p, st=None):
        try:
            m = (st or os.stat(p)).st_mtime
        except OSError:
            return
        if m > best[0]:
            best[0], best[1] = m, p

    def walk(d, keep):
        try:
            it = list(os.scandir(d))
        except OSError:
            return
        for e in it:
            if e.is_dir(follow_symlinks=False):
                if e.name not in ("__pycache__",):
                    walk(e.path, keep)
            elif keep(e.name, e.path):
                see(e.path, e.stat())

    walk(os.path.join(repo, "dossier"), lambda n, p: n.endswith(".json"))
    walk(os.path.join(repo, "history"), lambda n, p: n.endswith(".md") or n.endswith(".jsonl"))
    walk(os.path.join(repo, "registry"), lambda n, p: n.endswith(".tsv"))
    walk(HERE, lambda n, p: n not in NOT_BUILD_INPUTS and not n.endswith(".pyc"))
    for p in (("scripts", "dossier", "staleness.py"), ("scripts", "dossier", "staleness.policy.json"),
              ("sources", "MANIFEST.tsv")):
        see(os.path.join(repo, *p))
    return best[0], best[1]


def store_age(repo, db_path):
    """None when current, else the reason it must be rebuilt."""
    if not os.path.exists(db_path):
        return "no store yet"
    m, p = newest_input(repo)
    if m > os.stat(db_path).st_mtime:
        return "%s is newer" % os.path.relpath(p, repo).replace("\\", "/")
    try:
        db = sqlite3.connect("file:%s?mode=ro" % pathname2url(db_path), uri=True)
        ok = db.execute("SELECT 1 FROM sqlite_master WHERE name='raw'").fetchone()
        cols = {r[1] for r in db.execute("SELECT * FROM pragma_table_info('record')")}
        db.close()
    except sqlite3.Error as e:
        return "the store does not open (%s)" % e
    if not ok or "rno" not in cols or "self_hosted" not in cols:
        return "the store has an older schema"
    return None


def rebuild(repo, db_path):
    import build  # noqa: E402  (imported late: only a rebuild needs it)
    tmp = "%s.build-%d" % (db_path, os.getpid())
    t0 = time.time()
    devnull = open(os.devnull, "w")
    old = sys.stdout
    sys.stdout = devnull  # build() prints nothing today; keep stdout clean for MCP if that changes
    try:
        counts, _ = build.build(repo, tmp, "local")
    finally:
        sys.stdout = old
        devnull.close()
    for i in range(20):
        try:
            os.replace(tmp, db_path)
            break
        except PermissionError:
            if i == 19:
                raise Fail("rebuilt store left at %s: %s is open in another process" % (tmp, db_path))
            time.sleep(0.25)  # wait: lock, an explicit --db store that another process holds open
    return counts, time.time() - t0


def ensure_fresh(repo, db_path, quiet=False, force=False):
    why = "forced" if force else store_age(repo, db_path)
    if not why:
        return None
    if not quiet:
        sys.stderr.write("fr: rebuilding %s (%s); about 20 s\n" % (os.path.relpath(db_path, repo), why))
    counts, secs = rebuild(repo, db_path)
    if not quiet:
        sys.stderr.write("fr: rebuilt in %.1f s: %d records, %d entities\n"
                         % (secs, counts["records"], counts["entities"]))
    return why, counts, secs


class Store:
    def __init__(self, path, repo):
        if not os.path.exists(path):
            raise Fail("no store at %s; run fr verify" % path, 2)
        self.path, self.repo = path, repo
        self.db = sqlite3.connect("file:%s?mode=ro" % pathname2url(path), uri=True)
        self.db.execute("PRAGMA query_only=ON")
        self.db.create_function("fr_bm25", 1, bm25, deterministic=True)
        self.db.create_function("fr_matched", 1, matched_cols, deterministic=True)
        self.tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        self._names = None
        self._self_hosted = None

    def close(self):
        self.db.close()

    def q(self, sql, args=()):
        return self.db.execute(sql, args).fetchall()

    def one(self, sql, args=()):
        r = self.db.execute(sql, args).fetchone()
        return r[0] if r else None

    def has(self, t):
        return t in self.tables

    def need_local(self, t):
        if not self.has(t):
            raise Fail("table %s exists only in the local store (.tmp/fshy/local-HEAD-sF.db)" % t, 2)

    def meta(self):
        return dict(self.q("SELECT key, value FROM meta"))

    def cards(self, rids):
        """{rid: card row} for the given rids."""
        out = {}
        rids = list(rids)
        for i in range(0, len(rids), 500):
            part = rids[i:i + 500]
            for r in self.q("SELECT %s FROM record r WHERE r.rid IN (%s)" % (CARD_SQL, ",".join("?" * len(part))),
                            part):
                out[r[0]] = list(r)
        return out

    def rid_exists(self, rid):
        return self.one("SELECT 1 FROM record WHERE rid=?", (rid,)) is not None

    def self_hosted(self):
        """(rids with self_hosted = 1, eids whose every record has self_hosted = 1)."""
        if self._self_hosted is None:
            self._self_hosted = ({r for (r,) in self.q("SELECT rid FROM record WHERE self_hosted = 1")},
                                 {e for (e,) in self.q("SELECT eid FROM record GROUP BY eid HAVING min(self_hosted) = 1")})
        return self._self_hosted


# ====================================================================== ranking

def _mi(blob):
    return struct.unpack("@%dI" % (len(blob) // 4), blob)


def bm25(blob, weights=None):
    """Okapi BM25 over matchinfo(text_fts, 'pcnalx') with the contract's column weights.

    score = sum over phrase i, column j of
      w_j * idf_ij * tf_ij * (k1 + 1) / (tf_ij + k1 * (1 - b + b * len_j / avglen_j))
    idf_ij = ln(1 + (N - df_ij + 0.5) / (df_ij + 0.5)); df_ij = rows with a hit in column j.
    Higher is better. The twin of site/worker/rank.js bm25(); weights replaces the contract's column weights."""
    if blob is None:
        return None
    weights = FTS_WEIGHTS if weights is None else weights
    mi = _mi(blob)
    p, c, n = mi[0], mi[1], mi[2]
    a = mi[3:3 + c]
    ln = mi[3 + c:3 + 2 * c]
    x = 3 + 2 * c
    score = 0.0
    for i in range(p):
        for j in range(c):
            w = weights[j] if j < len(weights) else 1.0
            base = x + 3 * (i * c + j)
            tf = mi[base]
            if not tf or not w:
                continue
            df = mi[base + 2]
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            ratio = ln[j] / (a[j] or 1)
            score += w * idf * (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * ratio))
    return score


def matched_cols(blob):
    if blob is None:
        return None
    mi = _mi(blob)
    p, c = mi[0], mi[1]
    x = 3 + 2 * c
    hit = [j for j in range(c) if any(mi[x + 3 * (i * c + j)] for i in range(p))]
    return ",".join(FTS_COLUMNS[j] if j < len(FTS_COLUMNS) else str(j) for j in hit)


def fts_query(q):
    """The MATCH string, the twin of site/worker/text.js ftsMatch(): words of the normalised query
    AND-ed; a CJK run longer than one character becomes its bigrams; a word with punctuation is a
    quoted phrase; a plain word of 3+ characters is a prefix term. A term that repeats is kept once (its AND
    with itself matches the same rows, and each copy would cost one more pass over the index)."""
    def cjk(m):
        t = m.group(0)
        return (" " + " ".join(t[i:i + 2] for i in range(len(t) - 1)) + " ") if len(t) > 1 else t
    terms = []
    for w in CJK.sub(cjk, norm(q)).split():
        w = w.replace('"', "")
        if not re.search(r"[^\W_]", w):
            continue
        t = '"%s"' % w if re.search(r"[\W_]", w) else (w + "*" if len(w) >= 3 else w)
        if t not in terms:
            terms.append(t)
    return " ".join(terms)


def norm(s):
    """Name normaliser, the twin of site/worker/text.js normalize()."""
    if s is None:
        return ""
    s = str(s)
    if re.fullmatch(r"[ -~]*", s):
        return re.sub(r" +", " ", s.lower()).strip()
    t = unicodedata.normalize("NFKC", s).casefold()
    t = "".join(ch for ch in unicodedata.normalize("NFD", t) if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t)).strip()


def tokens(s):
    """Letter and digit runs (site/worker/text.js tokens)."""
    return re.findall(r"[^\W_]+", s)


def lev(a, b, cap):
    """Levenshtein distance, or cap + 1 once it is known to exceed cap (site/worker/rank.js editDistance)."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def fuzz_budget(t):
    n = len(t)
    return 2 if n >= 8 else (1 if n >= 4 else 0)


# The fuzzy tier runs for a query of at most this many distinct words (site/worker/rank.js MAX_FUZZY_TOKENS): each
# word is compared with every word of the index, so a long query would cost one full pass for each word.
MAX_FUZZY_TOKENS = 8


HOW = {100: "exact", 60: "prefix", 40: "substring", 30: "fuzzy"}


def hosted_first(items, is_self_hosted):
    """Every hosted item, then every self-hosted one; each part keeps the order it had (a stable partition).
    The one ordering rule over every list of records: self_hosted ascending is the first sort key."""
    return [x for x in items if not is_self_hosted(x)] + [x for x in items if is_self_hosted(x)]


def sort_entities(hits, best_vorder, all_self_hosted):
    """The entities of a name search, best first: the twin of site/worker/rank.js sortEntities(). hits: [(eid, score)].
    Score, then best verdict (best_vorder(eid), lower is better), then eid; then every entity whose every record is
    self-hosted (all_self_hosted(eid)) after every other entity. entity.best_vorder is the best verdict of the
    entity's hosted records, or of all its records when every one is self-hosted."""
    ranked = sorted(hits, key=lambda h: (-h[1], best_vorder(h[0]), h[0]))
    return hosted_first(ranked, lambda h: all_self_hosted(h[0]))


def resolve_entity(ranked):
    """The one entity a name lookup (fr entity NAME) resolves to: the twin of site/worker/rank.js resolveEntity().
    ranked: [(eid, score, ...)] in sort_entities() order. The best score wins, so an exact name is never beaten by
    a fuzzy or substring match; among entities with that score the first in list order wins, which puts a hosted
    entity before a wholly self-hosted one, then the better verdict, then the eid. None when nothing matched. The
    list of other matches keeps sort_entities() order."""
    if not ranked:
        return None
    top = max(h[1] for h in ranked)
    return next(h for h in ranked if h[1] == top)


def best_vorder(members):
    """The verdict that ranks an entity: the best (lowest) vorder of its hosted records, or of all its records when
    every one is self-hosted; None when it has none. members: [(vorder, self_hosted)]. The twin of
    site/worker/rank.js bestVorder(); entity.best_vorder holds the same value (build.py)."""
    hosted = [v for v, sh in members if not sh]
    every = [v for v, _ in members]
    return min(hosted) if hosted else (min(every) if every else None)


def name_scores(st, q):
    """[(eid, score, how)] best first: the twin of site/worker/rank.js scoreNames() plus sortEntities().
    An entity scores its best alias: exact 100, prefix 60, substring 40, else 30 when every query
    word meets a word of that same alias within its budget (1 edit for 4-7 characters, 2 for 8 or
    more, an exact word under 4). Each distinct query word counts once, and a query of more than 8 distinct
    words gets no fuzzy tier. The order is sort_entities()."""
    if st._names is None:
        st._names = name_index(st.q("SELECT eid, alias FROM alias"))
    best = score_names(st._names, q)
    if not best:
        return []
    bv = dict(st.q("SELECT eid, best_vorder FROM entity"))
    sh = st.self_hosted()[1]
    ranked = sort_entities(list(best.items()), lambda e: bv.get(e, 99), lambda e: e in sh)
    return [(e, sc, HOW[sc]) for e, sc in ranked]


def name_index(rows):
    """(eid, alias) rows -> the index score_names reads (site/worker/rank.js buildNameIndex)."""
    by = collections.OrderedDict()
    for eid, a in rows:
        k = norm(a)
        if k:
            by.setdefault(k, set()).add(eid)
    aliases = list(by)
    eids = [sorted(by[k]) for k in aliases]
    tokmap = collections.defaultdict(list)
    for idx, k in enumerate(aliases):
        for t in tokens(k):
            if not tokmap[t] or tokmap[t][-1] != idx:
                tokmap[t].append(idx)
    return aliases, eids, tokmap


def score_names(index, q):
    """{eid: best score} of one query (site/worker/rank.js scoreNames)."""
    aliases, eids, tokmap = index
    nq = norm(q)
    if not nq:
        return {}
    best = {}

    def put(idx, sc):
        for e in eids[idx]:
            if best.get(e, 0) < sc:
                best[e] = sc
    for idx, k in enumerate(aliases):
        if k == nq:
            put(idx, 100)
        elif k.startswith(nq):
            put(idx, 60)
        elif nq in k:
            put(idx, 40)
    hits = None
    qts = list(dict.fromkeys(tokens(nq)))
    for qt in qts if len(qts) <= MAX_FUZZY_TOKENS else ():
        cap = fuzz_budget(qt)
        found = set()
        if not cap:
            found.update(tokmap.get(qt, ()))
        else:
            for t, idxs in tokmap.items():
                if lev(qt, t, cap) <= cap:
                    found.update(idxs)
        hits = found if hits is None else (hits & found)
        if not hits:
            break
    for idx in hits or ():
        put(idx, 30)
    return best


def own_score(q, names):
    """The best score of a few names against a query by the rules of score_names; 0 when none matches."""
    return max(score_names(name_index([("-", n) for n in names if n]), q).values(), default=0)


def name_hit_records(st, q, eid, score, recs):
    """The rids that a name hit of an entity lifts to the top of a search (the twin of nameHitRecords of
    site/worker/api.js). When the vendor's own name or domain scores as well as the alias that matched, every record of
    the vendor; else the records whose own name (provider or slug) scores that well, so one record's name does not lift
    every other record of its vendor; a hit through an alias that no record's name carries keeps every record.
    recs: [(rid, provider, slug)] in list order."""
    ent = st.q("SELECT name, domain FROM entity WHERE eid = ?", [eid])
    if not ent or own_score(q, list(ent[0])) >= score:
        return [r[0] for r in recs]
    mine = [r for r in recs if own_score(q, [r[1], r[2]]) >= score]
    return [r[0] for r in (mine or recs)]


# ====================================================================== read operations

def _filters(topic=None, grp=None, include_duplicates=False, alias="r"):
    w, a = [], []
    ts = _list(topic)
    if ts:
        w.append("%s.topic IN (%s)" % (alias, ",".join("?" * len(ts))))
        a.extend(ts)
    if grp:
        gs = _list(grp)
        w.append("%s.grp IN (%s)" % (alias, ",".join("?" * len(gs))))
        a.extend(gs)
    if not include_duplicates:
        w.append("%s.duplicate_of IS NULL" % alias)
    return w, a


def _list(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            out.extend(_list(x))
        return out
    return [x.strip() for x in str(v).split(",") if x.strip()]


def _clamp(n, default, hi):
    try:
        n = int(default if n is None else n)
    except (TypeError, ValueError):
        raise Fail("limit must be an integer", 2)
    return max(1, min(n, hi))


def op_search(st, q, topic=None, grp=None, limit=20, offset=0, include_duplicates=False):
    q = " ".join(q) if isinstance(q, (list, tuple)) else (q or "")
    if not q.strip():
        raise Fail("search needs words", 2)
    limit, offset = _clamp(limit, 20, 50), max(0, int(offset or 0))
    w, a = _filters(topic, grp, include_duplicates)
    where = (" AND " + " AND ".join(w)) if w else ""
    notes = []
    # 1. names
    order, seen = [], set()
    if RID_RE.match(q.strip()) and st.rid_exists(q.strip()):
        order.append(q.strip())
        seen.add(q.strip())
    ents = name_scores(st, q)
    how = {}
    for eid, sc, hw in ents:
        recs = st.q("SELECT r.rid, r.provider, r.slug FROM record r WHERE r.eid = ?%s ORDER BY r.vorder, r.rid" % where,
                    [eid] + a)
        for rid in name_hit_records(st, q, eid, sc, recs):
            if rid not in seen:
                seen.add(rid)
                order.append(rid)
                how[rid] = hw
    n_name = len(order)
    # 2. full text
    mq = fts_query(q)
    fts = {}
    if mq:
        try:
            rows = st.q("SELECT r.rid, fr_bm25(matchinfo(text_fts, 'pcnalx')), fr_matched(matchinfo(text_fts, 'pcnalx')),"
                        " r.vorder"
                        " FROM text_fts JOIN record r ON r.rno = text_fts.docid WHERE text_fts MATCH ?%s" % where,
                        [mq] + a)
        except sqlite3.OperationalError as e:
            rows = []
            notes.append("full text skipped: %s (MATCH %s)" % (e, mq))
        rows.sort(key=lambda r: (-r[1], r[3], r[0]))
        for rid, sc, mc, _ in rows:
            fts[rid] = mc
            if rid not in seen:
                seen.add(rid)
                order.append(rid)
    # 3. hosted first; inside each part, name hits and then text hits, as ranked above
    sh = st.self_hosted()[0]
    order = hosted_first(order, lambda r: r in sh)
    n_sh = sum(1 for r in order if r in sh)
    total = len(order)
    page = order[offset:offset + limit]
    cards = st.cards(page)
    out = []
    for rid in page:
        m = fts.get(rid)
        cols = (["name(%s)" % how[rid]] if rid in how else []) + (m.split(",") if m else [])
        mc = ",".join(cols)
        out.append(cards[rid] + [mc])
    notes.append("name hits: %d records; text hits: %d more; MATCH %s"
                 % (n_name, total - n_name, mq or "(none)"))
    if n_sh:
        notes.append("self-hosted: %d records, listed after every hosted record" % n_sh)
    if not include_duplicates:
        notes.append("duplicates excluded; --include-duplicates brings them back")
    return Table(CARD_COLS + ["matched"], out, total, offset, notes)


def op_filter(st, topic=None, verdict=None, grp=None, confidence=None, no_card=False, no_phone=False,
              anonymous=False, iface=None, binding=None, crypto=False, max_usd_month=None, max_usd_tb=None,
              include_duplicates=False, sort="vorder", order="asc", limit=20, offset=0, keep_null=False):
    limit, offset = _clamp(limit, 20, 200), max(0, int(offset or 0))
    sort = sort or "vorder"
    if sort not in SORTS:
        raise Fail("sort must be one of %s" % ", ".join(SORTS), 2)
    order = (order or "asc").lower()
    if order not in ("asc", "desc"):
        raise Fail("order must be asc or desc", 2)
    w, a = _filters(topic, grp, include_duplicates)
    for col, vals, vocab in (("verdict", _list(verdict), VERDICTS), ("confidence", _list(confidence), LADDER),
                             ("binding", _list(binding), None)):
        if vals:
            if vocab:
                bad = [v for v in vals if v not in vocab]
                if bad:
                    raise Fail("%s %s is not one of %s" % (col, ",".join(bad), ", ".join(vocab)), 2)
            w.append("r.%s IN (%s)" % (col, ",".join("?" * len(vals))))
            a.extend(vals)
    if no_card:
        w.append("r.needs_card = 0 AND r.identity_basis = 'stated'")
    if no_phone:
        w.append("r.needs_phone = 0 AND r.identity_basis = 'stated'")
    if anonymous:
        w.append("r.identity_kind = 'anonymous' AND r.identity_basis = 'stated'")
    if iface:
        w.append("r.interfaces LIKE ?")
        a.append("%" + iface + "%")
    if crypto:
        w.append("r.crypto = 1")
    notes = []
    base_w, base_a = list(w), list(a)
    nullable = []
    for col, mx in (("usd_month", max_usd_month), ("usd_per_tb_month", max_usd_tb)):
        if mx is not None:
            w.append("r.%s <= ?" % col)
            a.append(float(mx))
            nullable.append(col)
    if sort in ("usd_month", "usd_per_tb_month") and sort not in nullable and not keep_null:
        w.append("r.%s IS NOT NULL" % sort)
        nullable.append(sort)
    for col in nullable:
        cw = base_w + ["r.%s IS NULL" % col]
        n = st.one("SELECT count(*) FROM record r WHERE " + " AND ".join(cw), base_a) if cw else 0
        notes.append("excluded for NULL %s: %d%s" % (col, n, "" if keep_null or col != sort else
                                                       " (--keep-null lists them last)"))
    where = (" WHERE " + " AND ".join(w)) if w else ""
    total = st.one("SELECT count(*) FROM record r" + where, a)
    nulls = "r.%s IS NULL, " % sort if sort in ("usd_month", "usd_per_tb_month", "stale_on", "verified_at") else ""
    rows = st.q("SELECT %s FROM record r%s ORDER BY r.self_hosted, %sr.%s %s, r.vorder, r.rid LIMIT ? OFFSET ?"
                % (CARD_SQL, where, nulls, sort, order), a + [limit, offset])
    n_sh = st.one("SELECT count(*) FROM record r%s%s r.self_hosted = 1" % (where, " AND" if where else " WHERE"), a)
    if n_sh:
        notes.append("self-hosted: %d records, listed after every hosted record" % n_sh)
    if not include_duplicates:
        notes.append("duplicates excluded")
    return Table(CARD_COLS, rows, total, offset, notes)


def _record_cols(st):
    return [r[1] for r in st.q("SELECT * FROM pragma_table_info('record')")]


def _leaves(v, p=()):
    if isinstance(v, dict) and v:
        for k, x in v.items():
            yield from _leaves(x, p + (k,))
    elif isinstance(v, list) and v:
        for i, x in enumerate(v):
            yield from _leaves(x, p + (i,))
    else:
        yield p, v


def jpath(p):
    out = "$"
    for k in p:
        if isinstance(k, int):
            out += "[%d]" % k
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k):
            out += "." + k
        else:
            out += '."' + k.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return out


def op_get(st, ids, detail="card", fields=None, raw=False):
    ids = _list(ids)
    if not ids:
        raise Fail("get needs at least one rid", 2)
    detail = detail or "card"
    if detail not in ("card", "full"):
        raise Fail("detail must be card or full", 2)
    cap = 5 if (detail == "full" or raw) else 50
    if len(ids) > cap:
        raise Fail("at most %d rids with %s" % (cap, "--raw" if raw else "--detail " + detail), 2)
    missing = [r for r in ids if not st.rid_exists(r)]
    if raw:
        st.need_local("raw")
        parts, data = [], {}
        for rid in ids:
            row = st.q("SELECT path, doc FROM raw WHERE rid=?", (rid,))
            if not row:
                if rid not in missing:
                    missing.append(rid)
                continue
            parts.append("# %s  %s (verbatim source)\n%s" % (rid, row[0][0], row[0][1]))
            data[rid] = json.loads(row[0][1])
        if missing:
            parts.append("# not found: %s" % ", ".join(missing))
        return Text("\n".join(parts), data)
    flds = _list(fields)
    if detail == "card":
        if flds:
            allowed = [c for c in _record_cols(st) if c not in ("rno", "doc")]
            bad = [f for f in flds if f not in allowed and f not in CARD_COLS]
            if bad:
                raise Fail("unknown field %s; fields are record columns: %s" % (",".join(bad), ", ".join(allowed)), 2)
            cards = {r[0]: list(r[1:]) for r in st.q(
                "SELECT r.rid, %s FROM record r WHERE r.rid IN (%s)" % (_card_select(flds, allowed),
                                                                         ",".join("?" * len(ids))), ids)}
            cols = flds
        else:
            cards = st.cards(ids)
            cols = CARD_COLS
        rows = [cards[r] for r in ids if r in cards]
        notes = ["not found: %s" % ", ".join(missing)] if missing else []
        return Table(cols, rows, notes=notes)
    parts, data = [], []
    for rid in ids:
        if rid in missing:
            continue
        rec = st.q("SELECT * FROM record WHERE rid=?", (rid,))[0]
        rc = dict(zip(_record_cols(st), rec))
        doc = json.loads(rc.pop("doc") or "null")
        rc.pop("rno", None)
        lv = [(jpath(p), v) for p, v in _leaves(doc)]
        if flds:
            pre = tuple(("$." + f) if not f.startswith("$") else f for f in flds)
            lv = [(p, v) for p, v in lv if p.startswith(pre)]
        claims = st.q("SELECT path, kind, num, unit, per, currency, usd, fx_date, parse FROM claim WHERE rid=? ORDER BY path",
                      (rid,))
        unknown = st.q("SELECT path, class, rule FROM unknown WHERE rid=? ORDER BY path", (rid,)) if st.has("unknown") else []
        hist = st.q("SELECT h.hid, h.when_utc, h.status, h.title FROM history_link l JOIN history h USING (hid)"
                    " WHERE l.rid=? ORDER BY h.when_utc DESC", (rid,))
        drift = st.q("SELECT kind, subject, other, field, a, b FROM drift WHERE subject=? OR other=?", (rid, rid))
        nstrip = st.one("SELECT count(*) FROM strip_log WHERE rid=?", (rid,)) if st.has("strip_log") else None
        notes = ["%s: verdict %s, %s, eid %s, %s" % (rid, rc["verdict"], rc["confidence"], rc["eid"], rc["path"])]
        if nstrip is not None:
            notes.append("projected view; the public projection changed %d values: fr get %s --raw for the source"
                         % (nstrip, rid))
        parts.append(Table(["path", "value"], [[p, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v]
                                               for p, v in lv], notes=notes))
        if claims:
            parts.append(Table(["path", "kind", "num", "unit", "per", "currency", "usd", "fx_date", "parse"], claims,
                               title="claims of " + rid))
        if unknown:
            parts.append(Table(["path", "class", "rule"], unknown, title="unknown values of " + rid))
        if hist:
            parts.append(Table(["hid", "when", "status", "title"], hist, title="history of " + rid))
        if drift:
            parts.append(Table(["kind", "subject", "other", "field", "a", "b"], drift, title="drift of " + rid))
        data.append({"rid": rid, "card": rc, "record": doc,
                     "claims": [dict(zip(["path", "kind", "num", "unit", "per", "currency", "usd", "fx_date", "parse"], c))
                                for c in claims],
                     "unknown": [list(u[:2]) for u in unknown],
                     "history": [dict(zip(["hid", "when", "status", "title"], h)) for h in hist],
                     "drift": [dict(zip(["kind", "subject", "other", "field", "a", "b"], d)) for d in drift]})
    if missing:
        parts.append(Text("# not found: %s\n" % ", ".join(missing)))
    return Multi(parts, {"records": data, "missing": missing})


def _card_select(flds, allowed):
    derived = {
        "identity": "coalesce(r.identity_kind, '?') || CASE WHEN coalesce(r.identity_basis, 'stated') <> 'stated' THEN '?' ELSE '' END",
        "card": "CASE r.needs_card WHEN 1 THEN 'yes' WHEN 0 THEN 'no' ELSE '?' END",
        "phone": "CASE r.needs_phone WHEN 1 THEN 'yes' WHEN 0 THEN 'no' ELSE '?' END",
    }
    return ", ".join(("r." + f) if f in allowed else derived[f] for f in flds)


def op_entity(st, id, limit=50, offset=0):
    q = " ".join(id) if isinstance(id, (list, tuple)) else (id or "")
    q = q.strip()
    if not q:
        raise Fail("entity needs an id or a name", 2)
    limit, offset = _clamp(limit, 50, 200), max(0, int(offset or 0))
    row = st.q("SELECT eid, name, domain, resolved_by, topics, n_records, best_vorder, review FROM entity WHERE eid=?", (q,))
    others, matched = [], None
    if not row:
        sc = name_scores(st, q)
        hit = resolve_entity(sc)
        if not hit:
            raise Fail("no entity matches %r; try fr search" % q)
        row = st.q("SELECT eid, name, domain, resolved_by, topics, n_records, best_vorder, review FROM entity WHERE eid=?",
                   (hit[0],))
        matched = hit[2]
        others = ["%s (%s)" % (e, hw) for e, _, hw in sc if e != hit[0]][:8]
    eid, name, domain, how, topics, n, bv, review = row[0]
    rids = [r for (r,) in st.q("SELECT rid FROM record WHERE eid=? ORDER BY self_hosted, vorder, rid", (eid,))]
    page = rids[offset:offset + limit]
    cards = st.cards(page)
    dups = dict(st.q("SELECT rid, duplicate_of FROM record WHERE eid=? AND duplicate_of IS NOT NULL", (eid,)))
    aliases = [a for (a,) in st.q("SELECT DISTINCT alias FROM alias WHERE eid=? AND kind IN ('name','provider','alias','domain')"
                                  " ORDER BY length(alias), alias LIMIT 8", (eid,))]
    notes = ["entity %s: %s; domain %s; resolved by %s; topics %s; %d records; best verdict order %s%s"
             % (eid, name, domain or "-", how, topics, n, bv, "; review: " + review if review else ""),
             "aliases: " + "; ".join(aliases)]
    if matched:
        notes.append("resolved by name: %s match" % matched)
    if eid in st.self_hosted()[1]:
        notes.append("self-hosted: every record of this entity is self-hosted, so it is the last resort")
    if dups:
        notes.append("duplicates: " + ", ".join("%s -> %s" % kv for kv in sorted(dups.items())))
    if others:
        notes.append("other name matches: " + ", ".join(others))
    return Table(CARD_COLS, [cards[r] for r in page], len(rids), offset, notes)


def load_needs():
    return json.load(open(os.path.join(HERE, "rules", "needs.json"), encoding="utf-8"))["needs"]


def op_need(st, id=None, limit=20, offset=0):
    needs = load_needs()
    if not id:
        return Table(["id", "topic", "sort", "title"], [[n["id"], n.get("topic"), n.get("sort"), n["title"]] for n in needs],
                     notes=["fr need ID runs one; the SQL is in scripts/fshy/rules/needs.json"])
    n = next((x for x in needs if x["id"] == id), None)
    if not n:
        raise Fail("no need %r; fr need lists them" % id, 2)
    limit, offset = _clamp(limit, 20, 200), max(0, int(offset or 0))
    s = n["sort"]
    rows = need_rows(st, n)
    sh = CARD_COLS.index("self_hosted") + 1
    nulls = sum(1 for r in rows if r[0] is None)
    n_sh = sum(1 for r in rows if r[sh] == "yes")
    allr = [list(r[1:]) + [r[0]] for r in rows]
    cols = CARD_COLS + ([s] if s not in CARD_COLS else ["sort_" + s])
    notes = [n["title"] + ": " + n["scope"]]
    if nulls:
        notes.append("no parsed number (NULL %s): %d rows, listed after the %d ranked rows of their part"
                     % (s, nulls, len(rows) - nulls))
    if n_sh:
        notes.append("self-hosted: %d rows, listed after every hosted row" % n_sh)
    return Table(cols, allr[offset:offset + limit], len(allr), offset, notes)


def need_rows(st, n):
    """Every row of one need, in list order: [sort value] + card. Hosted rows first, then self-hosted rows; in
    each part the rows with a sort value ascending, then the rows with none; ties by verdict, then rid."""
    s = n["sort"]
    return st.q('SELECT n."%s", %s FROM (%s) n JOIN record r ON r.rid = n.rid '
                'ORDER BY r.self_hosted, n."%s" IS NULL, n."%s", r.vorder, r.rid' % (s, CARD_SQL, n["sql"], s, s))


FORBIDDEN = ("INSERT UPDATE DELETE REPLACE UPSERT CREATE DROP ALTER ATTACH DETACH PRAGMA VACUUM REINDEX ANALYZE "
             "BEGIN COMMIT ROLLBACK SAVEPOINT RELEASE TEMP TEMPORARY").split()
# re.ASCII: a word boundary as JavaScript draws it, so "SELECT", a letter outside ASCII and "INSERT" are refused here as in guard.js
FORBID_RE = re.compile(r"\b(%s)\b" % "|".join(FORBIDDEN), re.I | re.ASCII)


MAX_SQL_CHARS = 10000


def strip_sql(sql, keep_idents=False):
    """Blank every string literal, quoted identifier and comment, keeping offsets (newlines stay),
    scanning left to right; the twin of site/worker/guard.js strip(). Refuses an unterminated one.
    With keep_idents, a quoted identifier ("x", `x` or [x]) keeps its name and loses only its quotes."""
    out = list(sql)
    n = len(sql)

    def blank(a, b):
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "
    i = 0
    while i < n:
        c = sql[i]
        d = sql[i + 1] if i + 1 < n else ""
        if c in "'\"`":
            j = i + 1
            while True:
                if j >= n:
                    raise Fail("read-only: unterminated quoted string", 1)
                if sql[j] == c:
                    if j + 1 < n and sql[j + 1] == c:
                        j += 2
                        continue
                    break
                j += 1
            if keep_idents and c != "'":
                out[i] = out[j] = " "
            else:
                blank(i, j + 1)
            i = j + 1
        elif c == "[":
            j = sql.find("]", i + 1)
            if j < 0:
                raise Fail("read-only: unterminated [identifier]", 1)
            if keep_idents:
                out[i] = out[j] = " "
            else:
                blank(i, j + 1)
            i = j + 1
        elif c == "-" and d == "-":
            j = sql.find("\n", i + 2)
            e = n if j < 0 else j
            blank(i, e)
            i = e
        elif c == "/" and d == "*":
            j = sql.find("*/", i + 2)
            if j < 0:
                raise Fail("read-only: unterminated /* comment", 1)
            blank(i, j + 2)
            i = j + 2
        else:
            i += 1
    return "".join(out)


# JavaScript's \s and String.prototype.trim(): the white space of site/worker/guard.js. Python's \s also takes U+0085
# and 0x1C to 0x1F, and JavaScript's takes neither, so the guard spells the JavaScript set out (R3-B-11)
JS_WS = "[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]"


# SQLite's white space is space, tab, LF, VT, FF and CR. These code points are white space to JavaScript (\s) or to
# Python (str.isspace) and not to SQLite; outside a literal they are refused on both sides (guard.js ODD_SPACE_CODES)
ODD_SPACE_CODES = (0x1c, 0x1d, 0x1e, 0x1f, 0x85, 0xa0, 0x1680, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006,
                   0x2007, 0x2008, 0x2009, 0x200a, 0x2028, 0x2029, 0x202f, 0x205f, 0x3000, 0xfeff)
ODD_SPACE = re.compile("[%s]" % "".join(chr(c) for c in ODD_SPACE_CODES))


# The functions a statement may call (site/worker/guard.js ALLOWED_FUNCTIONS, the guard_lists of parity.json): the
# functions that build a value larger than their input (hex, quote, char, the JSON builders), the row generators
# (json_each, json_tree) and the full-text helpers the store cannot serve are left out
ALLOWED_FUNCTIONS = frozenset("""
abs changes coalesce concat concat_ws format glob if ifnull iif instr last_insert_rowid length like likelihood likely
lower ltrim max min nullif octet_length printf random round rtrim sign sqlite_version substr substring total_changes
trim typeof unicode unlikely upper
avg count group_concat string_agg sum total cume_dist dense_rank first_value lag last_value lead nth_value ntile
percent_rank rank row_number
date datetime julianday strftime time timediff unixepoch
acos acosh asin asinh atan atan2 atanh ceil ceiling cos cosh degrees exp floor ln log log10 log2 mod pi pow power
radians sin sinh sqrt tan tanh trunc
json json_array_length json_error_position json_extract json_type json_valid
matchinfo pragma_table_info pragma_table_xinfo pragma_index_list pragma_index_info pragma_index_xinfo
pragma_foreign_key_list
""".split())
# words that can come before "(" and do not call a function (guard.js NOT_FUNCTIONS)
NOT_FUNCTIONS = frozenset("""
all and any as asc between by case cast collate current desc distinct else end escape except exclude exists filter
first following from groups having in intersect is join last limit match materialized not null nulls offset on or
over partition preceding range rows select then unbounded union using values when where window with
""".split())
MAX_WIDTH = 1000
PRINTF_REFUSED = ("q", "Q", "w")


def _after_as(text, i):
    """True when the word AS (not part of a longer name) and white space only come before offset i of text."""
    k = i
    while k > 0 and re.match(JS_WS, text[k - 1]):
        k -= 1
    return k >= 2 and text[k - 2:k].lower() == "as" and not (k >= 3 and re.match(r"[A-Za-z0-9_$]", text[k - 3]))


def check_functions(sql, named):
    """The twin of guard.js checkFunctions(): every name before "(" in named (literals and comments blanked, quoted
    names kept) is a word of NOT_FUNCTIONS, a name after AS, the name of a CTE defined with a column list, or a
    function of ALLOWED_FUNCTIONS. printf() and format() need a literal format string, then "," or ")"; each width
    and precision is at most MAX_WIDTH, with no "*", and no conversion is in PRINTF_REFUSED."""
    ws = JS_WS
    defs = {m.start(1) for m in re.finditer(r"(?:\bwith\b|,){0}*([A-Za-z_][A-Za-z0-9_$]*){0}*\([^()]*\){0}*as{0}*"
                                            r"(?:not{0}+)?(?:materialized{0}*)?\(".format(ws), named, re.I | re.ASCII)}
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_$]*){0}*\(".format(ws), named):
        name = m.group(1).lower()
        if name in NOT_FUNCTIONS or m.start() in defs or _after_as(named, m.start()):
            continue
        if name not in ALLOWED_FUNCTIONS:
            raise Fail("read-only: function not allowed: %s()" % name, 1)
        if name not in ("printf", "format"):
            continue
        at = m.end()
        while at < len(sql) and re.match(ws, sql[at]):
            at += 1
        if at >= len(sql) or sql[at] != "'":
            raise Fail("read-only: %s() needs a literal format string" % name, 1)
        j = at + 1
        while j < len(sql) and not (sql[j] == "'" and (j + 1 >= len(sql) or sql[j + 1] != "'")):
            j += 2 if sql[j] == "'" else 1
        k = j + 1
        while k < len(sql) and re.match(ws, sql[k]):
            k += 1
        if k >= len(sql) or sql[k] not in ",)":
            raise Fail("read-only: %s() needs a literal format string" % name, 1)
        for w in re.finditer(r"%[-+ #0,!]*(\*|[0-9]+)?(?:\.(\*|[0-9]+))?(?:ll?)?(.?)", sql[at + 1:j], re.S):
            for v in (w.group(1), w.group(2)):
                if v == "*" or (v and int(v) > MAX_WIDTH):
                    raise Fail("read-only: %s() width or precision over %d" % (name, MAX_WIDTH), 1)
            if w.group(3) in PRINTF_REFUSED:
                raise Fail("read-only: %s() conversion %%%s is not accepted" % (name, w.group(3)), 1)


def guard_sql(sql, limit):
    """-> (statement to run, LIMIT appended?), or raise Fail. The contract's read-only guard, the twin
    of site/worker/guard.js guard(); pass the row cap plus one to detect truncation."""
    # JavaScript's \s and trim() take U+FEFF (a byte order mark) as white space; Python's do not
    if not isinstance(sql, str) or not re.sub(JS_WS, "", sql):
        raise Fail("empty query", 2)
    if len(sql) > MAX_SQL_CHARS:
        raise Fail("read-only: query longer than %d characters" % MAX_SQL_CHARS, 1)
    if "\0" in sql:
        raise Fail("read-only: NUL byte in query", 1)
    bare = strip_sql(sql)
    # a character that JavaScript or Python takes as white space and SQLite does not: the two guards and SQLite would
    # read different statements, so it is refused outside a literal on both sides (U+FEFF among them)
    odd = ODD_SPACE.search(bare)
    if odd:
        raise Fail("read-only: U+%04X outside a literal: SQLite does not read it as white space" % ord(odd.group(0)), 1)
    m = re.search(";%s*$" % JS_WS, bare)
    semi = m.start() if m else -1
    body = bare[:semi] if semi >= 0 else bare
    if ";" in body:
        raise Fail("read-only: one statement only", 1)
    m = re.match("%s*([A-Za-z]+)" % JS_WS, body)
    if not m or m.group(1).upper() not in ("SELECT", "WITH", "VALUES", "EXPLAIN"):
        raise Fail("read-only: the statement must start with SELECT, WITH, VALUES or EXPLAIN", 1)
    f = FORBID_RE.search(body)
    if f:
        raise Fail("read-only: keyword not allowed: %s" % f.group(1).upper(), 1)
    if re.search(r"\brecursive\b", body, re.I | re.ASCII):
        raise Fail("read-only: a recursive CTE runs as long as the statement says; it is not accepted", 1)
    named = strip_sql(sql, keep_idents=True)
    check_functions(sql, named[:semi] if semi >= 0 else named)
    run = (sql[:semi] + sql[semi + 1:]) if semi >= 0 else sql
    limited = re.search(r"\blimit\b", body, re.I | re.ASCII) is not None
    if not limited:
        run = re.sub("%s+\\Z" % JS_WS, "", run) + "\nLIMIT %d" % int(limit)
    return run, not limited


def op_sql(st, query, limit=50):
    query = " ".join(query) if isinstance(query, (list, tuple)) else (query or "")
    limit = _clamp(limit, 50, 200)
    stmt, appended = guard_sql(query, limit + 1)
    try:
        cur = st.db.execute(stmt)
        rows = cur.fetchmany(limit + 1)
    except sqlite3.Error as e:
        raise Fail("sql: %s" % e, 1)
    cols = [d[0] for d in (cur.description or [])]
    more = len(rows) > limit
    rows = rows[:limit]
    notes = []
    if appended:
        notes.append("LIMIT %d applied" % limit)
    if more:
        notes.append("row cap %d reached; more rows exist (add LIMIT/OFFSET to page)" % limit)
    return Table(cols, rows, len(rows), 0, notes, more=more)


def op_worklist(st, kind, topic=None, as_of=None, forecast_days=0, limit=20, offset=0, cls=None):
    if kind not in WORKLISTS:
        raise Fail("worklist kind must be one of %s" % ", ".join(WORKLISTS), 2)
    limit, offset = _clamp(limit, 20, 200), max(0, int(offset or 0))
    if kind == "stale":
        try:
            day = dt.date.fromisoformat(as_of) if as_of else today()
        except ValueError:
            raise Fail("as_of must be YYYY-MM-DD", 2)
        until = (day + dt.timedelta(days=int(forecast_days or 0))).isoformat()
        w, a = _filters(topic, None, False)
        w.append("r.stale_on <= ?")
        a.append(until)
        where = " WHERE " + " AND ".join(w)
        total = st.one("SELECT count(*) FROM record r" + where, a)
        rows = st.q("SELECT %s, r.checked_on, r.verified_basis FROM record r%s "
                    "ORDER BY r.self_hosted, r.vorder, r.stale_on, r.rid "
                    "LIMIT ? OFFSET ?" % (CARD_SQL, where), a + [limit, offset])
        already = st.one("SELECT count(*) FROM record r WHERE r.stale_on <= ? AND r.duplicate_of IS NULL%s"
                         % (" AND r.topic = ?" if topic else ""), [day.isoformat()] + ([topic] if topic else []))
        return Table(CARD_COLS + ["checked_on", "verified_basis"], rows, total, offset,
                     ["stale on or before %s (as_of %s + %d days); %d already stale on %s; duplicates excluded"
                      % (until, day, int(forecast_days or 0), already, day)])
    tp = ("%s/%%" % topic) if topic else "%"
    if kind == "drift":
        total = st.one("SELECT count(*) FROM drift WHERE subject LIKE ?", (tp,))
        rows = st.q("SELECT d.kind, d.subject, d.other, d.field, d.a, d.b, d.detail FROM drift d "
                    "LEFT JOIN record r ON r.rid = d.subject WHERE d.subject LIKE ? "
                    "ORDER BY coalesce(r.self_hosted, 0), d.subject, d.other, d.field LIMIT ? OFFSET ?",
                    (tp, limit, offset))
        return Table(["kind", "subject", "other", "field", "a", "b", "detail"], rows, total, offset,
                     ["two records of one product disagree; fix one, or fr relate SRC duplicate_of DST"])
    if kind == "changes":
        # a log of events in time order, newest first: not a list of records, so not partitioned on self_hosted
        items = []
        for at, rid, path, old, new, rung, reason, op, url in st.q(
                "SELECT at, rid, path, old, new, rung, reason, %s, url FROM ledger WHERE rid LIKE ?" % ledger_op(st), (tp,)):
            items.append([at, "ledger", rid, "%s%s%s" % ("%s: " % path if path else "", ledger_title(old, new, op, path, url),
                                                     (" (%s)" % reason) if reason else "")])
        hw = "" if not topic else " WHERE hid IN (SELECT hid FROM history_link WHERE rid LIKE ?)"
        for hid, when, status, title in st.q("SELECT hid, when_utc, status, title FROM history" + hw,
                                             (tp,) if topic else ()):
            items.append([when, "history", hid, ("[%s] " % status if status else "") + (title or "")])
        items.sort(key=lambda r: r[0] or "", reverse=True)
        return Table(["at", "kind", "id", "what"], items[offset:offset + limit], len(items), offset)
    if kind == "unparsed":
        total = st.one("SELECT count(*) FROM claim WHERE parse='unparsed' AND rid LIKE ?", (tp,))
        if st.has("leaf"):
            rows = st.q("SELECT c.rid, c.path, c.kind, l.value FROM claim c JOIN record r ON r.rid = c.rid "
                        "LEFT JOIN leaf l ON l.lid BETWEEN r.lid_min AND r.lid_max AND l.path = c.path "
                        "WHERE c.parse='unparsed' AND c.rid LIKE ? ORDER BY r.self_hosted, r.vorder, c.rid, c.path "
                        "LIMIT ? OFFSET ?",
                        (tp, limit, offset))
        else:
            rows = st.q("SELECT c.rid, c.path, c.kind, NULL FROM claim c JOIN record r ON r.rid = c.rid "
                        "WHERE c.parse='unparsed' AND c.rid LIKE ? ORDER BY r.self_hosted, r.vorder, c.rid, c.path "
                        "LIMIT ? OFFSET ?", (tp, limit, offset))
        return Table(["rid", "path", "kind", "value"], rows, total, offset,
                     ["claim-bearing values no number was parsed from; restate them with a number and unit"])
    if kind == "unknown":
        st.need_local("unknown")
        w = "u.rid LIKE ?" + (" AND u.class = ?" if cls else "")
        a = [tp] + ([cls] if cls else [])
        total = st.one("SELECT count(*) FROM unknown u WHERE " + w, a)
        rows = st.q("SELECT u.rid, u.path, u.class, u.rule FROM unknown u LEFT JOIN record r ON r.rid = u.rid "
                    "WHERE %s ORDER BY coalesce(r.self_hosted, 0), u.rid, u.path LIMIT ? OFFSET ?" % w,
                    a + [limit, offset])
        by = st.q("SELECT class, count(*) FROM unknown WHERE rid LIKE ? GROUP BY class ORDER BY 2 DESC", (tp,))
        return Table(["rid", "path", "class", "rule"], rows, total, offset,
                     ["by class: " + ", ".join("%s %d" % r for r in by), "--class C narrows to one class"])
    # held
    st.need_local("strip_log")
    total = st.one("SELECT count(*) FROM strip_log WHERE rule LIKE '%-held' AND rid LIKE ?", (tp,))
    rows = st.q("SELECT s.rid, s.path, s.rule, s.before FROM strip_log s LEFT JOIN record r ON r.rid = s.rid "
                "WHERE s.rule LIKE '%-held' AND s.rid LIKE ? ORDER BY coalesce(r.self_hosted, 0), s.rid, s.path "
                "LIMIT ? OFFSET ?", (tp, limit, offset))
    return Table(["rid", "path", "rule", "before"], rows, total, offset,
                 ["clauses that carry a number but were held back from the public projection; "
                  "restate the number without the narrative to publish it"])


def op_evidence(st, rid):
    if not st.rid_exists(rid):
        raise Fail("no record %s" % rid)
    cap = dict(st.q("SELECT url, path FROM capture"))
    if st.has("raw"):
        doc = json.loads(st.one("SELECT doc FROM raw WHERE rid=?", (rid,)))
        ev = [(i, e.get("date"), e.get("url"), e.get("proved")) for i, e in enumerate(doc.get("evidence") or [])
              if isinstance(e, dict)]
        src = "source JSON"
    else:
        ev = st.q("SELECT ord, date, url, proved FROM evidence WHERE rid=? ORDER BY ord", (rid,))
        src = "projection"
    rows = [[o, d, u, cap.get(u), p] for o, d, u, p in ev]
    c = st.q("SELECT confidence, verified_at FROM record WHERE rid=?", (rid,))[0]
    return Table(["ord", "date", "url", "capture", "proved"], rows,
                 notes=["%s: confidence %s, verified_at %s; read from the %s" % (rid, c[0], c[1], src)])


def op_cites(st, part, limit=50, offset=0):
    if not part:
        raise Fail("cites needs part of a URL", 2)
    limit, offset = _clamp(limit, 50, 200), max(0, int(offset or 0))
    rows = []
    if st.has("raw"):
        for rid, doc in st.q("SELECT rid, doc FROM raw WHERE instr(doc, ?) > 0 ORDER BY rid", (part,)):
            for i, e in enumerate(json.loads(doc).get("evidence") or []):
                if isinstance(e, dict) and part in str(e.get("url") or ""):
                    rows.append([rid, i, e.get("date"), e.get("url"), e.get("proved")])
    else:
        rows = [list(r) for r in st.q("SELECT rid, ord, date, url, proved FROM evidence WHERE instr(url, ?) > 0 "
                                      "ORDER BY rid, ord", (part,))]
    verdict = dict(st.q("SELECT rid, verdict FROM record"))
    sh = st.self_hosted()[0]
    out = hosted_first([[r[0], verdict.get(r[0])] + r[1:] for r in rows if r[0] in verdict], lambda r: r[0] in sh)
    nrec = len({r[0] for r in out})
    return Table(["rid", "verdict", "ord", "date", "url", "proved"], out[offset:offset + limit], len(out), offset,
                 ["%d records cite a URL containing %r" % (nrec, part)])


def git_log(repo, relpath, n=10):
    try:
        p = subprocess.run(["git", "-C", repo, "log", "--follow", "-n", str(n), "--format=%H%x09%ct%x09%s", "--",
                            relpath], capture_output=True, text=True, encoding="utf-8", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    out = []
    for ln in p.stdout.splitlines():
        c = ln.split("\t", 2)
        if len(c) == 3:
            when = dt.datetime.fromtimestamp(int(c[1]), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            out.append([when, "commit", c[0][:10], c[2]])
    return out


def op_history(st, rid, limit=10):
    if not st.rid_exists(rid):
        raise Fail("no record %s" % rid)
    path = st.one("SELECT path FROM record WHERE rid=?", (rid,))
    items = []
    for at, p, old, new, rung, reason, op, url in st.q("SELECT at, path, old, new, rung, reason, %s, url FROM ledger "
                                                       "WHERE rid=?" % ledger_op(st), (rid,)):
        items.append([at, "ledger", p, "%s%s%s" % (ledger_title(old, new, op, p, url), " [%s]" % rung if rung else "",
                                                   " (%s)" % reason if reason else "")])
    linked = set()
    for hid, when, status, title in st.q("SELECT h.hid, h.when_utc, h.status, h.title FROM history_link l "
                                         "JOIN history h USING (hid) WHERE l.rid=?", (rid,)):
        linked.add(hid)
        items.append([when, "history", hid, ("[%s] " % status if status else "") + (title or "")])
    if st.has("raw"):
        for h in json.loads(st.one("SELECT doc FROM raw WHERE rid=?", (rid,))).get("history") or []:
            if isinstance(h, str) and h not in linked:
                items.append([None, "history", h, "(named in the record's history[])"])
    items.sort(key=lambda r: r[0] or "", reverse=True)
    commits = git_log(st.repo, path, limit)
    notes = ["%s: %s; ledger and history entries newest first, then the last %d commits of the file"
             % (rid, path, limit)]
    return Multi([Table(["at", "kind", "id", "what"], items, notes=notes),
                  Table(["at", "kind", "id", "what"], commits, title="git log --follow " + path)],
                 {"rid": rid, "path": path, "entries": items, "commits": commits})


def rule_meaning(rules, rid_):
    base = rid_
    suffix = ""
    for s in ("-held", "-neutralised"):
        if rid_.endswith(s):
            base, suffix = rid_[:-len(s)], s
    if base == "X01":
        return "excluded", "whole record excluded from the public projection"
    if re.fullmatch(r"T[0-9a-f]{8}", base):
        return "template", "boilerplate repeated across records, replaced by its unknown class"
    for r in rules.get("drop_paths", []):
        if r["id"] == base:
            return "drop-path", "key dropped: " + r["glob"]
    for k, what in (("url_rewrite", "URL rewritten to its origin"), ("url_drop", "URL withheld")):
        for r in rules.get(k, []):
            if r["id"] == base:
                return k.replace("_", "-"), what
    for r in rules.get("pre_rewrite", []):
        if r["id"] == base:
            return "rewrite", "text rewritten before clause rules"
    for r in rules.get("clause_rules", []):
        if r["id"] == base:
            act = r.get("action", r["class"])
            if suffix == "-held":
                return "held", "%s clause carrying a number, held back for review" % r["class"]
            if suffix == "-neutralised":
                return "neutralised", "%s clause rewritten, kept" % r["class"]
            return "clause-" + act, "%s clause %s" % (r["class"], "dropped" if act in ("drop", "legal", "narrative")
                                                       else act)
    return "?", ""


def op_strip(st, action, rule=None, sample=10, seed=0, topic=None, limit=50, offset=0):
    st.need_local("strip_log")
    rules = json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8"))
    if action == "report":
        rows = []
        held = 0
        for r, n in st.q("SELECT rule, count(*) FROM strip_log GROUP BY rule ORDER BY 2 DESC, 1"):
            kind, what = rule_meaning(rules, r)
            rows.append([r, n, kind, what])
            if r.endswith("-held"):
                held += n
        total = st.one("SELECT count(*) FROM strip_log")
        limit, offset = _clamp(limit, 50, 500), max(0, int(offset or 0))
        return Table(["rule", "n", "kind", "what"], rows[offset:offset + limit], len(rows), offset,
                     notes=["%d changes in all; %d held clauses (rules ending -held)" % (total, held),
                            "fr strip review --rule ID --sample N shows the text before"])
    if action != "review":
        raise Fail("strip takes report or review", 2)
    sample = _clamp(sample, 10, 200)
    tp = ("%s/%%" % topic) if topic else "%"
    if rule:
        rows = st.q("SELECT rid, path, rule, before FROM strip_log WHERE rule = ? AND rid LIKE ?", (rule, tp))
    else:
        rows = st.q("SELECT rid, path, rule, before FROM strip_log WHERE rule LIKE '%-held' AND rid LIKE ?", (tp,))
    key = lambda r: hashlib.sha1(("%s\0%s\0%s\0%s" % (seed, r[0], r[1], r[3])).encode("utf-8")).hexdigest()
    pick = sorted(rows, key=key)[:sample]
    pick.sort(key=lambda r: (r[0], r[1]))
    kind, what = rule_meaning(rules, rule) if rule else ("held", "all held clauses")
    return Table(["rid", "path", "rule", "before"], pick, len(rows), 0,
                 ["%s: %s; a deterministic sample, --seed N for another" % (rule or "*-held", what)])


def op_verify(repo, db_path, force=False, explicit=False):
    t0 = time.time()
    if explicit:
        r = ensure_fresh(repo, db_path, quiet=True, force=force)
    else:
        before = store_file(repo)
        db_path = ensure_store(repo, force=force)
        why = "forced" if force else ("no store yet" if not before else "an input is newer")
        r = None if db_path == before else (why, None, time.time() - t0)
    st = Store(db_path, repo)
    try:
        m = st.meta()
        n = st.one("SELECT count(*) FROM record")
        nraw = st.one("SELECT count(*) FROM raw") if st.has("raw") else None
    finally:
        st.close()
    nfiles = sum(1 for _, _, fs in os.walk(os.path.join(repo, "dossier")) for f in fs
                 if f.endswith(".json") and not f.endswith(".generated.json"))
    built = dt.datetime.fromtimestamp(os.stat(db_path).st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    head = ("rebuilt in %.1f s (%s)" % (r[2], r[0])) if r else "current"
    line = ("fr: store %s %s; %d records (%s source files, %d read); commit %s; as_of %s; built %s"
            % (os.path.relpath(db_path, repo).replace("\\", "/"), head, n, nfiles,
               nraw if nraw is not None else -1, (m.get("commit") or "-")[:10], m.get("as_of"), built))
    ok = nraw is None or nraw == nfiles
    return Text(line + ("" if ok else "; MISMATCH: files and store differ") + "\n",
                {"current": not r, "rebuilt": bool(r), "reason": r[0] if r else None, "records": n, "files": nfiles,
                 "read": nraw, "commit": m.get("commit"), "as_of": m.get("as_of"), "built": built,
                 "seconds": round(time.time() - t0, 2)}), ok


# ====================================================================== JSON text editing

ABSENT = object()


class Node:
    __slots__ = ("start", "end", "kind", "items", "value")

    def __init__(self, start, end, kind, items, value):
        self.start, self.end, self.kind, self.items, self.value = start, end, kind, items, value


def parse_spans(text):
    """JSON text -> Node tree with the source span of every value."""
    from json.decoder import scanstring
    dec = json.JSONDecoder()
    n = len(text)
    WS = " \t\n\r"

    def skip(i):
        while i < n and text[i] in WS:
            i += 1
        return i

    def value(i):
        i = skip(i)
        c = text[i]
        if c == "{":
            start, items, obj = i, [], {}
            i = skip(i + 1)
            if text[i] == "}":
                return Node(start, i + 1, "obj", items, obj), i + 1
            while True:
                i = skip(i)
                if text[i] != '"':
                    raise ValueError("expected a key at %d" % i)
                key, i = scanstring(text, i + 1)
                i = skip(i)
                if text[i] != ":":
                    raise ValueError("expected ':' at %d" % i)
                node, i = value(i + 1)
                items.append((key, node))
                obj[key] = node.value
                i = skip(i)
                if text[i] == ",":
                    i += 1
                    continue
                if text[i] == "}":
                    return Node(start, i + 1, "obj", items, obj), i + 1
                raise ValueError("expected ',' or '}' at %d" % i)
        if c == "[":
            start, items = i, []
            i = skip(i + 1)
            if text[i] == "]":
                return Node(start, i + 1, "arr", items, []), i + 1
            while True:
                node, i = value(i)
                items.append(node)
                i = skip(i)
                if text[i] == ",":
                    i += 1
                    continue
                if text[i] == "]":
                    return Node(start, i + 1, "arr", items, [x.value for x in items]), i + 1
                raise ValueError("expected ',' or ']' at %d" % i)
        v, end = dec.raw_decode(text, i)
        return Node(i, end, "scalar", None, v), end

    root, end = value(0)
    if text[end:].strip():
        raise ValueError("trailing data after the JSON value")
    return root


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def file_style(text):
    nl = "\r\n" if text.count("\r\n") * 2 > text.count("\n") else "\n"
    ind = 2
    for ln in text.split("\n")[1:]:
        s = len(ln) - len(ln.lstrip(" "))
        if s:
            ind = s
            break
    return nl, ind


def dump_preserving(text, root, new):
    """Serialise `new`, copying the source text of every subtree that did not change, so untouched
    lines stay byte-identical; changed parts use the file's indent and line ending."""
    nl, ind = file_style(text)

    def single_line(node):
        return node is not None and node.kind in ("obj", "arr") and node.items and \
            "\n" not in text[node.start:node.end]

    def fmt(v, node, level, inline_hint=False):
        if node is not None and same(v, node.value):
            return text[node.start:node.end]
        if isinstance(v, (dict, list)):
            if not v:
                return "{}" if isinstance(v, dict) else "[]"
            if single_line(node) or (node is None and inline_hint):
                return json.dumps(v, ensure_ascii=False)
            pad, close = " " * (ind * (level + 1)), " " * (ind * level)
            if isinstance(v, dict):
                old = dict(node.items) if node is not None and node.kind == "obj" else {}
                parts = [pad + json.dumps(k, ensure_ascii=False) + ": " + fmt(x, old.get(k), level + 1)
                         for k, x in v.items()]
                return "{" + nl + ("," + nl).join(parts) + nl + close + "}"
            olds = node.items if node is not None and node.kind == "arr" else []
            boxes = [o for o in olds if o.kind in ("obj", "arr") and o.items]
            hint = bool(boxes) and all(single_line(o) for o in boxes)
            parts = [pad + fmt(x, olds[i] if i < len(olds) else None, level + 1, hint) for i, x in enumerate(v)]
            return "[" + nl + ("," + nl).join(parts) + nl + close + "]"
        return json.dumps(v, ensure_ascii=False)

    body = fmt(new, root, 0)
    return text[:root.start] + body + text[root.end:]


# ====================================================================== write operations

def parse_jpath(p):
    s = p.strip()
    if not s.startswith("$"):
        s = "$." + s
    seg = re.compile(r'\.([A-Za-z_][A-Za-z0-9_-]*)|\."((?:[^"\\]|\\.)*)"|\[(\d+)\]|\["((?:[^"\\]|\\.)*)"\]')
    i, out = 1, []
    while i < len(s):
        m = seg.match(s, i)
        if not m:
            raise Fail("cannot read the path %r at %r; use $.key, $.\"a key\", $.list[2]" % (p, s[i:]), 2)
        if m.group(1) is not None:
            out.append(m.group(1))
        elif m.group(2) is not None:
            out.append(json.loads('"%s"' % m.group(2)))
        elif m.group(3) is not None:
            out.append(int(m.group(3)))
        else:
            out.append(json.loads('"%s"' % m.group(4)))
        i = m.end()
    if not out or not isinstance(out[0], str):
        raise Fail("the path must name a top-level key: $.free_tier.stated", 2)
    return out


def get_path(obj, segs):
    cur = obj
    for k in segs:
        if isinstance(k, int):
            if not isinstance(cur, list) or k >= len(cur):
                return ABSENT
        elif not isinstance(cur, dict) or k not in cur:
            return ABSENT
        cur = cur[k]
    return cur


def set_path(obj, segs, value):
    cur = obj
    for k, nxt in zip(segs[:-1], segs[1:]):
        if isinstance(k, int):
            if not isinstance(cur, list) or k >= len(cur):
                raise Fail("no element [%d] on the way to %s" % (k, jpath(segs)), 2)
        else:
            if not isinstance(cur, dict):
                raise Fail("%s is not an object on the way to %s" % (k, jpath(segs)), 2)
            if k not in cur or cur[k] is None:
                if isinstance(nxt, int):
                    raise Fail("no list at %s" % k, 2)
                cur[k] = {}
        cur = cur[k]
    last = segs[-1]
    if isinstance(last, int):
        if not isinstance(cur, list):
            raise Fail("%s is not a list" % jpath(segs[:-1]), 2)
        if last < len(cur):
            old, cur[last] = cur[last], value
        elif last == len(cur):
            old = ABSENT
            cur.append(value)
        else:
            raise Fail("index %d is past the end of %s (length %d)" % (last, jpath(segs[:-1]), len(cur)), 2)
    else:
        if not isinstance(cur, dict):
            raise Fail("%s is not an object" % jpath(segs[:-1]), 2)
        old = cur.get(last, ABSENT)
        cur[last] = value
    return old


def load_validate(repo):
    path = os.path.join(repo, "scripts", "dossier", "validate.py")
    if not os.path.exists(path):
        path = os.path.join(DEFAULT_REPO, "scripts", "dossier", "validate.py")
    spec = importlib.util.spec_from_file_location("fr_dossier_validate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sp = os.path.join(repo, "scripts", "dossier", "schema.json")
    if not os.path.exists(sp):
        sp = os.path.join(DEFAULT_REPO, "scripts", "dossier", "schema.json")
    return mod, mod.load_schema(sp)


def validate_record(repo, rec):
    mod, schema = load_validate(repo)
    v = mod.Validator(schema)
    v.validate(rec)
    return v.errors


def check_date(d, what="--date"):
    if not d or not DATE_RE.match(d):
        raise Fail("%s must be YYYY-MM-DD" % what, 2)
    try:
        day = dt.date.fromisoformat(d)
    except ValueError:
        raise Fail("%s %s is not a real date" % (what, d), 2)
    if day > today():
        raise Fail("%s %s is in the future (UTC today is %s)" % (what, d, today()), 2)
    return d


def capture_lanes(repo, cap):
    """The id folders under .tmp/ that hold capture `cap`: a session folder (.tmp/<id>/captures/) or a unit folder of
    a run (.tmp/<run>/units/<unit>/captures/)."""
    import glob
    h = cap.split(":", 1)[-1]
    hits = glob.glob(os.path.join(repo, ".tmp", "*", "captures", h + ".md")) + \
        glob.glob(os.path.join(repo, ".tmp", "*", "units", "*", "captures", h + ".md"))
    return [os.path.dirname(os.path.dirname(p)) for p in sorted(hits)]


def with_capture(repo, ev, args):
    """--capture sha256:... --quote "..." : the capture (a page text, or a probe record registered with --probe) must
    be in sources/c/, sources/p/ or a folder under .tmp/ (scripts/rq folder session, then scripts/rq capture URL --lane
    .tmp/session-<id>); the quote must be found in its text."""
    cap, quote = getattr(args, "capture", None), getattr(args, "quote", None)
    if not cap and not quote:
        rqc = _rq()
        u, d = ev.get("url") or "", ev.get("date") or ""
        page_row = u.startswith("http") and d >= rqc.SETTINGS["capture_cutover"]
        probe_row = u.startswith("probe:") and d >= rqc.SETTINGS.get("probe_capture_cutover", "9999-12-31")
        if page_row or probe_row:
            # the gate's rule C21 fails this row; say so before the write, not after the gate
            print("fr: warning: an evidence row dated %s with no --capture and --quote fails the gate (rule C21). Capture "
                  "the page with scripts/rq folder session, then scripts/rq capture URL --lane .tmp/session-<id> (a probe "
                  "record: --probe FILE) and pass --capture sha256:... --quote \"the sentence\"" % d, file=sys.stderr)
        return ev
    if not (cap and quote):
        raise Fail("--capture and --quote go together", 2)
    rqc = _rq()
    lanes = capture_lanes(repo, cap) if rqc.SHA_RE.match(cap) else []
    lane = lanes[0] if lanes else None
    text = rqc.read_capture(cap, repo, lane)
    if text is None:
        raise Fail("no capture %s in sources/c/, sources/p/ or a captures/ folder under .tmp/" % cap, 1)
    verdict, score = rqc.quote_found(quote, text)
    if verdict == "miss":
        raise Fail("the quote is not in capture %s (best %.2f)" % (cap[:20], score), 1)
    if not getattr(args, "dry_run", False) and lane:
        rqc.promote_capture(cap, lane, repo)
    ev["capture"], ev["quote"] = cap, quote.strip()
    return ev


def check_evidence(url, date, proved):
    if not url or not URL_RE.match(url):
        raise Fail("--evidence must be https://... or probe:<target>", 2)
    check_date(date)
    if not proved or len(proved.strip()) < 8:
        raise Fail("--proved must say what the source established (8 characters at least)", 2)
    if "\n" in proved or "\t" in proved:
        raise Fail("--proved must be one line", 2)
    return {"url": url, "date": date, "proved": proved.strip()}


def check_rid(rid):
    if not RID_RE.match(rid or ""):
        raise Fail("a rid is topic/slug in lowercase: storage/hetzner-storage-box", 2)
    return rid


def record_file(repo, rid):
    topic, slug = check_rid(rid).split("/")
    return os.path.join(repo, "dossier", topic, slug + ".json")


def read_record(repo, rid):
    p = record_file(repo, rid)
    if not os.path.exists(p):
        raise Fail("no record %s (looked for %s)" % (rid, os.path.relpath(p, repo)), 1)
    raw = open(p, "rb").read()
    text = raw.decode("utf-8")
    return p, text, parse_spans(text)


def write_atomic(path, text):
    tmp = "%s.fr-%d" % (path, os.getpid())
    with open(tmp, "wb") as f:
        f.write(text.encode("utf-8"))
    os.replace(tmp, path)


def append_line(path, line):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "ab") as f:
        f.write((line.rstrip("\n") + "\n").encode("utf-8"))


def ledger(repo, rid, path, old, new, rung, ev, reason, also=None):
    o = collections.OrderedDict()
    o["at"] = utc_stamp_ms()
    o["rid"] = rid
    o["path"] = path
    o["old"] = None if old is ABSENT else old
    o["new"] = new
    o["rung"] = rung
    o["evidence"] = ev
    o["reason"] = reason
    if also:
        o["also"] = also
    append_line(os.path.join(repo, "history", "ledger.jsonl"), json.dumps(o, ensure_ascii=False))
    return o


def diff_summary(old_text, new_text, name, maxlines=10):
    a, b = old_text.splitlines(), new_text.splitlines()
    lines = [x for x in difflib.unified_diff(a, b, lineterm="", n=0) if not x.startswith(("---", "+++"))]
    body = [x for x in lines if not x.startswith("@@")]
    adds = sum(1 for x in body if x.startswith("+"))
    dels = sum(1 for x in body if x.startswith("-"))
    out = ["%s: +%d -%d lines" % (name, adds, dels)]
    for x in body[:maxlines - 1]:
        out.append(cell(x, 160))
    if len(body) > maxlines - 1:
        out.append("... %d more changed lines" % (len(body) - maxlines + 1))
    return out


def subject(s):
    s = re.sub(r"\s+", " ", s).strip().rstrip(".")
    return s if len(s) < 100 else s[:96].rstrip(" ,;:-") + "..."


def short_path(segs):
    return jpath(segs)[2:] if len(segs) else "$"


def stronger(a, b):
    return LADDER.index(a) > LADDER.index(b)


def write_record(repo, path, rid, old_text, root, new, dry_run, why):
    """Validate and write; -> new text. Writes nothing when validation fails."""
    errs = validate_record(repo, new)
    if errs:
        msg = "; ".join("%s %s: %s" % (e.get("path"), e.get("keyword"), e.get("message")) for e in errs[:6])
        raise Fail("%s would not validate, nothing written: %s" % (rid, msg), 1)
    text = dump_preserving(old_text, root, new)
    if not same(json.loads(text), new):
        raise Fail("internal: the serialised record does not read back equal; nothing written", 1)
    if not dry_run and text != old_text:
        write_atomic(path, text)
    return text


def after_write(args, lines):
    if args.dry_run:
        lines.append("dry run: nothing written")
    elif getattr(args, "no_rebuild", False):
        lines.append("store not rebuilt: run fr verify")
    elif getattr(args, "db_explicit", False):
        r = ensure_fresh(args.repo, args.db_path, quiet=True)
        lines.append("store rebuilt in %.1f s" % r[2] if r else "store current")
    else:
        t0 = time.time()
        before = store_file(args.repo)
        after = ensure_store(args.repo)
        lines.append("store rebuilt in %.1f s" % (time.time() - t0) if after != before else "store current")
    return Text("\n".join(lines) + "\n", {"lines": lines})


WRITE_REFUSAL = ("the research checkout changes records only through a run: scripts/rq open amend TOPIC \"RID: what is "
                 "wrong\" (AGENTS.md section 2 rule 14). A hand change belongs to a session that the operator starts in "
                 "its own clone.")


def cmd_amend(args):
    rid = check_rid(args.rid)
    segs = parse_jpath(args.path)
    top = segs[0]
    if top in REFUSED_PATHS:
        raise Fail("refused: $.%s is not amendable (%s)" % (top, REFUSED_PATHS[top]), 2)
    mod, schema = load_validate(args.repo)
    if top not in schema.get("properties", {}):
        raise Fail("refused: %s is not a schema key; free-form fields go under $.extras" % top, 2)
    if args.rung and args.rung not in LADDER:
        raise Fail("--rung must be one of %s" % ", ".join(reversed(LADDER)), 2)
    if args.string:
        value = args.value
    else:
        try:
            value = json.loads(args.value)
        except ValueError:
            value = args.value
    ev = with_capture(args.repo, check_evidence(args.evidence, args.date, args.proved), args)
    path, text, root = read_record(args.repo, rid)
    rec = json.loads(text)
    old = set_path(rec, segs, value)
    also = {}
    if top == "confidence" and isinstance(value, str) and value in LADDER \
            and isinstance(old, str) and old in LADDER and stronger(value, old):
        if not args.rung or stronger(value, args.rung):
            raise Fail("refused: raising confidence to %s needs --rung %s or stronger" % (value, value), 2)
    evl = rec.setdefault("evidence", [])
    if not any(isinstance(e, dict) and e.get("url") == ev["url"] and e.get("date") == ev["date"]
               and e.get("proved") == ev["proved"] for e in evl):
        evl.append(ev)
    conf = rec.get("confidence")
    if args.rung and conf in LADDER and stronger(conf, args.rung):
        rec["confidence"] = args.rung
        also["$.confidence"] = [conf, args.rung]
    if args.verified:
        va = rec.get("verified_at")
        rec["verified_at"] = utc_stamp_ms()
        also["$.verified_at"] = [va, rec["verified_at"]]
    orig = json.loads(text)
    if same(orig, rec):
        return Text("%s: no change (value, evidence and verified_at already as given); nothing written\n" % rid,
                    {"changed": False})
    new_text = write_record(args.repo, path, rid, text, root, rec, args.dry_run, "amend")
    lines = diff_summary(text, new_text, os.path.relpath(path, args.repo).replace("\\", "/"))
    if not args.dry_run:
        ledger(args.repo, rid, jpath(segs), old, value, args.rung, ev, args.reason, also or None)
        lines.append("ledger: history/ledger.jsonl +1 line")
    for k, (a, b) in also.items():
        lines.append("also %s: %s -> %s" % (k, a, b))
    t, s = rid.split("/")
    lines.append("commit subject: " + subject("%s: %s %s amended" % (t, s, short_path(segs))))
    return after_write(args, lines)


def cmd_add(args):
    rid = check_rid(args.rid)
    topic, slug = rid.split("/")
    mod, schema = load_validate(args.repo)
    topics = schema["properties"]["topic"].get("enum") or []
    if topic not in topics:
        raise Fail("topic %s is not one of %s" % (topic, ", ".join(topics)), 2)
    path = record_file(args.repo, rid)
    if os.path.exists(path):
        raise Fail("refused: %s exists; change it with fr amend" % rid, 1)
    if not args.url or not re.match(r"^https?://\S+$", args.url):
        raise Fail("--url must be the http(s) page the numbers come from", 2)
    if not args.provider or not args.provider.strip():
        raise Fail("--provider is required", 2)
    rung = args.rung or "unverified"
    if rung not in LADDER:
        raise Fail("--rung must be one of %s" % ", ".join(reversed(LADDER)), 2)
    verdict = args.verdict or "trial-only"
    if verdict not in VERDICTS:
        raise Fail("--verdict must be one of %s" % ", ".join(VERDICTS), 2)
    ev = with_capture(args.repo, check_evidence(args.evidence, args.date, args.proved), args)
    why = "not stated: added by fr add from one source; %s not yet read"
    ph = []

    def p(path_, val):
        ph.append(path_)
        return val
    rec = collections.OrderedDict()
    rec["topic"] = topic
    rec["slug"] = slug
    rec["provider"] = args.provider.strip()
    rec["url"] = args.url
    rec["category"] = args.category or p("$.category", why % "the category")
    rec["free_tier"] = {"stated": p("$.free_tier.stated", why % "the offer"), "unit": p("$.free_tier.unit", "none"),
                        "source_url": args.url}
    rec["per_object_cap"] = {"stated": p("$.per_object_cap.stated", why % "the per-object cap")}
    rec["retention"] = {"stated": p("$.retention.stated", why % "the retention")}
    rec["egress"] = {"terms": p("$.egress.terms", why % "the egress terms"), "metered": p("$.egress.metered", False)}
    rec["interface"] = p("$.interface", ["unknown"])
    rec["tooling"] = p("$.tooling", why % "the tooling")
    rec["chaining"] = p("$.chaining", why % "how it chains")
    rec["limits"] = []
    rec["identity_cost"] = {"kind": p("$.identity_cost.kind", "email"),
                            "detail": p("$.identity_cost.detail", "not stated in the source: identity requirement "
                                                                   "not yet read; kind defaulted")}
    rec["reliability_note"] = p("$.reliability_note", why % "reliability")
    rec["confidence"] = rung
    rec["evidence"] = [ev]
    rec["verdict"] = verdict if args.verdict else p("$.verdict", verdict)
    rec["verified_at"] = utc_stamp_ms()
    rec["extras"] = {"identity_cost_defaulted": True, "placeholders": ph}
    errs = validate_record(args.repo, rec)
    if errs:
        raise Fail("%s would not validate, nothing written: %s" % (
            rid, "; ".join("%s: %s" % (e.get("path"), e.get("message")) for e in errs[:6])), 1)
    lines = []
    try:
        st = Store(args.db_path, args.repo)
        sims = name_scores(st, args.provider)[:8]
        import entity as ent_mod  # noqa: E402
        host, _ = ent_mod.host_path(args.url)
        dom = ent_mod.PSL().registrable(host) if host else None
        same_dom = st.q("SELECT eid, name, n_records FROM entity WHERE domain=?", (dom,)) if dom else []
        names = dict((e, (n, k)) for e, n, k in st.q("SELECT eid, name, n_records FROM entity"))
        for e, n, k in same_dom:
            lines.append("same domain %s: entity %s (%s, %d records)" % (dom, e, n, k))
        for e, s, hw in sims:
            if not any(e == x[0] for x in same_dom):
                lines.append("similar name: entity %s (%s, %d records, %s)" % (e, names[e][0], names[e][1], hw))
        st.close()
    except Fail:
        lines.append("no store to compare names against; run fr verify")
    if lines:
        lines.insert(0, "check these before keeping a second record for one provider (fr entity EID):")
    text = json.dumps(rec, ensure_ascii=False, indent=2) + "\n"
    if not args.dry_run:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            raise Fail("refused: %s appeared while writing" % rid, 1)
        write_atomic(path, text)
        ledger(args.repo, rid, "$", None, {"provider": rec["provider"], "url": rec["url"], "verdict": rec["verdict"],
                                           "confidence": rung}, rung, ev, args.reason or "new record")
        lines.append("ledger: history/ledger.jsonl +1 line")
    lines.append("%s dossier/%s/%s.json with %d placeholders (extras.placeholders); fill them with fr amend"
                 % ("would write" if args.dry_run else "wrote", topic, slug, len(ph)))
    lines.append("commit subject: " + subject("%s: add %s" % (topic, slug)))
    return after_write(args, lines)


def cmd_dead(args):
    rid = check_rid(args.rid)
    if args.cause not in CAUSES:
        raise Fail("--cause must be one of %s" % ", ".join(CAUSES), 2)
    check_date(args.observed, "--observed")
    ev = with_capture(args.repo, check_evidence(args.evidence, args.observed, args.proved), args)
    if args.rung and args.rung not in LADDER:
        raise Fail("--rung must be one of %s" % ", ".join(reversed(LADDER)), 2)
    path, text, root = read_record(args.repo, rid)
    rec = json.loads(text)
    old_verdict = rec.get("verdict")
    rec["verdict"] = "dead"
    ex = rec.get("extras")
    if not isinstance(ex, dict):
        ex = rec["extras"] = {}
    old_death = ex.get("death", ABSENT)
    ex["death"] = {"on": args.observed, "cause": args.cause}
    if not any(isinstance(e, dict) and e.get("url") == ev["url"] and e.get("date") == ev["date"]
               and e.get("proved") == ev["proved"] for e in rec.setdefault("evidence", [])):
        rec["evidence"].append(ev)
    also = {"$.extras.death": [None if old_death is ABSENT else old_death, ex["death"]]}
    conf = rec.get("confidence")
    if args.rung and conf in LADDER and stronger(conf, args.rung):
        rec["confidence"] = args.rung
        also["$.confidence"] = [conf, args.rung]
    if same(json.loads(text), rec):
        return Text("%s: already dead with this death and evidence; nothing written\n" % rid, {"changed": False})
    new_text = write_record(args.repo, path, rid, text, root, rec, args.dry_run, "dead")
    lines = diff_summary(text, new_text, os.path.relpath(path, args.repo).replace("\\", "/"))
    if not args.dry_run:
        ledger(args.repo, rid, "$.verdict", old_verdict, "dead", args.rung, ev, args.reason or args.cause, also)
        lines.append("ledger: history/ledger.jsonl +1 line")
    t, s = rid.split("/")
    lines.append("commit subject: " + subject("%s: %s is dead (%s on %s)" % (t, s, args.cause, args.observed)))
    return after_write(args, lines)


def tsv_field(v, what):
    if v is None or "\t" in v or "\n" in v or "\r" in v:
        raise Fail("%s must be one line with no tabs" % what, 2)
    return v.strip()


def ensure_tsv(path, header):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write((header + "\n").encode("utf-8"))


def read_tsv(path):
    if not os.path.exists(path):
        return []
    rows = []
    for ln in open(path, encoding="utf-8"):
        if ln.strip() and not ln.startswith("#") and not ln.startswith(("rid\t", "src\t")):
            rows.append(ln.rstrip("\r\n").split("\t"))
    return rows


def cmd_relate(args):
    src, dst = check_rid(args.src), check_rid(args.dst)
    if args.kind not in RELATIONS:
        raise Fail("KIND must be one of %s" % ", ".join(RELATIONS), 2)
    if src == dst:
        raise Fail("a record cannot relate to itself", 2)
    for r in (src, dst):
        if not os.path.exists(record_file(args.repo, r)):
            raise Fail("no record %s" % r, 1)
    if not args.evidence or not URL_RE.match(args.evidence):
        raise Fail("--evidence must be https://... or probe:<target>", 2)
    check_date(args.date)
    reason = tsv_field(args.reason, "--reason")
    if len(reason) < 8:
        raise Fail("--reason must say why (8 characters at least)", 2)
    path = os.path.join(args.repo, "registry", "relations.tsv")
    rows = read_tsv(path)
    for c in rows:
        if len(c) >= 3 and (c[0], c[1], c[2]) == (src, args.kind, dst):
            raise Fail("refused: %s %s %s is already recorded" % (src, args.kind, dst), 1)
        if args.kind == "duplicate_of" and len(c) >= 3 and c[1] == "duplicate_of":
            if c[0] == src:
                raise Fail("refused: %s is already duplicate_of %s" % (src, c[2]), 1)
            if c[0] == dst and c[2] == src:
                raise Fail("refused: %s is already duplicate_of %s; a cycle" % (dst, src), 1)
    row = "\t".join([src, args.kind, dst, tsv_field(args.evidence, "--evidence"), args.date, reason])
    lines = ["registry/relations.tsv: + %s" % row.replace("\t", "  ")]
    if not args.dry_run:
        ensure_tsv(path, "src\tkind\tdst\tevidence_url\tdate\treason")
        append_line(path, row)
    lines.append("commit subject: " + subject("registry: %s %s %s" % (src, args.kind, dst)))
    return after_write(args, lines)


def cmd_entity_set(args):
    rid = check_rid(args.rid)
    if not SLUG_RE.match(args.eid or ""):
        raise Fail("EID must be lowercase and hyphenated: hetzner", 2)
    if not os.path.exists(record_file(args.repo, rid)):
        raise Fail("no record %s" % rid, 1)
    reason = tsv_field(args.reason, "--reason")
    if len(reason) < 8:
        raise Fail("--reason must say why (8 characters at least)", 2)
    name = tsv_field(args.name or "", "--name")
    path = os.path.join(args.repo, "registry", "entities.tsv")
    prior = [c for c in read_tsv(path) if c and c[0] == rid]
    if prior and len(prior[-1]) > 1 and prior[-1][1] == args.eid and \
            (prior[-1][2] if len(prior[-1]) > 2 else "") == name:
        raise Fail("refused: %s is already set to entity %s" % (rid, args.eid), 1)
    row = "\t".join([rid, args.eid, name, reason])
    lines = ["registry/entities.tsv: + %s" % row.replace("\t", "  ")]
    if prior:
        lines.append("supersedes the earlier override %s -> %s (the last line wins)" % (rid, prior[-1][1]))
    if not args.dry_run:
        ensure_tsv(path, "rid\teid\tname\treason")
        append_line(path, row)
    lines.append("commit subject: " + subject("registry: %s joins entity %s" % (rid, args.eid)))
    return after_write(args, lines)


# ====================================================================== MCP

PROTOCOLS = ["2025-06-18", "2025-11-25"]
_S, _I, _N, _B = {"type": "string"}, {"type": "integer"}, {"type": "number"}, {"type": "boolean"}


def _obj(props, req=()):
    o = {"type": "object", "properties": props}
    if req:
        o["required"] = list(req)
    return o


MCP_TOOLS = [
    ("help", "Read first: the store's tables, vocabularies, rules and worked SQL.", _obj({})),
    ("search", "Find records by vendor name, then BM25 full text. Rows are cards plus matched columns.",
     _obj({"q": _S, "topic": _S, "grp": _S, "limit": _I, "offset": _I}, ["q"])),
    ("filter", "List records by whitelisted filters. no_card means needs_card=0 with a stated identity.",
     _obj({"topic": _S, "verdict": _S, "grp": _S, "confidence": _S, "no_card": _B, "no_phone": _B,
           "anonymous": _B, "iface": _S, "binding": _S, "crypto": _B, "max_usd_month": _N, "max_usd_tb": _N,
           "include_duplicates": _B, "sort": {"type": "string", "enum": SORTS},
           "order": {"type": "string", "enum": ["asc", "desc"]}, "limit": _I, "offset": _I})),
    ("get", "Records by rid (topic/slug): card rows, or detail=full for the record JSON, claims, unknowns, history.",
     _obj({"ids": {"type": "array", "items": _S}, "detail": {"type": "string", "enum": ["card", "full"]},
           "fields": _S}, ["ids"])),
    ("entity", "A vendor by eid or name, with all its records.", _obj({"id": _S}, ["id"])),
    ("need", "Best-per-need lists. No id lists the needs.", _obj({"id": _S, "limit": _I, "offset": _I})),
    ("sql", "Read-only SQL over the store (one SELECT/WITH/VALUES/EXPLAIN statement).",
     _obj({"query": _S, "limit": _I}, ["query"])),
    ("worklist", "Work queues: stale, drift, changes, unparsed (local also: unknown, held).",
     _obj({"kind": {"type": "string", "enum": WORKLISTS}, "topic": _S, "as_of": _S, "forecast_days": _I,
           "limit": _I, "offset": _I}, ["kind"])),
]


def mcp_call(repo, db_path, name, a):
    # the store path is resolved on each call, so a server that outlives a `scripts/rq sync` reads the new HEAD's store:
    # the memo of HEAD and of the marker lasts one call, not the life of the server (LIO7-03)
    if _MEMO is not None:
        _MEMO.clear()
    if db_path:
        ensure_fresh(repo, db_path)
    else:
        db_path = ensure_store(repo)
    st = Store(db_path, repo)
    try:
        if name == "help":
            return Text(primer.text(db_path))
        if name == "search":
            return op_search(st, a.get("q"), a.get("topic"), a.get("grp"), a.get("limit"), a.get("offset"),
                             a.get("include_duplicates", False))
        if name == "filter":
            keys = ("topic verdict grp confidence no_card no_phone anonymous iface binding crypto max_usd_month "
                    "max_usd_tb include_duplicates sort order limit offset keep_null").split()
            return op_filter(st, **{k: a[k] for k in keys if k in a})
        if name == "get":
            return op_get(st, a.get("ids"), a.get("detail") or "card", a.get("fields"))
        if name == "entity":
            return op_entity(st, a.get("id"), a.get("limit"), a.get("offset"))
        if name == "need":
            return op_need(st, a.get("id"), a.get("limit"), a.get("offset"))
        if name == "sql":
            return op_sql(st, a.get("query"), a.get("limit"))
        if name == "worklist":
            return op_worklist(st, a.get("kind"), a.get("topic"), a.get("as_of"), a.get("forecast_days") or 0,
                               a.get("limit"), a.get("offset"), a.get("class"))
        raise Fail("unknown tool %s" % name, 2)
    finally:
        st.close()


def serve_mcp(repo, db_path, inp, outp):
    def send(o):
        outp.write(json.dumps(o, ensure_ascii=False) + "\n")
        outp.flush()

    for line in inp:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}})
            continue
        batch = msg if isinstance(msg, list) else [msg]
        for m in batch:
            if not isinstance(m, dict):
                send({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "invalid request"}})
                continue
            mid, method, params = m.get("id"), m.get("method"), m.get("params") or {}
            if method is None:
                continue  # a response from the client; nothing to do
            notify = "id" not in m
            try:
                if method == "initialize":
                    want = str(params.get("protocolVersion") or "")
                    ver = want if want >= PROTOCOLS[0] else PROTOCOLS[-1]
                    res = {"protocolVersion": ver, "capabilities": {"tools": {"listChanged": False}},
                           "serverInfo": {"name": "fshy-local", "version": "1"},
                           "instructions": "Call help first. Rows are TSV with '# ' footers; rid = topic/slug."}
                elif method == "ping":
                    res = {}
                elif method == "tools/list":
                    res = {"tools": [{"name": n, "description": d, "inputSchema": s} for n, d, s in MCP_TOOLS]}
                elif method == "tools/call":
                    name = params.get("name")
                    if name not in [t[0] for t in MCP_TOOLS]:
                        raise Fail("unknown tool %s" % name, -32602)
                    try:
                        out = mcp_call(repo, db_path, name, params.get("arguments") or {})
                        res = {"content": [{"type": "text", "text": out.tsv(80)}], "isError": False}
                    except Fail as e:
                        res = {"content": [{"type": "text", "text": "fr: %s" % e}], "isError": True}
                    except (sqlite3.Error, ValueError, TypeError) as e:
                        res = {"content": [{"type": "text", "text": "fr: %s" % e}], "isError": True}
                elif method.startswith("notifications/"):
                    continue
                else:
                    if not notify:
                        send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "no method %s" % method}})
                    continue
                if not notify:
                    send({"jsonrpc": "2.0", "id": mid, "result": res})
            except Fail as e:
                if not notify:
                    send({"jsonrpc": "2.0", "id": mid, "error": {"code": e.code if e.code < 0 else -32602,
                                                                 "message": str(e)}})
            except Exception as e:  # keep serving: one bad call must not end the session
                if not notify:
                    send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": "%s: %s"
                                                                 % (type(e).__name__, e)}})


# ====================================================================== CLI

import primer  # noqa: E402

CLI_HELP = """
FR COMMANDS (local; every read rebuilds the store first when an input is newer)
  search WORDS | filter --topic T --no-card --sort usd_per_tb_month | get RID [--detail full|--raw]
  entity NAME | need [ID] | sql "SELECT ..." | worklist stale|drift|changes|unparsed|unknown|held
  evidence RID | cites URL-PART | history RID | strip report | strip review --rule ID | verify
  amend RID PATH VALUE --evidence URL --date D --proved TEXT [--rung R] [--verified] [--dry-run]
  add TOPIC/SLUG ... | dead RID --cause C ... | relate SRC KIND DST ... | entity-set RID EID ...
  --json on any command; fr COMMAND -h for its options. Details: scripts/fshy/README.md
"""


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="JSON output")
    common.add_argument("--repo", default=argparse.SUPPRESS, help="repository root (default: this checkout)")
    common.add_argument("--db", default=argparse.SUPPRESS, help="store path (default: the store of HEAD, REPO/.tmp/fshy/local-<HEAD 12>-s<F>.db)")
    common.add_argument("--width", type=int, default=argparse.SUPPRESS, help="clip cells at N characters; 0 = never")
    common.add_argument("--no-rebuild", action="store_true", default=argparse.SUPPRESS,
                        help="skip the staleness check (reads) or the rebuild after a write")
    ap = argparse.ArgumentParser(prog="fr", description=__doc__.split("\n")[0], parents=[common],
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=CLI_HELP)
    sub = ap.add_subparsers(dest="cmd", metavar="COMMAND")

    def sp(name, help_):
        return sub.add_parser(name, help=help_, parents=[common], description=help_)

    sp("help", "the primer: schema, vocabularies, rules, worked queries")
    p = sp("search", "names first, then BM25 full text")
    p.add_argument("q", nargs="+")
    p.add_argument("--topic")
    p.add_argument("--grp")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--include-duplicates", action="store_true")
    p = sp("filter", "whitelisted filters over record")
    p.add_argument("--topic")
    p.add_argument("--verdict", action="append", help="repeat or comma-separate")
    p.add_argument("--grp", action="append")
    p.add_argument("--confidence", action="append")
    p.add_argument("--no-card", action="store_true", help="needs_card=0 and identity stated")
    p.add_argument("--no-phone", action="store_true", help="needs_phone=0 and identity stated")
    p.add_argument("--anonymous", action="store_true")
    p.add_argument("--iface", help="substring of interfaces, e.g. s3")
    p.add_argument("--binding", action="append")
    p.add_argument("--crypto", action="store_true")
    p.add_argument("--max-usd-month", type=float)
    p.add_argument("--max-usd-tb", type=float)
    p.add_argument("--include-duplicates", action="store_true")
    p.add_argument("--sort", choices=SORTS, default="vorder")
    p.add_argument("--order", choices=["asc", "desc"], default="asc")
    p.add_argument("--keep-null", action="store_true", help="sorting on a price: list NULL rows last instead of excluding")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p = sp("get", "records by rid")
    p.add_argument("ids", nargs="+")
    p.add_argument("--detail", choices=["card", "full"], default="card")
    p.add_argument("--fields", help="card: record columns; full: path prefixes such as free_tier,egress")
    p.add_argument("--raw", action="store_true", help="the verbatim source JSON")
    p = sp("entity", "a vendor and its records")
    p.add_argument("id", nargs="+")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--offset", type=int, default=0)
    p = sp("need", "best-per-need lists")
    p.add_argument("id", nargs="?")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p = sp("sql", "guarded read-only SQL")
    p.add_argument("query", nargs="+")
    p.add_argument("--limit", type=int, default=50)
    p = sp("worklist", "work queues")
    p.add_argument("kind", choices=WORKLISTS)
    p.add_argument("--topic")
    p.add_argument("--as-of")
    p.add_argument("--forecast-days", type=int, default=0)
    p.add_argument("--class", dest="cls", help="worklist unknown: one class")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p = sp("evidence", "a record's evidence rows")
    p.add_argument("rid")
    p = sp("cites", "records whose evidence URL contains a string")
    p.add_argument("part")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--offset", type=int, default=0)
    p = sp("history", "ledger lines, history entries and commits of one record")
    p.add_argument("rid")
    p.add_argument("--limit", type=int, default=10)
    p = sp("verify", "rebuild the store when an input is newer; one line")
    p.add_argument("--force", action="store_true")
    p = sp("strip", "what the public projection removed")
    p.add_argument("action", choices=["report", "review"])
    p.add_argument("--rule")
    p.add_argument("--sample", type=int, default=10)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--topic")
    p.add_argument("--limit", type=int, default=50, help="report: rules shown")
    p.add_argument("--offset", type=int, default=0)

    def wr(p):
        p.add_argument("--dry-run", action="store_true", help="show the change, write nothing")

    p = sp("amend", "change one value of a record, with evidence")
    p.add_argument("rid")
    p.add_argument("path", help="$.free_tier.stated, $.limits[2].value, $.extras.\"NAT Start\".price")
    p.add_argument("value", help="parsed as JSON when it parses, else a string")
    p.add_argument("--evidence", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--proved", required=True)
    p.add_argument("--capture", help="sha256:... of the captured page (scripts/rq capture URL --lane .tmp/session-ID)")
    p.add_argument("--quote", help="the exact span of the capture that proves the value")
    p.add_argument("--rung", choices=list(reversed(LADDER)))
    p.add_argument("--reason")
    p.add_argument("--verified", action="store_true", help="set verified_at to the machine clock, UTC")
    p.add_argument("--string", action="store_true", help="take VALUE as a string even if it parses as JSON")
    wr(p)
    p = sp("add", "a new record skeleton with placeholders")
    p.add_argument("rid", metavar="TOPIC/SLUG")
    p.add_argument("--provider", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--proved", required=True)
    p.add_argument("--capture", help="sha256:... of the captured page (scripts/rq capture URL --lane .tmp/session-ID)")
    p.add_argument("--quote", help="the exact span of the capture that proves the value")
    p.add_argument("--rung", choices=list(reversed(LADDER)))
    p.add_argument("--verdict", choices=VERDICTS)
    p.add_argument("--category")
    p.add_argument("--reason")
    wr(p)
    p = sp("dead", "mark a record dead; nothing is deleted")
    p.add_argument("rid")
    p.add_argument("--cause", required=True, choices=CAUSES)
    p.add_argument("--observed", required=True, help="YYYY-MM-DD the death was observed")
    p.add_argument("--evidence", required=True)
    p.add_argument("--proved", required=True)
    p.add_argument("--capture", help="sha256:... of the captured page (scripts/rq capture URL --lane .tmp/session-ID)")
    p.add_argument("--quote", help="the exact span of the capture that proves the value")
    p.add_argument("--rung", choices=list(reversed(LADDER)))
    p.add_argument("--reason")
    wr(p)
    p = sp("relate", "record a relation in registry/relations.tsv")
    p.add_argument("src")
    p.add_argument("kind", choices=RELATIONS)
    p.add_argument("dst")
    p.add_argument("--evidence", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--reason", required=True)
    wr(p)
    p = sp("entity-set", "pin a record to an entity in registry/entities.tsv")
    p.add_argument("rid")
    p.add_argument("eid")
    p.add_argument("--name")
    p.add_argument("--reason", required=True)
    wr(p)
    sp("mcp", "stdio MCP server: help, search, filter, get, entity, need, sql, worklist")
    return ap


READS = {"help", "search", "filter", "get", "entity", "need", "sql", "worklist", "evidence", "cites", "history",
         "strip"}
WRITES = {"amend": cmd_amend, "add": cmd_add, "dead": cmd_dead, "relate": cmd_relate, "entity-set": cmd_entity_set}


def run(argv):
    ap = build_parser()
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code in (0, None) else 2
    args.json = getattr(args, "json", False)
    args.repo = os.path.abspath(getattr(args, "repo", DEFAULT_REPO))
    args.db_explicit = bool(getattr(args, "db", None))
    args.db_path = store_path(args.repo, getattr(args, "db", None))
    args.width = getattr(args, "width", 80)
    args.no_rebuild = getattr(args, "no_rebuild", False)
    if not args.cmd:
        ap.print_help()
        return 2
    if args.cmd == "mcp":
        serve_mcp(args.repo, args.db_path if args.db_explicit else None, sys.stdin, sys.stdout)
        return 0
    if args.cmd == "verify":
        if args.force and not args.db_explicit and research_checkout(args.repo):
            # a forced build would make a second store of HEAD and delete the one every agent reads (W-13)
            sys.stderr.write("fr: verify --force is refused in the research checkout: its store is built once, by the merge "
                             "session's scripts/rq sync (AGENTS.md section 2 rule 14)\n")
            return 2
        out, ok = op_verify(args.repo, args.db_path, args.force, explicit=args.db_explicit)
        sys.stdout.write(render(out, args.json, args.width))
        return 0 if ok else 1
    if args.cmd in WRITES:
        if research_checkout(args.repo):
            raise Fail(WRITE_REFUSAL, 2)
        out = WRITES[args.cmd](args)
        sys.stdout.write(render(out, args.json, args.width))
        return 0
    if args.db_explicit:
        if not args.no_rebuild:
            ensure_fresh(args.repo, args.db_path)
    elif not args.no_rebuild or not os.path.exists(args.db_path):
        args.db_path = ensure_store(args.repo, quiet=False)
    st = Store(args.db_path, args.repo)
    try:
        c = args.cmd
        if c == "help":
            out = Text(primer.text(args.db_path) + CLI_HELP)
        elif c == "search":
            out = op_search(st, args.q, args.topic, args.grp, args.limit, args.offset, args.include_duplicates)
        elif c == "filter":
            out = op_filter(st, args.topic, args.verdict, args.grp, args.confidence, args.no_card, args.no_phone,
                            args.anonymous, args.iface, args.binding, args.crypto, args.max_usd_month, args.max_usd_tb,
                            args.include_duplicates, args.sort, args.order, args.limit, args.offset, args.keep_null)
        elif c == "get":
            out = op_get(st, args.ids, args.detail, args.fields, args.raw)
        elif c == "entity":
            out = op_entity(st, args.id, args.limit, args.offset)
        elif c == "need":
            out = op_need(st, args.id, args.limit, args.offset)
        elif c == "sql":
            out = op_sql(st, args.query, args.limit)
        elif c == "worklist":
            out = op_worklist(st, args.kind, args.topic, args.as_of, args.forecast_days, args.limit, args.offset,
                              args.cls)
        elif c == "evidence":
            out = op_evidence(st, check_rid(args.rid))
        elif c == "cites":
            out = op_cites(st, args.part, args.limit, args.offset)
        elif c == "history":
            out = op_history(st, check_rid(args.rid), args.limit)
        else:
            out = op_strip(st, args.action, args.rule, args.sample, args.seed, args.topic, args.limit, args.offset)
    finally:
        st.close()
    sys.stdout.write(render(out, args.json, args.width))
    return 0


def main(argv=None):
    global _MEMO
    _MEMO = {}
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace", newline="\n")
        except (AttributeError, ValueError):
            pass
    try:
        sys.stdin.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        return run(sys.argv[1:] if argv is None else argv)
    except Fail as e:
        sys.stderr.write("fr: %s\n" % e)
        return e.code if e.code in (1, 2) else 1
    except BrokenPipeError:
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
