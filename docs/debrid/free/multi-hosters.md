# Multi-hosters

A multi-hoster, or debrid, holds a subscription to many file hosts and turns one
account into a download from all of them. This document is the core of the topic:
what the nine best-known services cost, what they actually cover, and which
constraint breaks first.

## The answer

⭐ **The cheapest flat month is AllDebrid at EUR 2.99, and the cheapest month that
clears 1 TiB is TorBox Essential at USD 3.00.** No service gives away a recurring
allowance that clears 100 GiB a month; the free counters are link-based, not
byte-based.

⛔ **Price is not the first gate. The caller's address is.** Five of the nine
refuse datacenter, VPS, proxy or cloud addresses in their own terms, and every
machine a reader can rent is one of those. TorBox is the only one whose
documentation affirmatively accepts any address; three publish no class rule at
all, and silence is neither permission nor refusal.

## The nine, priced

| service | 30 days | annual equivalent | free tier | usenet | verdict |
| --- | --- | --- | --- | --- | --- |
| AllDebrid | EUR 2.99 recurring, EUR 3.99 one-time | EUR 24.99 per 300 days | 7-day SMS trial, 25 GB | no | qualifies-with-caveat |
| Real-Debrid | EUR 4.00 | none sold | none | no | qualifies-with-caveat |
| TorBox Essential | USD 3.00 | not published | 10 downloads a month, 10 GB each | yes on Pro | qualifies |
| Debrid-Link | EUR 4.00 | EUR 25.00 per 300 days | not published | no | qualifies-with-caveat |
| Mega-Debrid | EUR 4.00 | EUR 16.00 per 180 days | none | no | qualifies-with-caveat |
| Deepbrid | EUR 4.99 | EUR 32.99 | 5 links a day, 1.2 GB a file | no | qualifies-with-caveat |
| High-Way | EUR 5.99 per 250 GB | EUR 47.99 per year | limited hosts | no | paid-only |
| Premiumize | EUR 9.99 or USD 11.99 | EUR 69.99 | none | yes | qualifies-with-caveat |
| LinkSnappy | USD 12.99 | USD 54.99 per 180 days | none | no | qualifies-with-caveat |

⚠ **A payer's month is not a month of bytes.** High-Way's EUR 5.99 buys 250 GB
that expires; its "UNLIMITED" tier means usenet and television are not counted,
while file-host bytes are fully metered, so the unlimited tier is worse per
file-host byte than Premium.

## What a plan actually covers

| service | host count, vendor API | what the marketing says |
| --- | --- | --- |
| AllDebrid | 46, of which 37 premium | "over 70" in its own meta description |
| Real-Debrid | 140 | a third-party matrix scored it 33 |
| Mega-Debrid | 85 | "100" on one page, "over 200" in its meta |
| Debrid-Link | 41 on one page, 42 on another | not stated |
| LinkSnappy | 75+, 50, and 11 in its own table | not stated |

⭐ **The API is the count to trust.** Every figure in the left column came from the
vendor's own host endpoint on 2026-10-23; every figure in the right column came
from a page trying to sell the service.

⚠ **A host count includes the dead.** Debrid-Downloader's "220+ hosts" contains
Zippyshare's own memorial page, "Here lies Zippyshare [2006 - 2023]". A count that
includes a grave is not a count.

## The daily cap is the real ceiling

⭐ **The per-host daily quota is what a multi-hoster actually sells, and five
services publish it in full.** TorBox returns 162 host rows with
`daily_bandwidth_limit`, `daily_link_limit` and `per_link_size_limit` to an
anonymous caller. The same host can carry caps that differ by 30 times:

| host | TorBox | Mega-Debrid | FakirDebrid | LinkSnappy |
| --- | --- | --- | --- | --- |
| isra.cloud | 53.7 GB/day | 20 | 25 | 10 |
| rapidgator | 537 GB/day | 1,000 | 35 | unlimited |
| turbobit | 53.7 GB/day | 80 | 25 | unlimited |
| katfile | 53.7 GB/day | 50 | 20 | unlimited |

⛔ **The link counter usually binds before the byte cap.** TorBox allows 5 links a
day on 15 hosts, so its byte cap only matters above 2.1 GB per file on one host
and 107 GB on another. A table that ranks services by bytes per day and omits the
link count has ranked the wrong number.

The full matrix is in [`host-quotas.md`](host-quotas.md).

## What breaks first

The first month meets five failure modes, in this order:

1. **A refusal by name.** Real-Debrid returns `{"error":"infringing_file",
 "error_code":35}` on the add. It returns the same body when two adds land
 inside 20 seconds, so a throttle and a block are one signal, and a retry loop
 cannot tell which it hit. Measured: six of six refused at 10 seconds, six of
 six accepted at 20.
2. **An account-wide rate lockout.** TorBox answers `429` with `Retry-After: 300`
 at about the 100th link resolution, whether the calls are flat out or paced.
 Debrid-Link answers `floodDetected` and says "retry later (~1h)".
3. **A lapsed plan.** TorBox returns `PLAN_RESTRICTED_FEATURE`, Mega-Debrid
 `vip_end` at token generation, High-Way code 5.
4. **A host removal.** A host stops being supported with no announcement.
5. **A second address.** `AUTH_BLOCKED` at AllDebrid, `22 IP Address not allowed`
 at Real-Debrid, a forced password reset at Real-Debrid when two addresses use
 one key.

The detail is in [`apis.md`](apis.md).

## The address class

| service | the rule | route |
| --- | --- | --- |
| TorBox | no address rule in its terms or its 33-code error table | none needed |
| Premiumize, LinkSnappy, High-Way | no class rule published | unknown |
| Real-Debrid | "will not use a dedicated server, VPS or any cloud service ... other than by using his Remote Traffic" | Remote Traffic, price unread |
| AllDebrid | "proxies, dedicated / private servers, cloud / entreprise networks are not allowed" | VPN authorisation, 12 hours, refusable |
| Debrid-Link | "Dedicated servers ... prohibited" | none named |
| Deepbrid | "dedicated server hosting, proxy and other infrastructure are prohibited" | none named |
| Mega-Debrid | VPN allowed only when authorised | 24 working hours |

⭐ **Real-Debrid's whitelist was withdrawn, not absent.** The 2026-08-29 archive
of `real-debrid.com/vpn` carries a 113-row table of allowed VPN addresses; the
2026-10-20 capture and both live reads render a zero-row table. The oracle still
answers per address: from a Cloudflare egress it returned "Your ISP or VPN
provider IP address is currently blocked", and from a residential address "not
blocked ... you don't seem behind a VPN", eight seconds apart.

⚠ **The workaround costs one VPN, not a proxy.** A sanctioned VPN is USD 2.15 a
month on a 27-month term, or USD 12.95 monthly. A static ISP proxy at USD 2.71 is
refused by name at all five refusing services, so adding it to the total buys
nothing. Metered residential at USD 0.35 to 6.00 a GB is 80 to 830 times the
subscription and is not a route.

## Fetch now, read later

| service | what survives a lapse |
| --- | --- |
| TorBox Pro plus AirLock | 37 days at best, 7 at worst: a 7-day purge window, then a 30-day clock from the last download |
| TorBox | 30 days |
| put.io | 15 days, unreadable during the grace |
| Offcloud | 7 to 30 days |
| Real-Debrid | 7 days on the link; the cache is shared and cached links die within about 3 months |
| Premiumize, LinkSnappy, Deepbrid, Mega-Debrid | 0 |

⛔ **Premiumize deletes everything at contract end**, and its own legal page says
so: "after automatic contract end ... all data in the cloud storage will be
irretrievably deleted". Its help article says "a short time". The contract governs.

## The secondary market

No secondary offer in stock beats the vendor's per-day price. Reseller vouchers
run 1.3 to 5.0 times the vendor rate, account shops sit at 1.04 to 1.11 times but
sell a login whose mailbox belongs to the seller, and lifetime deals are a trap:
Offcloud's StackSocial "lifetime" was converted to a one-year membership in
January 2026.

## What is dead

- **NinjaDebrid**, the best free offer found at "first 100 GB at full speed", died
 inside a fortnight; both hostnames now finish at `monkeytorrent.com`.
- **Fast-Debrid**'s domain is an Indonesian gambling site.
- **DebridMax**'s domain is a Chinese LED-sign factory.
- **Libera Premium**, a 2015-vintage Brazilian generator, announced its own end in
 2026 while search indexes still serve its price table.
- **Debrid.cc** is parked at `lander.parity.domains`.

## Two free generators are one service

⚠ `premiumlinkgenerator.net`'s only outbound link is `mixdebrid.com`, and
`leech.web.id/debrid` redirects there. MixDebrid publishes its own failure rate:
78 successes against 287 errors over seven days, or 21.1%. Counting those
doorways as separate services triples one service's capacity and triples its
failure rate with it.
