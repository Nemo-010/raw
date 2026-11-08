# Gaps: the claims that are weak, the contradictions that are open, and what rotted

A corpus is worth what its weakest evidenced claim is worth, because a reader cannot tell which
claim that is. This document names them. Everything here is a claim that a decision could
rest on and that is not settled, plus the contradictions that remain open.

Read this before acting on any number in the topic. The front page's withdrawn-claims table
carries what has been corrected; this page carries what is still uncertain.

## The five claims a decision would rest on, and how sure each is

| claim | rung | what would settle it | what decision it changes |
|---|---|---|---|
| the mean object size of a 20 TiB data set | `unverified` | one `find` over the data: mean size, and the share below 1 MiB | whether Cloudflare Pages needs one account or eleven |
| Cloudflare Pages serves the whole 47.68 TiB without an account-level throttle | `inferred` | a 20,000-file project, filled, served for a week | whether the archive tier is real |
| ModelScope's write throttle tolerance at 10 TiB | `inferred` | a batched 1 TiB commit, then read the error | whether the hot tier is fillable at all |
| Hetzner's discretionary 250 TB/month threshold | `documented` | an observed notice letter to a Storage Box customer, not a dedicated-server one | whether the serving tier is safe for a year |
| Internet Archive's per-IP shaping at about 145 GB/day | `documented` | a 1 GiB item, 60 seconds per stream, 1, 8 and 32 connections, with a same-machine baseline | whether the Archive can serve or only archive |

The first one is the most important and it is not a research question. It is a property of the
data, and every other number in the free lane is downstream of it.

## Contradictions closed

Four were settled by a probe rather than by an argument, and each is now a single claim in a
document.

**RepOD's range behaviour.** RepOD does not ignore `Range` uniformly. Two probes on 2026-10-22:
a 7,459-byte text file answered
`206 Partial Content` with `Content-Range: bytes 0-1023/7459` and a byte-identical first
kilobyte, and a 116,201,025-byte binary answered `200 OK` with the full length and no
`Content-Range`. Neither behaviour is general, and the entry below records it
as open rather than resolved.

**OpenCSG's 688.6 GB.** 688.6 GB is a repository total, not a per-object ceiling. The tree
API returns 176 files totalling 688,603,604,082 bytes with 163 shards above 1 GB and a largest
object of 6,584,784,447 bytes. The object cap is 6.58 GB and the repository total is 688.6 GB.

**Hi168.** The endpoint returned 526 through the fetch broker on 2026-10-22, which is a Cloudflare
origin failure rather than a TLS-chain failure. The verdict is `fails-quota`.

**The unit error in 48.8 TiB.** 100 projects x 20,000 files x 25 MiB is 48,828.125 GiB, which is
47.68 TiB. The figure 48.8 TiB is 48,828.125 GiB with the unit left unconverted.
The difference is 2.3% and it changes no decision.

## Contradictions still open

These are `conflicts[]` entries on records with a null resolution, where a probe would have to
settle the question. The 49 verdict conflicts are closed: each record carries a `resolution`
naming the winning reading, and every document prints the record's verdict rather than an
earlier row.

**Harvard Dataverse: 1 TiB, 2.5 TB, or no quota?** Three probes return three answers. The root
collection says "No quota defined" in 73 bytes, `SEE_Precursors` returns exactly
1,099,511,627,776 bytes, and `kgwas` returns 2,748,779,069,440 bytes. All three are true and only
one of them is a multiplier. What would settle it is one attempt to create a collection on a new
account, which would show whether the allocation is available or gated.

**Borealis has three verdicts in the provider table.** One row says `qualifies`, one
`qualifies-with-caveat`, one `fails-identity`. The quota probe says "No quota defined for this
collection", the signup page takes an email and a free-text affiliation, and the terms reserve
removal. The record carries one verdict and three provenance entries; two of the rows are
wrong and which two is unresolved.

**CSC Allas and LUMI-O: closed.** The provider table said `qualifies` and
`qualifies-with-caveat`; a verifier said `fails-identity` for both; three prose documents
agreed with the verifier. The endpoints answer anonymously and neither quota is observable
without a project, so the quota is real and the door is the decision. Both records carry
`verdict: fails-identity` and all three readings in `extras.conflicts[]`, and
`free/research-clouds.md` agrees with this page. It is marked closed so a reader does not
re-decide it.

**37 providers appear both as a table row and as a dead end.** Nine of them qualify in the table.
The records carry both claims. What would settle it is a probe on the current state of each,
which is 37 requests.

**Seven providers hold two records each, and four of those pairs are the same offer.** Icedrive,
pCloud, Hetzner, HostBrr, PulsedMedia and Source Cooperative each appear twice under two spellings,
because the ledger assigns the free-lane and paid-lane readings to different sections. The records
are separate dossiers with the same numbers, which is a consolidation artefact rather than a second
product. Merging each pair needs a slug rename and a ledger entry. HostBrr is the exception: its
three records are three genuinely different products (a storage box, a 16 TB coupon tier and a
storage VPS with an HDD block), and they stay separate. PulsedMedia is the pair resolved so far,
in the record rather than the prose; the other five are still open.

**PulsedMedia's 16 TB box holds two records: closed.** The vendor page publishes one product line
with four tiers (4, 8, 16 and 32 TB at EUR 8.99, 14.99, 26.99 and 63.99), so there is no second
16 TB SKU. `pulsedmedia-m10g-storage-box` is canonical and `pulsedmedia-m10g-storage-box-16tb`
carries `extras.duplicate_of` pointing at it, with every fact preserved. The second record merges
a 12 TB *seedbox* spelling into a storage-box record. A count over the directory includes this
offer twice and should filter on the field.

**The dead-end tally has six values in the corpus.** 935, 960, 948, 875, 682 and 339. Parsed: 960
raw records, 935 distinct names, 935 rows in the file, and 898 that hold no table row. This topic
states 445 rejected records with a table row and 898 that exist only in the dead-end list,
which sums to 1,343 in this topic. The other 483 are netdisk-pan records.

## What rotted

Each of these claims moved recently, and each is a data point about how fast this market changes.

**Filecoin Plus ended on 2026-10-19.** FIP-0118, the Solstice upgrade: "No new datacap is
minted; all minting and allocation methods are disabled." Fil+ was the mechanism that made
Filecoin storage free. A provider that was free last week is not free
this week.

**Buzzheavier's free tier cut twice.** Permanent, then 15 days, then an 8-day base with 2 days
per download. The vendor published the reason: the cheap storage was a reseller used beyond
its allocation at about USD 1 per TB per month, and it ended after a seizure.

**123pan's free download allowance.** 2 TB of storage with 20 GB per month of download traffic,
and the OpenAPI became a paid package. The storage number did not change and the usable product
did.

**FebBox went from 1 TB to 10 GB in March 2026.** Old blog posts still describe the 1 TB tier.

**Doubao's "unlimited" became a defined allowance in June 2026**, and the phrase it now uses is a
Chinese term for a quota rather than a number. That is the marketing-quota failure in its purest
form: a documented absence that turned into a discretionary limit.

**OSF sunsets for new projects on 2026-11-16** and reads only from 2027-02-19. **Fshare abolishes
its free tier on 2027-01-01** and purges data 30 days later. Both dates are near enough to change
a decision.

## What is not measured

Eleven things, each with the reason and the probe that would settle it.

**Transfer.it's 90-day clamp.** The upload path is a single-page app with no reachable JSON API.
`/api/options`, `/api/upload` and `/api/v2/options` all return the app's HTML, so a status code
there proves nothing. One browser-driven transfer at "1 year" would settle it.

**Any signup actually completing.** No account was created on any provider. Every
identity claim in this topic is `form-read` rather than `executed`, and the records say so in
`identity_probe`. Three are worth executing first: Ctfile, TeraBox and UpZur, because they carry
the largest quotas behind the cheapest gates.

**Ollama's throughput curve.** The shape reproduced and the magnitudes did not. One curve
used 8 MB ranges over a 10-second window; the baseline here differed. The direction, that a
single stream is throttled and fan-out is mandatory, holds.

**OpenCSG's multi-stream throughput.** The 8-parallel test reused one presigned URL,
which is the error the methodology's rule 7 warns about. A fresh URL per connection would
settle whether the 4.95 MB/s single-stream figure scales.

**Internet Archive's per-IP shaping.** Measured once, on one host, on objects too small to be
representative. A 1 GiB item with a 60-second window is the probe.

**Scaleway's Glacier rate.** Four URL variants returned empty or 404, and the record is
`unverified`. The July 2026 archive capture is the route.

**HostHatch's and Time4VPS's price tiers.** Both are client-side rendered and neither plan table
could be read from a static fetch.

**Tencent TCR's and Alibaba ACR's free egress.** Inferred from the absence of a billing line
rather than from a positive sentence. The billing document is the probe.

**Whether the 898 dead-end-only providers were paid or impossible.** About 153 rows match a price
keyword, and the reason text conflates "costs money" with "cannot reach 500 GB". A re-read
of each would let `retry_when` say "if the price drops below X" instead of "never" for that
subset.

**Hi168's current state.** The endpoint returns 526 through the broker. A probe from a host that
reaches the origin, plus a signup attempt, would settle it.

**RepOD's range discriminator.** Two probes, two answers, no visible cause. The size ladder is the
experiment: 1 KB, 1 MB, 10 MB, 100 MB, 1 GB on the same dataset.

## What is not in this topic at all

Four absences a reader should know about, because a corpus that does not name its holes invites a
reader to assume they are not there.

**No Chinese provider was signed up for.** Not one. Every Chinese row in this corpus is a form read
or a third-party report, and the pan drives are in `netdisk-pan/` for that reason.

**No throughput measurement was made at 1, 8 and 32 connections against a control.** The one
exception is a single ranged read per provider, which proves the read path and says nothing about
scaling.

**No provider was tested with a 1 TiB object.** The largest object tested was
116 MB, and the largest any record names is 688.6 GB as a repository total.

**No retention claim was tested by waiting.** Every retention number here is what a page states.
The one clamp claim in the corpus is unproven, which is why it is in the withdrawn-claims table.

## The open question this topic cannot answer

One question decides more than any of the above and it is not addressable by research: **what is
the mean object size of a 20 TiB data set?**

At 25 MiB the free archive is one Cloudflare account. At 1 MiB it is 10.5 accounts. At 100 KiB it
is 107. The entire free-tier plan turns on a number that a single `find` over the data would
produce, and no provider page in this topic matters as much as that command's output.
