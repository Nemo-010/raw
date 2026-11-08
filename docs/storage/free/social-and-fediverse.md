# Social and fediverse: what an instance or a platform gives a user

This class is the long tail of free storage: fediverse instances, social platforms, game
platforms with cloud saves, and the file APIs that AI products expose. The quotas are small
individually and the class is worth a document because the count is large, the interfaces are
documented, and one instance in it holds 1 TiB per user.

This document covers 14 qualifying records. 35 were rejected, and the largest
group is quota by a wide margin, which is what a class of volunteer-run instances looks like.

## The comparison

Sorted by the size of the single object accepted, because the account total in this class is
usually set by the instance operator rather than by a product.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Epic Online Services Player Data Storage | 400 MB total storage per user, 200 MB maximum per file... | per-object-cap: 200 MB per file and 64-character filename limit | - | qualifies-with-caveat |
| itch.io (butler / Wharf) | 30 GB uncompressed per build ('the itch.io backend will reject builds with a total... | per-object-cap: 30 GB uncompressed per build/channel | - | qualifies-with-caveat |
| ModDB (free member file hosting) | 4 GB per file via URL upload, ~2,800 MB via browser upload... | per-object-cap: 4,000 MB per file (URL upload) / ~2,800 MB (browser upload) | - | qualifies-with-caveat |
| PlayFab Game Saves (Development Mode titles) | Per Development Mode title: Profile storage 2 GB... | per-object-cap: 256 MB per player for Game Saves | - | qualifies-with-caveat |
| Steam Cloud (developer-set per-app quota) | Quota is set by each game's developer as 'Byte quota per user' and 'Number of files... | per-object-cap: 100 MB per FileWrite call... | - | qualifies-with-caveat |
| Alibaba Bailian / DashScope File API (QwenCloud SG) | 100 GB total per workspace; 10,000 files... | per-object-cap: 150 MB (file-extract) / 500 MB (batch) | any-phone | qualifies-with-caveat |
| Gemini Notebook (formerly NotebookLM), source corpus | 100 notebooks/user x 50 sources/notebook x 200 MB per source = 1,000,000 MB 1 TB free... | per-object-cap: 200 MB or 500,000 words | email | qualifies-with-caveat |
| OpenAI Files API, per-project file storage | 2.5 TB per project; 512 MB per file; no organization-wide storage cap... | per-object-cap: 512 MB | any-phone | qualifies-with-caveat |
| xAI Files API (Grok) + public CDN URLs | No published total-storage quota. Per-file 512 MB... | per-object-cap: 512 MB (50 MB for a public URL | email | qualifies-with-caveat |
| GitHub issue/PR comment attachments (user-attachments) | no account-level byte quota stated; per-file only, 10 MB images/GIFs... | per-object-cap: 25 MB/file | anonymous* | qualifies-with-caveat |
| Imgur (anonymous + account uploads) | 50 MB per non-animated image, 200 MB per GIF/video; 'no upload limit per account'... | - | anonymous* | fails-quota |
| Reddit native media (i.redd.it) | 20 MB per image post, ~1 GB per video post, no stated total | per-object-cap: 1 GB per video | - | qualifies-with-caveat |
| Substack file embeds | no stated total; 700 MB per PDF, XLSX/CBZ/CBR embeds supported | - | - | qualifies-with-caveat |
| Trello card attachments | 10 MB per attachment on Free, 250 MB on Standard... | per-object-cap: 10 MB/file | - | qualifies-with-caveat |

## What the class is

Four different things share this document and only one of them is scalable.

**A fediverse instance** is a volunteer-run server with a drive quota per user. misskey.gg gives
1 TiB, mk.absturztau.be 50 GB, misskey.flowers 12 GB, misskey.io 10 GiB. These numbers are set
by whoever pays for the server, and they change without notice.

**A social platform** gives an upload surface for its own content type. Reddit takes a 20 MB
image or a 1 GB video. Imgur takes a 50 MB image and 200 MB for a GIF. Substack takes a 700 MB
PDF embed.

**A game platform** has a cloud-save store with a quota the developer sets. Steam Cloud lets
each game choose its own byte quota and file count. PlayFab gives 2 GB of profile storage and
5 GB of UGC per development-mode title.

**An AI product's file API** is the newest member and the weakest: several of them are
write-only by design, which makes them a category error rather than a quota failure.

## misskey.gg, and the field that lies

The single largest instance quota in this class is 1 TiB per user.

`POST /api/meta` with `{"detail": true}` returned `policies.driveCapacityMb` of 1,024,000, which
is 1,000 GiB, and `emailRequiredForSignup: true` with `disableRegistration: false`. All three
were confirmed on 2026-10-22 (`measured`: 200, 3,228 B of JSON).

The per-object cap is the trap. The same response carries `policies.maxFileSizeMb` of 1024,
which reads as 1 GiB, and a top-level `maxFileSize` of 262,144,000 bytes, which is 250 MiB.
The second field is not under `policies`, so a reader who looks only inside `policies` finds
the wrong number, and the enforced value is the top-level one.

The practical consequence: a 1 TiB drive at 250 MiB per object needs 4,096 uploads, and the
grain of the shard plan is set by 250 MiB rather than 1 GiB.

Evidence: `https://misskey.gg/api/meta` (read 2026-10-22 as `measured`: 200, 3,228 B); record `dossier/storage/misskey-gg-misskey-2026-10-1-tb-drive-per-user.json`,
`documented` and `qualifies-with-caveat` on binding `per-object-cap` at 250 MiB.

Verdict: `qualifies-with-caveat`. The 1 TiB is the largest per-user quota found on a live,
registration-open instance, the 250 MiB object cap decides how it is used, and one volunteer
operator is the whole durability story.

## The files that cannot be read back

Six records in this document are file APIs whose upload succeeds and whose download does not
exist. They are the clearest instance of the write-gated pattern in the corpus.

Claude's Files API gives 1 TB per organisation and 500 MB per file, and uploaded files are
explicitly non-downloadable. Gemini's Files API gives 20 GB with the same restriction.
DeepSeek's is 25 GiB. OpenAI's `user_data` and Replicate's are write-only as well.

That is 1 TB of nominal capacity per organisation times 100 workspaces, which is 100 TB of
space that cannot be read. It is not storage, and the record's `dead_end.failure_class` is
`read-gated` rather than `quota`, because the quota is real and the read path is absent.

The three AI file APIs that *do* read back are worth naming: the OpenAI Files API at 2.5 TB per
project and 512 MB per file, the xAI Files API at 512 MB per file with public CDN URLs, and
Alibaba's DashScope File API at 100 GB per workspace with 10,000 files and no expiry.

## The game platforms

Five records here are game platforms and their quotas are set by the developer rather than the
platform, which makes them the most interesting structural case in the document.

Steam Cloud allows a developer to choose a byte quota and a file count per user, and it
enforces them on each save. PlayFab gives 2 GB of profile storage, 2 GB of content and
configuration storage, and 5 GB of UGC storage per development-mode title. Epic gives 400 MB
per user with 200 MB per file.

These are real stores with real APIs and their ceilings are two orders of magnitude short. They
are in the document because a plan that counts game platforms as capacity will find them and
assume a game engine is a storage provider.

### Epic Online Services Player Data Storage

> 400 MB total storage per user, 200 MB maximum per file, 1,000 files per user. No published product-level or title-level byte cap

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200 MB per file and 64-character filename limit. The record states no identity cost. Observed behaviour: Throttles writes (not errors) once the 400 MB per-user total is reached until files are deleted.

Evidence: `https://dev.epicgames.com/docs/epic-online-services/player-and-game-data/player-data-storage-interface/player-data-storage-overview` (2026-10-21), record `dossier/storage/epic-online-services-player-data-storage.json`.
Verdict: `qualifies-with-caveat`.

### itch.io (butler / Wharf)

> 30 GB uncompressed per build ('the itch.io backend will reject builds with a total uncompressed size that exceeds 30GB'). No documented total-account storage cap; project pages have a soft limit of 20, raisable on request. Free to host,...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 30 GB uncompressed per build/channel. The record states no identity cost. Observed behaviour: Pushing the same directory twice is a no-op, so versions accumulate as distinct builds rather than overwriting.

Evidence: `https://itch.io/docs/butler/pushing.html` (2026-10-21), record `dossier/storage/itch-io.json`.
Verdict: `qualifies-with-caveat`.

### ModDB (free member file hosting)

> 4 GB per file via URL upload, ~2,800 MB via browser upload. No documented total storage cap per account; Files / Addons / Mods tabs are all upload surfaces on a free account

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 4,000 MB per file (URL upload) / ~2,800 MB (browser upload). The record states no identity cost. Observed behaviour: Browser-upload path is fragile above ~2.8 GB and there is no resume, so a failed 12-hour upload wastes the slot.

Evidence: `https://www.moddb.com/features/overview-about-using-moddb` (2026-10-21), record `dossier/storage/moddb.json`.
Verdict: `qualifies-with-caveat`.

### PlayFab Game Saves (Development Mode titles)

> Per Development Mode title: Profile storage 2 GB, Content and configuration storage 2 GB, 5 GB UGC storage. 10 Development Mode titles per studio. Game Saves adds 256 MB per player per title

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 256 MB per player for Game Saves. The record states no identity cost. Observed behaviour: Titles in Development Mode cannot add users past 1,000 and must be launched (moved to a paid plan) to scale.

Evidence: `https://developer.microsoft.com/en-us/games/products/playfab/pricing/` (2026-10-21), record `dossier/storage/playfab-game-saves.json`.
Verdict: `qualifies-with-caveat`.

### Steam Cloud (developer-set per-app quota)

> Quota is set by each game's developer as 'Byte quota per user' and 'Number of files allowed per user', 'enforced on each Cloud-enabled game, on a per-user-per-game basis'. No Valve-imposed total. Community-observed ceilings: 93 GB per...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MB per FileWrite call (256 MB 'may result in a non-optimal storage.... The record states no identity cost. Observed behaviour: Entirely undocumented by Valve.

Evidence: `https://partner.steamgames.com/doc/features/cloud` (2026-10-21), record `dossier/storage/steam-cloud.json`.
Verdict: `qualifies-with-caveat`.

### Alibaba Bailian / DashScope File API (QwenCloud SG)

> 100 GB total per workspace; 10,000 files; NO expiry (no validity-period limit for now). Per-file: 150 MB for purpose=file-extract, 500 MB for purpose=batch, 300 MB for fine-tune, 50 MB for the newer Agent Studio endpoint

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 150 MB (file-extract) / 500 MB (batch). A new account costs any-phone. Observed behaviour: TWO CONTRADICTORY READ PATHS depending on the API generation used.

Evidence: `https://help.aliyun.com/zh/model-studio/openai-file-interface` (2026-10-21), record `dossier/storage/alibaba-bailian-dashscope-file-api.json`.
Verdict: `qualifies-with-caveat`.

### Gemini Notebook (formerly NotebookLM), source corpus

> 100 notebooks/user x 50 sources/notebook x 200 MB per source = 1,000,000 MB 1 TB free. Also 500,000 words/source cap and no page limit

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200 MB or 500,000 words. A new account costs email. Observed behaviour: READ-BACK IS EXTRACTED TEXT, NOT ORIGINAL BYTES.

Evidence: `https://support.google.com/gemininotebook/answer/16269187?hl=en` (2026-10-21), record `dossier/storage/gemini-notebook-source-corpus.json`.
Verdict: `qualifies-with-caveat`.

### OpenAI Files API, per-project file storage

> 2.5 TB per project; 512 MB per file; no organization-wide storage cap; orgs may create up to 2,000 projects by default

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 512 MB. A new account costs any-phone. Observed behaviour: READ GATE IS PER-PURPOSE, NOT PER-ACCOUNT.

Evidence: `https://developers.openai.com/api/reference/resources/files/methods/create` (2026-10-21), record `dossier/storage/openai-files-api-per-project-file-storage.json`.
Verdict: `qualifies-with-caveat`.

### xAI Files API (Grok) + public CDN URLs

> No published total-storage quota. Per-file 512 MB (some pages say 50 MB for the upload reference and 50 MiB for public URLs). Files are PERMANENT by default, `expires_after` is opt-in

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 512 MB (50 MB for a public URL.... A new account costs email. Observed behaviour: The absence of a published total quota is the finding, not an oversight, a third-party comparison site says outright 'no storage limit is stated.

Evidence: `https://docs.x.ai/developers/files/managing-files` (2026-10-21), record `dossier/storage/xai-files-api-public-cdn-urls.json`.
Verdict: `qualifies-with-caveat`.

### GitHub issue/PR comment attachments (user-attachments)

> no account-level byte quota stated; per-file only, 10 MB images/GIFs, 25 MB other files, 10 MB video on free plan (100 MB on paid)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 25 MB/file. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: assets persist after comment edit/delete in practice (URL is anonymised and not reference-counted).

Evidence: `https://github.com` (2026-10-21), record `dossier/storage/github-issue-pr-comment-attachments.json`.
Verdict: `qualifies-with-caveat`.

### Imgur (anonymous + account uploads)

> 50 MB per non-animated image, 200 MB per GIF/video; 'no upload limit per account'; 50 images/hour

That is the record's own wording (`reported`, 2026-10-21). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: the big one: Imgur has purged anonymous/unviewed content in past cleanup rounds and the 50-per-hour cap is enforced per IP.

Evidence: `https://imgur.com` (2026-10-21), record `dossier/storage/imgur.json`.
Verdict: `fails-quota`.

### Reddit native media (i.redd.it)

> 20 MB per image post, ~1 GB per video post, no stated total

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1 GB per video. The record states no identity cost. Observed behaviour: i.redd.it is Fastly-backed and 404s cleanly (observed returned a 2016-dated 404 with x-amz-version-id), i.e.

Evidence: `https://reddit.com` (2026-10-21), record `dossier/storage/reddit-native-media.json`.
Verdict: `qualifies-with-caveat`.

### Substack file embeds

> no stated total; 700 MB per PDF, XLSX/CBZ/CBR embeds supported

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: attachments live with the post.

Evidence: `https://substack.com` (2026-10-21), record `dossier/storage/substack-file-embeds.json`.
Verdict: `qualifies-with-caveat`.

### Trello card attachments

> 10 MB per attachment on Free, 250 MB on Standard, and explicitly 'there is no total limit for storage, just a per-file limit'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 MB/file. The record states no identity cost. Observed behaviour: attachments are real copies inside Trello ('Attachments from your computer create an actual copy within Trello').

Evidence: `https://trello.com` (2026-10-21), record `dossier/storage/trello-card-attachments.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Bluesky / AT Protocol PDS, 5 MiB blob default... | unsettled | blobUploadLimit defaults to 5 * 1024 * 1024 = 5 MiB per blob... |
| calckey.world, Sharkey, 10 GB per user | unsettled | 10240 MB = 10 GiB per user; maxFileSize 250 MiB |
| Farcaster hubs / Snapchain, storage RENT... | unsettled | Storage is allocated in integer units per fid and must be BOUGHT from the Storage Registry contract on Optimism... |
| infosec.exchange, Mastodon with a 1.35 GiB per-file... | unsettled | Per-account storage is UNLIMITED (stock Mastodon has no per-user media quota at all... |
| ioc.exchange, Mastodon, 1.32 GiB video / 80 MB image... | unsettled | Unlimited per-account; per-file video_size_limit=1419430400 (1.32 GiB), image_size_limit=83886080 (80 MiB) |
| Lemmy + pict-rs, per-instance image store... | unsettled | No per-user quota in Lemmy's own schema, the bound is pict-rs... |
| mastodonapp.uk / mstdn.social / mastodon.social and... | unsettled | Per-account UNLIMITED. Per-file: 103809024 bytes = 99 MiB (video)... |
| misskey.art, 5 GiB per user, 250 MiB per object | unsettled | 5120 MB = 5 GiB per user; maxFileSize 250 MiB |
| misskey.flowers, Misskey (hanami fork), 12 GB per user | unsettled | 12288 MB = 12 GiB per user; maxFileSize 250 MiB |
| misskey.gg, Misskey 2026.10... | unsettled | 1024000 MB = 1 TiB drive capacity PER USER, with maxFileSizeMb = 1024... |
| misskey.io, 10 GiB drive, 500 MiB per object... | unsettled | 10240 MB = 10 GiB per user; maxFileSize 524288000 bytes = 500 MiB per object |
| misskey.pm, 9.8 GB per user | unsettled | 10024 MB 9.8 GiB per user; maxFileSize 250 MiB |
| mk.absturztau.be, Sharkey, 50 GB drive per user | unsettled | 50000 MB = 50 GB per user drive; maxFileSize 262144000 bytes (250 MiB) per object |
| Nostr relays + NIP-94/NIP-96 file metadata... | unsettled | Zero bytes. NIP-94 is a *metadata* event: `url`, `m` (mime), `size`, `dim`, `i` (torrent infohash)... |
| pixelfed.de, Pixelfed, 15 MB per object... | unsettled | Per-account unlimited (Pixelfed has no per-user storage counter)... |
| Unity Cloud Content Delivery (CCD) | fails-egress | Conflicting. The live UGS pricing page lists Cloud Content Delivery 'Cloud Storage... |
| XBOX services Title Storage | fails-quota | Trusted Platform: 256 MB per player (Managed Partners) / 64 MB per player... |
| Anthropic Claude Files API | fails-egress | 1 TB per organization; 500 MB per file; files persist until deleted or until expires_at |
| Baidu Qianfan AppBuilder knowledge bases | fails-quota | Advertised as (file storage and processing unlimited) on the shared-storage path... |
| ChatGPT consumer file storage / Library + Projects | fails-quota | 25 GB shared upload storage per user, 100 GB per organization. 512 MB per file. Project file counts: Free 5, Go/Plus 25... |
| DeepSeek Files API | fails-egress | 25 GiB per user, 10,000 files, 64 MiB per file. Permanent if `expires_after` is omitted; otherwise 1 hour, 30 days |
| Gemini File Search stores (managed RAG) | fails-quota | Free tier 1 GB of store; Tier 1 10 GB; Tier 2 100 GB; Tier 3 1 TB. 100 MB per document |
| Google Gemini Files API (AI Studio) | fails-quota | 20 GB per project; 2 GB per file; 48-hour retention |
| mcp.gd, MCP-native object storage for agents | fails-quota | Free: 10 GB storage, 10 GB/month traffic, 100 MB web upload. Paid Starter $5/mo: 100 GB storage, 100 GB/mo traffic... |
| Moonshot / Kimi API Files | fails-quota | 10 GiB total storage per organization (default); 1,000 files; 100 MB per file |
| Perplexity Projects (formerly Spaces)... | fails-egress | 5 GB per Project, 10,000 files per Project, 100 MB per file, identical on every plan... |
| Poe bot knowledge bases | fails-quota | 5 GB or 30 million characters per knowledge base, combined across all sources of one bot. One knowledge base per bot |
| Together AI Files API (with 100 GB fine-tune objects) | fails-identity | 100 GB per training file (JSONL or Parquet); SDK constant MAX_FILE_SIZE_GB = 50.1 and MULTIPART_THRESHOLD_GB = 5.0... |
| Bilibili video upload | fails-egress | 8 GB per video reported for most accounts; some accounts higher (third-party guide, not vendor docs) |
| Confluence Cloud Free | fails-quota | 2 GB per site on Free (250 GB Standard, unlimited Premium); 100 MB default per attachment, admin-configurable |
| DeviantArt Sta.sh | fails-quota | 2 GB Sta.sh storage free, up to 100 GB with Core |
| Jira Cloud Free | fails-quota | 2 GB storage on Free, 250 GB Standard, unlimited Premium |
| Medium image hosting | fails-quota | 25 MB per image, images only |
| Stack Exchange image host (i.sstatic.net... | fails-quota | 2 MiB per image, no per-account total; unlimited images per post |
| Zhihu image hosting | fails-quota | no vendor page found; user reports cluster at 2-10 MB per image |

Quota is the largest group by far, and the numbers are small: 5 GiB per user, 10 GB per user,
15 MB per object. The class is a set of volunteer servers, and a volunteer server's half-life
is months. Five Cloudreve instances died inside two years, and the fediverse instance list has
the same shape.

Retention is the second group and it is the one that catches people. A misskey instance that
garbage-collects unreferenced blobs will delete a file that no post references, and a
Farcaster hub charges storage rent rather than giving it.

## Chaining

A fediverse instance is a replica for small objects and nothing more.

The one useful pattern is a public Blossom server as the store and a social platform as the
discovery layer, because a Nostr keypair costs nothing and a content-addressed identifier
survives the instance. That is the `relays-and-transports.md` pattern applied to a different
front end.

The pattern that fails is treating an instance quota as a tier. misskey.gg's 1 TiB is one
operator's disk, and the same operator can cut it to 100 GB without notice.
