#!/usr/bin/env python3
"""Apply reconciliation decisions to dossier records.

PURPOSE
    A reconciler decides which of two disagreeing lanes was right. That decision
    is data, not an edit, so it can be re-applied after a merge regenerates the
    records. This script reads a decisions file and writes the chosen value into
    the record, keeping the reason and the rejected value under `extras`.

WHY IT EXISTS
    Edits made directly to a merged file are lost the next time the merge runs.
    Edits applied from a file survive, and the file is reviewable on its own.

INPUT
    A JSON object keyed by slug:
    {"alldebrid": {"binding": {"value": "volume-quota", "reason": "...",
                               "evidence": ["https://..."]}}}

    A key may be a dotted path, such as `identity_cost.kind`.

DEPENDENCIES
    Python standard library.

OUTPUT
    JSON: {"applied": N, "records": N, "missing": [slug...], "unknown": [...]}

EXIT CODES
    0  every decision applied
    1  a decision named a record or a field that does not exist
    2  usage
    3  unreadable decisions file

EXAMPLES
    python scripts/dossier/apply-decisions.py \
        --decisions .tmp/debrid/reconcile-core/decisions.json \
        --dossier .tmp/debrid-merged --dry-run
    python scripts/dossier/apply-decisions.py \
        --decisions .tmp/debrid/reconcile-core/decisions.json \
        --dossier dossier/debrid
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys


def set_path(record: dict, path: str, value) -> bool:
    parts = path.split(".")
    node = record
    for part in parts[:-1]:
        if not isinstance(node.get(part), dict):
            return False
        node = node[part]
    node[parts[-1]] = value
    return True


def get_path(record: dict, path: str):
    node = record
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def write_json(path: str, payload) -> None:
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
    parser = argparse.ArgumentParser(description="Apply reconciliation decisions.")
    parser.add_argument("--decisions", required=True)
    parser.add_argument("--dossier", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        with open(args.decisions, encoding="utf-8") as handle:
            decisions = json.load(handle)
    except Exception as exc:  # noqa: BLE001
        print("apply: unreadable decisions: %s" % exc, file=sys.stderr)
        return 3
    if not isinstance(decisions, dict):
        print("apply: decisions must be an object keyed by slug", file=sys.stderr)
        return 3

    paths = {}
    for path in glob.glob(os.path.join(args.dossier, "*.json")):
        paths[os.path.basename(path)[:-5]] = path

    applied, missing, unknown, conflicts = 0, [], [], []
    for slug, fields in sorted(decisions.items()):
        path = paths.get(slug)
        if path is None:
            missing.append(slug)
            continue
        with open(path, encoding="utf-8") as handle:
            record = json.load(handle)
        record.setdefault("extras", {}).setdefault("decisions", {})
        for field, payload in fields.items():
            if not isinstance(payload, dict) or "value" not in payload:
                unknown.append("%s.%s: not a decision object" % (slug, field))
                continue
            old = get_path(record, field)
            if not set_path(record, field, payload["value"]):
                unknown.append("%s.%s: no such field" % (slug, field))
                continue
            if old is not None and old != payload["value"]:
                conflicts.append({"slug": slug, "field": field,
                                  "from": old, "to": payload["value"]})
            record["extras"]["decisions"][field] = {
                "value": payload["value"],
                "rejected": old if old != payload["value"] else None,
                "reason": payload.get("reason", ""),
                "evidence": payload.get("evidence", []),
            }
            applied += 1
        if not args.dry_run:
            refuse_in_research_checkout(path)
            write_json(path, record)

    print(json.dumps({"applied": applied, "records": len(decisions),
                      "missing": missing, "unknown": unknown,
                      "changes": conflicts, "dry_run": bool(args.dry_run)},
                     indent=2))
    return 0 if not missing and not unknown else 1


if __name__ == "__main__":
    sys.exit(main())
