# Which sandbox can I hold a session open in tonight

A sandbox is a container or a microVM that starts in under a second, bills by the
second, and is meant to be thrown away. It is the cheapest compute in this market
and the least durable: the price is low because the machine does not exist between
runs. The question that decides usability is not the rate but the clock, and there
are three of them on every page. A session cap ends a run. An idle reap ends a
quiet run. A disk clock deletes the state after the machine is gone.

The answer: use a sandbox as a tool, not as a host. The three that
publish a free allowance worth having are Freestyle (200 vCPU-hours a month,
hard stop, no persistent VMs), E2B (USD 100 one-time, 1 hour per session but an
indefinite pause) and Upstash Box (5 CPU hours a month, which is 2.5 hours of a
2 vCPU box). None of them can serve traffic. For a crawl that runs an hour at a
time, E2B's pause is the mechanism that makes the one-hour cap survivable.

## The comparison

Sorted by the free allowance a reader can obtain tonight without a card. `Held`
is the 24/7 figure at the record's entry shape. `Binds` is the clock that stops it.

| Provider | Free tier | Binds | Identity | At 300 h | Held 24/7 | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Freestyle | 200 vCPU-h and 400 GiB-h a month, hard stop | no persistent VMs, no snapshots | email | USD 39.67 | USD 96.54 | qualifies-with-caveat |
| E2B | USD 100 one-time, 20 concurrent | 1 hour per session | email | USD 49.68 | USD 120.89 | trial-only |
| Upstash Box | 5 CPU hours a month | 5 GB disk on Small | email | USD 3.29 | USD 8.00 | qualifies-with-caveat |
| Daytona | USD 200 one-time | 15 minutes idle by default | email | USD 49.68 | USD 120.89 | qualifies-with-caveat |
| Vercel Sandbox | 5 active-CPU hours a month | 45-minute maximum session | email | USD 102.24 | USD 248.78 | qualifies-with-caveat |
| Modal | USD 30 a month, recurring | 5-minute default lifetime | email | USD 71.39 | USD 173.71 | qualifies-with-caveat |
| Lizard | 7-day trial, USD 5 | 5-minute SDK default lifetime | card | USD 4.86 | USD 11.83 | qualifies-with-caveat |
| Agent 37 | USD 5 after a card | disk bills while stopped | card | USD 2.17 | USD 4.76 | qualifies-with-caveat |
| zipbox | USD 25 after a USD 5 top-up | 6 vCPU ceiling | card | USD 4.11 | USD 10.00 | qualifies-with-caveat |
| boat | none; USD 20 plan is credit | disk deleted 14 days after stop | card | USD 5.40 | USD 13.14 | qualifies |
| Cloudflare Containers | none | Workers Paid at USD 5 a month | card | USD 51.84 | USD 126.14 | paid-only |
| Run Cloud | withdrawn | unreachable | card | USD 0.00 | USD 0.00 | dead |

Both columns are the same 2 vCPU / 4 GiB shape from `paid/sandboxes-container-vm.md`
and from `scripts/report/compute-price.py`, so a reader can compare a free allowance
against the paid rate it runs out into. `At 300 h` is ten hours a day for a month;
`Held 24/7` is 730 hours.

Two rows carry a correction. Run Cloud was the cheapest row at
USD 0.00 and the product is closed to new organizations. Lizard was recorded at USD 0.009 an
hour and at USD 6.55 a month, and the live page says USD 0.0162
for the Small shape, so both figures were stale.

## Freestyle

The free tier is stated in units that make the ceiling arithmetic exact: 200
vCPU-hours and 400 GiB-hours of memory a month, with data transfer at 50 GB. On a
2 vCPU shape that is 100 hours a month, which is 3.3 hours a day. The allowances
are the same on every plan, and on Free they are hard stops rather than paid
overage, so an exhausted allowance refuses work instead of billing (`documented`,
`freestyle.sh/pricing`, read 2026-10-22).

What it cannot do is hold state. The free column marks Persistent VMs and
Persistent Snapshots as forbidden, and custom sizing too, so the shape is fixed at
4 vCPU, 8 GiB and 32 GiB of disk. The compute rate is USD 0.04032 per vCPU-hour
and USD 0.0129 per GiB-hour, which is USD 0.1322 an hour at 2 vCPU / 4 GiB gross.
Egress is USD 0.02 per GB after 50 GB, so a TiB is USD 20.

Evidence: `freestyle.sh/pricing` (read 2026-10-22) states the three rates, the
three included columns, the Free column's four prohibitions, and hard-stop
behaviour. Verdict: the best free compute allowance in this class and the worst
free state retention.

## E2B

Hobby costs nothing a month, carries a one-time USD 100 in usage credits, allows
20 concurrent sandboxes and 10 GiB of storage, and does not need a credit card
(`documented`, `e2b.dev/pricing`, read 2026-10-22). The rate is USD 0.000014 per
vCPU-second and USD 0.0000045 per GiB-second, which is USD 0.1656 an hour at the
default 2 vCPU / 4 GiB shape.

The one-hour session cap is real and it is not the end of the story. A sandbox can
be paused, and a paused sandbox is kept indefinitely with no time-to-live and no
automatic deletion (`documented`, `e2b.dev/docs/sandbox/persistence`, read
2026-10-22). The pause saves the filesystem and the memory, so a resumed sandbox
continues mid-process rather than replaying its setup. A pause can be refused with
HTTP 503 when the node is still finishing an earlier snapshot; the sandbox keeps
running and nothing is lost.

Evidence: `e2b.dev/pricing` and `e2b.dev/docs/sandbox/persistence` (read
2026-10-22). Verdict: the best mechanism in this class for surviving a session cap
and the worst fit for a workload that must answer a request at an arbitrary time.

## Upstash Box

Free is USD 0, 10 concurrent boxes, 5 CPU hours a month and USD 1 of LLM token
budget. Small is 2 vCPU, 4 GB and 5 GB of disk, billed at USD 0.10 per active CPU
hour or USD 8 a month for a keep-alive box (`documented`, `upstash.com/pricing/box`,
read 2026-10-22). Five CPU hours at 2 vCPU is 2.5 hours of a Small box a month.

The page carries two products and both price columns are right:
USD 3.29 is metered active CPU and USD 8.82 is the keep-alive. The 5 GB disk is
the tightest resource on the page, and standard boxes auto-pause when idle, which
is what makes metered billing cheap and unusable for a service.

Evidence: `upstash.com/pricing/box` (read 2026-10-22) states the plan table, the
three sizes, and the auto-pause and keep-alive split. Verdict: a cheap batch tool
with too little disk to hold a dataset.

## Daytona

The page says USD 200 in free compute included and a free trial with no credit
card (`documented`, `daytona.io/pricing`, read 2026-10-22). The rate is USD 0.0504
per vCPU-hour, USD 0.0162 per GiB-hour and USD 0.000108 per GiB-hour of storage
after the first 5 GiB, billed per second. At 2 vCPU / 4 GiB that is USD 0.1656 an
hour, and 300 hours is USD 49.68.

The number that decides it is not on the pricing page. The auto-stop interval
defaults to 15 minutes of inactivity and triggers even while internal processes
run (`documented`, `daytona.io/docs/en/sandboxes/`, read 2026-10-22). The timer
resets only for external interactions: lifecycle updates, preview requests, SSH
connections and toolbox API calls. A long computation with no client attached is
stopped after fifteen minutes. Setting the interval to zero disables it.

Evidence: `daytona.io/pricing` and `daytona.io/docs/en/sandboxes/` (read
2026-10-22). Verdict: the fastest sandbox here and the one most likely to stop
work that nobody is watching.

## Vercel Sandbox

Hobby includes 5 hours of active CPU, 420 GB-hours of provisioned memory, 5,000
creations and 10 concurrent sandboxes a month, with a 45-minute maximum session
(`documented`, `vercel.com/docs/sandbox/pricing`, read 2026-10-22). Active CPU is
time actually using the processor; time waiting on I/O does not count, which is
why the two columns differ by 38 per cent.

Five hours of active CPU a month is very little real work. The 64 GB of ephemeral
NVMe is generous and the 45-minute session is the cap that matters.

Evidence: `vercel.com/docs/sandbox/pricing` (read 2026-10-22). Verdict: cheap for
an agent that waits on a model and expensive for one that computes.

## Modal

Starter has no monthly fee and includes USD 30 of compute a month, and the credit
recurs (`documented`, `modal.com/pricing`, read 2026-10-22). The mechanism that
decides the bill is a 3x multiplier on CPU and memory for non-preemptible
resources, and Modal states that Sandboxes are priced at the non-preemptible rate.
The page publishes USD 0.00003942 per physical core-second and USD 0.00000667 per
GiB-second, and it says a physical core is 2 vCPU. So 2 vCPU is one core, and the
2 vCPU / 4 GiB shape costs 1 x 0.00003942 x 3600 + 4 x 0.00000667 x 3600 =
USD 0.2380 an hour. USD 30 is about 126 hours at that rate.

A sandbox has a default maximum lifetime of 5 minutes, extendable to 24 hours via
the timeout argument (`documented`, `modal.com/docs/guide/sandbox`, read
2026-10-22). Containers are kept for 60 seconds after the last input and that time
is billed. Volumes include up to 1 TiB free, which is the largest free volume in
this class.

Two recorded figures for this row differ by 12x because one applied the multiplier
and the other did not. The page confirms the multiplier.

Evidence: `modal.com/pricing`, `modal.com/docs/guide/sandbox` and
`modal.com/docs/guide/sandbox-networking` (read 2026-10-22). Verdict: the largest
recurring credit and the most expensive way to spend it.

## Lizard

Small is 2 vCPU, 4 GB and a 5 GB workspace at USD 0.0162 an hour, billed per
second including idle time; Medium is the default at USD 0.0324 and Large is
USD 0.0648 (`documented`, `lizard.build/pricing` and
`lizard.build/docs/platform/limits/`, read 2026-10-22). Sandbox egress has no
per-GB charge and the allowance is 2 TB per account over a rolling 30 days, which
is the largest included traffic allowance in the class after Cloudflare.

Two traps. A card is required to start the 7-day trial, and the SDK and CLI
default a sandbox's lifetime to five minutes where the raw API defaults to no
expiration. A caller who creates a sandbox from the SDK and walks away has five
minutes.

Evidence: `lizard.build/pricing` and `lizard.build/docs/platform/limits/` (read
2026-10-22), including the lifetime table. Verdict: the best egress allowance per
dollar and a lifetime default that will catch an agent.

## Agent 37

The rate is USD 0.80 per vCPU plus USD 0.70 per GB of RAM plus USD 0.09 per GB of
disk per 730-hour month, metered by the minute, and a VM costs 2.5x compute
(`documented`, `agent37.com/pricing`, read 2026-10-22). At 2 vCPU / 4 GB / 4 GB
that is USD 4.76 a month at 730 running hours. At 300 hours the bill is USD 2.17, because the disk still
bills for the month.

The pricing page does not carry the ceiling: 4 vCPU is the maximum on every instance
type, and a create that asks for more cores keeps the memory it asked for and
comes back with 4 vCPU at the price above (`documented`,
`agent37.com/docs/agents-api/instance-sizing`, read 2026-10-22). The request does
not fail; it silently provisions a smaller machine.

The disk bills while the instance is stopped and stops billing on delete, so a
long-lived workspace costs its disk alone when idle. That is the cheapest idle
state in this class.

Evidence: `agent37.com/pricing` and `agent37.com/docs/agents-api/instance-sizing`
(read 2026-10-22). Verdict: the cheapest credible per-hour sandbox and a silent
core ceiling.

## zipbox

Tiny is USD 0.0068, Small USD 0.0137 for 2 vCPU / 4 GB / 80 GB, Medium USD 0.0274
and Large USD 0.0548 for 6 vCPU / 16 GB / 320 GB, billed per second, and paused
boxes cost nothing (`documented`, `zipbox.ai/pricing`, read 2026-10-22). A new
account gets USD 25 in credit with a one-time USD 5 top-up, and the card is saved
for auto top-up.

The 80 GB of disk on the Small shape is the largest disk per dollar in the cheap
tier by a factor of six against Lizard's 5 GB. The page states nothing about
egress, the disk deletion clock or a session cap, so those are gaps rather than
zeros.

Evidence: `zipbox.ai/pricing` (read 2026-10-22). Verdict: the most disk for the
money and three unpublished terms.

## boat

`small` is USD 0.018 for 2 vCPU / 4 GB / 12 GB, `default` USD 0.036 for
4 vCPU / 8 GB / 50 GB, `large` USD 0.072 and `xlarge` USD 0.200, all billed per
second (`documented`, `docs.boat.dev/pricing`, read 2026-10-22). A stopped sandbox
costs no machine time and boat does not bill egress. Every sandbox gets a public
IPv6 address, outbound IPv4, and a public HTTPS URL per hosted port.

The disk clock is the constraint and it is short: a stopped sandbox keeps its disk
for 14 days, then boat deletes the data and the sandbox cannot resume. Automatic
snapshots are kept the same 14 days; a named snapshot never expires and the first
10 are free, then USD 1.70 a month each.

The USD 20 plan is credit rather than a fee, so a light month still bills USD 20.
That makes boat the row where 24/7 is cheaper than 10 hours a day.

Evidence: `docs.boat.dev/pricing` and `docs.boat.dev/hosting` (read 2026-10-22).
Verdict: the best network of any cheap sandbox and a 14-day clock on the state.

## Cloudflare Containers

There is no free plan. Usage is included with the USD 5 a month Workers Paid plan:
25 GiB-hours of memory, 375 vCPU-minutes and 200 GB-hours of disk a month
(`documented`, `developers.cloudflare.com/containers/platform/pricing/`, read
2026-10-22). Instance types run from `lite` at 1/16 vCPU and 256 MiB to
`standard-4` at 4 vCPU, 12 GiB and 20 GB.

Egress is the reason to be here: USD 0.025 per GB in North America and Europe with
1 TB included. 25 GiB-hours of memory on a 4 GiB provisioned container is 6.25
hours a month.

Evidence: `developers.cloudflare.com/containers/platform/pricing/` (read
2026-10-22). Verdict: a paid product whose included egress is worth more than its
included compute.

## What did not work

- **Run Cloud**: withdrawn. `docs.run.cloud/sandboxes/index.md` (read 2026-10-22)
  states the capability is being retired and is no longer available to new
  organizations. It was the cheapest row at USD 0.00.
- **Fly.io**: no free tier. `fly.io/docs/about/pricing/` (read 2026-10-22) states
  new organizations get no monthly free usage allowance; the trial is 2 hours of
  runtime or 7 days.
- **Play with Docker**: unavailable from 2026-03-01.
- **Hugging Face Spaces CPU Basic**: create-time plan gate. The hardware lists as
  FREE and a free account cannot create a Space that uses it.
- **GitHub Actions as a sandbox**: a 6-hour job cap and a runner destroyed at the
  end. Real compute, no continuity, and the `ci-cd-runners` topic's.
- **Killercoda**: one hour per scenario, then deleted. A learning lab.
- **pythonanywhere**: `max_always_on_tasks = 0` on free. The feature is absent, not
  limited.
- **Replit free**: a 30-day preview link, not hosting.
- **Neon free**: 100 CU-hours a month against a database that burns 730 hours if
  kept awake.
- **Browser Linux emulators** (self-hosted): the cycles are the reader's own laptop.

## Chaining

The one useful chain in this class is E2B's pause plus an object store. Run the
work inside a one-hour session, pause it, write its output to storage, and resume
later. The pause is what converts a session cap into a schedule, and the object
store is what makes the sandbox disposable. Every other combination here adds a
second clock without removing the first.
