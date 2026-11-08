# WireGuard overlays and zero-trust networks: why most publish nothing

Every product on this page uses WireGuard somewhere. Almost none of them gives a
public reader an address, and the difference is the whole point of the page.

⭐ **An overlay connects a reader's devices to each other. An ingress provider
connects a stranger to one of them.** A mesh that introduces two peers, or a
zero-trust gateway that lets an enrolled device reach a service, is genuinely
unmetered because no bytes transit the vendor. None of that reaches a reader who
has not enrolled.

The test: does the product publish a public address and port that a stranger can
dial, carrying UDP?

| product | WireGuard data plane | public ingress | free tier | verdict |
| --- | --- | --- | --- | --- |
| NetBird reverse proxy | yes | yes, TCP and UDP L4 | 5 users, 100 machines | `qualifies-with-caveat` |
| Nekotopia nSolo | yes, encrypted mesh | yes, a dedicated public IPv4 | 50 GB/month, then paid | `qualifies-with-caveat` |
| Pangolin | yes | yes, TCP and UDP raw resources | 5 users, 15 resources, but a self-hosted node is required | `paid-only` |
| Firezone | yes | no, gateways are private | free tier exists, no ingress | `fails-egress` |
| Twingate | no, a certificate-pinned TLS tunnel | no | 5 users | `fails-egress` |
| Border0 | yes, an agent | TCP with authentication, no UDP | pricing page 404s | `fails-egress` |
| Netrinos | yes | no, a private mesh | 3 users, 100 devices | `fails-egress` |
| tsocket | no, a TCP tunnel | TCP only | free | `fails-egress` |
| Wiredoor (self-hosted) | yes | yes, TCP and UDP to an approved port | the software is free, the host is not | `paid-only` |
| WirePort (self-hosted) | yes | yes, TCP and UDP L4 | the software is free, the host is not | `paid-only` |
| Netmaker (self-hosted) | yes | no, the vendor guide says deploy your own proxy | 3 users, 10 nodes | `fails-egress` |
| Defguard (self-hosted) | yes, native `.conf` | no | unlimited users, open source | `fails-egress` |
| Innernet (self-hosted) | yes | no | self-hosted | `fails-egress` |
| Headwire (self-hosted) | yes, static peers | no, addresses are private | not published | `fails-egress` |
| OpenZiti / zrok (self-hosted) | no, a libsodium overlay | public shares are HTTP only | self-hosted | `fails-egress` |

## The four that do publish

**NetBird's reverse proxy** puts a TCP or UDP resource on `*.proxy.netbird.io`
with an auto-assigned L4 port, on a free plan of 5 users and 100 machines
(`documented`, read 2026-10-23). The data plane is WireGuard and the private key
never leaves the client machine, so a raw `.conf` cannot reproduce it, but the ingress is
real and it carries UDP.

**Nekotopia nSolo** gives a dedicated public IPv4 over a WireGuard mesh, with a
50 GB monthly cap on the free tiers and 1 TB on Pro (`documented`, read
2026-10-23). 50 GB is 0.05 TiB, so the free tier fails the volume test and the
product is recorded as a paid row with a free sample.

**Pangolin, Wiredoor and WirePort** all publish TCP and UDP from a private
network, and all three require a node the reader runs. The software is free and
the path is not, so they are `paid-only` with a hosting requirement named in the
record, in the same way frp is.

## The tools that are not services

`proxyguard` (MIT, server plus client), `mullvad-udp-over-tcp` (a Rust library
and two binaries), `wgtcp` (a kernel patch) and `wireguard-ws` (a `wireguard-go`
fork with a WebSocket transport) all carry a WireGuard datagram over TCP or
WebSocket. They are recorded with the other transports in
[`wireguard-transports.md`](wireguard-transports.md), and none of them publishes
anything.

## What is dead

- **Firezone as an ingress**: a gateway is reachable by an enrolled device and
  nothing else.
- **OpenZiti and zrok public shares**: HTTP only, at every tier.
- **Twingate as WireGuard**: it is a TLS tunnel and the record says so.
- **Border0**: the pricing page returned 404 after the Tailscale acquisition, so
  the free allowance cannot be read.
- **Netmaker's managed ingress** (self-hosted): the vendor's own guide tells a reader to deploy
  a reverse proxy, which is a self-hosted answer.

## Chaining

**The private chain.** `Tailscale or NetBird -> a reader's own devices`. This is
genuinely unmetered and it is not a serving path.

**The public chain.** `NetBird reverse proxy -> a UDP resource -> a WireGuard
listener`. The scarce link is an unpublished rate on a shared proxy.

## The records

`dossier/egress/netbird-reverse-proxy.json`, `nekotopia-nsolo.json`,
`pangolin.json`, `wiredoor.json`, `wireport.json`, `firezone.json`,
`netmaker.json`, `defguard.json`, `innernet.json`, `twingate.json`,
`openziti.json`, `zrok-hosted.json`, `border0.json`, `netrinos.json`,
`headwire.json`, `metered-tsocket.json`, `proxyguard.json`,
`mullvad-udp-over-tcp.json`, `wgtcp.json`, `wireguard-ws.json`,
`tailscale-personal.json`, `tailscale-funnel.json`, `headscale.json`,
`zerotier-free.json`.

⚠ **Only NetBird's L4 proxy was read as carrying UDP to a public address on a free
tier.** Everything else on this page either publishes nothing or requires a host.
