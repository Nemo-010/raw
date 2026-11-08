# Where does mail land, and how is it read programmatically?

A mailbox is storage, and the free ones remove exactly the thing a program needs.
Zoho's free edition has 5 GB per user and excludes IMAP, POP and ActiveSync, so it
is a mailbox that cannot be read by a program. That is the finding for the whole
mailbox class, and it is why every verdict here is a caveat.

The other half is throwaway inboxes, which are the opposite trade: no storage worth
having and a fully programmatic read path. One of them was measured end to end.

Sorted by whether a program can read them.

| provider | free tier | what binds | identity | verdict |
| --- | --- | --- | --- | --- |
| mail.tm | a 40 MB inbox, keyless API | `per-object-cap`: 40 MB per inbox | anonymous | `qualifies-with-caveat` |
| TempsMail | a throwaway inbox, read API | `request-rate`: 100 requests a minute, IP-bound | email | `qualifies-with-caveat` |
| OVH MX Plan | 5 GB mailbox with a domain | `write-gated`: one mailbox per domain | card | `qualifies-with-caveat` |
| Zoho Mail | 5 users at 5 GB each | `retention-clamped`: no IMAP, POP or ActiveSync | email | `qualifies-with-caveat` |
| Yandex 360 | free personal mail | `write-gated`: a custom domain needs the business plan | country-phone(RU) | `paid-only` |

## mail.tm

A keyless REST API that creates an inbox, a token endpoint that returns a JWT, and
a messages endpoint. Measured on 2026-10-22 on a fresh account:

| step | result |
| --- | --- |
| `GET /domains` | 200, one active domain: `maxxspace.com`, id `6aa6b995482bea6f4a97f585` |
| `POST /accounts` | 201, `quota: 40000000`, `used: 0`, no email verification |
| `POST /token` | 200, a 360-character JWT |
| an SMTP message to `in.mail.tm` | accepted, `sendmail` returned no refusal |
| `GET /messages` | 200, the message listed with its subject and sender |
| `GET /messages/{id}` | 200, subject, sender, a text part and an HTML part |

That is the whole verification-code chain in four requests and one SMTP message.
The account was created with no key, no card and no email round trip, which is what
makes this the one offer in the topic that a script can use unattended.

What breaks: 40 MB per inbox against the server's advertised 25 MiB message size,
so one inbox holds one large message. There is one active domain, so a domain change
invalidates every address a script has recorded.

There is no published rate limit, which is a documented absence and not a
permission.

Evidence: probe records in `dossier/email/mail-tm.json`.

Verdict: `qualifies-with-caveat`.

## TempsMail

A receive-only API with a 100-request-a-minute and 30-address-creation-a-minute
limit per IP, and an inbox that can only be read from the IP and client that
created it (`documented`, 2026-10-22). It needs a free account and a personal key.

The IP binding is what makes it a different tool from mail.tm: it works for one
host's automated signups and not for a distributed flow. It is a lock rather than a
rate and no kind in the six-value vocabulary names it.

Evidence: `tempsmail.org/page/api` (read 2026-10-22);
`dossier/email/tempsmail.json`.

Verdict: `qualifies-with-caveat`.

## OVH MX Plan

A 5 GB mailbox per account with a free 100 MB web hosting plan, bundled with a
domain at OVH (`documented`, 2026-10-22). One mailbox per domain on the free
activation, with regional variation.

This is the cheapest route to a real mailbox with a custom domain, and unlike Zoho
it does not remove the protocols. It costs a domain and a hosting plan.

⚠ **The identity is one value and not two.** `identity_cost` takes exactly one of
seven values, and `card` is the strongest gate present, so the card is the kind and
the domain is the second gate.

Evidence: `docs.ovhcloud.com/en/guides/web-cloud/web-hosting/activate-start10m.md`
(read 2026-10-22); `dossier/email/ovh-mx-plan.json`.

Verdict: `qualifies-with-caveat`.

## Zoho Mail

5 users, 5 GB each, 1 custom domain and a 25 MB attachment limit
(`documented`, 2026-10-22). The free edition excludes IMAP, POP and ActiveSync, so
the only way to read it is webmail or the mobile app.

That is a hard fail on the programmatic-access filter, and it is recorded because
it is exactly the chain a reader reaches for first: free mailbox, then IMAP fetch.

The free edition is also region-limited; the page title reads "Free for 5 Users in
select regions".

Evidence: `zoho.com/mail/zohomail-pricing.html` (read 2026-10-22);
`dossier/email/zoho-mail.json`.

Verdict: `qualifies-with-caveat`. A mailbox that cannot be read by a program.

## Yandex 360

Free personal mail; a custom domain requires a paid business plan
(`documented`, 2026-10-22). The signup flow is RU-facing, so a Russian number is
the practical route.

Evidence: `360.yandex.com/business/tariff/` (read 2026-10-22);
`dossier/email/yandex-360.json`.

Verdict: `paid-only`.

## What did not work

- **Zoho Mail as an IMAP target**: no IMAP, POP or ActiveSync on the free edition.
- **Yandex 360 with a custom domain**: a business-plan feature.
- **mail.tm for a large inbox**: 40 MB per inbox against 25 MiB per message.
- **TempsMail from a second machine**: the inbox is bound to the creating IP.
- **A free mailbox with a large quota and open protocols**: none found. Every free
  mailbox either removes the protocols or caps the storage at 5 GB.
- **Three further disposable APIs, not opened**: MTempMail, NenzMail and the
  `mail.lesin.org` API. None has a record, and their limits are `unverified` because
  no page was read. A reader who needs a fourth disposable inbox should open those
  three first.

## Chaining

**The verification-code sink.** `mail.tm inbox -> a signup form -> read the code
over the API`. Measured. The scarce link is the 40 MB inbox and the single shared
domain.

**The real mailbox.** `OVH domain plus hosting -> MX Plan -> any IMAP client`. The
scarce link is the domain and the hosting plan, and it is the only chain in this
document that yields a mailbox a program can read at 5 GB.
