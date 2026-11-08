# Chinese pans: the +86 wall, and the one gate that opens

Every large Chinese consumer pan is behind a mainland phone number or a real-name
check, with one exception. This document is the wall, the exception, and the
evidence for each.

The answer: **Ctfile takes an email address and gives 5 TB with 20 GB per file.**
Nothing else in the Chinese set is reachable without a +86 number, and the pans
with the largest quotas are the ones with the strictest gates.

## The comparison

Sorted by whether a registrant without a PRC identity can register, because that
matters for a closed gate.

| pan | free tier | per-file cap | registration | identity | reachable |
| --- | --- | --- | --- | --- | --- |
| Ctfile | 5 TB | 20 GB | email + password + human-verification step | `email` | **yes** |
| Lanzou | unlimited | 100 MiB | Chinese-language form | `any-phone` | unverified |
| 123pan | 2 TB | 100 GiB | phone | `country-phone(86)` | no |
| Baidu | 2 TB | 1 GB web / 4 GB client | phone | `country-phone(86)` | no |
| Quark | 10 GB | none stated | phone | `country-phone(86)` | no |
| UC | 10 GB | none stated | phone | `country-phone(86)` | no |
| 115 | withdrawn | - | phone | `country-phone(86)` | no |

## Ctfile: the exception, in full

The registration page offers **Email**, **Password** and a human-verification step, with "Sign up
with phone instead" as the alternative. No Alipay, no +86, no identity photo. The
page also advertises direct link sharing, WebDAV and online media playback
(`documented`, 2026-10-22).

| measure | value | source |
| --- | --- | --- |
| free shared space | 5 TB | `ctfile.com/register` |
| per-file cap, free | 20 GB | `ctfile.com/help` |
| per-file cap, Standard | 30 GB | `ctfile.com/help` |
| files per account | 200,000 | `ctfile.com/terms`, cl. 3.2.7 |
| folders per account | 10,000 | `ctfile.com/terms`, cl. 3.2.7 |
| uploads per day | 10,000 | `ctfile.com/terms`, cl. 3.2.7 |
| concurrent downloads | 5 | `ctfile.com/terms`, cl. 3.2.9 |
| concurrent uploads | 5 | `ctfile.com/terms`, cl. 3.2.9 |
| deletion without sign-in, free | **30 consecutive days** | `ctfile.com/terms`, cl. 3.2.5 |
| deletion without sign-in, paid | 365 consecutive days | `ctfile.com/terms`, cl. 3.2.5 |
| Standard | CNY 28/month or CNY 98/year | `ctfile.com/` |
| Super | CNY 38/month or CNY 258/year | `ctfile.com/` |

⚠ **The 30-day clock is the number that decides how it can be used.** A monthly
sign-in keeps a free account's files, and nothing else does. That makes Ctfile a
working set that a cron job maintains, and it makes it unsuitable as an archive
without a paid tier. Even the paid tier's clock is 365 days, not permanent.

⛔ **Over-quota deletes the excess without prior notice.** Terms 3.2.6 states that
CTFile may "delete files exceeding the quota without prior notice". A file that
pushes an account over its quota can lose other files, so the reader's own
bookkeeping is the only protection.

The WebDAV tier question is worth stating precisely: WebDAV is advertised on the
free tier and as "WebDAV batch download" on Super, and clause 2.7 restricts it to
"batch uploads and batch downloads, but must not be used for synchronization or
backup". The protocol is available; the use is bounded by the vendor's terms,
which is a technical constraint on how a bridge may mount it and not a legality
question.

Verdict: `qualifies-with-caveat`, binding `retention-clamped`.

## Lanzou: unlimited space, and a 100 MiB cap

Lanzou (蓝奏云) is the cheapest place in the Chinese set to put a file under 100 MiB
that must be downloadable without an account. That is a narrow and real use.

- **Unlimited total storage**, stated by the vendor (`documented`, 2026-10-22).
- **No download speed, volume or count limit**, and share links are permanent.
- **100 MiB per file**, from the resolver project's first-party driver table.
- **No WebDAV and no official API.** The route is a share-link resolver.

The vendor page says `拥有无限制的总存储空间` and offers registration, upload and
share as three steps. It does not publish the per-file cap, which is why the cap is
cited to the resolver's table and not to the vendor.

⚠ **Registration is a Chinese-language form**, so `any-phone` is an inference
from the form's language and not a measured gate. The identity cost is unverified
and at least a phone.

Verdict: `fails-quota`, binding `per-object-cap`.

## The closed set, and the shape of each closure

**Baidu**: 2 TB free, and the free per-file cap is 1 GB on the web client and 4 GB
on the Windows client (`wangpan.baidu.com/disk/help`, read 2026-10-22). Registration
is a phone number. A free account that has not signed in for two years is reduced
to 100 GB.

**Quark and UC**: 10 GB free each and share downloads refused without a login. The
resolver's driver table marks both as `免登陆下载: ❌`, which is the one column that
matters: a pan that will not serve a share to a logged-out visitor cannot be a
read path for a registrant without a PRC identity even if that registrant could
register.

**123pan**: 2 TB free with a 100 GiB per-file cap, and shares above 100 MiB
require a login. The resolver project's README notes that the large-file path
"失效，需要登录" from 2023-08-24. That is a read path that closed and did not
reopen.

**115**: the free-space allocation was withdrawn. A community thread from
2026-07-31 answers "现在没有了，唯有氪金", "there is none now, only paying". The
account resale market is the only route and it is in
[`../paid/README.md`](../paid/README.md).

⛔ **The pattern in this section is the finding.** Every closure is on the read
path and not on the quota. The quotas stay large and the share downloads move
behind a login, which removes exactly the capability this topic wanted.

## Aliyun Drive, recorded as a trajectory

Aliyun Drive is not a candidate and its history is the cleanest example of how this
market moves. It launched claiming no speed limit, then limited non-members to
100 KB/s in March 2025, restored 500 KB/s with a 16-thread ceiling in May 2025, and
freezes an account 14 days after it exceeds a shrunken quota
(`linux.do/t/topic/477005`, `linux.do/t/topic/657858`, `linux.do/t/topic/567345`,
all `reported`). One forum post from 2026-04 gives 256 KB/s for a non-member
download.

⚠ **Four numbers from four forum posts in fourteen months is not a measurement.**
The trajectory is the finding: a pan's free tier is a marketing decision that is
revised, and a design that depends on one is a design with a deadline. The numbers
are `reported` and no record is created, because none of them is a quota the
reader can act on.

## Chaining

Ctfile is the only Chinese pan that can sit under a bridge for a reader without a
PRC identity, and the clock is what the bridge must be built around.

```
Ctfile (email, 5 TB, 30-day clock) -> OpenList -> Cloudflare -> reader
```

The monthly sign-in is not optional. It is a job, and the job is the price of the
5 TB. See [`../self-hosted/alist-openlist-ops.md`](../self-hosted/alist-openlist-ops.md).
