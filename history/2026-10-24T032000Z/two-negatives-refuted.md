# Both negatives this pass wrote were refuted by one page each

- **When:** 2026-10-24T03:20:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/paid/under-one.md`, which states twice that "nothing monthly was found under USD 1.00" and calls the sub-dollar band a prepay band; the Q2 table row for `gullos-hosting-nat-128` at USD 10.00 a year; the row for `eqvps-nat-nano` saying it "cannot accept a connection at all"; the `microlxc-tiny` shape at 256 MiB; and the `natkvm-nat-lxc` verdict that treated it as the answer
- **Superseded by:** the vendors' own pages read on 2026-10-24, quoted in each record's `evidence[]`
- **Evidence:** `dossier/compute/luo-cloud-lxc-nat.json`, `gullos-hosting-nat-128.json`, `natkvm-nat-lxc.json`, `eqvps-nat-nano.json`, `microlxc-tiny.json`, `firstbyte-msk-kvm-start.json`, and the lane reports at `.tmp/compute-2026-10-24/lanes/L22-subdollar-credibility/report.md` and `L23-subdollar-refute/report.md`
- **Confidence:** documented

## The two negatives, and what killed them

**"No monthly-billed machine under USD 1.00 exists."** It does. luo_cloud sells a German LXC
NAT box at **CNY 1.50 a month, USD 0.22**: one vCPU on a Ryzen 9 7900, 128 MiB, 2 GB SSD,
1 TB at a 2000 Mbit/s shared port, 20 NAT ports and one IPv6, on the store's own monthly cycle
(月繳). Two units were in stock at the time of the read. A US box at CNY 2.00 (USD 0.30) had ten
units, and a Hong Kong box at CNY 1.00 (USD 0.15) was sold out. The refutation took one search
in Chinese: `一元VPS`, `月付 便宜 VPS`, `NAT VPS 月付`.

⛔ **The worse half is that Cheap-Host at USD 0.73 was already in the same document's table**
while a paragraph three lines above said nothing monthly existed. The document contradicted
itself and neither half was checked against the other. A negative claim about a market is the
cheapest claim to write and the most expensive to get wrong.

**"NATKVM is the answer."** Its own site prints "Registered in England & Wales (Company No:
13550380)", and Companies House returns **"Dissolved on 26 December 2023"** for KHAN WEB HOST
LTD, incorporated 2021-08-05, with no successor entity named anywhere. Two public refund
refusals on annual plans sit on either side of that date, and a third thread describes outages
lasting hours almost daily. The money at risk is USD 4.99, so the correction is not that the
vendor is dangerous; it is that the recommendation rested on a counterparty that does not exist
when a cheaper one with a working WireGuard report does.

## The four rows that were simply wrong

| row | was | is | what took it away |
| --- | --- | --- | --- |
| `gullos-hosting-nat-128` | USD 10.00 a year, USD 0.83 a month | **USD 3.50 a year, USD 0.29 a month**, renewing at the same rate | the order page prints "1 Year @ $3.50" and "FR NAT IPv4 128MB (Oct 23, 2026 - Oct 23, 2027) 1 @ $3.50". The row was three times too expensive |
| `eqvps-nat-nano` | "cannot accept a connection at all" | one personal inbound port on the NAT line | the page states inbound on "your personal port" beside "No arbitrary inbound ports". One port is exactly what WireGuard needs |
| `microlxc-tiny` | 256 MiB | **64 MiB** | the deploy page lists 64 MiB while the home page advertises 256 MB; the two pages disagree and the deploy page is the one that sells |
| `natkvm-nat-lxc` | USD 5.50 a year | **USD 4.99 a year** for the NL 256MB NAT rung, same 20 ports, UDP, TUN/TAP and one IPv6 | a store card the first pass did not open |

## What the recommendation is now

**Gullo's Hosting, USD 3.50 a year, USD 0.29 a month**, because it is the cheapest row that is
also the only one in the band with a first-hand public report of WireGuard running on it: a user
installed precompiled `wireguard-go` and ran it with shadowsocks "without running out of ram"
across 255 days of uptime, and another confirms TUN and TAP can be enabled. It has no refund at
all and names no company, which is why the row says medium risk and not low.

**Cloudfanatic at USD 2.99 a month** is the answer if the node must not fail: a named Illinois
corporation, monthly billing, a written 7-day guarantee, a published SLA, a dedicated IPv4 with
all ports open, and five years of independent monitoring showing two outages of two or three
minutes. Three times the line, and the only row in the set where nothing important is
unverified.

## The lesson, stated as a rule for the topic

⭐ **Search in the language of the market before writing a negative.** Both negatives in this
pass were English-language searches over English-language hosts. The sub-dollar market is
Chinese and Russian, and one query in each language produced a counterexample. A negative is a
claim about a search, so it carries the search's scope in the same sentence or it is not a
finding.

⚠ **A price under a dollar is usually a shape nobody wants.** luo_cloud's USD 0.22 buys 128 MiB
and 2 GB of disk, FirstByte's USD 0.93 buys 768 MB and a dedicated IPv4 and is sold out, and
Gullo's USD 0.29 buys 128 MiB. The band is real and it is thin; the row worth running for a year
is the one with a report of somebody having run it.
