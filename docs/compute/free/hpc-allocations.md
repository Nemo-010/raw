# National HPC allocations: the largest capacity here, behind one door

This document answers one question: can a person without an institutional affiliation obtain
time on a national or supranational supercomputer, and what does each door cost in identity.
The class is the largest capacity in the corpus by orders of magnitude. ALCC's 2026-2027 pool
adds to 40,500,000 node-hours and INCITE awards 500,000 to 2,000,000 node-hours to one project,
and individual awards may be higher.
A reader can obtain none of it: sixteen of the seventeen records here return `fails-identity`
and the seventeenth is dead. The sixteen fail on the same field, an institution that can sign an
agreement or an employer that can be named on a form. Money, nationality and the science case
are not what bind.

## The short answer

Every programme in the slice, ordered by the identity that opens the door, from the loosest
test found to a programme with no door left. Read the fourth column first.

| Programme | Machine and scale | Award size | Who may apply | Verdict |
| --- | --- | --- | --- | --- |
| `incite` | Frontier and Aurora, up to 60 per cent of allocatable time | 500,000 to 2,000,000 node-hours per project, and individual awards may be higher, calendar 2027 | The call text admits non-US individuals; the award needs every institution to sign a user agreement | fails-identity |
| `fugaku-trial-access` | Fugaku, node-hours, 48 compute cores plus 4 assistant cores per node | up to 100,000 node-hours, or 1,000 fixed on the first-touch form | A person in a legal entity anywhere, with that organisation's head approving | fails-identity |
| `res` | MareNostrum 5 and the Spanish centres, site-hours | typically 50,000 to 2,000,000 hours, no stated minimum | Any scientist in the EU or an associated state, PI at an institution there | fails-identity |
| `access` | The ACCESS resource pool, credits rather than hours | 400,000 Explore credits, 1,500,000 Discover, 3,000,000 Accelerate, 12 months | US-affiliated people at an eligible organisation with a non-generic email domain | fails-identity |
| `lccf-horizon-leadership` | Horizon, 4,750 Vera CPU nodes and 2,000 Grace-Blackwell nodes | 125,000 to 500,000 SUs on Horizon, up to 50,000 on Vista, six months | US researchers in open research, typically faculty, with peer-reviewed funding | fails-identity |
| `archer2-pump-priming` | ARCHER2, four GPU nodes of eight MI210 each | 4,000 CU for six months, or 800 CU on the Driving Test | Researchers within the EPSRC remit at a UK research organisation | fails-identity |
| `cineca-iscra` | Leonardo Booster, A100 64 GB | 10,000 GPU-hours on Class C, 250,000 GPU-hours or 3,600,000 core-hours on Class B | Researchers affiliated to an Italian research organisation | fails-identity |
| `lumi` | LUMI-G, MI250X | not published centrally; set per national allocator | A person invited by a national Resource Allocator in a consortium country | fails-identity |
| `naiss-pdc` | Dardel, MI250X partition | no size published for the small test allocation | Academic researchers at postdoctoral level or above | fails-identity |
| `hlrs-test-access` | Hunter, MI300A, and Hawk, A100 | 100 Hunter node-hours for six months, not peer-reviewed | Investigators at German research institutions | fails-identity |
| `jsc-test` | JURECA, JUWELS and the JUPITER Booster, GH200 | no core-hour figure published; up to four months | Applicants employed at a German university or research facility | fails-identity |
| `alcf-director-s-discretionary` | Aurora, Polaris, and the AI Testbed: Groq, Graphcore, SambaNova, Cerebras | no range published; the page says the award is small | Researchers from industry, academia or government, year-round | fails-identity |
| `olcf-director-s-discretionary` | Frontier, 64-core EPYC and eight MI250X GCDs per node | 15,000 to 20,000 node-hours, up to 12 months | A PI who signs an agreement, and whose institution signs with UT-Battelle | fails-identity |
| `alcc` | Frontier, Aurora, Polaris, Perlmutter | the pool is 40,500,000 node-hours; the per-award maximum is not published | Universities, industry and government, DOE sponsorship not required | fails-identity |
| `eurohpc-ju-benchmark` | LUMI, JUPITER, Leonardo and the other JU systems | a limited number of node hours, maximum three months | Researchers established in an EU Member State or Horizon-associated country | fails-identity |
| `eurohpc-ai-factories` | LUMI, JUPITER, Leonardo, MareNostrum 5 | up to 5,000 GPU-hours on Playground, 50,000 on Fast Lane, more on Large Scale | An organisation with a VAT number and a PIC, and a PI it employs | fails-identity |
| `prace` | withdrawn | none | nobody: the allocation function moved to EuroHPC at the end of 2022 | dead |

## The capacity, added up

ALCC publishes its 2026-2027 pool as five figures in one sentence: 20,000,000 node-hours on
Frontier, 16,000,000 on Aurora, 1,000,000 on Polaris, and 2,250,000 CPU-node-hours plus
1,250,000 GPU-accelerated node-hours on Perlmutter. Those add to 40,500,000 node-hours for one
cycle across four systems, which is arithmetic on the record's figures and not a quoted total.
INCITE allocates up to 60 per cent of allocatable time on the same two largest machines for
2027, at 500,000 to 2,000,000 node-hours per project, and the record says individual awards may
be higher.

The unit is the trap in every number here. A node-hour is one node for one hour, and a node is
not a GPU. Frontier's node carries eight MI250X GCDs and 64 EPYC cores, so a 15,000 node-hour
OLCF award is 120,000 GCD-hours and 960,000 core-hours, and 20,000 node-hours is 160,000
GCD-hours and 1,280,000 core-hours. That is multiplication on two published figures, so the
converted figures are inferred here rather than quoted. Nothing in the corpus compares those
hours to a cloud GPU-hour, because no measured equivalence exists.

⚠ Two records are wrong on their own data. The `alcc` `notes` field says 37 million node-hours
across Frontier and Aurora, while its own figures give 36,000,000 for that pair and 40,500,000
for the pool. And the `alcc` shape field and `incite` notes both name MI300A as Frontier's
card, while `olcf-director-s-discretionary` quotes OLCF documentation for four MI250X packages
with two GCDs each. One machine cannot carry both cards, and the quoted primary source is OLCF.

## The United States: every rung wants a signature

The US lane is one ladder with a trial tier beside it: Director's Discretionary at the bottom,
ALCC in the middle, INCITE at the top. The rungs are not alternatives, and each produces the
evidence the next one asks for. A fourth door, `lccf-horizon-leadership`, allocates 125,000 to
500,000 SUs on Horizon for six months to US researchers with current peer-reviewed funding,
and admits non-US researchers only through a US partner. SU is a site-defined unit, not a
node-hour.

### INCITE, ALCC and ACCESS

INCITE is the most open on paper. The 2027 call states that individuals and teams from
academia, national laboratories, industry and federal agencies are eligible, and does not
restrict the PI to the United States (`doeleadershipcomputing.org/call-for-proposals/`, read
2026-10-22: US and non-US based individuals and teams are eligible to apply). The window ran
from 8 April 2026 to 15 June 2026, with awards in November 2026.

The same page closes the door. Every participating institution must accept or already have
signed the user agreement, or access is delayed, and the FAQ requires the applicant to hold all
funding needed to run the campaign at application time. A second filter is quantitative: the
record's notes say a request below 20 per cent of the average award is redirected to Director's
Discretionary or ALCC, which at 500,000 node-hours means a campaign on a fifth of an exascale
machine.

ALCC allocates 10 to 30 per cent of allocatable time on Frontier, Aurora, Polaris and
Perlmutter and states that DOE sponsorship is not required. Proposals for 2026-2027 were due 26
January 2026 with decisions in late May, and awards run one year and extend to three by
renewal. Every participating institution must sign the ASCR facility user agreement, and a
request above the maximum is ruled nonresponsive rather than escalated. No per-award maximum is
published: the page states award size as small to medium and never gives a ceiling.

ACCESS is the one US programme with a published credit scale and a turnaround: 400,000 credits
on Explore, 1,500,000 on Discover, 3,000,000 on Accelerate, reviewed in one to two business
days, valid 12 months, no deadline (`docs.jetstream-cloud.org/alloc/overview/`, read
2026-10-22: the three thresholds, reported by a resource provider rather than by ACCESS). Its
policy page is the cleanest refusal in the corpus. PIs and users must be affiliated with an
eligible organisation, and unaffiliated individuals are no longer eligible to request or be
added to an allocation. A person based outside the United States is not eligible to lead a
project regardless of affiliation, including at an international campus of a US institution.
The site will not let a non-US-based person or a generic email address initiate a request, and
public domains such as gmail.com are prohibited (`allocations.access-ci.org/allocations-policy`,
read 2026-10-22). The record attributes the change to NSF Important Notice No. 149 of 10 July
2025, so any guide older than that describes a door since closed.

### ALCF and OLCF Director's Discretionary

ALCF DD is the structural exception, and the record calls it the most valuable finding in the
DOE stack. The award waives the institutional user agreement that INCITE, ALCC and OLCF DD all
require (`docs.alcf.anl.gov/account-project-management/project-management/starting-alcf-award/`,
read 2026-10-22: the institutional agreement does not apply to Director's Discretionary
awards). It is year-round, usually three to six months, and it is the documented route to the
AI Testbed accelerators: Groq, Graphcore, SambaNova and Cerebras, one form for all four.

What remains is not a contract but a form. The account request asks for the name of the
employer, and a foreign national supplies a passport number, USCIS documents and a CV under an
ANL-593 request (`alcf.anl.gov/support-center/get-started/request-account`, read 2026-10-22). A
person with no employer has nothing for a required field and no sponsor for the authorisation.
The waiver removes one signature and leaves the employer field.

OLCF DD allocates about 10 per cent of the available Frontier hours in a calendar year,
typically 15,000 to 20,000 node-hours per project, applied for at any time and lasting up to 12
months. The PI signs a PI Agreement, passes an ORNL export-control review and a Personnel
Access System check, and a User Agreement is executed between UT-Battelle and the PI's
institution (`docs.olcf.ornl.gov/accounts/accounts_and_projects.html`, read 2026-10-22). A
foreign national participant also triggers a PAS request that the record puts at 15 to 35 days.

## Europe: affiliation, not nationality

The European lane fails differently. Nationality is usually irrelevant and one programme says
so; what binds is a registered organisation in the right country, often with an employment
contract. PRACE is the predecessor and not a door: `prace` returns `dead` because at the end of
2022 the EuroHPC JU took over its peer-review and support process
(`eurohpc-ju.europa.eu/supercomputers/supercomputers-access-policy-and-faq_en`, read
2026-10-22), and every PRACE cut-off after 2023-07-07 is filed under closed calls.

### EuroHPC Benchmark and AI Factories

The benchmark tier is the cheapest door in the EuroHPC stack and the thinnest award. It is
continuously open with monthly cut-offs through 2033, first-come-first-served against a monthly
quota, gives a limited number of node hours for scalability or AI application tests, runs three
months at most, and delivers access in two to three weeks
(`eurohpc-ju.europa.eu/eurohpc-ju-call-proposals-benchmark-access_en`, read 2026-10-22). ⚠ The
node-hour maximum is not published per system, because it depends on the systems in each
cut-off, so the record leaves the field null rather than borrowing a neighbouring tier's
figure.

The AI Factories are the largest GPU-hour number here that does not depend on peer-reviewed
science: up to 50,000 GPU hours for three months, approved within four working days,
first-in-first-out (`eurohpc-ju.europa.eu/ai-factories/ai-factories-access-modes/fast-lane-access-ai-factories_en`,
read 2026-10-22). Playground gives up to 5,000 GPU hours with no competitive selection and
access in two working days, Fast Lane runs 5,001 to 50,000, and Large Scale is above 50,000
with 3, 6 or 12 month allocations over about two cut-offs a month.

The identity test is a company, stated three ways: a valid VAT number and, if applicable, a
Participant Identification Code; a PI holding an employment contract there at submission and
for three months after the allocation; and an Industrial Innovation call restricted to the
industrial sector. The LUMI AI Factory page puts it plainly, stating that individual persons or
temporary teams are not entitled to its services
(`lumi-ai-factory.eu/pricing-and-eligibility/`, read 2026-10-22).

⭐ That is the clearest refusal in the slice. A natural person is named and excluded, so the
answer comes from the provider rather than from a form.

### LUMI and RES

LUMI has no allocation call of its own. A person must be a member of a project that has already
been granted resources, a national Resource Allocator creates the project and invites the PI
and members, and the terms of use require an institutional email address
(`docs.lumi-supercomputer.eu/firststeps/accessLUMI/`, read 2026-10-22). The record counts a
dozen national allocators plus the EuroHPC JU, and each country runs its own policy, so LUMI is
not one door. The only route without a consortium affiliation is the EuroHPC call, gated on an
EU-affiliated organisation instead. The Finnish national route states a floor of 1,000,000 core
hours for a developer project, the clearest published size for a LUMI national allocation.

RES is the most nationality-open programme in the slice and it is still closed. The FAQ states
that resources are open to all scientists in open research in the European Union and associated
states, that the PI may come from an institution in any of those countries, and that a Spanish
team member is strongly recommended rather than required (`res.es/en/faq`, read 2026-10-22).
Typical requests run 50,000 to 2,000,000 hours, a request above 10,000,000 hours needs a
justification, and fast access is evaluated weekly. The recorded HPC/AI/Quantum deadline was 15
September 2026. RES fails on affiliation, not on nationality, and the record says so. Hours
here are site-hours, with no conversion to core-hours.

### CINECA ISCRA

ISCRA has the lowest-friction entry here that is still inside a national
programme. A try project is requested by email to the CINECA service desk, is about 10 per cent
of a Class C project, is activated within 10 days and averages two months
(`hpc.cineca.it/hpc-access/access-cineca-resources/iscra-projects/iscra-project-size/`, read
2026-10-22). Class C awards up to 10,000 GPU hours on Leonardo Booster for up to nine months
under continuous submission, with monthly evaluation and allocation within 45 days. Class B
reaches 250,000 GPU hours or 3,600,000 core hours over 12 months.

The gate is Italian and sits on a different page. The general information page states that the
programme is open to researchers affiliated to an Italian research organisation and that PIs
are expected to be affiliated to an Italian institution
(`hpc.cineca.it/hpc-access/access-cineca-resources/iscra-projects/iscra-general-informations/`,
read 2026-10-22). The email-only tier is real, and it composes into nothing without the
affiliation the next tier demands.

### The national test tiers: ARCHER2, HLRS, JSC, NAISS

Each is a small, always-open award that exists to prepare a larger proposal, and each is gated
on national employment rather than on nationality.

| Programme | Award | Open | What fails |
| --- | --- | --- | --- |
| `archer2-pump-priming` | 4,000 CU for six months, or 800 CU on the Driving Test | always, decided in under two weeks | the EPSRC remit resolves to a UK research organisation |
| `hlrs-test-access` | 100 Hunter node-hours for six months, not peer-reviewed | offered to GCS applicants | the page is headed "for investigators at German research institutions" |
| `jsc-test` | no core-hour figure published, up to four months, plus about two person-weeks of staff support | all year | applicants must be employed at a German university or research facility |
| `naiss-pdc` | no size published for the small test allocation | any time, handled in one to two weeks | postdoctoral level or above, and a Swedish group or supervisor |

JSC's two person-weeks of Simulation and Data Lab support is worth more than the node hours to a
solo researcher, because staff time is the input a reader cannot buy. ARCHER2's CU is a
CPU-hour equivalent, not a GPU-hour unit, so its 4,000 CU ceiling cannot be compared with the
GPU-hour figures here. HLRS is the only centre in the slice that states outright that its test
application is not peer-reviewed.

⭐ `naiss-pdc` is the only record in the slice where the provider's own documentation states
that a person based outside the country can hold an allocation. The condition is a Swedish
research group with a supervisor in Swedish academia, so the door is a collaboration rather
than an application.

## Japan: one legal entity, anywhere

Fugaku Trial Access is the strongest single number in this slice and the simplest refusal.
It awards up to 100,000 node-hours per project, free of charge, with the call open all year, a
project period up to half a year, and a screening result within one to two weeks. The
first-touch option fixes 1,000 node-hours for a simplified application
(`hpci-office.jp/en/using_hpci/proposal_submission_current/fugaku_trial`, read 2026-10-22).
Both tiers are screened for eligibility rather than reviewed by experts. 100,000 node-hours at
48 compute cores per node is 4,800,000 core-hours, counting the 48 compute cores and excluding
the 4 assistant cores, and that conversion is inferred here rather than quoted.

The eligibility rule is organisational rather than national. The project representative must
belong to a legal entity, inside or outside Japan, and must obtain approval from the head of
that organisation. The HPCI FAQ adds that use by non-residents and by non-Japanese nationals is
possible, that a non-resident may be the project representative, and that projects with
non-resident participants need separate R-CCS approval. Japan is the one lane where geography is
explicitly not the test.

## The individual route, tested door by door

Five doors were candidates for a person with no institution. Each was tested against the
record's own sentences.

| Candidate door | What the record says | Why it is not a route |
| --- | --- | --- |
| INCITE, applicant sentence | US and non-US individuals and teams are eligible to apply | every participating institution must sign the user agreement, and the applicant must already hold the funding |
| Fugaku first-touch form | a person in a legal entity anywhere, online form, 1,000 node-hours | a legal entity is still required, plus that organisation's head approving |
| CINECA try project | requested by email, about 1,000 Leonardo GPU-hours, activated in 10 days | the programme is open to researchers affiliated to an Italian organisation |
| EuroHPC Playground | no competitive selection, access in two working days, up to 5,000 GPU hours | the AI Factory calls are industrial only, and individual persons are not entitled |
| RES fast access | weekly evaluation, PI from any EU or associated-state institution | the PI must be at an institution in one of those countries |

The result is zero. No record in this slice describes a route that a person with no affiliation
and no company can complete.

⭐ The nearest miss is worth naming, because the missing item is one form field rather than a
contract. ALCF Director's Discretionary waives the institutional user agreement, is open
year-round, and reaches four accelerator classes that no cloud free tier offers. It still asks
for an employer name and, for a non-US citizen, an ANL-593 authorisation with passport and CV.
Any named collaborating organisation, in any country, closes that gap.

## What the class does not give

- **It gives an individual nothing.** Sixteen records fail on identity and the seventeenth is
  dead. No trial tier in the slice admits a natural person alone.
- **It gives no comparable unit.** Node-hours, core-hours, GPU-hours, service units, CPU-hour
  equivalents and site-hours all appear, and no record converts between them. A reader who adds
  two of these numbers has invented a third.
- **It gives no route that composes.** Every trial tier produces evidence for a larger
  proposal: OLCF DD for INCITE, HLRS test access for a GCS proposal, the EuroHPC benchmark for
  Regular or Extreme Scale, JSC test projects for a regular project, the CINECA try project for
  Class C. Every rung above the first is closed, so the ladder composes into a refusal.
- **It gives access slowly.** Two working days at EuroHPC Playground is the fastest documented
  turnaround, and Fast Lane takes four. Two to three weeks is common, and a foreign national at
  OLCF adds 15 to 35 days for a PAS check.
- **It gives no money, no labour and no egress terms.** INCITE's award is time plus storage
  across the programme and excludes labour, travel and postdoc funding. No record in the slice
  found an egress term on the page it read, so this document asserts nothing about moving data
  off a national system. That is a gap, not a zero.

An affiliation, if a reader ever obtains one, converts this whole class from dead to usable,
and nothing else in the corpus does that. The free sandbox and GPU-notebook layer beside this
file needs no institution and gives hours rather than node months. The two do not substitute
for each other, and the identity cost is what separates them.

## What would change the answer

Four specific things, each a page rather than a policy shift.

1. **An ACCESS policy page that restores unaffiliated eligibility.** The current text bans
   unaffiliated, self-employed and retired people by name
   (`allocations.access-ci.org/allocations-policy`, read 2026-10-22). A reversal would move one
   row from `fails-identity` to a route to 400,000 credits with a two-day review.
2. **A EuroHPC AI Factory call open to natural persons.** The VAT number and PIC are the
   concrete blockers. One such call would open up to 5,000 GPU hours with no competitive
   selection.
3. **A CINECA try project granted without Italian affiliation.** The request is an email, so
   this is testable by measurement rather than by reading: send it and record the reply.
4. **A Fugaku first-touch screening that accepts an individual.** The tier is 1,000 node-hours
   on an online form with eligibility screening, and the rule is a legal entity. A published
   exception would open 1,000 node-hours and a route to 100,000.

A fifth change would not help. A guide saying a programme is "open to all researchers" is not
evidence, and three records here were settled by reading the policy page behind that sentence.
