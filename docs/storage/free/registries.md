# Registries: which one accepts an arbitrary blob

A registry is the cheapest large-object store nobody prices as storage, because a
container image layer or a package tarball is not a file as far as the pricing page is
concerned. The question is narrow: which registry accepts one object of tens of
gigabytes, how many of them, and what rate applies on the read path.

This document covers 33 qualifying records across four sub-classes: OCI registries,
package ecosystems, artifact managers, and the docs and wiki hosts that serve a similar
role for small objects. 16 more were rejected, and most of those are priced rather
than closed.

## The comparison

Sorted by the size of a single object they accept, because that is what sets the shard. A
`*` in the identity column means the value is read off the record's own prose rather than
from its `identity_cost` field.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Cloudsmith, open-source (Broadcast: Open Source)... | At least 50 GB of artifact data + 200 GB of package delivery per month, free... | per-object-cap: maximum file size is 5GB | - | fails-quota |
| Gemfury, Public (free) plan | Public plan is $0/mo with UNLIMITED public packages... | per-object-cap: 300 MB per file | - | qualifies-with-caveat |
| Atlassian Confluence Cloud Free | 2 GB file storage on the Free plan (10 users... | per-object-cap: attachment default 100 MB, admin-configurable upward | - | qualifies-with-caveat |
| Bitrix24 Free (Drive) | Free plan: '5 GB storage' with 'Unlimited users - no team size limits'... | retention-clamped: deleted after 40 days', this is a documented d | - | qualifies-with-caveat |
| Fandom (wiki farm, MediaWiki) | 10 MB per file, no file-count cap: 'The maximum size of uploads is 10 MB... | per-object-cap: 10 MB (hard, confirmed live via siteinfo `maxuploadsize` =... | - | qualifies-with-caveat |
| GitBook (Free plan file library) | No published total storage quota. Per-file cap is explicit: 'GitBook allows you to... | per-object-cap: 100 MB per file, the only hard published number | - | qualifies-with-caveat |
| HubSpot (free-tools file manager / hubfs) | Per-file 20 MB on free accounts, 2 GB on paid. No published account total: 'Generally... | per-object-cap: 20 MB per file on free tools... | - | qualifies-with-caveat |
| Nuclino (free teams) | Free plan: '2GB total storage', up to 50 items, up to 3 canvases. Storage is per TEAM... | per-object-cap: 10 MB per file, the API documents `413 | - | qualifies-with-caveat |
| ShoutWiki (wiki farm, MediaWiki) | No published per-wiki storage cap; per-file ceiling is 100 MB (live siteinfo). Free... | per-object-cap: 100 MB (104,857,600 B, from siteinfo) | - | qualifies-with-caveat |
| CodeFloe (Forgejo, Hetzner Germany) | 5 GB Git + 20 GB packages + 10 GB Git LFS + 10 GB attachments per account/organization... | - | - | qualifies-with-caveat |
| Fjord Commons (Forgejo) | 5 GB per account; up to 25 repositories, public or private | request-rate: 2000 minutes/month pooled across ALL of Comm | - | qualifies-with-caveat |
| GitLab.com container registry | No published storage cap. Explicitly excluded from the per-project 10 GiB limit... | - | - | qualifies |
| GitLab.com generic package registry | 5 GB maximum per uploaded file (Generic)... | per-object-cap: 5 GB per file | - | qualifies |
| GitLab.com snippets | No documented per-snippet storage cap; snippets are git-backed and unlimited in count... | - | - | qualifies-with-caveat |
| NeoNeko Git (Forgejo, open registration) | No published storage quota. Site advertises 'no seat limits, no repository caps'... | - | - | qualifies-with-caveat |
| Alibaba Cloud ACR Personal Edition | Free of charge with count-based quotas and NO published byte quota: 'Personal Edition... | - | - | qualifies-with-caveat |
| Amazon ECR Public | 50 GB per month of always-free storage for public repositories: 'Both new and existing... | - | - | qualifies-with-caveat |
| Huawei Cloud SWR Basic Edition | Free, and explicitly without a byte cap, the strongest storage wording of any registry... | - | - | qualifies |
| Oracle Cloud Infrastructure Registry (OCIR) | No registry fee at all, and storage is billed at raw Object Storage rates: 'Oracle does... | - | - | fails-quota |
| Tencent Cloud TCR Individual Edition | Free, count-based only: 'The TCR Individual Edition is free of charge and can be... | per-ip-shaping: 20 MB/s | - | qualifies-with-caveat |
| crates.io | 10 MB per.crate file. No limit on versions per crate... | pull-count: 1000 downloads/month | - | qualifies-with-caveat |
| GitLab Package Registry (generic / npm / Maven / PyPI... | Explicitly EXCLUDED from the project storage quota. GitLab docs... | per-object-cap: 5 GB per file | - | qualifies |
| jsDelivr (npm + GitHub proxy CDN) | No storage quota of its own, it is a *serving and permanence* layer over npm and... | per-object-cap: 20 MB per single GitHub file | - | qualifies |
| npm public registry (registry.npmjs.org) | No total storage quota, no per-account package cap ('Unlimited public packages'... | - | - | qualifies |
| NuGet.org | 250 MB per package. No documented total-storage quota and no documented cap on package... | per-object-cap: 250 MB per package | anonymous* | qualifies-with-caveat |
| PyPI (Python Package Index) | 100 MB per file, 10 GB per project, both are *defaults*... | per-object-cap: 100 MB/file | - | qualifies |
| RubyGems.org | No documented per-gem size limit and no documented total quota... | - | - | qualifies-with-caveat |
| Docker Hub (free Personal plan, public repositories) | Unlimited public repositories on the free Personal plan... | per-object-cap: 10GB per layer | - | qualifies |
| Quay.io public repositories (Red Hat) | "We offer unlimited storage and serving of public repositories"... | - | - | qualifies |
| ttl.sh (anonymous ephemeral OCI registry) | No account, no quota. "Free forever. Zero sign-up... | per-ip-shaping: 11 MB/s observed: 1 | - | qualifies-with-caveat |
| JFrog Artifactory Community Edition... (self-hosted) | Free of charge, self-hosted, no storage cap of any kind: the quota is whatever... | - | - | qualifies-with-caveat |
| Pulp (pulpcore), self-hosted | Free open-source (GPL) self-hosted repository server... | - | - | qualifies-with-caveat |
| Sonatype Nexus Repository... (self-hosted) | Free, self-hosted, no storage quota: 'There is no cost to use Sonatype Nexus Repository... | - | - | qualifies-with-caveat |

## What the class is

A registry is content-addressed storage with an authentication story attached. That makes
it good at three things and bad at one.

It is good at size. A layer limit in the multiple gigabytes is normal, and Quay's own
support article says "We offer unlimited storage and serving of public repositories". It is
good at reads, because a public repository is pullable anonymously and served from a CDN.
And it is good at durability, because a package that is deleted breaks every downstream
build, so the ecosystems discourage deletion in their own documentation.

It is bad at long-term retrieval of the bytes it holds, because a registry is a publication
channel. NuGet's docs say deletion is "strongly discouraged and effectively unsupported",
and npm unpublishes a package after 72 hours only if it has fewer than 300 weekly
downloads and no dependents. An archive published as packages cannot be taken back.

## The four sub-classes

**OCI registries** are the best shape for a large arbitrary blob. `ttl.sh` takes any OCI
artifact with no account and a TTL of up to 24 hours, and a 1.5 GB monolith was accepted
with no chunking. Docker Hub gives unlimited public repositories with a pull-count limit of
100 per 6 hours anonymous. Quay gives unlimited public storage. GHCR caps a layer at 10 GB.

**Package ecosystems** are the best shape for a large number of small objects. PyPI's 100 MB
per file and 10 GB per project are defaults rather than ceilings, both raisable by filing a
GitHub issue, and 40 GB grants are routine. GitLab's package registry is explicitly excluded
from the project storage limit and takes 5 GB per file.

**Artifact managers** split into hosted and self-hosted, and the distinction is the whole
finding. Cloudsmith gives 50 GB of artifact data with 5 GB per file, free, for open-source
repositories. Gemfury gives unlimited public packages with a hard 300 MB per file. The
self-hosted managers, JFrog Community Edition, Pulp and Nexus, have no quota at all because
there is no vendor; their limit is the disk the deployment attaches, which makes them a
different kind of answer.

**Docs and wiki hosts** are a weak version of the same idea: Confluence gives 2 GB per site
with a 100 MB attachment default, ShoutWiki gives 100 MB per file, Fandom 10 MB per file.
They are in this document because their interfaces are registries of a kind, and they are
not usable as storage at this scale.

## The three numbers that decide a shard plan

Three figures set what a registry can contribute, and they are spread across the table
rather than in one place.

The per-object cap is the largest single blob. GHCR's 10 GB and GitHub Releases' 2 GiB are
the two that matter for a GitHub-based plan, and the 5x gap between them is why a release
tier and a registry tier are not interchangeable.

The per-account total is the one most often absent. Docker Hub publishes no storage cap at
all for public repositories, which is a documented absence rather than a documented limit
and cannot be multiplied. Quay's "unlimited" carries undisclosed fair use behind it.

The read path is where a registry fails this workload. Docker Hub's 100 pulls per 6 hours per
IP is the binding constraint for a 500 GB to 1 TiB daily workload, and it needs few large
blobs rather than many small ones. A registry is a shard source, not a serving tier.

## The trap in this class

A registry's quota page usually describes a limit that does not apply. GitLab excludes its
package registry from the project storage limit, and its container registry from the same
limit, which is why both appear as `qualifies` here while the git repository itself is
capped. A reader who checks only the project storage limit will conclude GitLab gives 10 GiB
and miss the 5 GB per file registry entirely.

The second trap is the pull counter. An OCI manifest plus a layer is two pulls, and a client
that re-fetches a manifest per request doubles the count. That is the same error as minting
a signature per connection, and it turns a 100-pull budget into 50.

## The providers, one section each

### Cloudsmith, open-source (Broadcast: Open Source) repositories

> At least 50 GB of artifact data + 200 GB of package delivery per month, free, pooled across ALL open-source repositories in one org, 'You get at least 50GB of artifact data + 200GB of package delivery for free, across all open-source...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: maximum file size is 5GB. The record states no identity cost. Observed behaviour: Real hosted CDN with a real CLI/API.

Evidence: `https://cloudsmith.com` (2026-10-21), record `dossier/storage/cloudsmith-open-source-repositories.json`.
Verdict: `fails-quota`.

### Gemfury, Public (free) plan

> Public plan is $0/mo with UNLIMITED public packages, unlimited versions and unlimited collaborators, and NO private packages. No storage figure appears anywhere on the pricing table, the plan matrix lists only collaborators / private...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 300 MB per file. The record states no identity cost. Observed behaviour: Small independent operator (fury.co, the same shop as the old gemfury.com).

Evidence: `https://fury.co` (2026-10-21), record `dossier/storage/gemfury-public-plan.json`.
Verdict: `qualifies-with-caveat`.

### JFrog Artifactory Community Edition (CE for C/C++) / Artifactory OSS, self-hosted

> Free of charge, self-hosted, no storage cap of any kind: the quota is whatever disk/object-store you attach. 'This product gives all the power and flexibility of the Artifactory repository for Conan and generic binaries to the C/C++ world...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Mature, no data-vanishing risk.

Evidence: `https://jfrog.com/community/download-artifactory-oss/` (2026-10-21), record `dossier/storage/jfrog-artifactory-community-edition-artifactory-oss-self.json`.
Verdict: `qualifies-with-caveat`.

### Pulp (pulpcore), self-hosted

> Free open-source (GPL) self-hosted repository server; no quota because there is no vendor. 'Pulp is an open source project that makes it easy for developers to fetch, upload, organize and distribute Software Packages on-prem or in the...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Very reliable (Red Hat-backed, used by COPR).

Evidence: `https://pulpproject.org/` (2026-10-21), record `dossier/storage/pulp-self-hosted.json`.
Verdict: `qualifies-with-caveat`.

### Sonatype Nexus Repository, Community Edition (self-hosted)

> Free, self-hosted, no storage quota: 'There is no cost to use Sonatype Nexus Repository Community Edition'; the feature matrix marks 'Unlimited Nexus Repository Deployments' as included. Storage is your blob store, so the ceiling is your...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Mature and stable.

Evidence: `https://www.sonatype.com/products/sonatype-nexus-repository/download` (2026-10-21), record `dossier/storage/sonatype-nexus-repository-community-edition.json`.
Verdict: `qualifies-with-caveat`.

### Atlassian Confluence Cloud Free

> 2 GB file storage on the Free plan (10 users, unlimited spaces and pages). Crucially: 'Free, Standard, and Premium plans entitle you to one app instance. **You can have as many of these plans as you need.** You'll subscribe to each one...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: attachment default 100 MB, admin-configurable upward.... The record states no identity cost. Observed behaviour: Nothing is deleted at quota, writes are blocked until the plan is upgraded or space is freed.

Evidence: `https://www.atlassian.com/software/confluence` (2026-10-21), record `dossier/storage/atlassian-confluence-cloud-free.json`.
Verdict: `qualifies-with-caveat`.

### Bitrix24 Free (Drive)

> Free plan: '5 GB storage' with 'Unlimited users - no team size limits'. Portals are free and self-service

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: deleted after 40 days', this is a documented d. The record states no identity cost. Observed behaviour: Inactive free portals are deleted after 40 days per Bitrix24's own blog, so an archive role requires periodic activity.

Evidence: `https://www.bitrix24.com` (2026-10-21), record `dossier/storage/bitrix24-free.json`.
Verdict: `qualifies-with-caveat`.

### Fandom (wiki farm, MediaWiki)

> 10 MB per file, no file-count cap: 'The maximum size of uploads is 10 MB. The maximum image resolution is 12.5 megapixels.' and 'There is no limit to the number of files you can upload' (with the caveat 'they shouldn't be used just as file...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 MB (hard, confirmed live via siteinfo `maxuploadsize` = 10485760). The record states no identity cost. Observed behaviour: Two read-path traps in one host.

Evidence: `https://www.fandom.com` (2026-10-21), record `dossier/storage/fandom.json`.
Verdict: `qualifies-with-caveat`.

### GitBook (Free plan file library)

> No published total storage quota. Per-file cap is explicit: 'GitBook allows you to upload files up to 100MB per file.' GitBook's own docs ask-API, queried live, answered: 'I cannot find a documented storage quota or total storage limit per...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MB per file, the only hard published number. The record states no identity cost. Observed behaviour: Access token in the download URL is NOT enforced, a deliberately bogus `token=0000` returned the identical 838-byte file (same sha256), so file URLs are effectively public and permanent.

Evidence: `https://www.gitbook.com` (2026-10-21), record `dossier/storage/gitbook.json`.
Verdict: `qualifies-with-caveat`.

### HubSpot (free-tools file manager / hubfs)

> Per-file 20 MB on free accounts, 2 GB on paid. No published account total: 'Generally, there is no limit on how many files you can upload.' HubSpot's own catalog does not state a storage figure

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB per file on free tools (the binding constraint by a wide margin). The record states no identity cost. Observed behaviour: The API is genuinely good (2e5 calls/day, 100/10s) but the 20 MB free per-file cap means shard-only.

Evidence: `https://www.hubspot.com` (2026-10-21), record `dossier/storage/hubspot.json`.
Verdict: `qualifies-with-caveat`.

### Nuclino (free teams)

> Free plan: '2GB total storage', up to 50 items, up to 3 canvases. Storage is per TEAM, and team creation is self-service and unlimited: 'CREATE TEAM... Available to anyone. Available on all plans', and 'A user can be a member of several...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 MB per file, the API documents `413. The record states no identity cost. Observed behaviour: Hard 10 MB per-file ceiling makes this shard-only.

Evidence: `https://www.nuclino.com` (2026-10-21), record `dossier/storage/nuclino.json`.
Verdict: `qualifies-with-caveat`.

### ShoutWiki (wiki farm, MediaWiki)

> No published per-wiki storage cap; per-file ceiling is 100 MB (live siteinfo). Free, ad-supported; paid tiers exist for custom domains

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MB (104,857,600 B, from siteinfo). The record states no identity cost. Observed behaviour: Read path splits: the file CDN (`images.shoutwiki.com`) answers plainly (observed: 200, 12,472 B, real PNG 150x150) while the API is Anubis-gated.

Evidence: `https://www.shoutwiki.com` (2026-10-21), record `dossier/storage/shoutwiki.json`.
Verdict: `qualifies-with-caveat`.

### CodeFloe (Forgejo, Hetzner Germany)

> 5 GB Git + 20 GB packages + 10 GB Git LFS + 10 GB attachments per account/organization; unlimited public and private repositories

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Single small operator on one Hetzner box.

Evidence: `https://codefloe.com` (2026-10-21), record `dossier/storage/codefloe.json`.
Verdict: `qualifies-with-caveat`.

### Fjord Commons (Forgejo)

> 5 GB per account; up to 25 repositories, public or private

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: 2000 minutes/month pooled across ALL of Comm. The record states no identity cost. Observed behaviour: Explicitly shared infrastructure on a single Hetzner box with nightly backups described as DR-only, not per-account restore.

Evidence: `https://fjord.sh/commons` (2026-10-21), record `dossier/storage/fjord-commons.json`.
Verdict: `qualifies-with-caveat`.

### GitLab.com container registry

> No published storage cap. Explicitly excluded from the per-project 10 GiB limit; unlimited container repositories per project is the practical reading

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: GitLab has run garbage-collection and cleanup-policy tooling against registries since 2023.

Evidence: `https://registry.gitlab.com` (2026-10-21), record `dossier/storage/gitlab-com-container-registry.json`.
Verdict: `qualifies`.

### GitLab.com generic package registry

> 5 GB maximum per uploaded file (Generic). No per-project or per-namespace package storage cap is documented; the package registry is explicitly excluded from the 10 GiB project storage limit

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GB per file. The record states no identity cost. Observed behaviour: Snippets, packages and job artifacts count toward *namespace* storage as a display/billing figure but are not enforced as a cap, enforcement is per-project on repo+LFS only.

Evidence: `https://gitlab.com` (2026-10-21), record `dossier/storage/gitlab-com-generic-package-registry.json`.
Verdict: `qualifies`.

### GitLab.com snippets

> No documented per-snippet storage cap; snippets are git-backed and unlimited in count, but contribute to namespace storage accounting

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Snippets are visible/searchable by other users when public.

Evidence: `https://docs.gitlab.com/user/snippets/` (2026-10-21), record `dossier/storage/gitlab-com-snippets.json`.
Verdict: `qualifies-with-caveat`.

### NeoNeko Git (Forgejo, open registration)

> No published storage quota. Site advertises 'no seat limits, no repository caps'; Forgejo ships quota disabled by default (quota.ENABLED=false, quota.default.TOTAL=-1 = unlimited), and this instance exposes no quota documentation

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Hobby instance run by one admin.

Evidence: `https://git.neoneko.org` (2026-10-21), record `dossier/storage/neoneko-git.json`.
Verdict: `qualifies-with-caveat`.

### Alibaba Cloud ACR Personal Edition

> Free of charge with count-based quotas and NO published byte quota: 'Personal Edition is designed for individual developers. It is in public preview and is free of charge: Image pull and push: free'. Quotas table: 'Namespace quota 3 |...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Shared multi-tenant backend.

Evidence: `https://www.alibabacloud.com/product/acr` (2026-10-21), record `dossier/storage/alibaba-cloud-acr-personal-edition.json`.
Verdict: `qualifies-with-caveat`.

### Amazon ECR Public

> 50 GB per month of always-free storage for public repositories: 'Both new and existing customers get 50 GB per month of always-free storage for their public repositories.' Past 50 GB it is not blocked, storage is billed to the repository...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Very stable.

Evidence: `https://gallery.ecr.aws` (2026-10-21), record `dossier/storage/amazon-ecr-public.json`.
Verdict: `qualifies-with-caveat`.

### Huawei Cloud SWR Basic Edition

> Free, and explicitly without a byte cap, the strongest storage wording of any registry checked: 'SWR is a free service, but some features (such as image scans and triggers) use other cloud services.' and 'No quotas are imposed on SWR...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Long-standing free tier with no storage meter, but Basic Edition has no tag management or batch retention, so cleanup is manual and slow.

Evidence: `https://www.huaweicloud.com/intl/en-us/product/swr/` (2026-10-21), record `dossier/storage/huawei-cloud-swr-basic-edition.json`.
Verdict: `qualifies`.

### Oracle Cloud Infrastructure Registry (OCIR)

> No registry fee at all, and storage is billed at raw Object Storage rates: 'Oracle does not charge separately for the service. Users pay only for the associated storage and network resources that they consume' / 'Customers pay only for...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Public pull works but the console is hidden from anonymous users.

Evidence: `https://www.oracle.com/cloud/cloud-native/container-registry/` (2026-10-21), record `dossier/storage/oracle-cloud-infrastructure-registry.json`.
Verdict: `fails-quota`.

### Tencent Cloud TCR Individual Edition

> Free, count-based only: 'The TCR Individual Edition is free of charge and can be activated directly.' Quotas: 'Number of image namespaces in a single region | 10', 'Number of image repositories in a single region | 500 in the Guangzhou...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 20 MB/s. The record states no identity cost. Observed behaviour: 'the image repository of TCR Individual Edition is shared with all other public cloud accounts, the images that have been pulled/pushed are blocked in the queue and are not displayed.

Evidence: `https://www.tencentcloud.com/products/tcr` (2026-10-21), record `dossier/storage/tencent-cloud-tcr-individual-edition.json`.
Verdict: `qualifies-with-caveat`.

### crates.io

> 10 MB per.crate file. No limit on versions per crate ('There is no limit to the number of versions which can be published'), no documented cap on total crates or total bytes per account

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `pull-count`: 1000 downloads/month. The record states no identity cost. Observed behaviour: Effectively permanent, 'the code cannot be deleted', 'publish is generally permanent'.

Evidence: `https://crates.io` (2026-10-21), record `dossier/storage/crates-io.json`.
Verdict: `qualifies-with-caveat`.

### GitLab Package Registry (generic / npm / Maven / PyPI / NuGet / Conan)

> Explicitly EXCLUDED from the project storage quota. GitLab docs, verbatim: 'GitLab projects have a storage limit for their Git repository and Large File Storage (LFS). Only the project's repository and LFS are included in the storage...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GB per file. The record states no identity cost. Observed behaviour: Package registry is a real feature not a cache, no TTL, but a project cleanup policy can auto-delete package assets if configured, so leave it off.

Evidence: `https://gitlab.com` (2026-10-21), record `dossier/storage/gitlab-package-registry.json`.
Verdict: `qualifies`.

### jsDelivr (npm + GitHub proxy CDN)

> No storage quota of its own, it is a *serving and permanence* layer over npm and GitHub, so the quota is whatever the origin package holds. Hard limits: packages >150 MB and (for GitHub) single files >20 MB are refused by default, raisable...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 20 MB per single GitHub file. The record states no identity cost. Observed behaviour: Retention is *stronger* than the origin: 'Previously served immutable files may be retained in permanent storage even after upstream deletion.

Evidence: `https://www.jsdelivr.com` (2026-10-21), record `dossier/storage/jsdelivr.json`.
Verdict: `qualifies`.

### npm public registry (registry.npmjs.org)

> No total storage quota, no per-account package cap ('Unlimited public packages', npm Pro page), no cap on versions per package. The only bounds are per-artefact and per-packument: empirically ~200 MB per tarball (no documented figure...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Append-only and durable, 2018 tarballs still serve with the original Last-Modified.

Evidence: `https://www.npmjs.com` (2026-10-21), record `dossier/storage/npm-public-registry.json`.
Verdict: `qualifies`.

### NuGet.org

> 250 MB per package. No documented total-storage quota and no documented cap on package count per account; organizations are free. Over 500k packages / petabytes-scale gallery in practice

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 250 MB per package. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: No deletion path means data does not vanish, good for archive.

Evidence: `https://www.nuget.org` (2026-10-21), record `dossier/storage/nuget-org.json`.
Verdict: `qualifies-with-caveat`.

### PyPI (Python Package Index)

> 100 MB per file, 10 GB per project, both are *defaults*, both are raisable by filing a GitHub issue. Unlimited number of projects. Verified in warehouse source: MAX_FILESIZE = 100 * ONE_MIB, MAX_PROJECT_SIZE = 10 * ONE_GIB,...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MB/file. The record states no identity cost. Observed behaviour: Deletion is permanent and irreversible ('cannot be undone without administrative intervention').

Evidence: `https://pypi.org` (2026-10-21), record `dossier/storage/pypi.json`.
Verdict: `qualifies`.

### RubyGems.org

> No documented per-gem size limit and no documented total quota, this is itself the finding: RubyGems publishes its rate limits and its acceptable-use policy but NOT a byte limit. Per-gem size is exposed per version via the API; large gems...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: The unknown size cap is the risk, the one public 413 report (qtbindings) shows a hard limit exists and is enforced at the proxy, and it is not documented anywhere.

Evidence: `https://rubygems.org` (2026-10-21), record `dossier/storage/rubygems-org.json`.
Verdict: `qualifies-with-caveat`.

### Docker Hub (free Personal plan, public repositories)

> Unlimited public repositories on the free Personal plan; NO documented storage cap on public repositories. Docker's own limits table lists only pull-rate and repository counts, with no storage row. Docker's Feb 2025 policy post says...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10GB per layer. The record states no identity cost. Observed behaviour: Storage is unpriced today but Docker reserves the right to add charges and has flip-flopped before (announced Mar 2025, cancelled Apr 2025).

Evidence: `https://hub.docker.com` (2026-10-21), record `dossier/storage/docker-hub.json`.
Verdict: `qualifies`.

### Quay.io public repositories (Red Hat)

> "We offer unlimited storage and serving of public repositories", Red Hat's own support article. Every paid plan is priced only by private-repo count and lists 'Unlimited public repos'; a free account gets unlimited public repos, private...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Hosted multitenancy means a noisy-neighbour throttle is possible but not documented.

Evidence: `https://quay.io` (2026-10-21), record `dossier/storage/quay-io-public-repositories.json`.
Verdict: `qualifies`.

### ttl.sh (anonymous ephemeral OCI registry)

> No account, no quota. "Free forever. Zero sign-up. Push any OCI artifact with a TTL." Storage is bounded only by the TTL, max advertised 24 hours

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 11 MB/s observed: 1. The record states no identity cost. Observed behaviour: Expiry is best-effort: the deployment repo states 'Tag expiry is handled separately and is not yet wired up in this repo', and open issue #151 reports images not expiring.

Evidence: `https://ttl.sh` (2026-10-21), record `dossier/storage/ttl-sh.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| AWS CodeArtifact | fails-quota | First 2 GB of storage and first 100,000 requests per month free, a recurring monthly allowance... |
| Azure Artifacts | fails-quota | 2 GiB free per ORGANIZATION (not per project, not per feed), then tiered per-GiB: 2, 10 GiB $2/GiB, 10, 100 GiB $1/GiB... |
| JFrog Artifactory Cloud, free tier (historically 2 GB) | fails-quota | 2 GB total storage + 10 GB/month data transfer on the legacy 'JFrog Free' cloud subscription... |
| Packagecloud.io, Free plan | fails-quota | 2 GB storage + 10 GB bandwidth per month, unlimited repositories and unlimited CI/CD minutes... |
| Freshdesk (helpdesk attachments) | trial-only | Freshworks support states flatly: 'There is no storage limit on the Freshdesk platform... |
| Intercom (article/Messenger attachments) | trial-only | 'The size limit on individual attachments is 100mb for uploads via Messenger and there is currently no limit on the number... |
| Zendesk Guide (help center article attachments) | trial-only | 'Each article has no limit on overall storage or total number of attached files.' Per-file 20 MB... |
| Radicle Garden (hosted seed) + permissionless public... | fails-quota | 5 GB of storage to start with on a Garden subscription ('talk to us if you need more')... |
| DigitalOcean Container Registry (DOCR), Starter | fails-quota | 'Starter is a free offering with a single registry and repository to let you try out DOCR.' Storage 500 MiB: table row... |
| Google Artifact Registry (incl. the gcr.io domain) | fails-egress | 0.5 GiB-month, once per billing account, shared across every project on it: 'Artifact Registry Storage / 0 gibibyte month... |
| IBM Cloud Container Registry (free plan) | fails-quota | 500 MB storage and 5 GB pull traffic per month: 'Amount of storage for images / 500 MB / Unlimited'... |
| OVHcloud Managed Private Registry (Harbor) | fails-quota | No free tier, three paid plans: 'S / 200 GiB / $0.027/hour / ~$19.71/month', 'M / 600 GiB / $0.0613/hour / ~$44.749/month'... |
| Scaleway Container Registry (public images) | fails-egress | Public images are free up to 75 GB of storage; private images are EUR 0.027/GB/month: 'Public images / Free up to 75GB /... |
| Anaconda.org (public conda channels) | fails-quota | 3 GB per free personal account. Anaconda staff on the official forum: 'You'll hit a hard limit at 10 GB with the default... |
| Maven Central (Sonatype Central Portal / Central... | fails-quota | No total storage quota, but as of 2026 a *monthly publishing quota per organization* on three metrics... |
| Alibaba Cloud ACR Enterprise Edition / OSS-backed... | fails-quota | Enterprise Edition stores artifacts in the customer's OSS bucket, so 'registry storage' is just OSS storage and is billed as OSS... |

The rejections here are mostly priced rather than closed, and the prices are small enough
that a reader will wonder why. Azure Artifacts gives 2 GiB free per organisation, then
charges tiered per GiB. AWS CodeArtifact gives 2 GB of storage and 100,000 requests per
month as a recurring allowance. Google Artifact Registry gives 0.5 GiB-month once per
billing account.

Those are all real registries with real interfaces. They miss a 500 GB floor by two
orders of magnitude, and they are recorded as `fails-quota` rather than dropped, because
a reader who thinks "a registry must be cheaper than a drive" will otherwise
repeat the same four checks.

The second group is `trial-only`, and it is the more dangerous one. A registry that gives a
monthly allowance resets rather than accumulating, so a plan that sizes against the first
month discovers the ceiling on the second.

## Chaining

A registry is a shard source behind a namespace layer. `git-annex` and DVC both address one
as a special remote, which is what makes an OCI registry usable without writing a client:
`git-annex` has an `rclone` special remote that speaks to any of these, and a `git-lfs`
special remote that will use any LFS host.

The pairing worth noting is a registry for the shards and Releases for the serving path.
They are different products on the same account, and the 10 GB layer limit against the 2 GiB
release asset limit means the shard size changes between them. A pool that mixes the two
must shard at the smaller number, or it must keep two manifests.
