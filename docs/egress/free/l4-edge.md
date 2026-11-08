# L4 edge proxies: the free Spectrum class

Cloudflare Spectrum forwards arbitrary TCP and UDP from an anycast address to an
origin, and it is Enterprise-only. This page is every other edge network that
does the same, plus the game proxies that sell the same thing to a narrower
audience.

⭐ **One row in this class gives it away: TCPShield Sentry Tunnel, at 1.0 TB per
month on a free plan.** Every other vendor charges, and the reason is structural:
a UDP datagram carries no hostname, so each customer needs an address rather than
a shared edge. One vendor states it plainly, and that sentence is the finding of
this page.

| provider | what it forwards | free tier | UDP | identity | verdict |
| --- | --- | --- | --- | --- | --- |
| TCPShield Sentry | any TCP or UDP over VXLAN | 1.0 TB/month (0.909 TiB) | yes | email | `qualifies-with-caveat` |
| Gcore Edge Proxy | any TCP or UDP to an origin | a 2-day trial, then EUR 17/month | yes | card | `trial-only` |
| Cosmic Guard | any UDP port | a trial, then USD 0.03/player/day | yes | card | `trial-only` |
| 1DUN | all ports on a scrubbed address | a trial, then USD 149/month | yes | card | `trial-only` |
| Tencent EdgeOne | L4 proxy on the paid plan | 50 GB/month on free, HTTP only | paid | card | `paid-only` |
| Alibaba Anti-DDoS | 100 Mbit/s of clean traffic | none | yes | card | `paid-only` |
| AWS Global Accelerator | any TCP or UDP, any port | none | yes | card | `paid-only` |
| Google passthrough NLB | any TCP or UDP | none | yes | card | `paid-only` |
| Cloudflare Spectrum | any TCP or UDP | Enterprise only | yes | card | `paid-only` |
| Imperva, Akamai Prolexic | scrubbed L4 | none published | yes | card | `paid-only` |
| Fastly, bunny.net, Azure Front Door | HTTP only | 100 GB/month at Fastly | no | email | `fails-egress` |

## TCPShield Sentry Tunnel

The documented number in this class: the free plan carries "1.0 TB monthly bandwidth",
one network and three domains, and the Sentry tunnel forwards any TCP or UDP over VXLAN
from a scrubbing edge to a host the reader runs (`inferred`, read 2026-10-23).

⚠ **The rung is `inferred` and the gap is precise.** The pricing page states the
byte allowance for the base plan. No page states that Sentry is included in it,
and the FAQ names a Premium gate for Bedrock in the same paragraph. One free
signup would settle it.

The origin side is a Linux host with root, because the panel generates a shell script
that creates a VXLAN interface. That host is a separate machine, so this row composes
with the free VM lane rather than replacing it.

1.0 TB/month is 0.909 TiB, which is 9% short of the test, and no page says what
happens when it is crossed.

Evidence: `tcpshield.com/pricing` (read 2026-10-23);
`dossier/egress/tcpshield.json`.

## Gcore Edge Proxy

Any TCP or UDP service behind a scrubbing edge, at EUR 17/month after a 2-day
trial (`documented`, read 2026-10-23). It is the clearest paid Spectrum
alternative in the list: the origin can be an address or a domain, and the
protocol is not restricted to a game.

At 1 TiB/month the price is flat rather than metered, which makes it the cheapest
managed L4 edge found for a steady terabyte. The trial is 2 days, so it is not a
free tier.

Evidence: `gcore.com/security/edge-proxy` (read 2026-10-23);
`dossier/egress/gcore-edge-proxy.json`.

## Cosmic Guard and 1DUN

Both sell a scrubbed address with all ports open. Cosmic charges USD 0.03 per
player per day, which is a game-shaped price; 1DUN starts at USD 149/month for
one address and ten forwarding rules (`documented`, read 2026-10-23).

Neither has a free tier. Both are recorded because they are what the class costs
when a vendor prices an address rather than a hostname.

## The hyperscaler L4 products

AWS Global Accelerator charges USD 0.025 per hour plus USD 0.015 per GB, with no
cap (`documented`, read 2026-10-23). One TiB is about USD 18 a month in fixed
cost and USD 15 in transfer, so about USD 33. Google's passthrough network load
balancer bills a forwarding rule hourly plus egress at the standard rate. Azure
Front Door has no UDP at all.

⚠ **None of these is a free path, and all of them are cheaper than Cloudflare
Spectrum's entry price.** The comparison is worth keeping because Spectrum is what
a reader arrives looking for.

## The game proxies that do not carry an arbitrary service

MineGuard offers 1 TB/month and a Java-only connection. NeoProtect's free Basic
tier is Minecraft Java only. Infinity-Filter excludes Bedrock from the free plan.
FloodGuard puts Bedrock on a Pro card. Arvoris and MineKube Connect are Java TCP.

⛔ **A vendor that only protects a named game protocol fails the ingress test for
an arbitrary service**, whatever its traffic allowance. The record keeps the
number and the sentence that limits it, because the number is what a reader will
find first.

## What is dead

- **Cloudflare Spectrum as a free path**: Enterprise only, at every protocol.
- **Azure Front Door as an L4 edge**: HTTP only.
- **bunny.net as a UDP edge**: no UDP at any price, at either tier.
- **Tencent EdgeOne's free L4**: the free 50 GB is HTTP; L4 is a paid feature.
- **Path.net**: third-party pages disagree by two orders of magnitude on the
  price, so the record is `unverified` and no number is printed.

## Chaining

**The free chain.** `TCPShield Sentry -> VXLAN -> a Linux host with root -> a
WireGuard listener inside the tunnel`. The scarce link is the root host, which is
the free VM lane, not this one.

**The paid chain.** `Gcore Edge Proxy -> an origin address -> every port and
protocol`. The scarce link is EUR 17/month, and nothing else in the chain is
metered.

## The records

`dossier/egress/tcpshield.json`, `gcore-edge-proxy.json`, `cosmic-guard.json`,
`1dun.json`, `tencent-edgeone-l4-proxy.json`, `alibaba-anti-ddos-proxy.json`,
`aws-global-accelerator.json`, `gcp-passthrough-nlb.json`,
`cloudflare-spectrum.json`, `imperva-ddos.json`, `akamai-prolexic.json`,
`fastly-free.json`, `bunny-net.json`, `azure-front-door.json`,
`azure-ddos-protection.json`, `path-net.json`, `mineguard.json`,
`neoprotect.json`, `infinity-filter.json`, `floodguard.json`, `arvoris.json`,
`minekube-connect.json`, `turtleguard.json`.

⚠ **No L4 edge here was measured.** The two rows that would change with one
signup are TCPShield, which would become `documented`, and Gcore, whose 2-day
trial would show whether the origin can be an arbitrary address.
