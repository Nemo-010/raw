# Where does a build keep its output when the runner is destroyed?

A CI job is ephemeral and three storage pools are attached to it. All three are smaller than one
container image, and two of them share a budget. The answer is that the output must leave the
platform inside the job, and the free destination is an object store rather than the registry that
comes with the CI vendor.

## The comparison

Sorted by free storage, in the pool each one actually shares.

| pool | free allowance | eviction | identity | verdict |
| --- | --- | --- | --- | --- |
| GitLab Container Registry | excluded from the 10 GiB repository quota; no separate cap published | nothing expires by default | email | qualifies-with-caveat |
| GitHub Actions cache | 10 GB per repository | entries not accessed in 7 days | email | qualifies-with-caveat |
| GitHub artifacts | 500 MB on Free, shared with Packages | 90 days default | email | qualifies-with-caveat |
| GitHub Packages and GHCR | the same 500 MB pool for private packages; a public package is free and pulls anonymously | never, until deleted | email for a push, anonymous for a public pull | qualifies-with-caveat |
| Docker Hub | anonymous pull tokens, so a public base image is free | not applicable to pulls | anonymous | qualifies |

## The two facts that decide a build's storage

⛔ **The GitHub pools are two and not three.** Artifacts and Packages share **500 MB** on Free, and
the billing page says so directly: "your total storage across Packages and Actions artifacts
cannot exceed the included amount for your plan". The cache is a separate **10 GB** per repository.
So a repository that pushes an image and keeps artifacts is spending one 500 MB budget twice, and
the cache is the only generous pool.

⚠ **The GitLab registry is excluded, which is not the same as free.** The storage-quota
documentation states the container registry is excluded from the 10 GiB namespace repository quota.
It does not state that the registry is free, and no separate free figure is published. The 10 GiB
that circulates is the repository quota and the two are different limits.

## GitHub Actions artifacts

**500 MB on Free**, 1 GB on Pro, 2 GB on Team and 50 GB on Enterprise. Retention defaults to **90
days** and is configurable per repository, per organization and per artifact. Logs use the same
retention.

90 days is generous and 500 MB is not: a build that produces a 2 GB binary cannot store it at all,
and one that produces 50 MB of output can keep ten of them.

`Evidence:` `docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts`
(read 2026-10-22): "By default, GitHub stores build logs and artifacts for 90 days".
`docs.github.com/en/actions/reference/limits` (read 2026-10-22): the 500 MB, 1 GB, 2 GB and 50 GB
artifact figures per plan.

`Verdict:` qualifies-with-caveat. Ninety days of retention behind half a gigabyte.

## GitHub Packages and GHCR

GitHub Packages covers npm, Maven, Gradle, NuGet, RubyGems and container images under one billing
pool, and **GHCR is the container registry inside it**. On Free that is **500 MB of storage and 1
GB of transfer a month**, shared with Actions artifacts.

Two details from the billing page:

- A 500 MB package published in a private repository consumes 500 MB of storage. Publishing an
  updated 500 MB package without deleting the original puts you at 1 GB.
- A download of a 500 MB package consumes 500 MB of transfer. **A download by GitHub Actions using
  `GITHUB_TOKEN` does not count against the transfer allowance.**

That last sentence is what makes a build-then-deploy chain free: the runner pulls its own image
without spending the transfer budget.

GHCR does issue anonymous pull tokens for a public package. A request to
`https://ghcr.io/token?scope=repository:catthehacker/ubuntu:pull&service=ghcr.io` returned **200**
with 69 bytes of token JSON on 2026-10-22, and that token fetched a manifest:
`https://ghcr.io/v2/catthehacker/ubuntu/manifests/act-latest` returned **200** with 754 bytes of
`schemaVersion: 2`, media type `application/vnd.oci.image.index.v1+json`. `actions/actions-runner`
and `homebrew/core/hello` behaved the same way. So a public image in GHCR costs the puller nothing
and needs no identity, exactly as on Docker Hub. A **private** image still needs an authenticated
pull, which is a storage question and not a token question.

⚠ A token request for a repository that does not exist returns **403** `DENIED`. The namespace
matters: `library/` is Docker Hub's and does not exist on `ghcr.io`, so a probe of
`library/hello-world` there answers the path, not the policy.

`Evidence:` `docs.github.com/en/billing/concepts/product-billing/github-packages` (read 2026-10-22):
the shared pool, the two worked examples and the `GITHUB_TOKEN` exemption. Probe of the GHCR token
endpoint on 2026-10-22 for `catthehacker/ubuntu`: 200, 69 bytes, sha256 `e26b35c1`; the manifest
fetch: 200, 754 bytes, sha256 `62d572b9`. Negative control `library/hello-world`: 403, 86 bytes.

`Verdict:` qualifies-with-caveat. Half a gigabyte is smaller than one CUDA image.

## GitHub Actions cache

**10 GB per repository** by default, with any entry not accessed in **over 7 days** removed. Beyond
10 GB GitHub saves the new cache and evicts oldest-first by last access, which the documentation
warns can cause cache thrashing. Raising the limit is available only to accounts with a payment
method, up to 10 TB for a user-owned repository.

Rate limits: **200 uploads a minute**, **1,500 downloads a minute** and **400 deletes a minute**
per repository. A build that restores a thousand cache entries meets the download ceiling.

A cache created by a workflow triggered on a pull request is scoped to that merge ref, so it cannot
be restored by the base branch. That is a design detail that surprises a first cache implementation.

`Evidence:` `docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching` (read
2026-10-22): the 10 GB default, 7-day eviction, oldest-first beyond the limit, the payment-method
requirement, the per-pull-request cache scope and the rate limits.

`Verdict:` qualifies-with-caveat. Ten gigabytes that must be touched weekly.

## GitLab Container Registry

The registry is **excluded from the 10 GiB namespace repository quota**, and the documentation
publishes no separate free cap. Storage above the namespace's purchased amount is billed, and
nothing expires by default unless a cleanup policy is configured.

`Evidence:` `docs.gitlab.com/user/storage_usage_quotas/` (read 2026-10-22): the registry exclusion
sentence.

`Verdict:` qualifies-with-caveat. An exclusion is not an allowance.

## Docker Hub

Docker Hub issues **anonymous pull tokens**: `https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/alpine:pull`
returned **200** with 5,489 bytes of token JSON on 2026-10-22, with no account. A public base image
is therefore free to pull, which is what makes a container build possible on a runner with no
registry credentials. GHCR behaves the same way for a public package, so the difference is the
namespace, not the policy.

`Evidence:` probe of the Docker Hub token endpoint on 2026-10-22: 200, 5,489 bytes. Probe of the
GHCR token endpoint for a public package on the same day: 200, 69 bytes, and a 200 manifest.

`Verdict:` qualifies. Anonymous base images. GHCR is the second anonymous path for a public image,
and the only free registry in this set that also accepts a push.

## What did not work

- **Storing a 2 GB build output as a GitHub artifact**: 500 MB on Free
  (`documented`, `docs.github.com/en/actions/reference/limits`).
- **GHCR and Packages as two budgets**: one 500 MB pool for both
  (`documented`, `docs.github.com/en/billing/concepts/product-billing/github-packages`).
- **A private GHCR image pulled anonymously**: not tested. A token request for the nonexistent
  `library/hello-world` returns 403 DENIED, and that is a fact about the path, not about private
  packages (`measured`, 2026-10-22).
- **The GitLab 10 GiB as a registry quota**: the registry is excluded from that quota and no
  separate figure is published (`documented`, `docs.gitlab.com/user/storage_usage_quotas/`).
- **A cache as durable storage**: entries not accessed in 7 days are deleted
  (`documented`, `docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching`).
- **Raising the cache above 10 GB on Free**: it needs a payment method (`documented`, same page).

## Chaining

**Build on GitHub, store on R2.** `GitHub Actions` on a public repository, then `Cloudflare R2` at
10 GB free for the artifact. The scarce link is the 500 MB artifact pool, so the output must leave
inside the job, and R2's free tier is the smallest external destination that clears it.

**Cache in Actions, image in GHCR, base image from Docker Hub.** The cache is 10 GB and separate;
the image is in the shared 500 MB; either base registry serves a public image anonymously. The
scarce link is the 500 MB shared pool, and the chain works only if the runner pulls its own private
image with `GITHUB_TOKEN`, which does not spend the transfer allowance.
