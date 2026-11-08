# Gaps: the claims that are weak, the contradictions that are open, and what rotted

A corpus is worth what its weakest evidenced claim is worth, because a reader cannot
tell which claim that is. This document names them. It carries the claims a plan would
rest on, the contradictions that remain open, what has rotted, and what was never
measured.

Read this before acting on any number here. The front page's withdrawn-claims table
carries what was corrected. This page carries what is still open.

## The claims a plan would rest on, and how sure each is

| claim | rung | what would settle it | what decision it changes |
|---|---|---|---|
| Oracle Always Free is a 24/7 VM with 10 TB of egress a month | `documented` | one tenancy held for eight days at p95 CPU under 20 per cent, to watch the reclaim | whether the free always-on address is real or a two-week trial |
| the seven-day reclaim test is a percentile, not a total | `documented` | a bursty workload held for two weeks with a logged p95 | whether a sleeping workload survives, which is the whole free tier |
| Modal's USD 30 credit buys about 126 hours at 2 vCPU / 4 GiB | `documented` | one sandbox held for ten hours against the credit line, then read the bill | whether the largest recurring credit in this market is a working budget |
| four records carry `measured`, at the transport, listing or price level and never at the quota | `measured` | one quota exercised end to end: a tenancy held past the reclaim test, or a credit spent to zero | every throughput and every "works" sentence in the topic |
| egress is published for 597 of 1,411 records, by a `terms` string that does not begin "not " | `documented` | a page read per provider, or a probe of one GB out | what a serving workload costs, which is often more than the machine |

The fourth row is the one that decides the topic. `measurement.md` states it without
softening: four records in `compute` carry the `measured` rung, and each one measured a
transport, a listing or a price, never a quota. A probe proves that a socket opened and a
banner arrived; it does not prove the quota, the clock or the registration gate. So almost
the whole topic rests on pages that somebody read, and a page is first-party for what a
vendor sells and third-party for what it does.

## Contradictions in the records

**Vast.ai's rate gap was a page problem, not a missing rate.** The pricing page renders
live card prices client-side, so extraction returned none and the record carried a gap on
that basis. The marketplace API answers plainly: a probe of
`https://console.vast.ai/api/v0/bundles/` on 2026-10-22 returned HTTP 200 and 177,005
bytes with 64 offers, including GTX 1660 S at USD 0.021 per GPU-hour, RTX 3090 at
USD 0.109, RTX 4090 at USD 0.120 and RTX 5090 at USD 0.213. The record now carries those
figures with the snapshot date. ⚠ The rate is a marketplace snapshot and moves with host
supply, so it dates faster than a vendor's published price.

**RunPod's and Vast.ai's `extras.shape` is a shell.** Both carry the GPU field and no
vCPU, memory or disk, because both were priced as if they were CPU sandboxes. The
`runpod.json` note says so. A reader comparing them at the 2 vCPU shape this topic
prices is comparing a GPU market to a CPU market.

**Two `dead` GPU records died for different reasons and one is unproven.** `flowdeploy`
lapsed to a parking service, which is a documented death. `mistral-compute` lands on a
help-centre shell, which is a withdrawal. Both are `reported` rather than `documented`,
so neither death was observed first-party, and a re-check of one should cover both.

**`poplarml` answers 404 on its own origin.** `http://poplarml.com` returns 404 and no
route in the challenge protocol changes that. The record is `unverified` rather than
`dead` because a 404 on the apex is not a withdrawal, and the distinction matters for
the same reason it does everywhere in this topic.

**Fifteen records are `unverified` and five of them are whole products.** Azure App
Service F1, Hugging Face ZeroGPU, GKE Agent Sandbox, STACKIT and Vultr Cloud GPU. In
each the page exists and the number could not be read: a client-side table, a create
gate, an API refusal. A reader who treats an `unverified` row as absent will skip a
product that may be the answer.

**A `qualifies*` verdict can sit on a record whose own evidence says there is no free
tier.** ⛔ **That is a vocabulary defect and not a data defect**: `conventions` defines
`qualifies` as "at least 500 GB free per unit", which is a storage test, and `compute` has
no equivalent definition of its own. A reader filtering on the verdict gets a list that
mixes free capacity with invoices. A `--lint` mode in `scripts/dossier/promote.py` refuses
a record whose own free-tier sentence says there is no free tier while the verdict says
otherwise.

**The `dispute` field is populated on five records and three of them are unresolved.**
`modal.json` resolves its own dispute in `notes`. The other four name two conflicting
readings and do not say which is right. That is the conservative choice, because picking the
larger number silently is how a wrong figure gets published.

## What rotted

**Modal began charging for egress on 2026-10-01**, three weeks before the read that
recorded it. Records written before that date carry no egress term for Modal, and a table
built from them treats the largest recurring credit in the market as egress-free. The
record carries the term.

**Hyperbolic's rates refresh weekly.** Its own `retention-clamped` limit says so. A
price quoted in this corpus is not a price next week, and that is the fastest decay in
the topic by a wide margin.

**Oracle's free disk figure contradicts itself on one page.** One paragraph states a
47 GB minimum boot volume and another states 50 GB. The record carries both and treats
50 GB as operative because it appears in the allocation example. Neither is a
measurement.

## What is not measured

Nine things, each with the reason and the probe that would settle it.

**Any throughput, at any provider.** No probe has been pointed at a compute host in this
topic. The topic states throughput nowhere and every table is a price table. The probe is
one HTTP GET or one `iperf3` run per host and it costs nothing on a free tier.

**Any bill.** No paid provider was provisioned. Every price is a published rate, and a
published rate is not an invoice. The gap between them is the rounding rule, the plan
floor and the idle keep-alive, and `paid/minimum-bill.md` describes all three from pages
without once observing one.

**Any registration.** No account was created in this topic. The identity column is a
form read, and `dossier/README.md` calls that `form-read` rather than `executed`. Three
gates are worth executing first because they carry the largest allowances behind them:
Oracle (card plus phone), Kaggle (phone) and Lightning (email only).

**Any reap policy.** The 15-minute Daytona idle, the 4-hour Lightning restart and the
7-day Oracle reclaim are all page claims. Each needs a held session and a wall clock.
That is the one class of measurement this topic cannot do from a page.

**Whether a free tier survives a second account.** No duplicate registration was tested,
so every "per account" figure here is a figure per one account.

**What a sandbox does at its disk ceiling.** Two records carry a disk figure and neither
was filled. The refusal shape, which is the number a reader needs, is unobserved.

**GPU availability as distinct from GPU price.** Every GPU row prices a card. None
records whether the card is obtainable. A marketplace rate is an offer, not stock, and
`vast-ai` is the row where that distinction is largest.

**Whether the macOS and Windows lanes are usable at all.** 23 macOS records and 13
Windows cloud and desktop records price a host and none was booted. The cheap Windows VPS
market is priced separately in [`paid/windows-vps.md`](paid/windows-vps.md), and its eleven
qualifying rows are page reads too. The macOS lane additionally needs a signed build to be
useful, which is `ci-cd-runners`' problem.

**Egress for most records.** The term is a sentence beginning "not " on most of them,
and many are the literal string "not published on the source card". Only a small minority
carry a price per TiB or a free allowance, so the rows that can be priced for a serving
workload are a small minority of the topic.

## What is not in this topic at all

Four absences a reader should know about, because a corpus that does not name its holes
invites a reader to assume they are not there.

**No provider was booted.** Not one machine ran. Every clock, every disk figure and
every network policy in this topic is a sentence on a page.

**No GPU hour was bought or spent.** The free grants are recorded and the paid rates are
recorded, and neither was exercised. A "free GPU hour" in this corpus is an allowance
that a vendor publishes.

**No CI lane is priced here on purpose.** `paid/ci-adjacent.md` states the boundary and
`ci-cd-runners` owns the numbers. The 23 macOS records include runners, and their rates
live there.

**No serverless billing curve.** `free/runtimes-serverless.md` states the CPU wall and
the request count. What a real workload costs across a month of invocations is a
different measurement, and no such measurement exists.

## The open question this topic cannot answer

One question decides more than any number above and it is not a research question:
**what duty cycle does the workload have?**

Every price in this topic is a triple of shape, horizon and hold time. A sandbox at
USD 0.24 an hour is USD 2.40 a month at 10 hours a day and USD 173.71 at 24/7, and both
are the same rate. `paid/bursty-workload.md` prices three duty cycles because one
average hides the difference.

So the answer to "what is the cheapest compute" is a function of a number the analysis
does not fix. If the workload is an agent that runs in bursts, the cheap sandbox lane is
right and the VPS lane is waste. If it is a daemon that must answer at 03:00, only three
free rows and the paid VPS lane exist, and the sandbox lane is irrelevant at any price.
The topic's own headline says this and then ranks both lanes in one column, which is the
compromise a reader should not mistake for a single ranking.

## Documents and the question each answers

| document | the question it answers | what it covers |
|---|---|---|
| [`free/hpc-allocations.md`](free/hpc-allocations.md) | is any national supercomputer open to a person with no institution | 17 allocation programmes, almost all `fails-identity` |
| [`free/research-grids.md`](free/research-grids.md) | which grids and science gateways open on an email address | seven open routes, and the zero GPU-hours they award |
| [`free/startup-credits.md`](free/startup-credits.md) | which founder credits can one person reach | the incorporation gate |
| [`free/research-credits.md`](free/research-credits.md) | which research grants are real and which need a PI | 28 programmes grouped by gate |
| [`free/decentralized-gpu.md`](free/decentralized-gpu.md) | what the decentralized marketplaces are actually worth | 35 records, summed in USD and GPU-hours |
| [`free/regional-clouds.md`](free/regional-clouds.md) | what exists outside the US and EU mainstream | 18 providers by identity cost |
| [`free/asian-clouds.md`](free/asian-clouds.md) | which Chinese, Korean, Japanese and Indian lanes are reachable | domestic versus international lanes |
| [`free/forum-hosts.md`](free/forum-hosts.md) | what the four non-English forums offered | 55 records, two floors behind a local document |
| [`free/student-and-education.md`](free/student-and-education.md) | which student gates verify the person and which the institution | the verification route itself |
| [`free/perpetual-allowances.md`](free/perpetual-allowances.md) | what renews forever and survives an unattended month | 54 records ranked by survival |
| [`free/ci-as-compute.md`](free/ci-as-compute.md) | which CI runner is usable as a machine | public versus private lanes |
| [`free/sandbox-newcomers.md`](free/sandbox-newcomers.md) | what the newer sandboxes charge, and which aggregator tier is missing | the no-card credit worth 1,984 vCPU-hours |
| [`free/ai-and-data-credits.md`](free/ai-and-data-credits.md) | what one person reaches from AI and data vendors | cash separated from compute |
| [`free/devtool-and-platform-credits.md`](free/devtool-and-platform-credits.md) | which tool, prize and fund credits are reachable | the open-source and prize routes |
| [`paid/micro.md`](paid/micro.md) | what the smallest invoice buys, and what USD 2 to USD 50 returns | the entry price, ranked rather than averaged |
| [`paid/brokers-and-bare-metal.md`](paid/brokers-and-bare-metal.md) | what a brokered card and a whole rented machine cost | per-card broker rates against monthly machine prices |
| [`paid/spot-interruptible.md`](paid/spot-interruptible.md) | what the cheapest interruptible capacity costs and what kills it | interruption notice compared side by side |
| [`watchlist.md`](watchlist.md) | which third-party tables to re-read, and how often | the standing sources this topic depends on |

## Verdicts that changed

Each of these moved a record from one decision to another and carries a `history/` entry.
They are listed here because a reader who acts on an older document will meet the old
verdict.

- **Lightning AI's free Studio is dead.** All user access was revoked on 2026-10-16 and
  the platform was still inaccessible on 2026-10-22. No free tier replaced it.
- **Google Colab and Hugging Face Spaces are not trials.** Both publish standing free
  lanes. Colab's limits are unpublished and discretionary; the ZeroGPU allowance is five
  minutes of GPU a day and resets.
- **GitHub Actions public repositories are free and unlimited** on standard runners. The
  2,000 minutes belong to private repositories, and the binding constraint is the
  six-hour job cap.
- **Neon's 100 CU-hours are per project, not per account**, and the free plan is
  permanent rather than a trial.

## What remains unsettled

**No account was created anywhere.** Every registration gate is recorded from what a
vendor page says about it, never from the signup flow. Where a page states a document
requirement, the record says so; where the page is silent, the record says the check is
not described.

**No GPU credit was spent.** The decentralized class sums to a small number and no
deployment was watched to the end of its credit. What happens at exhaustion is
documented, not observed.

**Three sources are permanently unreadable.** A Chinese municipal portal, a forum that
blocks IPv6 readers and a JS-only notebook site could not be re-read on 2026-10-22, and
their records say so rather than carrying a silently refreshed date.

**MiraclePlus has a ceiling and no median.** The programme publishes CNY 1,000,000 as a
maximum and the award distribution is not public, so the record carries the ceiling and
names the gap.

**The regional lanes are the thinnest.** Brazil, Korea, Japan, Russia and India are the
thinnest lanes, and each needs a second read. The pattern is that a local identity
document is the gate far more often than a card, and that pattern deserves its own
document once the per-country detail exists to support it.
