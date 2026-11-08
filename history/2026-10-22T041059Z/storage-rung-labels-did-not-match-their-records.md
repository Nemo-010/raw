# The rung beside a provider was the rung we wished it had: 405 of 405 sections printed a class their own record did not carry

- **When:** 2026-10-22T04:10:59Z
- **Status:** corrected
- **Supersedes:** every `docs/storage/**/*.md` provider section carrying the sentence "That is the record's own wording", and `docs/storage/README.md` §Provenance of the numbers on this page
- **Superseded by:** the same sections after this entry, and `docs/storage/README.md` §Provenance of the numbers on this page
- **Evidence:** `.tmp/work/fx-storage/rung_join.py` joined all 415 `###` provider sections to their records through the section's `Evidence:` URL; `.tmp/work/fx-storage/fix_rungs.py` applied the correction; `dossier/storage/` holds 1,705 records
- **Confidence:** measured

## What we believed

Every provider section ended its quoted block with one sentence naming the source and its class:

> That is the record's own wording (`documented`, 2026-10-21).

The sentence was true about the *wording*: the block is the record's own `free_tier.stated`
text verbatim. The class beside it was not read from the record. It was written by hand, once
per section, and it said `documented` wherever the writer believed the claim was solid.

`docs/storage/README.md` stated the consequence in prose: "The 21 records marked `measured` were
re-run on 2026-10-22 against the live service; the rest carry `documented` from a page the seed
read on 2026-10-21."

## What we found

Three numbers, all wrong in the same direction.

**No record in this topic was `measured`.** The distribution over 1,705 records was `reported`
1,648, `inferred` 33, `documented` 23, `unverified` 1. Zero `measured`, at a moment when the
other ten topics held 86 between them. So the README's 21 was not a stale count; it counted
something that never existed in the records.

**1,648 of 1,705 records were `reported`, not `documented`.** The dossier pass converted the
seed's 91 dossiers mechanically and 832 records say so in their own `confidence_note`: *"no page
was read for this record in the storage-dossier pass."* A `reported` record cannot support a
`documented` sentence, because per `METHODOLOGY.md` §3.1 the record's class is the weakest rung
among the fields its verdict depends on, and per §3.5 one claim carries one class in the sentence
that states it.

**The join found 405 of 415 sections disagreeing with their record** — 365 printed `documented`
over `reported`, 14 printed `documented` over `inferred`, 17 printed `measured` over `documented`
or `reported`, and 9 printed `documented` correctly by accident. Two of the topic's own documents
had already noticed the rule and applied it once each (`free/ephemeral-hosts.md`, "read off the
record's own text (`inferred`)"), which is how we know the writer knew it.

The cause is not carelessness at the sentence. It is that the class was assigned by the document
author from memory of how the research felt, while the record was assigned by a converter from
what had actually been read. Two assigners, one fact, no reconciliation. That is the same failure
`METHODOLOGY.md` §3.1 exists to prevent, at scale.

## How we found it

A script, because a human cannot hold 415 sections. `rung_join.py` parses every `###` section,
takes its `Evidence:` URL as the join key against every record's `evidence[].url` and
`free_tier.source_url`, and falls back to provider-name and quoted-text matching where the seed
produced duplicate records for one provider. `fix_rungs.py` then rewrites the one sentence, and
only that sentence.

Two corrections inside the correction, both worth recording because they would have produced a
plausible wrong answer:

- **The seed holds duplicate records for one provider** — a revisit, a paid variant, a per-tier
  split — and they share an evidence URL. A pure URL join picked the wrong one 13 times. The tie
  is broken by matching the section's quoted block against the record's own stated prose.
- **A date is not a class.** 13 sections carried a date that did not match any date in the
  record's `evidence[]`. The date is now taken from the record too.

## What it cost us

This is the most expensive kind of error this corpus can make, and it is the one that does not
announce itself. `METHODOLOGY.md` §3.1 is the rule a reader uses to decide how hard to check a
number. A `documented` label over a `reported` record tells that reader the page was read and
quoted. It was not. The reader then spends their own time re-reading a page we told them we had
already read, or — worse — does not, and trusts a number whose source we never opened.

The second cost is the one that hides behind the first: 61 `measured` marks in the prose were
carried by 0 measured records, so every one of them either earned a record that does not carry the
rung or was a claim that nothing in this repository tested.

## What a future session should do differently

**A rung is a lookup, never a hand-typed string.** If a sentence states a class, the class comes
from the record, and a script that compares the two runs before the commit. `METHODOLOGY.md` §9.4
says the mechanical half is a script's job; this defect is what that sentence is about.

**Write the record first and the sentence from it.** The mechanical conversion produced a record
whose class was honest and a document whose class was aspirational, in that order, and nobody
compared them. The comparison is 30 lines of Python and it should have run on the first commit.

**When a topic reports zero records of a class the other topics report dozens of, that is a
finding about the pass, not about the topic.** Storage reported 0 `measured` while netdisk-pan
reported 42. Nobody looked at the row in `BRIEF.md`'s coverage table, and the doc prose quietly
supplied 61.
