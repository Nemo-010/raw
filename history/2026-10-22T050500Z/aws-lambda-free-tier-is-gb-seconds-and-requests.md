# Lambda's free tier is 400,000 GB-seconds a month, not a USD 6.87 credit

- **When:** 2026-10-22T05:05:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/aws-lambda.json` (free tier "USD 6.87 of compute credit each month", verdict `trial-only`)
- **Superseded by:** the same record, rewritten on 2026-10-22
- **Evidence:** `https://aws.amazon.com/lambda/pricing/` read 2026-10-22T04:47:12Z (200, 63,640 bytes)
- **Confidence:** documented

## What we believed

That Lambda's free allowance was a USD 6.87 monthly credit, and that the product
was therefore `trial-only`: something that runs out.

## What we found

The pricing page states the allowance in the units Lambda bills in:

> The monthly compute price is $0.0000166667 per GB-s and the free tier provides
> 400,000 GB-s.
>
> The monthly request price is $0.20 per one million requests and the free tier
> provides 1 million requests per month.

Both recur every month and neither expires. That is a permanent allowance, not a
trial, so the verdict moves to `qualifies-with-caveat`. The page adds one
exclusion that the record did not carry: *"The Lambda free tier does not apply to
functions enabling Provisioned Concurrency."* A reservation is billed from the
first GB-second.

USD 6.87 is the dollar value of the compute half at that rate; it is not what
AWS publishes, and a credit is a different product from a quota. The seed pass
converted a quota into a credit, which is the conflation `docs/expansion/compute.md`
names as an axis the topic has not established.

## How we found it

One read of the pricing page through the broker. The page had never been opened
by this repository: the record's only evidence row named the corpus card.

## What it cost us

The record sat in the `trial-only` group, so the topic README priced Lambda as a
thing that stops. It is the only AWS compute row that qualifies for a recurring
allowance, and it was filed as the opposite.

## What a future session should do differently

⭐ **A quota quoted in money is a conversion, and the conversion loses the
recurrence.** Lambda states GB-seconds and requests because those are what it
meters. When a seed card restates a metered quota as a dollar credit, check which
of the two the vendor published: the credit expires and the quota does not, and
the record's verdict turns on exactly that difference.
