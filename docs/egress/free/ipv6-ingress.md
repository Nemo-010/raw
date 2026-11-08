# A routed IPv6 prefix is a free public address with every port open

An IPv6 tunnel broker routes a prefix to the reader's endpoint. Every address in
that prefix is public, every port on it is reachable, and there is no NAT, no port
forward and, at the brokers listed here, no byte meter.

⭐ **That is the cleanest free ingress shape in the topic: one tunnel, a routed
prefix, and a WireGuard listener on any address in it.** It is also the shape with
the narrowest audience, because a reader needs IPv6 to reach it.

The question: **which brokers still answer in 2026, which deliver over WireGuard,
and how large is the prefix?**

| broker | prefix | transport | volume | identity | verdict |
| --- | --- | --- | --- | --- | --- |
| ROUTE64 | `/56` | WireGuard, GRE, IP6IP, 6in4 | no meter, 200 Mbit/s design | email | `qualifies` |
| Tahio | `/48` | SIT, GRE, WireGuard | no meter, 50 Mbit/s | email | `qualifies-with-caveat` |
| tunnel64 | `/64` per tunnel, up to 5 | WireGuard | no quota, 100 Mbit/s | email | `qualifies-with-caveat` |
| GhostTunnel | `/64` | SIT, GRE, WireGuard | none published | email | `qualifies-with-caveat` |
| 6Project | a routed prefix | WireGuard, GRE, 6in4, IPIP, OpenVPN | none published | email | `qualifies-with-caveat` |
| NetAssist | a routed prefix | 6in4 | "free of charge", no figure | email | `qualifies-with-caveat` |
| Hurricane Electric | `/48` | 6in4, GRE | no quota | email | `qualifies-with-caveat` |
| ip4market | a prefix | 6in4 | free, no meter | email | `qualifies-with-caveat` |
| GetIP | a WireGuard peer | WireGuard | 100 GB/month | email | `fails-quota` |
| IPv6rs | 5 static tunnels | WireGuard | unmetered, paid | card | `paid-only` |
| Karabro | `/60` | WireGuard | 10 Mbit/s fair use | Swedish identity | `fails-identity` |
| BGPTunnel | transit, not a prefix | GRE | free to networks | an AS number | `fails-identity` |

## ROUTE64

The best-documented free broker found. A non-profit on AS212895 that routes a
`/56` to an endpoint over WireGuard, GRE, IP6IP or 6in4, with a self-service
portal that generates the configuration (`documented`, read 2026-10-23). "Traffic
is not metered" and the service is designed for 200 Mbit/s, which is 2.16 TB/day.

⚠ **The prefix is IPv6, so a reader without IPv6 cannot reach it.** That is a
property of the reader and not a failure of the broker, and the record says it in
the same sentence as the number. 200 Mbit/s is 66 times the rate a 1 TiB month
needs, so nothing binds at the test volume.

Evidence: `route64.org/en` (read 2026-10-23); `dossier/egress/route64-org.json`.

## Tahio, tunnel64 and GhostTunnel

Three smaller brokers with the same shape and less documentation. Tahio routes a
`/48` over SIT, GRE or WireGuard with a 50 Mbit/s cap. tunnel64 gives a `/64` per
tunnel, up to five, at 100 Mbit/s, with dyndns2 updates and reverse DNS. GhostTunnel
routes a `/64` over SIT, GRE or WireGuard and says "free forever" (`documented`,
read 2026-10-23, each).

⚠ **A single-operator broker is a service with a half-life.** tunnelbroker.li
closed and route48 now redirects to BGPTunnel; both were listed as active by a
directory in the same week. The record keeps the shape and the date, and a reader
should re-check before depending on one.

## 6Project and NetAssist

6Project offers five transports including WireGuard, with no traffic allowance on
any page read (`inferred`). NetAssist offers a free 6in4 tunnel and no published
quota (`reported`). Both need the request form, and 6Project deprovisions a prefix
after a grace period if it is not renewed.

## Hurricane Electric

A free 6in4 tunnel and a routed `/48`, documented in
[`inbound-and-address.md`](inbound-and-address.md). It is
the oldest broker still answering and it carries no WireGuard option.

## GetIP

A free WireGuard peer whose allowance is 100 GB/month (`documented`, read
2026-10-23). That is 0.09 TiB, about one eleventh of the test, and the overage is
sold per gigabyte. It is the clearest example of a WireGuard-native offer that
fails on volume rather than on mechanism.

## The identity gates

Karabro (the former tunnelbroker.se) offers a `/60` at 10 Mbit/s fair use and
requires a Swedish identity. BGPTunnel offers GRE transit to networks with an AS
number, which is `institution`.

⛔ **Both are real capacity and both are unreachable without a Swedish identity or an AS
number.** The record states the ceiling and the gate in one sentence.

## What is dead

- **Freenet6 / gogoNET**: closed in 2016. The domain still returns HTTP 200 with
  an empty body, which is the status-code trap in its purest form.
- **tunnelbroker.li**: closing, and its own page points at BGPTunnel.
- **route48.org**: redirects to BGPTunnel; the independent broker is gone.
- **SixXS**: defunct for years and still named in old lists.

## Chaining

**The prefix chain.** `ROUTE64 /56 -> wg-quick on the endpoint -> every port and
protocol on a routed address`. The scarce link is IPv6 reachability at the reader.

**The dual-stack chain.** `ROUTE64 /56 -> a dual-stack front -> the origin`. The
scarce link is the front, because a reader without IPv6 never reaches the prefix
directly. That front is a paid CDN or a second machine.

## The records

`dossier/egress/route64-org.json`, `tahio-tunnelbroker.json`, `tunnel64.json`,
`ghosttunnel-cushell.json`, `6project-org.json`, `netassist-tunnelbroker.json`,
`he-tunnelbroker.json`, `ip4market.json`, `getip-online.json`, `ipv6rs.json`,
`karabro-tunnelbroker-se.json`, `bgptunnel.json`, `route48-org.json`,
`tunnelbroker-li.json`, `freenet6.json`.

⚠ **No prefix was routed.** Every row is a page read, and the first measurement that
would raise one is a `ping6` across the tunnel.
