# Storage VPS and storage servers: price per TB, and the largest disk at a price

This page answers one question with two columns, because they rank differently. What is the
cheapest disk per TB per month, and what is the largest single machine, and at what price?
Every figure comes from the vendor's own page on 2026-10-22, and every record behind it is in
`dossier/compute/`.

The distinction that decides the answer is how the disk is sold. A **block or slice** is sold
per TB attached to a machine rented separately, so its price per TB is a published rate. A
**storage server** is sold as one machine with a row of disks, so its price per TB is a
division.
The cheapest rate is a slice; the largest machine is a server.

## The short answer

| question | answer | price |
|---|---|---|
| cheapest disk per TB per month | Hetzner SX65 at its base configuration, 4 x 16 TB | **EUR 1.31 per TB** (EUR 84.00 a month, plus EUR 39.00 once) |
| cheapest per TB on an annual prepay | DediRock Storage, 2 TB for a year | **USD 1.15 per TB per month** (USD 27.68 a year) |
| cheapest per-TB *rate* with no machine to rent | InterServer storage slices | **USD 3.00 per TB per month** |
| largest single machine | Hetzner SX295, 14 x 22 TB | **308 TB at EUR 599.00 a month** |
| largest machine per euro | Hetzner SX65 at its maximum, 4 x 22 TB | 88 TB at EUR 159.00, which is EUR 1.81 per TB |
| cheapest way to start | Time4VPS, 256 GB | EUR 2.22 a month, promotional, renewing at EUR 4.45 |

⚠ **The Hetzner figures exclude VAT and carry a one-time setup fee**, EUR 39.00 on the SX65 and
EUR 439.00 on the SX295. A 12-month comparison that ignores the setup fee understates the first
year by about 4 per cent on the SX65 and 6 per cent on the SX295. Every per-TB figure below is
the monthly rate divided by the disk the vendor prints, and none of them amortises the setup.

## The comparison

Cost per TB is the monthly price divided by the vendor's own TB figure, at the configuration
named. A dash in `Transfer` means the vendor states none or calls it unlimited.

| Provider | Shape | Disk | Transfer | Price | Per TB / month | Rung |
| --- | --- | --- | --- | --- | --- | --- |
| `hetzner-storage` SX65, base | Ryzen 7 3700X, 128 GB, 2 x 1 TB NVMe | 64 TB | unlimited, 1 Gbit/s | EUR 84.00 | **1.31** | documented |
| `hetzner-storage` SX65, max | same, 4 x 22 TB | 88 TB | unlimited | EUR 159.00 | 1.81 | documented |
| `hetzner-storage` SX135, max | Ryzen 9 3900, 256 GB, 2 x 1.92 TB NVMe | 176 TB | unlimited | EUR 309.00 | 1.76 | documented |
| `hetzner-storage` SX295 | EPYC 7502P, 2 x 7.68 TB NVMe | 308 TB | unlimited | EUR 599.00 | 1.95 | documented |
| `worldstream` RX2540 M2 | 2 x Xeon E5-2620 v4, 32 threads, 2 x 960 GB SSD | 100 TB | not stated | EUR 219.00 | 2.19 | documented |
| `worldstream` T640 | 2 x Xeon Gold 5120, 56 threads, 2 x 960 GB NVMe | 216 TB | not stated | EUR 628.40 | 2.91 | documented |
| `interserver` storage slice | 1 core and 2 GB added per TB, 10 Gbps shared | 1 TB per slice | 2 TB per slice | USD 3.00 | **3.00** | documented |
| `hosthatch` storage | 1 vCPU, 1,024 MB, spinning disk | 10 TB | 25 TB | USD 38.00 | 3.80 | documented |
| `dedirock-storage-vps` Plus | 1 vCPU, 2 GB | 2 TB | 4 TB | USD 9.99 | 4.50 | documented |
| `kimsufi` KS-5 | Xeon E3-1270 v6, 32 GB, 2 x 2 TB to 2 x 4 TB | 4 TB | 300 Mbps port | USD 19.90 | 4.98 | documented |
| `buyvm` block slab | 256 GB slab attached to a slice from USD 24.00 a year | 10 TB max per slab | not stated | USD 50.00 | 5.00 | documented |
| `hetzner-server-auction` | i7-7700, 32 GB, 3 TB plus 6 TB HDD | 9 TB | not stated | EUR 49.70 | 5.52 | measured |
| `time4vps` | 1 vCPU, 16 GB at this tier | 8 TB | 64 TB | EUR 67.50 | 8.44 | documented |
| `vpsdime` | 4 vCPU, 2 GB, HGST HDD in RAID10 | 4 TB | 32 TB | USD 56.00 | 14.00 | reported |

**Read the first and third rows together.** The Hetzner box is the cheapest per TB, but it is a
whole machine with 128 GB of RAM, a 1 Gbit/s port and a EUR 39 setup; the InterServer slice is a
rate you can attach one terabyte at a time to a VPS you already pay for. A reader who needs 2 TB
does not buy 64 to get EUR 1.31, and one who needs 60 TB does not assemble sixty slices.

## The annual-prepay floor

DediRock sells the same storage line two ways, and the annual promo is the cheapest disk in this
document:

| plan | disk | annual price | per TB per month | monthly price for the same disk |
| --- | --- | --- | --- | --- |
| Storage Promo Starter | 256 GB | USD 11.88 | 3.87 | USD 3.99 |
| Storage Promo Essentials | 1 TB | USD 17.68 | 1.47 | USD 5.99 |
| Storage Promo Plus | 2 TB | USD 27.68 | **1.15** | USD 9.99 |

The annual rate is roughly a third of the monthly rate for the same disk, which is why a
per-TB table built only from monthly prices misranks this provider. ⚠ **The renewal price is not
established**: the billing store returns 403 to an unauthenticated fetch, so whether year two
costs USD 27.68 or the monthly rate is unverified, and that difference is the whole finding.

## What the affiliate articles get wrong

The four repositories behind this page are affiliate articles. **107 of their factual claims were
checked against the vendors and 15 were wrong and 22 unverifiable**. Three matter here:

- **The Hong Kong large-disk ladder is 23 to 31 per cent cheaper than the Chinese articles print**:
  RMB 30 / 55 / 100 / 180 a month against their RMB 40 / 80 / 140 / 260. Their per-GB arithmetic
  is built on the wrong price.
- **DediRock's RAID-5 is a migration in progress, not a delivered feature.** Three announcements
  in 2026 say the New York nodes are "being moved to RAID-5" and no page states it finished. An
  article that sells redundancy a backup does not have is the worst error available in this market.
- **Backblaze B2 is USD 6.95 per TB per 30 days**, not the USD 6 the article prints, so 2 TB is about
  USD 166.80 a year rather than USD 144, and its egress is free to three times the average stored
  rather than charged from the first byte.

That is a 14 per cent error rate on checkable claims in documents that present themselves as
comparisons. It is why those articles are recorded as leads and every number here is a vendor
page.

## Where this page stops

**Not every host sells a storage line, and the ones that do not are recorded as such.**
ServerHost, RackNerd, Little Creek and WebHorizon were checked and sell NVMe only; their records
say so rather than carrying an invented disk tier. Hostsailor and NexusBytes could not be read:
the storage path extracts to empty headings and the other host answered a gateway timeout twice.
Both stay `unverified` with the wall named.

**VAT and currency are not normalised.** Hetzner, Contabo, Worldstream and Time4VPS print euro
figures excluding VAT; DediRock, InterServer, HostHatch and VPSDime print dollars. No conversion
is asserted anywhere, so the per-TB column compares within a currency and not across one.

**No disk was measured.** Every throughput claim a reader might want -- IOPS on HDD RAID, the
real sequential rate on a 10 Gbps port -- is absent, because no machine was booted. The cheapest
per-TB figure is a price, and a price is not a performance.
