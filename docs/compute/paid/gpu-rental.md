# The GPU lane: what a card costs, and why 29 of 41 records cannot price one

`docs/expansion/compute.md` names GPU rental below the hyperscaler floor as the largest
whole category absent from the first census. The records carry it now: 41 carry
`category: GPU cloud`. This document covers all 41, and it states in every table how many
of the 41 the table holds.

The answer, in one paragraph. **Twelve of the 41 records state an hourly rate for a named
card, and 29 do not**, so a reader who wants a GPU price has 12 usable rows and 29 files
that will not answer. No record in the class grants a free GPU hour. Thirty-four carry
`free_tier_kind: none`. The 7 that carry `allowance` or `one-time-credit` grant nothing on a
card. Cerebrium's Free tier is a free platform with compute billed per second and a 5-GPU
concurrency cap. Comfy Deploy starts on credits. Paperspace's Free plan includes CPU
machines at USD 0.04 to USD 0.30 an hour. Baseten's allowance is the placeholder sentence,
and Vultr's rests on an API that refuses. The two credits are USD 5 at DigitalOcean and
USD 200 at OVHcloud, and both are one time. On the 12 rankable records the
price of one H100 ranges from USD 2.25 at TensorDock to USD 11.6751 per GPU on an eight-GPU
Google node, which is 5.19 times. On an A100 80 GB the same comparison is 2.20 times, and
Google sits within 0.57 per cent of Replicate. The spread is a term and a node shape, not
silicon.

## What this document covers, by mechanism

Each record sits in exactly one row, and the counts add to 41. The column that decides the
group is what the vendor is selling and whether it publishes a price for it.

| Mechanism | Records | What decides the price | Rankable here |
| --- | --- | --- | --- |
| USD hourly rate for a named card | 12 | the card class | yes |
| a monthly or fixed-term node | 3 | the term and the entry fee | partly |
| a marketplace of third-party hosts | 2 | supply, not the vendor | no |
| self-serve hourly, no per-card rate | 6 | the deployment, not the card | no |
| a one-time trial credit, no card rate | 2 | the credit size | no |
| contract-gated, no self-serve path | 6 | a negotiation | no |
| sells a product, not capacity | 4 | a licence or a request | no |
| priced per deployment | 1 | the instance size | no |
| page unreadable | 3 | nothing recorded | no |
| dead | 2 | nothing sold | no |

The 12 rankable records are `cerebrium`, `comfy-deploy`, `coreweave`, `gcp-compute-gpu`,
`hyperbolic`, `lambda`, `nebius`, `replicate`, `runpod`, `sfcompute`, `tensordock` and
`thunder-compute`. The other 29 carry no USD hourly figure for a named card, and 20 of the
29 carry no currency figure anywhere in the record. A reader who wants a price has 12 rows;
a reader who wants a mechanism has all 41.

## The card-rate group: 12 records, one comparable column

Sorted by card, then by rate. Every rate is the vendor's own figure from a page read on
2026-10-22. The unit is USD per GPU-hour. A row that names a whole node divides the node
price by its card count, and says so.

| Provider | Card | USD/hour | Free allowance | Rung | Verdict |
| --- | --- | --- | --- | --- | --- |
| Tensordock | unnamed consumer card | 0.12 | none | `documented` | paid-only |
| Tensordock | H100 SXM5 | 2.25 | none | `documented` | paid-only |
| Thunder Compute | RTX A6000 | 0.35 | none | `documented` | paid-only |
| Cerebrium | T4 | 0.5904 | allowance | `documented` | qualifies-with-caveat |
| Comfy Deploy | T4 | 0.6480 | credits | `documented` | qualifies-with-caveat |
| Replicate | T4 | 0.81 | none | `documented` | paid-only |
| Hyperbolic | H100 SXM | 3.19 | none | `documented` | paid-only |
| Thunder Compute | H100 SXM | 3.20 | none | `documented` | paid-only |
| Cerebrium | H100 | 3.3984 | allowance | `documented` | qualifies-with-caveat |
| Lambda | H100 SXM | 3.99 | none | `documented` | paid-only |
| SF Compute | H100 | 5.04 | none | `documented` | paid-only |
| Replicate | H100 | 5.49 | none | `documented` | paid-only |
| GCE | H100, per GPU on an 8-GPU node | 11.6751 | none; GPUs excluded | `documented` | qualifies-with-caveat |
| Lambda | A100 SXM 80 GB | 2.79 | none | `documented` | paid-only |
| Replicate | A100 80 GB | 5.04 | none | `documented` | paid-only |
| GCE | A100 80 GB | 5.0688 | none; GPUs excluded | `documented` | qualifies-with-caveat |
| Comfy Deploy | A100 80 GB | 6.1488 | credits | `documented` | qualifies-with-caveat |
| RunPod Community | H200 | 3.59 | none | `documented` | paid-only |
| Hyperbolic | H200 | 3.99 | none | `documented` | paid-only |
| RunPod Secure | H200 | 5.29 | none | `documented` | paid-only |
| Hyperbolic | B200 | 5.99 | none | `documented` | paid-only |
| Cerebrium | B200 | 6.012 | allowance | `documented` | qualifies-with-caveat |
| Lambda | B200 SXM6 | 6.69 | none | `documented` | paid-only |
| RunPod Community | B300 | 6.94 | none | `documented` | paid-only |
| RunPod Secure | B300 | 8.99 | none | `documented` | paid-only |
| Nebius | B300 NVLink | 9.50 | none | `documented` | paid-only |
| CoreWeave | RTX PRO 6000 | 20.00 | none | `documented` | paid-only |

Three arithmetic notes. Cerebrium publishes per second, so its T4 is USD 0.000164 times
3,600, its H100 is USD 0.000944 times 3,600 and its B200 is USD 0.00167 times 3,600
(`cerebrium.ai/pricing`, read 2026-10-22). Google publishes an eight-GPU node at USD 93.4007
an hour, so one H100-hour on that node is USD 11.6751 (`cloud.google.com`, read 2026-10-22).
RunPod publishes two tiers for one card. On the H200 the Secure tier is 47.4 per cent above
Community, and on the B300 it is 29.5 per cent above
(`runpod.io/pricing`, read 2026-10-22).

The spread inside one card is what a buyer can act on, and it is smaller than the topic's
headline suggests.

| Card | Cheapest | Dearest | Ratio | Records |
| --- | --- | --- | --- | --- |
| H100 | 2.25 | 11.6751 | 5.19 | 8 |
| A100 80 GB | 2.79 | 6.1488 | 2.20 | 4 |
| H200 | 3.59 | 5.29 | 1.47 | 3 |
| B200 | 5.99 | 6.69 | 1.12 | 3 |
| B300 | 6.94 | 9.50 | 1.37 | 3 |
| T4 | 0.5904 | 0.81 | 1.37 | 3 |

⚠ **The H100 row is the only wide one and its width is a node, not a vendor.** Drop the
eight-GPU Google node and the H100 range becomes USD 2.25 to USD 5.49, which is 2.44 times.
The five other cards sit between 1.12 and 2.20 times. A card is already a commodity in this
class, and the remaining spread is the term.

## The card where the hyperscaler is not the dearest

`paid/gpu-notebooks.md` states that AWS, Azure and GCP on-demand GPU run three to five times
RunPod per card. On the two cards where a Google rate and a marketplace rate both exist in
this class, that multiplier is 2.93 and 1.82, and on one comparison it fails outright.

| Card | Google | Marketplace host | Google against it |
| --- | --- | --- | --- |
| H100, per GPU on an 8-GPU node | 11.6751 | Lambda at 3.99 | 2.93 times above |
| H100, per GPU on an 8-GPU node | 11.6751 | Hyperbolic at 3.19 | 3.66 times above |
| A100 80 GB | 5.0688 | Lambda at 2.79 | 1.82 times above |
| A100 80 GB | 5.0688 | Replicate at 5.04 | 0.57 per cent above |
| A100 80 GB | 5.0688 | Comfy Deploy at 6.1488 | 17.6 per cent below |

⚠ **Comfy Deploy charges more for an A100 80 GB hour than Google does**, so "the hyperscaler
is always dearest" is false in this class on the one card where three sellers publish. The
comparison also depends on whether the buyer takes a node: the 3.66 and 5.19 times figures
are an eight-GPU node divided by one card.

⭐ **The claim that survives is narrower than three to five times.** On these five rows the
Google premium over another seller of the same card runs from 17.6 per cent below to 3.66
times above, and only the node-priced H100 rows reach the range that sentence asserts. A
quotation that needs one number should say "up to 3.66 times on an H100 node, and no premium
at all on an A100 80 GB".

The marketplace has no RunPod rate for a card Google also publishes in this class, because
`runpod.json` holds B300 and H200 only. So the three to five times sentence cannot be checked
against RunPod from these records at all.

`docs/compute/paid/gpu-notebooks.md` carries the same card ladder for notebooks and reaches
a compatible conclusion on the H100 tier.

## The marketplace group: 2 records, and the price is a listing

**Vast.ai** sets no price. Hosts compete across 40 or more data centres. On-demand bills per
second, and interruptible instances are reclaimable and stated at 50 per cent or more below.
Reserved runs sell on 1, 3 or 6 month terms (`vast.ai/pricing`, read 2026-10-22). The pricing
page renders live card prices client-side and the extraction returned no number, so no rate
is recorded. That is a gap and not a zero, and `vast-ai.json` carries it in
`extras.gap`.

**Shadeform** is the aggregator shape rather than the marketplace shape. It provisions
across 30 or more clouds from one console with centralised billing, and reserved capacity
carries a 12-month minimum term (`shadeform.ai/`, read 2026-10-22). It publishes no rate and
the record correctly holds none.

⭐ **These two are the records a price table cannot hold, and either could hold the cheapest
card.** The mechanism is the reason: a listing is an offer at a moment, and this corpus reads
pages weeks apart. The query has now been run: `https://console.vast.ai/api/v0/bundles/`
returned 64 offers on 2026-10-22, and `vast-ai` carries GTX 1660 S at USD 0.021 per GPU-hour,
RTX 3090 at USD 0.109, RTX 4090 at USD 0.120 and RTX 5090 at USD 0.213 from that snapshot.
⚠ Those are marketplace rates on one day and they move with host supply.

Both are `paid-only`, and both are 2 of the only 2 records in the whole class whose identity
cost was read from a page rather than assumed. The other 39 carry `identity_cost.kind: email`
with a detail saying the value was assumed, so this class cannot say what registration costs.

## The monthly-contract group: 3 records, and the entry fee is the price

These three rent a node on a term. The hourly figure exists on the page for one of them, and
it is not what a buyer pays in month one.

**Hetzner GPU servers** run from EUR 214.00 a month or EUR 0.3429 an hour, up to EUR 5.7676
an hour, and each configuration carries a one-time setup fee equal to one month's rent,
from EUR 209 to EUR 3,599 (`hetzner.com/dedicated-rootserver/matrix-gpu/`, read 2026-10-22).
The arithmetic decides the row. EUR 214.00 divided by EUR 0.3429 is 624.1 hours, so the
monthly price is not the hourly rate times 730. A buyer who rents 300 hours in month one
pays EUR 102.87 of compute plus EUR 209.00 of setup, which is EUR 311.87 and an effective
EUR 1.0396 an hour, or 3.03 times the quoted rate. Held for a year at 300 hours a month the
setup fee amortises to EUR 17.42 a month and the effective rate falls to EUR 0.4010, which
is 16.9 per cent above the quote. The fee equals 609.5 hours of the hourly rate, so a
rental shorter than that spends more on the fee than on compute.

**Scaleway GPU instances** list an L4 node from about EUR 574.87 a month and an L40S node up
to about EUR 4,599 (`scaleway.com/en/pricing/gpu/`, read 2026-10-22). The record states the
monthly figure and says instances are priced per hour with monthly equivalents; it does not
carry the hourly number. Divided by 730 the monthly figure is EUR 0.7875 an hour, and that
division is this document's, not the vendor's. A 300-hour month still bills the full EUR 574.87, which
is 2.43 times the 300-hour share of EUR 236.25.

**Voltage Park** sells HGX H100 capacity from 1 to 1,016 GPUs for bursts, or 32 to 8,000 or
more in one configuration on a contract, and states no ingress, egress or support charges
(`voltagepark.com/pricing`, read 2026-10-22). The record holds no rate, so the card cannot
be priced here.

## The two one-time credits: 2 records, and neither buys a GPU hour

Both records carry `free_tier_kind: one-time-credit` and both verdicts are `trial-only`.

**DigitalOcean GPU Droplets** carry USD 5 of credit for a new account, valid for 90 days and
forfeited with any remainder, and the record holds no rate for a Droplet
(`digitalocean.com/pricing`, read 2026-10-22). It is `reported` rather than `documented`,
because the GPU pricing page was not the page that was read.

**OVHcloud GPU instances** carry a one-time USD 200 new-account credit with no free instance
tier underneath it, and the cheapest general-purpose row on the page is b3-8 at USD 0.0605 an
hour (`ovhcloud.com/en/public-cloud/prices/`, read 2026-10-22). ⚠ The GPU table sits on the
same page and its rate was not extracted, so USD 200 divided by USD 0.0605 is 3,306 hours of
a CPU row and says nothing about GPU hours.

## The self-serve hourly group: 6 records with no per-card rate

Six vendors let a reader provision tonight and publish no figure comparable to the table
above. They are not the same product and they fail the table for different reasons.

**Crusoe** bills GPU capacity by the hour for GB200 NVL72 and AMD MI355X classes, and adds
dedicated inference endpoints that need no sales engagement
(`crusoe.ai/cloud/pricing`, read 2026-10-22). The page names the classes and carries no
figure the record kept. **Verda** states per-GPU-hour pricing on multi-node clusters with no
commitment and no minimum, with specs and price shown per GPU
(`verda.com/pricing`, read 2026-10-22). **Together AI** states that all GPU prices are per
GPU per hour on demand or reserved and carries no number
(`together.ai/pricing`, read 2026-10-22).

**SF Compute** (`sf-compute-gpu`) is two products with different walls, and both are `paid-only`. Its market
sells a whole node of eight H100 or H200 cards at an orderbook rate, and that rate is not
public: `/pricing` returns a sign-in page, `/prices` redirects to the homepage, and the
orderbook endpoint answers `missing authentication token`, so the docs' "public orderbook"
means anonymised rather than open. The only public labels are a marketing panel reading
"Reserved price $3.00/gpu/hr" and "Realized price $4.29/gpu/hr", and the panel contradicts
the docs, which define realized as the cost after resale and therefore below the reserved
rate. Its Autoresearch product publishes a full rate card without a sign-in: `h100-1` at
USD 0.084 a minute (USD 5.04 an hour) with a 15-minute idle window, an eight-GPU node at
USD 40.32 an hour, and "There is no minimum charge" because billing ends when the node
stops. Account caps are 5,760 node-hours with 720 per SKU, raised only by organization
verification and a support request.

**GPU.LAND** (`gpu-land`) publishes one headline figure, USD 0.25 an hour for a vGPU instance,
and states no VRAM and no card model on the page read (`gpu.land`, read 2026-10-22). A third-party
index prints a USD 722.70 row for the same provider, which is three orders of magnitude apart and
is recorded as an unresolved disagreement rather than averaged.

**Hyperstack** bills per minute and quotes one GPU row at USD 0.00672043 an hour plus storage
at USD 0.000096774 a GB-hour (`hyperstack.cloud/gpu-pricing`, read 2026-10-22). The page
rounds that storage figure to about USD 0.10 a TB-hour, and at the vendor's own decimal
gigabyte it is USD 70.65 a month for one TB held. ⚠ **That single GPU row is 334.8 times
below the cheapest H100 in the table above and 17.9 times below its cheapest row of any
kind, so it is not a whole card and the record does not say what it prices.**

**Jarvislabs** bills per minute, prices a CPU VM at USD 0.012 a vCPU-hour plus USD 0.0032 a
GB-hour of RAM and storage at USD 0.10 a GB-month, and states no GPU rate
(`jarvislabs.ai/pricing`, read 2026-10-22). Its smallest CPU tier is 2 vCPU and 8 GB, which
is USD 0.0496 an hour on its own formula.

**Paperspace** includes C4, C5 and C7 machines on a Free Gradient subscription at USD 0.04,
USD 0.08 and USD 0.30 an hour, and those are CPU machines
(`docs.digitalocean.com`, read 2026-10-22). Its GPU rate is not in the record.

⚠ **Paperspace is the row where a free-tier filter misleads most.** Its Free plan is a CPU
allowance on a GPU platform, so a reader who filters for a free GPU finds a row that grants
no GPU. Its own `retention-clamped` limit is the constraint that matters: a powered-off
machine still bills attached storage, public IPs and add-ons until those are destroyed.

## The contract-gated group: 6 records, no self-serve path

Six records sell capacity and will not sell it to a client who arrives without a
conversation. All six carry `binding: write-gated`, and the constraint is the finding rather
than the price.

| Record | What the page sells | Why it is not a row |
| --- | --- | --- |
| `fluidstack` | 250 MW data centres at AI-infrastructure scale | no self-serve plan and no published price |
| `rescale` | a simulation platform over elastic compute and storage | access is arranged with the vendor |
| `sf-tensor` | researchers embedded for a six-week fixed engagement | compute is billed separately on the client's own quota |
| `tensorpool` | a push and pull training workflow with normal SSH access | SSH is offered to an account that has bought capacity |
| `zibra-labs` | distributed clusters across hyperscalers and neoclouds | arranged by contact |
| `pipeshift` | managed single-tenant inference clusters on Pipeshift Cloud, or in the client's VPC | no plan, no price, no self-serve path |

⭐ **Five of the six are not a GPU rental and the sixth is a service.** TensorPool is the one
that sells a machine, and its gate is a purchase rather than a phone call. SF Tensor and
Rescale sell a person's time. A reader who needs a card tonight skips all six.

## The group that sells a product, not capacity: 4 records

These four carry `category: GPU cloud` and sell a licensed product. They are the group that
makes the category label wrong, and each is `write-gated` for that reason.

**fal** prices model calls per second and per token, from USD 0.007 per 1,000 tokens to
USD 1.20 per million tokens on the rows read, and states no free tier
(`fal.ai/pricing`, read 2026-10-22). The record's own session note says it best: the unit is
a second of generated video or a token, so there is no session.

**Expanse** predicts GPU allocation, memory use and completion probability before a job runs.
It analyses the buyer's queue and supplies no capacity (`expanse.sh`, read 2026-10-22).
**Sieve** processes and licenses video, audio and image data (`sievedata.com/`, read
2026-10-22). **Texel.ai** sells an optimised inference pipeline and names GPU selection among
the setup costs it has absorbed (`texel.ai`, read 2026-10-22).

⛔ **None of the four enters a per-hour comparison, and the category field is why a reader
finds them here.** A count over `category: GPU cloud` returns 41 records and 4 of them will
never quote a GPU hour. The record's `limits[]` says so in every case.

**Baseten** is a fifth deployment-priced record and sits in its own row above. It prices a
dedicated instance sized by CPU, RAM and GPU and publishes no rate
(`docs.baseten.co/deployment/resources`, read 2026-10-22). Its `free_tier.stated` is the
placeholder sentence, which 4 of the 41 carry and `../gaps.md` lists, and its confidence is
`reported`, so neither the free tier nor the rate is a finding.

## The records that could not be read, and the two that are gone

**`poplarml` answers 404 on its own origin.** The broker, the firecrawl route, a raw fetch
and the archive closest month all failed on 2026-10-22, and `http://poplarml.com` returns no
page at all. The record is `unverified` and not `dead`, because a 404 on an apex is not a
withdrawal. ⚠ **Its `paid-only` verdict rests on a catalogue card and a 404, so both of its
columns are unknown and a reader should treat neither as a finding.**

**`vultr-gpu` is `unverified` because the plans API refuses.** The GPU plan list returns 403
with a bot challenge to the broker and to the firecrawl route, and the raw fetch returned
1,774 bytes of challenge body. The record does not re-assert its verdict from a challenge.
The `vultr` record is `documented` from a page read and is the place to look for the general
position.

**`azure-gpu` is `reported` for a structural reason.** The retail-price API returns JSON price
records rather than a page, so no GPU rate is recorded and no factor for Azure is computable
from this corpus. Its 750 free hours name B2ts v2, B2pts v2 and B2ats v2, which are
burstable CPU shapes.

**`flowdeploy` is dead.** The domain serves a parked page of paid link-farm text pointing at
a subdomain, with no product, price or signup. **`mistral-compute` is dead.** The product page
returns 404 on every route and the capture lands on a help-centre shell. Both deaths are
`reported` and neither was observed first-party, so a re-check of one should cover both.

Thirteen other records carry `extras.reclassified_from: dead` and are live. Two of that
fourteen are the dead pair above, so twelve were moved from dead to live and each of the
twelve was read on 2026-10-22. The reclassification was right: no free tier on a catalogue
card is not evidence that a product is gone.

## The 10-hour money column does not price a card

Ten records carry `extras.talaria_m10h_usd` and one carries `extras.m10h_usd`. Those columns
hold what a 10-hour day costs for a month, and a reader will read them as a GPU price. On
the records where a per-card rate was also read from the page, they are not one.

| Record | Figure at 10 h a day | Implied USD/hour | Rate the page states | Ratio |
| --- | --- | --- | --- | --- |
| `nebius` | 11.04 | 0.0368 | 9.50 per B300 GPU-hour | 258 times below |
| `hyperstack` | 105.00 | 0.3500 | 0.00672043 on one GPU row | 52 times above |
| `sfcompute` | 219.46 | 0.7315 | 5.04 per h100-1 hour | 6.9 times below |
| `jarvislabs` | 15.00 | 0.0500 | 0.0496 on the 2 vCPU CPU formula | 1.008 times |

⛔ **On Jarvislabs the figure equals the CPU formula to within 0.8 per cent, so that
column priced a CPU VM and not a card.** On Nebius it sits 258 times below the vendor's own
B300 rate, and on SF Compute 6.9 times below its h100-1 rate. The column cannot be used
as a GPU price on any record, and `paid/vps-monthly.md` is the document that reads it
correctly, at a CPU shape.

## What the records contradict

**Two records state free egress and record none.** `thunder-compute` carries the limit "data
egress is $0.00 a GB" and `voltage-park` carries "no ingress, egress or support costs are
charged", and both carry `egress.terms: "not published on the source card"`. The field
disagrees with the record's own limits. All 41 carry an empty `egress` object, so a filter on
that field returns nothing for a class where two vendors do publish a zero term.

**The identity column is an assumption on 39 of 41 records.** Each of the 39 carries
`identity_cost.kind: email` and a detail that says the value is assumed because no signup was
performed. Only `runpod` and `vast-ai` carry a requirement that was read from a page: a card.
The class therefore cannot answer what registration costs, which is the constraint this
corpus says binds every large quota.

## What did not work

- **A free GPU on a permanent tier**: no record in this class publishes one. The free lane is
  a notebook quota, and `../free/gpu-notebooks.md` owns it.
- **Vast.ai as a rankable row**: the page renders prices client-side and returned none. A gap,
  not a zero.
- **The hyperscaler free tiers**: 750 hours and USD 200 of credit buy CPU. No GPU.
- **Hetzner as a cheap GPU hour**: a EUR 209 setup fee turns 300 hours into EUR 311.87, which
  is 3.03 times the quoted rate.
- **The `qualifies` verdict as a free-tier filter**: 6 of the 41 carry a `qualifies*` verdict
  and 2 of the 6, `gcp-compute-gpu` and `azure-gpu`, record `free_tier_kind: none` with their
  own evidence stating there is no free GPU allowance. `baseten` is a third whose evidence
  states no free tier and whose kind field says `allowance`. `../gaps.md` carries this as a
  vocabulary defect.
- **Expanse, Sieve, Texel.ai and fal as capacity**: they sell analysis, data, an optimised
  pipeline and model calls. All four are `write-gated`.
- **FlowDeploy and Mistral Compute**: a parked domain and a 404.
- **The 10-hour money column as a card price**: on Jarvislabs it is the CPU formula.

## What this cannot establish

⛔ **No card in this class was booted, and no GPU hour was bought.** Every rate here is a
page read on 2026-10-22. No record in this class carries the `measured` rung, and the
topic's four `measured` records measure a transport, a listing or a price rather than a
quota, so the difference between a published rate and an invoice is unobserved, and the rounding rule, the
plan floor and the idle keep-alive are exactly what this class does not record.

**Whether any card is obtainable.** A rate is an offer and not stock. Twenty-nine of the 41
records carry no per-card hourly rate, and none of the 41 states an availability figure.
`../gaps.md` names this as the largest hole in the GPU lane, and `vast-ai` is the row where
it matters most.

**What a run costs after the meter.** Seven of the 41 state a minimum bill in a numeric
field: `baseten`, `hyperstack`, `jarvislabs` and `verda` at 60 seconds, `runpod` and
`vast-ai` at 1 second, and `sfcompute` at 0. Eight records say per-second or per-GPU-second
in prose, and `gcp-compute-gpu` names the first second only to say billing starts there. So
the field understates the class and the prose overstates it in one place. ⚠ A 60-second
floor multiplies a 10-second job by six, and no record here says whether its floor applies
to a stopped-and-restarted instance.

**What egress costs.** Two records publish a zero term and 39 publish nothing. A training run
that moves a model out of this class is unpriced until the invoice arrives, and the serving
target assumed here is 500 GB a day to 1 TiB a day.

**What a monthly node costs at a duty cycle below 730 hours.** Scaleway's rate is a monthly
figure and its hourly number is not in the record. Hetzner's is both, and the two do not
agree, because EUR 214.00 is 624.1 hours of EUR 0.3429.

## The record index: all 41, by slug

Every record in the class, so a reader can reach the file behind any sentence above. The
slug is the join key and it is what `dossier/compute/` names. Seven of the 41 are named by
provider in the prose and not by slug, and this table is how those seven stay reachable.

| Group | Records |
| --- | --- |
| USD hourly rate for a named card | `cerebrium`, `comfy-deploy`, `coreweave`, `gcp-compute-gpu`, `hyperbolic`, `lambda`, `nebius`, `replicate`, `runpod`, `sfcompute`, `tensordock`, `thunder-compute` |
| monthly or fixed-term node | `hetzner-gpu`, `scaleway-gpu`, `voltage-park` |
| marketplace | `shadeform`, `vast-ai` |
| self-serve hourly, no card rate | `crusoe`, `hyperstack`, `jarvislabs`, `paperspace`, `together-gpu`, `verda` |
| one-time trial credit | `digitalocean-gpu`, `ovh-gpu` |
| contract-gated | `fluidstack`, `pipeshift`, `rescale`, `sf-tensor`, `tensorpool`, `zibra-labs` |
| sells a product, not capacity | `fal`, `sieve`, `texel-ai`, `expanse` (self-hosted) |
| priced per deployment | `baseten` |
| page unreadable | `azure-gpu`, `poplarml`, `vultr-gpu` |
| dead | `flowdeploy`, `mistral-compute` |

## Chaining

The lane is a card plus a checkpoint plus object storage off the instance. Thunder Compute is
the row to start with, and the reason is not its rate. Egress is USD 0.00 a GB and the first
100 GB of instance disk per GPU is included. Moving a model out is therefore priced at zero
on the one record that states a term. Every other provider in the class leaves that cost
unpublished.

Checkpoint every ten minutes on any row whose card is preemptible. Nebius states a
preemptible B300 from USD 0.99 a GPU-hour against USD 9.50 on demand, which is 9.6 times.
CoreWeave's spot rows sit at 81.2 and 52.1 per cent of on-demand on the two rows recorded
(`docs.nebius.com` and `coreweave.com/pricing`, both read 2026-10-22). SF Compute is the one
record with a numeric idle clock. It carries a 15-minute window on h100-1 that bills at most
USD 1.26, and 20 minutes on h100-8 that bills at most USD 13.44
(`autoresearch.sfcompute.com/`, read 2026-10-22). `../the-clock.md` owns the class.

Put the dataset in `storage` rather than on the instance. Every provider here that records a
storage term bills it separately from the card and most bill it while the card is stopped.
