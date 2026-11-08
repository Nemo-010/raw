# The sandbox long tail, part two: 58 records, and the mechanism that binds

`free/sandbox-long-tail.md` groups the class by the kind of free tier. This page groups the
remainder by the mechanism that stops a workload, because on this slice the kind field and
the binding constraint disagree more often than they agree.

The class is `category: container and VM sandbox`, which is 121 records. The two existing
documents name 63 of them between them, so **58 are here, and 19 of those carry a
`qualifies*` verdict**. All 19 carry `email` as the identity cost, so none of them wants a
card. That field is a read on only four of the 19, and on the other 15 the record says so in
as many words.

The answer in one paragraph. **One of the 19 states a renewable credit that converts to
money, and none of the others states a free compute quota at all.** `baponi` gives 1,000
credits a month and 10,000 at signup, and its own rate of USD 1.00 per 1,000 additional
credits makes that **USD 1.00 a month and USD 10.00 once**. `alibaba-agentbay` runs a free
Basic plan, and the record also says the plan pays for the resources it consumes, so the
storage is free and the compute is metered. `alibaba-agentrun` gives 15 GiB of disk and states
"no credit and no free compute". `arga-labs` gives a 60-minute expiry and publishes no price at
all, so the clock is real and there is nothing to buy. Five rows publish no plan and no price.
A reader who wants free compute from this slice has one row: `baponi`.

⚠ **That is the finding, and it is smaller than the class label promises.** A `qualifies*`
verdict on 19 of 58 rows sounds like 19 free sandboxes. One of them is a renewable credit with
a price on it. Four state a free plan at USD 0/mo, and `brimble` says the page publishes no
allowance for its own, `maritime` states no allowance at all, `openpond` says only "limited
monthly usage", and `alibaba-agentbay` publishes 100 GiB of storage against metered compute.
One is a clock with no price. Thirteen assert a tier and publish no size.

## How the 58 were computed

A record is in this page if its slug, its provider name, or the first token of its provider
name appears nowhere in `docs/compute/free/sandboxes-container-vm.md` or
`docs/compute/free/sandbox-long-tail.md`. That test names 63 of the 121 across the pair, so
58 remain. The pair overlaps on 9 rows, which is why 121 minus 63 is not 110.

One correction applies to the count. The test matches `docker` inside the
phrase "Play with Docker" in `sandboxes-container-vm.md`, which is a retired and different
product, so `docker-cloud-sandboxes` is dropped in error and belongs here. A plain substring
test that keeps every hit gets 57. `withruntime` is correctly absent: it has
two mentions of its own in the trial table.

## The 58 by the mechanism that binds

The first column names what actually stops a workload, not what the record calls the free
tier. The rows sum to 58.

| Mechanism | Records | What decides it | Rows |
| --- | --- | --- | --- |
| a concurrency cap | 3 | a session count between 5 and 10, with no hour quota beside it | `alibaba-agentbay`, `baponi`, `openpond` |
| a credit that does not renew | 1 | signup credits with no published size | `islo` |
| a session cap | 1 | 60 minutes in the product copy, and no price beside it | `arga-labs` |
| a free tier with no size | 13 | the page asserts a tier and publishes no amount, or no price at all | `alibaba-agentrun`, `brimble`, `dexto`, `gemini-code-execution`, `hoplite`, `isle`, `leap0`, `maritime`, `nebius-contree`, `orgo`, `orkestr`, `unikraft-cloud`, `volcengine-agentkit` |
| nothing free at all | 39 | a published rate, a sales gate, or a withdrawal | 38 `paid-only` and 1 `fails-identity` |
| a local machine (self-hosted) | 1 | software the reader runs, so no hosted capacity | `bytebot` |

The free-tier kind field on the same 58 says 38 `none`, 19 `allowance` and 1
`one-time-credit`. So the kind field and the mechanism agree on 39 rows and disagree on 19.
The fifth row is the finding of this page: 13 of the 19 qualifying records cannot be turned
into a budget, because the sentence that carries the verdict carries either no amount or an
amount that does not bound compute. `arga-labs` is counted as a session cap rather than as a
no-size row, because its clock is a number and its price is absent, and a clock with no rate is
a clock a reader can plan around.

## The 19 qualifying rows

Sorted by what a reader can act on. `Size` is an amount the record carries for the free tier,
and a dash means the record carries none. `Unit` is why the sizes do not sort into one column.
Four rows carry an amount, and only `baponi` and `alibaba-agentbay` state capacity to run work
on, because `alibaba-agentrun`'s 15 GiB is disk and `arga-labs`'s 60 is a clock.

| Provider | Stated free tier | Size | Unit | Binds | Rung |
| --- | --- | --- | --- | --- | --- |
| `baponi` | 1,000 credits a month, 10,000 at signup, 5 concurrent runs, no card | 1,000 | credits/month | 5 concurrent runs | `documented` |
| `alibaba-agentbay` | a free Basic plan on pay-as-you-go resources, 100 GiB storage, 10 Mbps | 100 | GiB | 10 concurrent sessions | `documented` |
| `arga-labs` | short-lived service twins that expire automatically; no price on the page | 60 | minutes | the 60-minute expiry | `documented` |
| `alibaba-agentrun` | 15 GiB of sandbox disk, and no free compute | 15 | GiB of disk | the disk, not the machine | `documented` |
| `islo` | credits at signup with no card; USD 0.07 a CPU-hour after | - | mixed | the credit balance | `documented` |
| `openpond` | a free tier with limited monthly usage; credits addable with no subscription | - | mixed | nothing on the free tier | `documented` |
| `maritime` | a Free plan at USD 0/mo with no card | - | none | nothing stated | `documented` |
| `brimble` | a Free plan at USD 0/mo; the allowances on the page belong to the USD 3 tier | - | none | nothing stated | `documented` |
| `leap0` | machines that spin up in 100 ms and tear down; the page prices nothing | - | none | an egress allowlist | `documented` |
| `orkestr` | free to start with no card, billed per second, no minimum, no platform fee | - | none | nothing stated | `documented` |
| `nebius-contree` | runs do not consume credits while the product is in beta | - | none | beta access | `documented` |
| `dexto` | models at USD 0.00 an input MTok; the page prices models, not machines | - | tokens | which model you call | `documented` |
| `isle` | the card asserts a tier; the site publishes no plan and no price | - | none | unknown | `documented` |
| `gemini-code-execution` | the card asserts a tier; the tool page publishes no quota of its own | - | none | unknown | `reported` |
| `hoplite` | the card asserts a tier; the site publishes no plan and no price | - | none | unknown | `reported` |
| `orgo` | the card asserts a tier; the extracted page carries no plan and no price | - | none | unknown | `reported` |
| `unikraft-cloud` | the page says idle infrastructure is not billed and prices no plan | - | none | unknown | `reported` |
| `volcengine-agentkit` | the card asserts a tier; the price table renders by script and was not read | - | none | unknown | `unverified` |
| `bytebot` (self-hosted) | Apache 2.0 software with no usage limit; the reader supplies the machine | - | unlimited | self-supplied hardware | `documented` |

Fourteen rows are `documented`, four are `reported` and one is `unverified`. Eleven of the 19
sentences contain a digit and eight contain none, and the gap between those two counts matters: a digit is not a size. `maritime` carries USD 0/mo, `brimble` the
same, `leap0` a 100 ms spin-up time, `dexto` a USD 0.00 token price, and `islo` three hourly
rates. None of those five digits says how much free capacity a reader receives.

## Baponi is the only row here that converts to money

⭐ **This is the one row in the slice a reader can budget from.** The record quotes USD 1.00
per 1,000 additional credits (`baponi.ai/pricing`, read 2026-10-22). That is the only
credit-to-money rate any of the 19 publishes, and it makes both free figures legible: 1,000
credits a month is **USD 1.00 a month**, and 10,000 credits at signup is **USD 10.00 once**.

`islo` shows what its absence costs. Its record publishes all three meters, USD 0.07 a
CPU-hour, USD 0.04 a GB-hour of memory and USD 0.0007 a GB-hour of disk, and states that
credits arrive at signup. The meters reproduce at 2 vCPU and 4 GiB as USD 0.30 an hour. The
record publishes no credit size, so the rate is priced and the budget is not.

`openpond` is the same defect with one more step removed. It publishes USD 10 a month for 10
concurrent sandboxes and says the free tier includes "limited monthly usage". The word limited
is where the arithmetic stops, so the rate is legible and the free quantity is not.

Fifteen of the 19 qualifying rows state no free compute quota, and they split three ways. Five
state a rate with no balance: `islo` publishes three hourly meters, `openpond` USD 10 a month
for its first paid tier, `brimble` and `maritime` a USD 0/mo plan with no allowance, and
`dexto` a USD 0.00 token price for some models. One states no limit at all because the software
is the product (`bytebot`). The other nine state neither a rate nor a size. The four outside
this group are `baponi`, `alibaba-agentbay`, `alibaba-agentrun` and `arga-labs`, and only the
first two state capacity to run work on.

## The 39 with nothing, and the 15 that are not a sandbox

The category label is wrong on 15 of the 39. They are filed as
`container and VM sandbox` and they do not rent a machine to anybody. ⛔ **A reader who filters
this class by `category` and assumes a machine gets 15 products that cannot be rented.**
Five price tokens or minutes and have no machine: `claude-managed-agents`, `openai-containers`,
`together-code-sandbox`, `minimax` and `sail`. A sixth, `moonshot-kimi`, sells a sandbox only
inside a hosted-agent product where runtime, tokens and plugin calls are three separate
meters.

Three are software or a wrapper the reader runs elsewhere: `butter` embeds a sandbox in the
reader's own process, `tencent-cubesandbox` needs a self-supplied x86_64 host with KVM, and
`arker` is a priced wrapper on an existing cloud account at 14 to 20 times the underlying rate.
Four are evaluation or benchmark suites rather than capacity: `halluminate`, `playgent`,
`refresh` and `vibrant-labs`. `runkit` is a browser notebook. `tilde-run` is closed and its
record points at the shutdown notice.

That leaves 24 ordinary merchants of a paid sandbox. Fourteen publish a rate in the sentence
that states there is no free tier. The other ten carry no rate, and each one carries a
different reason. `ainclave`, `chronicle-labs`, `claw2agent`, `omnirun` and `openreward` want a
written rate card, a booked call, a reviewed programme, a contract or an academic application.
`ppio-sandbox` prices its meters and sells credit as an account voucher. `seacloudai` is
`unverified` because no route returned its page. `tama` and `zhipu` state their meters on a
page this record does not cite, and `opencomputer` is the record that disagrees with itself.

The fourteen merchants with a rate are the group where the money is legible. Six of them
publish enough to check a per-hour figure:

| Provider | Published rate | Shape stated in the record | Per hour, computed |
| --- | --- | --- | --- |
| `nodus-compute` | USD 0.0075 | 1 vCPU, 1 GiB, 25 GB | - |
| `machine0` | USD 0.013 | 1 vCPU, 1 GB, 25 GB | - |
| `shellbox` | USD 0.02 | 2 vCPU, 4 GB, 50 GB | - |
| `mosaic` | USD 0.05 flat, RAM and storage included | - | USD 0.0500 |
| `docker-cloud-sandboxes` | USD 0.07 | 1 vCPU, 2 GiB | - |
| `prime-intellect` | USD 0.02 a vCPU-hour, USD 0.0125 a GiB-hour, USD 0.0002 a GiB-hour of disk | 1 vCPU, 1 GiB, 5 GiB | USD 0.0335 |
| `agentcomputer` | USD 0.07 a CPU-hour, USD 0.04375 a GB-hour of memory | 2 vCPU, 4 GiB | USD 0.3150 |

The last column is filled only where a reader can reproduce it from the columns beside it.
`prime-intellect` publishes its own worked example at USD 0.0335 a sandbox-hour, and
1 x 0.02 + 1 x 0.0125 + 5 x 0.0002 is USD 0.0335, so its three meters reproduce its own
figure exactly. `agentcomputer` at 2 x 0.07 + 4 x 0.04375 is USD 0.3150, and 300 hours of it is
USD 94.50, which is the record's own 10-hour column times 30.

Four of the five remaining rows publish a flat rate against a named shape, so their per-hour
figure is the stated rate and there is no second number to check it against: `nodus-compute`,
`machine0`, `shellbox` and `docker-cloud-sandboxes`. `mosaic` quotes a flat rate with no shape
at all, which is why its rate is the only money in the row and the shape cell is a dash.

## What the money columns hide

`sandboxes-container-vm.md` captions its 24/7 column as "`Held 24/7` is 730 hours". On the
rows of this slice that are pure hourly, the record's own two columns are a ratio of exactly
2.4, which is a 30-day month of 720 hours, not 730. Sixteen of the 27 slice rows that carry
both columns are in that class, among them `shellbox`, whose USD 0.02 an hour becomes
USD 14.40 at 720 hours and USD 14.60 at 730.

The scale is 1.39 per cent. That is too small to change a ranking and large enough to fail a
reconciliation, and it means the column mixes two month lengths under one caption. Across the
class, 36 of the 75 records with both columns use 720, six use 730 (`boat`, `e2b`,
`freestyle`, `opencomputer`, `vercel-sandbox`, `zipbox`) and the other 33 use some other ratio
because their shape carries a fixed monthly charge that does not scale with hours. `shellbox`
is the clearest of those: its stopped-slot fee is USD 0.50 a month whether it runs or not.

⚠ **The caption is the defect and not the arithmetic.** A 720-hour month is a defensible
choice and 16 slice rows make it consistently. The problem is that one document prints both
month lengths under the words "730 hours", so a reader who recomputes a row gets a different
number depending on which row they picked.

No row in this slice publishes an egress term. Zero of 58. Four of the 121 do: `boat`,
`freestyle`, `lizard` and `vercel-sandbox`. So a reader comparing this slice against the
class's four priced-egress rows has nothing to compare, and that silence is not a zero.

## Contradictions between these records and the two documents

`free/sandbox-long-tail.md` heads itself "121 records, and the five kinds among them" and its
own table lists six. The records confirm six: 29 `allowance`, 29 `one-time-credit`, 9 `trial`,
3 `recurring-credit`, 1 `prepaid-credit` and 50 `none`, which sums to 121. The headline's five
is the defect and the table below it is right.

⚠ **That same page's `none` row says "38 `paid-only`, 5 `dead`, and 6 that carry a
`qualifies` verdict anyway".** The records agree on all three, and the six are `boat`,
`ellipsis`, `omnara`, `onecli`, `scitix-agent-sandbox` and `ucloud`. The arithmetic in that
row also works, because 38 plus 5 plus 6 is 49 and the row is labelled 50, so one record is
unaccounted for. `openreward` is the missing one: it carries `fails-identity` rather than
`paid-only`.

`free/sandboxes-container-vm.md` opens "the eleven sandboxes a reader would act on tonight"
and its comparison table has 12 rows including a `dead` one. `free/sandbox-long-tail.md` opens
"it cannot cover the other 110". The 121 records carry 63 distinct names across the two pages,
of which 9 appear in both, so the records no document names are 58.

So the page that says it covers "the other 110" names 62 of them itself. There is no
arithmetic under which 110 is right: 121 minus the 12 table rows in its companion is 109, and
121 minus the 63 the pair actually names is 58.

The same page says "Nineteen records state a concurrent-sandbox cap" and 24 do. Twenty-five
records in the class carry a concurrency line in `limits[]`, and one of those is a negation
(`agent-37`: "no published concurrency or start-rate cap"), so 24 state a figure. On the
narrower reading of free-tier figures only, the count is 19, and the record does not say
which reading was meant.

`free/README.md` and `../gaps.md` both say 19 topic records hold a `qualifies*` verdict with
`extras.free_tier_kind: none`. The records agree. None of those 19 is in this slice: all 19
qualifying rows here carry `allowance` or `one-time-credit`, and 18 of them are `allowance`.
The class's six kind-`none` qualifying rows are `boat`, `ellipsis`, `omnara`, `onecli`,
`scitix-agent-sandbox` and `ucloud`, and both existing documents already name all six.

`opencomputer` runs the defect backwards. Its `free_tier.stated` describes a Free tier by
shape, up to 2 shared vCPU, 2 GiB of memory, 3 GiB of disk and 5 concurrency, and its verdict
is `paid-only` with `identity_cost: card`, on the ground that a plan requires a payment
(`opencomputer.dev`, read 2026-10-22). The stated tier and the verdict cannot both be right.
It is one of three `allowance` plus `paid-only` records in the topic, beside `gitlab-runners`
and `vultr-gpu`.

## What did not work

- **Filtering this slice on `free_tier_kind`.** It puts 19 rows in `allowance`, and 13 of
  those have no size for compute in the sentence that carries the verdict.
- **Ranking by the 10-hour money column.** 27 of the 58 carry one, and only 7 of the 19
  qualifying rows do, so the column is a ranking of the paid rows.
- **Treating `qualifies-with-caveat` as a usable tier.** Five of the 19 qualifying rows have a
  page that publishes no plan and no price, so there is nothing to obtain tonight.
- **Reading the category as a promise of a machine.** 15 of the 39 empty rows never rent one.

## What this does not establish

**Nothing here was booted.** All 58 rows rest on a page read on 2026-10-22 or on the
catalogue card, and 51 are `documented`. No session was started, no credit was spent and no
concurrency limit was reached, so "5 concurrent runs" is a sentence on a page and not a refusal
anybody observed.

**Whether any of the 13 unquantified rows is worth having.** Five of them (`hoplite`, `isle`,
`orgo`, `unikraft-cloud`, `leap0`) publish no plan or price at all, and two more
(`gemini-code-execution`, `volcengine-agentkit`) rest on a catalogue card whose page was read
and yielded no quota. One signup each would settle all 13, which is the cheapest verification available
in this class.

**What a session cap does to any of these rows.** 48 of the 58 carry a `session_cap.note` and
no number in either numeric field, and 9 carry no `session_cap` key at all. `arga-labs` at 60
minutes is the only numeric clock in the slice, and `../the-clock.md` already lists it among
the 24 wall-clock caps.

**Whether 10 of the 39 exist as a product.** Their `free_tier.stated` reads "the source card
records no free tier" and its `read_on` is 2026-10-02, so no page has been read. Sixteen
of the 58 carry `extras.reclassified_from: dead`, which means the record was moved out of
`dead` on an absence rather than on a page that showed a withdrawal.

**Where any of this traffic goes.** Zero of the 58 publish an egress rate, and `../gaps.md`
records that 365 of the 405 topic records publish none.

## The three rows whose own record contradicts their verdict

`../gaps.md` names the vocabulary defect: `conventions` defines `qualifies` as a storage test
and `compute` has no equivalent, so a verdict outlives the evidence under it. These three rows
carry a `qualifies*` verdict while their own `free_tier.stated` says there is no free tier.

| Record | Verdict | What the record's own sentence says |
| --- | --- | --- |
| `alibaba-agentrun` | qualifies-with-caveat | "no credit and no free compute; the only free allowance is 15 GiB of sandbox disk", and that disk is withdrawn while the instance is deep-asleep |
| `brimble` | qualifies-with-caveat | "the page publishes no CPU-hour, sandbox or bandwidth allowance for it", and the quotas it lists belong to the USD 3 tier |
| `unikraft-cloud` | qualifies-with-caveat | "no free tier stated: capacity with millisecond cold boots where idle infrastructure is not billed" |

All three were read on their own page on 2026-10-22, so this is not an inherited card. The
page said there was no free tier, the kind field says `allowance`, and the verdict says the
provider qualifies.

A reader filtering on the verdict gets 19 rows from this slice. Three of them have no free
capacity behind them in their own record, and 15 carry no size. ⛔ **The rows a reader can act
on tonight are `baponi` alone**: it is the only qualifying record here whose free tier is
renewable, sized and priced in the same sentence.
