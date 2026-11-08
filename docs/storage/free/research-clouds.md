# Research clouds: which national allocation a foreign individual can actually join

The largest quotas in this topic are here, and almost all of them are closed to an unaffiliated
reader. CSC Allas offers 10 TiB per project, LUMI-O offers 150 TB, HPCI offers 500 TB, OSN offers 1 to
50 TB, and every one of them requires an affiliation, a national programme or a project
allocation that an unaffiliated individual cannot produce.

The negative result is worth more than the positive one,
because it stops a reader chasing a 150 TB figure. And the grant programmes beside the
clouds are the one route to a paid tier that does not involve paying.

The 16 qualifying records split into national research clouds and credits, grants and
sponsorship. 11 were rejected, and the two Finnish clouds are in the rejected list
because the gate, not the quota, is what decides them.

## The comparison

Sorted by allocation, with the identity cost beside it, because that is the column that
decides.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| AWS Open Data Sponsorship Program | No published byte limit, the program 'covers the cost of Amazon S3 storage and data... | - | - | qualifies |
| Chan Zuckerberg Initiative - Essential Open Source... | No byte quota - $100,000-$400,000 total over two years... | write-gated: invited full proposal) | - | qualifies-with-caveat |
| Fastly Fast Forward (OSS CDN) | No byte quota - free CDN/edge services for eligible OSS projects and the nonprofits... | write-gated: reviewed by a human | - | qualifies-with-caveat |
| HPCI Shared Storage (Japan... | 500 TB initial allocation for new applicants... | - | - | qualifies-with-caveat |
| INCITE (ALCF + OLCF, US DOE) | 100 trillion bytes (~100 TB) of data storage awarded across the programme each year... | write-gated: reviewed annual renewal request | - | qualifies-with-caveat |
| NLnet / Restack fund (NGI Zero successor) | EUR 5,000-50,000 per first grant, 'with the possibility to scale them up if there is... | - | - | qualifies-with-caveat |
| Oracle for Research (Project Award / Cloud Starter) | Credit-based, amount 'will vary depending on the proposal and usage requirements'... | - | - | qualifies-with-caveat |
| Project Alexandria - Cloudflare's recurring OSS... | Recurring annual credits, amount set per project... | - | - | qualifies-with-caveat |
| Public Datasets hosting programme (Google Cloud) | No published quota - Google 'pays for the hosting of these datasets'... | - | - | qualifies-with-caveat |
| CSC Allas (Finland), 10 TiB default per project... | 10 TiB per CSC project by default. The quota table lists 'Allas / Storage / 10 TiB'... | identity: Haka or Virtu login, or a home organisation with a CSC contract | institution | fails-identity |
| CSC Fairdata IDA (Finland)... | No flat per-user number; the quota is a slice of the home organisation's allocation... | per-object-cap: not published | - | qualifies-with-caveat |
| Digital Research Alliance of Canada... | 'All Arbutus projects are allocated a default 1TB of object storage... | request-rate: not published | - | qualifies-with-caveat |
| LUMI-O (CSC / EuroHPC LUMI)... | 'LUMI-O offers a total of 30 PB storage space... | identity: a LUMI or EuroHPC project allocation | institution | fails-identity |
| NAISS Arrhenius Disk / SENS Storage (Sweden)... | Project storage is applied for in GiB through SUPR... | per-object-cap: not applicable (POSIX/Lustre) | - | qualifies-with-caveat |
| National Research Platform (NRP / Nautilus, US)... | No published byte quota. The docs are explicit that the storage is donated: 'The... | per-object-cap: CephFS has 'a per-file size limit of 16 TB | - | qualifies-with-caveat |
| NSF ACCESS / Jetstream2 object store... | 'By default, all allocations receive 1 TB... | per-object-cap: Swift, so large objects need segmentation | - | qualifies-with-caveat |
| Open Storage Network (OSN) via NSF ACCESS... | 'Allocations of a minimum 10 terabytes and max of 50 terabytes supporting up to 1.6... | request-rate: not published, but the docs note parallel requests against the... | - | qualifies |
| SURF Research Drive (Netherlands)... | Community Edition: 'Are you working at an institution without its own Research Drive... | per-object-cap: not published for Research Drive | - | qualifies-with-caveat |

## What the class is

A research cloud is a national or continental allocation sold as compute, storage and a project
quota. Three properties separate it from a commercial cloud.

**The allocation is applied for, not bought.** A project goes through a review, a national
access programme or a partner agreement, and the review is where the identity is checked.

**The storage is often the largest single number available anywhere.** LUMI-O allocates 150 TB
per project by default out of 30 PB total. HPCI allocates 500 TB initially, expandable to 1.5
PB, out of 90 PB logical capacity. NAISS applies for project storage in GiB with an upper limit
of 50,000.

**The endpoint is usually open even when the allocation is not.** That is the trap. `GET
https://a3s.fi/` returned 200 with 214 bytes containing
`<ListAllMyBucketsResult><Owner><ID>anonymous</ID><Buckets></Buckets>` on 2026-10-22
(`measured`), and `GET https://lumidata.eu/` returned 200 with 187 bytes of the same shape. Both
answer anonymously, and neither is usable without a project. A liveness probe on this class
proves the endpoint and says nothing about access.

## The four Tier-1 entries that are unreachable

These four are the reason the topic README leads with identity rather than quota.

| provider | allocation | what blocks it |
|---|---|---|
| CSC Allas | 10 TiB per project by default | Haka or Virtu login, or a home organisation with a CSC contract |
| LUMI-O | 150 TB per project by default | a LUMI or EuroHPC project |
| Open Storage Network | 1 to 50 TB of S3 per allocation, 10 TB minimum | a US NSF ACCESS allocation |
| HPCI Shared Storage | 500 TB initial, 1.5 PB expandable | a Japanese HPCI project application |

CSC's own account documentation settles the first: "The preferred registration method is to
log in using Haka or Virtu... you can get an account if your home organization has a contract
with CSC or you have been granted resources in a program." That is a quote from the vendor, and
it makes the verdict `fails-identity` rather than a caveat.

Both records carry `verdict: fails-identity` and all three readings
in `extras.conflicts[]`.
The document states the quota and the gate in the same sentence, which is what `fails-identity`
encodes: 10 TiB per project by default, reachable only through Haka or Virtu, so the quota is
real and unreachable.

## The one national cloud with a published default and a plausible path

Digital Research Alliance of Canada allocates 1 TB of object storage to every Arbutus project
by default, with an additional 9 TB available on request and up to 40 TB per project through
the resource allocation competition. The default is automatic rather than reviewed, and the
project needs a Canadian academic affiliation.

NSF ACCESS and Jetstream2 are the same shape in the United States: 1 TB per allocation by
default, with additional storage bought with ACCESS credits at 1 credit per GB. The allocation
needs an NSF identity.

These are the closest to usable, and "closest" means a form that requires an institutional
identity.

## The grant programmes, which are not storage

Eight records here are credits or grants rather than byte allocations, and they are in this
document because they are the only route to a paid tier that does not involve paying.

AWS Open Data Sponsorship covers the cost of S3 storage and data transfer for high-value public
datasets. Google's Public Datasets programme pays for hosting. Project Alexandria gives
recurring Cloudflare credits and explicitly includes increased R2 storage for builds and
artifacts. Oracle for Research gives credit that varies by proposal.

Two are aimed at an individual rather than an organisation and those are the ones worth
reading. NLnet and the Restack Fund give EUR 5,000 to 50,000 per first grant, with storage as a
claimable project expense, and the fund takes applications from individuals. The Chan
Zuckerberg Initiative's EOSS gives USD 100,000 to 400,000 over two years, and it needs an open
source project rather than an institution.

None of these is a quota. A grant is money, and money buys storage at the paid lane's prices.
The distinction matters because a reader who counts a grant as capacity will plan an archive of
20 TiB on a USD 10,000 credit, which buys about 400 TB-months at the floor and less than a
year at the top of the paid range.

### AWS Open Data Sponsorship Program

> No published byte limit, the program 'covers the cost of Amazon S3 storage and data transfer for high-value cloud-optimized public datasets' in full, on a dedicated AWS account that joins AWS's billing organization. Term is 2 years,...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Renewal review considers usage metrics.

Evidence: `https://aws.amazon.com/opendata/open-data-sponsorship-program/` (2026-10-21), record `dossier/storage/aws-open-data-sponsorship-program.json`.
Verdict: `qualifies`.

### Chan Zuckerberg Initiative - Essential Open Source Software for Science (EOSS)

> No byte quota - $100,000-$400,000 total over two years, from which cloud/storage is a claimable line item

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: invited full proposal). The record states no identity cost. Observed behaviour: Cycle-based, not rolling - the current cycle page shows Cycle 6 closed, so timing is the gate.

Evidence: `https://chanzuckerberg.com/rfa/essential-open-source-software-for-science/` (2026-10-21), record `dossier/storage/chan-zuckerberg-initiative-essential-open-source-softwar.json`.
Verdict: `qualifies-with-caveat`.

### Fastly Fast Forward (OSS CDN)

> No byte quota - free CDN/edge services for eligible OSS projects and the nonprofits that support them. Scope set per applicant after review

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: reviewed by a human. The record states no identity cost. Observed behaviour: Established programme (relaunched 2022) with real OSS members (PyPI historically).

Evidence: `https://www.fastly.com/fast-forward` (2026-10-21), record `dossier/storage/fastly-fast-forward.json`.
Verdict: `qualifies-with-caveat`.

### HPCI Shared Storage (Japan, RIKEN R-CCS + Univ. of Tokyo, Gfarm)

> 500 TB initial allocation for new applicants; expandable to 1.5 PB. Total logical capacity 90.0 PB, replicated east/west hub

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Enterprise DDN + Gfarm, cross-hub replication.

Evidence: `https://www.hpci-office.jp/en/using_hpci/hardware_software_resource/2026/hpci_2026_st-1` (2026-10-21), record `dossier/storage/hpci-shared-storage.json`.
Verdict: `qualifies-with-caveat`.

### INCITE (ALCF + OLCF, US DOE)

> 100 trillion bytes (~100 TB) of data storage awarded across the programme each year; per-project archival quota at OLCF is 200 TB (shared across Project/World/User Archive on Kronos)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: reviewed annual renewal request. The record states no identity cost. Observed behaviour: Tenured infrastructure.

Evidence: `https://doeleadershipcomputing.org/incite-faqs/` (2026-10-21), record `dossier/storage/incite.json`.
Verdict: `qualifies-with-caveat`.

### NLnet / Restack fund (NGI Zero successor)

> EUR 5,000-50,000 per first grant, 'with the possibility to scale them up if there is proven potential'. Storage is a claimable project cost, not a byte allocation

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Small sums relative to 20 TB of storage.

Evidence: `https://nlnet.nl/funding.html` (2026-10-21), record `dossier/storage/nlnet-restack-fund.json`.
Verdict: `qualifies-with-caveat`.

### Oracle for Research (Project Award / Cloud Starter)

> Credit-based, amount 'will vary depending on the proposal and usage requirements'. OCI Object Storage list price ~$25.5/TB-month, so $10k is roughly 32 TB-months

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Regional restriction is undisclosed, so eligibility cannot be confirmed without applying.

Evidence: `https://go.oracle.com/research-project-award` (2026-10-21), record `dossier/storage/oracle-for-research.json`.
Verdict: `qualifies-with-caveat`.

### Project Alexandria - Cloudflare's recurring OSS credit programme

> Recurring annual credits, amount set per project. Explicitly includes 'Increased R2 storage for builds and artifacts' and 'Increased requests to Cloudflare Workers and Pages'

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Credits can be revised or withdrawn.

Evidence: `https://www.cloudflare.com/lp/project-alexandria/` (2026-10-21), record `dossier/storage/project-alexandria-cloudflare-s-recurring-oss-credit-pro.json`.
Verdict: `qualifies-with-caveat`.

### Public Datasets hosting programme (Google Cloud)

> No published quota - Google 'pays for the hosting of these datasets'. Existing hosted sets (Sentinel-2, Landsat, ARCO-ERA5, NEXRAD) run to petabytes

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: No published process means no predictable outcome.

Evidence: `https://docs.cloud.google.com/storage/docs/public-datasets` (2026-10-21), record `dossier/storage/public-datasets-hosting-programme.json`.
Verdict: `qualifies-with-caveat`.

### CSC Allas (Finland), 10 TiB default per project, S3 + Swift on Ceph

> 10 TiB per CSC project by default. The quota table lists 'Allas / Storage / 10 TiB' with the increase path 'Contact CSC Service Desk'. There is no per-file or per-object size cap documented; the counted limits are 1,000 buckets per project...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is the registration gate, not one of the six: 10 TiB per project is real and a project needs a Haka or Virtu login or a home organisation with a CSC contract, so the identity cost is `institution`. Observed behaviour: Storage-BU exhaustion closes the project.

Evidence: `https://docs.csc.fi/data/Allas/introduction/` (2026-10-21), record `dossier/storage/csc-allas-10-tib-default-per-project-s3-swift-on-ceph.json`, and `https://docs.csc.fi/accounts/how-to-create-new-project/` for the gate.
Verdict: `fails-identity`.

### CSC Fairdata IDA (Finland), quota granted per CSC project, funded from the home organisation's

> No flat per-user number; the quota is a slice of your organisation's allocation. Published national pool (last updated 2025-02-28): University of Helsinki 1,500 TB, Aalto 480 TB, University of Oulu 465 TB, University of Turku 427 TB,...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: not published. The record states no identity cost. Observed behaviour: Second gate is a human approver at the applicant's home organisation.

Evidence: `https://www.fairdata.fi/en/ida-quotas-by-organisation/` (2026-10-21), record `dossier/storage/csc-fairdata-ida-quota-granted-per-csc-project-funded-fr.json`.
Verdict: `qualifies-with-caveat`.

### Digital Research Alliance of Canada, 1 TB default object storage per project, up to 40 TB proje

> 'All Arbutus projects are allocated a default 1TB of object storage. If more is required, you can either request an additional 9TB available through our Rapid Access Service. More than 10TB must be requested and allocated under the annual...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: not published. The record states no identity cost. Observed behaviour: Not backed up and self-managed.

Evidence: `https://docs.alliancecan.ca/wiki/Arbutus_object_storage` (2026-10-21), record `dossier/storage/digital-research-alliance-of-canada-1-tb-default-object.json`.
Verdict: `qualifies-with-caveat`.

### LUMI-O (CSC / EuroHPC LUMI), 150 TB allocated per LUMI project by default

> 'LUMI-O offers a total of 30 PB storage space... By default 150 TB of storage space is allocated per LUMI project, but projects can request for more LUMI-O storage space by contacting the LUMI helpdesk.' This is the single largest default...

That is the record's own wording (`documented`, 2026-10-22). The object cap is 500,000 objects per bucket, the same as Allas, but the constraint that binds first is the registration gate: the allocation exists only inside a LUMI or EuroHPC project, so the identity cost is `institution`. Observed behaviour: Data dies with the project.

Evidence: `https://docs.lumi-supercomputer.eu/storage/lumio/` (2026-10-21), record `dossier/storage/lumi-o-150-tb-allocated-per-lumi-project-by-default.json`.
Verdict: `fails-identity`.

### NAISS Arrhenius Disk / SENS Storage (Sweden), 25 PB and 10 PB project storage, applied in GiB

> Project storage is applied for in GiB through SUPR, with generous upper limits: Arrhenius Disk shows 'Upper Limit 50,000', 'Default Storage 250', 'Available 4,000,000' (GiB, so 50,000 GiB 48.8 TiB ceiling, 250 GiB default); Klemming 'Upper...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: not applicable (POSIX/Lustre). The record states no identity cost. Observed behaviour: No backup on Arrhenius Disk or SENS Storage.

Evidence: `https://supr.naiss.se/round/2026medium/` (2026-10-21), record `dossier/storage/naiss-arrhenius-disk-sens-storage-25-pb-and-10-pb-projec.json`.
Verdict: `qualifies-with-caveat`.

### National Research Platform (NRP / Nautilus, US), free Ceph S3 to any namespace holder, multi-si

> No published byte quota. The docs are explicit that the storage is donated: 'The Nautilus Ceph storage cluster can be accessed via S3 protocol. It uses our own storage, which is free for our users and is not part of Amazon or any...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: CephFS has 'a per-file size limit of 16 TB. The record states no identity cost. Observed behaviour: 6-month untouched-data purge is documented and unannounced.

Evidence: `https://nrp.ai/documentation/userdocs/storage/ceph-s3/` (2026-10-21), record `dossier/storage/national-research-platform-free-ceph-s3-to-any-namespace.json`.
Verdict: `qualifies-with-caveat`.

### NSF ACCESS / Jetstream2 object store (OpenStack Swift, S3-compatible), 1 TB default storage per

> 'By default, all allocations receive 1 TB (1000 GB) of Jetstream2 Storage quota.' Additional storage is bought with ACCESS credits at '1 ACCESS credit == 1 GB', and the default is a floor, not additive: 'the default 1 TB is replaced by a...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Swift, so large objects need segmentation. The record states no identity cost. Observed behaviour: Docs state plainly 'Jetstream2 is not primarily a storage service.

Evidence: `https://docs.jetstream-cloud.org/general/quotas/` (2026-10-21), record `dossier/storage/nsf-access-jetstream2-object-store-1-tb-default-storage.json`.
Verdict: `qualifies-with-caveat`.

### Open Storage Network (OSN) via NSF ACCESS, 1 to 50 TB of S3 per allocation, 10 TB minimum

> 'Allocations of a minimum 10 terabytes and max of 50 terabytes supporting up to 1.6 million files can be requested through the ACCESS CI allocation process.' The ACCESS documentation states it as a 10-50 TB project allocation with '1...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: not published, but the docs note parallel requests against the inside.... The record states no identity cost. Observed behaviour: Buckets are 'not backed up' and are created by ticket/portal form, not API, automation is limited to reads and writes, not bucket provisioning.

Evidence: `https://www.openstoragenetwork.org/get-involved/get-an-allocation/` (2026-10-21), record `dossier/storage/open-storage-network-via-nsf-access-1-to-50-tb-of-s3-per.json`.
Verdict: `qualifies`.

### SURF Research Drive (Netherlands), up to 5 TB free via NWO-funded Small Compute applications

> Community Edition: 'Are you working at an institution without its own Research Drive environment? Then apply for access to Research Drive Community Edition here. You will receive up to 5 TB of storage space.' Institutional instances have...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: not published for Research Drive. The record states no identity cost. Observed behaviour: servicedesk.surf.nl returns 401 to the reader and www.surf.nl intermittently 504s.

Evidence: `https://www.surf.nl/en/services/storage-data-management/research-drive` (2026-10-21), record `dossier/storage/surf-research-drive-up-to-5-tb-free-via-nwo-funded-small.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| ALCC (ASCR Leadership Computing Challenge) | fails-quota | 10-30% of ALCF/OLCF/NERSC resources each year, with associated project storage (e.g. OLCF 200 TB archive, 50 TB work) |
| AWS Cloud Credit for Research | fails-quota | Students capped at $5,000; 'Faculty and Staff awards are not capped'. Credit-denominated against S3 list price |
| EuroHPC JU Regular Access (LUMI, Leonardo... | fails-quota | Node-hours plus an associated storage quota set by the hosting entity... |
| GCP research credits programme... | fails-quota | $5,000 one-time for faculty/postdoc; $1,000 per year for PhD students. Credit-denominated... |
| Wellcome Trust - storage as a claimable grant cost | fails-quota | No byte quota - 'large-scale data storage' is an allowable service charge... |
| EOSC EU Node, 50 GB personal + 500 GB group file... | fails-quota | Access-policy table: File Storage (Personal) = 50 GB for Collaborator and Investigator... |
| NCI Gadi /g/data (Australia)... | fails-quota | Infrastructure is huge, '/g/data4-7 / 110+ PB / Persistent Storage', 'Massdata / 70+ PB'... |
| NIRD Data Lake (Sigma2, Norway), S3 object storage... | fails-quota | No fixed per-project byte number published, quota is set per project by the Resource Allocation Committee... |
| TACC Corral (US), 5 TB free per PI, $60/TB/year beyond | fails-quota | 'The first 5TB of storage for each PI, on one project, is available to researchers at all UT System institutions at no... |

The rejections are small in number and heavy in size, which is the opposite of every other
document in this topic. Eight of the nine are `fails-quota` or `identity`, and the quotas
involved are the largest in this topic.

NIRD Data Lake is not a free tier: the User Contribution Model
charges 470 NOK per TB per year.

EOSC needs eduGAIN or eIDAS. NCI Gadi needs an Australian allocation. TACC Corral gives 5 TB per
principal investigator and charges USD 60 per TB per year beyond it, which is a paid product
with a free first slice rather than a free tier.

## Chaining

The rule for this document is short and it is a negative one: do not build a plan on a research
cloud unless the deployment holds the affiliation.

The positive version is narrower. If a grant is available, it converts the paid lane from a
budget question into an application question, and the two funds that accept an individual are
NLnet and the Restack Fund. That is the only chaining this class supports.
