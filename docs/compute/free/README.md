# The free lane: what costs nothing, and what it charges instead

Free compute is not a smaller version of paid compute. It is a different mechanism
with a different failure. A paid server fails on the invoice, which arrives at a known
time and says a number. A free tier fails on a clock, a quota, or a decision made by
one person in another timezone, and it usually fails silently.

This page states the shape of the free lane as one argument, then the three products
that are called a free tier and are not the same product, then the ranking by what a
reader can obtain tonight. The twenty-nine documents beside it carry the providers.

## The argument in one page

**No free tier in this corpus is a machine that stays up for a year.** Two are close
and each carries a clock: Oracle's Always Free is a real 2 OCPU VM with 10 TB of egress
a month that Oracle reclaims if a seven-day 95th-percentile utilisation stays under 20
per cent, and Google's e2-micro has no idle reclaim at all and gives 1 GB of egress a
month. A third was close until 2026-10-16: Lightning's free Studio ran 24/7 and
restarted every four hours, and the vendor revoked all user access to the platform on
that date. Everything else in the lane is a shell, a sandbox, or a credit.

So the free lane is a composition, and the composition has four jobs.

| job | provider | ceiling | what it costs instead |
|---|---|---|---|
| an always-on address | Oracle Cloud Always Free | 2 OCPU, 12 GB, 200 GB, 10 TB a month | a 7-day p95 reclaim test, and a card and phone at signup |
| a machine with no card | Google Cloud e2-micro | 1 GB, 30 GB, 1 GB egress a month | an egress allowance that is 0.0067 per cent of one day's 500 GB serving |
| a shell that survives | the pubnix layer | 1 to 3 GB, no inbound port | a login clock, and a shared kernel |
| a burst sandbox | a dozen providers | 1 to 24 hours per session | a session cap, an idle reap, or a one-time credit |

Each row is a different kind of promise. Oracle's is a time-denominated quota with a
reclaim rule attached. Google's is a monthly allowance. The pubnix layer is a
volunteer's server. A sandbox credit is a single grant.

The failure each one meets, in the order it is likely to arrive:

- The always-on lane fails on **the reclaim test**, not on capacity. A workload that
  sleeps for five days and bursts for two is at risk, because the test is a percentile
  over the window and not a total.
- The no-card lane fails on **egress**. One GB a month is not a serving allowance; the
  daily target is 500 GB to 1 TiB.
- The shell lane fails on **the login clock**. Every pubnix here sweeps an account that
  does not log in, and the windows run from 30 days to five years.
- The sandbox lane fails on **the session cap**. Fifteen minutes idle is the common
  number and it kills any process that waits for input.

## Three products called a free tier

⭐ The distinction is the most expensive confusion in this topic. A reader who sees
"USD 300 free" and plans ten months has planned for one month and nine of nothing.

| kind | records | what it is | what it costs to rely on |
|---|---|---|---|
| allowance | 145 | a perpetual quota, usually in hours, seconds or requests | nothing, until the quota runs out mid-task |
| one-time credit | 54 | a single grant, spent once | the second month |
| trial | 28 | a clock with a stated end | the end date |
| recurring credit | 11 | a credit that renews each month | nothing; it is the only one that budgets |
| prepaid credit | 1 | credit bought ahead at a discount | the purchase |
| none | 165 | no free tier at all | the invoice |

Eleven rows out of 404 carry a credit that renews. That is 2.7 per cent of the market,
and Modal's USD 30 is the largest of them. ⚠ The famous USD 200 and USD 300 grants from
AWS, Azure and Google are one-time. **Oracle is not in that list**: its Always Free
capacity is a perpetual monthly allowance of 1,500 OCPU-hours, not a grant, and a reader
who files it as a credit plans for one month instead of twelve.

## Ranked by what a reader can obtain tonight

The column that decides everything is the clock, not the quota. A 24-hour sandbox with
12 GB is worth less than a 512 MB shell that answers next month.

| Provider | Free tier | Clock | Identity | Verdict |
| --- | --- | --- | --- | --- |
| Oracle Cloud Always Free | 2 OCPU, 12 GB, 200 GB, 10 TB egress | 7-day reclaim at p95 under 20% | card | qualifies-with-caveat |
| Google Cloud Free Tier | 1 e2-micro, 30 GB disk, 1 GB egress a month | none; the monthly hour allowance is the cap | card | qualifies-with-caveat |
| Lightning AI | 1 CPU Studio free 24/7, 80 GPU hours to start | access revoked 2026-10-16; the restart was every 4 hours | email | dead |
| Cloudflare Workers | 100,000 requests a day, 10 ms CPU, 128 MB | none; 10 ms of CPU per request | email | qualifies-with-caveat |
| Cloudflare Durable Objects | 128 MB, stateful, 13,000 GB-s a day | none while connected | email | qualifies-with-caveat |
| Kaggle Notebooks | 30 GPU hours a week on a P100 | 60-minute idle timeout | any-phone | qualifies-with-caveat |
| GitHub Codespaces | 120 core-hours and 15 GB-months a month | 120 core-hours, then blocked without a card | card | qualifies-with-caveat |
| Freestyle | 200 vCPU-h and 400 GiB-h a month | hard stop, no persistent VM on Free | email | qualifies-with-caveat |
| Modal | USD 30 a month, recurring | 5-minute default lifetime | email | qualifies-with-caveat |
| E2B | USD 100 one-time | 1 hour per session | email | trial-only |
| Vercel Sandbox | 5 active-CPU hours a month | 45-minute maximum session | email | qualifies-with-caveat |
| Daytona | USD 200 one-time | 15 minutes idle by default | email | qualifies-with-caveat |
| Upstash Box | 5 CPU hours a month | 5 GB disk on the entry shape | email | qualifies-with-caveat |
| Railway | anonymous 2 vCPU / 2 GB | 24 hours to claim, 3 boxes per IP a day | anonymous | trial-only |
| SDF Public Access UNIX | 20 MB on four filesystems | expires 2 years after the last login | email | qualifies-with-caveat |
| tilde.club | 1 GB soft, 3 GB hard | no idle policy published | email | qualifies-with-caveat |
| hashbang | 512 MB, 50% CPU | a 30-day login sweep | email | qualifies-with-caveat |

⭐ **194 of the 210 qualifying records need no card**: 193 want an email address and one
wants any phone. Sixteen want a card, and those sixteen are the rows where the largest
allowances sit. That split is the identity finding of this topic in one line.

⚠ **Three of the card rows are the best free capacity here.** Oracle, Google's e2-micro
and GitHub Codespaces all sit behind a card, and a card is a payment relationship even
when the charge is zero. Oracle may place a USD 0 to 1 authorisation hold.

## Four rows that look free and are not

These carry a `qualifies` verdict and their own records say there is no free tier.
They are the vocabulary defect this topic carries, and reading them as free rows is
the mistake they prevent.

| Provider | Verdict | What the record actually says |
| --- | --- | --- |
| Google Compute Engine GPU VMs | qualifies-with-caveat | no free-tier allowance applies to any GPU or TPU; billing starts with the first second |
| Azure GPU VMs | qualifies-with-caveat | the 750 free hours name three burstable CPU families and no GPU |
| Baseten | qualifies-with-caveat | the resources page publishes no free tier and no rate |
| boat | qualifies | no free tier is published; the smallest plan is USD 20 a month as credit |

`gaps.md` carries the class-level version of this: 57 records hold a `qualifies*`
verdict with `extras.free_tier_kind: none`.

## What the free lane is not

**It is not always-on in the sense a daemon needs.** Three rows survive a week of
silence and one of them is a 128 MB isolate that cannot run a binary.

**It is not a disk.** The pubnix quota is megabytes and a sandbox root filesystem dies
with the sandbox. Persistent storage is a paid product everywhere in this lane, and
`storage` owns the free versions of it.

**It is not durable.** Every row is one policy change from being wrong. Play with
Docker was withdrawn, Run Cloud retired its sandboxes for new organisations, and
Fly.io closed its free tier to new accounts. All three are in `dead-ends.md` with the
sentence that closed them. The always-on row went the same way on 2026-10-16, when
Lightning AI revoked all user access.

**It is barely measured.** ⛔ Four of 1,411 records carry the `measured` rung:
`nebius-ai-cloud`, `playht-playai`, `vast-ai-listing-structure` and
`zenix-open-source-sponsorship`, and each was measured at the transport, listing or price
level rather than at the quota. Every clock and every quota here is otherwise a page
somebody read, and `measurement.md` states why the ladder puts a probe below a documented
quota.

## The documents

| document | the question it answers |
| --- | --- |
| [`sandboxes-container-vm.md`](sandboxes-container-vm.md) | which sandbox can I hold a session open in tonight, and for how long |
| [`sandbox-long-tail.md`](sandbox-long-tail.md) | the other 110 sandboxes, by kind, and what a credit actually buys |
| [`sandbox-long-tail-2.md`](sandbox-long-tail-2.md) | the remaining 58, grouped by the mechanism that stops the workload |
| [`sandbox-newcomers.md`](sandbox-newcomers.md) | what the newer sandboxes charge, and which aggregator tier is missing |
| [`always-on-free.md`](always-on-free.md) | which free machine answers at 03:00 without a keepalive |
| [`anonymous-vms.md`](anonymous-vms.md) | what can I get with no account at all |
| [`dev-environments.md`](dev-environments.md) | which free IDE or devbox gives a persistent disk |
| [`dev-environment-long-tail.md`](dev-environment-long-tail.md) | the other 24 dev environments, and the durability axis |
| [`platform-hosts.md`](platform-hosts.md) | which free PaaS keeps a process up, and the four that need an existing cloud account |
| [`platform-host-long-tail.md`](platform-host-long-tail.md) | the other 15 platform hosts, the eight that need a self-managed server, and the clock none of them states |
| [`gpu-notebooks.md`](gpu-notebooks.md) | which free GPU exists, in which class, for how many hours |
| [`agent-browser-hosts.md`](agent-browser-hosts.md) | how many free browser minutes, and what the proxy costs |
| [`browser-host-long-tail.md`](browser-host-long-tail.md) | the other 29 browser hosts, and which allowances recur |
| [`runtimes-serverless.md`](runtimes-serverless.md) | what answers an HTTP request for nothing, and what is the CPU wall |
| [`free-tier-census.md`](free-tier-census.md) | how many free tiers are recurring, one-time, or a trial |
| [`chains.md`](chains.md) | which free resources compose into something none gives alone, and what breaks each |
| [`hpc-allocations.md`](hpc-allocations.md) | is any national supercomputer open to a person with no institution |
| [`research-grids.md`](research-grids.md) | which grids and science gateways open on an email address, and how little they award |
| [`startup-credits.md`](startup-credits.md) | which founder credits one person can reach |
| [`research-credits.md`](research-credits.md) | which research grants are real, and which need a PI |
| [`decentralized-gpu.md`](decentralized-gpu.md) | what the decentralized marketplaces are worth once supply is counted |
| [`regional-clouds.md`](regional-clouds.md) | what exists outside the US and EU mainstream |
| [`asian-clouds.md`](asian-clouds.md) | which Chinese, Korean, Japanese and Indian lanes are reachable |
| [`forum-hosts.md`](forum-hosts.md) | what the Chinese, Russian, Korean and Japanese forums offer that English-language sources miss |
| [`student-and-education.md`](student-and-education.md) | which education gate verifies the person and which the institution |
| [`perpetual-allowances.md`](perpetual-allowances.md) | what renews forever and survives an unattended month |
| [`ci-as-compute.md`](ci-as-compute.md) | which CI runner is usable as a machine |
| [`ai-and-data-credits.md`](ai-and-data-credits.md) | what one person reaches from AI and data vendors, and what only a company can claim |
| [`devtool-and-platform-credits.md`](devtool-and-platform-credits.md) | developer tools, platform hosts, prizes and open-source funds, cash separated from compute |
| [`credit-ranking.md`](credit-ranking.md) | which twenty balances are the largest a person can reach, what each costs at the gate, the hourly rate each balance sustains, and the machine it buys at 24/7 |
