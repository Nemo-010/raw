# The USD 6.49 floor was wrong, and so were four prices under it

- **When:** 2026-10-24T02:15:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/paid/README.md`, which states "the floor is a rented box at USD 6.49 a month, and everything below that figure in this topic is a free tier, a credit, or a product that has been withdrawn"; `docs/compute/paid/vps-monthly.md`, whose entry row is Hetzner CX23 at USD 6.49; `docs/compute/paid/micro.md`, whose lowest rows carry no renewal price and one campaign rate; and the `hetzner-cloud`, `digitalocean`, `netcup`, `serverhost` and `greencloudvps` records
- **Superseded by:** every row below was read at the vendor's own page on 2026-10-24. The claim that nothing under USD 5 exists is refuted by a single vendor page: GreenCloudVPS sells 8 GiB, 4 vCPU and 60 GB for USD 45.00 a year.
- **Evidence:** the specific page and sentence for each row is in that row's dossier record, and the lane reports at `.tmp/compute-2026-10-24/lanes/L02-one-to-five/report.md` and `L01-sub1-monthly/report.md`
- **Confidence:** documented

## What the pages say now

| claim | was | is | what took it away |
| --- | --- | --- | --- |
| the cheapest always-on box | USD 6.49, Hetzner CX23 | **USD 3.75**, GreenCloudVPS BudgetKVM, 8 GiB / 4 vCPU / 60 GB / 8 TB, USD 45.00 a year | `greencloudvps.com` plan cards, read 2026-10-24 |
| Hetzner CX23 | USD 6.49, the recommended entry | **EUR 5.99 (USD 6.70)** and marked "not available" | `hetzner.com/cloud`, read 2026-10-24 |
| Hetzner CX22 at "about EUR 3.79" | the cheap default in several documents | no such rung on the page; the cost-optimised tier is CX23 at EUR 5.99 and CAX11 at EUR 6.49 | the same page |
| DigitalOcean's USD 4 droplet | 1 GiB | **512 MiB**; 1 GiB is USD 6.00 | `digitalocean.com/pricing`, read 2026-10-24 |
| netcup VPS 1000 G11 | the entry rung | the page sells **G12.5**: VPS 500 at EUR 8.26 and VPS 1000 at EUR 14.50 | `netcup.com`, read 2026-10-24 |
| ServerHost USD 16.99 a year | a price | a **code-gated campaign rate** (`FBAD2GB2026`); the homepage advertises "from USD 3/mo" and no renewal is published | `serverhost.com`, read 2026-10-24 |
| RackNerd's cheapest | USD 21.99 a year | confirmed at USD 21.99 a year; the USD 10.99 figure that circulates is not on the page | `racknerd.com/specials`, read 2026-10-24 |

## The two that matter

**The floor claim was a scope error, not a stale price.** `paid/README.md` and
`paid/vps-monthly.md` priced the mainstream set and then wrote a sentence about the market.
The low-end hosts in the same topic's `micro.md` were already under the figure the front page
called the floor, so the topic contradicted itself on its own first page. The fix is the
sentence and the table, not a new discovery.

**The cheapest row is still not the best row.** ServerHost's USD 1.42 for 2 GiB is
USD 0.71 per GiB-month; GreenCloudVPS's USD 3.75 for 8 GiB is USD 0.47. The larger invoice
returns four times the memory for 2.6 times the money, and it is the row a daily driver
should take. That is the same arithmetic `micro.md` already stated, applied to a price the
front page said did not exist.
