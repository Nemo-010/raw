# Asia's two lanes: the free machine, and the door that is shut

This document answers one question: which cloud or notebook provider in China, Korea, Japan,
Indonesia, Vietnam, India or Central Asia gives a reader capacity at no cost, and what stops it
first. Twenty-one records are in scope, all read on 2026-10-22.

The count decides the value. Four of the 21 renew: `cepatcloud-id`, `dothome`, `mikrus-frog` and
`zoho-catalyst`, and two of those, `dothome` and `zoho-catalyst`, ask only for an email. Five carry
`fails-identity`, two are dead, eight sell a clock, and two charge from the first minute. The
published GPU total is zero hours.

## The short answer

Rows are ordered by country. `Lane` separates a domestic site from an international one, because
the two are different products with different doors. No row here has a GPU.

| Provider | Country | Lane | Free offer | Shape | Identity | What fails first | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Alibaba Cloud International `alibaba-cloud-international` | China | international | USD 90 for 3 months, USD 0.25 an hour ceiling, 220 GB egress a month | 2 vCPU, 4 GiB | card, phone, KYC | the credit at the USD 0.25 ceiling: 360 hours, 15 days | trial-only |
| Alibaba Cloud, mainland lane (same record) | China | domestic | CNY 300 quota, quoted in the record | 4 vCPU, 8 GiB maximum | Chinese verification | a mainland identity | fails-identity |
| Tencent Cloud International `tencent-cloud-international` | China | international | Lighthouse or CVM for 3 months, COS 50 GB for 6 months | 2 vCPU, 4 GiB | passport-class ID | the 2 to 4 day review | fails-identity |
| Huawei Cloud International `huawei-cloud-international` | China | international | withdrawn; the terms still claim 12 months | none listed | email, phone, card | the campaign page is gone | dead |
| Dothome `dothome` | Korea | domestic | 500 MB disk, 15 GB traffic a month, renewed every 6 months | shared host | email, captcha | the byte counter | qualifies-with-caveat |
| KakaoCloud `kakaocloud` | Korea | domestic | KRW 300,000 for 3 months, 30 GiB outbound a month | 2 vCPU, 0.5 GB | business licence | a Korean company | fails-identity |
| NAVER Cloud Platform `naver-cloud-platform` | Korea | domestic | KRW 100,000 for 3 months; a Micro Server for 1 year for residents | not published | card, phone | residence in Korea | trial-only |
| NHN Cloud `nhn-cloud` | Korea | domestic | KRW 200,000 for 1 year, GPU excluded | not published | KR or JP phone | the phone country | fails-identity |
| ConoHa VPS `conoha-vps` | Japan | domestic | JPY 360 coupon on a card | 512 MB minimum plan | card | 11.5 days at 512 MB | trial-only |
| Sakura Cloud `sakura-cloud-2` | Japan | domestic | none; both coupon routes have closed | not published | card | no free tier at all | paid-only |
| Sakura Cloud certification `sakura-cloud-certification` | Japan | domestic | 1 month, about 50 places a month | not published | JP address, voice call | the phone call | fails-identity |
| CepatCloud.id `cepatcloud-id` | Indonesia | domestic | 15 GB SSD, 1 core, 2 GiB, 100 Mbit/s, "Rp 0 selamanya" | 1 vCPU, 2 GiB | email, WhatsApp | manual activation | qualifies-with-caveat |
| mini.biz.id `mini-biz-id` | Indonesia | domestic | withdrawn: 750 MB, SSH | none | anonymous | the domain is for sale | dead |
| Bizfly Cloud `bizfly-cloud` | Vietnam | domestic | 3 days of a 2-core server; 10 GB cold storage a month for a year | 2 vCPU, 2 GiB | email | the 3-day clock | trial-only |
| VNG Cloud `vng-cloud` | Vietnam | domestic | VND 3,500,000 to 20,000,000, or USD 150, for 30 days | not published | business email | a registered company | fails-identity |
| NeevCloud `neevcloud` | India | domestic | INR 2,000 of CPU credit for 7 days; 10 GPU credits | not published | email | the 7-day clock | trial-only |
| Utho `utho` | India | domestic | INR 1,800, or USD 25 for 30 days | not published | card | three conflicting figures | trial-only |
| Zoho Catalyst `zoho-catalyst` | India | international | 25,000 GB-seconds and 900 GB-minutes a month, USD 250 for 6 months | serverless | email | 15 GB-hours of container | qualifies-with-caveat |
| Hoster.kz `hoster-kz` | Kazakhstan | domestic | 7 days by application | 1 vCPU, 1 GiB | any phone | sales approval | trial-only |
| oblako.kz `oblako-kz` | Kazakhstan | domestic | 3 days individual, 5 days legal | 8 vCPU, 16 GiB, 200 GB | any phone | a discretionary ticket | trial-only |
| Mikrus FROG `mikrus-frog` | Poland | domestic | 256 MB and 3 GB, perpetual | 1 vCPU, 0.25 GiB | card, PLN 5 once | a 3-month login sweep | qualifies-with-caveat |
| THE.Hosting `the-hosting-review-for-days-scheme` | Turkey | domestic | none; 30, 14 or 7 extra days after a paid month | none | email | a purchase first | paid-only |

The verdicts sum to 21 records: eight `trial-only`, five `fails-identity`, four
`qualifies-with-caveat`, two `dead`, two `paid-only`. The mainland Alibaba row is the 22nd row and
not a 22nd record: it is the fourth evidence row inside `alibaba-cloud-international`.

⚠ Eighteen of the 21 records state no egress term on the page they read. The other three give a figure
(`alibaba-cloud-international`: 220 GB a month), an archived page, and a third-party comparison
(`kakaocloud`: 30 GiB outbound).

⚠ Five records quote a page whose script is not Latin, and their quote fields lost the original
text on the way into the dossier. They are `dothome` and `naver-cloud-platform` for Korean,
`sakura-cloud-2` and `sakura-cloud-certification` for Japanese, and `alibaba-cloud-international`
for Chinese, whose quotes keep the numerals and drop the words. A sixth record,
`huawei-cloud-international`, lost one Chinese FAQ quote. This document gives the record's English
gloss, marks it as a gloss, and repeats no translated number the record lacks.

## One brand, two doors: the Chinese lane split

Alibaba Cloud, Tencent Cloud and Huawei Cloud each run a domestic site and an international site:
separate trials, card requirements, region lists and identity checks. `alibaba-cloud-international`
carries both lanes in one record. The mainland lane is a CNY 300 quota capped at 4 vCPU and 8 GiB
across seven regions including Hong Kong, and it needs Chinese identity verification, so the CNY 300
is `fails-identity` at the door for a registrant without a PRC identity
(`help.aliyun.com/en/ecs/user-guide/ecs-free-trial`, read 2026-10-22, quoted in the record). The
international lane is USD 90 behind a card, which is why that record is `trial-only`. The other two
records cover the international lane only: `tencent-cloud-international` holds no domestic figure,
and `huawei-cloud-international` has no live offer on either lane.

### Alibaba Cloud International

The offer in the vendor's words: a free quota of `USD 90.00` valid 3 months for ECS instances and
system disks, an hourly charge ceiling of `USD 0.25/`, and `220 GB` a month of free internet traffic
split as `200 GB + 20 GB`, meaning 200 GB outside mainland China and 20 GB inside, inbound free
(`documented`, `alibabacloud.com/blog/599911`, read 2026-10-22).

USD 90 divided by USD 0.25 an hour is 360 hours, which is 15 days at the ceiling, and the trial ends
at 3 months. The 200 GB a month is the only term that survives a quiet account, so an idle box wastes
the credit and a busy one meets egress first. Binding constraint: `volume-quota`. The record carries
2 vCPU and 4 GiB, and the credit names no shape.

Identity, quoted: eligibility needs `a verified phone number and a payment method`, and the accepted
methods are `Credit card (Visa, Mastercard, AMEX, or JCB with international payment enabled)`, a debit
card on the same networks, or `PayTM (available for users in India)`; `PayPal is not supported`; a
risk-control block requires KYC
(`alibabacloud.com/help/en/user-center/product-overview/learn-about-free-trials`, read 2026-10-22).
The phone is the gate a passport cannot open.

⚠ The USD 300 figure in credit roundups is stale: a third party dated its correction 2026-08-21 and
said the official free page lists per-product trials, with the ECS USD 90 as the compute-relevant
one (`reported`, `buildaicurrent.com/credits/alibaba-cloud-free-credits/`, read 2026-10-22).

### Tencent Cloud International

The offer, quoted: `LighthouseFree Trial for 3 months` on a `Lighthouse 2C2G30M`, `Cloud Virtual
MachineFree Trial for 3 months` on a `CVM S5 2C4G`, `COS 50GB Free Trial for 6 months`, `EdgeOne
Free Trial for 14 days`, and `Show you 30 trial products` (`documented`,
`tencentcloud.com/act/pro/FreeTier`, read 2026-10-22). The page states the trial runs at least to
2026-12-31. Shape is 2 vCPU and 4 GiB, matching `CVM S5 2C4G`; the names disagree on memory, since
`2C2G30M` names 2 GB where `2C4G` names 4 GB.

Identity, quoted: `You need to prepare a valid ID Card, passport, driver's license, or work permit
issued by a government authority in the jurisdiction where your account is registered`, from `the
same country/region as your account registration location`, reviewed `within 2-4 business days`
(`tencentcloud.com/document/product/378/10495`, read 2026-10-22). The door and the number belong in
one sentence: the 3-month Lighthouse is 90 days of a 2-core machine, and its key is a government
document from the country the account names. A passport is a document a foreigner normally holds, so
this is the softest gate in the Chinese lane, and it is still a real-name check. Recorded as
`national-id` and `fails-identity`.

⚠ The card requirement is contested: a third-party summary says a USD 1 pre-authorisation is taken
and virtual cards are refused, while Tencent's own walkthrough describes verification replacing the
card (`reported`, `studentoffers.co/offer/tencent-cloud`, read 2026-10-22).

### Huawei Cloud International

The offer is withdrawn. The campaign page returns 200 and serves `This page is no longer available.
Please go to our homepage to see more.` on two separate URLs
(`activity.huaweicloud.com/intl/en-us/free_packages/` and its `index.html`, read 2026-10-22). The
surviving terms page still claims `the free usage of specified products for 12 months from the
registration date` for accounts registered after 2025-01-01, and points for the product list to the
dead page.

Three surfaces still advertise it: a students page, a support FAQ last updated 2022-09-29 that says
the package is auto-issued, and the Brazil region page, which carries `Cota de uso de 1500 horas
gratuitas por 12 meses para 10 produtos populares` (1500 free hours for 12 months across 10
products) and `10 produtos que s o sempre gratuitos` (10 products that are always free). Those pages
repeat a withdrawn offer, so the 1,500 hours counts as zero.

## Korea: one durable host and three credits behind three doors

**Dothome** is the durable one. The free plan gives `500 MB` of disk, `15 GB` of traffic a month, a
supplied base domain and unlimited databases, on PHP 7.4, 8.0, 8.2 or 8.4 with MySQL 8.x, and the page
description reads "apply now for lifetime free hosting" (gloss). Renew every six months and it stays
free. The flow is email verification, a Google reCAPTCHA, then apply, with no phone step in the
documented flow (`docs.dothome.co.kr/books/9bf31/page/084b6`, read 2026-10-22). Egress is unpublished.
The free plan excludes SSH and domain connection; SSH costs KRW 500 a month. ⚠ Whether member signup
adds a Korean real-name step is not established. First failure is the byte counter, second is the
missing shell.

**KakaoCloud** gives `KRW 300,000` of credit to a new customer who registers a payment method and
applies within 3 months of signup, with 30 GiB a month of outbound data free. The door is a business:
signup requires a copy of the business registration certificate and its number as a mandatory first
step (`docs.kakaocloud.com/start/quickstart-guide/sign-up`, read 2026-10-22). Two startup tracks are
larger and also need a legal entity, at `KRW 5,000,000` for a year and `KRW 35,000,000` over two years.

**NAVER Cloud Platform** gives `KRW 100,000` after a payment method is registered, valid 3 months. A
separate Micro Server is free for one year, one per person, only where the country of residence is
Korea. Signup asks for country of residence, member type and language, and fixes the payment currency
by country (`ncloud.com/join/info`, read 2026-10-22). ⚠ Two live pages disagree on the credit, at
KRW 100,000 and at "up to KRW 300,000". A student lane at KRW 200,000 needs an academic address
(`fin-ncloud.com/main/creditEvent`, read 2026-10-22). This record corrects the corpus entry
`naver-cloud`, which graded the provider `paid-only` from a page with no credit event.

**NHN Cloud** gives `KRW 200,000` for one year on Compute instances, and the exclusions matter: GPU
Instance, Notification and marketplace products are out. It is one per phone number and one per
business number. Members split by country into Korean and Japanese members, and an individual needs a
mobile phone that can receive an SMS (`docs.nhncloud.com/ko/nhncloud/ko/user-guide/`, read
2026-10-22). Korea personal pays by PAYCO credit card or credit card; Japan by credit card only. The
Korean sum has four lanes. One perpetual shared host takes an email. KRW 300,000 sits behind a
Korean business licence. KRW 200,000 sits behind a Korean or Japanese phone. KRW 100,000 sits
behind a card and expires after 3 months.

## Japan: no standing free tier, and two coupon routes that closed

**ConoHa VPS** runs a coupon, not a trial: `JPY 360` for accounts newly registered from the campaign
page with a credit card attached. The page converts the coupon into free days per plan: about 11.5
days on 512 MB, 7.9 on 1 GB, 4.1 on 2 GB and 1.1 on 12 GB, falling to 2.8 hours on 128 GB, with GPU
types excluded (`vps.conoha.jp/campaign/freestart2026/`, read 2026-10-22). ⚠ The campaign ended
2026-10-01 16:00, before the read date, so this coupon may be closed. The support FAQ says there is no
free trial and points at a referrer programme instead.

**Sakura Cloud** has no free trial and says so: the FAQ answers "we do not offer a free trial; use
coupons instead" (gloss). The coupon channel was real and large, at `JPY 50,000` for the basic
certification exam and `JPY 10,000` for the update exam with a 12-month free window once applied, and
distribution ended with the third 2026 sitting. A separate campaign offered `JPY 25,000` to the first
500 applicants between 2026-04-08 and 2026-09-30, also closed. A coupon still needs a card on file,
because billing starts when the balance reaches zero. On the record's own arithmetic, JPY 50,000 was
about 32 months of the smallest server at JPY 1,540 a month.

**Sakura Cloud certification** is the near-miss worth reading: a one-month free learning environment,
about 50 applicants a month, and no card, since no credit card registration is required and any member
ID can apply (gloss). Then the second gate closes it. Registration wants a Japanese address and a
Japanese phone, and Sakura Cloud requires phone verification by voice call before any resource can be
created (`help.sakura.ad.jp/purpose_beginner/2545/`, read 2026-10-22), so the identity cost is
`country-phone` for Japan.

## Indonesia: the largest free shape, and a dead one

**CepatCloud.id** publishes the best specification in the region: `Rp 0 selamanya` (Rp 0 forever),
`15GB SSD Storage`, `1 Core CPU 2GB Ram`, `100Mb/s Unlimited Bandwidth`, `1 IPv6 & 1 IPv4 Private`,
`Ubuntu / Debian OS Only`, one per person, for Indonesian citizens, on the 2026-04-17 Wayback capture.
The live terms page adds that activation needs `Verifikasi alamat email dan Verifikasi nomor Whatsapp`
(email address and WhatsApp number verification), and that a VPS detected as unused `akan kami hapus`
(will be deleted) (`cepatcloud.id/terms-of-services/`, read 2026-10-22). What fails first is a person:
the offer page returned 530, DNS failed at the probe, and a crawl returned no pages. Two independent
users in August 2025 report registering and receiving no activation, calling the service `slow
respond atau udah nggak aktif` (slow to respond or no longer active) (`reported`,
`diskusiwebhosting.com/threads/vps-gratis-cepatcloudid-masih-jalan.39308/`, read 2026-10-22).

**mini.biz.id** published a `Micro 1` plan at `Rp0/mo, Free forever` with 750 MB, SSH, HTTP and
WebSocket on a shared public IPv4, and now redirects to a domain marketplace listing with a TLS name
mismatch at the probe. Verdict `dead`. ⚠ This is the second lapsed Indonesian free-VPS hobby project
in this slice, which is the pattern rather than the exception.

## Vietnam: three days, or a business licence

**Bizfly Cloud** gives a 3-day trial of one Cloud Server at up to 2 cores, 2 GB RAM and 60 GB SSD,
quoted as `Cloud Server - Prebuilt App | 3 ngay | ... Ram: 2 GB CPU: 2 Core HDD: 100GB hoac SDD: 60GB`,
with the account's resources kept no more than seven days after expiry
(`bizflycloud.vn/docs/platform_overview/chinh_sach_dung_thu`, read 2026-10-22). A storage trial beside
it gives 10 GB of cold storage free every month for a year, quoted as `10 GB Cold Storage mien phi
hang thang trong trong thoi han mot nam`. Identity is an email and no card. Viettel IDC advertises a
free trial with no card and no published duration (`reported`,
`viettelidc.com.vn/tin-tuc/dang-ky-trai-nghiem-chuong-trinh-vps-free-trial`, read 2026-10-22).

**VNG Cloud** gives `VND 3,500,000` to `VND 20,000,000` for 30 days on vServer and vStorage, and
admits only businesses, `Doanh Nghi p` in the page's folded text, that have never used the platform,
with full business details and a corporate email domain. The live form is headed `Try VNG Cloud for
free with US$150 credits in 30 days` and requires Company email, Company Name and Job Title
(`documented`, `vngcloud.vn/promotions/`, read 2026-10-22). ⚠ The policy page still says the programme runs to
2023-12-31 while the form is live, so the campaign may be a rolling renewal of one page. The conflict
does not change the verdict, which is `fails-identity` on the company email domain.

## India: the free tier is CPU, and the GPU is a conversation

**NeevCloud** states `Sign up today and claim INR 2,000 in FREE CPU Cloud credits, valid for 7 days`,
and separately that `your account is credited with 10 free credits to help you explore and deploy your
first GPU instance` (`docs.ai.neevcloud.com/getting-started/billing-wallet`, read 2026-10-22). The two
halves never meet: the INR 2,000 covers CPU only and burns in 7 days, and the 10 GPU credits have no
published credit-to-rupee rate, so the GPU allowance is unknown until an account exists. H100 clusters
are `USD 2.99` a GPU-hour on demand, with `Free Trial available for H100 GPU Clusters. Contact Us Now`,
which is a sales conversation and not a tier. The honest GPU sum for this slice is zero published
hours: 10 credits of unpublished value, plus one H100 trial that requires a call. No record here
states a GST number or a company registration for NeevCloud, Utho or Zoho, so the company-shaped gates
in this slice are KakaoCloud's business licence and VNG's corporate domain.

**Utho** is a warning about two numbers on one page. The landing page says `Try MicroHost Cloud free
with Rs.1800 Credit.` and, in the same view, `USD 25, 30-day free trial requires valid credit card`. A
third-party catalogue reports `INR 1,000 in free cloud credits for new users without a credit
card` (`reported`, `startupperklist.com/offers/utho/free-signup-credits`, read 2026-10-22). Three
sources, three figures, and the card is the identity cost.

**Zoho Catalyst** is the strongest reachable free tier in the slice, because the door is a Zoho
account rather than an Aadhaar number or a GST certificate. The monthly allowance renews forever:
`25,000 GB-seconds` of function execution, `900 GB-minutes` of AppSail container runtime, `2 GB-days`
of data store, `1,000,000` LLM input tokens and `500,000` output tokens through QuickML, `1,800
CPU-seconds` of model training, `100,000` API Gateway requests and `300,000` Web Client Hosting
requests, plus `USD 250 in credits` for the first six months (`catalyst.zoho.com/free-tier/`, read
2026-10-22).

The container is where the arithmetic bites: 900 GB-minutes divided by 60 is 15 GB-hours, so one
always-on 1 GiB container runs about 15 hours a month, and the same allowance gives a 512 MiB
container about 30 hours. ⚠ The tier applies only on the pay-as-you-go model, and the record did not
establish that model as card-free.

## Central Asia: seven days, by application

**Hoster.kz** gives a free test of up to 7 days through an online request form, on a ladder whose
smallest plan is `Cloud 1-1-25`: 25 GB NVMe, 1 GB RAM, 1 vCPU and 1 IP at KZT 3,100 a month, in
Almaty, Astana or Karaganda. The next step is `Cloud 1-2-50` at KZT 4,800 (`hoster.kz/cloud/vps/` and
`hoster.kz/support/oblachnyy-server/8451/`, read 2026-10-22). The record's own conversion puts
KZT 3,100 at roughly USD 6 a month. ⚠ Kazakhstan has no perpetual free tier: a comparison dated
2026-08-28 gives Hoster.kz 7 free days, AdminVPS.kz 7 free days at KZT 3,235, PS.kz a 14-day refund
rather than a free server, and Serverspace a bonus shown only after registration (`reported`,
`clex.kz`, read 2026-10-22).

**oblako.kz** gives the largest single-machine test in the set: up to 5 days for legal entities and 3
days for individuals, capped at 8 CPU, 16 GB RAM and 200 GB disk, by support ticket after phone
confirmation, and the provider states it may refuse without giving a reason
(`oblako.kz/help/billing/testoviy-period`, read 2026-10-22). Verdict `trial-only` and `write-gated`:
8 vCPU and 16 GiB is a real burst shape, and a discretionary approval is not a quota a plan can rely on.

## Two rows from outside the region

**Mikrus FROG** gives 256 MB RAM, 3 GB disk and Alpine Linux on LXC, one server per person, released by
a one-off identity payment of any amount from `PLN 5` upward: `wymagaja wplaty dowolnej kwoty (minimum
5zl) w ramach weryfikacji tozsamosci uzytkownika. Jest to oplata jednorazowa` (a payment of any amount,
minimum PLN 5, for user identity verification; a one-off fee). Servers with no login for 3 months are
deleted, the page asks Asian users not to activate, and it states the free box cannot carry an agent
stack: `Serwery FROG nie maja szans udzwignac rozwiazan typu N8N, Claude Code, Codex` (`frog.mikr.us/`,
read 2026-10-22).

**THE.Hosting** is not a free tier in any reading. Step one is to order or extend a VPS for at least
one month, quoted as `Mevcut VPS'yi en az 1 ay i in sipari edin veya uzat n`, and the reward for an
honest review plus following the social accounts is `ek 30, 14 veya 7 gun` (an extra 30, 14 or 7 days)
by plan tier (`the.hosting/tr/gift-vps`, read 2026-10-22). The same mechanism runs at
`profitserver.net/tr/server4feedback/`, read 2026-10-22. Verdict `paid-only`: the free days are a
rebate worth at most one month, behind a purchase.

## What the class does not give

- **No free GPU hours with a published rate.** The slice holds one GPU credit (NeevCloud, 10 credits)
  with no rate, and one H100 trial behind a sales call: 0 quotable GPU hours.
- **No Chinese mainland notebook in this slice.** That lane is covered outside this document:
  `modelscope-notebook` (100 AMD GPU hours on registration, gated by a national ID),
  `atomgit-notebook` (1,000 core-hours a month on Ascend 910B, gated by a country phone), `simpfun`
  (4 vCPU and 16 GiB kept alive by a daily check-in, behind a CNY 1 identity fee) and
  `miracleplus-compute` (an accelerator screen at roughly 2 per cent acceptance). None takes an email.
- **No Korean or Japanese notebook offer**, only virtual machines, coupons and a shared host.
- **No perpetual virtual machine.** The four renewing rows are a shared PHP host, a serverless runtime,
  a 256 MB LXC container and a dormant Indonesian VPS.
- **No domestic-lane access to any of the three Chinese brands.** Every mainland trial gates on
  real-name verification. The cross-record `alibaba-cloud-tencent` prices the domestic lanes at 7 days
  for Alibaba, 15 for Tencent, 30 for Huawei, 7 for Baidu and 15 for JD, all behind a national identity
  document.
- **No published egress term** for 18 of the 21 records.

## How it composes

Dothome is the only no-card state store here: a Korean-region PHP and MySQL host with a supplied
domain, which a free compute row elsewhere can call over HTTP. Zoho Catalyst is the only row that
budgets across months, since the USD 250 wallet carries a burst build for six months and the monthly
tier keeps a scheduled function alive afterwards.

## What would change the answer

- **A Tencent signup.** It settles the card question and whether a passport from outside the region
  passes the identity review, and if it does, the 90-day 2-core machine is the largest Chinese offer.
- **A NAVER signup and a Utho signup.** They settle KRW 100,000 against "up to KRW 300,000", and
  INR 1,800 against INR 1,000 and USD 25.
- **A live Alibaba free page.** `alibabacloud.com/free` (read 2026-10-22) is login-gated and served
  no content to any reader route, so the per-product list was never read directly.
- **A restored Huawei campaign page**, or a first-party product list: that would move `dead` to a trial
  and give the 12-month claim a subject.
- **A Dothome signup attempt**, to settle whether member registration adds a Korean real-name step.
- **One email to CepatCloud**, to settle whether the Indonesian 2 GiB perpetual VPS is dormant.
