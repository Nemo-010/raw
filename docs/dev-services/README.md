# dev-services

Free developer services that are not a virtual machine and not a model API. The question:
**which monitoring, analytics, job, queue, realtime and authentication services give a free tier
with no card, and what stops each one first?**

The topic holds 61 records. No document yet; the records are in `dossier/dev-services/`.

## What the topic covers

| class | examples to research | the number that decides |
| --- | --- | --- |
| uptime and synthetic monitoring | Better Stack, UptimeRobot, cron-job.org | monitors, check interval, retention |
| error tracking and logs | Sentry, Axiom, Honeycomb, New Relic, Grafana Cloud | events or bytes a month, retention days |
| product analytics | PostHog, Plausible | events a month, retention |
| scheduled jobs and workflow | n8n, Zapier, Pipedream, EasyCron, Inngest, Temporal, Trigger.dev, Windmill Cloud, Val Town | runs or tasks a month, run duration |
| message queues and realtime | CloudAMQP, Ably, Pusher, PubNub | messages a day or a month, concurrent connections |
| managed authentication and feature flags | Clerk, Auth0, Stytch, WorkOS, LaunchDarkly, GrowthBook, Flagsmith | monthly active users, seats |

Not in this topic: a virtual machine, a container host or a notebook (`compute`), a model
endpoint (`inference`), a database (`databases-kv`), a mail sender (`email`), a CI runner
(`ci-cd-runners`).

## Records that sit in a neighbour topic

These records describe developer services and sit under `compute`. A record's `topic`
and `slug` do not change, so a duplicate is recorded as a relation: `src` the old
record, `kind` `duplicate_of`, `dst` the new one
([`../research-protocol.md`](../research-protocol.md) section 2). A record that stays
where it is carries the reason in its `notes`.

| record | verdict on 2026-10-28 |
| --- | --- |
| [`compute/sentry`](../../dossier/compute/sentry.json) | qualifies-with-caveat |
| [`compute/grafana-cloud`](../../dossier/compute/grafana-cloud.json) | qualifies-with-caveat |
| [`compute/datadog`](../../dossier/compute/datadog.json) | fails-identity |
| [`compute/trigger-dev`](../../dossier/compute/trigger-dev.json) | qualifies-with-caveat |
| [`compute/val-town`](../../dossier/compute/val-town.json) | qualifies-with-caveat |
| [`compute/windmill-cloud`](../../dossier/compute/windmill-cloud.json) | qualifies-with-caveat |
| [`compute/windmill`](../../dossier/compute/windmill.json) (self-hosted) | qualifies-with-caveat |

## What a record in this topic states

- The free limit as a number, a unit and a period, quoted from a first-party page. `free_tier.unit`
  is `requests`, `users`, `minutes`, `hours` or `mixed` with the unit named in `stated`.
- The retention of the data the service keeps, in days.
- Whether a card is necessary, and the identity kind.
- What happens at the limit: a refusal, a queue, a bill, or a silent drop.

⚠ **A free tier that needs a self-hosted component is two findings.** Record the hosted free tier,
and name the self-hosted part in `tooling`. The self-hosted part runs on rented or free compute
from `compute`, never on hardware the user must buy.

## Documents

None yet. Every record is in `dossier/dev-services/`.

## Staleness

`scripts/dossier/staleness.policy.json` sets 45 days for a verified record and 180 days for the
oldest evidence row in this topic.

## Records that no other document names

Each `measured` or `documented` record of this topic that no other document of `docs/` names.

<!-- generated:start topic=dev-services kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `amplitude` | Amplitude | qualifies-with-caveat | documented |
| `aptabase` | Aptabase | qualifies-with-caveat | documented |
| `better-stack` | Better Stack | qualifies-with-caveat | documented |
| `bugfender` | Bugfender | qualifies-with-caveat | documented |
| `checkly` | Checkly | qualifies-with-caveat | documented |
| `cloudamqp-little-lemur` | CloudAMQP | qualifies-with-caveat | documented |
| `cloudamqp-loyal-lemming` | CloudAMQP | qualifies-with-caveat | documented |
| `cron-job-org` | cron-job.org | qualifies | documented |
| `cronitor` | Cronitor | qualifies-with-caveat | documented |
| `datadog-open-source` | Datadog | fails-identity | documented |
| `drumbeats-io` | Drumbeats | qualifies-with-caveat | documented |
| `goatcounter` | GoatCounter | qualifies-with-caveat | documented |
| `healthchecks-io` | Healthchecks.io | qualifies-with-caveat | documented |
| `heap` | Heap | qualifies-with-caveat | documented |
| `hotjar` | Hotjar | qualifies-with-caveat | documented |
| `instatus` | Instatus | qualifies-with-caveat | documented |
| `middleware` | Middleware | qualifies-with-caveat | documented |
| `mixpanel` | Mixpanel | qualifies-with-caveat | documented |
| `n8n-cloud` | n8n | trial-only | documented |
| `new-relic` | New Relic | qualifies-with-caveat | documented |
| `onlineornot` | OnlineOrNot | qualifies-with-caveat | documented |
| `openobserve-cloud` | OpenObserve | trial-only | documented |
| `phare` | Phare | qualifies-with-caveat | documented |
| `pulsetic` | Pulsetic | qualifies-with-caveat | documented |
| `pusher-beams` | Pusher Beams | qualifies-with-caveat | documented |
| `pusher-channels` | Pusher | qualifies-with-caveat | documented |
| `sentry-education` | Sentry | fails-identity | documented |
| `sentry-open-source` | Sentry | qualifies-with-caveat | documented |
| `statsig` | Statsig | qualifies-with-caveat | documented |
| `statuscake` | StatusCake | qualifies-with-caveat | documented |
| `temporal-cloud` | Temporal | trial-only | documented |
| `umami-cloud` | Umami | qualifies-with-caveat | documented |
| `uptimeobserver` | UptimeObserver | qualifies-with-caveat | documented |
| `cron-job-org-chronos` | cron-job.org chronos daemon (self-hos... (self-hosted) | qualifies-with-caveat | documented |
| `inngest-server` | Inngest server (self-hosted) (self-hosted) | qualifies-with-caveat | documented |
| `n8n-community-edition` | n8n Community Edition (self-hosted) (self-hosted) | qualifies-with-caveat | documented |
| `temporal-server` | Temporal server (self-hosted) (self-hosted) | qualifies-with-caveat | documented |
<!-- generated:end -->
