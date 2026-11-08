# Eleven verdicts moved, and the card gate is now recorded as a gate

- **When:** 2026-10-24T02:50:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/` records for `fly-io`, `fly-machines`, `koyeb`, `modal`, `northflank`, `alwaysdata`, `blinkenshell`, `tilde-team`, `render`, `baseten`, `heroku`, `clever-cloud`, `sevalla`, `isorun`, `withruntime`, `shellbox`, `conhost`, and the regional rows `iwinv`, `utho`, `webarena-indigo`, `xserver-vps`, `conoha-vps`, `locaweb-vps`; and the sentences in `docs/compute/free/README.md` and `docs/compute/README.md` that quoted the old ones
- **Superseded by:** each vendor's own page, read on 2026-10-24. The decisive sentence for each row is in that record's `evidence[]` with the date, and the working reports are at `.tmp/compute-2026-10-24/lanes/`
- **Evidence:** `dossier/compute/<slug>.json` `evidence[]` for every row named below, each carrying the URL and the date 2026-10-24; the lane reports at `.tmp/compute-2026-10-24/lanes/L04-free-nocard/report.md`, `L05-credit-audit/report.md`, `L07-paas/report.md`, `L08-regional/report.md` and `L19-q3-redteam/report.md`
- **Confidence:** documented

## The moves, and what took each one away

| record | was | is | the sentence that decided it |
| --- | --- | --- | --- |
| `fly-io` | `dead` | `trial-only` | "New organizations don't have a free tier or a monthly free usage allowance. A trial runs up to 2 hours of Machine runtime or 7 days." The free tier is withdrawn; the product is alive |
| `fly-machines` | `dead` | `trial-only` | the same sentence, on the same product. Two records for one product must not disagree |
| `koyeb` | `qualifies-with-caveat` | `fails-identity` | "We require a credit card ... We verify the card you enter by placing a $29 pre-authorization hold", and the Pro plan is charged pro rata |
| `modal` | `qualifies-with-caveat` | `fails-identity` | "you must have a payment method on file in order to use Modal". The USD 30 a month is real and sits behind the card |
| `northflank` | `qualifies` | `fails-identity` | "all users must add a payment method to start creating resources on Northflank, regardless of plan selection" — against the plan card's "No card needed", on the same site |
| `alwaysdata` | `qualifies-with-caveat` | `fails-quota` | the free plan's footnote: "it cannot be used to run services". A listener is out of scope whatever the disk says |
| `blinkenshell` | `qualifies-with-caveat` | `fails-identity` | step five of five: "Enter your personal cell/mobile phone number to receive an SMS with a verification code", after a 20-question quiz and two human vouches |
| `tilde-team` | `qualifies-with-caveat` | `dead` | "tilde.team got hacked. Someone was able to gain a root shell and ran `rm -rf /`", and "*ssh access is currently disabled in the meantime*" |
| `render` | `fails-quota` | `qualifies-with-caveat` | the 750 free instance hours are real and the 15-minute spin-down is the constraint; `fails-quota` read as "the hours are too few", which is not what the page says |
| `baseten` | `qualifies-with-caveat` | `paid-only` | the resources page publishes no free tier and no rate |
| `heroku` | `fails-identity` | `paid-only` | there is no free dyno at any identity level, so the gate is the price and not the account |
| `clever-cloud`, `sevalla` | `qualifies-with-caveat` | `paid-only` | no free row on either pricing page; Sevalla's is a trial, not a tier |
| `isorun`, `shellbox` | `qualifies-with-caveat` | `paid-only` | no free tier on the page; the earlier verdict came from an aggregator card |
| `withruntime` | `trial-only` | `qualifies-with-caveat` | the free allowance is real and the 730-hour figure is USD 6.39, not the USD 1.49 the aggregator's 200-hour model produces |
| `iwinv` | `paid-only` | `fails-identity` | South Korean nationality and a Korean mobile are required, and card registration needs a Korean public certificate |
| `locaweb-vps` | `paid-only` | `fails-identity` | CPF, RG, address and date of birth are collected at purchase |
| `utho` | `trial-only` | `paid-only` | no trial on the page; the entry plan is INR 1,435 |
| `webarena-indigo`, `conoha-vps` | `paid-only`, `trial-only` | `qualifies` | both sell a machine under USD 5 with no card gate; the earlier verdicts were unread rows |
| `xserver-vps` | `dead` | `paid-only` | the product sells; the free tier is what ended |

## Why this is one entry and not twenty

Every move has the same shape: **a verdict was written from an aggregator card, a pricing
page's headline, or a signup form, and the sentence that decides usability was on a different
page.** Koyeb is the clearest: the free instance is byte-identical across the year and the
thing that changed is a USD 29 hold that appears only in the FAQ. Northflank is the worst:
the contradiction is inside one page, a badge at the top and a billing sentence further down.

⛔ **The rule this pass adds to the topic: read the billing page, not the pricing page, and
read the status page, not the product page.** Six of the eleven moves are a card requirement
that a pricing page omitted, and one is a platform that is down while its marketing page still
sells the free tier.

## The two reversals worth naming separately

**Lightning AI stays `dead`, and a lane tried to revive it.** A lane re-read
`lightning.ai/pricing` on 2026-10-24, found "Run 1 Studio free 24/7. No credit card." still
printed, and reversed the verdict to `qualifies`. The incident page read the same hour states
"This is an active investigation and during this time the Platform will remain inaccessible to
all users", and the status banner still reads "Service is down to address a security incident"
with its newest update on 2026-10-19. The record keeps `dead` and now carries both pages, so
the contradiction is visible rather than resolved by preference.

**NATKVM's headline moved from USD 0.46 to USD 0.42 a month, and the correction is a floor
rather than a price.** An adversarial pass found `NL 256MB NAT` at USD 4.99 a year on the same
store, below the USD 5.50 LXC rung the first pass priced, with the same 20 forwarded ports,
UDP and TCP, TUN/TAP and one IPv6. Both cards read "Starting from" and both product pages
redirect to the cart, so USD 4.99 is the vendor's stated annual floor and not an invoiced
price. The record says so.

## What is still open

The two answers rest on vendors that publish no renewal price: GreenCloudVPS, NATKVM,
Cheap-Host, CloudCone, RackNerd and ServerHost. None carries a strike-through or a promo badge
either, which is why they are recorded as list rates rather than promotions, but a renewal
figure would settle it and none of the six publishes one. Only AlphaVPS does, and it states the
annual discount is locked for the life of the service.
