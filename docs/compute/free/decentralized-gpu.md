# Decentralized GPU: USD 6 at signup, USD 106 after one application

This document answers what the decentralized GPU marketplaces, the Bittensor subnets, the
consumer-GPU networks and the free inference lanes give a reader with no budget and no hardware.
Two platforms hand an individual a dollar credit at signup without a company: Akash Network at
USD 1 for an email address, and Lium at USD 5 for a confirmed email or a first paid deposit, which
the record classes as a card. That is USD 6, and at each platform's own rate for the
cheapest card with hosts behind it, USD 6 buys 27.5 RTX 3090 GPU-hours. One further application
adds USD 100 at AMD Developer Cloud, which is 50 hours on one MI300X and 94 per cent of the
class's dollar value. The ceiling for a plain individual is USD 106 and 77.5 GPU-hours, or 3.2
days of one card.

⭐ **The class is worth about USD 3 of consumer capacity and 50 hours on one datacenter card.**
Vast.ai sells the same RTX 3090 hour at USD 0.109 with no credit at all, so the 27.5 hours the
two credits buy would cost USD 3.00 in the open market.

⚠ **A rate is not capacity, and here that decides the number.** One marketplace prints USD 0.048
an hour for an RTX 3060 and reports zero available hosts for it. Another lists 199 host places
across seven cards, and both of the free places sit on one card. Every price below carries its
supply.

## The short answer

The credit lane, sorted by what an individual can claim. The card column names the cheapest card
that had supply, not the cheapest card on the rate card.

| Platform | Trial credit | Cheapest card with supply, and its rate | GPU-hours | Identity | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `akash-network` | USD 1, 30 days | RTX 3090 at USD 0.150 | 6.7 | email or OAuth; no card, no wallet | the 30-day window and the 24-hour deployment cap | trial-only |
| `lium` | USD 5, 14 days, one per IP address | RTX 3090 at USD 0.240; the USD 0.06 RTX 3060 shows 0 available GPUs | 20.8 | confirmed email or a paid deposit; one grant per IP | the per-IP rule and the USD 20/hour node cap | trial-only |
| `nosana` | USD 50 announced 2026-03-13; no self-serve route today | RTX 3090 at USD 0.192, on 2 of 39 hosts; the USD 0.048 RTX 3060 has 0 of 16 | 260.4 if granted | card on the 2026-06 route; the email route states no amount | supply, then the early-access list | trial-only |
| `amd-developer-cloud` | USD 100, 30 days, allocated at AMD's discretion | MI300X; the vendor's two figures divide to USD 2.00 | 50.0 | card at account creation, plus program membership | expiry destroys the VM and its data; a stopped instance still bills | trial-only |
| `amd-radeon-cloud` | 100 points, 1 point per GPU-hour | Radeon on ROCm, 16 cores and 55 GB | 100, in 20-point daily slices | any phone number, or a GitHub account | 20 points a day, one instance at a time, idle still bills | qualifies-with-caveat |
| `ocean-network` | USD 100 reported by a third party; the amount renders at claim | H200, H100 and A100 on paid environments; no rate recorded | not computable: no card rate | email, a Discord or Telegram handle, four questions | the amount is unknown until it renders; paid jobs need escrow | trial-only |
| `aethir` | up to USD 10,000 for selected partner teams | H200 class at about USD 1.25 | not computable for an individual | national ID through ComPilot and Sumsub | the application form, then KYC | fails-identity |
| `render-network` | EUR 50, concluded | OctaneBench tiers at EUR 0.60 to EUR 2.40 per 400 OBh | 0: the offer closed | email plus an Octane licence | the credits ended; network rendering needs a paid licence | trial-only |
| `gongji-compute-individual` | CNY 50, about 24 hours of one 4090 | RTX 4090 at CNY 15.84 per 8-card hour | 24 | email, then a group join and a form | anything above CNY 50 needs a review and an audience | qualifies |
| `vast-ai` | none; USD 5 minimum deposit | RTX 3090 at USD 0.109; GTX 1660 S at USD 0.021 | 0 | card | the first dollar; preemption on the interruptible tier | paid-only |

## What actually binds

Four candidates explain why the class stays small, and two survive. **The first dollar is
refuted**: the credits are free, the paid rows fail on a balance, and Vast.ai's cheapest offer is
USD 0.021 per GPU-hour. **Identity is confirmed for 7 of 35 records and for every large
allowance**: Baidu PaddlePaddle at 16 V100-hours a day and ModelScope Notebook at 100 MI300X hours
each need a national identity document. **Supply is confirmed**: `nosana` reports two free places,
both on one card, across the seven on its own homepage, and `lium` reports 1,612 of 1,692 GPUs
already rented.
**The calendar is confirmed at four platforms**: AMD destroys the VM and its data at expiry, Akash
closes a deployment at 24 hours, Lium's credit expires at 14 days, AtomGit wipes the filesystem at
2 hours. ⛔ No record here carries `identity_cost.kind: anonymous`, so the claim that this class is
anonymous is unsupported.

## The arithmetic, divided out

### Akash Network: USD 1 is 6.7 GPU-hours

The trial is USD 1 of credit for 30 days, with an email or OAuth signup and no card
(`akash.network/docs/getting-started/quick-start/`, read 2026-10-22): deployments up to 24 hours
each, and GPUs up to the RTX 3090 only. Every card above it, including the RTX 4090, RTX 5090,
A100, H100, H200 and B200, needs a non-trial account. USD 1.00 divided by USD 0.150 is 6.7
GPU-hours, at a third-party tracker's rate for an Akash RTX 3090
(`computeprices.com/providers/akash/gpus/rtx3090`, read 2026-10-22). A second index lists the
same card at USD 0.090, which would make the credit 11.1 hours, and neither index states how many
hosts were free, so 6.7 is a rate-card figure.

⚠ **Akash contradicts itself on H100**, stating USD 1.33 an hour on the homepage and USD 2.73 on
its H100 page as of 2026-10-20. An older blog still advertises USD 10 of trial credit.

### Lium: USD 5 is 20.8 hours, not the 83 the rate card implies

Lium grants USD 5 once per IP address, expiring at 14 days, against a confirmed email address or
a first paid deposit (`docs.lium.io/pod-users/fingerprint-signup`, read 2026-10-22). Its
`llms-full.txt` adds that the credit is false when this IP address has already signed up once.
The division has two versions and the difference is supply.

| Rate card | Division | Hours | Supply on that card |
| --- | --- | --- | --- |
| RTX 3060 at USD 0.06 | 5.00 / 0.06 | 83.3 | `available_gpus` 0, `available_nodes` 0 |
| RTX 3090 at USD 0.24 | 5.00 / 0.24 | 20.8 | rentable, the cheapest node with a host |
| H100 at USD 2.00 to USD 3.75 | 5.00 / 3.75 to 5.00 / 2.00 | 1.3 to 2.5 | rentable, the only datacenter card the credit reaches |

⚠ **The 83-hour figure is arithmetic on a card nobody can rent.** It is the number a summary
prints, and the same record that produced it recorded zero available GPUs. Lium's guide adds a
cap the rate card does not show, quoted from `docs.lium.io/developers/agents` (read 2026-10-22):
with only the USD 5 credit a renter can take nodes below USD 20 an hour, which excludes every
8-GPU H100 and B300 node.

### Nosana: USD 50 is 260.4 hours, and 2 hosts are free

The March 2026 post quotes USD 50 claimed instantly with no extra steps. The live site states
only that a user claims free credits when logging in with email, with no amount. The October and
November 2025 posts route the grant through an early-access list, and the June 2026 post puts it
behind payment verification.

The division is not the problem. USD 50.00 divided by USD 0.192 is 260.4 GPU-hours on an RTX
3090. USD 50.00 divided by USD 0.048 is 1,041.7 hours on an RTX 3060. USD 50.00 divided by USD
0.500 is 100 hours on an RTX 5090.

⚠ **The availability column kills two of those three.** Nosana's homepage reports hosts per card
as 0 of 16 on the RTX 3060, 0 of 5 on the 4060, 0 of 7 on the 4070, 2 of 39 on the 3090, 0 of 94
on the 4090, 0 of 38 on the 5090 and 0 of 0 on the H100. Those seven rows list 199 host places,
two of them available and both on the 3090. The 260.4 hours is the only division with a host
behind it, on a card that costs four times the cheapest one.

### AMD Developer Cloud: USD 100 is 50 hours on an MI300X

The USD 100 is a member benefit of the AMD AI Developer Program
(`developer.amd.com/ai-developer-program/`, read 2026-10-22): quoted, USD 100 in AMD Developer
Cloud credits. An AMD technical article puts the same grant at approximately 50 hours, and a
second AMD page corroborates the rate: 25 hours described as approximately USD 50 worth. USD 100
divided by 50 hours is USD 2.00 per MI300X GPU-hour, and USD 50 divided by 25 is the same figure.

Three terms decide whether the hours are usable, and all three are in AMD's own FAQ
(`amd.com/en/developer/resources/cloud-access/amd-developer-cloud.html`, read 2026-10-22). Credit
expires 30 days from deposit and expiry destroys the VM and its data. A powered-off instance
still consumes credit until it is destroyed. Allocation is discretionary, quoted as determined by
AMD in its sole discretion, and a valid credit card is required at account creation.

⚠ **The 50 hours are the only datacenter-card hours an individual can reach here.** The larger
AMD grant, 100,000 hours, is restricted to Indian researchers and startups, which is a country
gate rather than a quota.

### Vast.ai: the market rate that prices every credit above

Vast.ai has no trial. Its launch page quotes both sentences that end the question: no free trial
currently, and a card is required though a USD 5 deposit is enough to start. Its marketplace API
answers with prices, so the class finally has a benchmark. A probe of
`console.vast.ai/api/v0/bundles/` on 2026-10-22 returned HTTP 200 with 177,005 bytes, sha256
`14ae21ac30941206b38860c6107be97bdf05a59132e289ec0b25d6bca7241f78`, 64 offers and no
challenge. ⭐ **An offer in that JSON is rentable at that moment**, which is what separates it
from Nosana's zero-host card.

| Card | USD per GPU-hour | The credits above, priced against it |
| --- | --- | --- |
| GTX 1660 S | 0.021 | one of the 64 offers, not a training card |
| RTX 3090 | 0.109 | Akash 1.38 times above, Lium 2.2 times above |
| RTX 4090 | 0.120 | cheaper per hour than Akash's RTX 3090 rate |
| RTX 5090 | 0.213 | Nosana's USD 0.500 is 2.35 times above |

**`vast-ai.json` was corrected on 2026-10-22.** Its `notes` and `extras.gap` both describe
the API probe that produced those four rates, and `extras.rate_snapshot` fixes the snapshot date.
`docs/compute/paid/gpu-rental.md` and `docs/compute/gaps.md` carry the same probe. The evidence
row is the artefact, and the rates are one day's snapshot, not a rate card.

## The class total, added up

| Tier | What has to be true | Addition | Total USD | Total GPU-hours |
| --- | --- | --- | --- | --- |
| 1 | an email address | 1 + 5 | 6 | 6.7 + 20.8 = 27.5 |
| 2 | AMD allocates the member credit | 6 + 100 | 106 | 27.5 + 50.0 = 77.5 |
| 3 | Nosana grants USD 50 and Ocean grants USD 100 | 106 + 50 + 100 | 256 | 77.5 + 260.4 = 337.9, plus Ocean's unknown |
| 4 | a partner team selects you at Aethir | 256 + 10,000 | 10,256 | not computable |

⭐ **Tier 1 is the number a reader acts on: USD 6 and 27.5 GPU-hours.** Tier 2 is the
realistic best case, and 50 of its hours are on one card behind one decision. Tier 3 multiplies
the dollars by 2.4 (256 / 106) and quadruples the hours, and every term in it is an announcement
rather than a standing offer. ⛔ Two credits cannot enter the USD column, because no exchange rate
was recorded on the day: EUR 50 at `render-network`, which has concluded, and CNY 50 at
`gongji-compute-individual`.
Gongji divides inside its own currency: the vendor states CNY 50 is 24 hours of one 4090, and an
8-card 4090 hour is CNY 15.84, so CNY 50 divided by CNY 15.84 is 3.16 node-hours, or 25.3
card-hours.

**What the sum buys at the market's own price.** The 27.5 hours of tier 1 are RTX 3090 hours.
Vast.ai sells that card at USD 0.109, so the same hours cost USD 3.00. The credits price them at
USD 6.00 divided by 27.5 hours, which is USD 0.218 a GPU-hour, and that is 2.0 times the open
market for the same card. ⚠ The voucher's face value overstates what it buys. The datacenter half
is not small: USD 2.00 for an MI300X GPU-hour with 192 GB of VRAM beats any consumer card,
because no consumer card holds a 70B model at half precision.

## The free lanes that are not credits

Five lanes grant GPU time with no dollar credit, and the largest of them is twice the size of the
biggest credit above.

| Lane | What is free | Card | Identity | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- |
| `modelscope-notebook` | 100 GPU-hours, then up to 1,000 through content review | MI300X, 192 GB of VRAM | national ID, through a linked Alibaba Cloud account | 8 to 10 hours per boot, only `/workspace` persists | fails-identity |
| `modelscope` | 36 GPU-hours one-time, plus a free 8-core CPU notebook | A10 24 GB | national ID | 10 hours per instance, 1-hour idle stop | trial-only |
| `molab` | no published quantity | RTX Pro 6000 Blackwell, 96 GB of VRAM | email | quoted: free as long as resources are not oversubscribed | qualifies-with-caveat |
| `atomgit-notebook` | 1,000 core-hours a month | Ascend 910B | a mainland China phone number | 2-hour session, filesystem wiped on close | qualifies-with-caveat |
| `baidu-paddlepaddle-ai` | 16 V100-hours a day, 480 a month | V100 16 GB | national ID | the real-name gate, then PaddlePaddle-only images | fails-identity |

⭐ **`modelscope-notebook` carries the largest card in the slice and the clearest refusal.** 192 GB
of VRAM holds a 70B model at half precision with room for activations, and 100 hours at 8-hour
slices is 12 sessions. The gate is a national identity document, so the verdict is
`fails-identity` and the number is recorded to show what the gate is worth.

⚠ **AtomGit's 1,000 is core-hours, not GPU-hours.** The record holds `gpu_hours_per_month` null
because the shape table did not render, and dividing 1,000 by the vCPU count gives about 31
instance-hours at 32 vCPU and about 250 at 4 cores. `molab` publishes no number at all, only the
condition that it stays free while resources are not oversubscribed.

## The Bittensor subnets: what the token buys

Three records touch Bittensor, and the honest answer to what the token buys is that no record
states it.

**`lium` is recorded as Bittensor Subnet 51.** Its pricing, credit and node feed are denominated
in USD per GPU-hour, and signup is one unauthenticated POST that reports whether the credit
landed. No page read records a TAO balance, a stake or a registration fee.

**`chutes` contradicts itself on the wallet.** Its starter guide says a Bittensor wallet is
optional, its web signup works with a username plus a fingerprint credential, and its README and
CLI reference still say registration requires a wallet and hotkey, so a reader who follows the
CLI first wrongly concludes it is gated.

**`targon` is the counter-example to the wallet assumption.** Account creation is an email
address and a password with no wallet field, and its documentation never asks for a TAO balance.
The wallet appears on the provider side only, where a miner hotkey is used.

**`gensyn` is not a subnet, and it is inverted.** It pays suppliers who bring hardware, its
dashboard states there are no official swarms running right now, and its reward is an allocation
from a 2 per cent testnet pool with no published formula.

- **What the token buys: not established.** Nothing in the slice is priced in TAO. Lium prices in
  USD per GPU-hour, Chutes in USD a month for Plus at USD 10 and Pro at USD 20.
- **The minimum stake or registration cost: not established.** No record states a TAO stake, a
  registration fee, a burn or a token conversion.
- ⛔ **Whether the free compute is paid for in token acquisition: not established.** The two
  credits that exist, at Lium and Targon, are priced in USD and granted against an email or a
  card. Calling that a token subsidy would be a claim the records do not support.

## The free inference lanes

Ten records price tokens rather than cards, and `../../inference/README.md` owns the class. They are
named here because they compose with the GPU lanes and because three are refutations a reader will
meet in a roundup.

| Lane | Free quantity | Identity | What fails first | Verdict |
| --- | --- | --- | --- | --- |
| `cerebras-inference` | USD 5 for 30 days | card | the expiry; USD 5 is about 6.7M output tokens | trial-only |
| `voyage-ai` | 200M tokens on the voyage-4 family, 50M on older ones | email | a lifetime allowance; one re-embed consumes it | trial-only |
| `alibaba-cloud-model` | 1,000,000 tokens per model, 90 days | any phone, and probably a card | the 90-day expiry and a per-model pool that does not move | trial-only |
| `fireworks-ai-muse` | one free LoRA fine-tune on one 30B base model | email, no card | the window closes 2026-11-30, and only training is covered | trial-only |
| `io-net-intelligence` | a daily token allowance per model, size unpublished | email | the size is not published outside a login-gated table | qualifies-with-caveat |
| `mistral-la-plateforme` | free mode, three limit dimensions, no figure | any phone | no public page states the monthly cap | qualifies-with-caveat |
| `deepseek-api` | none | email | the first balance; USD 0.15 per 1M input off-peak | paid-only |
| `chutes` | none; the 200-request lane ended 2026-03-15 | email | the first balance | paid-only |
| `sambanova-cloud` | none; the USD 5 grant dropped 2026-08-14 | card | a 402 on the first call while `/v1/models` answers 200 | fails-identity |
| `hugging-face-inference` | none; free users read None in the credit table | email | the first credit purchase; PRO is USD 2.00 a month | paid-only |

⚠ **Three are the trap this corpus exists to catch.** Cerebras' model pages still print a
free-tier rate limit that its FAQ denies. SambaNova's rate-limit page still describes a free tier
its plans page removed, so a health check on the model list returns 200 while every completion
returns 402. Mistral's retired Experiment plan is still quoted as 1 billion tokens a month.

## What the class does not give

**No persistent storage.** The only exceptions are AMD Radeon Cloud's 25 GB `/workspace` and
ModelScope Notebook's files under `/workspace`, both alive only while the account is. AMD
Developer Cloud destroys the VM and its data at expiry, and a Lium volume is billed from the same
USD 5 at USD 0.00005 per GB-hour, detached or not.

**No long-running training at these credit levels.** Akash closes a deployment at 24 hours, Lium's
credit expires at 14 days, and AMD's at 30 days with the data. Four lanes cap one boot at 12 hours
or less: AtomGit at 2, ModelScope at 10, ModelScope Notebook at 8 to 10, molab at 12.

**No datacenter card for a usable duration on a trial tier.** Akash excludes every card above the
RTX 3090. Lium's USD 20 an hour cap excludes every 8-GPU H100 and B300 node and reaches one H100
for 1.3 to 2.5 hours. AMD's 50 MI300X hours are the exception, behind a discretionary allocation.

**No supply guarantee and no measurement.** Only one of the seven cards on Nosana's homepage has a
free host, and the cheapest has none. Lium had 85 GPUs available across 16 nodes on a feed of
1,692. No record here carries the `measured` rung, so the gap between a published rate, an offer
and an invoice is unobserved.

## What is closed

| Entry | What the page still says | Why it is not capacity |
| --- | --- | --- |
| `amazon-sagemaker-studio` | the docs page is live | quoted: Studio Lab is no longer open to new customers |
| `salad` | GPUs from USD 0.015 an hour | quoted: no free trial; the only credit is for qualifying companies |
| `clore-ai` | RTX 3090 around USD 0.37 an hour | a deposit of about USD 5, paid in CLORE, BTC, USDT or USDC |
| `render-network` | EUR 50 in free credits | quoted: the offer has concluded; a licence is now required |
| `green-compute` | RTX 4090 and 5090 by the minute | indicative prices and a negotiated enterprise contract |
| `ai-grant` | USD 5,000 to USD 50,000 in grants | no apply link, and the page matches its 2025-05-21 capture |

⚠ **`ai-grant` is dormant, not closed.** The three latest awards are 2023-era projects, so this is
a page that stopped moving, which is the quietest way for a programme to end. And `aethir`'s USD
10,000 is real and belongs to a partner team: the application form comes first, then a national
identity check through ComPilot and Sumsub before funds move.

## What would change the answer

- **An Akash live offer count.** The rate comes from two price indexes and neither states free
  hosts, so one query moves 6.7 hours from a rate-card figure to a supply figure.
- **A Vast.ai probe recorded as `measured`.** The bundles API already returns 64 offers with
  prices, which would give the class its only benchmark and its first non-`documented` rung.
- **The AMD allocation rate.** If the USD 100 reaches a plain individual more often than not, tier
  2 is real and the class is USD 106. If not, tier 1 stands at USD 6.
- **Lium's grant on a second IP address.** The outcome is reported by `signup_credit_granted`, so
  one call settles whether the grant is per person or per address.
- **A TAO price or a registration cost on any subnet page.** The Bittensor section is three
  refusals today, and it is the largest unanswered question in the slice.

## Record index

| Group | Records |
| --- | --- |
| credit lane | `akash-network`, `lium`, `nosana`, `amd-developer-cloud`, `ocean-network`, `aethir` |
| concluded or closed credit | `render-network`, `ai-grant`, `amazon-sagemaker-studio` |
| free GPU without a credit | `amd-radeon-cloud`, `modelscope`, `modelscope-notebook`, `atomgit-notebook`, `molab` |
| free GPU behind an identity gate | `baidu-paddlepaddle-ai`, `baidu-ai-studio`, `geant-testbeds-service`, `green-compute` |
| no free lane, priced in USD per hour | `vast-ai`, `salad`, `targon`, `clore-ai`, `gongji-compute-individual`, `intel-developer-cloud`, `gensyn` |
| token lanes | `cerebras-inference`, `voyage-ai`, `alibaba-cloud-model`, `fireworks-ai-muse`, `io-net-intelligence`, `mistral-la-plateforme`, `deepseek-api`, `chutes`, `sambanova-cloud`, `hugging-face-inference` |

The 35 records are 7 `fails-identity`, 11 `trial-only`, 7 `paid-only`, 5
`qualifies-with-caveat`, 2 `fails-quota`, 2 `dead` and 1 `qualifies`. Eleven carry
`binding: write-gated` and ten carry `binding: retention-clamped`, so the two constraints that
decide 21 of the 35 rows, or 60 per cent of the slice, are a form and a clock rather than a quota.

## How it composes

This class supplies the hour and never the place, so the chain is always the same: rent at the
cheapest lane with supply, push checkpoints to a storage provider that does not expire, and
destroy the instance rather than stopping it. The lane to start with is `amd-radeon-cloud`,
because it is the only free allowance here that is not a one-time credit: 20 points a day,
redeemable in slices, on a ROCm container with SSH and a persistent volume, beside an inference
endpoint that serves 16 public free models.

⛔ **Checkpoint to storage, not to instance disk.** AMD destroys the data at expiry, Lium bills
every read from `/mnt` and every download per GB, AtomGit wipes the filesystem at 2 hours, and
Vast's disk is on a third party's machine with `survives_destroy: false`.
