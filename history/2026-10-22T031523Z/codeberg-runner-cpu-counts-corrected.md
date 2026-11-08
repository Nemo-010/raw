# The census gave Codeberg 8-core runners and the vendor table gives 4

- **When:** 2026-10-22T03:15:23Z
- **Status:** corrected
- **Supersedes:** `.tmp/work/recon-extras/CI-CD-RUNNERS.md` §Verified inventory, the
  Codeberg Forgejo Actions row
- **Superseded by:** `docs/ci-cd-runners/free/other-hosted.md` §Codeberg's Forgejo runners
- **Evidence:** `codeberg.org/actions/meta` (read 2026-10-22), the "Available runners" table
- **Confidence:** documented

## What we believed

The census recorded Codeberg's three hosted runners as "2/4/8 cores at 2/5/10 minutes" and
attributed the figure to Codeberg's `actions/meta` repository, which it had not opened. The
per-job clock was right and the CPU counts were not.

## What we found

The vendor table gives 1, 2 and 4 CPUs, not 2, 4 and 8:

| label | CPU | RAM | runtime |
| --- | --- | --- | --- |
| `codeberg-tiny` | 1 | 2 GB | 2 min |
| `codeberg-small` | 2 | 4 GB | 5 min |
| `codeberg-medium` | 4 | 8 GB | 10 min |

The 8 in the census is the medium runner's **RAM in gigabytes**, and the 2 is the tiny runner's
RAM. The row appears to have been built from the RAM column with the CPU column's units dropped,
which produced a machine that is twice as fast at every tier.

The same page carries a second detail the census did not have: **the RAM allocation includes
writes to the filesystem**, so a job using 1 GB of RAM and writing 1 GB of temporary files counts
as 2 GB, with 2 GB of extra temporary storage granted per container.

## How we found it

The census named its own gap, so the repository was opened. `codeberg.org/actions/meta` answered
200 through the read broker with the runner table in it.

## What it cost us

Nothing, because the check was one page. The cost would have been a recommendation: ten minutes on
four CPUs is 40 CPU-minutes per job, and ten minutes on eight CPUs is 80. A reader planning a
fan-out on the census figure would have provisioned for twice the capacity that exists.

## What a future session should do differently

**A row that cites a repository it did not open is a row with no evidence.** The census did this
once and got the most-repeated number in the topic wrong in the other direction. Open the named
source before recording a spec, and when a spec has both a CPU and a RAM column, check which one
the numbers came from.
