# Forge surfaces: what a code forge stores besides code

A code forge is the cheapest place to put a large artefact, if its shape is accepted. Every
forge has three surfaces: the git repository itself, a release or package area that accepts
a large file, and a build artifact area that holds whatever a job produced. They have
different caps, different retention and different read paths, and a plan that treats "GitHub"
as one number will size the shard wrong.

This document covers 29 qualifying records: the three GitHub surfaces, the GitLab
equivalents, the git-annex and DVC adapters that turn any of them into a filesystem, and the
code forges that are their own ecosystem. 21 more were rejected.

## The comparison

Sorted by the class of surface: release and artifact surfaces first, then the LFS and
git-annex adapters, then the independent forges. A `*` in the identity column means the
value is read off the record's own prose.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| GitHub Actions Artifacts (public repositories) | Plan table still lists artifact storage 500 MB (Free) / 1 GB (Pro) / 2 GB... | retention-clamped: Retention: default 90 days | - | qualifies-with-caveat |
| GitHub Packages - public packages... | Unlimited for PUBLIC packages: 'GitHub Packages usage is free for public packages... | - | - | qualifies-with-caveat |
| GitHub Releases (release assets) | No total quota. Docs verbatim: 'Up to 1000 release assets may be associated with a... | per-object-cap: 2 GiB per file | - | qualifies |
| GitLab CI Job Artifacts (GitLab.com Free) | Not counted against the 10 GiB project storage limit... | retention-clamped: expiry 30 days, but `expire_in: never` i | - | qualifies-with-caveat |
| nightly.link (GitHub Actions artifact -> anonymous... | No quota of its own, it is a public-read proxy over GitHub Actions artifacts... | - | anonymous* | qualifies-with-caveat |
| Academic Torrents (tracker + index... | NO BYTE QUOTA ON THE INDEX, because the index is all they host: 'It's important to note... | per-object-cap: 10 MB for the | - | qualifies-with-caveat |
| CurseForge (Overwolf) author file hosting | No published total quota and no published per-file number that could be verified... | request-rate: not published | - | qualifies-with-caveat |
| Debian Salsa (salsa.debian.org) - GitLab with Generic... | No published total-storage quota, but a fully published per-object table on the... | per-object-cap: 5 GiB per Generic package file | - | qualifies-with-caveat |
| Framagit (framagit.org) - Framasoft's GitLab | No published total quota. Per-object table is published and slightly tighter than... | per-object-cap: 250 MiB CI artifacts (vs Salsa's 750 MiB), 5 GiB download file | - | qualifies-with-caveat |
| GNU Savannah download area... | No published byte quota found on any Savannah page - the hosting-requirements doc... | - | - | qualifies-with-caveat |
| Launchpad project file releases (+download area) | 1 GiB PER FILE in the project *file release* area - a separate... | per-object-cap: 1 GiB hard per release file | - | qualifies-with-caveat |
| ModDB / IndieDB (dbolical) file downloads | No published total quota, but a large installed base with published aggregate stats:... | per-object-cap: verified at least 8,442,728,905 bytes on a live file listing | - | qualifies-with-caveat |
| OSU Open Source Lab - FTP mirroring... | No published per-project quota, but an explicit capacity statement and an allocation... | - | - | qualifies-with-caveat |
| SourceForge File Release System... | NO PUBLISHED QUOTA. The Service Quotas page says verbatim: 'There are currently no... | per-object-cap: Individual files larger than 10 GB will not replicate out to... | - | qualifies |
| Azure DevOps Repos + Git LFS | No LFS storage quota is published and none is enforced in the docs... | - | - | qualifies |
| GitHub Git LFS | 10 GiB storage AND 10 GiB/month bandwidth on GitHub Free... | per-object-cap: Per-file: 2 GB | - | qualifies-with-caveat |
| GitLab.com Git LFS | 10 GiB free storage PER PROJECT on the Free tier... | - | - | qualifies-with-caveat |
| Hugging Face Storage Buckets via S3 gateway... | Public repos/buckets: 'Best-effort', no published numeric ceiling on a Free account... | - | - | qualifies-with-caveat |
| GitHub Container Registry (GHCR) via ORAS, known... | Container image storage and bandwidth are free: "Container image storage and bandwidth... | per-object-cap: 10 GB per layer | - | qualifies |
| jsDelivr as the free CDN layer over GitHub repos | Not storage, it is the egress answer for the serving workload: "there are no limits on... | per-object-cap: per file / 20 MB | - | qualifies-with-caveat |
| CNB (cnb.cool, Tencent Cloud Native Build... | Per top-level org, free tier per month: ' 100 GiB' + ' 100 GiB'... | per-object-cap: 64 GB per release/commit attachment... | anonymous | qualifies-with-caveat |
| FeijiPan (feijipan.com) `小飞机网盘` | Homepage: + '1024G, 1TB'. Baseline free space is small... | per-object-cap: 10 GB per file for free users ('10G10G') | country-phone | fails-egress |
| iLanzou (ilanzou.com) `蓝奏云优享版` | Free account starts at 10 GB; after phone/email verification it becomes 2 TB but only... | retention-clamped: 2 TB grant is 1 year, not permanent | email | qualifies-with-caveat |
| Gitea / Forgejo self-hosted with any S3 LFS backend | Unlimited by default: `quota.default.TOTAL = -1` means unlimited... | - | - | qualifies-with-caveat |
| DVC remotes (S3 / WebDAV / SSH / HTTP / Drive)... (self-hosted) | N/A, DVC ships no storage; the remote is whatever free store is configured... | - | - | qualifies-with-caveat |
| git-annex git-lfs special remote... (self-hosted) | N/A, a protocol adapter. Turns ANY git-lfs server (GitHub, GitLab, Bitbucket... | - | - | qualifies-with-caveat |
| git-annex rclone special remote... (self-hosted) | N/A, front-end to rclone's ~70 backends, so it inherits every free tier already... | - | - | qualifies |
| git-annex S3 special remote (backend-agnostic) (self-hosted) | N/A by itself, inherits whatever S3-compatible store it is pointed at... | - | - | qualifies |
| DataLad + git-annex workflow (orchestration layer) (self-hosted) | N/A, DataLad is a wrapper over git-annex... | - | - | qualifies-with-caveat |

## What the class is

A forge is a store whose write path is a tool already present. That is the whole value: no
new API, no new credential, and `git push` or a release upload does the work. The cost is
that the forge's caps are set for source code, and source code is small.

Three surfaces, three behaviours.

**Releases** take a large file and hold it forever. GitHub's docs state "Up to 1000 release
assets may be associated with a single release. Each file included in a release must be
under 2 GiB. There is no limit on the total size of a release, nor bandwidth usage"
(`documented`, 2026-10-22: 200, 3,494 B). That is 1.95 TiB per release and unlimited releases.

**Packages** take a smaller file and hold it for the life of the package. GitHub Packages is
free for public packages and states that data transferred in from any source is free.

**Artifacts** take whatever a job produced and delete it on a clock. GitHub Actions artifacts
are capped at 90 days and the storage pool is shared with Packages.

## The serving tier, and the token cache

This is the most operationally important finding in the document.

1 TiB per day at 2 GiB per asset is 512 full-asset fetches per day, which is trivial. The
binding term is the API call count, and only if a token is minted per client request.

Design A, resolve the SAS once per hour per asset and cache the bytes at the edge, fails on
the second clause: a 2 GiB asset cannot be edge-cached. Cloudflare's Workers limits page
states "Cloudflare does not enforce response body size limits. CDN cache limits apply:
512 MB for Free, Pro, and Business plans, and 5 GB for Enterprise"
(`documented`, 2026-10-22: 200, 27,086 B). A 2 GiB asset is four times the free-plan cache
object cap, so no TTL makes it cacheable.

Design B, resolve per client request with no caching, uses 5,000 requests per hour at one
request per second, which is 72% of the limit and dies at about 1.4 requests per second.

The design that survives is a token cache, not a body cache. Hold the resolved SAS in KV or
D1 keyed by asset, refresh it when the `se` field is within five minutes of expiry, and
stream the body through uncached. That is 512 resolves per day, about 24 per hour, which is
0.5% of the limit. A probe decoded the SAS window: `skt` at 02:09:45Z and `se`
at 03:10:37Z, which is 3,652 seconds, or 60.9 minutes (`inferred`, 2026-10-22).

The failure to design against is a mid-stream expiry, so re-resolution must be proactive
rather than triggered by a 404. A ranged read does work at the origin: the same probe
returned `302` followed by `206 Partial Content` with
`Content-Range: bytes 0-1023/13149392`.

## The adapters, and why they are the real finding

Six records in this document are not providers at all. They are adapters, and they are what
makes the rest of the corpus addressable as one store. They carry a dossier because each one
is a mechanism with a documented behaviour and a failure mode, and they do not enter a
provider count.

`git-annex` has an `rclone` special remote built in since 2023, so it inherits about 70
backends including every free tier in this topic. It also has a `git-lfs` special remote, so
any LFS host becomes an annex target, and an `s3` special remote, so any free S3 endpoint
becomes one. DataLad is a wrapper over annex that makes a dataset plus N special remotes
reproducible.

The consequence is worth stating plainly: a deployment does not need a provider that speaks
git-annex. It needs one that speaks S3 or LFS, and annex adapts it. That is why the
registries document and this one overlap in practice and not in principle.

## The independent forges

SourceForge is the best of them and it states its position: "There are currently no fixed
capacity limits around usage of our services", with a soft 10 GB per file and a phone PIN as
the write gate (`documented`, 2026-10-22: 200, 3,189 B). Its File Release System is mirrored,
and a mirror returned 206 on a ranged read.

Debian Salsa and Framagit publish a per-object table and no total quota. Salsa takes 5 GB per
generic package; Framagit caps an attachment at 12 MiB, an import at 300 MiB and a job
artifact at 250 MiB, which is tighter than Salsa on every row.

GNU Savannah, Launchpad's release area and OSU Open Source Lab are mirrors rather than
stores: each requires a purpose the host accepts, and OSU states that space on the main
mirrors is limited.

## The forge found through a Chinese forum

CNB at `cnb.cool` gives 100 GiB of repository storage and 100 GiB of object storage per
top-level organisation per month, free, with 160 build-CPU hours. It is the one record here
whose quota is stated in a language the English search never reaches, and its write gate is a
WeChat identity, which makes it `fails-identity` on everything except the
build path.

The two records beside it, FeijiPan and iLanzou, are Chinese pan drives whose home is
`netdisk-pan`; they stay here rather than being silently reclassified.

### GitHub Actions Artifacts (public repositories)

> Plan table still lists artifact storage 500 MB (Free) / 1 GB (Pro) / 2 GB (Team) / 50 GB (Enterprise), and that pool is SHARED with GitHub Packages. Billing docs state Actions usage is free for public repositories. Artifact storage for...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: Retention: default 90 days. The record states no identity cost. Observed behaviour: Hard TTL, artifacts are deleted at expiry and cannot be restored.

Evidence: `https://github.com/features/actions` (2026-10-21), record `dossier/storage/github-actions-artifacts.json`.
Verdict: `qualifies-with-caveat`.

### GitHub Packages - public packages (npm/Maven/NuGet/RubyGems)

> Unlimited for PUBLIC packages: 'GitHub Packages usage is free for public packages. In addition, data transferred in from any source is free.' Private packages consume the shared 500 MB/2 GB/50 GB plan pool

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Immutable versions.

Evidence: `https://github.com/features/packages` (2026-10-21), record `dossier/storage/github-packages-public-packages.json`.
Verdict: `qualifies-with-caveat`.

### GitHub Releases (release assets)

> No total quota. Docs verbatim: 'Up to 1000 release assets may be associated with a single release. Each file included in a release must be under 2 GiB. There is no limit on the total size of a release, nor bandwidth usage.' Per-file...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 2 GiB per file. The record states no identity cost. Observed behaviour: Very stable.

Evidence: `https://github.com` (2026-10-22), record `dossier/storage/github-releases.json`.
Verdict: `qualifies`.

### GitLab CI Job Artifacts (GitLab.com Free)

> Not counted against the 10 GiB project storage limit ('build artifacts are not included in the limit'). 1 GB compressed maximum per artifact archive on GitLab.com

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: expiry 30 days, but `expire_in: never` i. The record states no identity cost. Observed behaviour: Expiry is enforced hourly and irreversible, anything not pinned with `never`/Keep silently vanishes.

Evidence: `https://gitlab.com` (2026-10-21), record `dossier/storage/gitlab-ci-job-artifacts.json`.
Verdict: `qualifies-with-caveat`.

### nightly.link (GitHub Actions artifact -> anonymous URL wrapper)

> No quota of its own, it is a public-read proxy over GitHub Actions artifacts, which are themselves uncounted for public repos but capped at 90-day retention. Service is 'provided totally free of charge'

That is the record's own wording (`reported`, 2026-10-21). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Single-maintainer free service, a single point of failure if a project depends on the hosted instance.

Evidence: `https://nightly.link` (2026-10-21), record `dossier/storage/nightly-link.json`.
Verdict: `qualifies-with-caveat`.

### Academic Torrents (tracker + index, with optional donor mirroring)

> NO BYTE QUOTA ON THE INDEX, because the index is all they host: 'It's important to note that we don't directly host your data. However, we manage a network of donated servers. When you upload a torrent file to our site, hosting nodes...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 MB for the. The record states no identity cost. Observed behaviour: The fatal caveat: without a donor node or a webseed, an entry is a pointer to nothing.

Evidence: `https://academictorrents.com` (2026-10-21), record `dossier/storage/academic-torrents.json`.
Verdict: `qualifies-with-caveat`.

### CurseForge (Overwolf) author file hosting

> No published total quota and no published per-file number that could be verified this session - the author docs, the ideas board and the support KB were all behind SSO or Cloudflare. What IS verifiable is the observed size distribution:...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: not published. The record states no identity cost. Observed behaviour: Reads are hotlink-gated (403 from S3 on constructed URLs) and the whole author surface is SSO-walled, so this is the least auditable of the game hosts.

Evidence: `https://www.curseforge.com` (2026-10-21), record `dossier/storage/curseforge-author-file-hosting.json`.
Verdict: `qualifies-with-caveat`.

### Debian Salsa (salsa.debian.org) - GitLab with Generic package registry

> No published total-storage quota, but a fully published per-object table on the instance-configuration page. Package registry per-file caps: Generic 5 GiB, Conan 3 GiB, Maven 3 GiB, PyPI 3 GiB, Terraform 1 GiB, npm/NuGet 500 MiB, Helm 5...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GiB per Generic package file. The record states no identity cost. Observed behaviour: Manual registration review is the whole story - it converts account-farming from an API call into a queue observed in days.

Evidence: `https://salsa.debian.org` (2026-10-21), record `dossier/storage/debian-salsa-gitlab-with-generic-package-registry.json`.
Verdict: `qualifies-with-caveat`.

### Framagit (framagit.org) - Framasoft's GitLab

> No published total quota. Per-object table is published and slightly tighter than Salsa: max attachment 12 MiB, import 300 MiB, job artifact 250 MiB, page 250 MiB, snippet 50 MiB, import remote file 10 GiB, download file 5 GiB. Registry:...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 250 MiB CI artifacts (vs Salsa's 750 MiB), 5 GiB download file. The record states no identity cost. Observed behaviour: Registration sits behind an Anubis proof-of-work wall ('Making sure you're not a bot!', Anubis v1.28.2, modified by Framasoft) - so signup is not scriptable at all.

Evidence: `https://framagit.org` (2026-10-21), record `dossier/storage/framagit-framasoft-s-gitlab.json`.
Verdict: `qualifies-with-caveat`.

### GNU Savannah download area (download.savannah.gnu.org /.nongnu.org)

> No published byte quota found on any Savannah page - the hosting-requirements doc speaks only in terms of purpose ('The space given to you on this server is given for the expressed purpose of advancing free software') and permanence ('Our...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Two real breakages.

Evidence: `https://savannah.gnu.org` (2026-10-21), record `dossier/storage/gnu-savannah-download-area.json`.
Verdict: `qualifies-with-caveat`.

### Launchpad project file releases (+download area)

> 1 GiB PER FILE in the project *file release* area - a separate, much smaller surface than the PPA. The manual says: 'Each individual file must be no more than 1 GiB and you must be the: project maintainer / project driver / or the series...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1 GiB hard per release file. The record states no identity cost. Observed behaviour: Read path verified working end-to-end (303 -> launchpadlibrarian.net -> 200, 419,427 bytes).

Evidence: `https://launchpad.net` (2026-10-21), record `dossier/storage/launchpad-project-file-releases.json`.
Verdict: `qualifies-with-caveat`.

### ModDB / IndieDB (dbolical) file downloads

> No published total quota, but a large installed base with published aggregate stats: the downloads index reports 149,920 files totalling 43,307.57 GB and 387,395,913 downloads. Mean file size is therefore ~296 MB, and the tail is much...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: verified at least 8,442,728,905 bytes on a live file listing. The record states no identity cost. Observed behaviour: The whole domain is hostile to programmatic access right now: www.moddb.com and www.indiedb.com returned 503 to read.web.pkgforge.dev, the raw fetch proxy AND direct curl, and 403 on /downloads/start/<id>.

Evidence: `https://www.moddb.com` (2026-10-21), record `dossier/storage/moddb-indiedb-file-downloads.json`.
Verdict: `qualifies-with-caveat`.

### OSU Open Source Lab - FTP mirroring (ftp.osuosl.org / ftp2.osuosl.org)

> No published per-project quota, but an explicit capacity statement and an allocation policy: 'Because space on the main mirrors is limited, we also host projects on ftp2.osuosl.org. It runs in Salem and stores its content on our Ceph...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Human-gated and OSS-only in practice (the form asks for a source code repository and a role such as maintainer).

Evidence: `https://osuosl.org` (2026-10-21), record `dossier/storage/osu-open-source-lab-ftp-mirroring.json`.
Verdict: `qualifies-with-caveat`.

### SourceForge File Release System (FRS) + project web space

> NO PUBLISHED QUOTA. The Service Quotas page says verbatim: 'There are currently no fixed capacity limits around usage of our services. In lieu of specific disk usage caps (quotas), we may contact projects if they are using significant...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: "Individual files larger than 10 GB will not replicate out to our mirrors".... The record states no identity cost. Observed behaviour: The only fragile part is the soft quota: 20-30 GB 'may be permissible' means a project that grows to hundreds of GB gets an email.

Evidence: `https://sourceforge.net` (2026-10-21), record `dossier/storage/sourceforge-file-release-system-project-web-space.json`.
Verdict: `qualifies`.

### Azure DevOps Repos + Git LFS

> No LFS storage quota is published and none is enforced in the docs. Microsoft states plainly: 'Azure DevOps Services fully supports Git LFS and offers it for free.' The free tier is 5 Basic users with unlimited private Git repos; only...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: The 250 GB repo figure is guidance, not a wall.

Evidence: `https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/` (2026-10-21), record `dossier/storage/azure-devops-repos-git-lfs.json`.
Verdict: `qualifies`.

### DataLad + git-annex workflow (orchestration layer)

> N/A, DataLad is a wrapper over git-annex; quota is the special remote's. Its value here is that it makes 'dataset + N special remotes + reproducible publish' a supported, documented workflow instead of hand-written annex commands

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Used in production by academic consortia (OpenNeuro etc.) precisely for multi-TB datasets on donated storage, the most battle-tested 'big dataset on free/cheap stores' pattern that exists.

Evidence: `https://handbook.datalad.org/en/latest/basics/101-139-s3.html` (2026-10-21), record `dossier/storage/datalad-git-annex-workflow.json`.
Verdict: `qualifies-with-caveat`.

### DVC remotes (S3 / WebDAV / SSH / HTTP / Drive) pointed at free backends

> N/A, DVC ships no storage; the remote is whatever free store you configure. Free-tier bytes = the backing store's bytes. Supports Amazon S3 + S3-compatible (MinIO etc. via `endpointurl`), Azure Blob, GCS, Google Drive, Aliyun OSS,...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: DVC is an ML-tooling project (treeverse).

Evidence: `https://doc.dvc.org/user-guide/data-management/remote-storage` (2026-10-21), record `dossier/storage/dvc-remotes-pointed-at-free-backends.json`.
Verdict: `qualifies-with-caveat`.

### git-annex git-lfs special remote (annex over any LFS host)

> N/A, a protocol adapter. Turns ANY git-lfs server (GitHub, GitLab, Bitbucket, a self-hosted Gitea) into an annex special remote, so the LFS host's quota applies but annex adds hash-verified partial clone and `whereis` across mirrors

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Cannot delete = every mistake is permanent on the LFS side, and the host's month-storage accounting (GitHub) means the bytes keep counting against quota.

Evidence: `https://git-annex.branchable.com/special_remotes/git-lfs/` (2026-10-21), record `dossier/storage/git-annex-git-lfs-special-remote.json`.
Verdict: `qualifies-with-caveat`.

### git-annex rclone special remote (built into annex since 2023)

> N/A, front-end to rclone's ~70 backends, so it inherits every free tier already catalogued by the other C-slots. The docs' own list (still current) names Drive, OneDrive, Dropbox, Mega, pCloud, Box, Yandex, Jottacloud, WebDAV, FTP, SFTP,...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Solid.

Evidence: `https://git-annex.branchable.com/special_remotes/rclone/` (2026-10-21), record `dossier/storage/git-annex-rclone-special-remote.json`.
Verdict: `qualifies`.

### git-annex S3 special remote (backend-agnostic)

> N/A by itself, inherits whatever S3-compatible store you point it at. This is the multiplier: any free S3 endpoint (Internet Archive s3.us.archive.org, HF s3.hf.co, Oracle/Cloudflare-adjacent object tiers, MinIO on a free VM) becomes a...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Mature and boring, the special remote has existed for over a decade.

Evidence: `https://git-annex.branchable.com/special_remotes/S3/` (2026-10-21), record `dossier/storage/git-annex-s3-special-remote.json`.
Verdict: `qualifies`.

### Gitea / Forgejo self-hosted with any S3 LFS backend

> Unlimited by default: `quota.default.TOTAL = -1` means unlimited, and the soft-quota feature is 'currently not yet enabled by default'. You supply the disk/object store, so bytes = your infrastructure

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Quota feature is explicitly 'still in development' with 'little support for early prevention of operations in the UI'.

Evidence: `https://forgejo.org/docs/latest/admin/advanced/quota/` (2026-10-21), record `dossier/storage/gitea-forgejo-self-hosted-with-any-s3-lfs-backend.json`.
Verdict: `qualifies-with-caveat`.

### GitHub Git LFS

> 10 GiB storage AND 10 GiB/month bandwidth on GitHub Free (also 10/10 on Pro and Free-for-orgs; 250 GiB each on Team/Enterprise Cloud). This is UP from the old 1 GiB/1 GiB, the docs now show a 10 GiB table. Pre-paid data packs are gone; it...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Per-file: 2 GB. The record states no identity cost. Observed behaviour: Hard-blocked (not billed) without a payment method, so it degrades safely.

Evidence: `https://github.com/pricing` (2026-10-21), record `dossier/storage/github-git-lfs.json`.
Verdict: `qualifies-with-caveat`.

### GitLab.com Git LFS

> 10 GiB free storage PER PROJECT on the Free tier, and that 10 GiB explicitly covers 'the project's repository and Large File Storage (LFS)'. Premium/Ultimate: 500 GiB per project. CONFIRMED: LFS is IN the quota while containers, packages,...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Read-only state is reversible only by purchasing storage, so a blown project is stuck.

Evidence: `https://gitlab.com` (2026-10-21), record `dossier/storage/gitlab-com-git-lfs.json`.
Verdict: `qualifies-with-caveat`.

### Hugging Face Storage Buckets via S3 gateway (s3.hf.co), as an annex/DVC backend

> Public repos/buckets: 'Best-effort', no published numeric ceiling on a Free account (private is a hard 100 GB). Storage plans table: Free user or org = Public 'Best-effort', Private 100 GB. HF is on the known list, but the S3 gateway is...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Free public storage is explicitly 'best-effort', and HF says 'Beyond the first few gigabytes, please use this resource responsibly'. The page describes its mitigation as 'in place to prevent abuse', which is a limit on excess use.

Evidence: `https://huggingface.co/docs/hub/storage-buckets-s3` (2026-10-21), record `dossier/storage/hugging-face-storage-buckets-via-s3-gateway-as-an-annex.json`.
Verdict: `qualifies-with-caveat`.

### GitHub Container Registry (GHCR) via ORAS

> Container image storage and bandwidth are free: "Container image storage and bandwidth for the Container registry is currently free. If you use Container registry, you'll be informed at least one month in advance of any change to this...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 10 GB per layer. The record states no identity cost. Observed behaviour: Anonymous pull verified end-to-end.

Evidence: `https://ghcr.io` (2026-10-21), record `dossier/storage/github-container-registry-via-oras-known-numbers-re-veri.json`.
Verdict: `qualifies`.

### jsDelivr as the free CDN layer over GitHub repos

> Not storage, it is the egress answer for the serving workload: "there are no limits on bandwidth or number of requests" (AUP section 1), with soft limits of 10,000 actively accessed files and 100,000 files per repository

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: per file | 20 MB. The record states no identity cost. Observed behaviour: Immutable: 'Previously served immutable files may be retained in permanent storage even after upstream deletion', deletion upstream does not remove it from jsDelivr.

Evidence: `https://www.jsdelivr.com` (2026-10-21), record `dossier/storage/jsdelivr-as-the-free-cdn-layer-over-github-repos.json`.
Verdict: `qualifies-with-caveat`.

### CNB (cnb.cool, Tencent Cloud Native Build, community edition)

> Per top-level org, free tier per month: ' 100 GiB' + ' 100 GiB' (object storage covers 'LFS '), plus 160 build-CPU core-hours and 1600 dev-CPU core-hours. Over-quota is metered at CNY 1/GiB/month, and storage is billed on daily average...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 64 GB per release/commit attachment (provider's own plugin README: ' 64GB '). A new account costs anonymous. Observed behaviour: Community edition launched public beta 2025-08.

Evidence: `https://cnb.cool` (2026-10-21), record `dossier/storage/cnb.json`.
Verdict: `qualifies-with-caveat`.

### FeijiPan (feijipan.com)

> Homepage: + '1024G, 1TB'. Baseline free space is small; the 1 TB comes from the developer-signing programme. Their own blog: '2T'; VIP 10T / SVIP 15T

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 GB per file for free users ('10G10G'). A new account costs country-phone. Observed behaviour: the provider closes accounts that use it from a server. The most-used parser project warns of frequent account closures and IP-blocks for server-side use.

Evidence: `https://www.feijipan.com` (2026-10-21), record `dossier/storage/feijipan.json`.
Verdict: `fails-egress`.

### iLanzou (ilanzou.com)

> Free account starts at 10 GB; after phone/email verification it becomes 2 TB but only for 1 year (' 2T 1'). Paid 10 TB at CNY 9/mo or CNY 88/yr

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: 2 TB grant is 1 year, not permanent. A new account costs email. Observed behaviour: Two-tier product (classic vs) with repeated policy narrowing, IT reported APK sharing moved behind the CNY 9/mo paywall.

Evidence: `https://www.ilanzou.com` (2026-10-21), record `dossier/storage/ilanzou.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| CircleCI artifacts | fails-quota | No storage quota advertised on Free (30,000 credits/month). Artifact retention default AND maximum is 30 days on Cloud... |
| Codemagic artifacts | fails-quota | 500 free build minutes/month on macOS M2 (individuals). No free storage allowance advertised... |
| CPAN / PAUSE (pause.perl.org) | fails-quota | No published byte quota, and the empirical evidence points to a tight request-body limit rather than a documented number: a... |
| Game Jolt game builds | fails-quota | 3 GB TOTAL PER GAME, not per file. The 3 GB number is corroborated three ways observed: the official 9-year-old changelog... |
| GitGud (gitgud.io) - GitLab instance | fails-quota | unverified: blocked by challenge. The origin returned HTTP 403 through the fetch proxy... |
| Bitbucket Cloud Git LFS | fails-quota | Free (up to 5 users): 1 GB LFS storage. Academic 5 GB, Standard 5 GB... |
| Codeberg (Forgejo) Git LFS | fails-quota | 750 MiB git repository storage + 'Additional 1.5 GiB' for 'LFS, Packages, Releases... |
| Git LFS | fails-quota | Free: 10 GiB storage AND 10 GiB bandwidth per month; per-file 2 GB on Free/Pro, 4 GB Team, 5 GB Enterprise |
| Git-tracked repo files (direct... | fails-quota | 100 MiB hard per file ('GitHub blocks files larger than 100 MiB')... |
| GitHub Actions dependency cache | fails-quota | "the limit is 10 GB per repository" by default (configurable up to 10 TB for user-owned repos... |
| GitHub Pages (Fastly-served, 1 GB site) | fails-quota | "Published GitHub Pages sites may be no larger than 1 GB"... |
| Chaoxing Cloud (pan-yz.chaoxing.com) + (`超星云盘超星小组盘`) | fails-quota | 100 GB free per account (was 150 GB before a reduction; one vendor page still advertises '150G'). Per-file: 1 GB on web... |
| Doubao Drive (ByteDance; storage provided by)... | fails-quota | Contractual language is deliberately unquantified:. Reported reality: legacy users 100 GB, new users 10 GB... |
| Huawei Cloud Space `华为云空间` | fails-quota | About 5 GB free; ~CNY 6/month for more. Device-backup oriented |
| LeCloud (lecloud.lenovo.com) (`联想乐云`) | fails-quota | 5 GB base. '5GB71200GB'. Membership adds 20 GB per tier via sign-in activities |
| MediaTrack (app.mediatrack.cn) (`分秒帧`) | fails-quota | Free personal plan: 10 GB storage, 5 members per project... |
| Nutstore (jianguoyun.com) (`坚果云`) | fails-quota | Traffic-based, not capacity-based: '1GB3GB'. Space grows with what is uploaded and is bounded by the traffic allowance... |
| Tencent Weiyun `腾讯微云` | fails-quota | About 10 GB free; paid ~CNY 10/month. Massively downgraded from the 10 TB free era |
| UPYUN USS (Storage Service) (`又拍云`) | fails-egress | No standing free tier. Free capacity comes from (a) a 7-day trial with no storage/traffic cap... |
| WenShuShu (wenshushu.cn) `文叔叔` | fails-quota | 40 GB free drive space. Own site: ' 40GB'. Per-file: 5 GB ('5GB'). No login needed to send; login needed to keep |
| WoPan (pan.wo.cn, China Unicom) (`联通云盘沃盘`) | fails-quota | 60 GB free, raised from 10 GB by a 2025-09-01->15 promotion that was made permanent... |

The failures here are almost all quota, and the numbers are small enough to be surprising.
Codeberg caps at 750 MiB of git plus 1.5 GiB combined for LFS, packages, releases and
attachments. GitHub Packages' npm registry caps a tarball at 256 MB and does not fall under
the public-package carve-out. SourceHut has no Git LFS support at all and asks projects to
stay under 6 GiB.

The second group is `not-storage`, and it contains the shims: Travis CI artifacts upload to
a bucket the project owns, so Travis provides no storage; a nightly link is a proxy over an artifact
that a forge already holds; and an academic torrent tracker hosts an index rather than bytes.

## Chaining

The forge is the serving tier of a free composition and the adapter is what makes it
addressable.

The pairing that works is Releases for serving and Packages or a registry for shards,
because they are different products on one account with different caps: 2 GiB per asset
against 10 GB per layer. Shard at the smaller number or keep two manifests.

The pairing that does not work is two surfaces that share a quota. GitHub's artifact storage
pool is shared with Packages, so a build that fills the artifact pool has consumed the
package budget, and nothing in either page says so.
