#!/usr/bin/env python3
"""Report which card-gated records state how much money is held.

PURPOSE
  The operator's complaint about this corpus was specific: free tiers demand a
  credit card with roughly USD 50 held on it, and the corpus did not say so.
  A record whose `identity_cost.kind` is `card` but whose `detail` never names
  an amount tells a reader the gate exists and nothing about its price.

  This is a REPORT, not a gate check. Most card-gated providers never publish
  their hold, so a check that failed on a missing amount would be red forever
  and would be switched off within a week. What it does instead is make the gap
  countable, so a document that claims to rank registration cost can say how
  much of its ranking rests on a stated hold and how much on a guess.

WHAT IT COUNTS
  For each record:
    - `kind` from `identity_cost.kind`
    - `states_amount`: the detail names a currency amount AND a hold, authorisation,
      deposit, top-up, minimum or charge in the same sentence window
    - `hedged`: the detail carries "unverified", "not verified", "not stated",
      "not established" -- the honest form, counted separately from silence

USAGE
  python scripts/dossier/card-hold.py dossier/compute
  python scripts/dossier/card-hold.py dossier/compute --topic compute --json
  python scripts/dossier/card-hold.py dossier/compute --list-missing

EXIT CODES
  0  the report ran
  2  usage error, or the path holds no records
"""
import argparse
import glob
import json
import os
import re
import sys

# A currency amount, in the forms the corpus writes them: "USD 50", "EUR 1.00",
# "USD 0.00", and the bare "$50" a vendor quote may carry.
AMOUNT = re.compile(r"(?:usd|eur|gbp|cny|jpy|inr)\s?\d+(?:[.,]\d+)?|\$\s?\d+(?:[.,]\d+)?")
# The words that make an amount a hold rather than a price.
HOLD_WORD = re.compile(
    r"hold|authoris|authoriz|deposit|top-?up|minimum|pre-?auth|pending|charge"
)
HEDGE = re.compile(r"unverified|not verified|not stated|not established|could not|not readable")

# A detail that names no gate at all. "as stated by the provider's signup page"
# is the one that spread: it was pasted into 454 compute records, and it tells a
# reader nothing about the card, the hold or the identity document. A record
# carrying it has an `identity_cost.kind` and no cost.
VACUOUS = (
    "as stated by the provider's signup page",
)


def classify(record):
    identity = record.get("identity_cost") or {}
    detail = (identity.get("detail") or "")
    low = detail.lower()
    return {
        "kind": identity.get("kind") or "none",
        "states_amount": bool(AMOUNT.search(low) and HOLD_WORD.search(low)),
        "hedged": bool(HEDGE.search(low)),
        "vacuous": detail.strip().lower() in VACUOUS,
        "amount": (AMOUNT.search(low).group(0).upper() if AMOUNT.search(low) else None),
    }


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("path", help="a dossier topic directory, or one record file")
    ap.add_argument("--topic", default=None, help="label for the report header")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list-missing", action="store_true",
                    help="print the slug of every card record that states no amount")
    args = ap.parse_args(argv)

    if os.path.isdir(args.path):
        paths = sorted(glob.glob(os.path.join(args.path, "*.json")))
    elif os.path.isfile(args.path):
        paths = [args.path]
    else:
        print(f"no such path: {args.path}", file=sys.stderr)
        return 2

    records = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                records.append((os.path.basename(path)[:-5], json.load(fh)))
        except (OSError, ValueError) as exc:
            print(f"SKIP unreadable: {path}: {exc}", file=sys.stderr)
    if not records:
        print(f"no records under: {args.path}", file=sys.stderr)
        return 2

    kinds, card_stated, card_silent, card_hedged = {}, [], [], []
    vacuous = []
    for slug, record in records:
        c = classify(record)
        kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
        if c["vacuous"]:
            vacuous.append(slug)
        if c["kind"] != "card":
            continue
        if c["states_amount"]:
            card_stated.append((slug, c["amount"]))
        else:
            card_silent.append(slug)
            if c["hedged"]:
                card_hedged.append(slug)

    card_total = len(card_stated) + len(card_silent)
    out = {
        "topic": args.topic or os.path.basename(os.path.normpath(args.path)),
        "records": len(records),
        "kinds": dict(sorted(kinds.items(), key=lambda kv: -kv[1])),
        "card_required": card_total,
        "card_states_hold": len(card_stated),
        "card_silent_on_hold": len(card_silent),
        "card_silent_but_hedged": len(card_hedged),
        "coverage_pct": (round(100.0 * len(card_stated) / card_total, 1) if card_total else None),
        "vacuous_detail": len(vacuous),
    }

    if args.json:
        if args.list_missing:
            out["silent"] = card_silent
            out["stated"] = [{"slug": s, "amount": a} for s, a in card_stated]
        print(json.dumps(out, indent=1))
        return 0

    print(f"{out['topic']}: {out['records']} records")
    print("  identity kinds: " + ", ".join(f"{k} {v}" for k, v in out["kinds"].items()))
    print(f"  card required: {card_total}")
    print(f"  states a hold amount: {len(card_stated)}"
          + (f" ({out['coverage_pct']}%)" if card_total else ""))
    print(f"  silent on the amount: {len(card_silent)}"
          f", of which {len(card_hedged)} say so explicitly")
    if vacuous:
        print(f"  detail asserts nothing at all: {len(vacuous)}"
              " (the gate is named and its cost is not)")
    if args.list_missing:
        print("\n  silent, with no hedge (the dangerous ones):")
        for slug in card_silent:
            if slug not in card_hedged:
                print(f"    {slug}")
        print("\n  states an amount:")
        for slug, amount in card_stated:
            print(f"    {slug}: {amount}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
