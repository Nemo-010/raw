# Clouds and VPS as exit sources

Every cloud and VPS host is an exit source, because every one of them hands out a
public address. The question this document answers is not whether an address is
available. It is **which ASN that address is in, and whether a second one can be
had.**

**The answer:** a cloud buys rung 4 and refuses rung 5. Every free tier measured
here sits in the provider's own datacenter ASN, and the ASN is per *location*, not
per host. Four of the nine hosts surveyed do not even announce their own space.
The useful finding is not the price, which the `compute` topic already owns. It is
the ASN field, which the `compute` records do not carry.

---

## The measured ASNs

Every row was resolved with `stat.ripe.net/data/prefix-overview` and confirmed with
RDAP on 2026-10-24.

| provider | ASN | holder | announced v4 prefixes | free tier | the catch |
|---|---|---|---|---|---|
| Oracle | **AS31898** | ORACLE-BMC-31898 Oracle Corporation | 3,861 | 1,500 OCPU-h + 9,000 GB-h/mo, 10 TB/mo egress | card, USD 1.00 reversal; **7-day idle reclaim** |
| Google Cloud | **AS396982** | GOOGLE-CLOUD-PLATFORM Google LLC | 3,558 | e2-micro, 1 GB/mo egress | the address costs USD 3.65/mo |
| AWS | **AS16509** | AMAZON-02 Amazon.com, Inc. | **19,507** | 750 public-IPv4 hours | the largest pool here, and the same one ASN |
| Azure | **AS8075** | MICROSOFT-CORP-MSN-AS-BLOCK | 1,233 | USD 200 credit, 30 days | `/29` prefix exists, **price unreadable** |
| Hetzner | AS24940 | Hetzner Online GmbH | — | none | sells a contiguous `/29` |

⚠ **The prices and free-tier limits in this table are `compute`'s facts, not this
topic's.** [`../../compute/README.md`](../../compute/README.md) owns them and
`dossier/compute/` carries the records. This table exists only to attach the ASN
and the registration class, which the `compute` records do not carry. Where the two
disagree, `compute` is right.

⚠ **AWS's prefix count moved inside one day**, from 19,507 to 19,416 between two
reads. Treat the column as an order of magnitude.

⛔ **A bigger pool is not more diversity.** AWS announces 19,507 IPv4 prefixes and
all of them are Amazon's. An upstream counting ASN sees one caller.

⚠ **Azure's `/29` price is `unverified`.** Every price cell on
`azure.microsoft.com/en-us/pricing/details/ip-addresses/` renders as `$-`, because
the figures are injected by script. A reader who needs that number must use the
Azure calculator.

---

## The ASN is per location

⭐ **Sometimes the address is not the host's at all.**

| host | its own ASN? | where its traffic actually leaves |
|---|---|---|
| **RackNerd** | **no ASN at all** | AS35916, AS198566, AS40676 across its published test IPs |
| **DediRock** | **no ASN at all** | AS36352, AS40676 |
| **VolpaByte** | — | its Frankfurt location exits from **AS24940 Hetzner** |
| **Datalix** | AS218841, which announces **zero prefixes** | AS58087 |

⛔ **Any record that writes one ASN for a multi-location host is a defect.** The
`compute` topic's 1,411 records carry no ASN field at all.

⚠ **A "cheap VPS" is not a distinct network just because the brand is different.**
Four of the nine hosts surveyed are reselling somebody else's transit.

---

## The two hosts whose egress is genuinely not their own datacenter

Of the hosts advertising a residential or ISP address, two survived a registry
check. Both are in the paid lane because neither is free, but they belong here
because they are VPS products rather than proxies.

| host | the address | RIPE says | verdict |
|---|---|---|---|
| **RareCloud** Constanța residential | its published test IP | **AS39347 SELL-07INTERNET-RO** — an ISP registrant | ✅ passes |
| **VPC.KR** Korea native | `112.169.175.10` | **AS4766 KORNET-KR** Korea Telecom, portable allocation | ✅ passes |

⚠ **Both have a catch that matters more than the class.** RareCloud's residential
product is **out of stock** (`0 Available`) and the host states there is no IPv6 at
that site. VPC.KR is USD 5.80/month for one address.

⛔ **And four of the six vendors selling an ISP or residential claim failed:**

| vendor | RIPE says | why it fails |
|---|---|---|
| NovixLink (NTT line) | AS2914 NTT America | a transit carrier, not an eyeball network |
| NovixLink (GTT line) | AS3257 GTT-BACKBONE | the same |
| CStoneCloud | AS174 Cogent / AS3257 GTT | the same |
| K.PL | AS35179 KorbankDC | a datacenter |
| DeluxHost Amsterdam | AS834 IPXO | a lease broker |

⭐ **A 2-of-6 pass rate is the finding of the paid lane**, and it is why every
record in this topic carries `extras.rung`.

---

## The providers

<!-- generated:start topic=ip-proxy kind=provider verdict=fails-egress sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Oracle Cloud, Google Clou... | Oracle Always Free includes 1,500 OCPU-hour... | fails-egress | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/clouds-as-exit-sources.json` |
| IPPeak | No free tier. The ISP Proxies plan is sold... | fails-egress | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/ippeak-dual-ntt.json` |
<!-- generated:end -->

## What to do with a cloud address

| if the upstream keys on | a cloud helps | why |
|---|---|---|
| rung 2, the address | ✅ yes | a fresh VM is a fresh address |
| rung 3, the subnet | ⚠ maybe | a `/29` is a different block, but still one block |
| rung 4, the ASN | ❌ no | every cloud is one ASN, and a bigger pool is not a new one |
| rung 5, the class | ❌ no, except RareCloud and VPC.KR | datacenter registration |

⚠ **Oracle's free tier is the best free rung-2 source here and it is also the
one most likely to disappear.** Its own documentation: *"Oracle will deem virtual
machine and bare metal compute instances as idle if, during a 7-day period"* CPU
p95, network and memory are each *"less than 20%"*. An egress node
that is idle most of the day is exactly what that rule removes. The record carries
`retention-clamped` for that reason.

⭐ **Hetzner's `/29` is worth one number.** EUR 13.60/month plus EUR 34.90 setup
for six usable addresses is **EUR 2.27 per address per month**, which is 8 to 11
times the per-address price of Contabo and 56 times IPXO's campaign rate. It buys a
contiguous block, which is the opposite of what a subnet-counting gate punishes.
