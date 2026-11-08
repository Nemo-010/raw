# The beefiest machine under USD 1 a month, for a VPN node or a health monitor

Two answers, and they are different machines.

**For a WireGuard node, C-Servers' NanoVPS-384 US at USD 2.39 per six months, which is USD 0.40 a
month.** It is the only row under USD 1.00 that combines a written UDP statement with a 20-port
forwarded block and a seller Companies House shows as trading. The vendor's knowledge base says
"This means that: 20 NAT IPv4 ports can be customized directly by the customer, for TCP and UDP",
and the French version of the same article adds that the 20 ports can be used for any protocol. The
seller is Centerfield Ltd, company number 14864789, status Active, at the Manchester address the
store footer prints. A routed IPv6 /64 sits beside the NAT address, so a peer with IPv6 needs no
forwarding at all. The machine is 1 vCPU, 384 MiB, 12 GB of NVMe and 2 TB a month at 300 Mbit/s, and
it is KVM, so the guest loads the in-kernel WireGuard module.

**For a health monitor, TierHive's Micro at USD 0.10 a month**, billed at USD 0.000135 an hour:
128 MiB, 1 GB of NVMe, a NAT IPv4 with two TCP and two UDP ports, and an IPv6 /64 per location. A
monitor polls other hosts and never accepts a connection, so outbound traffic and a clock are the
whole requirement. This is the cheapest always-on machine found anywhere in the band. Hourly
billing means a stopped box costs nothing, it is the only seller here that prints "No credit card
required", and its company is Kernel Keepers LTD, 16294246, Active. It states two UDP ports, so it
can terminate one WireGuard listener. 128 MiB and a vendor that calls itself "a no-SLA, budget
service" make it the monitor answer rather than the node answer.

**Gullo's Hosting's FR NAT 128 MiB at USD 3.50 a year, which is USD 0.29 a month, is not refuted.**
It is the only row in the table with a first-hand report of a WireGuard tunnel running for months: a
user installed precompiled `wireguard-go` and ran it with shadowsocks "without running out of ram"
across 255 days of uptime, and another confirms TUN and TAP can be enabled. It is not the
recommendation, and the reason is one missing sentence. Five of its pages were read on 2026-10-24,
the packages page, the pricing table, the NAT IPv4 help page, the knowledge-base index and the
WireGuard how-to, and none says whether the 20 forwarded ports carry UDP. USD 0.11 a month buys that
sentence, 384 MiB instead of 128, 2 TB instead of 125 GB, and a company to write to. Its other
weakness is unchanged: it names no company, and the order form carries a mandatory "I understand
that there are no refunds" checkbox. 128 MiB is the smallest shape in the table, and it is enough
for WireGuard and nothing else.

**The plan with the best port documentation is NATKVM's NL 256MB NAT at USD 4.99 a year, which is
USD 0.42 a month**: one vCPU, 256 MiB of RAM, 5 GB of disk, 800 GB of transfer a month, a shared
IPv4 with **20 forwarded ports that the vendor states carry both UDP and TCP**, one dedicated IPv6,
and TUN and TAP enabled. It is the only plan read that states UDP forwarding, TUN and TAP,
and a dedicated IPv6 together.

⛔ **Its UDP sentence is contradicted by its own users, and its counterparty cannot be checked.**
Two users in a June 2024 thread report that UDP is blocked by default on these ports and needs a
support ticket, and the thread's opening poster could not get WireGuard up on a forwarded port at
all. The dissolved UK company is also no longer the entity the site names. The about page and the
terms of service both say "KhanWebHost PVT LTD", "a privately owned company based out of Pakistan",
with no registration number, so Companies House can neither confirm nor refute it.

Orders are still being fulfilled: the store returns 200 with live stock and working order buttons, a
host representative's post is dated 2026-10-12, and a review dated 2026-10-23 describes a purchase
and a migration. Two public refund refusals on annual plans and a report of network outages lasting
hours almost daily stand against it. The domain expires 2026-11-28, which is the nearest dated
event. The money at risk is USD 4.99, so this is a small-stakes decision, but a buyer has no
counterparty to pursue. Treat it as a write-off bet, not a purchase with recourse.

⛔ **USD 4.99, USD 3.50 and USD 2.39 are the vendors' stated rates, not invoiced prices.** The NATKVM
card reads "Starting from" and its product pages redirect to the cart. Gullo's order page prints the
line "FR NAT IPv4 128MB (Oct 23, 2026 - Oct 23, 2027) 1 @ $3.50", which is a cart and not a charge.
C-Servers prints "$2.39 / 6 month(s)" on a plan card. A checkout is what would confirm any of them.

**The answer to buy if the node must not fail is Cloudfanatic at USD 2.99 a month**, which is
three times the line and worth stating plainly: a named US corporation, monthly billing so no
year is prepaid, a written 7-day money-back window, a dedicated IPv4 with all ports open, and a
99.9 per cent uptime SLA stated on a third-party benchmark page for its former Servercheap brand.
The SLA is a reported claim and not a first-party one, and the independent monitoring that would
show how often the node actually fails has not been read. If the real constraint is "must not
fail" rather than "must be under a dollar", the answer changes vendor and not just plan.

**Most rows are containers and the rest are small KVM guests.** The store groups read
`ovz-nat-vps` and the marketing pages call those products OpenVZ while the store headings say LXC,
so the guest shares the host kernel and WireGuard runs in userspace over TUN/TAP; whether that host
kernel carries the module is stated nowhere. The KVM rows read here — C-Servers, VirNAT,
HostBrr, DediRock and TierHive — run their own kernel. The endpoint on a NAT row is the node's shared
IPv4, not an address that belongs to the buyer, and no vendor publishes what happens to the port
mapping when a node is rebuilt. And the term varies: five rows bill monthly, one bills hourly, six
are annual prepay, two bill three and six months at a time, two offer both a monthly and an annual
rate, and one offers a quarterly or an annual term. A price on this page is a term as well as a
number.

**The health monitor answer was Cheap-Host's NAT Start at 59 RUB a month, about USD 0.73, and
TierHive's Micro replaces it at about a seventh of the price.** Cheap-Host is still the beefiest NAT
row that states UDP in writing: 1 vCPU, 1 GiB, 10 GB, 999 forwarded ports with TCP and UDP stated,
and unlimited traffic at 100 Mbit/s, every field re-verified on 2026-10-24 and held. A monitor needs
none of that. ⚠ Its storefront domain is four months old, it publishes no terms of service and no
refund policy, and it takes Russian cards, SBP or crypto, so a buyer without a Russian card pays in crypto
with no chargeback. TierHive states no byte allowance at all, which is a documented absence rather
than a quota, and it calls itself "a no-SLA, budget service" that "is not the place to host things
you demand uptime for".

⭐ **A monthly-billed machine under USD 1.00 does exist.** One search in Chinese finds it.
**luo_cloud sells a German LXC NAT box at CNY 1.50 a month, which is USD 0.22**: one vCPU on
a Ryzen 9 7900, 128 MiB, 2 GB of SSD, 1 TB of transfer at a 2000 Mbit/s
shared port, 20 NAT ports and one IPv6, on the store's own monthly cycle rather than an
annual price divided by twelve. Two units were in stock when it was read. The same store
sells a US box at CNY 2.00, USD 0.30, with ten units in stock, and advertises a Hong Kong box
at CNY 1.00, USD 0.15, that is sold out.

⚠ **Cheap-Host at USD 0.73 is already in this table**, so a claim that no monthly machine
exists under USD 1.00 contradicts the table three paragraphs apart. A negative claim about a
market is the cheapest kind of claim to make and the most expensive to get wrong, and one page
refutes both price negatives in this band.

The CNY and RUB figures convert at the Central Bank of Russia table dated 24.10.2026 (USD
80.5381 RUB, CNY 12.0557 RUB, so 1 USD = 6.6805 CNY) and were cross-checked against the ECB
series for 2026-10-23 at 6.6702 CNY, 0.15 per cent apart.

**luo_cloud is not the recommendation either, and the reason is the shape rather than the
seller.** 128 MiB and 2 GB of disk is a WireGuard peer and nothing else, the store states that
NAT machines are not guaranteed a direct route and are not refundable, and no page read states
that its 20 NAT ports carry UDP. It is the cheapest row in the table on a monthly cycle, and it is
the row a reader should test before believing: one order, one `wg-quick up`, USD 0.22.

The prepay band still matters, because it buys a machine rather than a proof of concept. The
recommended row is USD 2.39 out of pocket for six months, with a company behind it, against USD
3.50 for a year with a one-person operator that states no UDP. Six months is the shorter commitment
and the smaller sum.

⚠ **Two rows move across the line depending on their term.** HostBrr's IPv6-only 1 GiB is USD
1.4375 billed monthly and USD 10.50 a year, which is USD 0.88 a month. DediRock's promo Saver is
USD 2.99 billed monthly and USD 9.88 a year, which is USD 0.82 a month. Neither is under USD
1.00 on the term a buyer picks by default, and both are under it only on annual prepay, which is
why a "cheapest monthly-billed" claim needs its term stated in the same sentence.

## Two different machines

**A WireGuard node needs a public UDP port.** It terminates handshakes, so the peer must be
able to send a datagram to an address and port that reach it.

**A health monitor needs outbound traffic and a clock.** It polls other hosts. It never
accepts a connection, so a machine behind CGNAT with no forwarded port is fine.

The distinction matters because several vendors sell an inbound-less machine as a discount.
EQVPS charges USD 3.00 a month for a box that states "No arbitrary inbound ports - you
cannot host a public server", which is ten times Gullo's box that can accept one. Its NAT line
does say inbound on "your personal port", so it is **one** forwarded port and not none: enough
for WireGuard, which needs exactly one, and not enough for anything else. For a monitor it is
a working machine at a poor price; for a tunnel it is one port and a five-month-old domain.

The distinction sets the two answers at the top of this page. A tunnel needs one forwarded port that
carries UDP. A monitor needs neither a port nor an address of its own.

## The rows

| plan | Monthly | Shape | IPv4 | IPv6 | Forwarded ports | UDP stated | Transfer | Term | What breaks it |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `tierhive-micro` | **USD 0.10** | 1 vCPU / 128 MiB / 1 GB | shared NAT | /64 | 4, of which 2 carry UDP | **yes** | no byte allowance, fair use | **hourly**, USD 0.000135/h | 128 MiB and 1 GB of disk; the vendor calls itself no-SLA and warns data is not recovered; the terms refuse signup from China, Russia, Brazil, Vietnam and Iran |
| `luo-cloud-lxc-nat` | **USD 0.22** | 1 vCPU / 128 MiB / 2 GB | shared NAT | 1 address | 20 | not stated | 1 TB at 2000 Mbit/s | **monthly**, CNY 1.50 | 128 MiB; no refund; UDP unstated; 2 units in stock |
| `virnat-us-256-kvm` | USD 0.23 | 1 vCPU / 256 MiB / 2 GB | shared NAT | /64 | 20, of which 19 carry traffic | **yes** | 200 GB at 200 Mbit/s | quarterly USD 0.80, or annual USD 2.80 | **no entity at all**: address, telephone and tax number are dashes on the about page |
| `gullos-hosting-nat-128` | **USD 0.29** | 128 MiB / 2 GB, vCPU not stated | shared NAT | /80 | 20 | not stated | 125 GB a month | annual, USD 3.50 | 128 MiB; no refund at all; UDP unstated on five pages, but a user reports wireguard-go running |
| `c-servers-nanovps-384-us` | **USD 0.40** | 1 vCPU / 384 MiB / 12 GB | shared NAT | /64 | 20 | **yes**, TCP and UDP | 2 TB at 300 Mbit/s, then fair use | **six months**, USD 2.39 | KVM; non-refundable and no backups; ports below 10000 restricted except 80 and 443 |
| `natkvm-nat-lxc` | USD 0.42 | 1 vCPU / 256 MiB / 5 GB | shared NAT | 1 dedicated | 20 | **yes, contradicted by users** | 800 GB | annual, USD 4.99 | **the UK company it traded under was dissolved in 2023**; the entity named now is Pakistani with no number; UDP reported blocked by default until a ticket |
| `natvps` | USD 0.63 | 1 vCPU / 512 MiB / 5 GB | shared NAT | /80 | 20 plus 1 SSH | not stated | 750 GB | annual, USD 7.50 | UDP unstated though the vendor documents WireGuard; the order page renders empty, so stock was not read |
| `cheap-host-nat-start` | USD 0.73 | 1 vCPU / 1 GiB / 10 GB | shared NAT | none | **999 TCP/UDP** | **yes** | unlimited at 100 Mbit/s | monthly, 59 RUB | no IPv6; no terms page; a four-month-old domain; **port 25 blocked**. The ladder runs to NAT Plus at 349 RUB (4 vCPU / 8 GB / 50 GB, USD 4.29) |
| `dedirock-promo-vps-saver` | USD 0.82 | 1 vCPU / 1 GiB / 10 GB | dedicated | none stated | all | **not stated**; no forwarding layer to omit it, and a host firewall was not tested | 1 TB | **annual prepay**, USD 9.88 on a Black Friday SKU; the default is monthly at USD 2.99 | **non-refundable by policy**; a chargeback is a terms violation; the named LLC is not in the Florida register |
| `softshellweb-lxc-ipv6-only` | USD 0.83 | 1 vCPU / 1 GiB / 15 GB | none | /64 | none | n/a | 750 GB | annual, USD 9.95 | IPv6-only; the cheap plan's refund window defaults to 3 days |
| `c-servers-nanovps` | USD 0.90 | 2 vCPU / 1 GiB / 30 GB | shared NAT | /64 | 20 | not stated | 5 TB | USD 2.69 per 3 months | prepay; UDP forwarding unstated, so a tunnel here is unverified |
| `hostbrr-ipv6-1g` | USD 1.44 monthly, USD 0.88 annual | 1 vCPU / 1 GiB / 15 GB | none | /64 | none | n/a | 2.5 TB | USD 1.4375 a month, or USD 10.50 a year | IPv6-only; **over the line monthly**, under it only on annual prepay |
| `cloudcone-ssd-vps-1` | USD 2.33 | 2 vCPU / 1 GiB / 30 GB | dedicated | 3 addresses | all | all ports | 4 TB | annual, USD 28.00 | annual prepay; over USD 1 |
| `alphavps-c2g` | USD 2.84 | 2 vCPU / 2 GiB / 30 GB | dedicated | /64 | all | all ports | 3 TB | annual, EUR 30.50 | over USD 1; the best shape above the band |
| `62yun-promo-vds` | USD 2.97 | 1 vCPU / 1 GiB / 10 GB | stated | stated | not stated | not stated | unlimited at 1 Gbit/s | monthly | promo tariff, renewal not published; port policy unstated |
| `cloudfanatic-standard-1gb` | **USD 2.99** | 1 vCPU / 1 GiB / 30 GB | dedicated | 1 address | all | all ports | unmetered fair share | monthly | over USD 1; **a named US corporation, a 7-day money-back window and a reported 99.9% SLA** |
| `eqvps-nat-nano` | USD 3.00 | 2 vCPU / 1 GiB / 15 GB | shared NAT | none | **one personal port** | not stated | not stated | monthly | one port, not none; no company named; a five-month-old domain |
| `oracle-cloud-vpn-node` | USD 0 | 1 OCPU / 1 GiB / 47 GB | public | VCN | all | all ports | 10 TB | always free | card at signup; the reclaim test |
| `route64-tunnel` | USD 0 | **not a machine** | none | routed /56 | n/a | it is the tunnel | 200 Mbit/s design | none | it is an ingress, not compute |

⚠ **The two C-Servers rows disagree in the UDP column, and the disagreement is in their records.**
The 384 MiB record carries the vendor's statement that the 20 NAT ports carry TCP and UDP. The
1024 MiB record carries no such sentence and still reads "not stated". The vendor statement is about
the product's 20-port block rather than one SKU, so it probably covers both, and no page read says so
for the 1024 MiB plan.

The two free rows are here because a reader will ask. Oracle is a real VM and it fails on
identity, not capacity: a card at signup, and a seven-day p95 reclaim test. The ROUTE64 row is
an IPv6 prefix over WireGuard and not a machine; it is the `egress` topic's and is listed so
nobody buys it as compute.

One free candidate is excluded for a different reason. `microlxc-tiny` offers 1 core, 64 MiB
and 2.56 GB at USD 0 with 20 forwarded ports, and it is orderable: six of sixteen locations are
out of stock and the other ten are not. What it does not state is the protocol. UDP appears
nowhere on the homepage, the deploy page or the raw HTML, so a WireGuard endpoint there is
unverified rather than impossible. It is the one row that would be free if a single
`iptables -t nat -L` on a deployed container showed the forwards carry UDP. ⚠ The home page
advertises 256 MiB and the deploy page lists 64 MiB, so the shape is itself unsettled.

## The sub-dollar rows that are advertised and not buyable

Two prices under USD 1.00 were found that cannot be bought today, and they are recorded rather
than dropped so they are not rediscovered as candidates:

| row | the price | why it is not a row |
| --- | --- | --- |
| `luo-cloud-lxc-nat` HK-2, HK-3 | CNY 1.00, USD 0.15 | sold out; the store shows zero units |
| `firstbyte-msk-kvm-start` | RUB 75, USD 0.93 | 1 vCPU / 768 MB / 7 GB **KVM with a dedicated IPv4** in Moscow, and the rung is marked sold out; the buyable rung is the same shape with 5 GB of disk at RUB 259, USD 3.22 |

⭐ **FirstByte is the one to watch.** A 768 MB KVM box with a dedicated IPv4 at USD 0.93 a
month is the shape this band actually wants. It is a real virtual machine rather than a
container, with an address that is the buyer's, and it exists and is out of stock. Its buyable
rung is USD 3.22, which is three times the advertised figure. A reader who quotes the RUB 75 has
quoted a price nobody can pay.

## Who stands behind the price

At this price the seller matters more than the shape, and the sellers are one-person
operations. What each one's own site and the public record say, read on 2026-10-24:

| plan | the seller | domain created | refund | risk |
| --- | --- | --- | --- | --- |
| `cloudfanatic-standard-1gb` | Cloudfanatic, INC., Illinois; trading since 2020-06 as Servercheap | 2021-12-06 | 7-day guarantee for new customers, once; crypto not refundable | **low** |
| `softshellweb-lxc-ipv6-only` | "registered UK company", no number given | 2019-02-20 | 7 days first-time only; the cheap plan defaults to 3 | medium |
| `gullos-hosting-nat-128` | no company named; a single operator | lookup failed, no RDAP for `.me` | **none**; a mandatory "no refunds" checkbox | medium |
| `microlxc-tiny` | no company named; a hobby project | 2020-05-16 | not applicable, it is free | medium |
| `eqvps-nat-nano` | no entity, no country, no address | **2026-05-27** | no cash refund; unused days become credit | medium |
| `natkvm-nat-lxc` | "KhanWebHost PVT LTD", a Pakistani company with **no registration number published**; the UK number it traded under, 13550380, was dissolved 2023-12-26 | 2021-07-02 | 72 hours, case by case; the site also says 2 days, 3 days and 48 hours | **high**; the domain expires 2026-11-28 |
| `cheap-host-nat-start` | no company named; Russian-language, RUB | **2026-06-14** | no terms page exists | **high** |
| `dedirock-promo-vps-saver` | Dedi Rock LLC, Clearwater FL, **named by the vendor and absent from the Florida register**; ATLAS CLOUD LLC, L21000425604, Active, is the only Florida entity the corpus pairs with the brand | 2021-12-14 | **non-refundable by policy**; a chargeback is a terms violation | **high** |
| `tierhive-micro` | Kernel Keepers LTD, Co. No. 16294246, London, **Active**, incorporated 2025-03-05 | not read | hourly, cancel anytime; the about page warns data is not recovered | medium |
| `c-servers-nanovps-384-us` | Centerfield Ltd, Co. No. 14864789, Manchester, **Active**, at the address the store footer prints | not read | **none**; "No Backups and Non-Refundable" | medium |
| `virnat-us-256-kvm` | **no entity at all**: the about page fills the registered-name row with "VirNAT" and leaves address, telephone and tax number as dashes | not read | not read | **high** |
| `natvps` | "NatVPS Services", a GSTIN, an Indian tax registration and not a company number | not read | not read | medium |

⛔ **Cheap-Host is not payable without a Russian bank.** Its payment block is five Russian rails
(SBP, SberPay, YuMoney and MIR cards) plus crypto, and its card line reads "payment with Russian
cards". No PayPal and no international Visa or Mastercard. A buyer without a Russian bank
account pays in crypto or does not buy, which also removes the chargeback.

**How to pay each one**, from the vendor's own checkout where it was read and from the record's
rails field where it was not, read on 2026-10-24:

| plan | rails the vendor lists | a debit card is stated |
| --- | --- | --- |
| `tierhive-micro` | **not read**: the feature list states only "No credit card required" | **unverified** |
| `gullos-hosting-nat-128` | **not established**: the order page read carries no payment-method section | **unverified** |
| `c-servers-nanovps-384-us` | Stripe, PayPal, CoinPayments, Paysafecard, OXXO, carried from the vendor's other record and not re-read for this SKU | **unverified** for this SKU |
| `natkvm-nat-lxc` | credit card, PayPal | no, "credit card" |
| `virnat-us-256-kvm` | **not read**: the store and the configure page list no payment method | **unverified** |
| `natvps` | **not read**: the signup page was not fetched | **unverified** |
| `cheap-host-nat-start` | SBP, SberPay, YuMoney, MIR, crypto | **Russian cards only** |
| `dedirock-promo-vps-saver` | Visa, MC, Amex, Discover, PayPal, Bitcoin, cheque | no, cards listed and debit not stated |
| `softshellweb-lxc-ipv6-only` | PayPal, **credit and debit cards**, crypto via NOWPayments, Alipay, iDeal, UPI | **yes** |
| `c-servers-nanovps` | Stripe, PayPal, CoinPayments, Paysafecard, OXXO | **yes**, inferred from Stripe, at a 7.99% handling fee |
| `cloudfanatic-standard-1gb` | Visa, MC, Amex, PayPal, wire | no, cards listed and debit not stated |
| `cloudcone-ssd-vps-1` | credit and debit cards, PayPal, Alipay, from the record's rails field | **unverified**: the record's identity field says the order flow was not opened |

⭐ **No row in this set has a card hold established.** CloudCone's record states a hold of
about USD 1, refunded within 7 days, in its rails field, and states in its identity field that
the order flow was not opened, so the hold is unverified rather than published. That is still
the opposite of the credit market, where Koyeb holds USD 29: a small host selling a USD 4.99
annual plan has no reason to authorise a large amount, and no row here establishes one.

⛔ **Two of the twelve rows name a company a register shows as trading, and five name no legal entity
at all.** The rest name something a register cannot confirm: a US corporation not checked
against a state register, a "registered UK company" with no name or number, a Pakistani company with
no number, a Florida LLC the state register does not carry, and a trade name with a tax number. That
is the finding this band needed, and it is why the recommendation is the row that carries both a
written UDP statement and a company a register confirms, rather than the cheapest row or the one with
the best port documentation. A USD 2.39 loss to a registered company is a small loss. A USD 4.99 loss
to a company whose UK registration was dissolved in 2023 is the same money with no counterparty.

⚠ **The two domains created in 2026 are four and five months old.** Cheap-Host and EQVPS sell
machines at prices that undercut hosts with a decade of history, and neither publishes a
company, a terms page or a refund policy. That is not proof of anything, and it is the reason
their rows say `high` and `medium` rather than `dead`.

## Why Scaleway's "USD 0.20" is not in this table

The STARDUST1-S instance is EUR 0.0006 an hour, and the topic priced it at ten hours a day.
At 24/7 it is USD 0.49 for the instance, and **a public IPv4 costs EUR 0.005 an hour, about
USD 4.09 a month**, which is eight times the instance. A VPN node needs a reachable address, so
the honest 24/7 price is about USD 4.58 and the row belongs in the under-five lane. The
record `scaleway-stardust1-s` carries both figures. This is the sharpest example in the
topic of a price that is true and a comparison that is not.

## What to check before paying

- **The protocol, in writing.** Five rows state UDP on their forwarded ports, and one of those,
  NATKVM, is contradicted by two users. Five state a port count without a protocol, and one states
  no port policy at all. DediRock's dedicated IPv4 has no forwarding layer to omit UDP, and no page
  states the protocol either. A NAT VPS with TCP-only forwarding cannot terminate WireGuard.
  Gullo's evidence is one user's report of `wireguard-go`, which is more than nothing and less than
  a measurement.
- **Whether the seller still exists.** NATKVM traded under a UK company number that Companies
  House records as dissolved in December 2023, and the entity it names now is a Pakistani company
  with no number a register can check. DediRock names a Florida LLC that the state register does not
  carry. Ask for the current entity before paying a year, or accept the loss.
- **The refund.** C-Servers sells the recommended row "No Backups and Non-Refundable", Gullo's has
  none, DediRock states products are non-refundable once paid, and Cheap-Host publishes no terms at
  all. SoftShellWeb and Cloudfanatic publish a 7-day window, NATKVM publishes 2 or 3 days with
  crypto excluded, and TierHive bills hourly, so a stopped box is the whole cancellation.
- **Whose address it is.** A shared IPv4 is the node's, not the buyer's. If it changes on a
  rebuild, every peer configuration changes with it. The recommended row's routed /64 avoids the
  question for a peer that has IPv6.
- **The traffic meter.** 2 TB a month at 300 Mbit/s on the recommended row, then fair use at the
  same speed rather than a cut. Gullo's 125 GB is the smallest metered allowance in the table, and
  its further blocks cost USD 1.00 per 125 GB.
- **The kernel.** An LXC or OpenVZ host may not expose the WireGuard module. The plan page
  stating TUN and TAP is the closest thing to a guarantee available without an account. The
  recommended C-Servers row is KVM, so the guest runs its own kernel and loads the module itself.

## What is not verified

⛔ **No account was created and no handshake was run.** Every row is `documented`. The UDP claim is
the vendor's sentence, not an observed datagram. On the recommended row that sentence comes from the
vendor's own knowledge base as a search index returned it, because the live article answers a
Cloudflare challenge to both the text extractor and a raw fetch; the same statement is indexed in
English and in French. What would settle it is one signup, one `wg-quick up`, and one handshake from
a second network, and that is the first item this topic should measure. The renewal rate of the
recommended row is not published, and no card hold is established on any row.

The per-provider sentences are in the records named in the first column. The tunnel side of
the same question, including ROUTE64 and the free UDP forwards, is the `egress` topic's:
[`../../egress/free/wireguard-ingress.md`](../../egress/free/wireguard-ingress.md).
