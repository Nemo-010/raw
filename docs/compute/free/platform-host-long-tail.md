# The platform-host long tail: 15 records, and the two free ones are not machines

The `platform host` category holds 83 records; this page covers 15 of them.
[`platform-hosts.md`](platform-hosts.md) names 31 of them by slug or by the exact provider
string, which leaves 21. Six of those 21 are discussed under a form that differs from the
record: Azure App Service (F1), Bitbucket Pipelines, the second Cloudflare Containers
record, Fly.io Machines, Hugging Face Spaces Dev Mode and InsForge (InstaCloud). The 15
that are left appear in no document, and they are this page. `paid/ci-adjacent.md` names
none of the 52.

To reproduce the 15, match each record's `slug` and `provider` against both documents, then
check the six names above.

The answer, in one paragraph. ⛔ **Two of the 15 claim free capacity, and neither supplies the
machine.** Hatchet's 100,000 free runs execute on workers a reader deploys elsewhere. The
self-hosted RunsOn has a free licence that provisions GitHub Actions runners into an AWS account of the reader's
own at spot prices. The other 13 hold no free tier, are withdrawn, or are not a machine at all.
⚠ **Not one of the 15 states a numeric sleep window or session cap.** So the question that
decides this class, whether a free tier keeps a process awake, is unanswerable from this slice
in either direction.

## The 15, grouped by who supplies the machine

Sorted by the mechanism. `Who supplies the machine` is the deciding column: a free control
plane over a cloud account the reader must open and pay is worth zero here.

| Provider | What the free tier is | Who supplies the machine | Clock stated | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Hatchet | 100,000 runs, no card | the reader, on whatever platform it deploys workers to | none; a run is a task in a DAG | email | qualifies-with-caveat |
| Caution | none; confidential compute by appointment | the reader, its own AWS Nitro enclave | none | email, unverified | paid-only |
| Aptible | none; a billing account is the only route | the vendor, in its own AWS environment | none | email, unverified | paid-only |
| Hugging Face Jobs | none; every Job bills by the minute | the vendor | none; the reader sets the timeout | email, unverified | paid-only |
| Nextmv | none; the page carries no plan and no price | the vendor | none | email, unverified | paid-only |
| Shuttle | none; a Rust deploy platform on the vendor's AWS | the vendor | none | email, unverified | paid-only |
| Hugging Face Spaces (CPU Basic) | the 2 vCPU hardware is free; creating a Space is not | the vendor | a Space sleeps after inactivity, interval unstated | card, PRO at USD 9 a month | paid-only |
| Tinfoil | none; an inference API | not applicable, it answers tokens | none | email, unverified | paid-only |
| Cloudflare Workers for Platforms | none; USD 25 a month | the vendor, an isolate per request | none | email, unverified | paid-only |
| Heroic Labs | none; the framework is open source and the hosted product is not | neither; no capacity is sold | none | email, unverified | paid-only |
| Ploomber | not established; no route returned the page | unknown | none | email, unverified | paid-only |
| Hyrex | withdrawn | none | none | email, unverified | dead |
| KubeSail | the hosted service has stopped | none | none | email, unverified | dead |
| RunsOn (self-hosted) | a licence at EUR 0 for open source or non-profit use | the reader, an AWS account of its own at spot prices | none; an ephemeral instance per job | email | qualifies-with-caveat |
| Trainy (self-hosted) | none; orchestration over GPUs rented elsewhere | the reader, or whoever it rents GPUs from | none | email, unverified | paid-only |

The verdict split is 11 `paid-only`, 2 `qualifies-with-caveat` and 2 `dead`. Thirteen of the
15 carry `extras.free_tier_kind: none`, and the two that do not are the two `qualifies*` rows:
Hatchet at `one-time-credit` and RunsOn at `allowance`.

**Two fields are empty across almost the whole slice.** Fourteen of the 15 declare
`interface: unknown`, so the slice says nothing about how a reader reaches these products. All
15 publish no egress term. A reader who needs a route in, or a cost out, gets a dash on every
row here.
## The six that put the machine in the reader's hands

⭐ **This is the finding, and the other document undercounts it.** `platform-hosts.md` says
two records in the class need an existing cloud account: Porter and Dockup. The records hold
six. The four it does not name are Hatchet, Caution, and the
self-hosted RunsOn and Trainy. Each states the mechanism in its own `free_tier.stated`.
Zeabur is not in the class: its Free Plan deploys serverless services on Zeabur's own compute.

| Provider | Where the machine runs | In this page | Verdict |
| --- | --- | --- | --- |
| Porter | an AWS, Azure or Google Cloud account of the reader's own | no | qualifies-with-caveat |
| Dockup | an AWS account of the reader's own | no | qualifies-with-caveat |
| Hatchet | on a container platform the reader deploys to, such as Railway or ECS | yes | qualifies-with-caveat |
| Caution | the reader's AWS Nitro enclave | yes | paid-only |
| RunsOn (self-hosted) | an AWS account of the reader's own, at spot prices | yes | qualifies-with-caveat |
| Trainy (self-hosted) | GPUs the reader rents elsewhere | yes | paid-only |

⛔ **Four of the six carry a `qualifies*` verdict.** In the storage vocabulary this corpus
inherited, `qualifies` means "at least 500 GB free per unit". Here it means the control plane is
free. The corpus assumes no cloud account and no machine, so these four verdicts describe software
a reader cannot run. A reader filtering on the verdict gets them mixed with the rows that
supply a machine.

Hatchet is the mildest of the six. Its page names Kubernetes, Porter, Railway, Render, ECS and
"any container platform" (`hatchet.run`, read 2026-10-22). So the workers can run on a host the
reader already pays for, rather than on a cloud account it must open. The free unit is still
runs against a queue and still not machine time. The row is recorded as bring-your-own because
no machine comes with it.

The distinction the class needs is not price. It is who owns the invoice for the CPU. Caution
and Trainy already say `paid-only`, which is answerable. For the four `qualifies*` rows the
record names a `binding` that hides the reason. Three say `write-gated` and Hatchet says
`request-rate`. ⚠ **Not one of the four names the real gate.**
The gate is that the reader must arrive with somewhere to run the work before the free tier does
anything.

## The one rate card in the slice, and the arithmetic it decides

Hugging Face Jobs is the only record here that publishes a machine price with a shape. CPU
Basic is 2 vCPU, 16 GB and 50 GB of ephemeral disk at USD 0.01 an hour
(`huggingface.co/docs/hub/en/jobs-pricing`, read 2026-10-22). It bills by the minute only while
the Job is Starting or Running. The GPU ladder runs from a T4 at USD 0.40 an hour to eight L40S
at USD 23.50 an hour.

That price decides something a reader can act on. At 10 hours a day, which is 300 hours a
month, CPU Basic is USD 3.00 and the top row is USD 7,050.00. The top shape is 2,350 times the
bottom shape. So "Hugging Face Jobs" as a lane name spans three orders of magnitude. A reader
quoting one figure for it has quoted the wrong shape.

⚠ **The record's seed money figure does not match its own page.** `huggingface-jobs.json`
carries `talaria_m10h_usd: 12.00`, which is USD 0.04 an hour over 300 hours. It also carries
`talaria_m24h_usd: 16.20`, which is USD 0.022 an hour over 730. The page states USD 0.01. The
two seed figures imply different rates from each other, so neither restates the page. Use the
page and not the money column.

## What USD 25 a month buys over the free Workers row

Cloudflare Workers for Platforms is `paid-only` at USD 25 a month for 20,000,000 requests,
60,000,000 CPU-milliseconds and 1,000 scripts
(`developers.cloudflare.com/cloudflare-for-platforms/workers-for-platforms/reference/pricing/`,
read 2026-10-22). The arithmetic is the finding. 60,000,000 milliseconds is 60,000 seconds,
which is 16.67 hours of CPU a month, and 20,000,000 requests spread over 30 days is 7.7
requests a second.

The free Workers row it replaces gives 100,000 requests a day and 10 milliseconds of CPU per
request (`dossier/compute/cloudflare-workers.json`). That is 1,000 seconds a day and 30,000
seconds a month, or 8.33 hours. So USD 25 a month buys twice the CPU and 6.7 times the requests
of the free row. Workers for Platforms is a product for reselling Workers to customers, not a
compute upgrade. A reader looking for more CPU here should read `free/runtimes-serverless.md`,
which owns that lane.

## The highest money figure in the topic, on a row with no price

Nextmv carries `talaria_m10h_usd: 2916.00`. One hundred and seventy-three records in this topic
carry both a ten-hour and a 24-hour figure, and that is the largest of them. Its 24-hour figure
of USD 6,998.40 is the largest there too. The record is `paid-only`, its `confidence` is
`reported`, its page read found "no plan and no price", and it carries no `extras.shape`.

A number with no shape is not a price, by this topic's own rule. So the top of the money column
is a figure no reader should use. Four more rows here have the same defect. Aptible carries
USD 559.00, Tinfoil USD 68.00, RunsOn USD 61.57 and Workers for Platforms USD 48.20, and none
has a shape. Only Hugging Face Jobs carries both.

## Where this page disagrees with the other documents

**`platform-hosts.md` says two bring-your-own-iron rows and the class holds six.** The four
it omits are in the table above. Each one's `free_tier.stated` names the mechanism, and the
sentence is the vendor's own.

**`platform-hosts.md` counts three free-tier kinds and the records name eleven.** Its three
counts are 20 allowances, 24 with no free tier, and 4 recurring credits, against 17, 24 and 2
in the canonical `extras.free_tier_kind` strings; they sum to 48 of the 83 records the
category holds. The records also hold 3 `trial`, 2 `trial-only` and 1 `one-time-credit`, plus
ten spellings used once each that no census groups.

⚠ **`paid/minimum-bill.md` has an arithmetic defect in the column that decides its own
section.** The section prices a 30-minute workload. Its `Penalty` column reads 4x on every
3,600-second row, and the two bill columns in the same row double a figure. Civo goes USD 8.93
to USD 17.86, and 17.86 divided by 8.93 is 2.00. On 25 of the 26 rows the penalty is the
minimum billed divided by 900 seconds, and 900 seconds is 15 minutes. So the table's penalty
assumes a 15-minute run while its section states 30, and MacStadium is the exception. A reader
who quotes the 4x is quoting a factor the adjacent two columns do not show.

⚠ **The page also prices two rows here at figures their records do not carry.** It lists
Aptible at USD 60.00 and Tinfoil at USD 48.00 for one run, at 2 vCPU and 4 GiB.
`aptible.json` holds USD 559.00 at 10 hours a day, which is USD 1.86 an hour. It carries no
`extras.shape` at all, so the figure is not traceable to a 2 vCPU price. `tinfoil.json` holds
USD 68.00 at 10 hours a day, which is USD 0.23 an hour. Its 3,600-second minimum appears in no
record field.

**`gaps.md` names five products as whole-product `unverified` rows, and two of the five are not
`unverified`.** The sentence reads "Thirteen records are `unverified` and five of them are
whole products". It then names Azure App Service F1, Hugging Face ZeroGPU, GKE Agent Sandbox,
STACKIT and Vultr Cloud GPU. Only three carry that rung: `gke-agent-sandbox.json`,
`stackit.json` and `vultr-gpu.json`. `azure-app-service-f1.json` carries `documented` and
`huggingface-spaces-zerogpu.json` carries `reported`. So two of the five are products whose
numbers were read. The rung total of 13 is right, and the roster is not.

**Four Hugging Face records sit in this category, not three.** `platform-hosts.md` states that
"three records carry the three spellings and all three say `paid-only`", and that is right about
Spaces. The fourth is `huggingface-jobs`. That is a different product in the same category, with
a different finding. It has no free allowance and a rate card that states a shape. A reader
treating "Hugging Face" as one row misses that the Jobs path prices a machine and the Spaces
path does not.

## The CI row

RunsOn is CI in all but name. Its free licence provisions GitHub Actions runners into the
an AWS account of the reader's own, and `ci-cd-runners` owns its numbers, which this page does not
restate. The class's other four CI records are Azure Pipelines, Google Cloud Build, AWS
CodeBuild and Bitbucket Pipelines. `platform-hosts.md` covers them, and their rates belong to
the same topic.

## What did not work

- **Hatchet as a free workflow host**: the 100,000 runs are orchestration against a queue, and
  the workers that do the work run on the reader's own platform.
- **Ploomber as a finding**: no route returned the page on 2026-10-22, and the fetch route
  answered with the broker refusing rather than the origin.
- **Hyrex as a product**: the origin returns HTTP 402 with "This deployment is temporarily
  paused".
- **KubeSail as a product**: the page is a shutdown notice, and the self-hosted Kubernetes
  path is a different product.
- **Tinfoil and Workers for Platforms as machines**: one answers tokens and the other runs an
  isolate per request, so neither has a session to hold.
- **Hugging Face compute Spaces as free capacity**: the hardware is free and the right to
  create it needs PRO at USD 9 a month.
- **RunsOn as a free runner** (self-hosted): the licence is free under a stated condition and the instances
  bill to an AWS account of the reader's own at spot prices.

## What this does not establish

⛔ **Nothing here was booted.** No record in this file carries the `measured` rung, and this
page repeats that. Every number is a vendor page read on the date the evidence entry gives.
Eleven of the 15 are `documented`, three are `reported` and one is `unverified`.

**Whether any of these stays awake. None of the 15 states a clock.** Seven of the class's 83
records carry a numeric sleep window or session cap — Azure App Service F1, Bitbucket Pipelines,
Koyeb, Modal, Render, Vercel and Yepcode — and none of them is in this page. The long tail
contributes no clock at all, so the class's central question has an answer on 8 per cent of its
records.

**Whether 10 of the 15 were read on the date the evidence gives.** Their
`free_tier.read_on` is 2026-10-02, inherited from the catalogue card. All 15 carry an evidence
entry dated 2026-10-22 with a quoted sentence. The evidence array is the newer statement, and
the `read_on` field was not updated with it.

**What a Ploomber row is.** Its `limits` array is empty, its `binding` is absent, and no page
answered. A reader should treat it as absent rather than as a product. One browser session
would settle it.

**Whether the five `qualifies*` bring-your-own-cloud rows cost anything in practice.** No AWS
account was opened. So the spot price, the egress bill and the idle volume on those rows are all
unpriced here. A free control plane over an unpriced bill is not a free resource.
