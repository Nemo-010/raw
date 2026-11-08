# Russia and the CIS: the any-phone set, and how it closed

The Russian services were the most promising non-Chinese tier because they accept
a phone number from a wide set of countries. This document records what each one
offers now, and the two facts that closed the tier: 5 GB is the free ceiling and
WebDAV became a paid feature.

The answer: **nothing in this set clears the 500 GiB floor for free.** Mail.ru's
1 TB is a paid annual plan, Yandex's free tier is 5 GB, and Yandex's WebDAV closed
on 2026-06-22.

## The comparison

Sorted by free quota, because every row fails on the same axis and the quota is
what separates them.

| service | free tier | per-file cap | WebDAV free | identity | verdict |
| --- | --- | --- | --- | --- | --- |
| Cloud Mail.ru | 1 TB **paid**, RUB 1,560 first year | not stated | yes | `any-phone` | paid-only |
| Yandex Disk | 5 GB | 1 GB without a plan | **no, from 2026-06-22** | `any-phone` | fails-quota |
| Yandex 360 | paid tiers | 50 GB with any plan | yes | `any-phone` | paid-only |

⚠ **The storage topic carries "Mail.ru 1 TB free" records.** They describe an
offer that the landing page read on 2026-10-22 does not make. This document states
what the page says and leaves the reconciliation to the topic that owns those
records.

## Cloud Mail.ru: a paid tier

The landing page read on 2026-10-22 offers:

- **1 TB**, at **RUB 1,560 for the first year** and **RUB 3,000 from the second**,
  with **nine months added**.
- A promotion window of **2026-10-15 to 2026-11-19**.
- Unlimited auto-upload of photos from the phone, which does not consume quota.

No free terabyte tier appears anywhere on the page.

⚠ **The offer is a promotion with a window and a price change in year two.** A
reader who converts RUB 1,560 to a monthly figure and compares it to a 12-month
average has compared a first-year promotional price to a list price. The honest
figure is RUB 3,000 per year from year two, which is the number a plan should use.

The per-file cap, the retention and the egress terms were not stated on the landing
page and are not recorded.

Verdict: `paid-only`, binding `per-object-cap` (as the named-but-unrecorded limit).

## Yandex Disk: 5 GB, and the WebDAV closure

Three facts, each from Yandex's own help pages read 2026-10-22:

- **"By default, users without a plan get 5 GB of storage space."**
  (`yandex.com/support/yandex-360/customers/disk/web/en/enlarge/disk-space`)
- **"Maximum size of a single file for uploading to Yandex Disk: Without a Yandex
  360 plan: 1 GB. With any Yandex 360 plan: 50 GB."**
  (`.../web/en/uploading.md`)
- **"Starting June 22, 2026, WebDAV access requires a Yandex 360 plan."**
  (`.../web/en/webdav`)

⛔ **The third fact decides the verdict.** Yandex was the natural
Russian candidate because its WebDAV endpoint is documented, standard, and
mountable by anything. From 2026-06-22 that endpoint is a paid feature, so the free
tier has no mountable protocol and 5 GB of storage.

Yandex Mail shares the same pool as Disk, so a mailbox and a drive together consume
one 5 GB quota. That is worth stating because it makes the effective free tier
smaller than it looks.

Verdict: `fails-quota`, binding `per-object-cap`. 5 GB with a 1 GB per-file cap is
0.05% of the 10 TiB working set, and the mountable protocol now costs money.

## The pattern, stated once

Three Russian and CIS services, three closures, and none of them is a quota cut:

- a free tier that was never large (5 GB),
- a protocol that moved behind a paid plan (WebDAV, 2026-06-22),
- an offer that is a promotional price rather than a free tier (Mail.ru).

⚠ **A free tier closes more often by losing a protocol than by shrinking.** The
quota number is what a document quotes and the protocol is what a reader needs, so
a reader tracking quotas would have missed the Yandex change entirely.

## What would reopen this tier

A paid Yandex 360 plan at 1 TB or more, priced per TB per month, with WebDAV
included. That is a paid-lane question and
[`../paid/README.md`](../paid/README.md) is where it belongs. No price for the plan
tiers is recorded, so no comparison is made.

## Chaining

Nothing in this set chains into a reader's stack today. If a paid Yandex plan
were bought, the chain would be the standard one:

```
Yandex 360 (paid, WebDAV) -> OpenList -> Cloudflare -> reader
```

See [`../self-hosted/README.md`](../self-hosted/README.md).
