#!/usr/bin/env python3
"""Apply lane change files to egress records that already exist.

WHY THIS EXISTS
    A research lane must not rewrite a record another lane already promoted, and
    the promoter refuses to. So a lane writes `.tmp/egress/<lane>/changes.json`
    and this applies it. Two shapes are accepted, because two lanes used both:

      {"slug_hint": "x", "field": "notes", "new_value": "...", "evidence": [...]}
      {"slug_hint": "x", "free_stated": "...", "wg_path": "...", ...}

    The second is a finding-shaped patch: every key that exists on the record is
    replaced, and a key the record does not have lands in `extras`.

USAGE
    python scripts/dossier/apply-egress-changes.py --changes .tmp/egress --dry-run
    python scripts/dossier/apply-egress-changes.py --changes .tmp/egress

EXIT CODES
    0  applied, or a dry run found nothing to refuse
    1  a change names a record that does not exist
    2  usage
    3  environment: a change file is unparseable
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

RECORD_KEYS = {
    "provider", "url", "category", "tier", "free_tier", "per_object_cap",
    "retention", "egress", "interface", "interface_detail", "endpoint",
    "tooling", "chaining", "limits", "limits_note", "binding", "binding_note",
    "identity_cost", "reliability_note", "confidence", "confidence_note",
    "confidence_legacy", "evidence", "verdict", "price_per_tb_month", "notes",
    "extras",
}

# A finding-shaped patch names the flat keys the lane wrote. The record stores
# most of them one level down, so the patch is translated rather than copied:
# without this, `free_stated` lands in extras and the record keeps its old offer.
FINDING_MAP = {
    "free_stated": ("free_tier", "stated"),
    "free_unit": ("free_tier", "unit"),
    "free_metered_on": ("free_tier", "metered_on"),
    "free_source": ("free_tier", "source_url"),
    "free_read_on": ("free_tier", "read_on"),
    "identity_kind": ("identity_cost", "kind"),
    "identity_detail": ("identity_cost", "detail"),
}
EXTRA_KEYS = {"wg_path", "wg_detail", "ingress", "volume_tib_month",
              "volume_stated", "bytes_transit", "transit_note",
              "hosting_requirement", "promoted_from", "reconciled"}


def merge_evidence(existing: list, extra: list) -> list:
    seen = {(e.get("url"), e.get("date")) for e in existing if isinstance(e, dict)}
    out = list(existing)
    for e in extra or []:
        if not isinstance(e, dict):
            continue
        key = (e.get("url"), e.get("date"))
        if key not in seen:
            out.append(e)
            seen.add(key)
    return out


def apply_one(rec: dict, change: dict) -> tuple[dict, list]:
    touched = []
    if change.get("field"):
        field, value = change["field"], change.get("new_value")
        if field in FINDING_MAP:
            outer, inner = FINDING_MAP[field]
            rec.setdefault(outer, {})[inner] = value
            touched.append(f"{outer}.{inner}")
        elif field in RECORD_KEYS:
            rec[field] = value
            touched.append(field)
        else:
            rec.setdefault("extras", {})[field] = value
            touched.append(f"extras.{field}")
    else:
        for key, value in change.items():
            if key in ("slug", "slug_hint", "field", "new_value", "reason",
                       "source", "confidence", "evidence"):
                continue
            if key in FINDING_MAP:
                outer, inner = FINDING_MAP[key]
                rec.setdefault(outer, {})[inner] = value
                touched.append(f"{outer}.{inner}")
            elif key in RECORD_KEYS:
                rec[key] = value
                touched.append(key)
            elif key in EXTRA_KEYS:
                rec.setdefault("extras", {})[key] = value
                touched.append(f"extras.{key}")
            else:
                rec.setdefault("extras", {})[key] = value
                touched.append(f"extras.{key}")
    if change.get("evidence"):
        rec["evidence"] = merge_evidence(rec.get("evidence") or [], change["evidence"])
        touched.append("evidence")
    if change.get("confidence"):
        rec["confidence"] = change["confidence"]
        touched.append("confidence")
    if change.get("reason"):
        note = rec.get("notes") or ""
        add = change["reason"].strip()
        if add and add not in note:
            rec["notes"] = (note + " " + add).strip()
            touched.append("notes")
    dates = [e.get("date") for e in rec.get("evidence") or [] if isinstance(e, dict)]
    if dates:
        newest = max(d for d in dates if d)
        if newest > (rec.get("verified_at") or "")[:10]:
            rec["verified_at"] = f"{newest}T00:00:00.000Z"
            touched.append("verified_at")
    return rec, touched


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
    ap.add_argument("--changes", default=".tmp/egress")
    ap.add_argument("--dossier", default="dossier/egress")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.changes, "*", "changes.json")))
    if not files:
        print("apply-egress-changes: no changes.json found")
        return 0

    applied, missing = 0, []
    for path in files:
        lane = os.path.basename(os.path.dirname(path))
        try:
            rows = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            print(f"unparseable {path}: {exc}", file=sys.stderr)
            return 3
        if isinstance(rows, dict):
            rows = rows.get("changes") or []
        for change in rows:
            if not isinstance(change, dict):
                continue
            slug = change.get("slug_hint") or change.get("slug")
            if not slug:
                continue
            target = os.path.join(args.dossier, slug + ".json")
            if not os.path.exists(target):
                missing.append(f"{lane}:{slug}")
                continue
            rec = json.load(open(target, encoding="utf-8"))
            rec, touched = apply_one(rec, change)
            applied += 1
            print(f"{'would apply' if args.dry_run else 'applied'} {lane}:{slug} -> {', '.join(touched)}")
            if not args.dry_run:
                refuse_in_research_checkout(target)
                with open(target, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(rec, fh, indent=2, ensure_ascii=True)
                    fh.write("\n")

    print(f"apply-egress-changes: {applied} change(s), {len(missing)} record(s) absent")
    for m in missing:
        print(f"  absent {m}", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
