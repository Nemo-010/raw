# What a bursty workload costs when the machine is held between calls

A bursty workload runs for seconds or minutes, waits, and runs again. It is the
shape most agent work has, and it is the shape that a monthly price models worst.
Two billing models answer it and they disagree by an order of magnitude: metered
time, which charges only the busy seconds, and a held machine, which charges the
whole month whether the work arrives or not.

The answer: on this shape the cheapest model is a per-second sandbox that stops
between runs, and the second cheapest is active-CPU billing. The worst is a
monthly box, and the gap is large enough that a reader who picks a VPS for a burst
workload has chosen the wrong product rather than a more expensive one.

## The workload, stated so the numbers mean something

Twenty runs a day, thirty minutes each, for thirty days. That is 300 busy hours a
month out of 730, a duty cycle of 41 per cent. At 2 vCPU and 4 GiB.

| Model | Provider | What bills | Month | Effective per busy hour |
| --- | --- | --- | --- | --- |
| per-second, stopped between runs | zipbox Small | 300 h | USD 4.11 | USD 0.0137 |
| per-second, stopped between runs | Lizard Small | 300 h | USD 4.86 | USD 0.0162 |
| per-second, stopped between runs | boat small | 300 h | USD 5.40, or the USD 20 plan floor | USD 0.0180 |
| compute while run, disk while kept | Agent 37 | 300 h plus the disk month | USD 2.17 | USD 0.0060 plus disk |
| active CPU, keep-alive flat price | Upstash Small | the lower of usage and USD 8 | USD 8.00 | USD 0.0267 |
| active CPU at 50 per cent | Vercel Sandbox | active CPU plus memory | USD 63.84 | USD 0.2128 |
| the whole month, held | Hetzner CX23 | 730 h at the cap | USD 6.49 | USD 0.0216 |
| the whole month, held | Contabo VPS 4 | 730 h at the cap | USD 6.60 | USD 0.0220 |

⭐ The finding is in the last two rows as much as the first. A EUR 6.49 VPS held
for the whole month costs USD 0.0216 per busy hour, which beats Vercel by a factor
of ten and loses to zipbox by a factor of 1.6. The burst workload does not make a
VPS absurd; it makes a metered sandbox cheaper by less than a reader expects,
because the sandbox's rate is low and the VPS's month is cheap.

⛔ What makes a VPS the wrong choice is not the price. It is that the VPS cannot
stop, so the 59 per cent of the month in which nothing happens is billed anyway,
and the sandbox can. A reader comparing USD 4.11 to USD 6.49 is comparing a bill
to a bill. A reader comparing USD 0.0137 to USD 0.0216 is comparing two rates and
missing that one of them applies to 300 hours and the other to 730.

## Where the model bites hardest

The lower the duty cycle, the wider the gap. At ten runs a day of ten minutes each,
the busy time is 50 hours a month and the numbers separate.

| Duty cycle | Busy hours | zipbox | Hetzner | Ratio |
| --- | --- | --- | --- | --- |
| 20 runs of 30 min a day | 300 | USD 4.11 | USD 6.49 | 1.6x |
| 10 runs of 10 min a day | 50 | USD 0.69 | USD 6.49 | 9.4x |
| 2 runs of 5 min a day | 5 | USD 0.07 | USD 6.49 | 93x |

⚠ The ratio is the point and the absolute numbers are not. A workload that runs for
five minutes a day should never be on a monthly plan, and one that runs for twenty
hours a day should never be on a metre.

## The two rows where metering is not the answer

**Upstash Box** sells a keep-alive box at USD 8 a month and metered active CPU at
USD 0.10 a core-hour, and the page states that a customer pays the lower of full CPU
usage and the matching keep-alive plan. On two cores the metered rate is USD 0.20 an
hour, so the crossover is 40 busy hours a month: below it the metre is cheaper,
above it the USD 8 flat price is. At 300 busy hours the metered bill is USD 60 and
the keep-alive is USD 8.

**Agent 37** bills the disk while the instance is stopped. At 4 GB that is
USD 0.36 a month, which is a fifth of its 300-hour bill and the whole cost of a
month in which nothing runs. It is still the cheapest model here because the
compute rate is the lowest, and the disk is the term to watch when the workload
stops for a season.

## The burst multiplier

`burst_x` is the ratio between the same month priced smoothly and the same month
priced as a burst of short starts. It is a different mechanism from the minimum
billable unit, and on the rows where both apply they do not agree.

179 records carry the figure. 25 of them price a burst month above 1.0x, and fourteen
clear 45 per cent. Both columns below are the `m10h` and `burst` costs from the
records, so the ratio is arithmetic over those two fields and this document only
tabulates it.

| Provider | Month at 10 h a day | Month as a burst | `burst_x` | What produces it |
| --- | --- | --- | --- | --- |
| azure-container-apps | USD 3.60 | USD 12.60 | **3.50x** | a one-hour minimum on a 15-minute start |
| expo | USD 124.00 | USD 298.00 | **2.40x** | USD 1 per build start |
| aws-workspaces | USD 84.01 | USD 172.20 | **2.05x** | a one-hour minimum |
| upcloud | USD 6.25 | USD 12.66 | 2.02x | a one-hour minimum |
| stackit | USD 15.40 | USD 30.79 | 2.00x | a one-hour minimum |
| Civo | USD 8.93 | USD 17.86 | 2.00x | a one-hour minimum |
| Hetzner Cloud | USD 3.12 | USD 6.24 | 2.00x | a one-hour minimum |
| Hetzner Dedicated | USD 32.25 | USD 64.50 | 2.00x | a one-hour minimum |
| Linode | USD 10.80 | USD 21.60 | 2.00x | a one-hour minimum |
| Naver Cloud | USD 42.42 | USD 84.84 | 2.00x | a one-hour minimum |
| Paperspace | USD 12.82 | USD 25.64 | 2.00x | a one-hour minimum |
| Scaleway | USD 7.78 | USD 15.56 | 2.00x | a one-hour minimum |
| Together Code Sandbox | USD 9.00 | USD 18.00 | 2.00x | a one-hour minimum |
| Vultr | USD 8.94 | USD 17.88 | 2.00x | a one-hour minimum |
| anchor-browser | USD 10.01 | USD 16.00 | 1.60x | a USD 0.01 per-start fee |
| sail | USD 13.01 | USD 19.00 | 1.46x | a USD 0.01 per-start fee |
| e2e-networks | USD 14.02 | USD 14.70 | 1.05x | rounds to one hour |

⭐ The multiplier is the number a reader acts on, and it is why a per-start fee and
a one-hour minimum belong in the same table: both convert a short burst into a
longer bill, and neither appears in an hourly rate column.

⚠ The tail of the distribution is a trap and it is recorded rather than ranked.
Five rows sit at exactly 1.0 (`alibaba-ecs`, `contabo`, `hostinger-vps`,
`latitude-sh`, `netcup`): all five carry a one-hour minimum that the burst
profile never reached, so a multiplier of 1.0 means the minimum did not engage at
that demand, not that the vendor has none. Eight more sit between 1.001 and 1.07
(`cloudflare-sandbox`, `github-codespaces`, `vercel-sandbox`, `stateset`,
`namespace`, `azure-vm`, `kamatera`, `sakura-cloud`), where a per-start fee or a
coarse rounding is real and negligible. Reading the first group as "no penalty"
would understate five bills.

The mechanism is the one the minimum-bill document tabulates by penalty, and both
documents read the same field from the same records.

## What did not work

- **A monthly VPS for a low duty cycle**: 93 times the metered cost at five busy
  minutes a day.
- **A one-hour minimum billable unit**: a thirty-minute run costs an hour, which
  doubles the effective rate. It applies to Hetzner and netcup, and for a
  24/7 box it is irrelevant, which is why the model has to be chosen before the
  vendor.
- **Active CPU for a workload that computes**: Vercel's USD 0.2128 per busy hour at
  50 per cent CPU is the most expensive row in the table.
- **A plan floor treated as a rate**: boat's USD 20 plan is a floor and a light
  month bills it, so the metered USD 5.40 is not what a burst workload pays.

## Chaining

The shape decides the model and the model decides the vendor, in that order. A
burst workload belongs on zipbox for the disk or Agent 37 for the lowest rate or
Upstash for a flat keep-alive. A continuous one belongs on Hetzner for the traffic.
A workload that waits on a model belongs on active-CPU billing, and the same
workload that computes belongs on a metre. One provider is never the answer to two
of those.
