# Neon's 100 CU-hours are per project, not per account

- **When:** 2026-10-22T14:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/neon.json` verdict `fails-quota`
- **Superseded by:** `dossier/compute/neon.json` verdict `qualifies-with-caveat`; `docs/compute/databases-kv`
- **Evidence:** `https://huggingface.co/docs/hub/spaces-overview`, `https://huggingface.co/docs/hub/spaces-zerogpu`, `https://research.google.com/colaboratory/faq.html`, `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, `https://railway.com/pricing`, `https://neon.com/pricing`, `https://neon.com/faqs/free-plan-limits-and-quotas`, `https://www.kamatera.com/free-trial/`, all read 2026-10-22 through `scripts/broker/broker.sh read`
- **Confidence:** documented

## What we believed

That 100 CU-hours was an account ceiling, which made the free plan unusable for anything
long-running, so the record read `fails-quota`.

## What we found

`https://neon.com/faqs/free-plan-limits-and-quotas`, read 2026-10-22, states "100 CU-hours of
compute per project per month, 1 GB of Postgres storage per project (up to 20 GB total across
all projects), and 5 GB of public network transfer per project per month", and then the
sentence that decides the record: "Compute quotas are measured per project, so 100 projects
each get their own 100 CU-hour bucket".

It also states "Running out of CU-hours or egress (5 GB) suspends compute until the next
billing period", and the pricing page states "The Free plan is permanent (not a trial); no
credit card required."

## What it changes

The verdict becomes `qualifies-with-caveat`. The quota is per project and the plan is
permanent, so the aggregate is larger than the stored note assumed. The suspension on
exhaustion is the caveat: it lasts until the billing period resets and scale-to-zero cannot be
disabled on the free plan.

## A citation defect this pass found

The incoming evidence row cited `https://neon.com/docs/guides/consumption-limits`, which
describes customer-set quotas created through the API, not Neon's own free-plan enforcement.
The verdict is right and the citation was wrong, so the correct pages are cited instead.

## The transferable point

Per-account and per-project are different units. A quota quoted without its unit of
aggregation is not a quota.
