# Which TLD is cheapest, once the renewal is counted?

The cheapest first year and the cheapest second year are different TLDs, and neither is the one
the promo pages lead with. The answer over a five-year horizon is `.com` or `.org` at at-cost, and
the answer for one year only is `.online` at USD 0.98.

## The comparison

Sorted by the three-year total, which is the shortest horizon that exposes a promo.

| TLD | cheapest first year | renewal | three-year total |
| --- | --- | --- | --- |
| `.com` at Spaceship | USD 8.88 | USD 9.98 | USD 28.84 |
| `.com` at Cloudflare | USD 10.46 | USD 10.46 | USD 31.38 |
| `.org` at Spaceship | USD 6.65 | USD 11.39 | USD 29.43 |
| `.org` at Cloudflare | USD 8.50 | USD 11.20 | USD 30.90 |
| `.io` at Cloudflare | USD 32.00 | USD 50.00 | USD 132.00 |
| `.online` at Spaceship | USD 0.98 | USD 15.08 | USD 31.14 |
| `.online` at Cloudflare | USD 4.99 | USD 27.70 | USD 60.39 |
| `.xyz` at Spaceship | USD 1.86 | USD 13.77 | USD 29.40 |
| `.xyz` at Porkbun | USD 2.04 | USD 14.21 | USD 30.46 |
| `.ai` at Spaceship | not stated | USD 79.98 | above USD 160 |

## The arithmetic, worked through

A reader can check each row in ten seconds.

- `.com` at Spaceship: 8.88 + 9.98 + 9.98 = **28.84**.
- `.com` at Cloudflare: 10.46 x 3 = **31.38**.
- `.org` at Spaceship: 6.65 + 11.39 + 11.39 = **29.43**.
- `.org` at Cloudflare: 8.50 + 11.20 + 11.20 = **30.90**.
- `.online` at Spaceship: 0.98 + 15.08 + 15.08 = **31.14**.
- `.xyz` at Spaceship: 1.86 + 13.77 + 13.77 = **29.40**.

⭐ **The spread is USD 2.54, and the set it holds over is four rows, not the table.** Across
`.com`, `.org` and `.xyz` at a good registrar, and `.online` at Spaceship, the three-year totals run
from **28.84 to 31.38**, a spread of **USD 2.54** or 8.8% of the cheapest. Inside that set the TLD
choice is nearly irrelevant once the renewal is counted, and the first-year promos are nearly all of
the apparent difference.

⛔ **Outside that set the claim inverts.** Two rows in the table above are in the same table and
not in the set: `.online` at Cloudflare at **USD 60.39**, and `.io` at Cloudflare at **USD 132.00**.
Against the cheapest row the `.io` spread is **USD 103.16, or 358%**. `.io` is the TLD a
developer-facing service would actually consider, and the "what did not work" list below calls it
four times a `.com`.

So the sentence to carry is: the TLD decision is trivial inside `.com`, `.org`, `.xyz` and a
Spaceship `.online`, and it is the whole cost outside them.

Over five years the same arithmetic changes the ranking. `.com` at Spaceship is 8.88 + 9.98 x 4 =
**48.80**. `.xyz` at Spaceship is 1.86 + 13.77 x 4 = **56.94**. The `.xyz` promo, which looks like
a third of a `.com` in year one, is 17% more expensive by year five.

## What a cheap TLD costs besides money

A `.xyz` or `.online` name is cheap and it carries a reputation cost, recorded here as a technical
note rather than a judgement: several free services reject or heavily rate-limit disposable TLD
signups, and Cloudflare Email Routing requires a zone under the holder's control either way. The
mechanism is that the TLD's spam reputation is a property of the TLD, not of the registrar.

That is a reliability note. It is not a reason to avoid a TLD and this document does not argue one.

## Cloudflare at cost

Cloudflare's model is the simplest to reason about **for a TLD whose registry fee is stable**:
registration, renewal and transfer are the same number, because that number is the registry fee plus
nothing. Its own page says prices are "always at or below what registries and ICANN charge us".

⚠ **At-cost pricing does not remove a registry promo, and four of the eight TLDs in this table
prove it.** `.com` and `.net` are flat, so for those two the sentence is exact. For the rest,
Cloudflare charges the registry's own promotional first year and then the registry's renewal:
`.org` USD 8.50 then USD 11.20, `.dev` USD 8.20 then USD 12.20, `.online` USD 4.99 then USD 27.70,
and `.xyz` USD 12.30 then USD 11.20, where the "renewal" is *cheaper* than the first year. "No
registrar markup" is not "no promo": the second is the registry's and survives at-cost pricing.

⭐ That is also the argument for a `.com`: it is the one TLD in the set where the registration and
the renewal are the same number at a registrar that takes no markup, so the three-year total can be
computed from one figure. The per-TLD figures come from a mirror of the at-cost table dated
2026-10-21, so the record is `reported` on the numbers and `documented` on the model.

`Evidence:` `cloudflare.com/products/registrar/` (read 2026-10-22) and `cfdomainpricing.com/` (read
2026-10-22, page dated 2026-10-21).

`Verdict:` the stable recommendation, and never the cheapest first year.

## Spaceship's two-year lead

Spaceship's `.com` is cheaper than Cloudflare's in the first year and the second, and the page
publishes both numbers on the same card. The `.org` row is the same shape: 6.65 then 11.39, which
beats Cloudflare's 8.50 then 11.20 over three years by USD 1.47.

`Evidence:` `spaceship.com/domains/` (read 2026-10-22): every TLD card carries the promo, the
renewal and the transfer.

`Verdict:` the cheapest `.com` and `.org` over three years of the registrars read here.

## What did not work

- **`$0.95 .xyz` as the cheapest option**: the first year is real and the renewal is 13.77 to
  14.21, so year two costs more than a `.com` at Cloudflare (`documented`, `spaceship.com/domains/`
  and `porkbun.com/tld/xyz`).
- **`.online` as a budget TLD**: 0.98 then 15.08 is a 15.4 times jump, and the three-year total is
  above a `.com` (`documented`, `spaceship.com/domains/`).
- **`.io` as a cheap developer TLD**: USD 50 renewal at Cloudflare and USD 51.75 at Spaceship, so a
  three-year `.io` is over four times a `.com` (`reported`: `cfdomainpricing.com/`, a third-party
  mirror dated 2026-10-21, and `spaceship.com/domains/`). Cloudflare publishes at-cost prices only
  in its dashboard, so no first-party page carries the USD 50.
- **`.ai` as a mainstream TLD**: USD 79.98 renewal, which is seven times a `.com`
  (`documented`, `spaceship.com/domains/`, which is first-party and prints the number).
- **A TLD choice as a cost decision**: the three-year spread across `.com`, `.org`, `.xyz` and a
  Spaceship `.online` is 9%, so the decision is reputation and availability rather than price
  (`inferred` from the arithmetic above).

## Chaining

**The cheapest complete endpoint over three years.** `Spaceship .com` at 28.84 for three years,
then `Cloudflare DNS` free, `Universal SSL` free and a `Tunnel` free. Total three-year cost is
**USD 28.84**, which is the number to compare against any paid endpoint.

**A one-year experiment.** `Spaceship .online` at 0.98 for the first year, abandoned before the
renewal. The scarce link is that abandonment is a real decision and the renewal is 15.4 times the
first year, so a name that turns out to matter costs a transfer.
