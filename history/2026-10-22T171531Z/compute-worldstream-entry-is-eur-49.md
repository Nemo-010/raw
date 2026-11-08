# Worldstream's entry server is EUR 49, not the EUR 104 on its banner

- **When:** 2026-10-22T17:15:31Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/worldstream.json`, `free_tier.stated` naming the EPYC 4000 series at "From EUR 104 per month" as the entry point, and `binding: none`
- **Superseded by:** `dossier/compute/worldstream.json`, which now carries the EUR 49 Xeon entry and `binding: volume-quota`
- **Evidence:** `https://www.worldstream.com/en/dedicated-server` and `https://www.worldstream.com/en/configure/110`, read 2026-10-22; the offer list is client-rendered, so the specification came from the page's own configuration name and processor selector
- **Confidence:** documented

## What we believed

That the cheapest Worldstream dedicated server was the AMD EPYC 4000 series at EUR 104 a
month, because that is the figure the landing banner prints, and that no quota bound above
the scale, because the landing page states no traffic term.

## What we found

The vendor's own offer list carries 43 entries and the cheapest is not the one on the banner:
a Fujitsu PRIMERGY RX1330 M3 with an Intel Xeon E3-1230v6 at 4 cores and 8 threads, 16 GB of
RAM, one 250 GB SSD and a 1 Gbit/s full-duplex port, at EUR 49.00 a month with 50 TB of
traffic included and delivery within two hours. No setup fee is published. Traffic past the
allowance is priced rather than refused: 100 TB costs EUR 50 a month more and unmetered
costs EUR 99 more.

Two traps sat on the same page. The offer list is client-rendered, so only the raw HTML
carries it. And the schema.org block on the entry configuration is stale: it still describes
the EPYC 4245P at EUR 135, which is a different configuration at `/configure/156`.

## What it changes

The record's entry price halves, its shape gains the RAM, disk, port and term it had left
null, and its binding moves from `none` to `volume-quota`, because a 50 TB allowance is a
ceiling a serving workload reaches. The price stays in EUR with no USD figure, because the
vendor publishes none and a conversion would be an invented number.

The minimum-term clause is still unstated rather than absent: `/en/terms-and-conditions`
returned 404, so the record says the term was not read.
