# The free tier that actually opens, and what it costs in identity

The question is whether a provider places a hold of about USD 50 on a credit card. Measured across the
**3,984 records** in `dossier/`, **no provider places a USD 50 hold.** The largest anywhere is
**Koyeb's USD 29**, cancelled at once and released over 7 to 21 days, and Koyeb takes a
prorated Pro charge at the same moment. The typical hold is
**USD 1**: Oracle, Tencent, Linode and Alibaba each publish that figure, CloudCone states
"usually about $1", and Google's authorisation is USD 0.00. The only pre-authorisation of
USD 15 or more in those records is Koyeb's USD 29; every other amount that size sitting beside
a hold word is a credit, a plan price or a top-up minimum, not money taken from the card.

Three figures look like the USD 50 fear and are something else. **Tenki's USD 50** is credit
released when a payment method is added, and its card terms are not stated (`tenki`).
**Isorun's USD 50** is an advertised credit whose pricing page would not render for a text
read, so it is `unverified` (`isorun`). **Oracle's USD 100** belongs to the upgrade to Pay As
You Go, not to signup; signup authorises USD 1.00 on Oracle's own billing page.

So the answer is three machines and one credit, and the split is identity and a clock rather
than price.

**1. The largest free machine with no card is a CI runner, and it is bigger than any free VM
here.** GitHub Actions on a public repository gives a **4 vCPU / 16 GiB / 14 GiB** VM with a
shell and a network, and GitHub states that "use of the standard GitHub-hosted runners is free
and unlimited on public repositories" (`github-actions`). A verified email is the whole
identity cost: no card, no phone, no document. One 6-hour job is 96 GiB-hours of RAM; four
back-to-back jobs are 384, against Oracle's 288 for its 12 GiB at 24/7.
⛔ **The reap is a clock and it is not money.** A job is terminated at 6 hours and the VM dies
with it; there is no inbound port and no disk that outlives the job, so a service cannot live
there and a scheduled workload that pushes its state out can. The cron floor is 5 minutes, and
GitHub disables a scheduled workflow on a public repository after **60 days without repository
activity**, which ends an unattended job silently. GitHub Codespaces gives 2 cores for 120 core-hours a month, which is 60 hours at that shape and
then stops (`github-codespaces`); the runner above has twice the cores and no monthly cap.

**2. If it must hold a port, the machine in this corpus is a German container with no IPv4.**
EUserv's VS2-free is a permanent free root server on the Linux-container platform: **1 core at
1 GHz, 1 GB of RAM, 10 GB of HDD and 1 TB of traffic a month**, free with IPv6 (`euserv`).
The gate is the address family, not money. The free model ships **one /128 and no IPv4**, and
IPv4 is sold as an extra, which turns the free tier into a paid one at a published per-IP
rate. The record's identity is `email`; its signup form was not read, so a card at checkout is
`unverified` rather than absent.

**3. The credible always-on machine with a routable address needs a card, and then it is
paid.** No provider in this corpus sells an always-free VM with a routable IPv4 to an adult
with an email address. Every always-free machine here that takes no card is IPv6-only,
clocked, ephemeral or age-gated, and the four are named below. That is a result for this
corpus, not a market census: it rests on the 3,984 records and on no signup attempt.
Tencent Cloud International's Lighthouse `2 vCPU / 2 GiB / 40 GB` is **USD 10.08 for the
first year, USD 4.20 a month at renewal**, behind a USD 1.00 pre-authorisation and no document
outside the Chinese Mainland (`tencent-lighthouse-intl`). That is the closest thing to a
credible free-tier replacement for a reader without a card.

**A USD 200 credit is a different thing from a machine, and it is not one that can be kept.**
Daytona gives **USD 200 one-time** on a verified email, which at its own rate card is **749
hours, or 31.2 days, of a 4 vCPU / 4 GiB / 10 GiB VM**. The arithmetic:
`4 x USD 0.0504 + 4 x USD 0.0162 + 5 x USD 0.000108 = USD 0.26694 an hour`, and
`730 x 0.26694 = USD 194.87`. At the maximum 8 GiB shape the month costs USD 242.17, so the
credit covers a month at 4 GiB and does not cover one at 8 GiB.
⛔ **The catch is egress, not money.** Tier 1 outbound is restricted to an unpublished
"essential services" list and cannot be overridden; full internet starts at Tier 3, which
needs a USD 500 top-up. A month of machine time that cannot reach most of the internet is
a sandbox, not a daily driver.

## The card, and what it holds

This table answers the question.
A hold is not a charge, and an unpublished hold is not zero. Every row names its record, and a
cell that reads `not established` means the record does not carry the fact. It does not mean
the provider asks for nothing. **Eleven rows state an amount, ten carry a card with no
published amount, and three take no card.** One of the eleven is above USD 10.

| provider | card at signup | hold | debit stated | prepaid | phone or ID | record |
| --- | --- | --- | --- | --- | --- | --- |
| Koyeb | yes | **USD 29** plus a prorated Pro charge | accepted | not stated | card | `koyeb` |
| Fly.io | after a 2-hour trial | **under USD 10** | not stated | refused as a saved method; accepted to buy credits at a USD 25 minimum | none stated | `fly-io` |
| Oracle Cloud | yes | **USD 1.00, published** | accepted; PIN debit refused | **refused** | **phone** | `oracle-cloud` |
| Google Cloud | yes | **USD 0.00, published** | accepted; two-factor debit refused | **refused** | name, address and card; phone for the trial | `google-cloud-free-tier` |
| Linode / Akamai | yes | **USD 1** | accepted | not stated | none stated | `linode` |
| CloudCone | not established | **usually about USD 1**, on adding a card, refunded within 7 days | accepted | not stated | not established | `cloudcone-ssd-vps-1` |
| Contabo | yes | **EUR 1** | not stated | not stated | none stated | `contabo` |
| Scaleway | yes | **EUR 1** | not stated | **refused** | email and phone | `scaleway` |
| DigitalOcean | yes | not published; may show for up to 7 days | accepted | **refused** | card | `digitalocean` |
| IONOS | yes | small test charge, amount not published | not stated | not stated | none stated | `ionos` |
| Kamatera | yes, for the trial | not published | accepted | **accepted** | email and card | `kamatera` |
| IBM Cloud | yes | not published; reversed in 24 to 72 hours | accepted, Visa or Mastercard only, no disposable number | **refused** | email, then card | `ibm-cloud` |
| Alibaba Cloud Intl | yes | **USD 1.00, published** | accepted with international payments enabled | **refused** | phone; KYC only on a risk-control block | `alibaba-cloud-international` |
| Tencent Cloud Intl | yes | **USD 1.00** | accepted; some card brands excluded | **disputed** | none outside the Chinese Mainland | `tencent-lighthouse-intl` |
| Vultr | yes | **USD 0.00** verification deposit; a small hold of unpublished size is possible | accepted | not stated | email, then a payment method | `vultr` |
| Hetzner | yes | not published | not stated | not stated | **an ID document or an advance card payment, at its discretion**; paid email domain | `hetzner` |
| netcup | yes | not stated | not stated for a card; Direct Debit, bank transfer and PayPal are listed | not stated | none stated | `netcup`, `netcup-vps-1000` |
| OVHcloud | yes | not published | accepted | not stated | none stated | `ovhcloud` |
| BuyVM | yes | not stated | not stated | not stated | none stated | `buyvm` |
| AlphaVPS | yes | not stated | not stated | not stated | none stated | `alphavps` |
| HostBrr | yes, at order | not stated | not stated | not stated | none stated | `hostbrr`, `hostbrr-value-8gb` |
| AWS Free plan | **no, for most new customers** | not applicable | not applicable | not applicable | email or an existing Google or GitHub sign-in; "additional verification" at AWS's discretion | `amazon-web-services-free-tier` |
| EUserv VS2-free | **no**, per the record's `email` identity | not applicable | not applicable | not applicable | email; a postal address may be required | `euserv` |
| Daytona, E2B, Render, Freestyle Free, GitHub Actions, IBM LinuxONE, SparkCloud | **no** | not applicable | not applicable | not applicable | email | `daytona`, `e2b`, `render`, `freestyle`, `github-actions`, `ibm-linuxone-community`, `sparkcloud` |

Five rows are outside the 2026-10-24 payment read: CloudCone, netcup, BuyVM, AlphaVPS
and HostBrr. CloudCone's hold is quoted from its own help centre and attaches to adding a card
rather than to creating an account; the other four records carry no payment statement at all.

**Prepaid is the rail a reader with no credit history has.** Seventeen vendors' own payment pages were read on
2026-10-24. Sixteen of them take a card; the seventeenth, AWS, takes none for most new
customers. Of the sixteen:

- **Seven refuse a prepaid card outright, in writing.** DigitalOcean: "We do not accept
  virtual, electron, or prepaid cards." Google Cloud: "Prepaid cards aren't accepted for
  payment." Scaleway: "Virtual and pre-paid credit cards are not accepted." Alibaba Cloud:
  "Prepaid, gift, virtual, and UnionPay-only cards are not supported." Oracle: "We do not
  accept debit cards with a PIN or virtual, single-use, or prepaid cards." Fly.io: "You can't
  use a prepaid card as a default (or saved) payment method." IBM Cloud refuses "disposable"
  and "one-time use" numbers.
- **One accepts it unambiguously.** Kamatera: "This includes virtual, prepaid, and electronic
  cards."
- **One is disputed.** Tencent Cloud's billing FAQ refuses prepaid and virtual cards while its
  registration document states "Seven types of credit cards/debit cards/prepaid cards are
  supported". Two first-party pages contradict each other and the record keeps both.
- **Seven publish nothing.** IONOS, Contabo, Vultr, Linode, Hetzner, OVHcloud and Koyeb.

Debit fares better, and it is the rail to plan on. **Eleven of the sixteen accept a debit
card**, five of them with a condition: Oracle refuses PIN debit, Google refuses a debit card
that needs two-factor authentication, IBM refuses anything that is not Visa or Mastercard,
Alibaba needs international payments enabled on the card, and Tencent warns that some card
brands do not support debit. The other five never say.

⚠ **A vendor's silence is not permission.** The seven silent rows are silent, not permissive,
and a prepaid card is refused at checkout by providers whose own page never mentions it. Civo
carries the same refusal for virtual and prepaid cards in its record, but no first-party
quotation behind it, so it is not counted here (`civo`).

## The free tiers that are not credible

| row | why it fails | record |
| --- | --- | --- |
| Koyeb free instance | card required, **USD 29 hold**, and a prorated Pro plan is charged on the way through | `koyeb` |
| Modal USD 30 monthly | card required at signup | `modal` |
| Fly.io free tier | withdrawn for new organisations; the product lives and the free tier does not | `fly-io` |
| Render free web service | spins down after 15 minutes idle and the filesystem goes with it; no shell on the free plan | `render` |
| alwaysdata free | the footnote forbids running services, so a listener is out of scope | `alwaysdata` |
| Blinkenshell | five-step signup ending in an SMS to a mobile number | `blinkenshell` |
| tilde.team | the host was rooted and `rm -rf /` was run; SSH is disabled | `tilde-team` |
| Northflank Sandbox | **card-gated.** The plan card says "No card needed" and the billing docs say "all users must add a payment method to start creating resources on Northflank, regardless of plan selection". The contradiction is inside one page, and the docs govern | `northflank` |
| Lightning AI | the pricing page still advertises "Run 1 Studio free 24/7. No credit card."; the security-incident page and the status banner say the platform remains inaccessible | `lightning-ai` |

The Lightning row is the one to read twice. The pricing page was read on 2026-10-24
and would reverse the `dead` verdict to `qualifies`. The operational pages read the same
hour refute it: the incident notice of 2026-10-15 is still active and the status banner still
reads "Service is down". A marketing page that was not updated is not evidence of a service,
and the record keeps `dead`.

## The sandbox class, for completeness

A sandbox is not a daily driver and it is not a VPN node, but a few of them are a real VM
with root for the price of a coffee, so they are recorded rather than dropped. Each was read
at the vendor's page on 2026-10-24.

| provider | price | shape | what it is | record |
| --- | --- | --- | --- | --- |
| CoolVDS | USD 4.00 a month | 1 vCPU / 512 MB / 10 GB NVMe, 1 TB | microVM, monthly reservation | `coolvds` |
| PillDrops | USD 3.00 for 30 active hours | 2 vCPU / 4 GiB / 10 GiB | 30-hour allowance, 4 h and 24 h session caps | `pilldrops` |
| SimpleSandbox | USD 1 a month of credit, no card | shape not published | USD 0.0252 per vCPU-hour | `simplesandbox` |
| unsandbox | USD 7.00 flat | 1 vCPU / 2 GiB | 7 requests a minute is the binding limit | `unsandbox` |
| Tembo Computer | USD 77.82 a month at 24/7 | Nano, 2 vCPU / 2 GiB, full VM | a real VM at a real price | `tembo-computer` |
| DeepInfra Sandboxes | USD 39.42 a month | shape behind an authenticated catalogue | 24-hour auto-stop | `deepinfra-sandboxes` |
| Mitos | USD 42.34 a month at 24/7 | 1 vCPU / 1 GiB | USD 100 of credit, no card at signup, then prepaid top-ups | `mitos` |

CoolVDS is the only row in this table under USD 5 that is a microVM with a monthly
reservation, and 512 MB is its ceiling. Krova Cloud is the better sub-USD-5 microVM and is
priced in [`../paid/under-five.md`](../paid/under-five.md).

⚠ **CoolVDS cannot be bought on 2026-10-24.** Its order page reads "All Slots Currently
Occupied" and offers a waitlist instead of an order button, so the price is real and the
capacity is not (`coolvds`).

## What the archive says about these offers

A capture from about twelve months ago, compared against today's page for twelve of the
providers above, separates a stale corpus claim from a durable one. Six are materially
unchanged, two raised a limit, three cut one, and one cannot be settled from the archive.

| provider | a year ago | today | change |
| --- | --- | --- | --- |
| Oracle Cloud | A1: 3,000 OCPU-hours and 18,000 GB-hours = 4 OCPU / 24 GB, four instances | 1,500 and 9,000 = 2 OCPU / 12 GB, two instances | **cut** |
| Koyeb | free service plus a 5-hour Postgres; no card for the free Instance | same free service; **card mandatory, USD 29 hold** plus a prorated Pro charge | **cut** |
| Modal | USD 30 a month, no stated exclusion | USD 30 a month of compute, Shared Endpoints excluded from 2026-09-01 | **cut** |
| Northflank | Free sandbox, "Limited resources", no USD figure | Free sandbox with **USD 20 a month of resources, always on, no sleeping** | **raised** |
| Railway | trial USD 5 for 30 days, then USD 1 a month at 0.5 GB / 1 vCPU | Free USD 1 a month; **Free Trial 1 GB / 2 vCPU** | **raised** |
| Google Cloud, Codespaces, Colab, Workers, Daytona, Render | — | identical text, word for word | same |
| Kaggle | no recoverable text | 30 GPU hours a week | unverified |

⭐ **The Oracle cut is the one to know about.** Oracle halved the Always Free ARM allowance
between 2026-06-03 and 2026-06-30 with no announcement, and the corpus caught up on
2026-10-22, four months later. That is the failure mode: not a
wrong number, a late one.

⚠ **Koyeb is the one that changed what it costs to start.** The free instance is
byte-identical and still exists; the price of entry moved from no card on the free Instance to
a mandatory card with a USD 29 hold. A reader who checked a year-old guide would meet a USD 29
authorisation on a free tier.

## The notebook tier, which is compute for a job rather than a host

Notebooks are in scope because they run a shell and a GPU for nothing. They are not
servers: the session dies with the tab unless the platform has a headless submit.

| provider | free allowance | shape | survives the tab | record |
| --- | --- | --- | --- | --- |
| Kaggle Notebooks | 30 GPU hours a week, "or sometimes higher depending on demand"; 12 h per session | 4 cores, 30 GB; P100, T4 or TPU, not promised | **yes**, `Save & Run All` runs it headless | `kaggle-notebooks` |
| Google Colab | **not published**, by the vendor's own statement | unpublished; 12 h cap; remote control such as SSH disallowed | no | `google-colab` |
| Google Cloud Shell | 50 hours a week | unpublished; a 40-minute cut for non-interactive sessions | no | `google-cloud-shell` |
| molab (marimo) | no monthly cap published | 4 CPU, 32 GB, RTX Pro 6000 | no | `molab` |
| Paperspace Gradient | no monthly hour cap published; a 12-hour auto-shutdown per session | M4000, 5 GB disk | no | `paperspace-gradient` |
| Posit Cloud | 25 hours a month | 1 CPU, 1 GB | no | `posit-cloud-free` |
| Deepnote | unlimited machine time | 2 vCPU, 5 GB | no | `deepnote-free` |
| Hex | no cap published | 0.5 CPU, 4 GB | no | `hex-community` |
| CoCalc | free plan | not established | no | `cocalc-free` |
| Observable | **0 minutes of compute a month**; 50 on Pro | not established | no | `observable-free` |
| DataCamp Workspace | free plan | not established | no | `datacamp-datalab-free` |

Three rows left this table on 2026-10-24, because the records settle them against the free
tier. Noteable serves an Afternic listing that reads "noteable.io is for sale!", so the service
is gone (`noteable`). Quarto Pub reads "Quarto Pub is closed to new sign-ups", and it published
rather than computed (`quarto-pub`). Valohai sells two per-seat tiers, Pro and Enterprise, and
publishes no free plan (`valohai`). Each stays recorded as it is, and none of the three is a
free notebook today.

Observable is a settled negative and not an open question: the Free column of its plan table
gives Compute nothing at all, against 50 minutes a month on Pro (`observable-free`).

The one that matters is Kaggle, because it is the only free notebook in this table with a
documented headless submit. Phone verification gates the GPU, and that requirement is on
Kaggle's forum rather than its docs, so it is `reported` rather than `documented`.

## The real machines, and why each one fails

**Oracle Cloud Always Free is the largest free machine in this document that stays up with a
routable address, and it is not free of identity.** 2 OCPU and 12 GiB of Ampere A1, two 1 GB
AMD micro instances, 200 GB of block volume and 10 TB a month out, with no expiry and a
seven-day p95 reclaim test. It needs a card and a phone, it refuses prepaid, single-use and
PIN-debit cards, and **it publishes the hold: USD 1.00 authorised at signup**, reversed
immediately on Oracle's side while the bank decides how long the release takes
(`docs.oracle.com/en-us/iaas/Content/Billing/Tasks/changingpaymentmethod.htm`, read
2026-10-24). The USD 100 is the Pay As You Go upgrade and not signup. Oracle's own billing page states the USD 1. Its capacity
is also regional: Oracle documents an "out of host capacity" error and offers a paid upgrade
as the workaround, so entitlement is not availability.

**Google Cloud's e2-micro is smaller and more honest.** One instance in three US regions,
0.25 sustained vCPU and 1 GiB, 30 GB of disk, and **1 GB of egress a month**, which is the
number that ends it. The authorisation is published at **USD 0.00**: "you might notice a
$0.00 transaction from Google on your bank or credit card statement. These are authorization
requests only, not actual charges", which a bank may show as pending for 1 to 14 business
days (`google-cloud-free-tier`). No Google billing page states a USD 1.00 upper bound.
IBM Cloud is the opposite case: it publishes the reversal window, 24 to 72 hours, and not the
amount (`ibm-cloud`). The always-free shape is contingent on a billing
account in good standing, and the USD 300 trial is a separate allowance: when a trial account
closes, "all of its associated projects and resources will be stopped".

**Tencent Cloud International is the largest free server in this slice that still asks for a
document.** A 2 vCPU / 2 GiB Lighthouse for a 3-month trial, and the gate is a government
document: individual verification accepts a passport, ID card, driving licence or work permit
from the registration country and takes two to four business days (`tencent-cloud-international`).
The record states no egress term for the trial, so the transfer allowance is `unverified`
rather than absent.

**Huawei Cloud International has no free server at all.** The international free-packages page
serves "This page is no longer available", and the surviving terms still claim 12 months of
free usage on products that no live page enumerates (`huawei-cloud-international`). A
third-party review reports that the 2026 list carried only management and security services,
with no ECS, EVS or OBS. That is `reported` and not confirmed, because the campaign page is
gone.

**IBM Cloud is the gate that is neither a card nor a document.** Its only card-free account is
a Trial that needs institution credentials, and every other account is Pay-As-You-Go from
registration with a card held for identity verification (`ibm-cloud`). A reader with no
institution has that door shut before the card is discussed.

**Four machines here are free, real and need no card, and each is gated on something that is
not money.** EUserv's VS2-free is a permanent root container with 1 GB of RAM and 1 TB a
month, and its gate is IPv6-only addressing (`euserv`). IBM's LinuxONE Community Cloud gives a
free s390x VM with full root for up to 120 days, with "no cost, no credit card"; the shape is
`reported` at 2 cores and 4 GiB rather than documented, because IBM's own pages state the term
and not the size (`ibm-linuxone-community`). GitHub Actions is a 4 vCPU / 16 GiB machine for
six hours at a time with no inbound port (`github-actions`). SparkCloud, run by a 501(c)(3),
gives root containers and SSH with no card at all, and "Sparkden is for teenagers. Every
account is age-verified" (`sparkcloud`).

⭐ **The claim that survives is narrower and it is the useful one.** Every always-free machine
in this corpus that takes no card is IPv6-only, clocked, ephemeral, or gated on something that
is not money. No provider in this corpus sells an always-free VM with a routable IPv4 to an
adult with an email address. The earlier claim was false on four counts, because it silently
scoped itself to a VM with a routable address among the clouds a listicle names.

## The credit rows that are a plan, not a grant

The largest no-card balances are not all the same product, and three of them are a
subscription's included usage rather than a grant. This matters because a reader who plans
against "USD 100 free" and finds a USD 299 plan behind it has planned for the wrong thing.

| provider | what the number actually is | the machine it buys | record |
| --- | --- | --- | --- |
| Daytona | USD 200 one-time wallet credit, no card, Tier 1 on a verified email | 749 hours, 31.2 days, of 4 vCPU / 4 GiB / 10 GiB | `daytona` |
| HopX | USD 200, and its largest shape and timeout ceiling are unpublished | 2,955 hours at 1 vCPU / 1 GiB | `hopx` |
| Prized | USD 30 | 2,143 hours at 2 vCPU / 2 GiB, or 2.9 months at 24/7 | `prized` |
| Tenki | **USD 50 at signup and USD 50 only when a payment method is added** | 302 hours at 2 vCPU card-free, so 12.6 days | `tenki` |
| Koyeb | USD 100 is **included compute on a USD 299 a month plan**, not a grant | n/a without the plan | `koyeb` |
| Lizard | USD 19 on a USD 19 plan | n/a without the plan | `lizard` |
| Beam | USD 20 on a USD 20 plan | n/a without the plan | `beam` |
| boat | USD 20 of time, lapsing monthly | n/a | `boat` |
| Blaxel | "up to USD 200", and a Tier 0 sandbox **expires at 7 days** | 7 days, whatever the balance | `blaxel` |
| E2B | USD 100 one-time, **one hour per session** | 604 hours, split into at least 604 sessions | `e2b` |

⭐ **A session cap beats a credit.** E2B's USD 100 is 604 hours and those hours must be split
into at least 604 sessions of an hour or less, so a 730-hour month is impossible on the free
tier whatever the balance. Blaxel's Tier 0 expires at seven days. Vercel Sandbox caps a Hobby
session at 45 minutes (`vercel-sandbox`), Railway's sandbox class at 5 minutes (`railway`),
and a Fly trial Machine at 5 minutes (`fly-io`). A credit is only a machine if the clock allows
the machine.

⛔ **The one credit that carries four cores through a full month without a card.** Daytona at
4 vCPU / 4 GiB is 749 hours on an email alone, which is 31.2 days. GitHub Actions has more
cores and more hours and is not a credit: it is a 6-hour job, four of which make a day. This
sentence is therefore about a machine that stays up, and Daytona is the only no-card row here
that does. The scope is those records: HopX buys 2,955 hours at 1 vCPU / 1 GiB and Prized
2,143 hours at 2 vCPU / 2 GiB, and neither reaches four cores (`hopx`, `prized`). It is also
the row with the restricted egress, so the month is real and the daily driver is not.

## The rule

**Read the billing page, not the pricing page.** Every false "no card" claim is
on a pricing page, and every true one on a billing or signup page. **Read the status
page, not the product page.** A platform can be down for eight days while its marketing page
sells the free tier. **Convert the credit to hours at the vendor's own rate card**, because
"USD 200 free" means 31 days at one shape and 25 at another.

⛔ **No account was created on any of these providers, so no row is `measured`.** The rows are
`documented` where a first-party page states the fact, and `reported` where only a third party
does. What would settle the most load-bearing rows: one Daytona signup to see
whether Tier 1 can create a VM sandbox at all, one Koyeb signup to see the USD 29 hold on a
statement, one Oracle tenancy held for eight days to watch the reclaim test, and one prepaid
card offered at Tencent Cloud to see which of its two first-party pages the payment processor
enforces. The hold table itself needs no probe to be read correctly; it needs the billing page
rather than the pricing page, which is how the sixteen vendor rows in it were read on
2026-10-24.

The rows above are records in `dossier/compute/`. The paid side of the same question, and
what a debit card buys under USD 5, is [`../paid/under-five.md`](../paid/under-five.md).
