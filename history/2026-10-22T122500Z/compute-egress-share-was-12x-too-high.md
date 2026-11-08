# The egress share of one day's serving was 12 times too high

- **When:** 2026-10-22T12:25:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/README.md` §The answer, `docs/compute/free/README.md` §Ranked by what a reader can obtain tonight, `docs/compute/free/always-on-free.md` §Google Cloud Free Tier, `docs/compute/relay-egress.md`
- **Superseded by:** those four sections, which now read 0.0067 per cent, and `docs/compute/paid/cloud-vms.md` §Google Cloud's e2-micro which carries the recomputation
- **Evidence:** 1 GB a month divided by 30 days, then by 500 GB a day; the derivation is in the entry
- **Confidence:** documented

## The claim that was superseded

`docs/compute/README.md`, `free/README.md`, `free/always-on-free.md` and
`relay-egress.md` all stated that Google's free 1 GB a month of egress is
**0.08 per cent of one day's serving**.

## What took it away

Arithmetic. The serving target is 500 GB a day.

```
1 GB a month / 30 days = 0.0333 GB a day
0.0333 GB / 500 GB = 0.0000667 = 0.0067 per cent
```

The stated figure is 12 times the true one. The likely origin is a division of
1 GB by 15,000 GB, which is a *month* at 500 GB a day and yields 0.0067 per cent,
followed by one further factor of 12 introduced when the monthly figure was
compared to a daily one.

## Where the correction lives

All four documents now read 0.0067 per cent. `paid/cloud-vms.md` carries the
correction note in place, because that document was written after the error and
its own arithmetic section had to be rebuilt from it.

## Why it survived four documents

The number looked small in every sentence, so no reader had a reason to check it,
and the conclusion it supported, that Google's egress is unusable for serving, is
correct at either figure. A wrong number that changes no decision is the kind that
is never found: it was found here only because a later pass recomputed every share
of a day from the record.
