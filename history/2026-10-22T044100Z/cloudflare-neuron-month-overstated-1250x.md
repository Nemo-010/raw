# Cloudflare's free allowance was overstated 1,250 times, and the conclusion built on it was void

- **When:** 2026-10-22T04:41:00Z
- **Status:** corrected
- **Supersedes:** `docs/inference/free/platform-allocation.md` §Cloudflare Workers AI, the sentence "So 10,000 Neurons a day is roughly 375 million neurons a month"; `dossier/inference/cloudflare-workers-ai.json`
- **Superseded by:** the same document's §Cloudflare Workers AI and the same record, both rewritten on 2026-10-22
- **Evidence:** `developers.cloudflare.com/workers-ai/platform/pricing/` and `.../platform/limits/`, both read 2026-10-22; capture `.tmp/work/fx-coding-inference/ev/<sha1 of url>.body`, 128,565 and 121,998 bytes
- **Confidence:** documented

## What we believed

The document stated that 10,000 Neurons a day is "roughly 375 million neurons a
month", and drew from that a conclusion that Workers AI's free allocation was a
large token figure: 152 billion input tokens a month at 2,457 neurons per million.

## What we found

10,000 x 30 is **300,000**. The document multiplied by 1,250 instead of by 30 and
never wrote the multiplication out, so nothing in the sentence could be checked
against itself. The error overstates the free allowance by a factor of 1,250.

The corrected arithmetic, with the ranges computed from the 39 text-generation
models on the pricing page rather than asserted:

| quantity | value |
| --- | --- |
| free allowance a month | 300,000 Neurons |
| input tokens at 2,457 neurons/M (`llama-3.2-1b-instruct`) | 122.1M a month, 4.07M a day |
| input tokens at 1,542 neurons/M (`granite-4.0-h-micro`, cheapest free-plan input) | 194.6M a month |
| input tokens at 60,000 neurons/M (`qwq-32b`, dearest free-plan input) | 5.0M a month |
| free-plan input spread | a factor of 38.9 |

The old sentence also claimed the spread between cheapest and dearest model was "a
factor of about fifty". Across the 31 models the free plan can reach it is 38.9; across
all 39 including the eight paid-only ids it is 82.5. Neither is fifty.

**The conclusion did not survive.** The target workload of 15M input and 37.5M
output tokens a month on `llama-3.2-1b-instruct` costs 15 x 2,457 + 37.5 x 18,252 =
**721,305 neurons**, which is 2.4 times the whole free monthly allocation. The input
half alone is 12.3 per cent of it; the output half alone is 2.28 times it. Workers AI on
a free account cannot carry the target workload, and the row is now stated as a fallback
rather than as a plan.

A second number in the same section was wrong in the same direction. The document said
"about 3,000 requests a minute for text generation". The limits page says **300** for
Text Generation; 3,000 is the figure for image classification, object detection and text
embeddings. A reader sizing a pipeline on 3,000 would have designed for 10 times the
ceiling.

## How we found it

An adversarial review re-read both vendor pages and did the multiplication. The review's
figure was checked here by re-fetching both pages and parsing every per-model neuron
rate out of the pricing table, then recomputing each derived quantity from the captured
bytes rather than from the review's prose.

## What it cost us

The inference topic's platform-allocation document carried a false conclusion in its
first paragraph for the length of one writing pass, and the topic README carried the
same 3,000-rpm error in its comparison table. Both were corrected before commit.

## What a future session should do differently

⛔ **Write the multiplication out inside the sentence that states the result.** "10,000 a
day is 300,000 a month" is checkable in two seconds; "roughly 375 million a month" is
checkable only by someone who already doubts it. A derived figure with no visible
derivation is the shape this error took, and it is the shape every arithmetic error in
this corpus will take.
