# Hugging Face Spaces has a free lane, and the ZeroGPU allowance recurs daily

- **When:** 2026-10-22T14:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/huggingface-spaces.json` verdict `paid-only`; `dossier/compute/huggingface-spaces-zerogpu.json` verdict `trial-only`
- **Superseded by:** both records now `qualifies-with-caveat`; `docs/compute/free/perpetual-allowances.md`
- **Evidence:** `https://huggingface.co/docs/hub/spaces-overview`, `https://huggingface.co/docs/hub/spaces-zerogpu`, `https://research.google.com/colaboratory/faq.html`, `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`, `https://railway.com/pricing`, `https://neon.com/pricing`, `https://neon.com/faqs/free-plan-limits-and-quotas`, `https://www.kamatera.com/free-trial/`, all read 2026-10-22 through `scripts/broker/broker.sh read`
- **Confidence:** documented

## What we believed

That a Gradio or Docker Space required a paid plan, so the whole product was `paid-only`,
and that ZeroGPU was a one-shot trial credit, so its record was `trial-only`.

## What we found

Two sentences on the vendor's own pages, read 2026-10-22, refute both.

`https://huggingface.co/docs/hub/spaces-overview`: "Static Spaces are free for everyone.
Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal
accounts, Team or Enterprise for organizations. Free personal accounts in good standing can
still host up to 2 Gradio Spaces running on ZeroGPU."

`https://huggingface.co/docs/hub/spaces-zerogpu`: "Free personal accounts: accounts in good
standing (verified email, account older than 30 days) can host up to 2 ZeroGPU Spaces for
free", with a usage table row "Free account | 5 minutes | Medium".

The allowance is 5 minutes of GPU a day and it resets. That is a recurring allowance, not a
credit, so `trial-only` was the wrong word for it.

## What it changes

`huggingface-spaces` becomes `qualifies-with-caveat`, with the binding constraint named as
the 5 minutes a day and the sleep on inactivity rather than the 2-Space cap. The free lane is
real and small: two Spaces, five minutes of GPU a day, 50 GB of non-persistent disk, a
verified email and an account older than 30 days.

`huggingface-spaces-zerogpu` becomes `qualifies-with-caveat` for the same reason the class
rule already gives: a recurring free allowance is not a trial.

## The transferable point

A product page that says "requires a paid plan to create" can be true of creation and false
of hosting, and the exception sits in the same paragraph. Reading the paragraph rather than
the first clause is what produced this correction.
