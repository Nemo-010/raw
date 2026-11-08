# What is the cheapest name a service can live on?

DNS is free and the name is not. Every managed-DNS provider surveyed gives away hosting on a
domain already owned, and none of them gives away a registrable domain with any reliability.
The cheapest complete public endpoint found is a USD 10.46 `.com` at cost, plus free DNS, free
TLS and a free tunnel.

## The four layers, and where each one's free tier stops

| layer | free? | who is in it | what binds |
| --- | --- | --- | --- |
| a subdomain under someone else's domain | yes | DuckDNS, afraid.org, EU.org, is-a.dev | not owned, and the owner can withdraw it |
| managed DNS on an owned domain | yes | Cloudflare, deSEC, ClouDNS, HE, Namecheap | records per zone, the domain count per account, and API rate |
| the domain itself | no | Cloudflare Registrar, Porkbun, Spaceship | the renewal price, which is not the first-year price |
| TLS | yes | Let's Encrypt, Cloudflare Universal SSL | 50 certificates per registered domain per 7 days |

## The constraint that decides the whole topic

⛔ **A free subdomain cannot be a Cloudflare zone.** A `*.duckdns.org` name resolves and nothing else
comes with it: no Tunnel, no Email Routing, no Universal SSL, no proxy. An egress chain needs a zone
whose nameservers point at Cloudflare, and that needs a registrable domain.

So the USD 10.46 is not avoidable, and everything else in this topic is downstream of it.

## The second constraint: records, not queries

Cloudflare never caps DNS queries on any plan. It caps **records**: 200 per zone on a free zone
created on or after 2024-09-01, and 1,000 on an older one. ClouDNS caps at **50 records and one
zone**. Namecheap's figure is about 150 and it is third-party.

A per-tenant subdomain scheme meets the record cap long before it meets anything else. Two
hundred records is 200 tenants, and the records that Cloudflare's own Email Routing adds count
against the same quota.

## The documents

| document | answers |
| --- | --- |
| [`free/subdomains.md`](free/subdomains.md) | which free hostname still works, and what it cannot carry |
| [`free/managed-dns.md`](free/managed-dns.md) | the record caps and API rates of the free DNS providers, with the two APIs that were probed |
| [`free/tls.md`](free/tls.md) | the Let's Encrypt limits and the one-level limit of Universal SSL |
| [`paid/registrars.md`](paid/registrars.md) | first-year versus renewal, per registrar and per TLD |
| [`paid/tlds.md`](paid/tlds.md) | the cheapest first year and the cheapest second year, which are different TLDs |

## The numbers to carry away

- **Cloudflare Registrar `.com`: USD 10.46 registration and USD 10.46 renewal.** For `.com` and
  `.net`, registration, renewal and transfer are the same number, because the price is the registry
  fee and Cloudflare takes no markup. It is not true of every TLD: at-cost pricing still carries the
  registry's own promo, so `.online` is 4.99 then 27.70 and `.org` is 8.50 then 11.20.
- **Spaceship `.com`: USD 8.88 then USD 9.98.** Cheaper in both years than Cloudflare's `.com`,
  which is the only row found where a promo beats at-cost twice.
- **Spaceship `.online`: USD 0.98 then USD 15.08.** A 15.4 times jump, which is the sharpest promo
  trap in the set.
- **Porkbun `.xyz`: USD 2.04 then USD 14.21.** Seven times the first year and more than a `.com`
  at Cloudflare.
- **Cloudflare DNS: 200 records per zone**, and no query cap.
- **deSEC: 300 RRset changes per domain per day**, 2,000 API requests per day per account, and a
  domain count per account that deSEC does not publish. A new account is reported to start at one.
- **Let's Encrypt: 50 certificates per registered domain per 7 days**, global across accounts.

## What is dead in this topic

**Four providers carry a non-qualifying verdict**: `freenom` is `dead`, and `cloudflare-registrar`,
`porkbun` and `spaceship` are `paid-only`. The dead ends below are additional and each lives in its
document's "What did not work" section. Two matter most:

- **Freenom** (`.tk`, `.cf`, `.ga`, `.gq`, `.ml`): the site answers 200 and the availability
  endpoint returns **500**, so the product is broken rather than closed, and no registration
  completes.
- **DuckDNS for anything Cloudflare-fronted**: it is a dynamic-DNS tool and not a name, and it
  cannot be a zone.

The rest are in each document's "What did not work" section and in `dossier/domains-dns/`.

## The records

Every provider named in this topic has one record.

| slug | provider | verdict | confidence |
| --- | --- | --- | --- |
| `cloudflare-dns` | Cloudflare DNS | qualifies | measured |
| `desec` | deSEC | qualifies | reported |
| `cloudns-free` | ClouDNS | qualifies-with-caveat | documented |
| `he-dns` | Hurricane Electric Free DNS | qualifies-with-caveat | documented |
| `namecheap-freedns` | Namecheap FreeDNS | qualifies | reported |
| `afraid-freedns` | afraid.org FreeDNS | qualifies-with-caveat | documented |
| `duckdns` | DuckDNS | qualifies-with-caveat | measured |
| `eu-org` | EU.org | qualifies-with-caveat | documented |
| `freenom` | Freenom | dead | measured |
| `cloudflare-registrar` | Cloudflare Registrar | paid-only | reported |
| `porkbun` | Porkbun | paid-only | documented |
| `spaceship` | Spaceship | paid-only | documented |
| `lets-encrypt` | Let's Encrypt | qualifies | measured |
| `cloudflare-universal-ssl` | Cloudflare Universal SSL | qualifies-with-caveat | reported |

## Where a number here came from

`measured` means a request was made from this machine on 2026-10-22. The deSEC API, the Let's
Encrypt directory, Cloudflare's DoH resolver, the DuckDNS update endpoint and the Freenom
availability endpoint were all called, and each transcript is in the record's `evidence`.
`documented` means a first-party page read on 2026-10-22. `reported` means a third party, and three records rest on one: Namecheap's record count, deSEC's
domain count per account, and Cloudflare's per-TLD prices, which Cloudflare publishes only in its
dashboard.

The records are in [`../../dossier/domains-dns/`](../../dossier/domains-dns/).

## Records that no other document names

This list holds each `measured` or `documented` record of this topic that no other document of
`docs/` names.

<!-- generated:start topic=domains-dns kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `bunny-dns` | Bunny DNS | paid-only | documented |
| `digitalplat-freedomain` | DigitalPlat FreeDomain | qualifies-with-caveat | documented |
| `dnspod-free` | DNSPod | qualifies-with-caveat | documented |
| `dynu-free` | Dynu | qualifies-with-caveat | documented |
| `dynv6` | dynv6 | qualifies-with-caveat | documented |
| `freemyip` | freemyip.com | qualifies-with-caveat | measured |
| `google-trust-services` | Google Trust Services | qualifies-with-caveat | documented |
| `hetzner-dns` | Hetzner DNS | qualifies-with-caveat | documented |
| `is-a-dev` | is-a.dev | qualifies-with-caveat | documented |
| `isroot` | isroot | qualifies-with-caveat | documented |
| `js-org` | JS.ORG | qualifies-with-caveat | documented |
| `kevin-service-registry` | Kevin Service Registry | qualifies-with-caveat | documented |
| `namesilo` | NameSilo | paid-only | documented |
| `no-ip-free` | No-IP | qualifies-with-caveat | documented |
| `nsupdate-info` | nsupdate.info | fails-identity | documented |
| `public-free-suffix` | Public Free Suffix | qualifies-with-caveat | documented |
| `ready-bd` | Ready (ready.bd) | qualifies-with-caveat | documented |
| `ydns` | YDNS | qualifies-with-caveat | documented |
| `zerossl` | ZeroSSL | qualifies-with-caveat | documented |
<!-- generated:end -->
