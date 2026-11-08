# Two throughput numbers for one host cannot both stand: the CDN read path is cache state, not a rate

- **When:** 2026-10-22T03:51:02Z
- **Status:** corrected
- **Supersedes:** `.tmp/seed/storage-research/ALIST-FINDINGS.md` section "Full sweep results (A11 agent, 45 hosts probed)", the `al.chirmyram.com` row
- **Superseded by:** `docs/netdisk-pan/self-hosted/cdn-fronting.md` section "The measurement that must not be quoted as a curve"
- **Evidence:** `probe.py --concurrency N --shard-bytes N` against a signed CDN URL resolved through `/api/fs/get`, run 2026-10-22; six whole-object reads of a 36,747,196-byte PDF, same session
- **Confidence:** measured

## What we believed

The seed's A11 wave recorded `al.chirmyram.com` as:

> `cf-cache-status: HIT`, **20.2 MB/s single**, **20.48 MB/s at 8 parallel**, 20/20 requests with no rate limit

Two figures that agree to within 1.4%, presented as evidence that the host is
stable under concurrency. The unit is also written as MB/s for a byte count over a
second, which is MiB/s.

## What we found

Six whole-object reads of the same 36,747,196-byte file, minutes apart, one
connection each:

```
11.54   12.54   42.96   43.77   67.43   78.58   79.58    MiB/s
```

A factor of 6.9 between the slowest and the fastest read of **one object from one
host in one session**. Parallel ranged reads made it worse rather than better:

| connections | shard | aggregate | single-stream baseline, same run |
| --- | --- | --- | --- |
| 8 | 8 MiB | 6.5 to 7.7 MiB/s | 18.1 to 51.2 MiB/s |
| 8 | 32 MiB | 10.5 MiB/s | 51.2 MiB/s |
| 32 | 8 MiB | 2.6 to 2.9 MiB/s | 13.1 to 35.5 MiB/s |
| 32 | 32 MiB | 7.5 MiB/s | 13.1 MiB/s |

**Every parallel figure is below its own baseline on the same run.** Eight
connections to one cached object contend for one client uplink, and each
connection's share falls as the count rises.

The one number that is stable is the range read: five attempts at
`bytes=0-1048575` returned 206 with `Content-Range: bytes 0-1048575/36747196` in
**71 to 88 ms**, which is 11.4 to 14.1 MiB/s and is a first-byte-plus-1-MiB figure
from the nearest PoP.

## How we found it

The methodology's sixth rule is "benchmark with parallel ranged GETs and measure a
baseline". Running it as written produced a parallel aggregate **below** the
baseline, which is not a shaping curve and is not a host property. The object was
already in Cloudflare's cache with `age: 21`, so the variable being measured was
the edge's state and the local link.

The seed's two numbers agreeing so closely is itself the tell. Real shaping
produces a curve; two figures 1.4% apart across a 8x change in concurrency describe
a binding constraint that does not move with concurrency, which for a cached object
is the uplink.

## What it cost us

A reader would have taken 20.2 MiB/s as the host's throughput and sized a serving
pool against it. The honest figure is that the read path is **cached at the edge,
ranges honoured, first byte under 90 ms on a warm object, throughput not
established** : which supports a serving decision and does not support a capacity
calculation.

The second cost is a unit. `20.2 MB/s` for a measurement is `MiB/s`, and the
conventions forbid printing one unit and labelling it another.

## What a future session should do differently

**Report a CDN-fronted host with three separate numbers and no aggregate:** the
cache status, the first-byte time on a warm range, and the range size. A throughput
figure from a cached object is a measurement of the cache's occupancy at that
second.

**When a parallel aggregate comes out below its baseline, stop and name the
contention before reporting a curve.** The rule's purpose is to separate host
shaping from signature throttling; a third cause, client-side contention, produces
the same shape and is distinguished by a local control download on the same machine
at the same moment.

**Always run that control.** Neither this session nor the seed's wave did, which is
why neither can say what the ceiling was.
