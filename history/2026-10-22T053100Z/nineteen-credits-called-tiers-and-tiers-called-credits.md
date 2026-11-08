# Nineteen records called a credit a tier, or a tier a credit

- **When:** 2026-10-22T05:31:00Z
- **Status:** superseded
- **Supersedes:** the verdict on 19 `compute` records — 15 moved `qualifies-with-caveat` to `trial-only`, 4 moved `paid-only` to `trial-only`
- **Superseded by:** those records, with the credit, its expiry and its measurement condition quoted
- **Evidence:** the 19 vendor pages read through the broker on 2026-10-22
- **Confidence:** documented

## What we believed

That a record carrying a dollar figure for free usage was a provider with a free
tier. The card gave a number, the number looked like an allowance, and the verdict
followed.

## What we found

A credit that is spent once and a tier that refills are different products, and the
pages say which in the same sentence as the number. Three of the shapes:

**A 30-day clock on a credit.** `celesto`: *"a one-time $5 runtime credit for 30
days, no card required"*. `shardflux`: *"At the cap or after 30 days the account is
on Free, with nothing deleted."* `zo-computer`: *"14-day trial; then recovery
only."* The clock, not the amount, is what a reader plans against.

**A discount instead of an allowance.** `ibm-cloud-vpc` offers *"70% off for 12
months"* on a new VPC. That is a trial by another name and it has a calendar date
on it — 2026-12-31. `kamatera` prices from $4 a month and links a separate
free-trial page rather than granting a tier.

**A credit whose size is the trial.** `runta`: *"$50 trial balance ... 32 vCPU and
64 GiB of memory in aggregate"*. The aggregate cap, not the balance, is what bounds
how many runtimes fit.

The four that moved from `paid-only` to `trial-only` are the mirror error:
`scrapingbee` gives *"1,000 free API credits"*, `cloudbrowser` a 7-day trial,
`depot` 2,000 sandbox minutes inside a 7-day window, and `pipekit` a free trial over
a per-cluster price. Calling those paid-only hid a real trial.

## How we found it

One read each. In every case the word that decided it — "one-time", "30 days",
"expires", "trial" — was within two lines of the number.

## What it cost us

Fifteen rows in the qualifying group that a reader would have planned an
alternative route around, and four in the paid group that they would have
skipped. The `reported-window-holds-at-14-days` decision was right for a reason
this pass keeps confirming: a number without its measurement condition is not a
finding.

## What a future session should do differently

⭐ **The arithmetic that separates a credit from a tier is one division.** Divide
the credit by the cheapest hourly rate. If it comes out in months, it is a trial;
if it is unbounded because the rate is zero, it is a tier. Doing that before writing
`qualifies` would have caught every row in this batch, and it takes one line.

⚠ **Copy the expiry, not just the amount.** "USD 250 of credit" reads as permanent
and "USD 250, redeemable until 2026-12-31, expiring two months after the contract
starts" does not. Both are true of `open-telekom-cloud`; only the second is a fact a
reader can act on.
