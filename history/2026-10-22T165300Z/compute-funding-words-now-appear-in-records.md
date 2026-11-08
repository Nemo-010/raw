# The claim that no compute record names its funder stopped being true

- **When:** 2026-10-22T16:53:52Z
- **Status:** corrected
- **Supersedes:** `docs/compute/economics.md`, the sentence "the words `sponsored`, `investor`, `donation` and `venture` appear zero times in all 619 records"
- **Superseded by:** `docs/compute/economics.md`, which now tests the claim and records that it fails
- **Evidence:** `grep -rli` over `dossier/compute/*.json` on 2026-10-22, returning 10 records for `sponsored`, 9 for `investor`, 3 for `donation` and 9 for `venture`, 28 distinct records in total
- **Confidence:** measured

## What we believed

That the funding model behind a free compute tier was never stated in the records. The page
used that absence as its reason for being mostly inference, and the absence was true of the
619 records that existed when the sentence was written.

## What we found

The later passes added records that state a funder outright. `aicrowd` sells a "sponsored
credit pool". `aws-activate-portfolio` is gated by an Org ID that an investor issues.
`compound-reverie-grants` is reviewed by a venture firm's partners. `boxybsd` answers the
donation question by refusing donations. Twenty-eight records now contain at least one of the
four words, and most of those carry it in a programme name, such as the Thiel Fellowship,
Emergent Ventures or Hub71.

## What it changes

The argument survives and its strongest sentence does not. A reader can no longer be told the
words never occur; they can be told that 28 records mention a funder and the rest still name
none. The same pass corrected three stale denominators in the topic, which had been written
against a 619-record tree and now sit at 957: the clock census in `the-clock.md` and
`README.md`, the durability census in `dev-environment-long-tail.md`, and the egress census in
`gaps.md`, `paid/README.md` and `free/regional-clouds.md`. The clock census also carried an
arithmetic error, printing 34 where its own two components sum to 35.
