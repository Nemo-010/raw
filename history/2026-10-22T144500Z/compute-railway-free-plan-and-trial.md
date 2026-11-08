# Railway has a permanent free plan beside its 30-day trial

- **When:** 2026-10-22T14:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/railway.json` verdict `trial-only`
- **Superseded by:** `dossier/compute/railway.json` verdict `qualifies-with-caveat`; `docs/compute/free/perpetual-allowances.md`
- **Evidence:** `https://huggingface.co/docs/hub/spaces-overview`, `https://huggingface.co/docs/hub/spaces-zerogpu`, `https://research.google.com/colaboratory/faq.html`, `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, `https://railway.com/pricing`, `https://neon.com/pricing`, `https://neon.com/faqs/free-plan-limits-and-quotas`, `https://www.kamatera.com/free-trial/`, all read 2026-10-22 through `scripts/broker/broker.sh read`
- **Confidence:** documented

## What we believed

That Railway's free offer was a trial, so the record read `trial-only`.

## What we found

`https://railway.com/pricing`, read 2026-10-22, carries two separate rows: "Free - $0/month
with $1 of monthly usage credits. Up to 1 vCPU / 0.5 GB per service, 1 replica, and 3-day log
history", and "Free Trial - $5 in credits for 30 days to try Railway. No credit card
required."

One is permanent and one expires. The stored record described only the second.

## What it changes

The verdict becomes `qualifies-with-caveat`. At the page's own rates of USD 20 per vCPU and
USD 10 per GB per month, USD 1 of credit buys about 29 hours of a 1 vCPU / 0.5 GB service in
a month. An always-on process does not fit inside that, which is the caveat.

A third lane exists and is recorded separately: an anonymous box reachable as `ssh
railway.new`, 2 vCPU / 2 GB, limited to 3 boxes per IP per day and deleted if unclaimed within
24 hours. It is a sandbox, not a host.

## The transferable point

Two rows on one pricing page can describe two products with different lifetimes. Reading the
first is not reading the page.
