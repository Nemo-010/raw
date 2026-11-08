# The small and regional providers

Every row below was read at its own page. Most fail. The page exists so that a reader
who meets one of these names in a search result finds a date, a verdict and the sentence
that decides it.

⭐ **Three rows here are shapes worth knowing: a peer-to-peer TCP and UDP proxy, a
game tunnel with a 24-hour session, and a WireGuard forwarding fabric.**
None of them is a household name and all three carry UDP.

| provider | what it is | free tier | UDP | verdict |
| --- | --- | --- | --- | --- |
| PortPlay | a game tunnel, 24-hour sessions | free forever, 1 port, 10 players | yes | `qualifies-with-caveat` |
| NodeMesh | a mesh that publishes a peer | free for one host | yes | `qualifies-with-caveat` |
| ProximaTunnel | a hosted tunnel | freemium, no volume published | yes | `qualifies-with-caveat` |
| Mudcat | a hosted tunnel | free with an 8-hour hostname lease | yes | `fails-quota` |
| TaiwanFrp | a Taiwanese public relay | free, TCP and UDP together | yes | `qualifies-with-caveat` |
| UlziX HK NAT | a free Hong Kong NAT VPS | 10 Mbit, a monthly human step | yes | `qualifies-with-caveat` |
| OpenTunnel | free WireGuard servers by country | unlimited data, a 7-day account | outbound only | `trial-only` |
| Somagu | a Korean NAT VPS | USD 0.54/month | yes | `paid-only` |
| Oray Peanut Hull | the largest Chinese NAT product | 1 GB/month | yes | `fails-identity` |
| Bili NAT | a Chinese NAT panel | CNY 8.88 one-time | yes | `paid-only` |
| 神卓互联 | a Chinese NAT panel | free, unlimited traffic since 2020 | yes | `trial-only` |
| 飞鸽 | a Chinese NAT panel | 0.5 Mbit/s, 20 connections | yes | `fails-quota` |
| Sunny NGrok | a Chinese ngrok clone | 2 Mbit/s, 1 tunnel | yes | `fails-quota` |
| Luyouxia | a Chinese panel | 1 GB/month, 1 Mbit/s | TCP only | `fails-egress` |
| Cpolar | a Chinese panel with an English site | 1 Mbit/s, random URL | TCP only | `fails-egress` |
| LocalPort | a paid-only tunnel | none | TCP only | `paid-only` |
| ShubhamTun, Proxlane | small TCP tunnels | 3 tunnels, 1 tunnel | TCP only | `fails-egress` |
| OnlySSH | an SSH proxy account | free UDP tunnel advertised | as advertised | `fails-egress` |
| FxTunnel, Steadip, Tunnl, Tunr, Pipenet, Tunnel To, Freehold | HTTP only | 2 GB to none | no | `fails-egress` |
| Stunl | a session tunnel | 2 GB/month, 1-hour sessions | no | `fails-quota` |
| Kemnir | a beta with no price | none published | TCP only | `fails-egress` |
| Malai | paused | none | none | `dead` |
| PCDeploy | a game panel | none readable | yes | `dead` |
| LusoVPS, RDPServers, FreeVPSHostings | free IPv6 and trial VMs | 10 GB, 1 TB, 7 days | yes | `trial-only` |
| MCGateway, Solar Proxy, GuildBit, BedrockTogether | game-specific relays | free | no | `fails-egress` |
| Hosting Minecraft Pro | a new game proxy | none yet | yes | `paid-only` |
| Holesail (self-hosted) | a peer-to-peer TCP and UDP proxy | free, no account | yes | `qualifies-with-caveat` |
| BastionRoute (self-hosted) | a WireGuard forwarding fabric | free, no volume published | yes | `qualifies-with-caveat` |
| Arena Tunnel (self-hosted) | AGPL software, no service | none | TCP only | `paid-only` |

## Holesail

A peer-to-peer proxy for TCP and UDP with no account and no relay in the normal
case (`documented`, read 2026-10-23). Two peers connect directly and the service
is a signalling layer, so its volume is the peers' link rate rather than a quota.

⚠ **A direct peer-to-peer path carries nothing when hole-punching fails**, and no
published figure covers the relay fallback. The record says so.

## PortPlay and NodeMesh

PortPlay gives one game port, ten players and a 24-hour session on a free plan
that never expires (`documented`, read 2026-10-23). NodeMesh publishes one of the
reader's own machines and is free for a single host. Both carry TCP and UDP, and
both fail the volume test at the scale this topic asks for: a ten-player session
is not a terabyte.

## The Japanese and Korean hosts

Five records cover those markets, read in their own language. **Sakura Internet** gives a
free trial of every VPS plan on a card; **Xserver VPS** ran a free VPS campaign that has
ended; **WebARENA SuitePRO** gave a 20-day trial; **Naver Cloud** gives one Micro Server
free for a year but requires a Korean identity; **OwnServer** advertised a free game
server without limits and no longer answers (`documented` and `reported`, read
2026-10-23).

⛔ **The pattern in that market is an identity gate or an ended campaign.** No
Japanese or Korean provider found here gives a standing free route to a UDP port,
and the two that did are closed.

## TaiwanFrp, UlziX and OpenTunnel

**TaiwanFrp** is a Taiwanese public relay that states it forwards TCP and UDP at
the same time, with no byte allowance anywhere (`unverified`, read 2026-10-23).
The failure its own site shows is an expired account, which is why the record
names `retention-clamped`.

**UlziX** gave away a Hong Kong NAT VPS at 10 Mbit. 10 Mbit carries a terabyte a
month, so the shaping does not bind; what binds is supply, because the offer was a
pre-sale with a monthly human step (`reported`).

**OpenTunnel** publishes free WireGuard servers per country with unlimited data
and a 7-day account life (`documented`). ⛔ It is a VPN exit and not an ingress:
the peer gets a private address and no inbound port, so it fails the ingress test
even though it is WireGuard-native and unmetered.

## The Chinese panels

Oray's Peanut Hull is the largest of them, with 1 GB/month free and a mainland
identity gate. Bili NAT sells a CNY 8.88 one-time plan with check-in traffic.
Shenzhuo says its free edition stopped limiting traffic in 2020 and the record is
still `trial-only` because no current page confirms the allowance.

⛔ **The pattern is the same as the frp page: a real offer, a small quota, and an
identity or a check-in.** None of these rows clears 1 TiB/month.

## The HTTP-only and TCP-only rows

FxTunnel, Steadip, Tunnl, Tunr, Pipenet, Tunnel To and Freehold are HTTP tunnels.
ShubhamTun, Proxlane and Arena Tunnel forward TCP and not UDP. A WireGuard
datagram cannot cross any of them without a wrapper at both ends, which is the
host problem described in [`wireguard-transports.md`](wireguard-transports.md).

## What is dead

- **Malai**: the deployment is paused.
- **PCDeploy**: advertised as free and no page confirms it is still running.
- **FreeVPSHostings' Learner plan**: seven days and no root.

## Chaining

**The peer chain.** `Holesail -> a direct UDP path -> a WireGuard listener`. The
scarce link is a successful hole punch.

**The game chain.** `PortPlay -> one UDP port -> a small service`. The scarce link
is a 24-hour session.

## The records

All in `dossier/egress/`: `holesail`, `portplay`, `nodemesh`, `proximatunnel`,
`mudcat`, `bastionroute`, `taiwanfrp`, `ulzix-hk-nat`,
`opentunnel-wireguard-singapore`, `vpnjantit-ssh-singapore`, `somagu-vps`,
`oray-peanut-hull`, `bili-nat`, `shenzhuo-hulian`,
`feige-fgnwct`, `sunny-ngrok`, `luyouxia`, `cpolar`, `arena-tunnel`,
`localport`, `shubhamtun`, `proxlane`, `onlyssh`, `fxtunnel`, `steadip`,
`tunnl-gg`, `tunr`, `pipenet`, `tunnel-to`, `freehold`, `stunl`, `kemnir`,
`malai`, `pcdeploy`, `lusovps-ipv6-free`, `rdpserverss-free-ipv6`,
`freevpshostings-com`, `mcgateway`, `solar-proxy`, `guildbit`,
`bedrocktogether`, `hosting-minecraft-pro`, `sakura-internet-vps`,
`xserver-vps-free`, `webarena-suitepro-trial`, `naver-cloud-micro`, `ownserver`.

⚠ **Every row here is a page read and none was probed.** A name that answers today
and not next month is the normal case in this class.
