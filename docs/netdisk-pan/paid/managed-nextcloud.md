# Managed Nextcloud: the one thing in this topic a reader can buy outright

A managed Nextcloud is a Nextcloud instance somebody else administers, reached over
WebDAV. It is the only class in this topic where the purchase is a contract, the
quota is bought rather than granted, and the identity cost is a card instead of a
phone number in a country the reader is not in.

This document answers one question: **which managed Nextcloud should a reader with
20 TiB of archive and no budget buy, and what does each one refuse to do?**

The answer, stated first. **Serverdiscounter NEXT Share at 25 TB for EUR 59.95 a
month including VAT is the only tier in the survey that holds the whole archive in
one order, and it is also the cheapest per terabyte at EUR 2.40/TB/month.** Hetzner
Storage Share is the same product with a shorter contract and a worse price. Every
other option here is either too small, or priced with a curve that punishes size, or
free and one funding decision from vanishing.

## The comparison

Sorted by the price at the largest tier, because the need is a quantity and not a
snapshot. All five paid rows were read from the vendor's own pricing table on
2026-10-22 and every figure carries the VAT position, which differs between them.

| host | largest tier | price at that tier | per TB/month | per-file cap | traffic | VAT | identity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Serverdiscounter NEXT Share | 25 TB | EUR 59.95/month | EUR 2.40 | 10 GB | flatrate | included | `card` |
| Hetzner Storage Share | 10 TB | EUR 27.39/month | EUR 2.74 | not published | unlimited | excluded | `card` |
| DanubeData Storage Share | 10 TB | EUR 29.99/month | EUR 3.00 | not published | unstated | unstated | `card` |
| Allsync | 10 TB | EUR 4/TB floor | EUR 4.00 floor | "unlimited" | "unlimited" | varies | `card` |
| nextfiles.one | 10 TB | EUR 99.99/month | EUR 10.00 | not published | unstated | included | `card` |

⚠ **The VAT column is not bookkeeping.** Serverdiscounter and nextfiles quote
including VAT and Hetzner quotes excluding it, so comparing the headline numbers
understates Hetzner by the local rate. At a 19% German rate, NX31 becomes EUR 32.59
and the gap to Serverdiscounter widens from EUR 2.19 to EUR 7.40 a month.

## Serverdiscounter NEXT Share: the one to buy

Twenty-five terabytes in a single order is more than 20 TiB of archive, so this is
the only option that does not require a second subscription or an internal split.
Full admin access with per-user storage quotas means the archive can be divided into
shares with separate credentials without buying more accounts, which is the
affordance that makes one paid unit behave like several.

- **EUR 4.95 for 1 TB, EUR 15.95 for 5 TB, EUR 29.95 for 10 TB and EUR 59.95 for
  25 TB, per month including VAT** (`documented`, 2026-10-22,
  `serverdiscounter.com/en/nextcloud`).
- **10 GB per file on every tier, including the 25 TB one.** This is the number that
  shapes the plan and it does not improve with size.
- **Traffic flatrate**, stated as a line of the feature comparison rather than a
  footnote, with WebDAV, an admin panel, storage quotas, app installation and
  versioning on all four tiers.
- **Minimum term one month, monthly cancellation, no setup fee, 30-day money-back.**
- **A 14-day free trial with no card**, deleted unless extended.

Verdict: `qualifies`, binding `per-object-cap`. The archive becomes about 2,000
objects at 10 GB each, which is a chunker setting and not an obstacle.

## Hetzner Storage Share: the boring one, and why it is not cheaper

Hetzner is the name a reader is most likely to arrive with, and it is the right
answer for a reader whose first concern is that the provider still exists in five
years. It is not the cheapest.

- **NX11 1 TB at EUR 4.29, NX21 5 TB at EUR 14.19, NX31 10 TB at EUR 27.39**, per
  month excluding VAT, billed hourly to a monthly maximum
  (`documented`, 2026-10-22, `hetzner.com/storage/storage-share/`).
- **3, 7 and 10 users per instance**, in that order. ⚠ This is a hard cap, and it
  matters: a plan that divides the archive across more than ten credentials needs a
  different provider.
- **Unlimited internal and external traffic**, stated as a product feature.
- **No published per-file cap.** The FAQ answers the related question honestly: an
  administrator's "unlimited" per-user quota "will actually be limited by the
  overall storage quota size of the Storage Share instance".
- **No minimum contract period and no cancellation period**, and the vendor states
  a plan change causes no data loss. Backups of the database and the storage backend
  run several times a day to a host the instance is not running on, restorable from
  konsoleH.
- **Falkenstein, Germany**, RAID with checksummed integrity checking.

Verdict: `qualifies`, binding `per-object-cap`. Ten terabytes is half the archive,
so this is a two-unit purchase at EUR 54.78 a month before VAT.

## DanubeData Storage Share: S3 behind a Nextcloud facade

The most interesting architecture of the five and the thinnest documentation. The
storage is documented as an object store with a Nextcloud front, so in principle the
same bytes are reachable by either path without a second copy.

- **DD1 Sulina 1 TB at EUR 4.99, DD5 5 TB at EUR 14.99, DD10 10 TB at EUR 29.99**,
  per month (`documented`, 2026-10-22, `docs.danubedata.ro/storage-share`).
- **Up to 10 subdomains and 200 concurrent connections** on the largest profile,
  which is a sharding affordance none of the others offer.
- **Nextcloud 32, S3-backed, dedicated CPU and memory, automatic TLS.**
- **Falkenstein, Germany**, the same data centre as Hetzner, so the failure domain
  is shared.

⚠ **Two things a buyer needs are not published**: the traffic terms, and whether the
S3 backend is reachable with credentials the customer holds. The WebDAV page under
`docs.danubedata.ro/storage-share/webdav` returned 404 on 2026-10-22, so the
endpoint is claimed in the profile table and documented nowhere else.

Verdict: `qualifies`, binding `request-rate`. EUR 3.00/TB/month at 10 TB makes it the
cheapest of the three 10 TB options, and the unverified traffic terms are the reason
it is not the recommendation.

## Allsync: the best-shaped contract and the least published price

Per-terabyte billing with no published egress line is the right shape for a hot
working set, because the cost tracks the bytes stored and not the bytes served.

- **A TB pool from 1 to 10 TB starting at EUR 4**, monthly or annually, and a GB
  pool from 10 to 1,000 GB starting at EUR 0.10/GB billed annually
  (`documented`, 2026-10-22, `allsync.com/pricing`).
- **Bandwidth, file size, users, devices and speed all stated as unlimited.**
- **End-to-end encryption is optional and needs a master password.** It is mutually
  exclusive with server-side Office, which is the usual Nextcloud trade.
- **Registered Dutch company, EU storage, cryptocurrency accepted**, which matters to
  a buyer who cannot or will not use a card in their own name.

⛔ **The per-terabyte ladder above 1 TB is not published.** The page states a
starting price and no tier table, so "10 TB for EUR 40 a month" is arithmetic a
reader might do and the vendor has not said. That is the reason this row carries a
floor and not a price.

Verdict: `qualifies`, binding `per-object-cap`. Nothing published can bind, so the
per-file ceiling is unestablished rather than absent.

## nextfiles.one: the only Seafile, with an inverted price curve

Worth knowing about for one reason: it is the only reseller here that also offers
Seafile, which gives library-level end-to-end encryption that Nextcloud does not.

- **1 TB at EUR 4.99, 3 TB at EUR 14.99, 5 TB at EUR 39.99 and 10 TB at EUR 99.99**,
  per month including VAT (`documented`, 2026-10-22).
- **The per-terabyte price rises with size**, from EUR 4.99/TB at 1 TB to EUR 10/TB
  at 10 TB. Every other reseller falls. A curve that inverts usually means the small
  tier is subsidised and the large tiers are for customers who will not price-compare.
- **One month free trial** on the Nextcloud plans.
- **Germany, ISO 27001 data centres, seven days of disaster-recovery backups.**

⚠ **The Seafile price is per tier, not per terabyte.** The live Seafile page prices
Business S at EUR 9.90 for **500 GB** and up to three users, and prices Business L
per user.

Verdict: `qualifies`, binding `per-object-cap`. A small-instance option, not an
archive target.

## The four that fail, and what each one proves

These offer the same interface and a reader will meet them in the same search.
Each fails for a different reason, and three of the four failures are the classes
worth naming.

| host | free tier | why it fails | what it proves |
| --- | --- | --- | --- |
| Disroot Cloud | 2 GB, up to 60 GB purchased | the ceiling is 60 GB at any price, and capacity above 2 GB is a human-reviewed form | a write gate can sit on capacity itself, not just on content |
| Shadow Drive | 20 GB | 20 GB per upload on every plan including 2 TB, and signup is fenced to 12 countries | a per-file cap that never improves with the tier is the constraint that survives paying |
| TAB.DIGITAL Nextcloud | 8 GB, no card | 8 GB is 1.6% of the filter and the free plan is one user | a free tier can survive a repricing, which is rare enough to record |
| TrekMail Drive | 5 GB plus a 30-day terabyte | the trial is the only large capacity and the paid ladder is behind a slider | a provider can design for programmatic ingest and still not be reachable for free |

Disroot's ceiling is the sharpest of the four: EUR 110 a year buys 60 GB, which is
EUR 152/TB/year. Price is not the obstacle. The obstacle is that the instance
operator has decided 60 GB is the maximum and reviews each request by hand.

Verdicts: Disroot `fails-quota`, Shadow Drive `fails-quota`, TAB.DIGITAL
`fails-quota`, TrekMail `trial-only`. All four are recorded with `write-gated` or
`per-object-cap` as the binding constraint.

## What a reader should do

Buy the 25 TB Serverdiscounter tier, mount it over WebDAV, and put a cache in front.
Two things then decide whether the plan works, and both are cheap to test before
paying: whether a 20 GB file uploads, and whether the flatrate traffic claim survives
a month of real serving. The 14-day trial with no card exists for exactly that.

If the answer has to be free, nothing in this document helps. The free Nextcloud
options here top out at 8 GB and 20 GB, and the only free tier that reaches a
terabyte is Ploud Storage in [`../pans/western.md`](../pans/western.md), which is
one sponsor away from closing.

## Where each name is covered

The table above is the index. Each name is covered in the section named.

| name | what it is | section |
| --- | --- | --- |
| Hetzner Storage Share | managed Nextcloud, EUR-priced | Hetzner Storage Share |
| Serverdiscounter NEXT Share | managed Nextcloud, 25 TB ceiling | Serverdiscounter NEXT Share |
| DanubeData Storage Share | S3-backed managed Nextcloud | DanubeData Storage Share |
| nextfiles.one (Nextcloud CE + Seafile Pro) | Nextcloud and Seafile reseller | nextfiles.one |
| Allsync | pay-as-you-go managed Nextcloud | Allsync |
| Disroot Cloud | donation-funded Nextcloud | The four that fail |
| Shadow Drive | hosted Nextcloud, 12 countries | The four that fail |
| TAB.DIGITAL Nextcloud (cloud.tab.digital) | managed Nextcloud, free 8 GB | The four that fail |
| TrekMail Drive | WebDAV plus REST plus MCP | The four that fail |

## Chaining

All five paid hosts chain identically, which is the point of buying one:

```
managed Nextcloud  ->  WebDAV  ->  OpenList  ->  Cloudflare  ->  reader
```

The Nextcloud ends the search for a durable tier that this topic could not answer
from the free side. [`../pans/README.md`](../pans/README.md) is why: every free pan
with real capacity is behind a phone number, and every free pan with an open
registration is under a terabyte.
