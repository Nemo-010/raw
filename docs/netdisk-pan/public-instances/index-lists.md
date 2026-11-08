# Index lists: where instances are announced, and how each index rots

A public instance is not self-announcing. It becomes visible because somebody
writes its hostname into a list, and every list in this population is either
curated, abandoned or dead. The curation is the property that decides what the
list can prove, and the three sources here fail in three different ways.

The question this document answers is which list to automate against and which
number a reader may take from each. The short answer: the live forum index is the
right discovery input and the wrong decay measurement; the GitHub post is the right
decay input and has stopped growing; the Telegram channel is dead.

## The comparison

Ordered by what a discovery loop gets from each, not by size.

| source | hosts | yield as discovery | yield as decay data | state |
| --- | --- | --- | --- | --- |
| `bangumi.tv/m/topic/group/472627` | 28 | highest: 20 listed mounts | none: pruned by a maintainer | live, maintained |
| GitHub list repositories | varies | high, and each addition is dated | high, because commits persist | live, maintained |
| `kuhehe.github.io/20240120224502/` | 144 | low: stopped adding hosts | **highest: 11 of 144 survived** | abandoned, still served |
| `t.me/s/alistshare` | 3 | zero | none | dead |

## The live forum index

`bangumi.tv/m/topic/group/472627` (read 2026-10-22) is the highest-yield input
measured. It is a flat forum page at `/m/topic/...` that needs no
login, and the read broker returns the whole post body rather than a snippet.

It yields 28 real hostnames from 31 hostname-shaped strings. Three of the 31 are
not instances: `ssl`, `www` and `www.kdocs.cn`, which are markdown artefacts and a
document service. Of the 28, 26 answered HTTP and 20 returned a non-empty mount
list.

Its distinctive property is that it publishes the **WebDAV credential in
plaintext** next to most sites:

```
[七米蓝仓库](https://al.chirmyram.com/)
  - url: https://al.chirmyram.com/dav/
  - 用户名: alist  密码: alist

[Alist追番](https://zhuifan.link/)
  - url: https://zhuifan.link/dav/
  - 用户名: zhuifan  密码: zhuifan  或  账号: guest  密码: guest
```

That is how the WebDAV read path was testable without an account, and it is why
[`webdav-fronting.md`](webdav-fronting.md) has measured PROPFIND results rather
than a description.

⚠ **A pruned list cannot be a decay measurement.** 20 of 28 listing mounts is
selection and not longevity: a maintainer removes dead entries every few weeks, so
the survivor rate from this list measures the maintainer's diligence. Use it for
discovery and use the abandoned GitHub post for decay.

Its own preamble states that the AList project was sold and recommends OpenList, a
community fork, for new deployments.

## The dated GitHub post, and why its date is wrong

`kuhehe.github.io/20240120224502/` (read 2026-10-22) is the only dated cohort
available and therefore the only way this topic can state a half-life at all.

Its metadata says `published: 2024-01-20T14:45:02Z`, the title is
`分享一些基于Alist搭建的资源站合集`, and the permalink path is the publish timestamp.
That reads like a frozen snapshot. It is not one.

The file at that path was committed **36 times**:

```
2025-06-17T14:45:50Z   last revision
2025-06-15T12:13:15Z
2024-11-13T07:45:48Z
2024-09-02T08:04:14Z
...
2024-02-29T14:59:37Z   earliest revision the API returns
```

and the body carries a section headed `3月23日新发现的alist资源站`, "AList sites newly
found on 23 March". The page begins `不定时更新中`, "updating from time to time". So
hosts were added to a permalink after its date, and the 144-host list mixes hosts
first listed in January 2024 with hosts added as late as mid-2025.

The earliest surviving revision contains 126 instance hostnames after noise
removal, of which 11 still list mounts. That gives 8.7% survival over 2.645 years
and a 9.0-month half-life, against 7.6% and 8.9 months from the 144 dated to the
publish date. **The correction changes the method and not the answer**, which is
the only reason the number is still usable. The arithmetic is in
[`README.md`](README.md#the-half-life-with-the-arithmetic-visible).

⛔ **A permalink date is not a content date until the commit history says so.**
The check is `git log --follow` on the path, or the GitHub commits API with
`path=`, before trusting any "snapshot" date.

⚠ **The repo stopped.** The last commit is 2025-06-17 and the newest section is
dated 23 March, so the list no longer tracks new hosts. It is a decay cohort and
not a discovery input.

## The dead Telegram channel

`t.me/s/alistshare` is finished. Its recent feed carries tools (`SaveAny-Bot`,
`TaoSync`, `Alist Helper`) rather than instances, and its pinned post is a notice
about excess use from January 2025.

Three hostnames from it were re-probed: `alist.xiaoya.pro` (302 to a consumer
portal), `media.advanced360.top` (302 to a host whose TLS fails) and
`al.chirmyram.com` (still working). One of three.

⛔ **Do not build a Telegram scraper for it.** The channel is recorded here so a
later probe does not spend its budget discovering that a discovery input stopped
producing discoveries. The record is
`dossier/netdisk-pan/alistshare-telegram.json`.

## The repositories worth watching by commit

A commit is a dated event and a forum post is not, which makes the GitHub diff the
only input that produces a reliable `first_seen`.

| repository | why | what a commit means |
| --- | --- | --- |
| `lm379/lm379-alist` | one instance operator's README, the most-maintained single instance, and it documents its own limits | a new mirror or a changed policy |
| `ChirmyRam/ChirmyRam-OneDrive-Repository` | the corpus behind `al.chirmyram.com` | new content, and the instance is alive |
| `kuhehe/kuhehe.github.io` | every revision of the 2024 cohort | a host added to a permalink, which is the bias this document warns about |
| `OpenListTeam/OpenList` (self-hosted) | `drivers/` is where a new anonymous driver appears | a new read path exists for a pan |

```bash
# the last two commits touching a list file: the diff is the discovery event
gh api "repos/lm379/lm379-alist/commits?path=README.md&per_page=2" --jq '.[].sha'
```

## The two unmeasured channels

Certificate transparency (`crt.sh?q=%25.alist.%25`) and GitHub code search
(`gh search code '"/api/public/settings"'`) are discovery channels with no
measurement. **Neither has been run.**

- certificate transparency: `unverified`. No query was made, so there is no
  measured yield, no false-positive rate and no rot rate. Subdomain enumeration
  would find hosts that were never announced, which is exactly the population the
  one writable instance came from, so it is plausibly the highest-value unmeasured
  channel.
- GitHub code search: `unverified` for the same reason. It would find self-hosted
  instances that were never announced.

⚠ **A channel nobody has run is not a channel that does not work.** Both are labelled
unverified in [`../auto-discovery.md`](../auto-discovery.md), and the loop must
run each once by hand before wiring it in.

## What an index cannot establish

An index records that a hostname existed and who wrote it down. It does not tell a
reader whether the host lists a mount, whether it accepts a write, or how long it will
live. Those are three separate probes, and
[`alist-openlist.md`](alist-openlist.md) is the protocol for all three.

⛔ **The advertised population and the writable population do not overlap.**
`data.yanshiqwq.cn`, the only writable host of 169, does not appear in the 2026
community index at all. Index scraping finds the read substrate; it does not find
the one thing that would change the answer. That is why the discovery design keeps
every hostname ever seen and re-probes it, rather than starting from the list each
month.
