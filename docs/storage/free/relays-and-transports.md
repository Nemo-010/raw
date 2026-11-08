# Relays and transports: which one moves bytes and which one only signals

Three very different mechanisms are filed together here, and the distinction that
separates them decides whether any of it is storage. **Signalling** is a relay that coordinates
a connection and carries no bytes. **Relaying** is a relay that carries the bytes. A
**transport** is a protocol with no store behind it at all.

This document covers 13 qualifying records: the Blossom and Nostr file servers, the
iroh transports and discovery services, the weird transports that turn a game platform into a
store, and the contributed-infrastructure networks. 40 were rejected, and the largest
group is the relay networks, because a relay that meters bytes is a very expensive transfer
service.

## The comparison

Sorted by whether the mechanism stores, relays or merely signals.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Filecoin Onchain Cloud (FWSS / Filecoin Pay) | $2.50/TiB/month per copy, plus $0.12 per data-set/month proving fee... | - | card | qualifies-with-caveat |
| Proxyrack Unlimited Residential (per-thread... | unmetered bytes; the limit is concurrency. 100 threads = $150/mo ($1.50/thread)... | per-ip-shaping: 12.7 MB/s for 1 TiB/day, which requires | card | qualifies-with-caveat |
| Sia Storage App (sia.storage) | Free 50 GB; Plus $7.99/mo for 500 GB; Pro $14.99/mo for 5 TB... | - | email | qualifies-with-caveat |
| Blossom server fleet (24242.io... | 24242.io 100 MiB/file, deleted if not accessed for 60 days. blossom.oslim.dev... | per-object-cap: 100 MiB on most servers (20 MiB on nostr | anonymous | qualifies |
| nostr.download (route96 Blossom server) | 10.00 GB per file (hard cap, read off the server's own TOS page)... | per-object-cap: 10 GB | anonymous | qualifies |
| nostrmedia.com (NIP-96 file host) | free plan max_byte_size 26,214,400 (25 MiB)... | per-object-cap: 25 MiB free | anonymous | qualifies-with-caveat |
| SourceForge File Release System (FRS)... | No fixed quota. SourceForge's own docs: 'There are currently no fixed capacity limits... | per-object-cap: 10 GB per file, 'Individual files larger than 10 GB will not... | - | qualifies-with-caveat |
| SourceForge Project Web (<project>.sourceforge.io) | No quota stated anywhere on the page, the docs grant each project a vhost and say... | - | - | qualifies-with-caveat |
| Modrinth | 500 MiB per version file (hard code-level cap: `read_from_field(field, 500 * (1 << 20)... | per-object-cap: maximum of 500MiB | - | qualifies-with-caveat |
| Roblox Open Cloud Assets | Per-asset caps only, no aggregate quota: 20 MB for most asset types... | per-object-cap: 20 MB/asset | - | qualifies-with-caveat |
| Thunderstore | 5,242,880,000 bytes (~5 GB) per package zip... | write-gated: moderation queue | - | qualifies-with-caveat |
| iroh Services, Community (free tier) | 0 bytes of storage. Free plan = public relays in US/EU/Singapore... | - | email | fails-egress |
| iroh Mainline-DHT content discovery... (self-hosted) | No quota, no storage. Pure discovery: publishes BLAKE3->provider mappings onto the... | - | anonymous | qualifies |

## What the class is

The distinction is architectural and it has a measurable consequence.

**Signalling is nearly free to operate**, because the data goes peer to peer after
hole-punching. iroh's hole-punch success rate is about 90 to 93%, and the 7 to 10% that falls
back is the part that costs money.

**Relaying is metered, always.** A relay carries real bytes, so a free tier on it is a small
allowance. Cloudflare Realtime TURN gives 1,000 GB per month, which is 33 GB per day, which is
3% of one day's workload. That is about 30 accounts for one day.

**A volunteer relay meters rate rather than bytes, and that is why it wins.** One Yggdrasil
peer advertising 200 Mbit/s moves 2.16 TB per day if it sustains, which is 1.96 TiB, with no
quota at all. A rate cap does not bound a day's volume; a byte quota does. The figure
"2.16 TiB per day" mixes decimal and binary: 200 Mbit/s is 2.16 TB
and 1.96 TiB, and the conclusion does not change but the unit does.

## iroh: an excellent transport, irrelevant as storage

`iroh-blobs` is real: BLAKE3-verified streaming
over QUIC, a provider and requester model, no upper size limit for blobs, and about 6%
outboard overhead.

The bytes stay on the local disk. n0 sells no storage or pinning at all; every paid row in
its pricing table is connections, relay egress, metrics or support. Its community tier gives
zero bytes of storage, public relays in three regions, seven days of metrics retention and
rate-limited traffic with no uptime guarantee.

Two consequences follow, and the second is the one that rules it out as a serving tier.
`iroh-blobs` is a QUIC ALPN, so Cloudflare cannot cache it. Getting HTTP means running
`iroh-gateway`, which is a second copy of the bytes.

The relay arithmetic is the finding: the fallback path is 70 to 100 GB per day, or 2 to 3 TB
per month, which on n0's paid relay costs roughly USD 190 to 270 per month, about ten times
the storage cost. Self-hosting `iroh-relay`, with rate limiting off by default, is the only
zero-per-gigabyte configuration.

## Blossom: the zero-identity path with content addressing

The Blossom protocol is the most interesting finding in this document, and it works because
the credential is a keypair rather than an account.

Authentication is a self-signed Nostr event, so a fresh keypair is a fresh namespace with no
signup. A `PUT` without a signature returns 401, which is the expected shape rather than a
wall. `/mirror` replication is built into the protocol, so a blob can be copied between
servers by identifier.

The fleet is what makes it usable: four servers with different caps. `24242.io` takes 100 MiB
per file and deletes after 60 days without access. `blossom.oslim.dev` takes 100 MB per file
with 8 GB per public key and claims permanent retention. `nostr.download`, running route96,
takes 10 GB per file with no published per-user total and no inactivity deletion.

`nostrmedia.com` is the NIP-96 alternative: 25 MiB on the free plan, 100 MiB on paid, with
`file_expiration: [0,0]` on every plan, which means never.

The pattern is the same zero-identity shape as BigFile.net, with content addressing and
replication added. It is the strongest anonymous finding in the whole corpus.

## The weird transports, which are real

Four records here turn a platform into a store, and each is a genuine finding rather than a
curiosity.

Roblox Open Cloud accepts assets with per-type caps: 20 MB for most types and up to 3.75 GB
for video, with 20 video uploads per day for ID-verified accounts. Thunderstore accepts
5,242,880,000 bytes per package zip, documented as a soft limit. Modrinth caps a version file
at 500 MiB in code, which is a hard limit with a readable error message. SourceForge's FRS has
no fixed capacity limit at all and is mirrored.

## The contributed-infrastructure networks

Three records are networks where contributing capacity is supposed to earn capacity, and the
arithmetic refutes the idea.

Sia pays a host USD 1.17 per TB per month and charges a renter USD 2 to 3, a ratio of about
2.6. Storj pays USD 1.35 and charges USD 7, a ratio of 5.2. Both pay cash or token and never
storage credit, so funding a 20 TiB rental would need about 52 TB of contributed disk at Sia's
rate and about 259 TB at Storj's with erasure coding. Contributing hardware is a business, not
a discount.

Filecoin Onchain Cloud is the cheapest storage in this topic and it is disqualified by its own
egress term. Storage is USD 2.50 per TiB per month, and egress is up to USD 14 per TiB through
Filecoin Beam. At 1 TiB per day the CDN bill is about USD 420 per month, which makes the total
about USD 520. It is the cleanest illustration of the topic's central rule.

Filecoin Plus died on 2026-10-19 with the Solstice upgrade, FIP-0118: "No new datacap is
minted; all minting and allocation methods are disabled." Fil+ was the mechanism that made
Filecoin storage free. A provider that was free last week is not free
this week. The record is
`dossier/storage/filecoin-plus-datacap-free-storage.json`; its `verdict` is `fails-quota` and its
identity cost was `institution`, because an allocator had to be petitioned before a byte moved.
Proof: the sector's 10x quality-adjusted power that made an SP accept free data now applies to
every new sector whether the data is vetted or not, so the subsidy has no object left.

### Filecoin Onchain Cloud (FWSS / Filecoin Pay)

> $2.50/TiB/month per copy, plus $0.12 per data-set/month proving fee. 20 TiB = $50/mo per copy; two copies = $100/mo

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Requires a funded stablecoin wallet.

Evidence: `https://docs.filecoin.cloud/cookbooks/payments-and-storage/` (2026-10-21), record `dossier/storage/filecoin-onchain-cloud.json`.
Verdict: `qualifies-with-caveat`.

### Proxyrack Unlimited Residential (per-thread, unmetered)

> unmetered bytes; the limit is concurrency. 100 threads = $150/mo ($1.50/thread); 500 = $750/mo; 1,000 = $1,250/mo ($1.25); 2,000 = $2,000/mo ($1.00); 5,000 = $4,500/mo ($0.90)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 12.7 MB/s for 1 TiB/day, which requires. A new account costs card. Observed behaviour: Exit nodes are consumer connections that go offline without notice.

Evidence: `https://www.proxyrack.com/pricing/` (2026-10-21), record `dossier/storage/proxyrack-unlimited-residential.json`.
Verdict: `qualifies-with-caveat`.

### Sia Storage App (sia.storage)

> Free 50 GB; Plus $7.99/mo for 500 GB; Pro $14.99/mo for 5 TB; Unlimited $19.99/mo for 10 TB, then +$4.99/TB-mo. 20 TiB = $19.99 + 10 x $4.99 = $69.89/mo

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Depends on third-party hosts remaining online.

Evidence: `https://sia.storage/` (2026-10-21), record `dossier/storage/sia-storage-app.json`.
Verdict: `qualifies-with-caveat`.

### Blossom server fleet (24242.io, blossom.oslim.dev / Lotus, blossom.nostr.build)

> 24242.io 100 MiB/file, deleted if not accessed for 60 days. blossom.oslim.dev (Lotus): 100 MB/file and 8 GB per pubkey, retention 'permanent', cost 'free'. blossom.nostr.build: 20 MiB/file free tier, 'no limit on how many files, and no...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MiB on most servers (20 MiB on nostr. A new account costs anonymous. Observed behaviour: small volunteer hosts, several with unstated total capacity.

Evidence: `https://24242.io/` (2026-10-21), record `dossier/storage/blossom-server-fleet.json`.
Verdict: `qualifies`.

### nostr.download (route96 Blossom server)

> 10.00 GB per file (hard cap, read off the server's own TOS page). No published per-user total. 'Inactive file deletion: No limit'. 'Delete never-downloaded files: After 1 days'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 GB. A new account costs anonymous. Observed behaviour: single volunteer operator, no SLA, no durability warranty ('Do not use this service as your only backup').

Evidence: `https://nostr.download/` (2026-10-21), record `dossier/storage/nostr-download.json`.
Verdict: `qualifies`.

### nostrmedia.com (NIP-96 file host)

> free plan max_byte_size 26,214,400 (25 MiB); paid 'purple'/'onyx' 104,857,600 (100 MiB). `file_expiration: [0,0]` on every plan = never expires

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 25 MiB free. A new account costs anonymous. Observed behaviour: transforms media at ingest on some paths (resizing, format_conversion, compression, metadata_stripping are all listed in the manifest), so verify originals come back byte-identical.

Evidence: `https://nostrmedia.com/` (2026-10-21), record `dossier/storage/nostrmedia-com.json`.
Verdict: `qualifies-with-caveat`.

### SourceForge File Release System (FRS), frs.sourceforge.net

> No fixed quota. SourceForge's own docs: 'There are currently no fixed capacity limits around usage of our services. In lieu of specific disk usage caps (quotas), we may contact projects if they are using significant storage.' Guidance:...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 10 GB per file, 'Individual files larger than 10 GB will not replicate out.... The record states no identity cost. Observed behaviour: Two real hazards found by probing.

Evidence: `https://sourceforge.net/p/forge/documentation/Release%20Files%20for%20Download/` (2026-10-21), record `dossier/storage/sourceforge-file-release-system-frs-sourceforge-net.json`.
Verdict: `qualifies-with-caveat`.

### SourceForge Project Web (<project>.sourceforge.io)

> No quota stated anywhere on the page, the docs grant each project a vhost and say nothing about a byte limit. Practically it is the same filesystem family as FRS (uploaded over the same SFTP), so expect the same discretionary 20-30 GB band

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: observed live: https://libreoffice.sourceforge.io/ -> 200 with 134,123 bytes of real HTML.

Evidence: `https://sourceforge.net/p/forge/documentation/Project%20Web%20Services/` (2026-10-21), record `dossier/storage/sourceforge-project-web.json`.
Verdict: `qualifies-with-caveat`.

### Modrinth

> 500 MiB per version file (hard code-level cap: `read_from_field(field, 500 * (1 << 20), "Project file exceeds the maximum of 500MiB...")`). No stated total-account storage quota. Per-user quotas read from `user_limits`: projects = 256,...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: maximum of 500MiB. The record states no identity cost. Observed behaviour: Moderated registry: junk projects can be removed and files hard-deleted.

Evidence: `https://modrinth.com` (2026-10-21), record `dossier/storage/modrinth.json`.
Verdict: `qualifies-with-caveat`.

### Roblox Open Cloud Assets

> Per-asset caps only, no aggregate quota: 20 MB for most asset types; Video up to 3.75 GB each, up to 20 video uploads/day for ID-verified 13+ accounts (5 min duration, 4096x2160 max). Audio: 100 uploads/month if ID-verified, 10/month if not

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB/asset. The record states no identity cost. Observed behaviour: Moderation removes assets silently and irreversibly.

Evidence: `https://create.roblox.com/docs/cloud/guides/usage-assets` (2026-10-21), record `dossier/storage/roblox-open-cloud-assets.json`.
Verdict: `qualifies-with-caveat`.

### Thunderstore

> 5,242,880,000 bytes (~5 GB) per package zip, documented as a soft limit that staff will raise on request; server default in source is REPOSITORY_MAX_PACKAGE_SIZE_MB=500. No per-team total quota; the only total cap is a global server-wide...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: moderation queue. The record states no identity cost. Observed behaviour: Packages surviving as 'mods' for a real game community.

Evidence: `https://thunderstore.io` (2026-10-21), record `dossier/storage/thunderstore.json`.
Verdict: `qualifies-with-caveat`.

### iroh Mainline-DHT content discovery (iroh-content-discovery)

> No quota, no storage. Pure discovery: publishes BLAKE3->provider mappings onto the public BitTorrent Mainline DHT

That is the record's own wording (`reported`, 2026-10-21). A new account costs anonymous. Observed behaviour: Experimental repo (12 stars, last push 2026-10-16).

Evidence: `https://github.com/n0-computer/iroh-content-discovery` (2026-10-21), record `dossier/storage/iroh-mainline-dht-content-discovery.json`.
Verdict: `qualifies`.

### iroh Services, Community (free tier)

> 0 bytes of storage. Free plan = public relays in US/EU/Singapore, 7-day metrics retention, no auth, rate-limited traffic, no uptime guarantee

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Free tier requires an account only to see metrics.

Evidence: `https://www.iroh.computer/pricing` (2026-10-21), record `dossier/storage/iroh-services-community.json`.
Verdict: `fails-egress`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Arweave via ar.io / Turbo (ario-deploy free tier) | fails-quota | Turbo free tier: 105 KiB per data item, 10 MiB over the lifetime of a wallet AND 10 MiB over the lifetime of an IP range... |
| Filebase (IPFS tier) | fails-quota | Free: 5 GB pooled storage across Object Storage and IPFS, 500 pinned files, 10 GB/month IPFS bandwidth... |
| Filecoin Plus DataCap (faucet + allocators) | fails-egress | 1 TiB of free DataCap per verified client, instantly, via Gitcoin Passport... |
| IPFS Foundation public gateways... | fails-egress | No storage at all, gateway only. And the gateway itself is being retired: ipfs.io/dweb.link return HTTP 429 with... |
| Pinata, dedicated gateway (free plan) | fails-egress | 1 dedicated gateway included on Free; serves only CIDs pinned to the account unless a Gateway Access Control is added... |
| Storacha (successor to web3.storage) | trial-only | No longer offered, the developer upload and IPFS service was shut down. Was 5 GB free at launch (2025-05)... |
| Storj | fails-egress | No free tier since 2024-03-31. Current public page offers only a 30-day free trial... |
| thirdweb Storage | fails-quota | 1 GB included free; 1 GB, 1 TB at $0.05/GB/month; 1, 10 TB at $0.04; 10 TB+ at $0.03 |
| Walrus | fails-quota | No free tier on the network itself: $0.023/GB/month, billed on *encoded* size... |
| Bright Data residential network (buy side) | fails-quota | pay-as-you-go $4.00-$8.00/GB depending on tier (141 GB included at $4.00/GB after the RESIGB50 coupon... |
| Chameleon Cloud (TACC / UChicago) | fails-identity | 534 nodes across KVM@TACC, CHI@UC, CHI@TACC, CHI@NRP; 62 nodes with >1TB total storage... |
| CloudLab c240g1 / per-node local blockstore (40 TB) | fails-identity | c240g1 node type = 12 x 3 TB HDDs (36 TB raw) on 5 nodes at Wisconsin... |
| CloudLab persistent remote dataset (10 TB, iSCSI) | fails-identity | up to 10 TB per persistent remote dataset; pool is 500 TB at Utah, 160 TB at Wisconsin... |
| Crust Network DSM | fails-quota | storage orders placed on-chain, each held for six months; the top four nodes submitting proofs share that file's reward |
| FABRIC testbed | fails-identity | VMs up to 64 cores / 384 GB RAM with directly attached NVMe, GPUs, SmartNICs; 'large storage volumes'... |
| Filecoin Plus / DataCap free storage | fails-quota | was: DataCap granted by allocators, deals free or near-free to the client because SPs got 10x quality-adjusted power |
| Frontproxy (unlimited residential, speed-tiered) | trial-only | $10 for a 3-day 25 Mbps unlimited trial; Pro from $375/day at 400 Mbps unlimited... |
| PacketStream (buy side) | fails-quota | $1.00/GB, $50 minimum purchase, balance never expires |
| Nostr relays as blob transport (event path... | fails-quota | no storage quota, but a hard per-event size ceiling that is the real limit... |
| Xirsys free (Developer plan) | fails-quota | 500 MB monthly TURN bandwidth on the free Developer plan, capped bandwidth... |
| ZeroTier free (Personal) | fails-quota | 10 devices, 1 network, non-commercial use. Vendor table effective 20 Oct 2026: 'Personal / Free / 10 / Not available' |
| Bulknews, free Usenet trial (10 GB) | trial-only | Trial: 10 GB, unlimited speed, 30 connections, listed as FREE. Paid blocks start at 20 GB |
| Eternal September (news.eternal-september.org)... | fails-quota | No byte quota. Free read AND write access to all *text* newsgroups after online registration. 281 hierarchies... |
| PulsedMedia Free Seedbox Trial (Helsinki) | trial-only | 50 GiB storage, 250 MB RAM, 200 GiB torrent traffic, 1 Gbps, for 30 days, free. 'Free Seedbox Trial 30 Days... |
| Puter (puter.com / Puter.js), user-pays cloud storage | fails-quota | Free tier shown on puter.com as '25 MB Storage' (the 100 GB / 500 GB / 2 TB figures on that page are the paid tiers... |
| Seedr, free tier | fails-quota | Free tier exists but is deliberately unspecified: 'You can try Seedr for free... |
| Arweave via Turbo / ar.io free tier | fails-quota | Free tier: 105 KiB per data item, and only 10 MiB over the lifetime of a wallet AND 10 MiB over the lifetime of an IP... |
| CurseForge (Overwolf) author upload API | fails-quota | No published per-file or total quota. Known caps: project media/gallery images limited to 2 MB (author complaint... |
| Ethereum blobs (EIP-4844) as a storage layer | fails-egress | No free tier. Live cost at time of check: $0.012 per MB as blobs (vs $11.01/MB as calldata). 128 KB per blob package... |
| Solana account rent as raw storage | fails-quota | No free tier, storage is a refundable rent-exempt deposit: 10 MiB account costs 53,268,311,040 lamports... |
| deCDN | fails-quota | No free capacity. No storage tier at all: 'Not a blockchain or storage network, durability relies on cheap... |
| Hippius Arion (Bittensor subnet on iroh) | fails-quota | Paid storage product (Hippius sells S3-compatible storage, Drive, Hub). No free tier published on the pages opened |
| Self-hosted Kubo/Rainbow gateway (own VPS) | fails-egress | Storage and egress are whatever the VPS or host allows. No provider quota exists... |
| M-Lab (host a measurement site) (self-hosted) | fails-quota | contribute servers, not consume storage; host-managed deployment onboarding is 'almost entirely automated' for 'any... |
| NYC Mesh (self-hosted) | fails-quota | a network connection plus the ability to host services on it; no storage quota because there is no storage product |
| Proxyware earn-app tier as a purchasable egress path... (self-hosted) | fails-egress | these pay the contributor; they do not sell to the buyer. Honeygain 10 GB = $1 ($0.10/GB); PacketStream $0.10/GB... |
| RIPE Atlas (host a probe or anchor) (self-hosted) | fails-quota | no storage; hosting earns credits spendable on custom measurements |
| Sia host (hostd) - supply side / the arbitrage test (self-hosted) | fails-quota | the host sets its own price; network median is $1.17/TB/month storage and $2.25/TB download (siascan), $1.30 KS/TB/month |
| Storj storage node operator (supply side) (self-hosted) | fails-quota | paid $1.35/TB/month stored + $1.00/TB egress (cut from $1.50/$2.00 on 1 Sep 2026... |
| Veilid (self-hosted) | fails-quota | no quota and no account, 'All Veilid applications running veilid-core are nodes... |

The relay networks are the largest rejection group and the reason is arithmetic rather than
policy. A free TURN tier is a byte meter, and a byte meter at 33 GB per day is 3% of the
workload. libp2p's circuit relay v2 is architecturally excluded rather than merely slow: the Go
default resets a relayed connection at 128 KiB per direction per two minutes, which is a
hole-punching budget rather than a transfer budget.

`not-storage` covers the signalling services that were counted as capacity: a discovery
service that publishes mappings onto a DHT holds nothing, and a WebRTC signalling library
exchanges session descriptions rather than bytes.

The most expensive mistake in this group is the cheapest storage in this topic. Filecoin
Onchain Cloud at USD 2.50 per TiB per month looks like a Hetzner replacement until the egress
line is read.

## Chaining

The rule that follows from the signalling-versus-relaying distinction is short: pin with a
Blossom server and use iroh as a second read path, never as the store.

The pairing that works is a self-signed keypair against two Blossom servers with different
retention models, because the credential costs nothing and content addressing makes the copy
verifiable. The pairing that does not work is any design where a relay carries the bytes at
this volume, because the free tier is measured in gigabytes per month and the workload is
measured in terabytes per day.
