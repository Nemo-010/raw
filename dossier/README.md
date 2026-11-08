# dossier

One record per provider. This is the **source of truth**; every table in `docs/`
is a view of it.

A document tells a reader what to do. A dossier records what we know and how we
know it, in a form a script can check. When the two disagree, the dossier is
right and the document has a defect. That ordering is the only thing that keeps
a corpus of a thousand providers from drifting into folklore.

## Why records, not prose

The storage corpus that seeded this repository reached 1,101 providers across ten
waves. Prose did not survive that: the same provider acquired three different
quota numbers in three documents, and each one was individually defensible
because nobody could see the other two. A single record per provider with one
field per fact cannot disagree with itself. When a fact changes, the record
changes, the document that reads it changes, and `history/` records why.

## Layout

```text
dossier/
  <topic>/
    <slug>.json            one provider, one file
```

No generated index is committed. A second committed copy of the record set would
fork from the first, which is the defect this directory exists to prevent.

⭐ A derived store is built instead, never committed, and rebuilt from these files:
`python scripts/fshy/build.py` writes `.tmp/fshy/local.db` (SQLite) in about 17 s,
and `python scripts/fshy/fr.py` queries and amends it. The published corpus in the
public repository `f-shy/fshy.ajam.dev` is an export of the projection of the
same store. The decision
is recorded in
[`history/2026-10-27T073916Z/a-derived-store-is-built-and-never-committed.md`](../history/2026-10-27T073916Z/a-derived-store-is-built-and-never-committed.md),
and the tool is described in [`scripts/fshy/README.md`](../scripts/fshy/README.md).

`<topic>` is one of the values of the `topic` enum in `scripts/dossier/schema.json`, the same
names as the directories under `docs/`; `scripts/fr help` prints them. A topic with no record
yet has no folder here: the first record that the integrator writes makes it. `<slug>` is lowercase, hyphenated,
and stable. It is the join key between the dossier, the document that cites it,
and the history entry that supersedes it. Renaming a slug is a breaking change
and needs a history entry.

## The record

The canonical schema is `scripts/dossier/schema.json`. The fields that carry the
weight:

| field | what it holds, and the failure it prevents |
|---|---|
| `topic`, `slug` | identity and join key |
| `provider`, `url` | the name a human uses, and the page the numbers came from |
| `category` | the shape: object storage, drive, registry, sandbox, subscription, broker… |
| `tier` | the named plan this record prices: `free`, `pro`, `build`, or the vendor's own label. A provider with two materially different tiers is two records, because their limits differ and a reader acts on one |
| `free_tier` | **object**: `{stated, unit, metered_on, source_url, read_on}`. The offer **and** the unit, and what the unit counts (`metered_on`). Never a bare number |
| `per_object_cap` | **object**: `{stated, bytes, source_url}`. The largest single object. Separate from the total, always |
| `retention` | **object**: `{stated, days, source_url}`. How long bytes survive without a touch. Separate from the cap, always |
| `egress` | **object**: `{terms, metered, free_allowance, source_url}`. The terms, plus whether they are metered, capped or free |
| `interface` | **array** of tokens from the closed set in `scripts/dossier/schema.json` (`scripts/fr help` prints it): `s3`, `rest`, `webdav`, `sftp` and others, `unknown` when no page says. An empty array is a failed record |
| `interface_detail`, `endpoint` | the vendor's own words about access, and the API endpoint. Never a credential |
| `tooling` | what exists today: rclone backend, CLI, SDK, restic, borg. ⛔ **A gap here is never a verdict** — "no rclone backend" and "browser only" are notes about tooling, not reasons to reject. See `METHODOLOGY.md` §12a |
| `chaining` | how it combines with other services into the stack. One sentence; empty is a defect |
| `limits[]` | each constraint as `{kind, value, source}` using the vocabulary below |
| `limits_note` | limit prose that names no vocabulary kind. Kept separate so a reader can see it is unclassified |
| `binding` | the one constraint that fails first at the scale, from the same vocabulary, or `none`. The gate requires it on a `measured` or `documented` record |
| `binding_note` | why that kind and not another, where it is not obvious from `limits[]` |
| `identity_cost` | **object**: `{kind, detail, country}`. `kind` is one of `anonymous`, `email`, `any-phone`, `country-phone`, `national-id`, `card`, `institution` |
| `reliability_note` | one line of technical reliability: bans, throttles, data loss, silent re-encoding. No legal caveat |
| `evidence[]` | **array** of `{url, date, proved, capture, quote}`, where `url` is `https://…` or `probe:<target>`. What each source established, not just that it exists. `capture` (`sha256:<hex>`: the page text under `sources/c/`, or for a `probe:` row the probe record under `sources/p/`) and `quote` (the exact span that proves it) are required on an `http` row dated 2026-10-28 or later and on a `probe:` row dated 2026-10-30 or later (gate rule C21) |
| `confidence` | the ladder rung, defined below |
| `confidence_note`, `confidence_legacy` | why this rung and what would raise it; and the seed's own `high`/`medium`/`low` kept verbatim when a record was migrated |
| `verdict` | `qualifies`, `qualifies-with-caveat`, `fails-egress`, `fails-quota`, `trial-only`, `fails-identity`, `dead`, `paid-only` |
| `self_hosted` | `true` when what the record offers is software, or a node, that the user installs, runs and maintains on a machine (owned, rented or free): a server, a daemon, a node, an operator in the user's own cluster, or a client, app, editor or agent whose free part serves nothing itself. The hosted service such software reaches keeps its own record. A record stays hosted when the vendor runs the service its free unit or price is spent on, even when the user runs a client, an endpoint, a routing daemon or their own application code against it: a hosted allocation (address space, a tunnel-broker or relay account), a hosted control plane whose workers the user deploys, or a cluster the vendor spins up in a cloud account the user rents. A remote-control account for software the user runs, with no capacity of its own, is self-hosted. `false` records a reviewed hosted offer, and a record whose category or tooling says self-hosted while it offers a hosted lane carries it; absent means hosted. ⛔ A self-hosted record is the last resort: every list puts it after every hosted record, and no list stars it, ranks it first or recommends it. It does not change the verdict. In a run, a lane's `set $.self_hosted` sets it (lane brief rule 13); in an own clone, `scripts/fr amend` |
| `verified_at` | the UTC instant the record was last confirmed against the live service, `2026-10-21T09:14:02.418Z` |
| `stale`, `stale_checked_at` | computed by `staleness.py --mark`. Never written by hand |
| `price_per_tb_month`, `probe` | the comparable price at the tier named, and a probe.py record for a `measured` claim |
| `history[]` | links to the `history/` entries that changed this record |
| `notes`, `extras` | the abandonment condition and the candidates considered; and fields migrated from a source with no canonical home |

### The constraint vocabulary

`limits[].kind` is one of:

- `request-rate`: a count of calls per unit time.
- `pull-count`: a cap on how many times a stored object may be fetched.
- `per-ip-shaping`: a throughput or daily-volume limit attached to the caller.
- `per-object-cap`: the largest single object.
- `write-gated`: a curator, review, build recipe or phone PIN stands between the
  account and a write.
- `retention-clamped`: the server silently shortens what the client requested.
- `volume-quota`: a byte allowance over a period, counted per account. Distinct
  from `per-ip-shaping`, which is attached to the caller's network rather than to
  the account, and from `per-object-cap`, which is one object rather than a total.
  A monthly transfer allowance is this and not an object size, which is the
  distinction a first pass got wrong on thirteen records.

⚠ **Seven kinds, and the seventh was added after a review found thirteen monthly
byte quotas filed as `per-object-cap`.** A vocabulary that absorbs every count
answers nothing: the reason `volume-quota` exists is that a monthly counter and an
object cap break in different ways, and a reader needs to know which one they will
meet first.

Naming the kind is mandatory. ⛔ **And the record names which one binds**, in `binding`, because
a list of seven constraints has not decided what breaks first. "1 TB free" with no constraint
named is not a finding; it is the marketing sentence we are supposed to have tested.

### The confidence ladder

| rung | means | requires |
|---|---|---|
| `measured` | we ran it in this repository's lifetime | a probe record: status, bytes, hash, timestamp, stored in `sources/p/` and cited by its hash (`scripts/rq capture --probe`) |
| `documented` | a vendor page said so | the URL and the date it was read. A `sources/` capture is kept **where the page is likely to change or disappear** — a pricing page, a limits page, anything behind a challenge. A stable public documentation page is cited by URL and not copied, because a copy forks |
| `reported` | a third party said so | the URL and date, and the fact that it is third-party |
| `inferred` | reasoning from other evidence | which evidence, and the reasoning in one sentence |
| `unverified` | asserted, unchecked | the reason it could not be checked |

⚠ **The capture is not mandatory, and the reason matters.** An earlier version of this
table said `documented` requires a capture. It does not, and it should not: most records at
that rung predate the capture rule, and `scripts/fr sql` counts them. What the rung requires is
a **date and a URL**, so a reader can tell whether the page was read and how long ago. From
2026-10-28 a new `http` evidence row carries a capture and a quote (rule C21), so a page read
now is kept as read. A rule that every old record must carry a copy would multiply the
repository by an order of magnitude to protect pages nobody expects to change.

A record's `confidence` is the **weakest** rung among the fields that matter to
its verdict. A provider whose quota is documented and whose egress is inferred
is an `inferred` record, and the document says so.

## Rules

- **One provider, one file.** Two files for one provider is the defect this
  directory exists to prevent.
- **Never delete a record.** A provider that died becomes `verdict: dead` with
  the evidence of its death. Deleting it re-opens the question for the next
  session, which will then spend its budget rediscovering the answer.
- **Every claim has an evidence entry that says what it proved.** Not "pricing
  page", but "per-object cap 2 GiB, stated in the limits table".
- **`verified_at` moves only when somebody actually checked.** A bulk touch of
  every `verified_at` is a lie that disables the staleness gate.
- **No credentials.** A dossier may say a public key exists at a URL; it never
  holds a key.

## Checking

Three commands, each of which runs as written from the repository root. The exit
codes are the contract from `scripts/README.md`: `0` pass, `1` a defect was
found, `2` usage error. ⛔ They read every record, so a research agent does not run
them in the research checkout (`AGENTS.md` section 2 rule 14): `scripts/rq integrate`
validates each record it writes, and CI runs the gate on the pull request.

```bash
python scripts/dossier/validate.py --schema scripts/dossier/schema.json dossier/   # CI or an own clone
python scripts/dossier/staleness.py dossier/ --summary                             # CI or an own clone
sh scripts/gate.sh --root .     # CI or an own clone; never in the research checkout, where it exits 2
```

- **`validate.py` needs `--schema`.** The schema is `scripts/dossier/schema.json`;
  there is no default, and naming it is the difference between a check and an
  exit 2. `1` here means a record does not match the schema, and the validator
  prints the file, the JSON path and the reason.
- **`staleness.py` exits `1` when something is stale**, which is a finding, not a
  failure of the command. Add `--stale-only` for the rows that need work, or
  `--summary` for one line per topic.
- **`gate.sh` needs `--root`, and runs in CI or an own clone.** Without `--root` it
  exits 2 and says so; the working form, in CI or an own clone, is
  `sh scripts/gate.sh --root .`. It never runs in the research checkout
  (`git config rq.researchCheckout` is `true`): there it exits 2 outside CI.

`render.py --check` belongs to the documents, not here: it fails when a table in
`docs/` disagrees with these records.

```bash
python scripts/report/render.py --check
```
