# What does a day of egress cost when free is not enough?

The per-gigabyte ladder, priced at the volume this topic measures so the numbers are
comparable. One day is 500 GB to 1 TiB; call it 1 TiB, which is 1,024 GiB or
1.10 TB decimal. Every figure below is multiplied out to that one day and to a
30-day month, because a per-gigabyte rate on its own tells a reader nothing.

The answer: the cheapest metered CDN rate found is USD 0.005/GB, which is USD 5.50
a day and USD 165 a month. That is the number every free claim in this topic should
be read against, and it is why a free tier that carries 3% of a day is worth
nothing.

Sorted by the all-in cost of one day at this volume.

| provider | rate | one day at 1 TiB | one month | what binds |
| --- | --- | --- | --- | --- |
| bunny.net volume network | USD 0.005/GB | USD 5.50 | USD 165 | billed per GB, with no free allowance to run out |
| bunny.net EU and NA | USD 0.01/GB | USD 11 | USD 330 | billed per GB |
| Cloudflare TURN above 1,000 GB | USD 0.05/GB | USD 55 | USD 1,650 | `per-ip-shaping`: the free 1,000 GB/month runs out in a day |
| iroh Shared relay above 100 GB | USD 0.09/GB | USD 99 | USD 2,970 | `per-ip-shaping`: the free 100 GB/month runs out in hours |
| consumer-connection proxy | USD 0.80/GB | USD 880 | USD 26,000 | `reported` from one vendor; the trial is 100 MB to 2 GB |
| GetAStatic | USD 2/month | not billable | USD 2 | `per-ip-shaping`: the 100 GB/month allowance, which is 3.3 GB/day |

The arithmetic, so a reader can check it: 1 TiB is 1,099,511,627,776 bytes, which
is 1,099.5 GB decimal. Every rate above is multiplied by 1,099.5, and the month is
thirty of those days. At USD 0.005/GB that is USD 5.50 a day. At USD 0.80/GB it is
USD 879.61 a day, which is printed as USD 880 because the rate is `reported` and a
cent belongs to a measured number.

⚠ **A binary figure would be USD 819.20 a day**, because 1,024 GiB at USD 0.80 is a
different product from 1,099.5 GB at the same rate. The 7% gap is the whole reason
a figure must carry its unit. USD 819/day is the binary computation and USD 880 is
the decimal one; both are the same rate and they are not the same computation.

## bunny.net

No free tier, a USD 1/month minimum, and USD 0.005/GB on the volume network
against USD 0.01/GB in EU and North America (`documented`, 2026-10-22). A pull zone
in front of an origin is the whole product.

At this volume the volume-network rate is USD 5.50 a day. That is the cheapest
metered path found and the price of not solving the problem.

Evidence: `bunny.net/pricing/` (read 2026-10-22); `dossier/egress/bunny-net.json`.

Verdict: `paid-only`.

## Cloudflare TURN above the free allowance

USD 0.05/GB after the first 1,000 GB each month, with the SFU sharing that
allowance (`documented`, 2026-10-22). The free 1,000 GB is spent before the first
day of this workload ends, so the marginal rate is the rate.

USD 0.05/GB on 1 TiB is USD 55 a day, which is ten times bunny.net for a worse
product.

Evidence: `developers.cloudflare.com/realtime/sfu/platform/pricing/` (read
2026-10-22); `dossier/egress/cloudflare-turn.json`.

Verdict: `fails-quota` on the free tier and the wrong shape on the paid one.

## iroh Shared relay above the free allowance

USD 0.09/GB after 100 GB per month, with a 5 MB/s per-connection rate limit
(`documented`, 2026-10-22). The free allowance is gone in about three hours of a
1 TiB day.

USD 0.09/GB on 1 TiB is USD 99 a day. This is the rate that decides the case against it:
iroh is an excellent transport and its paid relay is the most expensive per-gigabyte
option in the topic, so the 7 to 10% of connections that fail to hole-punch cost more
than the storage they serve.

Evidence: `docs.iroh.computer/iroh-services/relays/shared` (read 2026-10-22);
`dossier/egress/iroh-shared-relay.json`.

Verdict: `fails-quota`.

## Consumer-connection and mobile proxies

Trials run 100 MB to 2 GB over 3 to 14 days, gated on a card, KYC or a minimum
top-up. The cheapest rate found after the trial is USD 0.80/GB
(`reported`, from the vendor pricing pages read on 2026-10-22).

At USD 0.80/GB one day is about USD 880 and a month is about USD 26,000. This is not a
capacity source at any price. It stays recorded because the search results for "free
proxy trial" are confidently wrong in the direction that flatters the provider, and a
reader will meet them.

⚠ **The rung sets the precision.** One vendor page read here is not a market survey,
so the row carries two significant figures and the day total is not printed to the
cent. The same applies to the `USD 0.80/GB` itself: it is the cheapest rate seen
and not a median.

Evidence: `geonode.com/pricing` (read 2026-10-22);
`dossier/egress/residential-proxy-trial.json`.

Verdict: `fails-quota` as capacity. It remains usable as a source of rotating
consumer-connection addresses, a different job with its own per-gigabyte
budget.

## GetAStatic

USD 2/month for a dedicated US IPv4 with 100 GB and 20 Mbit/s
(`documented`, 2026-10-22). 100 GB/month is 3.3 GB/day, so the tier cannot carry
the workload and the price is not the interesting number.

Evidence: `getastatic.com/pricing` (read 2026-10-22);
`dossier/egress/getastatic.json`.

Verdict: `paid-only`.

## What did not work

- **Cloudflare TURN as a bulk paid path**: USD 55 a day for a relay this workload does
  not need.
- **iroh Shared relay as a paid path**: USD 99 a day.
- **Consumer-connection proxies**: about USD 880 a day at the cheapest rate seen,
  reported from one vendor.
- **portmap.io and stayport.io**: `/pricing` returned 404 on 2026-10-22, so no
  current number exists to compare.
- **A free static IPv4 with open ports**: no such product, at any tier.

## Chaining

The paid lane exists to cover what the free lane cannot, and there is one chain
worth stating: `GitHub Releases or R2 for the bytes -> a CDN only if the request
pattern defeats the free front`. The scarce link is the object cap, not the money,
because the free paths bind on size and the paid paths bind on volume. A reader
paying per gigabyte has chosen the wrong constraint to spend money on.
