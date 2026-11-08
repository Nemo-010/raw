# The dev-environment long tail: 33 more, and the axis that is empty

`free/dev-environments.md` answers the central question in this topic: which free devbox
gives a disk that is still there tomorrow. It covers ten providers. Fifty-three
records carry `category: dev environment`, so thirty-three are in this page, and the
topic's largest unpopulated axis is durability.

⛔ **`extras.persistent_storage.durability` is set on 77 of the 1,411 records, and on 4 of
the 53 dev-environment ones.** State durability is one of the
seven axes a compute record must answer, and it is the axis that decides whether a stop is
a pause or a loss. It is empty almost everywhere, and in this class, where the question is
the whole subject, it is empty on 49 of 53.

## The class by kind

| kind | records | what it means |
| --- | --- | --- |
| allowance | 19 | a quota on a shared, self-hosted or metered environment |
| one-time credit | 2 | a credit that never renews |
| trial | 6 | a clock with a stated end |
| none | 26 | no free tier, of which three are dead |

⚠ **Six of the 53 are not dev environments at all.** `kaggle` is a duplicate slug for
`kaggle-notebooks`, and the record says so in its own `free_tier.stated`. `dagger` is an
open-source engine that runs locally. `lapdev` and `signadot` install into an existing
Kubernetes cluster. `webapp-io` and `webcontainers` run in a browser tab or a
vendor's platform. Each is here because a catalogue row said "dev environment", and a reader
filtering on the class gets five products that give no machine.

## The allowances, and where the code actually runs

The row that matters is not the quota. It is whether the environment is somebody else's
machine, which is the premise of the whole corpus.

| Provider | Free allowance | Where it runs | Verdict |
| --- | --- | --- | --- |
| GitHub Codespaces | 120 core-hours and 15 GB-months a month | GitHub's machines | qualifies-with-caveat |
| Lightning AI | 1 CPU Studio, 24/7, 80 GPU hours to start; access revoked 2026-10-16 | Lightning's machines | dead |
| Boxes.dev | 4 vCPU, 8 GB, 100 GB disk, billed by the second | Boxes' machines | qualifies-with-caveat |
| Artillery | a quota row reading "no limit" | Artillery's machines | qualifies-with-caveat |
| Clusy | 1 concurrent sandbox | Clusy's machines | qualifies-with-caveat |
| Cube | 1 Developer seat, no dedicated deployment | Cube's shared plane | qualifies-with-caveat |
| Teclada | a Free tier, non-commercial only | Teclada's machines | qualifies-with-caveat |
| OpenHands Runtime | a free tier on a catalogue card, not read | not established | qualifies-with-caveat |
| Datalayer | a free tier on a catalogue card, not read | not established | qualifies-with-caveat |
| Prized | free credit, one box at a time | Prized's machines | qualifies-with-caveat |
| Namespace | a 30-day trial of Compute, Devboxes and Runners | Namespace's machines | trial-only |
| Server4Agent | USD 2 of trial credits, 5 GB of storage | the vendor's machines | trial-only |
| Zo Computer | a 14-day trial, 100 GB, 1 unit | Zo's machines | trial-only |
| Exe.dev | a 7-day trial behind a paid ChatGPT subscription | Exe's machines | trial-only |
| Webapp.io | a free trial of hosted test environments | the vendor's platform | qualifies-with-caveat |
| Webcontainers | a Free Personal plan | the browser tab | qualifies-with-caveat |
| Sealos Devbox | none; fixed monthly packages | Sealos' machines | paid-only |
| Tencent Cloud Studio | none; machine-hours deducted per shape | Tencent's machines | paid-only |
| Pipekit | a free trial of a managed control plane | a self-managed Kubernetes cluster | trial-only |
| Kasm Workspaces (self-hosted) | Community Edition, 5 concurrent sessions | a self-managed server | qualifies-with-caveat |
| Okteto (self-hosted) | Starter, free for up to 5 users | a self-managed Kubernetes cluster | qualifies-with-caveat |
| Coder (self-hosted) | Community Edition, unlimited self-hosted workspaces | self-managed servers | qualifies-with-caveat |
| Lapdev (self-hosted) | free during public beta | a self-managed Kubernetes cluster | qualifies-with-caveat |
| Signadot (self-hosted) | ephemeral environments sharing a self-managed cluster | a self-managed cluster | qualifies-with-caveat |

⚠ **Seven of the 25 allowances put the machine in the reader's hands**: Kasm, Okteto,
Coder, Lapdev and Signadot are self-hosted and the last resort, Pipekit is a managed control
plane over a cluster the reader must rent, and Cube depends on how it is read. The corpus
assumes no server and no cluster, so those seven are control planes over capacity that must
be rented first.
That is the same finding `free/platform-hosts.md` records, and it is worse here because
"dev environment" sounds like a service.

⚠ **Coder's Community Edition is genuinely free and unlimited, and it is software.** The
licence is real, the workspaces are unlimited, and every one of them runs on a host the
reader must supply. It is a finding about tooling and not about capacity.

## GitHub Codespaces, the largest real allowance

120 core-hours and 15 GB-months a month on a GitHub Free account, with the codespace disk
persisting while the codespace exists, and ⛔ **the allowance blocks rather than billing
without a card** (`documented`, `docs.github.com`, read 2026-10-22).

120 core-hours is two hours a day of a 2-core machine. ⚠ The disk counts separately: 15
GB-months means one 15 GB codespace for a month, or three 5 GB ones. A reader who spends
the core-hours and fills the disk has two independent walls.

## Lightning AI, closed on 2026-10-16

The offer was one CPU Studio free at 24/7 with no credit card, a restart required
every 4 hours on a free Studio, and a Studio filesystem that persisted across it
(`documented`, `lightning.ai/pricing`, read 2026-10-22).

The platform is closed to every user. `lightning.ai/security-incident` states that
the vendor revoked all user access on 2026-10-16 at 01:00 UTC and that the
platform stays inaccessible to all users (`documented`, read 2026-10-22). The
affected services are Studio, Deployments, Pipelines and Drive. `status.lightning.ai`
carried the banner "Service is down to address a security incident", with the
last update at 2026-10-19 12:49 UTC, and the incident was still open on
2026-10-22 (`documented`).

⚠ The pricing page was not updated. It still advertises "Run 1 Studio free 24/7"
at this read, so the page that sells the product contradicts the page that
reports the incident. The incident page wins because it is newer and it names
the closed service.

⛔ No Studio can be created. The class in this document has no free row that is
both always on and takes an email address alone, so the gap stands. A reader who
needs an always-on machine reads `always-on-free.md`, where Oracle Cloud Always
Free and Google's e2-micro are the rows that remain and both want a card.

Evidence: `lightning.ai/security-incident` and `status.lightning.ai` (both read
2026-10-22), against `lightning.ai/pricing` of the same date. Verdict: dead. The
offer was real until 2026-10-16 and no free lane survives the closure.

## The rows that are a placeholder

Three records here carry the literal sentence "the source card records a free tier without
a credit amount": OpenHands Runtime, Okteto and Datalayer. Across the whole topic 30
records carry it, and `gaps.md` lists all 30. ⚠ **Datalayer is `unverified`, which is at
least honest.**

⛔ **A `qualifies-with-caveat` verdict resting on a placeholder is the weakest claim in
this topic.** Twenty-nine of those 30 carry a `qualifies*` verdict and quote no page, so
one page read each would settle twenty-nine verdicts at once.

## The ones that died or never had a tier

**BuildJet** is `dead` on a catalogue card. **Play with Docker** is unavailable from
2026-03-01. **Gitpod and Ona** are one provider under two names and the pricing URL
resolves to a sales contact form asking for company website, headcount and cloud provider -
which is a `paid-only` verdict with a `write-gated` binding rather than a death.

**Amp** bills orbs by the minute from USD 0.08 an hour and a paused orb costs nothing,
which is a good design and no free tier. **Starsling** bills per-minute runners from
USD 0.004 a minute with unlimited concurrency and no free tier. **Sealos Devbox** and
**Tencent Cloud Studio** both sell fixed monthly packages, and neither has a free lane.

⚠ **Webcontainers is worth naming against the class's premise.** A free Personal plan with
unlimited public projects and a GitHub account needed to save work, and the runtime is the
reader's browser tab. It is not remote capacity, for the same reason Browser Linux
emulators are not, and it is the one row here where the "machine" is the reader's own.

## What this class does not establish

⛔ **What happens to the disk on stop, for 49 of 53 records.** That is the class's own
question and the field is empty. Every answer in this page is prose inside a vendor
sentence, and the field a count would read is null.

**No environment was started.** Every allowance, restart and persistence claim is a page
read on 2026-10-22, and the topic carries no `measured` record.

**No quota was exhausted.** 120 core-hours is the largest real allowance here and nobody
ran it out to see the refusal.

**No self-hosted row was installed.** Coder, Kasm, Lapdev and Signadot are recorded from
their pages, and none was deployed, which matters because their claim is about software and
the corpus assumes no machine to deploy it on.

## What did not work

- **Filtering this class for a machine**: 6 of 25 allowances run on self-managed infrastructure.
- **Reading the class as one product**: 6 of 53 are not dev environments.
- **Codespaces as a 24/7 host**: 120 core-hours is two hours a day of two cores.
- **A placeholder row as a finding**: 4 here and 7 more in three other classes.
- **Webcontainers as remote capacity**: the machine is the browser tab.
