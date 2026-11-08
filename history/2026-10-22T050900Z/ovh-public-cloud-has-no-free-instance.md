# OVH's public cloud has no free instance, and the record priced it as one

- **When:** 2026-10-22T05:09:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/ovhcloud.json` (verdict `qualifies-with-caveat`, free tier "USD 200 of one-time credit"), and the same figure in `dossier/compute/ovh-gpu.json`
- **Superseded by:** both records, rewritten on 2026-10-22
- **Evidence:** `https://us.ovhcloud.com/public-cloud/prices/` and `https://www.ovhcloud.com/en/public-cloud/prices/`, both read 2026-10-22
- **Confidence:** documented

## What we believed

That OVH's public cloud qualified on the strength of a USD 200
one-time credit, and that a GPU row qualified the same way.

## What we found

The credit is real and it is a **trial**: `### Get started with US$ 200 free`,
with the qualifying sentence *"You can find out if our solutions meet your needs
by trying them out for free."* There is no free instance tier underneath it.

The ladder starts at `b2-7` — 2 vCore, 7 GB, 50 GB of SSD — at **$31.19 a month**
or $0.0879 an hour. A `b3-8` is $0.0605 an hour. The largest row, `b3-640` at 160
vCore and 640 GB, is $2,996.39 a month.

One clause on the same page matters more than the prices, because it is the axis
the topic has never recorded: **"Outbound public network traffic is included in
the price of instances in all locations except the Asia-Pacific region (Singapore,
Sydney, and Mumbai)."** For a serving load of 500 GB to 1 TiB a day, that is the
difference between a metered bill and a flat one, and it is bought with the
instance: the guaranteed bandwidth runs from 250 Mbit/s on `b2-7` to 20 Gbit/s on
`b3-640`. The egress ceiling is a line item in the size you choose.

USD 200 at $0.0879 an hour is about 2,275 instance-hours, which is 3.1 months of
one `b2-7` running around the clock. That is a trial, and stating it as a
qualifying free tier overstated the supply by the whole of the rest of the year.

## How we found it

One read of each regional price list. The record cited the US list and had never
opened it; its `confidence_note` said in as many words that the page was "not
re-read".

## What it cost us

Two rows in the qualifying group that should have been in the trial group. Worse,
both rows hid the egress clause, which is the one fact that would decide whether
OVH is worth $31 a month at all.

## What a future session should do differently

⭐ **A credit is not a tier, and the arithmetic that separates them is one
division.** Divide the credit by the cheapest hourly rate: if the answer is
months, it is a trial; if it is unbounded because the rate is zero, it is a tier.
Doing that division before writing `qualifies` would have caught this row and the
three cloud rows in the same group.

⚠ **Read the egress clause on the same page as the price.** OVH includes outbound
traffic outside Asia-Pacific; most hyperscalers meter it from the first byte. The
two facts are one paragraph apart and they answer different questions.
