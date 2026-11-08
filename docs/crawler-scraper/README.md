# How do I read the web at scale, and what do I do when a page is walled?

This topic covers the market for reading the web: search APIs, reader and extractor
APIs, headless browsers, crawl APIs, archivers, and fetch relays. It also covers the
platform broker, because a reader that cannot use the broker cannot verify anything else
here.

The answer in one paragraph. **The free lane is real, and it is enough for research,
not for harvesting.** Four services carry it. The Wayback Machine covers any page older
than a day. Jina Reader and Context.dev read a walled page. The open search classes
find pages at all.

Jina Reader is keyless and read a Cloudflare-walled forum whole at `200` (measured
2026-10-22). That makes it the first thing to try and not the thing to depend on. It
blocks a domain outright after excess use, and `nodeseek.com` is blocked there until 2027.

For volume, one number decides everything: **a provider's credit is not a page.**
ScrapingAnt sells 10,000 credits a month and a default request costs 10, so the tier is
1,000 pages. ZenRows sells 5,000 and a rendered page costs 5, so the tier is 1,000.
Firecrawl sells 1,000 credits and a plain page costs 1, so the tier is 1,000. Three
different headlines, one number.

## The constraint that binds this class

Every provider in this market meters the request, and the request is the wrong unit.
A crawl is one job that spends an unknown number of requests, so the cost is
discovered after it runs. Two multipliers do the damage and both are published:

- **A render multiplies the unit.** ZenRows: 1 credit plain, 5 with JavaScript, 10
  with a premium proxy, 25 with both (`zenrows.com/pricing`, read 2026-10-22).
  Crawlbase states that site difficulty and rendering multiply a group's ladder
  price, and the platform's own research records a factor up to 40.
- **A search result is not a page, and a page is not a result.** Exa bills a base
  price for 10 results and USD 1 per 1,000 above that. SerpApi counts a search with
  100 results the same as an empty one.

So the sentence this topic exists to make impossible is "provider X gives 10,000 free
requests". The sentence it produces instead is "provider X gives 1,000 rendered pages
a month, at 5 concurrency, and the 1,000 arrives as a 10,000 credit headline".

⭐ **The second constraint is the wall.** A challenge page is not an error and does
not have a stable status code. The broker answered `200` with 18,041 bytes for
`linux.do` while the origin had answered `403` (measured 2026-10-22). DuckDuckGo's
HTML endpoint answered `202` with 14,258 bytes and zero results. A caller that reads
the status line records both as wins. What distinguishes them is a header, or a body
check, and never the status.

## The six classes, and the best entry in each

Three of these are exhausted as a capacity source and one is not. The table names the
class, the entry a reader should start with, and the constraint that fails first.
Every number's home is the class document and the record behind it; this table is a
pointer, not a second home.

| Class | Start with | What binds | Identity |
| --- | --- | --- | --- |
| Archive | the Wayback Machine: keyless listing, closest and replay | nothing at the rate a reader needs; paging is by a CDN resume key | anonymous |
| Reader and extractor | Jina Reader keyless at 20 requests a minute, then Context.dev at 1,000 credits a month | `per-ip-shaping` on the keyless route; a domain can be blocked outright | anonymous, then email |
| Search | the broker's search host, then Keenable at 100,000 requests a month | `request-rate` | anonymous through the broker, email direct |
| Crawl | Firecrawl at 1,000 pages a month | `request-rate`: 2 a minute on crawl | email |
| Headless browser | Browserless at 1,000 units a month | `retention-clamped`: a unit is 30 seconds of session | email |
| Fetch relay | ZenRows at 5,000 credits a month | `per-object-cap`: 1 to 25 credits a page | email |

The class documents carry the full tables, one row per provider, with the free tier,
the binding constraint, the identity cost and the verdict. Nine of the 51 records are
`verdict: dead`, and those are the ones worth reading first, because a dead end with
no record is a door that gets opened again.

## The documents

The free lane answers what a reader can start with now. The paid lane answers what a
unit of work costs once the free allowance is gone.

| Document | Answers |
| --- | --- |
| [`free/broker.md`](free/broker.md) | how to run research through the platform broker: the escalation ladder, the forum-snippet shortcut, the paging loops and the failure shapes |
| [`free/search-apis.md`](free/search-apis.md) | which search API to call, in what order, and which regional numbers must not be summed |
| [`free/reader-extractors.md`](free/reader-extractors.md) | which service turns a page into Markdown, and what each one costs a page |
| [`free/headless-browsers.md`](free/headless-browsers.md) | which browser grants exist, in what unit, and which are session-shaped |
| [`free/crawl-apis.md`](free/crawl-apis.md) | which provider can crawl a site, and why every one of them is a job |
| [`free/archives.md`](free/archives.md) | which archive answers, how far back, and how to cite a capture |
| [`free/unblockers-proxies.md`](free/unblockers-proxies.md) | which service reaches past a filter, and what a defended page really costs |
| [`free/keyless-legs.md`](free/keyless-legs.md) | what works with no account at all, measured |
| [`free/web-failure-shapes.md`](free/web-failure-shapes.md) | how the web lies to a researcher: 22 shapes, each with its signature and the probe that detects it |
| [`paid/search-apis.md`](paid/search-apis.md) | the per-1,000 price of a search, and what a result costs above ten |
| [`paid/reader-extractors.md`](paid/reader-extractors.md) | the per-page price of extraction, by feature |
| [`paid/headless-browsers.md`](paid/headless-browsers.md) | the per-browser-hour price, and what a page costs in browser time |
| [`paid/crawl-apis.md`](paid/crawl-apis.md) | what a 1,000-page crawl costs, by provider |
| [`paid/unblockers-proxies.md`](paid/unblockers-proxies.md) | the cheapest defended page, and the multiplier table |

## What this topic does not have

The paid lane exists and is thinner than the free lane. Twenty-three of the 51 records
are free-lane rows and eleven are `measured` rather than read from a vendor page here.
No paid plan was purchased, so a per-1,000 price is a price read from a page and not a
bill. Whether a plan enforces its own overage is not established, and the documents say
so where it matters.

Two things are missing. There is no measured throughput number for any provider, because
measuring one honestly needs a baseline on the same machine. And there is no price for a
provider that sells only through sales, of which Crawlbase's top tier and Bright Data's
enterprise tier are two.

**Nothing here is a statement about terms.** A suspension or a throttle appears as a
one-line technical reliability note.

## How to read the rungs

`measured` means a live call with its status and byte count recorded.
`documented` means a vendor page was read on the date given. `reported` means the
number came from the platform's research corpus or a forum and no first-party page
confirmed it here. Eleven of the 51 records are `measured`, 25 are `documented` and
15 are `reported`.

The topic rots on the market's schedule, not the evidence class's. The window is in
`scripts/dossier/staleness.policy.json` (60 days for this topic on 2026-10-29), because a free
tier is a marketing decision and it is revised quarterly. A record past that window is an open
finding.

## Records that no other document names

This list is generated by `scripts/report/render.py` from the records. It holds each `measured` or
`documented` record of this topic that no other document of `docs/` names, so a reader finds it and
the gate's `links` check counts it as cited. A document that names the record removes
its row at the next render.

<!-- generated:start topic=crawler-scraper kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `brave-search` | Brave Search API | fails-identity | documented |
| `cfai` | Cloudflare Workers AI | qualifies-with-caveat | documented |
| `dataforseo` | DataForSEO | trial-only | documented |
| `firecrawl-keyless` | Firecrawl keyless route | qualifies-with-caveat | documented |
| `linkup` | Linkup | qualifies-with-caveat | documented |
| `mojeek` | Mojeek | fails-identity | documented |
| `octoparse` | Octoparse | qualifies-with-caveat | documented |
| `outscraper` | Outscraper | qualifies-with-caveat | documented |
| `parsehub` | ParseHub | qualifies-with-caveat | documented |
| `scrapingdog` | Scrapingdog | fails-quota | documented |
| `serperdev` | Serper | trial-only | documented |
| `valyu` | Valyu | trial-only | documented |
| `zenserp` | Zenserp | qualifies-with-caveat | documented |
<!-- generated:end -->
