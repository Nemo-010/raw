# The shortlist pass: one pick replaced, one verdict explained, and 186 identity fields that said nothing

- **When:** 2026-10-24T05:30:00Z
- **Status:** corrected
- **Supersedes:** the Q1 paid pick (AlphaVPS C6G), the Tencent `fails-identity` verdict's *reason*, IBM LinuxONE's verdict, GitLab's verdict, the Q3 free-tier lead, and 186 `identity_cost.detail` fields
- **Superseded by:** ten verification and audit lanes (`.tmp/compute-2026-10-24/shortlist/`) and four repair lanes (`.tmp/compute-2026-10-24/repair/`)
- **Evidence:** the records named in `docs/compute/shortlist.md`; quotes are in each record's `evidence[]`
- **Confidence:** documented

## The four questions, answered

`docs/compute/shortlist.md` is new: ten free tiers, two paid beefy, two paid micro.

## Q1: one pick replaced, on the same money

**VolpaByte Ryzen KVM 8 GB replaces AlphaVPS C6G.** Both are **EUR 50.90 a year**, and for the
same out-of-pocket total VolpaByte gives 6 vCPU / 8 GiB / 100 GB / unlimited traffic against
AlphaVPS's 3 vCPU / 6 GiB / 55 GB / 6 TB.

⚠ **The trade is a written renewal.** AlphaVPS states "LOCKED AT RENEWAL, FOREVER" three ways on
one page; VolpaByte states no renewal term at all, and month 13 is inferred from its EUR 4.99
monthly list. VolpaByte also adds 19% VAT with **no country selector**, so a non-EU buyer's total
is untested — USD 4.75 if the VAT stands, USD 3.99 if not. Both are under the line.

**HostBrr Value 8GB stays**, because its checkout itself prints the renewal: "Total When
Renewing: 1 Year @ $55.00 USD". It is the only row in the lane whose renewal is stated by the
vendor's own cart rather than derived.

Both were confirmed **in stock and buyable**: AlphaVPS in Sofia and Los Angeles (sold out in four
other locations), HostBrr in Frankfurt, neither checkout asking for an ID document, a company or
a local address, neither stating a card hold. AlphaVPS's VAT answer was measured rather than
assumed: the same cart priced to a US address totals EUR 50.90 with no tax line; priced to a
German address it adds EUR 9.67 of VAT for EUR 60.57.

## Q2: both buyable, and one is cheaper on a longer term

**C-Servers NanoVPS-384 is in stock at Ashburn**, opens without an account, totals USD 2.39 at
step 2 with no setup fee and no tax line. Its order page sells 6/12/24/36-month terms and the
**36-month rung is USD 0.2497 a month** — the cheapest per-month rate of any documented,
in-stock, entity-verified row in the band.

⛔ **Its UDP statement carries a condition that matters.** The vendor's article requires a UDP
application to "preferentially send a continuous packet stream", which a WireGuard handshake
every 25 seconds is not. That is a stated requirement, not a measured failure, but it is why
**Cheap-Host NAT Start at USD 0.73** ranks above it on ports: 999 TCP/UDP ports, 1 GiB of RAM.
Cheap-Host's rails are SBP, SberPay, YooMoney and MIR only, and it names no company — so for a
buyer outside Russia the pick reverts to C-Servers.

**TierHive Micro survives and gets stronger**: six registration fields, **no payment instrument
at all**, so it is the only sub-dollar machine a buyer can start with nothing. Its first payment
is USD 3, not USD 0.10. ⚠ Its own AUP says the service is in "Alpha status" and "data loss can
occur at any time without warning".

## Q3: a real no-card VM, and a verdict finally explained

**Opus Host is the find**: 1 vCPU / 1 GiB / 20 GB, **KVM root with one IPv4 and one IPv6**, no
payment data of any kind, from a named German sole trader with an imprint, a phone number and a
status page. It is the only no-card row found that gives a full VM rather than a process.
⚠ Its plan JSON carries `runtime_days: 30` and no page explains it.

**Silly Development and Waifly** state in their own terms that they do not sleep, do not expire
and do not renew, for an email alone.

⛔ **GitHub Actions' "free and unlimited" has a condition, and it is not a number.** GitHub's
Additional Product Terms forbid "any activity unrelated to the production, testing, deployment,
or publication of the software project associated with the repository", and forbid using Actions
"as a content delivery network or as part of a serverless application", with account termination
as the remedy. The meter is unlimited; the permitted use is not. The honest headline is
**"unlimited compute for work on the repo it belongs to."** The shape is confirmed exactly:
4 vCPU / 16 GiB / 14 GB, 20 concurrent jobs on Free, 6-hour job cap, 5-minute cron floor,
60-day schedule disablement.

**Tencent's `fails-identity` is confirmed, and its stated reason was wrong.** Ordinary purchases
need verification only for the Chinese mainland. But **every promotional campaign, including the
free trial, requires 实名认证** — the individual identity check — because the campaign rules say
so in both English and Chinese. The earlier record said "the account cannot be opened at all
without a government document", which is false: an account opens with email, phone and a card.

## Two verdicts corrected

| slug | was | now | why |
| --- | --- | --- | --- |
| `ibm-linuxone-community` | `qualifies-with-caveat` | **`trial-only`** | a hard 120-day stop, after which "all resources will be cleared of your data", and no documented renewal. Its phone step is also **gone** — the SMS block is commented out of the live form, which is where the corpus's `any-phone` came from |
| `gitlab-runners` | `paid-only` | **`fails-identity`**, kind `card` | GitLab's own FAQ: "credit/debit card details are required if you choose to use GitLab.com shared runners", verified by a USD 1.00 authorisation |

Also: `buildkite` was recorded as providing no machine on the Free plan; it provides 2 vCPU /
4 GB with 2,000 vCPU-minutes a month.

## The largest repair: 186 identity fields that asserted nothing

**453 compute records carried `identity_cost.detail: "as stated by the provider's signup page"`**
— a string that names no card, no hold, no phone and no document, in the one field that prices
reaching a provider at all. Four lanes repaired **186 of them from evidence already in the
record**.

| measure | before | after |
| --- | --- | --- |
| records asserting nothing | 453 | **267** |
| records stating a hold amount | 26 | **38** |
| of 215 card-gated records, share stating a hold | 12.1% | **18.0%** |

**Four `kind` values were wrong**, and each could have held up a wrong verdict:

- `akamai-edgeworkers`: `card` → **`institution`**. The evidence requires "an active Akamai
  contract and login credentials for Akamai Control Center". No evidence row mentions a card.
- `blackbox-ai`: `card` → **`institution`**. The pricing page renders only an Enterprise card.
- `alibaba-cloud-model`: `any-phone` → **`card`**. The trial needs "Mobile number, payment
  method, billing address" — a phone is one of three, not the binding one.
- `lium`: `card` → **`email`**. The USD 5 is granted on an email address **or** a first deposit.

⚠ **267 remain.** Ten of the 186 could not be repaired because the record states no identity
fact at all, and they now say `unverified:` with the reason rather than a vacuous sentence. The
rest need a signup-page read each.

## The defect class that keeps recurring

⭐ **Four more hiding negatives were found and corrected in `micro.md` alone**, where the
document asserted:

- "No verified full VPS exists below USD 1.42" — **12 documented records** sit between USD 0.10
  and USD 0.90.
- "No record names a passport or residence document" — **26 compute records** carry
  `identity_kind: national-id`.
- "`hetzner-dedicated` carries no shape and no price" — its notes price the AX41 at EUR 59.00.
- "Four things would put a row under it" — all four had already happened.

That is now **seven** hiding negatives in this topic. Every one was a claim about absence written
without a search that could have found the counterexample. **A negative is a claim about a
search, and it carries the search's scope in the same sentence or it is not a finding.**

## What the document audits found

Four documents audited for the first time, 300+ claims checked:

- **`lowend-vps.md` had the market's shape backwards**: it claimed three rows under USD 2 and
  said every one is IPv6-only or NAT. There are **19**, and 8 carry an IPv4. The real shared
  constraint is prepay: 15 of the 19 price only a six-month or longer term.
- **`vps-monthly.md` crowned a box nobody can buy**: the Hetzner CX23 is marked "not available"
  on every rung of its line. The answer is now Contabo's Cloud VPS 4 at USD 6.60.
- **`cloud-vms.md`: 14 of 35 table rows disagreed with the record they cite**, all drift since
  the last rewrite. Five monthly figures elsewhere were the 10-hour column quoted as a monthly
  bill.
- **`always-on-free.md`'s tier table was fiction** in five places, including GitHub Codespaces
  filed DEAD when its record says `qualifies`.
- **`micro.md` applied Modal's list rate to a Sandbox** in four places; the page prints
  "Sandboxes are billed at non-preemptible rates of 3x list price", so a minimum container is
  USD 0.0207/h and USD 30 buys 1,446 Sandbox hours, not 4,348.

## The two niche catalogues, audited last

`forum-hosts.md` and `regional-clouds.md` were the last two documents in this topic never checked.
**133 claims checked, 25 failed.** The corrections that matter:

- **`sanfengyun` was mis-kinded.** Its record said `email` while its own offer text says a mobile
  number plus a CNY 0.3 real-name certification. Now `national-id`, which is the gate the
  operator cannot pass.
- **`cloudcone` prices were recorded as unpublished** when the record carries USD 28, 46 and 69
  a year for its three rungs.
- **`iwinv`'s monthly cap was arithmetic that did not hold**: 30 x KRW 210 = 6,300 against a
  5,600 monthly ceiling. Cap removed, the arithmetic shown.
- **`cloud.ru` Evolution moved `trial-only` → `fails-identity`** under the 2026-06-30 rules.
- **`webarena-indigo`'s "contradiction" was withdrawn**: JPY 50 is a monthly minimum and JPY 290
  a rate, so both are compatible. A false finding, correctly retracted rather than kept.
- **`chataoyun` was a typo** for `chamaoyun`.

⚠ **A count C3 measured mid-pass went stale before it landed.** It reported 450 records naming a
gate without pricing it, against the pre-repair dossier. The repair merged afterwards, so the
figure is now 266. Corrected in place with the sequence stated, along with five other `1,239`
counts that the merge to 1,255 had outdated.

## What is still open

- ⛔ **Nothing was signed up for.** No account was created and no machine booted. Every row in
  the shortlist is `documented`, not `measured`.
- **267 records still assert nothing about identity.**
- **Opus Host's `runtime_days: 30`** is unexplained — the difference between a permanent machine
  and a one-month one, and it needs one account watched past day 30.
- **VolpaByte's VAT and payment methods** are untested past the configurator.
- **`dossier/compute/netcup.json`** still carries a VAT-inclusive EUR figure labelled USD; the
  page prints all five plans at a 1.150 ratio while its own label says 19%, and the disagreement
  is recorded rather than resolved.
- **`littlecreek` and `little-creek-hosting`** are one provider under two slugs.
