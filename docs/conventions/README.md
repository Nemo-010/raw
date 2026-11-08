# Conventions

How prose, documents, JSON, shell and git are written in this repository.

[`../../METHODOLOGY.md`](../../METHODOLOGY.md) says what the work is. This says what it looks like on the
page. The register is one voice across every file here, and a reader moving between documents
should not notice a join.

⛔ **Where a rule can be checked, it is checked.** `scripts/gate.sh` runs the mechanical half, in CI on every pushed head.
A convention nobody can check is a preference, and a repository full of preferences is how a
reader stops believing the ones that matter.

## Contents

| section | what it covers |
| --- | --- |
| 1 | the register: Simplified Technical English, the markers, the character set |
| 2 | file naming and where each kind of file lives |
| 3 | document structure: headings, frontmatter, tables, citation |
| 4 | numbers, units, currency, rates |
| 5 | timestamps |
| 6 | JSON records |
| 7 | shell and command blocks |
| 8 | git |
| 9 | the mechanical checks |

---

## 1. The register

### 1.1 Write in Simplified Technical English

⛔ **Every document here is written in ASD-STE100, Simplified Technical English.** Not a house
style and not a list of banned characters: a controlled language written so that a procedure
means one thing to every reader, including one reading it in a second language and one reading
it under pressure.

It binds every document, every record's `notes` field, every commit message and every history
entry. There is no looser register for the pages that matter less.

The rules below are this repository's working subset. They are not a summary of the standard,
and the standard is somebody else's document.

**Words**

1. **One word, one meaning, one part of speech.** Pick a term and keep it. "Record" is the
   JSON file. "Document" is the prose page. Do not use either for the other.
2. ⛔ **Never reach for a synonym to avoid repetition.** Repeating the term is correct. A
   varied term makes a reader ask whether you mean something else, and in a technical document
   they are right to ask.
3. **Do not use a noun as a verb or a verb as a noun.** "Action the finding" and "the ask" are
   both refused.
4. **Use the real noun rather than one made from a verb.** "It fails" beats "a failure occurs".
5. **No more than three nouns in a row.** "Provider quota evidence field" has four. Break it
   with a preposition: "the evidence field for a provider quota".

**Verbs and voice**

6. **Active voice.** "The probe records the status", not "the status is recorded".
7. **Simple tenses.** Present for what is true, past for what happened. Not "will have been".
8. **Do not drop the verb.** A heading may. A sentence may not.
9. **Start an instruction with its verb.** "Run the gate before you commit", not "the gate
   should be run before committing".

**Sentences and paragraphs**

10. **One instruction per sentence.** A sentence carrying a second clause between commas is
    two instructions wearing one.
11. **An instruction is at most 20 words. A description is at most 25.**
12. **A paragraph covers one topic and runs to at most six sentences.**
13. **Put the condition before the instruction.** "If the probe exits 2, read the first line",
    not "read the first line if the probe exits 2". A reader who acts on the first half must
    not have acted wrongly.
14. **Put the warning before the step it applies to.** A warning a reader meets afterwards is
    a warning about damage already done.

**Punctuation**

15. ⛔ **A sentence that needs a dash is a sentence to split.** Every spelling of the dash is
    the same defect. Banning the character alone taught agents to write a comma instead, and
    not one sentence got shorter.
16. **No slash meaning "and-or".** Write which one you mean, or write both.
17. **Nothing essential inside parentheses.** A reader skips them. If it matters, it is a
    sentence.

⚠ **Most of this is a reading, and a checker declines it on purpose.** A guard over prose
either passes vacuously or refuses legitimate writing. The register is one of the review
lenses, not a script. What a script can hold is in section 1.2.

### 1.2 The character set

⛔ **Only ASCII, plus these five characters: `⛔` `⭐` `⚠` `✅` `❌`.**

The allowlist covers every tracked text file, not markdown alone.

⭐ **A specimen inside a code span or a fenced block is permitted**, because a page that bans
a character cannot otherwise show a reader which one it means.

⚠ **No emoji beyond the five.** No decorative glyphs, no arrows drawn with characters, no
box-drawing. If a symbol carries meaning a reader must act on, it is a sentence.

⛔ **No literal control bytes in a tracked text file.** A control byte makes the file
invisible to review: `grep` calls it binary and skips it, and `git diff` prints "Binary files
differ". Write it as an escape inside a fenced block.

⛔ **No em dash and no en dash, and no `--` used as one.** See rule 15.

⚠ **This section binds new text.** The router documents (`AGENTS.md`, `BRIEF.md`, `README.md`,
`METHODOLOGY.md`) and some topic documents still carry dashes and other characters outside the
set. Do not copy them; a line you change follows this section.

### 1.3 The three markers

| marker | meaning |
| --- | --- |
| `⛔` | a rule whose violation is unrecoverable, or one already broken here. A hard stop. |
| `⭐` | reach for this first. The highest-value item on the page. |
| `⚠` | a trap. It works until it does not, and the failure is quiet. |

⛔ **`⭐` never marks a self-hosted or on-premises option** ([`../../AGENTS.md`](../../AGENTS.md) section 2
rule 9). Software a reader would install and run itself is the last resort, and a marker that reaches for it
first says the opposite.

⛔ **They do not stack.** No `⛔⛔`. Escalating a marker is how a vocabulary stops meaning
anything: once a page has three levels of stop, a reader has to weigh them, and weighing is
what a marker exists to prevent.

⭐ **Use them sparingly enough that they stay visible.** The ceiling is **30 markers per 100
non-blank lines**. ⚠ No check enforces it yet: `scripts/gate.sh` runs no marker check, so a
page above the ceiling passes the gate today. The ceiling is a review lens until that check
exists, and section 9 lists it as specified and not built.

⚠ **The ceiling refuses the unreadable. It is not a target.** A page at 25 per 100 is already
dense.

### 1.4 Status glyphs are a different tier

`✅` and `❌` report a state in a table or a check result. They never carry a rule, and a
marker never reports a result.

| tier | the set | where | means |
| --- | --- | --- | --- |
| prose markers | `⛔` `⭐` `⚠` | documents | the table above |
| status glyphs | `✅` `❌` | result tables, check output | passed, failed |

⛔ **A `✅` means somebody ran a live request and recorded status and bytes.** It does not mean
"this is good", and it may never be inferred from a vendor page. A `✅` with no probe behind it
is a fabricated measurement, which is worse than an admitted gap.

### 1.5 The failure mode to watch for is metaphor, not marketing

⛔ **The register does not fail on hype. It fails on an ordinary word asked to carry a meaning
it does not have.**

The two substitutions that do most of the work:

- **Replace the adjective with the measurement.** "Fast" becomes the number and its
  conditions. "Robust" becomes what it survives.
- **Replace the metaphor with the mechanism.** "Load-bearing" becomes what breaks when it
  moves.

⚠ **`simply`, `just`, `obviously` and `of course` are the words to watch hardest.** They tell a
reader who is stuck that the thing they cannot do is easy.

### 1.6 No defensive framing

⛔ **Describe what a provider does in plain technical terms.** Do not write a disclaimer
arguing that something is acceptable, and do not tell a future reader not to re-open a
question.

Both backfire. A defensive paragraph primes a skeptical reader to look for the thing it denies.
A grepping agent trips on the reassurance words themselves and spends its budget reading the
matched line.

State the mechanism and its constraint. Stop there.

⚠ **This is not the same as section 12 of `METHODOLOGY.md`.** That section says the published
conditions are out of scope. This one says: having decided that, do not then write the
paragraph you decided not to write.

---

## 2. File naming and where things live

```
docs/<topic>/README.md                 the topic's starting point
docs/<topic>/free/<slug>.md            the free lane, one document per provider class
docs/<topic>/paid/<slug>.md            the cheapest-paid lane, same slugs
dossier/<topic>/<slug>.json            one provider, one record
history/<ISO-UTC>/<slug>.md            one event, one file
history/INDEX.md                       generated by scripts/report/history-index.py
sources/                               captures, script-maintained
references/<owner>__<repo>/            pruned third-party documents, hand-maintained
scripts/<area>/<name>.{sh,py}          instrumentation
```

### 2.1 Slugs

- Lowercase, ASCII, hyphenated: `cloudflare-pages`, `internet-archive`, `m365-a1-education`.
- ⛔ **A slug is a join key**, not a label. It joins the record, the document that cites it,
  and the history entry that supersedes it. Renaming one is a breaking change and needs a
  history entry.
- **One slug per provider**, not per offer. `hetzner` is one provider with a storage box and an
  object store; those are two documents and one record family, distinguished by
  `category` and a qualified slug such as `hetzner-storage-box`.
- ⚠ **A slug that names a marketing tier will age badly.** `tier1` means nothing in six
  months. Name the thing.

### 2.2 Topics

The topic directory names are fixed by `docs/README.md` and the records
use the same names, so a count in one joins a count in the other:
`storage`, `netdisk-pan`, `compute`, `coding-subs`, `inference`, `crawler-scraper`, `debrid`, `egress`,
`email`, `databases-kv`, `domains-dns`, `ci-cd-runners`, `ip-proxy`, `dev-services`, `data-apis`.

⛔ **A new topic is a decision, not a directory.** It needs the name in the `topic` enum of
`scripts/dossier/schema.json`, a row in `docs/README.md`, a README of its own, a window in
`scripts/dossier/staleness.policy.json`, and a line in `BRIEF.md`. ⚠ It also needs the public
repository: the topic in `publish/rules/topics.json` and in the New offer form of
`f-shy/fshy.ajam.dev`, in a public pull request merged before the first publish that carries a
record of the topic (that repository's `publish/README.md`, "The contract between export and build").
Without it, the export stops at its topic check. A topic created by making a
folder is a set of documents nothing routes to. An agent can propose one in a pull request under
the standing rule in [`../../AGENTS.md`](../../AGENTS.md) section 2 rule 12. So a new topic is two pull
requests, the public one first; the one here moves the pin in `scripts/fshy/public.lock`. Rule 12 says what
the public text may name.

### 2.3 Where each kind of content goes

| the content | goes to | because |
| --- | --- | --- |
| a fact a reader acts on now | `docs/` | it is the current answer |
| the machine form of that fact | `dossier/` | one fact, one home, and the record is the home |
| a claim that changed | `history/` | a document says what is true, not what was true |
| a rejected provider | `dossier/`, `verdict: dead` | a deletion re-opens a question that was already answered |
| what a page said on the day | `sources/` | the bytes are the evidence, and the page will change |
| a document that could be lost | `references/` | deliberately small, and pruned to what is cited |
| what is left to do | an open issue labelled `rq:research`, or `rq:operator` for a step that needs a person | the work queue has one home |
| what a run did | the run's pull request body and its ledger lines | the handover is the pull request |
| a unit's working note, its `seen` list and its abandonment condition while the unit is open | in a run, the unit's `log.md`; outside a run, `.tmp/session-<id>/notes.md` | it is scratch until the record exists, and `.tmp/` is the only place scratch lives |
| a file an agent makes while it works | `.tmp/<id>/`, the folder of its run, unit or session | thirty agents share one checkout ([`../../AGENTS.md`](../../AGENTS.md) section 2 rules 8 and 14), and the merge session deletes `.tmp/` after the merge |

⚠ **A unit note is scratch, and it is named so a reader can find it.** The note holds the work in
flight: the `seen` list of every provider name encountered, the abandonment condition written
before the measurement, and the candidates considered. When the unit closes, the `seen` list's
unopened names go into `open_question` operations (in a run; the integrator files them in
`queue/`) or into the issue of the work (outside a run), and the abandonment condition moves into
the record's `notes`. The note itself is never committed.

⛔ **A session log does not go in the tree.** `.gitignore` excludes `.tmp/` for exactly this
reason, and a session note promoted into `docs/` is a diary that a reader has to walk through
to reach a fact.

---

## 3. Documents

### 3.1 Headings

- **One `#` per file**, at the top, and it names the subject rather than the kind of file.
  `# Cloudflare Pages`, not `# Notes`.
- **`##` for a section a reader navigates by.** A reader should be able to answer their
  question from the `##` list alone.
- **`###` for a sub-answer inside a section.** Three levels is the limit. A fourth means the
  document is two documents.
- ⛔ **Never a heading as a link target that changes.** A document in `docs/` that a record or
  a history entry points at keeps its heading text stable. Renaming one breaks the link in the
  record that cites it, and the break is silent.

### 3.2 No frontmatter

⛔ **Documents carry no YAML frontmatter.** The facts that would go in it have homes: the date
and the evidence are in the record, the status is in `BRIEF.md`, and the topic is the path.

⚠ **A document that opens with a metadata block teaches a reader to skip the first screen**,
and the first screen is where the answer goes.

### 3.3 The shape of a provider document

1. **What the class is**, in one paragraph, before any provider is named.
2. **Who is in it**, as a table: provider, free ceiling, interface, identity, binding
   constraint, verdict.
3. **One short section per provider**, each with the numbers, the constraint, the identity
   cost, the evidence and the verdict.
4. **What is dead in this class**, with the reason, linking the records.

⭐ **The answer goes first.** A reader who reads only the table has made no wrong decision.

### 3.4 Paragraphs, not bullet soup

⛔ **A paragraph is the default.** Use a list only when the content is genuinely a set of
items: properties, options, steps that are performed in order.

⚠ **A document that is all bullets has no argument.** The reasoning, which is what a reader
needs in order to disagree with you, only survives in prose.

### 3.5 Tables

- **A header row, then a separator row of `---`.** No alignment colons; they add characters
  and no reader sees the alignment they produce.
- **Every cell carries a value or a dash.** ⛔ **Never an empty cell**, because an empty cell
  looks like an oversight and a dash looks like a finding.
- ⛔ **A dash means unknown. It never means not applicable.** If a field does not apply, say
  why in the cell.
- **The unit goes in the header, not in every cell.** `Ceiling (per object)` once, then
  `256 GiB`, not `256 GiB` in a column called `Ceiling`.
- **Sort by the thing the table is for**, and say what that is in the sentence above it.
- ⛔ **A self-hosted record goes last.** A row whose record carries `self_hosted: true` comes after
  every hosted row, whatever the sort, and no cell stars it, ranks it first or calls it the best or
  the recommended answer, and its first cell says `(self-hosted)`. `scripts/report/render.py` does
  this for a generated table. The gate's `selfhosted` check refuses a list in `docs/` that does not,
  for every row it can tie to records: by a record path, by a backticked slug of the document's
  topic, or by a provider name (whole, cut short, or with more words after it) whose records are all
  hosted or all self-hosted. A row that names a hosted provider and a self-hosted tool is a hosted row;
  a row whose first cell says `(self-hosted)` is a self-hosted row, even when it names no record.
- ⛔ **Prose never presents a self-hosted record as the pick.** In a paragraph that carries a star, or
  that opens "The answer", and in any sentence that says "best", "recommended", "start with" or the
  like, a sentence that names a self-hosted record says in that sentence that it is self-hosted,
  self-run or the last resort. Name the hosted offer first. The `selfhosted` check reads
  the record paths, backticked slugs, bold and linked names, and the provider names of self-hosted
  records in those sentences.
- ⛔ **A table in `docs/` that restates a record is generated**, between
  `<!-- generated:start -->` and `<!-- generated:end -->`, by `scripts/report/render.py`. A
  hand-edited generated table disagrees with its records at the next render, and the
  disagreement is silent.
- ⛔ **A self-hosted or on-premises option is the last row.** In every table and list, a row for
  software a reader would run itself, on any machine, comes after every hosted offer, whatever
  the sort key, and carries no ⭐ and no bold. The render orders generated tables this way once
  the records mark such an offer; order a hand-written list yourself.

### 3.6 Citations

⛔ **A citation is URL, then date, then what it proved, in that order.** Not a bare link, and
not a link with a title.

| write this | not this |
| --- | --- |
| `developers.cloudflare.com/pages/platform/limits/` (read 2026-10-21): 25 MiB per file | [Cloudflare docs](https://...) |
| `help.zenodo.org/docs/deposit/manage-quota/` (read 2026-10-21): 50 GB per record | Zenodo says 50 GB |
| `nodeseek.com/t/1234` (2026-03-12): a 20-file cap observed | according to the forums |

⭐ **"What it proved" is a claim, not a topic.** "The pricing page" proves nothing. "The
per-object cap is 2 GiB, stated in the limits table" proves one thing and can be checked.

⚠ **A citation of a page you did not open is a fabricated citation.** If a number came from
another document, cite that document and say so. Two documents quoting one source with no
check between them drift, and the reader trusts the wrong one.

⛔ **A vendor claim is cited as a claim.** "The page states 5 TB" and "the account holds 5 TB"
are different sentences, and the second one needs a probe.

---

## 4. Numbers, units and currency

### 4.1 Binary units only

⛔ **KiB, MiB, GiB, TiB, PiB.** Never `KB` for 1024, never `MB` for 1,048,576.

| write | means | never |
| --- | --- | --- |
| `256 GiB` | 274,877,906,944 bytes | `256 GB` when you mean the binary value |
| `2 GiB` | 2,147,483,648 bytes | `2 GB` |
| `10 TiB` | 10,995,116,277,760 bytes | `10 TB` |

⚠ **A decimal unit is correct when the provider states one.** A provider selling "5 TB" means
5,000,000,000,000 bytes and the record says `5 TB`. ⛔ **Do not convert a stated decimal figure
into a binary one to make a table look uniform.** The conversion is where a 10% error enters a
plan and is never found.

⛔ **Do not print one unit and label it another.** That is the defect these rules exist to
prevent.

### 4.2 Convert every rate before you compare it

A monthly quota, a per-second shaping number and a port speed are not comparable. Convert to
bytes per day, and say which conversion you used.

| stated | per day | share of 1 TiB |
| --- | --- | --- |
| 12.1 MiB/s | 1 TiB | 100% |
| 100 Mbit/s | 1.08 TB, or 0.98 TiB | 98% |
| 1 MB/s (a vendor's decimal figure) | 86.4 GB | 8% |
| 1 MiB/s (a measured figure) | 84.4 GiB | 8% |
| 1,000 GB per month | 33 GB | 3% |

⚠ **A measured rate goes in MiB/s; a rate a vendor stated stays as stated.** The two rows
above differ by 4.9% and both are correct about different things: the vendor's `1 MB/s` is
1,000,000 bytes per second, and a measured `1 MiB/s` is 1,048,576. Quoting a probe in `MB/s`
understates it, and quoting a vendor page in `MiB/s` misquotes it.

⚠ **Work the arithmetic through in the document where it matters.** `20,000 files x 25 MiB x
100 projects = 47.7 TiB` is checkable by a reader in ten seconds. `47.7 TiB` alone is a number
to be trusted or not.

### 4.3 Currency

⛔ **State the currency, never a bare number.** Write the ISO 4217 code before the amount:
`USD 2.03/TB/month`, `EUR 41/month`, `CNY 258/year`, `PLN 55/month`.

⚠ **The symbol is not enough and `€`, `£` and `¥` are not in the character set.** Section 1.2
allows ASCII and five markers. `$` is ASCII and passes the check, but it is used by a dozen
currencies, so a bare `$` is ambiguous in a corpus that prices in pesos and dollars. The code
is three characters and it is never ambiguous.

- **A price carries its date and its source**, like every other claim.
- **A total derived across currencies carries the rate and the rate date.** `EUR 41 at
  1.09 USD/EUR on 2026-10-21` is checkable. `about 45 dollars` is not.
- ⛔ **Never convert at a rate you did not record.** An unrecorded rate is a number with no
  date, and the conversion is the part that moves.
- **The unit is part of the price.** `USD 1.28/TB/month` and `USD 1.28/TB` are different
  offers, and one of them is a one-time purchase.
- **A lifetime price says so**, and carries the amortisation where a monthly figure is
  compared against it.

### 4.4 Never a fabricated number

⛔ **A dash where the value is unknown.** A wrong number on a report is worse than no number,
because a blank gets checked and a number gets used.

- **A measurement carries its conditions**: machine, date, connection count, sample size.
- **Measured or labelled, never estimated silently.** An estimate is allowed and it says
  "estimated" in the same sentence, every time it appears.
- **A correlation is not a cause.** Naming a culprit is a claim, and a claim needs a control
  that isolates it.

---

## 5. Timestamps

⛔ **ISO 8601, UTC, with `Z`.** `2026-10-22T07:41:03Z`. Not a date alone where a time is known,
not local time, not `22/10/2026`.

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
```

- **A record's `verified_at` is a full ISO instant**, `2026-10-21T09:14:02.418Z`, because two
  checks on one day must be orderable and the schema requires milliseconds and `Z`. A day,
  `2026-10-21`, is how a table renders it; it is never the stored value.
- **A history directory name is second-precision UTC without colons**,
  `2026-10-22T074103Z`, because two events on one day must be ordered and a colon cannot
  appear in a Windows path.
- **A probe record carries milliseconds**, `2026-10-21T09:14:02.418Z`, because two probes in
  one second are distinguishable and the ordering matters when a signature expires.
- ⛔ **Read the timestamp from the machine. Never type one.** A typed timestamp is a memory.
- ⛔ **Never retro-stamp.** A date nobody recorded is not recoverable, and inventing one is
  fabricating evidence.

⚠ **`git log` shows the committer's clock**, which a rebase or a machine in another zone
rewrites. A document that needs to assert when work happened says so explicitly.

---

## 6. JSON records

One provider, one file, in `dossier/<topic>/<slug>.json`. The canonical schema is
`scripts/dossier/schema.json`; this section is the style, and the schema wins where they
disagree.

### 6.1 Shape

This record validates against `scripts/dossier/schema.json` and passes
`scripts/dossier/staleness.py`. Copy it and change the values.

```json
{
  "topic": "storage",
  "slug": "example-host",
  "provider": "Example Host",
  "url": "https://example.invalid/pricing",
  "category": "object storage, S3-compatible",
  "free_tier": {
    "stated": "10 GiB stored free for one account, no card at signup",
    "unit": "GiB",
    "metered_on": "stored-bytes",
    "source_url": "https://example.invalid/pricing",
    "read_on": "2026-10-21"
  },
  "per_object_cap": {
    "stated": "5 GiB per object, stated in the limits table",
    "bytes": 5368709120,
    "source_url": "https://example.invalid/limits"
  },
  "retention": {
    "stated": "until deleted by the owner; no automatic expiry documented",
    "days": null,
    "source_url": "https://example.invalid/limits"
  },
  "egress": {
    "terms": "free and unmetered; the pricing table has no per-GB line",
    "metered": false,
    "source_url": "https://example.invalid/pricing"
  },
  "interface": ["s3", "rest"],
  "interface_detail": "S3 API for object operations; REST for account management",
  "endpoint": "https://s3.example.invalid",
  "tooling": "rclone backend s3, AWS CLI, any S3 SDK",
  "chaining": "direct S3 origin; front it with a CDN when egress locality is the concern",
  "limits": [
    {
      "kind": "request-rate",
      "value": "100 requests per second per account",
      "source": "https://example.invalid/limits"
    },
    {
      "kind": "per-object-cap",
      "value": "5 GiB per object",
      "source": "https://example.invalid/limits"
    }
  ],
  "binding": "per-object-cap",
  "binding_note": "the 5 GiB cap sets the shard size, so it decides the file count before the request rate is reached",
  "identity_cost": {
    "kind": "email",
    "detail": "email and password; no card and no phone at signup",
    "country": null
  },
  "reliability_note": "one account suspension reported after sustained multi-TiB uploads in a day; bytes retained",
  "confidence": "documented",
  "confidence_note": "quota and cap from the vendor pages; the read path was probed, which does not raise the quota above documented",
  "evidence": [
    {
      "url": "https://example.invalid/limits",
      "date": "2026-10-21",
      "capture": "sha256:4b1e8f0c2d7a9e6b3c5d1f0a8e7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b",
      "quote": "Objects up to 5 GiB. API: 100 requests per second per account.",
      "proved": "5 GiB per object and 100 requests per second, stated in the limits table"
    },
    {
      "url": "probe:https://s3.example.invalid/object.bin",
      "date": "2026-10-21",
      "capture": "sha256:9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d",
      "quote": "\"status\": 206",
      "proved": "ranged GET returned 206 with 1048576 bytes and a stable sha256 across two runs"
    }
  ],
  "verdict": "qualifies-with-caveat",
  "verified_at": "2026-10-21T09:14:02.418Z",
  "price_per_tb_month": null,
  "history": [],
  "notes": "suspension cause unverified: an unpublished upload rate or a per-account byte ceiling."
}
```

⚠ **`capture` and `quote` are required on an `http` evidence row dated 2026-10-28 or later, and on
a `probe:` row dated 2026-10-30 or later** (rule C21). `capture` is the hash that
`scripts/rq capture` printed: of the page text, or, with `--probe`, of the probe record. `quote` is
the exact span of that text. The two hashes above are placeholders: copy the shape, never the hash.

⚠ **Five fields are objects, not strings, and two are arrays.** The five object fields are
`free_tier`, `per_object_cap`, `retention`, `egress` and `identity_cost`. The two arrays are
`interface` and `evidence`. A record that writes `"retention": "permanent"` fails the schema
with a type error on that field, and the message reads as the writer's mistake when the cause
is a flat shape.

⭐ **`binding` names the constraint that fails first**, from the same vocabulary as
`limits[].kind`, or `none` when nothing binds above the working scale. The gate requires it
on a `measured` or `documented` record. `stale` and `stale_checked_at` are written only by
`staleness.py --mark`; do not write them by hand.

### 6.2 Style

- **Two-space indent.** One key per line, one array element per line where the element is a
  string.
- **Keys are `snake_case`.** Fixed names; do not invent a synonym for a field that exists.
- **Order the keys as the schema orders them**, so two records diff cleanly.
- **A timestamp field ends in `_at`** and holds a date or an ISO instant. A duration field ends
  in `_days` or `_seconds` and holds a number.
- **A quantity carries its unit in the string.** `"256 GiB"`, not `256` and not `"256"`.
- ⛔ **No trailing comma, no comment, no `NaN`.** A record that does not parse is a record that
  does not exist, and the gate exits 1.

### 6.3 The enumerated fields

⛔ **A value outside its set is a schema failure, not a judgement call.** The sets are closed
so that a count over them means something.

| field | the set |
| --- | --- |
| `verdict` | `qualifies`, `qualifies-with-caveat`, `fails-egress`, `fails-quota`, `trial-only`, `fails-identity`, `dead`, `paid-only` |
| `confidence` | `measured`, `documented`, `reported`, `inferred`, `unverified` |
| `identity_cost` | `anonymous`, `email`, `any-phone`, `country-phone(<cc>)`, `national-id`, `card`, `institution` |
| `limits[].kind`, `binding` | `request-rate`, `pull-count`, `per-ip-shaping`, `per-object-cap`, `write-gated`, `retention-clamped`, `volume-quota` (`binding` also takes `none`) |
| `interface` | `s3`, `s3-compatible`, `rest`, `graphql`, `webdav`, `sftp`, `ftp`, `ftps`, `scp`, `rsync`, `smb`, `nfs`, `ssh`, `graph`, `oci`, `git`, `rclone`, `cli`, `webdav-proxy`, `nntp`, `unknown` |
| `free_tier.unit` | `bytes`, `GiB`, `TiB`, `GB`, `TB`, `MB`, `objects`, `requests`, `seconds`, `minutes`, `hours`, `core-hours`, `gpu-hours`, `credits`, `tokens`, `users`, `unlimited`, `none`, `mixed` |

**The compute units.** `core-hours` is the number of cores times the hours: 8 cores for 1 hour is
8 core-hours. `gpu-hours` is the number of GPUs times the hours. `credits` is a vendor's own unit;
`stated` names what one credit buys when the page says it. Use `hours` only for wall-clock time on a
machine of a stated size.

⭐ **A value that fits no term is a reason to extend the set, not to pick a wrong term.** Extend it
by the route of [`../../AGENTS.md`](../../AGENTS.md) section 2 rule 12: a research agent files an
`open_question` that names the records, and a rules session in an own clone opens the
pull request. Until it merges, use `mixed` and name the true unit in `stated`.

⚠ **`fails-identity` is a verdict, not a note.** A provider whose quota is enormous and whose
registration cannot be completed has failed, and the verdict says so rather than
leaving a reader to find the reason in prose.

**Which verdict a candidate earns.** The four entry filters of `METHODOLOGY.md` section 1 say
what gets a row. These four rules say what the row's verdict is, and the difference between the
top two is whether a probe exists.

| verdict | the condition |
| --- | --- |
| `qualifies` | the free allowance meets the workload of the topic (for storage and netdisk-pan, at least 500 GB free per unit, or trivially repeatable); egress, interface and identity as the filters state; ⭐ **and one probe of a public read path run here, where one exists**. Without the probe, the verdict is `qualifies-with-caveat` with the missing probe named |
| `qualifies-with-caveat` | the same four filters, and at least one real design constraint: a retention clock, per-IP shaping, SAS expiry, a project lifetime, or a write gate |
| `fails-quota`, `fails-egress`, `fails-identity` | it clears some filters and fails that one. The name is the finding. |
| `trial-only`, `paid-only`, `dead` | it was free and is not, it was never free, or it no longer exists. `dead` carries the evidence of its death. |

⚠ **"Reachable interface" is not "an existing client".** The filter asks whether a client
*could* speak to the service — an API, a WebDAV mount, a documented protocol, a cookie
session a wrapper can drive. It does **not** ask whether rclone already supports it. A
provider with real capacity and no backend is a finding, not a rejection: the wrapper is a
weekend and the capacity is not. `METHODOLOGY.md` §12a has the rule.

⚠ **A tier can be unreachable while the provider is not.** Where an API exists on a paid plan
and not on the free one, that is a `qualifies-with-caveat` at the paid tier with the free
tier's limit named — not a `fails-*` for the provider.

⚠ **The probed condition is what separates the top two**, and it is the one a writer skips. A
provider that clears all four filters on a vendor page and was never probed is
`qualifies-with-caveat` with the missing probe named, because "documented to work" is not
"works".

### 6.4 The rules on a record

- ⛔ **One provider, one file.** Two files for one provider is the defect the directory exists
  to prevent.
- ⛔ **Never delete a record.** A provider that died becomes `verdict: dead` with the evidence
  of its death.
- ⛔ **Every claim has an evidence entry that says what it proved.** Not "pricing page", but
  "per-object cap 2 GiB, stated in the limits table".
- ⛔ **`verified_at` moves only when somebody checked.** A bulk touch disables the staleness
  gate and leaves it green.
- ⛔ **No credential in a record.** A record may say a public key exists at a URL. It never
  holds one.
- ⛔ **A self-hosted offer carries `self_hosted: true`.** That is software, or a node, that the user
  installs, runs and maintains on any machine, owned, rented or free: a server, a daemon, a node, an
  operator in the user's own cluster, or a client, app, editor or agent whose free part serves nothing
  itself. The hosted service such software reaches keeps its own record. A record stays hosted when
  the vendor runs the service its free unit or price is spent on, even when the user runs a client, an
  endpoint, a routing daemon or their own application code against it: a hosted allocation (address
  space, a tunnel-broker or relay account), a hosted control plane whose workers the user deploys, or a
  cluster the vendor spins up in a cloud account the user rents. A remote-control account for software
  the user runs, with no capacity of its own, is self-hosted. `false` records a reviewed hosted offer,
  and a record whose category or tooling says self-hosted carries one value or the other. A record
  marked `true` says why: its text names what the user installs or runs, or the `fr amend` that set
  the marker cites a vendor page, not an inherited catalogue card. A self-hosted record is the last
  resort: every list, need and search puts it after every hosted record and never recommends it. The
  field does not change the verdict.

---

## 7. Shell and command blocks

### 7.1 A prose payload goes through a file

⛔ **Write text to a file with a file-writing tool, then pass the path.** This applies to a
commit message, a document, a JSON body, anything multi-line, and anything containing an
apostrophe, a backtick, a dollar sign or a backslash.

⚠ **A quoted heredoc is the last resort, not the first, and it is where sessions go first
anyway.** It is documented to be literal and it is not reliable: a payload passed inline to a
shell had the backticks in its prose executed, and nothing returned non-zero.

| reach for | when |
| --- | --- |
| a tool that writes the file directly | always, if you have one |
| a helper built for it | you are in a shell and the payload is prose |
| base64 through an argument | the payload has to cross a shell |
| a quoted heredoc | nothing. See above. |

### 7.2 An exit code is read unpiped

⛔ **From the process that produced it.** Piping a check into `grep`, `head` or `tee` reports
the pipeline's status, so a guard that failed reads as green.

```bash
sh scripts/gate.sh --root .     # in CI, or in an own clone
echo $?
```

### 7.3 Fenced blocks

- **Tag the language**: `bash`, `json`, `text`, `markdown`.
- ⛔ **Every `bash` block parses.** A block that does not parse is a block nobody can copy.
- ⛔ **No angle-bracket placeholder inside a shell block.** A human reads `<deployment-id>` as
  "fill this in" and bash reads it as a redirect, so the reader gets a syntax error instead of
  an instruction. Use an upper-case name or a quoted variable.
- **A block that produces a value says what the value looks like**, in the sentence after it.

### 7.4 Tool invocation

- **The broker is called through its wrapper**, not by a hand-rolled `curl`.
  `scripts/broker/broker.sh` carries the escalation ladder and the timeouts.
- **A probe is run through `scripts/probe/probe.py`**, so the record it produces carries the
  status, the bytes and the digest without anybody remembering to add them.
- ⛔ **A command that writes outside `.tmp/`, `sources/` or a generated file is a bug.** A
  script that edits a hand-written document has taken a decision away from a person.

### 7.5 Line endings

- **LF in every tracked text file.** `.gitattributes` states it per type; a checker compares
  the working tree against what git resolves.
- ⚠ **`.ps1` is the exception** and keeps CRLF, because Windows PowerShell 5.1 mis-parses a
  here-string whose terminator arrives with a bare LF.
- ⚠ **A carriage return in an LF file is invisible to git and visible to everything else.**
  The index is normalised, so `git diff` shows nothing and a review cannot see it.

---

## 8. Git

### 8.1 No tool is credited

⛔ **A commit credits no tool.** No `Co-Authored-By` trailer naming a
model, no "generated with" line, no tool name in a body, a tag or a release note.

⚠ **A tool's own defaults may ask for such a trailer, and several do.** That is why this is a
hard rule: the failure arrives from a setting nobody chose, on every commit of a session.

```bash
git -c user.name="$NAME" -c user.email="$EMAIL" commit -F message.txt
```

### 8.2 Commit messages

- **A subject that says what changed**, in the imperative, scoped:
  `storage: record Cloudflare Pages file-count bound`
- **A body that says why.** The diff says what.
- ⛔ **The body goes through a file**, never inline to a shell.
- **A body may start with an ISO 8601 UTC stamp** where a project runs many sessions. Read it
  from the machine.

### 8.3 What is never committed

- Credentials of any kind, including expired ones and ones that look redacted.
- Anything under `.tmp/`, which holds scratch, captures and probe bytes.
- Build output, dependency directories, local databases.

⚠ **`.gitignore` applies only to files git is not already tracking.** Adding a line does not
untrack what is in. Check with `git ls-files` before assuming a rule took effect.

### 8.4 History is not rewritten

⛔ **No force push. No rebase of anything published. No amend of a commit that has left the
machine.** A rewrite to remove a secret needs authorisation and a manual run, because the
credential must be rotated first and the rewrite does not un-publish it.

### 8.5 One change, one concern

⛔ **Do not tidy a file while shipping something else.** A commit that adds a record and
reorders ten others is unreviewable, and the review is the only thing that catches the record's
defect.

⭐ **The record, its ledger line and the documents that quote it change in the same pull
request.** In a run, the integrator writes the record and the ledger line, and `scripts/rq land`
re-renders the generated tables. Outside a run, in an own clone, `scripts/fr` writes
the record and the ledger line, and a document that quotes the old number changes in the same pull
request. In the research checkout every change is a run. A session that
updates a record and leaves the document saying the old number has shipped a disagreement, and
the gate will find it on somebody else's turn.

---

## 9. The mechanical checks

`scripts/gate.sh` is the definition of done; CI runs it on every pushed head, and a research
session never runs it in the research checkout ([`../../AGENTS.md`](../../AGENTS.md) section 2 rule
14). It runs every check and exits non-zero on the first defect. `scripts/README.md` is its contract. What runs today, in the order
`ALL_CHECKS` names them:

| check | refuses |
| --- | --- |
| schema | a record that does not parse, or a value outside an enumerated set |
| staleness | a record past its class window, its topic window or its evidence budget, and a record re-dated without its evidence being re-read |
| binding | a `measured` or `documented` record that names no binding constraint |
| links | a link out of `docs/README.md` that does not resolve, or a verified record no document cites |
| attribution | an AI-attribution line, a banned marketing word, or a recommendation to acquire hardware |
| units | a decimal unit where a binary one belongs, and a local-time timestamp |
| tree | a required path that is missing, a document that links into `.tmp/`, or a credential file |
| rellinks | a relative Markdown link anywhere in the tree that does not resolve |
| sources | a registered provider list (`scripts/sources/*aggregators*.tsv`) that is overdue or was never diffed |
| projection | a projection rule that fails its selftest, a public store that does not build, a source value with no disposition, or a leak |
| selfhosted | a list in `docs/` or a need that puts a self-hosted record above a hosted one; a self-hosted row that recommends it or does not say it is self-hosted; a sentence of a starred or "The answer" paragraph, or one that recommends, that names a self-hosted record without saying so; a record whose category or tooling says self-hosted and that carries no `self_hosted` value; or a `self_hosted: true` record with no reason in its text or its ledger entry |
| contradictions | an error violation of `scripts/rq check` that the baseline does not hold |

What is specified and not yet built. Each of these is a real gap, and a session that needs one
reports the gap rather than counting the green gate as coverage:

| check | will refuse | status |
| --- | --- | --- |
| render | a generated table that disagrees with the records it views | `scripts/report/render.py --check` runs in CI as a step of its own; not a check of the gate script |
| markers | more than 30 markers per 100 non-blank lines, or a character outside the five | not implemented |
| manifest | a manifest entry whose digest does not match the file on disk | `scripts/sources/manifest.py --verify sources/` exists and is run by hand ([`../maintenance.md`](../maintenance.md)) |

```bash
sh scripts/gate.sh --root .     # in CI, or in an own clone; never in the research checkout
```

⚠ **A check that is not in the tree has verified nothing.** A session that finds one missing
reports the gap rather than counting the green gate as coverage. Each check also carries an
exit-code contract: `0` passed, `1` found a defect, `2`
bad input, `3` the environment is wrong, `4` the remote refused. A `3` about the broker says
nothing about the corpus, and a `1` in that situation would be a lie.

⭐ **A check that verified zero rows and reported success is worse than no check.** Every check
is demonstrated against a planted defect and must refuse it, and against correct input and must
accept it. A check whose plant passes is a check that is off.

⛔ **What no check can answer is whether a claim is true.** That is the review, and it stays
with a reader.
