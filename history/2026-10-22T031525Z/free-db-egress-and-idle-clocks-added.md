# Three free tiers were recorded without the number that binds them, and two of those numbers are egress

- **When:** 2026-10-22T03:15:25Z
- **Status:** corrected
- **Supersedes:** `.tmp/work/recon-extras/DATABASES-KV.md` §Verified inventory, the Atlas M0 and
  Pinecone Starter rows
- **Superseded by:** `docs/databases-kv/free/document-and-cache.md` §MongoDB Atlas and
  `docs/databases-kv/free/vector.md` §Pinecone
- **Evidence:** `mongodb.com/docs/atlas/reference/free-shared-limitations/` and
  `pinecone.io/pricing/`, both read 2026-10-22
- **Confidence:** documented

## What we believed

The census recorded Atlas M0 with `per-ip-shaping: 100 operations/second and a hard 512 MB` and
Pinecone Starter with `quota: 2 GB/org and one project; region locked to us-east-1`. Both were
right and both were incomplete in the same way: neither carried the free tier's traffic allowance.

## What we found

**Atlas M0 caps data transfer at 10 GB in and 10 GB out per rolling seven-day period.** The
limitations page states it, the mechanism is network throttling plus a one-second cooldown per
connection once the queue exceeds the operations limit, and it caps a serving workload at about
1.43 GB a day. The census had the operations rate and not the byte rate, and the byte rate is what
ends a retrieval service.

**Pinecone Starter caps egress at 1 GB per month.** The pricing table lists it beside the 2 GB of
storage. 1 GB a month is 33 MB a day, which at 6 KiB per 1,536-dimensional float32 vector is about
5,500 vector reads a day. The storage cap is unreachable because the egress cap arrives first.

Both pages also carry an idle clock or a pause the census did not record: **Atlas pauses a free
cluster after 30 days with zero connections**, which is the longest idle clock in the topic short
of Aiven.

## How we found it

The census named a storage figure and an operations figure. The question that follows is what
leaves the database, so the limitations and pricing pages were read to the end. Both limits are in
tables below the headline.

## What it cost us

A row that would have been trusted. "2 GB of free vector storage" and "512 MB of free document
storage" are both true and both describe capacity a network limit prevents a reader from reaching.
A recommendation built on either would have met the throttle in production.

## What a future session should do differently

**A free tier has five numbers, and the census recorded two of them.** The five are: storage, the
per-object or per-record cap, the operations or request rate, the traffic allowance, and the idle
clock. A row that omits the traffic allowance and the idle clock has recorded capacity and not
access, and it is the shape that produces a recommendation with its failure mode removed.
