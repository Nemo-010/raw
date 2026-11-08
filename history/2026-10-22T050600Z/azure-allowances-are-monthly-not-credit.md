# Azure's free compute is a monthly vCPU-second allowance, and three records carried the credit instead

- **When:** 2026-10-22T05:06:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/azure-container-apps.json` ("USD 5.4 of compute credit each month"), `dossier/compute/azure-windows.json` ("USD 200 of one-time credit"), and the `trial-only` grouping that followed from both
- **Superseded by:** those records, rewritten on 2026-10-22
- **Evidence:** `https://azure.microsoft.com/en-us/pricing/details/container-apps/` and `https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/`, both read 2026-10-22
- **Confidence:** documented

## What we believed

That Azure's free compute was the USD 200 thirty-day credit, and that every Azure
row was therefore a trial. The Container Apps record carried a USD 5.4 monthly
figure it could not source, which is the shape of a credit that had been divided
by something.

## What we found

Azure publishes recurring allowances, and the seed recorded the trial instead.

**Container Apps** states it in one sentence: *"The first 180,000 vCPU-seconds,
360,000 GiB-seconds, and 2 million requests per subscription per month are
free."* That is 50 vCPU-hours and 100 GiB-hours every month, indefinitely. It is
the same allowance as Google's Agent Engine, to the second, which suggests both
are priced off a common serverless convention rather than coincidence.

The mechanism that decides whether it is usable is the activity test: *"A replica
is active when vCPU usage is above 0.01 cores or when data received is above
1,000 bytes per second."* A scaled-to-zero replica costs nothing; a replica
holding an open connection at any real rate is billing, so an idle agent that
polls does not sit inside the free tier.

**Windows virtual machines** carry *"750 hours each of B2ts v2, B2pts v2, and
B2ats v2 burstable VMs free every month for 12 months."* Three families at 750
hours covers three always-on machines for a year, which is a permanent-ish free
tier of a kind the topic had filed as a trial. Twelve months is still a clock,
so the verdict stays `trial-only` for that row and the number names the clock.

**Azure Pipelines** was the same mistake in a different service: one
Microsoft-hosted job at 1,800 minutes a month, plus a self-hosted job with no
minute cap. The self-hosted half is unlimited and is the half that requires
owned hardware.

## How we found it

Four pricing pages read through the broker. Every one of them carried the
allowance in the first screen of the page; none of them required a search.

## What it cost us

Three records were mis-grouped, and the Container Apps figure of USD 5.4 was a
number with no page behind it at all — the exact defect `AGENTS.md` names as the
worst available outcome. It is now replaced by the allowance itself.

## What a future session should do differently

⭐ **A dollar figure that is not on the page is a converted quota, and the
conversion hides the recurrence.** The test that separates the two products: does
the allowance reset every month, and does the page say so in the same sentence as
the number? Container Apps does. The $200 credit does not, because it is spent
once.

⚠ **Read the activity test, not only the allowance.** 180,000 vCPU-seconds sounds
generous until the page defines an active replica as one above 0.01 cores. A
number and its measurement condition are one fact, and the seed pass took half.
