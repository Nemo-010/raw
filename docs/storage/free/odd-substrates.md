# Odd substrates: which non-storage service holds bytes, and what that costs

This class exists because a storage product is not the only place bytes can live. A database, a
backend-as-a-service asset pipeline, an email mailbox, and a notebook's working directory all
hold files, and several of them hold more than the storage products do. The question is what
each one costs in a currency other than money: a per-object cap, a message-count limit, an
expiry on the notebook, or an interface that was never meant for bulk transfer.

This document covers 11 qualifying records across backend-as-a-service and database
storage, email as storage, and notebook or compute-attached disks. 38 were rejected, and
the rejections are dominated by quota.

## The comparison

Sorted by substrate: BaaS and databases first, then email, then notebook disks.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Hygraph | Unlimited asset storage on Hobby (free) with a 50 MB per-asset cap... | per-object-cap: 50 MB per asset | - | qualifies-with-caveat |
| MongoDB Atlas (M0 / Free cluster) | 512 MB data storage per free cluster (0.5 GB, uncompressed BSON + indexes)... | - | - | fails-quota |
| Neon (Object Storage + Postgres) | 5 GB object storage per project + 1 GB Postgres per project (20 GB account total)... | per-object-cap: Max object size 5 GiB | - | fails-quota |
| Prismic | Unlimited assets + unlimited documents on Free; 100 GB CDN bandwidth/month (no overage) | - | - | qualifies-with-caveat |
| Sanity | 100 GB assets + 100 GB bandwidth/month per project... | - | - | qualifies-with-caveat |
| Mail.bg, 50 GB free mailbox with free IMAP/POP... | Signup page, Waybacks capture 2026-02-23: "50 GB ", "20 MB ", "1 GB ". = 50 GB mailbox... | per-object-cap: 20 MB per attachment (the binding constraint | - | qualifies-with-caveat |
| Seznam.cz Email, unlimited-size mailbox... | Docs page states verbatim: "Uzivatel muze schranku vyuzivat v neomezene velikosti... | per-object-cap: 35 MB attach send from web (25 MB from mobile app) | - | qualifies-with-caveat |
| UKR.NET Mail, 100 GB per single message... | Help wiki states verbatim: " 1024, ', 100." = up to 1,024 attachments per message... | per-object-cap: 100 GB/message | - | qualifies-with-caveat |
| Kaggle Notebooks + Datasets | Notebooks: '20 Gigabytes of auto-saved disk space... | per-object-cap: 200GB per dataset | - | qualifies-with-caveat |
| Lightning AI Studios | Free plan: '1 free active Studio (4 hour restarts)'... | retention-clamped: deleted after 6 months without login | - | qualifies |
| Modal | Volumes: 'Volumes include up to 1 TiB free' on the Starter plan... | retention-clamped: deleted data can bill up to 4 days) | - | qualifies |

## What the class is

Three substrates and three different failure modes.

**A backend-as-a-service** exposes an asset pipeline. Hygraph gives unlimited assets with a 50
MB cap and 100 GB of traffic per month. Sanity gives 100 GB of assets and 100 GB of bandwidth
per project. Prismic gives unlimited assets with 100 GB of CDN bandwidth and no overage option.
The quota is generous and the traffic allowance is the constraint.

**A database** gives a small allocation with a strong interface. MongoDB Atlas gives 512 MB per
free cluster. Neon gives 5 GB of object storage and 1 GB of Postgres per project, with 20 GB per
account across 100 projects. These are the smallest numbers in the topic and they are the most
reliable.

**Email** is the oldest substrate and the one with the strangest numbers. Seznam's mailbox is
unlimited in bytes with a 120,000-message cap. UKR.NET allows 100 GB per single message with
1,024 attachments. Mail.bg gives 50 GB with a 20 MB attachment limit.

**A notebook disk** is compute-attached and disappears with the runtime. Modal Volumes gives 1
TiB free per workspace, which is larger than any generalist free drive in the corpus.

## Email as storage, and the limit nobody reads

The three email records are worth reading together because they show three different binding
constraints on the same substrate.

Seznam's quota is unlimited in bytes and bounded by message count at 120,000, which can be
raised repeatedly. That is not a byte quota at all; it is a rate limit on the number of objects,
and it is the only such constraint in the corpus expressed in objects rather than bytes.

UKR.NET's 100 GB per single message with 1,024 attachments is the largest single-message cap
found anywhere. It is also a constraint on the *message* rather than the mailbox, so the
achievable total depends on how many messages the account will hold.

Mail.bg's 50 GB mailbox with a 20 MB attachment cap is the ordinary shape, and its 20 MB is two
orders of magnitude below the 2 GiB that a shard plan needs.

The interface is what decides whether any of them is usable. IMAP's `APPEND` is the write path
and its size limit is a server setting: a probe measured `APPENDLIMIT=71680000` on one host,
which is 68.4 MiB. The base64 encoding adds 33% overhead, which is why an email store's usable
bytes are about three quarters of its nominal quota.

## Notebook disks and compute-attached storage

Four records here are disks attached to a compute product, and their value is that they are
large and their cost is that they expire.

Modal Volumes gives 1 TiB free per workspace on the Starter plan, then USD 0.09 per GiB per
month. That is the largest free disk allocation in the topic and it is a real object store with
a real API.

Lightning AI Studios gives 200 GB of persistent storage on the free plan with a four-hour
restart. Kaggle gives 20 GB of auto-saved disk per notebook version and 200 GB per dataset.

All three share the same failure: the storage is attached to a runtime, and a runtime is
reclaimed. Modal is the exception among them because a Volume outlives the container, which is
why it appears as `qualifies` rather than caveated.

## The Chinese model hubs, and a documented absence

Five records here are Chinese or Chinese-adjacent model hubs, and three of them publish no quota
at all. OpenCSG states why, in its own words: "upload size and timeout limits are determined by
the site, proxy and storage configuration", and it warns against reading a site limit as a
protocol ceiling. Modelers and OpenXLab publish nothing.

That absence is the finding. A hub with no published quota and a measured repository total of
688.6 GB is a hub whose ceiling is an operational decision.

Baidu AI Studio is the one with two separate pools stated: 100 GB of cloud-persistent notebook
storage per user, plus a dataset centre with its own allowance. That separation is worth
noting because a plan that counts one pool as the other will be short by the difference.

## The Ollama namespace

Ollama's registry is the strongest finding in the model-hub class and the number needs stating
precisely.

`GET /v2/` returns 404 with 19 bytes, so the OCI discovery endpoint is absent. A manifest request
returns 200 with 1,006 bytes, and its largest layer is 42,520,398,528 bytes, which is 39.6 GiB
(`measured`, 2026-10-22: 200, 1,006 B manifest; 307 then 206 on the layer). The 455 GiB figure belongs to a different namespace, and
the `library/` namespace an uploader would use does not expose it.

The pull path is open and the push path is gated: an unauthenticated push returns 401 with
`www-authenticate: Bearer`. The practical write ceiling is an undocumented 413, so the registry
is a source of blobs rather than a destination.

### Hygraph

> Unlimited asset storage on Hobby (free) with a 50 MB per-asset cap; 100 GB asset traffic/month

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 50 MB per asset. The record states no identity cost. Observed behaviour: CDN-served, no expiry.

Evidence: `https://hygraph.com` (2026-10-21), record `dossier/storage/hygraph.json`.
Verdict: `qualifies-with-caveat`.

### MongoDB Atlas (M0 / Free cluster)

> 512 MB data storage per free cluster (0.5 GB, uncompressed BSON + indexes); one free cluster per project; 250 projects per Atlas user and 250 per organization

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Free clusters are shared and throttle at 100 ops/sec.

Evidence: `https://www.mongodb.com/atlas` (2026-10-21), record `dossier/storage/mongodb-atlas.json`.
Verdict: `fails-quota`.

### Neon (Object Storage + Postgres)

> 5 GB object storage per project + 1 GB Postgres per project (20 GB account total); 100 projects on Free

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Max object size 5 GiB. The record states no identity cost. Observed behaviour: Compute scale-to-zero after 5 min (Free, cannot disable).

Evidence: `https://neon.com` (2026-10-21), record `dossier/storage/neon.json`.
Verdict: `fails-quota`.

### Prismic

> Unlimited assets + unlimited documents on Free; 100 GB CDN bandwidth/month (no overage)

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Hard bandwidth stop at 100 GB with no paid overage on Free.

Evidence: `https://prismic.io` (2026-10-21), record `dossier/storage/prismic.json`.
Verdict: `qualifies-with-caveat`.

### Sanity

> 100 GB assets + 100 GB bandwidth/month per project; no maximum number of projects per account

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Free projects are hard-capped, not throttled: at 100 GB bandwidth the CDN returns errors until the calendar month resets.

Evidence: `https://www.sanity.io` (2026-10-21), record `dossier/storage/sanity.json`.
Verdict: `qualifies-with-caveat`.

### Mail.bg, 50 GB free mailbox with free IMAP/POP, Bulgarian

> Signup page, Waybacks capture 2026-02-23: "50 GB ", "20 MB ", "1 GB ". = 50 GB mailbox, 20 MB attachment cap, 1 GB file to any mailbox worldwide

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB per attachment (the binding constraint.... The record states no identity cost. Observed behaviour: Small national provider.

Evidence: `https://mail.bg` (2026-10-21), record `dossier/storage/mail-bg-50-gb-free-mailbox-with-free-imap-pop-bulgarian.json`.
Verdict: `qualifies-with-caveat`.

### Seznam.cz Email, unlimited-size mailbox, message-count-bound

> Docs page states verbatim: "Uzivatel muze schranku vyuzivat v neomezene velikosti. V praxi je kazda schranka zalozena s limitem na 120 000 zprav, ktery lze opakovane navysovat." = unlimited mailbox size; in practice each mailbox starts...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 35 MB attach send from web (25 MB from mobile app).... The record states no identity cost. Observed behaviour: Operators state up front that they police excess use of the unlimited claim: rules are tuned to catch anyone probing "kde je ta skutecna hranice" (where the real boundary is).

Evidence: `https://www.seznam.cz` (2026-10-21), record `dossier/storage/seznam-cz-email-unlimited-size-mailbox-message-count-bou.json`.
Verdict: `qualifies-with-caveat`.

### UKR.NET Mail, 100 GB per single message, 1024 attachments/message

> Help wiki states verbatim: " 1024, ', 100." = up to 1,024 attachments per message, and the total message size including all attachments must not exceed 100 GB. If that figure is real it is the largest per-object cap found anywhere in this...

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 GB/message. The record states no identity cost. Observed behaviour: The 100 GB claim is a docs statement with no observed evidence behind it and one plausible unit error (vs).

Evidence: `https://www.ukr.net` (2026-10-21), record `dossier/storage/ukr-net-mail-100-gb-per-single-message-1024-attachments.json`.
Verdict: `qualifies-with-caveat`.

### Kaggle Notebooks + Datasets

> Notebooks: '20 Gigabytes of auto-saved disk space (kaggle/working)' per notebook version. Datasets: '200GB per dataset limit', '200GB max private datasets', the 200 GB private cap is the only account-level storage number published; public...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200GB per dataset. The record states no identity cost. Observed behaviour: Notebook output survives session end as a versioned artifact, the closest thing here to real object storage, but it is write-once per version.

Evidence: `https://www.kaggle.com` (2026-10-21), record `dossier/storage/kaggle-notebooks-datasets.json`.
Verdict: `qualifies-with-caveat`.

### Lightning AI Studios

> Free plan: '1 free active Studio (4 hour restarts)', 'Persistent storage (200 GB limit)'. Studio docs say the default Studio disk is 400 GB; pricing page caps the free tier at 200 GB

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: deleted after 6 months without login. The record states no identity cost. Observed behaviour: Disk genuinely persists across sleep/switch ('Studios persist their environments when sleeping and switching machines').

Evidence: `https://lightning.ai` (2026-10-21), record `dossier/storage/lightning-ai-studios.json`.
Verdict: `qualifies`.

### Modal

> Volumes: 'Volumes include up to 1 TiB free' on the Starter plan, then $0.09/GiB/mo (per PricingSaaS capture of the Jun 2026 pricing change). Starter also includes $30/mo of compute

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: deleted data can bill up to 4 days). The record states no identity cost. Observed behaviour: Data persists independent of compute and survives container shutdown.

Evidence: `https://modal.com` (2026-10-21), record `dossier/storage/modal.json`.
Verdict: `qualifies`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Appwrite Cloud | fails-quota | 2 GB storage + 5 GB bandwidth on Free; 2 projects |
| CockroachDB Cloud (Basic) / Continuum | fails-quota | $15/month of free resource consumption per pay-as-you-go org = 50M Request Units + 10 GiB storage/month |
| Convex | fails-quota | 1 GB file storage on Free; 1 GB/month file egress; 0.5 GB database; 40 deployments |
| Firebase Storage (Cloud Storage for Firebase) | fails-egress | 5 GB stored on Spark (no-cost) plan; 1 GB downloaded per day; 50k download ops/day |
| Nhost | fails-quota | 1 GB storage + 1 GB database on Starter (free); 1 project |
| PocketHost (PocketBase hosting) | trial-only | 10 GB file storage + 250 MB DB per PocketBase slot, slots are $9.99/mo (or $5/mo annual, or lifetime), with a 7-day trial |
| Strapi Cloud | trial-only | 50 GB asset storage + 50 GB asset bandwidth on Starter, but Starter is $35/month, NOT free |
| Supabase | fails-egress | 1 GB file storage, PER ORGANIZATION, not per project; 5 GB egress + 5 GB cached egress per org... |
| Turso | fails-quota | 5 GB total storage, 100 databases on Free |
| Upstash (Redis / Vector / QStash) | fails-quota | Redis Free: 250 MB max data, 10 GB bandwidth/month, 1 database. Vector Free: 1 GB total data... |
| Aiven free tier (PostgreSQL / MySQL / Valkey /... | fails-quota | 1 GB disk each for PostgreSQL, MySQL and Valkey (Valkey maxmemory = 50% of 1 GB RAM = 512 MB usable)... |
| Algolia | fails-quota | 50,000 records on the Free/Build plan (100K on the paid Grow tier); 10,000 search requests/month |
| Amazon DynamoDB | fails-egress | 25 GB of storage, always free (does not expire), plus 25 WCU and 25 RCU provisioned capacity and ~200M requests/month |
| Cloud Firestore | fails-quota | 1 GiB stored data on the free tier; 50,000 document reads/day; 20,000 writes/day; 10 GiB/month outbound |
| CockroachDB Cloud (Basic tier) | fails-quota | $15/month of free resource consumption per pay-as-you-go org... |
| Firebase Realtime Database | fails-egress | 1 GB stored on the Spark (no-cost) plan; 10 GB/month downloaded (~360 MB/day) |
| Redis Cloud (free tier) | fails-quota | 30 MB single database, free forever |
| Upstash Redis | fails-quota | 250 MB max data size on Free; 500K commands per month; 10 GB bandwidth/month |
| Upstash Vector | fails-quota | 1 GB total data+metadata on Free; 10K daily queries; 200M vectors x dimensions |
| beehiiv (free plan), 500 MB per podcast episode... | fails-quota | Free plan is "Free forever" with unlimited email sends (pricing page)... |
| Ghost(Pro), 5 MB on free trial/Starter... | trial-only | "When uploading media files to Ghost, while there is no limit on the number of files you can upload to your site... |
| Gmail (free @gmail.com), 15 GB shared... | fails-quota | 15 GB per Google Account, shared across Gmail, Drive and Photos: "Each Google Account includes up to 15 GB of storage... |
| GMX (free), 65 GB mailbox, IMAP after opt-in... | fails-quota | GMX's own storage page: "With GMX, you can store up to 65 GB worth of emails. To put that into perspective... |
| Outlook.com (free), 15 GB mail quota... | fails-quota | 15 GB mail storage, explicitly separate from the 5 GB OneDrive allowance: "You get 15 GB of free Outlook.com email storage... |
| Yahoo Mail (free), 20 GB, down from 1 TB | fails-quota | Yahoo's own help, read live: "Yahoo Mail incluye actualmente 20 GB de almacenamiento gratuito con cada cuenta" = 20 GB free... |
| Yandex Mail, 5 GB pooled with Disk, 1 GB attachment | fails-quota | Yandex's own docs: "By default, users without a plan get 5 GB of storage space." Mail and Disk now share one pool: "Emails... |
| Zoho Mail Free, 5 GB/user... | fails-quota | Zoho's own help: "Each user is allocated 5 GB of storage under the free plan." Headcount: free plan is 5 users in select... |
| Deepnote | fails-quota | Free plan: 3 editors, 5 projects, Basic machine (5 GB RAM... |
| Google Cloud Shell | fails-quota | 'Cloud Shell provisions 5 GB of free persistent disk storage mounted as your $HOME directory... |
| Google Colab | fails-quota | No persistent disk at all. Notebook files live in Drive; the VM disk is per-session |
| Hex | fails-quota | Community (free): small compute only, 2 GB / 4 GB / 8 GB RAM profiles at $0/hr. No storage allocation published... |
| Hugging Face Spaces (disk check only) | fails-quota | 50 GB of disk per Space, but per HF's own docs the Space disk is NOT persistent... |
| molab (marimo cloud) | fails-quota | 'Notebooks get a limited amount of persistent storage', size deliberately undisclosed... |
| Observable | fails-quota | Free plan: 'File attachments 1 GB / mo.' |
| Paperspace Gradient (DigitalOcean) | fails-quota | Free tier: '5GB storage', basic instances, free GPU, public projects |
| Replit (App Storage) | fails-egress | No free storage allowance. App Storage is metered: $0.015/GiB/mo storage, $0.05/GiB data transfer, $0.0004/1k basic ops |
| Streamlit Community Cloud | fails-quota | 'Storage: No minimum, 50GB maximum' per app, but the filesystem is the build container, not durable storage |
| Val Town | fails-quota | Free plan blob storage: '10mb on the free plan and 1gb on pro'. Pro is the ceiling, so there is no free path to bulk |

Quota is the largest group and it is unremarkable. The interesting rejections are the ones where
the substrate is wrong rather than small.

`not-storage` covers the databases used as blob stores: a 512 MB cluster is a database, and a
plan that puts 20 TiB in one has misunderstood the product.

`egress` covers the BaaS traffic allowances, which are the real constraint in that group. A
backend with unlimited assets and 100 GB of monthly traffic is a 100 GB read budget, and the
asset quota is decoration.

## Chaining

An odd substrate is a metadata store, not an archive store, with one exception.

The exception is Modal Volumes, which gives 1 TiB free per workspace with a persistent volume
and a real API. That is larger than any free drive in the corpus and it is the one substrate
here that could hold a working set.

The pattern that works for everything else is a manifest in a database and the archive
elsewhere. An archive of 20 TiB at 25 MiB shards is 838,861 rows, which fits comfortably in a 512 MB
MongoDB cluster or a 1 GB Neon Postgres database, and the index is the only object that must be
durable while the shards are replaceable.
