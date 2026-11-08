# What a CI runner costs per minute, and where that topic owns it

Continuous integration is the oldest trick in this corpus: a build pipeline is a
machine that runs for the length of a job and is destroyed afterwards. It is real
compute, it is often free, and it belongs to the `ci-cd-runners` topic. This
document exists for one reason: to state where the boundary is and to stop the
compute census counting a runner twice.

The answer: do not use CI as a compute lane for the workloads assumed here. A runner
is capped at six hours a job on GitHub, the machine is destroyed at the end, and a
scheduled workflow is disabled after 60 days of repository inactivity. It is an
excellent way to run a build and a poor way to serve, hold state, or run a daemon.
The `ci-cd-runners` topic owns the numbers.

## The boundary

| What | Owner | Why |
| --- | --- | --- |
| a GitHub Actions job | `ci-cd-runners` | the minute allowance and the job cap are that topic's |
| a GitLab runner | `ci-cd-runners` | same |
| a Buildkite, Blacksmith or Depot runner | `ci-cd-runners` | same |
| a macOS runner for a signed build | `ci-cd-runners` | same, and the macOS lane is its own market |
| a sandbox created from a workflow | this topic | the workflow is the trigger and the sandbox is the machine |

## What the compute topic records, and why

Three records here exist only to close the boundary. Each carries
`extras.topic_note` naming `ci-cd-runners` as the owner.

**GitHub Actions.** 2,000 minutes a month on GitHub Free, a 6-hour cap per job on
a GitHub-hosted runner, a 256-job matrix per workflow run, a 35-day workflow-run
cap and a 500 KB workflow-file limit (`documented`,
`docs.github.com/en/actions/reference/limits`, read 2026-10-22). It is a creative
substrate that does not survive the 6-hour job cap, and for a serving workload that is
right.

**GitLab Runners.** A free tier with a monthly minute allowance and an ephemeral
per-job machine (`reported`, from the catalogue card).

**CodeSandbox SDK.** The catalogue prices it as a sandbox and the rate card is
labelled legacy, with Together recommending its successor for new integrations
(`documented`, `docs.together.ai/docs/together-code-sandbox-legacy`, read
2026-10-02). It sits on the boundary because a CI system can drive it.

## Why a runner is the wrong lane here

There are three reasons and the first is the one that decides.

⛔ **A runner is destroyed at the end of the job.** There is no disk to keep, no
process to leave running, and no address to come back to. A workload that must
answer at 03:00 cannot live on it.

**The job cap is six hours on GitHub and five days on a self-hosted runner**, and
a job that reaches the cap is terminated and marked failed. A workload that takes
seven hours does not run more slowly; it does not run.

**A scheduled workflow is disabled after 60 days of repository inactivity** on
GitHub. A cron that depends on a repository nobody pushes to stops, silently, after
two months.

⚠ The one thing a runner is genuinely good at is a parallel build: a 256-job matrix
turns a twenty-minute compile into a twenty-minute compile with 256 shards. That is
the `ci-cd-runners` topic's finding and this document does not restate its numbers.

## What a reader should do instead

For a burst workload, a per-second sandbox costs less than a runner's setup and does
not have a job cap. For an always-on process, a VPS with a traffic allowance is the
only shape that works. For a build, the runner is the right tool and it is free.

## What did not work

- **GitHub Actions as an always-on host**: a 6-hour job cap and a destroyed runner.
- **A macOS runner as a cheap macOS machine**: the macOS lane is the most expensive
  in this corpus and the `ci-cd-runners` topic carries it.
- **A workflow as a scheduler**: 60 days of repository inactivity disables it.
- **A self-hosted runner on a free tier**: the 5-day cap is generous and the free
  tier it runs on is the constraint, so the runner adds nothing.

## Chaining

The useful chain is a runner that builds an image and a sandbox or a VPS that runs
it. The runner does the parallel compile, publishes to a registry, and the long-lived
machine pulls the image. Neither half substitutes for the other, and the boundary
between the two topics sits exactly there.
