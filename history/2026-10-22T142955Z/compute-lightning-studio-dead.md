# Lightning AI's free Studio is dead, and the pricing page still sells it

- **When:** 2026-10-22T14:29:55Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/lightning-ai.json` verdict `qualifies-with-caveat`; `docs/compute/free/always-on-free.md`; `docs/compute/free/dev-environments.md`; `docs/compute/README.md`
- **Superseded by:** `dossier/compute/lightning-ai.json` verdict `dead`; `docs/compute/free/always-on-free.md` section "What the always-on class is worth after Lightning"
- **Evidence:** `https://lightning.ai/security-incident` and `https://status.lightning.ai`, both read 2026-10-22; the incident page is dated October 2026 and the status page still carried the down banner on the day of the read
- **Confidence:** documented

## What we believed

That Lightning AI offered one free Studio that ran continuously, subject to a four-hour
forced restart. The record was built from `https://lightning.ai/pricing`, which states
"Run 1 Studio free 24/7. No credit card. No commitments." and "Free Studios run 24/7 but
require restart every 4 hours." The binding constraint was recorded as
`retention-clamped`, on the grounds that the restart was the first thing to fail.

## What we found

The platform is closed. The incident page states:

> On **October 15, 11:00 PM UTC** we identified a security incident on the Lightning
> Platform involving unauthorized access to credentials. We revoked all user access to the
> Lightning Platform on **October 16 at 1:00 AM UTC** to address the issue.

and

> This is an active investigation and during this time the Platform will remain
> inaccessible to all users as our teams focus on addressing the event.

The same page names the affected services as "Studio, Deployments, Pipelines, and Drive"
and states that the GPU cluster rental infrastructure and the managed services
"like Kubernetes and SLURM" are not affected.

`https://status.lightning.ai` carried the banner "Service is down to address a security
incident" with a last update of 2026-10-19 12:49 UTC, and the incident was still open when
read on 2026-10-22, six days after access was revoked.

`https://lightning.ai/pricing` was not updated. It still offers the free Studio on the day
of the read. The marketing page and the incident page therefore disagree, and the incident
page is both newer and more specific.

## How we found it

A window pass on inverse signals read the incident page while looking for something else
in the same provider. The record had never cited it because the earlier pass read the
pricing page and stopped there, which is the failure the evidence ladder calls "a vendor
page proves a price, not that a limit is enforced": here the vendor page proves a product
that cannot be bought or run.

## What it changes

The record becomes `dead`, with `write-gated` as the binding constraint: no Studio can be
created, so the free allowance cannot be reached at all. The four-hour restart is no
longer the constraint that matters, and the sentence about it is kept only as history.

The paid lane is not dead. GPU cluster rental and the managed Kubernetes and SLURM
services are outside the incident, so a reader who needs accelerated compute at Lightning
should read the paid documents, not this record.

The lesson worth carrying: a shutdown announced on a security or status page is invisible
to a pricing-page read, and the status page is the only place that dates the closure. Every
record whose free tier is a hosted platform should cite the status page as well as the
pricing page.
