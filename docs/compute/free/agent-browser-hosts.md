# How many free browser minutes, and what does the proxy cost

A browser host sells minutes of a remote Chromium rather than a machine. The rate
is almost always small and the bill is almost never the browser: it is the
consumer-connection proxy, priced per gigabyte, and it costs more per hour of use
than the browser does. For a crawler that is the whole economics of the
class.

The answer: Ferr and Hyperbrowser both give 50 browser hours a month, and they are the
joint largest free allowance in this class. Hyperbrowser's arrives as 5,000 credits shared
with four products; Ferr's is a plain hour count with 3 concurrent sessions. Lightpanda
gives 10 browser hours a month on a purpose-built engine with no card and no time limit.
Kernel gives USD 5 a month, recurring, with unmarked mode and no charge for idle time.
Browserless gives 1,000 units a month on a Free plan with no card, which is 8.3 hours at 30
seconds a unit. Firecrawl's 1,000 monthly credits are 500 browser minutes. Cloudflare gives
10 minutes a day on Workers Free. Every one of them wants money for the bytes.

⚠ Hyperbrowser's 50 hours is not the largest by a
factor of five: Ferr's record carries the same 50 hours. The multiplier is an artefact of a
shortlist that leaves Ferr out. `free/browser-host-long-tail.md`
carries the full 38-record class.

## The comparison

Sorted by the free allowance in browser hours. `Proxy` is the part of the bill
that is not the browser.

| Provider | Free allowance | Proxy | 300 h | 730 h | Session cap | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hyperbrowser | 5,000 credits a month, about 50 browser hours | bundled | USD 30.00 | USD 30.00 | not stated | email | qualifies-with-caveat |
| Kernel | USD 5 a month, recurring | included on paid | USD 30.00 | USD 30.00 | none | email | qualifies-with-caveat |
| Lightpanda | 10 browser hours a month | bring-your-own proxy | USD 19.00 | USD 53.40 | not stated | email | qualifies-with-caveat |
| Browser Use | USD 15 one time | USD 5 per GB | USD 6.00 | USD 14.40 | not stated | email | trial-only |
| Steel | USD 30 one time | USD 10 per GB | USD 30.00 | USD 43.00 | 15 minutes | email | trial-only |
| Browserbase | 1 browser hour | priced separately | USD 44.00 | USD 95.60 | 15 minutes | email | trial-only |
| Bright Data Browser | USD 7.50 a month of credit | priced separately | not read | not read | not stated | card | qualifies-with-caveat |
| Browserless | 1,000 units a month, 8.3 hours at 30 s a unit | consumer-connection 6 units/MB | USD 350.00 | USD 350.00 | 2 minutes | email | qualifies-with-caveat |
| Cloudflare Browser Rendering | 10 minutes a day on Workers Free | through the edge | not read | not read | 15 minutes | email | qualifies-with-caveat |
| Firecrawl | 1,000 credits a month, 500 browser minutes | priced separately | not read | not read | not stated | email | qualifies-with-caveat |

⛔ These rows are in **browser hours**, not a 2 vCPU shape, so they are not
comparable with a sandbox row and the numbers here are not a ranking against one.
A browser host sells minutes of a remote browser. Three hundred browser hours is a
month of one browser at ten hours a day.

## Hyperbrowser

A free account gets 5,000 credits, which the page describes as enough for 50
browser hours or 5,000 fetched pages at base rates, and one credit is USD 0.001
(`documented`, `hyperbrowser.ai/pricing`, read 2026-10-22). That is USD 5 of usage
against a credit pool that covers browsers, sandboxes, web data and agents.

50 browser hours a month ties Ferr for the largest free browser allowance in this class,
and the class is 38 records rather than the nine this document covers. The catch is that
it is a credit pool shared with the agent and scraped-data products, so a crawl that uses
the agent consumes the browser budget too.

Evidence: `hyperbrowser.ai/pricing` (read 2026-10-22). Verdict: the joint best free
browser allowance and one pool for four products.

## Lightpanda

Explorer is USD 0 a month for ever with 10 browser hours, 5 concurrent sessions
and bring-your-own-proxy (`documented`, `lightpanda.io/pricing`, read 2026-10-22).
Builder is USD 19 a month for 300 hours, then USD 0.08 an hour, so 730 hours is
USD 53.40.

Lightpanda is not Chromium. It is a purpose-built headless engine, which makes it
faster per page and less compatible: a site that needs a full browser to render
will not render. The trade is worth stating plainly because it decides the use
case. For a crawl of server-rendered pages it is the cheapest engine here. For a
crawl of a JavaScript application it is the wrong tool.

The free plan recurs monthly, needs no card, and has no session cap. That
combination is unique in this class.

Evidence: `lightpanda.io/pricing` (read 2026-10-22). Verdict: the cheapest
recurring browser allowance and the narrowest engine.

## Kernel

Free is USD 0 a month plus usage, with USD 5 of free credits a month, 5 concurrent
browsers, unmarked mode including a human-verification handling feature and proxy,
3 managed auth connections and 1-day session replays (`documented`,
`kernel.sh/pricing`, read 2026-10-22). The page states that a signup needs no credit
card.

Usage is USD 0.0000166667 per GB-second with no charges for idle time or proxies.
That unit is the interesting part: the cost follows page weight rather than
wall-clock, so a held session that is doing nothing is free and a heavy page is
not. A reader who is used to per-hour billing will misjudge it in both directions.

An unmarked profile mode on the free tier is unusual. Most of this class puts it
behind a paid plan.

Evidence: `kernel.sh/pricing` (read 2026-10-22). Verdict: a recurring credit, a
GB-second unit, and the best free features.

## Steel

Launch is USD 0 a month plus usage with USD 30 of credits one time, 10 concurrent
sessions, sessions up to 15 minutes, up to 3 seats and no credit card (`documented`,
`steel.dev/pricing`, read 2026-10-22). Browser hours are USD 0.10 and proxy
bandwidth is USD 10 per GB on Launch; Scale is USD 250 a month with USD 100 of
credits each month and USD 6 per GB.

USD 30 at USD 0.10 an hour is exactly 300 browser hours, and the 15-minute session
cap turns that into 1,200 sessions with setup between each. Data retention is 7
days on Launch. Past the credit, 730 hours is USD 43.00.

⛔ The proxy is the number that decides: USD 10 per GB means a crawl that pulls
1 GB pays the equivalent of 100 browser hours. The browser is not the cost.

Evidence: `steel.dev/pricing` (read 2026-10-22). Verdict: a generous one-time
credit with a proxy price that dwarfs it.

## Browserbase

Free is 3 concurrent browsers, 1 browser hour, 3 agent runs, 1,000 search calls,
1,000 fetch calls, and 15 minutes per session (`documented`,
`browserbase.com/pricing`, read 2026-10-22). Developer is USD 20 a month for 25
concurrent browsers and 100 browser hours, then USD 0.12 an hour.

One browser hour in 15-minute sessions is four sessions a month. That is a
smoke test, not a crawl. On Developer, 300 browser hours is USD 44.00 and 730 is
USD 95.60, because the plan includes the first 100.

⚠ The catalogue figure of USD 899 for 300 hours is an artefact and is wrong. The plan
arithmetic above replaces it.

Evidence: `browserbase.com/pricing` (read 2026-10-22). Verdict: the smallest free
allowance here and a competitive paid rate.

## Browser Use

Browsers cost USD 0.02 an hour, and consumer-connection proxy is USD 5 per GB
(`documented`, `browser-use.com/pricing`, read 2026-10-22). A USD 100 one-time
top-up runs 50 browsers in parallel and credits never expire. A model-driven agent
adds 20 per cent on the model rate plus browser time and traffic.

USD 0.02 an hour is the cheapest published browser hour in this class. At that
rate the proxy is 250 browser hours per gigabyte, so the same conclusion holds
harder: the browser is nearly free and the traffic is the product.

Evidence: `browser-use.com/pricing` (read 2026-10-22). Verdict: the cheapest
browser hour and a proxy price that owns the bill.

## Browserless

Free is USD 0 a month with no card, 1,000 units a month, 2 concurrent browsers and
a 2-minute maximum session, and the paid plans above it are Prototyping at USD 25
and Starter at USD 140 (`documented`, `browserless.io/pricing`, read 2026-10-22).
A unit is up to 30 seconds of one browser connection, and a session reconnect
bills a fresh unit.

1,000 units is 8.3 hours a month if every unit is spent whole. The 2-minute
session cap is the constraint that matters: a crawl that needs a longer session
pays a fresh unit to reconnect and re-establish state.

The consumer-connection proxy is drawn from the same pool at 6 units per MB. One
gigabyte is 1,024 MB, so one gigabyte of consumer-connection traffic is 6,144 units,
or just over six months of the free allowance. That is the same finding as every
other row here: the browser is nearly free and the bytes are the bill.

Evidence: `browserless.io/pricing` (read 2026-10-22). Verdict: a real free
allowance, small, and a proxy price that is a factor of six above the whole free
pool for one gigabyte.

## What did not work

- **Firecrawl as a browser host**: the free plan is real at 1,000 credits a month
  and no card, and a browser minute costs 2 credits, so the free pool is 500
  browser minutes. It is a scraping API with a browser attached rather than a
  browser host, and it is the `crawler-scraper` topic's provider.
- **Browserless as a crawl engine**: the Free plan is 1,000 units a month, and a
  unit is up to 30 seconds of one browser connection, so 8.3 hours. The 2-minute
  session cap makes a reconnecting crawl pay twice for the same page.
- **Cloudflare Browser Rendering at volume**: Workers Free gives 10 minutes of
  browser time a day and 3 concurrent browsers. Ten minutes a day is a smoke test.
  The Durable Object free row does not give a browser.
- **Headless Chromium on a free sandbox**: a Chromium instance needs about 300 MB
  and the free sandbox shapes are 512 MB to 4 GB, so it fits, and the idle reap
  ends it. The host is the constraint, and a purpose-built browser host is the
  better trade.

## Chaining

Lightpanda for the bulk of a crawl and Hyperbrowser for the pages that need a real
engine is the only chain that uses each row for what it is. Lightpanda's
10 hours a month covers server-rendered pages at a lower cost per page; the
Hyperbrowser credit covers the JavaScript applications. Both then write to object
storage, because neither keeps a session.

⚠ The proxy is where the chain breaks. Neither free allowance includes consumer-connection
traffic, so any crawl that needs one is paying per gigabyte from the first byte.
