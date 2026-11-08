# The Q1 winner's month 13 is unknown, the Q2 winner never promised UDP, and the USD 50 hold does not exist

- **When:** 2026-10-24T03:30:00Z
- **Status:** corrected
- **Supersedes:** the Q1 recommendation (GreenCloudVPS at USD 3.75 as a daily driver), the Q2 recommendation (Gullo's at USD 0.29 for a WireGuard node), the Q3 lead (Daytona as the biggest no-card machine), and the Q3 negative "no always-free VM without a card"
- **Superseded by:** four research lanes that read vendor pages after the review pass: `.tmp/compute-2026-10-24/widen/W1/report.md` (renewals), `W2` (non-English market), `W3` (no-card free machines), `W4` (sub-dollar UDP)
- **Evidence:** `dossier/compute/{greencloud-budget-kvm-8gb,alphavps-c6g,hostbrr-value-8gb,bulutova-vps-8,c-servers-nanovps-384-us,tierhive-micro,github-actions,euserv,koyeb,hopx}.json`
- **Confidence:** documented

## Q1: the cheapest 8 GiB is a first-year price, and the worst case is 10x

GreenCloudVPS at USD 45.00 a year is still the cheapest 8 GiB machine found. **Its month-13
price is not knowable**, and the vendor's own pages say so twice:

- The store page never mentions renewal: **44 occurrences of "Annually", zero of "renew" or
  "recurring" in 320,626 bytes.**
- Terms §3: *"Prices listed on our website, in special offers, or provided as quotes apply
  only to new orders and may not be applied to existing orders due to inventory and stock
  management"* — and it reserves the right to *"adjust prices at the start of a customer's next
  billing cycle"*.
- ⛔ **The vendor prices the identical shape — 60 GB SSD, 4 cores, 8 GB, 8 TB, 10 Gbps — as
  SSDKVM-4 at USD 40.00 a month on its own Budget KVM page.** The clearance card is 9.4% of
  that list price. Two years at 45 then 480 averages USD 21.88 a month.

So USD 3.75 is a **first-year price on clearance stock**, not a price. A daily driver's cost
is the renewal, not the first invoice.

| row | price | renewal | what it costs |
| --- | --- | --- | --- |
| **AlphaVPS C6G**, 6 GiB / 3 vCPU | USD 4.75/mo | **locked, confirmed three ways on one page**: the banner "LOCKED AT RENEWAL, FOREVER", the invoice block "The price on the order form is the price on every invoice - renewal included", FAQ 04 "What happens to the price at renewal? Nothing." | the only permanent first-party rate lock in the set |
| **HostBrr Value 8GB**, 8 GiB / 2 vCPU | USD 4.58/mo | USD 5.50/mo published, which bounds month 13; the annual is exactly ten times the monthly | 8 GiB with a written ceiling. Whether the line includes IPv4 is not stated, so it is not claimed |
| **Bulutova VPS Sunucu 8**, 8 GiB / 2 vCore | USD 4.07/mo | USD 6.79 if the 40% discount lapses, **written on the page** | **no card**: Havale/EFT bank transfer. Verified in Turkey's ETBİS registry, Mersis 0178147856000001 |

**RackNerd refutes the promo assumption.** Its specials FAQ: *"Yes. These RackNerd VPS specials
are lifetime recurring. You can renew at the same rate for as long as you decide to keep the
service."* No price-change clause in its terms. Its 4 GB sits exactly on the line at USD 5.00.

## Q2: the recommended row never promised UDP, which is the one thing WireGuard needs

Gullo's at USD 0.29 was recommended on a first-hand report of `wireguard-go` running. Five of
its pages were read today and **none states UDP forwarding**; the vendor publishes a WireGuard
how-to but no port-protocol commitment.

**C-Servers NanoVPS-384 at USD 0.40/mo** is the row that does state it: *"la plage de ports
disponibles peut être utilisée pour TCP ou UDP, et les 20 ports peuvent être utilisés pour
n'importe quel protocole"*. Its seller, **Centerfield Ltd (14864789), is Active at Companies
House**, at the same Manchester address the store footer prints, and there is a routed IPv6
/64 beside the NAT address. Against Gullo's it costs USD 0.11 more a month and buys the UDP
sentence, 384 MiB instead of 128, 2 TB instead of 125 GB, and a company.

**TierHive Micro at USD 0.10/mo** is the answer for a health monitor, which needs outbound and
stability rather than ports: the cheapest always-on machine found anywhere in the band, hourly
billing, "No credit card required", and a live UK company (Kernel Keepers LTD, 16294246).

⛔ **Nothing in the band has both a dedicated IPv4 and a verifiable seller.** DediRock at USD
0.82 comes closest — the only sub-dollar plan with a dedicated IPv4, and KVM, so the guest
loads the in-kernel module — and fails the counterparty test: its site names "Dedi Rock LLC"
at Clearwater FL, and a Florida register search for that name returns nothing.

⚠ **DediRock's USD 0.82 needs a 12-month prepay.** USD 2.99 a month is the default on the
linked page; the annual is a separate Black Friday code on an unlinked one. A row quoting
USD 0.82 without that qualifier overstates the plan by 3.6x.

## Q3: the USD 50 hold does not exist in this corpus

The reason for distrusting the corpus was that free credits "require a
credit card with ~50$ on hold". **No provider in this corpus places a USD 50 hold.** The
largest anywhere is **Koyeb's USD 29**, cancelled immediately; the typical hold is **USD 1**.

The figures that look like USD 50 are something else, and this was the confusion worth killing:

| figure | what it actually is |
| --- | --- |
| Tenki USD 50 | *credit* released when a payment method is added, not a hold |
| Isorun USD 50 | an advertised *credit*, unverified |
| Oracle USD 100 | the **Pay-As-You-Go upgrade**, not signup |
| Oracle USD 1 | a forum report; Oracle publishes that a hold exists and **not** its size |

**The prepaid count was wrong in both directions.** Seven vendors refuse a prepaid card
outright and say so on a page read today: DigitalOcean, Google Cloud, Scaleway, Alibaba Cloud,
Oracle, Fly.io and IBM Cloud. **One accepts it in writing: Kamatera** ("This includes virtual,
prepaid, and electronic cards"). **One is disputed: Tencent Cloud**, whose billing FAQ refuses
prepaid while its registration doc says "Seven types of credit cards/debit cards/prepaid cards
are supported" — two first-party pages that contradict each other. Seven publish nothing.
Debit fares better than prepaid: eleven of sixteen accept it, five with a condition.

**The biggest no-card machine is not Daytona.** It is **GitHub Actions on a public repo: 4
vCPU / 16 GB / 14 GB SSD, free and unlimited**, on an email alone — 96 GiB-hours of RAM a day,
more than Oracle's whole always-free ARM allocation. The reap is the caveat and it is not
money: a job is terminated at 6 hours, there is no inbound port, no disk outlives the job, and
GitHub **disables a scheduled workflow on a public repo after 60 days without activity**.

**"No always-free VM without a card" is false as written**, on four counts: EUserv VS2-free (a
free root container on an email, IPv6-only), IBM LinuxONE (2 vCPU / 4 GB, 120 days, no card),
GitHub Actions public runners, and SparkCloud (root and SSH, no card, but open only to
13-to-17-year-olds). The claim that survives is narrower and useful:

> Every always-free machine that takes no card is IPv6-only, clocked, ephemeral, or gated on
> something that is not money. No provider in this corpus sells an always-free VM with a
> routable IPv4 to an adult with an email address.

## The non-English market, and what it does and does not win

Nine sellers found by searching in Turkish, Indonesian, Russian, Vietnamese, Ukrainian and
Romanian. **None beats the incumbent on GiB per USD** — the best is Bulutova at 1.96 against
2.13. What the market wins is signup and durability: two rows need no card, one settles by
domestic QR code, and three sellers are verifiable in government registries.

⭐ **Why 2.13 GiB per USD is hard to beat, measured.** IHOR.ONLINE's Russian price list sells
RAM at the margin: **+1 GB = 100 RUB/month = USD 1.23/GiB**. To reach 2.13 GiB/USD a seller must
price RAM near USD 0.47/GiB, a third of the going marginal rate. The incumbent is cheap because
it is clearance, not because the market is cheap.

**Six of the nine name no legal entity at all**, and none should be prepaid annually on that
evidence. **Chinese is the largest unclosed gap**: the leads are real but every one came from an
aggregator, and a mainland node requires 实名认证, a national-ID check that no foreign
registrant can satisfy, while Hong Kong nodes from the same sellers often need only an email and
Alipay. No Chinese record was written rather than one with a guessed identity.

## The rule this pass produced

⭐ **A negative is a claim about a search, so it carries the search's scope in the same
sentence or it is not a finding.** Every refuted negative in this corpus — "nothing monthly
under USD 1", "no always-free VM without a card", "exactly one accepts prepaid" — came from an
English-language search over English-language hosts, or from a count nobody re-took. The
sub-dollar market is Chinese and Russian; the prepaid answer was sitting in the corpus's own
Tencent record.

⚠ **A price without a renewal is half a price.** Six of the Q1 and Q2 rows published none, and
the one that was recommended as a daily driver published none while pricing the same hardware
at 10.7 times the money on its own list page.
