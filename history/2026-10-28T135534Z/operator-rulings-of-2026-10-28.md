# The operator decided seven open questions: three rules bind, three units and two topics are added, and the vocabulary may grow

- **When:** 2026-10-28T13:55:34Z
- **Status:** decided
- **Supersedes:** the warn severity of rules C01, C03 and C18 in `scripts/research/checks.py`; the `free_tier.unit` and `topic` enums in `scripts/dossier/schema.json` as they were before 2026-10-28; the policy paragraph of `docs/research-protocol.md` section 8
- **Superseded by:** `scripts/research/checks.py` (`RULES`), `scripts/research/baseline.tsv`, `scripts/dossier/schema.json`, `scripts/dossier/staleness.policy.json`, `docs/dev-services/README.md`, `docs/data-apis/README.md`, `AGENTS.md` section 2 rule 12, `docs/conventions/README.md` sections 2.2 and 6.3
- **Evidence:** the operator's ruling comments of 2026-10-28 on issues #10, #11, #12, #13, #20, #31 and #43 of `Azathothas/f-research`
- **Confidence:** documented

## What we believed

Three contradiction rules were warnings because whether they bind is a methodology decision, not a fact:
C01 (a qualifying verdict while the record's own free tier says there is none, 184 records), C03 (verdict
`qualifies` with no probe, 167 records) and C18 (a qualifying verdict behind an institution, a national ID or a
country phone, 114 records). `rq policy` filed one issue for each. The schema had no unit for compute time, so a
lane recorded 1,600 core-hours as `hours` and a check-in allowance of server time as `GiB`. Two classes of free
service, developer services and data APIs, had no topic, and research issues for them named a neighbour topic
as a stopgap.

## What we found

The operator ruled on each issue on 2026-10-28:

| issue | ruling | what changed |
| --- | --- | --- |
| #10 | C01 binds: a qualifying verdict needs a free tier or a recurring credit | C01 is an error; 184 records are in the baseline |
| #11 | C03 binds only in `storage` and `netdisk-pan`, where the read path is the claim | C03 is an error in those two topics (58 records in the baseline) and a warning in every other topic |
| #12 | C18 binds for a plain `qualifies`: a gated identity is `qualifies-with-caveat` at best | C18 is an error for `qualifies` (16 records in the baseline) and no longer fires on `qualifies-with-caveat` |
| #13 | add `core-hours`, `gpu-hours` and `credits` to `free_tier.unit`; an agent may extend a vocabulary or a category in a pull request that names the records that need it | the schema enum, a vocabulary note in the conventions, and the standing rule as `AGENTS.md` section 2 rule 12 |
| #20 | fix process and personal wording both ways: projection rules, and the named records at the source | new clause and leak rules in `scripts/fshy/rules/projection.json`; `fr amend` on the named records |
| #31 | create the topic `dev-services` | schema enum, README, a row in `docs/README.md`, a 45-day staleness window |
| #43 | create the topic `data-apis` | schema enum, README, a row in `docs/README.md`, a 60-day staleness window |

The baseline rows were written with `scripts/rq check --write-baseline`, never by hand. Verify runs fix the
records and `scripts/rq check --prune` removes their rows (issues #25 and #26 plan those runs).

## How we found it

The counts are from `scripts/rq check` on 2026-10-28 over 4,191 records. The C18 count falls from 114 to 16
because the ruling makes `qualifies-with-caveat` behind a gated identity the correct verdict, not a violation.

## What it cost us

The queued re-run of `compute/tencent-cnb`, `compute/baidu-ai-studio` and `compute/simpfun` failed its audit
twice; two of the four unsupported claims of the second attempt were the missing unit, not a misread. The
`staleness` check on `main` stays red on two of those records until the re-run lands.

## What a future session should do differently

A value that fits no term is a reason to extend the vocabulary, not to pick the nearest wrong term. Open the
pull request that adds the term, name the records that need it, and use `mixed` with the true unit in `stated`
until it merges. A warn rule that waits for a decision should name the issue that holds the question, so the
decision is one comment away.
