# Coverage against a sandbox list was not coverage of the VPS market

- **When:** 2026-10-22T22:47:49Z
- **Status:** corrected
- **Supersedes:** `docs/compute/watchlist.md`, which stated that the market's names were "known" and that "what is missing is measurement, not breadth", on the strength of one corpus where 368 of 369 providers were covered
- **Superseded by:** `docs/compute/watchlist.md`, which now reports both diffs, and `docs/compute/paid/lowend-vps.md`, which carries the 114 providers the second diff found
- **Evidence:** the provider index at `https://vpspricetracker.com/providers`, read 2026-10-23, listing 128 providers and diffed against `dossier/compute/` by normalized name and slug
- **Confidence:** measured

## What we believed

That discovery was finished. A 369-card provider corpus had been fetched and 368 of its
providers already had a record, so the remaining work was to measure what existed rather than
to find more hosts.

## What we found

That corpus is a sandbox, browser, devbox and hyperscaler list. It does not cover the cheap
VPS market at all. `vpspricetracker.com` listed 128 providers, and **106 of them had no record
anywhere in the corpus**. The two lists overlap barely enough to make the first result look
like a general one.

A second error sat inside the count. The tracker diff matched provider names by substring, so
eight names were treated as covered when they were not, including `hostbrr`, which
`paid/micro.md` had been quoting by name with no dossier record behind it. Reading the record
rather than the name found them.

## What it changes

`compute` went from 962 to 1,076 records in one turn, and the topic's document count from 54
to 55. The floor did not move: `paid/micro.md` still holds it at USD 1.42 a month, because
every provider the tracker added is dearer than that, and every entry it found under USD 2 is
IPv6-only or NAT.

The rule this leaves behind is that a coverage claim needs the list it was measured against,
named in the same sentence. "368 of 369 covered" was true and was read as "the market is
covered", which is a different claim and a false one.
