# The paid lane: what money buys that a free tier cannot

The free lane is bounded by a clock the vendor sets. The paid lane is bounded by a
duty cycle the reader chooses, and that is a different constraint with a different
decision behind it. A free tier fails because the session ended. A paid tier fails because the
meter keeps running while nothing is computing, and the pricing page puts that
mechanism in a footnote.

This page states the argument: what money buys, what it costs at three hold times, and
where the floor is.

## What money buys

Three things, and only one of them is capacity.

**It buys a clock the reader controls.** No 15-minute idle reap, no 4-hour restart, no
seven-day reclaim test. That is the single largest difference between a free tier and
a paid one, and it is worth more than the capacity: a machine that dies mid-task is
worse than a smaller machine that does not.

**It buys a network that can be sized.** A free tier's outbound allowance is shaped for
somebody else's economics. Oracle gives 10 TB a month, Google gives 1 GB, and most of
the class publishes nothing. A paid instance's bandwidth is a specification.

**It buys an operator with an invoice.** Not a guarantee. But a company with a monthly
bill has a reason to answer, and a volunteer with a server does not.

It does not buy capacity cheaply. ⛔ **The floor is a rented box at USD 3.75 a month, not
the USD 6.49 of the mainstream set**: GreenCloudVPS sells 8 GiB, 4 vCPU and 60 GB for
USD 45.00 a year, and AlphaVPS sells 6 GiB for USD 4.75 a month with the discount locked at
renewal. That figure is annual prepay, and the monthly-billed floor is higher: HostBrr's
2 GiB is USD 2.15 a month with no commitment, and the largest monthly-billed shape under
USD 5 is C-Servers' 6 GiB ExtraVPS at USD 4.29. The correction is recorded in
[`history/2026-10-24T021500Z/under-five-floor-corrected.md`](../../../history/2026-10-24T021500Z/under-five-floor-corrected.md).

## The three hold times, which are the whole pricing question

⛔ **A price without a duty cycle is not a price.** A sandbox bills only while it runs
and a VPS bills whether it runs or not, so one column misranks one of the two. Every
figure in this topic is a triple: a shape, a horizon, and what the number includes.

| hold | hours a month | what it models |
| --- | --- | --- |
| 1 h/day | 30 | an interactive session, a notebook, a scratch run |
| 10 h/day | 300 | a working day, the column called `agent` |
| 24/7 | 730 | a daemon, an endpoint, or anything that must answer at 03:00 |

The difference is not a rounding error. Modal's 2 vCPU / 4 GiB shape is USD 0.2380 an
hour, which is USD 71.39 at 10 hours a day and USD 173.71 at 24/7 for the same rate.
A reader who compares a sandbox's monthly figure to a VPS's monthly figure has compared
two different products.

⚠ **370 of the 1,411 records carry a shape with at least one field set**, and 25 of those
carry the explicit 2 vCPU / 4 GiB shape this topic prices. Everything outside that is a
recorded offer with no number attached, and it is excluded from the tables rather than
ranked. The count is a set over `extras.shape`, so a reader can reproduce it from the
records.

## The cheapest box that stays up

Monthly, because these are the rows that bill whether or not anything runs. The full ranking,
with thirteen rows, the first payment and the renewal caveat, is
[`under-five.md`](under-five.md); this table keeps only the rows that decide the answer.

| Provider | Shape | Held 24/7 | What binds |
| --- | --- | --- | --- |
| GreenCloudVPS | BudgetKVM, 4 vCPU / 8 GiB / 60 GB, USD 45.00 a year | USD 3.75 | clearance stock, no refund, renewal unpublished |
| AlphaVPS | C6G, 3 vCPU / 6 GiB / 55 GB, annual | USD 4.75 | annual commitment; monthly is USD 5.59 |
| OVHcloud | VPS-1 2027, 2 vCPU / 4 GiB / 40 GB, 12 months upfront | USD 4.54 | 500 Mbps port; monthly is USD 5.03 |
| HostBrr | Value 2GB, 1 vCPU / 2 GiB / 25 GB, monthly | USD 2.15 | 1 core; 2.5 TB at 10 Gbps |
| Hetzner Cloud | CX23, 2 vCPU / 4 GiB / 40 GB | EUR 5.99 (USD 6.70) | marked "not available"; above the line |
| Contabo | Cloud VPS 4, 4 vCPU / 8 GiB / 100 GB | USD 6.16 | the beefiest shape near the line, still over it |

⭐ **The cheapest credible always-on box is GreenCloudVPS, not Hetzner.** It returns 8 GiB
for USD 3.75 a month on an annual prepay, which is four times the memory of the CX23 for less
money, and its catch is stock and age rather than price. Hetzner's CX23 is EUR 5.99 and
unavailable on the page read on 2026-10-24, so it no longer decides anything.

⚠ **An annual figure divided by twelve is not a monthly bill.** Six of the thirteen rows in
`under-five.md` are annual prepay, and the first payment is a separate column there. Agent 37
at USD 4.76 is still a defensible 2 vCPU option; a larger shape now costs less.

## The cheapest sandbox per hour

At the 2 vCPU shape. These bill only while running, so the 10-hour column is the one
that models a working day and the 24/7 column is the one that shows why a sandbox is
the wrong product for a daemon.

| Provider | USD at 10 h/day | USD at 24/7 | Free lane |
| --- | --- | --- | --- |
| zipbox | 4.11 | 10.00 | USD 25 after a USD 5 top-up |
| Lizard | 4.86 | 11.83 | a 7-day trial and USD 5 of credits |
| boat | 5.40 | 13.14 | none; USD 20 is credit |
| Upstash Box | 3.29 | 8.00 | 5 CPU hours a month |
| Agent 37 | 2.17 | 4.76 | USD 5 after a card |

⛔ **The two questions have different answers and a reader who quotes one for the other
has made a shape error.** The cheapest credible *agent* box at the 2 vCPU shape is
Agent 37 at USD 2.17 for a 10-hour day. The cheapest box of any size is Scaleway's
STARDUST1-S at 1 vCPU / 1 GiB, USD 0.000683 an hour, which is USD 0.20 a month at 10
hours a day. That is 34 times cheaper and it will not hold a browser: 1 GiB is not an
agent sandbox. Scaleway flags it stock-limited, so it is not guaranteed available.

## What traffic out costs, and who publishes it

⭐ **Egress is the bill this lane hides, and it is usually larger than the compute.**
The serving target assumed here is 500 GB a day to 1 TiB a day.

At the vendor's decimal gigabyte, 500 GB a day for 30 days is 15,000 GB. That is
USD 300 at USD 0.02 per GB and USD 1,350 at USD 0.09 per GB. One tebibyte a day for 30
days is 30 TiB, which is 32,986 GB, so it is USD 660 and USD 2,969.

⛔ **Egress is published for 597 of the 1,411 records.** Another 814 carry a sentence
beginning "not ", of which 194 are the literal placeholder "not published on the source
card". That is a finding rather than a gap: five of the eighteen rows in
`paid/egress-and-network.md` publish no per-GB term at all.

The rows that do publish something useful are few. Oracle includes 10 TB a month with
Always Free, and caps E2.1.Micro instances at 50 Mbps. Koyeb gives 100 GB a month.
Thunder Compute states USD 0.00 a GB. Hetzner includes at least 20 TB a month in the EU
and bills only outbound, in 100 MB blocks rounded up. Contabo publishes "unlimited"
with no rate, which is a discretionary policy rather than a specification.

## The floor, and what is not available

⛔ **The cheapest compute per hour is hardware the reader owns, and it is not an
option.** The analysis assumes no local machine and no purchase, so a bought box is not a
cheaper answer; it is not an answer. Do not price one and do not compare against one.
A rented box with a monthly invoice is a service and is the floor this page prices.

What that floor actually is: USD 3.75 a month, which is USD 45.00 a year, for 8 GiB of RAM,
4 vCPU, 60 GB of disk and 8 TB of transfer. On monthly billing, a 2 vCPU / 4 GB machine with
unmetered EU traffic is OVHcloud's VPS-1 at USD 5.03, and the 20 TB shape is Hetzner's CX23 at
USD 6.70, which its own page marks "not available".

⛔ **That floor is a Linux floor. Windows is a second price line, and the machine
price is the cheaper half of it.** The cheapest machine that can boot it is
**USD 8.11 a month on Layer7's annual cycle**, or **USD 10.14 a month on its monthly
cycle**, for 4 cores, 16 GiB and 80 GB with a Windows Server evaluation image that
expires. Saganetwork is the cheapest row a buyer can start on a monthly term, at
USD 8.23 ex VAT and USD 9.88 paid. Rabisu is the cheapest row with a Windows image
at no surcharge, at USD 10.99 a month or USD 8.79 annual, and none of the three
pages read states that a licence is supplied. The licence itself is a separate
purchase at most
hosts: **USD 509.99 for 16 core licences, or USD 14.17 a month over 36 months**,
against Microsoft's USD 1,176 suggested MSRP. Sixteen cores is a per-server minimum,
so the licence is a fixed line and the machine is the only variable: a licensed
Layer7 is about USD 24.31 a month. The cheapest row where the licence is printed as
a price is Virtarix at USD 27.40, of which USD 16.00 is the licence. Kimsufi KS-3 is
USD 64.00 all-in, with the licence as its own USD 34.00 line on a USD 30.00 box. The
Windows lane is [`windows-vps.md`](windows-vps.md).

## The twenty-one documents

| document | the question it answers |
| --- | --- |
| [`micro.md`](micro.md) | the smallest invoice that returns a root shell, and the largest machine USD 2, 5, 10, 20 and 50 buy |
| [`lowend-vps.md`](lowend-vps.md) | the 114 cheap hosts one tracker lists, and the six ways its numbers are wrong |
| [`storage-vps.md`](storage-vps.md) | the cheapest disk per TB per month, and the largest machine at a price |
| [`sandboxes-container-vm.md`](sandboxes-container-vm.md) | the cheapest sandbox per hour at a named shape |
| [`under-five.md`](under-five.md) | the beefiest always-on machine under USD 5 a month, with the first payment and the renewal caveat |
| [`under-one.md`](under-one.md) | the beefiest machine under USD 1 a month, for a WireGuard node or a health monitor |
| [`niche-non-english.md`](niche-non-english.md) | nine non-English sellers under USD 5, ranked by GiB per USD, with the counterparty test each one fails or passes |
| [`vps-monthly.md`](vps-monthly.md) | the cheapest box that stays up, and what its traffic term is |
| [`cloud-vms.md`](cloud-vms.md) | the free cloud VM tiers, the reclaim clocks, and what traffic out costs |
| [`brokers-and-bare-metal.md`](brokers-and-bare-metal.md) | what a brokered GPU and a whole rented machine cost, and where the price hides |
| [`os-hosts.md`](os-hosts.md) | what a macOS or Windows machine costs, and who gives one away |
| [`windows-vps.md`](windows-vps.md) | the cheapest machine that boots Windows at 16 GiB, 4 vCPU and 50 GB, ranked across sixteen lanes with the licence path in every row, the USD 7 entry plans that miss the RAM floor, and the licence-supplied rows in a second table |
| [`gpu-rental.md`](gpu-rental.md) | the cheapest card, by marketplace, and what preemption costs |
| [`gpu-notebooks.md`](gpu-notebooks.md) | the cheapest GPU hour, by card class |
| [`dev-environments.md`](dev-environments.md) | what a real devbox costs once the free hours are gone |
| [`agent-browser-hosts.md`](agent-browser-hosts.md) | the cheapest browser hour, and what a GB of proxy adds |
| [`spot-interruptible.md`](spot-interruptible.md) | what interruptible capacity costs, how much notice a reclaim gives, and what a checkpoint must survive |
| [`minimum-bill.md`](minimum-bill.md) | what a 30-minute run costs after rounding and plan floors |
| [`egress-and-network.md`](egress-and-network.md) | what traffic out costs, and who publishes it at all |
| [`bursty-workload.md`](bursty-workload.md) | what a run-wait-run workload costs under each model |
| [`ci-adjacent.md`](ci-adjacent.md) | what a CI runner costs per minute, and where that topic owns it |

## What this lane does not establish

⛔ **No bill was paid and no machine was booted.** Every figure here is a published
rate. A published rate is not an invoice, and the gap between them is the rounding
rule, the plan floor and the idle keep-alive that `minimum-bill.md` describes from
pages without once observing one.

⚠ **GPU availability is not recorded anywhere in this lane.** Every card here has a
price. None has a stock position, and a marketplace rate is an offer rather than a
machine available tonight. That distinction is largest at Vast.ai, where the price is set
by supply and is not a stock position.
