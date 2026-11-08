# Which registrar is cheapest in year two?

Three registrars publish a price for a `.com` and the cheapest first year is not the cheapest
second year. The answer is Spaceship at USD 8.88 then USD 9.98 for a `.com`, and Cloudflare at
cost where a promo is not worth tracking.

## The comparison

Sorted by the second-year price, because that is the one paid every year after.

| registrar | `.com` first year | `.com` renewal | model |
| --- | --- | --- | --- |
| Spaceship | USD 8.88 | USD 9.98 | promo, then a published renewal |
| Cloudflare Registrar | USD 10.46 | USD 10.46 | at cost, with no markup |
| Porkbun | USD 11.08 | not published separately on the index | promo, then a regular price |

## The rule that decides the price

⛔ **A first-year price is not a price.** A domain is a subscription and the number that matters is
the one that recurs. A registrar that sells USD 1 then USD 20 is more expensive over three years
than one that sells USD 10.46 flat, and the comparison literature quotes the first number.

Work the arithmetic. Three years on Spaceship `.com` is 8.88 + 9.98 + 9.98 = **USD 28.84**. Three
years on Cloudflare `.com` is 10.46 x 3 = **USD 31.38**. Spaceship wins by USD 2.54, and the win
is real rather than a promo artefact, because its renewal is also below at-cost.

Now the `.online` row. Spaceship sells it at USD 0.98 and renews at **USD 15.08**, which is 15.4
times the first year. Three years is 0.98 + 15.08 + 15.08 = **USD 31.14** against Cloudflare's
4.99 + 27.70 + 27.70 = **USD 60.39**. Cloudflare's `.online` registration is itself a promo, which
is why its own renewal is 5.6 times its registration.

## Cloudflare Registrar

Cloudflare sells at cost. Its own page states that registration, transfer and renewal prices "are
always at or below what registries and ICANN charge us" and that it "does not mark up domain
prices at all". The `.com` is **USD 10.46 in every year**, and the domain must use Cloudflare
nameservers.

The per-TLD figures are not on that page. They are in the dashboard and in a third-party mirror,
`cfdomainpricing.com`, which is headed "Updated 2026-10-21" and gives registration and renewal
side by side. That makes this record `reported` on the numbers and `documented` on the model.

From that table: `.com` 10.46 and 10.46; `.org` 8.50 then 11.20; `.net` 11.86 and 11.86; `.xyz`
12.30 then 11.20; `.dev` 8.20 then 12.20; `.online` 4.99 then 27.70; `.io` 32.00 then 50.00;
`.cc` 8.00 and 8.00.

`Evidence:` `cloudflare.com/products/registrar/` (read 2026-10-22): the at-cost model and the
no-markup sentence. `cfdomainpricing.com/` (read 2026-10-22, page dated 2026-10-21): the
per-TLD registration and renewal table.

`Verdict:` paid-only. The stable choice, and not the cheapest first year.

## Porkbun

Porkbun's index lists `.com` from **USD 11.08**, `.net` from USD 12.52 and `.org` from USD 7.98.
The per-TLD pages separate a sale price from a regular price: `.xyz` is **USD 2.04 first year and
USD 14.21 regular**, which is seven times the first year and more than a `.com` at Cloudflare.

`Evidence:` `porkbun.com/products/domains` (read 2026-10-22): the pricing index. `porkbun.com/tld/xyz`
(read 2026-10-22): "2.04 first year sale" beside "14.21 regular price".

`Verdict:` paid-only. `.org` is the one row worth taking, at USD 7.98 against Cloudflare's USD 8.50.

## Spaceship

⭐ Spaceship prints the promo and the renewal on the same card. `.com` **8.88 then 9.98**; `.net`
11.20 and 11.20; `.org` **6.65 then 11.39**; `.online` **0.98 then 15.08**; `.xyz` **1.86 then
13.77**; `.io` renews at 51.75; `.ai` renews at 79.98. A `.com` also carries a **USD 0.20 per year
ICANN fee**.

`Evidence:` `spaceship.com/domains/` (read 2026-10-22): each TLD card with the strikethrough promo,
the current price, the renewal and the transfer, plus the ICANN fee line.

`Verdict:` paid-only. The cheapest `.com` in both years of the three registrars here.

## What did not work

- **A USD 1 first year as a cheap domain**: every promo in this set renews above its first year,
  and the `.xyz` and `.online` rows renew at seven and fifteen times respectively (`documented`,
  `porkbun.com/tld/xyz` and `spaceship.com/domains/`).
- **Cloudflare as a free registrar**: it charges at cost, which is not zero, and it requires the
  domain on Cloudflare nameservers (`documented`, `cloudflare.com/products/registrar/`).
- **Porkbun's `.xyz` as a budget option**: 2.04 then 14.21 costs more over two years than a
  Cloudflare `.com` at 10.46 flat (`inferred` from two documented prices).
- **A registrar price without a date**: these are the most perishable numbers here and every one
  carries 2026-10-22 (`documented`).
- **A `.com` renewal below USD 8**: no row found, and the registry fee sets the floor
  (`inferred` from Cloudflare's at-cost claim).

## Chaining

**Registrar at cost plus free everything else.** `Cloudflare Registrar` for the domain, then free
DNS, free Universal SSL and a free tunnel on the same account. The scarce link is the USD 10.46,
and everything downstream of it is free.

**A cheap first year with a planned transfer.** `Spaceship` for the first year at 8.88 and a
transfer to Cloudflare later if the renewal moves. The scarce link is that a transfer is a billed
event and the arithmetic only works if the renewal actually rises.
