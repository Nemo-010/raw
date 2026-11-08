# One provider list was not the market, and affiliate comparisons are 14 per cent wrong

- **When:** 2026-10-22T23:56:54Z
- **Status:** corrected
- **Supersedes:** `docs/compute/watchlist.md`, which concluded from one 369-provider corpus that "the names in this market are known" and that only measurement was missing; and the working assumption that a comparison article is a usable source
- **Superseded by:** `scripts/sources/aggregators.tsv` with the gate's `sources` check, `docs/compute/paid/lowend-vps.md`, `docs/compute/paid/storage-vps.md`, and `METHODOLOGY.md` section 6.0
- **Evidence:** eleven aggregator sources fetched and diffed on 2026-10-22; 107 claims in four affiliate repositories checked against vendor pages; `dossier/compute/` grown from 962 to 1,128 records
- **Confidence:** measured

## What we believed

That discovery was finished. A 369-card corpus had been diffed and 368 of its providers were
already recorded, so the remaining work was to measure what existed.

## What we found

That corpus is a sandbox and devbox list. It contains almost none of the cheap VPS market:

- `vpspricetracker.com` listed 128 providers; **106 had no record**.
- TierHive, a live NAT VPS host with a USD 0.10 plan, appeared on no list that had been
  consulted. It was missed a second time because its homepage returns an empty extraction on the
  raw-HTML path and a full read on the text path, and the first result was treated as the answer.
- LowEndBox's last 52 posts named 18 hosts, 10 of them absent.
- `vps.today` claims 119 hosters and 1,825 tariffs; 14 of its names had no record.
- `zhujiceping.com` listed 25 providers, 20 absent.

The four GitHub repositories offered as a seed are affiliate articles. A lane checked **107 of
their factual claims against the vendors: 15 were wrong and 22 unverifiable**. The three that
matter: the Hong Kong large-disk ladder is 23 to 31 per cent cheaper than both Chinese seeds
print; DediRock's RAID-5 is a migration announced three times and never declared finished; and
Backblaze B2 is USD 6.95 per TB per 30 days rather than the USD 6 printed, which moves a 2 TB
year from USD 144 to USD 166.80.

## What it changes

The registry and its gate check make the omission loud rather than silent: every source that
lists providers carries a cadence and a last-diff date, and the gate fails while one is undiffed,
overdue, or missing from the watchlist. It failed on all three conditions while this was written.

`compute` now holds 1,128 records and 56 documents, including the first storage catalogue with a
price-per-TB column and a largest-machine column. The floor did not move.

The rule left behind: **a coverage claim names the list it was measured against, in the same
sentence.** "368 of 369" was true of one corpus and was read, including by me, as a claim about
the market. Those are different claims, and only one of them was measured.
