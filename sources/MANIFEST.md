# sources/MANIFEST.tsv — the evidence index

One row per captured file. This is the only index that matters, and it is the
answer to "what did that page actually say on the day we relied on it".

## Columns

Tab-separated, this order, no header repeats:

| column | type | meaning |
|---|---|---|
| `captured_at` | ISO 8601 UTC, ms, `Z` | when the bytes were retrieved |
| `url` | string | the exact URL requested, query string included |
| `final_url` | string or `-` | where redirects landed; `-` when the URL did not move |
| `status` | integer | the response status |
| `bytes` | integer | size of the stored body |
| `sha256` | hex | hash of the stored body |
| `media_type` | string | `Content-Type`, lowercased, parameters stripped |
| `via` | enum | `fetch`, `read`, `archive`, `crawl`, `gh`, `probe`, `manual` |
| `path` | path | repository-relative path of the capture |
| `note` | string | one line: what this capture is evidence for |

## The `via` values, and why they are recorded

The broker that produced a capture changes what the capture proves. `fetch`
returns the origin's bytes and headers unchanged, so a `fetch` capture is
evidence about the origin. `read` returns extracted Markdown, so it is evidence
about what the page *said* but not about its markup or its headers. `archive`
returns a third party's copy, so it is evidence about that third party's capture
and only indirectly about the origin. A reader who cannot tell these apart will
mistake an extraction for a measurement.

`manual` marks a file a person placed. It is allowed for a dataset a tool
produced outside this repository, and the `note` must say which tool and when.
`probe` marks a machine record produced by `scripts/probe/probe.py`.

## The rules

- **Append, never rewrite.** A recapture of a changed page is a new row. The old
  row stays; that is how a change over time becomes visible.
- **`last_seen` is not a column, on purpose.** A re-verification that returns
  identical bytes updates nothing visible here. If you want to record that
  somebody checked, that belongs in the dossier's `verified_at`, not in the
  manifest. Keeping the two separate stops the manifest from pretending a page
  changed when it did not.
- **A challenge page is recorded as a capture.** Status 200 with a Turnstile body
  goes in with `note` starting `challenge:`, because "the vendor removed this
  page" and "we were walled" are different facts and conflating them is how a
  dead end gets misclassified.
- **No credentials.** A capture is a response body. It never carries a cookie, an
  `Authorization` header, or a token from a request.

## Checking the manifest

```bash
python scripts/sources/manifest.py --verify sources/
```

It fails when a row names a file that is absent, when a file has no row, or when
a `sha256` or `bytes` value disagrees with the file on disk. A manifest that has
drifted from the tree is worse than no manifest, because it looks authoritative.
