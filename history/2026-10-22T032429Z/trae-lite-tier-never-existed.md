# Trae's USD 3 Lite tier never existed, and its Pro price was half the real one

- **When:** 2026-10-22T03:24:29Z
- **Status:** corrected
- **Supersedes:** `.tmp/seed/coding-subs/2026-09-13/data/providers-database.csv`, the
  Trae Pro and Trae Lite rows; still present in
  `.tmp/seed/coding-subs/2026-09-20/data/providers-database.csv`
- **Superseded by:** `docs/coding-subs/free/free-tier-of-paid-plan.md` §Trae, and
  `dossier/coding-subs/trae.json`
- **Evidence:** `www.trae.ai/pricing`, read 2026-10-22, which returns the whole
  ladder as text
- **Confidence:** documented

## What we believed

The 2026-09-13 seed priced Trae Pro at USD 10 and Trae Lite at USD 3.

## What we found

Today's page states four tiers and no others:

| plan | price a month | included |
| --- | --- | --- |
| Free | USD 0 | auto mode only, limited usage, limited autocomplete |
| Pro | USD 20 | auto plus all models, USD 20 of usage a month, unlimited autocomplete, 10 concurrent cloud tasks |
| Pro+ | USD 60 | USD 60 of usage a month, 15 concurrent cloud tasks |
| Ultra | USD 200 | USD 200 of usage a month, model early access, 20 concurrent cloud tasks |

**There is no Lite tier at any price.** The 2026-09-13 capture was a 1,422-byte
truncation that ended mid-tag and contained no price at all; the 2026-09-20 pass
re-fetched the same URL and got the ladder as machine-readable JSON, corrected Pro
to USD 20, and left Lite at USD 3 in the newer file. The 2026-10-02 pass then
dropped Trae from its plan ladder entirely, so by the newest pass the contradiction
was neither fixed nor flagged.

## How we found it

One read of `www.trae.ai/pricing` on 2026-10-22 returned the ladder as plain text,
including the per-tier usage allowance which is denominated in USD and equal to the
price.

## What it cost us

A non-existent SKU survived two later passes. Any ranking that included a USD 3 row
was comparing against something a reader could not buy, and because the fake tier
was the cheapest, it sorted to the top of a "cheapest plan" table.

## What a future session should do differently

Abandonment is not a correction. When a later pass drops a row it cannot verify, the
drop leaves the earlier row live in the older file and removes the only place the
disagreement was visible. Write the withdrawal into `history/` and mark the record,
or the next reader inherits a defect that no table shows.
