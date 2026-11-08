# The seed's USD price ladder for Kimi and Z.ai does not match either vendor's current page

- **When:** 2026-10-22T03:24:33Z
- **Status:** corrected
- **Supersedes:** `.tmp/seed/coding-subs/2026-09-13/data/providers-database.csv`, the
  Kimi and Z.ai rows; and every Z.ai price in
  `.tmp/seed/coding-subs/2026-10-02/data/plan-ladder.csv`
- **Superseded by:** `dossier/coding-subs/kimi.json` and
  `dossier/coding-subs/zai-glm-coding-plan.json`
- **Evidence:** `kimi.com/help/membership/membership-pricing` and
  `docs.z.ai/devpack/overview`, both read 2026-10-22
- **Confidence:** documented

## What we believed

The seed carried a Kimi ladder of USD 19, 39, 99 and 199, and a Z.ai ladder of
Lite USD 18, Pro USD 72 and Max USD 160, the last two later corrected to USD 80 and
USD 168.

## What we found

**Kimi has five tiers, priced in CNY, and none of the four USD figures corresponds to
a tier.** The first-party help page gives Go at CNY 49, Plus at CNY 99, Pro at
CNY 199, Max at CNY 699 and Ultra at CNY 1,399 a month, with annual totals of 468,
948, 1,908, 6,708 and 13,428. The tier names in the seed (Moderato, Allegretto,
Allegro) are the *old* ladder, which the same page says existing subscribers keep.
Go excludes Kimi Code entirely. So the seed's USD 19 is not "Plus at a converted
rate": it is a four-tier ladder with different names, and the USD ladder itself was
third-party-sourced from a reseller page.

**Z.ai publishes the credit formula, and no page read today carries a price above
Lite.** The developer documentation states Lite from USD 18 a month with 2,000
five-hour credits and 10,000 weekly, Pro with 12,000 and 60,000, Max with 28,000 and
140,000. The subscribe page renders the three tier names and not the numbers. So the
seed's USD 72 / 80 / 160 / 168 figures cannot be confirmed or denied from the vendor
today, and the record carries no price for those two tiers.

## How we found it

Both vendor pages were read directly. Kimi's domestic ladder is published in a help
article with a screenshot dated 2026-10-19, and the Z.ai credit formula is in the
developer overview rather than the marketing page.

## What it cost us

The seed's currency handling. It priced a CNY ladder in USD, sourced the USD figures
from a reseller, and then recorded the discrepancy as "regional price
discrimination is real" instead of as two different ladders.

## What a future session should do differently

A ladder denominated in one currency, with a price captured in another, is two facts
and not one conversion. Record both with their own source, and never print a
converted figure without the rate and its date in the same cell.
