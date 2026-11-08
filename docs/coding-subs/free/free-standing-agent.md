# Agents that cost nothing because you bring the inference

A free-standing agent is a $0 product with no paid parent. The vendor does not serve
the model, so the vendor has no quota to publish and no allowance to withdraw. The
product is free in the way a text editor is free: the thing you spend money on is
somewhere else.

That is not a smaller version of the paid class, it is a different economics. A
coding subscription is a bundle of turns sold at a flat price, and its risk is that
the bundle is smaller than the work. A free-standing agent's risk is the endpoint it
calls: the cost is per token, the failure is a 429 or a revoked key, and both arrive
from a party the agent's vendor does not control.

The answer: **both agents in this class are self-hosted software, so neither is the
answer where no machine is available to install it on.** The hosted capacity is the
endpoint they call, and [`../../inference/`](../../inference/README.md) ranks those. Of
the two self-hosted agents, Cline is the reference case: a VS Code extension that
accepts any compatible base URL (`documented`, 2026-10-22). Qwen Code's free OAuth
route, the one $0 quota on the vendor's own service, was discontinued on 2026-04-15,
so the self-hosted Qwen Code now costs the tokens of the key it is given.

## The comparison

Sorted by how directly a script can drive them. `Cost` names what a reader
actually pays, which for every row is not the product.

| Provider | Product price | Cost to the reader | Programmatic | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cline (self-hosted) | USD 0 for individuals | the upstream endpoint's tokens | BYOK, any base URL | email | qualifies |
| Qwen Code (self-hosted) | USD 0, open source | the upstream key's tokens; the free OAuth route closed on 2026-04-15 | CLI, three protocols | email | qualifies-with-caveat |

Two rows is the whole class found in this market. It is small because most products
that look free-standing are either a free tier of a paid plan, which
`free-tier-of-paid-plan.md` owns, or a promotional resale of somebody else's quota,
which `free-promotional-window.md` owns.

## Cline

Cline is free for individual developers and is described by its own pricing page as
bring-your-own API key or managed infrastructure, with an Enterprise tier for
organisations (`documented`, `cline.bot/pricing`, read 2026-10-22). It runs as a VS
Code extension the reader installs, so it is self-hosted software, and it accepts an
arbitrary OpenAI-compatible or Anthropic-compatible base URL.

The consequence is that Cline can be pointed at any endpoint in
[`../../inference/`](../../inference/README.md) and inherits that endpoint's quota,
latency and substitution behaviour. There is no vendor-imposed usage cap because
there is no vendor-served inference to cap.

A table ordered by estimated monthly token capacity has no place for a product whose
capacity belongs entirely to somebody else's endpoint.

Evidence: `cline.bot/pricing` (read 2026-10-22): individual use is free, and the
product is described as BYO key or managed infrastructure. Verdict: free, and its
ceiling is whatever the endpoint you point it at will serve.

## Qwen Code

Qwen Code is an open-source terminal agent that supports OpenAI, Anthropic and Gemini
compatible APIs (`documented`, `qwen.ai/qwencode`, read 2026-10-22). It installs from
a shell script and is driven from the terminal, so it is self-hosted software.

⛔ **The free Qwen OAuth route was discontinued on 2026-04-15, and new requests are
rejected** (`documented`, `qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/`,
read 2026-10-29). The `/auth` options are now QwenCloud, Alibaba ModelStudio,
third-party providers and a custom provider, so the agent's cost is the endpoint it is
pointed at, as with Cline. `inference/qwen-code-oauth` records the closed route.

Evidence: `qwen.ai/qwencode` (read 2026-10-22) for the three protocols, and the
Qwen Code auth page (read 2026-10-29) for the end of the OAuth route. Verdict: free
software whose ceiling is whatever the endpoint you point it at will serve.

## What did not work

- **OpenCode (the app).** OpenCode itself is free and open source, but its free
  *models* are gated to requests that originate from the OpenCode client, and the
  endpoint answers a bare HTTP call with `403 FreeTierError` naming that restriction.
  The software is free; the free inference is not reachable from a script. See
  [`../../inference/free/keyless-anonymous.md`](../../inference/free/keyless-anonymous.md).
- **Roo Code and the other BYOK extensions.** A `$0` string inside an HTML or
  JavaScript payload is not evidence of a price, and not evidence of a free tier
  either. They are plausible members of this class with no capture behind them, so no
  record exists.

## Chaining

This class is the join between the two topics. An agent here plus an endpoint from
[`../../inference/`](../../inference/README.md) is a complete working stack with no
subscription in it, and the only bill is the endpoint's own quota. That is the
practical stack: Cline or Qwen Code, pointed at a keyless endpoint while one is
alive, and at a cheap paid endpoint when one is not.
