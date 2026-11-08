# Research grids and science gateways: what an email address alone reaches

One question: what compute does a university, a national laboratory or a research
network give to a person outside its own institution?
[`hpc-allocations.md`](hpc-allocations.md) answers it for the panel-reviewed calls and
finds sixteen of seventeen records closed. This page covers the other half: the grids,
the gateways and the small-compute routes that open continuously and award far less.

Nineteen records. Seven open with an email address and a click. One more, EGI Cloud
Compute, opens with a contact form a person answers. Eleven need an institution, an
employer in a named country, or a residency the reader does not hold. The seven give
625 GB of hosted storage, 200 core-hours a year and no GPU-hours at all. The zero is
the finding.

## The short answer

**The route an email address alone reaches is Galaxy Main.** Registration is "email,
password, user name and go". The account carries 250 GB of storage and 6 concurrent
jobs, and the jobs run on TACC, Jetstream2 and PSC Bridges hardware
(`galaxyproject.org/main/`, read 2026-10-22). Two sibling servers issue separate
accounts to the same address: Galaxy Europe at 250 GB and Galaxy Australia at 100 GB
for a non-Australian address. ⭐ Those three are the only place in this slice where a
free account reaches hardware that the programmes in
[`hpc-allocations.md`](hpc-allocations.md) gate behind an institutional signature.

**The largest award on the page is SURF Small Compute.** One application may ask for
1,000,000 Snellius SBU, 500,000 LUMI CPU core-hours, 14,000 LUMI GPU-hours,
1,000,000 CPU core-hours on Grid and Spider, and 50,000 CPU core-hours or 5,000
GPU-hours on HPC Cloud, for one year
(`surf.nl/en/small-compute-applications-nwo`, read 2026-10-22). Review is a
feasibility check rather than a merit panel, and it takes about two weeks. The
applicant must hold a Dutch appointment before the review starts.

**The honest total is 625 GB, 200 core-hours and no GPU.** The seven self-service
accounts add to 625 GB of storage across six operators' hardware and 200 core-hours a
year at CyVerse. The GPU figures here, 6,250 A100-hours, 82,400 A100-hours, 14,000
LUMI GPU-hours and 1,500 Derecho GPU-hours, all sit behind an institution. A reader
who wants GPU time from this class needs a door the reader cannot open.

## The nineteen records, by the door each one opens

Sorted from the loosest door to the tightest. The fourth column decides the row.

| Provider | What it gives | How to apply | PI or institution required | Verdict |
| --- | --- | --- | --- | --- |
| `galaxy-main` | 250 GB hosted data, 6 concurrent jobs, TACC and PSC hardware behind tool wrappers | email registration, automated | No | qualifies-with-caveat |
| `galaxy-europe` | 250 GB hosted data, no request path for more | email registration, automated | No | qualifies-with-caveat |
| `galaxy-australia` | 100 GB hosted data for a non-Australian address, removed after 365 days | email registration, automated | No | qualifies-with-caveat |
| `nanohub` | 10 GB storage, 3 simultaneous app sessions, 600-plus published apps | Google or email registration | No | qualifies-with-caveat |
| `sciserver` | 10 GB persistent storage, 3 containers, SDSS and Gaia data beside them | email registration | No | qualifies-with-caveat |
| `cyverse` | 5 GB Data Store, 200 core-hours a year, where 1 compute unit is 1 core-hour, 1 concurrent job | email registration | No | qualifies-with-caveat |
| `quantum-inspire` | Tuna 5, 9 and 17 transmon devices, 3 queued hardware jobs | email registration, no card | No | qualifies-with-caveat |
| `egi-cloud-compute` | 4 vCPU, 8 GB RAM, 100 GB block storage, one trial VM | contact form, answered by a person | No, but a human decides | trial-only |
| `cloudlab` | bare-metal nodes with no allocation counter, 9,336 cores at Utah across 1,000-plus nodes | project form, staff review of a few days | Yes: faculty or senior research staff | fails-identity |
| `fabric` | experiment slices across 29 sites, with GPU, SmartNIC, FPGA and NVMe | CILogon login, then project membership | Yes, per the teaching material; contested | fails-identity |
| `ospool` | opportunistic pool, 844K core-hours in one day, 1,000s concurrent cores per user | OSG portal account | Yes: US academic affiliation | fails-identity |
| `jetstream2` | 64 SU per g3.xl hour, so 6,250 A100-hours on a 400,000-credit Explore award | ACCESS allocation request | Yes: ACCESS institution and non-generic email | fails-identity |
| `nsf-ncar-derecho` | 500,000 core-hours and 1,500 GPU-hours, with no funding award needed | continuous, any time | Yes: US-based, Earth system science | fails-identity |
| `nersc-exploratory` | 250 Perlmutter node-hours, which is 32,000 core-hours, for 18 months | any time, decision in four weeks | Yes: Institutional User Agreement | fails-identity |
| `designsafe-ci` | 20,000 node-hours a year on Startup, 100,000 on Research | portal account, then allocation form | Yes: US institution PI | fails-identity |
| `cscs-small` | 8,000 Alps node-hours a year on GH200 nodes, 250 node-hours on the preparatory step | proposal at any time, decision in two months | Yes: Swiss academic postdoc | fails-identity |
| `surf` | 1,000,000 Snellius SBU, 500,000 LUMI CPU core-hours, 14,000 LUMI GPU-hours, 50,000 HPC Cloud core-hours | Small Compute form, two-week feasibility check | Yes: Dutch appointment | fails-identity |
| `it4innovations-open-access` | 95,600 Karolina CPU node-hours, 10,300 Karolina GPU node-hours, 15,500 LUMI-G node-hours, 198,200 QPU seconds per request | competition three times a year | Yes: employee of a Czech research organisation | fails-identity |
| `grid-5000` | roughly 1,000 nodes, reserved by name rather than queued | account form, French-site justification | Yes, and the open-access route is withdrawn | fails-identity |

Eleven rows return `fails-identity`, seven return `qualifies-with-caveat` and one
returns `trial-only`. ⚠ The verdict grades the door, not the machine. `surf` and
`nsf-ncar-derecho` carry the largest numbers on the page and the tightest doors.

## The distinction that decides everything

Three doors, and a programme belongs to exactly one of them. The name of the door
predicts the identity cost before any page is read.

| Class | What the door asks for | Records here | What the award is |
| --- | --- | --- | --- |
| Panel-reviewed allocation | A PI, an employer, and often a signature from the institution | `cscs-small`, `designsafe-ci`, `it4innovations-open-access`, `nersc-exploratory`, `nsf-ncar-derecho`, `surf` | node-hours or core-hours for months |
| Science gateway | An email address and a click | `galaxy-main`, `galaxy-europe`, `galaxy-australia`, `nanohub`, `sciserver`, `cyverse`, `quantum-inspire` | storage and concurrent slots, rarely hours |
| National grid or testbed | Residency, an institutional login, or a project leader in a senior post | `cloudlab`, `fabric`, `grid-5000`, `jetstream2`, `ospool` | a queue slot or a reservation |

The panel-reviewed door fails on a document rather than on merit. NERSC states the
mechanism plainly: an Institutional User Agreement between Berkeley Lab and the PI's
sponsoring organisation is required when the project is not federally funded
(`nersc.gov/users/become-a-nersc-user/working-with-us`, read 2026-10-22). The science
is not the obstacle. A signature is.

The gateway door fails on nothing and gives nothing large. It issues an account to an
address, and the award is counted in gigabytes and concurrent slots because the
service carries the cost. Galaxy Europe says why its quota request form was withdrawn:
storage "has become increasingly scarce and expensive"
(`galaxyproject.org/eu/storage/`, read 2026-10-22).

The grid door fails on where a person lives or works. OSPool states the test in one
sentence: "The OSPool is a source of computing capacity that is accessible to any
researcher affiliated with a US academic institution" (`osg-htc.org/services/ospool/`,
read 2026-10-22).

⚠ Three records sit between two classes and each is recorded at the weaker reading.
`ospool` has a guest notebook that needs no account, so a few HTCondor jobs are
reachable, but the 844K core-hours a day are not. `egi-cloud-compute` asks for an email
and routes it to a person, so the identity is loose and the decision is human. `fabric`
defaults its portal to ORCID, while its teaching material says institutional login is
required and that ORCID "might require extra approvals".

## What an email address reaches

Seven accounts, all self-service. Six publish storage, and the last column is the wall.

| Service | Storage | Concurrent slots | The wall |
| --- | --- | --- | --- |
| `galaxy-main` | 250 GB | 6 jobs | 250 GB reached stops new jobs until data is purged; walltime 36 to 48 hours |
| `galaxy-europe` | 250 GB | not published | fixed ceiling, no request path, no new jobs start at the limit |
| `galaxy-australia` | 100 GB | not published | data removed 365 days after upload |
| `nanohub` | 10 GB | 3 app sessions | sessions lapse when the user stops being active |
| `sciserver` | 10 GB | 3 containers | persistent volume only; temporary volumes are deleted after a grace period |
| `cyverse` | 5 GB | 1 job | 200 core-hours a year, and data above quota is deleted |
| `quantum-inspire` | not published | 3 hardware jobs | each hardware job waits behind calibration and other users |

The addition is 250 + 250 + 100 + 10 + 10 + 5 = 625 GB on the vendors' own decimal
figures, which is 582 GiB. A granted EGI trial adds 100 GB of block storage and would
make 725 GB. None of it is one namespace: six accounts on six operators' hardware, with
no shared login and no shared file system.

⭐ The concurrency adds up better than the storage. Galaxy Main gives 6 jobs, nanoHUB 3
sessions, SciServer 3 containers, CyVerse 1 job and Quantum Inspire 3 queued jobs. That
is 16 slots across five services, for one email address and no card. A batch of small
jobs can run on all of them at once, and the queues sit on different hardware.

⚠ A gateway account is not a machine. Galaxy gives no root, no arbitrary binary unless
it is packaged as a tool, and no inbound network. nanoHUB runs published tool engines
through a web page, in the nanotechnology domain, with MATLAB among the general tools.
SciServer's default images ship Python 3.7 and PyTorch 1.4.

The one reachable virtual machine is the smallest. `egi-cloud-compute` offers 4 vCPU,
8 GB of RAM and 100 GB of block storage as "Trial access", through a contact form. Its
value is shape rather than size: it is always on, so it holds state and submits to a
batch system.

## The residency wall

Eleven records fail identity. Nine close on an institution or an employer, one closes
on residency, and one closes because the programme that admitted outsiders was
withdrawn. The closing sentence is quoted where the record carries it.

- `cloudlab`: "You should only start a new project if you are a faculty member, senior
  research staff, or in some other senior position", and joining an existing project
  needs that leader's approval.
- `cscs-small`: "Small projects are intended for applicants from the Swiss user
  community", and every proposer "must hold at least a postdoctoral position at an
  academic institution". The 8,000 node-hours are decided before any technical review.
- `surf`: eligibility is a tenured or tenure-track appointment at a Dutch university,
  university of applied sciences, university medical centre, KNAW or NWO institute.
- `it4innovations-open-access`: "Eligible applicant: Employee of a Czech research
  organisation". The gate names employment, not nationality, which is the weakest form
  of this wall found here.
- `nsf-ncar-derecho`: "To use Derecho, you must be a U.S.-based researcher, and your
  research must be in the Earth system sciences or related to Earth system science".
  Country and field both bind, before any funding question arises.
- `ospool`: access is "for any researcher affiliated with a US academic institution",
  and joining somebody else's project needs that project's PI to add the user.
- `jetstream2`: every instance needs an active ACCESS allocation. The ACCESS policy
  quoted in [`hpc-allocations.md`](hpc-allocations.md) excludes unaffiliated people and
  refuses public email domains, so 6,250 A100-hours are closed to a gmail.com address.
- `designsafe-ci`: the PI is "typically a faculty member or research scientist at a
  US-based academic institution". Unfunded exploratory research is allowed, which
  changes the science question only.
- `grid-5000`: "The Grid'5000 Open-Access program is closed". The instrument runs and
  accounts are still issued; the door for an academic outside France is gone.

⛔ The wall is not about money and not about the quality of a proposal.
`nersc-exploratory` accepts requests at any time, decides in four weeks, and asks for
250 node hours rather than a campaign. What it needs is an organisation willing to sign
a contract with a US national laboratory.

## The conversion arithmetic

Where a record gives credits or node-hours rather than hours on a named card, the
division is shown. A record that states its own unit and no rate is not converted.

**ACCESS Explore, the worked example.** Jetstream2 prices every instance in ACCESS
service units at 1 SU per vCPU per hour on CPU flavours and 2 SU per vCPU per hour on
GPU and large-memory flavours. A full A100 flavour, g3.xl at 32 vCPU, 120 GB of RAM and
40 GB of GPU RAM, costs 64 SU an hour. The smallest ACCESS tier carries 400,000 credits
(`docs.jetstream-cloud.org/general/vmsizes/`, read 2026-10-22).

- 400,000 / 64 = 6,250 hours of a full A100 card.
- 400,000 / 32 = 12,500 hours of a half card, g3.large at 16 vCPU and 20 GB of GPU RAM.
- 400,000 / 16 = 25,000 hours of a quarter card, g3.medium at 8 vCPU and 10 GB.
- 400,000 / 1 = 400,000 vCPU-hours on CPU flavours.

⚠ Two facts change the effective hours. A stopped instance is still charged 75 per
cent and a shelved instance is charged nothing. The record in `dossier/compute/access.json`
states the 400,000 credit limit and never converts it, so this division is the only way
a reader learns whether Explore buys an afternoon or a year.

**IT4Innovations, the largest GPU quantity on the page.** One request may ask for
10,300 Karolina GPU node-hours, and a Karolina node holds eight A100 cards of 40 GB.
That is 10,300 x 8 = 82,400 A100-hours, which is 13.18 times the 6,250 an ACCESS
Explore award buys. Both figures are published; the multiplication is this document's.

**NERSC, node-hours to core-hours.** A Perlmutter CPU node is 2 AMD EPYC 7763
processors totalling 128 cores and 512 GB of memory. The Exploratory award of 250 node
hours is therefore 250 x 128 = 32,000 core-hours. The conversion holds for the CPU
partition only.

**DesignSafe and CyVerse, where the unit is money.** DesignSafe sells time to users
outside the NSF eligibility categories at approximately USD 0.50 per node-hour, and a
TACC node is 48 to 64 cores, so the rate is USD 0.008 to USD 0.01 per core-hour.
CyVerse Pro is USD 400 a year for 25,000 core-hours, which is USD 0.016 per core-hour
computed from the two published figures.

**What cannot be converted.** SURF states its Snellius allocation in SBU and does not
state the ratio to core-hours, so 1,000,000 SBU stays an unconverted billing unit.
CSCS counts 8,000 node-hours on Alps, where a node is a GH200 node, so the figure is
GH200 node-hours and not core-hours. NCAR's 500,000 core-hours are on EPYC cores of an
unstated count per node, and dividing by the fleet average would invent a figure.

## What the class does not give

- **No GPU-hours that an email address reaches.** The seven self-service records give
  zero. Every GPU figure in the slice needs an appointment, an employer or a residency,
  and the ACCESS route additionally refuses a public email domain.
- **No shell on a useful machine.** Galaxy, nanoHUB and SciServer expose tools and
  notebooks over a web page. The one reachable VM is 4 vCPU and 8 GB on a trial.
- **No wall-clock guarantee.** Galaxy jobs hit a 36 to 48 hour walltime. The gateways
  publish concurrency and rarely publish hours.
- **No comparable unit.** Node-hours, core-hours, GPU-hours, service units, SBU, QPU
  seconds and compute units all appear, and no record converts between them.
  ⛔ Adding a node-hour to a core-hour produces a number that appears nowhere.
- **No egress terms, no labour and no priority.** No record in the slice found an
  egress allowance on the page it read. OSPool states that jobs may be interrupted at
  any time, because the capacity is opportunistic.

## What could not be read

- Compute quotas on `galaxy-europe` and `galaxy-australia` are unpublished, so only
  storage is quantified for those two.
- ⚠ `galaxy-australia` gives three retention figures on its own pages: "service
  lifetime", one year, and 90 days from last activity. The shortest is used here.
- ⚠ `cscs-small` contradicts itself on the clock: a one-year duration in its offer, and
  three-month windows that expire unused in its chaining note. The two shapes admit
  different workloads, so the record does not settle which holds.
- The 10 GB at `sciserver` comes from a 2021 how-to, because the live policy page sits
  behind a login, and `fabric` names no approver for an ORCID signup.
- Per-app limits at `nanohub`, shots per job at `quantum-inspire`, per-container CPU and
  memory at `sciserver`, and the `egi-cloud-compute` trial duration are unpublished.
- CloudLab disk and RAM per node are absent from the page read, and the four d750 GPU
  nodes exist but are withheld.

## What would change the answer

1. **The OSPool guest notebook.** No account, Google or Microsoft sign-in, real
   HTCondor jobs: one measured run would test the 844K core-hour pool.
2. **A FABRIC signup with ORCID.** The portal defaults to ORCID and the teaching
   material says approval may follow. The attempt settles which is true.
3. **The EGI contact form.** No eligibility criteria are published, so a reply is the
   only evidence available for the one always-on machine in the slice.
4. **A compute quota for Galaxy Europe or Australia.** An hours figure would turn 16
   concurrent slots into measurable batch capacity.

A fifth change would not help. A guide calling a programme open to outside researchers
is not evidence: `grid-5000` is still recommended that way, and its own page says the
open-access programme is closed.

## Two more records, and the six-hour door

Neither is one of the nineteen above, and both also hold a record under `storage`.
`chameleon-cloud` gives a project "20,000 SUs for six months", renewable, with a decision
"within one business day", and PI status "is limited to faculty and research staff at
US-based academic institutions". The route that survives is Daypass: reproduce an
artefact published on Trovi, for a default 6 hours, reviewed by that artefact's PI.

`digital-research-alliance` is Canada's national platform, at about 233,000 CPU cores,
2,610 GPUs and 150 PB, reserving "a target of 20%" for a Rapid Access Service that an
Alliance account reaches at once. The other 80 per cent is a competition whose PIs must
"be a faculty member at a Canadian academic institution".

⚠ Both return `fails-identity` while the identity field says email and the `limits`
array is empty, so the refusal lives in the evidence rows rather than in the fields a
table reads.
