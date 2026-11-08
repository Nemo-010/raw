# Five compute hosts had closed, and every one of them was filed as `paid-only`

- **When:** 2026-10-22T05:07:00Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/kubesail.json`, `jamsocket.json`, `buildjet.json`, `computeruse-cloud.json`, `hyrex.json`, `flowdeploy.json` and `cloudrouter.json` — all `paid-only`, all with a corpus card as their only evidence
- **Superseded by:** those seven records, now `verdict: dead` with the evidence of the death
- **Evidence:** the seven pages read 2026-10-22 through the broker: `kubesail.com`, `jamsocket.com`, `buildjet.com/for-github-actions`, `computeruse.run`, `hyrex.io`, `flowdeploy.com` and `cloudrouter.dev`. Each record in `dossier/compute/` carries the quoted sentence
- **Confidence:** documented

## What we believed

That these seven hosts sold compute and had no free tier. `paid-only` is a verdict
about a price list, so it asserts that a price list exists.

## What we found

Seven different ways for a price list not to exist.

| host | what the page says now |
| --- | --- |
| kubesail.com | "we've made the difficult decision to stop operating our hosted services" |
| jamsocket.com | the team joined Modal; Modal testimonials and no Jamsocket plan |
| buildjet.com | "BuildJet for GitHub Actions has been shut down" |
| computeruse.run | HTTP 404, Vercel `DEPLOYMENT_NOT_FOUND` — the project, not the route |
| hyrex.io | HTTP 402, "This deployment is temporarily paused" |
| flowdeploy.com | a parked domain serving paid link-farm text |
| cloudrouter.dev | the domain now belongs to Manaflow and sells a terminal |

The distinction that matters is `dead` versus `paid-only`. A `paid-only` row tells
a reader "this exists and costs money, move on". A `dead` row tells the next
session "do not spend a wave here". All seven had been saying the first, so each
was a standing invitation to re-check a vendor that had already answered.

Two are worth separating from the other five. **Jamsocket** is not dead so much as
absorbed: Modal bought the team, and Modal is already in this topic with a
`documented` USD 30 monthly Starter allowance. The capability did not vanish; it
moved into a record that is fresh. **Hyrex** returns 402, which is what a host in
arrears looks like, so the pause may end — but the record says `dead` with the
status and the body, which is what a later session needs to tell a revival from a
resurrection.

## How we found it

One read each of the URL the record already carried. None of the seven needed a
search, a different path, or a single guess about where the pricing page might be.
The card had the right URL and nobody had opened it.

## What it cost us

Seven rows in the paid tables that a reader could act on. Cheap to fix, expensive
to have carried: `docs/expansion/compute.md` sequences its work by "the 40
providers a reader would act on tonight", and seven of the 405 were unfindable
answers pretending to be prices.

## What a future session should do differently

⭐ **Check that the price list exists before recording a verdict about it.**
`paid-only` is a claim, and the cheapest test of it is a status code: a 404, a 402
or a parking page is not a paid product, it is an absence. The rule already in
`METHODOLOGY.md` §5.1 — never trust a 200 — has a companion here: a 404 *is*
evidence, and it is evidence of a specific thing.

⚠ **A shutdown notice can sit above a working price table.** BuildJet's page still
shows the runner shapes it used to sell, with the shutdown banner above them. A
reader who greps for prices would find them and conclude the opposite of the
truth.
