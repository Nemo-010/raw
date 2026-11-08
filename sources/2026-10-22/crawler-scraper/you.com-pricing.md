---
title: "Pricing"
language: "en_US"
description: "Transparent, per-call pricing for You.com APIs. Choose the level of intelligence your workload needs."
words: 810
upstream_status: 200
content_kind: page
extraction: body
source: extractor
title_source: meta
final_url: "https://you.com/pricing"
fetched_at: "2026-10-22T04:00:45.078Z"
---
**NEW** Knowledge for Web Search: live stock prices, crypto, weather, and prediction markets. Same $5/1K calls.

**NEW** Stocks, crypto, weather, and more now available in Web Search.

[Learn More →](https://you.com/resources/knowledge-parameter-web-search-api)

# Web Search APIs, priced per call

Choose the level of intelligence your workload needs.

How to buyWhat to buyUse casesFor EnterpriseFAQs

Start building now

Free

[View MCP config docs](https://you.com/docs/build-with-agents/mcp-server)

- No API key, no account, no credit card
- 100 Web Search API queries/day via MCP
- Sign up only when you need more

Production workloads

Pay as you go

Compare pricing

- No minimums, no seats, no platform fee
- All endpoints, SDKs and MCP
- Auto top-up so jobs never stall

Enterprise teams

Custom

[Talk to our humans](https://you.com/book-demo)

- Zero Data Retention, SOC 2, DPA-ready
- Custom QPS and dedicated capacity
- SLA-backed support

Powering web search for leading enterprises

## APIs and features

All built on the same real-time index. Pick based on how much you want to build yourself.

[Get an API key](https://docs.you.com/quickstart)

Web Search

Web Search APIContents API

Agentic Research

Answer APIResearch APIFinance Research API

### Web Search

You get the sources and do the reasoning.

Endpoint

Latency

Price

[Web Search API](https://you.com/docs/guides/search)

Free tier

Real-time web and news results, optimized for programmatic access in AI applications.

Web Search APIFree

Live search through the MCP server, no API key—up to 100 queries a day. Prototype or drop live search into an agent before committing.

Latency

p50 ~0.4s

Price

Free

Web Search APIStandard

Full endpoint access: Highlights, Knowledge, extraction, and domain filters. Built for production traffic at scale.

Latency

p50 ~0.4s

Price

$5

/1k calls

[Contents API](https://you.com/docs/guides/contents)

Give it URLs you already have, get back clean Markdown or HTML per page. Use it when you know which pages you want and just need them parsed, not searched.

Latency

1-10s per page

Price

$1

/1k Pages

### Agentic Research

We do the reasoning and hand back the answer.

Endpoint

Latency

Price

[Answer API](https://you.com/docs/guides/answer)

One call turns a question into a cited answer with the sources it used. Choose this over Web Search when you want the answer written for you, not a list of links to synthesize yourself.

Latency

p50 ~2.7s

Price

$5

/1k calls

[Research API](https://you.com/docs/guides/research)

Multi-step research on the open web. It plans, searches repeatedly, reads full pages, and cross-references before answering. One research_effort parameter tunes cost and depth across five levels:

ResearchLite

Simple factual lookups in a single pass. No structured output.

Latency

Under 2s

Price

$12

/1k calls

ResearchStandard

Balanced depth for most production research

Latency

10-30s

Price

$50

/1k calls

ResearchDeep

Complex questions that span several sources and need cross-referencing.

Latency

Under 2min

Price

$100

/1k calls

ResearchExhaustive

High-stakes questions where claims get verified across dozens of sources.

Latency

Under 5min

Price

$450

/1k calls

ResearchFrontier

Research too long to finish inside a request. Background mode only.

Latency

~5min

Price

$1,200

/1k calls

[Finance Research API](https://you.com/docs/guides/finance-research)

The Research engine tuned for financial questions, at the same price and latency. Use it for company, market, and competitive analysis that needs grounded numbers.

Finance ResearchDeep

Earnings summaries, competitive benchmarking, and multi-quarter trends.

Latency

Under 2 min

Price

$110

/1k calls

Finance ResearchExhaustive

Full 10-K analysis, due diligence, and cross-market research.

Latency

Under 5 min

Price

$500

/1k calls

## Decide what to build, then find API.

Pick what you're building. We'll point you to the endpoint that fits, what it costs, and when to reach for something else.

Web Search

Web Search API

$5

/1k calls

---

Ranked web and news results your model reads and reasons over. You keep full control of synthesis — ideal for RAG.

$10 free credit = 2,000 searches

[View docs](https://you.com/docs/guides/search)[Get an API key](https://docs.you.com/quickstart)

## Enterprise-ready

Get custom pricing, higher rate limits, enterprise security, and dedicated support.

[Talk to a human](https://you.com/book-demo)

- ### ZDR available

  All queries and data can be automatically purged—giving you complete control over what's stored and for how long.
- ### SOC 2 certified

  Our infrastructure is independently audited to ensure best-in-class data security, privacy, and availability.
- ### DPA-ready

  Designed to seamlessly accommodate Data Processing Agreements.
- ### CCPA

  Compliant with California Consumer Privacy Act requirements for data handling and consumer rights.
- ### Custom QPS limits

  Enterprise-grade concurrency with performance optimization for high-volume usage available on request.
- ### Dedicated support

  Direct access to our engineering team for onboarding, optimization, and priority issue resolution.
- > The reliability and latency improvements when using You.com were decisive factors. We cut P50 web search latency from over five seconds to sub-one second and pushed our success rate to three 9s or higher.

  Jonathan Lucuix-Andre

  Technical Staff, Factory

## Frequent questions about API pricing

One request to an endpoint is one billable call, whatever it returns. A Web Search call returning 1 result and one returning 100 cost the same. Contents is billed per page returned.
