# Korea and Japan: the international tier, and what it costs in identity

The Korean and Japanese consumer pans are reachable in a way the Chinese set is not
and they are small in a way that makes them mostly irrelevant at the scale this
topic targets. This document records what exists, what could be established, and the two
that are worth a second look.

The answer: **TeraBox's 1 TB tier is the only one in this region that clears the
500 GiB floor, and its limits page could not be read.** Everything else here is
tens of gigabytes.

## The comparison

Sorted by quota, because the identity cost is similar across the set and the quota
is what separates them.

| service | free tier | per-file cap | identity | what it is | verdict |
| --- | --- | --- | --- | --- | --- |
| TeraBox | 1 TB | 128 GB shared | `email` | a Japanese-operated consumer drive with a global app | qualifies-with-caveat |
| PikPak | not established | not established | `email` | a Singapore-operated drive built around cloud download | unverified |
| Naver MYBOX | not established | not established | `country-phone(kr)` | a Korean portal drive | fails-identity |
| Kakao Drive | closed | - | `country-phone(kr)` | discontinued | dead |
| N Drive | not established | not established | `country-phone(jp)` | a Japanese carrier drive | fails-identity |

⚠ **Two of the five rows say `not established` and the reason is the same for
both.** Neither Naver's nor N Drive's limits page could be read, so no number is
asserted. A `dash` is a finding; a plausible number would not be.

## TeraBox

TeraBox offers a terabyte free on registration. The vendor states the figure as
1,024 GB, which is read here as a decimal 1.02 TB and quoted as 1 TB. The figure
comes from the site's own title and the app store listing, both read 2026-10-22
(`reported`, 2026-10-22). The share limit is 128 GB.

Three things are `unverified` and each one matters:

- **The per-file upload cap.** 128 GB is the *sharing* figure the app listing
  states. It is not established as the upload cap.
- **Retention.** No page read for this record states how long a dormant account
  keeps its files.
- **Egress terms.** No page read for this record states a download cap or a speed
  tier.

⛔ **The landing page returned a verification interstitial rather than the page.**
`terabox.com` resolved to `/simple-verify` with the body "Verification code was
entered incorrectly". That is why this record is `reported` and not `documented`,
and it is why the three gaps above are gaps and not oversights.

Verdict: `qualifies-with-caveat`, binding `per-object-cap`. 1 TiB free is the
largest single-tier free quota in the consumer set and none of its limits could be
confirmed first-hand.

## PikPak

A private cloud drive whose selling point is a server-side cloud-download engine:
a magnet or a torrent goes in and the file arrives on PikPak's disk in seconds,
which the landing page claims for "more than 80% of the files".

That is a claim about **acquisition**, not storage, and it is the reason PikPak
appears in this topic at all. A reader who needs to fetch a corpus from BitTorrent
has a real use for it.

What could not be established: the quota, the cap, the retention and the egress
terms. **The pricing page is served as a binary body**; the read broker refused it
as `not-html:binary` and the fetch broker returned a compressed body. The record is
`unverified` with that reason.

Verdict: `fails-quota` as recorded, because nothing numeric was established and an
unestablished quota cannot be relied on. The verdict is a statement about this
record and not about the service.

⛔ **Do not upgrade this record without reading the pricing page.** A browser that
renders that page can move it to `documented` in one call, and that is the cheapest
open item in this topic.

## The carrier drives, and why they are closed

Naver MYBOX and N Drive are portal or carrier products, and both are gated on a
domestic phone number and a domestic identity. They are recorded as
`fails-identity` and not explored further, because no route to a foreign
registration was found and there is no reason to expect one.

⚠ **`fails-identity` is a verdict and not a note.** A large quota behind a Korean
resident's phone is worth zero to a reader without one, and a table that lists it
beside a reachable tier without saying so has misled its reader.

## Chaining

TeraBox has no documented public API. The routes that exist are third-party
drivers, and the reliable pattern is a bridge:

```
TeraBox (email, 1 TB) -> a third-party driver in OpenList or Cloudreve -> CDN -> reader
```

⚠ **A third-party driver is a dependency on somebody else's reverse engineering.**
It breaks when the pan changes its private API, and the pan has no obligation to
announce that. That is a different risk from a public instance dying, and it is
recorded per instance in `extras.upstream_provider`.
