# How many messages a day can go out, and what stops first?

An API sender takes an HTTPS or SMTP request and delivers it from a shared IP. The
free tier is a daily allowance, and where the vendor states both a daily and a
monthly figure the daily one is what a launch meets.

The answer is 300 a day at Brevo, then 200 a day at SMTP2GO and Mailjet, then a
cluster at 100. The first cap a new account meets is frequently lower than any of
those, because account validation sits in front of the allowance: 25 an hour at
SMTP2GO before domain verification, 100 a day at ZeptoMail before Zoho validates,
a sandbox at Amazon SES.

⚠ **Seven of the fifteen rows state a daily cap as a number, and every row states
its position in that column.** Three state an explicit absence: Sender says "No
limits" on two of its own pages, Loops publishes a rolling 30-day window with no
daily field, and Postmark has no daily allowance by design. Two state a rate that
does the same job: SendPulse publishes 50 an hour on SMTP and MailerSend publishes
100 API requests a day. Two publish neither figure. One is software. Where a vendor
publishes only a monthly figure, whether the month can be spent in one day is not
established, and that is the open question rather than a footnote.

⚠ **Every row fills all five columns.** A dash would mean the question was not
asked; "not stated", "not established" and "not published" mean it was asked and the
vendor does not answer it.

Sorted by what a reader can actually reach, highest first.

| provider | per day | per month | per recipient | sending domain | card | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Brevo | 300 | none above it | counts as a send | authentication recommended, not required | no | `qualifies-with-caveat` |
| SMTP2GO | 200, and 25/hour until a domain is verified | 1,000 | counts as a send | yes, to lift the hourly cap | no | `qualifies-with-caveat` |
| Mailjet | 200 | 6,000 | not stated | not established | no | `qualifies-with-caveat` |
| Mailtrap | 150 | 4,000, shared with receiving | not stated | 1 domain | no | `qualifies-with-caveat` |
| Resend | 100, UTC calendar day | 3,000 | each recipient counts | yes, verified | no | `qualifies-with-caveat` |
| Mailgun | 100 | not stated | not stated | 1 custom domain | no | `qualifies-with-caveat` |
| ZeptoMail | 100 until validated | 10,000 once, from one credit | not stated | yes, validated | not established | `qualifies-with-caveat` |
| SendPulse | none stated; 50/hour on SMTP | 15,000 | 1 MB per message on Free | yes, authenticated | not stated | `qualifies-with-caveat` |
| Sender | none, stated as "No limits" | 15,000 | not stated | not established | no | `qualifies-with-caveat` |
| Scaleway Transactional Email | not published | 300 | 10 per email | yes | to raise limits | `qualifies-with-caveat` |
| Loops | none stated | 4,000 per rolling 30 days | not stated | not established | no | `qualifies-with-caveat` |
| Plunk (hosted) | not published | 1,000 | counts as a send | not established | no | `qualifies-with-caveat` |
| MailerSend | no email cap; 100 API requests | 500 | one request may address many | 1 domain | yes | `fails-quota` |
| Postmark | none | 100 | not stated | verified signature | no | `fails-quota` |
| Plunk (self-hosted) | not applicable | not applicable | not applicable | none from the software | no | `qualifies-with-caveat` |

## Brevo

300 email sends a day with no time limit on the free plan, and unused sends do not
roll over (`documented`, 2026-10-22). The help page states the campaign behaviour
explicitly: a campaign to more than 300 recipients delivers to 300 that day and the
rest need the Requeue option on successive days, so a 1,000-contact list takes
four days.

Once the daily limit is hit, up to 1,000 transactional emails are held in a retry
queue and anything beyond that is not delivered.

The 300 a day is the highest card-free daily cap found and there is no monthly
ceiling above it, which makes it the only free sender here whose monthly figure
cannot be the binding one.

**The other four fields.** A recipient counts as one send, so a 300-recipient
campaign is one day's whole allowance. Domain authentication is recommended and not
required: on a shared IP the SPF check passes through Brevo's own infrastructure
and SPF alignment rests on DKIM in the sending domain, which Brevo's branded
subdomain article states plainly. No card is required for the free plan.

Evidence: `help.brevo.com/hc/en-us/articles/208580669` and
`brevo.com/free-smtp-server/` (read 2026-10-22); the submission endpoint was probed
and answered 250 with STARTTLS and `AUTH LOGIN` 334; `dossier/email/brevo.json`.

Verdict: `qualifies-with-caveat`. No message was sent, so delivery is not proved;
the submission path is.

## SMTP2GO

1,000 a month, 200 a day, and 25 an hour while no sender domain is verified
(`documented`, 2026-10-22). Three stacked caps on one product, and the hourly one
is on the developer page and not on the pricing table.

**What binds and what is merely met first.** 25 an hour is 600 a day if sustained,
so it is not arithmetically the tightest cap. It is what a new account meets first,
and the pricing page will not sell a month above 1,000 anyway. The binding
constraint for one sender is the 1,000 a month once the domain is verified, and the
25 an hour is an onboarding gate that lifts.

**The other four fields.** A recipient counts as one send. A sending domain must be
verified to lift the hourly cap, and verification is the whole gate. No card is
required for the free plan.

Evidence: `developers.smtp2go.com/docs/rate-limiting` (read 2026-10-22); the
submission endpoint `mail.smtp2go.com:2525` answered 250 with STARTTLS and
`AUTH LOGIN` 334 (`measured`, 2026-10-22); `dossier/email/smtp2go.json`.

Verdict: `qualifies-with-caveat`. No message was sent.

## Mailjet

6,000 a month and 200 a day with 1,000 contacts, and the page states no credit card
is required at signup (`documented`, 2026-10-22).

⚠ **The queue-and-discard behaviour is `reported` and not documented.** The sentence
"over-quota mail is queued for three days and then discarded" came from a
knowledge-base article, `documentation.mailjet.com` article 360043048393, which
returns 404 on 2026-10-22, and the pricing page does not contain it. The record
carries it in `reliability_note` with that provenance. It may be true and it is not
currently checkable.

**Per recipient and domain.** Neither is stated on the page read. A card is not
required.

Evidence: `mailjet.com/pricing/` (read 2026-10-22); the submission endpoint
`in-v3.mailjet.com:587` answered 250 with STARTTLS and `AUTH LOGIN` 334
(`measured`, 2026-10-22); `dossier/email/mailjet.json`.

Verdict: `qualifies-with-caveat`.

## Mailtrap

4,000 emails a month and 150 a day on the free tier, with 1 user, 1 domain and 3
days of logs (`documented`, 2026-10-22). The pricing page's footnote reads "Email
limit per month. Shares quota between sending and receiving."

⚠ **The 4,000 is not a pool with a sendable sub-allowance.** The page does not state
one: the three occurrences of "1,000" on it are the sandbox message-store column and
the per-1,000 overage price. The shape is a single 4,000 shared between sending and
receiving, with a separate 150-a-day ceiling.

**The other four fields.** 150 a day is the number a launch meets and it is half
Brevo's. One domain is included. A card is not required.

Evidence: `mailtrap.io/pricing/` (read 2026-10-22); `dossier/email/mailtrap.json`.

Verdict: `qualifies-with-caveat`.

## Resend

3,000 a month and 100 a day, with the daily quota on a UTC calendar day rather than
a rolling 24 hours, resetting at midnight UTC (`documented`, 2026-10-22). Multiple
`To`, `CC` or `BCC` recipients count as separate emails, and received mail counts
against both quotas.

The UTC boundary is stated explicitly, which is unusual and useful: a spike at
23:50 UTC gets 100 more at midnight.

10 requests a second per account is the API rate and not the binding one.

Sending pauses above a 4% bounce rate, which is a reputation cap rather than a
volume cap and is the one that ends a free account mailing a scraped list.

**The other four fields.** Each recipient counts separately, which is the strictest
per-recipient rule in the set. A verified sending domain is required. No card on the
free plan.

Evidence: `resend.com/docs/knowledge-base/resend-sending-limits` (read 2026-10-22);
the submission endpoint `smtp.resend.com:587` answered 250 with STARTTLS and
`AUTH LOGIN` 334 (`measured`, 2026-10-22); `dossier/email/resend.json`.

Verdict: `qualifies-with-caveat`. The 100 a day is stated; delivery is not proved.

## Mailgun

100 messages a day with 1 custom domain, 1 inbound route, 2 API keys and one day of
log retention (`documented`, 2026-10-22). The help page returned HTTP 403 and the
body still extracted; the numbers match the pricing page.

⚠ **No monthly figure is published.** The pricing page offers "100 emails/day
included" and Mailgun's own comparison page restates it as "3,000 emails/month
(100/day limit)". The second is arithmetic on the first and is not a second limit,
so the record keeps the month unstated rather than quoting a derived one. A month of
100 a day is 3,000 at 30 days and 3,100 at 31, and neither is a number Mailgun
publishes.

**The other four fields.** One domain and one inbound route cap the shape rather
than the volume. A card is not required, which the help page states.

Evidence: `help.mailgun.com/hc/en-us/articles/203068914` (read 2026-10-22);
`dossier/email/mailgun.json`.

Verdict: `qualifies-with-caveat`.

## ZeptoMail (Zoho)

One free credit worth 10,000 emails, valid six months, with a 100 a day ceiling
until Zoho validates the account (`documented`, 2026-10-22). Credits do not refill.

This is a finite amount rather than a rate, which makes it the wrong shape for
anything with a schedule. The 100 a day is a write gate rather than a policy: it
lifts when a human validates the account.

**The other four fields.** A validated sending domain is required. Whether a card is
needed at signup is not established: Zoho's pricing path redirects to a CPaaS credit
page that states no monthly minimum and does not address the free credit.

Evidence: `zoho.com/blog/cpaas/announcing-quick-transition.html` and
`zoho.com/zeptomail/pricing.html` (read 2026-10-22); `dossier/email/zeptomail.json`.

Verdict: `qualifies-with-caveat`.

## SendPulse

Up to 15,000 emails a month on the free tariff, with 3 sender addresses and 250 MB
of image storage (`documented`, 2026-10-22).

**The daily figure is a rate and not a day.** No per-day cap appears on the pricing
table, and the SMTP limits page publishes 50 emails an hour for the free plan
(`documented`, 2026-10-22). 50 an hour sustained is 1,200 a day, which is below the
monthly allowance only if the month is short, so the hourly rate is what a burst
meets and 15,000 a month is what a sustained sender meets.

The free plan also refuses any message above 1 MB, which is a per-message cap rather
than a per-recipient one.

**The other fields.** Authenticated domains: 2 on the free SMTP plan. Whether a card
is required is not established.

Evidence: `sendpulse.com/pricing` and `sendpulse.com/knowledge-base/smtp/limits`
(read 2026-10-22); `dossier/email/sendpulse.json`.

Verdict: `qualifies-with-caveat`.

## Sender

Up to 2,500 subscribers and 15,000 emails a month, never expires, and "No credit
card, nothing to activate" (`documented`, 2026-10-22). Free-plan messages carry
Sender's branding.

⭐ **The daily cap is stated as absent, twice.** The pricing page's comparison table
reads "Daily email limits | No limits" for every plan including Free, and the
free-plan page repeats "No limits" (`documented`, 2026-10-22). That is a documented
absence rather than a number, so the daily figure is recorded as absent and the
15,000 a month is the only ceiling. Whether 15,000 can leave in one day therefore
follows from the vendor's own statement: it can.

⚠ **A documented absence is still weaker than a documented limit.** The absence is
one vendor's promise on two pages of its own site, and it cannot be multiplied.

**The other fields.** A 2,500-subscriber ceiling caps a campaign's reach. One user
seat. Sending-domain requirements are not established.

Evidence: `sender.net/pricing/`, `sender.net/pricing/free-plan/` and
`sender.net/email-marketing-cost-calculator/` (read 2026-10-22);
`dossier/email/sender-net.json`.

Verdict: `qualifies-with-caveat`.

## Scaleway Transactional Email

300 emails a month per organisation on the free tier, then EUR 0.25 per 1,000
(`documented`, 2026-10-22). Ten recipients per email, stated as a default.

⚠ **A new organisation gets neither published figure.** The capabilities page
states 10,000 a month as the service default and that new accounts face stricter
initial limits set by support with no number published. So 300 is a ceiling on the
free tier and not a plan: a reader who provisions for 300 may meet a lower limit
first, and the size of that limit is `unverified` because Scaleway does not publish
it.

**No daily cap is published.** Neither page states one, and the FAQ's only rate
language is about billing and reputation. Ten recipients per email is the only
per-message figure.

**The other four fields.** 10 recipients per email. A card is required to raise the
limits, and identity validation is part of the same step.

Evidence: `scaleway.com/en/pricing/managed-services/`,
`scaleway.com/en/docs/transactional-email/reference-content/tem-capabilities-and-limits/`
and `scaleway.com/en/docs/transactional-email/faq/` (read 2026-10-22);
`dossier/email/scaleway-tem.json`.

Verdict: `qualifies-with-caveat`.

## Loops

4,000 sends per rolling 30 days and 1,000 contacts, marketing and transactional
combined (`documented`, 2026-10-22). The 1,000-contact ceiling binds, not the 4,000:
a list of 1,000 can receive four messages a month.

**The window is rolling and there is no daily field.** The machine-readable pricing
file carries `send_window = rolling`, `send_window_days = 30` and `send_limit =
4000`, and no daily figure at all (`documented`, 2026-10-22). Whether 4,000 can
leave on day one is therefore not stated, and it is the question that decides
whether this is a burst sender.

**The other fields.** 1,000 contacts, and sends beyond the first 1,000 are refused
rather than billed. No card is required.

Evidence: `loops.so/.well-known/pricing.txt` (read 2026-10-22);
`dossier/email/loops.json`.

Verdict: `qualifies-with-caveat`.

## Plunk (hosted)

1,000 emails a month with unlimited contacts (`documented`, 2026-10-22). An
attachment costs two credits and inbound mail counts against the same allowance.

The 3,000 a month that circulates widely is the older figure and the billing page
says 1,000.

**No daily cap is published.** The billing page describes per-category caps that the
account holder sets, which is a budget control rather than a vendor limit, and no
per-day figure appears. The API rate limit that circulates in third-party trackers
is `reported` and was not found on a first-party page.

**The other fields.** A recipient counts as a send. A sending domain is required.
The pricing page states no credit card required.

Evidence: `docs.useplunk.com/concepts/billing` (read 2026-10-22);
`dossier/email/plunk-hosted.json`.

Verdict: `qualifies-with-caveat`.

## MailerSend

500 emails a month with 1 domain, 100 daily API requests and 1 template
(`documented`, 2026-10-22). The pricing page leads with a "14 days free to
integrate" banner above a permanent free plan that is much smaller.

⚠ **The 100 is a request cap and not an email cap.** The page's table row is "Daily
API requests | 500,000 | 100,000 | 1,000 | 100", and the FAQ restates it as "100
daily requests". One request may carry many recipients, so 100 requests a day is not
100 emails a day and the email ceiling is the 500 a month.

⚠ **A card is required for the free plan.** The page answers "Why do you need my
credit card details for the Free plan?" with "we just ask that you provide this
information to prevent abuse of the platform", meaning the card is the check on excess use. That is `card` on the identity
vocabulary and it is the gate that puts this row below the others.

500 a month is a fifth of Resend's and a sixtieth of Brevo's.

Evidence: `mailersend.com/pricing` (read 2026-10-22); the submission endpoint
`smtp.mailersend.net:587` answered 250 with STARTTLS and `AUTH LOGIN` 334 and
advertised no `SIZE` extension (`measured`, 2026-10-22);
`dossier/email/mailersend.json`.

Verdict: `fails-quota`.

## Postmark

100 emails a month on the free Developer tier, which does not expire
(`documented`, 2026-10-22). There is no daily allowance beyond it, so 100 is the
ceiling for the whole month.

That is a different shape from every other product here and it is why Postmark is
in the fails column: no burst room at all. A reader who plans on 100 a day and
meets a monthly ceiling of 100 loses the month.

**The other fields.** 100 a month is 3.3 a day averaged. A verified sender signature
or domain is required. No card is required.

Evidence: `postmark.com/pricing` (read 2026-10-22); the submission endpoint
`smtp.postmarkapp.com:587` answered 250 with STARTTLS and `AUTH LOGIN` 334
(`measured`, 2026-10-22); `dossier/email/postmark.json`.

Verdict: `fails-quota`.

## Plunk (self-hosted)

AGPL-3.0, with no limit from the software and SES or another relay behind it
(`documented`, 2026-10-22). The relay bill and the deliverability belong to whoever
runs the relay, so this is the front half of a paid chain rather than a free sender.

**No field in the table applies to software.** The daily cap, the per-recipient cap,
the domain requirement and the card requirement are all properties of whichever
relay sits behind it. The record carries `qualifies-with-caveat` rather than
`qualifies` because the claim is that the software imposes no limit, which is a
claim about absent code and was not measured.

Evidence: `docs.useplunk.com/concepts/billing` (read 2026-10-22);
`dossier/email/plunk-selfhost.json`.

Verdict: `qualifies-with-caveat` as software. The mail it sends is not free.

## What did not work

- **SendGrid**: the free plan was retired on 2025-05-27 and accounts were paused
  after a 60-day window. `dead`. The retirement is documented in Twilio's changelog.
- **Postmark**: 100 a month with no daily room. `fails-quota`.
- **MailerSend**: 500 a month and a card on the free plan. `fails-quota`.
- **Mandrill**: 500 sends in total to one verified domain, not a monthly
  allowance. `trial-only`.
- **MailerLite**: 2,500 a month with 250 subscribers, but the free plan cannot send
  over the API at all. That is a reachability limit of the tier, not a missing
  wrapper: the paid plan reaches the same API. `qualifies-with-caveat` at the paid
  tier, `fails-egress` while free.
- **Amazon SES's 62,000 a month**: withdrawn in August 2023. Every page citing it
  describes a tier that no longer exists.
- **A free bulk sender with no card**: AWS, Scaleway and OVH all require a payment
  method at some point in onboarding, and MailerSend requires one on the free plan
  itself.

## Chaining

**Rotating providers to escape the daily cap.** `Brevo 300 + Mailjet 200 + Resend
100 + SMTP2GO 200 + Mailgun 100 = 900 a day` across five providers on one verified
domain. The arithmetic works and the scarce link is domain reputation, not
capacity: five providers sending for one new domain will individually and
collectively hit spam filtering long before 900 a day is useful, and Resend's 4%
bounce rule pauses the account first.

A self-hosted front in front of a paid relay, the last resort: `Plunk self-host ->
Amazon SES at USD 0.10 per 1,000`. Real volume comes from the paid relay, SES; the
self-hosted front comes after every hosted offer. See
[`../paid/bulk-sending.md`](../paid/bulk-sending.md).
