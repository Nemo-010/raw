# The browser-host long tail: 29 more, and the month that repeats

`free/agent-browser-hosts.md` covers the nine browser hosts a reader would act on
tonight. Thirty-eight records carry `category: browser host`, so twenty-nine are in this
page. The other document's headline carries a defect, and the defect is the finding.

⛔ **`free/agent-browser-hosts.md` states that Hyperbrowser's 50 browser hours a month is
"the largest free browser allowance in this class by a factor of five against the next
row". Ferr's record carries the same 50 hours a month, on the free tier, with 3
concurrent sessions, quoted from the vendor page.** The factor of five is wrong because
the comparison set leaves Ferr out, and the two rows are the joint largest allowance in the
class.

⭐ **The second finding is about recurrence, which the comparison table does not have a
column for.** Five of the 29 rows in this page give a *monthly* browser allowance with no
card: Ferr at 50 hours, Bright Data at 5,000 credits, Remote Browser at 1 hour,
Browsercloud at 1 hour, and ZenRows at 5,000 credits. A one-time grant and a monthly
allowance are different products, and the class's tables mix them.

## The comparison

Sorted by the free allowance, in the unit the vendor states. `Recurs` is the column that
decides whether a crawl can be scheduled.

| Provider | Free allowance | Recurs | Card | Verdict |
| --- | --- | --- | --- | --- |
| Ferr | 50 browser hours a month, 3 concurrent | monthly | no | qualifies-with-caveat |
| Hyperbrowser | 5,000 credits, about 50 browser hours | monthly pool | no | qualifies-with-caveat |
| Bright Data Browser | 5,000 credits, 1 GB included, unlimited concurrent | monthly | no | qualifies-with-caveat |
| Airtop | 1,000 credits a month, plus a 10,000-credit bonus | monthly | no | qualifies-with-caveat |
| ZenRows | 5,000 credits a month, 5 concurrent | monthly | no | qualifies-with-caveat |
| Hyperbeam | 10,000 minutes a month | monthly | no | qualifies-with-caveat |
| Notte | credits across browsers, functions, proxies and tokens, 5 concurrent | monthly | no | qualifies-with-caveat |
| Gologin | a free start, consumer-connection IPs included, USD 1 per GB past the allowance | monthly | no | qualifies-with-caveat |
| Intuned | 3 compute hours, a USD 5 AI credit, 7 days of retention | monthly | no | qualifies-with-caveat |
| Skyvern | 5,000 credits, 1 concurrent run | one time | no | qualifies-with-caveat |
| Browseract | 200 credits, 2 agent builds, 5 local browsers | one time | no | qualifies-with-caveat |
| Tinyfish | Search and Fetch free at any balance; USD 8 wallet for Agent and Browser | rate-limited | no | qualifies-with-caveat |
| Surfsky | signup credit, 10 concurrent, USD 0.35 a browser hour | one time | no | qualifies-with-caveat |
| Scrapfly | 1,000 API credits, 5 concurrent, 1 week of logs | monthly | no | qualifies-with-caveat |
| Cloudaxis | 50 AI credits, 10 browser minutes, 10 searches a month | monthly | no | qualifies-with-caveat |
| H company | up to 3 concurrent agents, rate-limited | not stated | no | qualifies-with-caveat |
| Smooth | a free tier the page does not price | not stated | no | qualifies-with-caveat |
| Opensteer | USD 5 of model credit at signup, USD 5 a month of platform credit | monthly | no | qualifies-with-caveat |
| Remote Browser | 1 browser hour a month | monthly | no | qualifies-with-caveat |
| Browsercloud | 1 browser hour | monthly | no | qualifies-with-caveat |
| Anchor Browser | a free tier on a catalogue card, not read | not stated |  -  | qualifies-with-caveat |
| OpenAGI | a free tier on a catalogue card, not read | not stated |  -  | qualifies-with-caveat |
| Tabstack | a free tier on a catalogue card, not read | not stated |  -  | qualifies-with-caveat |
| ScrapingBee | 1,000 API credits | one time | no | trial-only |
| Cloudbrowser | 7-day trial on Basic, then from USD 25 a month | 7 days | no | trial-only |
| Cloudcruise | 2 automation hours, then USD 3 an hour | a trial | no | trial-only |
| Scrapeless | none |  -  |  -  | paid-only |
| Tilion | none; USD 2,000 a month |  -  |  -  | paid-only |
| Magnitude (self-hosted) | a free tier on a catalogue card, not read | not stated |  -  | qualifies-with-caveat |

⚠ **Four rows are a catalogue card and nothing else.** Anchor Browser, Magnitude, OpenAGI
and Tabstack each carry the literal sentence "the source card records a free tier without
a credit amount". That is a placeholder, not a finding, and it is one of 30 across the
topic, all listed in `gaps.md`.

## Ferr, the row the other document missed

Up to 50 browser hours a month with 3 concurrent sessions on the free tier, quoted from
the vendor as "Up to 50 browser hours / mo" alongside "3 concurrent sessions" and
"Sub-second cold starts on warm containers" (`documented`, `ferr.io/pricing`, read
2026-10-22).

⭐ **This ties Hyperbrowser for the largest free browser allowance in the class and it is a
plain hour count rather than a credit pool.** That difference matters: a Hyperbrowser
credit is shared with four products, so a crawl that uses the agent product spends the
browser budget. Ferr's 50 hours are 50 browser hours.

## The recurring allowances, which are the schedulable ones

A crawl that runs nightly needs a pool that comes back. Nine rows state a monthly figure
and a tenth states a monthly rate limit rather than a pool.

| Provider | Monthly | What one credit buys |
| --- | --- | --- |
| Ferr | 50 browser hours | a browser hour |
| Hyperbeam | 10,000 minutes | a participant-minute of a shared session |
| Bright Data Browser | 5,000 credits and 1 GB | a request, plus the traffic |
| ZenRows | 5,000 credits | a request, and a JS render costs more |
| Airtop | 1,000 credits | an agent step |
| Scrapfly | 1,000 API credits | a request, with an automated-traffic filter as a multiplier |
| Remote Browser | 1 browser hour | a browser hour, and USD 4.90 buys 30 |
| Browsercloud | 1 browser hour | a browser hour |
| Cloudaxis | 10 browser minutes | a minute, plus 50 AI credits |

⛔ **A credit count is not a browser hour and the class's tables treat them
as one.** ZenRows' 5,000 credits and Ferr's 50 hours are not comparable until somebody
states what a JS render costs in credits, and only Hyperbrowser publishes the conversion
at USD 0.001 a credit and 50 hours per 5,000.

⭐ **Bright Data Browser is the only row that includes traffic**: 1 GB a month with the
credits and unlimited concurrency. Every other row sells the proxy separately, which is
the class's central finding in `free/agent-browser-hosts.md`.

## Hyperbeam, the joint largest and a different product

10,000 free minutes every month, then pay as you go, with free participant-minutes counted
separately (`documented`, `hyperbeam.com/pricing`, read 2026-10-22).

⚠ **10,000 minutes is 166 hours, which is the largest raw allowance in the class, and it is
not a browser hour.** Hyperbeam embeds a shared virtual browser in an application, so a
minute is a minute of a session that may have several participants. A cron crawl cannot use
it and a reader comparing it to Ferr's 50 hours has compared two products.

## The self-hosted opt-out

**Browser Linux emulators** is `dead` as a class, for the reason that matters: WebVM is
real Debian on x86 with real Tailscale networking, and the processor is the reader's own
laptop and the machine dies with the tab. It is not remote capacity at all.

⚠ **That does not make it useless and it does make it out of scope.** The corpus records
what can be reached on somebody else's iron. An emulator that runs in the reader's tab uses
the reader's own processor, which is the one thing `METHODOLOGY.md` section 12a excludes.

## What the class does not establish

⛔ **No browser session was opened.** Every allowance here is a vendor sentence read on
2026-10-22.

**No credit-to-hour conversion exists for 30 of the 38.** Hyperbrowser publishes one and
the rest publish a credit count, so the class cannot be ranked in one unit.

**No proxy price was compared across the whole class.** Six rows state a per-GB rate and
the rest bundle it, which is the finding the other document already carries.

**No concurrent-session test was run.** Ten rows state a concurrency cap and none states
what a refused session looks like.

## What did not work

- **Ferr as a runner-up**: it ties for the largest monthly allowance.
- **Hyperbeam as the largest browser allowance**: 166 hours of a shared session is not a
  browser hour.
- **A credit count as a browser hour**: no conversion exists for 30 rows.
- **Scrapeless and Tilion as free rows**: both are `paid-only` with no free tier.
- **Browser Linux emulators as remote capacity** (self-hosted): the machine is the reader's tab.
