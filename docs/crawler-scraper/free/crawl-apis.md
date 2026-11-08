# Which provider can crawl a site, and why is every one of them a job?

A crawl asks for many pages from one site. Every provider in the class implements it
the same way: submit a job, then poll it. None returns a crawl in one response body.
That single fact decides the whole class. A crawl is a two-request shape with state
between the requests, and anything that answers one HTTP request cannot hold it.

The answer: **Firecrawl for the free allowance.** One measured job took about ten
seconds for three pages at 3 credits. Four providers sit behind the broker: Cloudflare
Browser Rendering, Firecrawl, Hyperbrowser and ZenRows. They differ on one axis that
matters, which is what the per-page unit is and what multiplies it.

## The comparison

`Per page` is the unit charged for one page, before any multiplier. `Binds` is what
fails first.

| Provider | Ceiling | Per page | Binds | Job cap | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Firecrawl | 1,000 pages a month | 1 credit, 4 rendered or JSON | `request-rate`: 10 a minute scrape, 2 a minute crawl | 100 pages | email | qualifies |
| Cloudflare Browser Rendering | 600 browser-seconds a day on Workers Free | 1 browser-second | `request-rate`: 20 crawl jobs a day on this deployment | 100 pages | email | qualifies-with-caveat |
| ZenRows | 5,000 credits a month | 1 plain, 5 rendered, 10 proxied, 25 both | `per-object-cap`: the per-page multiplier | unpublished | email | qualifies-with-caveat |
| Crawl4AI | 1,000 credits a month, which is 2,000 pages | 0.5 credit | `per-object-cap`: 0.5 credit a page | 50 URLs a batch | email | qualifies-with-caveat |
| Hyperbrowser | 5,000 credits on signup | 1 credit, +5 JSON, +9 unmarked mode | `retention-clamped`: 7 days on job results | 1 concurrent | email | trial-only |
| Apify | USD 5 of usage a month | a compute unit, not a page | `per-object-cap`: a compute unit is not a page | 5 concurrent runs | email | qualifies-with-caveat |
| Browserless | 1,000 units a month | 1 unit per 30 seconds per connection | `retention-clamped`: the unit is time, not pages | 2 concurrent | email | qualifies-with-caveat |

## Firecrawl

1,000 pages a month on Free, 2 concurrent browsers, 10 requests a minute on scrape and
2 a minute on crawl. The job takes `url`, `limit` up to 100, `depth` up to 10, a render
flag, a main-content flag and path globs. It returns `202` with a `Location`, and the
poll returns pages at most ten at a time.

This is the one crawl measured end to end here.

```bash
curl -qfsS -X POST "https://crawl.web.pkgforge.dev/crawl" -H 'content-type: application/json' -d '{"url":"https://developers.cloudflare.com/browser-run/","limit":3}'
```

`202` with `Location: /crawl/cj_...`; `running` with empty `pages` on the first poll
about five seconds in; `completed` with 3 pages and `usage: {unit: credit, amount: 3}`
by about ten seconds; provider `firecrawl` (measured 2026-10-22).

⚠ **A credit is a page and a render is four.** A crawl of a script-built site costs four
times its page count, so 1,000 credits is 250 rendered pages.

Evidence: `firecrawl.dev/pricing` (read 2026-10-22): "Free Plan ... 500 searches or
1,000 pages scraped, 2 concurrent requests, low rate limits". Measured: one job, 3
pages, 3 credits, about 10 seconds.

Verdict: the crawl leg to start with, and the only provider here that also reads and
searches on one credential.

## Cloudflare Browser Rendering

The crawl route submits a job on Cloudflare's browser fleet. It follows absolute links
and root-relative links, and it does not follow a link written relative to the page,
which is how MkDocs writes every link.

⚠ **An unrendered crawl of a MkDocs site ends at its start page.** The reason is
`links-not-followed`, and it is not a failure of the provider: the links are written
`rules/` and `../faq/` and Browser Run follows only `https://...` or `/docs/...`.
Rendered, it follows the links the browser resolves. The measured run of such a site
was 4 pages in 21 minutes and 5.8 browser-seconds, which is a useful shape of number:
the wall clock was 21 minutes and the bill was six seconds.

⚠ **It answers each page whole and refuses `main_content`.** A job that asks for main
content never goes to it.

Evidence: `crawl.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version
`4504f25e0613`): the link-following rule, the render behaviour, and the refusal of
`main_content`; the 4-pages-in-21-minutes measurement is the platform's own, dated
2026-10-21, and is `reported` here.

Verdict: the right crawl when the pages are on a site whose links are absolute, and
the wrong one for a documentation generator that writes relative links.

## ZenRows

`POST /v1/crawls` submits and the poll reads the job. A plain page is 1 credit, a
rendered page 5, a premium proxy 10, and both 25.

⚠ **A crawl that reserves 1 credit a page and enables rendering under-reserves
fivefold.** That is the single most expensive arithmetic error available in this class,
and it is why the platform's own rule is to reserve the maximum of the applicable
weight rather than the headline.

Evidence: `zenrows.com/pricing` (read 2026-10-22): "Standard page 1 credit", "With
JavaScript rendering 5 credits", "With premium proxies 10 credits", "JavaScript and
premium proxies 25 credits".

Verdict: the cheapest plain page and the most expensive defended one. Read the
multiplier before the ceiling.

## Crawl4AI

`POST /scrape/jobs` then `GET /scrape/jobs/{id}`, or `POST /scrape/batch` with up to 50
URLs which streams its answers. 0.5 credit a page, 10 requests a minute, 2 concurrent,
and per-response cost headers that state what the call spent.

⚠ **Two published allowances disagree.** The pricing object declares `scrape: 0.5`,
which makes 1,000 credits 2,000 pages, and it also declares `limits.community.allowance_per_month:
2500`, which would make 5,000. Budget 2,000 and read the header.

Evidence: `reported` from the platform's research corpus. `crawl4ai.com` answered `404`
to the reader on 2026-10-22, so no page was read here.

Verdict: the cheapest page unit in the class, with the least certain headline.

## Hyperbrowser

`POST /api/web/crawl` then a poll. 1 credit a page, plus 5 for JSON output and 9 for
the unmarked profile mode. One concurrent session on the free plan.

⚠ **It renders every page whatever is asked, and it takes no `depth`.** Its crawl
answer is labelled `x-web-crawl-render: true`, and a job with a depth goes to another
provider because Hyperbrowser cannot take one.

Evidence: `hyperbrowser.ai/pricing` (read 2026-10-22): "Free ... 5,000 credits
included, 1 concurrent session, 7 days of data retention". The capability limits are
from `crawl.web.pkgforge.dev/llms-full.txt` (read 2026-10-22).

Verdict: a trial, and the wrong leg for a plain crawl.

## Apify

Actors run on Apify's compute and are billed in compute units, with USD 5 of usage a
month on Free, 5 concurrent runs, and a proxy at USD 8 a gigabyte.

⚠ **A compute unit is not a page.** The free allowance buys an unknown number of pages
until the Actor's own price is counted, and the Actor is usually somebody else's. The
cheapest thing here is the Actor store, not the compute.

Evidence: `apify.com/pricing` (read 2026-10-22): "Free ... USD 5 included usage a
month, USD 0.2 per CU, 16 GB memory, 5 concurrent runs".

Verdict: a place to run somebody else's scraper, which is a different job from asking
for pages.

## Browserless

`/crawl` submits a job, and a unit is 30 seconds per connection rather than per page. 2
concurrent on Free.

⚠ **The bill is time and the unit is per connection, not per page.** A crawl of fifty
fast pages in one connection can cost less than a crawl of five slow ones.

Evidence: `browserless.io/pricing` (read 2026-10-22): "A Unit is a block of browser time
of up to 30 seconds per browser connection"; "Session-reconnects count as new browser
connections and incur a fresh Unit charge".

Verdict: the right crawl for a few slow pages and the wrong one for many fast ones.

## What did not work

- **A crawl through the search contract**: search is one call with a known cost, one
  refusal signature and one retry. A crawl has none of the three, because the cost is
  discovered after the job runs, the refusal is a job status and not an HTTP code, and
  the retry is a resume rather than a replay. `reported` from the platform's research.
- **Cloudflare Browser Rendering on a relative-link site**: the job ends at the start
  page with `links-not-followed` (`crawl.web.pkgforge.dev/llms-full.txt`, read
  2026-10-22).
- **A crawl pinned to a provider that cannot apply the globs**: ZenRows and Hyperbrowser
  cannot, so a job with `include_paths` never goes to them and a pin is a `503`.
- **A crawl of more than 100 pages in one job**: `limit` is capped at 100 and the
  answer's `limit` says which cap applied.
- **Polling forever**: a job nobody polls is settled or released by the service's cron
  after twice the provider's expected run, and a job id is deleted 15 days after it
  started, after which a poll is a `404`.

## Chaining

A crawl is the last thing to reach for, because its cost is unknown until it finishes.
The order that works: the broker's `read` for the pages already known, the broker's
`search` with `include_domains` to find the pages, and a crawl only when the site has
no sitemap and no index reaches it. When a crawl is needed, Firecrawl submits and
Browser Rendering renders its one page at a time. See
[`free/reader-extractors.md`](reader-extractors.md) for the extraction that turns each
page into something a model reads.
