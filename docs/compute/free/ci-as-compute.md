# Which CI runner is a machine a scheduled job can use, and what ends the job first

A CI runner is a machine with a scheduler in front of it and a wall clock attached. That makes
it free compute with two meters instead of one: a pool of minutes, and a ceiling on any single
job. The question this document answers is which of the free runners a scheduled job can
actually use tonight, which unit the pool is counted in, and which of the two meters stops the
job.

The compute dossier holds ten records of category `CI runner`. Eight are in this document. The
other two are `github-actions`, whose numbers live in
[`../../ci-cd-runners/free/github-actions.md`](../../ci-cd-runners/free/github-actions.md), and
its paid-only sibling `gitlab-runners`, in
[`../../ci-cd-runners/paid/`](../../ci-cd-runners/paid/). A ninth row below is Tencent CNB,
recorded under `dev environment` and included because it sells the same product: a build machine
with a quota and a cap.

The class is worth about 213 core-hours a month across four live accounts, on four pools one of
which is `unverified`, so the total needs the caveats in section "One unit before any sum". The
largest pool in wall-clock terms is 1,667 job-hours, and it sits behind the hardest gate: a
reviewed open-source programme with an annual re-application. The smallest lane imposes a
ten-minute ceiling on every job, which no amount of idle queue fixes.

## The short answer

Grouped by what the offer contains: a machine with a pool, then a scheduler with no machine, then
the lanes that are closed or were never hosted. Within the machine group the order is the pool
from largest to smallest, on the conversions in the next section. Every allowance cell stays in
the vendor's own unit, because the whole class is misread by converting it too early.

| provider | free allowance, unit, and lane | job cap | concurrency | identity gate | what fails first | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| GitLab `gitlab` | 400 compute minutes a month on Free, private namespace; 50,000 minutes at cost factor 0.5 on the public open-source programme | 60 minutes default; settable per project from 10 minutes to 1 month | not published in the record | email, then an annual review of every project in the namespace | the review, then the 400 minutes | qualifies-with-caveat |
| Tencent CNB `tencent-cnb` | 160 core-hours a month of build CPU and 1,600 core-hours of development CPU, as two separate pools; GPU quota 0 | not published; a forum post recorded a 4-hour session limit before the GPU quota was withdrawn | not published in the record | any-phone, which for a mainland account is a real-name check | the build pool: 20 hours at 8 vCPU, and a GPU quota of zero | qualifies-with-caveat |
| Buildkite `buildkite` | 2,000 Linux vCPU-minutes a month, plus 250,000 test executions; no separate public lane in the record | not published in the record | 10 concurrent jobs, 5 users | email; the page states no card | the vCPU-minute pool, which is 8 hours 20 minutes a month at 4 vCPU | qualifies-with-caveat |
| RunMyJob `runmyjob` | 400 vCPU-minutes a month at 12 vCPU and 32 GB per job, `unverified` and from a third-party directory; no separate public lane in the record | not published in the record | 10 concurrent jobs | email | the vCPU-minute pool: 33 minutes of a 12 vCPU job a month | qualifies-with-caveat |
| Cirun `cirun` | USD 0 for orchestration on unlimited public repositories; no compute included | set by the cloud account, not by Cirun | unlimited runners | card, plus a billed cloud account with a service-account key | the cloud bill, from the first vCPU-hour | paid-only |
| Codeberg Forgejo Actions `codeberg-forgejo-actions` | no monthly meter; 40 CPU-minutes per job at 4 vCPU for 10 minutes; public repository under a free licence | 2, 5 or 10 minutes by runner label | not published; fair use, with a `-lazy` queue that aims to finish within 24 hours | email, plus a public repository and a volunteer-reviewed request on the Woodpecker side | the 10-minute wall clock | qualifies-with-caveat |
| Cirrus CI `cirrus-ci` | was 50 compute credits a month for public repositories, stated as 10,000 Linux CPU-minutes or 500 macOS minutes | 2 hours per task with a full runtime | 16 CPUs on Linux, 8 CPUs per task | email | the service: shut down 1 June 2026 | dead |
| Quansight `quansight` | was free GPU CI for conda-forge feedstocks, on one host with 6 V100 | the record states that no per-job limit was implemented | 4 GPUs exposed server-wide | institution: a feedstock and a maintainer in the access file | the decommission on 2026-03-13 | dead |
| Drone CI `drone-ci` (self-hosted) | none hosted; the product ships as software the caller runs | not applicable, no service | not applicable, no service | institution | no registration path | paid-only |

## One unit before any sum

⭐ The class cannot be added up in the units the vendors print. A vCPU-minute is a core
multiplied by a wall-clock minute. A compute minute is a wall-clock minute multiplied by a
cost factor. A core-hour is a core for one hour. Those three are different units, and one
number in one unit does not compare with a number in another.

Buildkite states the pool as 2,000 Linux vCPU-minutes a month. Divide by 60 to get vCPU-hours:
2,000 / 60 = 33.3 vCPU-hours. Divide by the core count of the agent to get wall clock, because
the meter spends one unit per core per minute. On a 4 vCPU agent, 2,000 / 4 = 500 wall-clock
minutes, and 500 / 60 = 8.33 hours, or 8 hours 20 minutes for the whole month.

RunMyJob's allowance is 400 vCPU-minutes a month with a 12 vCPU shape per job, and that figure
is `unverified`: the record's notes say the free plan's allowance was not read from a
first-party pricing page, so it comes from a redirect page and a third-party directory. At 12
cores the meter spends twelve units a wall-clock minute, so 400 / 12 = 33.3 wall-clock minutes
for the month, if the allowance holds.

One vCPU-minute is worth 60 / 4 = 15 seconds of wall clock on a 4-core shape, and
60 / 12 = 5 seconds on a 12-core shape. The unit is the core count, not the clock.

⚠ A reader who takes a vCPU-minute for a minute of machine time overstates Buildkite by four on a
4-core agent and RunMyJob by twelve. That is the error the allowance column exists to prevent.

Cirrus counted CPU-minutes directly: 50 credits, stated as 10,000 Linux CPU-minutes. On the
default 2-CPU container that is 10,000 / 2 = 5,000 wall-clock minutes. Tencent CNB counts
core-hours: 160 / 8 = 20 hours of an 8 vCPU build. Codeberg publishes no monthly meter at all,
only 4 vCPU x 10 minutes = 40 CPU-minutes per job.

The sum, with its condition stated: 33.3 vCPU-hours (Buildkite) + 6.7 vCPU-hours (RunMyJob,
400 / 60) + 160 core-hours (CNB build) + 13.3 vCPU-hours (GitLab, 400 minutes on the 2 vCPU
default runner, which assumes a compute minute is charged per wall-clock minute) = 213.3
core-hours a month. The RunMyJob term is the weak one: it rests on an `unverified` figure, so the
total is 213.3 if that figure holds and 206.6 without it. Codeberg adds 40 CPU-minutes per job with
no published job count, so it has no monthly figure to add. The four pools sit on four accounts
with four identity gates and cannot be merged into one job.

## The public lane and the private lane

⭐ This is the confusion that costs an order of magnitude. For the providers that run both
lanes, the public one is a grant with a review and the private one is a small metered pool. The
numbers are not two versions of one number.

GitLab is the clearest case in the slice, because the record carries both rows. A Free namespace
receives 400 compute minutes a month, which is 400 job minutes at the factor of 1 that applies to
a standard project. The GitLab for Open Source programme gives 50,000 compute minutes at a cost
factor of 0.5. Divide 50,000 by 0.5 to get job minutes: 50,000 / 0.5 = 100,000 job minutes, and
100,000 / 60 = 1,667 hours. The ratio between the two lanes is 100,000 / 400 = 250. A reader who
plans against the private number and then applies it to an open-source workload is out by 250
times.

Codeberg has one lane, and it is public. The runner rules require a public repository under a
free licence, and the record quotes a further rule: "No extensive pipelines to assist LLM-driven
workflows". A private repository is not a smaller allowance here. It is not the lane.

Cirrus had one lane too: free for open source, on public repositories. Its death therefore
leaves no private product to fall back to at the same provider.

Buildkite, RunMyJob and Tencent CNB publish a single pool. None of their records carries a
public-repository discount, so the pool is the pool. That is a statement about the records, not
a claim that no discount exists.

## The cost factor, and the GPU multiplier

GitLab charges a job by duration and by runner shape. The record's table is small and it is the
whole mechanism: `duration / 60 x cost factor`, with a runner factor of 1 for small, 2 for
medium, 3 for large, 6 for xlarge, 12 for 2xlarge, 7 for the GPU standard runner and 6 for the
macOS M1 runner. Project type multiplies again: 1 for a standard project, 0.5 for a public
project in the programme, 0.008 for a public fork of one.

The arithmetic on each lane:

- 50,000 compute minutes x 0.5 project factor, small runner: 50,000 / 0.5 = 100,000 job minutes,
  and 100,000 / 60 = 1,667 hours on a 2 vCPU runner.
- The same pool on the medium runner, factor 2: 50,000 / (0.5 x 2) = 50,000 job minutes, and
  50,000 / 60 = 833 hours on 4 vCPU.
- The same pool on the GPU runner, factor 7: 50,000 / (0.5 x 7) = 14,286 job minutes, and
  14,286 / 60 = 238 hours of one T4.
- The Free lane's 400 minutes on a public fork, factor 0.008: 400 / 0.008 = 50,000 job minutes,
  and 50,000 / 60 = 833 hours. That factor is why a fork of a programme project is the cheapest
  wall clock per compute minute in the slice.

⚠ The record carries a second reading of the GPU number and does not choose between them. Applied
literally, the programme factor alone gives 50,000 / 0.5 = 100,000 job minutes, or 1,667 GPU
hours. Multiplied by the runner factor it gives 238. The difference is the factor 7. The record
states both and says which arithmetic produced each; the vendor documentation does not say whether
the two factors multiply or substitute.

That gap is the finding, not a footnote. 1,667 hours and 238 hours are different products.
238 / 24 = 9.9 days of one T4. 1,667 / 24 = 69 days, which no single calendar month contains, so
the literal reading cannot be spent in the month it is granted. The multiplied reading can.

The other multiplier in the slice is RunMyJob's overage, which the record prices per second. One
vCPU-hour is 3,600 vCPU-seconds, and 3,600 x EUR 0.00002 = EUR 0.072 per vCPU-hour. A 12 vCPU job
therefore costs 12 x 0.072 = EUR 0.864 an hour in CPU, and its 32 GB costs 32 x 3,600 x
EUR 0.000001 = EUR 0.1152 an hour in memory. The two together are EUR 0.9792 an hour, and the
free pool is 400 / 12 = 33.3 minutes of that shape, so the paid meter starts at minute 34 of the
month, if the pool figure holds.

## The wall-clock cap decides, not the pool

⭐ A job killed at six hours cannot run an eight-hour job however many minutes remain in the
pool. The cap is per job and the pool is per month, and the two answer different questions. Three
of the nine rows state a per-job cap. One states that it never implemented one. Five state no cap
at all.

Codeberg is the extreme and the clearest. The largest hosted runner is 4 vCPU for 10 minutes, so
the best job is 4 x 10 = 40 CPU-minutes, which is 40 / 60 = 0.67 vCPU-hours. A job that needs
eleven minutes cannot run on that service at all, and no queue depth changes it. The `-lazy`
variant changes when the job starts, not how long it may run.

Cirrus capped a task at 2 hours with a full runtime, against a pool of 10,000 CPU-minutes. An
eight-hour job is four capped tasks at minimum, each restarting from the beginning, and the
record states that the GPU job at scipy stopped working at the end of April 2026 with no email
announcement of the timing. A concurrency of 16 CPUs on Linux with an 8-CPU cap per task means two
maximal tasks at once.

GitLab is the only record in the slice whose stated ceiling exceeds a working day: 60 minutes by
default, settable per project between 10 minutes and 1 month. The ceiling rises with
configuration, which makes it the one lane where a long job is a settings question rather than a
product question. The pool then binds: 400 minutes at the default cap is 400 / 60 = 6.7 hours.

Buildkite and RunMyJob publish no per-job cap in their records, so the pool is the ceiling. At
8 hours 20 minutes a month on Buildkite's 4-core shape, one long job spends the month. Quansight
stated the opposite: it had not implemented a time limit per job, and it is dead.

⚠ A cap is not a quota and a quota is not a cap, and the Cirrus numbers show both directions.
10,000 CPU-minutes is 10,000 / 60 = 166.7 CPU-hours. A maximal task at 8 CPUs for 2 hours spends
8 x 120 = 960 CPU-minutes, so the pool is 10,000 / 960 = 10.4 maximal tasks. The same pool on the
2-CPU default container is 10,000 / 2 = 5,000 wall-clock minutes, and the 2-hour cap turns that
into 5,000 / 120 = 41.7 tasks. Which number is true depends on the shape the caller asks for.

## What the class cannot do

Four properties hold across the records, and each one ends a plan that assumed a plain machine.

**No inbound address.** A runner dials out to the scheduler and the scheduler hands it work. No
record in this slice publishes an inbound port on a hosted runner. `inferred` from the job model,
and it is the same wall [`always-on-free.md`](always-on-free.md) sorts into tier T3.

**No state between jobs.** Every job starts from the repository and whatever cache or artifact
service the provider sells beside it. Codeberg grants 2 GB of extra temporary storage per
container, which is scratch and not persistence. The one record with storage in the offer is
Tencent CNB, at 100 GiB of repository storage plus 100 GiB of object storage, and that storage is
the product rather than a property of the runner.

**No nested virtualisation on most.** A job runs in a container on a host the provider owns. The
Codeberg topic document records that the hosted runners have no Docker daemon
([`../../ci-cd-runners/free/other-hosted.md`](../../ci-cd-runners/free/other-hosted.md)); the
record here does not carry that line, so treat it as that document's claim. Quansight exposed VMs
on OpenStack with GPUs, the one exception in the slice, and it is dead.

**No GPU without a review.** The only live GPU offer in the slice is GitLab's single T4 at cost
factor 7, and it needs a reviewed open-source namespace at the Premium or Ultimate tier. Tencent
CNB's GPU quota is 0 core-hours a month from 2026-08-01, so that lane is a card and not a quota.
Quansight's six V100 went away on 2026-03-13, and the conda-forge successor on GitHub Actions
large runners states "Sadly, we don't have GPU CI jobs yet".

## The providers that closed

Three records in this slice report a closure. The table adds a fourth whose free plan never
included compute, because a reader weighing the same decision meets it beside them. The dates are
the finding: a page cached in a search index still describes the three as usable.

| provider | what closed | date | verdict | evidence |
| --- | --- | --- | --- | --- |
| `cirrus-ci` | new customers refused, then the service | announcement 7 April 2026; shutdown 1 June 2026 | dead | `cirruslabs.org/` (read 2026-10-22): "We are no longer accepting new customers for Cirrus Runners" and "Cirrus CI will shut down effective Monday, June 1, 2026" |
| `quansight` | the host | decommissioned 2026-03-13 | dead | `github.com/Quansight/open-gpu-server` (read 2026-10-22): "The server will be decommissioned as of 2026-03-13 and the service will not be available from then on." |
| `cirun` | nothing closed; the free plan never included compute | not applicable | paid-only | `cirun.io/pricing/` (read 2026-10-22): "Always free for open source", USD 0, unlimited runners, on a cloud account the caller brings |
| `drone-ci` (self-hosted) | registration | disabled since April 2022 | paid-only | `cloud.drone.io` (read 2026-10-22): HTTP 200 with no registration route, and a support thread opened 13 April 2022 titled "User registration is disabled on cloud.drone.io" |

`cirrus-ci` is the record that stops a wasted attempt: three fetch routes to `cirrus-ci.org`
returned HTTP 530 on 2026-10-22, and the allowance survives only in mirrors of the docs. `drone-ci`
is the trap of a different kind. The domain answers 200, and the 200 proves that a front end is
running and nothing else.

## The lane that is not a machine: four inference records in this slice

Four records in this slice are not CI runners: `cohere-trial-keys`,
`google-gemini-api`, `groq-cloud` and `openrouter`. They belong here because a CI job that calls a
model spends two meters at once, and either one can be the smaller. They also show the class
boundary: an inference endpoint has no machine, so it has no per-job wall clock and no job-level
concurrency, only a request rate.

| provider | free allowance and unit | rate | what fails first | verdict |
| --- | --- | --- | --- | --- |
| `cohere-trial-keys` | 1,000 API calls a month, across every model and endpoint | Chat 20 requests a minute per model; Embed 2,000 inputs a minute | 1,000 calls: 1,000 / 20 = 50 minutes of traffic at the cap | qualifies-with-caveat |
| `google-gemini-api` | free of charge, with the quantity no longer published | 20 requests a day on Gemini 3.8 Flash, reported; 500 a day on Flash-Lite | 20 x 30 = 600 requests a month on Flash for a 30-day month | qualifies-with-caveat |
| `groq-cloud` | 200,000 tokens a day, 1,000 requests a day, 8,000 tokens a minute per model | 30 requests a minute | the minute rate: 200,000 / 8,000 = 25 minutes of continuous traffic | qualifies-with-caveat |
| `openrouter` | 50 requests a day with under 10 credits purchased in total; 20 a minute | 20 requests a minute | 50 requests: 50 / 20 = 2.5 minutes of traffic, and a 1,000-item job is 1,000 / 50 = 20 days | qualifies-with-caveat |

⭐ The composition is the useful part. A 1,000-item job that calls a free model once per item
takes 20 days on the OpenRouter no-card lane, which is 20 x 24 = 480 job-hours of continuous
running. GitLab's per-job cap can be set to a month, so the cap is not what stops it: the Free
pool is 400 minutes, which is 6.7 hours, and 480 hours does not fit in it. Tencent CNB's 160
core-hours of build at 8 vCPU is 20 hours. So the composite job fails on both meters, and the
runner fails first. The fix is one call carrying many items, which is why `cohere-trial-keys`
Embed at 2,000 inputs a minute against a 1,000-call cap is the shape that works.

The Gemini record is the warning about a withdrawn number. The pricing page still prints "Free of
charge" for input, output and caching, and the rate-limits page no longer carries a free-tier
table at all. The 20-a-day figure is `reported` from a developer forum post dated 2026-09-03, not
a vendor number, and the record says so.

## How it composes

**A reviewed GitLab namespace plus CNB's development pool.** GitLab's programme, once approved,
gives 238 GPU hours of one T4 a month on the multiplied reading, and the same namespace gives
1,667 hours of 2 vCPU build time at factor 0.5. Tencent CNB's build pool is 160 core-hours a
month, which is 160 / 8 = 20 hours on an 8 vCPU shape, and its separate development pool of
1,600 core-hours is 200 hours that a build cannot spend. The scarce link is the
GitLab review, which is annual.

**A scheduler with no machine plus a machine with no scheduler.** Buildkite's free plan supplies
10 concurrent jobs and a control plane, and its record states the gap plainly: the agent is the
caller's. Cirun has the same shape at a different layer, and it needs a billed cloud account
before it schedules anything. Neither adds capacity on its own, which is why both records carry a
caveat rather than a qualification.

**A short-job lane beside a long-job lane.** Codeberg's 40 CPU-minutes per job runs a formatter,
a type check, or a small suite with no published monthly count. GitLab's 400 minutes at a
one-month cap runs the job that needs more than ten minutes. The scarce link is that the two hold
different repositories, so the source has to be mirrored.

## What would change the answer

- **One line in GitLab's compute-minutes page** stating whether the project factor and the runner
  factor multiply. That single sentence moves the GPU lane between 238 and 1,667 hours a month,
  which is the largest unresolved number in the slice.
- **A live `cirrus-ci.org` page.** The record rests on mirrors and an announcement. If the origin
  answers again with a free tier, the verdict moves from `dead` to a live lane with a 2-hour cap.
- **A first-party RunMyJob pricing page** that states the monthly vCPU-minute pool and a per-job
  cap. The record's figures come from `runmyjob.io`, which redirects to `runjob.eu`; the URL
  cited for the free plan returns HTTP 404.
- **A Codeberg label above 10 minutes.** The record's binding constraint is the wall clock, not
  the pool, so one new runner shape changes the verdict without changing any quota.
- **A restored CNB GPU quota.** It went to 0 core-hours on 2026-08-01 and the overage is
  CNY 0.5 per core-hour, so any GPU job there is paid from the first core-hour.
- **A Buildkite hosted agent on the free plan.** The free pool is metered in vCPU-minutes of an
  agent the caller supplies. A hosted agent inside the free plan would make the 10-job
  concurrency worth something.

## What this document does not settle

Two records disagree with themselves, and neither disagreement can be resolved from the record.

⚠ **Cirrus credit arithmetic.** The FAQ row states 50 compute credits equal 10,000 Linux
CPU-minutes, which is 10,000 / 50 = 200 CPU-minutes per credit. The pricing row states 1,000
minutes of 1 virtual CPU for 3 compute credits, which is 1,000 / 3 = 333.3 CPU-minutes per credit.
The two rows differ by a factor of 1.67. Either the two pages describe different credit pools, or
one of them is stale. The provider is dead, so the number no longer has a decision attached, but
the record keeps both rows and a reader should not average them.

⚠ **The Codeberg CPU counts.** This record carries 1, 2 and 4 CPU for the three labels. A reader
who has the older 2, 4 and 8 figures will overstate each job by a factor of two.

The four inference records are not CI
runners and they have no job cap. The compute topic's own page for that lane is
[`README.md`](README.md) in this directory, and the inference topic is
[`../../inference/README.md`](../../inference/README.md).
