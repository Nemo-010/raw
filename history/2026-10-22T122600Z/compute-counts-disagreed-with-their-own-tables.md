# Six counts in compute prose disagreed with the tables beside them

- **When:** 2026-10-22T12:26:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/dead-ends.md` §the opening count and §What the count means, `docs/compute/free/free-tier-census.md` §The counts and §The eleven recurring credits, `docs/compute/README.md` §The three facts
- **Superseded by:** those sections, and `docs/compute/gaps.md` §Contradictions this session closed which records the class
- **Evidence:** `scripts/report/render.py` rendered each table from the records; the prose was typed by hand beside it
- **Confidence:** documented

## What was superseded

Six hand-typed counts in `docs/compute/` were larger or smaller than the generated
table in the same document, and in each case the table was right and the sentence
was the defect.

| document | the sentence said | the records hold |
|---|---|---|
| `dead-ends.md` | seven records carry `verdict: dead` | 15 |
| `dead-ends.md` | five carry a `fails-*` verdict | 6 (2 identity, 4 quota) |
| `dead-ends.md` | fifty-seven reclassified from dead to paid-only | 58 |
| `free-tier-census.md` | nine recurring credits | 11 |
| `free-tier-census.md` | eighty-three one-time credits | 54 |
| `free-tier-census.md` | three hundred and two `qualifies-with-caveat` | 208 |
| `README.md` | 74 records are `paid-only` | 132 |
| `README.md` | only 18 records carry an explicit shape | 123 carry at least one field, 21 carry both vCPU and memory |
| `README.md` | only three records carry the 4 vCPU / 8 GiB shape | 2 |
| `free-tier-census.md` | "Nine rows out of 405" ... 2.2 per cent | 11, which is 2.7 per cent |

## What took them away

`scripts/report/render.py` renders the table from the records; the prose was typed
by hand beside it. Every one of those sentences introduced itself as derived from
the records, which is what made the disagreement invisible: a reader who checked
the table found agreement and stopped.

The recurring-credit roster was wrong in both directions. The prose table named
Bright Data Browser (`free_tier_kind: allowance`) and Scrapeless (`none`), and it
omitted Airtop, Buddy, Opensteer, Solari and Trigger.dev, which carry
`recurring-credit`. The count and the roster were wrong together, so each made the
other look checked.

## Where the correction lives

Every figure now reads from the record or names the field it counts.
`free/free-tier-census.md` carries a note recording that its recurring table listed
two rows that do not belong and omitted five that do.
`docs/compute/gaps.md` records the class of defect.

## The rule this restates

`docs/conventions/README.md` section 3.5: a table in `docs/` that restates a record
is generated between markers, and a hand-edited one disagrees with its records at
the next render. A count in *prose* had no such guard, and that is the gap this
event exposes: the tables were protected and the sentences beside them were not.
