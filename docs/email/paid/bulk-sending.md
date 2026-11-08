# What does a thousand messages cost when free is not enough?

The free senders cap at 300 a day and the volume a real notification workload needs
is larger. This is the cheapest paid ladder, priced per thousand messages so the
tiers are comparable, and the answer is that the floor is **USD 0.10 per 1,000**
at Amazon SES and every other option is two to ten times that.

The catch is not the price. It is that Amazon SES starts every new account in a
sandbox that can only mail verified identities, and the exit is a support request
with no published decision time.

Sorted by marginal cost per thousand messages.

| provider | rate | 1,000 messages | what binds | identity |
| --- | --- | --- | --- | --- |
| Amazon SES | USD 0.10/1,000 | USD 0.10 | `write-gated`: the sandbox | card |
| Scaleway Transactional Email | EUR 0.25/1,000 | EUR 0.25 | `write-gated`: support-set initial limits | email + card |
| Cloudflare Email Sending | USD 0.35/1,000 | USD 0.35 | `write-gated`: the Workers Paid plan | card |
| Mailchimp Transactional | USD 0.80/1,000 | USD 0.80 | `write-gated`: a verified domain | card |

The arithmetic, so a reader can check it: 1,000,000 messages a month at USD
0.10/1,000 is USD 100. At USD 0.35/1,000 it is USD 350. At USD 0.80/1,000 it is USD
800. The spread between the first and the last is the range a buyer chooses within.

## Amazon SES

USD 0.10 per 1,000 messages, which is the cheapest real bulk rate found
(`documented`, 2026-10-22). The free tier is separate and finite: 3,000 message
charges a month for the first 12 months, or USD 200 of general AWS credits over six
months for accounts created after 2025-07-15.

Every new account starts in the sandbox, where it can only send to verified
identities and there are unstated daily and per-second caps. Leaving requires a
Sending Limit Increase request through the support centre.

The 62,000 messages a month figure that still circulates widely was withdrawn in
August 2023.

Evidence: `aws.amazon.com/ses/faqs/` and `aws.amazon.com/ses/pricing/` (read
2026-10-22); `dossier/email/amazon-ses.json`.

Verdict: `qualifies-with-caveat`. The sandbox is the gate, not the price.

## Scaleway Transactional Email

EUR 0.25 per 1,000 after 300 a month for the free tier and 10,000 as the service
default (`documented`, 2026-10-22). Quotas can be raised after the payment method
and identity are validated.

⚠ **A new organisation gets neither published figure.** The capabilities page states
that new accounts face stricter initial limits set by support with no number
published. So 300 is a ceiling on the free tier and not a plan: a reader who
provisions for 300 may meet a lower limit first, and its size is `unverified`
because Scaleway does not publish it. The two published figures disagree and the
disagreement is recorded rather than resolved. See
[`../free/senders.md`](../free/senders.md).

Evidence: `scaleway.com/en/pricing/managed-services/` and
`scaleway.com/en/docs/transactional-email/reference-content/tem-capabilities-and-limits/`
(read 2026-10-22); `dossier/email/scaleway-tem.json`.

Verdict: `qualifies-with-caveat`. The unpublished initial limit is what a new
account meets.

## Cloudflare Email Sending

3,000 emails a month are included on the Workers Paid plan at USD 5 a month, then
USD 0.35 per 1,000 (`documented`, 2026-10-22). Arbitrary recipients require the
paid plan; sending to the account's own verified destination addresses is free on
every plan, including Workers Free.

The plan fee is part of the price and it is why the marginal rate is not comparable
to SES at low volume: 3,000 messages on Workers Paid is USD 5, which is USD 1.67 per
1,000 with the plan included.

Sends to verified destinations do not count against the quota, which is a genuine
free channel for notifying yourself and not a sender.

Evidence: `developers.cloudflare.com/email-service/platform/pricing/` (read
2026-10-22); `dossier/email/cloudflare-email-sending.json`.

Verdict: `paid-only`.

## Mailchimp Transactional (Mandrill)

USD 20 per block of 25,000 messages, which is USD 0.80 per 1,000
(`documented`, 2026-10-22). Blocks drop to USD 18 at 21 to 40 blocks.

The free offer is 500 sends in total to a verified domain, which is a
demonstration rather than an allowance and is recorded as `trial-only`.

Evidence: `mailchimp.com/pricing/transactional-email/` (read 2026-10-22);
`dossier/email/mandrill.json`.

Verdict: `trial-only` on the free tier and the most expensive paid tier here.

## What did not work

- **The 62,000 messages a month SES figure**: withdrawn in August 2023. Every page
  citing it describes a tier that does not exist.
- **Free bulk outbound without a card**: AWS, Scaleway and OVH all require a payment
  method at some point in onboarding.
- **The free tiers as a bulk channel**: 300 a day at the best of them, which is 9,000
  a month.
- **Mailchimp's demonstration block as a free tier**: 500 sends in total.
- **Cloudflare Email Sending on Workers Free**: arbitrary recipients are paid-only.
- **Yandex 360 with a custom domain**: a business-plan feature.

## Chaining

The chain that reaches real volume has a paid relay: `Amazon SES at USD
0.10/1,000`. Its front, `Plunk self-host or Postal`, is self-hosted software, the
last resort after every hosted offer. The scarce link is SES's sandbox exit, which
is one support request per account, and the second is reputation: a self-hosted
front sending for a new domain meets the same filtering as a hosted sender.

**The cheap Cloudflare chain.** `Cloudflare Email Routing for unlimited inbound ->
Cloudflare Email Sending on Workers Paid at USD 5 a month for 3,000 out`. The
scarce link is the 3,000 and the plan fee, and the chain is worth it only for the
inbound half.
