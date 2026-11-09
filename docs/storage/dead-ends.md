# Dead ends: every provider this topic rejected, grouped by the failure that binds

A dead end is a deliverable. It is the only thing that stops the same closed door being opened twice.

This page carries both halves of the topic's dead ends: **480** rejected records that also hold a row in the provider table, and **847** that exist only in the dead-end list. That is **1327** providers, each with a record under `dossier/storage/` carrying the verdict and the reason of its failure. The rung is not uniform: of the 1329 rejected records, 1305 are `reported`, 19 `inferred`, 4 `documented` and 1 `unverified`. A `reported` rejection is a third party's verdict, not a failure reproduced here, so "each with a record" is a statement about provenance and not about checking.

The table's rows are a count of records and not a count of rejections. Of the 480 with a provider-table row, 37 also appear in the table as a qualifying provider, which is what the section below is about.

## How the class is assigned

The class is the record's verdict where it has one: `fails-egress` becomes `egress`, `fails-identity` becomes `identity`, `trial-only` stays, and so on. Where the verdict is `fails-quota` the reason text is read, because "too small" and "deleted in 90 hours" are different findings that a single verdict collapses.

A provider whose reason names two failures gets one class: the one that would stop the workload first. The order is dead service, then identity, then a gated read, then a gated write, then retention, then egress, then a trial clock, then a category error, then price, then size. That order is a judgement, and it is written here so a reader can disagree with it.

## The size of each graveyard

| class | what it means | table rows | dead-end only | total |
|---|---|---|---|---|
| `dead-service` | the host is gone, parked, seized or sunset | 7 | 107 | 114 |
| `identity` | the quota is real and a reader cannot register | 3 | 18 | 21 |
| `read-gated` | the write works and the read returns nothing or different bytes | 0 | 5 | 5 |
| `write-gated` | a curator, review, invite or build recipe stands in front | 11 | 25 | 36 |
| `retention` | the bytes are deleted on a clock | 29 | 43 | 72 |
| `egress` | the read path is metered, shaped or absent | 42 | 63 | 105 |
| `trial-only` | a clock, however large | 0 | 0 | 0 |
| `not-storage` | a category error: compute, a catalogue, a metadata index | 7 | 38 | 45 |
| `paid` | it works, and only at a price above the floor | 16 | 42 | 58 |
| `quota` | the free allowance cannot reach 500 GB per unit | 365 | 506 | 871 |
| **total** | all classes | **480** | **847** | **1327** |

This table classifies by `failure_class`, which is not the record's `verdict` and is not
a partition of the same set. Two consequences follow. `trial-only` is
zero in both columns because the dead-end list never assigned that class: the 28 records
whose *verdict* is `trial-only` are not dead ends, and they are counted in the provider tables
instead. `identity` has 3 table rows and 18 dead-end-only ones.

## What the classes mean for a plan

Three of them change a decision and the rest are bookkeeping.

`read-gated` is worse than a dead service, because the write succeeds and the loss arrives later. FileDitch accepts 155 GiB and returns 503 to every non-browser client. Every AList instance that advertised a writable mount refused the PUT with `{"code":403}` inside an HTTP 200. A host that keeps bytes but will not return them is a one-way sink.

`retention` is the class that looks like a win, because the per-object caps there are the largest in this topic. file.kiwi takes 999 GiB and deletes it after 90 hours. firestorage.jp takes 300 GiB and deletes it after 3 days by default, 14 at most. A reader who sorts by cap and stops has sorted by the wrong column.

`not-storage` is the most common mistake in the corpus. Korean webhard sites sell per-download credit rather than storage. Print-on-demand takes unlimited ingress with no read path. A metadata harvester holds no bytes. None of these is a small provider; each is the wrong shape.

## The 37 providers that are on both lists

Thirty-seven names appear as a provider-table row and as a dead end, and nine of them qualify in the table. They are recorded individually rather than resolved, because a provider that qualified once and failed later is a fact about how fast this market moves. The nine that qualified are `akamai/linode object storage`, `contabo object storage`, `file.kiwi`, `neurovault`, `nuget.org`, `oracle cloud infrastructure registry`, `ovhcloud object storage cold archive`, `synology c2 object storage` and `wasabi hot cloud storage`. Each carries a `conflicts[]` entry in its record.

## `dead-service`: the host is gone, parked, seized or sunset (2)

| provider | verdict | why it fails |
|---|---|---|
| fal.ai persistent /data volume | fails-quota | No published byte quota on the /data volume, the docs state only 'Files written to /data persist between requests, across runner restarts, and across deployments' and 'Files you write there persist... |
| Fshare / FshareStorage (fshare.vn, FPT Telecom) | fails-quota | Free tier: 50 GB of 'dung lng khong dm bo' (non-guaranteed capacity). From 2027-01-01 the platform rebrands to FshareStorage, guaranteed capacity rises 50 GB -> 100 GB, and **the free account tier is... |

## `identity`: the quota is real and a reader cannot register (26)

| provider | verdict | why it fails |
|---|---|---|
| (mbd.pub) (`面包多`) | fails-identity | Their help centre says '(<1G)', unlimited file hosting, with a per-file note of <1 GB. So: unlimited total, 1 GB per object |
| AWS Open Data Sponsorship Program (revisit) - uncapped, 2... | fails-identity | No published byte limit; AWS pays S3 storage plus egress and cross-region fees for the approved dataset, in a dedicated Program Account joined to AWS's billing organisation. 2-year term from the... |
| Chameleon Cloud (TACC / UChicago) | fails-identity | 534 nodes across KVM@TACC, CHI@UC, CHI@TACC, CHI@NRP; 62 nodes with >1TB total storage, dedicated 'storage' (20) and 'storage_nvme' (10) node classes, plus 297 nodes at 400GB-1TB |
| CloudLab c240g1 / per-node local blockstore (40 TB) | fails-identity | c240g1 node type = 12 x 3 TB HDDs (36 TB raw) on 5 nodes at Wisconsin; the storage table prices a 'per-node local blockstore' at 90GB-40TB, so a multi-TB blockstore is requestable by size in the... |
| CloudLab persistent remote dataset (10 TB, iSCSI) | fails-identity | up to 10 TB per persistent remote dataset; pool is 500 TB at Utah, 160 TB at Wisconsin, 40 TB at Clemson. Anything over 1 TB 'likely to require administrative approval'; long-term datasets are... |
| DaRUS (Universitat Stuttgart) | fails-identity | No quota defined at root |
| data.boston.gov (City of Boston, Socrata/CKAN hybrid) | fails-identity | 235 datasets, 32 organisations, 0 unowned. Portal-hosted /download/ paths (tmp05gz_hzf.csv etc.) |
| data.gov.ie (Ireland) | fails-identity | 22,883 datasets, 172 organisations. No published per-user quota |
| data.gov.il (Israel, CKAN) | fails-identity | 1,203 datasets, 61 organisations. Files self-hosted (/dataset/.../download/datafile.csv) |
| data.gov.ro (Romania national portal) | fails-identity | 5,255 datasets across 181 organisations. Files are hosted on-portal, not linked out: resources resolve to /dataset/<uuid>/resource/<uuid>/download/<name>.xls. No per-user quota is published |
| data.gov.ua (Ukraine national portal) | fails-identity | No published quota. Files self-hosted at /dataset/<uuid>/resource/<uuid>/download/<file> |
| data.govt.nz (New Zealand) | fails-identity | CKAN API answers 200 but the payload is replaced by an Incapsula/Imperva JS challenge wrapper on the HTML side; dataset count not machine-readable through this path |
| data.qld.gov.au (Queensland Open Data Portal) | fails-identity | 188,887 datasets. No published per-user or per-file quota. Resources split between portal-hosted /download/ paths and agency app endpoints (apps.des.qld.gov.au) |
| DataverseNL | fails-identity | no quota defined (API); effectiveDatasetFileCountLimit=10000, the highest file-count ceiling seen in the sweep |
| DataverseNO (UiT The Arctic University of Norway,... | fails-identity | No quota defined at root, 2,311 datasets, 32 collections |
| DICE / EUDAT cost-free storage call (the EU's... | fails-identity | Not published as a number, DICE is a funding instrument, not a product. It buys 'personal drive storage' up to long-term preservation, priced by negotiation with whoever provides it. The EC put... |
| DSpace 7+ platform class (MIT, UCT, demo.dspace.org and... | fails-identity | NO QUOTA CONCEPT AT ALL. The string 'quota' does not appear once in DSpace's 2,125-line dspace.cfg; the only two hits repo-wide are a Solr query-parser class and a discovery.cfg comment. There is no... |
| EPrints 3.x platform class (White Rose, QUT, Southampton) | fails-identity | No quota model. EPrints has no per-user or per-collection byte accounting; the only constraints are the JavaScript max on the upload widget and Apache's LimitRequestBody |
| Europeana (EU cultural heritage aggregator) | fails-identity | No direct deposit at all, Europeana ingests metadata via accredited national aggregators; the media object stays on the provider's own server and is only linked |
| FABRIC testbed | fails-identity | VMs up to 64 cores / 384 GB RAM with directly attached NVMe, GPUs, SmartNICs; 'large storage volumes'; facility holds 'between 1/2 and 1PB of file storage space' for experiment data, plus... |
| GRO.data (Gottingen) | fails-identity | no quota defined (API) |
| Helix (Imperial College London, launched 2025-26) | fails-identity | No published per-record or per-user quota; the live API already serves a 13.58 GB single object and four objects over 6 GB, so per-object caps are at least ~14 GB. 40 records total, a very new... |
| InvenioRDM platform class, CaltechDATA, TU Graz, TU Wien,... | fails-identity | Per-record, NOT per-account: RDM_FILES_DEFAULT_QUOTA_SIZE = 10 GB and RDM_FILES_DEFAULT_MAX_FILE_SIZE = 10 GB, with APP_RDM_DEPOSIT_FORM_QUOTA maxFiles = 100. Records are unlimited. This is the... |
| Nakala (Huma-Num, France) - no formal size limit, but a... | fails-identity | 'There is no formal limitation on the size of data deposited'; above ~10 GB per file the depositor must contact the Nakala team first. Private pre-publication space is capped far lower (9,999 items or 100 GB),... |
| NASA Earthdata AWS allocation (2 PB pool via Space Act... | fails-identity | A 2 PB storage allocation held by NASA's Earth Science Division inside the AWS Open Data Program, subdivided by request. Individual allocations are not published; requests are reviewed monthly (1st)... |
| Together AI Files API (with 100 GB fine-tune objects) | fails-identity | 100 GB per training file (JSONL or Parquet); SDK constant MAX_FILE_SIZE_GB = 50.1 and MULTIPART_THRESHOLD_GB = 5.0. No published total-storage quota |

## `read-gated`: the write works and the read returns nothing or different bytes (1)

| provider | verdict | why it fails |
|---|---|---|
| iNaturalist | fails-quota | No per-account quota published or enforced (395,436,915 observations live at time of probe). But per-object: 20 MB/file upload cap, AND every image is re-encoded to a 2048 px longest edge, so the... |

## `write-gated`: a curator, review, invite or build recipe stands in front (8)

| provider | verdict | why it fails |
|---|---|---|
| Audiovisual / heritage: Open Heritage 3D (CyArk + UC San... | fails-quota | No published quota. The project is a consortium repository, 'we invite others to join the Open Heritage 3D project and contribute their datasets', with 200+ datasets and DOIs under the 10.26301... |
| Codeberg Pages (git-pages) | fails-quota | No hard quota: 'there is no quota for valid use-cases', with a soft review threshold at 750 MiB Git storage and 1.5 GiB packages/LFS/attachments per account |
| CTAN (Comprehensive TeX Archive Network) | fails-quota | No numeric quota published, but upload is a *manual web form* reviewed by the CTAN team, with extensive packaging rules (TDS layout, no.git, no editor backups, symlinks preferred over copies). There... |
| CyVerse Data Store | fails-quota | 5 GB default for every account, explicitly for 'all domestic and international CyVerse account holders'. Above that it is paid: $125/TB/year single-copy up to 4 TB, $105/TB/year beyond, and... |
| Fastly free account + Fast Forward OSS programme | fails-quota | Free account: 100 GB bandwidth/month free across all regions, 1M CDN requests/month, 5 domains, 100K purge requests. Above 100 GB: $0.12/GB EU/NA, $0.19/GB Asia/Australia, $0.28/GB Africa/India/South... |
| FileLu | fails-quota | 1 GB free; +20 GB by leaving reviews (support ticket); referral rewards '100 referrals gives you 100GB', 'Maximum reward: 1TB storage' |
| Flathub (dl.flathub.org OSTree repo) | fails-quota | No published storage quota for published applications. This is a deduplicating OSTree/OCI repo: apps are stored as content-addressed ostree commits, so identical files across apps are stored once.... |
| Veilid (self-hosted) | fails-quota | no quota and no account, 'All Veilid applications running veilid-core are nodes, and they are all equal in the eyes of the network. No nodes are special. Nodes are only limited by the resources they... |

## `retention`: the bytes are deleted on a clock (30)

| provider | verdict | why it fails |
|---|---|---|
| AWS CodeArtifact | fails-quota | First 2 GB of storage and first 100,000 requests per month free, a recurring monthly allowance, described on the pricing page as 'a monthly AWS Free Tier for storage and requests', with no 12-month... |
| Blaze (BLAZE Quantum) | fails-quota | Free Forever: 2 GB transfer with 7-day retention, plus 2 GB of BLAZE Drive storage, 2 workspaces, 2 upload portals. Starter EUR 6/user/mo: 100 GB transfer / 30-day retention / 100 GB Drive |
| Blossom blob servers (nostr.download,... | fails-quota | Per-object caps only, and small: nostr.build free uploads 20 MiB, hard cap 100 MiB, then storage plans 5 GB / $18/yr up to 500 GB / $240/yr. 24242.io: 100 MiB max file, files deleted after 60 days... |
| CircleCI artifacts | fails-quota | No storage quota advertised on Free (30,000 credits/month). Artifact retention default AND maximum is 30 days on Cloud; storage usage is a billed meter, not an allowance |
| Codemagic artifacts | fails-quota | 500 free build minutes/month on macOS M2 (individuals). No free storage allowance advertised. Artifact retention is per-team policy; Enterprise default is 1 year |
| Comet ML (Comet / Opik), artifact + dataset management | fails-quota | No storage allowance at all on the free tier. The free cloud plan is metered in spans, not bytes: 'Up to 10 team members - 25k spans per month - 60-day data retention'. Artifact/dataset management is... |
| Copernicus Data Space Ecosystem (CDSE / ESA DIAS) - 12... | fails-quota | 12 TB per rolling 30 days of download via S3/OData/STAC for a Copernicus General User, 20 MB/s per connection, 4 concurrent connections, 2,000 requests/min, empty-account registration. After the... |
| Eternal September (news.eternal-september.org), free NNTP... | fails-quota | No byte quota. Free read AND write access to all *text* newsgroups after online registration. 281 hierarchies, alt.* alone is 8,728 groups, free.* is 1,284. Retention: '3 years for de.*, 160 days for... |
| File Garden | fails-quota | free, 'forever' retention; per-file and per-account caps not published on the landing page |
| Filebin | fails-quota | no account; per-bin, no published byte cap; bins expire 6 days after creation |
| Filemail | fails-quota | 5 GB per transfer with no registration; 2 transfers per 24 hours; 7-day retention. Paid: Pro 250 GB/transfer, Business/Enterprise 'unlimited file size', and only Business/Enterprise can pick... |
| Google Gemini Files API (AI Studio) | fails-quota | 20 GB per project; 2 GB per file; 48-hour retention |
| Huawei Cloud OBS, free packages | fails-quota | Time-limited new-user packages only: OBS Single-AZ 100 GB for 12 months (regions CN-Hong Kong, AP-Bangkok, AP-Singapore, AF-Johannesburg) per the package listing; a separate enterprise-verified 500... |
| IBM Cloud Object Storage, Standard plan Free Tier | fails-quota | 5 GB/month of Smart Tier storage, 2,000 Class A + 20,000 Class B requests, 10 GB/month retrieval, 5 GB/month egress, for 12 months. The separate Lite plan (always-free, never expires) does not carry... |
| Irys (devnet bundler) | fails-quota | Devnet uploads are paid with free faucet tokens; 'Devnet... data retention lasting approximately 60 days before deletion'. Mainnet has no free allowance, storage is metered per byte-second |
| Mage.space uploads | fails-quota | 100 MB per upload, 30-day life. No account-level storage allowance is offered |
| Mail.ru (VK) | fails-quota | 8 GB free: ', 8 '. The historic 100 GB-for-beta-testers grant was cancelled in Nov 2024; accounts drop to 8 GB after 6 months of inactivity |
| MASV | fails-quota | 15 GB of free transfer every month plus 5 days of free storage per package. Credit card with a $10 pre-authorisation required at signup |
| PacketStream (buy side) | fails-quota | $1.00/GB, $50 minimum purchase, balance never expires |
| paste.gg | fails-quota | 10 MiB total per paste, 5 MiB per file. Anonymous pastes expire after 7 days; signed-in pastes can be permanent. Built on Cloudflare Workers |
| Replicate (r8.im + Files API) | fails-quota | Files API is a workspace scratch space with no advertised total; documented behaviour is expiry, not quota. r8.im is a private-ish OCI registry for cog models |
| Sendbird Chat (free plan) | fails-quota | Pricing page advertises 'Message storage: Unlimited' on the free tier, a number that is immediately contradicted by the retention row on the same page |
| SendGB | fails-quota | 5 GB per transfer, no account, unlimited number of transfers (no monthly 10-transfer cap). Retention size-dependent, up to 90 days for small files. Paid one-shots: Exceed (up to 1 TB, 7 days, no... |
| storage.to | fails-quota | No permanent free storage: anonymous 100 GB upload / 24h per visitor token (500 GB / 24h per IP), free-account token = unlimited upload bandwidth and no daily file cap, but every free file expires in... |
| temp.sh | fails-quota | no account; 4 GB per file, 3-day retention |
| TransferNow | fails-quota | 5 GB per transfer, no sign-up, 7 days, and the free plan is explicitly labelled 'No storage'. Premium EUR 6/mo = 250 GB/transfer, 365 days, 1 TB storage. A separate API/SDK tier advertises up to 5 TB... |
| Twilio Programmable Messaging, Media subresource | fails-quota | No quota, media is retained indefinitely. The docs say Twilio 'retains the stored media until you delete the related Media subresource instance', i.e. retention is customer-controlled and unbounded... |
| Wayback Machine, Save Page Now 2 (capture API) | fails-quota | No storage quota; the cap is per-object at 2GB ('Max resource size = 2GB') and 100,000 captures/day for authenticated users (4,000/day anonymous in the 2022 spec). Retention is effectively permanent |
| Zoom Team Chat, files API | fails-quota | No storage quota obtained. Zoom's chat-files docs were not readable through any allowed path (empty reader output, no retention number) |
| ExaVault (Files.com), free self-hosted appliance | fails-quota | The hosted product is gone. What is free is the *appliance*: unlimited capacity on the disk it runs on, licensed for up to 50 users, no expiry, no throttling. There is no free hosted storage at all |

## `egress`: the read path is metered, shaped or absent (76)

| provider | verdict | why it fails |
|---|---|---|
| 4EVERLAND (IPFS + S3-compatible Bucket) | fails-egress | Standard free package: 'IPFS Storage: 6 GB/month', 'Arweave Storage: Total 100 MB', 'Bandwidth: 10 GB/month', resets on the 1st. Separate 7-day Trial: 1 GB IPFS, 10 MB Arweave, 1 GB bandwidth |
| AkiraBox | fails-egress | unlimited storage advertised; 5 GB/file anonymous, 20 GB/file with a free account |
| Amazon DynamoDB | fails-egress | 25 GB of storage, always free (does not expire), plus 25 WCU and 25 RCU provisioned capacity and ~200M requests/month |
| Anthropic Claude Files API | fails-egress | 1 TB per organization; 500 MB per file; files persist until deleted or until expires_at |
| Appwrite Cloud | fails-quota | 2 GB storage + 5 GB bandwidth on Free; 2 projects |
| Baseten Delivery Network (BDN) model weight mirrors | fails-egress | No published per-account storage number. BDN 'mirrors model weights to Baseten and caches them near your replicas'; there is no documented quota and no free tier stated. Sized for 'a few GB or less'... |
| Bilibili video upload | fails-egress | 8 GB per video reported for most accounts; some accounts higher (third-party guide, not vendor docs) |
| Boosty (RU) | fails-egress | 20 GB per attached video (official FAQ post: ' 20 '). Community reports the effective limit was cut to 1 GB at one point (2025-07 post: '... 1 ') |
| Cisco Webex, Messages API file attachments | fails-egress | No storage quota published. Per-attachment cap is the only hard number: 'Message attachments are limited to 100MB each.' |
| Cloud.ru Evolution Artifact Registry | fails-quota | 500 GB storage quota and 1 TB/month egress quota per organisation, but storage is billed, no free tier |
| Cloudinary (free plan) | fails-quota | 25 monthly credits. 1 credit = 1 GB managed storage OR 1 GB CDN bandwidth OR 1,000 transformations, mixable. So max 25 GB if every credit is spent on storage and nothing is served |
| Convex | fails-quota | 1 GB file storage on Free; 1 GB/month file egress; 0.5 GB database; 40 deployments |
| Crust Network (free Web3Auth IPFS gateway + on-chain... | fails-egress | Gateway writes are described as 'free' but need a signature; the storage quota itself comes from a Discord channel, not a published number: 'Get free storage quota: 1. Join Crust discord 2. Follow... |
| DeepSeek Files API | fails-egress | 25 GiB per user, 10,000 files, 64 MiB per file. Permanent if `expires_after` is omitted; otherwise 1 hour - 30 days |
| DocDroid | fails-egress | Free/Standard account: 10 uploads per 24h, no document-count or storage figure published; Pro is "Unlimited Documents" for $19/month (3-day trial). Home page now flags free uploads as "Restricted... |
| Edge Network Storage | fails-quota | Free tier: '2 buckets / 5 GB storage / S3-compatible API / Zero egress fees' |
| Ethereum blobs (EIP-4844) as a storage layer | fails-egress | No free tier. Live cost at time of check: $0.012 per MB as blobs (vs $11.01/MB as calldata). 128 KB per blob package, separate blob fee market |
| Filebase (IPFS tier) | fails-quota | Free: 5 GB pooled storage across Object Storage and IPFS, 500 pinned files, 10 GB/month IPFS bandwidth, object egress free. Pro $7.50/mo: 500 GB pooled |
| Filecoin Plus DataCap (faucet + allocators) | fails-egress | 1 TiB of free DataCap per verified client, instantly, via Gitcoin Passport (score >= 20) on Optimism. Fil+ allocators can grant more. DataCap is a one-time, non-transferable credit, 'If a client... |
| Firebase Realtime Database | fails-egress | 1 GB stored on the Spark (no-cost) plan; 10 GB/month downloaded (~360 MB/day) |
| Firebase Storage (Cloud Storage for Firebase) | fails-egress | 5 GB stored on Spark (no-cost) plan; 1 GB downloaded per day; 50k download ops/day |
| Folder Fort 2.0 | fails-quota | Free plan exists with no credit card, size not published on the pricing page; free-plan bandwidth is 10 GB/month. Paid Personal starts at 100 GB, Business 1 TB |
| FolderFort, free tier + 2.0 pricing | fails-egress | Free plan with encrypted storage, no card; '+25GB free' if the account posts a social-media review. Paid Personal from 100 GB; Business up to 2x storage in bandwidth |
| Git LFS | fails-quota | Free: 10 GiB storage AND 10 GiB bandwidth per month; per-file 2 GB on Free/Pro, 4 GB Team, 5 GB Enterprise |
| GitHub Pages (Fastly-served, 1 GB site) | fails-quota | "Published GitHub Pages sites may be no larger than 1 GB"; source repositories "recommended limit of 1 GB". Bandwidth: "a *soft* bandwidth limit of 100 GB per month" |
| Google Artifact Registry (incl. the gcr.io domain) | fails-egress | 0.5 GiB-month, once per billing account, shared across every project on it: 'Artifact Registry Storage / 0 gibibyte month to 0.5 gibibyte month / $0.00 (Free) / 1 gibibyte hour, per 1 month /... |
| IEEE DataPort - 2 TB per dataset free upload, but every... | fails-egress | 2 TB of AWS S3 cloud storage per dataset for individual users (10 TB for institutional subscribers). No published limit on the number of datasets. Standard (non-Open-Access) deposit is free; making... |
| ImageShack | fails-egress | Free account with no published image-count or total-byte cap; the metered axis is bandwidth, not storage. 'Paid subscriptions don't impose a fixed file-count limit', and free is the same shape |
| IngramSpark | fails-egress | 1.5 GB via web upload ('web upload for files up to 1.5 GB, zip/stuff compression accepted'); user guide says files should not exceed 1.6 GB; ebook interiors 100 MB or less |
| InterServer Storage Hosting ST 600 (20 TB) | fails-egress | 200 GB $3 - 1 TB $5 - 2 TB $8 - 4 TB $10 - 10 TB $25 - 20 TB $42, all per month |
| IONOS CLOUD Object Storage | fails-egress | Per-GB-month; "Just 4.99 Dollar per TB for 30 days"; multi-region redundant |
| IPFS Foundation public gateways (ipfs.io / dweb.link /... | fails-egress | No storage at all, gateway only. And the gateway itself is being retired: ipfs.io/dweb.link return HTTP 429 with 'Retry-After: 900' and 'Sunset: Mon, 21 Sep 2026', and redirect browsers to... |
| Katfile | fails-quota | No free storage quota published; premium advertises 'Download files up to 200 GB' and bandwidth blocks up to 18 TB |
| Keep2Share / TezFiles (same operator) | fails-egress | Free plan: 10 GB/day of download traffic, no storage quota published. Paid Premium Max: 100 GB/day. Both are download-traffic products, not storage products |
| KeyCDN Push Zone (CDN storage) | fails-egress | Unlimited volume. Push Zone storage '$0.12/GB per month and charged on a daily basis' = **$120/TB/mo**. Tiered down to $0.04/GB above 1 TB/month of stored bytes |
| Lex.st, 150 GB free storage box 'for the life of the... | fails-quota | 150 GB HDD RAID-6 (NVMe cached), 1000 GB bandwidth, 2 domains, jailed SSH, DirectAdmin, Salt Lake City, free permanently |
| Lulu | fails-egress | No hard file limit. Own help page: 'We technically do not have a file limit for projects; however, the larger a file is, the longer it will take to process. We recommend keeping your interior file... |
| Netlify Blobs | fails-egress | Object store with 5 GB max per object, but the Free plan is 300 credits/month where 1 GB of web bandwidth = 20 credits, i.e. ~15 GB of transfer/month total, shared with every other metered feature |
| Nutstore (jianguoyun.com) (`坚果云`) | fails-quota | Traffic-based, not capacity-based: '1GB3GB'. Space grows with what is uploaded and is bounded by the traffic allowance, so effective free storage 1 GB/month of net new data |
| OpenDrive | fails-quota | 5 GB free (100 MB max file size, 1 GB/day bandwidth); 'Unlimited' storage/bandwidth/file-size starts at $12.95/month |
| OpenRouter Files API (workspace files) | fails-egress | 10 GiB per workspace, stated verbatim: 'Each workspace can store up to 10 GiB in total. When the workspace is full, uploads return a 403 error.' |
| Packagecloud.io, Free plan | fails-quota | 2 GB storage + 10 GB bandwidth per month, unlimited repositories and unlimited CI/CD minutes. Private repositories are no longer usable on the free plan (restricted since 7 Sep 2023), so the free... |
| Perplexity Projects (formerly Spaces), persistent file... | fails-egress | 5 GB per Project, 10,000 files per Project, 100 MB per file, identical on every plan, including free. Projects themselves: 'There's no limit on how many Projects you can create.' |
| PikPak Global Premium (10 TB) | fails-egress | 10 TB storage on Premium; additional storage purchasable |
| Pinata, dedicated gateway (free plan) | fails-egress | 1 dedicated gateway included on Free; serves only CIDs pinned to the account unless a Gateway Access Control is added. 10 GB/month bandwidth, 10,000 requests/month on Free |
| Pixiv | fails-egress | No published total quota; per-post caps only. Effectively unlimited posts |
| Rapidgator | fails-quota | Free: 5 GB upload per file, no storage allowance published; files kept 30 days from last download. Premium sells storage explicitly as a metered block: 6 TB / 12 TB / 24 TB with matching bandwidth |
| Replit (App Storage) | fails-egress | No free storage allowance. App Storage is metered: $0.015/GiB/mo storage, $0.05/GiB data transfer, $0.0004/1k basic ops |
| Scaleway Container Registry (public images) | fails-egress | Public images are free up to 75 GB of storage; private images are EUR 0.027/GB/month: 'Public images / Free up to 75GB /... / Free'. The FAQ repeats it verbatim with dated validation ('validation:... |
| Scribd | fails-egress | 100 MB max per document; no published account-level document or storage cap ("you can continue to upload more documents... as often as you like"). Effectively per-record 100 MB x unlimited records |
| Selectel Object Storage (Russia), coldest tier is cheap,... | fails-egress | Ice () 0.89/GB/mo; Cold 1.26/GB/mo; Standard 2.57/GB/mo. Volume ladder: up to 10 TB 1.35, 10-50 TB 1.31, 50 TB+ lower (per Selectel's own price-change digest) |
| SlideShare | fails-egress | 300 MB max per file (PDF/PPT/DOC), 300 slides for presentations; account-level storage not published. Uploads are currently disabled service-wide |
| Storadera Space Premium | fails-egress | EUR 7.95 per TB per month, granular per-byte, no minimum. 50 GB free for 30 days |
| Storj | fails-egress | No free tier since 2024-03-31. Current public page offers only a 30-day free trial; Standard plan $7/TB storage + $7/TB egress with a $5/month minimum |
| Storj Object Storage, Standard | fails-egress | Per-TB-month, globally distributed; $5 minimum monthly fee |
| Stream Chat (GetStream) free/Maker plan | fails-quota | No free storage allowance stated as a byte figure on the storage page; instead 'Stream applies fair-usage limits to storage, bandwidth, and API calls on every Chat plan' with overage rates once... |
| Supabase | fails-egress | 1 GB file storage, PER ORGANIZATION, not per project; 5 GB egress + 5 GB cached egress per org; 2 free projects per user (across all orgs) |
| Systemfreaks, S3-compatible object storage, 250 GB free... | fails-quota | 250 GB free during beta, 'and bandwidth is free'. Post-beta: $0.0050/GB storage ($5/TB/mo) with 1 TB bandwidth included then $1.00/TB |
| telnyx cloud storage | fails-egress | USD 6.14/TB/month at USD 0.006/GiB with genuinely free egress, which is three times the floor, and the pricing page now reframes the product around 'egress to inference' rather than object storage. The free tier is 10 GB with a KYC step on a public bucket |
| Tencent Cloud COS, new-user free tier | fails-egress | 50 GB STANDARD storage capacity, valid 6 months (180 days), new users only. Some third-party summaries claim enterprise accounts get 1 TB/month for 6 months, not stated on the vendor page read, so... |
| Unity Cloud Content Delivery (CCD) | fails-egress | Conflicting. The live UGS pricing page lists Cloud Content Delivery 'Cloud Storage, Free'. A third-party writeup of the same product reports 5 GB/month included. Unresolved; treat as small until an... |
| Upstash (Redis / Vector / QStash) | fails-quota | Redis Free: 250 MB max data, 10 GB bandwidth/month, 1 database. Vector Free: 1 GB total data, 200M vectors x dims. QStash Free: 1,000 messages/day, 50 GB bandwidth, 1 MB message |
| Upstash Redis | fails-quota | 250 MB max data size on Free; 500K commands per month; 10 GB bandwidth/month |
| UPYUN USS (Storage Service) (`又拍云`) | fails-egress | No standing free tier. Free capacity comes from (a) a 7-day trial with no storage/traffic cap, (b) 61 CNY voucher on real-name signup (1 month), (c) the programme: a one-off 12-month resource grant... |
| UpZur Premium | fails-egress | 'Unlimited upload size, Unlimited storage space, Download volume Unlimited' on Premium. Registered free tier is 1,953 GB |
| VK Cloud Object Storage | fails-egress | no perpetual free volume, pay-as-you-go per GB, per storage class (Hotbox/Icebox/Backup) |
| Xirsys free (Developer plan) | fails-quota | 500 MB monthly TURN bandwidth on the free Developer plan, capped bandwidth, single geographic region after a 30-day all-region trial. STUN unlimited |
| 小飞机网盘 FeijiPan (feijipan.com) | fails-egress | Homepage: '上传下载永不限速，该权益开放给所有用户，无需开通会员即刻享有极速下载'. Baseline free space is small and the 1 TB comes from a developer-signing programme: '签约领1024G'. The resolver project warns of frequent account closures and blocked datacentre IPs, so the read path is what fails |
| Mattermost Team Edition / Entry (self-hosted) | fails-egress | No storage quota at all in self-hosted Mattermost, free or paid. Only the per-file ceiling is configurable: default 100 MB (`MaxFileSize = 104857600` bytes), settable to anything |
| Proxyware earn-app tier as a purchasable egress path... (self-hosted) | fails-egress | these pay the participant; they do not sell to the participant. Honeygain 10 GB = $1 ($0.10/GB); PacketStream $0.10/GB; EarnApp moved to hourly pay on 20 Aug 2025, ceiling $10/IP/month in the US and $5 elsewhere; Pawns.app,... |
| Rocket.Chat self-hosted (Community / Starter) | fails-egress | No storage quota. Per-file ceiling is a single setting: 'Maximum File Upload Size (in bytes)... Use -1 to remove the limit.' |
| Self-hosted Kubo/Rainbow gateway (own VPS) | fails-egress | Storage and egress are whatever the VPS or host allows. No provider quota exists, the cost moves to the host's bandwidth allowance |
| Self-hosted Synapse media repository | fails-egress | Unbounded, `max_upload_size` defaults to 50M and can be set to any value; storage and media retention are entirely operator-controlled |
| Stoat / Revolt, self-hosted instance | fails-egress | No platform cap at all: `body_limit_size` and `[files.limit]` live in Revolt.toml and are set by the instance operator. Storage is whatever disk or MinIO is attached to Autumn |
| Storj storage node operator (supply side) (self-hosted) | fails-quota | paid $1.35/TB/month stored + $1.00/TB egress (cut from $1.50/$2.00 on 1 Sep 2026, an 18% total reduction). Paid in USDC on Ethereum, not STORJ |
| Air Cluster, commercial product that advertises... (self-hosted) | fails-egress | 'Air Cluster allows you to add several accounts from the same server (e.g., three different OneDrive accounts) and combine their capacity into one single cluster.' |

## `trial-only`: a clock, however large (29)

| provider | verdict | why it fails |
|---|---|---|
| ADTAQ Storage VPS, 2 TB, 30 days free (card-gated) | trial-only | 2 TB HDD (SSD-cached), 2 vCPU, 2 GB RAM, 6 TB/month bandwidth on 1 Gbps, $20/month, FREE for the first month. Paid ladder is $10/TB/month with RAID6 + NVMe cache, up to 4 TB at $40 |
| Alibaba Cloud OSS, new-user free trial | trial-only | Current international page: 'Standard LRS resource plan: 500 GB for 1 month' (individual) / '1 TB for 1 month' (enterprise), stacking with a 5 GB/month perpetual allowance to 505 GB (individual) /... |
| AWS Free Tier, S3 (current, post-2025 restructure) | trial-only | No perpetual S3 storage allowance remains in the current published Free Tier. What exists now: up to $200 in credits ($100 at signup + up to $100 for activities), expiring 6 months after account... |
| Azure Container Registry (Basic / free 12-month Standard) | trial-only | Basic SKU includes 10 GiB storage; Standard includes 100 GiB; Premium 500 GiB. Registry storage limit 40 TiB (Basic/Standard) / 100 TiB (Premium). Free grant: '1 Standard tier registry with 100 GB... |
| Bulknews, free Usenet trial (10 GB) | trial-only | Trial: 10 GB, unlimited speed, 30 connections, listed as FREE. Paid blocks start at 20 GB |
| Datum Storage | trial-only | 1 TB free from signup ('Get 1TB Free Cloud Storage From Datum') on an S3-compatible endpoint, which reaches the floor on paper. A signup promotion with no published term and no stated retention, so it is a clock and not a quota |
| DedicatedCore, 6 TB storage VPS, 60 days free (3 slots... | trial-only | 6 TB HDD, 3 vCPU, 4 GB RAM, 10,000 GB bandwidth, dedicated IP, free for 60 days. Only 3 units existed |
| Fil One (formerly Storacha / web3.storage successor) | trial-only | No standing free tier: '1 TB free for 30 days - No credit card required' and '1 TB of storage and 2 TB of egress for 30 days'. After that '$5.99 per TB stored per month' with a 1 TB minimum |
| Freshdesk (helpdesk attachments) | trial-only | Freshworks support states flatly: 'There is no storage limit on the Freshdesk platform. All the data is stored in Cloud.' Per-attachment 20 MB (15 MB on Sprout/trial) |
| Frontproxy (unlimited residential, speed-tiered) | trial-only | $10 for a 3-day 25 Mbps unlimited trial; Pro from $375/day at 400 Mbps unlimited, stated max transfer 4.3 TB/day at sustained full speed, 'effective cost $0.058 per GB'; scales to 2 Gbps |
| Ghost(Pro), 5 MB on free trial/Starter, 100 MB Publisher;... | trial-only | "When uploading media files to Ghost, while there is no limit on the number of files you can upload to your site, there is a file size limit based on your Ghost(Pro) plan. Free trial: 5mb / Starter:... |
| Impossible Cloud | trial-only | No free tier, '5 TB Cloud Storage Free for 30 Days' trial, then 'EUR 7.99 per TB/month' pay-as-you-go. Reserved capacity starts at 25 TB and is partners-only |
| Intercom (article/Messenger attachments) | trial-only | 'The size limit on individual attachments is 100mb for uploads via Messenger and there is currently no limit on the number of attachments that can be uploaded.' No account storage figure published |
| Microsoft Fabric trial capacity / OneLake | trial-only | 1 TB of data in OneLake, free for 60 days |
| pCloud PhotoDay2026 promo, 500 GB free for 3 months | trial-only | 500 GB free for 3 months, no card, via promo code `PhotoDay2026` on a fresh signup. Base free tier is 10 GB |
| PocketHost (PocketBase hosting) | trial-only | 10 GB file storage + 250 MB DB per PocketBase slot, slots are $9.99/mo (or $5/mo annual, or lifetime), with a 7-day trial |
| PulsedMedia Free Seedbox Trial (Helsinki) | trial-only | 50 GiB storage, 250 MB RAM, 200 GiB torrent traffic, 1 Gbps, for 30 days, free. 'Free Seedbox Trial 30 Days, FREE!!!! Free like Free Speech!, 50 GiB Storage' |
| RingCentral Team Messaging (Glip) posts/files | trial-only | No storage quota published; the API reference documents pagination over posts, not a media store with a byte allowance |
| Skool native video hosting | trial-only | 30 GB per uploaded video file, with no documented community-level storage cap. Course/lesson file attachments are separate and much smaller (images 413 above ~10 MB) |
| Snowflake 30-day trial ($400 credits) | trial-only | $400 in free credits on a 30-day trial ('Start your 30-day Snowflake trial today. Get $400 in credits'). No byte quota, storage is billed from the credit balance |
| Snowflake trial account (internal stage) | trial-only | No byte quota, a $400 credit balance and a 30-day clock, whichever ends first. 'The trial continues for 30 days (from the sign-up date) or until you've depleted your free usage balance.' Storage... |
| Storacha (successor to web3.storage) | trial-only | No longer offered, the developer upload and IPFS service was shut down. Was 5 GB free at launch (2025-05); the old web3.storage 1 TB free plan did not survive into Storacha |
| Storj DCS | trial-only | No free tier left. Current page: 'Free trial, $0, Free for 30 days... No credit card required'. The historical 25 GB storage + 25 GB egress free tier was withdrawn; agentdeals records the removal as... |
| Strapi Cloud | trial-only | 50 GB asset storage + 50 GB asset bandwidth on Starter, but Starter is $35/month, NOT free |
| Strato HiDrive, 1 TB for 12 months at EUR 0 (Valentine's... | trial-only | 1 TB, 12 months, EUR 0 (setup EUR 0). Regular price after the free year is EUR 5/month. Captured promo page states verbatim: 'HIDRIVE Basic / 1 TB / 12 Monate / 0 EUR / danach 5 EUR /Mon.' STATUS... |
| Time4VPS Storage VPS | trial-only | 0.25 TB (256 GB) / 0.5 TB / 1 TB / 8 TB. Lithuania, Vilnius. SATA HDD |
| Time4VPS Storage VPS 1 TB (Lithuania, EU) | trial-only | 0.25 / 0.5 / 1 TB |
| VPS Server (vpsserver.com), 30-day trial with 1 TB block... | trial-only | 1 TB of cloud block storage plus one cloud server worth up to $100, 30 days, 20+ locations |
| Zendesk Guide (help center article attachments) | trial-only | 'Each article has no limit on overall storage or total number of attached files.' Per-file 20 MB. But account-level file storage is separately capped at 10 GB base + 2 GB/agent (Team), the... |

## `not-storage`: a category error: compute, a catalogue, a metadata index (27)

| provider | verdict | why it fails |
|---|---|---|
| AUR (Arch User Repository) | fails-quota | Not a storage candidate at all: the AUR enforces a hard maximum blob size of 250 KiB per git object. The git hook rejects the push: 'remote: error: maximum blob size (250.00KiB) exceeded / remote:... |
| AWS Lambda layers (and function deployment packages) | fails-quota | Per-function/per-layer caps only, plus a regional aggregate. Verbatim: 'Deployment package (.zip file archive) size / 50 MB (zipped, when uploaded through the Lambda API or SDKs)... 50 MB (when... |
| data.world | fails-quota | 100 GB total storage on the free Community plan, but with a 3 GB limit per dataset or project, and their own docs are stricter still: 'Dataset ingested to data.world: 1 GB'; 'Size of a file in a... |
| datos.gob.es (Spain) | fails-quota | Not machine-readable from here, CKAN action API returns 403 behind the WAF; the public catalogue is harvested from ministry and regional nodes |
| deCDN | fails-quota | No free capacity. No storage tier at all: 'Not a blockchain or storage network, durability relies on cheap, reliable object storage (S3-class) owned by origin operators.' Target delivery price... |
| Estonia e-Residency | fails-quota | None. The programme issues a digital identity card + DigiDoc software and the right to run an EU company; it confers no storage allocation of any kind |
| FileAxa | fails-quota | Free registered: 488 GB storage, 10,000 Mb (10 GB) per file; free (unregistered) row has no storage pool |
| HAL (Hyper Articles en Ligne, CCSD / CNRS) | fails-quota | 200 MB maximum per file in the deposit UI, plus a 5 GB per-account FTP staging space that is provisional only: 'pour une duree provisoire pouvant aller jusqu'a 31 jours maximum'. No aggregate storage... |
| Hex | fails-quota | Community (free): small compute only, 2 GB / 4 GB / 8 GB RAM profiles at $0/hr. No storage allocation published; there is no user-writable persistent disk, only data connections |
| Jumpshare Basic | fails-quota | Free plan is metered by *upload count*, not bytes: 25 uploads and 60 seconds of recording. No storage figure is published |
| KakaoTalk Channel / AlimTalk (Kakao Business) | fails-quota | No storage quota. Kakao's message API takes an IMAGE URL hosted by the sender; it does not accept a binary upload and store it on the sender's behalf |
| LINE Messaging API, message content endpoint | fails-quota | No storage quota is offered at all. Content is a delivery mechanism, not a store |
| Loom (Atlassian) | fails-quota | Free Starter: up to 25 recordings per person, 5 minutes per video, 50 members. Not a storage quota, a recording-count quota |
| Matrix media repository (matrix.org homeserver) | fails-quota | Free plan: 10 MB maximum per attachment, 100 MB of attachments per 24 hours, up to 500 MB per 28 days. Premium: 100 MB per attachment, 1 GB/24h, 5 GB/28d. Accounts not on any plan get 500 MB/24h up... |
| mcp.gd, MCP-native object storage for agents | fails-quota | Free: 10 GB storage, 10 GB/month traffic, 100 MB web upload. Paid Starter $5/mo: 100 GB storage, 100 GB/mo traffic, 10 GB web upload. Marketing claims 'up to 100GB per file' and 'no storage capacity... |
| Microsoft Teams (free / personal) | fails-quota | 5 GB free per person for files in Teams for personal use; images/videos explicitly do not count and have no storage limit; files land in the 'Microsoft Teams Chat Files' folder in the user's OneDrive |
| Neptune.ai | fails-quota | No storage allowance published, and the pricing page I fetched contained no GB figure at all, the metered dimensions are experiment/run counts and seats. Artifact storage is not offered as a free pool |
| NeuroVault | fails-quota | Signup is plain username, email and password, which is a genuinely open gate, and the service stores statistical brain maps only: one image per map and no arbitrary files. The maintainers have signalled deprecation. The absence of a published cap is silence and not a stated infinity |
| Nostr relays as blob transport (event path, not Blossom) | fails-quota | no storage quota, but a hard per-event size ceiling that is the real limit. Probed NIP-11 limitation.max_message_length: relay.damus.io 1,000,000 bytes; relay.primal.net 1,000,000 bytes; nos.lol... |
| Streamable | fails-quota | 250 MB per file, 10 minutes per video on the free plan. No storage pool, the unit is the individual clip |
| Vercel Blob (Hobby plan) | fails-quota | 1 GB/month of storage, TOTAL per Hobby team, not per project. Pricing table: 'Blob Storage Size / Regional / Usage-based / 1GB/month' for the Hobby Included column, alongside 'Blob Simple Operations... |
| Vercel Deployment Storage / artifact store (Hobby, 30-day... | fails-quota | 10 GB of Deployment Storage per Hobby team, and that pool is what every retained deployment output draws from. This is the clearest example in the whole slot of a 'free tier' that is a build-artifact... |
| Viber Business Messages / REST Bot API | fails-quota | No storage quota, same inversion as Kakao: the caller passes a picture URL, Viber fetches it. Max image 1 MB on iOS, 3 MB on Android, thumbnail 100 KB |
| WhatsApp Cloud API, Media (upload / media_id) | fails-quota | Per-file caps only, no storage quota: documents 100 MB, images 5 MB, video 16 MB, audio 16 MB, stickers 500 KB (as listed on the reference page). Files persist 30 days |
| NYC Mesh (self-hosted) | fails-quota | a network connection plus the ability to host services on it; no storage quota because there is no storage product |
| RIPE Atlas (host a probe or anchor) (self-hosted) | fails-quota | no storage; hosting earns credits spendable on custom measurements |
| Spice.ai Cloud (Community Edition) (self-hosted) | fails-quota | No storage quota published, because the product is not storage. The free Community edition is the self-hosted OSS runtime under Apache 2.0 with community-only support; the hosted Cloud tier is... |

## `paid`: it works, and only at a price above the floor (17)

| provider | verdict | why it fails |
|---|---|---|
| CockroachDB Cloud (Basic tier) | fails-quota | $15/month of free resource consumption per pay-as-you-go org, equivalent to 50 million Request Units AND 10 GiB of storage per month |
| CockroachDB Cloud (Basic) / Continuum | fails-quota | $15/month of free resource consumption per pay-as-you-go org = 50M Request Units + 10 GiB storage/month |
| DigitalOcean Spaces | fails-quota | $5.00/mo base subscription includes 250 GiB across all buckets; +$0.02/GiB beyond |
| GCP research credits programme (Cloud for Higher... | fails-quota | $5,000 one-time for faculty/postdoc; $1,000 per year for PhD students. Credit-denominated, buys GCS at list price (~$20/TB-month Standard) |
| Hetzner Storage Box BX11, 1 TB, EUR 3.20/mo (price floor,... | fails-quota | BX11 = 1 TB at EUR 3.20/month excl. VAT (EUR 0.0051/hr). Ladder: BX21 5 TB EUR 10.90, BX31 10 TB EUR 20.80, BX41 20 TB EUR 40.60. Zero setup fee on every tier. No free tier of any size |
| Hippius Arion (Bittensor subnet on iroh) | fails-quota | Paid storage product (Hippius sells S3-compatible storage, Drive, Hub). No free tier published on the pages opened |
| JFrog Artifactory Cloud, free tier (historically 2 GB) | fails-quota | 2 GB total storage + 10 GB/month data transfer on the legacy 'JFrog Free' cloud subscription. That tier is no longer generally available: JFrog's own blog now carries the banner 'The below post... |
| Load Network, Load S3 (LS3) | fails-quota | No free tier found. $0.003/GB/month (~$3/TB/month) with a permanent-storage alternative at $11.9/GB one-time. S3 1:1 compatible |
| Mail.ru Cloud ( Mail) + Mail Space | fails-quota | 8 GB free per account; 1 TB only as a paid Mail Space plan (1 560 RUB first year, 3 000 RUB/yr after) |
| OVHcloud Managed Private Registry (Harbor) | fails-quota | No free tier, three paid plans: 'S / 200 GiB / $0.027/hour / ~$19.71/month', 'M / 600 GiB / $0.0613/hour / ~$44.749/month', 'L / 5 TiB / $0.291/hour / ~$212.43/month' |
| RADAR (FIZ Karlsruhe) | fails-quota | Paid institutional service, no free self-serve tier. Targeted at institutions and research groups buying a data-publication contract, not at individuals storing bulk data |
| Solana account rent as raw storage | fails-quota | No free tier, storage is a refundable rent-exempt deposit: 10 MiB account costs 53,268,311,040 lamports (~53.27 SOL) to create, reclaimed only on close |
| Stoat (formerly Revolt) + Autumn file service | fails-quota | 20 MB per file, no subscription: 'Custom emojis, a 20MB file upload limit and a server-specific profile picture with no subscription required.' No published total-storage cap and no paid tier that... |
| Synology C2 Object Storage | fails-quota | Product page 404s. The only figure available, a flat USD 7.99/TB with free egress in 1 TB increments, comes from a third-party catalogue and not from a page anybody opened. At that price it loses to Datalix at USD 4.40/TB |
| Walrus | fails-quota | No free tier on the network itself: $0.023/GB/month, billed on *encoded* size, which is 'about 4.5x the original blob plus a fixed 64 MB of per-blob metadata'. Lighthouse resells Walrus with a 100 MB... |
| Wasabi Hot Cloud Storage | fails-quota | USD 7.99/TB/month is four times the floor, and the 'free egress' is a discretionary policy rather than a right: 'If your monthly egress data transfer is greater than your active storage volume, then your storage will be ...'. A 1 TB minimum charge and RCS blocks of 25 TB and up |
| Yandex 'unlimited photo storage' (auto-upload) | fails-quota | unlimited photos/videos, but only with an active paid Yandex 360 plan; free accounts have those files counted against the 5 GB |

## `quota`: the free allowance cannot reach 500 GB per unit (244)

| provider | verdict | why it fails |
|---|---|---|
| / DataDeliver (dd.datadeliver.net) (`データ便`) | fails-quota | Free tier: 5 GB per transfer (registered, free), 2 GB per transfer (Light, no registration). '1' is only on the 330/550-yen business plan. The site's own headline says, the plan table contradicts it.... |
| / moark (formerly Gitee AI), model & dataset hub (`模力方舟`) | fails-quota | Not published. Gitee's help centre documents the AI-model hosting flow (models are stored as LFS files inside a Gitee-style repo and the UI annotates each with its size), and is presented as the... |
| / WoPan (pan.wo.cn, China Unicom) (`联通云盘沃盘`) | fails-quota | 60 GB free, raised from 10 GB by a 2025-09-01->15 promotion that was made permanent (' 10GB 60GB'). Site tagline ''. Non-Unicom numbers can register ('') |
| 4shared | fails-quota | 15 GB free per account |
| 4TU.ResearchData | fails-quota | 5 GB per researcher per year free, then a one-off EUR 4.50/GB (~$4,900/TB). Some sources cite 10 GB for non-4TU institutions |
| Acast, Starter (free) plan | fails-quota | 1 show, 5 episodes on Free, 'unlimited episodes when you make your show available in Acast's advertising marketplace'. So free capacity is 5 episodes unless the show opts into ad monetisation, in which... |
| Aiven free tier (PostgreSQL / MySQL / Valkey / OpenSearch... | fails-quota | 1 GB disk each for PostgreSQL, MySQL and Valkey (Valkey maxmemory = 50% of 1 GB RAM = 512 MB usable); 20 GB storage for OpenSearch; Kafka free tier is throughput-capped at 250 KiB/s. 'Only one... |
| ALCC (ASCR Leadership Computing Challenge) | fails-quota | 10-30% of ALCF/OLCF/NERSC resources each year, with associated project storage (e.g. OLCF 200 TB archive, 50 TB work) |
| Algolia | fails-quota | 50,000 records on the Free/Build plan (100K on the paid Grow tier); 10,000 search requests/month |
| Alibaba Cloud ACR Enterprise Edition / OSS-backed... | fails-quota | Enterprise Edition stores artifacts in the customer's OSS bucket, so 'registry storage' is just OSS storage and is billed as OSS pay-as-you-go. There is no free allowance |
| Amazon CloudFront free tier (as the egress layer for any... | fails-quota | 1 TB/month data transfer out + 10,000,000 HTTP/HTTPS requests + 2,000,000 CloudFront Function invocations, free every month, explicitly 'no longer limited to the first 12 months after signup' |
| Anaconda.org (public conda channels) | fails-quota | 3 GB per free personal account. Anaconda staff on the official forum: 'You'll hit a hard limit at 10 GB with the default storage settings. If you need a large amount of storage (>100GB), you'll need... |
| Arweave via ar.io / Turbo (ario-deploy free tier) | fails-quota | Turbo free tier: 105 KiB per data item, 10 MiB over the lifetime of a wallet AND 10 MiB over the lifetime of an IP range. Larger files are billed |
| Arweave via Turbo / ar.io free tier | fails-quota | Free tier: 105 KiB per data item, and only 10 MiB over the lifetime of a wallet AND 10 MiB over the lifetime of an IP range. Anything larger is billed in Turbo credits |
| AWS Bedrock, custom model import | fails-quota | Hard per-object cap: 'The size of the imported model weights must be less than 100GB for multimodal models and 200GB for text models.' No free storage at all, the source must already live in the caller's own... |
| AWS Cloud Credit for Research | fails-quota | Students capped at $5,000; 'Faculty and Staff awards are not capped'. Credit-denominated against S3 list price |
| ayaya.beauty | fails-quota | no account; 1 GiB per file |
| Azure Artifacts | fails-quota | 2 GiB free per ORGANIZATION (not per project, not per feed), then tiered per-GiB: 2-10 GiB $2/GiB, 10-100 GiB $1/GiB, 100-1,000 GiB $0.50/GiB, 1,000+ GiB $0.25/GiB |
| Azure Blob Storage always-free tier | fails-quota | 5 GB LRS hot block storage, with 20,000 read and 10,000 write operations per month, free for 12 months. Azure Files: 100 GB LRS hot/cool/transaction-optimized, 12 months. Archive Storage: 10 GB LRS,... |
| Azure DevOps Artifacts (Universal Packages) | fails-quota | 2 GiB free storage per organization; Universal Packages up to 4 TiB per file |
| Baidu Qianfan AppBuilder knowledge bases | fails-quota | Advertised as '' (file storage and processing unlimited) on the shared-storage path; documented default is 100 knowledge bases x 800 files each = 80,000 files. PDF up to 500 MB / 3,000 pages per file... |
| beehiiv (free plan), 500 MB per podcast episode,... | fails-quota | Free plan is "Free forever" with unlimited email sends (pricing page). Per-file: "The maximum file size for a single podcast episode upload is 500 MB." File blocks in posts allow attachments; images... |
| BIShare | fails-quota | 100 GB per transfer by link, no account on either side; unlimited size device-to-device on the same LAN (nothing uploaded) |
| Bitbucket Cloud Git LFS | fails-quota | Free (up to 5 users): 1 GB LFS storage. Academic 5 GB, Standard 5 GB, Premium 10 GB. Extra storage sold in 100 GB units at $10/month. Notable counter-property: no per-file cap at all |
| BitChute | fails-quota | No published total cap; free-tier per-file upload limit reported around 2 GB, higher for paid members (membership page advertises 'Higher Upload Limits' without a number) |
| Bluesky / AT Protocol PDS, 5 MiB blob default, GC'd... | unsettled | blobUploadLimit defaults to 5 * 1024 * 1024 = 5 MiB per blob, overridable per-PDS via the BLOB_UPLOAD_LIMIT env var. Per-account: bsky.app's hosted PDS is generous in practice but the protocol layer... |
| BOOTH (pixiv) | fails-quota | 1.2 GB per file (raised from 1 GB on 2026-03-09), 10 GB total per shop; storage add-on CNY 540/month per extra block |
| BorgBase — Medium / Large | fails-quota | 10 GB free forever; Small 250 GB, Medium 1 TB, Large 2 TB, with a flexible quota up to 3x the plan. The free tier is the product and it is 2% of the floor. A Borg or restic repository host, not an object store |
| BowlRoll (bowlroll.net) | fails-quota | Not published on any page reachable without login; the front page now opens with a funding appeal ('BowlRoll') asking users to support it via PixivFANBOX |
| Box (free developer plan) | fails-quota | 10 GB storage, 250 MB file upload limit, 1 file version |
| Box for Nonprofits, donated Starter (10 perpetual... | fails-quota | Box Starter, free for nonprofits via TechSoup validation: 'Secure file collaboration, storage and native e-signatures for up to 10 users / 100 GB of storage / 2 GB file upload'. TechSoup confirms... |
| Bright Data residential network (buy side) | fails-quota | pay-as-you-go $4.00-$8.00/GB depending on tier (141 GB included at $4.00/GB after the RESIGB50 coupon; $3.50, $3.00, $2.50 at higher volumes); free trial on all proxy types |
| Bunkr | fails-quota | No total quota published; 2 GB maximum per file |
| Cachix (Nix binary cache hosting) | fails-quota | 5 GB free for open-source projects: 'Users have a free 5 GB limit for open source projects and 20 Cachix Deploy agents.' Paid tiers start at 50 GiB |
| Calameo | fails-quota | BASIC (free) account: 1 GB storage, 100 MB / 500 pages max per document, unlimited number of publications, 5 private publications |
| calckey.world, Sharkey, 10 GB per user | unsettled | 10240 MB = 10 GiB per user; maxFileSize 250 MiB |
| Chaoxing Cloud (pan-yz.chaoxing.com) + (`超星云盘超星小组盘`) | fails-quota | 100 GB free per account (was 150 GB before a reduction; one vendor page still advertises '150G'). Per-file: 1 GB on web, up to 15 GB via the desktop client ('15G') |
| ChatGPT consumer file storage / Library + Projects | fails-quota | 25 GB shared upload storage per user, 100 GB per organization. 512 MB per file. Project file counts: Free 5, Go/Plus 25, Edu/Pro/Business/Enterprise 40. GPT knowledge: 20 files. 'Users can create an... |
| Chocolatey Community Repository | fails-quota | 200 MB hard per package: 'NOTE: 200MB is the maximum size of a package on the Chocolatey Community Repository. The package must download larger tools from a vendor site or mirror, or if possible,... |
| ClearML (hosted free tier) | fails-quota | Zero free bytes by design. ClearML's free tier is 'Flexible Storage, Store your datasets on any storage service and connect to ClearML - HTTP/S3/GCS/Azure/NAS'. That is bring-your-own-bucket: ClearML... |
| Clojars (repo.clojars.org) | fails-quota | No published byte quota on the site pages read. A 2020-era project commit records an 81 MB uberjar being rejected as 'too large for clojars', and a later commit adds a client-side 'uberjar size... |
| Cloud Firestore | fails-quota | 1 GiB stored data on the free tier; 50,000 document reads/day; 20,000 writes/day; 10 GiB/month outbound |
| Cloud Storage for Firebase (Spark/Blaze) | fails-quota | 5 GB stored free, but only on the Blaze pay-as-you-go plan; Spark project buckets return 402/403 |
| Codeberg (Forgejo) Git LFS | fails-quota | 750 MiB git repository storage + 'Additional 1.5 GiB' for 'LFS, Packages, Releases, Attachments' per user or organization. Non-promoted/personal content is capped at 100 MiB. Enforced since 2025-05-16 |
| Common Crawl (the petabyte corpus, read side only) | fails-quota | Not a hosting service: ~300 billion web pages across ~100+ monthly crawls, multi-petabyte, free to READ and free to re-host yourself. There is NO path to host private data with Common Crawl,... |
| Confluence Cloud Free | fails-quota | 2 GB per site on Free (250 GB Standard, unlimited Premium); 100 MB default per attachment, admin-configurable |
| Contabo Storage VPS 30 | fails-quota | 1 TB SSD (Storage VPS 10/20: 300/400 GB) |
| Contabo Storage VPS, unlimited traffic, 300 GB-1.4 TB | fails-quota | Storage VPS 10: 300 GB SSD (150 GB NVMe option), 2 vCPU / 4 GB RAM, EUR 5.50/mo for the first 24 months. Top tier 1.4 TB SSD at EUR 37/mo. Higher tiers listed as 'More storage available' |
| CPAN / PAUSE (pause.perl.org) | fails-quota | No published byte quota, and the empirical evidence points to a tight request-body limit rather than a documented number: a 2,072,566-byte distribution was rejected with 'Upload failed (request... |
| CRAN (Comprehensive R Archive Network) | fails-quota | Deliberately tiny, by policy. CRAN policy: 'As a general rule, neither data nor documentation should exceed 5MB... Source package tarballs should if possible not exceed 10MB.' Larger tarballs need a... |
| Crust Network DSM | fails-quota | storage orders placed on-chain, each held for six months; the top four nodes submitting proofs share that file's reward |
| CurseForge (Overwolf) author upload API | fails-quota | No published per-file or total quota. Known caps: project media/gallery images limited to 2 MB (author complaint, Apr 2026); mod file upload limit not documented anywhere public, the biggest evidence... |
| DataONE Hosted Repository (TACC / UC Santa Barbara) - the... | fails-quota | 1 TB repository capacity, 'Grow your 1 TB repository capacity based on your storage needs in 1 TB increments', replicated to two geographic regions (California and Tennessee), custom DOI prefix and... |
| Datarade | fails-quota | Zero bytes hosted. Datarade is explicitly a discovery and brokerage layer: it 'doesn't host or deliver data, instead, it focuses on discovery, comparability, and transparency'. Providers list a data... |
| DDownload | fails-quota | Ultimate (paid, EUR 3.33-14.99/mo): 'Unlimited Storage' and 'Unlimited File Size'. Free registered accounts are explicitly limited: 'Free accounts have a limited storage allowance', the number is not... |
| Debian snapshot archive (snapshot.debian.org) | fails-quota | No user quota because there is no user write path - snapshot ingests the Debian archive itself. Scale reference from the site's own news: 'Snapshot is currently holding 172TB of data' (2024-10-08),... |
| Deepnote | fails-quota | Free plan: 3 editors, 5 projects, Basic machine (5 GB RAM, 2 vCPU) unlimited. No free-tier disk figure is published anywhere on the pricing page or docs |
| DeepStorage (deepstorage.dev) | fails-quota | Free 2 TB, and 'Unlimited, while you are in the channel' if the account joins their Telegram, with no per-file size limit either way. The 2 TB is above the floor and the unlimited tier is conditioned on staying in a chat room, which the vendor can revoke |
| Degoo Ultimate 5 TB | fails-quota | Free 20 GB; Pro 500 GB; Ultimate 5 TB. Third-party trackers put Ultimate at $9.99/mo |
| Degoo, 20 GB free + referral ladder | fails-quota | 20 GB free, plus 5 GB referral bonus and 250 MB per referred friend. Paid: 500 GB $2.99/mo, 5000 GB Ultimate |
| Deno Deploy (managed Deno KV) | fails-quota | 1 GiB of KV storage on Free. Pricing page, KV section: 'KV storage: 1 GiB'; 'KV read units/mo (4KiB): 1,000,000'; 'KV write units/mo (1KiB): 500,000'. Pro raises KV to 5 GiB. Deployment assets are... |
| DeviantArt Sta.sh | fails-quota | 2 GB Sta.sh storage free, up to 100 GB with Core |
| DigitalOcean Container Registry (DOCR), Starter | fails-quota | 'Starter is a free offering with a single registry and repository to let you try out DOCR.' Storage 500 MiB: table row 'Storage / 500 MiB / 5 GiB / 100 GiB'. Allowance is prorated by active days: 'If... |
| DocumentCloud (MuckRock) | fails-quota | 500 MB per PDF (25 MB for non-PDF, converted via LibreOffice); no published account storage cap, but uploads require a manually verified account |
| DoodStream | fails-quota | 'Unlimited Storage' (marketing claim on the homepage) |
| Doubao Drive (ByteDance; storage provided by )... | fails-quota | Contractual language is deliberately unquantified: ''. Reported reality: legacy users 100 GB, new users 10 GB, API reports 5 TB but that is decorative, '/facade/get_user_storage5TB100G'. A 2026-06... |
| dpaste.org | fails-quota | approx. 1 MiB per paste (measured: 1,040,000 chars accepted, 1,133,336 chars -> HTTP 413). No account, no quota, no count limit observed |
| DropMeFiles | fails-quota | no account; up to 50 GB per transfer |
| Dryad | fails-quota | Pay-to-publish (Data Publishing Charge). Up to 5 GB = $150; 1 TB = $6,077; 2 TB = $12,162. Not a free tier in any sense |
| EOSC EU Node, 50 GB personal + 500 GB group file storage... | fails-quota | Access-policy table: File Storage (Personal) = 50 GB for Collaborator and Investigator; File Storage (Group) = 500 GB for Investigator only. Investigator also gets 'File Transfer 1TB/month'. Credits:... |
| EuroHPC JU Regular Access (LUMI, Leonardo, MareNostrum 5,... | fails-quota | Node-hours plus an associated storage quota set by the hosting entity (LUMI-O alone defaults to 150 TB per LUMI project). Not a standalone storage call |
| F-Droid (f-droid.org/repo APK archive) | fails-quota | No published total or per-app byte quota. The archive is large and browsable: index-v2.json is 66,480,070 bytes and a single APK (org.fdroid.fdroid) is 12,426,276 bytes. Builds are produced by... |
| Farcaster hubs / Snapchain, storage RENT, actively metered | unsettled | Storage is allocated in integer units per fid and must be BOUGHT from the Storage Registry contract on Optimism (0x00000000fcCe7f938e7aE6D3c335bD6a1a7c593D). Each CRDT specifies messages-per-unit, so... |
| figshare (figshare.com free accounts) | fails-quota | 20 GB storage quota per account. Note: the '5 GB per file' figure is stale; the current limit is 20 GB per individual file. Items 500, files per item 500, collections 100, projects 100 |
| File.io | fails-quota | no account; 4 GB per transfer ('file transfers are limited to a total of 4 GB') |
| file.kiwi Web Folder+ (prepaid Upload-GB) | fails-quota | Prepaid Upload-GB: 50 GB upload $1.20, 100 GB $1.60, 500 GB $3.99, 1000xn GB $6.99xn. 1 Upload-GB = a 1 GB file kept available for 7 days |
| Filecoin Plus / DataCap free storage | fails-quota | was: DataCap granted by allocators, deals free or near-free to the client because SPs got 10x quality-adjusted power |
| Filemail Basic | fails-quota | 5 GB of storage space and 5 GB max per transfer, on a free 1-user account |
| Filen | fails-quota | 10 GB free (10 GiB at signup) |
| Flickr | fails-quota | FREE TIER IS 1,000 ITEMS, NOT 1 TB. The famous 1 TB was killed on 2019-01-08. Free = 1,000 photos/videos total, of which max 50 may be non-public. Pro (paid) = unlimited storage, full-res, no monthly... |
| FOSSVPS / ST-Hosting, free VPS for open-source developers... | fails-quota | Free VPSs on donated hardware; the Frankfurt node is an AMD EPYC 7402P, 128 GiB RAM, 1 TB SSD donated by ST-Hosting for at least two years. Per-VM disk is small (the node is large, the slices are not) |
| Fourthwall | fails-quota | 1 GB per listing (all files counted together) on paid/members-only products; 25 MB total for free digital products. 50 products on Free, 500 on Pro |
| FreeMach, community free VPS (LES/HT/LET members, 3-month... | fails-quota | US1.KVM: 2 vCPU, 3 GB RAM, 120 GB HDD, 1 TB transfer. EU1.KVM: 2 vCPU, 2 GB, 25 GB SSD, 1 TB. Hosts are a VirMach Buffalo E3-1240v3 with 2x1TB HDD and an AlphaVPS Sofia dual-L5630 |
| Game Jolt game builds | fails-quota | 3 GB TOTAL PER GAME, not per file. The 3 GB number is corroborated three ways: the official 9-year-old changelog post ('Max filesize for builds has now been bumped to 3GB instead of 2GB.... |
| Gemini File Search stores (managed RAG) | fails-quota | Free tier 1 GB of store; Tier 1 10 GB; Tier 2 100 GB; Tier 3 1 TB. 100 MB per document |
| ggdriive.com | fails-quota | 20 GB free; 'ILIMITADO PRO' marketed as unlimited (paid) |
| Git-tracked repo files (direct, or via... | fails-quota | 100 MiB hard per file ('GitHub blocks files larger than 100 MiB'); repository size is soft, "We recommend repositories remain small, ideally less than 1 GB, and less than 5 GB is strongly recommended" |
| GitCode (gitcode.com, CSDN), Git/LFS/container quota | fails-quota | No number published. GitCode documents that it meters four resources per user, Git Repository Storage (all branches + all history, excluding LFS), Container Usage (core-hours), Git LFS Storage (all... |
| GitGud (gitgud.io) - GitLab instance | fails-quota | unverified: blocked by challenge. The origin returned HTTP 403 through the fetch proxy (x-web-origin-status: 403) on every attempt, and the reader returned empty content. No instance-configuration... |
| GitHub Actions dependency cache | fails-quota | "the limit is 10 GB per repository" by default (configurable up to 10 TB for user-owned repos, but anything past 10 GB is billed) |
| GitLab Pages (gitlab.io) | fails-quota | 1 GB maximum site size on gitlab.com (tied to the 1 GB max artifact size); 200,000 file entries per site; unlimited projects |
| GitVerse (Sber git hosting: LFS + releases + packages) | fails-quota | 2 GB Git LFS per user AND per org (monthly), 4 GB release assets per user/org, 500 MB packages per user/org |
| Gmail (free @gmail.com), 15 GB shared, and the honest... | fails-quota | 15 GB per Google Account, shared across Gmail, Drive and Photos: "Each Google Account includes up to 15 GB of storage, which is shared across Gmail, Google Drive, and Google Photos." Attachments: 25... |
| GMX (free), 65 GB mailbox, IMAP after opt-in, 135 MiB... | fails-quota | GMX's own storage page: "With GMX, you can store up to 65 GB worth of emails. To put that into perspective, that's around 500,000 emails!" |
| Google Cloud Free Tier, Cloud Storage | fails-quota | 5 GB-months of regional storage per month (us-east1/us-west1/us-central1 only), 5,000 Class A ops, 50,000 Class B ops, 100 GB outbound/month from North America |
| Google Cloud Shell | fails-quota | 'Cloud Shell provisions 5 GB of free persistent disk storage mounted as your $HOME directory... on a per-user basis and is available across projects.' |
| Google Cloud Storage Always Free tier | fails-quota | 5 GB-months of regional storage (US regions only) + 5,000 Class A ops + 50,000 Class B ops per month |
| Google Colab | fails-quota | No persistent disk at all. Notebook files live in Drive; the VM disk is per-session |
| Google Photos Library API (append-only upload) | fails-quota | No quota of its own, but every item uploaded counts against the user's Google Account storage at original quality. 200 MB max per photo, 20 GB max per video |
| Google Play Books (personal upload library) | fails-quota | Up to 1,000 uploaded files per Google account (2 GB max per file per the Partner Center spec; the consumer uploader historically enforced 100 MB). 1,000 x 2 GB 2 TB theoretical per Google account |
| Google Vertex AI Model Garden, custom model import | fails-quota | No hosting quota because there is no hosting: 'You must store your model artifacts in a Cloud Storage bucket, where the bucket's region matches the locational endpoint you're using.' Capacity is the bucket's... |
| Gumlet (free plan) | fails-quota | 60 storage minutes of video, not bytes. No meaningful free image allowance, this is a video-first CDN |
| Heyzine | fails-quota | Free Basic: 5 flipbooks, unlimited pages, 1 GB storage, 1 user, no watermark, API access included |
| hf-mirror.com / hf-mirror.net (Hugging Face mirror,... | fails-quota | None of its own, it is a transparent reverse proxy. Its published conditions say so explicitly: it is a '' (non-profit public AI infra acceleration node) that '... ' (only provides transparent proxying and download... |
| Hi168 (), S3-compatible object storage (`上海海文`) | fails-quota | 500 GB on registration, 1 TB after real-name verification (). Forum dealers advertised it as '1T' in Jan 2026; by 2026-01-19 nodeloc reported '5G', i.e. the grant was already being clawed back |
| Huawei Cloud Space (`华为云空间`) | fails-quota | About 5 GB free; ~CNY 6/month for more. Device-backup oriented |
| Hugging Face Spaces (disk check only) | fails-quota | 50 GB of disk per Space, but per HF's own docs the Space disk is NOT persistent. Persistent storage is the separate Storage Buckets product |
| HydroShare (CUAHSI) | fails-quota | 20 GB automatic on account creation, with an increase process designed to succeed: 'all reasonable requests will be approved subject to system capacity'. 20 GB is 4% of the floor and the increase is a review and not a purchase |
| HyperAI (hyper.ai), free CPU workspace + storage | fails-quota | Free tier storage is 'Free 20 GB + Extra 50 GB, totaling 70 GB', but the 70 GB is explicitly a Pro benefit ('Upgrade to HyperAI Pro, Unlock More Benefits... 3.5x more storage: Free 20 GB + Extra 50... |
| IBM Cloud Container Registry (free plan) | fails-quota | 500 MB storage and 5 GB pull traffic per month: 'Amount of storage for images / 500 MB / Unlimited', 'Pull traffic / 5 GB per month / Unlimited' (Free vs Standard). Free-plan allowance confirmed in... |
| ImageKit (free plan) | fails-quota | 3 GB DAM storage, fixed |
| India DigiLocker | fails-quota | 1 GB per account for citizen-uploaded documents (was 100 MB at launch) |
| infosec.exchange, Mastodon with a 1.35 GiB per-file... | unsettled | Per-account storage is UNLIMITED (stock Mastodon has no per-user media quota at all, media_attachment has only a per-file size validator, no account-level counter). Per FILE: image_size_limit =... |
| Internxt 100 TB lifetime (StackSocial) | fails-quota | StackSocial: 2 TB $129.99 - 5 TB $229.99 - 10 TB $359.99 - 50 TB $699.99 - 100 TB $999.99. Internxt's own site quotes higher (5 TB EUR 585) |
| InterServer Storage Cloud Compute, 1 TB slices at $3/mo,... | fails-quota | 1 TB SATA per slice at $3.00/TB/month, stackable up to multi-TB (32 TB ladder). 2 GB RAM, 1 core, 30 GB SSD boot per slice, 2 TB transfer |
| ioc.exchange, Mastodon, 1.32 GiB video / 80 MB image,... | unsettled | Unlimited per-account; per-file video_size_limit=1419430400 (1.32 GiB), image_size_limit=83886080 (80 MiB) |
| IONOS HiDrive (retail) | fails-quota | 100 GB / 250 GB / 1 TB / 2 TB on the public ladder |
| Issuu | fails-quota | Free Basic plan (since 2025-05-29): 5 published documents max, each capped at 50 MB and 10 pages |
| Item Metadata API (MDAPI) as free key-value/JSON store | fails-quota | No per-item metadata size is published; unlimited items x one JSON doc each, transaction-safe, free |
| Jira Cloud Free | fails-quota | 2 GB storage on Free, 250 GB Standard, unlimited Premium |
| JitPack (jitpack.io) - build-on-demand Maven from git | fails-quota | Bounded by the size of the git repo it builds from, not by a storage quota: a build fails with 'Git error. Max repo size 250MB exceeded'. JitPack builds any public git repo on demand and serves the... |
| Knowledge Network for Biocomplexity (KNB, NCEAS / UC... | fails-quota | 5 GB free per user ('Store up to 5GB of data for free'), with DOIs for permanent publication. Well under the 500 GB bar and with no per-record-unlimited escape hatch published |
| Ko-fi Shop | fails-quota | Free: 25 GB total asset storage, 2 GB per shop item. Standard/Gold: 200 GB total, 5 GB per item |
| KrakenFiles | fails-quota | Marketed as 'unlimit drive'; free registered users get unlimited file count with a 500 MB per-file ceiling for private files. No numeric total quota published |
| LeCloud (lecloud.lenovo.com) (`联想乐云`) | fails-quota | 5 GB base. '5GB71200GB'. Membership adds 20 GB per tier via sign-in activities |
| Lemmy + pict-rs, per-instance image store, no per-user... | unsettled | No per-user quota in Lemmy's own schema, the bound is pict-rs (the separate Rust image server) and the instance's disk. Upload is gated per-instance by the `image_upload` / `image_mode` local-site... |
| Lighthouse (Filecoin/IPFS pinning) | fails-quota | Filecoin plans, Free: 'Total Storage: 5 GB' (IPFS + Filecoin). Walrus plans, Free: 'Total Storage: 100 MB'. Next tier is $12/month for 500 GB |
| Lightning AI (Lightning Studios persistent storage) | fails-quota | No GB figure published. The free tier is framed entirely in GPU hours ('Start on the free tier with 80* free GPU hours'), one Studio free 24/7 with a forced restart every 4 hours, and 'Studios... |
| Mail.ru Cloud | fails-quota | 8 GB free, now a single pool shared between and |
| Mail.ru Cloud / Mail (VK), 1 TB with free public-link... | fails-quota | 1 TB plan. Landing promo (2026-10-15 to 2026-11-19): first year 1,560, from the second year 3,000 (, 1 560, 3 000 ). Free tier 8 GB, 2 GB max file. Paid 1-4 TB |
| mastodonapp.uk / mstdn.social / mastodon.social and the... | unsettled | Per-account UNLIMITED. Per-file: 103809024 bytes = 99 MiB (video), 16 MiB image on almost every stock instance. mastodonapp.uk raises the IMAGE cap to 99 MiB too, which is the unusual bit |
| Matrix.org homeserver (media repository) | fails-quota | Free plan: 10 MB max per attachment, 100 MB per 24 h, capped at 500 MB per 28 days. Premium: 100 MB per attachment, 1 GB/24 h up to 5 GB/28 days. Accounts not yet on a plan get fair-use 500 MB/24 h... |
| Maven Central (Sonatype Central Portal / Central... | fails-quota | No total storage quota, but as of 2026 a *monthly publishing quota per organization* on three metrics, with thresholds set at the ~90th percentile: 1,167 files / 78 MB release size / 7 releases per... |
| Maven Central (Sonatype Central Portal) - post-2026... | fails-quota | Maven Central introduced hard monthly *publishing* limits per organization in 2026. Three independent metrics: file count, release size, release count, evaluated as hard thresholds against the... |
| MediaFire | fails-quota | 10 GB free (Basic, ad-supported); 1 TB paid at $5.83/mo annual |
| MediaFire Pro 1 TB | fails-quota | Pro 1 TB; Ultra 100 GB (tier naming is inverted on the page) |
| MediaTrack (app.mediatrack.cn) (`分秒帧`) | fails-quota | Free personal plan: 10 GB storage, 5 members per project, 1 GB per single file (secondary source says 2 GB free). Paid: 100 GB / 300 GB / 1 TB / 2 TB / 3 TB / 5 TB+. Storage counts '' |
| Medium image hosting | fails-quota | 25 MB per image, images only |
| Mega4up | fails-quota | Free registered: 183 GB storage, 3,000 Mb per file, download volume Unlimited; files deleted 150 days after last download |
| Mendeley Data (Elsevier) | fails-quota | 10 GB per dataset, free, with unlimited datasets per account and the vendor's own suggestion to split work across them: 'you can split your datasets into small sizes'. Institutional Digital Commons Data raises the per-dataset cap to 100 GB. The per-object cap is 2% of the floor per unit |
| Microsoft Azure Free Account, Blob Storage | fails-quota | 5 GB LRS hot block blob with 20,000 read + 10,000 write operations, 'Free for your first 12 months'. Not in the always-free list |
| misskey.art, 5 GiB per user, 250 MiB per object | unsettled | 5120 MB = 5 GiB per user; maxFileSize 250 MiB |
| misskey.flowers, Misskey (hanami fork), 12 GB per user | unsettled | 12288 MB = 12 GiB per user; maxFileSize 250 MiB |
| misskey.gg, Misskey 2026.10, 1 TB drive per user (highest... | unsettled | 1024000 MB = 1 TiB drive capacity PER USER, with maxFileSizeMb = 1024 (1 GiB per single upload). This is the single largest per-user quota located on a live, registration-open fediverse instance |
| misskey.io, 10 GiB drive, 500 MiB per object (largest... | unsettled | 10240 MB = 10 GiB per user; maxFileSize 524288000 bytes = 500 MiB per object |
| misskey.pm, 9.8 GB per user | unsettled | 10024 MB 9.8 GiB per user; maxFileSize 250 MiB |
| mk.absturztau.be, Sharkey, 50 GB drive per user | unsettled | 50000 MB = 50 GB per user drive; maxFileSize 262144000 bytes (250 MiB) per object |
| molab (marimo cloud) | fails-quota | 'Notebooks get a limited amount of persistent storage', size deliberately undisclosed; 'Cached files are subject to limitations on file size and persistence duration, which may change at molab's... |
| MongoDB Atlas (M0 / Free cluster) | fails-quota | A hard 512 MB, not configurable: 'you are over your space quota, using 513 MB of 512 MB'. Three orders of magnitude short, with no path to raise it without moving to a paid tier |
| Moonshot / Kimi API Files | fails-quota | 10 GiB total storage per organization (default); 1,000 files; 100 MB per file |
| MorphoSource | fails-quota | 'MorphoSource is able to subsidize or support free contribution of data for most users with 100GB or less.' 100 GB to 1 TB is case-by-case and may be fully free; above 1 TB is USD 3.47/GB plus USD 30. Capacity here is granted by a subsidy decision and never bought |
| MyAirBridge | fails-quota | 20 GiB per transfer free, no registration required; storage ('save to storage') is a paid-plan feature |
| myQNAPcloud Storage | fails-quota | 16 GB free with any QNAP ID, no trial period, no file-size minimum. Paid starts $0.99/month; 1 TB was $4.99/month during beta |
| NCI Gadi /g/data (Australia), 110+ PB persistent parallel... | fails-quota | Infrastructure is huge, '/g/data4-7 / 110+ PB / Persistent Storage', 'Massdata / 70+ PB', but there is no free self-service quota: bytes come from the merit-based Adapter scheme or a share of a... |
| netcup Storage Space / Local Block Storage | fails-quota | Tariff A 250 GB / B 500 GB / C 1 TB inclusive, expandable per GB |
| Nhost | fails-quota | 1 GB storage + 1 GB database on Starter (free); 1 project |
| Nintendo Switch Online Save Data Cloud | fails-quota | Advertises 'no limit to the amount of storage space' and binds it to 'only one save data file per software title for each Nintendo Account'. The only client is the console, so there is no HTTP API and no programmatic read or write. The practical ceiling is titles owned times per-title save size |
| NIRD Data Lake (Sigma2, Norway), S3 object storage, 10 TB... | fails-quota | No fixed per-project byte number published, quota is set per project by the Resource Allocation Committee (RFK) in TiB on NIRD Data Peak and/or Data Lake separately. What IS fixed and unusually... |
| Nitroflare | fails-quota | Free: 'You can upload up to 10 GB files, for free!'. No free total-storage figure published anywhere on the site |
| NOMAD (NOMAD Central / nomad-lab.eu) | fails-quota | 32 GiB maximum per project, and at most 10 unpublished projects per user. Both are config knobs (process.max_upload_size, services.upload_limit) rather than business limits, and they differ per... |
| Nostr relays + NIP-94/NIP-96 file metadata, index only,... | unsettled | Zero bytes. NIP-94 is a *metadata* event: `url`, `m` (mime), `size`, `dim`, `i` (torrent infohash), `thumb`. The relay stores the JSON pointer, the file lives elsewhere |
| NuGet.org | fails-quota | 250 MB per package, with no documented total-storage quota and no documented cap on package count, and organisations are free. The gallery is designed for libraries and not for blobs: 250 MB per object against a 10 TiB working set is 42,000 packages |
| Observable | fails-quota | Free plan: 'File attachments 1 GB / mo.' |
| OneDrive consumer (Microsoft account) | fails-quota | 5 GB free per Microsoft account; paid tiers 100 GB / 1 TB / 2 TB |
| Open Context (archaeology / cultural heritage data... | fails-quota | No published byte cap, 'Essentially, we provide publication services for the vast bulk of media that typically cannot fit into a conventional book or article publication.' Volume is negotiated with... |
| OpenBayes (openbayes.com), Chinese GPU cloud with... | fails-quota | Free/entry tier attaches 50 GB of workspace storage; the upper tiers attach 200 GB. Additional storage is priced at 0.5 CNY/GB/month, i.e. storage is a metered dimension above the included amount,... |
| opencolorado.org (regional CKAN, US) | fails-quota | Historic operator statement: 100 GB total platform storage, individual uploads up to 50 MB, with the explicit goal of 'supporting data uploads which will make it much simpler for smaller... |
| OpenStreetMap GPS traces (openstreetmap.org/traces) | fails-quota | No published per-user quota and no quota endpoint; storage is GPX-only and appended to the OSM rails DB + a trace store. Effectively unlimited in count, tiny per unit |
| Oracle Cloud Infrastructure Registry (OCIR) | fails-quota | No registry fee at all, and storage is billed at raw Object Storage rates: 'Oracle does not charge separately for the service. Users pay only for the associated storage and network resources that they consume.' The service is free and the capacity is not, so the free Object Storage allowance is the constraint |
| Outlook.com (free), 15 GB mail quota, 150 MiB SMTP SIZE | fails-quota | 15 GB mail storage, explicitly separate from the 5 GB OneDrive allowance: "You get 15 GB of free Outlook.com email storage which is separate from your Microsoft cloud storage. You have 5 GB of free... |
| Oxen.ai (Oxen Hub, dataset versioning for ML) | fails-quota | Explorer (free forever): 50 GB data storage + 50 GB data transfer, unlimited public repos with unlimited collaborators, 5 private repos (max 3 collaborators). Hacker $30/mo: 100 GB storage / 100 GB... |
| Paperspace Gradient (DigitalOcean) | fails-quota | Free tier: '5GB storage', basic instances, free GPU, public projects |
| paste.rs | fails-quota | 393,216 bytes per paste (measured). 373,336 chars -> 201 Created; 426,668 chars -> 206 Partial Content with 393,216 bytes stored |
| pCloud Transfer | fails-quota | 5 GB per transfer, no registration; 200 MB per single file via the web uploader |
| pdfcoffee / dokumen.pub / idoc.pub (unlimited-PDF dump... | fails-quota | "Upload as much as you need! Unlimited volume of uploaded files", no document count or account quota; dokument.pub FAQ caps a single PDF at 200 MB and states "No limitation" on number of... |
| pixelfed.de, Pixelfed, 15 MB per object, unlimited per... | unsettled | Per-account unlimited (Pixelfed has no per-user storage counter). Per-file image_size_limit = video_size_limit = 15360000 bytes (14.6 MiB); 12 attachments per status; image_matrix_limit 2,073,600 px... |
| Pixeltable Cloud | fails-quota | 50 GB Media Store per organization on the free tier, explicitly a HARD limit ('50 GB Media Store per organization (hard limit)'), plus 10 GB database storage per database. Pro raises Media Store to... |
| Playbook, 100 GB free (300-asset cap) | fails-quota | Free: '100GB included' OR 300 total assets, whichever comes first. API 1K calls/month. Paid Pro $10/mo/member = 2 TB + 1 TB per added member up to 10 TB |
| Podbean, Basic Free plan | fails-quota | 5 hours / 500 MB TOTAL, not monthly: 'Total storage: 5 hours (500MB). Note: Storage does not reset monthly.' Help centre adds: 'The total file size should not exceed 500MB' and 'The total length of... |
| Poe bot knowledge bases | fails-quota | 5 GB or 30 million characters per knowledge base, combined across all sources of one bot. One knowledge base per bot |
| PrivateBin public instance network | fails-quota | 10 MB per document by default (sizelimit = 10000000 in upstream conf.sample.php); ~30+ listed public instances, some with file upload enabled. No account, no quota |
| Proton Drive | fails-quota | 5 GB free (starts at 2 GB, +3 GB welcome checklist within 30 days) |
| PulsedMedia Storage Boxes, 4 TB at EUR 8.99/mo + a... | fails-quota | Storage Boxes from 4 TB (EUR 8.99/mo, RAID5) to 32 TB. Separately, a FREE 30-day seedbox: 50 GiB storage, 250 MB RAM, 200 GiB torrent traffic, SSH + SFTP + Docker rootless |
| Pumble (free plan) | fails-quota | 10 GB of file storage for the whole workspace on Free |
| Puter (puter.com / Puter.js), user-pays cloud storage | fails-quota | Free tier shown on puter.com as '25 MB Storage' (the 100 GB / 500 GB / 2 TB figures on that page are the paid tiers, verified by reading the raw HTML, not the rendered summary). Developer-side cost... |
| Radicle Garden (hosted seed) + permissionless public seeds | fails-quota | 5 GB of storage to start with on a Garden subscription ('talk to us if you need more'); public permissionless seed nodes self-configure their own limit, e.g. 10 GB observed on a community node |
| Redis Cloud (free tier) | fails-quota | 30 MB single database, free forever |
| Rentry.co | fails-quota | 200,000 characters per entry (hard, enforced at API), unlimited entries, no account required. Entries kept 'forever' unless they break rules |
| Scramble Cloud Premium 6 TB lifetime (StackSocial) | fails-quota | 2 TB EUR 129.95 once - 6 TB EUR 279.95 once (official site). StackSocial carries 2/6/12/20 TB SKUs at $59.95 / $139.95 /, / $349.95 |
| Seedr, free tier | fails-quota | Free tier exists but is deliberately unspecified: 'You can try Seedr for free, with a low storage limit.' Paid tiers start at Basic $7.95/mo for 50 GB. No free GB figure is published anywhere on the... |
| Send Anywhere | fails-quota | Free: 1:1 real-time transfer up to 50 GB; LINK creation capped at 10 GB. Lite $5.99/mo raises download data to 200 GB |
| ServaRica, 'Unlimited Expanding Storage' (500 GB + 1... | fails-quota | Shrimp 1: 500 GB base + 1 GB/day automatic growth, $5/mo, i.e. it crosses 1 TB at ~day 500 and 1.87 TB at 4 years, on a fixed price. Shrimp 2: 500 GB + 2 GB/day, $7/mo. Lobster: 2 TB + 3 GB/day,... |
| Shade | fails-quota | 20 GB free account (stated in rclone's own backend docs) |
| Sia Storage (hosted indexer, sia.storage) | fails-quota | 50 GB free, 'The free plan includes 50 GB of storage, up to 3 connected apps, and transfer speeds up to 524 Mbps, with no Siacoin to buy and no server to run.' |
| Sirv (free plan) | fails-quota | 0.5 GB storage |
| Sketchfab (3D model hosting, Epic Games) | fails-quota | Free 'basic' plan is 10 uploads/month with a per-model cap that the two official pages disagree on: /features says 50 MB for Free / 200 MB Pro / 500 MB Premium, while the /plans comparison table... |
| Slack (free plan) | fails-quota | 5 GB per free workspace (hard cap), 1 GB max per file, plus a 90-day visibility window and permanent deletion of anything over one year old |
| Socrata / Tyler Data & Insights, 'Community Content' on... | fails-quota | No file storage at all. Community Users may create filtered views and visualisations of EXISTING public datasets; there is no upload of new bytes |
| SpaceByte Cloud (India), INR 150/TB/mo claimed, the... | fails-quota | Starter 50 GB INR 20/mo; Freelancer 100 GB INR 35/mo; 500 GB INR 100/mo; Studio Pro 1 TB INR 150/mo (or INR 1,650/yr); 25 GB free forever. Enterprise pooled storage on request |
| Stack Exchange image host (i.sstatic.net,... | fails-quota | 2 MiB per image, no per-account total; unlimited images per post |
| Streamlit Community Cloud | fails-quota | 'Storage: No minimum, 50GB maximum' per app, but the filesystem is the build container, not durable storage |
| Sync.com | fails-quota | 5 GB free, permanent; referral top-ups |
| Tableland | fails-quota | 500,000 rows and 24 columns per table. That is the entire quota, it is a SQL-over-SQLite network, not an object store. Byte capacity is implied by row content and is not published as a number, but... |
| TACC Corral (US), 5 TB free per PI, $60/TB/year beyond | fails-quota | 'The first 5TB of storage for each PI, on one project, is available to researchers at all UT System institutions at no cost. For storage needs larger than 5TB, and for multiple project allocations,... |
| Tencent Weiyun (`腾讯微云`) | fails-quota | About 10 GB free; paid ~CNY 10/month. Massively downgraded from the 10 TB free era |
| termbin.com | fails-quota | approx. 1 MB per paste, no account, no count limit. Measured: 1,000,000 bytes stored and retrievable; 2,400,000 bytes -> connection reset |
| thirdweb Storage | fails-quota | 1 GB included free; 1 GB-1 TB at $0.05/GB/month; 1-10 TB at $0.04; 10 TB+ at $0.03 |
| tmpfiles.org | fails-quota | no account; 100 MB per file |
| transfer.archivete.am | fails-quota | no account; no published per-file cap (transfer.sh successor, same DutchCoders codebase) |
| Transfer.zip | fails-quota | Quick Transfers are free and have NO file-size limit, but they are ephemeral P2P: 'deleted automatically when either party closes the transfer window'. Persistent storage starts at Starter $6/mo (200... |
| TransferXL | fails-quota | Free with account: 5 GB max transfer size, 10 GB daily / 300 GB monthly transfer allowance. Paid plans reach 100-200 GB per transfer |
| Tresorit Basic | fails-quota | 3 GB free, permanent (not a trial), zero-knowledge encrypted |
| Turso | fails-quota | 5 GB total storage, 100 databases on Free |
| Twist (Doist) Free plan | fails-quota | 5 GB of file storage per team on Free; unlimited on Twist Unlimited. 100 MB per attachment |
| Twist (free plan) | fails-quota | 5 GB storage on Free (unlimited on Twist Unlimited); 100 MB per attachment |
| Uguu | fails-quota | no account; 128 MiB max upload |
| uldl.sh | fails-quota | 250 MB free storage per name, 4.5 MB max per file, unlimited uploads/day. No account needed, the 'username' in the URL is claimed on first POST |
| Ultralytics HUB / Ultralytics Platform | fails-quota | Free: 100 GB storage, 10 GB per dataset upload, unlimited number of datasets and models. Pro ($29/seat/mo): 500 GB storage, 20 GB per upload. Enterprise: unlimited storage, 50 GB per upload |
| Uploadcare (free plan) | fails-quota | 1 GB storage, 1,000 operations/month, 5 GB/month traffic. Their pricing page lists operations and file-size caps rather than a storage number; 1 GB is the documented free storage allowance |
| uploader.jp / getuploader.com () (`アップローダーレンタル`) | fails-quota | 10 GB total per account: 100 MB per file, 1,000 MB per uploader, 10 uploaders per account = 10 GB. Free, and the terms state '' |
| Upstash Vector | fails-quota | 1 GB total data+metadata on Free; 10K daily queries; 200M vectors x dimensions |
| Uschovna (uschovna.cz) | fails-quota | Anonymous transfer: 30 GB per shipment, free, 14 days, 30 downloads per recipient. Paid (40 CZK): 50 GB, 90 days, unlimited downloads. Registered 'uschovna+' adds 50 GB of permanent storage on top of... |
| Val Town | fails-quota | Free plan blob storage: '10mb on the free plan and 1gb on pro'. Pro is the ceiling, so there is no free path to bulk |
| Vidyard (Free) | fails-quota | Free: 5 recorded videos per month, 25 videos in the library at once, 30 minutes max length. AI video generation capped separately |
| VikingFile | fails-quota | Tagline: 'Share large files anonymously. Unlimited storage. No mail required. No speed limit. No size limit.' No numeric quota page found |
| Walrus Console (Walrus Foundation, Oct 2026 launch) | fails-quota | 5 GB free. Launched 2026-10-07 with 'Get started today with 5GB free'. No larger free tier is published |
| Wellcome Trust - storage as a claimable grant cost | fails-quota | No byte quota - 'large-scale data storage' is an allowable service charge, plus a 'Data management and sharing plan costs' line |
| WenShuShu (wenshushu.cn) (`文叔叔`) | fails-quota | 40 GB free drive space. Own site: ' 40GB'. Per-file: 5 GB ('5GB'). No login needed to send; login needed to keep |
| WeTransfer | fails-quota | Free: 3 GB per transfer AND 10 transfers per rolling 30-day window (a pool, not per-send). Links live up to 3 days. Starter 10 transfers/300 GB. Ultimate unlimited transfers up to 1 TB/transfer |
| Wormhole | fails-quota | Up to 10 GB per send. Only the first 5 GB is actually stored server-side; anything above 5 GB is PEER-TO-PEER and requires the sender's tab to stay open |
| XBOX services Title Storage | fails-quota | Trusted Platform: 256 MB per player (Managed Partners) / 64 MB per player (Creators Program). Universal Platform: 64 MB per player. Global: 256 MB. No total-title byte cap published |
| Yahoo Mail (free), 20 GB, down from 1 TB | fails-quota | Yahoo's own help, read live: "Yahoo Mail incluye actualmente 20 GB de almacenamiento gratuito con cada cuenta" = 20 GB free per account. Plans: 100 GB, 1 TB; Mail Plus is 200 GB. The old 1 TB free... |
| Yandex Disk (+ Yandex 360) | fails-quota | 5 GB free per account (shared with Yandex Mail attachments); paid 200 GB-2 TB from 319-699 RUB/mo |
| Yandex Disk free tier (post-2026-06 change) | fails-quota | 5 GB by default for users without a plan: ' 5 '. Photo/video 'unlimited' auto-upload is a plan feature only, without a Yandex 360 plan, mobile uploads count against the 5 GB |
| Yandex Mail, 5 GB pooled with Disk, 1 GB attachment | fails-quota | Yandex's own docs: "By default, users without a plan get 5 GB of storage space." Mail and Disk now share one pool: "Emails and attachments in Yandex Mail now share storage with files on Yandex Disk."... |
| ZeroTier free (Personal) | fails-quota | 10 devices, 1 network, non-commercial use. Vendor table effective 20 Oct 2026: 'Personal / Free / 10 / Not available' |
| Zhihu image hosting | fails-quota | no vendor page found; user reports cluster at 2-10 MB per image |
| Zoho Mail Free, 5 GB/user, up to 25 users via referral,... | fails-quota | Zoho's own help: "Each user is allocated 5 GB of storage under the free plan." Headcount: free plan is 5 users in select regions, expandable, press release "increasing the number of mailboxes offered... |
| Zoho WorkDrive | fails-quota | 5 GB free forever on the Individual plan |
| Zooniverse (Panoptes) | fails-quota | Stores contributor *classifications*, not contributor *uploads*, and the upload side is capped at 10,000 subjects per user. Zooniverse Help, Lab Policies, verbatim: 'there is a limit of 10,000... |
| Zulip Cloud Free | fails-quota | 5 GB total file storage per organization on Cloud Free, not per user. Standard/Plus are 5 GB/25 GB per user |
| GoAnywhere MFT / GoDrive (self-hosted) | fails-quota | GoDrive EFSS is 'completely free' but only as a component of on-premises GoAnywhere MFT. Capacity is the server's disk; there is no hosted free storage |
| M-Lab (host a measurement site) (self-hosted) | fails-quota | contribute servers, not consume storage; host-managed deployment onboarding is 'almost entirely automated' for 'any reasonably modern, high-performance, and well-connected physical or virtual server' |
| Sia host (hostd) - supply side / the arbitrage test (self-hosted) | fails-quota | the host sets its own price; network median is $1.17/TB/month storage and $2.25/TB download (siascan), $1.30 KS/TB/month |

## Rejected in the dead-end list only, with no provider-table row

The 898 records below never held a row in the provider table, so no ledger row assigns them to a class document. They are grouped here by the same rule and named in full, because a graveyard that keeps only the half somebody indexed is a graveyard that loses 898 providers.

### `dead-service` (79)

| provider | why it fails |
|---|---|
| (almondcloud) (`杏仁云盘`) | 150 GB free with WebDAV was recommended in 2025 (''). Domain is dead: drive.almondcloud.cn returns NXDOMAIN as of 2026-10 |
| / (7so.top) (`七嗖云盘长青云盘`) | Marketed as 1 TB free with WebDAV; its own Cloudreve site config now returns title '-1119' (shutting down Nov 19) and registerEnabled=false. Dead mid-flight. The sibling (cloud.7 |
| / and the family (1 tb free, webdav) (`长青云盘七嗖云盘银杏云盘`) | The canonical '1 TB free WebDAV' post that every Chinese list still cites is a redirect to a shutdown notice. pan.7so.top now serves only ' 2025322 '; the migration tar |
| / quwenjian.com (claimed +1 gb/day forever, webdav)... | Origin no longer resolves. The 'unlimited growth of 1 GB/day' claim is attractive because it would clear 500 GB in 500 days from a single email account, so it is worth recording as a *catego |
| 0x0.st | Uploads are DISABLED, not merely broken. POST returns HTTP 503 with body 'uploads disabled because it's been almost nothing but AI botnet spam for the past few months. will be back with a fe |
| 0x0.st (the null pointer) | Uploads are globally disabled right now, not merely rate limited. POST returns HTTP 503 with the body 'uploads disabled because it's been almost nothing but AI botnet spam for the past few m |
| alist.xiaoya.pro, (xiaoya) public instance, the most... | DEAD. The canonical xiaoya host returns HTTP 302 from nginx and then a Cloudflare 504 on every path, including /api/public/settings. Xiaoya is the single largest AList deployment in China (m |
| archive.org classic web uploader (browser drag-and-drop) | Fails the programmatic-access filter on its own; also the weakest path (Resume-button retries, 503-slowdown-spam, ASCII-only filenames). Only the IAS3 API or ia CLI are viable at 20TB |
| baidu cloud ccr personal edition | Dead since 2024-04-25: personal-edition instances no longer accept new namespaces or repositories at all, and no external image migration is allowed. Only pre-existing images keep working |
| baidu pan /, anonymous read (`百度网盘`) | The guest path gets further than expected and then stops dead. An iPhone UA opens the share page, /share/verify returns errno 0 with a randsk cookie, and the page then renders window.yunData |
| bashupload.com | Domain no longer resolves to an origin, DNS returns only an SOA in the Authority section (NXDOMAIN-equivalent, registrar-servers.com), and the proxy returns HTTP 530. The dataset still list |
| bayfiles / anonfiles | Both gone, and they are not the same story. AnonFiles shut down August 2023 citing excess-usage volume; BayFiles' 2023-era successor domain no longer resolves. Neither has a free successor operatin |
| clouddrive2.chenkui.cn, the 'hosted clouddrive2 demo'... | Dead. No hosted demo of CloudDrive2 exists: the domain fails to connect entirely (curl exit with http_code 000). CloudDrive2 is a closed-source paid product distributed as a Docker image (cl |
| codehive (codehive.sr.ht) / sourcehut generally | codehive.sr.ht does not resolve (NXDOMAIN) - there is no such host. sourcehut itself is paid-for-project-hosting ('All users who host projects on SourceHut are expected to pay according to t |
| cowtransfer (`奶牛快传`) | Shut down 2026-01-10 and wiped server data. Was the canonical 'free 40 GB, never throttled' transfer host; now simply gone. Do not let an old blog post resurrect it |
| cran (r) | Policy explicitly caps and actively polices size: 'neither data nor documentation should exceed 5MB... authors will be asked to trim their documentation to a maximum of 5MB' and 'Source pac |
| cyberdrop (cyberdrop.me) | The.me domain is dead, Cloudflare 1016, origin hostname does not resolve. The service lives on at cyberdrop.cr; the.me records are a trap for anyone copying old links |
| dans easy (legacy) | Retired. 'As of 2 December 2024, EASY will no longer be accessible', datasets migrated to the domain-specific DANS Data Stations. Any EASY quota figure found in third-party guides is dead |
| datachain / datachain studio (iterative) | Already recorded dead and checked here: it is a Python data-context layer over S3/GCS/Azure, a catalogue and lineage tool. It provides zero bytes and requires a bucket supplied by the caller |
| dataverse's own installations json... | DNS dead. Cloudflare error 1016, origin hostname does not resolve. The working substitute is the GitHub data file that powers the same map |
| disposable-mail providers as storage (mail.tm, guerrilla... | All probed and all dead at the API layer, `api.mail.tm/domains` -> **502**, `POST api.mail.tm/accounts` -> **502 0 bytes**, `api.guerrillamail.com/ajax.php?f=get_email_address` |
| edgio / limelight networks | Chapter 11 in September 2024, CDN went dark 15 Jan 2025. Akamai acquired the assets and select contracts. Any cached pricing for Edgio is fiction |
| envs.sh | Domain is PARKED and for sale, 'This domain may be for sale' via abovedomains.com for-sale parking script. Serves HTTP 200 with a sale page, so it looks alive to a status-code check but is |
| envs.sh and null.slipfox.xyz (0x0 instances) | Both listed in the 0x0 instance directory as live alternatives. Both domains are now parked/for-sale pages served by abovedomains.com, not file hosts |
| euserv backuphd 1t se2021 / se2019 / wme2018, the '1 tb... | The most-cited 'free 1 TB' in this niche is a discontinued annual promo, not a standing offer. The pages are still live and still say 'free period of this offer is 1 year' + 'Offer is valid |
| feimaipan (feimaipan.com) | Origin hostname no longer resolves (Cloudflare 1016), so the site is gone rather than blocked |
| file.io (documented api path) | The REST flow printed in its own /about page no longer works: POST to both file.io and www.file.io returns 405 MethodNotAllowed from an S3-style object store. Listed as a dead end for the do |
| filestream.me | Domain no longer resolves. Probe: Could not resolve host: filestream.me. The 'seedbox + HTTP streaming' product is dead |
| gakunin rdm (nii, japan) | 100 GB per user with a 5 GB per-file cap on NII Storage, misses a 500 GB floor by 5x and the per-file cap is worse. Checked in Japanese and the numbers ar |
| gamesparks | Retired. AWS states 'Amazon GameSparks (Preview) is no longer accepting new customers'; the AWS SDK has removed the service entirely. Nothing to sign up for |
| ganso | Shut down entirely, cited alongside ThunderDrive as a completed instance of the 'cheap lifetime terabytes then vanish' script |
| github releases as buzzheavier's actual upstream (the... | Works as an architecture, dead as a specific artifact: `GrandpaNutz/fafda` 404s, the user account 404s, and buzzheavier's own post predicted it ('I don't trust GitHub. They can nuke my accou |
| gitpod (now ona) | gitpod.io no longer resolves to a pricing page, it redirects to ona.com, which routes /pricing to a sales contact form. There is no self-serve free tier to evaluate; the product pivoted to |
| guilded (roblox) | Actually dead. Roblox announced shutdown and Guilded went dark on 19 December 2025. Its old 500 MB per-file free limit was the most generous of any chat platform and is now irrelevant, do n |
| helm personal cloud server | Company shut down 30 Dec 2022 and purged all encrypted backups; the hardware is now Armbian-convertible e-waste. Relevant only as a warning about the appliance category |
| hetzner object storage (as the kms alternative to storage... | Not a dead end, only dominated: EUR 6.49/TB with only 1 TB traffic included, vs EUR 3.20/TB unlimited on the Storage Box. The guide that surfaced it states the comparison directly |
| hidrive (strato) | free 5 GB tier was discontinued, the free plan ended 2020-04-30; current entry plan is 500 GB at 6 EUR/month. WebDAV endpoint still live (PROPFIND -> 405 unauthenticated) and rclone has a T |
| idoud (idoud.cc) | mydearniko/idoud markets 'absolutely free, unlimited cloud storage' with a Go CLI and a curl-pipe installer, but both the site and the install host are down (530/502 in two separate probes) |
| infura ipfs | Discontinued. New uploads and pinning stopped 2026-08-03; the IPFS API and dedicated gateway ended 2026-08-15, after which unmigrated content is no longer available. Infura's own docs URL no |
| ipfs / arweave / filecoin pinning as the hidden upstream | No evidence at any of the seven, and round 1 already settled free pinning as <=6 GB or dead. pixeldrain's one decentralised dependency is Sia, not IPFS, and it is a cost-control measure with |
| ix.io | Root returns 404 and POST returns 404, the classic ix.io pastebin endpoint is dead |
| line keep | Service terminated 2024-08-28; stored data is not viewable or retrievable afterwards. Nothing to research |
| mapilio | The API host is down: api.mapilio.com returns HTTP 502 Bad Gateway (a Heroku-style error page). It is named in OSM community threads as a KartaView/Mapillary alternative, but nothing is prob |
| mega pro i/ii/iii as a per-tb play | Not a dead end as a product, but it LOSES to MEGA's own S4 line and to Jottacloud on this metric. Pro III is 16 TB for EUR 29.99/mo, and MEGA's own comparison strip advertises 'MEGA 1.25* pe |
| mexashare | Every provider in the read walk failed with dial-failed / 502; origin unreachable. Cannot verify limits |
| miraheze | Quota was the best in the niche, FAQ (archived 2026-06-04) says 'There are no hard limits except "be reasonable"' on wiki storage, but the entire farm is OFFLINE today. meta.miraheze.org |
| nft.storage | Already known to the swarm: the Classic free upload service was decommissioned 2024-06-30. The surviving site sells 'a small one-time fee' per NFT collection with an onchain endowment, no b |
| nft.storage classic (free ipfs pinning) | Free upload/pinning decommissioned 30 June 2024. Page still advertises 'up to 31GiB per individual upload' but signup is closed and existing data is only 'preserved' with degrading latency |
| ninefile (ninefile.com) | Was advertising '100 GB free' in search snippets, but the site now says 'NineFile is being rebuilt. The service is offline while we start it over from scratch.' Zero capacity today |
| ogramcloud (ogramcloud.com) | The repo Sanix-Darker/ogramcloud-cli-client (16 stars) still advertises 'free UNLIMITED STORAGE', but the host is gone: probe returned a pkgforge 522 with a Cloudflare 'Connection timed out' |
| opfs / browserfs / browser-based file systems | Offline-only by construction. The origin private file system is subject to browser storage quota and eviction, is invisible to the user's filesystem, and is deleted when site data is cleared |
| osdn (osdn.net / osdn.jp) | CONFIRMED DEAD, as round 2 suspected. `osdn.net` no longer resolves (DNS NXDOMAIN from two separate attempts); `osdn.jp` resolves but is now a Japanese consumer-affiliate content farm (' |
| p / (white-label 1-2 tb webdav pans) (`盘公云`) | These are the purest form of the pattern (email not even validated, 'x@x.com'), 1 TB free with WebDAV + offline download, but the poster's own thread title is the epitaph: ' |
| paste.ee | Offline for a migration with no ETA: 'Paste.ee is offline while we migrate... There is no estimated time for the site to return.' Reads still work, writes do not |
| pillowcase.su | Domain parked and for sale; the service is gone. Any list still naming it is stale |
| polarbackup | DEAD as a lifetime product, and the clearest proof of the revocation pattern. Sold 'permanent lifetime' 5 TB for a one-time fee, then terminated those subscriptions. UK company 12274576 stil |
| polarbackup lifetime (5 tb) | CONFIRMED DEAD, worse than dead. In 2024 PolarBackup permanently closed every lifetime account and deleted the data: 'those who did not seize the opportunity to upgrade their accounts have |
| prism drive | DEAD. Marketing site still answers 200 and still advertises 2 TB $49 / 5 TB $69 / 10 TB $89 lifetime, but the actual application is gone: https://app.prismdrive.com/ returns HTTP 500, web.pr |
| quqi cloud / (`曲奇云盘`) | Marketing claims 2TB free but the site returned 522 and every read provider timed out; the archived replay also failed. Cannot verify any number for a provider I could not open, treat as un |
| radicle garden subscription | 5 GB and it is a paid subscription, not a free tier; beyond that is 'talk to us'. Logged here as a dead end for capacity while the free permissionless-seed path is recorded above as a separa |
| roar (roar.eprints.org) | Cloudflare 522/403 on the raw endpoints. rawlist.txt (the one machine-readable dump) times out at 22 s; /view/software/dspace.html returns a 7 KB Cloudflare error page. Only recoverable via |
| rsync.net as the 20 tb solution | Not a dead end technically (unmetered egress, best tooling) but priced 4-9x above the floor: 20 TB at $15/TB = $300/mo vs EUR 40.60 for Hetzner BX41. Only worth it for the 500 GB free... |
| sagemaker studio lab | Dead in 2026: closed to new signups. AWS docs state 'no longer open to new customers' and point at SageMaker Studio instead. The 15 GB persistent free disk still exists for legacy accounts b |
| scaleway c14 cold storage (classic vault api) | Discontinued. The c14-cli repo carries an explicit warning and points users to the new S3-compatible Glacier class, which is already covered above as fails-egress |
| scloud (kr, claimed 500 tb free) | The 500 TB claim circulating in Korean blog roundups is dead: the live site advertises 'Free Storage (1GB)' in its own nav and page title. The 500 TB figure was blog-reported in 2024/25 and |
| sia / skynet | Skynet Labs shut down its websites and services in 2023 and Filebase ran a migration for Skynet customers; siasky.net free portal storage is gone. Sia itself survives as a protocol where a renter |
| skynet / siastream | Skynet is gone as a free product; Sia's current offering is the 50 GB hosted Sia Storage account recorded above. The Skynet guides that still rank describe a discontinued portal model |
| stackpath cdn | Company is gone. CDN shut 22 Nov 2023; the company ceased operations and liquidated in mid-2024; Akamai bought ~100 enterprise contracts. Their own product page is now titled 'Product Retire |
| starchive lifetime (1 tb) | DEAD. The $96.99 1 TB lifetime SKU was a limited promotional run sold through StackSocial/MacTrast/Cult of Mac in 2021. Starchive's own FAQ now says: 'This was a limited-time promotional off |
| storage boy (storageboy.com /.net /.jp) and... | STORAGE BOY is advertised in a live Japanese aggregator as '' with 1 GB per file and 7-day retention, but the domain no longer resolves on any TLD, NXDOMAIN on.com,.net and.jp |
| terabox anonymous share api (shorturlinfo) | The pre-Baidu-shutdown mechanism of hitting /api/shorturlinfo with app_id=250528 is dead: it now demands a verify_v2 device token, and with a warmed cookie jar it degrades to errno 2. Anonymous |
| tmpfiles.org via normal dns | Not dead, but effectively unreachable on this machine: DNS answers 0.0.0.0 /:: (sinkholed), so every plain curl fails with 'Could not resolve host'. Worked around with --resolve to the Clou |
| transfer.sh (the original) | Domain resolves but the origin does not serve::443 on 144.76.136.153 (via --resolve) fails to connect after 21 s, and fetch.web.pkgforge.dev returns 522. The brand is dead; only community m |
| university / alumni cloud accounts (google, microsoft 365) | CONFIRMED DEAD as a capacity source. The 2023-2024 Google Workspace for Education storage cap (pooled 100 TB per tenant, then often 5-20 GB per user) plus Microsoft's alumni-licence withdraw |
| upstash kafka | Discontinued. Deprecated 2024-09-11, shut down 2025-03-11. Do not plan around it; Upstash now points users at Workflow/QStash instead |
| uptobox | Seized and still dead. The domain answers with a Cloudflare 522 and a French/English maintenance banner ('Nous realisons une maintenance et nous revenons tres vite'), which reads like a live |
| uptobox as a precedent (or as a live host) | Dead and instructive, not usable. Seized 19 Sept 2023 across Scaleway, OpCore and OVH; owner Genius Servers Tech FZE (Dubai) fought it, lost in Aug 2024 on a time-bar rather than the me |
| vimeo weekly-quota premise (500 mb/week) | Dead premise worth correcting: the widely-repeated '500 MB/week free' figure describes the pre-June-2024 Free plan and legacy paid Plus/Pro weekly quotas. Current Free is unlimited public st |
| xserver vps storage expansion | The 200 GB storage add-on was discontinued for all new signups on 2025-02-03; the maximum disk on any current plan is 2,400 GB and only on 4 GB+ plans. Not purchasable for a new customer and |

### `read-gated` (16)

| provider | why it fails |
|---|---|
| 115 share download without login | Metadata is free, bytes are not, and no parameter variation moves it: the web endpoint returns 990001, the app endpoint 99, both meaning 'log in again'. proapi and webapi agree, so there is |
| artstation | Image posts cap at 10,000x10,000 px and the platform re-encodes for the portfolio viewer; free accounts have no meaningful byte quota but no original-byte delivery either. The Pro/Studio ups |
| bilibili as a byte store | 8 GB sounds good but every upload is transcoded and content-reviewed; playback is signed m3u8. Cannot return the uploaded bytes |
| bunny stream | Paid per GB stored and per GB delivered. Transcoding and player are free, storage is 'From $0.01/GB' and traffic is billed on top, this is exactly the per-GB metered model this topic rejects |
| buzzsprout, free plan | 2 hours of upload per month AND episodes are deleted from the feed after 90 days (with a further 90-day 'safety net' before permanent removal). It is a demo tier, not storage. Also re-encode |
| claude files api as an archive | 1 TB/org quota is real and per-file 500 MB is real, but uploaded files are explicitly non-downloadable, write-only. 100 workspaces x 1 TB would be 100 TB of nominal space and zero bytes ret |
| flathub as bulk storage | Human-reviewed flatpak app submissions; content-addressed/deduplicated OSTree means distinct bytes are not additive; registry.flathub.org does not resolve publicly |
| garmin connect | An upload path exists but is capped at 25 MB per activity file (.fit/.gpx/.tcx) and the service parses them into activities - the bytes are not stored as an object. Unusable as a blob store |
| google photos | 15 GB shared across the whole Google account (Gmail/Drive/Photos). Original quality counts against it, and 'Storage saver' re-encodes and resizes anything over 16 MP. Content deleted after 2 |
| gumlet | Free plan is 60 storage minutes of video (not GB) with 100 GB bandwidth/month, a transcode-and-deliver product, not storage; API access starts on the $6/mo Creator tier |
| linux.do and nodeseek as deal feeds | BOTH ARE WRITE/READ-GATED FOR THIS PURPOSE. linux.do returns a Cloudflare challenge to direct search.json, and behind it demands login for search (firecrawl resolved it to /login; individual |
| nekojarashi (nekojarashi.com) | No longer a consumer storage product at all. The site is now a B2B video-transcoding company (product page: 'High Performance Cloud Transcoder'; latest news item is 2019-08-30 about Setaria |
| quora | no attachment/file hosting at all, images are re-encoded into answers, the published conditions grant Quora a sublicensable redistribution licence, and there is no public API for media |
| replicate files as storage | 100 MiB per file, and prediction inputs/outputs are auto-deleted after one hour on the API path. The files API objects are described by the SDK as write-only inputs |
| transloadit | Free 'Community' is 5 GB of processing per month, 0.5 GB per file, watermarked output images and trimmed A/V, it is a transcoding pipeline with a hard stop at 5 GB, not a store |
| tumblr | photo posts only, re-encoded and resized; help centre has moved to a new knowledge-base structure and none of the image pages state a byte limit. Legacy API is unmaintained |

### `write-gated` (29)

| provider | why it fails |
|---|---|
| ads (archaeology data service) | Deposit is curated and costed per project via the 'Ingest' system; a registered account is required 'so that the ADS can manage your data deposits' and the depositor receives 'costing information', i |
| anonymous telegram file links for arbitrary documents | The t.me/s preview path carries photos and videos only. Probed seven public channels for tgme_widget_message_document: zero hits, zero.pdf links. There is no anonymous HTTP URL for a zip/pa |
| ardc nectar research cloud (australia) as free object... | Every researcher gets a 'project trial with 4 VCPUs allocated for six months', but object storage is not part of the trial, it is an RC-NAS allocation item reviewed by the Nectar Allocation |
| azure open datasets (as a hosting programme) | No intake at all. It is a curated catalogue of Microsoft/partner data surfaced through Azure ML; there is no application, no quota and no route to place a 20 TB data set there |
| cdnjs / cdnjs.cloudflare.com as a personal store | Not open-write: packages are added by maintainer PR against the cdnjs/cdnjs repo, i.e. write-gated by review. Its free mirror hop.js is useful (see candidate 1) but the underlying store is n |
| chocolatey community repository (community.chocolatey.org) | 150 MB max per package, moderation on every push, and active rate-limiting at ~100 installs/hour average with manual IP blocks that 'will not automatically expire'. Not a storage target |
| codeberg (as a storage host) | Explicitly capacity-managed for F/LOSS code: request approval above 750 MiB Git storage and 1.5 GiB of packages/LFS/attachments, 100 MB private storage without a request. Not a bulk target a |
| cran | 10 MB soft cap on source tarballs, 5 MB for data; policy explicitly rejects using packages to distribute bulk content. Human review |
| ctan | Web-form upload with manual editorial review; no API, no programmatic path regardless of size |
| degoo 10 tb lifetime (stacksocial) | Listing is still up but the vendor's reliability record disqualifies it: users report account deactivation and data loss including on the old lifetime plan. Cloudwards' 2026 review says stay |
| deic interactive hpc / ucloud (denmark) | Storage is a Weka filesystem product granted through a reviewed 'grant application' scored by an internal committee per provider, requested in GB with no published default. It is POSIX-on-Ku |
| disroot | free Nextcloud (so WebDAV works out of the box) but only 2 GB; extra space is granted by an application form, not by scaling accounts, and the instance is donation-funded and rate-conscious |
| filebin.net | Hard 6-day automatic deletion of every bin, and bins require approval before downloads are allowed. No persistence path at any price |
| filerule 2 tb lifetime (stacksocial) | Unvetted white-label, listed at $69 for 2 TB ($34.50/TB one-time). No independent reviews, no API, no rclone backend, no WebDAV. Included here only to document that StackSocial's storage cat |
| fosshub | NO LONGER HOSTS FILES AT ALL. The FAQ (updated 2026-09-24) is explicit: 'Application download links open the publisher's official service. Some publishers use GitHub or SourceForge... FossHu |
| free music archive / ccmixter | Both are curated libraries, not storage: FMA's upload path is gated behind a Tribe of Noise artist account and a curation/approval step, and /upload returns 404 on both sites (FMA has no sel |
| galaxy zoo / foldit / seti@home | Pure volunteer-compute. Galaxy Zoo runs inside Zooniverse (so the same 10,000-subject / review gate applies) and Foldit distributes protein-puzzle clients; neither exposes any user-addressab |
| google cloud public datasets (as an intake) | No application process exists. Google hosts only its own and partner datasets (Sentinel-2, Landsat, ARCO-ERA5, NEXRAD), and the only stated route for anyone else is an email address: 'If you |
| hex.pm (elixir/erlang) | 8 MB compressed / 64 MB uncompressed for packages and docs combined. Also requires a curated package name and does review. Far too small to shard meaningfully |
| lemmy.world / lemmy.ml / sh.itjust.works / feddit.org as... | The big Lemmy instances either require an application to register (lemmy.world: registration_mode='RequireApplication') or do not publish an upload size in the API at all, because the limit |
| lfs.gg | Markets 'Unlimited Git LFS bandwidth for GitHub, GitLab, and Bitbucket' but is paid per 100 GB/month with only the first 10 GB free, and is 'currently invite-only'. Not free storage at scale |
| library of congress 'by the people' (crowd.loc.gov) | Transcription and review only. Volunteers create and review transcriptions of LOC-held pages; no file is accepted and nothing is stored on the volunteer's behalf. Explicitly not a deposit pr |
| model zoo (modelzoo.co) | A curated index, not a host: every entry is an outbound link to the original author's repo or site. No upload, no storage, no quota |
| nvidia ngc catalog | Curated by NVIDIA, not user-writable: containers, models and Helm charts published by NVIDIA and partners. api.ngc.nvidia.com is an authenticated pull path (404/401 unauthenticated), and the |
| researchgate full-text upload | no published per-file or per-account quota; uploads are gated to works the depositor is an author of, and the help centre article for max file size 404s. Reviewer removed the only machine-readable pa |
| singapore nscc (aspire 2a / apollo) | Applications must be verified by the host institution's research office before prioritisation. Project storage is a quota inside an approved project, not a grant an individual can hold |
| surf spider / data archive as a free self-service tier | Tape archive access is requested through SURF's servicedesk and is institution- and application-gated (the free route is the NWO Small Compute application, which caps at 300 TB tape but requ |
| wikidot | Free account is 5 sites x 300 MB = 1.5 GB total, 25 MB per file. The 'unlimited' Community Site tier exists but is application-gated ('most popular, high-quality, community-driven projects |
| spareband / busyproxy / meowbyte / earnbear (2026... (self-hosted) | All four are pre-launch or invite-only supply-side apps: Spareband is waitlist-only with payouts explicitly not open yet; BusyProxy requires phone verification and pays $0.20-0.30/GB; MeowBy |

### `retention` (69)

| provider | why it fails |
|---|---|
| amazon sqs | 1M requests/month free and 1 MiB max message sound workable, but max retention is 14 days (default 4). It is a buffer, not storage, anything written is gone in two weeks. Free-tier request |
| arize ax / phoenix cloud free tier | AX Free is 25k spans/month with 1 GB ingestion and 7-15 day retention; Pro is 10 GB/30 days. Spans are telemetry, not objects, and there is no bulk-blob path |
| astraweb | No free trial on the live site any more, the homepage goes straight to $15/month, 5,500 days retention, 50 connections. The 'free trial' I searched for does not exist |
| azure for students | $100 credit valid 12 months plus free monthly service amounts - a credit, not storage. Expires to pay-go |
| azure for students ($100 credit) | '$100 credit to use on Azure services within 12 months', renewable annually 'as long as you're a student'. $100 is a few TB-months at best; the 12-month balance expiry is the binding limit |
| azure pipelines build artifacts (as a free archive) | Retention is configurable and a run can be marked 'retained indefinitely', but the backing storage is the Azure DevOps organization's storage, and the org's free artifacts allowance is 2 GiB |
| binder (mybinder.org) | Explicitly no persistence of any kind, and egress is throttled to ~1 mbit per session to stop it being used as a DDoS vector. Sessions die after 10 min idle / 6 h max, 1-2 GB RAM. A pure dea |
| blossom.band / nostr.build blossom (free tier) | Free uploads are 20 MiB per file with no retention guarantee ('A hard cap of 100 MiB per upload (20 MiB for free uploads)'), and the BUD-06 pre-flight is actively refused to non-browser clie |
| buildkite artifacts | Metered both ways: storage billed per GB-month and transfer billed per GB beyond plan inclusion, and retention maxes at 7/30/90 days depending on plan. Full custom retention is an Enterprise |
| canfar / opencadc vospace (canada) | Storage is per-deployment and per-project and the docs explicitly defer the number: 'The exact mounts, quotas, and retention policy belong to the deployment and your project' and 'ask suppor |
| clicknupload / filespace / dosya.co / hostize /... | All live, all far under the floor. Clicknupload: unlimited-for-active-files but 2 GB guest / 3 GB registered per file, inactive purged in 7-30 days. FileSpace: FAQ renders as the upload form |
| cloudflare queues | Tempting because per-queue backlog is 25 GB, but on Workers Free message retention is 'non-configurable at 24 hours', everything written is deleted within a day. Charged at 1 operation per |
| confluent cloud (kafka) | $400 in credit, but it expires after 60 days and is denominated in dollars rather than bytes. Not a free tier; a trial. Note also that Kafka is append-only with retention, even unlimited by |
| contabo storage vps line (all tiers) | Checked and rejected on price, not availability: $13.44/TB at the 1 TB tier versus EUR 2.03/TB at Hetzner BX41. The 'Unlimited Traffic*' asterisk is a discretionary-throttle clause, not a... |
| controlc.com | 100 KB per text paste, guest pastes expire in 48 hours max, and even media uploads cap at 500 MB/day guest / 2 GB/day member with 50 MB per image. Expiry and per-file cap both fatal |
| cults3d | 1 GB per upload, plus a daily upload-count limit to throttle mass AI uploads |
| databricks free edition (default storage as an archive) | Free Edition is perpetual in the sense that it does not expire, and hitting quota does not delete data ('your data and settings will not be deleted'). But it is serverless-only with per-acco |
| discord as a durable cdn origin | Signed attachment URLs expire in exactly 24 hours (measured ex-is = 86400) and unsigned fetches 404. A URL cannot be stored in a catalog and reused; every read needs an authenticated message |
| euserv backuphd 1t (se2021 / se2019 / wme2018) | The 1000 GB free-year offers are expired: the page itself says 'Offer is valid until 31.12.2021', one contract per customer, auto-renews at paid rates. The only current free product is 'Back |
| fal.ai | Same shape as Replicate and worse-documented for storage: the platform is per-second GPU billing for model APIs and Serverless deploys, with a 'fal CDN' for request media that is a retention |
| file.io (now limewire) | file.io redirects into LimeWire. Free plan is 40 GB storage with a 4 GB upload cap and files expire after 3 days; 20 downloads per file per day. Retention makes it unusable as storage, and t |
| filemail 'store files forever' | The only genuine forever-retention product in this niche, but it is Business/Enterprise only and consumes paid account storage. Not reachable from the free tier |
| fileport | 5 GB per upload, 50 GB/month on a free account, 7-day expiry for free uploads |
| filetransfer.io | 4 GB free, no registration, short retention. Below the floor by two orders of magnitude |
| gemini file search stores as bulk storage | Free tier is 1 GB of store, and store size runs ~3x input size, so real input capacity is ~333 MB. Only embeddings persist; raw files are deleted after 48h |
| gemini files api (ai studio) as an archive | 48-hour retention, clamped server-side, plus 'you can't download user-uploaded files'. 20 GB/project is moot |
| gitea cloud | Commercial managed Gitea. 30-day free trial only, storage is a paid add-on pack, and the 'unlimited network traffic' feature is unlimited-bandwidth-at-throttled-speed rather than free egress |
| github actions artifacts as an archive | 500 MB on Free, 90-day retention, token required for download. It is a build handoff medium, not storage |
| github student developer pack, storage angle | The Pack's 2026 partner list has no meaningful bulk-storage grant. What it offers is Microsoft Azure $100 credit (a trial that expires, 5-20 GB practical), 1 TB OneDrive via a Microsoft 365 |
| gofile.my (the 'free unlimited storage' lookalike) | Markets 'Free unlimited storage with no file size restrictions', but its TLS certificate expired 2026-09-30 and its upload API host does not answer, and it is a different operator from gofi |
| gog galaxy cloud saves | Hard 200 MB per game, and GOG actively purges the oldest files once a game exceeds it, capacity shrinks over time rather than growing. No public write API |
| hastebin.com (toptal) | API now requires a GitHub-issued access token, one token per user, 100 req/min, and content expires in 30 days even when authenticated (7 days otherwise). No anonymous writes |
| homebrew taps | A tap is just a GitHub git repo of formulae; storage is GitHub's (2 GB push / repo recommended limits), and bottles live in GHCR or on the project's own host. Nothing Homebrew-specific adds |
| ibm cloud object storage lite plan as a storage tier | The Lite plan is always-free and never expires, but the published storage allowance belongs to the Standard plan Free Tier (5 GB for 12 months). No Lite storage quota was published on any IB |
| inbox.eu free | Messaging docs say 20 GB ("Mailbox size... is the same - 20Gb") but the pricing page's 100 GB is the 30-day Business *trial* with a 3-emails-per-day send throttle, classic trial-vs-free co |
| jottacloud | 5 GB free; the genuinely interesting 'Unlimited' plan is NOK 129/mo and throttles upload after 5 TB. Not free |
| jottacloud free | 5 GB free. The interesting product is 'Unlimited' at NOK 129/mo, which throttles upload after 5 TB, and it is paid |
| justbeamit | Not storage of any kind, pure P2P with a 10-minute link. 'JustBeamIt does not upload any data until the recipient starts the transfer' and the link 'will expire after 10 minutes' |
| langsmith datasets/traces as storage | Free Developer plan is 5,000 base traces/month with 14-day base-trace retention, 1 seat, 1 workspace. Storage is billed as traces, not bytes, and the retention window is shorter than any arc |
| line messaging api content | Auto-deleted after an undisclosed period, no listing endpoint, token-only access. Cannot be addressed as storage even short-term |
| litterbox (catbox temporary) | Explicitly temporary, expiry is chosen at upload (1h/12h/1d/3d/7d max). Not storage by construction; only useful as an ephemeral hand-off |
| microsoft fabric trial / onelake | 1 TB but 60 days only; after expiry non-Power BI items go inactive and content is retained just 7 days. Great API surface (DFS + Blob), wrong duration for a 20 TB archive |
| ncar glade (campaign / work / scratch) | Work is 2 TB per user and Scratch is 30 TB but PURGED at 180 days; Campaign Storage is the only large tier and it is allocation-request-gated for university projects. The 30 TB scratch is th |
| oversubscription as a stable strategy (sell 10 tb,... | It exists but it is not the lever people think, because the hosts already limit the thing that would break it. gofile caps free accounts at 10,000 contents and 10 days' inactivity rather tha |
| pixeldrain (as a transport-tier finding) | Checked because rclone has a native `pixeldrain` backend and the free tier says storage 'No limit'. But free egress is 6 GB/day *per IP*, files expire 60 days after last download, hotlink |
| playstation app captures library | PS5 auto-upload goes to a private per-account library in the PS App with no public URL, no documented quota, no documented retention, and no API at all. Web-only, login-walled, unverified ev |
| powder (platform for open wireless data-driven... | A city-scale wireless/5G testbed (shuttles, indoor over-the-air lab, ORAN stack). The resource is radios and mobility, not disk; there is no multi-TB storage allocation and the experiments a |
| pulsedmedia free seedbox (50 gib / 30 days) | 50 GiB and terminates at day 30; all slots taken ('Available: 0'). The provider itself calls it 'a blatant marketing gimmick'. Fails the quota floor by 10x and the retention test outright |
| read the docs community | Free for public OSS docs, but no published output-size quota; build limits are 30 min / 7 GB RAM and builds are per-version with default-version-only retention. Cannot verify a storage figur |
| replicate (model hosting) | Output files are ephemeral by design: 'output files are automatically deleted after an hour' for API-created predictions, and replicate.delivery URLs 'expire after one hour'. Custom models a |
| roblox open cloud assets api | 20 MB per asset, and the asset types that matter are throttled monthly: audio 10 total uploads/month without ID verification (100 with), video 20/day. Asset delivery requires auth, anonymou |
| sendbird free plan 'unlimited message storage' | Unlimited is a rate allowance; retention is 6 months and the same pricing page says so twice. Extended retention is the paid upsell |
| sendgb 'unlimited transfers' | Real (no monthly transfer cap) but useless here: 5 GB per transfer, 90 day retention, and the provider explicitly has no API. Highest transfer-count ratio, lowest utility |
| slickdeals as a discovery channel | It only re-lists StackSocial and pCloud first-party promos, it adds no provider the StackSocial search did not already surface, and its useful hits are expired (the pCloud 10 TB thread is m |
| soundcloud, basic (free) plan | Only 2 hours of total upload time (not per month, lifetime), which at 128 kbit/s is ~110 MB of audio for the entire account. 4 GB per file and 24 h per track look generous but the 2-hour... |
| swisstransfer 30-day option | The 30-day selection is not a 30-day retention. Files are deleted at 15 days unless the sender clicks an extension email on day 12, and the offer closes 3 days later. 'Once expired, a link c |
| telegram cloud bot api alone (api.telegram.org) | Hard 20 MB download ceiling via getFile and 50 MB multipart upload. getFile links also expire: 'It is guaranteed that the link will be valid for at least 1 hour.' Unusable as a storage API w |
| temp.sh / uguu.se / litterbox / tmpfiles.org (transfer.sh... | All are short-TTL transfer services, not storage: temp.sh 4 GB but 3-day expiry; uguu.se 128 MiB and 3 hours; Litterbox 1 GB but 1 hour-3 days; tmpfiles.org 100 MB and 60 min-48 h. transfer |
| transfer.it (mega) as a paid capacity route | Transfer.it has no paid tier of its own, it is a sharing front end that requires MEGA storage: 'You can only share files that you have uploaded to MEGA.' Its expiry selector offers up to 1 |
| transferit-py's 10-year expiry | The library advertises MAX_EXPIRY_SECONDS = 10 years and will happily send e=315360000, but the bt7 server clamps to 90 days. Verified across five requested expiries. Do not trust client-sid |
| usenet / nntp free providers | No free binary provider with usable retention exists. The only genuinely free, posting-allowed server found (Eternal September) is text-only, explicitly 'no binaries', with 130-day retention |
| vercel hobby (static deployments) | 100 MB max static upload per deployment on Hobby, and since Apr 29 2026 Hobby deployment retention is capped at 30 days ('Deployments outside your retention window will be automatically remo |
| volcengine ark files api (doubao) | Server-side clamped retention: minimum 1 day, maximum 30 days, default 7 days. 512 MB per file on managed storage. Cannot hold anything |
| wenshushu () (`文叔叔`) | Free space is 40 GB, explicitly: ' 40GB'. Well under the 500 GB floor. Its 'never throttled' promise is real but irrelevant at this quota |
| xbox network captures | Policy since 2023-10-01 deletes captures stored on the Xbox network after 90 days. Explicitly a TTL cache, not storage; the intended destination is a personal OneDrive |
| xserver drive (xserver.ne.jp), the one japanese... | 2 GB free with a 100 MB per-file cap, verified by a Japanese developer who actually ran rclone against it. It is technically excellent (WebDAV works on the free plan, fast SSD, no inactivity |
| zoom team chat files | unverified, docs unreadable; download_token scoping and plan-dependent retention make anonymous serving implausible. Left recorded so nobody re-runs the same failed fetches |
| veilid for bulk data (self-hosted) | No congestion control and no relay throttling implemented; relay bandwidth management is an open to-do. Mobile-first design assumes 'limited storage and bandwidth' at every node |
| zus / blimp (0chain) (self-hosted) | The free-ish path requires contributing hardware, 'Launch a node... as little as 4 vCPU and a single 100 GB attached disk', so it is rent-seeking capacity, not a free tier, and it in |

### `egress` (51)

| provider | why it fails |
|---|---|
| ardrive / turbo (arweave free tier) | Free upload allowance is 105 KiB per file, 10 MiB lifetime per wallet AND 10 MiB lifetime per IP range, the IP-range meter makes it un-multipliable, six orders of magnitude below the bar |
| aruba cloud object storage / infomaniak object storage... | Both product URLs 404 through the read broker; Infomaniak's real numbers sit on a Public Cloud price page (EUR 0.01/GB = EUR 10/TB, egress free only to 10 TB/month per organisation, metered |
| azure blob storage 'always free' 5 gb | 5 GB per subscription with card verification, and the grant is labelled 12 months on the free-services page. Egress is metered at $0.087/GB after the first 100 GB/month, which alone kills th |
| bunny.net as a *free* egress source | Free transit applies only from Bunny Storage *into* Bunny CDN. There is no free public egress: end-user delivery is $0.01/GB EU/NA and $0.03/GB Asia, with a $1/month minimum, so Bunny is the |
| bytescale | No free tier at all any more, cheapest plan is $7/mo Basic with 10 GB storage and 10 GB download bandwidth; over-quota returns HTTP 400 |
| cachix | 5 GB free for open source. Cloudflare egress is genuinely unlimited, but 5 GB is the cap |
| cloudinary | Free plan is 25 credits/month where 1 credit = 1 GB storage OR 1 GB CDN bandwidth OR 1,000 transformations, i.e. 25 GB total across storage+delivery combined, and max raw file size is 10 MB |
| contentful (free / starter space) | Files are capped at 50 MB each and asset bandwidth at 50 GB/month with NO overage purchasable on Free; only 1 Starter space, 100k API calls/month. Storage size itself is not published as a G |
| deluxhost storage-4 (EUR 6.99 / 3 tb) | EUR 2.33/TB headline looks competitive but the offer table lists no traffic allowance at all for the STORAGE line (the '20G'/'30G' column is NVMe, not bandwidth), the plans are flagged... |
| e2e networks object storage (in) | INR 2.5/GB/mo = $26.46/TB plus INR 3/GB egress = $31.77/TB of egress. Billed on PEAK monthly usage, so deleting early in the month does not help. Both dimensions are far above the floor,... |
| evolution host | Checked as named. No storage product line at all, the entire catalogue is NVMe VPS from 20 GB to 160 GB with generous transfer (10-80 TB). High bandwidth, no disk. Exactly inverted from wha |
| fil one / storacha s3 tier | Marketed as cheap S3 ($5.99/TB/month, $0 egress) but the free component is a 30-day 1 TB trial, not a free tier. Below the archive requirement and time-boxed |
| filestack | Free plan is 1 GB bandwidth, 1 GB storage, 500 uploads, 1,000 transformations, pure demo tier |
| folderfort 2 tb lifetime (stacksocial $109.97) | Listing 404s. FolderFort has moved to a 'Folder Fort 2.0' subscription model with bandwidth allowances (10 GB/month on free), the lifetime SKU is gone and the new model fails the egress fil |
| gitbook (free site plan) | Free plan exists but publishes zero storage, bandwidth or file-size figures, it is positioned as a docs editor, not a host. No quota to verify means no basis to qualify it; hosting terms ar |
| github lfs as bulk storage | 10 GiB storage and 10 GiB/month egress on Free, three orders of magnitude short of an archive of 20 TiB, and egress is metered rather than unmetered |
| github pages as bulk storage | 1 GB published site and one user/org site per account; 100 GB/month soft bandwidth. Deduplicating into accounts gives ~hundreds of accounts per TB, not viable at 10 TiB |
| google cloud source repositories | 50 GB/month storage and 50 GB/month egress on the free tier, but the product is end-of-sale and being replaced by Secure Source Manager. Also a git-only interface, poor fit for 10 TiB of ra |
| gozunga | 100 GB/month free S3-compatible, then $0.025/GB and $0.005/GB egress. Misses both a 500 GB floor and the free-egress test; also below a 500 GB unit |
| greenhost | VPS-shaped: EUR 6.95 for 2 vCPU/4 GB/40 GB disk/10 TB traffic. The 10 TB traffic allowance is generous but 40 GB of disk makes it irrelevant as storage |
| imagekit | Free plan: 3 GB DAM storage (fixed limit) and 20 GB bandwidth/month; 225 GB storage costs $89/mo |
| iroh n0 public relays | Free tier is 'rate-limited traffic' with 'No uptime guarantees' and the exact limits are deliberately unpublished ('The exact rate limits aren't published today, as they get tuned as needed' |
| iwinv (kr) object storage and sata block | Priced per GB and it is expensive: 20/GB/mo = $15.09/TB for object, 39,000/TB = $29.42/TB for SATA block. On top of that, egress is separately metered on a declining scale (60/GB for the |
| jianguoyun / nutstore | The 'Space depends on the uploaded data' line looks like unlimited, but the free plan caps throughput at 1 GB upload / 3 GB download per month. That is a bandwidth wall, not a storage wall |
| magalu cloud object storage (brazil) | R$0.10/GiB/mo storage is a fair $20.39/TB/mo, but egress is R$0.10/GiB, a 1:1 storage-to-egress ratio, the worst structure possible for a serving workload, and it applies to any transfer p |
| metered open relay at the advertised 20 gb | The 20 GB/month figure on the Open Relay landing page is stale; the billing page sells a 500 MB/month free tier shared ingress+egress. 40x overstatement on the vendor's own site |
| neocities as the archive tier | 1 GB per site and 200 GB/month bandwidth per site means 20 TiB would need 20,480 sites and would still be bandwidth-starved; Free also restricts uploadable file types ('No File Upload Type R |
| ovhcloud object storage | No free storage tier at all; S3-compatible and 'no hidden fees for ingress/egress or API calls', but stored GB are billed from the first one. Only a $200 new-customer trial credit |
| ovhcloud object storage (standard / cold archive) | Free egress and free API calls is genuinely attractive, and OVH is not on the excluded-provider list, but the arithmetic loses. Standard One Zone is ~$0.0081/GiB/mo = ~$8.30/TB/mo, i.e. Wasabi pricing |
| photon (realtime / pun / fusion / chat) | No storage product at all. The free tier is 100 CCU for Fusion/Quantum and traffic allowances measured in GB of message relay; there is no bucket, file API or persistence surface to write by |
| pixeldrain pro / prepaid | Prepaid storage is genuinely EUR 4/TB/mo but egress is metered at EUR 1/TB with NO free download allowance on the filesystem, 'Downloads from the filesystem are charged at EUR 1 / TB for... |
| podomatic | 500 MB total storage and 15 GB/month bandwidth on the free Basic plan, smaller than Podbean and with no unlimited-drafts mechanism. 'Unlimited Storage and Bandwidth' is the $49.99/mo Broadcaste |
| pulsedmedia, 'eternal vainamoinen' EUR 1.99 storage tiers | The headline EUR 0.83-1.00/TB prices carry egress quotas an order of magnitude below storage: 'Storage 2TB R5 1G' is EUR 1.99/mo for 2 TB with 268 GB/month traffic; 'Storage 4TB R5 10G' EUR... |
| qiniu cloud kodo () (`七牛云对象存储`) | Structurally identical trap to Tencent and marginally cheaper on storage. Standard CNY 0.115/GB/mo ($17.60/TB/mo), archive CNY 0.031, deep archive CNY 0.012, but egress CNY 0.26/GB =... |
| qiniu kodo free quota | 10 GB/month standard storage + 10 GB/month CDN origin traffic + 1M GETs. Two orders of magnitude under the 500 GB floor and China-only CDN egress |
| quotaless (quotaless.cloud) | Genuinely unlimited storage with rclone/S3/WebDAV and unmetered bandwidth, but it is EUR 60/month recurring plus a one-time EUR 20/10TB fee. It is the *correct architecture* and the wrong p |
| scaleway perpetual 75 gb free object storage | Removed December 2023; only the 75 GB/month free egress survived. The replacement is a one-shot 750 GB / 90-day trial. A free-for-dev PR was merged removing Scaleway for exactly this reason |
| selectel promotional egress-waiver tariff | Recorded separately because it is a genuine but badly-shaped deal and the page has since 404'd. The promo (live to 2025-08-31, captured 2025-06-15) waives egress and all API requests for a y |
| sftp to go | 7-day free trial only; the free plan is a trial, and storage/bandwidth are priced per month |
| stack exchange as bulk storage | 2 MiB cap plus no API upload path plus per-site posting rate limits; the permanence is excellent but the throughput is a human-editor workflow |
| storacha / fil one | 1 TB free but for 30 days only, with 2 TB of egress in the trial: '1 TB free for 30 days - No credit card required... The 30-day trial includes 2 TB of egress.' After that it is $5.99/TB/mo |
| storj dcs standard | $7/TB storage AND $7/TB egress, the egress term alone ($7,168/TB-equivalent pattern) makes it the exact '$2 store with $10 egress' pathology inverted. $5/mo minimum. The egress was already |
| storj object storage (paid) | Egress is priced identically to storage, so it is strictly worse than Wasabi for this workload: $7/TB stored + $7/TB out. Serving 500 GB to 1 TiB each day (15-30 TB/mo) adds $105-210/mo on top of th |
| storx | Every route lands on a sign-in wall; the only quotable copy is 'S3-Compatible Offsite Backup Storage, No Egress Fees'. No free allowance was visible after two attempts, so nothing is claime |
| tebi.io | Was the best free S3 in the Chinese forum's book (50 GB split across 2 regions = 25 GB effective, 250 GB egress). Now closing: 'Tebi3.31' (Jan 2026) |
| tencent cloud cos () (`腾讯云对象存储`) | Storage is cheap, egress is the entire cost and it is the worst ratio in the set. Standard storage CNY 0.118/GB/mo ($18.06/TB/mo) but outbound traffic CNY 0.5/GB, that is CNY 512/TB =... |
| timeweb cloud s3 | Priced from 1 RUB/GB/mo with an auto-upgrade ladder (79 RUB for 10 GB, 349 for 100 GB, 'unlimited' 639 RUB/mo capped at 250 GB included then 4 RUB/GB), and egress is only 100 GB/month free |
| typesense cloud | The 'free tier' is a one-time 720 hours (30 days) of compute plus 10 GB of bandwidth, consumed once for the lifetime of the account, a trial rather than a recurring free allowance |
| uploadthing | Free '2GB App' shared across all apps, no egress allowance beyond that; next tier is 100 GB for $10/mo |
| utho object storage (in) | INR 500/mo for 100 GB then INR 4/GB = $42.34/TB. 'No egress fees in India' is genuinely attractive but the storage rate is 20x the floor |
| zrok (netfoundry public instance) | Free plan is bandwidth-metered at 5 GB/day over a rolling 24-hour window, with 50 share backends. It is a tunnelling service, so all traffic transits their edge |

### `not-storage` (75)

| provider | why it fails |
|---|---|
| / / / / / / (korean webhard category)... | The whole category is a **download-credit** business, not a storage business. Every one of these gives new sign-ups free *download coupons and points*, never free storage. The product yo |
| academia.edu, data upload | Same category error as ResearchGate, one step worse: it is a paper-sharing site with premium paywalls and no repository function, no DOI, and no documented byte quota because it was never de |
| academic literature on free-tier pooling /... | Does not exist. Four separate research-broker queries ('multi-cloud storage cost optimization free tier', 'erasure coding multi-cloud storage cost', 'free tier cloud storage aggregation serv |
| activeloop deep lake / hivemind | The product pivoted away from storage. deeplake.ai/pricing now sells 'Hivemind' agent traces and queries ($15 credits, 150k traces, 1.5M queries) with no storage allowance at all, and the FA |
| akash network | It is a compute marketplace, not storage: persistent storage is a paid resource attached to a deployment (per-GB-month in AKT), ephemeral by default, and there is no object-storage or IPFS p |
| alexhost storage | Named, checked, and there is no storage VPS, the VPS line is NVMe up to 80 GB. The storage product is a dedicated server starting at 20 TB HDD for EUR 153/mo, and it is listed 'Coming Soon'... |
| appsumo | No storage product exists in the catalogue. A site search for 'storage' returns 344 products and the top results are scheduling and social-media tools (TidyCal, AdaptlyPost), AppSumo's life |
| baseten | Inference-only PaaS. The pricing page is a model-API price list ($/token) plus per-second deployment billing; there is no storage product, no artifact store, and no free tier bytes to claim |
| cloudflare hyperdrive | Not a store, it is a connection pooler/cache in front of an origin database. It carries no storage of its own, so it adds nothing to the byte budget. Its 100,000 queries/day free quota is |
| cloudflare images, storage | The Free plan explicitly has NO storage: 'The Paid plan allows transformations, as well as access to storage in Images.' Free is transformations-only, 'up to 5,000 unique transformations eac |
| cnab (cloud native application bundles) | A packaging spec for distributed apps, not a storage provider; it defines a bundle format pushed to an existing registry. Adds nothing beyond ORAS itself |
| copernicus cds / ads | Retrieval-only by design: a queue-based API (`cdsapi`) that materialises requested slices. There is no user deposit path, so it cannot store arbitrary data, it is a data source, not stor |
| core (core.ac.uk), the 'can i deposit?' answer | No deposit path at all. CORE is a harvester: it indexes full text from repositories it already crawls and explicitly refuses author submissions. The API key is free and the fulltext is real |
| creodias free trial (cloudferro) | A credit, not storage: up to EUR 250 valid for 6 months, considered per applicant and revocable at will ('CloudFerro reserves the right to refuse granting free credits for any reason at any |
| data.europa.eu | Aggregator of national portals and open-data directives, not a host. Listing requires being an authorised representative of a European institution or a national/regional portal; there is no |
| data.gov (us federal catalog) | Metadata-only harvester. It does not host data files and has no self-service publisher path at all: sources are federal agency data.json inventories. The contact page states plainly that it |
| data.gov.uk (uk national data library) | Stopped hosting entirely. The 2026 guidance says the Library 'does not host datasets', publication must be on the organisation's own website, GOV.UK or the service's own hosting, then add a link |
| datacite commons, openalex, base, semantic scholar s2orc | All four are discovery/index layers with zero writable storage. DataCite Commons is the PID graph over DOIs; OpenAlex and BASE are harvesters; S2ORC bulk access is per-release S3 partitions |
| eurohpc benchmark access (as a storage route) | Explicitly a short pre-allocation test: 'Users receive a limited number of node hours; the maximum allocation period is three months.' No storage allocation and no renewal path beyond re-app |
| eurohpc ju benchmark access as a storage route | Benchmark access gives 'a limited number of node hours; the maximum allocation period is three months' for code-scaling tests. No storage allocation is described at all. Regular/Extreme acce |
| europeana | Aggregator, not a store. Europeana ingests metadata from accredited national aggregators and domain aggregators; an individual cannot deposit bytes, and the media stays on the provider's ser |
| europeana (incl. europeana 3d) | An aggregator, not a host. Content arrives by harvesting institutional metadata; there is no self-serve deposit and no byte storage. /share-your-collections returns nothing usable and api.eu |
| falco | No storage provider named Falco exists to verify. falco.io and falco.org both resolve to the CNCF runtime-security project (falco.io serves 'Falco, Why Falco? Strengthen container security' |
| filecloud (community edition) | Free edition is self-hosted only, 5 full users and 10 external accounts on infrastructure the deployer owns and pays for, i.e. it is a Nextcloud/Seafile substitute, not a storage provider. The hosted |
| fleek | The product is gone. fleek.xyz serves a placeholder: 'What if you could start over? We've been building something new.' No storage product, no pricing, no docs |
| gaia-x / catena-x as free hosting | Both are federation and trust frameworks, not storage providers. Gaia-X issues credentials and compliance labels; Catena-X onboards companies into an automotive data space. Neither hands out |
| gitgud.io | Free GitLab-based host, 100k users, zero-tracking, but publishes no storage or LFS quota anywhere I could reach. Their support repo 504'd and /help returned 409. Unverifiable, and a GitLab i |
| gpt4all / jan / lm studio / weights.gg (the 'desktop llm... | All four are distribution front-ends, not storage: gpt4all.io 301s to nomic.ai/gpt4all and its model catalogue is a static JSON in a GitHub repo (gpt4all-chat/metadata/models3.json, 40 KB) |
| guifi.net (as a storage provider) | A Catalan community telecommunications network built on shared infrastructure and social economy - the offering is connectivity and a commons, not storage. The site is Catalan-first and the |
| hasura cloud (ddn) | DDN Free is a control-plane/API tier, it exposes GraphQL over a database he already pays for. It provides no storage of its own; the storage limit is whatever the connected DB has. Rendered |
| host europe (hosteurope.de) storage server | No storage-server product line reachable. /Server/Storage-Server/ returned HTTP 422 through the reader and an empty body direct; the only published documents are legacy Preis- und Leistungsv |
| humble bundle (software bundles) | No storage. The software bundle page describes only pay-what-you-want game/dev/creative bundles; there is no storage or hosting category and no per-TB product |
| idrive personal 20 tb | $29.99/mo for 20 TB = $1.50/TB/mo, the cheapest headline in several 2026 price roundups, but it is backup software, not a storage endpoint: no rclone backend ('I'm afraid we don't have a ba |
| inspire-hep | Metadata and literature index only, it hosts no files at all, so there is no storage to gain regardless of quota. Its whole content model is records pointing at external full text |
| iroh-live | Media livestreaming over iroh (134 stars). Live media is a stream fan-out problem, not a stored-object problem; nothing is retained |
| jetbrains student pack | IDE licences only, no storage product of any kind. Nothing to place bytes in |
| kakao mybox (mybox.kakao.com) | Origin DNS fails from this network; cannot verify any quota. Kakao's corporate site only describes KakaoTalk, not a storage product with a free tier |
| manitu (manitu.de) root servers | Dedicated-only and priced far above the lane: Root-Server M EUR 67.22/mo excl. VAT for 2x 2 TB SSD SATA = EUR 16.81/TB, with a EUR 500 setup fee. No high-capacity HDD storage product. Not a... |
| microsoft teams free (5 gb) | Files are stored in OneDrive and share the same 5 GB consumer quota - not an additional pool. The 'images/videos have no storage limit' line is a possible smuggling route but unverified |
| several accounts across big-cloud free tiers | Every provider in this slot rules it out explicitly and technically aggregates usage: Oracle 'One Oracle Cloud Free Trial or Always Free account is permitted per person'; AWS aggregates usage across |
| naranja.tech | Checked, no storage product. All lines are NVMe 30-120 GB; the generous part is transfer (5-20 TB), not disk |
| njalla | Not a storage product. Largest published disk on the VPS line is 30 GB; storage-only tier does not exist on the site. Privacy-brand pricing, not capacity pricing |
| nostr relays as a byte store (including base64-in-event... | NIP-94 is metadata only, and the relay event size ceiling (~64 KB) caps any inline payload at roughly 48 KB after base64 expansion. Chainable as an index for Blossom, worthless as storage |
| openaire graph | Not a repository, its dumps are published *onto* Zenodo (community 'openaire-research-graph'), i.e. it consumes the same 50 GB/record budget everyone else does. 10.8 GB per part |
| packagist (php/composer) | It is an index, not a store. /about states packages are described by composer.json in 'your package's git/svn/.. repository', Packagist hosts metadata only and dist URLs point back at GitHu |
| pq hosting storage vps | https://www.pq.hosting/storage-vps returned HTTP 404 through the reader. No storage product at that path |
| quicknode ipfs | IPFS is not in the free tier at all. The Free trial plan lists 'Streams, Webhooks' only; IPFS appears first on the $49/mo Build tier. It is an add-on to a paid RPC plan, with no storage quot |
| racknerd | On the named list, checked, and there is no storage VPS product. The whole KVM line is RAID-10 SSD with 30-75 GB disks; the cheapest 20 GB plan is $21.99/yr. The only big-disk offering is a |
| racknerd, as a storage provider | Universally recommended on NodeSeek for cheap compute ('RN 14 20T') but they have no storage-VPS product line: /storage-vps/ and /storage both 404, and the homepage sells 'KVM VPS, AI VPS |
| saturn cloud | No free tier on the current plans page, it opens directly into a paid GPU/CPU rate table (cheapest listed is a 4 GB / 2 vCPU t3.medium at $0.15/hr, then nebius boxes). No storage allowance |
| seaart ai | Renders as an app shell; the /pricing and /models pages returned only nav chrome and generator marketing with no storage or upload-limit numbers. Same class as TensorArt: a generation site w |
| servdiscount (servdiscount.com) | Storage-server page returned HTTP 504; the English product page rendered a table header with zero rows (JS-hydrated pricing). No price obtainable. Aggregator rows (SD-SM-1275 at EUR 45/mo... |
| slite | No free plan at all any more, pricing is a 14-day trial and then 'you will see a message that purchasing one of our subscription plans is necessary to continue'. Not a storage candidate |
| streamable (as a durable store) | Listed as a candidate for completeness but the 90-day auto-deletion is disqualifying on its own, a storage target that erases content on a timer is not storage |
| supercharged git lfs (supercharged-lfs.com) | Explicitly paid: $5/month per 50 GB stored, and $99/month for the BYO-S3 tier. Its own pitch admits the LFS hosts cap files at 2 GB. No free tier beyond the sales page |
| techsoup as a storage provider | TechSoup is the *validation gateway* (NGO database token) for Box, Microsoft and others, not a storage provider itself. The Microsoft product catalogue now shows only Windows ESU and similar |
| test_collection as a staging area | Explicitly temporary: 'Items uploaded to the test collection will be removed in approximately 30 days.' Not storage, it is a trial bucket |
| threadless artist shops | Minimum 2000x2000 px, print-file templates; no arbitrary-file path and no storage figure, it is a merch shop, not a host |
| travis ci artifacts | The artifacts addon uploads to a project-owned S3 bucket; the job supplies ARTIFACTS_KEY/ARTIFACTS_SECRET/ARTIFACTS_BUCKET. Travis provides no storage at all; it is a BYO-bucket shim. Also unavailable o |
| uc drive / uc and quark as storage (`网盘`) | Both are cookie-or-nothing, and the cookie only comes from a logged-in +86 account. Quark's own download tickets are IP-bound, so even a harvested cookie cannot be shared across hosts, it d |
| warg.io / wa.dev (wasm package registry) | warg is an in-development federated index protocol, not a storage service, it is 'not opinionated about how package content is stored and hosted'. wa.dev returned 504 on read. No free bulk |
| z-library | Uploader is a catalogue, not storage: 50 books per web upload before FTP access must be requested, registration required, and every file is deduped against the library. No account storage quo |
| zoho wiki / readthedocs / tettra | Zoho Wiki is free for 3 users but publishes no storage number anywhere in its FAQ; ReadTheDocs Community is free for open-source and publishes no storage quota (only build resources: 7 GB RA |
| dumbpipe / pigeons / iroh-ssh (as storage) (self-hosted) | Tunnel products, not stores. dumbpipe's own tagline is 'Unix pipes between devices'; pigeons is SSH-over-iroh; iroh-ssh is 'SSH to any machine without ip'. They pass bytes and keep none, us |
| freifunk (as a storage provider) (self-hosted) | A federated set of German community WiFi projects whose stated purpose is free communication and open routers. No storage service, no quota, no API - the contribution model is 'make your Wi |
| grass (as a purchasable egress or storage path) (self-hosted) | Pays contributors in points converted to token/USDC; publishes no per-GB rate and no consumer product to buy. Stage 2 rewards closed 8 June 2026 and the claim window shuts 22 January 2027, s |
| lakefs (self-hosted) | Self-hosted data-versioning over an existing object store, it versions data, it does not store any. Zero free bytes; it is a layer above whatever S3 bucket is already paid for. Useful structurally |
| minio saas / zenko / garage as paid object storage (self-hosted) | These are self-hosted software, not storage services, there is no per-TB price because there is no storage included. MinIO and Garage are software run on someone else's disk (so the rea |
| osdf / pelican platform as a free origin (self-hosted) | Data can be federated by running a Pelican origin, but that means supplying the storage, the certificate and the host, the platform is a distribution layer, not a storage grant. N |
| perforce p4 (helix core) free edition (self-hosted) | The '20 users / 1 TB' figure does not exist on Perforce's pages. Current free tier is 'up to 5 users and 20 workspaces' with no storage allowance at all, it is a self-hosted server, so byte |
| zeronet (self-hosted) | Not a storage provider: a BitTorrent-based P2P site distribution tool with no hosting, no quota, no SLA, and no seeding guarantee beyond whoever is online. Requires a local machine to seed |
| disk-o (disk-o.cloud) (self-hosted) | Not a storage provider, a desktop aggregator client that mounts *other* clouds (its own copy: ' Mail.ru'). It contributes zero bytes |
| disk-o (mail) as a storage source (self-hosted) | It is a multi-cloud client/aggregator for Yandex Disk, Google Drive, Dropbox, Mail.ru etc., it owns no storage and adds no quota, so it can only ever surface the 5-8 GB free tiers it aggreg |
| strada (self-hosted) | Real iroh-shaped product (remote editing off somebody else's hard drive, 'upload nothing', 7 TB of source media over home internet per their case study) but it is an app, not a storage provi |
| radicle (self-hosted) | Not a storage provider and structurally cannot become one: it is a peer-to-peer forge where 'repositories are replicated across peers in a decentralized manner'. There is no host to upload t |

### `paid` (29)

| provider | why it fails |
|---|---|
| 115 paid-capacity route | The only path to 115TB/1PB is buying 5-year VIP bundles (the '15GB+115TB' and '5PB+15GB' rows). Free is 15GB flat, so the provider reduces to a paid product at these volumes |
| bonsai (managed elasticsearch/opensearch) | No free tier at all any more, the cheapest plan is Staging at $15/month for 1 GB storage / 100K documents. The historical 1 GB free cluster is not on the current pricing page |
| bunny stream / bunny storage | No free tier, Stream is 'only pay for the traffic' plus $1/month minimum and a 14-day trial; Storage is $0.01/GB/mo with free traffic to Bunny CDN only. Note for the swarm: Bunny *Storage* |
| bytesized hosting / appbox | No free tier at all, 'From EUR 5/month', 500 GB to 18 TB paid, add-on storage at 6 cent per 10 GB/month. Same for Free Packet ('Starting at $9.00/month') and freepacket.co |
| carbonite safe | No free tier at all, 15-day trial then $8/month for a single PC. Excluded as a backup service anyway |
| filemoon | Reachable (200) but the landing page offers only paid-tier marketing ('Storage 2.4 TB', RAID storage, $45/10k views), 2.4 TB is a paid-plan figure, not free, and there is no free anonymous |
| files.com | No free tier at all. Starter is $199/month for 10 full users and 1 TB monthly storage+transfer; only a 7-day trial is free, and extra capacity is $100/TB/month. The whole category prices per |
| fly.io, volumes and free allowance | There is no free tier for new organizations, full stop: 'Is there a free tier? No. New organizations don't have a free tier or a monthly free usage allowance.' New accounts get a trial of 'u |
| gitpod / ona | gitpod.io now redirects to ona.com, which routes to 'Contact sales' with no public pricing and no free tier. The free-tier Gitpod that people remember is gone |
| groups.io free (1 gb, and files is premium-only) | Basic plans: 1 GB. Worse, the storage is unreachable on a new free group: "Restriction: This feature is available only in Premium groups, Enterprise groups, and legacy Free groups." Groups c |
| guru | No free tier and no published storage or attachment number. Pricing page is entirely sales-led ('Get a package built around your scale'); the old 'Guru Starter' free product no longer appear |
| iagon | Cheapest plan is $2.20/month for 500 GB, no free tier at all. Closest thing is a token-hold discount ('Per GB dollar value of tokens to be held = 0.2USD'), i.e. staking |
| lancedb cloud | The self-serve Cloud tier was folded into Enterprise and the free credits programme has ended, so there is no free tier to hold bytes. It is a vector/lance-format database, not a blob store |
| meilisearch cloud | No free tier; $20/month minimum with a 14-day trial. Search-only index, no binary support |
| microsoft teams essentials / m365 business paid tiers | 10 GB per user (Essentials) or 1 TB per user (Business) but they are paid products - a trial at best. Only the Developer Program sandbox is actually free, and it is listed as a candidate abo |
| moveit / serv-u / filecatalyst / progress ws_ftp | All four are now Progress/Ipswitch enterprise MFT products sold by quote or per-server licence. None of them advertise a free hosted tier; they are the incumbent paid products this niche's f |
| mts web services (mws cloud) object storage | No free tier found; S3 is a paid enterprise product sold with a CDN bundle discount. Nothing to multiply |
| pastebin.com | 512 KB per paste (10 MB only on paid PRO), guests limited to 10 new pastes per 24h and cannot create private pastes, plus spam filtering that can add a human-verification step. Three hard caps at once |
| proton mail free | 1 GB storage only ("Proton Free, 1 GB storage"), and the programmatic path is paywalled: "Proton Mail Bridge is currently available only with a paid Proton Mail plan." Zero-access encryptio |
| put.io | No free tier. The trial is $0.99 for 24 hours ('Try every put.io feature for a day for $0.99. Ends after 24 hours'). Does not clear even the trial bar for storage use |
| redpanda cloud | No free tier. Serverless is pay-as-you-go or annual commit; Enterprise Edition is a 30-day trial. Nothing to store bytes on for free |
| sendowl | No per-file limit and SFTP ingest is genuinely good, but storage is ~1 TB before the plan is moved to a custom/enterprise plan, and there is no free tier ($9/mo minimum) |
| storj / sia / origrid / swisstransfer / transfer.it... | Storj has no free tier left, only a 30-day trial ('Free for 30 days', '25GB free storage for 30 days', 'No credit card required'). Sia's hosted product is 50 GB on the $0 plan. Origrid is 25 |
| tesla dashcam / sentry cloud | There is no Tesla-hosted recording store to begin with: footage loops on a local USB drive and is only streamed live with Premium Connectivity ($10/mo). Third parties (teslacamdrive.com) sel |
| thru (now boomi) | No free tier; the pricing page is a Boomi MFT trial funnel ('Start free trial' links all point at boomi.com/form/boomi-mft-trial). Acquired and re-packaged as enterprise MFT |
| walrus (sui) | $0.023/GB/month with no free tier, billed on encoded size which is ~4.5x the file plus 64 MB per-blob overhead. A 50 GB file for a year is ~$62; 20 TiB would be ~$25,000/yr and rising with e |
| webhard.co.kr (enterprise, lg u+ lineage) (`웹하드`) | The genuine 'webhard' product is enterprise file collaboration sold by capacity: 20 GB at 49,500 KRW/mo, 60 GB at 148,500, 500 GB at 396,000, 1,000 GB at 693,000. There is no free tier with |
| xata | Explicitly no free tier. Xata Cloud is a 14-day trial then $0.012/hr compute + $0.28/GB/mo storage. The open-source engine is Apache 2.0 (self-host only, no hosted storage) |
| zoolz | no free tier remains; the pricing page opens directly on paid plans (2.5 TB at $79.99/year). Same corporate family as PolarBackup; its own 'important message for Zoolz Home users' blog post |

### `quota` (550)

| provider | why it fails |
|---|---|
| 'email as filesystem' projects (imapfs, imapfs, gmailfs,... | All real, all abandoned or trivial, none production-grade. waweber/imapfs (7 stars, last push 2024-03) documents the fatal economics itself: base64 means "a 33% overhead (only 75% of server |
| 'write: true' in an alist /api/fs/list response | The single biggest trap in this niche, record it as a rule. Eight separate instances reported `"write": true` for the guest user while every actual PUT returned {"code":403,"message":"permi |
| (afdian) (`爱发电`) | Chinese creator-subscription platform; no public per-file storage figure, and creator payout is Alipay/WeChat gated, the exact identity wall |
| (geegeng, geegeng.com) (`桔梗云盘`) | 1 TB free with 100 MB no-login share links, and it looked like '123'. Two hard blocks: registration is a Chinese mobile number plus SMS (''), and the site's TLS certificate h |
| (huotan) (`货摊网`) | Small Chinese digital-goods stall platform; PayPal + Alipay + WeChat, buyer/seller docs exist but no published file-size or storage number was findable, unquantifiable, so unusable |
| (smzdm) / chinese netdisk promo calendar (`什么值得买`) | The /618 promo ecosystem is entirely Chinese-consumer netdisks (Baidu SVIP CNY 162-189/yr, Quark, 115, ) and it fails on identity, not price: every one requires Alipay/WeChat |
| / china unicom cloud (pan.wo.cn) (`联通云盘`) | Wikipedia lists 500 GB free, but the host did not resolve from this vantage point and the community reports the web client actively blocks F12 inspection and that login is app-QR-only (' |
| 10 tb migration program (`天翼云盘`) | The cheap path to a 10 TB account (10 TB packs '', resold accounts under CNY 10) partially closed: '92710T10T'. Buyable 10 TB accounts survive; the free migration r |
| 123 free tier (123pan) (`云盘`) | 123pan is listed as 2 TB free. As of 2025-11-26 the free tier gets 20 GB/month download across all clients (10 GB if third-party clients are used), OpenAPI became a paid '' at CNY 20/mo |
| 123pan free tier as a serving/fetch tier | Even though storage looks like 2TB, free extraction traffic is 10GB/month all-clients (20GB of bytes via the official client), which is ~1000x short of a 500 GB to 1 TiB daily workload and become |
| 123pan guest download (the old anonymous path) | The one genuinely useful anonymous path in Chinese pans, no-login download of files under 100 MB, was switched off on 2025-11-26. Anything written before that date about 123pan anonymous d |
| 123pan vip (20 tb) | Cheaper tier of a provider already rejected on identity. CNY 258/yr continuous annual = ~CNY 21.5/mo. At 20 TB that is ~CNY 1.08/TB/mo (~$0.15/TB/mo), again an order of magnitude below... |
| 163.com / 126.com free (netease) | 3 GB mailbox with a 280 MB bundled netdisk, attachment cap 20 MB: "3G280... 20". IMAP is live (`imap.163.com:993` -> `APPENDLIMIT=71680000`, 68.4 MiB), so the protocol |
| 189.qaiu.top, netdisk-fast-download ''... | AUTH-REQUIRED and paid. This is the tier that actually covers Baidu Pan, Quark, UC, 139, 189 and Unicom, precisely the pans the free tier omits. Every /parser call returns HTTP 401 'API |
| 4shared paid | Could not verify. https://www.4shared.com/upgrade/ and /upgrade both 302 to https://e.4shared.com/linkerror.jsp and render 'linkerror' content; /plans.jsp likewise. No price page obtainable |
| 500px | A Basic free account is capped at 21 uploads per rolling 7 days (~1,092 images/year). 'Lossless original image storage' is a paid Pro feature, not free |
| 61cloud / (now61.com) (`六一云`) | Free tier is 61 GB and WebDAV is explicitly disabled on it. The member-benefit table shows 'WebDAV ' on Basic (free) and only from Standard (CNY 5/mo, 200 GB). So the free tier fails quota |
| 8gears container registry (container-registry.com) | Per-user dedicated Harbor instances with project-level storage quotas; the pricing markdown twin renders empty (JS-gated) and signup provisions a paid subscription instance rather than a fre |
| abv.bg free | Blog states the quota evolution 6 GB -> 10 GB (7 GB mailbox + 3 GB drive), and the live IMAP port did not complete a CAPABILITY handshake. Under threshold regardless |
| academia.edu | upload flow documented but no quota anywhere in the help centre; documents are public-by-design and tied to an academic identity. No API |
| acronis cyber protect (bundled cloud storage) | Cloud storage is a license add-on, not a product. Essentials tier includes 5 GB per workstation; 50 GB requires Standard, 250 GB requires Advanced/Server. No free storage-only tier, no S3/We |
| afrihost and xneelo (south africa) | Neither sells bulk storage as a product; both sell web/cloud hosting where disk is a small attachment to a compute SKU. Afrihost Bronze is R310/mo for 100 GB ($18.90/TB, but only 4 TB of bu |
| ai data commons as storage: fineweb, common pile, dclm,... | All five are read-only distribution, not deposit targets, and they all sit on infrastructure that cannot be written to. FineWeb (25.9B docs / 48.6 TB) and Common Pile (8 TB) and Pleias comm |
| ai2 / allenai hosted datasets | No user-facing hosting. allenai.org/data is a catalogue that points at Hugging Face (allenai/WildChat-1M, allenai/winogrande), GitHub, or Semantic Scholar, there is no 'upload your data to |
| airtable for nonprofits (50% off, not free) | Nonprofit plans are 'a 50% monthly discount per user on Team plans', not a grant. Attachment storage per base: Free 1 GB, Team 20 GB, Business 100 GB, Enterprise 'Unlimited attachment stora |
| aispace.sh agent file drop | Free tier is 10 MB of storage and 100 uploads/month, max 7-day file lifetime, explicitly 'nothing lingers'. Off by 5 orders of magnitude |
| akkoma / pleroma hosts as a distinct quota tier | Probed akko.wtf, cofe.rocks, pleroma.envs.net, spinster.xyz. The first three return `{"error":"Nodeinfo schema version not handled"}` on /nodeinfo/2.0 and no useful /api/meta; only spinster |
| alist.ucu520.top, openlist v4.2.6 | Structurally broken: root listing returns {"code":500,"message":"failed get storage: storage not found; please add a storage first"}. The web UI is up, so a naive HTTP-200 liveness test pass |
| alist.zlion.top, zlion resource site | WebDAV was withdrawn by the host because of excess use, the index note reads ' WebDAV' (previously had WebDAV, now closed due to excess use). /api/public/settings and /api/fs/list both |
| amazon kdp (kindle direct publishing) | 650 MB conversion cap and 8,000-page cap; large files are actively discouraged and conversion fails above the limit |
| amazon photos | Unlimited full-resolution photos only for Prime members, Prime is paid, so this is not a free tier. Free accounts get 5 GB; video is capped at 5 GB even on Prime. No public upload API |
| amazon sns | Pub/sub only, zero storage. 1M publishes/month free, but messages are pushed and discarded; there is nothing to read back later |
| ameriflux | Deposit is gated on registering a physical tower site and having a Site PI choose a data policy; content is restricted to half-hourly flux/BADM formats. No blob storage, no general quota |
| anaconda.org free plan | 3 GB total per account; would need ~6,800 accounts for 20 TiB. Corporate-use condition since 2024 |
| anna's archive | No upload endpoint of its own, it is an index. Its FAQ routes uploads to Z-Library / Libgen.li and only takes >10,000-file dumps by email contact; its own 'datasets' are torrents of metadat |
| anonymous spn2 (no account) capture | The 2022 spec advertised 4,000 captures/day anonymous; live endpoint now refuses all anonymous writes with 401 and the GET form 429s |
| anonymous write to any github surface | Every write path needs an authenticated identity: anonymous release create -> 401, anonymous GHCR push scope -> DENIED, anonymous release-asset upload -> 400. The multiplier therefore depend |
| anubis / techaro botstopper walls (dans, dataverse.nl,... | Proof-of-work interstitial served with HTTP 200 on every HTML route. It inflates naive status-code probes: 10 hosts looked like they had an open signup form when the body was actually 'Makin |
| api.video | Encoding free but hosting is $0.00285 per minute per month and delivery $0.0017 per minute. Per-minute-of-video pricing, so it is both paid and duration-shaped; 10,000 hours would be ~$1,710 |
| appimagehub | Whole site sits behind an Anubis proof-of-work automated-traffic filter (upstream_status 200 but body is 'Making sure you're not a bot!'). Also it only indexes AppImages hosted elsewhere - it is a catalogue |
| appsumo pcloud 500 gb and icedrive lifetime listings | Both SOLD OUT / withdrawn. The AppSumo 60-day refund window, the main protection a lifetime buyer had, is therefore unavailable for storage. pCloud and Icedrive now sell lifetime only dire |
| appveyor artifacts | 14-day free trial only, no perpetual free tier. Artifacts are stored in 'AppVeyor cloud storage' but fetching them by URL requires authentication, no anonymous public artifacts |
| arch user repository (aur) | Git only, PKGBUILDs and small aux files; hard 256,000-byte (250 KiB) per-blob limit enforced in aurweb's git hook. No binaries at all |
| archive-it | Paid subscription crawler, not free storage; only appeared because it shares the Wayback infrastructure |
| archive.org forum '10gb per item' guidance | Decade-old staff answer; superseded. Real current limits are 1TB/item. Recorded so nobody sizes an architecture from it |
| arlo (netgear) camera cloud | Best-documented camera cloud of the lot (pyaarlo, jbyway/arlo-api, Meatballs1/arlo-cam-api, several downloaders), and all of it is read: library, CVR m3u8 pieces, snapshots. 30/60/90-day ret |
| arvancloud free cdn (iran) | Free CDN tier is 100 GB/month of traffic, per a LowEndTalk report and their own catalogue entries, a third of Gcore's free slice and with far worse latency outside the region. Also a genuin |
| arxiv | Endorsement-gated and paper-shaped: 'We only accept submissions from registered authors. If you are a new user or are submitting to a new category, you may be required to find endorsements' |
| asu dataverse / unc dataverse / uva dataverse (unverified... | All three answered the liveness and quota probes (6.11 asu build, 6.8, 6.9) and all three report 'No quota defined for this collection', but I did not establish their deposit eligibility, s |
| atlassian anonymous media-upload token (jira service desk... | A promising-looking wrapper that dies on probe. Public Jira Service Desk portals emit an anonymous, 20-minute 'mediaApiUploadInformation' bearer token scoped to 'urn:filestore:upload:*' and |
| atomgit (atomgit.com / docs.atomgit.com) | 5 GB of LFS per repo. The capacity doc states it plainly: 'By default, a repository has 2GB Git storage space and 5GB LFS storage space', confirmed by a 2024 user write-up (' 2GB Gi |
| aur | 250 KiB hard blob cap enforced by a server-side git hook. Off by three orders of magnitude |
| aussda (austria) | Self-deposit is limited to researchers at partner universities (Vienna, Graz, Linz, Innsbruck, Salzburg, Krems, WU, OeAW) who sign an archive contract. Not an open door despite 'no quota def |
| aws ecr private free tier (500 mb / 12 months) | Trial, not free tier, and tiny: 'As a new Amazon ECR customer, you get 500 MB per month of storage for your private repositories for one year as part of the AWS Free Tier.' Private repos als |
| aws s3 5 gb / 12-month free tier (as commonly cited) | The current AWS free-tier page and S3 pricing page no longer present a perpetual or 12-month 5 GB S3 allowance; the programme is now $200 of credits over 6 months and the account closes at 6 |
| azure artifacts (azure devops) | 2 GiB free per organization, and publishing is blocked at the limit: 'Once your organization reaches the storage limit, you won't be able to publish new artifacts.' Supports NuGet/npm/Python |
| azure container registry free standard tier | 'Included storage' is bundled into a paid daily SKU rate, not granted free; 100 GB for 12 months then billing. Basic is a paid SKU from day one |
| azure devops artifacts | 2 GiB free per org, hard block on publish at the cap, and pay-go tiers start at $2/GB for the 2-10 GiB band. The 4 TiB Universal Package file ceiling is unusable with 2 GiB of pool |
| azure files 100 gb free | 100 GB for 12 months only, then bills; requires an Azure subscription with card. No path to 500 GB |
| azure for students ($100/yr, renewable) | Genuinely renewable - '$100 credit to use on Azure services within 12 months', renewed annually 'as long as you're a student' - but it is $100, roughly 1-2 TB-months of Blob. Restricted to f |
| azure open datasets | Retired as a programme. Microsoft Learn's overview page 404s and the product page no longer exposes a dataset catalogue or an intake form; what remains is the Planetary Computer, which hosts |
| b2drop (eudat) | 20 GB per user ('For the current prototype there is a limit of 20GB per user'). Well below the bar and the FAQ still calls the service a prototype |
| baidu pan, foreign registration | Explicitly not possible. Baidu's own cross-border channel states ('does not support registration with a foreign phone number'), citing domestic positioning and complian |
| baidu qianfan 'unlimited' knowledge base storage | The unlimited claim is enterprise-tier marketing from 2024 and routes through user-funded BOS. The shared-storage path is documented as '' (small-scale import) with 800 files per KB a |
| baidupcs-go (and every baidu cli wrapper) | Requires a logged-in Baidu account before it will do anything. Its README's tutorial step 2 is literally (), 'log in to a Baidu account (mandatory)'. The fork by qjfoidnh adds shar |
| bandwidth alliance / free-to-cloudflare peering as the... | Every one of the seven answers with 'Server: cloudflare', but that is only the front door. All of them sit behind Cloudflare's proxy on the HTML, and then serve the bytes from their own infr |
| basecamp (free / paid) | Free is 1 GB and 1 project, 3 users. Paid tops out at 1 TB for $199/mo. No free path to bulk and no API for arbitrary binaries |
| basecamp for free | 1 GB of file storage, 1 project, 3 users; 'Public sharing links' and 'additional storage' explicitly not available on the free plan. No API for files |
| behance | 500 MB per file for project asset types and unlimited projects, but Behance renders display images at 1400px/2800px so the source file is not what is served. No upload API, Adobe-account gat |
| bibliotheque nationale de france, depot legal | Legal deposit is an OBLIGATION on French publishers/printers/importers, not an open storage offer: 'le depot legal est obligatoire pour l'editeur, l'imprimeur, l'importateur'. The depositor must be the publisher |
| bioconductor | Hard 5 MB per individual file even after acceptance, and 10 MB per source package. 'individual files must be <= 5MB. This restriction exists even after the package is accepted.' |
| bitbucket cloud free | Free workspaces were cut to 1 GB of total repository storage (all repos combined) effective 2025-04-28, delayed to 2025-05-29. Free plan also lost the Downloads feature entirely and lost sni |
| bitrise artifacts | Time-boxed and aggressively shortened in 2026: non-installable artifacts 90 days, installables 150 days, HTML reports and pipeline intermediates 7 days. Removal is permanent with no recovery |
| blinkenshell / sdf / free shell accounts (the 'tilde'... | Free SSH shell accounts exist and are charming, but the disk is 100 MB (Blinkenshell 'Disk Quota 100 MB', x4 on Supporter at EUR 3/mo). SDF's MetaARPA tier gives '20GB OS images' but require |
| boinc projects as storage | BOINC allocates *client* disk to projects, not server storage to users. The user-facing server facility is a 'file sandbox' for job inputs, and job submitters have explicit server disk quota |
| buzzheavier paid tier | Cannot be checked at all: buzzheavier.com/upgrade returns 404. The vendor's own post-mortem, 'The Real Cost of Storage: A Fresh Start', is the source |
| buzzheavier's original torrent/webseed tier | The 2024 architecture (direct link embedded as BitTorrent webseed, files 'forever and ever', no caps) is gone. The /t/ upload endpoint that minted torrents now 404s, the FAQ that promised pe |
| bytesized hosting, appbox range | Unmetered at every tier but the per-TB rate never improves: EUR 5/500GB (EUR 10/TB) down to EUR 96/18TB (EUR 5.33/TB). Beaten on both axes by HostBrr and PulsedMedia |
| c-v.sh | Advertised as a 'pastor' 512 MiB temporary host, but the documented upload form requires an Authorization header ('Header of type `authorization` was missing' -> 400) and PUT to /<name> retu |
| cafe24 quick server (kr) hdd expansion | The marginal HDD rate is the cheapest found, 16,000/mo per 4 TB = 4,000/TB = $3.02/TB, but it is an add-on to a dedicated server whose floor is 90,000/mo ($67.87) with |
| canva nonprofits (free canva pro, up to 50 seats) | '100% free for registered nonprofits... up to 50 users' but the Pro tier gives '100GB of cloud storage' for the whole team (pricing ladder: Free 5 GB, Pro 100 GB, Business 500 GB, Enterpris |
| catbox.moe (permanent) | Origin is DOWN/behind Cloudflare 521. Direct connection to its resolved IP 108.181.20.35 times out on:443 from here; fetch.web.pkgforge.dev returns HTTP 521 three times with Retry-After: 12 |
| cern document server (repository.cern, inveniordm) | CERN institutional repository, submissions are internal. Also holds no large files: querying files.size >= 1GB returned 0 records out of 73,837, so even as a read source it offers nothing f |
| cern open data portal | Read-only for outsiders. It disseminates LHC experiment data under experiment data policies; there is no deposit path for a member of the public. Excellent free reads, zero write capacity, s |
| cern open data portal / cern document server as writable... | Read-only dissemination for outsiders; CDS submissions are internal. Already recorded by the D-D1 agent; confirmed here as read-only only. No deposit path for a non-CERN account |
| cess deoss | Could not be probed alive: the documented endpoint does not resolve and the Cloudflare-fronted host returns 530. No quota page could be opened, so nothing to report |
| chainguard free images (cgr.dev) | Read-only. Free images are pull-only base images, no push path for user artifacts, and the free entitlement is '5 images of your choice, including previous versions' from Chainguard's catal |
| character.ai | No document/file storage product at all, text persona chat only. Nothing to store |
| china unicom cloud / (pan.wo.cn) (`联通云盘`) | Login wall: fetch returns 200 but read reports sign-in redirect, so the capacity/limit pages are unreachable anonymously. Marketing (500GB-2TB) comes only from forum posts, and the service i |
| circle | Paid-only, storage is 200 GB (Professional) / 500 GB (Business) / 1 TB (Scale, Plus), starting at $89/mo after a 14-day trial, and overage is auto-billed at $10/month per 50 GB block. The o |
| cirrus ci | Could not verify: the API host failed TLS negotiation from this environment, and the docs/pricing pages returned no extractable artifact-storage terms. Recorded as unverified rather than gue |
| civitai training-data / lora-dataset path (as a storage... | The cheapest-sounding Civitai surface is the shortest-lived: 'this data will be retained for 30 days', and training outputs 'retained for 30 days after the completion of the training job'. C |
| civitai vault (paid tier) | The obvious 'personal unlimited storage' feature on Civitai is paid and capped: Free has 'No access to Vault'; Bronze $10/mo = 100 GB, Silver = 250 GB, Gold = 500 GB. It is also download-deg |
| ckan's own default per-file cap (structural, applies to... | The default deployment is hostile to bulk storage before any policy gate applies: ckan.max_resource_size defaults to 10 MB and ckan.max_image_size to 2 MB. Any portal that merely 'allows upl |
| clickup | Free Forever Workspace gets 60 MB of total file storage, not per file, total. Paid jumps straight to 'Unlimited', which confirms the free tier is deliberately useless for this |
| clickup (free plan) | 'File Storage / 60MB' on Free - and the paid tiers are the only route to 'Unlimited'. 60 MB is a rounding error; not chainable in any useful way |
| cloud identity free (as a source of free identities /... | Attractive in theory (free identities, Drive for desktop supported), but it grants no Workspace storage entitlement and no shared drives, so it produces identities with zero bytes, the exac |
| cloudcone storage vps | Storage line tops out at 400 GB (Hashtag-26-Stor-VPS-4) and the headline '$14.24/Year' SKU is 55 GB. Fails 500 GB per unit; annual-only promotional pricing with a 'lifetime recurring' claim |
| cloudflare pages as a mutable object store | Recorded as a boundary, not a provider: Pages (and Workers static assets) cannot be used as mutable storage. Uploads are whole-deployment snapshots via git or wrangler; there is no put/delet |
| cloudflare stream | Paid, and metered in MINUTES not bytes: $5/month per 1,000 minutes of storage (16.7 h) and $1 per 1,000 minutes delivered. The inversion is interesting, because it is duration-priced, a 25 |
| cloudflare stream, video as storage | No free storage at all. Storage is prepaid: 'purchased in increments of $5 per month for each 1,000 minutes of video storage capacity.' Billing is on minutes of DURATION, not bytes, 'Storag |
| cloudmate 500 gb free backup box (beta) | A LET comment advertised 'Backup storage box with SFTP and FTP over TLS access but its currently FREE under BETA 500GB'. The linked cart (host.cloudmate.in/cart.php?gid=34) now resolves to a |
| cloudsmith | Free Core plan is 500 MB artifact storage and 1 GB package delivery, three orders of magnitude short, and the pricing page 429'd on first fetch, requiring escalation |
| cocalc | Pricing page has been reduced to a membership/licensing blurb with no comparable tier table and no published storage figure, the numbers that used to make CoCalc interesting (free hosted pr |
| cocoapods trunk | Trunk accepts a.podspec (JSON metadata, a few KB) and nothing else; the pod's source is a URL field pointing at the project's own host. 'pod trunk push [NAME.podspec] will deploy your Podspec to Tru |
| codeberg (forgejo flagship instance) | Quota is ~750 MiB Git + 1.5 GiB combined LFS/packages/attachments per user, plus 100 MiB for non-promoted/private content, plus 100 MB per release/issue attachment. Enforcement began 2025-05 |
| codeberg (forgejo) packages / container registry | Caps are tiny and hard: 750 MiB git repo, plus 1.5 GiB combined for LFS/Packages/Releases/Attachments, and non-promoted personal repos capped at 100 MiB. Quotas enforced by Forgejo with huma |
| codeberg / forgejo package registry (forgejo packages) | Hard caps: 750 MiB git repository storage plus 1.5 GiB combined for LFS/Packages/Releases/Attachments per user or org, and non-promoted personal repos capped at 100 MiB. Exceptions require a |
| confluence standard/premium as a free route | 250 GB and unlimited are paid tiers; the free tier is hard-capped at 2 GB and archived content still counts |
| conoha (jp) object storage | 450/100 GB/mo = CNY 4,500/TB = $28.50/TB. Its headline pitch is 'unlimited capacity, free data transfer', which is true and irrelevant at 6x the floor. Requires a Japanese payment method |
| contabo object storage as a *new* signup | Product appears delisted from public pricing, contabo.com/en/object-storage/ now 301s to /storage-vps/ (a VM product) and contabo.com/en/pricing/ lists no Object Storage. Orderable only fro |
| contabo storage vps | Worst $/TB of any storage VPS checked, and the advertised price is explicitly a 24-month teaser. Storage VPS 30 gives 1 TB for EUR 11.20/mo = EUR 11.20/TB, five to six times the price... |
| cpan / pause | No published quota, but the whole of CPAN was only 29.0 GB in 2021 and PAUSE has publicly run out of disk. A 2 MB distribution was rejected with 413 'Request Entity Too Large' in a public ma |
| crawl-scale free-host ftp hosts (storage share, cloudtb,... | Every one is paid. Storage Share 1 TB is a paid Nextcloud plan; CloudTB is '100 GB / $2 per month'; FBIPool 'Starts at Only Rs.24 Per Month' for 10 GB; ftpgrid is usage-based. The 'free FTP |
| cstcloud (china science and technology cloud 'data... | The most interesting Chinese-language lead found, and it dies on identity twice. Free quota is 20 GB, 25x short, and it requires (real-name verification) to reach even that. Source |
| ctfile modern /api/v2 download-url | The new web client's download endpoint is signature-gated in a way that is not reproducible from curl. Nine reference shapes were rejected identically with 403 'Download file reference is in |
| cunofs / tigris / garage / hammerspace / weka as... | Wrong problem class, and none of them advertises stacking free tiers. cunoFS is an HPC POSIX-on-object mount (docs now 404 at the previously indexed readthedocs paths, and it is a paid Storj |
| curseforge (upload api / forgecdn) | Media cap is 2 MB; the mod-file cap is not published anywhere I could open, and the CDN actively refuses direct hotlinks, probe through the edge returns 302 to mediafilez.forgecdn.net which |
| czi essential open source software for science (eoss) as... | Grants go to organisations; an unaffiliated person must designate a fiscal sponsor, and every CZI RFA read repeats 'All grants will be awarded to institutions, not individuals'. Also out o |
| dans data stations (knaw, netherlands) / dataversenl | Both sit behind Anubis proof-of-work ('Beveiligde verbinding wordt gecontroleerd...'), and DANS deposit is scope- and institution-oriented (archaeology, SSH, life sciences) with no open bulk |
| darkibox.com | Returns HTTP 410 Gone on the homepage. Dataset lists a 50 GB free per-file cap; the site is retired |
| darus (university of stuttgart, dataverse) | Explicitly restricted to 'Mitglieder und Partner der Universitat Stuttgart' (Stuttgart members and partners) and to completed research results, not a general depositor. Technically capable |
| data.gov.au | CloudFront returns 403 'Request blocked' to the probe for both the API and the register page, so no probe was possible. Publishing is in any case restricted to Australian government agenci |
| data.gov.hk (hong kong) and data.gov.tw (taiwan) | Neither exposes the CKAN action API (404 on package_search) and both have no /user/register route. Data.Gov.HK is a DATA.GOV.HK publishing platform for bureaux and departments; data.gov.tw i |
| data.gov.in (india) | Host did not resolve/connect at all (curl exit 6/000) from this network, so nothing could be verified. India's public-data policy routes publication through ministry nodal officers under the |
| data.gov.sg (singapore) | No longer a CKAN instance, it is a Next.js app and /api/3/action/* returns 404; there is no public register page either. Publication is by Singapore government agencies via the SingStat/Gov |
| datachain studio (formerly dvc studio, iterative) | Control plane only, it connects to the project's own Git remotes and cloud storage. No free byte pool was found on any page, and the self-hosted helm chart is for running the UI, not for ge |
| datacomp (datacomp.ai) | A benchmark definition, not a data host: 'the models are fixed and the challenge is to find the best possible data'. The pools (DataComp-1B CLIP pool, LM pool) live on Hugging Face. No uploa |
| datahub.io | Pivoted from open-data publishing to a paid 'Data Solutions' shop. /pricing 301s to /solutions (enterprise reference datasets, CSV, S3 API for customers); /publish is a 404. No free storage |
| dataone | It is a federation of member nodes, not a depositor. The Coordinating Node answers (cn.dataone.org/cn/v2/node -> 200 XML) but there is no general deposit endpoint; a deposit must go through a memb |
| datarade, see candidate entry (fails-quota) | A brokerage that stores no bytes on principle: 'doesn't host or deliver data'. The whole 'data marketplace' category (Datarade, data.world, AWS Data Exchange, Snowflake Marketplace listings) |
| dataverse installations on 5.5-6.0 (cuhk, icrisat,... | 19 of 149 installs predate the collection-quota feature (Dataverse 6.1+) and return 404 on the quota endpoint. They cannot be scored on this axis at all, the absence of the endpoint is not |
| dataverse upload api (post /api/users, post... | Not usable as a write path in this research frame. POST /api/users is 404 on 6.10+ (endpoint removed); POST /api/builtin-users requires:BuiltinUsersKey (403/404 without it). Writes therefor |
| dataverseno (norway) | Explicitly affiliation-gated: 'Anyone affiliated with a Norwegian research institution can deposit their research data, free of charge at DataverseNO.' External depositors are out unless the |
| dati.gov.it, data.overheid.nl, data.gouv.fr,... | A cluster of national/state portals that fail at the very first probe, 404 on the CKAN action API and either 404/403 on /user/register. data.gouv.fr has its own API (not CKAN); data.overhei |
| debian snapshot | Read-only ingest of the Debian archive; no user write path at any size. 172 TB belongs to the archive, not to a depositor |
| dediseedbox | Pricing is behind a JS configurator; /seedbox-plans/ and /seedbox-hosting/ both 404, homepage returns a heading with no plan table. Third-party figures ($25/3TB = $8.33/TB) are unattributabl |
| deepghs hub (hub.deepghs.org) | An HF-software deployment run by one anime-dataset group (deepghs): 73 models, 25 datasets, 26 spaces, and a 'Host Your Own Hub' link. Tiny to the point of being a personal instance; useful |
| deezer for creators | No upload path at all, 'While Deezer doesn't accept direct uploads from artists, we've made the process simple through our partnerships with trusted music distributors' (TuneCore, OneRPM, D |
| demo.cloudreve.org, official cloudreve demo | Alive but not a filesystem. /api/v4/site/ping returns {"code":0,"data":"4.19.1-pro"} yet /api/v3/site/config and /api/v4/site/config both 404 'page not found', and there is no anonymous list |
| deno deploy deployment assets (static file store) | The deployment bundle cap is 1 GB for ALL files in a deployment: 'the total size of all files within the deployment (source files and static files) should not exceed 1 gigabyte.' 'Revision s |
| deno kv (free tier) | 1 GiB total KV storage on the free plan, 64 KiB max value, 2 KiB max key, 800 KiB max atomic-operation size, 500k write units/mo. Even at 100% packing this is 1/500th of the bar and the writ |
| designsafe-ci / nheri data depot (tacc) | Publishing is genuinely uncapped, 'Currently we do not impose restrictions on the size of the datasets that can be published... Largest published datasets in DDR are ~5 TB', but it is a c |
| deutsche nationalbibliothek, pflichtexemplar | Same legal-deposit model as BnF (German National Library copies of everything published in Germany). Not an open deposit service; the page 404'd on the current path and the model is publishe |
| deviantart core as quota escape | 100 GB requires a paid Core subscription, that is metered spend, not free storage |
| digitalocean spaces via github student pack | The $100-$200 student credit was removed. Changelog: 'DigitalOcean is leaving the Student Developer Pack, and their student credit offer for $200 of platform credit will no longer be availab |
| directus cloud (core) | Core is $0/mo but is capped on seats/collections (3 seats, 25 collections, 5 flows) and provides no advertised free storage allowance, assets go to the storage adapter he configures. Self-h |
| dji flighthub 2 free quota | 100 GB cloud storage per organization, but it is one grant per organization, bound to an Enterprise dock/aircraft, and valid for 3 months only. Effectively a trial, and it needs DJI enterpri |
| dns txt records as a storage medium (desec / duckdns /... | Works as a protocol but the ceiling is ~1 MB per name: one RRset allows max 4091 record values and 64,000 characters total after JSON encoding, and RRset writes are capped at 300/day/domain |
| document360 | Free plan is 1 GB media storage (Startup 50 GB, Business 'Unlimited'), 150 MB per upload, 5,000 files per folder. 1 GB free is far under a 500 GB floor and the upgrade is quote-only |
| draft2digital / smashwords | Accepts only Word/ODT/RTF/EPUB for conversion; Smashwords is being fully absorbed into D2D (final migrations during 2025). An activation fee plus tax verification is required before publicat |
| drone ci (cloud.drone.io) | The hosted cloud service is effectively gone, cloud.drone.io returns 303 with no usable public artifact surface. Drone now ships as self-hosted Community/Enterprise Edition only, so there i |
| dropbox basic | 2 GB free at signup; referral bonuses are capped and the account is capped well under 500 GB. rclone backend exists (Tier 1) but the quota is fatal |
| dryad (data publishing with fee waiver) | A publishing charge, not a grant: $150 for a 0-5 GB dataset, rising by size band, and sponsorship exists only through a partner institution or journal. There is no individual waiver and the |
| dryad, the 2025-26 pricing model | Pay-to-publish, and the price scales with size, so it is anti-correlated with the need. Large-data fees: $259 for >10-50 GB, $464 to 100 GB, $1,123 to 250 GB, $2,153 to 500 GB, $4,3 |
| dspace registry cohort (60 of 60 sampled) | Every sampled site from page 1 of the official registry failed /server/api/info, they are DSpace 6 or earlier with no REST API, or the host is gone. The registry is a museum, not an invento |
| dspace.org/instances | 404, the registry moved. The live registry is dspace.org/registry/ (3,485 entries, 35 pages). Worth recording because the old path is still cited |
| e ysepan (ys168.com) (`永硕盘`) | Looks like a free space-based drive from the outside; it is actually space-purchased (''), with small capacity and small per-file limits. Registration is SMS-gated. Twenty-year-old prod |
| e2e networks object storage (india) | INR 2.5/GB/month is $26.95/TB/mo, 6.6x Utho's archive tier and 17x its own archive, and data transfer is INR 3/GB, i.e. $32.24 per TB read. Worse, billing is on PEAK usage per calendar... |
| ebird / macaulay library | A real media archive with no total quota, but JPG only under 20 MB and WAV under 500 MB, and every asset must attach to a valid checklist (species, count, location, date). Effectively 20 MB |
| ecpan (ecpan.cn) (`移动云空间`) | Listed by netdisk-fast-download and qaiu's parser as a resolvable drive (`ec`), and it does accept share links, but the product is enterprise SaaS with a trial, not a consumer free tier: ' |
| edmond (max planck, edmond.mpdl.mpg.de) | 308 permanent redirect to edmond.mpg.de on every path; the redirect target was not verified, so no quota or identity claim is made |
| egnyte | Trial only, every plan tier says 'Start Free Trial' with no perpetual free plan. The '100GB/150GB' figures on the pricing page appear to be trial or add-on storage allowances, not a free ti |
| elastic cloud (elasticsearch/opensearch hosted) | 14-day trial only, no permanent free tier. The trial is time-boxed, not byte-boxed, so it fails both the free test and the durability test |
| elephantdrive | 2 GB free 'Open Edition'; entry paid is 1,000 GB starting at $10/month. No programmatic path (app-only backup) |
| ena (european nucleotide archive) | Free and effectively unlimited, but Webin accounts are for nucleotide sequence submission only; the upload area is 'a temporary transit area which is not backed up and subject to a fair use |
| enter cloud suite object storage | OpenStack Swift, pay-per-use IaaS, no public price list, only protocol documentation exists. Zero pricing transparency, and Swift is not S3 |
| enzonix | Was part of a 70 GB stacked S3 haul in April 2025, now closed to new signups: 'enzonix' |
| eosc eu node as bulk storage | 50 GB personal / 500 GB group, 1 TB/month transfer, credits that do not roll over and cannot be topped up. Reported as a candidate above for completeness; it fails the 500 GB-per-unit bar fo |
| esa network of resources (nor) sponsorship | Was a EUR 5,000 voucher for any non-revenue EO project; the eligibility now reads 'ESA is currently supporting research, development and pre-commercial APEx and EarthCode ESA projects', and |
| esm.sh as a blob store | It is a *transform* service, not a file server: any module request returns a 136-byte re-export stub pointing at a rewritten path, not the bytes. Only JS/TS modules are addressable, and |
| ethstorage / evmfs / on-chain calldata file systems | Real systems (EthStorage mainnet chain 333, FlatDirectory contracts; EVMFS 20 KB chunks per call) but pricing is per-calldata-byte. Calldata is $11.01/MB live, 10 TiB would be ~$115 million |
| etsy (digital downloads) | 5 files per listing at 20 MB each = 100 MB per listing ceiling, plus a $0.20 listing fee per shard, so sharding costs more than the storage is worth. No programmatic way to attach files |
| eu ai factories, playground access | Free, FIFO, no competitive selection, access within 2 working days, the closest thing in Europe to a self-serve allocation. But it is aimed at 'Industry users' (SMEs/startups) and opens a 1 |
| eufy security (anker) camera cloud | Richest wrapper ecosystem in the niche (bropat/eufy-security-client -> eufy-security-ws -> mega-yfue/eufy-sdk), and it does have an upload endpoint - but only v1/app/upload_devs_params, whic |
| euserv backuphd classic free | 2 GB. The surviving free tier of the host everyone cites for 'free 1 TB'. Two orders of magnitude below the floor |
| evex storage (storage.evex.land) | Genuine unknown that turned out broken. A Hono service whose own page says 'Unlimited storage', with a published SDK (raicdev/evex-storage-sdk), but the upload endpoint refuses every form I |
| farcaster as a file store | Fails on first principles, not on a URL: the protocol stores no media. A cast embed is a URL to somebody else's host, and message acceptance is gated on rented storage units bought on Optimi |
| fars.ee (listed as a file host in the free-s3 research.md... | Not a file host at all, it is a `ptpb/pb` text pastebin and warns 'do NOT post large files'. A useful warning about the catalog itself: one of its 19 rows is wrong, so verify each row befor |
| febbox / (febbox.com) (`二月网盘`) | The corpus carries FebBox as 1 TB free. linux.do documents it being silently cut to 10 GB in March 2026: '1T10G 10G10G/'. Login is Google-only ('Google'), a |
| febbox / feb | The 'free 1TB' figure is stale marketing. The 2024 press release still says 'free 1TB storage', but the live plan page now reads 'Free Plan... 10GB basic space', and the FAQ confirms a down |
| febbox / feb 1 tb free | BAIT AND SWITCH, ALREADY EXECUTED. The 1 TB free offer circulated on Chinese forums in January 2026 (nodeloc thread 75566, '1Tfebbox'). By March 2026 linux.do thread 1753000 was titled ' |
| fed4fire+ / slices-ri | Fed4FIRE+ closed in June 2022 ('reached its finish line... Its legacy will be taken by SLICES-RI'). SLICES is a consortium of 16 European countries still building governance and roadmaps |
| figshare for institutions | Raises file size to 5 TB and private space per institution, but only for users with an institutional figshare repository, no self-serve route for an individual. Institutional quotas are set |
| figshare+ (large-data tier) | Paid, one-time data publishing charge ($875 per 250 GB per a third-party guide); requires a single publication/project, max 10 item DOIs, and all items submitted within 12 months. Commercial |
| filecoin pin (pin.filecoin.cloud) | The public demo is Calibration testnet only: 'data isn't permanent and infrastructure resets regularly', and the UI caps uploads at 200 MB. Mainnet use runs through Filecoin Onchain Cloud, w |
| fileditch old domain (fileditch.com) | Root domain is now only a meta-refresh stub to new.fileditch.com; all real limits/API live on the new host, so any blog citing fileditch.com figures is stale |
| filemoon.sx | Video-hosting shell, not a general file dump: the page is 1605 bytes of 'Byse Frontend' JS that only activates on /e/ embed paths. No upload API and no file storage surface for arbitrary dat |
| filen lifetime plans | WITHDRAWN. Filen phased out Pro lifetime after Black Friday 2025 and has kept the Starter lifetime unavailable since January 2026, citing hardware costs. Existing holders kept theirs; nobody |
| filepost (filepost.com) | Domain is now an ad/affiliate redirect farm ('ww547.filepost.com/?tkn=...' with 'best cloud storage plans' keyword links). The original file host is gone |
| filepost / filepost.jp / filepost.com | Two separate corpses. filepost.jp returns 504 through the reader and has no live upload surface; filepost.com was already recorded in round 2 as an ad/affiliate redirect farm. Also note the |
| files.link ('unlimited storage, permanent cdn urls') | Could not be verified at all: TLS handshake fails through both the reader and the fetcher (Cloudflare 525), and the http:// variant 404s. The 'unlimited' claim in the search snippet is unaut |
| filesend / (filesend.jp, ex-ogis ri), twice dead... | Closed. The landing page reads ', FileSend'. The original was killed in 2020 by a data breach with no resumption (OGIS Ri announced termination on 2 |
| firefish (firefish.social), project abandoned | The flagship returns an HTML shell instead of /api/meta JSON, and the wider Firefish ecosystem has been superseded by Sharkey/IceShark. Do not build against it; the API-compatible successors |
| firstvds vds storage (russia) | The base plan is 300 GB for 949-1,249/mo, $38.31/TB/mo at best, and expansion is priced at 125/mo per 50 GB without redundancy or 185/mo per 50 GB with, which is 2,500-3,700 per TB/mon |
| fitbit / withings health clouds | Both have clean OAuth APIs (wbsapi.withings.net/v2/measure is fully documented, including an llms.md written for agents), but they are data APIs - time series, workouts, measurements. There |
| fjord commons (hosted forgejo) | 5 GB per account and 'Git LFS is not enabled' at all. Free and non-expiring, but the LFS layer is simply absent |
| flock starter (free) | 5 GB of team storage on Starter; paid-only growth. No documented file API |
| stacking free tiers as the host's own upstream (the 'r2... | Ruled out by arithmetic. R2's free tier is 10 GB-month and Bunny/Backblaze free tiers are single-digit GB. No host in this set is running on anybody's free allowance. The real upstream mechanism |
| freeturn.net | Advertises a 2 Mbit/s per-peer cap (0.25 MB/s 21.6 GB/day), but the site returned HTTP 530 on every attempt, so the cap is from a search snippet only and the service could no |
| freidata (university of freiburg, inveniordm) | Unreachable during the probe, the host stopped completing TLS handshakes (curl: 'Failed to connect to freidata.uni-freiburg.de port 443 after 21086 ms'). It answered the API |
| fromsmash free tier | 2 GB before queueing; the '100 GB free' claim is a 14-day developer TRIAL, not a free tier. API access requires a paid account |
| fshare's 4share.vn sibling | 4share.vn is mid-pivot to a paid backup product: the pricing page says 'Dch v dang nang cp' and the only purchasable plan is 50 GB / 30 days for 59,000 VND, paid via MoMo or BoKim, a do |
| gakunin rdm (nii, japan) standard storage | 100 GB per user and <5 GB per file on NII Storage, consumed from the project creator's allowance, and access requires a Japanese institutional GakuNin account ('ID'). Below the |
| game jolt | 3 GB total per game, and users routinely hit it (games taken down for exceeding it) |
| gbif | Publishes Darwin Core occurrences and derived download archives, not arbitrary blobs. Anonymous download *requests* are refused (403), and the synchronous API caps at 100,000 records. The IP |
| gel (formerly edgedb) | Free Cloud tier is 1 GB disk, ~1/4 compute unit. Pro starts at $19.50/mo with 10 GiB. No project multiplication documented |
| geni | No longer a going concern as an allocation portal - the geni.net front page is a news archive whose most recent items are NSF/FABRIC announcements and a 2021 FABRIC workshop. GENI federation |
| gigafile member / paid plan | The paid tier buys ad removal, not capacity. Verbatim from the member page: joining a paid plan gives ' / ' (upload and download without ads), plus playback and fi |
| gitea.com (hosted gitea) | No container registry endpoint at all: GET https://gitea.com/v2/ returns 404. Gitea's cloud offering is a 30-day trial, and the self-hosted product is free software, not free storage |
| gitea.com (official hosted instance) | Instance is live and registration is open, but the container registry is not exposed: /v2/ returns 404 (not 401), and /api/v1/packages returns 404. Only the git side is usable, with no publi |
| gitee (gitee.com) as a storage host | The most precisely documented small quota in the whole slot, which makes it a useful calibration point: 1,000 repos, 500 MB per repo, 50 MB per file, 5 GB total across all personal AND organ |
| github actions dependency cache (as storage) | Explicitly a cache with an eviction policy: 10 GB per repo free, entries not accessed for 7 days are removed, LRU eviction at the cap, and caches are never publicly downloadable. Raising the |
| github campus program (school-level github enterprise... | '50,000 GitHub Actions minutes and 50 GB GitHub Packages storage', 50 GB, licence 'free for one year and will automatically renew annually'. An order of magnitude short, and Packages is a r |
| github codespaces disk | 15 GB-month of storage on GitHub Free, 120 core-hours. Explicitly a time-based quota in GB-hours, not a disk that data can be left on |
| github packages | Already covered (dossiers/github-packages.json); 500 MB storage + 1 GB transfer free on Free plan, metered beyond, far below the bar |
| github packages, maven registry | No file-size figure published on the doc page at all, so no quotable ceiling, cannot be reported as verified. Anonymous read denied (probed 401 Basic realm="GitHub Package Registry") |
| github packages, npm registry | 256 MB per tarball version, and it does not fall under the free-container carve-out; a private package on Free gets 500 MB storage + 1 GB/month transfer shared with Actions artifacts. Public |
| github packages, rubygems registry | Documented cap is on metadata, not payload ('maximum uncompressed size of a gem's metadata.gz file must be less than 2 MB'), and gems are a poor container for bulk bytes. No bulk-win over Nu |
| github pages as a >1 gb site | Hard 1 GB per published site. The 10 GB artifact limit in upload-pages-artifact misleads people into thinking 10 GB is available; the served site is still capped at 1 GB. Only useful as a mu |
| github student developer pack (as a storage programme) | No bulk storage in the pack. The only storage lines are GitHub Pro's 2 GB Packages + 10 GB LFS, plus a Microsoft 365 seat that is tied to a personal account and not API-friendly at scale. Th |
| github student developer pack (bundled storage) | The 2026 pack bundles no bulk storage at all. GitHub Pro gives only 2 GB Packages + 10 GB LFS; the Microsoft 365 offer is '1TB of cloud Storage' for one student; Azure is '$100 in Azure cred |
| gitlab pages | Hard 1 GB maximum site size on GitLab.com regardless of tier, plus a 200,000 file-entry cap and a 150 custom-domain cap. The 1 GB limit is a product-wide constant that an open GitLab issue a |
| gitverse (gitverse.ru) | 2 GB/month LFS storage per user AND per organization, 100 MB per file over HTTP, 1 GB per file over SSH. Too small, hard-capped, monthly |
| gmail as bulk storage | Gmail shares the same 15 GB (or pooled Workspace) quota as Drive, and attachments are capped at 50 MB inbound / 25 MB outbound, so it multiplies nothing while consuming the same bytes. Stri |
| gnu ftp / ftp.gnu.org (mirroring side) | Not a place to put data - ftp.gnu.org is the canonical GNU release server, and mirroring it is a 169 GB inbound commitment in the wrong direction. The upload registration path exists only fo |
| gnu savannah as an sftp target | The transport everybody assumes works does not: SFTP was disabled outright in 2023-11 after a vulnerability, and scp only works with `-O` (legacy protocol) on OpenSSH >= 9.0. A modern client |
| google artifact registry (as a blob store) | 0.5 GB/month free, three orders of magnitude short. Only GC's own container/image storage is bigger, and that is already covered by the known GHCR slot |
| google cloud free trial ($300 / 90 days) | Explicitly time-boxed: 'The Free Trial is a 90-day program'; at day 90 or credit exhaustion 'your Free Trial billing account will be closed and all of its associated projects and resources w |
| google colab as a serving box | Both disqualifiers land at once: file hosting and media serving are on the provider's excluded-activities list, and the VM is deleted on idle. There is no port-exposure feature to misuse even if one wanted to |
| google colab free-tier runtime disk (as scratch storage) | Colab's own FAQ explicitly disallows 'file hosting, media serving, or other web service offerings not related to interactive compute' on managed runtimes; VMs are deleted when idle and runti |
| google container registry (gcr.io) as a separate free tier | Not a separate quota. gcr.io-domain repositories are billed as Artifact Registry ('Repositories that support the gcr.io domain' are listed as storing artifacts subject to the same pricing) |
| google docs / sheets as unlimited storage (uds, base64... | Closed. Collaborative files (Docs, Sheets, Slides, Drawings, Forms) created or edited after 2021-06-01 / 2022-05-02 now count toward quota. The stewardmcgown/uds repo (4.4k stars) still exis |
| google groups as a file store | There is no file storage. Limits are message-activity limits: "Individual message size 25 MB", "Total message size 2.4 GB per hour" per group, "Total inbound emails per group 300 per 5 minut |
| google sites (new sites) as free hosting/storage | Sites and all embedded content count toward the owner's Drive storage, it is not an exempt surface. No independent quota exists |
| gopher / gemini capsule hosting (gemcities, tilde.team,... | Quotas are in megabytes: gemcities gives 50 MB per capsule and exists only for gemtext; tilde.team enforces 1 GB soft / 3 GB hard per user; SDF sells extra disks in 20 GB increments for $3/m |
| grey-market consumer-connection proxies / donated bandwidth as an... | Looked for it and did not find it. What exists instead is the mirror image: hosts are the VICTIMS of consumer-connection/datacentre proxy fleets (catbox closed datacenter+proxy anonymous uploads in |
| groq files api | Batch-only purpose,.jsonl only, 100 MB max file. No general-purpose storage class |
| hackage (haskell) | No documented size limit and no documented quota, could not establish any number from the upload page, the FAQ, or the server source (the upload handler has no size guard visible in Distrib |
| halalcloud / 6 / (2dland.cn) (`盘清真云`) | Surfaced via the OpenList `halalcloud` driver as a live-looking free drive with an OAuth client_id/secret flow. The provider's own landing page now says: 'Project Archived, HalalCloud Has E |
| hathitrust | No individual ingest at all: content can only be contributed by member libraries. Explicit: 'We are unable to work with individuals at this time to add digitized materials to our collection |
| helpjuice | 12 GB / 24 GB / 38 GB by plan is the whole storage story and there is no free plan, 'Free 14 Day Trial' only. Small and paywalled |
| hetzner server auction as a per-tb play | The auction page renders prices client-side and returned only marketing copy; more importantly the auction inventory is bursty and the SX-line fixed price (SX65-2 EUR 82.30) already beats... |
| hetzner storage box / contabo storage vps | Neither has a free tier or a trial. Contabo's cheapest storage VPS is EUR 5.50/mo for 300 GB SSD; Hetzner's Storage Box page returned no free offer. This is the 'free VPS with big disk' sub |
| hippius hub (hub.hippius.com / registry.hippius.com) | The most interesting-looking find that fails on both counts. It indexes 11,452 public models and 1,741 containers and is pullable with docker/oras, exactly the ORAS-as-storage shape this su |
| hostdare hdd vps | The HDD line maxes at 900 GB and the best $/GB is HDD8 (900 GB, 8 TB transfer) at $151.99/yr = $14.07/TB/mo. Nothing 1 TB exists, and the 'DEAL50' recurring coupon referenced in forums does |
| hostens storage vps | OpenVZ containers on 12x4TB RAID, priced at $21/mo for 1 TB = $21/TB, and since May 2026 all VPS are capped at 75 MB/s I/O and 300 IOPS. The I/O cap alone disqualifies it for a hot working |
| hostloc (hostloc.com), as a source | The Chinese low-end forum is effectively closed. NodeSeek threads from ~157 days ago are titled 'hostloc' and 'hostloc""'; the site now serves a ' / ' interstitial |
| hostsailor | Site renders entirely client-side; /seedbox.html returned only the section headings ('features', 'products', 'testimonials') with no plan data, and the homepage is a JS spec sheet. No price |
| huawei cloud obs free tier | The vendor's own free-OBS landing page (special/free-obs-pro.html) returns 404 and has no archive capture. What remains is a 100 GB / 12-month new-user package and a third-party claim of 500 |
| hugging face spaces disk (as persistent storage) | 50 GB sounds like a finding until the second sentence is read: 'This disk space is ephemeral'. Anything written to a Space is lost on restart, and creating a Gradio/Docker Space now needs a |
| hugging face storage buckets (baseline, not a candidate) | Recorded to check the HF numbers, not to claim them. The 2026 shape is materially different from the older entry: Free is 'Best-effort' public + 100 GB private; P |
| i.stack.imgur.com (legacy se host) | still 302-redirects to i.sstatic.net but is no longer an upload target; agents that test the old host will mis-read a redirect as success |
| ibm aspera on cloud | Trial only and small: 30 days OR 50 GB of transfer volume, whichever comes first, and package sending to external users is disabled during the trial. FASP's speed advantage is real but there |
| icos carbon portal | Download requires login and acceptance of a data licence; content is a fixed set of atmospheric/ecosystem variables from registered stations. Not a deposit target at all |
| idigbio | Media hosting is being deleted. 'All images and media will be permanently deleted' and portal media access terminates 31 August 2026; the site has already been demoted to a GBIF hosted porta |
| iheartradio podcast hosting | No free self-serve hosting product to verify. iheart.com/podcast-hosting/ returns HTTP 406 through the reader and the only hosting-shaped documents surfaced are content licence agreements, n |
| imgur as byte-exact storage | PNG >5 MB converted to JPEG, >1 MB anonymous images lossily compressed, 50 uploads/hour. Good CDN, useless for data |
| infinityfree | 5 GB disk, free forever, PHP/MySQL, a real free host but two orders of magnitude short, and web-root only |
| instances.social / fediverse.observer / fedidb.org, the... | All three were unreachable at probe time, so the sweep had to be done host-by-host. instances.social requires a manually-issued OAuth token and its list API is gone; api.fediverse.observer n |
| ionos free vps trial (30 days) | The 'free VPS' is a money-back guarantee on a paid contract, and the disk is the problem: the trial-matching tier is 'VPS S+... 1 vCore, 2 GB RAM, 60 GB NVMe'. 60 GB is 8x below the floor... |
| ipfs / libp2p circuit relay v2 as a data path | Protocol defaults are 2 min and 128 KB per direction, deliberately sized for hole-punching (DCUtR), not transfer. Kubo ships these defaults and the docs say v2 relays exist 'to enable NAT ho |
| ipfs / shipyard (the 'ipfs-like service' under test) | The IPFS pinning lane is closing, not opening, and free IPFS pinning is already excluded at <=6 GB. iroh's own blog frames Mainline+blake3.net as the successor, which is w |
| ipfs.family (ipfs on robinhood chain) | First 100 MB free, and the free tier is explicitly a 12-month pin ('Paid Free tier - 12 mo', 'Kept until Oct 8, 2027'). Per-GB payment on-chain after that. Two orders of magnitude short |
| ipums | Extract API returns 403 without a key and the product is pre-registered microdata extracts, not user uploads. No deposit path exists |
| iroh-dns-server (as a hosted third-party service) | The n0-computer/iroh-dns-server GitHub repo is archived (last push 2024-04-24) and carries no description. The functionality moved into the main iroh repo, and the maintained artefact is the |
| iroh-n0des (crate) | The old standalone rendezvous/discovery crate for 'p2p quic connections dialed by public key'. Superseded by the iroh 1.x address-lookup/pkarr path; repo README now just renders iroh-service |
| irys (ex-bundlr) | Permanent on-chain storage priced by the protocol in IRYS tokens; docs describe a fee market and price-stabilisation mechanism, not a free tier. Uploads require a funded wallet |
| jiocloud / jioaicloud | 50 GB free and 'Proudly made in India, securely stored in India', but the entire auth surface is an OTP sent to a phone ('OTP verification, Enter the OTP sent to you on'), i.e. an Indian-nu |
| jitpack | 250 MB repo cap; artifacts are derived and can be rebuilt/evicted, so it is a build service, not durable storage |
| jsdelivr as storage for release assets | The GitHub proxy only indexes git repo files. Release assets return 404, so the >2 GiB objects that make Releases interesting cannot be fronted by jsDelivr, they stay on GitHub's own Fastly |
| jsr (deno/typescript) | 20 MB per package tarball, 20 MB sum of all files, 20 MB per individual file; plus scope quotas (3 scopes/account, 100 packages/scope, 20 new packages/week). Quotas are raisable by email, bu |
| kaggle notebooks as a server | No inbound networking and no port exposure, Kaggle notebooks cannot listen for HTTP. The storage story (20 GB /kaggle/working + 200 GB datasets) is real, the CDN-origin story is not. Split |
| kakaotalk channel as a media host | Same inversion as Viber, image supplied as an external URL, no upload/store endpoint anywhere in the channel API |
| kartaview (openstreetcam, grab) | Read API is closed to unauthenticated clients: `GET /2.0/photo/?itemsPerPage=2` returns HTTP 200 with the body {"apiCode":400,"apiMessage":"Restricted access!"}, a 200 carrying an error, ex |
| kawaii (kawaii cloud) as a provider | Searches for a Kawaii cloud drive return only SEO guide sites (kawaii-cloud-guide.com, cloudplus-kawaii.com) and the unrelated hobby host NeoBox (128MiB max upload). No provider with a quota |
| kdrive (infomaniak) | THE textbook geo-fenced signup. The free offer is limited to a published 37-country list (CH, FR, BE, LU, DE, IT, AT, ES, PT, MC, AU, CA, CL, KR, DK, EE, US, FI, GR, HU, IE, IS, IL, JP, LV |
| kernel.org | Not evaluated as a storage option: it is the Linux kernel's own infrastructure, access by maintainer invitation only, and there is no general-purpose upload surface to test. Recorded so the |
| knb (knowledge network for biocomplexity) | 5 GB free per user, two orders of magnitude short |
| knowledgeowl | Advertises 'Unlimited file limits' and 200 MB per file, but every tier is 'Try it Free for 30 Days' followed by $100/month minimum. The unlimited claim is real; the free access is a trial |
| koofr lifetime (>1 tb) | The StackSocial lifetime SKU is 1 TB only, at $159.99-$199.99. No 5 TB or 10 TB lifetime SKU exists on StackSocial, and Koofr's own Crate tiers are subscription-only. So a 20 TB archive cann |
| koyeb, free starter plan | The free tier was withdrawn in the Mistral AI acquisition (Feb 17, 2026). Their own post: 'The Starter plan will soon be removed and new users will instead need to subscribe to the Pro, Scal |
| krakenfiles.com | Upload backend is unreachable: the uploader posts to https://hs6.krakencloud.net/_uploader/gallery/upload, which fails to connect on:443 (21 s). The front page returns a 1 GB limit banner |
| kts24, 1 tb storage vps free for 3 months (ceph beta) | Exactly the shape wanted (1 TB, 3 months, no card) but from March 2022 on a 'new ceph based storage vps series' that never launched publicly, the offer asked users to email a personal addr |
| kufile (kufile.com) | Domain is for sale on HugeDomains for $2,595. The service does not exist; any list naming KuFile as a Chinese host is at least a year stale |
| laion (laion-400m / 5b / re-laion-5b) | Read-only corpus publisher, not a host. laion.ai/data/ is a 404; everything is a link out to Hugging Face datasets (excluded as already known). No upload path, no account, no quota |
| lanzou cloud premium / (ilanzou.com) (`蓝奏云优享版`) | 10TB is a paid (CNY 88/yr) benefit on a separate account system; the free tier is 10GB on registration. Third-party 2026 price tables disagree on tiers, and ilanzou is a different login... |
| lenovo / lenovo nas share (`云盘`) | Lenovo Cloud Drive was device-locked: Lenovo's own KB says it can only be activated on specific models (XiaoXin Air 13/12, 510s) and only one Lenovo Cloud account per device. The OpenList dr |
| letbox storage kvm | Correct product, wrong availability and wrong price. The LA storage store shows every rung 'Out of Stock', and the 1 TB rung is $6.75 for 8 TB of transfer. Its '$2.50/TB' claim in the market |
| lex.st free 150 gb storage box | Below the 500 GB floor AND the domain is down, /, /storagebox/ and /storagebox/signup/ all return HTTP 530 (Cloudflare, origin unreachable). The LET thread is still the top hit for 'free st |
| liblibai (liblib.art) | Front-end loads but every model API path 404s anonymously: POST /api/www/model/list -> 200 with body {"code":500,"msg":""} (trailing 500-in-200), /api/www/model/getModelDownloadUrl |
| libp2p circuit-v2 public relays | Default relay limits are signalling-grade, not transport-grade: 128 KiB of data and 2 minutes per relayed connection. Fine for hole-punching, useless for bytes |
| library of congress / chronicling america / ndnp | Not a deposit surface for individuals. LoC acquires through NDNP state-partner awards and its own collections; there is no open upload endpoint, no account system, and no quota to consume. C |
| lightnode 'storage vps' line | Marketed as a storage product but every rung ships 50 GB of NVMe regardless of price. There is no big-disk SKU at all, the largest is 50 GB for $52.70/mo. Misses a 500 GB floor outright |
| linkbox (linkbox.to) | Has a genuine merged rclone backend (PR #7055, read+write, API token from /admin/account) but the free allowance is tens of GB and the API takes the auth token as a query parameter, a crede |
| linode / akamai cloud, managed container registry | No managed registry product exists. Akamai's own docs route users to self-hosting Harbor or running a private Docker registry on paid Compute + paid Object Storage; the cloud pricing page li |
| litterbox.catbox.moe (temporary) | Upload API is broken: POST to /resources/internals/api.php returns HTTP 500 (a full 69 KB HTML error page) for every time= value, with or without browser UA/Referer. The GET page renders ('T |
| loom / vidyard free tiers | Both cap by recording COUNT and clip LENGTH rather than bytes (Loom 25 videos x 5 min; Vidyard 5/month, 25-slot library). Ceiling is a few hundred MB per account, unreachable toward 500 GB w |
| lunaris cdn | Real service, real API (Bearer token, multipart, SHA-256 verified) but the free tier is 100 GB total / 5 GB per file, which is one-fifth of the filter and cannot be multiplied because it nee |
| magentacloud (deutsche telekom) | The whole product now redirects to a login page whose only identity path is 'Login with Telekom', a Telekom customer account. There is no standalone registration page (/register, /registrie |
| mail.bg | Signup collects a mandatory recovery phone (': *', marked required) plus gender and date of birth, and then does not activate automatically: ' |
| mail.com free (65 gb, but read-gated behind premium) | The 65 GB is real and the largest free mailbox found: "mail.com offers you up to 65 GB of email storage". But the read/write path is closed on the free tier: "these protocols [POP3, IMAP, SM |
| mail.ru '1 tb free' offer (historical) | The 1 TB giveaway is gone: current free volume is 8 GB and the 1 TB is an annual paid plan (1 560 RUB year one). Any 2013-2019 blog claiming 1 TB free is stale |
| makerworld (bambu lab) | Model files capped around 250-500 MB total per design and 150-200 MB per print profile; 3MF/STL pipeline only |
| mastodon /about/more as a limit source | The suggested read path no longer works: Mastodon 4.x serves /about/more as a client-rendered SPA, so the 'Upload limit' string is not in the HTML. Zero of 20 instances yielded an up |
| materials cloud archive | InvenioRDM node with a hard login wall before any upload; publishing is tied to a Materials Cloud workflow rather than open deposit |
| mattermost cloud free | The free cloud tier is deprecated - Mattermost now steers free users to self-hosted Entry. Self-hosted 'unlimited storage' just means the disk is bought, which is not free storage |
| maven central as bulk storage | Still no total-storage cap, but 2026 monthly per-organization publishing thresholds (~78 MB release size at p90, ~1.8 GB at p99) plus a commercial-nature gate from 2026-10-01 make sustained |
| maverick1983/google-drive-service-account 45 tb recipe... | The arithmetic (30 projects x 100 SAs x 15 GB = 45 TB) is no longer executable: service accounts report storageQuota limit '0' and every upload returns 403 storageQuotaExceeded. The repo's R |
| mcr (mcr.microsoft.com) | Microsoft's public registry is pull-only for anonymous users - nothing can be pushed, so it is not usable as storage. Kept here only to confirm it was checked |
| metered / xirsys / turnix free turn quotas | Recorded as a candidate above but they miss a 500 GB floor by two orders of magnitude: 20 GB, 500 MB and 10 GB per month against a 500 GB/day serving workload. Listed here so the relay s |
| microsoft 365 business basic/standard/premium (nonprofit... | 1 TB OneDrive per user but these are paid licenses; the nonprofit full free grant is gone (Business Premium grant ended, Microsoft deleted nonprofit tenants' data). 25 GB per license is the |
| microsoft 365 e5 developer sandbox | Cut from 1 TB/user to 10 GB/user OneDrive plus a 300 GB pooled tenant cap; setup now requires a linked Azure billing account that cannot be skipped. Eligibility needs a paid Visual Studio or ISV/ |
| microsoft 365 e5 developer subscription (the '25 x 1 tb'... | Widely cited as 25 TB. The current FAQ caps developer tenants at 300 GB pooled storage and 10 GB OneDrive per user, with the Developer SKU contributing 0 GB SharePoint in mixed tenants. Belo |
| microsoft mcr / registry.k8s.io (read-only public mirrors) | Anonymous pulls work (MCR returns 200 at /v2/), but both are read-only mirrors of vendor images, no push, no account, no writable namespace |
| microsoft mcr / registry.k8s.io / icr.io /... | All are read-only or reject auth-less writes. Probed anonymously: mcr.microsoft.com and registry.opensuse.org answer /v2/ with 200 but an anonymous POST blobs/uploads returns 411 (length req |
| minecraft realms | 10 GB of manual-save storage on Realms Plus, 5 GB on Realms Core, and both are paid subscriptions. One world per Realm |
| miro education / nonprofit plans | Education plan gives 'Unlimited active boards' but uploads are capped at 'maximum file size is 30 MB, maximum image resolution is 32 MP, maximum dimensions is 8192x4096'. Nonprofit is 'bette |
| misskey.io registration (as opposed to its capacity) | Its numbers are good (10 GiB, 500 MiB objects) but signup is closed indefinitely, the vendor states it cannot add server capacity because its cloud provider was breached. Capacity witho |
| misskey.social, 50 mb drive | Live and open, but driveCapacityMb=50 and maxFileSize=16 MB. Two orders of magnitude too small to matter; listed to show the family's low end and that 'Misskey' does not imply 'gigabytes' |
| mixdrop | Returns HTTP 410 Gone on the canonical domain, service withdrawn at this address. No limits page reachable |
| mopan (mopan) (`中国电信魔盘`) | Has a dedicated OpenList driver (`mopan`, reverse-engineered, with an explicit provider warning 'This network disk may store your password in clear text'), so it is technically mountable, b |
| morb0/tgbucket, two/telegram-fuse,... | Real projects but abandoned (tgbucket last pushed 2022-05-06, 8 stars). gh search repos 'telegram storage' returns 20+ repos with a median of ~10 stars, most unmaintained since 2022-2023. Th |
| morejust store (morejust.store) | kirillovmr/mjsChrome still links a Chrome Web Store listing for 'Free Unlimited Cloud Storage', but the vendor's own page says the org was closed and it is test-only: 'We were banned by Gi |
| multi-cloud manager guis (multcloud, and air cluster's... | They are transfer/copy schedulers between clouds, not capacity pools. MultCloud's own framing of the user request is telling, it answers 'how do I merge my cloud accounts' with a file-manag |
| mux | Pure pay-as-you-go across four meters (ingest/storage/delivery/encoding). No free storage allowance of any size; fails on cost before any storage question |
| mydevil.net (poland) | Advertised as a Polish hosting bargain with Transfer miesieczny bez limitu, but the plans are web-hosting SKUs (MD1-MD4: 25/50/100/200 GB SSD/NVMe), not per-TB storage. Prices render in GR |
| myminifactory | 100 MB/file for a plain Designer, 500 MB with a Store subscription; the 5 GB 'Archive Mode' is staff-granted (write-gated) and capped at 25 archives = 125 GB |
| n0 hosted blob pinning / storage service | Does not exist. n0 sells coordination (relays, metrics, diagnostics) and never bytes at rest. Checked the pricing table, the hosting page, the services dashboard, the org's 100-repo listing |
| nairr pilot (us) as a storage route | Twelve-month compute/model awards for AI research; eligibility is 'US-based researchers and educators from US-based institutions' with an institutional email, and the resource list is comput |
| nakama / heroic cloud storage engine | Storage objects are jsonb rows in Postgres, 'theoretically store up to 255 megabytes' but Heroic Labs explicitly advises against it ('we don't guarantee it will perform well at scale'). No |
| nara citizen archivist | Same shape as By the People: 'transcribe historical documents, tag archival photographs, or share comments'. Contribution is annotation to NARA's own records, not upload of new material. No |
| nasa veda data store (as a deposit target) | Ingestion is aimed at novel datasets produced by NASA Earth-science staff and at non-authoritative cloud-optimized versions of datasets from a DAAC; the process needs a veda-data pull req |
| natro xcloud / turhost (turkey) | Turkey's cloud-VPS market prices by RAM and vCPU with disk attached, never by the terabyte, and the per-TB cost of the disk included is not competitive: Natro XCloud Ultra+ is 4,933/mo di |
| neon | Read-only observatory API (verified live) serving instrument data from fixed sites. No ingest endpoint for outside data |
| netcup 'storage server' product line | The product page exists and advertises '1 GB storage space for less than 0.007 Euro per month including VAT, traffic and RAID level' (= ~EUR 7.17/TB) but publishes no plan table, no tier... |
| nextcloud one (nextcloud gmbh's own hosted service) | 30-day free trial with 10 GB and no backups during the trial; production starts at EUR 15/user/mo for 500 GB. Trial-only and then more expensive per TB than every reseller |
| nird data lake / data peak as a free tier (sigma2, norway) | Not free, this is the single most important correction in this dossier. The User Contribution Model v2.2 charges 470 NOK per TB/year for NIRD Data Lake and 800 NOK per TB/year for NIRD Data |
| no s3/s3-compatible endpoint at any of the three... | Probed for and did not find one: Hetzner publishes no S3 gateway for Storage Box (SFTP/rsync/WebDAV/SMB only), PulsedMedia exposes no object API (SFTP/rsync/WebDAV/HTTP), and Uloz.to is REST |
| nodeseek direct read (nodeseek.com) | Cloudflare/geo wall plus a hard IPv6 block: every fetch redirects to warning.nodeseek.com/ipv6-is-disabled and returns a 29-word apology page with HTTP 200, the exact 'status-code theatre' |
| notabug | DOWN, and down for exactly the reason this topic tracks. The homepage reads: 'Due to relentless AI scrapers notabug.org is currently down. We are attempting to come up with a solution to this problem. Currently |
| notion (free workspace as file store) | 5 MiB per file on Free (API and UI), and every Notion-hosted file URL is a signed S3 URL valid for one hour, 'Don't cache or statically reference these URLs'. Unlimited blocks on a single-o |
| now61.com (personal 95 gb / webdav pan) | A forum member's own server, 95 GB with 1 GB direct links, then a limited free-WebDAV round. Both threads are closed (''), and the vendor's own warning explains why: ' |
| nsf access / open storage network (as an individual route) | Round 2 recorded OSN as 1-50 TB via ACCESS. ACCESS has since tightened under NSF Important Notice No. 149 (2025-07-10): 'If you are based outside of the U.S., regardless of your institutiona |
| onedrive consumer 5 gb | 5 GB per Microsoft account, 2,000 accounts would be needed for 10 TB - not trivially repeatable, and no documented bulk-signup path |
| open heritage 3d (cyark + hes + usf) | Fully consortium-gated and mediated through Dropbox: 'Once the data is packaged it can be uploaded via a Dropbox request link assigned by the Open Heritage Alliance', with a DOI and a metada |
| open library | Not a file store: the only user upload is cover images capped at 30 MB, and bulk book import requires a privileged account via the JSON import API. Records point at Internet Archive items ra |
| opendal as a ready-made free-tier pool | Two separate misconceptions to kill. (1) `compfs` is not 'composed filesystem over services', its source is a `compio`-based local-filesystem backend. (2) RFC-7740 'Operator Composition' co |
| opendata.swiss | API and register both return 403 Forbidden (nginx) to the probe; the platform is operated by the Federal Statistical Office / cantonal offices and admits Swiss federal, cantonal and commun |
| opendoar v2 (v2.sherpa.ac.uk) | Jisc now blocks automated access at the edge. Returns a 'Jisc - Error 403 / Web page blocked' HTML page regardless of query parameters, including format=json. Not usable as a registry source |
| openml | Unreachable from this network, openml.org, www.openml.org, api.openml.org and docs.openml.org all timed out at TCP connect (21 s, 4 attempts incl. IPv4-forced, over ~ |
| openml (200 gb per dataset) | Could not be verified and is therefore NOT reported as a candidate, despite a promising number. Every attempt failed at the network layer: the API timed out (curl 28, port 443 |
| opentopography | No self-serve upload. The former upload page 404s after a site rebuild, and the service is a distribution portal for agency-supplied DEMs (its otCatalog API returns OTSDEM/OTLAS identifiers) |
| oracle cloud $300 / 30-day free trial | 30 days only, and it is a trap for this workload: during the trial unlimited data may be stored against credits, but 'If you are using more than the 20-GB limit when your Free Trial ends, al |
| osdn (osdn.net) | The SourceForge-Japan equivalent, would have been the obvious sibling candidate, is gone. DNS does not resolve (probe: Could not resolve host: osdn.net), read/fetch both 530, and the last |
| osf registrations (as a quota multiplier) | Registrations archive OSF Storage plus add-ons but are capped at 5 GB across all storage being registered, and Registrations can no longer be created from Projects after the transition. Not |
| oshi.at | Domain has been dropped and is now on a domain auction ('Bid on the domain oshi.at now / nicsell'). Also had an untrusted TLS chain (SEC_E_UNTRUSTED_ROOT). POST returns the auction page |
| outline | Cloud is trial-only: $10/mo minimum, and 'your first 30 days are free. Once this trial period elapses your knowledge base becomes read-only'. The only unlimited-storage route is self-hosting |
| outline (cloud) | No free cloud tier at all, 'your first 30 days are free. Once this trial period elapses your knowledge base becomes read-only until a payment method is added'. Trial, not free. Self-hosted |
| owncloud.online (saas) | Cheapest published plan is EUR 15/user/mo for 500 GB, roughly EUR 30/TB/mo, 7-12x the managed-Nextcloud resellers. ownCloud's own 'free' tiers are self-hosted only (Community Edition, unlim |
| pairdrop | WebRTC device-to-device only; the server is a signalling relay and only carries bytes as a TURN fallback. There is no object store, therefore no quota to multiply |
| pan.lm379.cn / cloud.lm379.cn, openlist, the index's #1... | The instance with the most prominent WebDAV advertisement in the index (public_dav:public) does not expose the AList API at all: /api/public/settings returns the SPA's index.html, not JSON |
| papers with code | Gone as an independent property, paperswithcode.com now 301s to huggingface.co/papers/trending. Even before the redirect it was a metadata index (papers, code links, leaderboard numbers), n |
| pastes.io | Free tier is 1 MB of text per paste and 100 MB total storage when signed in; Pro ($1.50/mo) is only 10 GB. Storage tier is smaller than a single 4K film |
| pcloud / koofr / icedrive / proton drive / mediafire /... | All six are wide-open on identity (email only, no card, no phone) and all six miss a 500 GB floor by 1-2 orders of magnitude: pCloud 10 GB, Koofr 10 GB (Briefcase plan, then 25 GB at EUR 0 |
| pcloud lifetime | Priced as a consumer photo product, not bulk storage: EUR 1499 for 10 TB = EUR 150/TB one-time, roughly 4x Drime's $36/TB lifetime and 15x Internxt's $10/TB. Encryption is a separate EUR... |
| peking university open research data platform... | A Harvard-Dataverse fork (' Dataverse ') with a real deposit flow, but the API and handbook both return 403 to a foreign registrant and the platform is aimed at PKU and Chinese resea |
| photobucket | The 2017 third-party-hosting ransom is over but the product is now 'Groupsy' and no longer a free image host: the free plan is signup-only, capped at 3 groups with 50-image limits, shows onl |
| pikpak share mounts as a capacity mechanism | Mounting someone else's share does not yield the bytes, OpenList records that share-mounted PikPak files play only 40-50% before cutting off, and the mount itself needs a username+passwo |
| pinata 402 / account-free ipfs | Not a free tier at all, it is x402 pay-per-upload with no account. Every upload is paid in crypto; nothing is free |
| pinecast, free (demo) plan | 48 MB per episode and only the ten most recent episodes per podcast stay available. Free forever with unlimited uploads, but the ten-episode visibility window makes it useless as storage. Pa |
| pixeldrain.com | Anonymous uploads are gone: PUT /api/file/{name} returns HTTP 401 authentication_required ('Please provide an API key in the password field of HTTP Basic Access Authentication'). The file AP |
| pixelfed flagship (pixelfed.social, pixelfed.art) | Both returned Cloudflare 521 (origin unreachable) on every probe. The software works and pixelfed.de/pixelfed.au answered normally, but the two biggest hosts were down, so |
| planetlab | No live service. The historical PlanetLab host lists are gone; successors are CloudLab/Emulab (both institution-gated) and OneLab. Nothing to allocate |
| planetscale | Free tier is GONE, confirmed on their own docs: 'PlanetScale does not offer a free plan, previously known as the "Developer" or "Hobby" plan.' Cheapest entry is a $5/month single-node Postgr |
| playstation plus cloud storage | 200 GB total (100 GB PS5 + 100 GB PS4, plus a 1,000-file cap on PS4 saves) and it is a paid subscription, not a free tier. No API, console UI only |
| polarbackup (precedent, not a candidate) | Named precedent worth knowing: a lifetime-deal cloud backup brand whose users report loss of data and service. Recorded only to calibrate how much to trust Blomp/ggdriive-styl |
| printful | 200 MB per print file, max 20,000x20,000 px, PNG/JPG only, and PDF is explicitly outside the accepted formats on every print method. The REST API is excellent and completely irrelevant, the file is an input |
| printify | JPEG/PNG up to 100 MB, SVG up to 20 MB. 413 Request Entity Too Large is the documented failure mode on the API |
| prism drive (alleged thunderdrive rebrand), $49 / 2 tb... | STILL BEING SOLD, DO NOT BUY. prismdrive.com/lifetime-pricing/ currently offers 2 TB for $49 one-time. Widely reported as a rebrand of ThunderDrive, which collapsed. User reports say it runs |
| profitdrive (claimed 999 tb free) | Site is down with a database error. The Korean roundup that reported '999TB free' itself warned it looked about to disappear |
| proton drive paid | Fails quota. Tiers top out where the workload starts: Drive Plus 200 GB, Proton Unlimited 500 GB + VPN. No 2 TB+ consumer SKU published, no lifetime plan, no WebDAV/rclone/S3 path that would m |
| prototype fund (germany) | Residency-gated rather than nationality-gated: 'Wohnsitz und steuerpflichtig in Deutschland' / 'You're a German resident, self-employed and paying German taxes. (German citizenship is not re |
| pub.dev (dart/flutter) | 'Keep package size within limits. We recommend less than 100 MB after gzip compression and less than 256 MB uncompressed.' Also 'Publishing is forever' (a permanence plus, but no delete mean |
| public baidu-pan / quark cookie pools and shared-account... | None of the candidate pools are a usable API. What exists is (a) forums and blogs trading-login QR automation (BaiduDisk-Qr-Login-Tenant-2.0, 'Cookie'), (b) paid '' acc |
| pumble free | 10 GB per workspace, hard stop, 'at the limit you must delete files before uploading more'. Confirmed here as a wall |
| quark/uc free-tier storage campaigns as a capacity plan | Checked and rejected as a plan rather than a provider: the 1 TB grants are 100-200 codes per campaign run, monthly, one per person. A lottery, not a repeatable unit |
| radar4kit (kit), 600 gb per dataset, but kit-members only | The best per-dataset number in the CERN-adjacent family, 600 GB per dataset, with WebDAV and a REST API for large uploads, but access is gated on a KIT/Shibboleth institution |
| radicle (+ public seed nodes) | P2P, no hosted storage quota to spend, capacity is whatever seeders choose to hold. Public nodes run restrictive policies; the team node lists a 'Restrictive' seeding policy and specific re |
| railway, volumes on the free plan | Free plan is a $1/month credit, and volumes are 0.5 GB on Free with 1 volume per project: 'Free and Trial plans: 0.5GB'. Volumes are a block device mounted into a container, not an HTTP-fetc |
| rapidseedbox | Cheapest plan $19/mo for 1.2 TB = ~$15.83/TB/mo, 5x the floor. Unlimited traffic but priced as a premium managed service |
| raysync | 7-day free trial only; paid tiers are where 'Unlimited' storage appears. No perpetual free capacity |
| rclone as a github client | No GitHub/Gist/Releases backend exists, verified by listing rclone's backend directory (alias, archive, azureblob, b2,... s3, sftp, webdav, yandex, zoho; nothing for github). Any GitHub-ba |
| rclone imap backend (the missing tooling) | The wrapper that would make this whole niche rclone-addressable does not exist yet. PR #9071 (2025-12-30) was closed unmerged; PR #9208 (2026-02-23) is still **open, merged=false**; issue #8 |
| recherche data gouv (france) | Deposit must go into the institutional space of the establishment a contributor belongs to; the 'generic space' exists only for French institutions lacking their own space. Dataverse 6.0 nod |
| redbubble | 300 MB cap, JPEG/PNG only, TIFF and PDF explicitly broken, and no retrieval path for the original; designs are resampled onto product templates |
| reddit as a file host | images and video only, there is no arbitrary-file attachment in the Reddit composer or API, so datasets cannot be stored at all regardless of the 20 MB figure |
| redis cloud (redis.io) | Free tier is 30 MB single DB, three orders of magnitude below the 500 GB bar, one database per account, no multiplication path |
| render, persistent disks and free web services | Persistent disks are paid-only: 'You can attach a persistent disk to a paid Render web service'. Free web services have an ephemeral filesystem, 'any changes to your web service's filesyste |
| researchgate, data upload as storage | Not a data repository and never was. Per-file limits are tiny and the platform is a publication-profile site: forum answers document an 80 MB document cap and a 512 MB video cap, and their o |
| reshare / uk data service | Submissions are tied to ESRC grant holders and UK Data Service registration; grant metadata is pulled from UKRI Gateway to Research, so the deposit is anchored to a funded project |
| retelit object storage | Not an independent provider, it is Wasabi's Milan region rebranded and resold (Wasabi case study + press release about the Milan region). No public price page; enterprise quote only. Anythi |
| revolt/stoat public instance as bulk storage | 20 MB per file with no paid tier and no public way to raise it. The public instance adds a human-verification step at signup. 1 TiB = 52,000 files. Only self-hosting removes the cap, which is no longer free |
| ring (amazon) camera cloud | Recordings are retrievable by a reverse-engineered API (python-ring-doorbell, ringdownloader, KoenZomers/RingRecordingDownload), but the write side is camera-only: the surface is history() + |
| ringcentral team messaging | Seat-licensed UCaaS with a trial, not a free tier; auth-only reads; no published storage allowance |
| roboflow (free tier) | Datasets are 'Uncapped; On-demand' in size, which looks like a win, but the free tier meters storage through a credit system (10 credits/month) and every operation, storage, labelling, trai |
| rodare (hzdr), 100 gb/dataset, institution-scoped | 50 GB per file and 100 GB per dataset is a genuinely useful number and above Zenodo's default, but it is HZDR's repository for HZDR research output, and the site explicitly caps ambition ('P |
| runpod network volumes | Correct architecture, wrong economics: network volumes are $0.07/GB/mo for the first 1 TB ($0.05 beyond), i.e. ~$72/TB/mo, and there is no free allowance. An account at $0 balance has its vo |
| sa->my-drive-shared-folder 16 gb ceiling (common... | Sharing a My Drive folder with a service account does not give it the owner's quota; uploads fail at 16,106,127,360 bytes with storageQuotaExceeded regardless of maxUploadSize. Many tutorial |
| sakura vps nfs (jp) | CNY 26,400/mo for 3,200 GB = CNY 8.25/GB = $52.25/TB. The most expensive per-TB option checked in this lane. Japanese-only signup and billing |
| samsung cloud, amazon drive, ionos free tiers | All three abandoned free cloud storage within the last five years. Amazon Drive was retired outright; Samsung Cloud was folded into OneDrive; IONOS dropped its free tier. Listed here so nobo |
| sbercloud / cloud.ru free tier, selectel free tier | Both are commercial IaaS with no meaningful perpetual free object storage. Cloud.ru's /free page returned nothing extractable and Selectel is a paid-from-zero provider; SberDisk (the consume |
| sbercloud / sberdisk | SberCloud was rebranded into Cloud.ru (docs.sbercloud.ru now serves Cloud.ru Evolution docs), so it is the same 15 GB free tier, not a second provider. The consumer SberDisk is 15 GB free, w |
| sberdisk / gitverse (sber) | Both authenticate through Sber ID, which is phone+SMS ('... QR- '), and GitVerse's own sign-in endpoint answers 401 |
| scielo data (data.scielo.org) | Bunny Shield challenge on every route including the API; dataset was not reachable |
| scienceopen | Challenge-walled for every non-browser tool: read.web returned 'deadline... after it moved on for `challenge`' with all providers failing, and /faq is a 404. ScienceOpen is a publishing/pee |
| sdisk / sdpan (zhenghaof/flash-disk-object-storage)... | A '' (use SDisk as free object storage) wrapper that '20'. The service endpoint is gone: sdpan.zhfblog.top returns 530 through the proxy, and the repo directs users |
| seaart (seaart.ai) | Model metadata is readable anonymously (POST /api/v1/model/detail returns a full JSON object with model_ver_info_v2, file_id, hashs) but there is no anonymous file download: /api/v1/model/do |
| seafile official cloud (seacloud.cc) | Registration closed. Trial plan is 1 GB for at most 3 users; Team Plan USD 8/user/mo starts at 3 users for 500 GB. No free path and no self-serve path at all, a referral takes an email to the vendor |
| seedbox.ch trialbox | 48-hour trial, 15 GB: 'Try a real managed seedbox free for 48 hours, no credit card. 15 GB'. Fails on both capacity and duration |
| seeweb cloud object storage | EUR 27.00/TB/month for the base 1 TB with 1 TB outbound included, and extra traffic is EUR 11.50/TB, 6.8x Datalix for the same bytes. Italian enterprise positioning, not a price competitor |
| send.skylerszijjarto.com (250 gib/file) | The single most generous row in the public Send-instance table, 250 GiB per file, 7 days, 10,000 downloads, returned Cloudflare 530 when probed. The biggest quotas in that table are the le |
| sendblob.app | Browser-to-browser is not actually P2P today: 'Browsers cannot open direct QUIC/TCP connections, so traffic is relayed through public iroh relays... no relay, no transfer.' Uses a per-tab O |
| serverius eurostack, 'free 1 tb for a EUR 1 setup fee' | A 2021 LET thread that never resolved into a usable service: commenters could not register ('cant seem to register here.. any luck so far?'), flagged it as 'not a trial but their smallest pl |
| shade (shade.inc) | Enterprise 'AI cloud NAS' at $29.75-35 per seat/month for 500 GB active storage per seat. Has both a native rclone backend and an S3 API at s3.shade.inc, so technically excellent, but per-s |
| shakker ai (shakker.ai) | Site is broken and behind an automated-traffic filter for reads: GET www.shakker.ai/models -> 500 Internal Server Error with x-robots-tag: noindex; /modelinfo/1 -> 500. Wayback capture 2026-05-13 renders only a model c |
| sharefile (progress) | 14-day trial only. Paid plans start at $16.50/user/month with a 3-user minimum and 1 TB of account storage per license, enterprise-sized, not free |
| sharefile storage model | Storage is sold as 3 TB account blocks plus $ per TB packs; there is no free byte anywhere in the product |
| sharepoint embedded | Unlimited containers but every byte and every API call is metered against an Azure subscription. Zero free allotment |
| sharkey.world, 100 mb drive | Live, open, 250 MiB objects, but only 100 MB of drive per user. Seven uploads exhaust it |
| shutterfly | 'Unlimited' photo storage, but it is conditioned on a purchase at least once every 18 months and is web/app-only with no API, WebDAV or rclone backend, fails both the free filter and the pr |
| signiant media shuttle | Free trial only; pricing is quote-based per-portal. No self-serve free tier. (Search results confirmed only /try-signiant-free/ and pricing-packaging pages, no free plan.) |
| simplecast / transistor / captivate / libsyn, unlimited... | All four advertise genuinely unlimited (!) audio storage or uploads, and Transistor and Captivate even leave a properly made MP3 untouched on the way through, the right behaviour, on the wr |
| sketchfab | 100 MB per model on Basic (50 MB per the features page); 10 uploads/month although downloadable models do not count. Ingest is a 3D mesh+texture pipeline, so arbitrary files do not survive a |
| skybox (1024skybox.com) / jollify | Both advertise '1 TB free'. SkyBox's landing page is a mockup of a non-existent product ('12M+ Happy Users', a fabricated dashboard screenshot showing '640 GB used of 1 TB') with no pricing, no API, no d |
| slab | Free plan caps attachments at 10 MB and the API (the only programmatic route) is 'only available to customers on the Business or Enterprise plan'. 10 MB x 90-day version history is not a sto |
| slack/discord-as-storage wrapper ecosystem (slackfs,... | These repos all solve the wrong problem: they archive, clean up or mount Slack - none of them removes the 5 GB cap or the 1-year deletion. slackfs is a FUSE view over channels (6 stars); fil |
| small institutional inveniordm instances (tu wien, kth,... | Every one I probed publishes no numeric per-record quota, hosts no large objects, and is sized for text/metadata rather than bulk data. Record counts are in the tens-to-hundreds (KTH 58, Tal |
| smithsonian open access / 3d.si.edu | Read-only. The Open Access corpus (2.8M 2D images + ~2,346 3D assets as of the FAQ) is downloadable and CC0, but there is no contributor upload path at all, the 3D API is described as 'vers |
| snowflake trial ($400 / 30 days) | Thirty days then suspension. Storage is billed from the credit balance, so $400 buys a few TB-months at most and then the account is suspended rather than downgraded. Trial, not free tier |
| society6 | 150 MB limit, JPG/PNG only, print-resolution pipeline |
| softpedia / majorgeeks / filehorse / snapfiles / lo4d /... | This whole sub-class is a mirage. None of them is a storage provider: they are catalogues that either link out to the vendor or proxy a vendor URL. Softpedia's submission path is a PAD-file/ |
| software heritage deposit (swh-deposit, the push api) | Upload capped at 100 MiB documented / 200 MiB default in config, and requires HTTP Basic auth - anonymous POST to deposit.softwareheritage.org/1/<collection>/ returns 401. Only useful for so |
| solcloud (solana p2p) | Landing page only; storage is explicitly paid per-upload in SOL ('Pay small fees in SOL tokens to store your memories'). No free quota stated anywhere on the page |
| sonatype nexus repository cloud (hosted) | Hosted Nexus is a paid, sales-led deployment: 'Contact the Sonatype sales team for the right deployment option'. No free hosted tier exists, only the self-hosted Community Edition is free |
| sourcehut (sr.ht) | No published quota, but the resource guidance is 'aim to have repos no larger than the Linux kernel git repo, which is 6 GiB' and 'Don't store lots of large binary objects'. Payment is expec |
| sourcehut (sr.ht) git | No Git LFS support at all, the project's own guidance is 'aim to have repos no larger than the Linux kernel git repo, which is 6 GiB' and 'Don't store lots of large binary objects in your r |
| spice.ai, see candidate entry (fails-quota) | The free tier is an Apache-2.0 runtime that is self-hosted. There are no free hosted bytes; the 'free datasets' are Spice's own samples, read-only |
| statically (cdn.statically.io) | Silently truncates every response. HTTP 200 with a correct Content-Length header for the *full* object but a body cut at 16,384 / 31,232 / 65,536 bytes depending on the path, and for some pa |
| steam friends chat file transfer | ~30 MB per file ceiling reported in the Steam Client Beta forum; P2P-ish, no public link, no API. Useless as storage |
| steam workshop | Hard ceiling far below the unit size, plus a paid gate: uploads need a Steamworks partner app ($100 Steam Direct fee per product) and the ISteamUGC API is a C++ SDK, not HTTP. Pract |
| stock rclone telegram backend | Does not exist. rclone's own tracker has the request closed unimplemented (issue #6975, 'Telegram Backend'; issue #5829 '[backend] add Telegram'). The only working rclone path is the Teldriv |
| storadera | EUR 7.95/TB/mo with a hard fair-use rule that equals the storage: 'The allowed download amount equals to your stored amount.' That is 1x storage/month, i.e. precisely the 1:1 ratio that... |
| storyblok (starter free) | Free space caps at 2,000 assets and 100 GB traffic/month with no additional traffic purchasable on Starter. 2,000 x 500 MB max is a theoretical 1 TB but the 2,000-asset count is the hard wal |
| strato hidrive as a recurring free-1tb play | The February Valentine's promo is real and recurs annually, but it has already been consumed and it is a one-shot trial, not a channel. The 2026 window opened ~Feb 3 and closed 2026-02-15 (B |
| stream chat free plan as bulk storage | Fair-usage storage ceiling with per-GB overage; converting free into an invoice is a fail, not a qualification |
| streamlit community cloud as storage | Listed as a candidate for the serving angle only. The 50 GB 'storage' maximum is the container's disk ceiling, not an allocation: files written at runtime are lost on reboot and apps sleep |
| surge.sh as a bulk archive (naive) | 450 MB / 10,100 files per project and every publish is a full gzipped-tarball replace, so a 450 MB project costs 450 MB of upload per change. Only viable if projects are written once and sha |
| tableland, see candidate entry (fails-quota) | 500k rows / 24 columns per table. Their own docs say to put large media on IPFS and store the CID. A pointer store cannot hold 500 GB |
| telepedia | 15 MB per file (live siteinfo) and the media CDN is 403 to everything: `static.telepedia.net/metawiki/1/18/favicon.ico` returns 403 both direct and through the fetch proxy. Upload-open / rea |
| telethon and pyrogram as the client stack | Both upstream libraries are ARCHIVED, Telethon read-only since 2026-02-21, Pyrogram since 2024-12-23. Patch-level breakage will not be fixed. Build on TDLib or MadelineProto, or accept Teld |
| tencent edgeone free plan / edgeone makers (pages) as... | Two separate failures. (a) The EdgeOne **Free Plan** is advertised as 'Unmetered Security Traffic' but its own guide puts the use case outside the allocation: it 'does not support video delivery or large-file d |
| tensorart | Behind an automated-traffic filter beyond use: tensor.art/ returns 403 with the extraction flagging paywall:status, /models likewise, /upload returns 422. Its landing page claims 'model hosting' but no limits page |
| tensorart (tensor.art) | Model files are not anonymously retrievable and the model page itself sits behind an automated-traffic filter: GET tensor.art/models/<id> -> 403 Forbidden; api.tensor.art returns HTTP 405 with a JSON body {"code":200 |
| terabox (kr/id/jp localisation) | Same 1 TB as everywhere else, and the localised pages are the interesting part: the /indonesian URL now redirects to /simple-verify with a 'Verification code was entered incorrectly' stub, a |
| terabox official rclone backend | Still not merged upstream: PR #8508 has been open since 2025-04-13 (last update 2026-09-09). Anyone planning on `rclone config` + terabox must ship a fork instead |
| the good cloud / hosting.de / hosting.fr / arkdisk /... | Every one of them tops out at 1-8 GB free. hosting.de and hosting.fr both have a 'Free 1 GB' tier and then jump to 100 GB at EUR 4.90/mo. The Good Cloud is 2 GB free with 1 TB at EUR 20/mo ( |
| the.hosting (ex-pq.hosting) storage vps | Flexible-capacity storage at 'EUR 0.04 per 1 GB' = EUR 40/TB = $44.94/TB/mo. Ten to twenty times the floor. This is where the PQ Hosting lead actually lands, the EUR 0.03/GB figure... |
| thingiverse | No published limit but uploads stall/fail on large files with no progress indicator, unreliable rather than capped |
| thunderdrive | Collapsed, and its customer base was reportedly migrated/rebranded into Prism Drive. Documented as a deceptive offer, with lost data and no support |
| timeweb cloud s3 (russia) | The 'Unlimited' storage tier is 639 /mo and immediately reveals itself: 250., 4 /, 250 GB included, then 4/GB, so 'unlimited' costs 4,096 per TB on |
| transferrocket | Free is 5 GB transfer AND 7 days storage, both as hard pay-per-use boundaries ('Transfers up to 5 GB are free', 'Transfers up to 7 days are free'), the product is metered from the first byt |
| tresorit | Fails quota at the individual tier and the price is an order of magnitude above the lane. Personal Lite is 50 GB with a 2 GB max file size and 2 GB link sharing, under the 500 GB floor. Bus |
| trove (national library of australia) | Anubis proof-of-work wall on /about/contribute, and structurally Trove is a discovery layer over member-collection metadata plus newspaper OCR, not an upload target for third-party bulk dat |
| tuxis | Sells VPS and private cloud, storage priced per GB of SSD as an add-on to compute: from EUR 13/mo for 20 GB. No per-TB bulk storage product exists to compare |
| tuya / smart life video cloud storage | Real object storage behind it and a documented developer API ('Video Cloud Storage' in the Cloud Services API Reference), but it is sold per device and the API returns device event recording |
| twilio gratis turn (the '20-25 gb free' claim) | No free TURN allowance exists on Network Traversal Service; TURN is $0.40-0.80/GB from byte one. The free figure traces to Twilio Video WebRTC Go, a retired 2020 product. Only STUN is free |
| uk ai research resource (airr / isambard-ai, dawn) | Compute-only calls and the applicant must be a UKRI-eligible organisation. Storage is never the allocation unit |
| ukr.net mail | Fixed-country dial code on the registration form: the phone field is pre-set to '+380' with the note ' ' (we will send a confirmation code to this n |
| uloz.to free tier | The rclone forum's canonical 'free drive' lost its appeal: free storage cut from 20 GB to ~1 GB (needs a bank card). Tracked as a live migration event by rclone users, not a provider |
| unity asset manager org storage (unity personal) | Explicitly a hard cap: 'The plan has a non-extensible cap of 10 GB of storage... At any given time, the total size of the assets that are currently stored in Unity Cloud can't exceed the li |
| unity cloud save (the cloud save product, not ccd) | 5 GiB/month stored on the free tier, with 1M writes and 1M reads per month. Two orders of magnitude under the 500 GB bar before any chaining |
| university alumni accounts as a storage class | The alumni-account route collapsed in 2024. Northeastern: 'Northeastern will discontinue providing alumni with storage on the University's Google Drive after October 1, 2024... alumni will |
| uploadcare | Free plan is 10 GB storage / 25 GB traffic / 5,000 operations per month, 1 GB max file, 'Personal use only', two orders of magnitude short on all three axes, and operations are consumed per |
| usgs / noaa ncei | Both are read-only public data services (verified live: waterservices.usgs.gov returns real JSON). NOAA's NCEI 'data' endpoints 301-redirect to AWS Open Data buckets. No user deposit, so irr |
| val town, blob storage | Blob storage counts against total Val Town storage, which is tiny: 'Blob-stored data counts towards your total Val Town storage - 10mb on the free plan and 1gb on pro.' Three orders of magni |
| vc subsidy / loss-leader venture money | None of the seven has institutional funding. pixeldrain is one person plus Patreon; catbox is 'Catbox LLC... it's just me!'; gofile is a SASU ('simplified joint-stock company with a single s |
| vercel blob | Hobby includes 1 GB/month blob storage and 10 GB data transfer, then regional metered pricing. 1 GB per account is 3 orders of magnitude below the bar and the overage is per-GB paid |
| vercel edge config / global config | Renamed to Global Config, and the Free limits are absurd for storage: 'Maximum store size / 1 MB' and 'Maximum number of stores (total) / 1' on Hobby. One megabyte. This is a feature-flag st |
| verypan (yun.verypan.com) | Advertises unlimited storage (' ') but caps a single file at 500 MB and requires (real-name identity verification) to upload at all. 500 MB x unlimited is a 40,000-object TiB |
| viber business as a media host | Inverted API: Viber consumes a public image URL, it never produces one. 1-3 MB cap on the file |
| virmach storage / cloud storage | Cheap headline ($3/mo for 250 GB) that inverts at scale: $10/TB at 500 GB, and the STORAGE-1T rung on the live page shows 'OR $4.80 PER YEAR', which is a clear page bug rather than a price |
| vk cloud 'memory' style consumer storage ( etc.) | Consumer phone-backup subscriptions: 8 GB free, then 60-500 RUB/mo for 80 GB-1.5 TB. Paid, small, and app-only |
| vultr object storage | Price page is 403 to the read broker and the docs path 404s; only the marketing shell is retrievable. No price may be quoted from a page that could not be opened |
| walrus mainnet (public upload) | No keyless publisher exists and none is planned: 'Walrus has no public unauthenticated publisher on Mainnet. There are no plans to create one.' Every store spends WAL + SUI, and 'There is no |
| wayback cdx server as storage | It is an index over captures, not a blob store. Useful only as a free listing/manifest source for items already uploaded (1.7s-38s per query in probes) |
| wayback replay as a general bulk store (upload-by-url) | Only what a URL already serves can be captured, so it is a second copy, not primary storage; and item-file URLs under archive.org/download/<item>/<file> are not crawlable through the replay |
| web werks (in) | Checked, and it publishes no pricing at all. The storage page is enterprise marketing prose with no SKU, no rate card and no order path, a quote-only enterprise colo/sto |
| webtorrent / webtorrent-hybrid seeding | No host, no quota, no persistence, capacity equals 'whatever one seeder with a live connection chooses to serve', and browser peers cannot reach a seeder behind NAT without a TURN/relay cos |
| wekeo (copernicus dias) free tier | Free account gives 'up to 20 GB of storage in your home directory' on JupyterHub. The larger Innovation Lab tier is a competitive call, not a quota |
| wekeo drive (copernicus dias file hosting) | 8 GB of free space - three orders of magnitude short of the 500 GB floor, and it is a file-sharing front end for notebooks rather than object storage |
| wellcome trust, alfred p. sloan, gordon and betty moore,... | All four fund organisations, not people. Wellcome pays 'large-scale data storage' only as a service charge on a grant held by an administering organisation. Sloan states plainly 'The Foundat |
| wenshushu / (`文叔叔`) | Every API surface rejects an unauthenticated caller with the same token error, and there is no anonymous share-read entry point. The promise is real but unreachable without a session |
| whatsapp cloud api media as archive | 30-day hard deletion plus 5-minute media URLs; the bytes are unrecoverable on day 31. Any 'WhatsApp as free storage' claim found in the wild is wrong about this |
| wisemodel (wisemodel.cn) | Reads are Chinese-market and mostly login-gated for the interesting parts: /models -> 200, but every model detail page I opened returned 504 through the reader (2 attempts), the git LFS ref |
| wistia free | Free plan has a fixed storage allowance that cannot be exceeded ('Free plans do not have the ability to purchase additional storage, and cannot exceed the included storage amount') plus a |
| wolkli | Swiss Nextcloud host with a 1 GB free tier (Level C1 'FREE'); the next step up is 10 GB for CHF 60/year, so there is no free path anywhere near 500 GB |
| wolkli (ch) | Free 'Level C1' is 1 GB; next step is 10 GB for CHF 60/yr. Never had a path near 500 GB on the free tier |
| wyze cam plus / cloud 60 | 14-day rolling event storage standard, 60 days as a paid add-on, unlimited cameras on the Unlimited plan. All of it is event-triggered clips from Wyze hardware; no upload API |
| x02.me | Free plan is 5 GB with 200 MB/file (80 MB anonymous) and 250 uploads/day. Clean REST API and an MCP server, unlimited free accounts, but 5 GB units and a 200 MB file ceiling make it irreleva |
| xeno-canto (bird sound archive) | Both the API and every documentation page sit behind an Anubis proof-of-work wall. `/api/3/recordings` without a key returns 401 asking for a `key` parameter, and /explore/api + /about/uploa |
| xirsys free turn | 500 MB/month, single region after 30 days. 16 MB/day, a sandbox, not a transport |
| xirvik | Entry shared plan is $14.95 for ~100 GB HDD, roughly $150/TB/mo. Team tier $124.95 for 4 TB ($31/TB). Nowhere near the floor despite 'unlimited traffic' |
| yandex cloud object storage free tier | Only 1 GB of standard storage, 10 000 PUT and 100 000 GET per month free, two orders of magnitude below the filter, and the initial grant is a time-boxed trial |
| yandex disk / yandex photos | 5 GB free. The 'unlimited' photo auto-upload is gated behind Yandex 360 paid plans and is not available on free |
| yumpu | Free plan is 3 uploads total (not per day) with 600 MB per PDF; the free tier is a demo of a paid publishing product, and every plan and FAQ page tried returned 404 or 422 |
| zalo cloud (cloud.zalo.me) | DNS does not resolve. Zalo's cloud offering exists only as 'Zalo Business Solutions' (zalo.solutions), an enterprise customer-service platform, there is no consumer storage product to evalu |
| zazzle | Uploads fail above ~3-4 MB in practice with no error message; 'no limits to the number of images' but each is tiny |
| zenodo | Deliberately not assessed here. Referenced once only because OSF's own comparison table cites '1TB free on Harvard Dataverse' as an add-on figure |
| zhipu bigmodel files | Batch purpose capped at 100 MB/file and 1,000 files; file-extract capped at 50 MB. Content download only supported for `batch` type. Well below the floor |
| zilliz cloud / milvus (free tier) | The free tier is denominated in Capacity Units (compute), not bytes, and the product stores embeddings rather than arbitrary objects. No blob/object API, no anonymous download, so it fails t |
| zoho workplace free edition | The free edition's WorkDrive team-storage number could not be pinned down on the pricing page (the 100 GB / 10 GB-per-user figures are the paid tiers). Not reportable as a quota without a li |
| zoolz lifetime | No lifetime product survives on the pricing page. zoolz.com/pricing/ now shows only Monthly/Yearly toggles with a '30% Off Yearly Plans' banner, no one-time option. Zoolz's historical lifet |
| zerotier free as a storage mesh | Cut to 10 devices / 1 network, non-commercial, and the self-hostable controller was removed from the default open-source build. Cannot host a shard farm |
| bittorrent / webtorrent seeding (self-hosted) | Same structural failure as Hypercore: no host, no quota, no persistence guarantee. WebTorrent needs an active seeder and browser peers; a torrent with no seeder is a 0-byte download. F |
| btfs (bittorrent file system) (self-hosted) | It is a host-side staking scheme, not a consumer storage tier: hosts must stake in 500,000 BTT units, redeem only after 90 days, and are penalised 10,000 BTT per failed validation. Docs host |
| earnapp (bright data) (self-hosted) | Dropped per-GB pay on 20 Aug 2025 and now pays per hour of active use, capped at $10/month per US IP and $5 elsewhere - a hard ceiling that makes it useless as a scale path in either directi |
| earthstar (self-hosted) | A specification plus JS library for local-first apps; explicitly self-hosted and serverless. 'Always self-hosted. Servers optional.' There is no provider, so no free quota to obtain, it is |
| git-annex bup / ddar special remotes (self-hosted) | Both dedupe into a repository that must be self-hosted, and both need full shell access (bup: 'git-annex-shell does not support bup... you need full shell access to the server'). No hosted fre |
| gnunet fs as a storage provider (self-hosted) | Files are addressed by hash onto a DHT with no hosting guarantee, retrievability requires live peers holding the blocks, and the local QUOTA setting governs only the local datastore. docs.gn |
| honeygain (as an egress source) (self-hosted) | Supply-side only; no buyer-facing proxy endpoint. Pays $0.10/GB (10 GB = $1) with a $20 payout minimum, and its own published usage example implies 50-67 GB/month across three separate netwo |
| horizonpush (lupuszr/horizon) (self-hosted) | Self-described 'Experimental & Work in Progress... Expect breaking changes, incomplete features, and evolving APIs'. It is a thin iroh-blobs front end whose cold path falls through to AWS S |
| hypercore / dat / holepunch (self-hosted) | P2P replication primitives, not a host. Holepunch ships Hypercore and the Keet app; data lives on peers' disks with no pinning service, no HTTP gateway, and no quota. Serving 500 GB/day woul |
| juicefs community edition as an n-bucket pool (self-hosted) | A single JuiceFS volume binds to exactly ONE object-storage endpoint; multi-bucket/multi-provider backend has been an open feature request since 2021-04-23 and is still open with no implemen |
| kohakuhub (hub.kohaku-lab.org) (self-hosted) | Self-hosted SOFTWARE, not a service, 'a self-hosted, open-source alternative to HuggingFace Hub... Keep your models and datasets on your own infrastructure'. It is the fastest-growing patt |
| lis (riffcc/lis) (self-hosted) | FUSE filesystem over iroh described as 'Life is short, but data should live forever', exactly the shape wanted, but the README exposes only put/list/get/mount with a read-only FUSE mount, n |
| matrixhub (matrixhub.ai) (self-hosted) | Same class, explicitly so: 'an open-source, self-hosted AI model registry... a drop-in private replacement for Hugging Face, purpose-built to accelerate vLLM and SGLang workloads'. Its head |
| minio gateway (s3/gcs/azure/hdfs) as a pooling layer (self-hosted) | Removed, not merely deprecated: 'MinIO Gateway will be removed by June 1st, 2022 from the MinIO repository'. There is a documented migration path away from it, and the entire minio/minio rep |
| pawns.app / traffmonetizer / repocket (self-hosted) | None of the three publishes a consumer pay rate on any public page - the rate is only visible inside the dashboard after signing up, so no bottom-up arithmetic is possible and none of them s |
| peer2profit (self-hosted) | Official site unreachable (connection closed, twice, on 2 Oct 2026). Third-party research places it at $0.28/GB for consumer-connection traffic feeding AstroProxy at $7.60/GB, but nothing about it can be verifi |
| rocket.chat starter / community (self-hosted) | Both free tiers are self-managed/self-hosted: the deployment supplies the storage. Cloud Starter is a 30-day trial, not a free tier. No free hosted storage |
| seaweedfs cloud tier as an n-free-provider pool (self-hosted) | Cloud Tier moves *whole 1 GB volume.dat files* to ONE configured remote provider; it is a hot/warm tiering mechanism, and the chunk files it writes 'are not usable outside of SeaweedFS'. Th |
| self-hosted gitea/forgejo as a route around the quota | Gitea and Forgejo default every package limit to -1 (no limit): LIMIT_TOTAL_OWNER_SIZE -1, LIMIT_SIZE_GENERIC -1, LIMIT_SIZE_CONTAINER -1; Forgejo quota.ENABLED defaults false and quota.defa |
| the 'self-hosted hf clone' search class itself (github:... | A whole class worth flagging so nobody re-searches it: GitHub repo search for 'model hub self-hosted' / 'huggingface alternative' returns almost exclusively self-hostable servers (hangar-hub |
| uppy companion (self-hosted) | Not a provider, it is a self-hosted OAuth bridge that pulls files from the user's own Drive/Dropbox/Instagram into the upload target. Zero storage of its own, so it cannot be multiplied; i |
| zulip self-hosted free / community | Self-hosted means the disk is paid for by the deployment. The only interesting artifact is the S3 upload backend, which points at a bucket already paid for |
| registrish (jpetazzo) and static-container-registry (self-hosted) | Not a provider, a mechanism for serving a read-only registry off static hosting. Interesting as an amplifier (point it at a free static host to get registry-shaped URLs), but it stores nothing |
| hyperswarm / hyperdht blind relay as free bulk... (self-hosted) | Blind relay exists, any willing peer forwards ciphertext when both sides are behind randomized NAT, but there is no operated free relay fleet to draw on; `relayThrough` is supplied by the caller |
| herihericloud (againsturb/herihericloud) (self-hosted) | Marketed as ' + WebDAV' and it is a genuinely good client, but its substrate is (classic Lanzou), already recorded in this topic. It adds WebDAV/MCP/OpenWRT surface to a known provider, not |
| clouder (oleksandrshabaldas/clouder) and the... (self-hosted) | A clean, well-tested Windows app ('107 tests') that pools 'Google Drive and MEGA today' into one 45 GB folder. Names only already-researched providers and adds no new tier, the multiplier i |

## What this page does not do

It does not resolve the 37 collisions, the 95 providers whose quota text differs between two rows, or the 59 whose verdict differs. Those are `conflicts[]` entries on the records, and `gaps.md` lists the ones that are still open.

It does not say a provider is permanently dead. `dead_end.retry_when` on each record names what would reopen the route, and for the twelve recorded as unreachable from this environment that value is "from a host that can reach it" rather than "never".
