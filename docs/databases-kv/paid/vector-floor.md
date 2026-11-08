# What does a vector index cost per gigabyte, and when is it worth paying?

Three providers publish a per-gigabyte rate and one is metered by the million dimensions. ⭐ **The
answer is that the storage rate does not decide it: Neon's pgvector at USD 0.35/GB-month and
Pinecone's Standard at USD 0.33 are within six cents of each other.** What decides it is that
pgvector is a table in a database already paid for and a managed vector service is a second system
with a second counter.

## The comparison

Sorted by the marginal cost of the first gigabyte beyond the free allowance.

| provider | storage rate | egress rate | free allowance |
| --- | --- | --- | --- |
| Neon (pgvector) | USD 0.35/GB-month | USD 0.10/GB beyond 500 GB | 1 GB per project |
| Pinecone Standard | USD 0.33/GB-month | USD 0.10/GB beyond 100 GB/month | 2 GB per organization |
| Weaviate Flex | from USD 45/month, dimensions metered | not published separately | 100,000 objects |
| Qdrant Standard | metered by vCPU, RAM, disk and backups | not published separately | 1 GB RAM, 4 GB disk |

## The comparison a reader actually needs

A vector index is storage plus a query path. The storage rates are close: USD 0.33 on Pinecone
and USD 0.35 on Neon. The difference is everything else.

On Neon, a vector index is a table in a database already paid for. There is no second bill, no
second client library, no second consistency problem and no separate egress allowance, because
the database's 500 GB covers the index's reads too.

On Pinecone, the index has its own 100 GB of egress on Standard and its own 2 GB organization cap
on Starter. That is a second system with a second counter.

The premium a managed vector service charges is for the query planner, the filtered search and
the index type. It is not for the storage, which is priced within six cents.

## Pinecone Standard

Standard is unlimited storage at **USD 0.33 per GB-month** with **100 GB of egress per month**
included and **USD 0.10 per GB** after. Builder at USD 25 gives 10 GB of storage and 10 GB of
egress, and is the tier a reader should compare against Neon's metered rate.

`Evidence:` `pinecone.io/pricing/` (read 2026-10-22): the Standard column for storage and egress,
and the Builder row.

`Verdict:` the closest managed competitor on storage price, with a second egress allowance to
manage.

## Weaviate Flex

Flex starts at **USD 45 a month** and meters vector dimensions from USD 0.00465 per million on
Flex, USD 0.003875 on Premium and USD 0.002718 on the prepaid tier. That is a different unit from
a gigabyte and it cannot be compared without knowing the dimension count and the query volume,
which is why the record states the unit rather than a converted figure.

`Evidence:` `weaviate.io/pricing` (read 2026-10-22): "Minimum USD 45 / month" on Flex and the
per-million-dimension rates per tier.

`Verdict:` the wrong unit to compare against a per-gigabyte rate without a workload model.

## Qdrant Standard

Qdrant bills compute, memory, storage and backup storage separately, hourly, with the free tier at
1 GB RAM and 4 GB disk. No per-gigabyte storage rate is published on the pricing page, so a
reader cannot compute a monthly figure without the cluster shape.

`Evidence:` `qdrant.tech/pricing/` (read 2026-10-22): billing is "based on compute (vCPU), memory
(GB), storage (GB) consumed by your clusters, storage (GB) consumed by backups, and used inference
tokens".

`Verdict:` metered in four dimensions, which is more knobs than this decision needs.

## What did not work

- **Pinecone Starter as a paid step**: the 2 GB cap is per organization and Builder is the first
  tier that raises it, so there is no small paid increment (`documented`,
  `pinecone.io/pricing/`).
- **Weaviate's per-dimension rate as a per-gigabyte figure**: the units do not convert without a
  dimension count and a query volume, so any comparison is a model and not a measurement
  (`documented`).
- **Qdrant's published price as a monthly number**: four metered dimensions and no per-GB rate
  (`documented`).
- **A managed vector service for fewer than a million vectors**: pgvector on the same 1 GB free
  Postgres is cheaper because it is the same bill (`inferred` from the Neon storage rate).
- **Chroma Cloud as a paid tier**: USD 5 of credits is a trial and the open-source server is the
  free path (`documented`, `trychroma.com/pricing`).

## Chaining

**A metered Postgres with pgvector, behind a free cache.** `Neon Launch` at USD 0.35 per GB-month
with `Upstash` in front. The scarce link is the index build, which is one large compute burst and
therefore one large CU-hour charge.

**A managed index for a large corpus and a free Postgres for the truth.** `Pinecone Standard` for
the index and any free Postgres for the metadata. The scarce link is keeping the two consistent,
which is the cost the storage rates do not show.
