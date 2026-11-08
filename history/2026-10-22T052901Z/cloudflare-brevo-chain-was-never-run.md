# The Cloudflare-plus-Brevo chain was claimed and never run, and its two halves meet at DMARC

- **When:** 2026-10-22T05:29:01Z
- **Status:** corrected
- **Supersedes:** `docs/email/free/inbound.md` §The complete pair, in its previous form, which called the chain "the single most useful chain in the topic" without stating what its two halves do to one zone's DNS
- **Superseded by:** `docs/email/free/inbound.md` §The DNS composition: does the inbound half combine with an outbound half?
- **Evidence:** `developers.cloudflare.com/email-routing/get-started/enable-email-routing/`, `help.brevo.com/hc/en-us/articles/12163873383186`, `help.brevo.com/hc/en-us/articles/35946791638802`, `help.brevo.com/hc/en-us/articles/4414335084434`, `rfc-editor.org/rfc/rfc7208.txt`, and DNS-over-HTTPS reads of `ajam.dev` on 2026-10-22
- **Confidence:** documented, with the DNS state measured

## What we believed

`Cloudflare Email Routing for inbound -> Brevo for 300 a day out` was presented as a
working chain: "a whole inbound and outbound mail presence on one domain for the
price of the domain". Nothing in `docs/email/` mentioned SPF, DKIM or MX.
`grep -rn "SPF\|DKIM\|MX record" docs/email/` returned no line.

## What we found

Three things, and the second is the one that changes the advice.

**The collision is at DMARC and not at SPF.** Brevo's authentication article states:
"The SPF and MX records are not required to authenticate a domain. We only provide
these records when setting up a dedicated IP." On the free shared-IP tier Brevo
writes a Brevo code TXT, a DKIM record and a DMARC record. Cloudflare writes MX, one
SPF record and a DKIM record at its own selector. Two DKIM selectors coexist, and
only one provider wrote an SPF record, so the two halves do not fight over it.

What they do share is `_dmarc`, where one record may exist. Brevo's flow asks before
replacing an existing DMARC record, so the collision is a decision rather than a
silent overwrite.

**On a dedicated IP the collision is real and the merge is mandatory.** Brevo then
provides SPF and MX, and a domain may carry only one SPF record. RFC 7208 section
3.2 forbids a second and section 4.5 returns `permerror` when one is present, which
voids SPF for every message on the domain rather than weakening it. Brevo publishes
a merge article for this case.

**The chain works on one domain, with a caveat about alignment.** Without a branded
subdomain "SPF passes via Brevo's infrastructure, not your own domain", so on the
shared tier SPF alignment rests on Brevo's return-path and DMARC passes on DKIM
alignment. A reader who wants strict SPF alignment adds a `mail.` subdomain.

The measured DNS state of a real Cloudflare-routed domain, `ajam.dev`, is
`v=spf1 include:_spf.mx.cloudflare.net ~all` on the root, MX at
`route{1,2,3}.mx.cloudflare.net`, a DKIM key at `cf2024-1._domainkey`, no DMARC
record and no Brevo selector. That is the shape the document now describes.

## How we found it

An adversarial review ran the mail.tm chain end to end and noted that the pair had
never been run. This session read the two vendors' own DNS instructions, quoted
them, fetched RFC 7208 for the multi-record rule, and read the live DNS of a domain
already using Cloudflare Email Routing.

The mail.tm chain was re-run here on a fresh account rather than inherited: one
active domain, 201 with `quota: 40000000`, a 360-character JWT, an SMTP message
accepted at `in.mail.tm`, and the message read back with subject and sender. The
inbound half of a disposable chain is measured three times over.

## What it cost us

A reader following the two sections in order would have overwritten whichever
authorisation they configured second, and the failure is quiet: mail still sends,
SPF and DMARC fail at the receiver, and the first symptom is a spam folder rather
than an error. That is the "two providers that each look fine and fight over DNS"
shape the brief asked to be tested, and the corpus had asserted the chain instead.

The outbound half of the chain is still not measured. Brevo credentials were not
available, so what is proved is the DNS composition and the submission endpoint, and
what is not proved is a delivered message.

## What a future session should do differently

**A chain is a DNS claim before it is a product claim, and DNS is cheap to read.**
Both vendors document their own records and neither documents the other's, so the
composition is a question the corpus has to answer for itself. A DNS-over-HTTPS
query against a domain already using one half costs one call and settles most of it.

⭐ **The migration to look up first is "does the vendor require an SPF record at
all".** SPF was the assumed collision and it was the wrong one: Brevo does not write
SPF below a dedicated IP, and DMARC was the shared name. Assuming the collision
without checking which record collides produced a recommendation that was wrong in
both directions, too alarmist about SPF and silent about the record that does
collide.
