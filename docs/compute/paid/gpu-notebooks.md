# The cheapest GPU hour, by card class

A GPU hour is not one commodity. An H100 hour and a T4 hour are different things, and
the price ratio between them is not the ratio of what they do, so a naive per-hour
comparison picks the wrong card. The number a reader needs is the price of the card they
actually need, on a marketplace that will actually give it to them.

The answer: the cheapest GPU hour in this lane is on Vast.ai's marketplace, at
USD 0.021 for a GTX 1660 S and USD 0.120 for an RTX 4090 in the 2026-10-22 snapshot,
and the host is a stranger's machine. The cheapest rate on a published card is RunPod's
RTX A5000 at USD 0.16 an hour on Community Cloud. Daytona's preemptible cards run from
an RTX 4090 at USD 0.57 to a B300 at USD 4.08, and its H200 at USD 2.61 is the cheapest
H200 here. Lightning AI publishes the broadest card table, from a T4 at USD 0.55 to an
H100 at USD 5.45, and ⛔ none of it is purchasable while the platform stays closed to all
users. Nothing in this lane has a live free tier: the grants in `free/gpu-notebooks.md`
are all dead.

## The comparison

By card, at the cheapest published rate. `Preemptible` is whether the host can
take the machine back, which is the term that decides whether a run can be
checkpointed. `Backed` is whether the record carries the rate.

⛔ **Every Lightning row below prices a platform that is closed to all users.** The
rates are published and unbuyable: all user access was revoked on 2026-10-16, and
`lightning.ai/security-incident` states that the Platform stays inaccessible to all
users. The rows stay because the rate card is the comparison, and `dead` is the verdict
on every one of them.

| Card | Provider | USD/hour | Backed | Preemptible | Verdict |
| --- | --- | --- | --- | --- | --- |
| T4 | Lightning AI | 0.55 | yes | no | dead |
| L4 | Lightning AI | 0.79 | yes | no | dead |
| A100 40GB | Lightning AI | 2.19 | yes | no | dead |
| A100 80GB | Lightning AI | 1.85 | yes | no | dead |
| L40S | Lightning AI | 3.54 | yes | no | dead |
| RTXP 6000 | Lightning AI | 4.64 | yes | no | dead |
| H200 | Lightning AI | 4.50 | yes | no | dead |
| H100 | Lightning AI | 5.45 | yes | no | dead |
| RTX 4090 | Daytona | 0.57 | yes | yes | paid-only |
| RTX 5090 | Daytona | 0.74 | yes | yes | paid-only |
| RTX PRO 6000 | Daytona | 1.74 | yes | yes | paid-only |
| H100 | Daytona | 2.27 | yes | yes | paid-only |
| H200 | Daytona | 2.61 | yes | yes | paid-only |
| MI355X | Daytona | 3.44 | yes | yes | paid-only |
| B200 | Daytona | 3.59 | yes | yes | paid-only |
| B300 | Daytona | 4.08 | yes | yes | paid-only |
| RTX A5000 | RunPod Community | 0.16 | yes | no | paid-only |
| RTX 3090 | RunPod Community | 0.22 | yes | no | paid-only |
| RTX 4090 | RunPod Community | 0.34 | yes | no | paid-only |
| L4 | RunPod Community | 0.44 | yes | no | paid-only |
| RTX PRO 6000 | RunPod Community | 1.69 | yes | no | paid-only |
| H200 | RunPod Community | 3.59 | yes | no | paid-only |
| H200 | RunPod Secure | 5.29 | yes | no | paid-only |
| B200 | RunPod Community | 5.98 | yes | no | paid-only |
| B200 | RunPod Secure | 7.99 | yes | no | paid-only |
| B300 | RunPod Community | 6.94 | yes | no | paid-only |
| B300 | RunPod Secure | 8.99 | yes | no | paid-only |
| GTX 1660 S | Vast.ai | 0.021 | yes | not stated in the record | paid-only |
| GTX TITAN X 12 GB | Vast.ai | 0.0422 | yes | no, on-demand | paid-only |

⛔ **Every row above is backed by a record.** A rate belongs to the record that
carries it: the Daytona GPU rows live in `daytona-gpu.json`, not in `daytona.json`, which
holds the sandbox rate card and no GPU table. `lightning-ai.json` carries the eight
Lightning rates, both A100 sizes and the RTXP 6000 included. `runpod.json` carries the
B200 and RTX PRO 6000 rows, all four of them, from `runpod.io/pricing` read 2026-10-24.
That page lists 21 cards behind a four-row table, which is why the RunPod block above is
eleven rows long.

⚠ **A rate in a document and not in its record is a fabrication risk.** Each row needs
one page read to hold it, and a row whose record carries no rate leaves the table.

## The two facts that decide the lane

**The A100 80GB is cheaper than the A100 40GB on Lightning's own table.** USD 1.85
against USD 2.19, both quoted from the rate table re-read on 2026-10-24. A reader who
assumes the larger card costs more will overpay for the smaller one. That is a pricing
artefact and it is worth checking on any provider's table before choosing.

**Daytona's preemptible tier is cheaper per card than RunPod's Community on-demand tier
on three of the four cards both price.** An H200 is USD 2.61 against USD 3.59, which is
27 per cent less; a B200 is USD 3.59 against USD 5.98, which is 40 per cent less; and a
B300 is USD 4.08 against USD 6.94, which is 41 per cent less. ⛔ The exception is the
RTX PRO 6000, where RunPod's USD 1.69 undercuts Daytona's USD 1.74 by 3 per cent.

⭐ For a training run that checkpoints, that discount is real money. For anything
that cannot resume, it is not a discount; it is a machine that will disappear.

## Lightning AI

T4 at USD 0.55, L4 at USD 0.79, L40S at USD 3.54, RTXP 6000 at USD 4.64, A100 40GB at
USD 2.19, A100 80GB at USD 1.85, H100 at USD 5.45 and H200 at USD 4.50, with 80 free
GPU hours to start (`documented`, `lightning.ai/pricing`, read 2026-10-24).

The page's own "Free hours to start" column converts the grant: 75 T4-hours, 31
L4-hours, 5 L40S-hours, 3 RTXP 6000-hours and 10 A100 40GB-hours. That spread, and not
a single number, is why publishing per-class prices matters.

⛔ **The platform is closed to all users, so no rate in this section can be bought.**
`lightning.ai/security-incident` states that all user access was revoked on 2026-10-16
at 01:00 UTC and that the Platform stays inaccessible to all users (`documented`, read
2026-10-24). The pricing page still advertises "Run 1 Studio free 24/7" at the same
read, and the operational page is the newer and more specific claim. ⚠ The incident
page names Studio, Deployments, Pipelines and Drive, and a platform closed to all users
closes the cluster lane with them.

⚠ The rate card is worth keeping for the day the banner clears. It is the broadest
single-vendor table in the lane, and it is not the cheapest: RunPod's L4 at USD 0.44 and
its RTX A5000 at USD 0.16 both undercut Lightning's T4 at USD 0.55.

Evidence: `lightning.ai/pricing`, `lightning.ai/security-incident` and
`status.lightning.ai` (all read 2026-10-24). Verdict: dead, and the rate card is the
part that outlives it.

## RunPod

On-demand, per second, in two tiers: Community Cloud and Secure Cloud. The page lists 21
cards on both tiers, from an RTX A5000 at USD 0.16 and USD 0.27 to a B300 at USD 6.94 and
USD 8.99 (`documented`, `runpod.io/pricing`, read 2026-10-24).

⛔ **The B200 and RTX PRO 6000 rates are real.** `runpod.json` carries both cards, and
the page publishes a B200 at USD 5.98 and USD 7.99 and an RTX PRO 6000 at USD 1.69 and
USD 2.49. The four rows are in the table.

⚠ **The page lists 21 RunPod cards and the table prices eleven.** The cheapest card here
is an RTX A5000 at USD 0.16, below Lightning's dead T4 rate and below every Daytona rate.
A rate card read only to its largest cards cannot support a claim about the cheapest
hour.

The Secure Cloud premium is 30 per cent on the B300 (USD 8.99 against USD 6.94) and 47
per cent on the H200 (USD 5.29 against USD 3.59). ⚠ The page does not state what the
premium buys and no reliability record for either tier is held here, so the difference is
a price and not a measured reliability claim.

⚠ Network storage is USD 0.05 per GB-month and up, which is a second bill that
scales with the dataset rather than the run.

⚠ The cheapest card, an RTX A5000 at USD 0.16, is USD 116.80 in a 730-hour month. CPU
pods are a separate product and are not on the page read, so this is the cheapest
machine this document can price at RunPod.

Evidence: `runpod.io/pricing` (read 2026-10-22 and 2026-10-24). Verdict: the clearest
two-tier market, the cheapest card rate on a published card, and a storage bill beside it.

## Daytona's GPU tier

Preemptible rates: RTX 4090 at USD 0.57, RTX 5090 at USD 0.74, RTX PRO 6000 at
USD 1.74, H100 at USD 2.27, H200 at USD 2.61, MI355X at USD 3.44, B200 at USD 3.59 and
B300 at USD 4.08 (`documented`, `daytona.io/pricing`, read 2026-10-22).

⛔ **These are not the cheapest card rates in the lane.** Vast.ai's marketplace was
quoting an RTX 4090 at USD 0.120 an hour and an RTX 5090 at USD 0.213 on the same day,
which is 4.75 times and 3.5 times below Daytona's rates for the same cards
(`vast-ai.json`). Daytona's rates are the cheapest on a published rate card here, but
not in the market.

On the two cards RunPod also prices, both Daytona rates are below RunPod's Community
on-demand rate, and every rate here is preemptible. Daytona also has an on-demand GPU
tier, whose rates the page lists under a heading the extraction did not resolve, so this
document carries the preemptible column only.

⛔ **The USD 200 free credit is not available for GPU sandboxes.** `daytona.json` quotes
the vendor's billing page: "Free credit balance: the amount of free credits; not
available for GPU sandboxes" (read 2026-10-24). The credit is a CPU sandbox allowance,
and the GPU lane has no free tier.

⚠ A GPU sandbox counts against a separate GPU quota in Daytona's earth region and
its vCPU, memory and disk do not count against the tier pool. The 15-minute inactivity
auto-stop applies to sandboxes and auto-stop 0 disables it, so an unattended GPU box is
possible, at USD 416.10 in a 730-hour month on the RTX 4090 rate.

Evidence: `daytona.io/pricing` (read 2026-10-22) and the billing page quoted in
`daytona.json` (read 2026-10-24). Verdict: the cheapest B200, B300 and H200 here, all of
them preemptible, and not the cheapest card in the lane.

## Vast.ai

Prices are set by supply and demand across 40 or more data centres, with
on-demand at per-second billing, interruptible at 50 per cent or more cheaper and
reclaimable, and reserved on 1, 3 or 6 month terms (`documented`,
`vast.ai/pricing`, read 2026-10-22).

⛔ **A gap recorded against a page that does not render is not a gap in the market.**
`vast-ai.json` carries the probe, the response size and its sha256.

A probe of `console.vast.ai/api/v0/bundles/` on 2026-10-22 returned 64 offers. Parsing
it gives the cheapest per-GPU rates as USD 0.021 for a GTX 1660 S, USD 0.109 for an RTX
3090, USD 0.120 for an RTX 4090 and USD 0.213 for an RTX 5090, and the record does not
separate those by tier. The cheapest whole card rentable on-demand was a GTX TITAN X
12 GB at USD 0.04222 an hour, which is USD 30.82 in a 730-hour month, and the cheapest
interruptible whole card was a GTX 1060 at USD 0.03339 an hour, which is USD 24.37.

The structural fact is the one that matters: Vast is a marketplace of third-party
hosts, so the cheapest rate is also the least reliable machine in the lane. The TITAN X
host is marked unverified, its reliability score is 0.985, and its egress is USD 4.00
per TB.

Evidence: `vast.ai/pricing` (read 2026-10-22) for the tier structure, and the
marketplace API snapshot of the same date for the rates. Verdict: the lowest rates and
the least accountability.

## Can any of these run as a machine

Every paid row in this document is a machine: an SSH endpoint or an API, a port that
answers, a disk that outlives the process, and no idle reap. That is what separates this
lane from the free one, where three of the five rows die with the tab and the other two
are a batch runner and a five-minute demo.

| Provider | Survives the tab | Idle reap | Session cap | Persistent disk | Reachable port | USD at 24/7 | Card gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lightning AI | no: the platform is closed | none | a 4-hour restart on a free Studio | yes | not stated | 0.00, and unbuyable | none |
| Daytona GPU | yes | 15 min, and auto-stop 0 disables it | none published | container disk survives a stop | previews and SSH | 416.10 | none to start; a card and a USD 25 top-up at Tier 2 |
| RunPod | yes | none | none | network volume, USD 0.05 a GiB-month | a port map and a proxy | 116.80 | card, and no hold amount recorded |
| Vast.ai | yes | none | none | host disk, retention set by the host | SSH and mapped ports | 30.82 | card and a USD 5 deposit |

⭐ **The cheapest 24/7 machine in this document is USD 30.82 a month**, which is 8.2
times the USD 3.75 answer for 8 GiB and 4 vCPU at GreenCloudVPS (`under-five.md`) and
106 times the USD 0.29 answer (`under-one.md`). Neither question asked for a
GPU. The notebook class is not the answer to either, and the two documents in this lane
exist for a workload that needs a card.

## What did not work

- **A free GPU on a sandbox provider**: no GPU sandbox is recorded for E2B, and its
  record carries no GPU field. That is an absence of evidence and not a vendor statement.
- **Google Colab as a paid GPU lane**: the limits are unpublished, so a budget
  cannot be computed. Colab Pro's compute units are a separate currency, and
  `google-colab-paid.json` carries `fails-quota`.
- **Kaggle as a paid lane**: no paid GPU tier is recorded. It is 30 hours a week and
  no more.
- **AWS, Azure and GCP on-demand GPU**: the affordable lanes are spot, which is
  preemptible, and no rate for any of the three is recorded in this corpus, so this
  document cannot price the comparison.
- **Serverless GPU platforms**: they price per invocation or per second of active
  compute, which is a different product and belongs with the inference topic.

## Chaining

Checkpoint every ten minutes and the preemptible tier is the right lane: Daytona's
H200 at USD 2.61 against RunPod's USD 3.59 is a 27 per cent saving and the only
cost is a restart. Without checkpoints the Secure Cloud or an on-demand Daytona box is
the answer and the premium is the price of finishing.

⭐ None of it answers the machine question. The cheapest 24/7 host in this document is
Vast.ai's GTX TITAN X at USD 30.82 a month, against USD 3.75 for 8 GiB and 4 vCPU at
GreenCloudVPS (`under-five.md`) and USD 0.29 for a WireGuard peer (`under-one.md`). A GPU
at 24/7 costs 8.2 times the USD 3.75 answer and 106 times the USD 0.29 answer, and neither
question asked for a GPU.
