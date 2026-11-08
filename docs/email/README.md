# email

Sending and receiving mail for nothing, and the caps that actually bind. The
question: **how much mail can go out and arrive a day for nothing, and what stops
it first?**

The structure of the market is simple and it is asymmetric. **Nobody gives away
bulk sending and everybody gives away bulk receiving.** Cloudflare Email Routing
states unlimited inbound on the owner's own domain, and Forward Email states the
same on a plan card with no limits page behind it. The best free daily outbound cap
found is 300 a day at Brevo, with a three-way tie at 100 to 200 a day behind it.

⚠ **The monthly figure is the binding one about as often as the daily figure is.**
A daily cap between a fifth and a thirtieth of the monthly one holds for four of
the fifteen rows: SMTP2GO at 5:1, Mailjet at 30:1, Mailtrap at 26:1 and Resend at
30:1. Every other row either states no daily figure, states that none exists, or
has no monthly figure to compare against. The daily cap is the number a launch
meets where it exists, and where it does not exist that is the finding.

⭐ **The daily cap is often not the first cap either.** SMTP2GO holds a new
account at 25 an hour until a sender domain is verified. Amazon SES starts every
account in a sandbox that can only mail verified identities. ZeptoMail holds at 100
a day until Zoho validates the account. MailerSend charges the free plan to a card.

## The five classes

| class | who is in it | what binds |
| --- | --- | --- |
| API sender, free forever | Brevo, SMTP2GO, Mailjet, Mailtrap, Resend, Mailgun, SendPulse, Sender, Loops, Plunk hosted | the daily cap where one is stated, the monthly one where it is not |
| API sender, finite or trial | ZeptoMail, Mandrill, MailerSend, Postmark, Scaleway | a credit that never refills, a card, or a tiny permanent allowance |
| Inbound routing | Cloudflare Email Routing, Forward Email, ImprovMX | destination addresses and aliases, not volume |
| Disposable inbox | mail.tm, TempsMail | a per-IP rate and an undocumented expiry |
| Outbound relay, self-hosted (the last resort) | Plunk self-host, Amazon SES behind it | reputation, and the sandbox |

## The documents

| document | the class | what it answers |
| --- | --- | --- |
| [`free/senders.md`](free/senders.md) | outbound API senders | how many messages a day can go out, and what stops first |
| [`free/inbound.md`](free/inbound.md) | receiving and routing | how much mail can arrive for nothing, and whether the two halves compose |
| [`free/mailboxes-and-disposable.md`](free/mailboxes-and-disposable.md) | mailboxes and throwaway inboxes | where mail lands, and how to read it programmatically |
| [`paid/bulk-sending.md`](paid/bulk-sending.md) | the cheapest real bulk rate | what a thousand messages cost when free is not enough |

## The daily cap, in one table

The number that stops a send mid-spike, highest first. "Not stated" and "absent" are
different answers: not stated means the vendor publishes a month and no day, absent
means the vendor says there is no daily limit.

| provider | per day | per month | ratio |
| --- | --- | --- | --- |
| Brevo | 300 | no monthly cap | not applicable |
| SMTP2GO | 200, and 25/hour before domain verification | 1,000 | 5:1 |
| Mailjet | 200 | 6,000 | 30:1 |
| Mailtrap | 150 | 4,000, shared with receiving | 26:1 |
| Resend | 100, UTC calendar day | 3,000 | 30:1 |
| Mailgun | 100 | not stated | not applicable |
| ZeptoMail | 100 until validated | 10,000 once, from one credit | finite |
| SendPulse | not stated as a day; 50/hour on SMTP | 15,000 | not applicable |
| Sender | absent, stated as "No limits" | 15,000 | 1:1 |
| Scaleway | not published | 300 | not applicable |
| Loops | absent; the window is a rolling 30 days | 4,000 | 1:1 |
| Plunk (hosted) | not published | 1,000 | not applicable |
| Postmark | absent; there is no daily allowance | 100 | not applicable |
| MailerSend | 100, and they are API requests rather than emails | 500 | not applicable |
| Plunk (self-hosted) | not applicable | not applicable | not applicable |

Postmark's 100 a month with no daily allowance is the only true monthly cap in the
set, and it is why the ratio column matters: a reader who plans on the monthly
number and meets a daily one loses the campaign, and a reader who plans on 100 a
day and meets a monthly ceiling of 100 loses the month.

## The dead ends, in one place

| provider | why it fails | verdict |
| --- | --- | --- |
| SendGrid | free plan retired 2025-05-27 and accounts paused after 60 days | `dead` |
| Postmark | 100 a month with no burst room | `fails-quota` |
| MailerSend | 500 a month and a card on the free plan | `fails-quota` |
| Mandrill | 500 in total, to one verified domain | `trial-only` |
| MailerLite | the free plan cannot send over the API | `fails-egress` |
| Yandex 360 | a custom domain needs the business plan | `paid-only` |
| Cloudflare Email Sending | arbitrary recipients need the paid Workers plan | `paid-only` |

## The records

One record per provider, in [`../../dossier/email/`](../../dossier/email/). The
tables above are a view of those records; where they disagree, the record is right.

⚠ **`qualifies` requires a probe of the read path and no sender in this topic has
one.** Every record that would carry `qualifies` carries `qualifies-with-caveat`
with the missing probe named, because no message was sent through any vendor. The
probe is narrower: six sender submission endpoints answered with a banner, STARTTLS
and an `AUTH LOGIN` challenge, and one disposable chain was measured end to end.

## What this topic does not know

- **One chain was measured end to end and it is a disposable one.** mail.tm was
  exercised on a fresh account: one active domain, `POST /accounts` returning 201
  with `quota: 40000000`, a JWT, an SMTP message accepted at `in.mail.tm`, and the
  message read back with its subject and sender. No vendor's outbound delivery was
  proved, because that needs account credentials.
- **No inbound volume was measured.** "Unlimited inbound" is a vendor statement on
  Cloudflare's and Forward Email's pages, and the numbers that bind there are
  destination addresses and message size rather than volume.
- **Scaleway's two pages disagree, and a third figure is unpublished.** The pricing
  page says 300 a month for the free tier, the capabilities page says 10,000 a month
  is the service default, and new organisations face stricter initial limits set by
  support with no number published. So a new account gets neither published figure
  and the number is unverified.
- **SendPulse and Sender both state 15,000 a month.** SendPulse publishes 50 emails
  an hour on SMTP and no daily figure; Sender publishes no daily limit at all. Both
  answers are recorded as the vendor states them and neither was tested.
- **The Cloudflare-plus-Brevo chain composes at DMARC and not at SPF**, and the
  outbound half is not measured. See
  [`free/inbound.md`](free/inbound.md) §The DNS composition.

## Records that no other document names

This list holds each `measured` or `documented` record of this topic that no other
document of `docs/` names.

<!-- generated:start topic=email kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `buttondown` | Buttondown | qualifies-with-caveat | documented |
| `elastic-email` | Elastic Email | qualifies-with-caveat | documented |
| `fastmail` | Fastmail | paid-only | documented |
| `maileroo` | Maileroo | qualifies-with-caveat | documented |
| `mailo` | Mailo | paid-only | documented |
| `mailpace` | MailPace | fails-quota | documented |
| `migadu` | Migadu | paid-only | documented |
| `purelymail` | Purelymail | paid-only | documented |
| `tuta` | Tuta (formerly Tutanota) | paid-only | documented |
<!-- generated:end -->
