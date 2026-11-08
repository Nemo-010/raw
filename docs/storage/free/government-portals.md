# Government portals: the clean negative

This is the only document in the topic with one qualifying record and thirteen rejections, and
the imbalance is the finding. Government open-data portals are the most obviously promising
source of large free public storage and they are uniformly closed to an individual depositor.

The one exception is HDX, run by UN OCHA, and what makes it an exception is worth stating
precisely: the gate is editorial rather than personal.

## The comparison

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| HDX (Humanitarian Data Exchange) | no published per-user or per-file quota; the platform hosts the files itself | `write-gated`: an organisation request is reviewed by OCHA | email plus a reviewed organisation | qualifies-with-caveat |

## The pattern, which is universal

Twenty or more portals were swept across national and municipal levels, and the same structure
appears everywhere. A portal hands out *consumer* accounts and reserves *publisher*
organisations for public bodies. The write path requires an organisation that a private
individual cannot create.

The cleanest proof is `data.gov.ro`, which has the most open registration form found: a plain
email address, no invite. Its `organization_create` endpoint still returns "Acces interzis".

A second test rules out the obvious alternative route. Samples of `data.gov.ua` with 300
datasets and `data.boston.gov` with 235 contained zero unowned datasets, so the route of
publishing without belonging to an organisation does not exist in practice either.

The technical ceiling is a third reason and it is independent of the policy. CKAN's default
`ckan.max_resource_size` is 10 MB, which is two orders of magnitude below the filter, and most
portals have stopped hosting bytes at all in favour of metadata that points at an agency's own
server.

## HDX, and why it is different

HDX runs the same CKAN-shaped software and it does not hand out organisations either. What is
different is that a request can be made and a person decides.

The path is an email signup, then a request at `data.humdata.org/org/request/new`, then OCHA's
review, then an upload to UN-hosted S3-backed storage with no published quota. Reads are
anonymous and unmetered.

So the constraint is `write-gated`, not `identity`, and that distinction is the whole finding
of this document. An editorial gate is a queue with a person in it, and a queue can be joined.
An identity gate is a wall.

The record carries `identity_cost: email` and `identity_probe: form-read`, because no signup was
executed. The organisation review is the part that would settle it.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| data.boston.gov (City of Boston, Socrata/CKAN hybrid) | fails-identity | 235 datasets, 32 organisations, 0 unowned. Portal-hosted /download/ paths (tmp05gz_hzf.csv etc.) |
| data.gov.ie (Ireland) | fails-identity | 22,883 datasets, 172 organisations. No published per-user quota |
| data.gov.il (Israel, CKAN) | fails-identity | 1,203 datasets, 61 organisations. Files self-hosted (dataset/.../download/datafile.csv) |
| data.gov.ro (Romania national portal) | fails-identity | 5,255 datasets across 181 organisations. Files are hosted on-portal... |
| data.gov.ua (Ukraine national portal) | fails-identity | No published quota. Files self-hosted at /dataset/<uuid>/resource/<uuid>/download/<file> |
| data.govt.nz (New Zealand) | fails-identity | CKAN API answers 200 but the payload is replaced by an Incapsula/Imperva JS challenge wrapper on the HTML side... |
| data.qld.gov.au (Queensland Open Data Portal) | fails-identity | 188,887 datasets. No published per-user or per-file quota... |
| datos.gob.es (Spain) | fails-quota | Not machine-readable from here, CKAN action API returns 403 behind the WAF... |
| Estonia e-Residency | fails-quota | None. The programme issues a digital identity card + DigiDoc software and the right to run an EU company... |
| Europeana (EU cultural heritage aggregator) | fails-identity | No direct deposit at all, Europeana ingests metadata via accredited national aggregators... |
| India DigiLocker | fails-quota | 1 GB per account for citizen-uploaded documents (was 100 MB at launch) |
| opencolorado.org (regional CKAN, US) | fails-quota | Historic operator statement: 100 GB total platform storage, individual uploads up to 50 MB... |
| Socrata / Tyler Data & Insights... | fails-quota | No file storage at all. Community Users may create filtered views and visualisations of EXISTING public datasets... |

The 13 rejections fall into three groups and each says something different.

**Identity** is the largest. A portal that requires a public-body organisation fails the same
way a Shibboleth repository does, and the record's `dead_end.failure_class` is `identity`
rather than `quota`.

**Not-storage** is the second and it is the one worth reading. Several portals are metadata
harvesters rather than hosts: `data.gov` in the United States does not host data files at all
and has no self-service publisher path, and its sources are agency `data.json` inventories. A
harvester has no bytes to give.

**Quota** is the third, and it is a consequence rather than a cause. A 10 MB default resource
size is not a policy decision about a reader; it is a software default set for documents.

## The one qualifying provider, in the shape every other document uses

### HDX (Humanitarian Data Exchange)

The offer is a hosting account with no published per-user or per-file quota, because the
platform hosts the files itself on UN-backed S3 rather than metering a user allowance. Reads are
anonymous and unmetered (`reported`, 2026-10-21).

The constraint that binds is `write-gated`, not `identity`: an organisation request at
`data.humdata.org/org/request/new` is reviewed by OCHA before an upload is accepted. That is a
queue with a person in it, and a queue can be joined.

A new account costs an email address, and the organisation review is the part that decides
whether the account can publish. No signup was executed, so the record carries
`identity_probe: form-read`.

Observed behaviour: the gate is editorial rather than personal, which is why this is the only
qualifying record in a document of thirteen rejections. Nothing in this entry was probed: the
absent quota and the review step are both the project's own help pages
(`reported`, 2026-10-21).

Evidence: `data.humdata.org` (2026-10-21), record `dossier/storage/hdx-humanitarian-data-exchange.json`.
Verdict: `qualifies-with-caveat`.

## What this means for a composition

Nothing in this document belongs in a composition of 20 TiB.

The one thing worth carrying forward is the test. A portal that publishes a `data.json`
inventory is a harvester. A portal with an `organization_create` endpoint behind a login is a
publisher that requires an organisation. Neither is storage, and both look like it from a
search result.

The second thing worth carrying forward is HDX's shape as a template: a gate that a person
operates is a gate that can open, and it is a different class of obstacle from a federation that
cannot.
