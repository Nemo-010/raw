# CSC Allas and LUMI-O were `qualifies` in the table a reader scans first, and `fails-identity` everywhere else

- **When:** 2026-10-22T04:15:00Z
- **Status:** corrected
- **Supersedes:** `docs/storage/free/research-clouds.md` §The comparison and the two provider sections for CSC Allas and LUMI-O
- **Superseded by:** `docs/storage/free/research-clouds.md` §The comparison and §The four Tier-1 entries that are unreachable, and `dossier/storage/csc-allas-10-tib-default-per-project-s3-swift-on-ceph.json` and `dossier/storage/lumi-o-150-tb-allocated-per-lumi-project-by-default.json`
- **Evidence:** `.tmp/seed/storage-research/verify/csc-allas.json` and `verify/lumi-o.json`, both `verdict: fails-identity` and `confidence: high`; `https://docs.csc.fi/accounts/how-to-create-new-project/` (read 2026-10-22): a project needs a Haka or Virtu login or a home organisation with a CSC contract
- **Confidence:** documented

## What we believed

`docs/storage/free/research-clouds.md` shipped two table rows in its size-ordered comparison:

| provider | allocation | verdict |
| --- | --- | --- |
| CSC Allas | 10 TiB per project by default | `qualifies` |
| LUMI-O | 150 TB per project by default | `qualifies-with-caveat` |

The same document, forty lines below the table, said the opposite in prose: "That is a quote from
the vendor, and it makes the verdict `fails-identity` rather than a caveat." `gaps.md` and
`free/README.md` both recorded `fails-identity`. The records carried `qualifies` and
`conflicts: null`.

## What we found

**Four documents, three answers, one provider.** The seed's `table.md` said `qualifies`. The
seed's own `verify/csc-allas.json` and `verify/lumi-o.json` — independently verified round-1
files — said `fails-identity` with `confidence: high`. Three of the seed's prose documents agreed
with `verify/`.

**The quota is real.** 10 TiB per CSC project by default, 150 TB per LUMI project out of 30 PB,
both re-read on 2026-10-22 and both confirmed. That part is not in dispute and never was.

**The gate is what decides it.** A CSC project is created through MyCSC only by a holder of a
Haka or Virtu login or a home organisation with a CSC contract. LUMI-O exists only inside a LUMI
or EuroHPC project. Neither project admits a registrant without an institutional
affiliation, so neither is available at all, and a quota behind a door that cannot be
opened is worth zero — which is `METHODOLOGY.md` §4.2's rule stated as a verdict.

**The direction of the error was the expensive one.** The `qualifies` rows sat in the
size-ordered table at the top of the document, which is the table a reader scans. `qualifies`
there reads as "10 TiB available", which is the single most expensive misreading this topic
offers. The correct reading was in the prose below the table and in a different document.

**And the sentence promising `conflicts[]` was false.** `research-clouds.md` said "The record
carries all three claims in `conflicts[]`". Neither record carried the key at all, so a reader
who went to check found nothing to check.

## How we found it

An adversarial review of `docs/storage/` compared the verdict in the table with the verdict in
`gaps.md` and with the record, and found four places where the same provider carried two
different answers. The resolution follows the evidence rather than the count of documents: the
seed's `verify/` file is the only artifact in the corpus that records the eligibility question
as a answered question, and the CSC account documentation quoted in the document's own §The four
Tier-1 entries settles it independently.

## What it cost us

A wave, if anyone had acted on it. A reader who took `qualifies` and planned a 10 TiB tier would
have spent the time to discover the Haka requirement, then re-planned. The corpus's own dead-end
list exists to prevent exactly this, and the entry that would have prevented it was in a different
file.

## What a future session should do differently

**A table's verdict column must be generated from the record, not typed.** `docs/conventions/
README.md` already makes a table that restates a record a *generated* table owned by
`scripts/report/render.py`. The tables in `docs/storage/` are hand-typed views, and this is what
happens: the table drifts from the record and the prose drifts from the table.

**When a page states a provider's verdict twice, the second statement is not a confirmation.**
The prose and the table agreed with each other on nothing here; they were written from different
intermediate notes and never compared.

**`conflicts: null` is a claim.** A record that says it has no conflicts asserts that its sources
agree. When a document then promises the reader that the conflicts are in the record, the
assertion and the promise cannot both be true, and the promise is the one that fails.
