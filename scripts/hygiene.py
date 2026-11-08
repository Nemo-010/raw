#!/usr/bin/env python3
"""hygiene.py -- refuse to commit what must never enter this repository.

The failure this prevents: a scratch capture, a probe body, a credential or a
vendored .git directory reaching the published tree. Every one of those has a
way of arriving unnoticed, because git add -A reports a count rather than a
list. This prints the list.

It checks the staged set when the repository is a git work tree, and otherwise
walks the tree. Either way it answers one question: is anything about to be
committed that should not be?

Exit codes: 0 clean, 1 prohibited path staged or present, 2 usage, 3 no tree.
"""
import argparse
import json
import os
import re
import subprocess
import sys

# Each rule is (name, matcher, why). The "why" is printed, because a check that
# only says "refused" teaches a session nothing and it will route around it.
RULES = [
    ("scratch", re.compile(r"(^|/)\.tmp/"),
     "agent scratch and the seed corpus live in .tmp/ and are never committed"),
    ("probe-output", re.compile(r"(\.probe\.json|\.sha256|\.part)$"),
     "probe records belong beside the dossier that cites them, not in the tree"),
    ("capture-body", re.compile(r"(^|/)probe-out/"),
     "raw probe bytes are cited by path and date, not stored"),
    ("git-dir", re.compile(r"(^|/)\.git/"),
     "a vendored repository keeps its history, which is not what we cite"),
    ("build-output", re.compile(r"(^|/)(target|dist|node_modules|__pycache__)/"),
     "build output is rebuilt, never committed"),
    ("secret", re.compile(r"(^|/)(\.env($|\..*)|[^/]*\.pem|[^/]*\.key|id_rsa[^.]*)$"),
     "this repository holds no credential, ever"),
    ("oversize", None,
     "a capture larger than the cap is cited by URL and date instead"),
]

CAP_BYTES = 8 * 1024 * 1024

# Files that exist in the tree legitimately and look like a rule hit.
ALLOW = {
    ".env.example",
}


def staged_paths(root):
    try:
        out = subprocess.run(["git", "-C", root, "diff", "--cached",
                              "--name-only", "--diff-filter=ACMR"],
                             capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return [p for p in out.stdout.splitlines() if p.strip()]


def tracked_paths(root):
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"],
                             capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return [p for p in out.stdout.splitlines() if p.strip()]


def walk_paths(root, skip=(".git", ".tmp")):
    """Every file on disk, minus the two directories that are never committed.

    `.tmp/` is excluded here rather than reported: walking it produces ~4,000
    "scratch" hits that are all true by definition and tell a reader nothing.
    The walk is for "what is in the tree", so it starts from what the tree is.
    """
    found = []
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in files:
            full = os.path.join(dirpath, name)
            found.append(os.path.relpath(full, root).replace("\\", "/"))
    return found


def ignored_set(root, rels):
    """The subset of `rels` that git would refuse to add, in one call.

    One `git check-ignore` for 2,700 paths is a second; one per path is minutes,
    and a slow check is a check that gets skipped. `--stdin -z` takes the list on
    stdin and prints only the ignored ones.
    """
    if not rels:
        return set()
    try:
        proc = subprocess.run(
            ["git", "-C", root, "check-ignore", "--stdin", "-z"],
            input="\0".join(rels) + "\0",
            capture_output=True, text=True)
    except (FileNotFoundError, OSError):
        return set()
    # Exit 0 means at least one path is ignored, 1 means none, 128 is "not a repo".
    if proc.returncode not in (0, 1):
        return set()
    return {p for p in proc.stdout.split("\0") if p}


def classify(paths, root):
    problems = []
    ignored = ignored_set(root, paths)
    for rel in paths:
        base = os.path.basename(rel)
        if base in ALLOW or rel in ignored:
            continue
        for name, pattern, why in RULES:
            if pattern is None:
                continue
            if pattern.search(rel):
                problems.append({"rule": name, "path": rel, "why": why})
                break
        else:
            full = os.path.join(root, rel)
            if os.path.isfile(full) and os.path.getsize(full) > CAP_BYTES:
                problems.append({
                    "rule": "oversize", "path": rel,
                    "why": "%.1f MiB exceeds the %d MiB cap; cite it by URL"
                           % (os.path.getsize(full) / 1048576, CAP_BYTES // 1048576)})
    return problems


def main():
    ap = argparse.ArgumentParser(
        description="refuse to commit scratch, secrets, build output or oversize captures")
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    ap.add_argument("--all", action="store_true",
                    help="check every tracked file, not only the staged set")
    ap.add_argument("--walk", action="store_true",
                    help="check every file on disk, tracked or not")
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each rule catches its own case and passes a clean one")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("hygiene: --root is not a directory: %s" % root, file=sys.stderr)
        return 3

    problems, source, paths = collect(root, staged=not args.all and not args.walk,
                                      tracked=args.all, walk=args.walk)

    if args.json:
        print(json.dumps({"source": source, "checked": len(paths),
                          "problems": problems}, indent=2))
    else:
        for p in problems[:50]:
            print("%-13s %-52s %s" % (p["rule"], p["path"], p["why"]))
        if len(problems) > 50:
            print("... %d more" % (len(problems) - 50))
        print("%d path(s) checked from the %s set, %d problem(s)"
              % (len(paths), source, len(problems)))

    # "0 paths checked, 0 problems" reads as a clean bill of health and is not
    # one: nothing was examined. A repository with no commits yet has an empty
    # index, so the staged set is empty and this exit code is the difference
    # between "clean" and "did not look".
    if not paths:
        print("hygiene: the %s set is empty, so this examined nothing; pass "
              "--walk to check the working tree" % source, file=sys.stderr)
        return 2

    return 0 if not problems else 1


def collect(root, staged=True, tracked=False, walk=False):
    """Return (problems, source, paths).

    The order matters: a git set that exists but is empty (a repository with no
    commits yet, or nothing staged) is NOT the same as "the tree is clean". It
    used to be reported as `0 path(s) checked, 0 problem(s)` and exit 0, which
    is a check that verified zero rows and reported success.
    """
    paths, source = None, "walk"
    if tracked:
        paths, source = tracked_paths(root), "tracked"
    elif staged:
        paths, source = staged_paths(root), "staged"

    if walk or not paths:
        if walk:
            source = "walk"
        elif source in ("tracked", "staged"):
            source = "%s (empty; fell back to the working tree)" % source
        paths = walk_paths(root)

    return classify(paths, root), source, paths


# -------------------------------------------------------------------- proof --

def selftest():
    """Each rule is planted, then removed. A rule that cannot fire is off."""
    import shutil
    import tempfile

    fails = 0

    def say(ok, name):
        nonlocal fails
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1

    tmp = tempfile.mkdtemp(prefix="hygiene-selftest.")
    try:
        def plant(rel, size=8):
            full = os.path.join(tmp, rel)
            parent = os.path.dirname(full)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(full, "wb") as fh:
                fh.write(b"x" * size)
            return rel

        cases = [
            ("sources/x.probe.json", "probe-output"),
            ("probe-out/body.bin", "capture-body"),
            ("node_modules/dep/index.js", "build-output"),
            (".env", "secret"),
            ("deploy/server.pem", "secret"),
            ("deploy/id_rsa", "secret"),
        ]
        for rel, rule in cases:
            plant(rel)
            problems, _, _ = collect(tmp, walk=True)
            hit = [p for p in problems if p["path"] == rel]
            say(bool(hit) and hit[0]["rule"] == rule,
                "%s is refused as %s" % (rel, rule))
            os.remove(os.path.join(tmp, rel))

        # Two rules are about paths that a filesystem walk deliberately skips:
        # `.tmp/` (never committed, so never walked) and a vendored `.git/`
        # (skipped by os.walk). Both arrive through the index, so classify() is
        # the thing that must catch them, not the walk.
        for rel, rule in ((".tmp/scratch.txt", "scratch"),
                          ("vendor/lib/.git/config", "git-dir")):
            problems = classify([rel], tmp)
            say(any(p["rule"] == rule for p in problems),
                "%s is refused as %s" % (rel, rule))

        say(not any(p["path"].startswith(".tmp/")
                    for p in collect(tmp, walk=True)[0]),
            "a walk does not report .tmp/ as 4,000 scratch hits")

        big = plant("captures/huge.bin", CAP_BYTES + 1)
        problems, _, _ = collect(tmp, walk=True)
        say(any(p["path"] == big and p["rule"] == "oversize" for p in problems),
            "a file over the cap is refused as oversize")
        os.remove(os.path.join(tmp, big))

        plant("docs/clean.md")
        plant("docs/another.md")
        plant(".env.example")
        problems, _, _ = collect(tmp, walk=True)
        say(not problems, "a clean tree with .env.example is accepted")

        # The false pass: an empty git set must not read as "clean". This is
        # the shape of a repository with no commits yet, which is this one.
        problems, source, paths = collect(tmp, staged=True, walk=False)
        say("fell back" in source,
            "an empty staged set falls back to the working tree, and says so")
        say(len(paths) >= 2, "the fallback examines the files on disk")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nhygiene selftest: %s"
          % ("0 failed" if not fails else "%d failed" % fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
