# Indexes and aggregators

An index lists objects; it does not hold them. A reader needs one that answers a
machine-readable request with no account, because a debrid key without an index
has nothing to fetch.

## The answer

⭐ **`scnlog.me/feed/` is the only DDL feed found that is both ungated and
link-bearing.** It serves RSS 2.0 with 40 items, and the post behind an item
carries nitroflare, ddownload and multiup URLs in clear text with no login. Its
WordPress JSON API returns 401, so RSS is the one machine route it leaves open.

It publishes no rate limit, and none was enforced at the rates measured: ten
sequential requests about 1.3 seconds apart and eight concurrent requests all
returned 200, with no `429` and no `Retry-After`.

## The indexes that answer without an account

| index | what it serves | gate | note |
| --- | --- | --- | --- |
| Scnlog | RSS 2.0, 40 items, host links in the post | none | the only ungated link-bearing DDL feed |
| DDLBase | RSS, 300 items, size in the title | login for more mirrors | deep feed with a hidden cap |
| apibay | JSON search, magnets | none | a torrent index with no key |
| Knaben | JSON search, magnets | none | publishes no number, only a warning |
| eztv | JSON, magnets | none | one catalogue |
| nyaa | JSON and RSS | none | one catalogue |
| torrents-csv | plain text search | none | smallest payload of the set |
| TorrentClaw | JSON, magnets | free key for magnets | publishes its own quota |
| FilePursuit | host search | RapidAPI account | 500/hour, 3,000/day |
| 0daydown | DDL index | VIP for links | live, write-gated |

## The quota that is published in the response

⭐ **TorrentClaw is the only index that states its anonymous quota in the
headers.** A request returns `x-ratelimit-limit: 10`, `x-ratelimit-tier:
anonymous` and a reset 42 to 60 seconds ahead, and the payload carries
`"_notice": "Magnet links, info hashes, and torrent downloads require a free API
key"`. A good number on the wrong side of an identity gate is still a wall, and
this record says both.

⚠ **RLSBB publishes an interval and forbids the crawl in the same file.**
`robots.txt` carries `Crawl-delay: 10` inside `User-agent: * / Disallow: /`, plus
named blocks for GPTBot, Claude-Web, CCBot and FacebookBot. The number is real and
the permission is not.

## What is dead

- **releasebb.net** is parked. The page is a 5,591-byte "Redirecting..."
 interstitial that POSTs fingerprints to `router.parklogic.com` with
 `domainApex: "releasebb.net"`.
- **No public GDrive search engine is alive.** Every 2026 result indexes the
 reader's own Drive rather than a public corpus.
- **Linksave.in and linkcrypt.ws** are dead: one redirects to a `ww17.` parking
 host and the other no longer resolves.

## Containers are not direct links

⚠ **A container resolves to host links, never to a direct link.** Filecrypt
answers 200 to an anonymous container GET and yields host pages plus an optional
captcha. A client that expects `resolve` to return a byte stream will wait
forever on a page it cannot parse.

## How a client should use this layer

1. Poll the RSS feeds that answer without a key: Scnlog and DDLBase.
2. Use one JSON search index for magnets: apibay, Knaben or torrents-csv.
3. Send the resulting host URL to a debrid, or the magnet to a torrent-to-cloud
 service.
4. Never count an index as capacity. It holds nothing.

⚠ **A feed is a list, not an archive.** Retention belongs to the host, and the
host's cap is in [`host-quotas.md`](host-quotas.md).
