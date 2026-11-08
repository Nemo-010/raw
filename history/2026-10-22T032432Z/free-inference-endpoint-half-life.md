# The free inference endpoint measured on 2026-10-02 was already dead by 2026-10-22, and four more changed state inside one session

- **When:** 2026-10-22T03:24:32Z
- **Status:** observed
- **Supersedes:** `.tmp/seed/coding-subs/2026-10-02/data/opencode-zen-probe.json`, the
  single anonymous survivor it recorded
- **Superseded by:** `docs/inference/free/keyless-anonymous.md` §The half-life of this
  market, and `dossier/inference/opencode-zen-free.json`
- **Evidence:** `probes-w.json` and `probes-w-run2.json` in
  `.tmp/work/w-coding-inference/`, plus `probes.csv` in `.tmp/work/recon-coding/`
- **Confidence:** measured

## What we believed

The seed's 2026-10-02 probe found `space-bunny-free` on OpenCode Zen answering with
no credentials, and carried it as the one anonymous survivor of that pass.

## What we found

It does not answer 20 days later. `space-bunny-free` returned `400` with
`{"type":"server_error","message":"Upstream request failed: Model is unavailable."}`
in the recon run and again in the first run of this session.

The larger finding is the second one. Two full probe runs **eight minutes apart**,
same machine, same candidate list, same script, changed the answer state of four
endpoints, and one of those changes is the instrument corrected rather than the
endpoint moving:

| endpoint | run at 03:02Z | run at 03:10Z | reading |
| --- | --- | --- | --- |
| `api.llm7.io/v1` `codestral-latest` | 200, answered | 429 rate limited | a real per-minute refusal |
| `uncensored-llm.sbs/v1` | 403 Cloudflare Error 1010 | 200, answered with filler | the 403 was the instrument's User-Agent |
| `ovh-qwen36-27b` | 200, answered | 200, empty content, reasoning only | budget exhaustion |
| `opencode-spacebunny` | 403 Cloudflare Error 1010 | 400 model unavailable | the 403 was the instrument's |
| `kilo-openrouter-free` | echoed `nemotron-3.5-lightning:free` | echoed `nemotron-3.5-content-safety` | a router choosing per call |

The 403 on `uncensored-llm` was the instrument, not the endpoint: a request carrying
Python's default User-Agent is refused by Cloudflare before it reaches the origin.
The same request with a curl User-Agent answered. That is recorded because a probe
that does not fix its User-Agent reports a working endpoint as blocked, and the
direction of that error flatters nothing.

The 403 on `uncensored-llm` was the instrument, not the endpoint: a request carrying
Python's default User-Agent is refused by Cloudflare before it reaches the origin.
The same request with a curl User-Agent answered. That is recorded because a probe
that does not fix its User-Agent reports a working endpoint as blocked, and the
direction of that error flatters nothing.

## How we found it

Two runs of a single-process probe, written for this session because the recon
instrument died of MSYS fork exhaustion at about twenty candidates. Every row
carries its own timestamp, status, byte count and body hash.

## What it cost us

It reframes the topic. The unit of a stability claim here is hours, not weeks, and a
document that prints "answers" without a timestamp and a second run is printing a
number that was true for one call.

## What a future session should do differently

Re-probe the top ten before quoting anything. Carry both runs beside every rate, and
treat a changed status between two runs as the finding rather than as noise to
average. Fix the User-Agent, because the default one is refused by at least one
Cloudflare-fronted host in this set.
