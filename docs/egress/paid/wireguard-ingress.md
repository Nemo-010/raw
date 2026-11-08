# The paid ladder for a WireGuard ingress

Free is the first question and it is answered on
[`../free/wireguard-ingress.md`](../free/wireguard-ingress.md). This page is what a
terabyte or two a month costs when a free row is not good enough, priced at the
volume this topic measures.

⭐ **Two paid shapes undercut every hosted tunnel: a managed WireGuard tunnel at
EUR 2 a month with a terabyte included, and a VPN with port forwarding at about
USD 4 a month with no traffic cap.** A managed WireGuard ingress product at USD 8
for 1 TB is not the cheap end of this market; it is the middle.

Sorted by cost for the first year at one terabyte a month. The four VPS rows, on which
the reader runs `wg-quick`, come last whatever their price: a self-hosted ingress is the
last resort (`AGENTS.md` section 2 rule 9).

| provider | the product | traffic | price | WG config | identity |
| --- | --- | --- | --- | --- | --- |
| TaipanTransit | a WireGuard tunnel at up to 1 Gbit/s | 1 TB included, then EUR 0.35/TB | EUR 2/month at the campaign rate | official `.conf` | card |
| HYEHOST | an IPv4 `/32` over a tunnel | no byte cap, 100 Mbit/s at the 95th percentile | USD 1.50 per IPv4 | `.conf` | card |
| AirVPN | a public IPv4 plus reserved ports | no traffic limits | EUR 49/year (EUR 4.08/month) | official `.conf` | card |
| OVPN | 7 ports, 49152 to 65535, TCP or UDP | unlimited | USD 4.22/month on 36 months, USD 12 monthly | official `.conf` | card |
| AzireVPN | per-device ports | no cap published | EUR 5/month, EUR 4 monthly on 3 months | official `.conf` | card |
| Private Internet Access | a forwarded port | unlimited | USD 3.99/month on a year | official toolkit | card |
| GetAStatic | a dedicated address and ports | 100 GB at USD 2, 1 TB at USD 4 | USD 4/month for 1 TB | WireGuard | card |
| tunnel-ip | a tunnel with a public address | not stated per plan | EUR 8/month | `.conf` | card |
| Ignite Solutions | a tunnel with a public address | not stated | USD 7/month | `.conf` | card |
| Hoppy | a public IPv4 and a `/56` | 1 TB/month | USD 8/month | official `.conf` | card |
| GetPublicIP | a public address over a tunnel | not stated | USD 8.99/month | `.conf` | card |
| Stayport | a public address over a tunnel | a fair-use allowance with no number | INR 599/month | `.conf` | card |
| IPv6rs | 5 static IPv6 tunnels at 1 Gbit/s | unmetered | USD 6.95/month | official `.conf` | card |
| WireGress | egress only, no inbound | none | USD 15/month | `.conf` | card |
| Rocket Internet | a dedicated IPv4 | not stated | USD 25/month after a 30-day trial | `.conf` | card |
| Core Transit | a tunnel with an address | not stated | USD 38/month | `.conf` | card |
| Fly.io | a dedicated IPv4 plus UDP services | metered at USD 0.02/GB | USD 2/month plus about USD 22/TB | `fly wireguard create` | card |
| AWS Global Accelerator | any TCP or UDP | metered at USD 0.015/GB | about USD 33/TB all in | none | card |
| Gcore Edge Proxy | any TCP or UDP | flat | EUR 17/month | none | card |
| chunkserve (last resort: self-hosted on a rented VPS) | a VPS | 5 TB/month | EUR 1.30/month | `wg-quick` on the VM | email |
| ethernetservers (last resort: self-hosted on a rented VPS) | a VPS | 3 TB/month | USD 3.00/month | `wg-quick` on the VM | email |
| spectraip (last resort: self-hosted on a rented VPS) | a VPS | 5 TB/month | EUR 3.29/month | `wg-quick` on the VM | email |
| Hetzner Cloud (last resort: self-hosted on a rented VPS) | a VPS | 20 TB/month | USD 6.49/month | `wg-quick` on the VM | card |

## The two rows that beat the rest

**TaipanTransit at EUR 2 a month** is the cheapest managed WireGuard ingress found:
a tunnel at up to 1 Gbit/s, 1 TB of transit included, and EUR 0.35/TB beyond it at
the campaign rate (`documented`, read 2026-10-23). One TiB costs about EUR 2.04.

**AirVPN at EUR 49 a year** is the cheapest unlimited path: a public IPv4,
reserved ports that do not move between servers, and an official WireGuard
`.conf` (`documented`, read 2026-10-23). The product is a VPN, and what makes it an
ingress provider is the port forwarding.

⚠ **A VPS is not a managed product and the two are not interchangeable.** The
managed rows hand a reader an address and a `.conf` and nothing else to run. The
VPS rows hand a reader a machine, an operating system and a patching job. Both are
somebody else's hardware, but a VPS row is self-hosting, the last resort after every
managed row (`AGENTS.md` section 2 rule 9).

Last resort, self-hosted on a rented VPS: chunkserve at EUR 1.30 a month for 5 TB is
the cheapest per terabyte in the whole corpus, with 1 vCPU, 1 GB RAM, 15 GB NVMe and a
1 Gbit port (`documented`, read 2026-10-23, from the compute topic). The reader runs
`wg-quick` on it and keeps the machine patched.

## The VPN rows

Nine providers still forward a port on a paid plan, and every one of them ships a
standard `.conf`:

| provider | ports | price | note |
| --- | --- | --- | --- |
| AirVPN | reserved, not server specific | EUR 49/year | the cheapest |
| OVPN | 7 ports, 49152 to 65535, TCP or UDP or both | USD 4.22/month at 36 months | the best specified |
| Private Internet Access | one forwarded port | USD 3.99/month at a year | a toolkit rather than a `.conf` |
| AzireVPN | per-device ports that expire on restart | EUR 4 to 5/month | slots are limited |
| PrivateVPN | a forwarded port | USD 6/month at 3 months | |
| TorGuard | a forwarded port | USD 9.99/month, USD 29.99/year | |
| hide.me | dynamic port forwarding on Premium | USD 11.99/month | 10 GB free, no forwarding |
| Windscribe | port forwarding on paid plans | USD 9/month | |
| Perfect Privacy | a forwarded port | EUR 12.99/month | |

⛔ **Mullvad and IVPN removed port forwarding in 2023** and both records say so.
They remain excellent egress VPNs and they are not ingress providers. Proton,
NordVPN, Surfshark and FastestVPN were checked and none publishes a forwarded port
on a plan a reader can buy (`fails-egress`).

## The managed WireGuard products

This is a real market with published prices, and the spread is 19 times between the
cheapest and the most expensive per address.

| provider | what it sells | price | traffic |
| --- | --- | --- | --- |
| TaipanTransit | a tunnel at up to 1 Gbit/s | EUR 2/month | 1 TB included, EUR 0.35/TB after |
| HYEHOST | an IPv4 `/32` over a tunnel | USD 1.50 per IPv4 | no byte cap, 100 Mbit/s at the 95th percentile |
| GetAStatic | a dedicated address and forwarded ports | USD 2 for 100 GB, USD 4 for 1 TB | as stated |
| tunnel-ip | a tunnel with a public address | EUR 8/month | not stated per plan |
| Ignite Solutions | a tunnel with a public address | USD 7/month | not stated |
| Hoppy | a public IPv4 and a `/56` | USD 8/month | 1 TB/month |
| GetPublicIP | a public address over a tunnel | USD 8.99/month | not stated |
| Stayport | a public address over a tunnel | INR 599/month | a fair-use allowance with no number |
| IPv6rs | 5 static IPv6 tunnels at 1 Gbit/s | USD 6.95/month | unmetered |
| WireGress | egress only, no inbound | USD 15/month | none that matters |
| Rocket Internet | a dedicated IPv4 | USD 25/month after a 30-day trial | not stated |
| Core Transit | a tunnel with an address | USD 38/month | not stated |
| AnchoredIP | a trial of a dedicated IPv4 and a `/48` | USD 0 for 7 days | not metered |

⭐ **HYEHOST is the row to read twice.** USD 1.50 buys a public IPv4 over a tunnel
with no byte cap and a 100 Mbit/s 95th-percentile rate, which is about 32 TB in 30
days. That is 30 times the test for the price of a coffee.

⚠ **TaipanTransit's EUR 2 is a campaign rate and the list rate is EUR 5.** Both are
in the record, and the campaign price is what a reader gets today.

⚠ **Sidecar Network is the opposite shape and worth naming**: its free tier is 3
peers at 2 Mbit/s, which is 0.65 TB/month and fails, and every paid tier is
"unlimited data transfer" because it charges for address and speed rather than
bytes (`documented`, read 2026-10-23).

## The metered edges

Fly.io charges USD 2/month for a dedicated IPv4 and USD 0.02/GB out, so 1 TiB is
about USD 22. AWS Global Accelerator charges USD 0.025/hour plus USD 0.015/GB,
about USD 33 for a TiB with the fixed cost included. Gcore Edge Proxy is flat at
EUR 17/month with no byte meter.

⚠ **Gcore is the cheapest flat-rate managed L4 edge found**, and it is the only
paid row that is both a Spectrum substitute and cheaper than the metered
hyperscaler products at this volume.

## What is dead

- **Stayport and portmap.io paid tiers**: the pricing paths return 404, so no current
  number exists.
- **A free static IPv4**: none exists. Every result was USD 2 to 15 a month.
- **Cloudflare Spectrum**: Enterprise only, at every protocol.
- **A managed WireGuard ingress under USD 2/month with a terabyte**: none found.

## Chaining

**The cheap chain.** `AirVPN EUR 49/year -> a reserved port -> wg-quick on the
reader's own device`. No machine to run, no byte cap, and the port does not move.

**The managed chain.** `Hoppy USD 8 -> a public IPv4 and a /56 -> wg-quick`. The
scarce link is the 1 TB allowance, which is the smallest in the table.

Last resort, self-hosted: `chunkserve EUR 1.30 -> wg-quick -> every port open`. 5 TB
included, and a machine the reader maintains.

## The records

`dossier/egress/airvpn.json`, `ovpn.json`, `azirevpn.json`,
`private-internet-access.json`, `privatevpn.json`, `torguard.json`,
`hide-me.json`, `windscribe.json`, `perfect-privacy.json`, `premiervpn.json`,
`mullvad.json`, `ivpn.json`, `proton-vpn.json`, `nordvpn.json`,
`surfshark.json`, `fastestvpn.json`, `vpnbook.json`, `wevpn.json`,
`hoppy.json`, `taipan-transit.json`, `hyehost-ipv4-tunnels.json`,
`tunnel-ip.json`, `ignyte-solutions.json`, `getpublicip.json`, `stayport.json`,
`wiregress.json`, `rocket-internet-ipv4.json`, `core-transit.json`,
`anchoredip.json`, `sidecar-network.json`, `get-real-ip.json`,
`novanode-ip-tunnel.json`, `serververse-network-transit.json`,
`steadip-anchor.json`, `getastatic.json`, `ipv6rs.json`, `fly-io.json`,
`aws-global-accelerator.json`, `gcore-edge-proxy.json`, `cloudflare-spectrum.json`,
`hetzner-cloud.json`, `ovhcloud-public-cloud.json`.

The VPS comparators are compute records:
`dossier/compute/chunkserve.json`, `spectraip.json`, `ethernetservers.json`,
`contabo.json`, `hetzner-cloud.json`.

⚠ **Every price on this page is a page read on 2026-10-23 and none was bought.**
A price without a purchase is a quote, and the record says so.
