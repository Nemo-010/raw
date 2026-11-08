# WebDAV fronting: the published guest credentials, and what breaks

A public AList instance exposes its storage twice: once as a REST API and once as
a WebDAV endpoint at `/dav`. The WebDAV endpoint is the one that matters to a
reader, because any desktop file manager and any mount tool speaks it, and because
the community index publishes the guest credential next to the site name.

This document covers what the WebDAV path actually does, measured against four
hosts on 2026-10-22, and what stops working.

## The comparison

Sorted by whether a published credential returns the filesystem.

| instance | endpoint | credential | PROPFIND result | verdict |
| --- | --- | --- | --- | --- |
| `al.chirmyram.com` | `/dav/` | `alist` / `alist` | 207, 581 bytes | works |
| `zhuifan.link` | `/dav/` | `guest` / `guest` | 207, 527 bytes | works |
| `alist.qsesvick.top` | `/dav/` | `davguest` / `davguest` | 207, 581 bytes | works |
| `pan.lm379.cn` | `/dav/` | `public_dav` / `public` | HTTP 524 after 31 s | fails at the front |

## What a 207 actually is

`PROPFIND` with `Depth: 0` returns `207 Multi-Status` and an XML body listing the
collection's own properties. A one-line request and a 581-byte answer is the whole
test:

```bash
curl -sS -X PROPFIND -u alist:alist -H 'Depth: 0' https://al.chirmyram.com/dav/
```

```
<?xml version="1.0" encoding="UTF-8"?><D:multistatus xmlns:D="DAV:"><D:response>
<D:href>/dav/</D:href><D:propstat><D:prop><D:displayname>root</D:displayname>
<D:supportedlock><D:lockentry xmlns:D="DAV:"><D:lockscope><D:exclusive/></D:lockscope>
<D:locktype><D:write/></D:locktype></D:lockentry></D:supp...
```

⚠ **`D:supportedlock` advertising `D:write` is not a write permission.** WebDAV
servers advertise the locks they can issue, not the rights the caller holds. The
seed's own probe recorded `PUT /dav/__probe.bin -u alist:alist -> 403` on this
exact host: the lock is advertised and the write is refused. That is the same lie
as `write: true` in the REST listing, in a different protocol.

## What the three working hosts have in common

All three answer 207 to a `Depth: 0` PROPFIND with a published credential, and all
three are read-only by design.

- **`al.chirmyram.com`** returns `displayname: root` and 581 bytes. It is the
  reference reader: 9 root directories, 7.43 TiB of content by the size fields, and
  the WebDAV path is the same storage as the REST listing.
- **`zhuifan.link`** returns `displayname: new` and 527 bytes, because its
  `base_path` is `/新番/anime/new` and `/dav/` is that subtree. A mount that
  assumes `/dav/` is the instance root sees only the anime index.
- **`alist.qsesvick.top`** returns `displayname: root` and 581 bytes. It is the
  WebDAV endpoint the index publishes for the 20237737 corpus, while
  `alist-cdn.20237737.xyz` is the site name for the same corpus.

⛔ **A `base_path` that is not `/` makes `/dav/` a different tree.** Check
`base_path` from `/api/me` before concluding anything about what a 207 contains.

## The host that fails at the front

`pan.lm379.cn` is the instance the community index recommends first, with
`https://pan.lm379.cn/dav/` and `public_dav` / `public`. On 2026-10-22:

| request | result |
| --- | --- |
| `GET https://pan.lm379.cn/` | 200 in 1.8 s |
| `PROPFIND https://pan.lm379.cn/dav/` with the published credential | **524 in 31.0 s** |

524 is Cloudflare's origin-timeout code. The site is up and the WebDAV route does
not answer within Cloudflare's ceiling.

⚠ **This is a custom front end, and no API probe can see it.**
`/api/public/settings` on this host returns single-page-app HTML rather than JSON,
so the capability protocol in [`alist-openlist.md`](alist-openlist.md) classifies it
`custom-frontend` and stops. The instance is described as fully usable over WebDAV
with about 10 TiB of content and a read-only public account, and that could not be
confirmed: the one route that would confirm it timed out at the edge.

⛔ **`unprobeable` is not `dead`.** A host behind a custom front end may be the best
reader in the population and invisible to every test in this topic. Record it as a
gap with the route that failed, and do not retire it.

## What breaks WebDAV, in the order it happens

Four failures, and the evidence for each.

**1. The instance operator closes it, and the API keeps working.** `alist.zlion.top` is the
measured case: the community index records `之前有 WebDAV，因滥用现已关闭`, "it had
WebDAV before, now closed because of excess use", and the host itself is now 000 on a TLS
handshake failure. The order matters: WebDAV closes first, because it is the route
that turns an instance into somebody's PCDN uplink.

**2. The excess use is downstream bandwidth, not storage.** `lm379.cn`'s own README
states that people take the site to farm PCDN downstream traffic and that the
instance operator has received arrears notices in the middle of the night several
times.
A WebDAV mount is the lowest-cost route to that traffic, so it is the first feature to go.

**3. The credential is rotated and the index is not updated.** The index publishes
a username and password per site and nothing re-checks them. A 401 on a published
credential is the normal end state, and it is indistinguishable from a wrong
password without a second source.

**4. The front times out.** `pan.lm379.cn` returns 524 in 31 seconds while its root
page returns 200 in 1.8. A CDN in front of a bridge adds a ceiling that the bridge
does not know about.

## The egress question, which is why WebDAV is worth the trouble

A Cloudflare-fronted instance serves the bytes from the edge and not from the
instance operator's uplink, and it does so whether the request arrives over REST or
over WebDAV. That is the whole value.

Measured on `al.chirmyram.com` on 2026-10-22, over a 36,747,196-byte PDF resolved
through `/api/fs/get` to a signed CDN URL:

```
GET <signed>        -> 200, Server: cloudflare, cf-cache-status: HIT, age: 21
GET <signed> -r 0-1048575 -> 206, 1,048,576 bytes,
                             Content-Range: bytes 0-1048575/36747196
                             71 to 88 ms across five attempts, 11.4 to 14.1 MiB/s
```

`cf-cache-status: HIT` is the finding: Cloudflare already holds the object and
serves it byte-identically, with `Accept-Ranges` honoured. The reader pays nothing
and the instance operator pays nothing per byte.

⚠ **The signed URL is not a gate and must not be treated as one.** Every request
to `/api/fs/get` for the same path returned the **same** signature across 16
calls, which means a signature is not minted per request here. Whether the
signature is validated at all was not tested by corrupting it, so the gate's
strength is `unverified`. Rule 9 of the methodology says an unvalidated signature
is not a gate; this record says the signature is stable and leaves its validation
untested.

## The measurement that does not scale

Six whole-object reads of the same cached file, minutes apart:

```
11.54  12.54  42.96  43.77  67.43  78.58  79.58   MiB/s
```

A factor of seven between the slowest and the fastest read of one object from one
host. That is not throughput; it is edge-cache behaviour and the reader's own
network. Parallel ranged reads at 8 and 32 connections measured **below** the
single-stream baseline, which is the signature of a shared cache and not of
shaping. [`../self-hosted/cdn-fronting.md`](../self-hosted/cdn-fronting.md) carries
that curve and the reason not to quote it as a provider number.

⛔ **Never quote a single-stream figure from a CDN-fronted host as that host's
throughput.** The number is a property of the edge cache's state at that second.

## What WebDAV is good for, and what it is not

**Good for:** mounting a read-only corpus as a filesystem, `rclone mount`, streaming
a file with range requests, and reaching a custom front end that hides the
REST API.

**Not for:** writing. Every working WebDAV mount found in this population is
read-only, and the two hosts that advertise write over REST refuse it over WebDAV
as well.

**Not for:** capacity. The mount is somebody else's storage, with a 9-month
half-life and no notice.
