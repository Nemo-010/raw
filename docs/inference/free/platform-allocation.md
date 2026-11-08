# An allowance attached to a platform you already use

Some inference is not sold. It arrives attached to a platform the reader already
holds an account on, denominated in the platform's own unit, and metered on the
platform's own clock. AWS, Cloudflare, GitHub, Kaggle and Colab all do
this, and the allowance is usually the smallest number in the whole topic because the
inference is a feature of the platform rather than a product.

The class is worth separating because its failure mode is different. A platform
allocation does not get repriced, it gets **quietly narrowed**: models move to a
paid-only list, an equivalent is published in a unit that is not tokens, and the
allowance keeps its old size in the old unit.

The answer: **Cloudflare Workers AI is the cleanest published allocation found:
10,000 Neurons a day, reset at 00:00 UTC, priced in the vendor's own unit**
(`documented`, 2026-10-22). The allowance is 300,000 Neurons a month, which buys
122.1 million input tokens on the cheapest 1B model and 5.0 million on the dearest
model the free plan can reach. It is a fallback, not a primary: it covers 42 per cent
of a 15M-input, 37.5M-output monthly workload and none of the output half. The unit
also makes a single USD-per-token figure impossible, which is why that figure should
not be quoted.

## The comparison

Sorted by how completely the allocation is stated. `Unit` is what the vendor meters,
because a neuron, a credit and a GPU-hour are not convertible.

| Provider | Free allocation | Unit | Reset | Paid-only models named | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Cloudflare Workers AI | 10,000 Neurons a day | Neurons | 00:00 UTC daily | yes, eight of them | email | qualifies-with-caveat |
| Hugging Face Inference | none on a free account | credits | monthly, for PRO and organisations | not read | card | paid-only |
| Kaggle Notebooks | 30 GPU hours a week | GPU-hours | weekly | n/a | any-phone | qualifies-with-caveat |
| GitHub Models | a per-model request allowance | requests | daily | n/a | email | qualifies-with-caveat |
| Google Colab | a free GPU session | wall-clock | daily | n/a | email | qualifies-with-caveat |

## Cloudflare Workers AI

Workers AI gives 10,000 Neurons a day at no charge on both the Workers Free and the
Workers Paid plan, with any usage above that billed at USD 0.011 per 1,000 Neurons on
a paid plan, and all limits resetting daily at 00:00 UTC (`documented`,
`developers.cloudflare.com/workers-ai/platform/pricing/`, read 2026-10-22). Past the
limit, operations fail with an error.

Two things the pricing page states that a summary usually drops, and both narrow the
allocation:

- **Per-model unit prices are printed, but billing is in Neurons.** The page presents
  a "price in tokens" column beside a "price in neurons" column as an equivalence,
  so a USD-per-million figure is derivable per model and there is no single figure for
  Workers AI. `@cf/meta/llama-3.3-70b-instruct-fp8-fast` is 26,668 neurons per million
  input tokens; `@cf/deepseek-ai/deepseek-v4-flash-0731` is 40,000.
- **Eight named models require a paid billing method**, including
  `@cf/moonshotai/kimi-k2.6`, `@cf/zai-org/glm-5.3` and three DeepSeek ids. A claim
  that Workers AI is free that does not exclude those is wrong.

Rate limits are per task type rather than per model by default: **300 requests a minute
for text generation**, unless the model requires the Workers Paid plan, with per-model
overrides and lower figures on beta models (`developers.cloudflare.com/workers-ai/platform/limits/`,
read 2026-10-22). The 3,000-a-minute figure on the same page belongs to image
classification, object detection and text embeddings, which are three other task types.
The eight paid models carry 20 requests a minute on standard billing and 50 with prepaid
AI Gateway credits, per account and per model.

So 10,000 Neurons a day is **300,000 Neurons a month**, and the arithmetic from there is
what decides the row. At 2,457 neurons per million input tokens, the rate for
`@cf/meta/llama-3.2-1b-instruct`, that is **122.1 million input tokens a month**, or
4.07 million a day. At 1,542 neurons per million, the cheapest input rate on a model
the free plan can reach (`@cf/ibm-granite/granite-4.0-h-micro`), it is 194.6 million
tokens a month. At 60,000 neurons per million, the dearest free-plan input rate
(`@cf/qwen/qwq-32b`), it is 5.0 million a month. The free-plan input spread is a factor
of 38.9.

That is a real allowance and it is not a large one. A workload of 15 million input and
37.5 million output tokens a month on `llama-3.2-1b-instruct` costs
15 x 2,457 + 37.5 x 18,252 = **721,305 neurons**, which is 2.4 times the whole free
monthly allocation. The input half alone is 12 per cent of it. The output half alone is
2.3 times it. ⛔ **Workers AI on a free account cannot carry that workload**, and the
recommendation below is a fallback for a quiet period rather than a plan.

Evidence: `developers.cloudflare.com/workers-ai/platform/pricing/` and
`/platform/limits/` (both read 2026-10-22). Verdict: the cleanest allocation here,
narrowed by a paid-only model list that excludes the models a reader most wants.

## Hugging Face Inference

Hugging Face sells Inference Providers as a router over third-party endpoints at
`router.huggingface.co/v1`. **A free account gets no monthly credits.** The pricing
documentation states that "PRO users and Team or Enterprise organizations receive
monthly credits to use with Inference Providers" and that "Free users can use Inference
Providers by purchasing credits, or by upgrading to PRO"
(`huggingface.co/docs/inference-providers/pricing`, read 2026-10-22). The eligibility
table is explicit: Free Users, "yes (credits purchase required)".

So this is not a platform allocation. It is a paid product with a free door, and the
door is a payment method. The identity cost is a card, not an email.

The router's unauthenticated response is still worth recording: it returns a **401
disguised as an HTML document**, not JSON, with a 3,087-byte body. A probe that
classifies on body shape rather than on status mis-handles this endpoint, and that is a
defect in the probe rather than in the provider.

Hugging Face also appears in the compute topic as a Jobs container provider at about
USD 0.50 a month. That is a different product on the same account, and this document
does not restate it.

## Kaggle and Colab

Both are notebook platforms whose free allowance is GPU time rather than an API. They
are listed here because the boundary with
[`self-hosted-on-free-compute.md`](self-hosted-on-free-compute.md) runs through them:
Kaggle's 30 GPU hours a week and Colab's free session can serve a model over an
OpenAI-compatible shim, at which point the platform allocation becomes an inference
endpoint.

The numbers and the session clocks belong to the compute topic, which owns the
machine. This document owns only the fact that the resulting endpoint is reachable
from a script.

## What did not work

- **A single USD per million tokens for Workers AI.** The unit is Neurons and the
  per-token column is an equivalence that changes with the model.
- **Treating the free allocation as covering every model.** Eight named models are
  paid-only, and three of them are the ones a coding workload would want.
- **Assuming a platform allocation renews on a month.** Cloudflare's resets daily,
  which is a shorter clock than any subscription in this corpus.

## Chaining

A platform allocation is the smallest and most reliable tier in a stack: it is
attached to an account the reader already has, it does not expire, and it does not
get withdrawn the way a keyless endpoint does. It is too small to be the primary and
good enough to be the fallback that never stops working.
