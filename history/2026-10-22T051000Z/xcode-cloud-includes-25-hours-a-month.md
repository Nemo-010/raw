# Xcode Cloud includes 25 compute hours a month, and the record called it paid-only

- **When:** 2026-10-22T05:10:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/xcode-cloud.json` (verdict `paid-only`, "the source card records no free tier")
- **Superseded by:** the same record, rewritten on 2026-10-22
- **Evidence:** `https://developer.apple.com/xcode-cloud/` read 2026-10-22
- **Confidence:** documented

## What we believed

That Xcode Cloud was paid-only, because someone had to pay for it and the corpus
card recorded no free tier.

## What we found

The product page's own first section is headed **"Get started for free with
Xcode"**, and it carries the allowance:

> 25 compute hours/month — Included with Apple Developer Program membership.

Apple Developer Program membership is USD 99 a year. So the hours are not free in
the sense that the corpus uses the word — they attach to a paid account — but they
**recur every month**, and 25 hours is more than every other free tier in this
topic except the ones with no cap at all. The paid ladder above it runs from
$49.99 a month for 100 hours to $3,999.99 for 10,000.

The correct verdict is `qualifies-with-caveat`, and the caveat is the identity
gate rather than the price: `identity_cost.kind` is `card`, because the membership
is the gate. That is a different finding from "no free tier", and it is the one a
reader needs.

## How we found it

One read of the page the record already cited. The word "free" is in the second
heading on it.

## What it cost us

A row in the paid tables for a provider that gives 25 recurring hours to anyone
who already pays Apple $99 a year, which for an iOS developer is not an extra
cost at all. The corpus has several readers who would have skipped it.

## What a future session should do differently

⭐ **`paid-only` and `qualifies-with-caveat` differ by whether the account you
must already hold is one the target reader plausibly holds.** A developer-programme
membership is not a payment for compute; it is a membership that carries compute.
The test is not "does money change hands" but "does money change hands *for this*".

⚠ **Read the heading above the ladder.** This page's ladder is four paid tiers,
and a reader who greps for prices finds only those. The allowance was in the
sentence before them.
