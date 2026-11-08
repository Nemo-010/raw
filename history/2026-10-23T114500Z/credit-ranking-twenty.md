# The credit ladder was widened to twenty, and nine more claims moved

- **When:** 2026-10-23T11:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/storage/confluent-cloud.json` (USD 400 for 60 days), `dossier/compute/northflank.json` (a plan named `nf-compute-100-1` at USD 18 a month), `dossier/compute/ovhcloud.json` (`c3-16` at USD 0.2498 an hour), `dossier/databases-kv/cockroachdb-basic.json` (a 30-day trial), `dossier/compute/netmind.json` (USD 100 on a new account), `dossier/compute/digitalocean.json` (USD 200 for 60 days, recorded `unverified`), `dossier/compute/linode.json` (USD 100 for 60 days), `dossier/compute/databricks.json` (USD 400 for 14 days), and `dossier/compute/vultr.json` (`verdict: paid-only`)
- **Superseded by:** `docs/compute/free/credit-ranking.md` (the twenty-row ranking) and the nine records above, each of which now carries the corrected value and the page it came from
- **Evidence:** `https://confluent.cloud/signup`; `https://northflank.com/pricing`; `https://us.ovhcloud.com/public-cloud/prices/`; `https://www.cockroachlabs.com/docs/cockroachcloud/free-trial`; `https://www.netmind.ai/event/freeCredit`; `https://www.digitalocean.com/pricing`; `https://www.akamai.com/cloud/pricing`; `https://www.databricks.com/try-databricks`; `https://www.vultr.com/coupons/`. All read 2026-10-23
- **Confidence:** documented

## What we believed

The committed ranking carried ten rows. Six further offers were believed to be worth USD 100 to
USD 400: Confluent at USD 400 for 60 days, CockroachDB at USD 400 for 30 days, Databricks at USD
400 for 14 days, Vultr as paid-only, and DigitalOcean and Akamai each at USD 200 and USD 100 for 60
days. Northflank's cheapest plan was recorded as `nf-compute-100-1` at USD 18 a month. OVHcloud's
`c3-16` was costed at USD 0.2498 an hour.

## What we found

Six of the nine changed the amount a reader can count on, and three changed only the shape of a
claim that survives.

- **Confluent is 30 days, not 60.** The signup page reads "New signups receive $400 to spend during
  their first 30 days", and the documentation reads "Your free credit expires 30 days after you
  receive it." The 60-day figure appears on neither.
- **Northflank's plan is gone.** The live price list runs `nf-compute-50` at USD 0.01667 an hour
  (0.5 vCPU, 1 GB, USD 12 a month), `nf-compute-100-2` at USD 0.03333 (USD 24), `nf-compute-200`,
  `-400` and `-800-16`. There is no 1 vCPU / 1 GB plan, so USD 20 a month now buys the smallest
  plan and leaves USD 8, and the next one overruns by USD 4.
- **OVHcloud's compute line is cheaper and its disk is unpriced.** `c3-16` is USD 0.2154 an hour,
  USD 155.09 for 30 days; the USD 0.2498 in the earlier ranking added 200 GB of local NVMe at an
  assumed rate. The disk column reads "Local storage low latency" with no size and no footnote, so
  the honest total is a range and the record says so.
- **CockroachDB publishes no trial length.** The page states the USD 400 and the 30-day grace
  period that follows an unclaimed trial, and nothing states how long the trial itself runs. The
  record's 30 days was an inference that read as a fact.
- **NetMind's USD 100 is not on its own page.** `/event/freeCredit` resolves to the homepage, and
  the only archive capture reads "you immediately unlock $ of credit" with the figure missing.
- **DigitalOcean and Akamai publish no current amount.** Both live pages carry a worked example
  ("if you received a $5 credit for 90 days", "if you received a $100 credit for 60 days"). The
  DigitalOcean USD 200 survives only in a 2026-05-15 archive of a URL that now redirects home; the
  Akamai USD 100 survives only as Japanese meta text whose English equivalent is 404.
- **Databricks states a ceiling and a discretion.** "Up to $400 in credits", with "eligibility ...
  the amount of credits (if any), and when any credits expire are solely determined by Databricks
  following account creation". The 14 days is platform access, not a credit expiry.
- **Vultr is not paid-only.** Two promo codes publish USD 250 and USD 300, new customers only, and
  the documentation states the credits last up to 30 days. A payment method is still required
  before any instance exists, so the gate did not soften; the balance appeared.

## How we found it

Two waves of parallel page reads covered sixteen vendor pages and their documentation, then the
rate cards that sizing depends on. Each read returned the quoted sentence and the page it came
from. The pattern in the failures is the same one the previous entry recorded, and it is worth
restating because it repeated here: **the page that carries the number is not the page a price
comparison links to.** Confluent's amount lives on `/signup` and its duration in `/docs`.
Northflank's plan list is a table on the pricing page and its card rule is in the documentation.
OVHcloud's trial is on `/public-cloud/free-trial/` while its rates are on `/public-cloud/prices/`.
Snowflake's USD 400 is on `/signup`, not on its pricing page at all.

A second pattern is new and cheaper to check: **a figure that appears inside an "if you received"
clause is an example, not an offer.** DigitalOcean and Akamai both keep their marketing number
alive as an FAQ hypothesis, and both read like a grant to a skimmer.

A third finding arrived from the same read and did not replace a claim, so it sits here rather
than in the table above. OVHcloud's US price list states a second offer on the page that carries
its rates: USD 200 on a first Public Cloud project plus USD 100 for a first managed database,
valid for 90 days from the day it is applied. The trial page states one month and USD 200. The
two readings differ in both amount and clock, and the 90-day reading buys a smaller machine
because the same money spreads across three times the hours.

One correction changed a record without changing the ranking. Confluent's 30 days is right, and
the record keeps `verdict: fails-quota`, because the balance cannot hold the bytes. A
row in the ranking would have contradicted the record's own verdict, so Confluent is excluded and
the exclusion says why.

## What it cost us

One committed ranking that a reader could have acted on: an OVHcloud total that was USD 25 a month
too high, a Northflank plan that does not exist, and a Confluent window twice its real length. No
account was created, so nothing was spent.

## What a future session should do differently

1. **Read the signup page, not only the pricing page.** The amount is a promotion and promotions
   live on landing pages. A price list answers what the product costs after the credit.
2. **Treat "if you received" as the tell.** A credit described inside a conditional is an example.
   Search the page for the string before ranking it.
3. **Read the plan table, not the plan name.** A record that names a SKU is stale the moment the
   vendor renames it, and a renamed plan changes what the smallest balance buys.
4. **Price the disk separately from the compute.** OVHcloud's Gen3 table omits the local-disk size
   and the footnote, and a total that silently assumes 200 GB is USD 25 a month wrong.
5. **Do not convert a per-unit rate into a shape without saying so.** Daytona publishes
   dollars per vCPU-hour and per GiB-hour; the 4 vCPU / 4 GiB figure in the ranking is arithmetic,
   and the record labels it that way. The same applies to IBM's derived profile rate.
