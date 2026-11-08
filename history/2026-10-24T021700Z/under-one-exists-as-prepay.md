# Under USD 1 a month exists, and only as annual prepay

- **When:** 2026-10-24T02:17:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/README.md`, which states that Scaleway's STARDUST1-S at USD 0.20 a month is "the only machine in this topic under USD 1 a month", and the absence of any sub-dollar row from `docs/compute/paid/micro.md`
- **Superseded by:** five machines read on 2026-10-24 at the vendor's own page, all annual or six-month prepay, and one negative result that matters as much: no monthly-billed machine under USD 1.00 exists in anything that was read
- **Evidence:** `.tmp/compute-2026-10-24/lanes/L01-sub1-monthly/report.md` and `.tmp/compute-2026-10-24/lanes/L09-vpn-nat/report.md`, with the per-provider sentences in their dossier records
- **Confidence:** documented

## The rows

| machine | price | monthly equivalent | shape | IPv4 | forwards a UDP port | term |
| --- | --- | --- | --- | --- | --- | --- |
| NATKVM LXC NAT | USD 5.50/yr | **USD 0.46** | 1 vCPU / 256 MiB / 5 GB | shared NAT | **yes, 20 ports, UDP and TCP stated**, TUN/TAP | annual |
| Cheap-Host NAT Start | 59 RUB/mo | USD 0.73 | 1 vCPU / 1 GiB / 10 GB | shared NAT | 999 ports, TCP and UDP stated | monthly |
| SoftShellWeb LXC IPv6 | USD 9.95/yr | USD 0.83 | 1 vCPU / 1 GiB / 15 GB | **none** | IPv6 only, /64 | annual |
| DediRock Promo Saver | USD 9.88/yr | USD 0.82 | 1 vCPU / 1 GiB / 10 GB | dedicated | yes, all ports | annual |
| Gullo's NAT 128 | USD 10.00/yr | USD 0.83 | 1 vCPU / 128 MiB / 5 GB | shared NAT | 20 ports, UDP unstated | annual |

## The negative result

**No monthly-billed machine under USD 1.00 was found.** The cheapest monthly-billed
machine with any IPv4 is DediRock at USD 2.99; the cheapest monthly-billed machine at all
is HostBrr's IPv6-only 1 GiB at USD 1.44. So the sub-dollar band is a prepay band: the
buyer pays USD 6 to USD 12 once and holds the machine for a year.

That changes what the row means. A USD 0.46 a month machine is USD 5.50 out of pocket and
a twelve-month commitment to a small operator, not a monthly subscription. `micro.md`'s
ladder already refused to treat an annual total divided by twelve as a monthly bill, and
this entry applies the same rule to the band below its first rung.

## Why Scaleway's USD 0.20 was not the answer

The STARDUST1-S instance is EUR 0.0006 an hour, and the record priced it at ten hours a day.
Two corrections follow. At 24/7 it is about USD 0.44 a month for the instance, and **a
public IPv4 costs EUR 0.005 an hour, about USD 4.09 a month**, which is nine times the
instance. A WireGuard endpoint needs a reachable address, so the honest 24/7 price of that
row is about USD 4.58, and it belongs in the under-five lane and not this one.

## What the port claim rests on

A WireGuard endpoint needs a UDP socket the internet can reach. Two of the five rows state
UDP forwarding in the vendor's own words; one states TCP only; two state a port count and
no protocol. Only NATKVM states UDP, TUN/TAP and a dedicated IPv6 on the same plan, which is
why it is the row and the others are alternatives. No handshake was run, so this is a
documented capability and not a measured one.
