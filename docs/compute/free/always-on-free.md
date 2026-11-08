# Which free machine answers at 03:00 without a keepalive

An always-on free tier is a different product from a free credit. The question is
not what it costs but whether it is still running when nothing has touched it for a
week. Three mechanisms decide that, and every row in this document is sorted by
them: an idle reclaim that watches utilisation, an inactivity timer that watches
traffic, and a login expiry that watches the human.

The answer: six rows carry no clock at all, and only one of them is a real VM
with a public address. Oracle Cloud Always Free is a 2 OCPU, 12 GB, 200 GB VM with
10 TB of egress a month, and it will be reclaimed if its seven-day
95th-percentile utilisation stays under 20 per cent, or if the account is left
idle for 30 days. Google's e2-micro has no idle reclaim at all and gives 1 GB of
egress a month. Cloudflare's Durable Object holds state and a WebSocket for
nothing but cannot run a binary. A member of that group was Lightning AI's free
Studio, which ran 24/7 and restarted every four hours until 2026-10-16, when the
vendor revoked all user access.
Everything else in this document is a shell with a login clock or a service that
sleeps.

## The comparison

The five-way tier is the load-bearing distinction in this document. Four of the five tiers
count toward an always-on free node; the fifth is not a tier at all and exists to
stop an unreachable row from being counted as one. Every row in the comparison table
is in exactly one of the five.

| tier | definition | count |
| --- | --- | --- |
| **T1** | always-on as it stands. No idle sleep, no session cap, no login expiry, no archival. Nothing needs doing to keep it. | 6 |
| **T2** | always-on with a keepalive, or with an expiry long enough to schedule around. It sleeps, scales to zero, is reclaimed when idle, or archives after a stated silence, and a periodic login, a held WebSocket, a cron or light CPU defeats it. | 11 |
| **T3** | needs a relay. It runs and cannot be reached: no inbound port, an egress restriction, or browser-only. An outbound tunnel or a held WebSocket makes it reachable. | 1 |
| **DEAD** | a hard wall. Nothing a relay or a keepalive fixes: a quota that exhausts regardless, a trial clock, a paid gate on *creation*, or an account that closes itself. | 12 |
| **blocked** | not a tier. Alive, free, and no new person can reach it. | 2 |

⭐ **The distinction the whole table exists for: a relay defeats a liveness wall and
cannot defeat a quota wall.** A relay fixes sleep, scale-to-zero and the absence of
an inbound port, because it converts an unreachable machine into a reachable one. It
does nothing about 120 core-hours a month, a 24-hour cap, a trial clock or a
creation-time PRO gate, because those end the machine rather than hide it. That one
sentence is why a relay is the right answer for orchestration and the wrong answer
for serving, and it is the premise [`../relay-egress.md`](../relay-egress.md) uses without
stating.

The five counts sum to the 32 rows of the table below.

| tier | the rows |
| --- | --- |
| T1 | Google Cloud Free Tier, Cloudflare Durable Objects, Cloudflare Workers, tilde.green, tilde.club, tilde.guru |
| T2 | Oracle Cloud Always Free, Oracle E2.1.Micro, ctrl-c.club, SDF, hashbang, serv00, Render, Azure App Service F1, Supabase, Hugging Face ZeroGPU, Google Cloud Shell |
| T3 | tilde.town |
| DEAD | Railway's anonymous VM, Killercoda, Replit, Render Postgres, Neon, PythonAnywhere, Hugging Face CPU Basic, Fly.io, AWS Free Tier, Azure Free Account, Play with Docker, Lightning AI |
| blocked | Koyeb, Northflank |

⚠ **Two rows are alive and free and no new person can reach them.** Koyeb and
Northflank both fail on identity, and both fail on a card with a published hold:
Koyeb takes a USD 29 pre-authorisation and a prorated plan charge, and Northflank
requires a payment method "regardless of plan selection" while its own pricing page
carries a "No card needed" badge. They are in the comparison table and in none of the
four tiers, because a tier describes the clock that ends a machine and these never
start. Northflank is the sharper of the two, because it is the only row here that
states "Always on, no sleeping" and it still asks for a card before the first
service.

⚠ **The tier is a judgement about the wall, and the record decides it.** `serv00` is
T2, not T3: its terms of service delete an account after 90 days without a DevilWEB
or SSH login, so it has a clock. `tilde.town` is the only T3 row left, because it is
the only one that runs and opens no port. `Neon` is DEAD here although its record
says `qualifies-with-caveat`, and the two do not conflict: the record answers whether
the free tier is usable at all, and this table answers whether it survives a week of
silence at 24/7, which 100 CU-hours does not.

⚠ **Rows outside the tier table, with the record's verdict.**
GitHub Codespaces is `qualifies`: 120
core-hours a month on a GitHub account with no card, which is a monthly quota and
would be T2. GitHub Actions is `qualifies-with-caveat`, with free and unlimited
standard runners on a public repository. Modal is `fails-identity`: USD 30 of compute
a month and "you must have a payment method on file in order to use Modal".
Blinkenshell is `fails-identity`: a mobile number and two human vouches for 100 MB.
ModelScope Studio is `fails-identity`: a Chinese phone number on the `.cn` site.
alwaysdata is `fails-quota`: its free plan forbids running services. Hugging Face Dev
Mode is `paid-only`, and Cloudflare Containers is `paid-only`. The browser emulators
and the inference endpoints are not compute rows and belong to their own topics.

Sorted by how long a machine survives with no attention. `Clock` is the mechanism
that ends it.

| Provider | Shape | Clock | Outbound | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Google Cloud Free Tier | 1 e2-micro, 1 GB, 30 GB disk | none; the monthly hour allowance is the only cap | 1 GB a month | card | qualifies-with-caveat |
| Oracle Cloud Always Free | 2 OCPU, 12 GB, 200 GB block | 7-day idle reclaim at p95 under 20% CPU, network, memory; plus a 30-day account-idle rule | 10 TB a month | card | qualifies-with-caveat |
| Cloudflare Durable Objects | 128 MB, single-threaded, SQLite | none while connected | through the edge | email | qualifies-with-caveat |
| Cloudflare Workers | 128 MB isolate | none; 10 ms CPU per request | through the edge | email | qualifies-with-caveat |
| tilde.green | shared Ubuntu, 1 GB soft and 1.5 GB hard | none; the host states idle accounts are welcome | not published | email | qualifies-with-caveat |
| tilde.club | shared Unix, 3 GB hard | none found | not published | email | qualifies-with-caveat |
| ctrl-c.club | shared Linux, 1 GB soft; signups closed, waitlist only | archived after 5 years without a login | not published | email | qualifies-with-caveat |
| SDF Public Access UNIX | shared host, 20 MB x4 | expires after 2 years without a UNIX login | not published | email | qualifies-with-caveat |
| hashbang | LXC, 512 MB, 50% CPU | sessions terminated after 30 days without a login unless `~/.keep-account` exists | not published | email | qualifies-with-caveat |
| serv00 | shared FreeBSD, 3 GB | deleted after 90 days without a DevilWEB or SSH login | not published | email | qualifies-with-caveat |
| tilde.town | shared Debian | no expiry; no inbound port at all | none opened | email | qualifies-with-caveat |
| tilde.guru | shared FreeBSD | none documented; a human gate at signup | not published | email | qualifies-with-caveat |
| Render | 512 MB, ephemeral disk | spins down after 15 minutes without traffic | 5 GB a month | email | qualifies-with-caveat |
| Koyeb | 0.1 vCPU, 512 MB | scales to zero after 1 hour without traffic | 100 GB a month | card | fails-identity |
| Azure App Service F1 | 1 GB, 60 CPU-minutes a day | 20-minute idle timeout | not published | card | qualifies-with-caveat |
| Supabase | 500 MB database plus Edge Functions | paused after 1 week without a query | 5 GB a month | email | qualifies-with-caveat |
| Oracle E2.1.Micro | 1/8 OCPU, 1 GB, up to 50 Mbps | same 7-day reclaim, CPU and network only | 10 TB a month | card | qualifies-with-caveat |
| Hugging Face ZeroGPU | half an RTX PRO 6000, 5 min of GPU a day | sleeps after 48 hours without a visitor | not published | email | qualifies-with-caveat |
| Google Cloud Shell | ephemeral VM, 5 GB home | 40 minutes non-interactive, 12 hours maximum, 50 hours a week | not published | email | qualifies-with-caveat |
| Railway anonymous VM | 2 vCPU, 2 GB | 24 hours to claim, then deleted | not published | anonymous | qualifies-with-caveat |
| Killercoda | browser lab | 1 hour, then deleted | not published | email | trial-only |
| Replit | browser IDE | preview link dies after 30 days | not published | email | trial-only |
| Render Postgres | free database | expires 30 days after creation | not published | email | trial-only |
| Neon | 100 CU-hours a month per project | the allowance, about 4 days at 24/7 | not published | email | qualifies-with-caveat |
| pythonanywhere | 100 CPU-seconds a day | `max_always_on_tasks = 0` | not published | email | fails-quota |
| Hugging Face CPU Basic | 2 vCPU, 16 GB | create-time plan gate | not published | card | paid-only |
| Fly.io | cheapest is USD 2.19 a month | no free tier exists; a 2-hour or 7-day trial instead | USD 0.02 per GB | card | trial-only |
| AWS Free Tier | credits for 6 months | account closes at 6 months | metered | email | trial-only |
| Azure Free Account | 750 hours for 12 months | the 12-month clock | metered | card | trial-only |
| Play with Docker | withdrawn | unavailable from 2026-03-01 | not applicable | anonymous | dead |
| Lightning AI | 1 CPU Studio, disk persisted | access revoked 2026-10-16; a restart was required every 4 hours | not published | email | dead |
| Northflank | 0.5 vCPU, 1 GB, USD 20 a month of resources | none; the vendor states "Always on, no sleeping" | not published | card | fails-identity |

## Google Cloud Free Tier

One non-preemptible e2-micro a month in us-west1, us-central1 or us-east1, with
30 GB-months of standard persistent disk and 1 GB of outbound transfer from North
America (`documented`, `cloud.google.com/free/docs/free-cloud-features`, read
2026-10-22). The allowance is by time rather than by instance, so exactly one
instance fits a month and a second would bill.

There is no idle reclaim: Compute Engine's suspend and resume are user-initiated
and never triggered by idleness. That makes it the cleanest always-on row in this
document. The e2-micro is a shared-core shape, two vCPUs bursting at about 12.5
per cent each, so it is a relay or a scheduler and not a compute box. One gigabyte
of egress a month is 0.2 per cent of one day's serving at 500 GB.

⚠ The card at signup is not charged. The published authorisation is USD 0.00, which
a bank may show as pending for 1 to 14 business days. No Google billing page states a
USD 1.00 upper bound. A debit card is accepted with a Visa or Mastercard logo, but a debit
card that requires two-factor authentication is refused, and prepaid cards are
refused.

Evidence: `cloud.google.com/free/docs/free-cloud-features` (read 2026-10-22), the
Compute Engine row and the three quoted sentences. Verdict: the most reliable free
machine here with an egress allowance too small to use for serving.

## Lightning AI, closed on 2026-10-16

The offer was one Studio free at 24/7 with no credit card and no commitment, a
restart required every 4 hours on a free Studio, and up to 80 free GPU hours
against a card table from a T4 at USD 0.55 an hour to an H200 at USD 4.50
(`documented`, `lightning.ai/pricing`, read 2026-10-22). The Studio filesystem
persisted across the restart.

The platform is closed to every user. `lightning.ai/security-incident` states
that the vendor revoked all user access on 2026-10-16 at 01:00 UTC and that the
platform stays inaccessible to all users, and it names Studio, Deployments,
Pipelines and Drive as the affected services (`documented`, read 2026-10-22).
GPU cluster rental and the managed Kubernetes and SLURM services are outside the
incident.

`status.lightning.ai` carried the banner "Service is down to address a security
incident", with the last update at 2026-10-19 12:49 UTC, and the incident was
still open on 2026-10-22 (`documented`).

⚠ The pricing page was not updated. It still advertises "Run 1 Studio free 24/7"
at this read, so the page that sells the product contradicts the page that
reports the incident. The incident page wins because it is newer and it names the
closed service.

⛔ No Studio can be created. What the class loses is a VM of its own, always on,
with a persistent disk, on an email address alone. The always-on rows that remain
above are Oracle Cloud Always Free and Google's e2-micro, and both want a card at
signup. The pubnix rows survive with no card and they are shared shells.

Evidence: `lightning.ai/security-incident` and `status.lightning.ai` (both read
2026-10-22), against `lightning.ai/pricing` of the same date. Verdict: dead. The
offer was real until 2026-10-16, which is why the record keeps it.

## Oracle Cloud Always Free

All tenancies get the first 1,500 OCPU-hours and 9,000 GB-hours a month on
VM.Standard.A1.Flex, which Oracle states is equivalent to 2 OCPUs and 12 GB of
memory, plus up to two VM.Standard.E2.1.Micro instances and 200 GB of block volume
(`documented`, the Always Free resources page at `docs.oracle.com`, read
2026-10-22).

⛔ The allowance is a time-denominated quota, not a size cap. The arithmetic decides it: 2 OCPUs run 730 hours is 1,460
OCPU-hours, which fits inside 1,500 with 40 to spare. A 3-OCPU box at 24/7 is
2,190 OCPU-hours and does not fit at all. A reader who believes the ceiling is
"2 OCPU" will build a three-core box and meet a bill.

The reclaim rule is the risk. Oracle deems an instance idle when, over a 7-day
period, the 95th-percentile CPU is under 20 per cent, network is under 20 per
cent, and on A1 shapes memory is under 20 per cent. A workload that sleeps for
five days and bursts for two is still at risk, because the test is a percentile
over the window and not a total. A second clock sits beside it, quoted from the
Free Tier FAQ on 2026-10-24: "Accounts left idle for 30 days or more may be deemed
abandoned and become eligible for suspension or termination."

The page also contradicts itself on disk: one paragraph states a 47 GB minimum
boot volume and another states 50 GB. The record carries both and treats 50 GB as
the operative figure because it appears in the allocation example.

⚠ The card at signup is charged USD 1.00 as an authorisation, reversed immediately
on Oracle's side while the bank decides how long the release takes. The USD 100
figure belongs to the upgrade to Pay As You Go, not to signup. Debit is accepted
only if it functions like a credit card, so PIN debit, prepaid, virtual and
single-use cards are refused.

Evidence: the Always Free resources page (read 2026-10-22), for the allowance, the
E2.1.Micro row, the reclaim test and the 200 GB volume. `oracle.com/cloud/free/`
returned HTTP 200 from the probe host, so a reported "whole domain 403" was that host's egress. Verdict: the only free tier here that is a real VM
with a public address and 10 TB of egress, and the only one that will take the
machine back if it looks idle.

## Cloudflare Durable Objects and Workers

A Durable Object is single-threaded with 128 MB of memory, is stateful, is
WebSocket-capable, and stays active while a request, a response stream, a
WebSocket or pending I/O is in flight. Its free allowance is **13,000 GB-seconds
of duration a day**, which is a Durable Object allowance and not a Workers
duration allowance (`documented`,
`developers.cloudflare.com/durable-objects/platform/pricing/`, read 2026-10-22).
The page also states that an idle object eligible for hibernation is not billed.

Workers themselves have no duration limit while the client is connected, 10 ms of
CPU per request, 128 MB of memory and 50 subrequests on the free plan, and 100,000
requests a day (`documented`,
`developers.cloudflare.com/workers/platform/limits/`, read 2026-10-22). A cron
trigger or a queue consumer is capped at 15 minutes.

⚠ The two allowances are on different pages and belong to different products. The
Workers limits page does not carry the 13,000 GB-seconds figure; the Durable Objects
pricing page does.

A Durable Object is the closest thing here to a free always-on stateful process:
it holds a WebSocket open indefinitely and is billed only while active. It cannot
run a binary, cannot open a listening socket of its own, and has 128 MB.

Evidence: the Durable Objects pricing page for the 13,000 GB-s duration allowance
and the Workers limits page for the request count and the CPU wall (both read
2026-10-22). Verdict: the best free relay and coordination substrate, and not a
machine.

## The pubnix layer

Seven shared shells answer SSH and cost nothing: tilde.green, tilde.club,
ctrl-c.club, SDF, hashbang, serv00 and tilde.town. Their prices are irrelevant and
their clocks are not, because each one has a different way of ending an account.
One of the seven is not open to a new reader: ctrl-c.club has closed signups and
runs a waitlist. Two more rows appear below and are not among the seven, because
neither is established as a free shell: tilde.zone serves a Mastodon instance, and
Blinkenshell wants a phone number and two human vouches.

tilde.green is the only one that states a positive promise: the host writes
that idle accounts are welcome. The quota figures read on 2026-10-06 are
50 processes, nice 10, a 40-login limit and 1 GB soft and 1.5 GB hard storage;
`tilde.green/tos` returned 404 when re-requested on 2026-10-22, so those figures
carry that date. It answered SSH with OpenSSH 10.6p1 (`measured`, 2026-10-22,
saved as `sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`).

tilde.club gives 1 GB soft and 3 GB hard, the largest pubnix quota here, and no
idle policy was found on any first-party page. Its FAQ was read on 2026-10-24
and states "Soft Limit: 1 GB", "Hard Limit: 3 GB" and "Grace Period: 1 week". It
answered SSH with OpenSSH 10.0 (`measured`, 2026-10-22, saved as
`sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`). "No idle policy"
is an absence of a sentence and the record says so. The signup form asks for a
username, an email address, a sentence on the applicant's interests and an SSH public key,
and a person reads the sentence.

ctrl-c.club archives an account after 5 years without a login, which is the
gentlest clock in the set, and gives 1 GB as a soft limit. It answered SSH
(`measured`, 2026-10-22, saved as
`sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`).

⛔ **Signups are closed and waitlist only.** `signup.ctrl-c.club/` states
"Signups are closed for now! ... We're pausing signups to work on some scaling
issues. You can still submit a signup to get on a waitlist." A new reader cannot
act on this row; only an existing member can reach the host today (`documented`,
read 2026-10-06, not fetched again). A reader acting on the table without this note
would try to sign up for a closed service.

SDF expires a validated account after 2 years without a UNIX login, and the clock
is `lastlog`, so a background job does not keep it alive. It gives 20 MB on each
of four filesystems, and the 500-file cap is not on either page
read on 2026-10-22. A prevalidated account is purged at about 600 days whether it
is used or not. It answered SSH with OpenSSH 10.4 (`measured`, 2026-10-22,
saved as `sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`).

hashbang terminates sessions for any user with no SSH login in 30 days, unless
`~/.keep-account` exists. That single file is the opt-out and it is the cheapest
keepalive in this document. The per-user limits are 512 MB of memory, a 50 per cent
CPU quota and a soft cap of 150 processes. It accepted TCP without sending a banner
(`measured`, 2026-10-22, saved as
`sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`).

serv00 gives 3 GB on FreeBSD, as the vendor's decimal GB. It states no idle kill in
the sense this document uses the word, but its terms of service do delete the
account: "A user account that has not been properly logged in by the DevilWEB or SSH
panel for a period of 90 days will be automatically removed from the system without
the possibility of recovering the data collected on that account." That makes it a
T2 row with a 90-day clock. It answered SSH with OpenSSH 9.9 (`measured`, 2026-10-22,
saved as `sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`).
Registration is free and reviewed by hand, in a few hours up to 72 hours, on an
email address with no card and no phone.

tilde.town opens no ports for users at all: the vendor states that services and
cron jobs are local-only (`tilde.town/wiki/faq.html`, read 2026-10-22). It
answered SSH (`measured`, 2026-10-22, saved as
`sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`). The machine is fine and the network is the
wall.

tilde.zone answered SSH with OpenSSH 10.0p2 and that is all that is established.
Fetched first-party on 2026-10-22, `tilde.zone/` redirects to `/explore` and serves
a Mastodon instance: a trending feed, with no shell, no signup and no operator page
in it. A first-party page naming an operator and a signup path would recover it, and none was
found. The record is `unverified` rather than `qualifies-with-caveat`, because a
banner proves a host and not a free shell. It is not one of the seven.

tilde.guru is curated by a person and its wiki join page returned 404. It accepted a TCP connection but sent no banner within 6 seconds
(`measured`, 2026-10-22, saved as `sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`).

Blinkenshell is the row that proves the port assumption is a research defect:
it answers on 2222, not 22. From the probe host both ports timed out, at 16 seconds
each, on both saved runs (`measured`), so reachability is unverified
rather than established. Its signup is five steps and step five is a mobile phone
number for an SMS code, after an email check, a 20-question quiz, an IRC NickServ
registration and two existing users who vouch for the applicant. The record is
`fails-identity`: 100 MB of disk for a phone number and two human vouches.

⚠ A shared shell is not a VM. Tens of thousands of users share one kernel, an
admin can kill a process under load, and the quotas are megabytes.

## The services that sleep

Render spins a free web service down after 15 minutes without inbound traffic,
counting both HTTP requests and WebSocket messages from existing connections, and
gives 750 instance-hours a month per workspace (`documented`, `render.com/docs/free`,
read 2026-10-24). One always-on service is about 720 hours, so exactly one fits. The
filesystem is ephemeral and changes are lost on spin-down. Hobby workspaces also
carry 5 GB of outbound bandwidth a month, then USD 0.15 per GB; without a payment
method Render suspends all Free services for the rest of the month instead of
billing. A wake after the spin-down takes about one minute, and Render states that
it "might restart a Free web service at any time".

Koyeb publishes one free web Service with 512 MB, 0.1 vCPU and 2 GB of SSD, and it
scales to zero after 1 hour without traffic with the interval not configurable
(`documented`, `koyeb.com/docs/faqs/pricing` and
`koyeb.com/docs/reference/instances`, read 2026-10-24). Volumes are disabled on the
free instance, so it cannot hold state. It also gives 100 GB of outbound a month
free, then USD 0.04 per GB.

⛔ **Koyeb is not reachable without a card, and the card is not free.** The pricing
FAQ states "We require a credit card to prevent fraud and abuse. We verify the card
you enter by placing a $29 pre-authorization hold and immediately canceling it", and
"Right after we place the $29 pre-authorization hold to verify your card, we also
charge you the pro-rated amount for the plan you select". The record's verdict is
`fails-identity`.

Supabase gives a real always-on process through Edge Functions on Deno with a
public URL, and pauses the project after a week without activity. A weekly query
is enough to keep it awake. That makes it the cheapest always-on process runtime
with a public address in this document. Its record rests on the vendor pricing page
read on 2026-10-22 and is `reported`, not `documented`: the free-project figures are
a page claim and no probe sits behind them.

Azure App Service F1 states 60 CPU-minutes a day, 1 GB of RAM and 1.00 GB of
storage, and it times an app out after 20 minutes without a direct request
(`documented`, `learn.microsoft.com/en-us/azure/app-service/webjobs-execution`,
read 2026-10-22). The page adds the part that matters for a keepalive: only a
direct request resets the timer, and a portal visit or a Kudu request does not.

⚠ The Azure pricing page does not state this timeout. Microsoft states it first-party on the
WebJobs execution page, which is the stronger source.

## What did not work

- **Hugging Face CPU Basic**: the hardware lists as FREE at 2 vCPU and 16 GB, and
  creating a Gradio or Docker Space that uses it needs PRO. A create-time plan gate
  is a wall no keepalive fixes.
- **Fly.io**: no free tier. The page states it in one sentence. What it has instead
  is a trial of 2 hours of Machine runtime or 7 days, whichever comes first, and the
  trial machines stop themselves after 5 minutes.
- **Neon**: 100 CU-hours a month per project. A database that never sleeps burns 730
  hours and exhausts the allowance in about four days. The record is
  `qualifies-with-caveat`, because the plan is permanent and the quota resets; it is
  the always-on use that fails, not the tier.
- **pythonanywhere**: `max_always_on_tasks = 0`. The feature is absent.
- **Render Postgres**: expires 30 days after creation.
- **Replit**: a 30-day preview link.
- **Killercoda**: 1 hour per scenario.
- **AWS Free Tier**: credits for 6 months, then the account closes. There is no
  always-free EC2 shape for a new account. No card is required to start for most new
  customers.
- **Azure Free Account**: 750 hours for 12 months, then billed.
- **Play with Docker**: withdrawn.
- **Hugging Face ZeroGPU**: 5 minutes of GPU a day and a 48-hour sleep. A demo
  budget. The record is `qualifies-with-caveat`, not `trial-only`: the allowance
  resets daily, so it recurs.
- **alwaysdata**: 1 GB and SSH for EUR 0, and the free plan's own footnote forbids
  running services. The record is `fails-quota`.
- **Browser Linux emulators** (self-hosted): the machine is the reader's own tab.

## Chaining

Oracle's A1 VM plus a pubnix shell plus Cloudflare's Durable Object covers three
different jobs cheaply. The VM is the always-on address and the egress. The pubnix
shell is a shell that survives without costing anything and without exposing a
port. The Durable Object is the coordination point that holds a WebSocket for
nothing. What none of them gives is a large disk, and that is the `storage` topic's
problem rather than this one's.

⚠ The chain has one ordering rule: put anything that must not be reclaimed on the
e2-micro, which has no idle test, rather than on Oracle, which does.
