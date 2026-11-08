# Startup credit programmes: the company is the gate

Thirteen credit programmes sit in this slice of the compute dossier. The question is not which
one is largest. It is which one a single person with no company can reach, and what the
reachable amount is worth. The answer is USD 2,300 from four programmes, and each of the four is
one review, one card or one account away rather than one signature away. The programmes
advertising the largest numbers, up to USD 200,000, are closed to a reader by a term that work
does not remove: incorporation, a venture round, or an Organizational ID that only an investor can
issue.

Every record here is `documented`: a vendor page read on 2026-10-22. None is `measured`, no
application was submitted and no award was received, so each figure is a vendor claim about what
a programme offers.

## The short answer

Sorted by what a person with no legal entity can reach, then by amount. `Gate` names the term
that fails first, not the whole eligibility list. `What it buys` uses a recorded hourly rate
where one exists, and says so where none does.

| Programme | Credit | Expiry | Gate | What it buys | Verdict |
| --- | --- | --- | --- | --- | --- |
| CloudRift AI Grant | USD 100 to USD 1,000 | not published | human review of a project; indie developers and content creators named as eligible | GPU time on RTX 4090, RTX 5090 or RTX PRO 6000; no hourly rate recorded, so hours are not derivable | qualifies-with-caveat |
| AWS Activate, Founders | USD 1,000 plus USD 350 Developer Support | 2 years | business email on the startup domain, a live company website, AWS Builder ID, linked AWS account; no incorporation term | USD 1,000 of EC2 and S3 at list price; no GPU rate paired in the record | qualifies-with-caveat |
| Microsoft for Startups, milestone 1 | USD 200 | 60-day milestone clock; credit expiry not published | personal LinkedIn account; the page forbids business accounts at this step | an estimated few days of a small Azure VM; too small to train on | qualifies-with-caveat |
| DigitalOcean Startups | not published | 12 months | company website, email on that domain, registered team account on a business email; an explicit no-partner route | CPU droplets, Spaces and managed databases; every GPU product excluded | qualifies-with-caveat |
| Zylora startup GPU | USD 25 Explorer, USD 100 Builder, USD 500 Startup, USD 2,500 Accelerator | 6 months | Explorer: card on file, no review. Builder: live site or public repository. Startup and Accelerator: funding or an accelerator batch | no GPU class is named per tier, so hours are not derivable | trial-only |
| Oracle Startup Growth | USD 5,000 to USD 60,000 | 12 months | 'legally registered technology companies', with due diligence on corporate identity and ownership | OCI at list price, including Ampere and GPU shapes; no rate paired in the record | fails-identity |
| Lambda Cloud credits | USD 1,000 | 12 months | current NVIDIA Inception membership, which requires incorporation, plus a card in a listed country | 250 H100-hours, 358 A100 80 GB-hours or 149 B200-hours at Lambda's own rates | fails-identity |
| NVIDIA Inception | not published | not published | 'officially incorporated', non-generic domain email, two named contacts; solo founders may apply but incorporation is not waived | partner cloud credits and preferred pricing; the amount is never published | fails-identity |
| Google for Startups | USD 2,000 Start; USD 200,000 to USD 350,000 funded tiers | not published | domain-matched business email, billing admin on that domain, live site describing company, team and product; funded tiers need a verifiable venture round | GCP list price; no rate paired in the record | fails-identity |
| AWS Activate, Portfolio | up to USD 200,000 | not published | Organizational ID issued by an Activate Provider, plus a round in the last 12 months | AWS list price including Bedrock third-party models | fails-identity |
| Databricks | up to USD 200,000 | not published | institutional round between pre-seed and Series A; no eligibility table is published | Databricks compute and Neon Postgres from one approval | fails-identity |
| MongoDB | not published | not published | 'Less than 7 years old and Series A or earlier', one software product, active website and LinkedIn profile; agencies refused | Atlas credits and Voyage AI tokens; the amount is undisclosed | fails-identity |
| DigitalOcean Hatch | none | retired | replaced by the Startups programme, so no quota or identity question applies | nothing | dead |

## The USD 2,300 a person without a company can reach

Four programmes publish an amount and an eligibility list a sole founder can meet:

- AWS Activate Founders: USD 1,000
- CloudRift AI Grant, top of its range: USD 1,000
- Microsoft for Startups, milestone 1: USD 200
- Zylora Builder: USD 100
- total: USD 1,000 + USD 1,000 + USD 200 + USD 100 = USD 2,300

The AWS Developer Support credits of USD 350 are excluded because they buy support, not compute.
The lower bound is USD 1,325, when CloudRift awards its floor and the applicant qualifies only
for Zylora Explorer: USD 1,000 + USD 100 + USD 200 + USD 25 = USD 1,325.

DigitalOcean Startups is the fifth programme that needs no venture firm, and it enters neither
bound: the amount is set by a partner or a program manager and appears only in the onboarding
email, so the record carries no total and the page states only a monthly ceiling of USD 10,000.

### AWS Activate Founders: the largest sum behind the weakest gate

USD 1,000 in AWS credits plus USD 350 in Developer Support credits, valid for two years
(`aws.amazon.com/aws-startups/learn/applying-for-aws-activate-credits-a-step-by-step-guide/`,
read 2026-10-22). The eligibility list is: new to Activate credits, self-funded, a fully
functioning company website, founded in the past 10 years, and a business email matching the
startup domain. No incorporation requirement appears in that list or in the seven-step guide.

The page states the routing rule: 'If you do not have an Org ID, you are initially eligible for
the Founders Package.' The Japanese getting-started page
(`aws.amazon.com/jp/activate/gettingstarted/`, read 2026-10-22) lists the required fields as an
AWS account ID, a company website or web profile and the applicant's LinkedIn profile, and
states that crowdfunding and friends-and-family funded startups remain eligible.

⚠ The review is what fails, not the quota. An AWS re:Post answer states that meeting the
published criteria does not guarantee approval and that AWS holds internal requirements beyond
the public list
(`repost.aws/questions/QUq-hqNzjaTq-9-IBFvxdhlg/repeated-rejections-for-aws-activate-founders-credits-need-guidance`,
read 2026-10-22). Submitted applications are not edited, so a weak website is final. The residual risk is that review, which is what `qualifies-with-caveat` carries.

### CloudRift AI Grant: the only GPU grant that names individuals

USD 100 to USD 1,000 in GPU credits for training models, building tools or making tutorials, on
RTX 4090, RTX 5090 and RTX PRO 6000 cards (`cloudrift.ai/ai-grant`, read 2026-10-22).
Eligibility is written as project categories rather than legal forms: 'Emmy compiler builders,
researchers, open-source maintainers, indie developers, content creators, and artists and
designers', which names individuals and not companies. No company, funding or institution term
appears on the page, and applications are reviewed every two weeks: 'We review applications every
two weeks'.

⚠ The constraint is the amount. USD 1,000 is hours of a consumer GPU, not a training run, and a
vendor this small is the shape that closes without notice. One aggregator lists a deadline of
2026-12-31 that the vendor page does not state.

### Microsoft for Startups: USD 200 against a personal LinkedIn account

Milestone 1 pays up to USD 200 immediately, on an Azure signup and identity verification with a
personal LinkedIn account
(`learn.microsoft.com/en-us/startups/microsoft-for-startups/getting-started-mfs`, read
2026-10-22). The page states it: 'Verify your identity (use a personal LinkedIn account, no
business accounts allowed at this step)' - the lowest identity bar here and the smallest amount.

Milestone 2 pays USD 5,000 and requires business verification, defined on the same page as
'Confirm your startup is a registered legal entity'. The ladder runs to USD 150,000, each step
gated on a workload count, a spend condition and a 60-day clock. USD 200 buys an estimated few
days of a small VM, not a training run.

### Zylora: USD 25 for a card on file

Explorer pays USD 25 in one-time credits, instant approval, open to 'any individual developer'
with a card on file (`zylora.dev/startups/`, read 2026-10-22). Builder pays USD 100 for an
active project with a live website or a public repository and about a five-minute review;
Startup and Accelerator pay USD 500 and USD 2,500 to funded startups and partner batch members.
Credits expire six months after the grant, unused credits are forfeited, and the limit is one
grant per person and per company.

No GPU class is named for any tier, so the page supports no hours figure. The record estimates
USD 100 at consumer prices as a few hours of one card, and that is an estimate rather than a
published rate.

## The gate, named exactly

**Incorporation.** Oracle's terms say the programme is 'intended for legally registered
technology companies that develop digital products or platforms with the potential for scalable
use of OCI', and that Oracle runs due diligence including verification of corporate identity and
ownership (`oracle.com/uk/artificial-intelligence/startup-growth-engine/terms/`, read
2026-10-22). NVIDIA's application states the company must be 'officially incorporated' and less
than 10 years old, with a working website, a non-generic domain email and two named contacts
(`programs.nvidia.com/phoenix/application`, read 2026-10-22). Lambda's USD 1,000 is not a
programme of its own: it requires current Inception membership and inherits that term
(`lambda.ai/nvidia-inception`, read 2026-10-22).

NVIDIA's page carries the sharpest sentence in the class: 'Solo founders with no other employees
may also apply'. The carve-out admits a one-person company and still requires the company.

**A venture firm's referral.** AWS Portfolio requires the applicant to be 'associated with an
Activate Provider and have their Organizational ID', and the provider list names Andreessen
Horowitz, Brex, Carta, Greylock, Sequoia and Y Combinator (`aws.amazon.com/startups/credits/`,
read 2026-10-22). The investor issues the ID, so the applicant cannot produce it alone.
Databricks describes its programme as 'purpose-built for early-stage, venture-backed startups
... who have recently raised institutional funding (pre-seed through Series A)'
(`databricks.com/blog/announcing-new-databricks-startup-program`, read 2026-10-22). Google's
funded tiers need verifiable pre-seed to Series A funding, and non-venture money such as grants,
bank loans, crowdfunding or friends and family does not qualify (`cloud.google.com/startup`,
read 2026-10-22).

**A domain email and a live product site.** AWS Founders, DigitalOcean, Google, MongoDB and
NVIDIA all require an address on the company's own domain, and Google also requires the billing
account to be administered by a user on that domain. DigitalOcean states the raise as a ceiling
rather than a floor, at USD 10m or less (`digitalocean.com/startups`, read 2026-10-22), which is
the one place in the class where raising less is an advantage. It also publishes the only
explicit route around the investor requirement: 'Please fill out the application here and select
Other when prompted for an affiliated partner organization'. With no partner, the award depends
on a program manager and the amount stays unnamed until the onboarding email.

**A card, and a human reading the project.** Lambda states 'A valid credit card is required to
prevent fraud and calculate tax' and limits eligibility by country, including the EU except
Lithuania, the UK, the US, Japan, South Korea, Singapore and Taiwan. Zylora's entry tier needs a
card and no review. CloudRift needs neither a card nor a company, and reviews a project every
two weeks.

⭐ The gate rises with the amount, monotonically. USD 200 asks for a personal LinkedIn account.
USD 1,000 asks for a domain, a website and a card. USD 5,000 to USD 60,000 asks for a registered
legal entity. USD 200,000 asks for a venture firm's Organizational ID. No programme in the slice
gives a large amount to a natural person, and none claims to.

## What the credit buys in GPU-hours

Only one programme carries both a credit and the vendor's own hourly rate. Lambda pays USD 1,000
and sells GPU time on the same platform, and the rate record quotes Lambda's price page
(`lambda.ai/pricing`, read 2026-10-22): H100 SXM at USD 3.99 a GPU-hour, A100 SXM 80 GB at USD
2.79, B200 SXM6 at USD 6.69.

The division, on the credit alone:

- USD 1,000 / USD 3.99 = 250.6, so 250 H100-hours
- USD 1,000 / USD 2.79 = 358.4, so 358 A100 80 GB-hours
- USD 1,000 / USD 6.69 = 149.5, so 149 B200-hours

That is `inferred` arithmetic on two `documented` inputs, checkable in one step. The credit also
covers persistent storage at USD 0.20/GB/month, which spends the same balance: 100 GB held for a
month is USD 20, or USD 20 / USD 3.99 = 5.0 H100-hours. Ingress and egress carry no fee on this
offer, so traffic does not compete with compute. The credit covers B200, H100, A100 and GH200
on-demand instances, so 250 H100-hours is an upper bound rather than a promise.

For every other programme the division cannot be done. CloudRift names three card classes and no
hourly rate. Zylora names no card class. AWS, Google, Oracle and Databricks sell GPU shapes
whose prices vary by shape and region, and no record here pairs one with the credit. Computing
those hours would need a rate that was not recorded, and a rate that was not recorded is an
invented number.

## What the class does not give

**A live programme at DigitalOcean under the old name.** Hatch is withdrawn, and its own terms
page says so: 'The Hatch Program is no longer an active program offered by DigitalOcean, and has
been replaced with DigitalOcean Startups Program'
(`digitalocean.com/legal/hatch-terms-of-service`, read 2026-10-22). The short URL answers with a
301 to `/startups`, which serves 200. A legacy landing page still publishes the old accelerator
requirement; the live page supersedes it.

**Published amounts, in four cases.** MongoDB names four tiers by funding stage and publishes no
dollar value for any of them; one partner landing page states up to USD 5,000 in Atlas credits,
which the programme page does not repeat, so the record holds null. NVIDIA Inception advertises
'Access free cloud credits from NVIDIA and partners' with no amount, tier or expiry.
DigitalOcean leaves the amount to the partner and states only the monthly ceiling: 'Participants
generally are entitled to a USD 10,000 monthly limit (and charges apply for any use in a month
exceeding this amount)'. Databricks publishes the USD 200,000 ceiling and not the tier that
yields it, so none can be sized before an applicant commits.

**A GPU slice at DigitalOcean.** The core credits exclude GPU Droplets, H100 GPU Kubernetes,
Bare Metal GPUs, Dedicated Inference and Serverless Inference, quoted as of 2026-05-13. An award
is CPU capacity and managed databases; GPU access is a separate application and is not covered.

**The Google Start tier, for an individual.** USD 2,000 is the smallest Google tier and it still
asks for a working MVP, a clear business model and plans to seek venture funding soon. The page
also states that applications may be rejected for a high volume of AI-generated site content,
which screens the website rather than the legal form.

**A standalone Lambda programme and an agreed Oracle figure.** Third-party listings put the
Lambda figure between USD 1,000 and USD 7,500; the vendor page says USD 1,000, so USD 1,000 is
recorded, and the credit exists only as an Inception benefit. For Oracle, third-party summaries
publish USD 100,000 from the rules and USD 60,000 from the launch announcement, while the UK
terms state 'The value of Universal Credits available under the Program ranges from USD 5,000 to
USD 60,000'. Whether the programme covers a given country is not verified.

## The pattern: not a discount, a different customer class

A programme that requires a company is not selling the same compute more cheaply. It is buying a
relationship with a different kind of customer, and the eligibility list is the purchase order.
The AWS Portfolio Org ID is issued by the investor, so the programme reaches companies a venture
firm has already screened; Databricks and Google gate on the round itself; Oracle verifies
corporate identity and ownership. In each case the credit is acquisition spend against a funded
balance sheet, and the value to the vendor is the paying account that follows the credit.

Three consequences follow. Ranking these programmes by credit size ranks them by gate: USD
200,000 is 87 times the USD 2,300 a reader can reach (200,000 / 2,300 = 87.0), and the
multiplier measures the distance between two customer classes rather than the generosity of one.
An application to a gated programme has a cost and no measurable return, because the review is
where rejection happens. And an unpublished amount is a refusal in a quieter form: MongoDB,
Inception and DigitalOcean accept a company-shaped applicant and decline to say what the award
is, so a null cell beats a number from a stale press release.

## How it composes

AWS Founders does not disqualify a later Portfolio application, so the chain for a founder who
later joins an accelerator is Founders first, Portfolio after. The Kiro startup credit promotion
excludes applicants who already hold Activate credits, so the two cannot be stacked. Both are
the record's composition notes, not a vendor page.

Lambda's credit is reachable only through Inception, and Inception is the front door to partner
credits rather than a credit itself. The published partner credit found here is Lambda's USD
1,000, which demands incorporation too, so every link in the chain needs a company. Databricks
funds Neon Postgres from the same approval, so one award covers a warehouse and an application
database.

The storage topic's `aws-activate` record keeps the same numbers and not the corrected
identity field; `dossier/compute/aws-activate-founders.json` is the authority on who may apply.

## What would change the answer

- **An approval reported with no legal entity.** Would move AWS Founders from `qualifies-with-caveat`
  to `qualifies` and confirm USD 1,000 of the reachable total.
- **A waiver of incorporation for solo founders.** Would unlock Lambda's USD 1,000, which is 250
  H100-hours at USD 3.99.
- **A published DigitalOcean award amount, or CloudRift hourly rates.** Either would replace a null
  cell with a usable number; the USD 10,000 monthly ceiling suggests a DigitalOcean term could
  exceed the other four together.
- **Written confirmation of Oracle's country scope.** The UK terms state the amount and the term;
  the regional scope is unverified, and an unverified scope is not an offer.
- **Either small vendor closing.** CloudRift and Zylora carry USD 1,100 of the total on pages that a
  two-person company could withdraw in a week.

## Scope and what was not measured

This document covers the 13 records in the table and nothing else, all read from
`dossier/compute/` on 2026-10-22. No application was submitted, no account was created and no
credit was spent, so no award, rejection or balance is observed. The USD 2,300 is a sum of
vendor ceilings and floors, not a measured balance, and the GPU-hour divisions are arithmetic
rather than a run.

The records: `aws-activate-founders`, `aws-activate-portfolio`, `cloudrift-ai-grant`,
`databricks`, `digitalocean-hatch`, `digitalocean-startups`, `google`, `lambda-cloud-credits`,
`microsoft`, `mongodb`, `nvidia-inception`, `oracle-startup-growth` and `zylora-startup-gpu`,
each at `dossier/compute/<slug>.json`.
