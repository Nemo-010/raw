# Lifetime deals and discount channels: which one is real, and when to buy

A lifetime deal is a bet that the vendor outlives the customer's data. The class is
attractive because the arithmetic is compelling: USD 36 per TB once is USD 0.60 per
TB per month over five years, which is below every recurring rate in the paid lane. The question
is which of them is a bet worth taking, and the answer turns on two things a pricing page does
not show: whether the vendor's egress term survives the read pattern, and whether the reseller
channel is the same company.

This document covers 27 qualifying records: lifetime plans sold direct, the same plans
through a discount channel, the discount coupons that recur, and the paid revisit of providers
the free lane rejected. 13 were rejected, and the rejections are the most useful half.

## The comparison

Sorted by the one-time cost per TB, because that is what a lifetime deal is. A recurring plan in
this table is present because it competes on the same axis.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Icedrive, lifetime plans (direct) | Lifetime Personal 500 GB $229 (from $344)... | - | email | fails-egress |
| Internxt, 100 TB lifetime via StackSocial | 100 TB lifetime, $974.97 (suggested $9,900... | - | email | fails-quota |
| pCloud, lifetime plans (direct) | 500 GB $219, 2 TB $499, 10 TB $1,499 one-time. Live as of 2026-10-17 per price audit... | - | email | fails-quota |
| Drime Secure Cloud Storage 10 TB lifetime... | StackSocial lifetime SKUs: 2 TB $149.97 - 6 TB $249.97 - 8 TB $279.97 - 10 TB $359.97... | - | email | qualifies-with-caveat |
| Hetzner Storage Box BX41 (20 TB) | 20 TB (BX11 1 TB / BX21 5 TB / BX31 10 TB / BX41 20 TB) | - | card | qualifies |
| HostBrr StorageBox 16 TB (BFBOX recurring coupon) | 500 GB / 1 / 2 / 4 / 8 / 16 TB, US (Utah) and DE... | - | email | qualifies-with-caveat |
| NetDynamics24 Germany Backup SFTP (LET50% recurring) | 250 GB $3/mo - 500 GB $4/mo - 1 TB $6/mo - 2 TB $11/mo. Germany... | - | email | qualifies-with-caveat |
| PulsedMedia M10G Storage Box (16 TB) | 16 TB HDD RAID5 (4/8/16/32 TB tiers) | per-ip-shaping: 100 Mbps sustained egress | email | qualifies |
| ServaRICA Polar Bear / Killer Whale / Mammoth storage | Opossum 1 1 TB $29/yr - Polar Bear 2 TB $5/mo or $48/yr - Killer Whale 3.5 TB $8.50/mo... | - | email | qualifies-with-caveat |
| Uloz.to Disk (ULTRA 25 TB) | PREMIUM 3 TB $6.50/mo - MAX 12 TB $16/mo - ULTRA 25 TB $32/mo - ULTIMATE 50 TB $64/mo | per-object-cap: MAX 12 TB | email | fails-quota |
| Drime (Advanced / 10 TB lifetime) | Subscription: Starter 500 GB, Essentials 2 TB, Professional 3 TB... | - | email | qualifies-with-caveat |
| Filen Pro X (10 TiB) | Pro I 200 GiB / Pro II 500 GiB / Pro III 2 TiB / Pro X 10 TiB... | - | email | qualifies |
| Icedrive Lifetime Personal+ 2 TB | Lifetime Personal 500 GB $229 (list $344)... | - | card | qualifies-with-caveat |
| Internxt lifetime (via StackSocial) | 1 TB / 2 TB / 5 TB on internxt.com; StackSocial carries 5 TB $229.99... | write-gated: (CLI bridge) + request-rate | card | qualifies-with-caveat |
| Jottacloud Pro 20 TB | 10 / 20 / 30 / 50 TB fixed tiers, 1 user each | - | email | qualifies |
| Jottacloud Unlimited (Personal) | Unlimited storage; 1 user. Free 5 GB tier exists | per-ip-shaping: upload side only | email | qualifies-with-caveat |
| Koofr (Suitcase XL+ 500 GB / 5 TB 5XXL) | Briefcase 10/25/100 GB at EUR 0.5/1/2 per mo... | per-ip-shaping: on public links, daily granularity Briefcase 10/25/100 GB at... | email | fails-quota |
| MEGA S4 (object storage) | No upper limit. Base 3 TB included from EUR 15/mo; EUR 3.50 per additional TB | - | email | qualifies |
| pCloud Premium Plus 2 TB / Ultra 10 TB (lifetime) | 500 GB $219; 2 TB $499 (list $709); 10 TB $1,499... | pull-count: ish only on public links | card | qualifies-with-caveat |
| Synology C2 Object Storage | Sold in whole-TB increments from 1 TB | - | email | qualifies-with-caveat |
| Zoolz Cloud Backup 12 TB | 2.5 TB (2 TB cold + 500 GB hot) $79.99/yr; 7 TB (6+1) $239.99/yr... | write-gated: cold storage means the restore is a request workflow | card | qualifies-with-caveat |
| 1fichier Premium GOLD (10 TB cold storage) | Unlimited hot storage; 10 TB cold storage included... | per-object-cap: 300 GB/file | email | qualifies-with-caveat |
| Hetzner Storage Box BX21 (5 TB) | 5 TB; 20 snapshots | - | card | qualifies |
| Icedrive 3 TB | 3 TB; $9.99/mo or $119.88/yr | - | card via stripe... | qualifies-with-caveat |
| InterServer Storage ST 600 (20 TB) | 20 TB space, 20 TB transfer/month, 60 domains, DirectAdmin | - | card | qualifies-with-caveat |
| pCloud Ultra 10 TB | 10 TB storage; monthly $29.99 / annual $359.88 | - | card | qualifies-with-caveat |
| PrismDrive 10 TB annual | 10 TB; $249/yr. Ladder: 2 TB $79/yr, 5 TB $149/yr, 10 TB $249/yr | - | card | qualifies-with-caveat |

## What the class is

Four purchase shapes.

**A lifetime plan sold direct.** Icedrive, pCloud and Internxt sell a one-time payment for a
fixed capacity. The bet is on the vendor's continued operation, and there is no escrow.

**The same plan through a reseller.** StackSocial sells Internxt and Drime at a discount. The
reseller channel is a different business from the vendor, and a licence bought through it is
governed by two sets of published conditions.

**A recurring discount.** HostBrr's BFBOX gives 40% recurring and NetDynamics24's LET50% gives
50% recurring. These are not lifetime deals; they are a permanently lower rate, which is a
strictly better instrument if the vendor honours it.

**A paid revisit of a rejected free tier.** 1fichier GOLD, Hetzner BX21, Icedrive 3 TB, InterServer
and pCloud Ultra are in this document because the free lane rejected them on a clock or a cap and
the paid tier removes that constraint.

## The four numbers, which are four products

The paid lane's headline rates are the ones most likely to be misused, so they are stated with
their class.

**1fichier GOLD at EUR 0.90 per TB** is cold archive only. EUR 108 per year for 10 TB, with
"Unlimited downloads, no monthly allowance", and additional cold storage at EUR 1 per TB per
month. The files are reclassified by access age, so the hot tier cannot be relied on as a
working set. It is the cheapest figure in this topic and it buys the archive column.

**Uloz.to at USD 1.28 per TB** buys 25 TB with a transfer allowance of about twelve times the
stored volume, on a rclone-native backend. It is hot storage at a cold price and its constraint
is the ratio.

**PulsedMedia at EUR 1.69 per TB** buys 16 TB on a 100 Mbps port, which is 0.982 TiB per day. The
allowance is not the binding limit; the port is. The arithmetic is in
[`storage-boxes.md`](storage-boxes.md).

**Hetzner BX41 at EUR 2.03 per TB** buys 20 TB with contractually unlimited traffic and a
fair-use threshold 8.3 times above this workload. It is the only one of the four that survives a
3:1 read pattern on a contractual term rather than a ratio.

A cold-cheapest number cannot substitute for a serving tier and a hot number is not a fair
comparison against cold storage. A reader who reads the column as "cheapest overall" will buy
the wrong product, and that is the single most likely misuse.

## The lifetime arithmetic, done honestly

The claim that makes a lifetime deal attractive is that it amortises below a recurring rate. It
does, and the amortisation has to carry the risk.

Drime at USD 359.97 for 10 TB is USD 36 per TB once, which is USD 0.60 per TB per month over
five years. Internxt at USD 269.97 for 10 TB is USD 27 per TB once, or USD 0.45 per TB per month
over five years. pCloud Ultra at USD 1,499 for 10 TB is USD 149.90 per TB once.

Three things the amortisation does not capture. First, a lifetime deal at a fixed capacity cannot
grow, so an archive of 20 TiB needs two of them. Second, the vendor's egress term applies to the
lifetime plan exactly as it does to a monthly one, and a 3:1 read pattern is the same problem
whether the storage was prepaid or not. Third, the failure mode of a lifetime vendor is
insolvency rather than a price rise, and there is one example: PolarBackup
permanently closed every lifetime account in 2024 and deleted the data.

That is the whole argument for treating a lifetime deal as a bet rather than a discount, and it
is why the record for each carries `reliability_note` rather than a verdict alone.

## When to buy

Black Friday 2026 is 27 November. Three facts about the
timing are worth recording because they are checkable and they change a purchase date.

HostBrr's BFBOX gives 40% recurring, which at 16 TB is about USD 1.11 per TB. PulsedMedia runs
flashes and an effective EUR 1.02 per TB has been observed. Hetzner never discounts the Storage
Box: Black Friday 2024 was a price increase. STRATO's promotional window is genuinely February
rather than November.

So the timing advice is specific: wait for 27 November if the vendor in question has a history of
discounting, and do not wait for Hetzner.

Four providers hold two records each in this document, because the ledger assigns the
free-lane and paid-lane spellings of the same offer to two sections. Icedrive, pCloud, Hetzner and
HostBrr each appear once as a lifetime or discount listing and once as a paid revisit. The numbers
are the same and the records carry both spellings in `provenance`; a reader should read the pair as
one offer.

## The reseller channel is a second counterparty

Six records here are sold through StackSocial rather than the vendor. The distinction matters
because a licence bought through a reseller is governed by two sets of published conditions and the vendor can
decline to honour a resold licence.

The Drime and Internxt entries are the same products as the direct listings and their prices are
lower. That is the whole value and it is a real one. What it is not is a different product, so
the record's `provenance` carries both listings and the document says the channel once.

### Icedrive, lifetime plans (direct)

> Lifetime Personal 500 GB $229 (from $344); Lifetime Personal+ 2 TB $499 (from $749). One-time, 'No recurring renewal'. Live on the vendor page 2026-10-21

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Gibraltar-registered ICE PRIVACY LTD, 30-day guarantee on the lifetime page but 14 days in the published conditions, decide inside 14. Read path (recorded as metered): Not metered on the plan page; 'Larger public transfers' is listed as a paid-tier feature without a published cap. (`reported`, 2026-10-21).

Evidence: `https://icedrive.net/lifetime-plans` (2026-10-21), record `dossier/storage/icedrive-lifetime-plans.json`.
Verdict: `fails-egress`.

### Internxt, 100 TB lifetime via StackSocial

> 100 TB lifetime, $974.97 (suggested $9,900, 90% off) on StackSocial. Vendor's own direct tiers are 1 TB / 2 TB / 5 TB / 10 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Post-quantum E2E encryption means a lost password is unrecoverable. Read path (recorded as not metered): No published egress cap found on any pricing page. Vendor FAQ silent on bandwidth. Absence of a clause is not a guarantee. (`reported`, 2026-10-21).

Evidence: `https://internxt.com/lifetime` (2026-10-21), record `dossier/storage/internxt-100-tb-lifetime-via-stacksocial.json`.
Verdict: `fails-quota`.

### pCloud, lifetime plans (direct)

> 500 GB $219, 2 TB $499, 10 TB $1,499 one-time. Live as of 2026-10-17 per price audit; AppSumo listing sold out

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Longest-running lifetime seller (since 2013), 14-day refund, short window, upload real data inside week one. Read path (recorded as metered): 'Upload files of any size with unrestricted transfer speeds' , no egress meter quoted on pricing page. (`reported`, 2026-10-21).

Evidence: `https://www.pcloud.com/cloud-storage-pricing-plans.html` (2026-10-21), record `dossier/storage/pcloud-lifetime-plans.json`.
Verdict: `fails-quota`.

### Drime Secure Cloud Storage 10 TB lifetime (StackSocial)

> StackSocial lifetime SKUs: 2 TB $149.97 - 6 TB $249.97 - 8 TB $279.97 - 10 TB $359.97. Subscription ladder on drime.cloud: 500 GB EUR 2.39/mo -> 2 TB EUR 4.40 -> 3 TB EUR 8.79 -> 6 TB EUR 15.99 (all billed annually)

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: European hosting, 20 GB free tier, file history 30-120 days by tier. Read path (recorded as not metered): Drime is rclone-native and the cheapest real paid option, so treat egress as the unverified term in this entry. (`reported`, 2026-10-21).

Evidence: `https://www.stacksocial.com/sales/drime-secure-cloud-storage-lifetime-subscription-advanced-plan-10tb` (2026-10-21), record `dossier/storage/drime-secure-cloud-storage-10-tb-lifetime.json`.
Verdict: `qualifies-with-caveat`.

### Hetzner Storage Box BX41 (20 TB)

> 20 TB (BX11 1 TB / BX21 5 TB / BX31 10 TB / BX41 20 TB)

That is the record's own wording (`documented`, 2026-10-22). A new account costs card. Observed behaviour: Hetzner DE/FI. Read path (recorded as not metered): VERBATIM: "Traffic: Unlimited *" on every tier, and "Each Storage Box comes with unlimited traffic" (docs). (`documented`, 2026-10-22).

Evidence: `https://www.hetzner.com/storage/storage-box/` (2026-10-22), record `dossier/storage/hetzner-storage-box-bx41.json`.
Verdict: `qualifies`.

### HostBrr StorageBox 16 TB (BFBOX recurring coupon)

> 500 GB / 1 / 2 / 4 / 8 / 16 TB, US (Utah) and DE (Falkenstein). 16 TB = $35.50/mo or $355/yr. 8 TB = $18.50/mo or $185/yr. 4 TB = $9.50/mo or $95/yr

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Real hosting business (labze), 2+ years on LET with a Patron Provider tag. Read path (recorded as not metered): VERBATIM: bandwidth is quoted as a hard multiple of storage , "5 TB Bandwidth @ 10 Gbps" on 1 TB, "40 TB" on 8 TB, "80 TB" on 16 TB. (`reported`, 2026-10-21).

Evidence: `https://my.hostbrr.com/order/main/packages/storagebox/?group_id=65` (2026-10-21), record `dossier/storage/hostbrr-storagebox-16-tb.json`.
Verdict: `qualifies-with-caveat`.

### NetDynamics24 Germany Backup SFTP (LET50% recurring)

> 250 GB $3/mo - 500 GB $4/mo - 1 TB $6/mo - 2 TB $11/mo. Germany (Falkenstein) and Finland (Helsinki) sold as separate product groups

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Small host (NetDynamics LLC), advertises 256 GB RAM Xeon E5-1650v3 storage nodes with RAID-6 and unmetered 1 Gbit/s.

Evidence: `https://www.netdynamics24.com/client/order.php?step=1&productGroup=13` (2026-10-21), record `dossier/storage/netdynamics24-germany-backup-sftp.json`.
Verdict: `qualifies-with-caveat`.

### PulsedMedia M10G Storage Box (16 TB)

> 16 TB HDD RAID5 (4/8/16/32 TB tiers)

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-ip-shaping`: 100 Mbps sustained egress. A new account costs email. Observed behaviour: Own DC in Finland, 15+ yrs operating.

Evidence: `https://pulsedmedia.com/storage-boxes.php` (2026-10-22, HTTP 200, 7,273 bytes), record `dossier/storage/pulsedmedia-m10g-storage-box.json`.
Verdict: `qualifies`.

⚠ **This plan carries two records and one is a duplicate.** `pulsedmedia-m10g-storage-box.json`
is the canonical one, `documented` from the page read on 2026-10-22. The older
`pulsedmedia-m10g-storage-box-16tb.json` is `reported` at the same URL and the same numbers, and it
carries `extras.duplicate_of` pointing at the canonical record. A reader who finds the second file
should follow this one: same product, stronger rung. The duplication is not a second offer.

### ServaRICA Polar Bear / Killer Whale / Mammoth storage

> Opossum 1 1 TB $29/yr - Polar Bear 2 TB $5/mo or $48/yr - Killer Whale 3.5 TB $8.50/mo or $84/yr - Mammoth 8 TB $20/mo or $220/yr

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Canadian provider since 2010, RAIDZ2. Read path (recorded as not metered): Quoted as a hard monthly transfer figure per plan: 4 TB / 12 TB / 18 TB / 24 TB on a 1 Gbps port. (`reported`, 2026-10-21).

Evidence: `https://servarica.com/storage-servers-2/` (2026-10-21), record `dossier/storage/servarica-polar-bear-killer-whale-mammoth-storage.json`.
Verdict: `qualifies-with-caveat`.

### Uloz.to Disk (ULTRA 25 TB)

> PREMIUM 3 TB $6.50/mo - MAX 12 TB $16/mo - ULTRA 25 TB $32/mo - ULTIMATE 50 TB $64/mo

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: MAX 12 TB. A new account costs email. Observed behaviour: Czech provider (Uloz.to/Kramerius) that pivoted from a public file locker to a paid private drive after EU DSM pressure in 2023-24. Read path (recorded as not metered): VERBATIM per-tier transfer allowance: PREMIUM "30 TB for data transfer/month", MAX "150 TB", ULTRA "300 TB", ULTIMATE "600 TB". (`reported`, 2026-10-21).

Evidence: `https://uloz.to/koupit-disk` (2026-10-21), record `dossier/storage/uloz-to-disk.json`.
Verdict: `fails-quota`.

### Drime (Advanced / 10 TB lifetime)

> Subscription: Starter 500 GB, Essentials 2 TB, Professional 3 TB, Advanced 6 TB. Lifetime via StackSocial: 2 TB $149.97, 3 TB $199.97, 10 TB $359.97. Direct partner landing shows 10 TB lifetime at $249 promo against a $360 base

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Founded 2024 per third-party review, shortest track record of any vendor here. Read path (recorded as metered): Subscription page lists 'Unlimited Bandwidth' as a feature of every paid tier. No metered-egress clause found on the pricing page. (`reported`, 2026-10-21).

Evidence: `https://drime.cloud/pricing` (2026-10-21), record `dossier/storage/drime.json`.
Verdict: `qualifies-with-caveat`.

### Filen Pro X (10 TiB)

> Pro I 200 GiB / Pro II 500 GiB / Pro III 2 TiB / Pro X 10 TiB. 'Plans stack on a single account. Combine two Pro X plans for 20 TiB on one Filen account, with no upper limit.'

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Filen withholds quota behind VPN IPs. Read path (recorded as not metered): Verbatim on every tier: 'Unlimited bandwidth' and 'Unlimited uploads' (`reported`, 2026-10-21).

Evidence: `https://filen.io/pricing` (2026-10-21), record `dossier/storage/filen-pro-x.json`.
Verdict: `qualifies`.

### Icedrive Lifetime Personal+ 2 TB

> Lifetime Personal 500 GB $229 (list $344); Lifetime Personal+ 2 TB $499 (list $749). Growth is by 'stack' add-ons (1 TB / 5 TB) or by attaching a subscription

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: No mass data-loss event documented. Read path (recorded as metered): Not metered on the plan page; 'Larger public transfers' is listed as a paid-tier feature without a published cap. (`reported`, 2026-10-21).

Evidence: `https://icedrive.net/lifetime-plans` (2026-10-21), record `dossier/storage/icedrive-lifetime-personal-2-tb.json`.
Verdict: `qualifies-with-caveat`.

### Internxt lifetime (via StackSocial)

> 1 TB / 2 TB / 5 TB on internxt.com; StackSocial carries 5 TB $229.99, 10 TB $269.97-$359.99, 100 TB $999.99. Vendor states plans are stackable: 'you can add up to 100 TB of storage to your Internxt lifetime membership'

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: (CLI bridge) + request-rate. A new account costs card. Observed behaviour: Documented file-loss pattern, not a single incident: a GitHub controlled test uploaded 198 files and lost some. Read path (recorded as not metered): No published egress cap found on any pricing page. Vendor FAQ silent on bandwidth. Absence of a clause is not a guarantee. (`reported`, 2026-10-21).

Evidence: `https://www.stacksocial.com/sales/internxt-cloud-storage-lifetime-subscription-10tb-plan` (2026-10-21), record `dossier/storage/internxt-lifetime.json`.
Verdict: `qualifies-with-caveat`.

### Jottacloud Pro 20 TB

> 10 / 20 / 30 / 50 TB fixed tiers, 1 user each

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Same operator as Unlimited but no retroactive-throttle exposure, since speed is contractual. Read path (recorded as not metered): No egress fee, 'Maximum speed' on both directions , explicitly no bandwidth limitation, unlike the Unlimited tier (`reported`, 2026-10-21).

Evidence: `https://jottacloud.com/en/why-jottacloud/jottacloud-pro` (2026-10-21), record `dossier/storage/jottacloud-pro-20-tb.json`.
Verdict: `qualifies`.

### Jottacloud Unlimited (Personal)

> Unlimited storage; 1 user. Free 5 GB tier exists

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: upload side only. A new account costs email. Observed behaviour: No documented mass data-loss event. Read path (recorded as not metered): No egress fee and no download throttle. Download speed and other use of the service is not changed, and you can still store as much data as you need in your account.' Upload is throttled once >5 TB stored: 'If you store more than 5 TB of data on Jottacloud, your upload speed is automatically reduced. (`reported`, 2026-10-21).

Evidence: `https://jottacloud.com/en/pricing/` (2026-10-21), record `dossier/storage/jottacloud-unlimited.json`.
Verdict: `qualifies-with-caveat`.

### Koofr (Suitcase XL+ 500 GB / 5 TB 5XXL)

> Briefcase 10/25/100 GB at EUR 0.5/1/2 per mo; Suitcase 250 GB EUR 4, 500 GB EUR 7, 1 TB EUR 10; Crate 2.5 TB EUR 20, 5 TB EUR 35; 10 TB+ on request

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: on public links, daily granularity Briefcase 10/25/100 GB at EUR 0. A new account costs email. Observed behaviour: Operated since 2012, Slovenian/EU. Read path (recorded as metered): Metered by tier on PUBLIC transfers only, daily: '200 GB daily public transfer limit' (Briefcase), '1 TB daily public transfer limit' (Suitcase XL/XL+/XXL), '4 TB daily public transfer limit' (Crate). (`reported`, 2026-10-21).

Evidence: `https://koofr.eu/pricing/` (2026-10-21), record `dossier/storage/koofr.json`.
Verdict: `fails-quota`.

### MEGA S4 (object storage)

> No upper limit. Base 3 TB included from EUR 15/mo; EUR 3.50 per additional TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: MEGA has run since 2013. Read path (recorded as not metered): Verbatim: '5x free egress, no API charges and no minimum storage period.' Vendor clarifies elsewhere: 'MEGA S4 allows up to 5x of the average monthly stored data as free egress.' At 20 TB stored that is ~100 TB/mo of free egress , covers a 1 TB/day serving load 3x over. (`reported`, 2026-10-21).

Evidence: `https://mega.io/objectstorage` (2026-10-21), record `dossier/storage/mega-s4.json`.
Verdict: `qualifies`.

### pCloud Premium Plus 2 TB / Ultra 10 TB (lifetime)

> 500 GB $219; 2 TB $499 (list $709); 10 TB $1,499 (list $2,799). Sale ladders reach 2 TB $299 and 10 TB $890

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `pull-count`: ish only on public links. A new account costs card. Observed behaviour: Operates since 2013, Swiss entity. Read path (recorded as metered): SHARED-LINK TRAFFIC IS METERED. Verbatim from pCloud's own blog (Sep 2026): 'Each pCloud plan comes with a predetermined amount of link traffic each month. (`reported`, 2026-10-21).

Evidence: `https://landing.pcloud.com/lifetime-cloud-storage` (2026-10-21), record `dossier/storage/pcloud-premium-plus-2-tb-ultra-10-tb.json`.
Verdict: `qualifies-with-caveat`.

### Synology C2 Object Storage

> Sold in whole-TB increments from 1 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Claims 99.999999999% durability, EU and US data centres. Read path (recorded as not metered): Verbatim: 'Free data retrieval , Retrieve all the data you have stored for free every month.' Plus 'No API request or data deletion fees'. (`reported`, 2026-10-21).

Evidence: `https://c2.synology.com/en-us/object-storage/overview` (2026-10-21), record `dossier/storage/synology-c2-object-storage.json`.
Verdict: `qualifies-with-caveat`.

### Zoolz Cloud Backup 12 TB

> 2.5 TB (2 TB cold + 500 GB hot) $79.99/yr; 7 TB (6+1) $239.99/yr; 12 TB (10 cold + 2 hot) $399.99/yr

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `write-gated`: cold storage means the restore is a request workflow. A new account costs card. Observed behaviour: Same corporate family as Polarbackup, which revoked paid lifetime deals outright. Read path (recorded as not metered): Not published as a fee; cold-tier retrieval is the practical cost and is not quantified on the pricing page (`reported`, 2026-10-21).

Evidence: `https://zoolz.com/pricing/` (2026-10-21), record `dossier/storage/zoolz-cloud-backup-12-tb.json`.
Verdict: `qualifies-with-caveat`.

### 1fichier Premium GOLD (10 TB cold storage)

> Unlimited hot storage; 10 TB cold storage included. Additional cold storage EUR 1/TB/month. File cap 300 GB, unlimited file count. Retention = whole subscription period on paid plans

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 300 GB/file. A new account costs email. Observed behaviour: Cold-storage overflow is destructive: forum reports say exceeding the cold quota earns a notice that the surplus is erased in 14 days and the account is blocked. Read path (recorded as metered): Verbatim, prices page: 'Premium ... Unlimited downloads, with no monthly allowance'. Unlimited downloads = no egress meter at all on the plan. (`documented`, 2026-10-22).

Evidence: `https://1fichier.com/tarifs.html?lg=en` (2026-10-21), record `dossier/storage/1fichier-premium-gold.json`.
Verdict: `qualifies-with-caveat`.

### Hetzner Storage Box BX21 (5 TB)

> 5 TB; 20 snapshots

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Same RAID-not-mirrored caveat. Read path (recorded as not metered): Unlimited (same table row as BX41) (`reported`, 2026-10-21).

Evidence: `https://www.hetzner.com/storage/storage-box/` (2026-10-21), record `dossier/storage/hetzner-storage-box-bx21.json`.
Verdict: `qualifies`.

### Icedrive 3 TB

> 3 TB; $9.99/mo or $119.88/yr

That is the record's own wording (`reported`, 2026-10-21). A new account costs card via stripe.... Observed behaviour: Twofish client-side encryption means every read costs local CPU. Read path (recorded as metered): Not metered on the plan page; 'Larger public transfers' is listed as a paid-tier feature without a published cap. (`reported`, 2026-10-21).

Evidence: `https://icedrive.net/plans` (2026-10-21), record `dossier/storage/icedrive-3-tb.json`.
Verdict: `qualifies-with-caveat`.

### InterServer Storage ST 600 (20 TB)

> 20 TB space, 20 TB transfer/month, 60 domains, DirectAdmin

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Transfer cap at 1:1 is the binding constraint, a 20 TB restore consumes the entire month's allowance.

Evidence: `https://www.interserver.net/storage/` (2026-10-21), record `dossier/storage/interserver-storage-st-600.json`.
Verdict: `qualifies-with-caveat`.

### pCloud Ultra 10 TB

> 10 TB storage; monthly $29.99 / annual $359.88

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: The 2x link-traffic rule is a genuine trap for serving: 10 TB stored -> 20 TB/mo shared-link traffic, i.e.

Evidence: `https://www.pcloud.com/cloud-storage-pricing-plans.html` (2026-10-21), record `dossier/storage/pcloud-ultra-10-tb.json`.
Verdict: `qualifies-with-caveat`.

### PrismDrive 10 TB annual

> 10 TB; $249/yr. Ladder: 2 TB $79/yr, 5 TB $149/yr, 10 TB $249/yr

That is the record's own wording (`inferred`, 2026-10-21). A new account costs card. Observed behaviour: This is the same lifetime-deal family pattern as PolarBackup ('a lifetime-deal cloud backup brand whose users report loss of data and service').

Evidence: `https://prismdrive.com/pricing/` (2026-10-21), record `dossier/storage/prismdrive-10-tb-annual.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Degoo, 20 GB free + referral ladder | fails-quota | 20 GB free, plus 5 GB referral bonus and 250 MB per referred friend. Paid: 500 GB $2.99/mo, 5000 GB Ultimate |
| FolderFort, free tier + 2.0 pricing | fails-egress | Free plan with encrypted storage, no card; '+25GB free' if the account posts a social-media review. Paid Personal from 100 GB... |
| pCloud PhotoDay2026 promo, 500 GB free for 3 months | trial-only | 500 GB free for 3 months, no card, via promo code `PhotoDay2026` on a fresh signup. Base free tier is 10 GB |
| Playbook, 100 GB free (300-asset cap) | fails-quota | Free: '100GB included' OR 300 total assets, whichever comes first. API 1K calls/month... |
| Internxt 100 TB lifetime (StackSocial) | fails-quota | StackSocial: 2 TB $129.99 - 5 TB $229.99 - 10 TB $359.99 - 50 TB $699.99 - 100 TB $999.99... |
| InterServer Storage Hosting ST 600 (20 TB) | fails-egress | 200 GB $3 - 1 TB $5 - 2 TB $8 - 4 TB $10 - 10 TB $25 - 20 TB $42, all per month |
| Scramble Cloud Premium 6 TB lifetime (StackSocial) | fails-quota | 2 TB EUR 129.95 once - 6 TB EUR 279.95 once (official site). StackSocial carries 2/6/12/20 TB SKUs at $59.95 / $139.95 /... |
| Storadera Space Premium | fails-egress | EUR 7.95 per TB per month, granular per-byte, no minimum. 50 GB free for 30 days |
| Degoo Ultimate 5 TB | fails-quota | Free 20 GB; Pro 500 GB; Ultimate 5 TB. Third-party trackers put Ultimate at $9.99/mo |
| MediaFire Pro 1 TB | fails-quota | Pro 1 TB; Ultra 100 GB (tier naming is inverted on the page) |
| file.kiwi Web Folder+ (prepaid Upload-GB) | fails-quota | Prepaid Upload-GB: 50 GB upload $1.20, 100 GB $1.60, 500 GB $3.99... |
| PikPak Global Premium (10 TB) | fails-egress | 10 TB storage on Premium; additional storage purchasable |
| UpZur Premium | fails-egress | 'Unlimited upload size, Unlimited storage space, Download volume Unlimited' on Premium. Registered free tier is 1,953 GB |

The rejections are the most valuable content in this document and they split three ways.

`paid` covers the vendors whose lifetime offer is real and whose product fails on egress: a
prepaid plan at a low storage rate with a metered read is the same trap as a monthly one.

`egress` covers the ones a buyer discovers after paying. pixeldrain's prepaid storage is genuinely
EUR 4 per TB per month and its filesystem downloads are charged at EUR 1 per TB with no free
allowance. That is a prepaid storage product with a metered read, and it is the cleanest example
of why the storage rate is not the price.

`trial-only` covers the offers that look like a free tier and are a clock.

And the one that is worse than dead is PolarBackup: in 2024 it permanently closed every lifetime
account and deleted the data. A dead service loses a route. A closed lifetime account loses the
bytes, which is a different failure and the reason this class is recorded as a bet.

## Chaining

A lifetime deal is a cold tier or a replica, never a serving tier, because its egress term is
unchanged by the prepayment and its capacity cannot grow.

The pairing that works is one lifetime archive plus one recurring hot box. The lifetime plan
carries the 20 TiB that is read rarely, and the recurring plan carries the working set with a
port that can be sized. That composition has the lowest five-year cost of anything in this
topic and it depends on the lifetime vendor surviving, which is the bet.
