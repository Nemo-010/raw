# Which free IDE or devbox gives a persistent disk

A dev environment is a shell with a home directory, an editor attached, and a
machine that survives the session. It is the most useful free tier in this topic,
because the one thing a sandbox will not give is a disk that is
still there tomorrow. The question is therefore not the hourly rate but what
happens to the files when the session ends, and what the quota is denominated in.

The answer: GitHub Codespaces gives 120 core-hours and 15 GB-months a month on a
GitHub Free account, which is two hours a day of a 2-core machine with nothing
left over. Lightning AI gave one CPU Studio free 24/7 with no card and a restart
every four hours, and the vendor revoked all user access on 2026-10-16. That
leaves no free machine in this document that neither bills nor expires.
Everything else is a trial credit.

## The comparison

Sorted by the free allowance. `Persists` is what happens to the disk on stop.

| Provider | Free tier | Persists | Identity | Held 24/7 | Verdict |
| --- | --- | --- | --- | --- | --- |
| GitHub Codespaces | 120 core-hours and 15 GB-months a month | disk persists while the codespace exists | card | USD 120.60 | qualifies-with-caveat |
| Daytona | USD 200 one-time | container disk until archived | email | USD 120.89 | qualifies-with-caveat |
| exe.dev | 7-day trial with a paid ChatGPT subscription | 100 GiB of filesystem included | card | USD 15.00 | trial-only |
| Killercoda | 1 hour per scenario | nothing | email | not applicable | trial-only |
| Gitpod (Ona) | no self-serve free tier; sales contact | not established | card | not established | paid-only |
| Google Colab | free GPU with unpublished limits | nothing; the VM is deleted | email | USD 0 | trial-only |
| Hugging Face Spaces CPU Basic | hardware lists FREE, create needs PRO | none; 50 GB non-persistent | card | USD 9.00 | paid-only |
| Replit | a 30-day preview | the preview link | email | not applicable | trial-only |
| Play with Docker | withdrawn | not applicable | anonymous | not applicable | dead |
| Lightning AI | 1 CPU Studio, 24/7, 80 GPU hours; access revoked 2026-10-16 | Studio filesystem survived | email | USD 0 | dead |

## Lightning AI, closed on 2026-10-16

The offer was one Studio free at 24/7 with no credit card and no commitment, with
a restart required every 4 hours on a free Studio and a Studio filesystem that
persisted across it (`documented`, `lightning.ai/pricing`, read 2026-10-22). The
account also started with 80 GPU credits against a card table from a T4 at
USD 0.55 an hour to an H200 at USD 4.50.

The platform is closed to every user. `lightning.ai/security-incident` states that
the vendor revoked all user access on 2026-10-16 at 01:00 UTC and that the
platform stays inaccessible, and it names Studio, Deployments, Pipelines and
Drive as the affected services (`documented`, read 2026-10-22). The status page
carried the banner "Service is down to address a security incident", with the
last update at 2026-10-19 12:49 UTC.

⚠ The pricing page was not updated and still advertises a free Studio that no
reader can create. Read the incident page, not the price.

Evidence: `lightning.ai/security-incident` and `status.lightning.ai` (both read
2026-10-22). Verdict: dead. Codespaces is the free devbox that remains.

## GitHub Codespaces

GitHub Free for personal accounts includes 15 GB-months of storage and 120 hours of
compute a month (`documented`,
`docs.github.com/en/billing/concepts/product-billing/github-codespaces`, read
2026-10-22). The default machine is 2 cores, 8 GB and 32 GB of storage, and the
compute cost is proportional to the core count, so a 16-core machine costs eight
times a 2-core one.

⚠ The unit is core-hours and the billing page is the only place that says so: its
"Included usage multiplier" column carries 2 for a 2-core machine, so one hour of
a 2-core codespace consumes 2 of the 120. That is 60 wall-clock hours a month, or
two hours a day. A reader who reads "120 hours" as wall-clock and works eight-hour
days plans fifteen days and has seven and a half.

At USD 0.09 per core-hour the 2-core rate is USD 0.18 an hour. Three hundred
running hours is 600 core-hours, which is USD 54.00 gross; the 120 included
core-hours are USD 10.80 of that, so the bill is USD 43.20. At 24/7 the gross is
USD 131.40 and the net USD 120.60, which is what the table prints.

The gate is at exhaustion. If the account has no valid payment method on file,
usage is blocked once the quota is used, so the card is the price of running past
month one rather than the price of starting.

Storage accrues in GB-hours while the codespace exists, whether it runs or not, so
a stopped codespace still costs its disk.

Evidence: the Codespaces billing page (read 2026-10-22). Verdict: the best free
Linux devbox with a shell, and a quota stated in a unit most readers will misread.

## Daytona

USD 200 in free compute, billed per second at USD 0.0504 per vCPU-hour and
USD 0.0162 per GiB-hour, with the first 5 GiB of disk free (`documented`,
`daytona.io/pricing`, read 2026-10-22). The trial needs no credit card.

The disk behaviour is better than most sandboxes and it depends on the sandbox
class. A stopped container sandbox occupies disk quota until it is archived;
archiving moves the filesystem to object storage, frees the quota and stops
billing. A stopped VM sandbox frees the quota by offloading its state, which keeps
resume fast. Paused VM sandboxes free the quota too (`documented`,
`daytona.io/docs/en/limits/`, read 2026-10-22).

The 15-minute default auto-stop is what turns the USD 200 into a budget rather
than a machine. It triggers even while internal processes run, and only external
interactions reset it.

Evidence: `daytona.io/pricing` and `daytona.io/docs/en/limits/` (read 2026-10-22).
Verdict: the best disk semantics among the sandboxes and an idle timer that
agrees.

## exe.dev

USD 15 a month for a pool of 2 vCPUs and 4 GiB of memory, 50 VMs, 100 GiB of
filesystem usage and 200 GiB of network bandwidth, with a 7-day trial available to
a paid ChatGPT subscription (`documented`, `exe.dev/pricing`, read 2026-10-22).

The pool model is unusual: the resources are shared across the VMs rather than
sized per VM, so fifty small machines cost the same as one large one. That is the
right shape for a fleet of short-lived agents and the wrong shape for one big
build.

Evidence: `exe.dev/pricing` (read 2026-10-22). Verdict: a cheap pool with a trial
that needs a ChatGPT subscription rather than a card.

## Google Colab

Free of charge, with access to GPUs and TPUs, and the limits are not published:
`research.google.com/colaboratory/faq.html` states in its own words that Colab
does not publish its limits, in part because they vary (`documented`, read
2026-10-22). In the free version a notebook can run for at most 12 hours
depending on availability and usage.

⛔ A documented absence is weaker than a documented limit. "Colab does not publish
these limits" is a discretionary throttle: there is no ceiling to design against
and no threshold at which the work is safe. The 12-hour figure is the only number
the page gives and even it is conditional.

The VM is deleted when idle and has a maximum lifetime enforced by the service, so
nothing persists except the notebook file.

Evidence: the Colab FAQ (read 2026-10-22). Verdict: a notebook with an
undisclosed throttle, useful interactively and impossible to schedule against.

## What did not work

- **Hugging Face Spaces CPU Basic**: 2 vCPU and 16 GB of hardware that lists as
  FREE and cannot be created on a free account. A create-time plan gate.
- **Replit**: the free tier publishes a link that goes down after 30 days. A
  preview, not hosting.
- **Killercoda**: one hour per scenario and then the environment is deleted.
- **Play with Docker**: unavailable from 2026-03-01.
- **Gitpod**: the pricing URL now resolves to a sales contact form. There is no
  self-serve free tier to measure.

## Chaining

Codespaces is the free devbox, and it is the row this document leads with.
Lightning was the free always-on machine it chained with, and that platform closed
to all users on 2026-10-16. `always-on-free.md` carries what replaces it, which is
Oracle Cloud Always Free and a card plus a phone at signup.

No row here is storage, so anything worth keeping leaves through git.
