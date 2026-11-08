# VPN subscriptions as exit sources

A VPN sells one exit per connection, drawn from a pool, for a flat monthly price.
The question that matters is not how many servers it has. It is **how many distinct
ASNs those servers sit in, and whether one can be pinned.**

**The question:** which VPN gives the most distinct ASNs per dollar?

**The answer:** **Windscribe, at 58 ASNs on a USD 39/year plan**, and it is also
the only vendor selling a *residential* static exit at a published price. Mullvad
is the best for control: 566 individually named relays across 27 ASNs, each
pinnable by hostname, for EUR 5 flat and payable in cash. But the market is
concentrated: **the largest two hosting ASNs alone hold about a third of the 1,720
prefixes measured here.**

---

## The measured ASN diversity

Every row was computed from the vendor's own published server list or API on
2026-10-24, then resolved with RIPE.

| vendor | price | servers | distinct ASNs | /24s | largest ASN share |
|---|---|---|---|---|---|
| **Windscribe** | USD 9.00/mo list, **USD 39/yr** | 1,074 IPs | **58** | 239 | AS212238 Datacamp, 26% |
| **Mullvad** | **EUR 5/mo flat** | 566 relays | **27** | 258 | AS9009 M247, 24% |
| IVPN | not readable | 178 hosts | 22 | 92 | — |
| **NordVPN** | USD 3.49/mo (2 yr) | **7,193** | **25** | 775 | **AS212238, 45%** |
| Proton VPN | USD 9.99/mo list | **21,202** | not enumerable | — | measured exit AS212238 |
| AirVPN | EUR 49/yr | — | — | — | no traffic limit, 5 ports |

⛔ **Counting servers as addresses overstates the answer by 8× to 288×.** NordVPN
has 7,193 servers across 25 ASNs; Mullvad has 566 across 27. The server count is a
capacity number, not an identity number.

⭐ **Windscribe's 58 ASNs on a USD 39/year plan is about USD 0.06 per ASN**, the
best ratio found. ⚠ **Use the USD 39 annual price, not a monthly one:** USD 5.75 is
USD 69/12, a figure from a different record that is not verified here.

## The concentration, from the records that own it

| ASN | holder | prefixes in the records here | share of 1,720 |
|---|---|---|---|
| AS212238 | CDNEXT Datacamp Limited | NordVPN 347 + Windscribe 62 + Mullvad 46 = **455** | **26.5%** |
| AS9009 | M247 Europe SRL | Mullvad 61 | 3.5% |

⛔ **The two rows above are the sum of what `nordvpn-exits.json`,
`windscribe-vpn.json` and `mullvad-vpn.json` carry.** A full union needs records for
IVPN, AzireVPN, PIA and AirVPN, which this topic does not have.

⚠ **What the two rows still show is the point:** the single measured Proton exit,
45% of NordVPN's prefixes and 26% of Windscribe's are the **same hosting ASN**. A
reader buying three VPNs for diversity may be buying one network three times.

⚠ **Virtual locations are the same finding by another method.** An independent
count (`vpnmap.ominuvo.com`, updated 2026-10-24) puts Proton at 149 countries with
**85 virtual**, NordVPN at 95 of 150 and PIA at 62 of 113. A "virtual location" is
a shared exit reached from another country. Two independent methods agree, and its
per-provider country totals match this topic's own measurements exactly.

---

## The measured baseline: Proton inside a Worker

⭐ **This is the one non-Cloudflare exit measured working inside a Cloudflare
Worker**, and it is the topic's starting point rather than its answer.

| | |
|---|---|
| the capture | the final log of the Proton-in-a-Worker experiment |
| when | 2026-10-03T19:09:40.882Z |
| result | HTTP 200, 14 bytes, body `149.50.216.236` |
| the exit | `149.50.216.236/24` |
| the network | **AS212238 CDNEXT Datacamp Limited** (RIPE, checked 2026-10-24) |
| handshake | 504 ms |
| the inner stack | WireGuard over a WebSocket, MTU 1320, `10.2.0.2/32` and `2a07:b944::2:2/128` |

⛔ **So the question is not whether a Worker can leave Cloudflare's network. It
can.** The question is whether AS212238 is better than AS13335 at an upstream, and
it is not: it is a hosting ASN. **Proton buys rung 4 and refuses rung 5**, at the
price of a subscription.

⚠ **The `/vpn/logicals` API now requires auth** (401 with every `x-pm-appversion`
tried, 422 for older versions), so Proton's 21,202 servers could not be enumerated
at ASN level. Only the one measured exit is known.

---

## Port forwarding, which is a different question

`egress` owns the ingress question, but one fact belongs here because it decides
whether a VPN can be both an exit and an entry:

- ⛔ **Mullvad removed port forwarding.** Its blog announces the removal, so it is
  an exit source and not an ingress one.
- **AirVPN** still forwards up to 5 ports, ports ≥ 2048, with no traffic limit
  (recorded in `dossier/egress/airvpn.json`).
- **Windscribe's static IPs are shared**: *"We do not offer dedicated IPs for
  privacy reasons … we allocate a single IP address to a handful of customers, so
  your activity can still be lost in the crowd."*

⭐ **That last sentence matters for this topic more than for `egress`.** A "static
IP" that a handful of customers share is rung 2 with a collision risk, not a
dedicated address.

---

## The providers

<!-- generated:start topic=ip-proxy kind=provider verdict=qualifies sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mullvad VPN | No free tier. The pricing page read 2026-10... | qualifies | documented | not applicable: an exit address... | not applicable: a liv... | anonymous | `dossier/ip-proxy/mullvad-vpn.json` |
<!-- generated:end -->

## What a subscription cannot do

| if the upstream keys on | a VPN helps | why |
|---|---|---|
| rung 2, the address | ✅ yes | pin a host, keep the address |
| rung 3, the subnet | ⚠ maybe | the 27 to 58 ASNs are spread over hundreds of `/24`s |
| rung 4, the ASN | ✅ **yes, this is what is being bought** | 27 to 58 networks instead of one |
| rung 5, the class | ❌ mostly no | AS212238 and AS9009 hold 30% of the measured prefixes |
| rung 6, the account | ❌ no | the account is the VPN's, not the upstream's |

⛔ **The device cap binds before the ASN count does.** Mullvad's 27 ASNs need 27
devices against a 5-device limit, which is 5.4 accounts. A subscriber who wants N
pinned addresses in N ASNs needs to read the device cap first.

## The cheapest useful purchase

⭐ **Windscribe at USD 39/year.** 58 ASNs, a free tier to test with, and a
residential static at USD 96/year that no other vendor sells at a published price.
The one thing to verify before relying on it is whether that residential static
actually reads as residential to an upstream. The vendor's own privacy stance
means the address is shared, and sharing is what a rung-5 gate would look for.

⚠ **TorGuard's residential dedicated IP at USD 19.99/month is the cheapest
per-address residential product found**, and its claim could not be checked: its
server list is Cloudflare-walled and it publishes no ASN. One purchase and one RIPE
query settles it.
