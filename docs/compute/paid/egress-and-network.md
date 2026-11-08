# What traffic out costs, and who publishes it

Egress is the term that decides whether a compute recommendation is affordable, and
it is the term vendors publish least. The serving target assumed here is 500 GB a day
to 1 TiB a day. At USD 0.02 a gigabyte that is USD 300 to USD 600 a month; at USD 0.09 it is USD 1,350
to USD 2,700. The compute in every case is USD 5 to USD 50. Traffic is the bill and
the machine is a rounding error.

The answer: five providers in this topic publish an egress term that a reader can
plan against, and two of them are worth using. boat does not bill egress at all and
gives every sandbox a public IPv6 address. Lizard includes 2 TB per account over a
rolling 30 days with no per-GB charge, which is 67 GB a day. Hetzner includes 20 TB
a month with a real overage rate and a 100 MB billing block. Oracle gives 10 TB a
month free on Always Free. Cloudflare gives 1 TB a month in North America and
Europe at USD 0.025 a gigabyte. Everything else in this topic states nothing, and
that absence is the finding.

## The arithmetic, before the table

A rate and a quota are not comparable until both are per day. 1 TiB a day is
12.1 MiB a second sustained, and 20 TB a month is 666.7 GB a day.

| Term | Per day | Share of 1 TiB a day | Monthly bill at 1 TiB a day |
| --- | --- | --- | --- |
| no egress charge | no ceiling | 100% | USD 0 of traffic |
| 2 TB per rolling 30 days | 66.7 GB | 6.5% | the overage is not priced |
| 20 TB a month included | 666.7 GB | 65.1% | EUR 1.00 per TB over the allowance |
| 10 TB a month included | 333.3 GB | 32.6% | overage only, rate not published |
| 1 TB a month in NA and EU, then USD 0.025/GB | 33.3 GB | 3.3% | USD 742 |
| 1 TiB a month included, then USD 0.04/GiB | 34.1 GB | 3.3% | USD 1,188 |
| 100 GB a month included, then USD 0.04/GB | 3.3 GB | 0.3% | USD 1,225 |

The monthly column is the overage only. One tebibyte a day for 30 days is 30 TiB,
so a 1 TiB allowance leaves 29 TiB to bill at USD 0.04 a gibibyte, which is
USD 1,188. The arithmetic is written out because the unit switch between TB and TiB
is where this kind of table goes wrong.

## The comparison

Only rows whose page states a term. `Then` is the marginal price, which is what a
serving workload actually pays.

| Provider | Included | Then | Region-sensitive | Read |
| --- | --- | --- | --- | --- |
| boat | no egress charge | USD 0 | no | `docs.boat.dev/pricing` (2026-10-22) |
| Lizard | 2 TB per account per 30 days | no per-GB charge | no | `lizard.build/docs/platform/limits/` (2026-10-22) |
| Hetzner Cloud | 20 TB a month | EUR 1.00 per extra TB, 100 MB blocks | no | `hetzner.com/cloud/cost-optimized/` (2026-10-22) |
| Oracle Cloud Always Free | 10 TB a month | metered | no | the Always Free resources page (2026-10-22) |
| Cloudflare Containers | 1 TB a month in NA and EU | USD 0.025 per GB | yes | `developers.cloudflare.com/containers/platform/pricing/` (2026-10-22) |
| Modal | 1 TiB a cycle on Starter | USD 0.04 per GiB | no | `modal.com/docs/guide/network-egress-billing` (2026-10-22) |
| Railway | none on Free | USD 0.05 per GB | no | `railway.com/pricing` (2026-10-22) |
| Freestyle | 50 GB on Free, 500 GB paid | USD 0.02 per GB | no | `freestyle.sh/pricing` (2026-10-22) |
| Koyeb | 100 GB a month | USD 0.04 per GB | no | `koyeb.com/docs/faqs/pricing` (2026-10-22) |
| Steel | none | USD 10 per GB of proxy | no | `steel.dev/pricing` (2026-10-22) |
| Browser Use | none | USD 5 per GB of proxy | no | `browser-use.com/pricing` (2026-10-22) |
| Fly.io | none | USD 0.02 per GB in NA and EU, USD 0.12 in Africa and India | yes | `fly.io/docs/about/pricing/` (2026-10-22) |
| e2b | not published | - | - | `e2b.dev/pricing` |
| Agent 37 | not published | - | - | `agent37.com/pricing` |
| zipbox | not published | - | - | `zipbox.ai/pricing` |
| Daytona | not published | - | - | `daytona.io/pricing` |
| Upstash Box | not published | - | - | `upstash.com/pricing/box` |
| Vercel Sandbox | 20 GB a month on Hobby | USD 0.15 per GB on Enterprise | yes | `vercel.com/docs/sandbox/pricing` (2026-10-22) |

## boat

boat does not bill egress, and every sandbox gets a public IPv6 address and
outbound IPv4 plus a public HTTPS URL per hosted port (`documented`,
`docs.boat.dev/pricing` and `docs.boat.dev/hosting`, read 2026-10-22). That
combination is unique in this topic: no other row both refuses to meter traffic
and publishes a port.

The catch is the URL, not the traffic. An address can change when a sandbox
resumes, so a stable public name requires the hosted port rather than the raw
address. The 14-day disk clock is the other catch and it is in the sandbox
document.

Evidence: `docs.boat.dev/pricing` and `docs.boat.dev/hosting` (read 2026-10-22).
Verdict: the only unbilled egress in the class, and it arrives with a port.

## Lizard

Sandbox egress has no separate per-GB charge, and the included allowance is 2 TB
per account over a rolling 30 days (`documented`,
`lizard.build/docs/platform/limits/`, read 2026-10-22). Two terabytes over 30 days is
66.7 GB a day, which is 6.5 per cent of the serving target assumed here.

⚠ A rolling window is not a calendar month. A reader who spends 2 TB in the first
week waits three weeks for the window to move, and there is no published overage
rate. The page says to contact Lizard before running more.

Evidence: `lizard.build/docs/platform/limits/` (read 2026-10-22). Verdict: the
largest included allowance in the sandbox class and no way to buy more from a
script.

## Hetzner Cloud

Only outgoing traffic is billed and 20 TB a month is included. Overage is billed
in 100 MB blocks rounded up (`documented`, `docs.hetzner.com/cloud/billing/faq`,
read 2026-10-22). Twenty terabytes a month is 666.7 GB a day, which is 65.1 per cent
of a tebibyte a day and most of the serving target assumed here.

⚠ The FAQ states that the notifications at 75 and 100 per cent of the allowance
do not cap or stop traffic and that anything beyond is billed as usual. A reader
who treats the notification as a brake meets the bill.

This is the best traffic term on a box that costs USD 6.49 a month. Overage at
EU-Central locations is EUR 1.00 per additional terabyte, published on the product
page as "For each additional TB at EU-Central locations we charge EUR 1.00".

⚠ Read the unit, not the label. The product page's own sentence prints that amount
followed by "per hour", which cannot be right against the same FAQ's 100 MB block
billing and against a 20 TB allowance. The amount is EUR 1.00 and the unit is the
terabyte; the record says the page's string is inconsistent rather than picking
one reading.

Evidence: the billing FAQ (read 2026-10-22). Verdict: the best traffic term on a
cheap VPS and an overage rate that needs one more read.

## Oracle Cloud Always Free

10 TB a month of outbound data transfer is included on Always Free, and E2.1.Micro
instances are capped at 50 Mbps on the internet (`documented`, the Always Free
resources page, read 2026-10-22). Ten terabytes a month is 333.3 GB a day, which is
32.6 per cent of the serving target, for nothing, on a machine that costs nothing.

⚠ The 50 Mbps cap applies to Micro instances. At line rate it is 540 GB a day, so
against a 333 GB-a-day allowance it is not the binding limit either.

Evidence: the Always Free resources page (read 2026-10-22). Verdict: the best free
traffic allowance in this repository.

## Cloudflare Containers

Egress is USD 0.025 per GB in North America and Europe with 1 TB included a month,
USD 0.05 in Oceania, Korea and Taiwan with 500 GB, and USD 0.04 everywhere else
with 500 GB (`documented`,
`developers.cloudflare.com/containers/platform/pricing/`, read 2026-10-22).

The regional split is the thing to notice: the same product costs twice as much
per gigabyte depending on where the container runs, and the included allowance
halves. The region is a price decision and not a latency one.

⚠ 1 TB a month is 33.3 GB a day, which is 3.3 per cent of the serving target. This
is a free allowance for a small service and not for a serving workload.

Evidence: the Containers pricing page (read 2026-10-22). Verdict: the cheapest
first-party egress rate here and an allowance a serving workload exhausts in a day.

## Modal

⛔ Modal began charging for network egress on 2026-10-01, three weeks before the read
that recorded it (`documented`, `modal.com/docs/guide/network-egress-billing`, read
2026-10-22). Starter includes 1 TiB a billing cycle and overage is USD 0.04 per
GiB. Outbound traffic from a task counts, as does private traffic to other Modal
containers and uploads through Cloud Bucket Mounts. Volume reads and writes do not.

Records written before that date carry no egress term for Modal. A reader working
from one would price a Modal workload at zero and be wrong.

⚠ 1 TiB a month is 34.1 GB a day. At a tebibyte a day the overage is USD 1,188 a
month, which is twice the largest compute bill in this topic.

Evidence: the egress billing page (read 2026-10-22). Verdict: a new charge that
changes Modal's place in the ranking for any workload that serves.

## The rows that publish nothing

Five of the eighteen rows in the comparison publish no egress term at all: E2B,
Agent 37, zipbox, Daytona and Upstash Box. Each of those five pages was read on
2026-10-22 and none of them carries an egress line. That is not an oversight in
this document. It is the state of the market.

⛔ A compute recommendation without an egress term is incomplete. A reader who
chooses zipbox because it has 80 GB of disk learns the traffic price after the
first terabyte, and by then the workload depends on it.

## What did not work

- **Cloudflare's free egress**: the Workers free plan serves responses without a
  per-byte charge and it cannot proxy a large file, because 128 MB of memory and a
  10 ms CPU wall stop it. The free egress and the free compute are on different
  products.
- **Oracle's 10 TB on a trial account**: the allowance is for Always Free
  tenancies, and a trial that expires takes it with it.
- **A consumer-connection proxy as an egress lane**: it is priced per gigabyte at USD 5 to
  USD 10 for browser hosts, which is 100 to 200 times the cheapest cloud rate. It
  is a crawl input and not a serving path.
- **Vast.ai as a serving host**: interruptible instances are reclaimable. A host
  that can vanish is not an origin.

## Chaining

Hetzner for the origin and Cloudflare in front is the pairing the published conditions cover:
20 TB a month from the box, and the CDN absorbs the cacheable share before the
box sees it. boat is the answer when the origin must be a sandbox, because it is
the only sandbox that does not meter. Neither removes the need to measure what the
cache misses, and that is the number this document cannot supply.
