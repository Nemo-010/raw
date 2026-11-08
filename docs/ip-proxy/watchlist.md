# The reading list behind the registry

`scripts/sources/ip-proxy-aggregators.tsv` lists every source that publishes other
providers. This document says what each one is good for, what it is not, and what a
diff of it can and cannot establish. The gate fails while a registered source is
missing from this page, which is the only reason this page stays current.

| source | what it is good for | what it is not |
|---|---|---|
| [Proxyway's residential audit](https://proxyway.com/best-residential-proxies) | the only third-party measurement found that tests proxy exits against real targets and reports a mobile-versus-residential purity figure per vendor | a price list, and not first-party. Every figure from it is `reported` |
| [IP2Location's demo endpoint](https://www.ip2location.com/demo) | the free instrument that discriminates a class claim. It returns `usage_type` and `as_usage_type` for any address, unauthenticated | a registry. It is a database, and a vendor can pin delivery to the one it chose |
| [monosans/proxy-list](https://github.com/monosans/proxy-list) | the only free list that ships a per-proxy ASN, so the registration class is knowable before spending a request | a pool. Regenerated hourly and measured to lose two thirds of its working entries in 22 minutes |
| [Mullvad's relay API](https://api.mullvad.net/www/relays/all/) | a public relay inventory with a hostname per relay, which is how an ASN count can be computed rather than guessed | a statement about what answers on connect. It measures the published list |
| [the prefix brokers](https://ipv4.global/) | the lease market, where a `/24` or a `/29` is priced per address per month | a class. A broker's block is registered to the broker |
| [NodeSeek](https://www.nodeseek.com/) and the Chinese forums | the vocabulary that English queries never surface: 住宅IP, 家宽, 原生IP, 双ISP, 落地机 | readable by a fetcher. Use `search.web.pkgforge.dev` with `include_domains=`, because the forums are Cloudflare-walled to every fetch path |

## What a diff of each can establish

⭐ **A source that lists forty providers and has one of them recorded is not a
source that has been read.**

| source | the diff that matters |
|---|---|
| Proxyway | which vendors it audits that no record names. Its participant table is the closest thing to a census of the residential market |
| IP2Location | nothing to diff. It is an instrument, and the count is zero on purpose |
| monosans | nothing to diff. A list of proxies is not a list of providers |
| the relay API | the ASN set, recomputed. A vendor that adds a network is a new finding |
| the prefix brokers | the price band per address per month, which moves |
| the Chinese forums | the vendor names. About 200 were seen and not opened |

## What a coverage claim must name

⛔ **A coverage claim names the list it was measured against, in the same sentence.**
"The vendors are known" is a claim about the world. "Eight addresses across five
vendors, four of which failed a registry check" is a claim about a measurement, and
it is the only kind this topic may make.

⚠ **The residential and mobile market is the least evidenced part of the topic.**
Twenty-one vendors were opened for prices and one was measured for registration
class. Every per-GB figure in [`paid/residential-and-mobile.md`](paid/residential-and-mobile.md)
is a page read, and no proxy in this topic was dialled.
