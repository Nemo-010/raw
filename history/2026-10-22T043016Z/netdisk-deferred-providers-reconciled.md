# The 70 deferred netdisk-pan providers are reconciled: 70 records, 4 new documents, 15 graveyard rows

- **When:** 2026-10-22T04:30:16Z
- **Status:** reconciled
- **Supersedes:** the `netdisk_pan_deferred` deferral in `dossier/storage/_dead-ends-index.generated.json`, and the completeness review's count of 68 unwritten records
- **Superseded by:** `dossier/netdisk-pan/`, which now carries the 70 records, and `docs/netdisk-pan/`
- **Evidence:** `dossier/storage/_dead-ends-index.generated.json` for the 70 reserved names; `.tmp/work/recon-storage/gen/ledger-qualifying.md` and `ledger-rejected.md` for the 70 reserved slugs; the seed dossiers under `.tmp/seed/storage-research/dossiers/` for the facts; `.tmp/work/recon-netdisk/sweep_final.tsv` for the measured instances; five vendor pricing tables read live on 2026-10-22
- **Confidence:** mixed by record, as each record states

## What was deferred

The `storage` pass cut `netdisk-pan` out as a peer topic and deferred 70 providers to it rather than writing them. The deferral was deliberate and visible: `_dead-ends-index.generated.json` carries a `netdisk_pan_deferred` block naming all 70 and stating the reason, and `extras.counts.netdisk_pan_names` carries the same list.

The plan behind it assigned those 70 names to four documents — `write/registerable-pans.md` (30), `read/public-instances.md` (16), `read/direct-link-extraction.md` (15), `read/bridge-hosts.md` (9) — and reserved a slug for each in `.tmp/work/recon-storage/gen/ledger-*.md`.

## What was found missing

A completeness audit found 68 of the 70 had no record anywhere. Two did, under `dossier/storage/`: Amazon Photos and Baidu Pan.

`dossier/netdisk-pan/` then held 52 records, and those 52 were largely the *public instances* the netdisk writer had probed itself. It had not picked up the deferred set, so the providers the storage pass named — the five purchasable managed Nextcloud hosts, `123pan`, `ploud`, `1yunpan`, `pan.moe`, `quark`, the twelve consumer drives with the largest installed bases — were still unwritten.

Six were `qualifies`, and they were the only group in the whole seed that could be **bought** without an identity problem: paid managed Nextcloud with WebDAV at EUR prices. The corpus could not answer a purchase question it existed to answer.

## What was restored

**103 records in the topic, up from 52.** Of the 70 deferred names:

- **56 have a new record of their own** under `dossier/netdisk-pan/`, at the reserved slug where the ledger's slug was a usable name.
- **14 are aliases on a record the netdisk writer had already made for the same host**, with the deferred name added to `extras.aliases` and the seed facts parked in `extras.seed_facts`. Writing a second file for the same public instance would have been the duplicate this repository's `dossier/README.md` exists to prevent.

That arithmetic is 56 + 14 = 70. The topic's record count moved by 51 rather than 56 because 13 of this pass's own first drafts for the public instances duplicated records the netdisk writer had made, and those 13 extra files were folded into the existing records and deleted rather than shipped twice.
- **All 70 are discharged**, and `.tmp/work/fx-netdisk-deferral/verify_deferral.py` proves it by reading the index, resolving each name, and refusing the run when a claimed path is missing or a claimed alias is not carried.

**Four documents written**, mapped from the plan's four filenames to the tree's existing lanes, because this topic split by access mode and has no `read/` or `write/` directory:

| the plan's name | where it landed | names |
| --- | --- | --- |
| `read/bridge-hosts.md` | `docs/netdisk-pan/paid/managed-nextcloud.md` | 9 |
| `write/registerable-pans.md` | `docs/netdisk-pan/pans/registerable.md` | 30 |
| `read/public-instances.md` | `docs/netdisk-pan/public-instances/instances.md` | 16 |
| `read/direct-link-extraction.md` | `docs/netdisk-pan/pans/reverse-engineered-clients.md` | 15 |

Each document carries a "Where the deferred names landed" table, so the mapping survives without this entry.

**Fifteen graveyard rows added** to `docs/storage/dead-ends.md`, in the class section each record's failure names, and the page's arithmetic updated from 445/898/1343 to 460/898/1358. The page claimed to be exhaustive and 15 records with an evidence trail had no row.

## The four reserved slugs that could not be used, and one that was

The ledger's reserved slug is a contract, and 60 of the 70 were usable names. Ten were placeholders, and three of those collided with a different provider already recorded under `dossier/storage/`:

| reserved slug | what already held it | what this pass used |
| --- | --- | --- |
| `provider` | 七嗖云盘 / 长青云盘 (7so.top) | `yike-album` |
| `provider-2` | 爱发电 (afdian) | `seven-so-cloud` |
| `provider-3` | 货摊网 (huotan) | `cstcloud-data-capsule` |
| `provider-8` | nothing | `china-unicom-wopan` |
| `samsung-cloud` | Samsung SDS Cloud Platform, in `dossier/compute/` | `samsung-cloud-storage` |
| `telnyx-cloud-storage` | the storage record of the same name | `telnyx-cloud-storage-egress-view` |
| `ai` | nothing, but it matches any document mentioning AI | `doubao-drive` |
| `uc` | nothing, but it is two letters | `uc-drive` |

The ledger's value is preserved in `extras.reserved_slug` on each of those records, so a future session searching for the reserved name still finds the record. **The contract is honoured in the sense that matters — the name resolves — and the placeholder itself is not used as a join key.**

## Three facts changed against the seed

1. **Hetzner Storage Share has 3, 7 and 10 users per instance**, not unlimited. The seed's C-C7 record said unlimited users; the live pricing block gives the counts per tier. This matters because a plan that divides a 10 TB unit across more than ten credentials needs a different provider.
2. **nextfiles.one prices Seafile Pro at EUR 9.90 for 500 GB**, not the seed's 1 TB. The live Seafile page prices Business S by user count and Business L per user. The record carries the live page and names the disagreement.
3. **Serverdiscounter has a 25 TB tier at EUR 59.95 including VAT**, which the seed did not record and which is the only single order in the survey that holds a whole 20 TiB archive. At EUR 2.40/TB/month it is also the cheapest per terabyte found.

## What is still open

- **The `links` check is red on 35 records outside this pass's write scope** — 20 in `storage`, 7 in `crawler-scraper`, 7 in `egress`, and one that this pass fixed. `scripts/gate.sh` was tightened by another session at 04:17Z to require a slug citation for every `measured` or `documented` record, which found pre-existing orphans across seven topics. Fixing them needs write access to those topics.
- **The `staleness` check is red on 342 records**, of which this pass's are dated honestly from the seed pass and not re-dated.
- **The `render` check is red on one row**, `coding-subs` in `BRIEF.md`, which is another session's topic. The `netdisk-pan` row agrees.
- **The GoPro upload experiment is unrun.** One account and one large non-GoPro upload would decide between unlimited storage at USD 59.99/yr and 100 GB. It is the highest-value unrun test this pass found.
- **DanubeData's traffic terms and S3 credentials are unverified**, and they are the two things that would move it ahead of Serverdiscounter on price.
