# Residential and mobile networks

The eyeball classes: addresses that belong to a consumer ISP or a mobile carrier.
They are the strongest registration class available and the most expensive per
byte, and at 41.8 GiB a month the per-byte framing is the wrong way to price them.

**The question:** at 41.8 GiB a month, what does an eyeball exit cost, and what does
the same money buy in distinct address classes?

**The answer:** USD 34 to USD 180 for a rotating residential month, and USD 59 to
USD 135 for a mobile port. Neither is a dead end at this volume. But the money buys
**one address at a time from a shared pool**, while the same USD 6 buys twenty
static ISP addresses held for a month. **The unit of sale is the address, and
per-GB is the retail tier.**

---

## The volume this is priced against

⭐ `inferred`, and the derivation is the point. A Workers relay gateway served
**39,929 requests in two days** (2026-09-21 to 2026-09-22), about 599,000 a month,
and a generation turn carries about **72.7 KB of SSE**. At 75 KB each that is
**598,935 × 75,000 = 44.9 GB decimal, or 41.8 GiB a month**.

⚠ **41.8 GiB is a floor.** It counts upstream response bytes only and assumes
every request is a generation turn. If the real figure is three times higher, every
per-GB row below moves and every per-address row does not, which is itself the
argument for the per-address products.

⛔ **It is `inferred`, so it carries no table cell.** Where a table below quotes a
monthly cost it is the vendor's own rate multiplied by 41.8 GiB, and the
multiplication is shown.

## Rotating residential, priced at 41.8 GiB

| vendor | rate at this volume | 41.8 GiB costs | minimum | identity |
|---|---|---|---|---|
| Geonode | USD 0.77/GB | **USD 34.65** | — | card |
| Proxy-Cheap | — | USD 39.78 | — | card |
| **Evomi** | **USD 0.99/GB** | **USD 44.55** | — | card, no KYC by default |
| SOAX (Tier 3) | USD 0.35/GB at Scale | USD 135 at the entry tier | USD 200/mo Builder | card, B2B only |
| Decodo | USD 3.75/GB at 3 GB | ~USD 169 | — | card |
| Bright Data | USD 4.00/GB (promo) | **USD 179.70** | USD 499/mo | **card + video KYC** |
| Oxylabs | USD 6.00/GB at small volume | — | — | card |

⛔ **A per-GB rate is only meaningful against a workload.** USD 0.80/GB against a
1 TiB/day workload is USD 26,388 a month; at 41.8 GiB it is **USD 36**. The
difference is a workload mismatch, not an arithmetic error.

⚠ **Every one of these is rung 2 or 3, not rung 5.** A rotating pool hands out a
different address per request, which 102 relay Workers already do for nothing. The
purchase is the *class*, not the rotation.

## Mobile, priced per port

| vendor | price | what is offered | identity |
|---|---|---|---|
| **Proxidize** | USD 59/proxy/month | one carrier address, 50 GB fair-use threshold | **national-id KYC** |
| StatesideIP | USD 45/30 days | one named-carrier US port, crypto accepted | anonymous |
| Proxuno | USD 75/30 days | one named modem on a named carrier | — |
| ProxyGuys | USD 80/month | "real carrier 5G", no carrier named | card |
| SOAX mobile | USD 3.00/GB entry | the shared pool | card, B2B only |
| **AirProxy** | **not published** | 1,200 Italian 4G modems on Vodafone/TIM/WindTre/Fastweb | **national-id + selfie** |

⚠ **Mobile is not a stronger rung than residential.** Both are eyeball classes. The
one third-party measurement found, Proxyway's 2026 audit across Amazon, Google and
Instagram, puts mobile at **75.26%** success against residential's **74.43%**, a
difference of 0.83 percentage points. The vendor story that a carrier address is
immune because blocking it would block thousands of real users is contradicted by
Cloudflare's own CGNAT research, which finds CGNAT addresses are rate-limited
**three times more often** than non-CGNAT ones.

⛔ **So a mobile port buys a different ASN, which is rung 4, at 10 to 100 times the
per-address price.** It does not buy a rung the residential pool leaves open.

---

## The identity walls, which are the real constraint

| vendor | wall | the sentence |
|---|---|---|
| Proxidize | **national-id** | *"You must complete identity verification (Tier 1) before you can use the proxies."* |
| AirProxy | **national-id plus a selfie** | *"we recommend to verify your identity by submitting valid id proof and selfie"*; Italian buyers need a VAT number or fiscal code |
| Bright Data | **card plus a video call** | *"a quick intro video call and some verification of your company or personal information"* |
| SOAX | B2B only | *"SOAX may decline access to the Platform for individuals acting in a personal or consumer capacity"* |

⭐ **The cheapest mobile offers are the ones with the weakest identity check.**
StatesideIP at USD 45 takes crypto and asks for nothing; Proxidize at USD 59 wants a
government photo ID and a camera. That trade is the finding, and it is the buyer's
to make.

---

## The providers

<!-- generated:start topic=ip-proxy kind=provider verdict=fails-identity,fails-quota sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AirProxy | No free tier. The vendor's /en/ page lists... | fails-identity | documented | not applicable: an address, not... | not applicable: a ren... | national-id | `dossier/ip-proxy/airproxy-mobile.json` |
| Bright Data | No recurring free allowance for proxy traff... | fails-identity | documented | not applicable: an address, not... | not applicable: a liv... | institution | `dossier/ip-proxy/brightdata-residential.json` |
| InterLIR | No free tier. Rent is listed 'from 110 euro... | fails-identity | documented | not applicable: an address bloc... | not applicable: a lea... | institution | `dossier/ip-proxy/interlir-ipv4-rent.json` |
| IPXO | No free IPv4 lease. The platform subscripti... | fails-identity | documented | not applicable: an address bloc... | not applicable: a lea... | institution | `dossier/ip-proxy/ipxo-ipv4-leasing.json` |
| Proxidize | No free tier on the cited pages. Per GB USD... | fails-identity | documented | not applicable: a proxy endpoin... | not applicable: a liv... | national-id | `dossier/ip-proxy/proxidize-mobile.json` |
| SOAX | No. Sandbox is our no-commitment option. It... | fails-quota | documented | not applicable: an address, not... | not applicable to tra... | card | `dossier/ip-proxy/soax-mobile.json` |
| ZoogVPN | A Free plan exists: '10 GB of monthly traff... | fails-quota | documented | not applicable: an address, not... | not applicable: a tun... | email | `dossier/ip-proxy/zoogvpn.json` |
<!-- generated:end -->

## Dead vendors in this class

⛔ **Vendors in this class that are gone:**

| vendor | status | evidence |
|---|---|---|
| **NetNut** | seized by the FBI, 2026-07-02 | a seizure notice on every path including `/robots.txt`; Alarum's own SEC exhibit confirms it |
| **LunaProxy** | NXDOMAIN | named in Google's IPIDEA takedown of 2026-01-28 |
| **PIA S5** | NXDOMAIN | two lookalike "continuation" sites carry identical copy |
| **911.re** | seized | — |
| **Bright Data mobile** | **withdrawn April 2026** | the product page redirects; the docs index lists Residential, Data Center and ISP only |

## The one experiment worth running

⭐ **One 30-day mobile port at StatesideIP (USD 45, crypto, no KYC) and one
residential month at Evomi (USD 44.55), then the same request from each and from a
Cloudflare address in the same minute, against an upstream known to refuse
Cloudflare.** That is USD 90 and it settles whether the eyeball class moves a
refusal at all. That is the one thing every vendor in this document asserts and this
topic has not measured.

⚠ **Run the Cloudflare control in the same minute.** Meta refuses a model it serves
in bursts lasting minutes, so two arms run one after another measure different
bursts.
