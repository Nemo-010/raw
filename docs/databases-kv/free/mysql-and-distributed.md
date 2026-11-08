# Which free MySQL or distributed SQL holds a real dataset?

Two providers give a free database above 5 GiB that needs no card, and both meter request units
rather than bytes. A third has no free tier at all and is the most commonly cited as if it did.
The answer is TiDB Cloud Starter for size and CockroachDB Basic for a reader who will add a card
anyway.

## The comparison

Sorted by free storage, because in this class storage is the largest number and the RU counter is
the one that binds.

| provider | free tier | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| TiDB Cloud Starter | 25 GiB row plus 25 GiB columnar, 250M RU, 5 instances per org | 250M RU per month | email | qualifies |
| CockroachDB Basic | 10 GiB plus 50M RU as a USD 15 monthly credit | 30-day deletion after the trial credits end | card | qualifies-with-caveat |
| PlanetScale | none since March 2024 | every database is paid | card | dead |

## TiDB Cloud Starter

TiDB Cloud Starter is MySQL-compatible and gives **25 GiB of row storage, 25 GiB of columnar
storage and 250 million Request Units per month** per organization, across up to five eligible
instances. A sixth instance requires a card and a spend limit, and that is where the card gate
sits: on the multiplication, not on the first five.

The documentation FAQ states **5 GiB and 50 million RUs per instance**, and the pricing page's own
footnote states the same thing: "each of up to five eligible instances includes 5 GiB row storage,
5 GiB columnar storage, and 50M Request Units per month. The allowance applies separately to each
instance." Five instances times 5 GiB is 25 GiB, so the organization total and the per-instance
figure are the same offer at two levels of arithmetic. The footnote sits directly under the table.

⭐ The practical reading is the conservative one: **5 GiB of row
storage and 50 million RUs per instance, 25 GiB and 250 million across five instances.** A sixth
instance requires a card and a spend limit.

The rate beyond the allowance starts at **USD 0.10 per million RUs**, which is cheap enough to be a
real price rather than a deterrent. Row storage beyond the allowance starts at USD 0.20/GiB-month
and columnar at USD 0.05/GiB-month.

What happens at the counter is documented and it is a refusal rather than a bill: "once a
MySQL-compatible TiDB Cloud Starter instance reaches its usage quota, it immediately denies any new
connection attempts" until the quota is raised or the month resets, while existing connections stay
open and are throttled. That is the answer to what comes after the free tier: the data stays, and
the connection stops.

`Evidence:` `pingcap.com/pricing` (read 2026-10-22): 25 GiB row, 25 GiB columnar, 250M RU, per
organization across five instances, footnote 1 stating 5 GiB and 50M RU per instance, and the
beyond-allowance rates. `docs.pingcap.com/tidbcloud/serverless-faqs/` (read 2026-10-22): 5 GiB and
50M RU per instance, and the card requirement for a sixth.
`docs.pingcap.com/tidbcloud/serverless-limitations/` (read 2026-10-22): the quota-exhaustion
sentence, 400 concurrent connections (5,000 with a spending limit) and the 340-second public-endpoint
idle timeout.

`Verdict:` qualifies. The largest card-free relational allowance in this topic, with a documented
refusal at the counter and no deletion clock published.

## CockroachDB Basic

CockroachDB Basic is Postgres-wire-compatible and distributed. A new organization gets **USD 400
in trial credits**. After that, Basic clusters receive **USD 15 a month** of free resource
utilization, which the documentation equates to **50 million Request Units and 10 GiB of
storage**, applied as a credit against the invoice.

⚠ The card question is genuinely ambiguous between two first-party pages. The pricing page says no
credit card is required; the free-trial documentation says a payment method must be added to be
eligible for the monthly credit. The sentences describe different things, the trial and the
recurring allowance, and the recurring allowance is the one that would make this a free database.

⛔ **What ends the trial is a deletion, not an interruption.** The free-trial page states: "If the
trial ends and a payment method has not been provided, a 30 day grace period begins where your
organization's clusters are throttled, and you are restricted from modifying their configuration".
And then: "If the end of the grace period is reached and no payment method has been added, all
clusters in the organization are deleted. Deleted clusters can not be restored."

So the free path here is a 400-dollar countdown to an unrecoverable deletion at 30 days past the
last credit. It is the only provider in this topic whose published after-free-tier behaviour is
*the data is gone*. A cluster does not power off on inactivity: Request Unit consumption "scales to
zero when your cluster has no activity", and the storage cap refuses further writes rather than
billing them.

Add to that: the free page publishes no egress allowance, and the pricing page says data transfer
is billed separately on data leaving the cluster. For a read-heavy workload that is an unpriced
constraint, which is worse than a small one.

`Evidence:` `cockroachlabs.com/docs/cockroachcloud/free-trial` (read 2026-10-22): the USD 400
trial credits, the USD 15 monthly credit equal to 50M RUs and 10 GiB, the 30-day grace period and
"all clusters in the organization are deleted. Deleted clusters can not be restored".
`cockroachlabs.com/docs/cockroachcloud/plan-your-cluster-basic` (read 2026-10-22): "Request Unit
consumption scales to zero when your cluster has no activity".
`cockroachlabs.com/pricing/` (read 2026-10-22): "No credit card required."

`Verdict:` qualifies-with-caveat. 10 GiB of always-free storage behind a card the vendor's own
pages disagree about, and a 30-day clock to unrecoverable deletion if the card never arrives.

## PlanetScale

PlanetScale has **no free plan**. Its own support answer says "Not at this time", records that
the Hobby plan was deprecated in March 2024, and states that "all databases created on
PlanetScale must be placed on a paid Scaler Pro plan when they are created and will begin to
accumulate charges for the time that the database is created." The plans documentation says the
same: "PlanetScale does not offer a free plan, previously known as the Developer or Hobby plan."

The cheapest published SKU is not PS-10. PlanetScale's pricing page carries four separate tables, and
the one that gives the floor is **Postgres EBS non-HA (single node)**: **PS-5 at USD 5 a month**
(1/16 vCPU, 512 MiB) and **PS-10 at USD 10** for arm64 (1/8 vCPU, 1 GiB), or USD 13 for x86-64. The
USD 30 row is **PS-10 arm64 in the Postgres EBS HA table**, which is three nodes rather than one:
one primary and two replicas.

That distinction is the whole pricing question here, because the USD 5 buys compute and nothing else.
Network-attached storage, backups and network transfer are billed separately from the SKU rate, so
USD 5 is a floor for a running cluster and not a monthly total for a usable database.

When the Hobby plan closed, remaining databases were slept, with a 24-hour wake offered to dump
data.

`Evidence:` `support.planetscale.com/hc/en-us/articles/32303734121239` (read 2026-10-22): "Not at
this time", the March 2024 deprecation, and the requirement to be on a paid plan from creation.
`planetscale.com/pricing` (read 2026-10-22, page generated 2026-10-22T03:42Z): "Postgres EBS non-HA
(single node)" table, `PS-5 | x86-64 | 1/16 | 512 MiB | $5`, `PS-10 | arm64 | 1/8 | 1 GiB | $10`;
the USD 30 figure is `PS-10 | arm64 | 1/8 | 1 GiB | $30` in the "Postgres EBS HA (3-node)" table.

`Verdict:` dead. Every "PlanetScale free tier" listicle is describing a product that closed in
March 2024.

## What did not work

- **PlanetScale**, above: no free plan, and the Hobby plan's closure deleted the product that the
  comparison literature is still selling.
- **PlanetScale at USD 30 a month as the cheap paid option**: USD 30 is the *three-node* PS-10 row,
  not the floor. The floor is PS-5 at **USD 5** for compute only, so this is the cheapest paid entry
  in the topic and not the most expensive (`documented`, `planetscale.com/pricing`). The comparison
  is in [`paid/postgres-floor.md`](../paid/postgres-floor.md).
- **CockroachDB's 10 GiB as a card-free tier**: the pricing page's card-free sentence covers the
  trial, and the recurring credit needs a payment method on the vendor's own docs.
- **TiDB's 25 GiB and 5 GiB as a contradiction**: they are the same offer at organization and
  instance level, and the pricing page's footnote states the per-instance figures. Use 5 GiB of row
  storage per instance and 25 GiB across the five (`documented`, `pingcap.com/pricing`, footnote 1).
- **MySQL 8 as a managed free tier without a card**: the two entries above are the whole field.
  Aiven's MySQL free plan is 1 GB, covered in
  [`postgres-always-on.md`](postgres-always-on.md).

## Chaining

**Distributed SQL plus a free Worker.** `TiDB Cloud Starter` behind a Cloudflare Worker gives an
HTTP data endpoint with no card and 25 GiB behind it. The scarce link is the RU counter, because a
Worker that queries per request will spend the allowance on cache misses.

**Two free relational tiers for one system.** TiDB for the large table and Aiven for the small
one is the only combination in this topic that is both card-free and above 5 GiB, and the scarce
link is that Aiven's free service powers off on inactivity, so the small side needs a keep-alive.
CockroachDB is not a third option for a reader with no budget: its trial ends in an unrecoverable
deletion.
