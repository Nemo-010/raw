# One-time and expiring credit, and what it is worth per dollar

A trial credit is a balance that does not renew. It is worth real money and it is
worth nothing as a rate, because a balance divided by an unbounded remaining life is
not a monthly allowance. The distinction decides how to use it: a trial credit is for
a benchmark, a one-off migration or a burst, and it is never for a workload that runs
every night.

This class overlaps the compute topic. A credit that can be spent on inference is
often the same credit that can be spent on a GPU, and the compute records own the
arithmetic for the machine. This document owns the endpoint.

The answer: **NVIDIA build is the one trial in this class stated as a rate, up to 40
requests a minute with no card and no per-token billing** (`documented`, 2026-10-28).
Together no longer offers a trial: a prepaid purchase of USD 15 comes first. A trial here is
a balance or a rate that cannot carry a plan.

## The comparison

Sorted by whether the allowance is stated as a rate or as a balance, because a rate
can be planned on and a balance cannot.

| Provider | Offer | Shape | Card | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| NVIDIA build | up to 40 requests a minute, no per-token billing | a rate, on a trial tier | no | email | trial-only |
| Together | none: a prepaid purchase of USD 15 first | no trial | yes | card | paid-only |
| Fireworks | trial credits | a one-time balance | varies | email | trial-only |
| Hyperbolic, DeepInfra | none: a deposit of USD 5 or a card or prepaid balance first | no trial | yes | card | paid-only |
| Cerebras | USD 5 of credits, 30-day expiry | a one-time balance behind a card | yes at signup | card | trial-only |

## NVIDIA build

NVIDIA's build platform offers a free tier with no per-token billing, rate limited to up
to 40 requests a minute for most models. Each account shows its own limit in the dashboard
(`documented`, `build.nvidia.com`, read 2026-10-28). No page read on 2026-10-28 states a
daily request figure, so the 10,000-a-day figure from the 2026-10-07 capture is not
carried here.

Stated as a rate rather than as a balance, 40 requests a minute is the one trial in this class
that can be planned against. The limit is per account and it varies by model.

Evidence: the `build.nvidia.com` FAQ, captured under `sources/c/` and cited by
`dossier/inference/nvidia-build-trial.json`.

## Together, Fireworks, DeepInfra, Hyperbolic

Fireworks sells a one-time credit at signup. Together, DeepInfra and Hyperbolic ask for a
card, a prepaid balance or a deposit before any call, as of 2026-10-28.

A one-time signup credit is a real balance, and its value depends entirely on the rate it
is spent at and on the model chosen.

None was called and none of the amounts was read, so no number is carried. The shape
is the finding: a one-time credit spent on inference is a burst allowance, and a
reader who converts it into a monthly figure has invented the divisor.

Together appears in both this topic and the compute topic, ranked there as a code
sandbox provider. The record is shared and each document is a view of it.

## What did not work

- **Planning against a trial.** A balance with no renewal date is a countdown, not a
  quota: a number divided by an unknown number of days is not a rate.
- **Converting a credit to a monthly token figure without the rate.** AMD's and
  Together's credits are stated in dollars; the tokens they buy depend on the model
  and change when the model changes.
- **Treating NVIDIA's trial as a free tier.** The rate is useful and the offer is a trial.
  Both facts belong in the same sentence.

## Chaining

A trial credit chains with nothing, by definition. Its only use is as
the cheapest way to benchmark a model on a vendor's own endpoint before deciding
whether the paid rate in [`../paid/per-token-undercut.md`](../paid/per-token-undercut.md)
is worth paying.
