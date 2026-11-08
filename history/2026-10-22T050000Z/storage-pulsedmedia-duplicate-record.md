# PulsedMedia's 16 TB box was recorded twice, and one of the two is now marked as the duplicate

- **When:** 2026-10-22T05:00:00Z
- **Status:** decided
- **Supersedes:** `dossier/storage/pulsedmedia-m10g-storage-box-16tb.json`, which stood as an independent record of an independent offer
- **Superseded by:** `dossier/storage/pulsedmedia-m10g-storage-box.json`, the canonical record, and the same file's `extras.duplicate_of`
- **Evidence:** `https://pulsedmedia.com/storage-boxes.php`, read 2026-10-22, HTTP 200, 7,273 bytes, four tier headings under one product name; capture at `.tmp/work/fx-storage-residual/pm-page.md`
- **Confidence:** documented

## What we believed

The topic held two records for a 16 TB PulsedMedia box: `pulsedmedia-m10g-storage-box.json` and
`pulsedmedia-m10g-storage-box-16tb.json`. Both carry EUR 26.99, 16 TB, RAID5, the same page URL and
the same egress string. The earlier pass described the second as a consolidation artefact in a
sentence under the provider, and left both records standing with their numbers intact. A reader who
grepped the directory found one offer twice, and had to read prose to learn that.

## What we found

The vendor page settles it. It publishes **one** product line with four tiers, titled
"M10G STORAGE BOX 4TB", "8TB", "16TB" and "32TB", at EUR 8.99, 14.99, 26.99 and 63.99, each on the
same 500 MB RAM and 10 Gbps platform with the same egress string. There is no second 16 TB SKU and
no 12 TB storage box: the 12 TB figure in the second record's `conflicts[]` belongs to the M10G
*seedbox* ladder, which is a different product on a different page.

So the two records are one product, and the previous pass's reading of *why* was also wrong in a way
worth recording. It said the ledger "assigned two seed spellings to two documents". In fact the two
records come from **different seed waves** — `A-P7-discount-channels.json` and
`A-P6-seedbox-storage-hosts.json` — and the earlier record carries a `merged_spellings` entry mixing
a storage box with a 12 TB seedbox, so the duplication began as a merge error, not as a routing one.

The canonical record also carried a defect of its own: `limits: []` with `binding: "none"`, while its
own `egress.terms` quotes "Unlimited@100Mbps (~30TB/Month / ~1TB/Day)". The port is the constraint
and this repository already has an entry naming it
([`pulsedmedia-port-is-the-cap.md`](../2026-10-22T030746Z/pulsedmedia-port-is-the-cap.md)). The
canonical record now carries the `per-ip-shaping` limit, `binding: per-ip-shaping`, and a link to
that entry. The gate requires a binding constraint on a `documented` record, so this was a live
omission rather than a tidy-up.

## How we found it

`sh scripts/broker/broker.sh read https://pulsedmedia.com/storage-boxes.php` on 2026-10-22 returned
200 with 7,273 bytes. The four headings were counted from that capture, and the price literals 8.99,
14.99, 26.99 and 63.99 appear once each. The earlier pass had read the same page and reached the
same product conclusion, but recorded it as prose under the section instead of in the record, which
left the directory contradicting the sentence.

## What it cost us

One duplicate in every count over `dossier/storage/`. The topic's record total is 1,708 and one of
those is this offer counted twice, so any per-record arithmetic that treats qualifying records as
distinct offers overstates 16 TB boxes by one. The `paid/storage-boxes.md` price-floor table and the
`paid/lifetime-and-deals.md` Black Friday section both cite the same product, which is defensible
once a reader knows they are one box.

## What a future session should do differently

**Resolve a duplicate in the record, not in the sentence under it.** The earlier pass wrote the
correct answer in the document and left the directory wrong, so the next script that counts records
still saw two offers. The repository already has the convention this needed — `extras.duplicate_of`,
used by `dossier/compute/gitpod.json` and `dossier/compute/kaggle.json` — and it was not reached for.

Both records are kept. The duplicate keeps its verdict, its rung, its evidence and its price, and
gains `extras.duplicate_of`, `extras.duplicate_note` and `extras.count_note`. Deleting it would
re-open a question that is now closed and would take the provenance of the seed's second wave with
it. A count that must exclude duplicates can now filter on the field instead of on a paragraph.
