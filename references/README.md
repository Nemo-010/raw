# references

Curated third-party material that earns a permanent place in this repository.

This directory is deliberately small and hand-maintained. It exists because
research depends on documents that disappear: a vendor's limits page that gets
rewritten, a GitHub repository that gets deleted, a forum post that is the only
public record of how a loophole closed. When losing a document would cost us a
finding, we keep the part we use.

## The promotion test

A file is promoted from `.tmp/` into `references/` only when **all** of these
hold:

1. **It is cited.** At least one document or dossier in this repository depends
   on it specifically, and the citation names the path here rather than a URL.
2. **The URL is not durable.** Either it has already changed, the host is known
   to prune, the repository is archived, or the author has signalled removal.
   A live, stable, well-known page is cited by URL and **not** copied — copying
   it only creates a second version that will drift.
3. **It is pruned to what we use.** The parts we do not cite are removed. A
   10,000-line vendor document becomes the 200 lines that carry our claims, with
   a header saying what was removed and where the original lived.
4. **Its licence permits it, and we say so.** Each reference carries the
   upstream licence in `MANIFEST.md`, or a note that the licence could not be
   established — in which case only short quoted excerpts are kept, never the
   whole work.

What does **not** qualify, and is refused on sight: a whole repository cloned
because it looked useful; a `.git` directory; build output, `node_modules`,
lockfiles, images and vendored dependencies; a page we could re-fetch in two
seconds; anything we merely intend to read later.

The operator's own seed repositories do **not** belong here. They are inputs to
this project, not references it cites, and their content is absorbed into
`docs/` and `dossier/` with provenance recorded in `sources/SEED.md`.

## Layout

```text
references/
  MANIFEST.md                  one entry per reference: why, from where, licence, what was cut
  <vendor-or-author>/<slug>/   the pruned document set
```

## `MANIFEST.md`

Every directory has an entry. The entry answers, in this order: **what it is**,
**why it is here** (the finding that would be lost), **where it came from** (URL,
commit or capture date), **the licence**, **what was removed**, and **what cites
it**. An entry without a citation is deleted at the next review — that is the
mechanism that keeps this directory from becoming an attic.

## Rules

- Never modify a reference to make it agree with a document here. The reference
  is the evidence; if they disagree, the document is wrong.
- Never store a reference's `.git`, and never store a patch series. If history
  matters, store the single commit hash in `MANIFEST.md`.
- A reference that has been superseded upstream is kept and marked
  `superseded: <url>, <date>` rather than replaced, because the point was to
  preserve what it said when we relied on it.
