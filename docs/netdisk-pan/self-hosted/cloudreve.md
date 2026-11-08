# Cloudreve: the other bridge, and when it is the better one

Cloudreve is the second self-hosted bridge in this population and the one with a
different architecture. It is a cloud drive that owns the file tree and hands
uploads and downloads to the client, where OpenList is a manager that passes
requests to a mounted drive. That difference decides which one to run.

This document covers what Cloudreve does, where it beats OpenList, and the two
measurements that make it nearly invisible to the capability protocol in this
topic.

## The comparison

Sorted by which upstream the bridge is better at.

| upstream | better bridge | why |
| --- | --- | --- |
| an object store (S3, OSS, COS) | **Cloudreve** | it uploads client-side against a storage policy, so the VPS never relays a byte |
| a consumer pan (OneDrive, Google Drive, 139Yun, a Chinese pan) | **OpenList** | it has the drivers, including the share-link ones that need no account |
| a local disk | either | both serve it and both add a database |
| many upstreams at once | **OpenList** | Cloudreve's own documentation says it is not a manager for other cloud drives |

⛔ **Cloudreve's own documentation answers the question.** The English docs
(read 2026-10-22) state that Cloudreve is "a cloud drive rather than a manager for
other cloud drives", that most of its supported storage providers are
storage-specific products from public clouds rather than consumer drives, and that
"the following scenarios are not suitable for Cloudreve: I want to redistribute
other cloud storage services to my users". Redistributing a consumer pan is exactly
what this topic wants, so Cloudreve is the wrong bridge for that job and it says so
first.

## What it is

A Go binary with a Vue front end, GPL-3.0, 28,868 stars, last push 2026-10-20. A
Community Edition and a paid Pro licence. It builds a virtual file system over a
database, isolates user files from the physical storage, and can organise several
instances into a primary-replica arrangement.

Its distinguishing feature is **client-side transfer against a storage policy**.
The browser uploads directly to the object store with a policy-issued credential,
so the VPS's bandwidth is not the ceiling. That is the property that matters for
the serving workload, because a bridge that relays every byte is a bridge whose
uplink is the constraint.

## The two measurements that make it hard to find

A Cloudreve v4 instance is nearly invisible to the capability protocol, and both
reasons are worth recording because a discovery loop that does not know them will
classify every Cloudreve as dead.

**It has no anonymous mount list.** `POST /api/fs/list` does not exist in the v4
API surface the way it does in AList. The probe's `root_list_ok` is therefore `no`
for every Cloudreve, and `alive-no-list` is its ceiling.

**Its ping identifies it and proves nothing else.** The public demo answers:

```
GET https://demo.cloudreve.org/api/v4/site/ping
200  {"code":0,"data":"4.19.1-pro"}
```

That is a live Pro build with **no filesystem**. Version 4.19.1 answers, the
`-pro` suffix says which edition, and there is nothing behind it. A scan that
stopped at the ping would record a live instance.

⛔ **`code: 0` is Cloudreve's success and AList's failure.** AList returns
`code: 200` for success and `code: 500` inside HTTP 200 for a broken storage.
Cloudreve returns `code: 0`. A probe that tests `code == 200` calls every Cloudreve
broken, and a probe that tests `code == 0` calls every AList broken. Test the shape
of the body, not the code.

## Which version answers which route

| version | liveness route | anonymous listing | WebDAV |
| --- | --- | --- | --- |
| v3 | `/api/v3/site/config` | `/api/v3/directory` with a public share | yes |
| v4 | `/api/v4/site/ping` | no anonymous mount list | yes |

⚠ **One host of 169 classified as Cloudreve**, and that is `demo.cloudreve.org`.
The population of public Cloudreve instances is not measurable by this protocol, so
the topic's 33-API figure is a figure about AList and OpenList and not about
bridges in general.

## What it is good for

A bridge over an object store, with client-side transfer, WebDAV access, share
links with expiry and download limits, multi-user registration, and a paid tier for
paid sharing. For a reader who already has an S3-compatible bucket, Cloudreve in
front of it is a working drive with a WebDAV endpoint and no egress relayed through
the VPS.

## What it is not good for

Redistributing a consumer pan. That is OpenList's job, and
[`alist-openlist-ops.md`](alist-openlist-ops.md) is the document for it.

It is also not a way to obtain capacity. Both bridges give protocols; neither gives
storage. The upstream is the capacity and the upstream is the thing that gets
frozen.

## Chaining

```
object store  ->  Cloudreve (client-side transfer, WebDAV)  ->  CDN  ->  reader
```

The chain is the same shape as the OpenList one and the layer in front is the same;
see [`cdn-fronting.md`](cdn-fronting.md). The difference is that the middle hop does
not touch the bytes.
