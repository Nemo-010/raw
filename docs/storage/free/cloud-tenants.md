# Cloud tenants: what an institutional account gives, and what it costs to hold one

This class is the largest free capacity in this topic and the most misleading, because
the quota belongs to an organisation rather than to a person. A pooled education tenant
holds 100 TB and every number in the offer is real. Whether a reader can hold one is a
separate question, and it is the one this document answers first.

The 27 qualifying records below fall into six groups: education and nonprofit tenants,
startup credit programmes, the Google Drive service-account history, consumer drives with
an open foreign signup, CIS video platforms used as bulk stores, and niche or crypto
drives. The second half of the document is the 44 that failed, and most of them failed on
identity rather than on quota.

## The comparison

Sorted by the size of the allocation, then by whether a reader can obtain it. `*` in
the identity column means the value is read off the record's own prose rather than from
its `identity_cost` field.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| RUTUBE | 25 GB max per video, 5 concurrent uploads... | per-object-cap: 25 GB max per video | - | qualifies-with-caveat |
| VK Video (video hosting as bulk store) | up to 256 GB per single uploaded file; no per-account total published on the page read | per-object-cap: 256 GB single file | - | qualifies-with-caveat |
| Azure for Students (and Azure for Students Starter) | $100 credit per 12 months plus free monthly amounts of 20+ services... | - | - | qualifies-with-caveat |
| Blossom servers (blossom.band / blossom.nostr.build... | 'Free uploads for everyone, from any Blossom-capable client.' 'A hard cap of 100 MiB... | per-object-cap: 20 MiB for free uploads (100 MiB only on the $18/yr plan) | anonymous* | qualifies-with-caveat |
| Walrus Testnet public publishers... | No account, no key, no quota. Docs quote only a per-request limit: 'Most aggregators... | per-object-cap: 1 GiB verified write | anonymous* | qualifies-with-caveat |
| Atlassian Confluence Premium via Social Impact... | Confluence Premium = 'Unlimited file storage'... | per-object-cap: the binding constraint: 'The default size limit is 100 MB' per... | anonymous* | qualifies-with-caveat |
| AWS Activate (Founders / Portfolio) | Founders tier: '$1,000 in AWS Activate Credits... | request-rate: S3 request rates are effectively unlimited at this scale but each... | - | qualifies-with-caveat |
| Cloudflare for Startups, nonprofit / civil-society... | Up to $350,000 in credits for a year on the current program page... | request-rate: Workers/API rate limits apply to control-plane calls | - | qualifies-with-caveat |
| Databricks Free Edition (default storage / Unity... | No published byte quota. Free Edition ships 'serverless compute and default storage... | request-rate: per-account serverless quotas... | - | trial-only |
| Google for Startups Cloud Program... | Scale and Scale AI tiers: '$200K - $350k in credits' for startups with verifiable... | request-rate: per-project GCS quotas (raiseable) | - | qualifies-with-caveat |
| Google Workspace for Education Fundamentals... | 100 TB of pooled cloud storage per institution... | per-object-cap: 5 TB per single upload... | - | qualifies |
| Microsoft 365 Business Basic... | Microsoft 365 Business Basic (Nonprofit Staff Pricing) is a 'Grant... | per-object-cap: 250 GB per file in OneDrive (Microsoft's documented ceiling) | - | qualifies |
| Microsoft Azure grant for nonprofits ($2,000/yr... | $2,000 (USD) in donated Azure services credits per year, renewable. Not a byte quota... | per-object-cap: Blob block blob max ~190 | - | qualifies-with-caveat |
| Google Chat spaces as a quota-exempt attachment store... | Per-record unlimited: 200 MB per attachment... | per-object-cap: 200 MB per file | - | qualifies-with-caveat |
| Google Drive shared drives written by service... | Service accounts now report storageQuota limit '0'... | per-object-cap: 5 TB max file | - | qualifies-with-caveat |
| Gofile | no storage figure at all on the free tier... | retention-clamped: deleted after 10 days of inactivity unless it k | - | qualifies-with-caveat |
| InfiniCLOUD (formerly TeraCLOUD) | 20 GB free account; referral bonus up to 1,000 GB for the referrer... | - | - | fails-quota |
| Linkbox / TeleBox | 5 GB on plain signup; 10 TB granted via 'Special Account Authentication' with an... | per-ip-shaping: 1 MB/s | - | qualifies-with-caveat |
| Azure DevOps Repos (Git as bulk blob store) | Unlimited private Git repositories free per organization... | per-object-cap: 250 GB per repository | anonymous* | qualifies |
| Microsoft 365 / Office 365 A1 Education tenant... | 100 TB (102,400 GB) free pooled storage per education tenant... | per-object-cap: 250 GB max single file | - | qualifies |
| SharePoint Online site collections... | 25 TB maximum storage per site collection; 2,000,000 site collections per organization... | - | - | qualifies-with-caveat |
| Cloud.ru Evolution S3 free tier | Free tier object storage: 15 GB standard + 1,000 GB cold + 3,000 GB ice... | - | - | qualifies-with-caveat |
| Datum Storage | 1 TB free from signup ('Get 1TB Free Cloud Storage From Datum'), S3-compatible endpoint | - | - | trial-only |
| file.kiwi | Web Folder Basic: 'No capacity limit. Auto-deleted 90 hours after upload.' API flow: 10... | per-object-cap: 999 GiB/file | - | qualifies-with-caveat |
| Seznam.cz (email-as-storage) | Mailbox is byte-unlimited: 'Uzivatel muze schranku vyuzivat v neomezene velikosti'... | per-object-cap: 50 MB receive per message | - | qualifies-with-caveat |
| TeraBox (Baidu / Flextech) | 1 TiB free ('Network disk capacity limited to 1 TiB' on the free column... | per-object-cap: 4 GB/file | - | qualifies |
| MEGA | 20 GB free at signup, plus stacking achievements of 5 GB each (desktop app, mobile app... | retention-clamped: expire after 365 days | - | qualifies-with-caveat |

## What the class is

A tenant is an administrative container with pooled storage, and the pool is shared
across every user in it. That is what makes the numbers large: 100 TB is a per-tenant
figure, not a per-user one, and a single user in a fresh tenant can consume all of it.

The class splits by who can create the tenant. An education tenant needs a
government-recognised institution with a verified domain. A nonprofit tenant needs a
registered charity. A startup credit programme needs a company, usually with funding. A
consumer drive needs only an email address, which is why its quotas are three orders of
magnitude smaller.

The one history worth reading closely is Google Drive's service-account chain, because it
is the most widely copied recipe in this niche and it is dead.

## The tenants that matter

### Microsoft 365 A1 education: 100 TB pooled per tenant

100 TB (102,400 GB) of pooled storage per education tenant, spanning OneDrive, SharePoint
and Exchange, free of charge. The pool is 100 TB base plus per-licence contributions, and
Office 365 A1 licences contribute zero while consuming from the pool.

Two limits sit behind it and both bind before the pool does. Office 365 A1 caps OneDrive at
100 GB per user, set in February 2024, while Microsoft 365 A1 allows up to 1 TB per user
against the same 100 TB pool. And a single upload is capped at 250 GB.

The identity is the whole question: an education tenant needs a verified domain and an
institution that qualifies. This is `qualifies` on quota and conditional on an education
tenant. The pool, the two user limits and the 250 GB upload cap are read off
Microsoft's pages (`reported`, 2026-10-21).

Evidence: `https://learn.microsoft.com/en-us/microsoft-365/education/` and
`https://www.microsoft.com/en-us/microsoft-365/enterprise/office-365-a1` (2026-10-21).
Verdict: `qualifies`.

### Google Workspace for Education Fundamentals: 100 TB pooled

100 TB pooled across Drive, Gmail, Photos and shared drives, at no cost, stated twice on
Google's own pages. The per-user upload throttle is 750 GB per 24 hours for upload and
copy, which refreshes rather than accumulating, and the single-file cap is 5 TB.

The same identity condition applies. The reason this entry matters is not the signup
itself; it is that a single working
institutional address converts several `fails-identity` entries in this topic into usable
ones. All three numbers are the vendor's page, not a measurement here (`reported`, 2026-10-21).

Evidence: `https://edu.google.com/workspace-for-education/editions/education-fundamentals/`
and `https://knowledge.workspace.google.com/admin/getting-started/editions/google-workspace-for-education-faq`
(2026-10-21).
Verdict: `qualifies`.

### Microsoft 365 Business Basic nonprofit: 300 seats at 1 TB each

A grant of up to 300 seats, free, with 1 TB of OneDrive per user, which is 300 TB of
pooled tenant storage at zero cost. The per-file cap is 250 GB in OneDrive, and the
mailbox is 100 GB.

This is the largest free allocation anywhere in the topic and it needs a registered
nonprofit. Its constraint is `per-object-cap` at 250 GB, not the 300 TB pool, and its
identity cost is an organisation the reader would have to form. The seat count and the caps
are Microsoft's page (`reported`, 2026-10-21).

Evidence: `https://www.microsoft.com/en-us/microsoft-365/nonprofit/` (2026-10-21), record `dossier/storage/microsoft-365-business-basic-nonprofit-grant.json`.
Verdict: `qualifies`.

### SharePoint Online: 25 TB per site collection

25 TB maximum per site collection, 2,000,000 site collections per organisation, and a 250 GB
upload limit. The site ceiling is not the real bound: a tenant with a 100 TB pool cannot
fill 25 TB across more than four sites, so the pool is what binds. Versioning multiplies
storage silently on overwrite, with 50,000 major versions allowed. Every number here is from the
limits page (`reported`, 2026-10-21).

Evidence: `https://learn.microsoft.com/en-us/sharepoint/limits-and-specifications` (2026-10-21), record `dossier/storage/sharepoint-online-site-collections.json`.
Verdict: `qualifies-with-caveat`.

### Azure DevOps Repos: git as a bulk blob store

Unlimited private repositories, each up to 250 GB, with storage not billed as a meter at
all: the free tier bills users, parallel jobs and Artifacts storage, and Git LFS is free.
The per-push limit is 5 GB and LFS pushes are exempt.

This is the cheapest large git store in the topic and it is `qualifies`. What breaks it is
the pack-file soft limit before 250 GB, and the fact that a git repository is a poor shape
for bulk data: every clone carries the whole history. The limits are Microsoft's page
(`reported`, 2026-10-21).

Evidence: `https://learn.microsoft.com/en-us/azure/devops/repos/git/limits` (2026-10-21), record `dossier/storage/azure-devops-repos.json`.
Verdict: `qualifies`.

### The Drive service-account chain, and why it inverted

The widely copied recipe was 15 GB per service account, 100 service accounts, 30 projects,
which is 45 TB. It no longer works. A service account now reports `storageQuota` limit
`"0"` and cannot own files at all, so every upload into My Drive returns
`403 storageQuotaExceeded`.

The chain inverted rather than died. Service accounts are still free and unlimited, and
they hold zero bytes, so they become a write-throughput multiplexer against one tenant's
pooled shared drive. The 750 GB per day upload budget is per acting identity and each
service account is a distinct identity, so N accounts lift N x 750 GB per day into one
shared drive. The pool is the ceiling, and the pool belongs to a tenant.

A hard 16 GB limit is also reported when uploading into a My Drive folder shared with a
service account, which is why shared drives are the only working target. The `storageQuota`
of `"0"` and the 750 GB per day budget are Google's API documentation, and the 403 was a
forum report rather than a probe (`reported`, 2026-10-21).

Evidence: `https://developers.google.com/workspace/drive/api/guides/about-shareddrives` and
`https://developers.google.com/workspace/drive/api/guides/limits` (2026-10-21).
Verdict: `qualifies-with-caveat`.

### Google Chat spaces: an attachment store outside the quota

200 MB per attachment, and Chat messages and attachments explicitly do not count toward
Google storage quota. The API allows 600 attachment uploads per minute per project, which
is about 120 GB per minute of theoretical ingest, and reads support `Range`.

This is the one Google surface where the quota is genuinely not the pool, and it needs a
Workspace account plus a Cloud project with the Chat API enabled. A personal `@gmail.com`
address is not enough.

The attachment cap, the quota exemption and the rate limit are all vendor documentation and
none of them was probed (`reported`, 2026-10-21).

Evidence: `https://developers.google.com/workspace/chat/api/reference` and
`https://developers.google.com/workspace/chat/limits` (2026-10-21), record
`dossier/storage/google-chat-spaces-as-a-quota-exempt-attachment-store.json`.
Verdict: `qualifies-with-caveat`.

### The consumer drives with an open foreign signup

Four drives in this class accept a foreign individual, and their quotas are small enough
that they are useful only as replicas.

MEGA gives 20 GB at signup plus achievement bonuses of 5 GB each, valid for 365 days. Its
real constraint is the transfer quota computed per IP over six hours, which throttles a
serving workload long before any volume is reached.

TeraBox gives 1 TiB free, which its own pricing page states as a gigabyte count of 1,024 in the free column, verified across ten localised front ends, with an email or
SSO signup and no country gate. The per-file cap is about 4 GB and the file count on the
free tier is capped, so 1 TB is unreachable at realistic object sizes.

InfiniCLOUD gives 20 GB free with a referral ladder to 1,000 GB, no file size limit, and a
2-year inactivity deletion. Its write feature is disabled on the free plan.

Gofile gives no storage figure at all, caps a free account at 10,000 contents, allows 100
GB of traffic per 30 days, and deletes after 10 days of inactivity.

Four records, and every quota above is the provider's own page. None of
the four was signed up for, so the identity column is a form read and not a registration
(`reported`, 2026-10-21).

### The video platforms used as bulk stores

This class re-encodes at ingest, so it is a delivery surface and not a store: the byte that
comes back is not the byte that went in (`reported`, 2026-10-21).

VK Video accepts up to 256 GB in a single uploaded file with no published per-account
total, and serves playback from its own CDN with no charge to the uploader. Rutube accepts
25 GB and 300 minutes per video with five concurrent uploads.

Both re-encode at ingest, so they hold video rather than arbitrary bytes. VK preserves the
original only if the uploader enables original-file download. Neither is storage in the
sense this corpus means, and both belong in the dead-end discussion of that class rather
than in a shard plan.

### RUTUBE

> 25 GB max per video, 5 concurrent uploads; no total per-account cap stated on the FAQ page read

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 25 GB max per video. The record states no identity cost. Observed behaviour: Ingest re-encodes, so this only stores video, not arbitrary bytes.

Evidence: `https://rutube.ru` (2026-10-21), record `dossier/storage/rutube.json`.
Verdict: `qualifies-with-caveat`.

### VK Video (video hosting as bulk store)

> up to 256 GB per single uploaded file; no per-account total published on the page read

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 256 GB single file. The record states no identity cost. Observed behaviour: Uploaded media may be transcoded.

Evidence: `https://vk.com/video` (2026-10-21), record `dossier/storage/vk-video.json`.
Verdict: `qualifies-with-caveat`.

### Azure for Students (and Azure for Students Starter)

> $100 credit per 12 months plus free monthly amounts of 20+ services; no credit card required. Explicitly renewable: 'Renew your subscription annually and continue to get free access to Azure as long as you're a student.' Starter tier...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Subscription is disabled at year end until renewed.

Evidence: `https://azure.microsoft.com/en-us/free/students` (2026-10-21), record `dossier/storage/azure-for-students.json`.
Verdict: `qualifies-with-caveat`.

### Blossom servers (blossom.band / blossom.nostr.build, run by nostr.build)

> 'Free uploads for everyone, from any Blossom-capable client.' 'A hard cap of 100 MiB per upload (20 MiB for free uploads), with no limit on the number of uploads or retention.'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MiB for free uploads (100 MiB only on the $18/yr plan). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: A ~19 MiB upload returned HTTP 500 'Error uploading the file: unknown error' while 5 and 15 MiB succeeded, so the usable ceiling is somewhat below the advertised 20 MiB.

Evidence: `https://blossom.band/` (2026-10-21), record `dossier/storage/blossom-servers.json`.
Verdict: `qualifies-with-caveat`.

### Walrus Testnet public publishers (Mysten Labs + community)

> No account, no key, no quota. Docs quote only a per-request limit: 'Most aggregators and publishers limit requests to 10 MiB by default'. In practice the reference publisher accepted 300 MiB and 1 GiB. Max storage duration is 53 epochs; on...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1 GiB verified write. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Testnet is periodically wiped without warning and publishers are volunteer-run (2 of 5 tested endpoints were down: h2o-nodes 502, atalma connection refused).

Evidence: `https://docs.wal.app/docs/system-overview/public-aggregators-and-publishers` (2026-10-21), record `dossier/storage/walrus-testnet-public-publishers.json`.
Verdict: `qualifies-with-caveat`.

### Atlassian Confluence Premium via Social Impact (nonprofit) License, unlimited file storage

> Confluence Premium = 'Unlimited file storage'. Atlassian's Feb 2026 announcement grants eligible nonprofits and social enterprises 100% off Confluence 'Standard or Premium up to 25 users' under the Social Impact License. So a verified...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: the binding constraint: 'The default size limit is 100 MB' per attachment.... The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Free Confluence sites can be deactivated for inactivity (login is the counter).

Evidence: `https://www.atlassian.com/teams/nonprofits/discount-pricing` (2026-10-21), record `dossier/storage/atlassian-confluence-premium-via-social-impact-license-u.json`.
Verdict: `qualifies-with-caveat`.

### AWS Activate (Founders / Portfolio)

> Founders tier: '$1,000 in AWS Activate Credits... Select startups may qualify for up to $5,000 over time'. Portfolio tier: 'up to $200,000 in AWS Activate Credits' for provider-backed (accelerator/VC) startups. Credits cover 'over 200...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: S3 request rates are effectively unlimited at this scale but each PUT/GET.... The record states no identity cost. Observed behaviour: Purely a spend credit: once exhausted, S3 reverts to paid and will bill the card on file.

Evidence: `https://aws.amazon.com/startups/learn/everything-you-need-to-know-about-aws-activate-credits` (2026-10-21), record `dossier/storage/aws-activate.json`.
Verdict: `qualifies-with-caveat`.

### Cloudflare for Startups, nonprofit / civil-society track

> Up to $350,000 in credits for a year on the current program page (tiered: Tier 3 $10k upward). The nonprofit track announced 2025-09-22 offers 'up to $250,000 in Cloudflare credits... which can be used for a variety of our developer and...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: Workers/API rate limits apply to control-plane calls. The record states no identity cost. Observed behaviour: Award is discretionary and cohort-based (501(c)(3) or equivalent required).

Evidence: `https://www.cloudflare.com/forstartups/` (2026-10-21), record `dossier/storage/cloudflare-for-startups-nonprofit-civil-society-track.json`.
Verdict: `qualifies-with-caveat`.

### Databricks Free Edition (default storage / Unity Catalog volumes)

> No published byte quota. Free Edition ships 'serverless compute and default storage, so you can immediately start exploring and building', default storage is 'a fully managed object storage platform' and in serverless workspaces you can...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: per-account serverless quotas ('Max of 5 concurrent job tasks per account'.... The record states no identity cost. Observed behaviour: Storage without a documented quota but also without a storage-native API, arbitrary bytes cannot be `PUT` without spinning compute, and compute is throttled to 'the rest of the day'.

Evidence: `https://docs.databricks.com/aws/en/getting-started/free-edition` (2026-10-21), record `dossier/storage/databricks-free-edition.json`.
Verdict: `trial-only`.

### Google for Startups Cloud Program (Start / Scale tiers)

> Scale and Scale AI tiers: '$200K - $350k in credits' for startups with verifiable Pre-Seed to Series A funding. Credits apply to 'most Google Cloud platform products... used in a pay-as-you-go (PayG) or consumption billed format', which...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: per-project GCS quotas (raiseable). The record states no identity cost. Observed behaviour: Requires a funded company, a matching domain email and a billing account owned by that domain.

Evidence: `https://cloud.google.com/startup` (2026-10-21), record `dossier/storage/google-for-startups-cloud-program.json`.
Verdict: `qualifies-with-caveat`.

### Microsoft Azure grant for nonprofits ($2,000/yr, renews)

> $2,000 (USD) in donated Azure services credits per year, renewable. Not a byte quota, a credit grant usable against 'the complete portfolio of Azure products and cloud services', which includes Blob Storage / Data Lake Storage Gen2 / Azure...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Blob block blob max ~190. The record states no identity cost. Observed behaviour: Missing the renewal window silently converts the subscription to pay-as-you-go and starts charging the payment instrument on file, a real cost hazard, not a data-loss hazard.

Evidence: `https://www.microsoft.com/en-us/nonprofits/azure` (2026-10-21), record `dossier/storage/microsoft-azure-grant-for-nonprofits.json`.
Verdict: `qualifies-with-caveat`.

### Gofile

> no storage figure at all on the free tier, free accounts get temporary storage with a 10,000-content cap per account ('Free accounts are capped at 10,000 stored contents'); free traffic allowance is '100 GB traffic / 30 days'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: deleted after 10 days of inactivity unless it k. The record states no identity cost. Observed behaviour: 10-day inactivity expiry plus cold-storage migration makes it storage-with-a-TTL, not a drive.

Evidence: `https://gofile.io` (2026-10-21), record `dossier/storage/gofile.json`.
Verdict: `qualifies-with-caveat`.

### InfiniCLOUD (formerly TeraCLOUD)

> 20 GB free account; referral bonus up to 1,000 GB for the referrer (+5 GB once for the referee). No file size limit

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: referral bonuses expire after a year for the referrer.

Evidence: `https://infini-cloud.net` (2026-10-21), record `dossier/storage/infinicloud.json`.
Verdict: `fails-quota`.

### Linkbox / TeleBox

> 5 GB on plain signup; 10 TB granted via 'Special Account Authentication' with an edu/gov email (third-party 2023 walkthrough, not re-verified on the vendor's own page)

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 1 MB/s. The record states no identity cost. Observed behaviour: origin times out repeatedly under a headless reader (504 deadline on /, /pricing, /admin/account), indicative of an unstable front end with automated-traffic filtering.

Evidence: `https://www.linkbox.to` (2026-10-21), record `dossier/storage/linkbox-telebox.json`.
Verdict: `qualifies-with-caveat`.

### Cloud.ru Evolution S3 free tier

> Free tier object storage: 15 GB standard + 1,000 GB cold + 3,000 GB ice, with 100k PUT / 100k POST on standard and 4,000 bonus roubles per block

That is the record's own wording (`inferred`, 2026-10-21). The record states no identity cost. Observed behaviour: the free tier is a promotional calculator allowance with an explicit 'for testing only' disclaimer, so treat any capacity as revocable.

Evidence: `https://cloud.ru` (2026-10-21), record `dossier/storage/cloud-ru-evolution-s3-free-tier.json`.
Verdict: `qualifies-with-caveat`.

### Datum Storage

> 1 TB free from signup ('Get 1TB Free Cloud Storage From Datum'), S3-compatible endpoint

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: app-gated identity makes account automation awkward.

Evidence: `https://storage.datum.org` (2026-10-21), record `dossier/storage/datum-storage.json`.
Verdict: `trial-only`.

### file.kiwi

> Web Folder Basic: 'No capacity limit. Auto-deleted 90 hours after upload.' API flow: 10 files per WebFolder, 999 GiB max per file

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 999 GiB/file. The record states no identity cost. Observed behaviour: 6-48 h download windows make it a transfer tool, not storage.

Evidence: `https://file.kiwi` (2026-10-21), record `dossier/storage/file-kiwi.json`.
Verdict: `qualifies-with-caveat`.

### Seznam.cz (email-as-storage)

> Mailbox is byte-unlimited: 'Uzivatel muze schranku vyuzivat v neomezene velikosti', with a 120,000-message cap that can be raised repeatedly

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 50 MB receive per message. The record states no identity cost. Observed behaviour: message-count cap plus per-message size cap is the real ceiling.

Evidence: `https://www.seznam.cz` (2026-10-21), record `dossier/storage/seznam-cz.json`.
Verdict: `qualifies-with-caveat`.

### TeraBox (Baidu / Flextech)

> 1 TiB free ('Network disk capacity limited to 1 TiB' on the free column; '1TB Free Cloud Storage for Basic & 2TB Storage for Pro'); Premium/Pro 2 TiB

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 4 GB/file. The record states no identity cost. Observed behaviour: no official rclone backend.

Evidence: `https://www.terabox.com` (2026-10-21), record `dossier/storage/terabox.json`.
Verdict: `qualifies`.

### MEGA

> 20 GB free at signup, plus stacking achievements of 5 GB each (desktop app, mobile app, per invite, VPN trial, Pass trial) valid 365 days

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: expire after 365 days. The record states no identity cost. Observed behaviour: Does not lose data.

Evidence: `https://mega.io/` (2026-10-21), record `dossier/storage/mega.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Cloud.ru Evolution Artifact Registry | fails-quota | 500 GB storage quota and 1 TB/month egress quota per organisation, but storage is billed, no free tier |
| GitVerse (Sber git hosting: LFS + releases + packages) | fails-quota | 2 GB Git LFS per user AND per org (monthly), 4 GB release assets per user/org, 500 MB packages per user/org |
| Mail.ru Cloud (Mail) + Mail Space (`Облако`) | fails-quota | 8 GB free per account; 1 TB only as a paid Mail Space plan (1 560 RUB first year, 3 000 RUB/yr after) |
| VK Cloud Object Storage | fails-egress | no perpetual free volume, pay-as-you-go per GB, per storage class (Hotbox/Icebox/Backup) |
| Yandex Disk (+ Yandex 360) | fails-quota | 5 GB free per account (shared with Yandex Mail attachments); paid 200 GB-2 TB from 319-699 RUB/mo |
| Yandex 'unlimited photo storage' (auto-upload) | fails-quota | unlimited photos/videos, but only with an active paid Yandex 360 plan... |
| Alibaba Cloud OSS, new-user free trial | trial-only | Current international page: 'Standard LRS resource plan: 500 GB for 1 month' (individual) / '1 TB for 1 month'... |
| Amazon CloudFront free tier... | fails-quota | 1 TB/month data transfer out + 10,000,000 HTTP/HTTPS requests + 2,000,000 CloudFront Function invocations... |
| AWS Free Tier, S3 (current, post-2025 restructure) | trial-only | No perpetual S3 storage allowance remains in the current published Free Tier. What exists now: up to $200 in credits... |
| Google Cloud Free Tier, Cloud Storage | fails-quota | 5 GB-months of regional storage per month (us-east1/us-west1/us-central1 only), 5,000 Class A ops, 50,000 Class B ops... |
| Huawei Cloud OBS, free packages | fails-quota | Time-limited new-user packages only: OBS Single-AZ 100 GB for 12 months (regions CN-Hong Kong, AP-Bangkok, AP-Singapore... |
| IBM Cloud Object Storage, Standard plan Free Tier | fails-quota | 5 GB/month of Smart Tier storage, 2,000 Class A + 20,000 Class B requests, 10 GB/month retrieval, 5 GB/month egress... |
| Microsoft Azure Free Account, Blob Storage | fails-quota | 5 GB LRS hot block blob with 20,000 read + 10,000 write operations... |
| Tencent Cloud COS, new-user free tier | fails-egress | 50 GB STANDARD storage capacity, valid 6 months (180 days)... |
| 4EVERLAND (IPFS + S3-compatible Bucket) | fails-egress | Standard free package: 'IPFS Storage: 6 GB/month', 'Arweave Storage: Total 100 MB', 'Bandwidth: 10 GB/month'... |
| Crust Network (free Web3Auth IPFS gateway + on-chain... | fails-egress | Gateway writes are described as 'free' but need a signature... |
| Edge Network Storage | fails-quota | Free tier: '2 buckets / 5 GB storage / S3-compatible API / Zero egress fees' |
| Fil One (formerly Storacha / web3.storage successor) | trial-only | No standing free tier: '1 TB free for 30 days - No credit card required' and '1 TB of storage and 2 TB of egress for 30... |
| Impossible Cloud | trial-only | No free tier, '5 TB Cloud Storage Free for 30 Days' trial... |
| Irys (devnet bundler) | fails-quota | Devnet uploads are paid with free faucet tokens; 'Devnet... data retention lasting approximately 60 days before deletion'... |
| Lighthouse (Filecoin/IPFS pinning) | fails-quota | Filecoin plans, Free: 'Total Storage: 5 GB' (IPFS + Filecoin). Walrus plans... |
| Sia Storage (hosted indexer, sia.storage) | fails-quota | 50 GB free, 'The free plan includes 50 GB of storage, up to 3 connected apps, and transfer speeds up to 524 Mbps... |
| Storj DCS | trial-only | No free tier left. Current page: 'Free trial, $0, Free for 30 days... No credit card required'... |
| Box for Nonprofits, donated Starter... | fails-quota | Box Starter, free for nonprofits via TechSoup validation: 'Secure file collaboration... |
| Snowflake 30-day trial ($400 credits) | trial-only | $400 in free credits on a 30-day trial ('Start your 30-day Snowflake trial today. Get $400 in credits'). No byte quota... |
| Cloud Storage for Firebase (Spark/Blaze) | fails-quota | 5 GB stored free, but only on the Blaze pay-as-you-go plan; Spark project buckets return 402/403 |
| Google Cloud Storage Always Free tier | fails-quota | 5 GB-months of regional storage (US regions only) + 5,000 Class A ops + 50,000 Class B ops per month |
| Google Photos Library API (append-only upload) | fails-quota | No quota of its own, but every item uploaded counts against the user's Google Account storage at original quality... |
| Filen | fails-quota | 10 GB free (10 GiB at signup) |
| Shade | fails-quota | 20 GB free account (stated in rclone's own backend docs) |
| Azure Blob Storage always-free tier | fails-quota | 5 GB LRS hot block storage, with 20,000 read and 10,000 write operations per month... |
| Azure Container Registry (Basic / free 12-month... | trial-only | Basic SKU includes 10 GiB storage; Standard includes 100 GiB... |
| Azure DevOps Artifacts (Universal Packages) | fails-quota | 2 GiB free storage per organization; Universal Packages up to 4 TiB per file |
| Microsoft Fabric trial capacity / OneLake | trial-only | 1 TB of data in OneLake, free for 60 days |
| Microsoft Teams (free / personal) | fails-quota | 5 GB free per person for files in Teams for personal use; images/videos explicitly do not count and have no storage limit... |
| OneDrive consumer (Microsoft account) | fails-quota | 5 GB free per Microsoft account; paid tiers 100 GB / 1 TB / 2 TB |
| Mail.ru Cloud | fails-quota | 8 GB free, now a single pool shared between and |
| Hi168, S3-compatible object storage (`上海海文`) | fails-quota | 500 GB on registration, 1 TB after real-name verification. Forum dealers advertised it as '1T' in Jan 2026... |
| 4shared | fails-quota | 15 GB free per account |
| Box (free developer plan) | fails-quota | 10 GB storage, 250 MB file upload limit, 1 file version |
| ggdriive.com | fails-quota | 20 GB free; 'ILIMITADO PRO' marketed as unlimited (paid) |
| OpenDrive | fails-quota | 5 GB free (100 MB max file size, 1 GB/day bandwidth); 'Unlimited' storage/bandwidth/file-size starts at $12.95/month |
| Proton Drive | fails-quota | 5 GB free (starts at 2 GB, +3 GB welcome checklist within 30 days) |
| Zoho WorkDrive | fails-quota | 5 GB free forever on the Individual plan |

The failures in this class are mostly about the tenant rather than the quota, and that is
the finding. The largest group is quota: a consumer drive that advertises 1 TB and caps
the file count, or a credit programme whose grant is a spend cap rather than a byte
allocation. The second is trial-only: a credit that expires in 12 months is not a free
tier, and the corpus counts 8 of them here.

The identity failures are the ones worth reading, because they are the class this
document is about. An education tenant, a nonprofit grant and a startup credit programme
all fail for the same reason: each needs an institution. A quota behind
an organisation is worth zero here.

## Chaining

A tenant is the base of the bridge pattern, not a replica. The working shape is a pooled
tenant mounted by AList or OpenList, fronted by Cloudflare, and read through a signed URL
that supports `206`.

The trap is that the tenant's identity is also the tenant's administrative control:
sharing outside the domain can be disabled by an administrator, and a workspace can be
suspended for inactivity with no notice. A pool built on a borrowed tenant needs a local
copy of the metadata index, because the index is the one part no administrator can take
away.
