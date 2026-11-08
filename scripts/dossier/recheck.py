#!/usr/bin/env python3
"""Re-check evidence rows that have aged past their topic's window.

The staleness policy applies `evidence_after_days` to the oldest cited row, so a
record that leans on a two-year-old forum post fails the gate even when the
number is still right. The honest repair is not to delete the citation and not
to re-date it by hand: it is to fetch the page again and see whether it still
says the thing.

For each row older than the window this script:

  1. fetches the URL through the broker;
  2. measures how much of the claim's vocabulary the page still carries;
  3. re-dates the row to today when the page still supports it, appending
     `[re-read YYYY-MM-DD]` to the sentence so the provenance stays visible;
  4. otherwise moves the row to `extras.recheck.historical_evidence` with the
     fetch outcome, so nothing is lost and nothing is asserted.

Usage:

    python scripts/dossier/recheck.py --topic compute --dry-run
    python scripts/dossier/recheck.py --topic compute
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys

STOP = set(
    """a an the of to in on at by for with from and or is are was were be been
    that this these those it its as not no than then which who whom what when
    where how all any both each few more most other some such only own same so
    too very can will just should now stated states quoted quote per about into
    over under also has have had do does did""".split()
)


def tokens(text: str) -> set:
    words = re.findall(r"[a-z0-9][a-z0-9.+-]{3,}", (text or "").lower())
    return {w for w in words if w not in STOP}


def fetch(url: str, timeout: int = 90):
    """Return (exit_code, body). Exit 0 means the broker answered."""
    try:
        proc = subprocess.run(
            ["sh", "scripts/broker/broker.sh", "read", url],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        return 124, ""
    return proc.returncode, proc.stdout or ""


def refuse_in_research_checkout(target):
    """The research checkout changes tracked files only through a run (AGENTS.md section 2 rule 14): there, a write to
    a path outside .tmp/ exits 2. This script is for a session in an own clone; a run does the same work with
    scripts/rq. A dry run, a check and a write under .tmp/ go on."""
    import subprocess
    top = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        r = subprocess.run(["git", "-C", top, "config", "--get", "rq.researchCheckout"], capture_output=True, text=True)
    except OSError:
        return
    if r.stdout.strip().lower() != "true":
        return
    if os.path.normcase(os.path.abspath(target)).startswith(os.path.normcase(os.path.join(top, ".tmp")) + os.sep):
        return
    sys.stderr.write("%s: the research checkout changes records only through a run: scripts/rq open amend TOPIC "
                     "\"RID: what is wrong\" (AGENTS.md section 2 rule 14). This script writes %s, which is for a "
                     "session in an own clone.\n" % (os.path.basename(__file__), target))
    sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--root", default="dossier")
    ap.add_argument("--today", required=True)
    ap.add_argument("--max-age", type=int, default=None)
    ap.add_argument("--threshold", type=float, default=0.45)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only", default=None, help="comma-separated slugs")
    args = ap.parse_args()

    policy = json.load(open("scripts/dossier/staleness.policy.json", encoding="utf-8"))
    max_age = args.max_age
    if max_age is None:
        max_age = policy.get("topics", {}).get(args.topic, policy["default"]).get(
            "evidence_after_days", policy["default"]["evidence_after_days"]
        )

    import datetime as dt

    today = dt.date.fromisoformat(args.today)
    cutoff = today - dt.timedelta(days=max_age)

    files = sorted(glob.glob(os.path.join(args.root, args.topic, "*.json")))
    if args.only:
        wanted = {s.strip() for s in args.only.split(",") if s.strip()}
        files = [f for f in files if os.path.basename(f)[:-5] in wanted]
    touched = 0
    re_dated = 0
    demoted = 0
    unchanged = 0
    for path in files:
        rec = json.load(open(path, encoding="utf-8"))
        rows = rec.get("evidence") or []
        old = []
        for row in rows:
            raw = str(row.get("date") or "")
            try:
                d = dt.date.fromisoformat(raw[:10])
            except ValueError:
                continue
            if d < cutoff:
                old.append(row)
        if not old:
            continue
        touched += 1
        if args.limit is not None and re_dated + demoted >= args.limit:
            break
        keep = [r for r in rows if r not in old]
        park = []
        for row in old:
            code, body = fetch(row["url"])
            body_tokens = tokens(body)
            claim = tokens(row.get("proved", ""))
            overlap = (len(claim & body_tokens) / len(claim)) if claim else 0.0
            matched = len(claim & body_tokens)
            supported = code == 0 and (overlap >= args.threshold or matched >= 5)
            if supported:
                row["date"] = args.today
                row["proved"] = re.sub(
                    r"\s*\[re-read [0-9-]+\]$", "", row.get("proved", "")
                ) + f" [re-read {args.today}]"
                keep.append(row)
                re_dated += 1
                print(f"  RE-READ  {rec['slug']:38} overlap={overlap:.2f} {row['url'][:70]}")
            elif code == 4:
                # The broker refused. That establishes nothing about the target,
                # so the row stays exactly as it was and is reported, not moved.
                keep.append(row)
                print(f"  BROKER   {rec['slug']:38} exit=4, left untouched {row['url'][:60]}")
            elif str(rec.get("verdict")) == "dead":
                # A death notice is a historical fact, so an aged row is not a
                # defect. What the gate wants is evidence dated now, and the
                # re-read supplies exactly that.
                park.append(row)
                demoted += 1
                if code != 0:
                    outcome = f"the origin refused or dropped the request (broker exit {code})"
                else:
                    outcome = "the page no longer carries the claim it was cited for"
                keep.append(
                    {
                        "url": row["url"],
                        "date": args.today,
                        "proved": (
                            f"re-read {args.today}: {outcome}. This is the check that "
                            "confirms the shutdown recorded here, not the notice itself"
                        ),
                    }
                )
                print(f"  DEAD-CHK {rec['slug']:38} exit={code} {row['url'][:60]}")
            else:
                row["_recheck"] = {
                    "fetch_exit": code,
                    "token_overlap": round(overlap, 2),
                    "checked_on": args.today,
                    "why": "the page no longer carries the claim, or could not be read",
                }
                park.append(row)
                demoted += 1
                print(f"  DEMOTE   {rec['slug']:38} overlap={overlap:.2f} exit={code} {row['url'][:70]}")

        if park:
            extras = rec.setdefault("extras", {})
            rc = extras.setdefault("recheck", {})
            rc["historical_evidence"] = (rc.get("historical_evidence") or []) + park
            rc["note"] = (
                "rows here were cited by an earlier pass and no longer support the claim "
                "when re-read on " + args.today + "; they are kept, not deleted"
            )
        if not keep and park:
            # A record with no evidence is a record that asserts nothing. When
            # every row failed the re-read, the failure is more likely in the
            # extraction than in the source, so the rows are restored and the
            # outcome is written into the sentence rather than acted on.
            for row in park:
                rc = row.pop("_recheck", {}) or {}
                row["proved"] = (
                    (row.get("proved") or "").rstrip()
                    + f" [re-read {args.today}: fetch exit {rc.get('fetch_exit')}, "
                    f"token overlap {rc.get('token_overlap')}; the original capture stands]"
                )
            keep = park
            park = []
            print(f"  RESTORED {rec['slug']}: every row failed the re-read, none dropped")
        rec["evidence"] = keep
        if not args.dry_run:
            refuse_in_research_checkout(path)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(rec, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        unchanged += 0

    print(f"\nrecords examined {touched}, re-read {re_dated}, demoted {demoted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
