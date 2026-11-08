# Which free document store or cache survives a month of silence?

Four providers, and two of them provision a working database with no account at all. The
document stores cap storage at half a gigabyte and the Redis tier caps commands. The finding that
matters is the idle clock: Atlas pauses at 30 days, Supabase at 7, and the anonymous lanes at 3
days and 72 hours.

## The comparison

Sorted by how long the data survives without being touched.

| provider | free tier | idle clock | identity | verdict |
| --- | --- | --- | --- | --- |
| Firestore | 1 GiB, 50k reads/day, one free database | none | email | qualifies |
| DynamoDB | 25 GB, 25 RCU, 25 WCU per region | none | card | qualifies-with-caveat |
| MongoDB Atlas | 512 MB, 500 connections, 100 ops/s | paused at 30 days with zero connections | email | qualifies-with-caveat |
| Upstash Redis | 250 MB, 500k commands/month, 1 database | 3 days for an anonymous database | anonymous or email | qualifies |
| Chroma Cloud | USD 5 of credits | spend cap | card | trial-only |

## The idle clock is the first question

⚠ A document store is usually written by an event and read by a person, and the gap between the two
is where a free tier's clock fires. Atlas is explicit: "Atlas automatically pauses Free clusters
after 30 days of inactivity where there are zero connections to the cluster", and it recommends
exporting a copy before a long pause. That is the longest published idle clock in this topic
short of Aiven, which does not pause at all.

Upstash's anonymous lane is the shortest at **3 days**. The Neon anonymous lane is **72 hours**.
Neither is a storage clock; both are trial clocks.

## MongoDB Atlas

The free cluster, formerly M0, gives **512 MB** of storage with **replication factor 3** and no
ability to configure the size. Four numbers beside the storage are what actually bind:

- **100 operations per second**, enforced by throttling with a one-second cooldown per connection
  once the queue exceeds the limit.
- **500 connections** maximum.
- **10 GB in and 10 GB out per rolling seven-day period**, which is the number that ends a
  serving use. Exceeding it throttles network speed.
- **One free cluster per project**, with no sharding and no network peering.

30 days of zero connections pauses the cluster, and it resumes "unless the paused cluster was
running on an old version that Atlas can't restore to the current version".

`Evidence:` `mongodb.com/docs/atlas/reference/free-shared-limitations/` (read 2026-10-22): 500
connections, 100 operations/second, 10 GB in and 10 GB out per 7 days, auto-pause at 30 days with
zero connections, replication factor 3, one free cluster per project.

`Verdict:` qualifies-with-caveat. 512 MB is a hard wall and 100 ops/s is a throughput ceiling
that no storage allowance can exceed.

## Upstash Redis

Upstash's Free tier gives **250 MB of data**, **500,000 commands per month**, **10 GB of monthly
bandwidth**, **10,000 commands per second**, a 10 MB maximum request, a 100 MB maximum record and
**one database**. No card is required.

500,000 commands a month is 16,600 a day, which is a different shape from the 10,000 a day that
the pre-2025-03 plan gave. A burst is fine and a steady one command a second is not: one a second
is 2.6 million a month.

The anonymous lane was measured on 2026-10-22 and it works. A `POST` to
`https://upstash.com/start-redis` with any UUIDv4 in an `Idempotency-Key` header returned **200**
with 3,239 bytes of markdown carrying an endpoint, a bearer token and `Expires: 2026-10-25 (3
days from creation)` (`measured`, 2026-10-22T02:53:12Z). Against that endpoint, `["PING"]`
returned `{"result":"PONG"}`, `SET k1 v1` returned `OK`, `GET k1` returned `v1`, and `DBSIZE`
returned 1, each in 0.73 to 0.92 seconds.

⛔ The database is deleted after 3 days unless claimed in a browser. The response says so, and it
also warns not to store sensitive data because the database is not tied to an account.

⚠ One measured gap: the documented developer API host `api.upstash.com` **did not resolve** from
this machine on 2026-10-22, while the per-database endpoint worked. A client that uses the
management API is relying on a host that did not resolve.

`Evidence:` `upstash.com/docs/redis/overall/billing` (read 2026-10-22): the Free column and the
sentence that an account with a payment method cannot have free databases. Probe on 2026-10-22:
the POST returned 200 with credentials, and four REST commands round-tripped.

`Verdict:` qualifies. The cheapest working cache here, and the only one obtainable with no
identity at all.

## Firestore

Firestore gives **1 GiB stored**, **50,000 document reads per day**, **20,000 writes per day** and
**20,000 deletes per day**, and exactly **one free database per project**. A project may hold up
to 100 databases and only one of them is free, so a multi-tenant design that wants a database per
tenant is a paid feature.

The one-database rule is the constraint a per-tenant design meets first, not the 1 GiB.

`Evidence:` `firebase.google.com/docs/firestore/quotas` (read 2026-10-22): the free quota table and
"Cloud Firestore allows exactly one free database per project".

`Verdict:` qualifies. 1 GiB with no idle clock and client SDKs is the most usable free document
store here.

## DynamoDB

The AWS Free Tier includes **25 GB of storage**, **25 read capacity units** and **25 write
capacity units** per region per payer account, plus 2.5 million Streams read requests a month.
An RCU is one strongly-consistent 4 KB read per second, so 25 RCU is 25 reads a second, and 25
WCU is 25 writes a second of a 1 KB item.

The throughput is the cap and the storage will never fill. A card is required because an AWS
account requires a payment instrument.

`Evidence:` `aws.amazon.com/dynamodb/pricing/` (read 2026-10-22): the 25 WCU and 25 RCU
allowance and the first 25 GB of storage per region, both stated in the page's worked examples.

`Verdict:` qualifies-with-caveat. 25 GB that never expires and never pauses, at a throughput
that fits a prototype.

## Chroma Cloud

Chroma Cloud's Starter is **USD 0 plus USD 5 of free credits**, with usage-based billing after.
That is a spend cap and not a tier: it is a trial that happens to have no expiry date, and a
vector index spends five dollars quickly.

`Evidence:` `trychroma.com/pricing` (read 2026-10-22): Starter at USD 0 with USD 5 of credits.

`Verdict:` trial-only.

## What did not work

- **Atlas M0 as a serving database**: 10 GB out per rolling seven days is 1.43 GB a day, which is
  0.14% of a 1 TiB a day working set (`inferred` from a documented number).
- **Atlas M0 as an ingest**: 100 operations a second, a one-second cooldown once the queue
  exceeds it, and 512 MB with no overage (`documented`,
  `mongodb.com/docs/atlas/reference/free-shared-limitations/`).
- **Firestore as a per-tenant store**: exactly one free database per project, so a tenant per
  database is paid (`documented`, `firebase.google.com/docs/firestore/quotas`).
- **Chroma Cloud**, above: USD 5 of credits is a trial.
- **The Upstash management API**: `api.upstash.com` did not resolve on 2026-10-22 while the
  per-database endpoint worked (`measured`).
- **The 10,000-commands-a-day Upstash figure**: it is the pre-2025-03 plan; the page states
  500,000 a month (`documented`, `upstash.com/docs/redis/overall/billing`).

## Chaining

**Redis in front of a free Postgres.** `Upstash` at 500,000 commands a month in front of `Neon`
at 100 CU-hours. The scarce link is the command counter: a cache that misses on every request
spends the month in a week.

**An anonymous database for a demo, a real one for the product.** The Upstash anonymous lane and
the Neon claimable lane both provision in one request with no identity, and both expire. The
scarce link is the claim step, which is a human in a browser and cannot be automated.
