# Usenet

Usenet is a separate retrieval network with its own providers and its own
indexers. A provider sells access to a spool of articles; an indexer turns a name
into an NZB. A reader needs one of each, and the two halves fail differently.

## The answer

⛔ **There is no free usenet path that clears 50 GiB a month, and none that
recurs.** The card-free offers are one-off allowances: Usenet.farm 10 GB,
UsenetAgency 30 GB over 7 days, Bulknews 10 GB listed free. That is 40 GB
confirmed and 50 GB at most, once per person.

The cheapest way to clear 50 GiB a month is a prepaid block on an independent
backbone. XS News sells 5,000 GB for EUR 59.95, which is EUR 11.99/TB, but it
takes a card or an EU bank transfer. The practical pick is **Cheapnews, 1,000 GB
for EUR 24.95**, which covers a year at that rate and is the only cheap block
whose vendor page lists crypto.

## The trap that decides the price

⭐ **Omicron sells one spool through eight storefronts.** Newshosting, Eweka,
UsenetServer, Tweaknews, Newsgroup Ninja, Sunny Usenet, Astraweb and Easynews all
draw on the same backbone. Buying two of them is buying one feed, and every
comparison table that ranks them separately is ranking one product eight times.

Four other groups matter for the same reason:

| backbone | storefronts recorded here |
| --- | --- |
| Omicron | Newshosting, Eweka, UsenetServer, Tweaknews, Newsgroup Ninja, Sunny, Astraweb, Easynews |
| UsenetExpress | UsenetExpress, Newsdemon, ThunderNews, CubeNet, UsenetPrime, Fastusenet |
| Abavia | XS News, Usenet.farm |
| independent | Vipernews, Giganews, Frugal Usenet, Cheapnews, Blocknews |

## The free offers, exactly

| provider | what it gives | card | recurs |
| --- | --- | --- | --- |
| Usenet.farm | 10 GB, stated in the page source | no | no |
| UsenetAgency | 30 GB over 7 days, "No auto billing" | no | no, one account |
| Bulknews | 10 GB listed FREE | unstated | no |
| UsenetMax | free NNTP server, 3 connections | no | unknown |
| Cheapnews | "Free 20GB Trial, no credit card needed" in prose, EUR 3.90 on the plan card | contradictory | no |

⚠ **A form is not a registration, and a trial banner is not a trial.** Two vendors
refuse a trial outright: Newshosting's knowledge base says it "does not currently
offer a free trial", and NewsDemon's `/free-trial` page says the same. Two more
gate it behind a payment step: Fastusenet's step 3 of 4 is Payment Information,
and Giganews' trials run through `billing_redirect.html`.

## Prices that matter

| provider | price | retention | connections | note |
| --- | --- | --- | --- | --- |
| XS News | EUR 59.95 per 5,000 GB | 3,800 days | 100 | EUR 11.99/TB, the per-TB floor |
| Cheapnews | EUR 24.95 per 1,000 GB | 4,000 days | 50 | crypto listed |
| Blocknews | USD 7.50 per 250 GB | 6,000 days | 50 | block, no expiry |
| Usenet.farm | EUR 4.95/month | 5,000 days | 50 | independent, NL |
| Frugal Usenet | USD 4.99/month | 5,800 days | 20 | Netnews plus upstream |
| Newsdemon | USD 28/year | 5,600 days | 60 | UsenetExpress backbone |
| Eweka | EUR 6.99 promo against EUR 14.49 list | 6,412 days | 50 | Omicron, EU notice regime |
| Newshosting | USD 12.95 against USD 19.94 list | 6,415 days | 100 | Omicron, US |

⭐ **The promo is not a cliff.** Eweka's "52% off" is computed against a list price
the vendor has not charged for 37 months, and neither Eweka nor Newshosting
publishes a renewal rate. Treat the list as an anchor and the promo as the price.

⚠ **Giganews claims 3,200+ days and the r/usenet provider map records 550 days for
binaries.** That is the widest vendor and community disagreement in this topic.
The record keeps 550 and says so.

## What is dead

- **XS Usenet**, which called itself "the first freemium Usenet provider" since
 2009, shut down in 2026 and migrated accounts to EasyUsenet.
- **CARNET's academic Usenet** closed on 2026-02-20, which removes one
 institutional route.
- **Astraweb and Bulknews** are alive. Their storage records are incomplete:
 Astraweb's carries no retention and no blocks, and Bulknews' block ladder from
 20 GB to 6,000 GB is missing.

## The indexer half

A provider without an indexer is a spool with no table of contents.

⭐ **The only indexer that gives a working API for nothing is the public Spotweb
layer.** `nzbserver.com` and `spotnzb.com` answer a full Newznab API (`t=caps`,
`t=search`, `t=g`) with no account, no key and no published daily limit. Their
NZB for the same message-id is byte-identical, so they are one catalogue at two
hostnames: failover, not extra coverage.

⚠ **That API clamps a large limit silently.** Measured ladder: `limit=500`
returns 178 items, `200` returns 178, `100` returns 100, and `501`, `999` and
`1000` all return the 50-result default, every one HTTP 200 with no error
element. A client asking for 1,000 gets fewer results than one asking for 200.

Account-based indexers are mostly shut:

| indexer | registration | free API allowance |
| --- | --- | --- |
| NZBFinder | open | 25 hits/day, reported |
| Usenet Crawler | open | 10,000 claimed |
| Treasure Maps | open | not published |
| NZB.life | open | not published |
| NZBGeek | `available=no open=no` | none usable |
| DrunkenSlug | `available=yes open=no` | none |
| Tabula Rasa | `available=no` | none |
| NinjaCentral | `available=yes open=no` | none |
| NZBPlanet | `open=no` | browse only |

Two deaths carry opposite signatures. `nzb.su` answers with an explicit error:
"This API endpoint has been retired. Update your indexer URL from nzb.su to
nzb.life." SimplyNZBs answers three times differently and then redirects to a
parking host, which is why a redirect target is worth reading before a verdict.

## How it composes

A block plus a public Spotweb index is the cheapest usenet pair with no
subscription: EUR 24.95 for a year of 50 GiB/month, against a free index. A
debrid does not help here; it retrieves from file hosts, not from a spool.

⚠ **The block outlives the plan, and that is the point.** XS News says "Data never
expires", Blocknews "Keep Your Gigs Until Used", Cheapnews "without any
time-limits". The bytes are prepaid and the articles sit on the spool for 3,000
to 4,000 days. That makes a block the best fetch-now-read-later store in the whole
topic, and the only one where a lapse costs nothing.
