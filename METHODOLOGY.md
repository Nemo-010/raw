# Methodology

This repository answers one question with evidence: which free,
nearly-unlimited or cheapest-paid services survive contact with reality.

A codebase is checked by its build. This repository's deliverable is a corpus of claims, and
every claim is one vendor decision away from being false. So the discipline answers different
questions than a software methodology does. What is a claim worth? What makes it expire? How
does the next session tell a measured fact from a plausible sentence?

Read this before your first tool call. Read `docs/conventions/README.md` before your first sentence.
Both are binding. This document says what the work is; that one says what the work looks
like on the page.

## Contents

| section | what it answers |
| --- | --- |
| 1 | what this repository is, and where research ends and implementation begins |
| 2 | what a research unit is, and how to write its question |
| 3 | the evidence ladder, in prose and in JSON |
| 4 | the constraint vocabulary, and what identity costs |
| 5 | the nine lines: never invent a number, never trust HTTP 200, one fact one home, and the rest |
| 6 | the research loop: a breadth pass and a depth pass |
| 7 | the challenge protocol: change route, and try every route |
| 8 | the forum layer, and the multilingual query vocabulary |
| 9 | the two review kinds, and what a reviewer never does |
| 10 | drift, staleness and decay: the policy file, the two clocks, and the bulk touch |
| 11 | handover, and what a session leaves behind |
| 12 | what is out of scope, stated once |
| 13 | the anti-patterns, named with their cost |
| 14 | what a session does not do |
| 15 | the definition of done |
| 16 | when to stop |

---

## 1. What this repository is

One question, one standard of proof.

The corpus assumes no local hardware and no institutional identity, and prices only free,
trial and cheapest-paid capacity. Every unit is judged against whichever workload it serves, and
the target is **every cheap resource**, not storage:

| resource | the question | the storage-shaped example |
| --- | --- | --- |
| storage | where do bytes live | a hot set, an archive set, and a daily served volume |
| compute | what runs, for how long, what reaps it | a machine that stays up, a sandbox, GPU hours |
| inference | what answers without a card | free and guest model endpoints |
| everything else | egress, email, DNS, databases, CI runners, credentials | each is a blocker when it costs money |

⚠ **The storage filter below applies to storage and to nothing else.** A free GPU hour, a
working email sender and 100 GB of Postgres are findings of the same rank as a free terabyte,
and judging them against a storage quota is how a session talks itself out of the resources
that matter most.

A **storage** candidate clears four filters or it does not enter a table: 500 GB (decimal,
500,000,000,000 bytes) or more free per unit, or trivially repeatable; free or Cloudflare-covered
egress; a reachable interface (S3, REST, WebDAV, SFTP, OCI, Git, rclone, or a protocol a wrapper
could speak); and an identity a registrant can produce.

⚠ **The filter is 500 GB decimal, and it is stated once for that reason.** 500 GiB is 7.4%
stricter, which changes which providers sit at the boundary. A provider whose page states a
binary figure is compared at its decimal equivalent and the conversion is written down.

⭐ **The repository answers what exists and what breaks. It does not build a working
stack.** Those are different jobs, and one session doing both stops testing the premise.

| the research unit owns | implementation owns |
| --- | --- |
| whether the mechanism works at all | making it work on every input |
| what it costs, measured | making it cost less |
| what breaks it, and what breaks first | handling what breaks it |
| the routes refused, and why | re-opening one when the constraint moves |

⛔ **Polishing is scope creep here.** A unit that builds an uploader has spent its
budget on the half that was not in doubt, and has stopped looking for the thing that would
have killed the recommendation. Say what is unfinished. Do not finish it.

---

## 2. The research unit

A unit is **one topic, one service class, one question**. Nothing else.

| topic | service class | question |
| --- | --- | --- |
| netdisk | Chinese pan drives | can a registrant without a PRC identity obtain 500 GB or more, and what binds first? |
| storage | OCI registries | which registries accept a single blob above 100 GiB, and what caps it? |
| coding | subscription coding agents | which plan serves 15M input and 37.5M output tokens a month for under $10? |

A programme is a set of units that share one scope and one reconciliation step. A programme
is not a unit written larger, and a unit is not a programme cut in half.

### 2.1 Write the question so that it has a wrong answer

⛔ **A unit with no falsifiable question produces a survey.** A survey is readable, it is
long, and nobody can act on it, because nothing in it was ever going to come out false.

| this is a question | this is a survey |
| --- | --- |
| can a new account store 1 TiB and read it back without credentials | what are the best cloud drives |
| what breaks first at 1 TiB per day | is this provider good |
| does the quota survive a second registration from the same address | how does registration work |

State what result would make you abandon the route **in the same paragraph, before any
measurement exists**. It goes in the unit's working note and moves into the record's `notes`
when the record exists. In a run, the working note is the unit's `log.md`; outside a run, it is
`.tmp/session-<id>/notes.md`. ⭐ **The abandonment condition is
the cheapest protection against the pass that finds what it was looking for**, and it costs one
sentence to write before you care about the answer.

### 2.2 Three questions, and the third is the one that gets skipped

| | the question | what skipping it costs |
| --- | --- | --- |
| **does it work** | the mechanism runs at least once, observed from outside | nothing. This one never gets skipped. |
| **what does it cost** | money, bytes served, requests, identity, a clock, a person | a provider adopted on capability alone, whose price arrives after it is depended on |
| ⛔ **what breaks it** | the rate, the cap, the clock, the concurrency or the size that defeats it | the only row that would have changed the decision |

⚠ **A finding with no third row is a recommendation with its failure mode removed.** A reader
then meets that failure first, with no budget for it and a plan built on the
assumption it was not there.

### 2.3 ⛔ The first explanation that fits is the one to distrust

**It fits because you stopped looking.** Nothing else follows from its fitting.

A confident, cheap answer can be built on one untested hypothesis, and nothing in its output
says so. **The first explanation that fits is the one to distrust**, because fitting proves
only that the search stopped.

So, past the point where a conclusion gets written down:

1. **Enumerate three candidate explanations before testing any of them**, and write them in
   the record's `notes`. One candidate means you have not read enough yet.
2. **Test to refute.** Ask what you would see if a candidate were false, then go and look for
   that. Evidence collected to support a hypothesis is not evidence.
3. **Do not let one line of inquiry suppress another.** Two candidates on the same line for
   different reasons are two candidates.
4. **Give every candidate one verdict**: confirmed with the evidence quoted, plausible with
   what would settle it, or refuted with what disproves it.
5. **Then read it again as somebody holding your list and looking only for what is not on
   it.** Finding nothing there is a result, and it is written as one.

⚠ **Speed, token count and confidence are not quality signals, and two of them run the wrong
way.** The honest measure is coverage: what was opened, what was run, what was left.

---

## 3. The evidence ladder

Every claim in this repository carries exactly one class. The class is not decoration. It
decides what the claim may be used for.

| class | what it means | what must be recorded | what it may carry |
| --- | --- | --- | --- |
| `measured` | a live request made in this session | status, bytes, SHA-256 or byte count, UTC timestamp, the exact command | any number, and the words "works", "breaks", "costs" |
| `documented` | a first-party page read in this session | URL, read date, the sentence quoted | a quota, a cap, a price, an interface, "documented to work" |
| `reported` | a third party: forum, blog, aggregator, tracker | URL, date, who said it | a failure someone hit, a change someone noticed, a regional price. Never a quota on its own. |
| `inferred` | reasoning over other evidence | the premises, each with its class, and the inference written out | a hypothesis and the test that would settle it. No number in a table. |
| `unverified` | asserted and not checked | the reason, named | a dash, and the reason |

### 3.1 The weakest link sets the class, and that is the only rule

A record's class is the **weakest** rung among the fields its verdict depends on. Apply that
rule in this order.

1. **Name the fields the verdict depends on.** They are quota, egress, interface, identity,
   retention and per-object cap. A field the verdict does not rest on does not enter.
2. **Give each of those fields its own rung**, from the table above.
3. **Take the weakest.** The record's `confidence` is that rung.

A probe that returned 206 proves the read path. It does not prove the quota, the retention
clock or the registration gate. So a record with a measured read and a documented quota is a
`documented` record carrying a probe. A record whose quota is `documented` and whose egress is
`inferred` is an `inferred` record, and `notes` says both.

⚠ **Why the weakest and not the most important.** "The field the verdict depends on most" is a
judgement about salience, and two honest readers make it differently on the same record. The
weakest rung is a minimum over a named set, so two readers compute the same answer. It is also
the conservative one: it can only move a claim down.

⚠ **An inherited `measured` is not `measured` here.** A number measured in another session, on
another day, against a service that has since changed, is a claim about that day. `BRIEF.md`
says it in its soft-spots list: anything inherited from an earlier session is `documented` at
best until it is re-run in this repository. Re-running the five providers a plan depends on is
cheap.

### 3.2 A documented absence is weaker than a documented limit

"Unlimited" is a claim about a missing sentence. It is not a limit, and it cannot be
multiplied.

- RepOD returns 404 on `/storage/quota` because it predates Dataverse 6.1. It has a quota.
- 83 of 149 Dataverse installs report no quota at all. Some of them have one; the endpoint is
  off.
- ModelScope publishes "no storage limits" and enforces an undisclosed, traffic-dependent
  commit throttle. The quota is not the constraint.

So a documented absence is recorded as a `documented` claim whose `proved` field says what is
missing, it may not be used in arithmetic, and the sentence that quotes it says the same.
⛔ **Do not conclude "unlimited" from a 404.**

### 3.3 A vendor page is first-party for what it sells and third-party for what it does

A pricing page proves a price. It does not prove that a limit is enforced, that a cap is
reached, or that a refusal looks the way the page says. Where a page and a probe disagree,
the probe is the finding and the page is the claim.

⚠ **Nor is a vendor's number always a quota document.** "Best-effort" with no number is a
discretionary throttle, which is worse than a quota: there is no ceiling to design against
and no threshold at which it is safe.

### 3.4 A form is not a registration

"Registrable by a foreigner" read from a signup form is `documented` about the form. It is
not a completed registration, and no Chinese provider here is recorded as signed
up for. The row says so. Where the whole recommendation rests on it, the sentence says so in
the same line.

### 3.5 How each class is written in prose

One claim, one class, in the sentence that states it.

- **measured**: "500 GiB read back byte-identical on 2026-10-21 (206, 5,242,880 bytes,
  SHA-256 `3f2a91c0`)."
- **documented**: "The help page states 5 TB (`https://1fichier.com/hlp.html`, read
  2026-10-21)."
- **reported**: "Two forum posts report a 20-file cap (`nodeseek.com/t/1234`, 2026-03-12)."
- **inferred**: "If the 90-day clock runs from last access, a monthly keep-alive holds it
  open. Not tested."
- **unverified**: "Not verified: every route to the signup form returned a challenge on
  2026-10-21."

⛔ **A `✅` with no probe behind it is a fabricated measurement**, and a more serious defect
than an admitted gap. `✅` means somebody ran a live request and recorded status and bytes.
`docs` means a page was read. Neither may be inferred from the other.

⚠ **A shortened digest is a specimen, not a citation.** A record carries the whole
`sha256`, because a prefix proves nothing and two different objects can share one.

### 3.6 How each class is encoded

This is a fragment of a record, showing only the three fields that carry the rung. The full
shape is `docs/conventions/README.md` section 6.1.

```json
{
  "confidence": "documented",
  "verified_at": "2026-10-21T09:14:02.418Z",
  "evidence": [
    {"url": "probe:https://zenodo.org/api/records/5656641/files/iPS.zip/content",
     "date": "2026-10-21",
     "proved": "206 Partial Content, 1048576 bytes, sha256 3f2a91c0d4e5b6a7; ranged read works anonymously"},
    {"url": "https://help.zenodo.org/docs/deposit/manage-quota/",
     "date": "2026-10-21",
     "proved": "quota is 50 GB per record and unlimited records, quoted"}
  ]
}
```

⭐ **The class lives in `confidence`, and the evidence for each field lives in `evidence`.**
The `proved` string is the part that makes a record auditable: it says which fact the source
established, so a later session can tell whether the source still proves the sentence.

⛔ **A new evidence row with an `http` URL also carries `capture` and `quote`.**
`capture` is the sha256 of the page text the claim was read from, stored under `sources/c/`.
`quote` is the exact sentence of that text that proves the value. A `documented` claim is then a
quote found in a stored capture, and a later session checks it without the live page. The gate
(rule C21) refuses a new row without both. See
[`docs/research-protocol.md`](docs/research-protocol.md) section 7.

⚠ **The record above is `documented`, not `measured`, and the reason is the rule.** The probe
proves the read path. The quota comes from a vendor page, so the quota field is `documented`,
and the weakest field decides. A record earns `measured` when every field its verdict depends
on was measured here.

`confidence` on the record is the weakest rung among the fields that matter to its verdict,
per `dossier/README.md`, and section 3.1 above is the same rule stated once. ⚠ **The per-field
rung is what makes a record auditable**, so a record
whose quota is `documented` and whose egress is `inferred` says both in `notes`, and its
`confidence` is `inferred`. The canonical field list is `scripts/dossier/schema.json`. Where
this document and that schema disagree, the schema wins and this document is the defect.

---

## 4. Constraints

The headline number is almost never the binding one. Seven constraints do the binding, and
every candidate names the one that binds it.

| constraint | what it looks like | what it does to a workload | the question that exposes it |
| --- | --- | --- | --- |
| `request-rate` | 5,000 per hour, 80 writes per minute, 1,000 per **month** | bounds calls, not bytes. A monthly counter is fatal to a nightly job. | what is the window, and is it per account, per project or per IP? |
| `pull-count` | 100 pulls per 6 hours per IP | turns a daily serving target into a counting problem | how many distinct objects per day, and how much reuse? |
| `per-ip-shaping` | 1.6 MiB/s, 5.6 GiB per day per IP | bounds one reader, and parallel readers multiply it | what does one stream get, and what does the thirty-second get? |
| `per-object-cap` | 2 GiB per asset, 256 GB per object, 20 GB per file | sets the shard size, therefore the file count, therefore the real total | what is the largest single object, and how many may I create? |
| `write-gated` | a curator, a review, a build recipe, a phone PIN | the write is a queue with a person in it | who approves, and what is the rejection rate? |
| `retention-clamped` | 1 year requested, 90 days granted | the clock is set by the server, not the client | what does the API report as expiry, not what did I ask for? |
| `volume-quota` | 1,000 GB per month, 100 GB per month of egress | a monthly counter, which bounds a month rather than a second or an object | is the allowance per account or per caller, and when does it reset? |

### 4.1 Convert every claim to a rate before you compare it

A port, a shaping number and a monthly quota are not comparable until they are per day.
1 TiB per day is **12.1 MiB/s sustained**.

| the provider states | that is, sustained | share of 1 TiB per day |
| --- | --- | --- |
| 1 MiB/s | 84.4 GiB per day | 8% |
| 10 Mbit/s | 0.098 TiB per day | 10% |
| 100 Mbit/s | 0.98 TiB per day | 98% |
| 1 TB per month | 33 GB per day | 3% |
| 12.1 MiB/s | 1 TiB per day | 100% |

⭐ **A rate cap does not bound a day's volume. A byte quota does.** One relay peer at
200 Mbit/s is 2.16 TB per day, or 1.96 TiB, with no quota at all. Cloudflare TURN at
1,000 GB per month is 33 GB per day, which is 3% of one day's workload. Both are "free". Only
one is usable, and the arithmetic says which.

⚠ **A decimal figure and a binary figure are not interchangeable.** 200 Mbit/s is 2.16 TB per
day exactly and 1.96 TiB per day. The conclusion does not change; the unit does, which is why
`docs/conventions/README.md` allows binary units only.

### 4.2 Identity is a first-class field, not a note

Every candidate carries `identity_cost`, and it is one of exactly seven values.

| value | what it costs to produce | reachable for a registrant |
| --- | --- | --- |
| `anonymous` | nothing | yes |
| `email` | an address | yes |
| `any-phone` | any number that receives a code | yes |
| `card` | a payment instrument, often with a $0 authorisation | yes, but it converts a free tier into a payment relationship |
| `country-phone(<which>)` | a number in a named country | only for that country |
| `national-id` | a real-name identity check | no |
| `institution` | an affiliation, a tenant, a project membership | no, unless the registrant holds one |

⛔ **An unreachable quota is worth zero, and the sentence that quotes the number says so.**
"10 TiB per project, Finnish affiliation only" is one sentence, not two. The corpus's biggest
numbers are mostly in this class: CSC Allas, LUMI-O and OSN total 10 to 150 TB each and are
all closed to a registrant without an institutional identity. Their figures are real and irrelevant.

⚠ **Search for the phrase "outside institution" on the deposit help page.** It separates the
institutions that take an email address from the federated ones that take a Shibboleth
identity, and it is the fastest test available for an academic repository.

### 4.3 ⛔ Name exactly one binding constraint

Several constraints apply to every provider. The record names the one that fails first at the
scale it is judged against.

The record holds a `limits[]` array, one entry per constraint it found, each
`{kind, value, source}`. Every entry is kept. ⭐ **Then the record names which one binds, in
the `binding` field**, because a table cell listing four constraints has not decided what
breaks first, and a reader cannot design against a list.

`binding` takes one value from the same seven-value vocabulary as `limits[].kind`, plus `none`
for a provider with no constraint above the working scale at all. `binding_note` carries the
one-sentence reason where it is not obvious from the list. The schema keeps both optional, so
a migrated record can land before anyone has decided. ⛔ **The gate CI runs (`scripts/gate.sh`) requires
`binding` on every record whose rung is `measured` or `documented`**, which is where the
decision changes a recommendation. A `reported` record can wait for its rung to rise.

The requirement, quoted: "Failure mode at scale. One
sentence: what breaks first: request rate, per-IP shaping, retention clock, queue
backpressure, pull counter, or project expiry."

⚠ **Two corollaries, and both are measured.** The biggest per-object caps cluster where
retention is shortest: 999 GiB on a 90-hour clock, 300 GiB on a 14-day clock. And the write
path is throttled separately from the read path, so a large quota can arrive with a small
upload budget.

---

## 5. The nine lines

Every rule below is one of these, and a rule that is not here is a preference.

1. **Never invent a number.** An unverified claim says `unverified` and why, in the sentence that
   states it.
2. **Never trust HTTP 200.** Hash every download; compare against the recorded hash.
3. **One fact, one home.** The dossier owns the record; every table in `docs/` is a view of it.
4. **Never delete a finding.** A dead provider becomes `verdict: dead` with the evidence of its
   death; a superseded claim moves to `history/` with the reason.
5. **No credentials in the tree, ever.**
6. **No tool or model attribution anywhere.** No co-author trailer, no "generated with", no tool
   or model name in a commit, a document footer or a file header.
7. **Every claim carries its rung:** `measured`, `documented`, `reported`, `inferred` or
   `unverified`.
8. **A server's `Retry-After` is the only pacing rule.** No client-side cap, no rate, no delay.
9. **The three scope facts.** No hardware and self-hosting last; a missing client tool is not a
   rejection; the target is every cheap resource, not storage.

The measurements behind the technical rules are in
[`docs/crawler-scraper/free/web-failure-shapes.md`](docs/crawler-scraper/free/web-failure-shapes.md).
The procedure is in [`docs/research-protocol.md`](docs/research-protocol.md).

## 6. Running a unit

The loop, in order. It has two passes, and they pay for different things.

| the pass | what it takes | what it buys |
| --- | --- | --- |
| breadth | every registered source of section 6.0, and a search per candidate class, in both directions, in every language section 6.1 names, plus its inverse queries | the candidate list and the `seen` list |
| depth | the eight checks of section 9.1 for every candidate that looks real, batched where one page answers several | records that can carry a decision |

⭐ **There is no call budget** ([`AGENTS.md`](AGENTS.md) section 2 rule 15). Make every call the
two passes need. When a unit finds more real candidates than it can probe fully, the parent plans
more units, one per provider class or group of names, and starts them all at once; a unit never
probes shallowly to fit.

```
map the niche breadth-first   -> every candidate class
pick every candidate that looks real
probe depth on each           -> read, probe, read back
write the records             -> one file per provider
reconcile                     -> merge, dedupe, resolve contradictions
report                        -> answer first, then the constraints
```

⚠ **Every check of the depth pass is done for every candidate that goes deep.** Checks five to
eight are the read-back, the throughput curve, the cap-with-retention pair and the failure mode
at scale, and those are the four that catch the failures the rules in section 5 were written about.
⛔ **A provider probed shallowly is worth less than none: it looks like a decision and cannot
carry one.**

⚠ **A unit that holds two questions is two units.** Running it as one is how a breadth pass
becomes a single-provider essay.

### 6.0 ⛔ Start from the source registry, not from a search

A breadth pass begins with `scripts/sources/aggregators.tsv`: every site known to list other
providers, each with a cadence and a last-diff date. Diff each one that is due against
`dossier/` before spending a search on candidates. The gate's `sources` check fails while a
registered source is undiffed, overdue, or missing from `docs/compute/watchlist.md`, which is
the only reason this rule survives a session that never read this document.

⚠ **One list is not the market.** Recording 368 of the 369 providers on one list does not make
that list the market. A cheap-VPS tracker listed 128 providers, and **106 of them were
absent**, including one the same topic had already been quoting by name. The error was not a
missing search. It was treating one list as the market.

⭐ **A coverage claim names the list it was measured against, in the same sentence.** "368 of
369 covered" is true of one corpus. "The names are known" is a claim about the world, and the
gate now refuses to let a registered source go undiffed while a document says it.

### 6.1 Map the niche breadth-first

As many searches as the candidate classes need, in both directions: who offers this, and who
exceeds the limit and what the enforcement looks like. The second direction finds the caps the first direction hides.
⭐ **Search the inverse explicitly**: "who exceeds the limit, and what the enforcement looks
like", "X limits reddit", "X suspended my account". The enforcement is never on the pricing
page.

⚠ **A niche that is not Anglophone needs its own language.** Section 8 carries the vocabulary.
An English query finds a Chinese pan drive's marketing page and never its real limits.

### 6.2 Pick what looks real, then go deep

A breadth pass produces many plausible names, and some of them look real. ⛔ **A shallow entry
cannot carry a decision**, so every candidate that looks real goes deep.

⚠ **Do not deepen the list shallowly.** The candidates that look real are the ones where a page
states a number that clears the filter, or a forum thread describes the cap. Each of them gets
the full depth pass, in this unit or in a unit of its own. The rest go on the `seen` list, which
is the next run's starting point.

### 6.3 Probe depth

For each candidate, in this order: the quota page, the terms or limits page, the API
documentation, the changelog, and the forum thread. The order matters because the quota page
states the intent and the forum states the enforcement.

Then run the read-back probe from section 5.2, which is the cheap one: a read-gated host
rejects a single GET, and a write-open host costs an upload to discover. Then run the
throughput benchmark from section 5.6 where the candidate survives that. Then record the
constraint that binds.

### 6.4 Write the records

⭐ **A unit with more than one lane is a run, and a run writes records through one program.**
The lanes propose changes with captures and quotes; `scripts/rq integrate` applies them with
compare-and-set, dedupe and the record's rules. See
[`docs/research-protocol.md`](docs/research-protocol.md).

One file per provider, `dossier/<topic>/<slug>.json`, schema in `docs/conventions/README.md` section 6
and the canonical definitions in `scripts/dossier/schema.json`. The record carries
`evidence[]`, `limits[]`, `identity_cost`, `confidence`, `verified_at` and `verdict`.

⭐ **A record per provider, not per niche.** A file per niche lets the same provider acquire
three quota numbers in three files, each individually defensible because nobody can see the
others. One provider, one file, one home.

⚠ **Keep a `seen` list in the unit's working note** of every provider name encountered,
including ones never opened. In a run, the working note is the unit's `log.md`; outside a run,
it is `.tmp/session-<id>/notes.md`. The unverified names are the next session's breadth
pass, already assembled, and they are the main value of a breadth run. When the unit closes,
the unopened names go into `open_question` operations, which the integrator files in `queue/`;
outside a run, they go into the issue of the work. `.tmp/` is never committed, and a list nobody
can find is a list nobody uses.

⚠ **A rejected provider is a record too**, `verdict: dead` or `verdict: fails-quota`, with the
evidence of its failure. The dead ends are half the value of this corpus, and a dead end with
no record is re-attempted by whoever has the idea next.

### 6.5 Reconcile

The same provider appears under many names. Collapse by vendor and service class, keep the
best-evidenced record, and merge the evidence arrays.

⛔ **Where two records disagree, keep the conservative number and record the
disagreement**, with what would settle it: a line in the record's `notes` and a history entry
if the change is material. A silent choice of the larger number is how the larger of two
disagreeing figures gets published, and nobody downstream can see that a choice was made.

### 6.6 Report

Answer first. The composition, one line per workload with the provider, the ceiling and the
catch. Then the constraints, then the tiers, then registration reality, then the dead ends,
then what could not be verified.

⚠ **A report that opens with its method has buried its answer.** The reader is out of
budget and has already read enough methodology.

⚠ **Tables in a document are generated from the records**, between markers, by
`scripts/report/render.py`. A hand-edited table is a table that will disagree with its
records on the next render, and the disagreement will be silent.

---

## 7. The challenge protocol

A human-verification step or a proof-of-work page is not an obstacle to work through. It is a
signal to change route. Never attempt to pass one.

⭐ **Change route, not effort, and try every route.** The ladder and its commands are in
[`docs/crawler-scraper/free/broker.md`](docs/crawler-scraper/free/broker.md), the broker manual;
every step is a call of `sh scripts/broker/broker.sh`, never a hand-rolled `curl`. Try every rung
of the ladder and every provider pin, with as many reads as each route needs
([`AGENTS.md`](AGENTS.md) section 2 rule 15). A lane has every rung: `scripts/rq capture URL --lane
WS --provider ID` (the pins: each id that `sh scripts/broker/broker.sh status` lists in `providers`
with `read` in its `caps`), and `fetch URL --dump-headers` and `archive URL --at YYYY-MM` written into its
workspace and registered with `scripts/rq capture URL --lane WS --from-file FILE` (lane brief rule 10). Record `unverified: blocked by challenge` only when
every route failed, and name the routes tried, so the next session knows what was ruled out.

⚠ **A route that hangs is over at its timeout; a route that answers is worth reading again.** A
broker refusal with `Retry-After` is not a failed route: read the page again after `retry_at`.

⚠ **Escalate on the evidence, not on the mood.** A 403 from the origin and a 200 carrying a
challenge body are different failures with different next steps. Read the body before
choosing the next route.

⭐ **A closed route is not a closed question.** Before recording anything as not obtainable,
name three routes considered and why each failed. If you cannot name three, you have not
looked.

---

## 8. The forum layer

The forums where practitioners document what actually works are Cloudflare-walled to every
fetch path. Search with `include_domains=` returns the **full post body in the snippet**,
with author and date. For a walled forum it is the only viable read path, and for survey
work it beats page fetching: one query returns twenty threads.

```bash
sh scripts/broker/broker.sh search "无限存储" --count 20 --domains linux.do
```

Snippet length is not a constant. Measured on 2026-10-22 across six runs of three queries at
`count=15` and `count=20`, the median was 540 to 835 characters and the range ran from 242 to
9,143. ⛔ **A snippet is a quotation, not a page read, whatever its length.** A snippet supports
a `reported` claim about what somebody wrote. It does not support a `documented` claim about
what a vendor's page says, and it never supports a number in a table on its own.

⚠ **Do not read a short snippet as truncation.** The distribution is wide and the tail is long,
so a 250-character result beside a 2,000-character one is the broker's ranking, not a failure.
Switching tools on a short snippet wastes the route that was working.

⚠ **A thread is evidence of what somebody believed or hit.** It is not evidence that the
provider does it now. Read the date, and treat a post older than the current quarter as a
lead rather than a finding.

### 8.1 Search in the language of the ecosystem

English queries find the marketing page and never the enforcement. These terms find what
English does not, and each one is a different question rather than a synonym.

| term | language | what it finds |
| --- | --- | --- |
| `白嫖` | zh | obtaining capacity at no cost: where a free tier is actually used, and what broke |
| `福利` | zh | a deal an operator posted, usually with the real cap in the thread |
| `羊毛` | zh | coupon-hunting: the price edge and how codes combine |
| `大盘鸡` | zh | a large-capacity VPS: storage sold as compute |
| `无限容量` | zh | unlimited capacity, and the threads arguing about whether it is |
| `不限速` | zh | no speed limit, which is the claim to test rather than repeat |
| `网盘直链` | zh | a direct link out of a pan drive: the read path |
| `무제한` | ko | unlimited |
| `無制限` | ja | unlimited |
| `бесплатное облако` | ru | free cloud |

⚠ **A translated term is not equivalent.** `无限容量` returns threads about what happens when
you exceed a quota that the vendor calls unlimited. `unlimited storage` returns the vendor's
own page. The first is evidence and the second is the claim.

---

## 9. Reviews

Two review kinds, and they answer different questions. Both are run by somebody who did not
write the material.

### 9.1 The adversarial review

**It tries to break the claim. It does not try to approve it.**

The reviewer takes the shortlist and turns a claim into a number they read themselves today,
or marks it unverifiable. Eight checks per provider:

1. the quota, quoted, with URL and read date. A newer number beats the record's: say
   `changed: yes` and give both.
2. the egress term, quoted. If no egress line exists anywhere, "not published" is the
   finding.
3. the interface, as an exact endpoint or rclone backend, never a category.
4. the identity cost, for a **new** account.
5. a live anonymous probe of the **read** path: status, bytes, and a digest where the object
   is small enough. A 401 is recorded with its shape, because it proves the endpoint exists.
6. throughput at 1, 8 and 32 connections, plus a control from a known-fast host on the same
   machine.
7. the per-unit cap and the retention as two numbers.
8. the failure mode at scale, in one sentence.

⛔ **A reviewer never fixes what it finds.** It reports. The author's judgement stays
separable from the reviewer's, and the record shows which sentences changed because of a
review and which were rewritten by the person who wrote them.

⚠ **A review that reports `changed: yes` on nothing is worth what it cost.** Where the
material is genuinely current, the review says which rows it re-read and what each returned,
so an empty result is distinguishable from an unrun pass.

### 9.2 The completeness review

**It diffs the corpus against the source and finds what fell out.**

Not "is this sentence true" but "what qualifying thing does the narrative never mention".
The corpus automates half of it: a script cross-references every record against every prose
file and prints large qualifying providers that no prose mentions. That is a mechanical
answer to a question a reader would otherwise answer by memory, and memory has never once
been complete.

⚠ **The two reviews are blind to each other's class.** An adversarial pass over a shortlist
cannot see the provider nobody shortlisted. A completeness pass cannot see that a row's
number is wrong.

### 9.3 A pass that reports nothing was too shallow

Where a pass genuinely found nothing, the write-up says **what would have had to be true for
it to fire**. That sentence is the evidence the pass ran at all.

⛔ **That is not a licence to invent a finding.** An empty result beats a manufactured one,
and padding a review costs the next reader their trust in the reviews that did fire.

### 9.4 The mechanical half is a script's job

Anything a check can assert, a check asserts: a verdict outside the legal set, a count that
no longer matches the rows, a record naming a provider the table does not carry, a
`verified_at` older than its class allows, a citation whose URL does not resolve.

⭐ **Doing the mechanical half in one second is what leaves budget for the half that needs
reading.**

⛔ **What no check can answer is whether a claim is true.** That stays with the reviewer.

### 9.5 Two keys

⭐ **Anything that raises trust needs two keys.** The first key is mechanical: the integrator's
evidence check and the rules of `scripts/rq check`. The second key is an independent re-read
of a random sample of each lane's claims from their captures, by another context and, where
one is available, another model (`scripts/rq audit`). A lane never audits itself, because
self-grading skews positive.

⛔ **A lane above the threshold is undone and re-run, not argued with.** The threshold is more
than 10% of decided claims unsupported, or a Wilson 95% upper bound above 25%. Zero errors in 30
audited claims bounds the error rate near 10%; zero in 100 bounds it near 3%.

---

## 10. Drift, staleness and decay

⛔ **This is the repository's central risk.** Every fact in it expires, and the ones that
expire fastest are the ones a reader plans against.

A provider page that was right in March was wrong in June and the sentence did not change. A
quota that was 5 TB became 500 GB with no announcement. A free tier closed to new
registrations, and every table still lists it first.

### 10.1 Every claim that can rot carries `verified_at`

`verified_at` is the UTC instant the claim was last checked, not the day the file was written
and not the day it was last edited. It is stored as `YYYY-MM-DDTHH:MM:SS.sssZ`, the same form
as every other instant in the repository. A day is a rendering of it, never the stored value.
Every record, and every field a verdict rests on.

⛔ **A record without `verified_at` is not a claim.** It is a memory, and the repo does not
carry memories.

⚠ **`verified_at` moves only when somebody actually checked.** A bulk touch of every record's
date is a lie that disables the staleness gate, and it is the fastest way to make the gate
worthless while it stays green. `scripts/dossier/staleness.py` detects one: it compares
`verified_at` against the newest `evidence[].date`, and a gap wider than the policy's
`bulk_touch_tolerance_days` is reported as `bulk-touch` by name. Re-dating a record without
re-reading its sources therefore fails the gate, which is the only mechanical defence this
rule has.

### 10.2 The policy lives in one file, and the script reads all of it

`scripts/dossier/staleness.policy.json` is the policy. It carries three independent windows
per record, and the shortest of the first two is the record's limit.

| window | where | what it says |
| --- | --- | --- |
| the class window | `classes[<confidence>].days` | how fast a rung rots. `measured` 90, `documented` 30, `reported` 14, `inferred` 30, `unverified` 14. |
| the topic window | `topics[<topic>].verified_after_days` | how fast a market rots. 21 to 120 days, per topic. |
| the evidence budget | `topics[<topic>].evidence_after_days` | how long one cited source stays usable. Applied to the oldest evidence row. |

⭐ **The binding number is the shorter of the class window and the topic window.** A `measured`
price is stale in 30 days, not 90, because prices rot faster than measurements do. The topic
window is a ceiling on every class in it. The script computes the minimum; it does not take a
view.

⚠ **A class window is a maximum, and `documented` takes the short end.** The ladder allows a
protocol fact 90 days and a price 30. A record does not say which kind its facts are, so the
class window is the shorter one, which can only move a claim down. A topic whose facts are
protocol facts raises its own topic window and the class window still governs; that is the
conservative direction and it is deliberate.

⚠ **The windows are data, and the document is not the owner.** The numbers above are a reading
of the policy file. Where they disagree, the file is right and this table is the defect. A
session that wants a different number edits the file and says why in its `why` field.

### 10.3 Two clocks, and both must be fresh

Staleness is not one number. A record has two ages, and either can expire it.

| the age | computed from | what a large value means |
| --- | --- | --- |
| `verified_age_days` | `verified_at` against today | nobody has confirmed the record |
| `evidence_newest_days` | the newest `evidence[].date` against today | nobody has read a source for it |

⚠ **A fresh `verified_at` over old evidence is a re-date, not a re-check.** This is the bulk
touch of section 10.1, and it is the specific lie the gate is able to see: the record says it
was confirmed today while every source behind it is a month old. `staleness.py` reports the
two ages as two columns and flags the gap.

⭐ **The report shows both ages, and neither may hide the other.** A session that quotes only
`verified_at` has quoted the field a re-date moves first.

### 10.4 The expiry is a defect, not a warning

A claim past its window is stale, it carries `"stale": true` in its record, and it may not
appear in a recommendation until it is re-checked. ⛔ **A stale row is an open finding**, and a
report says how many rows are in that state.

⚠ **`stale` is computed, never written by hand.** `staleness.py --mark` is the only writer of
`stale` and `stale_checked_at`, and it runs in an own clone: in the research
checkout `--mark` exits 2, because a run changes records only through `scripts/rq`. A
hand-written value is a claim about freshness that the next gate run overwrites, and a record
whose `stale` disagrees with its dates has been edited by somebody who did not want it counted.

⚠ **The arithmetic is the automated part.** The script compares `verified_at` and the evidence
dates to today, against the class window and the topic window, and prints the rows.

⛔ **Until that script runs, the policy is a reading and it is labelled as one.** A gate that
exits 0 without a staleness check has said nothing about staleness. The script exists and
`gate.sh` runs it in CI, so a session that finds it missing reports the gap rather than treating the
green gate as coverage.

### 10.5 Decay is not uniform, and the corpus measured one example

Zenodo's quota held unchanged across three months. A list of volunteer AList instances lost
five of them inside two years, and of 169 hostnames probed, 30 listed a mount anonymously and
one accepted a write ([`docs/netdisk-pan/README.md`](docs/netdisk-pan/README.md) owns the numbers). ⭐ **The class of provider predicts the decay better than the evidence class
does.** A single-operator service decays in months whatever the quality of the page that
described it.

⚠ **That also decides where to spend a re-check.** Five providers a plan depends on, re-measured,
are worth more than fifty volunteer instances re-confirmed, because the instances will be gone and
the five will still be deciding the plan.

---

## 11. Handover

A session ends. Another starts with no memory of it. What survives is what was written down.

### 11.1 What a session must leave

⭐ **The mechanics are [`docs/sessions.md`](docs/sessions.md)**: the `RESUME.md` written at the
start, the summary table printed at the end, and the next prompt. This section is what a session
must *leave behind in the corpus*; that file is the ceremony around it.

| | what it is | what it prevents |
| --- | --- | --- |
| the records | one per provider, schema-valid, with evidence and limits | the next session re-searching the same provider |
| the measurements | the probe command, its output and its digest, cited from the record | a number that cannot be re-run |
| the dead ends | every provider rejected, as a record with `verdict: dead` and the evidence | the same idea, attempted again by whoever has it next |
| the handover | the pull request body of the run, and the follow-up issue for what is left | a session that starts by re-reading everything |
| the history | the ledger line of every changed value, with the old value and the evidence | a corrected sentence with no record of why |

⚠ **The work queue is the open issues labelled `rq:research`, and nowhere else.** A second copy
in a session note, a handover file or a kickoff prompt goes stale the moment an item closes, and
the next session reads the stale one first. The questions that lanes filed are in `queue/`, and
an issue names the ones it covers. The ledger carries what changed and why. `BRIEF.md` carries
what is settled.

### 11.2 The handover entry

⚠ **This section and the next are for a session in an own clone.** A research run
writes no `history/` directory, no row of `README.md` and no line of `BRIEF.md`: in a run, the
ledger (`history/ledger/<run>/`) and the pull request body are the handover, and a stale line of
`BRIEF.md` becomes an `open_question` that names it (`AGENTS.md` section 2 rule 14, section 4).

In an own clone, history entries are dated UTC directories, one directory per event, one file
inside. This repository adds four requirements.

```
history/
  2026-10-22T071503Z/withdraw-zenodo-throughput.md
  2026-10-22T084112Z/tier1-quota-collapsed.md
  2026-10-22T093000Z/close-unit-netdisk-cn.md
  INDEX.md                     generated, newest first
```

- ⛔ **The directory name is full ISO 8601 UTC with seconds and `Z`, and no colons.** A date
  alone cannot order two events on one day, and two events on one day is the normal case here.
  ⚠ The basic form, `2026-10-22T071503Z`, is the repository's, because Windows cannot create a
  directory whose name holds a colon. `history/README.md` carries the same rule.
- ⛔ **One event, one directory, one file.** A session that withdraws a claim, closes a unit
  and opens another leaves three directories. A single summary file makes an event hard to
  cite and impossible to supersede on its own.
- ⛔ **The filename names what happened**, not the topic. `tier1-quota-collapsed.md`, not
  `storage.md`, so a reader can find it from `INDEX.md` without opening it.
- ⛔ **Every superseding entry states the reason and names what took the old claim away.** Not
  "corrected", but "the vendor page read on 2026-10-21 states 500 GB where the 2026-03 page
  stated 5 TB".

A history entry keeps superseded wording verbatim and adds the correction
underneath. This repository adds one requirement: ⭐ **the entry names the evidence that took
the claim away**, so the correction is not a second opinion.

⚠ **The entry carries no session narration.** If it does not change what a future reader
would believe or do, it is a log, and logs live in `.tmp/`.

### 11.3 The front page carries the withdrawn claims

In an own clone (a run files an `open_question` instead, section 11.2):

⛔ **A reader who trusts a page without checking the withdrawn list trusts sentences that are
wrong.**

The list is one table on `README.md`, headed **Withdrawn claims**, and it has three columns:
the claim, what took it away, and where the current correction lives. It sits above the
findings, so a reader meets it before any recommendation. `history/README.md` defines the
table's shape and the rule for what reaches it.

⚠ **The table is short on purpose.** An entry that changes no recommendation stays in
`history/` and does not reach the front page.

### 11.4 The handover is written for a session that distrusts you

The next agent implements from this and cannot ask you anything. Four things it needs, and a
summary usually drops all four.

1. **The negative results**, first. They are the most valuable paragraph and the first one a
   summary cuts.
2. **The claims you are least sure of**, listed, before any recommendation.
3. **What was not tested**, named: platforms, regions, sizes, "no live origin, only a
   redirect".
4. **The exact command** that re-runs each measurement, and the kind of vantage and the date it
   ran on (a residential ISP address, a CI runner), never the machine's own identity.

⭐ **The test is one sentence: could somebody who distrusts you re-run every claim a decision
rests on, without asking you anything?** If not, the unit produced an opinion with citations.

### 11.5 Restarting cold

Read `BRIEF.md` first for the state, then the newest history directory, then the records the
unit touches. Reconcile the three against each other before writing anything.

| what you find | what it means |
| --- | --- |
| the record and `BRIEF.md` agree | start at the next open question |
| the record is newer than `BRIEF.md` | `BRIEF.md` is stale. Trust the record. In a run, comment the stale line on the issue, or file an `open_question` that names `BRIEF.md`; a documents session in an own clone fixes it. |
| a record has no `verified_at` | it predates this methodology. Treat it as `unverified` until checked. |
| a cited URL no longer resolves | the claim is not wrong, it is uncheckable. Mark it and re-probe the host. |
| `BRIEF.md` says a unit is done and the records say otherwise | `BRIEF.md` is wrong. The record is the source of truth. |

---

## 12. What is out of scope

**The published conditions and legality are outside this repository's judgement.** State this
once and do not revisit it in a session.

- ⛔ **Never write a legal caveat.** No sentence tells the reader to verify the published
  conditions before acting, warns that the use may exceed those conditions, or assigns the
  risk of the use to the reader.
- ⛔ **Never exclude a provider because of its published conditions.** A provider that works
  and is registrable is a finding, whatever those conditions say.
- ⛔ **Never write a sentence that pre-empts the reader's decision**, in either direction.
  Not "this is acceptable" and not "this is outside the published conditions".

**Suspension, throttling and data loss are technical reliability facts.** One line per record,
in the `reliability_note` field, naming what happened and what it looked like. "An account was
suspended after 3 TiB in one day, and the bytes were unrecoverable" is a technical note.
A sentence that judges the use against the provider's published conditions is not this
repository's sentence.

⭐ **The distinction is operational, not moral.** A researcher who stops to argue the published
conditions spends the session on a question that is already decided, and the technical fact
that matters, that the account was suspended and the bytes were lost, arrives one sentence
later than it should.

---

## 12a. Three scope facts that are not up for rediscovery

Each of these is a scope fact. A document that violates one is unusable.

### ⛔ No hardware, and self-hosting is the last resort

The corpus assumes no local machine and no purchase of one. The premise is that somebody else
runs the iron.

⛔ **Never recommend, price or compare owning a disk, buying a server, running a homelab,
colocating a box, or keeping a machine at home.** A monthly cost table for a 20 TiB disk
bought outright, with amortisation and an electricity line, is correct arithmetic and an
unusable recommendation when there is no machine to plug it into.

⚠ **The distinction is ownership, not hosting, and a hosted offer always comes first.** A rented
box with a monthly invoice is a service and is often the right answer. A free VM on somebody's
cloud is a service. Software a reader installs and runs itself on that rented or free
machine (self-hosted or on-premises software) is the last resort: it is in scope, but in a list,
a table, a ranking or an answer it comes after every hosted offer, free, trial or paid. It never
carries ⭐ or bold, it is never ranked first, and it is never the answer while a hosted offer
(free, trial or paid) exists. What is out of scope altogether is acquiring, housing
and powering physical equipment.

⭐ **When the honest answer is "cheaper if you owned a disk", say what a managed option
costs instead.** The comparison may be one clause, marked as not applicable here,
and the finding continues from the managed figure. It is never the recommendation.

### ⛔ A missing client tool is not a rejection

The corpus researches **what can be reached**, not what already has a wrapper.

- "No rclone backend", "no public API", "browser only", "cookie-authenticated",
  "would need a wrapper" are notes about the current state of tooling. They belong in
  `tooling`, and nowhere else.
- **A provider is judged on capacity, egress and identity** — the three things that decide
  whether the resource is usable. A wrapper is a weekend; 500 GB of free storage is not.
- 125 records in this corpus describe missing tooling. Filing any of them as a failure is the
  defect this rule exists to stop.

⚠ **The one legitimate exception is technical impossibility**: a service that cannot be
reached by any client at all, such as one requiring a hardware token the provider will not
issue, or one that is browser-only behind a proof-of-work that no automation can pass. Even
then, name it as reachability, not as "no backend".

⭐ **A missing wrapper is an opportunity, not an obstacle.** Where a provider has real
capacity and no client, the finding is that a fork would unlock it. That is a better
finding than a provider that already works, because it is the one nobody has taken.

### ⛔ The target is every cheap resource, not storage

The corpus covers whatever free or nearly free capacity exists: compute, GPU time, model
inference, storage, egress, email, DNS, databases, CI runners, credentials, and anything
else a provider gives away.

⛔ **Never write an introduction, framing paragraph, README or section that narrows the
project to storage.** A session that opens a document saying "where does 20 TiB live" will not
think to look for free GPUs.

⭐ **Judge an opportunity on its own terms.** A free GPU hour is a finding of the same rank
as a free terabyte, and it is often worth more, because model inference is otherwise out of
reach.

---

## 13. Anti-patterns

Each named failure has a cost, and the cost is what makes the name worth having.

**The plausible number.** A figure that fits the pattern and was never seen on a page.
*Cost*: it will be believed, quoted in a recommendation, and it is the one thing in the repo
that cannot be traced. ⛔ A dash is always better, because a blank gets checked.

**The status-code 200.** A 200 read as success. *Cost*: a 106-byte 401 body published as a
model, an HTML error page published as a quota, and a recommendation built on both.

**The marketing quota.** "Unlimited", "no limits", quoted as a ceiling. *Cost*: the number
cannot be multiplied, so every total derived from it is fiction, and the real constraint, an
undisclosed throttle on the write path, is discovered after a stack is built on the
quota.

**The single-stream benchmark.** Throughput reported from one connection with no baseline.
*Cost*: a host that scales linearly with connections is reported as slow, a host already at
line rate is reported as throttled, and the two are indistinguishable in the table.

**The summary instead of the source.** A number copied from another document, or from a
snippet, or from a prior session. *Cost*: two documents that disagree, and the reader trusts
the wrong one. One fact, one home, and the home is the evidence.

**The deleted dead end.** A rejected provider dropped because it did not fit the section.
*Cost*: the next session has the same idea, searches the same way and spends the same effort.
A dead end with no record is re-attempted, and that is not a hypothetical.

**"I could not find it" that is really "I searched twice".** A limit recorded as settled after
two queries. *Cost*: a route is closed for everyone downstream, and the sentence reads as
diligence. Name three routes before recording anything as not obtainable.

**The first explanation that fits.** Section 2.3. *Cost*: the confident, cheap, wrong answer,
with nothing in the output saying so.

**The tidy table.** A table with every cell filled and no dash anywhere. *Cost*: the gaps moved
into plausible values, and the table now hides exactly what a reader needs to know.

**The fixed reviewer.** A review that edits the material as it goes. *Cost*: nobody can tell
which sentences survived scrutiny and which were rewritten by the person defending them.

---

## 14. What this repository does not do

- ⛔ **It does not build a working stack.** No uploader, no scheduler, no migration.
- ⛔ **It does not widen the question.** A second question is a second unit.
- ⛔ **It does not delete its evidence.** Not a capture, not a failed probe, not the run that
  disagreed with the others.
- ⛔ **It does not report a limit as settled.** Three routes considered, or it has not looked.
- ⛔ **It does not touch a repository outside the two it works in.** No issue, no pull
  request, no comment, whatever a tracker says it wants. The harness opens issues and pull
  requests in `f-shy/raw` and comments on issues of `f-shy/fshy.ajam.dev`.
- ⛔ **It does not create an account, pay, buy or provision anything** (`AGENTS.md` section 2
  rule 13). The sign-up gate is the finding.
- ⛔ **It does not write a legal view.** Section 12.
- ⛔ **It does not make a git worktree, a clone or a fork.** All research works in one checkout, and every
  file an agent makes goes under `.tmp/<id>/`, which the merge session deletes with `scripts/rq wipe` after its
  merges, and it never changes the checkout's branch, index, tracked files or git configuration (`scripts/rq`
  writes the run branch with git plumbing) (`AGENTS.md` section 2 rules 8 and 14).

---

## 15. The definition of done

A unit is done when all of these hold, and none is checked from memory.

1. **The question is answered**, including what breaks it.
2. **Every record carries `confidence`, `verified_at`, `identity_cost`, and its
   `limits[]` with the binding kind named in `binding`.** A record missing any of the four is
   not done. The gate enforces `binding` on every record whose rung is `measured` or
   `documented`; a `reported` record may land without it and gains it when its rung rises.
3. **Every `measured` claim has a probe record** a reader can re-run, with status, bytes,
   digest and UTC timestamp, stored in `sources/p/` and cited by its hash.
4. **Every `documented` claim has a URL and a read date**, and a capture in `sources/` where
   the page could be lost.
5. **The dead ends are records**, not prose rows, and the count in `BRIEF.md` matches the
   records on disk.
6. **CI's gate is green on the run's pull request**: no check fails that passes on `main`, and
   none is skipped. A research session does not run the gate itself ([`AGENTS.md`](AGENTS.md)
   section 2 rule 14). ⚠ Where CI fails on a check that is red on `main` too, the handover names
   it, and the unit does not fix it (`BRIEF.md` section 5 names its issue).
7. **The ledger line exists** for every value that changed, with the old value and the evidence
   that took it away.
8. **The handover exists**: the pull request body says what the unit settled, and what is left
   is in an issue.
9. **A reviewer who did not write it has tried to break the strongest claim**, and its
   findings are recorded whether or not they were accepted.

⚠ **A unit whose scope grew re-passes this list against its new scope.** The gate is against
what the work is now.

---

## 16. When to stop

**A unit ends when the question has an answer, not when the subject is exhausted.** The
subject is never exhausted.

Stop at the first of these:

| | |
| --- | --- |
| the question is answered, including what breaks it | write it up |
| the answer is no, and you can say why | this is a result and it ships |
| a cheaper route makes the question irrelevant | say so. That refutation is worth more than an answer. |
| the session is interrupted | report the partial answer and what the next run would settle |

⚠ **"More research is needed" is not a finding.** Name the next question, what it would cost,
and what decision it would change. A sentence that could be appended to any report says
nothing about this one.
