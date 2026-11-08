# Brokers and bare metal: the card that has a host, and the box that has none

This document answers one question: what does it cost to rent somebody else's GPU through a
broker, or a whole machine for one tenant, and where is the real price hidden? It covers 35
records and the Hetzner auction record beside them. Sixteen quote an hourly or
per-minute card rate, two quote a monthly per-card price, one publishes no price at all, and
sixteen sell a machine with no card in it. Of the 35, 30 are `paid-only`, 2 are `trial-only` and
3 are `fails-identity`, and none grants a free GPU hour that the record confirms covers a GPU.

Both halves hide the price in the same place and in opposite directions. A broker quotes a rate
per card and sells a fraction of one, so the number on the page is a slice. A dedicated host
quotes a monthly machine price and sells a 2012 processor, so the number on the page is a clock
rate with no work behind it.

## The short answer

| The question | The floor found | Term | The catch |
| --- | --- | --- | --- |
| Cheapest H100 hour | USD 0.94 per GPU-hour at Prime Intellect | hourly, spot | third-party tracker only; the vendor page returned 404; interruptible |
| Cheapest whole card per month | EUR 125 per card, USD 140.06, for an RTX 3090 at LeaderGPU | one month | a per-card price inside a 1 to 8 card server, and only at 730 hours of use |
| Cheapest dedicated box | USD 9.00 a month at Wholesale Internet | monthly | a 2007 Core 2 Duo, 4 GiB DDR2 and a 100 Mbit port |

The H100 floor is USD 0.94 at `prime-intellect-marketplace`, recorded by the tracker
`gpurentalprices.com/providers/primeintellect` (read 2026-10-22) as the spot floor for an H100.
The same tracker puts the cheapest secure on-demand H100 at USD 1.80 and the median at USD 3.29,
so the spot rate is 3.5 times below the median and it buys a card that can be taken back. The
vendor's pricing page answered 404 on the same day, so the rung is `reported`.

The monthly floor is `leadergpu`, at EUR 125 per card per month for an RTX 3090 24 GiB
(`leadergpu.com`, read 2026-10-22: "from EUR 125 per card / mo" on a 1 to 8 card server). At
USD 1 = EUR 0.89246 that is USD 140.06, or USD 0.192 per card-hour over 730 hours. The price is
a break-even, not a rate: at 100 hours of use the same card costs USD 1.40 an hour, and the
invoice is still the monthly figure.

The dedicated floor is `wholesale-internet` at USD 9.00 a month with free setup
(`wholesaleinternet.net/dedicated/`, read 2026-10-22): a Core 2 Duo at 1.6 GHz or faster, 2
cores and 2 threads, 4 GiB DDR2, a 250 GB SATA disk, a 100 Mbit unmetered port and one usable
IPv4 address. It is the cheapest whole machine in the slice and the worst value in it; the
section on threads per dollar gives the arithmetic.

## Brokers: who owns the card, and what happens when it is taken back

Sort the table by the rate the record quotes for the cheapest card it prices. The Seller column
decides the answer: an operator that owns the cards controls the price, and a marketplace passes
a third party's price through.

| Broker | Cheapest card priced | Rate | Seller | Interruption | Identity gate |
| --- | --- | --- | --- | --- | --- |
| `saladcloud-community-floor` | RTX 3090 24 GiB | USD 0.09 per GPU-hour | aggregator of community nodes | lowest priority tier, preempted by higher priority | email |
| `tensordock-floor` | RTX A4000 16 GiB | USD 0.10 per GPU-hour tracker, USD 0.12 vendor floor | marketplace, third-party hosts set price | none published | card, USD 5 minimum |
| `vast-ai-listing-structure` | RTX 3090 24 GiB | USD 0.0881 for half a card, USD 0.175 whole | marketplace, third-party hosts | interruptible instances may be reclaimed | card, USD 5 minimum |
| `prime-intellect-marketplace` | H100 80 GiB | USD 0.94 per GPU-hour spot | marketplace | spot, interruptible | email, prepaid credits |
| `voltage-park` | HGX H100 80 GiB | USD 1.99 per GPU-hour | operator | none published below a 1,016 GPU burst | email |
| `daytona-gpu` | H100 80 GiB | USD 2.27 per GPU-hour preemptible | reseller on its own sandbox platform | preemptible, plus a 15-minute inactivity stop | email, no card |
| `quantacloud` | H100 PCIe 80 GiB | USD 2.59 per GPU-hour | - | none recorded | - |
| `massed-compute` | H100 80 GiB | USD 2.73 per GPU-hour | operator | none published | email |
| `akash-network-gpu` | H100 80 GiB | USD 2.73 per GPU-hour, confirmed in stock | independent providers bid | deployments run up to 24 hours each | email |
| `vessl-cloud` | H100 SXM 80 GiB | USD 2.98 per GPU-hour | operator | none published | email, unconfirmed |
| `hot-aisle` | MI300X 192 GiB | USD 2.99 per GPU-hour | operator, one card model | none, one minute minimum | prepaid credits, card or USDT and USDC |
| `sfcompute` | H100, h100-1 | USD 0.084 a minute, USD 5.04 an hour | market with resale | 15-minute idle window, billed at USD 1.26 at most | email, unconfirmed |
| `sakura-cloud-koukaryoku` | H100 80 GiB | JPY 990 an hour, USD 6.30 | operator, Japanese incumbent | none published | card |

Two rows sell by the month rather than the hour, and the term is the product.

| Broker | Card | Rate | Seller | Interruption | Identity gate |
| --- | --- | --- | --- | --- | --- |
| `leadergpu` | RTX 3090 24 GiB | EUR 125 per card per month, USD 140.06 | operator, bare metal | one-month term | card |
| `synteq` | RTX PRO 4000 Blackwell | USD 185 a month, USD 0.25 an hour over 730 hours | operator | one-month prepaid, no partial refund | card |

Three rows arrive looking different from the way the table shows them. `voltage-park` is an
operator with a rate 40 percent below the USD 3.29 H100 median, but its page publishes a burst
range and a contract range rather than a per-hour number, so USD 1.99 is the tracker's reading.
`hot-aisle` prices one card model and bills by the minute, which makes it the cheapest way to
spend 20 minutes on 192 GiB of memory. `sfcompute` publishes a per-minute rate against a node of
eight GPUs, so the smallest orderable unit is USD 0.672 a minute and not USD 0.084.

⚠ A listed price with no host behind it is a reference rate, not a price. Three cases in this
slice show why the distinction is worth a column.

- `vast-ai-listing-structure` answered the anonymous bundle endpoint with 176,798 bytes of
  JSON in 64 offers, of which 3 carry `rentable` true and none is a bid. A query asking for
  whole-GPU rentable offers returned 0 offers, which cannot be separated from a wrong query
  from the evidence read.
- `sfcompute` has published no price since 2026-09-25. The tracker observed USD 1.84 per
  GPU-hour on an eight-GPU minimum node on 2026-09-24 and retired the provider on 2026-10-04.
  The vendor's current page is behind a login and prices an Autoresearch sandbox, not the
  market.
- `synteq` lists four cards at USD 185 and up and reports none of them in stock.
  `ori-global-cloud` publishes no price at all: `radiant.co/pricing` returned 404 on
  2026-10-22, and the vendor's own FAQ states the Ori cloud continues under the Radiant brand
  at 10,000 to 100,000 or more GPUs, sold by sales conversation.

## Three 24 GiB cards under USD 0.35 an hour that the reader cannot buy

Three Chinese retailers quote a whole 24 GiB card below USD 0.35 an hour and all three fail at
registration: the clearest case in the corpus of a price that exists with no door beside it.

| Provider | Card | Rate | Identity gate that fails |
| --- | --- | --- | --- |
| `featurize` | RTX 4090 24 GiB, 16 EPYC 9354 cores, 60 GiB RAM, 750 GB disk | CNY 1.87 an hour, USD 0.280 | Chinese mobile number; `featurize.cn/register` returned 404 so the form was not read |
| `autodl` | RTX 4090 24 GiB | CNY 1.88 an hour, USD 0.282 | SMS code, and the country selector renders +86, +852, +853 and +886 only |
| `matpool` | RTX 4090 24 GiB, 16 cores, 60 GiB RAM, 300 GB SSD | CNY 2.20 an hour, USD 0.330 | mobile number plus SMS code, then real-name |

`autodl` also prices an H800 80 GiB at CNY 9.98, which is USD 1.495 an hour, and an A800 80 GiB
at CNY 5.59, USD 0.838. `matpool` prices an A100 40 GiB at CNY 2.80, USD 0.420, which is the
cheapest 40 GiB A100 hour in the slice. Both are converted at USD 1 = CNY 6.6743, the rate read
on 2026-10-22. `featurize` is the weakest identity claim of the three: its register page 404s,
so the phone requirement is inferred from the currency and from the sibling form, and the
record says so.

The fourth identity failure in the slice is a machine, not a card: `horain-cloud`, which lists a
dual Xeon E5-2689 with 64 GiB and 512 GB NVMe at CNY 219 a month. The vendor site returned no
readable body through the broker, so the numbers rest on a forum post dated 2025-07-14 and a
reseller table.

## The fractional-GPU trap, and the rule that defuses it

A rate per GPU-hour is only a rate per card if the offer is one card. Vast.ai's public listing
makes the difference explicit: each offer carries `gpu_frac`, and the cheapest row on
2026-10-22 was an RTX 3090 at USD 0.0881 an hour with `gpu_frac` 0.5. That is half a card.

The rule is one division:

    whole-card rate = listed dph_total / gpu_frac

Applied to the two cheapest rows on the page: USD 0.0881 / 0.5 = USD 0.1762 for the 3090,
which the record rounds to USD 0.175, and USD 0.1215 / 0.125 = USD 0.972 for the 4090. The
second is the trap in its purest form: USD 0.1215 reads as the cheapest 4090 hour anywhere, and
it buys an eighth of one. The whole-card equivalents the record derives from the same page are
USD 0.101 for an RTX 5070 Ti, USD 0.109 for an RTX 4080S, USD 0.175 for an RTX 3090, USD 0.213
for an RTX 5090, USD 0.536 for an A100 PCIe and USD 0.802 for an RTX 4090.

Vast.ai is the broker in this slice that quotes fractions rather than cards. The same error runs
the other way at `sfcompute`, where the unit is a node of eight GPUs and the quoted per-GPU
figure is only reachable by buying all eight. ⚠ A fraction of a card is not a cheaper card: it
is less memory, a shared PCIe link and a neighbour whose job decides throughput. Convert
before comparing, and state the fraction beside the rate.

The same trap applies to a marketing floor that names no card. `saladcloud-community-floor`
corrects the vendor line "GPUs from USD 0.015 per hour", which does not correspond to any whole
card on the community tier: the cheapest named 24 GiB card is USD 0.09 for a 3090, then USD
0.16 for a 4090, USD 0.25 for a 5090 and USD 0.79 for an L40S.

## Dedicated and bare metal: 20 machines, sorted by price

Every row is a whole machine for one tenant. Sorted by the USD equivalent of the monthly price,
converted at the rate recorded on 2026-10-22: USD 1 = EUR 0.89246 and USD 1 = CNY 6.6743. The
generation column is read from the part number; no record states a manufacturing year, so treat
it as inferred. A dash means the record does not carry the value.

| Provider | CPU (generation) | Cores / threads | RAM | Disk | Port or traffic | Setup | Price as quoted | USD a month |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `wholesale-internet` | Core 2 Duo (2007) | 2 c / 2 t | 4 GiB DDR2 | 250 GB SATA | 100 Mbit unmetered | none | USD 9.00 | 9.00 |
| `oneprovider` | Atom C2350 (2013) | 2 c / 2 t | 4 GiB DDR3 | 1 x 1 TB HDD | 1 Gbps, fair use | EUR 4.99, waived | EUR 11.99 | 13.43 |
| `cstserver` | Xeon E5-2620 (2012) | 6 c / 12 t | 16 GiB | 120 GB SSD | 80 Mbit Frankfurt, 30 Mbit Hong Kong | - | USD 17.90 | 17.90 |
| `ovhcloud-kimsufi` | KS-4, configuration not read | - | - | - | - | - | EUR 16.99 | 19.04 |
| `hostnoc` | Xeon E3-1230 v2 (2012) | 4 c / 8 t | 16 GiB DDR3 | 1 x 1 TB HDD | 1 Gbps unmetered | - | USD 24.95 | 24.95 |
| `colocrossing` | - | - | 32 GiB | 1 TB | 40 TB a month | - | USD 25.00 | 25.00 |
| `quickservers` | Xeon E5-2450L (2012) | 8 c | 32 GiB | 4 x 600 GB SAS | 1 Gbps unmetered, fair use | none | USD 29.99 | 29.99 |
| `horain-cloud` | 2 x Xeon E5-2689 (2012) | 16 c / 32 t | 64 GiB | 512 GB NVMe | 20 Mbps Telecom | - | CNY 219 | 32.81 |
| `ovhcloud-so-you` | Xeon-E 2136 (2018) | 6 c / 12 t | 32 GiB DDR4 ECC 2666 | 2 x 512 GB NVMe | 1 Gbps guaranteed unmetered | EUR 29.99 | EUR 29.99 | 33.60 |
| `quickservers` | 2 x E5-2680 v2 (2013) | 20 c / 40 t | 128 GiB | 600 GB | 1 Gbps unmetered, fair use | none | USD 44.99 | 44.99 |
| `quickservers` | 2 x E5-2680 v2 (2013) | 20 c / 40 t | 128 GiB | 16 x 600 GB SAS, 9.6 TB raw | 1 Gbps unmetered, fair use | none | USD 59.99 | 59.99 |
| `ovhcloud-rise` | Xeon-E 2386G (2019) | 6 c / 12 t | 32 GiB ECC 3200 | 2 x 512 GB NVMe | 1 Gbps unguaranteed | EUR 56.99 | EUR 56.99 | 63.86 |
| `quickservers` | 2 x Xeon E5-2690 (2012) | 16 c / 32 t | 256 GiB | 4 x 300 GB SAS | 1 Gbps unmetered, fair use | none | USD 64.99 | 64.99 |
| `hetzner-dedicated` | Ryzen 5 3600 (2019) | 6 c / 12 t | 64 GiB DDR4 | 2 x 512 GB NVMe | 1 Gbit/s | none | EUR 59.00 | 66.11 |
| `hetzner-server-auction` | Core i7-8700 (2017) | - | 128 GiB | - | 1 Gbit/s, unlimited traffic | none | EUR 64.00 | 71.71 |
| `quickservers` | 2 x Xeon Gold 6140 (2017) | 36 c / 72 t | 128 GiB | 480 GB SSD | 10 Gbps, fine print 1 Gbps fair use | none | USD 79.99 | 79.99 |
| `phoenixnap-dedicated-outlet` | Xeon E-2186G (2018) | 6 c | 32 GiB DDR4 | 480 GB SSD | - | - | EUR 89.99 | 100.83 |
| `worldstream` | EPYC 4245P (2024) | 6 c / 12 t | - | - | - | - | EUR 104.00 | 116.53 |
| `packetra` | 2 x Xeon E5, model not stated | 28 c / 56 t | 64 GiB DDR4 | 1 TB SSD | 1 G unmetered or 10 G with 100 TB | none | EUR 164.61 | 184.45 |
| `datapacket` | EPYC 4245P (2024) | 6 c / 12 t | - | - | - | - | USD 240.00 | 240.00 |

One record is deliberately outside the sort. `invs` publishes "from 1200 RUB a month" and no
rouble rate was read on 2026-10-22, so the figure is not converted and the machine is not
ranked. Its own note is the warning: a Russian aggregator's entry prices of RUB 110 and RUB 139
cannot be whole machines at any plausible rate, so a Russian "dedicated" entry price should be
read as a VPS-class slice until the configuration is read.

Four rows in the table are worth naming rather than leaving to the sort.

`hetzner-dedicated` is the AX41 at EUR 59.00 a month excluding VAT: a Zen 2 Ryzen 5 3600, 64
GiB of DDR4, two 512 GB NVMe, one IPv4 and a /64, no setup fee, and EUR 0.0945 an hour against
the monthly cap. A day at the hourly rate costs EUR 2.27 and nothing accrues after the machine
is cancelled.

`ovhcloud-so-you` is the cheapest orderable current-generation machine in the slice. The domain
sells nothing to new customers, because the vendor grouped So you Start into OVHcloud and
discontinued the site, but the SYS SKU still orders at EUR 29.99 with a EUR 29.99 setup fee. On
2026-10-22 the OVH availability API returned stock at Beauharnois and London only, of the five
datacenters the range quotes.

`cstserver` is the cheapest machine with a China-optimised route, and the route is the price.
USD 17.90 buys 80 Mbit in Frankfurt or 30 Mbit in Hong Kong, which is a difference of about
16 TB a month of transfer at line rate for the same money. A 60 percent code and a three-year
prepay bring it to USD 9.80.

`packetra` is the only whole machine in the slice whose signup needs nothing but an address. The
vendor's post states "Email-only signup, no KYC at any stage", five dedicated IPv4 addresses and
a /64, at EUR 164.61 recurring after a 10 percent coupon against EUR 182.90 list. The evidence
is a vendor post on a third-party forum dated 2026-10-04, so the rung is `reported`.

## Threads per dollar, and why a 2012 Xeon is not cheap

A USD 25 box with eight threads looks like nearly four times the machine of a cloud instance at
USD 6.49, which is what this corpus prices Hetzner Cloud CX23 at with 20 TB of egress included.
It is not. The two reasons are the clock and the work per clock, and this table holds only rows
where the record carries both a thread count and a clock, so nothing here is estimated.

| Machine | Threads | Clock (GHz) | Price | USD per thread-month | USD per thread-GHz-month |
| --- | --- | --- | --- | --- | --- |
| `wholesale-internet` Core 2 Duo | 2 | 1.6 | USD 9.00 | 4.50 | 2.81 |
| `hostnoc` Xeon E3-1230 v2 | 8 | 3.3 | USD 24.95 | 3.12 | 0.95 |
| `hostnoc` Xeon L3426 | 8 | 1.86 | USD 25.72 | 3.22 | 1.73 |
| `wholesale-internet` i7-2600 | 8 | 2.8 | USD 25.00 | 3.13 | 1.12 |
| `hostnoc` i7-4790K | 8 | 4.0 | USD 39.95 | 4.99 | 1.25 |
| `wholesale-internet` i7-8700K | 12 | 3.7 | USD 59.00 | 4.92 | 1.33 |
| `wholesale-internet` 2 x E5-2696v3 | 72 | 2.30 | USD 199.00 | 2.76 | 1.20 |
| `ovhcloud-so-you` SYS-1 | 12 | 3.3 | EUR 29.99 | EUR 2.50 | EUR 0.76 |
| `ovhcloud-rise` RISE-1 | 12 | - | EUR 56.99 | EUR 4.75 | - |
| `datapacket` EPYC 4245P | 12 | 3.9 | USD 240.00 | 20.00 | 5.13 |
| `worldstream` EPYC 4245P | 12 | 3.9 | EUR 104.00 | EUR 8.67 | EUR 2.22 |

The USD 9 machine costs USD 4.50 a thread-month and USD 2.81 a thread-GHz-month, the worst
figure in the table on both measures. The USD 25 i7-2600 buys eight threads at USD 3.13 a
thread-month; its advantage over a small cloud instance is thread count, not throughput. The
cheapest per-thread machine is `quickservers` at USD 1.11 a thread-month for 72 threads and USD
79.99, a clearance configuration limited to one or two units.

⚠ Clock is not throughput. `hostnoc` records its own entry part as a 2012 Ivy Bridge and states
that per-thread throughput is about a third of a current Ryzen. That is the record's estimate,
not a measurement. A thread-GHz comparison across a 2012 Xeon, a 2019 Zen 2 and a 2024 Zen 5
understates the newer part, in the direction that decides whether USD 25 of 2012 silicon beats
USD 6.49 of current cloud. For a compute-bound job it does not.

## Auctions and clearance: a snapshot, not a price list

`hetzner-server-auction` is a live listing of single physical machines, and its price moves
while a reader looks at it. On 2026-10-22 the endpoint the auction page itself calls
(`hetzner.com/_resources/app/data/app/live_data_sb.json`) returned 116 machines. The cheapest
was EUR 64 a month for an Intel Core i7-8700 with 128 GiB of RAM, no setup fee, a 1 Gbit/s port
and unlimited traffic. The median was EUR 99.50 and the dearest EUR 918. The cheapest machine
with 64 GiB of RAM and 2 x 512 GB NVMe was EUR 70.

⚠ The read carries a date but no clock time, and the list moved between two reads four minutes
apart: the median went from EUR 100 to EUR 99.50 and the dearest from EUR 919.70 to EUR 918.
Any figure from this endpoint is a snapshot with a date and not a quotation. Two field
anomalies are worth carrying: `Hardware.Storage` is zero for all 116 records with the disks
present only as description strings, and `Hardware.CPU.CoreCount` is 1 for all of them because
it counts sockets.

The auction is not the cheapest dedicated machine even on its own date. EUR 59 buys the AX41
with a 2019 Zen 2 part, 64 GiB, two NVMe disks and no setup, against EUR 64 for a 2017 part
with 128 GiB. The auction wins on memory per euro and on nothing else.

Regional stock decides more of this class than price does. `ovhcloud-kimsufi` advertises the KS
range from EUR 9.99 excluding VAT, and that machine cannot be ordered in any datacenter: the
plan code `25skb012` returns `unavailable` in every location. Nineteen of the 26 KS plan codes
in the OVH catalogue return unavailable everywhere on 2026-10-22. The seven that hold stock are
North American or Asia-Pacific, so the cheapest orderable Kimsufi is KS-4 at EUR 16.99 in
Singapore, and the vendor states the Asia-Pacific locations carry a 25 TB monthly traffic limit
where the European, United States and Canadian ones are unlimited.

Clearance pages are the other half of the same problem.

- `phoenixnap-dedicated-outlet` is not an outlet. The published all-servers list opens at EUR
  89.99 a month, and the USD 58 headline that circulates comes from a 2015 datasheet.
- `quickservers` describes its list as an acquired fleet where most configurations are limited
  to one or two units, and the vendor edits the post to mark items sold.
- `synteq` reports none of its four configurations in stock, and `sfcompute` has been retired
  from the tracker that priced it.
- `cstserver` sale prices are dated 2026-08-20 and the codes may have expired by the date of
  the read.

## What this class does not give

⭐ No free tier. Of the 35 records, none grants a free GPU hour with the grant confirmed to
cover a GPU, and none grants a free dedicated machine. The free elements that do exist are
discounts and unquantified credits: `autodl` gives 30 days of membership, which is the 5 percent
member rate and worth CNY 0 at zero spend; `matpool` gives a new-user credit of unstated size
that is claimable only after the SMS step; `daytona-gpu` advertises USD 200 in "free compute"
with no card, on the same page that lists GPU rates, and the page does not say the credit
covers GPU hours. `akash-network-gpu` holds a USD 1 trial credit whose own terms exclude the
RTX 4090, RTX 5090, A100 and H100.

No card unless the box has one. Sixteen of the 35 sell a machine with no GPU, and a dedicated
box is not a route to GPU capacity. The three GPU rows in the machine group are priced out of
reach for this analysis: `phoenixnap-dedicated-outlet` lists 2 x Xeon Silver 4110 with a Tesla P40
24 GB at EUR 1,003 a month and a V100 16 GB at EUR 1,259, both by sales contact rather than
self-service, and `horain-cloud` lists 8 x RTX 4090 with 1 TB of RAM at CNY 7,500 a month
against an identity gate that does not open.

Minimum terms, and the fee that rides with them. `leadergpu` sells by the month, so the USD
0.192 card-hour exists only at 730 hours, and `synteq` bills the first month up front with no
partial refund. `ovhcloud-rise` charges a one-time installation fee equal to one month, so
RISE-1 costs EUR 113.98 in the first month and EUR 56.99 after it; on a 12-month term the fee is
zero and the total is EUR 649.69, or EUR 54.14 a month. `ovhcloud-kimsufi` prints a one-month
installation fee while the OVH catalogue returns zero for the same SKU.

Data loss is mostly unpriced in this slice. One record states a deletion rule: `autodl` reserves
data deletion after three months without a login or CNY 50 of arrears. The other 34 carry no
data-retention term at all, so a reader cannot price the loss of a dataset from these records,
and a machine that vanishes with an operator is a failure mode this slice does not measure.

## What could not be read

The routes tried, and what each one produced.

- `vast.ai` needed no key: the bundle endpoint answered 200 with 176,798 bytes, and the
  whole-card query returned 0 offers. Three explanations were considered for the low rentable
  count: the default page is a catalogue sample, the account-less view hides rentable rows, or
  most offers are genuinely idle hosts. The evidence cannot separate them. The vendor's own
  `/pricing` page renders by script and carried no numbers to the extractor.
- Four rates rest on a tracker because the vendor page did not answer: the Prime Intellect
  pricing page returned 404, and `hotaisle.xyz/pricing`, the QuantaCloud vendor site and the
  Voltage Park support article named as the rate source were not read.
- Three paths returned 404 and one host answered with no body: `radiant.co/pricing`,
  `featurize.cn/register` and `phoenixnap.com/dedicated-servers/pricing` are 404, so the
  all-servers list is that record's price source, and `horain.net` returned nothing readable.
- Two price tables load by script, so the figures came from elsewhere: the Hetzner dedicated
  root-server page, and the auction page, whose JSON endpoint was read instead.
- `oneprovider` renders two prices and two setup fees client-side, so the record cannot settle
  whether the second column is a clearance price or a shorter term. `invs` fills its price
  column by script, so RUB 1,200 is a stated floor and not a mapped row.
- `cstserver` writes "12C" for an E5-2620, which is the thread count of a 6-core part. A core
  count taken from that table is double the real one.

## What would change the answer

One authenticated Vast.ai search with the same filters would establish whether a whole card is
rentable at the rates the public page shows, and that measurement would either confirm or delete
the USD 0.175 floor. The Prime Intellect vendor page coming back would move USD 0.94 from
`reported` to `documented`, and one booked spot hour would show whether the floor survives
contact with supply. For the monthly floor, one `leadergpu` invoice at 100 hours of use would
test the record's own claim that the hourly figure is a break-even and not a rate.

For the dedicated side the number that would move a verdict is a benchmark rather than a price:
one single-thread run on the USD 9 Core 2 Duo and one on Hetzner Cloud CX23 at USD 6.49. The
record asserts a third of current per-thread throughput for a 2012 Xeon; a measured ratio on the
2007 part would replace that estimate with one number.
