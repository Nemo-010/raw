# Which free vector index is large enough to be useful?

Four managed vector databases offer a free tier and one of them caps objects rather than bytes.
The finding is that none of them beats pgvector on a free Postgres for a workload that already
has a free Postgres, and the egress cap decides the largest one.

## The comparison

Sorted by the size of the free index, in the unit each vendor states.

| provider | free index | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| Weaviate Cloud | 100,000 objects, 1 collection, 3 tenants | one collection | email | qualifies-with-caveat |
| Qdrant Cloud | 4 GB disk, 1 GB RAM, one cluster | 1 GB of RAM | email | qualifies |
| Pinecone Starter | 2 GB storage per organization, 5 indexes | 1 GB egress per month | email | qualifies-with-caveat |
| Chroma Cloud | USD 5 of credits | the credit balance | card | trial-only |
| pgvector on Neon or Supabase | the free Postgres storage | the compute-hour budget | email | qualifies |

## The numbers that decide the largest index

Three constraints decide it.

⛔ **Pinecone Starter caps egress at 1 GB per month.** The pricing page lists "Egress: Up to 1GB/mo"
on the Starter column beside the 2 GB of storage. 1 GB a month is 33 MB a day, and a retrieval
workload returning 1,536-dimensional float32 vectors returns 6 KiB per vector, so 33 MB a day is
about 5,500 vector reads a day before the storage cap is reachable. That is the constraint, not
the 2 GB.

**Qdrant's free tier is bounded by RAM, not disk.** 1 GB of RAM with 4 GB of disk means the index
that fits is the one that fits in memory, and the disk number is the ceiling that is never
reached.

⚠ **Weaviate caps collections at one.** 100,000 objects is generous and one collection is not: a
multi-tenant design that wants a collection per tenant stops immediately, and three tenants is
the whole fan-out.

## pgvector is the answer for most readers

Neon and Supabase both ship the `vector` extension at no extra cost. On the claimed Neon project,
`CREATE EXTENSION vector` succeeded in 1.1 s, `pg_extension` reported **version 0.8.0**, and a
`vector(3)` column answered an `ORDER BY e <-> '[1,2,3]'` query with distances 0.0 and 5.196 in
order (`measured`, 2026-10-22). The other extensions on the same project were `postgis 3.5.7`,
`timescaledb 2.17.1`, `pg_trgm 1.6` and `pgcrypto 1.3`. Building an index costs compute, and
compute is the free tier's scarce resource, so the trade is explicit: a separate vector service
costs no Postgres compute and adds a second system and a second counter.

For a workload that already has a free Postgres and fewer than about a million vectors, pgvector
wins on every axis except index build time.

## Pinecone

Pinecone's Starter gives **2 GB of serverless storage per organization**, **5 indexes**, **1
project**, **100 namespaces per index**, **1 GB of egress per month** and us-east-1 only. Builder
at USD 25 raises storage to 10 GB and egress to 10 GB; Standard is unlimited storage at USD 0.33
per GB-month with 100 GB of egress included.

The storage cap is per organization and there is one project, so there is no way to shard around
it. The egress cap is the one that binds a serving workload.

`Evidence:` `pinecone.io/pricing/` (read 2026-10-22): the Starter column with storage up to 2 GB,
egress up to 1 GB/month, 5 indexes and 100 namespaces per index; the Builder and Standard rows.
`docs.pinecone.io/reference/api/database-limits` (read 2026-10-22): the limits are split into
rate, object, operation and identifier pages, and the object-limits page is the authority for
per-plan counts.

`Verdict:` qualifies-with-caveat. 1 GB a month of egress is the number that ends a retrieval
service, and it is 3% of the storage allowance in traffic terms.

## Qdrant Cloud

Qdrant's free tier is **1 GB of RAM and 4 GB of disk**, one cluster, no high availability, and the
pricing FAQ says only that if data growth exceeds those limits "you can easily upgrade". There is no
published egress term, and **no published exhaustion behaviour**: nothing states whether a cluster at
1 GB of RAM throttles, refuses a write, or is suspended. That is a documented absence of a failure
mode, which is weaker evidence than a stated limit and is recorded as an absence rather than read as
headroom.

⚠ 4 GB of disk at 768 dimensions and 4 bytes per component is about 1.4 million vectors of raw
float32 before index overhead, and each vector is 3 KiB. The RAM bound arrives first.

`Evidence:` `qdrant.tech/pricing/` (read 2026-10-22): "The free tier includes 1GB RAM and 4GB disk
storage"; the free tier is "limited to 1GB RAM and 4GB disk without high availability".

`Verdict:` qualifies. The largest free disk among the managed vector services, with the RAM as
the real ceiling and an upgrade offered instead of a stated failure.

## Weaviate Cloud

Weaviate's Free tier gives **1 cluster per user**, **100,000 objects**, **1 GB of memory**, **10
GB of disk**, **1 collection** and **up to 3 tenants**, described as always free. The comparison
table repeats the object limit and the collection limit of 1.

The object cap is the unusual one: it bounds the record count and not the bytes, so 100,000 large
objects is the same allowance as 100,000 small ones.

`Evidence:` `weaviate.io/pricing` (read 2026-10-22): "Always free - 1 cluster per user";
"100,000 objects, 1 GB memory, 10 GB disk"; "1 collection, up to 3 tenants".

`Verdict:` qualifies-with-caveat. One collection is the constraint that decides it.

## Chroma Cloud

Chroma Cloud's Starter is **USD 0 with USD 5 of free credits** and usage-based billing after. The
open-source server is self-hostable, which is the last resort, after every hosted offer.

`Evidence:` `trychroma.com/pricing` (read 2026-10-22): Starter at USD 0 plus USD 5 of credits.

`Verdict:` trial-only.

## What did not work

- **Pinecone as a serving index**: 1 GB of egress a month is 33 MB a day, which is roughly 5,500
  vector reads a day at 6 KiB each (`inferred` from two documented numbers).
- **Pinecone sharding around 2 GB**: one project per organization and the storage cap is per
  organization, so there is nothing to shard into (`documented`, `pinecone.io/pricing/`).
- **Weaviate as a multi-tenant index**: one collection, three tenants (`documented`,
  `weaviate.io/pricing`).
- **Qdrant as a large index**: 1 GB of RAM is the ceiling and it is smaller than the 4 GB of disk
  the page leads with (`documented`, `qdrant.tech/pricing/`).
- **Chroma Cloud**, above: USD 5 is a trial.

## Chaining

**pgvector on a free Postgres plus a free Redis cache.** `Neon` with `vector` installed, and
`Upstash` in front for repeated queries. The scarce link is the CU-hour budget, because an index
build is the most expensive single operation a small compute can be asked to do.

**A managed vector index beside a free Postgres.** `Qdrant` for the index and `Neon` for the
relational truth. The scarce link is that the two must be kept consistent, and neither free tier
publishes a way to do that cheaply.
