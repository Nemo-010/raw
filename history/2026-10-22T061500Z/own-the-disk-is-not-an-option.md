# The cheapest option in the corpus is not available without owned hardware

- **When:** 2026-10-22T06:15:00Z
- **Status:** corrected
- **Supersedes:** `docs/storage/README.md` §The recommendation, `docs/storage/paid/README.md` §The floor: your own disk, and `docs/netdisk-pan/paid/README.md` §What to do instead
- **Superseded by:** those three sections, which now price managed capacity only
- **Evidence:** the standing instruction that the corpus assumes no owned hardware; the arithmetic below, retained so it is not re-derived
- **Confidence:** documented

## What we believed

That a 20 TiB archive should be bought as a disk. The corpus priced it, published it as the
headline recommendation in the storage topic, and repeated it as the fallback in
`netdisk-pan`. The arithmetic was correct:

| option | one-time | over 60 months | per TB per month |
|---|---|---|---|
| 20 TB CMR HDD, new | USD 330 | USD 5.50 | USD 0.28 |
| 20 TB shucked or refurbished | USD 200 | USD 3.33 | USD 0.17 |
| plus a used mini-PC | USD 200 | plus USD 3.33 | plus USD 0.17 |
| plus electricity at 6 W idle | n/a | n/a | plus USD 0.03 |

USD 200 / 60 = USD 3.33, and with the mini-PC USD 6.67 to 8.83 per month, plus about
USD 0.66 of power, gives USD 7.33 to 9.49 all in for 20 TB. That is USD 0.37 to 0.48 per TB
per month against EUR 2.03 (USD 2.28) for the best managed box: **five to six times
cheaper**, and two to three times below the cold tier.

## What we found

**The corpus assumes no owned hardware.** That is the premise of the project,
not a constraint to trade against. A recommendation to buy a disk is therefore not a cheaper
option — it is an option that does not exist.

Two documents led with it, one table carried it as a row, and a whole section was built
around amortising a purchase for somebody with nothing to plug the disk into. The work was
competent and entirely unusable, which is the worst combination available: a reader who
trusts the arithmetic and skips the premise is led to a USD 200 disk with nothing to power it.

## How we found it

The operator said so, after the corpus was published. Nothing in the corpus asked. That is
the failure worth recording: AGENTS.md named the three workloads and the identity cost, and
said nothing about whether owned hardware was in scope. A single line in the brief would have
saved the section.

## What it cost

One document's opening argument, a four-row table, one row in a five-row comparison, and a
wrong answer in `netdisk-pan`'s fallback path. Cheap as these things go, and it would have
cost USD 200 and a week of trying to make it work.

## What a future session should do differently

⛔ **Never recommend, price or compare owning hardware.** The rule is in `AGENTS.md` §2.9 and
`METHODOLOGY.md` §12a. A rented or managed box is a service and is often the answer; a box
that must be bought, housed and powered is not.

⚠ **When the honest finding is "cheaper if you owned a disk", say what a managed option costs
and move on.** The comparison may be one clause, marked not-applicable. It is never the
recommendation. This entry exists so the arithmetic above is not re-derived every time
somebody notices that buying a disk looks cheap.

⭐ **Ask whether owned hardware is in scope before pricing anything physical.** The premise
belongs in the brief, and it was missing for eleven topics.
