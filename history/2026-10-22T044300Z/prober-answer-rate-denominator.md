# The prober's answer rates were right and the reading of them was wrong

- **When:** 2026-10-22T04:43:00Z
- **Status:** corrected
- **Supersedes:** `docs/inference/free/keyless-anonymous.md` §LLM7 and §Chaining, the 37 per cent figure and the "LLM7 is second" ordering; `dossier/inference/llm7.json` and `dossier/inference/ovh-ai-endpoints.json`
- **Superseded by:** the same document and the same two records, rewritten on 2026-10-22
- **Evidence:** `stillworks.supercapybara.com/llm/llm7` and `/llm/ovh-anonymous`, read 2026-10-22T04:21:52Z; captures `.tmp/work/fx-coding-inference/prov-llm7.html` (81,108 bytes) and `prov-ovh-anonymous.html` (39,280 bytes)
- **Confidence:** reported

## What we believed

An adversarial review reported that two answer rates were invented. It said the
prober's payload gives LLM7 195 of 318 calls (61.3 per cent) and OVH 126 of 138 (91.3
per cent), that the documents printed 380 of 1,029 and 243 of 343, and that **neither
figure appears anywhere in either capture**. On that basis it called both numbers
fabricated.

## What we found

**The review was wrong on the facts and right about the defect.** Both figures exist,
verbatim, on the prober's per-provider track-record pages:

- `stillworks.supercapybara.com/llm/llm7`: "380 of 1029 real chat calls answered in 14
  days (37%), median 1133 ms."
- `stillworks.supercapybara.com/llm/ovh-anonymous`: "244 of 343 real chat calls answered
  in 14 days (71%), median 814 ms."

The review had only summed the `recent_attempts` and `recent_successes` fields of the
`/api/llm/up` JSON payload, which carries one row per *model* and therefore a rolling
per-model window. Those sums are 194 of 318 and 125 of 138 — the reviewer's numbers —
and they are a different statistic over a different window, not the one the documents
quoted. `grep -c 1029` over the API payload returns 0; `grep -c 1029` over the provider
page returns 2.

**One figure was still wrong.** The document printed "243 of 343" for OVH. The page says
244. That is a transcription error of one call, in the record and in the prose.

**And the reading of the headline was wrong in a way neither the writer nor the reviewer
noticed.** The prober prints a second figure on the same page that the document ignored:

- LLM7: "Counting only the 556 calls the provider accepted for a model it offers us, 380
  answered (68%): the rest of the gap is models that are listed and refused."
- OVH: "Counting only the 267 calls the provider accepted for a model it offers us, 244
  answered (91%)."

So the 37 per cent headline is dominated by 389 calls that asked for a model LLM7 does
not serve, not by the endpoint failing. Read correctly, LLM7 answers 68 per cent of the
calls it accepts, and the topic's ordering was wrong: OVH is first on both measures, but
second place belongs to free.ai (96 per cent accepted-only) and Pollinations (100 per
cent), with Kilo at 80 and LLM7 at 68. **LLM7 is fifth on acceptance, not second.**

The 14-day window is the prober's own and is stated on its page. The document said 14
days and was right about that.

## How we found it

Two routes were needed. The API payload at `/api/llm/up` was re-fetched live three times
(02:06Z, 03:01Z, 03:55Z) and aggregated per endpoint, reproducing the reviewer's
sums. The per-provider page was then fetched, because the payload's `disclaimer` field
says each entry was verified from the prober's own address and the landing page links a
per-provider page for every endpoint. That page carries the sentence the documents
quoted, and the sentence the documents did not.

## What it cost us

The LLM7 record's `identity_cost.detail`, its `confidence_note` and the document's
Chaining paragraph all rested on the 37 per cent figure being the endpoint's reliability.
The retry-loop advice was right and its justification was wrong.

## What a future session should do differently

⚠ **A payload is not the whole source.** The API returned a number, the number was
consistent across three fetches, and it was the wrong layer of the source. Before saying
a figure "appears nowhere", fetch the page the payload belongs to. ⭐ **And read the whole
sentence a figure sits in**, because this prober prints a denominator correction directly
under every headline and the correction reverses the ranking.
