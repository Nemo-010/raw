# references/MANIFEST.md

One entry per reference. A reference is here because a finding would be lost if
the document vanished, and because the document is the kind that does vanish.

The bar is in [`README.md`](README.md). The short form: it must be **cited** by a
document here, it must be **perishable**, it must be **pruned to what we use**,
and its **licence must permit** the copy.

---

## `hoangvu12__free-s3/RESEARCH.md`

**What it is.** A verified catalogue, written by the author of a free-tier
S3 gateway, of about nineteen free storage hosts: each one's upload API, per-file
cap, retention policy and direct-URL shape. It is the source material behind the
gateway's design.

**Why it is here.** `docs/storage/free/host-economics.md` cites it in two places:
as the reference implementation of the chunk-and-replicate pattern, and as the
verified per-host catalogue that a reader would act on. The document is a
third-party research file in a personal repository — exactly the class that gets
archived, renamed or force-pushed with no notice. The repository was live on
2026-10-22 (`api.gh.pkgforge.dev` returned 200), which is the reason to keep a
copy rather than a reason not to: the copy outlives the URL.

**Where it came from.** `https://github.com/hoangvu12/free-s3/blob/master/RESEARCH.md`,
retrieved 2026-10-22 through `fetch.web.pkgforge.dev`. Note the branch: the file
lives on `master` and `main` 404s, which the citing document already records.

**Licence.** Not stated in the upstream repository. The copy is therefore carried
as the cited excerpt rather than as a redistribution, and the header records that
it should be removed if upstream later states a licence forbidding it.

**What was removed.** Nothing. The file is 243 lines and is the per-host table
that is cited; trimming it would leave a citation pointing at an absence. This is
the one case where "prune to what you use" and "keep the thing you cite" give the
same answer.

**What cites it.** `docs/storage/free/host-economics.md` §The reference
implementation, §The three layers.

---

## What is deliberately not here

The corpus cites several hundred URLs and holds 38 captures in `sources/`. None of
the rest is promoted, and the reasons are the four bars:

- **A live, stable, well-known page is cited by URL.** Copying a vendor's pricing
  page creates a second version that will drift from the first, and the capture
  mechanism in `sources/` already covers the case where a page changes.
- **A whole repository is never cloned.** The operator's own seed passes are
  inputs to this project, not references it cites; their content is absorbed into
  `docs/` and `dossier/` with provenance in `sources/SEED.md`.
- **A page we could re-fetch in two seconds does not qualify.** `sources/` handles
  those with a hash and a date, which is cheaper and more honest than a copy in
  a curated directory.
- **Nothing is kept "for later".** An entry without a citation is deleted at the
  next review. That is the mechanism that stops this directory becoming an attic.
