# What does one defended page cost?

A defended page is the only page that must be bought, because nothing free reads it.
This document answers what one costs, and the answer is not a price: it is a multiplier
table. Every provider in this class sells a credit, and one credit is worth a whole plain
page, or a fifth of a rendered one, or a twenty-fifth of one that needs both a render and
a premium proxy.

The answer: **ZenRows at USD 0.28 per 1,000 plain pages on Launch, billed monthly, is the
cheapest in the class, and the same page with a render and a premium proxy is USD 6.90.**
A price without its billing term is not a price: ZenRows' Launch plan is USD 69 a month
month-to-month and USD 58 a month on annual billing, which is ten months paid for twelve.
The per-1,000 figures below use the monthly price. ScrapingAnt's default request is
already a rendered page at 10 credits, so its entry plan is USD 1.90 per 1,000 pages and
not USD 0.19. ScraperAPI's Google SERP is 25 credits. A plan built on a credit headline
without the multiplier is wrong by a factor between five and twenty-five at the providers
read here, and up to forty at Crawlbase.

## The multiplier table, which is the whole document

One credit, expressed as how many pages it buys. Read down the column to compare, and
read across to see what one provider charges for the same page.

| Provider | Plain | Rendered | Premium proxy | Both | Automated-traffic filter |
| --- | --- | --- | --- | --- | --- |
| ZenRows | 1 | 5 | 10 | 25 | not stated |
| ScrapingAnt | 1 | 10 (the default) | not stated | not stated | not stated |
| ScraperAPI | 1 | not stated | not stated | not stated | +10 on any page |
| Crawlbase | 1 | multiplied | multiplied | multiplied | up to 40 by its own ladder |
| Scrapfly | 1 | per feature | per feature | per feature | per feature |
| Bright Data | 1 record | not stated | not stated | not stated | not stated |

## The comparison

Sorted by price per 1,000 plain pages at an entry plan, on monthly billing. `Defended` is
what the same plan buys once the multiplier applies. ⛔ **The billing term is part of the
price**, so the `Plan` column states it.

| Provider | Plan | Plain, per 1,000 | Defended, per 1,000 | Binds | Verdict |
| --- | --- | --- | --- | --- | --- |
| ZenRows | Launch, USD 69 a month, monthly billing | USD 0.28 | USD 6.90 at 25 credits | `per-object-cap`: the multiplier | paid-only |
| ZenRows | Build, USD 19 a month, monthly billing | USD 0.42 | USD 10.56 at 25 credits | as above | paid-only |
| ScrapingAnt | Enthusiast, USD 19 a month | USD 1.90 at the default | USD 4.75 at 25 credits | `per-object-cap` | paid-only |
| ScraperAPI | Hobby and up | by plan | +10 credits on a defended page | `per-object-cap` | paid-only |
| Crawlbase | 100,000 a month | USD 0.76 | up to USD 30.40 at 40 | `per-object-cap` | paid-only |
| Bright Data | pay as you go | USD 1.50 | USD 1.50 a record | `request-rate` | paid-only |
| Scrapfly | Pro, USD 100 a month | USD 0.10 | multiplier unpublished | `per-object-cap` | paid-only |

## ZenRows

Build is USD 19 a month for 45,000 credits on monthly billing, which is USD 0.42 per
1,000. Launch is USD 69 for 250,000, which is USD 0.28. On annual billing those same
rungs are USD 16 and USD 58, which is USD 0.36 and USD 0.23 per 1,000: ten months paid
for twelve.

⚠ **The annual rate is a discount, not the price.** Every per-1,000 figure in this
document uses the monthly price, because the decision is monthly and a figure that only
holds after a year's commitment is a different offer. Quoting USD 0.23 as "the price"
understates the monthly figure by 15.9%.

⭐ **The plain page at USD 0.42 per 1,000 on Build is the cheapest in the corpus**, and it
includes the fetch relay network at the plain rate. That is the offer: the defence is
included and the *render* and the *consumer-connection proxy* are what cost extra.

⚠ **The four rates are the price list.** 1 credit plain, 5 rendered, 10 with a premium
proxy, 25 with both. A defended page that also needs a render is 25 credits, which is
USD 10.56 per 1,000 on Build. That is twenty-five times the headline.

Evidence: `zenrows.com/pricing` (read 2026-10-22): the four credit rates; Build at USD 16
to 33 a month annually and USD 19 to 39 monthly, for 45,000 to 120,000 credits; Launch at
USD 58 to 108 annually and USD 69 to 129 monthly, for 250,000 to 700,000 credits. The
page states both bases in its own structured data: "The price is the annual monthly rate
of the entry rung (pay for 10 months, get 12). Annual monthly rates run $58 to $108;
monthly billing of the same rungs is $69 to $129."

Verdict: the cheapest plain defended page and the most expensive fully defended one.

## ScrapingAnt

Enthusiast is USD 19 a month for 100,000 credits, and the default request, Chrome
rendering with standard proxies, costs 10 credits. Most requests cost between 1 and 25.

⚠ **The default is the defended case.** A caller who does nothing but send the URL pays
10 credits, so the entry plan is USD 1.90 per 1,000 pages, not USD 0.19.

Evidence: `scrapingant.com` (read 2026-10-22): "the default request, Chrome rendering
with standard proxies, costs 10 credits"; "Most requests cost between 1 and 25 credits
depending on the options you enable (proxy type, JavaScript rendering, etc.)".

Verdict: a rendered page at USD 1.90 per 1,000 on the entry plan. The plan is cheap and
the default is expensive.

## ScraperAPI

A standard page is 1 credit, Amazon 5, Google and Bing 25, LinkedIn 30, and a site
behind Cloudflare, DataDome or PerimeterX adds 10 credits a request.

⭐ **This is the only multiplier table that names the domains**, which makes it the
reference for what a defended page costs in the real world: the defence surcharge is a
flat 10 credits and the domain surcharge is up to 30.

⚠ **A Google SERP is 25 credits**, so a search through this provider costs 25 times a
plain page. That is the single highest per-page price in this topic for an ordinary
public page.

⚠ **`max_cost` per scrape is the feature worth copying.** It caps what one request may
spend, which is the only protection against a multiplier a caller did not anticipate.

Evidence: `scraperapi.com/pricing/` (read 2026-10-22): "A standard page costs 1 credit.
Amazon costs 5, Google and Bing ... cost 25, and LinkedIn costs 30. Sites behind bot
protection like Cloudflare, Datadome, or PerimeterX add 10 credits per request".

Verdict: the reference table, and a provider whose cheap page is cheap and whose
expensive page is 25 times it.

## Crawlbase

A ladder from USD 3.00 per 1,000 for the first thousand down to USD 0.60 at 100,000 and
USD 0.02 beyond a billion, with site difficulty and rendering multiplying a group's
ladder total.

⚠ **The multiplier reaches 40.** The platform's research corpus records a factor up to 40
at the auto-applied tier, which makes a defended page USD 30.40 per 1,000 at the 100,000
rate. That is the widest span in the class.

Evidence: `crawlbase.com/pricing` (read 2026-10-22): the ladder, and "Site difficulty and
JavaScript rendering multiply a group's ladder total". The factor of 40 is `reported`.

Verdict: the cheapest plain page at very high volume and the most expensive defended one.

## Bright Data

USD 1.50 per 1,000 records pay-as-you-go, from a 5,000-record free tier, with 1,000
requests a minute on the unfunded tier.

⚠ **A record is the output, not the request.** A job that returns fifty items from one
page bills fifty records, so USD 1.50 per 1,000 is a price per extracted item and not per
page.

Evidence: `brightdata.com/pricing/web-scraper` (read 2026-10-22): "Pay as you go USD
1.5/1K record"; "5K records per month" on Free.

Verdict: the largest network and the only unit that is output rather than input.

## Scrapfly

Pro is USD 100 a month for 1,000,000 credits at USD 0.10 per 1,000 credits, with
pay-as-you-go overflow at USD 3.50 per 10,000 extra.

⚠ **The per-feature costs are not published.** The page states that credit cost depends
on JavaScript rendering, the fetch relay, consumer-connection proxies and country
targeting, and gives no number for any of them, so USD 0.10 per 1,000 is a floor with no
ceiling.

Evidence: `scrapfly.io/pricing` (read 2026-10-22): "Pro USD 100 monthly, 1,000,000
included credits"; "Credit cost per request depends on the features you enable
(JavaScript rendering, Unblocker, residential proxies, country targeting, etc.)".

Verdict: the lowest per-credit price and an unquantified multiplier.

## What did not work

- **A credit headline as a page count**: five providers in this document publish a credit
  count whose page value is a fifth to a twenty-fifth of the number, and Crawlbase's
  own multiplier reaches forty.
- **A vendor name in the body as a challenge marker**: the platform's research found that
  matching a vendor's name marked ordinary pages as defended, and that
  `challenges.cloudflare.com` appears on ordinary pages' Turnstile widgets. A marker is
  usable only if a recorded challenge page contained it as a challenge.
- **A status code as a challenge signal**: a wall arrives as `200`, `202`, `403` or `429`.
  The broker answered `200` with 18,041 bytes for a page whose origin said `403`.
- **12ft.io**: `curl` exit 60, `SEC_E_UNTRUSTED_ROOT`, below HTTP (measured 2026-10-22).
- **Scrapfly's ceiling**: it cannot be computed from the page, so a plan cannot be built
  on it.

## Chaining

A defended page is the last rung and the only one that must be bought. The pattern that
works: the broker's `read` with a provider pinned, which costs nothing and passes most
walls; ZenRows when the page needs a consumer-connection proxy; Bright Data when the
defence is one the cheap networks cannot pass. Measure one page before choosing a plan, because the
multiplier decides the plan and not the reverse. See
[`paid/reader-extractors.md`](reader-extractors.md) for the per-page prices these
multipliers apply to.
