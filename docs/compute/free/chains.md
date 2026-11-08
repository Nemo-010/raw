# Chaining: what twelve free compositions buy, and which clock ends each

This document answers one question: when a reader joins two or more free compute resources, what
does the join give that no member gives alone, and what ends it first? The answer is twelve chains:
eight `documented`, four `inferred`, none run end to end. The joined pool is 58,172 vCPU-hours a
month on six registrations, and 57,600 of those hours are one member.

## The argument: no single free tier reaches the workload

The workload is 500 GB to 1 TiB served a day, 10 TiB held hot, 20 TiB archived, and jobs that
outlive a session. No record in this topic meets it alone: the free machine is one 2 OCPU box with
10 TB a month (`oracle-cloud`), the free CPU pool is a CI runner that dies at 6 hours
(`github-actions`), the free request runtime is 1,000 seconds of CPU a day (`cloudflare-workers`),
and the free database is 1 GB per project (`neon`). Each is large for its class and none is enough.

A composition is not a larger free tier. It is an arrangement in which one member's weakness is
another member's strength. The four jobs:

- **Hold the address.** A tunnel hostname is DNS, not an IP, so it survives the death of every machine
  behind it. The machine is the replaceable part.
- **Hold the state.** A cursor in a database turns a reaped session from a data loss into a restart,
  and it is the one job the free lane does well.
- **Supply the burst.** Twenty concurrent 4 vCPU runners is 80 vCPU at one instant, more than every
  always-on free machine in the corpus added together.
- **Supply the clock.** The member no meter charges for is the one that can wake the others. A
  scheduler with no minute meter is a free alarm clock.

What the composition buys is one property the parts do not have: **continuity past the end of a
process.** The parts each end, at 6 hours, at 60 minutes, at 15 minutes idle, or at the reclaim
window. What it costs is registrations, and one payment in two of the twelve. What it risks is that
each member fails on its own clock, at a time nobody watches.

The compute front page lists Oracle first among the free machines. At a monthly horizon the largest
member of the pool is the CI runner by a factor of 38: 57,600 vCPU-hours against 1,500 OCPU-hours.
The ratio is an upper bound on the runner's lead, because it counts an OCPU as one vCPU and an OCPU
is one physical core.

## Every chain in one table

Sorted by what the composition yields, largest first, then by registration count.

| # | chain | composes | what the composition yields | registrations | fails first on |
| --- | --- | --- | --- | --- | --- |
| 6 | the composed pool | GitHub, Oracle, Cloudflare, Kaggle, Modal, Freestyle | 58,172 vCPU-hours, 181 GPU-hours, 2.25 OCPU always on | 6 | the 60-day workflow disable |
| 4 | CI as the keepalive | `github-actions`, `oracle-cloud` | an always-on VM that passes a percentile test | 2 | the 60-day workflow disable |
| 2 | the Oracle tenancy | the Oracle services on one signup | 385 GB of storage, two databases, a load balancer | 1 | the 7-day p95 reclaim |
| 9 | origin plus edge | `oracle-cloud`, Cloudflare CDN | a 500 GB a day path at a 33 per cent hit ratio | 2 | 10 TB on the uncacheable bytes |
| 11 | the five-component stack | Oracle, Cloudflare, `neon`, `github-actions`, a domain | the serving path for USD 9.08 in year one | 5 | the domain, then the reclaim |
| 3 | burst plus tunnel | `github-actions`, a Cloudflare named tunnel | a public HTTPS server for 6 hours, 4 times a day | 3 | the 6-hour job cap |
| 7 | CI as a browser | `github-actions`, a Chromium image | 120 browser-hours at one instant | 1 | a 403 from a filtered target |
| 5 | the Cloudflare stack | Workers, Pages, R2, D1, Durable Objects, Tunnel | 1,000 seconds of CPU a day, no byte meter | 1 | the 10 ms CPU wall |
| 10 | sandbox plus state | `e2b`, `vercel-sandbox` or `daytona`, plus `neon` | a resumable worker with no limit on the work | 2 | the session cap |
| 1 | two GPU grants | `nosana`, `lium` | 917 GPU-hours on an RTX 3060 class card | 2 | the 14-day grant expiry |
| 12 | a GPU in the scheduler | Machine.dev, `github-actions` | 63 T4G GPU-hours inside a 6-hour job | 2 | depletion of a one-time credit |
| 8 | the dev machine | `github-codespaces` | 60 wall-clock hours at 2 cores, 32 GB of disk | 1 | the 120 core-hour pool |

## The chains

### 1. A USD 50 grant into a USD 5 grant: GPU-hours from two email addresses

**Composes.** The `nosana` grant of USD 50 on email signup and the `lium` grant of USD 5 on
confirmed email, spent at USD 0.06 per GPU-hour for an RTX 3060. **The arithmetic.** 50 + 5 = USD
55, and 55 / 0.06 = 916.7 GPU-hours. At the USD 0.048 an hour Nosana advertises, the USD 50 alone is
1,041.7 hours. A "roughly 55 GPU-hours" figure for this pair is wrong: 55 / 0.06 is 917, so it is off
by a factor of 16.7.

**Two clocks.** A is the 14-day expiry on the Lium grant. B is the Nosana eligibility list, with no
stated date and no stated size. One is a deadline and the other is a queue. **Breaks first** on A,
then on supply: 43 of 47 models showed no rentable pod, so USD 0.06 is a reference price rather than
a card a reader can rent tonight.

### 2. One tenancy as a whole stack

**Composes.** An Always Free tenancy carries, on one signup: a 2 OCPU / 12 GB A1.Flex instance, two
E2.1.Micro, 200 GB of block volume, 20 GB of object storage, two Autonomous AI Databases, NoSQL,
MySQL HeatWave, two load balancers, a CA and certificate pair, a vault and a mail sender. **The
arithmetic.** 2 OCPU for 730 hours is 1,460 of the 1,500 OCPU-hours, and 12 GB for 730 hours is
8,760 of 9,000 GB-hours, leaving 40 OCPU-hours. Storage sums to 385 GB: 200 block, 20 object, 2 x 20
Autonomous, 3 x 25 NoSQL, 50 MySQL. The load balancer is the smallest part: 10 Mbps is 1.25 MB/s, or
108 GB a day, so the 10 TB allowance is not the wall on that path. The 10 Mbps is.

**Two clocks.** A is the 7-day 95th-percentile window; B is the monthly reset of the 1,500
OCPU-hours. A machine passes B every month and can still be taken by A, because one is a total and
the other a percentile. **Breaks first** on A, before any quota.

### 3. A CI runner plus a named tunnel: a public server for six hours

**Composes.** A standard GitHub-hosted runner on a public repository, at 4 vCPU, 16 GB and 14 GB of
SSD, with a Cloudflare named tunnel giving it a public HTTPS hostname. **The arithmetic.** One job
is 4 vCPU for 6 hours, so 20 concurrent jobs is 120 runner-hours and 480 vCPU-hours at one instant,
and 14,400 runner-hours a month if jobs are chained back to back. The tunnel is what turns a machine
with no inbound connection into an addressable server.

**Two clocks.** A is the 6-hour job, which terminates and fails at the limit. B is the 60-day rule
that disables a scheduled workflow in a public repository after that long without activity. A ends
every instance; B ends the schedule that produces them. **Breaks first** on A, on every instance, so
the chain buys a 6-hour public server and never a service.

### 4. The scheduler that holds the always-on machine

**Composes.** `github-actions` as the keeper and `oracle-cloud` as the kept. **The arithmetic.** The
reclaim rule is a percentile, not a total. Seven days is 168 hours, and a 95th percentile at or
above 20 per cent needs at least 5 per cent of the window at or above 20 per cent, which is 8.4
hours a week. That is 0.4 OCPU for 36.4 hours a month, or 14.6 OCPU-hours, and the leftover
allowance after a 24/7 box is 40. The keepalive fits inside what the box does not already spend
(`inferred`: arithmetic on the rule, not an observation).

**Two clocks.** A is Oracle's 7 days; B is GitHub's 60 days. Neither sends a bill. **Breaks first**
on B, which is the counter-intuitive order: the keepalive suppresses A while it runs, so the part
that stops is the keeper. ⚠ The `github-actions` record does not state whether a scheduled run
counts as repository activity for the 60-day rule.

### 5. One Cloudflare account as six services

**Composes.** `cloudflare-workers`, Pages, R2, D1, `cloudflare-durable-objects` and a Tunnel on one
free account. **The arithmetic.** 100,000 requests a day at 10 ms each is 1,000 seconds of CPU a
day, or 1.2 per cent of a day; the request count is the visible number and it is not the meter.
Durable Objects at 13,000 GB-seconds a day is 0.15 GB held all day, because 13,000 / 86,400 = 0.15.
D1 is 5 million rows read a day and 5 GB in total, and R2 is 10 GB-month with egress free. None of
the six charges per byte out.

**Two clocks.** A is the 10 ms CPU wall, tested per request and answered immediately. B is the daily
reset of the 100,000 requests. A request that trips A leaves B untouched, so the daily counter looks
healthy on a day that failed. **Breaks first** on A, and the record notes that a JSON parse meets 10
ms on the first request.

### 6. The composed pool

**Composes.** Six accounts: `github-actions`, `oracle-cloud`, `cloudflare-workers`,
`kaggle-notebooks`, `modal` and `freestyle`. **The arithmetic.** 57,600 + 252 + 200 + 120 = 58,172
vCPU-hours a month, and GitHub is 57,600 / 58,172 = 0.990 of it.

**Two clocks.** A is daily, because Cloudflare's request count resets every day. B is monthly,
because Oracle, Freestyle, Codespaces and Modal reset on the billing period. A third rule, GitHub's
60-day disable, is not a period at all and fires on an event. **Breaks first** on that third rule,
for a reason that is not capacity: the 57,600 vCPU-hours need a public repository that stays active.

### 7. A CI runner as a browser

**Composes.** `github-actions` and a Chromium image; Playwright publishes a CI guide that treats a
CI agent as a supported browser platform. **The arithmetic.** 20 jobs of 6 hours is 120
browser-hours at one instant, against the largest recurring free browser-hour allowance in the
corpus, `ferr` at 50 a month. One instant of a runner is 2.4 times that whole month.

**Two clocks.** A is the 6-hour job, which is the length of a browser session. B is the 60-day
schedule rule, so a campaign is a series of A intervals inside one B window. **Breaks first** on
neither: the address breaks it. A runner presents a datacenter IP, and a target that filters
datacenter traffic answers 403 before the browser starts. The allowance is large and the reachable
fraction is unknown.

### 8. The dev machine behind the same account

**Composes.** `github-codespaces` for the shell and the 32 GB disk, with the Oracle volume as the
durable origin. **The arithmetic.** 120 core-hours a month, spent one unit per core per hour, is 60
wall-clock hours on the default 2-core machine and 30 on a 4-core machine. The 15 GB-month of
storage accrues whether or not a codespace runs.

**Two clocks.** A is the monthly core-hour pool, which stops compute. B is the monthly GB-month
storage pool, which accrues while nothing runs, so a month of no work spends part of B and none of
A. **Breaks first** on A, at 60 wall-clock hours, and at exhaustion the account is blocked unless a
payment method is on file.

### 9. Origin plus edge: the only serving path that closes

**Composes.** Oracle's 10 TB a month of outbound transfer and Cloudflare's free CDN, which states no
cap on bytes or requests. **The arithmetic.** 500 GB a day is 15,000 GB a month against a 10,000 GB
origin, so the break-even hit ratio is 1 - 10,000 / 15,000 = 33 per cent. At 1 TiB a day the decimal
figure is 32,985 GB and the break-even is 70 per cent, not 67: 30,720 is GiB and
not GB, which also makes 6,144 a GiB figure rather than the 6,597 GB the subtraction gives.

**Two clocks.** A is the monthly 10 TB reset. B is Oracle's 7-day reclaim, dormant while the origin
serves, because serving raises utilisation. **Breaks first** on A, and on the uncacheable fraction
rather than on total traffic: Cloudflare caches by file extension and does not cache HTML or JSON by
default, so an HTML or API site never reaches 33 per cent.

### 10. A sandbox plus a database: the reap becomes a restart

**Composes.** A session-capped sandbox and `neon`. The caps are 60 minutes on `e2b`, 45 minutes on
`vercel-sandbox`, 15 minutes idle on `daytona` and 5 minutes by default on `modal`. **The
arithmetic.** Neon's Free plan is permanent and needs no card: 100 CU-hours a month per project, 1
GB of Postgres per project, 20 GB across the account, 5 GB of object storage and 5 GB of egress. The
5 GB is 167 MB a day, so a sandbox that moves more than that exceeds it; the same 5 GB is 0.05 per
cent of Oracle's 10 TB.

**Two clocks.** A is the session, measured in minutes and enforced by the vendor. B is the month,
measured in CU-hours and egress and enforced by suspension. A destroys the machine; B stops the
database and deletes nothing, which the page states as "none of these limits delete your data".
**Breaks first** on A, and it is the only chain of the twelve whose first failure costs no work.

### 11. The whole stack, with its one paid component

**Composes.** Oracle as the always-on origin, the Cloudflare CDN as the edge, `neon` as the state,
`github-actions` as the burst lane and the scheduler, and one registered domain. **The arithmetic.**
`spaceship` lists .com at USD 8.88 for the first year and USD 9.98 to renew, and the same page
states a USD 0.20 ICANN fee, so year one is USD 9.08 at most. A "USD 8.88 a year" figure omits
that fee. `cloudflare-registrar` is USD 10.46 flat.

**Two clocks.** A is the 12-month renewal, the only clock in the twelve chains that arrives as a
payment. B is Oracle's 7-day reclaim. **Breaks first** on the domain in construction, because a
named tunnel's hostname must come from a zone Cloudflare holds, and on B in operation. ⚠ A quick
tunnel needs no zone, and the corpus does not establish whether a job can use one: its hostname
changes on every run.

### 12. A GPU inside the scheduler

**Composes.** Machine.dev, which attaches to a workflow by runner label, and `github-actions` as the
scheduler; changing `runs-on: ubuntu-latest` to `runs-on: machine/gpu=T4` is the whole integration.
**The arithmetic.** USD 10 at USD 0.00261 a minute is 3,831 minutes, or 63.9 hours of T4G, and 2,688
minutes or 44.8 hours at the USD 0.00372 the signup page also prints. 63 GPU-hours is 10 six-hour
jobs and half of an eleventh.

**Two clocks.** A is the credit, one-time and not renewed. B is the 6-hour job cap, which decides
how the credit is spent rather than whether it runs out. **Breaks first** on A, the only first
failure in the class that is arithmetic and dated. There is no record for this provider under
`dossier/compute/`; the claim rests on the vendor's pages cited in the finding, read 2026-10-22.

## The composed pool

One table, units kept apart, then the addition. The last column is the conversion.

| member | allowance as published | vendor unit | contribution to the pool |
| --- | --- | --- | --- |
| `github-actions` | 20 concurrent jobs x 6 hours at 4 vCPU, 16 GB, 14 GB SSD, no minute charge on a public repository | runner-hours | 14,400 runner-hours = 57,600 vCPU-hours a month |
| `modal` | USD 30 of compute a month, recurring | USD credit | about 126 sandbox hours at 2 vCPU / 4 GiB = 252 vCPU-hours |
| `freestyle` | 200 vCPU-hours, 400 GiB-hours, 60,000 GiB-hours of storage, 50 GB of transfer | vCPU-hours | 200 vCPU-hours |
| `github-codespaces` | 120 core-hours and 15 GB-month | core-hours | 120 vCPU-hours, or 60 wall-clock hours at 2 cores |
| `oracle-cloud` | 1,500 OCPU-hours and 9,000 GB-hours on A1.Flex | OCPU-hours | 1,500 OCPU-hours, a physical core, not added to the sum |
| `kaggle-notebooks` | 30 P100 GPU-hours a week, no monthly figure published | GPU-hours | 130 P100 GPU-hours a month |
| `cloudflare-workers` | 100,000 requests a day at 10 ms of CPU | requests | 1,000 seconds of CPU a day, or no vCPU-hours at all |

**vCPU-hours a month.** 57,600 + 252 + 200 + 120 = 58,172. GitHub is 99.0 per cent of it, and the
other three members are 572 vCPU-hours, or 1.0 per cent. The 57,600 assumes 20 jobs saturated for 24
hours a day across 30 days: 20 x 6 = 120 runner-hours at once, 120 x 4 cycles a day = 480 a day, 480
x 30 = 14,400 runner-hours, 14,400 x 4 vCPU = 57,600. No run in the corpus has sustained that.

**OCPU-hours are excluded.** An OCPU is one physical core and a vCPU is a share of one, and the
corpus holds no ratio, so 1,500 OCPU-hours stay in their own row. Dividing 57,600 by 1,500 gives
38.4, a number that credits Oracle with less than it owns.

**GPU-hours a month.** 130 P100 + 51 T4 = 181 GPU-hours, and the two classes are not
interchangeable. The 130 is 30 x 52 / 12 = 130.0, the weekly allowance averaged across a year. The
51 is a conversion of USD 30 at a T4 rate the `modal` record does not carry, one rung
weaker than the record beside it. Two one-off grants sit outside the monthly figure: 917 RTX
3060-hours from chain 1 and 63 T4G-hours from chain 12.

**Always-on capacity.** One A1.Flex at 2 OCPU and 12 GB continuously, which is 1,460 of the 1,500
OCPU-hours and 8,760 of the 9,000 GB-hours for a 730-hour month, plus two E2.1.Micro at 0.125 OCPU
and 1 GB each. The total is 2.25 OCPU, 14 GB, 200 GB of block volume, 10 TB of egress and three
machines, and one card and phone at signup buys it. The Cloudflare edge is always on too and holds
no disk.

**Persistent state.** Oracle carries 385 GB across five services, `neon` adds 20 GB of Postgres per
account and 5 GB of object storage per project, and Cloudflare adds 5 GB of D1 and 10 GB-month of
R2. With one Neon project the stated store is 425 GB. No component publishes a single-volume figure
above 200 GB, and the archive target is 20 TiB.

**Egress a month, from the three members that publish one.** Oracle 10 TB is 10,000 GB, Modal 1 TiB
is 1,099.5 GB, Freestyle 50 GB, and the sum is 11,149.5 GB, or 11.1 TB. Kaggle does not publish an
allowance, and Cloudflare charges nothing per byte out, so it adds no number and removes the meter
instead.

## What breaks first, across all twelve

Five failure modes recur. The count is the number of the twelve chains in which the record names
that mechanism, either as one of the two clocks or as the first failure.

| failure mode | chains | what it actually is |
| --- | --- | --- |
| a percentile reclaim (`oracle-cloud`) | 4 | a 7-day window, three conditions under 20 per cent, no invoice |
| the 6-hour job cap (`github-actions`) | 4 | a hard terminate and fail at the limit, on every instance |
| the 60-day workflow disable (`github-actions`) | 3 | an event, not a period, and it kills the scheduler rather than the job |
| a one-time grant reaching zero | 2 | dated and arithmetic, and the only mode with a forecast |
| the 10 ms CPU wall (`cloudflare-workers`) | 1 | per request, immediate, and invisible to the daily counter |

Two more appear once each: a session cap in chain 10 and a datacenter address refused with a 403 in
chain 7. The identity gates are separate, a card and a phone for Oracle and Codespaces and a domain
for chains 3 and 11, and a gate is admission rather than a clock.

- **The Oracle reclaim appears, in 4 of 12.** It is the only mechanism a workload can pass while
  appearing idle.
- **The GitHub job cap appears, in 4 of 12.** It is the most certain, because any job on a hosted
  runner dies at 6 hours, whatever else the chain waits on.
- **The Cloudflare CPU wall appears, in 1 of 12.** A real wall and a narrow one: chain 5 is the only
  chain that uses Workers for compute rather than delivery.
- **The sandbox session caps appear, in 1 of 12.** Chain 10 is the only chain that uses them, and the
  only one that survives its own first failure.

The recurring property is not the mechanism. It is that **every chain has at least two clocks that
run on different periods, and only one is visible in a console.** A daily request counter hides a
per-request wall. A monthly OCPU total hides a 7-day percentile. A 6-hour job hides a 60-day
schedule. A reader who watches the printed number is watching the clock that will not fire.

## What the corpus does not know

None of the twelve chains has been run end to end. The dossier holds no record of an operated
composition: eight findings carry `documented`, four `inferred`, none `measured`.
`docs/compute/measurement.md` states the standing position, that no record in this topic is
`measured` and that the probes which exist measure reachability rather than a quota. That gap
decides what the rest of this page means.

- The 57,600 vCPU-hours are a ceiling computed from a concurrency limit, not a throughput anyone
  sustained.
- The 917 GPU-hours in chain 1 are a price, not capacity: 43 of 47 models showed no rentable pod at
  read time.
- The keepalive arithmetic in chain 4 comes from the wording of a rule. Whether a 0.4 OCPU process
  passes a 95th-percentile test is a question a probe answers in eight days and no document answers
  at all.
- Whether a 6-hour job can hold a named tunnel for its whole length is unmeasured. The two facts are
  each documented and the join is not.
- Whether a scheduled run counts as repository activity for the 60-day rule is not stated on the page
  the record cites, and chains 3, 4 and 6 rest on it.
- The CDN break-even in chain 9 assumes Cloudflare caches the bytes, and no cache hit ratio was
  measured for any site.

## What would change the answer

1. **A probe that holds an A1 instance at or above 20 per cent of 2 OCPU for 36 hours in seven days,
   and reads the instance state on day 8.** It settles chain 4 and whether the leftover 40
   OCPU-hours are enough.
2. **One workflow file that runs for 61 days on a public repository.** It settles the 60-day rule, and
   with it chains 3, 4 and 6.
3. **One measured cache hit ratio against an HTML site behind the free CDN.** It settles chain 9, and
   it is the difference between 33 per cent and impossible.
4. **A timestamped pod listing on the GPU marketplace.** It turns 917 GPU-hours from a price into
   capacity, or confirms the cheap card is a reference price.

Until one of those exists, this document is a map of what the free lane would give. It is drawn from
records that describe the parts, and never from a run that joined them.
