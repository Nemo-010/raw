"""rq import-bundle: apply a contributor's run folder, received as a zip, onto a fresh run branch.

The bundle is data. Nothing in it is executed: the archive is read with zipfile, every member is checked
for a path that leaves the staging directory and for a suffix that is not data, and the records are
validated by the same lint and compare-and-set that `rq integrate` uses. The operator's checkout runs every
script; the staging directory holds only JSON and the lane's text.
"""
import hashlib
import json
import os
import shutil
import zipfile

import integrate
import units
from common import Fail, REPO, run_dir, stamp

DATA_SUFFIXES = (".json", ".jsonl", ".md", ".txt", ".tsv", ".csv", ".html", ".xml", ".yaml", ".yml")
# the harness's own files in a run folder: a contributor's copy of .tmp/<run>/ carries them, they hold no work, and
# a run that imports them would inherit a stale lock
TRANSIENT = ("lock", "lock.holder")


def _safe(member):
    """-> ("data", name), ("skip", name) for a transient file of the run folder, or ("refuse", name)."""
    name = member.filename.replace("\\", "/")
    if not name or name.endswith("/"):
        return "refuse", name
    if name.startswith("/") or ":" in name.split("/")[0]:
        return "refuse", name
    parts = name.split("/")
    if any(p in ("", ".", "..") for p in parts):
        return "refuse", name
    if parts[-1] in TRANSIENT:
        return "skip", name
    if not name.lower().endswith(DATA_SUFFIXES):
        return "refuse", name
    return "data", name


def extract(path, dest):
    """Extract the data members of the zip into dest, refusing a path that leaves it or a file that is not data.
    The run folder's lock files are skipped: they are the harness's, not the contributor's work.
    -> the number of members written."""
    n = 0
    with zipfile.ZipFile(path) as zf:
        for m in zf.infolist():
            if m.is_dir() or m.filename.endswith("/"):
                continue
            what, name = _safe(m)
            if what == "skip":
                continue
            if what == "refuse":
                raise Fail("the bundle carries %r, which is not a data file or does not stay inside the staging "
                           "directory. A bundle holds .json, .jsonl, .md, .txt, .tsv, .csv, .html, .xml or .yaml; "
                           "nothing in it is executed" % m.filename, 1)
            target = os.path.join(dest, *name.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zf.open(m) as src, open(target, "wb") as out:
                shutil.copyfileobj(src, out)
            n += 1
    return n


def find_run(stage):
    """The directory that holds run.json: the one directory of the staging tree that has it. A zip of .tmp/<run>/
    keeps the .tmp/ prefix, so the search is recursive; exactly one run.json is required."""
    found = sorted(root for root, _dirs, names in os.walk(stage) if "run.json" in names)
    if len(found) == 1:
        return found[0]
    if not found:
        raise Fail("the bundle has no run.json; a bundle is the folder .tmp/<run>/ of a run, zipped", 1)
    raise Fail("the bundle carries %d run.json files (%s); one bundle is one run"
               % (len(found), ", ".join(os.path.relpath(p, stage) for p in found[:4])), 1)


def import_bundle(path, repo=REPO):
    """-> (run id, report lines). The bundle's units are applied to a new run branch by the same integrator a run
    uses; the records are validated by the lint and the compare-and-set of that integrator."""
    if not os.path.isfile(path):
        raise Fail("no bundle at %s" % path, 2)
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()[:12]
    stage = os.path.join(repo, ".tmp", "imports", digest)
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage, exist_ok=True)
    n = extract(path, stage)
    root = find_run(stage)
    r = json.load(open(os.path.join(root, "run.json"), encoding="utf-8"))
    kind, topic, request = r.get("kind"), r.get("topic"), (r.get("request") or "").strip()
    if kind not in units.RUN_KINDS:
        raise Fail("the bundle's run.json names kind %r, not one of %s" % (kind, ", ".join(units.RUN_KINDS)), 1)
    if topic not in units.topics(repo):
        raise Fail("the bundle's run.json names topic %r, not one of %s" % (topic, ", ".join(units.topics(repo))), 1)
    if not request:
        raise Fail("the bundle's run.json carries no request", 1)
    new = units.open_run(kind, topic, request + " (imported bundle %s)" % digest, repo, no_issue=True)
    run = new["run"]
    src = os.path.join(root, "units")
    dst = os.path.join(run_dir(run, repo), "units")
    os.makedirs(dst, exist_ok=True)
    copied = 0
    for uid in sorted(os.listdir(src)) if os.path.isdir(src) else []:
        s = os.path.join(src, uid)
        if not os.path.isdir(s):
            continue
        d = os.path.join(dst, uid)
        shutil.copytree(s, d)
        up = os.path.join(d, "unit.json")
        if os.path.exists(up):
            u = json.load(open(up, encoding="utf-8"))
            u["run"] = run
            u["status"] = "ready"
            u.pop("attempt", None)
            units.save_unit(u, repo)
        copied += 1
    report, conflicts = integrate.integrate(run, repo)
    lines = ["imported %d file(s) from %s into run %s" % (n, os.path.basename(path), run),
             "applied %d unit(s); %d conflict(s)" % (copied, len(conflicts))]
    for uid, status, tally, rejects in report:
        lines.append("  %s: %s%s%s" % (uid, status,
                                        " (%s)" % ", ".join("%s %s" % (k, v) for k, v in sorted(tally.items())) if tally else "",
                                        "; %d reject(s)" % rejects if rejects else ""))
    lines.append("next: scripts/rq land %s" % run)
    return run, lines
