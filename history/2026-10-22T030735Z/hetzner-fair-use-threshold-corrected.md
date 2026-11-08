# Hetzner's fair-use threshold is 250 TB/month, not 50 to 100, and the margin is 8.3x

- **When:** 2026-10-22T03:07:35Z
- **Status:** corrected
- **Supersedes:** `docs/storage/paid/storage-boxes.md` section "Hetzner: two products, one machine, a 4x gap" and `docs/storage/paid/README.md` section "The three workloads, priced"
- **Superseded by:** `docs/storage/paid/storage-boxes.md` section "Hetzner: two products, one machine, a 4x gap"
- **Evidence:** the 2022 traffic notice letter quoted verbatim at `lowendtalk.com/discussion/180504`; the vendor term at `docs.hetzner.com/storage/storage-box/general/`, read 2026-10-22, which states "Each Storage Box comes with unlimited traffic"
- **Confidence:** documented

## What we believed

Two seed artefacts carried the same figure with the same framing. `TOP-FINDINGS.md` and
`CHEAP-PAID-FINDINGS.md` both said Hetzner's fair-use letter hits users at "50-100 TB/month" and
that a 30 TB per month load is "7-30x below" that threshold.

The number made Hetzner look risky. A 30 TB workload against a 50 TB threshold is a 1.7x margin,
which is not a margin at all for a plan that might grow.

## What we found

The primary letter reads 250 TB/month:

> "your traffic use, which currently averages above **250 TB/month** on some of your servers ...
> Although these servers include unlimited traffic, this is far above what we consider fair use
> ... we may choose to cancel your contract. (Please see 2.7 of our Terms and conditions)"

So the correct comparison is 30 TB against 250 TB, which is **8.3x below**, not 7 to 30x. The
direction of the error is more margin rather than less.

The 50 TB figure is real and it belongs to a different product. It is a dedicated-server
port-throttle rule, imported into a Storage Box argument where it does not apply. That is a
category error, and it made the strongest paid option in the corpus look weaker than it is.

The vendor's own product term is unambiguous and was re-read this session: "Each Storage Box comes
with unlimited traffic".

## How we found it

The seed's third review read the primary letter rather than the summary of it. This session
re-read the vendor documentation page and the pricing page: 116,243 bytes of HTML carrying the
four price literals 3.20, 10.90, 20.80 and 40.60 for 1, 5, 10 and 20 TB, which recomputes to EUR
2.03 per TB at the 20 TB tier.

## What it cost us

One purchase decision. At a 1.7x margin, a reader would look for a second paid option or accept
the free tier's fragility. At 8.3x, Hetzner is the only paid product in this corpus whose
unlimited claim survives the workload with room to grow.

The cost of the error was paid in the direction that made the recommendation weaker. That is the
rarer direction and it is worth naming, because the corpus's other corrections all moved numbers
down.

## What a future session should do differently

Read the primary letter before quoting a threshold, and check which product the letter is about.
A notice sent to dedicated-server customers and a notice sent to Storage Box customers are
different documents with different numbers, and the summary that conflates them is usually a
forum post.

And when a correction increases a number, say so as plainly as when it decreases one. The
temptation is to treat a favourable correction as a rounding fix and an unfavourable one as a
finding.
