# Per-object ceilings: the number that sets the shard size

A shard is one slice of a file, sized to a provider's per-object cap. A plan
shards across providers, so the largest single object each accepts sets the chunk
size, and the chunk size sets the file count, and the file count is what most of these
providers actually bill. Getting this wrong is the most expensive arithmetic error
available in this topic, because it is silent: a table that lists a repository total
as a per-object cap sets the chunk size 130 times too high, and nothing in the upload
fails until the bill arrives or the quota runs out.

## The ceilings, largest first

Every row is a per-object figure, not a total. Where a report gave a
total, the two numbers are separate, and the note says which is which.

| provider | per-object ceiling | retention | rung and date |
|---|---|---|---|
| file.kiwi | 999 GiB | 90 hours | `documented`, 2026-10-21 |
| Ollama registry | 455.5 GiB (not in the `library/` namespace) | none published | `documented`, 2026-10-21; `library/` layer measured at 42,520,398,528 B |
| GigaFile | 300 GB | 3 to 100 days, chosen at upload | `documented`, 2026-10-22 |
| firestorage.jp | 300 GiB | 3 days default, 14 days maximum, chosen at upload | `reported`, 2026-10-21 |
| BigFile.net | 256 GB | 365-day sliding | `measured`, 2026-10-22, byte-identical roundtrip |
| FileDitch | 155 GiB | not published | `documented`, 2026-10-21, from the uploader JS constant |
| axfc | 128 GiB | not published | `measured`, 2026-10-22: 200, 21,146 B, form constant 137438953472 |
| Civitai | 65.83 GiB | none published | `documented`, 2026-10-21 |
| CNB | 64 GB | none published | `documented`, 2026-10-21; needs a WeChat identity |
| FEX.NET | 50 GB per unregistered share | not published | `documented`, 2026-10-21 |
| SwissTransfer | 50 GB per transfer | 7 to 30 days | `documented`, 2026-10-21 |
| OpenCSG | 6.58 GB, the largest of 163 shards | none published | `measured`, 2026-10-22: tree API 200, 150,045 B |
| GitHub Releases | 2 GiB | none, while the repo lives | `documented`, 2026-10-22 |
| Cloudflare Pages | 25 MiB | none, plus a full-deploy write path | `documented`, 2026-10-22 |

The first two rows are the ones that mislead. file.kiwi's 999 GiB is the largest single
object in this topic and it lives for 90 hours, which makes it a transfer bus rather than
storage.

The pattern is narrower than "the biggest caps have the shortest clocks", and the column that
makes it visible is the retention cell rather than the sort. The top two rows are anonymous file
hosts and both carry a clock. Five of the ten largest caps carry none: Ollama at 455.5 GiB,
Civitai at 65.83 GiB, CNB at 64 GB and GitHub Releases at 2 GiB publish no expiry, and axfc at
128 GiB publishes none either. Those five are model hubs and code forges, where the object lives
until the account or the repository does. So the rule is a property of the anonymous file-host
class and not of size: a large object there is a bus, and a large object on a forge is storage.

## OpenCSG is a repository total, not an object cap

OpenCSG's 688.6 GB is a repository total, not a per-object cap. The tree API settles it.
`GET https://hub.opencsg.com/api/v1/models/deepseek-ai/DeepSeek-V3/tree` returned 200
with 150,045 bytes on 2026-10-22 (`measured`: 200, 150,045 B): 176 files, 688,603,604,082 bytes in
total, of which 163 are shards above 1 GB, and the largest single object is
6,584,784,447 bytes.

So the repository ceiling is at least 688.6 GB and the object ceiling is 6.58 GB. A
plan built on the first number would chunk at 688 GB and fail on the first upload. The
same API also shows the read path trap: the plain `resolve/` path answers 200 with a
135-byte LFS pointer, so a client that trusts the status code downloads 135 bytes and
reports success.

## Pages is file-count-bound, and the break-even is one number

Cloudflare Pages holds 100 projects x 20,000 files x 25 MiB, which is 2,000,000 slots
and 47.68 TiB per account. The limits page states all three numbers verbatim
(`documented`, 2026-10-22: 200, 7,360 B). 100 x 20,000 x 25 MiB = 47.68 TiB.

An archive of 20 TiB divides into that 2,000,000-slot budget at a mean object of 10.49
MiB. That is the break-even and it is the only number that matters:

| mean object size | files needed for 20 TiB | accounts required |
|---|---|---|
| 25 MiB | 838,861 | 0.42 |
| 16 MiB | 1,310,720 | 0.66 |
| 10.49 MiB | 2,000,000 | 1.00 |
| 8 MiB | 2,621,440 | 1.31 |
| 4 MiB | 5,242,880 | 2.62 |
| 1 MiB | 20,971,520 | 10.49 |
| 100 KiB | 214,748,365 | 107.37 |

This is a cliff, not a gradient. A single `tar`-per-directory step moves an archive of
small files from "needs 108 accounts" to "fits in 2 projects", which makes consolidation
the highest-leverage action in the free-tier plan and not an optimisation. The common
shape of raw scraped data is many small files, so the unfavourable reading is the
default one.

The write path reinforces it. A Pages deploy is a full-project upload, not an
incremental PUT: `wrangler` re-uploads any object whose hash is not already in the
deployment, page creation is throttled for a new account's first 48 hours, and an archive of
20 TiB at the cap is 42 projects of 20,000 files each. Nothing breaks; it is hours of
wall time, and a reason to build the archive once rather than iterate on it.

## Pages serves no ranges

A `Range: bytes=0-1023` request to three Pages-served assets returned `200` with the
full `Content-Length`, no `Content-Range` and no `Accept-Ranges`, on 2026-10-22. One asset
was probed three times and the other two once each. The probe that follows was re-run
(`measured`: 200, 749 B, no `Content-Range`):

```bash
curl -qsS -D - -o /dev/null -H 'Range: bytes=0-1023' https://astro-docs.pages.dev/favicon.svg
```

The response carries `HTTP/1.1 200 OK`, `Content-Length: 749`, and no range headers.
The same request against a GitHub release asset returned `302` followed by
`206 Partial Content`, `Content-Range: bytes 0-1023/13149392`.

So Pages is an archive downloaded whole. It rules Pages out as a serving tier, a
resumable fetch, a video seek, or a parallel ranged read. For a cold archive read
rarely and in full, that is acceptable; for anything else it is disqualifying.

## Chunk sizing, as a procedure

The order matters, because each step constrains the next.

1. **Measure the mean object size of the archive.** This is the number the whole plan
   turns on and it is the one nobody has. It decides how many Pages accounts the
   archive needs before any provider choice is made.
2. **Consolidate to at least 10.49 MiB where the archive target is Pages.** `tar` or
   `parquet` per directory. Below that threshold the provider is worse than Zenodo.
3. **Set the chunk size to the smallest ceiling among the providers you will
   actually use**, not the largest. A pool is bounded by its narrowest member.
4. **Check the chunk count against every file-count cap in the pool**, not just the
   byte total. TeraBox's free tier caps at 500 files, which makes its 1 TB
   unreachable at any realistic object size.
5. **Re-check the read path per provider.** A ranged read is what makes parallel fetch
   possible, and it is not implied by the write path. RepOD answers 206 on a 7,459 B
   text file and 200 on a 116 MB binary, and the discriminator is not visible from
   outside.

## The trap in a shard table

A shard table with every cell filled is a table that moved its gaps into plausible
values. Two specific errors recur.

The first is listing a repository total as an object cap, which sets the chunk 130
times too high. The second is merging two providers into one row, which happened to
FEX.NET and FileDitch: the 155 GiB figure belongs to FileDitch's uploader constant, and
FEX's ceiling is 50 GB per unregistered share.

A third is subtler and costs an hour rather than a research pass: the same GitHub file is 20 MB
on jsDelivr's `/gh/` path, 50 MB on raw.githack, and 64 MB on unpkg and hop.js. One
npm account plus 45 MB shards gives four independent free CDNs over one write, and a
shard sized to the wrong CDN silently 403s.
