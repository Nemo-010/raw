# netdisk-pan: which drive can I mount, and which of these public instances is real

A consumer pan drive is a storage service sold to people, and this topic asks
two questions about the population. Can a registrant without a PRC identity
obtain 500 GiB or more, and what breaks first? And of the hundreds of volunteer
instances that re-export somebody's drive over HTTP, which are real?

169 hostnames were probed. 33 answered as an AList or OpenList API. 30 exposed an
anonymous mount list. **One accepted a write and returned the bytes.** That ratio
is the finding, and it is structural rather than unlucky: the advertised write
flag is independent of the permission that gates a write, so 14 of the 30 hosts
advertise a write they will refuse.

⛔ **A public instance is a fetch path. It is not storage, at any price.** The
one writable host of 169 is a volunteer's home disk behind Cloudflare, with no
quota, no delete, and a 9-month half-life. A reader who takes one sentence from
this topic should take that one.

## The four numbers

Measured 2026-10-22 by one probe script over one host list, two runs per host.
The population is the union of a 144-host 2024 index, a 101-host 2026 sweep and
four individually probed hosts, deduplicated by hostname.

| measure | count | share of 169 |
| --- | --- | --- |
| answered as an AList or OpenList API | 33 | 19.5% |
| exposed an anonymous mount list with at least one entry | 30 | 17.8% |
| advertised `write: true` on at least one mount | 14 | 8.3% |
| accepted a write and returned the bytes byte-identically | 1 | 0.6% |

The last row is the only one that means "storage". The third row is the one that
misleads, because it is the number a reader would take from the API.

⚠ **The population is 169 hostnames, and the census has been recounted.** An
earlier recon pass reported 170 hosts, 32 API hosts and 29 with a mount list. The
union of the three probe files is 169, because one of the four hosts probed
individually was already inside the 166-host union. The API and listing counts are
33 and 30 when a host counts as answering if any run saw it answer, and 32 and 27
when only the last run counts; `alist.tianmoy.cn` flaps and is the single host
behind the difference. The writable count is 1 under every rule.
[`public-instances/README.md`](public-instances/README.md) states both rules with
the host lists.

⚠ **All four carry a noise floor of about 7%.** Two runs of the same probe
minutes apart disagreed on 3 of 42 hosts on the read axis. Any single-run
measurement of this population is a snapshot with real flake in it, which is why
the write verdict is a SHA-256 roundtrip and not a status code.

## The binding constraint

Across the population, `write-gated` binds. Not a quota, not a rate: the write
never reaches the disk. The mechanism is two predicates evaluated in series, and
only one of them is visible in the API.

`POST /api/fs/list` returns a `write` field. That field is
`common.CanWrite(user, meta, path)`, which is a **per-user exclusion-list
negation** and returns true for a user who is on no exclusion list
(`server/handles/fsread.go`, read 2026-10-22). The upload gate is a different
function: `user.CanWriteContent() || common.CanWriteContentBypassUserPerms(...)`,
where `CanWriteContent` is bit 3 of the permission bitmask and the second term is
a per-path metadata override (`server/middlewares/fsup.go`, read 2026-10-22).
So `write: true` and a refused `PUT` are consistent, and they co-occur on 13 of
14 hosts that advertise the flag.

The response that carries the actual permission state is
`write_content_bypass`, added in OpenList v4.x. It was present on 13 of 30
listable hosts, true on exactly one, and that one is the writable host.

## The four access modes

The `free`/`paid` split does not fit this topic: a public instance's price is not
what decides whether a reader can use it. The split that fits is by who holds the
credential, because that is what sets the lifetime.

| mode | who holds the credential | identity | good for | lifetime |
| --- | --- | --- | --- | --- |
| public instance | a volunteer, on the reader's behalf | `anonymous` | read and egress at CDN speed | about 9 months |
| registration-gated pan | the reader, after a signup wall | `email` to `country-phone(86)` | capacity, where the wall is passable | provider policy |
| paid pan | the reader, paying | `card` | capacity with a contract behind it | the contract term |
| self-hosted bridge, the last resort | the reader, on a rented VPS | `email` for the bridge, whatever the upstream needs | control of the bridge, after every hosted mode | as long as the VPS runs |

## The documents

| document | the question it answers |
| --- | --- |
| [`public-instances/README.md`](public-instances/README.md) | how big is the population, and why is one in thirty writable |
| [`public-instances/alist-openlist.md`](public-instances/alist-openlist.md) | **how do I tell a real instance from a fake one**: the API surface, the write-flag lie, the bitmask, the zero-byte oracle, the protocol |
| [`public-instances/index-lists.md`](public-instances/index-lists.md) | where instances are announced, and how each index rots |
| [`public-instances/webdav-fronting.md`](public-instances/webdav-fronting.md) | the published guest credentials, PROPFIND, and what breaks |
| [`public-instances/direct-links.md`](public-instances/direct-links.md) | share-link resolvers, and which pans they cannot reach |
| [`public-instances/instances.md`](public-instances/instances.md) | **the sixteen instances in the census, one row each**: what each serves, and which of them lie about writing |
| [`pans/README.md`](pans/README.md) | the provider survey, ordered by identity cost |
| [`pans/registerable.md`](pans/registerable.md) | **which signup form a registrant without a PRC identity can complete**: thirty pans ordered by identity cost, and the two worth having |
| [`pans/china.md`](pans/china.md) | the +86 wall, and the one gate that opens |
| [`pans/korea-japan.md`](pans/korea-japan.md) | the international tier, and what it costs in identity |
| [`pans/russia-cis.md`](pans/russia-cis.md) | the any-phone set, and how it closed |
| [`pans/western.md`](pans/western.md) | the 5 to 20 GB tier, and why it fails the floor |
| [`pans/reverse-engineered-clients.md`](pans/reverse-engineered-clients.md) | the fifteen platforms whose only API is somebody's app, and which of them can be written to |
| [`paid/README.md`](paid/README.md) | the cheapest paid capacity, and what the resale market signals |
| [`paid/managed-nextcloud.md`](paid/managed-nextcloud.md) | **the one thing in this topic a reader can buy outright**: five managed Nextcloud hosts, priced, with the 25 TB tier that holds the whole archive |
| [`dead-ends.md`](dead-ends.md) | every host that is gone, with the shape of its death |
| [`auto-discovery.md`](auto-discovery.md) | the discovery loop, as an implementable specification |
| [`self-hosted/README.md`](self-hosted/README.md) | the last resort, after every hosted mode: the bridge pattern, pooled tenant, then bridge, then CDN |
| [`self-hosted/alist-openlist-ops.md`](self-hosted/alist-openlist-ops.md) | running the bridge, and which drivers need no account |
| [`self-hosted/cloudreve.md`](self-hosted/cloudreve.md) | the other bridge, and when it is the better one |
| [`self-hosted/cdn-fronting.md`](self-hosted/cdn-fronting.md) | what the front does to the egress bill |

## The one thing to do with a public instance

Serve from it, with a cache and a fallback. A Cloudflare-fronted instance
returned `cf-cache-status: HIT` on a 36,747,196-byte PDF, honoured a byte range
with 206, and produced a 1 MiB ranged read in 71 to 88 ms across five attempts
(`measured`). That is Cloudflare caching somebody else's pan bytes at the edge
and handing them to the reader for nothing.

Two mirrors plus a cache turn a 9-month half-life into a non-event, because a
mirror that dies is replaced before the cache goes cold. 20 TiB of archive cannot
ride this, and nothing in this topic suggests it can.

## What did not work

The dead ends are records, not prose rows: `verdict: dead` in
[`dossier/netdisk-pan/`](../../dossier/netdisk-pan/), one per host, with the
evidence of its death. [`dead-ends.md`](dead-ends.md) groups them by the shape of
the failure, because the shape is what the next probe should test for.

The four shapes, and one host each:

- **repurposed domain**: `alist.xiaoya.pro` returns 302 to a consumer portal.
- **no TCP service**: `alist.zlion.top` returns 000 on a TLS handshake failure.
- **challenge page**: `pan.t-satoru.top` returns 403 behind an automated-traffic
  filter interstitial, and `alist.advanced360.top` returns 200 with a JavaScript
  cookie gate that is neither JSON nor a page.
- **answering but empty**: `alist.ucu520.top` serves a complete OpenList web UI
  and returns `code: 500, storage not found` inside an HTTP 200.

## What this topic does not do

It does not judge whether using any of this is permitted. One line per record
names the technical reliability fact instead.

It does not claim a half-life better than the data supports. The number is
9.0 months with a margin that the sample cannot narrow, and
[`public-instances/README.md`](public-instances/README.md) shows the arithmetic
so a reader can check it.

It does not know how many instances exist. 169 is what two index lists and one
host sweep produced, and the discovery design in
[`auto-discovery.md`](auto-discovery.md) is what would make that number real.

## Records that no other document names

This list is generated by `scripts/report/render.py` from the records. It holds each `measured` or
`documented` record of this topic that no other document of `docs/` names, so a reader finds it and
the gate's `links` check counts it as cited. A research run adds a row here only through the render
that `scripts/rq land` runs. A document that names the record removes its row at the next render.

<!-- generated:start topic=netdisk-pan kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `crt-sh-alist-openlist-ct-channel` | crt.sh certificate transparency searc... | qualifies-with-caveat | measured |
<!-- generated:end -->
