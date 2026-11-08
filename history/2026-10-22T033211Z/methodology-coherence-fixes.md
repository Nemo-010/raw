# The evidence ladder had two rules, the staleness policy enforced neither, and a retracted AList denominator was published

- **When:** 2026-10-22T03:32:11Z
- **Status:** corrected
- **Supersedes:** `METHODOLOGY.md` sections 3.1, 3.6, 4.3, 5.3, 10.1 to 10.4 and 15; `docs/conventions/README.md` sections 5, 6.1, 6.3 and 9; `dossier/README.md` "The record"; `README.md` "Withdrawn claims"
- **Superseded by:** the same sections, as they now read
- **Evidence:** an adversarial review of both documents (`.tmp/work/review-method/REPORT.md`, 24 findings); `scripts/dossier/staleness.py` run against four planted fixtures; `scripts/gate.sh --root .` before and after; the seed's own correction table at `.tmp/seed/storage-research/FINAL-REPORT.md` row 21
- **Confidence:** measured for the script and gate behaviour, documented for the prose corrections

## What we believed

Three things, and each had a document behind it.

1. **The evidence ladder was one rule.** Section 3.1 said a record's class is "the class of the
   field its verdict depends on most"; the same section's signature line said "the weakest link
   sets the class", and its last paragraph said `confidence` is "the weakest rung among the
   fields that matter". `dossier/README.md` and the schema's field comment both said weakest.
   Three homes, two rules, and no check anywhere that could arbitrate.

2. **The staleness policy enforced the windows it stated.** Section 10.2 gave five per-class
   windows and section 10.3 a topic table, and said the shorter binds. The shipped
   `staleness.policy.json` had no class dimension at all, and `staleness.py` never read
   `confidence`. Nothing in the repository could see a record that had been re-dated.

3. **"Eight of nine AList instances" was the rule-3 headline.** Rule 3's failure paragraph
   carried it, and `README.md` repeated it.

## What we found

**The ladder.** Two honest readers computed different rungs for one record. Where a record's
quota was `measured` and its egress `inferred`, section 3.1's first sentence gave `measured` and
its second gave `inferred`. Section 3.6's own example then set `confidence: measured` on a
record whose quota came from a vendor page, so the example taught the rung the stated rule
forbade. The failure mode is the one the document names at section 13: a rung decision is
negotiable when two rules describe it, and a session picks the higher.

**The policy.** Four planted records settled it. A 40-day `reported` claim passed as `fresh` in
a topic with a 120-day window, because the class window did not exist in the data. A record
with `verified_at` set to today and its only evidence dated five weeks earlier passed as
`fresh`, which is the bulk touch section 10.1 forbids in prose and nothing detected. The gate
reported 51 records as stale on a corpus whose dates were only one day old, because an
unparseable date and a rotted claim were counted in the same column.

**The number.** The seed's own correction table, row 21, is titled "8 of 9 'writable' AList
instances" and reads: "ALIST-FINDINGS says eight advertised it and all eight refused; '8 of 9'
invents a ninth." The seed's brief carried the wrong figure and its findings file carried the
right one. The derived methodology inherited the brief. That is the defect section 13 calls
"the summary instead of the source", committed by the document that names it.

## How we found it

An adversarial review of `METHODOLOGY.md` and `docs/conventions/README.md` at pinned hashes,
which produced 24 numbered findings. This entry records the five that had already propagated
and the one structural defect. Every claim above was re-run here rather than taken from the
report:

- the conventions' section 6.1 example, extracted verbatim and passed to
  `validate.py --schema scripts/dossier/schema.json`: 11 errors, six of them the
  scalar-versus-object family;
- a real record with `binding` and `stale` written onto it: exactly two
  `additionalProperties` errors, which is what made section 4.3's requirement unwritable;
- `staleness.py` against four planted records at known ages: all four passed;
- `grep` for the retracted figure across the tree: two live occurrences, in `METHODOLOGY.md`
  and `README.md`.

## What it cost

The conventions' example is the shape every writer copies, and it did not validate. Fifty-one
earlier records wrote `verified_at` as a bare date because section 10.1 and the conventions
both prescribed one, and the schema rejects it. That is a wave of writer time going into a
format the documents got wrong, and it was caught by a reviewer rather than by the gate.

The staleness gap cost more quietly. Three hundred and fifty `compute` records were stamped
with a session date over twenty-day-old evidence and passed every gate run until the evidence
clock existed. Nothing about them changed except that the gate can now see them.

## What a future session should do differently

1. **A rule stated twice is a rule with two versions.** The ladder now has one statement, in
   section 3.1, and the other two homes point at it. When you add a rule that a document and a
   script both need, write it in one place and make the other a pointer.
2. **Run the document's own example through the document's own validator** before publishing
   either. The example is what a reader copies, so an example that fails the schema teaches the
   failure at scale. `scripts/SELFTEST.md` records the run.
3. **A policy that is written in prose and not read by a script is not a policy.** Section 10.2
   listed five windows for months while the script read none of them. When you write a window,
   threshold or allowance into a document, either put it in the data file the script reads or
   say in the same sentence that it is not enforced.
4. **Check a number against the correction table before you copy it.** The seed's brief and the
   seed's findings file disagreed, and the brief was the one with the retracted figure. Where a
   source has a correction table, read it first.
5. **A gate that reports a count should be asked what the count is made of.** `stale=51` on a
   one-day-old corpus was not rot; it was a date format. The summary line now separates
   "unparseable", "past its window" and "re-dated", and the fix took less time than reading the
   number took to disbelieve.
