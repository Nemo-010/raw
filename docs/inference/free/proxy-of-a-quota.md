# Relays, resellers and dead shells, as a first-class category

A relay is a provider that answers a request from somebody else's quota. This is
where a free-endpoint catalogue usually stops being true, because the catalogue row
says "free" and the mechanism behind it is a key that belongs to a third party, a
consumer subscription repackaged as an API, or nothing at all.

It is a first-class category here and not a footnote, because the four shapes have
different failure modes and only one of them is worth using. This document names the
shapes, gives the tell that separates them, and records what breaks.

The answer: **every one of the relays measured here failed a caller who did not check
the echoed model.** BlockRun served `nvidia/nemotron-3-super-120b` for a
`nvidia/gpt-oss-20b` request (`measured`, 2026-10-22), and the cheapest available
tell was the model string in the response body.

## The four shapes

| Shape | What it is | The tell | What breaks |
| --- | --- | --- | --- |
| direct | the provider runs the GPUs or is the model vendor | model echoed equals model requested, and `/v1/models` matches the provider's own family | nothing structural; the quota is the only limit |
| relay | the provider forwards to a third-party API on its own key | an error body naming a different vendor's API, or a catalogue carrying many unrelated vendor families | the upstream revokes the provider's key and every user dies at once |
| reseller of subscriptions | the provider buys consumer plans and exposes them as an API | consumer-plan models at $0 in a catalogue that also sells them at list price | account bans, and a pool that empties without notice |
| dead shell | the page advertises a service and the endpoint answers 404, or 200 with an empty body | a 4-byte or empty 200, or a 404 wearing a full HTML page | nothing works, and an unrecorded one is checked again |

⛔ **The single highest-value column in any probe of this class is whether the echoed
model matches the requested one.** It is the only column that detects a relay and the
only one that detects a reseller. A latency table cannot see either.

## BlockRun, a relay

BlockRun is the clearest instance found. Five sequential identical requests to
`nvidia/gpt-oss-20b`, two seconds apart, produced:

| call | result |
| --- | --- |
| 1 | 200, echoed `nvidia/nemotron-3-super-120b`, a different and larger model |
| 2 | `FREE_MODEL_FAILED`, "Free model capacity exhausted", `debug: "NVIDIA API error: 429 Too Many Requests"` |
| 3 | 200, echoed `nvidia/gpt-oss-20b`, content `4` |
| 4 | `FREE_MODEL_FAILED` |
| 5 | `FREE_MODEL_FAILED` |

Three facts follow.

It is a **relay**, proved by its own error body naming NVIDIA. The 429 is NVIDIA's
limit on BlockRun and not on the caller, so a caller's own rate budget is irrelevant
to whether the request succeeds.

It **fails over to a different model**. A caller that does not compare the echoed
string receives a plausible answer from a model it did not choose, at a price it did
not agree.

It **works two times in five** under light sequential load, and it signals refusal
with a JSON `code` field rather than a 429 status. A retry loop keyed on HTTP status
will not fire. Two later runs answered cleanly, which is why a single probe would
record this endpoint as healthy.

Evidence: a five-call sequence and two clean calls at 03:02Z and 03:10Z. Verdict: a
relay with silent model failover, and the reference case for the category.

## Kilo's openrouter/free id, a router inside a relay

`openrouter/free` on Kilo's gateway echoed `nvidia/nemotron-3.5-lightning:free` in one
run and `nvidia/nemotron-3.5-content-safety` in the next, eight minutes apart, for the
same requested id (`measured`, 2026-10-22).

That is a router rather than a failover: the id names a policy and not a model, so
every call may land elsewhere. Its measured rate moved from 3.20 to 58.14 tok/s between
the two runs, a factor of 18, which is a measurement of two different models rather
than a measurement of one model twice.

A reader cannot use an id whose model is chosen per call for anything that depends on
model behaviour, and can use it as an anonymous fallback when any answer beats none.

## free.ai, one backend behind 513 names

free.ai answered `qwen3-8b`, `qwen-coder` and `deepseek-r1` with
`Qwen/Qwen3-30B-A3B-Instruct` every time, in both runs (`measured`, 2026-10-22). Its
`/v1/models` carries 513 entries and 45 are marked `self_hosted: true`.

This is a reseller shape rather than a relay: the catalogue advertises models that are
not served, and the served model is one the provider does host. The failure is not a
ban or a revocation, it is that the catalogue is fiction. Every capacity claim about
this provider is a claim about one model.

## Pollinations, a relay under an alias

The Classic API lists one model, `openai-fast`, described as `GPT-OSS 20B Reasoning LLM
(OVH)`, with aliases including `gpt-oss-20b` (`measured`, 2026-10-22). A request for
`openai-fast` returns `gpt-oss-20b`.

The catalogue is honest about the arrangement, which makes this the benign case: the
alias resolves to a named upstream and the description says whose hardware it is. The
substitution is a rename, and the finding is only that a benchmark keyed on the
requested string would be attributed to a model called `openai-fast`.

## Dead shells

Two were found and both defeat a status-code probe in different ways.

`models.github.ai/inference` returns **HTTP 200, `Content-Type: text/plain`, a 4-byte
body `OK`**, identical sha256 `19d8c9921b99c82d` across three calls and two model ids
(`measured`, 2026-10-22). A status-only probe scores it as a working free endpoint.

`persorai.com` returned a 404 with a 13-byte body while its landing page advertised a
keyless API, and `openapis.online` returned a 404 with a 17,899-byte HTML page, which
is a 404 wearing a full site. Neither is reachable.

A dead shell costs a request to find and is rediscovered when it is unrecorded. That
asymmetry is why every one here has a record rather than a mention.

## What did not work

- **A catalogue listing as evidence of service.** Four independent instances were
  found in these two topics where a listed model refused the call: OpenCode Zen,
  LLM7 twice, Kilo once and OVH once.
- **A status-code probe.** `models.github.ai` answers 200 and serves nothing.
- **A single-call verdict.** BlockRun answered 2 of 5, and two clean calls would
  record it as reliable.
- **A reputation-based exclusion.** These are technical facts about endpoint state,
  recorded as such. A public key found in a repository would be recorded as
  `public-key-in-repo: <url>, observed <date>, works|revoked` and never copied, and
  none was needed.

## Chaining

A relay is usable as an overflow and not as a base. The rule is to record the echoed
model on every call and to treat a mismatch as a failure even when the content looks
right, because the failure is silent by construction.
