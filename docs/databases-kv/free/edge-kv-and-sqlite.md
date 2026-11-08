# Which edge database holds a write-heavy workload?

Three providers put SQLite or a key-value store at the edge with a free tier. All three meter the
write path separately from the read path, and in all three the write budget is one to three
orders of magnitude smaller than the read budget. The answer for a read cache is any of them; for
an ingest there is no free option in this class.

## The comparison

Sorted by write budget, which is the number that ends most designs.

| provider | free write budget | free read budget | storage | idle / deletion clock | verdict |
| --- | --- | --- | --- | --- | --- |
| Cloudflare D1 | 100,000 rows written/day | 5,000,000 rows read/day | 500 MB/database, 5 GB/account | none: storage persists and the daily counters reset | qualifies |
| Turso | 10,000,000 rows written/month | 500,000,000 rows read/month | 5 GB total | archived after 10 days idle; no deletion on Free | qualifies-with-caveat |
| Cloudflare KV | 1,000 writes/day | 100,000 reads/day | 1 GB/account | none: a key persists unless the write sets an expiry | qualifies-with-caveat |

## The read-to-write ratio is the finding

D1's ratio is 50 reads per written row. Turso's is also 50. KV's is 100. All three say the same
thing: this class is a read cache with a small write path, and a design that writes one row per
request is the wrong shape for every one of them.

⚠ **A fourth column decides more than the ratio for an unattended job.** A counter resets; a
retention clock does not. Turso archives an idle
free database after ten days, so the 10-million-row monthly write budget is unreachable by any job
that runs less often than that. D1 and KV have no such clock.

Converted to a sustained rate, which is the only comparable form:

| provider | writes per second, sustained | reads per second, sustained |
| --- | --- | --- |
| Cloudflare D1 | 1.16 | 57.9 |
| Turso | 3.86 | 193 |
| Cloudflare KV | 0.0116 | 1.16 |

⭐ The KV write rate is under one write per minute. That is the arithmetic behind the sentence "the
KV has to be a cache and not a store".

## Cloudflare D1

D1 gives **10 databases**, **500 MB per database**, **5 GB per account**, **5 million rows read
per day** and **100,000 rows written per day** on the Workers Free plan. Row and BLOB size is
capped at **2,000,000 bytes**, a SQL statement at 100 KB, bound parameters at 100, a query at 30
seconds, and a Worker may issue 50 D1 queries per invocation on Free.

The behaviour at the limits is documented and it is a wall rather than a bill. At the daily read
or write limit "you will not be able to run queries against D1" and the API returns errors; at
the storage limit you must delete data before you can insert, create or alter tables, or create
indexes. Free limits reset daily at 00:00 UTC.

⚠ One detail decides query design: a row read is a row **scanned**, not a row returned. A full scan
of a 5,000-row table spends 5,000 of the 5 million daily reads, and an unindexed filter counts
every row it examined.

`Evidence:` `developers.cloudflare.com/d1/platform/limits/` (read 2026-10-22): 10 databases, 500
MB, 5 GB, 7-day Time Travel, 50 queries per invocation, 2,000,000-byte rows, 30-second queries.
`developers.cloudflare.com/d1/platform/pricing/` (read 2026-10-22): 5 million rows read and
100,000 rows written per day, the reset at 00:00 UTC, and the failure behaviour at each limit.

`Verdict:` qualifies. The best free SQL option in this class, on the strength of 500 MB per
database repeated ten times.

## Turso

Turso gives **100 databases**, **5 GB of storage**, **500 million rows read per month**, **10
million rows written per month** and 3 GB of sync on the Free plan, with 1-day audit logs and no
point-in-time restore. The Developer plan at USD 4.99 adds unlimited databases and 9 GB.

The 5 GB is a total across all databases, so a hundred databases average 50 MB each. The
500-database and 9-GB figures that circulate are the Developer plan and not Free.

⛔ **The free plan archives an idle database after 10 days.** Turso's own CLI reference states it
plainly: "Databases get archived after 10 days of inactivity for users on a free plan." An archived
database must be unarchived before it can be used, and the platform API exposes that as a
`groups/unarchive` endpoint, so the state is reachable programmatically and not only through the
CLI. Turso's own announcement of the paid Hobby plan sells "your databases never archived or scale
to zero" as the upgrade, which is the vendor stating that the free plan does archive.

The clock is not a deletion: the bytes survive, and no point-in-time restore is included on Free.
It is still the constraint that ends the obvious use of the tier. A quarterly job finds an archived
database every time it runs, and 10 million rows a month of write budget behind a 10-day archive is
a budget the job cannot reach.

The pricing page does not carry this clock. The finding is on the CLI reference and the API
reference, both first-party.

The API answered an unauthenticated request with a 401, `{"error":"token contains an invalid
number of segments"}`, which proves the platform API exists and is token-authenticated
(`measured`, 2026-10-22T02:51Z, 56 bytes).

`Evidence:` `turso.tech/pricing` (read 2026-10-22): Free column 100 databases, 5GB, 500 Million
rows read, 10 Million rows written, 3GB sync; Developer USD 4.99 with unlimited databases and
9GB. `docs.turso.tech/cli/group/unarchive` (read 2026-10-22): "Databases get archived after 10 days
of inactivity for users on a free plan". `docs.turso.tech/api-reference/groups/unarchive` (read
2026-10-22): the unarchive endpoint. Probe of `api.turso.tech/v1/organizations` on 2026-10-22: 401.

`Verdict:` qualifies-with-caveat. The largest row-write budget in this class by a factor of three,
the narrowest per-database storage, and a 10-day archive clock that binds before either.

## Cloudflare Workers KV

KV gives **100,000 reads per day**, **1,000 writes per day to different keys**, **1 write per
second to the same key**, **1 GB per account**, 1 GB per namespace, 1,000 namespaces, **512-byte
keys** and **25 MiB values**, with keys per namespace unlimited. The minimum cacheTtl is 30
seconds. On the paid plan reads, writes and storage are all unlimited.

The 25 MiB value cap is generous for a KV store and it is not the constraint. The 1,000 writes a
day is, and the 1-write-per-second-per-key limit is the second wall that a counter or a lock hits
immediately.

`Evidence:` `developers.cloudflare.com/kv/platform/limits/` (read 2026-10-22): the Free column as
above, including 1,000 writes/day, 1 write/second to the same key, 512-byte keys and 25 MiB
values.

`Verdict:` qualifies-with-caveat. A read cache with a write path too small for anything that
changes per request.

## What did not work

- **KV as a store**: 1,000 writes a day is 11.6 milliwrites per second, so any per-request write
  exceeds the budget in the first hour (`inferred` from a documented number).
- **D1 as an ingest target**: 100,000 rows written a day is 1.16 rows a second sustained, and a
  batch load of a million rows needs ten days (`inferred` from `d1/platform/pricing/`).
- **Turso's 500-database figure**: it is the Developer plan, not Free. Free is 100
  (`documented`, `turso.tech/pricing`).
- **Turso as the replica for a job that runs less often than weekly**: the free plan archives an
  inactive database after 10 days, and an archived database must be unarchived before use
  (`documented`, `docs.turso.tech/cli/group/unarchive`).
- **D1 with a large row**: the 2,000,000-byte row cap is the engine's, and a 5 GB database of
  2 MB rows is 2,500 rows in the largest table (`documented`, `d1/platform/limits/`).
- **Any of these as a system of record**: all three publish a daily or monthly counter with no
  paid-lift on the free plan, so the counter is a wall and not a bill.

## Chaining

**KV in front of a free Postgres.** `Cloudflare KV` reads at 100,000 a day and a Neon or Supabase
database holds the truth. The scarce link is the 1,000 KV writes a day, which means the cache
must be filled by the origin rather than by the request path.

**D1 as per-tenant state with Turso as the replica.** Ten D1 databases at 500 MB and a hundred
Turso databases at 50 MB average is 10 GB of free relational state across 110 namespaces. The
scarce link is Turso's 10-day archive: a replica nobody reads for a fortnight stops serving until
it is unarchived, so the chain needs a keep-alive per tenant, and that keep-alive is a read against
a database Turso is archiving for being unread.
