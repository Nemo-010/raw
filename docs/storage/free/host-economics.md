# How a free host pays for the disk, and what a pool costs

Every free bulk host in this corpus is losing money on storage and making it back somewhere
else. The somewhere else is not a secret, and it decides which hosts survive. This document
answers two questions: how a free host affords the disk, and what the chunk-and-replicate
architecture costs when twenty hosts are assembled into one store.

The provider records live in the other documents. This page is the economics and the
tooling, and the 49 mechanisms below are not providers, so they carry no dossier and no
place in the provider count.

## Three mechanisms, and only three

A reconstruction of operator publications finds three funding models. There is no fourth.

**Retention expiry is the business model, not an oversight.** A host's cost exposure is
arrival rate multiplied by retention, never cumulative bytes. Buzzheavier runs an 8-day base
life, plus 2 days per download, capped at 60 days. Gofile runs 10 days. Pixeldrain runs 60
days, reset only by a GET that moves more than 10% of the file. 1fichier runs 30 or 90 days,
and its own terms say automated accesses do not count. file.kiwi runs 90 hours. Catbox is
permanent, and is consequently the only host in the class capped at 200 MB per file. That
trade is the industry in one sentence.

**Downloader-paid egress.** The GET is monetised and the storage is the loss leader.
Pixeldrain sizes ad intrusiveness to file size and throttles free traffic to about 1 MiB/s
past roughly 5 GB per day per IP. file.kiwi charges USD 2 per download pass and USD 5 per
additional 6 hours. 1fichier sells "advertising, human-verification step, waiting time, limited speed" as the
free tier's description. Throttling the read path is the business model at five of seven
hosts, which is exactly why none of them can serve 500 GB per day and why the class is
unusable as a serving tier regardless of quota.

**Flat-rate colocation on owned autonomous systems.** Catbox publishes the whole bill: USD
1,810 per month for 272 TB of storage and 19 PB per year served, which is about USD 1.10 per
TB served. Gofile runs AS214390 and sells traffic at USD 2 per TB. 1fichier is AS198792 and
sells transit itself. The cheap hosts are cheap because they are the network, not because
they found free disk.

The folklore to discard is that these hosts ride someone else's free tier. R2's free tier is
10 GB per month, so file.kiwi is not using it for free; it is buying metered R2 and
using only the zero-egress line, which its own presigned `*.r2.cloudflarestorage.com`
URLs prove.

## What funds each class, and what that predicts

The class of funding predicts survival better than the quality of the page that described
the provider.

| funding | examples | what it predicts | evidence |
|---|---|---|---|
| Ad and download monetisation | pixeldrain, 1fichier | persists, throttles the read path | pixeldrain's operator posts monthly recaps: 1.26 EB served and 25,056 TB stored in 2025, with 90% of traffic from free accounts |
| a reseller used beyond its allocation | buzzheavier before 2024-12 | a hard expiry date | the host's own post: "storage exploits... about USD 1 per TB per month... after the recent police raid, our provider caught on. Game over"; in plain terms, capacity resold below cost, then the supplier shut it down |
| Institutional subsidy | Internet Archive | persists on donated infrastructure | the only host in this class whose mechanism is an institution rather than a business |
| Sold to someone else | Cloudflare R2, national research clouds | persists, because storage is the product | R2 sells zero egress as a feature; a research cloud sells allocation |
| One person's server | `pan.moe`, Ploud, 1yunpan | a half-life of months | five Cloudreve instances died within two years of being recorded |

The actionable reading: weight an archive toward providers whose storage is a product they
sell to someone else, and away from providers whose storage is a loss leader against ad
revenue. Neither extreme is storage that lasts a decade, but only one of them has a
revenue line that survives the archive.

## The reference implementation

`hoangvu12/free-s3` presents one S3-compatible endpoint over a pool of about 19 free hosts,
and its `RESEARCH.md` is a verified catalogue of each host's upload API, per-file cap,
retention and direct-URL shape. Note the branch: `RESEARCH.md` lives on `master`, and `main`
404s. A pruned copy is kept at
[`references/hoangvu12__free-s3/RESEARCH.md`](../../../references/hoangvu12__free-s3/RESEARCH.md),
because a third-party research file in a personal repository is the kind of document that
vanishes, and this one is the source for the claim.

The design, in the project's own words: chunk every object, upload each chunk to a free host,
store `(object -> [chunk: provider, locator, size, offset, replicas[]])` in a metadata
database, and reassemble on GET. Object size becomes unbounded, chunks spread and replicate
across providers so one host vanishing is not data loss, and the replication factor becomes
the durability dial. A keep-alive plus a 404 repair loop re-fetches from a replica and writes
back.

That is the mechanism: 20 TiB does not sit on one provider. It sits in 100 GB
chunks, replicated two or three times, across twenty providers, with a repair loop.

## The three layers

A pool is built in three layers, and only the third one is hard.

**Namespace merge.** `rclone union`, `mergerfs`, AList and OpenList, Cloudreve. These present
many remotes as one tree. Useful, and it cannot beat a per-file cap: a 200 MB cap stays a
200 MB cap. Every "unlimited cloud drive" claim that turns out to be shallow is this layer
alone.

**Chunk and place.** Split at the smallest common cap, not the largest. If one provider in
the pool takes 100 MB and another takes 100 GB, the chunk size is 100 MB unless the pool is
tiered. The projects that do this well:

| project | what it does |
|---|---|
| `hoangvu12/free-s3` | S3 gateway, provider pool, SQLite metadata; the reference implementation |
| `smit-p/pdrive` | rclone as transport (about 70 backends), chunking, optional Reed-Solomon, index backed up into the same pool |
| `scatterbox` | placement arithmetic: `ec(k,n)` erasure coding and `--spread packed` computing the maximum any one host holds |
| `telegram-s3` | the ancestor: Telegram chunked behind an S3 interface |

**Durability and repair.** Keep-alive re-reads to defeat inactivity pruning, and a 404 path
that fetches another replica and writes back. The honest assessment in the source material is
that the best form of this is "best-effort", because a host outside the deployment cannot be
audited.

## What the pool actually contains

The catalogue below is organised by what a provider gives, not by who it is. Every host here
has a record in one of the provider documents; this table is the pool view.

| tier | what it means | examples |
|---|---|---|
| Durable anchors | a real API, permanent retention, datacentre-friendly | Internet Archive, GitHub Releases, pCloud, Google Drive, OneDrive, Filebase, Lighthouse, Pinata |
| Anonymous durable | no signup, arbitrary types, long retention | FileDitch, pixeldrain, catbox, gofile, x0.at, pomf, buzzheavier, paste.c-net.org |
| Scratch | always re-derivable from a replica | temp.sh, tmp.ninja, litterbox, envs.sh, tmpfiles, uguu, filebin |

The catalogue's exclusions are worth as much as its inclusions, and several confirm findings
recorded elsewhere in this topic. file.io deletes on first download, which breaks replicated
reads. Storj's free tier ended. web3.storage's permanent tier is gone and NFT.Storage Classic
is dead. Crust needs a token. TeraBox serves an automated-traffic filter page and has no
official API.

One correction to the source catalogue: FileDitch's 100 GB and "permanent" pair does not
match the probe, which found the uploader's own JS constant at 155 GiB and no
published retention. The record carries the probe.

## The tools that make a pool work

These are implementations and mechanisms, not providers. They get no dossier and they do not
enter the provider count, because giving `mergerfs` a provider record would inflate a count
that a reader uses to judge coverage.

| tool or mechanism | what it does |
|---|---|
| `rclone union` | presents many remotes as one tree, with a policy per remote |
| `mergerfs` | a FUSE union over local and mounted paths |
| `hoangvu12/free-s3` | the S3 gateway over a provider pool |
| `smit-p/pdrive` | chunking, Reed-Solomon, index inside the pool |
| `scatterbox` | erasure-coding placement arithmetic |
| `telegram-s3` | Telegram as an S3 backend |
| `8storage` | several-accounts Drive pool with chunk, encrypt and round-robin |
| `GegeDevs/udrive` | pool several free Google Drive accounts behind one REST front end |
| `Maverick1983/google-drive-service-account` | the canonical published service-account write-up |
| `RcloneView` union how-to | the published procedure for combining free accounts |
| Apache OpenDAL | one operator API over 50 or more storage services |
| Tailscale DERP, Syncthing public relays | signalling only, with data peer to peer |
| iroh, `iroh-relay` self-hosted | BLAKE3-verified blobs over QUIC; the relay is a fallback path |
| Yggdrasil Network | a routed overlay whose peers meter rate rather than bytes |
| NKN, `nkn-tunnel` | a relay network with a free client mode |
| IPFS and libp2p circuit relay v2 | excluded as a data path by its own 128 KiB per 2 minutes default |
| Cloudflare Realtime TURN, Metered Open Relay, Twilio, Xirsys, Turnix, freeturn.net | free TURN tiers, all byte-metered |
| `croc`, `magic-wormhole`, `sendme` | point-to-point transfer with no store behind it |
| AList and OpenList (self-hosted) | a web front end and API over many storage backends |
| Cloudreve (self-hosted) | a bridge like OpenList, with its own user model |
| Teldrive, tgstate, tgnas (self-hosted) | Telegram-backed file managers |
| Headscale, NetBird (self-hosted) | self-hosted control planes for a private overlay |
| JuiceFS community edition (self-hosted) | one volume bound to one object endpoint; the multi-bucket request is open |

Three of these are load-bearing for the architecture and one is excluded by arithmetic. The
union layer is what makes a pool addressable. The chunker is what makes it larger than any
member. The metadata index is the only irreplaceable component, because it is the one thing
no provider holds. And circuit relay v2 is excluded by its own defaults: the Go
implementation resets a relayed connection at 128 KiB per direction per two minutes, which is
a hole-punching budget rather than a transfer budget.

## What the buzzheavier lead settled

The open question was how buzzheavier could afford arbitrary uploads at volume. The
answer is that it could not, and its operator said so.

The blog post "The Real Cost of Storage: A Fresh Start" (2024-12-02) states that the service
ran on "storage exploits" at about USD 1 per TB per month until "our provider caught on. Game
over" after the host's servers were seized, and that it now pays EUR 5 to 6 per TB per
month. In plain terms, that is storage resold below cost, ended when the supplier shut the
arrangement down. The singular "provider", not a set of consumer tiers combined, points at
one reseller used beyond its allocation rather than the chunk-and-replicate architecture.

Only three posts ever existed, and one of them carries the title "Exploit GitHub as infinite
storage" (2024-12-19) and describes using GitHub Releases fronted by `fafda`, an FTP and
rclone front end. That repository is deleted, which is why the lead cannot be re-run.

The live probe now shows the pattern this corpus warns about most: an anonymous PUT returns
201 with a 4-day expiry, and every read path returns 403 with `Cf-Mitigated: challenge`. A
write-only sink from a server.

## The one provider this document rejected

| provider | verdict | why it fails |
|---|---|---|
| Air Cluster, commercial product that advertises... (self-hosted) | fails-egress | 'Air Cluster allows you to add several accounts from the same server (e.g... |

One record in this document is a provider rather than a mechanism. Air Cluster is a commercial product that
advertises clustering over several cloud drives, at several accounts per drive. It is
`fails-quota` because the product sells the orchestration and the buyer
still supplies every account, so it adds no capacity that the accounts do not already hold.
The pool arithmetic above is what it implements, and a reader can build it from the tools
listed here for nothing.

## The honest floor, and what it implies

The host's own published figure is the niche's real cost: EUR 5 to 6 per TB per month.
That explains the 8-day clock. At that cost, holding an archive of 20 TiB for a stranger costs
EUR 100 to 120 per month for nothing.

Which gives the decision rule for this whole document. The per-provider numbers matter far
less than the sum of the pool, and durability is a parameter of the design. A pool of
the durable anchors alone already exceeds any single provider in this topic. The real work
is the metadata index and the repair loop, not the providers.

And the reason a single provider never reaches 20 TiB is not that no storage exists. It is
that no single provider wants to be the archive. The fix is to stop asking one to be.
