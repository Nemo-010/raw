# How a free compute tier is funded, and what that predicts

A free compute tier is a machine somebody else pays to keep powered. The counts below come
from a 619-record census of `dossier/compute/`; they describe that census, not the current
record count. Of the 543 records in it that carry a free offer, twenty name a mechanism,
seventy-seven show only the shape of an offer, and a hundred and forty-three give a quota
and no reason at all.

This document reconstructs what each group implies. It states what each predicts about
whether the tier survives, and it closes with which class to build on.

## The answer

**The compute record states its funding model far less often than the storage record
does.** `host-economics` found three models across seven hosts, and every one published a
reason. Here, 20 of 240 free offers state one.

⭐ **The words `sponsored`, `investor`, `donation` and `venture` appear in 28 records.**
Most are programmes whose own name carries the word, such as the Thiel Fellowship, Emergent
Ventures or Hub71, rather than a vendor explaining how its tier is funded: `aicrowd` sells a
"sponsored credit pool", `aws-activate-portfolio` is gated by an Org ID issued by an
investor, `compound-reverie-grants` is reviewed by a venture firm, and `boxybsd` states that
it accepts no donations. So the page remains mostly inference, and it says so in every
section.

The class that survives best is the vendor whose compute is the buyer's, at 14 free offers.
Its free tier is a licence, and its per-hour cost for a stranger is zero.

The class that looks like the answer and is not is the one-time credit, at 54 records. The
round-number figures and the stated expiries both say it is a marketing budget.

The class with the weakest promise is the vendor that publishes no price, at 31 records.
⚠ **No record in that class is `dead`**, so the ranking of it is a judgement and not a
measurement.

⛔ **No record in this topic is `measured`.** Nothing was booted. No bill was paid. No
registration was completed.

Every sentence below carries its rung. It is `documented` where a vendor page was read on
2026-10-22. It is `reported` where the figure came from the pinned catalogue. It is
`inferred` where this document reasons from the record. The funding model is `inferred`
throughout, because a record shows a price and the reason for it is a reading.

## The test, so a reader can re-run it

Every count below comes from one field or one search over `dossier/compute/`. The records
are the authority. This page is a view.

| the claim | the test | value |
| --- | --- | --- |
| records | one JSON file per record | 405 |
| free offers | `extras.free_tier_kind` is neither `none` nor null | 240 |
| offers that state a mechanism | the three rosters below | 20 |
| offers whose record shows a shape and no reason | a credit kind, or a published 24/7 bill | 77 |
| offers that state nothing beyond a quota | 240 minus 20 minus 77 | 143 |
| no published plan or price | a `write-gated` limit whose text says so | 31 |
| one-time credits | `extras.free_tier_kind: one-time-credit` | 54 |
| one-time credits at USD 100, 200 or 300 | the leading figure in `free_tier.stated` | 24 |
| recurring credits | `extras.free_tier_kind: recurring-credit` | 11 |
| records with a numeric 24/7 bill for a shape they also give away | `extras.m24h_usd` above zero | 27 |
| `dead` records | `verdict: dead` | 15 |
| records that publish a real egress term | `egress.terms` does not begin with "not " | 29 |

⚠ **The 20 is a floor and a judgement.** A record states a mechanism when its `free_tier`,
`notes` or `limits` gives a condition rather than only a quota.

The line matters. `baponi` says "Free forever, no card", which is a promise. `lapdev` says
"installed into the client's own Kubernetes clusters", which names who pays for the
silicon. The second is a mechanism and the first is a claim about the future.

## Three mechanisms the records state, and three things they only imply

The distinction is between a stated reason and a shape. A record that says "USD 200 of
credit, one time" has stated the size of a grant. It has said nothing about why the grant
exists.

| what the record shows | free offers | the evidence | rung |
| --- | --- | --- | --- |
| licensed non-commercially | 5 | the record names the status the reader must hold | `documented` |
| a beta | 3 | the record names beta, and two say what ends | `documented` |
| the compute is the buyer's | 14 | the record names the buyer's cluster, account or machine | `documented` |
| a credit, with no reason stated | 63 | `free_tier_kind` is `one-time-credit` or `recurring-credit` | `inferred` |
| a loss leader, with no reason stated | 14 | `extras.m24h_usd` prices the shape the offer gives away | `inferred` |
| a quota with nothing else | 143 | an allowance, a trial or a prepaid pack | `unverified` |

⭐ **The six rows sum to 242 and describe 240 records.** Two records carry two
reasons. The self-hosted `lapdev` is both a beta and the buyer's-hardware
class. The self-hosted `runs-on` is both a licence and the buyer's-hardware
class. The three `documented` rows are 22 reasons over 20 records.

⚠ **The last three rows are a partition, and the raw counts overlap.** The corpus holds 65
credit records and 27 records that publish a 24/7 bill beside a free offer. Thirteen carry
both, and two of the credits are already in the hardware row.

So the credit row is 65 minus 2, which is 63. The loss-leader row is 27 minus the 13 that
are also credits, which is 14. And 20 plus 63 plus 14 plus 143 is 240.

⛔ **The two `inferred` rows say nothing a record states.** No record says "this credit is
customer acquisition". None says "this tier is a loss leader".

What the record shows is a shape. A grant has a stated size. A free offer beside a
published bill has a price. The inference is that a vendor grants capacity to convert a
stranger. That is the reading the storage document reached for the same shape, and the
record cannot confirm the intent.

### The vendor's compute is the buyer's

Fourteen free offers sit in a product whose record names the buyer's cluster, account or
machine. Two of them give their free tier on the vendor's own compute, so they are not in the
table: `ferr` meters its 50 free browser hours on the vendor's "warm capacity", and its
self-run CLI is a different product; `zeabur`'s Free Plan deploys serverless services that
sleep, and managing a server the client owns is one row of its feature table. The other twelve
are below. Every one is a control plane, a licence or a local daemon, and not one is a machine.
The four hosted ones come first. The eight marked self-hosted need a machine the reader
runs, so they are the last resort.

| record | what the buyer supplies | what the free tier gives |
| --- | --- | --- |
| `porter` | the client's own AWS, Azure or Google account | a 6-month startup programme |
| `dockup` | the client's own AWS account | a free-forever plan |
| `hatchet-run` | the client's own workers | the first 100,000 runs |
| `amika` | the client's own machines | USD 50 of credits per organisation |
| `pipekit` | the client's own Kubernetes, under a managed control plane | a free trial of the control plane |
| `coder` (self-hosted) | infrastructure the buyer already owns | Community Edition, unlimited self-hosted workspaces |
| `okteto` (self-hosted) | the client's own Kubernetes | environments; the vendor supplies no compute |
| `lapdev` (self-hosted) | the client's own clusters | free during public beta, unlimited developers |
| `signadot` (self-hosted) | the client's own cluster | ephemeral environments that share it |
| `runs-on` (self-hosted) | the client's own AWS, at spot prices | a free licence for non-commercial use |
| `humanlayer` (self-hosted) | the client's own machine, through a local daemon | 200 sessions a month |
| `dagger` (self-hosted) | the client's own machine; the engine runs locally | the engine, open source |

⭐ **This class is the one the funding question resolves cleanly.** The vendor carries no
per-hour cost for a free user. The tier therefore costs a support ticket and a download.
That is why these offers can be perpetual when a sandbox credit cannot.

⚠ **It is also the class a reader with no hardware cannot use.** A licence to run
software elsewhere adds no capacity.

Seven further records in the class post no free tier, and each says why in one line.
`ellipsis` has "no per-seat fee for the platform" while "the compute bills to the client's
own AWS account". `butter` "embeds in the client's own process" (`documented`, read
2026-10-22).

### The one-time credit

Fifty-four records carry a one-time credit, which is the largest single credit kind. The
figures cluster on round numbers. That is what a marketing decision looks like when
somebody writes it down.

| figure | records | examples |
| --- | --- | --- |
| USD 300 | 2 | `gke-agent-sandbox`, `vertex-computer-use` |
| USD 250 | 1 | `civo` |
| USD 200 | 10 | `blaxel`, `daytona`, `hopx`, `ovh-gpu`, `microsoft-azure-free-account` |
| USD 100 | 12 | `e2b`, `novita`, `party`, `superserve`, `tenki`, `declaw` |
| USD 5 | 8 | `agent-37`, `coasty`, `sandbox0`, `sandbox-as-a-service` |
| no figure published | 9 | `browseract`, `createos`, `islo`, `scrapingbee` and five more |

Twenty-four of the 54 sit at exactly USD 100, USD 200 or USD 300. Eight sit at exactly
USD 5. A price that lands on a round number that often is set by a policy, not by a cost.

**What the mechanism predicts, worked through on one row.** `modal` prices the shape these
tables use at USD 0.2380 an hour for 2 vCPU and 4 GiB. Its USD 30 credit therefore buys 126
hours, which is 12.6 days at ten hours a day. Its own 24/7 column reads USD 173.71, so the
credit is 17.3 per cent of one always-on box.

⚠ **That arithmetic is the whole objection to the class.** USD 200 at the same rate buys
840 hours. That is 35 days at 24 hours a day and then nothing. The second month holds no
credit, and the offer never claims otherwise.

⛔ **The expiry is stated on several records, and it is easy to miss.** `digitalocean` and
`digitalocean-gpu` both say the credit is "valid for 90 days". Both add that "the credit
and any remainder expire at the end of that window".

`amazon-web-services-free-tier` says the account "closes after 6 months or when the credits
run out". `codesandbox-sdk` records a credit against a rate card its own record calls
"legacy". A grant, an expiry and a closing account are three mechanisms, and all three read
as "USD 200 free".

### The recurring credit

Eleven records carry a credit that renews. Ten are denominated in dollars and they sum to
USD 77 a month. The eleventh publishes credits rather than a figure, so it cannot be added.

| record | credit a month | what it buys |
| --- | --- | --- |
| `modal` | USD 30 | about 126 hours at 2 vCPU / 4 GiB |
| `blacksmith` | USD 12 | CI minutes; the record says "not re-read" |
| `insforge-instacloud` | USD 10 | a project that pauses when the credit runs out |
| `kedge` | USD 5 | about 244 vCPU-hours at USD 0.0205 |
| `kernel` | USD 5 | browser time, metered in GB-seconds |
| `opensteer` | USD 5 | platform credits; model credits are separate |
| `trigger-dev` | USD 5 | run compute, 20 concurrent runs |
| `solari` | USD 3 | sessions capped at 1 hour |
| `buddy` | USD 1 | compute and storage, 2 concurrency slots |
| `railway` | USD 1 | about 2 vCPU-hours at the VM rate |
| `airtop` | 1,000 credits | no dollar figure published |

**What the mechanism predicts.** A vendor that renews a credit has decided the free user is
worth carrying every month. That decision differs from granting USD 200 once. A recurring
cost is a cost the vendor has already put in a forecast, so it survives a budget review.

⚠ **The USD 77 total is not a budget, and the individual sums are small.** `freestyle`
shows what a real allowance costs its vendor. Its 200 vCPU-hours at USD 0.04032 is
USD 8.06, and its 400 GiB-hours at USD 0.0129 is USD 5.16. That is USD 13.22 a month per
free account.

Against its own USD 96.54 bill for an always-on box, that is 13.7 per cent.
`github-codespaces` gives 120 core-hours at USD 0.09, which is USD 10.80. Against its own
USD 120.60 bill that is 9.0 per cent. **A free tier here is a small fraction of the paid
tier, and that is exactly why it can persist.**

### The beta

Three free offers say the position is a beta. Each writes down what ends.

| record | the sentence the page carried | what ends |
| --- | --- | --- |
| `nebius-contree` | "runs don't consume your credits" while in beta | the beta, and "no notice is promised" |
| `apoxy` | "Invite-only beta" and "Request access" | the beta, and access is granted rather than bought |
| `lapdev` (self-hosted) | "currently in public beta and free to use" | the beta; the record calls its end "the clock" |

**What the mechanism predicts.** A beta is free because the price is not set yet. It ends
when the price is set. `ainclave` shows the same state in the paid lane and says it plainly:
"Rates are not published yet. We have not fixed the numbers."

⭐ **These three are the cleanest prediction in the document.** Each writes its end
condition into the record instead of leaving it implied. A tier that is free because it is
in beta has a known failure date. A tier that is free because an allowance covers it does
not.

### The non-commercial licence

Five records tie the free tier to a status the reader must hold. That status is the funding
model, because the vendor gives the product to a group it will never charge.

| record | the condition | what the record prices in its place |
| --- | --- | --- |
| `serv00` | "accounts are granted by a non-profit operator" | the non-profit's discretion |
| `teclada` | non-commercial use | paid plans at USD 100 and USD 500 a month |
| `runs-on` (self-hosted) | non-commercial, open-source and non-profit use | a link back; commercial licences EUR 300 to EUR 1,800 a year |
| `kasm-workspaces` (self-hosted) | individuals and non-profit organisations | a licence for commercial use |
| `tart-orchard` (self-hosted) | a free licence that "applies with no purchase" | Gold at USD 12,000 a year for 500 cores |

**What the mechanism predicts.** This class persists. The vendor has decided in advance
which users it will never charge, and a promise to a written-off group is cheap to keep.

⚠ It also ends the moment any of the output is paid work. No record defines where that line
falls.

## The three models this topic does not have

Three funding models exist in the storage topic and are absent here. Each absence is a
finding about the compute market rather than a hole in the reading.

**Advertising on a free tier.** Zero records. Five records contain a word formed from
"advert", and none describes a revenue model.

`serv00` states "no adverts" as a selling point. `flowdeploy` is a parked domain carrying
"keyword advertising for a link farm". `browsercloud`, `minicor` and `prime-intellect` use
the verb to say a page advertises a feature.

**A marketplace taking a spread on somebody else's hardware.** Three records describe a
marketplace, and all three publish no free tier. `vast-ai` says "prices are set by supply
and demand across 40 or more data centres". `shadeform` calls itself "The GPU Cloud
Marketplace" across "30+ top clouds".

`hyperbolic` prices an H100 at USD 3.19 an hour, on a page whose own limit says the rates
refresh weekly. All three carry `free_tier_kind: none`.

⭐ **That is the cleanest negative result here.** A marketplace cannot fund a free tier,
because its margin is a spread on a price it does not set. To give an hour away it would
have to pay the host from that spread. No record shows a marketplace doing so.

**Reselling committed capacity.** Eight records carry a contract term. `netcup` runs 12
months and `hostinger-vps` runs two years. `vast-ai` sells 1, 3 or 6 months and
`voltage-park` sells six. `shadeform` has a 12-month minimum, and `lambda`, `latitude-sh`
and `macstadium` bill annually.

Seven publish no free tier. The eighth, `netcup`, publishes none either, and its
`qualifies-with-caveat` verdict comes from a vocabulary defect this topic already carries.
**A reseller under a term has a floor cost every month and no room for a free user.**

## What the numbers predict, ranked by what a reader can act on

The rank is by how well the class's own record states its mechanism. A mechanism written on
a page is a better guide than one this document inferred.

| rank | class | free offers | survives because | dies because |
| --- | --- | --- | --- | --- |
| 1 | the recurring credit | 11 | the vendor has budgeted for it every month | the product is withdrawn |
| 2 | the buyer's own hardware | 14 | the free user costs the vendor nothing per hour | the software stops selling, or the reader has no machine |
| 3 | the non-commercial licence | 5 | the vendor wrote the group off in advance | the use becomes commercial |
| 4 | the beta | 3 | nothing; it is free because the price is unset | the beta ends, often with no notice |
| 5 | the one-time credit | 54 | one grant, already spent | the balance reaches zero |

⭐ **The death data separates two groups and refuses to separate five classes.** Fourteen of
the fifteen `dead` records carry `free_tier_kind: none`. That is 8.5 per cent of the 165
records with no free offer.

One of the 240 records with a free offer is dead, which is 0.4 per cent. It is
`browser-linux-emulators`, which its own `notes` field describes as "Not remote compute:
the cycles are the reader's own and the state dies with the tab". So the group holds no
clean death to read.

⚠ **Fifteen records cannot rank the five classes.** Two of the fifteen are census
guards rather than providers. The rank rests on the stated mechanism.

The death counts confirm only the coarser claim. The records with no free offer die about
twenty times more often than the records with one.

⚠ **`run-cloud` is the case a reader will reach for, and it cannot be counted.** It carried
a free tier of "a USD 15 a month recurring credit" before it was withdrawn. Its record
carries `free_tier_kind: none`.

So the most consequential withdrawal in this topic sits in the control group. Its lesson is
that a recurring credit did not save it.

## What this does not establish

⛔ **No revenue, cost or margin figure appears here, because no record carries one.** The
only arithmetic multiplies a vendor's published rate by that vendor's published allowance.
Both inputs are named in the sentence.

**Why 220 of the 240 free offers exist is not stated on any page.** That is 92 per cent of
the class. Of those 220, a credit or a published bill shows the shape of an offer for 77.
The remaining 143 show a quota and nothing else.

A record shows the quota and the price. It does not show the budget the quota is drawn
from. A reader who needs that reason for one provider must read material no page in this
corpus is.

**No survival claim here was observed.** Fifteen records carry `verdict: dead`. Every one is
a page that changed, a domain that lapsed or a deployment that was removed. Not one is a
tier observed to fail.

**Whether any free tier survives a second account is untested.** No registration was
completed, so every per-account figure here is a figure per one account.

**No provider was booted, so no funding model was tested against a live account.** A credit
that the page grants and a credit that a billing system honours are two claims. Only the
first is in this corpus.

## What this means for a reader with no hardware

The analysis assumes no local hardware and no institutional backing. The funding model
narrows the field to two rows, and both are the small ones.

⭐ **Build on the recurring credit first and the allowance second.** The eleven recurring
credits are the only offers here a reader can put in a spreadsheet. The amount is known, the
period is known, and the vendor has already forecast the cost.

`modal` at USD 30 a month is the largest. It buys 126 hours at the 2 vCPU shape, or 12.6
days at ten hours a day. `github-codespaces` is not a credit, but it behaves like one at 120
core-hours, which is 60 wall-clock hours a month of the default 2-core machine.

The class is small, renewable and predictable. That combination is the only one that
survives a plan.

⚠ **Do not build on the one-time credit, however large the figure.** `e2b` at USD 100 and
`daytona` at USD 200 are the two rows the free lane ranks high. Both are spent once, and
`digitalocean`'s 90-day expiry shows the balance can expire before it is spent.

⚠ **Do not build on the beta or the non-commercial licence.** A beta ends when the price is
set, and `nebius-contree` states that no notice is promised. A licence ends when the output
is sold, and no record says where that line is.

**Which class carries the weakest promise, and how to see it coming.** Thirty-one records
state in their own `limits[]` that they publish no plan and no price. The sentences read
"no plan and no price are published", "no self-serve price" and "rates are not published".

Twenty-one are `paid-only` and ten carry a qualifying verdict. Only seven of the thirty-one
carry a free offer at all.

⚠ **The prediction attached to that class is untested, and this page says so.** None of the
thirty-one is `dead`, so no withdrawal here confirms that a missing price forecasts one.

What the corpus does show is that those seven free offers sit on a page where nothing can be
valued. A product with no published rate and no published obligation has nothing in writing
behind its free tier. That is a reason to rank it last, and not a measurement.

A price on the page is not a guarantee either. `fly-io` kept a priced product and dropped
its free tier. **Neither a price nor its absence separates the survivors in this corpus.**
Only the stated mechanism does.

That gives the decision rule. Weight the plan toward the vendors that publish a rate, a
credit amount and a renewal period on one page. Treat a page with a free tier and no price
as a trial whose end date has not been announced. Use the buyer's-own-hardware class never,
because every free offer in it is a licence to run software on hardware the reader does not
have.

The reason a free compute tier cannot serve as the reader's server is not a lack of
capacity. It is that the 240 free offers are 240 separate funding decisions. Only 20 of them
state which, and only 11 renew.
