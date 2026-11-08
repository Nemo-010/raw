# What an email address buys, and why the numbers are not public

A keyed free tier is the mainstream offer: an account, an API key, and a published
rate limit. It is a different class from the anonymous endpoints in
`keyless-anonymous.md` for one reason that decides the answer: a key makes the quota
per account rather than per IP, so it survives a change of address and it does not
collide with whatever else was calling from that address.

The cost is an identity, and an email address is the cheapest kind. The problem is a
different one. **Most of these vendors do not publish the number that matters on a
page a reader or a script can see.** Google's free-tier limits are visible only inside
AI Studio after signup. Mistral's values sit behind a login too. OpenRouter's
thresholds read in the served page (see the OpenRouter section). Groq does publish a
per-model table, and it is the exception that proves the rule is about disclosure
rather than about the web.

The answer: **Groq is the best-documented free tier in this class, and its free numbers
are readable in the served page** (`documented`, 2026-10-22). It names six limit
dimensions, states that the first one reached binds, and prints a two-plan per-model
table whose Free column a reader can act on: 30 requests a minute, 1,000 requests a
day, 8,000 tokens a minute and 200,000 tokens a day on `openai/gpt-oss-120b`. That is
the only absolute, checkable free allowance in this topic, and it is 11.4 per cent of
a 52.5M-token monthly target.

## The comparison

Sorted by how much of the quota is publicly stated. `Dimensions` is how many separate
limits the vendor names, which matters more than any single number because a pipeline
sized on one dimension meets another.

| Provider | Free tier | Dimensions | Public number | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Groq | a Free Plan per model | 6: RPM, RPD, TPM, TPD, ITPM, OTPM | yes: 30 rpm, 1K rpd, 8K tpm, 200K tpd on gpt-oss | REST | email | qualifies-with-caveat |
| Google Gemini API | gemini-3.8-flash free of charge | 3 or 4: RPM, TPM, RPD, sometimes TPD | no: visible only in AI Studio | REST | email | qualifies-with-caveat |
| OpenRouter | `:free` ids only | 2: requests a minute, requests a day | yes: 20 rpm; 50 rpd under 10 credits bought, 1,000 rpd from 10 | REST | email | qualifies-with-caveat |
| Mistral | a free API tier, `restrictive` | 2: requests per second, tokens per minute and month | no: per-workspace, behind `admin.mistral.ai` | REST | email | qualifies-with-caveat |
| Cerebras | a trial after a payment method: USD 5, 30 days | RPM, TPM, TPH, TPD | yes: 5 rpm on `gpt-oss-120b` | REST | card | trial-only |
| DeepInfra | none: a card or a prepaid balance first | concurrent requests per model | yes: 200 concurrent per model | REST | card | paid-only |
| Together | none: a prepaid purchase of USD 15 first | not read | not applicable | REST | card | paid-only |
| Hugging Face Inference | none on a free account | monthly, for PRO and organisations | yes: PRO and Team or Enterprise only | REST | card | paid-only |

Seven of the eight were not called, and the reason is the same for each: no key was
available. Each is recorded as skipped with the variable named rather than sent
unauthenticated, because a 401 from a missing key and a 401 from a revoked key are
different facts.

## Groq

Groq's rate-limit page names six dimensions: requests per minute, requests per day,
tokens per minute, tokens per day, input tokens per minute and output tokens per
minute, with additional ASH and ASD figures (`documented`,
`console.groq.com/docs/rate-limits`, read 2026-10-22). Limits apply at **organisation
level rather than per user**, every dimension is evaluated, and the first threshold
reached binds. Cached tokens do not count toward any of them.

That design is the most complete in this class and it is also the reason a single
number cannot describe Groq. A workload of many short prompts meets RPM; a workload
of few long prompts meets TPM first. The vendor is telling a reader that the answer
depends on the traffic shape, which is true and which no marketing page says.

**The per-model free table is in the served HTML**, under a `Free Plan Limits` tab
beside `Developer Plan Limits`. Seven models carry a row, and the two a coding
workload would use are the two `gpt-oss` ids (`console.groq.com/docs/rate-limits`, read
2026-10-22):

| MODEL ID | RPM | RPD | TPM | TPD |
| --- | --- | --- | --- | --- |
| `openai/gpt-oss-120b` | 30 | 1K | 8K | 200K |
| `openai/gpt-oss-20b` | 30 | 1K | 8K | 200K |
| `openai/gpt-oss-safeguard-20b` | 3 | 1K | 2K | 200K |
| `qwen/qwen3.8-27b` | 30 | 1K | 8K | 200K |
| `meta-llama/llama-prompt-guard-2-22m` | 30 | 14.4K | 15K | 500K |
| `meta-llama/llama-prompt-guard-2-86m` | 30 | 14.4K | 15K | 500K |
| `canopylabs/orpheus-v1-english` | 10 | 100 | 1.2K | 3.6K |

So Groq is not the class's unreadable case. It is the one keyed tier in this topic with
an **absolute, checkable free allowance**, and the allowance is small. On
`openai/gpt-oss-120b` the daily token ceiling is 200,000, so 37.5M output tokens a
month would take 187.5 days at the free allowance. The 8,000-tokens-a-minute figure
allows 15M input tokens in 31.2 hours of sustained use, which reads generous until the
daily cap is applied over it.

⛔ **The binding dimension is TPD, not RPM and not TPM.** Thirty requests a minute and
8,000 tokens a minute are both workable for an interactive session. Two hundred
thousand tokens a day is 6 million a month against a 52.5M-token monthly target, which
is 11.4 per cent of it.

Evidence: `console.groq.com/docs/rate-limits` (read 2026-10-22): the six dimensions,
the organisation scope, the first-reached rule and the seven-row free-plan table with
its RPM, RPD, TPM and TPD columns. Verdict: the best-specified free tier here, the only
keyed one with a readable number, and too small to carry the workload.

## Google Gemini API

`gemini-3.8-flash` is free of charge for input and output on the Free Tier
(`documented`, `ai.google.dev/gemini-api/docs/pricing`, read 2026-10-22). The limits
are RPM, input TPM and RPD, applied **per project rather than per API key**, with RPD
resetting at midnight Pacific.

The binding fact is that the per-model numbers are served only at
`aistudio.google.com/rate-limit`, after signup. So any catalogue that prints "15 RPM,
1,500 RPD" for a Gemini free tier is quoting a third party and not Google. The
vendor's own page states that the limits vary by model and that some models carry a
TPD as well.

Two exclusions matter and both are on the page: Gemini 4 Argon is not available on the
free tier, and free-tier content is used to improve the vendor's products while the
paid tier is the one described as being for production.

Evidence: `ai.google.dev/gemini-api/docs/rate-limits` (read 2026-10-22): per-project
scope, midnight Pacific reset, and "Specified rate limits are not guaranteed". Verdict:
a real free tier on a model that is genuinely free, with the numbers behind a login.

## OpenRouter

OpenRouter's free-model limits apply only to model IDs **ending in `:free`**, and the
tier is selected by all-time credits purchased (`documented`,
`openrouter.ai/docs/api-reference/limits`, read 2026-10-22). `GET /api/v1/key`
reports `free_model_daily_requests` with a `limit` and a `remaining` field, and the
documentation says the per-minute cap is not reported there.

The limits table reads in the page on 2026-10-28: 20 requests a minute for every free
id, then 50 requests a day under 10 credits bought all time, or 1,000 requests a day from 10
credits (`documented`, `openrouter.ai/docs/api-reference/limits`). The daily window is the UTC
day and the 50 a day is a total across all free ids.

⛔ **The `:free` suffix is the whole rule.** `inclusionai/ling-3.1-flash` is priced at
zero and does not end in `:free`, so the free-model caps do not apply to it. A model
priced at zero without the suffix is a different quota class.

A live call to that id without a key returned `401 {"message": "No cookie auth
credentials found"}` in both runs, which proves the endpoint exists and gates on a key.

Evidence: `openrouter.ai/docs/api-reference/limits` (read 2026-10-22) and two
unauthenticated probes. Verdict: the clearest gating rule in the class and no readable
number.

## Mistral, Cerebras, DeepInfra, Together

These four were discovered and not measured. No key existed in the environment, so
each is recorded with the environment variable that was unset rather than sent
unauthenticated.

What is known about each is thin and is labelled as such. Mistral's free API tier is real and its
values are not public: the documentation path that described it returns 404 today, and
the archived copy states only that the tier exists with "restrictive rate limits" and that
the numbers live at `admin.mistral.ai/plateforme/limits` behind a login. Limits are set
per workspace, not per key. **Cerebras has no permanently free tier**: its rate-limits page
answers "Is there a permanently free tier?" with "No", and the offer is USD 5 of credits
that expire in 30 days after a verified payment method is added. DeepInfra and
Together ask for a card or a prepaid balance before any call, so both read paid-only on
2026-10-28.

Each of the four answers an unauthenticated call with a distinguishable 401 body:
`{"detail":"Invalid API Key"}` for Mistral and `{"error":{"message":"Invalid API
Key"...}}` for Groq. Hugging Face's router is the exception and it matters: it returns
a 401 disguised as an HTML document, so a probe that classifies on body shape rather
than status mis-handles it.

## What did not work

- **Reading a number off two of these pages.** Google and Mistral state a limit dimension
  and not a value, and show the values only after login.
- **Treating an unauthenticated 401 as a dead endpoint.** A 401 proves the endpoint
  exists and gates. Recording it as dead is how a live service gets written off.
- **A single rate for Groq.** Six dimensions with a first-reached rule cannot be
  summarised as one figure without discarding the vendor's own warning.

## Chaining

A keyed free tier is the fallback for a keyless stack. When OVH's two-a-minute ceiling
binds, a Gemini or Groq key removes the per-IP sharing and replaces it with a
per-account allowance that a change of address does not reset. The trade is an email
address and a number that has to be read from inside the vendor's console rather than
from this document.
