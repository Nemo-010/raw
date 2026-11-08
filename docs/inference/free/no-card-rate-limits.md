# Free LLM APIs that answer without a card, and their rate limits

This document lists the free LLM inference APIs that a person can use with no payment
method, and the rate limit of each one. Every row is a record in `dossier/inference/`
as it stood on 2026-10-28. The record is the authority for every number below; when a
row and its record disagree, the record is right.

The answer: **seven lanes give a repeatable, checkable allowance for an email address or
less**, and one of them needs no account at all. Groq gives 30 requests a minute and
200,000 tokens a day. NVIDIA build gives up to 40 requests a minute. OpenRouter `:free`
ids give 50 requests a day, or 1,000 a day after 10 credits are bought. Cloudflare Workers
AI gives 10,000 Neurons a day. flm gives 60 requests a minute and 10,000,000 tokens a day
per IP address with no account. Cohere gives 1,000 calls a month. Requesty gives 200
requests a day. Inception Labs also gives 100 million tokens once (`documented`, 2026-10-28).

## How to read the numbers

Most numbers are `documented`: a vendor page said it, and the record keeps the quoted
sentence and a capture. A `measured` number came from a probe or from a response header,
as the OVHcloud figure of 2 requests a minute did. A cell that says `unpublished` means the
vendor shows no number. A cell that says `login` means the number exists but only inside
a signed-in console.

⚠ **A limit has a window and a scope.** "20 requests a minute" per model is not the same
as 20 requests a minute per account. The record names the scope where the vendor does.
Where a daily and a per-minute limit both apply, the lower one binds first.

## Lane 1: no account and no key

These lanes accept a request with no `Authorization` header, or with a documented
placeholder. The limit is per IP address, so it is shared with everything else on that
address.

| Provider | Rate limit | Rung | Record |
| --- | --- | --- | --- |
| flm | 60 requests a minute, 20,000 requests a day and 10,000,000 tokens a day per IP address; 65,536 input and 8,192 output tokens per request | documented | `inference/flm` |
| OVHcloud AI Endpoints | 2 requests a minute per IP address and per model; 400 a minute with a key, per project and per model | measured | `inference/ovh-ai-endpoints` |
| DG AI API | 8 requests per 10 seconds anonymous; 16 per 10 seconds verified | documented | `inference/dg-ai-api` |
| Puter.js AI | 20 requests per 10 seconds for a guest account, 2 concurrent; the monthly allowance shows in the dashboard | documented | `inference/puter-js-ai` |
| Pollinations | 1 reply every 30 seconds per IP address | measured | `inference/pollinations` |
| LLM7 | keyless: unpublished. With a free token: 1 request a second, 60 a minute, 250 an hour and 100,000 tokens per 24 hours | measured and documented | `inference/llm7` |
| Api.Airforce | 1 request a minute and 1,000 requests a day, free models only; a username and password, no email | documented | `inference/api-airforce` |
| Kilo Gateway, BlockRun, free.ai, BeaverNet, JarvisClaw | unpublished for keyless use; see each record | mixed | `inference/kilo-gateway`, `inference/blockrun`, `inference/free-ai`, `inference/beavernet`, `inference/jarvisclaw-free` |
| AI Horde text | no quota; anonymous requests queue at the lowest priority | documented | `inference/ai-horde-text` |
| Hugging Face ZeroGPU Spaces and public Gradio chat Spaces | 2 minutes of GPU a day for an unauthenticated caller; 5 minutes with a free account | documented | `inference/huggingface-zerogpu-spaces-api`, `inference/huggingface-gradio-chat-spaces` |

⚠ **Answered once is not available.** A third-party prober reports that free.ai answered
27 per cent of calls over 10 days, LLM7 37 per cent over 14 days and Kilo Gateway 38 per
cent over 10 days. Treat every row in this lane as a fallback.

## Lane 2: an email address, no card

These lanes issue a key to an account made with an email address or a social sign-in.
The limit is per account, project or organisation.

| Provider | Rate limit | Rung | Record |
| --- | --- | --- | --- |
| Groq | 30 requests a minute, 1,000 a day, 8,000 tokens a minute and 200,000 a day on `openai/gpt-oss-120b`, `openai/gpt-oss-20b` and `qwen/qwen3.8-27b` | documented | `inference/groq` |
| NVIDIA build | up to 40 requests a minute for most models, per account; no per-token billing | documented | `inference/nvidia-build-trial` |
| OpenRouter `:free` ids | 20 requests a minute; 50 requests a day under 10 credits bought, 1,000 a day from 10 credits | documented | `inference/openrouter-free-ids` |
| Cloudflare Workers AI | 10,000 Neurons a day, reset 00:00 UTC; 300 requests a minute for text generation | documented | `inference/cloudflare-workers-ai` |
| Cohere trial key | 1,000 API calls a month; chat 20 requests a minute per model | documented | `compute/cohere-trial-keys` |
| Requesty | 200 requests a day and 20 a minute for a new organisation, across all free models | documented | `inference/requesty` |
| Inception Labs | 100 million tokens once; per minute 1,000 requests, 1,000,000 input and 100,000 output tokens | documented | `inference/inception-labs` |
| Google Gemini API | Free tier on `gemini-3.8-flash`; the numbers are `login` (AI Studio) | documented | `inference/google-gemini-api` |
| Mistral La Plateforme | Free mode, no card; the numbers are `login` | documented | `inference/mistral-la-plateforme` |
| LLM Gateway | 5 requests per 10 minutes per free model with no credits | documented | `inference/llm-gateway` |
| Netlify AI Gateway | a pool of 300 credits on the Free plan and 90 credits a minute per team, after one production deploy | documented | `inference/netlify-ai-gateway` |
| Z.ai and Zhipu BigModel | `GLM-4.7-Flash` and `GLM-4.6V-Flash` free; concurrency cap per model, `login`; BigModel registers with a phone number from any country | documented | `compute/z-ai-glm-flash`, `inference/zhipu-bigmodel-open-platform` |

Sign-up fields that the records mark `unverified` stay unverified here. No account was
created, so no keyed limit was measured.

## One-time and expiring credit with no card

These lanes give a stock of tokens once. The stock, not the rate, binds.

| Provider | Allowance | Record |
| --- | --- | --- |
| Inception Labs | 100 million tokens per new account | `inference/inception-labs` |
| BytePlus ModelArk | 500,000 tokens per model, one time | `inference/byteplus-modelark-free-tokens` |
| Tencent HY Text Generation Global | 1,000,000 tokens, `Hunyuan-translation` only, valid 1 year | `inference/tencent-hy-text-global` |
| AI21 Studio | USD 10 of credit for three months | `inference/ai21-studio` |
| Xiaomi MiMo | one-time credit; the amount is not stated | `inference/xiaomi-mimo-api` |
| StepFun | free credit of an unstated size; tier V0 allows 100 requests a minute and 500,000 tokens a minute | `inference/stepfun-open-platform` |
| Scaleway Generative APIs | 1,000,000 tokens and 60 minutes of audio; the rate limits apply with a payment method registered | `inference/scaleway-generative-apis` |

## What asks for a card, or closed

| Provider | State on 2026-10-28 | Record |
| --- | --- | --- |
| Cerebras | USD 5 after a verified payment method, 30 days; 5 requests a minute on the trial | `inference/cerebras` |
| AkashML | trial credit after a payment method is verified | `inference/akashml` |
| SambaNova | the no-card grant ended on 2026-08-14 | `compute/sambanova-cloud` |
| Together, DeepInfra, Parasail, Hyperbolic, Fluence | a card, a prepaid balance or a deposit before any call | `inference/together`, `inference/deepinfra`, `inference/parasail`, `inference/hyperbolic-inference`, `inference/fluence-inference` |
| AI/ML API | the free tier is paused | `inference/ai-ml-api` |
| Ollama Cloud, Cloudflare AI Gateway | no inference allowance of their own | `inference/ollama-cloud`, `inference/cloudflare-ai-gateway` |
| MiniMax, Meituan LongCat | no free allowance on the pages read | `inference/minimax-api-platform`, `inference/meituan-longcat-api` |
| Routeway | `:free` ids at 5 requests a minute and 200 a day on one page and 20 a minute on another; the terms list a payment method | `inference/routeway` |
| Vercel AI Gateway | USD 5 each 30 days per a 2025 launch post, and a payment method added to the team | `inference/vercel-ai-gateway` |
| Hugging Face Inference Providers | no credits on a free account | `inference/huggingface-inference` |
| OpenCode Zen free models | answered only from inside the OpenCode client | `inference/opencode-zen-free` |

## Closed or unreachable

| Provider | State on 2026-10-28 | Record |
| --- | --- | --- |
| Gemini CLI free route, Qwen OAuth, iFlow | closed on 2026-06-18, 2026-04-15 and 2026-04-17 | `inference/gemini-cli-free`, `inference/qwen-code-oauth`, `inference/iflow-api` |
| GitHub Models inference, KeylessAI, mlvoca, uncloseai | a 4-byte 200 body, a host that no longer resolves, a 502, and a 401 that says key registration is closed | `inference/github-models-inference`, `inference/keylessai`, `inference/mlvoca`, `inference/uncloseai` |
| ModelScope, Baidu Qianfan, Tencent Hunyuan China, Moonshot | a real-name check or a mainland phone number | `inference/modelscope-api-inference`, `inference/baidu-qianfan-modelbuilder`, `inference/tencent-hunyuan-api-cn`, `inference/moonshot-kimi-api` |
| Hack Club AI | accounts of people aged 18 and under | `inference/hack-club-ai` |

## What this document cannot tell you

**No keyed lane was called.** An account needs a sign-up, and no account was made. Every
keyed number is a vendor statement.

**Google and Mistral publish no number.** The values sit behind a login. A script cannot
read them, so neither lane has a limit in the records.

**Kilo Gateway and BlockRun have a documented limit that the records do not hold.** The
vendor pages state a per-IP figure for each. The record keeps its measured line `unpublished`,
because a documented value cannot replace a measured one. Read both records before you use
either lane.

**Free endpoints change in days.** Re-run the probe before you depend on a row.
