# What a 30-minute run actually costs after rounding and plan floors

A headline hourly rate is a rate. What a bill charges is a rate multiplied by a
rounded duration, and then raised to a floor if the provider has one. Those three
mechanisms produce most of the difference between two quotes for the same machine,
and none of them is visible in an hourly rate column.

The answer: the sandboxes in this topic bill per second with no minimum, so a
30-minute run costs half an hour. Agent 37 adds a disk charge that runs for the
whole month whether the box does or not, which makes it the only row here whose
short-run cost is dominated by a term other than compute. boat, Contabo and
netcup have a monthly floor, so a light month costs the floor. Modal bills 60
seconds of keep-alive after the last input. Vercel bills provisioned memory in
one-minute increments. Those are the five mechanisms, and every one of them is
smaller than the error a reader makes by comparing hourly rates across billing
models.

## The three mechanisms

| Mechanism | What it does | Where it bites |
| --- | --- | --- |
| minimum billable unit | rounds a short run up to the unit | a 30-minute run on a 1-hour minimum costs 2x |
| keep-alive after the last input | bills time when nothing is running | Modal charges 60 seconds for an idle container |
| plan floor | raises a light month to a plan price | boat, Contabo and netcup all have one |
| metered resource vs wall clock | bills one dimension of a run | Vercel and Upstash bill CPU, not time |
| disk for the whole month | bills storage by the month, compute by the second | Agent 37, and every provider with a volume |

## The comparison at a 30-minute run

At 2 vCPU and 4 GiB, one run, no credit. `Effective` is what the run costs divided
by a half hour, which is the number to compare against a headline rate.

| Provider | Billed unit | One 30-min run | Effective rate | Floor |
| --- | --- | --- | --- | --- |
| zipbox Small | 1 second | USD 0.0069 | USD 0.0137/h | 2x |
| Lizard Small | 1 second | USD 0.0081 | USD 0.0162/h | 2x |
| boat small | 1 second | USD 0.0090 | USD 0.0180/h | USD 20 a month plan |
| Agent 37 | compute by the minute, disk by the month | USD 0.0030 plus USD 0.36 of disk | USD 0.0060/h plus disk | 2x |
| E2B | 1 second | USD 0.0828 | USD 0.1656/h | 2x |
| Daytona | 1 second | USD 0.0828 | USD 0.1656/h | 2x |
| Freestyle | 1 second | USD 0.0661 | USD 0.1322/h | 2x |
| Modal Sandbox | 1 second plus 60 s keep-alive | USD 0.1229 | USD 0.2459/h | 2x |
| Upstash active CPU | 1 second | USD 0.1000 at full CPU | USD 0.2000/h | USD 8 a month keep-alive |
| Vercel at full CPU | memory by the minute, CPU by the second | USD 0.1704 | USD 0.3408/h | 2x |

The two rows a reader is most likely to misread are Agent 37 and boat. Agent 37's
30-minute run costs three-tenths of a cent of compute and thirty-six cents of disk,
so the run is a rounding error and the month is the bill. boat's run is nine-tenths
of a cent and its plan floor is USD 20, so twenty runs a day for a month costs
USD 10.80 of metered time and bills USD 20.

## The minimum billable unit

This is the largest multiplier in the corpus. A thirty-minute workload priced against
every provider in the catalogue records the multiplier each minimum produces. **26 providers
clear 1.15x, and five of them clear 20x.** The three mac rows are the extreme: a
minute of work billed as a month, at 48x and 1,440x.

⚠ **A multiplier computed against 900 seconds is exactly twice the right answer**,
because the workload is 1,800 seconds. The `Penalty` column is the second bill column
divided by the first, so a reader can check any row by hand. ⚠ MacStadium's row does
not follow its own minimum: 30 days at its stated rate would be the largest multiplier
on the table, and its bill ratio is 20x. That row is inconsistent.

Sorted by the multiplier, which is the number a reader acts on. `Bill, smoothed` is the
month at this workload before the minimum, and `Bill, with the minimum` is the month
after it.

| Provider | Minimum billed | Bill, smoothed | Bill, with the minimum | Penalty |
| --- | --- | --- | --- | --- |
| hostmyapple | 2,592,000 s (30 days) | USD 14.38 | USD 20,706.62 | **1440x** |
| AWS EC2 Mac | 86,400 s (1 day) | USD 195.00 | USD 9,360.00 | **48x** |
| Flow Swiss Mac | 86,400 s | USD 97.89 | USD 4,698.65 | **48x** |
| use-computer | 86,400 s | USD 135.00 | USD 6,480.00 | **48x** |
| MacStadium | 2,592,000 s | USD 3,225.20 | USD 64,504.08 | **20x** |
| Alibaba ECS | 3,600 s (1 h) | USD 5.33 | USD 10.65 | 2x |
| Aptible | 3,600 s | USD 60.00 | USD 120.00 | 2x |
| AWS WorkSpaces | 3,600 s | USD 12.74 | USD 25.48 | 2x |
| Civo | 3,600 s | USD 8.93 | USD 17.86 | 2x |
| Contabo | 3,600 s | USD 2.71 | USD 5.42 | 2x |
| e2e-networks | 3,600 s | USD 13.20 | USD 26.40 | 2x |
| Hetzner Cloud | 3,600 s | USD 3.12 | USD 6.24 | 2x |
| Hetzner Dedicated | 3,600 s | USD 32.25 | USD 64.50 | 2x |
| Hostinger VPS | 3,600 s | USD 10.06 | USD 20.13 | 2x |
| Latitude.sh | 3,600 s | USD 57.00 | USD 114.00 | 2x |
| Linode | 3,600 s | USD 10.80 | USD 21.60 | 2x |
| Naver Cloud | 3,600 s | USD 42.42 | USD 84.84 | 2x |
| netcup | 3,600 s | USD 3.50 | USD 7.00 | 2x |
| Paperspace | 3,600 s | USD 12.00 | USD 24.00 | 2x |
| Sakura Cloud | 3,600 s | USD 39.98 | USD 79.97 | 2x |
| Scaleway | 3,600 s | USD 6.89 | USD 13.79 | 2x |
| Stackit | 3,600 s | USD 14.78 | USD 29.55 | 2x |
| tinfoil | 3,600 s | USD 48.00 | USD 96.00 | 2x |
| UpCloud | 3,600 s | USD 6.25 | USD 12.50 | 2x |
| Vultr | 3,600 s | USD 8.94 | USD 17.88 | 2x |
| Vultr Windows | 3,600 s | USD 23.21 | USD 46.43 | 2x |

⚠ **Two rows carry money figures that neither record holds.** `aptible.json` and
`tinfoil.json` both have an empty `extras.m10h_usd` and `extras.m24h_usd`, so the bills
above come from the card and not from the records. Aptible's record also carries no
`extras.granularity`, so its one-hour minimum appears in no field. Both rows are kept
because the multiplier follows from the stated minimum, and both are marked here because
a price in a document and not in its record is the defect this corpus cares most about.

⛔ **A plan floor and a minimum billable unit are different mechanisms.** Four rows
carry a plan floor or a keep-alive; the minimum billable unit covers 26 rows. Counting
the two as one understates the multiplier by a factor of six and omits the three worst
cases.

⭐ This is the mechanism that separates a batch tool from an interactive one. A
tool that runs for 20 seconds and bills an hour is thirty times its rate, and no
hourly column shows it. A tool that runs for a minute and bills a month is 1,440
times its rate, and the vendor is not doing anything unusual: it is selling a
dedicated Mac by the month.

⚠ The multiplier and the shape are not separable, and a ranking without this table
reads as if the mac rows were cheap. `hostmyapple` at
USD 14.38 a month is the cheapest figure in its column and the most expensive bill
in the corpus, because the month is what it sells.

For the sandboxes here the unit is one second and the question does not arise.
That is the single strongest argument for a sandbox over a VPS for a burst
workload: it is not the rate, it is the rounding.

## The keep-alive after the last input

Modal keeps a container alive for 60 seconds after the last input and bills that
time (`documented`, `modal.com/pricing`, read 2026-10-22). A 30-minute run
therefore bills 31 minutes, which is a 3.3 per cent surcharge on a long run and not
worth modelling.

The sandbox rate is USD 0.2380 an hour, so 31 minutes is USD 0.1229 and the same
run on zipbox is USD 0.0069. The keep-alive is not the reason for that difference;
the non-preemptible rate is, and so is the shape. Both are on the same page and
only one of them is a rounding error.

⚠ It becomes worth modelling when the runs are short. An agent that makes a
10-second call every minute pays 60 seconds of keep-alive for each one, which is
six times the work it asked for. Modal allows the timeout to be configured, and
short-call workloads should set it.

## The plan floor

boat's USD 20 plan is credit rather than a fee, so a light month bills USD 20
while `small` at 300 hours is USD 5.40. Contabo and netcup bill the monthly price
by definition. In all three cases the floor is the product and the hourly rate is
decoration.

⭐ A floor is not a defect. It is what makes a 24/7 box cost USD 6.49 instead of
USD 4.76 times twelve. A reader should choose the floor when the workload is
continuous and avoid it when the workload is not.

## Metered resource against wall clock

Vercel bills active CPU and provisioned memory. Upstash bills active CPU. Kedge
bills CPU time scheduled on a core and memory pages touched. In all three, an agent
waiting on a model costs almost nothing and an agent parsing a document costs full
rate.

⛔ This is the mechanism behind the largest apparent conflicts. Vercel at USD 102.24
and USD 63.84 for the same shape are 100 per cent and 50 per cent CPU, and neither
figure states which it assumes. Upstash at USD 3.29 and USD 8.82 are a
keep-alive proration and a metered bill on one page. A reader given one of the two
numbers has been given a rate without its dimension.

## The disk that runs for the month

Agent 37 meters compute by the minute while the sandbox runs and disk while the
instance is kept (`documented`, `agent37.com/docs/agents-api/instance-sizing`, read
2026-10-22). At 2 vCPU, 4 GB and 4 GB of disk the disk is USD 0.36 a month.

That is 17 per cent of the 300-hour bill and it is the whole cost of a month in
which nothing runs. Every provider with a volume has the same shape and most do not
state it as plainly.

## What did not work

- **A one-hour minimum as a cost model**: it applies to Hetzner and to netcup, and
  for a 24/7 box it is irrelevant. It only binds a burst workload, and
  a burst workload should be on a per-second sandbox.
- **Comparing a rate across billing models**: the 90 disagreements across the
  catalogue are mostly this error and not a factual disagreement.
- **A plan floor as a rate**: Daytona's USD 2,000 and Contabo's USD 2.71 are both
  floors or quotients and neither is a bill.

## Chaining

The rule this document supports is short: choose the billing model before the
provider. A workload made of short runs belongs on a per-second sandbox with no
floor. A workload that stays up belongs on a monthly box with a traffic
allowance. A workload that waits on a model belongs on active-CPU billing. Getting
the model wrong costs more than any difference between two vendors in the same
model.
