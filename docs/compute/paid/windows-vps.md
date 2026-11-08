# Windows VPS: the cheapest machine that runs Windows at 16 GiB, 4 vCPU and 50 GB

The cheapest machine found that runs Windows at the minimum is **Layer7's AMD
Epyc Cloud Server VPS in Frankfurt at EUR 9.06 a month, which is USD 10.14**, or
**EUR 86.97 a year, which is USD 8.11 a month**, for 4 cores, 16 GiB of RAM and 80 GB of
NVMe. The OS list carries a Windows Server 2019 or 2022 Evaluation image at EUR 0.00.
Both totals are arithmetic on the vendor's own option deltas, not a printed plan, and the
table labels them so. The first payment on the annual term is USD 97.35, and an
evaluation image stops working after its period.

Vendor pages were read on 2026-10-26 and drew on at least 316 distinct provider
labels (339 first-column keys, reduced to 316 after removing generic labels and spelling
variants of one brand). The ranked table holds seventeen of them.

⛔ **Two earlier claims were wrong in a way that flattered a row.** Rabisu's licence was
recorded as included on a vendor FAQ sentence that does not reproduce on a re-read of the
configurator, the home page or the knowledge base. The licence status of that row is
unresolved, and this document does not claim a bundled licence. InterServer at USD 40.00
was named as the cheapest row whose licence the provider supplies; Virtarix sells the same
class of row at USD 27.40, with the licence printed as a USD 16.00 component inside the
price.

## The ranked answer

The sort key is the cheapest rate the vendor prints on any cycle. `Monthly` is
the rate on the shortest cycle. `First payment` is the cash due at order on
the cycle that produces the best-term figure. The last column names the record
in `dossier/compute/`. Every ranked row has one. All prices were read on
2026-10-26.

⚠ **The monthly column is not monotonic, and that is deliberate.** Rank 6 costs
USD 19.02 a month and rank 7 costs USD 16.00. The order follows the best-term column. A
reader who will not prepay must re-sort on the monthly column before choosing.

| # | Provider | Plan | vCPU | RAM (GiB) | Disk (GB) | Windows path | Monthly (USD) | Best term (USD) | First payment (USD) | Rung | Record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Layer7 | AMD Epyc, Frankfurt | 4 | 16 | 80 | 2019 or 2022 Evaluation image at EUR 0.00; expires | 10.14 (arithmetic) | 8.11 annual (arithmetic) | 97.35 annual; 10.14 monthly | documented monthly, inferred annual | `layer7-windows` |
| 2 | Saganetwork | VDS-16GB | 6 | 16 | 120 | FAQ says Windows installable; the cart has no OS field | 8.23 ex VAT | 8.23, no term discount | 9.88, KDV included | documented price, row unverified | `saganetwork-windows` |
| 3 | Rabisu | Aydin VPS x16 | 6 | 16 | 120 | Windows 2012R2, 2019 and 2022 in the OS list, no surcharge; licence unstated | 10.99 | 8.79 annual | 105.48 annual; 10.99 monthly | reported | `rabisu-windows` |
| 4 | NetVolo | VPS-Windows-3 | 4 | 16 | 200 | Windows product line; licence conditional, this plan page silent | 13.98 | 13.98 on a 3-year invoice | 503.48 on the 3-year invoice | documented | `netvolo-windows` |
| 5 | HOSTKEY | vm.v2-medium | 8 | 16 | 160 | Windows image list; licence sold separately, price unpublished. EUR 14.00 on the English storefront, RUB 3,390 on the Russian one (USD 42.02) | 15.67 | 15.67, monthly only | 15.67 | documented, with a failed EN re-read | `hostkey-windows` |
| 6 | By-Hoster | Windows - Plus | 8 | 16 | 250 | Windows installed at no charge; the buyer brings the licence | 19.02 incl VAT | 15.84 yearly | 190.09 yearly; 19.02 monthly | documented | `by-hoster-windows` |
| 7 | Linveo | Intel KVM 16GB Windows | 6 | 16 | 100 | Windows SKU, USD 5.00 above the Linux twin; licence not stated | 16.00 | 16.00, single cycle | 16.00 | documented | `linveo-windows` |
| 8 | Virtarix | WIN VPS M | 6 | 16 | 100 | licence printed at USD 16.00 and folded into the plan | 27.40 | 24.66 on 12 months | 32.70 first month; 275.65 on 12 months | documented | `virtarix-windows` |
| 9 | ServerPacket | Windows VPS 16 GB | 6 | 16 | 100 | page claims Windows licensing is included | 32.19 | 32.19, no term discount | 386.28 on 12 months | documented | `serverpacket-windows` |
| 10 | windowsvps.host | DeluxeBox | 4 | 16 | 125 | page claims the licence is included, Datacenter edition | 36.00 | 36.00, single cycle | 36.00 | documented | `windowsvps-host-windows` |
| 11 | SteadyVPS | Hyper-V4 | 4 | 16 | 120 | page claims the licence is included | 38.00 | 38.00 | 38.00 | documented | `none` |
| 12 | InterServer | Windows Cloud Compute, 8 slices | 4 | 16 | 320 | Windows SKU; licence not printed anywhere | 40.00 | 40.00, monthly | 40.00 | documented | `interserver-windows` |
| 13 | Contabo | Cloud VPS 8 plus Windows Datacenter 2025 | 8 | 24 | 300 | add-on at EUR 28.00, printed | 47.01 | 47.01 | 47.01 | documented | `contabo-windows` |
| 14 | Time4VPS | Windows 16 | 4 | 16 | 200 | included free, printed | 52.88 | 52.88 at renewal | 26.44 first month | documented | `time4vps-windows` |
| 15 | OVHcloud | VPS-4 2027 plus Windows Server 2025 | 8 | 24 | 200 | add-on at EUR 28.00, from the catalogue API | 57.63 | 57.63 | 57.63 | documented | `ovhcloud-windows` |
| 16 | CloudCone | WC2-3, Windows Cloud Compute | 4 | 16 | 240 | supplied by the SKU, not printed | 62.75 | 62.75 | 62.75 | documented | `cloudcone-windows` |
| 17 | Kimsufi | KS-3, rented dedicated | 4 | 32 | 480 | licence printed at USD 34.00 on a USD 30.00 box | 64.00 | 64.00, monthly | 64.00 | documented | `kimsufi-windows` |

**Seventeen rows clear 16 GiB, 4 vCPU and 50 GB with a purchasable Windows path.** Two of
them print a priced licence, at USD 16.00 and USD 34.00. One prints the Windows layer by
implication at USD 5.00. One sells an evaluation image. One installs Windows for a buyer
who brings a licence. Several sell the licence separately at a price the page does not
print. The rest rely on a page sentence. The Windows path column decides what a buyer
actually pays, and no other column can stand in for it.

⚠ **The second table repeats the licence-supplied subset in licence-detail form.** It is
not a second ranking and it contains no row that is not in this table, except Windows 365,
which is a managed desktop with no address and is excluded here for that reason.

### Where each row's price came from

1. `account.layer7.net/shop/amd-epyc-cloud-server-vps-germany-frankfurt-main` (read 2026-10-26): the base price, the two option deltas, the four cycle cards and the OS list.
2. `saganetwork.net/vds-kiralama.html` and its cart at `saganetwork.net/odeme/index.php?rp=/store/sanal-sunucu/sanal-sunucu-vds` (read 2026-10-26): the 16 GB card and the rendered cart with the KDV line.
3. `rabisu.com/panel/store/vps/aydin-vps-x16` (read 2026-10-26): four cycle rates, the Windows entries in the OS list and the region surcharges.
4. `netvolo.com/en/hosting/vps-windows` (read 2026-10-26): the plan card data, the strike-through list rate and the three-year footnote.
5. `hostkey.com/vps/windows/` (read earlier on 2026-10-26; a re-read returned 403) and `hostkey.ru/vps/` (read 2026-10-26): the EUR card and the RUB card.
6. `by-hoster.net/en/cheap-windows-vps` (read 2026-10-26): the Plus card, the tax sentence and the statement that no licence is supplied.
7. `billing.linveo.com/order/main/packages/windows-kvm-vps/?group_id=13` and the Linux twin at `billing.linveo.com/order/config/index/intel-kvm-vps/?group_id=8&pricing_id=51` (read 2026-10-26): two printed prices for one machine.
8. `virtarix.com/vps/windows-vps/`, its checkout at `my.virtarix.com/opcheckout.php?pid=2&plan=M&cycle=monthly` and `virtarix.com/vps/linux-vps/` (read 2026-10-26): the OS template line at USD 16.00 inside the USD 27.40 total.
9. `serverpacket.com/windows-vps-hosting/` (read 2026-10-26): the card, the licence claim and the 12-month billing note.
10. `windowsvps.host/buy-rdp/` (read 2026-10-26): DeluxeBox at USD 36.00 with the licence claim. The store render for the same plan prints USD 37.00.
11. `interserver.net/vps/windows-vps.html` (read 2026-10-26): the 8-slice card, which carries no licence sentence.
12. `kimsufi.com/en/ks/ks-3/` (read 2026-10-26): the configure screen, where the box and the licence are two priced lines. The listing page is not the evidence for this row.

### What the dollar figures rest on

Three rates convert the non-USD rows. The four ranked euro rows were converted at one
rate, so they can be compared without adjusting.

| conversion | value | source and date | rows |
| --- | --- | --- | --- |
| EUR to USD | 1.1193 | ECB reference rate, 2026-10-23, the rate every record uses | the ranked euro rows and their first payments: Layer7, NetVolo, By-Hoster, HOSTKEY |
| TRY to USD | 0.020085 | `open.er-api.com/v6/latest/USD`, `time_last_update_utc` 2026-10-26T00:02:31Z, TRY 49.789069 | Saganetwork |
| RUB to USD | 0.012396 | the `hostkey-windows` record's FX read, `open.er-api.com`, 2026-10-26, USD 1 = RUB 80.673994 | HOSTKEY's Russian card |

⚠ **A rate of 1.1209 is 0.14 per cent higher and changes no rank.** At 1.1209 the same
rows give USD 10.16, 8.12, 14.01, 19.04, 97.48, 504.20 and 190.36; this table and every
record print 10.14, 8.11, 13.98, 19.02, 97.35, 503.48 and 190.09 at 1.1193. By-Hoster's
EUR 16.99 is USD 19.02 at 1.1193 and USD 19.04 at 1.1209, so the two differ by two cents
on that row only. A figure of 19.03 appears in one summary and no recorded rate reproduces
it.

## The USD 7 machine: real, and always a smaller machine

The USD 7 Windows VPS is not a scam and not a rounding error. It is the entry rung of the
same ladders, and every row on it misses at least one of the three minimums. The
minimums are 16 GiB of RAM, 4 vCPU and 50 GB of disk.

| Provider | Plan | vCPU | RAM (GiB) | Disk (GB) | Monthly (USD) | Which minimum it fails |
| --- | --- | --- | --- | --- | --- | --- |
| CheapWindowsVPS | Windows 4GB SSD | 2 | 4 | 60 | 5.50 with code 50LEB, list 11.00 | RAM by 12 GiB, vCPU by 2 |
| Hostmayo | Windows RDP 1GB | 1 | 1 | 20 | 7.00 | RAM by 15 GiB, vCPU by 3, disk by 30 GB |
| SteadyVPS | Hyper-V1 | 1 | 2 | 25 | 7.00, list 14.00 | RAM by 14 GiB, vCPU by 3, disk by 25 GB |
| Rabisu | Aydin VPS X12 | 4 | 12 | 90 | 7.19 on the annual term | RAM by 4 GiB |
| FastyCloud | Windows 30GB | 1 | 2 | 30 | 7.99 | RAM by 14 GiB, vCPU by 3, disk by 20 GB |

**The Rabisu X12 is the likely source of the USD 7 claim.** It clears vCPU at 4 and disk
at 90 GB, and it misses the RAM floor by 4 GiB. The next rung up, the X16, is 16 GiB at
USD 8.79 on the annual term, which is USD 1.60 a month more. That USD 1.60 is the whole
difference between the claim and the minimum.

The rows above were read on 2026-10-26. `hostmayo.com/vps-windows.php` prints the 1 GB
card, `steadyvps.com/windows-vps/` prints Hyper-V1 at USD 7.00 against a USD 14.00 list,
`fastycloud.com/windows-vps-hosting` prints Windows 30GB, and `rabisu.com/panel/store/vps`
prints the X12 rung. The CheapWindowsVPS 4 GB row at USD 5.50 with code 50LEB comes from a
LowEndBox listing, because the vendor's own page prints USD 10.50 a month for that shape.
It is the weakest citation on this table.

⚠ **The two cheapest rows on this table fail the vCPU minimum as well as the RAM one.**
CheapWindowsVPS at 5.50 is 4 GiB on 2 vCPU, and Hostmayo at 7.00 is 1 GiB on 1 vCPU. Both
are small Windows guests, not a 16 GiB machine at a discount.

⚠ **No 16 GiB Windows machine at USD 7 exists in any surface reached.** The
cheapest 16 GiB machine with a Windows path is USD 8.11 on the annual cycle, and the
cheapest without an annual commitment is USD 8.23 ex VAT at Saganetwork. The USD 7 figure
is close, and it is still not a row this table can print.

## What a licence costs, and why the machine is the cheap half

The licence is a fixed line. The machine is the variable. A 4 vCPU guest pays the same
licence as a 16 core server, because Microsoft's own guide sets a floor of 16 core
licences per server whatever the core count of the box.

| Channel | Product | Price | Monthly over 36 months |
| --- | --- | --- | --- |
| MyChoiceSoftware | Windows Server 2022 Standard, 16 core, one-off | USD 509.99 | USD 14.17 |
| TrustedTechTeam | Windows Server 2022 Standard, 16 core, one-off | USD 526.99 | USD 14.64 |
| CDW | Windows Server 2022 Standard, 16 core, Select Plus | USD 799.99 | USD 22.22 |
| Microsoft | Windows Server 2025 Standard, suggested MSRP, 16 core | USD 1,176.00 | USD 32.67 |
| MyChoiceSoftware | Windows Server 2022 Datacenter, 16 core, one-off | USD 2,499.99 | USD 69.44 |
| Microsoft | Windows Server 2025 Datacenter, suggested MSRP, 16 core | USD 6,771.00 | USD 188.08 |
| Microsoft Evaluation Center | Windows Server 2022 evaluation, Standard or Datacenter | USD 0 for 180 days | USD 0 for 180 days |

`mychoicesoftware.com` (read 2026-10-26): the product page prints USD 509.99 for the
Windows Server 2022 Standard 16 Core Licence, and USD 2,499.99 for the Datacenter 16 core.
`microsoft.com/en-us/windows-server/pricing` (read 2026-10-26): the suggested MSRP for 16
core licences is USD 1,176 for Standard and USD 6,771 for Datacenter, and a footnote states
that both prices are for 16 core licences. The TrustedTechTeam and CDW rows are reads from the
same day and were not reopened.

⭐ **USD 509.99, or USD 14.17 a month over 36 months, is the number to carry.** It is the
cheapest Standard 16 core price found. It is 43 per cent of Microsoft's
suggested MSRP, and the comparison is approximate because the cheap SKU is a 2022 product
from a reseller and the anchor is a 2025 suggested price.

Three things the licence price does not include. Client access licences are required for
every user or device that reaches the server, and no quote was obtained. Software
Assurance is separate. The cheap channels do not state whether the SKU is OEM, open
licence or Select, and the cheapest channel that names its programme is CDW at
USD 799.99, Select Plus.

⚠ **The evaluation image commits the buyer to an edition.** A Standard Core evaluation
converts only to retail Datacenter Core, so choosing the free image can decide which
licence must be bought later.

**What each vendor charges for the same Windows layer.** The spread is the finding, and it
is wider than the spread between the machines.

| Vendor | How the licence appears | Printed price | Basis |
| --- | --- | --- | --- |
| Linveo | Windows SKU against the Linux twin | USD 5.00 | 16.00 minus 11.00, two printed prices |
| Virtarix | OS template line inside the plan | USD 16.00 | printed; the Linux twin is 11.40 and 11.40 plus 16.00 is 27.40 |
| Kamatera | Windows Server add-on | USD 19.00 | printed add-on |
| Contabo | Windows Server Datacenter 2025 | EUR 28.00 | printed add-on on the configurator |
| OVHcloud | Windows option on the VPS range | EUR 28.00 | OVH's public catalogue API, not the VPS page |
| Kimsufi | Windows Server 2016 Standard, 4 core | USD 34.00 | printed configure option on a USD 30.00 box |
| Retail | Standard, 16 core, one-off | USD 509.99 | reseller page, 14.17 a month over 36 months |

⚠ **Layer7 plus a retail licence is USD 24.31 a month, not USD 10.14.** The arithmetic is
the floor row's 10.14 plus the 14.17 licence line. The document this replaces printed no
licence price at all, so its floor measured hardware and called the result Windows.

## The five cheapest rows in detail

### Layer7: EUR 9.06 a month, or EUR 86.97 a year

The configurator starts at EUR 4.90 for 2 cores, 8 GiB and 80 GB of NVMe on an AMD Epyc
host in Frankfurt. The option table prints EUR 1.92 for 4 cores and EUR 2.24 for 16 GiB,
and the summary closes: 1.92 plus 2.24 is 4.16 of options, and 4.90 plus 4.16 is 9.06. The
annual cards price the same build at EUR 47.04 base, EUR 18.43 for 4 cores and EUR 21.50
for 16 GiB, which is EUR 86.97 a year or EUR 7.25 a month.

The OS list carries `Windows 2019 Std EN Evaluation` and `Windows 2022 Std EN Evaluation`
at EUR 0.00, beside Linux and BSD images, and the plan also offers an individual ISO
mount and a VNC console. The base includes 50 TB of traffic a month, one IPv4, one IPv6
and a 1 Gbps port; 2.5 Gbps costs EUR 30 a month more.

⚠ **Both totals are arithmetic on the vendor's own prices, and the annual one is not
rendered.** The page's cycle cards keep printing the base rate of 4.90 or 47.04 because
they do not recompute for options, so EUR 86.97 comes from three printed annual
components. No tax line is printed anywhere on the summary, so whether 9.06 is gross or
net is not stated.

### Saganetwork: TRY 410 a month, which is USD 8.23 ex VAT and USD 9.88 paid

The product card prints 6 cores, 16 GiB of RAM, 120 GB of SSD, unlimited traffic on a
1 Gbps port and TRY 410 a month. The rendered cart builds the total from four lines: base
100, RAM 190, CPU 40 and disk 80, which is the printed 410. It then adds KDV at 20 per
cent, 82.00, and a setup fee of 0.00, for 492.00 due today. The four cycles are 100, 300,
600 and 1200, so the monthly term carries no discount and the price is not annual-only.

The USD figures are TRY 410 at 0.020085, which is 8.23, and TRY 492 at the same rate,
which is 9.88. A TCMB conversion at 49.7627 gives 8.24. The gap is the FX source and not
the page, and the recorded rate settles it at 8.23.

⛔ **This row is not a confirmed Windows row.** The cart has four option fields: RAM, CPU,
disk and an extra IP. It has no OS field at all. The product page's FAQ says Windows
Server can be installed, in Turkish prose, and no licence price is printed in the flow.
The row is ranked because the machine and the price are documented, and the Windows path
is `unverified` until a cart shows an OS choice.

### Rabisu: USD 10.99 a month, or USD 8.79 on the annual term

Aydin VPS x16 is 6 cores, 16 GiB of RAM, 120 GB of SSD, a shared 1 Gbps port and unlimited
traffic under a fair-use clause, with one IPv4. The configurator prints four cycle rates,
USD 10.99 monthly, 9.89 quarterly, 9.34 semiannual and 8.79 annual, and the monthly radio
carries `checked` in the served HTML. The annual term needs USD 105.48 up front.

The OS list carries Windows Server 2012R2, 2019 and 2022 as plain options with no price
suffix, while every region upgrade prints its surcharge in the option text. The two
included regions are Istanbul and Sofia. London, Dublin, Falkenstein, New York, Los
Angeles, Miami, Dallas and Beauharnois add USD 5.22 a month; Sydney, Singapore and Hong
Kong add USD 8.72; Karachi adds USD 22.12.

⛔ **The licence status of this row is unresolved, and no page read today states one.**
The configurator, the home page and the knowledge base return zero matches for `licen`,
`License` and `genuine`. A FAQ sentence claiming that every Windows plan includes a
genuine licence does not reproduce on three pages, and this document does not repeat it as
fact. What the cart proves is a zero surcharge for
Windows, which is a different claim. No order summary total is printed, and the `FREE!
Setup Fee` text on the page belongs to a cross-sell block, not to this plan.

### NetVolo: EUR 12.49, which is USD 13.98, billed for three years

VPS-Windows-3 is 4 vCPU, 16 GiB of RAM and 200 GB of NVMe, with 16 TB of bandwidth a
month and a 1 Gbps network guarantee. The card prints EUR 24.99 struck against EUR 12.495
and the footnote `Billed as 449.82 EUR every 3 years`. The arithmetic closes: 12.495 times
36 is 449.82.

⚠ **No monthly cycle exists on this plan.** The strings `monthly`, `quarterly` and
`annually` return zero matches on the page, and all eight products on it carry a
three-year footnote. EUR 12.49 is a monthly equivalent of a EUR 449.82 invoice, which is
USD 503.48 before the machine starts. The renewal after the first term is not printed, so
12.49 is a first-term rate.

The licence sentence is conditional: a licence "may be included" depending on the plan,
with details on each plan page. This plan page lists no licence line. The licence is
`unverified` on this SKU.

### HOSTKEY: EUR 14.00, which is USD 15.67, plus a licence at an unpublished price

vm.v2-medium is 8 vCPU, 16 GiB of RAM, 160 GB of NVMe and 3 TB of traffic a month on a
1 Gbit/s port. The English page printed EUR 14.00 for that shape, and vm.v3-medium is
EUR 16.00 for the same shape.

⚠ **The EUR 14.00 was read at 12:18Z, and the same page answered 403 at about 15:20Z.**
The English page returned HTTP 200 with 2,731,056 bytes at 12:18Z on 2026-10-26, and its
JSON-LD carries price 14.00 with `priceCurrency` EUR for vm.v2-medium and 16.00 for
vm.v3-medium. A re-read at about 15:20Z returned HTTP 403, the English catalogue path
returned 403 in a 5,680-byte body, and one reader answered with a stored provider copy
whose own header records the 403; that copy is not citable. The Russian storefront reads,
and it prints RUB 3,390 for the same 8 vCPU, 16 GiB and 160 GB shape, which is USD 42.02
at 0.012396. The two storefronts differ by about 2.7 times and neither page explains the
gap, so the row carries both numbers.

The `.ru` page's own structured data labels a ruble price as `"priceCurrency":"EUR"`.
That is the mechanism by which a RUB 3,390 card can be read as a EUR 14.00 card, and it
is worth knowing before either number is trusted.

Neither page prints a Windows surcharge. The `.ru` page names Windows only in its list of
supported operating systems, and the `.com` page was readable only in the 12:18Z fetch.
The Linux page carries the same EUR 14.00 and EUR 16.00, so the licence is a checkout
line and not part of the plan price.

## Where the licence comes from

### Supplied by the provider

Eight of these rows print a licence price or a free-licence line, and one of the eight comes
from OVHcloud's catalogue API rather than from its page. The rest print a sentence or
nothing at all, and a sentence is a `documented` claim about the page, not about an invoice. Sorted by monthly
rate. `none` means no record exists for that row, and SteadyVPS is the only one.

| Provider | Plan | vCPU | RAM (GiB) | Disk (GB) | Licence position | Monthly (USD) | First payment (USD) | Record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Virtarix | WIN VPS M | 6 | 16 | 100 | printed at USD 16.00 inside the plan | 27.40 | 32.70 first month | `virtarix-windows` |
| ServerPacket | Windows VPS 16 GB | 6 | 16 | 100 | claimed in a page sentence | 32.19 | 386.28 on 12 months | `serverpacket-windows` |
| windowsvps.host | DeluxeBox | 4 | 16 | 125 | claimed in a page sentence, Datacenter | 36.00 | 36.00 | `windowsvps-host-windows` |
| SteadyVPS | Hyper-V4 | 4 | 16 | 120 | claimed in a page sentence | 38.00 | 38.00 | `none` |
| InterServer | Windows Cloud Compute, 8 slices | 4 | 16 | 320 | not printed on the order page | 40.00 | 40.00 | `interserver-windows` |
| Contabo | Cloud VPS 8 plus Windows Server Datacenter 2025 | 8 | 24 | 300 | add-on at EUR 28.00, printed | 47.01 | 47.01 | `contabo-windows` |
| Time4VPS | Windows 16 | 4 | 16 | 200 | included free, printed | 52.88 | 26.44 | `time4vps-windows` |
| Windows 365 | Business 4 vCPU, 16 GiB, 128 GB | 4 | 16 | 128 | included, no prerequisite | 56.00 | 56.00 | `windows-365` |
| OVHcloud | VPS-4 2027 plus Windows Server 2025 | 8 | 24 | 200 | add-on at EUR 28.00, from the catalogue API | 57.63 | 57.63 | `ovhcloud-windows` |
| CloudCone | WC2-3, Windows Cloud Compute | 4 | 16 | 240 | supplied by the SKU, not printed | 62.75 | 62.75 | `cloudcone-windows` |
| Kimsufi | KS-3 plus Windows Server 2016 Standard | 4 | 32 | 480 | printed at USD 34.00 on a USD 30.00 box | 64.00 | 64.00 | `kimsufi-windows` |
| AccuWeb Hosting | VPS Mellite | 4 | 16 | 200 | included, printed | 79.99 | 79.99 | `accuweb-windows` |
| Kamatera | 4 vCPU, 16 GiB, 50 GiB, Windows Standard | 4 | 16 | 50 | add-on at USD 19.00, printed | 83.00 | 83.00 | `kamatera-windows` |
| STRATO | Windows V-Server VPS XL | 8 | 16 | 480 | included; EUR 79.00 plus EUR 9.00 setup | 88.43 | 98.50 | `strato-windows` |
| IONOS | Windows XL+ | 8 | 16 | 480 | included, derived from the Linux price | 94.00 | 60.00 | `ionos-windows` |
| VDSina | Hi-CPU 8, 16 GiB, 320 GB | 8 | 16 | 320 | included, printed | 120.00 | 120.00 | `vdsina-windows` |
| Hostwinds | Managed Windows SSD Cloud 7 | 6 | 16 | 300 | included, printed | 182.99 | 118.94 | `hostwinds-windows` |

Each row's URL and read date are in its record, and the record is the citation for the
legacy rows that were not reopened.

**Virtarix is the cheapest row where the licence is a visible, priced component**, which
is a stronger claim than the sentence-based rows above it and a weaker one than a
quoted licence purchase. At 24.66 on the annual term it is also the cheapest row in the
whole set that combines a printed licence with a 16 GiB shape.

Three notes on this table. InterServer at USD 40.00 is not the cheapest licence-supplied
row. SteadyVPS clears all three minimums at 4 vCPU, 16 GiB and 120 GB, so it is an
expensive row and not a near miss; its page also prints a second, different machine at
USD 48.00 in its own structured data. STRATO's row prints USD 88.43 including VAT and a
EUR 9.00 setup fee, so the first payment is USD 98.50, against USD 74.31 net.

⚠ **Windows 365 has no public IPv4 and no inbound RDP.** It is not the cheapest
licence-supplied row: SteadyVPS at USD 38.00 is. Windows 365 at USD 56.00 is the cheapest
managed desktop with the licence inside a Microsoft subscription, and it is a desktop on
a subscription, not a server. Every row in the ranked table answers on an address the
buyer controls.

### Installed by the buyer

netcup sells no Windows licence. Its VPS 2000 G12.5 is 8 vCore, 16 GiB and 256 GB of SSD
at EUR 26.92 a month on a 12-month term including 19 per cent VAT, which is USD 25.32 at
1.1193 for a buyer outside the EU. The FAQ states that the buyer installs Windows through
the SCP, that the image carries a 180-day test licence, and that no licence can be bought
from netcup afterwards.

The row is not in the ranked table because netcup sells no Windows image: the buyer
brings the media and installs from it, and the image carries a 180-day test licence. It is
also the cheapest 16 GiB machine from a long-established German host, and that test licence
is the clock. `netcup-windows` carries the record.

**How often the buyer can do this at all.** Across 26 hosts, self-install is documented at
13, vendor-library-only at 3, refused at 6, and unverified at 4. Half, not most. Four of the
six refusals are the hosts a reader tries first.

## What binds first

**The licence binds first, and it binds at a fixed price.** A 16 core licence costs the
same on a 4 vCPU guest as on a 16 core server, so the machine is the only variable in the
pair. On the floor row the licence is 58 per cent of the total: 10.14 of machine plus
14.17 of licence is 24.31, and a reader who compares machine prices alone is comparing
less than half of each purchase.

**The term binds second.** Six rows in the ranked table charge a year or more before the
machine starts: Layer7 at USD 97.35, Rabisu at USD 105.48, By-Hoster at USD 190.09,
Virtarix at USD 275.65, ServerPacket at USD 386.28 and NetVolo at USD 503.48. The cheapest
rate and the cheapest month are different products at those rows, and the first payment
column is the only column that shows the difference.

**Identity binds third, and it binds on every row.** Every record for a ranked row grades
the identity cost as `card`: an account and a payment method at order, with no anonymous or
email-only path found. No row here is reachable without a card, and that is the one
constraint the ranking cannot show.

**Traffic binds fourth.** HOSTKEY prints 3 TB a month, Linveo 8000 GB, NetVolo 16 TB and
Layer7 50 TB. Rabisu and netcup print no byte number at all; Rabisu calls its traffic
unlimited under a fair-use clause and prints no threshold. A serving workload reaches
3 TB before it reaches any other limit on this table.

**Location binds fifth.** Rabisu's cheap regions are Istanbul and Sofia, and every western
region adds USD 5.22 a month or more. Layer7's price is Frankfurt. NetVolo sells Europe
only. A row's price is a price for one place.

## What is not measured

⛔ **No machine was booted, no RDP session was attempted and no order was placed.** Every
figure is a vendor page, an order configurator or a rendered cart read on 2026-10-26. One
printed order total was reached in a 20-row cart audit, at VPSDime, and VPSDime is not a
ranked row here. No invoice was read and no licence was activated.

**What could not be settled.** Each item names what would close it.

1. **HOSTKEY's two storefronts.** The English page returned HTTP 200 with 2,731,056 bytes at 12:18Z, its JSON-LD carries EUR 14.00 for vm.v2-medium, and a re-read at about 15:20Z returned 403; one reader answered with a stored copy that recorded the 403. What stays open is why the Russian storefront prints RUB 3,390 for the same shape, about 2.7 times the Euro figure. The price endpoint the page script calls, or a location-selected order screen, would close it.
2. **Rabisu's licence.** No page read today states that a licence is supplied. The cart proves a zero surcharge, which is a weaker claim. One support answer in writing, or one invoice, would close it.
3. **Virtarix's two totals.** The checkout prints USD 32.70 for a first month and USD 275.65 for a first year. Both are close to pro-rata to the renewal date, to within 0.2 USD, and neither reproduces exactly. The page also prints USD 27.60 in its own comparison bar against the 27.40 the checkout charges.
4. **VDSina's 4.08.** The unit is settled as per day. The composition is not: the plan's own data carries a 4.00 daily cost plus an 0.08 daily IPv4, while the itemised slider rates sum to 3.72.
5. **Layer7's annual total.** EUR 86.97 is arithmetic on three printed annual option prices. The cycle cards do not recompute for options, so no rendered annual total exists to compare against.
6. **Whether Layer7's prices are net or gross.** The rendered summary prints no tax line.
7. **By-Hoster's VAT rate.** The 20 per cent figure comes from the vendor's own worked example, not from a line on the plan or the invoice preview.

**Other open gaps.**

- **ServerPacket's own two pages disagree by a factor of 2.3.** The marketing card prints USD 32.19 a month billed every 12 months. The store prints USD 167.88 a year for the same 6 vCPU, 16 GiB, 100 GB and 32 TB shape. Neither page explains the gap, and the product URL redirects to a different product group. The row prints 32.19 because that page states the specification and the licence. If 13.99 is real, ServerPacket moves to rank 4.
- **Saganetwork's OS choice.** The cart has no OS field, and the licence cost is unread.
- **HostBrr's order page.** The configurator returned a subtotal of EUR 0.00 and a total of EUR 0.00, which is a wrong pricing id and not a price.
- **Hostmayo's order page.** The cycle selector renders, and the setup fee and total are blank in the served HTML.
- **A client access licence quote.** No quote was obtained, and every licensed row above
  needs one.
- **Contabo's Windows total on its own terms.** The add-on is EUR 28.00 a month. The machine is EUR 14.00 monthly or EUR 11.20 on a 24-month term, so the pair is EUR 42.00 or EUR 39.20. The configurator was read, and the order summary still defaulted to Ubuntu at EUR 14.00.
- **Kimsufi's KS-3 price.** The `kimsufi` record carries KS-3 at USD 21.10 from a 2026-10-22 read. The 2026-10-26 configure page printed USD 30.00 plus USD 34.00 for the licence. This row uses the later figure, and the difference between USD 21.10 and USD 30.00 for one plan name is unresolved.
- **A USD 4.55 promotional rate attributed to CheapWindowsVPS.** No page read carries that figure. The sourced promotional price is USD 5.50 with code 50LEB against a USD 11.00 list, and the table prints that.
- **Seven rows never reached an order screen.** NetVolo, HOSTKEY, By-Hoster, ServerPacket, windowsvps.host, InterServer and SteadyVPS are page or checkout-card reads, not completed carts. SteadyVPS also has no dossier record. One order screen each, with the Windows option selected, would close both the cart rung and the licence line.

## Near misses and dead ends

| Provider | What it offers | Why it is not ranked |
| --- | --- | --- |
| HostBrr | Value 16GB, 4 cores, 16 GiB, 160 GB, USD 11.00 a month, USD 110.00 a year | Windows is product prose and a logo tile. The page has no OS selector, the order page is a registration wall that reaches a different product group, and the page states no IPv4. `hostbrr-windows` carries the record |
| Cloudzy | 8 vCPU, 16 GiB, 350 GB, USD 49.98 promotional | the licence is a trial or the buyer's own, and the renewal rate is unpublished. `cloudzy-windows` carries the record |
| Hostmayo | KVM-16GB, 8 vCPU, 16 GiB, 200 GB, USD 30.00 | clears the hardware, and every Windows entry in its OS list is suffixed `Unlicensed`, so it is a machine at 30.00 and a licence on top. It would rank 9th as a machine |
| VDSina | cloud configurator, 8 vCPU, 16 GiB, 100 GB | USD 4.08 is per day, which is about USD 122 to 124 a month. The page states the unit three ways. `vdsina-cloud-configurator` carries the record |
| DataWagon | DW-16G, 6 cores, 16 GiB, 160 GB, USD 16.00 | the live page does not mention Windows; a forum reply by the provider claims a free licence at USD 10.00 |
| Deluxhost | Y-5, 3 vCore, 16 GiB, 90 GB, EUR 35.00 a year | one vCPU short, and the cart returns an unavailable-lines error |
| Hostinger | KVM 4, USD 12.99 promotional | Linux templates only, and the vendor states that custom images are not offered |
| GreenCloudVPS | Budget KVM, 8 GiB, USD 45.00 a year | half the RAM floor |
| Windows 365 Enterprise | 4 vCPU, 16 GiB, 128 GB, USD 66.00 | needs Windows Enterprise, Intune and Entra ID P1 per user, so its licence is not in the price. Business at 56.00 carries no prerequisite and is in the table above |

**Hosts that cannot put Windows on the disk.** Three have no route at all, because they
offer neither user media nor a Windows image, and each says so.

| Host | The sentence or fact that closes it |
| --- | --- |
| DigitalOcean | the vendor states that Windows is not supported on a Droplet and that ISO images are not supported |
| Linode and Akamai | uploaded images must be raw `.img` on ext3 or ext4, and the catalogue has no Windows image |
| Hostinger | the vendor states that custom OS images cannot be uploaded or installed |

Four more run Windows but forbid the buyer's own media, so the machine can never be
rebuilt with a licence the buyer holds: **Contabo** refuses Windows custom images and the
buyer's own key, **Vultr** allows licensed public images only, **CloudCone** exposes a
fixed rescue disk and its own OS library, and **Hetzner Cloud** serves Windows from its own
CD/DVD list and refuses a buyer-supplied Windows ISO. **OVHcloud VPS** is a fifth case:
Windows is order-time only, and a VPS delivered without it cannot take it later.
**HostDare** allows custom ISOs at 5000 MB each, which is under a stock Windows Server ISO.

**Dead, retired or not a hosting company.** PHP-friends states that its page is no longer
available and points to two successor brands. Hostway's German site redirects to another
company and no VPS remains under the name. REG.RU suspended Windows VPS sales, and its own
help page says so while existing customers keep access. Joe's Datacenter served an
account-suspended page at read time. Handy Networks now serves a managed-services brand.
Nyrstar is a metals producer whose `/vps` path returns 404. Aerhost and BThost did not
resolve. 81VPS did not resolve, which is a record of unreachability and not of death.

## Corrections to earlier figures

1. **Rabisu's licence is unstated.** The sentence recorded earlier does not reproduce on the
   configurator, the home page or the knowledge base. The row keeps its price and carries no
   licence claim.
2. **InterServer is not the cheapest licence-supplied row.** Virtarix at USD 27.40 is cheaper
   by 31.5 per cent, and windowsvps.host at USD 36.00 is cheaper as well.
3. **The licence has a price.** USD 509.99, or USD 14.17 a month over 36 months, is the
   number. A floor that omits it measures hardware.
4. **Saganetwork's Windows path is unverified.** The cart has no OS field, so the row is a
   machine with a Windows claim and not a Windows row.
5. **HOSTKEY's EUR 14.00 was read at 12:18Z and the re-read was blocked.** The English page
   returned 200 with its JSON-LD, the Russian storefront prints RUB 3,390, and the row
   carries both figures with their dates and rates.
6. **HostBrr is a near miss, not a rank.** The cheapest claim at USD 11.00 has no OS
   selector and states no IPv4. Its order page does not configure the plan.
7. **VDSina's USD 4.08 is per day.** At about USD 122 a month it is not a candidate for this
   table. The unit is settled.
8. **SteadyVPS is not a near miss.** It clears all three minimums and belongs in the
   licence-supplied table.

## The records

The records are `saganetwork-windows`, `virtarix-windows`, `by-hoster-windows`,
`serverpacket-windows`, `windowsvps-host-windows`, `kimsufi-windows`, `hostbrr-windows`
and `vdsina-cloud-configurator`, beside `rabisu-windows`, `hostkey-windows`,
`netvolo-windows` and `linveo-windows`.

Six records carry the leading rows of this document: `layer7-windows`,
`rabisu-windows`, `netvolo-windows`, `hostkey-windows`, `linveo-windows` and
`netcup-windows`. The licence-supplied table names the rest: `interserver-windows`,
`contabo-windows`, `time4vps-windows`, `windows-365`, `ovhcloud-windows`,
`cloudcone-windows`, `strato-windows`, `accuweb-windows`, `kamatera-windows`,
`ionos-windows`, `vdsina-windows` and `hostwinds-windows`.

⚠ **SteadyVPS is the one row in this document with no record.** It carries a price and a
licence claim in the table above and nothing in `dossier/`, so its figure has no
machine-readable home and no staleness clock.

`rabisu-windows` cites the live configurator. The `/vps-windows` path returns 404 and is
kept in that record's evidence with its death date, and the
licence sentence is carried there as a third-party reading with no live source; the
verdict is `qualifies-with-caveat` at `reported`, not `qualifies` at a documented licence.

`kimsufi` is the one record that still disagrees with an older record of the same vendor:
it carries KS-3 at USD 21.10 from a 2026-10-22 read against the USD 30.00 the configure
page printed on 2026-10-26, and the difference is unresolved. `hostkey-windows` documents
EUR 14.00 on the English storefront beside RUB 3,390 on the Russian one, and records the
HTTP 403 the English page returned on re-read.

The vendor pages were read on 2026-10-26. The EUR conversions use the rate in the table
above. The USD 7 check, the licence channels and the host policy table come from the same
day's reads, and each carries the rung recorded where it appears.
