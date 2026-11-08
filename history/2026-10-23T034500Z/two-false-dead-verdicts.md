# Two storage verdicts were false negatives

- **When:** 2026-10-23T03:45:00Z
- **Status:** corrected
- **Supersedes:** `dossier/storage/dediseedbox.json`, which carried `verdict: dead` because two pricing paths returned 404; and `dossier/storage/catbox-moe.json`, which carried `verdict: fails-quota` because the origin returned HTTP 521 on one day
- **Superseded by:** both records re-read on 2026-10-23. dediseedbox is `paid-only` and sells seedbox hosting with "10Gbps Unlimited traffic"; catbox.moe is `qualifies-with-caveat`, answered 200, and served a 6,585,929-byte object twice with a matching digest
- **Evidence:** `https://www.dediseedbox.com/` read 2026-10-23 (HTTP 200, "50+ apps One-click install", "NL hosted Netherlands datacenter"); `https://catbox.moe/` read 2026-10-23 (HTTP 200, Cloudflare headers) and a 6,585,929-byte read-back at 0.315 MiB/s recorded by the debrid measurement lane
- **Confidence:** documented

A failed price read is not a dead service, and a single-day 521 is not a quota
failure. Both records now say which fields were re-read and which were not: the
price, the per-object cap and the retention of each remain unread, and the records
state that rather than repeating an older number.
