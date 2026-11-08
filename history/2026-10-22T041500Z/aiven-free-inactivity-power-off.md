# Aiven's free plan was recorded as the one that never pauses, and it powers off on inactivity

- **When:** 2026-10-22T04:15:00Z
- **Status:** corrected
- **Supersedes:** `dossier/databases-kv/aiven-free.json` (`retention.stated`, `binding`), `docs/databases-kv/free/postgres-always-on.md` (title, comparison table, the "trade this class makes" section, the Aiven section and its verdict), `docs/databases-kv/README.md` (the class table row and the record table row)
- **Superseded by:** `dossier/databases-kv/aiven-free.json` as corrected, and `docs/databases-kv/free/postgres-always-on.md`
- **Evidence:** `aiven.io/free-postgresql-database`, `aiven.io/docs/products/postgresql/concepts/pg-free-tier`, `aiven.io/docs/platform/concepts/service-power-cycle` and `aiven.io/docs/platform/concepts/free-plan`, all read 2026-10-22
- **Confidence:** documented, from four first-party Aiven pages

## What we believed

Aiven's Free plan was the one free managed Postgres in this corpus that did not pause on
inactivity, and that was the property the class was formed to deliver. The topic's comparison table
read "Aiven | 1 GB per service | **never pauses** | email | qualifies-with-caveat", the class
section explained the trade as "a database that stays up at 1 GB, or one that sleeps at 20 GB", and
the verdict sentence read "The one free Postgres here that a weekly cron can rely on".

## What we found

Aiven's own pages say the opposite, in three places.

The free-PostgreSQL page, under the free-plan limits: "Service powers off after a period of
inactivity (you'll be notified by email and in-platform beforehand)", and in prose: "It's free
indefinitely with no time limit, but the service is automatically powered off after a period of
inactivity".

The free-tier documentation gives the two triggers: "Power off free services with no initial usage
within the first few hours after the service is running", and "Power off free services with no
continuative activity on the service".

The power-cycle documentation gives the consequence: "Services powered off for more than 180 days
are automatically deleted." The 180-day grace does not apply to a service whose major version has
reached end of life, which is deleted within 7 days of the power-off.

The paid step is what removes the clock, and the free-plan page says so: "Developer tier services
are not automatically powered off when inactive", at USD 5 a month for 8 GB.

## How we found it

A reviewer following the record's own citations. The record was not blind to it: `retention.stated`
read "the Free plan does not pause on inactivity; data retention is limited only by storage, with
the Free plan excepted". The clause after the semicolon is the vendor's carve-out, quoted from the
pricing page, and it was read as boilerplate rather than as the finding. One field contradicted
itself in one sentence and the contradiction survived because both halves looked like vendor noise.

## What it cost us

The class premise. A free tier that does not pause costs the provider money every hour and is
therefore small; a tier that pauses can be large. Aiven is small **and** it pauses, so size and
pause were never the trade, and the document's explanation of why the class looks the way it does
was reasoning from a premise its own subject falsified.

The reader cost is larger. A reader who picked Aiven for durability picked it for the one property
it does not have, and a weekly job on an Aiven free service is exactly the workload that lets the
service power off between runs.

## What a future session should do differently

**Read the carve-out.** "Data retention is only limited by storage, with the exception of Free
plan" is one sentence that states a clock for the plan under discussion. An exception clause is a
finding about the excepted case, and the excepted case was the whole subject of the section.

The class is now stated as three clocks rather than one property: CockroachDB deletes on a 30-day
clock after its trial, Aiven powers off on inactivity and deletes at 180 days, and TiDB publishes
no clock at all. The 1 GB storage figure and the 1 GB RAM figure were correct throughout and are
unchanged.
