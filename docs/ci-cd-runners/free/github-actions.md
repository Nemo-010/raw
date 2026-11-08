# Is GitHub Actions really unlimited, and for whom?

Yes on a public repository and no on a private one, and that single fact decides the strategy.
The public path has no minute cap and a hard 6-hour job ceiling with 20 concurrent jobs. The
private path has 2,000 minutes and the same 6-hour ceiling. Minutes are not the scarce resource;
concurrency and the per-job clock are.

## The comparison

Two products on one platform. Sorted by how much work you can put through them.

| product | free tier | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| public repository, standard runner | no minute cap | 6 hours per job, 20 concurrent jobs | email | qualifies |
| private repository, Free plan | 2,000 minutes/month | 2,000 minutes, 500 MB artifacts | email | qualifies-with-caveat |

## The public path

GitHub's billing documentation states it plainly: "GitHub Actions usage is free for self-hosted
runners and for public repositories that use standard GitHub-hosted runners". The only exception
on the same page is larger runners, which "are always charged for, even when used by public
repositories".

The caps that replace the meter, all from the limits reference read on 2026-10-22:

- **6 hours of execution per job** on a GitHub-hosted runner. A job that reaches it "is terminated
  and fails". A self-hosted job gets 5 days instead.
- **35 days per workflow run**, including waiting and approval time.
- **256 jobs per workflow run** from a matrix, on hosted and self-hosted runners alike.
- **20 concurrent jobs** on GitHub Free, with **5 concurrent macOS** jobs and no GPU runners.
- **500 KB per workflow file**, above which no run starts.
- **100 runs queued per concurrency group** when `queue: max` is used.

The runner is an Ubuntu 24.04 image with **4 vCPU, 16 GB of RAM and a 14 GB SSD**. A single-CPU
`ubuntu-slim` label exists at 1 vCPU and 5 GB.

⭐ Do the multiplication, and keep the units straight. **20 concurrent slots is a stock, not a
rate.** The stock is 20 jobs in flight at up to 6 hours each, which is 120 runner-hours existing at
one instant. The flow is bounded by the concurrency limit over a day: **20 slots x 24 h = 480
runner-hours a day**, and that is the ceiling when the queue never empties. No minute meter applies
while the repository is public.

⚠ **2,880 runner-hours a day is a units error.** Multiplying the 120-hour stock by 24 gives
runner-hours squared per day, not a rate. A figure of 2,880 a day would need 120 concurrent
slots, and GitHub Free provides 20.

`Evidence:` `docs.github.com/en/billing/concepts/product-billing/github-actions` (read 2026-10-22):
the free-for-public sentence and the larger-runner exception. `docs.github.com/en/actions/reference/limits`
(read 2026-10-22): the 6-hour and 5-day job limits, 35 days per run, 256 jobs per matrix, 500 KB
per workflow file, and the concurrency table. `docs.github.com/en/actions/reference/runners/github-hosted-runners`
(read 2026-10-22): the 4 vCPU / 16 GB / 14 GB shape.

`Verdict:` qualifies. The largest free compute lane in this corpus, with a public repository as
its price.

## The private path

A private repository on GitHub Free gets **2,000 minutes a month**, **500 MB of artifact storage**
and **10 GB of cache per repository**. Pro and Team raise minutes to 3,000 and artifacts to 1 GB
and 2 GB; Enterprise is 50,000 minutes and 50 GB of artifacts.

2,000 minutes is **33 hours of one runner a month**, and the 6-hour job ceiling applies
independently. A single six-hour job spends 18% of the month, so three of them is over half.

Beyond the allowance, Linux is **USD 0.006 a minute** and Windows USD 0.010, so 2,000 extra Linux
minutes is USD 12 in a month.

Minutes are charged to the repository owner and not to whoever triggered the run, which matters if
a public repository's workflow is triggered by a stranger.

⚠ **What happens when the pool runs out is the number a reader plans against, and it is a wall.**
The billing page states: "If your account does not have a valid payment method on file, usage is
blocked once you use up your quota." So a Free account with no card stops building when the 2,000
minutes are gone, and it does not run up a bill. Adding a card is what converts the wall into
USD 0.006 a minute.

`Evidence:` the same two pages, plus the Free / Pro / Team / Enterprise table on the billing page
giving 500 MB and 2,000 minutes for Free, and the sentence about blocked usage without a payment
method.

`Verdict:` qualifies-with-caveat. Thirty-three hours a month is a real allowance and the per-job
clock still binds first for any single long job.

## The storage pools, which are three and not one

This is where a build loses its output, and the three pools are easy to conflate.

- **Artifacts: 500 MB on Free**, and the default retention is **90 days**. Retention is
  configurable per repository and per artifact.
- **Packages and container images: the same 500 MB pool.** The billing page says "The storage
  amounts shown are shared with GitHub Actions artifacts. This means your total storage across
  Packages and Actions artifacts cannot exceed the included amount for your plan." So a repository
  that publishes an image and keeps build artifacts is spending one budget twice.
- **Cache: 10 GB per repository**, a separate pool, and **any entry not accessed in over 7 days is
  removed**. Beyond 10 GB GitHub evicts oldest-first by last access, which the docs warn can cause
  cache thrashing. Raising the limit beyond 10 GB is available only to accounts with a payment
  method.

Cache uploads are rate limited to **200 a minute** and downloads to **1,500 a minute** per
repository, with 400 deletes a minute. A build that restores a cache matrix of a thousand entries
meets that ceiling.

`Evidence:` `docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching` (read
2026-10-22): 10 GB default, 7-day eviction, oldest-first beyond the limit, and the payment-method
requirement to raise it. `docs.github.com/en/billing/concepts/product-billing/github-packages`
(read 2026-10-22): the shared pool sentence and the worked example where a 500 MB package consumes
500 MB of storage and each download consumes 500 MB of transfer.
`docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts` (read
2026-10-22): "By default, GitHub stores build logs and artifacts for 90 days".

`Verdict:` the storage is the constraint and the compute is not, and the 500 MB shared pool is
the smallest number on the platform.

## Using it as general compute

The honest test: a job is a 4 vCPU machine for at most six hours, with no inbound connection, that
is destroyed at the end. That is a batch worker.

What it can do is fetch inputs, compute, and push results somewhere durable while it still exists.
What it cannot do is serve, hold a socket open, or survive the six-hour boundary. A 7-hour job is
not possible at any price on a hosted runner, and the failure is termination rather than a bill.

Three alternative routes and what each costs:

- **Split the work into six-hour shards** and carry state through artifacts or an external store.
  The scarce link is 500 MB of artifacts shared with everything else.
- **Use a 256-job matrix** as a fan-out. 256 jobs of up to six hours is **1,536 runner-hours** at
  no minute cost on a public repository. The scarce link is 20 concurrent jobs: 256 divided by 20 is
  12.8, so the matrix runs in **thirteen waves of 20**, which is **78 hours of wall clock** at the
  six-hour job ceiling.
- Attach a self-hosted runner to the free control plane, the last resort. The 5-day job limit replaces the
  6-hour one and the machine becomes the cost. This is the route that stops being free, and it is
  covered in [`self-hosted.md`](self-hosted.md).

`Evidence:` the 6-hour and 5-day job limits, the 256-job matrix cap and the concurrency table, all
from `docs.github.com/en/actions/reference/limits` (read 2026-10-22).

`Verdict:` a batch worker with a hard clock, not a server.

## What did not work

- **Unlimited minutes as the win**: minutes are not the constraint. Concurrency times the per-job
  cap is, and a seven-hour job is impossible (`documented`,
  `docs.github.com/en/actions/reference/limits`).
- **Larger runners on a public repository**: always charged, even when the repository is public
  (`documented`, `docs.github.com/en/billing/concepts/product-billing/github-actions`).
- **A 300-job matrix**: 256 jobs per workflow run is the ceiling on hosted and self-hosted runners
  alike (`documented`, `docs.github.com/en/actions/reference/limits`).
- **Keeping a build image in GHCR and artifacts in Packages**: one 500 MB pool for both
  (`documented`, `docs.github.com/en/billing/concepts/product-billing/github-packages`).
- **Raising the cache above 10 GB on Free**: it needs a payment method
  (`documented`, `docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching`).
- **A scheduled workflow as a reliable cron**: a scheduled workflow is automatically disabled after
  60 days in which the repository has no activity (`documented`,
  `docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows`).

## Chaining

**Free compute with output that has somewhere to go.** `GitHub Actions` on a public repository,
then `Cloudflare R2` for the artifact. The scarce link is the 500 MB artifact pool, so the output
must leave the platform within the job. Actions downloading a package from a private repository
with `GITHUB_TOKEN` does not consume the transfer allowance, which is the detail that makes this
chain work.

**A 1,536-runner-hour fan-out.** A 256-job matrix on a public repository, running in thirteen waves
of 20 and 78 hours of wall clock. The scarce link is the six-hour job ceiling, which sets the
duration of each wave, then the 20-slot concurrency, which sets how many waves are needed. The
day's throughput is 480 runner-hours, so this matrix is a little over three days of the full lane.
