# The perpetual free allowance

A free trial ends on a printed date. A perpetual allowance renews for as long as the
account exists. This document asks what that is worth to a reader with no local hardware: how
many machine-hours a month, what the account costs in identity, and what kills an
unattended job. The class gives 4,380 machine-hours a month across six lanes that are up
for the whole 730-hour month. Only 730 of those hours need no renewal, and whether that
lane offers a reachable address was not measured. They are not unconditional: the terms
reserve an inactivity rule the plan pages do not quantify.

## The short answer

Sorted by how long a lane survives with no human action, not by headline size. The
`mechanism` column carries one of four letters defined below, or `none` where the record is
a trial, a gate, a paid floor or a closure. A letter on a dead row is the mechanism that
row had while it was alive.

| Provider | Mechanism | Allowance | Renewal | Identity | Fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `oracle-cloud` Oracle Cloud Always Free | (a) | 1,500 OCPU-hours and 9,000 GB-hours a month | none: the tenancy stays free | card | a 7-day p95 under 20% on CPU, network and memory triggers reclaim | qualifies-with-caveat |
| `instabox` InstaBox | (a) | one 4 vCPU / 8 GiB machine a month | none, but it pauses after 30 idle minutes | email | the pause, on any job that goes silent | qualifies-with-caveat |
| `botkeep` Botkeep | (b) | 512 MB RAM, 50% CPU, 1 GB disk, 24/7 | none: the vendor states no renewal timer | email | an unquantified inactivity clause in section 5 of the terms | qualifies-with-caveat |
| `envs-net` envs.net | (d) | a Debian shell, 1 GiB soft and 1.5 GiB hard, 200 processes | no clock published | email | the 200-process cap | qualifies-with-caveat |
| `gladiolus-vm-gl` Gladiolus (vm.gl) | (b) | a Linux VM with full root access; the number of machines and the shape are not published | the page states no calendar | email, then a human reads the request | a person decides, so there is no quota to plan against | qualifies-with-caveat |
| `efn` EFN | (d) | 500 MB disk, 256 MB memory, 3 background processes, one port | log in inside 60 days | email | the 60-day disable | qualifies-with-caveat |
| `freevps-org` FreeVPS.org | (d) | 1 fair-share core, 1 GiB RAM, 20 GB disk, 250 GB a month | none stated, and none guaranteed | institution (forum) | a node rebuild takes the VM | qualifies-with-caveat |
| `boxybsd` BoxyBSD | (b) | 1 vCPU, 1 GiB, 10 GB disk, IPv6 only | extend button every 90 days | email and GitHub | the 90-day delete | qualifies-with-caveat |
| `ibm-linuxone-community` IBM LinuxONE Community | (b) | a root s390x VM for up to 120 days | re-register at day 120 | email | day 120 | qualifies-with-caveat |
| `azure-functions` Azure Functions | (c) | 1M executions and 400,000 GB-s a month | none: a monthly grant | card | a 10-minute cap on one execution | qualifies-with-caveat |
| `fastly-compute` Fastly Compute | (c) | 10M requests and 100M vCPU-ms a month | none: a monthly grant | card | 100,000 seconds of vCPU, which is 27.8 hours | qualifies-with-caveat |
| `deno-deploy` Deno Deploy | (c) | 1M requests, 20 GiB egress, 10 active-CPU hours, 150 GiB-hours memory | none: a monthly grant | email | the 20 to 30 second idle shutdown | qualifies-with-caveat |
| `val-town` Val Town | (c) | 100,000 runs a day, 1 minute per run, cron every 15 minutes | none: a daily reset | email | the 10-second idle timeout | qualifies-with-caveat |
| `cloudflare-workers-ai` Cloudflare Workers AI | (c) | 10,000 Neurons a day, reset at 00:00 UTC | none: a daily reset | email | the daily Neuron pool, not the request rate | qualifies-with-caveat |
| `z-ai-glm-flash` Z.ai GLM Flash | (c) | two models priced Free on every column | none | email | no quota is published at all | qualifies-with-caveat |
| `leapcell` Leapcell | (c) | 3 GB-hours of compute and 100,000 invocations a month, `reported` | none: a monthly grant | email | 3 GB-hours is 45 minutes at the 4 GB shape | qualifies-with-caveat |
| `render` Render | (a) | 750 instance-hours a month per workspace | none: a monthly grant | email | a 15-minute spin-down | qualifies-with-caveat |
| `render-hobby` Render Hobby | (a) | 5 GB of bandwidth a month, inside the 750 hours | none: a monthly grant | email | the 750 instance-hours, which one always-on service spends in 31 days | qualifies-with-caveat |
| `snapdeploy` SnapDeploy | (a) | 100 running hours a month across the account | none: a monthly grant | email | 100 hours shared by four apps, at 25 each | qualifies-with-caveat |
| `github-codespaces` GitHub Codespaces | (a) | 120 core-hours and 15 GB-months a month | none: a monthly grant | email; a card to continue past the quota | 120 core-hours / 2 cores = 60 wall-clock hours | qualifies |
| `harvis-dev` harvis.dev | (a) | 100,000 requests, 1 GB-month storage, 50 deploys | none: monthly, with an automatic step-up | anonymous: the record carries no signup detail | crossing one ceiling bills USD 5 with no decision | qualifies-with-caveat |
| `ibm-quantum-open` IBM Quantum Open | (a) | 10 minutes of QPU runtime per 28-day window | none: a rolling window | email | one variational loop spends the window | qualifies-with-caveat |
| `kaggle-notebooks` Kaggle Notebooks | (a) | 30 GPU hours a week, one P100 per session | weekly reset | email, then a phone number for the GPU and the Internet toggle | the 30-hour weekly GPU quota | qualifies |
| `paperspace-gradient` Paperspace Gradient | (a) | a free M4000, 5 GB storage, no monthly hour figure | none published | email | the 12-hour auto-shutdown | qualifies-with-caveat |
| `hax-co-id` Hax.co.id | (d) | an IPv6 KVM, reported at 1 to 1.5 GiB and 7 to 10 GB | renew about weekly, with a captcha | not stated: the record's identity kind is `any-phone` and its detail says the gate is not proved | deletion at 17:00 UTC on the day it lapses | qualifies-with-caveat |
| `openworld` Openworld | (d) | 1 vCore, 512 MB, 5 GB disk, 50 GB a week on consumer hardware in Honduras | one click every 24 hours | email through Discord | suspension at day 7 | qualifies-with-caveat |
| `woiden-id` Woiden.id | (d) | a NAT VPS, reported at 1 GiB and 8 GB | a login every day | institution | the first missed day | qualifies-with-caveat |
| `qualcomm-device-cloud` Qualcomm Device Cloud | none | free minutes per device, reported at 5,000 | a reviewed request for more | email | the pool does not renew on its own | qualifies-with-caveat |
| `tilde-team` tilde.team | (d) dead | a shared shell, approved by a human | none | email | the user host was destroyed in August 2026 | dead |
| `akamai-edgeworkers` Akamai EdgeWorkers | none | 60M events a month across two products | an approved contract | not stated: an active Akamai contract is the gate, and the record names no card, phone or document | the approval itself | fails-identity |
| `nvidia-dsx-air` NVIDIA DSX Air | none | 10,000 compute-hour credits, 60 vCPU, 1 year | push the sleep date every 72 hours | institution: a non-public domain mailbox behind an NGC organization owner | a non-public email domain | fails-identity |
| `sparkcloud` SparkCloud | (d) | six free components on one account, no figure published | none stated | institution by age: verified 13 and over, per the record's detail | age verification | fails-identity |
| `alibaba-cloud-tencent` Alibaba Cloud, Tencent | none | 7 to 30 day trials across five vendors | none | national identity document: real-name verification | the expiry date | fails-identity |
| `huawei-cloud-modelarts` Huawei Cloud ModelArts | none | one 1-hour CodeLab session, one per user | a new session every hour | national identity document: a mainland China account, per the record | release after 72 idle hours | fails-identity |
| `gratisvps` GratisVPS | none | 2 vCPU and 2 GiB claimed | an ad click | phone: an SMS wall before credentials are issued | no root password is issued | fails-identity |
| `simpfun` SimpFun | none | 4 vCPU and 16 GiB while points last | a daily check-in | national identity document plus an invitation code and a CNY 1 fee | two points of margin a day | fails-identity |
| `cloud-studio` Cloud Studio | none | 2,000 machine-hours from a platform defect | unreproducible | not established: no page stating the signup requirement was read | it was a bug, not an offer | trial-only |
| `intel-tiber-developer` Intel Tiber Developer | none | 120 days, 192 GB RAM, oneAPI toolchain | extensions, unquantified | email | day 120 | trial-only |
| `kamatera` Kamatera | none | no free tier on the pricing page | none | card | the USD 4 a month floor | trial-only |
| `sap-business-technology` SAP Business Technology | none | a 90-day trial, Kyma for 30 days | none | card | day 90 | trial-only |
| `arvan-cloud` Arvan Cloud | none | free CDN, object storage, video and support only | a 30-day base plan on those products | institution | no compute product has a base plan | paid-only |
| `ibm-cloud` IBM Cloud | none | USD 200 of credit for 30 days; Lite plans, none of them a virtual server | none | card | the card at registration | trial-only |
| `idcloudhost` IDCloudHost | none | a top-up bonus only: IDR 55,000 in returns IDR 100,000 of bonus balance | none | institution | the IDR 55,000 top-up, and its own NEO Lite floor of IDR 87,000 | paid-only |
| `vpsfree-cz` vpsFree.cz | none | 8 cores, 4 GiB, 120 GB for a member | EUR 12 a month | email | the fee | paid-only |
| `vpsfree-es` VPSFree.es | none | EUR 2.45 a month | a card | card | there is no free tier | paid-only |
| `deta-space` Deta Space | (b) dead | a free always-on personal cloud with disk | none: it ended | email | shut down 2024-10-17, data deleted | dead |
| `digitalocean-open-source` DigitalOcean Open Source | none dead | recurring credits for open-source projects | an annual renewal that stopped | institution | the programme ended with no public notice | dead |
| `dimension-sh` dimension.sh | (d) dead | a tilde shell | none | anonymous | closed February 2026 | dead |
| `firebase-studio` Firebase Studio | (b) dead | 3 workspaces per user | none | email | signups closed 2026-06-22, sunset 2027-03-22 | dead |
| `fosshost` Fosshost | (d) dead | free VPS for about 250 projects | none | anonymous | end of life December 2022 | dead |
| `glitch` Glitch | (b) dead | free app hosting, no card, no published meter | none | email | hosting ended 2025-07-08 | dead |
| `lightning-ai` Lightning AI | (b) dead | one free 24/7 Studio, 80 GPU hours to start | none, but a restart every 4 hours | email | access revoked 2026-10-16 | dead |
| `ona-cloud` Ona Cloud | none dead | a free workspace | none | email | winds down 2026-10-31 | dead |
| `strapi-cloud` Strapi Cloud | none dead | a free project | none | email | the free plan was removed 2026-07-01 | dead |
| `joule` joule (self-hosted) | none | inference earned by donating GPU time | continuous contribution | anonymous: no account is recorded | no contribution, no access | fails-quota |

## Four mechanisms that do not compare

Each record is placed by what ends it, not by what it gives. A record can be metered and
also have a clock, and the clock is what kills an unattended job.

| mechanism | the thing that ends it | the tell |
| --- | --- | --- |
| (a) monthly-resetting quota | the meter: a pool resets on a calendar period and is spent by occupying a machine | an hour, core-hour or GB-hour count |
| (b) perpetual free tier, fixed shape | nothing, until a term or the vendor's next document change | a machine size with no meter beside it |
| (c) zero-cost endpoint per request or CPU-second | the request: nothing is resident, so nothing can be occupied | a request, vCPU-ms or token count |
| (d) donated or community host | a person: no invoice exists, so no contract restrains the host | a host writing in the first person |

⭐ (a) counts hours of a machine, so its numbers add, badly but dimensionally. (c) counts
six meters in this slice: memory-seconds at Azure, vCPU-milliseconds at Fastly, active-CPU
hours at Deno, GB-hours at Leapcell, runs at Val Town, and tokens at Cloudflare, with Z.ai
publishing no meter at all. ⛔ There is no total for group (c).

Three assumptions follow. **A1**: a month is 730 hours, or 2,628,000 seconds, which is the
figure Oracle's own arithmetic uses. **A2**: one request a second, sustained, is 2,628,000
requests a month. **A3**: a request spends 10 milliseconds of vCPU, used only where both a
request count and a CPU-time count are published.

## Mechanism (a): the quota that resets itself

| Record | Allowance as stated | Usable hours a month | The assumption |
| --- | --- | --- | --- |
| `oracle-cloud` | 1,500 OCPU-hours | 730 hours at 2 OCPU, using 1,460 of 1,500 | none stated: both numbers are in the record |
| `render` | 750 instance-hours | 750 hours; one always-on service uses 744 in 31 days | none |
| `snapdeploy` | 100 running hours | 100 hours, or 25 per app across four apps | the cap is shared, as stated |
| `github-codespaces` | 120 core-hours | 120 / 2 = 60 hours at 2 cores | every hour is billed at the 2-core multiplier |
| `instabox` | one 4 vCPU / 8 GiB machine a month | 730 hours | the machine survives the month, paused or running |
| `harvis-dev` | 100,000 requests | 0 machine-hours; 0.038 requests a second | A1 and A2 |
| `ibm-quantum-open` | 10 minutes per 28 days | 0.17 hours per 28 days, or 2.2 hours a year | none |
| `kaggle-notebooks` | 30 GPU hours a week | 130 hours in a 730-hour month | 30 x 730 / 168 |
| `paperspace-gradient` | no monthly figure published | not published | none |

The published hours add to 2,500: 730 at Oracle, 750 at Render, 100 at SnapDeploy, 60 at
Codespaces, 730 at InstaBox and 130 at Kaggle. Render Hobby shares Render's 750, so a
second add would count one pool twice. They sit on six machine sizes, so the total
describes the class and not a machine anyone can use.

⭐ Oracle is the only (a) record whose single box publishes an address and runs a whole month,
and the allowance is not what binds. 1,500 divided by 730 gives 2.05 OCPUs, so a 3-OCPU box
needs 2,190 and does not fit; a 2-OCPU box uses 1,460 and leaves 40, which is 1.7 days of one
core spare. The
binding constraint is the idle test: over 7 days, a 95th-percentile CPU, network and memory
each under 20% may trigger reclamation
(`docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm`,
read 2026-10-22, `documented`). A polling job at 3% CPU is what that test catches.

⚠ "Perpetual" at Oracle means until the next documentation change. The allowance was 4 OCPU
and 24 GiB with 3,000 OCPU-hours until 2026-06-15, when it became 2 and 12 with 1,500 and no
announcement (`infoq.com/news/2026/07/oracle-cloud-free-tier-limits/`, read 2026-10-22);
enforcement began on 2026-08-18 (`news.ycombinator.com/item?id=49183750`, read 2026-10-22,
`reported`).

## Mechanism (b): a fixed shape with no meter

Four live records give a machine and never count the use, and three publish the size. That is
the shape the class is named for. The four are `botkeep`, `boxybsd`, `gladiolus-vm-gl` and
`ibm-linuxone-community`. The three with a stated shape are `botkeep`, `boxybsd` and
`ibm-linuxone-community`; `gladiolus-vm-gl` publishes none.

`botkeep` is the only one with no clock: one server, 512 MB of RAM, 50% of a CPU, 1 GB of
persistent storage, 24/7, and the free plan "does not require periodic manual renewal"
(`botkeep.cloud/faq`, read 2026-10-22, `documented`). The qualifier sits in the terms:
section 5 states the entitlement "has no recurring price or scheduled expiry" and reserves
"inactivity rules" without quantifying them, and section 14 allows suspension for "prolonged
inactivity" (`botkeep.cloud/terms`, read 2026-10-22). Those terms pool two slots at 1 GB of
RAM, 1 vCore and 1 GB of storage, so the plan page's 512 MB is half the account budget.
`boxybsd` gives 1 vCPU, 1 GiB and 10 GB on IPv6 at EUR 0 a month, and deletes the box when a
90-day lifetime expires unless the extend button is pressed. A "can be destroyed at any time
for no reason" clause sits beside the offer (`boxybsd.com`, read 2026-10-22, `measured`). The
4 vCPU and 16 GiB tier is out of stock.

`ibm-linuxone-community` gives a root s390x machine for up to 120 days at no cost and no
card, and every resource returns to the pool at expiry (`linuxone.cloud.marist.edu`, read
2026-10-22, `documented`). The renewal is a fresh registration rather than a click. It is not
the only non-x86 lane: `qualcomm-device-cloud` also qualifies and gives ARM64, at 5,000
minutes per device rather than a VM.

## Mechanism (c): the endpoint that is never held

Seven records answer a request for nothing and hold no process, so none is an always-on half.

| Record | Meter | The hours, with the assumption named |
| --- | --- | --- |
| `azure-functions` | memory-seconds | 400,000 GB-s at the 128 MB minimum, which the record divides as 0.125 GB, is 3,200,000 seconds, or 888.9 hours of one slot |
| `fastly-compute` | vCPU-milliseconds | 100,000,000 vCPU-ms is 100,000 seconds, or 27.8 vCPU-hours, a 3.8% duty cycle of one core over A1 |
| `deno-deploy` | active-CPU hours | 10 hours; the 150 GiB-hours memory pool is 200 hours at the 768 MB default allocation, read as three quarters of a GiB |
| `val-town` | runs | 96 cron firings a day at the 15-minute floor, 2,880 in 30 days, 48.0 hours at 60 seconds each |
| `cloudflare-workers-ai` | tokens | not hours: 10,000 Neurons a day is 300,000 over 30 days, or 9.8M output tokens at the qwen3-30b rate |
| `leapcell` | GB-hours | 3 GB-hours at the 4 GB shape is 0.75 hours, or 45 minutes |
| `z-ai-glm-flash` | not published | not published |

The request counts look large and are small. 100,000 requests a month, the `leapcell` and
`harvis-dev` figure, is one every 26 seconds; 1M is 0.38 a second; 10M is 3.8. A scheduler
fits in 100,000 requests a month, and a web service does not.

⚠ Azure's grant carries a footnote the headline omits: the free grants "apply to the
on-demand meters on paid, consumption subscriptions only"
(`azure.microsoft.com/en-us/pricing/details/functions/`, read 2026-10-22). A subscription with
no billing method may not carry it at all, and one execution is capped at 10 minutes, so
3,200,000 seconds is at most 5,333 full-length runs and never one resident worker.

## Mechanism (d): the donated host

Seven live records come from a person, a nonprofit or a free-VPS operator, and none issues an
invoice. No contract restrains any of them. `tilde-team` is the eighth record in this group and
it is `dead`.

`envs-net` is the strongest on every measure except reach. It answers SSH today: a TCP
connect succeeded in 210 ms and the host sent `SSH-2.0-OpenSSH_10.0p2 Debian-7+deb13u4`, in
the saved run at `sources/2026-10-24/compute/tcp-probe-20261024T043117.200Z.json`, and the
root page answered HTTP 200 with 53,226 bytes and no challenge (`envs.net`, read 2026-10-24,
`measured`). The account gives a Debian 13 shell over SSH and mosh, 200 processes, 1 GiB of
soft storage against 1.5 GiB hard and a 250 MB mailbox. The record publishes no port policy,
so whether it will hold a listener is unestablished rather than refused.

`efn` gives 500 MB of disk, 256 MB of memory, 3 background processes, 20 simultaneous
processes and one listenable TCP or UDP port at USD 0.00 a month
(`shells.efn.lt/services`, read 2026-10-22). The port is what most pubnixes withhold, and the
same page excludes "proxy services, or tunneling mechanisms (such as TOR, SSH, TCP, or UDP
tunneling)" and "AI and other CPU intensive tools", so the port carries a small daemon and not
a tunnel. The clock is 60 days: "any shell account that has not been logged into for 60
consecutive days will be automatically disabled", with a VIP exception for donors
(`shells.efn.lt/start`, read 2026-10-22). A TCP connect from the probe host timed out at 32,253 ms
in the saved run at `sources/2026-10-24/compute/tcp-probe-20261024T050356.219Z.json`, which
matches the 32,376 ms the record carries, and it is recorded as no answer from the probe host rather
than as a dead provider.

`tilde-team` is the case study, and its record now reads `dead`. Someone gained a root shell
and ran `rm -rf /`; the host writes "ssh access is currently disabled in the meantime", and
the user host was destroyed in August 2026 (`tilde.team`, read 2026-10-22, `documented`). The
account is approved by a human, so the first thing that fails is the host.

`freevps-org` is the only (d) record with real inbound reachability at a stated size: 1
fair-share core, 1 GiB of RAM rising to 2 on justification, 20 GB of disk, 250 GB a month on
a 150 Mbit/s port and 20 forwarded NAT ports plus a /64. The price is reputation: a forum
account three months old, with 50 substantive posts and 25 thanks (`freevps.org`, read
2026-10-22, `documented`). The offer thread adds "no SLA", "RAID0 YOLO mode" and no backups.

`hax-co-id` and `woiden-id` are one product with two clocks. Hax creates each VPS for one
week, and the renewal page needs the site address typed and an arithmetic captcha solved
(`wiki.hax.co.id/ipv6-servers/getting-started/`, read 2026-10-22). The record is `unverified`
and states no default term, so the week is the wiki's figure rather than a measured clock.
Woiden reclaims unless renewed daily, and one missed weekend loses the machine and its data;
that cadence is `reported` from a third-party comparison, not from the vendor page.

## The renewal mechanic

The mechanic is the finding: it is what an unattended job dies on, sorted by cadence.

| Clock | Records | Actions a year |
| --- | --- | --- |
| every day | `woiden-id`, `simpfun` | 365 |
| every 7 days | `hax-co-id`, `openworld` | 52 |
| every 28 days, rolling | `ibm-quantum-open` | 13 |
| every 60 days | `efn` | 6 |
| every 90 days | `boxybsd` | 4 |
| every 120 days | `ibm-linuxone-community`, `intel-tiber-developer` | 3 |
| monthly, automatic | the (a) group, except `ibm-quantum-open`, `kaggle-notebooks` and `paperspace-gradient` | 0 |
| weekly, automatic | `kaggle-notebooks` | 0 |
| daily, automatic | `cloudflare-workers-ai` | 0 |

Four actions cannot be automated from a shell: a captcha at `hax-co-id`, a click at
`openworld`, an extend button at `boxybsd` and a daily check-in at `simpfun`. The check-in is
the tightest economy here: 50 points a day against a 48-point daily cost leaves a margin of
two, so one missed day stops the server (`simpfun.tx648.cn/`, read 2026-10-22, `reported`).

⭐ A renewal can be driven by a cron on another free host, and every (d) record with a clock
needs that. The chain has to bottom out somewhere with no renewal clock. Two lanes here have
none: `botkeep` and `gladiolus-vm-gl`. Only `botkeep` states a shape, and its public address
is inferred rather than measured.

## What the class is worth in a month

Six live lanes are up for the whole 730-hour month: `oracle-cloud` at 2 OCPU, `instabox` at
4 vCPU and 8 GiB, `botkeep` at half a core and 512 MB, `envs-net` and `efn` as shells, and
`freevps-org` at one fair-share core. That is 6 x 730 = 4,380 machine-hours. Converting the
four that publish a core count: 1,460 OCPU-hours at Oracle, 2,920 vCPU-hours at InstaBox
(4 x 730), 365 at botkeep (0.5 x 730) and 730 at FreeVPS.org (1 x 730) add to 5,475.
`gladiolus-vm-gl` is a seventh lane and publishes no shape, so it enters no sum here.
`envs-net` and `efn` publish no core count either, so the 4,380 counts them as one machine
each without knowing how much of one they are.

⚠ Two of the six are conditional: Oracle is reclaimed if the workload sits under 20% for a
week, and InstaBox pauses after 30 idle minutes. Two more are unestablished on inbound:
`envs-net` publishes no port policy and `efn` offers one port, which did not answer from this
host. The capacity with no calendar is
`botkeep`: 730 hours of 512 MB and half a core, one sixth of 4,380, and it holds only while
the unquantified inactivity rule in its terms does not fire. Its public address is `inferred`
and was not measured: the record's `interface` is `unknown`.
Everything else needs a condition met, and the (c) group adds no resident hours at all, so
adding its 888.9 Azure slot-hours to the 4,380 would count two different things.

## The hosts that shut down

Ten records here are closed, and the dates are the argument. The class's instability is not
a risk the reader takes on; it is a measured rate: seven of the ten stopped accepting a new
user inside the 18 months before this read, and `digitalocean-open-source` carries no
published date at all.

| Record | What it was | The end |
| --- | --- | --- |
| `deta-space` | a free always-on personal cloud with persistent storage | sunset 2024-10-17, then all apps and data deleted |
| `fosshost` | free VPS and AArch64 compute for about 250 projects | suspended September 2022, end of life December 2022, chief executive unreachable |
| `glitch` | free app hosting, no card, instant deploys | hosting and profiles shut down 2025-07-08, final post 2025-07-23 |
| `dimension-sh` | a tilde community, five years old | closed February 2026; the site is a memorial |
| `strapi-cloud` | a free project tier | free plan removed 2026-07-01, projects deleted 2026-09-01, on the ground that most free projects were never used |
| `firebase-studio` | 3 free workspaces | new workspaces and signups disabled 2026-06-22, sunset 2027-03-22 |
| `lightning-ai` | a free 24/7 Studio with a persistent disk | all access revoked 2026-10-16 at 01:00 UTC after a credential compromise |
| `ona-cloud` | a free workspace | notice published 2026-10-13, winding down 2026-10-31, signups closed |
| `tilde-team` | a shared shell approved by a human | root compromise and `rm -rf /`; SSH disabled, verdict `dead` |
| `digitalocean-open-source` | recurring credits for open-source projects | ended by email to recipients only, with no public announcement |

Glitch ended in July 2025, Strapi Cloud in July 2026 and Ona Cloud in October 2026. None of
the three died of a quota; each was withdrawn as a product.
`digitalocean-open-source` shows the quiet version: a reader checking the vendor's public
pages would still find the programme described as available, and only the participants got
the email. `lightning-ai` is the newest: its pricing page still advertises the
free Studio while the incident page states the platform is closed to all users.

## What the class does not give

**A trial is not an allowance.** `alibaba-cloud-tencent` records 7 to 30 day trials across
five vendors, all gated on real-name verification and all auto-released at expiry.
`huawei-cloud-modelarts` gives one 1-hour session per user and releases the instance after 72
idle hours. `sap-business-technology` gives 90 days, with its free tier needing a
Pay-As-You-Go or enterprise agreement. `intel-tiber-developer` gives 120 days on
pre-production silicon, `kamatera` has no free tier on the pricing page at all, and `ibm-cloud`
gives USD 200 of credit for 30 days on an account that is Pay-As-You-Go from registration.

**Identity is the wall, not the quota.** `alibaba-cloud-tencent`, `huawei-cloud-modelarts`
and `simpfun` need a national identity document. `nvidia-dsx-air` needs a non-public domain
mailbox behind an NGC organization owner, so a custom domain is the price of 10,000
compute-hour credits. `sparkcloud` needs an age inside a verified range. `freevps-org` needs
three months of forum participation. `gratisvps` reports an SMS wall after which no root
password is issued, so its 2 vCPU and 2 GiB exist only as a claim. `joule` sells inference
for donated GPU time, which a reader with no GPU cannot buy.

**The paid floor is close.** `vpsfree-cz` is EUR 12 a month for 8 cores, 4 GiB, 120 GB and a
public IPv4, and the name is about software freedom rather than price. `vpsfree-es` is a
different company at EUR 2.45 a month, `idcloudhost` gives an IDR 100,000 bonus against a
IDR 55,000 top-up and sells its own VM from IDR 87,000 a month, `kamatera` starts at USD 4, and
the `idcloudhost` record also carries Biznet Gio at IDR 50,000 a month for a NEO Lite box.

**An approval is not a quota.** `akamai-edgeworkers` publishes 60 million events a month and
gates it on an active contract, with a manual trial review as the only other route.

## How it composes

An always-on half needs a resident process, an address and no clock shorter than the job, and
no lane here is measured to have all three. `botkeep` would hold a webhook receiver or a poller
behind a public HTTPS URL and never sleeps, which is `inferred` from the offer: the record's
`interface` is `unknown` and was not probed, so no public address was measured. `oracle-cloud`
is the workload half: a full VM, a public IPv4, 10 TB of egress a month and 730 hours, provided
the job keeps utilisation above the reclaim threshold. `freevps-org` supplies what Oracle does
not: 20 forwarded ports and a /64, once the forum reputation is paid.

The scheduling half needs no machine. `val-town` fires a cron every 15 minutes, 96 firings a
day inside 100,000, and its "Email yourself" action makes it a free alerting path for a box
expected to die. `cloudflare-workers-ai` pairs with a free Worker for a nightly batch.

What cannot be the always-on half, and the clock that rules it out: `render` and `snapdeploy`
at 15 minutes, `instabox` at 30 minutes, `deno-deploy` at 20 to 30 seconds, `val-town` at 10
seconds, `azure-functions` at a 10-minute execution cap, `fastly-compute` at one request at a
time, `github-codespaces` at a stop and a 30-day deletion, `kaggle-notebooks` and `paperspace-gradient`
at a session, and `lightning-ai` at 4 hours while its platform is closed outright.

⭐ The arrangement worth naming: `botkeep` as the receiver, `oracle-cloud` as the worker,
`val-town` as the clock and the alert path, and `hax-co-id` only where a human is present for
the captcha. A chain that needs the fourth lane unattended will break on a Saturday. The first
lane is the one to test: its address is inferred, so the chain rests on an unmeasured field.

## What would change the answer

- One 30-day observation of a silent `botkeep` container. If one survives with no traffic,
  the capacity with no calendar rises from 730 hours to 1,460 and is observed rather than
  inferred; if not, it has none.
- Whether the Azure free grant attaches to a subscription with no billing method. The
  footnote says paid consumption only and the always-free page lists Functions at 1M
  requests, so 888.9 slot-hours turns on the answer.
- One probe of the `hax-co-id` renewal endpoint, to see whether the captcha can be answered
  without a human. Every unattended chain through the free-VPS group depends on it.
- The Z.ai rate-limit page, behind a login: until it is read, `z-ai-glm-flash` has a free
  price and no measurable ceiling. `paperspace-gradient` publishes no monthly GPU figure,
  and the `leapcell` invocation count rests on a third-party tracker.
