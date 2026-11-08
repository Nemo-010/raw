# Which free hostname still works, and what can it not carry?

Four services give away a hostname under someone else's domain. All four resolve. None of them
can be a Cloudflare zone, so none can carry a tunnel, email routing or a proxy certificate. The
one that can become a real zone is EU.org, and its queue is the constraint.

## The comparison

Sorted by how much control the holder has over the name.

| provider | what is offered | binding constraint | identity | verdict |
| --- | --- | --- | --- | --- |
| EU.org | a registrable subdomain under `.eu.org` | manual review, queue effectively stalled | email | qualifies-with-caveat |
| afraid.org | a hostname on a shared registry of 23,246 domains | the domain owner's consent | email | qualifies-with-caveat |
| DuckDNS | subdomains under `duckdns.org` | subdomains only, no custom domain | email | qualifies-with-caveat |
| Freenom | nothing: the availability endpoint returns 500 | the product is broken | email | dead |

## The test that decides each one

Ask three questions, in this order. Can it be a Cloudflare zone? Can its records be set by an
API? Does the owner's decision or a human's review sit in the path?

Only EU.org passes the first. All of them pass the second except Freenom. Three of the four fail
the third.

## EU.org

EU.org has given free registrable subdomains under `.eu.org` since 1996, with free renewal. It is
the only free option in this topic whose delegation the holder controls, so the name can be pointed
at Cloudflare's nameservers and become a zone.

The gate is a human. Every registration is reviewed, and the reports through 2025 and 2026
describe the queue as effectively stalled. That report is third-party; the site itself publishes
the review model and not its length.

`Evidence:` `nic.eu.org/` (read 2026-10-22): the site returned 200 and 3,554 bytes, running Apache
on FreeBSD, with the registration and general-policy pages linked. `nic.eu.org/policy.html` (read
2026-10-22): the review-based registration model.

`Verdict:` qualifies-with-caveat. The only free name that can become a zone, and a review queue
that means the name may not arrive this quarter.

## afraid.org FreeDNS

afraid.org offers free DNS hosting for a domain already owned, plus hostnames on a **shared
registry of 23,246 domains** whose owners have consented. The dynamic update is a URL with a
per-record token: `curl https://sync.afraid.org/u/<token>/` updates an A record, and
`v6.sync.afraid.org` does the same for AAAA.

The 5-hostname cap on the shared registry is a third-party figure and the site does not publish
one. Wildcard records are a paid feature.

⚠ The dependency is social: the domain owner can withdraw consent and the name goes away. That is a
technical reliability property, and it is the reason this is a dynamic-DNS tool rather than a
name.

`Evidence:` `freedns.afraid.org/` (read 2026-10-22): "23,246 domains in the shared domain
registry", the update URL form, and the v6 variant.

`Verdict:` qualifies-with-caveat. A hostname not owned, on a clock set by someone else.

## DuckDNS

DuckDNS gives subdomains under `duckdns.org` with a token API, IPv4, IPv6 and TXT support. The
update is one HTTPS GET: `https://www.duckdns.org/update?domains=NAME&token=TOKEN&ip=IP`, and
`clear=true` deletes the records. A TXT record set on a name applies to every sub-subdomain under
it.

⚠ The failure shape is worth carrying: a request with an empty token returned **HTTP 200** with a
two-byte body `KO` (`measured`, 2026-10-22T02:50:41Z). A status-only health check reports success
on a failed update.

The 5-subdomain cap is third-party; the site publishes the API and not the number.

`Evidence:` probe of `duckdns.org/update?domains=example&token=&ip=` on 2026-10-22: 200, 2 bytes,
`KO`. `duckdns.org/spec.jsp` (read 2026-10-22): the update URL, IPv4 and IPv6 parameters, the TXT
form and `clear=true`.

`Verdict:` qualifies-with-caveat. A name for a home IP, and nothing else.

## Freenom

Freenom sold free registrations on `.tk`, `.cf`, `.ga`, `.gq` and `.ml`. On 2026-10-22 the site
answered **302** to `my.freenom.com/domains.php`, which returned 200 with a working domain checker,
and an availability lookup for a `.tk` name returned **HTTP 500** with an "Oops!" page
(`measured`).

So the domain is up and the product is not. This is a different failure from a closed service, and
it is the one that misleads: a status check on the homepage says the provider is alive.

`Evidence:` probe of `freenom.com` and `my.freenom.com/domains.php?a=availability` on 2026-10-22:
302 then 200 on the checker, 500 on the lookup.

`Verdict:` dead.

## What did not work

- **Freenom**, above: the availability endpoint returns 500, so no registration completes.
- **DuckDNS for a Cloudflare-fronted service**: a `duckdns.org` name cannot be a zone, so no
  Tunnel, no Email Routing and no Universal SSL (`documented`, from Cloudflare's zone model).
- **afraid.org's shared registry as a stable name**: the owner can withdraw consent, and a
  wildcard is a paid feature (`documented`, `freedns.afraid.org/`).
- **EU.org as a name available now**: the review is the service and the queue is reported as
  stalled (`reported`).
- **A free hostname with a wildcard certificate**: a wildcard needs DNS-01 on a zone the holder
  controls, and three of these four are not zones (`inferred` from Let's Encrypt's DNS-01
  requirement).

## Chaining

**EU.org plus Cloudflare DNS plus Universal SSL.** `eu.org` delegation pointed at Cloudflare's
nameservers gives a free zone, a free certificate and a free tunnel. The scarce link is the EU.org
review, and it is the only chain in this topic whose total cost is zero.

**DuckDNS plus a direct A record.** A home IP with a name and no certificate automation. The
scarce link is that nothing else comes with the name, so a service on it is plain HTTP on a port.
