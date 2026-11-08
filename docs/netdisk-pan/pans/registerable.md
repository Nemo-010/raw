# Registerable pans: which signup form a registrant without a PRC identity can complete

Thirty providers are compared here, and the question for every one of them is the
same: **can a registrant without a PRC identity, with an email address and no
institutional affiliation, complete the signup?**

The answer, stated first. **Ctfile is the only large Chinese pan whose signup form
offers email and password as the primary path**, and it gives 5 TB with 20 GB per
file. Every other large Chinese quota is behind a +86 number, a real-name check, or
a one-time real-name payment. Six hosts outside mainland China take an email address
and give between 1 TB and 10 TB, and two of those are worth having.

## The comparison

Sorted by identity cost, which is the axis that decides reachability. Every row was
built from the dossier record named in the last column.

| pan | free tier | per-file cap | identity | binds on | verdict | record |
| --- | --- | --- | --- | --- | --- | --- |
| Ploud Storage | 1 TB | 100 MiB chunk | `any-phone` | signup form | qualifies-with-caveat | `ploud-storage` |
| 萌盘 PAN.MOE | 1 TB | not published | `email` | terms block expansion | qualifies | `pan-moe` |
| 1yunpan 易云盘 | 100 GB + 400 GB by check-in | not published | `email` | 1 TB/month traffic | qualifies-with-caveat | `1yunpan` |
| QuixiCloud | 10 GB | 20 GB at 6 TB | `email` | per-object cap | qualifies-with-caveat | `quixicloud` |
| 微雨云网盘 | 50 GB | not published | `email` | no API | qualifies-with-caveat | `vyuyun` |
| Ctfile 城通网盘 | 5 TB | 20 GB | `email` | 30-day inactivity clock | qualifies-with-caveat | `ctfile` |
| Lanzou 蓝奏云 | unlimited | 100 MB | `country-phone(86)` | per-object cap | fails-quota | `lanzou-cloud` |
| Lanzou Premium ilanzou | paid | above 100 MB | unverified | no free figure | fails-quota | `lanzou-premium` |
| Lark 飞书 Drive | 100 GB per tenant | 250 MB | `email` | per-object cap | qualifies-with-caveat | `lark-drive-via-multi-tenant-app-credentials` |
| 123pan 123云盘 | 50 GB + 2 TB deduped | 10 GB | `country-phone(86)` | 10 GB/month traffic | qualifies-with-caveat | `123pan-123` |
| UC 网盘 | 2 TB by promo | 1 GB | `country-phone(86)` | per-object cap | fails-quota | `uc-drive` |
| 一刻相册 | unlimited, photos only | media only | `country-phone(86)` | re-encodes at ingest | fails-quota | `yike-album` |
| 豆包 AI云盘 | 5 TB, time-limited | 50 GB | `country-phone(86)` | retention clamp | fails-quota | `doubao-drive` |
| 天翼云盘 Tianyi | 60 GB, promos to 12 TB | 2 GB | `country-phone(86)` | 2 GB/day upload | fails-identity | `tianyi-cloud-drive` |
| 中国移动云盘 China Mobile | 1 TB | not published | `country-phone(86)` | write gate on the driver | fails-identity | `china-mobile-cloud` |
| Aliyun 阿里云盘 | 100 GB | not published | `country-phone(86)` | 0.5 MB/s shaping | fails-quota | `aliyun-drive` |
| Baidu 百度网盘 | 300 GB | 1 GB web / 4 GB client | `country-phone(86)` | 0.1 MB/s shaping | fails-quota | `baidu-pan` |
| Quark 夸克网盘 | 10 GB | 50 MB without a cookie | `country-phone(86)` | shaping, then identity | fails-egress | `quark-cloud-drive` |
| 115 云盘 | 15 GB | 5 GB | `country-phone(86)` | real-name for the API | fails-egress | `115-cloud-drive-115` |
| 联通云盘 China Unicom | 60 GB | not published | `country-phone(86)` | per-object cap | trial-only | `china-unicom-wopan` |
| Weiyun 腾讯微云 | 10 GB | not published | `country-phone(86)` | share refused anonymously | fails-egress | `weiyun` |
| 62Cloud 61Cloud | 61 GB | 61 GB total | `country-phone(86)` | seasonal WebDAV | fails-quota | `62cloud-61cloud` |
| Naver MYBOX | 30 GB | 4 GB | `national-id` | per-object cap | fails-quota | `naver-mybox` |
| 中国科技云 CSTCloud | 1 GB, 20 GB verified | not published | `national-id` | national ID app | fails-quota | `cstcloud-data-capsule` |
| 华为云空间 Huawei | 5 GB | not published | `country-phone(cn)` | region gate | fails-quota | `huawei-mobile-cloud` |
| 小米云服务 Xiaomi | 5 GB | not published | `email` | wrong region | fails-quota | `xiaomi-cloud` |
| 缤纷云 Bitiful | 50 GB | not published | `country-phone(86)` | 10 GB/month egress | fails-egress | `bitiful` |
| Telnyx Cloud Storage | 10 GB | not published | `email` | KYC on a public bucket | fails-quota | `telnyx-cloud-storage-egress-view` |
| netdisk-fast-download | none, it resolves | not applicable | `anonymous` | write gate per pan | qualifies-with-caveat | `netdisk-fast-download-anonymous-multi-pan-parser` |

⚠ **`any-phone` on Ploud is the honest rung and it is not `email`.** The signup form
collects an international phone number, and the JavaScript has no SMS path, so the
only gate actually exercised is an email activation link. The form asks and the system
does not check. Recording that as `email` would be a claim the record cannot support.

## The two worth having, and why only two

**Ploud Storage gives 1 TB for a signup with no payment and no Chinese identity.** It
is Nextcloud 31.0.6.2 with a working WebDAV endpoint at `/remote.php/webdav/`, which
the instance operator documents itself for Windows and macOS. A `PROPFIND` returns a real
SabreDAV 401 with a Basic realm of "Ploud Storage", so the read path exists and is
gated rather than absent.

⚠ **It is one funding decision from vanishing.** A single sponsor, PSIADE in
Toulouse, one data centre near Paris, a donation page and no ad model. A 2024
`help.nextcloud.com` thread already predicted its closure and reported stale
certificates; the instance now answers `status.php` as 31.0.6.2 with valid TLS, so
that post is stale and the fragility it named is not. **Use it with a second copy and
never as the second copy.**

**萌盘 PAN.MOE gives 1 TB for an email address and a human-verification step,
with no phone field, and a WebDAV endpoint at `pan.moe/dav` that answers as DAV
class 2 with `PUT` in `Allow`.** It is the best identity-to-capacity ratio in the
whole corpus.

⛔ **Its terms name the sharding pattern and block it.** Section 5.4 blocks
creating several accounts "for the purpose of expanding capacity" and states
that accounts which do so are closed, and section 2.1 disclaims any durability
guarantee in any form. So the 1 TB is a hard 1 TB and the bytes carry no
promise. That is a fact about the instance operator and not a reason to exclude the
provider: the capacity is real, it is bought with an email address, and what it
cannot be is multiplied.

## Ctfile: the one Chinese pan that opens

Ctfile has run since 2009, and its English registration page offers **Email,
Password and a five-character image human-verification step**, with "Sign up with
phone instead" as the alternative. No +86, no Alipay, no identity photograph.

- **5 TB of shared space, 20 GB per file, no upload speed cap.**
- **30 GB per file on Standard**, CNY 28/month or CNY 98/year.
- **WebDAV advertised on the free tier**.
- **Files are deleted after 30 consecutive days without a sign-in** on a free
  account, or 365 days on a paid one. Over-quota deletes the excess without notice.
- **200,000 files and 10,000 folders per account, 10,000 uploads a day, five
  concurrent downloads and five concurrent uploads.**

Verdict: `qualifies-with-caveat`, binding `retention-clamped`. The monthly sign-in is
not optional and it is the price of the 5 TB. That makes Ctfile a working set behind
a cron job and not an archive.

## The closed set, one line each

Every one of these is recorded so that nobody re-tests it. The reason is the whole
finding and it is different in each case.

- **UC, 2 TB by promo code**: permanent once claimed, and **1 GB per file** makes
  20 TiB of archive 20,000 objects. The cap closes it, not the quota.
- **豆包, 5 TB**: unlimited at launch in 2025-05, cut to a time-limited 5 TB within
  months, 50 GB per file, and **no share links at all**, which removes the only
  reason to want a consumer pan.
- **天翼云盘, promos to 12 TB**: the largest single free pool in the survey and
  **2 GB a day of upload**, so a 4 TB archive takes about five and a half years.
- **一刻相册, unlimited photos**: Baidu's photo loss-leader, media only, re-encoded
  at ingest, and no API of any kind. An unlimited store that returns different bytes
  is not capacity.
- **中国科技云, S3 with unlimited traffic and no request metering** (CSTCloud's
  service, not 中科院's): exactly the workload this topic targets and behind a
  national digital identity app. 1 GB without one.
- **小米, 5 GB**: the only inverted gate in the corpus. Email registration works and
  lands in the region where the storage product was withdrawn in 2022, which is worse
  than a closed gate because it looks open.
- **Weiyun, 10 GB**: the share page embeds the metadata in a JavaScript blob and the
  CGI returns `ret 102027` with a null body. Metadata public, payload refused.
- **62Cloud, 61 GB**: one forum post is the whole evidence base, and WebDAV is issued
  around holidays rather than sold.
- **联通云盘, 60 GB**: the most stable of the three carrier pans because the OpenList
  driver has its own maintained SDK, and 60 GB does not reach the filter.
- **Telnyx, 10 GB with zero egress fees**: the best egress term in the survey and a
  KYC step on a public bucket, at a rate of USD 6.14/TB/month which is three times
  the floor.

## The resolver, which is not a pan

**netdisk-fast-download** is in this set and it is not storage. It converts a share
link into a direct `GET` and stores nothing. Its role is
[`../public-instances/direct-links.md`](../public-instances/direct-links.md), and the
one number worth carrying here is that the free instance covers lanzou, ilanzou,
ctfile, wenshushu, feijipan and ecpan, while **Baidu, Xunlei, Quark, UC, 139, 189 and
Unicom sit behind a keyed endpoint**.

## Chaining

Two of these chain into a real stack and the rest do not.

```
Ctfile (email, 5 TB, 20 GB/file, monthly cron)  ->  OpenList  ->  Cloudflare
萌盘 PAN.MOE (email, 1 TB, WebDAV class 2)       ->  rclone mount  ->  restic
```

The first is a working set and the second is a backup target. Neither is a 20 TiB
archive, and nothing in this document is.

## Where each name is covered

The table above is the index. The names are grouped by region, so two of the three
groups are covered in another document.

| name | section |
| --- | --- |
| Ploud Storage (PSIADE, FR), 萌盘 PAN.MOE, 1yunpan / 易云盘, 易云盘 (1yunpan / E-Disk), QuixiCloud, 微雨云网盘, Ctfile / 城通网盘, Lanzou Cloud, Lanzou Premium, netdisk-fast-download (NFD), Lark / 飞书 Drive | the comparison, and the sections below it |
| 123pan / 123云盘, Baidu Pan, Quark Cloud Drive, 115 Cloud Drive, Aliyun Drive | [`china.md`](china.md), which covers them in full |
| Alist追番, 七米蓝仓库, 延时の奇妙网盘, 晴天网盘, 组织云盘合集, 七十二时.的资源站, pan.timero.xyz, 云顶天宫, 姿势网盘, 小乐的网盘, 槿南盘, 趣盘, 龙猫网盘, 萤火虫资源站 | [`../public-instances/instances.md`](../public-instances/instances.md) |
