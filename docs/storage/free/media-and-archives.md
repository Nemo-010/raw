# Media and archives: what survives ingest byte for byte

This class is the one where a provider holds a huge quantity of bytes and returns
something else. A video platform, a podcast host and a 3D-print marketplace all accept a
large upload and then transcode, thumbnails, or re-pack it. That makes them storage for the
platform and not storage for the uploader, and the distinction is testable in one request:
upload a file with a known digest, download it, compare the bytes.

The 35 qualifying records below are the ones that pass that test or that serve a
genuine archive function. They cover the Internet Archive and its satellite services, video
platforms, software archives, citizen-science and heritage projects, and print and media
fulfilment. 30 more were rejected.

## The comparison

Sorted by the size of the single object they accept. A `*` in the identity column means the
value is read off the record's own prose rather than from its `identity_cost` field.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| 24242.io, public Blossom blob server (Nostr) | No account, no quota, no total cap stated... | per-object-cap: 100 MiB/file | anonymous | qualifies-with-caveat |
| blossom.ditto.pub (Ditto Blossom server) | No quota. Live server stats: 1,375,309 total blobs, 781.96 GB storage used... | per-object-cap: 2 GB/upload | anonymous | qualifies-with-caveat |
| Macaulay Library / eBird (Cornell Lab of Ornithology) | No published per-account byte quota, tens of millions of assets... | per-object-cap: 20 MB/file | institution | qualifies-with-caveat |
| Mapillary (Meta) | 'unlimited storage' per Mapillary's own blog: 'Mapillary offers unlimited storage and... | request-rate: 50,000 requests/minute/app | institution | qualifies-with-caveat |
| OpenAerialMap (HOT / Open Imagery Network) | Free hosting for anyone with nowhere to publish... | per-object-cap: 100 GB/file | institution | qualifies-with-caveat |
| Panoramax, OSM-FR instance... | NO QUOTA ANYWHERE IN THE SERVER. There is no quota code... | per-object-cap: 18 MB per 96 MP photo | institution | qualifies |
| Panoramax federation, 25 instances with per-instance... | No quota on any instance (same codebase, same absence of a quota mechanism)... | - | email | qualifies |
| Wikimedia Commons | NO TOTAL QUOTA, read verbatim from Commons:Maximum_file_size: 'there is no limit to the... | per-object-cap: 5 GiB/file | institution | qualifies-with-caveat |
| archive.org /download web serving path (the free CDN) | Serving is unmetered and free; no per-file download cap and no egress fee... | - | - | qualifies-with-caveat |
| IAS3 old-version retention... | No quota of its own, it multiplies the 1TB item limit by however many versions are PUT... | per-object-cap: 1TB item | - | qualifies-with-caveat |
| iiif.archive.org (free IIIF Image API over any... | No separate quota, it is a free image server over items already held... | per-object-cap: 1TB/item | - | qualifies-with-caveat |
| Internet Archive BitTorrents (webseed swarm) | Free, unlimited distribution; ~1.4 million items already torrented... | - | - | qualifies-with-caveat |
| Blomp (AIN/Blomp Cloud Storage) | 40 GB free on signup, advertised and confirmed as 'Get Up to 400 GB for Free'... | retention-clamped: invited account must log in at least once a year or the... | email | qualifies |
| Jottacloud (Norway) | 5 GB free. 'Unlimited*' Personal at USD 12.99/mo or USD 129.90/yr... | per-ip-shaping: upload speed throttled above 5 TB... | email | qualifies-with-caveat |
| PikPak | 6GB free; 10TB on Premium ("Free accounts include 6 GB of storage... | retention-clamped: inactive 12 months are deleted (effective 20 | - | qualifies-with-caveat |
| Apple Books (iTunes Connect / Partner) | 2 GB per book file, per the widely-cited store-limit table... | per-object-cap: ~2 GB (secondary source only) | email | qualifies-with-caveat |
| DLsite (circle / web upload) | 10GB (10 GB per work) via web upload; '10GB' (works over 10 GB can still be handled... | per-object-cap: 10 GB web / larger on request | email | qualifies-with-caveat |
| Google Play Books Partner Center | 2 GB per content file ('Each file must be less than 2 GB... | per-object-cap: 2 GB | email | qualifies-with-caveat |
| Gumroad | Own help centre: 'If you price your product at any number greater than $0.99... | per-object-cap: 20 GB (products >$0 | email | qualifies-with-caveat |
| Nexus Mods | Vendor help page states it outright: 'Unlimited storage and distribution for mods and... | per-object-cap: 20 GB via browser, larger by request | email | qualifies-with-caveat |
| Payhip | Explicit, from their own page: 'No, we have no storage or bandwidth limits... | per-object-cap: 5 GB, the only limit they publish | email | qualifies |
| Printables (Prusa Research) | No published account quota and no published upload cap... | per-object-cap: 1.037 GB | email | qualifies |
| Sellfy | Their own sell-downloads page: 'Upload unlimited eBooks, music, software, courses... | per-object-cap: 20 GB | email | qualifies-with-caveat |
| Fedora COPR (copr.fedorainfracloud.org) | No published storage quota, unlimited projects and builds for Fedora Account holders... | retention-clamped: deleted after 14 days | - | qualifies-with-caveat |
| Hackage (hackage.haskell.org) | No published per-package or total quota found on the upload page or the server API... | - | - | qualifies-with-caveat |
| Launchpad PPA (Ubuntu Personal Package Archive) | 8 GiB of disk per PPA by default ('Disk space / 8 GiB... | - | - | qualifies-with-caveat |
| openSUSE Build Service (OBS) - build.opensuse.org... | No published storage quota at all. The service is 'currently free for use' and 'anybody... | - | - | qualifies |
| Snap Store (api.snapcraft.io / snapcraft.io) | No published total-storage quota and no published per-snap byte cap... | per-object-cap: 5.5 GB upload | - | qualifies-with-caveat |
| Software Heritage Archive... | No storage quota is imposed on the depositor... | per-object-cap: (deposit only): 100 MiB documented... | anonymous* | qualifies-with-caveat |
| Dailymotion | No total storage cap stated. Per-account upload policy: 4 GB per file... | per-object-cap: 4 GB per file | - | qualifies-with-caveat |
| Odysee / LBRY | No storage quota at all. 16 GB per file via the Odysee uploader... | per-object-cap: 16 GB per file | - | qualifies |
| PeerTube, peertube.cif.su (open registration... | Unlimited total quota (`user.videoQuota: -1`)... | - | anonymous* | qualifies-with-caveat |
| Rumble | No published total storage cap. 15 GB per file standard... | per-object-cap: 15 GB/file | - | qualifies-with-caveat |
| Vimeo (Free plan) | Unlimited storage for public, non-embeddable videos... | per-object-cap: 200 GB per file | - | qualifies-with-caveat |
| YouTube (unlisted), with DCT/fountain-coded payload | No total storage cap. Per-upload max 256 GB or 12 hours... | per-object-cap: max 256 GB | - | qualifies-with-caveat |

## What the class is

Three different things are in this document and they fail differently.

**An archive** holds the bytes and serves them back. The Internet Archive is the only
institution-scale member of that group, at 1 TB per item and unlimited items, and it is the
only host in this corpus whose mechanism is neither advertising nor a subsidy but an
institution with a budget.

**A video platform** holds a rendition. YouTube, Vimeo, Dailymotion and Rumble all discard
or re-encode the source. Odysee and PeerTube return originals, which is why both appear as
`qualifies` rather than `qualifies-with-caveat`, and the one platform in this corpus that
stores an arbitrary payload is YouTube with a DCT and fountain-coded payload, which is a
coding scheme rather than a storage feature.

**A fulfilment surface** takes a large input and has no read path at all. Print-on-demand is
the clearest case: Lulu takes unlimited ingress, IngramSpark 1.5 GB, KDP 650 MB, and none of
them will serve the bytes back. That is a category error rather than a quota failure, and it
is recorded as such.

## The Internet Archive, and what its satellites do

The Archive is the strongest finding in this document, and it is worth stating the whole
shape rather than the quota.

1 TB per item is a hard limit and unlimited items per account makes the total unbounded.
The uploading-tips page states "Currently, there is a 1TB size limit for item pages" and
recommends at most 1,000 files or 500 GB per item (`documented`, 2026-10-22: 200, 5,433 B).
The interface is IAS3, which is S3-compatible, so rclone and the `ia` CLI both work.

Four satellite services extend it and each is a separate record:

`x-archive-keep-old-version` multiplies the 1 TB by however many versions are written, and
places them at `history/files/$key.~N~`. It is a version store rather than a capacity
multiplier, but the bytes are real.

`iiif.archive.org` is a free IIIF Image API over any uploaded image, one image per item, so
its capacity follows the 1 TB rule rather than adding to it.

The BitTorrent webseed swarm is a second distribution path: an item gets an
`_archive.torrent`, and about 1.4 million items are already torrented, which makes the
swarm a free egress channel that does not touch the per-IP shaping.

The `/download` web path is unmetered and free, with no per-file cap and no egress fee. What
bounds it is throughput rather than quota, at about 145 GB per day per IP.

## Panoramax, and what "no quota anywhere in the server" means

The OSM-FR Panoramax instance has no quota code, no quota column in its database
migrations, and no quota endpoint, because the feature does not exist. That is a stronger
claim than a published number, and it is a documented absence rather than a documented
limit: it cannot be multiplied, because the constraint is whatever the host's disk does.

The federation makes it more useful than one instance. The catalogue at `GET /api/instances`
lists 25 instances with a per-instance `registration_is_open` flag, so a reader can check
which ones accept a new account before trying. One instance is already holding 48.5 TB.

## The software archives

The software archives are the class where a build system is the write path, and that makes
them `write-gated` rather than quota-bound.

Fedora COPR accepts unlimited projects and builds and keeps one build per project, so its
constraint is retention. openSUSE Build Service publishes no storage quota and anybody can
build. Launchpad gives 8 GiB per PPA by default, with larger quotas on request. Hackage
publishes a package permanently and states no quota at all. The Snap Store publishes no
total quota and no per-snap cap.

SourceForge is the outlier and the best of them: "There are currently no fixed capacity
limits around usage of our services", with a 10 GB per file soft ceiling
(`documented`, 2026-10-22: the Disk Quotas page, 200, 3,189 B).

## The media-fulfilment surfaces that do serve bytes

Four of them are usable, and the per-file number is the finding.

Payhip states "no storage or bandwidth limits" with a 5 GB per file cap. Nexus Mods states
"Unlimited storage and distribution for mods and images that you create" with a 20 GB per
file cap. Gumroad allows a 20 GB single file on any product priced above USD 0.99. Sellfy
allows 50 files per product.

Printables is the one measured object in this group: a single 1,036,822,737 B STL, which is
1.037 GB decimal and 0.966 GiB binary, served from `files.printables.com` with an MD5 match
(`documented`, 2026-10-21). A "1 GB" figure understates it.

Apple Books is the other one worth a note. Its widely cited 2,048 MB per-file cap comes from
a third-party store-limit table rather than an Apple page, so the number is `reported` rather
than `documented`, and the row says so.

### 24242.io, public Blossom blob server (Nostr)

> No account, no quota, no total cap stated, 'Free and unrestricted... with no warranties... for now.' Per-file 100 MiB. First person to upload an object owns it (SHA-256 addressed)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MiB/file. A new account costs anonymous. Observed behaviour: 60-day access-decay retention makes this an ephemeral tier, not an archive.

Evidence: `https://24242.io` (2026-10-21), record `dossier/storage/24242-io-public-blossom-blob-server.json`.
Verdict: `qualifies-with-caveat`.

### blossom.ditto.pub (Ditto Blossom server)

> No quota. Live server stats: 1,375,309 total blobs, 781.96 GB storage used, 8,684 uploads/24 h. Max upload size 2 GB, max media size 1 GB, accepted types `*`

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 2 GB/upload. A new account costs anonymous. Observed behaviour: Operator-run hobby infrastructure with ~782 GB on disk.

Evidence: `https://blossom.ditto.pub` (2026-10-21), record `dossier/storage/blossom-ditto-pub.json`.
Verdict: `qualifies-with-caveat`.

### Macaulay Library / eBird (Cornell Lab of Ornithology)

> No published per-account byte quota, tens of millions of assets, and Cornell explicitly positions it as backup: 'the archive serves as your personal cloud storage and backup of your media files.' Capacity is bounded by per-file and...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB/file. A new account costs institution. Observed behaviour: Classic rule-2 pattern: upload-open, read-gated.

Evidence: `https://www.macaulaylibrary.org` (2026-10-21), record `dossier/storage/macaulay-library-ebird.json`.
Verdict: `qualifies-with-caveat`.

### Mapillary (Meta)

> 'unlimited storage' per Mapillary's own blog: 'Mapillary offers unlimited storage and makes imagery publicly available... any organization, public or private, can store and host their archive of street-level imagery at no cost.' No...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: 50,000 requests/minute/app. A new account costs institution. Observed behaviour: Upload-open / read-gated is the exact pattern in rule 2: storage is unlimited but pulling an archive back out at volume is throttled to 50k tile requests/day.

Evidence: `https://www.mapillary.com` (2026-10-21), record `dossier/storage/mapillary.json`.
Verdict: `qualifies-with-caveat`.

### OpenAerialMap (HOT / Open Imagery Network)

> Free hosting for anyone with nowhere to publish. The rewrite of the uploader is explicitly scoped to 'Handle files up to 100GB with resume capability, using S3 multipart upload with presigned URLs (direct browser-to-S3)'. No per-account...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 GB/file. A new account costs institution. Observed behaviour: The uploader was historically unreliable for large files and is mid-rewrite by a UC Berkeley Code-for-Good team (Spring 2026), so the 100 GB target is a workplan goal, not a shipped.

Evidence: `https://imagery.hotosm.org/contribute` (2026-10-21), record `dossier/storage/openaerialmap.json`.
Verdict: `qualifies-with-caveat`.

### Panoramax, OSM-FR instance (panoramax.openstreetmap.fr)

> NO QUOTA ANYWHERE IN THE SERVER. There is no quota code, no quota column in the DB migrations, and no quota endpoint, because the feature does not exist. A contributor filed Feature Request #334 '(Feature Request) Disable uploads when less...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 18 MB per 96 MP photo. A new account costs institution. Observed behaviour: Volunteer hardware with ZFS RAIDZ2 + daily remote snapshots.

Evidence: `https://panoramax.openstreetmap.fr` (2026-10-21), record `dossier/storage/panoramax-osm-fr-instance.json`.
Verdict: `qualifies`.

### Panoramax federation, 25 instances with per-instance `registration_is_open` (ulm / osm-es / see

> No quota on any instance (same codebase, same absence of a quota mechanism). The federation catalog itself is the useful artifact: `GET /api/instances` returns all 25 instances WITH each one's live configuration, including...

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: open=False on 11 of 25 instances (multimodall, bikespace, nl-test, osm-fulda, vee, multimob, serenedeluge, burakonder, mapcomplete, osm-tw).

Evidence: `https://api.panoramax.xyz/api/instances` (2026-10-21), record `dossier/storage/panoramax-federation-25-instances-with-per-instance-regi.json`.
Verdict: `qualifies`.

### Wikimedia Commons

> NO TOTAL QUOTA, read verbatim from Commons:Maximum_file_size: 'there is no limit to the *total* size of uploads by an individual account.' Per-file cap is 5 GiB (5,368,709,120 bytes) via chunked upload, 100 MiB otherwise. Live API...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GiB/file. A new account costs institution. Observed behaviour: The one platform here where a multi-TB batch is explicitly contemplated, Commons asks the uploader to warn sysadmins before 'batch uploads amounting to several TB'.

Evidence: `https://commons.wikimedia.org` (2026-10-21), record `dossier/storage/wikimedia-commons.json`.
Verdict: `qualifies-with-caveat`.

### archive.org /download web serving path (the free CDN)

> Serving is unmetered and free; no per-file download cap and no egress fee. Practical ceiling is throughput, not quota

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Throughput is the binding constraint, not quota: observed 1.19 MB/s on one 90s stream and 1.66 MB/s aggregate across 8 parallel range requests to one datanode from one IP (~145 GB/day).

Evidence: `https://archive.org/download/<identifier>/<filename>` (2026-10-21), record `dossier/storage/archive-org-download-web-serving-path.json`.
Verdict: `qualifies-with-caveat`.

### IAS3 old-version retention (x-archive-keep-old-version)

> No quota of its own, it multiplies the 1TB item limit by however many versions you PUT. 'Saved versions will be placed in history/files/$key.~N~'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1TB item. The record states no identity cost. Observed behaviour: Unofficial-ish surface: documented but not exposed by any major client, so it is untested at scale and easy to orphan copies with.

Evidence: `https://archive.org/developers/ias3.html` (2026-10-21), record `dossier/storage/ias3-old-version-retention.json`.
Verdict: `qualifies-with-caveat`.

### iiif.archive.org (free IIIF Image API over any uploaded image)

> No separate quota, it is a free image server over items you already hold, one image per item. Capacity therefore follows the 1TB/item rule

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-object-cap`: 1TB/item. The record states no identity cost. Observed behaviour: Third-party workshop doc, not IA's own page.

Evidence: `https://iiif.archive.org/iiif/` (2026-10-21), record `dossier/storage/iiif-archive-org.json`.
Verdict: `qualifies-with-caveat`.

### Internet Archive BitTorrents (webseed swarm)

> Free, unlimited distribution; ~1.4 million items already torrented, 'comprising almost a petabyte of public domain materials'. Egress is unbounded because the swarm and webseeds share the load

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Old torrents for a mutated item loop forever re-downloading mismatched pieces.

Evidence: `https://archive.org/details/torrents` (2026-10-21), record `dossier/storage/internet-archive-bittorrents.json`.
Verdict: `qualifies-with-caveat`.

### Blomp (AIN/Blomp Cloud Storage)

> 40 GB free on signup, advertised and confirmed as 'Get Up to 400 GB for Free', +40 GB per friend who joins and stays active, i.e. 40 GB x 10 referrals = 400 GB. Referral ceiling 400 GB is a hard stop on a single account; past that you buy...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: invited account must log in at least once a year or the granter loses the.... A new account costs email. Observed behaviour: Two independent red flags: a nodeloc poster notes Blomp 'literally copied pCloud's marketing copy' and later changed it.

Evidence: `https://www.blomp.com/` (2026-10-21), record `dossier/storage/blomp.json`.
Verdict: `qualifies`.

### Jottacloud (Norway)

> 5 GB free. 'Unlimited*' Personal at USD 12.99/mo or USD 129.90/yr, with the asterisk being 'upload speed gradually reduced after 5 TB'. Home 1 TB NOK 79/mo, Pro up to 50 TB

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: upload speed throttled above 5 TB, described by HN as a 'harsh inflection'.... A new account costs email. Observed behaviour: Long-running, well-documented provider.

Evidence: `https://jottacloud.com/en/pricing` (2026-10-21), record `dossier/storage/jottacloud.json`.
Verdict: `qualifies-with-caveat`.

### PikPak

> 6GB free; 10TB on Premium ("Free accounts include 6 GB of storage, and Premium includes 10 TB")

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: inactive 12 months are deleted (effective 20. The record states no identity cost. Observed behaviour: Download links are bound to the requesting IP/CIDR, so a CDN or multi-node serving layer breaks.

Evidence: `https://mypikpak.com` (2026-10-21), record `dossier/storage/pikpak.json`.
Verdict: `qualifies-with-caveat`.

### Apple Books (iTunes Connect / Partner)

> 2 GB per book file, per the widely-cited store-limit table (Apple Books 2 GiB). Vendor page does not publish a per-file number in the fetchable docs

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-object-cap`: ~2 GB (secondary source only). A new account costs email. Observed behaviour: Apple requires a tax ID / banking setup and an Apple ID with 2FA.

Evidence: `https://itunespartner.apple.com/books/` (2026-10-21), record `dossier/storage/apple-books.json`.
Verdict: `qualifies-with-caveat`.

### DLsite (circle / web upload)

> 10GB (10 GB per work) via web upload; '10GB' (works over 10 GB can still be handled, by arrangement). Accepted formats zip/rar/7z, and files over 4 GB must be RAR or 7-Zip

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 GB web / larger on request. A new account costs email. Observed behaviour: Circle registration requires a payout bank account and, for paid sales, My Number (individual number) registration, so while the ID itself is email-based, monetisation is national-id gated.

Evidence: `https://www.dlsite.com/circle/circle/webup` (2026-10-21), record `dossier/storage/dlsite.json`.
Verdict: `qualifies-with-caveat`.

### Google Play Books Partner Center

> 2 GB per content file ('Each file must be less than 2 GB. This limit includes cover image files'); audiobook audio files under 100 MB each, but multiple parts allowed plus ZIP

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 2 GB. A new account costs email. Observed behaviour: Payout requires tax/payment setup.

Evidence: `https://support.google.com/books/partner/answer/3424254` (2026-10-21), record `dossier/storage/google-play-books-partner-center.json`.
Verdict: `qualifies-with-caveat`.

### Gumroad

> Own help centre: 'If you price your product at any number greater than $0.99, the largest single file that you can upload to a product is 20 GB in size... you can add as many files as you want to each product.' Free/$0 products are capped...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 GB (products >$0. A new account costs email. Observed behaviour: Purchases require a payment method on the seller side to withdraw, but uploading does not.

Evidence: `https://gumroad.com` (2026-10-21), record `dossier/storage/gumroad.json`.
Verdict: `qualifies-with-caveat`.

### Nexus Mods

> Vendor help page states it outright: 'Unlimited storage and distribution for mods and images that you create. Unlimited file hosting for mods and images that you've created and uploaded.' Their own wiki table: Maximum Storage...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 GB via browser, larger by request. A new account costs email. Observed behaviour: The 1, 1.5 MB/s un-premium cap is the real constraint, ~3.5, 5 GB/hour per stream, so per-IP-shaping governs, not storage.

Evidence: `https://www.nexusmods.com` (2026-10-21), record `dossier/storage/nexus-mods.json`.
Verdict: `qualifies-with-caveat`.

### Payhip

> Explicit, from their own page: 'No, we have no storage or bandwidth limits. We only have a 5GB per file limit.' Help centre repeats: 'Payhip supports a maximum file size of 5GB per digital product.'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GB, the only limit they publish. A new account costs email. Observed behaviour: Serving path is fine.

Evidence: `https://payhip.com` (2026-10-21), record `dossier/storage/payhip.json`.
Verdict: `qualifies`.

### Printables (Prusa Research)

> No published account quota and no published upload cap. Verified live object: a single 1,036,822,737 B (1.037 GB) STL served from files.printables.com. Also verified a model holding 29 files totalling 404.3 MB, and one holding six ZIPs of...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1.037 GB. A new account costs email. Observed behaviour: TOS 2.9 states plainly 'PRINTABLES does not serve as data storage' and disclaims liability for deletion, treat durability as unguaranteed.

Evidence: `https://www.printables.com` (2026-10-21), record `dossier/storage/printables.json`.
Verdict: `qualifies`.

### Sellfy

> Their own sell-downloads page: 'Upload unlimited eBooks, music, software, courses, or other digital products packing up to 50 files per product, with each file weighing in at up to 20GB.' FAQ repeats: 'As many as you want! There are no...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 GB. A new account costs email. Observed behaviour: No free tier, plans start at $22/mo with a 14-day trial, so it is paid-only.

Evidence: `https://sellfy.com` (2026-10-21), record `dossier/storage/sellfy.json`.
Verdict: `qualifies-with-caveat`.

### Fedora COPR (copr.fedorainfracloud.org)

> No published storage quota, unlimited projects and builds for Fedora Account holders, but retention, not size, is the constraint: 'We keep one build for each package in one project indefinitely. All other builds (old packages, failed...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: deleted after 14 days. The record states no identity cost. Observed behaviour: Reliable and Fedora-funded, but the pruner is the whole story: unused artefacts disappear by design, so it is a distribution channel, not storage.

Evidence: `https://copr.fedorainfracloud.org` (2026-10-21), record `dossier/storage/fedora-copr.json`.
Verdict: `qualifies-with-caveat`.

### Hackage (hackage.haskell.org)

> No published per-package or total quota found on the upload page or the server API. Uploads are permanent: 'Upload and publish a package permanently' and 'You can only upload a package version once and this cannot be undone'. Real large...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Immutable by design - a bad upload cannot be deleted, which is irreversibility risk in the other direction.

Evidence: `https://hackage.haskell.org` (2026-10-21), record `dossier/storage/hackage.json`.
Verdict: `qualifies-with-caveat`.

### Launchpad PPA (Ubuntu Personal Package Archive)

> 8 GiB of disk per PPA by default ('Disk space | 8 GiB; larger quotas considered on request'), and multiple PPAs per person or team ('Every individual and team in Launchpad can have one or more PPAs, each with its own URL'). Quota increases...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Very stable, data persists until removed.

Evidence: `https://launchpad.net` (2026-10-21), record `dossier/storage/launchpad-project-file-releases.json`.
Verdict: `qualifies-with-caveat`.

### openSUSE Build Service (OBS) - build.opensuse.org, public instance

> No published storage quota at all. The service is 'currently free for use' and 'anybody can build packages'; the only quotas in the codebase are per-project PACKAGE-COUNT quotas read from an admin quota.xml, not byte quotas. Published...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Very stable (SUSE/openSUSE-funded, ~30k users, 140k packages).

Evidence: `https://openbuildservice.org` (2026-10-21), record `dossier/storage/opensuse-build-service-build-opensuse-org-public-instanc.json`.
Verdict: `qualifies`.

### Snap Store (api.snapcraft.io / snapcraft.io)

> No published total-storage quota and no published per-snap byte cap; the practical ceiling is what the upload tooling survives. Evidence of real large artefacts: `kicad` stable snap is 1,659.5 MB and `android-studio` is 1,657.8 MB in the...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5.5 GB upload. The record states no identity cost. Observed behaviour: The write path is the weak link.

Evidence: `https://snapcraft.io/store` (2026-10-21), record `dossier/storage/snap-store.json`.
Verdict: `qualifies-with-caveat`.

### Software Heritage Archive (CAPI read side) + Save Code Now (anonymous crawl trigger)

> No storage quota is imposed on the depositor, because the depositor never uploads bytes. The archive stores content-addressed git objects from public repositories, deduplicated by sha1_git, and growth is the Foundation's problem, not...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: (deposit only): 100 MiB documented, 200 MiB default in swh-deposit config. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Read path is reliable but rate-shaped: 120 req/window/IP will throttle a naive tree walk of an archive of 20 TiB - parallelise across IPs or batch directory listings.

Evidence: `https://archive.softwareheritage.org` (2026-10-21), record `dossier/storage/software-heritage-archive-save-code-now.json`.
Verdict: `qualifies-with-caveat`.

### Dailymotion

> No total storage cap stated. Per-account upload policy: 4 GB per file, 2 hours per file, 15 videos per 24 hours, 10 hours of content per 24 hours (standard creators). Premium/Edge lifts to 64 GB/file and unlimited duration

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 4 GB per file. The record states no identity cost. Observed behaviour: Exceeding either the count or duration limit suspends uploads for 24 hours.

Evidence: `https://www.dailymotion.com` (2026-10-21), record `dossier/storage/dailymotion.json`.
Verdict: `qualifies-with-caveat`.

### Odysee / LBRY

> No storage quota at all. 16 GB per file via the Odysee uploader (4 GB from the plain lbry.com web form). Unlimited claims. Storage cost is a one-time LBC claim deposit, minimum 0.0001 LBC

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 16 GB per file. The record states no identity cost. Observed behaviour: This is the only candidate here that stores the original bytes, but the platform is visibly decaying in 2026, community 'collapse watch' posts and a Sept 2026 outage report.

Evidence: `https://odysee.com` (2026-10-21), record `dossier/storage/odysee-lbry.json`.
Verdict: `qualifies`.

### PeerTube, peertube.cif.su (open registration, unlimited quota)

> Unlimited total quota (`user.videoQuota: -1`), 5 GiB per day (`videoQuotaDaily: 5368709120`). Registration open, no approval, no email verification

That is the record's own wording (`reported`, 2026-10-21). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Volunteer-run instances disappear without notice, a single admin's disk decision deletes the archive.

Evidence: `https://peertube.cif.su` (2026-10-21), record `dossier/storage/peertube-peertube-cif-su.json`.
Verdict: `qualifies-with-caveat`.

### PeerTube, hittube.fr (open registration, 50 GiB per user, no daily cap)

> 50 GiB per user and no daily upload cap: `user.videoQuota: 53687091200` and `user.videoQuotaDaily: -1`, with registration open and no email verification required

That is `measured` from `hittube.fr/api/v1/config` (2026-10-22), record `dossier/storage/peertube-hittube-fr.json`. The instance is HitTube, PeerTube 8.3.1, in France, with two registered users and 201 local videos totalling 21,058,245,956 bytes.

⚠ **The quota is the smaller half of the finding.** The same config sets `transcoding.alwaysTranscodeOriginalResolution: true` with 720, 1080 and 2160 enabled, so every upload is re-encoded at its own resolution and what comes back is a transcode, not the bytes that went in. **50 GiB that returns a renditions set is a video host and not storage.**

The two PeerTube instances are the useful comparison because their quota shapes are opposite: `peertube.cif.su` reports unlimited total with a 5 GiB daily cap, and this one reports 50 GiB total with no daily cap. Neither shape is a PeerTube default; both are per-instance policy set by whoever runs the box.

Verdict: `qualifies-with-caveat`, binding `per-object-cap`.

### Rumble

> No published total storage cap. 15 GB per file standard, 30 GB for Premium/monetised channels; up to 8 hours duration

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-object-cap`: 15 GB/file. The record states no identity cost. Observed behaviour: rumble.com/faq returned 404/504/410 on three fetch attempts from this network.

Evidence: `https://rumble.com` (2026-10-21), record `dossier/storage/rumble.json`.
Verdict: `qualifies-with-caveat`.

### Vimeo (Free plan)

> Unlimited storage for public, non-embeddable videos; 3 GB total for embeddable and non-public videos. This is a 2024-onwards rewrite of the old '500 MB/week' rule, the weekly quota now applies only to legacy paid Plus/Pro accounts, not Free

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200 GB per file. The record states no identity cost. Observed behaviour: The killer is not quota.

Evidence: `https://vimeo.com` (2026-10-21), record `dossier/storage/vimeo.json`.
Verdict: `qualifies-with-caveat`.

### YouTube (unlisted), with DCT/fountain-coded payload

> No total storage cap. Per-upload max 256 GB or 12 hours, whichever is less. Unverified accounts are limited to 15-minute videos; phone verification lifts that

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: max 256 GB. The record states no identity cost. Observed behaviour: From a datacenter IP, yt-dlp hit `Sign in to confirm you're not a bot` on 2 of 3 observed videos and HTTP 429 on the watch page.

Evidence: `https://www.youtube.com` (2026-10-21), record `dossier/storage/youtube-with-dct-fountain-coded-payload.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| iNaturalist | fails-quota | No per-account quota published or enforced (395,436,915 observations live at time of observed)... |
| OpenStreetMap GPS traces (openstreetmap.org/traces) | fails-quota | No published per-user quota and no quota endpoint; storage is GPX-only and appended to the OSM rails DB + a trace store... |
| Zooniverse (Panoptes) | fails-quota | Stores contributor *classifications*, not contributor *uploads*... |
| Item Metadata API (MDAPI) as free key-value/JSON store | fails-quota | No per-item metadata size is published; unlimited items x one JSON doc each, transaction-safe, free |
| Wayback Machine, Save Page Now 2 (capture API) | fails-quota | No storage quota; the cap is per-object at 2GB ('Max resource size = 2GB') and 100,000 captures/day for authenticated users... |
| FileLu | fails-quota | 1 GB free; +20 GB by leaving reviews (support ticket); referral rewards '100 referrals gives you 100GB'... |
| MediaFire | fails-quota | 10 GB free (Basic, ad-supported); 1 TB paid at $5.83/mo annual |
| myQNAPcloud Storage | fails-quota | 16 GB free with any QNAP ID, no trial period, no file-size minimum. Paid starts $0.99/month... |
| Boosty (RU) | fails-egress | 20 GB per attached video (official FAQ post: ' 20 '). Community reports the effective limit was cut to 1 GB at one point... |
| BOOTH (pixiv) | fails-quota | 1.2 GB per file (raised from 1 GB on 2026-03-09), 10 GB total per shop; storage add-on CNY 540/month per extra block |
| Fourthwall | fails-quota | 1 GB per listing (all files counted together) on paid/members-only products... |
| IngramSpark | fails-egress | 1.5 GB via web upload ('web upload for files up to 1.5 GB, zip/stuff compression accepted')... |
| Ko-fi Shop | fails-quota | Free: 25 GB total asset storage, 2 GB per shop item. Standard/Gold: 200 GB total, 5 GB per item |
| Lulu | fails-egress | No hard file limit. Own help page: 'We technically do not have a file limit for projects... |
| (mbd.pub) `面包多` | fails-identity | Their help centre says '(<1G)', unlimited file hosting, with a per-file note of <1 GB. So: unlimited total, 1 GB per object |
| AUR (Arch User Repository) | fails-quota | Not a storage candidate at all: the AUR enforces a hard maximum blob size of 250 KiB per git object... |
| Cachix (Nix binary cache hosting) | fails-quota | 5 GB free for open-source projects: 'Users have a free 5 GB limit for open source projects and 20 Cachix Deploy agents.'... |
| Chocolatey Community Repository | fails-quota | 200 MB hard per package: 'NOTE: 200MB is the maximum size of a package on the Chocolatey Community Repository... |
| Clojars (repo.clojars.org) | fails-quota | No published byte quota on the site pages read. A 2020-era project commit records an 81 MB uberjar being rejected as 'too... |
| CRAN (Comprehensive R Archive Network) | fails-quota | Deliberately tiny, by policy. CRAN policy: 'As a general rule... |
| CTAN (Comprehensive TeX Archive Network) | fails-quota | No numeric quota published, but upload is a *manual web form* reviewed by the CTAN team... |
| Debian snapshot archive (snapshot.debian.org) | fails-quota | No user quota because there is no user write path - snapshot ingests the Debian archive itself... |
| F-Droid (f-droid.org/repo APK archive) | fails-quota | No published total or per-app byte quota. The archive is large and browsable: index-v2.json is 66,480,070 bytes and a... |
| Flathub (dl.flathub.org OSTree repo) | fails-quota | No published storage quota for published applications. This is a deduplicating OSTree/OCI repo: apps are stored as... |
| JitPack (jitpack.io) - build-on-demand Maven from git | fails-quota | Bounded by the size of the git repo it builds from, not by a storage quota: a build fails with 'Git error... |
| Maven Central (Sonatype Central Portal) - post-2026... | fails-quota | Maven Central introduced hard monthly *publishing* limits per organization in 2026. Three independent metrics: file count... |
| BitChute | fails-quota | No published total cap; free-tier per-file upload limit reported around 2 GB... |
| Loom (Atlassian) | fails-quota | Free Starter: up to 25 recordings per person, 5 minutes per video, 50 members. Not a storage quota, a recording-count quota |
| Streamable | fails-quota | 250 MB per file, 10 minutes per video on the free plan. No storage pool, the unit is the individual clip |
| Vidyard (Free) | fails-quota | Free: 5 recorded videos per month, 25 videos in the library at once... |

Three failure modes dominate, and one of them is unique to this class.

`quota` is the largest group, and it is unremarkable: a platform that caps a file below the
floor or an account below 500 GB.

`not-storage` is the interesting one, and it is why this document exists. A print-fulfilment
service with unlimited ingress and no read path, a video platform that re-encodes, a
metadata index that holds no bytes, and a photo site that is a shop window rather than a
drive are all in this group. They are not small. They are the wrong shape, and a reader who
finds one of them by searching for "unlimited storage" will otherwise chase it.

`write-gated` covers the software archives and the scientific databases, where a curator, a
build recipe or a review stands between the reader and a write.

## Chaining

The Archive is the durable anchor of a free pool, and it is the one member whose funding
model predicts a decade rather than a quarter. Two rules follow.

Pair it with a host whose retention clock is short and whose per-object cap is large, so the
short-lived copy absorbs the write burst while the Archive's queue drains. The Archive's
write path is a queue with a global derive step, and a backlog can stall uploads for hours.

Use the torrent as a serving path where the item is public. It costs nothing, it does not
touch the per-IP shaping, and it is the only free egress channel in this corpus that
multiplies with readers rather than dividing.
