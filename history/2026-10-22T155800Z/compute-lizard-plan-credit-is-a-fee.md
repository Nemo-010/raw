# Lizard's USD 19 plan is a fee, not a free tier

- **When:** 2026-10-22T15:58:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/lizard.json` verdict `qualifies-with-caveat`
- **Superseded by:** `dossier/compute/lizard.json` verdict `trial-only`; `docs/compute/free/sandboxes-container-vm.md`; `docs/compute/paid/README.md`
- **Evidence:** `https://lizard.build/pricing`, read 2026-10-22
- **Confidence:** documented

## What we believed

That Lizard qualified as a free tier with a caveat, on the strength of a USD 19 plan that
includes USD 19 of monthly usage.

## What we found

The pricing page states both halves in one paragraph and they mean different things:

> Pro costs $19 a month and includes $19 in monthly credits for the whole platform: apps,
> databases, Sandboxes, storage and egress.

and

> Yes. Pro starts with a 7-day trial and $5 in trial credits. You need a card to start it,
> but we charge nothing during the 7 days, and you can cancel before the trial ends. If you
> keep Pro, we charge $19 when the trial ends and then each month.

A plan whose fee returns as usage is not free capacity. The USD 19 leaves the account and
comes back as a credit; calling that a free tier counts the same money twice. The only free
lane is the 7-day trial with USD 5 of credit, behind a card.

## What it changes

The verdict becomes `trial-only`, the binding constraint becomes the USD 5 credit, and the
record carries the arithmetic: at the medium sandbox rate of USD 0.0324 an hour, USD 5 buys
about 154 sandbox hours; at the small rate of USD 0.0162, about 309.

The per-second rates stay in the paid documents unchanged. Lizard is still one of the
cheapest per-second sandboxes at USD 0.0162 an hour for 2 vCPU / 4 GiB, and a reader
comparing paid lanes is not affected by this correction.

## The transferable point

"USD X a month with USD X of usage included" is a prepayment, not an allowance. The test is
whether the money leaves the account: a recurring credit that arrives without a fee is an
allowance, and a credit that arrives because a fee was paid is a wallet. Three records in
this topic have that shape and each needs the same reading.
