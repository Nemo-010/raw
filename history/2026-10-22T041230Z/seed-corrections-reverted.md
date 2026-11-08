# Two seed corrections were reverted, and one of them put a closed service back on the table

- **When:** 2026-10-22T04:12:30Z
- **Status:** corrected
- **Supersedes:** `dossier/compute/ctrl-c-club.json` (`identity_cost`, `limits[]`, `notes`), `dossier/compute/tilde-zone.json` (`verdict`, `confidence`, `free_tier`), `docs/compute/free/anonymous-vms.md:27,29`, `docs/compute/free/always-on-free.md` section The pubnix layer
- **Superseded by:** the same files, plus `docs/compute/free/always-on-free.md` section The comparison, which now carries the tier taxonomy both corrections were made inside
- **Evidence:** `.tmp/seed/peli-cloud-talaria/data/always-on-free.json` `corrections_vs_launch_base` and `rows`; `.tmp/seed/peli-cloud-talaria/research/deep-reviews-anon-vms.md` R22 (2026-10-02); `tilde.zone/explore` (read 2026-10-22)
- **Confidence:** documented

## What we believed

That the destination carried both seeds' own corrections. Eleven of thirteen did,
some of them improved: Oracle's time-denominated quota, GitHub Codespaces' restored
120 hours, Hugging Face's PRO gate, Koyeb's published free Instance, Blinkenshell's
Supporter-only ports, Northflank's card requirement, Azure F1's real shape,
ModelScope's withdrawal and its `.cn` phone gate, and hashbang's 30-day sweep.

Two did not.

## What we found

**Ctrl-C.club's signups are closed and the destination had dropped the fact.** The
seed records it as a correction in its own right and carries the vendor's words:
"Signups are closed for now! Thank you for your interest in Ctrl-C.club! We're
pausing signups to work on some scaling issues. You can still submit a signup to get
on a waitlist." `grep -rli waitlist` over `docs/`, `dossier/` and `history/`
returned three storage files and nothing in compute. The row appeared in two
tables as a service a reader could sign up to.

That is the worst shape a stale fact takes here: not a wrong number, but a door a
reader walks into. The 5-year retention clock and the 1 GB soft limit were both
correct, so the row looked checked.

**tilde.zone was re-promoted, which is the regression the review contract names by
hand.** The seed demoted it in review R22 for a stated reason: a host answering SSH
is evidence of a host and not of a free shell. It set `class: changed`,
`cost_usd: unknown` and an empty quote, and it wrote down what would recover the
row: a first-party page that names an operator and a signup path.

The destination mapped the seed's `changed` class onto `qualifies-with-caveat` at
`confidence: measured`, resting the verdict on the SSH banner alone. Its own
`free_tier.stated` conceded "no quota, lifetime or login policy was published to
either pass" and its `limits_note` said "the terms are unread", which is a record
arguing against its own verdict on one screen.

## How we found it

The completeness review diffed both seeds' `corrections_applied` and
`corrections_vs_launch_base` lists against the destination record by record and read
`research/deep-reviews-anon-vms.md` for what the seeds' own reviewers cut and why.

For tilde.zone the review's finding was re-tested rather than taken. `tilde.zone/`
was fetched on 2026-10-22 and redirects to `/explore`, which serves a Mastodon
instance: a trending feed with post and hashtag links, 518 words of rendered text,
and no mention of a shell, a signup, a quota or an operator. R22's conclusion holds
eight weeks later.

## What changed

**ctrl-c.club** gained a `write-gated` limit quoting the waitlist sentence, the same
sentence in `identity_cost.detail`, the soft-limit wording in `notes`, and two
`evidence` entries from `signup.ctrl-c.club/`. The document row now reads "email,
and signups are closed: waitlist only", and the paragraph in
`always-on-free.md` carries the vendor's words.

**tilde.zone** is `confidence: unverified` with `verdict: qualifies-with-caveat`,
which is the honest pair: the reachability is measured and the offer is not
established. The record says in its own `notes` that recovering it needs what R22
asked for, and the document says the same.

⚠ **The verdict vocabulary has no `unverified` value**, so the record cannot say in
its verdict field what its confidence field says. `qualifies-with-caveat` is the
least wrong of the eight values because the machine does answer, and the confidence
rung is where the doubt is recorded. That is a schema limitation and not this
record's finding.

## What this cost, and what it would have cost

One row a reader could not sign up to, and one row whose verdict outranked its
evidence. The second is the more expensive of the two: it is the failure mode R22
was written to prevent, it was recorded as prevented, and a later pass re-made the
same mistake with the same evidence.

The general lesson is the one this repository keeps relearning. A correction that
lives in a seed's review file does not survive a rewrite unless the rewrite reads
the review file. Both of these were in `research/deep-reviews-anon-vms.md`, which is
the document a reviewer reads and a writer skips.
