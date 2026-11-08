# Compute seed claims superseded on first read

- **When:** 2026-10-22T03:07:05Z
- **Status:** superseded
- **Supersedes:** the 2026-10-06 `peli-cloud` talaria pass, its free-tier census and its ranked table
- **Superseded by:** `dossier/compute/*.json`, which now own each of the four facts
- **Evidence:** four vendor pages read 2026-10-22, cited per claim below
- **Confidence:** documented

Four claims inherited from the two `peli-cloud` passes do not survive a page read.
The repository is new and the topic's records are its first claims, so this entry
dates the seed numbers rather than correcting a document. Each one is cited from
the record that now owns the fact.

## Run Cloud is withdrawn, and it was the seed's cheapest row

The 2026-10-06 talaria pass priced Run Cloud at USD 0.00 at 2 vCPU and 4 GiB and
ranked it first. Its free-tier census counted a USD 15 a month recurring credit
and called it the third largest in the market.

`docs.run.cloud/sandboxes/index.md` (read 2026-10-22) states that Linux microVM
sandboxes are deprecated, that the capability is being retired, and that it is no
longer available to new organizations. Existing workloads run during the
deprecation window.

The record is `dossier/compute/run-cloud.json`, `verdict: dead`. A ranked table
built on the newer seed pass puts a closed door at the top, and that is why no
ranked table was published from either pass.

## Fly.io has no free tier, and both seeds gave the wrong reason

nemo recorded `provider-documented`; talaria recorded DEAD. `fly.io/docs/about/pricing/`
(read 2026-10-22) states in one sentence that new organizations get no free tier and
no monthly free usage allowance, and that the trial is 2 hours of Machine runtime or
7 days.

talaria's verdict was right and neither pass gave the reason. The host is up; the
offer was withdrawn.

## Lizard was repriced, and both seed figures were stale

talaria carried USD 0.009 an hour for Small, giving USD 2.70 a month. nemo carried
USD 6.55 and labelled it disputed. `lizard.build/pricing` (read 2026-10-22) states
Small at 2 vCPU and 4 GB for USD 0.0162 an hour, Medium for USD 0.0324 and Large
for USD 0.0648.

Both were wrong and the two-page conflict both passes agonised over no longer
exists. The record is `dossier/compute/lizard.json` with a note naming both stale
figures.

## Oracle Cloud was reachable, and its allowance is a time quota

Both passes recorded the whole `oracle.com` domain as returning 403 and carried the
A1 allowance unverified. `oracle.com/cloud/free/` returns HTTP 200 from this host,
so the 403 was one host's egress and not a property of the provider.

The allowance itself is 1,500 OCPU-hours and 9,000 GB-hours a month, which Oracle
states is equivalent to 2 OCPUs and 12 GB. Both passes discussed it as a size cap.
It is a time-denominated quota: 2 OCPUs at 24/7 is 1,460 OCPU-hours and fits with
40 to spare, and 3 OCPUs at 24/7 is 2,190 and does not fit. A reader who believes
the ceiling is a size will build a three-core box and meet a bill.

## Two claims that changed without a provider changing

Modal began charging for network egress on 2026-10-01, three weeks before this read.
Both passes were written before the charge existed, so neither carried an egress
term for Modal. The record now carries one, and a reader working from either pass
would have priced a Modal workload at zero.

Hugging Face Spaces CPU Basic remains 2 vCPU and 16 GB of FREE hardware, and
creating a Gradio or Docker Space that uses it requires PRO. talaria demoted the row
correctly and nemo did not. The hardware did not change; the right to use it did.

## What this means for the topic

Every number in `docs/compute/` that came from a seed pass is `reported` and every
one that was read on 2026-10-22 is `documented` or `measured`. The distribution is
in `docs/compute/measurement.md`. A reader who wants to know which of the 405
records to trust should read that file first, because the honest answer is that 347
of them were inherited without a page read.
