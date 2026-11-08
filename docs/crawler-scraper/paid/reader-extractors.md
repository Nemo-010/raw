# What does a page cost once the free allowance is gone?

Extraction is the most expensive operation per unit, and the paid lane
makes the reason plain: a plain page costs USD 0.28 per 1,000 at the cheapest plan read
here, and a page that needs a render and a premium proxy costs USD 6.90 per 1,000 at the
same provider. Nothing differs in the output.

The answer: **ZenRows at USD 0.28 per 1,000 plain pages on its Launch plan, billed
monthly, is the cheapest in the class, Context.dev at USD 0.79 is the cheapest that
includes a render, and Exa's contents endpoint at USD 1 per 1,000 per content type is the
cheapest when the URLs are already known.** The trap is that a credit count is not a page
count: a render multiplies it by five and a premium proxy by ten. ⛔ **The second trap is
the billing term**: ZenRows' Launch plan is USD 69 a month monthly and USD 58 a month
annually, so a per-1,000 price quoted without the basis is 15.9% below the monthly one.

## The comparison

Sorted by price per 1,000 pages at a plan size a person could actually buy, on monthly
billing. `Features` says whether the price includes a render and a proxy.

| Provider | Plan | Per 1,000 pages | Features included | Verdict |
| --- | --- | --- | --- | --- |
| Exa contents | pay-as-you-go | USD 1.00 per content type | text, highlights or summary, each billed | paid-only |
| Context.dev | Standard, USD 99 a month | USD 0.79 | scrape with rendering and proxies | paid-only |
| Context.dev | Starter, USD 19 a month | USD 2.53 | as above | paid-only |
| Firecrawl | Standard, USD 83 a month | USD 0.83 | 1 credit a page | paid-only |
| Firecrawl | Hobby, USD 19 a month, monthly billing | USD 3.80 | as above | paid-only |
| Crawl4AI | hosted cloud | USD 0.25 implied at 0.5 credit | plain scrape | paid-only |
| ZenRows | Launch, USD 69 a month, monthly billing | USD 0.28 plain, USD 1.38 rendered | plain, then 5 credits rendered | paid-only |
| ScrapingAnt | Enthusiast, USD 19 a month | USD 1.90 at the default request | Chrome rendering and standard proxies | paid-only |
| Browserless | Prototyping, USD 25 a month | USD 1.25 per 1,000 units | 30 seconds of browser time a unit | paid-only |
| Scrapfly | Pro, USD 100 a month | USD 0.10 per 1,000 credits | per-feature multiplier | paid-only |

## Exa contents

`/contents` returns full page text, highlights and summaries for URLs already held, at
USD 1 per 1,000 pages per content type.

⭐ **It is the cheapest page in the class, and it is not a reader.** It does not fetch a
URL you do not have and it does not pass a challenge. It is the right call when a search
already returned the URLs.

⚠ **Each content type bills separately.** Text and highlights on one page is two pages
of billing, so asking for both doubles the price to USD 2 per 1,000.

Evidence: `exa.ai/pricing` (read 2026-10-22): "`/contents` USD 1 / 1k pages, per content
type"; "one page with `text` and `highlights` counts as two".

Verdict: the cheapest paid page, for a URL already in hand.

## Context.dev

Standard is USD 99 a month for 125,000 credits with overage at USD 1.80 per 1,000, which
is USD 0.79 per 1,000 pages. Starter is USD 19 a month for 7,500 credits at USD 2.53 per
1,000, Business USD 299 for 500,000 at USD 0.60, and Scale USD 499 for 1,000,000 at USD
0.50.

The base rate is 1 credit a scrape and 5 with JSON extraction, and the scrape includes
rendering and proxies. That inclusion is why it is the cheapest credible page: the
provider whose headline is lower often costs more per rendered page.

⚠ **JSON extraction is five times the base rate.** A structured sweep at 5 credits a
page costs USD 3.96 per 1,000 on Standard, not USD 0.79.

Evidence: `context.dev/pricing` (read 2026-10-22): "Starter USD 19/month, 7,500 credits,
USD 2.20 per 1,000 overage"; "Standard USD 99/month, 125,000 credits, USD 1.80 per 1,000
overage"; "Scrape from 1 credit per call", "Scrape with JSON extraction 5 credits per
page".

Verdict: the cheapest per page that includes a render. The one to buy when the free
1,000 runs out.

## Firecrawl

Hobby is USD 19 a month on monthly billing, or USD 16 billed annually, for 5,000 pages.
Standard is USD 83 a month and those prices are quoted on annual billing on the vendor's
own card. At monthly billing Hobby is USD 3.80 per 1,000 and Standard USD 0.83. Top-ups
are 1,000 credits per USD 5, which is USD 5 per 1,000.

⚠ **A render or a JSON extraction is 4 credits.** So a Standard plan of 100,000 credits
is 25,000 rendered pages, at USD 3.32 per 1,000, not USD 0.83.

⚠ **Top-ups are six times the plan rate.** USD 5 for 1,000 credits against USD 0.83 per
1,000 on Standard is the price of not planning the volume.

Evidence: `firecrawl.dev/pricing` (read 2026-10-22): "Hobby: USD 19/month billed monthly,
or USD 16/month billed annually, for 5,000 credits per month"; "$83/month ... 50,000
searches or 100,000 pages scraped" on a card headed "Prices shown are per month, billed
annually"; "1,000 extra credits per USD 5".

Verdict: the cheapest page at Standard and one of the most expensive top-ups. Buy the
plan size, not the overage.

## Crawl4AI

0.5 credit a page, so at a 2,000-page allowance per 1,000 credits the implied rate is
about USD 0.25 per 1,000 if a paid plan matches the free one's ratio.

⚠ **The paid rate card was not read here.** The vendor page answered `404` on
2026-10-22, so the only figure available is the free tier's ratio, and it is `reported`.
A price derived from a free allowance is an inference, not a quote.

Evidence: `reported` from the platform's research corpus; `crawl4ai.com` answered `404`
to the reader on 2026-10-22.

Verdict: the cheapest unit if the ratio holds and the least established price in the
lane.

## ZenRows

Build is USD 19 a month for 45,000 credits at USD 0.42 per 1,000, Launch USD 69 for
250,000 at USD 0.28, Growth USD 199 for 1,200,000 at USD 0.17, and Scale USD 549 for
5,000,000 at USD 0.11, all on monthly billing. Annual billing is USD 16, 58, 166 and 458,
which is ten months paid for twelve and is where the widely quoted USD 0.23 comes from.

⚠ **The per-credit price falls fourfold and the per-page price is what buys a render.**
A rendered page is 5 credits, so Launch's USD 0.28 per 1,000 credits is USD 1.38 per
1,000 rendered pages. A premium proxy at 10 credits is USD 2.76. Both at 25 credits is
USD 6.90.

⛔ **Quote the billing term with the price.** The vendor's own structured data says "The
price is the annual monthly rate of the entry rung (pay for 10 months, get 12). Annual
monthly rates run $58 to $108; monthly billing of the same rungs is $69 to $129." A
per-1,000 figure built on USD 58 is 15.9% below the monthly price.

Evidence: `zenrows.com/pricing` (read 2026-10-22), structured data: "Free USD 0/mo,
5,000 credits/month"; Build "45,000 to 120,000 credits/month ... annual monthly rates run
$16 to $33; monthly billing of the same rungs is $19 to $39"; Launch "250,000 to 700,000
credits/month ... annual monthly rates run $58 to $108; monthly billing of the same rungs
is $69 to $129"; "Standard page 1 credit, with JavaScript rendering 5 credits, with
premium proxies 10 credits, JavaScript and premium proxies 25 credits".

Verdict: the cheapest plain page at volume and a price that quadruples at the first
defence.

## ScrapingAnt

Enthusiast is USD 19 a month for 100,000 credits, Startup USD 49 for 500,000, Business
USD 249 for 3,000,000, Business Pro USD 599 for 8,000,000, and Custom USD 699 for 10M
and above.

⚠ **The per-credit price and the per-page price differ tenfold.** At the default request
of 10 credits, Enthusiast is USD 1.90 per 1,000 pages, not USD 0.19. Business is USD
0.83, and Business Pro USD 0.75. The headline credit price is the number nobody pays.

Evidence: `scrapingant.com` (read 2026-10-22): "Enthusiast 100K credits/mo USD 19/mo";
"the default request, Chrome rendering with standard proxies, costs 10 credits".

Verdict: a rendered page at USD 1.90 per 1,000 on the entry plan. Read the credit table
before the plan price.

## Browserless

Prototyping is USD 25 a month for 20,000 units at USD 1.25 per 1,000 units, and a unit
is 30 seconds of browser connection. Overage is USD 0.002 a unit, which is USD 2.00 per
1,000.

⚠ **The unit is time.** Twenty thousand units is 166 hours of browser time, and a page
that takes three seconds is 3 seconds of that, so the per-page cost depends entirely on
the site. A per-1,000-units price cannot be converted to a per-page price without
measuring the page.

Evidence: `browserless.io/pricing` (read 2026-10-22): "Prototyping USD 25/month ...
20k units per month ... USD 0.0020 per unit overages"; "A Unit is a block of browser
time of up to 30 seconds per browser connection".

Verdict: the cheapest browser hour and the only row whose per-page price is unknown by
construction.

## Scrapfly

Pro is USD 100 a month for 1,000,000 credits at USD 0.10 per 1,000 credits, with 20
concurrency and pay-as-you-go overflow at USD 3.50 per 10,000 extra credits, which is
USD 0.35 per 1,000.

⚠ **The credit is multiplied by every feature enabled.** JavaScript rendering, the
fetch relay, consumer-connection proxies and country targeting each cost credits and the
page does not give the per-feature numbers, so USD 0.10 per 1,000 is a floor with no ceiling.

Evidence: `scrapfly.io/pricing` (read 2026-10-22): "Pro USD 100 monthly, 1,000,000
included credits, USD 3.50 per 10k extra, 20 concurrency"; "Credit cost per request
depends on the features you enable".

Verdict: the lowest per-credit price and an unquantified multiplier.

## What did not work

- **A per-credit price as a per-page price**: ScrapingAnt is tenfold off, ZenRows
  fivefold, Firecrawl fourfold. Three providers, one error.
- **A top-up as a plan rate**: Firecrawl's USD 5 per 1,000 credits against USD 0.83 per
  1,000 on Standard.
- **Crawl4AI's paid rate**: not published on a reachable page, so the price is inferred
  from the free ratio and is labelled `reported`.
- **Browserless converted to pages**: it cannot be, because the unit is time and the
  page time is unknown.
- **Scrapfly's multiplier**: not published per feature, so its ceiling cannot be
  computed.

## Chaining

The cheap pattern is one search and one contents call: a search returns the URLs and
Exa's contents returns the text at USD 1 per 1,000. The reliable pattern is a reader
that passes a wall, which is Context.dev at USD 0.79 per 1,000 on Standard. The
expensive pattern is a render, which multiplies everything by five. See
[`paid/unblockers-proxies.md`](unblockers-proxies.md) for the multiplier tables in one
place.
