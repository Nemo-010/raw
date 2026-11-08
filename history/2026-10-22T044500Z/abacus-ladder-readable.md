# Abacus.AI's ladder was readable all along and has no free tier on it

- **When:** 2026-10-22T04:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/coding-subs/abacus-chatllm.json` (`confidence: unverified`, free tier "no first-party capture has ever priced this product")
- **Superseded by:** the same record, rewritten on 2026-10-22
- **Evidence:** `abacus.ai/pricing` read 2026-10-22T04:14:01Z (200, 144,207 bytes)
- **Confidence:** documented

## What we believed

The record said no first-party page had ever priced ChatLLM, and carried `unverified`.
The topic README listed Abacus among the dead ends on the strength of that.

## What we found

`abacus.ai/pricing` returns 200 with 144,207 bytes and the ladder is in the page title:
"ChatLLM Pricing | Basic $10, Pro $20 per user a month". Basic is USD 10 a user a month,
discounted to USD 7 for the first month, with 20,000 credits a month and **3 AI Agent
conversations a month**; Pro is USD 20 a user a month with 30,000 credits a month and
unrestricted Agent and CLI use.

So the seed's USD 10 figure was right and only its capture was missing. What was wrong
was the seed's framing: there is **no free tier** on the ladder, so the row was never a
free lane. The verdict stays `paid-only`, and the rung rises to `documented`.

The binding constraint is the one nobody would have guessed from the price: three Agent
conversations a month on Basic bind long before 20,000 credits do.

## How we found it

One fetch of `abacus.ai/pricing`, which the previous pass had not tried. It had tried
`abacus.ai/`, the marketing root.

## What it cost us

One row sat at `unverified` for a writing pass while its price was one URL away, and the
topic README counted it among the dead ends.

## What a future session should do differently

⭐ **Try `/pricing` before recording a product as unpriced.** A marketing root carries a
nav bar; the pricing path carries the ladder. The previous pass fetched the root, found
no plan, and wrote that no first-party page had ever priced the product, which was a
claim about the seed being mistaken for a claim about the vendor.
