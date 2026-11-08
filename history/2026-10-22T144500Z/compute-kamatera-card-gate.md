# Kamatera's trial needs a card, not an email

- **When:** 2026-10-22T14:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/kamatera.json` identity cost `email`
- **Superseded by:** `dossier/compute/kamatera.json` identity cost `card`; verdict unchanged at `trial-only`
- **Evidence:** `https://huggingface.co/docs/hub/spaces-overview`, `https://huggingface.co/docs/hub/spaces-zerogpu`, `https://research.google.com/colaboratory/faq.html`, `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, `https://railway.com/pricing`, `https://neon.com/pricing`, `https://neon.com/faqs/free-plan-limits-and-quotas`, `https://www.kamatera.com/free-trial/`, all read 2026-10-22 through `scripts/broker/broker.sh read`
- **Confidence:** documented

## What we believed

That the 30-day Kamatera trial was reachable with an email address, recorded with an
unverified identity.

## What we found

`https://www.kamatera.com/free-trial/`, read 2026-10-22, states "Sign up for a free 30-day
trial to receive cloud services worth up to $100", "1 cloud server valued up to $100 with the
configuration of your choice", and on the form itself, "Free trial requires valid credit
card". The FAQ repeats it: "Customers must provide a valid credit card to start the trial".

The stored note also claimed the trial was only a link at signup. The trial page carries its
own terms, so that was wrong too.

## What it changes

The identity cost becomes `card`. The verdict stays `trial-only`: 30 days, up to USD 100 of
configuration, 1 TB of transfer.

## The transferable point

Identity is the field that turns a trial into a decision. A trial that needs a card is a
payment relationship with a 30-day clock, and the record must say so before a reader plans
around it.
