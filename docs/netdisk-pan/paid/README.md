# Paid capacity: what is cheapest, and what the resale market shows

This document names what capacity costs when the free answer fails, and reads the
resale market as evidence rather than as a shop. The resale market is the most
informative thing in this topic about how "unlimited" quotas behave.

The answer: **the cheapest paid capacity that works is a pooled tenant, rented or
owned, and the rental market prices it at CNY 15 to 20 per month for unlimited
space with a 400,000-file cap and a 750 GB per day upload cap.**

## The comparison

Sorted by cost per unit of usable capacity, with the thing that actually binds in
the last column.

| offer | price | capacity | binding | reliability |
| --- | --- | --- | --- | --- |
| rented Google team drive | CNY 20/month, 6-month minimum | "unlimited" | 400,000 files, 750 GB per day upload | the tenant is not the reader's |
| rented domain | quoted separately | "unlimited" per drive | 2.5 TB per day per domain | the same |
| Ctfile Standard | CNY 28/month or CNY 98/year | 5 TB shared | 30 GB per file, 365-day clock | a published contract |
| Ctfile Super | CNY 38/month or CNY 258/year | 10 TB shared + 2 TB private | 100 GB/month direct-link traffic | a published contract |
| 123pan 20 TB | CNY 258/year | 20 TB | identity check | not reachable |
| Cloud Mail.ru | RUB 1,560 year one, RUB 3,000 after | 1 TB | not stated | a promotional window |

⚠ **"Unlimited" appears once in this table and it is the row with the worst
reliability.** That is not a coincidence: a quota sold as unlimited is one that is
being arbitraged, and the arbitrageur's account is the thing that fails.

## The resale market, read as evidence

Four listings on one forum between 2024-05 and 2026-10, at CNY 15 to 20 per month:

| listing | date | price | caps stated |
| --- | --- | --- | --- |
| "再开一车gd无限盘" | 2025-06-01 | CNY 20/month, 6 months | 400,000 files, 750 GB per day upload, downloads unlimited |
| "出租团队盘-正真的无限空间" | 2026-07-03 | CNY 20/month, 6 months | 400,000 files, 750 GB per day, 2.5 TB per day for a rented domain |
| the same seller, later | 2026-10-04 | CNY 20/month, 6 months | the same |
| "出租无限gd团队盘" | 2024-05-08 | CNY 15/month | not stated |

⛔ **Two independent sellers quote the same two caps.** 400,000 files and 750 GB
per day appear in three listings by two sellers across sixteen months, which is the
strongest evidence in this topic that those are the real limits of the underlying
product and not a seller's invention.

⚠ **The buyer's side of the thread is the finding.** One reply says
`200T的workspace都是卡bug扩容的`, "the 200 TB workspaces are all expanded past the
quota by a software bug", and another reports `我的团队盘，直接消失不见了`, "my team drive
just vanished". A market exists because the underlying quota is being arbitraged,
and the arbitrage is what fails.

The record is `dossier/netdisk-pan/115-team-drive-rental.json`,
`verdict: paid-only`, `confidence: reported`.

## What a rental actually buys

A permission on somebody else's shared drive. The bytes live on Google's storage
under the seller's tenant, and the reader's access ends when the seller stops
paying or when Google closes the tenant.

That is a real thing to buy and it is not storage in the sense this corpus means.
The distinction is the same one the public-instance documents make: a rented
tenant is a bridge over somebody else's account, and the account is the failure
point.

⚠ **A six-month minimum with no mid-term refund is stated in every listing read.**
The seller's own terms describe the risk accurately, which is worth recording
because it means the price is not the whole cost.

## Ctfile, as the paid comparison

Ctfile is the only pan in the survey that a foreign registrant can pay for at list
price without an identity check, and its paid tiers are the honest baseline:

| tier | price | shared space | private space | per-file |
| --- | --- | --- | --- | --- |
| Free | CNY 0 | 5 TB | - | 20 GB |
| Standard | CNY 28/month, CNY 98/year | 5 TB | - | 30 GB |
| Super | CNY 38/month, CNY 258/year | 10 TB | 2 TB | 30 GB |

Source: `ctfile.com/`, read 2026-10-22. The Super tier adds 100 GB per month of
direct-link traffic, which is 3.3 GB per day and therefore 0.3% of the serving
workload. **That is the number that decides whether Super is worth it: it
is not.**

⛔ **A direct-link traffic allowance is not egress capacity.** 100 GB per month is
3.3 GB per day against a daily target of 500 GB to 1 TiB. The tier is worth buying
for the space and not for the traffic.

## The arithmetic that says paid is not the answer here

The working set is 30 TiB: 10 TiB of hot storage and 20 TiB of cold storage.

At the resale market's implied price, unlimited is CNY 240 per year. At Ctfile's
list price, 10 TB is CNY 258 per year. Both numbers look small, and both describe a
product whose capacity is somebody else's account.

⚠ **The storage topic owns the cheapest-paid comparison and its numbers.** This
document's claim is narrower: in the pan market, the cheapest paid capacity is
rented and the rental is the least reliable thing in the table.

## What to do instead, if the free answer fails

Rent a managed box. The storage topic's `paid/README.md` prices a managed Nextcloud at
EUR 2.40 per TB per month and a Hetzner Storage Box at EUR 2.03, both on somebody else's
hardware with an invoice. That is the comparison a reader should make, and this topic does
not restate its numbers.

⛔ **Buying a disk is cheaper and is not an option here.** No topic recommends it.

## Chaining

A rental chains exactly like a tenant:

```
rented team drive -> OpenList -> Cloudflare -> reader
```

and it inherits the rental's failure. See
[`../self-hosted/README.md`](../self-hosted/README.md#why-the-tenant-is-the-weak-layer-and-the-bridge-is-not).
