# What is genuinely unmetered, and why?

⭐ A signalling service introduces two endpoints and then leaves the path. After
hole-punching the provider carries no bytes, so its marginal cost is near zero and
its free tier can be honestly unlimited. This is the only class in the topic where
"unlimited" survives the arithmetic, and the reason is structural rather than
generous.

The distinction has a consequence a reader can act on: a signalling provider's
quota is a count of things rather than a byte count, so it never binds a transfer.
When the provider *does* put bytes on its own relays, as Tailscale Funnel and
iroh's Shared relay do, the quota comes back.

⚠ **A count of users, devices or destinations is not a rate, and the vocabulary has
no kind for it.** A device count has no window, so `request-rate` is the wrong kind
for it. Those entries sit in `limits_note` as unclassified counts, and each record
says so.

Sorted by how much of the ingress need the class serves.

| provider | free tier | what binds | identity | verdict |
| --- | --- | --- | --- | --- |
| Tailscale Personal | 6 users, unlimited user devices | a count of users, which is not one of the seven kinds; no byte limit | email | `qualifies` |
| NetBird | 100 machines | a count of machines; the relay's rate is unpublished | email | `qualifies-with-caveat` |
| ZeroTier | 10 devices, 1 network | a count of devices; the relay's rate is unpublished | email | `qualifies-with-caveat` |
| iroh public relays | 4 regions, no auth | `per-ip-shaping`: an unpublished per-connection rate | anonymous | `qualifies-with-caveat` |
| Cloudflare WARP | no published cap | unstated | email | `qualifies-with-caveat` |
| Tailscale Funnel | public HTTPS on a *.ts.net name | `per-ip-shaping`: non-configurable, unpublished | email | `fails-quota` |
| iroh Shared relay | 100 GB/month | `per-ip-shaping`: the 100 GB/month allowance | email | `fails-quota` |
| Headscale (self-hosted) | BSD-3, no node cap, self-hosted | `volume-quota`: the host's egress allowance | anonymous | `paid-only` |

## Tailscale Personal

6 users, unlimited user devices, 3 ACL groups and 50 tagged resources, with 1,000
ephemeral node-minutes a month (`documented`, 2026-10-22). Bytes do not appear in
the limits because in the normal case they do not transit: peers negotiate a
direct WireGuard path.

The free tier is genuinely unlimited in volume for that reason, and the caps that
exist are counts of things.

⭐ **The direct path was measured on this host.** The Tailscale client 1.102.4 runs
on a live tailnet, and `tailscale ping` to a peer answered `pong from
a peer (its tailnet address) via a LAN address on port 41641 in 100ms`
(`measured`, 2026-10-22). The `via` clause names a LAN endpoint rather than a DERP
region, so the two peers held a direct path. That is the signalling claim confirmed
at the only place it can be: the control plane introduced them and the bytes did not
cross Tailscale's relays.

DERP relays carry bytes when hole-punching fails. That is the case where the bytes
do transit and it was not measured.

Evidence: `tailscale.com/pricing` (read 2026-10-22); probe record in
`dossier/egress/tailscale-personal.json`.

Verdict: `qualifies`. The Funnel product, which does put bytes on Tailscale's
relays, is recorded separately and fails.

## Headscale

A BSD-3 control server for Tailscale clients, self-hosted, with no node cap
(`documented`, 2026-10-22). It replaces the coordination service and nothing else,
so the byte path is unchanged and the constraint is the server's uptime.

Evidence: `github.com/juanfont/headscale` (read 2026-10-22);
`dossier/egress/headscale.json`.

Verdict: `paid-only`. The control plane sees no payload and the software is free.
The path is not free, because it needs a host, and the host is a separate provider.
No probe: a control server was not stood up.

## NetBird

100 machines plus 10 per user on the cloud plan, with direct WireGuard paths and
the vendor's relay as a fallback (`documented`, 2026-10-22). Self-hosting
removes the machine cap.

The relay's rate is not published, so the fallback path has no number.

Evidence: `netbird.io/pricing` (read 2026-10-22); `dossier/egress/netbird-free.json`.

Verdict: `qualifies-with-caveat`.

## ZeroTier

10 devices, 1 network and 1 administrator on the free plan (`documented`,
2026-10-22). The cap is devices, not bytes, and a relay fallback exists at an
unpublished rate.

Evidence: `zerotier.com/pricing/` (read 2026-10-22);
`dossier/egress/zerotier-free.json`.

Verdict: `qualifies-with-caveat`. Ten devices is enough for a reader's own
machines and is not a capacity number.

## iroh public relays

Four public regions, no authentication, and a per-connection rate limit that is
deliberately unpublished: "The exact rate limits aren't published today, as they
get tuned as needed" (`documented`, 2026-10-22). The same page says not to rely on
the public relays for production: "This means that public infrastructure is meant
for development and hobby use. Do not rely on it for production workloads,
especially if your application is sensitive to rate limiting, uptime, or relay
software version."

This is a relay that transits bytes and meters rate rather than volume, so its
free tier is real in the sense that no byte counter stops it, and unusable as a
plan because no number exists and the vendor says not to depend on it.

Evidence: `docs.iroh.computer/relays/rate-limiting` (read 2026-10-22);
`dossier/egress/iroh-public-relay.json`.

Verdict: `qualifies-with-caveat`, and the caveat is the vendor's own sentence: a
redundancy layer, not a capacity layer. A plan cannot name a throughput for it, so
it belongs in no serving chain.

## Cloudflare WARP (consumer)

Free, with no published data cap and no published rate (`documented`,
2026-10-22). It gives a device a new exit and does not give a server one, which is
the wrong shape for the serving workload this topic measures.

A community report describes about 1.8 MB/s on WARP to a home tunnel; it was not
reproduced.

Evidence: `developers.cloudflare.com/warp-client/` (read 2026-10-22);
`dossier/egress/cloudflare-warp.json`.

Verdict: `qualifies-with-caveat`. Nothing here can be planned against.

## Tailscale Funnel

The product that puts bytes on Tailscale's relays, and the quota comes back with
it: "Traffic sent over a Funnel is subject to non-configurable bandwidth limits",
on ports 443, 8443 and 10000 only (`documented`, 2026-10-22).

Evidence: `tailscale.com/kb/1223/funnel` (read 2026-10-22);
`dossier/egress/tailscale-funnel.json`.

Verdict: `fails-quota`. The contrast with Tailscale Personal is the whole point of
this document: the same vendor is honestly unlimited when it signals and
discretionary when it relays.

## iroh Shared relay

100 GB of relay egress per month, 10,000 concurrent connections and a 5 MB/s rate
limit, then USD 0.09/GB (`documented`, 2026-10-22). 100 GB/month is 3.3 GB/day.

Evidence: `docs.iroh.computer/iroh-services/relays/shared` (read 2026-10-22);
`dossier/egress/iroh-shared-relay.json`.

Verdict: `fails-quota`.

## What did not work

- **Tailscale Funnel**: an unpublished, non-configurable throttle. `fails-quota`.
- **iroh Shared relay**: 100 GB/month. `fails-quota`.
- **libp2p circuit-relay v2**: 128 KiB per direction per circuit by default, so a
  relayed connection is a handshake carrier and not a transport. `fails-quota`.
- **Cloudflare TURN**: 1,000 GB/month is 3.03% of one day. `fails-quota`.
- **Cloudflare WARP as an egress multiplier**: no published cap and no published
  rate, and the consumer client is a device VPN that gives a device a new exit
  rather than a server one.
- **ZeroTier beyond 10 devices**: the cap is a device count, so a mesh of 30
  machines is a paid plan.

## Chaining

**The signalling chain.** `Tailscale or Headscale for the mesh -> a named
Cloudflare Tunnel for the one service that must be public`. The scarce link is the
domain the tunnel needs. The mesh carries private traffic for nothing and the tunnel
carries the public traffic.

⚠ **The mesh in that chain is signalling and the tunnel is transit.** They are not
substitutes for each other. A reader who reads "mesh for nothing" as a serving
answer has made the error this document exists to prevent.

**The relay-when-it-fails chain.** `iroh direct path -> iroh public relay for the 7 to
10% that do not hole-punch`. The scarce link is the unpublished rate and the vendor's
own warning against production use. The fallback share is 7 to 10% from iroh's published
figure (`reported`), and at this volume that is 70 to 100 GB/day. On n0's paid relay at
USD 0.09/GB the month is USD 180 to 270, which is 2.1 to 3.0 TB over 30 days. The
self-hosted `iroh-relay` ships with rate limiting off, which is the only configuration
with no per-gigabyte term.

⚠ **The cost figure is arithmetic on a reported share, not a measurement.** The
fallback rate was not measured; it is the vendor's figure. Two of the three numbers
in that sentence are `documented` and the share is `reported`.
