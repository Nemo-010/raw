# ip-proxy

Where an exit identity comes from. A leased prefix, a per-address proxy, a
residential or mobile network, a VPN, a free list, a cloud that happens to sit in
a different ASN. The unit of sale in this topic is **an address**, or a prefix, or
a registration class. It is not a byte and it is not a path.

⭐ **The question:** which source of IP addresses lets a Cloudflare-Workers-hosted
service reach an upstream that refuses Cloudflare's own ranges, for free or for the
least money, and what does each source cost in identity, diversity and reliability?

⚠ **This topic is not `egress`.** `egress` buys a path and answers how much traffic
can leave. This topic buys an address and answers what the upstream sees, and
whether the address can be changed. A tunnel that happens to change the exit
address belongs in [`../egress/`](../egress/README.md); a vendor that sells 5,000
addresses belongs here.

## The answer, in one paragraph

A Cloudflare Worker **can** already reach the internet from a network that is not
Cloudflare's, and it has been measured doing it: a Proton WireGuard tunnel run
inside a Worker exits from `149.50.216.236`, which RIPE puts in **AS212238 CDNEXT
Datacamp**. So the question is not whether a non-Cloudflare exit exists. It is
whether the exit is any *better* than Cloudflare's, and AS212238 is a hosting ASN,
so it is not. That distinction runs through the whole topic: an address outside the
reader's control is worth nothing, and a *different* address is worth almost
nothing, because 102 relay Workers already draw a different address per
connection. **What is worth money is a different registration class, and the
market for it is mostly a labelling market.**

## The eight rungs, which decide every verdict

⛔ **A provider is not good or bad. It is a defence against a specific keying
strategy.** Every record carries its rung in `extras.rung`, and the topic is
organised by rung rather than by vendor type.

| # | what the upstream keys on | what defeats it | what does not | evidence here |
|---|---|---|---|---|
| 1 | the **session** | a fresh session | nothing else | refuted: OC-Free's bucket follows the egress, not the session id |
| 2 | a **single address** | any new address | a stable address | measured: OC-Free, `quotaByAddress: true` |
| 3 | a **subnet** (`/24` v4, `/64` or `/48` v6) | an address in a *different* subnet | a new address in the same subnet | ⚠ inferred, never caught in the wild |
| 4 | the **ASN** | a different network | every Cloudflare road, WARP, placement, renew | measured |
| 5 | the **registration class** | an ISP or eyeball-registered prefix | a datacenter prefix in a fresh ASN | ⚠ vendor-asserted; **4 of 8 published addresses fail a registry check** |
| 6 | the **account** | a new account | any wire-level change | measured: Meta, ZAI |
| 7 | the **client fingerprint** | a different client stack | any address change | measured: OC-Free, curl 403 vs bun 200 |
| 8 | **behaviour** | a different pattern | a different address | reported |

⭐ **What is measured in this topic and what is measured elsewhere are two
different things, and the table above says which.** Rungs 2, 4, 6 and 7 were
measured by a relay gateway's own instrumentation, in its VPN dashboard and its
experiment log, and rungs 6 and 7 have **no record in this topic**. ⛔ **Rungs 3, 5
and 8 have no measurement anywhere.**

## What the topic found, ranked by what a reader should do

### 1. The cheapest lever is not a purchase, and it is not a choice

⛔ **The transport does not select the ASN.** One address per transport found three
ASN numbers and suggested the transport selects the ASN. A paired 6-draw test on
2026-10-24 refutes that:

```
fetch()    172.71.254.79   172.70.127.94   104.28.166.120  ...   all AS13335
sockets    104.28.163.81   104.28.153.140  104.28.162.236  ...   all AS13335
```

`fetch()` returned `104.28.166.120`, which `cf-sockets` also returned. The two
transports draw from **one pool**, and the ASN is a property of the `/24` that pool
happened to hand out.

**What is true:** Cloudflare's egress pool spans at least three ASNs, all held by
Cloudflare, Inc.

| ASN | holder as RIPE prints it | where it was seen |
|---|---|---|
| **AS13335** | CLOUDFLARENET - Cloudflare, Inc. | both transports, most draws |
| **AS14789** | CLOUDFLARENET - Cloudflare, Inc. | `fetch()`, once in 30 draws |
| **AS132892** | CLOUDFLARE - Cloudflare, Inc. | the IPv6 `fetch()` path, `2a06:98c0:3600::/48` |

**What is not true:** that the IPv4 transports select the ASN. On IPv4 a draw lands
in one of them at random and neither the transport, the header, nor the colo
chooses it. ⭐ **The IPv6 road is the exception and it is the one lever here:**
`2a06:98c0:3600::103` is a fixed address in AS132892, the same every time.
Reproduce the refutation:

```bash
for i in 1 2 3 4 5 6; do
  sh scripts/broker/broker.sh fetch https://ipinfo.io/json | grep -o '"ip": *"[^"]*"'
  sh scripts/broker/broker.sh fetch https://ipinfo.io/json --egress cf-sockets | grep -o '"ip": *"[^"]*"'
done
curl -qsS "https://stat.ripe.net/data/prefix-overview/data.json?resource=104.28.166.120"
```

⭐ **The consequence is a different claim.** An upstream that counts ASN *numbers*
already sees a random draw from three networks rather than one, and no
configuration controls which. That is a reason a rung-4 block might be intermittent
rather than total. It is **not** a lever, and the rung-4 experiment is unrun.

⚠ **The IPv6 draw is bounded by the `/48`, not the `/128`.** Measured: 14 requests
produced 9 distinct `/128`s but only **7 distinct `/48`s**; 10 requests produced 9
and **6**. So the rotation ceiling is the `/48` count, which is the same shape as
the IPv4 finding of 9 addresses in 6 `/24`s.

### 2. Rung 5 is real, and half the vendors fail their own claim

⛔ **Eight published addresses, across five vendors. Four fail and four pass.**

| vendor | the address | registry says | claim |
|---|---|---|---|
| Decodo | `37.120.211.30` | **AS9009 M247 Europe** — hosting | ❌ fails |
| Decodo | `90.135.104.218` | AS1257 Tele2 Sverige — ISP | ✅ passes |
| NovixLink (NTT line) | `192.220.114.2` | AS2914 NTT America — transit carrier | ❌ fails |
| NovixLink (GTT line) | `216.36.86.2` | AS3257 GTT-BACKBONE — transit carrier | ❌ fails |
| NovixLink (Cox line) | `24.120.4.1` | **AS22773 Cox Communications** — ISP | ✅ passes |
| AnchoredIP | `194.0.109.1` | ASSIGNED PA, an individual in Kazakhstan | ❌ fails |
| RareCloud | its published test IP | **AS39347 SELL-07INTERNET-RO** — ISP | ✅ passes |
| VPC.KR | `112.169.175.10` | **AS4766 KORNET-KR** Korea Telecom | ✅ passes |

⭐ **The denominator matters and the count is small.** It is eight addresses, not
eight vendors: Decodo contributes two and NovixLink three. ⚠ **Two of the four
passes are single product lines inside a vendor whose other lines fail**, so a
buyer who checks nothing at Decodo gets the M247 address and a buyer who checks
nothing at NovixLink gets a carrier.

⚠ **A separate survey of six VPS hosts found the same 2-of-6 pass rate**, on a
different population that shares three names with this table. It is in
[`free/cloud-egress.md`](free/cloud-egress.md) and it is not the same measurement.

### 3. Size is not diversity, and the `/48` claim is false in a specific way

The question is whether IPYE's free `/48` gets around the technique that blocks
IPv6 rotation. It does not, and the reason is measured:

- ⛔ **Meta's own measurement says a `/48` is the bucketing unit.** Li & Freeman,
  *Towards A User-Level Understanding of IPv6 Behavior*, IMC 2020, on Facebook's
  own traffic: *"IPv6 /48 subnets appeared most similar to IPv4 addresses in their
  distribution of user population sizes, so existing rate limiting logic applied to
  IPv4 addresses could potentially be translated to IPv6 /48 prefixes."* A `/48`
  lands exactly on the unit the defender would pick.
- ⭐ **The paper's blocklisting recommendation is `/64`, not `/48`**: *"either the
  full IPv6 address or /64 subnets are most suitable for IP-based security
  applications"*. A `/48` is the *coarser* of the two, so a `/48` is strictly worse
  than rotating `/64`s inside it, which is what Cloudflare already does.
- ⚠ **A `/48` is not a residential delegation.** APNIC Labs measures `/48` at 2% of
  end-site prefixes; `/64` is 57%, `/56` 20%, `/60` 21%. A real home connection is
  usually a `/56` or `/60`, which is *smaller*.
- ⛔ **The free `/48` is not the ISP product.** The ISP-registered class claim is
  attached to a **USD 1,600/month** bundle. The free `/48` is a datacenter
  allocation, and announcing it needs an ASN the holder does not have.

Full reasoning in [`free/prefix-leases.md`](free/prefix-leases.md).

### 4. Free sources decay in minutes, and that is the finding

Measured here on 2026-10-24, on real samples, not list sizes:

| list | t0 payload | +22 min | verdict |
|---|---|---|---|
| `monosans/proxy-list` | 35 of 100 | 21 of 100 | 60% survival in 22 minutes |
| ProxyScrape | 32 of 100 | 30 of 100 at +5 min | dies slower, no ASN field |
| `openproxylist.xyz` | 12 of 60 | — | worst of the metadata-free lists |
| `TheSpeedX/PROXY-List` | 8 of 100 | 8 of 100 | 92 of 100 dead weight |

⭐ **The honest form of the decay is an intersection, not a ratio.** Of the 35
`monosans` lines that carried a payload at t0, **10 still did 22 minutes later**.
The 21-of-100 second yield is a different set of addresses; 21/35 is a ratio of
yields, not a survival rate. Only `monosans` ships a per-proxy ASN, so it is the
only free list where the registration class is knowable before spending a request,
and 24 of 59 measured exits from it sat in ISP or mobile ASNs.

### 5. The unit of sale is the address, and per-GB pricing is the retail tier

At the measured volume the arithmetic decides it. 599,000 requests a month at
roughly 75 KB each is **about 41.8 GiB a month (45 GB decimal)** (`inferred`).

| the shape | 41.8 GiB costs | what is offered |
|---|---|---|
| rotating residential at USD 0.80/GB | **USD 36** | one address at a time from a shared pool, rung 2 |
| rotating residential at Bright Data's USD 4/GB | USD 180 | the same, plus a video KYC |
| **static ISP at Webshare USD 0.30/IP** | **USD 6 for 20 addresses** | 20 addresses held for a month, unlimited bytes, rung 5 |
| mobile per-proxy at Proxidize | USD 59 | one carrier address, and a national-ID check |

⛔ **Every price in this topic is per distinct address-class per month. A
per-gigabyte price is reported only to be converted, never to be compared.**

## The documents

| document | the class | what it answers |
|---|---|---|
| [`free/prefix-leases.md`](free/prefix-leases.md) | prefixes and subnet leases | does a bigger prefix defeat rotation, and what does a `/24` cost |
| [`free/free-lists.md`](free/free-lists.md) | public proxy lists and volunteer relays | what costs nothing, and what survives an hour |
| [`free/cloud-egress.md`](free/cloud-egress.md) | clouds and VPS as exit sources | which free tier gives an address, and which ASN it is in |
| [`paid/isp-proxies.md`](paid/isp-proxies.md) | per-address ISP proxies | the rung-5 market, priced per address, and who fails a registry check |
| [`paid/residential-and-mobile.md`](paid/residential-and-mobile.md) | residential and mobile networks | what an eyeball exit costs at 41.8 GiB, and what the identity wall is |
| [`paid/vpn-exits.md`](paid/vpn-exits.md) | VPN subscriptions | how many distinct ASNs a subscription actually buys |
| [`techniques.md`](techniques.md) | technique, not product | which moves change the address, the subnet, the ASN or the class |
| [`fingerprint.md`](fingerprint.md) | the client stack | rung 7, and why it is often the real answer |
| [`watchlist.md`](watchlist.md) | the reading list | which sources publish other providers, and what a diff of each can establish |

## The constraints that bind

| constraint | where it bites | the number |
|---|---|---|
| `write-gated` | a free prefix with no ASN | IPYE's `/48` needs an origin ASN, and the shared one is USD 300/yr |
| `retention-clamped` | prepaid credits and idle VMs | SOAX credits expire in 60 days; Oracle reclaims an idle VM at 7 days |
| `volume-quota` | every per-GB product | 250 GB included on Webshare, 500 GB on NovixLink Lite |
| `per-ip-shaping` | every static address | Proxidize's 50 GB fair-use threshold per proxy per month |
| `request-rate` | every target blocklist | Oxylabs refuses whole target classes by policy |
| `none` | the honest answer for several | Mullvad meters nothing; IPRoyal's ISP product meters nothing |

## Dead ends

- **NetNut is seized.** An FBI seizure notice on every path, and Alarum's own SEC
  exhibit confirms it, 2026-07-02.
- **LunaProxy and PIA S5 are gone.** NXDOMAIN, and LunaProxy is named in Google's
  IPIDEA takedown of 2026-01-28. `911.re` is seized.
- **Bright Data no longer sells mobile proxies.** Withdrawn April 2026.
- **A bigger prefix is not more diversity.** A `/24` is one rung-3 unit, whatever
  it costs.
- **Public proxy lists are not a pool.** Of 35 pre-verified proxies that worked,
  only 10 still worked 22 minutes later.
- **WARP does not diversify.** Its exit is Cloudflare's own `104.28.0.0/16`.

## What this topic does not do

It does not build a router, write a legal view, recommend self-hosting, or price a
byte.

## Records that no other document names

This list holds each `measured` or `documented` record of this topic that no other
document of `docs/` names.

<!-- generated:start topic=ip-proxy kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `kookeey-residential-and-isp` | kookeey | trial-only | documented |
| `novproxy` | Novproxy | trial-only | documented |
| `nymvpn-exits` | NymVPN | trial-only | documented |
| `trust-zone-exits` | Trust.Zone | trial-only | documented |
| `zooproxy-isp-proxy` | ZooProxy | trial-only | documented |
<!-- generated:end -->
