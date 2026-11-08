# Which $0 tier on a paid product is worth using, and what each one withholds

A free tier of a paid plan is a $0 tier on the same account and the same product as
a plan somebody buys. It is not a free product and it is not a trial, and the
distinction decides how to read it. When a reader upgrades, the model set, the
interface and the quota mechanism stay the same, so a measurement taken on the free
tier describes the paid one too. The reason to separate this class from
`free-standing-agent.md` is that the upgrade path and the model set survive the
change, and the reason to separate it from a promotional window is that this tier
has no announced end.

The answer: **GitHub Copilot Free is the only tier in this class with a published,
countable allowance and a CLI** (`documented`, 2026-10-22). Kiro Free is a countable
50 credits. Trae Free, Cursor Free and Antigravity publish no number, and Claude
Code is excluded from Anthropic's Free tier entirely.

## The comparison

Sorted by how much a reader can act on the row. `Withholds` is the part the $0 tier
removes relative to its own paid parent, which is what a reader needs and what the
vendor's feature list buries.

| Provider | Free allowance | Withholds | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| GitHub Copilot | 2,000 completions a month | unlimited completions, cloud agent, code review, model choice | CLI | email | qualifies |
| Kiro | 50 credits a month | 950 of the 1,000 credits Pro gives, and model choice | none | email | qualifies-with-caveat |
| Trae | auto mode, limited usage | every named model, and every task limit | none | email | qualifies-with-caveat |
| Cursor | "limited usage" | third-party models entirely, cloud agents, automations | none | email | qualifies-with-caveat |
| Antigravity | "a meaningful quota", weekly | the five-hour refresh that Pro and Ultra get | none | email | qualifies-with-caveat |
| Claude | nothing: Free excludes Claude Code | the product itself | none | card | paid-only |

## GitHub Copilot

Copilot Free costs USD 0, needs no card, and includes 2,000 completions a month,
access to Haiku 4.5 and GPT-5 mini, and the Copilot CLI (`documented`,
`github.com/features/copilot/plans`, read 2026-10-22). Pro at USD 10 adds unlimited
completions, the cloud agent, code review, third-party agents and USD 15 a month in
GitHub AI Credits. Pro+ at USD 39 carries USD 70 of credits and Max at USD 100
carries USD 200.

The allowance is stated in completions, which is the one unit here that does not
inflate. Two thousand completions is a countable number of keystroke events, and it
does not become an unknown when a model changes underneath it. What the free tier
withholds is agent work: the paid plans meter agent mode and code review in AI
Credits, and the Free page says the CLI and agent mode are supported without saying
how much of the credit allowance a free account receives.

Evidence: `github.com/features/copilot/plans` (read 2026-10-22): Free is USD 0 with
2,000 completions and no card required. Verdict: the best $0 coding tier in this
market, and the only one a script can drive.

## Kiro

Kiro Free costs USD 0 and gives 50 credits a month with access to open-weight models
and Claude Sonnet 4.5 (`documented`, `kiro.dev/pricing/`, read 2026-10-22). Pro is
USD 20 for 1,000 credits, Pro+ USD 40 for 2,000, Pro Max USD 100 for 5,000 and Power
USD 200 for 10,000, with add-on credits at USD 0.04 each.

Fifty credits against a thousand is five per cent, the smallest free-to-paid ratio
in this class, and the page does not state what one credit buys. The model access is
the same set as the paid tiers on the free plan for accounts created with a social
login or an AWS Builder ID, so the gate differs by sign-in route.

Kiro is an editor product. The pricing page links only to a download, and no API base
URL is published, so the free tier is not reachable from a script.

Evidence: `kiro.dev/pricing/` (read 2026-10-22): the full five-tier ladder with its
credit counts. Verdict: a real free tier whose unit is undefined and whose product
is editor-bound.

## Trae

Trae Free costs USD 0 and restricts the account to auto mode with limited usage and
limited autocomplete (`documented`, `www.trae.ai/pricing`, read 2026-10-22). Pro is
USD 20 with USD 20 of usage a month and all models, Pro+ is USD 60 with USD 60 of
usage, and Ultra is USD 200 with USD 200.

Every paid tier's usage allowance equals its price in dollars, which makes the
ladder unusually easy to read: the plan is a prepaid balance with a concurrency
limit attached. Ten, fifteen and twenty concurrent cloud tasks at the three paid
tiers is the only number that is not simply money.

The free tier withholds the model choice, and that is the whole of it. A reader who
wants to know what the free tier does is told "limited usage", which is a
discretionary allowance rather than a quota.

Evidence: `www.trae.ai/pricing` (read 2026-10-22): four tiers, no Lite tier, and
usage allowances equal to the prices. Verdict: a usable free tier with no published
number, and the USD 3 Lite tier does not exist (see
`history/2026-10-22T032429Z/`).

## Cursor

Cursor Free costs USD 0 and gives agent and chat with limited usage and no
third-party models (`documented`, `cursor.com/docs/models-and-pricing`, read
2026-10-22). It sits on The X Subscription ladder with Plus at USD 8, Premium at
USD 30, Super at USD 100 and Ultra at USD 200.

The ladder this replaces is still documented as legacy: Hobby free, Pro USD 20,
Pro+ USD 60, Ultra USD 200. New accounts start on the new ladder, and the vendor's
own comparison says each new paid plan includes at least twice the coding usage of
the legacy plan it maps to. The free tier is the one rung that did not change.

The new free tier is weaker in a specific way: third-party models are billed at API
list price from prepaid credit on Premium and above, and are not available at all on
Free and Plus. So the free tier is the vendor's own models only, at an unpublished
size.

Evidence: `cursor.com/docs/models-and-pricing` and
`cursor.com/docs/account/pricing/legacy-cursor-plans` (both read 2026-10-22).
Verdict: a free tier with no published allowance, and the only one in this class
whose sibling tiers were replaced rather than repriced.

## Antigravity

Google Antigravity gives every plan a baseline quota, and accounts not on Google AI
Pro or Ultra receive "a meaningful quota, refreshed weekly" with a weekly rate limit
(`documented`, `antigravity.google/docs/plans`, read 2026-10-22). Pro and Ultra add a
quota refreshed every five hours until the weekly limit is reached.

There is no number on the page. The vendor states that the limits "correlate with
the amount of work done by the agent", which is a discretionary allowance with no
ceiling to design against and no threshold at which it is safe. Pro and Ultra can
draw on purchased AI credits above the baseline, controlled by an AI Credit Overages
setting with a "Never" option; the free tier cannot.

The baseline includes Gemini 3.8 Flash as the core agent model, unlimited tab
completions, scheduled tasks and a CLI. That is a working product with no published
size, which is worse for planning than a small published one.

Evidence: `antigravity.google/docs/plans` (read 2026-10-22): the quota structure and
the five-hour refresh for paid plans, with no numeric allowance anywhere. Verdict:
the largest capability set on the smallest published information in this class.

## Claude

Anthropic's Free tier is a chat product with no Claude Code (`documented`,
`anthropic.com/pricing`, read 2026-10-22). The page names Claude Code on the Pro and
Max cards and not on Free, and the support article it links describes Pro as the
plan that includes Claude Code.

So there is no free coding tier here to compare. Pro is USD 20 a month, or USD 17 a
month billed annually at USD 200 up front. Max is "From $100" with a choice of 5x or
20x more usage than Pro, and it carries USD 100 to USD 200 a month in API credits on
the Claude Platform.

Evidence: `anthropic.com/pricing` (read 2026-10-22): the Free column lists chat,
search, file creation, memory and connectors, and Claude Code appears only on the
Pro and Max cards. Verdict: no free coding tier, and the paid entry point is USD 20.

## What did not work

- **Abacus.AI ChatLLM's free tier.** The product is sold and its ladder is readable
  (`abacus.ai/pricing`, read 2026-10-22: Basic USD 10 a month, Pro USD 20), but no free
  tier appears on that page. The USD 10 tier is paid, not a free lane.

Three providers that look unreadable are not. Windsurf's `windsurf.com` host
308-redirects every path to `devin.ai`, so its ladder is Devin's and there is no
separate Windsurf price. Devin's own page returns 200 with 582,848 bytes and a live
Free/Pro/Max/Teams ladder: Free is USD 0 with "a light quota to code with agents".
StepFun's `www.stepfun.com/pricing` is a 2,262-byte shell, but
`platform.stepfun.ai/docs/en/step-plan/overview.md` returns 9,444 bytes of current
documentation and four tiers from USD 6.99. A 404 or a shell on one path is a moved
page; only a host that does not answer is a dead provider.

## Chaining

A free tier and a free-standing agent combine well and a free tier and a paid plan do
not. Copilot Free inside a repository, plus Cline as the agent with an endpoint from
[`../../inference/`](../../inference/README.md), gives an editor, an agent and an
inference bill of zero until the endpoint's own quota binds. Upgrading any single
plan here changes one quota and leaves the rest of the stack alone.
