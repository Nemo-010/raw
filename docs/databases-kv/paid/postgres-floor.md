# What is the smallest monthly payment that removes the pause or the clock?

Three providers sell a Postgres small enough to be a rounding error and large enough to stop
suspending. ⭐ **The answer is USD 5 on Aiven for 8 GB of storage with no inactivity power-off and
no connection pooling, or USD 0.106 per CU-hour on Neon if the workload is bursty enough that a
monthly minimum is wasted.** Aiven's Developer tier is the one page in this topic that states the
paid step removes the clock: "Developer tier services are not automatically powered off when
inactive".

## The comparison

Sorted by the smallest monthly amount that removes the free tier's binding constraint.

| provider | smallest paid step | what it removes | monthly price |
| --- | --- | --- | --- |
| PlanetScale PS-5 | 1/16 vCPU, 512 MiB, single node | nothing: there is no free tier to remove | USD 5, compute only |
| Aiven Developer | 1 GB RAM, 8 GB storage, no pause | the 1 GB storage cap and the inactivity power-off | USD 5 |
| Neon Launch | 500 GB egress/project, compute hours billed | the CU-hour cap and the 5 GB egress cap | USD 0.106 per CU-hour, no minimum |
| Railway | 1 vCPU, 0.5 GB per service | the trial | USD 1 of usage, not a database |
| Supabase Pro | no pause, 8 GB database, 250 GB egress | the 7-day pause and the 500 MB cap | USD 25 |
| PlanetScale PS-10 | 1/8 vCPU, 1 GiB, three nodes | nothing: there is no free tier to remove | USD 30 |

## The arithmetic that decides it

The table sorts by the smallest monthly amount, and two rows tie at USD 5 for different things. **Aiven
Developer is the cheapest monthly payment that buys a usable database**, because the USD 5 includes 8
GB of storage against a tier that stops powering off. PlanetScale's PS-5 is USD 5 for compute alone:
network-attached storage, backups and network transfer are billed separately from the SKU rate, so its
monthly total is above USD 5 and by an amount the pricing page does not cap.

A free Supabase project is 500 MB and pauses at 7 days. Pro is USD 25 and gives an 8 GB database,
250 GB of egress and no pause. That is 16 times the storage, 50 times the egress and no clock for
USD 25.

A free Neon project is 1 GB with 100 CU-hours. Launch is metered at USD 0.106 per CU-hour with no
monthly minimum, so a workload that runs 100 CU-hours a month costs USD 10.61 and one that runs
ten costs USD 1.06. For a bursty workload Neon's paid step is the cheapest in the set; for a
continuously connected one it is the most expensive.

Aiven's Developer tier at USD 5 gives 8 GB of always-on storage and 1 GB of RAM. At the same 8 GB
Supabase Pro costs USD 25 and Neon costs USD 0.35 per GB-month above the free 1 GB, which is
USD 2.45 for 7 GB of storage plus the compute.

⚠ **PlanetScale is not four to six times the next entry.** The USD 30 figure is the three-node
PS-10 row. The single-node floor is PS-5 at USD 5, so PlanetScale's compute floor is the same USD 5
as Aiven's whole tier. Per node, PlanetScale is the cheaper of the two by a wide margin; per usable
database it is unquantifiable because the storage line is separate.

## Aiven Developer

USD 5 a month buys 1 GB of RAM and **8 GB of total storage**, which is the cheapest way to get
above 1 GB of managed Postgres. The next step is Hobbyist from USD 12.

⭐ **It also removes the inactivity power-off, which is the larger of the two things it buys.** The
free plan powers off and is deleted 180 days later; the Developer tier "services are not
automatically powered off when inactive". So USD 5 is the price of a free Postgres that stays up at
all, and the 8 GB is the second half of the same purchase.

⚠ Two limits come with it and both are on the same documentation page: `max_connections` is set to
**20** and there is **no connection pooling**. Twenty is the number a deployment with a worker pool
meets first, and it does not move with the storage.

`Evidence:` `aiven.io/pricing/postgresql` (read 2026-10-22): the Developer column at USD 5 with
1 GB RAM and 8 GB storage; the Free column at 1 GB and 1 GB.
`aiven.io/docs/platform/concepts/free-plan` (read 2026-10-22): "Developer tier services are not
automatically powered off when inactive". `aiven.io/docs/products/postgresql/concepts/pg-free-tier`
(read 2026-10-22): `max_connections` set to 20 and no connection pooling.

`Verdict:` the cheapest paid step that removes both the storage cap and the clock, with a
20-connection ceiling attached.

## Neon Launch

Launch bills **USD 0.106 per CU-hour** with no monthly minimum, gives **500 GB of public network
transfer per project** before USD 0.10 per GB, and allows scale-to-zero to be disabled. Storage is
USD 0.35 per GB-month with no free allowance on the paid plan.

The absence of a minimum is the property worth paying for: a workload that runs four hours a
month costs USD 0.42, and the same workload on Aiven costs USD 5 because the storage is always on.

`Evidence:` `neon.com/pricing` (read 2026-10-22): Launch at USD 0.106 per CU-hour, 500 GB per
project included then USD 0.10/GB, storage USD 0.35/GB-month, scale-to-zero can be disabled.

`Verdict:` the cheapest paid step for a bursty workload and the more expensive one for a
continuous one.

## Supabase Pro

USD 25 a month gives an 8 GB database, 250 GB of egress then USD 0.09 per GB, 250 GB of cached
egress then USD 0.03 per GB, daily backups kept 7 days, and no pausing. Point-in-time recovery is
a separate USD 100 a month per 7 days of retention.

`Evidence:` `supabase.com/pricing` (read 2026-10-22): the Pro column and the pausing row "Never".

`Verdict:` the right paid step if the workload needs the auth and storage products that come with
the same project.

## Railway and PlanetScale

Railway's USD 1 a month is a container, not a database: one vCPU and 0.5 GB per service against a
credit that does not roll over. PlanetScale's cheapest SKU is **PS-5 at USD 5** for 1/16 vCPU and
512 MiB in the single-node table, and there is no free tier for it to remove. The USD 30 row is
PS-10 arm64 in the three-node table.

`Evidence:` `railway.com/pricing` (read 2026-10-22): the Free plan with USD 1 of monthly usage credit,
1 vCPU and 0.5 GB per service. `planetscale.com/pricing` (read 2026-10-22, page generated
2026-10-22T03:42Z): "Postgres EBS non-HA (single node)", `PS-5 | 1/16 | 512 MiB | $5`; the three-node
"Postgres EBS HA" table carries `PS-10 | arm64 | USD 30`.

`Verdict:` Railway is not a database budget. PlanetScale's floor is USD 5 for compute with storage
billed separately, so it is not a monthly total and it does not carry a comparison against a tier
that includes storage.

## What did not work

- **A free tier that becomes paid by adding a card**: Upstash's documentation says an account with
  a payment method cannot have free databases, so adding a card to a free Redis account converts
  every database rather than upgrading one (`documented`,
  `upstash.com/docs/redis/overall/billing`).
- **Neon as a fixed monthly cost**: with no minimum, the bill scales with the workload and a
  continuously connected 2 CU database is USD 155 a month at 730 hours, which is six times Supabase
  Pro (`inferred` from two documented numbers).
- **Supabase Pro as 8 GB**: the 8 GB is the database size and the egress is 250 GB, so a serving
  workload spends the egress allowance in four hours at 1 TiB a day (`inferred`).
- **Aiven Developer as a working set**: 8 GB against a 10 TiB working set is 0.08% (`inferred`).
- **PlanetScale's USD 30 as its cheapest SKU**: it is the three-node PS-10 row, and the single-node
  PS-5 is USD 5 (`documented`, `planetscale.com/pricing`). Every comparison built on 30 inherits the
  error.
- **Railway's USD 1**, above: one small container.

## Chaining

**A paid Postgres that stays up, with a free vector index inside it.** `Aiven Developer` at USD 5
with pgvector installed costs no extra and removes both the storage cap and the inactivity
power-off. The scarce link is the 20 connections, not the 8 GB: a single Worker or a small pool fits
inside twenty, and a fan-out of clients does not.

**A metered Postgres behind a free cache.** `Neon Launch` at USD 0.106 per CU-hour with `Upstash`
in front. The scarce link is that every cache miss costs compute, so the cache is the cost control
and not an optimisation.
