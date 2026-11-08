# Which service passes a challenge, and what does a defended page cost?

A fetch relay is a fetch with a proxy and a browser already attached. The class exists
because a page behind an automated-traffic filter cannot be read by rendering alone.
The defence is not that the page needs JavaScript. It is that the page refuses anything
that looks automated. So a fetch relay is priced higher than a reader and its unit is
multiplied by how hard the page is.

The answer: **ZenRows at 5,000 credits a month, of which 5,000 are plain pages, 1,000
rendered, 500 proxied and 200 both.** The headline is not the ceiling and the multiplier
is not a footnote. Bright Data and ScrapingAnt are the other two with a recurring
monthly grant. ScraperAPI, Crawlbase and Scrapfly give a one-time grant and a published
multiplier table.

## The comparison

`Multiplier` is what a defended or rendered page costs against the plain page. `Binds`
is what fails first.

| Provider | Ceiling | Multiplier | Binds | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| ZenRows | 5,000 credits a month, 5 concurrent | 1 plain, 5 render, 10 proxy, 25 both | `per-object-cap`: the multiplier | email | qualifies-with-caveat |
| Bright Data | 5,000 records a month | 1 record a request | `request-rate`: 1,000 a minute unfunded | email | qualifies-with-caveat |
| ScrapingAnt | 10,000 credits a month, which is 1,000 pages | 10 on the default request, 1 to 25 in range | `per-object-cap`: the default is a rendered page | email | qualifies-with-caveat |
| ScraperAPI | 1,000 credits on signup | 1 standard, 5 Amazon, 25 Google, +10 automated-traffic filter | `per-object-cap`: the per-domain multiplier | email | qualifies-with-caveat |
| Crawlbase | up to 5,000 requests, one time | ladder price, multiplied by difficulty | `per-object-cap`: the multiplier reaches 40 | email | qualifies-with-caveat |
| Scrapfly | 1,000 credits on signup | per feature enabled | `per-object-cap`: a per-feature multiplier that does not hard-cap | email | qualifies-with-caveat |
| 12ft.io | none | not reachable | `request-rate`: no request completes | anonymous | dead |

## ZenRows

5,000 credits a month, no card, 5 concurrent, monthly refresh with no rollover, and
Extract free on top of the Fetch request it uses. Build is USD 19 a month on monthly
billing, USD 16 on annual, for 45,000 credits and 20 concurrent.

⚠ **The multiplier is the whole offer.** A standard page is 1 credit, with JavaScript
rendering 5, with premium proxies 10, with both 25. So 5,000 credits is 5,000 plain
pages or 200 fully defended ones, and both numbers are true statements about the same
tier. A document that quotes 5,000 without the multiplier has overstated it twenty-five
fold in the worst case.

Evidence: `zenrows.com/pricing` (read 2026-10-22): "Free USD 0/mo, 5,000 credits/month,
no card, 5 concurrent requests"; "Standard page 1 credit", "With JavaScript rendering 5
credits", "With premium proxies 10 credits", "JavaScript and premium proxies 25
credits".

Verdict: the best value in the class because the plain page is one credit and the
extract is free.

## Bright Data

5,000 records a month on the Free Tier, no credit card, at USD 1.50 per 1,000 records
pay-as-you-go. The Web Scraper API returns records, not pages: one record is one scraped
item.

⚠ **A record is not a request and not always a page.** A job that returns fifty items
from one page bills fifty records. The unit is the output, so the ceiling depends on the
shape of what is scraped and cannot be converted to pages without knowing the site.

Evidence: `brightdata.com/pricing/web-scraper` (read 2026-10-22): "Free Tier 5K records,
5K records per month, no credit card required"; "Pay as you go USD 1.5/1K record".

Verdict: the largest proxy network in the class and the smallest free allowance relative
to it. The escalation target for a page defended by a vendor the cheap ones cannot pass.

## ScrapingAnt

10,000 credits a month, no card, refreshed monthly, with three agent-callable MCP tools:
`get_web_page_html`, `get_web_page_markdown` and `get_web_page_text`.

⚠ **The headline is ten times the usable figure.** The page states that the default
request, Chrome rendering with standard proxies, costs 10 credits, and that most
requests cost between 1 and 25. So 10,000 credits is 1,000 pages, and a page with a
premium proxy is 400. This is the clearest arithmetic trap in the topic.

Evidence: `scrapingant.com` (read 2026-10-22): "10K free credits, no card"; "the default
request, Chrome rendering with standard proxies, costs 10 credits"; "Most requests cost
between 1 and 25 credits".

Verdict: a rendered page at ten times Firecrawl's unit. The wrong first leg and a
reasonable last one.

## ScraperAPI

1,000 credits on signup with 5 concurrent connections, and a `max_cost` parameter that
caps what one request may spend.

The multiplier table is the most honest in the class, because it names the domains
instead of describing them: a standard page is 1 credit, Amazon 5, Google and Bing 25,
LinkedIn 30, and a site behind Cloudflare, DataDome or PerimeterX adds 10.

⚠ **A Google SERP costs 25 credits here, so the free grant is 40 searches.** That is the
number a search sweep needs and it is not on the front of the page.

Evidence: `scraperapi.com/pricing/` (read 2026-10-22): "1,000 free API credits with a
maximum of 5 concurrent connections"; "A standard page costs 1 credit. Amazon costs 5,
Google and Bing ... cost 25, and LinkedIn costs 30. Sites behind bot protection ...
add 10 credits per request".

Verdict: the reference table for what a defended page costs, and a one-time grant.

## Crawlbase

Up to 5,000 requests free with no card, then a ladder from USD 3.00 per 1,000 for the
first thousand down to USD 0.02 beyond a billion.

⚠ **Site difficulty and rendering multiply a group's ladder total.** The platform's
research corpus records a factor up to 40 at the auto-applied tier. A per-1,000 price
says nothing about one defended, rendered page.

Evidence: `crawlbase.com/pricing` (read 2026-10-22): "Up to 5,000 requests free. No
credit card"; "The card shows standard requests. Site difficulty and JavaScript
rendering multiply a group's ladder total".

Verdict: a one-time grant and a multiplier. Its `cb_status` field is one of the few
provider-level block markers worth trusting.

## Scrapfly

1,000 API credits on signup, no card, 5 concurrency, and extra credits not allowed on
the free tier, so it hard-caps rather than overflowing. One key reaches every product on
one balance: JavaScript rendering, a fetch relay, consumer-connection proxies and country
targeting.

⚠ **The credit cost depends on the features enabled.** The page states it and does not
give the per-feature numbers, so the ceiling cannot be converted to pages.

Evidence: `scrapfly.io/pricing` (read 2026-10-22): "Free tier: 1,000 API credits on
signup, no credit card"; "Credit cost per request depends on the features you enable";
"Free ... 5 concurrency, quota cap".

Verdict: a test, not a lane. The hard cap is the honest part.

## 12ft.io

Nothing. `curl` exit 60, `SEC_E_UNTRUSTED_ROOT`: the certificate chain is issued by an
authority that is not trusted, so no HTTP request completes.

⚠ **This is the one dead end whose failure is below HTTP.** A caller that records `000`
and moves on has the right answer; a caller that retries a TLS error has none. The name
still circulates in lists of paywall readers.

Evidence: `12ft.io/https://example.com` (measured 2026-10-22): curl exit 60, no status
received.

Verdict: dead.

## What did not work

- **ScrapingAnt's headline as a page count**: 10,000 credits is 1,000 pages, not 10,000
  (`scrapingant.com`, read 2026-10-22).
- **A premium-proxied page at ZenRows**: 10 credits, so the 5,000-credit tier is 500
  pages and not 5,000 (measured arithmetic from `zenrows.com/pricing`).
- **12ft.io**: TLS failure below HTTP (measured 2026-10-22).
- **A challenge detected by a vendor name in the body**: a detector that matches any
  occurrence of a vendor's name marks ordinary pages as defended. A marker is usable
  only if a recorded challenge page contained it as a challenge, and
  `challenges.cloudflare.com` is explicitly not one because it appears on ordinary
  pages' Turnstile widgets.
- **Detecting a challenge from the status code**: a challenge can arrive as `200`,
  `202`, `403` or `429`. The broker's own read answers a wall at `200` with
  `x-reader-upstream-status: 403`.

## Chaining

A fetch relay is the fifth rung and it is priced like one. The order that works: the
origin's own fetch, then a reader, then a reader with a provider pinned, then an
archive, then a fetch relay for the page that must be read live. When a fetch relay is
needed, ZenRows for a plain page and Bright Data for one defended by a vendor the cheap
ones cannot pass. See [`free/keyless-legs.md`](keyless-legs.md) for the route that costs
nothing before any of these.
