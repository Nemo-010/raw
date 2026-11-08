# What does a thousand-page crawl cost?

A crawl is priced per page and billed per credit, and the two are the same number only
for a provider that has no multipliers. This document answers what 1,000 pages costs at
each provider, which is the only figure a plan can be built on.

The answer: **USD 0.28 per 1,000 plain pages at ZenRows' Launch plan, on monthly billing,
is the cheapest, and the same crawl of rendered pages costs USD 1.38.** Firecrawl at
USD 0.83 per 1,000 and Context.dev at USD 0.79 are the two cheapest that include a
render. Every other provider's headline is a credit price that a multiplier turns into
something else. ⛔ **A per-1,000 figure carries its billing term**, because ZenRows' Launch
plan is USD 69 a month monthly and USD 58 a month annually, and the annual rate is 15.9%
lower.

## The comparison

Sorted by price per 1,000 pages at an entry plan a person could buy, on monthly billing.
`Plain` and `Rendered` are two separate numbers, because that is the whole point of the
class.

| Provider | Plan | Plain, per 1,000 | Rendered, per 1,000 | Verdict |
| --- | --- | --- | --- | --- |
| ZenRows | Launch, USD 69 a month, monthly billing | USD 0.28 | USD 1.38 | paid-only |
| ZenRows | Build, USD 19 a month, monthly billing | USD 0.42 | USD 2.11 | paid-only |
| Context.dev | Standard, USD 99 a month | USD 0.79 | USD 0.79 | paid-only |
| Firecrawl | Standard, USD 83 a month | USD 0.83 | USD 3.32 | paid-only |
| ScrapingAnt | Business, USD 249 a month | USD 0.83 | USD 0.83 | paid-only |
| ScrapingAnt | Enthusiast, USD 19 a month | USD 1.90 | USD 1.90 | paid-only |
| Crawlbase | 100,000 a month | USD 0.76 | multiplied, up to 40 | paid-only |
| Crawl4AI | hosted cloud | USD 0.25 implied | not published | paid-only |
| Browserless | Prototyping, USD 25 a month | USD 0.42 a page at 30 seconds | unknown, time-billed | paid-only |

## ZenRows

Launch is USD 69 a month for 250,000 credits at USD 0.28 per 1,000, and Build is USD 19
for 45,000 at USD 0.42, both on monthly billing. Annual billing is USD 58 and USD 16, or
USD 0.23 and USD 0.36 per 1,000, because the annual plan pays for ten months and gets
twelve. A standard page is 1 credit, a rendered page 5, a premium proxy 10, and both 25.

⭐ **Four numbers for one page, all of them true.** A 1,000-page crawl is USD 0.28 plain,
USD 1.38 rendered, USD 2.76 proxied, or USD 6.90 with both. The plan does not change; the
page does.

⚠ **A crawl that reserves 1 credit a page and enables rendering under-reserves
fivefold.** The platform's own rule is to reserve the maximum of the applicable weight,
which is the only safe number before a page is seen.

Evidence: `zenrows.com/pricing` (read 2026-10-22), structured data: "Launch ... The price
is the annual monthly rate of the entry rung (pay for 10 months, get 12). Annual monthly
rates run $58 to $108; monthly billing of the same rungs is $69 to $129." The credit
rates are "Standard page 1 credit", "with JavaScript rendering 5 credits", "with premium
proxies 10 credits", "JavaScript and premium proxies 25 credits".

Verdict: the cheapest plain page at volume and the widest span between plain and
defended.

## Context.dev

Standard is USD 99 a month for 125,000 credits at USD 0.79 per 1,000 pages, and a scrape
includes rendering and proxies at the base rate of 1 credit.

⭐ **This is the only row where the plain and rendered prices are the same**, because the
render is included rather than metered. That makes it the cheapest rendered page in the
class at USD 0.79, against Firecrawl's USD 3.32 and ZenRows' USD 1.38.

⚠ **JSON extraction is 5 credits a page.** A structured crawl at 5 credits is USD 3.96
per 1,000 on Standard, which puts it back in the same range as the others.

Evidence: `context.dev/pricing` (read 2026-10-22): "Standard USD 99/month, 125,000
credits, USD 1.80 per 1,000 overage"; "1 credit per scrape at the base rate"; "Scrape with
JSON extraction 5 credits per page".

Verdict: the cheapest rendered crawl and the one place where the render is not a
surcharge.

## Firecrawl

Standard is USD 83 a month for 100,000 credits at USD 0.83 a page, and Hobby is USD 19
for 5,000 at USD 3.80. Both are on monthly billing; the card on the vendor page is
headed "Prices shown are per month, billed annually", and Hobby's own line gives both
bases: "USD 19/month billed monthly, or USD 16/month billed annually".

⚠ **A crawl credit is a page and a render is four.** A 1,000-page crawl of a
script-built site is 4,000 credits, which is USD 3.32 per 1,000 on Standard, not USD
0.83.

⚠ **Crawl is limited to 2 requests a minute on the free tier and the job cap is 100
pages.** A 1,000-page crawl is ten jobs, so the wall clock is part of the price.

Evidence: `firecrawl.dev/pricing` (read 2026-10-22): "Standard USD 83/month ... 100,000
pages scraped"; `crawl.web.pkgforge.dev/llms-full.txt` (read 2026-10-22): `limit` 1 to
100, and `usage.amount` reports credits per job. Measured: a 3-page job billed 3 credits
in about 10 seconds.

Verdict: the cheapest page at Standard for a static site and four times that for a
rendered one.

## ScrapingAnt

Business is USD 249 a month for 3,000,000 credits, which at the default request of 10
credits is USD 0.83 per 1,000 pages. Enthusiast at USD 19 for 100,000 is USD 1.90.

⭐ **The rendered price is the plain price**, because the default request already includes
Chrome rendering and standard proxies. A page that needs neither costs 1 credit and is
ten times cheaper, which is the only way this row beats Context.dev.

⚠ **The credit headline is tenfold the page count.** 3,000,000 credits is 300,000
rendered pages.

Evidence: `scrapingant.com` (read 2026-10-22): "Business 3M credits/mo USD 249/mo";
"the default request, Chrome rendering with standard proxies, costs 10 credits"; "Most
requests cost between 1 and 25 credits".

Verdict: a rendered crawl at USD 0.83 per 1,000 on Business and USD 1.90 on the entry
plan. The credit table decides, not the plan name.

## Crawlbase

Up to 5,000 requests free, then a ladder from USD 3.00 per 1,000 for the first thousand
down to USD 0.60 at 100,000 and USD 0.02 beyond a billion.

⚠ **Site difficulty and rendering multiply a group's ladder total, and the platform's
research records a factor up to 40.** So USD 0.76 per 1,000 blended at 100,000 is the
plain price and a defended page can be thirtyfold.

Evidence: `crawlbase.com/pricing` (read 2026-10-22): "USD 0.76 blended per 1,000
requests" at 100K; "The card shows standard requests. Site difficulty and JavaScript
rendering multiply a group's ladder total".

Verdict: the widest multiplier in the class, and the ladder makes volume cheap.

## Crawl4AI

0.5 credit a page, so a 1,000-page crawl is 500 credits. At the free tier's ratio that
implies about USD 0.25 per 1,000.

⚠ **The paid rate card was not read.** `crawl4ai.com` answered `404` on 2026-10-22, so
the figure is inferred from the free allowance's ratio and is `reported`.

⚠ **1 concurrent browser and 2 hard per site on the free tier.** A 1,000-page crawl
against one host is a slow queue.

Evidence: `reported` from the platform's research corpus.

Verdict: the cheapest unit and the least certain price.

## Browserless

Prototyping is USD 25 a month for 20,000 units at USD 1.25 per 1,000, and a unit is 30
seconds of browser connection.

⚠ **The per-page price cannot be computed from the rate card.** A page that takes 30
seconds is one unit and USD 0.00125; a page that takes 3 seconds is a tenth of a unit but
bills a whole one, because the unit is a block. So the per-page cost is between USD 0.0013
and USD 0.0013, and the only honest statement is that it depends on the page.

Evidence: `browserless.io/pricing` (read 2026-10-22): "A Unit is a block of browser time
of up to 30 seconds per browser connection"; "`/crawl` ... 1 unit per 30 s per
connection, not per page" from the platform's research corpus.

Verdict: the right crawl for a few slow pages and the wrong one for many fast ones.

## What did not work

- **A crawl that reserves the headline per page**: ZenRows reserves fivefold low with
  rendering and twenty-fivefold with a proxy, and Crawlbase's multiplier reaches 40.
- **A crawl pinned to a provider that cannot apply path globs**: ZenRows and Hyperbrowser
  cannot, so the pin is a `503`.
- **A crawl with `main_content` at Browser Rendering, ZenRows or Hyperbrowser**: all
  three answer each page whole, so a job asking for main content never goes to them.
- **A crawl of more than 100 pages in one job**: `limit` is capped at 100, so a 1,000-page
  crawl is ten jobs and ten submissions.
- **A crawl job polled after 15 days**: the job id is deleted and the poll is a `404`.
  Browser Rendering keeps results 14 days and Hyperbrowser 7, so the `410` arrives sooner
  than the `404`.

## Chaining

A crawl is the last thing to buy and the first thing to size. The pattern that works:
measure one page's credit cost by submitting a 3-page job, multiply by the intended page
count, and only then choose the plan. Context.dev for a rendered crawl, ZenRows for a
plain one, Firecrawl when the same credential must also read and search. See
[`paid/reader-extractors.md`](reader-extractors.md) for the per-page prices that a crawl
is built from.
