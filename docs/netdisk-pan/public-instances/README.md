# Public instances: how big the population is, and why one in thirty is writable

A public instance is one person's server mounting storage they do not own and
serving a guest session to anyone who asks. There are hundreds. The question this
document answers is how many of them are useful, and the answer is a ratio rather
than a list, because the list is different every month.

The ratio: of 169 hostnames, 33 answered as an AList or OpenList API, 30 exposed
a mount list, and **1 accepted a write and returned the bytes**. The protocol that
establishes those numbers is [`alist-openlist.md`](alist-openlist.md). This
document is the population: how it was sampled, how fast it turns over, and why
the last number is a structural zero with one exception.

## How the population was sampled

Three lists, one probe script, one day.

| source | source date | hostnames | what it is |
| --- | --- | --- | --- |
| `kuhehe.github.io/20240120224502/` | 2024-01-20, edited until 2025-06-17 | 144 | an HTML post listing AList sites, used as the decay cohort |
| `bangumi.tv/m/topic/group/472627` | read 2026-10-22 | 28 | the live community index, with WebDAV credentials beside most entries |
| a 25-host list | 2026-10-21 | 25 | hosts named one day before the probe, re-probed here |
| four individually probed hosts from the 2026 index | 2026-10-22 | 4 | hosts the index lists that the other sources did not carry |

Deduplicated by hostname across the first three, that is 166 hostnames. Three of
the four individually probed hosts are new, so the total is **169**.

⚠ **169 is a sample, not a census of the population.** It is what two index lists
and one host sweep produced. The population is whatever the discovery loop in
[`../auto-discovery.md`](../auto-discovery.md) can reach, which is a larger and
unknown number.

⚠ **Two counting rules give two answers, and both are stated here.** A host was
probed more than once where the lists overlap, and the two runs disagreed on a few
hosts. Counting a host as an API host if **any** run saw it answer gives 33 API
hosts and 30 with a listing; counting on the **last** run alone gives 32 and 27.
The single host behind the difference is `alist.tianmoy.cn`, which flaps. The
documents use the any-run rule because a host that answered once has a read path.

⚠ **Two counts of the same population differ by one host and one API host.** Adding
the four individually probed hosts to the 166 gives 170, but one of the four,
`file.cnxiaobai.com`, is already inside the 166, so the population is **169**. The
recon plan's 32 was its last-run API count, and its 29 was a listing count under a
stricter rule; this document states 33 and 30 under the any-run rule written
above. The writable count of 1 is the same under every rule, which is the number
the topic rests on.

## The four numbers

| measure | count | share of 169 | how it was decided |
| --- | --- | --- | --- |
| answered as an AList or OpenList API | 33 | 19.5% | `GET /api/public/settings` returned JSON with a `code` field |
| exposed an anonymous mount list | 30 | 17.8% | `POST /api/fs/list` on `/` returned `code: 200` with a non-empty `content[]` |
| advertised `write: true` on a mount | 14 | 8.3% | any listing carried `"write": true` |
| accepted a verified write | 1 | 0.6% | `PUT` then `GET` then a SHA-256 match |

The 33 breaks down as 30 that list and 3 that answer but list nothing:
`alist.ucu520.top` (structurally broken), `mmpan.net` (200 with no body) and
`pan.iosrxwy.com` (flapping). A fourth, `pan.xyyh.xyz`, listed on one run and not
on the other.

⚠ **The population is 169 hostnames and 26 distinct instances.** Six hostnames
were one corpus, so the readable population is smaller than the counts above
suggest; the dedupe is in "Duplicates" below.

## The half-life, with the arithmetic visible

The decay measurement is the reason the 2024 index was worth extracting. It is
the only dated cohort available, and a dated cohort is the only way this topic can
state a turnover rate at all.

Two facts have to be established first.

**Fact one: 11 of the 144 hosts still list mounts.** That is 7.6%.

**Fact two: the page's date is not its content date.** The permalink
`20240120224502` reads as 2024-01-20 and the page's own metadata says
`published: 2024-01-20T14:45:02Z`. The file at that path was committed **36
times**, the earliest revision the GitHub API returns is 2024-02-29T14:59:37Z and
the last is 2025-06-17T14:45:50Z, and the body carries a section headed
`3月23日新发现的alist资源站` ("AList sites newly found on 23 March"). Hosts were
added to a permalink after its date, so the 144-host list mixes hosts first listed
in January 2024 with hosts added as late as mid-2025.

So the fit is computed twice, and both are shown because the reader should see
that the correction does not rescue the method, only the conclusion.

**On the 144 hosts as probed, dated from the page's publish date:**

```
exposure   = 2026-10-22 - 2024-01-20 = 2.754 yr
survival   = 11 / 144              = 7.64%
t_half     = 2.754 x ln2 / ln(1/0.0764)
           = 2.754 x 0.6931 / 2.5719
           = 0.742 yr
           = 8.9 months
```

**On the 126 hosts present in the earliest surviving revision, dated from that
revision:**

```
exposure   = 2026-10-22 - 2024-02-29 = 2.645 yr
survival   = 11 / 126              = 8.73%
t_half     = 2.645 x 0.6931 / ln(1/0.0873)
           = 2.645 x 0.6931 / 2.4384
           = 0.752 yr
           = 9.0 months
```

**The answer is 9 months, and the model behind it is wrong in a known direction.**
The constant-hazard fit assumes a host is equally likely to die in any month,
which the evidence contradicts: instances die in batches when a provider revokes a
shared token, when a Cloudflare bill arrives, or when an operator closes WebDAV
for excess use. A batched process has a heavier tail than an exponential one, so 9
months is an average and not a schedule.

⚠ **The margin is wide and the sample cannot narrow it.** n = 144 from one
cohort, one measurement date, one run. Eleven survivors could be ten or twelve on
another run, which moves the answer between 8.6 and 9.2 months. State it as
"about nine months", never as 8.9.

**The monthly turnover follows from the same fit, and it is the number that
decides the discovery cadence:**

```
monthly turnover = 1 - 0.5^(1/9.0)
                 = 1 - 0.5^0.1111
                 = 1 - 0.9260
                 = 7.4% per month
```

7.4% a month is why the discovery loop runs monthly and not daily. A daily sample
of a population that turns over 7.4% a month gains about a quarter of a percent of
resolution per day and multiplies the requests by thirty. The cadence argument is
in [`../auto-discovery.md`](../auto-discovery.md).

## Why one in thirty is structural and not bad luck

The writable fraction is not a sampling artifact for three reasons, and each one
is a measurement.

**The flag and the gate are different predicates.** `write` in a listing is
`common.CanWrite`, a per-user exclusion-list negation that is always true for a
guest on no list. The upload gate is `CanWriteContent() (bit 3) || a per-path
metadata override`. So a host reports `write: true` while holding no write bit,
and 13 of the 14 hosts that advertise the flag refuse the `PUT`. One host,
`data.yanshiqwq.cn`, reports `write_content_bypass: true` and is writable. The
mechanism is in [`alist-openlist.md`](alist-openlist.md); the point here is that
it explains the whole population and predicts that the next wave will find the
same ratio.

**Two independent sweeps found the same host.** A probe on 2026-10-21 and another
on 2026-10-22 each found exactly one writable instance, and it was
`data.yanshiqwq.cn` both times. The second probe ran four times over the whole
population and got the same answer each time. That rules out a one-run fluke. It
does not rule out a fluke of the two sweeps, and no measurement available here
could.

**The writable host is not in the live index.** `data.yanshiqwq.cn` does not
appear in the 2026 community index at all. The advertised population and the
writable population do not overlap, which is an argument against index scraping
as the discovery method for the one thing that matters and an argument for
keeping every host ever seen and re-probing it.

## The noise floor, which is larger than it looks

Two runs of the same script over the same 42 hosts, minutes apart on 2026-10-22:

| axis | run 1 | run 2 | hosts that flipped |
| --- | --- | --- | --- |
| answered as an API | 32 | 33 | 2 |
| returned a listing | 29 | 28 | 3 |

3 of 42 flipped on the read axis, which is **7.1%**. The three were
`alist-cdn.20237737.xyz`, `alist.jiejingfan.vip` and `alist.tianmoy.cn`.
`alist.jiejingfan.vip` was hand-probed three times in a row and answered once and
timed out twice at 8 seconds.

⚠ **A single timeout is not a death.** At a 7% per-run flake and a 9-month
half-life, one failure carries almost no information and three consecutive
monthly failures carry most of it. That is where the three-strike retirement rule
comes from, and it is a consequence of the measurement rather than a preference.

## The population by upstream, which predicts what dies first

The `provider` field from the listing is the only visible clue to whose storage
is behind an instance, and it decides the death mode.

| upstream | instances | who holds the bytes | how it dies |
| --- | --- | --- | --- |
| a pooled tenant (`Onedrive`, `GoogleDrive`, `139Yun`, `189CloudPC`) | 5 | an operator's paid account, re-exported | the tenant is revoked or the account frozen |
| the instance operator's own disk (`Local`) | 2 | the instance operator | the disk, the VPS or the instance operator's interest goes |
| `unknown` | 23 | not visible from outside | unknown, which is itself the finding |

The five pooled-tenant instances are `pan.timero.xyz` (Onedrive, 1,724 entries),
`share.xiaole88.com` (Onedrive), `zhuifan.link` (GoogleDrive), `alist.jiejingfan.vip`
(139Yun) and `pan.dumpapp.com` (189CloudPC). The two `Local` ones are
`file.i80k.com` and `kho.t0m.top`.

⛔ **`unknown` on 23 of 30 is the honest answer and not an omission.** AList
returns `unknown` when the storage driver does not expose its type, which is
common on the older v3 builds. A record that guessed `Local` for those would be
inventing the field that decides the death mode.

## Duplicates: 30 hostnames are not 30 instances

Six hostnames served the same 26-entry iOS-signing corpus, and five of them
returned byte-identical listing bodies: `ipa.p12.pp.ua`, `p.591meta.com`,
`p.vx365.vip`, `pan.applep12.vip` and `pp.591meta.com` all hashed to
`6fb4c929e98c`. The sixth, `ppp.591meta.com`, differs by one entry that changes
between requests, so the corpus is live and shared.

⛔ **A hostname count is not an instance count.** Deduplicating by the content of
the root listing reduced 30 listable hostnames to **26 distinct listings** on
2026-10-22. The dedupe key for a discovery loop is the registrable domain plus the
API base path, and the reason is measured: `alist.qsesvick.top`,
`alist-cdn.20237737.xyz` and the dead `alist.20237737.xyz` are one instance
operator and one corpus behind three names.

## What the population is good for

Read and egress, with a cache and a fallback. Not storage.

`al.chirmyram.com` returned `cf-cache-status: HIT` on a 36,747,196-byte PDF,
honoured `Range` with 206 and `Content-Range: bytes 0-1048575/36747196`, and
produced a 1 MiB ranged read in 71 to 88 ms across five attempts, which is 11.4 to
14.1 MiB/s. Its content sums to 7.43 TiB from the size fields alone. That is a
real read substrate and it costs the reader nothing.

⚠ **The throughput number does not scale and must not be quoted as a curve.**
Six whole-object reads of the same 36,747,196-byte file measured 11.5 to 79.6
MiB/s, because the object was already in Cloudflare's edge cache and the variance
is the CDN's, not the host's. Parallel ranged reads at 8 and 32 connections
measured **below** the single-stream baseline, which is the signature of a shared
edge cache and not of shaping. [`../self-hosted/cdn-fronting.md`](../self-hosted/cdn-fronting.md)
carries that measurement in full.

## The verdicts in the population

| verdict | count | what it means |
| --- | --- | --- |
| `qualifies-with-caveat` | 26 | a working read path, no write, usable as a fetch substrate |
| `fails-egress` | 1 | `pan.ios98.com`: the write lands and the read-back is signed |
| `dead` | 7 | five hosts plus the two the protocol cannot classify |

The exact records are in `dossier/netdisk-pan/`, one per hostname, and
[`../dead-ends.md`](../dead-ends.md) groups the dead ones by the shape of the
failure.
