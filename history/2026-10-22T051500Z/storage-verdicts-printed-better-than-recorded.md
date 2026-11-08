# Forty-nine sections printed a better verdict than their record, and the documents were the defect

- **When:** 2026-10-22T05:15:00Z
- **Status:** corrected
- **Supersedes:** the `Verdict:` line and the comparison-table verdict cell of the 49 sections named below, in 17 documents under `docs/storage/`
- **Superseded by:** `dossier/storage/<slug>.json` `verdict` for each, now printed by the document; the policy is `.tmp/work/fx-storage-residual/VERDICT-POLICY.md`
- **Evidence:** `dossier/storage/*.json` `extras.seed_verdict[]` (which seed wave said what) and `extras.conflicts[]` (both readings); audit at `.tmp/work/fx-storage/rung_join.py`, 418 sections, 0 rung mismatches and 0 verdict disagreements after the change
- **Confidence:** documented

## What we believed

The topic carried 49 sections whose stated verdict differed from their record's, and the working
assumption was that these were the seed's own disagreements, faithfully surfaced: `conflicts[]`
carried both readings with `resolution: null`, no document picked a winner, and `gaps.md` listed them
as open. The brief for this pass offered a second reading of the same fact — that a document stating
which of two seed verdicts it believes is correct behaviour, not a defect.

## What we found

The second reading does not apply, because **no document states which reading it believes**. A search
of each of the 49 sections for any marker of adjudication returns nothing: no section says "the seed
gave two verdicts", "an earlier wave said", "I take the stricter one", or anything else. Each prints
a bare `Verdict: \`qualifies\`` over a record that says `fails-quota`. That is not a second opinion;
it is a stale view.

The direction settles it. In **49 of 49** the document prints a *better* verdict than the record:
21 print `qualifies-with-caveat` over `fails-quota`, 13 print `qualifies` over
`qualifies-with-caveat`, 6 print `qualifies-with-caveat` over `fails-egress`, 3 print
`qualifies-with-caveat` over `fails-identity`, 2 print `qualifies` over `fails-identity`, 2 print
`qualifies-with-caveat` over `trial-only`, and one each print `qualifies` over `fails-egress` and
over `fails-quota`. **Zero print a worse one.** A rule permitting a document its own reading would
make all 49 over-recommendations, and 21 of them would tell a reader that a provider qualifies when
the record says it fails on quota.

The records' verdicts are also the *later* reading. Each record keeps `extras.seed_verdict[]` as
`{value, area}`; in 49 of 49 the record's verdict is the later entry and the document's is an
earlier one. Borealis is the clearest: rows in areas `D/D11` and `D/D2` say `qualifies` and
`qualifies-with-caveat`, and the later `E/E16` row says `fails-identity`, which is the wave that read
the infrastructure document and found "Non-affiliated accounts are explicitly read-only until a
collection administrator grants permission." The optimistic document rests on a row that never found
that sentence.

The cause is one layer up. The seed's `consolidate.py` ranks verdicts `qualifies`=0 (best) to
`fails-quota`=5 (worst) and sorts by that rank, so its `table.md` was built to surface the most
favourable reading of each provider. The documents inherited the table's reading; the records did
not.

## How we found it

Mechanical, not by reading. `python .tmp/work/fx-storage/rung_join.py` joins every section to the
record it cites and compares the printed verdict with the record's. It reported 50 disagreements. One
of those was not a seed conflict at all: the `OVHcloud Cold Archive` section cites **two** records,
and the join took the first citation, which is the Standard record. The Cold Archive record says
`qualifies` and the document was right. The join now prefers, among several cited records, the one
whose provider name explains the heading; the count fell to **49**, which is the figure the brief
carried.

## What it cost us

A wrong recommendation, 49 times over, and the review round spent deciding whether the documents or
the records were at fault. The expensive part was not the edit — 49 `Verdict:` lines and 47 table
cells, all verdict-only, verified by a diff that permits no other change — but the decision, which
had been deferred once already on the grounds that resolving it needed evidence the session did not
have.

It did not need new evidence. It needed the comparison of the record's verdict against the order of
its own `extras.seed_verdict[]`, which was in the record the whole time and takes one line to read.

## What a future session should do differently

**When two readings disagree, check which is later before checking which is better.** The record's
`extras.seed_verdict[]` is ordered provenance and it settles precedence for free. A conflict is not
symmetrical just because both sides are written down.

**A `conflicts[]` entry with `resolution: null` is a decision that has not been made, not a fact that
cannot be decided.** Forty-nine of these sat as if they were unanswerable. They were answerable on
the ordering alone. Resolve them when the evidence is in front of you, and leave `null` only where a
probe is genuinely required — the Harvard Dataverse quota question still is, because three endpoints
return three answers and only a deposit attempt would settle it.

**A document may print a number and its rung; it may not print a conclusion the record's fields do
not support.** A verdict is drawn from the quota, identity, egress and retention fields, not asserted
beside them. The 49 records were unchanged in `verdict` by this pass, which is the check that the fix
went the right way.
