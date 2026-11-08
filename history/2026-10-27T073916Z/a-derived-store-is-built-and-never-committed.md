# A derived store of the dossier is now built on every change, and it is never committed

- **When:** 2026-10-27T07:39:16Z
- **Status:** decided
- **Supersedes:** `dossier/README.md` §Layout ("There is no generated index") and the `dossier/index.py` row of `scripts/README.md`
- **Superseded by:** `scripts/fshy/README.md`, `scripts/fshy/build.py`, and the `projection` check in `scripts/gate.sh`
- **Evidence:** `python scripts/fshy/build.py` builds the store from 4,136 records in about 17 s; five recon reports and two independent designs, all measured against commit `872967a`
- **Confidence:** measured

## What we believed

That a generated index of the dossier would fork from the records, so none should exist. Every count a reader
needed was emitted by `scripts/report/render.py` into the document that needed it.

## What we found

The rule protected the records from a second committed copy, and it held. It did not protect the reader. With
4,136 records and 51,238 lines of documents, a cross-topic question cost an agent 3 to 6 tool calls and 40 to 90 KB
of reading and still came back 40 to 65% complete. 1,125 records were named in no document, 11.8% of record text
reappeared in any document, and 139 hand-written table rows carried a verdict different from their record. No
document can be a complete view of that many records; a query can.

The new rule keeps the old one's intent. The JSON in `dossier/` stays the only truth and the only thing a reviewer
reads in a diff. `scripts/fshy/build.py` derives a SQLite store from it into `.tmp/fshy/` (never committed), and the
public wiki, API and MCP at `fshy.ajam.dev` are a projection of that store, rebuilt from the records on every push.
Nothing is written back into `dossier/` by the build. Freshness is computed from `scripts/dossier/staleness.py`, not
stored.

## How we found it

Five measuring passes (data model, documents and pipeline, query cost, store options, deployment) and two design
passes that could not see each other. Both designs arrived independently at the same shape: JSON stays the truth,
the store is derived and disposable, every source value gets exactly one logged disposition, and the public
projection strips process narrative, personal details and terms text.

## What a future session should do differently

Query before reading. `python scripts/fshy/fr.py help` prints the schema and the vocabularies; `fr search`,
`fr filter` and `fr need` answer most questions in one call; `fr amend` changes a record and writes the old value to
`history/ledger.jsonl`. A count typed into a document is a defect waiting to happen; cite the query instead.
