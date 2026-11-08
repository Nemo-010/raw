# The IPv6 road is deterministic; the IPv4 pool is not

- **When:** 2026-10-24T15:05:00Z
- **Status:** corrected
- **Supersedes:** the claim that a Cloudflare egress draw lands in one of three ASNs at random, on every road
- **Superseded by:** the 24-draw and 30-draw runs of 2026-10-24 in this entry
- **Evidence:** the draw lists in this entry, with the RDAP holder of each address
- **Confidence:** measured

**What was claimed.** That Cloudflare's egress pool spans three ASN numbers and a
draw lands in one at random, so a rung-4 block is intermittent rather than total.
That was the corrected form of an earlier and worse claim that the transport
selected the ASN.

**What sharpens it.** A 24-draw run on 2026-10-24 returned **9 distinct IPv4
addresses, all AS13335**:

```
104.28.153.126  104.28.163.81  104.28.166.120  104.28.166.126  172.69.58.194
172.70.127.93   172.70.130.177 172.70.179.42   172.71.254.78     all AS13335
```

In a 30-draw set the AS14789 address `172.69.76.180` appeared once. So the IPv4
pool is roughly **97% AS13335**, and "three ASNs at random" overstated the spread
by implying a third of draws would land elsewhere.

**What is genuinely deterministic.** The IPv6 `fetch()` path returns
`2a06:98c0:3600::103` on every request, and RIPE puts that in
`2a06:98c0:3600::/48` → **AS132892 CLOUDFLARE**. Five consecutive reads returned
the same address. That is a fixed address in a different ASN number, reachable by
asking for a name with an AAAA record.

⭐ **So the honest form of the finding is this:** on IPv4 you cannot choose the ASN,
and you will almost always get AS13335. On IPv6 you get a different ASN every time,
by construction. If an upstream counts ASN numbers, the IPv6 road answers and the
IPv4 road does not. If it counts the organisation, neither helps, because all three
holders read "Cloudflare, Inc."

**Where the correction lives.** `docs/ip-proxy/README.md` §1 and
`docs/ip-proxy/techniques.md` §1. The operator's standalone playbook carries the
same correction and lives outside the corpus at
`.tmp/ip-proxy/exit-identity-playbook.md`, so it is not a tracked path.

⚠ **What would reopen it.** A run in which the IPv6 road returns more than one
address, or in which a named upstream answers over IPv6 and refuses over IPv4 for a
reason other than the ASN. Neither has been observed.
