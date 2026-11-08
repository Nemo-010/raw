"""State shared by every research process on this machine, in one SQLite file, .tmp/rq/state.db (never committed):
write leases with fencing numbers, the registry of the top-level id folders under .tmp/, the records a live run
created, the drain and wipe rows of a merge session, the local claims of rq:research issues, and the facts a checkout
learns once (the repository's labels). SQLite's own locking makes it safe across processes on Windows, Linux and
macOS.

Every transaction is short: no network call, no file walk and no subprocess inside one. There is no request bucket
and no rate here: the harness sets no client-side cap (AGENTS.md section 2 rule 15).
"""
import json
import os
import sqlite3

from common import SETTINGS, Fail, now_ts, rq_home, stamp

LEASE_HOURS = SETTINGS["lease_hours"]

DRAIN_LINE = ("a merge session is draining .tmp/ for a wipe since %s: open no new run; finish and land the run you "
              "have, then stop (AGENTS.md section 2 rule 8)")


def connect(repo):
    """One connection per state file per process, reused, so that close_all can close it."""
    path = os.path.join(rq_home(repo), "state.db")
    db = _OPEN.get(path)
    if db is not None:
        if db.in_transaction:
            db.execute("ROLLBACK")
        return db
    os.makedirs(rq_home(repo), exist_ok=True)
    db = sqlite3.connect(path, timeout=30, isolation_level=None)
    db.execute("PRAGMA journal_mode=WAL")
    db.executescript("""
CREATE TABLE IF NOT EXISTS lease (key TEXT PRIMARY KEY, run TEXT NOT NULL, unit TEXT NOT NULL,
  fence INTEGER NOT NULL, expires REAL NOT NULL, kind TEXT NOT NULL DEFAULT 'work');
CREATE TABLE IF NOT EXISTS fence (n INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS folder (id TEXT PRIMARY KEY, kind TEXT NOT NULL, created TEXT NOT NULL, holder TEXT,
  ended TEXT);
CREATE TABLE IF NOT EXISTS pending_new (run TEXT NOT NULL, rid TEXT NOT NULL, topic TEXT, domain TEXT, core TEXT,
  slug TEXT, urls TEXT, tier TEXT, PRIMARY KEY (run, rid));
CREATE TABLE IF NOT EXISTS control (what TEXT PRIMARY KEY, pid INTEGER, at TEXT, who TEXT);
CREATE TABLE IF NOT EXISTS claim (issue INTEGER NOT NULL, run TEXT NOT NULL, topic TEXT, at REAL NOT NULL,
  PRIMARY KEY (issue, run));
CREATE TABLE IF NOT EXISTS memo (key TEXT PRIMARY KEY, value TEXT, at TEXT);
""")
    cols = {r[1] for r in db.execute("PRAGMA table_info(lease)")}
    if "kind" not in cols:
        db.execute("ALTER TABLE lease ADD COLUMN kind TEXT NOT NULL DEFAULT 'work'")
    if "tier" not in {r[1] for r in db.execute("PRAGMA table_info(pending_new)")}:
        # a state file of an older harness: its pending rows name no tier, and a row with no tier decides nothing. Two
        # processes that open it at once both see no column, and the second ALTER finds the first one's
        try:
            db.execute("ALTER TABLE pending_new ADD COLUMN tier TEXT")
        except sqlite3.OperationalError as e:
            if "duplicate column" not in str(e).lower():
                raise
    if db.execute("SELECT count(*) FROM fence").fetchone()[0] == 0:
        db.execute("INSERT INTO fence VALUES (0)")
    _OPEN[path] = db
    return db


_OPEN = {}


def close_all():
    """Close every state connection this process opened. An open one holds state.db, and on Windows a folder that
    holds an open file cannot be renamed or removed (the wipe, the selftest's clone)."""
    while _OPEN:
        try:
            _OPEN.popitem()[1].close()
        except Exception:
            pass


class Tx:
    """BEGIN IMMEDIATE ... COMMIT, rolled back on an exception."""

    def __init__(self, repo):
        self.db = connect(repo)

    def __enter__(self):
        self.db.execute("BEGIN IMMEDIATE")
        return self.db

    def __exit__(self, kind, *a):
        self.db.execute("ROLLBACK" if kind else "COMMIT")


def control(repo, what):
    """The drain or wiping row: (pid, at, who), or None."""
    return connect(repo).execute("SELECT pid, at, who FROM control WHERE what = ?", (what,)).fetchone()


def _refuse_if(db, drain=True):
    w = db.execute("SELECT pid, at FROM control WHERE what = 'wiping'").fetchone()
    if w:
        raise Fail("a merge session is wiping .tmp/ (pid %s since %s); nothing can be created or leased now" % w, 1)
    if drain:
        d = db.execute("SELECT at FROM control WHERE what = 'drain'").fetchone()
        if d:
            raise Fail(DRAIN_LINE % d[0], 1)


def register_folder(repo, fid, kind, holder="", drain=True):
    """Register a top-level id folder of .tmp/ (a run, a session, a merge session's review folder), in the same
    transaction that checks for a drain or a wipe: either the wipe sees the new folder or the new folder sees the wipe."""
    with Tx(repo) as db:
        _refuse_if(db, drain)
        db.execute("INSERT OR IGNORE INTO folder (id, kind, created, holder) VALUES (?,?,?,?)", (fid, kind, stamp(), holder))


def end_folder(repo, fid):
    connect(repo).execute("UPDATE folder SET ended = ? WHERE id = ?", (stamp(), fid))


def take_folder(repo, fid, holder):
    connect(repo).execute("UPDATE folder SET holder = ?, ended = NULL WHERE id = ?", (holder, fid))


def folders(repo, kind=None):
    q = "SELECT id, kind, created, holder, ended FROM folder" + (" WHERE kind = ?" if kind else "") + " ORDER BY created"
    return connect(repo).execute(q, (kind,) if kind else ()).fetchall()


def lease_keys(unit):
    """The write scope of a unit as lease keys. Two units whose keys intersect cannot run at once."""
    sc = unit.get("scope") or {}
    keys = ["rid:" + r for r in sc.get("rids") or []]
    new = sc.get("new") or {}
    topic = new.get("topic") or unit.get("topic")
    for n in new.get("names") or []:
        keys.append("name:%s:%s" % (topic, " ".join(n.lower().split())))
    if new.get("slice"):
        keys.append("slice:%s:%s" % (topic, new["slice"].strip().lower()))
    return sorted(set(keys))


def acquire(repo, run, unit, done_units=()):
    """Grant every key of the unit's scope or none. -> fence number. Raises Fail naming the holder. A key held by a
    unit of the same run that is done (integrated, reverted, abandoned: done_units) moves to this unit: a reconcile
    unit settles the records of its own run. A work lease expires after lease_hours; a held lease (an integrated unit,
    hold_unit) and a review lease (a landed run) hold until the merge or the close (G5-02)."""
    fence, foreign = relet(repo, run, unit, done_units)
    if foreign:
        raise Fail("scope %s; drop it from this unit or wait" % holder_text(foreign[0]))
    return fence


def holder_text(row):
    """'KEY is leased by run R unit U (why)' for a (key, run, unit, kind) row of relet."""
    return "%s is leased by run %s unit %s%s" % (row[0], row[1], row[2], {
        "review": " (in review until its pull request is merged or closed)",
        "held": " (integrated: held until that run merges or closes)"}.get(row[3], ""))


def relet(repo, run, unit, done_units=()):
    """acquire, without the raise: every key of the unit's scope or none. -> (fence, []) when granted, or
    (None, [(key, run, unit, kind)]) naming each key that another run, or a unit of this run that is not done, holds.
    integrate calls it for a unit whose work lease expired while its lane worked (a lane that outlived lease_hours:
    HTTP 429 pauses): a key that nobody took is let again to the same unit, and its finished work is kept."""
    keys = lease_keys(unit)
    now = now_ts()
    with Tx(repo) as db:
        _refuse_if(db, drain=False)
        db.execute("DELETE FROM lease WHERE kind = 'work' AND expires < ?", (now,))
        foreign = []
        for k in keys:
            row = db.execute("SELECT run, unit, kind FROM lease WHERE key = ?", (k,)).fetchone()
            if row and not (row[0] == run and (row[1] == unit["id"] or row[1] in done_units)):
                foreign.append((k,) + tuple(row))
        if foreign:
            return None, foreign
        db.execute("UPDATE fence SET n = n + 1")
        fence = db.execute("SELECT n FROM fence").fetchone()[0]
        for k in keys:
            db.execute("INSERT OR REPLACE INTO lease (key, run, unit, fence, expires, kind) VALUES (?,?,?,?,?,'work')",
                       (k, run, unit["id"], fence, now + LEASE_HOURS * 3600))
    return fence, []


def add_keys(repo, run, uid, keys, fence):
    """Lease keys to an integrated unit: the records it created (rid: keys), or its own scope again, so another run
    cannot change them before this run merges. A key that another run holds is never taken over: it is returned, and
    the caller logs a conflict (G2-09). The lease is a held one, which does not expire with time (G5-02); a run in
    review keeps review leases. -> [(key, holder run, holder unit)] of the keys not leased."""
    now = now_ts()
    foreign = []
    with Tx(repo) as db:
        db.execute("DELETE FROM lease WHERE kind = 'work' AND expires < ?", (now,))
        review = db.execute("SELECT 1 FROM lease WHERE run = ? AND kind = 'review' LIMIT 1", (run,)).fetchone()
        kind = "review" if review else "held"
        for k in keys:
            row = db.execute("SELECT run, unit FROM lease WHERE key = ?", (k,)).fetchone()
            if row and row[0] != run:
                foreign.append((k, row[0], row[1]))
                continue
            db.execute("INSERT OR REPLACE INTO lease (key, run, unit, fence, expires, kind) VALUES (?,?,?,?,?,?)",
                       (k, run, uid, fence or 0, now + LEASE_HOURS * 3600, kind))
    return foreign


def hold_unit(repo, run, uid):
    """integrate: the work lease of a unit that is now integrated becomes a held lease, which lasts until the run
    merges or closes, not lease_hours after the plan; a run that lands a day after its plan still holds what its open
    pull request changes (G5-02)."""
    connect(repo).execute("UPDATE lease SET kind = 'held' WHERE run = ? AND unit = ? AND kind = 'work'", (run, uid))


def holds(repo, run, unit):
    """True when every key of the unit is still leased to this run and unit with the unit's fence."""
    keys = lease_keys(unit)
    if not keys:
        return True
    db = connect(repo)
    now = now_ts()
    for k in keys:
        row = db.execute("SELECT run, unit, fence, expires, kind FROM lease WHERE key = ?", (k,)).fetchone()
        if not row or row[0] != run or row[1] != unit["id"] or row[2] != unit.get("fence") or \
                (row[4] == "work" and row[3] < now):
            return False
    return True


def holder(repo, key):
    """(run, unit, kind) of a live lease on key, or None."""
    db = connect(repo)
    row = db.execute("SELECT run, unit, kind, expires FROM lease WHERE key = ?", (key,)).fetchone()
    if not row or (row[2] == "work" and row[3] < now_ts()):
        return None
    return row[:3]


def to_review(repo, run):
    """land: the run's leases become review leases, which do not expire with time. land leases the keys of every
    integrated unit again first (add_keys), so a key whose work lease expired is held again here (G5-02)."""
    connect(repo).execute("UPDATE lease SET kind = 'review' WHERE run = ?", (run,))


def release(repo, run):
    """The run's leases and its pending new records go (a merge, a close, a cleanup)."""
    with Tx(repo) as db:
        db.execute("DELETE FROM lease WHERE run = ?", (run,))
        db.execute("DELETE FROM pending_new WHERE run = ?", (run,))


def release_unit(repo, run, uid):
    connect(repo).execute("DELETE FROM lease WHERE run = ? AND unit = ?", (run, uid))


def leases(repo, live=True):
    """(key, run, unit, fence, expires, kind) rows; live=True leaves out work leases that have expired (a held and a
    review lease do not expire)."""
    rows = connect(repo).execute("SELECT key, run, unit, fence, expires, kind FROM lease ORDER BY run, unit").fetchall()
    now = now_ts()
    return [r for r in rows if not live or r[5] != "work" or r[4] >= now]


def add_pending(repo, run, rid, topic, domain, core, slug, urls, tier=None):
    connect(repo).execute("INSERT OR REPLACE INTO pending_new (run, rid, topic, domain, core, slug, urls, tier) "
                          "VALUES (?,?,?,?,?,?,?,?)", (run, rid, topic, domain, core, slug, json.dumps(sorted(urls)), tier))


def pending(repo, topic=None, other_than=None):
    """Records that a live run created and that main does not have yet: (run, rid, topic, domain, core, slug, urls,
    tier), tier None when the record names none."""
    q = "SELECT run, rid, topic, domain, core, slug, urls, tier FROM pending_new"
    args, cond = [], []
    if topic:
        cond.append("topic = ?")
        args.append(topic)
    if other_than:
        cond.append("run <> ?")
        args.append(other_than)
    rows = connect(repo).execute(q + (" WHERE " + " AND ".join(cond) if cond else ""), args).fetchall()
    return [r[:6] + (json.loads(r[6] or "[]"), r[7]) for r in rows]


def set_control(repo, what, who=""):
    connect(repo).execute("INSERT OR REPLACE INTO control VALUES (?,?,?,?)", (what, os.getpid(), stamp(), who))


def clear_control(repo, what):
    connect(repo).execute("DELETE FROM control WHERE what = ?", (what,))


def claims(repo, issue):
    """The local claims of an rq:research issue: (run, topic, at) of each run of this checkout that claimed it. The
    claim lock of the issue and topic (track.claim) is held while one is added, so two sessions of this checkout
    cannot both claim one topic of one issue."""
    return connect(repo).execute("SELECT run, topic, at FROM claim WHERE issue = ? ORDER BY at", (issue,)).fetchall()


def add_claim(repo, issue, run, topic):
    connect(repo).execute("INSERT OR REPLACE INTO claim (issue, run, topic, at) VALUES (?,?,?,?)",
                          (issue, run, topic, now_ts()))


def drop_claim(repo, issue, run=None):
    """A claim given back: of one run, or of every run of this checkout (run None)."""
    if run:
        connect(repo).execute("DELETE FROM claim WHERE issue = ? AND run = ?", (issue, run))
    else:
        connect(repo).execute("DELETE FROM claim WHERE issue = ?", (issue,))


def memo(repo, key):
    """A fact this checkout learned once and keeps until a wipe (the labels of the GitHub repository). -> value or None."""
    row = connect(repo).execute("SELECT value FROM memo WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def set_memo(repo, key, value):
    connect(repo).execute("INSERT OR REPLACE INTO memo (key, value, at) VALUES (?,?,?)", (key, value, stamp()))


def drop_memo(repo, key):
    connect(repo).execute("DELETE FROM memo WHERE key = ?", (key,))
