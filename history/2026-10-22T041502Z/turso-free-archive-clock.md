# Turso's free plan was recorded as having no idle clock, and it archives an inactive database after 10 days

- **When:** 2026-10-22T04:15:02Z
- **Status:** corrected
- **Supersedes:** `dossier/databases-kv/turso.json` (`retention`, `limits`, `binding`, `chaining`), `docs/databases-kv/free/edge-kv-and-sqlite.md` (comparison table, Turso section, What did not work, Chaining)
- **Superseded by:** `dossier/databases-kv/turso.json` as corrected, and `docs/databases-kv/free/edge-kv-and-sqlite.md`
- **Evidence:** `docs.turso.tech/cli/group/unarchive`, `docs.turso.tech/api-reference/groups/unarchive` and `turso.tech/pricing`, all read 2026-10-22
- **Confidence:** documented

## What we believed

`retention.stated` read "databases persist while the plan is active", and the comparison table had a
write-budget column and no idle-clock column at all. The verdict was `qualifies`.

## What we found

Turso's CLI reference states: "Databases get archived after 10 days of inactivity for users on a
free plan." The API reference exposes a `groups/unarchive` endpoint, so the archive state is
reachable programmatically. Turso's own announcement of its paid Hobby plan sells "your databases
never archived or scale to zero" as the upgrade, which is the vendor saying the free plan does
archive.

The archive is not a deletion: the bytes survive and an unarchive restores service. It is still the
binding constraint, because it is what a job that runs less often than every ten days meets first.

## How we found it

An adversarial review found the sentence on a page the record already cited for another number. The
pricing page does not carry the clock, which is why the record did not either.

## What it cost us

The table's shape. `edge-kv-and-sqlite.md` compared D1, Turso and KV on write budget and read
budget, and the two counters reset while the retention clock does not, so the two were not
comparable on the axis the table used. The table now has an idle and deletion clock column, and
Turso is the only row in it with a clock.

## What a future session should do differently

**A pricing page is not the retention page.** Every other database document in this topic has an
idle clock, and this one did not, which was visible from the table's own columns. When one document
in a class lacks the column the rest have, that is the signal to go looking for the field rather
than to conclude the provider lacks the clock.
