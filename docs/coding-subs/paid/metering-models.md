# Credits, requests, dollar ceilings and pools, and what each does at the ceiling

Every plan in this market meters something, and the thing it meters decides what
happens when the allowance runs out. That is the question a reader asks at 3 a.m.
and it is the question no pricing page answers in the same place. This document
collects the four metering shapes found, the overage behaviour of each, and the
conversion arithmetic where a vendor has published enough to do it.

The answer: **a dollar-denominated ceiling is the only shape that converts to
tokens by arithmetic a reader can check**, and OpenCode Go is the only plan here that
publishes one per model (`documented`, 2026-10-22). Every other shape is a count of
events whose cost per event is unstated, or a multiple of a baseline that is itself
unstated.

## The comparison

Sorted by how far a reader can get with arithmetic. `At the ceiling` is the behaviour
that matters, and `Overage` names which of the five shapes the vendor documents.

| Provider | Meters | Unit value published | At the ceiling | Overage | Verdict |
| --- | --- | --- | --- | --- | --- |
| OpenCode Go | a dollar ceiling per model | yes: both the ceiling and the token price | falls back to pay-as-you-go credit if enabled, else blocks | fallback-to-credits | qualifies-with-caveat |
| Trae | a dollar balance per month | yes: the balance equals the price | not stated | unpublished | qualifies-with-caveat |
| Copilot | GitHub AI Credits | partly: a dollar allowance, an unpublished rate | not stated on the pricing page | unpublished | qualifies-with-caveat |
| Z.ai | credits with a published formula | yes: a formula, not a token count | not stated | unpublished | paid-only |
| Kiro | credits | no | not stated | add-on credits at USD 0.04 | fallback-to-credits |
| Cursor | one weekly pool | no | on-demand arrears on legacy, top-ups on the new ladder | bill-in-arrears | qualifies-with-caveat |
| Anthropic | a multiple of Pro | no | not stated | fallback-to-credits on Max | qualifies-with-caveat |
| Kimi | a shared pool | no | the pool is shared, so one exhausted feature blocks the others | silent-throttle | paid-only |

## The dollar ceiling

OpenCode Go's limit is a monthly dollar amount per model, and the token prices that
spend it are published for both Go and Go Plus (`documented`,
`opencode.ai/docs/go`, read 2026-10-22). That makes the conversion a division a
reader can do: GLM-5.3 has a USD 15 monthly ceiling on Go and costs USD 1.40 per
million input tokens, so the ceiling is about 10.7M input tokens with no output at
all, and less once output at USD 4.40 is included.

The 5-hour and weekly splits are also published: 20 per cent of the monthly figure
per five hours and 50 per cent per week. So the visible ceiling at any moment is the
five-hour one, which is USD 3 on a USD 15 model. A monthly figure quoted alone
overstates what a burst can spend by a factor of five.

At the ceiling, the behaviour is documented and it is the best in this class: with
prepaid credit enabled, Go falls back to pay-as-you-go rather than blocking, and
without it, requests are refused and the free models stay usable.

## The dollar balance

Trae states its allowance as USD 20, 60 or 200 of usage a month, equal to the price
(`documented`, `www.trae.ai/pricing`, read 2026-10-22). A balance is the most legible
shape available and it is the one that tells a reader least, because the rate that
spends it is not on the page.

At the ceiling the behaviour is unstated. The free tier is described as ending in auto
mode with limited usage, and no tier page says what a paid account meets when the
balance reaches zero.

## The credit

A credit is a count of something the vendor defines. Kiro gives 50 to 10,000 credits
across its ladder and prices top-ups at USD 0.04 (`documented`, `kiro.dev/pricing/`,
read 2026-10-22), which is the one number that constrains what a credit is worth: it
cannot be worth more than USD 0.04, or the top-up would be free money.

Z.ai goes further and publishes the formula: model credits equal (input tokens times
input multiplier, plus cached input times cached multiplier, plus output times output
multiplier) divided by 10,000, with per-model multipliers of 6.9, 1.7 and 24 for
GLM-5.3 (`documented`, `docs.z.ai/devpack/overview`, read 2026-10-22). That is a
credit with a published definition, and it is the only one in this market.

Copilot's GitHub AI Credits are a dollar allowance with an unpublished consumption
rate per agent action, so the allowance is convertible and the activity is not.

## The pool

A pool is one allowance shared across products, and its distinguishing behaviour is
that exhaustion in one place blocks another. Cursor's new ladder has one weekly pool
shared across Cursor, its CLI, cloud agents and the Grok apps, and it refreshes
weekly so that one heavy day does not consume a month (`documented`,
`cursor.com/docs/models-and-pricing`, read 2026-10-22). Kimi's is monthly and shared
between web and Kimi Code, and unused quota does not carry over (`documented`,
`kimi.com/help/membership/membership-pricing`, read 2026-10-22).

Two pools with different clocks and different sharing rules are not comparable, and
the difference is not in any price. A weekly pool bounds a burst more tightly than a
monthly one at the same total, and a pool shared with a chat product is smaller in
practice than its face value for a coding workload.

## Overage, which is the column nobody prints

The five shapes are: refuse, bill in arrears, silently throttle, fall back to credits,
and fall back to a cheaper model. They are opposite risks. Refusal stops work and
protects the card. Arrears keeps work running and produces a bill; Cursor's legacy
arrears billing has produced an unsupervised USD 200 overage.

Three findings from the pages:

- OpenCode Go documents its fallback and its refusal in the same paragraph, which is
  the only complete overage statement found.
- Cursor's legacy individual plans bill in arrears and it is **off until the account
  turns it on**, with a monthly spend limit set at the same place. Teams has it on by
  default. So the arrears risk is a default difference between an individual and a
  team account.
- Copilot, Kiro, Trae and Z.ai do not state their overage behaviour on the pages read.
  A dash in this column is a finding about the page.

## What did not work

- **A single USD-per-million figure for any plan here.** Four of the eight rows cannot
  produce one without an assumption the vendor has not made.
- **Comparing Kiro's credits to Z.ai's.** One has a published formula and the other
  has a top-up price. The units share a name and nothing else.
- **Reading a monthly figure as the working limit.** Where a vendor publishes a
  five-hour split, that split is the ceiling a burst meets first.

## Chaining

The conversion arithmetic is the chain. A plan with a dollar ceiling and a published
token price can be compared against the same model on a pay-as-you-go endpoint in
[`../../inference/paid/`](../../inference/paid/), and that comparison is the only one
in these two topics where both sides are numbers rather than multiples.
