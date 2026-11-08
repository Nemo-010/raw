# Free inference: the expansion plan

Free inference endpoints rot faster than anything else in this corpus. One
endpoint verified working on 2026-10-02 was dead by 2026-10-22, and four more
changed state inside a single session. A document older than a month is a
hypothesis, and a document older than a quarter is a list of historical endpoints.

So this plan is not about finding more endpoints. It is about making the finding
**renewable**: a probe set that runs on a schedule, a record that carries the
time it was last seen answering, and a document that reads its table from those
records rather than from prose somebody typed once.

## The gap, quantified

| what exists | count | confidence |
|---|---|---|
| endpoints in `docs/inference/` | see `docs/inference/README.md` | mostly `measured` at the probe date |
| records in `dossier/inference/` | see the topic README's generated count | mixed |
| endpoints discovered but not probed | not in the repository: a scratch file, not retained | `unverified` |
| the probe set | not in the repository: a scratch script, not yet a permanent script | — |

The gap is not a missing market survey. The market is covered: public Ollama
hosts, LiteLLM proxies, OpenAI-compatible free tiers, Hugging Face Inference,
Cloudflare Workers AI, Google AI Studio, Groq, Cerebras, Mistral, OpenRouter,
Together and Fireworks trial credits, Kaggle and Colab hosted inference, and the
serve-it-on-free-compute path. The gap is that **nothing renews it**.

## The verification gate

A candidate becomes a record only when a request answers. The probe must record,
for each endpoint:

| field | why it decides something |
|---|---|
| `http_status` | a 200 is not success; see below |
| `answered` | the body parsed as a completion, not as an error page |
| `model_echoed` | what the endpoint says it served, not what was requested |
| `echo_match` | false means the endpoint substituted a model — worse than a 404 |
| `needle_echoed` | false means the endpoint ignored the prompt |
| `ttft_ms` | time to first token, which is what a user feels |
| `tokens_per_sec` | **and the basis**: without it the number is not comparable |
| `body_sha256` | proof the same request produced the same bytes, for reproducibility |
| `probed_at` | ISO 8601 UTC with `Z` |

⛔ **A 200 that answered with a substituted model, or that ignored the needle, is
a failure, not a finding.** An endpoint that returns a plausible answer to a
different question is harder to detect than one that refuses, and it is worse,
because the caller does not know to check.

⚠ **A key found in a public repository is a fact about the endpoint's state, not a
recommendation.** Record it as `public-key-in-repo: <url>, observed <date>,
works|revoked`. Never copy the key into a document, and never present it as
something to rely on.

## The loop

⚠ **`scripts/probe/inference-sweep.py` is not built.** It is a tools change with
an offline self-test, and issue #35 holds it. The loop below is the plan for after
it merges: a `verify` run executes the sweep, and `land` renders the tables.

```text
python scripts/probe/inference-sweep.py --from dossier/inference/ --out .tmp/<run>/tools/inference/
```

Weekly. The corpus's measured half-life for these endpoints is days, so weekly is
the slowest cadence that still produces a document worth reading. A run that
takes longer than an hour has too many endpoints in the set; prune the dead ones
to a `dead` verdict and stop probing them.

**What the loop writes:** one line per endpoint into its record — `last_seen_ok`,
`last_probe` — and a regenerated table in `docs/inference/`. It does not rewrite
prose. A prose passage that contradicts the regenerated table is a defect the
gate should catch.

**What the loop does not do:** it does not add new endpoints. Discovery is a
separate, slower job, and conflating them means a broken discovery path silently
stops the renewal.

## The discovery method

| source | how | what it yields | rot rate |
|---|---|---|---|
| the aggregator lists on GitHub | `api.gh.pkgforge.dev/search/repositories?q=free+llm+api&sort=stars` then read each list | many candidates, high dead rate | the list is stale but its git history dates each entry |
| the same lists' commit diffs | diff the last two blobs of the README | **newly added endpoints**, with a date | best signal available |
| `linux.do`, `nodeseek` via search snippets | `include_domains=linux.do` with `免费`, `白嫖`, `api` | high, bursty, and often the only public record | high |
| the providers' own free-tier pages | read broker on each | authoritative for limits, not for liveness | slow |
| public key dumps in repos | `gh search code` for `sk-` patterns near `openai` | works-today endpoints | highest — keys revoke in hours |
| an endpoint served on a rented or free VM (self-hosted, the last resort) | provision, serve, expose: an `rq:operator` step, because provisioning needs an account | full control, no third party | none, but the compute rots instead |

⚠ **Two of these are not verified.** The yield of `gh search code` key dumps and
of a self-hosted deployment has not been measured, because both are more work than
a survey. A loop that wires the key-dump route in without measuring it is a loop
built on a guess: run it once by hand, record what it returned, then decide.
The self-hosted route comes after every hosted offer (`AGENTS.md` section 2 rule 9),
and no agent creates the account that provisioning needs (rule 13): its measurement,
if one is wanted, is an `rq:operator` issue.

## The staleness policy

| class | window | because |
|---|---|---|
| an endpoint's liveness | 7 days | measured: four changed state in one session |
| a free-tier limit | 30 days | vendors change a monthly allowance on a billing cycle |
| a model list | 14 days | a provider adds and retires models faster than it changes price |
| a serve-on-rented-compute recipe | 90 days | the compute underneath is what rots, not the recipe |

The topic's review window is 30 days in the policy file. That is too slow for
liveness; the probe loop is what keeps the liveness field current, and the review
window governs the prose.

## What a session should do, in order

1. A tools session that the operator starts in its own clone builds
   `scripts/probe/inference-sweep.py` from the field table above (issue #35). It must be
   hermetic, emit JSON per endpoint, and have a `--selftest` that runs offline.
2. A run: the parent runs the sweep against the existing set into `.tmp/<run>/tools/`,
   records the pass rate, and plans `verify` units seeded with the sweep's output.
3. The tables are the render that `land` runs. Every endpoint graded `measured`
   carries a `probed_at` from the probe.
4. Prose that disagrees with the rendered table is wrong: the lanes file an
   `open_question` that names the document, and a documents session in an own clone
   fixes it.
5. Prune the dead to `verdict: dead` with the date of death. Do not delete.
6. Only then, discover new endpoints, and add them to the probe set before writing
   anything about them.

## What would make this plan wrong

If free inference consolidates into a few stable providers — a plausible future —
the weekly loop becomes unnecessary and a quarterly review suffices. The signal to
watch: **if three consecutive weekly runs show no state change, lengthen the
cadence.** The plan exists because the state changes; when it stops changing, the
plan should stop running so often.
