# Forum hosts: 55 records from four non-English markets, and the document each door asks for

This page answers one question. What do the Chinese, Russian, Korean and Japanese forums
offer that English-language sources do not? The answer is 55
records. Each market has a published floor: CNY 99 a year for a four-core machine in China,
RUB 169 a month in Russia, KRW 5,040 a month in Korea, and JPY 290 a month in Japan. Three of
the four name a card as the gate, and one of the three documents it: the Russian and Korean
floor records carry `identity_cost.kind: card` with no evidence row behind the word, so those
two are unverified. The Chinese one takes an age band and a mainland ICP filing.

The tree holds 1,411 compute records, and 113 carry a CJK character anywhere
in the file. 37 of those 113 are the records below. No
record here is `measured`. 44 are
`documented`, which means a vendor page stated the figure. 11 are `reported`, which means a
third party stated it and no vendor page with the number was read.

⚠ **The CJK count depends on the tree it is run against.** The 2026-10-22 count
was 957 records and 59 with CJK evidence, the 2026-10-24 count was 1,239 and 75, and a later merge the same day took it to
1,255; the 2026-11-08 count is 1,411 and 113. All these numbers are small against
the corpus, so the argument does not change.

## 1. What each language added

The four language lanes came back with 55 records between them. The counts are of records, not
of providers, because two providers here carry two offers each.

| lane | forums and boards read | records | dead | fails-identity | cheapest paid machine, list price |
| --- | --- | --- | --- | --- | --- |
| Chinese | hostloc.com, nodeseek.com, nodeloc.com, v2ex.com | 21 | 1 | 3 | Lanmao Cloud at CNY 2.62/month on a 75-percent-off code, not a list price |
| Russian | vc.ru, habr.com, lowendtalk.com, hosters.ru, freerank.ru | 15 | 2 | 2 | RuWeb from RUB 169/month, specification not published |
| Korean | discuss.pytorch.kr, help.megazone.com, vendor notice boards | 11 | 1 | 3 | XDN IDC at KRW 5,040/month, on a 12-month term |
| Japanese | 5ch hosting threads, vendor notice and price pages, prtimes.jp | 8 | 0 | 0 | WebARENA Indigo at JPY 290/month before tax |

"Cheapest paid machine, list price" is the most useful column and the weakest one. It reports
what the vendor asks, not what a reader can obtain: the Chinese figure is a promotion code on
a 256 MiB NAT instance whose renewal price belongs to a different Singapore instance, and the
Korean figure is quoted only on a 12-month term. Section 3 counts the doors instead.

The Chinese lane is the largest and the least usable. It is also the only lane where a
four-core, four-GiB machine is sold by the year rather than the month. The Russian trials run
from 3 days to 7, and the Japanese from 10 days to 30. The Korean lane is priced per day by one
provider and per month by every other, and its two free offers are credits rather than
machines. The Japanese lane is the only one where nothing fails on identity, and three of its
rows carry a three-month minimum instead.

## 2. The four markets

Each table is sorted by what a reader can start today: free lanes first, then trials, then the
cheapest paid machine, then the GPU ladder, then the rows the door closes on, then the dead.
Every price stays in the vendor's own currency, unconverted, and every figure was read on
2026-10-22 unless the row says otherwise; five records were read on 2026-10-24 and their rows
carry that date. The URL behind each row is in its record under `dossier/compute/`.

⚠ **`unverified` in an identity cell is a measurement, not a shorthand.** It means the record's
`identity_cost.detail` is the string "as stated by the provider's signup page", which asserts
nothing, and no evidence row in that record states the field either. 30 of the 55 records are in
that state: 23 `card`, 3 `email`, 2 `country-phone`, 1 `any-phone` and 1 `national-id`.
`python scripts/dossier/card-hold.py dossier/compute --list-missing` (run 2026-10-24, exit 0) reports the topic-wide version of the same defect: of 1,255
compute records, 214 require a card, **39 state how much is held**, and 266 name a gate without
asserting what it costs. The 266 are the ones whose records carry no identity evidence to
promote.

⚠ **`none named` in the counterparty cell is the finding that matters here.** Only four of
the 55 records name any legal person at all, and none of the four was checked against a company
register. The popular hosts gate hard, so a niche host is the alternative;
the cost is that on 51 of these rows there is nobody to serve a claim against.

### 2.1 Chinese-language forums, 21 records

| Provider | What it sells | Price, renewal and stock | Identity gate | What fails first | Counterparty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `euserv-vs2-free` EUserv VS2-free | 1 core at 1 GHz, 1 GiB, 10 GB, IPv6 only, 10 GB FTP backup | free, 1 TB a month then 1 Mbit/s; a user reports a EUR 2.00 one-time extension fee, which no vendor page confirms | email; the product page states no phone or real-name step | manual monthly renewal, and no IPv4 | none named | qualifies-with-caveat |
| `sanfengyun` Sanfengyun | 1 core, 1 GiB, 5 Mbit/s BGP, dedicated IPv4 | free; first activation 24 hours, each approved extension adds 5 days, reopening an expired server costs CNY 2 | mobile number plus real-name at CNY 0.3; the record files the kind as `national-id`, because the real-name check is what closes the door | the one-day clock and the review gate | none named | fails-identity |
| `hostslate` HostSlate | NAT VPS, one in Japan and one in the United States | free; renewed by a coupon announced in a Telegram group, so the term lasts only as long as the next coupon; no price is published | email or GitHub; the terms reserve a KYC demand on a risk trigger | the coupon, and no price is published | a UK brand by its own terms; no company number and no register check | qualifies-with-caveat |
| `vip-cloud` VIP Cloud | 2 vCPU, 2 GiB, 20 GB in Los Angeles | free for 3 days, then renewal by referral, claimed up to ten years; paid CNY 199/year for 8 vCPU, 8 GiB, 50 GB SSD, 20 Mbps | email; a further check reported after a failed payment | the 3-day clock and the referral loop | none named | qualifies-with-caveat |
| `rainyun` Rainyun | cloud server and shared host | CNY 1 for one day per product; CNY 15/month cloud-server floor and CNY 8/month shared-host floor | real-name inferred from mainland licences; the signup page was not read | one day per product, one purchase per account, three refunds per account | none named; the vendor states it holds its own mainland licences | trial-only |
| `damodel` DAMODEL | RTX 4090 24 GB | CNY 20 credit; USD 0.267 per card-hour on demand, USD 0.18 preemptible, USD 0.224 monthly | not established; the signup form was not read | the credit runs out after about 11 hours of a 4090 | none named | trial-only |
| `lanmao-cloud` Lanmao Cloud | a Hong Kong NAT instance, and a separate Singapore instance | CNY 2.62/month on a 75-percent-off code with 2 TB; the CNY 12 renewal belongs to the Singapore 1 vCPU / 256 MiB / 500 GB shape, not to the CNY 2.62 one | not established | a shared IPv4, a reseller coupon, and free machines resold at CNY 180 to CNY 600 | none named; described as a recent entrant | qualifies-with-caveat |
| `dedione` DediOne | 2 vCPU, 1 GiB, 20 GB, 1 TB | USD 3.99/month; the store shows monthly terms only | not established; the order flow was not entered | 1 TB a month at 1 Gbit/s | none named | paid-only |
| `bandwagonhost` BandwagonHost | 2 vCPU, 1 GiB, 20 GB, 1 TB | USD 49.99/year | not established; the front page states no verification requirement | 1 TB a month on an annual term | US-registered per the record, with no company name or number | paid-only |
| `lighthouse-99` Lighthouse 99 | 2 vCPU, 2 GiB, 30 Mbit/s, 1,000 GB | CNY 99/year, renewable once at the same price, so CNY 198 covers two years; the promotion recurs across v2ex threads spanning several months | mainland real-name verified account; the international storefront is a separate product this price does not cover | 1 TB a month, and one renewal only | Tencent Cloud, mainland storefront; no entity named | paid-only |
| `chamaoyun` Chamaoyun | 4 vCPU, 4 GiB, 50 GB, 50 Mbit/s, 1 TB | CNY 99/year | age 18 to 25 and a domain with a mainland ICP filing; overseas access blocked | 1 TB a month, then 10 Mbit/s | Chengdu Aite Shiji Network Technology, per a reseller profile; trading since 2020, no register check | fails-identity |
| `autodl` AutoDL | RTX 4090 24 GB | CNY 1.88/hour, with a 5 percent member discount | real-name, with an overseas-passport route stated; the registration form is a phone plus SMS and its country selector offers only +86, +852, +853 and +886, so the passport route does not settle the phone gate | the phone country, then the balance at about 53 hours per CNY 100 | none named | paid-only |
| `compshare` Compshare | RTX 4090 24 GB with 14 vCPU and 32 GiB | CNY 1.92/hour, CNY 1,154.64/month, CNY 1.31/hour preemptible; the monthly rate beats on-demand only above about 601 hours | real-name, and the record does not say whether a non-Chinese passport passes | the preemptible lane is reclaimable | none named | paid-only |
| `ai-galaxy` AI Galaxy | RTX 4090 24 GB | CNY 1.65/hour | not established | a shared pool, priced higher for dedicated use | none named | paid-only |
| `gpushare` gpushare | RTX 3090 at CNY 0.98 and RTX 4090 at CNY 2.00, plus a 4090D at CNY 1.10 and a 48 GB 4090 at CNY 3.45 | per card-hour | email, with a price directory claiming no real-name check; no vendor page confirms it | the funding tier caps cards per instance | none named | paid-only |
| `ppio-gpu` PPIO | RTX 4090 24 GB in a 62 GiB container | CNY 2.31 on demand, CNY 1.16 preemptible | not established | the spot lane | none named | paid-only |
| `xiangongyun` Xiangongyun | RTX 4090D 48 GB | USD 0.238 on demand, USD 0.194 on a monthly rate | not established | stock of one card in one region | none named | paid-only |
| `xkey` XKey | RTX 3090 24 GB | USD 0.128 per card-hour on annual billing in a four-card instance, USD 0.223 on demand | not established | the annual commitment | sells through silengine.com; no entity named | paid-only |
| `student-voucher` student voucher | CNY 300 voucher and 13 instance shapes | CNY 300, no threshold; the student status behind it lapses every 30 days | mainland student register plus Alipay real-name | enrolment in a mainland institution | Alibaba Cloud; no entity named | fails-identity |
| `cloudcone` CloudCone | Los Angeles KVM, SSD VPS 1 | USD 28/year billed annually for 2 vCPU, 1 GiB, 30 GB and 4 TB; SSD VPS 2 at USD 46/year and SSD VPS 3 at USD 69/year | not read | disk recovery after a hypervisor compromise | CloudCone, LLC, US, per the record's own field; not checked against a state register | qualifies-with-caveat |
| `clawcloud` ClawCloud | VPS and VDS | not applicable, closed | moot, the product cannot be bought | the closure date | none named | dead |

### 2.2 Russian-language forums, 15 records

| Provider | What it sells | Price, renewal and stock | Identity gate | What fails first | Counterparty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `adminvps` AdminVPS | 1 core at 3.6 GHz, 1 GiB, 15 GB, 100 Mbit/s, 1 TB | 7 days free; RUB 250/month; a first paid month free with the code ISP30DAY; the trial server is deleted 24 hours after it ends | unverified: the record's detail asserts nothing and no evidence row states the field. A third-party table claims the trial is legal-entities-only, which the provider page contradicts | 1 TB a month, and the trial disables cron and all mail | none named | trial-only |
| `cloudvps` CloudVPS | 1 core at 3.6 GHz, 1 GiB, 15 GB NVMe, 200 Mbit/s, 5 TB | 7 days free; BYN 19.99/month, BYN 14.99 with a 25 percent discount applied on the page; the record does not say whether 14.99 is a first-term or a standing price | card, and the vendor page states international and Russian cards in any currency, which is one of the two evidenced foreign-card rails on this page | 5 TB a month against a daily 500 GB to 1 TB | none named; the record infers one billing platform behind this brand and AdminVPS from identical copy, undocumented | trial-only |
| `ihc` IHC | 1 CPU, 1 GiB, 20 GB SSD | 3 days free after a RUB 100 top-up that stays withdrawable; RUB 380/month, or RUB 3,800/year presented as RUB 317/month | unverified: the record's detail asserts nothing and no evidence row states the field | the 3-day clock | none named | trial-only |
| `ruweb` RuWeb | any tariff in the catalogue | 6 days free after a top-up; from RUB 169/month; the deposit is RUB 300 in the trial page body, RUB 200 twice in that page's FAQ, and RUB 300 for a VPS against RUB 100 for shared hosting on the promotions page, so three figures across two pages | unverified: the record's detail asserts nothing and no evidence row states the field | three deposit figures, and ports 25 and 465 closed | none named | trial-only |
| `serverspace` Serverspace | up to 8 vCPU, 16 GiB, 200 GB | 3 days free for an individual, 5 for a legal entity, by ticket; from RUB 430/month; billing every 10 minutes | unverified: the record's detail asserts nothing. Its evidence rows state testing without card binding, which supports no card, not an email-only door | a support decision that can refuse | none named | trial-only |
| `spaceweb` SpaceWeb | any VPS tariff, and S3 to 500 GB | 3 days free, campaign to 2027-01-31; from RUB 0.30/hour, about RUB 219/month at 730 hours; files kept 7 days after the trial | a phone confirmation; the record files `any-phone`, and the page says only "confirm a phone number", so a non-Russian number is unverified | 10 Mbit/s during the trial | none named | trial-only |
| `webhost1` WebHOST1 | 1 core at 2.8 GHz, 2 GiB, 20 GB, 100 Mbit/s | RUB 336/month, or RUB 285.60/month on the annual term, which is RUB 4,032 against RUB 3,427.20 for 12 months | card, with foreign cards through Robokassa at a RUB 1,000 minimum and a named refusal list; the second evidenced foreign-card rail on this page | 100 Mbit/s tops out near 1.08 TB a day | none named | trial-only |
| `cloud-ru-evolution` Cloud.ru Evolution | CPU time only | RUB 4,000 grant valid 60 days, on a card never previously attached to any Cloud.ru account | card, and the rule that decides the verdict is elsewhere: the campaign approved 2026-06-30 admits only persons registered in the Russian Federation, which is recorded in the evidence row and in `notes`, not in the identity field | the 60-day expiry, the GPU exclusion, and the registration country | none named | fails-identity |
| `hostkey` HOSTKEY | 1 vCPU, 1 GiB, 40 GB, 1 Gbit/s, 3 TB | RUB 490/month, hourly below that | card; the record names Mir, Russian transfers and electronic systems only, so a foreign card is unverified | 3 TB a month, about 100 GB a day | none named | paid-only |
| `aeza` Aeza | 2 GiB RAM, 30 GB NVMe, 25 Gbit/s, traffic printed as unlimited | EUR 5.93/month or EUR 0.04/hour; the hourly rate is about five times the monthly at 730 hours; a EUR 1.99 Stockholm promo plan is described in the wiki but is not on the price page and may be sold out | email plus a robot check; crypto top-up documented in the vendor wiki; the card rails are unread because the order console is behind a sign-in | continuity: Aeza Group has been on the US OFAC SDN list since 2025-07-01, and the storefront would not answer through the broker on 2026-10-24, so whether it is purchasable today is unverified | two legal entities, one in Hong Kong behind aeza.net and one in Russia behind aeza.ru, as separate contracts; the record also calls the UK company 15109642 a shell | paid-only |
| `vdsina` VDSina | 8 cores, 8 GiB, 150 GB NVMe, an L4 slice with 2 GB, 32 TB | USD 60/month or USD 2.00/day, so the month is exactly 30 days of the daily rate | unverified: the record's detail asserts nothing and no evidence row states the field | 32 TB a month | none named | paid-only |
| `firstvds` FirstVDS | L40S 4 GiB vGPU, 2 cores, 4 GiB RAM, 50 GB | RUB 299/day or RUB 8,970/month, so the month is exactly 30 days | unverified: the record's detail asserts nothing. The promotions page titles the CPU trial as legal-entities-only while the blog page does not | the CPU trial needs a sales decision, and the GPU lane has none | none named | trial-only |
| `hosting-vds-com` Hosting-VDS.com | a VPS | not published in the record | a Russian mobile number, demanded after payment clears | verification, after the money moved | none named | fails-identity |
| `h3llo-cloud-year-free-package` h3llo.cloud year-free package | 2 x 2 vCPU / 4 GiB, a managed database, 100 GB object storage | RUB 5,000 top-up for 12 months; joining closed 2026-03-08, and the landing page still advertises the package while the rules page carries the deadline | a Russian phone; the vendor attributes the requirement to the Ministry of Digital Development | the campaign closed on 2026-03-08 | none named; the record notes two live domains with different prices and different egress terms | dead |
| `4vps-su` 4vps.su | a Japanese VDS | paid, never delivered | unverified: the record's detail asserts nothing, and the one evidence row is a complaint about delivery, not a signup page | delivery | none named | dead |

### 2.3 Korean-language forums, 11 records

| Provider | What it sells | Price, renewal and stock | Identity gate | What fails first | Counterparty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `iwinv` iwinv | 1 vCPU, 1 GiB, 25 GB NVMe, 20 GB a day | KRW 210/day or KRW 5,600/month, excluding VAT, so KRW 6,160 with the 10 percent Korean consumer rate | Korean nationality and a Korean mobile phone, both quoted from the vendor's help pages; card registration needs a Korean public certificate | 600 GB a month, and the nationality gate | the consumer brand of SmileServ, per the record; no entity number | fails-identity |
| `xdn-idc` XDN IDC | 1 vCPU, 1 GiB, 25 GB HDD, 600 GB | KRW 5,040/month on a 12-month commitment; a 24-month term discounts it 5 percent and 36 months 10 percent; overage KRW 70 per GB to 1,000 GB then KRW 60 | unverified: the record's detail asserts nothing and no evidence row states the field | 600 GB a month and the term | a one-site reseller in Seoul; no entity named | paid-only |
| `cafe24-virtual-server` Cafe24 virtual server | 1 GiB, 30 GB SSD, 300 GB | KRW 9,000/month including VAT, plus a KRW 22,000 setup fee; the entry price rose from KRW 7,000 to KRW 9,000, so a one-month test costs more in setup than in service | unverified: the record's detail asserts nothing and no evidence row states the field | 300 GB a month, then KRW 165 per GB | none named | paid-only |
| `gabia-cloud-gen1` Gabia Cloud Gen1 | 0.5 GiB Micro | KRW 45/hour on the service page, against the price-change notice's KRW 5,000/month or KRW 7/hour for the same Micro shape, so the two vendor pages disagree | card authentication through a Korean public certificate, which is issued against a Korean resident registration number | card authentication needs the certificate | none named | fails-identity |
| `kinx-ixcloud` KINX IXcloud | 1 vCPU, 1 GiB, 50 GB | KRW 20,000/month or KRW 30/hour; the SSD variant KRW 23,500/month or KRW 35/hour | unverified for the account door. The FAQ evidences post-paid billing to a registered credit card or account transfer, which is not the same fact | the hourly price | none named; an internet exchange operator selling its own cloud | paid-only |
| `egg-hosting` Egg Hosting | 2 vCPU, 4 GiB, 50 GB NVMe | KRW 24,000/month excluding VAT; overage tiers KRW 49 down to KRW 29 per GB | unverified: the record's detail asserts nothing and no evidence row states the field | 300 GB a month | none named | paid-only |
| `cloudv` CLOUDV | 1 core, 2 GiB, 100 GB SSD, 1,200 GB | KRW 31,500/month excluding VAT | unverified: the record's detail asserts nothing and no evidence row states the field | 1,200 GB, then KRW 70 per GB with no throttle | the cloud brand of SmileServ, the same company as iwinv, per the record | paid-only |
| `samsung-cloud-platform` Samsung Cloud Platform | any product except GPU and bare metal, which need a console enquiry first | KRW 300,000 credit, valid 3 months, one per account | card plus vendor approval | manual approval | Samsung SDS; no entity number | trial-only |
| `naver-cloud-platform` NAVER Cloud Platform | any service except free-tier and marketplace products | KRW 100,000 credit, 3 months. A second live page on micro.ncloud.com advertises up to KRW 300,000 and neither page reconciles the gap | payment method plus mobile real-name, and Korea residency for the free Micro server; the record files the kind as `card`, which names the second gate rather than the first | residency | NAVER; no entity number | fails-identity |
| `aircloud` AirCloud | RTX 4090 24 GiB, 8 vCPU, 58 GiB | USD 0.51/hour, against a KRW 10,000 minimum top-up plus 10 percent VAT, so the practical entry cost is KRW 11,000 rather than one hour | unverified: the record's detail asserts nothing and no evidence row states the field | the balance is the quota, and running out terminates the workload | AIEEV; no entity named | paid-only |
| `gabia-vps-hosting` Gabia VPS hosting | 2 vCPU, 512 MiB, 12.5 GB, 300 GB | KRW 10,000/month, with no minimum term and no cancellation penalty; the ladder is still published, from KRW 10,000 a month | unverified: the record's detail asserts nothing, and the product cannot be bought anyway | no new application since 2024-05-02 | none named | dead |

### 2.4 Japanese-language forums, 8 records

| Provider | What it sells | Price, renewal and stock | Identity gate | What fails first | Counterparty | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `sakura-vps-2-week` Sakura VPS 2-week | every plan, up to 32 GiB and 8 cores | 2 weeks free with card payment, then automatic conversion to paid at the list price; a three-month minimum term follows the conversion; 512 MiB at JPY 590/month equivalent, 1 GiB at JPY 807, up to 32 GiB at JPY 24,200 | card, which the vendor states as the condition of the trial; no other gate is stated | automatic conversion and a 3-month minimum, and a 10 Mbit/s cap with port 25 closed during the trial | none named | trial-only |
| `ablenet-vps` ABLENET VPS | 0.5 GiB, 1 vCPU, 30 GB SSD | 10 days free with no automatic conversion; JPY 554/month including tax, plus a JPY 1,130 setup fee on L0 only; L0 cannot be reached by downgrading a larger plan | unverified: the record's detail asserts nothing. The vendor states a trial on every Linux plan with no minimum period, and the card is inferred from the billing model | the 10-day clock | none named | trial-only |
| `webarena-indigo` WebARENA Indigo | 768 MiB, 1 vCPU, 20 GB, IPv6 only | JPY 0.48/hour capped at JPY 290/month, JPY 319 with tax; the 1 GiB shape with IPv4 is JPY 0.64/hour capped at JPY 409, JPY 449 with tax; no setup fee and no minimum period; billed from creation to deletion, including while stopped | card, after email verification and an SMS or voice call. A separate eKYC check accepts Japanese documents only, and which signup paths require it is not established | no IPv4 on the entry shape | none named | qualifies |
| `kagoya-cloud-vps` KAGOYA CLOUD VPS | 1 GiB, 1 vCPU, 100 GB NVMe | JPY 20/day capped at JPY 550/month; annual prepayment JPY 6,072, which the vendor presents as JPY 506/month | card; the payment page names credit card or account transfer and refuses debit cards | no free lane at all | none named | paid-only |
| `coreserver-v2` CORESERVER V2 | 6 GiB allocation, 300 percent CPU, 500 GB NVMe | JPY 830/month monthly, JPY 610 on a 12-month term, JPY 430 on 36 months, plus a JPY 1,650 setup fee; the 30-day free start is stated on the vendor front page but not in the price table the record read | unverified: the record's detail asserts nothing and no evidence row states the field | the load limit bans computational work, and 200 processes and 30 concurrent connections | none named | qualifies-with-caveat |
| `onamae-com-vps` Onamae.com VPS | 1 GiB, 2 vCPU, 100 GB SSD | JPY 985/month including tax, JPY 873 effective on 12 months; no setup fee, and a three-month minimum makes the entry cost JPY 2,955 | unverified: the record's detail asserts nothing and no evidence row states the field | the 3-month minimum | none named | paid-only |
| `shin-vps` Shin VPS | 1 GiB, 1 core, 30 GB NVMe | JPY 750/month, JPY 671 on 12 months, JPY 451 on 36 months, no setup fee; raised from JPY 540 on 2026-09-01, about 39 percent | unverified: the record's detail asserts nothing and no evidence row states the field | the 3-month minimum, and the rise | none named | paid-only |
| `xserver-vps` XServer VPS | 2 GiB, 2 vCPU, 30 GB, and a 4 GiB shape | the two free shapes at JPY 0 are still listed and the signup button reads suspended; the paid product continues from JPY 1,265/month for 2 GiB | card, and the free-plan page states card registration is required; the signup path was not read | applications suspended for both free plans | none named | dead |

## 3. The identity finding, counted once

Eight of the 55 records carry the verdict `fails-identity`. `iwinv` carries it on 2026-10-24, with
the vendor's own help pages quoted. The document each one
asks for is the useful part, because it says what a reader outside these markets would have to
produce.

| record | document the record names | quoted from the record |
| --- | --- | --- |
| `chamaoyun` | PRC age band and a mainland ICP filing | "age 18 to 25", "a domain with a mainland ICP filing is required, and IP plus port access is not supported", and "overseas access blocked" |
| `sanfengyun` | PRC real-name certification | "Phone registration plus real-name certification at CNY 0.3" |
| `student-voucher` | a mainland student register plus Alipay real-name | "requires full-time enrolment at a mainland Chinese higher-education institution, checked against the national student register" |
| `gabia-cloud-gen1` | a Korean public certificate | "card authentication through a Korean public certificate, which is issued against a Korean resident registration number" |
| `naver-cloud-platform` | a Korean mobile real-name check and residency | "the account is real-name verified by mobile phone, and the perpetually free Micro Server is limited to residents of Korea" |
| `iwinv` | Korean nationality and a Korean mobile phone | `대한민국 국적의 만 14세 이상이며 핸드폰 인증이 가능한 사용자라면 누구나` (anyone of Korean nationality aged 14 or over who can pass mobile-phone verification), and `정상적인 카드 등록을 위해 공동인증서가 필요합니다` (a Korean public certificate is needed to register a card) |
| `hosting-vds-com` | a Russian mobile number | "a Russian mobile number only, a condition not stated during signup" |
| `cloud-ru-evolution` | a Russian card and Russian registration | the record names the card, and its evidence row limits the campaign to persons registered in the Russian Federation |

Three of the eight want a Chinese document, three a Korean one, two a Russian one. That split is
the finding: in each market the cheapest machine is gated by the local identity rail, and the
card is the second gate rather than the first. Two records evidence a rail a foreign reader can
use, and both are Russian: foreign cards through Robokassa at `webhost1`, and international
cards in any currency at `cloudvps`. `serverspace` states bitcoin among its payment methods in
its offer sentence, and the evidence rows for that record do not carry it. `aeza`'s current
record no longer names Russian cards or SBP in its own voice: it records email plus a robot
check, crypto documented in the vendor wiki, and says the card rails were not read because the
order console sits behind a sign-in. The Russian-card and SBP claim survives only in that
record's superseded block, sourced to a third-party catalogue. None of the eight shows a
foreign passport reaching a Chinese or Korean offer.

The count by identity kind, which is the field the dossier stores:

| kind | rows | of which fails-identity | what the remaining rows mean |
| --- | --- | --- | --- |
| `card` | 25 | 2 | a card is stated, but not tested with a non-domestic one, and 23 of the 25 assert nothing beyond the word |
| `national-id` | 8 | 4 | the other four are `autodl`, `compshare`, `lighthouse-99` and `rainyun` |
| `email` | 8 | 0 | the open rows of the page, three of which assert nothing |
| `institution` | 11 | 1 | nine are placeholders for "not established", see below |
| `country-phone` | 2 | 1 | the second is `h3llo`, which is dead |
| `any-phone` | 1 | 0 | `spaceweb`, which accepts confirmation of any number |

The counts are the sum of the columns: 55 rows, 8 of them `fails-identity`. `sanfengyun` is counted under `national-id` because its own offer sentence states a mobile number and a CNY 0.3 real-name check.

⚠ **`institution` is doing two jobs in this slice.** Nine rows carry
`identity_cost.kind` set to `institution` while their `detail` says the door was not read:
`ai-galaxy`, `damodel`, `ppio-gpu`, `xiangongyun`, `xkey`, `lanmao-cloud`, `bandwagonhost`,
`dedione` and `cloudcone`. They are not all Chinese: `bandwagonhost` and `cloudcone` are
US-registered. Only `student-voucher` is institution-gated in the sense the vocabulary means, and
`clawcloud` is moot. A count of `institution` rows in this topic reads as eleven gated providers
when one is.

⚠ **And `email` is doing the same job in the same slice.** Of the eight `email` rows, three
carry the vacuous detail string and nothing else: `adminvps`, `serverspace` and `firstvds`, all
in the Russian lane. The fourth that did, `sanfengyun`, was worse than unverified, because its
own offer sentence states a mobile number and a CNY 0.3 real-name check while its field said
`email`. That contradiction is a record defect.

The four `national-id` rows that are not `fails-identity` are the interesting ones. `autodl`
states three individual routes and names an overseas passport among them, and its own
registration evidence says the form is a phone plus SMS with a country selector offering only
+86, +852, +853 and +886, so the passport route does not reach the phone gate. `compshare`
states real-name and does not say whether a non-Chinese passport passes. `lighthouse-99` needs a
mainland account for the CNY 99 price. `rainyun` holds mainland licences and states no
document. The gate is real in all four. None of the four records the gate as a verdict.

One placement fact is worth its own line. `hosting-vds-com` asks for the Russian number after
the payment clears, not at signup, and the buyer in the report received no server and no
refund. The gate costs the transaction rather than the registration, which is what makes
identity the binding constraint here and capacity irrelevant.

## 4. The hosts that vanished

Four records carry `verdict: dead`, and a fifth row belongs in the table because its free
product is dead while its record stays `paid-only`: `xserver-vps`.

| record | last date the record supports | what the record shows | what remains |
| --- | --- | --- | --- |
| `clawcloud` | 2026-06-30 | notice: new registrations, purchases, renewals and upgrades stopped on 2026-06-01; 2026-06-01 to 2026-06-30 was a migration and refund window; at 24:00 on 2026-06-30 every instance was force-stopped and the data destroyed | the domain returned HTTP 503 on 2026-10-22, and the separate free-container host run.claw.cloud returned a broker-side HTTP 530 on 2026-10-24 |
| `gabia-vps-hosting` | 2024-05-02 | new applications restricted from 14:00 that day, with two named replacement products | the price ladder is still published, from KRW 10,000 a month |
| `h3llo-cloud-year-free-package` | 2026-03-08 | joining was open until that date inclusive, and the rules page now carries a banner that the campaign finished | a 30-day trial credit replaced it for new clients |
| `4vps-su` | not dated in the record | a paid Japanese VDS never started, the ticket went unanswered, the buyer was removed from the chat, and a refund request went unanswered for more than 15 days | the complaint page was read on 2026-10-22 |
| `xserver-vps` (verdict `paid-only`) | 2026-07-10 | the notice of that date suspends new applications for both free plans; a second notice cuts the free period to 24 hours for both shapes from 2026-07-22 17:00, from 96 hours on the 2 GiB and 48 on the 4 GiB | the signup button read as suspended on 2026-10-22, and the paid product continues from JPY 1,265 a month |

The pattern is the same in three of the five: the free or cheap product is withdrawn while the
paid product at the same address continues, so a search result still resolves and a reader
concludes the offer exists. `xserver-vps` is the clean case: the free plan page still lists two
shapes at JPY 0, and the button beside them is closed. The five split as one shutdown, one
campaign that ended, two products withdrawn, and one delivery failure: `4vps-su` sold, took the
money, delivered nothing, and the record exists so the name is not tried again.

`cloudcone` is not in the table because its verdict is `qualifies-with-caveat`, but it belongs
in the reliability fact this section is about. Several Los Angeles nodes were compromised
through a Virtualizor vulnerability, the boot sectors of guest disks were overwritten, and the
vendor states that the data cannot be recovered. A machine can lose its disk with no closure
at all, and a snapshot kept on the same provider is not a backup.

## 5. What these markets sell cheaper than anywhere else

Four shapes recur, and each one is a different mechanism rather than a lower price for the
same thing.

**The annual prepay, in China.** `lighthouse-99` sells 2 vCPU and 2 GiB for CNY 99 a year and
`chamaoyun` sells 4 vCPU and 4 GiB for the same CNY 99 a year. `vip-cloud` sells 8 vCPU and
8 GiB for CNY 199 a year. 99 / 12 = CNY 8.25 a month for the first two, which is below the
CNY 15 monthly floor `rainyun` advertises. Two of the three are gated: `lighthouse-99` on a
mainland account, `chamaoyun` on an age band and an ICP filing. The renewal limit is the second
gate, because `lighthouse-99` allows one renewal at the same price and the records show no
second one.

**The per-card-hour GPU, in China.** `autodl` prices an RTX 4090 24 GB at CNY 1.88 an hour,
`gpushare` prices an RTX 3090 at CNY 0.98, and `compshare` prices a 4090 with 14 vCPU at
CNY 1.92 with a CNY 1.31 preemptible lane. `xkey` is the lowest 24 GB rate in the lane at
USD 0.128 per card-hour, on annual billing, in a four-card instance; the same card is
USD 0.223 on demand, which is 74 percent more. AutoDL at CNY 1.88 for 730 hours is
CNY 1,372.40 a month, and the record's own arithmetic puts a CNY 100 deposit at about 53
hours.

**The free week, in Russia.** The trials run 3 days at `ihc`, `serverspace` and `spaceweb`,
6 at `ruweb`, 7 at `adminvps` and `cloudvps`. The largest shape is `serverspace` at 8 vCPU,
16 GiB and 200 GB of disk for 3 days, and it is granted by a person after a written purpose.
`firstvds` has no free GPU at all and its CPU trial is also a sales decision, which makes the
Russian free lane a week of CPU and nothing else.

**The daily meter with a monthly cap, in Japan and Korea.** `kagoya-cloud-vps` charges
JPY 20 a day and stops charging at JPY 550 a month for a 1 GiB box. `webarena-indigo` charges
JPY 0.48 an hour and stops at JPY 290 a month for 768 MiB. `iwinv` charges KRW 210 a day for
1 vCPU and 1 GiB, with no cap. A one-day job therefore costs JPY 20, JPY 11.52 or KRW 210
depending on the provider, and a one-month job costs the cap at the first two. At `iwinv` the
daily meter is the more expensive one: 30 x KRW 210 = KRW 6,300 against the KRW 5,600 monthly
plan, so the month is the cheaper purchase and there is no cap to reach.

⚠ **A promotion price is not a renewal price, and a low-end plan sells out.** `lanmao-cloud`
sells its Hong Kong NAT instance at CNY 2.62 a month on a 75-percent-off code, and the CNY 12
renewal belongs to a different, Singapore instance. `shin-vps`
raised its 1 GiB plan from JPY 540 to JPY 750 on 2026-09-01, about 39 percent.
`cafe24-virtual-server` raised its entry price from KRW 7,000 to KRW 9,000. `gabia-cloud-gen1`'s
two vendor pages disagree on its own Micro shape, at KRW 45 an hour against KRW 5,000 a month.
`xserver-vps` still lists two free shapes and will not sell either. `aeza`'s EUR 1.99 promo is
described in its wiki, is absent from its price page, and may be sold out. A price read once is
a price for one term, and a shape read once may not be orderable at all.

## 6. What could not be read

Eleven records are `reported` rather than `documented`. Seven rest on a forum or a thread for
their offer or their incident: `4vps-su` on a vc.ru complaint, `chamaoyun` on a hostloc post,
`cloudcone` on three nodeseek threads, `hosting-vds-com` on a LowEndTalk scam alert,
`lanmao-cloud` on four nodeseek posts, `lighthouse-99` on three v2ex threads, and `vip-cloud`
on two nodeseek threads and one nodeloc thread beside its own page. The other four are prices
where no vendor page came back usable: `ai-galaxy`, `gpushare`, `xiangongyun` and `xkey`. The
routes that failed fall into four groups, and the group matters because each one has a
different repair.

**Price ladders rendered by script.** `ai-galaxy` returned 274 words of navigation on both of
the pages that carry its prices, so the figures come from the search index's rendering of the
same URLs. `xiangongyun` renders its table client-side and only the aggregator figure was read;
two third-party tables disagree with it at CNY 1.78 and CNY 2.37 an hour. `gpushare` renders
its per-card table and its rates come from two price directories. `lighthouse-99` prices its
promotion on an activity page whose cards are script-rendered, so the CNY 99 comes from v2ex
threads. `rainyun` returned 422 with no content on its store page. `compshare` lost the GPU
model headers in extraction, so the card behind the CNY 1.92 row was taken from the search
snippet of the same URL. `samsung-cloud-platform` returned a shell page with no content from
the free-trial page.

**Responses that were not a usable 200.** `clawcloud` returned 503 from the origin.
`vip-cloud` returned 403 upstream while still yielding a body, so the text is real and the read
is not clean. `aeza` loops redirects on its Russian home page with 508 and serves no price rows
on its Russian catalogue, so only the English catalogue was read. `euserv-vs2-free` 404s on its
English slug and was read on the German page. `gabia-vps-hosting` 404s on its product URL and
was read through the customer manual. `ppio-gpu` 404s on its first product URL.
`hostslate` returned 200 with 36 words, and a 5-page crawl of 21,664 bytes reached 5 of 21
pages, recovering the signup form and the terms but no price table.

**Pages that arrived only as a search snippet.** `hostkey`, `webhost1`, `ruweb`, `vdsina`,
`firstvds`, `serverspace`, `spaceweb`, `adminvps`, `kagoya-cloud-vps`, `egg-hosting` and
`kinx-ixcloud` were read this way for at least one of their price figures, so that figure is
quoted from a rendering of the page and not from the page's own bytes.

**Price directories as the only source.** Six records lean on an aggregator for at least one
figure, four of them `reported`: `ai-galaxy`, `xiangongyun` and `xkey` on suanli.ai alone,
`gpushare` on gpu114.com and dxnt.com, and `damodel` and `ppio-gpu` on suanli.ai beside their
own vendor pages. An aggregator that polls daily is a reasonable witness for a price and a
poor one for an identity gate. `gpushare` is the case that matters: the claim that it runs no
real-name check is the difference between a usable GPU host and one more `fails-identity` row,
and it comes from a directory rather than from the vendor.

No record documents a login wall or a challenge page behind these forums.
The dominant failure is a 200 with a script-rendered body rather than a refusal. Fourteen vendor
pages yielded no readable price: seven with a table rendered in script, and seven whose
response was not a usable page.

Two incident dates are missing as well. The nodeseek threads behind `clawcloud`, `cloudcone`
and `vip-cloud` came back without a post date in the extracted snippet, so those dates are not
stated rather than guessed.

## 7. Where the records disagree with themselves

These are defects a reader should know about before acting on a row, and each one is a line in
the record rather than a doubt about the record.

`webarena-indigo` carries a monthly cap and a monthly floor. The offer field says JPY 290 a month capped and JPY 319 with tax for
the 768 MB shape; the limit entry says the monthly floor is JPY 50 (JPY 55 with tax), which is
the minimum a month with any usage at all costs. The two are compatible: at JPY 0.48 an hour
the floor binds below about 104 hours and the cap above about 604. No contradiction, and no
change to the JPY 290 figure this page uses.

`cloud-ru-evolution` carries `fails-identity` with `identity_cost.kind` set to `card` and a
detail that reads "as stated by the provider's signup page". The rule that supports the verdict,
that the campaign admits only persons registered in the Russian Federation, is in the evidence
row and not in the identity field.

`spaceweb` states 3 days in the body of its page and "up to 12 months" in its own meta
description. `hostkey` publishes three answers on the trial: none, none, and three days.
`ruweb` publishes three deposit figures across two pages: RUB 300 in the trial page body, RUB
200 twice in that page's FAQ, and RUB 100 for shared hosting on the promotions page.

`h3llo.cloud` has two live domains with different prices and different egress terms, and the
trial terms exist on only one of them. `aeza` runs two legal entities, one in Hong Kong and one
in Russia, and they are separate contracts; its record also calls the UK company 15109642 a
shell, and carries an OFAC SDN listing from 2025-07-01 as a continuity fact.

`ai-galaxy` publishes the same four prices on its student page and its individual-developer
page, so the student label is a label and not a discount. `gpushare` prices 4090 stock at
CNY 1.10, CNY 2.00 and CNY 3.45 across three regions and two card variants.

`gabia-cloud-gen1` disagrees with itself on its own entry shape: the service page prices the
Micro at KRW 45 an hour and the price-change notice prices it at KRW 5,000 a month or KRW 7 an
hour. Those are not compatible, and neither was reconciled.

`naver-cloud-platform` has two live pages on two credit sizes, KRW 100,000 on the main credit
page and up to KRW 300,000 on micro.ncloud.com, and neither reconciles the gap.

`lanmao-cloud` states a CNY 2.62 Hong Kong NAT instance and a CNY 12 Singapore renewal for a
different shape in the same offer field. This page splits them, because the record does not say
the 2.62 instance renews at 12.

## 8. What would change the answer

Nine probes would close the largest unknown on this page. The nine rows whose door is recorded
as not established are the unknown, and one registration attempt each would turn them into
either a price or a refusal: `ai-galaxy`, `damodel`, `ppio-gpu`, `xiangongyun`, `xkey`,
`lanmao-cloud`, `bandwagonhost`, `dedione` and `cloudcone`.

Four single pages would move four more. The form at `autodl.com/register` has been read, and it
settles the question against reachability rather than leaving it open: the form is a phone
number plus an SMS code, and the country selector offers only +86, +852, +853 and +886, so the
overseas-passport real-name route does not get past the phone field. What is left is one
attempt with a Hong Kong or Macao number, which the selector does offer. The international
Lighthouse price at tencentcloud.com decides whether the CNY 99 shape exists for a card outside
China. The order page at `gpushare` decides the real-name claim that a directory makes for it.
The Gabia price-change notice against the service page decides which of KRW 45 an hour and
KRW 5,000 a month the Micro actually costs.

One headless render of the seven script-rendered pages would move four records from `reported`
to `documented`: `ai-galaxy`, `xiangongyun`, `gpushare` and `lighthouse-99`. The seven pages are
the AI Galaxy price cards, the Xiangongyun table, the gpushare card table, the Tencent activity
page, the Rainyun store, the Compshare header row and the Samsung trial page. One tool and one
pass, and it is the cheapest quality gain left in this slice.

Two reports would settle the two rows that rest on one account each. `hosting-vds-com` rests on
one buyer and `4vps-su` on one published complaint. A second report for either would move it
from `reported` to a pattern, and one delivered server would overturn `4vps-su`.

A company-register check would move the whole page, and it is the one thing no record here has.
Four records name a legal person: `cloudcone` gives "CloudCone, LLC, US" in its operator field,
`chamaoyun` gives Chengdu Aite Shiji Network Technology through a reseller profile, `hostslate`
says its terms register a UK brand without a number, and `aeza` names two entities and calls a
third a shell. Checking those four against their registers is an hour's work and it is the only
check on this page that separates a seller from a name.
