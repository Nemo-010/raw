# Baselines: Hugging Face, ModelScope and GHCR

Three providers are excluded from every shortlist in this topic because a reader already
knows them. They still need current numbers, because a plan built around an
unknown is built on a guess, and because these three are the yardstick against which
the rest of the corpus is measured.

## The three, and what each is actually promising

| provider | free offer | what the wording is | binding constraint | rung |
|---|---|---|---|---|
| Hugging Face | public repositories "best-effort", private 100 GB | discretionary, with no number attached to the public side | `write-gated` on private space; no published public ceiling | `documented`, 2026-10-22 |
| ModelScope | "no storage limits" | a vendor sentence with no egress policy behind it | `request-rate` on the write path, undisclosed and traffic-tuned | `documented`, 2026-10-22 |
| GHCR | 10 GB per layer, public images free | a container registry cap, not a storage product | `per-object-cap` at 10 GB | `documented`, 2026-10-21 |

## Hugging Face: "best-effort" is not a quota

The storage-limits page states "Best-effort" for free public repositories and 100 GB
for private ones, and it carries 10 TB and 200 TB rows above them for paid and
enterprise plans (`documented`, 2026-10-22: `huggingface.co/docs/hub/storage-limits`,
200, 17,325 B).

"Best-effort" with no number is a discretionary throttle, which is worse than a quota.
There is no ceiling to design against and no threshold at which the storage is safe, so
a plan cannot size against it. The record carries it as `discretionary: true` and the
number is not multiplied anywhere in this corpus.

Storage Buckets via the S3 gateway at `s3.hf.co` is the part worth having, because it
turns the platform into an S3 backend that git-annex and DVC can address. That is a
`free/forge-surfaces.md` finding, not a quota finding.

## ModelScope: the quota is not the constraint

The vendor sentence is current and verbatim: "ModelScope doesn't have any storage
limits", under the heading "1. Free Unlimited Storage Space"
(`documented`, 2026-10-22: `modelscope.ai/posts/434366`, 200, 4,380 B).

The enforcement is real, dynamic and deliberately unpublished. A maintainer answered an
upload-limit report in `modelscope/modelscope` issue 1793, closed, on 2026-09-09:

> "the commit frequency limit is dynamically-adjusted based on real-time platform
> traffic, and we do not plan to disclose the limit at this moment. and no, the quota
> is not adjustable at this moment. please try to include multiple files in one
> commit/push when using git or modelscope sdk. avoid doing one-file-per-commit (which
> is most likely a malpractice), then you should be fine."

That is a measured refusal with a named error code (`E1021`, HTTP 429), not a
documented limit. Three consequences follow.

The throttle targets exactly the shape a bulk migration produces. A 10 TiB initial upload of
25 MiB shards is 419,000 files, and one-file-per-commit is the pattern the maintainer
calls malpractice. Batching is mandatory, so the hot tier is a days-long job rather than
a store that fills in one session.

The cap cannot be bought past, because the vendor says the quota is not adjustable at
this moment.

The scale ceiling is still unknown. A separate report describes HTTP 413 on a roughly
100 GB dataset upload, and the SDK carries `MAX_FILE_COUNT_IN_DIR = 50000`, so 10 TiB
at 25 MiB needs at least 8.4 repositories. None of that evidences a capacity ban. It
evidences a write-path throttle, and the two are different findings.

## GHCR: 10 GB per layer, and that is the number

GitHub Container Registry carries 10 GB per layer for public images, which is the
figure that decides whether it can hold a shard. As a container registry it is one of
the better ones, and it belongs with the other OCI registries in
`free/registries.md`. A layer over 10 GB is refused at push time.

The distinction that matters here is that GHCR's cap is per layer and the pull path is
unmetered, which makes it a shard source rather than a serving tier. An archive of 20 TiB
at 10 GB per layer is 2,048 layers, and nothing in the registry caps the layer count.

## Why these three stay excluded from the shortlist

None of the three is a candidate for the composition, and the reasons are different in
each case.

Hugging Face's public side has no number, so it cannot carry a byte target. Its private
side stops at 100 GB, which is a fifth of the hot working set.

ModelScope's quota is a sentence and its write path is an undisclosed throttle. It is
viable as a hot tier only if the write can be batched across several days and repositories,
and a second copy is kept because the sentence could change without notice.

GHCR's 10 GB layer is a good shard size and a bad archive size, and its value in this
corpus is as a worked example of a registry that states a real number.

## What this baseline is for

Every "unlimited" claim elsewhere in this topic is read against these three. A provider
that publishes no number is in the same class as Hugging Face's public tier, and a
provider that publishes a number and then throttles the write path is in the same class
as ModelScope. Naming the class is what stops a new provider's marketing sentence from
reading as a new finding.
