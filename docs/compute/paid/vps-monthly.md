# The cheapest box that stays up, and what its traffic term is

A VPS is the only shape in this topic that never stops. It bills by the month
whether it runs or not, which makes it the wrong product for a burst workload and
the right one for anything that must answer at 03:00. The question is the monthly
cap, and then the second question is the traffic term, because a box that costs
USD 6.70 and charges EUR 1.00 per additional terabyte is a different product from
one that costs the same and includes 20 TB.

The answer is **Contabo's Cloud VPS 4 at USD 6.60 a month for 4 vCPU, 8 GB and
100 GB**, and the reason is not that it is the best box. It is the cheapest row
here that a reader can order today. Hetzner's CX23 is the better machine on paper
at EUR 5.99, which is USD 6.70 at the 2026-10-23 ECB rate, and **Hetzner lists it
as "not available"** on its own cost-optimized page, as it does every rung on that
line. netcup's entry shape is USD 9.25 on a 12-month contract.

Two terms go against Contabo and both are stated below rather than here. Its price
is printed "for the first 24 months" with no renewal rate, and its traffic is
unlimited with no published rate, which is a discretionary throttle and not a
quota.

## The comparison

Sorted by the monthly bill at a shape close to 2 vCPU / 4 GiB. `Month` is the
24/7 bill at the monthly cap in USD, converted at EUR 1 = USD 1.1193 and GBP 1 =
USD 0.74804, both the 2026-10-23 reference rates. `Traffic` is the included
allowance and then the rate, because the rate is where the bill is.

⚠ **`Shape priced` is the shape the price belongs to, and for ten rows the record
does not carry it.** `extras.shape` is null on `ionos`, `gcore`, `alibaba-ecs`,
`vultr`, `digitalocean`, `linode`, `azure-vm` and `aws-ec2`, so their shape comes
from the card and their `m24h_usd` is the card's figure for it; the record says so
through `seed_status: ranked` and `talaria_m24h_usd`. Three rows carry a shape in
the record that is not the shape priced, and those are marked in the cell:
`upcloud`'s record describes the EUR 3 entry plan while USD 14.00 is a larger rung,
`hostinger-vps` records 1 vCPU and 50 GB of NVMe, and `ovhcloud` records b2-7 at 2
vCore and 7 GB. Where the cell says `not in the record`, the shape is unverified.

| Provider | Shape priced | Month | Traffic included | Then | IPv4 | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Oracle Cloud Always Free | 2 OCPU / 12 GB / 200 GB | USD 0 | 10 TB | metered | included | qualifies-with-caveat |
| Google Cloud e2-micro | 1 GB / 30 GB | USD 0 | 1 GB | metered | ephemeral, not reserved | qualifies-with-caveat |
| Hetzner Cloud CX23 | 2 vCPU / 4 GB / 40 GB | USD 6.70 | 20 TB | EUR 1.00 per TB | EUR 0.50 a month extra | paid-only |
| Contabo Cloud VPS 4 | 4 vCPU / 8 GB / 100 GB | USD 6.60 | unlimited, no published rate | none published | not stated | paid-only |
| netcup VPS 500 G12.5 | 2 vCPU / 4 GB / 64 GB | USD 9.25 | flat rate, not quantified | none published | included | paid-only |
| Ionos | 2 vCPU / 4 GB, not in the record | USD 10.65 | not read | not read | not read | paid-only |
| Gcore | 2 vCPU / 4 GB, not in the record | USD 13.92 | not read | not read | not read | paid-only |
| UpCloud | 2 vCPU / 4 GB; the record describes the 1 vCPU entry plan | USD 14.00 | not read | not read | not read | paid-only |
| Alibaba ECS | 2 vCPU / 4 GB, not in the record | USD 14.48 | not read | not read | not read | qualifies-with-caveat |
| Hostinger VPS | 1 vCPU / 50 GB, per the record | USD 14.99 | not read | not read | not read | paid-only |
| OVHcloud | b2-7: 2 vCore / 7 GB / 50 GB, per the record | USD 18.43 | not read | not read | not read | trial-only |
| Scaleway | 2 vCPU / 4 GB, not in the record | USD 18.67 | not read | not read | charged separately | paid-only |
| Vultr | 2 vCPU / 4 GB, not in the record | USD 20.00 | not read | metered | not read | trial-only |
| DigitalOcean | 2 vCPU / 4 GB, not in the record | USD 24.00 | not read | metered | not read | paid-only |
| Linode | 2 vCPU / 4 GB, not in the record | USD 24.00 | not read | metered | not read | paid-only |
| Azure VM | 2 vCPU / 4 GB, not in the record | USD 28.55 | not read | metered | not read | qualifies-with-caveat |
| AWS EC2 | 2 vCPU / 4 GB, not in the record | USD 36.93 | not read | metered | charged separately | trial-only |

The month column is the 24/7 bill at the monthly cap, which is what a VPS costs
if it stays up. A box destroyed between runs costs the `10h` figure instead, and
that is in each record's `extras.m10h_usd`. The gap is 55 to 63 per cent on every
row except Hostinger, where it is 33 per cent: DigitalOcean is USD 10.71 at 10
h/day against USD 24.00 at 24/7, Azure is USD 11.28 against USD 28.55, and
Hostinger is USD 10.06 against USD 14.99. A figure quoted without its duty cycle
is not a comparison.

⚠ The `not read` cells are the honest state of a catalogue built from a third-party
card. Most of these rows were priced from the card and their pages were not opened,
so their traffic term is unknown and their records say `reported`. The rows that were
read are the ones a recommendation should rest on. The
`Verdict` column separates a free offer that ends from one that was never there:
`trial-only` rows have a credit or a window, and `paid-only` rows have neither.

## Hetzner Cloud

CX23 is EUR 5.99 a month, or EUR 5.49 excluding IPv4, with 20 TB of traffic
(`documented`, `hetzner.com/cloud/cost-optimized/`, read 2026-10-24). Hetzner's own
price-adjustment table prints the same rung as **USD 0.0104 an hour or USD 6.49 a
month excluding IPv4 and VAT**, and the corpus converts the EUR figure at 1.1193 to
**USD 6.70**. The 0.21 gap is Hetzner's own FX rate against the recorded one, not a
different machine, and both figures are on the record.

⛔ **The CX23 is not orderable.** Re-read on 2026-10-24, the cost-optimized page
prints "CX23 / not available", and so does every other rung on that line: CAX11,
CX33, CAX21, CX43, CAX31, CX53 and CAX41. The line's own page explains why: "this
resource-saving use means that the number of available servers is limited". The
front page repeats it, marking the whole Cost-Optimized family "Currently not
available". The CX23 is the better machine on paper, and a reader acting on that would
find no way to buy the box.

⚠ **Every rung on the product page is exactly EUR 0.50 above the price-adjustment
table, and that EUR 0.50 is the Primary IPv4.** The vendor's own primary-IP page
states the charge: "We charge EUR 0.50 / $ 0.60 per month (excl. VAT) for our
Primary IPv4s." The delta holds to the cent on all eight rungs, so the product page
is quoting IPv4-inclusive and the adjustment table is quoting ex-IPv4. A reader who
takes EUR 5.99 as the ex-IPv4 price overpays by 0.50 in the comparison.

The monthly figure is a cap: a VM bills hourly and stops at the monthly rate, so
a box that runs for a week costs a week and a box that runs all month costs the
cap. Twenty terabytes of traffic are included and overage is billed in 100 MB
blocks rounded up (`documented`, `docs.hetzner.com/cloud/billing/faq`, read
2026-10-22). That allowance is what would make Hetzner the answer if it were
orderable: 20 TB a month is 666.7 GB a day, which covers two thirds of the serving
target assumed here and misses the top of it. Overage at EU-Central locations
is EUR 1.00 per additional terabyte, published on `hetzner.com/cloud/cost-optimized/`.

⚠ The FAQ also states that the usage notifications at 75 and 100 per cent do not
cap or stop traffic, and that anything beyond the allowance is billed as usual. A
reader who treats the notification as a brake will meet the bill instead.

**The orderable Hetzner rung is CPX02 at EUR 6.49, which is USD 7.26**, with 1
AMD vCPU, 1 GB and 20 GB of NVMe (`documented`,
`hetzner.com/cloud/regular-performance/`, read 2026-10-24). That is a quarter of
the RAM for the same money as the CX23, which is the real cost of the stockout:
the substitute is not the same product. The Regular Performance page carries no
"not available" string on any rung.

Evidence: the cost-optimized page, the price-adjustment table, the primary-IP page
and the billing FAQ (all read 2026-10-24, the FAQ 2026-10-22). Verdict: the
cheapest box with a real traffic allowance and no committed term, and not
currently purchasable.

## Contabo

Cloud VPS 4 is USD 6.60 a month for 4 vCPU, 8 GB of RAM, 100 GB of SSD, one
snapshot and unlimited traffic (`documented`, `contabo.com/en-us/vps/`, read
2026-10-24).

⚠ **The USD 6.60 is a 24-month rate.** The product page prints the price with "for
the first 24 months" beneath every rung, and it also prints a VAT-inclusive figure
of USD 5.28 beside it. Two different bases on one card, and the record carries the
6.60 as the bill while noting that the page's strikethrough markup makes the promo
direction unclear: the previous-price elements carry EUR 5.50, 7.50, 14.00, 25.00,
37.00 and 49.00 across the five rungs, which would make EUR 5.50 the pre-discount
figure, while the product data gives EUR 5.50 as the low price. The plan-level
record `contabo-cloud-vps-4` converts EUR 5.50 at 1.1193 to **USD 6.16** on a
24-month term with no published renewal rate. Both readings are above USD 5, so
the row fails the lane's ceiling either way and the ambiguity is recorded rather
than resolved.

⛔ "Unlimited traffic" with no published rate is the weakest kind of term. It is
not a quota: there is no ceiling to design against, no threshold at which the
workload is safe, and no way to compute a marginal cost. The corpus's own rule is
that a documented absence is weaker than a documented limit, and this is that
case.

⚠ **The two columns, USD 2.71 and USD 6.60, are not the same product divided two
ways.** 6.60 divided by 730 is **USD 0.009 an hour**, which is a rate and not a price.
USD 2.71 is 6.60 times 300 over 730, which is 10 hours a day for 30 days, the `10h`
figure. The lower number is the duty-cycle figure and the two are different questions,
not two divisions of one month.

The disk is the reason to be here: 100 GB and 8 GB of RAM for USD 6.60, against
Hetzner's CPX02 at USD 7.26 for 20 GB and 1 GB. The CX23 beats it on shape at 40 GB
and 4 GB for USD 6.70 and cannot be bought.

Evidence: the Contabo VPS page and pricing page (read 2026-10-24), and the
plan-level record's `AggregateOffer`. Verdict: the most disk and RAM per dollar
that is actually orderable, and a traffic term that promises nothing.

## netcup

VPS 500 G12.5 is EUR 8.26 a month excluding VAT on a 12-month contract, which is
**USD 9.25** at 1.1193, for 2 vCPU, 4 GB and 64 GB (`documented`,
`netcup.com/en/server/vps`, read 2026-10-24). The same card prints a second figure,
EUR 9.50, labelled "(incl. 19% VAT)".

⛔ **That label is wrong on netcup's own page, on all five rungs.** EUR 8.26 at 19
per cent is EUR 9.83, not 9.50. The ratio between the two printed columns is 1.150
on every rung: 8.26 to 9.50, 14.50 to 16.68, 26.92 to 30.96, 45.36 to 52.16, 67.11
to 77.16. A 1.150 ratio is not 19 per cent VAT, and no rung on the page is. The
corpus records the ex-VAT figure and converts it, which is why this table says USD
9.25 and not USD 10.63.

⚠ Neither earlier figure survives. USD 3.50 is a plan that does not exist at that
price, and USD 5.03 is a different shape. A figure of "USD 8.51 on a one-month term"
appears in no record and in no history entry, so it is not carried.

The 12-month contract is the constraint. The monthly price is only available on
that term, which makes the commitment the product. The product links carry both
12-month and 24-month variants, so a lower 24-month rate exists and is not
published on the page read.

Evidence: `netcup.com/en/server/vps` (read 2026-10-24), five rungs quoted. Verdict:
a European box with a flat traffic term and a year-long commitment.

## The free VMs, for comparison

Oracle's Always Free A1 shape is 2 OCPU and 12 GB with 200 GB of block storage and
10 TB a month of egress, and it costs nothing (`documented`, the Always Free
resources page, read 2026-10-22). Google's e2-micro is 1 GB with 30 GB of disk and
1 GB of egress a month, also free.

Both are cheaper than every row in this document and both have a catch. Oracle
reclaims an instance whose seven-day 95th-percentile utilisation stays under 20 per
cent, and the test covers CPU, network **and memory** on A1, so a box that idles at
low memory is at risk even when it is working. Google gives 1 GB of traffic a
month, which is not a serving allowance.

⚠ Both free rows need a card. Oracle takes a USD 1.00 authorisation at signup and
states it does not accept debit cards with a PIN, or virtual, single-use or prepaid
cards. Google's authorisation is a USD 0.00 request that a bank may show as pending
for one to 14 business days. A reader comparing a USD 6.60 VPS to a free VM should
compare the identity cost and the traffic term first, because those are where the
free row loses.

## What did not work

- **AWS and Azure as paid VPS lanes**: the on-demand rates run from four to five
  and a half times Hetzner's for the same shape. Azure is USD 28.55 and AWS EC2 USD
  36.93 against the CX23's USD 6.70, which is 4.3 and 5.5 times. A figure of "three
  to five times" with Azure at USD 11.28 and AWS at USD 14.73 uses the 10 h/day
  figures, not the monthly bill. GCP is not
  in this comparison because no record carries a 2 vCPU / 4 GiB monthly figure for
  it: `gcp-compute` prices the free e2-micro only.
- **The USD 0.09 a gigabyte egress figure is `unverified`.** No record in
  `dossier/compute` carries it: `aws-ec2.egress.terms`
  and `azure-vm.egress.terms` both read "not published on the source card", and no
  page was read for either. The number is dropped rather than carried forward.
- **DigitalOcean and Linode**: USD 24.00 each for the same shape, with metered
  egress. The USD 10.71 and USD 10.80 are their `10h` figures. They are the reference
  price and not the answer.
- **Hostinger VPS**: USD 14.99 monthly, and USD 10.06 at 10 h/day. The card also
  states "from $6.49 a month on a two-year term, renewing at $11.99 a month", which
  is a third price on a third basis and the one a buyer meets at renewal.
- **Fly.io**: no free tier and the cheapest always-on Machine is 256 MB. It is a
  platform, not a VPS. It does carry a trial: up to 2 hours of Machine runtime or 7
  days, whichever comes first, with no card. A card is required after it.
- **Kakao Cloud, Samsung Cloud, Naver Cloud**: regional providers whose prices are
  quoted in local currency. ⚠ **The claim that their signup wants a local phone is
  `unverified`.** All three records carry
  `identity_cost.kind: email` with the detail "unverified: not stated in the source
  card", so no signup was read for any of them. The record set carries them and this
  document does not rank them.
- **Oracle's trial**: USD 300 for 30 days. A trial, not a VPS.

## Chaining

A Hetzner CX23 with 20 TB of traffic is the single box that covers a serving
workload up to 666.7 GB a day, and the rest is billed per terabyte at
EUR 1.00. Above that the answer is a CDN in front rather than a bigger box, and
that is the `egress` topic's. Contabo's 100 GB disk is where a working set lives
when the serving box should stay small, and at USD 6.60 it is the one of the two
that a reader can buy today.

## Superseded claims

Figures this document has replaced, with the evidence that replaced them, are dated in
[`compute-seed-claims-superseded.md`](../../../history/2026-10-22T030705Z/compute-seed-claims-superseded.md).
