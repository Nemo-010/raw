# A first-party page said the free tier was larger than the census recorded, and a second page said it was smaller

- **When:** 2026-10-22T03:15:24Z
- **Status:** observed
- **Supersedes:** `.tmp/work/recon-extras/DATABASES-KV.md` §Verified inventory, the TiDB Cloud
  Starter row
- **Superseded by:** `docs/databases-kv/free/postgres-always-on.md` §TiDB Cloud Starter
- **Evidence:** `pingcap.com/pricing` and `docs.pingcap.com/tidbcloud/serverless-faqs/`, both read
  2026-10-22
- **Confidence:** documented

## What we believed

The census recorded 25 GiB of row storage and 250 million Request Units per organization, and
marked the figure "corrected upward" from the 5 GiB and 50 million RU that circulate. That is
correct as far as it goes, and it is half the story.

## What we found

Two TiDB pages disagree, and both were read on the same day.

The pricing page states the allowance **per organization, across up to five eligible instances**:
25 GiB of row storage, 25 GiB of columnar storage and 250 million Request Units.

The documentation FAQ states it **per instance**: "5 GiB row data + 5 GiB columnar data + 50
million RUs per TiDB Cloud Starter instance", for up to five instances.

The two readings differ by a factor of five, and both cannot be right. The census took the pricing
page and did not open the FAQ.

## How we found it

The census cited the pricing page and the FAQ in the same row, so both were opened. The pricing
page matched the census. The FAQ did not.

## What it cost us

Nothing yet, and this is the entry that says what it would cost. A reader who takes 25 GiB per
organization and builds five instances has 25 GiB total. A reader who takes 5 GiB per instance has
25 GiB total. The arithmetic agrees at the organization level and disagrees per instance, so the
multiplication a reader performs is the part that breaks.

## What a future session should do differently

**When a row cites two first-party pages, read both.** A vendor that documents the same allowance
twice will eventually document it differently, and the direction of the disagreement is not
predictable: here the pricing page is the generous one and the FAQ is the conservative one, which
is the opposite of the usual pattern where marketing inflates and documentation tells the truth.

The record keeps the conservative per-instance reading and names the disagreement. Settling it
needs one provisioned instance and a measurement, which no session has done.
