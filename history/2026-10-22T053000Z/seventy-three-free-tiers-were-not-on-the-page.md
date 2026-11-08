# Seventy-three records claimed a free tier the vendor page does not publish

- **When:** 2026-10-22T05:30:00Z
- **Status:** superseded
- **Supersedes:** the `qualifies-with-caveat` verdict on 73 `compute` records, each of which carried "the source card records a free tier without a credit amount" and no page behind it
- **Superseded by:** those records, now `verdict: paid-only` with the rate card quoted
- **Evidence:** the 73 vendor pricing pages read through the broker on 2026-10-22. Each record in `dossier/compute/` names its own URL and quotes the sentence the verdict was changed on
- **Confidence:** documented

## What we believed

Seventy-three providers qualified with a caveat because a catalogue card said they
had a free tier. Not one of the records had ever had its own URL opened, and
`confidence_note` said so in as many words: *"no page was read in this session"*.

## What we found

On 73 of them the page publishes a rate card and no free tier at all. The shapes
repeat:

| the shape | an example |
| --- | --- |
| a rate card and nothing else | `exoscale`: "Resources are billed by the second", with a 1.42 GiB an hour free *egress* allowance that the card had read as a free instance |
| a free item that is not compute | `self-host-baremetal`: the page's two free items are phone and email *support* |
| "no subscriptions" read as a free tier | `prime-intellect`: "Tier-free pricing built for scale" means there is no plan ladder, not that a tier is free |
| a paying product reached by signup | `claude-managed-agents`, `openai-containers`, `fal`: these are token and model APIs, not machines |
| the compute is self-supplied | `dagger`, `okteto`, `porter`, `coder`, `warpbuild`'s caches: a free control plane over hardware already paid for |

The `docker-cloud-sandboxes` row is the cleanest illustration. The record carried a
USD 25 credit. The page states *"We meter compute by the second, and nothing else.
A paused sandbox costs nothing"* and prices Micro at $0.07 an hour. There is no
credit anywhere on it. The card's number was not wrong when it was written; it was
wrong by the time it was read, and nobody had read it.

## How we found it

One read each of the URL the record already carried. That is the whole method.
This pass opened 319 pages and 239 of them answered 200 with a rate card.

## What it cost us

The largest single block of wrong answers in the topic. A reader asking "what can I
run for nothing" would have been given 73 providers, and the true count of ones
with a permanent free allowance is closer to forty. `docs/expansion/compute.md`
sequences its work by "the 40 providers a reader would act on tonight", and those
40 could not be found in a set where 73 rows were confidently wrong in the same
direction.

## What a future session should do differently

⭐ **A free tier is a claim about a page, so it needs the page.** The corpus rule
was already right — a vendor page is `documented` and a catalogue is `reported` —
and the failure was that 73 `reported` rows were being rendered as qualifying
without anybody noticing that `reported` is not good enough to recommend on.

⚠ **"No free tier" and "no free *compute* tier" are different sentences.** Six of
the 73 give a free sandbox, a free control plane or free egress, and charge for the
machine. The record says which, in `limits_note`, so the next reader does not have
to open the page again to find out.
