#!/usr/bin/env python3
"""Diff a research source against the dossier, and fail when a source goes stale.

WHY THIS EXISTS
    The corpus missed an entire market because nobody diffed a provider list
    against the records. One aggregator was read, 128 providers were diffed, and
    the conclusion "the names are known" was drawn from a list that did not
    contain half the market. A note saying "check more lists" is the failure mode.
    This is the machine-readable list plus the check that makes forgetting it
    impossible: every registered source carries a cadence and a last diff date,
    and the gate fails when one is overdue or still pending.

WHAT A SOURCE IS
    kind=provider-index   a site that links to many providers (vpspricetracker, serverhunter)
    kind=offer-feed       a feed of individual offers (lowendbox, lowendtalk, zhujiceping)
    kind=price-index      a site that publishes rates rather than hosts (computeprices)
    kind=corpus           a repository of provider cards (battleships)

    A source is diffed two ways. `--diff` extracts provider names from a saved
    page with the row's regex and compares them with dossier/compute; use it when
    the page links providers. `--record` takes counts a person or an agent
    established by reading, for feeds whose names are in prose rather than links.

USAGE
    python scripts/sources/aggregator-diff.py --check
    python scripts/sources/aggregator-diff.py --diff vpspricetracker --html .tmp/session-<id>/vpt-prov.html --update
    python scripts/sources/aggregator-diff.py --record lowendbox --covered 41 --missing 7
    python scripts/sources/aggregator-diff.py --selftest

EXIT CODES
    0  check passed, or the requested diff ran
    1  a source is overdue, pending, or absent from the watchlist
    2  usage
    3  environment: registry or dossier unreadable
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys

FIELDS = ["slug", "url", "kind", "cadence_days", "last_diff", "covered",
          "missing", "pattern", "status", "note", "topic"]
KINDS = ("provider-index", "offer-feed", "price-index", "corpus")
# A registry file names its topic in every row, because a tunnel list and a
# compute list are diffed against different watchlists. A row without a topic
# predates the column and belongs to compute, which is where the registry began.
DEFAULT_TOPIC = "compute"


def repo_root(explicit: str | None = None) -> str:
    if explicit:
        return os.path.abspath(explicit)
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(here))


def load(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if i == 0 or parts[0] == "slug":
                continue
            parts += [""] * (len(FIELDS) - len(parts))
            rows.append(dict(zip(FIELDS, parts[:len(FIELDS)])))
    return rows


def save(path: str, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(FIELDS) + "\n")
        for r in rows:
            fh.write("\t".join(r.get(f, "") for f in FIELDS) + "\n")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def dossier_index(dossier: str) -> tuple[set[str], list[str]]:
    slugs, providers = set(), []
    for topic in sorted(os.listdir(dossier)):
        tdir = os.path.join(dossier, topic)
        if not os.path.isdir(tdir):
            continue
        for name in os.listdir(tdir):
            if not name.endswith(".json"):
                continue
            slugs.add(norm(name[:-5]))
            providers.append(norm(name[:-5]))
    return slugs, providers


def missing_names(names: list[str], known: set[str]) -> list[str]:
    """A name is covered when its normalized form matches a slug, or when one
    contains the other and the shorter is at least five characters. The five-char
    floor is what stops 'vps1' matching every slug that contains it."""
    out = []
    for n in names:
        k = norm(n)
        if not k:
            continue
        if k in known:
            continue
        hit = any((len(k) >= 5 and k in s) or (len(s) >= 5 and s in k) for s in known)
        if not hit:
            out.append(n)
    return out


def names_from_html(html: str, pattern: str) -> list[str]:
    rx = re.compile(pattern)
    seen, out = set(), []
    for m in rx.finditer(html):
        val = m.group(1) if m.groups() else m.group(0)
        val = val.strip().strip("/").split("/")[0]
        if val and val.lower() not in seen:
            seen.add(val.lower())
            out.append(val)
    return out


def cmd_check(args, rows: list[dict]) -> int:
    today = dt.date.fromisoformat(args.today)
    root = repo_root(args.root)
    watch_cache: dict[str, str] = {}

    def watch_text(topic: str) -> str:
        if topic not in watch_cache:
            path = os.path.join(root, "docs", topic, "watchlist.md")
            watch_cache[topic] = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        return watch_cache[topic]

    problems, pending, active = [], 0, 0
    retired = 0
    topics = set()
    for r in rows:
        slug, status = r["slug"], (r.get("status") or "").strip()
        topic = (r.get("topic") or "").strip() or DEFAULT_TOPIC
        topics.add(topic)
        if status == "retired":
            retired += 1
            continue
        if status == "pending":
            pending += 1
            problems.append(f"{slug}: pending, never diffed")
            continue
        if status != "active":
            problems.append(f"{slug}: unknown status '{status}'")
            continue
        active += 1
        try:
            last = dt.date.fromisoformat(r["last_diff"])
            cadence = int(r["cadence_days"])
        except ValueError:
            problems.append(f"{slug}: bad date or cadence")
            continue
        age = (today - last).days
        if age > cadence:
            problems.append(f"{slug}: {age} days since last diff, cadence {cadence}")
        if r["url"] not in watch_text(topic):
            problems.append(f"{slug}: url missing from docs/{topic}/watchlist.md")
    print(f"aggregators  {len(rows)} registered, {active} active, {pending} pending, "
          f"{retired} retired, topics: {','.join(sorted(topics))}")
    for p in problems:
        print(f"  DEFECT {p}")
    return 1 if problems else 0


def cmd_diff(args, rows: list[dict]) -> int:
    row = next((r for r in rows if r["slug"] == args.diff), None)
    if row is None:
        print(f"no source '{args.diff}' in the registry", file=sys.stderr)
        return 2
    html = open(args.html, encoding="utf-8", errors="replace").read()
    names = names_from_html(html, row["pattern"])
    if not names:
        print(f"pattern matched nothing: {row['pattern']!r}", file=sys.stderr)
        return 1
    dossier = os.path.join(repo_root(args.root), "dossier")
    slugs, providers = dossier_index(dossier)
    known = set(slugs) | set(providers)
    missing = missing_names(names, known)
    print(f"{row['slug']}: {len(names)} providers, {len(names)-len(missing)} covered, {len(missing)} missing")
    for m in missing:
        print(f"  MISSING {m}")
    if args.update:
        row["covered"] = str(len(names) - len(missing))
        row["missing"] = str(len(missing))
        row["last_diff"] = args.today
        row["status"] = "active"
        save(args.registry, rows)
        print(f"registry updated: {row['slug']} {row['covered']}/{row['missing']} on {args.today}")
    return 0


def cmd_record(args, rows: list[dict]) -> int:
    row = next((r for r in rows if r["slug"] == args.record), None)
    if row is None:
        print(f"no source '{args.record}' in the registry", file=sys.stderr)
        return 2
    row["covered"] = str(args.covered)
    row["missing"] = str(args.missing)
    row["last_diff"] = args.today
    row["status"] = "active"
    save(args.registry, rows)
    print(f"recorded {row['slug']}: {row['covered']} covered, {row['missing']} missing on {row['last_diff']}")
    return 0


def cmd_selftest(args) -> int:
    import tempfile
    fails = 0
    html = '<a href="/provider/Aeza/vps">A</a><a href="/provider/TierNet/vps">B</a>'
    got = names_from_html(html, r'/provider/([^/"]+)/vps')
    if got != ["Aeza", "TierNet"]:
        print(f"FAIL extraction: {got}")
        fails += 1
    known = {norm("aeza")}
    miss = missing_names(got, known)
    if miss != ["TierNet"]:
        print(f"FAIL diff: {miss}")
        fails += 1
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.tsv")
        open(p, "w").write("\t".join(FIELDS) + "\n")
        rows = [{"slug": "x", "url": "u", "kind": "provider-index", "cadence_days": "7",
                 "last_diff": "2026-01-01", "covered": "1", "missing": "0",
                 "pattern": "", "status": "active", "note": ""}]
        save(p, rows)
        back = load(p)
        if back[0]["slug"] != "x" or back[0]["last_diff"] != "2026-01-01":
            print("FAIL round trip")
            fails += 1
    print("selftest: 3 checked,", "0 failed" if not fails else f"{fails} failed")
    return 0 if not fails else 1


def inside_tmp(path, root):
    p = os.path.normcase(os.path.abspath(path))
    return p.startswith(os.path.normcase(os.path.join(os.path.abspath(root), ".tmp")) + os.sep)


def research_checkout(root):
    import subprocess
    try:
        r = subprocess.run(["git", "-C", root, "config", "--get", "rq.researchCheckout"], capture_output=True, text=True)
    except OSError:
        return False
    return r.stdout.strip().lower() == "true"


def main() -> int:
    root = repo_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="repository root; defaults to the tree holding this script")
    ap.add_argument("--registry", default=None)
    ap.add_argument("--today", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--diff")
    g.add_argument("--record")
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--html")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--covered", type=int)
    ap.add_argument("--missing", type=int)
    args = ap.parse_args()
    if not args.registry:
        args.registry = os.path.join(repo_root(args.root), "scripts", "sources", "aggregators.tsv")

    if args.selftest:
        return cmd_selftest(args)
    writes = args.update or (args.record and not inside_tmp(args.registry, repo_root(args.root)))
    if writes and research_checkout(repo_root(args.root)):
        # the research checkout changes tracked files only through a run (AGENTS.md section 2 rule 14): the parent
        # copies the registry with scripts/rq show --out into .tmp/RUN/tools/, records there, and puts it with rq put
        print("aggregator-diff: the research checkout changes records only through a run: scripts/rq open amend TOPIC "
              "\"RID: what is wrong\" (AGENTS.md section 2 rule 14). Record into a copy under .tmp/RUN/tools/ "
              "(--registry), then scripts/rq put RUN scripts/sources/FILE .tmp/RUN/tools/FILE --reason \"...\".",
              file=sys.stderr)
        return 2
    if not os.path.exists(args.registry):
        print(f"no registry at {args.registry}", file=sys.stderr)
        return 3
    rows = load(args.registry)

    if args.check:
        return cmd_check(args, rows)
    if args.diff:
        if not args.html:
            print("--diff needs --html", file=sys.stderr)
            return 2
        return cmd_diff(args, rows)
    if args.record:
        if args.covered is None or args.missing is None:
            print("--record needs --covered and --missing", file=sys.stderr)
            return 2
        return cmd_record(args, rows)
    return 2


if __name__ == "__main__":
    sys.exit(main())
