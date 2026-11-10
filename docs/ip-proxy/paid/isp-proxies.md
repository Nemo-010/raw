# Per-address ISP proxies

The rung-5 market. A vendor sells one address at a time, registered to a consumer
ISP, running on a datacenter server. It is the cheapest per-address route
to a registration class, and it is the market where the most claims fail a registry
check.

**The question:** what does one ISP-registered address cost per month, and does the
class claim survive a lookup?

**The answer:** between **USD 0.27 and USD 2.80 per address per month**, and four
of the eight published addresses failed a registry check. The class is real; the
marketing is not reliable.

---

## The price ladder, per address per month

| vendor | price per address | minimum order | what is included |
|---|---|---|---|
| **Decodo** | **USD 0.27** (shared, pay-per-IP) | — | shared; dedicated from USD 2 |
| **Webshare** | **USD 0.30** (at 20 proxies) | 20 for USD 6.00/mo | 250 GB included |
| Oxylabs | USD 1.10 to USD 1.50 | USD 30/mo Starter floor | semi-dedicated |
| IPRoyal | USD 1.80 (24 h) to USD 2.40 (90 d) | 1 | unlimited bandwidth |
| Proxy-Seller | "from USD 0.98" — **not readable** | 1 | uncapped, fair use |
| Decodo dedicated | from USD 2.00 | — | dedicated |
| LinkStatic single IP | USD 2.80 | 1 | unlimited traffic |
| **Rayobyte** | USD 5.00 (5 to 99 IPs) | 5 | headline "$0.95" is a commitment rate |
| IPPeak | USD 4.90 | 1 | ❌ class claim fails |

⚠ **Rayobyte's headline is not its entry price.** The page reads "from $0.95/IP a
month" and the table below it reads `$5/IP` for 5 to 99 IPs; `$0.95` applies only
at "Enterprise … at scale with a commitment". A record that quotes USD 0.95 is
wrong by 5×.

⚠ **Proxy-Seller's price is unreadable.** The page title says "from $0.98/IP" and
the order form renders client-side, so the raw HTML carries `Price for 1 IP : $0`.
The real tier price is `unverified`.

---

## The registration check

⭐ **Four vendors here published a sample address or a test IP, across seven
addresses. Four of the seven failed.**

| vendor | the address they published | RIPE says | the vendor claims | verdict |
|---|---|---|---|---|
| Decodo | `37.120.211.30` | **AS9009 M247 Europe**, `M247-LTD-Warsaw`, "M247 LTD Warsaw Infrastructure" | ISP | ❌ **hosting** |
| Decodo | `90.135.104.218` | AS1257 SWIPNET Tele2 Sverige, `LT-TELE2-GPRS` | ISP | ✅ passes |
| NovixLink NTT | `192.220.114.2` | AS2914 NTT America, DIRECT ALLOCATION | 双ISP 住宅 | ❌ carrier |
| NovixLink GTT | `216.36.86.2` | AS3257 GTT-BACKBONE | 双ISP 住宅 | ❌ carrier |
| NovixLink Cox | `24.120.4.1` | **AS22773 Cox Communications**, `wsip-24-120-4-1.lv.lv.cox.net` | 双ISP 家宽 | ✅ passes |
| AnchoredIP | `194.0.109.1` | `ASSIGNED PA`, an individual, KZ | "RIPE-registered" | ❌ not an organisation |
| IPPeak | "Dual NTT" ×9 locations | AS2914 NTT facilities | ISP / residential | ❌ carrier |

⛔ **The "dual ISP" label is a database read, not a network property.** NovixLink's
own knowledge base: *"两类 IP 都要求 ASN 名称和运营公司的类型标签均为 ISP，这就是双
ISP 的含义，并不代表两条线路"*. Both the ASN name and the company-type label must
read "ISP" *in a database*, and it explicitly does not mean two lines. Their terms
then pin delivery to the database they chose: *"仅以服务首次交付时的 IPLense 快速模式
结果和系统记录作为正式交付标准"*. A label the vendor selects the instrument for is
not falsifiable.

⭐ **The instrument that does discriminate is free.** `ip2location.com/demo/<ip>`
returns `usage_type` and `as_usage_type` unauthenticated. On it: `1.1.1.1` reads
`CDN`/`CDN`, `8.8.8.8` reads `DCH`/`DCH`, and the Proton exit this topic measures
reads `DCH`/`CDN`. NovixLink's NTT and GTT test IPs both read `DCH`/`DCH`.

---

## The vendors state what they are selling

Two vendors state the split plainly, and their sentences are worth more than any
marketing claim:

**Webshare:**

> An ISP proxy lives in two worlds at once: the IP address belongs to a residential
> ISP, but the server it runs on sits in a datacenter.

> Tools that check the ASN ... will correctly show a residential ISP like AT&T or
> Comcast. Tools that check the hosting environment may label the IP as datacenter
> or hosting, because, technically, that is where the server is.

**Oxylabs:**

> Static Residential Proxies originate from datacenter proxies, therefore they are
> just as fast as their counterparts.

⭐ **So rung 5 is partly a labelling question.** An ISP proxy defeats a gate that
reads the ASN's *registration*, and it does not defeat a gate that reads the
*hosting flag*. Which of those an upstream reads is not yet measured.

---

## The providers

<!-- generated:start topic=ip-proxy kind=provider verdict=qualifies,qualifies-with-caveat sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AdGuard VPN | Free version: 'Unlimited VPN traffic, compa... | qualifies-with-caveat | documented | not applicable: an exit address... | not applicable: a liv... | email | `dossier/ip-proxy/adguard-vpn.json` |
| AnchoredIP | Trial $0/mo, Dedicated IPv4 1, IPv6 /48 1,... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/anchoredip-registration-corrected.json` |
| Decodo (formerly Smartproxy) | 3-day free trial with 100 MB included to te... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a liv... | card | `dossier/ip-proxy/decodo-isp-proxies.json` |
| RackNerd, DediRock, Volpa... | No free tier at any of the four. Entry pric... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/host-asn-field-absent.json` |
| IPRoyal | No free tier is stated. The cheapest purcha... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a ren... | card | `dossier/ip-proxy/iproyal-isp-proxies.json` |
| IPYE | /48 IPv6 (Free): Full /48 prefix, Instant d... | qualifies-with-caveat | documented | not applicable: a prefix, not a... | not applicable: a rou... | email | `dossier/ip-proxy/ipye-free-48.json` |
| LinkStatic | No free tier is stated; the vendor offers f... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a lea... | email | `dossier/ip-proxy/linkstatic-c-class.json` |
| monosans/proxy-list | Free, no key: an unauthenticated GET return... | qualifies-with-caveat | measured | not applicable: an address, not... | not applicable: a liv... | anonymous | `dossier/ip-proxy/monosans-proxy-list.json` |
| Mullvad VPN | No free tier. The pricing page read 2026-10... | qualifies | documented | not applicable: an exit address... | not applicable: a liv... | anonymous | `dossier/ip-proxy/mullvad-vpn.json` |
| NordVPN | No free tier. The cheapest plan read is Bas... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/nordvpn-exits.json` |
| NovixLink (诺联主机) | No free tier. LAX-CUPN Lite CAD 7.99/month:... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/novixlink-isp-vps.json` |
| Oxylabs | One-time USD 5.00 Welcome Credit on registr... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/oxylabs-isp-proxies.json` |
| Proton VPN | Free plan, quoted from the pricing page: 'C... | qualifies-with-caveat | documented | not applicable: an exit address... | not applicable: a liv... | email | `dossier/ip-proxy/protonvpn-exits.json` |
| Proxy-Seller | No free tier: 'A standard free trial is not... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/proxyseller-isp-proxy.json` |
| RareCloud (Constanta resi... | No free tier on either. RareCloud's Residen... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a ren... | any-phone | `dossier/ip-proxy/rarecoud-and-vpckr.json` |
| RiseupVPN | Free to use with no account: 'You just inst... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a tun... | anonymous | `dossier/ip-proxy/riseup-vpn.json` |
| Riseup VPN | Free to use: no configuration, no account r... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | anonymous | `dossier/ip-proxy/riseup-vpn-exits.json` |
| Route64 | Route64 provides the following services to... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a sta... | email | `dossier/ip-proxy/route64-ipv4-blocks.json` |
| StarVPN (Star Internet Se... | Free VPN Anonymous: '100GB/month data usage... | qualifies-with-caveat | documented | not applicable: an exit address... | not applicable: a liv... | anonymous | `dossier/ip-proxy/starvpn-residential-vpn.json` |
| TheSpeedX/PROXY-List | Free and keyless: 10,256 lines in total acr... | qualifies-with-caveat | measured | not applicable: an address, not... | not applicable: a liv... | anonymous | `dossier/ip-proxy/thespeedx-proxy-list.json` |
| TorGuard | No free tier. A residential dedicated IP is... | qualifies-with-caveat | unverified | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/torguard-residential.json` |
| VPN Gate | Free with no registration: the relay nodes... | qualifies-with-caveat | documented | not applicable: a tunnel and an... | not applicable: a liv... | anonymous | `dossier/ip-proxy/vpn-gate-sstp.json` |
| Windscribe | Free plan carries 2 to 10 GB per month and... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/windscribe-vpn.json` |
<!-- generated:end -->

## The identity walls

| vendor | the wall | the sentence |
|---|---|---|
| Bright Data | **card plus a live human KYC** | *"The KYC process may include a quick intro video call and some verification of your company or personal information."* |
| SOAX | B2B only | *"SOAX may decline access to the Platform for individuals acting in a personal or consumer capacity (B2C)."* |
| Oxylabs | a target blocklist | *"Some websites are restricted on our Residential Proxy network ... All Apple domains ... Some Google domains ... Government websites"* |

⛔ **Bright Data's KYC is the hardest identity wall in this topic** for an
individual with no company, and it applies before any residential or mobile byte is
served.

## What to buy first

⭐ **One USD 1.80 day of IPRoyal, or one USD 6.00 month of Webshare, and one RIPE
lookup per delivered address.** That is the entire experiment: it settles whether a
per-IP vendor's inventory is genuinely spread across subnets, which is the one
number the whole class rests on and which only Proxy-Seller claims.

⚠ **Buy from the vendor whose sample address passed, not the one whose headline is
cheapest.** Decodo's USD 0.27 shared tier and its M247 sample address are the same
vendor.
