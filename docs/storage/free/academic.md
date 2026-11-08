# Academic repositories: which open-science deposit accepts an unaffiliated depositor, and what its ceiling really is

An academic repository is the largest free allowance in this topic that does not require an
institution, and almost all of them are free at the point of deposit. The question a reader
arrives with is therefore not "how much" but "which door is open", and the two are
independent: the quota is a software feature and the door is an institutional policy.

This document covers 33 qualifying records across generalist repositories, domain
science archives, preprint and data services, and the grant programmes that pay for storage
as a project expense. 20 were rejected, and the reason is almost always identity.

The sibling document [`academic-identity.md`](academic-identity.md) carries the Dataverse and
DSpace sweep, which is the systematic test of that independence.

## The comparison

Sorted by ceiling, with the repositories that publish no ceiling after those that do. A `*`
in the identity column means the value is read off the record's own prose.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| DesignSafe-CI Data Depot (NSF NHERI / TACC) - no... | No published cap on published dataset size or file count: 'right now there is no limit... | write-gated: twice: a TACC account (free... | email | qualifies-with-caveat |
| Emergent Ventures (Mercatus Center) - 13+, worldwide... | Open-budget microgrant: no fixed cap. Third-party trackers report a $1k-$50k typical... | - | email | qualifies-with-caveat |
| GBIF IPT via a data-hosting centre - free email... | No quota published anywhere: a data-hosting centre gives a depositor an account on its IPT... | - | email | qualifies-with-caveat |
| Harvard Dataverse Repository - per-collection quota... | 1 TB per Dataverse Collection allocation... | per-object-cap: per-file 2.5 GB | email | qualifies |
| NLnet / Restack Fund - the grant an unaffiliated... | EUR 5,000-50,000 for a first grant, and storage is a claimable project expense rather... | - | email | qualifies-with-caveat |
| Science Data Bank (ScienceDB... | 1 TB per dataset and 2,000 files per dataset, with no per-user or per-account cap... | per-object-cap: 1 TB per dataset | email | qualifies |
| Shuttleworth Foundation Fellowship - individual... | Fellowship covers the Fellow's time for a year plus project funding reported at... | - | email | qualifies-with-caveat |
| Source Cooperative (re-verify) - uncapped public... | No published byte cap: 'allowing trusted organizations and individuals to publish data... | - | email | qualifies-with-caveat |
| BioStudies / ArrayExpress (EMBL-EBI) | Free deposit, no published cap. 'Is there a cost to deposit data in BioStudies? No... | per-ip-shaping: 1 stream 7 KB/s, 16 parallel 25 KB/s against the EBI FTP edge | - | qualifies |
| ENA (European Nucleotide Archive), Webin | No fixed quota. Own fair-use policy: 'We place no absolute limit within the 2-month... | per-ip-shaping: single stream 45 KB/s, 8 parallel ranged GETs 430 KB/s (9 | - | qualifies |
| Mendeley Data (Elsevier) | 10 GB per dataset for free individual accounts... | per-object-cap: 10 GB per dataset | - | fails-quota |
| MorphoSource | 'MorphoSource is able to subsidize or support free contribution of data for most users... | - | - | fails-quota |
| NCBI GEO | No published volume cap; raw sequence data is redirected to SRA... | per-object-cap: not stated (defer to SRA for raw reads) | anonymous* | qualifies-with-caveat |
| NCBI SRA, with anonymous read via AWS Open Data | No per-account quota published. Submission is genuinely bulk: FTP... | per-ip-shaping: from S3, not a storage cap | - | qualifies |
| NeuroVault | Free, no published per-file or per-account cap found on the site or FAQ (silence... | per-object-cap: unstated | - | qualifies-with-caveat |
| OpenNeuro | Free, no published per-dataset or per-account cap... | per-ip-shaping: but weak | - | qualifies |
| PANGAEA (Data Publisher for Earth & Environmental... | Free to publish ('PANGAEA can be used free of charge'... | per-object-cap: Individual files must be less than 15 GB in size | - | qualifies-with-caveat |
| Synapse (Sage Bionetworks) | No clear public storage cap found. Platform is free SaaS on S3... | - | - | qualifies-with-caveat |
| TCIA (The Cancer Imaging Archive) | Free. 'We do not charge a fee for sharing your data through TCIA except in rare... | per-object-cap: one zip per DICOM series (tens of MB each) | anonymous* | qualifies-with-caveat |
| B2SHARE (EUDAT) | 20 GB per record, 10 GB per file, and explicitly unlimited records and unlimited files | per-object-cap: 10 GB per file | - | qualifies-with-caveat |
| DANS Data Stations (ssh.datastations.nl / DataverseNL) | 9.3 GB maximum per file, no per-dataset or per-collection quota configured... | per-object-cap: 9.3 GB per file | - | fails-identity |
| Harvard Dataverse | 1 TB of storage, free, for 'All researchers from any discipline... | per-object-cap: 2.5 GB per file | - | qualifies |
| HydroShare (CUAHSI) | 20 GB automatic on account creation, with an increase process that is explicitly... | write-gated: on the increase (email a human), and the quota is small by default | email | fails-quota |
| IEEE DataPort, Data Competition module... | 2 TB per dataset for individual users, 10 TB for Institutional Subscribers... | write-gated: + read-gated, and the gate differs by route | email | fails-egress |
| Kaggle Models (distinct from Kaggle Datasets) | 200 GB for private models, alongside 200 GB for private datasets... | per-object-cap: 200 GB and 50 top-level files per dataset | email | qualifies-with-caveat |
| Mozilla Data Collective (MDC) | 150 GB per uploaded file, raised from a lower value in the Python SDK on 2026-03-24... | write-gated: hard | email | qualifies-with-caveat |
| Nebula Block, Standard object storage tier... | No storage quota on the Standard tier, it is priced at $0/GB/month by design:... | - | card | qualifies-with-caveat |
| ScienceDB (Science Data Bank, CAS / CNIC)... | No data-volume limit. A 2025 peer-reviewed comparison of Zenodo and ScienceDB in... | write-gated: by 'formal review' of upload completeness | email | qualifies-with-caveat |
| Source Cooperative (source.coop / data.source.coop)... | No published byte quota; the org states it 'hosts over 5 petabytes of data' across 330+... | write-gated: publishing data requires applying to be a beta tester' via a... | email | qualifies-with-caveat |
| CaltechDATA (InvenioRDM, California Institute of... | 1 TB of free storage per user, announced 2026-06-26... | - | - | fails-identity |
| OSF (Open Science Framework), per-component quotas | 50 GB per public project, 5 GB per private project, 5 GB per file... | per-object-cap: 5 GB per file | - | qualifies-with-caveat |
| Recherche Data Gouv (French national Dataverse) | 50 GB max per file via the deposit interface... | per-object-cap: 50 GB max per file | - | fails-identity |
| Zenodo anonymous download throughput... | n/a, this entry records the observed read path for the 500GB-1TiB/day serving workload | - | - | qualifies |

## What the class is

Four kinds of institution share this document and they differ in what they will accept.

**A generalist repository** takes any discipline. Zenodo, B2SHARE, Harvard Dataverse,
Borealis and OSF are the members, and their quotas range from 20 GB per record to a per
collection allocation of 1 TiB.

**A domain repository** takes data of one kind, and that is why its ceiling is often absent.
ENA takes nucleotide sequences and states no fixed quota because the submission volume of a
sequencing centre is not a number anyone can cap. NCBI SRA redirects raw reads to itself.
PANGAEA takes earth and environmental data.

**A preprint or data service** carries a file alongside a paper. Mendeley Data gives 10 GB
per dataset, IEEE DataPort 2 TB per dataset through one route, Mozilla Data Collective 150 GB
per file.

**A grant programme** is not storage at all. It pays for storage as a line item, and it is
in this document because it is the only route to a paid tier that does not involve paying.

## The one thing that decides it

The phrase to search for on a deposit help page is "outside institution". It separates the
repositories that take an email address from the federated ones that take a Shibboleth
identity, and it is the fastest test available. Harvard takes anyone. DataverseNO, DaRUS and
all nine RODBUK sites take only their own institutions, and they run the same software.

The structural finding underneath it: 83 of 149
registered Dataverse installations report no quota at all, and DSpace has no quota concept in
its 2,125-line configuration file. **Storage is almost never the constraint in this layer.
The account is.**

## Harvard Dataverse, and what the 1 TiB actually is

The support page says all researchers inside and outside Harvard can deposit files of up to
2.5 GB and store up to 1 TB. The 2024 Large Data Services document describes a free support
edge of 1.0 TB for non-Harvard researchers and 2.5 TB for affiliates, with paid services above
those figures.

So 1 TiB is a support threshold rather than a platform quota: it is where Harvard starts
charging, not where uploads stop. The enforcement surface is a per-collection quota that is
off by default and experimental. Three probes on 2026-10-22 settle what exists:

| endpoint | response |
|---|---|
| `/api/dataverses/harvard/storage/quota` | `No quota defined for this collection`, 73 B |
| `/api/dataverses/SEE_Precursors/storage/quota` | `Total quota allocation for this collection: 1,099,511,627,776 bytes` |
| `/api/dataverses/kgwas/storage/quota` | `2,748,779,069,440 bytes` |

All three are `measured` (200, 73 B / 104 B / 104 B on 2026-10-22). Three different things
are true at once, and only one of them is a
multiplier: 1 TiB is the canonical allocation where an administrator set one, 2.5 TB exists on
at least one live collection, and the root collection has none. Presenting "collections free
and unlimited, times 1 TiB" as a hard product is not supported by the source. Collection
creation was in fact disabled for authenticated users in November 2022 and reopened in June
2024, so unlimited self-serve collections are not guaranteed either.

## Zenodo, and the read path that makes it a serving candidate

50 GB per record with an unlimited number of records, plus a 150 GB allowance for larger
files. The quota page states both verbatim (`documented`, 2026-10-22: 200, 2,413 B).

The finding that matters more is the read path. A ranged GET returned 206 with
`content-range: bytes 0-1023/2556616` and `server: nginx` (`measured`, 2026-10-22). The
throttle is per connection rather than per IP, which is why parallel ranged GETs are the only
honest way to measure it and why a sequential download is a large underuse of the link.

Zenodo is the reference case for the whole class: an email account, a real quota, and a read
path that responds to concurrency.

## The repositories that publish no ceiling

Nine qualifying records state "no quota defined at root", and the phrase is the same because
the software is the same. That is a documented absence rather than a documented limit, and
the difference matters: an absence cannot be multiplied, so no total can be derived from it.

The useful reading is that the absence is a signal about the institution. A repository that left
the quota feature off has not decided to be large. It has simply not decided to be small, and
the constraint is whatever its disk and its curator will tolerate.

## Two records for one provider, and why they are both kept

Source Cooperative holds two records that carry different numbers for the same
platform: the first describes an uncapped public publishing surface that is beta-gated, and the
second reports the vendor's own scale figures at over 5 petabytes across 330 or more products,
serving about 700 TB per month. The consolidation ledger keeps the two dossiers rather than merging
them, because a merge would need a slug rename and a ledger entry. A reader should treat them as one
provider with two readings, and `gaps.md` records the duplication.

## The grant programmes, which are a different answer

Five records here are not storage. NLnet and the Restack Fund give EUR 5,000 to 50,000 with
storage as a claimable project expense. Shuttleworth funds a fellow for a year with reported
project funding at USD 275,000. Emergent Ventures is an open-budget microgrant.

These belong in the document because a grant is the only route to a paid tier that does not
involve paying. They are not a storage finding and the record says so: their `free_tier.unit`
is `credits`, not bytes.

### DesignSafe-CI Data Depot (NSF NHERI / TACC) - no published cap on published datasets

> No published cap on published dataset size or file count: 'right now there is no limit to the amount of files that can be published in DesignSafe'. Policies page describes largest published datasets as ~5 TB (CoreTrustSeal submission:...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: twice: a TACC account (free, self-register) and curation 'Publish' approval. A new account costs email. Observed behaviour: CoreTrustSeal-certified, two-region replication (Corral + Ranch tape).

Evidence: `https://www.designsafe-ci.org/` (2026-10-21), record `dossier/storage/designsafe-ci-data-depot-no-published-cap-on-published-d.json`.
Verdict: `qualifies-with-caveat`.

### Emergent Ventures (Mercatus Center) - 13+, worldwide, no institution, fastest individual grant

> Open-budget microgrant: no fixed cap. Third-party trackers report a $1k-$50k typical range and up to $100k over two years, but the programme itself publishes no range - budgets are evaluated case by case. Rolling applications, one...

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: One-time or slightly staggered payments.

Evidence: `https://www.mercatus.org/emergent-ventures` (2026-10-21), record `dossier/storage/emergent-ventures-13-worldwide-no-institution-fastest-in.json`.
Verdict: `qualifies-with-caveat`.

### GBIF IPT via a data-hosting centre - free email account, but the payload must be biodiversity oc

> No quota published anywhere: a data-hosting centre gives you an account on its IPT installation, and your dataset lives in that IPT's data directory. Capacity is whatever the centre provisioned; there is no per-user byte figure to quote

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Long-lived EU-funded centres with backed-up IPT data directories.

Evidence: `https://www.gbif.org/data-hosting-centres` (2026-10-21), record `dossier/storage/gbif-ipt-via-a-data-hosting-centre-free-email-account-bu.json`.
Verdict: `qualifies-with-caveat`.

### Harvard Dataverse Repository - per-collection quota (the multiplier, not the 1 TB headline)

> 1 TB per Dataverse Collection allocation (2.5 TB for Harvard affiliates). Per-file 2.5 GB through UI/API; larger via the S3 direct-upload path. The 1 TB is enforced as a *collection* allocation, not a per-person cap: GET...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: per-file 2.5 GB. A new account costs email. Observed behaviour: Anonymous read is a 1-hour signed S3 redirect, so re-resolve per request (rule 8).

Evidence: `https://dataverse.harvard.edu/` (2026-10-22), record `dossier/storage/harvard-dataverse-repository-per-collection-quota.json`.
Verdict: `qualifies`.

### NLnet / Restack Fund - the grant an unaffiliated individual can actually hold

> EUR 5,000-50,000 for a first grant, and storage is a claimable project expense rather than a byte allocation. Next deadline 3 November 2026 12:00 CET; deadlines fall on the 3rd of every odd month

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Realistic size: a EUR 50k grant buys roughly 12-25 TB-months at Hetzner-class pricing, or funds an engineer - it does not buy 20 TB for five years.

Evidence: `https://nlnet.nl/propose/` (2026-10-21), record `dossier/storage/nlnet-restack-fund-the-grant-an-unaffiliated-individual.json`.
Verdict: `qualifies-with-caveat`.

### Science Data Bank (ScienceDB, Chinese Academy of Sciences / CNIC)

> 1 TB per dataset and 2,000 files per dataset, with no per-user or per-account cap; the 1 TB/2,000-file line is a soft gate (contact sciencedb@cnic.cn for more) rather than a hard refusal. 'Data packages' bundle multiple datasets under one...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1 TB per dataset. A new account costs email. Observed behaviour: CNIC-operated, long-lived (Springer Nature recommended-repository status).

Evidence: `https://www.scidb.cn/en` (2026-10-21), record `dossier/storage/science-data-bank.json`.
Verdict: `qualifies-with-caveat`.

### Shuttleworth Foundation Fellowship - individual, no organisation, $275k project funding

> Fellowship covers the Fellow's time for a year plus project funding reported at $275,000 per fellow per year, with the foundation matching the fellow's own contribution. Amount is set individually from the fellow's outside salary equivalent

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: One-year grants, renewable in practice for multi-year fellows, but per-fellow and discretionary.

Evidence: `https://www.shuttleworthfoundation.org/funding/fellowship-programme/who-can-apply/` (2026-10-21), record `dossier/storage/shuttleworth-foundation-fellowship-individual-no-organis.json`.
Verdict: `qualifies-with-caveat`.

### Source Cooperative (re-verify) - uncapped public publishing, beta-gated, BYOB is the real lever

> No published byte cap: 'allowing trusted organizations and individuals to publish data of any kind at any scale'. Case study: Earth Genome publishes 60+ TB. Platform total reported at just over 5 PB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Nonprofit (Radiant Earth 501(c)(3) parent) with in-kind AWS/Azure.

Evidence: `https://source.coop/` (2026-10-21), record `dossier/storage/source-cooperative-uncapped-public-publishing-beta-gated.json`.
Verdict: `qualifies-with-caveat`.

### BioStudies / ArrayExpress (EMBL-EBI)

> Free deposit, no published cap. 'Is there a cost to deposit data in BioStudies? No, both deposition of data to BioStudies and data access are free of charge.' Docs discuss 'larger data volumes (hundreds of GiB)' as routine

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 1 stream 7 KB/s, 16 parallel 25 KB/s against the EBI FTP edge. The record states no identity cost. Observed behaviour: Read edge is slow per connection and stalls connections under parallel load (one of 16 timed out with 0 bytes).

Evidence: `https://www.ebi.ac.uk/biostudies` (2026-10-21), record `dossier/storage/biostudies-arrayexpress.json`.
Verdict: `qualifies`.

### ENA (European Nucleotide Archive), Webin

> No fixed quota. Own fair-use policy: 'We place no absolute limit within the 2-month period on the total volume of user data that may exist in a data upload area at any one time' and 'we... expect that volumes would not exceed 10 Terabytes...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: single stream 45 KB/s, 8 parallel ranged GETs 430 KB/s (9. The record states no identity cost. Observed behaviour: Upload path is the weak side, FTP sessions drop out, Aspera recommended.

Evidence: `https://www.ebi.ac.uk/ena` (2026-10-21), record `dossier/storage/ena-webin.json`.
Verdict: `qualifies`.

### Mendeley Data (Elsevier)

> 10 GB per dataset for free individual accounts. Institutional Digital Commons Data subscribers get 100 GB per dataset

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 GB per dataset. The record states no identity cost. Observed behaviour: Archived in perpetuity via DANS with 3 copies, so bytes persist.

Evidence: `https://data.mendeley.com` (2026-10-21), record `dossier/storage/mendeley-data.json`.
Verdict: `fails-quota`.

### MorphoSource

> 'MorphoSource is able to subsidize or support free contribution of data for most users with 100GB or less.' 100 GB, 1 TB is case-by-case (may be fully free); >1 TB is $3.47/GB + $30

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Funding-dependent: the docs themselves state the free 100 GB subsidy is time-limited and will likely fall to ~15 GB within 2, 5 years.

Evidence: `https://www.morphosource.org` (2026-10-21), record `dossier/storage/morphosource.json`.
Verdict: `fails-quota`.

### NCBI GEO

> No published volume cap; raw sequence data is redirected to SRA. Notable for retention rather than size

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: not stated (defer to SRA for raw reads). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Records cannot stay private once an accession is cited in a manuscript or preprint, GEO staff release unilaterally.

Evidence: `https://www.ncbi.nlm.nih.gov/geo` (2026-10-21), record `dossier/storage/ncbi-geo.json`.
Verdict: `qualifies-with-caveat`.

### NCBI SRA, with anonymous read via AWS Open Data

> No per-account quota published. Submission is genuinely bulk: FTP, Aspera (`ascp -QT -l 100m -k1 -d`), or Aspermera; operator guidance for 'tens or more terabytes' is to contact SRA support directly

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: from S3, not a storage cap. The record states no identity cost. Observed behaviour: Historically flaky FTP uploads ('frequent drop-outs, you only have a few minutes from logging in').

Evidence: `https://www.ncbi.nlm.nih.gov/sra` (2026-10-21), record `dossier/storage/ncbi-sra-with-anonymous-read-via-aws-open-data.json`.
Verdict: `qualifies`.

### NeuroVault

> Free, no published per-file or per-account cap found on the site or FAQ (silence, not a stated infinity). 715,868 images currently indexed

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: unstated. The record states no identity cost. Observed behaviour: Single origin behind Cloudflare, small operator.

Evidence: `https://neurovault.org` (2026-10-21), record `dossier/storage/neurovault.json`.
Verdict: `qualifies-with-caveat`.

### OpenNeuro

> Free, no published per-dataset or per-account cap. 'Is this service free to use? Yes!' A 6.4 TB dataset has been deposited (staged incrementally)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: but weak. The record states no identity cost. Observed behaviour: Large uploads fail in the staging area and require batch-then-wait choreography.

Evidence: `https://openneuro.org` (2026-10-21), record `dossier/storage/openneuro.json`.
Verdict: `qualifies`.

### PANGAEA (Data Publisher for Earth & Environmental Science)

> Free to publish ('PANGAEA can be used free of charge'; a voluntary 500 EUR contribution is appreciated, not required). No total-volume cap found; the stated cap is per file

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Individual files must be less than 15 GB in size. The record states no identity cost. Observed behaviour: Submission queue is weeks long and editor-mediated.

Evidence: `https://www.pangaea.de` (2026-10-21), record `dossier/storage/pangaea.json`.
Verdict: `qualifies-with-caveat`.

### Synapse (Sage Bionetworks)

> No clear public storage cap found. Platform is free SaaS on S3; documented pain point is a '1GB per day' quota on modelState (compute artifacts), not on file storage

That is the record's own wording (`inferred`, 2026-10-21). The record states no identity cost. Observed behaviour: Certification gate plus no published quota means capacity is discretionary.

Evidence: `https://www.synapse.org` (2026-10-21), record `dossier/storage/synapse.json`.
Verdict: `qualifies-with-caveat`.

### TCIA (The Cancer Imaging Archive)

> Free. 'We do not charge a fee for sharing your data through TCIA except in rare circumstances where proposals are extremely large.'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: one zip per DICOM series (tens of MB each).... The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Deposit is a months-long institutional process.

Evidence: `https://www.cancerimagingarchive.net` (2026-10-21), record `dossier/storage/tcia.json`.
Verdict: `qualifies-with-caveat`.

### B2SHARE (EUDAT)

> 20 GB per record, 10 GB per file, and explicitly unlimited records and unlimited files

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 10 GB per file. The record states no identity cost. Observed behaviour: Rate-limited at 500 requests/window and watched for bulk growth.

Evidence: `https://b2share.eudat.eu` (2026-10-21), record `dossier/storage/b2share.json`.
Verdict: `qualifies-with-caveat`.

### DANS Data Stations (ssh.datastations.nl / DataverseNL)

> 9.3 GB maximum per file, no per-dataset or per-collection quota configured. Dutch national repository (KNAW/NWO); deposit is free for researchers at Dutch institutions and for EASY-migrated data

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 9.3 GB per file. The record states no identity cost. Observed behaviour: Tightly coupled to Dutch institutional eligibility, so account supply is the limit rather than bytes.

Evidence: `https://ssh.datastations.nl` (2026-10-21), record `dossier/storage/dans-data-stations.json`.
Verdict: `fails-identity`.

### Harvard Dataverse

> 1 TB of storage, free, for 'All researchers from any discipline, both inside and out of the Harvard University community', but only 2.5 GB per file. 1 TB clears the 500GB bar on its own, and datasets/dataverses can be multiplied

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 2.5 GB per file. The record states no identity cost. Observed behaviour: Live observed of a file returned a 303 to S3 and then a 2.5 MB download at 3.2s end-to-end, the redirect chain works anonymously.

Evidence: `https://dataverse.harvard.edu` (2026-10-22), record `dossier/storage/harvard-dataverse.json`.
Verdict: `qualifies-with-caveat`.

### HydroShare (CUAHSI)

> 20 GB automatic on account creation, with an increase process that is explicitly designed to succeed: 'if needed, request reasonable quota increase... all reasonable requests will be approved subject to system capacity limitations'. No...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: on the increase (email a human), and the quota is small by default. A new account costs email. Observed behaviour: US NSF-funded via CUAHSI.

Evidence: `https://www.hydroshare.org` (2026-10-21), record `dossier/storage/hydroshare.json`.
Verdict: `fails-quota`.

### IEEE DataPort, Data Competition module (the free + public route)

> 2 TB per dataset for individual users, 10 TB for Institutional Subscribers. The Data Competition submission type is listed as FREE and carries the same 2 TB / 10 TB ceilings, 'Dataset files may total up to 2 TB or 10 TB for Institutional...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: + read-gated, and the gate differs by route. A new account costs email. Observed behaviour: S3 bucket is real and correctly access-controlled (403, not a fake 200).

Evidence: `https://ieee-dataport.org/submit-dataset` (2026-10-21), record `dossier/storage/ieee-dataport-data-competition-module.json`.
Verdict: `fails-egress`.

### Kaggle Models (distinct from Kaggle Datasets)

> 200 GB for private models, alongside 200 GB for private datasets, from Kaggle's own product announcement 'Doubling of Private Quota and Public File Size Limit': 'Users now have a limit of 200GB for private models and 200GB for private...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200 GB and 50 top-level files per dataset.... A new account costs email. Observed behaviour: Kaggle is Google-owned and long-lived.

Evidence: `https://www.kaggle.com/models` (2026-10-21), record `dossier/storage/kaggle-models.json`.
Verdict: `qualifies-with-caveat`.

### Mozilla Data Collective (MDC)

> 150 GB per uploaded file, raised from a lower value in the Python SDK on 2026-03-24 ('Increase upload file size limit to 150GB'). No published per-account or total quota anywhere in the provider terms, FAQ, or API reference; the archive in...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: hard. A new account costs email. Observed behaviour: The gate is a human reviewer, not a form, treat acceptance as the scarce resource.

Evidence: `https://mozilladatacollective.com` (2026-10-21), record `dossier/storage/mozilla-data-collective.json`.
Verdict: `qualifies-with-caveat`.

### Nebula Block, Standard object storage tier (storage free, egress billed)

> No storage quota on the Standard tier, it is priced at $0/GB/month by design: 'Standard, Stored data: Free, Durable, high-capacity storage. The default'. The paid tiers are Performance at $0.015/GB/month and Accelerated at $0.02/GB/month....

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Canadian (Montreal/Quebec) provider, small.

Evidence: `https://www.nebulablock.com/storage` (2026-10-21), record `dossier/storage/nebula-block-standard-object-storage-tier.json`.
Verdict: `qualifies-with-caveat`.

### ScienceDB (Science Data Bank, CAS / CNIC), write path

> No data-volume limit. A 2025 peer-reviewed comparison of Zenodo and ScienceDB in Journal of Agricultural Big Data states it plainly: for ScienceDB the row reads (no limit on data volume; users may upload datasets of any size), against...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: by 'formal review' of upload completeness.... A new account costs email. Observed behaviour: API probing shows the public JSON endpoints are not the same shape as Zenodo's, /api/v1/dataset/.

Evidence: `https://www.scidb.cn/en` (2026-10-21), record `dossier/storage/sciencedb-re-verified-write-path.json`.
Verdict: `qualifies-with-caveat`.

### Source Cooperative (source.coop / data.source.coop), byte-level re-probe

> No published byte quota; the org states it 'hosts over 5 petabytes of data' across 330+ products from 130+ organisations and serves ~700 TB/month, and positions itself as 'data publishing at any scale'. I could not find any per-product,...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: publishing data requires applying to be a beta tester' via a Google Form.... A new account costs email. Observed behaviour: Beta + announced-but-unpublished pricing means the free window has an unknown end date.

Evidence: `https://source.coop` (2026-10-21), record `dossier/storage/source-cooperative-byte-level-re-probe.json`.
Verdict: `qualifies-with-caveat`.

### CaltechDATA (InvenioRDM, California Institute of Technology)

> 1 TB of free storage per user, announced 2026-06-26, 'made possible through a National Science Foundation Campus Cyberinfrastructure grant' and backed by the Open Storage Network. Additional storage $200/TB one-time. 550 files max per...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Anonymous API reads work and are generous (X-RateLimit-Limit: 500 observed on /api/records).

Evidence: `https://data.caltech.edu` (2026-10-21), record `dossier/storage/caltechdata.json`.
Verdict: `fails-identity`.

### OSF (Open Science Framework), per-component quotas

> 50 GB per public project, 5 GB per private project, 5 GB per file, but 'Each Component on a project has its own 5GB/50GB storage limit' and, crucially, 'Currently, there is no applied overall cap on the amount of OSF Storage per user.'...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GB per file. The record states no identity cost. Observed behaviour: OSF is mid-'Project Transition' per its own help banner, which is a structural-change risk for a long-lived archive.

Evidence: `https://osf.io` (2026-10-21), record `dossier/storage/osf-per-component-quotas.json`.
Verdict: `qualifies-with-caveat`.

### Recherche Data Gouv (French national Dataverse)

> 50 GB max per file via the deposit interface; institutional datasets carry an agreement limit 'currently 5 TB'; datasets over 50 GB are explicitly supported via DVUploader and the S3 direct-upload API, and TB-range datasets are handled by...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 50 GB max per file. The record states no identity cost. Observed behaviour: Instance is healthy and live (Dataverse 6.0 at observed).

Evidence: `https://entrepot.recherche.data.gouv.fr` (2026-10-21), record `dossier/storage/recherche-data-gouv.json`.
Verdict: `fails-identity`.

### Zenodo anonymous download throughput (the fetch-serving question)

> n/a, this entry records the measured read path for the 500GB-1TiB/day serving workload

That is the record's own wording (`documented`, 2026-10-22). The record states no identity cost. Observed behaviour: Single-stream downloads are painfully slow (~215 KB/s on a 100MB range.

Evidence: `https://zenodo.org/api/records/5656641/files/iPS.zip/content` (2026-10-22), record `dossier/storage/zenodo-anonymous-download-throughput.json`.
Verdict: `qualifies`.

### Zenodo restricted-access records, and what the visibility flag buys

> 50 GB per record and a 150 GB account pool, unchanged by visibility: restricting the files neither reduces nor refunds the quota. A secret link grants 'Can view' on restricted or embargoed files of all current and future versions, with an optional expiry date

That is `documented` from `help.zenodo.org/docs/share/link-sharing/` (2026-10-21), record `dossier/storage/zenodo-restricted-access-records-and-secret-links.json`. ⚠ **Metadata is always public**, so titles, descriptions and the minted DOI leak even when the files do not. That makes it a leaky private tier rather than a private bucket, and it is the answer to the working-storage question: usable for data that should not be published but may be named.

Verdict: `qualifies-with-caveat`, binding `per-object-cap`. Restricting a record buys privacy and no capacity, so the record count for an archive of 20 TiB is about 410 either way.

### Zenodo DOI batching, which is what makes the sharding practical

> One DOI per record, minted automatically and free, with `prereserve_doi` already set in the deposition response. DOI count is therefore not a constraint on sharding, and there is no per-DOI cost and no approval step

That is `documented` from `developers.zenodo.org/` (2026-10-21), record `dossier/storage/zenodo-doi-batching-automatic-datacite-minting.json`. The consequence is the one worth carrying: a 410-record archive is also 410 citable handles at no extra cost, so the record boundary is a safe place to shard. What binds is the authenticated request rate at 100 per minute and not any record limit.

Verdict: `qualifies-with-caveat`, binding `request-rate`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| AWS Open Data Sponsorship Program... | fails-identity | No published byte limit; AWS pays S3 storage plus egress and cross-region fees for the approved dataset... |
| Copernicus Data Space Ecosystem... | fails-quota | 12 TB per rolling 30 days of download via S3/OData/STAC for a Copernicus General User, 20 MB/s per connection... |
| DataONE Hosted Repository... | fails-quota | 1 TB repository capacity, 'Grow your 1 TB repository capacity based on your storage needs in 1 TB increments'... |
| IEEE DataPort - 2 TB per dataset free upload... | fails-egress | 2 TB of AWS S3 cloud storage per dataset for individual users... |
| Nakala (Huma-Num, France) - no formal size limit... | fails-identity | 'There is no formal limitation on the size of data deposited'... |
| NASA Earthdata AWS allocation... | fails-identity | A 2 PB storage allocation held by NASA's Earth Science Division inside the AWS Open Data Program... |
| Dryad | fails-quota | Pay-to-publish (Data Publishing Charge). Up to 5 GB = $150; 1 TB = $6,077; 2 TB = $12,162. Not a free tier in any sense |
| figshare (figshare.com free accounts) | fails-quota | 20 GB storage quota per account. Note: the '5 GB per file' figure is stale... |
| RADAR (FIZ Karlsruhe) | fails-quota | Paid institutional service, no free self-serve tier. Targeted at institutions and research groups buying a data-publication... |
| AWS Bedrock, custom model import | fails-quota | Hard per-object cap: 'The size of the imported model weights must be less than 100GB for multimodal models and 200GB for... |
| CyVerse Data Store | fails-quota | 5 GB default for every account, explicitly for 'all domestic and international CyVerse account holders'... |
| data.world | fails-quota | 100 GB total storage on the free Community plan, but with a 3 GB limit per dataset or project... |
| Datarade | fails-quota | Zero bytes hosted. Datarade is explicitly a discovery and brokerage layer: it 'doesn't host or deliver data, instead... |
| DICE / EUDAT cost-free storage call... | fails-identity | Not published as a number, DICE is a funding instrument, not a product... |
| Google Vertex AI Model Garden, custom model import | fails-quota | No hosting quota because there is no hosting: 'You must store your model artifacts in a Cloud Storage bucket... |
| NOMAD (NOMAD Central / nomad-lab.eu) | fails-quota | 32 GiB maximum per project, and at most 10 unpublished projects per user. Both are config knobs (process.max_upload_size... |
| Snowflake trial account (internal stage) | trial-only | No byte quota, a $400 credit balance and a 30-day clock, whichever ends first. 'The trial continues for 30 days... |
| Tableland | fails-quota | 500,000 rows and 24 columns per table. That is the entire quota, it is a SQL-over-SQLite network... |
| Walrus Console (Walrus Foundation, Oct 2026 launch) | fails-quota | 5 GB free. Launched 2026-10-07 with 'Get started today with 5GB free'. No larger free tier is published |
| Spice.ai Cloud (Community Edition) (self-hosted) | fails-quota | No storage quota published, because the product is not storage... |

The rejections split into three groups and only one of them is about size.

`quota` is the largest: HAL caps a file at 200 MB, KNB gives 5 GB per user, 4TU gives 5 GB per
researcher per year and then charges EUR 4.50 per GB.

`identity` is the one that matters. DataverseNL, GRO.data, DaRUS, DataverseNO and Helix all
report no quota and all require an institution, which is the combination this document
separates. A 13.58 GB object already exists on Helix and a reader outside the institution cannot
deposit one.

`not-storage` covers the platform classes: an InvenioRDM installation that gives 10 GB per
record, a DSpace installation with no quota model, an EPrints installation with no
per-collection accounting. They are recorded because a reader who finds one installation and
assumes the software implies the quota will be wrong at the next institution.

## Chaining

Two rules, and both come from the identity finding.

Register with the generalist repository first, because it is the only class where the door
and the quota are both open. Zenodo, B2SHARE and Borealis are the three, and Borealis is the
only institution-scale one with an open door and no quota object.

Use the domain repository for the data that fits its domain, because the ceiling there is the
absence of one. An ENA submission of a sequencing dataset has no published fixed quota, and
the same bytes at a generalist repository would be 50 GB per record.
