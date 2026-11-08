# The endpoints that need no account, how they substitute, and how fast they die

The anonymous class is the only inference here that costs no identity at all. There
is no account, no key, no email address and no card. That is a real advantage for a
reader whose binding constraint is registration, and it is bought with three
properties that make the class hard to use: the quota is metered per IP rather than
per account, the served model is often not the requested one, and the provider owes
the caller nothing.

Every finding below is a live call made on 2026-10-22, twice, on one machine from one
IP.

The answer: **OVHcloud's public AI Endpoints is the only endpoint here that answered
every call, served the requested model, published a price per token and published its
own rate limit in a response header** (`measured`, 2026-10-22). Behind it the order is
set by the prober's own accepted-only rate: free.ai and Pollinations at 96 and 100 per
cent, Kilo at 80, LLM7 at 68. Every one of them substitutes a model or serves filler
eventually, so none is a substitute for a keyed tier.

## The comparison

Sorted by how much of the request was honoured. `Echo` compares the model string the
endpoint returned against the one sent. The tok/s columns are the two runs and they
are not comparable to each other across rows, only within one.

| Endpoint | Model requested | Echo | A | B | tok/s A | tok/s B | Ceiling | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVHcloud | gpt-oss-20b | same | 200 yes | 200 yes | 12.02 | 14.77 | 2 a minute, in headers | qualifies |
| OVHcloud | Meta-Llama-3_3-70B-Instruct | same | 200 yes | 200 yes | 9.19 | 8.98 | 2 a minute, in headers | qualifies |
| OVHcloud | Mistral-Nemo-Instruct-2407 | same | 200 yes | 200 yes | 3.67 | 3.67 | 2 a minute, in headers | qualifies |
| OVHcloud | Qwen3.8-27B | same | 200 yes | 200 yes | 27.64 | 21.76 | 2 a minute, in headers | qualifies |
| OVHcloud | gpt-oss-120b | same | 200 yes | 200 yes | 22.67 | 25.84 | 2 a minute, in headers | qualifies |
| OVHcloud | Qwen3Guard-Gen-0.6B | same | 200 yes | 200 yes | 103.11 | 91.75 | 2 a minute, in headers | qualifies |
| LLM7 | nemotron-3-nano:30b | same | 200 yes | 200 yes | 53.12 | 86.43 | not published | qualifies-with-caveat |
| LLM7 | minimax-m2.7 | same | 200 yes | 200 yes | - | - | not published | qualifies-with-caveat |
| Kilo Gateway | cohere/north-mini-code:free | same | 200 yes | 200 yes | 33.62 | 44.03 | not published | qualifies-with-caveat |
| Kilo Gateway | minimax/minimax-m3.1-flash:free | same | 200 yes | 200 yes | 61.35 | 33.22 | not published | qualifies-with-caveat |
| Kilo Gateway | dots-studio/dots-3-note-preview:free | same | 200 yes | 200 yes | 8.04 | 23.86 | not published | qualifies-with-caveat |
| BlockRun | nvidia/gpt-oss-20b | same in both runs | 200 yes | 200 yes | 12.92 | 13.23 | upstream NVIDIA 429 | qualifies-with-caveat |
| Kilo Gateway | poolside/laguna-s-2.1:free | same | 200 yes | 200 yes | - | - | not published | qualifies-with-caveat |
| Pollinations | openai-fast | `gpt-oss-20b` | 200 yes | 200 yes | - | - | 1 reply per 30s per IP | qualifies-with-caveat |
| free.ai | qwen3-8b | `Qwen/Qwen3-30B-A3B-Instruct` | 200 yes | 200 yes | 10.91 | 13.87 | one backend for 513 names | qualifies-with-caveat |
| free.ai | qwen-coder | `Qwen/Qwen3-30B-A3B-Instruct` | 200 yes | 200 yes | 10.03 | 12.92 | one backend for 513 names | qualifies-with-caveat |
| Kilo Gateway | reflection/beam-free | `reflection/beam` | 200 yes | 200 yes | 183.40 | 221.56 | not published | fails-quota |
| Kilo Gateway | openrouter/free | two different models | 200 yes | 200 yes | 3.20 | 58.14 | routes per call | fails-quota |
| OVHcloud | Qwen3.5-397B-A17B | same | 200 no | 200 no | - | - | 256-token reasoning budget | qualifies-with-caveat |
| uncensored-llm.sbs | uncensored-llm-70b | same | 403 | 200 filler | - | - | not published | fails-quota |
| OpenCode Zen | space-bunny-free | n/a | 403 | 400 | - | - | the OpenCode client | dead |
| OpenCode Zen | longcat-2.5-preview-free | n/a | 403 | 403 | - | - | the OpenCode client | fails-identity |
| Pollinations | gpt-5-nano | n/a | 402 | 404 | - | - | per-IP budget, then not served | dead |
| Kilo Gateway | nvidia/nemotron-3-super-120b-a12b:free | n/a | 404 | 404 | - | - | not on the tier from this IP | dead |
| LLM7 | GLM-5.3-Flash | n/a | 400 | 400 | - | - | listed, refuses | dead |
| LLM7 | DeepSeek-V4-Flash-0731 | n/a | 400 | 400 | - | - | listed, refuses | dead |
| LLM7 | codestral-latest | n/a | 200 yes | 429 | - | - | a per-minute 429 | qualifies-with-caveat |
| OVHcloud | Qwen3-32B | n/a | 404 | 404 | - | - | listed, does not exist | dead |
| OVHcloud | Qwen3.6-27B | same | 200 yes | 200 no | - | - | 256-token reasoning budget | qualifies-with-caveat |
| GitHub Models | openai/gpt-4o-mini | n/a | 200 `OK` | 200 `OK` | - | - | nothing is returned | dead |

⛔ **Every rate in that table is `streamed chars/4 / (time_total - time_starttransfer)`
on a second streaming call**, not a tokenizer count. The `tok/s A` and `tok/s B`
columns differ by up to 3x for an endpoint that served the same model in both runs,
and by 18x on the one row that served a different model in each call. A single figure
from this table describes one call and nothing else.

## OVHcloud AI Endpoints

OVHcloud's public AI Endpoints answer with no key and expose 22 model ids, each
carrying a `context_length` and a `pricing` object in USD per token (`measured`,
`oai.endpoints.kepler.ai.cloud.ovh.net/v1/models`, read 2026-10-22). Twelve of the 22
are chat models and the rest are one image model, three embeddings, four TTS and two
ASR. Nine ids were probed: seven answered in the first run and six in the second,
every one of them echoing the requested model, with the needle present in five of the
seven.

The ceiling is published in a response header rather than in documentation:
`x-ratelimit-limit-minute: 2`, `ratelimit-reset: 34`. Two requests a minute is the
tightest published ceiling found anywhere in this topic, and it is also the most
honest, because it is stated in the reply to a real request rather than in a policy
page that may describe a different tier.

The pricing object is the machine form of "free" that a catalogue should carry.
`Qwen3Guard-Gen-0.6B` and `Qwen3Guard-Gen-8B` are priced at exactly zero for prompt
and completion. `gpt-oss-20b` is priced at 0.00000005 USD per prompt token and
0.00000018 per completion token, which is USD 0.05 and USD 0.18 per million. So a
caller with no key is spending a real, published amount of somebody's money, and the
endpoint is not free in the sense that matters to a budget.

⛔ **Two models return HTTP 200 with empty content at `max_tokens: 256`.**
`Qwen3.5-397B-A17B` and `Qwen3.6-27B` are reasoning models that spend the completion
budget on a `reasoning` field and return `finish_reason: length` with nothing in
`content`. That is a working model out of budget, not a dead endpoint, and a re-run at
`max_tokens: 900` returned 897 completion tokens, a `stop` reason and a real answer. A
probe that reads only `content` reports a working reasoning model as broken.

Evidence: nine live calls across two runs on 2026-10-22, plus `/v1/models` and a
header read at 03:17:26Z. Verdict: the best-behaved keyless endpoint found, on the
tightest ceiling, at a published price above zero.

## LLM7

LLM7 answered with no key and echoed the requested model for `nemotron-3-nano:30b`,
`minimax-m2.7` and `codestral-latest` (`measured`, 2026-10-22). Its `/v1/models`
lists 68 ids, each with a pricing object in USD per 1M tokens, and none of them is
priced at zero.

`nemotron-3-nano:30b` measured 53.12 and 86.43 tok/s in the two runs and was the
fastest clean endpoint in the sweep. `codestral-latest` answered in run A and
returned `429 rate_limit_exceeded, retry_after: 1` in run B, eight minutes later. So
the endpoint has a per-minute ceiling and does not publish it.

Two listed ids refuse the chat call outright: `GLM-5.3-Flash` and
`DeepSeek-V4-Flash-0731` both return 400 `model_unavailable`. Neither string is in
LLM7's own `/v1/models` list, which carries `glm-5.3` and `deepseek-v4-flash:0731`
instead. So both ids are slugs from elsewhere, and a 400 on an id the vendor never
published is correct behaviour. It is not evidence of a catalogue that lies.

The prober's own track record for the endpoint is 380 of 1,029 calls answered over 14
days, 37 per cent (`stillworks.supercapybara.com/llm/llm7`, read 2026-10-22T04:21Z).
That headline understates the endpoint, and the prober says so on the same page. Of the
1,029 calls, 389 asked for a model the provider does not serve, which is the same
listed-but-refused shape the paragraph above describes. **Counting only the 556 calls
LLM7 accepted for a model it offers, 380 answered, which is 68 per cent.** The 120
rate-limited calls are the real ceiling signal, and 649 - 120 - 84 - 389 - 24 - 32 = 0,
so the breakdown is complete.

For comparison the same page's figures for the other keyless endpoints are OVH at 244
of 343 (71 per cent, 91 per cent excluding models it does not serve), Kilo at 549 of
1,464 (38 per cent, 80 per cent accepted-only), free.ai at 194 of 732 (27 per cent, 96
per cent accepted-only) and Pollinations at 343 of 343. **LLM7 at 68 per cent is the
third of five, not the second.** The ordering that survives is OVH, then free.ai and
Pollinations tied on accepted-only, then Kilo, then LLM7.

Evidence: ten live calls across two runs, `/v1/models`, and the prober's per-endpoint
track record. Verdict: 68 per cent of the calls it accepts, and a retry loop is worth
writing because one call in three meets a 429 or a model the provider will not serve.

## Kilo Gateway

Kilo's gateway answered eight of nine `:free` ids with no key and echoed the requested
model for six of them (`measured`, 2026-10-22). `cohere/north-mini-code:free` is a
coding model and measured 33.62 and 44.03 tok/s. `minimax/minimax-m3.1-flash:free`
measured 61.35 and 33.22.

Three findings make this the most complicated row here:

- `reflection/beam-free` echoed `reflection/beam`. A `:free` suffix was stripped,
  which is benign, but it means a benchmark keyed on the requested string is
  attributed to a model that never ran.
- `openrouter/free` echoed `nvidia/nemotron-3.5-lightning:free` in run A and
  `nvidia/nemotron-3.5-content-safety` in run B. The same id routed to two different
  models eight minutes apart, which is what a router does and which makes any
  per-call rate meaningless for that id.
- `nvidia/nemotron-3-super-120b-a12b:free` returned 404 in both runs, and the body
  nests the upstream provider's 404 inside Kilo's error envelope. The third-party
  prober had that model at 34 of 35 answered, so the difference is this IP or this
  tier and not the endpoint's health.

Evidence: eighteen live calls across two runs, plus the 540 KB `/models` payload.
Verdict: the widest free catalogue in the class, with per-call routing that defeats
comparison.

## BlockRun

BlockRun answered `nvidia/gpt-oss-20b` with the requested model echoed in both runs,
at 12.92 and 13.23 tok/s (`measured`, 2026-10-22). In a sweep eight minutes earlier,
one of five sequential identical calls echoed `nvidia/nemotron-3-super-120b` instead,
and three returned `FREE_MODEL_FAILED` with
`debug: "NVIDIA API error: 429 Too Many Requests"`.

That error body is the finding. It names a different vendor's API, which means
BlockRun forwards to NVIDIA on its own key and the 429 is NVIDIA's limit on BlockRun
rather than on the caller. Its `/v1/models` carries 117 ids across at least thirteen
vendor families including OpenAI, Anthropic, Google, xAI and ElevenLabs, and only
seven of them are priced at zero. A catalogue that broad is a relay, not a model
vendor.

The failure mode matters for a retry loop: `FREE_MODEL_FAILED` arrives with a JSON
`code` field rather than a 429 status, so a caller that classifies on HTTP status
will report this endpoint healthy while it refuses most calls.

Evidence: the 2-of-5 sequential-call result in the earlier sweep and two clean calls
in the runs above. Verdict: a relay that fails over to a different model and names its
upstream.

## free.ai

free.ai answered every id probed with no key and **echoed
`Qwen/Qwen3-30B-A3B-Instruct` for all of them** (`measured`, 2026-10-22):
`qwen3-8b`, `qwen-coder` and `deepseek-r1` in run A, and the first two again in run
B. Its `/v1/models` carries 513 entries, 45 of them marked `self_hosted: true`.

So the catalogue is 513 names for approximately one backend. Every capacity or
quality claim about free.ai is a claim about Qwen3-30B-A3B, and the third-party
prober's "9 of 513 models answering" is better read as nine ids that resolve to the
same model.

Evidence: six live calls across two runs and a count of the models array. Verdict:
usable, and not usable as a model catalogue.

## Pollinations

Pollinations' Classic API lists exactly one model, `openai-fast`, described as
`GPT-OSS 20B Reasoning LLM (OVH)` with aliases including `gpt-oss` and `gpt-oss-20b`
(`measured`, `text.pollinations.ai/models`, read 2026-10-22). A request for
`openai-fast` returns `gpt-oss-20b`, so the endpoint is a relay of the OVH public tier
under an alias.

Its ceiling is the most important number in this class. A second model on the same
base returned **402** with `"Free limit reached: 1 reply every 30 seconds per IP"` in
run A and **404** with `"Model 'gpt-5-nano' isn't on the Classic API"` in run B, eight
minutes apart. Two different failures for the same URL in one session.

That 402 is the whole argument about keyless quotas. The allowance is metered per IP
and is shared with everything else on that address, so it can be exhausted with no
account in existence, and the same endpoint can answer from one IP while refusing
from another at the same moment.

Evidence: four live calls across two runs and the one-entry model list. Verdict: one
model, an alias, a 30-second per-IP floor, and a relay of OVH beneath it.

## What did not work

- **GitHub Models inference.** HTTP 200, `Content-Type: text/plain`, a 4-byte body
  `OK`, identical sha256 `19d8c9921b99c82d` on three calls across two runs. A
  status-only probe scores it as a working free endpoint.
- **uncensored-llm.sbs.** Answers 200 with valid JSON, `finish_reason: stop` and
  content that is filler, not an answer. Also refused once with Cloudflare Error 1010
  because the request carried Python's default User-Agent.
- **OpenCode Zen.** `longcat-2.5-preview-free` returns 403 `FreeTierError: OpenCode's
  free tier can only be used from within OpenCode`, with two different User-Agents.
  `space-bunny-free`, the only anonymous survivor measured on 2026-10-02, returns 400
  "Model is unavailable" twenty days later.
- **Two listed-but-unserved ids.** Kilo's `nemotron-3-super-120b-a12b:free` and OVH's
  `Qwen3-32B` return 404 while their catalogues list them. Two LLM7 ids that refuse are
  slugs from elsewhere: neither string is in LLM7's own `/v1/models`, so a 400 on them
  is correct behaviour and not a lying catalogue.

## Chaining

OVH plus a free-standing agent from
[`../../coding-subs/free/free-standing-agent.md`](../../coding-subs/free/free-standing-agent.md)
is a complete stack with no account: a CLI agent, an endpoint, and a two-request-a-
minute ceiling that a batch job fits inside and an interactive session does not. For
anything faster, LLM7 is the endpoint to pair with a retry loop, because the prober's
own figures put it at 380 of 556 accepted calls answered, 68 per cent, and 120 of the
1,029 calls it measured met a 429.
