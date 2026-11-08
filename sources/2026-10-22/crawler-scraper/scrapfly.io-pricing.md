# Scrapfly Pricing

> Machine-readable pricing for AI agents. The canonical, human-readable version lives at https://scrapfly.io/pricing, that page is authoritative if anything below diverges. Currency: USD. Billing: monthly, usage-based.

## What you pay for

Scrapfly bills in **API credits**. One API key gives you access to every product on the same credit balance:

- **Web Scraping API**, managed proxies + Unblocker (formerly ASP)
- **Cloud Browser**, remote Chromium pool driven by Playwright / Puppeteer / CDP
- **Screenshot API**, full-page, element, and viewport screenshots
- **Extraction API**, LLM-driven structured extraction (prompt + JSON schema)
- **Crawler API**, site-wide traversal with policy and budget controls

Credit cost per request depends on the features you enable (JavaScript rendering, Unblocker, residential proxies, country targeting, etc.). Estimator at https://scrapfly.io/pricing#estimator.

## Free tier

- **1,000 API credits** on signup
- No credit card required
- Discovery, hobby, and evaluation use cases

## Plans

| Plan       |       Monthly base | Included credits | Extra credits (per 10k) | Concurrency | Overflow      |
| :--------- | -----------------: | ---------------: | ----------------------: | ----------: | :------------ |
| Free       |                 $0 |            1,000 |             not allowed |           5 | quota cap     |
| Discovery  |                $30 |          200,000 |                   $5.00 |           5 | quota cap     |
| Pro        |               $100 |        1,000,000 |                   $3.50 |          20 | pay-as-you-go |
| Startup    |               $250 |        2,500,000 |                   $2.00 |          50 | pay-as-you-go |
| Enterprise |               $500 |        5,500,000 |                   $1.20 |         100 | pay-as-you-go |
| Custom     | $1,200 to $30,000+ |       negotiated |              negotiated |  negotiated | pay-as-you-go |

**Overflow behavior:** Pro and above switch to pay-as-you-go when included credits are consumed — your integration never stalls. Discovery and Free hard-cap at quota for predictable bills.

## Plan limits (resource caps)

| Resource              | Discovery | Pro | Startup | Enterprise |
| :-------------------- | --------: | ---: | ------: | ---------: |
| Projects              |         2 |   5 |      15 |         50 |
| Schedules             |         5 | 100 |     200 |        500 |
| Proxy pools           |         5 |  10 |      50 |        100 |
| Webhooks              |         5 |  10 |      20 |         50 |
| Extraction templates  |        10 |  15 |      50 |        100 |
| Datastores            |         5 |   5 |      10 |         50 |
| Log retention (weeks) |         1 |   2 |       3 |          4 |

## Discounts

- **Annual billing:** 2 months free (16% off) when paid annually
- **Custom contracts:** committed-volume pricing from $1,200/mo upward, negotiated per use case

## SLA & support

- **All plans:** community support via docs and email
- **Pro+:** priority email support
- **Custom:** dedicated technical contact, custom integration work
- We do **not** publish a contractual uptime or response-time SLA. Custom contracts include MSA, DPA, BAA, and HIPAA on request.

## Compliance & legal

- SOC 2 Type II
- ISO/IEC 27001
- HIPAA, BAA available on Custom plans
- GDPR, DPA available for all paid plans
- See https://trust.scrapfly.io for the full report library

## Buy / start

- **Self-serve signup:** https://scrapfly.io/register (free credits, no card)
- **Plan selector:** https://scrapfly.io/pricing
- **Sales (Custom tier):** https://scrapfly.io/contact
- **Billing changes:** dashboard → Account → Subscription
- **Pay-as-you-go invoicing:** monthly, on the 1st of the following month

## API endpoints relevant to billing

- `GET https://api.scrapfly.io/account`, current plan, included credits, used credits, extra rate, concurrency
- `GET https://api.scrapfly.io/scrape?cost=true&...`, cost estimation for a given scrape configuration without executing it

## Resources

- HTML pricing page: https://scrapfly.io/pricing
- Cost estimator (interactive): https://scrapfly.io/pricing#estimator
- Error catalog: https://scrapfly.io/api_errors.json
- Docs: https://scrapfly.io/docs
- Status: https://scrapfly.statuspage.io/

_Generated from live plan data. Always reconcile against https://scrapfly.io/pricing before purchase decisions._
