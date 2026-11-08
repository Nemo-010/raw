# Student packs: what sits behind the enrolment gate, and who can pass it

This document answers one question: how much compute is locked behind a student or education
identity gate, how each gate is checked, and which checks a reader with no
enrolment can pass. The sixteen records give one answer. Every gate that carries compute is a
gate on enrolment, and the one gate a reader passes outright carries no compute.

A reader who passes both GPU gates holds 160 GPU hours in the first enrolled year, 100 one-shot
from StarverseAI plus 5 a month from CamberCloud over twelve months. A reader who clears the
Microsoft student programme holds USD 150 a month of Azure credit, which is USD 1,800 a year and
18 times what Azure for Students gives. None of it is reachable without enrolment.

## The short answer

Sorted by what a reader can reach: open first, then person-gated, then institution-gated,
then dead. `Verdict` is the record's own field.

| Programme | What is given | Verification route | Renewable | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- |
| `aws-educate` | Simulated EC2, S3, RDS, VPC and Cloud Operations labs; no provisioned account | nothing: an email address, at age 13 or over | no credit to renew; access is stated as open | the labs are simulated, so there is no quota to exhaust | fails-quota |
| `jetbrains-student-pack` | 10 IDEs; a one-IDE route gives eight of them singly | nothing for a one-IDE route; for the full pack, a university email, an ISIC/ITIC card, an official document, or the GitHub pack | one year for the full pack, renewed annually | no compute in either route; the full pack needs enrolment proof | fails-quota |
| `github-student-developer` | About 60 partner offers, 5 of them compute | a school ID photo with a current enrolment date, a class schedule, a transcript, or an enrolment letter; an academic email where the school is verified that way | 2 years per validation, then revalidate | one document review decides all 60 offers | fails-identity |
| `azure` | 750 hours each of B1s, B2pts v2 and B2ats v2 a month; 720 vCore hours of a 4- or 8-vCore instance; USD 100 for 12 months | an institution-issued email address, plus an attestation of full-time study | yearly, while a student | the institution email | fails-identity |
| `freevps-edu-pl` freevps.edu.pl | a free Windows VPS; the page states no core count or RAM figure | student verification, and the page does not describe which document it accepts | not stated | the verification step, which is not described | fails-identity |
| `microsoft-learn-student` | USD 150 a month of Azure credit | full-time enrolment, an existing Azure for Students account, and onboarding activities that are reviewed | monthly | the enrolment fact, then the review after it | fails-identity |
| `cambercloud-student-plan` | 40 CPU hours, 5 GPU hours, 50 GB of storage and 50 agent messages a month | an active GitHub Student Developer Pack | monthly, while enrolled | pack verification; then core-scaling spends the hours faster than the clock | fails-identity |
| `github-copilot-student` | Unlimited completions plus an allowance of GitHub AI Credits, auto model selection only | the GitHub Education student verification | rechecked every month | verification lapse, and a model list fixed to auto selection | fails-identity |
| `deepnote-education-plan` | Unlimited basic machines at 2 vCPU and 5 GiB; advanced machines, scheduling and AI excluded | a school email address connected to the account | not described in the record | the school email; the machine is 2 vCPU | fails-identity |
| `boxedtux` | 1 vCPU, 1 GiB DDR5, 10 GB NVMe, 200 GB a month, an IPv6 /64, no IPv4, at EUR 0 | an institutional address; the FAQ says other routes come "at a later time" | 6-month terms aligned with semesters, with re-verification | the box is deleted the moment a term expires, with no grace period | fails-identity |
| `starverseai-student-support` | 100 hours of A10 or RTX 4090 time once, plus a CNY 10 trial credit | an .edu address, a CHSI enrolment code, or a student card upload, reviewed within 30 minutes | one-shot; no renewal | the .edu or CHSI check; there is one grant only | fails-identity |
| `sakura-cloud-student` | JPY 100,000 a month of cloud resources | a Sakura Cloud certification pass plus enrolment at a Japanese school | monthly, while enrolled | Japanese enrolment; the exam comes before it | fails-identity |
| `1517-medici-project` | USD 1,000 cash, with no claim on the project or its IP | nothing: the route is career stage, quoted as "high school, college students, and dropouts", by email with a five-minute video | one-time | the payment rail, which the fund says cannot pay outside North America | fails-identity |
| `aws-academy` | A teaching curriculum for the institution; a student gets Skill Builder for 12 months and community access | an institution joins the programme, and an enrolled educator runs the course | Skill Builder for 12 months | the institution must join first, and no compute allowance is stated | fails-quota |
| `digitalocean-2` | The USD 200 pack credit, as it was | pack membership, which no longer applies | none; the offer ended | withdrawn, with the balance expired | dead |
| `digitalocean-student-credit` | The same USD 200 credit | the same pack membership | none | ended after 2026-07-31; remaining balance expired on 2026-08-01 | dead |

## The distinction that decides everything

⭐ Two different things are checked under the word "student", and they behave in opposite ways
for a reader with no affiliation.

**A check on the person** asks whether the applicant is enrolled somewhere. The evidence is a document
about the applicant: a student card, a transcript, a class schedule, an enrolment letter, or an address
the institution issues only to the people it enrols. In principle a person can answer this,
because the only requirement is that some accredited institution has enrolled them.

**A check on the institution** asks whether the applicant's school has joined something. The evidence is a
tenant, a domain the school administers, or a purchase order, and no individual can cause it.
`aws-academy` is the pure case. `sakura-cloud-student` is a person check with a country
condition that fails a non-resident before the certification exam.

The academic address sits in between, and the gap is where a reader without an institution falls. It is evidence
about the person, but its issuer is the institution, so it behaves as an institution check for
anyone the institution has not admitted. `azure` states it in that form: "You must verify your
academic status through your organization's email address"
(`learn.microsoft.com/en-us/azure/education-hub/faq`, read 2026-10-22). A Microsoft Q&A answer
the same day records the result: without a college or university address the student
subscription cannot be started, and a document-based fallback is not guaranteed.

⚠ A third kind hides in the vocabulary. `1517-medici-project` checks neither: eligibility is
career stage and the route is an email with a five-minute video, so its gate is the payment
rail. The record carries `identity_cost.kind` as `card` while its detail describes a geographic
restriction rather than a card requirement, which is the one field here I would reassign.

## The programmes gated on the person

### GitHub Student Developer Pack

`github-student-developer` is the hub of the lane, and it is the row to read first because the
other compute rows route through it. The pack is about 60 partner offers, mostly software
licences, and the live list read on 2026-10-22 carries five compute-bearing ones: Azure with a
USD 100 credit, Camber with 40 CPU hours and 5 GPU hours a month, Heroku with USD 13 a month for
24 months, Codespaces at Pro level, and Deepnote with 2 vCPU and 5 GiB machines.

The verification is the best documented here, and it is a person check. The application requires
documents proving current student status, and the accepted set is named: a picture of a school
ID with a current enrolment date, a class schedule, a transcript, or an affiliation or
enrolment verification letter
(`docs.github.com/en/education/about-github-education/github-education-for-students/apply-to-github-education-as-a-student`,
read 2026-10-22). The same page closes the address shortcut for some schools: where the system
detects prior applicants from a school verified by academic email, future applicants from that
school must also use an academic email. Validation lasts 2 years, after which the holder must
revalidate, and offers may not be redeemed more than once (pack terms, read 2026-10-22).

One review decides all 60 offers and one lapse removes all 60, which is why the record grades
the binding constraint as `write-gated`. Five of about 60 offers provision anything that runs
code. A sixth, `github-copilot-student`, is a model allowance rather than a machine, and it is
not one of those five.

### Azure for Students

`azure` is the only compute-bearing student grant from a tier-one cloud in this slice, and its
quota is large enough to plan against if the gate were passable: 750 hours each of three
burstable VM families a month, 720 vCore hours of a 4- or 8-vCore instance, 100,000 vCore
seconds of serverless SQL, and a USD 100 credit usable within 12 months. 750 hours a month
covers one VM of each family continuously, because a 31-day month is 744 hours; 720 vCore hours
on a 4-vCore instance is 180 wall-clock hours a month. ⚠ The amounts run for 12 months and
apply to new customers only, so the grant is a year of three small machines, not a permanent
allowance.

The gate is the address. The education FAQ requires an attestation of full-time study at an
accredited, degree-granting, two-year or four-year institution, and names the organisation's
email address as the verification method (`learn.microsoft.com/en-us/azure/education-hub/faq`,
read 2026-10-22). The signup page says the school
email is used to sign up and to renew yearly while a student. One account per person is the cap,
and the end is stated: when the credit is not used within its period, the subscription and its
products are disabled.

### Microsoft Learn Student Ambassadors

`microsoft-learn-student` carries the largest recurring student compute figure in this lane:
USD 150 a month of Azure credit, quoted beside Microsoft 365 and Visual Studio Enterprise.
Registration is described as open with no application, to students in all degree fields and
levels, part-time or full-time. The eligibility behind that sentence is narrower: at least 18,
enrolled full-time at an accredited academic institution, and already an Azure for Students
account holder (`mvp.microsoft.com/en-us/faq`, read 2026-10-22).

So the credit is a second door behind the Azure address gate, and onboarding activities are
reviewed before the benefit arrives, which is why the binding constraint is `write-gated`.
USD 150 a month renews monthly rather than yearly: one year is USD 1,800 against USD 100.
That the two do not add to USD 1,900 is `inferred`, because the ambassador credit sits on the
student subscription that must exist first, and no record states whether the credits stack. The
record does not describe how full-time enrolment is proved.

### CamberCloud Student plan

`cambercloud-student-plan` is the smallest compute grant here and the one with the clearest
billing failure. The pack changelog dated 2026-08-20 lists 40 CPU hours, 5 GPU hours, 50 GB of
storage and 50 agent messages a month, free while enrolled. The route is a GitHub sign-in that
requires an active Student Developer Pack, so its gate is `github-student-developer` by
reference.

The vendor publishes the rates that price it. One Camber Credit is USD 1, a CPU node of 16
cores and 64 GB costs 0.64 credits an hour, and the XSMALL GPU node with one L4, 8 cores and
32 GB costs 1.5 credits an hour (`docs.cambercloud.com/docs/nodes-pricing/`, read 2026-10-22).
So 5 GPU hours is 7.5 credits, USD 7.50, and 40 CPU hours is 2.5 wall-clock hours on the
16-core node at 1.6 credits. The monthly grant is 9.1 credits, USD 9.10, against the record's
own range of about USD 9 to USD 14.

⚠ The failure mode is the meter, not the size. Three users on the vendor's community tracker
report a dashboard cap of 40 CPU hours against an offer that said 200, and one measured more
than 6 hours billed for about 10 minutes of use, attributed to core-scaling on a 64 GB instance
(read 2026-10-22; open at the last comment on 2026-06-11). A per-core meter in front of a
per-core price table is how a 40-hour grant becomes an afternoon.

⭐ The same vendor gives 100 free credits, USD 100, on the ordinary free trial to anyone with an
email, while the student plan gives about USD 9 a month and needs enrolment proof.

### Copilot Student, Deepnote and JetBrains

`github-copilot-student` is inference rather than compute, and it is here because it is the one
pack offer that is a model allowance. The plans table puts Copilot Student at Free with an
allowance of GitHub AI Credits, auto model selection only and third-party agents excluded,
against Copilot Pro at USD 10 a month with a base of 1,000 credits (read 2026-10-22). GitHub
reevaluates eligibility every month, so the licence lapses the month verification does, which
makes this offer lapsed-on-graduation by construction rather than by policy. ⚠ The record does
not describe the check: it defers to the GitHub Education review documented above.

`deepnote-education-plan` is the smallest machine here: the Education plan is free for students,
teachers and researchers who connect their accounts to school email addresses, and it excludes
advanced compute machines, scheduling and Deepnote AI (`deepnote.com/docs/edu-overview`, read
2026-10-22). The pack describes the same offer as unlimited basic machines with up to 5 GiB of
RAM and 2 vCPU, a smaller reading than the vendor page implies. The gate is the school address,
and neither page describes the renewal cadence.

`jetbrains-student-pack` is the one row with a route that needs no verification. The full pack
is 10 IDEs plus a JetBrains AI Pro trial, verified by a university email address, an ISIC or
ITIC card, an official document, or the GitHub pack. Beside it, stated as needing no student
verification, is a one-IDE option covering IntelliJ IDEA, PyCharm, CLion, WebStorm, RustRover,
Rider, RubyMine and DataGrip.

⭐ The ISIC route looks like the loophole in this lane, because an international student card
sounds purchasable. It is not: the issuer says the card is available only to full-time students
and requires dated proof of current full-time study (`isic.org/support/`, read 2026-10-22). That
collapses four routes into one gate. The pack is valid for one year and renewed annually, and
the record does not describe what graduation does. A free non-commercial licence beside the
pack covers six of the IDEs with no enrolment condition (`sales.jetbrains.com`, read 2026-10-22).

`boxedtux` is the only real machine in the slice: 1 vCPU, 1 GiB DDR5, 10 GB NVMe, an IPv6 /64,
no IPv4, 200 GB a month on a 50 Mbit/s port, at EUR 0 with no card. The eligible list is entirely
academic: enrolled students, teachers, research projects, bootcamp participants and high-school IT
programmes. The FAQ says routes without an .edu domain will come "at a later time", and names a
discretionary programme for non-profit projects (`boxedtux.com`, read 2026-10-22; probed at 200,
31,698 bytes). ⚠ The term is 6 months, aligned with semesters, and expiry is immediate: no grace
period, and 200 GB a month is not a backup allowance.

### StarverseAI and Sakura Cloud

`starverseai-student-support` carries the largest GPU-hour grant in this class: 100 hours of
A10 or RTX 4090 time plus a CNY 10 trial credit, for full-time students, announced 2026-03-07.
The applicant uploads a student card or a CHSI verification code, or enters an .edu address,
and review is stated to take under 30 minutes. The anti-abuse layer is face recognition plus a
device fingerprint.

The grant is one-shot. At the vendor's rates of CNY 1.8 an hour for an RTX 4090 and CNY 2.2 for
an A10, 100 hours is worth CNY 180 to 220, which is the record's own figure. A second
sponsorship on the same site gives .edu.cn holders a CNY 500 voucher described as more than 300
hours of RTX 4090 or 80 hours of A100 40G (`starverse-ai.com/guide/archives/2130`, read
2026-10-22), so a Chinese academic address holds more than 400 hours of 4090 time once, and any
other .edu address holds 100.

`sakura-cloud-student` is the largest monthly allowance in the lane and the least reachable:
JPY 100,000 a month of cloud resources, against a passed Sakura Cloud certification and
enrolment at a Japanese university, graduate school, college of technology, vocational school
or high school. The record also carries a narrower Sakura programme as `reported`: free cloud
for college-of-technology students, free for one year (`kknews.co.jp/news/20240903o02`, read
2026-10-22).

⚠ The Sakura record's quoted fields are damaged: `free_tier.stated` and its first evidence row
both open with a bare `' 10 '` and a bare `' Web '` where the Japanese should be, because the
text did not survive extraction. The amount and the eligibility list survived in the English
summary, so the record is usable, but the quote cannot be checked from it.

## The programme gated on the institution

`aws-academy` is the only pure institution gate with a cloud vendor behind it, and it gives a
student no compute. The programme provides higher education institutions with a free,
ready-to-teach cloud curriculum; a student receives a Skill Builder subscription for 12 months
and community access after course completion; educators receive exam discounts and the same
subscription (`aws.amazon.com/training/awsacademy/`, read 2026-10-22). No compute allowance is
stated for either group. The gate is a tenant with a course in it. This is the row that
student-offer lists most often confuse with `aws-educate`, and the confusion runs in the
expensive direction.

## The programmes with no student gate

`aws-educate` is the one programme here that a reader passes outright. The page states it is
open to any individual regardless of where they are in their education, technical experience or
career journey, and that learners as young as 13 can register with just an email address
(`aws.amazon.com/education/awseducate/`, read 2026-10-22). The registration form asks for name,
country, city, birth month and year, and an email address, and requests no enrolment document.

The programme's own FAQ states what a lab is: a simulated environment where a user interacts
with AWS services and applies theoretical knowledge. There is no provisioned account, no quota
to exhaust, no egress to meter and no wall clock that ends with a resource to lose, which is
why the record grades the constraint as `none`. A reader who needs to practise the EC2 console
gets that here; a reader who needs a machine does not.

`1517-medici-project` is the second programme with no student check and the one that names
dropouts explicitly. The fund gives USD 1,000 cash grants, with no claim on the project or the
IP, to "high school, college students, and dropouts", by email to any partner with a five-minute
Loom video (`1517fund.com/medici`, read 2026-10-22). The gate is the payment rail: the fund
states it cannot issue grants to teams outside North America, and the rail it names is Venmo,
which is US-only. USD 1,000 is real and unreachable for a reader based elsewhere.

## The renewal cadence, and what graduation does

The records state the cadence in five different units.

| Programme | Cadence | What the record says at the end |
| --- | --- | --- |
| `github-student-developer` | 2 years per validation | revalidate student status; offers may not be redeemed again |
| `github-copilot-student` | rechecked every month | eligibility is reevaluated monthly, so the licence lapses the month it fails |
| `azure` | yearly, while a student | the subscription and its products are disabled when the credit period ends |
| `cambercloud-student-plan`, `microsoft-learn-student` | monthly credit | "while you're enrolled" for Camber; no end condition stated for the ambassador credit |
| `boxedtux` | 6-month terms aligned with semesters | expired boxes are deleted immediately, with no grace period |
| `starverseai-student-support` | one-shot | nothing to lapse; the 100 hours are spent once |
| `jetbrains-student-pack` | one year, renewed annually | graduation is not described |
| `sakura-cloud-student`, `aws-academy` | monthly, 12 months | no end condition stated; the course ends with the subscription |
| `digitalocean-2`, `digitalocean-student-credit` | ended | the credit expired and the balance did not roll over |

⭐ Only two records state what graduation does, and they state it in different units: two years
for the pack, one month for Copilot. A graduate loses the licence first and the pack second.

## What the class does not give

- **No GPU hour without enrolment.** Both GPU grants sit behind enrolment, so the class total is
  zero, not a small number.
- **No always-on machine.** Every row that provisions a machine deletes it at a term end
  (`boxedtux`) or runs it inside a student credit that expires.
- **No institution-tenant route.** `aws-academy` gives a student a curriculum, not capacity.
- **No USD 200 cloud credit.** `digitalocean-2` and `digitalocean-student-credit` record its
  withdrawal, so any list still advertising it is stale.

## What would change the answer

One page would move the largest row. `azure` and `microsoft-learn-student` rest on the same
organisation-email requirement, and a published alternative proof, such as an enrolment letter
reviewed by hand, would move `azure` from `fails-identity` to reachable for a reader who can
obtain any enrolment at all. The Microsoft Q&A row already hints that a document fallback exists
in some cases and is not guaranteed.

A fresh read would move the GPU total. `starverseai-student-support` rests on one vendor blog post
plus a homepage with no education section, and its 100 hours are the largest GPU grant in the
class. If that announcement has been superseded, the total drops from 160 hours to 60.
