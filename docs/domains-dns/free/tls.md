# What does free TLS cost, and what does it not cover?

Two free certificate sources matter and they fail differently. Let's Encrypt has no cost and a
rate limit that binds a multi-tenant scheme. Cloudflare's Universal SSL has no rate limit and a
depth limit that binds the same scheme. The free answer that covers both is a wildcard from
Let's Encrypt over DNS-01 on a zone the holder controls.

## The comparison

Sorted by how much of a name space each one covers.

| source | coverage | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| Let's Encrypt with DNS-01 | any name the holder controls, including a wildcard | 50 certificates per registered domain per 7 days | anonymous | qualifies |
| Cloudflare Universal SSL | the apex and one level of subdomain | one level only | email plus a zone | qualifies-with-caveat |

## Let's Encrypt

Let's Encrypt issues free 90-day certificates, including wildcards over DNS-01, with automated
renewal. It needs no account that a human registers: an ACME account key is generated locally.

The limits are published and they are detailed:

- **50 certificates per registered domain per 7 days**, global across all accounts, refilling at
  one per 202 minutes.
- **5 certificates per exact set of identifiers per 7 days**, refilling at one per 34 hours.
- **300 new orders per account per 3 hours.**
- **10 new accounts per IP per 3 hours.**
- **5 failed authorizations per identifier per account per hour.**
- **1,152 consecutive authorization failures** per identifier, after which the identifier is
  paused until it is unpaused through the self-service portal.

⭐ A renewal that uses ARI, or that repeats the exact set of identifiers, is exempt from the order
limit and from the per-registered-domain limit. That exemption is the reason a well-behaved client
does not need an override.

Both the production and the staging directories answered on 2026-10-22. The production directory
returned 200 with 961 bytes and sha256
`ee1bfe324dcd5aff6e67ba25ea98397494d5b6ebf6c7f16e98348254636190e0`, listing `keyChange`, a `meta`
block with the current subscriber agreement, and three profiles: `classic`, `shortlived` and
`tlsserver`. The staging directory returned 200 with 1,035 bytes.

Using staging for a test is the cheap protection: staging endpoints have far looser limits, so an
issuance bug costs nothing against the production counters.

`Evidence:` probes of `acme-v02.api.letsencrypt.org/directory` and the staging directory on
2026-10-22, both 200 with the byte counts and digest above.
`letsencrypt.org/docs/rate-limits/` (read 2026-10-22): every limit quoted above, and the ARI
exemption.

`Verdict:` qualifies. The 50-per-registered-domain limit is the one a per-tenant scheme meets, and
the exact-identifier limit is the one a retry loop meets.

## Cloudflare Universal SSL

Every Cloudflare zone gets a free certificate automatically. The limit is depth: it covers
`example.com` and `app.example.com`, and **not** `a.b.example.com`. Deeper names need Advanced
Certificate Manager, which is paid.

⚠ That one-level limit is the trap. A per-tenant scheme at `tenant.app.example.com` is two levels
deep and is not covered, and the fix on the same platform is a paid product. The free fix is a
wildcard from Let's Encrypt over DNS-01, which needs the record API and therefore the same zone.

`Evidence:` `developers.cloudflare.com/ssl/edge-certificates/universal-ssl/` (read 2026-10-22):
Universal SSL is free on every plan, with the one-level coverage limit and the Advanced Certificate
Manager upgrade path. The one-level figure is repeated across Cloudflare's TLS pages and in
third-party summaries, so this record is `reported`.

`Verdict:` qualifies-with-caveat. Free and automatic, and one level deep.

## The chain that covers everything

`Cloudflare DNS` for the zone, a `CNAME` at the apex if a service needs one, `Let's Encrypt` with a
DNS-01 challenge for a wildcard, and `Cloudflare Tunnel` for the ingress. Total cost is the domain.

The scarce link is not the certificate and not the DNS. It is the 200-record cap on the zone, and
it arrives at the same tenant count as the certificate's 50-per-week limit: roughly the point
where a per-tenant subdomain scheme stops being free.

## What did not work

- **Universal SSL for a per-tenant scheme**: one level only, so `tenant.app.example.com` is
  uncovered (`reported`, `developers.cloudflare.com/ssl/edge-certificates/universal-ssl/`).
- **Let's Encrypt for 500 new names in a week under one domain**: 50 certificates per registered
  domain per 7 days, globally (`documented`, `letsencrypt.org/docs/rate-limits/`).
- **A wildcard from Let's Encrypt without a DNS API**: DNS-01 needs a TXT record and therefore a
  provider with an API, which rules out DuckDNS and the afraid.org shared registry as a zone
  (`inferred` from Let's Encrypt's challenge types and the free-DNS APIs).
- **Universal SSL's 2024 behaviour as current**: the one-level rule is stable, but the record cap
  on a zone created after 2024-09-01 is 200, not 1,000
  (`documented`, `developers.cloudflare.com/dns/manage-dns-records/`).
- **A certificate for an IP address**: Let's Encrypt issues for IP addresses under the same limits,
  but the certificate is not a name and does not solve the zone problem (`documented`,
  `letsencrypt.org/docs/rate-limits/`).

## Chaining

**The zero-cost public endpoint.** `EU.org` or a paid domain, plus `Cloudflare DNS`, plus
`Universal SSL`, plus a `Tunnel`. The scarce link is the domain, and the certificate and the DNS
are free on either path.

**A wildcard for a per-tenant service.** `deSEC` or `Cloudflare DNS` for the zone and `Let's
Encrypt` over DNS-01 for a wildcard. The scarce link is the record cap on the zone, which is 200 on
Cloudflare and unpublished on deSEC.
