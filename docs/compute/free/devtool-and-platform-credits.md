# Developer credits, platform hosts and prizes

This document covers 124 records that do not form one class: twenty-five developer tools and
agent platforms, nineteen application hosts, eighteen competitions, twenty regional
programmes, seventeen decentralized networks and twenty-five open-source sponsorships. The
question is which of them hands a person with no company, no institution and no card
something usable tonight, and which pay in cash or visibility instead of capacity.

The lanes open without an application add to 12 CPU-hours a month, 1,000,000 agent tokens a
month, 15 agent tasks a day and one anonymous queue. The slice advertises USD 14,845,000 in
prize pools, which belongs in another column, and publishes no GPU-hour a new account can
claim.

## The short answer

Four lanes are reachable. Three give capacity and one gives money.

| Lane | Records | What is reachable | Largest single number | What fails first |
| --- | --- | --- | --- | --- |
| Host accounts | 19 | a monthly allowance that renews while the account exists | 360 GB-hours of memory a month (Vercel) | the memory meter, before the CPU meter |
| Agent tools | 25 | a token or task quota on a vendor's model | 1,000,000 tokens a month (Bolt) | the 300,000 daily token cap |
| Decentralized networks | 17 | a queue on volunteer GPUs | 51 workers over 28 text models, measured 2026-10-22 | anonymous calls sit at the lowest priority |
| Prizes and competitions | 18 | money, after a leaderboard | USD 10,000,000 (AIMO fund) | the modal payout is zero |

⭐ **The reachable total, with the addition shown.** Vercel publishes 4 hours of Active CPU
a month and Azion publishes 8 hours of compute a month, so the host lane is 12 CPU-hours.
Bolt publishes 1,000,000 tokens and Jules publishes 15 tasks a day, and a task does not
publish its token cost, so those stay two numbers. AI Horde publishes no quota, only a
queue. The storage does not add up either: Firebase 10 GB, Sevalla 100 sites of 1 GB,
Encore 1 GB of database and 1 GB of object storage, Suga 1 GB of disk are four vendors with
no shared meter.

⚠ **The number that decides the class is zero.** Seventeen records describe a decentralized
GPU network, and not one publishes a GPU-hour a new account can claim: ten charge per token,
per hour or per stake, two pay in test currency, four give a queue or a request allowance
rather than compute, and one publishes a USD 100 credit at an unstated rate.

## The whole slice, in six tables

Every record appears once, sorted from the strongest verdict to the weakest: `qualifies`,
`qualifies-with-caveat`, `trial-only`, `fails-quota`, `fails-identity`, `paid-only`, `dead`.
`perpetual` means no renewal clock is stated, and the identity column names the gate that
binds, which is not always `identity_cost.kind`.

### Developer tools and agent platforms (14 free, 3 trials, 6 paid, 2 dead)

| Provider | What is given | Unit | Cadence | Identity gate | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `bolt` Bolt | 1,000,000 AI tokens, 300,000 a day, web requests, hosting | tokens | monthly, daily cap | email | the 300,000 daily cap, which does not carry over | qualifies |
| `jules` Jules | 15 tasks a day, 3 concurrent, Gemini 2.5 Pro | tasks | rolling 24 h | email | the window stops new work | qualifies |
| `amazon-q-developer` Amazon Q Developer | 50 agentic requests and 1,000 transformed lines | requests | monthly | email | 50 requests is about two a working day | qualifies-with-caveat |
| `codesandbox` CodeSandbox | 400 credits, 40 hours a month on a Nano VM, 20 sandboxes | credits | monthly | email | the pool freezes every VM in the workspace | qualifies-with-caveat |
| `devin-including` Devin | a light agent quota and unlimited inline edits | quota not published | not stated | email | a quota message with no number in it | qualifies-with-caveat |
| `jetbrains-ai` JetBrains AI | unlimited completion and 3 credits | credits | monthly | email | 3 credits buys little agent work | qualifies-with-caveat |
| `kilo-code` Kilo Code | a free individual platform, a supplied key or free models | none | perpetual | email | whichever free model serves that hour | qualifies-with-caveat |
| `lovable` Lovable | 30 build credits, 5 a day for the first six days | credits | monthly | email | day six, then nothing until the month turns | qualifies-with-caveat |
| `manus` Manus | 300 credits a day, capped at 1,500 a month | credits | daily and monthly | email | the 1,500 monthly cap on day five | qualifies-with-caveat |
| `v0` v0 | 7 messages a day, deploys to Vercel | messages | daily | email | 7 messages, so a second attempt is often the last | qualifies-with-caveat |
| `warp` Warp | agent CLI and limited cloud agents, inference from a key the reader supplies | none | perpetual | email | no Warp inference is included | qualifies-with-caveat |
| `anything` Anything | 3,000 credits, public projects only | credits | one-time | email | credits are consumed and not refilled | trial-only |
| `emergent` Emergent | 10 credits on day one; publishing needs 50 | credits | one-time | email | day two has no credits at all | trial-only |
| `qodo` Qodo | 14 days, then zero | days | trial | email | day 15, and the capacity vanishes rather than shrinks | trial-only |
| `augment-code` Augment Code | nothing: USD 20 a month including USD 20 of usage | USD | monthly | card | a 40 percent fee on all inference | paid-only |
| `blackbox-ai` Blackbox AI | nothing: token spend committed once | USD | contract | card | a contract before any capacity | paid-only |
| `factory` Factory | nothing: paid plans start at USD 20 a month | USD | monthly | card | the first paid tier, with rolling limits unquantified | paid-only |
| `tabnine` Tabnine | nothing at a self-serve price | none | sales only | institution | a sales form, after the Tricentis acquisition | paid-only |
| `venice-ai` Venice AI | nothing on the API: every call is metered | USD per token | metered | card | the balance, which starts at zero | paid-only |
| `sourcegraph-cody` Sourcegraph Cody | nothing: Cody Free and Pro withdrawn 2025-07-23 | none | closed | institution | no signup route for an individual | dead |
| `goose` Goose (self-hosted) | an open-source agent for a key the reader supplies | none: no vendor inference | perpetual | anonymous | the endpoint key and its bill | qualifies-with-caveat |
| `zed` Zed (self-hosted) | the editor and agent, unlimited with a key the reader supplies | none | perpetual | anonymous | the endpoint and its key | qualifies-with-caveat |
| `onlook` Onlook (self-hosted) | a desktop download; hosted use is a sales call | none | perpetual | anonymous | no self-serve hosted lane exists | paid-only |
| `amp-2` Amp (self-hosted) | the agent and its tokens; unlimited self-hosted orbs | none: no vendor inference | perpetual | email | the model bill moves to a key of the reader's own | qualifies-with-caveat |
| `continue` Continue (self-hosted) | nothing: acquired by Cursor | none | closed | institution | the product is gone | dead |

### Platform hosts (8 free, 5 trials, 3 bring-your-own-cloud, 1 fails-quota, 2 dead)

| Provider | What is given | Unit | Cadence | Identity gate | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `alibaba-cloud-esa` Alibaba Cloud ESA | 100,000 edge requests a day per plan, 5 plans per account | requests/day | perpetual | email | 100,000 a day, or 500,000 across five plans | qualifies-with-caveat |
| `azion` Azion | 8 compute-hours, 3,000,000 requests, 1 TB transfer, 10 workloads | hours | monthly | email | 8 hours at the 2 s CPU cap is 14,400 full invocations | qualifies-with-caveat |
| `encore-cloud` Encore Cloud | 2 dev environments, 1 GB database, 1 GB object storage | requests/day | perpetual | email | 100,000 requests a day, about 1.16 a second | qualifies-with-caveat |
| `firebase-hosting` Firebase Hosting | 10 GB storage, 10 GB transfer, 2 GB per file | GB | monthly | email | 10 GB of transfer, which one serve can spend | qualifies-with-caveat |
| `netlify` Netlify | 300 credits: 30 GB-hours, or 15 GB, or 20 deploys | credits | monthly | email | one pool across four products, with no recharge | qualifies-with-caveat |
| `sevalla` Sevalla | 100 static sites of 1 GB, 100 GB transfer, 600 build minutes | GB | perpetual | email | the 1 GB per-site cap | qualifies-with-caveat |
| `suga` Suga | 1 project, 0.1 vCPU, 256 MiB RAM, 1 GB disk, 1-day logs | GiB | perpetual | email | the machine shape and the one-project count | qualifies-with-caveat |
| `vercel` Vercel | 4 CPU-hours, 360 GB-hours memory, 1,000,000 invocations, 100 GB | hours | monthly | email | the memory meter: 2 GB held for 180 hours spends it | qualifies-with-caveat |
| `amazon-web-services-free-tier` AWS Free Tier | up to USD 200 in credits over six months | USD | 6 months | card | the account closes at month six | trial-only |
| `aws-amplify-hosting` AWS Amplify Hosting | 1,000 build minutes on 4 vCPU, 5 GB storage, 15 GB transfer | mixed | 12 months | card | month twelve, when every line is metered | trial-only |
| `scalingo` Scalingo | 30 days, then billing by the minute | days | trial | card | day 31, and containers never sleep | trial-only |
| `upsun` Upsun | 15 days, then a credit covering the platform fee and the seat | days | trial | email | the first provisioned CPU-hour at EUR 0.033 | trial-only |
| `zerops` Zerops | 15 build hours, 5 GB backup, 100 GB egress, USD 15 of credit | hours | one-time credit | email | the USD 15, which the vendor prices at three to five months | trial-only |
| `codesphere` Codesphere | 5 commits a month, and no vCPU, memory or storage figure | commits | monthly | email | the sixth commit, on a plan whose shape is unpublished | fails-quota |
| `flightcontrol` Flightcontrol | the control plane only; the app runs in an AWS account of the reader's own | none | perpetual | card | the AWS bill, which starts at the first deployment | paid-only |
| `qovery` Qovery | nothing: USD 299 a month after a 14-day trial | none | trial 14 d | card | the platform floor, plus the cloud invoice | paid-only |
| `sst` SST | the Console to 350 active resources; the app runs in an AWS account of the reader's own | none | perpetual | card | the AWS account behind the Console | paid-only |
| `adaptable` Adaptable | nothing: the free plan ended 2024-09-23, the company shut down | none | closed | email | every path answers HTTP 530 | dead |
| `cyclic` Cyclic | nothing: usage ended 2024-05-31 | none | closed | email | the live page still advertises a Free Forever tier | dead |

### Competitions, prizes and benchmark programmes (7 open, 8 event prizes, 3 gated)

| Provider | What is given | Unit | Cadence | Identity gate | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `aicrowd` AIcrowd | USD 100 of sponsor credits after beating a published baseline | USD | per track | email | a 7 to 14 day verification, then first come | qualifies-with-caveat |
| `aimo-prize` AIMO Prize | USD 10,000,000 fund, USD 5,000,000 grand, H100 notebooks | USD | contest rounds | email | a 5-hour GPU notebook with the internet disabled | qualifies-with-caveat |
| `arc-prize-foundation` ARC Prize | USD 2,000,000 across three tracks | USD | milestones in 2026 | email | releasing the solution is a condition of payment | qualifies-with-caveat |
| `kaggle-benchmarks` Kaggle Benchmarks | a high compute quota and model access to benchmark hosts | not published | rolling | email | the quota pays for evaluations, not for training | qualifies-with-caveat |
| `thiel-fellowship` Thiel Fellowship | USD 250,000 over two years, no entity required | USD | cohort | email | an age and enrolment condition, before any project | qualifies-with-caveat |
| `vesuvius-challenge` Vesuvius Challenge | USD 2,140,000 open pool, USD 800,000 grand prize | USD | open until claimed | email | the science, and the entrant funds the GPU time | qualifies-with-caveat |
| `zindi` Zindi | USD 4,500 first of a USD 10,000 pool, plus 10,000 points | USD | per challenge | email | a pool split across several hundred entrants | qualifies-with-caveat |
| `aws-trainium-frontier` AWS Trainium Frontier | one Trainium2 chip for 30 minutes; the top ten get 4 hours | chip-hours | 2026 cycle, closed | email | registration closed 2026-09-30 | trial-only |
| `digitalocean-gradient-ai` DigitalOcean Gradient AI | USD 8,000 first prize, USD 600 credits, USD 200 on signup | USD | one event | email | one winner among 2,592 entrants | trial-only |
| `global-ai-hackathon` Global AI Hackathon | Qwen credits, and USD 70,000 or more in cash and credits | USD | one event | email | a per-track token budget, spent in hours | trial-only |
| `icml-2026-agent` ICML 2026 Agent | USD 4,000 in GPU credits: 2,000, 1,000 and two of 500 | USD | one cycle | email | the onboarding credit was exhausted within days | trial-only |
| `inference-time-compute-hackathon` Inference-Time Compute | 8 H100s for 24 hours, USD 100 credits, USD 50,000 top prize | H100-hours | one event | email | the clock, which makes 192 H100-hours per team | trial-only |
| `microsoft-agents-academy` Microsoft Agents Academy | USD 12,000 of Store gift cards across the tracks | USD | one cycle | email | store credit cannot buy compute | trial-only |
| `test-flight` Test Flight | USD 300,000 in compute credits to the winner | USD | event, 2026 closed | email | in-person Boston; 2026 closed 2026-09-19 | trial-only |
| `zoltan-s-flops-gpu` Zoltan's FLOPs GPU | USD 5,000 split across one to five projects | USD | closed | email | applications closed 2025-04-15 | trial-only |
| `amazon-alexa-prize` Amazon Alexa Prize | USD 250,000 grant, devices and AWS cloud per team | USD | cohort | institution | one accredited university per team | fails-identity |
| `drivendata-doe` DrivenData / DOE | USD 300,000 pool, USD 100,000 first prize | USD | closes 2026-12-03 | country-phone | US citizenship or permanent residency | fails-identity |
| `mlperf` MLPerf | no compute at all; the submitter supplies the system | none | not stated | institution | working-group membership, before hardware | fails-identity |

### Regional and national programmes (5 above fails-identity, 14 gated, 1 offline)

| Provider | What is given | Unit | Cadence | Identity gate | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `european-innovation-council` European Innovation Council | EUR 2,499,999 grant maximum, plus equity of EUR 500,000 to 10,000,000 | EUR | 2026 work programme | institution | an SME in a member or associated country | qualifies-with-caveat |
| `itida-startit` ITIDA StartIT | EGP 480,000 fund, USD 10,000 AWS, one year of incubation | EGP | cohort | email | a working prototype and delivery in Egypt | qualifies-with-caveat |
| `start-up-chile` Start-Up Chile | CLP 15,000,000, 30,000,000 or 75,000,000, equity-free | CLP | cohort | email, then a Chilean entity | two of the three tiers need a Chilean entity | qualifies-with-caveat |
| `the-catalyst` The Catalyst | ten weeks in Riyadh, no equity, 200 consulting hours | SAR | cohort, closes 2026-11-05 | email | ten weeks in person, and 15 places | qualifies-with-caveat |
| `true-digital-park` True Digital Park | THB 100,000 package with USD 25,000 of Google Cloud credit | THB | not stated | card | a Thai company, 25 percent share, THB 600,000 saved | qualifies-with-caveat |
| `ai-singapore` AI Singapore | SGD 150,000 co-funding and a six-month engineering team | SGD | cohort | institution | a Singapore entity with cash to match | fails-identity |
| `alfred-p-sloan` Alfred P. Sloan | USD 60,000 or less, for books, to individuals | USD | rolling, books only | institution | no unsolicited proposal is read at all | fails-identity |
| `bndes-garagem` BNDES Garagem | BRL 915,000 in prizes across ten winners | BRL | annual | institution | a Brazilian operation | fails-identity |
| `bpifrance` Bpifrance | EUR 30,000 maximum, at 50 to 70 percent of cost | EUR | not stated | institution | a French entity under one year old | fails-identity |
| `cdti-neotec-2026` CDTI Neotec 2026 | EUR 250,000 at 70 percent; EUR 325,000 with a doctorate hire | EUR | annual call | institution | a Spanish company under three years | fails-identity |
| `enterprise` Enterprise Estonia | EUR 20,000 start-up grant (closed); up to EUR 2,000,000 research | EUR | rounds | institution | an Estonian company with substance in Estonia | fails-identity |
| `enterprise-compute-initiative` Enterprise Compute Initiative | SGD 350,000 of AWS, SGD 250,000 of Azure or Oracle | SGD | programme | institution | 10 staff in Singapore, plus a tech team of two | fails-identity |
| `hub71` Hub71 | at most AED 750,000: in-kind, cash for equity, top-up | AED | programme | institution | an ADGM licence and long-term relocation | fails-identity |
| `indiaai-compute-portal` IndiaAI Compute Portal | 40 percent subsidy on about INR 65 per GPU-hour | INR | portal | institution | an institute email, plus an APAAR or DPIIT number | fails-identity |
| `malaysia-digital-acceleration` Malaysia Digital Acceleration | MYR 2,000,000, performance-based | MYR | closed 2025-07-18 | institution | Malaysian incorporation plus MD status | fails-identity |
| `national-ai-innovation` National AI Innovation | compute credits; no amount published | not published | challenge | national-id | Nigerian citizenship, checked first | fails-identity |
| `startup-india-seed` Startup India Seed Fund | INR 2,000,000 (20 lakh) grant and INR 5,000,000 convertible | INR | incubator rounds | institution | DPIIT recognition, incorporated under two years | fails-identity |
| `startup-sg-tech` Startup SG Tech | SGD 400,000 proof of concept, SGD 800,000 proof of value | SGD | call | institution | 30 percent local equity, before the project | fails-identity |
| `technology-innovation-agency` Technology Innovation Agency | ZAR 50,000 to 650,000; up to ZAR 1,200,000 | ZAR | regional calls | institution | a university or accredited incubator must apply | fails-identity |
| `fast-grants` Fast Grants | nothing: the domain returns a 404 deployment error | none | closed | institution | the programme is offline | dead |

### Decentralized networks (5 free lanes, 2 testnets, 10 paid)

| Provider | What is given | Unit | Cadence | Identity gate | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `ai-horde` AI Horde | anonymous text and image generation on volunteer GPUs | none published | continuous | anonymous | anonymous calls sit at the lowest priority | qualifies-with-caveat |
| `inference-net` Inference.net | 1,000,000 gateway requests, 30 a minute, one seat | requests | monthly | email | model tokens are billed; routing is the allowance | qualifies-with-caveat |
| `livepeer-studio` Livepeer Studio | 1,000 transcoding minutes, 5,000 delivery minutes, 30 viewers | minutes | monthly | email | the transcoding minutes and the viewer cap | qualifies-with-caveat |
| `netmind` NetMind | USD 100 of credit; up to USD 100,000 for startups, `reported` | USD | signup credit | email | USD 100 at a rate the record does not state | qualifies-with-caveat |
| `nineteen-ai` Nineteen AI | Llama 3.1 8B at less than USD 0.00 per million tokens | tokens | while the subsidy lasts | email | an undocumented per-key limit, then the subsidy | qualifies-with-caveat |
| `iexec` iExec | 5 RLC per claim on a testnet, 24-hour cooldown | RLC | daily | email | test currency only, and 5 RLC a day | fails-quota |
| `ritual` Ritual | 5 RITUAL per access code on a testnet | RITUAL | faucet | email | no mainnet capacity exists to buy at any price | fails-quota |
| `bittensor` Bittensor | nothing free: a subnet slot cost 605.7 TAO on 2026-10-22 | TAO | chain time | card | capital, before identity | paid-only |
| `cudo-compute` Cudo Compute | nothing: every accelerator reads quote on request | none | sales | institution | there is no self-serve purchase at all | paid-only |
| `fluence` Fluence | nothing free; a 2 vCPU, 2 GB VM from USD 2.54 a month | USD | metered | email | the first paid VM | paid-only |
| `golem-network` Golem Network | tGLM test tokens the documentation says have no value | GLM | metered | card | a GLM purchase on mainnet, plus gas | paid-only |
| `marlin` Marlin | nothing: integration contracts for other protocols | none | sales | institution | there is no individual on-ramp | paid-only |
| `morpheus` Morpheus | nothing free: per token, or a stake of MOR | MOR | metered | card | MOR has to be bought on an exchange first | paid-only |
| `near-ai-cloud` NEAR AI Cloud | nothing free: every token is billed, from USD 0.04 per 1,000,000 | USD per token | metered | email | the account balance | paid-only |
| `phala-cloud` Phala Cloud | nothing free: a confidential VM from USD 0.06 an hour | USD | metered | card | a card before the first deploy | paid-only |
| `spheron` Spheron | nothing free: a deposit of USD 15 to USD 5,000 per transaction | USD | metered | card | the deposit, before any identity check | paid-only |
| `expanso` Expanso (self-hosted) | software for nodes the customer operates | none | perpetual | institution | it supplies no capacity of its own | paid-only |

### Open-source sponsorships and stipends (19 open, 5 gated, 1 closed)

| Provider | What is given | Unit | Cadence | Identity gate | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `aws-cloud-credits` AWS Cloud Credits | promotional credits; the amount is not published | USD | monthly review | card | an active paid AWS account, and no credits in December | qualifies-with-caveat |
| `cloudflare-project-alexandria` Cloudflare Project Alexandria | recurring annual credits; no amount, cap or deadline published | USD | annual | card | a payment method on file before any credit | qualifies-with-caveat |
| `filecoin-foundation-next` Filecoin Foundation Next | USD 5,000 paid in FIL | USD | every two weeks | email | a working prototype and a tax form | qualifies-with-caveat |
| `github-secure-open` GitHub Secure Open | USD 10,000 per project, plus USD 10,000 of Azure credits | USD | annual cohort | email | two security check-ins across twelve months | qualifies-with-caveat |
| `github-sponsors` GitHub Sponsors | whatever a sponsor chooses; no fee from personal accounts | USD | continuous | email | a sponsor has to exist | qualifies-with-caveat |
| `google-open-source` Google Open Source | USD 500 to USD 15,000 per patch, by tier | USD | per accepted patch | email | a merged patch comes before any payment | qualifies-with-caveat |
| `google-summer` Google Summer of Code | USD 750 to USD 6,600 per project, by size and location | USD | annual | email | a mentor organisation must select the proposal | qualifies-with-caveat |
| `heroku-open-source` Heroku Open Source | twelve monthly credit allocations; the amount is not published | USD | monthly, 12 months | card | a card before applying | qualifies-with-caveat |
| `hugging-face-community` Hugging Face Community | the hardware tier of one Space | hours, not published | on request | email | discretionary, and bound to one Space | qualifies-with-caveat |
| `lfx-mentorship` LFX Mentorship | USD 1,000 to USD 6,600, set by country | USD | cohort | email | about one accepted applicant in ten | qualifies-with-caveat |
| `mozilla-foundation-human-scale` Mozilla Human-Scale | USD 300,000, up to USD 500,000 across three years | USD | cohort, April 2027 | email | a competitive shortlist | qualifies-with-caveat |
| `mozilla-open-source` Mozilla MOSS | USD 5,000 to USD 150,000, average USD 70,000 | USD | rolling, monthly | email | the project must already matter in its ecosystem | qualifies-with-caveat |
| `netlify-open-source` Netlify Open Source | 10,000 credits a month, and sites stay up when they run out | credits | monthly | email | a review, plus a visible badge on the site | qualifies-with-caveat |
| `open-technology-fund` Open Technology Fund | USD 10,000 to USD 900,000, contracted with the applicant | USD | rolling | email | a two-stage written application | qualifies-with-caveat |
| `openai-codex` OpenAI Codex | API credits and six months of ChatGPT Pro | USD, not published | on review | email | a review, and core-maintainer status | qualifies-with-caveat |
| `outreachy` Outreachy | USD 7,000 for a three-month internship | USD | two windows a year | email | a contribution period, then selection | qualifies-with-caveat |
| `sentry` Sentry | a sponsorship plan: 5,000,000 errors, 5,000 GB of logs, no term limit | events | no term limit | email | a sponsorship review | qualifies-with-caveat |
| `sovereign-tech-fellowship` Sovereign Tech Fellowship | EUR 64,000 to EUR 82,000 a year, or freelance at 6 to 32 hours | EUR | 2026 cohort, closed | email | the intake is closed | qualifies-with-caveat |
| `sovereign-tech-fund` Sovereign Tech Fund | project work whose cost exceeds EUR 50,000 | EUR | rolling | email | a panel review, and the EUR 50,000 floor | qualifies-with-caveat |
| `datadog` Datadog | a free plan with qualitative limits | not published | by application | institution | one year old, five contributors, two employers | fails-identity |
| `digital-catapult` Digital Catapult | USD 25,000 AWS, up to USD 100,000 Google, EUR 10,000 OVHcloud | USD and EUR | 14-week cohort | institution | a UK registered company | fails-identity |
| `microsoft-azure-credits` Microsoft Azure credits | nothing: the application form is closed | USD | closed | institution | no application route exists | fails-identity |
| `numfocus-small-development` NumFOCUS Small Development | USD 10,000 per proposal | USD | cycle | institution | an already affiliated project | fails-identity |
| `openssf-alpha-omega` OpenSSF Alpha-Omega | a share of a budget stated as over USD 7,000,000 a year | USD | by engagement | institution | a named foundation to hold the contract | fails-identity |
| `mozilla-builders-accelerator` Mozilla Builders | up to USD 100,000; the last round closed 2024-08-01 | USD | closed | email | no round has been published since 2024 | dead |

## What each sub-class is worth

### Hosts: 12 CPU-hours a month, in a pool that does not recharge

The host lane is the only one where an email signup holds a running service permanently.
`vercel.com/docs/pricing` (read 2026-10-22) gives Hobby 4 hours of Active CPU and 360
GB-hours of provisioned memory a month. `azion.com/en/pricing/` (read 2026-10-22) gives 8
hours of compute and 3,000,000 requests, with each invocation capped at 2 s of CPU. Four
plus eight is 12 CPU-hours.

What breaks it is the accounting. Netlify's single 300-credit pool ends at 15 GB of
bandwidth. Vercel's memory meter binds before its CPU meter: a function held at the 2 GB
Hobby ceiling spends 360 GB-hours in 180 hours. Azion's 8 hours vanish at 14,400 full
invocations.

### Agent tools: 1,000,000 tokens a month, and five clients that serve no model

Fourteen records carry a free lane in five units. Bolt publishes 1,000,000 tokens a month
with a 300,000 daily cap; Jules publishes 15 tasks a day on a rolling window. A task
publishes no token cost, so the two do not add.

⚠ Five (Amp, Goose, Kilo Code, Warp, Zed) serve no model, so their free tier is a client and
the capacity is the user's key. Manus caps 300 credits a day at 1,500 a month, so day five
ends the month; Lovable's 30 credits end on day six.

### Competitions: USD 14,845,000 advertised, and 192 H100-hours on a clock

The pools an individual can enter sum to USD 14,845,000: AIMO 10,000,000, ARC 2,000,000,
Vesuvius 2,140,000, DrivenData 300,000, Thiel 250,000, Inference-Time 100,000, Trainium
25,000, DigitalOcean 20,000, Zindi 10,000.

USD 300,000 of it is closed by nationality, and USD 25,000 by a cycle that has ended. The
modal payout against the rest is zero. The compute is 8 H100s for 24 hours, which is 192
H100-hours per team, once. Everything larger is a prize.

### Regional: twenty gates, and no dollars without an entity

Five of twenty carry a verdict above `fails-identity` and none pays without a presence cost.
The European Innovation Council is the largest at EUR 2,499,999 and needs an SME in a
member or associated country; Enterprise Compute reaches SGD 350,000 and needs 10 staff
based in Singapore.

Start-Up Chile publishes `WE ARE AGNOSTIC TO NATIONALITIES` and still needs a Chilean entity
for two of three tiers. The gate is quoted in the records: IndiaAI requires an `institute /
organization email address`, and Startup SG Tech requires `at least 30% local equity held
directly or indirectly by Singaporean(s) and/or Singapore PR(s)`.

### Decentralized: seventeen records, no GPU-hour to claim

Five give a usable lane and two give test currency. AI Horde serves volunteer GPUs with the
key `0000000000` and `No need to register`; 51 workers over 28 text models were measured on
2026-10-22, so the queue binds. Livepeer gives 1,000 transcoding minutes a month, and
Inference.net bills every model token.

The faucets say what they are: iExec pays 5 RLC a day on a testnet, and Golem's tGLM `have
no real value`. Paid capacity is cheap: Fluence at USD 2.54 a month for 2 vCPU, Phala at
USD 0.06 an hour.

### Open-source: the largest cheque open to a person is a contract

Nineteen of twenty-five do not require an organisation. The largest is the Open Technology
Fund at USD 900,000: `Funding awards are performance-based contracts signed directly with
the applicant or applicants.`

Behind it the lane is per-project sums. Mozilla MOSS pays USD 5,000 to USD 150,000 with a
USD 70,000 average and excludes new projects. Summer of Code pays USD 750 to USD 6,600,
Outreachy USD 7,000, and Google USD 500 to USD 15,000 a security patch. Microsoft's Azure
form is not open.

## Cash and compute are different columns

A fellowship is money and a GPU-hour allocation is capacity. They expire differently, and a
table that adds them produces a number true of nothing.

| Group | Largest cash figure | Largest capacity figure | Same quantity |
| --- | --- | --- | --- |
| Competitions and prizes | USD 10,000,000 (AIMO fund) | 192 H100-hours at one event | no |
| Regional programmes | EUR 2,499,999 (EIC grant) | none without an entity | no |
| Open-source sponsorship | USD 900,000 (OTF ceiling) | USD 10,000 of Azure credits | no |
| Hosts | none | 360 GB-hours of memory a month | not applicable |
| Agent tools | none | 1,000,000 tokens a month | not applicable |
| Decentralized networks | none | USD 100 of credit, rate unpublished | not applicable |

Money buys capacity only after it arrives: Mozilla Human-Scale pays USD 300,000 for support
beginning April 2027, and the Sovereign Tech Fellowship pays EUR 64,000 to EUR 82,000 a year
to up to twelve people. Neither puts a machine in front of a reader this month.

A prize is not a grant, because Vesuvius pays an entrant who already spent the compute and
ARC makes an open-source release a condition of payment. A credit is money with an expiry and
a merchant: AWS's USD 200 closes the account at month six, while Vercel's 4 CPU-hours renew.

## The same programmes outside the United States

The entity requirement decides the answer, so it has its own column.

| Country or region | Programme | What it gives | Entity requirement | Verdict |
| --- | --- | --- | --- | --- |
| Brazil | `bndes-garagem` BNDES Garagem | BRL 915,000 in prizes, 100 businesses a year | a Brazilian operation | fails-identity |
| Chile | `start-up-chile` Start-Up Chile | CLP 15,000,000 to 75,000,000, equity-free | a Chilean entity for two of three tiers | qualifies-with-caveat |
| Egypt | `itida-startit` ITIDA StartIT | EGP 480,000, USD 10,000 AWS, one year | email, but the pitch is in person in Egypt | qualifies-with-caveat |
| Estonia | `enterprise` Enterprise Estonia | EUR 20,000 (closed) to EUR 2,000,000 | an Estonian company with substance in Estonia | fails-identity |
| European Union | `european-innovation-council` EIC | EUR 2,499,999 grant plus equity | an SME in a member or associated country | qualifies-with-caveat |
| France | `bpifrance` Bpifrance | EUR 30,000 at 50 to 70 percent of cost | a French entity under one year, or an incubator | fails-identity |
| India | `indiaai-compute-portal` IndiaAI Compute Portal | 40 percent off about INR 65 per GPU-hour | an institute email plus APAAR or DPIIT | fails-identity |
| India | `startup-india-seed` Startup India Seed Fund | INR 2,000,000 grant, INR 5,000,000 convertible | DPIIT recognition and an Indian company | fails-identity |
| Malaysia | `malaysia-digital-acceleration` Malaysia Digital | MYR 2,000,000, performance-based | Malaysian incorporation and MD status | fails-identity |
| Nigeria | `national-ai-innovation` National AI Innovation | compute credits, amount unpublished | Nigerian citizenship | fails-identity |
| Saudi Arabia | `the-catalyst` The Catalyst | ten weeks, no equity; SAR 150,000 in the GAIA track | an AI-native startup able to be in Riyadh | qualifies-with-caveat |
| Singapore | `ai-singapore` AI Singapore | SGD 150,000 co-funding over six months | a Singapore organisation with cash to match | fails-identity |
| Singapore | `enterprise-compute-initiative` ECI | SGD 350,000 of AWS credits | 10 staff in Singapore and a tech team of two | fails-identity |
| Singapore | `startup-sg-tech` Startup SG Tech | SGD 400,000 or SGD 800,000 | Singapore registration and 30 percent local equity | fails-identity |
| South Africa | `technology-innovation-agency` TIA | ZAR 50,000 to 650,000, up to ZAR 1,200,000 | a university or accredited incubator applies | fails-identity |
| Spain | `cdti-neotec-2026` CDTI Neotec | EUR 250,000 at 70 percent, EUR 325,000 with a hire | a Spanish company under three years | fails-identity |
| Thailand | `true-digital-park` True Digital Park | THB 100,000 package with USD 25,000 of Google Cloud | a Thai company, 25 percent share, THB 600,000 saved | qualifies-with-caveat |
| United Arab Emirates | `hub71` Hub71 | up to AED 750,000, partly for equity | an ADGM licence and long-term relocation | fails-identity |
| United States | `alfred-p-sloan` Alfred P. Sloan | USD 60,000 or less, books only | none for books; no unsolicited proposals otherwise | fails-identity |
| United States | `fast-grants` Fast Grants | nothing: the domain is a 404 | an academic institution, when it existed | dead |

Two records carry an amount a reader should not take at face value. The Start-Up Chile
brochure states CLP 30,000,000 for IGNITE while a CORFO call page states CLP 50,000,000; the
table carries the brochure figure. True Digital Park lists USD 25,000 of Google Cloud credit,
which may be Google's own tier rather than the park's grant.

## What the class does not give

**An entity is the price of admission.** Fourteen of twenty regional records fail on an
entity, a national identity, an institutional email or a closed process. The same gate
appears at MLPerf (membership), Amazon Alexa (one university), OpenSSF (a foundation) and
Datadog (five contributors at two employers).

**Cadence decides whether a lane is usable tonight.** Rolling: Open Technology Fund, Mozilla
MOSS, Filecoin, AWS credits, GitHub Sponsors. Annual or cohort: Summer of Code, Outreachy,
ARC, AIMO, the Sovereign Tech Fellowship, Mozilla Human-Scale. Already run: Test Flight
(2026-09-19), Trainium (2026-09-30), Malaysia Digital (2025-07-18), Zoltan's FLOPs
(2025-04-15).

**Six products are gone and one page still sells one.** Adaptable, Cyclic, Continue,
Sourcegraph Cody, Fast Grants and Mozilla Builders carry `dead`. Cyclic still publishes a
Free Forever tier of 1 GiB of RAM more than two years after the service stopped.

**No GPU-hour, no cluster, no long-running machine.** The largest allocation is 192
H100-hours at an event, the largest self-serve machine is 0.1 vCPU, and the largest storage
is Sevalla's 100 sites of 1 GB.

## How it composes

The host and sponsorship lanes meet at one account: Netlify's Open Source plan raises the
same site to 10,000 credits a month if the repository carries an OSI licence, a code of
conduct and a badge, and Vercel's Hobby plan receives whatever `v0` deploys.

The agent and anonymous lanes meet at the key: Goose, Zed, Kilo Code and Amp take a key from
any provider, so AI Horde's anonymous key fits with no paid subscription.

The prize lane composes with nothing, because it pays after the work. A reader who needs
capacity this month should read [perpetual-allowances.md](perpetual-allowances.md) and
[gpu-notebooks.md](gpu-notebooks.md).

## What would change the answer

**A published rate for NetMind's USD 100.** The record is `reported` and the vendor page
serves a JavaScript application. One hourly rate would turn it into hours, and those would
be the only free GPU time in the slice.

**A worker count for AI Horde above 51**, measured on 2026-10-22 over 28 text models. The
queue is the only thing limiting an anonymous job.

**Microsoft reopening the Azure credit form**, quoted as `The application form is not
currently open`, and **a new Mozilla Builders round**, which would restore up to
USD 100,000. **The Google patch multiplier expiring 2026-12-31** makes the top of the
USD 500 to USD 15,000 range a two-month window.

## Two records that disagree with themselves

`arc-prize-foundation` states the ARC-AGI-3 track as `USD 850K Total`, then lists a
USD 700,000 grand prize, a USD 75,000 top-score award and two USD 75,000 milestone rounds.
Those parts sum to USD 925,000, which is USD 75,000 more than the track total. This document
uses the headline USD 2,000,000 and quotes the track figures as written.

`start-up-chile` records `identity_cost.kind` as `email` while its binding note says the
first disbursement needs a Chilean entity. The regional table states the stronger gate.
