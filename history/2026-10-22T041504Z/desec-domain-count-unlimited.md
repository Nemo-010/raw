# deSEC was recorded as having no published cap and recommended for many zones, and a new account gets one domain

- **When:** 2026-10-22T04:15:04Z
- **Status:** corrected
- **Supersedes:** `dossier/domains-dns/desec.json` (`free_tier`, `limits`, `binding`, `confidence`), `docs/domains-dns/free/managed-dns.md` §deSEC, §Chaining, `docs/domains-dns/README.md` (the record table, the numbers to carry away, the rejected count)
- **Superseded by:** `dossier/domains-dns/desec.json` as corrected, and the two documents
- **Evidence:** `talk.desec.io/t/feedback-about-recent-limit-changes/1834`, `talk.desec.io/t/how-to-apply-for-a-spot/1370`, `yepoleb.at/blog/2025/10/27/my-experience-with-desec/` and `desec.io/signup`, all read 2026-10-22
- **Confidence:** reported

## What we believed

The comparison table read "deSEC | no published cap; 300 RRset changes per domain per day", the
record set `free_tier.unit` to `unlimited`, and the verdict was "the right choice for many small
zones". The reasoning was that the rate-limit page documents per-domain rates and says nothing about
how many domains an account may hold, which was read as no cap.

## What we found

deSEC's rate page documents per-domain rates and says nothing about the domain count. The count
exists anyway, and it is of order one.

A deSEC staff reply on the project's own forum gives the formula: "the limit is
`max(1, s + round(sqrt(s)))`, were `s` is the number of domains delegated to us with DNSSEC
enabled", which is 6 for `s = 4`. An earlier thread records a new account's allowance: "New accounts
are limited to one domain and there is a note when you add a domain: 'Contact support to apply for a
higher limit.'" An independent write-up records the same experience, and the signup form says only
"Your first domain (you can add more later)".

## How we found it

An adversarial review listed the threads. They were re-read here and a fourth independent source
was added, because a single forum post is a weak basis for a finding that changes a verdict.

## What it cost us

A recommendation for exactly the use the counter constrains. "The right choice for many small zones"
is the sentence a reader building a multi-tenant scheme acts on, and the scheme meets a domain
counter of order one before it meets the rate limit the document was measuring.

It also cost a convention breach that was invisible at the time: `unit: "unlimited"` is a documented
absence promoted to a capacity, and `METHODOLOGY.md` section 3.2 forbids exactly that. The absence of
a published number is not the absence of a limit, and this record is the example.

## What a future session should do differently

**An unpublished number is not a missing limit, and `unlimited` is never the right unit for one.**
The set that is genuinely unlimited is empty until somebody measures it.

**One signup settles this.** The record now says the number is `reported`, and one email address and
one account creation would raise it to `measured`. That is cheaper than the wave this correction
took, and it is the same trade the corpus makes everywhere else when a number is load-bearing.
