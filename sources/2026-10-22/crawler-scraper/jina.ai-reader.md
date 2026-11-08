---
title: "Reader API"
description: "Convert any URL to Markdown for better grounding LLMs."
words: 2836
upstream_status: 200
content_kind: page
extraction: main
source: extractor
title_source: meta
final_url: "https://jina.ai/reader/"
fetched_at: "2026-10-22T04:01:01.659Z"
---
# Reader

Convert a URL to LLM-friendly input by prepending `r.jina.ai`.

---

---

## Reader API

Convert a URL to LLM-friendly input by prepending `r.jina.ai`.

API Key & Billing

Usage

More

---

[Rate limit](https://jina.ai/api-dashboard/rate-limit)

[Raise issue](https://github.com/jina-ai/reader/issues)

[FAQ](https://jina.ai/reader#faq)

[Status](https://status.jina.ai/)

---

Use `r.jina.ai` to read a URL and fetch its content

Use `s.jina.ai` to search the web and get SERP

Add `mcp.jina.ai` as your MCP server to use our APIs in LLMs

---

Parameters

Add API Key for Higher Rate Limit

Enter your Jina API key to access a higher rate limit. For latest rate limit information, please refer to the table below.[Learn more](https://jina.ai/reader#rate-limit)

Browser Engine (Quality/Speed)

X-Engine

Choose the browser engine for fetching the webpage content. This affects the quality, speed, completeness, accessibility of the content.[Learn more](https://jina.ai/api-dashboard/reader-speed-test)

Default

Content Format

Return-Format

You can control the level of detail in the response to prevent over-filtering. The default pipeline is optimized for most websites and LLM input.

Default

JSON Response

Accept

The response will be in JSON format, containing the URL, title, content, and timestamp (if available). In Search mode, it returns a list of five entries, each following the described JSON structure.

Timeout (seconds)

X-Timeout

Maximum time to wait for page load. Increase for slow pages, decrease for simple static pages.

Token Budget

X-Token-Budget

Limits the maximum number of tokens used for this request. Exceeding this limit will cause the request to fail.

Use jina-ocr-v1

X-Respond-With

Uses jina-ocr-v1 to convert images to Markdown, delivering high-quality results on pages and documents with complex structure and content. Costs 40× more tokens![Learn more](https://jina.ai/news/jina-ocr-v1-faster-document-parsing-on-low-budget-gpus)

Pagination

X-Page

The page to process. Focuses on the specified page of a multi-page document, and only applies when a document such as a PDF is being processed.

Extract Only (CSS Selector)

X-Target-Selector

Only extract content matching these CSS selectors. Example: article, .main-content, #post-body

Wait For (CSS Selector)

X-Wait-For-Selector

Wait until these elements appear before extracting content. Useful for dynamically loaded content.

Exclude (CSS Selector)

X-Remove-Selector

Remove these elements before extraction. Example: nav, footer, .sidebar, #ads

Remove All Images

X-Retain-Images

Strip all images from the output. Reduces token usage when images are not needed.

OpenAI Citation Format

X-Retain-Links

Format links for OpenAI's web browsing tool. Uses special citation markers compatible with GPT models.[Learn more](https://cookbook.openai.com/articles/openai-harmony#browser-tool)

Links Summary Section

X-With-Links-Summary

A "Buttons & Links" section is added at the end. This helps downstream LLMs and web agents navigate the page or take further actions.

None

Images Summary Section

X-With-Images-Summary

An "Images" section will be created at the end. This gives the downstream LLMs an overview of all visuals on the page, which may improve reasoning.

None

Browser Viewport Size

POST

viewport

Set browser window dimensions. Affects responsive layouts and content visibility.[Learn more](https://pptr.dev/api/puppeteer.viewport)

Forward Cookie

X-Set-Cookie

Our API server can forward your custom cookie settings when accessing the URL, which is useful for pages requiring extra authentication. Note that requests with cookies will not be cached.[Learn more](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

Image Caption

X-With-Generated-Alt

Captions all images at the specified URL, adding 'Image [idx]: [caption]' as an alt tag for those without one. This allows downstream LLMs to interact with the images in activities such as reasoning and summarizing.

Use a Proxy Server

X-Proxy-Url

Our API server can utilize your proxy to access URLs, which is helpful for pages accessible only through specific proxies.[Learn more](https://en.wikipedia.org/wiki/Proxy_server)

Use a Country-Specific Proxy Server

X-Proxy

Set country code for location-based proxy server. Use 'auto' for optimal selection or 'none' to disable.

Bypass Cached Content

X-No-Cache

Our API caches URL contents for a certain amount of time. Set it to true to ignore the cached result and fetch the content from the URL directly.

Cache Tolerance (seconds)

X-Cache-Tolerance

Accept cached content if younger than N seconds. Set to 0 for fresh content (same as Bypass Cache), or higher values to allow faster responses from cache.

Page Ready Timing

X-Respond-Timing

When to consider a page fully loaded. Later timings wait longer but capture more dynamic content.

Default

Custom User-Agent

X-User-Agent

Override the browser User-Agent string. Useful for accessing sites that require specific browsers or block crawlers.

Custom Referer

X-Referer

Set the HTTP Referer header. Some sites check this to verify traffic comes from expected sources.

Preserve Base64 Images

X-Keep-Img-Data-Url

Keep inline base64-encoded images in markdown output instead of converting them to external URLs.

Do Not Cache or Track

DNT

Prevent this request from being cached or logged on our servers. Use for sensitive URLs.

GitHub Flavored Markdown

X-No-Gfm

Opt in/out features from GFM (GitHub Flavored Markdown).

Enabled

Stream Mode

Accept

Stream mode is beneficial for large target pages, allowing more time for the page to fully render. If standard mode results in incomplete content, consider using Stream mode.[Learn more](https://github.com/jina-ai/reader?tab=readme-ov-file#streaming-mode)

Customize Browser Locale

X-Locale

Control the browser locale to render the page. Lots of websites serve different content based on the locale.[Learn more](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/language)

Respect robots.txt

X-Robots-Txt

Check robots.txt rules before fetching. Specify which bot name to use for the check.

Include iframe Content

X-With-Iframe

Extract content from embedded iframes. Enable for pages with content loaded in iframes.

Include Shadow DOM

X-With-Shadow-Dom

Extract content from Shadow DOM components. Enable for pages using web components.

Use Final URL as Base

X-Base

Resolve relative URLs using the final destination URL after redirects, instead of the original URL.

Local PDF/HTML file

POST

Use Reader on local PDF and HTML files by uploading them. Only PDF and HTML files are supported. For HTML, also specify a reference URL so related CSS/JS scripts can be parsed correctly.

Run JavaScript Before Extraction

POST

Execute custom JS to modify the page before content extraction. Can be inline code or a URL to a script file.[Learn more](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

Heading Style

X-Md-Heading-Style

Sets markdown heading format (passed to Turndown).

Hash Style

Horizontal Rule Style

X-Md-Hr

Defines markdown horizontal rule format (passed to Turndown).

Bullet Point Style

X-Md-Bullet-List-Marker

Sets bullet list marker character (passed to Turndown).

*

Emphasis Style

X-Md-Em-Delimiter

Defines markdown emphasis delimiter (passed to Turndown).

_

Strong Emphasis Style

X-Md-Strong-Delimiter

Sets markdown strong emphasis delimiter (passed to Turndown).

**

Link Style

X-Md-Link-Style

Determines markdown link format (passed to Turndown).

Inline

EU Residency

Experimental

When enabled, infrastructure and data processing for this request are located within the EU.

---

Request

GET

Bash

```
curl "https://r.jina.ai/https://www.example.com"
```

---

---

API key

---

Available tokens

0

This is your unique key. Store it securely!

## jina-ocr-v1: Faster Document Parsing on Low-Budget GPUs

A 3.4B mixture-of-experts document parser that activates only 570M parameters per token. It reads a page image and returns Markdown with text, formulas, tables and reading order in a single pass.

## What is Reader?

Feeding web information into LLMs is an important step of grounding, yet it can be challenging. The simplest method is to scrape the webpage and feed the raw HTML. However, scraping can be complex and often blocked, and raw HTML is cluttered with extraneous elements like markups and scripts. The Reader API addresses these issues by extracting the core content from a URL and converting it into clean, LLM-friendly text, ensuring high-quality input for your agent and RAG systems. The Reader API is developer infrastructure: it converts a URL you supply into LLM-friendly text so you can build your own search, RAG, and agent systems. It is not a consumer search engine and does not index or rank the web on your behalf; you control which URLs are processed and are responsible for how the output is used.

Enter your URL

Click below to fetch the source code of the page directly

---

Reader URL

Click below to obtain the content through our Reader API

---

---

Raw HTML

---

Reader Output

---

Pose a Question

Input a question and combine it with the fetched content for LLM to generate an answer

## Reader for web search and SERP

Reader can be used as SERP API. It allows you to feed your LLM with the content behind the search results engine page. Simply prepend `https://s.jina.ai/?q=` to your query, and Reader will search the web and return the top five results with their URLs and contents, each in clean, LLM-friendly text. This way, you can always keep your LLM up-to-date, improve its factuality, and reduce hallucinations.

Enter your query

Type a question that requires latest information or world knowledge.

---

Reader URL

If you use this URL in code, don't forget to encode the URL.

---

---

Please note that unlike the demo shown above, in practice you do not search the original question on the web for grounding. What people often do is rewrite the original question or use multi-hop questions. They read the retrieved results and then generate additional queries to gather more information as needed before arriving at a final answer.

## Reader also reads images!

Images on the webpage are automatically captioned using a vision language model in the reader and formatted as image alt tags in the output. This gives your downstream LLM just enough hints to incorporate those images into its reasoning and summarizing processes. This means you can ask questions about the images, select specific ones, or even forward their URLs to a more powerful VLM for deeper analysis!

## Reader also reads PDFs!

Yes, Reader natively supports PDF reading. It's compatible with most PDFs, including those with many images, and it's lightning fast! Combined with an LLM, you can easily build a ChatPDF or document analysis AI in no time.

[Original PDF](https://www.nasa.gov/wp-content/uploads/2023/01/55583main_vision_space_exploration2.pdf)

---

[Reader Result](https://r.jina.ai/https://www.nasa.gov/wp-content/uploads/2023/01/55583main_vision_space_exploration2.pdf)

## The best part? It's free!

Reader API is available for free and offers flexible rate limit and pricing. Built on a scalable infrastructure, it offers high accessibility, concurrency, and reliability. We strive to be your preferred grounding solution for your LLMs.

Rate limit

Rate limits are tracked in two ways: **RPM** (requests per minute) and **TPM** (tokens per minute). Limits are enforced per IP/API key and will be triggered when either the RPM or TPM threshold is reached first. When you provide an API key in the request header, we track rate limits by key rather than IP address.

Columns

|  | Product | API Endpoint | Description | w/o API Key | w/ Free API Key | w/ Paid API Key | w/ Premium API Key | Average latency | Token Usage Counting | Allowed Request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Reader API | `https://r.jina.ai` | Converts a URL to LLM-friendly text | 20 RPM | 500 RPM | 500 RPM | 5000 RPM | 7.9s | Count the number of tokens in the output response. | GET/POST |
|  | Reader API | `https://s.jina.ai` | Search the web and convert results to LLM-friendly text |  | 100 RPM | 100 RPM | 1000 RPM | 2.5s | Every request costs a fixed number of tokens, starting from 10,000 tokens | GET/POST |
|  | Embedding API | `https://api.jina.ai/v1/embeddings` | Convert text/images to fixed-length vectors |  | 100 RPM & 100,000 TPM | 500 RPM & 2,000,000 TPM | 5,000 RPM & 50,000,000 TPM | depends on the input size | Count the number of tokens in the input request. | POST |
|  | Reranker API | `https://api.jina.ai/v1/rerank` | Rank documents by query |  | 100 RPM & 100,000 TPM | 500 RPM & 2,000,000 TPM | 5,000 RPM & 50,000,000 TPM | depends on the input size | Count the number of tokens in the input request. | POST |

Don't panic! Every new API key comes with 10M free tokens!

---

## API Pricing

API pricing is based on the token usage. One API key gives you access to all search foundation products.

With Jina Search Foundation API

The easiest way to access all of our products. Top-up tokens as you go.

Enter the API key you wish to recharge

Top up this API key with more tokens

Depending on your location, you may be charged in USD, EUR, or other currencies. Taxes may apply.

Please enter the correct API key to top up.

Understand the rate limit

Rate limits are the maximum number of requests that can be made to an API within a minute per IP address/API key (RPM). Find out more about the rate limits for each product and tier below.

Auto top-up on low token balance

Recommended for uninterrupted service in production. When your token balance drops below the set threshold, we will automatically recharge your saved payment method for the last purchased package, until the threshold is met.

We introduced a new pricing model on May 6th, 2025. If you enabled auto-recharge before this date, you'll continue to pay the old price (the one when you purchased). The new pricing only applies if you modify your auto-recharge settings or purchase a new API key.

< 1M Tokens

Top up when

## FAQ

What are the costs associated with using the Reader API?

How does the Reader API function?

Is the Reader API open source?

What is the typical latency for the Reader API?

Why should I use the Reader API instead of scraping the page myself?

Does the Reader API support multiple languages?

Does the Reader API respect website access controls?

Can the Reader API extract content from PDF files?

Can the Reader API process media content from web pages?

Is it possible to use the Reader API on local HTML files?

Does Reader API cache the content?

Can I use the Reader API to access content behind a login?

Can I use the Reader API to access PDF on arXiv?

How does image caption work in Reader?

What is the scalability of the Reader? Can I use it in production?

What is the rate limit of the Reader API?

What is ReaderLM? How can I use it?

How do I extract structured data from webpages?

Does Reader actively bypass website anti-bot protection?

Will upgrading from a free to a paid API key give me access to more websites?

Can I run Reader inside my own infrastructure?

### How to get my API key?

Your browser does not support embedded video

### What's the rate limit?

Rate limit

Rate limits are tracked in two ways: **RPM** (requests per minute) and **TPM** (tokens per minute). Limits are enforced per IP/API key and will be triggered when either the RPM or TPM threshold is reached first. When you provide an API key in the request header, we track rate limits by key rather than IP address.

Columns

|  | Product | API Endpoint | Description | w/o API Key | w/ Free API Key | w/ Paid API Key | w/ Premium API Key | Average latency | Token Usage Counting | Allowed Request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Reader API | `https://r.jina.ai` | Converts a URL to LLM-friendly text | 20 RPM | 500 RPM | 500 RPM | 5000 RPM | 7.9s | Count the number of tokens in the output response. | GET/POST |
|  | Reader API | `https://s.jina.ai` | Search the web and convert results to LLM-friendly text |  | 100 RPM | 100 RPM | 1000 RPM | 2.5s | Every request costs a fixed number of tokens, starting from 10,000 tokens | GET/POST |
|  | Embedding API | `https://api.jina.ai/v1/embeddings` | Convert text/images to fixed-length vectors |  | 100 RPM & 100,000 TPM | 500 RPM & 2,000,000 TPM | 5,000 RPM & 50,000,000 TPM | depends on the input size | Count the number of tokens in the input request. | POST |
|  | Reranker API | `https://api.jina.ai/v1/rerank` | Rank documents by query |  | 100 RPM & 100,000 TPM | 500 RPM & 2,000,000 TPM | 5,000 RPM & 50,000,000 TPM | depends on the input size | Count the number of tokens in the input request. | POST |

API-related common questions

Can I use the same API key across all Jina APIs?

Can I monitor the token usage of my API key?

What should I do if I forget my API key?

Do API keys expire?

Can I transfer tokens between API keys?

Can I revoke my API key?

Why is the first request for some models slow?

Is my API data used to train your models?

What are the rate limits for Jina APIs?

Are there batch size limits for the APIs?

Are the Jina APIs the same thing as Jina models inside Elastic?

Billing-related common questions

Is billing based on the number of sentences or requests?

Is there a free trial available for new users?

Are tokens charged for failed requests?

What payment methods are accepted?

Is invoicing available for token purchases?

How do I buy a commercial license rather than API tokens?

Can I pay by invoice or purchase order instead of card?

I paid, but my balance or rate limit has not changed. What should I check?

How do I cancel, stop auto top-up, or remove a saved payment method?
