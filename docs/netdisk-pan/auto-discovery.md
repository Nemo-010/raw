# Auto-discovery: the specification for the monthly loop

This document specifies a program that does not exist yet: inputs, stages, the
verification gate, the dedupe key, the state store, the schedule, the alert, the
retirement rule, and the failure modes with the measured evidence for each.

The design rests on one measured number and one measured mechanism. The number is
a 9.0-month half-life with 7.4% monthly turnover; the mechanism is that the
`write` flag is a different predicate from the write gate. Both are in
[`public-instances/README.md`](public-instances/README.md) with the arithmetic.
Everything below is a consequence.

## Why the loop exists, and what it must not optimise for

Four candidate motives, and only two are worth an automation.

| motive | value | why |
| --- | --- | --- |
| keep the read substrate current | high | a fetch path dies every nine months and a cache forgives it |
| alert on a newly writable instance | high | it has happened once in the measured population and it would change the answer |
| count instances | none | the count is a property of the index, not of the population |
| find capacity | none | 1 of 169 accepts a write, and that one is a home disk |

⛔ **The loop must not page anybody.** It writes one line to `BRIEF.md` and one
line to a run report. The event it watches for is rare, not urgent.

## Inputs, ranked by yield

| input | how to read it | yield | how it rots |
| --- | --- | --- | --- |
| `bangumi.tv/m/topic/group/472627` | the read broker on `/m/topic/...`, which needs no login and returns the whole post body | **highest**: 20 of 28 real hosts listed mounts | a maintainer prunes it, so it self-heals and hides churn |
| GitHub list repositories, watched by commit | `api.github.com/repos/<owner>/<repo>/commits?path=<file>&per_page=2`, then diff the two blobs | high, and the only source that yields a *dated* `first_seen` | repos persist after the sites die |
| `kuhehe.github.io/<YYYYMMDDHHMMSS>/` | the directory name is a publish timestamp; walk `git/trees/master` for all revisions | high for historical cohorts, low for new hosts | stopped updating; last commit 2025-06-17 |
| the recorded host list, re-probed | read `dossier/netdisk-pan/*.json` and extract every hostname | high, and it is the only input that found the writable host | it does not grow on its own |
| `linux.do`, `nodeseek.com`, `hostloc.com` | search with `include_domains=` only; the snippet carries the post body | medium and bursty: one viral post can add five hosts in a day | high |
| GitHub code search for the API path | `gh search code '"/api/public/settings"'` | medium; finds self-hosted instances never announced | not applicable |
| `t.me/s/alistshare` | the `/s/` preview | **zero**: the channel now posts tools and pins an excess-use notice | dead |
| certificate transparency, `crt.sh?q=%25.alist.%25` | not attempted | **unverified** | not measured |
| `gh search code` for compose files | not attempted | **unverified** | not measured |

⚠ **Two channels in this table are unverified.** Certificate transparency and
GitHub code search have no yield, no rot rate and no measured false-positive rate.
A loop built on them would be built on a guess. Run each once by hand before wiring
it in, and record what it returned.

⛔ **Do not crawl the open internet for port 5244.** That is a port scan, it gets
ranges blocked, and it measures the scanner rather than the population.

## The four stages

Monthly, each writing into `.tmp/<run>/tools/discover/`.

```
1  HARVEST    index pages + GitHub commit diffs since last run + forum searches
              -> candidates.txt     one hostname per line, with a provenance tag

2  EXPAND     for each candidate, follow same-page links that look like instances
              -> candidates-expanded.txt

3  GATE       run the capability probe over the deduplicated set
              -> results.tsv        the 22-column schema in alist-openlist.md

4  RECONCILE  diff results.tsv against dossier/netdisk-pan/*.json
              -> new.json  newly-dead.json  changed.json  alerts.txt
```

**Stage 1 detail, because it is the only stage that produces a reliable
`first_seen`.** A commit that adds a hostname to a list file dates that host.

```bash
# for each watched repository, the last two commits touching the list file
gh api "repos/OWNER/REPO/commits?path=PATH&per_page=2" --jq '.[].sha'
# then fetch both blobs, extract hostnames from each, and set-difference them.
# a hostname in the newer blob and not the older one has first_seen = that commit's date.
```

Watched repositories:

- `lm379/lm379-alist`: one operator's README, the most-maintained single instance
- `ChirmyRam/ChirmyRam-OneDrive-Repository`: the corpus behind `al.chirmyram.com`
- `kuhehe/kuhehe.github.io`: the 2024 cohort's source and its revisions
- `OpenListTeam/OpenList` (self-hosted): a new anonymous driver in `drivers/` creates a new read path

**Stage 3 must call the capability probe and not a liveness check.** A liveness
check on this population returns 33 and distinguishes nothing. The capability
probe returns 30 listable, 14 advertising a write, and 1 writable.

## The verification gate

The protocol in [`public-instances/alist-openlist.md`](public-instances/alist-openlist.md),
run in full, with these hard stops:

- A **challenge** response is recorded as `challenge` for the host, and the probe
  tries the host's other routes ([`../../METHODOLOGY.md`](../../METHODOLOGY.md)
  section 7). It never attempts to pass one.
- `permission` is **recorded and never acted on**. It is a bitmask whose bit 8 is
  WebDAV read, and the writable host reports 256 with no bit 3.
- `PUT -> 200` is **recorded and never acted on**.
- Only `PUT -> GET -> SHA-256 identical` sets `write_capability: verified`.
- **At most one 4 KiB object per host per run**, because a probe object is never
  deleted. The probe makes every request the classification needs.
- **Never delete.** Delete is denied on the one writable host, so a probe object is
  permanent.
- **Never recurse past one level** below the root.

## The dedupe key

**The registrable domain plus the API base path.** Not the hostname.

The reason is measured, twice.

`alist.qsesvick.top`, `alist-cdn.20237737.xyz` and the dead `alist.20237737.xyz`
are one operator with one corpus behind three names; the community index lists
`alist.qsesvick.top` as the WebDAV endpoint and `alist-cdn.20237737.xyz` as the
site. And six hostnames served the same 26-entry iOS-signing corpus, five of them
byte-identically: `ipa.p12.pp.ua`, `p.591meta.com`, `p.vx365.vip`,
`pan.applep12.vip` and `pp.591meta.com` all produced the listing hash
`6fb4c929e98c`.

Counting hostnames tripled the apparent population on one corpus and sextupled it
on another. Deduplicating by listing content reduced **30 listable hostnames to 26
distinct listings**.

Key construction: `eTLD+1` from an embedded table of the roughly 40 TLDs this
population uses, plus the `base_path` where it is not `/`, plus the hash of the
sorted `(name, size, is_dir)` triples of the root listing as the tiebreaker for
genuinely distinct instances on one domain.

```
pan.lm379.cn            -> lm379.cn
cloud.lm379.cn          -> lm379.cn            same key: one instance
alist.qsesvick.top      -> qsesvick.top
alist-cdn.20237737.xyz  -> 20237737.xyz
alist.20237737.xyz      -> 20237737.xyz         one instance behind three names
```

⚠ **The listing hash is not stable across requests on a live corpus.**
`pp.591meta.com` differed from the other five by one entry, and that entry changed
between two requests minutes apart. Use the hash as a tiebreaker and the registrable
domain as the key.

## The state store

**One JSON record per instance in `dossier/netdisk-pan/` is the state store.** Not
a separate database. This is the repository's one-fact-one-home rule applied to a
live population, and it means the loop produces dossier edits rather than a
parallel truth.

The observation log goes in `extras.observations[]`, which the schema allows as a
free object. That is the decision on where an observation log lives: **in the
record's `extras`, append-only**, and not in a side file, because a side file is a
second truth and the first thing to go stale.

```json
"extras": {
  "dedupe_key": "20237737.xyz",
  "aliases": ["alist.qsesvick.top", "alist-cdn.20237737.xyz"],
  "first_seen": "2024-02-29T14:59:37Z",
  "first_seen_source": "kuhehe.github.io revision at commit 5f5947f0",
  "last_verified_alive": "2026-10-22T03:21:00Z",
  "last_verified_dead": null,
  "consecutive_failures": 0,
  "observations": [
    {"at": "2024-02-29T14:59:37Z", "state": "listed", "entries": 5, "writable": false},
    {"at": "2026-10-22T03:21:00Z", "state": "listed", "entries": 5, "writable": false}
  ]
}
```

`observations[]` is append-only, and it is what lets the corpus measure its own
half-life over a year.

⚠ **The staleness policy will mark most of these records stale, and that is
correct.** `netdisk-pan` has a 21-day verify window, which is shorter than the
about-nine-month half-life. A record policy-stale but machine-verified yesterday
reads correctly because the document carries the current state and the record
carries the date. ⛔ **Do not teach `staleness.py` that `consecutive_failures`
means death.** `dead` in that script is a staleness band and not a verdict, and
conflating them breaks the report for every other topic.

## The schedule

- **Monthly, at a minute and a day that are not the first.** Cron `17 3 4 * *`.
  The minute is not `:00` and the day is not the 1st, because every scheduled job
  in the world fires then, and a sweep that meets that load measures it.
- **Why monthly and not weekly or daily.** 7.4% monthly turnover means one sample a
  month dates a death to plus or minus a month, which is the resolution the
  half-life has anyway. A weekly or daily loop dates a death no better than the
  half-life allows, so the half-life sets the cadence.
- **Per-run scope.** Every host of the list, all at once, with every request the
  classification needs, and 2 seconds between a host's write and its read-back: the
  wait is part of the measurement. No cap of the probe's own limits the requests
  ([`../../AGENTS.md`](../../AGENTS.md) section 2 rule 15).
- **A server's own pacing.** A host that answers 429 or 503 with `Retry-After` is
  read again after that time. A host that answers 429 with none is recorded with its
  status, and the probe reports the count it could not evaluate.
- **The scheduled sweep does not run on demand.** A probe covers any host it needs,
  whenever it needs, with every request the question needs
  ([`../../AGENTS.md`](../../AGENTS.md) section 2 rule 15); re-checking stale
  instances from `scripts/discover/probe-alist.sh` is such a probe.

## The alert

One type, one condition:

```
ALERT  when  write_capability becomes "verified"
       and   the previous record said anything else
```

Not "a new instance appeared", which fires several times a month and is noise. Not
"an instance died", which is the half-life and belongs in the digest. **A newly
writable public instance is the only event worth a human's attention**, because it
has happened once in the measured population and it is the one thing that would change
the answer.

Delivery is a line in the sweep's report. No email and no webhook: the alert is
for a later session, not for a pager.

A second-tier monthly digest, no alert: `new`, `newly-dead`, `changed-version`,
and `changed-upstream`, where the `provider` string moved and the instance operator swapped
the backing pan.

## Retiring a dead instance without deleting its record

Three strikes, because 7% per-run flake means one timeout is not a death.

```
run N    fail  -> consecutive_failures = 1   state stays live, no other change
run N+1  fail  -> consecutive_failures = 2   state "flapping", the document shows a warning
run N+2  fail  -> consecutive_failures = 3   verdict = "dead", last_verified_dead = now
                                             evidence gains the death record
```

The record is **never deleted and never leaves the dossier**. It loses its row in
the live table, which is generated from `verdict != dead`, and it gains a line in
[`dead-ends.md`](dead-ends.md). A host that comes back resets the counter and gets
a `history/` entry, because "it came back" is a fact about the population worth
keeping.

## The failure modes, with the evidence for each

| failure | what it looks like | how the design handles it |
| --- | --- | --- |
| **a challenge page read as a live host** | HTTP 200 with a filter response body. Measured: `pan.t-satoru.top` returned 403 with an interstitial, `alist.advanced360.top` returned 200 with `<title>Loading...</title>` and a `window.location.replace` carrying a JWT, `alist.zlion.top` returned 000 on a TLS failure | detect on the body, not the status. Test for `Just a moment`, `cf_chl_opt`, `turnstile`, `人机验证` **and** a redirect carrying `ch=` or `js=`. Record the host as `challenge` and try its other routes |
| **alive but empty** | `code: 200, total: 0`. Measured: `alist.ucu520.top` returns `code: 500, storage not found` while its web UI is fully up, and `mmpan.net` returns 200 with no body | require `total > 0` for `state: listed`; `empty` is its own state and not a pass |
| **an instance proxying somebody else's paid account** | the instance lists 4 TiB and serves it at CDN speed and the `provider` field says `Onedrive` or `139Yun`. Measured: `al.chirmyram.com` resolves a 29 GiB `.iso` to a SharePoint tenant, and `pan.timero.xyz` lists 1,724 entries with provider `Onedrive` | record `upstream_provider` and `fronting_cdn` as first-class fields. The document must say whose account, because that is what dies first |
| **the host rate-limits the probe** | 429, 503, or a silent empty body after N requests. `lm379.cn`'s own README states that too-frequent access triggers a human check or a temporary blacklist | read the host again after its own `Retry-After`; with none, record the status, and the probe **reports the count it could not evaluate** |
| **the read-back path is signed** | `PUT -> success` and `GET -> code 401, expire missing`. Measured on `pan.ios98.com`: 33 bytes in, 51 bytes of error out | resolve `raw_url` from `/api/fs/get` before hashing; if that also refuses, record `read-gated` and not writable |
| **the instance is a custom front end** | `/api/public/settings` returns `<!doctype html>`. Measured on `pan.lm379.cn`, which has public WebDAV and is fully usable and which no API probe can see | classify `custom-frontend`, then attempt a WebDAV `PROPFIND` with whatever credential the index publishes; otherwise `unprobeable`, which is an honest gap and not a dead host |
| **the same operator under three names** | three hostnames, one corpus, one death. Measured twice, on the 20237737 corpus and on the 591meta corpus | dedupe on `eTLD+1` plus `base_path` |
| **the probe changes what it measures** | a 4 KiB object left on a volunteer's disk forever, because delete is denied | one object per host per run, a self-describing name, never a delete attempt |
| **one run's flake read as a death** | 3 of 42 hosts flipped verdict between two runs minutes apart, which is 7.1% | three consecutive failures before `verdict: dead` |

## What to build first, and what it costs

The cheapest useful version is stage 3 plus stage 4 against the existing dossier:
re-probe every hostname already recorded, diff the result, and alert on a new
verified write. That needs no harvester, it is about 50 hosts, and it is the half
that stops the corpus rotting.

Stage 1 is the expensive half, and its most valuable piece is the GitHub commit
diff rather than the forum search, because a commit date is a `first_seen` and a
forum post is not.

⛔ **Do not build the harvester before the verifier.** A discovery loop without
the capability probe finds instances and cannot say which are real.
