# Cloud credits as a WireGuard ingress, and why most of them fail

A credit is a burst, not a month. The arithmetic that decides a credit is
`credit divided by egress price`, and the number it produces is compared with the
days the credit lasts.

⭐ **Two credits clear 1 TiB/month for their whole window and both are card-gated:
Azure at 2.18 TiB inside 30 days and DigitalOcean at 9.8 TiB a month across 60
days.** Google's USD 300 and AWS's USD 200 do not, because their egress prices are
high enough that the credit buys less than a terabyte a month.

| programme | credit | window | egress price | TB it buys | per month | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Azure free account | USD 200 | 30 days | USD 0.087/GB after 100 GB | 2.18 TiB | 2.18 TiB | `trial-only` |
| DigitalOcean | USD 200 | 60 days | USD 0.01/GiB | 19.5 TiB | 9.8 TiB | `trial-only` |
| Akamai Linode | USD 100 | 60 days | USD 0.005/GB | 18.2 TiB | 9.1 TiB | `trial-only` |
| Oracle Free Trial | USD 300 | 30 days | metered, plus Always Free | unverified | unverified | `trial-only` |
| Google Cloud | USD 300 | 90 days | USD 0.12/GiB | 2.57 TiB | 0.86 TiB | `fails-quota` |
| AWS Free Tier | USD 100 to 200 | 6 months | USD 0.09/GB | 1.01 to 2.02 TiB | 0.26 to 0.43 TiB | `fails-quota` |
| IBM Cloud | USD 200 | unstated | not read | unverified | unverified | `trial-only` |
| Vultr | credit, amount unstated | 30 days | not read | unverified | unverified | `trial-only` |
| Alibaba Cloud | 220 GB/month free | standing | metered | 0.22 TB | 0.2 TiB | `fails-egress` |
| AWS Activate | USD 1,000 to 200,000 | 1 to 2 years | metered | large | large | `fails-identity` |
| Cloudflare for Startups | up to USD 350,000 | 1 year | metered | large | large | `fails-identity` |
| DigitalOcean Hatch | 12 months of credits | 1 year | USD 0.01/GiB | large | large | `fails-identity` |
| GitHub Student Pack | USD 100 Azure | 12 months | USD 0.087/GB | 1.15 TiB | 1.15 TiB | `fails-identity` |
| Azure for Students | USD 100 | 12 months | USD 0.087/GB | 1.15 TiB | 1.15 TiB | `fails-identity` |

## The two that clear the test

**Azure** gives USD 200 for 30 days, and its egress is USD 0.087/GB after the
first 100 GB (`documented`, read 2026-10-23). USD 200 buys 2.18 TiB inside the
window, which clears 1 TiB for one month and then stops.

**DigitalOcean** gives USD 200 for 60 days, and its egress is USD 0.01/GiB
(`reported`, read 2026-10-23: two third-party pages carry the offer and
DigitalOcean's own pricing page did not). USD 200 is 19.5 TiB, or 9.8 TiB a month
across the window.

**Akamai Linode** gives USD 100 for 60 days at USD 0.005/GB, which is 18.2 TiB
(`reported`). The credit is larger than the one DigitalOcean gives and the price
is half.

⚠ **All three are card-gated**, and a card at signup is an identity cost even when
the money is not spent.

## The two that do not

**Google Cloud** preloads USD 300 for 90 days, and its egress is USD 0.12/GiB for
the first 1,024 GiB (`documented`, read 2026-10-23). USD 300 buys 2.57 TiB in
total, which is 0.86 TiB a month across 90 days. The credit is the largest of the
four and the price is the highest.

**AWS** gives USD 100 immediately and up to USD 100 more, over six months, with
100 GB a month of free transfer (`documented`, read 2026-10-23). At USD 0.09/GB
that is 1.01 to 2.02 TiB in total, or 0.26 to 0.43 TiB a month.

⭐ **The lesson is the egress price, not the credit size.** A USD 300 credit at
USD 0.12/GiB is worth less than a USD 100 credit at USD 0.005/GB, by a factor of
seven.

## The programmes that are unreachable

AWS Activate, Cloudflare for Startups, DigitalOcean Hatch and the student packs
are all `fails-identity`: they need a company, an investor introduction, or a
verified student status.

⛔ **A USD 200,000 credit behind a company application is worth zero to a reader
without a company**, and the record says so in the same sentence as the number.

## What is dead

- **A credit that renews monthly**: none found. Every credit here is one-time.
- **Alibaba Cloud's 220 GB/month**: a standing allowance rather than a credit, and
  20% of the test.
- **A student pack without student status**: the gate is the institution.

## Chaining

**The burst chain.** `Azure USD 200 -> a VM -> wg-quick -> a month of service`. The
scarce link is the 30-day window and the card.

**The long chain.** `DigitalOcean USD 200 -> 60 days -> wg-quick`. The scarce link
is that the offer is reported rather than published.

## The records

`dossier/egress/azure-free-account.json`, `digitalocean.json`,
`akamai-cloud-linode.json`, `oracle-always-free.json`,
`google-cloud-free-trial.json`, `aws-free-tier.json`, `ibm-cloud.json`,
`vultr.json`, `alibaba-cloud-international.json`, `aws-activate.json`,
`cloudflare-for-startups.json`, `digitalocean-startups.json`,
`github-student-developer-pack.json`, `azure-for-students.json`,
`scaleway-instances.json`, `ovhcloud-vps.json`, `hetzner-cloud.json`.

⚠ **No credit was claimed.** Every figure is a page read, and the two rows that would
change with one signup are Oracle and IBM.
