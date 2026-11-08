# sources

Third-party material this repository depends on, kept **as received**.

Nothing here is hand-edited. A file in `sources/` is either the byte-for-byte
output of a fetch or the byte-for-byte archive of a page, and the manifest or a
sidecar says which URL produced it and when. Scripts write it:
`scripts/rq integrate` (and `scripts/fr` with `--capture`) for `c/` and the probe
records in `p/`, and `scripts/sources/manifest.py` checks the rest. If the vendor changes the page, the next run of
the refresh script writes a new dated capture beside the old one; it never
overwrites it. That is the whole point: a claim in `docs/` must be checkable
against what the page actually said on the day we read it, and a page that has
since changed is the most common way a corpus like this rots.

## Layout

```text
sources/
  MANIFEST.tsv          one row per captured file; the only index that matters
  <YYYY-MM-DD>/         captures grouped by the UTC date of the run
    <host>/
      <slug>.<ext>      the capture, extension reflecting the media type
  c/<aa>/<sha256>.md.gz page text that a research run's evidence cites, with a .json sidecar
  p/<aa>/<sha256><ext>.gz   probe and process output that records cite, gzipped
  p/<aa>/<sha256>.json      the sidecar of a probe record that a run's measured evidence cites
  p/<aa>/<sha256>.tree.tsv  the index of a folder: each file's path, size, sha256 and where it is stored
```

A file of `p/` with a `<sha256>.json` sidecar beside it is a probe record that the
integrator copied (`scripts/rq capture --probe`); the sidecar indexes it, as in
`c/`. Every other file of `p/` has a row in `MANIFEST.tsv`.

The manifest-indexed files of `p/` hold the evidence that records once cited under `.tmp/` and that
still existed on 2026-10-28: 15 files and 2 folders, 514 stored files. The name is the sha256 of the bytes as kept.
Forty-five files carried the probe machine's IPv4 or IPv6 address, its ISP, its country, the names of its own
egress road, a local user path, the country that a vendor page printed for the visitor from geolocation, an
operator host name (the page reader's hosts in tool output among them) or the name of an operator project.
Each value is replaced with a bracketed placeholder before hashing, and the manifest note and the folder index
name each replacement and its count. Executables and bytecode are listed in their folder index and not kept.
The records that cited one of the 33 paths that no longer existed are the work of an open `rq:research` issue.

`sources/MANIFEST.tsv` is tab-separated and has exactly these columns, in this
order:

| column | meaning |
|---|---|
| `captured_at` | ISO 8601 UTC with milliseconds and `Z`, e.g. `2026-10-22T07:41:03.912Z` |
| `url` | the exact URL requested, including query string |
| `final_url` | where redirects landed, and `-` when it did not move |
| `status` | the HTTP status the origin returned |
| `bytes` | the size of the body as stored, in bytes |
| `sha256` | the hash of the stored bytes |
| `media_type` | the `Content-Type`, lowercased, parameters stripped |
| `via` | `fetch`, `read`, `archive`, `crawl`, `gh` or `manual` — the broker that produced it |
| `path` | the repository-relative path of the capture |
| `note` | one line: what this capture is evidence for, or `-` |

## What is allowed in

A capture earns its place when a record or a document in this repository cites
it. `sources/` is not a web cache; it is the evidence appendix. Nothing prunes it
today: no prune script and no retention window exist.

A page behind a challenge is captured as the challenge, not as a failure. The
capture records `status` and the body we actually received, and the `note`
column says `challenge: <signature>` so a later reader can tell "the vendor
removed this page" from "we were walled".

## What is not allowed in

- Credentials, cookies, tokens or `Authorization` headers. A capture is the
  response body, never the request's secrets.
- Personal data. If a page carries an email address or a name that is not the
  vendor's own published contact, the capture is redacted at the field level and
  the `note` says so.
- Anything larger than the capture cap. A 40 MiB PDF is cited by URL and date in
  `docs/`; it is not stored here. The cap is `CAP_BYTES` in
  `scripts/sources/manifest.py` (8 MiB) and `scripts/hygiene.py` refuses a
  committed file above it.

## Refreshing, and why there is no refresher

```bash
python scripts/sources/manifest.py --verify sources/   # 0 clean, 1 defect, 2 usage
scripts/rq folder session                              # prints your folder, .tmp/session-<id>
scripts/rq capture URL --lane .tmp/session-<id>        # re-capture one page; prints its sha256
```

⚠ **`scripts/sources/refresh.sh` does not exist.** Earlier revisions of this file
documented `sh scripts/sources/refresh.sh --topic storage --dry-run` as the way to
re-capture the pages we cite; that command exits `127` and always has. A
refresher has to answer two questions before it is safe to build: *which* of the
records still need a capture, and *whether* a re-capture changed a verdict. The
policy for the second does not exist, and a refresher without it is a cron job
that rewrites evidence while nobody is reading.

Until then, a re-capture goes through `scripts/rq capture`, into a folder with its
own id under `.tmp/` (`AGENTS.md` section 2 rule 14). In a run, the lane captures the
page into its unit folder and the integrator copies the capture into `c/` when a change
cites it. Outside a run, `scripts/rq capture URL --lane .tmp/session-<id>` (the folder
that `scripts/rq folder session` prints) gives the hash. In the research checkout the
change itself is an `amend` run, `scripts/rq open amend TOPIC "RID: what is wrong"`,
whose lane cites the capture; `scripts/fr amend ... --capture sha256:... --quote "..."`
refuses there and copies a capture into `c/` only in an own clone. Nobody adds a
`MANIFEST.tsv` row by hand. The dossier's
`evidence[]` is the record of what a capture proved; both move together or neither
does.

## Provenance of the seed

The corpus began as three external research passes and one platform's own
documentation. Those are recorded in `sources/SEED.md` — what was taken, from
which public repository at which commit, and what licence it carried — because a
reader is entitled to know which claims in this repository were inherited rather
than measured here, and an inherited claim starts life at the `reported` rung of
the evidence ladder until somebody re-measures it.
