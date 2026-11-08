# What does a browser hour cost, and what does one page cost in it?

A headless browser is priced by time and used by page. That mismatch is the whole
economics of the class, and it is why two providers that both charge USD 0.10 an hour
can differ fourfold on the same job.

The answer: **Browserless at USD 1.25 per 1,000 units is the cheapest entry, and its unit
is 30 seconds, so the price per page is unknown until the page is measured.** Cloudflare
Browser Rendering is cheaper per browser-second and has no separate plan. Hyperbrowser at
USD 0.10 a browser hour is the cheapest per hour by a wide margin and its free grant is
one-time.

## The comparison

Sorted by price per browser hour at an entry plan. `Unit` is what one billable thing is,
because that is what makes the rows comparable.

| Provider | Plan | Per browser hour | Unit | Verdict |
| --- | --- | --- | --- | --- |
| Hyperbrowser | Startup, USD 30 a month | USD 0.10 | 100 credits an hour at USD 0.001 a credit | paid-only |
| Browserbase | Developer, USD 20 a month | USD 0.12 | 100 hours included, then USD 0.12 | paid-only |
| Browserless | Prototyping, USD 25 a month | USD 0.50 | 120 units an hour at USD 1.25/1,000 | paid-only |
| Browserless | Scale, overage | USD 0.60 | 120 units an hour at USD 0.0015 | paid-only |
| Apify | Free, against USD 0.2 a compute unit | USD 0.20 a compute unit | a compute unit, not an hour | paid-only |
| Steel.dev | USD 30 one time | not published per hour | browser-second against a USD 30 credit | trial-only |

## Hyperbrowser

Startup is USD 30 a month with USD 30 of usage included and 30,000 credits, which is
USD 0.001 a credit and 100 credits a browser hour, so USD 0.10 a browser hour. Scale is
USD 100 a month for 100,000 credits.

⭐ **It is the cheapest browser hour in the class by a factor of four.** No other
provider here sells an hour for a tenth of a dollar.

⚠ **It renders every page whatever is asked.** So the cheap hour is charged whether the
page needed it or not, and a plain HTML page costs the same as a script-built one.

⚠ **Job results are kept 7 days.** A poll after that is a `410`.

Evidence: `hyperbrowser.ai/pricing` (read 2026-10-22): "Startup USD 30 per month, USD 30
in usage included, 30,000 credits, 25 concurrent sessions"; "Browser usage 100 credits /
hour, USD 0.10 / hour"; "1,000 credits = USD 1 in usage".

Verdict: the cheapest hour, and the render is not optional.

## Browserbase

Developer is USD 20 a month for 100 browser hours at 25 concurrent, with hours past the
included ones at USD 0.12, plus 1,000 Search calls and 1,000 Fetch calls included.

⚠ **The Search and Fetch allowances are the valuable part.** 100 browser hours at USD
0.12 is USD 12 of the USD 20, and the rest buys 2,000 calls. A job that mostly fetches
and only occasionally renders gets more from this plan than from any other here.

Evidence: `browserbase.com/pricing` (read 2026-10-22): "Developer USD 20/mo, 25
concurrent browsers, 100 browser hours then USD 0.12/browser hr, 1,000 Search calls,
1,000 Fetch calls".

Verdict: the cheapest hour with a fetch API attached.

## Browserless

Prototyping is USD 25 a month for 20,000 units at USD 1.25 per 1,000. A unit is 30
seconds, so an hour is 120 units and a browser hour is USD 0.15 at that rate, or USD
0.50 if the units are bought at the overage price of USD 0.002.

⚠ **The per-hour figure depends on which rate the units came from.** Included units at
USD 1.25 per 1,000 make an hour USD 0.15; overage units at USD 2.00 per 1,000 make it
USD 0.24; Scale at USD 0.0015 a unit makes it USD 0.18. Three prices for one hour on one
page.

⚠ **A reconnect bills a fresh unit.** A page that drops its connection pays twice.

Evidence: `browserless.io/pricing` (read 2026-10-22): "Prototyping USD 25/month, 20k
units per month, USD 0.0020 per unit overages"; "Scale ... 180k units per month, USD
0.0017 per unit overages"; "Session-reconnects count as new browser connections and
incur a fresh Unit charge".

Verdict: the middle of the class per hour and the only one with a documented `429`.

## Apify

Free is USD 5 of usage a month at USD 0.2 per compute unit with 16 GB of memory, and
Starter is USD 19 a month at the same unit price.

⚠ **A compute unit is not an hour.** It is a normalised measure of memory and time, and
the page does not give the conversion, so USD 0.20 a unit cannot be turned into a price
per browser hour without measuring.

Evidence: `apify.com/pricing` (read 2026-10-22): "Free USD 0.2 / CU, 16 GB, 5
concurrent"; "Starter USD 0.2 / CU, 64 GB, 32 concurrent"; "Scale USD 0.16 / CU".

Verdict: a compute marketplace rather than a browser vendor, and its unit is not
comparable to the others.

## Steel.dev

USD 30 of credits, one time, valid 90 days, at 10 concurrent and 20 requests a minute on
Browser Tools. The page read here gives no per-hour rate.

⚠ **The 90-day expiry is the price.** USD 30 that expires in a quarter is USD 120 a year
of value that cannot be carried, so its effective cost is higher than its face.

Evidence: `api.steel.dev/v1/scrape` (measured 2026-10-22): `421` with "No route defined
for GET /v1/scrape", which proves the host is live. The allowance is `reported`.

Verdict: a trial with a deadline and no published rate.

## What did not work

- **A per-credit price as a browser-hour price**: Hyperbrowser's USD 0.001 a credit is
  USD 0.10 an hour, and the credit figure reads as a hundredth of the hour's real cost.
- **A unit converted to pages without a measurement**: Browserless's 30 seconds cannot be
  turned into a per-page price, because the page time is unknown and a reconnect doubles
  it.
- **Apify's compute unit converted to hours**: the conversion is not published.
- **Steel's scrape route**: `421 No route defined for GET /v1/scrape` (measured
  2026-10-22).
- **A one-time grant counted as a monthly tier**: Steel's USD 30, Notte's USD 10 and
  Hyperbrowser's 5,000 credits are all single grants, and only Hyperbrowser's converts to
  a useful hour count.

## Chaining

A browser is the expensive way to read a page, so the pattern is to render once and reuse
the output. Hyperbrowser for the hour, Browserbase when the job needs its Fetch API more
than its browser, and Browserless when the crawl needs a documented `429` and a stable
unit. See [`paid/crawl-apis.md`](crawl-apis.md) for the crawl that carries the render
across many pages.
