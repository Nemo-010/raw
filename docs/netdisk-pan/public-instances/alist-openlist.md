# How to tell a real AList or OpenList instance from a fake one

AList and its fork OpenList are one Go program that mounts other people's storage
and serves it over a REST API, WebDAV, S3, FTP and SFTP. That makes a public
instance cheap to run, which is why 169 hostnames were probed and 33 answered as
one. It also makes an instance cheap to fake, because the API is unauthenticated
by default and every signal it returns about permission can be wrong.

This document is the protocol. It says what each response shape means, in the
order a script should ask, and it names the three shapes that decide the answer.
Every one of them was measured on 2026-10-22.

## The answer, in one paragraph

A host is alive when `/api/public/settings` returns JSON with a `code` field. It
is readable when `POST /api/fs/list` on `/` returns `code: 200` with a non-empty
`content[]`. It is writable **only** when a `PUT` of a known 4 KiB object is
followed by a `GET` whose SHA-256 matches. Nothing else establishes a write,
including an HTTP 200 from the `PUT` itself, and including every flag the API
returns about it.

## Step 0: kind and liveness, one request

```
GET /api/public/settings
```

| response | means |
| --- | --- |
| `200`, JSON, has `code` and `data` | AList or OpenList. `data.version` separates them: `v3.x` is AList, `v4.x` is OpenList |
| `200`, HTML starting `<!doctype html` | a custom front end. Not probeable by API and possibly fully usable over WebDAV |
| `200`, HTML with `Just a moment`, `cf_chl_opt`, `turnstile` or `人机验证` | a challenge page. Record it as challenge and try the host's other routes ([`METHODOLOGY.md`](../../../METHODOLOGY.md) section 7); never pass one |
| `200`, HTML with `<title>Loading...</title>` and `window.location.replace(...ch=1&js=` | a JavaScript cookie gate. Also a challenge page, and the one with no vendor name on it |
| `404` JSON, or `200` with `code: 404` | not an AList. Try `GET /api/v4/site/ping` for Cloudreve |
| connect error, timeout, or `000` | dead |
| `301` or `302` to a consumer portal | the domain has been repurposed or seized |

The last two rows are the ones a status-code check gets wrong. `alist.xiaoya.pro`
answered 302 and `alist.zlion.top` answered 000, and both are dead. `alist.advanced360.top`
answered **200** with a 502-byte body whose SHA-256 was
`770fedcf5d7b62a606978c08b3753fb6ed3c90e6fcae1cb9ecd45fc8e5b88992`, and it is
also dead: the body is `<title>Loading...</title>` and a `window.location.replace`
carrying a JWT, which is a gate and not a page.

⚠ **The challenge surface is not only Cloudflare's markup.** A test that
recognises `Just a moment` and `cf_chl_opt` passes `alist.advanced360.top` as a
live instance. Test the body for a redirect carrying `ch=` or `js=` as well.

## Step 1: who am I, one request

```
GET /api/me
```

| response | means |
| --- | --- |
| `{code: 200, data: {username: "guest", role: 1, permission: N, base_path: "/..."}}` | an anonymous guest session exists |
| `code: 401`, or `Guest user is disabled, login please` | the instance is alive and closed. A definite no for both read and write |
| `code: 200` with `disabled: true` | same as above |

Record `permission` and `base_path`, and **decide nothing from `permission`**.
Step 4 explains why.

`base_path` matters more than it looks. `zhuifan.link` reports
`base_path: /新番/anime/new` and `w2.apachecn.org` reports `/公共`, so `/` in the
API is not the instance root and a listing that looks empty may be a listing of a
subtree.

## Step 2: the root listing, one request

```
POST /api/fs/list   {"path":"/","password":"","page":1,"per_page":0,"refresh":false}
```

| response | means |
| --- | --- |
| `code: 200` with a non-empty `content[]` | **the read path works.** Record `total`, `provider`, `write`, `write_content_bypass` |
| `code: 200` with an empty `content[]` | alive but empty. Not a usable instance |
| `code: 500`, `failed get storage: storage not found` **inside HTTP 200** | structurally broken: the web UI is up and no storage is configured |
| `code: 500`, `failed get dir: object not found` | the mount is configured and the upstream is gone |
| `code: 403`, `permission denied` | the guest may see the site and not `/`. Retry at the `base_path` |
| `code: 401`, or `Guest user is disabled` | closed |

The `provider` string identifies the upstream and is the field that explains
what dies first: `Local` is the instance operator's own disk, `Onedrive`, `GoogleDrive`,
`139Yun` and `189CloudPC` are pooled accounts somebody else pays for.

⛔ **`code: 500` inside HTTP 200 is the shape that defeats a liveness check.**
`alist.ucu520.top` serves a complete OpenList v4.2.6 front end, answers
`/api/public/settings` with 200, and returns `storage not found` for every
listing. A probe that reads the status calls it alive.

## Step 3: mounts, one level

List each root entry in turn.

| response | means |
| --- | --- |
| `code: 200` with `content[]` | the mount is live and browsable |
| `code: 500`, `object not found` | the mount is a stub. Common: `alist.jiejingfan.vip` and `w2.apachecn.org` both carry half-dead trees |
| `code: 403` | the mount exists and the guest cannot read it |

⛔ **Do not recurse past one level.** One level classifies the host. Deeper is an
enumeration of somebody's corpus, and the classification does not need it.

## Step 4: the write question, which is where the topic lives

Two stages. The first costs one byte and proves nothing on its own. The second
costs 4 KiB and is the verdict.

### 4a. The zero-byte permission oracle

`server/middlewares/fsup.go` checks the write permission **before** it notices
that the target exists, and `server/handles/fsup.go` then returns `file exists`
when `Overwrite: false` and the path is already there. So a `PUT` aimed at an
existing directory returns one of two messages and writes nothing:

```
PUT /api/fs/put     File-Path: /<existing root directory>     Overwrite: false     body: 1 byte
```

| response body | means |
| --- | --- |
| `{"code":403,"message":"file exists"}` | the permission **passed**; nothing was written |
| `{"code":403,"message":"permission denied"}` | the permission **failed**; nothing was touched |
| `{"code":200,...}` | it overwrote a directory. Inconclusive, so run 4b |

Both responses carry `code: 403` and both arrive inside HTTP 200. **The message
is the signal and the code is not.** On 2026-10-22 `al.chirmyram.com` returned
`permission denied` and `data.yanshiqwq.cn` returned `file exists`.

This is the only honest pre-filter available, because it decides the question
without uploading anything. It is necessary and not sufficient.

### 4b. The roundtrip, which is the verdict

```
PUT /api/fs/put     File-Path: /<uuid>-probe.bin     body: 4096 bytes with a known SHA-256
```

| `PUT` response | means |
| --- | --- |
| `{"code":200,"message":"success"}` | the write **may** have landed. Not a verdict |
| `{"code":403,"message":"permission denied"}` inside HTTP 200 | no. **This is the dominant shape: 13 of the 14 hosts that advertise the flag** |
| `413`, or `code: 413` | the fronting CDN's body limit. Record it as a per-object cap |
| HTTP 200 with an HTML body | the single-page app swallowed the request and the route is not what it appears |
| `code: 500`, `failed get storage` | the mount died between the listing and the write |

Then read it back and hash it:

```
GET /p/<the same path>
```

| read-back | means |
| --- | --- |
| `200`, digest identical | **writable. The only yes** |
| `200`, 51 bytes, `{"code":401,"message":"expire missing"}` | the instance signs its raw path and a guest cannot mint the signature. `pan.ios98.com` measured exactly this: 33 bytes in, 51 bytes of error out |
| `302` to a signed CDN URL | follow it and hash the **final** body, after redirects |
| `404`, or `code: 404` | the `PUT` reported success and stored nothing |
| `200` with a different digest or length | never writable. A host that does not give the bytes back is not storage |

## The three response shapes, exactly

These three are the core of this document. Each one was reproduced against a live
host.

**1. `file exists` means the permission passed.**

```
PUT /api/fs/put   File-Path: /rep   Overwrite: false   body: x

{"code":403,"message":"file exists"}
```

Nothing was written. The handler reached the existence check, which is *after*
the permission check, so the permission gate opened. This is a `yes` about
permission and says nothing about the write.

**2. `permission denied` inside HTTP 200 is the dominant lie.**

```
HTTP/1.1 200 OK

{"code":403,"message":"permission denied"}
```

The status is the envelope and the body is the answer. This shape appeared on 13
of the 14 hosts advertising `write: true`. `pan.jinnan.top` is the cleanest case:
its root contains a directory literally named `05 游客上传`, its mount advertises
`write: true`, and every `PUT` returns this. The instance operator intended guest
upload and the permission never reached the guest role.

**3. `success` then `expire missing` means the write landed and the reader cannot read it.**

```
PUT /api/fs/put   ->  {"code":200,"message":"success"}
GET /p/<path>     ->  200, 51 bytes,  {"code":401,"message":"expire missing"}
```

The bytes went in. The raw path is signed and the signature is minted by
`POST /api/fs/get`, which a guest can call and then must use immediately. For a
reader the verdict is no: a host that accepts bytes it will not return is a
one-way sink, which for an archive is data loss on a delay.

## The two traps worth more than the three shapes

### Trap 1: `permission: 256` is bit 8, and it is not write

`/api/me` returns a `permission` bitmask, and a large number invites the reading
"can write". The bit meanings are in the struct comment in
`internal/model/user.go`:

```
bit 0  see-hides        bit 4  rename         bit 8  webdav-read      bit 12 read-archives
bit 1  no-password      bit 5  move           bit 9  webdav-write     bit 13 decompress
bit 2  offline-download bit 6  copy           bit 10 ftp-read        bit 14 share
bit 3  mkdir+upload     bit 7  remove         bit 11 ftp-write       bit 15 custom-share-id
```

**256 is bit 8, WebDAV read.** A guest with `permission: 256` can mount the
instance over WebDAV and read, and cannot upload. Both `data.yanshiqwq.cn`, which
is writable, and `zhuifan.link`, which is not, report `permission: 256`.

⚠ **The bitmask is also not exhaustive, which is the more useful half of the
lesson.** The upload gate in `server/middlewares/fsup.go` is:

```go
if !user.CanWriteContent() && !common.CanWriteContentBypassUserPerms(parentMeta, parentPath) {
    common.ErrorResp(c, errs.PermissionDenied, 403)
}
```

`CanWriteContent()` is bit 3. The second term is a **per-path metadata override**:
an instance operator can enable writing on one directory for users who hold no write bit
at all. `data.yanshiqwq.cn` is exactly that case. It reports `permission: 256`,
its bit 3 is clear, and it accepts writes because the metadata on one path grants
them.

⛔ **Read the bitmask to explain a result, never to reach one.** On the measured
population an argument from `permission` would have found zero writable hosts
and missed the one that matters.

### Trap 2: `write` in the listing is not the write gate

This is the trap that produces the headline number, and its mechanism is worth
stating exactly.

`server/handles/fsread.go` populates the listing response with two different
predicates:

```go
Write:              common.CanWrite(user, meta, reqPath),
WriteContentBypass: common.CanWriteContentBypassUserPerms(meta, reqPath),
```

`common.CanWrite` returns true unless the user is named in a metadata
exclusion list (`server/common/check.go`). For an anonymous guest on no list it
is **always true**, whatever the role permits.

`write_content_bypass` is the second term of the actual upload gate, so it is the
field that mirrors the permission that decides a `PUT`.

The measurement, over the 30 listable hosts, one request each:

| field | true | false | absent |
| --- | --- | --- | --- |
| `write` | 14 | 13 | 3 |
| `write_content_bypass` | **1** | 12 | 17 |

`write_content_bypass` is an OpenList v4 addition. It is absent on all 17 AList
v3 builds and on `pan.ios98.com`, so it is a strong positive signal and a weak
negative one: a true is the writable host, and an absent is "use the oracle".

## The permission bitmask, and what a probe may do with it

A probe leaves no litter, because the thing it measures is a volunteer's server.

- **At most one 4 KiB object per host per run**, on a path that names itself. The
  probe makes every read the classification needs.
- **Never delete.** `data.yanshiqwq.cn` denies `/api/fs/remove`, so a probe object
  is permanent litter on somebody's disk.
- **Never work past a challenge page.** Record it, and try the host's other routes;
  never attempt to pass one.
- **Never recurse past one level** below the root.
- **Never assume `/p/` is the raw route.** Resolve `raw_url` from
  `/api/fs/get` first and fall back to `/p/`.

⚠ **The probe changes what it measures.** A run against 42 hosts left 42 files
that cannot be deleted. Six runs left six per host. That is a real cost, paid to
somebody who volunteered a disk, and it is the reason the write test is one
object and not a suite.

## The verdicts, and which rung carries them

| state | established by | rung |
| --- | --- | --- |
| alive | `/api/public/settings` returns JSON with a `code` | measured |
| readable | `POST /api/fs/list` on `/` returns a non-empty `content[]` | measured |
| writable | `PUT` of a known 4 KiB object, then `GET`, then a digest match | measured |
| read-gated | `PUT` returns success and the read-back returns 401 or 403 | measured |
| empty | `code: 200` with `total: 0` | measured |
| structurally broken | `code: 500, storage not found` inside HTTP 200 | measured |
| blocked by challenge | a filter response body on any route, once | measured |

⚠ **`alive-no-list` is not a verdict to argue about, it is a state to retire
from.** Four hosts in the population are alive and list nothing: `alist.ucu520.top`,
`mmpan.net`, `pan.iosrxwy.com` and `pan.xyyh.xyz`. Two of them flipped between
answering as an API and answering as a non-API within minutes, which is the
per-run flake this population has and the reason a death needs three strikes.

## What this protocol does not establish

It does not establish the upstream's quota, retention, or egress terms. A public
instance serves somebody else's bytes under somebody else's agreement, and the
`provider` string is the only clue to whose. `al.chirmyram.com` resolves a 29 GiB
`.iso` to a SharePoint tenant, which is why its single files reach tens of GiB.

It does not establish that a host will answer tomorrow. The measured half-life
is about nine months for the population, and the per-host flake is about 7% per
run, so one timeout is not a death.

It does not judge whether any of this is permitted by whoever runs the upstream.
This document records the mechanism, not a view about it.

## Evidence

Every claim above rests on a request made against a live host on 2026-10-22, or
on source code read on that date. The source citations are
`server/middlewares/fsup.go`, `server/handles/fsup.go`, `server/handles/fsread.go`,
`server/common/check.go` and `internal/model/user.go` in `OpenListTeam/OpenList`,
all read 2026-10-22. The AList issue that first
described the oracle is `github.com/AlistGo/alist/issues/9600`, read 2026-10-22,
where a collaborator confirms the `metadata write flag` mechanism and uses the
same non-writing probe.
