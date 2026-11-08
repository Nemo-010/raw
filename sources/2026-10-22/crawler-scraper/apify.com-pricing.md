# Apify Pricing

Flexible plans with pay-as-you-go usage on top of the monthly fee. See [apify.com/pricing](https://apify.com/pricing) for the full interactive pricing page.

This page is the pricing reference. How an agent connects to Apify, authenticates, and pays, including with no account and nobody to sign in, is in the agent quickstart at [apify.com/agents.md](https://apify.com/agents.md).

## Plans

Save 10% on paid plans when billed annually.

| Plan     | Monthly price | Annual price / month | Included usage / month | Apify Store discount        | Support               |
| -------- | ------------- | -------------------- | ---------------------- | --------------------------- | --------------------- |
| Free     | $0            | $0                   | $5                     | No Apify Store discount     | Community support     |
| Starter  | $19           | $17                  | $19                    | Bronze Apify Store discount | Chat support          |
| Scale    | $199          | $179                 | $199                   | Silver Apify Store discount | Priority chat support |
| Business | $999          | $899                 | $999                   | Gold Apify Store discount   | Account manager       |

Building and publishing your own Actors? The Creator plan costs $1 / month and comes with a one-time $500 of platform usage for the first 6 months, but limits Apify Store to universal Actors. See [apify.com/pricing/creator-plan.md](https://apify.com/pricing/creator-plan.md).

## Actor runs

Most Actors in Apify Store use pay-per-event pricing, listed on each Actor's page. Pay-per-usage Actors and your own Actors bill platform usage instead, and some pay-per-event Actors charge both. Compute is measured in compute units (CUs). 1 CU = 1 GB of RAM running for 1 hour.

| Plan     | CU price   | Max RAM | Max concurrent runs |
| -------- | ---------- | ------- | ------------------- |
| Free     | $0.2 / CU  | 16 GB   | 5                   |
| Starter  | $0.2 / CU  | 64 GB   | 32                  |
| Scale    | $0.16 / CU | 256 GB  | 128                 |
| Business | $0.13 / CU | 512 GB  | 256                 |

## Proxy

| Plan     | Residential proxy | Datacenter proxy                 | SERPs proxy        | Unblocker              |
| -------- | ----------------- | -------------------------------- | ------------------ | ---------------------- |
| Free     | $8 / GB           | 5 IPs included                   | $2.5 / 1,000 SERPs | $1.5 / 1,000 requests  |
| Starter  | $8 / GB           | 30 IPs included, then $1 / IP    | $2.5 / 1,000 SERPs | $1.5 / 1,000 requests  |
| Scale    | $7.5 / GB         | 200 IPs included, then $0.8 / IP | $2 / 1,000 SERPs   | $1.25 / 1,000 requests |
| Business | $7 / GB           | 500 IPs included, then $0.6 / IP | $1.7 / 1,000 SERPs | $1 / 1,000 requests    |

For a full cost breakdown including storage, data transfer, and detailed Actor pricing, see [apify.com/pricing#PricingDetailsSection](https://apify.com/pricing#PricingDetailsSection).

## Enterprise

Need a custom plan?

- Custom scraping solutions
- Scalable pricing
- SLAs with guaranteed data
- Dedicated team of experts

[Talk to us](https://apify.com/contact-sales)

## Add-ons

| Add-on            | Description                                                                                                                  | Price          |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------- |
| Concurrent runs   | Allows multiple instances of an Actor to run simultaneously, enabling faster task processing and efficient resource use.     | $5 / run       |
| Actor RAM         | The memory allocated to an Actor while it runs. More memory lets an Actor process more data and run faster.                  | $1 / GB        |
| Datacenter proxy  | Fast, cost-effective non-residential IPs from data centers, ideal for scraping less-protected websites and automation tasks. | from $0.6 / IP |
| Personal training | Personal training support or guidance to help you use the platform, optimize Actors, and achieve specific goals.             | $150 / hour    |

## Frequently asked questions

### What is the prepaid platform usage, and how much do I need?

The Apify platform has a number of services that are charged based on usages, such as Actors, proxies, data transfer, and storage. See [pricing](/pricing) for the full list of platform services.

Each subscription plan comes with a certain amount of prepaid platform usage that is used to pay for services. If your platform usage in a given billing cycle exceeds this prepaid amount, the excess usage will be added to your next invoice, and you'll get a notification. If you're on the free plan, your access to Apify's services will be blocked until the beginning of the next monthly cycle.

**Note that unused usage credits are not rolled over to the next billing cycle, and they expire at the end of the billing cycle.**

### Can I try Apify for free?

Absolutely! We offer a [free plan](/pricing) that lets you use most of the features of the Apify platform, but with certain limits. No credit card is required. The free plan includes Apify Proxy, which is limited to use within the platform and does not extend to external clients.

If you'd like a free demo of Apify's custom solutions, please [contact us](/contact-sales/demo).

### Which plan should I choose?

If you're unsure which plan is right for you, just pick the lowest-priced plan that has all the features you need. If you exceed the prepaid platform usage, you'll get a notification, and the excess usage will be added to the next invoice (see below for details).

You can upgrade to a higher plan at any time in your [Billing](https://console.apify.com/billing) settings, and you'll only pay for the price difference.

### What is the pricing for Actors in Apify Store?

Every Actor in Apify Store uses one of two pricing models, and each Actor's page states which one applies to it.

**Pay per event** - you pay a fixed price for the events the Actor's developer defines, such as starting the Actor or returning a single result. Most pay-per-event Actors include the Apify platform usage in the event price, but some charge for it separately, so check the pricing section on the Actor's page.

**Pay per usage** - the developer charges nothing on top, and you only pay for the platform usage consumed by the Actor's runs: compute units, data transfer, storage operations, and residential or SERP proxies.

Both models draw on the platform usage credits included in your plan, and excess usage is charged to your next invoice. Reading from or writing to a run's dataset after the run finishes also counts as platform usage.

The exact platform usage depends on the specific Actor, the type of job it performs, how often it runs, and for how long. The easiest way to find out the platform usage of an Actor is to perform a test run. You can then review your platform usage in your [Billing](https://console.apify.com/billing) settings and figure out the best subscription plan for your needs.

For a full breakdown of both models, see [Actors in Apify Store](https://docs.apify.com/actors/running/actors-in-store.md). If you need advice, please [contact us](/contact-sales).

### Can an AI agent pay for Actor runs without an Apify account?

Yes. An autonomous agent with a crypto wallet can pay through the agentic payment protocols [x402](https://www.x402.org/) and [MPP](https://mpp.dev/), with no account and no human sign-up. The agent pays once at [agi.apify.com](https://agi.apify.com/), receives a temporary Apify API token with a fixed spend cap, and calls the Apify API with it like any other token. Each Actor run is metered against that prepaid balance, and unused balance expires with the token.

Agents find the complete, current instructions, including supported chains, terms, and balance checks, at [agi.apify.com/AGENTS.md](https://agi.apify.com/AGENTS.md).

### Can I upgrade, downgrade or cancel my plan?

You can upgrade, downgrade, or cancel your plan at any time in your [Billing](https://console.apify.com/billing) settings.

When you upgrade, your payment will be prorated, so you will only pay for the difference between the old and the new price, taking into account how much of the billing cycle has already passed.

When you downgrade, there's no proration except for the unused platform usage that's rolled over to the new plan.

If you decide to cancel, your subscription will last until the end of the current billing cycle. It won't be renewed after that. Note that you might still be charged for excess platform usage.

### What drives the cost of an Actor run?

Most Actors in Apify Store use pay-per-event pricing. You pay the prices listed on the Actor's page for events such as returning a result. Pay-per-usage Actors and your own Actors bill platform usage instead, including compute units, storage, proxies, and data transfer. Some pay-per-event Actors charge both. You can check your daily [usage chart](https://console.apify.com/billing) on the Apify platform.

### What happens after I run out of prepaid usage?

If you're a paying user, you can continue using the platform and will be charged for overage until you reach the usage limit configured in the billing. If you're on the free plan, you'll be blocked until the next billing cycle.

### What happens to my prepaid usage if I don't use all of it?

If you don't consume all your prepaid usage, it disappears at the end of the billing cycle. Go to our [pricing](/pricing) page to learn more about the prepaid usage of all Apify's subscription plans.

### Why do some of my Actor runs cost more than others?

On a pay-per-event Actor, a run costs more when it returns more results or triggers more events. When you pay for platform usage, the cost depends on proxies, data transfers, memory, and run duration. It also depends on the number of retries when a request fails.

### How does Apify pay as you go work?

If you're on one of Apify's paid plans, you can continue using the platform after reaching the limit by paying the rest as overage. That means you don't have to change your pricing plan to exceed the usage limit of your current plan.

### Does Apify offer any discounts for universities or nonprofit organizations?

Apify offers discounts on its paid plans to both academic institutions and nonprofit organizations. Students are eligible for 30% off Starter and Scale plans, while nonprofits can get a personalized discount. Learn more at [Apify for universities](/resources/universities) and [Apify for nonprofits](/resources/nonprofits).

### Do startups get the same pricing as enterprise customers?

Apify believes in encouraging startups to grow by using online data at scale. So we're giving a special 30% discount on our Scale plan to startups. Learn more at [Apify for startups](/resources/startups).

### I would like to develop Actors. What should I do?

[Apify Academy](https://docs.apify.com/academy.md) is a free course that shows you how to start developing Actors on the Apify platform. You can also find more information in the [Apify documentation](https://docs.apify.com).
