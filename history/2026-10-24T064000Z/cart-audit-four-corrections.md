# The cart audit: four recommendations were wrong, and nine pages charged a different price

- **When:** 2026-10-24T06:40:00Z
- **Status:** corrected
- **Supersedes:** the Q1 paid pick (**VolpaByte Ryzen KVM 8 GB**), the Q1 runner-up (**HostBrr Value 8GB** at USD 4.58), the Q2 micro pick ordering, the claim that no sub-dollar machine has a dedicated IPv4, and the statement that DediRock was not worth listing
- **Superseded by:** eight research lanes (`.tmp/compute-2026-10-24/nat/N01b`, `N02`, `N03`, `N05`, `N07`, `N08`, `N09`, `N10`) plus the parent session's browser verification
- **Evidence:** each record's `evidence[]`; the worked failures are in `.tmp/compute-2026-10-24/nat/PARENT-dedirock-verdict.md`, `PARENT-dedirock-verified.md` and `PARENT-cart-verification.md`
- **Confidence:** documented

## What this pass was for

The operator reported two things about the compute corpus: that many free credits demand a
credit card with a large hold, and that there is "just too many false information in there".
One example: Daytona written as a nothing burger when USD 200 of its credit runs a
full VM for a month with no card — and asked for ten free tiers, ten beefy paid and ten
micro paid, each with a direct cart link.

The method that found the errors was not a re-read of the pages. It was **following the
vendor's own "Order now" href and reading what the cart charged**. That single step
contradicted four published recommendations.

## The four corrections

**1. VolpaByte Ryzen KVM 8 GB is dead, and it was the top recommendation.**

Its marketing page still renders "Ryzen KVM 8 GB EUR 4,99 pro Monat", 6 AMD Ryzen vCores and
8 GB DDR4-3200 ECC. Its own "Jetzt bestellen" href is
`dashboard/index.php?rp=/store/vps/ryzen-kvm-8-gb`, which redirects to `/store` and renders:

> Could not load any product groups.

The plan cannot be bought at the advertised price. `verdict` moved from
`qualifies-with-caveat` to **`dead`**. This was independently observed by lane N07 and
re-read by the parent session.

**2. HostBrr Value 8GB is not the machine the corpus described.**

The record said 8 vCPU and USD 4.58. The order page says **2 vCore** and **USD 5.50 a month
or USD 55.00 a year**. USD 4.58 is the annual rate divided by twelve, so the row is still
under the line on annual prepay, but the monthly list is over it and the shape was wrong by
a factor of four. Separately, HostBrr's marketing "Deploy Server" button points at
`pricing_id=1166` and renders `Subtotal: $0.00 USD ... Total Due Today: $0.00 USD`; the
working link is the group page.

**3. DediRock is both a fossil and a live offer, at two different URLs.**

The Black Friday page advertises a USD 9.88/year Saver. Its Order href
`…/store/promo-vp/promo-vps-saver-ny-bf` lands on a category listing whose cheapest line is
**USD 5.99 per month** for a different shape — no error, no sold-out marker. That is a
fossil, and it is what the corpus had recorded.

But the standing promo SKU at `…/store/promo-vp/promo-vps-special-ny` is a different
product and it **does** sell. The Cloudflare challenge was cleared and the rendered
order form was read directly: **2 GiB / 1 vCPU / 30 GB / 2 TB / 1 IPv4, "Annually: $9.88
USD", "$9.88 USD Total Due Today"**.

So the earlier verdict was right about the URL it checked and wrong as a statement about the
host. The corpus had no record for the SKU that works.

**4. The USD 50 card hold does not exist anywhere in this corpus.**

The largest hold found remains Koyeb at USD 29. The typical is USD 1. Oracle's is USD 1.00.
The operator's complaint is about a real pattern in the wider market; it is not what these
records show, and the page now says so with the numbers.

## What the cart audit found across 42 rows

Lane N07 followed the order link on every qualifying row at or under USD 5 and read the
destination:

| verdict | n | meaning |
| --- | --- | --- |
| cart prices the plan | 16 | link is good |
| cart prices something else, is out of stock, or is walled | 14 | link is bad |
| no price readable by GET | 12 | JS shell, `action=add`, or no SKU |

**Nine were fossils of the DediRock class** — the link resolves to a different product or to
nothing: `luo-cloud-lxc-nat` (CNY 1.50 advertised, CNY 25.00 category rendered, 16.7×),
`natkvm-nat-lxc`, `dedirock` ×2, `softshellweb-lxc-ipv6-only`, `volpabyte-ryzen-kvm-8gb`,
`62yun-promo-vds`, `firstbyte-msk-kvm-start`, `alibaba-swas-intl`.

Three were **out of stock but correctly linked** — a stock fact, not a broken link:
`vds6-v6-1`, `greencloud-budget-kvm-8gb`, `cloudfanatic-standard-1gb`.

## What replaced them

**Q1 beefy:** **AlphaVPS C6G** returns as the pick, at EUR 50.90 a year for 3 vCPU / 6 GiB /
55 GB NVMe / 6 TB / 1 IPv4 + a /64. It is the only row where a real browser read the cart,
it priced exactly as advertised, and it is in stock. ⚠ **Two of seven locations only** —
Sofia and Los Angeles; London, Nuremberg, Dallas, New York and Seattle render "Out of
stock".

**Best value per gigabyte:** **HostBrr ECO 4 GB** at USD 32.50 a year (USD 2.71/mo), cart
prices it exactly.

**Q2 micro:** **DediRock Promo Special NY at USD 0.82** is now the WireGuard pick and the
only sub-dollar row with a **dedicated IPv4** and **2 GiB** — four times the next-largest
machine in the band. **TierHive at USD 0.10** stays the monitor.

**Free tiers:** the ten are reordered around the card column. **Daytona moves from sixth to
fourth** with the arithmetic the operator supplied: USD 200 is 749 hours of a 4 vCPU / 4 GiB
VM, 31.2 days, no card. `freeshell.de` enters at ninth — 42 GB of real disk, a listening
port and cron, gated on a **postcard to Germany** rather than a card.

## What was added that the corpus did not have

- **NAT records: 5 → 29.** The largest hole in the corpus.
- **54 new provider records**, dossier 1,255 → 1,309, zero schema errors.
- **IPv6-only sellers under USD 2:** DeluxHost at USD 0.50/mo (a /64, all ports open) and
  Skhron at EUR 1.69 + EUR 0.65 for an IPv4 add-on, with a routed /64 and a free /56.
- **Seasonal pages tested: 11 pages, 41 order links, one seller.** The hypothesis that old
  Black Friday pages still sell held for **zero** Black Friday pages and for one standing
  promo SKU the BF page never links to.

## What this pass did not do

- **No account was created and no order placed anywhere.** Every row is `documented`.
  Twelve rows are `unknown` on the cart because settling them needs a browser session or an
  account.
- **Hostodo's Black Friday 2025 remains unverified.** A control request with a bogus plan
  code returned **byte-identical** output, so its HTTP 200 proves nothing.
- **DediRock's renewal is not published.** USD 9.88 is year one; year two is unknown.
- **Datalix's cart arrived logged in as another person** (`Eingeloggt als
  florian@kolbs.email`), so its `cart_works` is weaker than the other rows.

## A correction to this correction: VolpaByte is not dead

This entry first recorded VolpaByte as `dead`, on the strength of nine order links that each
rendered **"Could not load any product groups."** That verdict was wrong, and the way it was
wrong matters more than the verdict did.

**A stateless fetch makes a healthy WHMCS store look dead.** Lane N04 found it: carry a
cookie jar from `volpabyte.net/` first, and the identical URL redirects to
`cart.php?a=confproduct&i=0` and prints all four billing cycles. The parent session then ran
the control both ways:

| request | final URL | body |
| --- | --- | --- |
| no cookie jar (what the broker does) | `…/dashboard/index.php?rp=/store` | **"Could not load any product groups"**, zero prices |
| jar warmed from the homepage | `…/dashboard/cart.php?a=confproduct&i=0` | **EUR 4,99 / 14,22 / 26,95 / 50,90**, full configurator |

Same URL, same minute, opposite answers. The vendor never changed anything.

The same artefact hit AlphaVPS: `cart.php?a=add&pid=509` bounces to the store list without a
jar and lands on the configurator with one. **Two research lanes and this session each
published a "dead" verdict produced by the tool, not by the vendor.**

### What was restored

**VolpaByte Ryzen KVM 8 GB is the beefy pick again**, at EUR 50.90 a year for 6 AMD Ryzen
vCores / 8 GiB ECC / 100 GB / unlimited traffic / 1 IPv4 + a /64, in Frankfurt. Its
`verdict` moved `dead` → `qualifies`, and `extras.cart_works` is `yes`.

⚠ Its renewal is still unstated. The cart prints four cycles and says nothing about year
two; EUR 4.99 monthly is the only evidence for month 13, and that is an inference.

### The guard this produced

A note would not have stopped this, because three independent readers hit it in one session.
`scripts/probe/cartcheck.py` now does the read with a jar and exits `0` only when the cart
priced something. It was tested both ways before being documented: `priced` and exit 0 on
VolpaByte, `error` and exit 1 on the DediRock fossil, `no-price` and exit 1 on a page with no
cart. The rule is now mechanical: **a cart is only dead when it fails with a jar.**

### Two other verdicts this pass withdrew

- **GreenCloudVPS's "USD 40.00/mo list, 10.7× worst case"** — that list price does not exist
  on the page. Withdrawn as unverified. The honest statement is USD 3.75 now and month 13
  unknown.
- **TierHive's "USD 0.10 with a cart"** — no cart exists. Every Deploy button, Micro
  included, points at `control.tierhive.com/register`, which redirects to `/login`. USD 0.10
  is a pricing-card figure.

## Four more corrections, from browser screenshots

Four vendor pages were cleared in a real browser on 2026-10-24. Each one changed a
record.

### 1. Cheap-Host's plan table is read, and its top rung is the biggest NAT machine found

`cheap-host.onl/nat-vps/?lang=en` renders **four** rungs, not the one the corpus carried:

| rung | RUB/mo | USD/mo | vCPU | RAM | NVMe |
| --- | --- | --- | --- | --- | --- |
| NAT Start | 59 | 0.73 | 1 | 1 GB | 10 GB |
| NAT Base | 99 | 1.22 | 1 | 2 GB | 15 GB |
| NAT Pro | 199 | **2.45** | 2 | **4 GB** | 25 GB |
| NAT Plus | 349 | 4.29 | 4 | **8 GB** | 50 GB |

All four: unlimited traffic, 100 Mbit/s, Germany, shared IPv4 with **no IPv6**,
**999 TCP/UDP ports + SSH**, **port 25 blocked**.

The record previously said `nat_config: "not described"` and left UDP unstated. Both are now
settled from the plan card. **NAT Pro at USD 2.45 for 4 GB and 2 vCPU is more machine than
any other NAT row in the corpus under USD 3**, and 999 forwarded ports is the widest block
found anywhere.

Two things still keep it out of the ranked ten: every "Choose plan" button routes to the
account panel, so **no price renders before login** (`cart_works: unknown`), and its rails
are SBP, SberPay, YooMoney, MIR and crypto — **no card-network rail**.

### 2. VolpaByte charges 19% VAT, and the corpus said it did not

The order summary reads `Monthly: €4,19 EUR`, `VAT @ 19.00%: €0,80 EUR`, `€4,99 EUR Total Due
Today`. So **EUR 4.99 is gross and EUR 4.19 is net**, and there is no country selector to make
the VAT fall away for a non-EU buyer.

This record had said "no VAT line and no country selector". The second half was right and the
first was wrong. Corrected, with the arithmetic in `extras.price_ex_vat_eur` and
`extras.vat_pct`.

### 3. RackNerd's Black Friday 2025 is confirmed out of stock at the product URL itself

`my.racknerd.com/index.php?rp=store/blackfriday2025/1-gb-kvm-vps-black-friday-2025` renders:

> Oops, there's a problem… **Out of Stock** — The plan you selected is out of stock and not
> available for ordering at this time.

Previously this rested on a `0 Available` counter elsewhere in the store. It now rests on the
product page refusing the plan, which is the stronger form of the same finding.

### 4. Hostodo stays unverified, and now for a stated reason

The deploy console loads but prints no price, and a control request with a bogus plan code
returned byte-identical output. Reading the price needs a signed-in session, and this corpus
creates no accounts. Recorded `unverified` rather than dead.

## The last two lanes: AWS has no card gate, and a dissolved company still sells

### AWS Free plan — the corpus was wrong about the card

The corpus assumed an AWS account means a credit card. **AWS's own signup page says
otherwise**, and the parent session re-read the sentence to confirm it:

> With Sign up for AWS (new), most new customers will not be required to provide a payment
> method to get started.

> Our verification process holds USD $1 (or equivalent) for 3-5 days to verify your account
> and help prevent fraud; however, your card will not be charged.

So the gate is: **no card for most new customers**, and a **USD 1 hold for 3–5 days** when one
is asked for. The machine is a `t4g.small` — 2 vCPU, 2 GiB of Graviton — free for **750 hours
a month**, plus USD 100 of credits on signup and up to USD 100 more.

⛔ **The end is hard:** *"Your free account plan ends after six months or when your credits are
fully used — whichever occurs first. After your free account plan expires, your account closes
automatically."* That is a six-month stop, not a renewal, and AWS retains content for 90 days.

AWS enters the free-tier ten at **fourth**, displacing Waifly to eleventh.

### Oracle's USD 1.00 hold is withdrawn

Oracle's signup page states that a hold exists and **publishes no amount**. The USD 1.00 figure
this corpus carried is withdrawn; the honest value is a dash. That matters because the hold
amount is the thing in question.

### The largest hold found is CHF 20, not USD 50

Across every free tier read: Infomaniak at **CHF 20** (~USD 22), Koyeb at USD 29, and USD 1
authorisations at AWS, Alibaba and Huawei. **Nothing in this corpus holds USD 50.**

### KhanWebHost: a live store behind a dissolved company

The UK company KhanWebHost **was dissolved on 2023-12-26** and the store has kept selling
annual plans under that name since. The price is real — USD 5.99 a year for 256 MB with TCP
and UDP stated — and the entity is not.

This is the clearest case in the corpus of a finding that is technically true and commercially
worthless, and it is the second such case: a recommended provider's UK company was dissolved
in 2023 while it kept selling annual plans. Both are now recorded with the dissolution date.

### Two more clean micro rows

**Privex VNano SE at USD 0.99** — 256 MB, 5 GB, a /64 with DNS64/NAT64, **crypto only, no
card**, and a real AS210083 holder. **Mikrus at USD 0.74** — 384 MB, 5 GB, **UDP stated**,
IPv6-mostly, VAT PL6821639338. Mikrus's free rung is a queue and lottery, so only the paid one
is reliable.
