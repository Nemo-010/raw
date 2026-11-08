# Free lists and volunteer relays

The class that costs nothing: public proxy lists, volunteer VPN relays, and the
free tiers of commercial VPNs. Every one of them is a rung-2 answer at best, and
most of them decay within minutes.

**The question:** what costs nothing, and what survives?

**The answer:** two free sources are worth anything, and neither is a list. VPN
Gate's volunteer relays are the strongest free source of **carrier-registered**
exits measured in this topic: 35 distinct ASNs led by Korea Telecom, SoftBank, KDDI
and LG Powercomm. `monosans/proxy-list` is the only list that ships a per-proxy
ASN, so it is the only one where the registration class is knowable before
spending a request. Everything else is a number that measures the list, not the
network.

---

## The survival measurements

⛔ **A list's size is not a finding. The survival rate is.** These were measured on
2026-10-24 on stratified random samples, by dialling each proxy and requiring a
full HTTPS GET of `https://ip.pkgforge.dev/json` with a parseable `ip` field.

| list | sample | handshake | carried a payload | re-run | verdict |
|---|---|---|---|---|---|
| `monosans/proxy-list` | 100 | 38 | **35** (35%) | **21** at +22 min | the only one worth using |
| ProxyScrape | 100 | 38 | 32 (32%) | 30 at +5 min | dies slower, no ASN field |
| `openproxylist.xyz` | 60 | 14 | 12 (20%) | — | worst of the metadata-free lists |
| `TheSpeedX/PROXY-List` | 100 | 17 | **8** (8%) | 8 at +23 min | 92 of 100 are dead weight |

⭐ **The decay is the finding, and the honest form of it is a survival count, not a
ratio.** The same 100 `monosans` lines went from 35 working to 21 working in 22
minutes. ⚠ **21 over 35 is 60%, and that 60% is the ratio of two yields, not the
survival of the same addresses.** Intersected on host and port, **10 of the 35 that
worked at the first check worked at the second, which is 29%.**

> **So of 100 pre-verified proxies, 35 carried a payload at t0 and 10 of those
> same 35 still did 22 minutes later.**

⛔ **Do not extrapolate this to a list size.** A 10,000-line list is not 10,000
tested proxies; the sample here was 100 lines drawn stratified from 1,751. The
measured facts are the two yields and the 10-of-35 intersection, and they are
enough: **a list is a retry budget, not a pool.**

### Why the survival rate differs by 4×

`monosans` describes its own pipeline: *"Every proxy here was verified minutes
before the last commit by proxy-scraper-checker. To make the list, a proxy had to
fetch a real URL in full, so proxies that connect and then stall never appear."*
`TheSpeedX` describes nothing. **A list that pre-verifies with a real fetch is four
times better than a raw scrape**, and that is the only quality signal available
before testing.

### What the survivors are

| list | the exits that worked | registration |
|---|---|---|
| `TheSpeedX` | 8 of 8 | **all datacenter**: OVH AS16276 ×2, Contabo AS51167, DigitalOcean AS14061, Microsoft AS8075, GoDaddy AS26496/AS398101, Biznet AS17451 |
| `monosans` | 59 distinct, 45 ASNs, 58 prefixes | **24 of 59 in ISP or mobile ASNs**: China Mobile AS9808, Viettel AS7552 ×5, Cox AS22773 ×6, Biznet AS17451, TATTELECOM AS28840, Superonline AS34984 |

⛔ **So the free lists do reach rung-5 *classes*. Nothing here shows that a
rung-5 class defeats a rung-5 gate.** That test has not been run. What has been run
is the registration lookup, and it says a free list can hand out a Cox or a China
Mobile address for nothing. Whether that address is worth more than a Cloudflare
one at the upstream is `unverified`.

---

## VPN Gate: the strongest free source found

| | |
|---|---|
| what it is | a volunteer relay network, public and free, no registration |
| measured exit | AS8369 INTERSVYAZ |
| payload | **16 MiB crossed in 918 s** (measured in a VPN client dashboard) |
| exit ASNs | **35 distinct**, led by Korea Telecom, SoftBank, KDDI, LG Powercomm |
| identity cost | **anonymous** |
| the catch | the transit TLS terminates at a volunteer |

⭐ **It is the only free source here whose exits are mostly consumer
carrier ASNs.** That is rung 5 for nothing. It is also the slowest way measured, at
918 seconds for 16 MiB.

⚠ **The transit TLS terminating at a volunteer is a reliability fact.** It means
the path depends on one person's machine staying up, and it is recorded in
`reliability_note` rather than argued about.

---

## The commercial VPN free tiers

| provider | the free tier | what it gives |
|---|---|---|
| Proton VPN | 1 device, 10 randomly selected countries | a real exit, but the paid exit is AS212238, a hosting ASN |
| Windscribe | 2 to 10 GB/month, no card | the same fleet as its paid tier, capped |
| Cloudflare WARP | free | ⛔ **does not diversify**: exit is Cloudflare's own `104.28.0.0/16` |
| Hide.me | 10 GB/month, one device | ⚠ its own pages disagree: one says "we never cap your data" |

⚠ **Hide.me's free cap is unresolved.** Two pages on the same site, both read
2026-10-24, state "we never cap your data" and "one device and 10 GB per month".
Settling it needs a signup and a byte count.

---

## The providers

<!-- generated:start topic=ip-proxy kind=provider verdict=dead sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JibaoProxy (极豹代理) | 500 MB of dynamic residential traffic on re... | dead | inferred | not applicable: an address or a... | not applicable: a pro... | email | `dossier/ip-proxy/jibaoproxy.json` |
| JibaoProxy | The site no longer serves: the home page an... | dead | measured | not applicable: an address or a... | not applicable: the s... | email | `dossier/ip-proxy/jibaoproxy-residential.json` |
| LunaProxy, PIA S5 Proxy a... | No live offer. lunaproxy.com and piaproxy.c... | dead | documented | not applicable: an address, not... | not applicable: an ad... | anonymous | `dossier/ip-proxy/lunaproxy-and-pia-s5.json` |
| NetNut | nothing reachable: both https://netnut.io/... | dead | documented | not applicable: an address, not... | not applicable: a liv... | email | `dossier/ip-proxy/netnut-seized.json` |
| openproxylist.xyz | Free and registration-free: the front page... | dead | measured | not applicable: an address, not... | not applicable: a lis... | anonymous | `dossier/ip-proxy/openproxylist-xyz.json` |
| ProxyScrape | Free, no account: the page states 20,000+ l... | dead | measured | not applicable: an address, not... | not applicable: a liv... | anonymous | `dossier/ip-proxy/proxyscrape-free-list.json` |
<!-- generated:end -->

## What kills this class

| killer | the number |
|---|---|
| decay | of 35 that worked, **10** still worked 22 minutes later |
| datacenter exits | 8 of 8 survivors from the raw scrape were hosting ASNs |
| no ASN metadata | only 1 of the 4 lists shows the class before spending a request |
| the volunteer | one person's machine, and the TLS terminates there |
| the free tier cap | Windscribe 2 to 10 GB/month against a 41.8 GiB workload |

## The one thing worth doing with a free list

⭐ **Use `monosans` as an ASN filter, not as a pool.** It ships `proxies.json` with
a per-proxy ASN, so a request can be aimed at a specific registration class instead
of sampling blind. That is the only free path to a mobile-registered exit
(AS9808) that was measured working here.

⚠ **Do not design a service against it.** Two of ten survivors held for 12 to 25
consecutive requests in the soak, which is a retry budget rather than a pool.
