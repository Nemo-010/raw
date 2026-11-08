# ZenRows' per-1,000 price was the annual-billed rate quoted as the monthly price, and every per-1,000 figure in the paid lane was 15.9% low

- **When:** 2026-10-22T04:23:24Z
- **Status:** corrected
- **Supersedes:** `docs/crawler-scraper/paid/unblockers-proxies.md` §The comparison and §ZenRows; `docs/crawler-scraper/paid/crawl-apis.md` §The comparison and §ZenRows; `docs/crawler-scraper/paid/reader-extractors.md` §The comparison and §ZenRows; `dossier/crawler-scraper/zenrows.json` `limits[]` and `evidence[]`
- **Superseded by:** the same four files, which now quote USD 69 and USD 19 on monthly billing and carry the annual rate as the discount
- **Evidence:** `zenrows.com/pricing` structured data, read through the broker on 2026-10-22T03:56Z and captured at `sources/2026-10-22/crawler-scraper/zenrows.com-pricing.md`
- **Confidence:** measured

## What we believed

The paid lane's headline was **"ZenRows at USD 0.23 per 1,000 plain pages on Launch is the
cheapest in the class"**, derived from USD 58 a month for 250,000 credits. Build was
USD 16 for 45,000 at USD 0.36. Every rendered, proxied and fully-defended figure in three
documents multiplied one of those two numbers.

## What we found

USD 58 and USD 16 are the **annual monthly rate**, not the monthly price. The vendor
page's own structured data says it, verbatim:

> "The price is the annual monthly rate of the entry rung (pay for 10 months, get 12).
> Annual monthly rates run $16 to $33; monthly billing of the same rungs is $19 to $39."

and for Launch:

> "Annual monthly rates run $58 to $108; monthly billing of the same rungs is $69 to $129."

So the month-to-month prices are **USD 19 and USD 69**, and the per-1,000 figures are:

| plan | annual, as quoted | monthly, the price | error |
| --- | --- | --- | --- |
| Launch, 250,000 credits | USD 58 = USD 0.232 per 1,000 | USD 69 = USD 0.276 per 1,000 | 15.9% low |
| Build, 45,000 credits | USD 16 = USD 0.356 per 1,000 | USD 19 = USD 0.422 per 1,000 | 15.9% low |

Every derived figure moved with it: a rendered page at 5 credits is USD 1.38 not
USD 1.16, a premium proxy at 10 credits USD 2.76 not USD 2.32, and both at 25 credits
USD 6.90 not USD 5.75.

The verdict survives. ZenRows is still the cheapest plain page in the class against
ScrapingAnt's USD 1.90 and ScraperAPI's by-plan pricing. **The number was wrong and the
conclusion was right**, which is the shape that survives a review nobody runs.

The 15.9% is the annual rate's discount against the monthly one: 58/69. The error is
not uniform in the other direction, because the monthly rate is 19.0% above the annual
one, and a document that quotes either without the basis can be checked against neither.

Firecrawl carried the same defect on the same day and in the same three documents: its
Hobby tier is "USD 19/month billed monthly, or USD 16/month billed annually", and the
card above Standard is headed "Prices shown are per month, billed annually". Hobby moved
from USD 3.20 to USD 3.80 per 1,000, which is the same 15.8% discount.

## How we found it

An adversarial review read the vendor page rather than the document, found two rates for
one plan, and recomputed every derived figure. The same review noticed that no paid
document in the topic stated a billing period anywhere, which is the defect that let the
wrong rate pass as the price.

## What it cost us

Three paid documents, two dossier records and every per-1,000 figure in the class. The
error is in the flattering direction: it makes the cheapest plan look 15.9% cheaper than it
is, which is exactly the direction a reader does not check.

## What a future session should do differently

⛔ **A price without its billing term is not a price**, and the conventions already say a
price carries its conditions. Write the term into the `Plan` column, not into a footnote:
`Launch, USD 69 a month, monthly billing`. Where a vendor publishes two rates, record both
and derive from the one the decision is made on.

⚠ **Read the page's structured data, not its headline.** The two rates were in the page
as `AggregateOffer` objects with `lowPrice` and `highPrice` per rung; the human-readable
card showed one number. A reader who greps for `USD` finds the annual figure first,
because it is the one the page is built to lead with.

⭐ **The check is one question: what do I pay in month one?** If the answer needs a
twelve-month commitment, the per-unit figure is a discount and it belongs in a sentence
that says so.
