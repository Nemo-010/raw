# The web broker: how to run research through it

`web.pkgforge.dev` is the platform broker. It is free, it needs no key, and every
measurement in this topic was taken through it. A reader that does not know its failure
modes cannot trust its own results. The broker can answer `200` with a wall, with a
truncated body, or over another transport than the one the caller named.

This document is a working manual. A reader who finishes it can run a full research
task: find pages, read a walled page, reach an old copy, crawl a documentation site, and
tell a real answer from a refusal that looks like one. Every number here is `measured`
or quoted from the live contract. The contract version is named where the answer depends
on it.

One fact governs the rest. **A status code from this broker is not evidence about the
origin.** Read the provenance headers first, then the body. The measured example is
`linux.do`: the broker answered `200` with 18,041 bytes, and the origin had answered
`403` (`x-reader-upstream-status: 403`, `x-reader-fallback: challenge`, measured
2026-10-22T02:17Z).

## The seven hosts, and the question each answers

| Host | The question it answers | The one call to paste |
| --- | --- | --- |
| `search` | which pages exist for this query | `sh scripts/broker/broker.sh search "QUERY" --count 20` (20, the most one request returns, is the default) |
| `read` | what does this page say, as Markdown | `sh scripts/broker/broker.sh read https://example.com` |
| `fetch` | what bytes and status did the origin send | `sh scripts/broker/broker.sh fetch https://example.com/ --dump-headers` |
| `crawl` | fetch a whole site, many pages | `sh scripts/broker/broker.sh crawl https://example.com --limit 100` (100, the most one job returns, is the default) |
| `archive` | what did this page say in the past | `sh scripts/broker/broker.sh archive https://example.com --at 2024-06` |
| `research` | which papers exist for this question | `sh scripts/broker/broker.sh research "QUERY" --count 100` (the default); the next page is `research --next URL`, with the answer's `next` link |
| `api.gh` | what is in this GitHub repository | `sh scripts/broker/broker.sh gh repos/torvalds/linux` |

⛔ **Call the broker through `sh scripts/broker/broker.sh`, never with a hand-rolled `curl`**
([`../../../AGENTS.md`](../../../AGENTS.md) section 4, [`../../conventions/README.md`](../../conventions/README.md)
section 7.4). The wrapper maps a broker refusal to exit 4 and an origin refusal to exit 1, and
passes a broker 429 or 503 with `Retry-After` on as `retry_after` and `retry_at`. A raw `curl` line further down this manual documents the HTTP contract
the wrapper calls (a parameter, a header, a paging loop); read it to understand an answer, not to
make a call.

All six broker hosts (every row above except `api.gh`) answered `/healthz` with `200`, Worker version
`328eb5babcb1`, D1 ok in 156 to 203 ms (measured 2026-10-22T04:07Z). The GitHub
proxy has no published contract and is not part of the broker's repository, so its
behaviour is described from observation alone.

Every host publishes four root documents: `llms.txt`, `llms-full.txt`,
`openapi.json` and `SKILL.md`. Read `llms-full.txt` for the host you are about to
use. It carries a version string which is the first twelve hex digits of a digest
over all four, and that string is how a reader tells whether a quoted rule
still holds.

| Host | Contract version, 2026-10-22 |
| --- | --- |
| `fetch` | `891d53061c03` |
| `search` | `75c922fee334` |
| `read` | `0c6c90bbd663` |
| `research` | `b92c62204f7b` |
| `crawl` | `6767245fca12` |
| `archive` | `338ed53460cc` |

The fetch document is the one to re-read before a measurement, because the pin rule
changed. An earlier copy, `7f55a2da79b5`, does not contain the string `not-applicable`;
the live copy contains it four times and states the rule that a pin which cannot apply
is set aside (measured 2026-10-22). A captured copy of all six live contracts is in
`sources/2026-10-22/crawler-scraper/`, so a reader can diff what this document quoted
against what the host serves now.

## The four calls you will use ninety percent of the time

**Search with a host filter.** The filter is the most valuable parameter on the
service, and a provider that cannot apply it is not asked at all.

```bash
sh scripts/broker/broker.sh search "无限存储" --count 20 --domains linux.do,nodeseek.com
```

`count` above 20 is clamped to 20 and the header `x-web-count-clamped: 20` says so
(measured: asked 50, got 20). `q` is at most 400 characters. `include_domains` and
`exclude_domains` take at most 50 hosts each, and a host in both lists is a `400`.

**Read a page.** The path form takes the whole URL. Use the `?url=` form when the
URL itself carries a query string or a fragment, or the reader will treat the
origin's parameters as its own controls.

```bash
sh scripts/broker/broker.sh read https://example.com
sh scripts/broker/broker.sh read "https://example.com/?a=b"
```

The wrapper picks the `?url=` form by itself when the URL carries a query string or a fragment.

⛔ **Never put `-f` on a `read` call.** `read` passes the origin's status through:
an origin's 404, 409 or 422 is answered as a 404, 409 or 422, with the page's
Markdown as the body and the origin's status in `upstream_status`. `-f` turns every
one of those into `curl: (22)` with no body written at all, so the front matter, the
`upstream_status` and the `x-reader-final-url` are deleted, on exactly the walled,
missing and challenged pages this document exists to diagnose. The wrapper does not
put `-f` on `read`, and neither does a raw call: use `-qsS`, and read the status as
information. Measured on one URL:

```text
curl -qfsS .../read/https://example.com/pricing   ->  curl: (22) The requested URL returned error: 404
curl -qsS  .../read/https://example.com/pricing   ->  404, 388 bytes, upstream_status: 404
```

The answer is Markdown with YAML front matter. Read `upstream_status`, `source`,
`title_source`, `words` and `final_url` in that front matter before the content.
`__format=json` returns the same fields as one JSON object (measured 2026-10-22).

⚠ **Check `final_url` against the page you asked for.** An origin can redirect the
broker's egress to a notice page and answer `200`. `nodeseek.com` is the measured
case: 29 words and `final_url: warning.nodeseek.com/ipv6-is-disabled`. Pin a
provider, or reject the answer.

**Fetch the origin's bytes.** `--dump-headers` prints the headers, and `x-web-egress`
is the line that matters.

```bash
sh scripts/broker/broker.sh fetch https://example.com/ --dump-headers | head -40
```

Do not put `-f` on a `fetch` call you are diagnosing. You want the origin's `404`
and `500`, and `-f` turns them into an empty answer with a non-zero exit.

**Ask for the nearest old copy.**

```bash
sh scripts/broker/broker.sh archive https://example.com --at 2024-06
```

That call answered `200` in 2.25 seconds and named capture `20240531235508` with two
`compared[]` entries, one from Wayback at 292 seconds from the instant asked and one
from URL Scanner (measured 2026-10-22T04:02Z). `query.at_asked` echoes the period and
`query.at` gives the instant asked.

## The escalation ladder, when a page is walled

A challenge is a signal to change tool. It is not an obstacle to solve. Try every
rung and every provider pin, with as many reads as each needs; record the gap only
when every route failed, and name the routes tried.

| Rung | Call | What it proves |
| --- | --- | --- |
| 1 | `sh scripts/broker/broker.sh read URL` | the origin answered, or a provider rewrote it |
| 2 | `sh scripts/broker/broker.sh read URL --provider ID`, for each ID that `sh scripts/broker/broker.sh status` lists in `providers` with `read` in its `caps` and a `state` other than `failing` | which provider can read it, and whether the unpinned answer was the wrong page |
| 3 | `sh scripts/broker/broker.sh fetch URL --dump-headers`, with no `--egress` | the origin's own status, and the default chain's escalation |
| 4 | `sh scripts/broker/broker.sh archive URL --at YYYY-MM` | what the page said before it broke |
| 5 | give up, and record `unverified: blocked by challenge` | the attempt count belongs in the finding |

This is the ladder `METHODOLOGY.md` section 7 points at.

The measured outcomes for four real URLs, so a reader can compare a fresh run:

| URL | Rung 1 | Rung 2 | Rung 3 |
| --- | --- | --- | --- |
| `linux.do` | `200`, 18,041 bytes, `upstream_status 403`, `fallback challenge`, provider `contextdev` | `?__provider=firecrawl` gives `200`, 27,697 bytes, 742 words in 4.5 s | origin `403` |
| `nodeseek.com/post-918318-1` | `200`, 623 bytes, 29 words, `final_url: warning.nodeseek.com/ipv6-is-disabled` | `?__provider=contextdev` gives `200`, 5,806 bytes, 257 words, the real post | origin redirects the broker's IPv6 egress to a notice page |
| `reddit.com` thread | `409 challenge`, `x-reader-route: reddit-feed:404` | the `.rss` route reads `422` | the `.rss` through `fetch` answers `404` with a 711-byte Atom body |
| `hostloc.com/forum.php` | `200` with the wrong page, `final_url: https://www.miit.gov.cn/` | not asked | `301` to `https://www.miit.gov.cn/` |

⚠ **Rung 1 can return the wrong page at `200`.** `nodeseek.com` is the case that breaks
trust in the data: 29 words with `confidence: low`, and the `final_url` host is
`warning.nodeseek.com`. The rule that catches it is one line: if `x-reader-final-url`
names a host other than the target's, reject the answer and pin a provider.

⚠ **A wall through `__providers=none` is an honest `403`.** The same `linux.do` read
with that control answers `403 challenge` and the detail names Cloudflare's block
page (measured 2026-10-22). Use it when you need the origin's own refusal rather
than a provider's rewrite.

## The forum-snippet read path

The forums that carry the most useful evidence in this topic are walled to every fetch
path. Search returns the post body in the snippet, and that is the only viable read
path.

```bash
sh scripts/broker/broker.sh search "大盘鸡" --count 20 --domains nodeseek.com
```

Across 20 results for one Chinese query over three forums, snippets ran from 148 to
4,795 characters with a median of 253 (measured 2026-10-22). A platform measurement
on the same day put the median at 585 across 29 forum results, so the median moves
with the query. Treat 150 to 600 characters as the ordinary band and one long result
per page as normal. One snippet carried a whole comparison of nine file hosts in 611
characters.

⚠ **A snippet is a quotation, not a page read.** It supports a `reported` claim
about what somebody wrote. It never supports a `documented` claim about a vendor
page, and it never carries a number in a table on its own.

Search in the language of the ecosystem. A translated term is a different question,
not a synonym.

| Term | Language | What it finds |
| --- | --- | --- |
| `白嫖` | zh | obtaining capacity at no cost: where a free tier is actually used, and what broke |
| `福利` | zh | a discount or campaign an operator posted, usually with the real cap in the thread |
| `羊毛` | zh | a discount campaign: the price edge and the stacking mechanism |
| `大盘鸡` | zh | a large-capacity VPS: storage sold as compute |
| `无限容量` | zh | unlimited capacity, and the threads arguing about whether it is |
| `不限速` | zh | no speed limit, which is a claim to test rather than repeat |
| `网盘直链` | zh | a direct link out of a pan drive: the read path |
| `무제한` | ko | unlimited |
| `無制限` | ja | unlimited |
| `бесплатное облако` | ru | free cloud |

Two failure shapes belong to this read path. `empty[]` names the providers that answered
nothing, and it is not a `200` with zero results and no explanation: one query over
an impossible domain returned `empty: [exa, perplexity, octenai, parallelai]`
(measured 2026-10-22). A `429` from the keyless search leg holds that leg for 600
seconds, and `Retry-After` states it. Retrying sooner meets the same 429; read other
pages and read again after `retry_at`.

## The archive-first rule

For any page that matters and is older than a day, ask for the nearest capture
before the live page. It is fast, it is cached for an hour, and it survives the
origin changing its mind about what it serves.

`hostloc.com` is the measured case. Every forum path now answers `301` to
`https://www.miit.gov.cn/`, so the live read returns a ministry page at `200` with
`final_url` naming the redirect. The 2024 capture replays at `200` with 26,000
bytes and `x-web-origin-status: 200` (measured 2026-10-22).

```bash
sh scripts/broker/broker.sh archive https://hostloc.com/forum.php --at 2024-06
```

The wrapper has no replay subcommand. The replay of one named capture is
`GET https://archive.web.pkgforge.dev/capture/20240530023233/https://hostloc.com/forum.php?provider=wayback`
in the archive host's contract; register a replay you fetched with `scripts/rq capture URL --lane WS --from-file FILE`.

A short `at` is the first instant of its period: `2024-06` is asked as
`20240601000000`, and `query.at` in the answer says so.

⚠ **Never open `web.archive.org` in a browser.** It hangs. Use the broker's archive
service instead.

⚠ **A substituted capture is not the capture you asked for.** Read
`x-web-capture-substituted` and `x-web-capture-asked` before citing a timestamp. The
Wayback Machine never replays a redirect capture as its `3xx`; it redirects to the
nearest capture of the redirect's target instead, and the answer says so.

## What each service can and cannot do

⭐ **A capability set is only as true as the branch that implements it.** Every row below
was measured on the path named, and a capability declared for a service can still be
false on one of its transports. The table therefore says per transport rather than per
service, and `x-web-egress` belongs beside every measurement you record.

| Service | Inputs | Hard caps | What the body is | The one thing it cannot do |
| --- | --- | --- | --- | --- |
| `search` | `q` to 400 characters; `count`, `freshness`, `include_domains`, `exclude_domains`, `rank`, `provider` | `count` clamped at 20; 50 hosts a list | normalised `results[]`, never the provider's bytes | return more than 20 results, or page |
| `read` | a URL; `__provider`, `__format`, `__mode`, `__pages`, `__max-bytes`, `__timeout-ms`, `__max-words` | `__max-bytes` 4,096 to 10,000,000; `__timeout-ms` 1,000 to 25,000; 60 PDF pages | Markdown with front matter, or JSON | give the origin's raw bytes |
| `fetch` | a URL; `__egress`, `__identity`, `__provider`, `__providers`, `__timeout-ms` | `__timeout-ms` to 300,000 | the origin's status, headers and body | forward an origin's framing headers honestly; `cf-fetch` decodes the body and keeps `content-encoding` and `content-length` |
| `crawl` | `url`, `limit` to 100, `depth` to 10, `render`, `main_content`, path globs | body 8,192 bytes; 100 pages a job | each page's provider Markdown | return a crawl in one response |
| `research` | `q` to 1,000 characters and 3,000 bytes encoded; `from`, `to`, `type`, `oa`, `count`, `rank` | `count` at 100 | normalised works | page past 10,000 works |
| `archive` | `url` to 2,048 characters; `from`, `to`, `at`, `limit`, `provider`, `skip` | `limit` clamped at 1,000; `crawls` 1 to 12 | capture rows, or one archived body | reach a capture older than the archive holds |
| `api.gh` | a GitHub REST path | 5,000 core an hour, 30 search a minute, 10 code search a minute | GitHub's own JSON | answer GraphQL, or 10 of 20 paths tried |

⚠ **A conversion spends the deadline, and a big one spends all of it.** A PDF up to 60
pages is read by the service itself with unpdf and answers `x-reader-source: pdf(unpdf)`;
past 60 pages, or when unpdf refuses, it goes to toMarkdown with
`x-reader-fallback: unpdf:<reason>`. `__convert-images=1` sends a document target to the
same converter. ⛔ **The converter's time comes out of `__timeout-ms`, and a deadline
that expires mid-conversion answers `504` with no pages at all.** Measured on
2026-10-22T04:04Z on one image:

```text
$ curl -qsS -D - "https://read.web.pkgforge.dev/https://httpbin.org/image/jpeg?__convert-images=1&__timeout-ms=3000"
HTTP/1.1 504 Gateway Timeout
x-reader-fallback: deadline
{"status":504,"title":"read deadline","detail":"the read stopped early, at 3000 ms of its 3000 ms
 deadline, after it moved on for `tomarkdown:timeout`: 0 ms were left, under the 5000 ms a provider
 walk is started with, so no provider was asked","reason":"deadline","fallback":"tomarkdown:timeout",
 "elapsed_ms":3000,"retryable":true}
```

⚠ **`fallback: tomarkdown:timeout` is the token that names the converter**, and it is how a
reader tells "the page had no text" from "the conversion ran out of time". The two are a
different finding and only one of them is about the page.

The same target with the default deadline answered `200` with 147 words in 20.7 seconds,
because the conversion had the whole budget. So the rule is not "raise the timeout" but
**give a conversion its own call**: do not batch images behind a short deadline, and do
not put `__timeout-ms` on a conversion you want back.

⚠ **A document target can answer with the page about the document.** A provider that
does not read the format returns the landing page, and the front matter says so:
`content_kind: landing-page`, no `pages`, and a word count in the low tens. One PDF read
through `/WAI/ER/.../dummy.pdf` answered `200` with 4 words, `source: provider firecrawl`,
`upstream_status: 403` and `confidence: low`, which is a wall rather than a reading. A
15-page paper read through the same service with `source: pdf(unpdf)` answered 6,150 words
with `pages: 15`. Compare `pages` to the document's own page count before quoting it.

⚠ **`fetch` forwards a decoded body under the origin's framing headers.** Through
`cf-fetch` the runtime decodes the response and leaves `content-encoding` and
`content-length` as the origin sent them, so `HEAD` on a compressing origin reports
a size that is not the size of the body you receive. There is no caller-facing knob
for it. Never forward a proxied `Content-Length` as the object's size; count the
bytes you got.

⚠ **`te` is dropped whatever it carries.** A request declaring `te: trailers`
arrives at the origin without it, so an origin that would have sent trailers sends
none and you cannot tell why. Do not record a `te` value as delivered without an
origin that echoes it.

⚠ **A request body is forwarded on `cf-fetch` only, and the pin is not an error.**
A `POST` with `__egress=cf-sockets` is a `200` via `cf-fetch`, not a `502`: the pin
cannot apply to a request with a body, so it is set aside and `x-web-egress` says
`tried=cf-sockets(not-applicable)+cf-fetch`. Measured twice, with
`__egress=cf-sockets` and with `__egress=broker:socks5`, both `200` with the form
body arriving at `httpbin.org/anything` (2026-10-22T03:57Z). This is the same rule
as `pinned=` below, and it is the sentence that decides whether a POST is possible
at all: it is, over `cf-fetch`, and you cannot choose the transport for it.

⚠ **`cf-vpc` has no observable dial failure.** `x-web-egress` reports
`dialFailureObservable=false` for it, so an unresolvable name, a filtered port and a
working dial all look alike unless something answers. A `502` is the only signal you
get, and it is the service's, not the origin's.

⚠ **`cf-vpc` may leave from a private network, and by port 80 it rewrites the
envelope.** The VPC dial follows the account's Mesh routes (P-32), so a
public-looking destination can be reached from somebody else's WAN. Only that
binding follows them (P-37): `cf-sockets` and `cf-fetch` are safe from the account's
route table, so a VPC dial adds reach, not identity. On a port-80 hop the response
arrives as `HTTP/1.0` with `connection` rewritten and `Server-Timing` and `Cf-Team`
added (P-22), so a `cf-vpc` measurement is not evidence about the origin's own
envelope. Use `cf-sockets` when you need the origin's bytes and framing.

⚠ **A control header can reach a third party.** The transport reads some headers
that the header layer does not strip, so one of the service's own control headers
can be echoed back by the origin. Treat any unexpected `x-` header in an origin's
echo as the caller's, not the origin's.

⚠ **A client that times out early may get a truncated answer with no signal.** A
disconnect cancels the invocation, and `request.signal` does not fire. A short
`--max-time` therefore reports a partial body as a complete one, and no header says
so. Compare the byte count to `content-length`, or to the size you expected, before
trusting an answer taken under a deadline you set.

## The paging loops

Three services page and three do not. `search`, `read` and `fetch` answer whole.
`research`, `crawl` and `archive` hand back a cursor, and each loop is different.

⚠ **`more: true` and a non-null `next` are the normal answer for a query that has
results.** Neither field is a promise that the walk is nearly over. A loop written
as "while `next` is not null" runs until the index's own 10,000-work ceiling stops it,
and a loop written that way on `captures` walks thousands of pages. Real use stops on
`more: false`, on a null `next`, or when it holds the rows the question needs: read
every page the question needs, with no self-imposed budget (`AGENTS.md` section 2
rule 15). `MAX` in each example below is a demonstration size that keeps this
manual's output short, not a limit to copy; each example says which condition
ended it.

**Works search.** Follow `next` and stop on `more: false`, on a null `next`, or when
you hold the works the question needs. Through the wrapper, each page is
`sh scripts/broker/broker.sh research --next URL` with the answer's `next` link. The contract's own limits are the reason a `more: false` is
rare: paging ends where OpenAlex's paging ends, which is at 10,000 works or at a
window the index answers short of its asked size. The cursor is opaque and bound to
`q`, `from`, `to`, `type`, `oa` and `rank`, so it cannot be reused with a different
query. Each page asks the index again and is ranked again, so give `rank=provider`
when you need every work exactly once. The loop counts distinct works, because a
cursor that repeats a page is the failure that looks like progress.

```bash
URL="https://research.web.pkgforge.dev/works?q=vector+database&count=10&rank=provider"
MAX=5   # a demonstration size for this manual, not a limit
PAGE=0
: > "$WS/tmp/ids.txt"   # WS is the workspace, a folder under .tmp/<id>/
while [ "$PAGE" -lt "$MAX" ]; do
  PAGE=$((PAGE + 1))
  BODY=$(curl -qsS "$URL")
  MORE=$(printf '%s' "$BODY" | python -c 'import json,sys;print(str(json.load(sys.stdin).get("more")).lower())')
  N=$(printf '%s' "$BODY" | python -c 'import json,sys;print(len(json.load(sys.stdin)["works"]))')
  printf '%s' "$BODY" | python -c 'import json,sys;[print(w["ids"]["openalex"]) for w in json.load(sys.stdin)["works"]]' >> "$WS/tmp/ids.txt"
  echo "page $PAGE: works=$N more=$MORE total=$(wc -l < "$WS/tmp/ids.txt") unique=$(sort -u "$WS/tmp/ids.txt" | wc -l)"
  [ "$MORE" = "false" ] && { echo "stop: more=false"; break; }
  URL=$(printf '%s' "$BODY" | python -c 'import json,sys;print(json.load(sys.stdin).get("next") or "")')
  [ -z "$URL" ] && { echo "stop: next=null"; break; }
done
[ "$PAGE" -ge "$MAX" ] && echo "stop: example page count $MAX reached"
```

Run at `MAX=5` on 2026-10-22T04:29Z it walked five pages and stopped at the example's
page count, because `more` was true on all five, and every work was new:

```text
page 1: works=10 more=true total=10 unique=10
page 2: works=10 more=true total=20 unique=20
page 3: works=10 more=true total=30 unique=30
page 4: works=10 more=true total=40 unique=40
page 5: works=10 more=true total=50 unique=50
stop: example page count 5 reached
```

The equal totals are the point: a stuck cursor would show `unique` falling behind
`total`, and a `more: true` that never ends is not a stuck cursor. A shorter run at
`count=10` on the same day answered pages of 10 and 2 alternately, because the merge
margin absorbs duplicate versions; a page of two works beside a page of ten is the
merge, not the end of the results. And a query with no results does terminate on its
own: `{"works":[],"more":false,"next":null}` for an impossible query, same day.

**Crawl.** Submit, read `Location` from the response headers, then poll. Three
things the loop must do:
`Location` is **relative** (`/crawl/cj_<32 hex>`), so it is appended to the host;
the job id is the last path segment; and a wrong id answers `400` with a `detail`
that names the format, so the poll must not carry `-f`.

To run a crawl, use the wrapper, which does this loop:
`sh scripts/broker/broker.sh crawl URL`, whose `--limit` is 100 by default, the most
one job returns. A hand-rolled curl against the brokers is never the route
([`AGENTS.md`](../../../AGENTS.md) section 4 step 3). The
block below describes the raw API the wrapper speaks; it is not a command to copy,
and its `sleep` is the poll of a job that runs on the broker, not a pause between
requests.

```text
BASE=https://crawl.web.pkgforge.dev
LOC=$(curl -qsS -D - -o /dev/null -X POST "$BASE/crawl" \
  -H 'content-type: application/json' \
  -d '{"url":"https://developers.cloudflare.com/browser-run/","limit":3}' \
  | sed -n 's/^[Ll]ocation: *//p' | tr -d '\r')
JOB=$(printf '%s' "$LOC" | sed 's#.*/crawl/##')
echo "job: $JOB"
for i in 1 2 3 4 5 6 7 8 9 10; do
  BODY=$(curl -qsS "$BASE/crawl/$JOB")
  STATUS=$(printf '%s' "$BODY" | sed -n 's/.*"status":"\([a-z]*\)".*/\1/p')
  echo "poll $i: status=$STATUS"
  [ "$STATUS" = "completed" ] && break
  [ "$STATUS" = "failed" ] && break
  sleep $(( i < 5 ? 2 : 5 ))
done
```

Run end to end on 2026-10-22T04:32Z, in 23.6 seconds:

```text
job: cj_2356bbd3d9204f7f96f802527fae3e2a
poll 1: status=running
poll 2: status=running
poll 3: status=completed
```

A slower run the same day polled five times and completed in 22.8 seconds, and the
finished job read `completed firecrawl 3 pages {'unit': 'credit', 'amount': 3}`. The
`Location` header it came from was `/crawl/cj_41dd94d7584944bdabf4e70ef44223f0`,
**relative to the host**: pasting it into `https://crawl.web.pkgforge.dev/crawl/` gives
`/crawl/crawl/cj_...` and a `400`.

⚠ **A mistyped job id is a readable `400`, and only if you leave `-f` off.** The
service names the format:

```text
$ curl -qsS "https://crawl.web.pkgforge.dev/crawl/cj_0000"
{"status":400,"title":"bad request","detail":"no such job id: a job id is cj_ and 32 hex digits, as POST /crawl answered it","see":"https://crawl.web.pkgforge.dev/llms.txt","reason":"bad-request","retryable":false}
```

`cj_0000` is a deliberately wrong id, and the `detail` names the shape the service wants.
There is no placeholder to fill in: the id comes from `Location` on the submit.

With `-f` that call returns `curl: (22)` and no body, which is the same defect as
`-f` on `read`. The initial POST answers `202` with a `Location` and a `poll` field
that names the same path, so either works; `202 Accepted` and the `Location` are
both real (measured 2026-10-22T03:31Z and 04:32Z).

**Capture listing.** Follow `next` and stop on `more: false`, on a null `next`, or
when you hold the captures the question needs. A page that Cloudflare URL Scanner answered always carries
`more: true` and a `next` carrying `skip=cfscan`, so a listing can never end on that
archive; the loop ends only on the other archives, and only when they hold no more.
A timestamp window narrows the walk and is the usual way to bound it.

```bash
URL="https://archive.web.pkgforge.dev/captures?url=example.com&limit=3"
MAX=8   # a demonstration size for this manual, not a limit
PAGE=0
: > "$WS/tmp/ts.txt"   # WS is the workspace, a folder under .tmp/<id>/
while [ "$PAGE" -lt "$MAX" ]; do
  PAGE=$((PAGE + 1))
  BODY=$(curl -qsS "$URL")
  MORE=$(printf '%s' "$BODY" | python -c 'import json,sys;print(str(json.load(sys.stdin).get("more")).lower())')
  N=$(printf '%s' "$BODY" | python -c 'import json,sys;print(len(json.load(sys.stdin)["captures"]))')
  printf '%s' "$BODY" | python -c 'import json,sys;[print(c["timestamp"]) for c in json.load(sys.stdin)["captures"]]' >> "$WS/tmp/ts.txt"
  echo "page $PAGE: captures=$N more=$MORE total=$(wc -l < "$WS/tmp/ts.txt") unique=$(sort -u "$WS/tmp/ts.txt" | wc -l)"
  [ "$MORE" = "false" ] && { echo "stop: more=false"; break; }
  URL=$(printf '%s' "$BODY" | python -c 'import json,sys;print(json.load(sys.stdin).get("next") or "")')
  [ -z "$URL" ] && { echo "stop: next=null"; break; }
done
[ "$PAGE" -ge "$MAX" ] && echo "stop: example page count $MAX reached"
```

Run at `MAX=8` on 2026-10-22T04:29Z it walked eight pages and stopped at the example's
page count, with `more: true` and three new captures on every one:

```text
page 1: captures=3 more=true total=3 unique=3
...
page 8: captures=3 more=true total=24 unique=24
stop: example page count 8 reached
```

`unique` equals `total` on every page, so the cursor is advancing and each new row is a
capture this walk had not seen. ⚠ **A loop with no bound on this query never ends.**
`next` carries a Wayback CDX resume key, and the archive holds far more than eight pages
of `example.com`.

A bounded window does terminate on its own, and that is the form to use when the
question is about a period rather than a page count:

```bash
curl -qsS "https://archive.web.pkgforge.dev/captures?url=hostloc.com/forum.php&from=2024-05-29&to=2024-06-02&limit=5"
# {"captures":[1],"more":false,"next":null}  (measured 2026-10-22)
```

An empty listing can also carry `more: true` when a Common Crawl crawl is still
unasked, and `note` says how many are left. That is not a promise of a capture; on an
empty listing `more` means only that an index remains to ask.

## Failure shapes, and what to do with each

| Answer | What it means | What to do |
| --- | --- | --- |
| `400 unknown-transport` | the `__egress` id does not exist; `validTransports` lists four | fix the id; four were listed: `cf-fetch`, `cf-sockets`, `cf-vpc`, `broker:socks5` |
| `403 destination-refused` | the guard refused the target; nothing was dialled | do not retry; the address is loopback, private or a mail port |
| `403 platform-refused` | the platform refused the address after the dial | fatal, no fallback ran; do not retry on that transport |
| `409 challenge` or `login-wall` | the page is a block page or a sign-in wall | pin a provider, or record the wall |
| `413 too-many-elements` | an extraction cap, not a timeout | raise nothing; the page is too large to parse |
| `415 not-html:json` | the target is JSON, not a page | use `fetch`; it answered `415` with that hint on an API URL |
| `422 no-content` | nothing to extract and no provider read it | try a provider pin, or take the page from `fetch` |
| `429 held` | every leg is rate limited or spent | read `Retry-After`; the keyless search leg held 600 s |
| `502 providers-failed` | every provider asked failed | read `errors[]`; an `input-refused` means change the query, not retry |
| `503 disabled` | the service was switched off | read other pages; nothing is established about the target. Read it again later: the broker gave no `Retry-After`, so no time is known. `/healthz` still answers `200` |
| `504 deadline` | the deadline expired | raise `__timeout-ms`, or drop it |
| `530 dns-failure` | the name did not resolve | check the host name; fatal |
| `420` from `api.gh` | the path is not proxied | use a REST path; `/user`, `/emojis`, `/licenses`, `/meta` and `/graphql` all answer `420` with zero bytes |

⚠ **`429` is the one to read twice.** `Retry-After` is a fact and a guess is not.
The measured hold on the keyless search leg was 600 seconds, and the same leg
answered `200` 22 minutes later (platform record, 2026-10-22).

⚠ **A `502` that names `input-refused` is a query problem.** Retrying the same query
buys the same refusal. Only a `5xx`, a timeout or an unreachable host is worth a
retry.

⚠ **A trailing dot is the same DNS name.** `example.com.` and `example.com` resolve
to the same host, and an exact string comparison of hostnames misses it. The
destination guard normalises it; a check you write yourself may not, so strip a
trailing dot before you compare hosts.

⚠ **A `303` to `blocked.teams.cloudflare.com` is a policy block, not the origin.**
Through a VPC dial a Gateway denial arrives as an `HTTP/1.0 303 See Other` injected
into the stream, with `Location: https://blocked.teams.cloudflare.com?...`, about
752 bytes, identical across runs. On 443 the same blocked host produces a synthetic
TLS `handshake_failure` alert instead, and through the binding's own `fetch()` it is
a `200` carrying Cloudflare's block page. Never read a `303` to that host as the
origin's own redirect.

⚠ **A `200` is the honest answer for a proxied success, and only for that.** A
destination the platform refuses arrives as a `200` carrying Cloudflare's error page,
so the status and the body disagree. That is why every claim in this topic carries a
byte count beside its status.

⚠ **`server: cloudflare` is not evidence of a Cloudflare front.** A Worker
`fetch()` response says it for any origin, CloudFront and S3 included. The signal
that a destination is Cloudflare-served is the transport refusal, not the header.

⚠ **A `503 disabled` still answers `200` on `/healthz`.** A service can be switched off,
and the health route reports the Worker and its database, not the routes. A green
`/healthz` is not a working route.

## The provenance headers, and what each is evidence of

| Header | What it proves |
| --- | --- |
| `x-web-egress` | which transport actually dialled; `pinned=` is a request, not a fact |
| `x-reader-source` | which leg answered: `extractor`, `provider`, `pdf(unpdf)`, `tomarkdown` |
| `x-reader-fallback` | why the read escalated: `challenge`, `unpdf:too-large`, `origin-markdown:raw-html` |
| `x-reader-upstream-status` | the origin's own status, also on a provider's answer |
| `x-reader-final-url` | the URL after redirects; a different host means the wrong page |
| `x-web-provider` | which provider answered, on a provider's answer only |
| `x-web-cache` | `hit` means a stored answer, not a fresh one |
| `x-web-body` | `verbatim`, `snapshot`, `rewritten-by=<id>`, `converted`, `extracted` |
| `x-web-rank` | `reranked(bge-reranker-base@...)` or `provider(<reason>)` |
| `x-web-store` | `degraded` means the provider store could not be read and only keyless legs ran |

⭐ **`grep` for `x-web-` and `x-reader-` before you trust an answer, and read three of
them.** `x-reader-upstream-status` says what the origin answered, `x-reader-final-url`
says whether the page is the one you asked for, and `x-web-cache` says whether the
answer is fresh. A fourth, `x-web-rank`, says whether the order was scored or fell back
to the provider's own; a spent Workers AI allocation turns the rerank off silently and
the results still look ranked (`search.web.pkgforge.dev/llms-full.txt`, read 2026-10-22).

⚠ **`x-reader-paywall` is absent when a provider read a metered article.** `nytimes.com`
and `wsj.com` both answered `200` with a provider's rewrite and no paywall header, so the
header's absence proves nothing about completeness. Treat such an answer as
`unverified: totality`.

⭐ **`egress=` is the field to read, and `pinned=` is not.** A pin that cannot apply
is set aside and the request continues. Measured both directions on 2026-10-22:

```text
?__egress=cf-sockets  ->  200  egress=cf-vpc     tried=cf-sockets(not-applicable)+cf-vpc pinned=cf-sockets
?__egress=cf-vpc      ->  200  egress=cf-sockets tried=cf-vpc(not-applicable)+cf-sockets pinned=cf-vpc
```

So a measurement labelled by the parameter it passed may have been taken over
another transport. Record `egress=` and nothing else.

## Readings that look like answers and are not

Four shapes account for most wrong results in this topic. Each is measured.

**A range answer may be a decoded slice.** Asking a gzip origin for bytes 0 to 99
returned `200` with 616 bytes and `decoded=gzip`; the whole body, not a range. The
same header against an identity origin returned `206` with `Content-Range: bytes
0-99/6034`, and the contract's token said `range=decoded-slice(gzip)`. The 100 bytes
matched the first 100 bytes of the full 6,034-byte body (`cmp` identical), so the
slice is of the decoded representation, not of the wire bytes. Naming
`__egress=cf-sockets` gave a real `206` with `responseFramingModified=false` and a
strong ETag.

**`Set-Cookie` survives here (P-1, P-3).** Two cookies through `fetch` against two
direct from the origin (measured 2026-10-22T04:06Z): `Set-Cookie: a=1` and `Set-Cookie:
b=2` arrived as two headers, and the origin's own echo carried the same two. The trap
that deleted them (P-1) was a `cf` cache option in the previous generation of the
Worker: passing any caching option routes the subrequest through Cloudflare's cache, a
response that sets a cookie cannot be stored, and the cache layer removes every
`Set-Cookie` before the Worker sees them. `cacheTtl: 0` reads as "do not cache" and does
the opposite. The second cookie trap (P-3) is independent and survives: a `Headers` copy
built with `set()` in a loop keeps only the last value, and `get("set-cookie")` returns
one joined malformed value, so only `append` is correct. ⚠ **Neither trap is visible
from the status code.** The request succeeds and nothing is logged.

**`x-web-cache: hit` is a D1 row, not the Cache API (P-42).** The zone this broker
runs on carries a cache rule that overrides the Cache API, so the Workers Cache API
stores nothing there: three identical queries four seconds apart answered `miss`
every time with no error from the `put` or the `match`. The stored answers this
service serves come from its D1 database, and a `hit` is shared per colo. Ask what
stored the answer, not what cached it.

**A header mutation is a property of the transport, not of the platform (P-17).** An
answer taken over `cf-sockets` with `identity=browser` once reported
`headers=partial(accept-encoding)` for a header the origin received intact. The
report derived the mutated list from the headers declared rather than from the ones
observed. ⚠ **Record a header fact per transport, never per platform.** A claim that
"the broker rewrites `accept-encoding`" is a claim about one dial on one day.

**`server: cloudflare` is not evidence of a Cloudflare front.** A Worker `fetch()`
answer says it for any origin.

**An unvalidated signature is not a gate, and a walled page is not a `200`.** The
`200` with `upstream_status: 403` is the first and the more expensive of the two.

## What the broker cannot do

Each of these a writer will hit in the first hour. The alternative route is the useful part.

1. **Read a Cloudflare-walled forum through `read` unpinned.** `linux.do` is walled,
   `nodeseek.com` redirects the broker's egress to an IPv6 notice page, and
   `hostloc.com` no longer serves its forums. Use `search` snippets, pin
   `__provider=contextdev` on `nodeseek.com`, and use `archive` for `hostloc.com`.
2. **Pin a transport.** A pin that cannot apply is set aside. Read `egress=`.
3. **Answer GraphQL on the GitHub proxy.** `/graphql` is a `420`. REST only, so
   repository discussions are unreachable and that is a gap to record.
4. **Say whether a metered article is complete.** `nytimes.com` and `wsj.com` both
   answered `200` with a provider's rewrite and no `x-reader-paywall`. Label the
   answer `unverified: totality` rather than "the article".
5. **Guarantee a large download's integrity.** The platform's trap register records a
   stream cut by the CPU budget ending as a clean `200`, and a platform measurement put
   the ceiling at roughly 350 to 650 MB. Measured on 2026-10-22 that ceiling did not hold:
   a 100 MiB file arrived byte-identical to a direct download (SHA-256
   `20492a4d0d84f8beb1767f6616229f85d44c2827b64bdbfb260ee12fa1109e0e` both ways on
   104,857,600 bytes), and a 1 GiB file arrived whole in 33.4 seconds at 30.7 MiB/s. So
   the ceiling is not a fixed size. The hazard is real and unsized: check the byte count
   against `Content-Length` and hash what you keep, and measure throughput against the
   origin with `probe.py`.
6. **Give a byte-exact range of a compressed origin.** Ask for `cf-sockets`, or take
   the whole body.
7. **Date a capture better than the archive can.** Read `x-web-capture-substituted`
   and `x-web-capture-asked` before citing a timestamp.
8. **Archive on demand without Internet Archive keys.** `/save`
   needs Internet Archive keys and answers `202`, then `429` after five saves of one
   URL a day. Ask `/closest` first.
9. **See past Reddit's wall.** The thread is a `409` and the documented feed route
   answered `404` inside the reader. Use search snippets, as for the forums.
10. **Be trusted to answer the same query twice.** Search caches 300 s, read 300 or
    3,600 s by source, an archive listing 3,600 s, a research lookup 24 h. A `hit`
    is a stale answer with fresh headers. Read `x-web-cache` and change a parameter
    when a price or a quota is the fact.

## Traps that are not about the web

Twelve entries in the platform's 42-entry trap register are about how the Worker is
built, not about the web or about using the broker. They are listed once here so
a reader does not look for a lesson in them.

| Trap | Why it is out of scope |
| --- | --- |
| P-4 | a TLS ClientHello field; no writer here builds one |
| P-5 | a socket upgrade flag; no writer here opens a socket |
| P-12 | a frozen clock inside a Worker; timing here is done by `probe.py` |
| P-13 | a TLS 1.3 record nonce; stack construction |
| P-14 | a compatibility ChangeCipherSpec; stack construction |
| P-16 | `wrangler tail` output format; platform tooling |
| P-20 | an ML-KEM export format; a crypto API detail |
| P-24 | a fixed brotli defect whose moral is already the local-test rule |
| P-26 | a stream cap in platform code |
| P-33 | version URL hygiene at deploy time |
| P-39 | placement of an RPC handler; platform architecture |
| P-40 | a pipe between two runtime transform streams; platform code |

The other thirty are routed below.
Fifteen are in this document, each beside the operation it traps, and each carries
its register number so a reader can find the original:

| Trap | Where in this document | The fact |
| --- | --- | --- |
| P-1 | Readings that look like answers | a `cf` cache option deletes every `Set-Cookie` |
| P-3 | Readings that look like answers | `set()` in a copy loop keeps one `Set-Cookie` |
| P-7 | What each service can and cannot do | `fetch()` hands back a decoded body under the origin's framing headers |
| P-10 | What each service can and cannot do | `te` is dropped, whatever it carries |
| P-17 | Readings that look like answers | a header mutation is a property of the transport, not the platform |
| P-21 | What each service can and cannot do | a refused VPC dial is not an error; `dialFailureObservable=false` |
| P-22 | What each service can and cannot do | the VPC port-80 hop rewrites the response envelope |
| P-23 | Readings that look like answers | a Gateway denial arrives as an injected `HTTP/1.0 303` |
| P-27 | What each service can and cannot do | a capability set is only as true as the branch that implements it |
| P-29 | Readings that look like answers | a trailing dot is the same DNS name |
| P-30 | What each service can and cannot do | a control header the transport reads can reach a third party |
| P-31 | What each service can and cannot do | a client disconnect cancels the invocation and `request.signal` never fires |
| P-32 | What each service can and cannot do | a VPC dial follows the account's Mesh routes |
| P-37 | What each service can and cannot do | only the VPC binding follows Mesh routes |
| P-42 | Readings that look like answers | `x-web-cache: hit` is a D1 row, not the Cache API |

The fifteen that are rules for any researcher rather than facts about this broker are
collected in [`web-failure-shapes.md`](web-failure-shapes.md), which names each shape,
its signature and the probe that detects it.

## Evidence

- `fetch.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, version `891d53061c03`,
  captured at `sources/2026-10-22/crawler-scraper/broker-fetch-llms-full.txt`):
  the pin rule, the `range=decoded-slice` token, the 300,000 ms deadline, the
  `x-proxy-forward-set-cookie` default, the list of `403` and `530` reasons.
- `search.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, `75c922fee334`,
  captured in the same directory): the 20-result clamp, the 400-character query,
  the 300-second cache, `empty[]`.
- `read.web.pkgforge.dev/llms-full.txt` (read 2026-10-22, `0c6c90bbd663`, captured):
  the 4,096 to 10,000,000 byte cap, the 25,000 ms deadline, the 60-page PDF limit,
  the 300 and 3,600 second cache split, and the rule that an origin's 4xx page is
  answered with the origin's status.
- `crawl.web.pkgforge.dev/llms-full.txt` (`6767245fca12`), `archive` (`338ed53460cc`)
  and `research` (`b92c62204f7b`), captured in the same directory: the 100-page job,
  the 8,192-byte body, the 1,000-capture page, the 12-crawl limit, the 30-day URL
  Scanner reach, and the paging ceilings this document quotes.
- `web.pkgforge.dev/status.json` (read 2026-10-22T03:40Z, captured as
  `sources/2026-10-22/crawler-scraper/broker-status.json`): 27 providers, and
  capability counts of search 14/14, read 14/14, fetch 8/8, crawl 4/4, works 5/5,
  archive 3/4.

Every command in this document was run, at the timestamp beside it. The re-runnable form
of each measurement is the command itself: status, byte count and headers are quoted
inline, and a reader can reproduce any one of them with the call printed above it.

The broker itself has one record, `dossier/crawler-scraper/web-pkgforge.json`,
`measured` and `qualifies` on binding `request-rate`: free to every caller with no
key, no account and no quota, with a spend breaker that can cap each caller IP at
100 requests per 60 seconds for at most 12 hours. Its seven root documents carry a
version string that moves, and the large-body ceiling is the finding worth keeping:
1 GiB (1,073,741,824 bytes) arrived whole in 33.39 s, which is 30.67 MiB/s, against
the platform's 350 to 650 MB figure.
