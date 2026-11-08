# The paid lane: what money buys that a free tier cannot

The free lane is bounded by retention and identity. The paid lane is bounded by the egress
ratio, and that is a different constraint with a different decision behind it. A free tier fails
because the clock runs out or the door is shut. A paid tier fails because the read costs more
than the storage, and the read is the half the pricing page puts in a footnote.

This page states the argument: what the paid lane buys, what it costs at the three
workloads, and where the floor actually is.

## What money buys

Three things, and only one of them is capacity.

**It buys a clock you control.** No retention band, no inactivity deletion, no re-upload loop.
That is the single largest difference between a free archive and a paid one, and it is worth
more than the capacity.

**It buys a port that can be sized.** A free tier's read path is shaped for somebody else's economics.
A paid box's port is a specification, and 100 Mbps is 0.982 TiB per day while 1 Gbps is 9.82 TiB.

**It buys a vendor with a contract.** Not a guarantee: a
fair-use clause is discretionary rather than contractual. But a company with an invoice has a
reason to answer, and a volunteer with a server does not.

It does not buy capacity cheaply. The floor across the whole paid lane is EUR 1.69 per TB per
month for a managed box on a 100 Mbps port. Everything below that figure is cold storage or a bet.

## The floor: a managed box

⛔ **The cheapest per TB is a disk bought outright, and it is out of scope here.** The corpus
assumes no local hardware, so a bought disk is not an option rather than a cheaper one.
The arithmetic is real — roughly USD 0.37 to 0.48 per TB per month all-in for a 20 TB machine
amortised over five years, which is five to six times below the best managed box — and it is
recorded in `history/2026-10-22T061500Z/own-the-disk-is-not-an-option.md`.
**It is not the recommendation.**

What the floor actually is: a rented or managed box, invoiced monthly, on somebody else's
hardware.

| provider | capacity | monthly | per TB per month | egress |
|---|---|---|---|---|
| Serverdiscounter NEXT Share | 25 TB managed Nextcloud | EUR 59.95 | EUR 2.40 | included |
| Hetzner Storage Box BX41 | 20 TB | EUR 40.60 | EUR 2.03 | unlimited, vendor-stated |
| PulsedMedia M10G | 16 TB | EUR 26.99 | EUR 1.69 | unlimited at 100 Mbps |
| DanubeData Storage Share | 10 TB managed Nextcloud | EUR 29.99 | EUR 3.00 | included |

EUR 40.60 / 20 TB = EUR 2.03 per TB per month, and EUR 26.99 / 16 TB = EUR 1.69. Those two are
the floor for capacity that can actually be bought, and the EUR 1.69 row is the cheaper of them
only because its port is smaller: 100 Mbps is 0.982 TiB per day, so it fits 500 GB per day and
does not fit 1 TiB. The price difference between the two rows buys the port.

## The three workloads, priced

The composition depends on which end of the range is real, and the difference is
EUR 14.

| workload | right buy | monthly cost | what binds |
|---|---|---|---|
| 500 GB per day serving | PulsedMedia M10G, 16 TB | EUR 26.99 | the port is 50% used |
| 1 TiB per day serving | Hetzner BX41, 20 TB | EUR 40.60 | fair use at 250 TB per month, 8.3x above |
| cold archive only | 1fichier GOLD, 10 TB | EUR 108 per year | cold tier, 300 GB per file |
| free tiers for the archive | Cloudflare Pages plus a box for hot | the box only | the archive never touches the box |

A "$30 hybrid" is priced for the low end of the range while the workload table says
500 GB to 1 TiB every day. At 1 TiB per day the EUR 27 box is 101.8% of its port, so the honest
answer is EUR 40.60. Do not budget EUR 27 and expect 1 TiB per day.

## Cheapest in class, not cheapest overall

The four headline rates are four products, and the column heading is the defect.

| rate | class | what it cannot do |
|---|---|---|
| EUR 0.90 per TB (1fichier GOLD) | cold archive | serve a working set, or hold a file over 300 GB |
| USD 1.28 per TB (Uloz.to) | hot, 12x transfer allowance | exceed the ratio without a renegotiation |
| EUR 1.69 per TB (PulsedMedia M10G) | hot, 100 Mbps port | carry 1 TiB per day |
| EUR 2.03 per TB (Hetzner BX41) | hot, unlimited traffic | exceed a discretionary 250 TB per month |

Only the last one survives a 3:1 read-heavy serving pattern on a term rather than a ratio, and
its term is still discretionary. That is the honest summary of the paid lane: the cheapest rate
that works is not the cheapest rate.

## The egress traps, which are the decisive column

Every cheap-storage claim dies here, and the table is the reason this document exists.

| provider | advertised | reality | all-in per stored TB with one full read per month |
|---|---|---|---|
| IONOS | USD 4.99 per TB | plus USD 0.024 to 0.036 per GB out | about USD 30 |
| Scaleway | EUR 8.22 per TB | plus EUR 0.01 per GB | about EUR 18 |
| Selectel Ice | USD 11.04 per TB | USD 24.31 per TB per read-back | USD 35 |
| Tencent COS | USD 18.06 per TB | USD 76.52 per TB egress | catastrophic |
| Wasabi | "free egress" | 1:1 ratio only, and 3:1 is "not a good fit" | fails its own test |
| PikPak | USD 0.83 per TB | rclone is a "Connected App", which is 1 TB per month | about 30 times short |
| netcup | cheap | freezes the volume for the month | worse than expensive |
| AlphaVPS | "EGRESS EUR 0" | EUR 3.00 per TB overage in the terms | EUR 40 to 85 |
| Storadera | "No download charges" | downloads capped at the stored amount | misleading |
| Icedrive | USD 3.00 per TB | bandwidth both ways at 2x | fiction |

The rule survives every check: when a vendor says free egress, find the
ratio or the cap, and find what the ratio is counted on. Wasabi is 1:1 (`wasabi.com/pricing/faq`,
read 2026-10-22); MEGA S4 is 5:1 (`mega.io/objectstorage`, read 2026-10-22); Datalix is 10:1
(`datalix.de/s3-kompatibler-objectstorage-mieten`, read 2026-10-22); Hetzner and 1fichier's cold
tier publish no ratio at all. Only the last two survive a 3:1 pattern.

pCloud is 2:1 on **public shared-link traffic only** (`help.pcloud.com/article/shared-link-
traffic`, read 2026-10-22: Premium Plus 2 TB gets 4 TB per month, Ultra 10 TB gets 20 TB), and
that qualifier decides which side of the argument pCloud is on. The cap is on downloads that
other people make through a shared link. API, WebDAV and rclone downloads are not counted against
it, and rclone is the access path for a private archive. So pCloud is a trap for a CDN-fronted serving
workload and fine for a private archive read back over rclone. A ratio quoted without its scope
is a different claim, and this one was.

## The documents

| document | the question it answers |
|---|---|
| [`storage-boxes.md`](storage-boxes.md) | which box is cheapest per usable TB, and what its port caps |
| [`object-storage.md`](object-storage.md) | which S3-compatible store survives a read-heavy pattern |
| [`lifetime-and-deals.md`](lifetime-and-deals.md) | which lifetime deal is real, and when to buy |
| [`regional.md`](regional.md) | is regional cheaper, and by how much (it is not) |
