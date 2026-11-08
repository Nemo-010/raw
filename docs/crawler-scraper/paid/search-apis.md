# What does a search cost per thousand, and what is one result?

The paid search lane answers one question the free lane cannot: at what volume does a
free allowance become a bill, and what is the bill per unit. Every provider here sells
the same thing, which makes the class the easiest in the topic to compare: a price per
1,000 requests, and a rule about what counts as a request.

The answer: **the per-1,000 price spans 30 cents to 7 dollars, a thirtyfold range, and
almost none of that spread is quality.** Serper is USD 0.30 per 1,000 and SerpApi is
USD 7.25 per 1,000 at its Searcher tier. The platform's quality index measures neither.

Where quality is measured the range is narrower: Exa's lite mode at USD 4 per 1,000 and
Tavily at USD 8 per 1,000 cover a point spread of 65.6 to 79.2.

## The comparison

Sorted by price per 1,000 requests at the cheapest plan that includes API access.
`Unit` is what one request buys, because that is what makes the rows comparable.

| Provider | Cheapest paid plan | Per 1,000 | Unit | Verdict |
| --- | --- | --- | --- | --- |
| Serper | pay-as-you-go | USD 0.30 | one Google SERP | paid-only |
| Exa | pay-as-you-go | USD 4.00 lite, USD 7.00 auto | 10 results, then USD 1/1,000 each | paid-only |
| Keenable | pay-as-you-go | USD 4.00 | one search request | paid-only |
| Tavily | pay-as-you-go | USD 8.00 | one credit | paid-only |
| Perplexity | pay-as-you-go | USD 5.00, or USD 1.00 Fast | one successful POST /search | paid-only |
| Parallel | pay-as-you-go | USD 1.00 to USD 5.00 | 10 results | paid-only |
| Octen | pay-as-you-go | USD 1.00 promotional, USD 5.00 list | one call | paid-only |
| SerpApi | Searcher, USD 725 a month | USD 7.25 | one search | paid-only |
| web.pkgforge.dev | none: free | USD 0.00 | one search, 20 results | qualifies |

## Serper

USD 0.30 per 1,000 queries from the home page headline, against a Google SERP, with no
minimum stated. That is the cheapest search in this topic by an order of magnitude.

⚠ **The cheapness is the whole product and the quality is unmeasured.** The platform's
quality index does not list Serper. A price that is a tenth of the market's is a reason
to look at what is being sold, which here is a parsed Google result page.

Evidence: `serper.dev` (read 2026-10-22): "USD 0.30 per 1,000 queries", "No credit card
required".

Verdict: the cheapest per unit and the least measured. Worth a control call, not a
dependency.

## Exa

USD 4 per 1,000 for a lite search, USD 7 for auto and fast, USD 12 for deep, USD 15 for
deep-reasoning. The base price covers 10 results and each result above 10 is USD 1 per
1,000.

⚠ **`numResults: 20` is the base price plus ten results.** A caller that asks for 20
results to fill a wider table pays an extra result charge it did not see in the headline.

⚠ **`/contents` bills per content type.** One page with text and highlights is two
pages at USD 1 per 1,000 each.

Evidence: `exa.ai/pricing` (read 2026-10-22): "`/search` (`lite`) USD 4 / 1k requests";
"Each result above 10 USD 1 / 1k results"; "`/contents` USD 1 / 1k pages, per content
type".

Verdict: the best measured quality in the class at a mid price. The cheapest paid leg
worth depending on.

## Keenable

USD 4 per 1,000 requests pay-as-you-go after 100,000 free, cloud only, with a
self-serve agent storefront that sells access directly and takes many payment methods.

⚠ **The free tier is two orders of magnitude larger than the price implies.** 100,000
requests a month free at USD 4 per 1,000 means the free allowance is worth USD 400 a
month, and no other provider in this class gives away anything close.

Evidence: `keenable.ai/pricing` (read 2026-10-22): "100K free requests a month", then
"USD 4 / 1000 requests".

Verdict: the capacity answer. Its quality, 67.0 on the platform's index, is the reason
to pair it with Exa.

## Tavily

USD 0.008 per credit, which is USD 8 per 1,000, with a Project plan at USD 30 a month
for a larger allowance. One credit is one request of any type.

⚠ **Search, extract and crawl draw on one pool.** A mixed workload divides one
allowance, so the per-1,000 price applies to whichever mixture is actually run.

Evidence: `tavily.com/pricing` (read 2026-10-22): "USD 0.008 / credit"; "Project USD 30
/ month".

Verdict: mid price, mid quality (65.6 on the platform's index), and one pool for three
jobs.

## Perplexity

USD 5.00 per 1,000 search requests, USD 1.00 for Fast Search. A successful `POST
/search` is one billing unit whatever the number of queries in it, up to five.

⭐ **Five queries for one billing unit is the useful detail.** A request carrying five
queries at USD 5 per 1,000 is USD 1 per 1,000 per query, which is cheaper than every
other row here.

⚠ **A successful response is billed even when it returns no results.** Invalid,
rate-limited and upstream-failed requests are not billed, so a 200 with an empty result
set is.

Evidence: `docs.perplexity.ai/getting-started/pricing` (read 2026-10-22): "Search API
USD 5.00"; "A successful request containing an array of up to five queries is one
billing unit".

Verdict: the best per-query price in the class if a caller batches five queries, and the
second-best measured quality.

## Parallel

The Search API is USD 0.001 to USD 0.005 per request for 10 results, which is USD 1.00
to USD 5.00 per 1,000. The Task API is USD 0.005 to USD 2.40 a request, and the
difference is that a task can run for 25 minutes.

⚠ **The Search and Task prices are two orders of magnitude apart and the page presents
them in one table.** A caller that confuses a search with a task misreads the bill by
two hundredfold.

Evidence: `parallel.ai/pricing` (read 2026-10-22): "Price per request USD 0.005 to USD
2.4 [Task]; USD 0.001 to USD 0.005 for 10 results [Search]".

Verdict: a cheap search and an expensive deep-research task under one account.

## Octen

USD 1 per 1,000 calls on a promotional rate from USD 5 list, USD 0.50 per 1,000 results
for full content, with ten full-content results free per call.

⚠ **A promotional price is not a price.** The page shows USD 5 struck through and USD 1
beside it, which is a campaign and it ends. Plan on USD 5.

Evidence: `octen.ai/pricing` (read 2026-10-22): "$1 $5/ 1k calls, 80% Off"; "$0.5/ 1k
results (full content)"; "10 full-content results free per call".

Verdict: high quality (77.1 on the platform's index) at a list price of USD 5 per
1,000. The promotion makes it worth testing now.

## SerpApi

USD 725 a month for 100,000 searches, which is USD 7.25 per 1,000, with 20,000 an hour
throughput. The Free plan is 250 a month.

⚠ **The minimum spend is USD 725 a month.** This is the only provider in the class with
no pay-as-you-go entry, so the price per unit is irrelevant: the cheapest way to buy
one search is USD 725.

Evidence: `serpapi.com/pricing` (read 2026-10-22): "Searcher USD 725/mo, 100,000
searches/mo, 20,000 throughput/hr".

Verdict: the reference for what a guaranteed-throughput Google search costs, and
unreachable.

## web.pkgforge.dev

Free, and it is the cheapest row in the table by definition. Its 20-result clamp is the
only thing it does not do.

Evidence: `search.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version
`731c403806c8`): "free to every caller; no key, no account and no quota", with a spend
breaker at 100 requests a minute per caller IP.

Verdict: the lane. The paid rows exist for the query the free lane cannot answer, which
is a query that needs more than 20 results.

## What did not work

- **Perplexity as a free route**: no free tier; the Search API bills from the first
  call (`docs.perplexity.ai`, read 2026-10-22).
- **Brave Search at any price**: the dashboard answered `409` to a reader, so neither
  the free nor the paid figure could be confirmed here, and the platform's research
  records a card required in practice.
- **SerpApi below USD 725 a month**: the plan table has no cheaper paid entry, and the
  free plan is 250 searches.
- **A per-1,000 price as a per-result price**: Exa bills results above ten, Perplexity
  bills a request that may hold five queries, and SerpApi counts a 100-result response
  as one search. Three different units under one header.
- **A promotional rate as a budget**: Octen's USD 1 is a struck-through campaign from
  USD 5.

## Chaining

Search is the cheap half of a research task and reading is the expensive half. The
pattern that works: Keenable for coverage, Exa or Perplexity for the query that decides
a finding, and a reader for the page each one returns, which costs more per page than
the search that found it. See [`paid/reader-extractors.md`](reader-extractors.md).
