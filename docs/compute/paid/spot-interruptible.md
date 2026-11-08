# Spot and preemptible capacity: the discount, then the notice

A spot rate is a discount with a deadline attached. Every provider here cuts the rate, so
the question is whether the notice before reclaim is long enough to write a checkpoint and
restart from it. This document answers that for the five records carrying a spot or
preemptible GPU offer. The headline is a pair. Nebius lists an H100 NVLink at USD 0.79 a
GPU-hour in eu-north1 against USD 4.50 on-demand: 17.6 per cent of on-demand, 5.70 times
cheaper, with 60 seconds of notice. Azure lists an A100 80 GiB at USD 0.67877 against USD
3.673 in eastus: 18.5 per cent and 5.41 times, with 30 seconds. The two deepest discounts
in the class are 30 seconds apart in the warning they give, and no record here carries a
maximum continuous runtime to compare them on.

## The short answer

Sorted by the share of on-demand the spot rate represents, cheapest first. `Share` is the
spot rate divided by the on-demand rate for the same instance in the same region on the
same day. A dash means the record carries no such figure.

| Provider | Instance, GPU | Spot (USD/h) | On-demand (USD/h) | Share | Notice | Max runtime | Fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `nebius-ai-cloud` | H100 NVLink, eu-north1 | 0.79 | 4.50 | 17.6%, 5.70x | 60 s | not stated | the price ceiling | qualifies |
| `microsoft-azure-spot` | NC24ads_A100_v4, 1x A100 80 GiB, eastus | 0.67877 | 3.673 | 18.5%, 5.41x | 30 s | not stated | the 30 s notice | qualifies |
| `oracle-cloud-infrastructure` | VM.GPU3, preemptible | - | - | 50% less, stated | 120 s | not stated | no rate in the record | paid-only |
| `google-cloud-spot` | a2-highgpu-1g | 2.20401 | - | not computable | 120 s or 0 s | not stated | no on-demand pair | qualifies-with-caveat |
| `amazon-ec2-spot` | g6.xlarge, us-east-1 | 0.476 | 0.805 | 59.1%, 1.69x | 120 s | not stated | GPU Spot quota is 0 | fails-quota |

The notice runs from 30 seconds to 120, a factor of four, and it is the only number a
scheduler can act on before launch. The AWS row is here on price alone: its verdict is
`fails-quota`, because the GPU Spot quota defaults to 0 vCPU and the Free plan allowlist has no
GPU family.

## The arithmetic: one pair, one region, one day

A discount is a ratio between two rates for the same machine, so a ratio built from one
region against another is not a discount. Every division below shows its pair.

**Amazon EC2 Spot: 59.1 per cent.** `amazon-ec2-spot` records one pair from a single
per-region table: g6.xlarge spot at USD 0.476 in us-east-1 against on-demand USD 0.805 in
us-east-1. `0.476 / 0.805 = 0.591`, so the spot rate is 59.1 per cent of on-demand and 1.69
times cheaper, the weakest discount in the slice. AWS states "up to 90% compared to
On-Demand pricing", and that 90 is a ceiling across families rather than a rate for this
shape. A run costing USD 100 on-demand costs USD 59 here, and two restarts from scratch
cost more than the on-demand run would have.

The record contradicts itself on this price, and the disagreement is the finding. The AWS
feed at `website.spot.ec2.aws.a2z.com/spot.js` (read 2026-10-22) returns 7,625,200 bytes
with a last-modified header of 13 May 2024, more than two years before the read, and it
prices g6.xlarge at USD 0.1050. Against the same USD 0.805 that is 13.0 per cent and 7.67
times, and nobody can buy it. Two live trackers read on 2026-10-22 disagree for one region:
`devzero.io/instances/aws/g6.xlarge` gives USD 0.411 for us-east-2, and
`doit.com/compute/spot/us-east-2/g6.xlarge` gives USD 0.2238.

**Google Cloud Spot: the discount is stated, the pair is not in the record.**
`google-cloud-spot` carries three accelerator rows, all quoted for 1 hour: a2-highgpu-1g at
USD 2.20401, a3-highgpu-1g at USD 6.273932575, and g2-standard-4 at USD 0.423016. It
carries no on-demand rate for any of them. ⛔ **No ratio is computed for GCP here.** The
page states "up to 91% discounts for many machine types, GPUs, TPUs, and Local SSDs", which
is a ceiling and not a pair. Dividing USD 2.20401 by a rate from another page would produce
a number in the same column as Azure and Nebius that is comparable to neither.

The record carries something a scheduler can use before a launch. Estimated uptime is "the
minimum amount of time that you can expect most of your Spot VMs to run before Compute
Engine preempts them", and it takes three values: 60 minutes, 10 minutes, or 1 minute. If
it returns 10 minutes and the checkpoint interval is 10 minutes, the lane does not cover
its setup cost. ⚠ **The GCP preemption rate is a different statistic.** It divides
preempted VMs by VMs that stopped running, and that denominator counts machines their
owners stopped, so it is not a per-hour probability.

**Microsoft Azure Spot: 18.5 per cent, the same ratio on three cards.**
`microsoft-azure-spot` carries the cleanest pair in the slice, because both numbers come
from one Retail Prices query filtered to `armRegionName eq 'eastus'` and
`armSkuName eq 'Standard_NC24ads_A100_v4'`, each with `unitOfMeasure` of "1 Hour": spot USD
0.67877, on-demand USD 3.673. `0.67877 / 3.673 = 0.1848`, so 18.5 per cent and 5.41 times
cheaper. Two more SKUs from the same filter set hold the ratio, so it is not a scrape
accident: NV6ads A10 v5 is USD 0.083899 spot against USD 0.454 on-demand, 18.5 per cent and
5.41 times, and NC4as T4 v3 is USD 0.149174 against USD 0.526, 28.4 per cent and 3.53
times.

**Nebius AI Cloud: 17.6 per cent, and a ceiling one cent under on-demand.**
`nebius-ai-cloud` pairs a probed spot page against an on-demand table from the same
provider. H100 NVLink in eu-north1 is USD 0.79 against USD 4.50, so `0.79 / 4.50 = 0.1756`,
17.6 per cent and 5.70 times. H200 in us-central1 is USD 0.89 against USD 5.40, 16.5 per
cent and 6.07 times. Both are the deepest ratios in the slice.

The B300 row is where the care goes. The pricing page gives USD 9.50 on-demand and "From
$0.99" preemptible. `0.99 / 9.50 = 0.104` gives 10.4 per cent and 9.6 times, and the
numerator is a floor across twelve markets while the denominator is one stated rate. That
is a discount against a floor, not against a region: the best number in the class and the
least reliable one.

⚠ **The Nebius rate is the floor of a range that moves every 15 minutes.** The policy
states the price "may change as often as every 15 minutes" and that "the highest
preemptible VM price is always one cent below the current pay-as-you-go on-demand rate".
The worst case for the H100 is USD 4.49, 5.68 times the recorded rate, so a run with no
price cap has unbounded cost. The record's chaining field divides a USD 300 credit by USD
0.79 and gets 380 H100-hours; `300 / 0.79 = 379.7` reproduces that, and no evidence row in the
record states a USD 300 credit, so that field is its only source.

**Oracle Cloud Infrastructure: 50 per cent, on two shapes.**
`oracle-cloud-infrastructure` states the discount without a rate pair: "Preemptible
capacity costs 50% less than on-demand capacity in all regions". Fifty per cent less is 0.50
of on-demand, or 2.00 times, and the record holds no rate for any preemptible GPU shape, so
no division is shown. The Supported Shapes list contains VM.GPU2 and VM.GPU3, and it does
not contain VM.GPU.A10, VM.GPU4, or bare metal. The cheapest OCI GPU is not offered as
preemptible at all, so a reader who wants the 50 per cent lands on a V100-generation shape.

## The interruption notice, side by side

Sorted by notice, shortest first, because the shortest notice sets the checkpoint budget.

| Provider | Notice | How it arrives | Best effort? | After the notice |
| --- | --- | --- | --- | --- |
| `microsoft-azure-spot` | 30 s | a scheduled event | stated best effort | not stated in the record |
| `nebius-ai-cloud` | 60 s | SIGTERM to the guest | not stated | STOP only; volumes preserved |
| `amazon-ec2-spot` | 120 s | EventBridge, and IMDSv2 `spot/instance-action` | stated best effort | stop or terminate |
| `google-cloud-spot` | 120 s, or 0 s configured | not stated in the record | the 30 s shutdown period is best effort | up to 30 s of shutdown work |
| `oracle-cloud-infrastructure` | 120 s | an event fires | not stated | termination |

A checkpoint that writes 4 GiB spends `4096 x 1024 x 1024 x 8 / 1e9 = 34` seconds on the
wire at 1 Gbit/s before protocol overhead. That does not fit Azure's 30 seconds, and it
takes over half of Nebius's 60. It fits more than three times inside the 120 seconds that
AWS, GCP and OCI give.

⚠ **A notice is not a guarantee.** AWS marks its two-minute notice best effort and Azure
marks scheduled-event delivery best effort. Poll the event stream continuously, checkpoint
on the interval, and use the notice only to trigger a final flush. Google's
`--preemption-notice-duration` accepts 120 seconds or 0 and nothing between, and 0 removes
the trigger entirely, so a reader who sets it has no signal to flush on.

## What an 8-hour job survives

The arithmetic comes from `microsoft-azure-spot`, which computes it rather than measuring
it, so the record's rung is `inferred`. Its 2.3 and 4.1 per cent inputs come from an
analysis of 10 million spot instance hours, not from a probe. Take a 10-minute checkpoint,
so the expected work lost per preemption is 5 minutes. At 2.3 per cent an hour the overhead
is 0.19 per cent and the effective A100 80 GiB rate is USD 0.680. At 4.1 per cent an hour
the overhead is 0.34 per cent and the rate is USD 0.681. A 10-minute checkpoint turns a 5.41
times discount into a 5.40 times discount, so what breaks a run is the absence of a resume
path, not the rate.

| Preemption rate | 1 hour | 8 hours | 10 hours |
| --- | --- | --- | --- |
| 2.3% an hour | 97.7% | 83.0% | 79.5% |
| 4.1% an hour | 96.0% | 71.5% | 66.4% |
| 17.5% an hour | 83.9% | 21.5% | 17.4% |

The 1-hour and 10-hour columns are the record's. The 8-hour column is computed here from
the same model, `0.977 ^ 8 = 0.830`, `0.959 ^ 8 = 0.715` and `0.825 ^ 8 = 0.215`, so each
cell derives from the rate in its row and is not a new measurement.

⚠ **The record's 17.5 per cent row does not reproduce.** A 17.5 per cent hourly rate leaves
0.825 per hour, which is 82.5 per cent at one hour, not the 83.9 printed. The printed pair
of 83.9 and 17.4 reproduces from 0.839 per hour, a 16.1 per cent rate, so read that row as
16.1 per cent. The 2.3 and 4.1 rows do reproduce.

An 8-hour job on the A100 row finishes on one attempt 83.0 per cent of the time at 2.3 per
cent an hour, and 71.5 per cent at 4.1 per cent. The rest restart from the last checkpoint,
at 5 minutes plus reload each. A job needing 8 hours of uninterrupted state, such as a warm
optimiser and a loader queue held in memory, is not a spot job at any of these rates unless
it can serialise that state inside the notice.

## Checkpointing: what the provider gives and what you build

One of five records states what survives a preemption. `nebius-ai-cloud` preserves volumes,
and its only supported preemption action is STOP. The boot disk and every attached volume
survive; the process does not. That is persistence of storage, not of process state.

The other four do not state what happens to attached disk at preemption. For AWS that
matters, because stop and terminate are different actions with different disk outcomes and
the record names both. ⛔ **Write the gap, do not fill it.** A run that assumes the volume
survives on AWS, GCP, Azure or OCI assumes something no record here supports.

So the reader builds the checkpoint, and the cost lands in the storage lane rather than the
GPU lane. Write it to object storage off the instance, on an interval well inside the
notice. Google's 30-second shutdown period is the only stated window for work after the
notice, and it is best effort, so it holds a buffer flush and not a checkpoint.

## The minimum bill

Only one record carries a billing interval, and it is the one with the deepest discount.
`nebius-ai-cloud` bills in 15-minute intervals, with a worked example: 8 GPUs at 0.25 hours
at USD 2.00 is USD 4.00, then 8 GPUs at 0.25 hours at USD 2.50 is USD 5.00 across a price
change. A 1-minute run on one H100 therefore bills 0.25 hours, so `0.25 x 0.79 = USD
0.1975`. The unrounded minute would be `0.79 / 60 = USD 0.0132`, and the multiplier is 15.

The other four records carry no interval, and that gap is worth naming. Azure's Retail
Prices API returns `unitOfMeasure` of "1 Hour" for the price it quotes, and a unit of price
is not a billing granularity. ⛔ **A price unit is not a minimum.** Reading "1 Hour" as a
floor would invent a minimum of USD 0.67877 that no page states.

## The identity gate

All five records name `card` as the identity cost, and none names a company or an
institution. Spot capacity is open to an individual with a card and a billable account, and
to nobody without one.

| Provider | Identity | What the card unlocks | Blocking step |
| --- | --- | --- | --- |
| `amazon-ec2-spot` | card, and a paid plan | Spot at standard rates | the Free plan allowlist has no GPU |
| `google-cloud-spot` | card | Spot VMs on a billable account | the trial cannot add GPUs |
| `microsoft-azure-spot` | card, pay-as-you-go 003P | Spot on the supported SKUs | NC_A100_v4 starts at 0 cores |
| `nebius-ai-cloud` | card | everything; prices readable without an account | none beyond the card |
| `oracle-cloud-infrastructure` | card | preemptible VM.GPU2 and VM.GPU3 | the GPU is not on Always Free |

Amazon fails on quota rather than price, and it fails twice. The Free plan allowlist is
T3.micro, T3.small, T4g.micro, T4g.small, C7i-flex.large and M7i-flex.large, and no GPU
family appears on it. Separately, the Spot quota table lists "All G and VT Spot Instance
Requests" at a default of 0 vCPU. Either gate needs an upgraded paid plan, so the USD 100
to 200 credit buys CPU Spot at standard rates and not GPU time. The credit survives the
upgrade for 12 months.

Google's blocker is the account class. On a non-billable trial account the console refuses
"Add GPUs to your VM instances", and the Spot limitations list states that the Compute
Engine Free Tier credits "don't apply to Spot VMs". The USD 300 over 90 days cannot buy a
Spot GPU.

Azure's blocker is a quota of zero. Specialized families including NC_A100_v4 start at "a
default of zero cores", and GPUs also default to zero. Spot supports three offer types
only: Enterprise Agreement, pay-as-you-go 003P, and Sponsored 0036P and 0136P. 003P is the
individual's route, and an account on the USD 200 for 30 days free tier must upgrade first.

Nebius is the one row where the discount is verifiable at zero identity cost. The policy
states "You don't need a Nebius AI Cloud account to view them", and the spot page was read
anonymously, returning 202,986 bytes with a stated update time of 22 Oct 2026, 13:40 UTC.

## A spot price list is not spot capacity

⚠ **The cheapest listed rate is not available in every region, and often not in the region
priced.** Five records show this, by five mechanisms.

The AWS feed is a stale snapshot: last-modified 13 May 2024, and the parsed config holds no
g6e, p5e or g7e size, so the newest GPU families are absent from the file that would price
them. Nebius shows the opposite failure: the rate is real and the region is single. H100 is
priced in eu-north1 and the record names no second region, so there is nowhere to move when
the price rises. H200 is priced in three regions on one reading at USD 0.89, USD 2.45 and
USD 5.09, a spread of `5.09 / 0.89 = 5.72` times inside one provider on one minute. A
reader quoting "Nebius H200 at 0.89" has quoted the best of three markets.

Azure shows a regional multiplier over a stable home market: spot at USD 0.67877 in eastus,
eastus2, westus2 and westus3, and at USD 1.357541 in brazilsouth, exactly twice the eastus
spot. No brazilsouth on-demand rate is in the record, so the discount there is not computed.

Google shows a measurement gap. Preemption history covers 30 days per machine type and
zone, and it cannot report "N1 machine types with GPUs attached, custom machine types or
TPUs", so the cheap GPU lane is the lane the history cannot describe, and the feature is
Preview. Oracle shows a shape gap: the 50 per cent holds "in all regions", the only uniform
discount in the slice, and it covers two shapes that exclude the cheapest GPU.

## What this class does not give

No provider here puts a GPU on a free plan. The AWS allowlist has six shapes and no GPU, and
its GPU Spot quota is 0. GCP bars Spot from the Compute Engine credits. Azure starts
NC_A100_v4 at zero cores. OCI's Always Free page lists two compute entitlements, two
VM.Standard.E2.1.Micro instances and 1,500 OCPU hours of VM.Standard.A1.Flex a month, and no
GPU shape.

⭐ **The 500 GPU-hour Oracle claim is dead, and the refutation is worth keeping.** A
syndicated article states that OCI Always Free includes "1 NVIDIA A10 GPU, 24GB VRAM ...
capped at 500 GPU-hours per month", worth about USD 640 a month. The official page, read in
full, holds no GPU entitlement. The cited blog returns HTTP 403 and Wayback reports no
capture. That is why `oracle-cloud-infrastructure` carries `verdict: paid-only`: the claim
of a free GPU is dead and the provider is not. The record's
own evidence rows document a live preemptible offer at 50 per cent off, so a reader who wants
that offer reads the evidence rows and not the verdict alone.

## What would change the answer

The probe that would settle the class is written in the notes of `microsoft-azure-spot`:
rent one A100 spot in eastus for 24 hours, checkpoint every 10 minutes to object storage,
log every eviction with its timestamp and the offset between the scheduled event and the
stop, and repeat across four regions. That run yields both the real per-hour rate and the
real notice-to-eviction interval, which is the column this document cannot verify from a
page.

Four smaller measurements would each move one row. A regional g6.xlarge spot price read
from the AWS API on the day, because the feed is stale and two trackers disagree by 1.84
times for one region. An on-demand rate for a2-highgpu-1g, which turns Google's stated 91
per cent into a pair that belongs beside the others. A price for a preemptible VM.GPU3
shape, the one number missing from the Oracle row. An eviction probability read from Azure
Resource Graph for NC24ads_A100_v4 in eastus, which replaces the third-party 2.3 per cent
and upgrades the survival table's rung.
