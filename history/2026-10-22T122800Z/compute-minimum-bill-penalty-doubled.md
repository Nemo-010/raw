# The minimum-bill penalty column was exactly twice the right answer

- **When:** 2026-10-22T12:28:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/paid/minimum-bill.md` §The minimum billable unit, all 33 rows of the penalty table and two prose sentences
- **Superseded by:** that section, where every row is now the ratio of its own two bill columns
- **Evidence:** the two adjacent bill columns; 3,600 s / 1,800 s = 2x where the table printed 4x
- **Confidence:** documented

## What was superseded

`docs/compute/paid/minimum-bill.md` priced a **30-minute run** and printed a
`Penalty` column giving the multiplier each provider's minimum billable unit
applies. Every row was a factor of two too large.

| provider | minimum | printed | correct |
|---|---|---|---|
| hostmyapple | 2,592,000 s | 2,880x | 1,440x |
| AWS EC2 Mac | 86,400 s | 96x | 48x |
| Flow Swiss Mac | 86,400 s | 96x | 48x |
| use-computer | 86,400 s | 96x | 48x |
| Alibaba ECS | 3,600 s | 4x | 2x |
| and 28 more | 3,600 s | 4x | 2x |

## What took it away

The document's own two bill columns. `Seed bill, with the minimum` divided by
`Seed bill, smoothed` gives the correct multiplier on every row, and the `Penalty`
column disagreed with both.

```
3,600 s minimum / 1,800 s workload = 2x
printed: 4x
```

The divisor used was 900 seconds, which is 15 minutes, not the 30-minute workload
the document states in its own title. One detail confirms it: the prose said the mac
rows were extreme "at 96x and 2,880x", which are exactly twice 48 and 1,440.

## Where the correction lives

All 33 rows now carry the ratio of their two bill columns, so a reader can check any
row by hand. The two prose sentences that repeated the doubled figures are corrected.

⚠ **MacStadium's row does not follow its own minimum.** At 30 days its stated rate
would give the largest multiplier on the table and its bill ratio is 20x. That
inconsistency came from the seed, is left visible rather than silently normalised,
and is named in the document.

## Why a factor of two is the dangerous kind

It changes no ranking, so the table still sorted correctly and the conclusion still
held. It changes every number a reader would quote, and a reader quoting "2,880x"
for a Mac billed by the month is quoting a figure twice the truth. The column had
been in the tree since the seed merge and was found only when a later pass
recomputed it from the two adjacent columns.
