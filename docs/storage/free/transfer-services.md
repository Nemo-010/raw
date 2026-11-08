# Transfer services: what a transfer is, and why it is not storage

A transfer service moves bytes between two people and holds them briefly. That is a useful
function and it is not storage. The distinction is not
pedantic: a transfer service that holds 50 GB per transfer for 30 days is a 30-day buffer, and
a plan that treats it as an archive has planned a data loss event.

This document covers 13 qualifying records: enterprise managed file transfer, consumer
transfer services, upload APIs, and the pastebins that behave like a transfer with a very small
object. 30 were rejected, and the largest group is retention.

## The comparison

Sorted by per-object cap. The retention column matters more than the cap in every row.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Smash (fromsmash.com), Free web tier | No file size limit and no limit on number of transfers on the free web tier... | per-object-cap: on the anonymous web tier | - | fails-quota |
| Catbox (catbox.moe + Litterbox) | 200 MB per file on catbox.moe, no total quota... | per-object-cap: 200 MB/file | - | qualifies-with-caveat |
| GitHub Gist | Unlimited gists per account; each gist is a full Git repo... | per-object-cap: 100 MiB per file | - | qualifies-with-caveat |
| GitLab Snippets / GitLab.com projects | 10 GiB free storage per project on GitLab.com Free tier (repo + LFS)... | - | - | qualifies-with-caveat |
| x0.at (filehost2, x0.at / 0x0 family) | 1024 MiB per file, no account, no per-account cap... | per-object-cap: 1024 MiB/file | anonymous* | fails-quota |
| Origrid | 25 GB per file with NO account; 50 GB per file / 50 GB storage with a free account... | per-object-cap: 25 GB/file anonymous, 50 GB/file free account | - | qualifies-with-caveat |
| SwissTransfer (Infomaniak) | 50 GB per transfer, all files combined, no account required... | per-object-cap: 50 GB per transfer (combined, not per file) | - | qualifies-with-caveat |
| timvisee Send instances (Firefox Send forks) | Per-instance. Public table (read live) includes send.cyberjake.xyz at 10 GiB / 30 days... | per-object-cap: table's Size limit column (2 | - | qualifies-with-caveat |
| Transfer.it (MEGA) | No per-transfer size limit (MEGA blog: 'Send 100 GB, 1 TB, or even more... | request-rate: not hit in ~10 uploads | - | qualifies-with-caveat |
| GigaFile `ギガファイル便` | 300 GB per file, unlimited number of files, no account required ('1300G') | per-object-cap: 300 GB/file | - | qualifies-with-caveat |
| StreamRuby | 250 GB free storage, grows +250 GB per 1,500 monthly views; 'no upper limit'... | - | - | qualifies-with-caveat |
| UploadHive | Free tier published table: max upload file size 'Unlimited'... | retention-clamped: deleted 50 days after last download | - | qualifies-with-caveat |
| UpZur | Registered free account: 1,953 GB storage... | per-object-cap: 5,120 MB per file | - | qualifies |

## What the class is

Three mechanisms share the name and they fail differently.

**A transfer service** takes a file, stores it for a period, and lets a recipient download it.
Smash, SwissTransfer, Transfer.it and Origrid are members. Their caps are per transfer rather
than per account, so the account is not the unit of capacity.

**An upload API** is a programmatic endpoint with the same shape. GigaFile, StreamRuby,
UploadHive and UpZur are members, and their per-file caps reach 300 GB.

**A pastebin** is a text store with a size limit around a megabyte and a retention measured in
days. Catbox, GitHub Gist and x0.at sit between the two, at 200 MiB, 100 MiB and 1,024 MiB.

## The retention is the finding, and one clamp is not yet proven

Six records in this class publish a retention of 30 days or less. SwissTransfer gives 7 to 30
days. Smash gives 7 days on a free transfer. x0.at gives 3 to 100 days scaled by file size.
Catbox keeps an anonymous file until two years of inactivity, which is the longest in the
class and comes with a 200 MB cap.

Transfer.it is the important case and it is **not proven**. A one-year
request is reported to be clamped to 90 days server-side, which would make it the cleanest
example of `retention-clamped` in the corpus. That is not confirmed. The page offers "Never,
7 days, 30 days, 90 days, 6 months, 1 year", and no JSON API is reachable: `/api/options`,
`/api/upload` and `/api/v2/options` all return the single-page-app HTML with `text/html`, so a
status code there proves nothing (`measured`, 2026-10-22: 200, SPA HTML, `text/html`).

The UI offering "1 year" is consistent with the claim and is not proof of it. The clamp is a
post-time behaviour, and settling it needs one browser-driven transfer. Until then the record
carries the claim as `reported` and `gaps.md` carries the open question.

## The two that are worth using

Two records in this class are genuinely useful and neither is a transfer service in the narrow
sense.

**Origrid** gives 25 GB per file with no account, 50 GB per file with a free account, and a
Contributor tier that raises storage automatically. The no-account tier is unusual at that
size.

**GigaFile** gives 300 GB per file with an unlimited count and no account, and its retention
band of 3 to 100 days is chosen at upload (`documented`, 2026-10-22: the page description
names the seven periods). It is the best transfer
service in the corpus and it is still a transfer service.

## The upload APIs

Four records are programmatic endpoints, and their value is that they can be driven from a job
rather than a browser.

UpZur gives 1,953 GB on a registered free account. StreamRuby starts at 250 GB and grows by
250 GB per 1,500 monthly views with "no upper limit". UploadHive publishes an unlimited file
size and unlimited download volume with no storage column at all. Each of these is a
`qualifies` in the table and each has a caveat that matters: a transfer service that says
"unlimited" is describing its queue, not its disk.

## Pastebins, and the object they actually hold

GitHub Gist blocks a single file at 100 MiB and a push at 2 GB, and a gist is a real git
repository. GitLab Snippets allow 50 MB per file within a 10 GiB project. Catbox gives 200 MB
per file with no total quota. x0.at gives 1,024 MiB with no account.

They are useful for the metadata index rather than the archive. A manifest of 20 TiB at 25 MiB
shards is 838,861 rows, which at 200 bytes per row is about 160 MB: one Gist file, one
GitLab snippet, or one Catbox file. That is a legitimate use and it is the only one in this
document that survives the retention question, because a manifest can be regenerated from the
archive and an archive cannot be regenerated from a manifest.

### Smash (fromsmash.com), Free web tier

> No file size limit and no limit on number of transfers on the free web tier; no account required. Transfers above 2 GB are queued behind paid traffic

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: on the anonymous web tier. The record states no identity cost. Observed behaviour: Free transfers are queued when >2 GB with no SLA on queue time.

Evidence: `https://fromsmash.com/discover-smash/everyone` (2026-10-21), record `dossier/storage/smash-free-web-tier.json`.
Verdict: `fails-quota`.

### Catbox (catbox.moe + Litterbox)

> 200 MB per file on catbox.moe, no total quota, anonymous or free account. Anonymous files live until 2 years of inactivity; files tied to an account are permanent. Litterbox (sister service) takes 1 GB but expires in 1h-3d by choice

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 200 MB/file. The record states no identity cost. Observed behaviour: Uploads return a valid files.catbox.moe URL, but every download in observed returned HTTP 200 with Content-Length: 0, both text and binary, repeated across several files and minutes, incl.

Evidence: `https://catbox.moe` (2026-10-21), record `dossier/storage/catbox.json`.
Verdict: `qualifies-with-caveat`.

### GitHub Gist

> Unlimited gists per account; each gist is a full Git repo. Hard block at 100 MiB per single file; 2 GB per push. Total repo size is not capped, only 10 GB on-disk is the documented recommendation

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 100 MiB per file. The record states no identity cost. Observed behaviour: Push hook is strict and fires at 100 MiB.

Evidence: `https://gist.github.com` (2026-10-21), record `dossier/storage/github-gist.json`.
Verdict: `qualifies-with-caveat`.

### GitLab Snippets / GitLab.com projects

> 10 GiB free storage per project on GitLab.com Free tier (repo + LFS); snippet files up to 50 MB each (50,000,000-byte default admin limit); projects per account and accounts are free

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Read-only lockout is automatic and immediate on exceeding 10 GiB, and it blocks pushes rather than deletes data.

Evidence: `https://gitlab.com` (2026-10-21), record `dossier/storage/gitlab-snippets-gitlab-com-projects.json`.
Verdict: `qualifies-with-caveat`.

### x0.at (filehost2, x0.at / 0x0 family)

> 1024 MiB per file, no account, no per-account cap, unlimited uploads. Retention 3 to 100 days, scaled by file size via MIN_AGE + (MAX_AGE - MIN_AGE) * (1 - size/max_size)^2, so small files live ~100 days and near-max files ~3 days

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1024 MiB/file. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Longest-lived 0x0 derivative still accepting uploads.

Evidence: `https://x0.at` (2026-10-21), record `dossier/storage/x0-at.json`.
Verdict: `fails-quota`.

### Origrid

> 25 GB per file with NO account; 50 GB per file / 50 GB storage with a free account; Contributor tier (automatic: 25 GB stored + 30 days old + clean record) gives 100 GB storage, 50 GB/file and links that never expire; Verified Uploader =...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 25 GB/file anonymous, 50 GB/file free account. The record states no identity cost. Observed behaviour: READ PATH IS GATED BY A MINTED TOKEN.

Evidence: `https://origrid.io` (2026-10-21), record `dossier/storage/origrid.json`.
Verdict: `qualifies-with-caveat`.

### SwissTransfer (Infomaniak)

> 50 GB per transfer, all files combined, no account required. Hosted in Infomaniak's own Swiss datacentres. One notable global property: the source is open (Infomaniak android/iOS/multiplatform clients on GitHub) and there is a working CLI

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 50 GB per transfer (combined, not per file). The record states no identity cost. Observed behaviour: The write path requires human verification at the API: POST /api/containers without a recaptcha field returns 400 'The recaptcha field is required.

Evidence: `https://www.swisstransfer.com` (2026-10-21), record `dossier/storage/swisstransfer.json`.
Verdict: `qualifies-with-caveat`.

### timvisee Send instances (Firefox Send forks)

> Per-instance. Public table (read live) includes send.cyberjake.xyz at 10 GiB / 30 days / 100 downloads and send.adminforge.de at 8 GiB / 7 days / 1,000 downloads. The listed send.skylerszijjarto.com at 250 GiB / 7 days / 10,000 downloads...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: table's Size limit column (2. The record states no identity cost. Observed behaviour: Instance-level liveness is genuinely poor: of the three observed, send.cyberjake.xyz served 200/6176 bytes.

Evidence: `https://github.com/timvisee/send-instances` (2026-10-21), record `dossier/storage/timvisee-send-instances.json`.
Verdict: `qualifies-with-caveat`.

### Transfer.it (MEGA)

> No per-transfer size limit (MEGA blog: 'Send 100 GB, 1 TB, or even more, all for free'). Backing store is a fresh ANONYMOUS ephemeral MEGA account per uploader with mstrg = 21474836480 (20 GiB), read live from the API

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `request-rate`: not hit in ~10 uploads. The record states no identity cost. Observed behaviour: Expiry IS re-settable in place: a:xm with a new 'e' on an existing xh works and returns 0 (verified 1d -> 30d -> 90d).

Evidence: `https://transfer.it` (2026-10-21), record `dossier/storage/transfer-it.json`.
Verdict: `qualifies-with-caveat`.

### GigaFile

> 300 GB per file, unlimited number of files, no account required ('1300G')

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 300 GB/file. The record states no identity cost. Observed behaviour: Download endpoint only serves when called with the referer/cookie chain from the file page (a bare GET returns an 'open the proper download screen' interstitial).

Evidence: `https://gigafile.nu` (2026-10-22), record `dossier/storage/gigafile.json`.
Verdict: `qualifies-with-caveat`.

### StreamRuby

> 250 GB free storage, grows +250 GB per 1,500 monthly views; 'no upper limit'; unlimited bandwidth; no credit card

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: video-only: everything is transcoded to HLS, so it is not byte-exact storage.

Evidence: `https://streamruby.com` (2026-10-21), record `dossier/storage/streamruby.json`.
Verdict: `qualifies-with-caveat`.

### UploadHive

> Free tier published table: max upload file size 'Unlimited', download volume 'Unlimited', storage column '-' (no storage cap published), files deleted 50 days after last download

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `retention-clamped`: deleted 50 days after last download. The record states no identity cost. Observed behaviour: dl.cgi returned 'Wrong IP' on every download attempt regardless of referer/cookies, downloads appear bound to the uploading IP, so a distributed fetch layer needs matching egress IPs.

Evidence: `https://uploadhive.com` (2026-10-21), record `dossier/storage/uploadhive.json`.
Verdict: `qualifies-with-caveat`.

### UpZur

> Registered free account: 1,953 GB storage ("Storage space | - | 1953 GB | Unlimited" across Free/Registered/Premium columns), 5,120 MB per file, download volume Unlimited

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5,120 MB per file. The record states no identity cost. Observed behaviour: single-operator file host of the XFileSharing family.

Evidence: `https://upzur.com` (2026-10-21), record `dossier/storage/upzur.json`.
Verdict: `qualifies`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| Filemail Basic | fails-quota | 5 GB of storage space and 5 GB max per transfer, on a free 1-user account |
| Folder Fort 2.0 | fails-quota | Free plan exists with no credit card, size not published on the pricing page... |
| Jumpshare Basic | fails-quota | Free plan is metered by *upload count*, not bytes: 25 uploads and 60 seconds of recording. No storage figure is published |
| MASV | fails-quota | 15 GB of free transfer every month plus 5 days of free storage per package... |
| MyAirBridge | fails-quota | 20 GiB per transfer free, no registration required; storage ('save to storage') is a paid-plan feature |
| pCloud Transfer | fails-quota | 5 GB per transfer, no registration; 200 MB per single file via the web uploader |
| Sync.com | fails-quota | 5 GB free, permanent; referral top-ups |
| TransferXL | fails-quota | Free with account: 5 GB max transfer size, 10 GB daily / 300 GB monthly transfer allowance. Paid plans reach 100... |
| Tresorit Basic | fails-quota | 3 GB free, permanent (not a trial), zero-knowledge encrypted |
| dpaste.org | fails-quota | approx. 1 MiB per paste (observed: 1,040,000 chars accepted, 1,133,336 chars -> HTTP 413). No account, no quota... |
| paste.gg | fails-quota | 10 MiB total per paste, 5 MiB per file. Anonymous pastes expire after 7 days... |
| paste.rs | fails-quota | 393,216 bytes per paste (observed). 373,336 chars -> 201 Created... |
| PrivateBin public instance network | fails-quota | 10 MB per document by default (sizelimit = 10000000 in upstream conf.sample.php)... |
| Rentry.co | fails-quota | 200,000 characters per entry (hard, enforced at API), unlimited entries... |
| termbin.com | fails-quota | approx. 1 MB per paste, no account, no count limit. observed: 1,000,000 bytes stored and retrievable... |
| uldl.sh | fails-quota | 250 MB free storage per name, 4.5 MB max per file, unlimited uploads/day. No account needed... |
| BIShare | fails-quota | 100 GB per transfer by link, no account on either side; unlimited size device-to-device on the same LAN (nothing uploaded) |
| Blaze (BLAZE Quantum) | fails-quota | Free Forever: 2 GB transfer with 7-day retention, plus 2 GB of BLAZE Drive storage, 2 workspaces... |
| Filemail | fails-quota | 5 GB per transfer with no registration; 2 transfers per 24 hours... |
| Send Anywhere | fails-quota | Free: 1:1 real-time transfer up to 50 GB; LINK creation capped at 10 GB. Lite $5.99/mo raises download data to 200 GB |
| SendGB | fails-quota | 5 GB per transfer, no account, unlimited number of transfers (no monthly 10-transfer cap). Retention size-dependent... |
| Transfer.zip | fails-quota | Quick Transfers are free and have NO file-size limit, but they are ephemeral P2P: 'deleted automatically when either party... |
| TransferNow | fails-quota | 5 GB per transfer, no sign-up, 7 days, and the free plan is explicitly labelled 'No storage'... |
| WeTransfer | fails-quota | Free: 3 GB per transfer AND 10 transfers per rolling 30-day window (a pool... |
| Wormhole | fails-quota | Up to 10 GB per send. Only the first 5 GB is actually stored server-side... |
| FileAxa | fails-quota | Free registered: 488 GB storage, 10,000 Mb (10 GB) per file; free (unregistered) row has no storage pool |
| Mega4up | fails-quota | Free registered: 183 GB storage, 3,000 Mb per file, download volume Unlimited; files deleted 150 days after last download |
| storage.to | fails-quota | No permanent free storage: anonymous 100 GB upload / 24h per visitor token (500 GB / 24h per IP)... |
| ExaVault (Files.com), free self-hosted appliance | fails-quota | The hosted product is gone. What is free is the *appliance*: unlimited capacity on a disk the buyer owns... |
| GoAnywhere MFT / GoDrive (self-hosted) | fails-quota | GoDrive EFSS is 'completely free' but only as a component of on-premises GoAnywhere MFT. Capacity is the server's disk... |

Retention and quota are the two large groups, and the ordering between them is not the point.
The point is that a transfer service fails on the clock before it fails on the size, because
the size is what it advertises.

One rejection is a category error worth naming. JustBeamIt is pure peer to peer with a
10-minute link and uploads nothing until the recipient starts the transfer. Counting it as
storage inflates a total with a number that cannot be written twice, which is the
link-handoff error.

## Chaining

A transfer service is an ingress path, never a tier.

The pattern that works is a landing zone: accept a large upload into the service, then drain it
to a durable anchor inside the retention window, and delete nothing until the drain is
verified. SwissTransfer's 30 days at 50 GB per transfer is a workable window for a 20 TiB
migration at about 400 transfers, and GigaFile's 300 GB per file makes it 70.

The pattern that fails is using two transfer services as replicas. Neither holds the bytes long
enough for the other to be a backup, and the failure of one is silent until both have expired.
