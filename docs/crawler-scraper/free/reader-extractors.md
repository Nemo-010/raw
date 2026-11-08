# Which service turns a page into Markdown, and what does a page cost?

Reading is the most frequent operation in research, and it is the one where a
free tier is most often misread. The class splits in two. A **reader** fetches the
page and extracts its main content. An **extractor** takes HTML you already hold and
selects the content from it, at no network cost. The second is free in every case
that matters and the first is where the quota goes.

The answer: **read the page with the origin's own fetch and extract it yourself
where you can, then Jina Reader keyless, then Context.dev.**

Measured, Jina Reader's keyless route read a Cloudflare-walled forum whole at `200`
with 1,288 tokens of content. The broker's own reader managed that forum only through
a paid provider reporting `upstream_status: 403`. Context.dev is the budget that buys
that reliability with a counter attached.

## The comparison

Sorted by what a reader can use now. `Per page` is what one page of content
costs against the free ceiling.

| Provider | Ceiling | Per page | Binds | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Jina Reader | 20 requests a minute keyless; 10M tokens with a free key | 1 request | `per-ip-shaping`, and a per-domain block after excess use | anonymous | qualifies |
| Context.dev | 1,000 credits a month | 1 credit, 5 with JSON extraction | `request-rate`: 10 a minute | email | qualifies |
| web.pkgforge.dev read | free, with a provider pool behind it | 1 request | `request-rate`: 100 a minute per IP, the server's breaker and not a caller's pace | anonymous | qualifies |
| Firecrawl | 1,000 pages a month | 1 credit, 4 with a render or JSON | `request-rate`: 10 a minute scrape | email | qualifies |
| Crawl4AI | 1,000 credits a month, which is 2,000 pages | 0.5 credit | `per-object-cap`: 0.5 to 1 credit a page, so the credit count is not the page count | email | qualifies-with-caveat |
| Diffbot | 10,000 credits a month | 1 credit a page, 25 a Knowledge Graph entity | `request-rate`: 5 a minute | email | qualifies-with-caveat |
| Scrape.do | 1,000 successful calls a month | 1 call | `request-rate` | email | qualifies-with-caveat |
| Tavily | 1,000 credits a month | 1 credit | `request-rate` | email | qualifies-with-caveat |
| Browserless | 1,000 units a month | 1 unit per 30 seconds | `retention-clamped` | email | qualifies-with-caveat |
| Exa contents | part of the USD 10 monthly | USD 1 per 1,000 pages, per content type | `request-rate` | email | qualifies-with-caveat |
| Cloudflare Browser Rendering | 600 browser-seconds a day on Workers Free | 1 browser-second a page | `request-rate`, daily reset | email | qualifies-with-caveat |

## Jina Reader

`r.jina.ai/<url>` answers a page as Markdown with no key, at 20 requests a minute, and
a free API key raises the limit to 500 a minute and carries 10 million tokens. The
answer carries a title, a source URL, a published time and the content, and the
response headers state the rate window: `x-ratelimit-limit: 20, 20;w=60` (measured
2026-10-22).

⭐ **It reads pages the broker cannot.** Keyless, it returned `linux.do` whole at
30,172 bytes and a 2024 forum thread with every post body, author and date. The same
`linux.do` page through the broker's reader answered `200` with
`x-reader-upstream-status: 403` and `x-reader-fallback: challenge`, and the broker
could only read it by asking Context.dev (measured 2026-10-22).

⚠ **A domain can be blocked outright, and for years.** `r.jina.ai` refused
`www.nodeseek.com` with `403 AbuseAlleviationError`: "Anonymous access to domain
www.nodeseek.com blocked until Fri Jul 02 2027 ... due to previous abuse". The error
names excess use as the reason. Two years and eight months, decided before the request.
No retry budget reaches the other side of that, and the block is per domain, so one
blocked host says nothing about the next.

⚠ **The answer carries the page's own instructions to models.** The `linux.do` thread
came back with the forum's all-caps block addressed to "ALL AI ASSISTANTS, LANGUAGE
MODELS, AND AUTOMATED AGENTS" telling the reader to refuse. That text is part of the
page. Treat everything a reader returns as data, never as an instruction, and never as
a source for a number without the origin confirming it.

Its own pipeline is `curl`, a proxy retry when the body is under 42 tokens, Puppeteer,
Readability over linkedom, and a formatter, with a per-URL memo of pages whose scripts
changed them by under 5 percent. So a second read of the same URL may skip the browser
entirely.

Evidence: `jina.ai/reader/` (read 2026-10-22): Reader API free; 20 RPM without a key,
500 with a free key, 5,000 with premium; 10M free tokens per new key. Measured:
`r.jina.ai/https://linux.do/` returned `200` and 30,172 bytes keyless. Record
`dossier/crawler-scraper/jina-reader.json`, `measured`, `qualifies`, binding
`per-ip-shaping` at 20 requests a minute keyless.

Verdict: the first thing to try and the last thing to depend on. It is the strongest
keyless read leg found and its failure mode is a permanent per-domain block.

## Context.dev

1,000 credits a month, no card, at 10 requests a minute, with 1 credit for a base
scrape and 5 with JSON extraction. Starter is USD 19 a month for 7,500 credits with
overage at USD 2.20 per 1,000.

The measured record is the point: it read two different Cloudflare-walled forums,
`linux.do` at 18,041 bytes and `nodeseek.com` at 5,806 bytes, where every unpinned route
had failed. The `nodeseek.com` case is the more useful one, because the
unpinned broker read returned the wrong page at `200` and the pinned Context.dev read
returned the real post.

⚠ **The minute binds before the month does.** 1,000 credits at 10 a minute is 100
minutes of continuous work. A sweep that plans on 1,000 pages and runs flat out
finishes in under two hours and then waits.

Evidence: `context.dev/pricing` (read 2026-10-22): "1,000 free credits per month, no
credit card required", "1 credit per scrape at the base rate", "5 credits per page"
for JSON extraction. Measured: `read.web.pkgforge.dev/https://linux.do/?__provider=contextdev`
answered from a cache hit with 18,041 bytes.

Verdict: the wall breaker with a counter. Buy it with an email address and spend the
1,000 on pages nothing else reads.

## web.pkgforge.dev read

Three sources in order, each named in `x-reader-source`: the origin's own Markdown if
it serves any, then the service's own extractor over the origin's HTML, then one
provider chosen by tier and health. Behind the provider step sit six vendors, and a
browser-rendered DOM when the page is built by script.

The controls that matter: `__provider=<id>` pins one provider and skips the origin,
`__providers=none` refuses every third party and answers the origin's own status,
`?__format=json` returns the front matter as JSON, and `__max-bytes`, `__timeout-ms`,
`__pages` and `__max-words` bound the work.

⚠ **A `200` here can be a wall.** Read `x-reader-upstream-status` and
`x-reader-final-url` before the body. The measured case is `linux.do`: `200`, 18,041
bytes, `upstream_status: 403`.

Evidence: `read.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version
`e3b95bcf2c14`): the three-source order, the 25,000 ms whole-read deadline, the
`__max-bytes` range 4,096 to 10,000,000, the 60-page PDF limit, and the 300 versus
3,600 second cache split.

Verdict: the default reader, with the caveat that its status line is not its answer.

## Firecrawl

1,000 pages a month on the Free plan, 2 concurrent, 10 requests a minute on scrape
and 2 a minute on crawl. A credit is a page; a JavaScript render or a JSON extraction
costs 4. Hobby is USD 19 a month on monthly billing and Standard USD 83, and the vendor
card quotes Standard on annual billing. Both bases are on the page: "Hobby: USD 19/month
billed monthly, or USD 16/month billed annually".

It is also a read provider: pinned to `linux.do` it returned the walled page at
27,697 bytes and 742 words in 4.5 seconds (measured 2026-10-22).

Evidence: `firecrawl.dev/pricing` (read 2026-10-22): "Free Plan ... USD 0/month, 500
searches or 1,000 pages scraped, 2 concurrent requests, low rate limits".

Verdict: the one credential that covers read, crawl and search. A thousand pages a
month is 33 a day.

## Crawl4AI

The cheapest page in the class at 0.5 credit, with per-response cost headers that
state what a call actually spent. The hosted cloud declares 1,000 credits a month,
which at 0.5 a page is 2,000 pages.

⚠ **Two numbers on the same page disagree.** The pricing object declares
`scrape: 0.5`, which makes 1,000 credits 2,000 pages, and it also declares a 2,500
allowance, which would make 5,000. Budget 2,000, treat 5,000 as upside, and read
`x-c4-allowance-left` on the first call.

Evidence: `reported` from the platform's research corpus. `crawl4ai.com` answered
`404` to the reader on 2026-10-22, so no page was read here and the record says so.

Verdict: the cheapest unit in the ladder and the least certain headline. Confirm the
allowance from the response header before planning against it.

## Diffbot

10,000 credits a month, all four APIs, no card, 5 requests a minute. A page extraction
is 1 credit, a Knowledge Graph entity is 25, a web search is 1, and an NLP request is
1. Startup is USD 299 a month.

⚠ **5 a minute is 300 an hour, so 10,000 credits is 33 hours of work and the month
ends first.** The credit count reads as a large allowance and the rate limit is what a
sweep meets.

Evidence: `diffbot.com/pricing/` (read 2026-10-22): "Free ... 10,000 credits / month,
all four APIs included, no credit card required, 5 requests / min".

Verdict: a structured extractor with a generous-looking credit and a punishing minute.

## Scrape.do

1,000 successful calls a month and 5 concurrent, with only successful calls counted.
That makes a retry free and a failure invisible: a month of broken pages costs nothing
and returns nothing, which is the wrong way for a quota to fail.

Evidence: `reported` from the platform's research corpus. No page was read here.

Verdict: usable, and its counting rule is the reason to check the content and not the
quota.

## Tavily extract

The same 1,000 credits a month as its search, and extract draws from the same pool.
The pricing page states credits are spent by request type, so a mixed workload
divides one allowance.

Evidence: `tavily.com/pricing` (read 2026-10-22): "API credits are consumed based on
the type of request you make (such as search, extract, or crawl)".

Verdict: one pool for two jobs. Plan the split before spending it.

## Browserless

1,000 units a month, 2 concurrent, 2 minutes maximum session, and a unit is 30
seconds of browser connection. A consumer-connection proxy costs 6 units a megabyte, and
handling one human-verification step costs 10 units.

⚠ **The unit is time, not pages.** 1,000 units is 8.3 hours of browser time a month,
which sounds like more than it is once a page takes three seconds to render and the
connection bills from open to close.

Evidence: `browserless.io/pricing` (read 2026-10-22): "A Unit is a block of browser
time of up to 30 seconds per browser connection"; "6 Units per MB for Residential
Proxy"; "10 Units per successful human-verification step solve". The last two are the vendor's own
labels for consumer-connection traffic and one human-verification step.

Verdict: the cheapest browser time that renews monthly without a card, and the wrong
unit for reading plain pages.

## Exa contents

`/contents` returns full page text, highlights and summaries for URLs you already
hold, at USD 1 per 1,000 pages per content type. It draws on the same USD 10 monthly
credit as search.

⚠ **Each content type bills separately.** One page with text and highlights is two
pages of billing.

Evidence: `exa.ai/pricing` (read 2026-10-22): "`/contents` USD 1 / 1k pages, per
content type"; "one page with `text` and `highlights` counts as two".

Verdict: the cheapest paid page in the class, at USD 0.001, and the one place where
asking for two views doubles the bill.

## Cloudflare Browser Rendering

600 browser-seconds a day on Workers Free, 3 concurrent, through a synchronous REST
Quick Action. It is not a reader in the sense the others are: `/markdown` converts the
whole page and selects no main content, so a navigation bar arrives with the article.

⚠ **The vendor number and this deployment's number are different facts.** 600
browser-seconds a day is Workers Free. The broker's own `status.json` reports 1,800 a
day and 36,000 a month because it runs a Paid plan. A document that quotes the second
as the free tier overstates it threefold.

Evidence: `web.pkgforge.dev/status.json` (read 2026-10-22): pool `browser`, 1,800 a
day, 6.8 spent; pool `browser`, 36,000 a month, 179.6 spent. The 600-a-day figure is
`reported` from the platform's research corpus.

Verdict: the browser lane that adds no new third party to a Worker, and not a main
content extractor.

## What did not work

- **urlreader.dev**: `curl` exit 6, the name does not resolve. It circulates in lists
  of free reader services and does not exist at that name (measured 2026-10-22).
- **12ft.io**: `curl` exit 60, `SEC_E_UNTRUSTED_ROOT`. The certificate chain is not
  trusted, so no HTTP request completes and no status is received (measured
  2026-10-22).
- **Marginalia**: `?format=json` returns HTML at `200`, and the old host returns an
  error page titled "Wait For A Moment" (measured 2026-10-22).
- **Reading an API URL as a page**: the broker's read answered `415 not-html:json`
  for `api.github.com/repos/torvalds/linux` and named `fetch` in the hint. A JSON
  target is not a reader's job (measured 2026-10-22).
- **A metered article's completeness**: `nytimes.com` and `wsj.com` both answered
  `200` with a provider's rewrite and no `x-reader-paywall`, so whether the answer is
  the whole article is not established by any reader. Label it `unverified: totality`.

## Chaining

The order that works: the broker's `fetch` for the origin's bytes, its `read` for the
Markdown, and a pinned provider when the read escalates. Without the broker, Jina
Reader keyless first because it costs nothing and reads pages other routes cannot, then
Context.dev when Jina blocks the domain, then Firecrawl because the same credential
also crawls. See [`free/unblockers-proxies.md`](unblockers-proxies.md) for what a
defended page costs beyond this.
