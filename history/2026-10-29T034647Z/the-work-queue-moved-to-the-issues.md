# The work queue moved from BRIEF.md to the rq:research issues

- **When:** 2026-10-29T03:46:47Z
- **Status:** decided
- **Supersedes:** `BRIEF.md` section 5, "Open, ranked", "Recently closed" and the text of "Known red checks", as they were at commit 80b0dce
- **Superseded by:** the open issues labelled `rq:research`, the open issue labelled `rq:operator` (#58), and `BRIEF.md` section 5
- **Evidence:** the operator's rulings on the readiness audit of 2026-10-29, stated in the pull request that made this change
- **Confidence:** documented

## What we believed

`BRIEF.md` section 5 was "the only queue". A session picked a unit there and wrote its handover there,
and the research protocol pointed a parent at it after each run.

## What we found

The queue lived in three places: the numbered items of `BRIEF.md` section 5, the files in `queue/`,
and the open `rq:research` issues. The items overlapped and disagreed. The research harness writes
records, ledger lines and queue files through one program on a run branch, and nothing in it writes
`BRIEF.md`, so a run either left the file stale or edited it by hand on a branch that other runs also
edited. Several queue items asked for a sign-up or a purchase, which no agent may make.

## How we found it

An independent audit of every instruction a research agent reads (findings I-08, I-10, I-14 and I-33).

## What it cost us

Twelve files in `queue/` had no issue that named them, so no run would plan them. A parent that
followed `BRIEF.md` could have planned a sign-up or an order.

## What a future session should do differently

Take the work from an open `rq:research` issue. Do not add a work item to `BRIEF.md`. A step that
needs an account, a purchase or a real send goes to the `rq:operator` issue. The handover of a run is
its pull request body and the follow-up issue that `scripts/rq merge` files.

## Where each item went

| item of the old queue | where it is now |
| --- | --- |
| 0. prefer a thin topic | `BRIEF.md` section 5 keeps the rule; the table of section 2 counts the records |
| 1. storage has never had a byte written | #24 |
| 2. coding-subs: one subscription each to StepFun and OpenCode | #58 (operator) |
| 3. inference: build the probe loop | #35 |
| 4. netdisk-pan: auto-discovery | #37 |
| 5. compute: one account and one job; the Civo sign-up; the six orders; `yabs.sh` | #58 (operator) |
| 5. compute: discovery from the registered lists | #30 |
| 5. compute: renewal prices, stock, and the Windows page and cart reads | #28 |
| 6. egress: the TCPShield sign-up, one handshake, one real send | #58 (operator) |
| 6. egress: the names of the tunnel and offer lists | #45 |
| 7. databases-kv: one provider run to its limit | #58 (operator) |
| 8. domains-dns: the deSEC sign-up and count | #58 (operator); the rest of the topic is #39 |
| 9. five compute leads | #30 |
| 10. debrid: CloudPipe, TorBox and Real-Debrid | #58 (operator) |
| 10. debrid: four storage records, about 207 names | #46 |
| 11. ip-proxy: the `fetch()` test, the purchases, the ClientHello fields | #58 (operator) |
| 11. ip-proxy: BYOIP, the seen list, the prefix brokers | #44 |
| 12. (a) held clauses, (c) duplicates and entities | #47 |
| 12. (b) parse coverage | #59 |
| 12. (d) guides on the wiki | #58 (operator decision) |
| 13. the queued re-run of CNB, Baidu AI Studio and SimpFun, and the other queue items | #26 (the `0424` and `0913` compute items), #33 (`20261028-0433-expand-inference-u08-q05`); #30 (the LowEndTalk threads) |
| 14. dev-services and data-apis | #31 and #43 |

## The queue as it stood

The rest of this file is the text of `BRIEF.md` section 5 at commit 80b0dce, unchanged except that
each relative link now starts from this folder. This entry is evidence for the "Why" sections of the
issues; a parent never plans from it.

### Open, ranked

0. ⛔ **The queue is not a storage queue, and storage is not the priority.** By word
   count storage is 42% of this corpus (145,931 of 348,000) because it was researched
   longest, not because it matters most. Every free or nearly free resource is
   in scope, and the thinnest topics are where the leverage is: `domains-dns` has
   14 records, `ci-cd-runners` 18, `coding-subs` 18, `inference` 21, `databases-kv` 23.
   ⭐ **A session with a free slot should prefer a thin topic over another storage
   refinement.** Storage is over-served and the others are under-served.

1. **`storage` has never had a byte written to it.** The rung mislabelling is
   closed (348 to 0) and every record is fresh, but storage holds **1 of 1,709
   `measured` records** and no record carries a probe of a chunked write. Every cap
   in this topic is a page read. The work is not more providers: it is one shard
   written to one provider and read back, hashed, at 25 MiB, then at the largest cap
   a provider will take. Downstream: the whole chunk-and-replicate pattern, which is
   described in `free/host-economics.md` and never once exercised.
2. **`coding-subs` was reviewed and fixed; it is now current, not five weeks stale.**
   The adversarial review's six blockers are closed and every record was re-audited
   against its own capture. What remains is a measurement rather than a page: no
   account was created in this topic, so every quota is `documented` and none is
   `measured`. One subscription to StepFun Flash Plus at USD 9.99 and one to OpenCode
   Go at USD 10 would convert the two cheapest rows. Downstream: the paid lane's
   ranking, which currently rests on published pages alone.
3. **`inference` needs its probe loop built.** `docs/expansion/free-inference.md`
   specifies it and `scripts/probe/inference-sweep.py` does not exist. This is
   the highest-value script in the repository, because nothing else renews.
4. **`netdisk-pan` auto-discovery.** Specified in full at
   `docs/netdisk-pan/auto-discovery.md`, unbuilt. Two of its inputs were never
   measured — run them by hand before wiring them in.
5. **`compute` went from 405 records to 1,154 across five waves; measurement is still the
   whole gap, and discovery is not finished either.** Later waves added 1,154 minus 405
   records over 39 lanes, and 17 documents, including the cheap-VPS catalogue, the storage
   per-TB page and the two credit pages.
   ⛔ **Eight of 1,154 records are `measured`.** Every other claim is a page somebody read.
   No account was created in any wave and no GPU credit was spent, so every
   registration gate is vendor prose rather than a completed signup.
   ⭐ **The next unit is one account, not one provider**: register for the single most
   valuable free lane, run a job to its limit, and record where it stopped. That is the
   only move that changes the topic's evidence rung, and identity is unread for every one
   of the 114 tracker hosts and the 25 feed hosts.
   ⭐ **The credit ladder is now twenty rows, ranked and re-read** in
   `docs/compute/free/credit-ranking.md` (2026-10-23). Seventeen claims moved across two
   passes, including two false `paid-only` verdicts. The page also answers the operator's
   question directly: ten of the twenty hold a process open 24/7, each row carries the shape
   that spends the balance without overrunning, what the remainder buys, and what two equal
   machines cost against one. Civo is still the cheapest next signup: USD 250, 31 days, and a
   verified card, which would convert the best-evidenced gate in the table from `documented`
   to `measured`.
   ⭐ **Discovery is tracked, not assumed.** `scripts/sources/aggregators.tsv` lists every
   source that publishes other providers with a cadence and a last-diff date, and the gate's
   `sources` check fails on an undiffed or overdue one. The queue it measures is large:
   ServerHunter lists 971 providers and 857 are unrecorded, computeprices 116 and 51,
   vpsbenchmarks 76 and 46. Start there rather than from a blank search.
   ⭐ **`docs/compute/watchlist.md` is the reading list behind that registry**, naming what
   each source is good for and what it is not. **`sandboxprices.com` was added on 2026-10-24**
   as a 30-day price index: it serves its whole 160-product catalogue as JSON at
   `https://api.sandboxprices.com/api/products`, which is how it is diffed, and 86 of the 160
   were already recorded. ⛔ **Its headline month is 200 active hours, not 730**, so every
   time-based rate it prints is optimistic by up to 3.65 times. That single fact invalidated
   three candidate rows in one lane.
   ⛔ **The Windows VPS lane has been swept, and the sweep did not move the floor.**
   The first two passes had covered 11 vendors and then 6. The third pass ran sixteen
   lanes on 2026-10-26, one per segment, and read at least 316 distinct provider labels:
   the offer archives, US budget hosts, Russia and the CIS, Europe, the Windows
   specialists, the RDP resellers, Turkey and MENA, Asia-Pacific, rented dedicated
   servers, the hyperscalers, hosted desktops, WHMCS and wholesale resellers, the price
   aggregators, the install and policy checks, the licence channel and a cart audit. That
   count is the distinct first-column labels of the lane and merge tables in
   `.tmp/win-swarm/`, case-folded, with plan suffixes dropped, spelling variants of one
   brand merged and directory sites excluded. The
   Windows-specialist merge alone ranks 58 rows that clear 16 GiB, 4 vCPU and 50 GB.
   Every lane kept the licence path per row and no row was re-ranked on a forum price
   alone. What the sweep changed is in
   [`history/2026-10-26T133000Z/windows-breadth-sweep.md`](../../history/2026-10-26T133000Z/windows-breadth-sweep.md).
   ⭐ **The Windows floor is a machine price, not a licence price**, and that
   distinction is now part of every row. No lane found a 16 GiB machine under
   USD 8.11 a month. The one claim that could have, VDSina's USD 4.08, is a per-day
   rate worth about USD 122 a month.
   ⛔ **The measurement gap is unchanged and is now the only thing that matters.** Four
   documents answer the operator's four questions and every row in them is `documented`.
   Nothing was bought and nothing was booted, so no row carries a probe. Six moves would
   each raise one answer's rung:
   - **One Gullo's order and one `wg-quick` handshake**, which settles whether the 20
     forwarded ports really carry UDP. It is the single load-bearing claim under the whole of
     `paid/under-one.md` and it costs USD 3.50. A user reports `wireguard-go` running there,
     which is a report and not a measurement.
   - **One luo_cloud order at CNY 1.50**, which settles whether a monthly USD 0.22 box is real
     and whether its 20 NAT ports carry UDP. It is the cheapest test in the corpus.
   - **One GreenCloudVPS order**, to see whether the clearance 8 GiB rung still exists and
     what the invoice says. It is USD 45 and it is the Q1 answer.
   - **One Daytona signup**, to see whether a Tier 1 account can create a VM sandbox at all
     and what its egress allowlist blocks. It costs nothing and it decides Q3.
   - **One `yabs.sh` run** on any of these hosts, which is the only thing that turns the
     `reported` Geekbench table in `paid/under-five.md` into a measurement. The vCPU count is
     a weak predictor of throughput: nine 2 vCPU rows span 300 to 2,242 single-core points.
   - **One Rabisu order at USD 10.99**, which settles whether the FAQ sentence
     "all Windows VPS plans include a genuine Windows Server license" survives the
     first renewal. The configurator prices the Windows image at zero on a 6 core,
     16 GiB, 120 GB plan, and USD 8.79 a month on the annual term is the cheapest
     row with a licence claim in `paid/windows-vps.md`. The floor itself is
     Layer7 at USD 8.11 a month on its annual cycle. One HOSTKEY cart at
     EUR 14.00 plus the unpublished licence is the second move; a surcharge
     under EUR 5.00 makes it the cheapest 8 vCPU row.

   ⚠ **Six of the Q1 and Q2 rows publish no renewal price**: GreenCloudVPS, NATKVM,
   Cheap-Host, CloudCone, RackNerd and ServerHost. None carries a strike-through or a promo
   badge either, which is why they are recorded as list rates, but a renewal figure would
   settle it and only AlphaVPS publishes one.
   ⚠ **The low-end market is the thinnest evidenced sub-topic.** 57 to 58 records are
   `dead` in the counts those passes took, most of them small hosts that vanished; the
   count moved between passes and this file does not re-date records to settle it. The
   generated topic table above carries the record-derived figure. The forum lanes found
   that a promo price is rarely a renewal price. A price row without a renewal figure is
   incomplete, and `docs/compute/paid/micro.md` says so in every row that lacks one.
   **Stock is the second fragility**: the Q1 winner carried 21 units in 4 of 20
   locations, and Datalix has 21 of its 24 rungs marked sold out.

   ⭐ **The Windows VPS question is answered at the machine rung, and sixteen lanes
   did not move the answer.** [`docs/compute/paid/windows-vps.md`](../../docs/compute/paid/windows-vps.md)
   ranks the cheapest machines that can boot Windows. Layer7 holds the floor at
   EUR 9.06 a month (USD 10.14), or EUR 86.97 a year (USD 8.11 a month, USD 97.35
   first payment), for 4 cores, 16 GiB and 80 GB with an evaluation image.
   Saganetwork is the cheapest row a buyer can start on a monthly term, at USD 8.23
   ex VAT and USD 9.88 paid, for 6 cores, 16 GiB and 120 GB, with its Windows path
   unverified. Rabisu is the cheapest row with a Windows image at no surcharge, at
   USD 10.99 a month or USD 8.79 annual, for 6 / 16 / 120, and its licence is
   unresolved. Then NetVolo USD 13.98 on a three-year prepayment, HOSTKEY USD 15.67
   with the licence sold separately, Linveo USD 16.00, By-Hoster USD 19.02 with the
   buyer supplying the licence, Virtarix USD 27.40 with the licence printed at
   USD 16.00 inside the price, ServerPacket USD 32.19, windowsvps.host USD 36.00,
   InterServer USD 40.00 and Kimsufi KS-3 USD 64.00 all-in. The earlier USD 40.00
   InterServer floor ranked only machines whose licence the provider supplies, and
   it is 4.9 times the machine floor. ⛔ **No machine was booted.**
   ⭐ **The licence is a fixed line, and the machine is the only variable.** Windows
   Server Standard is USD 509.99 one-off for 16 core licences, which is USD 14.17 a
   month over 36 months, against Microsoft's USD 1,176 suggested MSRP. Datacenter is
   USD 2,499.99, or USD 69.44 a month. Sixteen cores is a per-server minimum, so a
   4 vCPU VPS pays the same licence as a 16 core one: a licensed Layer7 is about
   USD 24.31 a month, not USD 10.14.
   ⛔ **Four Windows items are open. Each needs one page read or one order screen:**
   - **Rabisu's licence.** The configurator prices Windows 2019 and 2022 at no
     surcharge, and none of the three pages read states that a licence is supplied.
     One order and one renewal decide it.
   - **Contabo's Windows add-on.** The plan page prints the machine only, at EUR 14.00
     a month for 8 cores, 24 GiB and 300 GB. A second page lists Windows Server
     Datacenter 2025 at EUR 28.00 a month, and the two were not reconciled, so
     Contabo is ranked on the machine price alone.
   - **ServerPacket's price.** The marketing page prints USD 32.19 a month billed
     every 12 months, which is USD 386.28 a year, and the store page prints
     USD 167.88 a year for the same 6 / 16 / 100 shape. If the lower figure is
     Windows-capable, the row ranks fifth at about USD 13.99.
   - **The rows with no order screen read.** ServerPacket, HOSTKEY, HostBrr, xHosts,
     LittleCreek, LumaDock and windowsvps.host carry a page price and no cart. One of
     the 20 rows in the cart audit reached a printed total, VPSDime at USD 40.00.

6. **`egress` went from 38 records to 376 and now answers the WireGuard ingress
   question. The open work is one signup and one handshake.**
   The topic gained a second question, and it is the one an operator asks first:
   which provider gives a WireGuard endpoint a public UDP port. The answer is at
   least ten, because a WG endpoint needs one UDP port and a free UDP forward is
   therefore a WG ingress provider. Eighteen documents now cover the class,
   hosted first: WG-native prefixes, hosted UDP forwards, public frp relays, L4
   edges, IPv6 brokers, overlays, platform ports, wrappers, the tunnel
   catalogues, and the paid ladder.
   ⛔ **Nothing here was measured end to end.** No account was created, so no free
   UDP port was allocated and no WG handshake crossed one. Two moves would change
   the rung: a TCPShield signup, which decides whether Sentry is on the free plan
   at 1 TB/month, and one `wg-quick` handshake through any free UDP forward. The
   volume evidence is also thin: the strongest free rows publish no byte cap, and
   `playit.gg`'s 1 to 2 TB/day is one operator's sentence.
   ⭐ **The last sweep added a search rule worth keeping.** Microsoft Dev Tunnels
   was listed as an unpriced free TCP forward until the resource-limits page
   stated 5 GB per user per month. A vendor's overview page and its FAQ can both
   omit the limits table, and the table lives on a product-wide limits page under
   a different name. Read it before calling a free tier unmetered.
   ⚠ **The earlier egress corrections still hold**: Yggdrasil has no exit nodes,
   the vocabulary gained `volume-quota`, and no record carries `qualifies` without
   a probe. The email half of this row is unchanged and still needs a real send.
7. **`databases-kv`: "after the free tier" is now answered for every provider.**
   `docs/databases-kv/free/after-the-free-tier.md` now carries an explicit row per
   provider with the inactivity policy, the deletion policy, the storage cap, the
   compute cap, the connection limit and the egress past the allowance. All eighteen
   rows for a provider with a free tier answer all six fields: where the value does
   not exist the cell says "not published" and the record names the URL that was
   checked. Eleven of them publish no connection limit and four publish no egress
   allowance, which is the finding and not a gap. The one remaining gap
   is a measurement rather than a page: nothing in this topic has been run against a
   provider's limit to watch what the refusal looks like.
8. **`domains-dns` carries one number it can settle cheaply.** First-year versus
   renewal pricing is fixed and the `.io` row is correctly `reported`. What is left
   is deSEC's domain count per account, which every source for is a forum post or a
   blog. One signup and one count would raise it from `reported` to `measured`.
9. **Five compute leads were found in an earlier wave and never recorded.** They
   were the only entries in `.tmp/` with no dossier record and no mention in a
   document, and `.tmp/` was cleaned on 2026-10-23, so this line is now their only
   home. Each is a `trial-only`, `unverified` or `fails-identity` row, which is why
   none was written up at the time: Modal for Academics (`modal.com/academics`),
   Leafcloud's 50 GPU-hours a month (`linkedin.com/posts/leafcloud-bv_...`), AYOO
   Cloud (`ayoocloud.com.br`), Dreamify AI (`free.waxianzhi.com`) and Abeiyun
   (`abeiyun.com/free/`). Record them or refute them in the next `compute` unit.
10. **`debrid` is new, and its whole evidence is a page read.** The topic went from
   nothing to a full catalogue in one programme, and the finding is not the count:
   ⛔ **no account was created in any of the 40 lanes.** Every quota is a vendor
   sentence, and the only `measured` rows are the relays, the open libraries and
   the file-host throughput, which need no account. Three moves change the rung,
   in this order:
   ⭐ **One 3 GB job through CloudPipe**, 40% of the no-card month and the only
   number resting on an unproven operational assumption (a 15 GB Drive cycled 30
   times). One job proves or kills the 1,116 GB month.
   **One TorBox free signup and one 10 GiB download**, which tests the only service
   whose documentation accepts a cloud address and whose WebDAV endpoint `rclone`
   can mount.
   **One paid month of Real-Debrid**, only to call `POST /rest/1.0/unrestrict/check`
   and settle whether a link is cached before a plan is bought.
   ⚠ Four storage records still need facts this unit found and did not apply:
   `put-io` retention is 15 days and its egress is 1 TB/month then 1.5 MB/s;
   `seedr-free-tier`'s "no free figure" note is stale, the FAQ says 2 GB and keeps
   files indefinitely; `rapidseedbox` is "from USD 5", not USD 19; Astraweb and
   Bulknews are missing their block ladders. The first two change a reader's
   decision and are the ones to do first.
   ⭐ **About 207 retrieval names from the seen-list sweep remain unopened**, plus
   eight bot names. The ledger is `.tmp/debrid/sweep/unverified-names.txt`, which
   holds 308 rows including non-retrieval names; `.tmp/debrid/sweep/sweep.json`
   carries the outcome per name. The highest value are four Telegram bots and the
   remaining file hosts.

11. **`ip-proxy` is new, and the whole topic rests on one class that no vendor has
    been proved to deliver.** Thirty-one records and eight documents, built for the
    gateway in §3.9. The finding is not the count: it is that **rung 5 — the
    registration class — is asserted by every vendor in the paid lane and was
    checked against a registry for only eight of them, four of which failed.** So
    the topic's central claim is a 50% failure rate on a sample of eight, and every
    per-address price in `paid/isp-proxies.md` is `documented` rather than
    `measured`.
    ⛔ **Nothing here was bought.** No proxy was dialled, no VPN was subscribed, no
    prefix was leased, no ASN was announced. Four moves change the rung, in this
    order:
    ⭐ **One `fetch()` against an upstream that refused a Cloudflare address, and
    the same request over `connect()` in the same minute, repeated enough times to
    land in more than one ASN.** That is the free rung-4 test the topic found and
    nobody has run: Cloudflare's pool spans AS13335, AS14789 and AS132892, a draw
    lands in one at random, and if the upstream counts ASN numbers the block is
    already intermittent. ⛔ **Do not describe this as a lever.** A paired 12-draw
    test refuted the claim that the transport selects the ASN; see
    `history/2026-10-24T111500Z/transport-does-not-select-asn.md`.
    **One day of IPRoyal ISP at USD 1.80 and one RIPE lookup per delivered
    address**, which tests whether a per-IP vendor's inventory is spread across
    `/24`s — the one number the whole per-address class rests on, and which only
    Proxy-Seller claims (200+ Class B, 600+ Class C).
    **One USD 45 StatesideIP mobile port and one USD 44.55 Evomi residential month,
    then the same request from each and from a Cloudflare control in the same
    minute**, which settles whether an eyeball class moves a refusal at all.
    **One TorGuard residential dedicated IP at USD 19.99**, whose "leased directly
    from major ISPs" claim could not be checked because its server list is
    walled — one purchase and one RIPE query decides it.
    ⚠ **Two open questions have no owner yet.** Whether Cloudflare BYOIP announces
    from the customer's ASN decides whether rung 5 is purchasable inside Cloudflare
    at a known price, and no Cloudflare page states it. And which ClientHello
    fields the OC-Free gate reads is still `unmeasured` in the gateway's own record,
    so `fingerprint.md` describes the tooling without being able to say which field
    matters.
    ⭐ **The seen list is large and unrecorded**: about 200 Chinese, Japanese and
    Russian vendor names from lane 3, the prefix brokers from lane 2 (IPXO,
    InterLIR, anyip, tacs.cloud, ghostnet.de), and the fingerprint projects from
    lane 8. A breadth pass starts there, not from a blank search.
12. **The fshy store is live; the public site is not.** `scripts/fr` queries a
    SQLite store built from `dossier/` in about 17 s. The public site was taken
    down on 2026-10-28 and its code moved to the public repository
    `Azathothas/fshy.ajam.dev`, where a merge session publishes the projection of
    reviewed records; it is not deployed again yet. Open, in
    order: (a) **review the held clauses**: `scripts/fr worklist held` lists
    about 260 sentences that carry a number and a process or terms marker and are
    therefore withheld from the public build; each is a source edit (`fr amend`)
    or a reviewed exception. (b) **Parse coverage**: only 285 records have a
    USD-a-month price and 690 a USD-per-TB price; `fr worklist unparsed` is the
    queue, and the parsers are in `scripts/fshy/derive.py`. (c) **Duplicates and
    entities**: `drift` holds about 310 same-product pairs that disagree on verdict
    or identity; settle each with `fr relate ... duplicate_of` or a field fix, and
    fix wrong vendor groupings in `registry/entities.tsv`. (d) **Guides**: the
    hand-written documents are not on the wiki yet; carrying them needs the same
    projection the records get.
13. **The research queue is in `queue/`, and four GitHub issues hold decisions.** Runs
    file what they could not settle as `queue/<id>.json` (128 items on 2026-10-28; list
    them with `scripts/rq queue`) and plan them with `scripts/rq plan RUN --queue ID`.
    The CNB, Baidu AI Studio and SimpFun re-run is queued; issue #13 was decided on
    2026-10-28 (`core-hours`, `gpu-hours` and `credits` are units now), so it can pass.
    The operator decided C01, C03 and C18 on the same day (issues #10, #11, #12): C01 is an
    error, C18 is an error for a plain `qualifies`, and C03 is an error in `storage` and
    `netdisk-pan` only. Today's cases are in `scripts/research/baseline.tsv`, and verify
    runs fix them (issues #25 and #26). Issue #16 holds the inference run's open items.
    About 20 LowEndTalk offer threads that name no vendor in the title were not opened.
14. **Two topics are new and empty: `dev-services` and `data-apis`.** The operator created
    them on 2026-10-28 (issues #31 and #43). Each has a README, a staleness window and no
    records. The first run for each is the issue that asked for it, with the new topic.
    Each README lists the records that sit in a neighbour topic and need a `relate` or a
    stated reason to stay.

### Recently closed

- **2026-10-28: research runs go through `scripts/rq`, with one writer and a second key.**
  `docs/research-protocol.md` is the procedure a parent agent follows for "Research/Expand
  <topic> <details>". Four runs used it: a compute verify run (#5), the eleven LowEndTalk
  vendors that were in no record (#7: ten `compute` records and `email/mailbig`), a re-run
  of the two units whose audit failed (#14), and the inference expansion below (#15),
  which a parent agent ran from that one line. A second model re-read 467 of their claims
  and judged 29 unsupported (6.2%); six units were undone and queued again. The runs found
  ten defects in the harness, fixed in #6 and #9. See
  `history/2026-10-28T101546Z/research-runs-have-one-writer-and-a-second-key.md`.

- **2026-10-28: free LLM inference APIs without a card, with their rate limits (run
  `20261028-0433-expand-inference`).** The run added 44 records, so `inference` holds 65.
  It re-read all 21 earlier inference records and 8 compute records. Where the vendor
  prints a rate limit, the record now holds it with a number, a unit and a scope, quoted
  from the vendor page. `docs/inference/free/no-card-rate-limits.md`
  is the answer. Seven lanes give a repeatable allowance for an email address or less: Groq,
  NVIDIA build, OpenRouter `:free` ids, Cloudflare Workers AI, Cohere trial keys, Requesty
  and flm, which needs no account. Three units failed their audit and were undone: u02, u04
  and u12. u02 and u04 were run again as u31 and u32, and both passed. Two audited claims
  were wrong in the first pass: GitHub Models names no endpoint, and DeepInfra's pricing page
  has no promotion. The closed free routes are Gemini CLI (2026-06-18), Qwen OAuth
  (2026-04-15) and iFlow (2026-04-17). `cheahjs/free-llm-api-resources` answered 404 on
  2026-10-28.
  - **Open after two reconcile rounds.** A `documented` value cannot replace a `measured`
    field, so the vendor-published limits of `inference/blockrun` and `inference/kilo-gateway`
    and three fields of `inference/opencode-zen-free` are not in the records. The fix is a
    new `limits[]` row at the next index, which a lane can write because an absent path takes
    any rung. One audited claim of `compute/cloudflare-workers-ai` is unsupported.
  - **Next.** Google Gemini and Mistral print no number without a login, so a signed-in read
    is the only way to fill them, and that account is the operator's to make. Five keyless
    hosts publish no limit: Kilo Gateway, BlockRun, free.ai, BeaverNet and JarvisClaw. 74
    open questions sit in `queue/`; plan the inference ones with `scripts/rq plan RUN --queue`.
    Register the free-LLM-API lists as inference sources in `scripts/sources/`, then diff them
    on the 30-day cadence. The weekly probe loop in item 3 above is still not built.

- **2026-10-26: the Windows VPS question answered three times, and the third pass
  was a sixteen-lane sweep.** The first correction priced six records for the
  cheapest machine that can boot Windows at 16 GiB, 4 vCPU and 50 GB. Layer7 leads
  at EUR 9.06 a month
  (USD 10.14), or EUR 86.97 a year (USD 8.11 a month, USD 97.35 first payment),
  for 4 cores, 16 GiB and 80 GB with a Windows Server Evaluation image. Saganetwork
  is the cheapest row a buyer can start on a monthly term at USD 8.23 ex VAT and
  USD 9.88 paid, for 6 / 16 / 120, with its Windows path unverified. Rabisu follows
  at USD 10.99 a month (USD 8.79 annual) for 6 / 16 / 120 with a Windows image at no
  surcharge and no licence sentence anywhere on its site. Then NetVolo at
  USD 13.98 on a three-year prepayment, HOSTKEY at USD 15.67 (EUR 14.00 on one
  storefront, RUB 3,390 on the Russian one) with the licence sold separately, Linveo
  at USD 16.00, Virtarix at USD 27.40 with the licence printed at USD 16.00 inside
  the price, ServerPacket at USD 32.19, windowsvps.host at USD 36.00, InterServer at
  USD 40.00 and Kimsufi KS-3 at USD 64.00 all-in. The first pass ranked only
  provider-supplied licences and started at InterServer's USD 40.00, which is 4.9
  times the machine floor. The third pass read sixteen lanes and at least 316 distinct
  provider labels, and the Windows-specialist merge alone ranks 58 rows that clear the
  minimums. It moved three claims and priced a fourth line: Rabisu's licence claim
  did not reproduce, HostBrr was left out because its order page configures no OS,
  VDSina's USD 4.08 is a per-day rate worth about USD 122 a month, and the licence
  itself is USD 509.99 for 16 core licences, or USD 14.17 a month over 36 months.
  Seven rows joined the twelve-row table and netcup left it. Cua's record was
  refuted in the same session: the live page rents no machine, and the 20 remote
  hours are relay time on hardware the customer owns. See
  `docs/compute/paid/windows-vps.md`, `history/2026-10-26T113332Z/`,
  `history/2026-10-26T121800Z/` and `history/2026-10-26T133000Z/`.


- **2026-10-24 — `ip-proxy` created from nothing, for one named client.** Thirty-one
  records and eight documents answer what a Cloudflare Worker's upstream actually
  sees, organised by the eight things an upstream can key on rather than by vendor
  type. Twelve breadth lanes ran over the western, Chinese, Japanese and Russian
  markets, free lists and volunteer relays, prefixes, clouds, VPNs and client
  software. Five findings are worth the wave: Cloudflare's egress pool spans **three
  ASNs** (AS13335, AS14789, AS132892), so a rung-4 block is already intermittent and
  the gateway cannot choose which; **four of the eight published addresses failed a
  registry check**; of 35 free proxies that worked, **10 still worked 22 minutes
  later**; a VPN buys **ASNs, not servers** (Windscribe 58 ASNs on a USD 39/yr plan
  against NordVPN's 7,193 servers over 25); and the free `/48` does not
  defeat rotation because **Meta's own paper names the `/48` as the rate-limiting
  unit**. Two premises were corrected: the gateway does not record that "rotation
  buys nothing", and residential proxy at 45 GB is **USD 36 a month**, not the
  USD 26,388 that a 1 TiB/day reading implied. Four vendors were found dead
  (NetNut seized by the FBI, LunaProxy and PIA S5 NXDOMAIN, 911.re seized) and one
  product withdrawn (Bright Data mobile).

- **2026-10-24 — the three operator questions answered, and the topic's own floor claim
  refuted.** A pass of 23 lanes rebuilt Q1, Q2 and Q3 from vendor pages. Three documents are
  new: `paid/under-five.md`, `paid/under-one.md` and `free/no-card.md`. `paid/README.md` said
  nothing existed below USD 6.49 while `paid/micro.md` listed eight machines below USD 5; the
  front page now says USD 3.75. Eleven verdicts moved, most of them a card requirement that a
  pricing page omitted, and Lightning AI stays `dead` against a lane that tried to revive it
  from its own marketing page while the status banner still read "Service is down".
  `sandboxprices.com` is registered and diffed. See
  `history/2026-10-24T021500Z/`, `2026-10-24T021700Z/` and `2026-10-24T025000Z/`.

- **2026-10-24 — the card gate became a recorded field, not a footnote.** The operator's
  complaint was that credit offers hid a USD 50 hold. The pass established the amounts for the
  vendors that publish one — Koyeb **USD 29**, Fly under USD 10, Contabo and Scaleway EUR 1,
  Google USD 0.00 to 1.00, IBM about USD 1.00 — and recorded that Oracle, Alibaba, OVHcloud
  and Huawei publish no amount at all. Five vendors refuse a prepaid or virtual card outright:
  DigitalOcean, Civo, Scaleway, Google and Alibaba. Exactly one accepts prepaid in writing:
  Kamatera.

- **2026-10-23 — the credit ladder widened to twenty and sized for 24/7.** Ten more balances were
  added and every row re-read. Nine claims moved: Confluent's trial is 30 days rather than 60,
  Northflank's cheapest plan is `nf-compute-50` at USD 12 rather than `nf-compute-100-1` at USD 18,
  OVHcloud prices compute at $0.2154/h and leaves the local disk unstated, CockroachDB publishes no
  trial length, NetMind's USD 100 is absent from its own page, Vultr publishes USD 250 and USD 300
  promo codes rather than being paid-only, and DigitalOcean, Akamai and Databricks all publish less
  than the corpus recorded. The page now states the hourly rate each balance sustains and the shape
  that spends it. See `history/2026-10-23T114500Z/credit-ranking-twenty.md`.

- **2026-10-23 — Civo's card gate.** The ranking called Civo the one large balance that asks
  for neither a card nor a phone. Civo's billing documentation says a payment method must be on
  file before any instance or cluster exists, so the gate is `card`, and the signup form is not
  the contract. See `history/2026-10-23T082000Z/civo-card-gate.md`.

- **2026-10-23 — the credit ladder was ranked.** Ten balances from USD 400 down to USD 200, every
  one re-read against the vendor's own page. Eight claims moved, two of them false `paid-only`
  verdicts (OVHcloud, IBM Cloud). Azure and AWS are excluded by operator instruction. The ranking
  is [`docs/compute/free/credit-ranking.md`](../../docs/compute/free/credit-ranking.md) and the
  corrections are in `history/2026-10-23T080500Z/`. Civo is the cheapest next signup: USD 250,
  31 days, and a verified card.

- **2026-10-23 — `debrid` built from nothing to a full topic.** Thirty-two research
  lanes, a reconciler that decided 54 contested fields, and four adversarial
  verifiers. Three headline claims were corrected by their verifiers: the no-card
  month is 1,116 GB rather than 966, but it clears 1 TiB only if three assumptions
  hold; UsersDrive's 73 GB/day wins on cash but only for files it already holds,
  so it does not beat a USD 3 plan; and the cloud-IP claim was one service too
  broad, with three services silent rather than refusing. Two storage verdicts
  were overturned as false negatives. See
  `history/2026-10-23T034500Z/two-false-dead-verdicts.md`.

- **2026-10-22 — `coding-subs` and `inference` blockers closed.** An adversarial review
  found six `blocks-use` defects in the two topics. All six are fixed, and the
  systematic audit that followed found four more: Cerebras has no permanently free
  tier, Hugging Face grants no credits to a free account, Abacus.AI's ladder is
  readable and has no free tier, and Groq's per-model free table is in the served HTML.
  Two `dead` verdicts were overturned on evidence of life (Devin, Windsurf), one
  record was corrected from `qualifies` to `paid-only` (Hugging Face), two from
  `unverified` to `documented` (StepFun, Abacus), and one from `qualifies-with-caveat`
  to `trial-only` (Cerebras). The topic's headline answer changed: StepFun Flash Plus
  at USD 9.99 is the cheapest script-drivable plan with a published ceiling, and it
  was absent from every table. See
  `history/2026-10-22T044100Z/`, `2026-10-22T044300Z/`, `2026-10-22T042700Z/`,
  `2026-10-22T043000Z/` and `2026-10-22T044500Z/`. Open from this pass: the
  `ttft_ms > latency_ms` rows are re-measured with a corrected instrument
  (`.tmp/work/fx-coding-inference/probe3.py`) and every record's `verified_at` now
  carries a machine-read instant rather than a typed midnight.


### Known red checks

⚠ **On 2026-10-26 the gate exits 1 on `staleness`, and on nothing else.** The two rows are
`dossier/compute/baidu-ai-studio.json` and `dossier/compute/tencent-cnb.json`. Each carries a
`linux.do` evidence row dated 2026-04-27, which is 182 days old against a 180-day budget. The
live thread now serves an anti-AI notice instead of the post, the archive broker returned
HTTP 429, and the search snippet quotes the thread but not the specific GPU claim. Re-reading
the source is the only legitimate fix, and re-dating the row is the bulk touch the check exists
to catch. Both rows predate this session.

On 2026-10-28 it is still the only red check. Two verify units re-read both records with first-party
captures, and both failed their audit (4 of 30, then 4 of 26 claims unsupported), so the integrator
undid them. Two of the second attempt's four failures were the `free_tier.unit` vocabulary, which had
no unit for core-hours (issue #13). The operator added `core-hours`, `gpu-hours` and `credits` on
2026-10-28, so the queued attempt can pass now. Until it lands, the check is red on `main` as well,
and `scripts/rq gatecmp` (no check fails that passes on the base) is the test of a change.

The `sources` check was red at the start of the session and passes now. `lowendtalk-com-26`
was diffed at 27 covered and 48 missing on 2026-10-26, and `monosans-proxy-list` at 1 covered
and 0 missing.
