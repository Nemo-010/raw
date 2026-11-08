# The beefiest always-on machine under USD 5 a month

**The beefiest machine under the line is VolpaByte's Ryzen KVM 8 GB at EUR 50.90 a year:
6 AMD Ryzen vCores, 8 GiB of ECC RAM, 100 GB of SSD and unlimited traffic on 1 Gbps, in
Frankfurt, with 1 IPv4 and a /64 of IPv6.** Its cart prints four billing cycles and the
annual one is EUR 50.90; it says nothing about year two, so the renewal is an inference from
the EUR 4.99 monthly rung rather than a statement. ⚠ Its cart is a WHMCS store, which means
**a cookieless read returns "Could not load any product groups" and looks like a dead
vendor**. It is not dead — see `scripts/probe/cartcheck.py`.

**The cheapest 8 GiB is GreenCloudVPS's BudgetKVM rung: 8 GiB of RAM, 4 vCPU, 60 GB of
disk and 8 TB of transfer a month for USD 45.00 a year, which is USD 3.75 a month.** The
store page names **no renewal rate at all** in 320,626 bytes, so month 13 is genuinely
unknown rather than known-bad. ⚠ **A USD 40.00 a month figure for the same shape is
unverified**: it could not be found on the vendor's Budget KVM page on 2026-10-24. If it
holds, the worst case is 10.7 times the clearance rate. What remains true is narrower: the
price is a first-year clearance price, the terms of service apply listed prices to new orders
only, and the vendor reserves a change at the start of the next billing cycle. Stock is the
sharper problem — only four of twenty location cards carry units.

Five rows answer the question, and each one trades a different risk.

1. ⭐ **The best daily driver is VolpaByte `Ryzen KVM 8 GB` at EUR 50.90 a year: 6 vCPU, 8 GiB, 100 GB
   and unlimited traffic**, cart-verified, with the renewal unstated.
2. ⭐ **If a written renewal matters more than shape, AlphaVPS `C6G` at USD 4.75 a month:
   6 GiB, 3 vCPU, 55 GB and 6 TB for EUR 50.90 a year.** A daily driver's cost is the
   renewal, not the first invoice, and this is the only row here with an explicit permanent
   first-party rate lock. The page
   states it three ways: the banner says the annual rate is "LOCKED AT RENEWAL, FOREVER", the
   invoice block says the order-form price is the price on every invoice, "renewal included",
   and FAQ 04 answers "What happens to the price at renewal? Nothing." Prices are ex-VAT.
2. **The best 8 GiB bet with a written renewal is HostBrr's `ECO Memory-Optimized 8 GB` at USD 4.58 a month:
   8 GiB, **2 vCore**, 80 GB and 5 TB on a 10 Gbps port for USD 55.00 a year.** It is standing
   list pricing with no promo language, and the annual is exactly ten times the published
   USD 5.50 monthly rate, which bounds month 13; the cart itself prints
   `Total When Renewing: 1 Year @ $55.00`. ⚠ The shape is **2 vCore, not 8 vCPU**, and the
   monthly rate is USD 5.50, which is **over** the line —
   only the annual prepay qualifies. Two years cost USD 110. Certainty costs USD 0.83 a month
   against GreenCloud and buys two fewer cores and 3 TB less transfer.
3. **The row that needs no card at all is Bulutova's `VPS Sunucu 8` at USD 4.07 a month on the
   annual term: 8 GiB of ECC RAM, 2 vCore, 60 GB of NVMe and a 1 Gbps port in Istanbul.**
   ⚠ **The headline is a prepay figure.** The page prints "40% İNDİRİM, 281.45 → 168.87 TL/ay"
   and the Order Now button lands on the **annual** term, TRY 2,026.44. The monthly rung is
   **194.21 TL, which is USD 4.68** — still under the line, but only just. The discount is
   struck against TRY 281.45, so if it lapses the renewal is USD 6.79 and over the line.
   ⚠ **The annual cart prints `KDV (%0) 0,00 TL` and the page JSON carries
   `taxEnabled:false, taxRate:0`**, so no KDV line is reachable at that step. The seller is
   in the Turkish ETBIS registry since 25.04.2022:
   BITWISE YAZILIM INTERNET VE TICARET LIMITED SIRKETI, Gebze trade register 33061, tax number
   1781478560, Mersis 0178147856000001.
4. **RackNerd's 4 GB sits on the line at USD 5.00 and its renewal is published and recurring:
   4 GiB, 3 vCPU, 60 GB and 7 TB for USD 59.99 a year.** The specials page answers the renewal
   question in its own FAQ: "These RackNerd VPS specials are lifetime recurring. You can renew
   at the same rate for as long as you decide to keep the service." No clause in the terms
   contradicts it. RackNerd's reputation as a promo host is out of date on this page.

If a year's prepay is not acceptable, the monthly-billed rows under the line are **C-Servers
`ExtraVPS-6144`: 6 GiB, 4 vCPU, 40 GB and 6 TB for USD 4.29 a month with no commitment**,
**HostBrr's `Value 4GB`: 4 GiB, 1 vCPU, 40 GB and 2.5 TB for USD 3.25 a month**, and
**Datalix's Ryzen GEN 2 Starter: 4 GiB, 1 vCPU, 25 GB and 10 TB for USD 4.42 a month**. Of the
rows read, C-Servers is the only one that is both under the line and monthly-billed at 6 GiB.
Datalix carries 10 TB of transfer a month, the largest metered allowance of any sub-USD-5
row found; the two rows in the table that carry more are OVHcloud's unlimited EU
traffic and Krova's unmetered port, and neither publishes a number.

⛔ **The unit decides the ranking.** A VPS bills
whether it runs or not, so its monthly bill is the number to compare, and an annual total
divided by twelve is a monthly equivalent and not a monthly bill. Seven of the seventeen rows
below are annual prepay. The out-of-pocket first payment is in its own column, because
USD 3.75 a month that costs USD 45 today is a different offer from USD 3.75 charged
monthly.

## The rule this table uses

**Beefiest means RAM first, then vCPU, then disk, then transfer.** A daily driver is
bounded by memory before it is bounded by cores: a browser, a JVM or a Postgres instance
meets the RAM ceiling first, and a vCPU on a shared host is a scheduling claim rather than
a clock. The core count is in the table because it changes what the box can do, not
because it ranks the rows.

## The rows, under USD 5.00 a month

Every row was read at the vendor's own page on 2026-10-24. `Monthly` is the 24/7 bill.
`Renewal` is the month-13 bill, and it says whether the vendor publishes it. `First payment`
is what leaves the account today.

| # | plan | RAM | vCPU | disk | Monthly | Renewal | First payment | Transfer | Monthly billed? | What breaks it |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `greencloud-budget-kvm-8gb` | **8 GiB** | 4 | 60 GB | USD 3.75 | **not published** | USD 45.00 | 8 TB | no, annual | clearance stock; E5v3/v4 on the in-stock locations; no refund; average CPU capped at 30% |
| 2 | `hostbrr-value-8gb` | **8 GiB** | 2 | 80 GB | USD 4.58 | USD 4.58 annual; USD 5.50 monthly is the ceiling | USD 55.00 | 5 TB | no, annual | 2 cores; whether the line includes IPv4 is not stated |
| 3 | `bulutova-vps-8` | **8 GiB** | 2 | 60 GB | USD 4.07 | USD 6.79 if the 40% lapses | USD 4.07 | unlimited, shared | **yes**, monthly | no IPv6; the 40% discount has no end date; the card does not state root or SSH |
| 4 | `c-servers` | **6 GiB** | 4 | 40 GB | USD 4.29 | USD 4.29, inferred | USD 4.29 | 6 TB | **yes**, monthly | 300 Mbps port; the renewal is inferred from a monthly-only term |
| 5 | `alphavps-c6g` | 6 GiB | 3 | 55 GB | USD 4.75 | **USD 4.75, locked forever** | USD 56.97 | 6 TB | annual or monthly at USD 5.59 | annual commitment; monthly rate is over the line |
| 6 | `datalix` | 4 GiB | 1 | 25 GB | USD 4.42 | USD 4.42, printed on the order | USD 4.42 | **10 TB** | **yes**, monthly | 21 of 24 rungs sold out; 25 GB is the smallest disk among the 4 GiB rows |
| 7 | `ovhcloud-vps-1-2027` | 4 GiB | 2 | 40 GB | USD 4.54 | catalogue price, no lock | USD 54.48 | unlimited in the EU | 12-month upfront for this rate | 500 Mbps port; monthly rate is USD 5.03 |
| 8 | `hostbrr` | 4 GiB | 1 | 40 GB | USD 3.25 | USD 3.25, published monthly | USD 3.25 | 2.5 TB | **yes**, monthly | 1 core; 2.5 TB at 10 Gbps is mismatched |
| 9 | `racknerd-4gb` | 4 GiB | 3 | 60 GB | USD 5.00 | **USD 5.00, lifetime recurring** | USD 59.99 | 7 TB | no, annual | sits exactly on the line, not under it |
| 10 | `alphavps-c2g` | 2 GiB | 2 | 30 GB | USD 2.84 | USD 2.84, flat at renewal | USD 34.14 | 3 TB | no, annual | 2 GiB and 30 GB meet the ceiling first |
| 11 | `cloudcone-ssd-vps-2` | 2 GiB | 4 | 60 GB | USD 3.83 | USD 3.83, same rate, no lock | USD 46.00 | 7 TB | no, annual | 2 GiB; the 4 cores are the best count under the line |
| 12 | `hosthatch-nvme-2gb` | 2 GiB | 1 | 10 GB | USD 4.00 | USD 4.00, a "from" rate | USD 4.00 | 1 TB | **yes** | 10 GB disk ties Krova for the smallest in the set |
| 13 | `tencent-lighthouse-intl` | 2 GiB | 2 | 40 GB | USD 4.20 | USD 4.20, printed as USD 50.40 a year | USD 10.08 in year one | 0.5 TB | monthly or annual | 0.5 TB is the smallest allowance here; debit and prepaid accepted |
| 14 | `krova-cube` | 2 GiB | 1 | 10 GiB | USD 4.75 | no renewal; prepaid credit | USD 4.75 | unmetered | per minute | TCP-only ingress; a-la-carte shape from the rate card |
| 15 | `webarena-indigo` | 1 GiB | 1 | 20 GB | USD 2.86 | USD 2.86, the monthly cap | USD 2.86 | port-capped 100 Mbit/s | hourly with a monthly cap | Japanese-only site; signup needs email, then SMS or voice, then a card; 1 GiB |
| 16 | `time4vps-linux` | 1 GiB | 1 | 10 GB | USD 3.35 | USD 3.35, printed twice on the card | USD 3.35 | 1 TB | **yes** | 1 GiB; the 4 GiB rung is a promo that doubles at renewal |
| 17 | `kamatera-basic` | 1 GiB | 1 | 20 GB | USD 4.00 | USD 4.00, list with no contract | USD 4.00 | 5 TB | **yes**, no contract | 1 GiB for USD 4 is the worst value here; priced per configuration, no contract |

Three rows that a reader will look for are deliberately absent. **Hetzner CX23** is
EUR 5.99 (USD 6.70) and marked "not available" on its own page, so it is neither under
the line nor purchasable. **Contabo Cloud VPS 4** is USD 6.16 for 8 GiB of RAM, which is
1.30 GiB per USD and over the line, against 1.96 for Bulutova and 1.75 for HostBrr's
`Value 8GB`. **Datalix's 8 GiB** is EUR 3.95 on its 2026 sale ladder, which is USD 4.42 and
under the line, and the card is marked "Ausverkauft"; the buyable 4 GiB rung is the row in
the table. Twenty-one of the twenty-four rungs across Datalix's four KVM ladders are sold
out, so that ladder is a snapshot rather than a catalogue.

One row is absent because it cannot be bought at all. **CoolVDS** sells 1 vCPU / 512 MB /
10 GB for USD 4.00, and its order page states "All Slots Currently Occupied" with a waitlist
and no order button. The shape and price are recorded and the row is not buyable, which is a
different finding from an expensive one.

## Whether it survives a Tuesday

A price and a shape do not decide whether a box is a daily driver. What decides it is whether
the box can be recovered at 2 a.m. after a kernel update fails, and that is a documented capability
rather than a specification. Six rows were read for it on 2026-10-24: five from the table
above, and netcup's VPS 500 at USD 9.25, which is over the line and in no other table here.
Two rows, `hostbrr-value-8gb` and `bulutova-vps-8`, were not read for recovery.

| plan | API | backup and snapshot | rescue and out-of-band | IPv6 | panel firewall |
| --- | --- | --- | --- | --- | --- |
| `ovhcloud-vps-1-2027` | **yes**, v1 and v2 REST, a CLI and `python-ovh` | a daily 24-hour backup **included**; a snapshot at USD 0.40 a month | **yes**: panel rescue with credentials by mail, KVM console, boot logs | one /128 | not published |
| `netcup-vps-500-g12-5` | **yes**, a SOAP webservice and REST | copy-on-write snapshots, offline and exportable; allowance unpublished | **yes**: Media, then Rescue System | /64 | **yes**, free, 500 rules |
| `greencloud-budget-kvm-8gb` | not published | **one free snapshot**; scheduled ones are a paid add-on | **yes**: VirtFusion rescue, two methods, plus VNC | /64, and /112 in Bucharest | not published |
| `hostbrr` | not published | one backup slot included | **yes**: VirtFusion rescue, VNC, custom ISO | /64 | not published |
| `alphavps-c6g` | claimed "API - BUILT IN", no endpoint found | snapshots "included", count unpublished | **yes**: noVNC, boot order, ISO, rescue mode | /64 | not published |
| `tencent-lighthouse-intl` | **yes**, a full REST API, TCCLI and CloudShell | free snapshots, two per instance | VNC and OrcaTerm, **no rescue boot** | **none** | **yes**, 100 rules |

⭐ **OVHcloud answers the recovery question better than any other row, and the recommendation
above does not take it.** A real API, a backup included by default, and a rescue boot plus a KVM
console plus boot logs are each a first-party answer, and that is the combination that recovers
a box that will not start. Netcup answers the same three questions, and it is one of the two
rows with a panel firewall. OVHcloud's weaknesses are a 500 Mbps port, no published panel
firewall, a single /128 rather than a routed prefix, and a renewal charged at the catalogue
price in force with no published guarantee, which is USD 5.03 on monthly billing today.
AlphaVPS `C6G` is the row the recommendation takes: its rate is locked, and its recovery path is
a noVNC console, boot order, ISO and rescue mode, with no API endpoint found. A reader who
values the API and the included backup over the price lock takes OVHcloud and accepts the
catalogue risk.

⛔ **GreenCloudVPS wins on shape and loses on operations.** No API, no panel firewall, no
refund on the plan, no published renewal, and 21 units left across 4 of the 20 location cards
at the time of the read. Its rescue documentation is the best of the six, which is the one
thing that makes it usable at all. A buyer who takes the GreenCloud 8 GiB row is buying capacity
and accepting that the recovery path is manual.

⚠ **Tencent Lighthouse is the row that looks best on paper and is worst at 2 a.m.** The best
API and a real panel firewall at 100 rules, against netcup's 500, no IPv6 at all ("If you need
IPv6, please use CVM"), and no rescue mode anywhere in its documentation. A failed kernel costs
a snapshot rollback, which is irreversible, or a reinstall.

⚠ **"Not published" is not "absent".** GreenCloud, AlphaVPS, HostBrr and OVHcloud publish no
panel firewall; each gives root and expects `nftables`. That is a different product from one
with a managed firewall and it is not a defect, but a reader should not read the empty cell as
a missing capability.

⛔ **No rescue mode was exercised, no snapshot was taken and no API call was made.** Every cell
above is a page read on 2026-10-24.

## Who is behind the invoice

At USD 3.75 a month the counterparty matters more than the specification. What each
seller's own site, its national register and its
refund page say, read on 2026-10-24:

| plan | the seller | domain created | refund | what happens when a card expires | risk |
| --- | --- | --- | --- | --- | --- |
| `greencloud-budget-kvm-8gb` | 365 Group LLC, country not stated | 2013-10-06 | 7 days on a first VPS, and **every sale SKU's order page says "No refund/Money back on this plan"** | suspend day 1, terminate day 3 | medium |
| `alphavps-c6g` | DA International Group Ltd, Sofia, Bulgaria, company no. 202826767; own network AS203380 | 2009-07-14 | 14 days on a first order, unused only; promo and China orders excluded | "immediately terminate", no fixed day | medium |
| `hostbrr` | PFWeb Solutions, Denmark, a registered sole proprietorship with a CVR number | 2022-04-22 | 7 days on a card or PayPal order, 30 on shared; crypto none | suspend day 1, terminate day 3 | medium |
| `bulutova-vps-8` | BITWISE YAZILIM INTERNET VE TICARET LIMITED SIRKETI, Turkey; ETBIS registry since 2022-04-25, Gebze trade register 33061 | - | not published | no deletion clock published, and Havale/EFT is a second rail | medium |
| `datalix` | a sole trader in Germany trading as Datalix | RDAP failed, DENIC publishes no creation date | 14-day EU withdrawal, prorated | suspend at expiry, delete day 3 | medium |
| `ovhcloud-vps-1-2027` | OVHcloud, a public company | decades | statutory withdrawal | auto-renew, then suspend and delete "after a few days" | low |
| `c-servers` | no entity named | not read | not published | not published | medium |
| `racknerd-4gb` | RackNerd LLC, Delaware | 2015-06-09 | none by default, "case-by-case" | terminate day 7, data removed at once | medium |
| `tencent-lighthouse-intl` | Tencent Cloud, a public company | decades | refund of unused term | suspended about 48 h after expiry, released after 15 days | low |
| `krova-cube` | Krova Inc., Delaware | **2026-03-14**, seven months old | **none**: all credit is non-refundable | disk deleted 7 days after the balance hits zero | high |
| `cloudcone-ssd-vps-2` | CloudCone, LLC, US | 2014-12-21 | **none**: prepaid is non-refundable including annual | suspend without notice, terminate day 10 | high |

⭐ **GreenCloudVPS's own order page says no refund on that plan.** The vendor publishes a
7-day policy and then excludes the sale SKUs, which is the row in the table above. That is not
a reason to avoid it; it is a reason to buy the annual term knowing the first payment is gone
if the box does not work.

⚠ **A sole trader and a company are different risks, and both appear here.** Datalix is one
person in Germany with a statutory EU withdrawal right; AlphaVPS is a Bulgarian company with its
own network and an AS number, which is the strongest operator evidence in the set. Neither is
safer in the abstract. The first is easier to leave and easier to lose; the second has more to
lose and a longer record.

⛔ **Two rows are excluded from the shortlist on this evidence rather than on price.** Aeza
has been on the US OFAC sanctions list since 2025-07-01, so the machine can stop existing for
reasons the contract does not cover, and its storefront would not answer through the broker at
all. Krova Cloud's terms prohibit VPN use and its credit is non-refundable in cash, which closes
it for the second question and makes it a prepaid bet for the first. Both remain in `dossier/`
with the reason.

## What disqualifies a row, which is most of the market

- **A first-term promo is not a price.** IONOS advertises USD 2 for three months on a
  one-year term and lists USD 6 after; Time4VPS advertises EUR 4.38 and states EUR 8.76
  at renewal on the same card. Both of those rows double. The reverse case is rarer and it
  exists: RackNerd's page is titled Specials and its own FAQ states the rate is lifetime
  recurring, so the label on the page is not the test.
- **An advertised IPv4 is not always included.** Scaleway's STARDUST1-S is EUR 0.0006 an
  hour and looks like the cheapest machine in the topic, but a public IPv4 is EUR 0.005
  an hour, about USD 4.09 a month, which is more than eight times the instance. Vultr's
  USD 2.50 rung is labelled IPv6-only.
- **A sold-out plan is not a plan.** Hetzner's cost-optimised tier and the GreenCloud
  row both print availability on the card; the second one is why the stock count is in
  the first row.
- **A shared port is not a guaranteed rate.** 8 TB on a 10 Gbps port and 2.5 TB on a
  10 Gbps port are different products: the second is exhausted in under an hour at line
  rate, so the quota is the real port.

## Five figures that are commonly wrong

1. **The floor is not USD 6.49.** That figure priced the mainstream set and said nothing
   about the market. See `history/2026-10-24T021500Z/under-five-floor-corrected.md`.
2. **Hetzner is not the cheap default.** CX23 is EUR 5.99 and unavailable, and the CX22
   rung several documents quote at about EUR 3.79 is not on the page. `hetzner-cx23`
   carries the current figures.
3. **DigitalOcean's USD 4 droplet is 512 MiB**, not 1 GiB, which is USD 6.00
   (`digitalocean-droplet-1gb`).
4. **netcup's entry rung is the G12.5 generation**: VPS 500 at EUR 8.26 and VPS 1000 at
   EUR 14.50 (`netcup-vps-500-g12-5`).
5. **ServerHost's USD 16.99 a year is a campaign rate**, gated on the code in the URL
   (`promocode=FBAD2GB2026`), with no published renewal, against a published USD 6.00 a month
   list price for the same 2 GB shape, which is USD 72.00 a year and a 4.2 times jump; its
   homepage advertises "from USD 3/mo" (`serverhost-2gb-promo`).

## Which vCPU is a real vCPU

The table above ranks by the vendor's core count, and the core count is the weakest number
in it. A third-party Geekbench 6 sample of these hosts, collected from published results
rather than run here, spans **300 to 2,596 single-core points across the nine rows**, an 8.7
times spread. The spread does not follow the core count: both 4 vCPU rows score below 1,000
single-core, under a 1 vCPU row at 1,548 and a 2 vCPU row at 2,242, because the cheap
many-core rows are older silicon on busier hosts.

| host | measured plan | CPU | vCPU | Geekbench 6 single / multi | USD/month | source date |
| --- | --- | --- | --- | --- | --- | --- |
| AlphaVPS | Specials Ryzen-1GB `*` | Ryzen 9 7900 | 2 | **2,242 / 2,517** | USD 2.84 | 2025-08-31 |
| Datalix | Ryzen GEN 2 Small `*` | Ryzen 9 5950X | 1 | 1,548 / 1,546 | USD 2.82 | 2025-11-06 |
| Aeza | HKs-1 | Ryzen 9 7950X3D | 1 | 2,596 / 2,437 | USD 6.64 | 2024-05-05 |
| GreenCloudVPS | BudgetKVMNL-3 | EPYC 7702P | 4 | 992 / **2,782** | USD 3.75 | 2025-10-23 |
| RackNerd | 2.5 GB KVM `*` | Xeon E5-2690 v4 | 2 | 943 / 1,633 | USD 1.83 | 2026-08-10 |
| OVHcloud | VPS-1 | Haswell | 2 | 696 / 1,206 | USD 4.54 | 2026-10-11 |
| Hetzner | CX23 | Xeon Skylake | 2 | 638 / 1,059 | USD 6.70 | 2026-08-28 |
| Contabo | Cloud VPS 10 `*` | EPYC | 4 | 841 / 2,275 | USD 6.16 | 2026-09-09 |
| Time4VPS | Linux 4 | Xeon E3 v2 | 2 | 300 / 547 | USD 9.80 | 2024-02-13 |

⛔ **These are `reported` numbers, not measurements.** They are third-party
Geekbench results with the dates shown, and the plan measured is not always the plan priced:
the four rows marked `*` were measured on a different rung from the row this page prices.
Datalix was measured on its 2 GiB Small and is priced above as the 4 GiB Starter at USD 4.42;
RackNerd was measured on its 2.5 GB rung, its USD 1.83 is the 1 GB annual special, and the row
priced above is the 4 GB plan at USD 5.00; AlphaVPS was measured on the 1 GiB Specials rung and
is priced above as C2G at USD 2.84; Contabo's 4 vCPU / 8 GiB shape is priced from
`contabo-cloud-vps-4` at USD 6.16, and the sample names that rung Cloud VPS 10; Aeza's HKs-1 and
the WAWs-1 row priced here are both 1 vCPU / 2 GiB. The source URL and date are in the
`extras.benchmark` array of the record for seven of the nine rows, and that array sits in
`extras` rather than `evidence`, so it does not raise the record's rung; `ovhcloud-vps-1-2027`
and `hetzner-cx23` carry none, so those two rows rest on this table alone. Geekbench 5 and 6 are
never mixed, and the two hosts that published only GB5 are not in this table. Two of the sources
are more than two years old, which is why the column is a lead and not a fact: a host can change
hardware without changing its plan name.

⭐ **The direction is the finding.** The 8 GiB rows are not the fastest single-thread rows.
If the daily driver is interactive, AlphaVPS at USD 2.84 with a Ryzen 9 7900 is the better
machine than GreenCloudVPS at USD 3.75 with a 2014-era Xeon, and the RAM column says the
opposite. If the workload is parallel, GreenCloud's 2,782 multi-core score at USD 3.75 is the
best in the band. Nine of the seventeen rows above have no line in this table: C-Servers,
HostBrr, Bulutova, CloudCone, HostHatch, Tencent, Krova, WebARENA and Kamatera. HostBrr's own
record carries a 1,244 / 2,064 result for its 2 vCPU rung that the table does not show. CoolVDS,
which cannot be bought, has none either, and Hetzner's CX22 is not on the vendor's page at all.

Time4VPS is the row to avoid on this evidence: 300 single-core points is 8.7 times slower than
Aeza's 2,596, and no disk figure was recorded for it, so the core result is the whole of the
evidence.

## The rows that were read and rejected

Every row below was read at the vendor's page on 2026-10-24 and kept as a record so it is
not read twice. None is in the table above.

| record | what it is | why it is not the answer |
| --- | --- | --- |
| `contabo-cloud-vps-4` | 8 GiB / 4 vCPU / 100 GB, USD 6.16 | the beefiest shape near the line and over it; 200 Mbit/s port |
| `time4vps-linux-4` | 4 GiB / 2 vCPU / 50 GB, EUR 4.38 first term | the same card states EUR 8.76 at renewal |
| `ionos-vps-s-plus` | 2 GiB / 1 vCPU / 60 GB, USD 2 for three months | list price USD 6 after the promotion |
| `naranja-kvm-nvme-2gb` | 2 GiB / 1 vCPU / 30 GB, EUR 5.00 | over the line at any term |
| `aeza-waws-1` | 2 GiB / 1 vCPU / 30 GB, EUR 5.93 | unlimited traffic on 25 Gbps at the wrong price |
| `buyvm-slice-2048` | 2 GiB / 1 vCPU / 40 GB, USD 7.00 | unmetered traffic, one core, over the line |
| `buyvm-slice-512` | 512 MiB / 1 vCPU / 10 GB, USD 24.00 a year | 512 MiB is a proxy, not a host |
| `racknerd-1gb-special` | 1 GiB / 1 vCPU / 20 GB, USD 21.99 a year | good value, smaller than the rows above |
| `vultr-regular-1gb` | 1 GiB, USD 5.00 | exactly on the line; the USD 2.50 rung is IPv6-only |
| `scaleway-stardust1-s` | 1 GiB, EUR 0.0006 an hour | a public IPv4 adds about USD 4.09 a month |
| `lightnode-tokyo` | 2 GiB / 1 vCPU / 50 GB, USD 7.71 monthly | over the line |
| `sakura-vps` | 512 MiB / 1 vCPU / 25 GB, USD 3.76 | phone verification by automated voice call before first use |
| `locaweb-vps` | 1 GiB / 2 vCPU / 40 GB, USD 4.74 renewal | CPF, RG and date of birth at checkout |
| `alibaba-swas-intl` | 1 GiB / 1 vCPU / 20 GB, USD 4.50 | a non-mainland mobile is required, and virtual cards are refused |
| `sparklehosting-dead` | the domain is for sale, USD 3,695 | there is no product |

⛔ **Nothing here was paid for and nothing was booted.** Every number is `documented`,
read at the vendor's page on 2026-10-24, and no probe measured disk throughput, network
throughput or contention. The core count is a vendor claim. A published third-party
benchmark is the only thing that would separate a 4 vCPU row from a 1 vCPU row with more
real throughput, and this page does not have one.

The rows above are records in `dossier/compute/`; the slug in the first column is the
file. `docs/compute/paid/README.md` is the lane front page, and `docs/compute/gaps.md`
carries what is still open.

## What this page does not establish

⛔ **Nothing was bought and nothing was booted.** Every number here is `documented`, read at
the vendor's page on 2026-10-24, and no probe measured disk throughput, network throughput or
contention. The core count is a vendor claim and the benchmark column is a third party's
published run, not a run made here.

Stock and renewal are the two facts that decide whether the first row is real tomorrow, and
only one of them is published. GreenCloudVPS carried units on 4 of its 20 location cards at
the read — JAX-3, MO-3, CUK-3 and RO-3 — and its renewal price appears nowhere: the store page
names no rate, the terms price the offer for new orders only, and the vendor reserves a change
at the start of the next billing cycle. ⚠ **The exposure is not bounded by a list price.** A
USD 40.00 a month figure for the same shape could not be found on the vendor's Budget KVM
page on 2026-10-24 and is
**unverified**. Month 13 is unknown, and unknown is the honest answer. One ticket to the vendor
would settle it, and none was sent. The refund window is the other unpublished term, because
the same order page excludes the sale SKUs from the 7-day policy.

The recovery path is answered above, in "Whether it survives a Tuesday", and it rests on
documentation rather than on an exercised rescue boot. No rescue mode was entered, no snapshot
was taken and no API call was made.
