# StepFun's USD 9.99 tier was live, and a month-old date error hid the cheapest plan in the market

- **When:** 2026-10-22T04:30:00Z
- **Status:** corrected
- **Supersedes:** `dossier/coding-subs/stepfun-step-plan.json` (`verdict: trial-only`, `confidence: unverified`); `docs/coding-subs/README.md` §The comparison and §The staleness of this topic; `docs/coding-subs/paid/under-20.md` §What did not work; `docs/coding-subs/free/free-tier-of-paid-plan.md` §What did not work
- **Superseded by:** the same record and the same three documents, rewritten on 2026-10-22
- **Evidence:** `platform.stepfun.ai/docs/en/step-plan/overview.md` read 2026-10-22T04:14:01Z (200, 9,444 bytes)
- **Confidence:** documented

## What we believed

The record said StepFun's ladder "did not render" and set `verdict: trial-only`. The
topic README's staleness table said "StepFun USD 9.99 | 2026-09-07 pass, not re-read |
over 30 days | not a row in any table". `under-20.md` said "its page returned a 396-byte
shell today. Not a row."

## What we found

Two errors stacked, and either alone would have hidden the tier.

**The URL was the wrong one.** `www.stepfun.com/pricing` is a 2,262-byte marketing shell
with no plan name and no price, and it still is. The URL the seed itself cites,
`platform.stepfun.ai/docs/en/step-plan/overview.md`, returns 9,444 bytes of current
documentation with the full ladder:

| plan | monthly Credits | monthly | quarterly | yearly |
| --- | --- | --- | --- | --- |
| Flash Mini | 400M | USD 6.99 | USD 18.99 | USD 69.99 |
| Flash Plus | 1,600M | USD 9.99 | USD 26.99 | USD 95.99 |
| Flash Pro | 8,000M | USD 29 | USD 79 | USD 289 |
| Flash Max | 40,000M | USD 99 | USD 269 | USD 989 |

The page also states "Credits convert to payment at approximately USD 1 = 7M Credits",
so 1,600M Credits is about USD 228.6 of model usage for USD 9.99. It states two Base
URLs (`api.stepfun.ai/step_plan` for the Anthropic shape, `/step_plan/v1` for OpenAI
Chat Completions), names Claude Code, Trae, Cursor and OpenClaw as supported clients,
and says Step Plan carries no request-frequency limit.

**The date was wrong by a month.** There is no 2026-09-07 pass in the seed. The passes
are 2026-09-13, 09-20, 10-02, 10-06 and 10-07, and the StepFun row is in
`.tmp/seed/coding-subs/2026-10-07/data/vendor-sweep.csv`, line 13. The table dated the
row a month earlier than any pass that contains it, then used that age to dismiss the
reading as stale.

## How we found it

One fetch of the URL in the seed's own row, which the previous pass had replaced with
the vendor's marketing page. The suggestion to try it came from reading the seed CSV
rather than the document.

## What it cost us

At USD 9.99 for 1,600M Credits this is the cheapest plan per unit of work found in
either topic, and it was absent from every table for the length of one writing pass. The
topic's headline — that USD 10 of OpenCode Go is the only plan in the bracket publishing
both a ceiling and an endpoint — was false as written, because StepFun publishes both.
The claim is now stated as two plans, with StepFun the cheaper.

## What a future session should do differently

⛔ **Read the URL the evidence row cites, not the vendor's marketing root.** A vendor
usually has both, and the one a seed row cites is usually the one that carries the
numbers. ⚠ **And never date a row from memory of which pass "felt" like the one.** The
pass directories are on disk; a date that is not in one of them is a typo, and this one
cost the corpus its cheapest finding.
