# Google Colab's free tier is a standing service, not a trial

- **When:** 2026-10-22T14:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/google-colab.json` verdict `trial-only`
- **Superseded by:** `dossier/compute/google-colab.json` verdict `qualifies-with-caveat`; `docs/compute/free/gpu-notebooks.md`
- **Evidence:** `https://huggingface.co/docs/hub/spaces-overview`, `https://huggingface.co/docs/hub/spaces-zerogpu`, `https://research.google.com/colaboratory/faq.html`, `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, `https://railway.com/pricing`, `https://neon.com/pricing`, `https://neon.com/faqs/free-plan-limits-and-quotas`, `https://www.kamatera.com/free-trial/`, all read 2026-10-22 through `scripts/broker/broker.sh read`
- **Confidence:** documented

## What we believed

That the free Colab tier was a time-boxed offer, recorded as `trial-only`.

## What we found

The FAQ, read 2026-10-22, answers the question directly: "Yes. Colab is free of charge to
use". It also states "In the version of Colab that is free of charge notebooks can run for at
most 12 hours, depending on availability and your usage patterns", that "Colab does not
publish these limits, in part because they can vary over time", and that "access to expensive
resources like GPUs is heavily restricted".

Nothing there puts a clock on the offer. What is time-boxed is a session, not the tier.

## What it changes

The verdict becomes `qualifies-with-caveat`. The caveat is not a small one: every limit that
decides whether a workload fits is unpublished and can change without notice, and the 12-hour
figure is itself conditioned on availability. A reader must treat the capacity as
discretionary rather than as a quota.

## The transferable point

`trial-only` means the offer ends. A session cap, a queue or a discretionary limit is a
different constraint and belongs in `binding`, not in the verdict. Two records in this pass
confused the two.
