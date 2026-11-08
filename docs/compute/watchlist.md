# Sources that change without notice, and when to re-read them

Most of this topic is a vendor page that states a price and may revise it. A smaller set of
sources is different: it publishes a *table of other vendors*, it updates on its own
schedule, and it names providers this corpus has never heard of. Those are worth a standing
re-read rather than a one-off citation, because a single fetch gives a snapshot and the next
fetch gives a different market.

This page lists them, says what each is good for, and says what it is not.

⛔ **A comparison page is `reported` for every vendor except the one that publishes it.** The
publisher is first-party about its own price and a competitor about everyone else's. Take the
name and the claim from the table, then read the vendor's own page before recording a number
as `documented`.

## The standing list

| source | what it publishes | re-read | what it is not |
|---|---|---|---|
| `https://boat.dev/compare` | fourteen sandbox and devbox providers at one 4 vCPU / 8 GB shape, with list prices dated in the page, plus a fleet-price table and a benchmark comparison | monthly | not a free-tier list. It compares paid hourly rates, and its own free trial is described three different ways across its docs, homepage and this page |
| `https://www.computeprices.com/` | 116 providers of per-GPU rates by card, with a last-updated date per page; 51 were unrecorded on 2026-10-22 | monthly | not a capacity list. A price with no host behind it is a reference rate, and the page does not say whether the card is rentable now |
| `https://skycisa.com/` | a second per-GPU index, useful as a cross-check when the first disagrees | quarterly | not authoritative on any single vendor |
| `https://sandboxprices.com/` | modelled monthly cost for 160 sandbox, microVM and container products, one isolation type and one startup time per row, with first-party rate assertions behind each priced row. The whole catalogue is also served as JSON at `https://api.sandboxprices.com/api/products`, which is how it is diffed | monthly | not a VPS list and not a free-tier list. ⛔ **Its headline month is 200 active hours, not 730**, so every time-based rate is optimistic by up to 3.65 times; the row it prices is a 0.25 vCPU slice rounded up to the smallest purchasable box; and egress, regional multipliers and concurrency are excluded. The publisher says 99 of 160 rows are source-checked. Take the name and the claim, then read the vendor page and recompute at 730 hours |
| `https://github.com/AnicetNgrt/hpc-sandbox-benchmarks` | the same Node.js build-and-test loop run on each sandbox provider's 4 vCPU / 8 GB machine, as a leaderboard with dates | quarterly | not a price. It measures throughput, and a faster machine at a higher rate can still be the cheaper one |
| `https://vpspricetracker.com/providers` | a provider index of 128 cheap-VPS hosts, each with a page of its cheapest, largest and fastest offers at named specs, locations and prices | monthly | not a price guarantee. Its rows carry no date, it merges IPv4 and IPv6 shapes, it fills an unstated allowance with a port-derived number, and it lists plans the vendor does not sell |
| `https://free-for.dev/` | a maintained list of developer free tiers, by category | monthly | not verified. Every entry needs the vendor page read before it becomes a record |
| `https://github.com/ariana-dot-dev/battleships` | 369 provider cards under `research/cards/`, each with a category, isolation model, per-vCPU-hour or per-size rate, egress term and quoted evidence | quarterly | not a free-tier list, and not first-party. A card is `reported` until the vendor page is read. It is a discovery and cross-check set, not a source of verdicts |
| `https://old.reddit.com/r/selfhosted/` and `r/webhosting` | user reports of what broke, throttled or closed | monthly | not evidence of a quota. A report is a lead |
| `https://lowendbox.com/feed/` | daily offers from hosts that appear on no index, with the plan and price in the post; the RSS titles carry host and plan | fortnightly | an advertisement, often affiliate-linked. The renewal price and the stock are the vendor's to state |
| `https://lowendtalk.com/categories/offers` | forum offers, including hosts too small for a directory | fortnightly | a post is not a product. Cloudflare walls the reader; use the broker's search with `--domains lowendtalk.com` |
| `https://www.serverhunter.com/` | a VPS search engine faceted by provider, location and price; its own counter says 971 providers and a diff on 2026-10-22 found **857 unrecorded** | monthly | it lists what providers submit, and a provider that does not submit is invisible |
| `https://www.vpsbenchmarks.com/` | 76 providers it has benchmarked, with published prices and measured scores; 46 were unrecorded on 2026-10-22 | monthly | the benchmark set is smaller than the market, and a missing provider is not a bad one |
| `https://www.gpuperhour.com/` | a GPU rate index by card and host, with the cheapest row per card | monthly | a rate with no stock behind it; the card class and the VRAM are often unstated |
| `https://cloud-gpus.com/` | a GPU price index across clouds and brokers | monthly | a rate with no stock behind it |
| `https://vps.today/` | a Russian-run price index with hourly and monthly tariffs per host; claims 119 hosters and 1,825 tariffs | monthly | the claim is its own. Fourteen records came from it and three of its names had no vendor page |
| `https://poiskvps.ru/` | a Russian VPS search and price index | monthly | domestic offers are usually gated on a Russian document |
| `https://hostings.info/` | a Russian hosting catalogue with tariffs | quarterly | catalogue entries rot; several list plans the host no longer sells |
| `https://www.zhujiceping.com/` | Chinese VPS reviews and offer posts | monthly | review posts carry affiliate links and stale prices |
| `https://hostloc.com/` | the largest Chinese-language VPS forum: new providers, reseller offers, and enforcement reports | monthly | not readable without an account for some threads. Use the broker's search with `--domains hostloc.com` and read the snippet |
| `https://www.nodeseek.com/` | a second Chinese-language forum, stronger on new small hosts and on shutdown notices | monthly | blocks some readers by IPv6; a redirect to a warning page is a wall, not a dead provider |
| `https://linux.do/` | Chinese-language forum where free-tier offers are posted with the real cap in the thread | monthly | threads frequently render empty to a text extractor; the search snippet carries the post body |
| `https://arca.live/` and `https://www.clien.net/` | Korean-language operator forums, where domestic free tiers are announced | quarterly | domestic-only offers are usually gated on a Korean phone number, which is a `fails-identity` finding |
| `https://4pda.to/` and `https://habr.com/` | Russian-language forums, where CIS hosting offers and grants appear | quarterly | the same caveat: a local identity document is usually the gate |

## Why boat's comparison page is on the list

It is one of very few pages that prices a dozen competitors at one shape on one date. That
makes it a cheap cross-check: when this corpus quotes a sandbox rate, the comparison table
either agrees or gives a reason to re-read the vendor. It is also a lead generator, because
the vendors it names change, and a name that appears there and not in `dossier/compute/` is
a provider this topic has missed.

⚠ **Its own product is described three ways.** The page says "25 free hours to start", the
documentation says a 7-day trial with lower limits, and the homepage says 7 days then from
USD 20. Reading one page of a vendor is how a record gets a wrong free tier.

## What the provider trackers show

Two inventories were diffed against `dossier/compute/`, and they agree on almost nothing.

**The sandbox corpus is saturated.** The 369-card corpus was fetched on 2026-10-22 and compared
with the dossier by host name. **368 of its 369 providers already had a record**, which is the
strongest coverage signal this topic has: an independent curated list of sandboxes, browsers,
devboxes and hyperscalers, and almost nothing in it was new. The one that was missing,
`tangle-sandbox`, is now a record.

**The cheap-VPS tracker was not.** `vpspricetracker.com` listed 128 providers on 2026-10-23 and
**106 had no record at all**. `paid/lowend-vps.md` now holds 114 of them. The lesson: 368 of
369 sounded like coverage and was coverage of one market only. A corpus can be complete
against a sandbox list and empty against the low-end VPS list, because those are different
lists.

⚠ **A name comparison can over-count or under-count a gap.** Comparing full
host names left three providers unmatched that were covered, so
`docs.steel.dev` did not match a record filed under `steel.dev`; matching
provider names by substring treated eight names as covered when they were not,
including `hostbrr`, which a document already quoted with no record behind it.
Compare the registrable domain, then open the record, then write.

## How to use a source on this list

1. Fetch it, and note the date the source itself claims for its data, not the date you read it.
2. Extract the names, not the numbers, on the first pass.
3. For each name, check `dossier/compute/<slug>.json`. A name with no record is the finding.
4. For a name with a record, compare and record a disagreement as an evidence row, attributed
   to the source and marked `reported`.
5. Re-date the source's row rather than deleting it, so the next reader sees the movement.
