# Twelve GPU rates in a document had no record behind them

- **When:** 2026-10-22T12:27:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/paid/gpu-notebooks.md` §The comparison, §The two facts that decide the lane, and §RunPod
- **Superseded by:** that document, which now carries a `Backed` column marking twelve rows `no`, and `docs/compute/paid/gpu-rental.md` which cites only rates a record holds
- **Evidence:** a field-by-field comparison of the document against `dossier/compute/*.json`
- **Confidence:** documented

## What was superseded

`docs/compute/paid/gpu-notebooks.md` carried a comparison table of 22 rated rows in
which 12 rates appear in the document and nowhere in the corresponding dossier
record.

| provider | rates in the document | in the record |
|---|---|---|
| Daytona | 0.57, 0.74, 1.74, 2.27, 2.61, 3.59, 4.08 | none. The strings `3.59`, `1.74`, `2.27`, `2.61`, `4.08`, `B200` and `RTX PRO` appear nowhere in `daytona.json` |
| RunPod | B200 at 5.98 and 7.99, RTX PRO 6000 at 1.69 and 2.49 | the record holds B300 at 6.94 / 8.99 and H200 at 3.59 / 5.29 only |
| Lightning AI | A100 80GB at 1.85, RTX PRO 6000 at 4.64 | the record holds six of the eight rates and neither of these |

## What took them away

A field-by-field comparison of the document against `dossier/compute/*.json`. The
Daytona record carries the sandbox rate card: `retention-clamped` for the 15-minute
auto-stop, `request-rate` for 300 sandbox creations a minute, and `per-object-cap`
for the 5 GiB of free disk. It holds no GPU table at all.

`runpod.json`'s own note warns that the seed priced RunPod at USD 18 a month for a
2 vCPU shape, which "is not the product". Its `limits[]` names the B300 and H200
pairs. The B200 and RTX PRO 6000 rows were inherited and attributed to a page read.

## Where the correction lives

`paid/gpu-notebooks.md` now carries a `Backed` column, marks the twelve rows `no`,
and states the count. The two sections that reasoned from those rates carry the
qualification in place rather than being deleted, because the arithmetic in them is
correct and its inputs are what is missing.

`paid/gpu-rental.md` was written after this finding and cites only rates that appear
in a record.

## The distinction that matters and cannot be recovered here

Either the vendor page was read and the dossier was never updated, or the number was
inherited from the seed catalogue and attributed to a page. The first is an
incomplete record; the second is a fabricated citation. Nothing in the tree
distinguishes them, and one page read per row is what settles it. That work is on
`BRIEF.md`'s compute queue.
