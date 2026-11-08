# boat has a free trial, and its own pages disagree about its shape

- **When:** 2026-10-22T15:15:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/boat.json` verdict `paid-only` with `free_tier.stated` reading that no free tier is published
- **Superseded by:** `dossier/compute/boat.json` verdict `trial-only`; `docs/compute/free/dev-environments.md`
- **Evidence:** `https://docs.boat.dev/pricing`, `https://boat.dev/`, `https://boat.dev/compare`, all read 2026-10-22
- **Confidence:** documented

## What we believed

That boat published no free tier, so the record read `paid-only` and its offer sentence said
so in those words.

## What we found

Three pages on the vendor's own site, read on 2026-10-22, all describe a trial, and they
disagree with each other about what it contains.

`https://docs.boat.dev/pricing`: "Your first plan starts with a 7-day free trial. A card is
required. The trial has its own lower limits."

`https://boat.dev/`: "Billed per second, free when stopped. 7-day free trial, then from
$20/mo."

`https://boat.dev/compare`: "25 free hours to start".

The `/free-trial` page that the documentation links to returns 404, so the trial's allowance
cannot be established from the vendor. Only the clock can.

## What it changes

The verdict becomes `trial-only`, the identity cost becomes `card`, and the binding
constraint becomes the trial clock plus the 14-day stopped-disk window, which is the term
that actually destroys work: a stopped sandbox keeps its disk for 14 days and is then
deleted without recovery.

The comparison page also carries the reason this record was opened at all: it lists
fourteen sandbox providers at one shape with list prices dated 2026-09-26, which is a
cross-check the corpus had never used.

## The transferable point

A "no free tier" conclusion drawn from a pricing page is a conclusion about that page. The
same vendor's documentation, homepage and comparison page each carried a different version
of the answer, and the link between them was already broken.
