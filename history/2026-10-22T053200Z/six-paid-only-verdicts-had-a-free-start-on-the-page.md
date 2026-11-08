# Six records said paid-only about a page that offers a free start

- **When:** 2026-10-22T05:32:00Z
- **Status:** corrected
- **Supersedes:** `verdict: paid-only` on `agent-relay`, `brimble`, `gologin`, `nebius-contree`, `teclada` and `tencent-scf`
- **Superseded by:** those six records, now `qualifies-with-caveat` with the free path quoted
- **Evidence:** the six pages read through the broker on 2026-10-22
- **Confidence:** documented

## What we believed

That these six had no free tier, because the corpus card recorded none.

## What we found

Each page offers a free path, and the card had missed it for a different reason
each time:

| host | what the page says |
| --- | --- |
| `brimble` | a `Free` plan at `$0/mo` above the $3 Hacker tier; the card had put the *sandbox* quotas, which belong to Hacker, under the free row |
| `teclada` | `Free (non-commercial use)` in the plan table beside $100 and $500 a month |
| `gologin` | `Start free · Flat hourly · Residential IPs included`, and `Free, no card` |
| `agent-relay` | `Sign up and go. Free to start.` |
| `nebius-contree` | `Free while in beta — runs don't consume your credits` |
| `tencent-scf` | the billing overview's own contents list `免费额度`, a free quota |

`tencent-scf` is the one worth reading twice. The record's URL is the billing
*overview*, whose table of contents names a free-quota section and then links the
pricing page that gives the amount. The card read the overview, found no number,
and recorded paid-only. The number was one link away, and the section that held it
was named in the page's own contents.

## How we found it

One read each. In five of the six, "free" is in the first screen of the page.

## What it cost us

Six providers a budget-less reader would have skipped. Two of them —
`tencent-scf` and `brimble` — are the kind of thing that is actually used: a
function runtime and a hosting plan with a free row.

## What a future session should do differently

⭐ **"No free tier" is a claim, and the cheapest test is one read.** The corpus was
recording an absence it had never looked for. Where a page has a plan table, read
the table rather than the marketing sentence above it: `brimble`'s free plan is
real and its *limits* are the thing that was missing, which is a different defect
from having no plan at all.

⚠ **A page's contents list is evidence.** `tencent-scf`'s overview names the section
that answers the question. A reader who checks that a section exists before deciding
it does not would have found the quota without leaving the page.
