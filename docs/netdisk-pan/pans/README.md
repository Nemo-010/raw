# Pans: the provider survey, ordered by what registration costs

A pan is a consumer drive sold to a person. This document is the survey of the
ones that could hold 500 GiB or more, ordered by identity cost rather than by
price, because identity is what closes almost all of them to a registrant
without a PRC identity.

The answer, stated first: **one Chinese pan takes a foreign registrant on an email
address, and it is Ctfile.** Every other large Chinese quota is behind a +86
number, a real-name check, or a share download that requires a login the reader
cannot obtain.

## The comparison

Sorted by identity cost, which is the axis that decides reachability.

| pan | free tier | per-file cap | registry | identity | binding | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Ctfile | 5 TB | 20 GB | China | `email` | `retention-clamped` 30 days | qualifies-with-caveat |
| Lanzou | unlimited | 100 MiB | China | `any-phone` | `per-object-cap` | fails-quota |
| TeraBox | 1 TB | 128 GB shared | international | `email` | `per-object-cap` | qualifies-with-caveat |
| Yandex Disk | 5 GB | 1 GB | Russia | `any-phone` | `per-object-cap` | fails-quota |
| Cloud Mail.ru | 1 TB paid | not stated | Russia | `any-phone` | price | paid-only |
| FeijiPan | 10 GB, 1 TB by contract | 10 GB | China | `any-phone` | `per-ip-shaping` | fails-egress |
| 123pan | 2 TB | 100 GiB | China | `email` | `fails-identity` on the large tier | fails-identity |
| Baidu, Quark, UC, 115 | 10 GB to 2 TB | varies | China | `country-phone(86)` | - | fails-identity |
| PikPak | not established | not established | international | `email` | - | unverified |

The regional documents carry the detail: [`china.md`](china.md),
[`korea-japan.md`](korea-japan.md), [`russia-cis.md`](russia-cis.md),
[`western.md`](western.md).

## The identity wall, stated as one number

Of the eleven large consumer pans surveyed, **three** are reachable on an email
address or less: Ctfile, TeraBox and 123pan's free tier. The rest need a phone
number in a specific country or a real-name check.

⛔ **An unreachable quota is worth zero and the sentence that quotes it says so.**
Baidu's 2 TB free tier, Quark's and UC's 10 GB, and 115's capacity are all real and
all closed to a registrant without a PRC identity. They are recorded as
`fails-identity`, not as candidates.

## Ctfile: the one that opens

Ctfile (城通网盘, `ctfile.com`) is a Chinese pan that has been running since 2009 and
it is the only one in this survey where the registration form offers **email and
password as the primary path** with "Sign up with phone instead" as the alternative.

- **5 TB of shared space free, 20 GB per file** (`documented`, 2026-10-22), and
  30 GB per file on Standard.
- **No upload speed cap** on any tier, which is unusual: the tiers differ on
  download speed, not upload.
- **WebDAV is advertised on the free tier** and as batch download on Super.
- **Files are deleted after 30 consecutive days without a sign-in** on a free
  account, or 365 days on a paid one, and over-quota deletes the excess without
  prior notice.
- **200,000 files and 10,000 folders per account, 10,000 uploads per day, 5
  concurrent downloads and 5 concurrent uploads.**

Evidence: `ctfile.com/register` (read 2026-10-22) for the form and the 5 TB / 20 GB
figures, `ctfile.com/help` for the per-file limits and the email registration, and
`ctfile.com/terms`, clause 3.2.5 for the 30-day deletion, clause 3.2.7 for the
file count and clause 3.2.9 for the concurrency.

Verdict: `qualifies-with-caveat`. The identity gate is open, the quota is real, and
the binding constraint is the 30-day clock. That makes it a working set behind a
monthly cron job, not an archive.

⚠ **`5 TB` here is the decimal figure the vendor states.** It is 5,000,000,000,000
bytes and the record says `TB`. It is not converted to TiB, because converting a
stated decimal figure is how a 10% error enters a plan.

## Lanzou: unlimited space, 100 MiB files

Lanzou (蓝奏云) genuinely offers unlimited total storage and genuinely does not
limit downloads. Its per-file cap is 100 MiB, which is the whole problem: 100 MiB
over a 10 TiB working set is 100,000 objects, and the file count becomes the
constraint before the bytes do.

Registration is a Chinese-language form, so the identity cost is recorded as
`any-phone` and not as `email`. The vendor page
states unlimited space, unlimited download speed and permanent share links
(`documented`, 2026-10-22).

Verdict: `fails-quota`. The total is real and the cap makes it a patch host, not a
store.

## TeraBox: a terabyte free, and no first-party limits page

TeraBox offers a terabyte free on registration, which is the largest single-tier
free quota in the consumer set. The vendor writes the figure one thousand and
twenty-four gigabytes, which this document quotes as 1 TB rather than converting
it. The site's own title and the app store listing both state it
(`reported`, 2026-10-22).

What could not be established: the per-file upload cap (128 GB is the *sharing*
figure the app listing states), retention, egress terms, and whether an email-only
registration produces a usable account. **The landing page returned a verification
interstitial on 2026-10-22**, so the record is `reported` and not
`documented`.

Verdict: `qualifies-with-caveat`. 1 TiB is worth knowing about and nothing about it
could be confirmed first-hand.

## Yandex Disk: the free WebDAV path closed

5 GB free, 1 GB per file without a plan, and a documented REST and WebDAV API. The
fact that changed: **from 2026-06-22, WebDAV access requires a Yandex 360 plan**
(`documented`, 2026-10-22, `yandex.com/support/yandex-360/customers/disk/web/en/webdav`).
The free tier's role was as a small always-available mount and that role is gone on
a published date.

Verdict: `fails-quota`. 5 GB with a 1 GB per-file cap is three orders of magnitude
below the working set, and the mountable protocol now costs money.

## Cloud Mail.ru: a paid tier, not a free one

The landing page read on 2026-10-22 offers 1 TB at **RUB 1,560 for the first year
and RUB 3,000 from the second**, with nine months added, under a promotion running
2026-10-15 to 2026-11-19. No free terabyte tier appears on the page.

⚠ **This contradicts the "Mail.ru 1 TB free" records in the storage topic**,
which are that topic's to reconcile. This record is scoped to the pan's role
here and says `paid-only`.

Verdict: `paid-only`.

## The pans that are closed, with the reason

Recorded so nobody re-tests them:

- **Baidu**: 2 TB free, a +86 number for registration, and a free single-file cap
  of 1 GB on web / 4 GB on the desktop client. `fails-identity`.
- **Quark**: 10 GB free and share downloads refused without a login.
  `fails-identity`.
- **UC**: 10 GB free and share downloads refused without a login. Its resolver
  driver broke in July 2023 and needs a cookie. `fails-identity`.
- **115**: the free-space allocation was withdrawn; a community thread from
  2026-07-31 answers "现在没有了，唯有氪金", "there is none now, only paying".
  The resale market for 115 accounts is in [`../paid/README.md`](../paid/README.md).
- **FeijiPan**: 10 GB free with 1 TB by a signed developer agreement, and the
  resolver project warns of frequent account bans and blocked datacentre IPs.
  `fails-egress`.
- **123pan**: 2 TB free and a share above 100 MiB requires a login, so the read
  path is closed; the 20 TB tier is CNY 258/year and behind an identity check.
  `fails-identity`.
- **PikPak**: the pricing page is served as a binary body that neither the reader
  nor the fetch broker would return as text. `unverified`, with the reason.

## Chaining

A pan is only useful in this topic as the upstream of a bridge. Ctfile on email
plus a 30-day cron job is the one combination that works without a +86 number, and
[`../self-hosted/alist-openlist-ops.md`](../self-hosted/alist-openlist-ops.md) is
what mounts it.

```
Ctfile (email, 5 TB, 30-day clock) -> OpenList -> Cloudflare -> reader
```
