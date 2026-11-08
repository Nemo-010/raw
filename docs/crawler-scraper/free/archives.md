# Which archive answers, how far back, and how do I cite a capture?

An archive answers what a page said on a day. That is the only evidence that survives a
vendor changing its pricing page, and this corpus depends on it.

The answer: **the Wayback Machine.** It answered in 3.2 seconds with a 2024 capture of
a forum that no longer serves its forums. Four archives are worth naming, one of them
is degraded, and one of them is not an archive at all. All four are keyless, so this is
the one class where identity costs nothing.

## The comparison

Sorted by how far back each reaches and how reliably it answers. `Reach` is how far
back a capture exists, which is a different question from the allowance.

| Archive | Reach | Binds | Identity | Verdict |
| --- | --- | --- | --- | --- |
| Wayback Machine | the whole web since 1996, unevenly | `per-object-cap` on paging only | anonymous | qualifies |
| Arquivo.pt | the Portuguese web, and some of the rest | `request-rate`, with a permanent block past it | anonymous | qualifies-with-caveat |
| Common Crawl | crawls from 2008 onward, per crawl | `request-rate`: about 1 a second, and an index that times out | anonymous | qualifies-with-caveat |
| Cloudflare URL Scanner | 30 days | `retention-clamped`: 30 days | email | qualifies-with-caveat |
| urlscan.io | scans somebody submitted | `request-rate` | anonymous | qualifies-with-caveat |
| archive.today | recent captures, unevenly | `request-rate`: `429` on the first request | anonymous | dead |

## Wayback Machine

Keyless listing, closest-match and replay of existing captures, with Save Page Now
needing keys. The CDX server lists a URL's captures oldest first with status, mimetype,
a digest and `record_length`. The Availability API answers a nearest-capture question.
The raw replay at `/web/<timestamp>id_/<url>` returns the body without the archive's
own toolbar.

The measured run is the strongest evidence in this document. `hostloc.com` no longer
serves its forums: every path `301`s to `https://www.miit.gov.cn/`, so a live read
returns a ministry page at `200`. The 2024 capture replays at `200` with 26,000 bytes
and `x-web-origin-status: 200` (measured 2026-10-22).

⚠ **`record_length` is the compressed WARC size, not the body.** A row that says 7,402
bytes describes a record, not a page. Comparing it to a download's length is the
fastest way to conclude a capture is truncated when it is not.

⚠ **A redirect capture does not replay as a redirect.** The Wayback Machine's raw
replay of a `3xx` capture answers with its own redirect to the nearest capture of the
redirect's target. A caller that cites the timestamp it asked for cites a capture it did
not get. Read `x-web-capture-substituted` and `x-web-capture-asked`.

Evidence: `archive.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version
`130dcfbac441`): the capture walk, the substitution headers, and the 3,600-second cache
on a listing. Measured: `/closest?url=hostloc.com/forum.php&at=2024-06` returned `200`
in 3.2 s naming capture `20240530023233` with `compared[]` giving a distance of 163,647
seconds.

Verdict: the archive. Ask it before the live page for anything older than a day.

## Arquivo.pt

The Portuguese web archive, keyless, with a CDX endpoint and a replay. It has no
closest-match operation, so it answers a listing and not a nearest-capture question,
and that is why the broker asks it third.

⚠ **It blocks permanently past its limit.** The platform's research corpus records a
permanent block on exceeding the rate window, which makes it the least forgiving
provider in this census. Its stated limits are 60 CDX requests a minute and 120 replays
a minute.

Evidence: `web.pkgforge.dev/status.json` (read 2026-10-22): probe ok at 01:40Z with 0
consecutive failures. The rate limits and the block behaviour are `reported`.

Verdict: a second opinion on a URL the Wayback Machine does not hold, worth one call
and not worth a loop.

## Common Crawl

Each crawl has its own index on `index.commoncrawl.org` and its own WARC files on
`data.commoncrawl.org`. Up to 12 crawls are asked, newest first, and a URL no crawl
holds is answered `none` without an index call.

⚠ **It is degraded, and the difference between degraded and dead is the finding.** A
direct index call answered `504` after 11.3 seconds, and the broker's own status page
reported nine consecutive probe timeouts at 02:50Z (measured 2026-10-22). It is the
only provider on that page not in state `ok`.

⚠ **An `unknown` crawl is not an absence.** A crawl the listing could not read is
recorded `unknown`, and an empty listing can still carry `more: true` because crawls
remain unasked. `note` says how many. An empty answer from Common Crawl is never
evidence that the page was never archived.

Evidence: `index.commoncrawl.org/CC-MAIN-2026-38-index?url=example.com` (measured
2026-10-22): `504` from nginx after 11.3 s. `web.pkgforge.dev/status.json`: state
`failing`, outcome `timeout`, 9 consecutive failures.

Verdict: usable when it answers and unusable as a dependency. Record the `unknown`.

## Cloudflare URL Scanner

Scans of the exact URL in the last 30 days, read and never submitted by the broker.
A read of a scan's body is three requests: the search, the result and the body.

⚠ **Thirty days is not an archive.** It is a recent-copy cache, and the broker's own
listing says so structurally: a page URL Scanner answered always carries `more: true`
and a `next` with `skip=cfscan`, so the loop never ends on it. A pinned request outside
the window is a `400` that names the reach.

Evidence: `archive.web.pkgforge.dev/llms-full.txt` (read 2026-10-22): the 30-day
window, the `skip=cfscan` contract, the 240-a-minute account window shared with read,
and the 4 requests kept free for a read lookup. Measured:
`/captures?url=nodeseek.com/post-918318-1&limit=2&skip=cfscan` returned 0 captures,
`more: false` and three miss rows.

Verdict: the fallback when the Wayback Machine is slow, and never the answer on its
own.

## urlscan.io

1,000 unlisted and 5,000 public scans a day, 1,000 searches a day and 10,000 result
requests a day, with 30 requests a minute on search. A scan is a page's DOM and
resource list as somebody else's browser saw it.

That is what makes it useful: it is the only source for a page a challenge keeps from
every live fetch, because the scan was recorded by a browser that got through.

Evidence: `urlscan.io/api/v1/search/?q=domain:example.com&size=1` (measured 2026-10-22):
`200`, 1,953 bytes, `results[]` with a canonical URL, no key.

Verdict: a stored scan when nothing else has the page. The limits are `reported` and
one keyless call was measured.

## archive.today

No account and no published allowance.

⚠ **The redirect names a capture that does not exist.** `archive.ph/newest/https://example.com`
answered `302` to `https://archive.ph/20351231145959/http://example.com/`, a timestamp
in 2035, and following it returned `429` with a 59,077-byte page (measured 2026-10-22).
A caller that trusts the redirect records a capture from the future.

Evidence: `archive.ph/newest/https://example.com` (measured 2026-10-22): `302` to a
2035 timestamp, then `429`. `archive.today/` answered `301` with a zero-byte body.
Record `dossier/crawler-scraper/archive-today.json`, `measured`, verdict `dead`,
binding `request-rate`.

Verdict: dead for programmatic use.

## What did not work

- **archive.today**: `302` to a 2035 timestamp, then `429` (measured 2026-10-22).
- **Common Crawl's index on 2026-10-22**: `504` after 11.3 seconds, and nine
  consecutive probe timeouts on the broker's status page (measured).
- **Cloudflare URL Scanner before its 30 days**: a `400` naming the reach. It holds no
  scan there, so a pinned request for 2020 is a refusal and not an empty answer.
- **Reading an archive capture through the reader**: the broker's read accepts a
  `capture/<timestamp>/<url>` URL of its own archive host and reads the Wayback raw
  capture behind it, and refuses another archive's with a `403` that says so. A caller
  that tries the other three through `read` gets the refusal.
- **`web.archive.org` in a browser**: it hangs. Use the broker's archive service
  instead.

## Chaining

An archive is the first rung for an old page and the fourth for a walled one. The
pattern that works: `closest` for the nearest capture to a date, then `capture` for its
body, and `search` with `include_domains` when the archive holds nothing. For a page
that is live but walled, the reader comes first and the archive second. See
[`free/broker.md`](broker.md) for both ladders in one place.
