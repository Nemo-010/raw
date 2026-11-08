# The write-flag lie is a mechanism, not a count: 13 of 14, and the bitmask cannot find the one that works

- **When:** 2026-10-22T03:51:03Z
- **Status:** corrected
- **Supersedes:** `.tmp/seed/storage-research/ALIST-FINDINGS.md` section "The trap that defines this whole slot" and `METHODOLOGY.md` 5.3's "eight of nine" example
- **Superseded by:** `docs/netdisk-pan/public-instances/alist-openlist.md` section "Trap 2 : `write` in the listing is not the write gate"
- **Evidence:** `server/handles/fsread.go`, `server/middlewares/fsup.go`, `server/common/check.go` and `internal/model/user.go` in `OpenListTeam/OpenList`, read 2026-10-22; one listing request against each of the 30 listable hosts, same session
- **Confidence:** measured

## What we believed

The corpus stated the write-flag lie as a count:

> Eight instances advertised `"write": true`; **all eight refused PUT** with
> `{"code":403}` inside an HTTP 200.

That is a true observation and it was recorded as the topic's defining trap.
`METHODOLOGY.md` 5.3 carries it as "eight of nine AList instances advertised
`"write": true` for the guest user and refused PUT".

## What we found

The count is 13 of 14, and the reason is not that operators misconfigure their
instances. **The flag and the gate are different predicates in the source.**

`server/handles/fsread.go` builds the listing response with:

```go
Write:              common.CanWrite(user, meta, reqPath),
WriteContentBypass: common.CanWriteContentBypassUserPerms(meta, reqPath),
```

`common.CanWrite` (`server/common/check.go`) returns true unless the user is named
in a metadata exclusion list. For an anonymous guest on no list it returns **true
always**, whatever the role permits.

The upload gate (`server/middlewares/fsup.go`) is:

```go
if !user.CanWriteContent() && !common.CanWriteContentBypassUserPerms(parentMeta, parentPath) { deny }
```

`CanWriteContent()` is bit 3. So the listing's `write` field says nothing about the
gate, `write_content_bypass` says everything about one of its two terms, and
neither is the answer on its own.

Measured over the 30 listable hosts, one request each:

| field | true | false | absent |
| --- | --- | --- | --- |
| `write` | 14 | 13 | 3 |
| `write_content_bypass` | **1** | 12 | 17 |

## The second correction, which is the more useful one

The plan's first pass used the `permission` bitmask to find a writable host and
would have reported **two**. `permission: 256` is bit 8, WebDAV read, and it is not
write. Both `data.yanshiqwq.cn`, which is writable, and `zhuifan.link`, which is
not, report 256.

The writable host is writable **because the bitmask is incomplete**. It reports
`permission: 256` with bit 3 clear, and a per-path metadata override grants the
write. So an argument from the bitmask finds zero hosts and misses the one that
matters.

⛔ **Read the bitmask to explain a result, never to reach one.**

## How we found it

The count came from one listing request per host. The mechanism came from reading
the four source files after the count would not explain itself: if `write` were the
gate, a `PUT` would not refuse while it said true.

The confirmation is the writable host's own response: `write: true` **and**
`write_content_bypass: true` **and** `permission: 256` with no bit 3. Three fields
that look contradictory are consistent once the two predicates are separated.

## What it cost us

A count without a mechanism gets re-learned on every new instance. The seed knew
that the flag lies and could not say which hosts to test, so a probe still had to
try every one. With the mechanism, the discriminator is `write_content_bypass` and
the answer is one field on one response.

The bitmask error is the more expensive one, because it is an attractive shortcut:
a number that looks like a permission and behaves like a different one. It would
have produced a confident wrong answer on the second run.

## What a future session should do differently

**When a count is surprising, read the code that produces it before writing the
count down.** Eight of nine is surprising. The reason it is eight of nine is one
line of Go, and that line is what makes the finding general.

**Never derive a permission from a bitmask without the function that consumes it.**
`CanWriteContent()` is bit 3; `permission` also carries bit 8 for a different
protocol. The mapping is documented in the struct comment and the gate is in a
different file, and only the second one decides.
