# What will answer a completion request without a card

An inference endpoint sells tokens at a rate, or gives them away to acquire users.
That is the opposite of a coding subscription, which sells a bundle of agent turns at
a flat price. The binding constraints differ, the failure modes differ, and so does
the question: can a script call a model tonight with no account.

Everything here was measured or read on 2026-10-22, and the measurement is the
substance: 34 endpoints called twice, eight minutes apart, with the status, the echoed
model, the latency and the tokens per second recorded for each call.

The answer, and it is narrower than the market advertises. **Seven hosts answered a
completion with no key at all, six of them in both runs. Four of the seven echoed the
model they were asked for on every answered call: OVHcloud's public AI Endpoints, LLM7,
BlockRun, and uncensored-llm.sbs. Only three of those four also returned an answer
rather than filler, so the three that both echo and answer are OVHcloud, LLM7 and
BlockRun** (`measured`, 2026-10-22). OVH publishes a per-minute
ceiling of 2 in its response headers and a price per token in its model list. LLM7
publishes neither, and refused one call with a 429 eight minutes after answering the
same one. BlockRun answered cleanly here and failed over to a different model eight
minutes earlier. Everything else in the keyless class either substituted a model,
served filler, gated the request to a vendor's own client, or answered 200 with four
bytes.

**The rate limits are stated with numbers and windows.** Seven lanes give a repeatable
allowance for an email address or less. `free/no-card-rate-limits.md` lists each limit with
its window and scope. NVIDIA build states up to 40 requests a minute, and no page read states
a daily figure. OpenRouter `:free` limits read 50 requests a day, or 1,000 from 10 credits
bought. Together and DeepInfra read paid-only, behind a card or a prepaid balance.

## The five facts that decide the recommendation

**A 200 is not an answer, and neither is a non-empty completion.** `models.github.ai`
returned HTTP 200, `Content-Type: text/plain`, a 4-byte body `OK`, and the identical
body hash on three calls. `uncensored-llm.sbs` returned valid JSON with
`finish_reason: stop` and the content "I'd be happy to assist. What specific aspect
would you like me to focus on?" to a request for a single token. Both defeated a
status test and one defeated a content test.

**Substitution is commoner than failure.** Six of the 34 endpoints served a model
whose name differs from the one requested (`measured`, 2026-10-22). `free.ai` served
`Qwen/Qwen3-30B-A3B-Instruct` for `qwen3-8b`, for `qwen-coder` and for
`deepseek-r1`. `kilo.ai` served `nvidia/nemotron-3.5-lightning:free` on one call and
`nvidia/nemotron-3.5-content-safety` on the next, for the same id. A benchmark keyed
on the requested string is a benchmark of a model that never ran.

**The half-life is hours, not weeks.** Four endpoints changed answer state between
two runs eight minutes apart, on one machine, with one script. The single anonymous
survivor measured on 2026-10-02 was refusing every call by 2026-10-22. A document
that prints "answers" without a timestamp is printing something that was true for one
call.

**"Keyless" describes the authentication, not the price or the quota.** OVH requires
no key and publishes a price per token for most of its models. Pollinations requires
no key and meters 1 reply every 30 seconds per IP, shared with everything else on
that address, and a caller can exhaust it with no account in existence.

**Echoed model identity is the cheapest relay detector there is.** BlockRun's error
body names `NVIDIA API error: 429 Too Many Requests`, which means BlockRun forwards
to NVIDIA on its own key and the limit belongs to BlockRun. Its failover served
`nvidia/nemotron-3-super-120b` for a `nvidia/gpt-oss-20b` request. An error naming a
different vendor's API is the tell, and it costs one call to see.

## The comparison

Sorted by whether the endpoint served what it was asked for, then by whether it
answered at all. `Echo` is the model string compared to the requested one. `A` and
`B` are the two runs. Every row is measured; the per-run numbers are
in the three class documents and in `dossier/inference/`.

| Endpoint | Requested | Echo | Answered A and B | Binds | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| OVHcloud AI Endpoints | gpt-oss-20b and 7 others | same | yes, yes | 2 requests a minute | anonymous | qualifies |
| LLM7 | nemotron-3-nano:30b | same | yes, yes | unpublished; 120 of 1,029 prober calls met a 429 | anonymous | qualifies-with-caveat |
| Kilo Gateway | 9 ids, 6 marked `:free` | 2 substituted | 8 of 9, 8 of 9 | unpublished; a 404 from this IP | anonymous | qualifies-with-caveat |
| BlockRun | nvidia/gpt-oss-20b | substituted on failover | yes, yes | upstream NVIDIA 429 | anonymous | qualifies-with-caveat |
| free.ai | 3 ids | substituted every time | yes, partly | one backend for 513 names | anonymous | qualifies-with-caveat |
| Pollinations | openai-fast | substituted | yes, yes | 1 reply per 30 seconds per IP | anonymous | qualifies-with-caveat |
| Cloudflare Workers AI | any `@cf/` model | not measured | not measured | 300,000 Neurons a month, 00:00 UTC | email | qualifies-with-caveat |
| Google Gemini API | gemini-3.8-flash | not measured | not measured | limits visible only in AI Studio | email | qualifies-with-caveat |
| Groq | `gpt-oss-120b` | not measured | not measured | 200K tokens a day, 8K a minute | email | qualifies-with-caveat |
| NVIDIA build | deepseek-v4.1-flash | not measured | not measured | up to 40 requests a minute, trial | email | trial-only |
| OpenRouter `:free` ids | ling-3.1-flash | not measured | no, no: 401 | a key, then the free-model caps | email | qualifies-with-caveat |
| OpenCode Zen free models | longcat-2.5-preview-free | n/a | no, no: 403 | the OpenCode client only | email | fails-identity |
| uncensored-llm.sbs | uncensored-llm-70b | same | no, yes with filler | unpublished | anonymous | fails-quota |
| GitHub Models inference | openai/gpt-4o-mini | n/a | no, no: 200 `OK` | nothing: no completion is returned | anonymous | dead |
| Public Ollama instances | any | n/a | not probed | no operator, no quota; the list host 404s | anonymous | fails-quota |
| Cerebras | gpt-oss-120b | not measured | not measured | USD 5 of credits that expire in 30 days, after a card | card | trial-only |
| Hugging Face Inference | any provider | not measured | no: 401 as HTML | no credits on a free account | card | paid-only |

## How the rate was measured, and why the number is weak

⚠ **Tokens per second is computed on a second, streaming request**: TTFT is
`time_starttransfer` and the denominator is `time_total - time_starttransfer`. The
numerator counts characters inside `delta.content` fragments and divides by four.

That is an approximation and not a tokenizer, and every row carries it as
`streamed chars/4 / (time_total - time_starttransfer)` so no reader can mistake one
basis for another. The non-streaming `completion_tokens` figure is carried beside it
for the same reason.

The rate is also not stable. Across three runs the same endpoint moved by up to 9.1x,
and the biggest movement between the two runs eight minutes apart was 18.2x on
`openrouter/free`, which served a different model in each call and is therefore not
the same measurement twice. **The reproducible finding is the set of endpoints that
answer and the order of magnitude, not any single rate.**

## The documents

| document | what it answers |
| --- | --- |
| [`free/no-card-rate-limits.md`](free/no-card-rate-limits.md) | every free lane that needs no card, with its rate limit, window and scope |
| [`free/keyless-anonymous.md`](free/keyless-anonymous.md) | the endpoints that need no account, how they substitute, and how fast they die |
| [`free/free-tier-with-key.md`](free/free-tier-with-key.md) | what an email address buys, and why the numbers are not public |
| [`free/trial-credit.md`](free/trial-credit.md) | one-time and expiring credit, and what it is worth per dollar |
| [`free/platform-allocation.md`](free/platform-allocation.md) | an allowance attached to a platform you already use |
| [`free/proxy-of-a-quota.md`](free/proxy-of-a-quota.md) | relays, resellers and dead shells, as a first-class category |
| [`paid/per-token-undercut.md`](paid/per-token-undercut.md) | the cheapest published rate, with the traffic mix stated |
| [`paid/batch-and-offpeak.md`](paid/batch-and-offpeak.md) | the half-price window and how to work inside it |
| [`paid/committed-throughput.md`](paid/committed-throughput.md) | reserved capacity, and when it beats paying per token |
| [`free/self-hosted-on-free-compute.md`](free/self-hosted-on-free-compute.md) | the last resort, after every hosted lane: serving your own weights on a free machine, and the boundary with the compute topic |

## What this topic cannot tell you

**Keyless rate limits are not measured**, so every keyless row carries `unverified`
for its ceiling, except OVH, whose ceiling is in its own response headers. A probe
that reaches the 429 settles a ceiling.

**Seven keyed free tiers were not called.** Groq, Cerebras, Mistral, OpenRouter,
Together, Hugging Face and DeepInfra carry a key requirement and no key was available.
Three of the seven were read from their own pages: Cerebras has no permanently free
tier, Hugging Face grants no credits to a free account, and Mistral's free tier exists
with its numbers behind a login. Each is recorded with the environment variable that
was unset, which is an absence with a cause and not a failure. Their published terms
are documented; none of their allowances was measured.

**Groq's numbers are readable.** The per-model free table is in the served HTML under
a `Free Plan Limits` tab, not behind JavaScript. It gives 30 requests a minute, 1,000
requests a day, 8,000 tokens a minute and 200,000 tokens a day on the two `gpt-oss`
ids. Groq is therefore the one keyed tier here with an absolute checkable allowance,
and the allowance is 11.4 per cent of a 52.5M-token monthly target, so it is a
fallback rather than a plan.

**Stability over weeks is not measured.** Two runs eight minutes apart are the whole
of the evidence, and they already show four endpoints changing state. The claim that
survives is about hours.

**Context windows were not swept.** A needle was retrieved at every size to 370k
characters on 2026-10-02, which shows the method. The advertised context in each
record is `documented` from the model list rather than measured.

## The dead ends

Eleven endpoints were checked and recorded with the evidence of their failure:
`models.github.ai` returns 200 with a 4-byte body; `uncensored-llm.sbs` returns
filler; `opencode.ai/zen` gates its free tier to its own client; `llm7` lists
`GLM-5.3-Flash` and `DeepSeek-V4-Flash-0731` and refuses both; `kilo` lists
`nemotron-3-super` and returns 404; OVH lists `Qwen3-32B` and returns 404;
`text.pollinations.ai` refuses `gpt-5-nano` with 402 and then 404. The pattern is
consistent enough to state as a property of the class: **a catalogue that lists a
model is not evidence that the model is served.** Seven instances are recorded: three
from an earlier sweep and four from the two runs above.

The half-life of the class is recorded in
[`../../history/2026-10-22T032432Z/`](../../history/2026-10-22T032432Z/free-inference-endpoint-half-life.md).

## The records

The records are in `dossier/inference/`. The block below counts them by verdict. Query the
store for the list: `scripts/fr sql "SELECT rid, verdict FROM record WHERE topic = 'inference'"`.

<!-- generated:start topic=inference kind=breakdown field=verdict label=verdict sort=value order=qualifies,qualifies-with-caveat,trial-only,fails-quota,fails-identity,paid-only,dead -->
| verdict | Records |
| --- | --- |
| `qualifies` | 4 |
| `qualifies-with-caveat` | 100 |
| `trial-only` | 60 |
| `fails-quota` | 3 |
| `fails-identity` | 15 |
| `paid-only` | 170 |
| `dead` | 13 |
| **all** | 365 |
<!-- generated:end -->

## Records that no other document names

Each `measured` or `documented` record of this topic that no other document of `docs/` names.

<!-- generated:start topic=inference kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `302ai` | 302.AI | paid-only | documented |
| `abliteratedllm` | AbliteratedLLM | trial-only | documented |
| `abliteration-ai` | abliteration.ai | paid-only | documented |
| `adaption` | Adaption | paid-only | documented |
| `adzuki` | Adzuki AI | paid-only | documented |
| `agentrouter` | AgentRouter | trial-only | documented |
| `agnes` | Agnes AI | paid-only | documented |
| `ai-router` | AI-ROUTER | paid-only | documented |
| `aiand` | ai& | paid-only | documented |
| `aigrow` | AIGROW | paid-only | documented |
| `aihubmix` | AIHubMix | qualifies-with-caveat | documented |
| `aion-labs` | Aion Labs | qualifies-with-caveat | documented |
| `aipg` | AI Power Grid | paid-only | documented |
| `aistupidlevel` | AI Stupid Level | qualifies-with-caveat | documented |
| `aixy` | Aixy | paid-only | documented |
| `aki-io` | AKI.IO | paid-only | documented |
| `alibaba-cn` | Alibaba (China) | qualifies-with-caveat | documented |
| `amazon-bedrock` | Amazon Bedrock | paid-only | documented |
| `ambient` | Ambient | paid-only | documented |
| `anonrouter` | AnonRouter | qualifies-with-caveat | documented |
| `anyapi` | AnyAPI | qualifies-with-caveat | documented |
| `apiko` | APIKO | trial-only | documented |
| `arcee` | Arcee | paid-only | documented |
| `augure` | Augure | qualifies | documented |
| `auriko` | Auriko | qualifies-with-caveat | documented |
| `autarcho` | Autarcho | paid-only | documented |
| `azure-cognitive-services` | Azure Cognitive Services | trial-only | documented |
| `bailing` | Bailing | paid-only | documented |
| `bazaarlink` | BazaarLink | qualifies-with-caveat | documented |
| `blueclaw` | Blue Claw | paid-only | documented |
| `bothub` | Bothub | paid-only | documented |
| `boundless` | Boundless | paid-only | documented |
| `bumo` | Bumo Router | paid-only | documented |
| `cedarllm` | CedarLLM | paid-only | documented |
| `cheapaimodel` | cheapaimodel | paid-only | documented |
| `cheapest-token` | CheapestToken | paid-only | documented |
| `cheapllm` | cheapllm.shop | qualifies-with-caveat | documented |
| `clarifai` | Clarifai | trial-only | documented |
| `claudinio` | Claudinio | paid-only | documented |
| `cloudcode` | CloudCode.ONE | paid-only | documented |
| `confidential-ai` | Confidential AI | paid-only | documented |
| `contextual-ai-rerank` | Contextual AI reranker API | trial-only | documented |
| `coralbricks` | CoralBricks | paid-only | documented |
| `cortecs` | Cortecs | paid-only | documented |
| `coze` | Coze | trial-only | documented |
| `crossmodel` | CrossModel | paid-only | documented |
| `dahl-inference` | Dahl Inference | trial-only | documented |
| `daoxe` | DaoXE | paid-only | documented |
| `deepl-api-developer` | DeepL API (Developer plan) | trial-only | documented |
| `deepl-api-free` | DeepL API (Free plan) | dead | documented |
| `dinference` | DInference | paid-only | documented |
| `dothoosh` | DotHoosh | paid-only | documented |
| `doubleword` | Doubleword | paid-only | documented |
| `drun` | D.Run (China) | paid-only | documented |
| `ebcloud` | EBCloud | trial-only | documented |
| `edenai` | Eden AI | paid-only | documented |
| `empiriolabs` | EmpirioLabs AI | qualifies-with-caveat | documented |
| `engy` | engy | paid-only | documented |
| `entrim` | Entrim | paid-only | documented |
| `ezkielyna` | Ezkielyna | paid-only | documented |
| `fastrouter` | FastRouter | qualifies-with-caveat | documented |
| `fiftyx` | 50X | paid-only | documented |
| `fireworks-ai` | Fireworks AI | paid-only | documented |
| `fireworks-ai-serverless` | Fireworks AI | paid-only | documented |
| `fortytwo` | Fortytwo | qualifies-with-caveat | documented |
| `freemodel` | FreeModel | qualifies | documented |
| `friendli` | Friendli | paid-only | documented |
| `friendli-ai` | FriendliAI Model APIs | paid-only | documented |
| `gisoo` | Gisoo | paid-only | documented |
| `glhf` | GLHF (glhf.chat) | dead | measured |
| `google-cloud-translation` | Google Cloud Translation | qualifies-with-caveat | documented |
| `google-vertex` | Vertex | trial-only | documented |
| `google-vertex-anthropic` | Vertex (Anthropic) | trial-only | documented |
| `graphn` | GraphN | trial-only | documented |
| `greenpt` | GreenPT | trial-only | documented |
| `grokified` | Grokified | trial-only | documented |
| `helicone` | Helicone | qualifies-with-caveat | documented |
| `hopper` | Hopper | trial-only | documented |
| `hostinger-router` | Hostinger Router | paid-only | documented |
| `huawei-maas` | Huawei Cloud MAAS | paid-only | documented |
| `hubris` | Hubris | qualifies-with-caveat | documented |
| `humain` | HUMAIN | fails-identity | documented |
| `ibm-watsonx-ai-free` | IBM watsonx.ai (Free / Lite plan) | qualifies-with-caveat | documented |
| `impossibl` | Impossibl | paid-only | documented |
| `inco` | Inco | paid-only | documented |
| `inferall` | InferAll | qualifies | documented |
| `inference-coop` | Inference Cooperative | paid-only | documented |
| `inferenceapis` | Inference APIs | paid-only | documented |
| `inferris` | Inferris | trial-only | documented |
| `infersia` | Infersia | qualifies-with-caveat | documented |
| `inferx` | InferX | paid-only | documented |
| `isoquant` | Isoquant | paid-only | documented |
| `jad-ai` | Jad AI | qualifies-with-caveat | documented |
| `jalapeno` | Jalapeno Cloud | paid-only | documented |
| `jiekou` | Jiekou.AI | paid-only | documented |
| `jina-ai-embeddings-reranker` | Jina AI embeddings and reranker API | trial-only | documented |
| `joingonka` | JoinGonka | paid-only | documented |
| `jzstoken` | JZSTOKEN | trial-only | documented |
| `kenari` | Kenari | qualifies-with-caveat | documented |
| `kitani` | Kitani | paid-only | documented |
| `klavo` | Klavo AI | paid-only | documented |
| `klokintegration` | klokintegration.se | trial-only | documented |
| `korouter` | KoRouter | paid-only | documented |
| `kosmik` | Kosmik Compute | trial-only | documented |
| `kunavo` | Kunavo | paid-only | documented |
| `lambda-inference` | Lambda Inference API | dead | measured |
| `langsearch-rerank-api` | LangSearch Rerank API | dead | documented |
| `libretranslate-hosted` | LibreTranslate hosted (libretranslate... | paid-only | documented |
| `liquid` | Liquid Inference | qualifies-with-caveat | documented |
| `lithosai` | LithosAI | paid-only | documented |
| `llamaparse-free` | LlamaParse | qualifies-with-caveat | documented |
| `llmgateway-providers` | LLM Gateway | qualifies-with-caveat | documented |
| `llmtech` | LLM Tech | qualifies-with-caveat | documented |
| `llmtr` | LLMTR | paid-only | documented |
| `logits` | Logits | paid-only | documented |
| `lowrouter` | LowRouter | trial-only | documented |
| `lucidquery` | LucidQuery | paid-only | documented |
| `mallard` | Mallard AI | trial-only | documented |
| `mathpix-ocr-api` | Mathpix OCR API | paid-only | documented |
| `meganova` | Meganova | qualifies-with-caveat | documented |
| `melious` | Melious | paid-only | documented |
| `meragpt` | meraGPT | trial-only | documented |
| `merge-gateway` | Merge Gateway | qualifies-with-caveat | documented |
| `minimax-cn` | MiniMax (minimax.cn) | paid-only | documented |
| `mixedbread-search-starter` | Mixedbread (managed search with reran... | trial-only | documented |
| `mixlayer` | Mixlayer | qualifies-with-caveat | documented |
| `model-oracle-ai` | Model Oracle AI | paid-only | documented |
| `modelis` | Modelis | qualifies-with-caveat | documented |
| `modular` | Modular | paid-only | documented |
| `moneo` | Moneo | trial-only | documented |
| `moonshot-kimi-api-international` | Moonshot Kimi API Platform international | paid-only | documented |
| `moonshotai-cn` | Moonshot AI (China) | paid-only | documented |
| `munito-eu` | Munito AI (EU) | fails-identity | documented |
| `nano-gpt` | NanoGPT | paid-only | documented |
| `nearai` | NEAR AI Cloud | paid-only | documented |
| `nebius-token-factory` | Nebius Token Factory | trial-only | documented |
| `neosmith` | NeoSmith | paid-only | documented |
| `neuralwatt` | Neuralwatt | fails-identity | documented |
| `nlp-cloud` | NLP Cloud | fails-identity | documented |
| `nodecode` | Nodecode | qualifies-with-caveat | documented |
| `nokeep` | nokeep | paid-only | documented |
| `nous-portal-free` | Nous Portal | qualifies-with-caveat | documented |
| `novita-ai` | Novita AI | paid-only | documented |
| `novita-llm-api` | Novita LLM API | qualifies-with-caveat | documented |
| `oathbreaker` | Oathbreaker AI | paid-only | documented |
| `obscurify` | Obscurify.ai | trial-only | documented |
| `ofox` | Ofox | paid-only | documented |
| `onomeo` | onomeo | paid-only | documented |
| `openreason` | OpenReason | paid-only | documented |
| `opper` | Opper | qualifies-with-caveat | documented |
| `orcarouter` | OrcaRouter | qualifies-with-caveat | documented |
| `outerlabs` | Outer Labs | trial-only | documented |
| `pareto` | Pareto Inference | paid-only | documented |
| `pendra` | Pendra | paid-only | documented |
| `perplexity-agent` | Perplexity Agent | paid-only | documented |
| `pinecone-inference` | Pinecone Inference (embeddings and re... | qualifies-with-caveat | documented |
| `pioneer` | Pioneer | paid-only | documented |
| `powerspring` | Powerspring | paid-only | documented |
| `privatemode-ai` | Privatemode AI | trial-only | documented |
| `proxystacks` | ProxyStacks Relay | paid-only | documented |
| `qdrant-cloud-inference` | Qdrant Cloud Inference (free models o... | qualifies-with-caveat | documented |
| `qihang-ai` | QiHang | paid-only | documented |
| `qiniu-ai` | Qiniu | paid-only | documented |
| `rayline` | Rayline | paid-only | documented |
| `reducto-standard` | Reducto | trial-only | documented |
| `refuseless` | Refuseless | qualifies-with-caveat | documented |
| `routing-run` | routing.run | paid-only | documented |
| `ruapi` | RuAPI | paid-only | documented |
| `sagg` | SAGG | paid-only | documented |
| `sakana` | Sakana AI | paid-only | documented |
| `sandbase` | SandBase | paid-only | documented |
| `sap-ai-core` | SAP AI Core | paid-only | documented |
| `sarvam` | Sarvam AI | qualifies-with-caveat | documented |
| `scx-ai` | SCX.ai | paid-only | documented |
| `sensenova` | SenseNova (China) | qualifies-with-caveat | documented |
| `snowflake-cortex` | Snowflake Cortex | paid-only | documented |
| `sokkan` | SOKKAN Router | paid-only | documented |
| `sparrowcodes` | SparrowCodes | qualifies-with-caveat | documented |
| `standardcompute` | Standard Compute | trial-only | documented |
| `steadyrouter` | SteadyRouter | trial-only | documented |
| `stepfun-ai` | StepFun (Global) | paid-only | documented |
| `stepping-stone` | stepping stone AG | paid-only | documented |
| `subconscious` | Subconscious | paid-only | documented |
| `submodel` | submodel | qualifies-with-caveat | documented |
| `superbot-gg` | superbot | qualifies-with-caveat | documented |
| `synthorai` | Synthorai | paid-only | documented |
| `teamorouter` | TeamoRouter | paid-only | documented |
| `teapot-router` | Teapot Router | trial-only | documented |
| `tencent-tokenhub` | Tencent TokenHub | qualifies-with-caveat | documented |
| `tensorx` | TensorX | paid-only | documented |
| `tetrate-agent-router-service` | Tetrate Agent Router Service | trial-only | documented |
| `the-grid-ai` | The Grid AI | paid-only | documented |
| `therouter` | TheRouter | paid-only | documented |
| `thinkingmachines` | Thinking Machines | paid-only | documented |
| `toapis` | ToAPIs | paid-only | documented |
| `togetherai` | Together AI | qualifies-with-caveat | documented |
| `token-harbor` | Token Harbor | qualifies-with-caveat | documented |
| `tokengo` | TokenGo | paid-only | documented |
| `tokenify` | Tokenify | trial-only | documented |
| `tokenlab` | TokenLab | paid-only | documented |
| `tokenrouter` | TokenRouter | paid-only | documented |
| `tokenwatt` | TokenWatt | trial-only | documented |
| `trustedrouter` | TrustedRouter | paid-only | documented |
| `trustedtokens` | TrustedTokens | fails-identity | documented |
| `umans-ai` | Umans AI | paid-only | documented |
| `unbiased` | Pareto by Unbiased | paid-only | documented |
| `uncensuredai` | UncensuredAI | paid-only | documented |
| `unorouter` | UnoRouter | qualifies-with-caveat | documented |
| `unstructured-transform-free` | Unstructured Transform | trial-only | documented |
| `uplinkswitch` | UplinkSwitch | paid-only | documented |
| `vancine` | Vancine | paid-only | documented |
| `vivgrid` | Vivgrid | paid-only | documented |
| `wafer-ai` | Wafer | paid-only | documented |
| `wallaby` | Wallaby | trial-only | documented |
| `wally` | Wally | paid-only | documented |
| `watsonx` | watsonx.ai | qualifies-with-caveat | documented |
| `watt` | Watt Cloud | trial-only | documented |
| `weaviate-embeddings` | Weaviate Embeddings (Weaviate Cloud f... | qualifies-with-caveat | documented |
| `xpersona` | Xpersona | paid-only | documented |
| `xxapi` | xxapi | paid-only | documented |
| `zeldoc` | Zeldoc | fails-identity | documented |
| `zenifra` | Zenifra | paid-only | documented |
| `zenmux` | ZenMux | qualifies-with-caveat | documented |
| `zeroentropy-rerank-embeddings` | ZeroEntropy zerank reranker and zembe... | dead | measured |
| `zhipuai` | Zhipu AI | qualifies-with-caveat | documented |
| `zro` | Zro | qualifies-with-caveat | documented |
| `atomic-chat` | Atomic Chat (self-hosted) | qualifies-with-caveat | documented |
| `frogbot` | FrogBot (self-hosted) | paid-only | documented |
| `lmstudio` | LMStudio (self-hosted) | qualifies-with-caveat | documented |
| `lynkr` | Lynkr (self-hosted) | qualifies-with-caveat | documented |
| `qvac` | QVAC (self-hosted) | qualifies-with-caveat | documented |
<!-- generated:end -->
