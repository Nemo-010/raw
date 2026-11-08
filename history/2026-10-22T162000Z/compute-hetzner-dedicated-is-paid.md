# Hetzner's dedicated range publishes prices, so it is paid-only and not a qualifying tier

- **When:** 2026-10-22T16:20:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/hetzner-dedicated.json` verdict `qualifies-with-caveat`
- **Superseded by:** `dossier/compute/hetzner-dedicated.json` verdict `paid-only`; `docs/compute/paid/brokers-and-bare-metal.md`
- **Evidence:** vendor pages and campaign rules read 2026-10-22 through `scripts/broker/broker.sh`; the exact URLs and quoted sentences are in each record's `evidence[]`
- **Confidence:** documented

## What we believed

That the dedicated line qualified as a cheap paid option, and that its prices were behind a
script that no reader could extract.

## What we found

The AX matrix publishes the range: from EUR 59.00 a month excluding VAT for the AX41, an AMD
Ryzen 5 3600 on Zen 2 with 64 GB of DDR4 and two 512 GB NVMe drives, up to EUR 614 for the
largest model. Nothing about the line is free, and the price is not hidden.

## What it changes

The verdict becomes `paid-only`, which is what `docs/conventions/README.md` defines for a
product that was never free. The record keeps the price matrix as evidence, so a reader
comparing a dedicated box against a VPS has the figure.
