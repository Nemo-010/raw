# Cursor was repriced into a different product, and the seed's Pro and Pro+ rows are now legacy

- **When:** 2026-10-22T03:24:28Z
- **Status:** superseded
- **Supersedes:** `.tmp/seed/coding-subs/2026-10-02/data/plan-ladder.csv`, the four
  Cursor rows, carried into the seed's `providers-database.csv`
- **Superseded by:** `docs/coding-subs/paid/20-to-100.md` §Cursor, and
  `dossier/coding-subs/cursor.json`
- **Evidence:** `cursor.com/docs/models-and-pricing` and
  `cursor.com/docs/account/pricing/legacy-cursor-plans`, both read 2026-10-22
- **Confidence:** documented

## What we believed

The seed priced Cursor as Hobby at USD 0, Pro at USD 20, Pro+ at USD 60, Ultra at
USD 200 and Teams at USD 40 a user, each with a monthly usage pool split into Cursor
models and other models.

## What we found

That ladder is now sold as a legacy product. Cursor's current pricing document
describes **The X Subscription**: Free at USD 0, Plus at USD 8, Premium at USD 30,
Super at USD 100 and Ultra at USD 200, with **one weekly usage pool** shared across
Cursor and Grok instead of two monthly pools.

The legacy page confirms the old ladder and adds the mapping:

| legacy plan | legacy price | comparable new plan |
| --- | --- | --- |
| Hobby | free | Free |
| Pro | USD 20 | Premium, USD 30 |
| Pro+ | USD 60 | Super, USD 100 |
| Ultra | USD 200 | Ultra, USD 200 |
| Teams Standard | USD 40 a user | Teams, Premium seat, USD 30 a user |
| Teams Premium | USD 120 a user | Teams, Super seat, USD 100 a user |

Two changes matter more than the prices. The usage window moved from monthly to
**weekly**, which is a shorter clock and therefore a smaller buffer at the same
monthly spend. And third-party models left the included allowance: on the new ladder
they are billed at API list price from prepaid credit, which removes the "Other
Models" pool that legacy Pro, Pro+ and Ultra carried.

`cursor.com/pricing` still answers, and it now serves the Plus/Premium/Super ladder
rather than the Pro/Pro+ ladder the seed recorded.

## How we found it

The public pricing page was read first and returned a ladder that did not match the
seed. The docs index at `cursor.com/llms.txt` named a page called "Legacy Cursor
plans", which is the vendor's own statement that the seed's ladder is the old one.

## What it cost us

Not yet measurable. The seed ranked all 44 rows by estimated monthly token capacity,
and Cursor's rows in that ranking used prices from a ladder that a new customer
cannot buy.

## What a future session should do differently

When a vendor renames its tiers, the old ladder is usually still documented under a
"legacy" heading. Read that page before concluding that a price changed, because
"repriced" and "replaced by a different product" lead to different rows: the first
is a new number, the second retires the old SKU and adds a migration mapping.
