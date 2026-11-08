# `read` was documented with `curl -f`, which deletes the diagnostic the ladder exists to deliver

- **When:** 2026-10-22T04:23:11Z
- **Status:** corrected
- **Supersedes:** `docs/crawler-scraper/free/broker.md` §The seven hosts (row `read`), §Read a page, and every rung of §The escalation ladder
- **Superseded by:** `docs/crawler-scraper/free/broker.md` §Read a page, which now forbids `-f` on `read` in the operation itself
- **Evidence:** `curl -qfsS` against `read.web.pkgforge.dev` and `curl -qsS` against the same URL, both run 2026-10-22T03:56Z; the pair is reproduced in the document
- **Confidence:** measured

## What we believed

The broker document's `read` examples were written as `curl -qfsS`. The `-f` was copied
from the `search` and `archive` calls beside them, where it is correct: those services
answer `200` or a problem document, so a `-f` failure loses nothing.

The document also carried, six lines below the `read` block, the rule that a reader must
read `upstream_status` before the body, and that a `200` from this service is not evidence
about the origin. The two statements contradict each other and the contradiction was not
noticed for a whole wave.

## What we found

`read` passes the origin's status through. The service's own contract states it: "An
origin's 4xx or 5xx page is answered with the origin's status, not 200: the page's
Markdown is the body, and the status is in `x-reader-upstream-status` and
`upstream_status`."

So `-f` turns every 404, 409 and 422 into `curl: (22)` with **no body written at all**.
The front matter, the `upstream_status`, the `x-reader-final-url` and the
`x-reader-dropped` tokens are all deleted, on exactly the walled, missing and challenged
pages the document exists to diagnose:

```text
$ curl -qfsS "https://read.web.pkgforge.dev/https://example.com/pricing"
curl: (22) The requested URL returned error: 404

$ curl -qsS -D - "https://read.web.pkgforge.dev/https://example.com/pricing"
HTTP/1.1 404 Not Found
x-reader-upstream-status: 404
x-reader-dropped: script-style-noscript:1,candidates-considered:2,low-confidence:short-output
--- title: "Example Domain" words: 25 upstream_status: 404 confidence: low ...
```

The same on the Reddit thread the document uses as a worked example: `-qfsS` gives
`curl: (22) ... 409`, and without `-f` the answer is a 929-byte problem document naming
the challenge. The repository's own wrapper already disagreed with the document:
`sh scripts/broker/broker.sh read https://example.com/pricing` exits 1 **with the body on
stdout**.

A second defect sat on the same lines. The paste URL was `https://example.com/pricing`,
which does not exist: the first command a cold reader ran returned a 404 at best and
`curl: (22)` at worst.

## How we found it

An adversarial review ran every `curl` invocation in `broker.md` as written, in a cold
session, and recorded the exit code and the bytes for each. Four of eighteen failed. Two
of the four were the `read` calls.

## What it cost us

One review round, and a document that taught a reader to destroy its own central
diagnostic. A cold session following it would have recorded every walled page as
"unreachable" rather than as "walled, with the origin's status known".

## What a future session should do differently

⭐ **`-f` is a property of the caller's intent, not a house style.** Put it on a call whose
failure carries no information, and leave it off a call whose failure *is* the
information. Any command that passes an origin's status through must be written without
`-f`, and the document that teaches it must say so at the call, not in a note below.

⚠ **The rule that catches this class is cheap: run every command you write, in a cold
shell, and paste the exit code.** A command that has never been run is a claim about a
command.
