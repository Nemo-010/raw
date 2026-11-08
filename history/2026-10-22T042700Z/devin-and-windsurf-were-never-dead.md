# Devin and Windsurf were never dead; a broker 404 was read as a vendor death

- **When:** 2026-10-22T04:27:00Z
- **Status:** corrected
- **Supersedes:** `dossier/coding-subs/devin.json` (`verdict: dead`, `confidence: unverified`); `dossier/coding-subs/windsurf.json` (same); `docs/coding-subs/README.md` §The dead ends and the comparison table; `docs/coding-subs/free/free-tier-of-paid-plan.md` §What did not work
- **Superseded by:** the same two records and the same two documents, rewritten on 2026-10-22
- **Evidence:** `devin.ai/pricing` read 2026-10-22T04:14:01Z (200, 582,848 bytes); `windsurf.com/pricing` the same minute (308, `Location: https://devin.ai/pricing`)
- **Confidence:** measured

## What we believed

Both records said `verdict: dead` and `confidence: unverified`. Devin's evidence entry
read "the read broker returned 404 with reason no-content; no plan name was present".
Windsurf's note read "the pricing URL is 404 to every extraction route while the product
is still sold ... the next session should try the app subdomain."

## What we found

**Devin is live.** `devin.ai/pricing` returns HTTP 200 with 582,848 bytes and a complete
ladder: Free USD 0, Pro USD 20 a month, Max USD 200 a month, Teams USD 80 a month plus
USD 40 a month per full dev seat. The Free card reads "Light quota to code with agents",
"Unlimited inline edits", "Unlimited Tab completions", and the page carries a
"Compare Plans Free $0/month Pro $20/month Max $200/month Team $80/month" row.

**Windsurf did not 404 and did not move to a subdomain.** `windsurf.com/pricing` returns
`HTTP/1.1 308 Permanent Redirect` with `Location: https://devin.ai/pricing`, and
`windsurf.com` itself 308s to `devin.ai/desktop`. The product was acquired or merged: the
brand, the host and the ladder are Devin's now, and there is no separate Windsurf price
list to find. The old note sent the next session after a subdomain that does not exist
and after a product that no longer has its own pricing.

**Both records were `dead` on a broken link rather than on evidence of death.** That is
the distinction the verdict vocabulary exists to carry, and both got it backwards.

## How we found it

One `curl -L` per host. The read broker had failed; the raw fetch answered on the first
try with no challenge and no JavaScript requirement, which is route 5 of the challenge
protocol in `METHODOLOGY.md` §7.

## What it cost us

The topic README told a reader Devin and Windsurf "returned no readable page", and the
free-tier document told them no row could exist. For a zero-budget requirement, removing a
live USD 0 tier and the cheapest end of the paid ladder from the decision surface is the
most expensive kind of error this topic can make. The staleness table also carried both
as "not read", which understated the gap instead of declaring it.

A third row in the same group, StepFun, failed the same way and is recorded separately in
`../2026-10-22T043000Z/stepfun-tier-restored.md`.

## What a future session should do differently

⛔ **A `dead` verdict needs evidence of death, not of a broken link.** Probe the host
before writing the verdict. A 404 on one path is a moved page and a 308 is a merge. Only
a host that answers nothing is dead, and only then does the word belong in the record.
⭐ The check costs one request and it is the difference between a finding and a fiction.
