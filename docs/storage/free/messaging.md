# Messaging: what a chat platform's attachment store actually holds

A chat platform is the most common way people accidentally build a large free store, and it is
also the class where the read path fails most often. The write is a message with an attachment.
The read is a CDN URL that may expire, may be behind authentication, or may be re-encoded.

This document covers 17 qualifying records: Telegram and its satellite services,
Discord and the chat CDNs built on it, team chat and document tools, and consumer IM APIs.
23 were rejected, and the rejections are dominated by platforms whose API cannot
return the bytes at all.

## The comparison

Sorted by the size of a single attachment, because the total is usually undocumented and the
per-object cap is what a shard fits. A `*` in the identity column means the value is read off
the record's own prose.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| WeChat Official Account, uploadimg... | NO documented count cap. The docs state explicitly: "100000"... | per-object-cap: Per-file cap 1 MB | - | fails-egress |
| Discord cloud uploads (direct-to-GCS... | Reserve an upload slot with `POST /channels/{id}/attachments` and PUT the body straight... | per-object-cap: 500 MiB per file | - | qualifies-with-caveat |
| Discord free account (attachment CDN) | No total storage cap documented anywhere... | per-object-cap: 20 MiB per file | - | qualifies-with-caveat |
| Steam Workshop (per-app item storage) | Per-item size is set by the game developer, not by Valve... | - | - | qualifies-with-caveat |
| Stoat (formerly Revolt), official instance | 20,000,000 bytes (20 MB) per attachment as the server-enforced default... | per-object-cap: 20 MB per file | - | qualifies-with-caveat |
| Airtable (free plan) - attachment fields | 1 GB attachment storage per base on Free... | per-object-cap: 5 MB per direct API upload | - | qualifies-with-caveat |
| Coda / Superhuman Docs (free plan) - attachments | 1 GB of attachments per doc on Free, 10 MB per individual attachment... | per-object-cap: 10 MB per single attachment | - | qualifies-with-caveat |
| DingTalk Drive (DingTalk Docs) (`钉盘`) | 100 GB of permanently free Drive capacity per organization by default... | per-object-cap: 8 GB per file | - | qualifies-with-caveat |
| Discord + ddrive (Discord as a datastore) | No total storage cap on free accounts; 10 MB per file on free... | per-object-cap: 10 MB per file | - | qualifies-with-caveat |
| Discourse hosted Free plan | 5 GB of uploads (images, videos, files) per free site, with unlimited topics... | - | - | qualifies-with-caveat |
| Lark (Feishu) Starter - free plan | 100 GB total storage per organization on Starter (Free)... | per-object-cap: 250 MB per file | - | qualifies-with-caveat |
| Microsoft Teams (free / personal) - Gallery & Media... | 5 GB OneDrive-backed file storage per user... | per-object-cap: 100 MB per file | - | qualifies-with-caveat |
| Notion (free plan) - file blocks & Files property | No total storage cap: 'Unlimited file uploads' on Free... | per-object-cap: 5 MiB per file | - | qualifies-with-caveat |
| Telegram, MTProto user account + unlimited channels... | No total storage cap, quoted from Telegram: 'you can... | per-object-cap: Per-file 2 GB | - | qualifies-with-caveat |
| Telegram public-channel web CDN... | Not a storage tier, this is the READ path for files already in a public channel... | - | - | qualifies-with-caveat |
| TG-FileStreamBot / filestream.bot... | Inherits Telegram's unlimited storage but solves a different problem: turning a stored... | per-object-cap: 20 MB per file | - | qualifies-with-caveat |
| ddrive (Discord as a filesystem) (self-hosted) | Unlimited logical file size and unlimited total: 'Tested with storing 4000 GB of data... | - | - | qualifies-with-caveat |

## What the class is

Three properties decide whether a messaging platform is storage.

**The total is usually absent.** Not one record in this document publishes a total storage cap.
Telegram states an unlimited number of files and no cap. Discord documents no total. The
absence is a documented absence rather than a documented limit, so it cannot be multiplied and
it does not appear in any arithmetic here.

**The per-object cap is small and hard.** Discord gives 20 MiB per attachment on a free account
since 2026-09-03. Notion gives 5 MiB per file on the free plan. Airtable gives 1 GB per base
instead of a per-file number. Coda gives 10 MB per attachment.

**The read path is the failure.** A Telegram file needs MTProto or a bot to fetch. A Discord CDN
URL carries an expiry. A WhatsApp media identifier is valid for five minutes and the bytes are
deleted on day 30.

## Telegram, and why it is the exception

Telegram is the one platform in this class whose numbers support a large store, and it does so
for a reason worth stating: it has published an unlimited file count for years and its
infrastructure is funded by a subscription product rather than by advertising the read.

Its per-file cap is 2 GB, or 4 GB on Premium, expressed in the API as
`upload_max_fileparts` of 4,000 or 8,000 times 524,288 bytes. A ranged read returned 206
(`documented`, 2026-10-21).

Three satellite services make it usable and each is a separate record.

The **public-channel web CDN** is the anonymous read path: a `t.me/s` preview page links to
`cdnN.telesco.pe`, which serves bytes with no account and no token. That is what makes a
Telegram channel readable by a job that holds no credentials.

**TG-FileStreamBot** turns a stored file into a plain HTTP URL, which is the adapter that makes
Telegram look like an object store.

**Teldrive** and the rclone backend mount the account as a filesystem. Three rules
apply to all three: mint a URL per connection, expect the signature to expire, and compare the
`Content-Length` to the expected size.

## Discord, and the filesystem built on it

Discord is the class's most interesting failure because the community built a filesystem on it
anyway.

`ddrive` stores 4 TB in one channel by splitting a file into attachments and rebuilding it.
Discord does not re-encode an arbitrary attachment, so the bytes survive, and the project
reports 4,000 GB stored on a single channel.

The platform's own cloud upload path reserves a slot with `POST /channels/{id}/attachments` and
then PUTs the body straight into Discord's Google Cloud Storage bucket. That is a legitimate
direct upload and it is the only documented API path in the class.

What breaks it: 20 MiB per attachment on a free account, a CDN URL with an expiry, and no
published total. An archive of 20 TiB at 20 MiB is 1,048,576 attachments, and the reconstruction
work belongs to the uploader.

## The team-chat and document platforms

Nine records here are workspace tools with an attachment store. Their caps are uniformly small
and their interfaces are uniformly good, which makes them tempting.

DingTalk Drive gives 100 GB per organisation with 8 GB per file. Lark Starter gives 100 GB per
organisation with 250 MB per file. Discourse's hosted free plan gives 5 GB per site. Microsoft
Teams gives 5 GB per user backed by OneDrive, with Gallery and Media uploads explicitly not
counted against it.

The last one is the only genuine find in this group, and it is a quota-accounting fact rather
than a quota: an image or video uploaded through Gallery does not consume the user's OneDrive
allocation. That is the same shape as Google Chat's attachments being exempt from the storage
quota, and both are worth knowing and neither is a 20 TiB plan.

## The consumer IM APIs

Four records are messaging APIs rather than chat products, and they are in this document
because people count them as storage.

WhatsApp's Cloud API media is deleted after 30 days and a media URL is valid for five minutes.
That is a transfer, not a store, and any claim that WhatsApp is free storage is wrong about the
30-day deletion. LINE's message content endpoint has a similar shape.

### WeChat Official Account, uploadimg (the uncapped endpoint)

> NO documented count cap. The docs state explicitly: "100000", images uploaded via this endpoint do NOT count against the 100,000-image library limit. Per-file cap 1 MB, JPG/PNG only

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Per-file cap 1 MB. The record states no identity cost. Observed behaviour: Images are permanent in practice (they must survive in published articles forever), but the service is tuned for article inline images.

Evidence: `https://developers.weixin.qq.com/doc/service/api/material/permanent/api_uploadimage` (2026-10-21), record `dossier/storage/wechat-official-account-uploadimg.json`.
Verdict: `fails-egress`.

### ddrive (Discord as a filesystem)

> Unlimited logical file size and unlimited total: 'Tested with storing 4000 GB of data on single discord channel'. Splits files into 24 MB chunks and fans them across webhooks

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Viable and battle-tested at multi-TB scale, but every download depends on re-deriving a 24 h signed URL, so the front-end must be alive.

Evidence: `https://github.com/forscht/ddrive` (2026-10-21), record `dossier/storage/ddrive.json`.
Verdict: `qualifies-with-caveat`.

### Discord cloud uploads (direct-to-GCS, 500 MiB reservation)

> Reserve an upload slot with `POST /channels/{id}/attachments` and PUT the body straight into Discord's Google Cloud Storage bucket, the reservation path accepts up to 500 MiB per file, independent of the 20 MiB message-time limit. Note the...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 500 MiB per file. The record states no identity cost. Observed behaviour: Endpoints are undocumented-but-stable and have moved URL shape before.

Evidence: `https://docs.discord.food/topics/cloud-uploads` (2026-10-21), record `dossier/storage/discord-cloud-uploads.json`.
Verdict: `qualifies-with-caveat`.

### Discord free account (attachment CDN)

> No total storage cap documented anywhere. Per-file only: 20 MiB per attachment on a free account since 2026-09-03 (raised from 10 MiB). 10 files per message. Server Boost tiers raise it for all members in that server: Tier 2 = 50 MB, Tier...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MiB per file. The record states no identity cost. Observed behaviour: Attachment CDN URLs are signed and expire in exactly 24 h.

Evidence: `https://discord.com` (2026-10-21), record `dossier/storage/discord-free-account.json`.
Verdict: `qualifies-with-caveat`.

### Steam Workshop (per-app item storage)

> Per-item size is set by the game developer, not by Valve, and some games are explicitly unlimited, Arma 3: 'Arma 3 Workshop now support items of unlimited size.' Others are tiny: House Flipper raised its cap from 12 MB to 20 MB in a patch....

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Very durable, Workshop items have survived a decade, links do not expire, and downloads are anonymous.

Evidence: `https://partner.steamgames.com/doc/features/workshop` (2026-10-21), record `dossier/storage/steam-workshop.json`.
Verdict: `qualifies-with-caveat`.

### Stoat (formerly Revolt), official instance

> 20,000,000 bytes (20 MB) per attachment as the server-enforced default, no paid tier to raise it, and no documented total storage cap

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB per file. The record states no identity cost. Observed behaviour: Critically different from Discord: attachment URLs are UNSIGNED and permanent.

Evidence: `https://stoat.chat` (2026-10-21), record `dossier/storage/stoat-official-instance.json`.
Verdict: `qualifies-with-caveat`.

### Airtable (free plan) - attachment fields

> 1 GB attachment storage per base on Free, with unlimited bases and 1,500 bases per workspace

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 MB per direct API upload. The record states no identity cost. Observed behaviour: 1,000 API calls per month on Free is a hard wall - that is ~33 uploads/day, so the 1.5 TB chain is rate-limited long before it is capacity-limited.

Evidence: `https://airtable.com` (2026-10-21), record `dossier/storage/airtable-attachment-fields.json`.
Verdict: `qualifies-with-caveat`.

### Coda / Superhuman Docs (free plan) - attachments

> 1 GB of attachments per doc on Free, 10 MB per individual attachment, with no cap on the number of personal docs or their objects

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 MB per single attachment. The record states no identity cost. Observed behaviour: Sharing a doc flips it into the 50-object / 1,000-row regime and can lock it read-only after a 14-day grace period - the unlimited mode is strictly the unshared mode.

Evidence: `https://coda.io` (2026-10-21), record `dossier/storage/coda-superhuman-docs-attachments.json`.
Verdict: `qualifies-with-caveat`.

### DingTalk Drive (DingTalk Docs)

> 100 GB of permanently free Drive capacity per organization by default; 8 GB max per uploaded file

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 8 GB per file. The record states no identity cost. Observed behaviour: Quota accounting changed in 2023 to count in-document attachments, so a previously-fine account can silently blow its 100 GB.

Evidence: `https://www.dingtalk.io` (2026-10-21), record `dossier/storage/dingtalk-drive.json`.
Verdict: `qualifies-with-caveat`.

### Discord + ddrive (Discord as a datastore)

> No total storage cap on free accounts; 10 MB per file on free (20 MB per Discord's own File Attachments FAQ), 50 MB Nitro Basic, 1 GB Nitro; attachments upload up to 500 MiB per file via the cloud-upload endpoint before the message-time...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 MB per file. The record states no identity cost. Observed behaviour: Highest operational risk of the set: Discord rate-limits uploads hard, CDN URLs expire, and the reference demo (ddrive.forscht.dev) is currently down (HTTP 522).

Evidence: `https://discord.com` (2026-10-21), record `dossier/storage/discord-ddrive.json`.
Verdict: `qualifies-with-caveat`.

### Discourse hosted Free plan

> 5 GB of uploads (images, videos, files) per free site, with unlimited topics, chat and members. Paid tiers: 20 GB / 100 GB / 200 GB+

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Uploads are permanent permalinks, no signed expiry.

Evidence: `https://www.discourse.org/pricing` (2026-10-21), record `dossier/storage/discourse-hosted-free-plan.json`.
Verdict: `qualifies-with-caveat`.

### Lark (Feishu) Starter - free plan

> 100 GB total storage per organization on Starter (Free); 250 MB single-file limit for Docs uploads on Starter

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 250 MB per file. The record states no identity cost. Observed behaviour: Rate limits are explicit (5 QPS on single upload) and multipart is resumable.

Evidence: `https://www.larksuite.com` (2026-10-21), record `dossier/storage/lark-starter-free-plan.json`.
Verdict: `qualifies-with-caveat`.

### Microsoft Teams (free / personal) - Gallery & Media uploads

> 5 GB OneDrive-backed file storage per user, BUT images and videos uploaded via Gallery/Media are explicitly NOT stored in OneDrive and have no storage limit

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MB per file. The record states no identity cost. Observed behaviour: The media path has no documented retention guarantee and no API - it is UI-only, so it is a manual archive at best.

Evidence: `https://www.microsoft.com/en-us/microsoft-teams/free` (2026-10-21), record `dossier/storage/microsoft-teams-gallery-media-uploads.json`.
Verdict: `qualifies-with-caveat`.

### Notion (free plan) - file blocks & Files property

> No total storage cap: 'Unlimited file uploads' on Free, but each file is capped at 5 MiB on Free (5 GiB on paid). Block limit is unlimited for a single-member Free workspace

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 MiB per file. The record states no identity cost. Observed behaviour: The MIME whitelist is the killer: no generic octet-stream blobs, so archival datasets must be packed as.zip/.7z/.tar which Notion does accept.

Evidence: `https://www.notion.com` (2026-10-21), record `dossier/storage/notion-file-blocks-files-property.json`.
Verdict: `qualifies-with-caveat`.

### Telegram, MTProto user account + unlimited channels as the volume

> No total storage cap, quoted from Telegram: 'you can... share an unlimited number of photos, videos and files (doc, zip, mp3, etc.) of up to 2 GB each'. Per-file 2 GB free, 4 GB with Premium. Per-account volume is effectively unbounded...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Per-file 2 GB. The record states no identity cost. Observed behaviour: Throttling is the real risk, not deletion: FLOOD_PREMIUM_WAIT_X caps non-Premium throughput and FLOOD_WAIT_X backs off per method.

Evidence: `https://telegram.org` (2026-10-21), record `dossier/storage/telegram-mtproto-user-account-unlimited-channels-as-the.json`.
Verdict: `qualifies-with-caveat`.

### Telegram public-channel web CDN (t.me/s preview -> cdnN.telesco.pe), anonymous reads

> Not a storage tier, this is the READ path for files already in a public channel. Anonymous, no account, no token, no API key. Scraping the public preview of a channel yields directly-fetchable media URLs for every photo and video post

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Token semantics are weaker than they look.

Evidence: `https://t.me/s/telegram` (2026-10-21), record `dossier/storage/telegram-public-channel-web-cdn-anonymous-reads.json`.
Verdict: `qualifies-with-caveat`.

### TG-FileStreamBot / filestream.bot, HTTP stream front-end over Telegram files

> Inherits Telegram's unlimited storage but solves a different problem: turning a stored Telegram file into a plain HTTP URL that a browser, VLC, or a download manager can range-request. 1,933 stars, pushed 2026-03-07, actively maintained

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB per file. The record states no identity cost. Observed behaviour: Maintained and the streaming model is sound.

Evidence: `https://github.com/EverythingSuckz/TG-FileStreamBot` (2026-10-21), record `dossier/storage/tg-filestreambot-filestream-bot-http-stream-front-end-ov.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Cisco Webex, Messages API file attachments | fails-egress | No storage quota published. Per-attachment cap is the only hard number: 'Message attachments are limited to 100MB each.' |
| KakaoTalk Channel / AlimTalk (Kakao Business) | fails-quota | No storage quota. Kakao's message API takes an IMAGE URL that the sender hosts... |
| LINE Messaging API, message content endpoint | fails-quota | No storage quota is offered at all. Content is a delivery mechanism, not a store |
| RingCentral Team Messaging (Glip) posts/files | trial-only | No storage quota published; the API reference documents pagination over posts, not a media store with a byte allowance |
| Sendbird Chat (free plan) | fails-quota | Pricing page advertises 'Message storage: Unlimited' on the free tier... |
| Stream Chat (GetStream) free/Maker plan | fails-quota | No free storage allowance stated as a byte figure on the storage page... |
| Twilio Programmable Messaging, Media subresource | fails-quota | No quota, media is retained indefinitely. The docs say Twilio 'retains the stored media until you delete the related Media... |
| Viber Business Messages / REST Bot API | fails-quota | No storage quota, same inversion as Kakao: the caller passes a picture URL, Viber fetches it. Max image 1 MB on iOS... |
| WhatsApp Cloud API, Media (upload / media_id) | fails-quota | Per-file caps only, no storage quota: documents 100 MB, images 5 MB, video 16 MB, audio 16 MB... |
| Zoom Team Chat, files API | fails-quota | No storage quota obtained. Zoom's chat-files docs were not readable through any allowed path in observed... |
| Matrix.org homeserver (media repository) | fails-quota | Free plan: 10 MB max per attachment, 100 MB per 24 h, capped at 500 MB per 28 days. Premium: 100 MB per attachment... |
| Skool native video hosting | trial-only | 30 GB per uploaded video file, with no documented community-level storage cap... |
| Twist (Doist) Free plan | fails-quota | 5 GB of file storage per team on Free; unlimited on Twist Unlimited. 100 MB per attachment |
| Zulip Cloud Free | fails-quota | 5 GB total file storage per organization on Cloud Free, not per user. Standard/Plus are 5 GB/25 GB per user |
| Pumble (free plan) | fails-quota | 10 GB of file storage for the whole workspace on Free |
| Slack (free plan) | fails-quota | 5 GB per free workspace (hard cap), 1 GB max per file, plus a 90-day visibility window and permanent deletion of anything... |
| Twist (free plan) | fails-quota | 5 GB storage on Free (unlimited on Twist Unlimited); 100 MB per attachment |
| Matrix media repository (matrix.org homeserver) | fails-quota | Free plan: 10 MB maximum per attachment, 100 MB of attachments per 24 hours... |
| Stoat (formerly Revolt) + Autumn file service | fails-quota | 20 MB per file, no subscription: 'Custom emojis, a 20MB file upload limit and a server-specific profile picture with no... |
| Mattermost Team Edition / Entry (self-hosted) | fails-egress | No storage quota at all in self-hosted Mattermost, free or paid. Only the per-file ceiling is configurable: default 100 MB... |
| Rocket.Chat self-hosted (Community / Starter) | fails-egress | No storage quota. Per-file ceiling is a single setting: 'Maximum File Upload Size (in bytes)... Use -1 to remove the limit.' |
| Self-hosted Synapse media repository | fails-egress | Unbounded, `max_upload_size` defaults to 50M and can be set to any value... |
| Stoat / Revolt, self-hosted instance | fails-egress | No platform cap at all: `body_limit_size` and `[files.limit]` live in Revolt.toml and are set by the instance operator... |

`not-storage` is the largest group here and it is the finding. A messaging API that accepts a
media object and deletes it on a clock, or that returns a URL which expires in minutes, is a
transport. Counting it as capacity is the link-handoff error.

`quota` is the second group: ClickUp gives 60 MB of file storage on its free plan, and the paid
tiers are the only route to "unlimited".

`egress` is the third and it is the one a plan discovers late. A Discord CDN URL that expires
means every read needs a fresh resolution, which is the same problem as a presigned URL and
costs the same effort to solve.

## Chaining

A messaging platform is a shard target behind an adapter, never a tier.

The pattern that works is Telegram plus one adapter: an account as the store, a bot or Teldrive
as the filesystem, and the public-channel CDN as the anonymous read path. That is the only
combination in this class where the write, the mount and the anonymous read are all documented.

The pattern that fails is a workspace tool as a primary. A 100 GB organisation cap with a 250 MB
file limit is a document store, and no adapter changes the 100 GB.
