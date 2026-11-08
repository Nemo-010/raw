# Three hundred and fifty compute records claimed to have been checked after their evidence was

- **When:** 2026-10-22T04:26:26Z
- **Status:** corrected
- **Supersedes:** the `verified_at` and `confidence_note` values written by
  `.tmp/work/w-compute/gen-records.py` and `.tmp/work/w-compute/gen-census.py`
  into 350 `dossier/compute/*.json` records
- **Superseded by:** those records as they now read, each with a `verified_at`
  its own evidence supports
- **Evidence:** `scripts/dossier/staleness.py` before and after; the two generator
  scripts at the lines named below; 17 vendor pages re-read on 2026-10-22 with the
  quote that proves each claim recorded in `.tmp/work/fx-data/proof.json`
- **Confidence:** measured for the generator behaviour and the 17 re-reads,
  documented for the records that remain at the seed date

## What we believed

That 350 `compute` records had been verified on 2026-10-22. Every one carried
`"verified_at": "2026-10-22T00:00:00.000Z"`, which is a claim that somebody
confirmed the record against the live service that day. The staleness gate read
that field as the record's freshness and passed them.

## What we found

Two generator scripts wrote the constant. `gen-records.py:15` defines
`PROBE_AT = "2026-10-22T02:16:12.000Z"` and stamps it on every record at
`gen-records.py:166`; `gen-census.py:14` defines `AT = "2026-10-22T02:35:00.000Z"`
and does the same. Neither script read a page. Their evidence rows carry the seed
dates `2026-10-02` and `2026-10-06` and say so in their own words: "listed in the
peli-cloud corpus card at commit f6a71ab0; the card is the source, not the vendor
page".

So the record said *checked today* while its only source said *read eighteen days
ago, second-hand*. That is the bulk touch `METHODOLOGY.md` section 10.1 forbids by
name, and section 10.3 names the two clocks it defeats. The dates had also been
flattened to midnight, which shows the value never came from a real probe
timestamp.

The gate could not see it until the evidence clock existed. The entry at
`history/2026-10-22T033211Z/methodology-coherence-fixes.md` added that clock and
recorded the count; this entry fixes the data the clock exposed.

The three non-compute records in the same report are a different defect and are
**not** corrected here. `storage/aws-codeartifact`, `storage/blomp` and
`storage/stoat-revolt-self-hosted-instance` fail on `evidence-past-topic`: an
oldest evidence row of 942, 272 and 752 days against a 180-day budget. Their dates
are honest — a genuinely old source is being cited, and the gate is right to say
it has expired. Dropping the row would hide the expiry, so they are left failing
and reported as open findings.

## How we found it, and which of the four resolutions each record got

A classifier read every record and its evidence, then bucketed it. No single rule
was applied to all 350: the buckets exist because the records differ.

| bucket | what it means | records |
|---|---|---|
| 1 re-verified | the cited page was fetched today and its own text carries the record's claim | 15, plus 2 already carrying a today evidence row |
| 2 stale date | nothing proves a re-check; `verified_at` returned to the newest evidence | 6 |
| 3 unknown | no dated evidence at all, so no honest date exists | 0 |
| 4 seed conversion | a mechanical conversion of the corpus card, with no page read | 327 |

Bucket 3 was empty on the live corpus: every failing record had at least one dated
evidence row, so the undated sentinel was never needed.

Buckets 2 and 4 land on the same date, because the newest evidence date is the
honest value in both cases. They are counted apart because the reason differs, and
bucket 4 also records the conversion in `confidence_note` so the next reader knows
the date is the seed pass rather than a check.

For bucket 1 the test was a verbatim quote, not a token match. An early pass
promoted records whose page merely contained `4 GiB`, which is on every pricing
page in the class and proves nothing; those were rejected. Each of the 17 has the
sentence that decides its claim recorded in `.tmp/work/fx-data/proof.json`, and a
fresh dated `evidence[]` row now carries what the page established. Confidence was
**not** raised: the free-tier and limit figures are now read, but the record's
weakest field still rests on the card, and the ladder takes the weakest.

## What it cost

The whole `compute` topic read as fresh for a day while 327 of its records had
never been opened. A reader asking for the cheapest sandbox would have been given
numbers from a third-party catalogue with a 2026-10-02 date and a 2026-10-22
stamp, and nothing in the record distinguished it from a record this repository
had measured.

The repair cost the corpus its green staleness check for the `compute` topic: 323
records are now correctly `stale` and may not appear in a recommendation until
somebody reads their page. That is the honest state, and it is worse-looking than
the lie it replaced. It is also the only state in which the count means anything.

## What a future session should do differently

1. **A generator must not own `verified_at`.** A migration script can date a
   record it converted, but the date must come from the record's own evidence, not
   from the clock at build time. `gen-records.py` had the seed dates in hand on
   the same line and used the wall clock instead.
2. **When a build stamps a constant, the gate should fail, not pass.** The check
   that caught this compares `verified_at` against the newest evidence and is the
   right one. The lesson is that a new gate needs one run against the corpus it is
   added to, before the corpus is trusted; the defect had been present since the
   records were generated.
3. **Freshness is worth re-checking rather than assuming.** Re-reading 17 of 350
   pages took under four minutes and converted more than a third of the `documented`
   rows from a stamp to a fact. The remaining 327 are cheap to fix the same way,
   one page each, and the `stale` flag now rations that work in the order it
   matters.
