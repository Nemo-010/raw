# Prefixes and subnet leases

The class that sells a *block* rather than an address: a `/48` of IPv6, a `/24` of
IPv4, a routed `/29`. It is the only class that can attack rung 3, and it is the
class most often sold with a claim about rung 5 that does not survive a registry
check.

**The question:** does a bigger prefix defeat IPv6 rotation blocking, and what
does a `/24` actually cost per address?

**The answer:** a bigger prefix does not defeat rotation, because size is not
diversity. Meta's own measurement says a `/48` is the bucketing unit a defender
would choose, and its blocklisting recommendation is `/64`. The free `/48` is a
datacenter allocation that needs an ASN the holder does not have. The
ISP-registered class is a separate product at USD 1,600 a month.

---

## Why a `/48` does not help, and the evidence

The question is whether IPYE's free `/48` gets around the technique that blocks
IPv6 rotation. Four separate findings say no.

### 1. Meta's own paper measures the `/48` as the unit that behaves like one IPv4 address

Li and Freeman, *Towards A User-Level Understanding of IPv6 Behavior*, ACM IMC
2020, pp. 428–442, DOI `10.1145/3419394.3423618`. The sample is 0.1% of all
authenticated Facebook requests, 2020-01-23 to 2020-04-19, over prefixes from
`/112` to `/32`. ⚠ The ACM copy is paywalled; the sentences below were read from
the full text on 2026-10-24.

The paper's rate-limiting finding, verbatim:

> We found in Section 6.2 that IPv6 /48 subnets appeared most similar to IPv4
> addresses in their distribution of user population sizes, so existing rate
> limiting logic applied to IPv4 addresses could potentially be translated to IPv6
> /48 prefixes.

⭐ **That is the sentence that answers the question**, and it is narrower than "a
`/48` defeats blocking". It says a `/48` is where *user populations* look like an
IPv4 address, which is the input a **rate limiter** counts. A vendor that limits per user-population will therefore land on the `/48`.

### 2. For *blocklisting* the same paper recommends `/64`, which is inside a `/48`

> /56 subnets are closest in behavior to IPv4 addresses for malicious users,
> either the full IPv6 address or /64 subnets are most suitable for IP-based
> security applications, with both providing better performance tradeoffs than
> IPv4 addresses.

⛔ **So the two mechanisms have different units, and the topic must not blur
them.** A rate limiter is likely to count the `/48`; a blocklister is recommended
to count the `/64` or the full address. **Either way a `/48` is the wrong shape:**

| if the defender counts | what a `/48` buys |
|---|---|
| the `/48`, per the rate-limiting finding | **nothing**: it is the counted unit |
| the `/64`, per the blocklisting recommendation | 65,536 chances inside one counted `/48`, which is what Cloudflare already does for free |
| the ASN | nothing |

⭐ **That is the answer.** The `/48` is either exactly the unit counted or a
container of units that can already be rotated.

### 3. A `/48` is not what a residential connection looks like

APNIC Labs, *IPv6 prefix lengths*, `blog.apnic.net/2024/04/25/ipv6-prefix-lengths/`,
read 2026-10-24:

> The /64 subnet is the most common subnet size, used in 57% of cases in recent
> data. The /60 and /56 subnets are seen in 21% and 20% of cases respectively.
> Finally, the /48 subnet is seen in 2% of cases.

> This data indicates that few ISPs assign end sites a /48 prefix … the use of a
> /64 prefix is prevalent in mobile services … while the use of a /60 and /56
> appears to have become the default setting in broadband deployments.

⚠ **A real home broadband line is usually a `/56` or a `/60`, which is *smaller*
than the `/48` being sold.** So an ISP advertising a `/48` as a "residential shape"
is selling a block larger than a typical residence has.

### 4. The free `/48` is not the ISP product

IPYE's own pages separate the two:

| the product | price | what it is |
|---|---|---|
| free `/48` | **USD 0** | a datacenter allocation, "limited support", needs an origin ASN |
| `/44` | USD 20/yr | the same, larger |
| `/36` | USD 200/yr | the same, larger |
| **ISP Network Bundle** | **USD 1,600/mo** | `/22` IPv4, ISP-assigned, 1,024 addresses, 10 Gbps unmetered |

The ISP class claim is attached to the USD 1,600 bundle. The free `/48` carries no class claim at all.

⛔ **And the free `/48` cannot be used until the holder has an ASN.** The vendor's
own sentence:

> Announcing the prefix needs an origin ASN. Use one you already operate, or add a
> shared or dedicated ASN from IPYE.

The shared ASN is USD 300/yr and the dedicated one USD 700/yr. So the free `/48`
is not usable without a paid ASN.

---

## What a prefix actually costs per address

⭐ **The number that decides the class: a contiguous block is more expensive per
address than a single address, and it buys fewer rung-3 units than 256 separate
addresses would.**

| product | price | addresses | per address per month |
|---|---|---|---|
| IPYE `/24` | USD 160/mo | 256 | **USD 0.63** |
| LinkStatic 整C段 US | USD 500/mo | 256 | USD 1.95 |
| Hetzner `/29` | EUR 13.60/mo + EUR 34.90 setup | 6 usable | EUR 2.27 |
| IPXO `/29` campaign | USD 2.00/mo | 8 | USD 0.25 |
| **Webshare static ISP** | **USD 6.00/mo for 20** | 20 | **USD 0.30** |
| Decodo shared pay-per-IP | USD 0.27/IP | 1 | USD 0.27 |

⚠ **Read the last two rows against the first two.** Twenty separate ISP addresses
at USD 0.30 each cost the same as one `/24` at USD 160 and give twenty *separate*
subnets instead of one. A `/24` is **one** rung-3 unit. Twenty per-IP proxies are
up to twenty.

⭐ **That comparison is the topic's central economic claim, and it is `inferred`,
because the distinct `/24`s behind a per-IP vendor's inventory have not been
counted.** Proxy-Seller publishes the only number that bears on it: *"IPs are
distributed across 200+ Class B and 600+ Class C subnets, preventing IP clustering
in a single range"*. That sentence is testable with a 20-IP order and twenty RIPE
lookups.

---

## The providers

<!-- generated:start topic=ip-proxy kind=provider verdict=qualifies,qualifies-with-caveat,paid-only sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 711Proxy | No free tier stated. The pricing index list... | paid-only | documented | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/711proxy-residential-gb.json` |
| 711Proxy | No free tier for the static product. Static... | paid-only | documented | not applicable: an address or a... | not applicable: an ad... | email | `dossier/ip-proxy/711proxy-static-residential.json` |
| AaITR | No free tier. The product page lists a dedi... | paid-only | reported | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/aaitr-static-residential-vps.json` |
| AdGuard VPN | Free version: 'Unlimited VPN traffic, compa... | qualifies-with-caveat | documented | not applicable: an exit address... | not applicable: a liv... | email | `dossier/ip-proxy/adguard-vpn.json` |
| AirVPN | No free tier. The buy page lists Three days... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | anonymous | `dossier/ip-proxy/airvpn-exits.json` |
| AnchoredIP | Trial $0/mo, Dedicated IPv4 1, IPv6 /48 1,... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/anchoredip-registration-corrected.json` |
| AnyIP.com (Seven Digital... | No free tier. 'Prices per month with an ann... | paid-only | documented | not applicable: an address bloc... | not applicable: a lea... | email | `dossier/ip-proxy/anyip-com-ipv4-lease.json` |
| Astrill VPN | No free tier. The pricing page lists three... | paid-only | documented | not applicable: an exit address... | not applicable: a liv... | email | `dossier/ip-proxy/astrill-vpn.json` |
| AzireVPN | No free tier. The pricing page lists 1 Mont... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/azirevpn-exits.json` |
| Cliproxy | No free tier is stated on the pages read. S... | paid-only | documented | not applicable: an address or a... | not applicable: an ad... | email | `dossier/ip-proxy/cliproxy-static-isp.json` |
| Cryptostorm | No free tier. The cheapest 1-year token is... | paid-only | documented | not applicable: an address, not... | not applicable: a tun... | anonymous | `dossier/ip-proxy/cryptostorm.json` |
| Cryptostorm | No free tier read. Access is a token bought... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | anonymous | `dossier/ip-proxy/cryptostorm-exits.json` |
| Decodo (formerly Smartproxy) | 3-day free trial with 100 MB included to te... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a liv... | card | `dossier/ip-proxy/decodo-isp-proxies.json` |
| FastestVPN | No free tier. The pricing page lists a 1 Mo... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/fastestvpn-exits.json` |
| GHOSTnet GmbH | No free tier. '119,- € / Monat*' for a /24... | paid-only | documented | not applicable: an address bloc... | not applicable: a ren... | email | `dossier/ip-proxy/ghostnet-ipv4-24-rent.json` |
| RackNerd, DediRock, Volpa... | No free tier at any of the four. Entry pric... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/host-asn-field-absent.json` |
| IPFLY (Chengdu Smart Mapp... | No standing free tier with a stated size. T... | paid-only | documented | not applicable: a traffic plan... | Rotating residential... | email | `dossier/ip-proxy/ipfly.json` |
| IPRoyal | No free tier is stated. The cheapest purcha... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a ren... | card | `dossier/ip-proxy/iproyal-isp-proxies.json` |
| IpStar | No free tier stated on the plan pages. The... | paid-only | documented | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/ipstar-residential.json` |
| IPYE | /48 IPv6 (Free): Full /48 prefix, Instant d... | qualifies-with-caveat | documented | not applicable: a prefix, not a... | not applicable: a rou... | email | `dossier/ip-proxy/ipye-free-48.json` |
| IPYE | No free tier for this bundle. The Server +... | paid-only | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/ipye-isp-network-bundle.json` |
| IVPN | No free tier. The pricing page lists three... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | anonymous | `dossier/ip-proxy/ivpn-exits.json` |
| LinkStatic | No free tier is stated; the vendor offers f... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a lea... | email | `dossier/ip-proxy/linkstatic-c-class.json` |
| LokiProxy (mingdi Network... | No self-service free tier. 'Do you offer tr... | paid-only | documented | not applicable: a traffic pack... | Premium Plan traffic... | email | `dossier/ip-proxy/lokiproxy.json` |
| LokiProxy | No free tier. The FAQ states 'The LokiProxy... | paid-only | documented | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/lokiproxy-rotating-residential.json` |
| monosans/proxy-list | Free, no key: an unauthenticated GET return... | qualifies-with-caveat | measured | not applicable: an address, not... | not applicable: a liv... | anonymous | `dossier/ip-proxy/monosans-proxy-list.json` |
| Mullvad VPN | No free tier. The pricing page read 2026-10... | qualifies | documented | not applicable: an exit address... | not applicable: a liv... | anonymous | `dossier/ip-proxy/mullvad-vpn.json` |
| Mysterium VPN | No free plan. Yearly prices read from the p... | paid-only | documented | not applicable: an address, not... | not applicable: a tun... | email | `dossier/ip-proxy/mysterium-vpn.json` |
| NodeMach (formerly VIRCS) | No free tier. The KVM cloud host Standard p... | paid-only | reported | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/nodemach-formerly-vircs.json` |
| NordVPN | No free tier. The cheapest plan read is Bas... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/nordvpn-exits.json` |
| NovixLink (诺联主机) | No free tier. LAX-CUPN Lite CAD 7.99/month:... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/novixlink-isp-vps.json` |
| NymVPN | No free plan. The pricing page shows the 1-... | paid-only | documented | not applicable: an address, not... | not applicable: a tun... | anonymous | `dossier/ip-proxy/nymvpn.json` |
| Obscura | No free plan and no yearly plan. The pricin... | paid-only | documented | not applicable: an address, not... | not applicable: a tun... | anonymous | `dossier/ip-proxy/obscura.json` |
| Oeck | No free tier read. The live pricing page li... | paid-only | documented | not applicable: an exit address... | not applicable: a liv... | email | `dossier/ip-proxy/oeck-vpn.json` |
| OnesProxy (壹创云) | No price-free tier stated; the page has a '... | paid-only | documented | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/onesproxy-residential.json` |
| OnesProxy | No standing free tier. New users can ask cu... | paid-only | documented | not applicable: an address or a... | not applicable: an ad... | email | `dossier/ip-proxy/onesproxy-static-residential.json` |
| Oxylabs | One-time USD 5.00 Welcome Credit on registr... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/oxylabs-isp-proxies.json` |
| Private Internet Access | No free tier. The buy page lists 1 Month at... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/private-internet-access-exits.json` |
| Proton VPN | Free plan, quoted from the pricing page: 'C... | qualifies-with-caveat | documented | not applicable: an exit address... | not applicable: a liv... | email | `dossier/ip-proxy/protonvpn-exits.json` |
| Proxy001 | No free allowance on the pricing page. Regu... | paid-only | documented | not applicable: an address or a... | purchased traffic is... | email | `dossier/ip-proxy/proxy001-residential.json` |
| Proxy001 | No free tier on the pricing page. The page... | paid-only | documented | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/proxy001-rotating-residential.json` |
| Proxy-Seller | No free tier: 'A standard free trial is not... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/proxyseller-isp-proxy.json` |
| RareCloud (Constanta resi... | No free tier on either. RareCloud's Residen... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a ren... | any-phone | `dossier/ip-proxy/rarecoud-and-vpckr.json` |
| Residential-IDC (resident... | No free tier. The store lists US RCN VDS (A... | paid-only | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/residential-idc-us-vds.json` |
| ResidentialVPS (residenti... | No free tier. Starter is $34.95 monthly (4... | paid-only | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/residentialvps-us-rdp.json` |
| RiseupVPN | Free to use with no account: 'You just inst... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a tun... | anonymous | `dossier/ip-proxy/riseup-vpn.json` |
| Riseup VPN | Free to use: no configuration, no account r... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | anonymous | `dossier/ip-proxy/riseup-vpn-exits.json` |
| Route64 | Route64 provides the following services to... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: a sta... | email | `dossier/ip-proxy/route64-ipv4-blocks.json` |
| Shlii (shlii.io) | No free tier. A third-party review of the v... | paid-only | reported | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/shlii-hinet-home-broadband.json` |
| SixtyNet (sixtynet.net) | No free tier. A trade site's 2025-10-22 rea... | paid-only | reported | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/sixtynet-residential-vps.json` |
| SolaDrive | No free tier. Residential IP VPS SD-2 is 'S... | paid-only | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/soladrive-residential-ip-vps.json` |
| sososo | No free tier. Japan D zone dedicated is $29... | paid-only | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/sososo-japan-private-room.json` |
| sososo | No free tier. Japan Rakuten dedicated is $9... | paid-only | documented | not applicable: an address, not... | not applicable: a ren... | email | `dossier/ip-proxy/sososo-rakuten-5g-private-room.json` |
| StarVPN (Star Internet Se... | Free VPN Anonymous: '100GB/month data usage... | qualifies-with-caveat | documented | not applicable: an exit address... | not applicable: a liv... | anonymous | `dossier/ip-proxy/starvpn-residential-vpn.json` |
| Surfshark | No free plan read. The pricing page FAQ sta... | paid-only | measured | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/surfshark-exits.json` |
| tacs.cloud (TA Consulting... | No free tier. The site's IP calculator stat... | paid-only | documented | not applicable: an address bloc... | not applicable: a lea... | email | `dossier/ip-proxy/tacs-cloud-ipv4-lease.json` |
| TheSpeedX/PROXY-List | Free and keyless: 10,256 lines in total acr... | qualifies-with-caveat | measured | not applicable: an address, not... | not applicable: a liv... | anonymous | `dossier/ip-proxy/thespeedx-proxy-list.json` |
| Tokyonline | No free tier. So-Net Standard is JPY 8,800... | paid-only | documented | not applicable: an address, not... | not applicable: a ren... | any-phone | `dossier/ip-proxy/tokyonline-so-net-vps.json` |
| TorGuard | No free tier. A residential dedicated IP is... | qualifies-with-caveat | unverified | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/torguard-residential.json` |
| Trust.Zone | No free plan. A 3-day free trial with 'No c... | paid-only | documented | not applicable: an address, not... | not applicable: a tun... | email | `dossier/ip-proxy/trust-zone.json` |
| VPN.ac | No free plan. The plans page lists '1 Year'... | paid-only | documented | not applicable: an address, not... | not applicable: a tun... | email | `dossier/ip-proxy/vpn-ac.json` |
| VPN.ac | No free tier. A 1-week trial account costs... | paid-only | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/vpn-ac-exits.json` |
| VPN Gate | Free with no registration: the relay nodes... | qualifies-with-caveat | documented | not applicable: a tunnel and an... | not applicable: a liv... | anonymous | `dossier/ip-proxy/vpn-gate-sstp.json` |
| Webshare | No free tier for the Static Residential (IS... | paid-only | documented | not applicable: an address, not... | not applicable: an ad... | card | `dossier/ip-proxy/webshare-static-residential.json` |
| Windscribe | Free plan carries 2 to 10 GB per month and... | qualifies-with-caveat | documented | not applicable: an address, not... | not applicable: an ad... | email | `dossier/ip-proxy/windscribe-vpn.json` |
| ZooProxy (formerly FluxISP) | Residential from $0.38/GB and ISP proxy fro... | paid-only | documented | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/zooproxy-fluxisp.json` |
<!-- generated:end -->

## The registration check, which is the only thing that matters

A prefix vendor's claim is about the **registry entry**, and the registry is
public. Two commands settle it for any address:

```bash
curl -qsS "https://stat.ripe.net/data/prefix-overview/data.json?resource=ADDRESS"
curl -qsS "https://rdap.db.ripe.net/ip/ADDRESS"
```

| what RIPE returns | what it means for rung 5 |
|---|---|
| a carrier name, e.g. `AS22773 Cox Communications` | ✅ the class claim is plausible |
| a hosting name, e.g. `AS9009 M247 Europe` | ❌ it is a datacenter address |
| a lease broker, e.g. `IPXO` or `Private Customer` | ❌ the block is subleased, and the class is the broker's |
| `ASSIGNED PA` under an individual | ❌ not even an organisation allocation |
| a transit carrier, e.g. `AS2914 NTT America` | ❌ a carrier is not an eyeball network |

⚠ **The distinction between a transit carrier and an eyeball ISP is the one buyers
miss.** NTT, GTT, Cogent and Telia are carriers: their addresses are announced to
other networks, not assigned to homes. "Dual NTT" and "NTT America 直供" are
carrier addresses, and both vendors selling them failed the check.

## Dead ends in this class

- **A larger prefix is not more diversity.** Every row above is one contiguous
  block in one ASN. Hetzner's `/29`, Azure's `/29` and IPYE's `/22` all fail rung 4
  for the same reason Cloudflare does.
- **A `/48` routed to a VPS does not change the ASN of the packets leaving that
  VPS.** The prefix's registration and the announcing AS are two facts, and a
  vendor selling "ISP subnets" sells the first.
- **"Native IP" (原生IP) is the weakest claim in the vocabulary.** It asserts only
  that the registration country matches the machine country. A native datacenter
  address is still a datacenter address.
