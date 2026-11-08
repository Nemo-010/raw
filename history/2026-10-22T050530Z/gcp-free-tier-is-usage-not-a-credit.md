# Google Cloud's free tier is a recurring usage allowance, and the record priced it as a credit

- **When:** 2026-10-22T05:05:30Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/gcp-compute.json`, `dossier/compute/google-agent-engine.json` and `dossier/compute/google-cloud-build.json` — each carried the corpus card's dollar figure where Google publishes a monthly allowance
- **Superseded by:** those three records, rewritten on 2026-10-22
- **Evidence:** `https://cloud.google.com/free/docs/free-cloud-features` and `https://cloud.google.com/free`, both read 2026-10-22
- **Confidence:** documented

## What we believed

That Google Cloud's compute offer was a USD 300 credit inside a 90-day trial, and
that everything on the free tier was therefore `trial-only`.

## What we found

Two products sit side by side, and the seed pass recorded only the first.

The **Free Trial** is the USD 300 credit: valid for 90 days, and if it is spent or
the 90 days pass without upgrading, the billing account closes and the projects
stop. That part is a trial.

The **Free Tier** underneath it is not. `cloud.google.com/free` says it plainly:
*"The free usage limit does not expire."* Compute Engine's row is one
non-preemptible `e2-micro` for the whole of every month in `us-west1`,
`us-central1` or `us-east1`, with 30 GB-months of standard disk and 1 GB of North
American egress.

The detail that decides usability is a sentence the summary page does not carry:

> Your Free Tier `e2-micro` instance limit is by time, not by instance. Each
> month, eligible use of all of your `e2-micro` instances is free until you have
> used a number of hours equal to the total hours in the current month.

So the allowance is **hours**, and one always-on machine consumes the whole
month. Two half-month machines consume exactly the same. A reader who assumed one
instance meant one quota would be surprised by the second machine's bill, and the
exception is stated in the same paragraph: *"GPUs and TPUs are not included."*

Three more allowances were missing from the records because the dollar figure had
replaced them. Agent Engine gets 180,000 vCPU-seconds and 360,000 GiB-seconds a
month, which is 50 vCPU-hours and 100 GiB-hours. Cloud Build gets 2,500
build-minutes a month, which Google calls promotional and subject to change.

## How we found it

Two reads: the pricing page, which carries rates and no allowance, and the
free-tier document, which carries the allowance and no rates. The records had
cited only the first, so the number they needed was never on the page they read.

## What it cost us

Every GCP compute row was grouped with the trials, so the one cloud that gives a
permanent free machine sat in the same bucket as the ones that expire. The
expansion plan's first axis, wall-clock, was unanswerable from the record and is
now the first line of it.

## What a future session should do differently

⭐ **When a cloud publishes two free offers, read both pages.** The trial page is
the marketing one and the free-tier document is the metered one, and a seed pass
that reads the pricing page alone will record the credit and lose the allowance.
The test: does the number recur monthly and never expire? If it does, it is a
tier, and `trial-only` is the wrong verdict.
