# history

Superseded claims, abandoned directions, and the narrative that does not belong
in a document a reader navigates by.

A research repository has a problem a software repository does not: its claims
**die**, and the death is the finding. A provider that offered 1 TB in March and
10 GB in October is not a corrected typo. It is a data point about how that
market behaves, and deleting it destroys the only evidence we have that it will
happen again to the next provider. So nothing here is deleted. It is superseded,
in public, with a reason.

## Layout

```text
history/
  <YYYY-MM-DDTHHMMSSZ>/         one directory per event, UTC, second precision
    <slug>.md                    one file per event
  INDEX.md                       generated; one row per event, newest first
  ledger.jsonl                   one line per value that scripts/fr changed: old value, new value, evidence
  ledger/<run>/<unit>.jsonl      the same for a research run, written by scripts/rq integrate
  ledger/<run>/manifest.json     the run manifest that scripts/rq land commits for the merge session
```

⭐ **The ledger is the history of a changed value.** `scripts/fr` and `scripts/rq integrate`
write a line for every change, with the old value and the evidence, so a changed value needs no
hand-written entry here. A `<YYYY-MM-DDTHHMMSSZ>/` entry is for an event a reader must understand
beyond the old and the new value: a correction of a whole document, an abandoned direction, a
ruling.

The directory name is the moment of the event, not the day. Two sessions on the
same day get two directories and cannot collide. The `Z` is mandatory; local
time is a defect, because these directories are read across machines and a
reader cannot tell `2026-10-22T074103` in Warsaw from the same string in Tokyo.

⚠ **No colons in the directory name.** The extended form `2026-10-22T07:41:03Z`
is valid ISO 8601 and Windows cannot create it: `os.mkdir` returns `WinError 123`.
The basic form carries the same information and this repository is built on
Windows, so the basic form is the repository's.

A file inside is named for what happened, not for the topic:
`tier1-quota-collapsed.md`, not `storage.md`. One event, one file, so a reader
can find it by reading the index.

## What belongs here

| kind | example | why it is not in `docs/` |
|---|---|---|
| **superseded claim** | a provider's quota was 1 TB, is now 10 GB | `docs/` states what is true now, not what was true |
| **abandoned direction** | "we spent a wave on academic DSpace installs and 83 of 149 had no quota, but every one required institutional identity" | the conclusion is in `docs/`; the road there is not |
| **a dead end worth remembering** | a whole class of hosts that looked identical from outside and all failed the same way | the dead-end table carries the verdict, not the story |
| **a method change** | we stopped trusting status 200 after N false positives | `METHODOLOGY.md` carries the rule; this carries the incident |
| **a review that changed the answer** | an adversarial review found the headline number was file-count-bound | the corrected number is in `docs/`; the correction is here |
| **an operator decision** | we are not paying for anything this quarter | not a research finding, but it constrains future work |

What does **not** belong: a diary of what the agent did. If the entry does not
change what a future reader would believe or do, it is not history, it is a log,
and logs live in `.tmp/`.

## The format of an entry

Six lines at the top, then prose.

```markdown
# <what happened, as a sentence>

- **When:** 2026-10-22T07:41:03Z
- **Status:** superseded | abandoned | corrected | decided | observed
- **Supersedes:** `docs/storage/free/zenodo.md` §Quota (or `-`)
- **Superseded by:** `docs/storage/free/zenodo.md` §Quota (or `-`, if still current)
- **Evidence:** the URL, the capture path in `sources/`, or the probe output
- **Confidence:** measured | documented | reported | inferred
```

Then, in order: **what we believed**, **what we found**, **how we found it**,
**what it cost us** (a wave? a wrong recommendation? a review round?), and
**what a future session should do differently**. The last section is the only
one that makes the file worth keeping; if there is nothing to say there, the
entry is a note, not a history entry.

## The withdrawn-claims table lives on the front page

`README.md` carries one table headed **Withdrawn claims**, and it is the short
curated list a reader meets before any recommendation. `history/` is the long
record; the front-page table is the five-or-so entries that would change a
reader's decision if they still believed them.

Columns, in this order: **the claim**, **what took it away** (one clause, with
the date), and **where the current correction lives** (a `docs/` path or a
history directory). A reader who checks the table and stops has avoided the
wrong sentences. A reader who wants the reasoning follows the third column.

⚠ **The table is not a copy of this directory.** An entry here that changes no
recommendation does not reach the front page, or the table grows until nobody
reads it.

## Rules

- **Never rewrite an entry.** A history entry that is edited to match a later
  understanding destroys the thing it exists for. Write a new entry that
  supersedes it and link both ways via the two header fields.
- **Never delete an entry**, including one that turned out to be wrong. An
  entry that was wrong is evidence about the method that produced it.
- **Link in both directions.** The header names the document it supersedes, and
  that document names this entry in its own history line. A one-way link is how
  a reader gets a claim with no provenance.
- **No AI attribution, no session narration.** The voice is a colleague
  explaining what changed the answer, not a transcript.
