# The credit ladder was re-read, and eight claims moved

- **When:** 2026-10-23T08:05:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/digitalocean.json` (USD 5 of credit for 90 days), `dossier/compute/alibaba-cloud-international.json` (USD 90 over 3 months), `dossier/compute/blaxel.json` (up to USD 200 in credits), `dossier/compute/boxlite-cloud.json` (USD 100 on signup), `dossier/compute/amd-developer-cloud.json` (USD 100 over 30 days), `dossier/inference/together.json` (a one-time starting credit), and `dossier/compute/ovhcloud.json` plus `dossier/compute/ibm-cloud.json`, which both carried `verdict: paid-only` while a free-trial page published a balance
- **Superseded by:** every record above was re-read against the vendor's own page on 2026-10-23. DigitalOcean publishes no current amount, Alibaba Cloud International has replaced its money credit with points and per-product quotas, Blaxel has quotas and no cash, BoxLite has no free tier, AMD gives 25 hours over 10 days, Together denies a free trial, OVHcloud publishes USD 200 for one month, and IBM publishes USD 200 for 30 days
- **Evidence:** `https://www.digitalocean.com/pricing`; `https://www.alibabacloud.com/help/en/user-center/product-overview/learn-about-free-trials`; `https://blaxel.ai/pricing`; `https://www.boxlite.ai/`; `https://www.amd.com/en/developer/resources/cloud-access.html`; `https://docs.together.ai/docs/billing`; `https://www.ovhcloud.com/en/public-cloud/free-trial/`; `https://www.ibm.com/products/cloud/free`. All read 2026-10-23
- **Confidence:** documented

A credit page is a promotion, and a promotion changes without an announcement. The eight
corrections above are two different findings wearing one label.

Six are withdrawals or narrowings. BoxLite's USD 100 was present on 2026-10-22 and absent one
day later. Alibaba replaced a money credit with points. Blaxel's USD 200 became a sandbox quota
with no cash in it. Together states in its own billing documentation that it does not offer a free
trial, which contradicts every guide that quotes a signup credit. AMD halved its grant and cut the
window from 30 days to 10. DigitalOcean's USD 5 was never an offer: it is a sentence inside a
worked example, and the USD 200 that circulates is not on any first-party page that this session
could read.

Two are false negatives. OVHcloud and IBM both carried `paid-only`, because the record was built
from a price list and the balance lives on a separate trial page. That is the same shape as
Snowflake, whose pricing page carries no trial either. A price list answers what a product costs
after the credit, and it is silent about the credit itself.

The lesson is not that the earlier reads were careless. Each one quoted a page that said what the
record claimed. The lesson is that a provider has more than one page, and the page that carries
the number is often not the page a price comparison links to.

One further contradiction is recorded and not resolved. Lightning AI carries `verdict: dead`
because the vendor revoked all user access on 2026-10-16. Its pricing page on 2026-10-23 still
advertises five credits on registration and twenty-five more with a card. A pricing page is not
evidence that a signup completes, so the verdict stands and the record names the conflict. One
registration would settle it.
