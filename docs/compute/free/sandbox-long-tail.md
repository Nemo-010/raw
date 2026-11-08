# The sandbox long tail: 121 records, and the five kinds among them

`free/sandboxes-container-vm.md` covers the eleven sandboxes a reader would act on
tonight. It cannot cover the other 110, and this document does. The class is the
largest in the topic at 121 records, and a reader has no way to tell a
USD 200 no-card credit from a 30-second invocation cap without opening each record.

The answer, in one paragraph. **The class is 29 allowances, 29 one-time credits, 9
trials, 3 recurring credits, 1 prepaid pack and 50 products with no free tier at all.**
So the "sandbox" label hides four different products: a monthly quota, a single grant, a
clock, and an invoice. The useful ranking is not by credit size, because a USD 200 credit
on a 1-hour session cap is worth less than a USD 50 credit with no cap, and the records
that state a buy-power figure say so in the vendor's own words.

## The class by kind

| kind | records | what it means for a reader |
| --- | --- | --- |
| allowance | 29 | a monthly quota, and the only kind that can be a standing budget |
| one-time credit | 29 | a single grant, and the second month is a bill |
| trial | 9 | a clock with a stated end |
| recurring credit | 3 | a small monthly grant; Buddy, Kedge and Solari |
| prepaid credit | 1 | Tensorlake's USD 5 to 20 packs |
| none | 50 | no free tier; 38 `paid-only`, 5 `dead`, and 6 that carry a `qualifies` verdict anyway |

⚠ **Six of the 50 "no free tier" records carry a `qualifies` verdict**: `boat`,
`ellipsis`, `omnara`, `onecli`, `scitix-agent-sandbox` and `ucloud`. That is the
vocabulary defect `gaps.md` names, and it is worst in this class because a reader
filtering on `qualifies` gets 50 per cent more rows than there are free products.

## The allowances, and what each one is actually worth

A monthly quota is the only kind that can be planned against. The records state these
in four different units, which is why they cannot be sorted in one column.

| Provider | Allowance | Unit | The catch |
| --- | --- | --- | --- |
| Freestyle | 200 vCPU-h, 400 GiB-h, 60,000 GiB-h storage | hours | a hard stop, and no persistent VM on Free |
| Vercel Sandbox | 5 active-CPU hours, 420 GB-hours of memory | active CPU | 45-minute maximum session |
| Microsandbox | 5 vCPU-h, 20 GiB-h memory, 20 GiB-h disk | hours | a 1 GiB durable limit |
| Rivet | 100,000 awake actor hours a month | awake hours | state and active CPU bill separately |
| Upstash Box | 5 CPU hours | CPU hours | a 5 GB disk on the entry shape |
| Archil | 5 disks of 10 GB, 1,000 tool calls, 30 min of sandbox | mixed | 30 minutes of sandbox compute in total |
| LangSmith Sandbox | 1 free seat, 1 Serverless (Small) deployment | seats | runtime bills at 0.0675 LSU a vCPU |
| Riza | 30 s per invocation, 128 MiB | per call | HTTP-only network |
| Deno Sandbox | a monthly request allowance | requests | a per-plan concurrency cap |
| Humanlayer (self-hosted) | 200 sessions a month | sessions | a local daemon runs the session |

⛔ **Five different units in one class, and no conversion between them.** A reader
comparing Vercel's 5 active-CPU hours to Freestyle's 200 vCPU-hours is comparing
active CPU to provisioned vCPU, and the ratio between them is the workload's own duty
cycle. That is why this table has a `unit` column and no total.

⭐ **Freestyle's 200 vCPU-hours is the largest sandbox allowance in the topic**, and it
is 100 hours of a 2 vCPU machine, which is 3.3 hours a day. Vercel's 5 active-CPU hours
sounds smaller and is a different measurement: it is CPU actually consumed, so a
sandbox that idles burns none of it.

## The one-time credits, ranked by what they buy

⛔ **A credit's size is not its value, and the records prove it.** Three vendors publish
their own buy-power figure and the arithmetic is checkable: Hopx's USD 200 at about
4,000 hours is USD 0.05 an hour, Isorun's USD 50 at about 1,250 hours is USD 0.04 an
hour, and Sandbox as a Service's USD 5 at about 56 hours is USD 0.089 an hour.

| Provider | Credit | Stated buy-power | USD/hour | Card |
| --- | --- | --- | --- | --- |
| Hopx | USD 200 | about 4,000 h of 1 vCPU / 1 GiB | 0.05 | no |
| Isorun | USD 50 | about 1,250 h of the default 1 vCPU / 1 GiB | 0.04 | no |
| Superserve | USD 100 | no time limit on a sandbox | not stated | no |
| Smol Machines | USD 100 | a base price of USD 0.04/h | 0.04 | no |
| Sandbox as a Service | USD 5 | about 56 h of a 2 vCPU / 4 GB | 0.089 | no |
| E2B | USD 100 | about 590 h at USD 0.17/h, in 1-hour sessions | 0.17 | no |
| Blaxel | USD 200 | not stated | not stated | no |
| Party | USD 100 | 2 concurrent sessions | not stated | no |
| Replicas | USD 100 | not stated | not stated | no |
| Declaw | USD 100 | plus USD 200 of separate guardrails credit | not stated | no |
| Tenki | USD 100 | 5 concurrent sessions | not stated | no |
| Novita | USD 100 | after an account setup survey | not stated | no |
| InstaVM | USD 50 | 10 GB of volume, 5 concurrent VMs | not stated | no |
| Amika | USD 50 | unlimited sandboxes on the client's own machines | not stated | no |
| Boxd | EUR 30 | RAM billed on use | not stated | no |
| Archal | USD 20 | USD 5 at signup and USD 15 at the first ready sandbox | not stated | no |
| Dedalus Labs | USD 20 | up to 4 vCPU, 16 GiB, 10 GiB disk | not stated | no |
| HUD | USD 10 | not stated | not stated | no |
| Miosa | USD 10 | up to 4 vCPU and 8 GiB | not stated | no |
| Agent 37 | USD 5 | and a card is required to get it | not stated | yes |
| Coasty | USD 5 | on a USD 0.05 per managed step meter | not stated | no |
| Paperpod | USD 5 | not stated | not stated | no |
| Pandastack | USD 5.40 | no egress charge on any plan | not stated | no |
| Sandbox0 | USD 5 | no one-hour compute minimum | not stated | no |
| Zipbox | USD 25 | requires a USD 5 top-up | not stated | yes |
| Createos | 500 credits | auto-pauses after 5 minutes idle | not stated | no |
| CodeSandbox SDK | a monthly credit | the rate card is labelled legacy | not stated | no |
| Vertex Computer Use | USD 300 | from the source card, not read | not stated | no |

⭐ **Hopx's USD 200 at USD 0.05 an hour is the largest usable grant in this class**, and
the reason is not the size. It is that the vendor published a conversion, so a reader
can compute a budget. Two-thirds of these rows publish a raw number and no rate, which
makes the credit unspendable in advance.

⚠ **Smol Machines' USD 100 does not expire** and behaves as ordinary prepaid balance,
which makes it the only row here that is not a clock. E2B's USD 100 expires into the
credit model and its one-hour session cap turns it into 590 sessions with setup between
each, which is a different product from 590 hours.

⚠ **Agent 37 and Zipbox both need a card** and no other one-time-credit row does. That
is the identity finding in this class: 27 of the 29 grants are reachable with an email
address alone.

## The recurring credits, which are only three

| Provider | Credit | What it is |
| --- | --- | --- |
| Kedge | USD 5 a month | consumed before paid credit, at USD 0.0205 a vCPU-hour |
| Solari | USD 3 a month | sessions capped at 1 hour, 3 concurrent browsers |
| Buddy | USD 1 a month | 2 concurrency slots, 1 seat |

⚠ **All three are small enough to be a rounding error.** The class's real budget rows are
`Modal` at USD 30 and `Railway` at USD 1, and Modal is filed as a `platform host` rather
than a sandbox. A reader who filters on this class for a recurring credit finds three and
misses the largest one.

## The trials, which are clocks with a number on them

| Provider | Trial | Ends |
| --- | --- | --- |
| Withruntime | 100 hours of a 1 GB machine, plus 100 GiB a month outbound | after 30 days |
| Shardflux | a trial at Pro limits | at the cap or after 30 days |
| Celesto | USD 5 runtime credit | after 30 days |
| Runloop | USD 50, 100 GB of storage | at the end of the Pro trial |
| Runta | USD 50, capped at 32 vCPU and 64 GiB in aggregate | at the balance |
| Stateset | USD 25 | at the balance, about 892 hours at 4 vCPU |
| Lizard | USD 5, and a card is required | after 7 days |
| Huawei Cloud | 20 CU once | at the balance, then CNY 1.1108 a CU |
| Collimate | a demo key, 2 concurrent at 1 hour | at the key |

⭐ **Withruntime's 100 hours in 30 days is the largest free trial in the class** and it
is 3.3 hours a day for a month, which is a real workload. It is `trial-only` because it
ends, and it is worth more than half of the one-time grants above.

## The five that died, and why the reason matters

`run-cloud` was withdrawn from new organisations and is the single most consequential
row in this topic: it was recorded as the cheapest row at USD 0.00.
The records carry `cloudrouter`, `computeruse-cloud`, `jamsocket` and `cua` as dead on a
catalogue card rather than a page.

⚠ **`cua` is the interesting one.** Its pricing page states that the current offer
connects computer-use agents to the client's own compute and that the earlier hosted
Fleet rate is no longer published. Dead as a host, alive as a framework, and a reader
who needs the framework will not find it by filtering on `dead`.

## What this class does not establish

⛔ **No sandbox here was booted.** Every allowance, credit and cap is a vendor sentence
read on 2026-10-22. This class carries no `measured` record, and the topic carries four;
`the-clock.md` records that 67 of the 1,411 records state a numeric clock at all.

**No credit was spent to exhaustion.** The buy-power figures are the vendors' own
estimates where they exist and arithmetic from a published rate where they do not, and
not one was verified by running out.

**No concurrency limit was tested.** Nineteen records state a concurrent-sandbox cap and
none states what a refusal looks like.

**No allowance was measured across a month.** A 5 vCPU-hour quota on the first day of a
billing cycle and on the twenty-eighth are the same sentence and different products.

## What did not work

- **Filtering this class on `qualifies`**: six rows carry a verdict their own record
  contradicts.
- **Ranking by credit size**: Hopx's USD 200 buys 4,000 hours and E2B's USD 100 buys
  590, so a 2x credit is a 7x difference in capacity.
- **Treating the class as one product**: 50 of 121 have no free tier at all.
- **A recurring credit as a budget**: three rows carry one and the largest is USD 5.
