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
| `qualifies` | 1 |
| `qualifies-with-caveat` | 39 |
| `trial-only` | 26 |
| `fails-quota` | 3 |
| `fails-identity` | 7 |
| `paid-only` | 20 |
| `dead` | 12 |
| **all** | 108 |
<!-- generated:end -->

## Records that no other document names

Each `measured` or `documented` record of this topic that no other document of `docs/` names.

<!-- generated:start topic=inference kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `aion-labs` | Aion Labs | qualifies-with-caveat | documented |
| `bazaarlink` | BazaarLink | qualifies-with-caveat | documented |
| `contextual-ai-rerank` | Contextual AI reranker API | trial-only | documented |
| `coze` | Coze | trial-only | documented |
| `dahl-inference` | Dahl Inference | trial-only | documented |
| `deepl-api-developer` | DeepL API (Developer plan) | trial-only | documented |
| `deepl-api-free` | DeepL API (Free plan) | dead | documented |
| `fireworks-ai-serverless` | Fireworks AI | paid-only | documented |
| `friendli-ai` | FriendliAI Model APIs | paid-only | documented |
| `glhf` | GLHF (glhf.chat) | dead | measured |
| `google-cloud-translation` | Google Cloud Translation | qualifies-with-caveat | documented |
| `grokified` | Grokified | trial-only | documented |
| `ibm-watsonx-ai-free` | IBM watsonx.ai (Free / Lite plan) | qualifies-with-caveat | documented |
| `iteracompute` | IteraCompute | qualifies-with-caveat | documented |
| `jina-ai-embeddings-reranker` | Jina AI embeddings and reranker API | trial-only | documented |
| `lambda-inference` | Lambda Inference API | dead | measured |
| `langsearch-rerank-api` | LangSearch Rerank API | dead | documented |
| `libretranslate-hosted` | LibreTranslate hosted (libretranslate... | paid-only | documented |
| `llamaparse-free` | LlamaParse | qualifies-with-caveat | documented |
| `mathpix-ocr-api` | Mathpix OCR API | paid-only | documented |
| `mixedbread-search-starter` | Mixedbread (managed search with reran... | trial-only | documented |
| `moonshot-kimi-api-international` | Moonshot Kimi API Platform international | paid-only | documented |
| `nebius-token-factory` | Nebius Token Factory | trial-only | documented |
| `nlp-cloud` | NLP Cloud | fails-identity | documented |
| `novita-llm-api` | Novita LLM API | qualifies-with-caveat | documented |
| `onomeo` | onomeo | paid-only | documented |
| `pinecone-inference` | Pinecone Inference (embeddings and re... | qualifies-with-caveat | documented |
| `qdrant-cloud-inference` | Qdrant Cloud Inference (free models o... | qualifies-with-caveat | documented |
| `reducto-standard` | Reducto | trial-only | documented |
| `tetrate-agent-router-service` | Tetrate Agent Router Service | trial-only | documented |
| `token-harbor` | Token Harbor | qualifies-with-caveat | documented |
| `unstructured-transform-free` | Unstructured Transform | trial-only | documented |
| `weaviate-embeddings` | Weaviate Embeddings (Weaviate Cloud f... | qualifies-with-caveat | documented |
| `zeroentropy-rerank-embeddings` | ZeroEntropy zerank reranker and zembe... | dead | measured |
<!-- generated:end -->
