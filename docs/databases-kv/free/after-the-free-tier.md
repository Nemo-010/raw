# What happens after the free tier ends, provider by provider?

The per-provider answer is scattered across the topic's documents. This page puts the answers in
one table, because the comparison is the finding: seventeen providers have a free tier to answer
for, one of them deletes the data on a published clock, and the rest stop in three different ways
that a reader must not conflate. Six more have no free tier, and the table says so rather than
leaving them out.

## The five outcomes

⛔ **Suspension, refusal and deletion are not the same event.** A suspended database wakes on the
next connection and has lost nothing. A refusing database answers an error and keeps the bytes. A
deleted database is gone. Every row below names which of the three it is, and the rows where the
vendor publishes no answer say so.

| outcome | what is lost | who is in it |
| --- | --- | --- |
| nothing, and the bill starts | money only | Nile, Firestore, DynamoDB |
| availability, until the next connection | latency, and an unattended job's success | Neon, Supabase, Atlas, Aiven, Turso, Prisma |
| the write path, or new connections | the ability to ingest, not the data | D1, KV, TiDB, Upstash, Weaviate, Qdrant, Pinecone |
| **the data, on a published clock** | **everything** | **CockroachDB Basic** |
| no free tier to answer for | not applicable | PlanetScale, Fauna, Xata, Chroma Cloud, Railway, Tembo |

## The matrix

Six columns, one per question. A dash means the vendor publishes no value; the source URL for
each is in the record named in the last column.

| provider | inactivity policy | deletion policy | storage cap | compute cap | connections | egress past the allowance | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Neon | compute suspended after 5 min idle, and it cannot be disabled on Free | none: "None of these limits delete your data" | 1 GB per project, 20 GB per account | 100 CU-hours per project per month | 10,000 pooled client connections | suspends compute until the next billing period | `neon` |
| Supabase | project paused after 7 days of low activity | none inside a year: paused projects are restorable up to 1 year | 500 MB per database | Nano compute, 0.5 GB RAM | set by compute size, not published as one number | billed at USD 0.09/GB, cached egress USD 0.03/GB | `supabase` |
| Cloudflare D1 | none | none: Time Travel gives 7 days of point-in-time recovery | 500 MB per database, 5 GB per account | 5M rows read and 100,000 written per day | 6 simultaneous connections per Worker invocation | not charged at all | `cloudflare-d1` |
| Cloudflare KV | none | none: a key persists unless the write sets an expiry | 1 GB per account | 100,000 reads and 1,000 writes per day | not published | not charged at all | `cloudflare-kv` |
| MongoDB Atlas M0 | paused after 30 days with zero connections | none: resumable, unless the version can no longer be restored to | 0.5 GB | 100 operations per second | 500 | throttled to a 1-second cooldown per connection, not billed | `mongodb-atlas-m0` |
| Firestore | none | none | 1 GiB, one free database per project | 50,000 reads, 20,000 writes, 20,000 deletes per day | not published | 10 GiB per month included, then billed at the network rate | `firestore` |
| DynamoDB | none: always-free, no expiry | none | 25 GB per region | 25 RCU and 25 WCU per region | not published | billed per GB out, with no free transfer allowance | `dynamodb` |
| Prisma Postgres | none published | none published | 2 GB | 200,000 operations per month | 10 direct and 10 pooled | no database egress fee; 10 GB a month on Prisma Compute then USD 0.025/GB | `prisma-postgres` |
| **Aiven** | **powers off after a period of inactivity, on two documented triggers** | **deleted after 180 days powered off; 7 days past end of life** | 1 GB per service | 1 GB RAM, 1 CPU, no pooling | 20 | not published | `aiven-free` |
| **Turso** | **archived after 10 days of inactivity** | none: the archive keeps the bytes and an unarchive restores service | 5 GB total across 100 databases | 500M rows read and 10M written per month | not published | not charged: rows are the meter | `turso` |
| **CockroachDB Basic** | none: Request Units scale to zero when idle | **all clusters deleted 30 days after the trial credits end without a payment method, and they cannot be restored** | 10 GiB | 50M Request Units per month | not published | billed separately, with no published allowance | `cockroachdb-basic` |
| TiDB Cloud Starter | none published | none published | 25 GiB row, 25 GiB columnar per organization | 250M Request Units per month | 400, or 5,000 with a spending limit | not published | `tidb-cloud-starter` |
| Upstash Redis | none published | none published | 250 MB | 500,000 commands per month | not published | 10 GB a month included, then billed | `upstash-redis` |
| Nile | **never pauses, stated by the vendor** | none published | 1 GB, then USD 1.50/GB | 50M query tokens per month | 500 | not published | `nile` |
| Qdrant Cloud | none published | none published | 4 GB disk | 1 GB RAM | not published | not published | `qdrant-cloud` |
| Weaviate Cloud | none published | none published | 1 GB sandbox | not published | not published | free during a promotional period, with charges possible later | `weaviate-cloud` |
| Pinecone | none published | none published | 2 GB per organization | 5 indexes, one project | not published | 1 GB a month on Starter | `pinecone` |
| PlanetScale | no free tier | not applicable | not applicable | not applicable | not applicable | network transfer billed from the first byte | `planetscale` |
| Fauna | no free tier: the service shut down on 2025-05-30 | the whole product | not applicable | not applicable | not applicable | not applicable | `fauna` |
| Xata | no free tier: a 14-day trial | the trial ends | trial only | trial only | trial only | not published | `xata` |
| Chroma Cloud | no free tier: USD 5 of credits | the credits run out | the credit balance | the credit balance | not published | folded into the credit | `chroma-cloud` |
| Railway | no free database: USD 1 of monthly credit | the credit runs out | the credit balance | the credit balance | not published | USD 0.05 per GB | `railway` |
| Tembo | no free tier: a dollar-denominated trial | the trial ends | the trial allowance | the trial allowance | not published | drawn from the same allowance | `tembo` |

## The two rows that matter most

⛔ **CockroachDB Basic is the only free relational database in this topic whose published end state
is that the data is gone.** The page the record cites states: "If the trial ends and a payment
method has not been provided, a 30 day grace period begins where your organization's clusters are
throttled ... If the end of the grace period is reached and no payment method has been added, all
clusters in the organization are deleted. Deleted clusters can not be restored." For a reader
with no budget, that is the definition of a tier that cannot hold state worth keeping.

⛔ **Aiven's free service powers off on inactivity and is deleted 180 days later.** It is the
second deletion clock: the free plan does not stay up, so a weekly job is exactly the workload that
lets it power off. The 180 days is the grace between the power-off and the deletion, not a generous
idle window.

Neither clock is on a pricing page. Both are on a documentation page that the record cites for
another number.

## The providers that answer with an absence

⭐ **"Not published" is a finding and it is recorded as one.** Eleven of the eighteen rows with a
free tier carry "not published" in the connections column, four in the egress column and one in the
compute column. In each case the record's `limits[]` or `egress.terms` names the gap and the URL that
was checked, because a dash in a table and a dash in a record mean different things: the table cell is
a summary, and the record says which page failed to state a number.

Three of those absences change a decision. Qdrant publishes a 4 GB disk and a 1 GB RAM ceiling and
no connection or egress figure, so the memory is what binds and a reader cannot size a client pool.
Aiven publishes no egress allowance at all, so a free service used for serving has an unpriced
path out. Turso publishes no connection limit, so the 10-day archive is not the only
unknown in front of a high-fanout design.

## Where the numbers come from

Every row is a record in [`../../../dossier/databases-kv/`](../../../dossier/databases-kv/). Where
a cell says "not published", the record's `limits[]` or `egress.terms` carries the URL that was
checked and found silent. The two attribution figures worth naming: Aiven's connection limit of 20
is on its free-tier documentation page, and Supabase's connection count is deliberately not a
number because the vendor sets it per compute size.
