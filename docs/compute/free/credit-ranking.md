# The twenty-one most generous credit offers, ranked

A credit is a balance, not a machine. It is the one free lane that arrives as money, so it is
the only lane a reader can point at a price list and spend. This page ranks the twenty-one largest
balances a single person can reach, across every topic in this corpus, and states what each one
costs at the gate and what it buys per hour.

## The answer

**The largest balance reachable without an institution is up to USD 1,000**, from
`yotta-labs-academic` Yotta Labs, and it is an application rather than a signup. **The largest
balance a signup grants is USD 400**, and three offers reach it: `snowflake` Snowflake,
`cockroachdb-basic` CockroachDB Cloud, and `databricks` Databricks, whose USD 400 is a ceiling
rather than a grant. **The largest balance that renews is USD 30 a month**, from `modal` Modal,
which is USD 360 over a year. `northflank` Northflank renews USD 20 a month, USD 240 a year, and
is the only one of the twenty-one that runs a service indefinitely without a daily recreate.
Both renew only behind a card.

**Nine of the twenty-one can hold a process open for 24 hours a day**, and a tenth, Modal, only
by recreating it daily. The calendar is the real limit: seven of those nine have a 30- or 31-day
window, one of them assumed because the vendor publishes no expiry. Run in sequence they cover
301 days of continuous uptime; only Northflank and Modal renew.

⛔ **Azure and AWS are excluded.** The corpus records a report that both refuse the email address at signup, so
their balances are unreachable capacity and do not enter
the ranking. AWS Activate's USD 1,000 founders tier and Azure's USD 200 trial are real numbers
behind a door this reader cannot open.

## Method

**Generous means the dollars a person can spend in the first twelve months.** A one-time credit
counts once. A recurring credit counts twelve times. That is the only comparison that treats
Modal's USD 30 a month and Snowflake's USD 400 once as the same kind of object.

**A balance is not a rate.** USD 300 over 30 days is 41.7 cents an hour; the same USD 300 over 90
days is 13.9 cents an hour. The ranking below is by total value, and the section
[The 30-day problem](#the-30-day-problem) re-sorts the same rows by the hourly rate the balance
sustains. The second order decides which machine fits.

**What the ranking excludes, and why.**

| class | why it is out |
| --- | --- |
| institution-gated credit | Google for Startups, AWS Activate, Microsoft for Startups, Cloudflare for Startups, and the academic clouds that admit only accredited staff. The number is large and the identity is unreachable |
| country-phone gated credit | Tencent and the mainland Alibaba lane need a national identity document or a mainland number |
| prize money | AIMO's USD 10,000,000 and the fellowship pools pay after a competition, not at signup |
| perpetual allowances | Oracle Always Free and Cloudflare Workers are worth more than a credit in the second year and cannot be denominated in USD without invented prices |
| an amount no live page states | DigitalOcean's USD 200 and Akamai's USD 100 survive only in archives and worked examples; GoCloud Africa's USD 300 has no signup path |
| a balance whose own record rejects the product | Confluent Cloud publishes USD 400, and its storage record carries `fails-quota` because the balance cannot hold the reader's bytes |

Every row below was read against the vendor's own page on 2026-10-23 or 2026-10-24, except Vultr,
whose live page refused the fetch and whose rates come from a broker snapshot dated 2026-10-21. The
evidence rung is `documented` unless the row says otherwise. No account was created, so every
identity gate is the vendor's sentence and not a completed signup.

## The ranking

Sorted by reachable USD over twelve months. The `Clock` column states what ends the balance.

| # | Provider | Credit | Value (USD) | Clock | Identity gate | What it buys |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `yotta-labs-academic` Yotta Labs | up to USD 1,000 | 1000 | not stated | an application, no card | GPU time, at a rate the page does not publish |
| 2 | `snowflake` Snowflake | USD 400 | 400 | 30 days | email only | virtual warehouses, storage, serverless |
| 3 | `cockroachdb-basic` CockroachDB Cloud | USD 400 | 400 | not stated | email or SSO | managed CockroachDB compute |
| 4 | `databricks` Databricks | up to USD 400 | 400 | 14 days of access | email | all-purpose clusters, SQL, jobs |
| 5 | `modal` Modal | USD 30 a month | 360 | monthly, renewing | card, no hold stated | serverless compute and GPU functions |
| 6 | `google-cloud-trial` Google Cloud | USD 300 | 300 | 90 days | card, USD 0.00–1.00 hold | any Google Cloud service, no GPU and no Gemini API |
| 7 | `oracle-cloud-trial` Oracle Cloud | USD 300 | 300 | 30 days | card, not prepaid, no hold stated | any eligible OCI service, then Always Free |
| 8 | `clickhouse-cloud` ClickHouse Cloud | USD 300 | 300 | 30 days | email only | managed ClickHouse |
| 9 | `aiven` Aiven | USD 300 | 300 | 30 days | email only | managed Postgres, Kafka, Valkey |
| 10 | `civo` Civo | USD 250 | 250 | 31 days | card, verified first, no hold stated | Kubernetes and VMs |
| 11 | `vultr` Vultr | USD 250 | 250 | 30 days | card, promo code, USD 0.00 deposit option | Cloud Compute VMs |
| 12 | `northflank` Northflank | USD 20 a month | 240 | monthly, renewing | card per docs, no hold stated | always-on services and jobs |
| 13 | `deepgram` Deepgram | USD 200 | 200 | none while the account lives | email only | speech to text, text to speech |
| 14 | `daytona` Daytona | USD 200 | 200 | not published | email for tier 1 | sandbox compute, no GPU |
| 15 | `ovhcloud` OVHcloud | USD 200 | 200 | 1 month | card, no hold stated | Public Cloud instances |
| 16 | `ibm-cloud` IBM Cloud | USD 200 | 200 | 30 days | card, nominal hold, 24–72 h | VPC virtual server instances |
| 17 | `e2b` E2B | USD 100 | 100 | none stated | email only | sandboxes, one hour per session |
| 18 | `speechmatics` Speechmatics | USD 100 | 100 | none stated | email only | speech to text |
| 19 | `anyscale` Anyscale | USD 100 | 100 | none stated | work email | Ray clusters |
| 20 | `kamatera` Kamatera | up to USD 100 | 100 | 30 days | card, no hold stated | one cloud server |
| 21 | `zylora-startup-gpu` Zylora | USD 100 | 100 | 6 months | review, or card for USD 25 | GPU instances |

⚠ **One of the ten card-gated rows states a firm hold amount.** A card is the gate on ten of the
twenty-one — nine, if Northflank's "No card needed" badge is the right reading of its own
contradiction. Google Cloud authorises USD 0.00 to USD 1.00. Vultr offers a USD 0.00 deposit and
warns that a small authorisation hold may still apply, without naming it. IBM places a nominal
verification hold, reversed within 24 to 72 hours, which one of its pages puts near USD 1.00 and
the account FAQ does not publish. The other seven — Modal, Oracle, Civo, Northflank, OVHcloud,
Kamatera and Zylora — state a card and no amount at all, so what the gate costs is unknown for
them. Oracle is the case to watch: its companion `oracle-cloud` record notes that "the USD 1 that
circulates is a forum report", so the number a reader is most likely to meet is a rumour rather
than a vendor sentence. The remaining rows need no card.

⚠ **The two renewing rows are the two with an unresolved card gate.** `modal` and `northflank`
both gate on a payment method before anything runs, and neither record states a hold amount.
Northflank's own pages disagree — the pricing page badges the free plan "No card needed" while the
billing documentation requires a payment method on every plan — and the record has carried both
readings. They are ranked because the credit is real and the shape is published, and they are the
only two rows that renew: a reader who cannot clear a card gate has no renewing offer on this page
at all.

⚠ **Four cells are ceilings, not grants.** Databricks states that eligibility, amount and expiry
are decided after account creation. Kamatera offers "up to USD 100" on one server. Yotta Labs
publishes "$1000 Credits" on the page and "Up to $1,000" in its own follow-up post, behind a
review. Zylora's USD 100 needs a five-minute review with a public repository or live site, and
only the USD 25 tier is instant.

⚠ **Yotta Labs is an academic programme and is ranked first anyway.** The exclusion of "the
academic clouds" does not reach it: its eligibility list ends with a lane for "Other Independent
Researchers — Anyone conducting their own research projects", which is the gate this page is
built around. The record is honest about the risk, noting that the three demonstrated awards are
university labs, so the independent lane is published and not yet demonstrated.

⚠ **The tie at USD 400 is broken by the clock and the product, not by the number.** Snowflake's
balance burns in about eight days at the smallest warehouse, so 30 days is not 30 days of machine.
CockroachDB publishes no clock at all. Databricks gives a discretionary ceiling behind a 14-day
access window.

⚠ **Vultr publishes two codes.** `250VULTRFLY` grants USD 250 and `FLY300VULTR` grants USD 300.
The row uses the smaller one because a campaign code is not guaranteed to be live at signup, and
the USD 300 code would move the row to a tie at USD 300.

⚠ **This table is a hand-written view of twenty-one records.** `Value` is derived by the rule above.
Every record carries the URL and the date for its own row in `evidence`.

## If the gate matters more than the number

This is the table for a reader whose signup was refused by a hyperscaler. It ranks by the gate:
no card first, then the least demanding form, then value.

| Provider | Gate | Credit | Note |
| --- | --- | --- | --- |
| `snowflake` Snowflake | valid email address | USD 400 | the form still asks for a work email and a company name |
| `cockroachdb-basic` CockroachDB Cloud | email, GitHub, Google or Microsoft | USD 400 | a name and company details follow email verification; a card only at the end |
| `databricks` Databricks | email, no card | up to USD 400 | a work email is recommended, not required; the Free Edition takes a personal address |
| `aiven` Aiven | email, no card | USD 300 | the trial URL is dead; the claim lives on two other Aiven pages |
| `deepgram` Deepgram | email, no card | USD 200 | no expiry while the account lives |
| `speechmatics` Speechmatics | email, no card | USD 100 | no expiry is stated |
| `e2b` E2B | email, no card | USD 100 | one-time credit, one-hour sessions on the Hobby plan |
| `anyscale` Anyscale | work email, no card | USD 100 | the credit attaches to an organisation, so a personal address may not reach it |
| `daytona` Daytona | verified email | USD 200 | tier 1 caps the pool at 10 vCPU and 10 GiB of RAM, with 30 GiB of storage |
| `clickhouse-cloud` ClickHouse Cloud | email, no card | USD 300 | the vendor's FAQ states no card is required; the signup console is JavaScript-only and was not exercised |
| `civo` Civo | name, email, password, then a verified card | USD 250 | the form takes no card; no instance exists until one is verified |
| `yotta-labs-academic` Yotta Labs | an application with a review | up to USD 1,000 | no card; the eligibility list names independent researchers, and the record notes the three demonstrated awards are university labs |

⚠ **This table covers twelve of the twenty-one rows, not all of them.** The nine it leaves out —
Modal, Google Cloud, Oracle, Vultr, Northflank, OVHcloud, IBM Cloud, Kamatera and Zylora — are the
rows whose gate is a card and nothing else. Read it as a shortlist of the weakest gates, not as
the complete no-card list.

## The 30-day problem

Most of these trials are 30 or 31
days, and that changes the answer. A 30-day clock does not reduce the value, it sets the burn rate. The balance divided by the
window is the hourly rate a machine may cost and still last the whole term.

| Provider | Credit | Days | Rate the balance sustains | What that rate buys on that provider |
| --- | --- | --- | --- | --- |
| Yotta Labs | up to USD 1,000 | not stated | not stated | GPU hours at a rate the page does not publish |
| Snowflake | USD 400 | 30 | USD 0.5556/h | nothing: an X-Small warehouse is 1 credit an hour, and a credit is USD 2, so the balance is gone in 200 hours |
| CockroachDB | USD 400 | not stated | not stated | a managed database, not a VM; 6 vCPU at USD 0.092 per vCPU-hour for a month, if the clock is a month — the same page's footer reads USD 0.057, and the record carries the conflict |
| Databricks | up to USD 400 | 14 | USD 1.1905/h | no rate was published on the page read, so no shape |
| Modal | USD 360 a year | 365 | USD 0.0411/h | 0.25 physical core and 256 MiB for 720 hours; a 31-day month exceeds the grant by USD 0.86 |
| Google Cloud | USD 300 | 90 | USD 0.1389/h | `e2-standard-4`, 4 vCPU and 16 GB, at USD 0.13402284/h |
| Oracle Cloud | USD 300 | 30 | USD 0.4167/h | `VM.Standard.A1.Flex` at 16 OCPU and 96 GB costs USD 0.304/h; the rest buys storage |
| ClickHouse | USD 300 | 30 | USD 0.4167/h | a small managed service; compute scales to zero when idle |
| Aiven | USD 300 | 30 | USD 0.4167/h | twenty Hobbyist services at USD 0.02/h, or one large one |
| Civo | USD 250 | 31 | USD 0.3360/h | `Extra Large` is USD 0.119048/h; the tight fit is four sizes together |
| Vultr | USD 250 | 30 | USD 0.3472/h | an 8 vCPU / 32 GB instance is USD 0.219/h; the rest buys smaller ones |
| Northflank | USD 240 a year | 365 | USD 0.0274/h | `nf-compute-50` at USD 0.01667/h, renewing |
| Deepgram | USD 200 | none | USD 0.0228/h if held a year | about 700 hours of Nova transcription |
| Daytona | USD 200 | not published | USD 0.2778/h assumed for 30 days | 4 vCPU, 4 GiB and 10 GiB is USD 0.26694/h |
| OVHcloud | USD 200 | 30 | USD 0.2778/h | `c3-16` at USD 0.2154/h before local disk |
| IBM Cloud | USD 200 | 30 | USD 0.2778/h | `bx4-4x16` plus a `bx4-2x8` at a derived rate |
| E2B | USD 100 | none | not applicable: one-hour sessions | no continuous rate exists |
| Speechmatics | USD 100 | none | USD 0.0114/h if held a year | 416 hours at the USD 0.24 base rate |
| Anyscale | USD 100 | none | not stated | the rate card is in AC, not dollars |
| Kamatera | up to USD 100 | 30 | USD 0.1389/h | one custom server; the largest preset is USD 39 a month |
| Zylora | USD 100 | 182.5 | USD 0.0228/h | GPU hours at a rate the page does not publish |

⭐ **What this table decides.** The three USD 300 offers with a 30-day window sustain three times
the hourly rate of the USD 300 offer with a 90-day window. Google is the longest-lived machine and
Oracle is the largest one, and they are the same balance. A 30-day credit is a one-shot burst; a
renewing credit is a host.

### One year of uptime, in sequence

Because eight of the ten compute offers are one-shot trials, the way to run 24/7 across a year is
to spend them one after another rather than at once. In descending order of sustained rate:

| Order | Provider | Days | Machine |
| --- | --- | --- | --- |
| 1 | Oracle Cloud | 30 | `VM.Standard.A1.Flex`, 16 OCPU / 96 GB |
| 2 | Vultr | 30 | 8 vCPU / 32 GB, plus smaller instances |
| 3 | Civo | 31 | two `Extra Large`, plus `Large`, `Medium` and `xSmall` |
| 4 | OVHcloud | 30 | `c3-16`, 8 vCore / 16 GB |
| 5 | IBM Cloud | 30 | `bx4-4x16` plus `bx4-2x8` |
| 6 | Daytona | 30 assumed | 4 vCPU / 4 GiB, auto-stop and TTL disabled |
| 7 | Google Cloud | 90 | `e2-standard-4`, 4 vCPU / 16 GB |
| 8 | Kamatera | 30 | one custom server near USD 0.1389/h |
| not counted | Northflank | indefinite | `nf-compute-50`, 0.5 vCPU / 1 GB, renewing |
| not counted | Modal | indefinite | 0.25 core / 256 MiB, recreated daily |

**301 days** from the one-shot rows, plus two perpetual machines that can run underneath them.
The sequence is arithmetic over the published windows, not a measurement: a missed signup, a
refused card or an out-of-stock shape breaks it. Daytona's 30 days is assumed because the vendor
publishes no expiry.

## What each balance buys if left running

Ten of the twenty-one sell something that can run a process, nine of them around the clock. The
rest are a warehouse, a database, an API, a sandbox with a session cap, or a platform whose rate
cannot be read; they are listed after the table. Each row sizes one machine to the full life of
the credit, then states what the remainder buys.

⚠ **These totals cover compute only.** Egress, block storage and public IPv4 addresses bill
separately on every provider in the table, and a serving workload moves bytes. A box kept busy at
a daily target of 500 GB to 1 TiB exceeds most of these budgets before the calendar
does.

| Provider | 24/7? | Service and shape | Rate | Cost for the window | Left | The remainder buys |
| --- | --- | --- | --- | --- | --- | --- |
| Oracle Cloud | yes | `VM.Standard.A1.Flex`, 16 OCPU / 96 GB, 47 GB boot | USD 0.3040/h | USD 218.88 / 30 d | USD 81.12 | a 6 OCPU / 32 GB A1 in a second availability domain, USD 77.76 |
| Civo | yes | two `Extra Large` (6 cores / 16 GB / 150 GB), one `Large`, one `Medium`, one `xSmall` | USD 0.334822/h | USD 249.11 / 31 d | USD 0.89 | nothing: this is the tight fit |
| OVHcloud | yes | `c3-16`, 8 vCore / 16 GB, plus 200 GB local NVMe | USD 0.24982/h | USD 179.87 / 30 d | USD 20.13 | nothing on this reading; on the compute-only reading the left is USD 44.91 and buys a `c3-4` at USD 38.88 |
| Google Cloud | yes | `e2-standard-4`, 4 vCPU / 16 GB | USD 0.13402284/h | USD 289.49 / 90 d | USD 10.51 | disk at list price, not another machine |
| IBM Cloud | yes, rate derived | `bx4-4x16`, 4 vCPU / 16 GiB | USD 0.183208/h | USD 131.91 / 30 d | USD 68.09 | one `bx4-2x8`, USD 65.95 |
| Vultr | yes | 8 vCPU / 32 GB / 640 GB | USD 0.219/h | USD 157.68 / 30 d | USD 92.32 | 4/8, 2/4, 2/2 and 1/1 together, USD 85.68 |
| Daytona | yes, auto-stop 0 and no TTL | 4 vCPU / 4 GiB / 10 GiB sandbox | USD 0.26694/h | USD 192.20 / 30 d | USD 7.80 | about 20 GiB more disk (USD 1.55); the tier-1 cap of 30 GiB leaves USD 6.25 unspendable |
| Kamatera | yes, one server | a custom Cloud Server, Type B, scaled to the USD 100 ceiling | about USD 0.1389/h | USD 100 / 30 d | USD 0 | the trial covers exactly one server |
| Northflank | yes, indefinitely | `nf-compute-50`, 0.5 vCPU / 1 GB | USD 0.01667/h | USD 12.00 / month | USD 8.00 / month | nothing: the next plan is USD 24, which overruns |
| Modal | only by recreating daily | 0.25 physical core / 256 MiB | USD 0.04148/h | USD 29.87 / 30 d | USD 0.13 | nothing |

Every total is published rate times hours, with three exceptions that the sections below state.
Vultr's rates come from the 2026-10-21 snapshot. IBM's rate is derived from component rates.
OVHcloud's rate adds an assumed 200 GB of local disk at USD 0.0001721 per GB-hour, because the
vendor does not publish the disk size. The totals are arithmetic, not invoices, because no
account was created.

### Oracle: the quota binds before the money

`VM.Standard.A1.Flex` at 16 OCPU and 96 GB is the largest single A1 machine a trial tenancy can
launch **in one availability domain**. The service limit is 16 OCPU and 96 GB per domain, and the
shape's own maximum is 76 OCPU and 472 GB at up to 64 GB per OCPU. At USD 0.01 per OCPU-hour plus
USD 0.0015 per GB-hour, 16/96 costs USD 0.304 an hour and USD 218.88 over 30 days.

USD 300 buys 987 A1 hours, so the money does not bind the shape; the quota does. The leftover
USD 81.12 cannot enlarge the same machine, because 16 OCPU and 96 GB is a hard ceiling in that
domain. The ways to spend it are ranked:

1. **A second availability domain.** The limit is per domain, so a 6 OCPU / 32 GB A1 costs
   USD 77.76 for 30 days and leaves USD 3.36. A1 capacity is subject to availability.
2. **Block storage** at USD 0.0255 per GB-month (unverified: no record in this corpus carries the
   rate), about 3.2 TB for the month. The 47 GB boot volume sits inside the Always Free 200 GB
   block allowance on an Always Free tenancy; if the trial bills it, it takes USD 1.20 from the
   remainder.

More RAM on the first machine is not an option: 96 GB is the domain's memory limit, and a
16 OCPU / 171 GB request is refused. Ampere instances above the Always Free allowance are
disabled and deleted after the trial unless the account is upgraded.

Read at <https://www.oracle.com/cloud/free/> and
<https://docs.oracle.com/en-us/iaas/Content/General/service-limits/default.htm> on 2026-10-23.

### Civo: the rate card is not linear, so buy the size below the top

`2X Large` at 8 vCPU, 32 GB and 200 GB costs USD 177.14 across the 31 days. It is not the best use
of the credit, because `Extra Large` is 6 cores for USD 0.119048 an hour while `2X Large` is 8
cores for USD 0.238095. Two `Extra Large` cost the same as one `2X Large` and carry 12 cores
against 8.

The tightest fit under USD 250 over 744 hours is **two `Extra Large`, one `Large`, one `Medium`
and one `xSmall`**: USD 0.334822 an hour, USD 249.11 for the window, USD 0.89 left, and 19 cores,
45 GB and 475 GB of NVMe. Nothing else on the card comes closer without overrunning.

The catch is the account's instance quota. Civo publishes it only as an image and a default of
8 vCPU is reported rather than documented, so an increase may be needed before 19 cores exist.
Billing is hourly and rounded up, and a stopped instance still bills in full, so stopping it does
not preserve the balance. The Kubernetes control plane is free on every cluster, and worker nodes
bill from the same card, so a cluster is a container path at the same rate as a VM.

Read at <https://www.civo.com/pricing> and <https://www.civo.com/legal/terms> on 2026-10-23.

### OVHcloud: compute is priced, the disk is not, and the clock has two readings

`c3-16` is USD 0.2154 an hour and USD 155.09 for 30 days before local disk. The price list shows
the disk column as "Local storage low latency" with no size and no footnote, so the only honest
total is a range: USD 155.09 if the disk is in the compute line, USD 179.87 if 200 GB is billed at
the USD 0.0001721 per GB-hour used earlier. Both fit under USD 200.

The clock has two readings, and they change the machine. The trial page gives one month and
USD 200. The US price list states USD 200 on a first Public Cloud project plus USD 100 for a first
managed database, "valid for 90 days from the day the credit has been applied". A 90-day USD 300
reading sustains USD 0.1389 an hour, and the tight fit there is `c3-8` at USD 0.1078/h, which is
USD 232.85 for 2,160 hours, or two `c3-4` at USD 233.28. Monthly billing is irreversible and keeps
charging after a one-month credit ends, so the conservative shape is the 30-day `c3-16`.

Read at <https://us.ovhcloud.com/public-cloud/prices/> and
<https://www.ovhcloud.com/en/public-cloud/free-trial/> on 2026-10-23.

### Google Cloud: the longest-lived machine

`e2-standard-4` at 4 vCPU and 16 GB costs USD 289.49 for the full 90 days, which is the closest fit
to the credit on the whole list: 96.5 per cent of the balance and one shape. The USD 10.51 left
covers disk at list price and almost no egress: the always-free allowance is 1 GB a month from
North America. A serving workload exceeds the credit before day 90. E2 gets no sustained-use
discount, and a trial billing account cannot request more quota or add a GPU.

Read at <https://cloud.google.com/free/docs/free-cloud-features> and
<https://cloud.google.com/compute/vm-instance-pricing> on 2026-10-23.

### IBM Cloud: the rate is derived, and the quota is not the constraint

IBM publishes the Balanced profiles but not a per-profile rate. The figure above is derived from
IBM's component rates, USD 1.7626 per 63 vCPU-hours and USD 2.0054 per 450 GB-hours, which gives
USD 0.183208 an hour for `bx4-4x16`. It is a hypothesis until the console estimator confirms it,
and the 1.07 per cent headroom means any error above one per cent overruns the credit. On that
rate, `bx4-4x16` plus a `bx4-2x8` costs USD 197.86 and leaves USD 2.14. The profiles are
`bx4-2x8`, `bx4-4x16` and `bx4-8x32`; there is no 3x12, and the fourth-generation Balanced
profiles are offered in Dallas only. No vCPU quota is recorded for the account, so the 30-day
window is the constraint here. The card comes first: the record carries a nominal verification
hold, reversed within 24 to 72 hours, which one vendor page puts near USD 1.00 and the account FAQ
does not publish.

Read at <https://cloud.ibm.com/docs/vpc?topic=vpc-profiles> and
<https://cloud.ibm.com/docs/account?topic=account-accounts> on 2026-10-23.

### Vultr: a code, a card, and five small shapes

The credit is a promo code, not a signup grant: `250VULTRFLY` for USD 250 and `FLY300VULTR` for
USD 300, new customers only, and the documentation says the credits last up to 30 days. A payment
method is required before any instance exists.

The largest published shape that fits is the 8 vCPU / 32 GB Regular Performance instance at
USD 0.219/h, USD 157.68 for 30 days. The remaining USD 92.32 is best spent down the bench rather
than on one bigger machine: 4/8 at USD 0.06, 2/4 at USD 0.03, 2/2 at USD 0.022 and 1/1 at USD
0.007 add USD 85.68 and leave USD 6.64, for 17 vCPU and 47 GB across five instances. The bench is
cheaper per vCPU than the top shape: 4/8 is USD 0.015 per vCPU-hour and 8/32 is USD 0.0274.

Read at <https://www.vultr.com/coupons/> and <https://www.vultr.com/pricing/> on 2026-10-23.

### Daytona: turn the idle stop and the TTL off, in that order

The default stops a sandbox after 15 minutes idle, which kills an unattended process. Disabling
auto-stop is not enough on its own: the documentation states that disabling it "does not disable
wall-clock TTL", and a non-ephemeral VM class falls back to a 60-minute auto-pause. A 24/7 sandbox
needs `auto_stop_interval=0`, no `ttl_minutes`, and `auto_pause_interval=0` for the VM class.

Rates are per unit, not per shape: USD 0.0504 per vCPU-hour, USD 0.0162 per GiB-hour and USD
0.000108 per GiB-hour of storage. The first 5 GiB of disk is free, so a 4 vCPU / 4 GiB / 10 GiB
sandbox is USD 0.26694 an hour, USD 192.20 for 30 days. The USD 7.80 left buys 20 GiB more disk,
which reaches the tier-1 cap of 30 GiB total; USD 6.25 of the balance has no use inside that cap.
Tier 1 network access is filtered, and the credit does not cover GPU sandboxes.

Read at <https://www.daytona.io/docs/en/limits/> and <https://www.daytona.io/pricing> on
2026-10-23.

### Kamatera: one server, and a ceiling rather than a grant

The trial gives "services worth up to USD 100 on 1 server" for 30 days, with 1 TB of block storage
and 1 TB of traffic, and it requires a card. The published presets are Basic at USD 4 a month
(1 vCPU, 1 GB), Standard at USD 25 (2 vCPU, 2 GB) and Pro at USD 39 (2 vCPU, 4 GB), so the largest
preset leaves USD 61 unspent. The ideal configuration is a custom Cloud Server on Type B, scaled
until the calculator reaches the USD 100 ceiling near USD 0.1389 an hour. The calculator runs in
the browser, so the exact vCPU and memory at that price cannot be read from the page. Scaling is
capped "within the USD 100 configuration", and hourly servers bill by the minute.

Read at <https://www.kamatera.com/free-trial/> and <https://www.kamatera.com/pricing/> on
2026-10-23.

### Northflank: the only one that never runs out

The USD 20 is a monthly allowance, not a depleting balance. The current cheapest plan is
`nf-compute-50` at 0.5 vCPU and 1 GB for USD 0.01667 an hour or USD 12 a month, so it runs
indefinitely and leaves USD 8 a month that buys nothing smaller. The next plan, `nf-compute-100-2`
at 1 vCPU and 2 GB, is USD 24 and overruns by USD 4. The free plan is named Sandbox, allows two
services, two jobs and one database, and states "Always on, no sleeping".

The card rule is contradictory in the vendor's own pages. The pricing page labels the free plan
"No card needed"; the documentation states that all users must add a payment method regardless of
plan. The free per-instance ceiling is published only as "Limited", so the 0.5 vCPU selection may
be refused.

Read at <https://northflank.com/pricing> on 2026-10-23.

### Modal: 24 hours is the lifetime

A sandbox cannot outlive 24 hours, so 24/7 here means a daily recreate from a filesystem snapshot.
USD 30 a month buys 0.25 physical core and 256 MiB for 720 hours, which is 0.5 vCPU and not a
server; a 31-day month costs USD 30.86 and exceeds the grant. The same credit buys 1 core and
1 GiB for 7.5 days. Use it for bursts, and let the monthly reset refill it.

Read at <https://modal.com/docs/guide/billing> on 2026-10-23.

### What cannot host a process, and what cannot be sized

| Provider | Why not |
| --- | --- |
| Snowflake | the balance is a warehouse budget; an X-Small burns 1 credit an hour at USD 2 a credit, so USD 400 is 200 hours, not 720 |
| CockroachDB | a managed database, no arbitrary process |
| ClickHouse Cloud | a managed database; compute scales to zero when idle |
| Aiven | managed services only, no general-purpose VM |
| Deepgram | bills per minute of audio, not per hour of uptime |
| Speechmatics | bills per hour of audio transcribed |
| E2B | one-hour sessions on Hobby; 24 hours on Pro, which needs a card and a paid plan |
| Databricks | a cluster can run 24/7 for the 14-day window, but no DBU rate was published on the page read, so it cannot be sized |
| Anyscale | the rate card is denominated in AC, and no AC-to-dollar rate is published |
| Zylora | GPU instances, but no per-GPU rate on the page read, and the instant tier is USD 25 |
| Yotta Labs | GPU instances, and no per-GPU rate was published on the page read |

## Two equal machines instead of one big one

Splitting the same balance across two identical machines costs the same on a provider whose price
is linear in vCPU and memory. It costs more where a per-instance charge exists, and it can buy
more on a rate card with a size step, which Civo and Vultr both have. This table holds each
provider to the same total window and the same balance.

| Provider | Equal pair | Rate each | Pair cost | Left | Against one machine |
| --- | --- | --- | --- | --- | --- |
| Oracle Cloud | 2 x `A1.Flex` 10 OCPU / 72 GB, one per domain | USD 0.2080/h | USD 299.52 | USD 0.48 | 20 OCPU / 144 GB against 16 / 96, and it needs a second availability domain |
| Civo | 2 x `Extra Large`, 6 cores / 16 GB / 150 GB | USD 0.119048/h | USD 177.14 | USD 72.86 | 12 cores against 8 for the same money, and the remainder buys `Large`, `Medium` and `xSmall` to reach the same USD 249.11 tight fit |
| OVHcloud | 2 x `c3-8`, 4 vCore / 8 GB (compute only) | USD 0.1078/h | USD 155.23 | USD 44.77 | the same 8 vCore and 16 GB as one `c3-16`, in two boxes; the local disk is unpriced on both |
| Vultr | 2 x 6 vCPU / 16 GB, USD 80 a month | USD 0.1111/h | USD 160.00 | USD 90.00 | 12 vCPU / 32 GB against 8 / 32, and USD 0.0185 per vCPU-hour against USD 0.0274 |
| Google Cloud | 2 x `e2-standard-2`, 2 vCPU / 8 GB | USD 0.06701142/h | USD 289.49 | USD 10.51 | the same vCPU and memory as one `e2-standard-4`, because E2 is linear |
| IBM Cloud | 2 x `bx4-2x8`, 2 vCPU / 8 GiB | USD 0.091604/h | USD 131.91 | USD 68.09 | 4 vCPU / 16 GiB, and the leftover buys a third `bx4-2x8` to reach the same 6 / 24 as the one-machine route |
| Daytona | 2 x 2 vCPU / 2 GiB / 10 GiB | USD 0.13374/h | USD 192.59 | USD 7.41 | the same vCPU and memory as one 4/4, with 20 GiB of storage instead of 10 |
| Modal | 2 x 0.125 core / 128 MiB | USD 0.02074/h | USD 29.87 | USD 0.13 | the same total, split into two daily recreations |
| Kamatera | not offered | not applicable | not applicable | not applicable | the trial covers exactly one server |
| Northflank | 2 x `nf-compute-50` = USD 24 a month | USD 0.01667/h | USD 24.00 | -USD 4.00 | overruns the USD 20 allowance |

⭐ **The rule.** Ask what the provider prices per instance rather than per vCPU. Civo and Vultr
reward the smaller size, so the pair carries more cores for the same money. Oracle, OVHcloud,
Google, IBM, Daytona and Modal are linear, so the pair is a redundancy choice and not a capacity
one. Northflank and Kamatera's trial cannot do it at all.

## What the verification changed

Each row below was checked against the vendor page, and the claim it carried before is stated
beside what the page says.

| Provider | Claim before 2026-10-23 | What the page says |
| --- | --- | --- |
| `confluent-cloud` Confluent Cloud | USD 400 for 60 days | USD 400 for 30 days; both the signup page and the docs say 30 |
| `northflank` Northflank | `nf-compute-100-1` at USD 18 a month | that plan is gone; the cheapest is `nf-compute-50` at USD 12, and the next is USD 24 |
| `ovhcloud` OVHcloud | `c3-16` at USD 0.2498/h | compute is USD 0.2154/h and the local disk is unpriced, so the total is a range |
| `cockroachdb-basic` CockroachDB | USD 400 for 30 days | the page states no trial length; the 30 days is the post-trial grace period |
| `netmind` NetMind | USD 100 on a new account | the event URL resolves to the homepage and the archive has the figure blank |
| `digitalocean` DigitalOcean | USD 200 for 60 days | no current amount is published; the USD 200 survives only in a 2026-05-15 archive |
| `linode` Akamai Cloud | USD 100 for 60 days | no English offer exists; the USD 100 is Japanese meta text and an FAQ example |
| `databricks` Databricks | USD 400 for 14 days | "up to USD 400", at Databricks' discretion, with 14 days of platform access |
| `vultr` Vultr | paid-only | USD 250 or USD 300 by promo code, up to 30 days, with a payment method |
| `aiven` Aiven | not recorded | USD 300 for 30 days with no card, on two pages rather than the dead trial URL |

**The 2026-10-24 read checked every row against its record and corrected eight claims.**
The card question drove it: a credit was ranked
without saying what the card costs, and this page named a card in ten rows and an amount held in
none.

| Provider | Claim before 2026-10-24 | What the record says |
| --- | --- | --- |
| the ranking | USD 400 is the largest balance reachable without an institution | `yotta-labs-academic` holds up to USD 1,000 on an application whose eligibility list ends with "Other Independent Researchers"; it is ranked first, and USD 400 is now the largest a signup grants |
| `modal` | the largest renewing balance, gate "card" and no amount | the record names the card as the binding constraint and states no hold; its verdict has been recorded both as `fails-identity` and as `qualifies`, and the row now says so |
| `northflank` | "the only one that never runs out" | the billing documentation requires a payment method on every plan while the pricing page badges "No card needed"; no hold amount is stated under either reading |
| the Identity gate column | a card named, no amount | one record states a firm amount (Google's USD 0.00 to USD 1.00), two a qualified one (Vultr's USD 0.00 deposit option, IBM's unpublished nominal hold), and seven none |
| `clickhouse-cloud` | "card unverified" | the record quotes the vendor's "no credit card required", so the row says email only |
| `anyscale` | absent from the gate table | work email, no card, USD 100: added to the gate table |
| `cockroachdb-basic` | USD 0.092 per vCPU-hour, stated | the same page's footer reads USD 0.057, and the record carries the conflict |
| the 24/7 count | "Ten of the twenty can hold a process open" | nine do, and Modal only by recreating it daily, which this page's own table already said |

⚠ **The Confluent correction does not put it in the ranking.** Its storage record carries
`fails-quota`, so the balance is real and the product does not answer the reader's storage
question. The correction stands in the record and the row stays out.

⚠ **Two corrections went the other way.** OVHcloud and IBM Cloud were both recorded as paid-only and both publish USD 200. Lightning AI was recorded as dead while its pricing page
still advertises credits, which conflicts with the recorded revocation of user access. That record
keeps `dead`.

## What did not make the twenty-one

| Provider | Credit | Why it is out |
| --- | --- | --- |
| `gocloud` GoCloud Africa | USD 300 claimed | the only evidence is a homepage badge; no signup form, no terms, no expiry |
| `confluent-cloud` Confluent Cloud | USD 400 | the record's verdict is `fails-quota`: the credit cannot hold the reader's bytes |
| `digitalocean` DigitalOcean | USD 200 in an archive | no current amount is published on any first-party page |
| `linode` Akamai Cloud | USD 100 in Japanese meta | the English trial URL is 404 and the FAQ figure is an example |
| `assemblyai` AssemblyAI | USD 50 | below the cut |
| `railway` Railway | USD 5 | the trial is real and small |
| `render` Render | 750 instance-hours a month | an allowance, not a balance, and the free database is deleted at day 30 |
| `cerebras-inference` Cerebras Inference | USD 5 | the vendor states there is no permanently free tier |
| `alibaba-cloud-international` Alibaba Cloud | points | the international trial is per-product quotas plus points at 1 point to USD 1 |

## The offers that are bigger and unreachable

The largest numbers in the corpus are not credits a person can claim. They are applications, and
the gate is the finding.

| Programme | Ceiling | Gate |
| --- | --- | --- |
| Google for Startups | USD 200,000 to 350,000 | verifiable Pre-Seed to Series A funding and a startup wrapper |
| Cloudflare for Startups | up to USD 350,000 | a funding stage under USD 5M raised |
| AWS Activate | USD 1,000 at the founders tier, up to USD 200,000 at the portfolio tier | an Activate Provider organisation ID at the top tier |
| Microsoft for Startups | USD 200 at milestone 1 | a personal LinkedIn account and an Azure signup |
| Cerebras Inference Research | USD 50,000 of inference | a principal investigator at a university |
| NVIDIA DGX Cloud | up to USD 100,000 | a portfolio company of four named venture funds |

None of these is a signup. Each one is an application with a reviewer, and the reviewer is the
constraint. The distance between USD 400 and USD 350,000 is the distance between an email address
and a company.

## How this ages

A credit ladder rots faster than a price list, because vendors use it as a promotion and withdraw
it without notice. The USD 100 that BoxLite carried on 2026-10-22 was gone on 2026-10-23, and
NetMind's USD 100 was gone from its own event page by the time it was checked.

Treat every row here as a hypothesis with a date. Re-read the vendor page before a signup.

The next measurement is one account. Civo is the cheapest to try: USD 250, 31 days, and a card
that is not virtual or prepaid. Registering it would convert the best-evidenced gate in this table
from `documented` to `measured`, and it is the only move that settles whether the gate is as weak
as the form suggests.
