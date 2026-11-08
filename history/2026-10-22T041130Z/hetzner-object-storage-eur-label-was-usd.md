# EUR 8.21 per TB was the dollar figure, and the ratio built on it was the wrong ratio

- **When:** 2026-10-22T04:11:30Z
- **Status:** corrected
- **Supersedes:** `docs/storage/README.md` §The answer, and its price, and `docs/storage/paid/storage-boxes.md` §Hetzner: two products, one machine, a 3.6x gap
- **Superseded by:** the same two sections after this entry
- **Evidence:** `https://www.hetzner.com/storage/object-storage/` fetched 2026-10-22 (200, 137,802 B): base `{"EUR":6.49,"USD":7.99}`, "Storage: EUR 0.0087 per hour, excl. VAT per TB-hour", "Egress traffic: EUR 1.0000 per hour, excl. VAT per TB"; the record `dossier/storage/hetzner-object-storage.json` carries the same arithmetic in `extras.price_verbatim`
- **Confidence:** documented

## What we believed

The topic's opening argument was built on a comparison between two Hetzner products:

> The Storage Box is EUR 2.03 per TB per month with unlimited traffic. The Object Storage is
> EUR 8.21 per TB per month and metered. The 4.0x gap is the egress term and nothing else.

`docs/storage/paid/storage-boxes.md` carried the same number under a heading that named the
ratio: "Hetzner: two products, one machine, a 4x gap".

## What we found

**EUR 8.21 is the dollar figure.** The record computes it correctly in dollars: EUR 146.16 at
1.1234 USD/EUR is USD 164.19, which is USD 8.21 per TB. The euro figure for the same 20 TB stored
and 20 TB read is **EUR 7.31 per TB**.

The arithmetic, from the live page on 2026-10-22:

| line | calculation | EUR |
| --- | --- | --- |
| base, 1 TB storage and 1 TB egress included | `6.49` | 6.49 |
| storage overage, 19 TB for a 730-hour month | `19 x 0.0087 x 730` | 120.67 |
| egress, 19 TB at EUR 1.00 per TB | `19 x 1.00` | 19.00 |
| **total** | | **146.16** |
| per TB | `146.16 / 20` | **7.31** |

So the sentence printed a dollar digit with a euro code, which `docs/conventions/README.md` §4.1
names as the defect the rule exists to prevent: *"Do not print one unit and label it another.
That is the defect these rules exist to prevent, and it has been shipped."*

**And the ratio was computed across the error.** `8.21 / 2.03 = 4.04` divides a dollar numerator
by a euro denominator. The same-currency comparison is `7.31 / 2.03 = 3.6`, which is the figure
the seed's own R3 review defended and which `FINAL-REPORT.md` states as "3.6x as the dossier
frames it". The document had silently replaced an audited 3.6x with a 4.0x that existed only
because of the unit error.

## How we found it

An adversarial review of `docs/storage/` recomputed the comparison and noticed that the record's
own text says `$8.21/TB` while the document says `EUR 8.21`. The live page was re-fetched this
session through the fetch broker: 200, 137,802 bytes, base price block
`{"StartingPrice":{"EUR":6.49,"USD":7.99}`, overage sentences verbatim.

## What it cost us

Nothing in the recommendation changes — the argument gets *stronger*, because 3.6x is still a
large gap and now it does not depend on a mixed-unit division. But a reader who checked the
arithmetic would have found it wrong, which is worse than finding it absent: `README.md` says in
its own words that "the arithmetic a reader should check" is stated so a reader can check it, and
this one did not survive the check.

The same defect appeared a second time on the same page (`OVHcloud One Zone Standard is EUR 8.31
per TB`, where the record says dollars) and a third time three lines below it (the own-disk
section compared against "a USD 0.90 per TB cold tier", where 1fichier GOLD is EUR 0.90). One
currency slip is a typo. Three in the opening argument of one topic is a habit, and the habit is
"the number is right, the unit is decoration".

## What a future session should do differently

**A price comparison states one currency and converts once, in the same sentence, with the rate
and its date.** `EUR 7.31 per TB, which is USD 8.21 at 1.1234 USD/EUR` is checkable. `EUR 8.21`
followed by a ratio computed against a euro denominator is not.

**When a record and a document disagree on a currency, the record is right and the document is
broken** — but check which one the record itself got right, because this record carried the
correct conversion in its `extras` while its `price_per_tb_month` was unpopulated. The subtraction
that finds this is one script over `dossier/` and `docs/`, and it has not been written.
