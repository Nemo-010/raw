# CDN fronting: what the front does to the egress bill

Self-hosting is the last resort, after every hosted mode of this topic (`AGENTS.md`
section 2 rule 9).

A bridge without a CDN pays for every byte twice: once at the upstream and once at
the VPS's uplink. A bridge behind a CDN pays for neither, because the edge caches
the object and serves it. The mechanism is often misquoted, so this document
separates what was measured from what was not.

## The comparison

Sorted by what the front charges for the one thing a reader needs, which is bytes
out.

| front | observed on | cost per byte out | cache behaviour | measured |
| --- | --- | --- | --- | --- |
| Cloudflare | `al.chirmyram.com`, `pan.timero.xyz`, `www.yhcres.top`, `data.yanshiqwq.cn` | none on the free plan | `cf-cache-status: HIT`, `age` present, ranges honoured | yes |
| Tencent EdgeOne | none in this population | not established | not established | no |
| Alibaba ESA | `alist.ucd520.top`, `alist-cdn.20237737.xyz` | not established | not established | no |
| none | `share.xiaole88.com` (Tengine), `alist.jiejingfan.vip` (nginx) | the instance operator's uplink | none | yes, by absence |

⚠ **Three fronts appear in the population and only one was measured.** Fifty-four
per cent of the population sits behind Cloudflare, two hosts behind ESA, and the
rest behind plain nginx or openresty. EdgeOne and ESA are named here because they
are what a Chinese operator would choose and because a discovery loop needs to
recognise them, not because anything is known about their pricing.

## What Cloudflare was measured doing

One object: a 36,747,196-byte PDF on `al.chirmyram.com`, resolved through
`/api/fs/get` to a signed CDN URL on 2026-10-22.

```
GET <signed>            -> 200
                           Server: cloudflare
                           cf-cache-status: HIT
                           age: 21
                           Accept-Ranges: bytes
                           Cache-Control: private, max-age=31536000

GET <signed> -r 0-1048575  -> 206
                              Content-Range: bytes 0-1048575/36747196
                              content-length: 1048576
                              71 to 88 ms across five attempts
                              11.4 to 14.1 MiB/s
```

`cf-cache-status: HIT` is the finding. Cloudflare held the object before the reader
asked, served a byte-identical range, and honoured `Range` correctly with a
`Content-Range` total matching the origin's `Content-Length`.

⛔ **A HIT means the edge already had it, and that changes what the number is.** A
26 to 49 ms first-byte and 11.4 to 14.1 MiB/s on a 1 MiB range is a cache read from
the nearest PoP. It is not the origin's throughput, it is not the provider's
throughput, and it is not a curve.

## The measurement that must not be quoted as a curve

Six whole-object reads of the same file, minutes apart, one connection each:

```
11.54   12.54   42.96   43.77   67.43   78.58   79.58    MiB/s
```

A factor of 6.9 between the slowest and the fastest read of one object from one
host. The object was already cached, so the variance is the edge's state and the
reader's own network, not the host's policy.

Parallel ranged reads made the picture worse, not better:

| connections | shard | aggregate | single-stream baseline on the same run |
| --- | --- | --- | --- |
| 8 | 8 MiB | 6.5 to 7.7 MiB/s | 18.1 to 51.2 MiB/s |
| 8 | 32 MiB | 10.5 MiB/s | 51.2 MiB/s |
| 32 | 8 MiB | 2.6 to 2.9 MiB/s | 13.1 to 35.5 MiB/s |
| 32 | 32 MiB | 7.5 MiB/s | 13.1 MiB/s |

**Every parallel figure is below its own single-stream baseline.** That is the
signature of a shared edge cache and a client-side uplink, not of shaping: eight
connections to the same cached object contend for one client link, and each
connection's share falls as the count rises.

⚠ **This is the measurement a parallel-GET benchmark would misread.** The rule is
"benchmark with parallel ranged GETs against a baseline". Here the baseline is
*higher* than the parallel aggregate. A reader who reported
only the parallel number would call this host slow; a reader who reported only the
fastest single read would call it 79 MiB/s. Neither is a throughput.

⛔ **Report this host's read path as: cached at the edge, ranges honoured,
first-byte under 90 ms on a warm object, throughput not established.** That is the
honest sentence and it is shorter than the wrong one.

⚠ **Two older rates for this host are labelled `MB/s` and their elapsed times were
not kept, so which divisor produced them cannot be recovered.** Read decimally they
are 19.7 and 20.0 MiB/s; read binarily they are 20.2 and 20.48 MiB/s. Both readings
agree to 1.4%, and neither should be quoted as a throughput; the measurement that
carries this host is the 11.5 to 79.6 MiB/s range above.

## What the front actually saves

The arithmetic is the same everywhere: convert to a rate.

The serving workload is a daily 500 GB to 1 TiB, which is 5.8 to 12.1 MiB/s
sustained. A CDN that caches at the edge means the reader's own uplink does not
carry those bytes and the origin's uplink does not either, after the first fetch.

| arrangement | who carries 1 TiB per day | who pays for it |
| --- | --- | --- |
| a bridge with no front | the VPS's uplink, once per request | the reader, in the VPS's bandwidth allowance |
| a bridge behind Cloudflare | the edge, after the first fetch | nobody, on the free plan |
| a public instance behind Cloudflare | the edge, and the instance operator's origin once | nobody billable |

⚠ **Free-plan Cloudflare is not unlimited and the limits are on the request path,
not the byte path.** The free plan's cache serves static bytes without a per-GB
charge; what it constrains is the request rate and the cacheable response types.
That is why other topics price Cloudflare by rule count and not by bytes. This
document does not restate those numbers: the egress topic owns them.

## What the front does not fix

**It does not make a dead origin live.** A HIT is a cache; once the entry expires
and the origin is gone, the next request is a 522. Two mirrors behind one CDN are
what turn a 9-month half-life into a non-event, and that is a mirroring decision and
not a CDN decision.

**It does not fix a signed path.** `pan.ios98.com` returns `code: 401, expire
missing` from its own origin; no front can cache a response the origin refuses to a
guest.

**It does not fix a write.** The one writable instance is Cloudflare-fronted and
its 413 between 100 MiB and 110 MiB is the front's body limit, which is a per-object
cap the instance operator never chose. ⛔ **A CDN adds a limit to an upload path
and it arrives as a 413 with no explanation.**

## Chaining

```
tenant  ->  bridge  ->  Cloudflare  ->  cache  ->  reader
```

The cache is the layer that buys time; the CDN is the layer that buys bandwidth;
the bridge is the layer the reader can replace. The pattern and the reason it beats
any single instance are in [`README.md`](README.md).
