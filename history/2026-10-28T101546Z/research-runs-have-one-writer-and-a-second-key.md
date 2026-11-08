# Research runs now have one writer and a second key, and the first four runs found ten defects in the harness

- **When:** 2026-10-28T10:15:46Z
- **Status:** decided
- **Supersedes:** `AGENTS.md` §4 as written before 2026-10-28, where a parent agent dispatched up to 30 lanes that each wrote `dossier/` directly
- **Superseded by:** `docs/research-protocol.md`, `scripts/research/README.md`, and the `contradictions` check in `scripts/gate.sh`
- **Evidence:** pull requests #5, #7, #14 and #15 (one per run, each merged on a green gate and green CI); pull requests #6 and #9 (harness fixes); `scripts/rq report RUN` for runs `20261028-0424-verify-compute`, `20261028-0425-expand-compute`, `20261028-0913-verify-compute` and `20261028-0433-expand-inference`
- **Confidence:** measured

## What we believed

That lanes writing records in parallel, with a parent agent reading their summaries and repairing collisions,
was a workable way to research at width. Earlier waves show the cost: 4% to 13% of slugs in a wave were written
by two or more lanes, nine of twelve wave-landing commits needed a repair commit within an hour, and one compute
day produced 68 lane reports, about 569 KB, for one parent to read.

## What we found

A run now has one writer. Lanes propose changes with a capture of the page and an exact quote; `scripts/rq
integrate` applies them on a run branch with compare-and-set on the old value, the rung order, dedupe, the schema
and the record rules, and writes a ledger line with the old value. A second model re-reads a sample of each
unit's claims from the captures. A unit above the threshold is undone from its ledger and queued again. A run
lands as a pull request, and only when no gate check fails that passed on main. The harness calls no model, so
the parent and the lanes can be any agent in any tool.

Four runs went through it on 2026-10-28:

| run | units of work | new records | claims audited | unsupported | units undone | pull request |
| --- | --- | --- | --- | --- | --- | --- |
| verify compute (stale and inherited records) | 4 | 0 | 94 | 10 (10.6%) | 2 | #5 |
| expand compute (eleven LowEndTalk vendors) | 5 | 11 | 28 | 1 (3.6%) | 0 | #7 |
| verify compute (the two undone units, again) | 2 | 0 | 56 | 4 (7.1%) | 1 | #14 |
| expand inference (no-card rate limits) | 20 | 44 | 289 | 14 (4.8%) | 3 | #15 |

Over the four runs, 467 claims were re-read by a second model and 29 were unsupported (6.2%). The fourth run was
started by a parent agent given one line and nothing else: "Expand inference free LLM inference APIs that answer
without a card, with their rate limits". It read `AGENTS.md` and `docs/research-protocol.md`, planned nine
units, ran two reconcile rounds and two re-runs, and landed 44 records with a follow-up issue (#16) for what it
could not settle.

The runs also found ten defects in the harness itself, all fixed in #6 and #9:

1. Lint did not run the record rules, so a lane that set fields without a `confirm` (rule C10) or wrote
   narrative into a draft field (C20) learned it only from a rejection at integration.
2. Lint and briefs read records from the main checkout, so a reconcile unit on a record added earlier in the
   same run was refused.
3. Dedupe treated any shared deep URL as the same offer. A forum list page cited by four vendors merged three of
   them into the fourth. A shared page now counts only on the vendor's own domain.
4. The audit planner walked paths with a split on dots and missed list indexes, so claims read `null`.
5. The audit planner paired each claim about a new record with its first evidence row only.
6. The audit planner audited values the lane itself had marked `unverified`.
7. Unsupported claims of a unit that passed its audit went to a folder nothing read. They are conflicts now.
8. The Wilson bound was applied to audits that read every claim of a unit, where nothing is extrapolated, so one
   wrong claim in eleven undid four new records. A census audit now fails on the observed rate alone.
9. The undo did not remove list items a unit had appended.
10. A run that added `documented` records could not land, because no document cited them. `rq land` now merges
    the current main into the run branch and re-renders the generated tables before it compares the gate.

## How we found it

By running real units, not fixtures. Each defect surfaced as a rejection, an undo, a red gate or an audit
verdict that a person then traced to the harness. Defect 3 was the exception: no check caught it, and it was
found by reading why a discovery unit reported "corroborated 3" for vendors the work queue said were in no
record.

## What it cost us

Two re-integrations and one re-planned audit in the second run, and one landing attempt refused by the gate.
The two records behind the red `staleness` check (`compute/tencent-cnb`, `compute/baidu-ai-studio`) are still
stale: their unit failed its audit twice, and two of the four failures the second time were a schema gap, not a
misread. `free_tier.unit` has no value for core-hours or server time (issue #13).

## What a future session should do differently

Give a parent agent the one line and let it follow `docs/research-protocol.md`; do not add context to a lane's
instruction. Read `scripts/rq report RUN`, not lane output. When a count looks wrong, such as "corroborated" for
a provider the corpus lacks, read the ledger lines of that unit before landing: the dedupe is the one decision
in the integrator that no later check re-examines. Settle issue #13 before the third attempt at the CNB, Baidu
and SimpFun unit.
