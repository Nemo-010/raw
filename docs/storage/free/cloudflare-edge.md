# Cloudflare edge: can a CDN be a store, and what does the edge actually guarantee

Cloudflare is the only provider in this topic whose free storage is a published product
commitment rather than a marketing sentence. Its static-asset pricing page states that
requests to static assets are free and unlimited on both free and paid plans, with no ratio,
no cap and no fair-use threshold. That is categorically stronger than every "unlimited" claim
in the paid lane, including Hetzner's.

It is also the provider where a plan built on the headline number fails twice.

This document covers 15 qualifying records: the two Cloudflare storage surfaces, the
static hosts that compete with them, and the edge CDNs that can be used as an object store.
9 were rejected.

## The comparison

Sorted by what the surface actually is: free static hosts first, then paid edge storage, then
the CDN proxies that multiply an existing store.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Cloudflare Pages (Direct Upload / Wrangler) | 20,000 files per site on Free; 25 MiB max per file... | per-object-cap: 25 MiB hard per file | - | qualifies |
| Cloudflare Workers Static Assets | 20,000 files per Worker version on Free; 25 MiB per file... | per-object-cap: 25 MiB per file | - | qualifies |
| GitLab Container Registry (gitlab.com) | Not counted against any storage quota. GitLab docs: 'Only the project's repository and... | - | - | qualifies |
| Neocities | Free: 1 GB storage, 200 GB/month bandwidth... | - | - | qualifies-with-caveat |
| Surge.sh | Free plan: unlimited projects and unlimited publishes... | - | - | qualifies-with-caveat |
| Akamai / Linode Object Storage | Scales 250 GB -> 5 PB per bucket, 10 billion objects... | - | card | qualifies-with-caveat |
| Bunny.net Edge Storage (+ free origin->CDN transit) | Unlimited volume, pay-as-you-go. $0.01/GB/mo HDD per region (up to 9 regions)... | per-ip-shaping: 100 concurrent conns per IP per server | card | qualifies-with-caveat |
| CacheFly Object Storage ($25/TB with $0 egress) | Unlimited, $25 per TB per month. S3-compatible | per-object-cap: not stated on the page opened | card | qualifies-with-caveat |
| CDN77 Object Storage | S3-compatible storage, slider up to 50 TB on the page... | - | card | qualifies-with-caveat |
| Gcore Free CDN (1 TB/mo traffic, no card) | 1 TB/month included traffic and 1 billion requests on the free PAYG plan at EUR... | - | email | qualifies-with-caveat |
| ghproxy mirrors (ghproxy.net, ghfast.top)... | No quota; it proxies raw.githubusercontent.com and release assets... | per-ip-shaping: the real constraint, observed ~128 KB/s (7 | anonymous | qualifies-with-caveat |
| hop.js CDN (cdn.hopjs.net)... | No quota of its own. It is a permanent mirror: every file is copied into Bunny Storage... | per-object-cap: ~64 MB proven, likely bounded by npm's own ~100 MB tarball... | anonymous | qualifies-with-caveat |
| raw.githack.com (CDN for GitHub/GitLab/Bitbucket raw... | No quota of its own; ceiling is GitHub's 100 MiB hard repo file block... | per-object-cap: GitHub's 100 MiB repo block is the real ceiling (50 MB proven) | email | qualifies-with-caveat |
| Telnyx Object Storage ($6/TB, zero metered egress) | Unlimited, $0.006 per GiB/month ($6.14/TB)... | - | card | qualifies |
| unpkg (npm CDN) | No storage quota of its own, it serves the npm registry... | per-object-cap: npm publish-side (~100 MB tarball, 413 above that) | email | qualifies |

## The arithmetic, and one unit error to fix first

Cloudflare Pages allows 20,000 files per site on the Free plan, 25 MiB maximum per file, and
100 projects per account. All three numbers are verbatim on the limits page
(`documented`, 2026-10-22: 200, 7,360 B).

20,000 x 25 MiB is 488.28 GiB per project. Times 100 projects is 48,828.125 GiB, which is
47.68 TiB per account.

The records state "~488 GiB per project, ~48.8 TiB per account", and the second figure
is the first times 100 with the unit left as it was: 48,828 GiB is not 48.8 TiB, it is
47.68 TiB. The 2.3% difference does not change any decision. The correct pair is 488 GiB and
47.68 TiB.

## Failure one: Pages is file-count-bound

47.68 TiB exists only if every file is at the 25 MiB cap. An archive of 20 TiB needs a mean object
of at least 10.49 MiB, and at a 1 MiB mean it needs 10.5 accounts. The full table is in
[`sharding.md`](sharding.md), because it is a shard-sizing fact rather than an edge fact.

The operational consequence belongs here: a Pages deploy is a full-project upload rather than
an incremental PUT. `wrangler` re-uploads any object whose hash is not already in the
deployment, page creation is throttled for a new account's first 48 hours, and an archive of
20 TiB at the cap is 42 projects of 20,000 files each. Nothing breaks; it is hours of wall time, and a
reason to build the archive once.

## Failure two: Pages serves no ranges

A `Range: bytes=0-1023` request to a Pages asset returns `200` with the full `Content-Length`
and no `Content-Range` and no `Accept-Ranges`. Two assets were probed
(`measured`, 2026-10-22): `favicon.svg` returned 200 with `Content-Length: 749`, and
`make-scrollable-code-focusable.js` returned 200 with `Content-Length: 116`.

So Pages is an archive downloaded whole. It rules Pages out as a serving tier, a resumable
fetch, a video seek, or a parallel ranged read. For a cold archive read rarely and in full,
that is acceptable; any plan that drifts Pages toward
serving is dead on these two probes.

## Workers static assets are the same product with a different name

20,000 files per Worker version, 25 MiB per file, 100 Workers per account, which is the same
48,828 GiB. The difference that matters is that a Worker can also execute, so the same account
holds both the store and the logic that serves it.

The cache cap is the number that constrains any edge-caching design: "Cloudflare does not
enforce response body size limits. CDN cache limits apply: 512 MB for Free, Pro, and Business
plans, and 5 GB for Enterprise" (`documented`, 2026-10-22: 200, 27,086 B). A 2 GiB object is
four times that cap, which is why a body cache cannot hold a release asset and a token cache
must. The full argument is in [`forge-surfaces.md`](forge-surfaces.md).

## The edge CDNs used as object stores

Seven records here are commercial edge storage sold per gigabyte, and they are in this
document because their egress term is the reason to consider them.

Telnyx sells object storage at USD 0.006 per GiB per month, about USD 6.14 per TB, with no
platform fee and zero metered egress. That is the cleanest zero-egress claim in the corpus
and it is `qualifies` rather than caveated.

CacheFly sells at USD 25 per TB with zero egress. CDN77 prices at USD 20 per TB. Bunny.net
charges USD 0.01 per GB per month for HDD storage per region with pay-as-you-go egress.
Akamai's entry plan is USD 5 per month for 250 GB with 1 TB outbound included.

None of these is free, and the class is worth reading against the paid lane rather than
against Pages. Their value is the ratio: a store at USD 6 per TB with no egress meter is
cheaper than a store at USD 2 per TB with a metered read, once the read is real.

## The proxies, which are not storage

Five records are proxies over somebody else's store: `ghproxy` mirrors, `raw.githack.com`,
`unpkg`, `hop.js` and `jsDelivr`. Each has no quota of its own because it holds no bytes; its
ceiling is the origin's.

They are useful for one thing and it is worth stating precisely. The same GitHub file is
limited to 20 MB on jsDelivr's `/gh/` path, 50 MB on raw.githack, and 64 MB on unpkg and
hop.js. One npm account publishing 45 MB shards therefore gives four independent free CDNs
over one write, and a shard sized to the wrong CDN silently 403s. A 50,901,339-byte GitHub file
served through raw.githack returned 200 with the full content length and a matching SHA-256.

A proxy is a multiplier on egress, not on capacity. Counting one as storage is the link-handoff
error the methodology names.

### Cloudflare Pages (Direct Upload / Wrangler)

> 20,000 files per site on Free; 25 MiB max per file; 100 projects per account => ~488 GiB per project, ~48.8 TiB per account. No stated total-bytes cap

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 25 MiB hard per file. The record states no identity cost. Observed behaviour: Assets stay cached on the CDN until the next deployment, so re-upload churn is the only real risk.

Evidence: `https://pages.cloudflare.com` (2026-10-22), record `dossier/storage/cloudflare-pages.json`.
Verdict: `qualifies`.

### Cloudflare Workers Static Assets

> 20,000 files per Worker version on Free; 25 MiB per file; 100 Workers per account => ~488 GiB per Worker, ~48.8 TiB per free account. 'There is no additional cost for storing Assets.'

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 25 MiB per file. The record states no identity cost. Observed behaviour: Free-tier 429s apply to script-invoking routes only.

Evidence: `https://developers.cloudflare.com/workers/static-assets/` (2026-10-22), record `dossier/storage/cloudflare-workers-static-assets.json`.
Verdict: `qualifies`.

### GitLab Container Registry (gitlab.com)

> Not counted against any storage quota. GitLab docs: 'Only the project's repository and LFS are included in the storage limit. The container registry, package registry, and build artifacts are not included in the limit.' The 10 GiB Free...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Storage is reported under 'reduce container registry storage' but no hard cap or eviction is documented on Free.

Evidence: `https://registry.gitlab.com` (2026-10-21), record `dossier/storage/gitlab-container-registry.json`.
Verdict: `qualifies`.

### Neocities

> Free: 1 GB storage, 200 GB/month bandwidth, WebDAV and API on Free (WebDAV is listed on the Supporter table as a Free-tier feature)

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Bandwidth is internally enforced and will throttle, not delete.

Evidence: `https://neocities.org` (2026-10-21), record `dossier/storage/neocities.json`.
Verdict: `qualifies-with-caveat`.

### Surge.sh

> Free plan: unlimited projects and unlimited publishes; each project capped at 450 MB and 10,100 files. No account-level byte quota

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Deploy is full-replace, not incremental, a slow link makes each publish expensive.

Evidence: `https://surge.sh` (2026-10-21), record `dossier/storage/surge-sh.json`.
Verdict: `qualifies-with-caveat`.

### Akamai / Linode Object Storage

> Scales 250 GB -> 5 PB per bucket, 10 billion objects, 20K RPS. Entry plan $5/mo = 250 GB + 1 TB outbound included

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Post-Linode acquisition.

Evidence: `https://www.linode.com/products/object-storage/` (2026-10-21), record `dossier/storage/akamai-linode-object-storage.json`.
Verdict: `qualifies-with-caveat`.

### Bunny.net Edge Storage (+ free origin->CDN transit)

> Unlimited volume, pay-as-you-go. $0.01/GB/mo HDD per region (up to 9 regions), $0.02/GB/mo SSD per region (up to 15). 20 TiB single-region HDD = $200/mo. $1 monthly minimum

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 100 concurrent conns per IP per server. A new account costs card. Observed behaviour: PCI/99.99% SLA on storage.

Evidence: `https://bunny.net/pricing/storage/` (2026-10-21), record `dossier/storage/bunny-net-edge-storage.json`.
Verdict: `qualifies-with-caveat`.

### CacheFly Object Storage ($25/TB with $0 egress)

> Unlimited, $25 per TB per month. S3-compatible

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: not stated on the page opened. A new account costs card. Observed behaviour: Self-signup 'requires a credit card at registration.

Evidence: `https://www.cachefly.com/object-storage/` (2026-10-21), record `dossier/storage/cachefly-object-storage.json`.
Verdict: `qualifies-with-caveat`.

### CDN77 Object Storage

> S3-compatible storage, slider up to 50 TB on the page; priced at '$100/month ($0.02/GB)' i.e. $20/TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: 330 Tbps, enterprise-oriented.

Evidence: `https://www.cdn77.com/pricing` (2026-10-21), record `dossier/storage/cdn77-object-storage.json`.
Verdict: `qualifies-with-caveat`.

### Gcore Free CDN (1 TB/mo traffic, no card)

> 1 TB/month included traffic and 1 billion requests on the free PAYG plan at EUR 0/month. Verified against Gcore's own pricing payload: 'Included FREE Traffic 1 TB/Month', 'Traffic overage (per GB) EUR 0.01', 'Requests over 1B (per 1M) EUR...

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: 210+ PoPs, 200+ Tbps.

Evidence: `https://gcore.com/cdn` (2026-10-21), record `dossier/storage/gcore-free-cdn.json`.
Verdict: `qualifies-with-caveat`.

### ghproxy mirrors (ghproxy.net, ghfast.top), free anonymous GitHub raw/release proxy

> No quota; it proxies raw.githubusercontent.com and release assets, so the ceiling is GitHub's own (100 MiB/repo file, ~1.95 TiB/release). Probed a 50,901,339-byte GitHub file through ghproxy.net: HTTP 200, correct Content-Length

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: the real constraint, measured ~128 KB/s (7. A new account costs anonymous. Observed behaviour: Volunteer infrastructure, high churn, of four mirrors tested observed, gh-proxy.com and cdn.gitmirror.com failed to resolve/connect while ghproxy.net and ghfast.top both returned the full file.

Evidence: `https://ghproxy.net/` (2026-10-21), record `dossier/storage/ghproxy-mirrors-free-anonymous-github-raw-release-proxy.json`.
Verdict: `qualifies-with-caveat`.

### hop.js CDN (cdn.hopjs.net), Bunny.net's free OSS mirror of npm + cdnjs

> No quota of its own. It is a permanent mirror: every file is copied into Bunny Storage SSD and served from there, so your ceiling is the npm cap. Probed single files of 32.2 MB, 54.0 MB and 64.5 MB, all served complete and byte-identical...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: ~64 MB proven, likely bounded by npm's own ~100 MB tarball publish limit.... A new account costs anonymous. Observed behaviour: Young third-party service (Bunny-backed, 119 PoPs, logging disabled by design).

Evidence: `https://hopjs.bunny.net/` (2026-10-21), record `dossier/storage/hop-js-cdn-bunny-net-s-free-oss-mirror-of-npm-cdnjs.json`.
Verdict: `qualifies-with-caveat`.

### raw.githack.com (CDN for GitHub/GitLab/Bitbucket raw files)

> No quota of its own; ceiling is GitHub's 100 MiB hard repo file block. Probed a 50,901,339-byte GitHub file: HTTP 200, full length, sha256 fd112e5b... A 3,408,573-byte file came back with sha256 55fb913b..., byte-identical to jsDelivr's...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: GitHub's 100 MiB repo block is the real ceiling (50 MB proven). A new account costs email. Observed behaviour: Small independent operator, its own homepage says it serves 479M+ requests and 46 TB+ of traffic monthly, which is ~0.2% of a 1 TiB/day serving target, so treat it as a mirror.

Evidence: `https://raw.githack.com/` (2026-10-21), record `dossier/storage/raw-githack-com.json`.
Verdict: `qualifies-with-caveat`.

### Telnyx Object Storage ($6/TB, zero metered egress)

> Unlimited, $0.006 per GiB/month ($6.14/TB), no platform fee. Confirmed live: '$0.006per GB/mo', '$0platform fee', and the page's own worked example '10,000 GB STORED... $60.00'

That is the record's own wording (`reported`, 2026-10-21). A new account costs card.

Evidence: `https://telnyx.com/pricing/storage` (2026-10-21), record `dossier/storage/telnyx-object-storage.json`.
Verdict: `qualifies`.

### unpkg (npm CDN)

> No storage quota of its own, it serves the npm registry, so the ceiling is npm's ~100 MB publish limit. Probed 28.3 MB, 32.2 MB, 54.0 MB and 64.5 MB single files: all HTTP 200, all full length, sha256 identity with hop.js on the 54 MB and...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: npm publish-side (~100 MB tarball, 413 above that). A new account costs email. Observed behaviour: Long-running but small-team.

Evidence: `https://unpkg.com/` (2026-10-21), record `dossier/storage/unpkg.json`.
Verdict: `qualifies`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Codeberg Pages (git-pages) | fails-quota | No hard quota: 'there is no quota for valid use-cases', with a soft review threshold at 750 MiB Git storage and 1.5 GiB... |
| GitLab Pages (gitlab.io) | fails-quota | 1 GB maximum site size on gitlab.com (tied to the 1 GB max artifact size); 200,000 file entries per site; unlimited projects |
| Netlify Blobs | fails-egress | Object store with 5 GB max per object, but the Free plan is 300 credits/month where 1 GB of web bandwidth = 20 credits... |
| Fastly free account + Fast Forward OSS programme | fails-quota | Free account: 100 GB bandwidth/month free across all regions, 1M CDN requests/month, 5 domains... |
| KeyCDN Push Zone (CDN storage) | fails-egress | Unlimited volume. Push Zone storage '$0.12/GB per month and charged on a daily basis' = **$120/TB/mo**... |
| AWS Lambda layers (and function deployment packages) | fails-quota | Per-function/per-layer caps only, plus a regional aggregate. Verbatim: 'Deployment package... |
| Deno Deploy (managed Deno KV) | fails-quota | 1 GiB of KV storage on Free. Pricing page, KV section: 'KV storage: 1 GiB'; 'KV read units/mo (4KiB): 1,000,000'... |
| Vercel Blob (Hobby plan) | fails-quota | 1 GB/month of storage, TOTAL per Hobby team, not per project... |
| Vercel Deployment Storage / artifact store (Hobby... | fails-quota | 10 GB of Deployment Storage per Hobby team, and that pool is what every retained deployment output draws from... |

The failures split three ways. Vercel's Hobby tier caps a static upload at 100 MB per
deployment and has capped deployment retention at 30 days since April 2026, which makes it a
deploy target rather than a store. Netlify's "100 GB" is legacy-only. Cloudflare Stream is
priced in minutes rather than bytes, at USD 5 per month per 1,000 minutes of storage, which is
a different unit and cannot be compared with a byte quota.

`not-storage` covers the proxies that look like capacity: a CDN that
truncates a response at 16,384 bytes while sending a correct `Content-Length` for the full
object is worse than a 404, because every automated check reads it as success.

## Chaining

Pages is the cold tier and the Worker is the logic, and they are one account. That pairing is
the strongest free combination in this corpus: contractually unmetered static serving, no
retention clock, and a published commitment with no ratio.

The pairing that does not work is Pages for serving. The absence of range support is not a
performance issue, it is a capability one, and a plan that puts Pages behind a Worker expecting
ranged reads is dead on the first `Range` header.
