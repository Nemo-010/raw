# The cheapest published rate, with the traffic mix stated

A per-token price is only comparable to another per-token price when the mix is the
same. One rate applies to input and another to output, and a third to a cache hit,
and the ratio between them differs by a factor of ten between vendors. A reader who
compares a headline input price against another headline input price is comparing two
numbers that will not describe their workload.

This document states the rates found, names the mix each conversion assumes, and marks
how far each rate is from being verified here.

The answer: **DeepSeek's off-peak cache-read rate is the cheapest published figure in
this market, and its cache-hit rate is roughly fifty times its miss rate**, which
makes prompt caching the largest single lever available (`reported`, third-party
summary of the vendor page; the vendor page did not render its price table to any
route tried on 2026-10-22).

## The comparison

Sorted by the input rate. `Verified` says how the number was obtained, because a rate
read off a vendor page and a rate read off a blog are different kinds of claim.
`Mix` states the ratio the per-month conversion assumes.

| Vendor and model | Input per 1M | Output per 1M | Cache read per 1M | Verified | Verdict |
| --- | --- | --- | --- | --- | --- |
| DeepSeek V4.1 Flash, off-peak | USD 0.15 | USD 0.60 | USD 0.003 | reported | paid-only |
| DeepSeek V4.1 Flash, peak | USD 0.30 | USD 1.20 | USD 0.006 | reported | paid-only |
| OpenCode Go, GLM-5.3-Flash | USD 0.15 | USD 0.50 | USD 0.03 | documented | qualifies-with-caveat |
| OpenCode Go, GPT 6 Luna | USD 0.10 | USD 0.50 | USD 0.01 | documented | qualifies-with-caveat |
| OpenCode Go, Claude Haiku 5.5 | USD 0.10 | USD 0.50 | USD 0.01 | documented | qualifies-with-caveat |
| OpenCode Go, DeepSeek V4.1 Flash off-peak | USD 0.15 | USD 0.60 | USD 0.003 | documented | qualifies-with-caveat |
| Cloudflare Workers AI, deepseek-v4.1-flash | USD 0.30 | USD 1.20 | USD 0.006 | documented | qualifies-with-caveat |
| DeepSeek V4 Pro, off-peak | USD 0.66 | USD 1.98 | USD 0.022 | reported | paid-only |
| Cursor, Composer 2.5 | USD 0.50 | USD 2.50 | USD 0.20 | documented | paid-only |

## DeepSeek

DeepSeek serves two models, `deepseek-flash` and `deepseek-v4-pro`, over OpenAI and
Anthropic compatible base URLs (`documented`, `api-docs.deepseek.com`, read
2026-10-22). The naming changed: `deepseek-flash` is now served by
DeepSeek-V4.1-Flash-1017, and the legacy names `deepseek-v4-flash` and
`deepseek-v4-flash-vision-exp` are accepted but their models are retired and their
requests are billed at the Flash price.

The rate table itself did not render through any extraction route tried today, so the
figures in the table above are third-party and are labelled `reported`. Four
independent third-party summaries agree on the shape: USD 0.30 input and USD 1.20
output at peak, USD 0.15 and USD 0.60 off-peak, with cache reads at about two per cent
of the input price; peak is stated as Monday to Friday, 01:00 to 04:00 and 06:00 to
10:00 UTC.

⛔ **A rate whose source did not render is `reported`, not `documented`.** The
distinction matters here because the off-peak rate is the cheapest number in this
document and the whole paid case for DeepSeek rests on it.

## The cache ratio is the lever, not the headline

Across every row in the table, the cache-read price is between one-fiftieth and
one-seventh of the input price. DeepSeek's off-peak cache read at USD 0.003 against
its input at USD 0.15 is a factor of fifty.

For an agent workload that sends a long system prompt and a large code context with
every turn, the cached portion dominates the input tokens, so the effective input rate
is closer to the cache rate than to the headline. That is why the cheapest arithmetic
uses the cache-read price rather than the input price, and why a comparison that
ignores caching overstates every vendor's cost by an order of magnitude.

It also means a cheap vendor with no caching is not cheap for this workload. Of the
rows above, Cloudflare's `deepseek-v4.1-flash` is the same model as DeepSeek's own
`deepseek-flash` at twice the input price, so the only reason to buy it there is a
platform already in use.

## The mix, stated

A monthly cost cannot be computed from a price table alone. It needs the input-to-
output ratio and the fraction of input that hits cache, and those are properties of
the workload rather than of the vendor.

Two mixes are used, and both are labelled where they appear. A one-to-one
input/output ratio at full cache is an upper bound that no workload reaches and it is
useful only as a bound. A ninety-seven per cent input mix with a high cache hit rate
describes a coding agent and is the one used for the arithmetic here.

A rate per million tokens with no mix beside it is not a cost.

## What did not work

- **Reading DeepSeek's rate table.** Four routes returned the model-naming page and
  not the price table, including the `.md` variant and the firecrawl provider.
- **Comparing input prices across vendors.** The output-to-input ratio ranges from 2.5
  to 5 between the rows above, so the ranking changes with the mix.
- **Ignoring cache.** A vendor with no cache is between seven and fifty times more
  expensive than the table suggests for an agent workload.

## Chaining

The cheapest paid path is a subscription with a published dollar ceiling, compared
against the same model at the vendor's own API price. OpenCode Go publishes both sides
of that comparison for DeepSeek V4.1 Flash, which is the one place in these two topics
where a subscription and a per-token rate can be checked against each other with
arithmetic rather than trust.
