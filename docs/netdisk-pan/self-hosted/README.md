# Self-hosted bridge: the last resort

Self-hosting is the last resort, after every hosted mode of this topic (`AGENTS.md`
section 2 rule 9).

Every public instance in this topic is one person running the same arrangement,
and the arrangement is reproducible. This document is the arrangement: a pooled
tenant, a bridge in front of it, and a CDN in front of the bridge. A bridge a
reader runs on a rented VPS lives as long as that VPS, where a public instance has
a 9-month half-life.

The finding it rests on is not the instance count. It is that the instances which
work are not bridging Chinese pans at all: `al.chirmyram.com` resolves a 29 GiB
`.iso` to a SharePoint tenant, and `pan.timero.xyz` lists 1,724 entries with
provider `Onedrive`. The bridge and the CDN are the reusable part, and the tenant
underneath is replaceable.

## The shape

```
   pooled tenant                      reader-owned              reader-owned
   M365 / SharePoint  ---.
   Google Workspace   ---+-->  OpenList or Cloudreve  -->  Cloudflare  -->  reader
   a pan account      ---'     (REST, WebDAV, S3)          (edge cache)
```

Three layers, three different failure modes, and each one is separately
replaceable. That separability is the whole point: a dead tenant costs a
re-registration, a dead bridge costs a restart, and a dead CDN is a DNS change.

## The comparison

Sorted by how much of the arrangement the reader controls, which is the thing that
decides the lifetime.

| mode | who holds the upstream | identity | lifetime | owns the failure |
| --- | --- | --- | --- | --- |
| public instance | a volunteer | `anonymous` | about 9 months | nobody reachable |
| the reader's bridge on a rented tenant | the reader | `email` plus whatever the tenant needs | the tenant's term | the reader, partially |
| the reader's bridge on a rented disk | the reader | `email` for the VPS | the VPS's life | the reader, fully |

## Why the tenant is the weak layer and the bridge is not

The upstream decides everything that matters and it is the layer the reader
controls least. Three measured cases:

**A pooled tenant dies when the tenant does.** `pan.timero.xyz` serves 1,724
entries with `provider: Onedrive`, and `share.xiaole88.com` serves 15 with the same
provider. Both are one instance operator re-exporting one paid account. The
mechanism is recorded for `alist.xiaoya.pro`: shared tokens were revoked and the
instance went to 504, and the host now 302s to a consumer portal.

**A tenant can be arbitraged, and then revoked.** `115` and Google team-drive
rentals sell at CNY 15 to 20 per month for unlimited space with a 400,000-file cap
and a 750 GB per day upload cap, and one seller's own thread carries a buyer
reporting that the drive vanished. Where a rental market exists, the underlying
"unlimited" is a quota being arbitraged and the arbitrageur's account is what fails.
The record is `dossier/netdisk-pan/115-team-drive-rental.json`.

**A self-hosted tenant does not die that way.** An M365 A1 or a Google Workspace
account the reader holds has a published term, and its 25 TB per site for SharePoint
is the reason the instances that work can offer 59 to 80 GiB single files. The
storage topic carries the tenant quota; this document owns only the bridge.

⚠ **The bridge cannot fix a bad upstream, and a bad upstream is the normal case.**
Choosing the bridge first and the tenant second is how a reader ends up with a
working bridge over an account that gets frozen in a month.

## What the bridge must do

A bridge that satisfies all six of these is enough, and OpenList and Cloudreve both
do with different trade-offs.

- **Serve REST and WebDAV**, so both a script and a filesystem mount can read.
- **Redirect, not relay**, where the upstream supports it. A bridge that proxies
  every byte through the VPS turns the VPS's bandwidth into the ceiling, which is
  the constraint that killed the bandwidth-arbitrage instances.
- **Expose a per-path write grant**, so a guest can write to one directory and not
  to the instance. This is the mechanism behind the one writable public instance,
  and it is a feature rather than a bug: `server/middlewares/fsup.go` evaluates
  `CanWriteContent() || CanWriteContentBypassUserPerms(meta, path)`.
- **Sign its raw path if it is going to sign it properly.** `pan.ios98.com` accepts
  a write and then returns `code: 401, expire missing` on the read-back, which is
  the worst of both: the bytes are stored and unreadable.
- **Say what the upstream is.** The `provider` field is the only visible clue to
  whose account dies first, and a bridge that returns `unknown` for every mount
  hides the one fact a reader needs.
- **Be replaceable.** One config file, one binary, one database file.

## The chain, with the documents that own each hop

| hop | what it decides | owner |
| --- | --- | --- |
| the tenant | capacity, and when it is revoked | [`../pans/`](../pans/README.md) and the storage topic |
| the bridge | what protocol the client speaks | [`alist-openlist-ops.md`](alist-openlist-ops.md), [`cloudreve.md`](cloudreve.md) |
| the CDN | the egress bill and the cache hit rate | [`cdn-fronting.md`](cdn-fronting.md) |
| the reader | nothing; it is a `GET` | - |

## What this arrangement is not

It is not free. It costs a VPS, and the tenant costs whatever the tenant costs. The
topic's claim is narrower than "free": the bridge and the CDN are free and the
tenant is the part the reader already has or already pays for.

⛔ **It is not a way to make a public instance durable.** Adding a cache in front of
somebody else's instance does not extend its life. It makes the death cheap, which
is a different and sufficient thing.

## Chaining

The arrangement is the chain, so this section is the summary of the other three
documents rather than a separate composition.

```
tenant  ->  OpenList  ->  Cloudflare  ->  cache  ->  reader
            (WebDAV)      (edge)
```

A second bridge over a second tenant, both behind the same CDN, is the arrangement
that turns a 9-month half-life into a non-event: a mirror that dies is replaced
before the cache goes cold. The measurement behind that claim, and the reason not
to quote a throughput curve from it, is in [`cdn-fronting.md`](cdn-fronting.md).
