# Cloud.ru's free VM stopped accepting registrations on 2026-06-30

- **When:** 2026-10-22T16:20:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/cloud-ru-evolution.json` verdict `trial-only`
- **Superseded by:** `dossier/compute/cloud-ru-evolution.json` verdict `fails-identity`; `docs/compute/free/forum-hosts.md`
- **Evidence:** vendor pages and campaign rules read 2026-10-22 through `scripts/broker/broker.sh`; the exact URLs and quoted sentences are in each record's `evidence[]`
- **Confidence:** documented

## What we believed

That Cloud.ru Evolution was a live free tier: a 2 vCPU / 4 GiB / 30 GB machine for a new
account, with a RUB 4,000 grant alongside it.

## What we found

The campaign rules approved on 2026-06-30 state that the free VM is closed to accounts
registered after that date, and that the account must be registered in the Russian
Federation. What survives is 25 vCPU-hours a month of Container Apps, 10 TB a month of
object-storage egress, 15 GB of storage and 1,000,000 DNS queries.

A second fact from the same lane makes the offer worse than it looks: the free VM never
included a public IP, and renting one costs RUB 151.40 a month, which is more than a working
VPS from three other hosts in the same market.

## What it changes

The verdict becomes `fails-identity`, because the surviving lanes are gated on a Russian
registration. The record keeps the grant's exclusion list, which is the reason a grant
programme does not repair a closed free tier: the RUB 4,000 grant excludes every GPU SKU and
the Container Apps allowance.
