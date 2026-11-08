# Platform hosts: the free PaaS, and the three that need an existing cloud account

Eighty-three records carry `category: platform host`, which is the label this topic uses
for everything that runs a program without giving a reader a machine to administer: a PaaS, a
build service, a workflow engine, an MCP gateway. Twenty are allowances, counted over the
same eleven kind strings `free-tier-census.md` uses, 24 have no free tier at all
(`extras.free_tier_kind: none`), and four carry a recurring credit.

The answer, in one paragraph. **Six hosted free platform hosts will keep a process
answering without a session cap**, and the best of them are not the most famous.
Northflank's free sandbox is described as always-on with no sleeping, and the catch is
that a payment method is mandatory on every plan. Wasmer gives 6 compute hours and 150 GB
of bandwidth forever. Render spins down after 15 minutes and Koyeb after an hour, and
both are honest about it. ⚠ **And five records in the topic are not free capacity at
all: they deploy into a cloud account the reader must already have**, which is
the same as not being an option.

## The comparison

Sorted by whether a process stays up with no keepalive, which is the only question that
separates a PaaS from a sandbox.

| Provider | Free allowance | Stays up? | Identity | Verdict |
| --- | --- | --- | --- | --- |
| Northflank | 2 services, 2 cron jobs, 1 addon | yes, "no sleeping" stated | card, mandatory on every plan | qualifies-with-caveat |
| Wasmer | 6 compute hours, 150 GB bandwidth | yes, an edge isolate | email | qualifies-with-caveat |
| Azure App Service F1 | 60 CPU-minutes a day, 1 GB | 20-minute idle timeout | card | qualifies-with-caveat |
| Koyeb | 1 web Service, 512 MB, 0.1 vCPU | scales to zero after 1 hour | email | qualifies-with-caveat |
| Render | 512 MB, 750 instance-hours a month | spins down after 15 minutes | email | qualifies-with-caveat |
| Modelence | a free tier for hobby projects | yes, "operates your app 24/7" | email | qualifies-with-caveat |
| Specific | unlimited API requests, limited compute | not stated | email | qualifies-with-caveat |
| Reflex | a Free plan with a periodic refill | not stated | email | qualifies-with-caveat |
| Metorial | a free Dev plan | an MCP gateway, no session | email | qualifies-with-caveat |
| Agent Relay | free to start, no priced tier | a message handoff, no session | email | qualifies-with-caveat |
| Apoxy | a free plan during an invite-only beta | a tunnel, no inbound port | email | qualifies-with-caveat |
| Skyhook | a Kubernetes PaaS, no card | not stated | email | qualifies-with-caveat |
| Yepcode | 50,000 seconds, 300 runs a day | 30-second cap per execution | email | qualifies-with-caveat |
| Trigger.dev | USD 5 a month, 20 concurrent runs | no card | email | qualifies-with-caveat |
| InsForge Instacloud | USD 10 a month, 4 vCPU | a project pauses | email | qualifies-with-caveat |
| Modal | USD 30 a month | 5-minute default lifetime | email | qualifies-with-caveat |
| Railway | USD 1 a month | 24 hours on the anonymous box | email | trial-only |
| Azure Pipelines | 1,800 hosted minutes a month | a job, not a service | email | qualifies-with-caveat |
| Google Cloud Build | 2,500 build-minutes a month | a build, not a service | email | qualifies-with-caveat |
| Cloudflare Containers | none; USD 5 Workers Paid |  -  | email | paid-only |
| Hugging Face Spaces | static only; compute needs PRO |  -  | card | paid-only |
| Heroku | a free tier on the catalogue card, not read |  -  | email | qualifies-with-caveat |
| Windmill Cloud | 1,000 executions a month, no card | not stated | email | qualifies-with-caveat |
| Windmill (self-hosted) | unlimited executions, open source | yes, on your own worker | email | qualifies-with-caveat |

⚠ **Five rows in that table are labelled `qualifies-with-caveat` on a catalogue card
that has not been read**: Heroku, Clever Cloud, Eventual, AWS CodeBuild and OpenShift. Their `free_tier.stated` is the literal sentence "the source card records a
free tier without a credit amount".
That is a placeholder and not a finding, and it is the weakest evidence anywhere in this
topic.

## The two that need an existing cloud account

| Provider | What it is | Where the machine runs |
| --- | --- | --- |
| Porter | a startup programme, 6 months free | an AWS, Azure or GCP account of the reader's own |
| Dockup | a Free-forever plan | an AWS account of the reader's own |

⛔ **Both sell orchestration and supply no capacity.** A free control plane over a bill
that starts at the first deployment is worth zero. `METHODOLOGY.md` section 12a separates
the two: self-hosted software on a rented or free machine is the last resort, after every
hosted offer, while owning the machine is out of scope. These two put
the infrastructure in the reader's name, and the price of that infrastructure is the
whole cost.

Mastra is not in this class. Its hosted Mastra Platform has a Starter plan at USD 0 a month with
100K events and 24 CPU hours, and Manufact has a hosted Free plan with USD 5 of credits a month and
1 project, no card (`documented`, `mastra.ai/pricing` and `manufact.com/pricing`, read 2026-10-29).

⚠ **Two more records in the topic claim a similar shape and do not have it.**
`ellipsis` bills its compute to an AWS account of the reader's own at USD 0.142 a vCPU-hour, so it
belongs in this list and is filed under `container and VM sandbox`. `omnara` offers both
paths: self-managed machines for nothing, or USD 0.0414 a GiB-hour of memory for an
Omnara-managed machine that auto-sleeps. ⭐ **Omnara's managed row is real capacity and
its own-machines row is not**, which makes it the only record in the topic where the same
provider is both a free resource and a bring-your-own-machine product.

**Zeabur is not in this class.** Its Free Plan deploys serverless services on Zeabur's
own compute, with no card, and they sleep after a period of inactivity (`documented`,
`zeabur.com/docs/en-US/pricing/free-plan`, read 2026-10-24). Managing a self-hosted server
is one row of its feature table, not the free tier. What is not established is
whether the Free Plan carries a compute allowance at all, and how long a service stays
awake.

## Northflank, the one that does not sleep

A free sandbox with 2 services, 2 cron jobs and 1 addon, described as always-on with no
sleeping, and ⛔ **a payment method is mandatory for every user regardless of plan**
(`reported`, `northflank.com/pricing`).

⭐ **This is the only row in the class that claims to keep a process up for free and
names the reason it can**: a card on file means the vendor is not absorbing a stranger's
idle compute. The card is the price of the no-sleep promise.

⚠ The record is `reported` and not `documented`, so the page has not been read
directly. That is the one verification this row needs.

## Render and Koyeb, the two that sleep honestly

**Render.** 512 MB of RAM, less than one CPU, an ephemeral filesystem, and 750 free
instance-hours per workspace a month, spinning down after 15 minutes without inbound
traffic counted as HTTP requests or WebSocket messages (`reported`, `render.com/docs/free`).

⚠ **The filesystem is ephemeral, so a spin-down loses every change.** 750 hours is 31.25
days, which is one service always on and nothing else.

**Koyeb.** One free web Service in Frankfurt or Washington, D.C. with 512 MB, 0.1 vCPU
and 2 GB of SSD, scaling to zero after one hour without traffic with the interval not
configurable, plus one free PostgreSQL database with 5 hours of active time and 1 GB of
storage (`documented`, `koyeb.com/docs/faqs/pricing`, read 2026-10-22).

⛔ **Volumes are disabled on the free instance**, so it cannot hold state, and 0.1 vCPU
is one tenth of a core. The one-hour window is four times Render's and both lose the
filesystem.

## Azure App Service F1, and the keepalive that fails

60 CPU-minutes a day, 1 GB of RAM, 1.00 GB of storage and no SLA, timing an app out after
20 minutes without a direct request (`documented`,
`learn.microsoft.com/en-us/azure/app-service/webjobs-execution`, read 2026-10-22).

⭐ **The page adds the part that decides a keepalive: only a direct request resets the
timer, and a portal visit or a Kudu request does not.** A cron that pings the management
endpoint every ten minutes keeps nothing awake.

⚠ **60 CPU-minutes a day is the other wall.** An app that is awake all day and uses more
than 60 minutes of CPU stops, regardless of idleness.

## The edge and workflow rows

**Wasmer.** Free forever: 150 GB of bandwidth, a global edge CDN and 6 compute hours on a
single seat (`documented`, `wasmer.io/pricing`, read 2026-10-22). Six compute hours is a
month of light use and it is an isolate rather than a machine.

**Yepcode.** 50,000 Yeps, which are seconds of execution time, with 300 executions a day,
a 30-second cap per execution, one concurrent execution, and 5 storage files of 5 MB each
(`documented`, `yepcode.io/pricing`, read 2026-10-22). ⛔ **The 30-second cap is the
binding constraint** and 50,000 seconds is 13.9 hours spread across many runs.

**Specific.** Free with unlimited API requests and users but limited compute per service,
and ⚠ **the USD 25 of usage credits arrives on the first paid tier, not on Free**
(`documented`, `specific.dev/pricing`, read 2026-10-22).

**Reflex.** A Free plan at USD 0 with limited usage for AI generation and hosting that
refills periodically, with paid tiers from USD 25 to USD 200 carrying an allowance equal
to the price (`documented`, `reflex.dev/pricing`, read 2026-10-22).

**Trigger.dev.** USD 5 a month of free credits with 20 concurrent runs and unlimited
tasks, no card (`documented`, read 2026-10-22). It is one of the twelve recurring credits
in the topic.

**Windmill Cloud.** The hosted Community plan starts with 1,000 executions a month, with no
credit card and an SSO sign-up (`documented`, `windmill.dev/docs`, read 2026-10-29).

**Windmill (self-hosted).** Free and open source at USD 0 a month with unlimited
executions, with Enterprise Self-Host from USD 120 a month (`documented`, `windmill.dev`,
read 2026-10-29). ⚠ "Unlimited executions" is on a worker the reader runs, so it is the
last resort; Windmill Cloud is the hosted lane.

## The build services, which are not this topic's

Four records here are CI in everything but name: **Azure Pipelines** at 1,800 hosted
minutes a month plus one self-hosted job with unlimited minutes, **Google Cloud Build** at
2,500 build-minutes a month on e2-standard-2, **AWS CodeBuild**, and **Bitbucket
Pipelines**, whose page does not render the Free plan's build-minute allowance at all.

`paid/ci-adjacent.md` states the boundary and `ci-cd-runners` owns the numbers. They are
recorded here because a build service is a machine that runs for the length of a job, and
they are not restated because a second copy of a number goes stale on its own schedule.

## What is dead or paid in this class

**Fly.io and Fly Machines** are `dead` in this topic, and both records say the same
sentence: new organisations get no free tier and no monthly free usage allowance, and the
trial is up to 2 hours of Machine runtime or 7 days. Two records for one product is a
merge artefact and both are kept.

**Cloudflare Containers** has no free plan; usage is included with the USD 5 a month
Workers Paid plan. The free Durable Object row is the substitute and it is in
`free/always-on-free.md`.

**Hugging Face Spaces** is the class's clearest create-time gate. Static Spaces are free,
and creating a Gradio or Docker Space requires a paid plan, PRO for personal accounts.
Three records carry the three spellings and all three say `paid-only`.

**Heroku, Clever Cloud and Eventual** carry a free tier on a catalogue card and
no page read. They are the three rows to verify first, because a `qualifies`
verdict resting on a placeholder is the weakest claim in the topic.

## What this class does not establish

⛔ **No platform here was deployed to.** Every idle window, memory cap and minute allowance
is a vendor sentence. The class carries no `measured` record, and no sleep window here was
measured: Render spins down after 15 minutes, Koyeb after an hour, and Northflank's sandbox
is described as always-on.

**No card-free path to a no-sleep PaaS was found.** Northflank wants a card on every plan,
Azure wants one, and the rows that ask for an email only either sleep or need a cloud
account.

**The three placeholder rows are unresolved.** Heroku, Clever Cloud and Eventual
would each take one page read, and none has been done.

## What did not work

- **Heroku's free tier**: a catalogue card asserts one and no page was read.
- **Porter, Dockup, Ellipsis and Omnara**: free control planes over an existing
  cloud account, which is not a free machine.
- **Fly.io**: closed to new organisations.
- **Cloudflare Containers**: USD 5 a month, and Durable Objects is the free substitute.
- **Hugging Face compute Spaces**: a create-time PRO gate.
- **Yepcode as a long-running host**: a 30-second cap per execution.
