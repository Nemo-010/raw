# Which free GPU exists, in which class, for how many hours

A free GPU is not one thing. The class decides the value: an hour on a T4, a P100
and an H100 are different commodities. Lightning's pricing page carries the
conversion in a "Free hours to start" column, so its grant converts into 75 T4-hours,
31 L4-hours, 5 L40S-hours, 3 RTX PRO 6000-hours or 10 A100 40 GB-hours depending on
the card. The vendor revoked all user access on 2026-10-16, which makes the grant
unspendable.
A GPU-hour figure without the card class is not comparable across providers.

The answer: Kaggle gives 30 GPU hours a week on a single P100, which is the largest
published recurring GPU allowance among the products measured here and more than four
hours a day. molab attaches a free RTX PRO 6000 Blackwell with 96 GB of VRAM to any
notebook for up to 12 hours at a time and publishes no monthly cap, so the best card
in this document is not the one with the best hours. Lightning AI gave a starting GPU
grant worth 75 T4-hours or 10 A100-hours on its own published conversion, with a free
24/7 CPU Studio attached, and the vendor revoked all user access on 2026-10-16, so the
grant cannot be spent. The incident page names Studio, Deployments, Pipelines and
Drive as the affected services and states that the Platform stays inaccessible to all
users, so the GPU cluster rental beside them is unreachable too while the closure
holds.
So Kaggle is what a reader plans with for hours, molab is what a reader plans with for
a card, and the table below keeps the dead row with its date.

Hugging Face gives 5 minutes of GPU a day through ZeroGPU on an account older than 30
days. Google Colab gives unspecified GPU access with unpublished limits. None of them
is a machine that answers a login for a week.

## The comparison

Ordered by what a reader can plan against: the free allowances first, then the rows
with no free allowance, then the dead one. `Class` is the card, because the card is
the commodity. `Clock` carries the idle timeout and the session cap, which are two
different numbers and are the two that decide whether anything unattended runs.

| Provider | Class | Free allowance | Clock | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Kaggle Notebooks | 1x P100 | 30 GPU hours a week | 20-minute idle; 12-hour session | any-phone | qualifies |
| molab | 1x RTX PRO 6000 (96 GB) | no monthly cap published | 90-minute idle; 12-hour session | email | qualifies |
| Hugging Face ZeroGPU | half an RTX PRO 6000 | 5 minutes of GPU a day | 48-hour sleep | email | qualifies-with-caveat |
| Google Colab | unpublished | unpublished | 12 hours maximum, conditional | email | qualifies-with-caveat |
| Paperspace Gradient | 1x M4000 | a free GPU, no hour cap published | 12-hour auto-shutdown | email | qualifies-with-caveat |
| RunPod | B300, H200, RTX and others | none | none; billed per second | card | paid-only |
| Vast.ai | RTX 3060 to B200 | none | interruptible instances are reclaimable | card | paid-only |
| Daytona GPU | B300 to RTX 4090 | none: the USD 200 credit is not available for GPU sandboxes | 15-minute idle auto-stop, which can be disabled | email | paid-only |
| Lightning AI | T4 to H200 | 75 T4-hours, 31 L4-hours, 10 A100-hours, 5 L40S-hours, 3 RTX PRO 6000-hours | access revoked 2026-10-16; the free Studio restarted every 4 hours | email | dead |

## Kaggle Notebooks

The GPU quota is 30 hours a week, resets weekly, and is sometimes higher depending
on demand and resources (`documented`, `kaggle.com/docs/efficient-gpu-usage`, read
2026-10-22). A single NVIDIA Tesla P100 can be added to a notebook for free, with
availability limited and queued.

The two Kaggle pages disagree on the idle timeout. The GPU page says "Interactive
sessions remain active until they reach the 60 minute idle timeout limit". The
notebooks page says "While editing a Notebook, you are provided with 20 minutes of
idle time for your interactive session" (both quoted, read 2026-10-24). ⚠ The
notebooks page is the more specific statement, so this document carries 20 minutes and
flags the disagreement rather than averaging it.

30 hours a week is 4.3 hours a day and 130 hours in a 730-hour month, and it is the
largest published recurring GPU allowance here. The P100 is an older card and it is
still a real accelerator; molab's free card carries 96 GB of VRAM against it.

⭐ The session that does not need the browser is `Save & Run All`, the commit button,
or `kaggle kernels push`. The notebook runs top to bottom in a separate session, so
the interactive idle timeout never applies. The wall-clock cap does: "In order to save
successfully, the entire Notebook must execute within 12 hours (9 hours for TPU
notebooks)" (`kaggle.com/docs/notebooks`, quoted, read 2026-10-24). A 20-minute idle
and a 12-hour wall are different clocks, and only the second one binds a headless run.

The phone verification is the identity cost, and it is the only row here that wants a
phone rather than an email or a card. No card is required. Phone verification gates
the GPU accelerator and the Internet toggle, and the requirement sits in Kaggle's
product-feedback threads rather than its documentation, so it is carried at `reported`
confidence.

Evidence: `kaggle.com/docs/efficient-gpu-usage` and `kaggle.com/docs/notebooks`
(read 2026-10-22 and 2026-10-24). Verdict: the best free GPU time in the class, and a
batch runner rather than a host.

## molab

molab is marimo's host. A notebook gets 4 CPUs and 32 GB of RAM by default, and an
NVIDIA RTX PRO 6000 Blackwell with 96 GB of VRAM can be attached to any notebook
(`documented`, `docs.marimo.io/guides/molab/`, read 2026-10-24). Sessions run 12 hours
and a notebook idle for more than 90 minutes is shut down. The vendor publishes no
monthly hour cap at all.

⭐ 96 GB of VRAM with no monthly figure is the largest free card among the products
measured here and the only allowance with no number to exhaust. The reason there is no
number is the clause that governs it: "It will remain free as long as our resources are
not oversubscribed, though we may tweak resource parameters in the public preview as we
adapt to load" (`marimo.io/blog/newsletter-25`, quoted, read 2026-10-22). That is a
capacity condition and not a quota, so it can end without notice and it cannot be
planned against.

⛔ molab is not a machine. The documentation describes no scheduler and no headless
submit, a 90-minute idle shutdown implies an attached session, and a forum report of the
public beta states that the notebook has no public IP interface and that tunnelling is
generally blocked (`reported`, `linux.do`, 2026-09-01). Training, not serving.

Evidence: `docs.marimo.io/guides/molab/` (read 2026-10-24). Verdict: the best free card
in the class, on a preview with no published quota.

## Lightning AI, the free Studio is dead

Two lanes, and the incident names the one that is closed. The affected services are
Studio, Deployments, Pipelines and Drive, so the free Studio and its starting grant are
gone. The incident page also states that the Platform stays inaccessible to all users,
which closes the GPU cluster rental beside it while the closure holds, and
`../paid/gpu-notebooks.md` prices that lane.

The grant is 80 free GPU hours against a published rate table: T4 at USD 0.55 an hour,
L4 at USD 0.79, L40S at USD 3.54, RTXP 6000 at USD 4.64, A100 40GB at USD 2.19, A100
80GB at USD 1.85, H100 at USD 5.45 and H200 at USD 4.50 (`documented`,
`lightning.ai/pricing`, read 2026-10-24).

The same table carries a "Free hours to start" column: 75 on a T4, 31 on an L4, 5 on an
L40S, 3 on an RTXP 6000 and 10 on an A100 40GB. So the 80 hours is a headline and not a
quantity of any one card: no card in the column shows 80, and no card above the A100
40GB shows a free-hours figure at all. That spread is what made the grant possible to
spend well.

⛔ The free lane is dead. `lightning.ai/security-incident` states that all user
access was revoked on 2026-10-16 at 01:00 UTC and that the platform stays
inaccessible to all users (`documented`, read 2026-10-22). `status.lightning.ai`
still showed "Service is down to address a security incident" on 2026-10-22, with
the last update at 2026-10-19 12:49 UTC (`documented`). No Studio can be created,
so the grant cannot be spent.

⚠ The pricing page was not updated. It still advertises "Run 1 Studio free 24/7"
at this read, which is why the class table above carries this row as `dead` and
not as a free allowance.

Evidence: `lightning.ai/security-incident` and `status.lightning.ai` (both read
2026-10-22 and 2026-10-24), against `lightning.ai/pricing` of the same dates. Verdict:
the free grant lane is dead, and `../paid/gpu-notebooks.md` prices the cluster lane,
which is unreachable too while the platform stays closed.

## Hugging Face ZeroGPU

A free personal account in good standing, meaning a verified email and an account
older than 30 days, can host up to 2 ZeroGPU Spaces. The allowance is 5 minutes of GPU
a day, and the daily-quota table pairs that row with the `Medium` size (`documented`,
`huggingface.co/docs/hub/en/spaces-zerogpu`, read 2026-10-24). The `large` profile is
half an RTX PRO 6000 Blackwell with 48 GB of VRAM, quoted from the same page, and
Gradio is the only SDK.

⚠ Which size the free five minutes buys is not stated. The daily-quota row reads
`Medium` and the free-tier text names the `large` profile, and the record carries both
readings rather than picking one.

Five minutes a day is a demo budget: 5 minutes a day is about 2.5 hours in a 30-day
month. A Space also sleeps after 48 hours without a visitor, and the sleep timeout is
confirmed server-side through the runtime API reporting
`gcTimeout 172800`.

⛔ ZeroGPU is not an always-on substrate. It is a queue that gives a Gradio app a card
for five minutes a day, and the card is shared. ⭐ The Space around it does serve
without a browser tab, on one https endpoint and with no session cap, which is the one
machine-like property in this document and the one thing five minutes of GPU cannot
make useful.

Evidence: `huggingface.co/docs/hub/en/spaces-zerogpu` (read 2026-10-24) and
`huggingface.co/docs/hub/en/spaces-overview` (read 2026-10-22). Verdict: a demo
allowance on a large card, and not a training budget.

## Google Colab

Free of charge, with GPUs and TPUs, and no published limits. The FAQ states that
Colab does not publish its limits, in part because they can vary over time, and
that in the free version notebooks can run for at most 12 hours depending on
availability and usage (`documented`,
`research.google.com/colaboratory/faq.html`, read 2026-10-22).

The card types vary over time and are not guaranteed. Colab also states that
access to expensive resources like GPUs is heavily restricted in the free tier,
and that it prioritises users who are actively programming in a notebook.

⚠ The distinction between a quota and a discretionary throttle matters here more
than anywhere in this topic. Colab has a throttle. There is no number to plan
against and no threshold at which a run is safe.

Evidence: the Colab FAQ (read 2026-10-22). Verdict: useful interactively, and
impossible to build a schedule on.

## Paperspace Gradient

The Free plan lists "FREE GPU", a 12-hour auto-shutdown limit and 5 GB of storage, and
DigitalOcean's pricing table names the free machine "Free GPU (M4000)" (`documented`,
`paperspace.com/pricing` and `docs.digitalocean.com/products/paperspace/pricing/`, read
2026-10-24). No weekly or monthly GPU-hour cap is published on either page.

⚠ The M4000 is an older card, the page publishes no memory figure for the free shape,
and the same card is USD 0.45 an hour on a paid instance, which is the only price on the
page. Two first-party pages also disagree about visibility: the plans page gives the Free
plan "Public projects" only, while DigitalOcean's page says free machines "can only be
used for Notebooks in private workspaces". Which one is enforced is unknown.

⚠ A 2026 third-party guide reports the free GPU as discontinued while the vendor page
still lists it and the probe returned a live page with no false-200 signature. The vendor
page proves the listing and not that capacity is obtainable.

Evidence: `paperspace.com/pricing` and
`docs.digitalocean.com/products/paperspace/pricing/` (read 2026-10-24). Verdict: a free
card with no published quota, and the least certain row in this document.

## RunPod and Vast.ai

Neither has a free tier. RunPod publishes on-demand rates across 21 cards, from an RTX
A5000 at USD 0.16 an hour to a B300 at USD 6.94 on Community Cloud and USD 8.99 on
Secure Cloud, and network storage from USD 0.05 per GB a month (`documented`,
`runpod.io/pricing`, read 2026-10-24). Vast.ai sets prices by supply and demand
across 40 or more data centres, with interruptible instances at 50 per cent or
more cheaper and reclaimable (`documented`, `vast.ai/pricing`, read 2026-10-22).

⛔ Vast.ai's pricing page renders its live card prices client-side and returns none of
them, but its marketplace API does not. A probe of `console.vast.ai/api/v0/bundles/` on
2026-10-22 returned 64 offers. The cheapest whole card rentable on-demand was a GTX
TITAN X 12 GB at USD 0.04222 an hour, which is USD 30.82 in a 730-hour month, and the
cheapest interruptible whole card was a GTX 1060 at USD 0.03339 an hour, which is
USD 24.37. The same parse gives cheapest per-GPU rates of USD 0.021 for a GTX 1660 S,
USD 0.109 for an RTX 3090, USD 0.120 for an RTX 4090 and USD 0.213 for an RTX 5090, and
the record does not separate those by tier (`documented`, the probe and its sha256 are
in `vast-ai.json`).

The difference between the two is the reliability of the host. RunPod sells a two-tier
rate card; Vast.ai sells a marketplace, where the cheapest card is a stranger's server
with a 50 per cent discount for the risk of preemption. The TITAN X host is marked
unverified and its egress is USD 4.00 per TB. For a training run that checkpoints, the
discount is real money. For a serving workload it is not a host.

Evidence: `runpod.io/pricing` and `vast.ai/pricing` (read 2026-10-22 and 2026-10-24), and
the Vast marketplace API snapshot of 2026-10-22. Verdict: paid-only, and
`../paid/gpu-notebooks.md` carries the per-card comparison.

## Can any of these run as a machine

A reader of this document wants a host and not a card, and the card is the smaller
question. A free T4 for 12 hours is not a machine. Four fields decide it: whether the
process survives the browser tab, what the idle reap is, whether a disk outlives the
session, and whether anything can reach it. `USD at 24/7` is a 730-hour month at the
record's own rate.

| Provider | Survives the tab | Idle reap | Session cap | Persistent disk | Reachable port | USD at 24/7 | Card gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kaggle Notebooks | yes, through a headless commit | 20 min interactive, and not on the headless path | 12 h | 20 GB in /kaggle/working, across sessions | none: outbound only | 0.00, and the quota buys 130 h a month | none; a phone for the GPU |
| molab | no | 90 min | 12 h | limited, by sidebar upload or persistent cache | none stated, and no public IP | 0.00 | none stated |
| Hugging Face ZeroGPU | yes, the Space serves | 48 h without a visitor | none | no: the runtime is ephemeral and the repo persists | one https endpoint per Space | 0.00 | none; a 30-day-old account |
| Google Colab | no | unpublished | 12 h | none | none | 0.00 | none |
| Paperspace Gradient | no | none published | 12 h | 5 GB | none | 0.00 | none |
| RunPod | yes | none | none | network volume, USD 0.05 a GiB-month | a port map and a proxy | 116.80 | card, and no hold amount recorded |
| Vast.ai | yes | none | none | host disk, retention set by the host | SSH and mapped ports | 30.82 | card and a USD 5 deposit |
| Daytona GPU | yes | 15 min, and it can be disabled | none published | container disk survives a stop | previews and SSH | 416.10 | none to start; a card and a USD 25 top-up at Tier 2 |
| Lightning AI | it was the free 24/7 Studio | none | a 4-hour restart | yes | not stated | 0.00, and unbuyable | none |

⭐ **No free row here is an always-on machine.** Kaggle is the only one that runs a job
with the tab closed, and it is a batch runner: a 12-hour wall, 130 hours a month, no
inbound port, and a runtime that is lost when the session ends. molab, Colab and
Paperspace stop on the tab or on a shutdown clock. The nearest thing to a free machine is
a Hugging Face Space, because it serves without a browser and has no session cap, and it
cannot be logged into, has no scheduler, and holds 5 minutes of GPU a day.

**The paid rows are machines and none of them is cheap.** The cheapest 24/7 machine in
this document is Vast.ai's GTX TITAN X at USD 30.82 a month. The cheapest VPS answer is USD 3.75
for 8 GiB of RAM and 4 vCPU at GreenCloudVPS (`../paid/under-five.md`), which is 8.2
times cheaper, and the cheapest under-one-dollar VPS is USD 0.29 (`../paid/under-one.md`), which is 106
times cheaper. A GPU at 24/7 does not compete with a VPS at either line.

## What did not work

- **Hugging Face Spaces CPU Basic as a GPU host**: the create-time plan gate
  applies to every compute Space, so there is no free path to a GPU Space other
  than ZeroGPU's five minutes.
- **Colab as a scheduled runtime**: a documented absence of limits is a
  discretionary throttle. It cannot be budgeted.
- **A free GPU on a sandbox provider**: no GPU sandbox is recorded for E2B, and its
  record carries no GPU field at all. That is an absence of evidence and not a vendor
  statement.
- **A free GPU with a published hour cap**: molab and Paperspace both hand out a card and
  neither publishes a monthly figure. A free card with no ceiling is a capacity condition
  and not a quota, and it can be withdrawn without notice.

## Chaining

Kaggle is what this document can still chain. It gives 30 hours a week on a P100
for steady work, and the burst lane that sat beside it was Lightning's grant,
which cannot be spent while the platform is closed to all users. A reader with a
card has Lightning's published rate card, which `../paid/gpu-notebooks.md` prices and
which cannot be bought today.

molab chains with Kaggle on the card rather than on the hours: a 96 GB Blackwell for 12
hours at a time will not run unattended, so the artefact that survives is a file written
out of the session, the same as Kaggle's.

⚠ Kaggle publishes no egress term on the page read, so moving a large model out
of it is unpriced and untested.
