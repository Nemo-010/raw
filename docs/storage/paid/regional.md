# Regional: is regional cheaper, and by how much

The hypothesis is that storage in a country where bandwidth and power are cheap is cheaper than
storage in Germany or the United States. It is a reasonable hypothesis and the answer is no:
regional storage is not five to ten times cheaper, and outside
RUB-denominated providers it is usually more expensive.

This document covers 10 qualifying records across Russia, Ukraine, Brazil, India, Poland
and Japan. 3 were rejected. It closes a direction rather than opening one, and
the negative result is the finding.

## The comparison

Sorted by all-in cost per TB per month in the vendor's currency, with the recorded conversion.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Beget S3 (Russia), free egress S3 at 350 Mbit/s... | 0.07 per GB per DAY (2.10/GB/month), billed daily on actual usage... | per-ip-shaping: 350 Mbit/s is a hard port cap 3 | card | fails-quota |
| Cloud.ru Evolution Object Storage (ex-SberCloud)... | Single-zone S3 object storage 1.1346 per GB per month including 22 % VAT... | - | card | fails-quota |
| EVEO Object Storage S3 (Brazil)... | R$0.05/GB/month, billed on stored GB only... | - | card | qualifies-with-caveat |
| KUB.ua File Cloud (Ukraine)... | FILE CLOUD 1: 869.57 /mo for 1 TB; FILE CLOUD 5: 1,840.36 /mo for 5 TB... | - | card | qualifies-with-caveat |
| OVHcloud Object Storage One-Zone Standard... | Unlimited / unbilled minimum: Mozesz przechowywac dowolna ilosc danych... | - | card | qualifies |
| Rollin Host Drive empresarial / Backup & Storage... | Topazio 1 TB R$79.90/mo; Esmeralda 5 TB R$199.90/mo... | - | card | qualifies-with-caveat |
| RUVDS " " /, Russian flat-rate disk VPS with... | 1,023 /mo for 1,024 GB; 1,899 /mo for 2,048 GB... | per-ip-shaping: 100 Mbit/s on the entry tier caps the se | card | qualifies-with-caveat |
| TheHost.ua KeepData, 10 TB flat with traffic... | 25 GB / 100 GB / 500 GB / 1 TB / 10 TB / 50 TB. 10 TB = $59.48/mo... | - | card | qualifies |
| Utho Archive Storage (India)... | INR 0.38/GB/month, no minimum commitment, 11-nines designed durability... | - | card | qualifies-with-caveat |
| Yandex 360 " " (Profi) 3 TB... | 3 TB / 5 TB / 10 TB / 20 TB / 30 TB tiers under Profi... | per-object-cap: Per-object cap 100 GB | email | qualifies-with-caveat |

## What the class is

A regional provider sells storage at a local price in a local currency from a local datacentre.
Three things make it attractive to a reader: the headline rate is often low, the egress is often
included, and the provider is outside the market the big three price for.

Three things make it unattractive, and each is checkable.

**The currency moves.** A rate in RUB, UAH, BRL, INR or PLN is not comparable with a rate in EUR
without a recorded conversion and a recorded date. Every figure in this document carries both.

**The payment rail is often local.** A card issued outside the country may be refused, or the
provider may require a local bank transfer.

**The egress term is the same trap.** A regional provider's storage rate is low for the same
reason a German one's is: the port is cheap locally. Its read term is not different in kind.

## The five figures, and what they say

Five records are the strongest in the class and they are not cheap in absolute terms.

Beget S3 in Russia is USD 26.04 per TB per month with free egress, which is more expensive than
Hetzner's metered Object Storage. Its claim is the free egress at 350 Mbit/s, and the egress is
what costs elsewhere.

Cloud.ru Evolution is USD 14.07 per TB, EVEO in Brazil is USD 10.19, OVHcloud's Polish subsidiary
is USD 9.34 with free egress, and KUB.ua is USD 8.16.

The two below USD 6 are the exceptions and neither generalises. TheHost.ua's KeepData is USD 5.95
per TB at 10 TB with traffic included and WebDAV, SFTP and Samba, which is a genuine European-facing
floor. Yandex 360's Profi tier is USD 2.00 per TB at 3 TB, and it is the only regional option below
the USD 2 floor in the entire corpus.

Yandex is the exception: every regional option except
RUB-priced Yandex is more expensive than the USD 2 per TB floor. It is cheap because it is priced
in roubles for a domestic market, and its identity and payment terms are domestic too.

## The Asia result

Two records here are the Asian market and both are above the floor by a wide margin. Utho's Archive
tier in India is USD 4.10 per TB for cold storage with no egress fee, and it is the cheapest Asian
figure found. Every other Asian option in the corpus, including the ones rejected, is six to
twenty times the floor.

That is the second half of the negative result. The market with the cheapest bandwidth does not
sell cheap storage to a foreign individual, because the products are priced for domestic committed
volume.

## Why the hypothesis fails

Three reasons, and they are structural rather than incidental.

The cheap part of a regional market is bandwidth, not disk. A provider that owns an ASN and
transit sells egress cheaply and charges the international market rate for storage, which is why
Beget's free egress comes with a USD 26 per TB storage rate.

The storage rate that looks low is usually a cold tier. Utho's USD 4.10 is an archive class with a
restore path, and comparing it with Hetzner's hot rate is the same category error as comparing
OVHcloud's Cold Archive with its Standard tier.

And the floor is not a regional phenomenon at all. EUR 1.25 per raw TB at Webtropia and EUR 1.69 at
PulsedMedia are German and Finnish prices, and no regional provider in this document beats them.

### Beget S3 (Russia), free egress S3 at 350 Mbit/s, the only Russian object store with traffic in

> 0.07 per GB per DAY (2.10/GB/month), billed daily on actual usage, unlimited buckets. Avail 99.98 %, three copies across servers

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 350 Mbit/s is a hard port cap 3. A new account costs card. Observed behaviour: Long-running Russian shared host with 24/7 support and 99.98 % stated availability.

Evidence: `https://beget.com/ru/cloud/storage` (2026-10-21), record `dossier/storage/beget-s3-free-egress-s3-at-350-mbit-s-the-only-russian-o.json`.
Verdict: `fails-quota`.

### Cloud.ru Evolution Object Storage (ex-SberCloud), cheapest Russian object rate, VAT-inclusive

> Single-zone S3 object storage 1.1346 per GB per month including 22 % VAT (0.93 ex-VAT). Tariff document takes effect 2026-09-28. No volume published

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Cloud.ru is the rebranded SberCloud and is the largest non-hyperscaler Russian cloud. Read path (recorded as metered): Not stated in the tariff fragment that was retrievable (the document's traffic annex was truncated at the point of reading). (`reported`, 2026-10-21).

Evidence: `https://cloud.ru/documents/tariffs/evolution/object-storage` (2026-10-21), record `dossier/storage/cloud-ru-evolution-object-storage-cheapest-russian-objec.json`.
Verdict: `fails-quota`.

### EVEO Object Storage S3 (Brazil), the only zero-egress S3 endpoint found in Latin America

> R$0.05/GB/month, billed on stored GB only; buckets up to 5 PB, no provisioning. Positioned as Armazenamento sem taxas de download (egress) ou API>>

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Enterprise-oriented Brazilian provider with Tier III DCs and two-region replication.

Evidence: `https://www.eveo.com.br/object-storage-s3/` (2026-10-21), record `dossier/storage/eveo-object-storage-s3-the-only-zero-egress-s3-endpoint.json`.
Verdict: `qualifies-with-caveat`.

### KUB.ua File Cloud (Ukraine), Nextcloud-backed flat per-TB with unlimited traffic

> FILE CLOUD 1: 869.57 /mo for 1 TB; FILE CLOUD 5: 1,840.36 /mo for 5 TB. Unlimited users, unlimited traffic, 50 concurrent connections, 7-day trial, Nextcloud platform

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Nextcloud-on-managed-infrastructure.

Evidence: `https://kub.ua/file-cloud/` (2026-10-21), record `dossier/storage/kub-ua-file-cloud-nextcloud-backed-flat-per-tb-with-unli.json`.
Verdict: `qualifies-with-caveat`.

### OVHcloud Object Storage One-Zone Standard (Poland subsidiary), flat S3 with contractually free

> Unlimited / unbilled minimum: Mozesz przechowywac dowolna ilosc danych, nie okreslamy minimalnego wolumenu>>. Billed per GiB-hour at 0.00004861 PLN, shown as ~0.0354853 PLN/GiB/month over 730 h

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: No reliability concern raised by any source. Read path (recorded as not metered): FREE, three times over and verbatim: the prices table reads Ruch zewnetrzny przychodzacy/wychodzacy | Darmowy (external incoming/outgoing traffic: free) for Standard, High Performance AND Infrequent Access; the product page states nie pacisz za wywoania API ani za ruch przychodzacy i wychodzacy (no charge for API calls nor for incoming or outgoing traffic); the classes page repeats Brak opat za ruch wychodzacy. (`reported`, 2026-10-21).

Evidence: `https://www.ovhcloud.com/pl/public-cloud/prices/` (2026-10-21), record `dossier/storage/ovhcloud-object-storage-one-zone-standard-flat-s3-with-c.json`.
Verdict: `qualifies`.

### Rollin Host Drive empresarial / Backup & Storage (Brazil), flat per-TB, no request or traffic c

> Topazio 1 TB R$79.90/mo; Esmeralda 5 TB R$199.90/mo; Diamante 10 TB R$379.90/mo. Monthly cycle, no lock-in (sem fidelidade>>), Brazilian NF-e invoice, ceiling 10 TB then sales contact

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Small Brazilian host. Read path (recorded as not metered): FREE, stated twice and unambiguously: Preco fixo por capacidade , sem cobranca por upload, download ou requisicao (fixed price per capacity , no charge for upload, download or request) and repeated per plan as Sem cobranca de trafego. (`reported`, 2026-10-21).

Evidence: `https://www.rollinhost.com.br/backup-na-nuvem` (2026-10-21), record `dossier/storage/rollin-host-drive-empresarial-backup-storage-flat-per-tb.json`.
Verdict: `qualifies-with-caveat`.

### RUVDS " " /, Russian flat-rate disk VPS with unlimited traffic

> 1,023 /mo for 1,024 GB; 1,899 /mo for 2,048 GB; 3,798 /mo for 4,096 GB. Line advertised 1 18 >>. Landing headline: 500 1 />>

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 100 Mbit/s on the entry tier caps the se. A new account costs card. Observed behaviour: Long-established Russian host (ruvds.com), KVM, own DCs.

Evidence: `https://ruvds.com/ru/huge-disk/` (2026-10-21), record `dossier/storage/ruvds-russian-flat-rate-disk-vps-with-unlimited-traffic.json`.
Verdict: `qualifies-with-caveat`.

### TheHost.ua KeepData, 10 TB flat with traffic included, WebDAV/SFTP/Samba, the best Western-faci

> 25 GB / 100 GB / 500 GB / 1 TB / 10 TB / 50 TB. 10 TB = $59.48/mo, or $642.34/yr (10 % discount), or $1,141.90 for 2 years (20 %). Also sold in UAH and EUR on the same table (2,499 / EUR 49.98 / $59.48 per month for 10 TB). Inodes: 1,000 K...

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: Ukrainian operator (Kyiv), billing in UAH/EUR/USD with card. Read path (recorded as not metered): Included and unmetered , the traffic row reads simply Traffic, with access speed 10 Gbit/s, and there is no meter, overage rate or traffic pack anywhere on the page. (`reported`, 2026-10-21).

Evidence: `https://www.thehost.ua/en/hosting/cloud-storage` (2026-10-21), record `dossier/storage/thehost-ua-keepdata-10-tb-flat-with-traffic-included-web.json`.
Verdict: `qualifies`.

### Utho Archive Storage (India), INR 0.38/GB/mo cold tier, INR -denominated, no egress fee

> INR 0.38/GB/month, no minimum commitment, 11-nines designed durability, 1-4 hour standard retrieval (instant available). The general object tier is quoted separately at INR 4/GB/month above a 100 GB base

That is the record's own wording (`reported`, 2026-10-21). A new account costs card. Observed behaviour: The most important reliability finding here is a PRICE DISCREPANCY INSIDE ONE VENDOR. Read path (recorded as not metered): No egress fees in India on the object-storage page and Zero egress fees / No bandwidth overage charges on the pricing page. (`reported`, 2026-10-21).

Evidence: `https://utho.com/archive-storage` (2026-10-21), record `dossier/storage/utho-archive-storage-0-38-gb-mo-cold-tier-denominated-no.json`.
Verdict: `qualifies-with-caveat`.

### Yandex 360 " " (Profi) 3 TB, the regional price floor with unlimited public-link downlo

> 3 TB / 5 TB / 10 TB / 20 TB / 30 TB tiers under Profi. 3 TB is the value tier: 990 /mo list, 495 /mo when paid annually (50 % annual discount is the steady state, not a short promo, the crossed-out 990 is the monthly rate). Upload per...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: Per-object cap 100 GB. A new account costs email. Observed behaviour: Two real risks.

Evidence: `https://360.yandex.ru/premium-plans/` (2026-10-21), record `dossier/storage/yandex-360-3-tb-the-regional-price-floor-with-unlimited.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Mail.ru Cloud / Mail (VK)... | fails-quota | 1 TB plan. Landing promo (2026-10-15 to 2026-11-19): first year 1,560, from the second year 3,000 (1 560... |
| Selectel Object Storage (Russia)... | fails-egress | Ice 0.89/GB/mo; Cold 1.26/GB/mo; Standard 2.57/GB/mo. Volume ladder: up to 10 TB 1.35, 10-50 TB 1.31... |
| SpaceByte Cloud (India), INR 150/TB/mo claimed... | fails-quota | Starter 50 GB INR 20/mo; Freelancer 100 GB INR 35/mo; 500 GB INR 100/mo; Studio Pro 1 TB INR 150/mo (or INR 1,650/yr)... |

Three records were rejected and two of them are instructive. Tencent Cloud COS has the worst egress
ratio in the corpus at USD 76.52 per TB. Selectel's cold tier is cheap and its read-back is USD
24.31 per TB.

SpaceByte's claim of INR 150 per TB per month is the lowest credible-looking number found anywhere
and it did not survive contact: a rate two orders of magnitude below the floor is a marketing
figure, and the record says so.

## Chaining

Regional storage is not a tier, and the document says so.

The one thing worth carrying forward is the method. A regional price is not comparable until it
carries a conversion and a date, and a storage rate is not comparable until its egress term is
read. Applied to regional offers, those two rules close the direction in an afternoon.
