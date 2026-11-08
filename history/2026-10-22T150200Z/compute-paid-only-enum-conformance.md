# Four records said 'no free tier' and still carried a qualifies verdict

- **When:** 2026-10-22T15:02:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/hetzner-cloud.json` `qualifies`; `boat` `qualifies`; `contabo` `qualifies-with-caveat`; `netcup` `qualifies-with-caveat`
- **Superseded by:** all four now `paid-only`; `docs/compute/README.md` table
- **Evidence:** vendor pages read 2026-10-22 through `scripts/broker/broker.sh read`; the exact URLs and quoted sentences are in each record's `evidence[]` and in the body below
- **Confidence:** documented

## What we believed

That these four providers qualified, on the strength of a cheap monthly price.

## What we found

Each record states in its own `free_tier.stated` field that no free tier exists: Hetzner
"no free tier; the entry shape CX23 is USD 6.49 a month excluding IPv4 and VAT", boat "no free
tier is published; the smallest plan is USD 20 a month", Contabo "no free tier", netcup "no
free tier". `docs/conventions/README.md` defines `paid-only` as "it was never free", so the
verdict contradicted the record's own evidence.

## What it changes

All four become `paid-only`. This is an enum conformance fix rather than a price change, and
it moves four rows in the generated table at `docs/compute/README.md`.

## The transferable point

A verdict that contradicts the field directly above it is the cheapest kind of defect to find
and the most expensive kind to leave: a reader who trusts the table never reads the field.
Any future pass should assert that `free_tier_kind: none` implies a `paid-only` or `dead`
verdict, and the reconciler now does.
