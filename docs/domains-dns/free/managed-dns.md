# Which free DNS provider has the record cap and the API a service needs?

Five providers host DNS for a domain already owned, for nothing. The record cap is what decides
between them and the API rate is what decides whether a service can be provisioned. Cloudflare has
the widest documented feature set and caps a new zone at 200 records, down from 1,000 on a zone
created before 2024-09-01. ClouDNS publishes the smaller cap at 50 and one zone. deSEC publishes
no record cap, publishes the strictest rate limit, and gates the number of domains an account may
hold behind a support request the page does not quantify.

## The comparison

Sorted by how many records a zone can hold, because that is the number a per-tenant scheme meets
first.

| provider | free records | API | identity | verdict |
| --- | --- | --- | --- | --- |
| deSEC | no published record cap; a domain counter of order one per account, and 300 RRset changes per domain per day | full REST, probed | email | qualifies-with-caveat |
| Hurricane Electric | unpublished | web panel, key-based dynamic update | email plus IPv6 cert | qualifies-with-caveat |
| Namecheap FreeDNS | about 150, third-party | web panel | email | qualifies |
| Cloudflare DNS | 200 per zone on a zone created after 2024-09-01 | full REST and DoH, probed | email | qualifies |
| ClouDNS | 50 records, 1 zone | REST | email | qualifies-with-caveat |

## The four questions this document answers

For each provider: the record limit, whether the API exists, whether `CNAME` works at the apex,
and whether the domain must be registered with that provider. The last one is the gate that is
easiest to miss.

| provider | record limit | API | CNAME at apex | domain must be registered there |
| --- | --- | --- | --- | --- |
| Cloudflare | 200 | yes | yes, via CNAME flattening | no |
| deSEC | none published; one domain per new account until support raises it | yes | yes, `subname` empty is the apex | no |
| ClouDNS | 50 | yes | unverified | no |
| Namecheap | about 150 | no documented API for FreeDNS | unverified | no, and it refuses its own |
| Hurricane Electric | unpublished | a key-based dyndns URL only, no REST | unverified | no |

## Cloudflare DNS

A free zone gets anycast resolution, a full API, DNSSEC, DoH and DoT resolvers, and **200 DNS
records** on a zone created on or after 2024-09-01. A free zone created before that date keeps
**1,000**. Pro and Business get 3,500 and Enterprise falls to a per-account quota.

Records that other Cloudflare services create count against the same quota, and the documentation
says they are enforced "with a small buffer", so a zone may briefly hold slightly more than its
limit. The dashboard warns at 85% of the quota, and the current quota and usage are readable per
zone through the API.

⭐ **Cloudflare never limits or caps DNS queries** on any plan. The constraint is records, not
traffic.

**CNAME at the apex works**, through CNAME flattening. The zone-apex guide says an ANAME or ALIAS
record from a previous provider can be recreated as a CNAME at `@`, and that flattening makes it
legal.

`Evidence:` probe of `cloudflare-dns.com/dns-query?name=example.com&type=A` on 2026-10-22: 200,
251 bytes of JSON with two A records, so the keyless DoH resolver answers programmatically.
`developers.cloudflare.com/dns/manage-dns-records/` (read 2026-10-22): the per-zone quota table and
the 2024-09-01 boundary. `developers.cloudflare.com/dns/manage-dns-records/how-to/create-zone-apex/`
(read 2026-10-22): "Cloudflare's CNAME flattening allows you to create CNAME records at your zone
apex". `developers.cloudflare.com/dns/faq/` (read 2026-10-22): "Cloudflare never limits or caps
DNS queries".

`Verdict:` qualifies. The published limit that binds is the record cap at 200, and Cloudflare states it never limits or caps DNS queries, so there is no query ceiling to meet.

## deSEC

deSEC gives free managed DNS with anycast, a full REST API and DNSSEC, and it publishes no record
count cap. The binding limits are rates, and they are published in detail:

- **RRset create, delete or modify: 2 per second, 15 per minute, 100 per hour, 300 per day, per
  domain.**
- **Any activity: 2,000 per day per account, or per IP for an unauthenticated caller.**
- **dynDNS updates: 2 per 2 minutes per domain.**
- DNS reads: 10 per second and 50 per minute. Domain creation and deletion: 10 per second, 300 per
  minute, 1,000 per hour. Account actions with external effects: 3 per minute.

The windows slide and a throttled request returns 429 with a `Retry-After` header. The docs
recommend bulk requests when 300 changes a day is not enough, which is the alternative route for a large
import: 500 records one at a time takes two days, and one bulk call takes one.

The API was reachable and correct on 2026-10-22. An unauthenticated `GET /api/v1/domains/` returned
**401** with 58 bytes, `{"detail":"Authentication credentials were not provided."}`, carrying
`WWW-Authenticate: Token` and `Allow: GET, POST, HEAD, OPTIONS`. The login endpoint returned
**400** with `{"email":["This field is required."],"password":["This field is required."]}`, which
proves a live DRF login route rather than a stub.

The API addresses RRsets rather than individual records, and **an empty `subname` is the apex**.
A wildcard is allowed once at the beginning of a name.

`Evidence:` probes of `desec.io/api/v1/domains/` and `desec.io/api/v1/auth/login/` on 2026-10-22.
`desec.readthedocs.io/en/latest/rate-limits.html` (read 2026-10-22): the rate table quoted above.
`desec.readthedocs.io/en/latest/dns/rrsets.html` (read 2026-10-22): "If `subname` is empty, this is
equal to `{name}.`".

⛔ **The domain counter is the constraint, and it is not published.** deSEC's rate page documents
per-domain rates and says nothing about how many domains an account may hold. A new account is
reported to start at one domain, with the panel's message asking the user to contact support for a
higher limit, and a deSEC staff reply on the project's own forum gives the current formula as
`max(1, s + round(sqrt(s)))` for `s` domains delegated with DNSSEC enabled, which is 6 for `s = 4`.
An independent write-up records the same one-domain start. The signup form says only "Your first
domain (you can add more later)", which is the closest thing to a first-party statement and gives no
number.

That is a `reported`-rung finding against a `documented`-rung rate table. It is not a
`blocks-use` finding because every source for the number is a forum post or a blog rather than a
vendor page, and one email address and one signup would settle it.

`Verdict:` qualifies-with-caveat. The right choice for **one** small zone and for anything that
needs a `CNAME` at the apex without Cloudflare, with a support request standing between the reader
and the second zone.

## ClouDNS

ClouDNS's Free Forever plan gives **1 DNS zone, 50 DNS records, 500,000 DNS queries per month, 1
mail forward, 1 dynamic DNS hostname** and 4 unicast nameservers. It is the only provider here
that publishes a query cap, because Cloudflare states it has none; and its record cap is the
smallest published in the class, so it is the first thing a reader meets.

`Evidence:` `cloudns.net/managed-dns/` (read 2026-10-22): the Free Forever column as quoted.

`Verdict:` qualifies-with-caveat. One zone and 50 records is a demo, not a host.

## Namecheap FreeDNS

Namecheap hosts DNS for **third-party domains only**, which means it refuses a domain registered
at Namecheap itself. Nameserver verification takes up to 16 hours, and the registrar gives 10 days
to make the change.

The record count is **about 150** and it is a comparison-page figure. Namecheap's own page
describes the service and publishes no number, so this record is `reported` and no table cell
rests on it alone.

`Evidence:` `namecheap.com/domains/freedns/` (read 2026-10-22): "Free 3rd-party domains support
only", the 16-hour verification and the 10-day window. No record count.

`Verdict:` qualifies. A backup DNS for a domain whose primary is elsewhere, which is the use
Namecheap names.

## Hurricane Electric

Hurricane Electric gives free hosted forward and reverse DNS with many record types and multiple
domains per account. Reverse DNS is the property the other providers here do not offer as readily.

The gate is an account: an IPv6 certification or a tunnelbroker account. The portal returned 200
with 16,458 bytes on 2026-10-22, so the service answers. **No record or query cap is published**,
which is worse than a small published one: a discretionary throttle has no ceiling to design
against.

`Evidence:` probe of `dns.he.net/` on 2026-10-22: 200, 16,458 bytes, the login portal.

`Verdict:` qualifies-with-caveat. An unpublished cap and a gated account.

## What did not work

- **ClouDNS as a per-tenant zone host**: one zone and 50 records, so the second tenant needs a
  second account (`documented`, `cloudns.net/managed-dns/`).
- **Namecheap FreeDNS for a Namecheap-registered domain**: the service is for third-party domains
  only (`documented`, `namecheap.com/domains/freedns/`).
- **Hurricane Electric as a provisioned zone**: no documented REST API for records and no
  published cap, so a script cannot plan against it (`documented`, `dns.he.net/`).
- **deSEC for a bulk import in one run**: 300 RRset changes per domain per day, so 500 records
  takes two days unless a bulk request is used (`documented`,
  `desec.readthedocs.io/en/latest/rate-limits.html`).
- **Cloudflare as a per-tenant zone host at no cost**: 200 records per zone is per zone and not
  per account, but the records Email Routing adds count against it (`documented`,
  `developers.cloudflare.com/dns/manage-dns-records/`).

## Chaining

**Cloudflare for one zone with many records under 200.** `Cloudflare DNS` plus `Universal SSL` plus
a `Tunnel`. The scarce link is the 200-record cap, which a per-tenant subdomain scheme reaches at
tenant 200.

**deSEC for one small zone, with a support request per extra domain.** `deSEC` with its own
registrar. The scarce link is the domain counter, not the rate: deSEC publishes no number for how
many domains an account may hold, a new account is reported to start at one, and the panel asks the
user to contact support for more. The 300 changes per domain per day is fine in steady state and
painful to bootstrap.

**deSEC for ACME DNS-01.** A `CNAME` at the apex plus a wildcard record makes a wildcard
certificate possible on a provider that charges nothing. The scarce link is the 2-per-2-minutes
dynDNS rate, which only matters if the certificate is issued and revoked repeatedly, and the domain
counter, which limits the scheme to as many zones as support has granted.
