# Sandbox newcomers: what the new providers charge, and the aggregator tiers that are not there

Two questions about one slice, kept apart because they fail differently. The first is what the
newer sandbox and agent-VM providers sell, per hour, at a
named shape. The second is what the free-tier aggregators say about the same names. The 33
records behind this page answer both, and every page was read on 2026-10-22.

The value of the slice is one number. `boxlite-cloud` gives USD 100 at signup with no card, and
its meter is USD 0.0504 per vCPU-hour, so 100 / 0.0504 = **1,984.1 vCPU-hours**. At its Medium
size of 2 vCPU / 4 GiB, 100 / 0.1620 = **617.3 hours**, or 617.3 / 24 = 25.7 days. No record
here prices a GPU, so there is no GPU-hour conversion to state; "What the class does not give"
carries that absence.

## The short answer

| the decision | the answer | the arithmetic | what it costs |
| --- | --- | --- | --- |
| largest card-free credit | `boxlite-cloud`, USD 100 | 100 / 0.0504 = 1,984.1 vCPU-hours; 100 / 0.0666 = 1,501.5 Small-box hours; 100 / 0.1620 = 617.3 Medium hours | a one-time grant, and a stopped box bills disk until it is deleted |
| cheapest always-on 2 vCPU / 4 GiB in USD | `remotehost` Starter, USD 20 a month | 730 x 0.5 = 365 of the 610 included machine-hours; 20 / 730 = USD 0.0274 an hour | a card at checkout, and a 24-hour session cap |
| cheapest always-on 2 vCPU / 4 GiB in EUR | `inis-run` medium, EUR 0.036 an hour | 0.036 x 730 = EUR 26.28 for 730 hours | the EUR 1.00 credit covers 1 / 0.036 = 27.8 hours, not a month |
| cheapest box that stays up at 0.5 GiB resident | `ix` | 0.5 x 0.0108 x 720 = USD 3.89 for 30 days | a card, and no grace period when the balance runs out |

**The two USD rows compare and the EUR row does not.** No exchange rate was read, so
`inis-run`'s EUR 26.28 stays out of the ranking. At 4 GiB resident `ix` costs 4 x 0.0108 x 720 =
USD 31.10 for 30 days, above `remotehost`'s USD 20; the two meet at 20 / 720 / 0.0108 = 2.57 GiB.

**The two cheapest shapes are cheap for opposite reasons.** `remotehost` sells a whole month at a
fixed price and lets a 2 vCPU / 4 GiB box run 730 hours inside a 610 machine-hour allowance,
because that size counts 0.5 machine-hours per hour. `ix` has no allowance and charges memory
held plus CPU consumed, so its figure collapses when the box idles and rises to 107.14 for a busy
2 vCPU / 8 GiB machine.

**Four records give credit with no card.** `boxlite-cloud` USD 100, `bunny-sandbox` USD 20,
`everstack` USD 5 and `inis-run` EUR 1.00: 100 + 20 + 5 = USD 125 across three accounts, and none
of it renews. The only credit that renews without a card is `the-vibe-hosting`'s USD 0.90 a
month. ⚠ Spending "USD 125 free" takes three registrations and leaves nothing in month two.

### What the 33 records are

Two counts decide who can use the slice, and both sum to 33.

| verdict | records | identity cost | records |
| --- | --- | --- | --- |
| qualifies-with-caveat | 14 | email | 23 |
| trial-only | 11 | card | 8 |
| paid-only | 6 | national-id | 1 |
| fails-identity | 1 | anonymous | 1 |
| dead | 1 | - | - |

So 24 of the 33 need no card and one needs no account at all. The 8 card-gated rows are the ones
with a per-second meter or a prepaid balance, and 6 of the 8 are sandboxes rather than hosts.

## Half one: the new sandbox and VM providers

Fifteen records rent a machine or a sandbox. Ten publish a meter and are priced below at a named
shape, one publishes no rate at all, and four carry a flat price. ⛔ A rate with no shape is not a
rate, so every cell in the second column names the vCPU and memory the rate buys.

| provider | per hour at a named shape | sleeps or stays up | free lane | identity | what kills a running job |
| --- | --- | --- | --- | --- | --- |
| `inis-run` | EUR 0.036 at 2 vCPU / 4 GB, millisecond meter | stays up to a 24-hour backstop; a paused session keeps storage | EUR 1.00, no card, credit does not expire | email | the 24-hour continuous-live backstop, 6 hours on an unverified trial; a self-pause cannot resume (410) |
| `vers` | USD 0.0800 at 2 vCPU / 4 GiB, memory included | paused, stopped and branched VMs accrue nothing | credits at signup, amount not published | email | the monthly card charge for what ran; no session cap is published |
| `bunny-sandbox` | USD 0.0600 at 2 core / 4 GB, plus USD 1.00 a month workspace and USD 2.00 a month IPv4 | stays up until deleted | USD 20 trial, no card, 14 days | email | the 14-day clock or the USD 20 balance; an orphan keeps billing |
| `qiniu-cloud-ai` | CNY 0.3240 at 2 vCPU / 2 GiB | stays up for a 5-minute default lifetime | no compute allowance; 20 GiB local disk, 10 GiB persistent storage a month | national-id | the 5-minute default lifetime and a 15-second default exec |
| `boxlite-cloud` | USD 0.1620 at 2 vCPU / 4 GiB / 20 GiB | stays up; compute stops at the stop request, disk bills until delete | USD 100, no card, expiry not stated | email | the disk meter after a stop; the credit does not renew |
| `ix` | USD 0.1008 at 2 vCPU / 4 GiB of consumed CPU and memory in use | stays up; a stopped machine pays only its disk | none: "There is no free credit on signup" | card | the balance, with no grace period; disks are deleted 24 hours later |
| `sailboxes` | USD 0.1430 at the smallest Sailbox, 1 vCPU / 16 GiB | sleeping, paused and checkpointing time is not billed | USD 5 a month once a card is attached | card | the 16 GiB RAM floor bills whether it is touched; a spent credit pauses every box |
| `everstack` | USD 0.1332 at 2 vCPU / 2 GiB; 4 GiB needs 4 vCPU / 4 GiB at USD 0.2664 | not stated | USD 5 one-time, no payment method | email | 1 GiB of RAM per vCPU forces a shape change; one credit per organization |
| `digitalocean-harness-runtime` | USD 0.1260 at 2 vCPU / 4 GB full allocation; USD 0.0600 at 25 per cent of both vCPUs | pause, resume and fork; checkpoints bill while paused | USD 5 one-time, on top of a prepaid balance | card | the prepaid balance; checkpoints accrue storage at a zero balance |
| `remotehost` | USD 0.0274 at 2 vCPU / 4 GB over 730 hours | stays up, in 24-hour sessions | 7-day trial | card | the 24-hour session cap and the 610 machine-hour allowance |
| `byteplus-ai-cloud` | not published; a third party states USD 0.0351 per vCPU-hour and USD 0.0081 per GiB-hour | bills only while executing | none published | not established | the write gate: the rate card and the signup route both sit behind an account |
| `containarium` | USD 20 a seat a month, no meter: 20 / 730 = USD 0.0274 an hour at 2 vCPU (1 guaranteed) / 4 GiB / 20 GB | sleeps when idle | none found; the console is a login wall | card | 100 GB of egress a month; the second vCPU is best effort; an idle box sleeps |
| `sandock` | no rate: USD 5 a month for 5 sandboxes, up to 4 vCPU | stays up to the session timeout | none: "Sandock is a paid product" | card | a 4-hour session timeout on Plus and 8 hours on Pro |
| `the-vibe-hosting` | RAM only, USD 0.005 per GB-hour awake, CPU free, so no per-vCPU rate exists | stays up 24/7 | USD 0.90 a month anonymous, USD 2.25 with a phone | anonymous | the monthly credit at USD 0.25 per GB-month of disk: 3.6 x 0.25 = 0.90 spends it |
| `euserv` | no rate: free | stays up | a permanent 1 core at 1 GHz / 1 GiB / 10 GB, 1 TB a month | email | the port drops to 1 Mbit/s after 1 TB, and there is no IPv4, only one /128 |

The last four rows carry a flat price or nothing in place of a rate. `remotehost` and `sandock`
decide a long job, and both fail on a clock: `remotehost` recreates the session every 24 hours on
Starter and every 72 on Max, and `sandock` caps one at 4 hours on USD 5 and 8 on Pro.

## The unit problem

Seven denominations appear in this slice and they are not interchangeable. The table names the
meter, the providers that use it, and what the meter actually charges for.

| denomination | how the vendor writes it | providers and stated rate | what it charges for |
| --- | --- | --- | --- |
| vCPU-hour, allocated | USD per vCPU-hour | `vers` 0.04, `boxlite-cloud` 0.0504, `everstack` 0.0666 effective | the vCPU whether or not it executes |
| vCPU-hour, consumed | USD per vCPU-hour of CPU time used | `ix` 0.0288, `digitalocean-harness-runtime` 0.044, `sailboxes` 0.015 | only the cycles that run |
| vCPU-second | CNY per vCPU per second | `qiniu-cloud-ai` 0.00003, `cohesivity` 100,000 a month | the same meter at a finer unit |
| CPU core-hour | USD per core-hour | `bunny-sandbox` 0.02 | a core, which the page does not equate to a vCPU |
| machine-hour | machine-hours per hour | `remotehost` 0.5, 1 or 2 by size; `inis-run` fixed sizes | a named shape for an hour, not its parts |
| GB-hour or GiB-hour of memory | USD per unit-hour | `bunny-sandbox` 0.005 per GB, `digitalocean-harness-runtime` 0.0095 per GB, `sailboxes` 0.008 per GiB, `ix` 0.0108 per GiB, `boxlite-cloud` 0.0144 per GiB | memory held or memory in use, depending on the row |
| GiB-hour or GiB-month of disk | USD per unit | `boxlite-cloud` 0.00018 an hour, `ix` 0.101 a month, `sailboxes` 0.0007 an hour of NVMe | the bytes that survive the session |

### One box, three meters

A 2 vCPU / 4 GiB box for one hour, priced three ways from the records that publish enough to
reproduce:

- `vers`: 2 x USD 0.04 = **USD 0.0800**. Memory is included, so the second dimension is zero.
- `boxlite-cloud`: 2 x 0.0504 + 4 x 0.0144 + 20 x 0.00018 = 0.1008 + 0.0576 + 0.0036 =
  **USD 0.1620**, with 20 GiB of disk.
- `ix`: 2 x 0.0288 + 4 x 0.0108 = 0.0576 + 0.0432 = **USD 0.1008**, and 20 GiB of disk is
  20 x 0.101 = USD 2.02 a month.

The hourly figures rank `vers` < `ix` < `boxlite-cloud`, and 0.1620 / 0.0800 = 2.025, so the
most expensive is 2.0 times the cheapest at full duty. That ranking holds. What does not hold is
the gap, and the arithmetic that shows it is the idle case, where the box is up for the whole
month and executes at 5 per cent of one vCPU:

| meter | 730 hours at full duty | 730 hours up, 5 per cent CPU | what the difference is |
| --- | --- | --- | --- |
| `vers` | 0.0800 x 730 = USD 58.40 | 0.0800 x 730 = USD 58.40 | an allocated vCPU bills whether it runs |
| `ix` | 0.1008 x 730 = USD 73.58 | (0.05 x 2 x 0.0288 + 4 x 0.0108) x 730 = 0.04608 x 730 = USD 33.64 | the CPU meter falls with use and the memory meter does not |
| `boxlite-cloud` | 0.1620 x 730 = USD 118.26 | 0.1620 x 730 = USD 118.26 | an allocated box bills until it is stopped or deleted |

At full duty `vers` / `ix` is 58.40 / 73.58 = 0.79, so `vers` is cheaper. At 5 per cent duty
58.40 / 33.64 = 1.74, so `ix` is cheaper. `boxlite-cloud` is 118.26 / 33.64 = 3.52 times `ix` in
the idle case and 2.03 times `vers` in the busy one. ⚠ **A per-hour headline is a duty-cycle
assumption wearing a unit.** The same three rates reverse order on load alone.

### Where the units do not convert

**Decimal GB against GiB.** `bunny-sandbox` states USD 0.005 per GB-hour and
`digitalocean-harness-runtime` USD 0.0095, while `ix`, `boxlite-cloud` and `sailboxes` state GiB.
A 4 GiB allocation is 4 x 1.073741824 = 4.294967296 GB, so the bunny line is
4.2950 x 0.005 = USD 0.0215 and not 4 x 0.005 = USD 0.0200, a ratio of 0.0215 / 0.0200 = 1.074.
On DigitalOcean's Medium the correction moves 0.1260 to 2 x 0.044 + 4.2950 x 0.0095 = USD 0.1288,
2.2 per cent, because memory is 30 per cent of that shape.

**Core-hour against vCPU-hour.** `bunny-sandbox` prices a core and caps at 8. The page does not
say how many vCPUs a core is, so its USD 0.0600 at 2 core / 4 GB cannot be ranked against a vCPU
meter without an assumption this corpus will not make.

**vCPU-second against vCPU-hour.** `qiniu-cloud-ai` publishes CNY 0.00003 per vCPU per second,
and 0.00003 x 3,600 = CNY 0.108 a vCPU-hour, so a 2 vCPU / 2 GiB box is
2 x 0.108 + 2 x 0.054 = CNY 0.3240 an hour. `cohesivity` publishes the same unit as a monthly
bucket: 100,000 / 3,600 = 27.78 vCPU-hours, which at its 0.5 vCPU cap is 27.78 / 0.5 = 55.6
hours, against 400,000 / 3,600 = 111.1 hours at 1 GB. The CPU bucket empties first.

**A subscription with a ceiling has no rate.** `sandock` sells 5 sandboxes for USD 5 a month with
"up to 4 vCPU": 5 / 5 = USD 1.00 a sandbox, and no vCPU-hour rate exists, because a ceiling is
not an allocation. ⛔ **Do not divide a ceiling by a month.** `containarium`'s 2 vCPU with 1
guaranteed is the same trap.

**Two shapes that cannot be bought.** `everstack` sells 1 GiB per vCPU, so 2 vCPU / 4 GiB does
not exist and the nearest is 4 vCPU / 4 GiB at USD 0.2664. `sailboxes` starts at 16 GiB, so its
floor is 1 vCPU / 16 GiB at 0.015 + 16 x 0.008 = USD 0.1430. A table that lists both at
"2 vCPU / 4 GiB" has invented two products.

**Two month lengths.** `ix` reproduces its own 30-day figure at 720 hours: 0.144 x 720 = 103.68,
plus 20 x 0.101 = 2.02, gives the page's USD 105.70. At 730 hours the same machine is 107.14. The
gap is 730 / 720 = 1.014, larger than several differences a reader is trying to measure, so every
figure here names its month.

### Three places where the published arithmetic does not close

- `boxlite-cloud`'s meters reproduce all three named sizes exactly: 0.0504 + 0.0144 + 0.0018 =
  0.0666 for Small, 0.1008 + 0.0576 + 0.0036 = 0.1620 for Medium, and 0.2016 + 0.1152 + 0.0090 =
  0.3258 for Large. It is the only record here that passes that check on every size.
- `qiniu-cloud-ai`'s worked example is CNY 2.61 for 2 vCPU / 2 GiB over 8 hours, and its meters
  give 0.324 x 8 = CNY 2.592, so 2.61 / 2.592 = 1.007. The 0.7 per cent is rounding or a term the
  page does not name, and the record cannot tell which.
- `digitalocean-harness-runtime`'s record says a Medium sandbox "25 percent busy costs about
  USD 0.011 per hour in CPU". 0.044 x 0.25 = 0.011 is one vCPU at 25 per cent; if the whole
  2 vCPU machine is 25 per cent busy, the bill is 0.5 x 0.044 = USD 0.022 and the total is
  0.022 + 0.038 = USD 0.060, not USD 0.049. The record does not say which reading it used, and
  the two differ by 22 per cent.

## Half two: the aggregator claims, checked

Eighteen of the 33 records are platform hosts rather than sandboxes. They are in this half
because that is where the aggregator claims point: free-for.dev and dalisoft/awesome-hosting both
list small app hosts as free compute, and a reader who wants a sandbox often lands on one.

| provider | free ceiling | identity | what binds | verdict |
| --- | --- | --- | --- | --- |
| `apexweave` | a 14-day trial plus a 120-day grace period, no capacity figure published | email | the clock, 134 days in total | trial-only |
| `appish` | 1 slot of 4 hours, extendable by hand, shared and unspecified resources | email | the 4-hour expiry | qualifies-with-caveat |
| `apply-build` | 0.5 vCPU and 512 MiB on one account, no card | email | one account-wide half core; no sleep timer published | qualifies-with-caveat |
| `awardspace` | 1 GB disk, 5 GB a month, about 5,000 visits, one MySQL database | email | traffic, not compute; no CPU or RAM figure published | qualifies-with-caveat |
| `cohesivity` | 100,000 vCPU-seconds and 400,000 GB-seconds a month at 0.5 vCPU / 1 GB | email | 55.6 hours of running time a month | qualifies-with-caveat |
| `deplexo` | 1 app at 0.25 CPU, 128 MB RAM, 250 MB disk, 100 GB a month | email | 250 MB of disk and 128 MB of RAM | qualifies-with-caveat |
| `faable` | 0.6 vCPU / 512 MB, 3 projects, 10 GB egress a month at 1 GB a day | email | a 30-minute idle sleep, and a planned 4-hour rest in every 24 | qualifies-with-caveat |
| `gigalixir` | 1 replica at 0.5 GB, a Postgres capped at 10,000 rows and 2 connections | card | the 10,000-row database; sleeps after 30 days without a deploy | qualifies-with-caveat |
| `hostim-dev` | 5-day trial, then EUR 2.50 a month for 1 vCPU / 1 GB | email | nothing at EUR 2.50; billing is hourly with a one-hour minimum | trial-only |
| `mrvm` | none: the plan page returns 404 | email | no plan exists to measure | dead |
| `ownkube` | USD 5 signup credit, one-off | email | the credit is spent at about USD 0.0246 a vCPU-hour, then the account pauses | trial-only |
| `podway` | 1 Mini pod free in early access: 1 vCPU / 1 GB / 6 GB | email | one pod, and only from the vendor's app catalogue | qualifies-with-caveat |
| `qoddi` | 3 static sites; no application compute | card | the USD 6 a month application floor, and a card even for the free static tier | paid-only |
| `runsite` | static sites plus 5 GB of object storage; the 0.1 vCPU web service is EUR 3 a month | email | EUR 3 for the smallest web service | paid-only |
| `shiper` | 1 instance at 0.25 vCPU / 256 MB, no custom domain | email | one instance at a quarter core | qualifies-with-caveat |
| `staxa` | 2 tenants, each one Small tier, no custom domains | email | two tenants; the size comes from an API example payload, not a price table | qualifies-with-caveat |
| `velixir` | 0.25 vCPU / 256 MB / 1 GB, custom domains, no card | email | sleeps when idle; one deployment slot | qualifies-with-caveat |
| `wso2-choreo` | a 2-week trial; the plans are USD 150 per component a month | email | the 14-day clock | trial-only |

### Eighteen claims, checked against the vendor page

Each row is one claim the record went to verify: 13 from free-for.dev and 5 from
dalisoft/awesome-hosting.

| record | what the aggregator says | what the vendor page says | verdict |
| --- | --- | --- | --- |
| `faable` | 0.5 CPU / 1 GB per project, 10 GB bandwidth, 10 deploys a day, sleeps after 2 hours | bi.xs is 0.6 vCPU / 512 MB, the cap is 50 deploys a day, and idle sleep is 30 minutes | refuted on three terms |
| `gigalixir` | one free instance that never sleeps | Free "Sleeps after 30 days"; only Standard never sleeps; a card is required at signup | refuted, and the card is omitted |
| `qoddi` | a free tier for static assets, staging and developer apps | application hosting starts at USD 6 a month; only 3 static sites are free; a card is required even for those | refuted |
| `runsite` | a free web service at 0.1 vCPU / 256 MB | the 0 EUR row is static sites; the 0.1 vCPU web service is EUR 3 a month | refuted |
| `wso2-choreo` | 5 components and USD 100 of credit a month | the page lists Team at USD 150 per component and Enterprise, plus a 2-week trial | tier withdrawn |
| `ownkube` | Starter runs in your own AWS account with no card and no monthly fee | a prepaid wallet, a USD 5 signup credit, and no bring-your-own-account offer | tier withdrawn |
| `mrvm` | LXC-256 at EUR 0.5 a month, the list's cheapest row | the site is a placeholder and the plan URL returns 404 | not orderable |
| `appish` | 1 slot with 2-hour sessions | 1 slot, 4 hours, extendable with one click | refuted in the reader's favour |
| `awardspace` | free hosting plus a free short domain, PHP, MySQL, no ads | PHP, MySQL, one mailbox and no ads hold; the plan gives one domain the reader brings and three subdomains | short domain refuted |
| `apexweave` | plans at USD 5 a month | neither the pricing page nor the free-tier page publishes a plan price | price unsupported |
| `the-vibe-hosting` | a 2-core, 512 MB server 24/7 with a verified phone | no core count is published and CPU is billed as free | figure unsupported |
| `apply-build` | 0.5 vCPU / 512 MiB, European servers, automatic firewall | the same shape, and the free tier survives cancelling paid packages | holds |
| `deplexo` | 1 app at 0.25 vCPU, 128 MB RAM, 250 MB disk, 100 GB | the same on every number | holds |
| `velixir` | 1 app at 0.25 vCPU / 256 MB that sleeps, custom domains, no card | the same | holds |
| `cohesivity` | 10 projects, 100K edge requests, 10 GB of storage, 100 emails, USD 5 a month | the project count matches; the 100,000 vCPU-seconds, 400,000 GB-seconds and 60-deploy cap are omitted | incomplete |
| `hostim-dev` | sa-1-1 at EUR 2.5 a month, a 5-day trial, no free tier | the same, and the full plan ladder | holds |
| `podway` | Mini at USD 4 a month, no trial, 1 app free | the same, and the free app is attached to early access | holds, with a term |
| `shiper` | Builder at USD 5 a month, a USD 1 trial, a free tier | the same, and the plan shapes | holds |

**9 of the 18 claims are refuted, 2 more state a figure the vendor does not publish, and 7 hold,
one of them with an omission.** The direction is the finding: eight of the nine make the offer
look better than the page does, and only `appish` errs the other way by 2 hours.

| how the list is wrong | records | why a reader is worse off |
| --- | --- | --- |
| a tier the vendor does not sell | `wso2-choreo`, `ownkube`, `qoddi`, `runsite`, `mrvm` | 5 free plans that are withdrawn, narrowed, or 404 |
| the sleep rule or the session length | `faable`, `gigalixir`, `appish` | `faable` overstates survival by 120 / 30 = 4 times, and `gigalixir` says "never sleeps" where the page says 30 days |
| a feature the plan does not include | `awardspace` | the free short domain is one domain the reader brings plus three subdomains |
| an omitted card requirement | `gigalixir`, `qoddi` | the field that decides whether a reader can reach the tier |

⚠ **The omissions cost as much as the errors.** `qoddi` and `gigalixir` require a card and
neither list says so, and `cohesivity` leaves out the 100,000 vCPU-seconds that bound the
account. `podway` is correct and promotional: the free pod exists in early access and can end
without a price change.

## What the class does not give

**No GPU, at any price.** All 33 records carry `gpu_class` and `gpu_count` in their shape, and
both are null on every one. `qoddi` is filed under a category that names a GPU cloud, and the
page it cites prices no GPU line. The largest card-free credit therefore converts to CPU-hours
only: 100 / 0.0504 = 1,984.1 vCPU-hours and 0 GPU-hours. A GPU-hour figure here would be an
invention.

**A clock on what stays up.** Thirteen of the 33 publish a number.

| the number | what it is | providers |
| --- | --- | --- |
| 5 minutes | default sandbox lifetime | `qiniu-cloud-ai` |
| 30 minutes | idle sleep | `faable` |
| 4 to 8 hours | a slot, or a session on the cheapest and the next plan | `appish`, `sandock` |
| 24 hours | a session, or a continuous-live backstop | `remotehost`, `inis-run`, `ix` |
| 72 hours | an ephemeral tenant, or a session on the top plan | `cohesivity`, `remotehost` |
| 5 to 14 days | a trial | `hostim-dev`, `remotehost`, `bunny-sandbox`, `wso2-choreo` |
| 30 days | idle sleep, or a paused-session retention | `gigalixir`, `inis-run` |
| 120 days | a grace period | `apexweave` |

The other 20 records carry no numeric clock, which is not the same as no clock: `containarium`
and `velixir` sleep on idleness with no number, and `boxlite-cloud` has no session cap because
the disk meter runs instead. ⛔ **A box that stays up is not a box that keeps a process.**

**One perpetual free VM, and no IPv4.** `euserv` gives 1 core at 1 GHz, 1 GiB, 10 GB and 1 TB a
month for nothing, with one /128 IPv6 address and no IPv4, so a client reached over IPv4 has to
buy an address and the free tier becomes a paid one.

**The egress term, on most rows.** `bunny-sandbox` and `digitalocean-harness-runtime` meter
USD 0.01 per GB, so 1 TiB inside the bunny trial is 1,024 x 0.01 = USD 10.24, which is 51 per
cent of the USD 20 balance. `ix` and `boxlite-cloud` charge nothing for outbound traffic, and 17
records say plainly that no egress term was found, which is an absence and not a zero.

**Four pricing routes behind a wall.** `staxa`'s /pricing redirects to sign-in, `containarium`'s
console returns a login wall, `byteplus-ai-cloud`'s documentation renders as a script shell, and
`mrvm` has no plan page left. Reaching any of the four needs an account.

## What could not be read, and what would change the answer

Each route below was tried and failed, and each is in `extras.wave2.seen_routes`.

- `byteplus-ai-cloud`. Tried the product page (200, mechanics only), the billing overview and the
  cloud sandbox overview at docs.byteplus.com (both 200, navigation shell, no table), and a
  search that returned third-party comparison tables only. The USD 0.0351 per vCPU-hour here is
  a third party's figure and the rung is `reported`. An account would expose the console rate
  card, and may show that a personal account cannot create a sandbox at all.
- `staxa`. Tried /pricing (broker exit 1, sign-in page), a 2026-09 archive capture (none, and the
  Wayback and Cloudflare scans are empty), and a search on the site name, which returned the
  pricing table text verbatim. These numbers come from indexed text, not a live render, and the
  500m / 512Mi / 5Gi shape is an example payload in the API documentation.
- `containarium`. Tried the pricing and sandbox pages (both 200) and the hosted console at
  cloud.containarium.dev (login wall, status 409). A trial, if one exists, is invisible without
  an account, and the record says `paid-only` on that basis.
- `euserv`. Tried the VS2-free page (200) and /en/vps/vps-free/ (exit 1). The registration form
  was not read, so identity is the vendor's stated requirement and not an observed checkout, and
  whether the box accepts inbound ports beyond the vendor's no-filing proxy is unrecorded.
- `qiniu-cloud-ai` and `mrvm`. The first is fully read and gets no USD figure because no exchange
  rate was read; the second returns a placeholder and /lxc returns 404, so its cheap plan exists
  only for customers who already hold it.

**Nothing in this slice was booted.** Four probe records exist, for `inis-run`, `vers`,
`bunny-sandbox` and `qiniu-cloud-ai`, and each proves a pricing page returned 200 with a recorded
byte count and sha256: 12,856 bytes, 50,024, 73,098 and 54,413 respectively. None proves a
sandbox starts, a credit is granted, or a cap fires at the stated hour. Every "24 hours" and
"5 minutes" here is a sentence on a page.

**One record disagrees with another.** `sailboxes` records USD 5 of compute credit a month and
says this changes `sail.json`, which describes Sail Research as an inference provider with "no
free compute tier"; both records exist and cannot both be right. ⚠ The note also
overstates its own credit: "about 39 hours" at USD 0.128 counts the 16 GiB RAM floor and no CPU
second, and 1 vCPU running is 0.015 + 16 x 0.008 = USD 0.1430, so 5 / 0.143 = 34.97 hours.

**What would change the answer, in order of cost.** One BoxLite signup settles whether the USD
100 expires, which decides whether the largest card-free credit is a month or a year. One hour of
`remotehost` across the 24-hour boundary shows whether the session cap kills the process or rolls
it. One boot on `inis-run` tests the backstop and the 410. One account at `byteplus-ai-cloud`
turns a third-party rate into a documented one.
