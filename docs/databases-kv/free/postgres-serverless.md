# Which scale-to-zero Postgres survives a job that runs once a week?

Four providers sell a free Postgres that stops charging when it is idle. Three suspend compute or
pause the project rather than delete data, and each caps the thing that replaces a bill: compute
hours, a weekly activity clock, or operations. The fourth, Nile, states that it never pauses at
all. The answer for a weekly job is Supabase with a keep-alive, for a continuous small workload it
is Neon, and for an idle-tolerant multi-tenant shape it is Nile.

## The comparison

Sorted by how well each holds a workload that is not continuously connected. The binding
constraint column names the one that fails first.

| provider | free tier | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| Supabase | 500 MB database, 2 active projects, 5 GB egress | paused after 1 week of low activity | email | qualifies-with-caveat |
| Neon | 100 projects, 100 CU-hours each, 1 GB each, 5 GB egress each | 100 CU-hours per project | email | qualifies-with-caveat |
| Prisma Postgres | 200,000 operations/month, 2 GB, 50 databases | 200,000 operations and 10 connections | email | qualifies-with-caveat |
| Nile | 50M query tokens/month, 1 GB, unlimited databases and tenants | the token counter, with overage rather than a wall | email | qualifies-with-caveat |
| Xata | 14-day trial, then USD 0.012/hr + USD 0.28/GB-month | the trial ends | card | trial-only |
| Railway | USD 5 for 30 days, then USD 1/month | USD 1 a month | card | trial-only |

## The persistence test, applied

The question is not "how big" but "will the data still be there". The three free plans answer
differently, and the difference is the finding.

- **Neon suspends compute and never deletes.** The pricing page says exceeding CU-hours or the
  5 GB transfer "suspends compute until the next billing period", and exceeding storage "blocks
  writes", and then states "None of these limits delete your data" (`documented`, read
  2026-10-22). A suspended project wakes on the next connection.
- **Supabase pauses a project and keeps it restorable for a year.** The trigger is low activity
  "over a 7-day period", and the guide says "typically a few user requests to the database each
  day over the previous week is enough to keep the project from being paused" (`documented`, read
  2026-10-22). Two warning emails precede the pause.
- **Prisma's free tier does not publish a deletion clock** and does not pause, but the operation
  counter is low enough that the pause question rarely arises.

⭐ **The rule.** A paused project with a one-year restore window is storage with an availability
gap. A project deleted on a clock is a demo. Nothing in this class is deleted on a clock, and the
one thing that is, is the anonymous claimable project covered below.

## Neon

Neon's Free plan gives 100 projects, 10 branches per project, 1 GB of Postgres storage per
project with 20 GB across the account, 5 GB of public network transfer per project per month, and
**100 CU-hours per project per month**. A CU-hour is defined on the page as "compute size x hours
running", with the worked example `0.25 CU x 4 hours = 1 CU-hour`. Autoscaling reaches 2 CU
(8 GB RAM) on Free, and scale-to-zero happens after 5 minutes idle and **cannot be disabled on
Free**.

⭐ 100 CU-hours at the 0.25 CU minimum is about 400 wall-clock hours, which is 16 days of a
continuously connected minimum-size database. At 2 CU it is 50 hours. That arithmetic is the
whole finding: **the storage is 20 GB per account, not 100 GB**, and the compute to serve even
that is the binding number.

⚠ **Twenty, not one hundred.** One GB per project across 100 projects is a nominal 100 GB, and the
account-wide cap is 20 GB: the vendor page reads "1 GB/project, 20 GB account total". So the
multiplication buys 100 separate compute budgets and 20 GB of shared storage, which is a shape for
many small databases and not one large one.

The pooled endpoint accepts up to 10,000 client connections through PgBouncer in transaction
mode, with each pool sized at 0.9 x `max_connections`. On the compute observed in the probe
`max_connections` was 450.

**The anonymous lane.** A second Neon product provisions a Postgres with no signup, no email and
no card. `POST https://claimable.neon.tech/v1/agent/identity` with `{"type":"anonymous",
"capabilities":["postgres"]}` returns 201 with an identity assertion and a project id
(`measured`, 2026-10-22T02:41:42Z, 1480 bytes). The assertion exchanges at
`POST /v1/oauth2/token` for a 3,600-second bearer token, and
`GET /v1/projects/<id>/connection_uri?database_name=neondb&role_name=neondb_owner` returns a
working `postgresql://` URI.

⛔ That project is a demo and it says so. Unclaimed projects **expire in 72 hours**, are capped at
**100 MB of storage and 1 GB of transfer**, and claim codes expire in 15 minutes
(`documented`). The cap is enforced in the engine, not in the dashboard: `SHOW
neon.max_cluster_size` returns `100MB`, and a bulk insert failed at SQLSTATE 53100 with `could
not extend file because project size limit (100 MB) has been exceeded` (`measured`, 2026-10-22,
after 70 rows of 500 kB and 78 MB of reported size).

Two numbers from that probe matter for anyone building an agent that provisions its own
database. A cold anonymous project took **1,750 ms per single-row autocommit insert** over ten
inserts, which is idle-wake latency and not query cost. Bulk insert of 35 MB ran at 1.61 MB/s.
Both are usable for a test and neither is usable for a service.

`Evidence:` `neon.com/pricing` (read 2026-10-22): 100 projects, 100 CU-hours/project, 1 GB and
20 GB storage, 5 GB egress, 5-minute scale-to-zero. `neon.com/docs/reference/claimable-neon`
(read 2026-10-22): 72-hour expiry, 100 MB, 1 GB transfer. Probe on 2026-10-22T02:41Z to
02:49Z: 201, a Postgres 17.11 connection, a roundtrip, and the 53100 cap.

`Verdict:` qualifies-with-caveat. The free tier is the best continuous small-workload Postgres
here. The anonymous lane is a 72-hour sandbox and not a database.

## Supabase

Supabase's Free plan gives a **500 MB** database on shared CPU with 500 MB RAM, **2 active
projects**, **5 GB of egress** and 5 GB of cached egress, plus unlimited API requests. The pause
is the finding: a Free project is paused after **1 week of low activity**, and paused projects do
not count against the 2-project limit, so a paused project is a free parked project.

The restore path is not the 90 days that the 2024-06-24 changelog announced. The current pausing
guide says a paused project is restorable "for up to 1 year after it was paused", and the reason
it gives is that backups are retained for a limited period and platform changes may not be
backward compatible with older ones.

⚠ The egress term is the sharp edge. Free includes 5 GB and publishes **no overage price**, which
means the sixth gigabyte is not a bill. Compare the paid row on the same page: 250 GB included,
then USD 0.09 per GB. There is no free-plan equivalent, so a read-heavy workload stops rather
than costs.

`Evidence:` `supabase.com/pricing` (read 2026-10-22): 500 MB database, 2 active projects, 5 GB
egress, the pausing row "After 1 week of inactivity". `supabase.com/docs/guides/platform/free-project-pausing`
(read 2026-10-22): the 7-day low-activity test, the two warning emails, and the one-year restore
window.

`Verdict:` qualifies-with-caveat. The best free Postgres for a job that runs weekly, provided
the job touches the database at least once every few days.

## Prisma Postgres

Prisma's Free tier is **200,000 operations a month**, **2 GB of storage**, **50 databases**, and
a connection limit of **10 direct and 10 pooled** with a 60-minute idle timeout. Every query
counts as an operation, so 200,000 a month is 6,667 a day and about 0.08 a second sustained.

The 50 databases is the widest per-tenant fan-out in this class, and the 10-connection ceiling is
what stops it: a pooler in front of a database that accepts 10 connections is still 10. The plan
table lists both numbers on the same row.

Prisma Compute adds a separate Free allowance of 1 million requests, 360 GB-hours of provisioned
memory, 4 vCPU-hours of active CPU and 10 GB of outbound bandwidth. The Accelerate cache product
retires on 2026-12-01.

`Evidence:` `prisma.io/pricing` (read 2026-10-22): 200k operations, 2 GB, 50 databases,
connection limit pooled 10 and direct 10, idle timeout 60 minutes.

`Verdict:` qualifies-with-caveat. The operation counter is the constraint, and it is small
enough that this is a prototype tier rather than a service tier.

## Nile

Nile is a multi-tenant Postgres and its free tier is shaped the opposite way from the three above.
The limits are **per workspace across unlimited databases and unlimited tenants**, so tenant count
costs nothing and the meter is query volume: **50 million query tokens a month**, then USD 0.06 per
million additional tokens. **1 GB of storage** is included, then USD 1.50 per additional GB. The Free
column allows **500 connections**, one region and one branch, with one day of backup retention.

⭐ **It is the only provider in this topic whose vendor states that the free database does not
pause.** The pricing page's own FAQ answers "Does my db pause in the free tier?" with "No, the db
never pauses. We don't have any cold start time on the free tier." The architecture page supports
it: storage and compute are decoupled and the database "scales to zero with no cold start time".

**What happens at the limit is an overage, not a refusal.** The FAQ: "We will reach out to you when
you are nearing your usage limits. You can typically pay for additional capacity without having to
move to a higher tier. This is true even when you are on the free tier." That is the opposite of
TiDB, which denies new connections, and the opposite of Neon, which suspends compute.

⚠ **What it does not publish is anything about time.** No inactivity policy, no expiry, no deletion
clock. The one day in the Free column is backup retention and not a retention clock. So the honest
answer to "what happens after the free tier" is: nothing happens to the data, and the bill starts.
That is a better answer than most in this topic and it is still an absence of a published policy
rather than a published policy.

⚠ **A query token is a discretionary meter.** The page defines it as "abstract units of CPU and
memory used when queries are executed" and gives no conversion, so 50 million tokens cannot be
expressed in rows or bytes. There is a price per unit and no ceiling a reader can size a job
against.

`Evidence:` `thenile.dev/pricing` (read 2026-10-22): the Free column as above, and the FAQ answers
quoted, which the page renders collapsed and which were read through the search index.
`thenile.dev/docs/getting-started` (read 2026-10-22): the scale-to-zero-with-no-cold-start claim.

`Verdict:` qualifies-with-caveat. No pause, no deletion clock, an overage instead of a wall, and a
meter with no published conversion.

## Xata

Xata has **no free tier**. Xata Cloud starts with a **14-day free trial**, then a micro instance
costs USD 0.012 an hour, about USD 9 a month, plus USD 0.28 per GB-month of storage. A card is
required after the trial. The Apache-2.0 core is free to self-host and is a different product.

`Evidence:` `xata.io/pricing` (read 2026-10-22): "Open source is free forever. Xata Cloud starts
with a 14-day free trial."

`Verdict:` trial-only. The 15 GB always-free tier that many comparisons still print no longer
exists.

## Railway

Railway gives **USD 5 of credit for 30 days**, then **USD 1 a month** which does not roll over.
One vCPU and 0.5 GB per service. USD 1 a month is roughly one small always-on container and no
database budget.

`Evidence:` `railway.com/pricing` (read 2026-10-22): the 30-day trial credit and the USD 1
monthly amount.

`Verdict:` trial-only.

## What did not work

- **Xata**, above: the always-free tier was retired and the trial is 14 days (`xata.io/pricing`,
  2026-10-22).
- **PlanetScale**: no free plan since March 2024, and every database is paid from creation
  (`support.planetscale.com`, read 2026-10-22). Recorded under the distributed-SQL document.
- **Railway**, above: USD 1 a month is not a database budget.
- **Chroma Cloud**: Starter is USD 0 plus USD 5 of credits, which is a spend cap and not a tier.
  Recorded under the vector document.
- **Neon's 100-project multiplication as one database**: 100 projects share an account-wide 20 GB
  storage cap, so the multiplication gives 20 GB of storage and 100 separate compute budgets, not
  100 GB in one place (`documented`, `neon.com/pricing`).
- **Supabase's 5 GB egress as a serving allowance**: 5 GB a month is 0.17 GB a day, which is
  0.02% of a 1 TiB a day working set (`inferred` from two documented numbers).

## Chaining

**Free Postgres behind a free tunnel.** `Neon or Supabase free tier` plus a Cloudflare Tunnel
gives a public Postgres endpoint with no card. The scarce link is not the database and not the
tunnel; it is the free plan's egress allowance, which is 5 GB a month on both and is smaller
than the tunnel's capacity by orders of magnitude.

Both free plans ship the `vector` extension. It was installed and queried on the claimed project
rather than merely listed: `CREATE EXTENSION vector` succeeded in 1.1 s, `pg_extension` reported
**version 0.8.0**, a `vector(3)` column accepted two rows, and `ORDER BY e <-> '[1,2,3]'` returned
distances 0.0 and 5.196 in order (`measured`, 2026-10-22). The other extensions available on the
same project were `postgis 3.5.7`, `timescaledb 2.17.1`, `pg_trgm 1.6` and `pgcrypto 1.3`.
The scarce link is the CU-hour budget, because building an index is the most expensive thing to
ask of a small compute.
