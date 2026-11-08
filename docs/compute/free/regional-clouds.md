# Regional clouds: identity decides before capacity does, in 18 records from seven countries

This page answers one question. What will a regional cloud or VPS provider outside the United States
and the European Union give one person with no company, no local tax number, no local card and no
local address? The answer is thinner than the marketing numbers suggest, and it is concentrated in
one provider.

Across 18 records, seven fail on identity before any quota is reached and six are trials of days or
one credit. One allowance is large enough to plan on: Savannaa's 750 hours a month for twelve months,
which is 9,000 hours of a 1 GiB instance in Lagos. GPU capacity across the slice is zero hours.

Seventeen records are at the `documented` rung, one is `unverified`, and none is `measured`, because
no account was registered at any of these providers. The identity column is a reading of a signup
form, not an executed registration, and one row carries a contradiction inside its record: GoCloud's
`identity_cost.kind` is `email`, while its own detail says the gate was not established because every
signup page returned a shell. The table shows both.
`docs/compute/gaps.md` records the same gap for the whole topic.

## The comparison, sorted by what the front door costs

The sort is the decision. The doors run from an email address, to a phone of any country, to a phone
of one country, to a card, to a national identity number, to an institution, to a closed lane.

| Provider | Country | Free or cheapest offer | Shape | Identity | What fails first | Counterparty | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HostNowNow Flux | Nigeria | Flux Free, perpetual, no overage billed | not stated | email | 100 GB a month across 10 projects, then it stops | none named | qualifies-with-caveat |
| Savannaa | Nigeria | 750 hours a month for 12 months plus NGN 10,000 | 1-2 vCPU / 1 GiB / 10 GB | email plus a phone from NG, GH, KE or ZA | the public IPv4 bills at NGN 4,360 a month | none named | qualifies-with-caveat |
| shellter.me | not stated | a perpetual 150 MB bash account | 150 MB of ZFS, 3 IPv6 | email or GitHub | an automated anti-abuse suspension, no threshold published | none, and it says so: "Two people, no company" | qualifies-with-caveat |
| GoCloud | Nigeria | USD 300 of startup credit, no card | 1 vCPU / 512 MiB / 10 GiB | `email` in the record, `not established` in its own words: no signup form was reachable | the credit is one-time and its expiry is not published | a trading name, "GoCloud by Metronet", with an Abuja address and no company number | trial-only |
| Jagoan Cloud | Indonesia | IDR 150,000, 30-day trial | 1 vCPU / 1 GiB | email | the free box has no public IPv4, only NAT and IPv6 | none named | trial-only |
| Liara | Iran | 500,000 toman of signup credit | not stated | email | an IPv4 address alone costs 200,000 toman a month | none named | trial-only |
| Nevacloud | Indonesia | IDR 50,000 promo code | not stated | email plus a public social post | the credit is awarded by selection, not on signup | none named | trial-only |
| PenDC | Turkey | two months of free hosting | not stated | email | claimed through a contact form, not a checkout | none named | trial-only |
| VK Cloud | Russia | RUB 5,000 for an individual, 60 days | not stated | email, from an IP in Russia, on a corporate domain | the network origin, which no document supplies | none named | fails-identity |
| RUVDS | Russia | 3-day trial of any configuration under RUB 3,000 a month | 2 vCPU / 2 GiB | any phone plus email | 72 hours in total | none named | trial-only |
| Beget | Russia | a perpetual 1 GiB shared host | 1 GiB SSD, 25,000 files | a phone from RU, BY, UA or KZ | the phone number country | none named | fails-identity |
| Cloud.ru Evolution | Russia | RUB 4,000, valid 60 days | not stated | a bank card never used on Cloud.ru, and an account registered in Russia | the Russian registration the 2026-06-30 rules require | none named; Sber ID is offered as a login route, which states no ownership | fails-identity |
| Selectel | Russia | none | no free lane | card | the entry point is a RUB 100 top-up | none named | paid-only |
| Magalu Cloud | Brazil | BRL 100 over the first two months | 1 vCPU / 1 GiB / 10 GB | a CPF or CNPJ plus a card | the Brazilian tax number | none named | fails-identity |
| Timeweb Cloud grant | Russia | up to RUB 1,000,000 over 6 months | not stated | a Russian resident sole proprietor or legal entity | GPU servers are excluded from the grant | none named | fails-identity |
| Nobus Cloud | Nigeria, Kenya | up to NGN 500,000,000 across a cohort | not stated | a company registration number | the per-applicant amount is not published | none named; it asks the applicant for a number and gives none of its own | fails-identity |
| FOSSVPS | not stated | 2 vCPU / 4 GiB / 64 GiB, no charge | 2 vCPU / 4 GiB / 64 GiB | reputation on LET or LES | a reputation gate, a country block, and node end dates | none named; six nodes are sponsored by named hosting brands | fails-identity |
| Yandex Cloud | Russia | withdrawn for new clients | no free lane | a legal entity paying by wire transfer | nothing is granted at all | none named | dead |

⚠ **No counterparty is named in any of the 18 records.** Sixteen of the rows above begin `none
named`. Thirteen are the bare two words. Three attach a qualifier and still name nobody: Cloud.ru
offers Sber ID as a login route, Nobus Cloud asks the applicant for a company registration number
while publishing none of its own, and FOSSVPS lists six sponsor brands behind its nodes without an
operator entity. shellter.me is the only row that states the absence itself, in the words "Two
people, no company", and GoCloud is the only row with a trading name, "GoCloud by Metronet", an
Abuja street address and a `metronetgroup.com` mailbox but no company number. A trading name is not
a legal person. Not one of the 18 was checked against a company register, so no row here says who
would answer a claim. That matters more in this slice than in most, because a niche provider is the point of it:
the further a provider sits from a household name, the more the absence
of a legal person costs.

## The sum: 9,072 hours, of which 99.2 per cent is one provider

Savannaa gives 750 hours a month for twelve months, pooled across two instance types and two cities.
750 hours a month is 31.25 days of continuous running, so the pool is slightly more than one
always-on instance: 750 x 12 = 9,000 hours. The rate card prices that instance at NGN 32,438.35 a
month, so 12 x NGN 32,438.35 = NGN 389,260.20 of compute given away. `savannaa.com/pricing/rates`
(read 2026-10-22) states "t2.micro | 1 | 1 GB | 10 GB | NGN 32,438.35".

RUVDS adds 3 x 24 = 72 hours on a 2 vCPU, 2 GiB box. 9,000 + 72 = 9,072 hours, of which 9,000 /
9,072 = 99.2 per cent comes from one provider. The rest is one month of an Indonesian box, a shell
account, a 100 GB application allowance, and credits in six currencies.

⛔ **The credits are not added, and this page will not add them.** They are denominated in RUB, USD,
BRL, IDR, NGN and toman, and no record carries a rate with a date for any pair except one. Savannaa's
rate card fixes its own naira prices at NGN 1,327.24 per USD as of 2026-09-30 and states that "Naira
prices don't move with the exchange rate". That fixes one vendor's price list. It is not a market
rate, and using it on a ruble grant produces a number that describes nothing.

⭐ **The GPU addition is available and it equals zero.** Cloud.ru excludes GPU compute, ML Inference,
Foundation Models and GPU notebooks. Timeweb excludes dedicated servers, GPU servers and AI agents.
GoCloud lists a vGPU line with no price and no free lane. 0 + 0 + 0 = 0 hours.

## Three doors, not two

**The identity door.** A CPF for Magalu Cloud, Russian tax residency for the Timeweb grant, a company
registration number for Nobus Cloud, a phone from RU, BY, UA or KZ for Beget, an account registered in
Russia for Cloud.ru, forum reputation for FOSSVPS. Each is a document or a standing a reader cannot
produce, so each is `fails-identity`. VK Cloud fails here too, on the network rather than on the
document, and the paragraph below gives that gate.

**The payment rail.** A card for Cloud.ru, specifically one never previously attached to any Cloud.ru
account. A RUB 100 top-up for Selectel. BRL 5.00 to BRL 9.99 of card verification for Magalu Cloud. A
card needs a banking relationship in the country; an identity number needs residency. Liara is the
clean split: the account opens on an email and only spend beyond the credit needs an Iranian route.

**The network door.** `cloud.vk.ru/bonus/` (read 2026-10-22) conditions RUB 5,000 on an account
registered from an IP in Russia on a corporate domain. FOSSVPS blocks VPN registration and blocks
registration from Russia, China and North Korea. No passport fixes either condition.

⚠ **A `fails-identity` row is a result, not a hole.** The quota exists, the price is published, and the
door is named. An unreachable quota is worth zero, and saying so is the finding.

## Russia and the CIS: seven records, one perpetual tier, and it is a shared host

**Beget** is a perpetual shared host, not a virtual machine. `beget.com/ru/hosting/free` (read
2026-10-22) gives 1 GiB of SSD, one site, one database, a 25,000-file limit, PHP and MySQL, with no
support. The door is a mobile number from RU, BY, UA or KZ and an SMS code, and
`beget.com/ru/rulesfree` (read 2026-10-22) lets the provider demand documents proving the details.
Record: `dossier/compute/beget.json`.

**Cloud.ru Evolution** gives RUB 4,000 for 60 days, on a card never previously attached to any Cloud.ru
account. `cloud.ru/docs/billing/ug/topics/concepts__start_grant` (read 2026-10-22) excludes GPU compute,
ML Inference, Foundation Models, GPU notebooks and Container Apps, so the credit buys CPU time only.
The verdict is `fails-identity` rather than `trial-only` because the campaign rules approved on
2026-06-30 require the account to be registered in the Russian Federation, and the 2 vCPU / 4 GiB
free VM is closed to accounts registered after that date; what survives for a new account is 25
vCPU-hours a month of Container Apps and the object-storage egress allowance.
Record: `dossier/compute/cloud-ru-evolution.json`.

**VK Cloud** gives RUB 5,000 for an individual and RUB 12,000 for a legal entity, valid 60 days, and only
RUB 2,000 of the individual bonus reaches virtual machines. `cloud.vk.ru/bonus/` (read 2026-10-22)
requires an account registered from an IP in Russia on a corporate domain, and the startup grant of up
to RUB 2,000,000 is entity-gated. Record: `dossier/compute/vk-cloud.json`.

**RUVDS** is the one Russian provider here that an individual outside Russia can reach, because the door
is any phone number rather than a passport. `ruvds.com/vps_test/` (read 2026-10-22): any tariff under
RUB 3,000 a month, free for 3 days, no card, one IP, any data-centre, Windows licences included. Three
days measures round-trip time and confirms an outbound route. Record: `dossier/compute/ruvds.json`.

**Selectel** has no entry lane. `selectel.ru/services/cloud/servers/` (read 2026-10-22) states in its FAQ
that there is no free testing for cloud servers and that evaluating one costs a RUB 100 top-up, and the
grant of up to RUB 30,000 is for legal entities and sole proprietors only. The durable item is 3 TB of
pooled free egress, recorded from `docs.selectel.ru/cloud-servers/about/payment/` (read 2026-10-22):
billing deducts external traffic above a free allowance of 3 TB across all projects of the account.
Record: `dossier/compute/selectel.json`.

**The Timeweb Cloud grant** is the largest Russian number and the least reachable: up to RUB 1,000,000
for up to 6 months, one bonus to one rouble. `timeweb.cloud/grant` (read 2026-10-22) limits the
participant to a resident of the Russian Federation, including a sole proprietor or a legal entity, and
excludes dedicated servers, GPU servers and AI agents. Record: `dossier/compute/timeweb-cloud-grant.json`.

**Yandex Cloud** is dead for a new account. `yandex.cloud/en/docs/getting-started/free-trial/concepts/quickstart`
(read 2026-10-22) states: "Currently, the trial period and introduction grant are unavailable for new
clients", and the trial survives only for businesses paying by wire transfer. The search index still
advertises RUB 4,000, KZT 20,000 and USD 30. Record: `dossier/compute/yandex-cloud.json`.

## Two community hosts: a real machine behind an editorial gate

**FOSSVPS** is the largest free shape in the slice: 2 vCPU, 4 GiB of RAM, 64 GiB of disk, dual-stack NAT
plus IPv6, at six locations with named sponsors. `fossvps.org/` (read 2026-10-22) prints a sponsor end
date per node, and two of the six have already passed: buc1 on 2026-04-17 and buc2 on 2026-10-17. A
rebuild destroys the data.
`lowendspirit.com/discussion/10909` (2026-05-27) records the host accepting reputation only from LET
or LES and blocking VPN registration, throwaway email and registration from Russia, China and North
Korea. Record: `dossier/compute/fossvps.json`.

**shellter.me** is the smallest shape and the most honest page: a bash account on FreeBSD, 150 MB of ZFS
home, three IPv6 addresses with reverse DNS the user sets, SSH on port 2222. `shellter.me/rules` (read
2026-10-22) states no paid tier and no SLA, warns at 75 days without a login and archives at 90, and the
host attributes a same-day suspension reported in the launch thread to "our automatic anti abuse
system". The appeal route is IRC. Record: `dossier/compute/shellter-me.json`.

## Brazil: one record, one tax number, and free egress

**Magalu Cloud** is the most interesting refusal in the slice, because the offer behind the door is
good: BRL 100 over the first two months, on a card carrying a BRL 5.00 to BRL 9.99 verification charge.
`docs.magalu.cloud/docs/billing/bss/billing-info/billing-information` (read 2026-10-22) requires a valid
CPF or CNPJ, a billing address and a card, and the tax number cannot be changed later. The cheapest
instance is 1 vCPU, 1 GB and 10 GB at BRL 34.99 per 730 hours, so BRL 100 covers 100 / 34.99 = 2.86
months. Record: `dossier/compute/magalu-cloud.json`.

⭐ **The prize is egress.** `docs.magalu.cloud/docs/network/prices` (read 2026-10-22) lists egress for
public IPs, NAT and NAT Gateway at "Sem custo" per GiB in both br-se1 and br-ne1, and states that none
of that traffic is charged at the moment. "At the moment" is the constraint: a practice, not a term.

## Nigeria and Kenya: four records, one perpetual tier, and the only free egress schedule

**Savannaa** is the closest thing in the corpus to a regional hyperscaler micro tier.
`savannaa.com/pricing/free-tier` (read 2026-10-22): 750 hours a month of t2.micro (1 vCPU, 1 GiB, 10 GB)
or t3.micro (2 vCPU, 1 GiB, 10 GB) for the first twelve months in Lagos and Abuja, pooled across both
types and regions. It includes NGN 10,000 of credit with no expiry, and the page states "Always free: Not
offered yet". `savannaa.com/docs?section=getting-started` (read 2026-10-22) needs an email and a recovery
number from NG, GH, KE or ZA, and no payment method. ⚠ The exclusion that decides the verdict is the
address: `savannaa.com/pricing/rates` (read 2026-10-22) bills public IPs at NGN 4,360.00 a month, so a
reachable server costs that while the compute is free. Egress is not charged until 2026-12-31; from
2027-01-01 the account gets 5 TB a month included, then NGN 15.00 per GB. The API limit is 60 requests a
minute with a burst of 10 a second. Record: `dossier/compute/savannaa.json`.

**HostNowNow Flux** is the only perpetual application tier in the slice:
`hostnownow.com/products/flux` (read 2026-10-22) gives 10 projects and 100 GB of bandwidth, TLS, DDoS
protection and a managed WAF, an OpenAI-compatible inference endpoint per project billed in naira, and
"never bills overage". A traffic spike stops the service instead of producing an invoice. The per-project
memory and CPU cap is not stated. Record: `dossier/compute/hostnownow-flux.json`.

**GoCloud** is the unusual door for the region: USD 300 of startup credit, no card, and no national-ID or
BVN mention on the pages read. `gocloud.africa/services` (read 2026-10-24) prices the smallest
machine at "$0.00595/hr" and "$6.00/mo" for 1 vCPU, 512 MiB, 10 GiB and 500 GiB of transfer,
per instance. The credit is one-time and the name suggests incorporation, so the door is unverified:
`/signup`, `/register`, `/startups`, `/free-trial` and `/terms` all return shells with no form. ⚠ A
vGPU line is listed with no price and no spec. Record: `dossier/compute/gocloud.json`.

**Nobus Cloud** carries the largest headline and it is not a quota: "Up to 500 million naira worth of
cloud credit" (`nobus.io/partner-catalyst`, read 2026-10-22), on a form requiring a Business Name and a
Company Registration or Incorporation Number. The per-applicant amount is published nowhere checked, so
NGN 500,000,000 is a fund. The reachable piece is the Deploy route, up to NGN 70,000 by selection.
Record: `dossier/compute/nobus-cloud.json`.

## Indonesia: two records, and the credit is a contest or a clock

**Jagoan Cloud** grants IDR 150,000 on registration, advertised on the signup form as "Get Free IDR
150.000 Credit Bonus for 30 Days Trial". `maobuni.com/2022/09/02/jagoan-freevps/` (read 2026-10-22)
reports an OVZ NAT VPS with a 20 Mbps cap, no public IPv4, and a 768 MB instance consuming the
IDR 150,000 in a month; the lowest paid tier is IDR 45,182 for 1 core. Record:
`dossier/compute/jagoan-cloud.json`.

**Nevacloud** is the same market with an editorial gate. `nevacloud.com/en/free-vps/` (read 2026-10-22):
"You'll get a Nevacloud promo code that can be redeemed for IDR 50,000 in credit", within 30 days, one per
email, Twitter and Instagram account, after following the provider and sharing a post. Record:
`dossier/compute/nevacloud.json`.

## Turkey and Iran: two records where the free lane is a conversation

**PenDC** states "2 AY UCRETSIZ BARINDIRMA", two months of free hosting, on the homepage, linking to a
contact page. `pendc.com/` (read 2026-10-22) publishes no configuration, no traffic term and no price
there, so all three are dashes.
`technopat.net/sosyal/konu/bedava-veya-ucuz-vds-var-mi.3713191/` (read 2026-10-22) states three months
instead of two, and neither figure is a published quota. Record: `dossier/compute/pendc.json`.

**Liara** is the exception in the Iranian market, because the door is an email address.
`console.liara.ir/` (read 2026-10-22) accepts an email or a mobile number. The signup gift is 500,000
toman, which the record labels IRR-equivalent, raised from 200,000 toman. `liara.ir/products/iranian-vps/`
(read 2026-10-22) prices 2,500 toman per GB downloaded with upload free, and adds 200,000 toman a month
for an IPv4 address, so the address alone consumes 40 per cent of the credit. ⚠ The free-hosting lane
contradicts itself inside one page: `liara.ir/products/free-cloud-host/` (read 2026-10-22) states that
free hosting is not provided while international connectivity is limited, and the copy below still
offers a free plan.
Record: `dossier/compute/liara.json`.

## The export pattern: a payment rail, never a second price list

⛔ **None of the 18 records carries a second price list for a foreign market**, so this page states no
out-of-market price for any of them. What the records do carry is four cross-border mechanisms, and only
one of them is a price.

- **Savannaa** fixes naira prices at NGN 1,327.24 per USD as of 2026-09-30 and states that "Naira prices
  don't move with the exchange rate". That hedges its own currency; it does not open a foreign market.
- **RUVDS** is reported to accept foreign cards through a processor settling in USD, per
  `russiable.com/russian-vps-hosting/` (read 2026-10-22). A payment rail, not a rate.
- **GoCloud** prices in USD on its home page, so a foreign buyer reads the same USD 6.00 a month a Lagos
  buyer reads. A quoting convention, not a discount.
- **FOSSVPS and shellter.me** serve a global audience with no country pricing at all, and FOSSVPS excludes
  three countries at registration. Free capacity with no price has no export question.

A local card, a local price and a local identity are three separate obstacles, and RUVDS is reported to
solve the first without touching the other two.

## What the class does not give

**No probe of any interface.** Fourteen of the 18 records carry `interface: unknown`, three assert REST
and one asserts SSH, and every value is marked "inferred from the tooling the provider documents; not
probed". The only interface number in the slice is Savannaa's 60 requests a minute. Budget a control
panel and a wiki.

**Egress is unpublished at 14 of 18.** Only Magalu Cloud, Savannaa, HostNowNow Flux and Selectel publish
a term, and one of the four publishes a term that expires on a date. `dossier/compute/selectel.json`
contradicts itself here: its `egress` field says no term was found, while its third evidence row records
the 3 TB free allowance and its `chaining` note repeats the figure. The evidence row is the artefact, so
the 3 TB stands and the `egress` field is the error. `docs/compute/gaps.md` records the same gap for the
whole topic and its figure is stale: it states 854 of 957 records, and the same test run on 2026-10-24
returns 844 of 1,255, of which 308 are the literal string "not published on the source card".

**No object storage in the compute records.** Where these providers sell object storage it is priced in
the storage topic, and `docs/storage/paid/regional.md` measures the class: Beget S3 at USD 26.04 per TB
per month with free egress and Cloud.ru Evolution at USD 14.07 per TB. The regional rate sits above the
global floor in both cases. The cheap part of a regional market is bandwidth, not disk. That document
also carries `beget`, `cloud-ru-evolution`, `ruvds` and `selectel` as storage records.

**One timezone of support, and sometimes none.** Beget states that no technical support is provided on
the free tier. shellter.me is two people and an IRC channel. FOSSVPS and PenDC answer through a forum
thread and a contact form. A ticket queue in one timezone decides whether an unattended job is
recoverable.

**Twelve of the 18 records carry no vCPU or RAM figure.** The table shows a dash for eight of them and
"no free lane" for Selectel and Yandex Cloud, and the other two state a disk and nothing more: Beget at
1 GiB and shellter.me at 150 MB, both from their own offer text. A credit of RUB 4,000 with no SKU is a
budget, not a machine.

## How it composes

The one useful composition is Savannaa plus anything else: a 1 GiB instance in Lagos with free egress
until 2026-12-31 holds state and serves West African traffic at zero egress cost, while compute that needs
more memory runs where the free tier is largest. The public IP is the only unavoidable charge in the chain.

The second is RUVDS as an instrument rather than a host: three days on a Russian box measures round-trip
time and confirms whether an outbound route exists from a Russian address. Pair it with
`docs/compute/measurement.md`.

⚠ **FOSSVPS and shellter.me are not storage.** A FOSSVPS node ends on a printed date and a rebuild
destroys the data; a shellter.me account archives at 90 days without a login.

## Coverage: Poland, Kazakhstan, Israel, and two records that arrived late

The lane names Russia and the CIS, Brazil, Poland, Turkey, Israel, Nigeria, Kenya and Kazakhstan. The 18
records carry providers in seven countries: Russia (7), Nigeria and Kenya (4), Indonesia (2), Brazil (1),
Turkey (1) and Iran (1), which is 16 of the 18. Indonesia and Iran were not on the list and are in the
slice. Poland, Israel and Kazakhstan are on the list and are not.

Kazakhstan appears once as a phone country Beget accepts, and once as a withdrawn figure in the Yandex
index snippet, KZT 20,000 for residents. That is not a provider record. ⛔ **No Polish or Israeli provider
is in this slice**, and the absence is a gap in the slice rather than a finding about either market.

⚠ **Two records reached the dossier after this slice was cut, and neither states a country.**
`freevps-edu-pl` offers a Windows VPS to students and gates on student verification, which the page does
not describe; that is an institution door of a kind the 18 do not contain, so the verdict is
`fails-identity`. `gladiolus-vm-gl` offers Linux VMs on human review, with no shape, no egress term and no
published number of machines, so the gate is a judgement rather than a quota; the verdict is
`qualifies-with-caveat`. Two records inside the slice carry no home country either: FOSSVPS runs sponsored
nodes in Frankfurt, Chisinau and Bucharest among others, and shellter.me's pages do not name a location.

## What would change a verdict

**A Russian IP address, or a phone number that receives an SMS.** VK Cloud's RUB 5,000 and Beget's 1 GiB
host both turn on that one fact, and no record here attempted the registration that would settle it.

**A CPF.** Magalu Cloud's BRL 100 and its free egress unlock on a Brazilian tax number. If egress stays at
"Sem custo", a CPF turns a refusal into the only free-egress regional cloud in the corpus.

**One signup at Savannaa.** The 9,000 hours are a page claim. The public IP charge, the hour metering,
whether the twelve months start at signup, and whether a second account is allowed are unmeasured. That
verdict moves on a registration and a bill, not on another reading.

**A price on GoCloud's vGPU line.** A free or cheap GPU minute in Lagos would be the first GPU capacity
in this class and would change the zero in the sum.

**One reachable GoCloud signup page.** Every signup route returns a shell, so the `email` kind in that
record is a guess its own detail contradicts, and the USD 300 credit cannot be claimed or tested until
a form exists. One readable `/signup` would settle the identity door and move the record off
`unverified`.

**A fresh FOSSVPS node list.** Every node carries an end date. One node has already terminated (buc1,
2026-04-17), one is past (buc2, 2026-10-17) and the next two fall on 2026-11-22 and 2026-12-21, and the
record's two evidence rows disagree on whether the printed range starts 2026-10-17 or 2026-12-21. The
live node count is unknown.
