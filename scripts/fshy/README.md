# fshy: the derived store and the `fr` tool

`fr` answers questions across every dossier record in one call, and changes a record
without hand-editing JSON. It reads a SQLite store, `.tmp/fshy/local-<HEAD 12>-s<F>.db`
(F is `build.STORE_FORMAT`), that `build.py` derives from `dossier/`, `history/`,
`registry/` and `sources/MANIFEST.tsv`. The store is never committed and never edited:
the JSON in git is the truth.

⭐ **One store per commit, shared.** In the research checkout (`git config
rq.researchCheckout` is `true`) the store of HEAD is fresh when its file exists: the merge
session's `scripts/rq sync` builds it once after each fast-forward, and a call that finds none
builds it, in about two minutes, under `.tmp/fshy/build.lock`, while every other call waits
for that build. In any other clone a store is fresh while no input is newer than it, and every
build writes a new file, `local-<HEAD 12>-s<F>-<UTC>.db`; nothing is ever replaced, because a
reader may hold the old file open. Each build appends one line to `.tmp/fshy/builds.log`. Why there is a
store at all is recorded in
[`history/2026-10-27T073916Z/a-derived-store-is-built-and-never-committed.md`](../../history/2026-10-27T073916Z/a-derived-store-is-built-and-never-committed.md).

Query before you read. A document costs tens of kilobytes and covers one topic; a
`search`, `filter` or `need` costs one to five kilobytes and covers every record.

## What is here

| file | what it does |
|---|---|
| [`build.py`](build.py) | dossier/ to the store: local, public (`--public`, the projection the public repository exports), and the gate's `--check` |
| [`schema.sql`](schema.sql) | the store's tables; the same schema for the local store, the public download and the Worker copy. Its version is `SCHEMA_VERSION` in `build.py`: 3, where 2 added `record.self_hosted` and 3 added `ledger.op`, what a ledger row did (`set`, `confirm`, `append_evidence`, `drop_evidence`, `add_record`, `dead`, `relate`, `undo`, `undo_skipped`, `basis`; NULL for a line of `fr amend`, `add` or `dead`) |
| [`project.py`](project.py), [`rules/projection.json`](rules/projection.json) | the public projection: what is stripped before anything leaves the repository |
| [`derive.py`](derive.py), [`entity.py`](entity.py) | derived columns (identity flags, prices, freshness) and vendor entities |
| [`rules/needs.json`](rules/needs.json) | best-per-need queries, shared by `fr need` and the public build (the code of the wiki and the API, not deployed now) |
| [`fr.py`](fr.py) | the CLI and the stdio MCP server; `scripts/fr` is its wrapper |
| [`primer.py`](primer.py) | the help text, generated from a store; the public API serves it as `/api/v1/help.txt` when it is deployed |
| [`test_fr.py`](test_fr.py) | the selftest; every write runs on a copy. It runs in CI or an own clone, and refuses in the research checkout |
| [`test_prices.py`](test_prices.py) | the price parser's selftest: the exact cases, the unit classes, and every dossier record; CI runs it |
| [`public.lock`](public.lock), [`check_lock_fresh.py`](check_lock_fresh.py) | the pinned public commit, and the check that the pin is not behind a public change of the Worker's rules (needs the network; CI only) |
| [`../../registry/entities.tsv`](../../registry/entities.tsv), [`../../registry/relations.tsv`](../../registry/relations.tsv) | entity overrides and record relations, appended by `fr entity-set` and `fr relate` |

## Start

```bash
scripts/fr help
scripts/fr verify
```

`help` prints the primer: the tables and their key columns, the closed vocabularies with
their meanings, the rules below, and eight SQL queries that run as written. `verify`
builds the store when it is missing (in an own clone, also when any dossier record, history
entry, `history/ledger.jsonl`, registry file or build input is newer than it), and prints one
line. Every read command runs the same check first and says so on stderr when it builds.
`--no-rebuild` skips it. In an own clone, `verify --force` builds a new file of HEAD, and an older
file of the same commit is deleted once nothing holds it open. The research checkout refuses `--force`: its store
is built once, by the merge session's `scripts/rq sync`.

The wrapper needs `sh`; without it, call `python scripts/fshy/fr.py` with the same
arguments.

## Reading

```bash
scripts/fr search hetzner
scripts/fr filter --topic storage --no-card --sort usd_per_tb_month --limit 5
scripts/fr need inference-no-card-no-phone
scripts/fr get storage/hetzner-storage-box --detail full
scripts/fr entity hetzner
scripts/fr worklist stale --forecast-days 30 --limit 5
scripts/fr sql "SELECT verdict, count(*) FROM record GROUP BY verdict"
```

| command | answers |
|---|---|
| `search WORDS [--topic T] [--grp G]` | vendor names first, then full text; each row says which columns matched |
| `filter` | whitelisted filters: `--topic`, `--verdict`, `--grp`, `--confidence`, `--no-card`, `--no-phone`, `--anonymous`, `--iface s3`, `--binding`, `--crypto`, `--max-usd-month`, `--max-usd-tb`; `--sort` and `--order` |
| `get RID... [--detail card or full] [--fields F] [--raw]` | card rows; `full` lists every JSON path of the projected record with its claims, unknown values, history and drift; `--raw` prints the source file as it is in git |
| `entity ID-OR-NAME` | one vendor and all its records |
| `need [ID]` | the best-per-need lists; rows with no parsed number come after the ranked rows, and self-hosted rows after every hosted row |
| `sql "SELECT ..."` | one read-only statement over any table |
| `worklist stale, drift, changes, unparsed, unknown, held` | what needs work: past or near its freshness window, records that disagree, recent changes, numbers that did not parse, placeholders, clauses held back from publication |
| `evidence RID`, `cites PART-OF-URL`, `history RID` | a record's evidence; every record citing a host; ledger lines, history entries and the last ten commits of one record |
| `strip report`, `strip review --rule ID --sample 10` | what the public projection removed, per rule, and the text before it |

### Output

Tab-separated: a header row, one row per result, cells clipped with `...` (`--width 0`
turns clipping off), then footer lines starting `# `. The first footer line is always
`# 20 of 71 rows; offset=20 for more` or `# 5 of 5 rows` (`sql`, which does not count
past its cap, says `# 50 rows; more exist`); the others carry notes such as
`# excluded for NULL usd_per_tb_month: 467`. `--json` on any command gives
`{columns, rows, truncated, total, notes}`.

A card row is `rid, provider, verdict, self_hosted, confidence, identity, card, phone, usd_month,
usd_per_tb_month, stale_on, summary`. `identity` ends in `?` when the identity kind was
defaulted, `card` and `phone` are `yes`, `no` or `?`, and `self_hosted` is `yes` or `no`.

### Rules the answers follow

- `rid` is `topic/slug` and is stable. `rno` is a build-local number; never quote it.
- `provider`, `tier` and `category` are the titles of pages, rows and search hits. In the public store they lose a research note (a review state such as "(revisit)", a cross-reference such as "see candidate entry", a numbered rule of the method, ranking commentary such as "the best ... in the set"): rule `title_rule` (H1) of `rules/projection.json`. The vendor and the product stay, and `rid` and `slug`, the permanent URLs, never change.
- `needs_card`, `needs_phone`, `needs_id`, `needs_institution` are 1, 0 or NULL, and NULL
  means unknown, never no. `--no-card` is `needs_card=0 AND identity_basis='stated'`.
- `identity_basis` says how far the identity columns can be trusted: `stated` (the requirement was read), `inferred` (the kind was worked out from the record's prose or its category; the detail says so) and `defaulted` (the kind is a placeholder). For the last two every `needs_*` flag is NULL, the institution kind included. For `stated`, a clause that names a card or a phone and says it is not stated, not quoted or unverified makes that flag NULL; a clause for an upgrade only does not count; a plain negation is 0; a card kind whose free plan says it needs no card is 0. `--no-card` and the need lists read `identity_basis='stated'`, so both bases are left out on purpose; a query that wants them says `identity_basis <> 'stated'`.
- Whether a record has a free allowance is the claim row `kind='has-free-tier'`: `num` 1 or 0, and no row when it is not known (`derive.free_allowance`). `free_unit` is the unit of the headline offer, and a paid plan carries one too, so it is no test: a paid-only record stores the unit `none`. A free list reads `rid IN (SELECT rid FROM claim WHERE kind='has-free-tier' AND num=1)`, or leaves out `num=0` rows.
  The claim is 1 only where a free allowance is stated: the facet `free_tier_kind` names one, or the free tier names a unit and its text says that something costs nothing (free, USD 0, gratis, 免费 and the like, but not a free trial, a free period or free egress), or that a credit or a grant is given, or the offer is neither a priced plan nor a trial. A priced plan is a record filed as a paid offer (`extras.target_document` under `paid/`) or a free tier text that prices its own sizes (`250 GB $3/mo`); a price after "then", "beyond" or "extra" is an overage and does not count. The dossier schema calls `free_tier` "the headline offer", and the paid storage plans hold their plan size there, so a dedicated server's 64 TB of disks is not a free allowance (live walk 2, W2-01). The claim is 0 for a paid-only or dead record, a summary that opens with "no free", "None." or "No.", and a facet that says none, closed or dead.
- A record is stale on day D when `stale_on <= D`: `stale_on` is the first day past its window, the day
  the gate's `staleness` check first counts it. `verified_basis='inherited'` means
  `checked_on` is only an upper bound.
- A filter or sort on `usd_month` or `usd_per_tb_month` reports how many rows it dropped
  for NULL. `--keep-null` lists them last instead.
- Records with a `duplicate_of` are left out of lists; `--include-duplicates` brings them back.
- ⛔ **A self-hosted record is the last resort.** `record.self_hosted` is 1 when the record carries
  `self_hosted: true`: software, or a node, that the user installs, runs and maintains. Every list
  of records (`search`, `filter`, `need`, `entity`, `cites`, and every `worklist` but `changes`, which
  is a log in time order) sorts on `self_hosted` before any other key, so every hosted record comes
  first and each part keeps its own order. A footer line counts the self-hosted rows. The public
  server sorts the same way. `fr entity NAME` resolves a name by score first: the best-scoring entity
  wins, so an exact name is never beaten by a fuzzy match, and a hosted entity wins only a tie
  (`resolve_entity`, the twin of `rank.resolveEntity`). A wholly self-hosted result says so in a
  footer line.

### Prices: what `usd_per_tb_month` is

`record.usd_per_tb_month` is the price of **one TB held or allowed for one month, in USD**, and nothing else. It is
read from the free text of the dossier field `price_per_tb_month` by `derive.price_claim`, whose docstring is the
rule. The text becomes one `claim` row at `$.price_per_tb_month`, and the claim says what the number is:

| what the text states | `claim.kind` | `unit`, `per` | feeds |
|---|---|---|---|
| a price per TB per month, or per TiB (divided by 1.0995), per GB (x 1000), per GiB (x 1e12/2^30), per year (/ 12), per 30 days, per day (x 30); a monthly price for a stated volume (`EUR 26.99 for 16 TB`) | `price-per-tb` | `TB`, `month` | `usd_per_tb_month` |
| a flat price per month or per 30 days, with no volume (`EUR 4.50/month subscription`) | `price` | none, `month` | `usd_month` |
| several per-TB figures "at N TB" that are one flat price divided by volumes the text picks, in a text that calls the plan flat or unlimited (`$0.43/TB/mo at 30 TB` of a flat `$12.99/mo 'Unlimited'`) | `price`, parse `partial` for the figures; the flat price when the text states one | as stated | the flat price feeds `usd_month`; nothing feeds `usd_per_tb_month` |
| any other price: per GB with no period, per IP, per domain, per minute, per million operations, per year, a credit, no period | `price` | its own unit and period | nothing |
| a number that was read and passed over: an egress or retrieval fee, a lifetime price, a promotion | `price`, parse `partial` | its own, period `once` for a one-time price | nothing |
| no money amount (`n/a`, `unverified`) | `price-per-tb`, parse `unparsed` | NULL | nothing |

A stated per-TB figure beats one worked out from another unit, and the cheapest stated tier counts. A figure with no
period is monthly only in the topics whose price field is the price of a stored TB (`storage`, `netdisk-pan`); in
debrid, egress and the rest a per-TB price with no period is a one-off price per TB and stays a `price` claim. A
price in a currency with no dated rate keeps the currency and has a NULL `usd`; no rate is guessed, so a PLN price
fills in when a record cites a PLN rate in `extras.fx`.

What is never a TB-month price: an operations price (per million requests), an egress, delivery or retrieval fee, a
total bill, a credit, a price per minute, hour, IP, domain, vCPU or account, a promotion (the text names the steady
price), another vendor's price, a figure the text calls workload, all-in or effective, a number in a text that says it
has no per-TB price, and a lifetime or one-time price. A lifetime deal gets NULL: its amortised figure ("over 5
years") rests on a horizon the record's author picked, and the records amortise the same deal over anything from 2 to 20
years, so the column would rank deals by a guess. The one-time price stays in the claim (`per = once`).
A cheapest tier of zero is a free tier, and a zero is never a price to rank by.

### Prices: what `usd_month` is

`record.usd_month` is the price of the offer **kept for a whole month, in USD**. It is the cheapest monthly list
price that the record states (`extras.monthly_usd`, the monthly price that `extras.price_on_page` prints, or a flat
monthly price of the price text); without one, the price of the machine run 24 hours a day for a month
(`extras.m24h_usd`); without that, the cheapest other monthly `price` claim. The 10-hours-a-day figure
(`extras.m10h_usd`, 300 hours at the hourly rate) is a claim with the unit `10 hours a day` and never feeds
`usd_month`, and neither does the renewal price (`extras.renewal_usd`), which the records write per month and per
year. Live walk 2 (W2-02) found 61 compute records ranked on the 10-hours figure. `build.py --check`, which the
gate's `projection` check runs, fails when a `usd_month` is below a monthly list price that its record states, or is
the 10-hours figure (`derive.price_violations`).

`claim.kind` keeps the names the public repository reads (`price-per-tb`, `price`, `free-quota`, `limit:*`); no kind is
added. The public primer's example query on `kind='price-per-tb'` now lists TB-month prices only, and the pages'
"Parsed numbers" list prints the unit and the period the claim carries. `test_prices.py` checks that every non-NULL
`usd_per_tb_month` has a claim in unit TB per month, and that a record stating `X/TB` in its price text gets one of
the stated figures, converted at the repository's dated rate.

### Search ranking

The ranking is the same arithmetic as the public server's (`site/worker/rank.js` and
`site/worker/text.js` in the public repository); `test_fr.py` runs those files under node when a
checkout of it is beside this one, and skips the check otherwise.

Names first. The query and every alias are normalised: NFKC, casefold, combining marks
stripped, whitespace collapsed. An entity scores its best alias: 100 when the alias equals
the query, 60 when it starts with it, 40 when it contains it, else 30 when every query
word meets a word of that same alias within its budget: one edit for words of four to
seven characters, two for eight or more, and an exact match for shorter words (plain
Levenshtein distance). A query word that repeats counts once, and a query of more than
eight distinct words gets no fuzzy tier (each word is compared with every word of the
index, so a long query would cost one full pass per word); exact, prefix and substring
still apply. Entities sort by score, then best verdict (`entity.best_vorder`, the best
verdict of the entity's hosted records, or of all its records when every one is self-hosted),
then eid, and an entity whose every record is self-hosted comes after every other entity
(`sort_entities`, the twin of `rank.sortEntities`); their records come first, best verdict first. A name hit lifts every
record of its vendor only when the vendor's own name or domain scores as well as the alias that matched; when the alias
is one record's name ("Google Cloud Storage Always Free tier"), it lifts the records whose own provider or slug scores
that well, and the vendor's other records rank by their text like any other record (`name_hit_records`, the twin of
`nameHitRecords` in `site/worker/api.js`; live walk 2, W2-11). `matched` says `name(exact)`, `name(prefix)`,
`name(substring)` or `name(fuzzy)`, followed by any full-text columns. A Chinese,
Japanese or Korean name works as typed.

Then full text over `text_fts`. The normalised query is split into words; a CJK run longer
than one character becomes its overlapping bigrams, a word with punctuation becomes a
quoted phrase, and a plain word of three or more characters becomes a prefix `word*`; a term
that repeats is kept once, and the terms are AND-ed. Rows are ranked by Okapi BM25 from
`matchinfo(text_fts, 'pcnalx')`, then by verdict, then by rid:

```text
score  = sum over query term i and column j of
         w_j * idf_ij * tf_ij * (k1 + 1) / (tf_ij + k1 * (1 - b + b * len_j / avglen_j))
idf_ij = ln(1 + (N - df_ij + 0.5) / (df_ij + 0.5)), always positive
k1 = 1.2, b = 0.75, df_ij = rows with a hit for term i in column j
w = name 4, offer 2, limits 1.5, egress 1.5, identity 1.5, access 1, notes 1, evidence 0.7, extras 0.5
```

`fr` registers this as the SQL function `fr_bm25(matchinfo(text_fts, 'pcnalx'))`, with
`fr_matched(...)` for the matched columns, for its own `search`. Do not rely on them in
`fr sql`: it applies the public server's guard, which allows a fixed list of functions.
Records with a `duplicate_of` are left out unless `--include-duplicates`.
Last, the whole list, name hits and then text hits, is split in two: every hosted record in
that order, then every self-hosted record in that order.

### Read-only SQL

`fr sql` opens the store read-only (`mode=ro` and `PRAGMA query_only=ON`) and applies the
public server's guard before running anything. String literals, quoted identifiers and
comments are blanked first (an unterminated one is refused). Then it refuses more than one
statement (one trailing `;` is fine), a first keyword other than SELECT, WITH, VALUES or
EXPLAIN, and any of INSERT, UPDATE, DELETE, REPLACE, UPSERT, CREATE, DROP, ALTER, ATTACH,
DETACH, PRAGMA, VACUUM, REINDEX, ANALYZE, BEGIN, COMMIT, ROLLBACK, SAVEPOINT, RELEASE,
TEMP or TEMPORARY anywhere else. That includes the `replace()` function: use `substr()` and
`||`. A statement with no LIMIT gets `LIMIT n+1` on a line of its own, so the footer can say
whether more rows exist (n defaults to 50, at most 200). `pragma_table_info('record')` is a
table-valued function, not a PRAGMA statement, and works.

## Changing a record

⛔ **Not in the research checkout.** There, `amend`, `add`, `dead`, `relate` and `entity-set`
refuse and exit 2: a record changes only through a run, and a one-record fix is an `amend` run
with one unit, `scripts/rq open amend TOPIC "RID: what is wrong"`
([`../../AGENTS.md`](../../AGENTS.md) section 2 rule 14). A hand change belongs to a session that
the operator starts in its own clone; this section is for that clone.

Five commands write. Each one edits files in the working tree and nothing else: it
never commits, never deletes, and never touches `.tmp/` except to build the store
afterwards (`--no-rebuild` leaves that to `fr verify`). Each prints a diff summary of at
most ten lines and a commit subject with no full stop. `--dry-run` shows the change and
writes nothing.

⚠ **An `http` evidence row dated 2026-10-28 or later needs `--capture` and `--quote`**, or the
gate's rule C21 fails it (a `probe:` row from 2026-10-30). Capture the page first, into a
session folder (`scripts/rq folder session` makes it):
`scripts/rq capture URL --lane .tmp/session-<id>` prints `sha256:HASH path`; open the path and
copy the sentence that proves the value. `fr` finds the capture in any `.tmp/*/captures/` or
`.tmp/*/units/*/captures/`. `fr` warns before it writes a row without them, and copies
the capture into `sources/c/` (a probe record, registered with `--probe`, into `sources/p/`).

```text
scripts/rq capture https://www.hetzner.com/storage/storage-box/ --lane .tmp/session-ID
scripts/fr amend storage/hetzner-storage-box '$.free_tier.stated' '1 TB (BX11) ...' \
    --evidence https://www.hetzner.com/storage/storage-box/ --date 2026-10-28 \
    --capture sha256:HASH --quote "the sentence of the page that states it" \
    --proved "plan table lists BX11 at 1 TB" --rung documented --verified
scripts/fr add storage/example-host --provider "Example Host" --url https://example.com/pricing \
    --evidence https://example.com/pricing --date 2026-10-28 --proved "pricing page lists 1 TB free" \
    --capture sha256:HASH --quote "Free plan: 1 TB"
scripts/fr dead storage/example-host --cause free-tier-removed --observed 2026-10-28 \
    --evidence https://example.com/pricing --proved "pricing page no longer lists a free plan" \
    --capture sha256:HASH --quote "Plans start at USD 5"
scripts/fr relate storage/a duplicate_of storage/b --evidence https://example.com/ \
    --date 2026-10-28 --reason "one plan page, two records"
scripts/fr entity-set storage/a example --name "Example" --reason "same vendor under a second domain"
```

| command | writes |
|---|---|
| `amend RID PATH VALUE` | one value. PATH is `$.key.sub`, `$.list[2].value` or `$.extras."A key".x`; VALUE is JSON when it parses as JSON, else a string (`--string` forces a string). The evidence `{url, date, proved}` is appended to `evidence[]` |
| `add TOPIC/SLUG` | a schema-complete skeleton: unknown fields hold `not stated: ...` placeholders, `interface` is `["unknown"]`, the identity kind is marked defaulted, confidence is `unverified` unless `--rung`, the verdict is `trial-only` unless `--verdict`, and `extras.placeholders` lists every placeholder path. It refuses an existing rid and names existing entities with a similar name or the same domain |
| `dead RID` | `verdict: dead` and `extras.death = {on, cause}`, plus the evidence. Causes: dead-service, registration-closed, free-tier-removed, revoked, acquired |
| `relate SRC KIND DST` | a row in `registry/relations.tsv`: duplicate_of, variant_of, successor_of or same_offer_as. A second duplicate_of for one record, and a cycle, are refused |
| `entity-set RID EID` | a row in `registry/entities.tsv`; the last row for a rid wins |

What the record writes guarantee:

- **Validation first.** The whole record is checked against `scripts/dossier/schema.json`
  with `scripts/dossier/validate.py`. On any error nothing is written and the exit code is 1.
- **Refused paths.** `stale` and `stale_checked_at` (computed by `staleness.py`), `topic`
  and `slug` (a rename is a new file and a history entry), `verified_at` (use
  `--verified`), and any top-level key outside the schema. Free-form fields go under
  `$.extras`. A refused path exits 2.
- **The rung only goes down.** `--rung` weaker than the record's confidence lowers it, on
  the ladder measured, documented, reported, inferred, unverified; a stronger rung never
  raises it. Raising `$.confidence` by path needs a `--rung` at least that strong. Inside a
  run it is the other way: a lane's change at a weaker rung than the record's becomes a
  conflict, and no lane operation lowers a rung. Lowering one is this command, in a pull
  request of its own.
- **Time comes from the clock.** `--verified` sets `verified_at` to the machine's UTC time
  with milliseconds. Evidence dates in the future are refused.
- **Minimal diffs.** Unchanged values are copied from the file byte for byte, so key
  order, the file's indent (2 or 1 spaces), its line endings (LF or CRLF), its trailing
  newline and any single-line objects survive; only changed lines differ. Non-ASCII text
  is written as itself.
- **A ledger line.** `amend`, `add` and `dead` append one JSON line to
  `history/ledger.jsonl`: `{"at", "rid", "path", "old", "new", "rung", "evidence": {"url",
  "date", "proved"}, "reason"}`, with `at` from the clock. When the change also lowered
  the confidence or moved `verified_at`, an `also` object carries those old and new values.
  Repeating an identical change writes nothing.

Exit codes: 0 done, 1 a defect or a refused write (validation failed, the rid exists, the
row is already recorded), 2 usage (bad arguments, a refused path).

## MCP

`fr mcp` serves the eight read operations of the public server (help, search, filter,
get, entity, need, sql, worklist) over stdio: JSON-RPC 2.0, one message per line,
protocol 2025-06-18 or later. Each tool answers with the same TSV text the CLI prints.
Each tool registers a stdio server in its own way; the command to register, run from the
repository root, is:

```text
python scripts/fshy/fr.py mcp
```

## Checking

```bash
python scripts/fshy/test_fr.py
python scripts/fshy/test_prices.py
```

The selftest checks the SQL guard, the full-text query builder and BM25, and, when node
is installed, runs the public server's `rank.js`, `text.js` and `guard.js` on the same inputs and
requires identical answers. It round-trips every dossier file through the writer and
requires byte-identical output; then copies a few records (an LF, a CRLF, a one-space
and an inline-object file among them) into a temporary repository and runs every write
there: minimal diffs, the ledger, validation failures and refused paths that leave the
file untouched, rung lowering, `dead`, `relate`, `entity-set`, `add`, the rebuilt store,
every read command and an MCP session. It ends by confirming the real records and ledger
were not touched. `--real` adds read-only commands against the real store and prints
their output sizes. `python scripts/fshy/check_lock_fresh.py --selftest` is the selftest of the pin-age check.

### Parity with the public Worker

`fr.py` and `build.py` hold Python twins of the public Worker's rules: the text rules (`text.js`), the
ranking (`rank.js`) and the read-only SQL guard (`guard.js`). The twins must give the Worker's answers.

- ⭐ **The public commit is pinned** in [`public.lock`](public.lock). The CI job `parity` checks out that commit
  of `f-shy/fshy.ajam.dev`, never its moving `main`. `test_fr.py` reads the Worker at the pin: from
  `$FSHY_PUBLIC` (CI) or from a checkout named `fshy.ajam.dev` beside this one. When that checkout is at
  another commit, it reads the pinned commit's `site/worker/` from git into `.tmp/fshy/`, and the checkout is
  not changed. When the checkout does not hold the pinned commit, the parity check does not run, and CI
  (`FSHY_REQUIRE_PARITY=1`) fails.
- **The fixture.** `site/worker/test/parity.json` at the pin holds inputs and the JavaScript outputs of each
  rule. `test_fr.py` runs the Python twin on every case and requires the same output (a score within 1e-9).
  When the pinned commit has no fixture, the test prints `skip  parity fixture` and says which commit it read;
  the live comparison under node still runs.
- **The export contract.** The same check compares `schema.sql` (comment lines aside), `rules/needs.json` and
  the topic enum of `scripts/dossier/schema.json` with `publish/schema.sql`, `publish/rules/needs.json` and
  `publish/rules/topics.json` at the pin. A change to one of them lands in the public repository first, like a
  rule change, so a merge here never stops the next publish. It also compares the titles of ledger rows in `fr.py`
  (`LEDGER_TITLE`, `LEDGER_NO_OP`, used by `worklist changes` and `history` on a store that holds no old or new
  value) with those of `site/worker/api.js` at the pin.
- ⚠ **A rule change that touches both repositories goes in this order.**
  1. The public pull request changes the rule in `site/worker/` and regenerates the fixture
     (`node site/worker/test/parity.mjs --write`). Its own CI checks the fixture. Nothing here turns red,
     because the pin has not moved.
  2. A merge session merges it. Note the merge commit.
  3. One pull request here changes the twin (`fr.py` or `build.py`) and moves the line in `public.lock` to that
     merge commit, together. Its `parity` job checks the new twin against the new rule.
  4. A merge session merges it. Until then, the published Worker and `fr` can disagree on the changed rule; the
     published corpus and, when they are deployed again, the wiki and the API are built from the public
     repository, so a reader sees the public rule.

  A change in the other direction (the twin first) follows the same order with the roles swapped only when
  the public side already holds the rule. Never move the pin to a commit that is not on the public `main`
  except to test a public pull request that is not merged yet, and then say so in the pull request: the
  merge session moves the pin to the merge commit before it merges.
- **The pin is checked for age.** The job `lock-fresh` of the workflow `f-research-ci` in
  `f-shy/fshy.ajam.dev` runs `python scripts/fshy/check_lock_fresh.py` every day; a pull request that changes
  the pin runs `sh scripts/research/ci-checks.sh lock` in its own clone. It asks the GitHub
  API for the newest commit of the public default branch that changed `site/worker/guard.js`, `rank.js`, `text.js` or
  `test/parity.json`, and fails when the pin does not contain it. Ancestry decides, not the date. Exit 0 is fresh, 1 is
  stale (the pin is behind a public rule change: do the steps above), 2 is a failure to ask, which is not a stale pin.
  `gate.sh` does not run it, because the gate is offline, and the `parity` job does not run it, because a public merge
  must not turn an unrelated pull request here red. `python scripts/fshy/check_lock_fresh.py --selftest` runs its
  tests with no network. `docs/maintenance.md` says what a red result means.

Typical output sizes on the real store, in characters (divide by about four for tokens):

| command | characters |
|---|---|
| `search hetzner` (20 rows) | 5,000 |
| a two-character Chinese name (17 rows) | 4,400 |
| `filter --topic storage --no-card --sort usd_per_tb_month --limit 5` | 1,300 |
| `need inference-no-card-no-phone` (20 rows) | 4,600 |
| `worklist stale --forecast-days 30 --limit 5` | 1,500 |
| `get storage/hetzner-storage-box --detail full` | 5,600 |
| `entity hetzner` (20 records) | 4,600 |
| `help` | 7,200 |
