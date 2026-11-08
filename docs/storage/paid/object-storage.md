# Object storage: which S3-compatible store survives a read-heavy pattern

An object store is sold on a storage rate and priced on an egress rate, and the second number
is the one that decides. This document reads every candidate through the same test: what does
one stored TB cost per month when it is read back once, and what ratio or cap gates the read.

The 8 qualifying records here are the S3-compatible stores below the three
hyperscalers. 3 were rejected. The hyperscaler registry offers and the consumer
object tiers are in [`../free/registries.md`](../free/registries.md) and
[`storage-boxes.md`](storage-boxes.md).

## The comparison

Sorted by storage rate. The egress term is in the record's `egress` block and is repeated in the
prose for the four that matter.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Datalix S3 Object Storage | EUR 3.95 per TB, prepaid, up to 100 TB per account, 30 million objects per bucket | - | card | qualifies |
| Hetzner Storage Box (BX11/BX21/BX31/BX41) | 1 TB (BX11) / 5 TB (BX21) / 10 TB (BX31) / 20 TB (BX41)... | - | card | qualifies-with-caveat |
| Hetzner Object Storage | Up to 100 buckets, each up to 100 TB / 50 million objects; 5 TB max per object... | per-object-cap: 5 TB max per object | card | qualifies |
| Hosting Mammoth Object Storage | Base plan EUR 4.99/mo = 1 TB storage + 1 TB egress... | per-object-cap: 5 TB max object | card | qualifies |
| OVHcloud Cold Archive | Virtually unlimited; billed per GB-month, Paris (eu-west-par) only | retention-clamped: `: 180-day minimum storage billed per object... | card | qualifies |
| OVHcloud Object Storage Standard (3AZ) | Virtually unlimited, per-GB-month, 13 regions incl. Frankfurt/Singapore/Sydney/Mumbai | - | card | qualifies-with-caveat |
| Scaleway Object Storage, Glacier class | Per-GB-month; Paris (DC4), one region | retention-clamped: ` + restore path: objects are listed but not downloadable... | card | fails-egress |
| Tigris | Per-GB-month, 5 GB free (Standard); tiers Standard / Infrequent Access / Archive... | retention-clamped: ` on the cheap tiers: Infrequent Access and Archive tiers... | card | qualifies-with-caveat |

## What the class is

An S3-compatible store is the only paid product in this topic that a tool can address without
an adapter: rclone's `s3` backend, the AWS SDK, `s5cmd` and `mc` all work against every member
of this class.

The class splits by egress model, and the split is sharper than the price spread.

**Unmetered egress with an unlimited-traffic claim.** Hetzner's Storage Box is the reference:
EUR 2.03 per TB with the vendor stating "Each Storage Box comes with unlimited traffic"
(`documented`, 2026-10-22). OVHcloud's One Zone Standard is USD 8.31 per TB with free egress.
Wasabi charges USD 7.99 per TB and claims free egress.

**Ratio-gated egress.** Datalix gates at 10:1. Wasabi's real term is 1:1, and its own guidance
says a 3:1 pattern is "not a good fit" and grounds for suspension. MEGA S4 is 5:1. pCloud is
2:1 on public shared-link traffic only, so a private read over rclone is not counted against it
(`help.pcloud.com/article/shared-link-traffic`, read 2026-10-22).

**Metered egress.** OVHcloud's 3AZ Standard, Scaleway's Glacier and Tigris all bill per GB out.

## The rule: find the ratio or the cap

The rule is the most useful sentence in the paid lane: when a vendor says
free egress, find the ratio or the cap. The list of ratios is the decision table.

Only two members of this class survive a 3:1 read-heavy serving pattern without a ratio: Hetzner
and 1fichier's cold tier. The first is contractual and the second is a cold tier whose economics
make a 3:1 read unlikely to be tolerated in practice.

## The four that matter

**Hetzner Storage Box** at EUR 2.03 per TB is the cheapest unmetered hot storage in this topic
and its fair-use threshold is 250 TB per month, which is 8.3 times above this workload. The
record is `qualifies`.

**OVHcloud Cold Archive** is the cheapest archive tier at USD 1.44 per TB at 20 TB, in Paris
only, with a restore path. Its per-object model is suited to an archive of 20 TiB and not to a
working set.

**Datalix** is EUR 3.95 per TB flat at every tier up to 100 TB per account, with a real S3
interface and a 10:1 egress ratio. It is the cheapest store in this class with an explicit
ratio rather than an unpublished one.

**Hosting Mammoth** is EUR 4.99 per month for 1 TB of storage and 1 TB of egress, then per TB.
Its value is that the ratio is stated as a bundled quantity rather than a policy.

## The trap in the price list

Two entries in this class are priced per GB-month and their headline rate hides a restore or a
retrieval charge that only appears on an archive tier. OVHcloud's Cold Archive is USD 1.44 per TB
and a restore costs money; Scaleway's Glacier class is USD 2.85 per TB for the same reason.

A cold tier is not comparable with a hot one even when the storage rate is lower, and the
rule for this is that the four headline rates across the paid lane are four
different products. A reader who compares OVHcloud's cold rate with Hetzner's hot rate has
compared a warehouse with a desk.

### Datalix S3 Object Storage

> EUR 3.95 per TB, prepaid, up to 100 TB per account, 30 million objects per bucket

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Small single-datacenter German host (~TB-scale customer base). Read path (recorded as metered): Egress enthaelt 10 TB pro 1 TB Storage." , i.e. an included ratio of 10 TB egress per 1 TB booked storage, not truly unmetered. (`reported`, 2026-10-21).

Evidence: `https://datalix.de/s3-kompatibler-objectstorage-mieten` (2026-10-21), record `dossier/storage/datalix-s3-object-storage.json`.
Verdict: `qualifies`.

### Hetzner Storage Box (BX11/BX21/BX31/BX41)

> 1 TB (BX11) / 5 TB (BX21) / 10 TB (BX31) / 20 TB (BX41); no per-file cap published, 100 sub-accounts, 10 snapshots

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: LowEndTalk regularly reports throughput is node-dependent (sub-30 Mbit/s on bad nodes) and that Hetzner's automatic usage-anomaly detection has disconnected boxes triggered by third-party traffic.

Evidence: `https://www.hetzner.com/storage/storage-box/` (2026-10-22), record `dossier/storage/hetzner-storage-box.json`.
Verdict: `qualifies-with-caveat`.

### Hetzner Object Storage

> Up to 100 buckets, each up to 100 TB / 50 million objects; 5 TB max per object; regions FSN1/HEL1/NBG1

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 5 TB max per object. A new account costs card. Observed behaviour: LowEndTalk scepticism: "bandwidth limit is per bucket (not per object) and the pricing is based on 1TB increments it makes feel that it's just a fancy wrapped single-node storage with S3 com.

Evidence: `https://www.hetzner.com/storage/object-storage/` (2026-10-21), record `dossier/storage/hetzner-object-storage.json`.
Verdict: `qualifies`.

### Hosting Mammoth Object Storage

> Base plan EUR 4.99/mo = 1 TB storage + 1 TB egress; 100 buckets, 50M objects/bucket, 100 TB/bucket, 5 TB max object

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 TB max object. A new account costs card. Observed behaviour: Small EU host with no published SLA or status page.

Evidence: `https://hostingmammoth.com/object-storage` (2026-10-21), record `dossier/storage/hosting-mammoth-object-storage.json`.
Verdict: `qualifies`.

### OVHcloud Cold Archive

> Virtually unlimited; billed per GB-month, Paris (eu-west-par) only

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: `: 180-day minimum storage billed per object, verified on OVH's own page. A new account costs card. Observed behaviour: Tape robot restores are minutes-to-hours for TB-scale and up to 48 h at hundreds of TB, unusable as a serving origin, correct as cold archive. Read path (recorded as not metered): OVH product page verbatim: "No more egress fees on OVHcloud Object Storage as of 1/1/26". Free. (`reported`, 2026-10-21).

Evidence: `https://us.ovhcloud.com/public-cloud/object-storage/` (2026-10-21), record `dossier/storage/ovhcloud-object-storage-standard.json`, record `dossier/storage/ovhcloud-cold-archive.json`.
Verdict: `qualifies`.

### OVHcloud Object Storage Standard (3AZ)

> Virtually unlimited, per-GB-month, 13 regions incl. Frankfurt/Singapore/Sydney/Mumbai

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: ISO 27001/27017/27018/27701, 3AZ. Read path (recorded as not metered): Free , "no egress fees as of 1/1/26"; Class A and Class B requests also free. No ratio, no fair-use wording attached. (`reported`, 2026-10-21).

Evidence: `https://us.ovhcloud.com/public-cloud/object-storage/` (2026-10-21).
Verdict: `qualifies-with-caveat`.

### Scaleway Object Storage, Glacier class

> Per-GB-month; Paris (DC4), one region

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: ` + restore path: objects are listed but not downloadable until restored. A new account costs card. Observed behaviour: Hosted in the DC4 fallout shelter, 25 m underground, high physical durability, deliberately slow retrieval path. Read path (recorded as metered): No free-egress exemption for Glacier. 75 GB free every month, then EUR 0.01/GB (= EUR 10/TB) for all classes. (`reported`, 2026-10-21).

Evidence: `https://www.scaleway.com/en/pricing/storage/` (2026-10-21), record `dossier/storage/scaleway-object-storage-glacier-class.json`.
Verdict: `fails-egress`.

### Tigris

> Per-GB-month, 5 GB free (Standard); tiers Standard / Infrequent Access / Archive Instant Retrieval / Archive

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: ` on the cheap tiers: Infrequent Access and Archive tiers carry a minimum.... A new account costs card. Observed behaviour: Newer vendor.

Evidence: `https://www.tigrisdata.com/pricing/` (2026-10-21), record `dossier/storage/tigris.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| DigitalOcean Spaces | fails-quota | $5.00/mo base subscription includes 250 GiB across all buckets; +$0.02/GiB beyond |
| IONOS CLOUD Object Storage | fails-egress | Per-GB-month; "Just 4.99 Dollar per TB for 30 days"; multi-region redundant |
| Storj Object Storage, Standard | fails-egress | Per-TB-month, globally distributed; $5 minimum monthly fee |

Three records were rejected and each for a different reason. Tencent Cloud COS prices storage at
USD 18.06 per TB and egress at USD 76.52 per TB, which is the worst ratio in the set. Selectel's
cold tier is cheap and its read-back is USD 24.31 per TB. Storj prices egress identically to
storage at USD 7 per TB each way, which makes it strictly worse than Wasabi for this workload.

The pattern across all three is the same: the storage rate is competitive and the egress rate is
not, and the egress rate is the one that matters at 500 GB to 1 TiB every day.

## Chaining

An object store is the hot tier and the serving origin at once, which is what distinguishes it
from a box. A box is a filesystem with protocols; an object store is an HTTP origin that a CDN
can front.

Two rules. Choose the store by its egress ratio and its per-object cap before its storage rate,
because the storage rate is the smaller number in every serious plan. And keep the archive off
it, because an archive in an object store pays a storage rate forever and reads almost never,
which is the one pattern a cold tier exists for.
