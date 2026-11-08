# Modal's free credit resets monthly, so it is an allowance and not a trial

- **When:** 2026-10-22T15:02:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/modal.json` evidence and `binding_note`
- **Superseded by:** `dossier/compute/modal.json` verdict stays `qualifies-with-caveat`, with the reset named as the constraint
- **Evidence:** vendor pages read 2026-10-22 through `scripts/broker/broker.sh read`; the exact URLs and quoted sentences are in each record's `evidence[]` and in the body below
- **Confidence:** documented

## What we believed

That Modal's free credit was a one-time trial, on the strength of an academic grant whose
terms say credits are granted once per conference and expire when submission results are
final.

## What we found

`https://modal.com/pricing`, read 2026-10-22: "Starter has no monthly fee and includes $30 of
compute (GPUs, CPUs, Memory) per month."

The academic grant and the Starter plan are two different programmes. The one-time terms
belong to the grant, which is a separate record; the Starter credit resets every month.

## What it changes

The verdict does not move, and the record now cites the reset rather than a trial clock. That
matters because a reader planning a monthly batch job needs to know the allowance returns,
while a reader planning a single large run needs to know it does not accumulate.

## The transferable point

"Credits are granted once" and "credits are included per month" are opposite facts about the
same product family. A record that quotes one while describing the other costs a reader a
month of planning.
