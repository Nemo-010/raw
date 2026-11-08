# How the web lies to a researcher

This is a catalogue of failure shapes, not a list of providers. Each entry is one way a
page, a status code or a header reports something that is not true, in a form that a
careful reader still falls for. Each carries its signature, the probe that detects it,
and the rule it becomes. Twelve of them are the platform's own numbered traps, cited by
number so a reader can find the original; the rest are shapes measured here or
reported.

⭐ **Read this before you write a `measured` claim.** The evidence ladder says a live
request outranks a page. That is only true when the request's answer was read correctly.
A `200` read as success, a `206` read as a delivered range, or a header read at the
proxy instead of the origin each produce a `measured` claim that is false, and false at
the highest rung there is.

⛔ **A shape in this catalogue is not a defect of one provider.** It is a property of the
layer between the researcher and the page. The same wall arrives as `200` from one
broker, `403` from another and `202` from a third.

## The shapes, by what they cost

| # | the shape | the signature | the probe | the rule |
| --- | --- | --- | --- | --- |
| 1 | a `200` carrying a wall | body under 30 words, `confidence: low`, or a challenge marker in the body | read the body, not the status | never trust HTTP 200 (P-11, P-28) |
| 2 | a `200` carrying the wrong page | `final_url` names a different host | compare `final_url` to the URL asked | reject any answer whose `final_url` host differs |
| 3 | a `206` that is a decoded slice | `200` where a `206` was asked, or a `Content-Range` total that is the decoded size | `cmp` the slice against the full body | a range answer may be of the decoded representation (P-19, P-41) |
| 4 | a wall arrives as an injected `303` | `HTTP/1.0 303`, `Location: https://blocked.teams.cloudflare.com?...` | read the `Location` host | a policy block is not the origin's redirect (P-23) |
| 5 | a private-destination refusal is a `200` | the body is Cloudflare's error page, not the origin's | compare the body to what the origin serves | a `403` or `530` may be the platform, not the origin (P-11) |
| 6 | a stream cut by a CPU budget ends as a clean `200` | byte count under `Content-Length`, or curl exit 0 with a short body | count bytes and hash | check a large download's length, never assume it (P-34) |
| 7 | a header mutation at the proxy | two runs on two transports, two header sets | ask an origin that echoes the request | report a header per transport, never per platform (P-8, P-9, P-17) |
| 8 | a compressed body with no `content-encoding` | bytes begin `1f8b`, no header says gzip | read the first two bytes | declare `Accept-Encoding` when measuring bytes (P-18, P-27) |
| 9 | a decoded body under the origin's framing headers | `HEAD` reports a size the body does not have | `wc -c` the body | never forward a proxied `Content-Length` (P-7) |
| 10 | a local test that passes on a deployed edge that fails | the failure reproduces in production, not in the local runtime | run the probe against the deployed service | a local test is not a deployed test (P-2) |
| 11 | a parsed-but-unused parameter | the answer ignores a parameter the caller named | change the parameter and re-run | a parameter that is parsed and unused is worse than a rejected one (P-15) |
| 12 | `server: cloudflare` on a host Cloudflare does not front | the header appears on any origin behind a Worker `fetch()` | compare against a control on another transport | `server: cloudflare` is not evidence of a Cloudflare front (P-38) |
| 13 | an unreachable destination by class | every dial fails in 0 to 3 ms, or a name resolves into a refused range | dial a control in the same class | a destination can be unreachable by class, not by name (P-6, P-35, P-36) |
| 14 | a latency number that belongs to the origin's idle close | the port is named, and the number is the same for every host | repeat against a different port on the same host | a latency measurement is of the pair, so name the port (P-25) |
| 15 | a `200` with a zero-length body | status `200`, `content-length: 0`, no bytes | count the bytes, not the status | a `200` with no body is a failure (P-28) |
| 16 | a substitution reported as the capture asked for | `x-web-capture-substituted: true` | read the two headers beside the timestamp | a substituted capture is not the capture you asked for |
| 17 | a cached answer with fresh headers | `x-web-cache: hit` | change one parameter and re-run | a `hit` is a stale answer, not a fresh one |
| 18 | a snippet quoted as a page read | the claim rests on `snippet`, not on a body | fetch the page, or label the claim `reported` | a snippet is a quotation, not a page read |
| 19 | a PDF that is not the document's text | `content_kind: landing-page`, or words in the low tens | compare `pages` to the PDF's page count | a document target can answer with the page about the document |
| 20 | a signature field nothing validates | the same bytes arrive with the token corrupted | corrupt the token and re-fetch | an unvalidated signature is not a gate |
| 21 | a table of numbers with no billing basis | the price is quoted without a period | read the vendor's own structured data | a price without its billing term is not a price |
| 22 | a conversion that eats its own deadline | `504` with `x-reader-fallback: deadline`, no pages at all | re-run with no `__timeout-ms` | a conversion needs its own budget |

## 1. A `200` carrying a wall, and the family it belongs to

**The shape.** The origin refused, and the layer between you and the origin answered
`200` with something that is not the page. Wall, block page, sign-in wall, proof of work,
an empty shell.

**The signature.** A body under 30 words. `confidence: low` in the front matter. A
challenge marker in the title, such as `just a moment`, `attention required` or `prove
you are human`. A `final_url` on a host that serves a notice page.

**The measured case.** `read.web.pkgforge.dev/https://linux.do` answered `200`, 18,041
bytes, `x-reader-upstream-status: 403`, `x-reader-fallback: challenge`,
`x-web-provider: contextdev` (measured 2026-10-22T04:08Z). The status line says success.
The only signals that it is a wall are `upstream_status` and `x-reader-fallback`, and
neither is in the body.

**The probe.** Read the body and the provenance headers, in that order, and never the
status line alone. Where the reader returns a `confidence` or an `x-reader-dropped`
token, read them before the content.

**The rule.** ⛔ **Never trust HTTP 200.** Record status, bytes and a digest on every
download, and refuse a body whose size or first bytes contradict what the origin should
have sent.

⚠ **A status-only probe overstates open registration by about 25%** on the academic
population measured here: Anubis and Bunny Shield both return `200` with a
proof-of-work body.

## 2. A `200` carrying the wrong page

**The shape.** The origin redirects the researcher's egress to a notice page and the
redirect is followed, so the answer is a different page at a clean `200`.

**The signature.** `final_url` names a host other than the target's. The word count is
low and the content is about the researcher rather than the subject.

**The measured case.** `nodeseek.com/post-918318-1` answered `200` with 623 bytes, 29
words and `final_url: warning.nodeseek.com/ipv6-is-disabled`. Pinning
`__provider=contextdev` returned the real 5,806-byte post.

**The probe.** Compare `final_url` to the URL asked, on every read. Where a provider can
be pinned, pin it and compare the two answers.

**The rule.** A redirect that lands on a different host is a refusal wearing a `200`.
Reject the answer, and record which host it landed on, because the redirect target is
the finding.

## 3. A range answer that is a decoded slice

**The shape.** `Range` and a compressed representation cannot both be honoured. The
service asks the origin for the bytes, gets a compressed representation, decodes it and
returns the decoded bytes from the requested offset. The answer is a slice of something
you did not ask for.

**The signature.** `200` where a `206` was asked. Or a `206` whose `Content-Range` total
is the decoded length rather than the wire length. The contract's own token is
`range=decoded-slice(<coding>)` on the dial.

**The measured case.** Asking a gzip origin for bytes 0 to 99 returned `200` with 616
bytes and `decoded=gzip`, which is the whole decoded body. The same request against an
identity origin returned `206` with `Content-Range: bytes 0-99/6034`. The 100 bytes
matched the first 100 of the 6,034-byte body byte for byte, so the slice was of the
decoded representation.

**The probe.** `cmp` the returned slice against the same range of a full body you
already hold. Where the totals disagree, the slice is decoded.

**The rule.** A `206` can name a range it does not deliver. Ask for a transport that
sends identity, or take the whole body and slice it yourself.

## 4. A wall that arrives as a redirect

**The shape.** A policy layer in front of the destination answers with its own redirect,
and the researcher records "the origin moved you" for a decision the network made.

**The signature.** `HTTP/1.0 303` in a place where the origin serves `HTTP/1.1`.
`Location: https://blocked.teams.cloudflare.com?...` with empty reason fields. About 750
bytes, identical across runs. On a TLS port the same block arrives as a synthetic
`handshake_failure` alert instead of any HTTP at all.

**The probe.** Read the `Location` host, not the status. Blocked-host redirects name the
blocking service.

**The rule.** ⛔ **Never read a `303` to a blocking service's own host as the origin's
redirect.** Where the redirect target is a policy page, the finding is that the route is
blocked, not that the page moved.

## 5. A private-destination refusal that looks like a success

**The shape.** A request to a loopback, private or metadata address answered by the
platform's own error page at `200`.

**The signature.** The body is the platform's error page, not the origin's. A `403` or
`530` with an error code the origin would not produce.

**The probe.** Compare the body to what a control request to a public host returns
through the same path. A body that is identical across two unrelated targets is the
platform's.

**The rule.** A `403` or a `530` may be the platform, not the origin, so never infer a
refusal from a status. Name which layer refused, or the finding is about the wrong party.

## 6. A stream cut by a budget that ends as a clean `200`

**The shape.** A JavaScript-pumped stream is cut when the runtime's CPU budget expires.
The client sees a `200` and a short body, and curl exits 0.

**The signature.** The byte count is under `Content-Length`. Or curl exit 0 with a body
shorter than the object.

**The measured case.** A 757,624,512-byte download through a proxy returned a clean
`200` with curl exit 0 and fewer bytes than the file. The same proxy carried a 100 MiB
file byte-identical, and a 1 GiB file whole in 33.4 seconds at 30.7 MiB/s, so the
ceiling is not a fixed size.

**The probe.** `wc -c` the body and compare it to `Content-Length`, then hash it against
a digest taken elsewhere. ⛔ A matching length is not a matching file.

**The rule.** A large download's length is checked, never assumed. The hazard is real and
unsized, so the only safe form is a byte count plus a digest.

## 7. A header mutation that belongs to the transport, not the platform

**The shape.** A header arrives changed, or is reported changed, and the researcher
attributes it to the platform. Then a different transport on the same platform does not
do it.

**The signature.** Two runs of the same request on two transports produce two header
sets. Or a report of a mutated header names one the origin received intact.

**The measured case.** A report said `headers=partial(accept-encoding)` for a header the
origin had received unchanged, over a transport that writes its own bytes. The
declaration was true of one branch and false of the other, and nothing in the type system
or the report distinguished them.

**The probe.** Ask an origin that echoes the request back, on each transport, and diff
the sets. Insertion order is not wire order: only an echo can tell you what arrived.

**The rule.** Report a header fact per transport, never per platform. Never claim a
header value was delivered without measuring it at the origin.

## 8. A compressed body with no `content-encoding`

**The shape.** The edge drops a coding the client never declared, so the client receives
gzip bytes and no header saying so.

**The signature.** The first two bytes are `1f8b`. No `content-encoding` header. A body
that fails to parse as text.

**The probe.** Read the first two bytes of every body before parsing it.

**The rule.** Declare `Accept-Encoding` when you measure bytes, or you receive gzip with
no header and a parser that reports a syntax error instead of an encoding.

## 9. A decoded body under the origin's framing headers

**The shape.** The runtime decodes the body on the way in and does not rewrite
`content-encoding` or `content-length`.

**The signature.** `HEAD` reports a size the `GET` body does not have. `content-encoding:
gzip` beside a plaintext body.

**The measured consequence.** `HEAD` on a compressing origin carries no usable
`Content-Length`, so the origin's size cannot be learned through a decoding proxy at all.

**The probe.** `wc -c` the body and compare to the header. Where they disagree, the
header is the wire form and the body is the decoded one.

**The rule.** ⛔ **Never forward a proxied `Content-Length` as an object's size.** Count
the bytes you got.

## 10. A local test that passes and a deployed edge that fails

**The shape.** A defect that does not reproduce in the local runtime reproduces on the
deployed edge, because the edge is the only place the behaviour exists.

**The measured case.** A `Set-Cookie` data loss did not reproduce under the local
development runtime and did reproduce on the live edge.

**The probe.** Run the probe against the deployed service. A local run establishes what
the code intends, not what the edge does.

**The rule.** A local test is not a deployed test. Where the claim is about a deployed
behaviour, the probe runs against the deployment, and the version string is recorded
with it.

## 11. A parsed parameter that is not used

**The shape.** A request names a parameter the service accepts and ignores. The request
succeeds and the behaviour is unchanged, so the caller believes the parameter was
applied.

**The signature.** The same answer with the parameter set to two opposite values.

**The probe.** Change the parameter to its opposite and re-run. A parameter that changes
nothing is not applied.

**The rule.** A parsed-but-unused parameter is worse than a rejected one, because a
rejection is visible and this is not. ⛔ **A probe that reports a configuration it never
applied is a fabricated measurement.**

## 12. `server: cloudflare` on an origin Cloudflare does not serve

**The shape.** A header that reads like provenance is written by the layer, for every
origin.

**The signature.** The same header on a host that is demonstrably served by another CDN.

**The probe.** Compare against the same host fetched by a path that does not write the
header.

**The rule.** `server: cloudflare` is not evidence of a Cloudflare front. The signal that
a destination is Cloudflare-served is a transport refusal, not a response header.

## 13. An unreachable destination by class

**The shape.** A destination is unreachable because of what it is, not because of its
name. Every dial to it fails, and the failure is fast enough to look like a local
problem.

**The signature.** Failure in 0 to 3 milliseconds. A refusal for every host in a range,
including ones the published list does not contain. A trailing dot on a name that skips
an exact comparison.

**The probe.** Dial a control in the same class and a control outside it. Where the class
control fails and the other succeeds, the class is the cause.

**The rule.** A destination can be unreachable by class, not by name, so a refusal is
evidence about the route and not about the host. ⚠ **Normalise a trailing dot before you
compare hostnames**, because `example.com.` and `example.com` are one name.

## 14. A latency number that belongs to the other end

**The shape.** A timing measurement is of a conversation, and one end can hold the
connection open. The number is then the origin's idle close, not the route's cost.

**The signature.** A port that costs about ten seconds where the same host on another
port costs tens of milliseconds.

**The probe.** Repeat against another port and against another host on the same port.

**The rule.** Name the port with every latency figure, because a latency measurement is
of the pair.

## 15. A `200` with nothing in it

**The shape.** A failure after the response head is committed arrives as a `200` with a
zero-length body.

**The signature.** `200`, `content-length: 0`, no bytes. Or a `content-length` above zero
with no bytes.

**The probe.** Count the bytes and refuse a `200` whose body is empty where a body was
expected.

**The rule.** This extends "never trust HTTP 200" to the body's length: a `200` with no
body is a failure, and a proxy can manufacture one.

## 16. A substitution reported as the capture you asked for

**The shape.** An archive answers the nearest capture it holds rather than the one asked
for, and the answer is a `200` with a page.

**The signature.** `x-web-capture-substituted: true`, `x-web-capture-asked` naming the
timestamp asked, `x-web-capture-timestamp` naming the one answered. `memento-datetime`
says the same.

**The probe.** Read the two capture headers beside the timestamp before citing it, and
compare the answered timestamp to the one asked.

**The rule.** A substituted capture is not the capture you asked for. Cite the timestamp
answered, and say it was substituted.

## 17. A cached answer wearing fresh headers

**The shape.** A `hit` serves a stored answer with headers generated now. The answer's
`fetched_at` is the stored instant, not this one.

**The signature.** `x-web-cache: hit`. `x-web-snapshot-at` older than the request.

**The probe.** Change one parameter so the cache key differs, and compare the two
answers. Where a price or a quota is the fact, the cache TTL decides whether you measured
it.

**The rule.** A `hit` is a stale answer with fresh headers. Read `x-web-cache` before you
record a price, and change a parameter when the fact is one that moves.

## 18. A snippet quoted as a page read

**The shape.** A search result carries the post body, and the body is long enough to look
like a page. It is a quotation with a length the broker chose.

**The signature.** The claim rests on a `snippet` field. The length is anywhere from 150
to 9,143 characters on the same day across queries.

**The probe.** Fetch the page where the page is reachable. Where it is walled, label the
claim `reported` and name the forum and the date.

**The rule.** A snippet supports a `reported` claim about what somebody wrote. It never
supports a `documented` claim about a vendor page, and it never carries a number in a
table on its own.

## 19. A document answered by the page about the document

**The shape.** A PDF or a document target is read by a provider that returns a landing
page: the abstract, the citation block, the download button.

**The signature.** `content_kind: landing-page`. A word count in the low tens where the
document has hundreds. No `pages`.

**The measured case.** A 15-page paper read through a PDF reader returned 6,150 words
with `source: pdf(unpdf)` and `pages: 15`. The same target read through a landing page
returns the abstract and a citation.

**The probe.** Compare the word count and the `pages` field to the document's own page
count. Where `pages` is absent and `content_kind` is `landing-page`, the text is not the
document's.

**The rule.** A document target can answer with the page about the document. Read
`content_kind` before you quote a document's text, and record a page count where one
exists.

## 20. A signature field nothing validates

**The shape.** A URL carries a signature, a token or an access key, and the server does
not read it.

**The signature.** The same bytes arrive with the field corrupted or removed.

**The probe.** Corrupt the token and re-fetch. Where the bytes still arrive, the gate is
decoration.

**The rule.** An unvalidated signature is not a gate, and the finding is that the
material is public.

## 21. A price with no billing basis

**The shape.** A vendor's headline price is one of two rates, and the page states which
only in its structured data or a footnote. The per-unit figure a reader derives is then
15.9% below the price they would actually pay.

**The signature.** Two rates for one plan on one page. A card headed "billed annually" or
"billed yearly". A structured-data description that says the price is the annual monthly
rate.

**The measured case.** A pricing page's structured data reads: "The price is the annual
monthly rate of the entry rung (pay for 10 months, get 12). Annual monthly rates run $58
to $108; monthly billing of the same rungs is $69 to $129." A per-1,000 figure built on
the quoted USD 58 is USD 0.23; the same plan billed monthly is USD 69, which is USD 0.28.
The error is 15.9% and it propagates into every derived figure.

**The probe.** Read the page's own structured data and every card heading, then quote the
monthly rate with the term beside it. Where both rates exist, record both.

**The rule.** ⛔ **A price without its billing term is not a price.** Quote the term
beside the amount, derive per-unit figures from the monthly price where the decision is
monthly, and name the annual rate as the discount it is.

## 22. A conversion that eats its own deadline

**The shape.** A PDF or an image is converted to Markdown, the converter's time comes out
of the caller's own deadline, and the deadline expires mid-conversion. The answer is a
`504` with no pages and nothing to quote.

**The signature.** `504`, `reason: deadline`, `x-reader-fallback: deadline`. The `detail`
says how much time was left when the conversion moved on, and a value of `0 ms` against a
provider walk that needs 5,000 is the shape: there was never enough budget for the
converter plus anything else.

**The measured case.** An image read with `__convert-images=1&__timeout-ms=3000` answered
`504` in 3.4 seconds with `x-reader-fallback: deadline` and "0 ms were left". The same
target with the default deadline answered `200` with 147 words in 20.7 seconds.

**The probe.** Re-run with no `__timeout-ms` and compare. Where the answer arrives with the
default deadline and fails with a short one, the conversion is the cost and the deadline is
the cause.

**The rule.** ⛔ **A conversion needs its own call and its own budget.** Do not put a short
`__timeout-ms` on a document target, do not batch images behind one deadline, and do not
read a `504 deadline` as "the page has no text".

## The shapes this catalogue does not carry

Two shapes a reader will meet and this topic has no measurement for.

**An iframe-only page.** A page whose content is entirely inside a frame. No document in
this topic reads one, and the broker's contract does not describe frame traversal, so
this is a gap rather than a shape: `unverified: iframe content not tested`.

**A cookie-gated redirect written by JavaScript.** A page whose redirect only happens
after a script runs. The broker follows a `meta-refresh` and a `link` stub once as a
redirect, and its contract describes no JavaScript redirect. `unverified: script
redirect not tested`.

⚠ **A gap is written as a gap.** The two above are named so the catalogue is not read as
complete, and so a page is not recorded as unreadable when the cause was an untried
route.

## Where each shape is answered

The broker facts live beside the operation they trap, in
[`free/broker.md`](broker.md). This document is the half that generalises: a shape here
belongs to any fetch path, any archive and any reader, and a session that meets it
through a different tool is not looking at a different defect.
