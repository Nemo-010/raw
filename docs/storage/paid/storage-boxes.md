# Storage boxes: which box is cheapest per usable TB, and what its port caps

The paid lane is a different argument from the free lane. Free storage is bounded by retention
and identity; paid storage is bounded by the egress ratio. A box that sells 20 TB with unlimited
traffic and a box that sells 20 TB with a metered read are not the same product at the same
price, and the gap between them is the whole economics of this class.

This document covers 31 qualifying records: European storage servers and dedicated
machines, seedbox and backup hosts, and the US and Asia storage VPS market. 5 were
rejected. The S3-compatible object stores are in [`object-storage.md`](object-storage.md), the
lifetime and discount offers in [`lifetime-and-deals.md`](lifetime-and-deals.md), and the
regional market in [`regional.md`](regional.md).

## The comparison

Sorted by all-in cost per usable TB per month. A price in EUR is the vendor's currency; the USD
column in the record converts at a recorded rate and the date is in the record's `price.notes`.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Contabo Object Storage (S3-compatible) | 250 GB increments, up to 25 TB, 5 TB max object size | per-object-cap: 5 TB max object | card | qualifies-with-caveat |
| Datalix S3-compatible Object Storage (Frankfurt) | 1 TB, 100 TB per account, 30 M objects per bucket | - | email | qualifies |
| Hetzner Storage Box BX11 / BX21 / BX31 (1/5/10 TB) | 1 TB / 5 TB / 10 TB | - | email | qualifies |
| Hetzner SX135-2 dedicated storage server | 8x 16 TB SATA = 128 TB raw; 112 TB usable at RAID-6 | - | email | qualifies-with-caveat |
| Hetzner SX65-2 dedicated storage server | 4x 16 TB SATA = 64 TB raw; 48 TB usable at RAID-5... | - | email | qualifies |
| HostBrr StorageBox (Germany / USA) | 500 GB, 16 TB | - | email | fails-quota |
| InterServer Storage VPS (1 TB slices) | 1 TB per slice, 1, 20+ slices stacked | per-ip-shaping: 10 Gbps shared port | card | qualifies-with-caveat |
| Kimsufi KS-5 (OVH budget brand) | 2x 2 TB, 2x 4 TB HDD (configured up to 3x 4 TB) | per-ip-shaping: 300 Mbps public port caps near ~97 | card | qualifies-with-caveat |
| OVHcloud Object Storage, One Zone Standard | unlimited, per GiB | - | card | qualifies-with-caveat |
| STRATO HiDrive Business | 1 / 3 / 5 / 10 TB | - | card | qualifies-with-caveat |
| Wasabi Hot Cloud Storage | Pay-as-you-go, billed per-GB/day; Reserved Capacity from 25 TB | retention-clamped: ` 90-day minimum storage duration on pay-as-you-go... | card | qualifies-with-caveat |
| Webtropia Storage Server RYZ5-20 (4x 22 TB) | 4x 22 TB = 88 TB raw (RYZ5-12: 4x 14 TB = 56 TB, EUR 79.99) | - | email | qualifies-with-caveat |
| BorgBase, Medium / Large | 10 GB free forever; Small 250 GB, Medium 1 TB, Large 2 TB; flexible quota up to 3x plan | - | email | fails-quota |
| Feral Hosting, Radon (8 TB) | 1 / 1.5 / 2 / 3 / 4.5 / 8 TB HDD; SSD line 150 GB-1.6 TB | - | email | qualifies-with-caveat |
| HostBrr, StorageBox 16TB | 16 TB on NVMe-cached HDD RAID-60 (500 GB / 1 / 2 / 4 / 8 / 16 TB) | per-ip-shaping: 100 MB/s I/O ceiling reported by buyer | email | qualifies-with-caveat |
| Hosting by Design, App hosting 24 TB... | 1 / 2 / 4 / 8 TB shared; 18 / 24 / 28 TB dedicated disk | - | email | qualifies |
| PulsedMedia, M10G Storage Box 16TB | 16 TB HDD RAID5 (4/8/16/32 TB tiers) | per-ip-shaping: 100 Mbps sustained egress | email | qualifies |
| rsync.net, Standard (ZFS, SSH-only filesystem) | 800 GB minimum order; 0-9 TB, 10-99 TB, 100+ TB bands | - | card | qualifies-with-caveat |
| SeedHost.eu, HD 24 | 1 / 2 / 3 / 4 / 5 / 7 / 9 / 12 / 15 / 18 / 24 TB HDD | - | email | qualifies-with-caveat |
| Ultra.cc, Platinum 28 TB | 1 / 2 / 4 / 6 / 8 / 12 / 16 / 22 / 28 TB HDD | - | email | qualifies-with-caveat |
| Whatbox, H3-22 | 3.9 / 5.9 / 9.9 / 15.8 / 21.7 TB HDD | per-ip-shaping: 100 Mbps throttle, not a bill 3 | email | qualifies-with-caveat |
| Advin Servers KVM Storage VPS | Kansas City: Storage 1 2,560 GB / Storage 2 5,120 GB / Storage 3 10,240 GB / Storage 4... | per-ip-shaping: 10 Gbps | card | qualifies-with-caveat |
| AlphaVPS Storage VPS | 256 GB / 512 GB / 1 TB / 2 TB / 3 TB / 4 TB / 8 TB / 16 TB... | - | card | qualifies |
| BuyVM Block Storage Slabs | Sold in 256 GB chunks at $1.25/month. 1 TB = $5.00/mo. 10 TB = $50.00/mo... | per-object-cap: Max 10 TB | card | fails-quota |
| DeluxHost Storage VPS | STORAGE-1 500 GB / -2 1 TB / -3 2 TB / -4 3 TB / -5 4 TB / -6 5 TB / -10 20 TB... | - | card | qualifies |
| GreenCloudVPS Storage KVM | US/EU: Storage-0.5TB 500 GB, Storage-1 1 TB, Storage-2 2 TB (SATA RAID-10... | per-ip-shaping: 10 Gbps port) | card | qualifies |
| HostBrr storage VPS + HDD block | Premium StorageBrr 1/2/4/6/8 GB RAM with 500 GB HDD block included... | - | card | qualifies |
| HostHatch Storage VM | 1 / 2 / 3 / 4 / 5 / 6 / 8 / 10 TB HDD, 'enterprise-grade spinning hard disk drives'... | - | card | qualifies-with-caveat |
| Kyun.host Bricks (HDD block) | HDD block volumes attached to a Danbo VM... | - | email | qualifies-with-caveat |
| NovaCloud-Hosting Storage VPS | Storage Stellar 2 TB, Storage Cosmic 6 TB... | - | card | qualifies-with-caveat |
| ServaRica storage VPS | Opossum 1 1 TB, Opossum 2 1 TB, Polar Bear 2 TB, Killer Whale 3.5 TB, Horse 3 TB... | - | card | qualifies-with-caveat |

## What the class is

Three products share this document and they differ in what the buyer is buying.

**A storage box** is a managed filesystem with protocol access: SFTP, SCP, rsync, WebDAV, Samba
and Borg. Hetzner's BX line, PulsedMedia's M-series and HostBrr's StorageBox are members.

**A dedicated storage server** is a machine with many disks. Hetzner's SX line and Webtropia's
RYZ line are members, and their per-TB price is the lowest in the class because the buyer
carries the operational burden.

**A storage VPS** is a virtual machine with a large disk and a shared port. AlphaVPS, BuyVM,
DeluxHost, GreenCloudVPS, HostHatch, InterServer and ServaRica are members, and their constraint
is the port rather than the disk.

## The port is the limit, not the quota

This is the arithmetic that changes which box to buy.

PulsedMedia's own plan table reads "Internet egress: Unlimited@100Mbps (~30TB/Month / ~1TB/Day)",
and the string appears four times on the page (`documented`, 2026-10-22: 200, 7,273 B, with the
EUR 26.99 price for the 16 TB tier). Run it:

| quantity | value |
|---|---|
| 100 Mbps sustained for 24 hours | 1.08 TB, which is 0.982 TiB |
| 1 TiB per day requires | 101.8 Mbps |
| so 1 TiB per day is | 101.8% of the port |
| 1 TiB per day against the 30 TB monthly allowance | 110%, so the allowance is also exceeded |

The port is the limit and it is within 2% of the workload at the top of the range. The vendor's
"~1TB/Day" is 30 TB divided by 30 days, which is arithmetic rather than a measured rate, and the
TB there is decimal. Read the other way, 30 TB per month is 0.91 TiB per day, which would bind
*before* the port's 0.982 TiB per day and make the allowance the limit — but only if "~30TB/Month"
is a real allowance rather than a restatement of the port. The page does not say which, so the
record carries both readings and the decision below does not depend on it: at 1 TiB per day the
box fails either way. In practice the M10G port is shared between about a dozen users, so a
sustained 800 to 900 GB per day is the honest ceiling.

The consequence is that PulsedMedia at EUR 26.99 is the right buy at 500 GB per day and the
wrong one at 1 TiB per day, where Hetzner's BX41 at EUR 40.60 is the only one of the two that
fits. The topic README states this as the workload-conditional recommendation it is.

## Hetzner: two products, one machine, a 3.6x gap

Hetzner sells the same 20 TB twice and the difference is the egress term.

The Storage Box BX41 is EUR 40.60 per month for 20 TB, which is EUR 2.03 per TB, and the docs
page states "Each Storage Box comes with unlimited traffic"
(`documented`, 2026-10-22: the pricing page carries 3.20, 10.90, 20.80 and 40.60, and the docs
page carries the traffic sentence). The Object Storage is EUR 7.31 per TB and metered, which is
USD 8.21 per TB at 1.1234 USD/EUR. The euro figure is the one to compare: 20 TB stored and
20 TB read is EUR 6.49 base plus 19 TB of storage overage at EUR 0.0087 per TB-hour plus 19 TB
of egress at EUR 1.00, which is EUR 146.16, or EUR 7.31 per TB. `7.31 / 2.03 = 3.6`, and the
USD figure over the euro denominator gives 4.04 only because the two units are mixed.

The fair-use threshold is 250 TB per month. The
2022 traffic notice letter reads "your traffic use, which currently averages above 250 TB/month
on some of your servers... Although these servers include unlimited traffic, this is far above
what we consider fair use." At 30 TB per month the workload is 8.3 times below that threshold.

The dedicated line is cheaper per TB and carries the machine. SX65-2 gives 64 TB raw, 48 TB
usable at RAID-5, for EUR 82.30, which is EUR 1.29 per raw TB. SX135-2 gives 128 TB raw and 112
TB usable at RAID-6 for EUR 287.30, which is EUR 2.24 per raw TB. Both are `qualifies` and both
put the operational burden on the buyer.

The same 16 TB M10G plan holds a second record, `pulsedmedia-m10g-storage-box-16tb.json`, which is
the same product recorded twice. The vendor page publishes one product line with four tiers — 4, 8,
16 and 32 TB at EUR 8.99, 14.99, 26.99 and 63.99 — so there is no second 16 TB SKU. The
`pulsedmedia-m10g-storage-box` record is canonical; the second carries `extras.duplicate_of` pointing
at it and keeps its numbers, its rung and its evidence. A count
that treats qualifying records as distinct offers should exclude the duplicate.

## The price floor, and what it looks like

Five records sit at or below EUR 2.10 per TB per month and they are the floor of this class.

Webtropia's RYZ5-20 gives four 22 TB disks for EUR 109.99, which is EUR 1.25 per raw TB and the
lowest figure in this topic. Hosting by Design gives 24 TB for EUR 49.95, which is EUR 2.08.
HostBrr gives 16 TB for EUR 32.00, which is EUR 2.00. Hetzner's BX31 gives 10 TB for EUR 20.80,
which is EUR 2.08. InterServer gives 1 TB slices at USD 3.00 flat at every size.

The floor is real and it is not where the risk is. A dedicated machine at EUR 1.25 per TB has no
egress meter, no fair-use clause and no vendor who can change the product; what it has instead
is a disk that fails and a buyer who is the administrator.

## Seedbox hosts, and why they are a different buy

Seven records are seedbox hosts: Feral, SeedHost, Ultra.cc, Whatbox, rsync.net, BorgBase and
Hosting by Design. Their per-TB price runs from EUR 2.08 (Hosting by Design, 24 TB) and EUR 2.29
(SeedHost, 24 TB) up to GBP 7.50 (Feral, 8 TB) and USD 7.50 (BorgBase, 1 TB), and rsync.net sits
above all of them at USD 15.00 per TB in its first band. Measured against the EUR 1.69 managed
floor that is 1.2 to 8.9 times, and
against the USD 0.17 to 0.28 disk floor it is 7.6 to 90 times. They sell something else: a managed
application stack, a fast port, and in rsync.net's case a ZFS filesystem with snapshots over SSH
only.

The distinction matters because a seedbox's port is shared and its storage is
fast. Ultra.cc's Platinum gives 28 TB for EUR 79.95, which is EUR 2.86 per TB, and Whatbox's
H3-22 gives 21.7 TB for USD 64, which is USD 2.95. Both are above Hetzner's floor and below its
dedicated line, and both include a port that does not have to be sized.

### Contabo Object Storage (S3-compatible)

> 250 GB increments, up to 25 TB, 5 TB max object size

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 TB max object. A new account costs card. Observed behaviour: Triple-replicated Ceph per their docs. Read path (recorded as not metered): Truly free and unlimited , page title is 'S3-Compatible & Free Egress'; body: 'unlimited transfer included in the flat monthly rate', 'no hidden traffic or download' charges, 'retrieval is not billed separately'. (`reported`, 2026-10-21).

Evidence: `https://contabo.com/en/object-storage/` (2026-10-21), record `dossier/storage/contabo-object-storage.json`.
Verdict: `qualifies-with-caveat`.

### Datalix S3-compatible Object Storage (Frankfurt)

> 1 TB, 100 TB per account, 30 M objects per bucket

That is the record's own wording (`documented`, 2026-10-22). A new account costs email. Observed behaviour: Small German host (AS203446), Equinix FRA-05/07/08. Read path (recorded as metered): Verbatim: 'Ingress is free and unlimited.' / 'Egress includes 10 TB per 1 TB of storage.' / '10 TB egress included per 1 TB of booked storage.' At 20 TB booked that is 200 TB/mo included , 6.6x a 30 TB/mo serving load. (`documented`, 2026-10-22).

Evidence: `https://datalix.eu/rent-s3-compatible-objectstorage` (2026-10-21), record `dossier/storage/datalix-s3-compatible-object-storage.json`.
Verdict: `qualifies`.

### Hetzner Storage Box BX11 / BX21 / BX31 (1/5/10 TB)

> 1 TB / 5 TB / 10 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Same platform as BX41, verified as EUR 3.20/TB at 1 TB, confirmed unchanged observed. Read path (recorded as not metered): Unlimited on all four tiers , the matrix row 'Traffic | Unlimited' spans 1/5/10/20 TB. Same fair-use caveat as BX41. (`reported`, 2026-10-21).

Evidence: `https://www.hetzner.com/storage/storage-box/` (2026-10-21), record `dossier/storage/hetzner-storage-box-bx11-bx21-bx31.json`.
Verdict: `qualifies`.

### Hetzner SX135-2 dedicated storage server

> 8x 16 TB SATA = 128 TB raw; 112 TB usable at RAID-6

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Scales the SX65 down in EUR /TB, at 128 TB the per-TB rate is worse than SX65-2 but the absolute egress headroom (1 Gbit = ~330 TB/mo theoretical) is unchanged.

Evidence: `https://www.hetzner.com/dedicated-rootserver/sx135/` (2026-10-21), record `dossier/storage/hetzner-sx135-2-dedicated-storage-server.json`.
Verdict: `qualifies-with-caveat`.

### Hetzner SX65-2 dedicated storage server

> 4x 16 TB SATA = 64 TB raw; 48 TB usable at RAID-5 (4x 22 TB = 88 TB raw available as SX65-1/-3)

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: This is the lowest genuine EUR /TB in Europe found observed. Read path (recorded as not metered): Verbatim matrix: 'Traffic usage is unlimited and free of charge. Please note that our unlimited traffic policy does not apply to servers that have the 10G uplink addon. (`reported`, 2026-10-21).

Evidence: `https://www.hetzner.com/dedicated-rootserver/sx65/` (2026-10-21), record `dossier/storage/hetzner-sx65-2-dedicated-storage-server.json`.
Verdict: `qualifies`.

### HostBrr StorageBox (Germany / USA)

> 500 GB, 16 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Multiple positive LET reviews over 12+ months ('uptime + speed has me impressed', 'genuinely, I couldn't be a happier customer'). Read path (recorded as metered): Verbatim: 'Every plan includes transfer equal to five times its storage, so there is never a surprise line item for downloading your own data.' 1 TB 5 TB transfer; 16 TB 80 TB transfer. (`reported`, 2026-10-21).

Evidence: `https://hostbrr.com/storageboxes.html` (2026-10-21), record `dossier/storage/hostbrr-storagebox.json`.
Verdict: `fails-quota`.

### InterServer Storage VPS (1 TB slices)

> 1 TB per slice, 1, 20+ slices stacked

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 10 Gbps shared port. A new account costs card. Observed behaviour: Long-established US host (Secaucus/LA).

Evidence: `https://www.interserver.net/vps/storage.html` (2026-10-21), record `dossier/storage/interserver-storage-vps.json`.
Verdict: `qualifies-with-caveat`.

### Kimsufi KS-5 (OVH budget brand)

> 2x 2 TB, 2x 4 TB HDD (configured up to 3x 4 TB)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 300 Mbps public port caps near ~97. A new account costs card. Observed behaviour: OVH's clearance brand, cheapest way into OVH's network with unlimited traffic.

Evidence: `https://www.kimsufi.com/en/` (2026-10-21), record `dossier/storage/kimsufi-ks-5.json`.
Verdict: `qualifies-with-caveat`.

### OVHcloud Object Storage, One Zone Standard

> unlimited, per GiB

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: The cheapest metered-egress-free hot S3 tier among the mainstream EU clouds.

Evidence: `https://www.ovhcloud.com/en/public-cloud/prices/` (2026-10-21), record `dossier/storage/ovhcloud-object-storage-one-zone-standard.json`.
Verdict: `qualifies-with-caveat`.

### STRATO HiDrive Business

> 1 / 3 / 5 / 10 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: STRATO is the German consumer-grade option. Read path (recorded as not metered): Not published as a volume on the pricing page. Protocol access (SFTP, WebDAV, SMB, rsync, SCP, Git) is tier-gated: 'Im Business Essential und Standard Tarif sind die Zugriffsmoglichkeiten WebDAV und SMB inklusive. (`reported`, 2026-10-21).

Evidence: `https://www.strato.de/cloud-speicher/hidrive-business/` (2026-10-21), record `dossier/storage/strato-hidrive-business.json`.
Verdict: `qualifies-with-caveat`.

### Wasabi Hot Cloud Storage

> Pay-as-you-go, billed per-GB/day; Reserved Capacity from 25 TB

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: ` 90-day minimum storage duration on pay-as-you-go (30 days on RCS). A new account costs card. Observed behaviour: Most enterprise-grade of the cheap set, but the 90-day minimum and the 1:1 egress ratio are both hostile to this workload: 30 TB/month of serving against 10 TB hot storage is 3:1.

Evidence: `https://wasabi.com/pricing` (2026-10-21), record `dossier/storage/wasabi-hot-cloud-storage.json`.
Verdict: `qualifies-with-caveat`.

### Webtropia Storage Server RYZ5-20 (4x 22 TB)

> 4x 22 TB = 88 TB raw (RYZ5-12: 4x 14 TB = 56 TB, EUR 79.99)

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Cheapest raw EUR /TB found in Europe, but the traffic term is unverified, do not commit without a ticket.

Evidence: `https://www.webtropia.com/en/amd-storage-server.html` (2026-10-21), record `dossier/storage/webtropia-storage-server-ryz5-20.json`.
Verdict: `qualifies-with-caveat`.

### BorgBase, Medium / Large

> 10 GB free forever; Small 250 GB, Medium 1 TB, Large 2 TB; flexible quota up to 3x plan

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: EU or US region choice. Read path (recorded as not metered): Verbatim from docs: "We don't charge upload, download or API calls." Unmetered, fair-use policed by a human. (`reported`, 2026-10-21).

Evidence: `https://www.borgbase.com/` (2026-10-21), record `dossier/storage/borgbase-medium-large.json`.
Verdict: `fails-quota`.

### Feral Hosting, Radon (8 TB)

> 1 / 1.5 / 2 / 3 / 4.5 / 8 TB HDD; SSD line 150 GB-1.6 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: Own ISP and hardware since ~2008. Read path (recorded as not metered): Truly unmetered both directions, 20 Gbit/s, fair-use with weekend peak throttling. Verbatim FAQ: "We run our own ISP meaning upload quotas no longer makes sense for us. (`reported`, 2026-10-21).

Evidence: `https://www.feralhosting.com/pricing` (2026-10-21), record `dossier/storage/feral-hosting-radon.json`.
Verdict: `qualifies-with-caveat`.

### HostBrr, StorageBox 16TB

> 16 TB on NVMe-cached HDD RAID-60 (500 GB / 1 / 2 / 4 / 8 / 16 TB)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 100 MB/s I/O ceiling reported by buyer. A new account costs email. Observed behaviour: Forum reality check: LET buyers report the '10 Gbps' is not delivered (480 Mbps observed), a 100 MB/s I/O cap.

Evidence: `https://hostbrr.com/storageboxes.html` (2026-10-21), record `dossier/storage/hostbrr-storagebox-16tb.json`.
Verdict: `qualifies-with-caveat`.

### Hosting by Design, App hosting 24 TB (owners of seedbox.io)

> 1 / 2 / 4 / 8 TB shared; 18 / 24 / 28 TB dedicated disk

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: seedbox.io now 301-redirects to hostingby.design, same operator (HNielsen Technologies ApS, DK). Read path (recorded as metered): Shared tiers metered (1TB->3TB, 2TB->6TB, 4TB->10TB, 8TB->25TB out). 18/24/28 TB dedicated tiers list "Unlimited" outgoing. (`reported`, 2026-10-21).

Evidence: `https://hostingby.design/app-hosting/` (2026-10-21), record `dossier/storage/hosting-by-design-app-hosting-24-tb.json`.
Verdict: `qualifies`.

### PulsedMedia, M10G Storage Box 16TB

> 16 TB HDD RAID5 (4/8/16/32 TB tiers)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 100 Mbps sustained egress. A new account costs email. Observed behaviour: Own DC in Finland, 15+ yrs operating.

Evidence: `https://pulsedmedia.com/storage-boxes.php` (2026-10-21), record `dossier/storage/pulsedmedia-m10g-storage-box-16tb.json`.
Verdict: `qualifies`.

### rsync.net, Standard (ZFS, SSH-only filesystem)

> 800 GB minimum order; 0-9 TB, 10-99 TB, 100+ TB bands

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Operating since 2001, 7 daily + 4 weekly snapshots on 10 TB+ accounts, physical media shipment. Read path (recorded as not metered): "No Egress Charges" / "NO Charges for ingress/egress" , unmetered both ways, no per-request fees. (`reported`, 2026-10-21).

Evidence: `https://www.rsync.net/pricing.html` (2026-10-21), record `dossier/storage/rsync-net-standard.json`.
Verdict: `qualifies-with-caveat`.

### SeedHost.eu, HD 24

> 1 / 2 / 3 / 4 / 5 / 7 / 9 / 12 / 15 / 18 / 24 TB HDD

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: NL, long-running. Read path (recorded as metered): Store page notes "only outgoing traffic is counted to the limit (UL), incoming (DL) is not counted". (`reported`, 2026-10-21).

Evidence: `https://www.seedhost.eu/shared-app-hosting/` (2026-10-21), record `dossier/storage/seedhost-eu-hd-24.json`.
Verdict: `qualifies-with-caveat`.

### Ultra.cc, Platinum 28 TB

> 1 / 2 / 4 / 6 / 8 / 12 / 16 / 22 / 28 TB HDD

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: NL/CA/SG. Read path (recorded as metered): "Unmetered Download" + "50Gbps Shared Upload", but a monthly upload allowance per plan: 2 TB (1TB plan) to 70 TB (28TB plan). (`reported`, 2026-10-21).

Evidence: `https://ultra.cc/` (2026-10-21), record `dossier/storage/ultra-cc-platinum-28-tb.json`.
Verdict: `qualifies-with-caveat`.

### Whatbox, H3-22

> 3.9 / 5.9 / 9.9 / 15.8 / 21.7 TB HDD

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 100 Mbps throttle, not a bill 3. A new account costs email. Observed behaviour: Running since 2008.

Evidence: `https://whatbox.ca/plans` (2026-10-21), record `dossier/storage/whatbox-h3-22.json`.
Verdict: `qualifies-with-caveat`.

### Advin Servers KVM Storage VPS

> Kansas City: Storage 1 2,560 GB / Storage 2 5,120 GB / Storage 3 10,240 GB / Storage 4 20,480 GB, each as 20 GB NVMe boot + HDD, 10 Gbps

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 10 Gbps. A new account costs card. Observed behaviour: Delaware-based, ~30 nodes US+EU, 99.9% SLA, 14-day money-back, own hardware.

Evidence: `https://advinservers.com/vps` (2026-10-21), record `dossier/storage/advin-servers-kvm-storage-vps.json`.
Verdict: `qualifies-with-caveat`.

### AlphaVPS Storage VPS

> 256 GB / 512 GB / 1 TB / 2 TB / 3 TB / 4 TB / 8 TB / 16 TB. 16 TB is the ceiling on a single VPS; the ladder is flat-priced, so EUR /TB does not improve above 1 TB

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Bulgarian operator (DA International Group Ltd.), own AS203380 since 2013, 99.9% uptime SLA in the published SLA. Read path (recorded as not metered): Plan transfer allowances: 1 TB plan = 3 TB/mo, 2 TB plan = 6 TB, 4 TB = 10 TB, 8 TB = 20 TB, 16 TB = 40 TB, all on ports 'up to 10 Gbit'. (`reported`, 2026-10-21).

Evidence: `https://alphavps.com/storage-vps` (2026-10-21), record `dossier/storage/alphavps-storage-vps.json`.
Verdict: `qualifies`.

### BuyVM Block Storage Slabs

> Sold in 256 GB chunks at $1.25/month. 1 TB = $5.00/mo. 10 TB = $50.00/mo. Max 10 TB per slab, up to 8 slabs per server

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Max 10 TB. A new account costs card. Observed behaviour: BuyVM/Frantech have a strong 10+ year reputation on LET for storage VPS and for not overselling. Read path (recorded as not metered): 'Unmetered Bandwidth' on every slice, governed by a fair-use rule the company states publicly on LET: 'The rule-of-thumb for WAN (internet-facing connections) is 100Mbit/s of 24/7 usage per every 4GB of memory with a purchased slice. (`reported`, 2026-10-21).

Evidence: `https://buyvm.net/block-storage-slabs/` (2026-10-21), record `dossier/storage/buyvm-block-storage-slabs.json`.
Verdict: `fails-quota`.

### DeluxHost Storage VPS

> STORAGE-1 500 GB / -2 1 TB / -3 2 TB / -4 3 TB / -5 4 TB / -6 5 TB / -10 20 TB. HDD RAID-5 + NVMe cache, Eygelshoven NL, SkyLink DC

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Small NL provider. Read path (recorded as not metered): 'Unlimited Traffic, fair usage' on every storage plan. (`reported`, 2026-10-21).

Evidence: `https://deluxhost.net/en/storage` (2026-10-21), record `dossier/storage/deluxhost-storage-vps.json`.
Verdict: `qualifies`.

### GreenCloudVPS Storage KVM

> US/EU: Storage-0.5TB 500 GB, Storage-1 1 TB, Storage-2 2 TB (SATA RAID-10, 10 Gbps port). APAC: same three sizes in Tokyo and Singapore but with a quarter of the bandwidth. **No plan above 2 TB exists.**

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 10 Gbps port). A new account costs card. Observed behaviour: '#1 Top Provider Award & #1 Most Stable Provider on LowEndTalk' is their own claim on their own page.

Evidence: `https://green.cloud/storage-kvm-vps.php` (2026-10-21), record `dossier/storage/greencloudvps-storage-kvm.json`.
Verdict: `qualifies`.

### HostBrr storage VPS + HDD block

> Premium StorageBrr 1/2/4/6/8 GB RAM with 500 GB HDD block included, configurable upward. Budget line quoted at '$2.5 per TB of HDD storage' and hybrid at '$3.75 per TB' on the order forms page

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: German provider, generally well regarded on LET/LowEndSpirit for the price. Read path (recorded as metered): Metered: 3,000 GB on the 1 GB plan, 5,000 GB on the 2 GB, 10,000 GB on the 4 GB, 15,000 GB on the 6 GB, 20,000 GB on the 8 GB. (`reported`, 2026-10-21).

Evidence: `https://my.hostbrr.com/order/main/packages/storage/?group_id=26` (2026-10-21), record `dossier/storage/hostbrr-storage-vps-hdd-block.json`.
Verdict: `qualifies`.

### HostHatch Storage VM

> 1 / 2 / 3 / 4 / 5 / 6 / 8 / 10 TB HDD, 'enterprise-grade spinning hard disk drives', 8 locations

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Mixed and the worst reliability record of the three leaders. Read path (recorded as metered): Exceeding it is throttling, not billing , a holder of the 2 TB Hong Kong plan reports '2.5 TB (throttled to about 5 Mbps after limit from my experience)' (LET thread 217891). (`reported`, 2026-10-21).

Evidence: `https://hosthatch.com/products` (2026-10-21), record `dossier/storage/hosthatch-storage-vm.json`.
Verdict: `qualifies-with-caveat`.

### Kyun.host Bricks (HDD block)

> HDD block volumes attached to a Danbo VM, Romania only. Initial beta run ~20 TB capacity total across all customers

That is the record's own wording (`reported`, 2026-10-21). A new account costs email. Observed behaviour: The most honest reliability disclosure in this lane and simultaneously the worst track record. Read path (recorded as metered): The model is a VM plus attachable block, with the VM carrying the traffic allowance. Treat as unknown/unmetered-by-usage rather than free , this is a one-person operation and the beta explicitly has no published egress schedule. (`reported`, 2026-10-21).

Evidence: `https://blog.kyun.sh/p/bricks` (2026-10-21), record `dossier/storage/kyun-host-bricks.json`.
Verdict: `qualifies-with-caveat`.

### NovaCloud-Hosting Storage VPS

> Storage Stellar 2 TB, Storage Cosmic 6 TB, plus a 1 TB special. 20 GB NVMe RAID-1 boot + HDD RAID-6 with NVMe cache, Netherlands

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Small NL provider, active on LET as a Patron Provider. Read path (recorded as metered): 'Fair-Use Traffic' with no published number on the storage page , the offer threads give '7,5 TB Traffic per month included' on the 2 TB plan and describe 'Unlimited @ 5Gbps shared' on the 1 TB special. (`reported`, 2026-10-21).

Evidence: `https://novacloud-hosting.com/vps-storage` (2026-10-21), record `dossier/storage/novacloud-hosting-storage-vps.json`.
Verdict: `qualifies-with-caveat`.

### ServaRica storage VPS

> Opossum 1 1 TB, Opossum 2 1 TB, Polar Bear 2 TB, Killer Whale 3.5 TB, Horse 3 TB, Penguin 4 TB, Mammoth 8 TB; the 4-20 TB tier adds Chimera Hybrid 4 TB / 8 TB / 16 TB at 4-16 TB of HDD plus NVMe. RAIDZ2 on HDD, Montreal CA

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Long-standing CA provider with a strong LowEndTalk record, 'Have been using servarica for close a year now.

Evidence: `https://servarica.com/storage-servers-2/` (2026-10-21), record `dossier/storage/servarica-storage-vps.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Contabo Storage VPS 30 | fails-quota | 1 TB SSD (Storage VPS 10/20: 300/400 GB) |
| IONOS HiDrive (retail) | fails-quota | 100 GB / 250 GB / 1 TB / 2 TB on the public ladder |
| netcup Storage Space / Local Block Storage | fails-quota | Tariff A 250 GB / B 500 GB / C 1 TB inclusive, expandable per GB |
| Time4VPS Storage VPS 1 TB (Lithuania, EU) | trial-only | 0.25 / 0.5 / 1 TB |
| Time4VPS Storage VPS | trial-only | 0.25 TB (256 GB) / 0.5 TB / 1 TB / 8 TB. Lithuania, Vilnius. SATA HDD |

The rejections here are few and they are all quota or trial. A storage VPS line that ships 50 GB
at every tier regardless of price is the clearest: LightNode markets a "Storage VPS" and its
largest SKU is 50 GB, so the product name is the finding and the disk is not.

The second group is `trial-only`, which in this class means a free period followed by a paid
plan. A 30-day trial with 1 TB of block storage is a way to test a host, not a way to hold data.

## Chaining

A storage box is the hot and serving tier of a hybrid composition, and the free archive stays on
Cloudflare Pages.

Two rules follow from the arithmetic. Size the box by the port, not the disk, because a 16 TB
box with a 100 Mbps port carries 0.982 TiB per day and a 20 TB box with unlimited traffic carries
whatever the uplink does. And keep the archive off the box, because the box is the only tier with
a monthly invoice and the archive is the tier that grows.
