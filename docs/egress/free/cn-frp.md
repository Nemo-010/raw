# Public frp relays and the Chinese NAT-traversal panels

A public frp relay is a server its operator opens to strangers: a caller runs `frpc`,
connects with a shared token, and the relay forwards a port back. `frp`
carries TCP, UDP, HTTP and HTTPS, so a public relay is a free UDP ingress
provider with no account at all.

This is the largest free UDP surface found in the topic and the least durable. It
is one operator's server, offered without a contract, and several of the panels
fund it with a daily check-in rather than a subscription.

The question: **which of these still answer, which carry UDP, and which require
an identity a registrant cannot produce?**

## The identity wall decides half of them

| service | free offer | UDP | identity | verdict |
| --- | --- | --- | --- | --- |
| SakuraFrp | 2 tunnels at 10 Mbit/s and 5 GiB/month, plus a daily check-in grant | yes | mainland phone and real-name verification | `fails-identity` |
| 蜻蜓映射 (Qingting) | 1 mapping at 1 Mbit/s and 1 GB/month | yes | real-name verification | `fails-identity` |
| 樱花frp (chmlfrp) | 4 tunnels at 8 Mbit/s with unlimited traffic | yes | real-name verification | `fails-identity` |
| NATAPP | 2 GB/month at 1 Mbit/s | TCP only on the free tier | email | `fails-quota` |
| 内网云 (iis-pub-frp) | 10 GB/month, 2 tunnels | yes | email | `fails-quota` |
| 星空frp (starryfrp) | a daily check-in grant of 1 to 10 GiB | yes | email | `fails-quota` |
| fnat | 20 to 50 GB/month on 3 to 5 tunnels | yes | email | `fails-quota` |
| frp-vip | 1 Mbit/s, one port, a trial | yes | email | `fails-quota` |

⛔ **A real-name check is `national-id`, and a panel that requires one is unreachable
without real-name verification.** Three of the largest panels are in that class, and
their quotas are real and irrelevant. SakuraFrp is the one whose record names a mainland
Chinese ID number and an Alipay face check. The record states the ceiling and the gate
in one sentence, because a number without the gate is a marketing claim.

## The relays that answer without an account

| relay | what it publishes | UDP | volume | verdict |
| --- | --- | --- | --- | --- |
| freefrp.com | `frps` on ports 10000 to 60000, token `public.freefrp.com` | yes | no quota, 30 Mbit/s sustained ceiling | `qualifies-with-caveat` |
| freefrp.net | `frps` on port 7000, ports 10001 to 50000 | yes | no quota published | `qualifies-with-caveat` |
| NATP2P | a relay plus direct connection, TCP and UDP | yes | a daily grant with no figure | `qualifies-with-caveat` |
| OpenFrp | 2 tunnels at 12 Mbit/s | yes | daily check-in grant | `qualifies-with-caveat` |
| MeFrp | 2 tunnels at 10 Mbit/s, 25 Mbit/s after real-name | yes | daily check-in grant | `qualifies-with-caveat` |
| Mikrus | a free VPS in Finland, 256 MB RAM | via `wireguard-go` | no byte figure | `qualifies-with-caveat` |

⭐ **freefrp.com and freefrp.net need nothing at all**: a shared token, a public
port range and `frpc`. They are the only anonymous UDP ingress found that carries
an arbitrary port, and that is why they sit at the top of this page despite an
unverified operator.

⚠ **freefrp.com states that sustained traffic at or above 30 Mbit/s gets a `/24`
blocked.** 1 TiB/month needs 3.24 Mbit/s, so the rate does not bind at this
volume; nothing published says what does.

### The daily check-in model

OpenFrp, MeFrp, starryfrp and the rest grant traffic for a daily action rather
than a monthly allowance. The grant is the quota and its size is not published,
so a reader cannot compute a month. At 12 Mbit/s a month is 3.9 TB if the grant
never runs out, and the grant is what decides whether 1 TiB is reachable.

⚠ **A check-in grant is a quota in a different unit: attention.** It is renewed
by a human action, it is not additive across accounts in any documented way, and
the service can change the grant without notice. The record keeps it as
`volume-quota` and says the size is unknown.

## What is dead

- **LocyanFrp** advertised unlimited tunnels and a check-in grant, and the pages
  that would confirm it did not resolve. `dead`, `unverified`.
- **SakuraFrp's free tier** is 5 GiB/month before the check-in grant, which is
  0.5% of one TiB month even before the identity gate.
- **Waiwang Men's "1T"** is one-way server traffic on a shared 1000M node, which
  is a VPS allowance and not a tunnel quota.

## Chaining

**The anonymous chain.** `freefrp.com token -> frpc -> a UDP tunnel -> a WireGuard
listener`. Nothing in the chain needs an account, and the scarce link is the
operator's continued goodwill.

**The check-in chain.** `OpenFrp account -> frpc -> a UDP tunnel`. The scarce link
is a daily action and an unpublished grant, so it is a path for a person who is
present, not for an unattended job.

## The records

`dossier/egress/sakurafrp.json`, `natapp.json`, `qingting-map.json`,
`chmlfrp.json`, `openfrp.json`, `me-frp.json`, `freefrp-com.json`,
`freefrp-net.json`, `natp2p.json`, `starryfrp.json`, `iis-pub-frp.json`,
`frp-vip.json`, `fnat.json`, `locyanfrp.json`, `waiwang-men.json`,
`tamago-hkt-nat.json`, `mikrus-frog.json`. All are in `dossier/egress/`.

⚠ **Every volume figure on this page is a vendor claim.** No account was created, so
no free grant was measured, and no tunnel carried a byte.
