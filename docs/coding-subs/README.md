# Which coding subscription buys the most agent work per dollar, and which ones can a script drive

A coding subscription sells a bundle of agent turns at a flat price. The bundle is
denominated in something the vendor chooses: completions, credits, requests, a
monthly dollar ceiling, or the word "unlimited". Almost none of them publishes a
token count, and the ones that do publish a ceiling measured in money rather than
in tokens. So the first finding of this topic is that the market's headline numbers
are not comparable, and the second is that a plan which only works inside a
vendor's editor is worth nothing to a reader whatever it costs.

The answer at zero cost. **GitHub Copilot Free is the only $0 coding
tier here with a published, countable allowance** (`documented`, 2026-10-22): 2,000
completions a month, no card, and a CLI that a script can drive. Kiro Free gives 50
credits, Trae Free restricts the model to auto routing, Cursor Free states no
number, and Antigravity's free quota is the word "meaningful" with no figure at all.
For a working agent at a known price, **OpenCode Go at USD 10 a month is the only
plan in this market that publishes a per-model monthly dollar ceiling and the API
endpoint that spends it** (`documented`, 2026-10-22).

## The four facts that decide the recommendation

**Free is not a tier here, it is a fraction of one.** Kiro's free tier is 50 credits
against 1,000 on its USD 20 plan, which is 5 per cent. Copilot Free is 2,000
completions against "unlimited" on Pro, which cannot be expressed as a fraction
because the paid side has no number. Comparing free tiers as if they were products
compares a sample against a bundle.

**The quota window got shorter while the price did not.** Cursor moved from two
monthly pools to one weekly pool in the same repricing that raised Plus to USD 30.
Anthropic sells Max as "5x or 20x more usage than Pro" per five-hour session.
OpenCode Go splits each model's monthly ceiling into a five-hour cap at 20 per cent,
a weekly cap at 50 per cent and a monthly cap at 100 per cent. A monthly figure is
now the outer bound and not the working limit.

**Programmatic access is the axis that removes most of the market.** Of the plans
read today, OpenCode Go publishes REST endpoints per model family, Cline and Qwen
Code are BYOK and accept any compatible base URL, and Copilot ships a CLI. Antigravity,
Kiro, Trae and Cursor are editor products with a CLI at best.

**A $0 product with no paid parent has no quota to measure.** Cline and Qwen Code
cost nothing because the vendor does not serve the inference. Their cost is the
endpoint they call, which is why they are documented here and priced in
[`../inference/`](../inference/README.md). Each is software the reader installs and
runs, so both are self-hosted records and come after every hosted plan in a list.

## The comparison

Sorted by what a reader can use tonight at zero cost, then by price. Every row is a
record in `dossier/coding-subs/`. `Binds` is the constraint that binds first for a
single reader. `Programmatic` is the fifth axis every aggregator omits.

| Provider | Free tier | Binds | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| GitHub Copilot | 2,000 completions a month | 2,000 completions, no agent-mode figure | CLI | email | qualifies |
| Devin | Free USD 0, "a light quota to code with agents" | that quota, no number | desktop client only | email | qualifies-with-caveat |
| Windsurf | same ladder, served at devin.ai/pricing | that quota, no number | desktop client only | email | qualifies-with-caveat |
| StepFun Step Plan | no free tier; Flash Mini USD 6.99, Flash Plus USD 9.99 | monthly Credits clear at month end | REST, OpenAI and Anthropic shapes | card | qualifies-with-caveat |
| OpenCode Go | USD 10 a month; 3 models Free, limited time | per-model monthly dollar ceiling | REST endpoints per family | card | qualifies-with-caveat |
| Kiro | 50 credits a month | 50 credits, conversion unpublished | editor only | email | qualifies-with-caveat |
| Trae | auto mode only, no number | no published quota at all | editor only | email | qualifies-with-caveat |
| Antigravity | "a meaningful quota", weekly | the word "meaningful" | editor and CLI | email | qualifies-with-caveat |
| Cursor | limited usage, no number | one weekly pool, size unpublished | editor and CLI | email | qualifies-with-caveat |
| Claude Code | Free excludes Claude Code | usage stated only as a multiple of Pro | CLI | card | qualifies-with-caveat |
| Z.ai GLM Coding Plan | none; Lite USD 18 | 2,000 five-hour credits | REST | card | paid-only |
| Kimi | none; Go CNY 49 excludes Kimi Code | shared monthly pool | CLI | card | paid-only |
| Cline (self-hosted) | the product is free | the upstream endpoint's quota | BYOK, any base URL | email | qualifies |
| Qwen Code (self-hosted) | the agent is free | the upstream key's quota; the free OAuth route closed on 2026-04-15 | CLI, multi-protocol | email | qualifies-with-caveat |

Only three of the fourteen rows publish a countable free allowance: Copilot's 2,000
completions, Kiro's 50 credits and OpenCode Go's three unlimited models. StepFun, Z.ai
and Kimi have no free tier. Cline and Qwen Code are free because the vendor does not
serve the inference, so their cost is the endpoint they call. The other six state a
word, and that is the state of the market. Two of
those six, Devin and Windsurf, are worth a row because their word is attached to a
USD 0 plan that exists rather than to a plan that has closed.

## What this topic cannot tell you

**No plan here publishes a monthly token ceiling that can be verified.** OpenCode Go
publishes a dollar ceiling per model, which converts to tokens only at a stated
input-to-output mix. Z.ai publishes a credit formula with per-model multipliers,
which converts to credits and not to tokens without knowing the prompt shape.
Everything else is a request count, a credit count, or a multiple of another plan.

**Nothing in this topic was subscribed to.** No account was created and no
authenticated request was made, so every quota in this topic is `documented` and
none is `measured`. The one thing measured is which endpoints are free and
reachable, and that belongs to [`../inference/`](../inference/README.md).

## The staleness of this topic

The market moves inside a single month. A seven-day delta recorded four of forty-two
common rows changing price and thirty-five rows appearing. Twelve pages were read on
2026-10-22, and they show **two ladders replaced rather than repriced** (Cursor, Kimi)
and **one SKU that never existed** (Trae Lite). The rows below are marked by the date
they were read, not by the date this document was written.

| claim | read on | age on 2026-10-22 | usable as on 2026-10-22 |
| --- | --- | --- | --- |
| Copilot, Trae, Kiro, Antigravity, Cursor, Claude, Kimi, OpenCode Go, Z.ai credit formula, Cline | 2026-10-22 | 0 days | current |
| Devin ladder, and the Windsurf redirect that serves it | 2026-10-22T04:14Z | 0 days | current |
| StepFun Step Plan four tiers, USD 6.99 to USD 99 | 2026-10-22T04:14Z | 0 days | current |
| Abacus.AI ChatLLM ladder, USD 10 and USD 20 | 2026-10-22 | 0 days | current, no free tier on it |
| ChatGPT tier names | 2026-10-22 | 0 days | names only, no price |
| NVIDIA build trial rate | 2026-10-07 | 15 days | a trial, quoted with its date |
| Kimi USD ladder 19/39/99/199 | 2026-09-13, third party | over 30 days | withdrawn |

## The documents

| document | what it answers |
| --- | --- |
| [`free/free-tier-of-paid-plan.md`](free/free-tier-of-paid-plan.md) | which $0 tier on a paid product is worth using, and what each one withholds |
| [`free/free-standing-agent.md`](free/free-standing-agent.md) | agents that cost nothing because you bring the inference |
| [`free/free-promotional-window.md`](free/free-promotional-window.md) | free while it lasts, and why none of it can be planned on |
| [`paid/under-20.md`](paid/under-20.md) | what USD 20 buys, and which of those plans a script can drive |
| [`paid/20-to-100.md`](paid/20-to-100.md) | the mid ladder, where the free tiers stop being a fraction of it |
| [`paid/over-100.md`](paid/over-100.md) | the top of the ladder and who it is for |
| [`paid/metering-models.md`](paid/metering-models.md) | credits, requests, dollar ceilings and pools, and what each does at the ceiling |

## The dead ends

Four providers are recorded in `dossier/coding-subs/` with the evidence of what failed:
Cursor's request-based generation is closed to new accounts, ChatGPT's prices will not
extract from a 403 challenge, Kimi and Z.ai have no free tier at all, and Abacus.AI's
ChatLLM ladder is readable but has no free tier on it. The Trae Lite tier never existed;
it is withdrawn in
[`history/2026-10-22T032429Z/`](../../history/2026-10-22T032429Z/trae-lite-tier-never-existed.md).

Three providers look dead on one URL and are not: a broker 404 or a shell on one path
is not a dead provider. **Windsurf's host 308-redirects to `devin.ai`, so its ladder is
Devin's.** **Devin's own page returns 200 with 582,848 bytes and a live Free/Pro/Max/Teams
ladder.** **StepFun's documentation page returns 9,444 bytes with four tiers from USD
6.99.** A provider is dead when it does not answer, not when one URL moves. See
[`history/2026-10-22T042700Z/`](../../history/2026-10-22T042700Z/devin-and-windsurf-were-never-dead.md).

## The records

One row per record in `dossier/coding-subs/`, in the order the documents discuss them, self-hosted last.
A reader who wants the machine form of a row starts here.

| Slug | Provider | Rung | Verdict |
| --- | --- | --- | --- |
| `github-copilot` | GitHub Copilot | documented | qualifies |
| `opencode-go` | OpenCode Go | documented | qualifies-with-caveat |
| `kiro` | Kiro | documented | qualifies-with-caveat |
| `trae` | Trae | documented | qualifies-with-caveat |
| `antigravity` | Google Antigravity | documented | qualifies-with-caveat |
| `cursor` | Cursor | documented | qualifies-with-caveat |
| `claude-code` | Anthropic Claude | documented | qualifies-with-caveat |
| `devin` | Devin | documented | qualifies-with-caveat |
| `windsurf` | Windsurf | documented | qualifies-with-caveat |
| `stepfun-step-plan` | StepFun Step Plan | documented | qualifies-with-caveat |
| `zai-glm-coding-plan` | Z.ai GLM Coding Plan | documented | paid-only |
| `kimi` | Moonshot Kimi | documented | paid-only |
| `anthropic-api` | Anthropic API | documented | paid-only |
| `cursor-legacy-request-plans` | Cursor request-based plans | documented | dead |
| `chatgpt-plans` | OpenAI ChatGPT | unverified | qualifies-with-caveat |
| `abacus-chatllm` | Abacus.AI ChatLLM Teams | documented | paid-only |
| `cline` (self-hosted) | Cline | documented | qualifies |
| `qwen-code` (self-hosted) | Qwen Code | unverified | qualifies-with-caveat |

## Records that no other document names

Each `measured` or `documented` record of this topic that no other document of `docs/` names.

<!-- generated:start topic=coding-subs kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `alibaba-cloud-model-studio-coding-plan` | Alibaba Cloud Model Studio Coding Plan | paid-only | documented |
| `alibaba-cloud-model-studio-coding-plan-china` | Alibaba Cloud Model Studio Coding Pla... | fails-identity | documented |
| `amp-individual` | Amp | paid-only | documented |
| `augment-code-business` | Augment Code | paid-only | documented |
| `augment-code-standard` | Augment Code | paid-only | documented |
| `baidu-comate` | Baidu Comate (文心快码) | qualifies-with-caveat | documented |
| `bolt-free` | Bolt | qualifies-with-caveat | documented |
| `bolt-pro` | Bolt | paid-only | documented |
| `cerebras-code` | Cerebras Code | trial-only | documented |
| `charm-hyper` | Charm Hyper | paid-only | documented |
| `codebuddy` | CodeBuddy (Tencent Cloud, internation... | qualifies-with-caveat | documented |
| `lingma` | Qoder CN (formerly TONGYI Lingma) | fails-identity | documented |
| `marscode` | MarsCode (豆包 MarsCode, ByteDance) | dead | documented |
| `mistral-vibe-code` | Mistral Vibe Code (formerly Mistral C... | qualifies-with-caveat | documented |
| `qoder` | Qoder (Qoder International) | qualifies-with-caveat | documented |
| `qwencloud-token-plan-personal-edition` | QwenCloud Token Plan (Personal Edition) | paid-only | documented |
| `qwencloud-token-plan-team-edition` | QwenCloud Token Plan (Team Edition) | paid-only | documented |
| `tabnine-enterprise` | Tabnine | paid-only | documented |
| `v0-free` | v0 | qualifies-with-caveat | documented |
| `v0-plus` | v0 | paid-only | documented |
| `warp-build` | Warp | paid-only | documented |
| `warp-free` | Warp | qualifies-with-caveat | documented |
| `warp-max` | Warp | paid-only | documented |
| `zed-pro` | Zed | paid-only | documented |
| `aider` | Aider (self-hosted) | qualifies-with-caveat | documented |
| `amp-hobby` | Amp (self-hosted) | qualifies-with-caveat | documented |
| `crush` | Crush (self-hosted) | qualifies-with-caveat | documented |
| `zed-personal` | Zed (self-hosted) | qualifies-with-caveat | documented |
<!-- generated:end -->
