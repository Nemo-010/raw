# Per-host quotas

A multi-hoster does not sell bytes. It sells a daily allowance **per source host**,
and that allowance is the number a 1 TiB month meets first. This document is the
matrix, the sources behind it, and the two services that meter multiplicatively
instead.

## The answer

⭐ **TorBox is the only service that publishes the whole matrix to an anonymous
caller.** `https://api.torbox.app/v1/api/webdl/hosters` returns 162 hosters, 95
file hosts and 67 stream hosts, with `daily_bandwidth_limit`, `daily_link_limit`
and `per_link_size_limit`. That is 72,261 bytes and no credential.

⛔ **The same host carries caps that differ by up to 30 times.** isra.cloud is
10 GB a day at LinkSnappy, 20 at Mega-Debrid, 25 at FakirDebrid and 53.7 at
TorBox. katfile is 20, 50 and 53.7 GB a day on three services and unlimited on
LinkSnappy. Which service is cheapest therefore depends on which host the reader
uses, and a single price per month hides that.

## Where each column comes from

| service | endpoint | what it returns |
| --- | --- | --- |
| TorBox | `/v1/api/webdl/hosters` | 162 rows, bytes, links and per-link size |
| Mega-Debrid | `?page=register`, VIP column | 16 caps |
| FakirDebrid | `/status.php` | 64 caps, daily and weekly |
| LinkSnappy | `/landing` | 11 caps |
| DebridMaster | `/status` | 5 caps |
| AllDebrid | `/v4.1/user/hosts` | `quotaMax`, key required |
| Real-Debrid | `/rest/1.0/traffic` | `limit`, key required |
| Debrid-Link | `/api/v2/downloader/limits/all` | `daySize`, key required |
| Deepbrid | `/api/v1/user/limits` | key required |
| Premiumize | `/api/services/list` | `fairusefactor`, no key |

⚠ **A host missing from a service is not a host with no cap.** A dash means the
service does not list the host at all. `no cap published` means it lists the host
and publishes no number, which is not the same as unlimited. `account-only` means
a cap exists and is returned only to a key. The three are kept separate because a
client acts differently on each.

## The hosts that bite first

Sorted by the tightest published cap, which is where a 1 TiB month stops:

| host | tightest cap | service | note |
| --- | --- | --- | --- |
| file.al | 5 GB/day | FakirDebrid | 3x points at Premiumize |
| filedot.to | 5 GB/day | FakirDebrid | |
| upstore.net | 5 GB/day | FakirDebrid | 20 GB/day at DebridMaster |
| wdupload.com | 5 GB/day | Mega-Debrid | 10.7 GB/day at TorBox |
| world-files.com | 8 GB/day | FakirDebrid | |
| filesmonster.com | 8 GB/day | FakirDebrid | 4x points at Premiumize |
| keep2share.cc | 10 GB/day | FakirDebrid | 50 GB/day at DebridMaster |
| isra.cloud | 10 GB/day | LinkSnappy | 53.7 GB/day at TorBox |
| wupfile.com | 10.7 GB/day | TorBox | the tightest TorBox row |
| ddownload.com | 10 GB/day | Mega-Debrid | unlimited at Fakir and LinkSnappy |

⭐ **A free host's ceiling can be read from a competitor's table.** Leechall
publishes per-host daily pull caps that the hosts themselves hide: extmatrix
6 GB/day, 1fichier 8 GB/day, mega.nz 1 GB/day, isra.cloud 650 MB/day, emload
250 MB/day. That is a vendor publishing its own inputs, and it is the cheapest
measurement of each host's real ceiling.

## The link counter

⛔ **The link count usually binds before the bytes.** TorBox allows 5 links a day
on 15 hosts, so a 10.7 GB byte cap only matters for files above 2.1 GB on
wupfile, and 107 GB on rapidgator. Debrid-Link documents 300 links against
85.9 GB for the same host, which puts the counter second there and the bytes
first.

A client that opens one connection per file is bounded by links. A client that
opens many connections per file is bounded by bytes. The matrix has to carry both.

## Two services meter by a multiplier

| service | shape | example |
| --- | --- | --- |
| Premiumize | `fairusefactor` 1 to 5 times per host | 14 hosts at 1x, 4 at 5x |
| HIGHWAY | 33 to 50% of consumed bytes on discounted hosts | table members-only |

⚠ **A multiplier is not a byte cap and cannot be added to one.** Premiumize's
1,000 points a month, at 1 GB per point and 30 points a day, is 900 GB a month at
1x. A host at 5x turns the same 10 GB into 50 points, so the month is five times
shorter on that host, not five times larger.

## What the refusal looks like

Four services document a per-host cap and refuse a keyless caller, in three
different shapes. A client that branches on the wrong one retries forever:

| service | status | body |
| --- | --- | --- |
| AllDebrid | HTTP **200** | `AUTH_MISSING_APIKEY`, 98 bytes |
| Real-Debrid | HTTP 401 | `bad_token`, 43 bytes |
| Debrid-Link | HTTP **404** | `badToken`, 106 bytes |
| Deepbrid | HTTP **200** | a 43 KB login page |

⭐ **The cheapest next probe is Real-Debrid's `POST /rest/1.0/unrestrict/check`**,
the only unauthenticated per-link check found. A direct POST would settle whether
a link is cached before a plan is bought.

## How to use this

1. Name the hosts the reader actually uses. A plan is bought per host, not per
 service.
2. Read that host's row across the services in scope. The cheapest month is the
 one whose row is highest for those hosts.
3. Read the link count beside the byte cap. The smaller of the two binds.
4. For a host at a multiplier, convert the points before comparing a month.
