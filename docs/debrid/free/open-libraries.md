# Open libraries

Not every byte needs a debrid. A research workload is often public data, papers or
models, and those are free by design, with no account and no quota. This
document records where that is true, how fast it is, and where the free path is a
false 200.

## The answer

⭐ **Hugging Face Hub gives the most bytes a day with no account: 39.98 MiB/s
measured on a complete 548,118,077-byte file over one connection**, which is about
3.3 TiB a day if the rate held. Common Crawl is second at a flat 20 MiB/s, and the
Internet Archive third at 3.17 MiB/s single and 8.0 MiB/s at eight connections.

⚠ **Every other source in this class is metadata-shaped.** A catalogue API returns
tens of kilobytes to a few megabytes per call, so its bytes a day are set by the
call rate, not the bandwidth. An account buys request headroom there, not bytes.

## The measured sources

| source | rate | connections | note |
| --- | --- | --- | --- |
| Hugging Face Hub | 39.98 MiB/s | 1 | 548,118,077 bytes, whole file |
| Common Crawl | about 20 MiB/s | flat | HTTP and S3 paths |
| Internet Archive | 3.17 MiB/s | 1 | 8.0 MiB/s at 8 |
| Wikimedia dumps | 3.6x from 1 to 8 | scales | latency-bound |
| World Bank API | 21x from 1 to 8 | scales | call-bound, not byte-bound |

⭐ **Parallel connections are not a multiplier, and at Hugging Face they halve
throughput.** Three 256 MiB runs: 36.6, 34.8 and 36.6 MiB/s at one connection
against 17.1, 21.3 and 20.4 at eight. The variable is whether the host shapes bytes
or calls.

⚠ **A short span measures the ramp, not the rate.** A 32 MiB span makes the
Internet Archive look like it ignores parallelism at 2.75 to 5.39 MiB/s; a 256 MiB
span shows 2.2 to 2.6 times scaling to 8 to 11.4 MiB/s. Chunk setup hides the
effect.

## The content stores

| source | what it holds | gate | size |
| --- | --- | --- | --- |
| PubMed Central OA | about 8M article versions, world-readable S3, `accept-ranges` | none | about 880 GB |
| Internet Archive | items, metadata and download APIs | none | 1 TB per item |
| Project Gutenberg | books | none | tens of GB |
| Standard Ebooks | books | none | small |
| LibriVox | audio | none | hundreds of GB |
| Zenodo | research artefacts | email | 50 GB per record |
| OpenAlex, Crossref, Semantic Scholar | metadata | none to email | call-bound |
| Hugging Face datasets | models and datasets | none | very large |

⭐ **PubMed Central's `pmc-oa-opendata` bucket is the best anonymous content
store**: about 8 million article versions, world-readable S3, no login,
`accept-ranges: bytes`, and one XML measured at 109,974 bytes. Its legacy FTP path
was deleted in the week of 2026-08-24.

## The false 200s

| source | what happens |
| --- | --- |
| Crossref snapshot | HTTP 200 with 41 bytes of HTML |
| Standard Ebooks `.epub` | HTTP 200 with an 8,777-byte page, "Your Download Has Started!" |
| data.gov CKAN API | 404 while the human catalogue returns 200 |
| Eurostat legacy bulk TSV | 404 |
| Europe PMC FTP | HTTPS 403 and port 21 timeout |

⚠ **Standard Ebooks needs `?source=download`** to return the real 831,959-byte
EPUB, and its bulk ZIPs are a paid patrons benefit. A parser that trusts the
extension gets a web page.

## What this changes

1. **For public data, no debrid is needed.** Hugging Face and Common Crawl are
 faster than any multi-hoster measured in this topic.
2. **For papers, no account is needed.** PubMed Central and the Internet Archive
 answer anonymously.
3. **For a private file host, a debrid is still the answer**, because no open
 library holds it.
4. **Measure the span before the rate.** A 32 MiB window reports the ramp; use at
 least 256 MiB and more than one connection count.

⚠ **The line ceiling here is unknown.** `speed.cloudflare.com/__down` returned 403,
so every bytes-a-day figure is a lower bound on what the line allows, and the
Hugging Face margin may be a property of this line rather than of the host.
