# How do I get a stable address with no static IP?

Two different problems, and they are easy to confuse. One is a **name** that
resolves to a machine whose address changes. The other is an **address reachable
from outside** when nothing inbound can be opened. A tunnel solves both for HTTP
and solves neither for arbitrary TCP.

⭐ The answer for a name is a domain plus Cloudflare's proxy and Tunnel, and the only
paid element is the domain. The answer for an address with open ports is that none
is free. The free approximation is an IPv6 /48 over a 6in4 tunnel, which works only
for clients that already have IPv6.

Sorted by what the reader is trying to reach.

| provider | free tier | what binds | identity | verdict |
| --- | --- | --- | --- | --- |
| Cloudflare Tunnel (named) | unmetered transit on any plan | `write-gated`: a domain on Cloudflare nameservers | email | `qualifies-with-caveat` |
| Hurricane Electric tunnelbroker | a 6in4 tunnel and a routed /48 | `write-gated`: the endpoint must accept protocol 41 | email | `qualifies-with-caveat` |
| GetAStatic | none; USD 2/month for a dedicated IPv4 | `per-ip-shaping`: the 100 GB/month allowance | card | `paid-only` |

## Cloudflare Tunnel (named)

An outbound-only connection from the origin to Cloudflare, with the hostname served
from Cloudflare's edge. Transit is unmetered on every plan, the account limits are
1,000 tunnels and 50,000 routes, and no bandwidth figure is listed anywhere among
them (`documented`, 2026-10-22).

The gate is the domain. Tunnel requires the hostname's zone to be on Cloudflare
nameservers, so a free DNS provider such as deSEC does not substitute: the chain is
Cloudflare-DNS-or-nothing for this shape. The domain is about USD 10.46 a year at
Cloudflare Registrar and it is the only paid element.

The limits that fail rather than shape are the 100 MB proxied request body on Free
and the 125 s proxy read timeout (`documented`, 2026-10-22).

Evidence: `developers.cloudflare.com/cloudflare-one/account-limits/` and
`developers.cloudflare.com/fundamentals/reference/connection-limits/` (read
2026-10-22); `dossier/egress/cloudflare-tunnel.json`.

Verdict: `qualifies-with-caveat`. The cheapest stable HTTP address found, at the
price of a domain.

## Hurricane Electric tunnelbroker

A free 6in4 tunnel and a routed /48, so the machine gets a whole public IPv6
prefix with no NAT and no port forwarding (`documented`, 2026-10-22). The endpoint
must answer ICMP and accept protocol 41, which is the gate.

⚠ **Protocol 41 is not a `write-gated` constraint.** `write-gated` is a curator, a
review, a build recipe or a phone PIN, which is a queue with a person in it.
Protocol 41 is a network capability the reader's ISP either passes or does not, and
no person approves anything. The requirement is real and none of the seven kinds
names it, so the record carries it in `limits_note` with `binding: none`.

This is the free answer to a static address rather than to capacity. Its limit is
that only clients with IPv6 can reach it, which excludes most of the internet for
the serving workload this topic measures.

The site served an incomplete TLS chain on 2026-10-22: `openssl s_client` reports
"unable to get local issuer certificate", the chain names only
`CN=tunnelbroker.net`, and `curl` exits 35 `CRYPT_E_REVOKED` without `-k`
(`measured`, 2026-10-22). The service is reachable and the certificate path is
broken, which is worth knowing before automating against it.

Evidence: `tunnelbroker.net/` and `dossier/egress/he-tunnelbroker.json`.

Verdict: `qualifies-with-caveat`. Throughput was not measured.

## GetAStatic

USD 2/month for a dedicated US IPv4 with 100 GB of transfer and 20 Mbit/s
(`documented`, 2026-10-22). 100 GB/month is 3.3 GB/day and 20 Mbit/s would be
216 GB/day, so the quota binds and the rate does not.

⚠ **The 100 GB is a monthly byte allowance and not a per-object cap.** The number
lives in `egress.free_allowance` and `binding` names `volume-quota`, the kind for a
byte allowance over a period counted per account.

Evidence: `getastatic.com/pricing` (read 2026-10-22);
`dossier/egress/getastatic.json`.

Verdict: `paid-only`. Recorded because no free static IPv4 exists and a reader will
look for one.

## What did not work

- **Free static IPv4**: none exists. Every result was USD 2 to 15 per month
  (GetAStatic, Stayport, portmap.io), and `portmap.io/pricing` and
  `stayport.io/pricing` both returned 404 on 2026-10-22.
- **A free DNS provider behind a tunnel**: deSEC and similar are free and are not
  enough, because Cloudflare Tunnel requires Cloudflare-authoritative DNS.
- **Hurricane Electric as a general serving path**: IPv6 only.
- **`tunnelto.dev/pricing`**: 404 as a standalone path. The pricing is on the
  landing page and the product is live, so a 404 on a `/pricing` path is not evidence
  that a product is dead.

## Chaining

**The name chain.** `domain at Cloudflare Registrar -> the zone on Cloudflare
nameservers -> a named Tunnel -> the origin`. The scarce link is the domain, and
every other element is free with no byte meter.

**The address chain.** `he.net tunnelbroker /48 -> a dual-stack front -> the
origin`. The scarce link is the front, because IPv6-only reachability covers a
minority of clients and a dual-stack front is a paid CDN or a second machine.
