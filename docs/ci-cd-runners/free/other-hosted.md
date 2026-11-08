# Which other hosted CI still has a free allowance worth using?

Eight providers sell hosted CI with a free tier. Two are dead, one has lost its live site, and
four give a pool between 400 and 2,000 minutes a month. The one worth knowing is Codeberg's
Forgejo runners: no published job-count and no minute meter, with each job capped at 2, 5 or 10
minutes.

## The comparison

Sorted by free capacity, in the unit each vendor states.

| provider | free tier | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| Codeberg Forgejo Actions | no published job-count or minute cap; 2, 5 or 10 minutes per job | 10 minutes per job on the medium label | email | qualifies-with-caveat |
| CircleCI | 30,000 credits/month private, 400,000 public | 30,000 credits | email | qualifies-with-caveat |
| Buildkite | 2,000 Linux vCPU-minutes/month, 10 concurrent | 2,000 vCPU-minutes | email | qualifies-with-caveat |
| Azure Pipelines | 1,800 minutes/month, 1 parallel job | 60 minutes per job | card | qualifies-with-caveat |
| GitLab CI | 400 compute minutes/month | 400 minutes | email | qualifies-with-caveat |
| Cirrus CI | 50 credits/month, 10,000 Linux CPU-minutes | 2 hours per free task | email | qualifies-with-caveat |
| AppVeyor | unlimited public projects, no stated minute allowance | 60 minutes per build, 1 concurrent | email | qualifies-with-caveat |
| Codeberg CI (Woodpecker) | free after manual approval | a volunteer reviews the request | email | qualifies-with-caveat |
| Azure Pipelines public | retired; grants end in 2027 | the product is withdrawn | card | dead |
| Travis CI | no self-serve free tier | OSS credits by support email | card | dead |

## Codeberg's Forgejo runners

Codeberg runs three hosted runner labels on a free Codeberg account, in open alpha. The specs come
from Codeberg's own `actions/meta` repository:

| label | CPU | RAM | runtime |
| --- | --- | --- | --- |
| `codeberg-tiny` | 1 | 2 GB | 2 min |
| `codeberg-small` | 2 | 4 GB | 5 min |
| `codeberg-medium` | 4 | 8 GB | 10 min |

Two details make this honest and unusual. The RAM allocation **includes filesystem writes**, so a
job using 1 GB of RAM and writing 1 GB of temporary files counts as 2 GB, and Codeberg grants 2 GB
of additional temporary storage per container to soften that. And each label has a `-lazy` variant
that may wait up to **24 hours** for a slot, which is how Codeberg schedules against load.

Codeberg publishes **no monthly meter and no job-count cap**, and it publishes no ceiling either.
A project can run jobs without a count, each at most ten minutes on the medium label. Ten minutes
on four CPUs is 40 CPU-minutes per job. "No published cap" is what the page supports, and it is
weaker than "unlimited": a documented absence is not a quota, and this one is on an alpha.

The cost is that the runtime is described as "guidelines ... enforced by fair use" rather than a
hard quota, the service is in open alpha and "might break at any time and for an undefined period
of time", and the default image is `ghcr.io/catthehacker/ubuntu:act-latest` with no Docker daemon.
Those three sentences are the reason the verdict is a caveat rather than a qualification.

`Evidence:` `codeberg.org/actions/meta` (read 2026-10-22): the three-row runner table, the RAM
sentence and the lazy variants. The CPU figures are 1, 2 and 4, not 2, 4 and 8;
see [`history/2026-10-22T031523Z/codeberg-runner-cpu-counts-corrected.md`](../../../history/2026-10-22T031523Z/codeberg-runner-cpu-counts-corrected.md). `docs.codeberg.org/ci/actions/` (read 2026-10-22): Forgejo Actions
is available with self-hosted runners and a hosted version "in limited fashion in open alpha".
`docs.codeberg.org/ci/` (read 2026-10-22): the service "might break at any time and for an
undefined period of time".

`Verdict:` qualifies-with-caveat. The second-best free compute lane in this topic after GitHub's
public path, and the least known.

## CircleCI

CircleCI Free gives **30,000 credits a month** for private projects and **400,000 credits a month
for public repositories**, with 5 active users and 30x concurrency. Credits are consumed by machine
size and duration and **expire monthly**. Network and storage beyond the included thresholds are
**420 credits per GB**.

30,000 credits is roughly 6,000 small-Docker minutes, which is 100 hours. That is the largest
private pool in this class. The 400,000-credit public pool is a different product and it is the one
to check first if the work can be public.

The 5,000-credit figure that appears in older comparisons is the pre-2025 plan.

`Evidence:` `circleci.com/pricing/` (read 2026-10-22): the Free row with 30,000 credits, 5 users
and 30x concurrency, and the public-repository figure. `docs.circleci.com/guides/plans-pricing/credits`
(read 2026-10-22): credits are consumed by machine size and duration, and 420 credits per GB beyond
the network and storage thresholds.

`Verdict:` qualifies-with-caveat. The largest private pool and an expiry that wastes whatever is
unused.

## Buildkite

Buildkite Free gives **5 users**, **10 concurrent jobs** and **2,000 Linux vCPU-minutes a month**,
plus 250,000 test executions. Hosted agents beyond that are **USD 0.004 per vCPU-minute**, metered
to the second with no minimum.

The unit matters: a vCPU-minute, not a minute. A job on a 4-vCPU agent spends four units per
wall-clock minute, so 2,000 vCPU-minutes is 500 wall-clock minutes on that shape and 2,000 on a
single-vCPU one.

The free control plane with your own agents is the property worth knowing, because a self-hosted
agent removes the pool entirely and Buildkite becomes a scheduler.

`Evidence:` `buildkite.com/pricing` (read 2026-10-22): the Free column and the per-vCPU-minute rate.

`Verdict:` qualifies-with-caveat. Thirty-three vCPU-hours, and a unit that halves or quarters it
depending on the agent shape.

## Azure Pipelines

The free grant for a private project is **1 free parallel job with 1,800 minutes a month** and
**60 minutes per job**, on an agent with a 10 GB disk. The 360-minute job cap applies only with a
paid parallel job, so the free tier's job ceiling is one hour.

An Azure subscription is required, which means a payment instrument even when the grant is free.
That is a card gate on a free tier, and it is the reason this record's identity cost is `card`
rather than `email`.

`Evidence:` `learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted` (read 2026-10-22): the
1,800-minute, 1-parallel-job and 60-minute figures, and the 360-minute cap on paid parallel jobs.

`Verdict:` qualifies-with-caveat. The smallest per-job cap in this class and a subscription gate.

## GitLab CI

GitLab Free gives **400 compute minutes a month** per namespace, 5 users per top-level group and
10 GiB of repository storage. A job consumes `duration / 60 x cost factor`, and the factor is 1 for
a small Linux runner, 2 for medium, 3 for large, 6 for xlarge and 12 for 2xlarge.

Two project-type discounts change the arithmetic for open source: **0.5** for a public project in
the GitLab for Open Source programme and **0.008** for a public fork of one. At 0.008 one compute
minute buys 125 minutes of job time, which makes a fork of a programme project the cheapest CI
here per unit of work.

The 300,000-minute figure that circulates is the community-contribution programme and it requires
contributing to projects maintained by GitLab. It is not a general allowance.

`Evidence:` `docs.gitlab.com/ci/pipelines/compute_minutes/` (read 2026-10-22): the 400-minute Free
quota, the cost-factor table, the project-type discounts and the community-contribution cap.

`Verdict:` qualifies-with-caveat. Four hundred minutes is 6.7 hours, and a medium runner halves it.

## Cirrus CI

Cirrus gives public repositories **50 compute credits a month**, which its FAQ states equals
**10,000 Linux CPU-minutes** or 500 macOS minutes, with **16 CPUs** on Linux and 8 CPU per task.
A **hard 2-hour limit** applies to free tasks.

The vendor's own two pages disagree on the conversion, and the live site could not be reached on
2026-10-22: `cirrus-ci.org` and `www.cirrus-ci.com` returned NXDOMAIN, `cirrus-ci.com` resolved to
34.117.12.6 and failed the TLS handshake, and the read broker reported the origin unreachable with
a Cloudflare 525. The figures here come from a **2026-04-19 archive capture** of the FAQ, and the
record says so.

The 2-hour task cap matters more than the credit count because it is the ceiling on any single
unit of work.

`Evidence:` probes on 2026-10-22 of `cirrus-ci.org/faq/` (NXDOMAIN), `www.cirrus-ci.com`
(NXDOMAIN) and `cirrus-ci.com` (TLS handshake failure), and the read broker's 502 with a Cloudflare
525. `archive.web.pkgforge.dev/capture/20260419203508/https://cirrus-ci.org/faq/`: the 50-credit,
10,000-CPU-minute, 500-macOS-minute and 2-hour figures.

`Verdict:` qualifies-with-caveat. FreeBSD and macOS access, on a service whose live site was
unreachable the day it was checked.

## AppVeyor

AppVeyor's Open-source plan is USD 0 and its bullet list reads "**Unlimited** public projects", with
**1 concurrent job**, 5 self-hosted jobs and a **60-minute maximum build**. Windows and Linux images
are available.

⚠ **The page says unlimited projects, not unlimited builds.** No monthly minute allowance is
published for that plan, and the 60-minute ceiling applies to every plan ("All plans have maximum
build job execution time of 60 minutes"). A reader should treat the absence of a minute meter as an
unpublished allowance rather than as an unlimited one.

One concurrent job and 60 minutes is a build system for a small project. The concurrency of one is
the number that ends any fan-out idea.

`Evidence:` `appveyor.com/pricing/` (read 2026-10-22): the Open-source column with "Unlimited public
projects", 1 concurrent job and 5 self-hosted jobs, and the FAQ sentence on the 60-minute maximum.

`Verdict:` qualifies-with-caveat. The cheapest real Windows build and the smallest concurrency.

## Codeberg CI on Woodpecker

Codeberg runs a Woodpecker instance at `ci.codeberg.org`. Onboarding needs a request form and a
Codeberg volunteer reviews it. `linux/amd64` is the only build target and there is **no Docker
daemon** inside the hosted runners.

The page publishes no per-job cap; the caps that exist are on the Forgejo Actions runners above
and on the Woodpecker side they are enforced by fair use.

⛔ The **600 free minutes a month** that appears in circulation does not exist. The hosted runners cap
a job at 2, 5 or 10 minutes depending on the label, and the project needs approval.

`Evidence:` `docs.codeberg.org/ci/` (read 2026-10-22): the manual onboarding, the volunteer review,
the amd64-only limit, the absence of Docker-in-Docker, and the sentence that CI "might break at any
time and for an undefined period of time".

`Verdict:` qualifies-with-caveat. A reviewed gate and a service that does not promise availability.

## What did not work

- **Azure Pipelines for public projects**, above: retired, and existing grants end in 2027
  (`documented`, `learn.microsoft.com`).
- **Travis CI**, above: the free trial is withdrawn and OSS credits need a support email
  (`documented`, `docs.travis-ci.com/user/billing-overview/`).
- **Codeberg's "600 free minutes"**: no such allowance exists; the caps are per job
  (`documented`, `docs.codeberg.org/ci/` and `codeberg.org/actions/meta`).
- **Cirrus CI's live site**: three fetch routes failed on 2026-10-22, so its figures rest on a
  dated archive capture (`measured`).
- **GitLab's 300,000 minutes**: it is the community-contribution programme and not a general
  allowance (`documented`, `docs.gitlab.com/ci/pipelines/compute_minutes/`).
- **CircleCI's 5,000 credits**: it is the pre-2025 plan; the page states 30,000
  (`documented`, `circleci.com/pricing/`).
- **Codeberg's 8-core medium runner**: the CPU counts are 1, 2 and 4, not 2, 4 and 8
  (`documented`, `codeberg.org/actions/meta`).
- **AppVeyor as a fan-out**: one concurrent job (`documented`, `appveyor.com/pricing/`).

## Chaining

**Codeberg's uncapped short jobs plus GitHub's unlimited long ones.** `forgejo actions` on
Codeberg for anything under ten minutes, and `GitHub Actions` on a public repository for anything
that needs six hours. The scarce link is that the two do not share a repository, so the code has
to be mirrored.

**A minute pool multiplied across providers.** CircleCI 30,000 credits plus Buildkite 2,000
vCPU-minutes plus GitLab 400 plus Azure 1,800 is roughly 12,000 minutes a month across four
accounts. The scarce link is identity and operations: four CI configurations, four secret stores
and four repository hosts, and none of the pools can be merged into one job.
