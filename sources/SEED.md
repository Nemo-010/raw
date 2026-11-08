# sources/SEED.md — what this repository inherited

The corpus did not begin here. It began as four external research passes, run by
others, under licences that permit reuse, plus one platform's own public
documentation. This file records exactly what was taken, from where, and what
that means for how much a reader should trust it.

**Every claim inherited from these sources starts at the `reported` rung of the
evidence ladder**, no matter how confidently the source stated it. A claim is
promoted to `documented` only when a page in `sources/` was re-read here, and to
`measured` only when this repository ran the probe. That rule is the whole reason
this file exists: an inherited number that looks authoritative is the most
dangerous thing in a corpus like this one.

---

## 1. `storage-research` — the storage corpus

| | |
|---|---|
| **What** | Ten research waves over free and near-free bulk storage: 91 dossiers, 1,101 distinct providers, 935 rejected providers with reasons, 12 verification files, 189 captured raw pages |
| **Origin** | An earlier research pass, completed 2026-10-22 |
| **Licence** | The operator's own work; no third-party licence attaches |
| **What was taken** | `FINAL-REPORT.md`, `DEAD-ENDS.md`, `table.md`, `TOP-FINDINGS.md`, `ROUND2-FINDINGS.md`, `CHEAP-PAID-FINDINGS.md`, `ECONOMICS-AND-STACKING.md`, `ALIST-FINDINGS.md`, `BASELINE.md`, `PROVIDER-RESEARCH.md`, all 91 `dossiers/*.json`, all 12 `verify/*.json`, and the `raw/` captures where a document cites them |
| **What was not taken** | the three downstream agent briefs (superseded by `METHODOLOGY.md`), `archive/` drafts, the python scripts (rewritten in `scripts/`), the `.tmp/` and `tmp/` scratch |
| **Trust note** | The corpus is internally reviewed — three independent reviewers produced Appendices R1–R3 of the final report — but its numbers were measured in a different session on a different day. Re-measurement is required before any number is promoted to `measured` here |

---

## 2. `peli-cloud` (two independent passes) — the compute corpus

Two different researchers catalogued cloud sandbox, VM, dev-environment and
agent-runtime providers with the same name and different results. Both are kept,
because the disagreement is the finding.

### 2a. `talaria0101/peli-cloud`

| | |
|---|---|
| **What** | A cheapest-first catalogue over a 366-provider corpus, priced at three usage shapes and four duty cycles, with a cross-check driver and per-provider JSON |
| **Origin** | `https://github.com/talaria0101/peli-cloud`, snapshot dated 2026-10-02, repository last pushed 2026-10-07 |
| **Licence** | 0BSD |
| **What was taken** | `README.md`, `data/*.json` (per-provider records, the billing-posture model, the exclusion ledger, the crosscheck summary), and the method described in its `NOTICE` |
| **Trust note** | A price snapshot, explicitly not a live feed. Its own README says so |

### 2b. `Nemo-010/peli-cloud`

| | |
|---|---|
| **What** | A second catalogue, with material the first does not carry: anonymous/no-account VMs, SSH relay and relay-forward egress, and a provenance file |
| **Origin** | `https://github.com/Nemo-010/peli-cloud`, snapshot dated 2026-10-02, repository last pushed 2026-10-02 |
| **Licence** | 0BSD |
| **What was taken** | `README.md`, `data/*.json`, `docs/ANONYMOUS-VMS.md`, `docs/RELAY-FORWARD.md`, `docs/SSH-RELAY.md`, `research/*`, `sources/2026-10-02/MANIFEST.tsv` |
| **Trust note** | Its `research/deep-reviews*.md` removed rows from its own catalogue, which is evidence of method. Its verification files are dated and should be re-run rather than trusted |

---

## 3. `talaria0101/coding-subs` — the subscription corpus

| | |
|---|---|
| **What** | Market research on cheapest frontier coding-agent subscriptions: a model database, a provider database, an Artificial Analysis snapshot, and 100+ captured vendor pages |
| **Origin** | `https://github.com/talaria0101/coding-subs`, snapshot dated 2026-09-13, repository last pushed 2026-10-07 |
| **Licence** | 0BSD |
| **What was taken** | `2026-09-13/README.md`, `data/*.csv`, `data/aa-snapshot-*.json`, `references/references.md`, and the vendor captures in `sources/` |
| **What was not taken** | its CI workflow, which pins a Node version and runs a check specific to that repository |
| **Trust note** | **This is the stalest seed in the corpus.** Five weeks is several pricing cycles in this market. Treat every price as a hypothesis until re-measured, and expect a material fraction of the catalogue to have moved |

---

## 4. `web.pkgforge.dev` — the tool contract

| | |
|---|---|
| **What** | A public, free, keyless web-access platform: search, read (page → Markdown), fetch (transparent HTTP proxy), crawl (job-based), research (scholarly broker), archive (capture and replay), plus GitHub and Hugging Face proxies and a status endpoint |
| **Origin** | `https://web.pkgforge.dev/llms.txt` and `/llms-full.txt`, captured 2026-10-22; the implementation is the operator's own project |
| **Licence** | The operator's own work |
| **What was taken** | The published contract, into `docs/crawler-scraper/free/broker.md` and into the `scripts/broker/` wrappers. Also its 39 measured platform traps, triaged into the documents that own them |
| **Trust note** | The contract is generated from the deployed code, so it does not drift from the services. It does drift from *observed* behaviour when a provider is degraded; `docs/` records observed behaviour separately |

---

## 5. `TEMPLATE` — the methodology

| | |
|---|---|
| **What** | The operator's standing methodology, conventions and session protocol for agent-worked repositories |
| **Origin** | `https://github.com/Azathothas/TEMPLATE`, `docs/methodology/` and `docs/conventions/` |
| **Licence** | The operator's own work |
| **What was taken** | Structure and register for `METHODOLOGY.md` and `docs/conventions/`. Not copied wholesale: a research repository has no build, no deploy and no test suite, so the parts about those do not apply |
| **Trust note** | Where this repository's methodology diverges from the template, the divergence is stated with its reason. A silent divergence would make the two documents disagree |

---

## 6. `podbox` — the history convention

| | |
|---|---|
| **What** | A reference example of how the operator records superseded work |
| **Origin** | `https://github.com/Azathothas/podbox`, `docs/history/` |
| **Licence** | The operator's own work |
| **What was taken** | The *idea* — dated entries, one event per file, no deletion — and an improvement on it: directories are named for the moment in UTC with a `Z` suffix, and an `INDEX.md` is generated, so entries are findable rather than scattered |
| **Trust note** | Its own history directory mixes conventions (some dated, some `-before-<date>` snapshots). This repository does not |

---

## The rule that follows from all of this

A promoted claim carries the rung it earned **here**, not the rung its source
claimed. When a document in `docs/` cites a number inherited from any of the six
sources above and nobody has re-measured it, the document says `reported` and
links to the source. When the re-measurement happens, the rung changes and
`sources/MANIFEST.tsv` gains a capture. That is the only path by which a number
becomes trustworthy in this repository, and it is deliberately the slow one.
