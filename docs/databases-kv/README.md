# Where does state live after the free tier ends?

A free managed database is a promise that the state outlives the offer. This topic tests that
promise. It separates **persistence** from **availability**: a free Postgres that suspends its
compute every five minutes still holds the bytes, and a free Postgres that is deleted after a
week of silence does not. Both are called free.

Five classes share the topic, and the class decides which constraint binds first.

| class | free shape | who is in it | what binds |
| --- | --- | --- | --- |
| serverless Postgres with scale-to-zero | 0.5 to 2 GB per project, compute-hours | Neon, Supabase, Prisma | compute-hours and an idle clock |
| always-on managed Postgres | 1 GB, powers off on inactivity | Aiven, Xata (trial only) | an inactivity power-off, then 180 days to deletion |
| distributed SQL and serverless MySQL | 5 to 25 GiB, request units | TiDB Starter, CockroachDB Basic | RUs per month, and a card |
| edge KV and SQLite | 1 to 5 GB, daily row budgets | Cloudflare KV, D1, Turso | rows or writes per day |
| document, cache and vector | 250 to 512 MB, or a fixed index | Atlas, Upstash, Firestore, Pinecone, Qdrant | absolute storage, or ops per second |

## The rule that decides this topic

⛔ **A free database that loses data on a clock is not storage. It is a demo.**

⭐ Apply three tests before building on one, in this order. First, does the free plan delete the
data, or does it suspend compute or block writes? Neon and D1 suspend or block; Supabase pauses
and keeps the data restorable for a year; an unclaimed anonymous project is deleted in 72 hours.
Second, what wakes it, and how long does that take? Third, what is the total after the cap, in
the unit actually stored?

The three answers are different products, and the headline is none of them.

## The constraint that decides most of this topic

⚠ On Postgres the storage number is rarely the binding one. Neon gives 1 GB per project across 100
projects, capped at **20 GB per account** rather than the 100 GB the multiplication suggests, and
then caps compute at **100 CU-hours per project** while autoscaling to 2 CU. A workload that holds one connection open exhausts that in about 100 hours.
The storage is generous and the compute is not.

On everything else the binding constraint is a **counter**, not a size: 500,000 Redis commands a
month, 100,000 D1 rows written a day, 200,000 Prisma operations a month, 100 Atlas operations a
second, 50,000 Firestore reads a day. A counter is the number to design against; a size is the
number a vendor markets.

## The two anonymous offers

Two providers in this topic provision a working database with no account, no email and no card.
Both were measured, and both expire.

- `POST https://upstash.com/start-redis` with any UUIDv4 in an `Idempotency-Key` header returns a
  working Redis endpoint and token, deleted after 3 days unless claimed (`measured`).
- `POST https://claimable.neon.tech/v1/agent/identity` returns an identity assertion that
  exchanges for a Postgres connection URI, with a 72-hour expiry, a **100 MB** storage cap and
  **1 GB** of transfer (`measured`).

Neither is storage. Both are the cheapest way to test a schema or a client library before
committing an email address, and the 100 MB cap on the Neon path is the tightest number in this
topic.

## The documents

| document | answers |
| --- | --- |
| [`free/postgres-serverless.md`](free/postgres-serverless.md) | which scale-to-zero Postgres survives a job that runs weekly, and what the idle clock is |
| [`free/postgres-always-on.md`](free/postgres-always-on.md) | the free relational tiers that do not scale to zero, and what ends each one instead |
| [`free/after-the-free-tier.md`](free/after-the-free-tier.md) | the per-provider answer to what happens when the free tier ends: inactivity, deletion, storage, compute, connections and egress |
| [`free/mysql-and-distributed.md`](free/mysql-and-distributed.md) | the largest card-free relational allowance, and the RU counters |
| [`free/edge-kv-and-sqlite.md`](free/edge-kv-and-sqlite.md) | the write-per-day and row-per-day budgets of the edge databases |
| [`free/document-and-cache.md`](free/document-and-cache.md) | document stores, Redis, and the anonymous Redis lane |
| [`free/vector.md`](free/vector.md) | index size, dimension limits, and why pgvector usually wins |
| [`paid/postgres-floor.md`](paid/postgres-floor.md) | the smallest monthly payment that removes the pause or the clock |
| [`paid/vector-floor.md`](paid/vector-floor.md) | per-GB vector pricing and the crossover against a free index |

## What is dead in this topic

**Six providers carry a non-qualifying verdict**: `fauna` and `planetscale` are `dead`, and
`chroma-cloud`, `railway`, `tembo` and `xata` are `trial-only`. A further set of dead ends are
misuses of a live provider rather than rejected providers, and each is in a document's "What did not
work" section. Three matter most:

- **PlanetScale** has had no free plan since March 2024, confirmed on its own support page. Every
  listicle that prints one is three years stale.
- **Fauna** shut down on 2025-05-30. Its status page still answers HTTP 200 with a shutdown
  banner, which is why a status code is not a finding.
- **Xata** retired its always-free 15 GB tier. Xata Cloud is a 14-day trial.

## The records

Every provider named in this topic has one record. A provider named in a document with no facts of
its own is in that document's "also seen" line and has no record, because an empty record is noise.

| slug | provider | verdict | confidence |
| --- | --- | --- | --- |
| `neon` | Neon (Lakebase Postgres) | qualifies-with-caveat | measured |
| `supabase` | Supabase | qualifies-with-caveat | documented |
| `prisma-postgres` | Prisma Postgres | qualifies-with-caveat | documented |
| `xata` | Xata | trial-only | documented |
| `railway` | Railway | trial-only | documented |
| `tembo` | Tembo | trial-only | documented |
| `aiven-free` | Aiven | qualifies-with-caveat | documented |
| `tidb-cloud-starter` | TiDB Cloud Starter | qualifies | documented |
| `cockroachdb-basic` | CockroachDB Cloud Basic | qualifies-with-caveat | documented |
| `planetscale` | PlanetScale | dead | documented |
| `cloudflare-d1` | Cloudflare D1 | qualifies | documented |
| `turso` | Turso | qualifies | documented |
| `cloudflare-kv` | Cloudflare Workers KV | qualifies-with-caveat | documented |
| `mongodb-atlas-m0` | MongoDB Atlas free cluster | qualifies-with-caveat | documented |
| `upstash-redis` | Upstash Redis | qualifies | measured |
| `firestore` | Cloud Firestore | qualifies | documented |
| `dynamodb` | Amazon DynamoDB | qualifies-with-caveat | documented |
| `nile` | Nile | qualifies-with-caveat | documented |
| `qdrant-cloud` | Qdrant Cloud | qualifies | documented |
| `weaviate-cloud` | Weaviate Cloud | qualifies-with-caveat | documented |
| `pinecone` | Pinecone | qualifies-with-caveat | documented |
| `chroma-cloud` | Chroma Cloud | trial-only | documented |
| `fauna` | Fauna | dead | measured |

## Where a number here came from

Every number carries a rung and a read date. `measured` means a request was made from this
machine on 2026-10-22 and the transcript is in the record's `evidence`. `documented` means a
first-party page was read on 2026-10-22. `reported` means a third party, and no table cell rests
on it alone.

The records are in [`../../dossier/databases-kv/`](../../dossier/databases-kv/). When a document
and a record disagree, the record is right.

## Records that no other document names

This list holds each `measured` or `documented` record of this topic that no other document of
`docs/` names.

<!-- generated:start topic=databases-kv kind=uncited -->
Every `measured` or `documented` record of this topic is named by a document.
<!-- generated:end -->
