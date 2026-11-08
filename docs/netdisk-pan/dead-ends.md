# Dead ends: every host that is gone, by the shape of its death

At a 9-month half-life the dead list only grows. This document groups the dead
hosts by the **shape** of the failure, because the shape is what the next probe
should test for, and a list of hostnames teaches nothing.

Every row was probed on 2026-10-22 and has a `verdict: dead` record in
`dossier/netdisk-pan/` with the evidence of its death. This page is a view of those
records; the records are the home.

## The four shapes

| shape | what the probe sees | how many here | what it means |
| --- | --- | --- | --- |
| repurposed domain | a 3xx to a consumer portal or a different product | 2 | the instance operator stopped and the domain was sold or reused |
| no TCP service | `000` on a TLS handshake failure | 1 | nothing is listening |
| challenge page | 200 or 403 with a filter response body | 2 | alive and closed to a probe |
| answering but empty | a valid API and no storage or no files | 4 | the hardest case, because the status says alive |

⚠ **Four of the nine are "answering but empty", and that is the shape a
status-code check cannot see.** More than half the dead hosts return HTTP 200.

## Repurposed domain

**`alist.xiaoya.pro`**: 小雅 xiaoya, the most widely published public instance in
the population. It returns **302** on `/api/public/settings`, to a consumer portal
rather than to an API. The mechanism: shared Aliyun tokens were revoked and the
instance went to 504; the domain has since been repurposed.

**`alist.20237737.xyz`**: the original hostname of the 七十二时 corpus. It returns
**301** with no AList API behind the redirect. The same corpus is still served at
`alist.qsesvick.top` and `alist-cdn.20237737.xyz`, so the instance operator moved
and the original name did not. This is the case that makes hostname counting wrong: a
hostname can die while the instance lives on under two others.

## No TCP service

**`alist.zlion.top`**: Zlion, a film and anime instance. It returns **000** on a
TLS handshake failure. The community index records the sequence:
`之前有 WebDAV，因滥用现已关闭`, "it had WebDAV before, now closed because of misuse".
The WebDAV route closed first and the host followed.

⚠ **This is the death order to expect.** An instance that is being used as a PCDN
uplink loses WebDAV before it loses the site, because WebDAV is the cheapest route
to draw downstream bandwidth from the instance.

## Challenge page

**`pan.t-satoru.top`**: an instance from the 2024 cohort. It returns **403** with
an automated-traffic filter interstitial. No fetch path passed it, so its
capability is `unverified` and it is unusable as a substrate for the same
reason a dead host is.

**`alist.advanced360.top`**: a cookie gate that is neither JSON nor a page. It
returns **HTTP 200** with a **502-byte** body whose SHA-256 is
`770fedcf5d7b62a606978c08b3753fb6ed3c90e6fcae1cb9ecd45fc8e5b88992`:

```html
<html><head><title>Loading...</title></head><body><script type='text/javascript'>
window.location.replace('https://alist.advanced360.top/api/public/settings?ch=1&js=eyJhbGci...&sid=...');
</script></body></html>
```

That is not JSON and it is not a page. It is a cookie gate that sets a JWT and
redirects once, and a `is_challenge()` test that only looks for Cloudflare's markup
passes it as a live instance.

⛔ **Test the body for a redirect carrying `ch=` or `js=`, not only for
`Just a moment` and `cf_chl_opt`.**

## Answering but empty

The four that a status check calls alive.

**`alist.ucu520.top`**: a complete OpenList v4.2.6 front end. `/api/public/settings`
returns 200 with a valid payload, and `/api/fs/list` returns
`{"code":500,"message":"failed get storage: storage not found; please add a storage first"}`
**inside an HTTP 200**. The software runs and no storage is configured.

**`media.advanced360.top`**: the media mirror. It returns **302** to
`ww547.advanced360.top`, whose TLS handshake then fails. The redirect and the
pinned notice about excess use are two ends of one shutdown.

**`mmpan.net`**: answers the AList API and returns HTTP 200 on `/api/fs/list` with
no parseable body, on two separate runs. There is nothing to read and no error to
record beyond that.

**`pan.xyyh.xyz`** and **`pan.iosrxwy.com`**: the two the protocol cannot classify.
Each answered as an AList API on one run and as a non-API on another minutes later,
and neither ever returned a stable listing. `pan.xyyh.xyz` listed 2 entries once,
and its zero-byte oracle returned neither `file exists` nor `permission denied`.

⚠ **These two are recorded `dead` with the flake named, and that is a deliberate
choice.** At a 7.1% per-run flake rate, one failure carries almost no information;
but a host that has never produced a stable listing across four runs has not been
useful once. The three-strike rule in
[`auto-discovery.md`](auto-discovery.md) is what a scheduled loop uses; a single
sweep records what it saw.

## Closed and not probed as instances

These are not hosts but routes, and each one closed for a structural reason.

- **`t.me/alistshare`**: the channel now posts tools and pins a notice about
  excess use. A discovery input that stopped producing discoveries.
  Record: `dossier/netdisk-pan/alistshare-telegram.json`.
- **`alist.xiaoya.pro` via a shared Aliyun token**: the mechanism, not the host:
  when a pooled token is revoked the instance goes to 504 and every mount behind it
  becomes `object not found`. That is the failure mode of every pooled-tenant
  instance in the population, and five of them are alive today.
- **A `repl.co` subdomain AList**: several hostnames in the 2024 cohort are
  `.repl.co` deployments, and Replit shut that hosting tier down. All of them
  return 000.

## What this list is for

Two things, and both are worth more than the count.

**It stops a re-attempt.** A reader who finds `alist.xiaoya.pro` in an old list
would spend a probe rediscovering that it 302s. This page says so before the probe.

**It dates the population.** Nine dead of the 169 probed, plus the four dead of
the 25 hosts listed on 2026-10-21, is the visible edge of a 7.4% monthly turnover. The
half-life arithmetic is in
[`public-instances/README.md`](public-instances/README.md).

⛔ **A dead record is never deleted.** A host that comes back gets its counter reset
and a history entry, because "it came back" is a fact about the population. A
deleted record re-opens a question that took a probe to close.

## The dead in the 25-host list

<!-- fx-netdisk-deferral:start -->
The records for the closed instances named in this page, by slug, so a
reader can find the evidence behind each row above:

- `alist-20237737-xyz`: the primary host of 七十二时, now 301-looping through openresty; only the -cdn mirror answers.
- `alist-advanced360-top`: a media instance behind a JavaScript cookie gate that is neither JSON nor a page.
- `alist-qsesvick-top`: a 七十二时 mirror that answers as an API and serves nothing of use.
- `alist-tianmoy-cn`: a write flag it refused inside an HTTP 200, and a host that flipped between two runs.
- `alist-ucu520-top`: a complete OpenList web UI and `code: 500, storage not found` inside an HTTP 200.
- `alist-xiaoya-pro`: 小雅 xiaoya, the most widely published instance in the population, now 302 to a consumer portal.
- `alist-zlion-top`: a TLS handshake failure, and a WebDAV withdrawn for excess use before that.
- `media-advanced360-top`: the media mirror, now 302.
- `mmpan-net`: 200 with no body: the second shape of answering-but-empty.
- `pan-iosrxwy-com`: a host that flaps between listing and not answering.
- `pan-t-satoru-top`: 403 behind an automated-traffic filter interstitial.
- `pan-xyyh-xyz`: listed on one run and refused on the next, which is the population's per-run flake.
<!-- fx-netdisk-deferral:end -->

A 25-host list dated 2026-10-21 names the following hosts, one day before the
probe. Of those 25:

| state on 2026-10-22 | count | hosts |
| --- | --- | --- |
| still list mounts | 16 | `al.chirmyram.com`, `zhuifan.link`, `alist.jiejingfan.vip`, `w2.apachecn.org`, `pan.timero.xyz`, `alist-cdn.20237737.xyz`, `www.yhcres.top`, `pan.jinnan.top`, `pan.mediy.cn`, `s3.776161.xyz`, `cloud.zsxwz.com`, `share.xiaole88.com`, `file.i80k.com`, `alist.tianmoy.cn`, `alist.shenzjd.com`, `data.yanshiqwq.cn` |
| alive, no API | 3 | `pan.lm379.cn` (custom front end), `media.advanced360.top`, `demo.cloudreve.org` |
| dead | 4 | `alist.xiaoya.pro`, `alist.20237737.xyz`, `alist.zlion.top`, `alist.advanced360.top` |
| broken but answering | 1 | `alist.ucu520.top` |

⚠ **Nine of 25 changed in one day, and that is not a decay rate.** It is the list
having recorded hosts at different moments, plus ordinary flapping, plus one real
regression. Do not quote it as a rate; the rate is the 144-host cohort's 9.0
months.
