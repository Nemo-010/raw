# Compute: the expansion plan

The compute topic prices machines, and establishes what can be run on them for
only part of the catalogue. That is the gap this plan closes. It is not a gap in
coverage: the union of the two source catalogues is 366 providers and 89 census rows, and a
completeness audit matched **366 of 366 and 89 of 89**. Nothing fell out. The gap
is in **depth on the axes that decide usability**, and in whole categories not yet
covered.

## The gap, quantified

| axis | how many of the 405 audited records establish it | why it decides the answer |
|---|---|---|
| wall-clock cap and idle reap | the `Clock` column in `free/always-on-free.md`, ~30 rows | a free tier that reaps in 15 minutes cannot run an agent |
| outbound network policy | stated for a minority | a box that cannot open a socket cannot serve or crawl |
| inbound reachability | stated for a handful | decides whether the box can be an endpoint |
| state durability on stop vs delete | almost nothing | decides whether a stop is a pause or a loss |
| GPU class, and whether it is shared | partially | a "free GPU" that is a queue position is not a GPU |
| whether a free tier is recurring or a one-off credit | mixed | a trial and a tier are different products and the catalogue conflates them |
| measured throughput | 9 records | a sandbox is not a VPS |

**Whole categories not yet covered**, and each is a real option:

| category | examples to establish | why it matters here |
|---|---|---|
| GPU rental below the hyperscaler floor | Vast.ai, RunPod community, TensorDock, Salad, io.net, Akash | inference compute at a price a card-free survey never reaches |
| free-tier CI as general compute | GitHub Actions public-repo runners, Codeberg, Cirrus | already partly in `ci-cd-runners`, but not answered as *compute*: what reaps it, and what can it reach |
| university and national HPC with open application | INCITE, ACCESS, EuroHPC, PRACE successor | INCITE (200 TB, open to foreigners, annual application) is the one known row |
| bare-metal and dedicated at the low end | Hetzner auction, OVH Kimsufi, SoYouStart, Wholesale Internet | a rented dedicated box at EUR 30 is the floor above a VPS and below a managed platform |
| edge function runtimes with real CPU time | Cloudflare Workers, Deno Deploy, Vercel Edge, Fastly Compute | the CPU-second cap is the constraint and it is stated in a unit nobody converts |
| container hosts with a persistent volume | Fly machines, Railway, Render, Koyeb, Northflank | persistence is the axis not yet recorded |

## The verification gate

A compute record is not usable until these are answered, and a provider that will
not answer them is a provider whose section says so:

1. **Shape** — vCPU, memory, disk, GPU class and whether it is shared or
   exclusive.
2. **Clock** — wall-clock cap, idle-reap window, and whether the clock resets on
   activity or on creation.
3. **State** — ephemeral root, attached volume, git remote, nothing. And what
   happens to it on stop versus on delete.
4. **Network** — outbound permitted? which ports? inbound possible?
5. **Identity** — card, phone, email, anonymous.
6. **Product class** — recurring tier, expiring trial credit, or a permanently
   free allowance. Three different products.
7. **Cost at the duty cycle** — not a monthly list price. A sandbox bills while
   it runs, so the price is a function of hold time: price at 1 h/day, 10 h/day
   and 24/7, and say which is cheapest at each.

⛔ **A price without a duty cycle is not a price.** This is the axis a list price
flattens, and the reason the cheapest row in the source catalogue was a provider
that had closed (Run Cloud). Every paid figure must state the hold time it
assumes.

## The measurement loop

Compute rots slowest of the three expansion areas — a free tier rarely changes
within a quarter — so the loop is quarterly, not weekly. What changes faster is
**availability**: a provider closes, a free tier ends, a region fills.

⚠ **`scripts/discover/compute-census.sh` is not built.** The census is a tools
change with an offline self-test (`docs/research-protocol.md` section 2). Until it
exists, the liveness half is `python scripts/probe/probe.py` over a URL list
written from `scripts/fr`, and the discovery half is the registered lists of
`scripts/sources/aggregators.tsv` (issue #30).

```text
# quarterly, once the census exists
sh scripts/discover/compute-census.sh --from dossier/compute/ --out .tmp/session-<id>/discover/compute/
while read -r u; do python scripts/probe/probe.py "$u" --out .tmp/session-<id>/probe; done < .tmp/session-<id>/discover/compute/health.txt
```

One probe per URL: `--urls-file` with `--concurrency N` is the throughput benchmark of `probe.py`, which probes
only the first N URLs.

Two checks, different questions:

- **Liveness** — does the signup page still exist and still offer the tier the
  record claims? A 404 on the pricing page is a dead provider, not a network blip.
- **Reap policy** — does the limits page still state the clock? This is the field
  most likely to change silently, because a provider can tighten a reap window
  without announcing it.

⚠ **Do not probe by creating resources.** A liveness check reads a page. The
moment a loop starts provisioning machines to test them, it has become a cost and
an account that no agent may open (`AGENTS.md` section 2 rule 13). Where a reap
policy can only be learned by holding a machine, the record says
`unverified: requires provisioning`, and the step goes to the open issue labelled
`rq:operator`.

## The discovery method

| source | query or route | what it yields |
|---|---|---|
| the source catalogues | read once; do not re-read | the 366-provider base |
| `awesome-*` lists on GitHub | `search/repositories?q=awesome+free+hosting`, then each list's git log | new entrants, dated |
| Hacker News and Lobsters | search for "free tier", "sandbox", "we're shutting down" | both launches and deaths, which matter equally |
| the cheap-VPS forums | `lowendtalk.com`, `hostloc.com` via search snippets | regional providers the English lists miss |
| provider changelogs | each vendor's `/changelog` or `/status` | the only early warning of a tier change |
| the `peli-cloud` crosscheck driver | re-run it against current pages | the source catalogue's own method |

## Sequencing

1. **Fill the seven axes for the 40 providers a reader would act on tonight.**
   Depth on 40 beats a row for 400.
2. **Add the GPU-rental category.** It is the largest whole gap and the inference
   need makes it urgent.
3. **Answer CI-as-compute properly**, cross-referencing `ci-cd-runners` rather
   than duplicating it.
4. **Re-price every paid figure at three duty cycles.**
5. **Then discover.** Adding providers to a catalogue whose axes are incomplete
   only makes the incompleteness larger.

## What would make this plan wrong

If free-tier access closes — a card requirement appears, an account is suspended,
an identity gate tightens — the free sandbox lane collapses and the paid dedicated
lane becomes the whole topic. The signal to watch: **the number of `qualifies` compute
records that acquire a `fails-identity` verdict.** Three in a quarter would invert this
plan's priority order: GPU rental and dedicated boxes first, free tiers as a footnote.

⛔ **This plan does not invert on hardware ownership.** The corpus prices no
hardware purchase, so that scenario is not a branch to plan for.
