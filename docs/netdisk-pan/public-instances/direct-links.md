# Direct links: resolving a share link into a fetchable URL

Most consumer pans do not offer WebDAV and do not expose a mountable API. They
offer a share link, which is a web page. Turning that page into a URL a ranged
`GET` can read is the job of a resolver, and one project does it for nineteen pans
at once.

This document covers the resolver, what it reaches for free, what it puts behind a
key, and the two pans whose per-file caps make the answer useless anyway.

## The comparison

`lz.qaiu.top` is the free endpoint and `189.qaiu.top` is the paid one. The split
between them is the map of which pans still resist programmatic access.

| tier | endpoint | identity | what it reaches | measured |
| --- | --- | --- | --- | --- |
| free | `lz.qaiu.top` | none | Lanzou, iLanzou, movably, FeijiPan, Fangcloud, 123pan, WenShuShu, Lenovo, Ctfile, Cloudreve, ecpan | 500 with the driver's own error, no key |
| paid | `189.qaiu.top` | an `X-API-Key` header or a `token` parameter | adds Baidu, Xunlei, Quark, UC, 139, 189 | 401 without a key |

The 500 in the free row is the proof that the free path is live: the endpoint
answered without a credential and reported the driver's own parse failure rather
than refusing the request.

```
GET https://lz.qaiu.top/parser?url=https%3A%2F%2Fwww.123pan.com%2Fs%2Fabc
500  {"code":500,"msg":"123网盘-ye: url=... - 解析异常: 获取分享信息失败: ShareKey格式异常"}

GET https://189.qaiu.top/parser?url=https%3A%2F%2Fpan.baidu.com%2Fs%2Fabc
401  {"code":401,"msg":"未提供API Key（请在请求头X-API-Key或URL参数token中提供）"}
```

⛔ **The 401 is the finding, not an obstacle.** It says the paid tier is a key and
not a different parser, and it names exactly which pans the free tier cannot
reach.

## The driver table, which is the per-pan capability matrix

The project's own documentation (read 2026-10-22) states each driver's free-download
capability and its per-file limit. This is the most compact first-party statement of
what each pan allows, and it is worth reading as a table rather than as prose.

| pan | driver | no-login download | encrypted share | free space | per-file limit |
| --- | --- | --- | --- | --- | --- |
| Lanzou | `lz` | yes | yes | unlimited | 100 MiB |
| iLanzou | `iz` | yes | yes | 10 GB | none stated |
| WenShuShu | `ws` | yes | yes | 10 GB | 5 GB |
| movably (ecpan) | `ec` | yes | yes | 5 GB personal | none stated |
| FeijiPan | `fj` | yes | yes | 10 GB | none stated |
| Fangcloud | `fc` | yes | yes | 100 GB, real-name required | none stated |
| 123pan | `ye` | yes | yes | 2 TB | 100 GB, above 100 MiB needs a login |
| WPS Docs | `pwps` | yes | no | 5 GB | 10 MiB free |
| Quark | `qk` | **no** | yes | 10 GB | none stated |
| UC | `uc` | **no** | yes | 10 GB | none stated |

⚠ **Two columns decide different things.** The per-file limit sets the shard size.
The free-download column sets whether the resolver is useful at all: a pan that
requires a login to download a share cannot be a resolver target no matter how
large its free space is.

**What that table says about the Chinese pan market.** The pans with the largest
free space have the smallest per-file caps or the strictest download gates. 123pan
gives 2 TB and stops serving a share above 100 MiB without a login. Lanzou gives
unlimited space and 100 MiB per file. Quark and UC give 10 GB and refuse a share
download outright. The generous quotas and the programmatic access are on opposite
sides of the table.

## The other resolver, and what it costs

`netdisk-fast-download` is not the only project of its kind. The corpus carries a
record for `189-qaiu-top-netdisk-fast-download-baidu-xunlei-quark-uc` under
the storage topic; this topic's record is
`dossier/netdisk-pan/netdisk-fast-download.json` and it is scoped to the resolver's
role as a read path rather than to its pans.

⛔ **One provider, one home.** The storage topic owns the pans' quota numbers. This
document owns the resolver's behaviour and links to the driver table. If the two
disagree, the storage record is right about a pan's quota and this document is
right about whether a share resolves.

## The operational limits, which the project states itself

The README (read 2026-10-22) carries three warnings that belong in a specification
rather than a footnote:

- **Do not depend on `lz.qaiu.top`.** It asks users to self-host or run it on their
  own server. A public instance of a resolver has the same half-life problem as a
  public instance of a pan.
- **Heavy request volume gets the server restricted by the pan vendors.** The
  resolver is a client of the pans, so its IP is the one the pans throttle.
- **FeijiPan blocks most mainland datacentre IPs** and has been closing accounts
  frequently, which the project warns about in its own words.

⚠ **A resolver is a hop, and a hop is not capacity.** It consumes no storage and
holds no bytes between the write and the read: it returns a 302 to the pan's CDN.
Counting a resolved link as storage would inflate a total with a number that cannot
be written twice.

## The signed-URL lifetime, which is the parameter that breaks a downloader

The resolver returns a redirect to the pan's own CDN, and those URLs are
short-lived. A ChinaMobileEOS redirect with a 24-hour signed link is recorded; no
lifetime was re-measured on any driver, because every free-driver parse attempted
failed on the share key rather than reaching the redirect.

⛔ **`unverified` on the lifetime, with the reason.** No share link with a valid
key was available, so no signed URL was minted and no expiry was observed. The 24
hours is a `reported` figure, not `measured` here.

The design consequence does not depend on the number: **re-resolve per request,
never cache a resolved URL.** A cached signed URL is a 301 with zero bytes once it
expires.

## What the resolver cannot do

It cannot enumerate a folder tree behind a share beyond what the share exposes, it
cannot write, and it cannot authenticate a pan that requires a cookie. The pans
that need a configured cookie (Quark, UC) are listed as supported and are
unusable without one, which is a different kind of key from the paid tier's
`X-API-Key`.

It also cannot help with a pan that has closed share downloads to logged-out
visitors, which is the direction every large Chinese pan has moved.

## Chaining

The resolver's place in the stack is narrow and real: it turns a share link into
an HTTP GET, and an HTTP GET is what a cache, a mirror and a `Range` request can
work with. It sits after
[`alist-openlist.md`](alist-openlist.md) has established that no API is available
and before anything is stored anywhere.

```
share link  ->  resolver  ->  302 to the pan's CDN  ->  ranged GET  ->  cache
```

⛔ **Never put a resolution inside a serving path.** A resolver that is down or
rate-limited takes the whole path with it, and the pan vendors throttle the
resolver's IP and not the reader's. Resolve once, store the target rather than the
URL, and serve from a cache.

`lz-qaiu-top-netdisk-fast-download-keyless-multi-pan-dire` is the record for the hosted
instance, as distinct from `netdisk-fast-download-anonymous-multi-pan-parser` for the
self-hostable project. The first covers what the public endpoint resolves and the second
covers the parser library.
