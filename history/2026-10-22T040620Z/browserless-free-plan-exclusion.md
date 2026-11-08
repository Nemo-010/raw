# Browserless was excluded from two documents on a premise the live page contradicts

- **When:** 2026-10-22T04:06:20Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/browserless.json` (`verdict: paid-only`, "USD 350 a month, there is no free lane"), `docs/compute/free/agent-browser-hosts.md` §What did not work, `docs/compute/paid/agent-browser-hosts.md` §What did not work
- **Superseded by:** the same files, and the rows now carrying a free allowance
- **Evidence:** `browserless.io/pricing` (read 2026-10-22): `No card required`, `Free`, `$0/month`, `1k units/month`, `2 max concurrent browsers`, `2 min. max session time`, and `A "Unit" is a block of browser time of up to 30 seconds per browser connection`
- **Confidence:** documented

## What we believed

Browserless sold nothing below USD 350 a month. Both browser documents listed it
under "what did not work" and the record was `paid-only`, justified in one
sentence: "the entry plan is USD 350 a month. There is no free lane."

## What we found

The page has a **Free plan at USD 0/month with no card**, 1,000 units a month, 2
concurrent browsers and a 2-minute session cap. The paid ladder starts at
Prototyping, USD 25 for 20,000 units, then Starter at USD 140 for 180,000. The USD
350 tier is the fourth rung, not the entry price.

1,000 units at up to 30 seconds each is 8.3 browser hours a month, and the
consumer-connection proxy draws from the same pool at 6 units per MB, so one gigabyte of
proxied traffic is 6,144 units, or six months of the whole free allowance.

## How we found it

The record's rung was `documented` and its single evidence entry read "no free
tier on the card; the cheapest plan is USD 350 a month" dated 2026-10-02. That is
a catalogue-card read, not a page read, so the rung was wrong before the value
was: a card read is `reported`. The review treated the rung mismatch as the entry
point and fetched the page.

## What it cost us

A live free tier in a class where free tiers are scarce, excluded from both
documents that rank that class. The same check found three more rows excluded on
premises that had changed: Firecrawl (1,000 free credits a month, no card),
Cloudflare Browser Rendering (10 minutes of browser time a day on Workers Free),
and Browserless itself. Firecrawl was described as having "no free browser tier"
and Cloudflare as "paid past the plan", and neither sentence was true of the page.

## What a future session should do differently

⭐ **"No free lane" is a claim about a page and needs a page.** It was written
from a card on a record marked `documented`. A card cannot establish an absence,
because the absence of a row is exactly what a card does not record.

⚠ **Audit the exclusions, not only the inclusions.** A provider wrongly included
produces a bad recommendation and a reader notices. A provider wrongly excluded
produces nothing at all, and the only way to find it is to re-check the premise
that removed it. Every "what did not work" list in this repository is unverified
in that direction until somebody re-reads it.

⚠ **The exclusion reason is where the stale premise hides.** Four of the nine rows
in `free/agent-browser-hosts.md`'s comparison rested on a card rather than a page,
and the three that were wrong were all in the "what did not work" section rather
than the table. A table row that says `not read` is honest; a paragraph that says
"there is no free lane" is not, and reads the same either way.
