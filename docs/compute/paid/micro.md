# The floor: the least money that buys a working machine

Every other document in this topic prices a shape. This one prices the entry: the
smallest invoice that returns a machine with a root shell, and the largest machine
that amount buys at USD 2, USD 5, USD 10, USD 20 and USD 50. The answer is a
ladder, because the cheapest invoice and the best value are different rows.

This page prices the ladder from USD 1.42 upward, and that is not the floor. Twelve
records in `dossier/compute` price a paid always-on machine under USD 1.00, the lowest
at USD 0.10, and the cheapest of them with a dedicated IPv4 is USD 0.82. Those rows are
priced in [`under-one.md`](under-one.md), which owns that band; this document states
what they are and does not repeat their cards. The VPS ladder here runs from USD 1.42
to USD 35.50, and the dedicated lane opens at USD 19.90 for the shape that beats every
VPS below it. Memory is written in GiB because the records store it that way; where a
vendor prints GB the table keeps that figure, and the two units differ by 7 per cent.

## The short answer

The cheapest row on this ladder is ServerHost at USD 16.99 a year, USD 1.42 a month,
for 1 vCPU, 2 GiB and 30 GB of NVMe. It is not the cheapest machine in the corpus:
TierHive's Micro is USD 0.10 a month and DediRock's Promo VPS Saver is USD 0.82 a
month with a dedicated IPv4, both `documented`, and both in
[`under-one.md`](under-one.md). The cheapest machine on this ladder worth running a
real job on is GreenCloudVPS at USD 45.00 a year, USD 3.75 a month, for 4 vCPU, 8 GiB
and 60 GB of NVMe. A dedicated box first buys more RAM and disk than a VPS at
USD 19.90, where Kimsufi returns 32 GiB and 4 TB against Contabo's 24 GiB at
USD 13.44.

## The ladder

Sorted by the monthly bill. `USD/month` is the figure to compare, and `Billed as`
carries the vendor's own price in its own currency. EUR rows are converted at
EUR 1 = USD 1.1205, the rate `api.frankfurter.dev/v1/2026-10-22?base=EUR&symbols=USD`
returned for the reference date 2026-10-22. The conversion is inferred, and the
native figure beside it is the documented one. Several records carry their own
conversion at 1.1193, the 2026-10-23 reference rate, which moves a row by at most
one cent.

| USD/month | Shape (vCPU / RAM / disk) | Provider | Billed as | Renewal | What breaks it |
| --- | --- | --- | --- | --- | --- |
| 1.42 | 1 / 2 GiB / 30 GB | ServerHost | annual, USD 16.99/yr | not published | campaign rate with the promo code in the URL; 1 Gbps shared port |
| 1.83 | 1 / 1 GiB / 20 GB | RackNerd | annual, USD 21.99/yr | same rate, lifetime recurring | 20 GB disk and a 3 TB cap; a failed renewal loses the year |
| 2.00 | 1 / 512 MiB / 10 GB | BuyVM | annual, USD 24.00/yr | list price | fair-share CPU on a shared port; 512 MiB is a proxy, not a host |
| 2.08 | 2 / 4 GiB / 35 GB | GreenCloudVPS | annual, USD 25.00/yr | not published | stock shows 0 Available at several locations; no refund |
| 2.15 | 1 / 2 GiB / 25 GB | HostBrr | monthly, EUR 2.00 / USD 2.15, both printed | same rate, no strike-through | one Frankfurt site; 25 GB is the ceiling for a stored corpus |
| 2.33 | 2 / 1 GiB / 30 GB | CloudCone | annual, USD 28.00/yr | same USD 28, raisable on 45 days' notice | 1 GiB ceiling; the 4 TB quota is a stop, not a bill |
| 2.48 | 1 / 1 GiB / 30 GB | netcup | 12-month contract, EUR 2.21/mo incl VAT | list price | the cheapest rung carries the longest commitment |
| 2.50 | 1 / 512 MiB / 10 GB | Vultr | hourly capped, USD 2.50/mo | list price | IPv6 only, so no A record without the USD 3.50 rung |
| 2.75 | 1 / 2 GiB / 20 GB | Datalix | monthly, EUR 2.45/mo | not published | 21 of 24 advertised rungs are `Ausverkauft`; the in-stock list is three Ryzen GEN 2 rows |
| 2.85 | 2 / 2 GiB / 30 GB | AlphaVPS | annual, EUR 2.54/mo | flat at renewal, stated as locked forever | 30 GB fills before the transfer allowance; the 14-day refund is first-order, unused only, and excludes promo and China orders |
| 3.75 | 4 / 8 GiB / 60 GB | GreenCloudVPS | annual, USD 45.00/yr | not published | stock; no refund on any line |
| 4.00 | 1 / 512 MiB / 10 GiB | DigitalOcean | hourly capped, USD 4.00/mo | list price | 512 MiB cannot hold a JVM or a browser |
| 4.00 | 1 / 1 GiB / 20 GB | Kamatera | monthly or hourly, USD 4.00/mo | list price | the record's own 24/7 column says USD 19.73 for this shape |
| 4.00 | 1 / 2 GiB / 10 GB | HostHatch | monthly, from USD 4.00/mo | same standing rate | a "from" price: the per-location and annual figures sit behind the console login |
| 4.54 | 2 / 4 GiB / 40 GB | OVHcloud | starting at, longest commitment | not published | the term behind the figure is unknown; 500 Mbps port |
| 5.00 | 2 / 512 MiB / 20 GB | AWS Lightsail | monthly, USD 5.00/mo | list price | 0.5 GiB and 1 TB; the next rung is USD 7 |
| 5.00 | 1 / 2 GiB / 60 GB | IONOS | 1-year term, USD 2/mo for 3 months | USD 6.00 | the year costs USD 60, not USD 24 |
| 5.28 | 4 / 8 GiB / 100 GB | Contabo | 24-month term, USD 5.28/mo | USD 6.60 list | leaving early costs the remaining term |
| 6.19 | 4 / 8 GiB / 75 GB | AlphaVPS | annual, EUR 5.52/mo, EUR 66.20/yr | flat at renewal | annual prepay to a small operator; the refund is first-order and unused only |
| 6.57 | 2 / 4 GiB / 80 GB | netcup | 6-month contract, EUR 5.86/mo incl VAT | list price | a 6-month term on a 4 GiB machine |
| 6.64 | 1 / 2 GiB / 30 GB | Aeza | hourly capped, EUR 5.93/mo | not published | the record is `documented`; the storefront did not answer on 2026-10-24, and the EUR 1.99 promo is Stockholm, not a Russian region |
| 6.71 | 2 / 4 GiB / 40 GB | Hetzner Cloud | hourly capped, EUR 5.99/mo ex VAT | list price | CX23 was not available in either eu-central location |
| 7.20 | 6 / 12 GiB / 200 GB + 100 GB | Contabo | monthly, USD 7.20/mo | not published | the record states no term for this row; 300 Mbit/s port |
| 8.50 | 4 / 8 GiB / 75 GB | OVHcloud | starting at, longest commitment | not published | the same unknown term as VPS-1 |
| 10.64 | 4 / 8 GiB / 160 GB | netcup | 3-month contract, EUR 9.50/mo incl VAT | list price | a 3-month term for the same 8 GiB as the USD 3.75 row |
| 13.44 | 8 / 24 GiB / 300 GB + 150 GB | Contabo | monthly, USD 13.44/mo | not published | the record states no term for this row; 600 Mbit/s port |
| 18.67 | 8 / 16 GiB / 320 GB | netcup | 2-month contract, EUR 16.66/mo incl VAT | list price | 16 GiB where Contabo sells 24 GiB for less |
| 19.90 | 8 threads / 32 GiB / 2 x 2 TB | Kimsufi | monthly, USD 19.90/mo | list price | available in 3 of 9 regions; the install queue |
| 34.58 | 16 / 32 GiB / 640 GB | netcup | 1-month contract, EUR 30.86/mo incl VAT | list price | 16 vCPU on a shared host is a scheduling claim, not a clock |
| 35.50 | 8 threads / 64 GiB / 2 disks | Kimsufi | monthly, USD 35.50/mo | list price | regional scarcity; 500 Mbps public port |

⭐ The table refuses its own headline. The cheapest row is not the best row:
ServerHost at USD 1.42 buys 2 GiB for USD 0.71 per GiB, and GreenCloudVPS at
USD 2.08 buys 4 GiB for USD 0.52 per GiB. Sixty-six cents separates the two invoices
and the larger invoice returns twice the memory. A reader who sorts on the first
column and stops has bought the worse machine.

OVHcloud is not the floor at its own provider: `ovhcloud` prices the Public Cloud
b2-7 at USD 31.19 for 2 vCore and 7 GB, which the VPS-1 row undercuts by 6.9 times.

⚠ The `not published` cells are the honest state. ServerHost and GreenCloudVPS
record no renewal rate at all, and BuyVM carries the same USD 24.00 in its renewal
field as in its first payment without stating a renewal term, so for all three the
second year is unknown from the page that sells the first. The other three do
publish one: RackNerd a lifetime recurring rate, CloudCone a standing rate the terms
let it raise on 45 days' notice, and AlphaVPS a rate it states is locked forever.
IONOS is not the only row where a promotional rate and a later rate sit side by
side: Contabo's own structured data prints USD 5.28 against a USD 6.60 list.

## The ceiling at each price band

The largest verified shape in each band, with the unit arithmetic beside it.
`USD/GiB` is the monthly bill divided by the memory, and `USD/vCPU` the monthly bill
divided by the thread count. A band runs from the previous ceiling to its own
figure, so the USD 2 row carries USD 2.08, the first invoice above the line that
returns more than 2 GiB. Every row here is a machine with a root shell. One shape
outside that class is larger: `huggingface-spaces-cpu-basic` lists 2 vCPU and 16 GB
at USD 9.00 a month, and it is a Space on a paid plan rather than a host, so it does
not enter the ladder.

| Band | Largest shape | Provider | USD/month | USD/GiB-month | USD/vCPU-month |
| --- | --- | --- | --- | --- | --- |
| USD 2 | 2 vCPU / 4 GiB / 35 GB | GreenCloudVPS | 2.08 | 0.52 | 1.04 |
| USD 5 | 4 vCPU / 8 GiB / 60 GB | GreenCloudVPS | 3.75 | 0.47 | 0.94 |
| USD 10 | 6 vCPU / 12 GiB / 300 GB | Contabo | 7.20 | 0.60 | 1.20 |
| USD 20 | 8 threads / 32 GiB / 4 TB | Kimsufi | 19.90 | 0.62 | 2.49 |
| USD 50 | 8 threads / 64 GiB / 2 disks | Kimsufi | 35.50 | 0.55 | 4.44 |

At exactly USD 2.00 the ceiling is ServerHost's 2 GiB for USD 1.42. The USD 2 row
above is 4 GiB for USD 0.66 more, which is the best marginal return in the table. At
USD 5 the ceiling is 8 GiB for 1.80 times the money, which is 4 GiB more for
USD 1.67. At USD 10 the ceiling is 12 GiB for 1.92 times the USD 5 row, and the
memory grows only 1.5 times, so the USD 10 band is where the curve turns against the
buyer. At USD 20 the ceiling is 32 GiB for 2.76 times the USD 10 row, and the memory
grows 2.67 times, which is linear. At USD 50 the ceiling is 64 GiB for 1.78 times
the money and twice the memory.

The per-GiB rate stays between USD 0.47 and USD 0.62 across all five bands. Money
above USD 10 buys a larger ceiling, a faster port and a shorter contract, not a
cheaper unit of memory. That is the least obvious fact on this page: the annual
low-end lane is already at its floor price per GiB at USD 3.75, and every step above
it is a payment for capacity or flexibility. One row outside the five bands beats
that floor and it is not a VPS with an address: `tierhive-micro` is USD 0.80 per GiB
at USD 0.10 for 128 MiB, which is a NAT container, and the band belongs to
[`under-one.md`](under-one.md).

The public clouds invert the arithmetic. Vultr charges USD 2.50 for 512 MiB, which
is USD 5.00 per GiB-month. DigitalOcean charges USD 4.00 for the same 512 MiB, which
is USD 8.00 per GiB. AWS Lightsail charges USD 5.00 for 512 MiB, which is USD 10.00
per GiB. Against GreenCloudVPS at USD 0.47, the three entry rungs cost 10.6, 17.1
and 21.3 times as much for the same unit of memory. What the difference buys is an
API, an address that is already trusted, and a monthly cancellation.

## Per hour against per month

The floor for a burst is not the floor for a daemon. Per-second billing makes a
40-minute job nearly free and makes a 24/7 service the most expensive way to buy a
machine in this slice.

| Rate | Shape | 730 hours | Source of the rate |
| --- | --- | --- | --- |
| EUR 0.0006/h | 1 vCPU / 1 GiB, storage and IPv4 excluded | EUR 0.44, USD 0.49 | Scaleway STARDUST1-S |
| USD 0.0069/h at list, USD 0.0207/h as a Sandbox | 0.125 core / 128 MiB, the minimum container | USD 5.04 at list, USD 15.14 as a Sandbox | Modal |
| USD 0.0162/h | 2 vCPU / 4 GiB | USD 11.83 | Lizard small |
| USD 0.0324/h | 4 vCPU / 8 GiB | USD 23.65 | Lizard medium |
| USD 0.0289/h | RTX 3060 Ti, 8 GB VRAM class; the record carries no core or RAM figure | USD 21.10 | Vast.ai, measured |
| USD 0.018/h | 2 vCPU / 4 GiB / 12 GB | USD 13.14 | boat small |
| USD 0.036/h | 4 vCPU / 8 GiB / 50 GB | USD 26.28 | boat default |

Scaleway's Stardust is the cheapest per-hour row in the table above: 0.0006 multiplied
by 730 is EUR 0.44 a month for a running instance. The instance is not the product. A
public IPv4 is billed at EUR 0.005 an hour, which is EUR 3.65 a month, and 0.005
divided by 0.0006 is 8.3. The address costs 8.3 times the compute. Add the two and
the month is EUR 4.09, or USD 4.58, for 1 vCPU and 1 GiB before storage. The hourly
floor is real and the monthly total is not the number in the headline. The one row in
the corpus that undercuts it per hour is `tierhive-micro` at USD 0.000135 an hour,
and that is a 128 MiB container behind NAT ports rather than a machine with an
address.

Modal is the cheapest per-second sandbox in the slice only if the comparison is a
Function. The page prints both rate columns, read on 2026-10-24: preemptible CPU at
`$0.0000131 / core / sec` and memory at `$0.00000222 / GiB / sec`, against
non-preemptible CPU at `$0.00003942 / core / sec` and memory at `$0.00000667 / GiB /
sec`, and it states `Sandboxes are billed at non-preemptible rates of 3x list
price`. A physical core is 2 vCPU. The list rate is therefore USD 0.0473 per
core-hour and USD 0.008 per GiB-hour, and the minimum container, `*minimum of 0.125
cores per container`, is USD 0.0069 an hour at list and USD 0.0207 an hour at the
Sandbox rate. Starter includes `$30 / month` of compute, so 30 divided by 0.0207 is
1,446 Sandbox hours, not the 4,348 that the list rate gives.

The same arithmetic at a usable shape is the argument against per-second for a
daemon. Four cores at USD 0.0473 plus 8 GiB at USD 0.008 is USD 0.2532 an hour at
list, and USD 0.7597 an hour at the Sandbox rate. Multiplied by 730 that is
USD 184.84 a month at list and USD 554.61 as a Sandbox, against USD 3.75 for the
GreenCloudVPS box of the same shape, a factor of 49 at list and 148 as a Sandbox.
Lizard is cheaper at 4 vCPU and 8 GiB, and its USD 0.0324 an hour is USD 23.65 a
month, which is still 6.3 times the annual host at the same shape.

### Where a month stops being hourly

A monthly-capped instance bills the hourly rate until the cap, then stops. The
break-even is the cap divided by the hourly rate, and it is close to a full month on
every provider that publishes both numbers.

| Provider | Cap | Hourly | Break-even |
| --- | --- | --- | --- |
| Vultr, IPv6 rung | USD 2.50 | USD 0.004 | 625 hours |
| Hetzner CX23 | EUR 5.99 | EUR 0.0096 | 624 hours |
| DigitalOcean 512 MiB | USD 4.00 | USD 0.00595 | 672 hours |

730 hours is a month. The cap is reached after 624 hours at Hetzner, 625 at Vultr
and 672 at DigitalOcean, which is 85 to 92 per cent of a month. A machine destroyed
before that point bills less hourly than the monthly plan. Past it the cap charges
the monthly figure, so the hourly rate decides nothing.

## The dedicated floor

Kimsufi KS-5 is USD 19.90 a month for a named Xeon E3-1270 v6 with 4 cores and
8 threads, 32 GiB of memory, 2 x 2 TB of disk and a 300 Mbps public port. It is the
cheapest dedicated machine in this lane that carries 32 GiB, not the cheapest
dedicated row in the corpus. `ovhcloud-kimsufi` records the cheapest orderable KS SKU
at EUR 16.99 in Singapore, USD 19.04 at the rate above, metered at 25 TB a month
because the European stock is empty. `oneprovider` lists an Atom C2350 with 4 GB and
1 TB at USD 14.28 in Paris, and `phoenixnap-dedicated-outlet` opens at EUR 89.99.
`hetzner-dedicated` carries no shape and no price in its structured fields and its
two price columns disagree by a factor of 2.4, but its notes price the AX41 at
EUR 59.00 for a Ryzen 5 3600 with 64 GB and two 512 GB NVMe, so it is rankable by
reading the note rather than the field.

The honest comparison splits the bill into two rates, and it does not favour the
dedicated box on CPU. A Contabo Cloud VPS 4 at USD 5.28 a month gives 4 vCPU and
8 GiB, which is USD 1.32 per vCPU and USD 0.66 per GiB. The Kimsufi box gives
8 threads and 32 GiB for USD 19.90, which is USD 2.49 per thread and USD 0.62 per
GiB. For a compute-bound job that fits in 8 GiB, the dedicated box costs 3.8 times
as much in total for twice the threads, and 1.9 times as much per thread. It is
cheaper per GiB. A named Xeon E3-1270 v6 at USD 19.90 is not a cheaper CPU than a
shared 4-vCPU VPS at USD 5.28. It is cheaper memory.

What the USD 19.90 actually buys is the ceiling. No VPS row below USD 19.90 in this
lane reaches 32 GiB, and none reaches 4 TB of local disk: the nearest VPS is Contabo
at USD 13.44 for 24 GiB and 300 GB. A job that needs more than 24 GiB resident, or
more than 300 GB on local disk, has no cheaper row anywhere in this table. A job
that needs neither is paying for capacity it does not use.

The comparison holds at the top too. KS-5-B is USD 35.50 for 64 GiB and a 500 Mbps
port, which is USD 0.55 per GiB, and netcup's 16 vCPU / 32 GiB row is USD 34.58 at
USD 1.08 per GiB. The dedicated lane is 1.9 times cheaper per GiB at the USD 35
level and more expensive per thread at the USD 20 level. Neither lane dominates.

## What the floor costs in risk

Every cheap row carries a term, a stock position or an unpublished number. The catch
belongs beside the price, because a reader who learns it after the invoice has
already paid for it.

| Row | The catch |
| --- | --- |
| ServerHost, USD 1.42 | The page is a campaign URL with the promo code in the link. No renewal rate is printed anywhere, so the second year is unknown. |
| RackNerd, USD 1.83 | Prepaid annually. A failed renewal loses the whole year rather than a month, and no refund term is published on the specials page. |
| GreenCloudVPS, USD 2.08 and USD 3.75 | Every card states `No refund/Money back on this plan`, and several locations show `0 Available`. Stock is the real gate. |
| CloudCone, USD 2.33 | The annual figure is the standing price, not a promo, but the terms let CloudCone raise it at the start of any renewal term on 45 days' notice, with silence treated as acceptance. The same provider has a second record built from a disk-wiping incident, and the two were never reconciled. |
| netcup, USD 2.48 | The 12-month contract sits on the cheapest rung. The contract period falls as the price rises, so the least flexible plan is the one at the floor. |
| Vultr, USD 2.50 | IPv6 only. The IPv4 shape is USD 3.50, so the floor for anything that needs an A record is a dollar higher. |
| Datalix, USD 2.75 | 21 of the 24 advertised rungs across the four KVM pages are marked `Ausverkauft`, and the in-stock set is three Ryzen GEN 2 rows. Stock is the gate before price is. |
| AlphaVPS, USD 2.85 | Annual prepay. The 14-day refund is a first order, unused only, and excludes promo and China orders, so a used machine has no exit. |
| `ionos-2`, USD 5.00 | The USD 2 headline is a 3-month rate. Three months at USD 2 and nine at USD 6 is USD 60 for the year, and then USD 6 a month. |
| Contabo, USD 5.28 | A 24-month term. Leaving early costs the remaining term, and the USD 5.28 is 20 per cent below the USD 6.60 list price in the page's own structured data. |
| Hetzner Cloud, USD 6.71 | CX23 was `not available` in both eu-central locations at the time of reading. The price is a price without stock. |
| Kimsufi, USD 19.90 | Available in 3 of 9 regions. The install queue is the difference between the price and a working machine. |
| Vast.ai, USD 0.0289/h | The rate moves between calls: the 0.0287 row below it carried reliability 0.811 while this one carried 0.999, and the host can preempt the instance at any time. |

⚠ The identity column is thin, and that is a gap in the records rather than a clean
bill. Twenty-six records in `dossier/compute` carry `identity_cost.kind:
national-id`, so a passport or a resident document is a real door somewhere in this
topic: `autodl` states real-name certification with a PRC identity card, a bank card
or an overseas passport, and `chamaoyun` states an age band of 18 to 25 plus a
mainland ICP filing. None of those twenty-six is a row in this table, so no row here
is known to demand a document. What the table's rows do record is a card, an email
or nothing: `ionos-2` gives `email`, and `ionos-vps-s-plus` says a payment method is
asked for at order and that the payment page was not read. Identity beyond that is
`unverified` at every row above, which is not the same as absent.

⚠ One row is a record built from an incident rather than a signup. The `cloudcone`
record grades the provider `reported`, gives `identity_cost` as `institution`, and
says the signup route was not read. The price in the ladder comes from a different
record at the same vendor, which read the plan card and graded it `documented`. Both
cannot describe the same account door.

## What is not below the floor

A verified full VPS does exist below USD 1.42 a month, and twelve of them sit under
USD 1.00. The lowest is `tierhive-micro` at USD 0.10 a month for 1 vCPU, 128 MiB and
1 GB, which the vendor prints as `$0.10/mo` against an hourly 0.000135, and it is
`documented`. The cheapest with a dedicated IPv4 is `dedirock-promo-vps-saver` at
USD 0.82 a month on annual prepay, USD 9.88 out of pocket. Between those and the
USD 1.42 row sit `luo-cloud-lxc-nat`, `virnat-us-256-kvm`, `gullos-hosting-nat-128`,
`c-servers-nanovps-384-us`, `natkvm-nat-lxc`, `scaleway-stardust1-s`,
`cheap-host-nat-start`, `softshellweb-lxc-ipv6-only`, `hostbrr-ipv6-1g` and
`c-servers-nanovps`. [`under-one.md`](under-one.md) prices that band and owns it;
this document's ladder starts where a full 2 GiB machine begins, which is ServerHost
at USD 16.99 a year.

What is genuinely absent below USD 1.42 is a machine with a dedicated IPv4 and
2 GiB of memory. `dedirock-promo-vps-saver` has the address and 1 GiB;
`hostbrr-ipv6-1g` has the memory and no IPv4; the rest are NAT containers, IPv6-only
guests or 128 to 384 MiB. That gap, not the floor, is the finding.

The free lane is not cheaper, it is a different product. Oracle Cloud returns
2 OCPU and 12 GiB at zero cost, but an instance idle over a 7-day window may be
reclaimed. Google returns one e2-micro with 1 GiB and 1 GB of monthly egress, with
no idle reaping. InstaBox returns one 4 vCPU / 8 GiB machine a month that pauses
after 30 idle minutes. Modal returns USD 30 of compute a month that resets and does
not roll over. Each of those is an allowance with a clock or a reclaim rule, and none
of them is an invoice under USD 1.42. A reader who needs a machine that stays up and
answers pays the floor.

The free lane also loses rows, and one loss is recorded. The `digitalocean-2`
student credit of USD 200 was withdrawn: DigitalOcean left the GitHub Student
Developer Pack and every credit issued through it expired on 2026-07-31. A free
route that closed is not a floor candidate, and the record keeps it so nobody
re-opens the search.

The four conditions this page sets for a row under USD 1.42 are met by rows in
[`under-one.md`](under-one.md). A vendor page with a named shape, an annual
price under USD 16.99 and a published renewal: `gullos-hosting-nat-128` is USD
3.50 a year for a 128 MiB NAT container and the page prints the same USD 3.50
as the renewal, and `virnat-us-256-kvm` is USD 2.80 a year. A documented
campaign that survives a second renewal at the same rate: the same Gullo's
page, and `hostbrr-ipv6-1g` at USD 10.50 a year, where the order page sells
one, three and twelve months of the same machine at a consistent rate with no
strike-through, though the record states that no renewal rate is published. A
free allowance with no idle reclaim: `google-cloud-free-tier` records no idle
reaping, so that one is met and rejected on the egress rather than on the
clock. A provider selling below cost to fill a region, which is how the
ServerHost rate was set, is still the mechanism behind `servitro-1gb` at USD
12.00 a year, `reported` rather than `documented`.

⚠ The floor moves. `vast-ai-listing-structure` records three 8 GB-VRAM rows on
2026-10-22 at dph_total 0.0287, 0.0289 and 0.0296, so the rate is a snapshot of one
page rather than a constant. A figure of USD 0.0222 appears in no record in
`dossier/compute` and is `unverified`. ServerHost's USD 16.99 sits on a page whose path ends in
`serverhost-fb-ad-june.html`, so the figure is a campaign rate rather than a list
rate, and the same record puts the monthly list price for that 2 GB shape at USD 6.00
against the USD 16.99 year. A floor is a snapshot with a date, not a constant.

## Where the records disagree

These are the contradictions among the records this page rests on. Two are resolved in
the records and the rest remain open.

| Records | What disagrees |
| --- | --- |
| `cloudcone` against the same vendor's plan card | The record gives verdict `qualifies-with-caveat`, confidence `reported`, identity `institution` and binding `none`, from a data-loss incident. `cloudcone-ssd-vps-1` gives USD 28/yr, `documented`, card, volume-quota. Both cannot describe the same account door. |
| `hetzner-cloud` against the page read today | Resolved in the record on 2026-10-24: `m24h_usd` is USD 6.70, the corpus conversion of EUR 5.99 at 1.1193. The USD 6.49 is Hetzner's own USD conversion of the same CX23 plan, and the 0.21 gap is the vendor's FX rate, not a second machine. |
| `scaleway` against `scaleway-2` | The first records a floor of EUR 0.01428/h, about EUR 10.42 a month. The second records STARDUST1-S at EUR 0.0006/h, 23.8 times cheaper. Two records, one provider, one floor. |
| `vultr` against `vultr-2` | The first carries a 24-hour figure of USD 20.00 with no shape. The second records the entry rung at USD 2.50. The corpus figure is 8 times the real floor. |
| `digitalocean` against the droplet table | The record's 24-hour column is USD 24.00, which is the 4 GiB droplet. The entry rung is USD 4.00. |
| `contabo` against today's page | The record holds USD 6.60 at 4 vCPU / 8 GiB / 100 GB with binding `request-rate`, and its own `binding_note` says the binding thing is unlimited traffic with no published rate. The page also offers USD 5.28 on a 24-month term, which is 20 per cent below that list price. The port speed is in the record's evidence and not in its structured field. |
| `kamatera` inside itself | The stated entry price is USD 4.00 a month for 1 vCPU and 1 GiB. The same record's 24-hour column is USD 19.73, which is above its own monthly cap. The `price_note` says the column respects the cap. |
| `modal` against its own rate table | The record's `m24h_usd` is USD 9.99 and its `price_arithmetic` derives USD 0.0473 per core-hour and USD 0.0080 per GiB-hour from the vendor's worked example, treating the rate as `inferred`. The page prints the rate lines, so the derivation is no longer needed, and at the printed Sandbox multiplier the 2 vCPU / 4 GiB shape is USD 0.238 an hour, which is USD 173.74 a month and not the USD 9.99 in the field. |
| `kimsufi` shape field | The shape says 4,096 GiB of disk for a page that sells 2 x 2 TB. That is a decimal figure converted to a binary one, which the unit rule forbids. |
| `ionos-2` against the same page | The record gives binding `none` and identity `email`. `ionos-vps-s-plus` describes the same product as asking for a payment method at order, and records the 60 GB NVMe disk that fills first. A card is not stated as required anywhere read. |
| `hetzner-dedicated` | The free-tier field says a card records a free tier without a credit, the kind is `none`, and no price or shape is in the structured fields. Its two price columns are USD 32.25 and USD 77.40 for the same row. Its notes do price the AX41 at EUR 59.00, so the shape exists in prose and not in the field. |

## Evidence

The prices in the ladder come from the pages each finding read, and the records
carry two read dates rather than one: the 2026-10-22 read and a re-read on
2026-10-24 for `hostbrr`, `datalix`, `aeza`, `alphavps-c2g`, `alphavps-c6g`,
`digitalocean-droplet-1gb`, `ionos-vps-s-plus`, `cloudcone-ssd-vps-1`,
`hetzner-cloud`, `contabo` and `scaleway-stardust1-s`. Every figure above carries
the date of the record it came from, not a single date for the page. The pages that
carry the arithmetic are
`racknerd.com/specials`, `buyvm.net/kvm-dedicated-server-slices/`,
`cloudcone.com/vps/`, `greencloudvps.com/billing/store/budget-kvm-sale`,
`alphavps.com/cheap-vps`, `ionos.com/servers/vps`, `contabo.com/en-us/pricing/`,
`kimsufi.com/en/`, `us.ovhcloud.com/vps/`, `hetzner.com/cloud/cost-optimized/`,
`netcup.com/en/server/vps-lite`, `hostbrr.com/vps.html`, `aeza.net/virtual-servers`,
`scaleway.com/en/pricing/virtual-instances/`, `modal.com/pricing`,
`lizard.build/pricing`, `boat.dev/pricing` and `vast.ai`. This document read the
records and their quoted rows, not the vendor pages themselves, with one exception:
`modal.com/pricing` was read on 2026-10-24 for the rate lines quoted above, because
the record said the rate was not printed and the page prints it.

The rate is the one exception: `api.frankfurter.dev/v1/2026-10-22?base=EUR&symbols=USD`
returned `{"base":"EUR","date":"2026-10-22","rates":{"USD":1.1205}}` when read on
2026-10-24, and every EUR to USD conversion here divides by that single figure. The
`/v1/latest` endpoint answers a different question and returns a different number:
on the same day it returned EUR 1 = USD 1.1193 dated 2026-10-23, which is the rate
several records used. A reader who needs a different rate can recompute each row
from the native price in the `Billed as` column.

Evidence: `dossier/compute/serverhost-2gb-promo.json`,
`dossier/compute/greencloudvps.json`, `dossier/compute/hetzner-cloud.json`,
`dossier/compute/scaleway-2.json`, `dossier/compute/modal.json` and
`dossier/compute/kimsufi.json` for the shapes above;
`dossier/compute/aws-lightsail.json`, `dossier/compute/digitalocean-droplet-1gb.json`,
`dossier/compute/vultr-2.json`, `dossier/compute/alphavps-c2g.json`,
`dossier/compute/racknerd-1gb-special.json`, `dossier/compute/buyvm-slice-512.json`
and `dossier/compute/hostbrr.json` for the entry rungs;
`dossier/compute/ovhcloud-2.json`, `dossier/compute/ovhcloud-vps-1-2027.json`,
`dossier/compute/netcup.json`, `dossier/compute/contabo.json`,
`dossier/compute/contabo-cloud-vps-4.json`, `dossier/compute/greencloud-budget-kvm-8gb.json`,
`dossier/compute/hosthatch-nvme-2gb.json` and `dossier/compute/aeza-waws-1.json` for
the mid ladder; `dossier/compute/boat.json`, `dossier/compute/lizard.json`,
`dossier/compute/scaleway-stardust1-s.json`, `dossier/compute/instabox.json`,
`dossier/compute/oracle-cloud.json`, `dossier/compute/google-cloud-free-tier.json`
and `dossier/compute/vast-ai-listing-structure.json` for the free and per-second
lanes; `dossier/compute/ovhcloud-kimsufi.json`, `dossier/compute/oneprovider.json`
and `dossier/compute/phoenixnap-dedicated-outlet.json` for the dedicated floor;
`dossier/compute/datalix.json`, `dossier/compute/cloudcone-ssd-vps-1.json`,
`dossier/compute/ionos-2.json` and `dossier/compute/ionos-vps-s-plus.json` for the
rows with an open corner; `dossier/compute/tierhive-micro.json`,
`dossier/compute/dedirock-promo-vps-saver.json`, `dossier/compute/luo-cloud-lxc-nat.json`,
`dossier/compute/virnat-us-256-kvm.json`, `dossier/compute/gullos-hosting-nat-128.json`,
`dossier/compute/c-servers-nanovps.json`,
`dossier/compute/c-servers-nanovps-384-us.json`, `dossier/compute/natkvm-nat-lxc.json`,
`dossier/compute/cheap-host-nat-start.json`,
`dossier/compute/softshellweb-lxc-ipv6-only.json`,
`dossier/compute/hostbrr-ipv6-1g.json` and `dossier/compute/servitro-1gb.json` for the
band under USD 1.00 that [`under-one.md`](under-one.md) owns;
`dossier/compute/hetzner-dedicated.json`, `dossier/compute/ovhcloud.json`,
`dossier/compute/scaleway.json`, `dossier/compute/vultr.json`,
`dossier/compute/digitalocean.json`, `dossier/compute/kamatera.json` and
`dossier/compute/cloudcone.json` for the contradictions above.
