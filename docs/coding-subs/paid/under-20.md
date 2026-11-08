# What USD 20 buys, and which of those plans a script can drive

USD 20 a month is the entry point of this market and the price at which four vendors
have converged from different directions: Anthropic Pro, Cursor Premium, Kiro Pro and
Trae Pro. A fifth, Copilot Pro, sits at USD 10 and a sixth, OpenCode Go, at USD 10.
The convergence is not a coincidence and it is not a price: each of those plans
meters something different, and the same USD 20 buys between 1,000 credits and an
unstated multiple of an unstated baseline.

The answer: **two plans in this bracket publish both a ceiling and the endpoint that
spends it, and StepFun Flash Plus is the cheaper of the two** (`documented`,
2026-10-22). At USD 9.99 it buys 1,600M Credits, about USD 228.6 of model usage at the
vendor's own 7M-to-the-USD conversion, on two published Base URLs. OpenCode Go at USD 10
publishes a per-model dollar ceiling without a credit conversion. For an editor-bound
agent, Copilot Pro at USD 10 and Claude Pro at USD 20 are the two with a CLI and a
working free tier underneath.

## The comparison

Sorted by price. `Meters` is the unit the allowance is stated in, which is the axis
that makes the column beside it incomparable. `Programmatic` is the fifth axis and
the one that decides the answer.

| Provider | Price a month | Meters | Allowance | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| StepFun Flash Mini | USD 6.99 | Credits, 7M to the USD | 400M Credits, about USD 57.1 of usage | REST, OpenAI and Anthropic shapes | card | qualifies-with-caveat |
| Cursor Plus | USD 8 | one weekly pool | "Base" | CLI | email | qualifies-with-caveat |
| StepFun Flash Plus | USD 9.99 | Credits, 7M to the USD | 1,600M Credits, about USD 228.6 of usage | REST, OpenAI and Anthropic shapes | card | qualifies-with-caveat |
| GitHub Copilot Pro | USD 10 | credits plus unlimited completions | USD 15 of AI Credits | CLI | email | qualifies |
| OpenCode Go | USD 10 | a dollar ceiling per model | USD 15 to USD 80 a model | REST per family | card | qualifies-with-caveat |
| Z.ai Lite | USD 18 | credits with a published formula | 2,000 per five hours, 10,000 weekly | REST | card | qualifies-with-caveat |
| Claude Pro | USD 20 | a multiple of an unstated baseline | "more usage" than Free | CLI | card | qualifies-with-caveat |
| Kiro Pro | USD 20 | credits | 1,000 credits | none | email | qualifies-with-caveat |
| Trae Pro | USD 20 | a dollar balance | USD 20 of usage | none | email | qualifies-with-caveat |
| Cursor Premium | USD 30 | one weekly pool | "4x Plus" | CLI | email | qualifies-with-caveat |

## GitHub Copilot Pro

Copilot Pro is USD 10 a user a month and adds unlimited code completion, the cloud
agent, code review, third-party agents including Claude Code and Codex, model
selection and USD 15 a month in GitHub AI Credits to the free tier
(`documented`, `github.com/features/copilot/plans`, read 2026-10-22).

The allowance is now stated in two units at once: "unlimited" for completion and a
dollar figure for agent work. That split is honest and it is the shape the whole
market is moving to, because completion is cheap per event and an agent turn is not.
A reader who only wants completion gets an unlimited allowance for USD 10.

Evidence: `github.com/features/copilot/plans` (read 2026-10-22): Pro is USD 10 with
USD 15 of credits, Pro+ USD 39 with USD 70, Max USD 100 with USD 200. Verdict: the
cheapest plan in this market with a CLI and an unlimited component.

## OpenCode Go

OpenCode Go is USD 10 a month and its usage limits are **monthly dollar amounts per
model**, with the 5-hour allowance at 20 per cent of the monthly figure, the weekly
at 50 per cent and the month at 100 per cent (`documented`, `opencode.ai/docs/go`,
read 2026-10-22).

The ceilings vary: 16 of Go's 36 per-model ceilings are USD 15, 13 are USD 60, two
are USD 30, two are USD 80 and three are Unlimited for a limited time. Token prices are
identical between Go and Go Plus, so Go Plus at USD 40 buys a higher ceiling on the same
rates rather than a discount.

The page also publishes an **estimated request count per model**, not a request cap. It
prints the assumed token shape each estimate uses, for example GLM-5.3/5.2 at 700 input,
52,000 cached and 150 output tokens per request, under the sentence "The estimates use
the following token counts per request; actual usage varies" (`opencode.ai/docs/go`, read
2026-10-22). Those figures are a modelling assumption, and a workload whose prompts are
longer than the assumption meets its monthly dollar ceiling sooner. The page states no
per-request limit at all.

The endpoints are published per model family:
`opencode.ai/inference/go/openai/v1/responses`,
`opencode.ai/inference/go/anthropic/v1/messages` and
`opencode.ai/inference/go/google/v1beta/models/`. A reader can point a client at one
without an SDK.

Evidence: `opencode.ai/docs/go` (read 2026-10-22): the per-model ceiling tables, the
20/50/100 per cent window split, the 24 per-model token shapes behind the request
estimates, and the endpoint list. Verdict: the only plan here whose ceiling and endpoint
are both published.

## Claude Pro

Claude Pro is USD 20 a month, or USD 17 a month billed annually at USD 200 paid up
front, and it is the cheapest Anthropic plan that includes Claude Code
(`documented`, `anthropic.com/pricing`, read 2026-10-22). Max is "From $100" with a
choice of 5x or 20x the usage of Pro per five-hour session, and carries USD 100 to
USD 200 a month in API credits.

No tier publishes a usage number. The page says "more usage" on Pro and "5x or 20x
more usage than Pro" on Max, which means the unit of the entire ladder is an
unstated baseline. A reader cannot convert Pro into tokens, and neither can a
vendor-side comparison, because the baseline is not fixed.

The plan's advantage is that Claude Code is a CLI and a script can drive it, and its
disadvantage is that the quota it draws on is invisible until it stops.

Evidence: `anthropic.com/pricing` (read 2026-10-22): Pro USD 17 annual or USD 20
monthly, Max from USD 100 with a 5x or 20x choice. Verdict: the reference plan in
this market and the one with the least published about its allowance.

## Kiro Pro

Kiro Pro is USD 20 a user a month for 1,000 credits with access to premium models
and add-on credits at USD 0.04 each (`documented`, `kiro.dev/pricing/`, read
2026-10-22). Pro+ is USD 40 for 2,000, Pro Max USD 100 for 5,000 and Power USD 200
for 10,000.

The add-on price is the useful number: USD 0.04 a credit means the USD 20 plan's
1,000 credits are worth USD 40 of add-on purchases, so the plan carries a discount
against its own top-up rate. That is the only place where this ladder exposes a
rate, and it is worth having.

What the page does not say is what a credit buys. Without that, the ladder ranks by
price and not by capability.

Evidence: `kiro.dev/pricing/` (read 2026-10-22): five tiers and the USD 0.04 add-on
rate. Verdict: a clean ladder whose unit is undefined, bound to an editor.

## Trae Pro

Trae Pro is USD 20 a month for USD 20 of usage, all models, unlimited autocomplete
and up to ten concurrent cloud tasks (`documented`, `www.trae.ai/pricing`, read
2026-10-22). Pro+ is USD 60 for USD 60 of usage and fifteen tasks, Ultra USD 200 for
USD 200 and twenty tasks.

Each allowance equals the price, which makes Trae the one plan here that can be read
as a prepaid balance: a reader gets exactly the money back in usage and pays nothing
for the editor. The only premium is the concurrency limit, which rises with the
tier.

Evidence: `www.trae.ai/pricing` (read 2026-10-22): three paid tiers, each with a
usage allowance equal to its price. Verdict: an honest prepaid balance in a product
that no script can reach.

## Cursor Premium and Plus

Cursor's ladder is now The X Subscription: Free at USD 0, Plus at USD 8, Premium at
USD 30, Super at USD 100 and Ultra at USD 200, with annual prices of USD 80, 300,
1,000 and 2,000 (`documented`, `cursor.com/docs/models-and-pricing`, read
2026-10-22). Each paid plan includes one weekly usage pool for Cursor models, shared
across Cursor, the CLI, cloud agents and the Grok apps.

Every allowance is stated relative to Plus: "Base" on Plus, "4x Plus" on Premium,
"15x Plus" on Super, "50x Plus" on Ultra. So the ladder's unit is again an unstated
baseline, and the only absolute numbers on the page are prices.

Plus at USD 8 is notable for what it removes: no Auto, no cloud agents, no
automations, no third-party models and no own API keys, and Cursor's own models run
at fixed settings. It is the cheapest tier and the most restricted.

Evidence: `cursor.com/docs/models-and-pricing` (read 2026-10-22): the five tiers,
their prices and the shared weekly pool. Verdict: a repriced ladder with no
published pool size, and the legacy mapping in
`history/2026-10-22T032428Z/`.

## Z.ai Lite

The GLM Coding Plan's Lite tier starts at USD 18 a month and carries 2,000 five-hour
credits and 10,000 weekly credits (`documented`, `docs.z.ai/devpack/overview`, read
2026-10-22). Pro carries 12,000 and 60,000, Max 28,000 and 140,000.

Z.ai publishes the credit formula: model credits are (input tokens times input
multiplier, plus cached input times cached multiplier, plus output times output
multiplier) divided by 10,000. For GLM-5.3 the multipliers are 6.9, 1.7 and 24, and
for GLM-5.3-Flash they are 2.3, 0.56 and 8.

That formula is the only published path from a plan to a token count anywhere in
these two topics. It still needs the prompt-to-completion ratio, which the workload
supplies rather than the vendor, so a converted figure is an estimate and would be
labelled as one.

Evidence: `docs.z.ai/devpack/overview` (read 2026-10-22): the credit allowances per
tier, the formula and the per-model multipliers. Verdict: the most convertible quota
in the market, and the Pro and Max prices are not readable.

## StepFun Step Plan

Step Plan has four tiers and the entry is the cheapest plan found in either topic:
Flash Mini at USD 6.99 for 400M Credits, Flash Plus at USD 9.99 for 1,600M, Flash Pro
at USD 29 for 8,000M and Flash Max at USD 99 for 40,000M (`documented`,
`platform.stepfun.ai/docs/en/step-plan/overview.md`, read 2026-10-22).

The page states the conversion: about USD 1 buys 7M Credits. So 1,600M Credits is
**about USD 228.6 of model usage for USD 9.99**, which makes this the largest ratio of
allowance to price in this bracket. The allowance is denominated in Credits and spent
per model at the model's own rate, so the conversion is the vendor's and the token count
is not published.

Three properties decide whether it fits. **The interface is published**: two
Base URLs, `api.stepfun.ai/step_plan` for the Claude Code and Anthropic SDK shape and
`api.stepfun.ai/step_plan/v1` for OpenAI Chat Completions, with Claude Code, Trae, Cursor
and OpenClaw named as supported clients. **There is no request-frequency limit**: the
page says Step Plan is not subject to the platform's tiered RPM and TPM limits and is
governed by the monthly Credit allowance alone. ⛔ **The allowance is cleared at month
end** and does not roll over, so unused Credits are lost rather than carried, and
booster packs run on their own 30-day cycle.

Evidence: `platform.stepfun.ai/docs/en/step-plan/overview.md` (read 2026-10-22): the four
tiers with monthly, quarterly and yearly prices, the 7M-to-the-USD conversion, the two
Base URLs and the no-rate-limit statement. Verdict: the cheapest plan per unit of work
in the market, on a card, with a clock that clears instead of a request rate that caps.

## What did not work

- **Trae Lite at USD 3.** No such tier exists. Withdrawn in
  `history/2026-10-22T032429Z/`.
- **Cursor Pro and Pro+.** Now the legacy ladder; new accounts cannot buy them. See
  `history/2026-10-22T032428Z/`.
- **Kimi Go and Plus.** Priced in CNY, and Go excludes Kimi Code entirely, so the
  cheapest Kimi tier that includes Kimi Code is Plus at CNY 99.
- **Z.ai Pro and Max.** Two different price pairs have been recorded (USD 72 and 160,
  then USD 80 and 168) and neither is readable today. Neither is carried.

`www.stepfun.com/pricing` is a 396-byte shell and it is the marketing page.
`platform.stepfun.ai/docs/en/step-plan/overview.md` returns 9,444 bytes of current
documentation, so the tier is a row in the table above.

## Chaining

The bracket is where a stack is cheapest to assemble. Copilot Pro at USD 10 is an
editor and a CLI; OpenCode Go at USD 10 is an endpoint; and the pair costs USD 20 with
two independent quotas, which is the same price as one Anthropic Pro with one
invisible quota. Adding a free-standing agent from
[`../free/free-standing-agent.md`](../free/free-standing-agent.md) removes the need
for the editor tier and leaves only the endpoint.
