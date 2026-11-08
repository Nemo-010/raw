# The top of the ladder and who it is for

Above USD 100 a month the ladder stops selling capacity to an individual and starts
selling either concurrency, priority, or a bundled API credit. Four vendors have a
tier at or near USD 200 and each of them means something different by it: Cursor
sells 50 times its base pool, Copilot sells USD 200 of credits, Kiro sells 10,000
credits, Trae sells USD 200 of usage and Anthropic sells a 20x multiple plus USD 200
of API credit.

The answer: **nothing in this bracket is worth buying, and one tier is worth
understanding because it is the cheapest way to buy API credit at face value.**
Anthropic Max 5x at USD 100 carries USD 100 of Claude Platform credit
(`documented`, 2026-10-22), which is a real allowance at a published rate and the
only part of the ladder that converts.

## The comparison

Sorted by price. `Convertible` answers whether any part of the allowance can be
turned into tokens by arithmetic a reader can check.

| Provider | Price a month | Allowance | Convertible | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Anthropic Max 5x | USD 100 | 5x Pro usage, USD 100 API credit | the credit only | CLI | card | qualifies-with-caveat |
| Anthropic Max 20x | USD 100 upward | 20x Pro usage, USD 200 API credit | the credit only | CLI | card | qualifies-with-caveat |
| Copilot Max | USD 100 | USD 200 of AI Credits | in full | CLI | email | qualifies-with-caveat |
| Kiro Pro Max | USD 100 | 5,000 credits | no: the credit unit is undefined | none | email | paid-only |
| Kiro Power | USD 200 | 10,000 credits | no | none | email | paid-only |
| Trae Ultra | USD 200 | USD 200 of usage | in full, at face value | none | email | paid-only |
| Cursor Super | USD 100 | 15x Plus, one weekly pool | no | CLI | email | qualifies-with-caveat |
| Cursor Ultra | USD 200 | 50x Plus, one weekly pool | no | CLI | email | qualifies-with-caveat |
| Kimi Max | CNY 699 | a shared pool, 2x Ultra's agent quota reversed | no | CLI | card | paid-only |
| Kimi Ultra | CNY 1,399 | 28x agent quota, 4 parallel tasks | no | CLI | card | paid-only |

## Anthropic Max

Claude Max is "From $100" a month and lets the buyer choose 5x or 20x the usage of
Pro per five-hour session, with higher output limits and priority access
(`documented`, `anthropic.com/pricing`, read 2026-10-22). Both options carry API
credits: USD 100 a month on one and USD 200 on the other, spendable on the Claude
Platform.

The 20x price is not published. The page source carries `data-plan` attributes for
`free`, `pro_monthly`, `pro_annual`, `max_5x_monthly` and the two team tiers, and
there is no `max_20x` attribute anywhere in the served document. So the 20x tier
exists, is named in the comparison table, and has no price on the page.

What a reader can use is the credit. USD 100 a month of platform credit at published
per-token rates is worth exactly its face value, and it is the only line in this
bracket that a reader can check with arithmetic rather than trust.

Evidence: `anthropic.com/pricing` (read 2026-10-22): Max from USD 100, the 5x and 20x
choice, and the two credit amounts. Verdict: the only convertible allowance here, and
the 20x price is unpublished.

## Copilot Max

Copilot Max is USD 100 a user a month for USD 200 of monthly AI Credits, 2.9 times
the Pro+ included usage or more, and priority access to new models
(`documented`, `github.com/features/copilot/plans`, read 2026-10-22).

Two dollars of credit per dollar of price is the best ratio in this market, and it is
in full: credits are a dollar-denominated allowance, so USD 200 of credits is USD 200
of agent work at the vendor's own rates. On a pure credit-per-dollar comparison,
Copilot Max is the best offer found.

It is still USD 100 a month for an editor. The ratio is good and the entry price is
the problem.

Evidence: `github.com/features/copilot/plans` (read 2026-10-22): Max at USD 100 with
USD 200 of credits. Verdict: the best credit ratio in the market on the most
expensive plan in this class.

## Kiro at the top

Kiro Pro Max is USD 100 for 5,000 credits and Kiro Power is USD 200 for 10,000, with
add-on credits at USD 0.04 each throughout (`documented`, `kiro.dev/pricing/`, read
2026-10-22).

The ladder is perfectly linear at twenty credits per dollar from USD 20 to USD 200.
Nothing improves with scale, and 10,000 credits is 10,000 credits of an undefined
unit.

Evidence: `kiro.dev/pricing/` (read 2026-10-22): the five-tier ladder. Verdict: a
linear ladder whose only defined rate is the top-up price.

## Trae Ultra

Trae Ultra is USD 200 a month for USD 200 of usage, unlimited autocomplete, model
early access and up to twenty concurrent cloud tasks (`documented`,
`www.trae.ai/pricing`, read 2026-10-22).

At USD 200 the balance is again exactly the price. The differentiator is twenty
concurrent cloud tasks, which is a concurrency allowance rather than a capacity one.

Evidence: `www.trae.ai/pricing` (read 2026-10-22): USD 200 of usage at USD 200.
Verdict: a prepaid balance at face value in an editor-bound product.

## Cursor Super and Ultra

Cursor Super is USD 100 a month with 15 times the usage of Plus and priority access at
peak times, and Ultra is USD 200 with 50 times Plus and earliest access to new
products (`documented`, `cursor.com/docs/models-and-pricing`, read 2026-10-22). Both
sit on the one weekly pool shared across Cursor, its CLI, cloud agents and the Grok
apps.

The multiple is the whole allowance, so neither tier adds a number. Ultra at USD 200
for 50x Plus is the steepest ratio in the ladder and still a multiple of an unstated
base.

Evidence: `cursor.com/docs/models-and-pricing` (read 2026-10-22): Super at USD 100
with 15x Plus and Ultra at USD 200 with 50x Plus. Verdict: the largest multiple on the
smallest published base.

## Kimi Max and Ultra

Kimi's Max is CNY 699 a month and Ultra is CNY 1,399 a month on the domestic ladder,
with annual totals of CNY 6,708 and 13,428 (`documented`,
`kimi.com/help/membership/membership-pricing`, read 2026-10-22). Ultra carries 28
times the agent quota, described as twice Max's, with four parallel agent tasks,
25 scheduled tasks, 25 widget tasks, 100 projects and 50 GB of project storage.

The quota numbers are multiples and counts, not tokens. The only absolute figure in
the tier description is the 50 GB of project storage, which is not a coding
allowance.

Evidence: `kimi.com/help/membership/membership-pricing` (read 2026-10-22): the CNY
ladder and Ultra's 28x agent quota. Verdict: a multiple of an unpublished base with a
storage figure attached to it.

## What did not work

- **Claude Max 20x as a priced row.** The tier is named and has no price on the page.
- **A USD-per-token comparison across this bracket.** Every allowance except the two
  credit amounts is a multiple of an unstated baseline, so a per-token figure would be
  an estimate dressed as a measurement.
- **Any assumption that a higher tier is cheaper per unit.** Copilot improves its
  credit ratio with price, Kiro and Trae do not move at all, and Anthropic and Cursor
  never state the unit. There is no general rule.

## Chaining

Nothing here chains, and that is the finding. The bracket is designed for a single
buyer with a single account, and a reader assembling a stack buys three cheap plans
that fail independently rather than one expensive plan that fails everywhere at once.
