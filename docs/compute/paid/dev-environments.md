# What a real devbox costs once the free hours are gone

A dev environment is the free lane's best product and the paid lane's least
interesting one. Once the 120 code-hours are spent, the price per hour is set by
the same three providers and it does not move much. The question a reader actually
has is different: what does a machine with a persistent disk and a shell cost,
monthly, when the free quota is not enough.

The answer: GitHub Codespaces at USD 0.18 an hour for a 2-core machine is
USD 43.20 for 300 core-hours and USD 120.60 for 24/7. exe.dev is USD 15 a month
for a pool of 2 vCPUs, 4 GiB, 50 VMs and 100 GiB of disk, which is the cheapest
way to get a fleet of small persistent machines. Daytona is USD 49.68 for 300
hours and USD 200 of trial credit. Above those three the lane is Cloud9-class
products at USD 70 to USD 200 a month and none of them beats a USD 6.49 Hetzner
box with a shell.

## The comparison

Sorted by the 300-hour bill at a 2 vCPU shape. `Disk` is what makes it a devbox
rather than a sandbox. The Lightning row is kept at USD 0 because the free Studio was
priced at zero; it has been inaccessible to every user since 2026-10-16 and its verdict is
`dead`.
The paid GPU cluster rental at the same vendor is outside that incident and is priced in
`gpu-notebooks.md`.

| Provider | Shape | 300 h | 24/7 | Disk | Persistent | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Lightning AI | 1 CPU Studio | USD 0 | USD 0 | Studio filesystem | yes | dead |
| exe.dev | pool of 2 vCPU / 4 GiB, 50 VMs | USD 15.00 | USD 15.00 | 100 GiB | yes | trial-only |
| GitHub Codespaces | 2 core / 8 GB | USD 43.20 | USD 120.60 | 32 GB | yes | qualifies-with-caveat |
| Daytona | 2 vCPU / 4 GiB | USD 49.68 | USD 120.89 | 5 GiB free | until archived | qualifies-with-caveat |
| Cube | 1 developer seat, no dedicated deployment | not read | not read | not read | not read | qualifies-with-caveat |
| Namespace | 1 vCPU / 2 GB unit | USD 0.002/min | not read | USD 0.20 per GB-month | yes | trial-only |
| Ona (formerly Gitpod) | sales-led | not published | not published | not established | not established | paid-only |
| Boxes.dev | 4 vCPU / 8 GB / 100 GB | USD 0 wall-clock while awake | not read | 100 GB | until the box sleeps | qualifies-with-caveat |
| Coder (self-hosted) | serve it on a rented or free VM | USD 0 software, the VM's cost | same | the VM's disk | yes | qualifies-with-caveat |

⚠ Six of these rows were priced from a third-party card and their pages were not
opened. Their records say `reported`. The three at the top are `documented`.

## exe.dev

`exe-dev` costs USD 15 a month for a pool of 2 vCPUs and 4 GiB of memory, 50 VMs, 100 GiB of
filesystem usage and 200 GiB of network bandwidth (`documented`, `exe.dev/pricing`,
read 2026-10-22). Work is USD 37.50 at an introductory price against a regular
USD 75.

The pool model is the interesting part. The two vCPUs are shared across fifty VMs
rather than sized per VM, so fifty small machines cost the same as one large one.
That is the right shape for a fleet of short-lived agents and the wrong shape for a
single build that needs both cores.

⚠ The 7-day trial needs a paid ChatGPT subscription rather than a card. That is an
unusual identity gate and it is the reason this row is not in the free lane.

Evidence: `exe.dev/pricing` (read 2026-10-22). Verdict: the cheapest persistent
pool and a trial behind a subscription rather than a card.

## GitHub Codespaces

USD 0.18 an hour for a 2-core machine, USD 0.36 for 4-core, USD 0.72 for 8-core,
with storage at USD 0.07 per GB-month and the first 120 core-hours and 15 GB-months
free on a personal account (`documented`,
`docs.github.com/en/billing/concepts/product-billing/github-codespaces`, read
2026-10-22).

At USD 0.09 a core-hour, 300 hours of a 2-core machine is 600 core-hours, less the
120 free, which is USD 43.20. 24/7 is 1,460 core-hours less 120, which is
USD 120.60. The 24/7 figure is the one that shows why a codespace is not a server:
the same money buys a Hetzner CX23 for a year and a half.

The device that makes this cheap is the devcontainer: a prebuilt image means the
setup does not repeat, and a prebuild consumes storage quota rather than compute.

Evidence: the Codespaces billing page (read 2026-10-22), including the included
usage multiplier column. Verdict: the best editor and image in the lane, and a
price that only makes sense for interactive work.

## Daytona

USD 0.0504 per vCPU-hour and USD 0.0162 per GiB-hour with the first 5 GiB of disk
free (`documented`, `daytona.io/pricing`, read 2026-10-22). At 2 vCPU and 4 GiB
that is USD 49.68 for 300 hours, against a USD 200 trial credit.

Daytona is a sandbox with a devbox's ergonomics: a toolbox API, SSH, snapshots and
sub-90 ms creation. What it is not is persistent by default. A container sandbox
occupies disk quota until archived, and archiving moves the filesystem to object
storage and stops billing.

⚠ The 15-minute default auto-stop fires while internal processes run.

Evidence: `daytona.io/pricing` and `daytona.io/docs/en/limits/` (read 2026-10-22).
Verdict: the fastest machine in the lane and an idle timer that treats a running
build as idle.

## Ona, formerly Gitpod

The Gitpod pricing URL now resolves to `ona.com/contact/sales`, a form asking for
company website, headcount and cloud provider (`documented`, read 2026-10-22).
There is no self-serve price to read and no free tier to measure.

This is recorded as a paid-only row with no numbers rather than as a dead end,
because the product exists and the route is a sales conversation. A reader who
wants it should expect a contract.

Evidence: `ona.com/contact/sales` (read 2026-10-22). Verdict: a sales-led product
with no published price.

## Coder

Coder is software rather than a host: the control plane and the workspaces run on
infrastructure the reader supplies (`reported`, from the catalogue card; the pricing page
was fetched and carries a self-hosted model). That makes its cost the cost of
whatever machine it runs on, which is the VPS document's problem.

⚠ Ona and Coder are the two rows in this lane whose price is not a price. One is a
contract and the other is a licence plus hardware the reader supplies.

## What did not work

- **Hugging Face Spaces as a devbox**: Dev Mode exposes SSH and is part of PRO.
- **Codespaces at 24/7**: USD 120.60 a month for a 2-core machine against
  USD 6.49 for a Hetzner box with the same cores. The codespace is an editor, not
  a server.
- **Gitpod as a free tier**: the URL is a sales form.
- **Replit, Killercoda and Colab**: notebooks and previews, not machines with a
  disk that persists on a schedule.
- **A cloud IDE with a persistent disk and no quota**: no row in this lane offers
  that. The free quota always ends.

## Chaining

The free quota plus a monthly VPS is the chain that works: codespaces for
interactive work under 120 core-hours, and a Hetzner CX23 for anything that has to
stay up. exe.dev is the single-provider answer for a fleet of small machines, at
the cost of a shared pool rather than a dedicated core.
