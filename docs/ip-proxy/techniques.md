# Technique, not product

Which moves change the **address**, the **subnet**, the **ASN**, or the
**registration class**. Four different things, and almost every technique changes
only the first.

**The question:** what can move the exit without buying anything?

**The answer:** Cloudflare's own transports already provide **two ASN numbers** for
free. Nothing else in this document beats that for cost, and nothing here clears the
registration class.

---

## The four things a move can change

| the move | address | subnet | ASN | class | cost |
|---|---|---|---|---|---|
| `fetch()` instead of `connect()` | ✅ | ✅ | ✅ **AS14789 vs AS13335** | ❌ | **free** |
| a new relay in a new colo | ✅ | ✅ | ❌ | ❌ | free, already deployed |
| a renew or a re-placement | ❌ | ❌ | ❌ | ❌ | free, and measured to do nothing |
| NAT64 / DNS64 | ✅ | ✅ | ✅ (to the NAT64 gateway's ASN) | ❌ | free |
| an IPv6 tunnel broker | ✅ | ✅ | ✅ (to the broker's ASN) | ❌ | free |
| a CDN in front of the origin | ✅ | ✅ | ✅ | ❌ | free |
| a VPN exit | ✅ | ✅ | ✅ | ⚠ sometimes | subscription |
| a leased ISP prefix | ✅ | ✅ | ⚠ maybe | ⚠ **asserted, not measured** | USD 0.27 to USD 1,600/mo |

## 1. Cloudflare's pool spans three ASNs, and the draw cannot be chosen

⛔ **The transport does not select the ASN.** One address per transport produced
three ASN numbers and looked like a lever. A paired 6-draw test shows both
transports drawing from one pool, with `104.28.166.120` returned by both:

```
fetch()    172.71.254.79   172.70.127.94   104.28.166.120   all AS13335
sockets    104.28.163.81   104.28.153.140  104.28.162.236   all AS13335
```

| ASN | holder | where it was seen |
|---|---|---|
| **AS13335** | CLOUDFLARENET - Cloudflare, Inc. | both transports; 9 of 9 distinct addresses in a 24-draw run |
| **AS14789** | CLOUDFLARENET - Cloudflare, Inc. | `fetch()`, once in 30 draws |
| **AS132892** | CLOUDFLARE - Cloudflare, Inc. | IPv6 `fetch()`, `2a06:98c0:3600::/48`, **the same address every time** |

⭐ **The IPv4 pool is roughly 97% AS13335 and the draw cannot be chosen. The IPv6
road is different: it is a fixed address in a different ASN number, so it is
the one deterministic move available.** If an upstream counts ASN numbers, that
move answers. If it counts the organisation, none of the three helps, because all
three holders read "Cloudflare, Inc.".

```bash
for i in 1 2 3 4 5 6; do
  curl -qsS "https://fetch.web.pkgforge.dev/https://ipinfo.io/json" | grep -o '"ip":"[^"]*"'
  curl -qsS "https://fetch.web.pkgforge.dev/https://ipinfo.io/json?__egress=cf-sockets" | grep -o '"ip":"[^"]*"'
done
curl -qsS "https://stat.ripe.net/data/prefix-overview/data.json?resource=104.28.166.120"
```

⛔ **This is not rung 5 and must never be sold as it.** All three holders read
"Cloudflare, Inc.".

⚠ **The IPv6 draw is bounded by the `/48`, not the `/128`.** Measured: 14 requests
produced 9 distinct `/128`s but only **7 distinct `/48`s**; 10 requests produced 9
and **6**. The rotation ceiling is the `/48` count, the same shape as the IPv4
finding of 9 addresses in 6 `/24`s.

## 2. What Cloudflare's own products do and do not give

| product | gives a Worker a non-Cloudflare ASN? | the sentence |
|---|---|---|
| **Dedicated Egress IPs** | ❌ no | *"Only available as an add-on to Zero Trust Enterprise plans"*, and it applies to Gateway-proxied device traffic, not a Worker's `fetch()` |
| **BYOIP** | ⚠ **unverified** | the customer's own registry allocation, so possibly; no page states the origin AS |
| **Containers outbound** | ❌ no | a policy layer: `enableInternet`, `allowedHosts`, `deniedHosts`; no address, no ASN |
| **Containers egress** | ❌ no | USD 0.025/GB in North America and Europe, 1 TB included on Workers Paid |
| **Spectrum** | ❌ no | proxies inbound traffic; the origin still dials out |
| **WARP / MASQUE** | ❌ no | ⛔ exit is Cloudflare's own `104.28.0.0/16`; measured, and it does not diversify |

⭐ **The one open question is BYOIP.** If a Worker's egress can be announced from a
prefix the customer owns, rung 5 becomes purchasable inside Cloudflare at a known
price. No Cloudflare page states the origin AS for BYOIP egress, and one sales
reply would settle it.

## 3. NAT64 and tunnel brokers

Both move the exit to a different ASN, and neither moves the class.

| the technique | the exit ASN | what it buys |
|---|---|---|
| NAT64/DNS64 via Hetzner | **AS24940** | a datacenter ASN, measured in a VPN client dashboard |
| NAT64 via Trex | AS29432, `ASSIGNED PI` + `LEGACY` | the only free NAT64 whose registry type is not leased hosting space |
| Hurricane Electric tunnelbroker | AS6939 | a transit carrier |
| Route64 IPv6 | AS212895 | its IPv4 blocks read `IPXO` / "Private Customer" in RDAP |

⛔ **A tunnel broker does not make an exit residential.** A broker is a network
operator; its addresses are registered to it, not to homes.

⚠ **A NAT64 test must use a hostname, not a literal.** The broker refuses every
IPv6 literal outright with Cloudflare error 1003 (`platform-refused`), on a NAT64
synthetic address and on a plain Google IPv6 address alike, while an IPv4 literal
to the same route returned 200. So a failed IPv6-literal request is evidence about
a literal, not about NAT64.

## 4. What is measured to do nothing

| the move | why it fails | the measurement |
|---|---|---|
| a relay renew | the colo decides the blocks | 6 reads with a renew, 6 without, same spread |
| more relays in one colo | they share the colo's blocks | stated in the relay gateway's notes |
| a redraw loop inside one invocation | median 0 new `/64`s per group of four | measured in two colos |
| a Durable-Object fan-out | the ceilings are invocations, not sockets | costed at ~391,000 GB-s/month |
| `placement.host` | the colo changes, the stamps and the network do not | measured |
| a second Cloudflare zone | changes `Cf-Worker`, not the ASN | AS14789 on both zones, 6 runs |
| WARP | its exit is Cloudflare's | 16 MiB carried, `104.28.0.0/16` |

## 5. The technique that is not about the address at all

⭐ **Sometimes the block is the client, not the network.** One case was measured
where the same bytes were refused from `curl`/Schannel and answered from `bun`.
That is the TLS ClientHello, not the IP. That is rung 7, it is a different
document, and [`fingerprint.md`](fingerprint.md) is where it lives.

⛔ **Buying addresses to fix a fingerprint problem buys nothing.**

## The order to try things in

1. **Switch transport.** Free, and it changes the ASN number. One header.
2. **Pin a relay in a colo the upstream has not seen.** Free, already deployed.
3. **Try a fingerprint profile.** Free to test.
4. **Buy one day of a per-address ISP proxy.** USD 1.80, and it settles whether
   the class claim survives a registry check.
5. **Buy a VPN subscription.** USD 39/yr for 58 ASNs.
6. **Only then** consider a prefix lease or a residential month.

⚠ **Steps 1 to 3 cost nothing and answer more than steps 4 to 6.** Starting at step
5 skips the three cheapest tests in the topic.
