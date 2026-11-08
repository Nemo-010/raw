# PulsedMedia's "unlimited" is a port speed, and 1 TiB/day is 101.8% of it

- **When:** 2026-10-22T03:07:46Z
- **Status:** corrected
- **Supersedes:** `docs/storage/paid/storage-boxes.md` section "The port is the limit, not the quota" and `docs/storage/paid/README.md` section "The three workloads, priced"
- **Superseded by:** `docs/storage/paid/storage-boxes.md` section "The port is the limit, not the quota"
- **Evidence:** `curl -L https://pulsedmedia.com/storage-boxes.php` returned 200 with 7,273 bytes on 2026-10-22, carrying "Unlimited@100Mbps (~30TB/Month / ~1TB/Day)" four times and the price literals 8.99, 14.99, 26.99 and 63.99 EUR; capture in `.tmp/work/w-storage/probes/`
- **Confidence:** measured

## What we believed

The seed's report treated PulsedMedia's "Unlimited@100Mbps (~30TB/Month / ~1TB/Day)" as a vendor
that quantifies its own cap, which reads as honest and adequate. Its 16 TB plan at EUR 26.99 was
the cheapest hot option in the corpus at EUR 1.69 per TB, and the report's headline recommendation
was a "$30 hybrid" built on it.

Both figures in the vendor's own string look like they support the workload. 30 TB per
month is above the 15 to 30 TB a 500 GB to 1 TiB per day serving pattern needs, and ~1 TB per day
is exactly the top of the stated range.

## What we found

The cap is the port, not the allowance, and the two are within 2% of each other at the top of the
range.

| quantity | value |
|---|---|
| 100 Mbps sustained for 24 hours | 1.08 TB, which is 0.982 TiB |
| 1 TiB per day requires | 101.8 Mbps |
| so 1 TiB per day is | 101.8% of the port |

The vendor's "~1TB/Day" is 30 TB divided by 30 days, which is arithmetic rather than a sustained
rate, and the TB there is decimal. So the usable figure is 0.98 TiB per day, which is 2% short of
the specification before any contention.

Contention is not speculative. The operator's own wiki states the M10G port is shared between
about twelve users, so a sustained 800 to 900 GB per day is the honest ceiling.

The conclusion re-sizes the recommendation rather than breaking it. At 500 GB per day the box is
comfortable at about half its port. At 1 TiB per day it is at or past the edge, and the right
purchase is Hetzner BX41 at EUR 40.60, whose constraint is a discretionary fair-use threshold
rather than a port speed.

## How we found it

One division. 100 Mbit/s times 86,400 seconds divided by 8 is 1.08e12 bytes, which is 1.08 TB
decimal and 0.982 TiB. The corpus's own rate-conversion table in `docs/conventions/README.md`
states the same figure, so the arithmetic was available and unused.

The measurement this session added is the price and the string: the page carries
"Unlimited@100Mbps (~30TB/Month / ~1TB/Day)" four times and 26.99 EUR for the 16 TB tier, which
confirms the vendor's own wording rather than a reseller's summary of it.

## What it cost us

One purchase. A reader who budgeted EUR 27 for a 1 TiB per day workload would have bought a box
that cannot carry it, discovered the shortfall under load, and had no obvious explanation: the
vendor said 1 TB per day and the plan table said 30 TB per month.

The second cost is that the report's own table had already been corrected to say the EUR 27 box
cannot carry 1 TiB per day, while the prose below it still said "$30 hybrid". A table and a
paragraph in the same section disagreed, and the paragraph was the one a reader acts on.

## What a future session should do differently

Convert every "unlimited" to a rate before comparing it, and convert the rate to bytes per day
before comparing it with a byte target. A port speed and a monthly allowance are not the same
instrument, and this vendor publishes both in one string, which is what makes the error easy.

When a vendor writes "unlimited@<rate>", the rate is the specification and the word is decoration.
