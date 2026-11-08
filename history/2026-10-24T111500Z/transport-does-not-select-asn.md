# The transport does not select the ASN

- **When:** 2026-10-24T11:15:00Z
- **Status:** corrected
- **Supersedes:** the claim that each Cloudflare transport (`fetch()`, raw `connect()`, IPv6 `fetch()`) exits from its own ASN
- **Superseded by:** the paired draws of 2026-10-24 in this entry, and `history/2026-10-24T150500Z/ipv6-road-is-deterministic.md`
- **Evidence:** the draw table in this entry, one vantage point, 2026-10-24
- **Confidence:** measured

**What was claimed.** That Cloudflare's transports each exit from a different ASN,
so switching transport was a free lever against a gate counting ASNs. The evidence
was one address per transport:

| transport | one draw | ASN |
| --- | --- | --- |
| `fetch()` | `172.69.76.180` | AS14789 |
| raw `connect()` | `104.28.155.104` | AS13335 |
| IPv6 `fetch()` | `2a06:98c0:3600::103` | AS132892 |

**What took it away.** A paired 6-draw test on 2026-10-24, from one vantage point,
alternating the two transports:

```text
fetch()    172.71.254.79   172.70.127.94   104.28.166.120   all AS13335
sockets    104.28.163.81   104.28.153.140  104.28.162.236   all AS13335
```

`fetch()` returned `104.28.166.120`, which `cf-sockets` also returned in the same
run. The two transports draw from **one pool**. RIPE resolves every one of the
twelve addresses above to AS13335. In a 30-draw set the AS14789 address appeared
once, from plain `fetch()`.

So the ASN is a property of the `/24` the pool happened to hand out, not of the
transport. The first pass generalised a pool draw into a routing property, which is
the error `METHODOLOGY.md` §2.3 names: the explanation fit because nobody kept
looking.

**What is true now.** Cloudflare's egress pool spans at least three ASN numbers, all
held by Cloudflare, Inc.:

| ASN | holder | where it was seen |
| --- | --- | --- |
| AS13335 | CLOUDFLARENET - Cloudflare, Inc. | both transports, most draws |
| AS14789 | CLOUDFLARENET - Cloudflare, Inc. | `fetch()`, once in 30 draws |
| AS132892 | CLOUDFLARE - Cloudflare, Inc. | the IPv6 `fetch()` path |

An upstream counting ASN numbers therefore sees a **random draw** from three
networks rather than one, and the gateway controls neither the draw nor the choice.
That makes a rung-4 block more likely to be intermittent than total. It is not a
lever, and the rung-4 experiment is still unrun.

**Where the correction lives.** `docs/ip-proxy/README.md` §1 and
`docs/ip-proxy/techniques.md` §1 both carry the refutation and the reproduce
command. `BRIEF.md` §3.9 no longer states the lever.

⚠ **What would reopen it.** A paired test at one colo in which `fetch()` returns
AS14789 across many draws while `connect()` never does. The 12 paired draws here
show the opposite, with overlapping addresses.
