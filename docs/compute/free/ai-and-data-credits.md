# AI and data credits: what one person reaches, and what a company is offered

Sixty-five records from the compute dossier, read on 2026-10-22: AI-native inference
vendors, data and warehouse platforms, voice and media generators, and accelerator
programmes. The question is narrow. What can a reader with an email address, no company and
no card claim, and what is the largest balance that exists only for a company?

The answer is USD 300 against up to USD 100,000. The class is worth less to a reader than
the storage lane, and the reason is structural. The vendors built their credit programmes for
companies, and the free product tiers they left for individuals are denominated in minutes
and images rather than dollars.

Confidence is `documented` for 55 records, `reported` for 6, `inferred` for 2, `unverified`
for 1 and `measured` for 1, and the one measurement is the DNS check on `playht-playai`.

## The short answer

**The reachable ceiling is USD 300**, from `clickhouse-cloud` ClickHouse Cloud, whose page
states USD 300 in credits for 30 days and 'no credit card required'. **The ceiling behind an
institution is up to USD 100,000**, published by `deepgram-startup-program` Deepgram's
startup programme and by `nvidia-dgx-cloud` NVIDIA DGX Cloud Lepton.

The two numbers are not the same quantity. USD 300 is a balance a person can spend this
week. USD 100,000 is a ceiling a company applies for, printed as 'up to' with no floor, and
the NVIDIA version is restricted to portfolio companies of four named venture funds. The
ratio is 100,000 / 300 = 333.

One record sits between them and must be named rather than folded in. `snowflake` Snowflake
offers USD 400 for 30 days, and its form asks for a 'Work email' and a 'Company name'. The
dossier records `email` because a personal address is accepted, but the label states the
expectation and no test was run. It is counted with the company group, not with the
card-free balances, and it is the one number here whose group is a judgement.

By verdict: 24 `qualifies-with-caveat`, 13 `fails-identity`, 11 `paid-only`, 9 `trial-only`,
7 `dead`, 1 `fails-quota`. Eighteen of the sixty-five are therefore either closed or sold
with no free lane at all.

## All 65 records

Grouped by sub-class so the sections below can refer to the rows. `Unit` is the measurement
the offer is denominated in, taken from the record. `Fails first` is the constraint that
stops the workload, which is not always the constraint the vendor prints.

| Provider | What is free | Unit | Expiry | Identity gate | Fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **Inference and GPU credits** | | | | | | |
| `anyscale` Anyscale | USD 100 of platform credit | hours | one-time, no expiry published | email, and the page asks for a work address | 176 T4-hours, then pay-as-you-go | qualifies-with-caveat |
| `cerebras-inference-research` Cerebras Inference Research | inference credits capped at USD 50,000 | none | not published | institution: a principal investigator at a university | the written proposal | fails-identity |
| `cudo-compute` Cudo Compute | nothing: every accelerator row is 'Quote on request' | none | none | institution: a sales enquiry | there is no self-serve signup | paid-only |
| `deepinfra-deepstart` DeepInfra DeepStart | 50,000,000,000 inference tokens | tokens | 1 year from approval | institution: a company that has raised | the funding threshold | fails-identity |
| `featherless-ai` Featherless AI | nothing; the lowest plan is USD 25 a month | unlimited | none | card | a 32K context and 4 concurrent units | paid-only |
| `genesis-cloud` Genesis Cloud | a trial credit whose amount is not published | none | trial, unquantified | card, plus a phone number and an SSH key | a quota request for GPU classes | trial-only |
| `gmi-cloud-scale` GMI Cloud SCALE | USD 500 on acceptance, a 1:1 match to USD 4,500, a USD 3,000 GPU voucher | hours | the cohort term | institution: admission to a cohort of about 25 | the match needs USD 4,500 spent first | fails-identity |
| `lepton-ai` Lepton AI | nothing: the platform stopped on 2025-05-20 | none | closed | anonymous | no endpoint resolves | dead |
| `nomic` Nomic | a free plan, no card, allowance not quantified | users | not stated | email | 'Limited agent requests', number unpublished | qualifies-with-caveat |
| `nvidia-dgx-cloud` NVIDIA DGX Cloud | up to USD 100,000 in GPU capacity credits | none | not published | institution: portfolio companies of four named funds | workspace activation by a technical account manager | fails-identity |
| `nvidia-launchpad` NVIDIA LaunchPad | nothing: it was USD 20,000 of cloud-equivalent capacity | none | closed, 2025-11 | email | the lab URL redirects to build.nvidia.com | dead |
| `ori-global-cloud` Ori Global Cloud | nothing: merged into Radiant, no price page | none | none | institution: a sales relationship | no signup form exists | paid-only |
| `predibase` Predibase | nothing: a Rubrik subsidiary since 2025-06-24 | none | closed | institution | the pricing URL lands on an enterprise product | dead |
| `siliconflow` SiliconFlow | CNY 14, plus a CNY 16 voucher after real-name | tokens | the CNY 16 lasts 180 days | country-phone: a mainland mobile number | CNY 14 buys 20 million tokens on a 14B model | fails-identity |
| `upstage` Upstage | nothing; the free week closed on 2026-08-11 | none | closed | card | every call is metered per token | paid-only |
| `venice-ai` Venice AI | nothing on a free account; USD 5 only for subscribers | none | none | card | 'There is no unmetered API tier' | paid-only |
| `xai-grok-api` Grok API | nothing documented; the USD 150 a month credit is gone from the index | none | withdrawn | card | a prepaid balance before the first call | paid-only |
| **Data and vector infrastructure** | | | | | | |
| `clickhouse-cloud` ClickHouse Cloud | USD 300 in credits | GiB | 30 days | email, 'no credit card required' | the day-30 clock, then pay-as-you-go | trial-only |
| `cratedb-cloud` CrateDB Cloud | 2 vCPU, 2 GB RAM, 8 GB storage, a daily backup | GiB | none: perpetual | email | the 8 GB storage cap | qualifies-with-caveat |
| `grafana-cloud` Grafana Cloud | 10,000 active series and 50 GB of logs a month | GiB | perpetual, 14-day retention | email, no card | 10,000 active series | qualifies-with-caveat |
| `influxdb-cloud-serverless` InfluxDB Cloud Serverless | 5 MB per 5 minutes, 2 buckets, 30-day retention | minutes | perpetual | email | the ingest rate, which cannot be burst | qualifies-with-caveat |
| `motherduck` MotherDuck | 10 GB of storage and 10 Pulse compute-hours a month | hours | perpetual | email, card not required | the 10 compute-hours | qualifies-with-caveat |
| `neo4j-auradb` Neo4j AuraDB | 200,000 nodes, 400,000 relationships, 1 GB | hours | perpetual; pauses at 72 idle hours, deleted at 30 days | email | 400,000 relationships | qualifies-with-caveat |
| `singlestore` SingleStore | 1 GB compressed per cluster, 10 tables, unlimited clusters | GiB | perpetual | email | 10 tables per database | qualifies-with-caveat |
| `snowflake` Snowflake | USD 400 in credits | none | 30 days | email, and the form asks a work email and a company name | day 30 ends access and credit together | trial-only |
| `tiger-cloud` Tiger Cloud | a 30-day trial of the Performance plan | GiB | 30 days | email, no card | day 31 has no free tier to fall back to | trial-only |
| **Voice and media** | | | | | | |
| `amazon-polly` Amazon Polly | 5 million Standard characters a month, about 115 hours | hours | monthly; every better voice 12 months | card | the 12-month drop back to Standard | qualifies-with-caveat |
| `assemblyai` AssemblyAI | USD 50 in credits | hours | one-time | email, no card | 5 new streaming connections a minute | qualifies-with-caveat |
| `black-forest-labs` Black Forest Labs | nothing; USD 0.048 an image | none | none | email, then a card for the first image | no free lane exists | paid-only |
| `cartesia` Cartesia | 20,000 credits a month: 27 minutes of speech or 1h51m of transcript | hours | monthly, rollover caps at 2x | email | the 27 minutes | qualifies-with-caveat |
| `deepgram` Deepgram | USD 200 in credits | hours | one-time; the FAQ says none, the docs say one year | email, no card | 50 REST connections, 150 on WSS | qualifies-with-caveat |
| `deepgram-startup-program` Deepgram Startup Program | up to USD 100,000 over 12 months | none | 12 months from issue | institution: company, funding and team disclosure | discretionary approval | fails-identity |
| `elevenlabs` ElevenLabs | 10,000 credits a month, about 10 minutes of speech | minutes | monthly, no rollover | email | the monthly pool | qualifies-with-caveat |
| `elevenlabs-startup-grants` ElevenLabs Startup Grants | 33,000,000 characters for 12 months | hours | 12 months | institution: business email, under 25 employees, one per company | the review committee | fails-identity |
| `gladia` Gladia | EUR 50 in credits | hours | one year | email, no card stated | the 12-month wallet | qualifies-with-caveat |
| `google-cloud-text-to-speech` Google Cloud Text-to-Speech | 4 million characters a month for Standard and WaveNet | hours | monthly | card: billing must be enabled | an overrun bills with no prompt | qualifies-with-caveat |
| `hume-ai` Hume AI | nothing self-serve; the September free plan is withdrawn | minutes | withdrawn | institution: 'contact our team to request access' | the access request | fails-identity |
| `ideogram` Ideogram | nothing on the price list; USD 15 is the entry | unlimited | none | email | the cheapest credit costs USD 15 | paid-only |
| `kling-ai` Kling AI | 66 credits a day, claimed and contradicted | hours | daily, if it exists | email | 360p to 540p output and a watermark | fails-quota |
| `leonardo-ai` Leonardo.Ai | 150 Fast Tokens a day | tokens | daily, no carry-over | email | 'Auto Only' models and Basic quality | qualifies-with-caveat |
| `luma-ai` Luma AI | nothing; USD 30 buys the first 10,000 credits | none | none | email | no free row on the pricing page | paid-only |
| `pika` Pika | a USD 0 plan whose credit row reads '0 - packs only' | none | none | email | zero monthly credits | paid-only |
| `playht-playai` PlayHT / PlayAI | nothing: the domain does not resolve | none | closed, end 2025 | anonymous | api.play.ht returns a non-existent domain | dead |
| `recraft` Recraft | 30 credits a day, a third-party figure | none | daily, no rollover | email | free outputs are owned by Recraft and public | qualifies-with-caveat |
| `rev-ai` Rev AI | 5 hours of Reverb, worth USD 1.00 | hours | one-time | email | USD 1.00 is the whole allowance | trial-only |
| `runway` Runway | 125 one-time credits | seconds | one-time | email | 60 credits per 5 seconds of Gen-4.5 | trial-only |
| `speechmatics` Speechmatics | USD 100 in credits | hours | not stated | email, 'No card required' | the discount ladder: USD 0.24 base, not 0.121 | qualifies-with-caveat |
| `stability-ai` Stability AI | 25 credits, which is USD 0.25 | none | not stated | email | 3 images on SD 3.5 Large | trial-only |
| `suno` Suno | 50 credits a day, about 10 songs | none | daily, no carry-over | email, no card | the v6-mini model only, no commercial rights | qualifies-with-caveat |
| **Accelerators** | | | | | | |
| `arm-virtual-hardware` Arm Virtual Hardware | 15 cores, 100 core-hours, 25 device slots | hours | 30 days | email | 100 core-hours over 5 cores is 20 wall-clock hours | trial-only |
| `axelera-ai-voyager` Axelera AI Voyager | EUR 25 of assistant tokens | tokens | not published | email | no device is attached; the card is separate | qualifies-with-caveat |
| `cann-points-mall` CANN points mall | 100 CANN points per Ascend card-hour, earned by tasks | none | not stated | country-phone: a Huawei Cloud account with real-name | how many points the community issues | qualifies-with-caveat |
| `degirum-ai-hub` DeGirum AI Hub | nothing: operations ceased 2026-08-01 | none | closed 2026-09-30 | email | the service ended 22 days before this reading | dead |
| `esperanto-technologies` Esperanto Technologies | nothing: the company ceased operations | none | closed | anonymous | the homepage says so and still sells the server | dead |
| `furiosaai-furiosa-access` FuriosaAI Furiosa Access | evaluation access, no allocation published | none | none | institution: a business email and a sales call | the sales form | fails-identity |
| `graphcore-ipu-cloud` Graphcore IPU Cloud | nothing: the free-trial page returns 404 | none | closed | institution: a quote for four cards | the four-card minimum | fails-identity |
| `intel-liftoff` Intel Liftoff | credits, amount never published | none | not published | institution: an early-stage startup, reviewed | the application review | fails-identity |
| `k-cloud` K-Cloud | 4 ATOM+ cards inside KT Cloud, by selection | none | the programme term | institution: a Korean demand company | the NIPA selection | fails-identity |
| `moore-threads-ai` Moore Threads AI | a 30-day free trial, 100 signups a day | none | 30 days | country-phone, reported | 100 signups a day, then the clock | trial-only |
| `psc-neocortex` PSC Neocortex | CS-3 time on 2 nodes, allocation size unpublished | none | the allocation term | institution: a PI at a US academic or non-profit | the PI requirement | fails-identity |
| `qualcomm-ai-hub` Qualcomm AI Hub | compile, profile and infer on hosted devices | GiB | perpetual, no quota published | email | no ceiling or rate is published at all | qualifies-with-caveat |
| `sima-ai-edgematic` SiMa.ai Edgematic | a free beta through AWS Marketplace | none | the beta, no end date | card: an AWS account | no device-minute figure is published | qualifies-with-caveat |
| `tenstorrent-tt-console` Tenstorrent TT Console | browser inference on Tenstorrent hardware | TiB | not published | email | no rate, session or token figure is published | qualifies-with-caveat |
| `untether-ai` Untether AI | nothing: bankrupt 2025-10-15, assets to AMD | none | closed | anonymous | speedAI and the SDK stopped being supplied | dead |
| `hailo-developer-zone` Hailo Developer Zone (self-hosted) | the compiler, runtime and model zoo; no silicon | none | none | email | the output runs only on a purchased module | paid-only |

## What each sub-class is worth

### Inference and GPU credits: USD 100

Seventeen records. Two carry a balance: `anyscale` at USD 100, which a person can spend, and
`siliconflow` at CNY 14, which the phone number blocks. The other fifteen split six paid-only,
four institution-gated, three dead, one unpublished trial and one unquantified free tier.

The reachable balance converts to machine time because the record carries a balance and an
hourly rate. USD 100 / USD 0.5682 an hour = 176.0 T4-hours. USD 100 / USD 4.9591 an hour =
20.2 A100-hours.

Token credits convert only where the record pairs a token count with a token price, and the
multiplication is shown rather than summarised:

- `deepinfra-deepstart`: 50,000,000,000 tokens / 1,000,000 = 50,000 million-token units.
  50,000 x USD 0.06 = USD 3,000 of input. 50,000 x USD 0.18 = USD 9,000 of output. The grant
  is real and the gate is a funding threshold, so the figure is company-only.
- `siliconflow`: 20 million tokens x CNY 0.7 per million = CNY 14.
- `xai-grok-api`: USD 150 / USD 2.00 per million input tokens = 75 million tokens a month.
  USD 150 / USD 6.00 per million output tokens = 25 million. Conditional, because the credit
  is not on the current documentation index: this is what the withdrawn offer would be worth.

The two largest numbers in the slice cannot be converted, so none is attempted.
`cerebras-inference-research` carries USD 50,000 and `nvidia-dgx-cloud` carries USD 100,000,
and neither record holds a token price. A dollar of inference credit is not a dollar of GPU
time.

**Where the sum breaks.** There is no sum. USD 100 plus CNY 14 is two currencies, and one is
blocked at registration. The sub-class total for an individual is one T4 for 176 hours.
Everything above it belongs to somebody with an affiliation.

### Data and vector infrastructure: USD 300, and 20 GB that renews

Nine records, six with a perpetual lane and three with a 30-day clock, and no dead vendors.
Currency: USD 300 from `clickhouse-cloud` plus USD 400 from `snowflake` is USD 700 nominal,
and the sum misleads twice. Both expire in 30 days, and the 400 carries a company-name field,
so the reachable figure is 300.

Perpetual storage: `cratedb-cloud` 8 GB + `motherduck` 10 GB + `neo4j-auradb` 1 GB +
`singlestore` 1 GB = 20 GB as the vendors print it. Converted, 20 x 10^9 / 2^30 = 18.6 GiB,
and each row keeps the decimal figure the vendor published. `motherduck` adds 10 Pulse
compute-hours a month, which is 120 hours a year. `influxdb-cloud-serverless` gives a rate
rather than a volume, 5 MB per 5 minutes, which the record computes as about 1.4 GiB a day
and which cannot be burst for a backfill. `grafana-cloud` gives 50 GB of logs a month with 14
days of retention, which is an observation window and not a store.

**Where the sum breaks.** The four storage addends are four products. CrateDB is distributed
SQL over a Postgres wire protocol, MotherDuck is DuckDB over managed Parquet, AuraDB is a
property graph, and SingleStore is a row and column store. Adding their bytes assumes one dataset can be split across four query languages. `singlestore` breaks the addition
twice over: unlimited 1 GB clusters make the term a function of the partitioning done
by hand, and a schema change means rebuilding a cluster.

The class has no vector database. The nearest record is `nomic`, which moved from embeddings
to document parsing and publishes no request count, and `neo4j-auradb` is a graph rather than
a vector index. That gap is real and this slice does not fill it.

### Voice and media: USD 351.25 plus EUR 50, and 1,841 hours of transcript

Twenty-three records. Eleven carry a free allowance with a caveat, three are one-time trials,
four are paid-only, three are institution-gated, one is dead and one is an unverified daily
allowance.

Speech-to-text hours, added as the records state them:

- `deepgram` 775 hours, from USD 200 / USD 0.0043 a minute = 46,511 minutes.
- `speechmatics` 416 hours, from USD 100 / USD 0.24 an hour at the base rate.
- `assemblyai` 333 hours, from USD 50 / USD 0.15 an hour.
- `gladia` 312 hours, the vendor's own figure for EUR 50 on solaria-3.
- `rev-ai` 5 hours, which is USD 1.00 of Reverb at USD 0.20 an hour.

775 + 416 + 333 + 312 + 5 = 1,841 hours, once, and only if every vendor is new to the reader.
Nominal balances: 200 + 100 + 50 = USD 350, plus USD 1.00 from `rev-ai` and USD 0.25 from
`stability-ai`, which is USD 351.25. `gladia` bills in EUR and stays EUR 50.

Text-to-speech is the strongest recurring lane in the document and it belongs to two
hyperscalers rather than to any AI startup. `amazon-polly` gives 5 million Standard characters
a month, which the vendor's own table converts at 23 hours 8 minutes per million, so about
115 hours. `google-cloud-text-to-speech` gives 4 million characters a month, which is 4,000
minutes or 66 hours at 1,000 characters a minute. 115 + 66 = 181 hours a month. The two voice
startups give `elevenlabs` 10,000 credits, which is 10 minutes, and `cartesia` 20,000 credits,
which the vendor converts to 27 minutes. 10 + 27 = 37 minutes. The ratio is 181 x 60 / 37 =
293, so the hyperscalers give 293 times the monthly speech, and both require a card.

Images and video are counted in generations. `runway` gives 125 one-time credits, which is
10.4 seconds of Gen-4.5 at 60 credits per 5 seconds, or 15 images. `leonardo-ai` gives 150
tokens a day, `recraft` 30 credits a day, and `suno` 50 credits a day, which is 10 songs.

**Where the sum breaks.** The 1,841 hours are five models at five prices, and an hour of
Nova-3 is not an hour of Reverb. `deepgram` gives the largest single allowance at 775 hours.
`assemblyai` is the cheapest per unit of currency at 333 / 50 = 6.7 hours per USD, against
`gladia` at 312 / 50 = 6.2 hours per EUR. The generators break the sum differently: `recraft`
owns free-plan images, `suno` excludes commercial rights, and `kling-ai` reports a forced
watermark. A dataset built on those terms is not the reader's.

### Accelerators: 100 core-hours, and no card-hours at all

Sixteen records. Five carry a free lane with a caveat, two are clocked trials, five fail at
identity, three are dead and one is paid-only software.

The only quantified reachable allowance is `arm-virtual-hardware`: 100 core-hours inside 30
days, 15 active cores, 25 device slots. 100 / 5 = 20 wall-clock hours on a five-core device,
and the trial shuts the virtual device down at day 30. Those are CPU core-hours on
instruction-accurate models, so they buy functional correctness and not throughput.

Six vendors give free silicon or free software with no published quantity. `qualcomm-ai-hub`
states it is 'currently completely free to use' and publishes no rate.
`tenstorrent-tt-console` offers browser inference on Tensix hardware and publishes no session
length, and `sima-ai-edgematic` is a free beta with no device-minute figure. `cann-points-mall`
quotes 100 CANN points per card-hour and never states how many points a task pays, so the rate
exists and the quantity does not. `axelera-ai-voyager` adds EUR 25 of assistant tokens, which
buys planning help and not accelerator time. `hailo-developer-zone` is the clearest case of a
free thing that cannot run: the compiler and model zoo are free, and the output executes only
on a module the developer owns.

**Where the sum breaks.** There is nothing to add. One hundred Arm core-hours and EUR 25 of
chat tokens are the whole reachable quantity, and zero card-hours of real accelerator time are
reachable from any of the sixteen. `k-cloud` shows the ceiling: 4 Rebellions ATOM+ cards,
free, inside a Korean government programme, to a selected demand company. `psc-neocortex`
shows the second shape: 2 Cerebras CS-3 nodes, free to non-proprietary research, to a
principal investigator at a US institution.

## The gate: what each vendor asks for, in its own words

Grouped by the term that has to be met before the offer exists. Counts are the dossier's
`identity_cost` field, narrowed by reading the detail.

| Gate | Records | Largest balance behind it | The sentence that decides it |
| --- | --- | --- | --- |
| no account at all | 4 | none | all four vendors are dead |
| an email address | 35 | USD 400, on a form that also asks a company name | `clickhouse-cloud`: 'no credit card required' |
| a work or business address | 2 of the 35 | USD 400 | `anyscale`: 'Use work email for' USD 100 'free credits' |
| a card | 8 | none published | `google-cloud-text-to-speech`: 'You must enable billing' |
| a mainland phone number | 3 | CNY 14 | `siliconflow`: real-name verification unlocks the second voucher |
| a company | 10 | up to USD 100,000 | `elevenlabs-startup-grants`: 'Only applications with valid business emails will be considered' |
| a fundraise | 2 of the 10 | up to USD 100,000 | `deepinfra-deepstart`: 'Have raised between 250K and 10M USD' |
| a university or a government | 3 | USD 50,000 | `psc-neocortex`: 'Applicants must be a researcher or educator at a US academic or non-profit research institution' |
| a sales conversation | 2 | none published | `hume-ai`: 'The API is currently in limited release; contact our team to request access' |

The distribution answers the question. Thirty-five of sixty-five records want nothing more
than an address, and every reachable balance sits inside that group. Every balance at or above
USD 500 sits among the other thirty.

**The claim under test.** AI credits in this period are mostly a
company benefit. The records support it, with one qualification that changes what to chase.

Supported: no record offers a balance between USD 300 and USD 500 without either a card or a
company field. Every balance at or above USD 500 is attached to a company, a university, a
government programme or a named venture fund: `cerebras-inference-research` at 50,000,
`nvidia-dgx-cloud` and `deepgram-startup-program` at 100,000, `gmi-cloud-scale` at 8,000
before partner credits, `deepinfra-deepstart` at 3,000 to 9,000, and
`elevenlabs-startup-grants` at a vendor-valued 5,500. The gap between 300 and 500 is where the
personal lane ends and the corporate lane starts.

The funding gate is the tightest and least visible. `deepinfra-deepstart` wants a company
founded within two years that has raised between USD 250,000 and USD 10,000,000, which
excludes a bootstrapped developer and a later-stage company alike. `nvidia-dgx-cloud` wants a
portfolio company of Accel, Elaia, Partech or Sofinnova.

Qualified: the gated money is not where the useful capacity is. The two largest recurring
allowances are card-gated rather than company-gated, and a card is a personal instrument.
`amazon-polly` at 115 hours a month and `google-cloud-text-to-speech` at 66 hours a month are
worth more per year than a 12-month character grant a committee must approve, and neither asks
for a company. Six of the nine data records are perpetual and email-only. So the accurate
statement is narrower: currency-denominated AI credits are a company
benefit, and recurring product allowances are not.

## What the class does not give

**Expiry horizons are short and they bind first.** Five records run on a 30-day clock:
`clickhouse-cloud`, `snowflake`, `tiger-cloud`, `arm-virtual-hardware` and `moore-threads-ai`.
`clickhouse-cloud` states it plainly: 'The trial ends after 30 days or once the credits are
consumed, whichever comes first'. Four wallets run 12 months: `gladia`, `deepinfra-deepstart`,
`deepgram-startup-program` and `elevenlabs-startup-grants`. `cartesia` caps rollover at twice
the monthly rate, `elevenlabs` states that 'Rollover does not apply to the Free plan', and
`suno` states that credits 'do not carry over from day to day or month to month'.
`genesis-cloud` and `sima-ai-edgematic` sit on a clock with no published amount or end date.

**Rate limits arrive before balances.** `assemblyai` caps streaming at 5 new connections a
minute against 100 on the paid tier, so a live capture cannot use its USD 50. `deepgram` caps
REST at 50 and WebSocket at 150 connections, so a batch waits on slots while USD 200 sits
unspent. `influxdb-cloud-serverless` caps ingest at 5 MB per 5 minutes, so a backfill fails
although the plan has no volume cap. `cartesia` allows 2 concurrent TTS requests, and
`featherless-ai` allows 4 concurrent units with no API traffic on its cheapest plan.

**Model exclusions decide the quality, not the quantity.** `google-cloud-text-to-speech`
prints 'Not available' in the free column for the Gemini-family voices, so the newest models
are excluded while 4 million characters a month are given away. `amazon-polly` keeps only
Standard permanent and dates Neural to 12 months. `leonardo-ai` locks the free plan to 'Auto
Only' models and Basic quality. `suno` pins the free plan to v6-mini, `kling-ai` reports 360p
to 540p with a watermark, and `recraft` keeps ownership of free-plan images. The free lane is
the previous model, and the current model is the paid lane.

**Region locks are quiet.** `neo4j-auradb` runs free instances in GCP us-central1 only.
`siliconflow` registers by mainland mobile number, and `cann-points-mall` redeems into a
Huawei Cloud account that needs real-name verification. `moore-threads-ai` admits 100
developers a day. `psc-neocortex` and `cerebras-inference-research` are US-academic. `k-cloud`
is a Korean legal entity. None of those sentences appears in a pricing table.

**Fourteen records describe a lane that closed or lost its self-serve door.** Dead outright:
`playht-playai` (the domain does not resolve), `lepton-ai`, `predibase`, `nvidia-launchpad`
(redirected), `degirum-ai-hub` (2026-09-30), `esperanto-technologies` and `untether-ai`
(bankrupt 2025-10-15). Closed lane, live company: `graphcore-ipu-cloud` ('Running code on IPUs
in Paperspace is no longer supported', and the free-trial page 404s), `hume-ai` (self-serve
withdrawn behind an access request), `upstage` (the free week ended 2026-08-11), `xai-grok-api`
(no credit on the live documentation index). `ideogram` is a twelfth by inference, since its
price list no longer carries a free row, and `cudo-compute` and `ori-global-cloud` are the last
two in a milder form: both still operate and neither has a self-serve door left.

`degirum-ai-hub` carries the most expensive lesson in the slice. Its documentation still
serves the free-plan table while the homepage states the service is discontinued, so a reader
who lands on the docs records a live free tier that ended 22 days before this reading.
`esperanto-technologies` is the same shape: the notice sits four lines below the product pitch.

## How this composes, and what would change the answer

Composition inside the slice is weak; composition across lanes is where the value is. One free
runner from the compute lane plus USD 200 at `deepgram` is a working transcription pipeline,
and `qualcomm-ai-hub` covers the compile loop while the Qualcomm Device Cloud record covers
the application, so model work and app work both happen without owning a phone.

Three measurements would move a verdict, and each is cheap:

- One `snowflake` signup with a personal address, to settle whether USD 400 is card-free and
  company-free. This is the one number whose group is a judgement.
- One `qualcomm-ai-hub` account or one `tenstorrent-tt-console` signup, to find the ceiling
  behind a lane that publishes no quota at all.
- One logged-in `kling-ai` credit read before and after a generation, plus one `recraft` plan
  table read with JavaScript enabled. Between them they settle two figures that half the web
  repeats and no official page confirms, and the second moves a `reported` rung upward.

The corpus-wide ceiling is not in this slice. `docs/compute/free/startup-credits.md` records up
to USD 200,000 from AWS Activate Portfolio and Databricks, so the USD 100,000 above is the
ceiling among these sixty-five records and not the ceiling of the catalogue.
