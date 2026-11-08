# The public-instance half-life was an impression and is now 9.0 months, and the cohort that produced it was edited in place

- **When:** 2026-10-22T03:46:28Z
- **Status:** corrected
- **Supersedes:** `.tmp/seed/storage-research/ALIST-FINDINGS.md` section "The structural conclusion" and the netdisk-pan recon plan's 3 half-life table
- **Superseded by:** `docs/netdisk-pan/public-instances/README.md` section "The half-life, with the arithmetic visible"
- **Evidence:** `census3.py` and `probe-alist.sh` in `.tmp/work/w-netdisk/`; `final-probe.tsv` (42 hosts, two runs); the GitHub commits API for `kuhehe/kuhehe.github.io` path `20240120224502/index.html`; all read or run 2026-10-22
- **Confidence:** measured

## What we believed

Two claims, both stated as impressions, and both true in direction.

The seed wrote that volunteer instances are "ephemeral" and that a `.repl.co` host
had been shut down, and it recorded one wave in which 45 instances were probed and
only one was writable. It gave no rate, because one wave cannot give one.

The recon plan then fitted a half-life of **8.9 months** from a 144-host cohort
dated 2024-01-20, on the stated premise that the source page was "a dated snapshot,
which is what makes the half-life measurable".

## What we found

**The half-life is 9.0 months and the arithmetic holds, but the premise was
wrong.** The page at `kuhehe.github.io/20240120224502/` is not a snapshot. Thirty-six
commits touch that path. The earliest revision the GitHub API returns is
2024-02-29T14:59:37Z and the last is 2025-06-17T14:45:50Z, and the body carries a
section headed `3月23日新发现的alist资源站` ("AList sites newly found on 23 March") and
opens `不定时更新中` ("updating from time to time").

So the 144-host cohort mixes hosts first listed in January 2024 with hosts added as
late as mid-2025, which biases survival upward. Recomputing on the **126 hosts
present in the earliest surviving revision**, dated from that revision:

```
exposure = 2.645 yr,  survival = 11/126 = 8.73%
t1/2 = 2.645 x ln2 / ln(1/0.0873) = 0.752 yr = 9.0 months
```

against 2.754 yr and 11/144 = 7.64%, which gives 8.9 months. **The correction
changes the method and not the answer**, and that is the only reason the number is
still quotable.

The two claims that were genuinely new are a mechanism and a rate:

- **The write flag is not the write gate.** `write` in a listing is
  `common.CanWrite`, a per-user exclusion-list negation that is always true for a
  guest on no list; the upload gate is `CanWriteContent() (bit 3) || a per-path
  metadata override`. That is why 13 of 14 hosts that advertise the flag refuse the
  `PUT`, and why the seed's "8 of 9" was a count of a mechanism rather than a
  coincidence. Source: `server/handles/fsread.go` and `server/middlewares/fsup.go`,
  read 2026-10-22.
- **7.4% monthly turnover**, derived from the same fit as `1 - 0.5^(1/9.0)`. That
  number decides the discovery cadence: monthly, not daily.

The census was also re-derived from the raw probe files and differs from the plan's
figures: **169 hosts, 33 answering as an API, 30 listing mounts, 14 advertising a
write, 1 writable.** The plan reported 32, 29 and 1 from a 170-host population; the
difference is a union of overlapping host lists and four individually probed hosts
that the plan counted in the total but not in the numerators.

## How we found it

The plan's own appendix listed the cohort file, so the first check was cheap: the
GitHub commits API for that exact path, with `per_page=100`. Thirty-six rows came
back. That one call is what turned a snapshot into an edited page.

Then the earliest revision was fetched by its commit SHA, its hostnames extracted,
and the cohort split into "present at the first revision" and "added later". The
11 survivors all sit in the first group and **none of the 18 later additions
survived**, which is what a cohort biased toward recent hosts looks like.

The re-probe was run twice over the same 42 hosts, minutes apart, and the two runs
disagreed on 3 of 42 on the read axis. That 7.1% flake is why the write verdict is a
SHA-256 roundtrip and why retirement needs three strikes.

## What it cost us

A wrong sentence nearly shipped with a precise-looking number attached. The plan's
"8.9 months" was arithmetically correct on its inputs and rested on a premise a
single API call disproves. A reader would have had no way to tell.

The second cost is the census drift. Three documents could have carried 32, 29,
30 and 33 depending on which file was counted first. Re-deriving from the raw TSV
files, with the population rule written into the script's docstring, is what stopped
that.

## What a future session should do differently

**Before trusting any "snapshot" date, call the commits API with `path=`.** A
permalink contains a date and no promise. One request settles it.

**When a survival rate is computed from a list, state whether the list was
pruned.** A maintained list measures its maintainer, not the population, and the
2026 index in this topic is exactly that case: 20 of its 28 hosts list mounts,
which is selection and not longevity.

**Write the population rule into the script that computes the census.** The
difference between 29 and 33 listable hosts is a union of overlapping files, and
a hand-counted figure cannot be re-run by the reader who doubts it.
