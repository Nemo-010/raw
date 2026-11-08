# Which free Postgres does not scale to zero on an idle clock, and what ends it instead?

Three providers give a free managed relational database that does not suspend on an inactivity
clock the way Neon does. None of the three is durable, and each one ends for a different reason:
one powers off on inactivity, one deletes the data when a spend limit is not raised, and one keeps
the data and refuses the connection. A reader who needs an unattended job to run is choosing
between those three clocks, not choosing an always-on host.

## The comparison

Sorted by free storage. The idle column is the one this document exists to answer, and no cell in
it reads "none".

| provider | free storage | idle behaviour | deletion clock | identity | verdict |
| --- | --- | --- | --- | --- | --- |
| CockroachDB Basic | 10 GiB plus 50M RUs/month as a USD 15 credit | no power-off published; usage scales to zero | 30 days after the trial ends without a payment method, then the clusters are deleted unrecoverably | card | qualifies-with-caveat |
| TiDB Cloud Starter | 25 GiB row plus 25 GiB columnar per organization | no power-off published | none published; the quota denies new connections instead | email | qualifies |
| Aiven | 1 GB per service | powers off on inactivity | 180 days after a power-off, 7 days past end of life | email | qualifies-with-caveat |

## The trade this class makes

The class rests on the claim that a free tier which does not pause costs the provider money every
hour and is therefore small, while a tier that pauses can be large. The reasoning holds; the
conclusion does not. Aiven is small at 1 GB **and** it powers off on inactivity,
so size and pause were never the trade. Neon gives 20 GB across 100 projects and suspends the
compute; Aiven gives 1 GB and powers the service off. Both have a clock, and on Aiven's pages the
clock is shorter than a weekly job.

⚠ **A suspended compute keeps the bytes. A powered-off service keeps them for 180 days. A deleted
cluster keeps nothing.** Those are three different outcomes and the vendor pages state which one
applies. This document sorts by the third.

⭐ No free relational database found here stays available without a keep-alive, and only one of
the three deletes the data on a published clock.

## Aiven

Aiven's Free plan gives **1 GB of RAM and 1 GB of total storage per service**, on Postgres, MySQL,
Valkey, Kafka and OpenSearch. It is free indefinitely with no time limit, and **it powers off after
a period of inactivity**. Two triggers are documented: no initial usage within the first few hours
after the service is created, and no continuative activity on the service. A notification arrives
by email and in the platform before a power-off.

The power-off is not the end of the clock. **"Services powered off for more than 180 days are
automatically deleted"**, and the grace does not apply to a service whose major version has reached
end of life, which is deleted within 7 days of the power-off.

So the weekly-cron question has a negative answer here, on Aiven's own pages. A job that runs once
a week is a job that lets the service power off between runs, and the only thing standing between
that and deletion is the 180-day clock. A keep-alive is required, and the paid tier is what removes
the clock: "Developer tier services are not automatically powered off when inactive", at USD 5 a
month for 8 GB of storage.

The pricing page's own carve-out reads: "Data retention is only limited by storage, with the
exception of Free plan". The exception is this clock.

The 5 GB that several comparison pages still print is the previous plan; the current page says
1 GB.

`Evidence:` `aiven.io/free-postgresql-database` (read 2026-10-22): "Service powers off after a
period of inactivity" and "It's free indefinitely with no time limit, but the service is
automatically powered off after a period of inactivity".
`aiven.io/docs/products/postgresql/concepts/pg-free-tier` (read 2026-10-22): the two power-off
triggers. `aiven.io/docs/platform/concepts/service-power-cycle` (read 2026-10-22): "Services powered
off for more than 180 days are automatically deleted", and the 7-day end-of-life rule.
`aiven.io/docs/platform/concepts/free-plan` (read 2026-10-22): "Developer tier services are not
automatically powered off when inactive". `aiven.io/pricing/postgresql` (read 2026-10-22): "RAM per
VM 1 GB" and "Total storage 1 GB" on the Free column; Developer USD 5 with 8 GB.

`Verdict:` qualifies-with-caveat. 1 GB of storage, an inactivity power-off, and a 180-day deletion
behind it. It qualifies on egress, programmatic access and identity, and the caveat is the clock.

## TiDB Cloud Starter

TiDB Cloud Starter's free monthly allowance is stated per organization on the pricing page:
**25 GiB of row storage, 25 GiB of columnar storage and 250 million Request Units**, across up to
five eligible instances. The pricing page's own footnote states the same allowance at instance
level: "each of up to five eligible instances includes 5 GiB row storage, 5 GiB columnar storage,
and 50M Request Units per month. The allowance applies separately to each instance." Five times five
is twenty-five, so the two statements reconcile.

The limit that binds is not storage. It is the counter, and what happens when it runs out is
documented: "Once a MySQL-compatible TiDB Cloud Starter instance reaches its usage quota, it
immediately denies any new connection attempts until you increase the quota or the usage is reset
upon the start of a new month. Existing connections established before reaching the quota will
remain active but will experience throttling." That is a refusal on the write path and on new
connections, with the bytes retained. No idle power-off and no deletion clock is published.

Two connection facts matter more than the storage. A Starter instance allows
**400 concurrent connections**, rising to **5,000** with a spending limit set. And the idle timeout
on a public endpoint is **340 seconds**, because AWS Global Accelerator does not permit TCP
keep-alive on it, so a long-lived idle connection is dropped by the network rather than by the
database.

A sixth instance requires a credit card and a spend limit, which is a `write-gated` constraint on
the multiplication rather than on the first five.

`Evidence:` `pingcap.com/pricing` (read 2026-10-22): "25 GiB row storage, 25 GiB columnar storage,
250M Request Units ... Per organization, across up to five eligible instances", and footnote 1
stating the per-instance figures. `docs.pingcap.com/tidbcloud/serverless-faqs/` (read 2026-10-22):
"5 GiB row data + 5 GiB columnar data + 50 million RUs per TiDB Cloud Starter instance".
`docs.pingcap.com/tidbcloud/serverless-limitations/` (read 2026-10-22): the 400 and 5,000 connection
limits, the 340-second idle timeout on a public endpoint, and the quota-exhaustion sentence.

`Verdict:` qualifies. The largest relational allowance found here that needs no card, with a
documented refusal at the counter and no deletion clock published.

## CockroachDB Basic

CockroachDB Cloud starts every new organization with **USD 400 in trial credits**, applied to all
cluster plans. After that, an account with Basic clusters receives **USD 15 a month of free
resource utilization**, which the documentation equates to **50 million Request Units and 10 GiB
of storage**, applied as a credit on the monthly invoice.

⛔ **What happens when the trial ends is the finding, and it is not an interruption.** The page
states: "If the trial ends and a payment method has not been provided, a 30 day grace period begins
where your organization's clusters are throttled, and you are restricted from modifying their
configuration". Then: "If the end of the grace period is reached and no payment method has been
added, all clusters in the organization are deleted. Deleted clusters can not be restored."

For a reader with no budget, that is the answer to the question this topic asks, and it is the
only provider in the class that deletes the data on a published clock. The USD 400 trial is a countdown,
not a free tier, and a Basic cluster that has never had a card on file is deleted 30 days after the
credits run out.

The recurring USD 15 is card-gated, and the two pages are about different things rather than
contradictory: the pricing page's "No credit card required" covers creating an organization and
running a trial workload, and the free-trial documentation's "A payment method must be added to the
account to be elegible for this benefit" covers the recurring credit that would make this a free
database rather than a countdown. The conservative reading is that the recurring allowance is
card-gated, which is what the record says.

The cluster does not power off on inactivity. Request Unit consumption "scales to zero when your
cluster has no activity", so an idle cluster costs nothing and is not suspended. Storage is billed
per GiB-month against the credit.

`Evidence:` `cockroachlabs.com/docs/cockroachcloud/free-trial` (read 2026-10-22): the USD 400
credits, the USD 15 monthly credit equal to 50 million RUs and 10 GiB, the 30-day grace period, and
"all clusters in the organization are deleted. Deleted clusters can not be restored".
`cockroachlabs.com/docs/cockroachcloud/plan-your-cluster-basic` (read 2026-10-22): "Request Unit
consumption scales to zero when your cluster has no activity"; "If you reach your storage limit,
your cluster will be unable to write to its storage unless you delete data or increase your storage
limit". `cockroachlabs.com/pricing/` (read 2026-10-22): "No credit card required."

`Verdict:` qualifies-with-caveat. 10 GiB is the largest always-free relational storage here, and
the same page that grants it states that the data is deleted 30 days after a card is not produced.

## What did not work

- **Aiven Free as the host for a weekly job**: the service powers off on inactivity and is deleted
  180 days after a power-off (`documented`, `aiven.io/docs/platform/concepts/service-power-cycle`).
- **Aiven's 5 GB**: the figure in circulation is the previous plan, and the page states 1 GB.
- **Aiven Free as a working set**: 1 GB of storage and 1 GB of RAM is 0.01% of a 10 TiB working
  set (`inferred` from two documented numbers).
- **CockroachDB Basic without a card**: the clusters are deleted 30 days after the trial credits
  end, and "Deleted clusters can not be restored" (`documented`,
  `cockroachlabs.com/docs/cockroachcloud/free-trial`).
- **CockroachDB's card-free sentence as a free database**: the card-free sentence covers the trial,
  and the recurring allowance needs a payment method on the vendor's own documentation.
- **Xata** as an always-on free Postgres: the always-free tier was retired and Xata Cloud is a
  14-day trial (`xata.io/pricing`, read 2026-10-22). Covered in
  [`postgres-serverless.md`](postgres-serverless.md).
- **Tembo** as a Postgres host: the product is now an agent workspace with a dollar-denominated
  trial allowance and no perpetual free tier (`tembo.io/pricing`, read 2026-10-22).

## Chaining

**A free Postgres plus a free tunnel.** `TiDB Cloud Starter` plus a Cloudflare Tunnel gives a public
endpoint that is not powered off for inactivity. The scarce link is the 340-second idle timeout on
a public endpoint, so the pooler must reconnect rather than hold a connection open.

**The two-provider split.** TiDB or CockroachDB for the relational working set and Neon or Supabase
for a large sleeping set is the shape that uses both free tiers for what each is good at. The scarce
link is that the two are separate systems and keeping them consistent is the reader's work, which
is out of scope here.
