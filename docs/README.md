# docs

One fact has one home. When two documents disagree, the owner below is right and
the other is a defect: in an own clone, fix it in the same change; a run files an
`open_question` that names the document.

Every topic answers the same question for a different market: **what can be had
for nothing, or for the least money, and what does it actually cost in
constraints, identity and reliability?** The structure is deliberately uniform so
a reader who has learned one topic can navigate all of them.

## The topics

| topic | what it covers | the question a reader arrives with |
|---|---|---|
| [`storage/`](storage/README.md) | object storage, drives, registries, academic and institutional repositories, file hosts, media hosts, the cheap-paid disk lane | where do 20 TiB live, and where do 1 TiB/day come from |
| [`netdisk-pan/`](netdisk-pan/README.md) | consumer pan drives, the AList/OpenList/Cloudreve bridge ecosystem, public instances, direct-link extraction | which drive can I mount, and which of these public instances is real |
| [`compute/`](compute/README.md) | serverless runtimes, container and VM sandboxes, dev environments, GPU and notebook hosts, agent runtimes, anonymous VMs | what can I run, for how long, and what reaps it |
| [`coding-subs/`](coding-subs/README.md) | coding-agent subscriptions, their included models, quotas and overage | which subscription buys the most agent work per dollar |
| [`inference/`](inference/README.md) | free, guest and unauthenticated model endpoints; free tiers of paid inference; self-hosting on free compute | what will answer a completion request without a card |
| [`crawler-scraper/`](crawler-scraper/README.md) | search APIs, reader and extractor APIs, headless browsers, crawl APIs, archivers, fetch relays — and the broker this repository uses | how do I read the web at scale, and what do I do when a page is walled |
| [`debrid/`](debrid/README.md) | debrid multi-hosters, usenet, torrent-to-cloud, hosted downloaders, indexes, Telegram bots | which subscription turns the least money into the most retrieved bytes |
| [`egress/`](egress/README.md) | tunnels, relays, CDN fronting, WireGuard UDP ingress, WARP-class egress, consumer-connection and mobile exit, free static ingress | how do I get traffic out, or a service in, without a bill |
| [`email/`](email/README.md) | transactional senders, SMTP relays, inbound routing, disposable and catch-all mail | how do I send and receive mail at volume for nothing |
| [`databases-kv/`](databases-kv/README.md) | managed Postgres, MySQL, Redis, document, vector and edge KV | where does state live after the free tier ends |
| [`domains-dns/`](domains-dns/README.md) | free subdomains, free managed DNS with an API, cheapest registrars, free TLS | what is the cheapest name I can put a service on |
| [`ci-cd-runners/`](ci-cd-runners/README.md) | compute obtained through continuous integration, plus the artifact and cache storage that comes with it | what can I run by pretending it is a build |
| [`ip-proxy/`](ip-proxy/README.md) | exit identity: leased prefixes, per-address ISP proxies, residential and mobile networks, VPN exits, free lists, and the client-stack and transport techniques that move the exit | what does the upstream see, and can I change it |
| [`dev-services/`](dev-services/README.md) | developer services that are not a VM and not a model API: monitoring, error tracking, analytics, scheduled jobs, workflow, queues, realtime, authentication | which of these services is free with no card, and what stops it first |
| [`data-apis/`](data-apis/README.md) | free data APIs and their bulk downloads: geocoding, IP geolocation, market data, weather, news, open knowledge | how many free calls, at what rate, and is there a dump |

[`expansion/`](expansion/README.md) is not a topic. It holds the gap analyses for
three areas, each with its measured gap, its discovery method, its verification
gate and its staleness policy.
[`maintenance.md`](maintenance.md) is the operating schedule: what to run weekly,
monthly and quarterly, and how to read a red gate.
[`sessions.md`](sessions.md) is the session protocol: starting, ending and
resuming.
[`research-protocol.md`](research-protocol.md) is the procedure for a research
run: from the plan to the landed pull request.

## How each topic is laid out

```text
<topic>/
  README.md          the topic's starting point: what it covers, the answer, the binding constraints, the dead ends
  free/<slug>.md     one document per provider class, free lane
  paid/<slug>.md     the same classes, cheapest-paid lane
```

Not every topic splits free from paid, and a topic says so in its own README when
it does not. `netdisk-pan` splits by access mode instead, because a public
instance's price is not the thing that decides whether it can be used.

## The three registers

- **A topic README** is navigation. It states the answer in one paragraph, then
  the constraint that binds, then a table of the documents with what each
  answers. A reader who stops after the README should still have made no wrong
  decision.
- **A provider-class document** is the substance. It states what the class is,
  who is in it, a comparison table, then one short section per provider with the
  numbers, the constraint, the identity cost, the evidence and the verdict.
- **A dossier record** in [`../dossier/`](../dossier/README.md) is the machine
  form of the same facts. Documents are views of dossiers, never the reverse.

## What every document owes

| obligation | because |
|---|---|
| the **binding constraint**, named from the vocabulary in [`../dossier/README.md`](../dossier/README.md) | the headline number is almost never the one that decides |
| the **identity cost** | a 100 TB quota behind an institutional login is worth zero to a reader without one |
| a **date and a URL** for every number | a number without them cannot be checked |
| the **verdict**, including "dead" | a dead end recorded once is not researched twice |
| the **evidence rung** — measured, documented, reported, inferred, unverified | a reader must be able to weigh a claim without re-reading its source |

## What no document does

- It does not give legal or terms-of-service advice. Reliability failures are
  recorded as technical notes.
- It does not repeat a fact that a topic README or a dossier already owns. It
  links.
- It does not carry history. A superseded claim moves to
  [`../history/`](../history/README.md) and is linked from both ends.

## Checking that the tree is coherent

CI runs `sh scripts/gate.sh --root .` on every pushed head, in the public repository's Actions. A research session never runs it in the
research checkout ([`../AGENTS.md`](../AGENTS.md) section 2 rule 14); in an own clone, run it there.

The gate fails when a document named here is missing, when a link is broken, or
when a `measured` or `documented` record is cited by no document. No check of the
gate compares a number in a document with its record: `python scripts/report/render.py --check`
tells whether a generated table agrees with its records, and nothing checks a
hand-typed number.
