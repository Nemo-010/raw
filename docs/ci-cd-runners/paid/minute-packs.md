# What does a CI minute cost once the allowance is gone?

Four providers publish a per-unit rate beyond the free allowance and they are not comparable units.
GitHub sells minutes by operating system, Buildkite sells vCPU-minutes, CircleCI sells credits and
Weaviate sells dimensions. The answer is that GitHub's USD 0.006 per Linux minute is the cheapest
way to buy general CI time and Buildkite's per-vCPU-minute is the most honest about what it sells.

## The comparison

Sorted by the cost of one wall-clock minute on a single-core-equivalent machine.

| provider | unit | rate | equivalent per wall-clock minute |
| --- | --- | --- | --- |
| GitHub, Linux | per minute | USD 0.006 | USD 0.006 |
| GitHub, Windows | per minute | USD 0.010 | USD 0.010 |
| Buildkite, hosted agents | per vCPU-minute | USD 0.004 | USD 0.004 on 1 vCPU, USD 0.016 on 4 vCPU |
| CircleCI | credits | 420 credits per GB of network or storage | not convertible without a machine size |
| GitLab | compute minute with a cost factor | cost factor 1 to 12 by runner size | the factor is the price |

## The conversion that makes them comparable

GitHub sells a minute of a 2-core Linux machine for USD 0.006. Buildkite sells a minute of one
vCPU for USD 0.004, so a 4-vCPU minute is USD 0.016. The two are only comparable after the core
count is fixed, and neither page states the core count on its rate line.

A reader buying a fixed amount of compute should convert to **core-minutes**:

| provider | rate | core-minutes per USD 1 |
| --- | --- | --- |
| GitHub Linux | USD 0.006 per 2-core minute | 333 |
| Buildkite 4-vCPU agent | USD 0.016 per 4-core minute | 250 |

GitHub is about a third cheaper per core-minute, and Buildkite meters to the second with no
minimum, which matters for a 40-second job.

## GitHub

Linux is **USD 0.006 a minute** and Windows **USD 0.010**. A worked example on the billing page:
5,000 minutes beyond the Team allowance, split 3,000 Linux and 2,000 Windows, is USD 38.

The paid step is small: 2,000 extra Linux minutes is USD 12 a month, which doubles a Free
private repository's allowance.

`Evidence:` `docs.github.com/en/billing/concepts/product-billing/github-actions` (read 2026-10-22):
the per-minute rates and the USD 38 worked example.

`Verdict:` the cheapest published per-minute rate in this topic.

## Buildkite

Hosted agents are **USD 0.004 per vCPU-minute**, metered to the second with no minimums and no
rounding, and "every Linux shape uses the same rate; effective cost scales with vCPU count".

The absence of rounding is a real difference for a CI pipeline of many short jobs, and the
no-minimum term is the one to read twice: a 40-second job on a 1-vCPU agent costs USD 0.0027.

`Evidence:` `buildkite.com/pricing` (read 2026-10-22): the vCPU-minute rate, the no-minimums and
no-rounding terms, and the flat-rate-per-shape sentence.

`Verdict:` the honest unit, at a higher per-core price than GitHub.

## CircleCI

CircleCI sells credits rather than minutes, and credits are consumed by machine size and duration.
The only published conversion on the pages read is that network and storage beyond the included
thresholds cost **420 credits per GB**. That is a storage price and not a compute price, so a
reader cannot compute a per-minute figure from the published material.

30,000 credits a month is quoted in circulation as roughly 6,000 small-Docker minutes, which
implies a small Docker executor costs about 5 credits a minute. That conversion is `reported` and
not on a page read here, so this document states the credit pool and refuses the minute figure.

`Evidence:` `circleci.com/pricing/` (read 2026-10-22): the 30,000-credit Free row.
`docs.circleci.com/guides/plans-pricing/credits` (read 2026-10-22): credits are consumed by machine
size and duration; 420 credits per GB beyond the network and storage thresholds.

`Verdict:` a credit pool whose per-minute rate is not published.

## GitLab

GitLab's paid unit is the compute minute with a cost factor, and the factor is the price. A small
Linux runner is 1, medium 2, large 3, xlarge 6 and 2xlarge 12, so an xlarge minute consumes twelve
of the purchased minutes. A GPU-enabled medium is 7.

The discount structure is the interesting part and it is free rather than paid: **0.5** for a
project in the GitLab for Open Source programme and **0.008** for a public fork of one. At 0.008
one minute buys 125 minutes of job time, which is the cheapest CI in this corpus per unit of work
and it requires an accepted open-source project rather than money.

`Evidence:` `docs.gitlab.com/ci/pipelines/compute_minutes/` (read 2026-10-22): the cost-factor table
and the project-type discounts.

`Verdict:` the cheapest per unit of work if the project is accepted into the open-source programme,
and a plain factor multiplier otherwise.

## What did not work

- **A per-minute comparison across providers without fixing the core count**: GitHub sells a
  2-core minute and Buildkite a 1-vCPU minute, so the raw rate lines are not comparable
  (`inferred` from two documented pages).
- **CircleCI's credits converted to minutes from the pricing page**: the page does not publish the
  conversion, so any figure is `reported` (`documented`, `circleci.com/pricing/`).
- **Buildkite's 2,000 vCPU-minutes as 2,000 minutes**: it is 500 wall-clock minutes on a 4-vCPU
  agent (`documented`, `buildkite.com/pricing`).
- **GitLab's cost factors as a flat rate**: a 2xlarge minute consumes twelve, so the pool shrinks
  by a factor of twelve and not by the machine's speedup (`documented`,
  `docs.gitlab.com/ci/pipelines/compute_minutes/`).
- **Buying minutes to escape the 6-hour job cap**: no per-minute purchase raises a per-job wall
  clock (`documented`, `docs.github.com/en/actions/reference/limits`).

## Chaining

**A paid minute pack behind a free public repository.** `GitHub Actions` on a public repository for
everything that fits, and the private repository's 2,000 minutes plus USD 12 for the overflow. The
scarce link is the 6-hour job cap, which money does not lift.

A vCPU-minute pool with your own agents, the last resort: `Buildkite` as the control plane and a self-hosted
agent on a machine you already pay for. At that point the USD 0.004 rate never applies, because the
agent is yours, and the control plane is free.
