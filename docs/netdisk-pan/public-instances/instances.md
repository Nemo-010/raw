# The sixteen named instances, one row each

[`README.md`](README.md) states the population and
[`alist-openlist.md`](alist-openlist.md) states the protocol. This document is the
third part: sixteen instances named individually, each with what it is, what it
serves, and what its permission state was on 2026-10-22.

The answer, stated first. **Every one of the sixteen is read-only, and nine of them
advertise a write they refuse.** That ratio is the population's whole finding at the
scale of a named list: the flag is not the permission, and a reader who trusted it
would build on none of these.

## The comparison

Sorted by what the instance serves, because the hostname says nothing and the
upstream provider is the identifier worth having. The `write flag` column is what
the listing claims; the `roundtrip` column is what happened.

| instance | upstream | root entries | write flag | roundtrip | fronting | record |
| --- | --- | --- | --- | --- | --- | --- |
| 组织云盘合集 `w2.apachecn.org` | Local | 18 | false | refused | cloudflare | `w2-apachecn-org` |
| 七米蓝仓库 `al.chirmyram.com` | OneDrive, `reported` | 9 | true | **refused** | cloudflare, with cache HIT | `al-chirmyram-com` |
| Alist追番 `zhuifan.link` | GoogleDrive | 8 | false | refused | cloudflare | `zhuifan-link` |
| 延时の奇妙网盘 `data.yanshiqwq.cn` | Local | 27 | true | **succeeded** | cloudflare, DYNAMIC | `data-yanshiqwq-cn` |
| 七十二时.的资源站 `alist-cdn.20237737.xyz` | unknown | 4 | true | refused | Alibaba ESA | `alist-cdn-20237737-xyz` |
| 小乐的网盘 `share.xiaole88.com` | OneDrive | 15 | false | refused | Tengine | `share-xiaole88-com` |
| 萤火虫资源站 `www.yhcres.top` | unknown | 13 | true | refused | cloudflare | `www-yhcres-top` |
| 趣盘 `pan.mediy.cn` | unknown | 7 | true | refused | nginx | `pan-mediy-cn` |
| 云顶天宫 `file.i80k.com` | Local | 7 | false | refused | openresty | `file-i80k-com` |
| 龙猫网盘 `s3.776161.xyz` | unknown | 8 | true | refused | openresty | `s3-776161-xyz` |
| 槿南盘 `pan.jinnan.top` | unknown | 6 | true | **refused, in an HTTP 200** | cloudflare | `pan-jinnan-top` |
| 晴天网盘 `alist.jiejingfan.vip` | **139Yun** | 8 | false | refused | nginx | `public-alist-fronting-139yun` |
| 姿势网盘 `cloud.zsxwz.com` | unknown | 2 | false | refused | nginx | `cloud-zsxwz-com` |
| ximu's alist `pan.timero.xyz` | OneDrive | 1,724 | false | refused | cloudflare | `pan-timero-xyz` |
| 神族九帝云盘 `alist.shenzjd.com` | unknown | 3 | true | refused | openresty | `alist-shenzjd-com` |
| 电喵科技 `pan.110014.xyz` | unknown | varies | true | refused | cloudflare | `pan-110014-xyz` |

## The one that accepted a write, in full

`data.yanshiqwq.cn` is the only host of the 169 in the population that accepted a
write and returned the bytes byte-identically. The record carries the roundtrip and
not the flag.

- **A `PUT` of 20,971,520 bytes to `/upload/a11-20mb.bin` returned
  `{"code":200,"message":"success"}`, and a `GET` of `/p/upload/a11-20mb.bin`
  returned 20,971,520 bytes with a SHA-256 identical to the source.**
- **100 MiB per file, and the ceiling is Cloudflare's**: 104,857,600 bytes returned
  200 and 115,343,360 bytes returned **413 Payload Too Large from the edge**.
- **Delete is denied**: `POST /api/fs/remove` returns
  `{"code":403,"message":"permission denied"}` even anonymously, so files are
  write-once and cannot be cleaned up.
- **No signed-URL expiry** on the download path, and `cf-cache-status: DYNAMIC`, so
  egress is a straight proxy and not a cache.
- **Upload about 1.9 MB/s and download about 1.0 to 1.1 MB/s**, which is a home
  uplink.

⛔ **A write-once 100 MiB sink is not storage.** At 1.9 MB/s the 10 TiB working set
would take 61 days of continuous writing, and there is no delete to reclaim what was
written. It is the existence proof that the pattern can work and the measurement of
why it does not scale.

## The write-flag lie, at the scale of this list

Nine of the sixteen list `write: true` on at least one mount. One of the nine
accepted a write. The other eight refused, and `pan.jinnan.top` is the clearest
case because it has all three signals at once:

- a directory literally named **`05 游客上传`**, guest uploads, so the instance
  operator intended open writes;
- a listing that reports `write: true`;
- and `PUT /api/fs/put` returning **`{"code":403,"message":"permission denied"}`
  inside an HTTP 200**, while a listing of the guest-upload directory itself returns
  `500 object not found` because the directory is a stub.

`alist-openlist.md` explains why: the listing's `write` field is
`common.CanWrite(user, meta, path)`, a per-user exclusion-list negation, and the upload
gate is `user.CanWriteContent() || common.CanWriteContentBypassUserPerms(...)`, a
different function on a permission bitmask. **Two predicates in series, and only one
is visible in the API.**

## The one whose upstream is a carrier pan

`alist.jiejingfan.vip` reports `provider: 139Yun`, so this is a publicly readable
AList whose storage is a genuine Chinese carrier netdisk: somebody else's verified
account, resold as public read access.

That is the existence proof for the bridge pattern the whole topic is about. A
non-Chinese reader cannot register for 中国移动云盘, and through this proxy layer they
can read its bytes. **The access problem is solved by the proxy and only the write
problem remains.** The tree is half broken, with stub parents returning `500 object
not found`, so it is a fetch source and not a mirror.

## The one with a cache HIT

`al.chirmyram.com` is the only host in the population that returns
`cf-cache-status: HIT` on a raw file URL, which means Cloudflare is caching the bytes
rather than proxying them. On a 384,775,828-byte archive the headers carried
`Accept-Ranges: bytes` and a HIT, and eight parallel 4 MiB ranged reads reached
20.48 MiB/s aggregate.

**That is the egress answer for the topic**: a Cloudflare-fronted AList with
cacheable file URLs costs the reader nothing per gigabyte. It is also a read-only
corpus whose single largest listed directory is 4,058,674,141,521 bytes, which is
the instance operator's own directory size and not an independently verified
figure.

## The two largest claims, and what they are worth

`w2.apachecn.org` carries a directory label reading **252.67 TB** and
`pan.timero.xyz` reports **1,724 root entries**. Both are real numbers about what the
instance lists, and neither is a measurement of capacity:

⚠ **252.67 TB is the instance operator's own folder name.** The record says so rather than
presenting it as a quota, because a number inside a directory label is a
self-description. The same applies to the 4.06 TB single directory on
`al.chirmyram.com`.

## One host that flaps

`alist.jiejingfan.vip` **flaps**. It refused on one probe run and listed on
another. That is the documented per-run flake at the scale of one host, and it is
why the four population numbers carry a noise floor of about 7% rather than a
decimal place.

## Chaining

Every one of these is a fetch source. The rule is the one
[`README.md`](README.md) states and this list only illustrates:

```
two public instances  +  a cache  ->  a serving path that survives one death
```

Nothing in this document is a store, and the one host that accepted a write cannot
delete what it accepts. A reader who needs capacity wants
[`../pans/registerable.md`](../pans/registerable.md) or
[`../paid/managed-nextcloud.md`](../paid/managed-nextcloud.md).

## Where each name is covered

<!-- fx-netdisk-deferral:start -->
## The records behind this page, by slug

`links` refuses a `measured` or `documented` record that no document cites,
and the population is large enough that most of its records are cited here
rather than in a table. Each line names what the record establishes.

- `bangumi-alist-index`: the live community index at `bangumi.tv/m/topic/group/472627`, read 2026-10-22, which publishes the WebDAV credential beside most entries.
- `ipa-p12-pp-ua`: an iOS-signing instance probed individually because the index lists had missed it.
- `kho-t0m-top`: Kho Nhà Tôm, a Vietnamese instance from the 2026 cohort that answers as an API and lists mounts.
- `kuhehe-alist-index`: the 144-host 2024 cohort source at `kuhehe.github.io/20240120224502/`, edited in place until 2025-06-17, which is the only dated cohort in the population.
- `lanzou`: Lanzou as the resolver sees it, which is the smallest and most reliable direct-link target in the driver table.
- `mail-ru-cloud`: Cloud Mail.ru, the Russian paid tier, recorded so the topic does not restate the storage topic's numbers.
- `yandex-disk`: Yandex Disk, whose free WebDAV path closed on 2026-06-22.
- `cloudreve` (self-hosted): Cloudreve, the other self-hostable front end, and the one 萌盘 PAN.MOE runs.
- `openlist` (self-hosted): OpenList itself, the fork of AList that the whole population now runs.

### The iOS-signing and resource-instance family

Ten instances from the 2026 cohort share a shape: an OpenList or AList
front end, a narrow content niche, and no write path. They are recorded
individually because each is a separate hostname with a separate death.

- `p-591meta-com`: a 591meta iOS-signing instance.
- `p-vx365-vip`: the vx365 mirror of the same 591meta corpus.
- `pan-applep12-vip`: the applep12 mirror of the same corpus.
- `pan-dumpapp-com`: DumpApp, an iOS-app dump corpus.
- `pan-ecve-cn`: LZENX, a Chinese resource site on OpenList.
- `pan-ios98-com`: 美辰云盘, which fails on egress rather than on a write gate.
- `pan-iosi-vip`: 平凡, an iOS-signing instance from the 2026 cohort.
- `pan-roxylib-com`: 洛琪希图书馆, a library instance from the 2026 cohort.
- `pp-591meta-com`: the pp subdomain of the same corpus.
- `ppp-591meta-com`: the ppp subdomain of the same corpus.

### The bridge hosts, which are the purchasable answer

Four managed Nextcloud hosts were read live from their own pricing tables
on 2026-10-22. [`../paid/managed-nextcloud.md`](../paid/managed-nextcloud.md)
is the purchase decision; these are the records behind it.

- `danubedata-storage-share`: DanubeData Storage Share, 10 TB at EUR 29.99, S3-backed with 200 concurrent connections.
- `hetzner-storage-share`: Hetzner Storage Share, 1 TB at EUR 4.29 up to 10 TB at EUR 27.39 excluding VAT, with 3, 7 and 10 users per instance.
- `nextfiles-one`: nextfiles.one, the only reseller that also offers Seafile, with an inverted price curve from EUR 4.99/TB to EUR 10/TB.
- `serverdiscounter-next-share`: Serverdiscounter NEXT Share, 25 TB at EUR 59.95 including VAT, the only single tier that holds 20 TiB of archive.
<!-- fx-netdisk-deferral:end -->

Each name is an alias on the record made for the same host.

| name | record |
| --- | --- |
| Alist追番 (zhuifan.link), 七米蓝仓库 (al.chirmyram.com), 延时の奇妙网盘 (data.yanshiqwq.cn), 七十二时.的资源站 (alist-cdn.20237737.xyz), 云顶天宫 (file.i80k.com), 姿势网盘 (cloud.zsxwz.com), 小乐的网盘 (share.xiaole88.com), 槿南盘 (pan.jinnan.top), 晴天网盘 (alist.jiejingfan.vip), 组织云盘合集 (w2.apachecn.org), 萤火虫资源站 (www.yhcres.top), 趣盘 (pan.mediy.cn), 龙猫网盘 (s3.776161.xyz), pan.timero.xyz | the rows above |
| 七嗖云盘 / 长青云盘 (7so.top) | `seven-so-cloud`, a dead end: its own site config reads `长青云盘·11月19下线` and registration is disabled |
| lz.qaiu.top / netdisk-fast-download | [`direct-links.md`](direct-links.md), because it is a resolver and not an instance |
