# SELFTEST — what was run, and what it proved

Every number below is pasted from an actual run on 2026-10-22 (UTC) on Windows
Git Bash, `python` 3.13.15, `curl` 8.21.0. Nothing here is a description of what
the tools are meant to do; it is a record of what they did, including the cases
where they were wrong first.

Run everything again with:

```bash
python scripts/probe/probe.py --selftest
python scripts/dossier/validate.py --selftest
python scripts/dossier/staleness.py --selftest
python scripts/report/render.py --selftest
python scripts/sources/manifest.py --selftest
python scripts/hygiene.py --selftest
sh scripts/gate.sh --selftest
sh scripts/check-readme-commands.sh scripts/README.md
```

Every count below was re-measured on 2026-10-22 and corrected where the earlier
text was wrong. Where a number moved because the tool changed, the entry says so.

---

## 1. probe.py — the core primitive

### Offline selftest: 33 cases, 0 failed

```text
selftest: 33 passed, 0 failed, 33 total
```

The harness starts a loopback HTTP server and probes it, plus a `data:` URL, so
the whole selftest runs with no outside network. It covers: hashing a `data:`
URL; a plain 200; an empty 200 caught as `false_200.kind=empty`; a single
redirect and a two-hop chain; a honoured range (206) and an ignored one
(`honoured=False`); `--bytes` truncation with the true `Content-Length` retained;
the four false answers (Cloudflare challenge page, JSON error inside a 200,
HTML "404 Not Found" inside a 200, a git-LFS pointer); retry on a 503 with and
without `--retries`; timeout classification; 404; sha256 and byte-count
expectation mismatches; HEAD; a peer that closes early (`truncated-body`);
concurrency with a baseline; the sharded ranged-GET benchmark; and the exception
classifier for TLS, DNS, refused and timeout.

### Against real targets

| target | result |
|---|---|
| `https://example.com/` | 200, 577 bytes, sha256 `25ddf2c883e0…`, `usable: true`, exit 0 |
| `https://www.nodeseek.com/` | 403, `challenge.detected: true`, signature `cloudflare-challenge:title:just a moment...`, `usable: false`, exit 1 |
| `https://expired.badssl.com/` | `error: tls_untrusted`, `tls.handshake_ok: true`, `tls.verify_message: "certificate has expired"`, `tls.cert_der_sha256` recorded, exit 1 |
| same, `--insecure` | 200, 494 bytes, `usable: true`, exit 0 — proving the tool separates "TLS broken" from "host broken" |
| `archive.org/…/stackoverflow.com-PostHistory.7z` `--head` | 302 then 200, `declared_bytes 37747369973`, matching the seed dossier's recorded size |
| the same with `--range 0-1023` | 302 then **206**, 1024 bytes, `Content-Range: bytes 0-1023/37747369973`, `honoured=true` |
| the same, `--shard-bytes 8388608 --concurrency 8` | 8 × 206, 8 388 608 bytes, 1.731 MiB/s parallel vs 1.471 MiB/s baseline, `speedup 1.18x`, ranges honoured |

### Defects found by running it, and fixed

1. **HEAD was reported as an empty 200.** `detect_false_200` fired on every HEAD
   because the body is empty by definition. Caught on the second real probe.
   Fixed by passing the method in and treating HEAD as legitimately bodyless, so
   a HEAD is judged on its declared `Content-Length` alone.
2. **`data:` URLs crashed the false-200 detector.** `urllib` gives a `data:` URL
   no status line, so `status` was `None` and the comparison raised
   `TypeError`. Fixed by synthesising 200 for a `data:` handler.
3. **`--shard-bytes` did not exist.** The first concurrency implementation ran N
   identical GETs, which measures connection setup, not bandwidth — the corpus
   benchmark is N *ranged* GETs against **one** object (rule 6). Added, with a
   one-connection baseline over the same byte span so the speedup is honest, and
   a `declines` flag because OSN gets *slower* under concurrency.
4. **Exit codes did not match the repository contract.** The first version used
   0/1/2/3. `scripts/README.md` fixes 0/1/2/3/**4**, where 4 is "the remote said
   no, retryably". A probe that gets a 429 or 503 now exits 4 so a caller can
   tell "this host is rate-limiting me" from "this host does not have the file".
5. **`--tls-info` was declared but never wired.** Added the second handshake, so
   `tls.cert_der_sha256` and `tls_version` are populated on demand.

---

## 2. broker.sh — the broker wrappers

Exercised against the live broker (`overall: ok`, all six services `ok`).

| invocation | result |
|---|---|
| `status --human` | six services, all `ok`; fetch p95 2900 ms, read p95 15138 ms |
| `read https://example.com/` | Markdown with YAML front matter, `upstream_status: 200` |
| `search "hetzner storage box" --count 3 --domains lowendtalk.com --tsv` | 3 rows of `url<TAB>title<TAB>snippet`, snippets carrying full forum bodies |
| `fetch https://example.com/` | raw HTML bytes |
| `fetch … --head` | origin headers, `x-web-egress` provenance intact |
| `fetch <404 url>` | exit **1** — the page said no |
| `read <404 url>` | exit **1** |
| `read` with no URL | exit **2** |
| `read notaurl` | exit **2** |
| `frobnicate` | exit **2** |
| `BROKER_READ=https://nonexistent.invalid` | exit **3** — the broker is unreachable, nothing established about the target |
| a local server returning a broker-style `503 application/problem+json {"reason":"disabled"}` | exit **4**, message `broker: the broker said no (disabled, HTTP 503); the target was not judged` |

The last row is the whole point of the script: a broker-side refusal is a fact
about the tool, never a finding about the host.

**Defect found and fixed:** the first `search --tsv` emitted `�` for every
non-ASCII character in a forum title, because Windows Python defaults to cp1252.
Fixed by exporting `PYTHONIOENCODING=utf-8` before any helper runs.

---

## 3. verify-dossier.py and dossier.schema.json

### Offline selftest: 20 cases, 0 failed

```text
selftest: 20 passed, 0 failed, 20 total
```

⚠ This section was labelled "21 cases" and the pasted count said 21. The tool
prints **20**, and until this pass it could not run at all: `selftest()`
resolved `dossier.schema.json` beside the script, a name that has never existed
(the file is `schema.json`), and returned 1 before the first case. The count is
the tool's own output, verified by running it.

A valid record passes; then 16 mutations each fail with the right keyword —
missing `per_object_cap`, `confidence: "high"`, unknown topic, bad slug, empty
evidence, evidence with no date, evidence dated `22/10/2026`, `verified_at`
without a `Z`, `verified_at` without milliseconds, a non-URI `url`, an identity
kind outside the vocabulary, a `limits[].kind` outside the constraint
vocabulary, an additional property, an empty `interface`, an unknown `verdict`,
and the seed's `medium` leaking into `confidence`.

### The four real seed dossiers, and all 91 seed waves

The migration was run on **all 91 waves**, producing **1 255 records** — exactly
the seed's own candidate count, so nothing was silently dropped:

```text
files    1255   records 1255
errors   0   warnings 0
verdict  PASS
```

What survived, measured rather than asserted:

| field | result |
|---|---|
| records produced | 1 255 of 1 255 candidates (100%) |
| `verdict` | present on 1 255 (100%) |
| `evidence` rows | 4 009 carried across |
| `interface` | parsed from prose; 128 records (10.2%) have only an unclassifiable description and are marked `unknown` |
| `limits[]` | 0 records left with an empty list; 312 (24.9%) yield a constraint named from the vocabulary |

Where the seed did **not** fit, and what I did instead of dropping it:

1. **`identity_cost` is absent on 792 of 1 255 records (63.1%).** The seed left
   it blank. Defaulting it silently to `email` would have invented a finding, so
   the record carries `kind: "email"` **plus** a `confidence_note` saying it was
   absent, and migration marks `identity_defaulted`.
2. **The seed's confidence scale is `high`/`medium`/`low`, not the five-rung
   ladder.** These are not equivalent — `high` does not distinguish "we measured
   it" from "a vendor page said so". Mapped `high→documented`, `medium→reported`,
   `low→inferred`, and preserved the original verbatim in a new optional field
   `confidence_legacy` so the translation is auditable rather than invisible.
3. **72.6% of records state no per-object cap, and 95.0% state no retention** —
   the two numbers the corpus says must always be separate. They are not
   defaulted; `stated` holds the sentence "not stated in the source record" and
   `extras.per_object_cap_absent` / `extras.retention_absent` record the gap.
4. **Only 3.4% of the 4 009 evidence rows carry a date.** That is a defect in the
   seed, not in the schema. An undated row is stamped with the sentinel
   `0001-01-01` rather than given a plausible date, so `staleness.py` can count
   it as *undated* instead of quietly treating it as ancient or fresh.
5. **`verified_at` does not exist in the seed at all.** Derived from the newest
   date the record itself states, marked `extras.verified_at_derived`; 1 128
   records state no date anywhere and carry the 1970 sentinel plus
   `extras.verified_at_unknown`. Inventing today's date would have marked the
   whole corpus fresh and disabled the staleness gate — the exact lie
   `dossier/README.md` warns about.
6. **Seed `quota_url` fields sometimes append prose after the URL**
   (`"https://… (text read from https…"`). Extracted the URL rather than pass a
   string that fails `format: uri`.
7. **Seed prose has no home for `write_once`, `probe`, `agent_focus`,
   `quota_url`.** All four are preserved under `extras`, which is an open object,
   so nothing was invented and nothing was lost.

### Against the records other agents wrote independently

The live `dossier/` tree — written by other agents while this schema was being
built, without seeing it — validates against it with zero errors and zero
warnings:

```text
files    2107   records 2107
errors   0   warnings 0
verdict  PASS
```

That is the strongest available evidence that the schema matches the contract the
rest of the operation was already using, rather than one I invented in isolation.

### Defects found by running it, and fixed

1. **90 records silently overwritten.** Migrating all waves into one flat
   directory collided on slugs (`1101` became `1165`… then `1255`). Fixed by
   writing one subdirectory per wave, leaving the collision visible for a human.
2. **Slugs truncated mid-word left a trailing hyphen** and failed the slug
   pattern. Fixed by cutting on a hyphen boundary.
3. **`restic` parsed as the REST interface**, and `HTTPS` as S3 — a substring
   match. Fixed with word-boundary regexes.
4. **A missing `--path` reported PASS.** The most dangerous bug of the set: a
   typo in the path produced `files 0, errors 0, PASS`. A silent zero is exactly
   the failure this repository is built to prevent. Now a nonexistent path exits
   2.
5. **`_CURRENT_FILE` truthiness** made migration crash on a list rather than its
   element; caught by the selftest on its first run.
6. **`verified_at` accepted second-resolution timestamps.** The repo requires
   milliseconds and `Z`; the regex now enforces both.

**Fixtures:** `fixtures/dossier-good/` passes; `fixtures/dossier-broken/`
produces **15 distinct errors** and exits 1.

---

## 4. staleness.py

### Offline selftest: 25 cases, 0 failed

```text
selftest: 25 passed, 0 failed, 25 total
```

Covers: a fresh record with both ages reported; a 21-day record stale under
`storage`'s 10-day topic window but not under the 90-day default; **a 32-day
`reported` claim stale under the 14-day class window while the same 32-day
`measured` claim in a 90-day topic is current**; the shorter-window rule; a
recent `verified_at` over 51-day-old evidence failing on the evidence clock; a
20-day re-date reported as a bulk touch and a one-day gap not; undated evidence;
a missing `verified_at`; an unparseable `verified_at`; a `verified_at` in the
future; a record with no rung; every band boundary
(0/7/8/30/31/45/46/90/91/180/181); `--max-days` replacing the binding window; the
shipped policy loading with all 11 topics and all 5 rungs; the four fixtures
below; and the TSV header and row count.

### The four fixtures: each classified as recorded

They live in `fixtures/staleness/`, with their expectations in `expect.json` and a
fixed `as_of` of 2026-10-22, so a fixture cannot start passing because the
calendar moved. Run them with `python staleness.py --fixtures fixtures/staleness`:

```text
PASS fresh.json                 stale=False bulk=False bucket=fresh    limit=45
PASS class-stale.json           stale=True  bulk=False bucket=aging    limit=14
PASS evidence-stale.json        stale=True  bulk=True  bucket=aging    limit=30
PASS bulk-touched.json          stale=True  bulk=True  bucket=current  limit=45
fixtures: all four records classified as recorded
```

| fixture | `verified_at` | newest evidence | rung | what it proves |
|---|---|---|---|---|
| `fresh.json` | 2 days ago | 2 days ago | `measured` | a current record passes |
| `class-stale.json` | 40 days ago | 40 days ago | `reported` | the **class** window binds at 14 days inside a topic that allows 120 |
| `evidence-stale.json` | today | 40 days ago | `documented` | the **evidence** clock fails a record whose `verified_at` is recent |
| `bulk-touched.json` | today | 20 days ago | `measured` | a **bulk touch** is named, not passed |

`class-stale.json` is the case the earlier script could not see: a 40-day
`reported` claim in `domains-dns` passed as fresh because the topic window is 120
days and the script never read `confidence`. `bulk-touched.json` is the case
`METHODOLOGY.md` section 10.1 forbids by name and nothing detected.

### Against the corpus, 2026-10-22

```text
  compute          n=405  stale=350  bulk=350  undated=0    topic=45d  current=350 fresh=55
  storage          n=1705 stale=3    bulk=0    undated=0    topic=45d  fresh=1705
  ...
TOTALS n=2315 stale=353 bulk=350 undated=0
```

The 350 `compute` records are one writer's output: it stamped `verified_at` with
the session date over evidence dated 2026-10-02, a 20-day gap. That is a real
finding about those records, not a tool fault, and it is the finding the old
script could not report. The 3 `storage` records are past their evidence budget
(942, 272 and 752 days). Recorded, not fixed here: another agent owns that
directory.

### What the policy is

`staleness.policy.json` holds three windows, and the script reads all of them:
`classes[<confidence>].days` (the rung), `topics[<topic>].verified_after_days`
(the market) and `topics[<topic>].evidence_after_days` (one cited source). The
binding number is the shorter of the first two. `bulk_touch_tolerance_days` sets
how wide a gap between `verified_at` and the newest evidence counts as a re-date.
`--mark` is the only writer of the `stale` and `stale_checked_at` fields.

---

## 5. gate.sh — the definition of done

### Offline selftest: 8 cases, 0 failed

```text
PASS empty directory passes
PASS broken dossier fails schema
PASS stale dossier fails staleness
PASS KB-instead-of-KiB fails units
PASS AI attribution fails attribution
PASS dangling doc link fails links
PASS clean fixture passes schema, links, attribution, units, tree
PASS --strict fails on a skipped check
gate selftest: 8 cases, 0 failed
```

**The four deliberate failures all fire**, as required:

| fixture | check that catches it |
|---|---|
| `fixtures/dossier-broken/fixture-broken.json` | `schema` — 15 errors |
| `fixtures/dossier-stale/fixture-stale-host.json` | `staleness` — 1 021 days old |
| `fixtures/docs-broken/free/units-and-attribution.md` | `units` — `25 MB per file`, `1024 GB`, `40 kbps` |
| the same file | `attribution` — `Generated with Claude Code`, `Co-Authored-By:` |
| `fixtures/docs-broken/free/broken-link.md` | `links` — dangling target |

An empty directory (only `AGENTS.md`) exits 0, so the gate measures coherence,
not progress.

### Against the real repository

Two runs, before and after the binding check was added. The first is the state the
reviewer found; the second is the state after this session's fixes.

```text
PASS schema      2313 records valid
FAIL staleness   353 record(s) past their class or topic window (350 re-dated without re-checking)
FAIL binding     57 of 256 measured/documented record(s) name no binding constraint
FAIL links       1 problem(s): missing:netdisk-pan/README.md
PASS attribution no AI attribution, no banned marketing words
PASS units       binary units written KiB/MiB/GiB/TiB; timestamps UTC
PASS tree        required paths present; no .tmp links; no credential files

7 checks: 4 pass, 3 fail, 0 skip
```

Every remaining failure is a finding about the tree, not about the gate:

- `staleness` 353: 350 `compute` records re-dated by their writer over 20-day-old
  evidence, and 3 `storage` records past their evidence budget. Another agent owns
  both directories and is still writing.
- `binding` 57: records written before the field existed. The check is new, so
  these are the population it was built to find.
- `links` 1: `docs/netdisk-pan/README.md` is not written yet.

### Defects found in the gate itself, and fixed

1. **Both selftests looked for `dossier.schema.json`, and the file is `schema.json`.**
   `gate.sh --selftest` reported `1 failed` and `validate.py --selftest` reported
   `0 passed` with "not beside this script" on every run. Fixed in both, and the
   two fixture roots now put the schema at `scripts/dossier/schema.json`, which is
   where a real root keeps it.
2. **The staleness summary line did not add up.** It printed `stale=N` beside a
   bucket histogram summing past `n`, because a record can be counted in a bucket
   and again as stale. The summary now ends in one `TOTALS` line with disjoint
   counts, and the gate parses that line instead of summing the topic rows.
3. **`stale=51` on a fresh corpus.** The old gate counted an unparseable
   `verified_at` as stale, so fifty date-only records read as rot. The script now
   separates "unparseable" from "past its window" in the reason text and the
   `flags` column.

### Defects found by running it, and fixed

The first full-repo run produced **four false positives**, and every one of them
was a way to get the gate switched off, so each was fixed rather than tolerated:

1. **`units` fired on prose teaching the rule** — a line literally saying "not
   `22/10/2026`". Fixed by stripping inline code spans before scanning.
2. **`units` fired on a vendor's own decimal wording** — Zenodo really does say
   "50 GB per record". Fixed by skipping lines that carry a URL or a read date.
3. **`units` fired on a price** — "USD 10 per GB" is a rate, decimal by
   definition. Fixed with a price-context exemption.
4. **`units` fired on cloud specs** — "12 GB of RAM", "500 GB a month". These are
   the vendor's phrasing. Replaced a blanket decimal grep with four contexts
   where binary genuinely is correct: a binary multiple with a decimal suffix, a
   per-object cap, a *measured* byte-per-second rate, and `kbps`.
5. **`attribution` fired on "a paid ChatGPT subscription"** — a provider fact,
   not an attribution. Fixed by requiring attribution phrasing.
6. **`links` took minutes.** A `find … | while read` loop spawns processes per
   iteration under Git Bash; on a 403-record tree the check never finished.
   Replaced with `sort` + `comm` set arithmetic and single recursive greps. The
   whole gate now runs in about 4 seconds.
7. **`--root` was resolved relative to `gate.sh`'s own directory**, so
   `--root ../..` silently pointed at the wrong tree. Now resolved with `cd`.

---

## What was not verified

- **No test of `broker crawl` or `broker archive` against a live job.** Both were
  syntax-checked and their request shapes follow the broker's documented
  contract, but I did not submit a real crawl job or fetch real captures, so their
  polling and `--at` handling are `unverified`. Everything else in `broker.sh`
  was run live.
- **`--use-env-proxy` and `--proxy` are untested**; I ran hermetic throughout.
- **The 1970 sentinel is a choice, not a measurement.** 1 128 migrated records
  have no date anywhere in the source, and the sentinel says so rather than
  pretending otherwise. Any consumer must treat `1970-01-01` as "unknown", never
  as "checked in 1970".
