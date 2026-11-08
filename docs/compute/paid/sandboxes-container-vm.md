# The cheapest sandbox per hour at a named shape

The free lane ends at a session cap, an allowance, or a credit that does not
renew. This document is the path from there: what a sandbox costs once the free
hours are gone, at one shape, so the numbers compare.

Every figure below is computed from a published rate at 2 vCPU and 4 GiB by
`scripts/report/compute-price.py`, which takes the billing model as an input. A
price is a triple: a shape, a horizon, and what is billed. Two of the three are
easy and the third is where the market's disagreements live.

The answer at 300 hours a month, ten hours a day: Agent 37 is USD 2.17, Upstash
Box is USD 3.29 as a keep-alive box, zipbox is USD 4.11, Lizard is USD 4.86 and
boat is USD 5.40. At 730 hours the ranking inverts, because the rows with a floor
become the cheap ones. A burst workload belongs on Agent 37; anything that must
never stop belongs on a VPS and not here.

## The comparison

At 2 vCPU / 4 GiB, list rate, before any credit. `10h` is 300 hours a month and
`24/7` is 730. `Bills` is what the meter counts, which is the column that decides
whether two rows are comparable at all.

| Provider | USD/hour | 10h a month | 24/7 a month | Bills | Disk | Included egress | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| zipbox Small | 0.0137 | 4.11 | 10.00 | running time | 80 GB | not published | qualifies-with-caveat |
| Lizard Small | 0.0162 | 4.86 | 11.83 | running time | 5 GB | 2 TB per account per 30 days | qualifies-with-caveat |
| boat small | 0.0180 | 5.40 | 13.14 | running time | 12 GB | not billed | qualifies |
| Agent 37 | 0.0060 | 2.17 | 4.76 | compute while run, disk while kept | 12 GB max | not published | qualifies-with-caveat |
| Upstash Box Small, keep-alive | 0.0110 | 3.29 | 8.00 | flat per box | 5 GB | not published | qualifies-with-caveat |
| Upstash Box Small, active CPU at 100% | 0.2000 | 60.00 | 146.00 | active CPU | 5 GB | not published | qualifies-with-caveat |
| Vercel Sandbox at 100% CPU | 0.3408 | 102.24 | 248.78 | active CPU plus provisioned memory | 64 GB | 20 GB a month | qualifies-with-caveat |
| Vercel Sandbox at 50% CPU | 0.2128 | 63.84 | 155.34 | active CPU plus provisioned memory | 64 GB | 20 GB a month | qualifies-with-caveat |
| Freestyle | 0.1322 | 39.67 | 96.54 | running time | 32 GB | 50 GB, then USD 0.02/GB | qualifies-with-caveat |
| E2B | 0.1656 | 49.68 | 120.89 | running time | 10 GiB | not published | trial-only |
| Daytona | 0.1656 | 49.68 | 120.89 | running time | 5 GiB free | not published | qualifies-with-caveat |
| Modal Sandbox | 0.2380 | 71.39 | 173.71 | running time at the non-preemptible rate | 1 TiB volume | 1 TiB, then USD 0.04/GiB | qualifies-with-caveat |

⛔ Four of these rows cannot be compared on the `USD/hour` column alone, and the two
catalogues disagreed on 90 of 153 providers for exactly that reason. Upstash
at 100 per cent CPU is USD 0.20 an hour and as a keep-alive box it is USD 0.011;
those are the same page and different products. Vercel at 100 per cent CPU is
USD 0.34 and at 50 per cent it is USD 0.21; those are the same product and two
utilisations. Agent 37's hour is compute alone and its bill carries a disk that
runs every month whether the box does or not.

## Agent 37

USD 0.80 per vCPU plus USD 0.70 per GB of RAM plus USD 0.09 per GB of disk per
730-hour month, metered by the minute (`documented`, `agent37.com/pricing`, read
2026-10-22). At 2 vCPU, 4 GB and 4 GB of disk the month at 730 running hours is
USD 4.76, and the 300-hour bill is USD 2.17: USD 1.81 of compute and USD 0.36 of
disk for the month the disk is kept.

⚠ USD 1.81 is the compute alone. A reader who budgets it is USD 0.36 light every
month, which is small and is still the shape of
the error that makes a corpus wrong.

The ceiling is 4 vCPU on every instance type, and a create that asks for more
cores keeps the memory it asked for and comes back with 4 vCPU at the price above.
The request does not fail; it provisions a smaller machine.

Evidence: `agent37.com/pricing` and `agent37.com/docs/agents-api/instance-sizing`
(read 2026-10-22). Verdict: the cheapest metered sandbox and a silent core
ceiling.

## Upstash Box

Small is 2 vCPU, 4 GB and 5 GB of disk at USD 0.10 per active CPU hour, or USD 8
a month for a keep-alive box (`documented`, `upstash.com/pricing/box`, read
2026-10-22). Medium is USD 0.20 a core-hour or USD 16 a month, and Large USD 0.40
or USD 32.

The page states that a customer pays the lower of full CPU usage and the matching
keep-alive plan. That is what makes two rows necessary: an agent that works an hour
a day pays the keep-alive USD 8, and one that drives both cores for a week pays
metered. At 100 per cent CPU for 300 hours the metered bill is USD 60 and the
keep-alive is the cheaper of the two.

⚠ 5 GB of disk on the Small shape is the tightest resource here.

Evidence: `upstash.com/pricing/box` (read 2026-10-22). Verdict: two products on
one page, and the cheaper one depends on duty cycle.

## zipbox

Small is 2 vCPU, 4 GB and 80 GB of disk at USD 0.0137 an hour, billed per second,
and paused boxes cost USD 0 (`documented`, `zipbox.ai/pricing`, read 2026-10-22).
Tiny is USD 0.0068, Medium USD 0.0274 and Large USD 0.0548 for 6 vCPU, 16 GB and
320 GB.

The 80 GB of disk is sixteen times Upstash's 5 GB and six times Lizard's 5 GB at a
similar rate. For a workload with a working set, that is the decision.

⚠ Three terms are unpublished: egress, the disk deletion clock and any session
cap. The record carries them as gaps rather than zeros.

Evidence: `zipbox.ai/pricing` (read 2026-10-22). Verdict: the most disk per dollar
and three unknown terms.

## Lizard

Small is USD 0.0162 an hour for 2 vCPU, 4 GB and a 5 GB workspace, Medium
USD 0.0324 with 20 GB, Large USD 0.0648 with 50 GB (`documented`,
`lizard.build/pricing` and `lizard.build/docs/platform/limits/`, read 2026-10-22).
Billing is per second including idle time.

⭐ Sandbox egress has no separate per-GB charge and the allowance is 2 TB per
account over a rolling 30 days. That is the largest included traffic allowance of
any sandbox here and it is the reason to choose Lizard for a crawl that also
serves.

Pro is USD 19 a month with USD 19 of usage included.

⚠ The SDK and CLI default a sandbox's lifetime to five minutes; the raw API
defaults to no expiration.

Evidence: `lizard.build/pricing` and `lizard.build/docs/platform/limits/` (read
2026-10-22). Verdict: the best egress terms in the class and the smallest disk on
the entry shape.

## boat

`small` is USD 0.018 for 2 vCPU, 4 GB and 12 GB; `default` USD 0.036 for 4 vCPU,
8 GB and 50 GB; `large` USD 0.072 and `xlarge` USD 0.200 (`documented`,
`docs.boat.dev/pricing`, read 2026-10-22). Billed per second, and a stopped
sandbox costs no machine time.

boat does not bill egress, gives every sandbox a public IPv6 address and outbound
IPv4, and publishes a port on a stable HTTPS URL. It is the only cheap sandbox here
that can answer an inbound request without a tunnel.

The floor is the plan. The USD 20 plan is credit rather than a fee, so a light
month bills USD 20 while `small` at 300 hours is USD 5.40. For this shape the plan
is the bill.

⚠ A stopped sandbox keeps its disk for 14 days, then the data is deleted and the
sandbox cannot resume. A named snapshot past the first 10 costs USD 1.70 a month.

Evidence: `docs.boat.dev/pricing` and `docs.boat.dev/hosting` (read 2026-10-22).
Verdict: the best network of any cheap sandbox, a 14-day state clock and a plan
floor above the metered price.

## Vercel Sandbox

USD 0.128 per active CPU hour and USD 0.0212 per GB-hour of provisioned memory on
Pro, with Hobby carrying 5 active-CPU hours and 420 GB-hours a month
(`documented`, `vercel.com/docs/sandbox/pricing`, read 2026-10-22). Active CPU
excludes time waiting on I/O; provisioned memory bills for the whole run.

That split produces two figures and both are right: USD 102.24 for 300 hours at
100 per cent CPU and USD 63.84 at 50 per cent. Neither figure states which
utilisation it assumes, which is why they look like a conflict.

For an agent that spends most of its time waiting on a model, this is the cheapest
model in the table. For one that computes, it is not.

Evidence: `vercel.com/docs/sandbox/pricing` (read 2026-10-22). Verdict: metered
honestly and reported ambiguously.

## Freestyle

USD 0.04032 per vCPU-hour and USD 0.0129 per GiB-hour, with 200 vCPU-hours and
400 GiB-hours a month included on every plan; on Free the allowances are hard
stops, on paid they are billed past (`documented`, `freestyle.sh/pricing`, read
2026-10-22). Hobby is USD 50 a month and Pro USD 500, both credited against usage.

Persistent VMs and persistent snapshots require Hobby or Pro, which is the line
between a tool and a host and it costs USD 50.

Evidence: `freestyle.sh/pricing` (read 2026-10-22). Verdict: an exact allowance
and the cheapest way past it is USD 50.

## E2B

USD 0.000014 per vCPU-second and USD 0.0000045 per GiB-second, which is USD 0.1656
an hour at 2 vCPU and 4 GiB (`documented`, `e2b.dev/pricing`, read 2026-10-22).
Storage is free and Hobby includes 10 GiB.

The reason to pay E2B is the pause. A paused sandbox is kept indefinitely with no
time-to-live, and it saves the filesystem and the memory, so a workload that runs
an hour at a time behaves like a schedule rather than a stopwatch.

⚠ Hobby caps a session at 1 hour, so the pause is not optional for anything longer.

Evidence: `e2b.dev/pricing` and `e2b.dev/docs/sandbox/persistence` (read
2026-10-22). Verdict: the best lifecycle in the class and a rate in the middle.

## Daytona

USD 0.0504 per vCPU-hour, USD 0.0162 per GiB-hour and USD 0.000108 per GiB-hour
of storage after the first 5 GiB (`documented`, `daytona.io/pricing`, read
2026-10-22). At 2 vCPU and 4 GiB that is USD 0.1656 an hour and USD 49.68 for 300
hours, before the USD 200 trial credit.

A USD 2,000 figure for Daytona is a plan floor. The live page is per-second metered
with no plan fee, and the number that matters is the 15-minute default auto-stop, which
fires even while internal processes run.

Evidence: `daytona.io/pricing` and `daytona.io/docs/en/sandboxes/` (read
2026-10-22). Verdict: fast, metered, and stopped when nobody is watching.

## Modal

Sandboxes are priced at the non-preemptible Function rate, which is 3x the list
price (`documented`, `modal.com/pricing`, read 2026-10-22). The table publishes
USD 0.00003942 per physical core-second and USD 0.00000667 per GiB-second, and it
states that a physical core is 2 vCPU. At 2 vCPU and 4 GiB the shape is one core
plus four GiB, so the rate is USD 0.2380 an hour and 300 hours is USD 71.39. The
same shape at the preemptible rate is USD 0.0791 an hour.

Modal is here because it carries the largest recurring credit in the market and
because its rate is the one most likely to be misread. A reader who compares
Modal's Function rate to a sandbox rate is comparing two products on one page.

⚠ The default maximum lifetime is 5 minutes and containers are kept 60 seconds
after the last input, billed.

⚠ The 3x multiplier on a 2 vCPU shape is not what makes this row expensive. At
USD 0.2380 an hour against E2B's USD 0.1656 it is 1.4 times the rate, and the
figure that made it look like 4.6 times was a rate for the 8 vCPU shape. What
still makes it expensive is the same thing: Modal bills the non-preemptible rate
and the cheapest rows here do not.

Evidence: `modal.com/pricing` and `modal.com/docs/guide/sandbox` (read 2026-10-22).
Verdict: a mid-priced sandbox on the largest recurring credit in the market.

## What did not work

- **Fly.io**: no free tier and no cheap sandbox lane. The cheapest always-on
  Machine is USD 2.19 a month for 256 MB.
- **Run Cloud**: withdrawn from new organizations.
- **OpenComputer at 2 vCPU**: USD 0.0063 a minute is USD 0.378 an hour, twenty
  times the cheap tier. Its USD 20 and USD 200 plans grant 10 times their price in
  credits, which moves the effective rate and not the list rate.
- **CodeSandbox SDK**: the rates are labelled legacy and Together recommends its
  successor for new integrations.
- **Docker Sandboxes**: USD 0.140 an hour for the smallest published size, which
  is ten times zipbox for a shape this table cannot match.
- **Cua** (self-hosted): its hosted Fleet rate is no longer published. The pricing page states
  the offer now connects agents to the customer's own compute, so there is no managed rate.

## Chaining

zipbox for the disk and Lizard for the egress is the pairing the terms suggest: a
crawl writes to an 80 GB box and serves from an account with 2 TB included. boat
is the single-provider answer if inbound traffic is needed, because it is the only
row here that publishes a port. Neither chain removes the other's clock, so state
leaves through object storage either way.

## Superseded claims

Figures this document has replaced, with the evidence that replaced them, are dated in
[`compute-seed-claims-superseded.md`](../../../history/2026-10-22T030705Z/compute-seed-claims-superseded.md).
