# Which browser grants exist, in what unit, and which shape fits?

A headless browser is the only way to read a page a script builds. It is also the
worst-value unit in this market, because a browser bills by time and a job is
counted in pages. The class therefore sorts by one question: **does a single HTTP POST
return the content, or does it open a session?**

The answer: **five grants exist and three of them cannot be used by anything that
answers an HTTP request.** Cloudflare Browser Rendering returns a page from one `POST`
and resets daily. Browserless returns a page from one `POST` and renews monthly at
1,000 units. Browserbase, Hyperbrowser, Steel and Notte are session models, which means
a second request, a socket, or an asynchronous job, and none of them is a read leg
inside a request handler. Anchor returns raw HTML on its REST path and Markdown only
over a browser control protocol, which puts it on the wrong side of the same line.

## The comparison

`Unit` is what one billable thing is, because that is what makes two rows comparable.
`Shape` says whether one request returns the answer.

| Provider | Ceiling | Unit | Shape | Binds | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Cloudflare Browser Rendering | 600 browser-seconds a day on Workers Free | browser-second | one POST, synchronous | `request-rate`: a daily reset | email | qualifies-with-caveat |
| Browserless | 1,000 units a month, 2 concurrent | 30 seconds of connection | one POST, and a crawl job | `retention-clamped`: the unit is time | email | qualifies-with-caveat |
| Browserbase | 1 browser hour, 1,000 search, 1,000 fetch | browser hour | session | `request-rate`: one hour is the whole grant | email | trial-only |
| Hyperbrowser | 5,000 credits on signup, 1 concurrent | credit at USD 0.001 | job | `retention-clamped`: 7 days on results | email | trial-only |
| Steel.dev | USD 30, credited for 90 days | browser-second | session | `retention-clamped`: the credit expires in 90 days | email | trial-only |
| Notte | USD 10, no expiry | session | session, 15 minutes | `retention-clamped`: a 15-minute session | email | trial-only |
| Anchor Browser | USD 5 or 5 credits a month, the two disagree | session | session; Markdown only over CDP | `request-rate`: 5 session creates a minute | email | trial-only |

## Cloudflare Browser Rendering

The Quick Action route returns JSON in the response body: a `POST /markdown` or
`/snapshot` and the content comes back. Nothing outlives the call. On Workers Free the
allowance is 600 browser-seconds a day with 3 concurrent browsers, and the reset is
daily rather than monthly, which is a different failure mode from every other row.

That daily reset is the property worth having. A monthly pool empties on the 14th and
stays empty; a daily one is full again tomorrow, which suits a research workload that
runs in bursts.

⚠ **It converts the whole page.** `/markdown` selects no main content, so a
navigation bar, a cookie banner and a footer arrive with the article. It is a renderer,
not an extractor, and the broker uses it as the rendered-DOM leg whose output its own
extractor reads.

⚠ **Never merge the vendor tier with this deployment's plan.** 600 browser-seconds a day
is Workers Free. The broker's `status.json` reports 1,800 a day and 36,000 a month
because the broker's deployment runs a Paid plan with 20 crawl jobs a day. Quoting the
second as the free tier overstates it threefold.

Evidence: `web.pkgforge.dev/status.json` (read 2026-10-22): pool `browser` 1,800 a
day with 6.8 spent, 36,000 a month with 179.6 spent, one account excluded. The
600-a-day figure is `reported` from the platform's research corpus; the vendor page
was not read.

Verdict: the one browser lane that adds no new third party to a Worker's trust domain,
and a renderer rather than a reader.

## Browserless

1,000 units a month, 2 concurrent browsers, 2 minutes maximum session, no card, with a
`429` documented and a one-shot REST path. A unit is 30 seconds of browser connection
and a reconnect bills a fresh unit.

The unit is the trap. 1,000 units is 8.3 hours of browser time a month, and a
connection bills from open to close whatever the page does. A consumer-connection proxy
costs 6 units a megabyte and a human-verification step 10 units, so a proxied megabyte
is 3 minutes of browser time.

Evidence: `browserless.io/pricing` (read 2026-10-22): "Free ... 1k units/month, 2 max
concurrent browsers, 2 min. max session time"; "A Unit is a block of browser time of
up to 30 seconds per browser connection"; "6 Unitsper MB for Residential Proxy".

Verdict: the only third-party browser with a recurring monthly grant, no card, and a
one-shot REST path. The reserve lane.

## Browserbase

The Free plan gives 1 browser hour, 1,000 Search calls, 1,000 Fetch calls, 3
concurrent browsers and USD 5 in model tokens. Developer is USD 20 a month for 100
browser hours at 25 concurrent, with hours past the included ones at USD 0.12.

One browser hour is one hour. The 1,000 Search and 1,000 Fetch calls are the more
useful part of the plan and are much easier to spend, because they are counted in
calls and not in seconds.

Evidence: `browserbase.com/pricing` (read 2026-10-22): "Free Plan ... 3 concurrent
browsers, 1 browser hour, 1,000 Search calls, 1,000 Fetch calls, USD 5 in tokens".

Verdict: a session model, so a trial. Its Fetch and Search calls are the part worth
using.

## Hyperbrowser

5,000 credits on signup, one concurrent session, 7 days of data retention, and 100
credits an hour of browser use at USD 0.001 a credit. So the grant is 50 browser hours.

⚠ **It renders every page whatever is asked.** Its own crawl documentation says so,
and the broker's crawl answer labels it `x-web-crawl-render: true`. A page that needs
no render still pays for one.

⚠ **Job results are kept 7 days.** A poll after that is a `410` and the work is gone.
That is the retention clock to record beside the price, because the price is worthless
without it.

Evidence: `hyperbrowser.ai/pricing` (read 2026-10-22): "Free ... USD 0 to start, 5,000
credits included, 1 concurrent session, 7 days of data retention"; "100 credits / hour,
USD 0.10 / hour".

Verdict: a trial that is worth its 50 browser hours if the job needs rendering anyway.

## Steel.dev

USD 30 of credits, one time, valid 90 days, with 10 concurrent sessions and 20 requests
a minute on Browser Tools.

⚠ **The 90-day expiry is the binding number, not the USD 30.** A credit that expires
in a quarter is a deadline, and a plan that spreads USD 30 over a year has nothing
left when it is needed.

Evidence: `api.steel.dev/v1/scrape?url=https://example.com` (measured 2026-10-22):
`421` with a 35-byte body reading "No route defined for GET /v1/scrape". The host is
live and the path is wrong, which is a more useful refusal than the `401` every other
browser provider in this set returned. The allowance is `reported`.

Verdict: a trial with a clock.

## Notte

USD 10 of credits, one time, no expiry, 5 concurrent sessions and a 15-minute session
cap, oriented at agent runs rather than at page reads.

⚠ **The 15-minute session is the constraint.** A crawl that needs longer resubmits,
and a session model with a cap is a different design from one without.

Evidence: `api.notte.cc/sessions` (measured 2026-10-22): `401` with a 30-byte JSON body
reading "Not authenticated". The session cap and the allowance are `reported`.

Verdict: a trial with no expiry and a session cap.

## Anchor Browser

The docs state USD 5 of credits a month; the pricing card states 5 credits a month. Both
figures are published and they differ by the price of a credit, which the page read here
does not state.

⚠ **Raw HTML on REST, Markdown only over the browser control protocol.** A single POST
returns HTML, so Markdown needs a CDP connection and that is a session.

Evidence: `api.anchorbrowser.io/v1/sessions` (measured 2026-10-22): `401` with
"Unauthorized, please log in." The two conflicting allowances are `reported` from the
platform's research corpus and are recorded as a disagreement rather than resolved by
choosing the larger.

Verdict: a trial. A published allowance that cannot be converted to pages is not a
ceiling.

## What did not work

- **Anchor's REST path for Markdown**: it returns HTML, so the Markdown route needs a
  session. Measured indirectly: the broker treats it as a session provider and not a
  read leg.
- **A session model inside a Worker**: Browserbase, Hyperbrowser, Steel and Notte all
  need a second request or a held socket. The platform's own rule is that a browser
  option qualifies only if one HTTP POST returns the page content, and these fail it.
- **Browserbase's `format:"markdown"`**: the platform's research corpus records it
  returning `403`. `reported`.
- **Hyperbrowser at one concurrent session**: a crawl across a documentation site
  serialises, so 5,000 credits can take a day to spend.
- **Steel's documented scrape path**: `421 No route defined for GET /v1/scrape`. The
  host is live and the path is not, which is a documented route that does not exist
  (measured 2026-10-22).

## Chaining

A browser is the last rung, not the first. The pattern that works: the broker's
`fetch` for a static page, its `read` for Markdown, and a browser only when the page
is built by script and the extractor returns an empty mount point. When a browser is
genuinely needed, Cloudflare Browser Rendering for one page at a time inside a Worker,
and Browserless when the answer has to be a rendered DOM that something else extracts.
See [`free/reader-extractors.md`](reader-extractors.md) for the extraction step that
sits behind both.
