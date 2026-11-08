# GitHub Actions public repositories are free and unlimited; the 2,000 minutes are private

- **When:** 2026-10-22T14:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/github-actions.json` verdict `fails-quota`
- **Superseded by:** `dossier/compute/github-actions.json` verdict `qualifies-with-caveat`; `docs/compute/free/ci-as-compute.md`
- **Evidence:** `https://huggingface.co/docs/hub/spaces-overview`, `https://huggingface.co/docs/hub/spaces-zerogpu`, `https://research.google.com/colaboratory/faq.html`, `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, `https://railway.com/pricing`, `https://neon.com/pricing`, `https://neon.com/faqs/free-plan-limits-and-quotas`, `https://www.kamatera.com/free-trial/`, all read 2026-10-22 through `scripts/broker/broker.sh read`
- **Confidence:** documented

## What we believed

That the 2,000-minute monthly allowance was the ceiling for the product, so the record read
`fails-quota`.

## What we found

The 2,000 minutes belong to private repositories.
`https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, read 2026-10-22,
states "Use of the standard GitHub-hosted runners is free and unlimited on public
repositories". The billing page says the same in different words and adds the sentence that
matters for GPU work: "Larger runners are always charged for, even when used by public
repositories".

## What it changes

The verdict becomes `qualifies-with-caveat`, and the binding constraint moves to the job cap:
6 hours per job, 20 concurrent jobs on the Free plan. A job killed at 6 hours cannot use the
rest of an unlimited allowance, so the cap is what decides the shape of a workload.

GPU runners are not free on any plan. They are larger runners, billed per minute, and sold to
Team and Enterprise. A reader who reads "unlimited" and plans a GPU job has misread it.

## The transferable point

A single number on a pricing page usually belongs to one lane. The lane is the finding, and
the public-repository lane is the one that can be used.
