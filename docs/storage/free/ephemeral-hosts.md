# Ephemeral hosts: the 3 to 100 day lane, and the retention treadmill

This class is where the largest per-object caps in this topic live, and it is the class that
looks most like a win until the retention column is read. A host that accepts 300 GiB in one
file and deletes it after 14 days is a transfer service, and treating it as an archive is the
most expensive misreading available in this topic.

The 10 qualifying records are the hosts that accept a large object without an
institution. 15 more were rejected, and the reason is usually the clock rather than
the size.

## The comparison

Sorted by per-object cap, with the retention beside it. The two numbers belong on the same row
and neither is meaningful alone.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| DeepStorage (deepstorage.dev) | Free: 2 TB storage + 50 GB/month uploads... | - | - | fails-quota |
| FEX.NET | Up to 50 GB of files shareable without registration... | - | anonymous* | qualifies-with-caveat |
| FileDitch (new.fileditch.com) | No total storage quota stated; 'no limit on the number of files you can upload'... | per-object-cap: 150 GB per file | anonymous* | fails-egress |
| firestorage.jp `ファイヤーストレージ` | Unregistered and free-member tiers: per-file max 300 GiB... | per-object-cap: 300 GiB per file | anonymous* | qualifies-with-caveat |
| Hitfile | Homepage headline: 'Your free and unlimited file storage'... | per-ip-shaping: 60 KB/s, one download per IP with que | - | qualifies-with-caveat |
| Lanzou `蓝奏云` | Unlimited total storage on the free:. Per-file cap is the binding constraint... | - | - | qualifies-with-caveat |
| Mintfile | Up to 300 GB per transfer, free, no sign-up... | per-object-cap: 300 GB per transfer | - | qualifies-with-caveat |
| Patrins | Free 8 GB forever. Pro from $5/mo = 1 TB... | per-object-cap: 1 TB file | card | qualifies-with-caveat |
| Turbobit | Unlimited total: 'The total volume and number of your files are unlimited'... | per-object-cap: uploads are capped at 200 MB | - | qualifies-with-caveat |
| VIP (u-p.vip) `优盘` | VIP1 (free on registration): 500 GB+ storage... | per-object-cap: 5 GB per file | - | qualifies-with-caveat |

## What the class is

An ephemeral host is defined by a retention clock that the uploader does not control. Six of the
ten qualifying records publish a clock, and the range is 3 to 100 days at GigaFile, 14 days at
firestorage.jp, and a month of inactivity at DeepStorage before the free allowance changes.

The class also contains the hosts whose retention is a business model rather than a policy.
pixeldrain resets its 60-day clock only when a GET moves more than 10% of a file. 1fichier
resets on a "qualified access" and explicitly excludes automated accesses. A keep-alive loop
therefore has to be shaped to each host's definition of a touch, and a loop that works on one
will silently fail on another.

## The three retention models, and what each does to an archive

The distinction is operational and it decides whether a keep-alive loop can hold the data.

**Time from upload.** GigaFile's 3 to 100 days and firestorage.jp's 3 to 14 days are this model.
The band is set when the object is uploaded, so a plan can pick the long end; it cannot be
extended afterwards, so the only defence is re-upload, which costs the full bandwidth of the
archive on every cycle. At 20 TiB and a 14-day clock that is 1.43 TiB per day of re-upload, which
is more than the serving workload, and at firestorage.jp's 3-day default it is 6.67 TiB per day,
which is not a plan at all.

**Time from last access.** pixeldrain's 60 days, file.kiwi's 90 hours and ZeroFS's 15 days are
this model. A keep-alive is viable in principle, but the definition of access differs and each
one must be read rather than assumed.

**Activity-based.** Buzzheavier's 8-day base with 2 days per download up to 60 days, and
permanent at 30 downloads per 60 days, is the most complex model in this topic. It rewards a
loop that downloads the object, and the download itself is subject to the same challenge gate
as any other read.

## The write-path throttle behind a large quota

Two records here are worth reading together because they show the pattern from both sides.

DeepStorage's free tier is 2 TB of storage with 50 GB per month of uploads. Its Community tier
is "unlimited, while you are in the channel" with 200 GB per month, unlocked by joining a
Telegram channel. The storage is not the constraint; the upload budget is, and it is 50 GB per
month against a 10 TiB working set. The 200 GB figure belongs to the Community tier, not the
free tier; attaching it to the free tier understates the throttle by a factor of four.

Lanzou states unlimited total storage with no download limit and no speed limit, and its
per-file cap is the binding constraint. That claim is about storage and egress and says
nothing about the write path, which is where this class usually fails.

## FEX.NET, and the 155 GiB figure that belongs to FileDitch

FEX accepts up to 50 GB of files shareable without registration, and its paid tiers step from
16 GB to 9 TB. The figure "155 GiB" belongs to FileDitch's uploader constant only. FEX's
ceiling is 50 GB per unregistered share.

The correction matters because a shard plan built on 155 GiB for both would size chunks three
times too large for one of them. The two records are separate and their caps are separate.

## The Chinese regional hosts

Four records here are Chinese or ex-Soviet file hosts found through forums. Lanzou's free tier
now requires a +86 SMS, which moves it to
`netdisk-pan/write/registerable-pans.md` for the signup question while the retention fact stays
here.

### DeepStorage (deepstorage.dev)

> Free: 2 TB storage + 50 GB/month uploads; Community: storage 'Unlimited, while you are in the channel' + 200 GB/month, unlocked by linking Telegram and joining their channel

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: very new, single-operator service that funds itself on $9/mo Pro.

Evidence: `https://deepstorage.dev` (2026-10-21), record `dossier/storage/deepstorage.json`.
Verdict: `fails-quota`.

### FEX.NET

> Up to 50 GB of files shareable without registration; paid tiers step 16 GB -> 9 TB. No free permanent quota published

That is the record's own wording (`reported`, 2026-10-21). The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Russian-market host.

Evidence: `https://fex.net` (2026-10-21), record `dossier/storage/fex-net.json`.
Verdict: `qualifies-with-caveat`.

### FileDitch (new.fileditch.com)

> No total storage quota stated; 'no limit on the number of files you can upload'. 150 GB maximum per file

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 150 GB per file. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: The bandwidth/CDN host itsfileditchfiles.st puts a Cloudflare managed challenge in front of datacenter IPs: a plain curl GET of an uploaded file returned 403 'Just a moment' (and 403 thr.

Evidence: `https://new.fileditch.com` (2026-10-21), record `dossier/storage/fileditch.json`.
Verdict: `fails-egress`.

### firestorage.jp

> Unregistered and free-member tiers: per-file max 300 GiB, unlimited number of uploads. The free *member* storage drive is only 2 GiB (25 GiB light, 100 GiB regular), the 'capacity unlimited' claim applies to the transfer service, not the...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 300 GiB per file. The identity cost is anonymous, read off the record's own text (`inferred`). Observed behaviour: Two different caps on the same site (2 GiB from the front page.

Evidence: `https://firestorage.jp` (2026-10-21), record `dossier/storage/firestorage-jp.json`.
Verdict: `qualifies-with-caveat`.

### Hitfile

> Homepage headline: 'Your free and unlimited file storage'. No numeric total quota published anywhere on the site

That is the record's own wording (`inferred`, 2026-10-21). The constraint that binds is `per-ip-shaping`: 60 KB/s, one download per IP with que. The record states no identity cost. Observed behaviour: Blog/inventory claim only, 'unlimited' is a headline, with no docs page stating it and no per-file number anywhere.

Evidence: `https://hitfile.net` (2026-10-21), record `dossier/storage/hitfile.json`.
Verdict: `qualifies-with-caveat`.

### Lanzou

> Unlimited total storage on the free:. Per-file cap is the binding constraint, and it is tier-set in ->

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Registration is SMS-gated on a Chinese mobile number, which is the hardest registration gate in this class.

Evidence: `https://www.lanzou.com` (2026-10-21), record `dossier/storage/lanzou.json`.
Verdict: `qualifies-with-caveat`.

### Mintfile

> Up to 300 GB per transfer, free, no sign-up, 100 files per transfer. There is no total-storage account at all, it is a per-transfer envelope

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 300 GB per transfer. The record states no identity cost. Observed behaviour: Retention max 100 days plus a mandatory malware scan on every file makes this a transfer service.

Evidence: `https://mintfile.com` (2026-10-21), record `dossier/storage/mintfile.json`.
Verdict: `qualifies-with-caveat`.

### Patrins

> Free 8 GB forever. Pro from $5/mo = 1 TB, one-time payment that stacks (10 months buys 12); Unlimited from $10/mo; Teams 2-40 TB pooled

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 1 TB file. A new account costs card. Observed behaviour: No credit card for free tier.

Evidence: `https://patrins.com` (2026-10-21), record `dossier/storage/patrins.json`.
Verdict: `qualifies-with-caveat`.

### Turbobit

> Unlimited total: 'The total volume and number of your files are unlimited'. Free unregistered uploads are capped at 200 MB; registered free accounts go much higher (operator advertises up to 100 GB file transfer volume)

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: uploads are capped at 200 MB. The record states no identity cost. Observed behaviour: Free-tier serving is throttled to dial-up speeds and gated behind a human-verification step and a queue, so it works as storage but not as a fetch origin.

Evidence: `https://turbobit.net` (2026-10-21), record `dossier/storage/turbobit.json`.
Verdict: `qualifies-with-caveat`.

### VIP (u-p.vip)

> VIP1 (free on registration): 500 GB+ storage, 120 GB on signup plus 380 GB for registering the partner app, with +100 GB per invited user, (unlimited expansion). Per-file 5 GB on VIP1

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 5 GB per file. The record states no identity cost. Observed behaviour: The entire free-storage economy is a shopping-rebate funnel, capacity is denominated in invites and points from a third-party app.

Evidence: `https://web.u-p.vip` (2026-10-21), record `dossier/storage/vip.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| AkiraBox | fails-egress | unlimited storage advertised; 5 GB/file anonymous, 20 GB/file with a free account |
| ayaya.beauty | fails-quota | no account; 1 GiB per file |
| DropMeFiles | fails-quota | no account; up to 50 GB per transfer |
| File Garden | fails-quota | free, 'forever' retention; per-file and per-account caps not published on the landing page |
| File.io | fails-quota | no account; 4 GB per transfer ('file transfers are limited to a total of 4 GB') |
| Filebin | fails-quota | no account; per-bin, no published byte cap; bins expire 6 days after creation |
| temp.sh | fails-quota | no account; 4 GB per file, 3-day retention |
| tmpfiles.org | fails-quota | no account; 100 MB per file |
| transfer.archivete.am | fails-quota | no account; no published per-file cap (transfer.sh successor, same DutchCoders codebase) |
| Uguu | fails-quota | no account; 128 MiB max upload |
| DDownload | fails-quota | Ultimate (paid, EUR 3.33-14.99/mo): 'Unlimited Storage' and 'Unlimited File Size'... |
| Katfile | fails-quota | No free storage quota published; premium advertises 'Download files up to 200 GB' and bandwidth blocks up to 18 TB |
| Keep2Share / TezFiles (same operator) | fails-egress | Free plan: 10 GB/day of download traffic, no storage quota published. Paid Premium Max: 100 GB/day... |
| Nitroflare | fails-quota | Free: 'You can upload up to 10 GB files, for free!'. No free total-storage figure published anywhere on the site |
| Rapidgator | fails-quota | Free: 5 GB upload per file, no storage allowance published... |

The rejections are dominated by quota, and the second group is retention. That ordering is
misleading and worth stating: a host rejected for quota joins a long list, while a host
rejected for retention is the one a reader will otherwise adopt, because its per-object cap is
the largest on the page.

The third group is `not-storage`, and it holds the services whose "unlimited" describes an
allowance that resets monthly. A monthly allowance is not a quota: it is a rate, and a plan
that sizes against the first month discovers the ceiling on the second.

## Chaining

An ephemeral host is a write buffer, never a tier.

The pattern that works is a two-stage write: land the burst on a host with a large per-object
cap and a short clock, then drain it to a durable anchor through a job that runs inside the
clock. GigaFile at 300 GB per file and 100 days is the best buffer in this topic for that,
because the retention band is chosen at upload rather than imposed.

The pattern that fails is chaining two ephemeral hosts, because their clocks do not align and
the second copy expires while the first is being read.
