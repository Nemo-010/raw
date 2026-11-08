# Storage: where 20 TiB lives, and where 1 TiB per day comes from

This topic answers one question: which services can hold an archive of 20 TiB and a hot
working set of 10 TiB, and serve 500 GB to 1 TiB every day, with programmatic access and
an identity a reader can produce. The storage test assumes those three sizes.

## The answer, and its price

Three findings decide it, and each one costs something.

**The purchase is bandwidth, not bytes.** Hetzner sells the same 20 TB twice. The
Storage Box is EUR 2.03 per TB per month with unlimited traffic. The Object Storage is
EUR 7.31 per TB per month, which is USD 8.21 at 1.1234 USD/EUR, and metered. The 3.6x
gap is the egress term and nothing else (`documented`, 2026-10-22: the Storage Box
pricing page carries 3.20, 10.90, 20.80 and 40.60 EUR and the docs page states "Each
Storage Box comes with unlimited traffic"; the Object Storage base price is EUR 6.49
per month, storage overage EUR 0.0087 per TB-hour and egress EUR 1.00 per TB, so
20 TB stored and 20 TB read is EUR 146.16 = EUR 7.31/TB).
Every cheap-storage claim dies on the same rock. When a vendor says
free egress, find the ratio and its scope: Wasabi is 1:1 (`wasabi.com/pricing/faq`,
read 2026-10-22: "if you store 100 TB with Wasabi and download (egress) 100 TB or less
within a monthly billing cycle"); MEGA S4 is 5:1 (`mega.io/objectstorage`, read
2026-10-22: "MEGA S4 includes up to 5x your average monthly stored data as free
egress"); pCloud is 2:1 on **public shared-link traffic only** (`help.pcloud.com/
article/shared-link-traffic`, read 2026-10-22: Premium Plus 2 TB gets 4 TB per month,
Ultra 10 TB gets 20 TB), so API, WebDAV and rclone downloads are not counted against
it; Datalix is 10:1 (`datalix.de/s3-kompatibler-objectstorage-mieten`, read
2026-10-22: "10 TB Egress je 1 TB gebuchtem Storage"). A free-tier chain pays for its
bytes with someone else's bandwidth, which makes it fragile.

**The free lane is bounded by retention and identity, not by quota.** Cloudflare Pages
holds 47.68 TiB per account, which is 100 projects x 20,000 files x 25 MiB, and
requests to static assets are "free and unlimited" on both free and paid plans
(`documented`, 2026-10-22: limits page 200, 7,360 B, all three numbers verbatim). That
figure is reachable only if the mean object is at least 10.49 MiB, and 20 TiB at a
1 MiB mean needs 10.5 accounts. In the anonymous file-host class the largest per-object
caps sit on the shortest clocks: file.kiwi accepts 999 GiB and deletes it after 90 hours;
firestorage.jp accepts 300 GiB and deletes it after 3 days by default. The model hubs and
code forges in the same ranking have no clock at all (Ollama at 455.5 GiB, Civitai at
65.83 GiB, CNB at 64 GB, GitHub Releases at 2 GiB), so this is a property of the class
rather than of size: a large object on an anonymous host is a transfer bus, and the same
object on a forge is storage that lasts while the repository does. An archive of 20 TiB that
lands on firestorage.jp is 20 TiB of scheduled data loss; one that lands on Ollama has no
publishing path at all.

**The largest quotas are behind institutional doors.** CSC Allas offers 10
TiB per project and LUMI-O offers 150 TB, and both require a Finnish or EuroHPC
project. The National Research Platform answers an anonymous bucket list, and its
namespace needs a US institutional sponsor. Those figures are real and worth zero
here. The academic repositories that do leave the door open are a different set, and
their quota is usually a software default rather than a policy: 83 of 149 Dataverse
installations report no quota at all, DSpace has no quota concept, and the binding
question is whether the installation allows email signup.

The recommendation that follows is a composition, not a provider. Use Cloudflare Pages for
the free cold copy, after consolidating objects to 25 MiB shards. Use GitHub Releases behind
a Worker for the serving tier, with a token cache rather than a body cache. Rent a managed
box for the hot working set: the EUR 27 PulsedMedia box fits 500 GB per day, and the EUR 41
Hetzner BX41 is the figure that fits 1 TiB per day.

⛔ **Storage bought and owned outright is out of scope.** It is about five times cheaper
per TB than any managed box, and it is excluded because the corpus assumes no local
hardware. The arithmetic is in
`history/2026-10-22T061500Z/own-the-disk-is-not-an-option.md`. Everything in this topic
that prices capacity prices a service somebody else runs.

## Four ways to hold 20 TiB, priced

The four headline rates below are four different products. Read the column as
"cheapest in its class", never as "cheapest overall".

| approach | monthly cost | what it gives | what binds |
|---|---|---|---|
| Free-tier chain | USD 0 | 47.68 TiB on Pages, plus a serving tier on Releases | mean object at least 10.49 MiB, write-once, no ranged reads |
| 1fichier GOLD | EUR 0.90 per TB (EUR 108/year, 10 TB) | cold archive, "Unlimited downloads, no monthly allowance" | cold tier only, 300 GB per file (`documented`, 2026-10-22) |
| PulsedMedia M10G | EUR 1.69 per TB (EUR 26.99, 16 TB) | hot space, WebDAV and rsync | `per-ip-shaping`: 100 Mbps is 0.982 TiB per day (`inferred`, 2026-10-22) |
| Hetzner BX41 | EUR 2.03 per TB (EUR 40.60, 20 TB) | hot space, rclone, WebDAV, SFTP, Samba | discretionary fair use at 250 TB/month, 8.3x above this workload |

The arithmetic a reader should check: 100 x 20,000 x 25 MiB = 47.68 TiB. 20 TiB
divided by 2,000,000 slots = 10.49 MiB. 100 Mbps sustained for 24 hours = 1.08 TB,
which is 0.982 TiB. EUR 40.60 divided by 20 TB = EUR 2.03.

## The seven constraints

The marketing number is almost never the binding one. Every finding in this topic
names which of these applies, and the record carries one entry per constraint found.
This section is the only statement of them; every other document links here.

| constraint | what it looks like | what it does to the workload | the question that exposes it |
|---|---|---|---|
| `request-rate` | 5,000 per hour, 80 writes per minute, 1,000 per month | bounds calls, not bytes. A monthly counter is fatal to a nightly job. | what is the window, and is it per account, per project or per IP? |
| `pull-count` | 100 pulls per 6 hours per IP | turns a daily serving target into a counting problem | how many distinct objects per day, and how much reuse? |
| `per-ip-shaping` | 1.7 MB/s, 6 GB per day per IP | bounds one reader; parallel readers multiply it | what does one stream get, and what does the thirty-second get? |
| `per-object-cap` | 2 GiB per asset, 256 GB per object, 20 GB per file | sets the shard size, therefore the file count, therefore the real total | what is the largest single object, and how many may be created? |
| `write-gated` | a curator, a review, a build recipe, a phone PIN | the write is a queue with a person in it | who approves, and what is the rejection rate? |
| `retention-clamped` | 1 year requested, 90 days granted | the clock is set by the server, not the caller | what does the API report as expiry, rather than what was requested? |
| `volume-quota` | 1,000 GB per month, 100 GB per month of egress | a monthly counter, which is not an object cap and not a rate | is the allowance per account or per caller, and when does it reset? |

Two corollaries, both measured. The write path is throttled separately from the read
path, so a large quota can arrive with a small upload budget: DeepStorage's free 2 TB
accepts 50 GB of uploads. And a rate cap does not bound a day's volume while a byte
quota does, so a volunteer relay at 200 Mbit/s moves 1.96 TiB per day with no quota
while a free TURN relay at 1,000 GB per month moves 33 GB per day.

## The documents

Read the row, not the tree. The counts are summed on 2026-10-22 from each record's own
`verdict`, grouped by the document the record names as its `target_document`: 376 qualifying
records (`qualifies` or `qualifies-with-caveat`) and 482 rejected, across the 22 documents
that carry records. The `dead-ends.md` row carries a dash because its 445 rejected providers
are already inside the 482, and repeating them would double the column.

| document | what question it answers | qualifying | rejected |
|---|---|---|---|
| [`free/README.md`](free/README.md) | what the free lane is, and which four Tier-1 entries are unreachable | 0 | 0 |
| [`free/cloud-tenants.md`](free/cloud-tenants.md) | what a Google, Microsoft, education or nonprofit tenant gives, and what it costs to hold one | 24 | 47 |
| [`free/academic.md`](free/academic.md) | which open-science repositories accept a deposit, and what their real ceiling is | 26 | 27 |
| [`free/academic-identity.md`](free/academic-identity.md) | why identical Dataverse software answers differently at two institutions | 20 | 18 |
| [`free/research-clouds.md`](free/research-clouds.md) | which national research clouds exist, and which of them a foreign individual can join | 16 | 11 |
| [`free/cloudflare-edge.md`](free/cloudflare-edge.md) | can a CDN be a store, and what does the edge actually guarantee | 15 | 9 |
| [`free/anonymous-hosts.md`](free/anonymous-hosts.md) | what accepts bytes with no account at all | 33 | 43 |
| [`free/ephemeral-hosts.md`](free/ephemeral-hosts.md) | which file hosts hold a large object, and for how long | 8 | 17 |
| [`free/registries.md`](free/registries.md) | which OCI, package and artifact registry accepts an arbitrary blob | 31 | 18 |
| [`free/forge-surfaces.md`](free/forge-surfaces.md) | what a code forge stores besides code, and how the release path behaves | 28 | 22 |
| [`free/relays-and-transports.md`](free/relays-and-transports.md) | which transport moves bytes without a byte meter, and which one only signals | 12 | 41 |
| [`free/transfer-services.md`](free/transfer-services.md) | what a transfer service is, and why it is not storage | 11 | 32 |
| [`free/messaging.md`](free/messaging.md) | what a chat platform's attachment store actually holds | 16 | 24 |
| [`free/social-and-fediverse.md`](free/social-and-fediverse.md) | what a fediverse instance or a social platform gives a user | 14 | 35 |
| [`free/media-and-archives.md`](free/media-and-archives.md) | what survives ingest byte for byte, and what is re-encoded | 35 | 30 |
| [`free/models-and-media.md`](free/models-and-media.md) | which model hub accepts a single huge blob | 12 | 19 |
| [`free/odd-substrates.md`](free/odd-substrates.md) | which non-storage service can be made to hold bytes, and what that costs | 9 | 40 |
| [`free/government-portals.md`](free/government-portals.md) | can an individual publish to a government open-data portal | 1 | 13 |
| [`free/baselines.md`](free/baselines.md) | what Hugging Face, ModelScope and GHCR offer, re-measured | 0 | 0 |
| [`free/sharding.md`](free/sharding.md) | what per-object ceiling sets the shard size, and where the Pages break-even is | 0 | 0 |
| [`free/host-economics.md`](free/host-economics.md) | how a free host pays for the disk, and what the pool architecture costs | 0 | 1 |
| [`paid/README.md`](paid/README.md) | what the paid lane buys that the free lane cannot | 0 | 0 |
| [`paid/storage-boxes.md`](paid/storage-boxes.md) | which box is cheapest per usable TB, and what its port caps | 28 | 8 |
| [`paid/object-storage.md`](paid/object-storage.md) | which S3-compatible store survives a read-heavy pattern | 7 | 4 |
| [`paid/lifetime-and-deals.md`](paid/lifetime-and-deals.md) | which lifetime deal is real, and when to buy | 22 | 18 |
| [`paid/regional.md`](paid/regional.md) | is regional cheaper, and by how much | 8 | 5 |
| [`dead-ends.md`](dead-ends.md) | every rejected provider in this topic, grouped by the failure that binds | 0 | - |
| [`gaps.md`](gaps.md) | which claims are weak, which contradictions are unclosed, and what rotted | 0 | 0 |

## Ranked by reachability, not by size

The column that decides everything is identity. The ranking orders by reachability
rather than by headline quota.

| rank | provider | ceiling | identity | the catch |
|---|---|---|---|---|
| 1 | Cloudflare Pages | 47.68 TiB per account | email | write-once, 25 MiB per file, mean object at least 10.49 MiB |
| 2 | Borealis | no quota object on the collection | email, affiliation free text | 2.5 GB per file, terms reserve removal |
| 3 | Zenodo | 50 GB per record, unlimited records, 150 GB pool | email | write-once, edits for 30 days |
| 4 | Internet Archive | 1 TB per item, unlimited items | email | about 145 GB per day per IP |
| 5 | Harvard Dataverse | 1 TiB per collection where one is set | email | new collections support-gated |
| 6 | RepOD | "not to exceed 2 TB" per dataset, advisory | email, self-serve | 5 GB per file, ranged reads conditional |
| 7 | `pan.moe` | 1 TB, permanent | email | single operator, Cloudreve over local disk |
| 8 | Ploud | 1 TB, Nextcloud | any-phone | single operator |
| 9 | 1yunpan | 500 GB | email | 1 TB per month egress |
| 10 | M365 A1 education | 100 TB pooled per tenant | education tenant | quotas falling |
| 11 | HDX (UN OCHA) | no published quota | email plus a reviewed organisation | editorial gate |

Ranks 1 to 6 are reachable today. Ranks 7 to 9 are reachable and depend on one
person's server staying up. Rank 10 needs an education tenant.

## Dead-end classes

The 1329 rejected records in this topic fall into ten classes, 480 of them also holding a
row in the provider table and 847 existing only in the dead-end list. The full table, with
the reason for each provider, is [`dead-ends.md`](dead-ends.md).

| class | table rows | dead-end only | what it means |
|---|---|---|---|
| quota | 365 | 506 | the free allowance cannot reach 500 GB per unit |
| egress | 42 | 63 | the read path is metered, shaped or absent |
| dead-service | 7 | 107 | the host is gone, parked, seized or sunset |
| not-storage | 7 | 38 | a category error: compute, a catalogue, a metadata index |
| retention | 29 | 43 | the bytes are deleted on a clock |
| paid | 16 | 42 | it works, and only at a price above the floor |
| write-gated | 11 | 25 | a curator, review or invite stands in front |
| trial-only | 0 | 0 | a clock, however large |
| identity | 3 | 18 | the quota is real and a reader cannot register |
| read-gated | 0 | 5 | the write works and the read returns different bytes or nothing |

Four classes deserve a sentence each, because they are the ones a reader will
otherwise re-attempt.

A `read-gated` host is worse than a dead one, because the write succeeds and the loss arrives
later. FileDitch accepts 155 GiB and returns 503 to every non-browser client, and every AList
instance that advertised `"write": true` refused the PUT with 403 inside an HTTP 200.

A `not-storage` service is the most common mistake in the corpus. Korean webhard sites sell
per-download credit rather than storage, and print-on-demand takes huge ingress with no read
path at all.

A `retention` host looks like a win, because some of the per-object caps there
are the largest recorded. file.kiwi takes 999 GiB and deletes it after 90 hours. The ten
largest caps are split: the anonymous file hosts among them all carry a clock, and the model
hubs and code forges among them carry none.

`trial-only` is zero in both columns, and that is structural rather than a gap: this table
classifies by `failure_class`, and the dead-end list never assigned that class.
The 28 records whose *verdict* is `trial-only` are not dead ends and are counted in the provider
tables. `identity` has 3 table rows and 18 dead-end-only ones.

`dead-service` is large: five Cloudreve instances and OSDN are in it, and each one closed within
two years of being recorded.

## Withdrawn claims

A reader who trusts a page without reading this table trusts sentences that are
wrong. Each row names what took the old claim away and where the current correction
lives.

| withdrawn claim | what took it away | current correction |
|---|---|---|
| RepOD ignores `Range` | two probes on 2026-10-22: a 7,459 B text file answered 206 with a byte-identical first 1,024 B, and a 116,201,025 B binary answered 200 with no `Content-Range` | [`free/academic-identity.md`](free/academic-identity.md), and `gaps.md` |
| OpenCSG's 688.6 GB is a per-object ceiling | the tree API on 2026-10-22: 176 files, 688,603,604,082 B total, 163 shards over 1 GB, largest 6,584,784,447 B | [`free/models-and-media.md`](free/models-and-media.md) |
| Hetzner's fair-use threshold is 50 to 100 TB per month | the 2022 traffic notice letter reads 250 TB per month, quoted verbatim | [`paid/storage-boxes.md`](paid/storage-boxes.md) |
| P2P box advertises "unlimited", so it carries 1 TiB per day | 100 Mbps sustained is 0.982 TiB per day, which is 101.8% of the port for 1 TiB | [`paid/storage-boxes.md`](paid/storage-boxes.md) |
| hi168 grants 500 GB rising to 1 TB | the endpoint returned 526 through the fetch broker on 2026-10-22, and one corpus post says new signups get 5 GB | [`free/cloud-tenants.md`](free/cloud-tenants.md), verdict `fails-quota` |
| 1,122 candidate records dedupe to 1,101 providers | the 91 dossiers carry 1,255 candidate records, and the vendor and service-class merge yields 928 records | this page, `gaps.md` |

## What this topic does not do

It does not build a deployment stack. It does not say whether a provider's terms
permit a use; it records ban, throttle and data loss as technical reliability notes
only. It does not restate a number without a rung and a date. Where prose and the
records disagree, the record wins and the disagreement is recorded.

## Provenance of the numbers on this page

Everything here rests on the topic's 91 dossiers, its 1,101-row provider table and its
935-row dead-end list, re-probed where a probe was cheap. The distribution below is generated
from `dossier/storage/`, so it cannot drift from the records the rest of this page rests on:

<!-- generated:start topic=storage kind=breakdown field=confidence sort=value order=measured,documented,reported,inferred,unverified -->
| confidence | Records |
| --- | --- |
| `measured` | 3 |
| `documented` | 170 |
| `reported` | 1517 |
| `inferred` | 30 |
| **all** | 1720 |
<!-- generated:end -->

A `measured` claim needs a live request with its status, byte count and command recorded
(`METHODOLOGY.md` §3); reading a page and quoting it is `documented` by definition. The
`reported` majority follows from a mechanical conversion: 832 of these records state that no
page was read for them. Every rung printed beside a provider on this page is that provider's
`confidence` field, compared mechanically against its record.

Records with a live request in their own `evidence[]` carry a higher rung: OpenCSG, GigaFile,
Harvard Dataverse, SourceForge FRS and its project web space. A `reported` record cannot support
a `documented` sentence. The record's `evidence[]` carries the URL and the reading date.
Unicode is folded to ASCII on this page (EUR for the euro sign, a comma for a dash). A provider
whose own name is not ASCII keeps that name in a code span.

## Records that no other document names

This list is generated by `scripts/report/render.py` from the records. It holds each `measured` or
`documented` record of this topic that no other document of `docs/` names, so a reader finds it and
the gate's `links` check counts it as cited. A research run adds a row here only through the render
that `scripts/rq land` runs. A document that names the record removes its row at the next render.

<!-- generated:start topic=storage kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `acast-starter-plan` | Acast — Starter (free) plan | fails-quota | documented |
| `amazon-cloudfront-free-tier` | Amazon CloudFront free tier (as the e... | fails-quota | documented |
| `archive-org-classic-web-uploader` | archive.org classic web uploader (bro... | qualifies-with-caveat | documented |
| `archive-org-forum-10gb-per-item-guidance` | archive.org forum '10gb per item' gui... | qualifies-with-caveat | documented |
| `aws-s3-glacier-deep-archive` | Amazon S3 Glacier Deep Archive | paid-only | documented |
| `backblaze-b2` | Backblaze B2 | qualifies-with-caveat | documented |
| `basecamp-for-free` | basecamp for free | fails-quota | documented |
| `beehiiv-500-mb-per-podcast-episode-newsletter-attachment` | beehiiv (free plan) — 500 MB per podc... | fails-quota | documented |
| `bunny-net-as-a-free-egress-source` | bunny.net as a *free* egress source | fails-egress | documented |
| `bunny-stream` | bunny stream | paid-only | documented |
| `bytesized-hosting-appbox-range` | bytesized hosting — appbox range | paid-only | documented |
| `cachix-2` | cachix | fails-quota | documented |
| `claude-files-api-as-an-archive` | claude files api as an archive | fails-quota | documented |
| `cloud-ru-evolution-artifact-registry` | Cloud.ru Evolution Artifact Registry | paid-only | documented |
| `cloudflare-stream` | cloudflare stream | paid-only | documented |
| `common-crawl` | Common Crawl (the petabyte corpus — r... | fails-quota | measured |
| `contabo-storage-vps` | contabo storage vps | paid-only | documented |
| `contabo-storage-vps-30` | Contabo Storage VPS 30 | paid-only | documented |
| `crawl-scale-free-host-ftp-hosts-storage-share-cloudtb-fb` | crawl-scale free-host ftp hosts (stor... | paid-only | documented |
| `ctan-2` | ctan | fails-quota | documented |
| `cubbit-ds3-cloud` | Cubbit DS3 Cloud | trial-only | documented |
| `dataone-hosted-repository-the-price-anchor-for-managed-1` | DataONE Hosted Repository (TACC / UC... | paid-only | documented |
| `debian-snapshot` | debian snapshot | fails-quota | documented |
| `debian-snapshot-archive` | Debian snapshot archive (snapshot.deb... | fails-quota | documented |
| `deluxhost-storage-4` | deluxhost storage-4 (€6.99 / 3 tb) | paid-only | documented |
| `designsafe-ci-nheri-data-depot` | designsafe-ci / nheri data depot (tacc) | qualifies-with-caveat | documented |
| `deviantart-core-as-quota-escape` | deviantart core as quota escape | fails-quota | documented |
| `disposable-mail-providers-as-storage` | disposable-mail providers as storage... | qualifies-with-caveat | documented |
| `eurohpc-ju-regular-access` | EuroHPC JU Regular Access (LUMI, Leon... | fails-identity | documented |
| `euserv-backuphd-1t` | euserv backuphd 1t (se2021 / se2019 /... | dead | documented |
| `febbox-feb` | febbox / feb | fails-quota | documented |
| `febbox-feb-1-tb-free` | febbox / feb 1 tb free | fails-quota | documented |
| `figshare-for-institutions` | figshare for institutions | fails-quota | documented |
| `fil-one-storacha-s3-tier` | fil one / storacha s3 tier | trial-only | documented |
| `google-artifact-registry-3` | google artifact registry (as a blob s... | fails-quota | documented |
| `hetzner-object-storage-2` | hetzner object storage (as the kms al... | paid-only | documented |
| `hetzner-storage-box-bx11-1-tb-3-20-mo` | Hetzner Storage Box BX11 — 1 TB, €3.2... | paid-only | documented |
| `hostdare-hdd-vps` | hostdare hdd vps | paid-only | documented |
| `idrive-e2` | IDrive e2 | trial-only | documented |
| `idrive-personal-20-tb` | idrive personal 20 tb | paid-only | documented |
| `imagekit-2` | imagekit | fails-egress | documented |
| `internxt-100-tb-lifetime` | Internxt 100 TB lifetime (StackSocial) | paid-only | documented |
| `interserver-storage-cloud-compute-1-tb-slices-at-3-mo-re` | InterServer Storage Cloud Compute — 1... | paid-only | documented |
| `ionos-hidrive` | IONOS HiDrive (retail) | fails-quota | documented |
| `iroh-n0-public-relays` | iroh n0 public relays | fails-egress | documented |
| `iwinv-object-storage-and-sata-block` | iwinv (kr) object storage and sata block | fails-egress | documented |
| `jottacloud-2` | jottacloud | fails-quota | documented |
| `koofr-lifetime` | koofr lifetime (>1 tb) | paid-only | documented |
| `letbox-storage-kvm` | letbox storage kvm | paid-only | documented |
| `loom-vidyard-free-tiers` | loom / vidyard free tiers | fails-quota | documented |
| `mail-ru-cloud-mail-1-tb-with-free-public-link-download` | Mail.ru Cloud / Облако Mail (VK) — 1... | fails-quota | documented |
| `manitu-root-servers` | manitu (manitu.de) root servers | paid-only | documented |
| `mastodonapp-uk-mstdn-social-mastodon-social-and-the-stoc` | mastodonapp.uk / mstdn.social / masto... | fails-quota | documented |
| `mediafire-pro-1-tb` | MediaFire Pro 1 TB | fails-quota | documented |
| `microsoft-365-e5-developer-subscription` | microsoft 365 e5 developer subscripti... | fails-quota | documented |
| `microsoft-fabric-trial-onelake` | microsoft fabric trial / onelake | trial-only | documented |
| `multi-account-multiplication-of-big-cloud-free-tiers` | several-accounts multiplication of bi... | fails-quota | documented |
| `ncar-glade` | ncar glade (campaign / work / scratch) | fails-identity | documented |
| `nird-data-lake-s3-object-storage-10-tb-single-object-sup` | NIRD Data Lake (Sigma2, Norway) — S3... | paid-only | documented |
| `nsf-access-open-storage-network` | nsf access / open storage network (as... | fails-identity | documented |
| `ovhcloud-active-archive` | OVHcloud 3-AZ Active Archive class | paid-only | documented |
| `ovhcloud-high-performance-1-az` | OVHcloud High Performance (1-AZ) | paid-only | documented |
| `ovhcloud-infrequent-access-1-az` | OVHcloud Infrequent Access (1-AZ) | paid-only | documented |
| `ovhcloud-infrequent-access-3-az` | OVHcloud Infrequent Access (3-AZ) | paid-only | documented |
| `ovhcloud-local-zone-standard` | OVHcloud Local Zone Standard | paid-only | documented |
| `ovhcloud-managed-private-registry` | OVHcloud Managed Private Registry (Ha... | paid-only | documented |
| `ovhcloud-object-storage` | ovhcloud object storage | paid-only | documented |
| `ovhcloud-object-storage-2` | ovhcloud object storage (standard / c... | paid-only | documented |
| `ovhcloud-object-storage-cold-archive` | ovhcloud object storage cold archive | paid-only | documented |
| `ovhcloud-swift-cloud-archive` | OVHcloud Public Cloud Swift Cloud Arc... | paid-only | documented |
| `ovhcloud-swift-standard` | OVHcloud Swift Standard Object Storage | paid-only | documented |
| `playstation-app-captures-library` | playstation app captures library | fails-quota | documented |
| `playstation-plus-cloud-storage` | playstation plus cloud storage | paid-only | documented |
| `privatebin-public-instance-network` | PrivateBin public instance network | fails-quota | documented |
| `proton-mail-free` | proton mail free | fails-quota | documented |
| `pulsedmedia-eternal-v-in-m-inen-1-99-storage-tiers` | pulsedmedia — 'eternal väinämöinen' €... | fails-egress | documented |
| `pulsedmedia-storage-boxes-4-tb-at-8-99-mo-a-genuinely-fr` | PulsedMedia Storage Boxes — 4 TB at €... | paid-only | documented |
| `qiniu-kodo-free-quota` | qiniu kodo free quota | fails-egress | documented |
| `sakura-vps-nfs` | sakura vps nfs (jp) | paid-only | documented |
| `scramble-cloud-premium-6-tb-lifetime` | Scramble Cloud Premium 6 TB lifetime... | paid-only | documented |
| `seeweb-cloud-object-storage` | seeweb cloud object storage | paid-only | documented |
| `sendbird-chat` | Sendbird Chat (free plan) | fails-quota | documented |
| `sendgb-unlimited-transfers` | sendgb 'unlimited transfers' | fails-quota | documented |
| `servarica-unlimited-expanding-storage` | ServaRica — 'Unlimited Expanding Stor... | paid-only | documented |
| `sharepoint-embedded` | sharepoint embedded | paid-only | documented |
| `stack-exchange-as-bulk-storage` | stack exchange as bulk storage | fails-quota | documented |
| `storacha-fil-one` | storacha / fil one | trial-only | documented |
| `storj-object-storage-standard` | Storj Object Storage — Standard | fails-egress | documented |
| `systemfreaks-s3-compatible-object-storage-250-gb-free-du` | SystemFreaks S3-Compatible Object Sto... | paid-only | documented |
| `tableland-see-candidate-entry` | tableland — see candidate entry (fail... | fails-quota | documented |
| `tacc-corral-5-tb-free-per-pi-60-tb-year-beyond` | TACC Corral (US) — 5 TB free per PI,... | fails-quota | documented |
| `telnyx-cloud-storage` | telnyx cloud storage | fails-quota | documented |
| `tencent-cloud-cos` | tencent cloud cos (腾讯云对象存储) | fails-egress | documented |
| `time4vps-storage-vps` | Time4VPS Storage VPS | paid-only | documented |
| `twilio-programmable-messaging-media-subresource` | Twilio Programmable Messaging — Media... | paid-only | documented |
| `uldl-sh` | uldl.sh | fails-quota | documented |
| `utho-object-storage` | utho object storage (in) | paid-only | documented |
| `vercel-blob-2` | vercel blob | fails-egress | documented |
| `xirsys-free` | Xirsys free (Developer plan) | fails-quota | documented |
| `cubbit-ds3-composer` | Cubbit DS3 Composer (self-hosted) | fails-identity | documented |
| `perforce-p4-free-edition` | perforce p4 (helix core) free edition (self-hosted) | fails-quota | documented |
<!-- generated:end -->
