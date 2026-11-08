# Cloud VMs: the free tiers, the clocks, and what traffic out costs

A cloud VM is the only shape in this topic that can be an endpoint. A sandbox runs a
job and is destroyed, a serverless runtime answers a request and forgets, and a
notebook gives a kernel. A VM has an address, a disk that survives a reboot, and a
process that can be left running. That is the resource the 03:00 requirement needs, and
it is the one the free lane gives away least.

The answer, in one paragraph. **Exactly one provider gives a perpetual free VM with
usable egress: Oracle Cloud Always Free.** It offers 2 OCPU, 12 GB, 200 GB and 10 TB a
month. It wants a card and a phone at signup and it applies a seven-day reclaim test.
Google's e2-micro has no idle reclaim and 1 GB of egress a month, which is 0.0067 per
cent of one day's 500 GB serving target. AWS and Azure are six-month and twelve-month
clocks, not tiers. Below those, the paid floor in this class is Contabo's Cloud VPS 4 at
USD 6.60 a month; the topic's floor is USD 3.75, GreenCloudVPS's 8 GiB on annual prepay,
priced in `paid/README.md`. The
row that matters most in the paid lane is not the CPU price. It is the traffic term
beside it. ⭐ **The class this document prices is 46 records, and eleven of them are not
VMs at all.** They are managed agent runtimes billed per vCPU-hour. One of those costs
a whole month of that USD 6.70 box in about thirty hours.

## The comparison

The class this document prices holds 46 records. Thirty-five are machines or machine-shaped offers and are
in the table below. Eleven are billed by a unit of work rather than by a machine. They
are in the next section, because a per-vCPU-hour row cannot be ranked beside a per-month
one.

The table groups by the one variable that decides the question: what ends the offer.
`Held 24/7` is the record's own 24/7 figure. Six rows convert a euro or yen price at a
rate the record does not carry. The note under the table names them.

| What ends it | Provider | Shape or offer | Held 24/7 | Egress | Identity | Binds | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| renews monthly | Oracle Cloud Always Free | 2 OCPU, 12 GB, 200 GB | USD 0 | 10 TB a month | card | retention-clamped | qualifies-with-caveat |
| renews monthly | Google Cloud Free Tier | 1 e2-micro, 30 GB | USD 0 | 1 GB a month | card | per-ip-shaping | qualifies-with-caveat |
| renews monthly | Google Compute Engine | the same e2-micro, priced as a paid machine | USD 48.25 | 1 GB a month | card | request-rate | qualifies-with-caveat |
| a clock | AWS Free Tier | up to USD 200 of credit | - | - | email | retention-clamped | trial-only |
| a clock | Microsoft Azure Free Account | USD 200 for 30 days, and 750 h of three shapes for 12 months | - | - | card | retention-clamped | trial-only |
| a clock | AWS EC2 | USD 100 inside the six-month account window | USD 36.93 | 100 GB a month, all services | email, assumed | per-ip-shaping | trial-only |
| a clock | Azure Virtual Machines | no Linux allowance of its own | USD 28.55 | - | email, assumed | retention-clamped | qualifies-with-caveat |
| a clock | Civo Compute | USD 250 at signup | USD 21.43 | - | card | volume-quota | qualifies-with-caveat |
| a clock | DigitalOcean | no published signup amount | USD 24.00 | - | card | write-gated | paid-only |
| a clock | IBM Cloud VPC | 70% off for 12 months to 2026-12-31 | USD 23.59 | - | email, assumed | retention-clamped | trial-only |
| a clock | Open Telekom Cloud | EUR 250 on a booked contract | USD 94.27 | - | email, assumed | retention-clamped | trial-only |
| a clock | Kamatera | a separate trial page; 1 vCPU and 1 GB from USD 4 | USD 19.73 | - | card | volume-quota | trial-only |
| a clock | E2E Networks | a trial account granted on application | USD 33.65 | - | institution | write-gated | fails-identity |
| a clock | Alibaba Cloud ECS | USD 90 of credit on a card | USD 14.48 | - | email, assumed | request-rate | qualifies-with-caveat |
| a month, with a traffic term | Hetzner Cloud | CX23: 2 vCPU, 4 GiB, 40 GiB; marked "not available" | USD 6.70 | at least 20 TB a month | card | per-ip-shaping | paid-only |
| a month, with a traffic term | Contabo | Cloud VPS 4: 4 vCPU, 8 GiB, 100 GB | USD 6.60 | "unlimited", no rate | card | request-rate | paid-only |
| a month, with a traffic term | netcup | VPS 500: 2 vCPU, 4 GiB, 64 GiB | EUR 9.50 | flat rate, no rate | card | retention-clamped | paid-only |
| a month, with a traffic term | UpCloud | entry: 1 core, 1 GB, 10 GB, 250 Mbit/s | USD 14.00 | zero cost | email, assumed | request-rate | paid-only |
| a month, with a traffic term | Gcore | from EUR 8.93 a month | USD 13.92 | free on every VM | email, assumed | request-rate | paid-only |
| a month, with a traffic term | Exoscale | billed by the second in every zone | USD 35.61 | 1.42 GiB an hour | email, assumed | per-ip-shaping | paid-only |
| a month, with a traffic term | Latitude.sh | metal, VM and GPU by commitment term | USD 136.80 | 20 TB a month | email, assumed | per-ip-shaping | paid-only |
| a month, with a traffic term | Scaleway | from EUR 0.01428 an hour | USD 18.67 | in the list price | card | request-rate | paid-only |
| a month, with a traffic term | Linode | dedicated, shared and high-memory families | USD 24.00 | 0 to 20 TB by family | card | request-rate | paid-only |
| a month, with a traffic term | OVHcloud | b2-7: 2 vCore, 7 GB, 50 GB | USD 18.43 | included outside APAC | card | volume-quota | trial-only |
| a month, with a traffic term | Hostinger VPS | entry: 1 vCPU, 50 GB NVMe, two-year term | USD 14.99 | 4 TB on the entry plan | email, assumed | request-rate | paid-only |
| the hour, no traffic term | IONOS | CPU, RAM and GPU templates by the hour | USD 10.65 | - | card | request-rate | paid-only |
| the hour, no traffic term | KakaoCloud | six families; block storage billed apart | USD 23.44 | - | email, assumed | request-rate | paid-only |
| the hour, no traffic term | NAVER Cloud | seven families, hourly or monthly | USD 101.80 | - | email, assumed | request-rate | paid-only |
| the hour, no traffic term | Sakura Internet | from JPY 1,540 a month or JPY 7 an hour | USD 95.96 | - | email, assumed | request-rate | paid-only |
| the hour, no traffic term | Samsung SDS | hourly, with a 1 or 3 year commitment rate | USD 64.51 | - | email, assumed | request-rate | paid-only |
| the hour, no traffic term | Vultr | no free line for compute; the "Free" row is a storage appliance | USD 20.00 | - | card | volume-quota | trial-only |
| the hour, no traffic term | Ubicloud | by the minute on provisioned resources | USD 22.46 | - | email, assumed | request-rate | paid-only |
| the hour, no traffic term | Hetzner Dedicated AX | rented hardware, monthly | USD 77.40 | - | email, assumed | write-gated | paid-only |
| nothing read | Alibaba Cloud ACK | managed Kubernetes; the card asserts a tier and quotes none | USD 115.57 | - | email, assumed | request-rate | qualifies-with-caveat |
| nothing read | STACKIT | a machine-readable SKU feed with no free-tier field | USD 36.95 | - | email, assumed | - | qualifies-with-caveat |

⭐ **The egress column is still the finding, and it is thinner than this table looks.**
Seventeen of the 46 records carry a traffic figure anywhere: 5 in the `egress.terms`
field, 16 in a `free_allowance` or `extras.net.allowance` field, and 5 as a
`per-ip-shaping` limit, with overlap between all three. The other 29 carry nothing,
which includes every hyperscaler runtime in the next section. Five of the 46 state the
figure in a sentence a reader can price against: Contabo's unlimited, Google's 1 GB,
Hetzner's 20 TB, netcup's flat rate and Oracle's 10 TB.

⚠ **Six rows in the `Held 24/7` column are not clean dollars.** netcup's record quotes
EUR 8.26 and EUR 9.50, and it stores 9.50 in a field named `m24h_usd`. The table prints
the euro figure rather than misquote it. Five more quote a euro or yen price on their
page and carry a dollar figure in that field. They are Gcore, UpCloud, Scaleway, Open
Telekom Cloud and Sakura Internet. No record states the rate it used. Treat the column as
an order of magnitude across those six rows, never as a conversion.

**All 35 rows name an identity kind, and fifteen carry `card`.** Twenty-nine of the 46
records carry `email`, and for 28 of those the field's own text calls it an assumption
rather than a reading. Seventeen records state an identity from a page read. One row,
E2E Networks, names `institution` and is the only kind in the class that is neither
`email` nor `card`. The identity column is the weakest
column in this class, and no amount of arithmetic on the price columns repairs it.

## The eleven rows that are not VMs

Eleven of the 46 records in this class are billed by a unit of work and not by a
machine. AWS carries four: Fargate, Lambda, Lambda MicroVMs and Bedrock AgentCore.
Microsoft carries three: Azure Container Apps, Azure Container Apps Sandboxes and
Foundry hosted agents. Google carries two: Agent Engine and GKE Agent Sandbox. GitHub
and Tencent carry one each: Copilot cloud sandboxes and SCF. These are managed agent
runtimes. The records file them here because each is a place to run code and each is
reached with an account. This section prices them apart from the table above.

⛔ **A managed agent runtime is priced per vCPU-hour and per GiB-hour, and those units
are not a machine.** A VM price is a monthly cap on a box that exists. A runtime price
is a meter on something that exists only while a call is in flight. The same numeric
rate therefore produces a different bill at every duty cycle. `paid/README.md` states
the rule this section exists to enforce: a price without a duty cycle is not a price.

### Why the pricing is different, and what it does to the comparison

Three mechanisms separate a runtime from a VM, and each one moves the answer.

**The meter runs while the unit is allocated, not while it computes.** Azure Container
Apps bills a replica it considers active. Its page defines active as above 0.01 of a
core, or above 1,000 bytes a second of inbound data (`documented`,
`azure.microsoft.com/en-us/pricing/details/container-apps/`, read 2026-10-22). A replica
that idles above that threshold bills. That is the same failure as a stopped Azure VM
billing its allocated cores, at a smaller threshold.

**The free allowance is denominated in the same unit, so it expires in hours.**
Container Apps and Google's Agent Engine both give 180,000 vCPU-seconds and 360,000
GiB-seconds a month (`documented`, both pages read 2026-10-22). That is 50 vCPU-hours
and 100 GiB-hours. At 2 vCPU and 4 GiB the two limits bind at the same point: 25 hours.
Twenty-five hours is 3.47 per cent of a 720-hour month. Either free tier covers one
always-on agent for about a day and then stops.

**There is no monthly cap to stop the bill.** A VPS charges its monthly figure and then
stops. A runtime has no cap unless the vendor publishes a quota, and the meters here
count per second. Lambda's 15-minute invocation limit is the only wall-clock number in
the group. It caps one call rather than the month.

### The break-even against a rented box

A reader decides between a runtime and a VM on one number. That number is how long the
runtime can run for the price of the cheapest credible always-on box. The table prices
against Hetzner's CX23 at USD 6.70 a month, which is USD 0.009306 an hour over 720
hours, because every runtime record here was built at the same 2 vCPU / 4 GiB shape and
the CX23 is that shape. Contabo's Cloud VPS 4 is the cheaper row in this class at
USD 6.60 and returns 8 GiB for it; the two differ by 1.5 per cent, so no hour below moves
by more than one.

| Runtime | Record's 24/7 figure | USD an hour | Hours that cost one CX23-month |
| --- | --- | --- | --- |
| AWS Lambda MicroVMs | USD 181.58 | 0.2522 | 26.6 |
| Microsoft Foundry hosted agents | USD 177.12 | 0.2460 | 27.2 |
| GitHub Copilot cloud sandboxes | USD 165.52 | 0.2299 | 29.1 |
| Amazon Bedrock AgentCore | USD 156.10 | 0.2168 | 30.9 |
| Azure Container Apps Sandboxes | USD 155.52 | 0.2160 | 31.0 |
| GKE Agent Sandbox | USD 151.26 | 0.2101 | 31.9 |
| Azure Container Apps | USD 150.12 | 0.2085 | 32.1 |
| Google Agent Engine | USD 148.32 | 0.2060 | 32.5 |
| AWS Lambda | USD 108.33 | 0.1505 | 44.5 |
| Tencent Cloud SCF | USD 89.65 | 0.1245 | 53.8 |
| AWS Fargate | USD 41.83 | 0.0581 | 115.3 |

⭐ **Six of the eleven land between 26 and 32 hours, and the median is 32.0.** The
cluster is not a coincidence. A per-vCPU-hour runtime near USD 0.21 an hour at the 2
vCPU / 4 GiB shape is the hyperscaler list rate. USD 6.70 buys about thirty-two hours of it.
The rule a reader can carry away: **above roughly 32 hours a month a rented VM is the
cheaper purchase.** Below it the runtime wins. The runtime is also the only one of the
two that can be created and destroyed per request.

⚠ **The figure is sensitive to which box the reader calls the floor.** Against
GreenCloudVPS at USD 3.75 the eight rows that cost under 33 hours here land between 14.9
and 18.2 hours, and against the CX23 at USD 6.70 between 26.6 and 32.5. The ratio between
the two floors is 1.79, and
it moves every hour in the table by that factor. This document prices against the CX23
because the runtime records were all constructed at the same 2 vCPU / 4 GiB shape and the
CX23 is that shape; GreenCloudVPS's rung is 4 vCPU / 8 GiB and is not.

⚠ **Fargate at 115.3 hours is the outlier and it is not a better product.** Its record
prices a task at a lower rate and carries no memory term in the same figure. The column
therefore measures a different shape from the other ten. Read it as the cheapest
per-hour meter here. Read it also as the least complete record: it publishes no egress
term and no monthly cap either.

⚠ **Every figure in that table is a published rate, not a bill.** Only one of the eleven
records carries an explicit vCPU or RAM field, and it is Azure Container Apps at 0.25
vCPU / 0.5 GiB rather than the shape priced here. The "2 vCPU / 4 GiB" in the heading is
the topic's comparison shape, not a vendor specification. Two rows carry the unit rates
to rebuild, and only one of them lands on that shape: AgentCore does, to the cent, and
Copilot does not. The reconciliation is below.

### What each one costs to create, which is the part that surprises

⛔ **Ten of the eleven records mark the identity `email`, and every one of those ten
calls it an assumed value rather than a reading.** Azure Container Apps is the eleventh
and it names `card`, stated rather than assumed. No other runtime row carries a page that
states its signup requirement.
The gates the records do describe are these:

| Runtime | What the record says stands between a reader and a running unit |
| --- | --- |
| Amazon Bedrock AgentCore | an AWS account; the credit is "up to" USD 200 and the record keeps it at `reported` |
| AWS Fargate | an AWS account; the credit is the AWS Free Tier's, not a Fargate allowance of its own |
| AWS Lambda | an AWS account; 400,000 GB-seconds a month recur, and Provisioned Concurrency is excluded |
| AWS Lambda MicroVMs | an AWS account; the Lambda page carries no microVM line item at all |
| Azure Container Apps | an Azure subscription with a card; the allowance is per subscription |
| Azure Container Apps Sandboxes | an Azure subscription plus the `Container Apps SandboxGroup Data Owner` role |
| Microsoft Foundry hosted agents | an Azure subscription; the page publishes no runtime allowance and no USD 200 |
| GitHub Copilot cloud sandboxes | a Copilot plan; without a payment method, usage is blocked at the quota |
| Google Agent Engine | a Google Cloud project; the allowance recurs |
| GKE Agent Sandbox | a Google Cloud project; the agent-sandbox page returned 404 on every route tried |
| Tencent Cloud SCF | a Tencent Cloud account; log delivery bills under CLS, which has its own short-lived quota |

⭐ **GitHub Copilot's row is the one whose gate is a mechanism rather than a price.** The
record quotes the page: without a valid payment method, usage is blocked once the quota
is spent rather than billed past it. That is a `write-gated` limit in the record, and its
`binding` field still reads `request-rate`. Tencent SCF is the group's other `write-gated`
limit, but its gate is a billing route rather than a refusal: log delivery to CLS carries
its own short-lived quota. Copilot is the only row in the group whose free tier cannot
turn into an invoice.

⚠ **The GKE row is the group's only `unverified` record.**
`kubernetes-engine/docs/concepts/agent-sandbox` returned 404 on the broker read, a raw
fetch, a firecrawl read and an archive lookup, all on 2026-10-22. The record keeps the
GKE cluster allowance. That allowance is one Autopilot or zonal Standard cluster a month
against the cluster charge. The record states plainly that the agent-sandbox product is
not documented. Its USD 151.26 is therefore a construction against a product nobody
read.

⚠ **Two rows carry a credit their own note says was never re-read.** The AgentCore
record's 2026-10-22 evidence quotes the vCPU-hour and GB-hour rates and calls the credit
"up to USD 200". Its `free_tier.stated` still reads "USD 100.0 of one-time credit, from
the source card; not re-read". Foundry's note says the page "publishes no free runtime
allowance and no USD 200 figure", while its `free_tier.stated` carries USD 200. The field
and the note disagree twice, and the field is the one a table renders.

### The two arithmetic checks that reconcile

A price inherited from a card is worth checking against the vendor's own unit rates,
where the record carries both. Two rows reconcile exactly and one does not.

**Bedrock AgentCore reconciles.** Its page states USD 0.0895 per vCPU-hour and
USD 0.00945 per GB-hour. At 2 vCPU and 4 GB that is `2 x 0.0895 + 4 x 0.00945 =
USD 0.2168` an hour. Seven hundred and twenty hours is USD 156.10, which is the record's
figure to the cent. The page's v2 rate is USD 0.1276 per vCPU-hour on CPU alone, which
is USD 183.74 for two vCPUs over 720 hours. The record therefore holds the v1 rate.

**GitHub Copilot's does not, and the gap is 6.4 per cent.** Its page states USD 0.000024
per compute-second and USD 0.000003 per GiB-second. One compute-second a second is one
compute unit always on. Two units plus 4 GiB is `(2 x 0.000024 + 4 x 0.000003) x 3600 =
USD 0.2160` an hour, and 720 hours is USD 155.52. The record carries USD 165.52, which is
USD 0.2299 an hour. Solving for the compute rate gives 2.16 compute-seconds a second. The
record's figure is a 2.16-unit box, not the 2-unit shape this table prices.

**Container Apps and Agent Engine reconcile exactly.** Both records state their allowance
in vCPU-seconds and the sum is the same integer on both sides. The figures 180,000 and
360,000 give 25 hours at the 2 vCPU / 4 GiB shape.

**Fargate and Tencent SCF cannot be checked.** Neither record carries a unit rate to
check against, and Fargate's page was read for billing granularity only.

### The allowance against the credit, which are different offers

⛔ **A recurring allowance and a one-time credit are not the same free tier.** This group
splits six to five. Six rows carry a monthly allowance that returns: Lambda, Container
Apps, Container Apps Sandboxes, GitHub Copilot, Agent Engine and Tencent SCF. Five carry
a one-time credit: AgentCore, Fargate, Lambda MicroVMs, Foundry and GKE Agent Sandbox.
`gke-agent-sandbox` is the row where the credit is the only thing there is, because no
page was read.

The difference decides the second month. Fifty vCPU-hours a month returns every month
and is worth 600 vCPU-hours a year. A USD 100 credit against AgentCore's USD 0.2168 an
hour is 461 hours, which is 19.2 days, and then it is gone. Against Foundry's USD 0.2460
an hour, USD 200 is 813 hours, or 33.9 days. Against Fargate's USD 0.0581 an hour, the
same USD 100 is 1,721 hours, or 71.7 days.

⚠ **A credit is a countdown and an allowance is a budget.** The OVH row was
priced as a tier on a credit that was a trial.
[`history/2026-10-22T050900Z/ovh-public-cloud-has-no-free-instance.md`](../../../history/2026-10-22T050900Z/ovh-public-cloud-has-no-free-instance.md)
carries the correction. One division separates these five: the credit over the
hourly rate.

## Oracle Cloud Always Free

All tenancies get 1,500 OCPU-hours and 9,000 GB-hours a month on VM.Standard.A1.Flex.
Oracle states that is equivalent to 2 OCPUs and 12 GB. Each tenancy also gets up to two
VM.Standard.E2.1.Micro instances and 200 GB of block volume (`documented`, the Always
Free resources page at `docs.oracle.com`, read 2026-10-22). Egress is 10 TB a month, and
E2.1.Micro instances are capped at 50 Mbit/s.

⛔ **The allowance is a time-denominated quota, not a size cap.** The arithmetic
decides it. Two OCPUs run for 730 hours is
1,460 OCPU-hours, which fits inside 1,500 with 40 to spare. A 3-OCPU box at 24/7 is
2,190 OCPU-hours and does not fit at all. A reader who believes the ceiling is "2 OCPU"
will build a three-core box and meet a bill.

⚠ **The reclaim rule is the risk, and it is a percentile rather than a total.** Oracle
deems an instance idle when its seven-day 95th-percentile CPU is under 20 per cent. The
same test applies to network, and on A1 shapes it applies to memory. A workload that
sleeps for five days and bursts for two is still at risk.

The page contradicts itself on disk: one paragraph states a 47 GB minimum boot volume
and another states 50 GB. The record carries both and treats 50 GB as operative because
it appears in the allocation example.

Evidence: the Always Free resources page (read 2026-10-22) for the allowance, the
E2.1.Micro row, the reclaim test and the 200 GB volume. Verdict: the only perpetual free
VM in this class with a public address and usable egress. It is also the only one that
will take the machine back if it looks idle. The claim survives a test against all 511
records now filed under this category: the only other perpetual allowances with a
numeric egress figure are Google's 1 GB and `microlxc-tiny`'s 200 GB container, and
`oracle-cloud-vpn-node` is a second record of the same offer.

## Google Cloud's e2-micro

One non-preemptible e2-micro a month in us-west1, us-central1 or us-east1. It comes with
30 GB-months of standard persistent disk and 1 GB of outbound transfer from North
America (`documented`, `cloud.google.com/free/docs/free-cloud-features`, read
2026-10-22). The allowance is by time rather than by instance. Exactly one fits a month
and a second would bill.

⭐ **There is no idle reclaim.** Compute Engine's suspend and resume are user-initiated
and never triggered by idleness. That makes this the cleanest always-on row in the
topic. The e2-micro is a shared-core shape, two vCPUs bursting at about 12.5 per cent
each. It is a relay, a scheduler or a cron host, not a compute box.

⛔ **One gigabyte of egress a month is 0.0067 per cent of one day's serving.** One
gigabyte a month is 0.0333 GB a day. Against the 500 GB low end of the serving target
assumed here that is 0.0067 per cent. The row is included here because it is free and perpetual, not
because it can serve.

⚠ **A figure of 0.08 per cent is 12 times too high.** Three documents carry the
corrected 0.0067 — `free/README.md`, `relay-egress.md` and `compute/README.md`. The arithmetic is
one division, and it is shown here so a reader can check it.

Evidence: the Free Tier page (read 2026-10-22), the Compute Engine row and the three
quoted sentences. Verdict: the most reliable no-reclaim free machine here, with an
egress allowance too small to use.

## AWS and Azure, which are clocks and not tiers

Four records price the two hyperscalers as machines. Three are `trial-only`: both
account-level rows and the EC2 product row. The fourth, Azure Virtual Machines, is
`qualifies-with-caveat`, and the section on it below explains why that verdict does not
match its own free-tier sentence.

**AWS Free Tier.** It gives up to USD 200 of credit over six months: USD 100 on signup
and up to USD 100 more for completing activities. ⛔ **The account closes after six
months or when the credits run out** (`documented`, `aws.amazon.com/free/`, read
2026-10-22). There is no always-free EC2 shape for a new account. EC2 itself bills per
second with a 60-second minimum. Data transfer out is free to 100 GB a month across all
AWS services. A public IPv4 address is charged whether the instance is used or idle.

**AWS EC2** carries the machine row. It is `trial-only` and `reported`, and its USD 100
credit is the same credit the account-level record states as up to USD 200. The two rows
are one offer counted twice. Its own 2026-10-22 read proved the billing unit, the
60-second minimum and the 100 GB allowance, and proved nothing about the credit
(`aws.amazon.com/ec2/pricing/on-demand/`, read 2026-10-22). At the 2 vCPU shape it is
USD 36.93 for 24/7, which is 5.51 times Hetzner's USD 6.70.

**Azure Free Account.** It gives USD 200 of credit for 30 days. It also gives 750 hours
each of B1s, B2pts v2 and B2ats v2 burstable VMs for 12 months, then billed. Three shapes
at 750 hours is one of each running 24/7 for a month.

⚠ **Azure Virtual Machines is `qualifies-with-caveat` on a page that states no Linux
allowance at all.** The record's own `free_tier.stated` opens "no free allowance for a
Linux VM". The verdict still reads `qualifies-with-caveat` with `free_tier_kind:
one-time-credit`. The 750 hours belong to the account row above and to the Windows page,
not to this record. Its USD 28.55 for 24/7 is real and read from the page
(`azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/`, read 2026-10-22).
The verdict and the free tier beside it are not.

⚠ **Both hyperscalers are trials with a free aesthetic.** A reader who plans a year on
either has planned for the part before the clock. Neither has a free GPU:
`gcp-compute-gpu` and `azure-gpu` state that no free allowance applies to an
accelerator.

⭐ **The stopping state differs, and it is the trap on this pair.** Azure bills a Stopped
VM for its allocated cores. It stops only on Deallocate, which discards the temporary
disk (`documented`, the Linux pricing page, read 2026-10-22). AWS bills the public IPv4
address whether the instance runs or not. Neither charges nothing for a box that exists.

## Hetzner Cloud

No free tier. The entry shape CX23 is USD 6.70 a month at the corpus conversion,
excluding IPv4 and VAT, or USD 0.0104 an hour. Hetzner's own price-adjustment table
prints the same plan as USD 0.0104 an hour or USD 6.49 a month, and the 0.21 gap is its
exchange rate against the recorded 1.1193 rather than a different machine. The plan
shows "not available" in the eu-central locations NBG1 and HEL1 at the time of reading.
Outbound traffic is billed in 100 MB blocks rounded up. Cloud servers
in the EU include at least 20 TB of traffic a month (`documented`, `hetzner.com/cloud/`,
read 2026-10-22).

⭐ **Twenty terabytes a month is 666.7 GB a day.** That is 133 per cent of the 500 GB low
end of the serving target assumed here, and 61 per cent of one tebibyte a day. That, and
not the USD 6.70, is what makes this row the cheapest credible always-on box here. The
record reads `paid-only`, because there is no free tier for `qualifies` to describe. No
record in this class holds `qualifies`.

⚠ The 20 TB is vendor-stated, and Hetzner applies a discretionary threshold at a much
higher figure. `storage/gaps.md` records a separate 250 TB per month fair-use threshold
for the Storage Box line. That is a policy rather than a specification.

⚠ **The Hetzner row is the clean example of why this class needs two columns.** Its
record carries USD 3.12 at 10 hours a day and USD 6.70 at 24/7. That ratio is 2.15 rather
than the 2.4 that 300 hours against 720 would give. Both are correct. USD 0.0104 an hour
over 300 hours is USD 3.12. The same rate over 720 hours would be USD 7.49, so the
monthly cap stops it at USD 6.70. A VPS ratio below 2.4 means the cap binds. A reader who
assumes every row is a flat meter will overstate a VPS by that difference. Twenty-one
of the 42 records carrying both columns sit at 2.4. The ones below it
are the rows with a monthly cap.

Evidence: the Cloud page (read 2026-10-22) for the CX23 price and the traffic inclusion.
Verdict: the cheapest credible always-on box in this topic, and the benchmark every
runtime row above is measured against.

## The traffic terms that decide the paid lane

Every row below is `paid-only` and none is cheaper than Hetzner on CPU. They differ on
what a byte out costs. For a serving workload that difference is the whole comparison.

**UpCloud.** Servers from EUR 3 a month, data transfer carries zero cost, and the entry
size has 250 Mbit/s of bandwidth (`documented`, `upcloud.com/pricing`, read 2026-10-22).
⚠ The record carries a dated change: pricing changes take effect on 2026-11-16.

**Gcore.** VMs from EUR 8.93 a month, egress free on every VM, billed only while an
instance is active (`gcore.com/pricing`, read 2026-10-22).

**Exoscale.** Billed by the second across all zones, with outbound carrying a free tier
of 1.42 GiB an hour and inbound free (`exoscale.com/pricing`, read 2026-10-22). ⭐ 1.42
GiB an hour is 34.08 GiB a day, which is 3.3 per cent of one tebibyte. It is the only
row here that states a per-hour egress allowance rather than a monthly one.

**Latitude.sh.** 20 TB of free outbound a month and unlimited inbound on every plan, up
to 200 Gbit/s. Longer terms carry 50 and 65 per cent discounts.

**Scaleway.** Instances from EUR 0.01428 an hour, about EUR 10.42 a month. Egress and
IPv6 are included in the list price. Local storage and a public IPv4 are billed
separately (`scaleway.com/en/pricing/`, read 2026-10-22).

⚠ **Four of those five publish a term that excludes something.** UpCloud excludes the
IPv4 and the storage. Scaleway excludes storage and the public IPv4. Latitude prices the
commitment rather than the hour. Exoscale's free tier is a rate and not a quota, and
`METHODOLOGY.md` section 4.1 states the difference. A rate cap does not bound a day's
volume; a byte quota does.

## Contabo and netcup, the two that look cheapest

**Contabo.** Cloud VPS 4 is USD 6.60 a month with 4 vCPU, 8 GB and 100 GB of SSD. The
product description states traffic is unlimited (`documented`, `contabo.com`, read
2026-10-22). ⛔ **"Unlimited" with no published rate is a discretionary throttle, which
is worse than a quota.** There is no ceiling to design against. The record's binding
constraint is `request-rate` for exactly this reason.

**netcup.** VPS 500 G12.5 is EUR 8.26 a month on a twelve-month term. The page prints
EUR 9.50 "(incl. 19% VAT)" beside it, and it carries a traffic flat rate (`documented`,
`netcup.com`, read 2026-10-22). The contract is the constraint, and it is a year.
⚠ The two figures do not reconcile at 19 per cent: 8.26 x 1.19 is 9.83, and 9.50 / 8.26
implies 15.01 per cent. All five plans on the page show the same 1.150 ratio, so the label
and the arithmetic disagree by a constant. This document quotes both as printed and
derives neither.

⚠ Both are cheaper per vCPU than Hetzner. Neither is a better buy at the assumed scale,
because the egress term is unstated rather than generous.

## The regional providers

Eleven records price a VM in a market the English lists under-serve. They are Alibaba
Cloud ECS, IONOS, KakaoCloud, NAVER Cloud, Sakura Internet, Samsung SDS, OVHcloud Public
Cloud, Linode, Vultr, Ubicloud and Hostinger VPS. Eight of the eleven are `paid-only`.
Alibaba Cloud ECS is `qualifies-with-caveat`, and its reason is a credit rather than a
page. OVHcloud and Vultr are `trial-only`. None of the eleven carries a `per-ip-shaping`
limit, and all eleven carry the same placeholder in `egress.terms` — "not published on
the source card" — so the group publishes no usable traffic term.

⚠ **Eight of the eleven bind on `request-rate`, and that is the field's name rather than a
finding.** `request-rate` here means the hourly meter keeps running, which is the
constraint of any paid box. OVHcloud and Vultr bind on `volume-quota` instead. The only
row with a free-tier question is Alibaba Cloud ECS.
Its `qualifies-with-caveat` verdict rests on a USD 90 credit that the same record says it
has not re-read. Its page routes a new customer to a separate campaign page, and the
pricing page itself states no free allowance
(`alibabacloud.com/en/product/ecs/pricing`, read 2026-10-22).

⭐ **Two are worth naming for a reason other than price.** Vultr's page carries no free
compute allowance at all, and its only "Free" line is a storage appliance. That is the
kind of row a careless count treats as a free tier. Ubicloud bills by the minute on
provisioned resources and sells GitHub Actions runners from USD 0.00125 a minute. That
makes it a `ci-cd-runners` row with a VM attached.

⚠ **Kamatera and E2E Networks are the two rows whose free path is not a free tier, and
they fail for different reasons.** Kamatera is `trial-only` with `free_tier_kind: trial`,
and the trial is stated rather than hidden: one server worth up to USD 100 for 30 days,
with 1 TB of block storage and 1 TB of traffic (`kamatera.com/free-trial/`, read
2026-10-23). What it will not do is give a second server, so the cheap multi-box build the
preset prices invite is not available on it. E2E Networks is `fails-identity`, not a
trial: every named credit needs an incorporated company with a headcount and age test, so
a reader without a company cannot reach it at all
(`e2enetworks.com/pricing`, read 2026-10-22). An offer that costs a company is not a
trial a reader can plan against.

## The three rows whose free tier is a placeholder

Three records in this class say exactly "the source card records a free tier without a
credit amount", which is the placeholder `gaps.md` counts. Each is a catalogue artefact:
the card recorded that a field existed, not that a free allowance did.

**Alibaba Cloud ACK** and **STACKIT** both carry the placeholder with an `allowance`
kind. **Hetzner Dedicated AX / EX** carries it with `free_tier_kind: none`. That is the
same defect seen twice: the sentence asserts a tier and the kind field records none.

⚠ **STACKIT's record has a second problem and it is the larger one.** Its `confidence` is
`unverified` and its `binding` is null. Its `confidence_note` says the record is "a
mechanical conversion of the corpus card" whose `verified_at` is a card date rather than a
re-check. `gaps.md` lists STACKIT among the `unverified` records in the topic. Its
USD 36.95 is a construction, and no page stands behind it.

⚠ **A reader who scans for `qualifies` in this class gets an empty list, and
that is the repair rather than a gap.** Four records were reclassified from
`qualifies` to `paid-only` because they had an account at signup and no free
tier at all: Contabo, Hetzner Cloud, netcup and Hetzner Dedicated. The class
holds no `qualifies` record. `gaps.md` names the underlying problem as a
vocabulary defect rather than a data defect, and records the fix: a `--lint`
mode in `scripts/dossier/promote.py` refuses a record whose own free-tier
sentence says there is no free tier while the verdict says otherwise.
`conventions` defines `qualifies` as a storage test of "at least 500 GB free
per unit", and `compute` has never had an equivalent, so the four verdicts
were reclassified rather than redefined.

## What did not work

- **AWS as a perpetual free VM**: the account closes at six months. There is no
  always-free EC2 shape for a new account.
- **Azure's GPU free hours**: the 750 hours name three burstable CPU families and no
  GPU.
- **Azure Virtual Machines as a free offer**: the record's own free-tier sentence opens
  "no free allowance for a Linux VM".
- **Google's e2-micro as a serving host**: 1 GB of egress a month.
- **Contabo's "unlimited" traffic**: no published rate, so no ceiling to design against.
- **netcup as a short-term answer**: a twelve-month contract on the entry plan.
- **GKE Agent Sandbox and STACKIT**: both `unverified`, and neither names a binding
  constraint because neither number could be read.
- **Kamatera and E2E Networks as trials**: neither publishes what its trial gives.
- **A managed agent runtime as an always-on host**: six of the eleven cost more in 32
  hours than a CX23 costs for a month.

## Chaining

Oracle's A1 VM as the always-on address and Hetzner's CX23 as the paid box when the
reclaim test is unacceptable. The A1 gives 10 TB of egress and a reclaim rule; the CX23
gives 20 TB and no clock at all for USD 6.70. ⭐ The ordering rule is the one
[`../free/always-on-free.md`](../free/always-on-free.md) states. Put anything that must
not be reclaimed on the e2-micro, which has no idle test. Do not put it on Oracle, which
does.

⭐ **A runtime and a VM chain rather than compete.** The runtime is the right host for
anything that runs per request and stops, because there is no bill between calls. The
CX23 is the right host for the process that has to answer at 03:00. A runtime meter has
no monthly cap, and 30 hours of it costs the whole CX23 month. Put the scheduler on the
VM and the workers on the runtime.

## What this document covers, and what it cannot establish

**Coverage: 46 of 46, against the class as this document defines it.** Thirty-five are in
the table above and eleven are in the runtime section. Between them every record is named
and priced, or explicitly described as having no price. The test is re-runnable: for each
of the 46 slugs, does this file contain the slug or a recognisable form of the provider's
name. Twelve rows a string search cannot find by slug are named in the table below.

⚠ **The category label does not select 46 records.** `dossier/compute` holds 511 records
with `"category": "cloud VM"`. The reclassification came from
`scripts/dossier/promote.py`, whose `canon_category()` returns `cloud VM` when no rule
matches, so records that were filed elsewhere landed here. The 46 are the set this
document prices, and every figure on this page is against that set. The other 465 are not
audited here.

| slug | what names it |
| --- | --- |
| `aws-ec2` | AWS EC2, in the AWS and Azure section |
| `aws-lambda` | AWS Lambda, in the runtime table |
| `aws-agentcore` | Amazon Bedrock AgentCore, in the runtime table |
| `azure-container-apps` | Azure Container Apps, in the runtime table |
| `azure-container-apps-sandboxes` | Azure Container Apps Sandboxes, in the runtime table |
| `azure-vm` | Azure Virtual Machines, in the AWS and Azure section |
| `azure-foundry-agents` | Microsoft Foundry hosted agents, in the runtime table |
| `github-copilot-cloud-sandboxes` | GitHub Copilot cloud sandboxes, in the runtime table |
| `google-agent-engine` | Google Agent Engine, in the runtime table |
| `e2e-networks` | E2E Networks, in the regional providers section |
| `kamatera` | Kamatera, in the regional providers section |
| `tencent-scf` | Tencent Cloud SCF, in the runtime table |

**The document does not restate every record's numbers.** `paid/vps-monthly.md` owns the
monthly bill at the 2 vCPU shape for eighteen of these rows. This document does not
repeat its figures, and it does not silently disagree with it either. Where the two
differ, the difference is named below.

### The 29 records that remain thin, by axis

Coverage is not the same as depth. Tested on five axes, 29 of the 46 records fail at
least one, and 17 fail none. The 17 that fail none are the ones a recommendation can
rest on: `aws-ec2`, `azure-vm`, `contabo`, `exoscale`, `gcore`, `gcp-compute`,
`google-cloud-free-tier`, `hetzner-cloud`, `hostinger-vps`, `ibm-cloud-vpc`,
`latitude-sh`, `linode`, `netcup`, `oracle-cloud`, `ovhcloud`, `scaleway` and `upcloud`.
The egress axis reads "no usable traffic figure", which means no `egress.terms` sentence
beyond a statement that nothing is published, no `free_allowance`, no
`extras.net.allowance`, and no `per-ip-shaping` binding either.

| Axis | Records missing it | What a reader loses |
| --- | --- | --- |
| no usable egress term | 29 | whether the row can serve at all, which is the class's deciding variable |
| no 24/7 figure | 2 | any monthly comparison: the two account-level trial rows |
| unverified confidence | 2 | the number itself: `gke-agent-sandbox` and `stackit` |
| placeholder free tier | 3 | what the free allowance is: `alibaba-ack`, `hetzner-dedicated`, `stackit` |
| `qualifies` with no free tier | 0 | nothing: the four verdicts were reclassified to `paid-only` |

⭐ **The egress axis is the one that matters and it is the one almost nothing fixes.**
Twenty-three of the 46 records fail on egress and nothing else. For those rows the price,
the identity and the verdict are all read, and the traffic term is not. Five fail on two
axes: `alibaba-ack` and `hetzner-dedicated` on the placeholder, `gke-agent-sandbox` on the
confidence, and the two account-level trial rows on the 24/7 figure. One fails on three:
`stackit`.

⚠ **A single-axis failure is not a small failure here.** A row with a real price and no
egress term cannot be compared to Hetzner's 20 TB. Hetzner's 20 TB is what decides the
class. One page read each would clear the two `unverified` rows and the three
placeholders, and that is the cheapest work left in this document.

### Contradictions in the documents

**`paid/vps-monthly.md` prints twelve verdicts its records do not hold.** Of the
seventeen rows in its traffic table, twelve disagree with the record they cite. It gives
`qualifies-with-caveat` to IONOS, Gcore, UpCloud, Hostinger VPS, OVHcloud and Scaleway,
and `qualifies` to Hetzner and `qualifies-with-caveat` to Contabo and netcup. Those ten
records read `paid-only`, except OVHcloud, which reads `trial-only`. It gives
`paid-only` to Vultr, whose record is `trial-only`, and to Azure VM, whose record is
`qualifies-with-caveat`; and `trial-only` to DigitalOcean, whose record is `paid-only`.
Every one is a hand-written table disagreeing with the record it cites, which is the
error `docs/conventions/README.md` section 3.5 exists to prevent. That file is outside
this document's scope; its CX23 row also prints USD 6.49.

**The 24/7 column has two sources and they disagree on 12 of the 18 rows that carry
both.** Each record keeps a `m24h_usd` field and a `talaria_m24h_usd` field, and 18
carry both. Six agree exactly. Twelve differ, and the largest is Hostinger at USD 14.99
against USD 24.15, which is 37.9 per cent. The table above reads `m24h_usd` first where
it is set, because that is the field used as the monthly cap.

**The 24/7 column is 720 hours on 21 of the 42 records that carry both figures, and
not on the other 21.** A row whose 24/7 figure is exactly 2.4 times its 10-hour figure
was computed at 720 hours. The implied hours on the rest run from 300 to 815. Twelve
imply fewer than 720: Contabo and netcup at 300, `alibaba-ack` 401, `gke-agent-sandbox`
430, Hostinger 447, Hetzner Cloud 644, Copilot 664, Linode 667, Vultr 671, UpCloud and
DigitalOcean 672, `tencent-scf` 700. Nine imply more: STACKIT 750, AWS EC2 752, Azure
Container Apps 758, Azure Virtual Machines 759, Exoscale 763, E2E 765, AWS Lambda 790,
Scaleway 813, Alibaba ECS 815.

A reader subtracting one row from another across that set is subtracting different duty
cycles. The two directions have different causes. A figure below 720 is a monthly cap
binding, which is what a VPS does. A figure above 720 is a record whose 10-hour column
was built on fewer than 300 hours, and that is the error the column exists to expose.

**Three records in this class carry a placeholder free tier**: alibaba-ack,
hetzner-dedicated and stackit. Two more, azure-gpu and gcp-compute-gpu, carry the same
placeholder but are filed under `GPU cloud` rather than `cloud VM`, so they belong to a
class this document does not own.

**A figure of 0.08 per cent for the egress share is wrong by a factor of 12.** It reads
1 GB a month as 0.08 per cent of one day's serving. The division gives 0.0067 per cent
against 500 GB, and `compute/README.md`, `free/README.md` and `relay-egress.md` carry
0.0067.

### What this cannot establish

⛔ **No machine in this class was booted and no runtime was invoked.** Every figure is a
vendor page read on 2026-10-22 or a construction on a card. No record among these 46
carries the `measured` rung. Four records in the topic do, at the transport, listing or
price level and never at a quota, and one of them — `zenix-open-source-sponsorship` — is
filed under this category without being part of the 46 this document prices.

**Whether any of the eleven runtimes can be created at all.** Ten of the eleven records
carry no page that states their signup requirement, and each calls its `email` an
assumption. Azure Container Apps states a card and a subscription.

**What a byte out of a runtime costs.** Twenty-nine of the 46 records carry no traffic
term. That set is every runtime in the class plus most of the hyperscaler machine rows. A
runtime that serves a response bills for the response somewhere, and no record here says
where or at what rate.

**The price of the rows that need a specific account tier.** Azure Container Apps
Sandboxes needs a role assignment. GitHub Copilot needs a plan. Neither record carries
the plan's price. Bedrock AgentCore and Foundry are reachable only through an AWS or
Azure account whose own price is not in this class.

**Whether the thirty-hour break-even holds in practice.** It is arithmetic on two
published rates. It does not account for a runtime's minimum billing unit, its cold
start, or a vendor's own free allowance. None of those three is a field in these records.

⚠ Nothing in this document was booted. Every clock, allowance and egress term is a page
read on 2026-10-22. `gaps.md` records that the topic's four `measured` records measured a
transport, a listing or a price, and never a quota, so the rung would not settle any
figure on this page even where it exists.
