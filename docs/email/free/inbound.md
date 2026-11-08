# How much mail can arrive for nothing?

Receiving is the asymmetric half of this topic. Three providers route inbound mail
for nothing, and the widest of them states no volume limit because inbound routing
costs the provider a message-passing operation rather than a delivery reputation.

The answer: **Cloudflare Email Routing and Forward Email both state unlimited
inbound on the owner's domain.** What binds is not volume but the number of
destination addresses and routing rules, and those are per account, so a reader
with thirty domains still has one pool.

⚠ **"Unlimited" is not the same evidence at the two providers.** Cloudflare's is a
pricing-table row on a page that also publishes a limits page with 200 destinations,
200 rules and a 25 MiB message cap. Forward Email's is a plan-card bullet on a
pricing page with no limits page and no enforcement figure found. A documented
absence is weaker than a documented limit, and the two are not interchangeable.

Sorted by how much inbound the free tier carries.

| provider | free tier | what binds | identity | verdict |
| --- | --- | --- | --- | --- |
| Forward Email | unlimited domains, aliases and inbound | `retention-clamped`: forward only, no sending | email | `qualifies-with-caveat` |
| Cloudflare Email Routing | unlimited inbound | a count of 200 destination addresses per account, which is not one of the seven kinds | email | `qualifies-with-caveat` |
| ImprovMX | 1 domain, 25 aliases | `request-rate`: 500 forwards a day | email | `qualifies-with-caveat` |
| TempsMail | a throwaway inbox and read API | `request-rate`: 100 requests a minute per IP | email | `qualifies-with-caveat` |

## Forward Email

Unlimited domains, unlimited aliases, unlimited inbound email and a 50 MB
attachment limit, forwarding only (`documented`, 2026-10-22). The free tier cannot
send and keeps no mailbox.

⚠ **What kind of evidence the "unlimited" is.** The Free column of the pricing page
reads "Unlimited inbound email" among a list of plan features. No limits page, no
fair-use page and no message-rate figure was found for the free tier beyond the
50 MB attachment cap. So the absence is a marketing bullet on a plan card and it is
recorded as such.

That is a feature removed rather than a volume capped, which is why the verdict is
a caveat rather than a fail: for the receiving half of a mail chain this is the
widest offer found, and the missing half is a different provider's job.

Sending requires the USD 3/month Enhanced Protection tier.

Evidence: `forwardemail.net/en/pricing` (read 2026-10-22);
`dossier/email/forward-email.json`.

Verdict: `qualifies-with-caveat`.

## Cloudflare Email Routing

Unlimited inbound email on both Workers Free and Workers Paid, with 200 routing
rules per domain, 200 destination addresses per account, 30 domains per zone and a
25 MiB inbound message limit (`documented`, 2026-10-22).

This is the one genuinely unmetered thing in the topic, and it is the better
evidence of the two: a pricing-table row, plus a limits page that publishes the
three counts and the message cap. The cap a reader meets is the 200 verified
destination addresses, and it is **per account rather than per domain**, so thirty
domains share one pool of 200. That is the quiet constraint.

⚠ **200 destinations is a count and not a rate.** It has no window, so no kind in
the six-value vocabulary names it. The record carries it in `limits_note` with
`binding: none`, because nothing limits the volume and the count limits the shape.

A routing rule maps one pattern to one destination. Fanning a single address out to
several destinations needs a Worker that calls `forward()` once per destination,
which is a different shape and is not free in CPU time.

Evidence: `developers.cloudflare.com/email-service/platform/pricing/` and
`.../platform/limits/` (read 2026-10-22);
`dossier/email/cloudflare-email-routing.json`.

Verdict: `qualifies-with-caveat`. The receiving half of the free chain and the best
of them; no probe, because the inbound path could not be exercised from this host.

## ImprovMX

1 domain, 25 aliases, 500 forwards a day, 7-day logs and API access
(`documented`, 2026-10-22). The free plan forwards only and provides no mailbox.

500 forwards a day is the inbound analogue of the outbound daily cap and it is the
number to check before pointing a busy address at it. 25 aliases is the smaller
constraint for a catch-all.

Evidence: `improvmx.com/pricing/` (read 2026-10-22); `dossier/email/improvmx.json`.

Verdict: `qualifies-with-caveat`. No probe: the inbound path needs a domain
delegated to ImprovMX.

## TempsMail

A throwaway inbox and a read API, free with an account key, at 100 requests a
minute and 30 address creations a minute per IP (`documented`, 2026-10-22). A
created inbox can only be read from the IP and client that created it.

That IP binding is the constraint that decides whether the service is usable: it
cannot be read from a second machine, so it is a verification-code sink for one
host rather than a shared inbound endpoint. It is a lock rather than a rate and none
of the seven kinds names it.

Evidence: `tempsmail.org/page/api` (read 2026-10-22);
`dossier/email/tempsmail.json`.

Verdict: `qualifies-with-caveat`. It needs an account and a key.

## The DNS composition: does the inbound half combine with an outbound half?

⭐ **Two providers that each look fine do not automatically compose.** A domain has
one SPF record, one MX set and one DMARC record per name, so whoever writes second
either merges or breaks the first.

### What was measured on a real domain

A domain on Cloudflare nameservers with Email Routing enabled (`DOMAIN` below) was
read over DNS-over-HTTPS on 2026-10-22:

| record | value |
| --- | --- |
| `MX DOMAIN` | `route1`, `route2`, `route3.mx.cloudflare.net` |
| `TXT DOMAIN` | `v=spf1 include:_spf.mx.cloudflare.net ~all` |
| `TXT cf2024-1._domainkey.DOMAIN` | a DKIM public key, `v=DKIM1; h=sha256; k=rsa` |
| `TXT _dmarc.DOMAIN` | none |
| `TXT brevo._domainkey.DOMAIN` | none |

So Email Routing writes one SPF record that authorises Cloudflare's own sending
range and nothing else, and it uses a `cf2024-1` DKIM selector. Both facts matter
below.

### What Brevo actually requires

⚠ **Brevo does not write an SPF record on the free shared-IP plan.** Its
authentication article states: "The SPF and MX records are not required to
authenticate a domain. We only provide these records when setting up a dedicated
IP" (`help.brevo.com/hc/en-us/articles/12163873383186`, read 2026-10-22).

The collision is real and it is not the default case:

- **On the free shared-IP tier the two halves do not fight over SPF.** Brevo writes
  a Brevo code TXT, a DKIM record and a DMARC record. Cloudflare writes MX, SPF and
  its own DKIM at a different selector. Two DKIM selectors coexist by design, and
  one SPF record remains because only one provider wrote one.
- **The shared record is DMARC, not SPF.** Only one `_dmarc` record may exist per
  name, and Brevo offers its own `p=none` record with `rua=mailto:rua@dmarc.brevo.com`.
  Brevo's automatic flow asks before replacing an existing DMARC record, so the
  merge is a decision a reader makes and not a silent overwrite. `DOMAIN` has no
  DMARC record at all, so a reader following both guides in order would end up with
  Brevo's.
- **On a dedicated IP the collision is real.** Brevo then provides SPF and MX, and
  the SPF record must be merged into one string. Brevo publishes a merge article for
  exactly this case (`help.brevo.com/hc/en-us/articles/4414335084434`, read
  2026-10-22), which states "A domain can only have one SPF record" and works the
  example through.

⚠ **The RFC is the reason and it is not a vendor preference.** RFC 7208 section
3.2: "The SPF record is expressed as a single string of text found in the RDATA of
a single DNS TXT resource record; multiple SPF records are not permitted for the
same owner name", and section 4.5: "If the resultant record set includes more than
one record, check_host() produces the 'permerror' result". Two `v=spf1` records do
not weaken SPF; they void it for every message on the domain.

### Does the chain work, and under what arrangement

**Yes, on one domain, on Brevo's free shared-IP tier, with two conditions.**

1. **Brevo authenticates the domain and no SPF record is added.** The Brevo code,
   Brevo's DKIM record and one DMARC record go on the root; Cloudflare's SPF stays
   as it is. Two DKIM selectors, one SPF record, one DMARC record.
2. **Brevo's branded subdomain is not required, and its absence has a cost.**
   Brevo's own article states: "Without a branded subdomain, SPF passes via Brevo's
   infrastructure, not your own domain", and branding "moves SPF alignment onto your
   sending domain". So on the shared tier, SPF alignment rests on Brevo's return-path
   domain rather than the reader's, and authentication leans on DKIM alignment in the
   reader's domain. DMARC still passes on DKIM. A reader who wants strict alignment
   adds `mail.yourdomain.com` as a subdomain under Brevo and puts Brevo's SPF and MX
   records there, which is the arrangement that keeps the root clean.

⭐ **The arrangement to use: one domain, Cloudflare for MX and SPF, Brevo for DKIM
plus a DMARC record, and Brevo's branded subdomain only if strict SPF alignment is
wanted.** That is one chain over three record names and it does not require a second
domain.

### Which link is scarce

**The verified sending domain is the scarce link.** Cloudflare's half needs the
domain delegated to Cloudflare nameservers and needs nothing from Brevo. Brevo's
half refuses to authenticate a domain the account does not control, and its help
article says so: "You can only authenticate a domain that you or your business owns
and controls." So the domain is the one paid element, about USD 10.46 a year at
Cloudflare Registrar, and both halves depend on the same delegation.

The second scarce link is the outbound daily cap: 300 a day at Brevo, which a
1,000-contact list spends over four days.

### What was run and what was not

✅ **Run: the inbound half of a disposable chain, end to end, three times over.**
`GET /domains` on `api.mail.tm` returned one active domain, `maxxspace.com`;
`POST /accounts` returned 201 with `quota: 40000000` and no email verification;
`POST /token` returned a 360-character JWT; an SMTP message to `in.mail.tm` was
accepted; `GET /messages` returned it with the subject, the sender and both a text
and an HTML part (`measured`, 2026-10-22). Four requests and one SMTP message.

✅ **Run: the DNS state of a real Cloudflare-routed domain**, in the table above.

✅ **Run: the submission endpoint of the outbound half.** `smtp-relay.brevo.com:587`
answered 250, STARTTLS completed, and `AUTH LOGIN` returned 334 within two seconds
(`measured`, 2026-10-22). The endpoint exists and speaks the protocol.

⛔ **Not run: a message sent through Brevo and received at a Cloudflare-routed
address.** That needs Brevo account credentials, which the probe did not have.
So the **outbound half of the chain is documented and not measured**, the DNS
composition is measured, and the two are not the same claim.

⚠ **What was tried and failed.** Three Cloudflare MX hosts were dialled from this
host and none produced SMTP-level evidence: `route1`, `route2` and `route3`
answered 550 on the sender's IPv6 reverse lookup, and TCP 25 was reset over IPv4.
Neither result distinguishes a working inbound path from a broken one, and both are
recorded rather than read as a refusal.

## What did not work

- **Zoho Mail on the free plan as an IMAP target**: the free edition excludes
  IMAP, POP and ActiveSync, so there is no programmatic read. This kills the
  obvious "free mailbox plus IMAP fetch" chain. `qualifies-with-caveat`, recorded
  in the mailbox document.
- **Yandex 360 with a custom domain**: the custom-domain feature is behind the
  business plan. `paid-only`.
- **Cloudflare Email Routing to multiple destinations per address**: a rule maps to
  one destination, and a fan-out needs a Worker in the path.
- **A free inbound mailbox that stores mail**: every free offer here forwards.
  Storage is the paid part.
- **ImprovMX beyond 25 aliases or 500 forwards a day**: a paid plan.
- **Two SPF records, one per provider**: RFC 7208 returns `permerror`, so the domain
  has no SPF at all. The merge is mandatory and Brevo publishes the recipe.

## Chaining

**The unlimited-inbound chain.** `Forward Email or Cloudflare Email Routing for
unlimited inbound on the reader's domain -> a mailbox or a webhook`. The scarce
link is the destination-address count, 200 per account at Cloudflare, and it is not
the volume.

**The complete pair.** `Cloudflare Email Routing for inbound -> Brevo for 300 a day
out`. Cloudflare owns MX and SPF, Brevo owns DKIM and DMARC, and the root domain
carries one record of each type. The scarce link is the verified domain, and the
second is Brevo's 300 a day. The inbound half was measured on a disposable chain and
the DNS composition was measured on a real domain; the outbound half is not
measured. See [`senders.md`](senders.md) and §The DNS composition above.
