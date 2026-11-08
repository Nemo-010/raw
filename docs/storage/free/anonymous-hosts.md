# Anonymous hosts: what accepts bytes with no account at all

This is the class with no registration gate, and it is the only one where the identity
cost is genuinely zero. The providers here accept an upload from anyone, return a URL, and
hold the bytes for some period. None of them can be enumerated by its owner, so
the manifest is the uploader's, and losing it loses the data even when the bytes are still
there.

The 33 qualifying records cover five sub-classes: file hosts built for anonymity, audio
and podcast hosts, image hosts, document hosts, and hosts found through non-English
forums. The distinctions that matter are the per-object cap and the retention, and they are
separate columns in every table here.

## The comparison

Sorted by what the class is for: anonymous file hosts first, then media, then images, then
forum finds. A `*` in the identity column means the value is read off the record's own
prose rather than from its `identity_cost` field, which is empty for most of
this class. A dash means neither recorded one.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Buzzheavier | no account, NO per-file size cap; activity-based retention that can become permanent | - | anonymous* | qualifies-with-caveat |
| CyberDrop | Not stated numerically, 'Will you keep my files forever? Yes'... | - | - | qualifies-with-caveat |
| Pixeldrain | 'No storage limit' on the free tier (also on Pro and Prepaid)... | per-object-cap: 10 GB per file | - | qualifies-with-caveat |
| Streamtape | 'Unlimited Storage, Upload as many Videos as you wish. Active files will be saved' | - | - | qualifies-with-caveat |
| ZeroFS | Unlimited storage for active files; no file size limit | retention-clamped: inactive for 15 days are deleted, the shortes | - | qualifies-with-caveat |
| Audiomack | Unlimited uploads, free forever: 'Audiomack is a FREE... | per-object-cap: 250 MB per file | - | qualifies-with-caveat |
| Audius (Open Audio Protocol)... | 'There is no limit to the number of tracks you can upload to your Audius profile' and... | per-object-cap: 2 GB per track | anonymous* | qualifies |
| Bandcamp, free artist account | 291 MB per track to start ('It starts out at 291MB per track... | per-object-cap: 291 MB per track | - | qualifies-with-caveat |
| Castbox Creator Studio | 'There is no limit on uploading storage (total) for a channel.' Per-file cap 400 MB... | per-object-cap: 400 MB per file | - | qualifies-with-caveat |
| Freesound, Creative Commons sound library... | 1 GB per upload batch ('there is a file size upper limit of 1GB... | per-object-cap: 1 GB per upload | - | qualifies-with-caveat |
| hearthis.at, free tier | 400 MB per week, reset Sunday 19:00 CET: 'Upload up to 400 MB of music each week for... | - | - | qualifies-with-caveat |
| Jamendo (artist upload) | No published per-account total; 480 MB per file, lossless only (WAV/FLAC/AIFF... | per-object-cap: 480 MB per file | - | qualifies-with-caveat |
| Mixcloud, Basic tier (unlimited drafts) | 10 published shows (>15 min) + 10 published tracks... | per-object-cap: 4 GB max per show file | - | qualifies-with-caveat |
| RedCircle, Core (free) plan | Unlimited. Core is 'our entirely free option... | per-object-cap: 200 MB per audio file | - | qualifies-with-caveat |
| RSS.com, Free plan | Unlimited. Free plan: 'Unlimited episodes and unlimited audio, with no storage cap'... | per-object-cap: 2 GB per episode | - | qualifies-with-caveat |
| Spotify for Creators (formerly Anchor) | Free hosting with no stated numeric cap. Spotify's own episode-publishing doc: 'We... | - | - | qualifies-with-caveat |
| Spreaker, Free plan | One podcast, unlimited episodes: 'The free plan allows users to have one podcast with... | - | - | qualifies-with-caveat |
| Zencastr, free hosting | Advertised as no cap: 'No episode caps, no storage limits... | - | - | qualifies-with-caveat |
| AnyFlip (flipbook PDF host) | FREE plan: 100 GB storage, unlimited number of publications, 5 uploads/day... | request-rate: 5 uploads/day free (60/day Pro) | - | qualifies-with-caveat |
| Internet Archive (IAS3 / petabox item upload) | 1 TB hard limit per item page ("Currently, there is a 1TB size limit for item pages")... | per-object-cap: 1 TB/item | - | qualifies |
| 1fichier, registered free account... | Registered (free) tier: '5 TB of temporary storage', folder sharing, remote upload... | retention-clamped: Retention: 30 days after upload, or 90 days | email | qualifies-with-caveat |
| Evolution Host, $0.00 lifetime VDS, 1 TB NVMe... | 1 TB NVMe, 128 GB DDR5 RAM, 16 cores @ 5 GHz, DDoS protected, $0.00 'lifetime'... | write-gated: reviewed for SEO value | email | qualifies-with-caveat |
| ImgBB | Unlimited/indefinite storage for free accounts... | - | - | qualifies |
| Postimages (postimages.org / postimg.cc) | No storage cap stated: 'we do not impose strict limits on our users... | per-object-cap: 32 MB/file | - | qualifies-with-caveat |
| Telegraph (telegra.ph) | Unlimited pages and unlimited uploaded images... | - | anonymous* | qualifies-with-caveat |
| 88file.jp `八八ファイル便` | Claims (unlimited-capacity file transfer, free) and, no send-volume limit, free... | - | - | qualifies-with-caveat |
| ACdata (ac-data.info) | Two products on one site. Transfer: '1 25065', unlimited total, 250 GB per file... | per-object-cap: 250 GB | - | qualifies-with-caveat |
| AllFiles.org | 'Upload, store, and send files up to 200 GB for free', 100 GB per file... | per-object-cap: 100 GB | anonymous* | qualifies-with-caveat |
| Axfc Uploader (axfc.net) `あぷろだ` | No account, no total quota, per-object only. '1128 GiB' (max 128 GiB per file... | per-object-cap: 128 GiB | anonymous* | qualifies-with-caveat |
| BigFile.net | No account and no published total quota, storage is per-object and unbounded in count... | per-object-cap: 256 GB | anonymous* | qualifies |
| GigaWatasu (giga-watasu.jp) (`ギガワタス`) | 333 GB per file, no registration. Registered free members additionally get 111-day... | per-object-cap: 333 GB | - | qualifies-with-caveat |
| MrOwl (mrowl.com) | 'free unlimited storage for content that is shared to the world' + 10 GB private... | per-object-cap: 20 MB on the unlimited public tier | - | qualifies-with-caveat |
| U.UA (u.ua) | 50 GB per file, unlimited file count, no registration, 7 days storage | per-object-cap: 50 GB | anonymous* | qualifies-with-caveat |

## What the class is

An anonymous host is a transfer bus with a long stop. It takes a large object and keeps it
for a period set by its own business model rather than by the uploader's request. That is why
the per-object caps here are the largest in this topic and the retention is the shortest:
file.kiwi takes 999 GiB and deletes it after 90 hours, and firestorage.jp takes 300 GiB and
deletes it after 3 days by default, 14 at most. The two numbers belong on the same row, and a table that shows
only the cap has turned a 90-hour buffer into an archive.

The class also splits by whether it re-encodes. A host that transcodes at ingest is not
storage, because it does not return the bytes it was given. In the video lane only Odysee
and PeerTube return originals, and in the audio lane only Audius does. Every podcast host
in this document either re-encodes or caps the episode at a size that makes it irrelevant
here.

## The three hosts that carry the class

Three of the 33 do the work, and each one carries a different caveat.

**BigFile.net** is the only large per-object cap with zero registration: 256 GB, no
account, no published total. Its API has three requirements that cost an hour to discover.
It needs an `Origin` or `Referer` header, and without one it returns
`403 {"status":false,"message":"来源验证失败"}`. Its `Hash` header carries the SHA-256 in
base62 rather than hex. And its `Content-Range` value must be bare: `0-65535` returns 200
with `{"status":true}`, while the RFC-7233 form `bytes 0-65535/65536` returns 500 with
`{"status":false,"message":"上传失败"}`. A 65,536-byte roundtrip was byte-identical on
2026-10-22 (`measured`), and a ranged read returned 206 with
`Content-Range: bytes 0-1023/65536`.

Because there is no account, nothing can enumerate or restore the data. The manifest is
mandatory, not convenient, and it is the only object in this class the uploader must keep.

**axfc** is the oldest thing in this topic, at 22 years, and the form constant is exact:
`max="137438953472"`, which is 128 GiB to the byte (`inferred`, 2026-10-22). It has no
published total quota and no account to hold one. Programmatic use means driving a form
rather than calling an API, and the site's age is the strongest reliability signal any
anonymous host here has.

**GigaFile** is the cleanest anonymous host for one large object: 300 GB per file, no count
limit, no registration, and seven retention bands from 3 to 100 days chosen at upload
(`documented`, 2026-10-22: the page description reads "3 days to 100 days, seven selectable
retention periods" and "300G per file"). The band is the uploader's choice rather than a clock nobody
published, which makes it the one host in this class where the retention is a decision
rather than a risk. It still is not storage, because 100 days is the maximum.

## What the caps do to an archive of 20 TiB

The arithmetic decides whether any of this is a shard plan or a curiosity.

At BigFile.net's 256 GB, 20 TiB is 80 objects. At GigaFile's 300 GB it is 70. At axfc's
128 GiB it is 160. Those are workable counts, and the constraint that kills them is not the
object size: it is that GigaFile deletes after at most 100 days and BigFile.net on a
365-day sliding window. An archive of 20 TiB spread over 80 objects needs a keep-alive loop that
touches every one of them inside the window, and a loop that fails once loses the object.

The image hosts are not part of that arithmetic. At 32 MB per file an archive of 20 TiB is
655,360 objects, and no host in this class offers a batch API that could carry the count.

## The providers, one section each

### Buzzheavier

> no account, NO per-file size cap; activity-based retention that can become permanent

That is the record's own wording (`reported`, 2026-10-21). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: CRITICAL: upload is fully scriptable but the read path is Cloudflare-challenged, which breaks an automated fetch workload unless a CF-solving client or proxy is inserted.

Evidence: `https://buzzheavier.com` (2026-10-21), record `dossier/storage/buzzheavier.json`.
Verdict: `qualifies-with-caveat`.

### CyberDrop

> Not stated numerically, 'Will you keep my files forever? Yes'. No published storage ceiling found; account creation is unverified and email-less

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Retention claims 'forever' and has been stable for years, but the extension allowlist and account-wide purge on a single CSAM hash match are real technical failure modes.

Evidence: `https://cyberdrop.cr` (2026-10-21), record `dossier/storage/cyberdrop.json`.
Verdict: `qualifies-with-caveat`.

### Pixeldrain

> 'No storage limit' on the free tier (also on Pro and Prepaid); per-file cap 10 GB free / 100 GB paid

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 GB per file. The record states no identity cost. Observed behaviour: operator explicitly says free storage is not for backups and has wiped data of accounts that exceeded the limit before.

Evidence: `https://pixeldrain.com` (2026-10-21), record `dossier/storage/pixeldrain.json`.
Verdict: `qualifies-with-caveat`.

### Streamtape

> 'Unlimited Storage, Upload as many Videos as you wish. Active files will be saved'

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Re-encoding destroys byte fidelity, so it cannot store arbitrary binaries.

Evidence: `https://streamtape.com` (2026-10-21), record `dossier/storage/streamtape.json`.
Verdict: `qualifies-with-caveat`.

### ZeroFS

> Unlimited storage for active files; no file size limit

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: inactive for 15 days are deleted, the shortes. The record states no identity cost. Observed behaviour: Very new, looks like a Buzzheavier-style clone (same 'we only act on local court orders' posture, same lost-ID-never-recovered model).

Evidence: `https://zerofs.link` (2026-10-21), record `dossier/storage/zerofs.json`.
Verdict: `qualifies-with-caveat`.

### Audiomack

> Unlimited uploads, free forever: 'Audiomack is a FREE, limitless music sharing and discovery platform'; 'Whether you have 1 song or 1,000, Audiomack lets you host it all for free. No premium creator accounts ever!'. Per-file cap 250 MB...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 250 MB per file. The record states no identity cost. Observed behaviour: Streaming-only platform: no original-file download path was found, so the payload is retrievable only as a transcode or not at all.

Evidence: `https://audiomack.com` (2026-10-21), record `dossier/storage/audiomack.json`.
Verdict: `qualifies-with-caveat`.

### Audius (Open Audio Protocol), original file is served byte-for-byte

> 'There is no limit to the number of tracks you can upload to your Audius profile' and 'no limit on the duration of your tracks'; per-upload file size cap is 2 GB. Unlimited tracks x 2 GB = unbounded, free, no paid tier exists

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 2 GB per track. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: No transcoding on the download path.

Evidence: `https://audius.co` (2026-10-21), record `dossier/storage/audius-original-file-is-served-byte-for-byte.json`.
Verdict: `qualifies`.

### Bandcamp, free artist account

> 291 MB per track to start ('It starts out at 291MB per track... Once you've made a few sales through Bandcamp (totaling $20 USD or more), we increase the max per-track upload size to 600 megs'), and crucially 'There is no limit on the size...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 291 MB per track. The record states no identity cost. Observed behaviour: Lossless masters are kept and fans who buy get the original format.

Evidence: `https://bandcamp.com` (2026-10-21), record `dossier/storage/bandcamp-free-artist-account.json`.
Verdict: `qualifies-with-caveat`.

### Castbox Creator Studio

> 'There is no limit on uploading storage (total) for a channel.' Per-file cap 400 MB, from a help page last updated 7 years ago ('Updated: 7 years ago'), the 400 MB figure is stale and should be treated as unverified

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-object-cap`: 400 MB per file. The record states no identity cost. Observed behaviour: Unverifiable.

Evidence: `https://castbox.fm` (2026-10-21), record `dossier/storage/castbox-creator-studio.json`.
Verdict: `qualifies-with-caveat`.

### Freesound, Creative Commons sound library (byte-exact originals)

> 1 GB per upload batch ('there is a file size upper limit of 1GB... when uploading multiple files at once, the size limit is applied to the sum of all file sizes'), no published total-account cap. Volume comes from the number of sounds, not...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1 GB per upload. The record states no identity cost. Observed behaviour: Serves the original, byte-for-byte, and says so explicitly: 'When you download the sound you get the exact same original file that was uploaded.

Evidence: `https://freesound.org` (2026-10-21), record `dossier/storage/freesound-creative-commons-sound-library.json`.
Verdict: `qualifies-with-caveat`.

### hearthis.at, free tier

> 400 MB per week, reset Sunday 19:00 CET: 'Upload up to 400 MB of music each week for free' and 'Your weekly upload quota of 400 MB is automatically reset every Sunday at 7:00 pm (CET)'. ~1.7 GB/month recurring, uncapped total accumulation

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: RE-ENCODES to 192 kbit/s CBR joint stereo for everyone on Free ('This ensures compatibility across all devices.

Evidence: `https://hearthis.at` (2026-10-21), record `dossier/storage/hearthis-at-free-tier.json`.
Verdict: `qualifies-with-caveat`.

### Jamendo (artist upload)

> No published per-account total; 480 MB per file, lossless only (WAV/FLAC/AIFF, 16 or 24-bit, 44.1 or 48 kHz, 1-2 channels)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 480 MB per file. The record states no identity cost. Observed behaviour: Lossless in, transcoded for streaming.

Evidence: `https://www.jamendo.com` (2026-10-21), record `dossier/storage/jamendo.json`.
Verdict: `qualifies-with-caveat`.

### Mixcloud, Basic tier (unlimited drafts)

> 10 published shows (>15 min) + 10 published tracks (<=15 min). But: 'there's currently no limit to the number of uploads you can have in your drafts', drafts are uploaded, stored, and private. That is the actual finding: published storage...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 4 GB max per show file. The record states no identity cost. Observed behaviour: Mixcloud is a streaming platform: shows are transcoded for playback and there is no original-file download link on Basic.

Evidence: `https://www.mixcloud.com` (2026-10-21), record `dossier/storage/mixcloud-basic-tier.json`.
Verdict: `qualifies-with-caveat`.

### RedCircle, Core (free) plan

> Unlimited. Core is 'our entirely free option... host one podcast with unlimited storage, bandwidth, episodes, and downloads'. Pricing page comparison table confirms storage / bandwidth / episodes / downloads all 'Unlimited' on Core

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200 MB per audio file. The record states no identity cost. Observed behaviour: Serves a dynamic-ad-inserted stream, not the uploaded file.

Evidence: `https://redcircle.com` (2026-10-21), record `dossier/storage/redcircle-core-plan.json`.
Verdict: `qualifies-with-caveat`.

### RSS.com, Free plan

> Unlimited. Free plan: 'Unlimited episodes and unlimited audio, with no storage cap', 'no trial and no expiry date', 'Your episodes are never deleted'. Only three stated limits: one podcast per account, 30 days of analytics history, one...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 2 GB per episode. The record states no identity cost. Observed behaviour: RE-ENCODES.

Evidence: `https://rss.com` (2026-10-21), record `dossier/storage/rss-com-free-plan.json`.
Verdict: `qualifies-with-caveat`.

### Spotify for Creators (formerly Anchor)

> Free hosting with no stated numeric cap. Spotify's own episode-publishing doc: 'We don't have a file size limit'. The video doc repeats it: 'Spotify for Creators doesn't have a file size limit'. No episode count, storage or bandwidth cap...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: RE-ENCODES everything to 128 kbit/s stereo.

Evidence: `https://creators.spotify.com` (2026-10-21), record `dossier/storage/spotify-for-creators.json`.
Verdict: `qualifies-with-caveat`.

### Spreaker, Free plan

> One podcast, unlimited episodes: 'The free plan allows users to have one podcast with an unlimited number of episodes.' No total-storage or per-file figure is published on the plans page or in the free-plan announcement, the plans page...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Definitively re-encodes, Spreaker's own help tells uploaders to upload WAV/FLAC 'so they will not be transcoded' twice, which confirms the platform stores a single normalised format, not the master.

Evidence: `https://www.spreaker.com` (2026-10-21), record `dossier/storage/spreaker-free-plan.json`.
Verdict: `qualifies-with-caveat`.

### Zencastr, free hosting

> Advertised as no cap: 'No episode caps, no storage limits, no upcharging as your show grows. Unlimited hosting, included in every plan', plus 'Up to 5 shows for free'. No numeric storage or per-file figure is published anywhere in their...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: No independent confirmation of transcode behaviour and no live enclosure observed possible without an account.

Evidence: `https://zencastr.com` (2026-10-21), record `dossier/storage/zencastr-free-hosting.json`.
Verdict: `qualifies-with-caveat`.

### AnyFlip (flipbook PDF host)

> FREE plan: 100 GB storage, unlimited number of publications, 5 uploads/day, 150 MB max PDF

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: 5 uploads/day free (60/day Pro). The record states no identity cost. Observed behaviour: Originals are re-served as derived page images, and the free download path returns 403 without a session.

Evidence: `https://anyflip.com` (2026-10-21), record `dossier/storage/anyflip.json`.
Verdict: `qualifies-with-caveat`.

### Internet Archive (IAS3 / petabox item upload)

> 1 TB hard limit per item page ("Currently, there is a 1TB size limit for item pages"), recommended 500 GB / 1,000 files per item; items per account unlimited. Single file "should not be larger than ~500 to ~700 GB"

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 1 TB/item. The record states no identity cost. Observed behaviour: Writes are asynchronous through a per-item queue.

Evidence: `https://archive.org` (2026-10-22), record `dossier/storage/internet-archive.json`.
Verdict: `qualifies`.

### 1fichier, registered free account, 5 TB of temporary storage with FTP + API

> Registered (free) tier: '5 TB of temporary storage', folder sharing, remote upload, FTP upload, and API access. Paid ladder: Premium Light 500 GB EUR 10/yr, 1000 GB EUR 20/yr, Premium EUR 54/yr with 4 TB cold storage, Premium GOLD EUR...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `retention-clamped`: Retention: 30 days after upload, or 90 days. A new account costs email. Observed behaviour: 1fichier/DStorage is a carrier with its own transit, so egress is not a marginal cost for them, which is why the free 5 TB survives where others died.

Evidence: `https://1fichier.com/tarifs.html` (2026-10-21), record `dossier/storage/1fichier-registered-free-account-5-tb-of-temporary-stora.json`.
Verdict: `qualifies-with-caveat`.

### Evolution Host, $0.00 lifetime VDS, 1 TB NVMe, in exchange for a backlink

> 1 TB NVMe, 128 GB DDR5 RAM, 16 cores @ 5 GHz, DDoS protected, $0.00 'lifetime', conditional on keeping a link to Evolution Host on a website you own

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: reviewed for SEO value. A new account costs email. Observed behaviour: 12+ year provider with a history of these barter offers.

Evidence: `https://lowendtalk.com/discussion/211463/0-00-high-spec-vds-128gb-ram-16-cores-5ghz-1tb-nvme-backlink-required` (2026-10-21), record `dossier/storage/evolution-host-0-00-lifetime-vds-1-tb-nvme-in-exchange-f.json`.
Verdict: `qualifies-with-caveat`.

### ImgBB

> Unlimited/indefinite storage for free accounts; no published total-byte cap. Third-party trackers consistently report 'unlimited storage, permanent hosting'

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: No re-compression documented and large JPEGs survive byte-for-byte.

Evidence: `https://imgbb.com` (2026-10-21), record `dossier/storage/imgbb.json`.
Verdict: `qualifies`.

### Postimages (postimages.org / postimg.cc)

> No storage cap stated: 'we do not impose strict limits on our users... Some users store and share tens of thousands of images'. Explicitly 'you will never have to worry about your images being removed due to inactivity'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 32 MB/file. The record states no identity cost. Observed behaviour: Web endpoint refuses scripted uploads with 403 'Automated uploads are not allowed via the website', must use the token API.

Evidence: `https://postimages.org` (2026-10-21), record `dossier/storage/postimages.json`.
Verdict: `qualifies-with-caveat`.

### Telegraph (telegra.ph)

> Unlimited pages and unlimited uploaded images; no account-level byte quota. Each page is an independent object with a permanent URL

That is the record's own wording (`reported`, 2026-10-21). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Upload endpoint is undocumented and flaky from datacenter IPs: all four attempts (direct, via proxy, with browser UA/Origin/Referer) returned '"Unknown error"' or UNKNOWN_METHOD.

Evidence: `https://telegra.ph` (2026-10-21), record `dossier/storage/telegraph.json`.
Verdict: `qualifies-with-caveat`.

### 88file.jp

> Claims (unlimited-capacity file transfer, free) and, no send-volume limit, free, ad-free, domestic Japanese servers

That is the record's own wording (`inferred`, 2026-10-21). The record states no identity cost. Observed behaviour: This is the classic Japanese small-host failure mode: the marketing page stays up and the actual service is down.

Evidence: `https://88file.jp` (2026-10-21), record `dossier/storage/88file-jp.json`.
Verdict: `qualifies-with-caveat`.

### ACdata (ac-data.info)

> Two products on one site. Transfer: '1 25065', unlimited total, 250 GB per file, up to 65 days. Separate cloud-drive product: 10 GB free, 30 GB if you hold premium on IllustratorAC/PhotoAC/SilhouetteAC

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 250 GB. The record states no identity cost. Observed behaviour: Run by the AC illustration-workspace group, so it is a marketing surface for their paid art subscriptions rather than a storage business, historically stable.

Evidence: `https://ac-data.info` (2026-10-21), record `dossier/storage/acdata.json`.
Verdict: `qualifies-with-caveat`.

### AllFiles.org

> 'Upload, store, and send files up to 200 GB for free', 100 GB per file, 200 GB per transfer, 30-day retention, no registration

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 GB. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Presents as a multi-language generic transfer host (identical copy in RU and EN).

Evidence: `https://allfiles.org` (2026-10-21), record `dossier/storage/allfiles-org.json`.
Verdict: `qualifies-with-caveat`.

### Axfc Uploader (axfc.net)

> No account, no total quota, per-object only. '1128 GiB' (max 128 GiB per file, multiple files uploaded in sequence). Upload form constant `data-max="137438953472"` = 128 GiB, confirming the number in the markup

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 128 GiB. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: This is the legendary Japanese uploader and it is emphatically alive: the public file list was showing uploads from minutes earlier on the day it was read.

Evidence: `https://www.axfc.net` (2026-10-22), record `dossier/storage/axfc-uploader.json`.
Verdict: `qualifies-with-caveat`.

### BigFile.net

> No account and no published total quota, storage is per-object and unbounded in count. 'Up to 256 GB per single file. No limit on batch uploads as long as each file is under 256 GB.'

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 256 GB. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Genuinely good for a no-account host: upload and read both verified by SHA-256 in observed, and the site advertises a 'zero-database architecture' meaning no inventory to lose.

Evidence: `https://www.bigfile.net` (2026-10-22), record `dossier/storage/bigfile-net.json`.
Verdict: `qualifies`.

### GigaWatasu (giga-watasu.jp)

> 333 GB per file, no registration. Registered free members additionally get 111-day retention, send history and a receive folder, all free. No total-storage figure because there is no account-level bucket

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 333 GB. The record states no identity cost. Observed behaviour: Newer entrant (the vendor runs a comparison blog and scores itself #1, which is a caveat on the ranking but not on the numbers).

Evidence: `https://giga-watasu.jp` (2026-10-21), record `dossier/storage/gigawatasu.json`.
Verdict: `qualifies-with-caveat`.

### MrOwl (mrowl.com)

> 'free unlimited storage for content that is shared to the world' + 10 GB private. The asterisk is the whole story: 'Free unlimited files stored in public branches up to 20MB per file'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB on the unlimited public tier. The record states no identity cost. Observed behaviour: The front page timed out repeatedly when read (504 through the reader, 0 bytes direct) while the help page and an April 2026 Wayback capture both served.

Evidence: `https://www.mrowl.com` (2026-10-21), record `dossier/storage/mrowl.json`.
Verdict: `qualifies-with-caveat`.

### U.UA (u.ua)

> 50 GB per file, unlimited file count, no registration, 7 days storage

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 50 GB. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Ukrainian file-exchange site, appears healthy.

Evidence: `https://u.ua` (2026-10-21), record `dossier/storage/u-ua.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Bunkr | fails-quota | No total quota published; 2 GB maximum per file |
| DoodStream | fails-quota | 'Unlimited Storage' (marketing claim on the homepage) |
| KrakenFiles | fails-quota | Marketed as 'unlimit drive'; free registered users get unlimited file count with a 500 MB per-file ceiling for private... |
| VikingFile | fails-quota | Tagline: 'Share large files anonymously. Unlimited storage. No mail required. No speed limit... |
| Acast, Starter (free) plan | fails-quota | 1 show, 5 episodes on Free, 'unlimited episodes when you make your show available in Acast's advertising marketplace'... |
| Podbean, Basic Free plan | fails-quota | 5 hours / 500 MB TOTAL, not monthly: 'Total storage: 5 hours... |
| Calameo | fails-quota | BASIC (free) account: 1 GB storage, 100 MB / 500 pages max per document, unlimited number of publications... |
| DocDroid | fails-egress | Free/Standard account: 10 uploads per 24h, no document-count or storage figure published... |
| DocumentCloud (MuckRock) | fails-quota | 500 MB per PDF (25 MB for non-PDF, converted via LibreOffice)... |
| Google Play Books (personal upload library) | fails-quota | Up to 1,000 uploaded files per Google account (2 GB max per file per the Partner Center spec... |
| Heyzine | fails-quota | Free Basic: 5 flipbooks, unlimited pages, 1 GB storage, 1 user, no watermark, API access included |
| Issuu | fails-quota | Free Basic plan (since 2025-05-29): 5 published documents max, each capped at 50 MB and 10 pages |
| pdfcoffee / dokumen.pub / idoc.pub... | fails-quota | "Upload as much as you need! Unlimited volume of uploaded files", no document count or account quota... |
| Scribd | fails-egress | 100 MB max per document; no published account-level document or storage cap... |
| SlideShare | fails-egress | 300 MB max per file (PDF/PPT/DOC), 300 slides for presentations... |
| ADTAQ Storage VPS, 2 TB, 30 days free (card-gated) | trial-only | 2 TB HDD (SSD-cached), 2 vCPU, 2 GB RAM, 6 TB/month bandwidth on 1 Gbps, $20/month... |
| Contabo Storage VPS, unlimited traffic, 300 GB... | fails-quota | Storage VPS 10: 300 GB SSD (150 GB NVMe option), 2 vCPU / 4 GB RAM... |
| DedicatedCore, 6 TB storage VPS... | trial-only | 6 TB HDD, 3 vCPU, 4 GB RAM, 10,000 GB bandwidth, dedicated IP, free for 60 days. Only 3 units existed |
| FOSSVPS / ST-Hosting, free VPS for open-source... | fails-quota | Free VPSs on donated hardware; the Frankfurt node is an AMD EPYC 7402P, 128 GiB RAM... |
| FreeMach, community free VPS (LES/HT/LET members... | fails-quota | US1.KVM: 2 vCPU, 3 GB RAM, 120 GB HDD, 1 TB transfer. EU1.KVM: 2 vCPU, 2 GB, 25 GB SSD... |
| Hetzner Storage Box BX11, 1 TB... | fails-quota | BX11 = 1 TB at EUR 3.20/month excl. VAT (EUR 0.0051/hr). Ladder: BX21 5 TB EUR 10.90, BX31 10 TB EUR 20.80... |
| InterServer Storage Cloud Compute... | fails-quota | 1 TB SATA per slice at $3.00/TB/month, stackable up to multi-TB (32 TB ladder). 2 GB RAM, 1 core, 30 GB SSD boot per slice... |
| Lex.st, 150 GB free storage box 'for the life of the... | fails-quota | 150 GB HDD RAID-6 (NVMe cached), 1000 GB bandwidth, 2 domains, jailed SSH, DirectAdmin, Salt Lake City, free permanently |
| PulsedMedia Storage Boxes... | fails-quota | Storage Boxes from 4 TB (EUR 8.99/mo, RAID5) to 32 TB. Separately, a FREE 30-day seedbox: 50 GiB storage, 250 MB RAM... |
| ServaRica, 'Unlimited Expanding Storage'... | fails-quota | Shrimp 1: 500 GB base + 1 GB/day automatic growth, $5/mo, i.e. it crosses 1 TB at ~day 500 and 1.87 TB at 4 years... |
| Strato HiDrive, 1 TB for 12 months at EUR 0... | trial-only | 1 TB, 12 months, EUR 0 (setup EUR 0). Regular price after the free year is EUR 5/month... |
| Systemfreaks, S3-compatible object storage... | fails-quota | 250 GB free during beta, 'and bandwidth is free'. Post-beta: $0.0050/GB storage... |
| VPS Server (vpsserver.com)... | trial-only | 1 TB of cloud block storage plus one cloud server worth up to $100, 30 days, 20+ locations |
| Cloudinary (free plan) | fails-quota | 25 monthly credits. 1 credit = 1 GB managed storage OR 1 GB CDN bandwidth OR 1,000 transformations... |
| Flickr | fails-quota | FREE TIER IS 1,000 ITEMS, NOT 1 TB. The famous 1 TB was killed on 2019-01-08. Free = 1,000 photos/videos total... |
| Gumlet (free plan) | fails-quota | 60 storage minutes of video, not bytes. No meaningful free image allowance, this is a video-first CDN |
| ImageKit (free plan) | fails-quota | 3 GB DAM storage, fixed |
| ImageShack | fails-egress | Free account with no published image-count or total-byte cap... |
| Pixiv | fails-egress | No published total quota; per-post caps only. Effectively unlimited posts |
| Sirv (free plan) | fails-quota | 0.5 GB storage |
| Uploadcare (free plan) | fails-quota | 1 GB storage, 1,000 operations/month, 5 GB/month traffic... |
| BowlRoll (bowlroll.net) | fails-quota | Not published on any page reachable without login; the front page now opens with a funding appeal... |
| DataDeliver (dd.datadeliver.net) (`データ便`) | fails-quota | Free tier: 5 GB per transfer (registered, free), 2 GB per transfer (Light... |
| Fshare / FshareStorage (fshare.vn, FPT Telecom) | fails-quota | Free tier: 50 GB of 'dung lng khong dm bo' (non-guaranteed capacity)... |
| Mail.ru (VK) (`Облако`) | fails-quota | 8 GB free: ', 8 '. The historic 100 GB-for-beta-testers grant was cancelled in Nov 2024... |
| Uschovna (uschovna.cz) | fails-quota | Anonymous transfer: 30 GB per shipment, free, 14 days, 30 downloads per recipient. Paid (40 CZK): 50 GB, 90 days... |
| uploader.jp / getuploader.com (`アップローダーレンタル`) | fails-quota | 10 GB total per account: 100 MB per file, 1,000 MB per uploader, 10 uploaders per account = 10 GB. Free, and the terms state |
| Yandex Disk free tier (post-2026-06 change) | fails-quota | 5 GB by default for users without a plan: ' 5 '. Photo/video 'unlimited' auto-upload is a plan feature only... |

Four failure modes account for most of the 43 rejections.

Quota is the largest group: a host that advertises "unlimited" and caps a file at 500 MB,
or a podcast host whose "unlimited episodes" means one show and five episodes. Egress is
the second: a download path throttled so hard that the host is selling the read rather than
the write. Retention is the third, and it is the one that looks like a win, because the
caps there are the largest.

The fourth is the pattern this corpus warns about most, and it is why a status code is not
evidence. Buzzheavier accepts an anonymous PUT with 201 and a 4-day expiry, and every read
path returns 403 with `Cf-Mitigated: challenge`. FileDitch accepts 155 GiB and returns 503
to every non-browser client. A host that takes bytes and will not return them is a one-way
sink, which for an archive is data loss that arrives later.

## Chaining

An anonymous host is a replica tier, never a primary. Two rules make it work.

Mint the manifest before the first upload, because no host in this class can enumerate what
it was given. The manifest is the only index, and it holds the digests that a repair loop
needs to tell a corrupt replica from a missing one.

Replicate across two different funding models, because the failure of one is correlated
with its business rather than with its uptime. BigFile.net and axfc have nothing in common
except that both are cheap to try: one is a commercial host on a sliding clock, the other a
22-year-old form with no account. An archive on both survives either one's policy change.

The pair that should not be chained is two hosts from the same forum thread. They tend to
share an operator, a reseller or a jurisdiction, and they fail together.
