# Tencent Cloud Studio gives a monthly minute allowance, not a paid-only product

- **When:** 2026-10-22T15:02:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/tencent-cloud-studio.json` verdict `paid-only`
- **Superseded by:** `dossier/compute/tencent-cloud-studio.json` verdict `qualifies-with-caveat`; `docs/compute/free/asian-clouds.md`
- **Evidence:** vendor pages read 2026-10-22 through `scripts/broker/broker.sh read`; the exact URLs and quoted sentences are in each record's `evidence[]` and in the body below
- **Confidence:** documented

## What we believed

That Cloud Studio was a paid product with no free lane.

## What we found

Tencent's product 1039 document, `https://cloud.tencent.com/document/product/1039/94098`, read
2026-10-22, states in the original: "免费额度内每月提供5万分钟通用工作空间使用时长和1万分钟高性能空间使用时长，超出后按量计费。"
That is 50,000 minutes a month of general workspace time and 10,000 minutes a month of
high-performance workspace time inside the free allowance, billed on demand beyond it.

A second regime runs in parallel at `cloudstudio.net`, where a 20 machine-hour pack is granted
on binding a Tencent Cloud account and 2 machine-hours can be claimed on each daily login,
valid 7 days.

## What it changes

The verdict becomes `qualifies-with-caveat`. Three caveats are recorded: an exhausted pack
does not stop the application and bills on demand, a free high-performance workspace idle for
30 days is released without recovery, and reaching the paying account needs Tencent Cloud
real-name verification, which the China site issues for mainland, Hong Kong, Macau and Taiwan
documents.

## The transferable point

Two products with similar names ran in parallel here, one with a minute allowance and one
with expiring machine-hours. The record names which one it prices, because a reader who mixes
them plans against the wrong meter.
