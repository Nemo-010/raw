# The cheapest browser hour, and what a gigabyte of proxy adds

The browser market prices two things and only one of them is in the plan name. A
browser hour is cheap: USD 0.02 to USD 0.12 across this lane. A consumer-connection
gigabyte is not, at USD 5 to USD 12, and a crawl that needs one pays more for a
gigabyte than for a hundred browser hours. This document is about the second
number.

The answer: Browser Use is the cheapest browser at USD 0.02 an hour, with proxy at
USD 5 a gigabyte. Lightpanda's Builder plan is USD 19 a month for 300 hours, which
is USD 0.063 an hour, and it accepts a customer-supplied proxy so it is the cheapest
engine plus whatever proxy the reader already has. Browserbase's Developer plan is
USD 20 a month for 100 hours at USD 0.12 after, and its 15-minute session cap does
not move. Nothing in this lane provides consumer-connection traffic at a price that
survives a terabyte.

## The comparison

By browser hour, at the cheapest published plan. `Proxy` is the marginal price of
a gigabyte, which is the number that decides a crawl.

| Provider | Plan | 300 browser hours | Proxy per GB | Session cap | Verdict |
| --- | --- | --- | --- | --- | --- |
| Browser Use | pay as you go | USD 6.00 | USD 5 | not stated | trial-only |
| Lightpanda | Builder USD 19 | USD 19.00 | customer-supplied | not stated | qualifies-with-caveat |
| Kernel | Hobbyist USD 30 | USD 30.00 | included, unlimited | none | qualifies-with-caveat |
| Hyperbrowser | Startup USD 30 | USD 30.00 | bundled in the credit | not stated | qualifies-with-caveat |
| Steel | Scale USD 250 | USD 44.00 at Launch rates | USD 10 at Launch, USD 6 at Scale | 15 min at Launch | trial-only |
| Browserbase | Developer USD 20 | USD 44.00 | priced separately | 15 min | trial-only |
| Bright Data Browser | USD 7.50 of monthly credit | not read | priced separately | not stated | qualifies-with-caveat |
| Browserless | Prototyping USD 25 | USD 25.00 | 6 units/MB consumer-connection proxy | 15 min at Prototyping | qualifies-with-caveat |
| Cloudflare Browser Rendering | Workers Paid USD 5 | USD 5.00 plus 10 h included | through the edge | 15 minutes | qualifies-with-caveat |

## The proxy arithmetic

A browser hour of ordinary web crawling moves 50 MB to 300 MB depending on what is
being fetched. At 150 MB an hour:

| Proxy price | Cost for 1 TB | Browser hours that 1 TB buys at USD 0.02/h |
| --- | --- | --- |
| USD 5 per GB | USD 5,120 | 256,000 hours |
| USD 6 per GB | USD 6,144 | 307,200 hours |
| USD 10 per GB | USD 10,240 | 512,000 hours |
| not billed (Kernel, boat) | USD 0 | not applicable |

⛔ The ratio is the finding. At USD 10 a gigabyte, one terabyte of proxied traffic
costs the same as half a million browser hours. Any crawl that needs consumer-connection
egress is a proxy purchase with a browser attached, and a plan comparison that
looks at the browser hour has compared the wrong number.

⭐ The corollary: a provider that does not bill proxy traffic, or accepts a
customer-supplied proxy, is worth a large premium on the browser hour. Kernel's USD 30 a
month with unlimited proxy is cheaper than Browser Use's USD 0.02 an hour the
moment the crawl moves a few hundred gigabytes.

## Browser Use

USD 0.02 a browser hour and USD 5 per GB for a consumer-connection proxy, with a USD 100
one-time top-up running 50 browsers in parallel and credits that never expire
(`documented`, `browser-use.com/pricing`, read 2026-10-22).

USD 0.02 is the cheapest browser hour here by a factor of three. Three hundred
hours is USD 6.00, which makes the browser essentially free and the proxy the
product.

Evidence: `browser-use.com/pricing` (read 2026-10-22). Verdict: the cheapest hour
and a proxy price that is the real term.

## Lightpanda

Builder is USD 19 a month for 300 browser hours, then USD 0.08 an hour, with 30
concurrent sessions (`documented`, `lightpanda.io/pricing`, read 2026-10-22).
Explorer is free at 10 hours and 5 sessions. It accepts a customer-supplied proxy at
every tier.

The engine is not Chromium, so the compatibility trade is the decision. For a
server-rendered page it is faster and cheaper per page. For a JavaScript
application it is the wrong tool, and no price makes it the right one.

Evidence: `lightpanda.io/pricing` (read 2026-10-22). Verdict: the cheapest
per-page engine and the narrowest compatibility.

## Kernel

Hobbyist is USD 30 a month with USD 10 of credit, 10 concurrent browsers, unlimited
proxy usage, 7-day session replays and unlimited managed auth (`documented`,
`kernel.sh/pricing`, read 2026-10-22). Usage is USD 0.0000166667 per GB-second with
no charge for idle time or proxies.

⭐ Unlimited proxy on a USD 30 plan is the single most useful term in this lane. At
any real crawl volume it is cheaper than every per-GB row by an order of magnitude.

⚠ The unit is GB-seconds, so the cost follows page weight and not wall-clock. A
heavy page costs more than a light one held for the same time.

Evidence: `kernel.sh/pricing` (read 2026-10-22). Verdict: the best plan for a crawl
that needs consumer-connection egress.

## Browserbase

Developer is USD 20 a month for 25 concurrent browsers and 100 browser hours, then
USD 0.12 an hour (`documented`, `browserbase.com/pricing`, read 2026-10-22). Three
hundred hours is USD 44.00 and 730 is USD 95.60.

The 15-minute session cap is on both Free and Developer. A crawl that needs a
session to live longer must reconnect, and the setup cost per reconnect is real.

Evidence: `browserbase.com/pricing` (read 2026-10-22). Verdict: a competitive rate
and a session cap that shapes how a crawl is run.

## Steel

Launch is pay-as-you-go at USD 0.10 a browser hour against a USD 30 one-time
credit; Scale is USD 250 a month with USD 100 of credits each month, USD 0.08 an
hour, 1-hour sessions and USD 6 per GB of proxy (`documented`, `steel.dev/pricing`,
read 2026-10-22).

The step from USD 0.10 to USD 0.08 requires USD 250 a month, and the session cap
step from 15 minutes to an hour comes with it. That is a cliff rather than a ladder.

Evidence: `steel.dev/pricing` (read 2026-10-22). Verdict: a large one-time credit
and a plan cliff.

## Browserless

Free is USD 0 a month with no card and 1,000 units; Prototyping is USD 25 for
20,000 units and Starter USD 140 for 180,000, at USD 0.0020 and USD 0.0017 a unit
over the plan (`documented`, `browserless.io/pricing`, read 2026-10-22). A unit is
up to 30 seconds of one browser connection, so 300 browser hours is 36,000 units,
which is USD 72 at Prototyping's overage rate.

The consumer-connection proxy is 6 units per MB and the datacenter proxy is 2, so a
gigabyte of consumer-connection traffic is 6,144 units. At Prototyping's USD 0.0020 that
is USD 12.29 a gigabyte, which is the top of the range in this lane and is why the
row does not win on a proxied crawl.

Evidence: `browserless.io/pricing` (read 2026-10-22). Verdict: an entry plan at
USD 25 rather than USD 350, and a proxy price that decides it.

## What did not work

- **A consumer-connection proxy inside the free tier**: no row here includes
  consumer-connection traffic for nothing. Every free allowance is for the browser.
- **Bright Data Browser at USD 7.50 of monthly credit**: the credit is real and the
  per-gigabyte proxy price was not on the page read, so the row cannot be ranked.
- **Firecrawl as a browser host**: 1,000 free credits a month with no card, and a
  browser minute costs 2 credits, so the free pool is 500 browser minutes. It is
  priced per page rather than per browser hour and it is the `crawler-scraper`
  topic's provider.
- **Headless Chromium on a free sandbox**: a Chromium instance needs about 300 MB,
  which fits in a 512 MB free sandbox, and the idle reap ends it. The host is the
  binding constraint and this document exists because that is a bad trade against a
  purpose-built host.
- **Browserless at USD 350**: that is the fourth tier, not the entry. Prototyping is
  USD 25 for 20,000 units and Starter is USD 140 for 180,000, and the Free plan is
  1,000 units a month with no card.

## Chaining

Lightpanda for the bulk and Kernel for the pages that need consumer-connection egress is
the pairing the terms support: Lightpanda is the cheapest per page on
server-rendered HTML, and Kernel is the only plan where proxy traffic does not
dominate the bill. Both write to storage, because neither keeps a session.
