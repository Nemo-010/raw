# Chinese retrieval

The Chinese market does not sell "debrid". It sells cloud download, membership
acceleration, traffic packs, and per-file fetch (daixia). The same job is done, and
the price is often a tenth of the Western one.

## The answer

⭐ **115's own product API is the price list, and it is the cheapest retrieval in
the corpus.** `vip.115.com/?ac=product_list&ct=product` returns JSON rather than a
page: 1 TB of login-free download traffic is CNY 55, and the 100 TB pack is CNY
38.88/TB. An eight-year membership with 50 TB is CNY 915, or CNY 9.53 a month, and
carries 1,500 cloud-download tasks a month with no byte meter on the owner's own
retrieval.

⭐ **Xunlei Super Member is the cheapest recurring allowance**: CNY 9.93 a month
for 10 TB a month of cloud retrieval.

⛔ **Both are closed by identity.** 115, Quark, Baidu, Aliyun, 123pan, Tianyi and
Taobao all require a +86 phone number. **PikPak is the only Chinese service in the
corpus with an email gate**: 6 GB free, 10 TB on a plan at roughly USD 20 to 58 a
year, and the only genuine server-side cloud downloader reachable without a
mainland number.

## The price ladder

| service | price | what it buys | identity |
| --- | --- | --- | --- |
| 115 traffic pack | CNY 55/TB, CNY 38.88/TB at 100 TB | login-free download traffic | +86 |
| 115 eight-year plan | CNY 915 | 50 TB plus 1,500 cloud tasks a month | +86 |
| Xunlei SVIP | CNY 9.93/month | 10 TB/month cloud retrieval | any-phone |
| PikPak | USD 20 to 58/year | 10 TB plus cloud download | email |
| 77File VIP | CNY 598/TB | 25 or 100 high-speed requests a day plus traffic | +86 |

⚠ **115's traffic pack is debited from the sharer, not the downloader.** That is
what makes CNY 38.88/TB a public egress price rather than a personal allowance,
and it is why it is 13 times cheaper than the best daixia service.

## The speed ladder

⭐ **Xunlei publishes the only speed ladder in the market**, and it is the clearest
statement of what a membership buys anywhere in this corpus:

| tier | speed |
| --- | --- |
| free | 586 KB/s |
| member | 7.82 MB/s |
| SVIP | 15.8 MB/s |

⚠ **Free Xunlei has no cloud-add at all.** Its own page says the offline download
and speed channel have been merged into the paid acceleration feature, so free
Xunlei is not a debrid in any sense.

## Per-file fetch (daixia)

A daixia shop fetches a pan link and returns a direct link for a fee. Two models:

| model | price | note |
| --- | --- | --- |
| Taobao retail | CNY 0.5 to 6.99 per file | about CNY 0.2/GB on a 10 GB file; needs a +86 account and a human per order |
| specialist sites | CNY 0.53 to 1.2/GB | more expensive per GB, no human |
| 8591 (Taiwan) | NT$10 per file, 24-hour delivery | no mainland identity |

⚠ **A per-file price is a bet on object size.** CNY 2 a file is USD 30.97/TiB at
10 GB files, USD 288/TiB at 1 GiB, and USD 6.19/TiB at 50 GB. The same sticker
price spans 46 times the cost per byte.

⭐ **Tuzipan is the only daixia that publishes a per-host multiplier**: rapidgator
1.5x, takefile 1.6x, katfile 1.0x. Its CNY 598/TB sticker is therefore CNY 897/TB
on the hosts people actually use, and the vendor says so.

## miaochuan (instant upload) and deduplication

"Instant upload" (miaochuan) proves the host already holds the exact bytes. It is alive
at 123pan, Guangya (which imports from Baidu, Quark, Tianyi and 123) and Xunlei's
drive, closed at Aliyun Drive, and effectively closed at 115. For a reader it is a
deduplication oracle: a hit means the object is retrievable without an upload.

## What is dead

- **PanDownload and its forks** are gone; every 2026 result is a client for a
 service that no longer answers.
- **The old unlimited-speed era** ended with the membership speed ladder. A free
 account is 586 KB/s, which is 49 GiB a day at best and usually less.

## How it composes

1. **PikPak first**, because it is the only email-gated service and 10 TB at USD 20
 to 58 a year is the cheapest reachable capacity in the corpus.
2. **A daixia shop** for a single file on a host PikPak does not cover, priced per
 file and only for objects above about 10 GB.
3. **115's traffic pack** only if a +86 number exists, because at CNY 38.88/TB it
 beats every other option by an order of magnitude.

⚠ **Do not compare a CNY price to a USD one without the rate.** 115's CNY 38.88/TB
is about USD 5.40/TB at 7.2 CNY/USD; the record carries the rate and its date.
