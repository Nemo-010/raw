# The `reported` window is 14 days, and 323 compute records prove it

- **When:** 2026-10-22T04:40:00Z
- **Status:** decided
- **Supersedes:** nothing; this is the first policy decision about the `reported` rung
- **Superseded by:** `scripts/dossier/staleness.policy.json` `classes.reported.days`
- **Evidence:** `python scripts/dossier/staleness.py dossier/ --summary` reports 323 `compute` records at 20 days against a 14-day limit; the fixtures in `scripts/fixtures/staleness/` encode the same rule and all 25 selftest cases pass
- **Confidence:** measured

## What we believed

That the `reported` rung's 14-day window was a rule about forum posts. The
justification in the policy file says so: *"a forum post describes a moment, and
the operator may have fixed it."* Under that reading, the 323 `compute` records
carrying `confidence: reported` at 20 days are a false positive — they are
mechanically converted catalogue cards, not forum whispers, and 20 days is not
long for a price.

## What we found

The window is right and the records are correctly flagged. Two things settled it.

**First, the population is not what the rung was written for.** Those 323 records
rest on the `peli-cloud` seed pass of 2026-10-02: a single vendor page, read once,
by another session, twenty days ago. That is `reported` under the ladder's own
definition — a third party stated it — and the ladder's rule is that an inherited
number starts at `reported` until somebody here re-measures it. The records are
honest. The flag is honest. What is wrong is the assumption that they are
comfortable.

**Second, the alternative was worse.** An earlier fixer proposed treating them as
`documented` because they cite a vendor URL. That would raise 323 records a rung on
the strength of a page nobody in this repository opened, which is the one
direction the ladder forbids. The rung is correct; the work is outstanding.

## How we found it

`staleness.py` had a `fail_on_bucket` list in its policy that **no code read**.
It said only the `stale`, `rotten` and `dead` bands fail, while the code failed a
record the moment it passed its class window — two definitions of one word, and
the stricter one was invisible. The first attempt to reconcile them made the gate
green by loosening the rule, and the fixtures caught it: 3 of 4 planted defects
stopped being detected. The list was removed instead, and the policy now says what
the code does. A dial that does nothing is the same defect as a record that claims
a rung it did not earn.

## What it cost

One round trip and a reverted edit. The cost that matters is downstream: `compute`
cannot be called complete while 323 of its 405 records are twenty days past their
window, and the expansion plan's first step is now to re-read those pages rather
than to add providers.

## What a future session should do differently

**When a policy and its code disagree, the fixture is the arbiter.** The four
planted records in `scripts/fixtures/staleness/` encode the intended behaviour, and
they are the reason the loosening was caught within a minute. Any change to a
threshold must be run against them before it is believed.

**Do not tune a threshold to make a red gate green.** The red gate was correct. The
temptation was to widen `reported` to 30 days, which would have hidden 323 records
that genuinely need a re-read. A threshold is a claim about how fast the world
changes; widen it and you have claimed the world is slower, without evidence.
