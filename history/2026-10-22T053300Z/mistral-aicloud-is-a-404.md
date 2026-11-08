# Mistral's AI-cloud page is a 404, and the record sold it as paid capacity

- **When:** 2026-10-22T05:33:00Z
- **Status:** superseded
- **Supersedes:** `dossier/compute/mistral-compute.json` (`verdict: paid-only`, "the source card records no free tier")
- **Superseded by:** the same record, now `verdict: dead` with the evidence of the death
- **Evidence:** `https://mistral.ai/products/aicloud/` read 2026-10-22 through the broker, the firecrawl provider and a raw fetch
- **Confidence:** documented

## What we believed

That Mistral sold an AI cloud and charged for it, so the row belonged in the paid
tables.

## What we found

The address returns **404** on all three routes and lands on Mistral's help-centre
shell, which offers a help centre, a console login, a Discord invite and a
documentation link. There is no product, no price and no signup for anything called
`aicloud`.

A `paid-only` verdict asserts that a price list exists. There is no price list at
this address, so the record had been asserting the existence of something a single
read disproves.

This is the eighth of its kind in this pass. The other seven are in
[`five-compute-hosts-closed-and-were-filed-as-paid.md`](../2026-10-22T050700Z/five-compute-hosts-closed-and-were-filed-as-paid.md),
written before this one was reached, and they are a different lesson: a shutdown
notice, a parking page, an acquisition. This one is plainer — the page is simply
gone — and it is worth its own line because the landing page makes it look like a
soft 404 rather than a dead host.

## How we found it

Three routes: the default read, `?__provider=firecrawl`, and the raw fetch. All
three agree on 404. The first capture, at 1,028 bytes, was the help-centre shell,
which is the kind of body that would pass for a live page to anything checking only
for a 200.

## What it cost us

One row in the paid tables pointing at an address that does not resolve to a
product. Cheap on its own; the eighth of eight is what makes it a pattern rather
than a slip.

## What a future session should do differently

⭐ **Check that the price list exists before recording a verdict about what it
says.** `paid-only` is a claim, and the cheapest test of it is the status code. A
404 is not a network blip and not a reason to retry: it is evidence, and it is
evidence of exactly one thing.

⚠ **A soft-404 body can pass a status check made on the body's size alone.** The
help-centre shell is 1 KB of real prose. Read what the page is *about*, not only
that it answered.
