# OpenCSG's 688.6 GB was a repository total, and the per-object cap is 6.58 GB

- **When:** 2026-10-22T03:07:19Z
- **Status:** corrected
- **Supersedes:** `docs/storage/free/sharding.md` section "The ceilings, largest first" and `docs/storage/free/models-and-media.md` section "OpenCSG: the repository total is not the object cap"
- **Superseded by:** `docs/storage/free/sharding.md` section "The ceilings, largest first"
- **Evidence:** `GET https://hub.opencsg.com/api/v1/models/deepseek-ai/DeepSeek-V3/tree` returned 200 with 150,045 bytes on 2026-10-22; capture in `.tmp/work/w-storage/probes/opencsg-tree.json`
- **Confidence:** measured

## What we believed

Two artefacts disagreed and both were published. `TOP-FINDINGS.md` listed OpenCSG in a
per-object table at "688.6 GB model (multi-shard)". `FINAL-REPORT.md` section 6 carried the same
row at position two of the same table, above GigaFile's 300 GB, in a table whose stated purpose
was "sets your shard size".

The report's own audit caught it and called it "the worst arithmetic defect in the report": 130
times the real shard, in the one table whose entire purpose is to set the chunk size. The audit
moved the row to the bottom at "~5.2 GB/shard" and left the repository total in the capacity
section.

Neither number had been read off the platform's own index. Both were arithmetic over a file
listing.

## What we found

The tree API settles it precisely.

176 files. 688,603,604,082 bytes in total. 163 of them are shards above 1 GB. The largest single
object is 6,584,784,447 bytes.

So the repository total is 688.6 GB, the per-object cap is 6.58 GB, and the audit's "~5.2 GB"
was the largest blob in a different repository. Four numbers were circulating and only two of them
are the same measurement.

The same probe re-confirmed the read-path trap. `GET .../resolve/main/model-00001-of-00005.safetensors`
returned 200 with 135 bytes, which is a git-lfs pointer:
`version https://git-lfs.github.com/spec/v1`, `oid sha256:31d6a825...`, `size 3996250744`. A client
that trusts the status code downloads 135 bytes and reports success.

## How we found it

The API returns the whole tree with sizes in one response, which makes the arithmetic trivial and
is why the absence of this request in three waves is the finding. A 150 KB JSON body answered a
question that a report, an audit and a findings file had each answered differently.

## What it cost us

A plan built on 688.6 GB would chunk at 688 GB and fail at the first upload, having wasted the
transfer. A plan built on the audit's 5.2 GB would chunk 21% below the real ceiling, which costs
file count rather than correctness.

The deeper cost is that the correction itself introduced a number nobody had measured. The audit
was right about the class of error and wrong about the value, which is the shape of correction
that is hardest to catch: a fixed row looks fixed.

## What a future session should do differently

Read the repository's own index rather than summing a listing. Every model hub in this corpus
returns a tree endpoint with per-file sizes, and the difference between a total and a maximum is
one `max()` call away.

And when a correction replaces a number, say which measurement produced the new one. "~5.2 GB"
with no probe behind it is the same defect as "688.6 GB" in a per-object table, one order of
magnitude smaller.
