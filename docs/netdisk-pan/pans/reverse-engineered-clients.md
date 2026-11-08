# Reverse-engineered clients: the fifteen platforms whose only API is somebody's app

A camera vendor, a phone vendor, a console maker and a Chinese TV client all sell
storage. None of them publishes an API. All of them publish enough of a client that
the protocol can be recovered, and the recovered protocol is the only way in.

This document covers fifteen providers whose only API is a recovered client
protocol, and the finding is uniform enough to state once: **the reverse-engineered
API is a read path or a write path, rarely both, and which one it is decides whether
the provider is storage.**

## The comparison

Sorted by whether a write path exists, because that is the column that separates a
store from a source.

| provider | free tier | the recovered API | upload | download | verdict |
| --- | --- | --- | --- | --- | --- |
| 光鸭云盘 GuangYaPan | 2 TB, 100 GB per file | OpenList `guangyapan` driver, merged | yes, SMS auth | yes, 302 links | qualifies-with-caveat |
| Lark / 飞书 Drive | 100 GB per tenant | Lark Drive open platform v1, wrapped by FeiSync | yes, app credentials | yes | qualifies-with-caveat |
| 天翼云盘 Tianyi (189) | 60 GB, promos to 12 TB | OpenList `189`, `189_tv`, `189pc` | yes, 2 GB a day free | yes | fails-identity |
| 小米云服务 Xiaomi Cloud | 5 GB | wangbjun/go-micloud, OpenList PR 1391 unmerged | partial | yes | fails-quota |
| 华为云空间 HUAWEI Mobile Cloud | 5 GB | RzdPai/Huawei_Cloud_Webdav | via WebDAV | via WebDAV | fails-quota |
| 中国移动云盘 China Mobile | 1 TB | OpenList `139` (139Yun) | via mount | yes | fails-identity |
| Quark TV / UC TV | 300 GB | OpenList `quark_uc_tv`, public sign key | **no**, read-only by design | yes, streamed | fails-quota |
| GoPro Cloud / Quik | unlimited GoPro content | himewel/gopro-api, dustin/gopro | **none documented** | yes | qualifies-with-caveat |
| Amazon Photos | unlimited photos on Prime | trevorhobenshield/amazon_photos | yes, cookie auth | yes | qualifies-with-caveat |
| ASUS WebStorage | 5 GB | rclone PR 6808, draft since 2023-03 | no | no | fails-quota |
| NIKON IMAGE SPACE | 2 GB, 20 GB with a product | none; SnapBridge only | via SnapBridge, downscaled | no | fails-quota |
| Nintendo Switch Online | one save per title | none, console only | console only | console only | fails-quota |
| PlayStation Plus | 200 GB | none, console only | console only | console only | fails-egress |
| Samsung Cloud | none, discontinued | none | not applicable | not applicable | dead |
| LG U+ Box | none, discontinued | none | not applicable | not applicable | dead |

## The three that a reader can actually use, and how

**GuangYaPan** is the largest free allocation in the survey after Ctfile: 2 TB at
registration and 100 GB per single file, which is the best per-file cap on any free
consumer pan found. The OpenList driver is merged rather than a fork, so it is
maintained by people who are not the vendor. Two numbers the marketing merges and a
reader must not: capacity is 2 TB free, and traffic is **2 GB a day at high speed**
on the free tier. As a cold archive the traffic never binds because uploads happen
once. As a serving layer it ends at 2 GB a day. Registration is SMS-only, and every
email-shaped auth path returns 404, so a registrant with only an email address
cannot reach it.

**Lark Drive** is the cleanest of the fifteen because the vendor publishes the API.
The quota is 100 GB per tenant and tenancy is free and self-service, so capacity is
100 GB times the number of tenants. The constraint is 250 MB per file, which turns
20 TiB of archive into 84,000 objects. The FeiSync wrapper does the multi-tenant
routing, and the one trap is stated in its own forum thread: two apps inside one
tenant share that tenant's 100 GB, so a second app is not a second quota.

**Amazon Photos** is unlimited for photographs on a paid Prime membership and capped
at 5 GB of video. It is the classic unlimited-photo shape: if arbitrary image bytes
are accepted, and they are because it is a photo service, then a photo-shaped payload
is free across accounts. What stops it being a pipeline is that there is no OAuth and
no API key, only a browser cookie, and every wrapper's README says the cookie expires
and must be refreshed by hand.

## The one experiment worth running

**GoPro Cloud is unlimited storage at USD 59.99 a year, if the provenance rule is not
enforced.** The terms draw the line at "content You capture with a GoPro camera
(excluding Fusion)", which is a rule about the device and not about the file. If
ingest does not check capture provenance, the capacity is unlimited for anything. If
it does, the offer collapses to 100 GB on Premium or 500 GB on Premium+, which is
about USD 120/TB/year and therefore bad.

⛔ **Nobody has published an upload through the recovered API.** Every wrapper
searches, downloads and syncs; the Quik app clearly uploads; no public implementation
does. So the write path is undocumented rather than absent, and the record says
`qualifies-with-caveat` with that sentence in it. The test that settles it is one
account and one large non-GoPro upload. That is a task, not a research question, and
it is the single highest-value unrun test in this topic.

## The read-only case, which is the cleanest example in the corpus

**Quark TV and UC TV are documented as read-only by design.** The OpenList driver
sets `NoUpload` and `NoOverwriteUpload` on both, and the client is a streaming client
so that is correct behaviour rather than a restriction.

This is the exact inverse of the public-instance problem. There, an AList advertises
a write it refuses, and
[`../public-instances/alist-openlist.md`](../public-instances/alist-openlist.md) shows
why the flag and the permission are different functions. Here, a client is published
as download-only and says so in its source. Both cases teach the same rule: **read
the write capability from the driver's own flags, never from the product page.**

## The console clouds, and why they are a category error

Sony and Nintendo both sell storage and neither sells a store. PlayStation Plus gives
100 GB for PS5 saves and 100 GB for PS4 saves with a 1,000-file cap on PS4 data, and
every step of the upload path is console UI. Nintendo advertises "no limit to the
amount of storage space" and binds it to "only one save data file per software title
for each Nintendo Account".

⚠ **Both sentences are true and both are worthless to a reader with no console.** A
write quota with no programmatic read is not storage, and 200 GB of opaque save blobs retrievable
only by a console is not a read path. They are recorded so that nobody re-tests them,
which is the only job a dead end has.

## The two that are gone

Samsung Cloud and LG U+ Box both closed and both are recorded with the evidence of
closure rather than as gaps. Samsung's Gallery Sync and Drive migrated to OneDrive by
2021-09-30 and the quota Samsung matched lasted one year. LG's U+Box terminated on
2021-12-01 after eleven years, and LG Electronics left the phone business on
2021-04-05. **All three Korean carriers exited consumer cloud**, which is why
[`../pans/korea-japan.md`](../pans/korea-japan.md) has only Naver MYBOX left.

## Chaining

A reverse-engineered client is a bridge input, and the bridges are in
[`../self-hosted/alist-openlist-ops.md`](../self-hosted/alist-openlist-ops.md):

```
reverse-engineered client API  ->  OpenList driver  ->  WebDAV  ->  Cloudflare
```

The two constraints that decide whether the chain is worth building are the per-file
cap and the daily traffic allowance, in that order. GuangYaPan fails the second and
Lark fails the first, and both are otherwise the right shape.

## Where each name is covered

The table above is the index. Each name is covered in the section named.

| name | section |
| --- | --- |
| 光鸭云盘 / GuangYaPan | The three that a reader can actually use |
| Lark / 飞书 Drive via multi-tenant app credentials | The three that a reader can actually use |
| Amazon Photos (Prime) | The three that a reader can actually use |
| GoPro Cloud / Quik (GoPro subscription) | The one experiment worth running |
| Quark TV / UC TV | The read-only case |
| 天翼云盘 / Tianyi Cloud Drive (189), incl. the TV-edition OAuth client | The comparison |
| 小米云服务 / Xiaomi Cloud (Mi Cloud Drive) | The comparison |
| 华为云空间 / HUAWEI Mobile Cloud | The comparison |
| 中国移动云盘 (China Mobile / 和彩云) | The comparison |
| ASUS WebStorage | The comparison |
| NIKON IMAGE SPACE / Nikon Imaging Cloud | The comparison |
| Nintendo Switch Online Save Data Cloud | The console clouds |
| PlayStation Plus cloud storage (Sony) | The console clouds |
| Samsung Cloud | The two that are gone |
| LG U+ Box / LG Cloud | The two that are gone |
