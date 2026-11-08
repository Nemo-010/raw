# Running OpenList: the bridge, and which drivers need no account

Self-hosting is the last resort, after every hosted mode of this topic (`AGENTS.md`
section 2 rule 9).

OpenList is a Go program that mounts storage and serves it over five protocols.
A copy a reader runs on a rented machine lasts as long as that machine, and the
part that decides whether it works is not the bridge: it is which upstream the
bridge mounts and whether that upstream grants a read without an account.

This document covers the operations, the drivers that matter, and the two
mechanisms that a reader will otherwise discover at 3 a.m.

## The comparison

Sorted by how much of the arrangement the driver leaves the reader holding.

| driver class | example | account needed | what it gives | what breaks it |
| --- | --- | --- | --- | --- |
| local disk | `Local` | none | the disk on the VPS | the disk or the VPS |
| a mounted API | `Onedrive`, `GoogleDrive`, `139Yun`, `189CloudPC` | an OAuth token per account | capacity somebody else pays for | the token is revoked |
| a share-link driver | `Lanzou`, `123Pan`, `ilanzou` share modes | none for a public share | a read path with the pan's per-file cap | the pan closes share downloads |
| a cookie driver | `Quark`, `UC` | a configured cookie | the pan's files | the cookie expires and nothing says so |

⚠ **The `provider` field returns `unknown` for 23 of the 30 listable public
instances.** That is not a defect in them: an older AList v3 build does not always
expose the storage type. It is the field that decides the death mode, so an
instance that reports `unknown` cannot tell a reader whose account dies first.

## The two mechanisms

### Mechanism 1: the write gate is an OR, and only one side is in the bitmask

`server/middlewares/fsup.go` (read 2026-10-22):

```go
parentMeta, err := op.GetNearestMeta(parentPath)
if !user.CanWriteContent() && !common.CanWriteContentBypassUserPerms(parentMeta, parentPath) {
    common.ErrorResp(c, errs.PermissionDenied, 403)
    c.Abort()
    return
}
if !common.CanWrite(user, parentMeta, parentPath) {
    common.ErrorResp(c, errs.PermissionDenied, 403)
    c.Abort()
    return
}
c.Next()
```

`CanWriteContent()` is bit 3 of `Permission`, which is `mkdir+upload`.
`CanWriteContentBypassUserPerms` returns true when the nearest metadata entry has
`Write: true` and the path is that entry's own path, or a subpath when `WSub` is
set (`server/common/check.go`).

So **an instance operator enables anonymous upload by setting "write" on one
directory in the metadata panel**, and the guest's role keeps no write bit. That is exactly what
`data.yanshiqwq.cn` does: `permission: 256` (bit 8, WebDAV read), bit 3 clear, and
`write_content_bypass: true`.

⛔ **Read the AList issue on this before changing an instance's permissions.**
`github.com/AlistGo/alist/issues/9600` (read 2026-10-22) is somebody reporting that
a guest with no permissions could upload; a collaborator
replied that the cause is the metadata write switch, that it is designed to let
visitors upload when the role grants nothing, and that the same investigation found
a real bug in `JoinBasePath` where a user's `base_path` was never applied. The
oracle in [`../public-instances/alist-openlist.md`](../public-instances/alist-openlist.md)
comes from that thread.

### Mechanism 2: `base_path` rewrites every path, and it silently did not

`User.JoinPath` calls `utils.JoinBasePath(u.BasePath, reqPath)`. The bug in issue
#9600 was that `JoinBasePath` returned early whenever the path already began with
`/`, which is always, so a guest restricted to `/public` could request another
storage's absolute path and list it.

⚠ **A bridge's own access control is not a security boundary and this topic does
not treat it as one.** The operational fact is narrower and it matters: if a
`base_path` is set, verify it with a request to a path outside it, because on a
build before the fix the restriction is not applied.

## Mounting, in the order that fails least

1. **Decide the upstream before the bridge.** A bridge over an account that will
   be frozen is a month of work with a deadline nobody announces.
2. **Mount with the narrowest token you can issue.** An OAuth token scoped to one
   directory is replaceable; an account password is not.
3. **Set `base_path` per user and test it from outside.**
4. **Put the CDN in front before you publish anything**, because the egress bill
   arrives after the traffic does.
5. **Record the `provider` string.** It is the only visible clue to whose account
   is behind a mount.

## The drivers that need no account, and what they cost

A share-link driver turns a public share into a read path without anybody's
credential. That is the one arrangement that needs no identity at all, and its cost
is the pan's per-file cap.

| driver | identity | per-file cap | free-download of a share | useful for |
| --- | --- | --- | --- | --- |
| `Lanzou` (`lz`) | none for a public share | 100 MiB | yes | small files, patches, configs |
| `123Pan` (`ye`) | none for a public share | 100 GiB, above 100 MiB needs a login | yes | medium files |
| `ilanzou` (`iz`) | none for a public share | none stated | yes | medium files |
| `Quark` (`qk`) | a cookie | none stated | **no** | nothing without the cookie |
| `UC` (`uc`) | a cookie | none stated | **no** | nothing without the cookie |

The caps and the free-download column are the resolver project's first-party driver
table, read 2026-10-22; [`../public-instances/direct-links.md`](../public-instances/direct-links.md)
carries the full table with its source.

⛔ **The drivers with no account requirement have the smallest caps.** 100 MiB on
Lanzou is 100,000 objects for a 10 TiB working set, which is a file-count problem
before it is a storage problem. That is the whole trade in this table.

## What rots, and the order it rots in

**Tokens first.** A mounted API driver holds an OAuth refresh token, and the token
is revoked when the account is frozen, when the password changes, or when the
provider rotates its policy. The symptom is `failed get storage` on every listing
and `failed get dir: object not found` on a deep path.

**Share downloads second.** A pan that stops serving a share to a logged-out
visitor takes every share-link driver with it. `123pan` already requires a login
above 100 MiB, and the project's README notes that `UC` broke in July 2023 and
`123pan`'s large-file path in August 2023.

**The bridge itself last.** It is a static binary and it does not rot on its own.

## The upgrade path, which is a fork and not a version

AList was sold in June 2025: the project owner, the documentation, the code and the
community were all rewritten, and the original developer left the communities. The
community forked it as OpenList, which is where new work happens
(`OpenListTeam/OpenList`, 25,183 stars, last push 2026-10-21).

| signal | AList v3 | OpenList v4 |
| --- | --- | --- |
| `data.version` in `/api/public/settings` | `v3.x` | `v4.x` |
| `write_content_bypass` in a listing | absent | present |
| `site_title` default | `AList` | `OpenList` |

⚠ **The version string is the only reliable discriminator and it is not always
readable.** `pan.ios98.com` reports `v3.61.0` and `al.chirmyram.com` reports
`v4.2.7`, so both builds are in production on public instances today. A bridge
operator should run OpenList; a reader should not care, because the capability
protocol works on both.

## The measurement that says this is worth running

The two oldest instances in the population are also the two most stable readers:
`al.chirmyram.com` since 2022 and `zhuifan.link` on an AList v3.23 build from about
2022. **Age is the best single predictor of next-month survival**, and a bridge the
reader runs is the only one whose age the reader controls.

The population's half-life is about nine months; the arithmetic is in
[`../public-instances/README.md`](../public-instances/README.md).

## Chaining

The bridge takes one upstream and gives four protocols. Its place in the stack is
between a tenant the reader controls and a CDN the reader does not pay for:

```
tenant -> OpenList (/api/*, /dav, /s3, ftp, sftp) -> Cloudflare -> reader
```

[`cloudreve.md`](cloudreve.md) is the same shape with different trade-offs, and
[`cdn-fronting.md`](cdn-fronting.md) is the layer in front.
