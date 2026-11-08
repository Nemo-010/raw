# RepOD's blanket "Range ignored" claim is withdrawn: it serves small files and not large ones

- **When:** 2026-10-22T03:07:02Z
- **Status:** corrected
- **Supersedes:** `docs/storage/free/academic-identity.md` section "RepOD, and a range claim that is withdrawn"
- **Superseded by:** `docs/storage/free/academic-identity.md` section "RepOD, and a range claim that is withdrawn"
- **Evidence:** `curl -H 'Range: bytes=0-1023' https://repod.icm.edu.pl/api/access/datafile/39782` and the same against `/api/access/datafile/18`, run 2026-10-22; captures in `.tmp/work/w-storage/probes/`
- **Confidence:** measured

## What we believed

Two artefacts said the same thing in different words. `FINAL-REPORT.md` section 4 carried a row
reading "5 GB/file; `Range` ignored". `verify/repod.json` said "Range is accepted syntactically
but IGNORED, so parallel ranged fetch is not available on this host". The verifier had tested it
and the report had copied the conclusion, and neither had tested a second object.

## What we found

The behaviour is conditional and neither artefact is right.

`/api/access/datafile/39782` is a 7,459-byte text file. A request for `bytes=0-1023` returned
`206 Partial Content` with `Content-Range: bytes 0-1023/7459` and 1,024 bytes that are
byte-identical to the first kilobyte of a full GET. A repeat at `bytes=1000-2023` returned 206
twice with the same MD5.

`/api/access/datafile/18` is a 116,201,025-byte binary. The same request returned `200 OK` with
the full `Content-Length` and no `Content-Range`.

Ranged serving works on the small text object and fails on the large binary object, and the
discriminator is not visible from outside. Size, type and path are all candidates and none is
tested.

## How we found it

The verifier brief's sixth check is "throughput at 1, 8 and 32 connections". A range probe is the
cheapest way to satisfy it, and a probe on one object satisfies it for one object. The failure was
in the generalisation, not in the probe: one object became "this host ignores ranges", and the
sentence survived into a report that three reviews read.

The current state is recorded as two `evidence[]` entries on the record, and the document states
both results and claims neither blanket behaviour.

## What it cost us

One recommendation rests on ranged reads: parallel fetch is the only way to get useful throughput
from a host that throttles a connection. A reader who believed "ranges are ignored" would have
excluded RepOD from a serving pool for a reason that is false for small objects, and a reader who
believed the opposite would have built a ranged fetcher that silently degrades to a full download
on every large object.

The second cost is credibility. The report's own audit listed this row as confirmed.

## What a future session should do differently

Run the size ladder before writing a blanket sentence about a protocol behaviour: 1 KB, 1 MB,
10 MB, 100 MB and 1 GB on the same dataset, with the status and `Content-Range` of each recorded.
Five requests settle what one request cannot.

And when a probe result becomes a general claim, write the claim with the sample size in the same
sentence. "Ranges are ignored on the one 116 MB object tested" is true and checkable. "Range is
ignored" is a statement about a host that nobody tested.
