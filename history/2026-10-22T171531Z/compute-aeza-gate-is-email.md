# Aeza wants an email, not a card, and states its traffic term

- **When:** 2026-10-22T17:15:31Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/aeza.json`, `identity_cost.kind: card` with the boilerplate detail, `egress.terms` asserting that no term was found, and a `notes` sentence leaving the free-test question open
- **Superseded by:** `dossier/compute/aeza.json`, `identity_cost.kind: email` with the rails that were actually read, the unlimited-traffic term with its port cap, and the free-test question answered as far as a public page can answer it
- **Evidence:** `https://aeza.net/virtual-servers`, `https://wiki.aeza.net/en/servers/virtual/promo-info/` and the vendor FAQ, read 2026-10-22; the knowledge-base page for the free test server returns 404
- **Confidence:** documented

## What we believed

That the account gate was a card, that the traffic term was unpublished, and that a free
test server might still exist because one catalogue page advertises it.

## What we found

Signup is an email address plus a robot check, and the wiki documents a crypto top-up, so a
card is not the only route to a balance. The traffic term is published as "Traffic
infinity": the constraint is the port at 25 Gbit/s, not a byte counter.

The free test server is gone from the knowledge base. Its page returns 404 and is absent from
the wiki sitemap, while `terminator.aeza.net` answered the broker with HTTP 530, which says
nothing about the target. The vendor's own FAQ answers the trial question with hourly billing
and a test balance for legal entities on request.

The entry price is a promo plan at EUR 1.99 a month in Stockholm, monthly billing only, with
no first-term variant and no reversion rate stated anywhere, so it renews at the same figure
from balance. Hourly billing is unavailable on promo plans.

## What it changes

A reader without a card is no longer excluded by the record, and a reader planning traffic no
longer sees a blank where the vendor states infinity. What remains unverified is whether
unlimited traffic survives a sustained transfer, which only a probe would show, and whether
`terminator.aeza.net` is alive, because a broker 530 is not evidence about the provider.
