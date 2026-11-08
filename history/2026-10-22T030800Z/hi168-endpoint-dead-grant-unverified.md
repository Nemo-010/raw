# hi168's S3 endpoint no longer answers, and the 500 GB to 1 TB grant was never verified

- **When:** 2026-10-22T03:08:00Z
- **Status:** superseded
- **Supersedes:** `docs/storage/free/cloud-tenants.md` section "The consumer drives with an open foreign signup"
- **Superseded by:** `docs/storage/free/cloud-tenants.md` section "The consumer drives with an open foreign signup"
- **Evidence:** `curl -qsS -D - https://fetch.web.pkgforge.dev/https://s3.hi168.com/` returned 526 on 2026-10-22; `https://www.hi168.com/` returned 200 with 4,668 bytes
- **Confidence:** measured

## What we believed

Three seed artefacts stated the 500 GB rising to 1 TB grant as settled fact: `FINAL-REPORT.md`
sections 4, 8 and 11, and `ROUND2-FINDINGS.md`. The source was a third-party blog published
2026-03-12 and a nodeloc thread, not hi168's own pricing page.

The report's own audit removed the `✅` marks from all three places and marked the figure
disputed, because no login was ever performed. It did not change the figure.

The endpoint finding was separate and it was recorded as `SEC_E_UNTRUSTED_ROOT`, with the note
that the host answers with verification disabled. That reading made hi168 a live router behind an
incomplete certificate chain, which is a fixable problem rather than a dead host.

## What we found

Three things, and the third is the one that changes the verdict.

The grant is contradicted inside the corpus. A nodeloc post dated 2026-01-19 says new signups
already receive 5 GB: "目前新用户注册只有5G了". The March blog still describes 500 GB on
registration. Either the grant was restored, or the later blog repeated marketing copy that the
January poster had already falsified, and the corpus cannot tell which.

The email-login path exists as a form label, `账号/手机号/邮箱`, and no signup was executed. So
"email login verified" was never true.

And the endpoint no longer answers at all. Through the fetch broker on 2026-10-22,
`s3.hi168.com` returned **526**, which is a Cloudflare origin TLS failure, rather than the
earlier certificate error. The `www` host returns 200 with 4,668 bytes. The "live router behind an
incomplete chain" reading does not hold, because there is no router answering now.

## How we found it

One request through the fetch broker, which reports true status codes rather than a reader's
rendering of a failure. The earlier finding came from a direct `curl` on a Windows client, where
schannel's `SEC_E_UNTRUSTED_ROOT` is a local trust-store verdict and says nothing about whether the
origin answers.

## What it cost us

A Tier-1 row. hi168 appeared in the report's Tier-1 table at rank 10 of 12 and in the §8
registration table as one of four free providers "genuinely open at >= 500 GB". The audit had
already reduced that count from five to four by excluding hi168; the row stayed anyway.

The second cost is a wrong mechanism. A reader who trusted "live router behind an incomplete
chain" would have tried to reach the host with verification disabled, which was the exact test
that failed.

## What a future session should do differently

Distinguish a client-side trust failure from an origin failure. `SEC_E_UNTRUSTED_ROOT` from
schannel means the local machine does not trust the chain; a 526 from Cloudflare means the edge
could not complete a handshake with the origin. They are different facts and only the second is
about the provider.

And when a figure is marked disputed in three places and none of them is the vendor's own page,
change the verdict rather than the annotation. A disputed number in a recommendation is a
recommendation with an unverified premise, and the honest verdict for a quota nobody measured is
`unverified`, not a footnote.
