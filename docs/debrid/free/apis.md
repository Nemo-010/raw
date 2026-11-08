# APIs and failure modes

A debrid that cannot be driven by a script is a website. This document records what
each service's API actually does, the request rate that stops it, and the error
shapes a client must branch on.

## The answer

⭐ **A script can drive TorBox end to end on its free key.** The token is a plain
bearer, the rate is documented at 300 requests a minute with 60 an hour for uncached
adds, and a first-party WebDAV endpoint at `https://webdav.torbox.app` takes the API
key as a password, so `rclone` can mount it with no shim.

⛔ **What breaks it is not a rate. It is the 10 GiB per-download cap**, returned as
`DOWNLOAD_TOO_LARGE`. At 1 TiB a month, which is 3.4 Mbit/s sustained, no documented
request rate on any of the eight services is reachable. The caps are.

## The request rates

| service | published rate | what a client actually meets |
| --- | --- | --- |
| TorBox | 300/min, 60/hour for uncached adds | a 10 GiB object cap long before the rate |
| Real-Debrid | 250/min | about one add per 20 seconds; 6 of 6 refused at 10 seconds |
| AllDebrid | not published | per-host quotas, `limitedHostersQuotas` |
| Premiumize | not published | a points budget, not a rate |
| Debrid-Link | per endpoint, `floodDetected` | an hour lockout, "retry later (~1h)" |
| Deepbrid | 250/min premium, 100/min free | 5 link generations a day on free |
| Mega-Debrid | 50/s before an IP ban | premium-only API |
| LinkSnappy | not documented | endpoints only in ResolveURL source |

⚠ **The published rate is not the rate a script meets.** Real-Debrid's 250 a minute
is real for general calls, but its torrent endpoint is paced at about one add per
20 seconds by third-party measurement, and a client that trusts 250 loops into a
refusal it cannot distinguish from a block.

## The error shapes

| service | shape | what it means |
| --- | --- | --- |
| Real-Debrid | `451` or `403`, body `{"error":"infringing_file","error_code":35}` | a blocked name **and** a throttle inside 20 seconds, one signal |
| TorBox | `429` plus `Retry-After: 300` | account-wide link-resolution budget exhausted |
| TorBox | `DOWNLOAD_TOO_LARGE` | the object exceeds the plan's per-download cap |
| Debrid-Link | `floodDetected` | per-endpoint lockout, about an hour |
| AllDebrid | HTTP 200 plus `AUTH_MISSING_APIKEY` | a missing key, not a refusal of the request |
| AllDebrid | `AUTH_BLOCKED` | the key is geo- or IP-blocked |
| Mega-Debrid | `vip_end` | the plan requires premium for the API |
| Premiumize | HTTP 200 plus `rate_limit_reached` | every error is a 200 |
| Usenet | `430 No Such Article` | aged out **or** removed, one code |

⛔ **A client cannot branch on the HTTP status alone.** AllDebrid and Premiumize
return 200 for a refusal, Debrid-Link returns 404 for a bad token, and Real-Debrid
returns 451 for two different causes. The body is the contract.

## The services, one line each

| service | API | note |
| --- | --- | --- |
| TorBox | REST, bearer, WebDAV | the only one drivable end to end on a free key |
| Real-Debrid | REST, private token | an unauthenticated `POST /unrestrict/check` exists and is the cheapest cache test |
| AllDebrid | REST v4 and v4.1 | `remainingTrialQuota` exposes the trial's remaining MB |
| Premiumize | REST | 1,000 points a month, `fairusefactor` per host |
| Debrid-Link | REST v2 | its docs page is a JavaScript shell; the contract is at `/api/v2/api_doc/infos` and `/errors` |
| Mega-Debrid | REST with a password in the query string | premium-only by design; a token dies on the next login |
| Deepbrid | REST v1 | 100 requests a minute on free |
| LinkSnappy | undocumented | endpoints reconstructed from ResolveURL; `reported` |

⚠ **Mega-Debrid authenticates with a password in the query string.** That is a
credential in a URL, which leaks into logs and proxies. It also bans an IP after
50 requests a second or four bad logins.

## What a client must do

1. **Treat the body, not the status, as the result.** A 200 with `AUTH_MISSING_APIKEY`
 is not success.
2. **Pace adds at 20 seconds** on Real-Debrid, and treat `error_code: 35` as
 ambiguous between a block and a throttle.
3. **Read `Retry-After`** on a 429 and stop the whole account, not one request.
4. **Check the per-object cap before the transfer**, because a 10 GiB cap fails a
 large object after the request has been accepted.
5. **Record the refusal string** in the client's log, because the same code means
 different things across services.

## The client layer

| tool | what it does | status |
| --- | --- | --- |
| rclone with TorBox WebDAV | mounts a free account | works, first-party |
| Torrentio | returns streams from a debrid key | hosted, public manifest |
| Debrid Media Manager | manages a debrid library in a browser | hosted, needs a key |
| zurg (self-hosted) | WebDAV front end for Real-Debrid | splits pacing to 250 general and 75 torrents |
| Decypharr (self-hosted) | qBittorrent-compatible front end for debrid and usenet | a client, not a service |
| RDT-Client (self-hosted) | downloads a debrid torrent to local disk | needs local disk |

⭐ **A missing client is never a rejection.** A provider with a real API and no
wrapper is an opportunity; the wrapper is a small piece of work, the capacity is
not.
