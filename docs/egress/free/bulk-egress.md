# Which free path actually moves 500 GB to 1 TiB in a day?

Two lanes, and neither is a relay. One is an object host with no bandwidth limit
and a per-object cap. The other is a CDN pair whose egress is unmetered and whose
origin storage is the thing that limits it.

⭐ GitHub Releases measured 14.11 MiB/s at four connections, which is 1.16 TiB/day,
and what binds is the 2 GiB asset size rather than the volume.

⚠ **A volunteer relay does not carry this traffic.** Yggdrasil has no exit nodes, so a
200 Mbit/s peer is 2.16 TB per day between two Yggdrasil nodes and not between an origin
and a reader. The arithmetic is right and the subject is wrong. See §Yggdrasil public
peers below, and the history entry at
[`history/2026-10-22T052900Z`](../../../history/2026-10-22T052900Z/yggdrasil-has-no-exit-nodes.md).

Everything centrally operated that transits bytes to the public internet is
metered, and every metered allowance found is two to three orders of magnitude
short of the floor.

Sorted by measured daily capacity, largest first.

| provider | free tier | what binds | identity | verdict |
| --- | --- | --- | --- | --- |
| GitHub Releases | no bandwidth limit, 2 GiB per asset | `per-object-cap`: 2 GiB per asset | email | `qualifies` |
| Cloudflare Tunnel (named) | unmetered transit, 1,000 tunnels | `write-gated`: a domain on Cloudflare nameservers | email | `qualifies-with-caveat` |
| Cloudflare Pages | unlimited static requests | `per-object-cap`: 25 MiB per asset | email | `qualifies-with-caveat` |
| Oracle Cloud Always Free | 10 TB/month out | `per-ip-shaping`: the 10 TB/month allowance | card | `qualifies-with-caveat` |
| Cloudflare R2 | egress free, 10 GB stored | none on egress; the 10 GB storage volume | email | `qualifies-with-caveat` |
| playit.gg | no published cap | `per-ip-shaping`: an unpublished tolerance | email | `qualifies-with-caveat` |
| Cloudflare TURN | 1,000 GB/month | `per-ip-shaping`: the 1,000 GB/month allowance | email | `fails-quota` |
| Fastly | 100 GB/month | `per-ip-shaping`: the 100 GB/month allowance | email | `fails-quota` |
| Vercel Hobby | 100 GB/month | `per-ip-shaping`: the 100 GB/month allowance | email | `fails-quota` |

## The constraint kind for a byte allowance

⚠ **A monthly byte quota is not a rate, and the table needs the right kind for it.**
A byte allowance over a period, counted per account, is the constraint that decides
four rows above. `per-object-cap` is an object size, `request-rate` bounds calls, and
`per-ip-shaping` bounds a volume but attaches it to the caller's address rather than
to an account.

The constraint vocabulary names the kind `volume-quota`: a byte allowance over a
period, counted per account rather than per caller. The number itself lives in
`egress.free_allowance`, and a record that names `per-ip-shaping` for a byte allowance
carries a `binding_note` that says why.

## GitHub Releases

No bandwidth limit and no total size limit; under 2 GiB per asset and 1,000
assets per release (`documented`, 2026-10-22). Each download redirects to a signed
`release-assets.githubusercontent.com` URL that honours `Range` (`measured`,
2026-10-22).

Measured on a 40,227,721-byte asset: one connection at 6.72 MiB/s, four
connections with a freshly minted URL each at 14.11 MiB/s (`measured`,
2026-10-22). 14.11 MiB/s is 1.16 TiB/day, which clears the floor on one account.
A control download from `proof.ovh.net` on the same machine at the same time
reached 29.5 MiB/s, so this is not the machine's ceiling.

The 2 GiB cap sets the shard size. An archive of 20 TiB is 10,240 assets of 2 GiB,
which is ten releases of 1,000.

Evidence: `docs.github.com/en/repositories/releasing-projects-on-github/about-releases`
(read 2026-10-22); probe records in `dossier/egress/github-releases-cdn.json`.

Verdict: `qualifies`. The only hosted free path **measured** above the serving
floor, and it binds on object size rather than volume. Cloudflare Tunnel and Oracle
both claim more and neither was measured, so the claim is scoped to the rung and
not to the market.

## Yggdrasil public peers

A peer-to-peer overlay where a node peers with volunteers listed in a public
directory. The protocol has no byte meter, so the ceiling is the link rate the peer
advertises. One peer at 200 Mbit/s is 2.16 TB/day, or 1.96 TiB/day.

⛔ **That capacity is between two Yggdrasil nodes and it is not a path to a
reader.** Yggdrasil's own about page states: "Yggdrasil has no native exit nodes,
nor does it have any concept of exit nodes, for providing access to the public
Internet or to other networks. This can be achieved using proxies or other
tunnelling solutions on top of Yggdrasil but this is not something we explicitly
aim to provide" (`documented`, 2026-10-22). The FAQ confirms the network transports
only IPv6 internally and routes inside the deprecated `0200::/7` range.

The workload this topic measures is 500 GB to 1 TiB of HTTP serving to the public each
day. No part of that traffic can traverse a Yggdrasil peer, because the peer belongs to an
overlay that does not reach the public internet. A reader who chose this row for
serving would have chosen it for a capability it does not have.

**What Yggdrasil is good for.** A private mesh between a reader's own machines.
Every node is a router, a node behind NAT becomes reachable once it peers, and
addresses are derived from a cryptographic key so they follow the machine. A node
reaches another node's `0200::/7` address with no port forward and no public
address, and the network is genuinely unmetered because no byte meter exists. That
is real and it is worth having for a control plane.

**What it is not.** A way to reach the public web, a CDN, or a serving path. Putting
a proxy or a tunnel on top of it does not change which network carries the last
mile, and the project says it does not aim to provide that.

The directory states the rates. Entries read "up to 1000 Mbps", "100 Mbit/s",
"1Gbit/s" and "400 Mbit/s" in one national file (`documented`, 2026-10-22). Three of
four sampled peers accepted a TCP connection from this host; the fourth, an Oracle
Ashburn node, timed out (`measured`, 2026-10-22). Throughput was not measured, and
a throughput figure would describe overlay capacity rather than egress.

An Oracle Always Free node is the case to check: its directory entry reads "Oracle
Cloud VPS(Always Free Tier, 480Mbps, **Metered**)" (`documented`, 2026-10-22), because
Oracle's 10 TB/month quota sits behind it. The 200 Mbit/s used for the arithmetic above
is a baseline and not this node's advertised rate. It is the one case in the network
where a byte quota applies.

Evidence: `yggdrasil-network.github.io/about.html` and `.../faq.html` (read
2026-10-22); `github.com/yggdrasil-network/public-peers` and the national files
under it; probe record in `dossier/egress/yggdrasil-public-peers.json`.

Verdict: `fails-egress`. The network carries bytes and carries none of them to the
public internet.

⚠ **The same category error, checked for elsewhere in this topic.** Every record
carries `extras.bytes_transit`. Three never transit anything: Yggdrasil, Headscale
and serveo. Three transit only when a direct path fails: Tailscale Personal,
NetBird and ZeroTier. Two transit only the host they run on: `frp` and
`zrok-selfhost`, which are software rather than services. The remaining thirty
relay to the public internet. No other record claims a transit path that does not
exist.

## Cloudflare Tunnel (named)

Unmetered on every plan: the account limits page lists 1,000 tunnels, 25 replicas
per tunnel and 50,000 routes, and no bandwidth figure at all (`documented`,
2026-10-22). That is a documented absence and not a quota, and it is not
multiplied here.

What fails rather than shapes is the 100 MB proxied request body on Free and the
125 s proxy read timeout (`documented`, 2026-10-22). A read path under those two
numbers is not bounded by volume at all, which is why this row belongs in this
table at a size no other hosted row reaches.

Evidence: `developers.cloudflare.com/cloudflare-one/account-limits/` and
`.../fundamentals/reference/connection-limits/` (read 2026-10-22);
`dossier/egress/cloudflare-tunnel.json`.

Verdict: `qualifies-with-caveat`, and the caveat is the domain rather than the
volume. Not measured.

## Cloudflare Pages

Static asset requests are free and unlimited, and a static asset is capped at
25 MiB (`documented`, 2026-10-22). The Functions invocation count is the other
number and it only applies when a Function runs, so a pure static deployment does
not touch it.

This record owns the egress term. The storage arithmetic belongs to the storage
topic, which states 488 GiB across 100 projects. For egress the finding is narrow:
static bytes are not counted, whatever their volume.

Evidence: `developers.cloudflare.com/pages/platform/limits/` (read 2026-10-22);
`dossier/egress/cloudflare-pages-egress.json`.

Verdict: `qualifies-with-caveat`. 25 MiB per object is the shard size and the
build is a write gate.

## Oracle Cloud Always Free

10 TB/month of outbound transfer is free in every region band, then metered
(`documented`, 2026-10-22). That is 333 GB/day, a third of the floor this topic measures.

The free shape's internet bandwidth is 50 Mbps on its single VNIC, and 480 Mbps
applies only to private and in-region endpoints (`documented`, 2026-10-22). The
arithmetic matters: 50 Mbit/s sustained is 540 GB/day, so the 10 TB/month quota binds first
and the rate never has to be shaped against. Two regions double the quota to
666 GB/day and still leave it binding.

Idle instances are reclaimed after 7 days of low CPU, network and memory traffic,
so a machine that only serves files can be taken. A card is required at signup.

Evidence: `oracle.com/cloud/networking/pricing/` (read 2026-10-22);
`docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm`
(read 2026-10-22) for the 50 Mbps line and the reclamation rule;
`dossier/egress/oracle-always-free.json`.

Verdict: `qualifies-with-caveat`. Not probed: an Always Free account needs a card.

## Cloudflare R2

Egress to the internet is free on every plan, unconditionally, and the free tier
is 10 GB-month of storage with 1M Class A and 10M Class B operations per month
(`documented`, 2026-10-22).

Zero egress is the most valuable single term in this topic. The storage is what
limits a deployment and the egress is not limited at all: 10 GB is 0.1% of the hot
working set, and the chain that matters is R2 as the origin behind a free
Cloudflare front, where the 10 GB stays and the bill does not appear.

⚠ **A storage volume is not a per-object cap.** The 10 GB-month is recorded in
`limits_note` rather than forced into a kind that does not fit, and `binding` is
`none` because nothing binds the egress.

Evidence: `developers.cloudflare.com/r2/pricing/` (read 2026-10-22, page updated
2026-10-01); `dossier/egress/cloudflare-r2.json`.

Verdict: `qualifies-with-caveat`, on the storage rather than the egress.

## playit.gg

The only centrally operated relay found with no published cap, and its operator
described 1-2 TB/day on a free account as tolerated in a forum post on 2026-05-28
(`reported`). Generic TCP moved to the paid tier; free ports are game presets and
UDP (`documented`, 2026-10-22).

Evidence: `discuss.playit.gg/t/traffic-limits/5574` (read 2026-10-22);
`dossier/egress/playit-gg.json`.

Verdict: `qualifies-with-caveat`. A tolerance is not a quota, and the same post
says the tolerance moves with regional bandwidth cost.

## Cloudflare TURN

1,000 GB/month of Realtime egress, shared with the SFU, then USD 0.05/GB
(`documented`, 2026-10-22, page updated 2026-09-22). 1,000 GB/month is 33.3 GB/day,
3.03% of one day.

A byte quota relayed does not compound, so it cannot be wrapped into more.
Reaching 1 TiB/day would need about 30 accounts at the free allowance, which is
not a plan.

Evidence: `developers.cloudflare.com/realtime/sfu/platform/pricing/` (read
2026-10-22); `dossier/egress/cloudflare-turn.json`.

Verdict: `fails-quota`. Useful only as a NAT-traversal fallback for a
WebRTC-shaped workload.

## Fastly and Vercel

Both give 100 GB/month, which is 3.3 GB/day and 0.30% of one day
(`documented`, 2026-10-22 each). Fastly meters per region, so a multi-region
service spends the allowance several ways. Vercel holds excess rather than billing
it.

Evidence: `fastly.com/pricing` and `vercel.com/docs/plans/hobby` (read
2026-10-22); records `dossier/egress/fastly-free.json` and
`dossier/egress/vercel-hobby.json`, both `documented` and both `fails-quota`.

Verdict: `fails-quota` for both.

## What did not work

- **Yggdrasil public peers as a serving path**: no exit nodes, so no peer reaches
  the public internet. `fails-egress`.
- **Cloudflare TURN**: a byte quota at 3.03% of one day. `fails-quota`.
- **Fastly**: 100 GB/month. `fails-quota`.
- **Vercel Hobby**: 100 GB/month. `fails-quota`.
- **iroh Shared relay**: 100 GB/month, 3.3 GB/day. `fails-quota`.
- **ngrok**: 1 GB/month, which is 33.3 MB/day or 31.8 MiB/day. `fails-quota`.
- **zrok hosted**: 5 GB/day. `fails-quota`.
- **libp2p circuit-relay v2**: 128 KiB per direction per circuit by default, so a
  1 GiB object needs 8,192 relayed connections and 1 TiB needs 8.4 million.
  Architecturally excluded from bulk rather than slow. `fails-quota`. Record
  `dossier/egress/libp2p-circuit-relay-v2.json`: `documented`, `fails-quota`,
  binding `per-object-cap` at 128 KiB per direction.

  ⚠ **The per-direction qualifier comes from go-libp2p and the value from
  js-libp2p.** go-libp2p's `Data` field comment reads "The limit of data relayed (on
  each direction) before resetting the connection", with `Data: 1 << 17` in the
  default `Resources` literal. js-libp2p defines `DEFAULT_DATA_LIMIT = 1 << 17`
  with the comment "128k is the default data limit" and no per-direction language.
  Both are cited. The difference matters because a limit on one direction halves the
  object count a circuit can carry against a limit on the circuit.
- **jsDelivr**: serves npm and GitHub package content only, and the policy page
  that would state the per-file limit returns 404. `fails-quota`.
- **Consumer-connection and mobile proxies**: USD 0.80/GB at the cheapest rate
  seen, which is USD 880 for one day at two significant figures. `fails-quota`.
  The rate is `reported` from one vendor page, and a census figure of USD 819/day
  computed on 1,024 GiB also exists; the gap is the decimal-versus-binary
  difference and not a disagreement about the rate.
- **Free static IPv4**: none exists. Every result was USD 2 to 15 per month, and
  the free equivalent is an IPv6 /48 plus a dual-stack front, which is a different
  shape and works only for clients that have IPv6.

## Chaining

**The object chain.** `GitHub Releases as the byte store -> a ranged fetcher with a
manifest`. The scarce link is the 2 GiB asset cap, which sets the shard size. This
chain clears the floor on one account and needs no domain and no card. It is the
only chain in the topic that was measured end to end.

**The front chain.** `R2 as origin -> a Cloudflare front for the read path`. The
scarce link is R2's 10 GB of storage. Egress is free on both halves, so the volume
is unbounded and the corpus that fits in 10 GB is the whole answer.

**The quota chain.** `Oracle Always Free VM -> a direct IPv6 path`. The scarce link
is Oracle's 10 TB/month at 333 GB/day, so the 50 Mbit/s never has to be shaped
against. Two regions double the quota and still leave it binding. This chain
approaches the floor this topic measures and falls short by two thirds without
probing.

⚠ **Two chains were checked and rejected.** `Cloudflare TURN plus free STUN` as a
bulk relay: TURN's 1,000 GB is a byte quota and cannot be wrapped into more, and
the 33.3 GB/day it yields is 3.03% of demand. `Oracle VM -> Yggdrasil peer` as a
serving path: the second half does not reach the public internet, so the chain ends
inside an overlay.

**The private-mesh chain, which is not a serving chain.** `Yggdrasil peer -> a node
behind NAT -> its 0200::/7 address`. The scarce link is a volunteer's willingness.
This carries private traffic between a reader's own machines and none of it to the
public.
