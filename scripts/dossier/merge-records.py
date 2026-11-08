#!/usr/bin/env python3
"""Merge duplicate dossier records produced by parallel research lanes.

PURPOSE
    Ten lanes research one topic at once and more than one of them will write a
    record for the same provider. `promote-records.py` refuses the second one, so
    the duplicates have to be reconciled before promotion. This script does the
    mechanical half: it groups by slug, keeps the best-evidenced record as the
    base, unions the evidence and the constraints, and writes every disagreement
    into a report so a person decides what the base cannot.

WHY IT EXISTS
    Merging by hand across hundreds of files loses a source silently. A merge that
    says which lane said what is checkable; a merge that picked one is not.

DEPENDENCIES
    Python standard library only.

OUTPUT
    A merged record per slug in --out, and a JSON report on stdout:
    {"groups": N, "merged": N, "conflicts": [{slug, field, values}]}

EXIT CODES
    0  merged, no conflicting scalar fields
    1  merged, and the report carries conflicts a person must resolve
    2  usage
    3  no records found

EXAMPLES
    python scripts/dossier/merge-records.py --source .tmp/debrid \
        --out .tmp/debrid-merged
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

RANK = {"measured": 0, "documented": 1, "reported": 2,
        "inferred": 3, "unverified": 4}

# Scalar fields where a disagreement changes a recommendation. Two lanes may
# describe one provider differently; the base keeps one value and the report
# names the other, so nothing is lost and a person sees the choice.
CONFLICT_FIELDS = (
    ("free_tier", "stated"),
    ("per_object_cap", "stated"),
    ("retention", "stated"),
    ("egress", "terms"),
    ("identity_cost", "kind"),
)


def weight(rec: dict) -> tuple:
    return (RANK.get(rec.get("confidence"), 9),
            -len(json.dumps(rec)),
            rec.get("verified_at") or "")


def nonempty(value) -> bool:
    if isinstance(value, (list, dict)):
        return bool(value)
    return value not in (None, "")


def merge_group(slug: str, group: list[dict]) -> tuple[dict, list[dict]]:
    group = sorted(group, key=weight)
    base = json.loads(json.dumps(group[0]))
    conflicts = []

    for other in group[1:]:
        lane = other.get("_lane", "?")
        base.setdefault("extras", {})
        merged_from = base["extras"].setdefault("merged_from", [])
        if isinstance(merged_from, str):
            merged_from = [merged_from]
        if lane not in merged_from:
            merged_from.append(lane)

        for field in ("evidence", "limits", "history"):
            have = base.get(field) or []
            if not isinstance(have, list):
                continue
            keys = {json.dumps(item, sort_keys=True) for item in have}
            for item in other.get(field) or []:
                marker = json.dumps(item, sort_keys=True)
                if marker not in keys:
                    have.append(item)
                    keys.add(marker)
            base[field] = have

        for parent, child in CONFLICT_FIELDS:
            left = (base.get(parent) or {}).get(child)
            right = (other.get(parent) or {}).get(child)
            if nonempty(left) and nonempty(right) and left != right:
                conflicts.append({"slug": slug, "field": "%s.%s" % (parent, child),
                                  "kept": left, "other": right, "lane": lane})

        for key in ("verdict", "price_per_tb_month", "binding"):
            left, right = base.get(key), other.get(key)
            if nonempty(left) and nonempty(right) and left != right:
                conflicts.append({"slug": slug, "field": key,
                                  "kept": left, "other": right, "lane": lane})

        if other.get("notes"):
            base["notes"] = ((base.get("notes") or "").rstrip()
                             + " Merged from %s: %s" % (lane, other["notes"].strip())).strip()

        for key, value in (other.get("extras") or {}).items():
            if key == "merged_from":
                continue
            if key not in base["extras"]:
                base["extras"][key] = value
            elif base["extras"][key] != value:
                base["extras"].setdefault("merge_conflicts", {})[key] = [
                    base["extras"][key], {"lane": lane, "value": value}]

    if len(group) > 1:
        base["extras"]["record_count_merged"] = len(group)
    return base, conflicts


def write_json(path: str, payload) -> None:
    """Write LF, two-space JSON. Windows text mode would write CRLF and the
    conventions require LF in every tracked file."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Merge duplicate lane records.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", default=None)
    args = parser.parse_args(argv)
    refuse_in_research_checkout(args.out)
    if args.report:
        refuse_in_research_checkout(args.report)

    paths = sorted(glob.glob(os.path.join(args.source, "**", "records", "*.json"),
                             recursive=True))
    if not paths:
        print("merge: no records under %s" % args.source, file=sys.stderr)
        return 3

    groups: dict[str, list[dict]] = {}
    skipped = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8") as handle:
                rec = json.load(handle)
        except Exception:  # noqa: BLE001 - the skipped count is the report
            skipped += 1
            continue
        if not isinstance(rec, dict) or not rec.get("slug"):
            skipped += 1
            continue
        rec["_lane"] = path.replace("\\", "/").split("/")[-3]
        groups.setdefault(rec["slug"], []).append(rec)

    os.makedirs(args.out, exist_ok=True)
    conflicts, merged = [], 0
    for slug, group in sorted(groups.items()):
        record, found = merge_group(slug, group)
        record.pop("_lane", None)
        conflicts.extend(found)
        write_json(os.path.join(args.out, slug + ".json"), record)
        if len(group) > 1:
            merged += 1

    report = {"groups": len(groups), "merged": merged, "skipped": skipped,
              "conflicts": conflicts}
    if args.report:
        write_json(args.report, report)
    print(json.dumps({"groups": len(groups), "merged": merged,
                      "skipped": skipped, "conflicts": len(conflicts)}, indent=2))
    for item in conflicts[:40]:
        print("%(slug)s %(field)s: kept %(kept)r over %(other)r from %(lane)s"
              % item, file=sys.stderr)
    return 0 if not conflicts else 1


if __name__ == "__main__":
    sys.exit(main())
