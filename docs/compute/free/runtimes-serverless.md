# What answers an HTTP request for nothing

A serverless runtime is not a machine. It answers a request, runs for
milliseconds, and stops. The relevant question differs from the other documents
in this topic: not how long it lives, but whether it can open an outbound socket,
whether it can hold a connection open, and what the CPU wall is.

The answer: Cloudflare Workers is the only free tier in this class worth building
on. It gives 100,000 requests a day, 128 MB of memory, 50 subrequests per request
and six simultaneous outgoing connections, with no duration limit while the client
stays connected and a 10 ms CPU wall per request. Google Cloud Run gives 2 million
requests and 180,000 vCPU-seconds a month, which is 50 vCPU-hours and 25 hours of a
2 vCPU service, and it can listen on a port. Every other runtime here is either a
request-count allowance with a CPU wall that a data workload will hit, or a trial.

## The comparison

Sorted by what a free plan can actually do. `CPU wall` is the number that stops a
data workload.

| Provider | Free tier | CPU wall | Outbound | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cloudflare Workers | 100,000 requests a day, 128 MB | 10 ms per request | 50 subrequests, 6 connections | email | qualifies-with-caveat |
| Cloudflare Durable Objects | 13,000 GB-seconds a day of duration | 10 ms per request | through the edge | email | qualifies-with-caveat |
| Google Cloud Run | 2M requests, 180,000 vCPU-s, 360,000 GB-s a month | per-request, 60 minutes maximum | unrestricted | card | qualifies-with-caveat |
| Vercel Sandbox | 5 active-CPU hours a month | not applicable: a sandbox | 15 open ports | email | qualifies-with-caveat |
| Cloudflare Containers | Workers Paid only | 30 seconds default | unrestricted | card | paid-only |
| AWS Lambda | credit figure from the catalogue, unread | not stated | not stated | card | trial-only |
| Deno Deploy | a free plan on a request count | not read | not read | email | qualifies-with-caveat |

## Cloudflare Workers

Workers Free gives 100,000 requests a day, 10 ms of CPU time per request, 128 MB
of memory, 50 subrequests per request and 6 simultaneous outgoing connections
(`documented`, `developers.cloudflare.com/workers/platform/limits/`, read
2026-10-22). There is no request-per-second cap.

The duration rule is the one that makes this usable: there is no hard limit on
duration for an HTTP-triggered Worker. As long as the client remains connected,
the Worker can keep processing, make subrequests and stream a response. Cron
triggers, Durable Object alarms and queue consumers are capped at 15 minutes.

⛔ 10 ms of CPU is the wall, not the 100,000 requests. Waiting on a `fetch` does
not count toward CPU time, so a Worker that calls an API and streams the answer
can run for hours. A Worker that parses a 100 MB JSON document hits the wall in
the first second.

The six simultaneous outgoing connections and the 50-subrequest cap decide the
shape of any crawl: a Worker cannot fan out to sixty hosts at once, and it cannot
make sixty requests in one invocation on the free plan.

Evidence: the Workers limits page (read 2026-10-22), including the Duration
section. Verdict: the only free runtime here that can serve, and a CPU budget too
small for data processing.

## Google Cloud Run

The free tier for request-based billing is 2 million requests a month, 360,000
GB-seconds of memory and 180,000 vCPU-seconds of compute, plus 1 GB of outbound
data transfer from North America a month (`documented`,
`cloud.google.com/free/docs/free-cloud-features`, read 2026-10-22).

180,000 vCPU-seconds is 50 vCPU-hours. On a 2 vCPU service that is 25 hours of
compute a month, which is more useful for a data job than a Worker's 10 ms and far
less than a sandbox. A Cloud Run service can also listen on a port and hold a
connection, which a Worker cannot.

The cost of the card is real and so is the cold start. A container that has scaled
to zero takes hundreds of milliseconds to answer.

⚠ An unresolved question remains about whether the grant applies to the Services
meter or the Instances meter. The record says so rather than picking a number.

Evidence: `cloud.google.com/free/docs/free-cloud-features` (read 2026-10-22), the
Cloud Run row. Verdict: the most compute on a free serverless plan and a card at
signup.

## Cloudflare Durable Objects

A Durable Object is a single-threaded, stateful, WebSocket-capable object with
128 MB of memory. Its free allowance is 13,000 GB-seconds of duration a day, and
that is a Durable Object allowance rather than a Workers one (`documented`,
`developers.cloudflare.com/durable-objects/platform/pricing/`, read 2026-10-22).
Workers Free separately carries 100,000 requests a day (`documented`,
`developers.cloudflare.com/workers/platform/limits/`, read 2026-10-22).

A Durable Object stays active while a request, an RPC call, a response stream, a
WebSocket or pending I/O is in flight, and duration is billed only while active.
That makes it the cheapest way to hold a long-lived connection: a WebSocket that
sends one message a minute keeps the object active for a minute's worth of
duration rather than an hour's.

It cannot run a binary, it has 128 MB, and it is single-threaded. It is a
coordination point, a counter, a queue and a relay. It is not a worker.

Evidence: the Durable Objects pricing page for the duration allowance and the
Workers limits page for the request count (both read 2026-10-22). Verdict: the
best free stateful substrate and the smallest.

## Cloudflare Containers

There is no free plan. Containers are included with Workers Paid at USD 5 a month,
which carries 25 GiB-hours of memory, 375 vCPU-minutes and 200 GB-hours of disk a
month (`documented`,
`developers.cloudflare.com/containers/platform/pricing/`, read 2026-10-22). The
default CPU limit is 30 seconds and the maximum is 5 minutes.

The egress line is the reason to look: USD 0.025 per GB in North America and
Europe with 1 TB included, which is the largest included traffic allowance of any
row in this topic.

Evidence: the Containers pricing page (read 2026-10-22). Verdict: paid-only, and
worth the USD 5 for the egress rather than the compute.

## What did not work

- **AWS Lambda**: the catalogue carries a credit figure for it and no always-free
  compute row. The Free Tier page states up to USD 200 of
  credits over 6 months and then the account closes, which makes the account a
  trial regardless of the per-service always-free list. The Lambda record stays
  `reported` and this document does not rank it.
- **Deno Deploy as a measured row**: the catalogue carries it as a free plan on a
  request count and its rate is unpublished. No free-tier page has been read for
  it, so its record stays `reported` and this
  document does not rank it. It is not a dead end; it is an unread row, and the
  difference matters.
- **Vercel Sandbox as a runtime**: it is a sandbox with a 45-minute session, which
  is the `free/sandboxes-container-vm.md` document's problem.
- **A Worker as a proxy for large files**: 128 MB of memory and a 10 ms CPU wall.
  It can stream, and it cannot buffer.

## Chaining

A Worker in front of a Durable Object in front of a sandbox is the shape this
class rewards. The Worker terminates the request and enforces the rate. The
Durable Object holds the state and the WebSocket. The sandbox does the work that
needs a filesystem. Each layer has a different free allowance and none of them
consumes another's.
