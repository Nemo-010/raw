# Which search API do I call, and in what order?

A search API answers one question: which pages exist for this query, as a list of URLs
with a snippet. The class is large and most of it is small. Nineteen vendors are
covered. Four carry anything a reader can use for research: Keenable at 100,000 requests
a month, Exa at USD 10 a month, TinyFish at 500 requests an hour, and the broker's own
search host, which is free and needs no account.

The answer: **use the broker, and treat every direct provider as a fallback.** The
broker decides which upstream to ask, reranks the results, and costs nothing. Its limit
is 20 results a query, which is a research limit and not a problem.

## The comparison

Sorted by what a reader can use tonight. `Ceiling` is the free allowance in the
provider's own unit. `Binds` is the constraint that fails first.

| Provider | Ceiling | Binds | Identity | Verdict |
| --- | --- | --- | --- | --- |
| web.pkgforge.dev search | free, 20 results a query | `request-rate`: 100 requests a minute per IP (the server's breaker, not a caller's pace), and a 300 s cache | anonymous | qualifies |
| Keenable | 100,000 requests a month | `request-rate` | email | qualifies |
| Exa | USD 10 a month, reset monthly | `request-rate`: about 2,500 lite searches | email | qualifies-with-caveat |
| TinyFish | 500 search requests an hour | `request-rate`: three windows, and the hour binds | email | qualifies-with-caveat |
| Tavily | 1,000 credits a month | `request-rate` | email | qualifies-with-caveat |
| You.com keyless | 100 queries a day | `request-rate`, and the MCP shape | anonymous | qualifies-with-caveat |
| Serper | 2,500 queries on signup | `request-rate`: the grant is one-time and does not renew | email | qualifies-with-caveat |
| SerpApi | 250 searches a month, 50 an hour | `request-rate`: 8 a day | email | qualifies-with-caveat |
| Octen | USD 5 balance | `request-rate`: the grant is one-time and does not renew | email | trial-only |
| Parallel | 5,000 requests a month | `request-rate`: the allowance survives only while a card is on file | card | qualifies-with-caveat |
| Perplexity | none | `request-rate`: every request is billed from the first | card | paid-only |
| Brave Search | USD 5 a month | `request-rate`, behind a dashboard that needs a card | card | fails-identity |
| Cloudflare Workers AI | 10,000 Neurons a day | `request-rate`: a spent allocation turns the rerank off | email | qualifies-with-caveat |

## web.pkgforge.dev search

One query goes to one upstream provider, chosen by tier, mode and health, and the result
is a normalised `results[]`. Unpinned calls answered from Exa. The free ceiling is the
whole service: no key, no account, no quota. What binds is 100 requests a minute per
caller IP, and a cache that answers an identical query from 300 seconds ago with
`x-web-cache: hit`. The breaker is the server's; a research agent does not pace to it
and reacts only to its 429 and Retry-After (`AGENTS.md` section 2 rule 15).

Two parameters do the work. `include_domains` sends a host filter to the provider and
skips any provider that cannot apply it, which is how to favour primary sources.
`count` above 20 is clamped and the answer says so in `x-web-count-clamped`.

`empty[]` names the providers that answered nothing, which is the difference between
"no results exist" and "the query was refused". One query over an impossible domain
answered with `empty: [exa, perplexity, octenai, parallelai]` (measured 2026-10-22).

Evidence: `search.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version
`731c403806c8`): `count` clamps at 20, `q` is at most 400 characters, a cache hit is
300 seconds old, and `empty[]` names each provider that answered none.

Verdict: the default. Read [`free/broker.md`](broker.md) for the rest of its use.

## Keenable

100,000 requests a month and then USD 4 per 1,000, cloud only, with the agent-facing
storefront at `zeroclick.keenable.ai` selling access directly. That is the largest
recurring general-web search allowance found in this topic, by two orders of magnitude
over Tavily's 1,000.

The measured quality is mid-table. The platform's research corpus ranks Keenable's
`pro` mode at 67.0 on a 100-point index where Exa's lite mode is 79.2.

⚠ **The tier is documented and the endpoint is not probed.** No call was made against
Keenable's own API; a guessed `/search` path answered `404`, and the record is
`qualifies-with-caveat` for that reason. A vendor page that states a tier is not a probe
of the read path.

Evidence: `keenable.ai/pricing` (read 2026-10-22): "Start searching with 100K free
requests a month", then "USD 4 / 1000 requests" pay as you go. `keenable.ai/` reads at
`200`, 4,528 bytes, 502 words, `upstream_status: 200` (measured 2026-10-22).

Verdict: the capacity answer for a search sweep, with an unprobed endpoint named. Its
quality is the reason to use it for coverage and not for the one query that decides a
finding.

## Exa

USD 10 of credit the day you sign up, and the balance resets to USD 10 on the first of
every month with no payment method. A lite search is USD 4 per 1,000, so the month is
about 2,500 searches. Auto and fast are USD 7, contents USD 1 per 1,000 pages, answer
USD 5, monitors USD 15.

The resetting balance is the feature. A credit that renews monthly is a tier; a
credit that arrives once is a trial, and most of this market sells the second.

Two billing details catch a caller. A base price covers up to 10 results and each
result above 10 is USD 1 per 1,000, so `numResults: 20` costs the base plus ten
results. `/contents` bills each content type separately, so one page with text and
highlights is two.

Evidence: `exa.ai/pricing` (read 2026-10-22): free tier is USD 10 of credit, reset to
USD 10 monthly, no payment method; lite USD 4 per 1,000 requests; each result above
10 is USD 1 per 1,000.

Verdict: the best measured quality in the class and the smallest recurring dollar
allowance. Use it for the query that matters.

## TinyFish

Search is free with two windows at once: 30 requests a minute and 500 an hour. Fetch
is free at 150 URLs a minute and 1,000 URLs a day. Agent and Browser are paid per step
and per minute.

⚠ **500 an hour is not 12,000 a day.** The platform's research corpus records 12,000
searches a day, which is 500 an hour sustained for all 24 hours. The published hour
cap is the number a design meets, and 30 a minute is 1,800 an hour, so the hour
window is the one that binds.

Evidence: `tinyfish.ai/pricing` (read 2026-10-22): "Search Free, Limits: 30 requests /
min, 500 requests / hour"; "Fetch Free, Limits: 150 urls / min, 1,000 urls / day".

Verdict: the largest free search volume that renews daily, at a quality of 71.2 on
the research corpus's index.

## Tavily

1,000 credits a month, no card, reset on the first of the month, and requests stop
when the credits are spent until the reset. USD 0.008 a credit pay-as-you-go, or USD
30 a month for the Project plan.

⚠ **A credit is not a search.** The pricing page states credits are consumed by
request type, search, extract or crawl, so 1,000 credits is 1,000 searches only if
every call is a search.

Evidence: `tavily.com/pricing` (read 2026-10-22): "You start with 1,000 free API
credits per month with no credit card required", reset on the first day of each
month.

Verdict: a small, reliable keyed leg. Its keyless sibling is the last resort and holds
for 600 seconds when it rate limits.

## You.com keyless

100 Web Search queries a day through a hosted MCP server with no API key, no account
and no credit card. The paid path is USD 5 per 1,000 calls with no minimum.

This is the only search route in the topic with a stated daily number and no identity
at all. It is MCP rather than a plain HTTP search endpoint, so it needs an MCP client
and cannot be called with a bare `curl` GET.

Evidence: `you.com/pricing` (read 2026-10-22): "No API key, no account, no credit
card", "100 Web Search API queries/day via MCP". Record
`dossier/crawler-scraper/youdotcom.json`, `documented`, `qualifies-with-caveat`,
binding `request-rate` at 100 queries a day.

Verdict: the one anonymous daily search allowance. Worth an MCP client if a session
has one.

## Serper

2,500 queries on signup, one-time, and USD 0.30 per 1,000 thereafter from the home
page headline. It bills against a Google SERP, which makes it the right control when a
broker result looks wrong: a second engine either confirms the page exists or does
not.

⚠ **The signup grant is a trial.** It does not renew, so a sweep planned on 2,500
queries works once. `/pricing` answers 404 to the reader, so the per-1,000 figure is
the home page's own claim and not a rate card.

Evidence: `serper.dev` (read 2026-10-22): "USD 0.30 per 1,000 queries" and "No credit
card required". The 2,500 grant is `reported` from the platform's research corpus.

Verdict: a one-time control. Not a lane.

## SerpApi

250 searches a month and 50 an hour on the Free plan, and USD 725 a month for 100,000
searches at 20,000 an hour on Searcher. Only successful searches count, and a response
with 100 results costs the same as an empty one.

250 a month is 8 a day. That is a monitoring allowance, not a sweep.

Evidence: `serpapi.com/pricing` (read 2026-10-22): Free plan USD 0 with 250
searches/mo and 50/hour throughput.

Verdict: a price reference for a Google-backed search at volume, which is the ceiling
a free tier is measured against.

## Octen

USD 5 of balance on signup and then pay-as-you-go or a QPS subscription. One-time.
The quality is high, 77.1 on the research corpus's index, which makes the USD 5 worth
spending deliberately rather than on a broad sweep.

Evidence: `octen.ai/pricing` (read 2026-10-22): "Sign up and get USD 5 in free
balance".

Verdict: a trial with good quality. Spend it on the hard query.

## Parallel

5,000 requests a month free, with a Search API at 200 ms to 3 seconds and a Task API
from 5 seconds to 30 minutes. The Search API costs USD 0.001 to USD 0.005 a request
for 10 results.

⚠ **The identity cost is a card, and the page read here does not say so.** The
allowance is real and the card requirement is inherited from the platform's research
corpus. That turns a free tier into a payment relationship, so the tier is
unreachable without a card.

Evidence: `parallel.ai/pricing` (read 2026-10-22): "Run up to 5,000 requests per
month for free". Identity cost: `reported`.

Verdict: unreachable without a card.

## Perplexity

No free tier. The Search API is USD 5.00 per 1,000 requests and Fast Search USD 1.00,
billed per successful `POST /search` whatever the number of queries inside it.

Evidence: `docs.perplexity.ai/getting-started/pricing` (read 2026-10-22): "Search API
USD 5.00", "one billing unit" per successful request.

Verdict: paid-only. Ranks second on the research corpus's quality index, which is
exactly why its absence of a free tier is worth recording.

## Brave Search

USD 5 of credits a month, with the page also stating up to USD 20, at 50 QPS on
search. The dashboard answered `409` to a reader fetch on 2026-10-22, so the figure
could not be confirmed here, and the research corpus records a card as required in
practice.

Evidence: `api-dashboard.search.brave.com` (read 2026-10-22): `409`, the page is
behind an authenticated dashboard. The allowance is `reported`.

Verdict: `fails-identity`. An allowance behind a closed dashboard and a card is worth
zero, and the verdict says so rather than leaving a reader to find the reason in prose.

## Cloudflare Workers AI

10,000 Neurons a day per account on Workers Free, and the broker reports 30,000 a day
across its accounts with 18.04 spent at 02:50Z (measured 2026-10-22). It is not a search
provider at all: it reranks search results, converts documents to Markdown, and
describes an image when asked.

⭐ **Its rerank is why a broker search looks ordered.** `bge-reranker-base` scores the
first 30 results' titles and snippets against the query on the Cloudflare accounts first,
then the deployment's own binding, and `x-web-rank` says which ran. The accounts are
asked first because each has its own daily Neurons.

⚠ **A spent allocation is silent.** The answer then carries `x-web-rank: provider(<reason>)`
and the results keep the provider's own order, which still looks like a ranking. After
three failed reranks in 60 seconds the breaker opens for 60 seconds and every answer says
`provider(skipped:breaker)` and is stored for 60 seconds, so a caller who does not read
the header keeps a stale, unranked answer for a minute.

Evidence: `search.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version
`731c403806c8`): the rerank order, the 3,000 ms account budget, the 1,500 ms binding
budget, and the `x-web-rank` reasons including `allocation` and `skipped:breaker`.
Measured: `web.pkgforge.dev/status.json` reports the `neurons` pool at 30,000 a day with
18.038 spent.

Verdict: not a search lane and the reason every other lane's answer is ordered.

## What did not work

- **Bing Search APIs**: retired on 2025-08-11 and every instance decommissioned. Any
  list still carrying a Bing free tier is a year out of date
  (`learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement`,
  read 2026-10-22). Record `dossier/crawler-scraper/bing-search-api.json`,
  `documented`, `dead`, and its identity cost was `card` at the time it closed, so
  even the last year of it was not anonymous.
- **Google Programmable Search**: 100 queries a day, closed to new customers, and
  discontinued on 2027-01-01. The free tier is real and unreachable
  (`developers.google.com/custom-search/v1/overview`, read 2026-10-22). Record
  `dossier/crawler-scraper/google-custom-search.json`, `documented`, `dead`, binding
  `request-rate` at 100 queries a day.
- **Marginalia**: three routes, three failures. `search.marginalia.nu` redirects to
  `marginalia-search.com`; `?format=json` there returns HTML at `200`;
  `old-search.marginalia.nu` returns an error page titled "Wait For A Moment"
  (measured 2026-10-22).
- **DuckDuckGo HTML endpoint**: `202` with 14,258 bytes and zero result nodes. `202`
  is the shape to distrust: not a `429`, not a `403`, and no results (measured
  2026-10-22). Record `dossier/crawler-scraper/duckduckgo-html.json`, `measured`,
  `dead`. A scraper that checks the status records this as a win.
- **SearXNG public instances**: seven probed, and zero returned JSON. The JSON format
  is off by default and most instances disable it (`reported`).
- **The Kakao and Naver numbers**: 900,000 and 750,000 monthly calls, the two largest
  recurring figures in this topic. Both index Korean only. Routing an
  English query to either records a miss as a provider failure, so neither belongs in
  a capacity sum.

## Chaining

A search and a read come from different services. The broker supplies both from one
credential. The pattern that works without it is
Keenable for coverage, Exa for the query that decides a finding, and Jina Reader for
the page the search returns. See [`free/reader-extractors.md`](reader-extractors.md)
for the second half.

The same question asked of papers rather than pages is `research.web.pkgforge.dev/works`,
whose index is OpenAlex. OpenAlex gives USD 1 of API usage a day with a free key and 10
requests a second without one, and its basic paging stops at 10,000 results, so a
literature sweep needs the free key for cursor paging before it needs anything else
(`help.openalex.org/access/pricing/` and `docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication`,
both read 2026-10-22).
