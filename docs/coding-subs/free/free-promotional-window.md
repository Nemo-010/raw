# Free while it lasts, and why none of it can be planned on

A promotional window is free while it lasts, with a published or unpublished end. It
differs from a free tier of a paid plan in one way that decides everything: the
vendor has not committed to it. The end may be a date, a capacity pool, a campaign,
or the word "limited time" attached to a product that is otherwise sold.

The rule this document applies: **refuse to compute a yield for a lane whose end is
unpublished.** A number divided by an unknown number of days is not a rate. So
nothing below carries a monthly capacity figure, and the reason is stated in the same
sentence as the offer.

The answer: **three OpenCode Go models are priced Free with an "Unlimited" monthly
limit marked limited time**, and they are the largest such window found
(`documented`, 2026-10-22). Everything else in this class is either a capacity pool
that empties without notice or a discount on a paid plan.

## The comparison

Sorted by how much is published about the offer. `End` is what the vendor says about
when it stops, and a dash there means the offer cannot be planned on at all.

| Provider | Offer | End | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| OpenCode Go | LongCat 2.5 Preview Free, Beam Free, MiniMax M3.1 Flash Free: unlimited, limited time | "limited time" | REST endpoint on a paid plan | card | trial-only |
| OpenCode Zen | 14 model ids priced Free | "limited time", and restricted to the OpenCode client | none: gated | email | fails-identity |
| Command Code | Ling 3.1 Flash, Ling 3.0 Flash Sante and Laguna S 2.1 at $0 input, output and cache | "while it lasts", "while capacity lasts" | plan API key | card | trial-only |
| Z.ai | GLM-5.3 and GLM-5.3-Flash included on every paid tier, with multipliers | not a promotion | REST | card | paid-only |
| Gemini API | gemini-3.8-flash free of charge on the Free Tier | no end stated, but no number either | REST | email | qualifies-with-caveat |
| NVIDIA build | a free trial tier at 40 rpm and 10,000 requests a day | trial only, production barred | REST | email | trial-only |

## OpenCode Go free models

OpenCode Go is USD 10 a month, and inside it three models carry an **Unlimited**
monthly limit with a "limited time" annotation: LongCat 2.5 Preview Free, Beam Free
and MiniMax M3.1 Flash Free (`documented`, `opencode.ai/docs/go`, read 2026-10-22).
The page also states that when a paid limit is reached, the free models remain
usable, so they are a floor rather than a bonus.

That is the clearest statement of a free window in this market: a paid plan, an
unlimited allowance on named models, and an end nobody has published. What it does
not do is survive the identity constraint. The free window requires a USD 10
subscription and a card, and the request has to reach the Go endpoint, which needs a
key from the console.

Two of the three are also region-limited. Beam Free is listed as unavailable in
twenty named countries and regions, including China, Russia and Belarus. Meta's
Muse Spark Contributor models on the same plan carry a separate geographic policy.

Evidence: `opencode.ai/docs/go` (read 2026-10-22): the per-model ceiling table with
Unlimited on three rows, and the note that free models stay usable past the paid
limit. Verdict: the largest free window found, behind a card, with no end date.

## OpenCode Zen free models

Zen prices 14 model ids at Free for input, output and cached read, each marked Free
or limited time (`documented`, `opencode.ai/docs/zen`, read 2026-10-22). The list
includes Big Pickle, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free and LongCat 2.5
Preview Free.

None of them is reachable from outside the OpenCode client. A bare HTTP request to
`opencode.ai/zen/v1/chat/completions` returns `403` with
`{"type":"FreeTierError","message":"OpenCode's free tier can only be used from
within OpenCode."}` (`measured`, 2026-10-22, twice, with two different
User-Agents). So the free tier is real, priced at zero, and worth nothing to a
script.

The related finding is that `space-bunny-free`, the one anonymous survivor on this
endpoint measured on 2026-10-02, returned 400 "Model is unavailable" on 2026-10-22.
Twenty days.

Evidence: `opencode.ai/docs/zen` (read 2026-10-22) for the price table; a live probe
of the endpoint for the 403. Verdict: free models behind a client gate, and the
survivor is gone.

## Command Code

Command Code lists three models at $0 input, $0 output and $0 cache: Ling 3.1 Flash,
Ling 3.0 Flash Sante and Laguna S 2.1 (`documented` from a 2026-10-07 capture,
`commandcode.ai/docs/resources/pricing-limits`). The terms are "while it lasts" and
"while capacity lasts", and Ling 3.0 Flash Sante carries 100 requests a day per
account resets at midnight UTC.

The row carries its 2026-10-07 date and was not re-read, so it is fifteen days old on
2026-10-22. The entry cost is also not $0: the deals require a Command Code plan, the
cheapest being Go at USD 1 a month plus an unstated processing fee, and a session
needs USD 1 of credits in the account.

The identity verdict for this lane is UNKNOWN, and that verdict is the finding: the
leaderboard scores the slug at II 41.0906 while the vendor's page does not say which
checkpoint or reasoning mode it serves. A free lane on an identity-unverified endpoint
cannot support a capability claim.

Evidence: capture `2026-10-07/sources/free-lanes/commandcode-pricing-limits.html`
(read 2026-10-07). Verdict: a real $0 lane behind a $1 entry, with no end date and no
established model identity.

## Gemini API

The Gemini API free tier is not a promotion and does not belong in this class on
that ground, but it is listed because it is the other side of the same question:
what does a vendor do when it gives capacity away. `gemini-3.8-flash` is "Free of
charge" for input and output on the Free Tier (`documented`,
`ai.google.dev/gemini-api/docs/pricing`, read 2026-10-22), and its limits are visible
only inside AI Studio, per project, resetting at midnight Pacific.

The vendor states that free-tier content is used to improve its products and
describes the paid tier as the one for production. That is a published trade rather
than a hidden one, which is more than any other row here offers.

Evidence: `ai.google.dev/gemini-api/docs/rate-limits` (read 2026-10-22): per-project
limits, midnight Pacific reset, and "Specified rate limits are not guaranteed".
Verdict: a durable free tier with no public number.

## NVIDIA build

The NVIDIA trial tier allows up to 40 requests a minute and 10,000 requests a day
with no card (`documented` from a 2026-10-07 capture). Ten thousand requests
a day is the largest published daily request allowance found anywhere in these two
topics.

It is a trial by the vendor's own wording, and the terms bar production use. A free
allowance that the vendor describes as "for limited trial purposes only" is a
promotion with a legal shape rather than a date, and it cannot be planned on for the
same reason.

Evidence: `build.nvidia.com/deepseek-ai/deepseek-v4.1-flash` (read 2026-10-07, not
re-read). Verdict: the largest daily request allowance found, and a trial.

## What did not work

- **Cerebras Code.** Every paid Code tier was sold out on 2026-09-13, which is a
  capacity failure rather than a price one. No live tier was found here.
- **Trae Pro's early pricing.** The USD 10 figure was a truncation artefact; it is
  withdrawn in `history/2026-10-22T032429Z/`.
- **"Unlimited, limited time".** This phrase appeared on three offers and is recorded
  as a term, never as a quota. A limit that is both unlimited and temporary cannot be
  converted into a rate in either direction.

## Chaining

Nothing here chains, by construction. A promotional window is the wrong thing to
build a stack on, and the only safe use is as an overflow for work that is already
runnable against a paid endpoint. The rule for a reader who finds one alive: use it,
record the timestamp, and do not write a plan that needs it tomorrow.
