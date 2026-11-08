# The sources this topic is measured against

A list read once is not a market. This file names every site that enumerates
other providers for tunnels and proxies, what each one is good for, and what it
is not. The registry is `scripts/sources/egress-aggregators.tsv`, and
`scripts/gate.sh` fails while a registered source is undiffed, overdue or absent
from this page.

⭐ **A coverage claim names the list it was measured against, in the same
sentence.** "154 entries covered" is true of one list. "The tunnel market is
known" is a claim about the world, and no single list supports it.

## What each source is for

| source | kind | every | what it enumerates | good for | not good for |
| --- | --- | --- | --- | --- | --- |
| [awesome-tunneling](https://github.com/anderspitman/awesome-tunneling) | provider index | 30 days | 154 links: 75 open source, 35 commercial, 44 overlay | the canonical name list, and the only one that marks a subset as carrying UDP | no price, no quota, and the UDP mark is 18 entries, so a name without it may still forward UDP |
| [ouicu compare](https://ouicu.com/compare) | price index | 90 days | 14 tunnels with price, free plan, protocols, warning page and open-source flag | the only structured table with a free-plan column | one author, dated 2026-10-07, and the author sells ouicu |
| [faun secure tunnels](https://faun.dev/toolbox/compare-open-source-secure-tunnels/) | price index | 90 days | 22 providers scored on 12 axes | the widest name coverage found | the scores are relative to the page and are not evidence |
| [ipwithease ngrok alternatives](https://ipwithease.com/best-ngrok-alternatives/) | price index | 180 days | 6 providers in one protocol table | a dated cross-check on the small commercial set | search content, no price and no free-tier number |
| [vpspricetracker](https://vpspricetracker.com/providers) | provider index | 30 days | 133 provider links | a price snapshot per host | no NAT or WireGuard facet, so it never surfaces an ingress product |
| [serverworth](https://serverworth.com/best-vps-for/wireguard-vpn/) | price index | 30 days | 15 hosts aimed at a WireGuard VPS | plan-level deep links for a price diff | ranks on price and never tests whether UDP arrives |
| [post4vps compare](https://post4vps.com/compare/) | price index | 30 days | 9 hosts with an IPv6 address count per plan | the one comparator that counts IPv6 addresses | small and low-end only |
| [serverhunter](https://www.serverhunter.com/) | provider index | 30 days | 971 providers and 87,838 servers | NAT IPv4 and IPv6 Only facets, which is the closest a list gets to ingress | renders plan names, so a provider diff needs the facet pages |
| [lowendbox](https://lowendbox.com/feed/) | offer feed | 14 days | one post per deal | the cheapest hosts as they appear | never a table, and a promo is rarely a renewal price |
| [lowendtalk](https://lowendtalk.com/categories/offers) | offer feed | 14 days | 21 offers per page | dated offers from small hosts | an offer is a lead and not a quota |
| [lowendtalk NAT threads](https://lowendtalk.com/discussion/199604/cheapest-nat-vps) | offer feed | 30 days | 12 sellers across 10 threads | the recurring NAT question, answered by people who bought | no per-provider dates |
| [serverdeals](https://serverdeals.cc/) | offer feed | 14 days | 47 offers from 34 hosts, with a NAT section | the best offer feed for this lane | last updated 2026-06-03, so the page is a snapshot |
| [product hunt](https://www.producthunt.com/) | corpus | 30 days | 9 launches from one query | new commercial entrants, early | no limits, no price, no continuity |
| [Hacker News Show HN](https://news.ycombinator.com/) | corpus | 30 days | 8 tools from 9 threads | a dated lead on a new tunnel | an author's announcement, not a list |
| [r/ipv6 brokers thread](https://www.reddit.com/r/ipv6/comments/y896f2/ipv6_tunnel_brokers_other_than_hurricane_electric/) | corpus | 90 days | 3 brokers beside Hurricane Electric | the only thread that names brokers | 37 lines, and the other subreddits returned operational questions |

Retired sources, with the reason and what would reopen them, are rows in the
registry with `status: retired`.

## What no list here does

⚠ **Not one of them indexes WireGuard ingress.** They index tunnels by protocol
(HTTP, TCP, UDP) or hosts by price. The question this topic asks crosses the two:
a port a WireGuard datagram can reach, with a byte allowance. Every row that
answers it was assembled from vendor pages, and the lists supplied only names.

⭐ **The `UDP` token in awesome-tunneling is a starting point and not a filter.**
18 of 154 entries carry it. A name without it may still forward UDP once a
vendor page is read, and a name with it may forward UDP only on a paid tier.

## How a diff is run

Write the diff onto the run branch, never into the tree
([`../research-protocol.md`](../research-protocol.md) section 2):

```bash
scripts/rq show RUN scripts/sources/egress-aggregators.tsv --out .tmp/RUN/tools/egress-aggregators.tsv
python scripts/sources/aggregator-diff.py --registry .tmp/RUN/tools/egress-aggregators.tsv --record lowendtalk --covered 0 --missing 21
scripts/rq put RUN scripts/sources/egress-aggregators.tsv .tmp/RUN/tools/egress-aggregators.tsv --reason "sources: diff lowendtalk"
```

In an own clone only, `--diff` with `--update` writes the registry in place:

```bash
python scripts/sources/aggregator-diff.py --registry scripts/sources/egress-aggregators.tsv --diff awesome-tunneling --html .tmp/session-ID/awesome.html --update
```

The `--diff` form extracts provider names from a saved page with the row's pattern
and updates the counts. The `--record` form records counts a person established by
reading, for a feed whose names live in prose. `--check` is what CI's gate runs.
