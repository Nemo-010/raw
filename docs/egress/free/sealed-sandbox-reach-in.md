# How does a machine that cannot listen get reached, and what does the path cost?

A sandbox that refuses `bind(2)`, a pubnix with no user ports, and a Worker that
answers only what it received have the same problem. Each runs code and cannot be
reached. The answer for all three is a rendezvous both ends dial out to, and the
rendezvous is a byte transport rather than a machine.

⭐ The relay measured here carries a whole SSH session in both directions and caps
one session at 64 MiB. That cap decides the question. The path is right for a
shell, a control channel and an orchestration job, and it is not a serving path,
because one day at 1 TiB would need 16,384 sessions.

This document is the measured record for the relay in
`dossier/egress/ajam-ssh-relay.json`. `RELAY_HOST` below stands for its host name. The
machine it reaches is the `compute` topic's; what the path costs is this topic's.

## What the service is

A WebSocket that carries a raw TCP stream. It does not implement SSH or any other
client protocol. Binary frames go to a public target, or between two paired peers,
and the bytes are copied in order (`documented`, the relay's own
`RELAY_HOST/llms-full.txt`, read 2026-10-22).

| purpose | address |
| --- | --- |
| forward, any public TCP target | `wss://RELAY_HOST/connect/HOST/PORT` |
| reverse node | `wss://RELAY_HOST/v1/node/NAME` |
| reverse operator | `wss://RELAY_HOST/v1/connect/NAME` |
| reverse status | `https://RELAY_HOST/v1/status/NAME` |
| self-service pair | `POST https://RELAY_HOST/v1/pair` |
| self-service forward token | `POST https://RELAY_HOST/v1/mint` |
| pool ranking | `https://RELAY_HOST/relays.json` |
| diagnostics | `https://RELAY_HOST/trace` |

The service reports itself as `tcp-ssh-relay` version `2026-10-03-r2`, with
reverse enabled and a 37-entry pool (`measured`, 2026-10-22, 1,436 bytes). The
version matters: `2026-10-01-r2` reported a four-entry pool, and the pool has grown by
33 placements in twenty days.

## The two ends, and why neither needs a port

A node dials `/v1/node/NAME` and keeps that socket. An operator dials
`/v1/connect/NAME` and the relay pairs the two by name. The node never becomes
addressable, so nothing on the machine's side has to accept a connection.

| the reverse path, as measured | result |
| --- | --- |
| `POST /v1/pair` with an empty body | 200, 312 bytes, a 128-bit name and three 64-hex tokens |
| the three tokens | `node_token`, `connect_token`, `stop_token`, each 64 hexadecimal characters |
| token lifetime | 72.0 hours from issue (`measured`, 2026-10-22) |
| a node that is not dropbear and not SSH | answered `hello`, `open` and `close`, sent `ready` and one data frame |
| the reverse-operator socket | received the text `ready`, sent binary, read the node's 44 bytes back |

That last pair is the useful control. The seed pass proved the reverse path with
`dropbear` over `dropssh` and a real SSH login. On 2026-10-22 a node that speaks
nothing but the relay's own control messages answered, so the reverse transport is
not SSH-specific (`measured`, 2026-10-22).

The relay's own words for the trust model are exact, and they are the constraint:
**it authenticates tokens, not people.** Both tokens on a pair are bearer
credentials, so anyone who reads the name and the tokens can open a session, and
the relay carries the plaintext byte stream it forwards.

## The four things that had to change on the sealed host

These are configuration, not patches. They are kept because "it works now" without
the failures it went through is not a reusable result.

**The passwd database must come from a file.** With no `/etc/passwd` the first
login was refused with `Login attempt with wrong user root`. `dropssh` ships a
`fakepwd.so` preload shim, but the `dropbear` in its v0.2.3 tarball is a static-pie
musl binary and a preload cannot interpose a static executable. `dropbear -Y FILE`
reads one `passwd(5)` line per login and is the only passwd path on that build.

**The passwd line must name the serving process's uid.** `dropbear` refuses a login
whose uid differs from the process serving it. A line beginning `root:0:0` failed
against a server running as uid 966; `966:x:966:965:...` worked. The entry's home
directory must also be owned by that user.

**The server's paths must not be world-writable.** Under `/tmp` dropbear refused to
start with `/tmp must be owned by user or root, and not writable by group or
others`. A host key, an authorized-keys directory or a passwd file that a third
party could replace is refused, which is the correct behaviour and a real
constraint on where a work directory may live.

**The client still needs a passwd entry.** The local OpenSSH is dynamically linked,
so the preload shim *can* interpose it. Without one, `ssh-keygen` and `ssh` die at
`No user exists for uid 966`. This is the one place a preload is the right tool,
and it is deliberately the client rather than the server.

## The forward path works in both directions

⛔ An earlier measurement reported that the forward path cannot carry the caller's
bytes past the target's first response. That result does not reproduce.

An earlier measurement reported that the forward path delivers the target's first bytes
and **cannot deliver the caller's bytes past that point, for any protocol**. It tested
`example.com:80`, `neverssl.com:80` and `example.com:443` with an HTTP `GET` and got
zero bytes back with a broken pipe. It never drove a raw WebSocket client at `/connect`,
and its failing probes contained no SSH at all.

On 2026-10-22 a raw WebSocket client that is not `dropssh` was driven at the same
endpoint, and the forward path carries both directions.

| probe | result |
| --- | --- |
| `GET /` through `/connect/example.com/80` | 1,010 bytes back in three binary frames, first line `HTTP/1.1 200 OK`, close 1000 `target closed` |
| `GET /` through `/connect/neverssl.com/80` | 493 bytes back, first line `HTTP/1.1 403 Forbidden`, which is the target's answer rather than a transport failure. An earlier probe of the same target got zero bytes, so this row is the direct before-and-after |
| an SSH identification string through `/connect/github.com/22` | the target's 18-byte banner first, then 824 bytes of key-exchange payload came back |

⚠ Two explanations fit and this measurement does not separate them. The relay may have
fixed the path between `2026-10-01-r2` and `2026-10-03-r2`, or the fault may
always have been `dropssh`'s client. The second is the likelier one, because the
missing control is exactly the probe that now passes.

## What the path costs: two numbers measured, the rest quoted

The 64 MiB session cap and the 180-second idle close were documented and unmeasured.
Both are measured here, and both fail rather than shape: the relay closes the socket.

⚠ **Two of the rows below are `measured` and seven are `documented`.** The table
says which for each.

| limit | value | how it was established |
| --- | --- | --- |
| session byte cap | 64 MiB in both directions combined | `measured`: 67,107,029 bytes then close 1009 `session byte cap` at 64.0 MiB, 6.66 s |
| sustained rate to the cap | 9.605 MiB/s | `measured`: the same probe |
| idle close | 180,000 ms of payload inactivity | `measured`: closed at 180.7 s with close 1001 `idle timeout` |
| session life | 720 minutes | `documented`, the specification page |
| forward frame | 262,144 bytes | `documented`, `/health?detail=1` and the specification |
| reverse operator frame | 65,536 bytes of payload after a 32-byte session id | `documented`, the specification |
| admission brake | 120 per minute per address, unauthenticated forward and public `mint` and `pair` only | `documented`, the specification |
| backpressure | 1 MiB queued per receiver, then close 1011 `relay backpressure` | `documented`, the specification |
| node sockets per name | one; a second is refused 409 before accept | `documented`, the specification |

⚠ **`per-object-cap` is the nearest kind and not an exact one.** The relayed unit
is a session rather than an object, and the cap is on the bytes one session carries
in both directions. The vocabulary has no kind for a session byte cap, and the
record says so in `limits_note`.

⭐ The 64 MiB cap is the constraint that decides every use. At the measured
9.605 MiB/s a session reaches the cap in about seven seconds, so the operation a
reader must plan is session replacement rather than bandwidth. One day at 1 TiB is
16,384 sessions, which is one new session every 5.3 seconds for a day.

## The egress address

A caller's traffic leaves through the relay, so the target observes the relay's address
rather than the caller's. Seven colos were probed, each returned a distinct address and
every one of them took the `vpc` road (`measured`, 2026-10-22).

| colo | placement | observed egress | family | total |
| --- | --- | --- | --- | --- |
| `default` | client-nearest | `104.28.196.82` | 6 | 304 ms |
| `eu-central-1` | `aws:eu-central-1` | `104.28.197.9` | 6 | 116 ms |
| `us-central1` | `gcp:us-central1` | `104.28.248.184` | 6 | 130 ms |
| `us-east-1` | `aws:us-east-1` | `104.28.196.79` | 6 | 71 ms |
| `eu-west-3` | `aws:eu-west-3` | `104.28.211.192` | 6 | 127 ms |
| `ap-south-1` | `aws:ap-south-1` | `104.28.200.92` | 6 | 258 ms |
| `azure-westeurope` | `azure:westeurope` | `104.28.219.140` | 6 | 155 ms |

All seven sit inside Cloudflare's `104.28.0.0/16`. Seven colos answered with
seven distinct source addresses on one day. Two probes returned
`104.28.196.82` for both `default` and `us-central1`, which is either a stale
counter or a shared exit, and a spaced re-probe returned `104.28.248.184` for
`us-central1`, so one probe per colo does not settle a per-colo claim.

⭐ **Three of four earlier addresses are unchanged twenty days later**, which is the
one stability claim available.

| placement | 2026-10-02 | 2026-10-22 | same |
| --- | --- | --- | --- |
| `aws:ap-south-1` | `104.28.200.92` | `104.28.200.92` | yes |
| `aws:eu-central-1` | `104.28.197.9` | `104.28.197.9` | yes |
| `aws:us-east-1` | `104.28.196.79` | `104.28.196.79` | yes |
| client-nearest (`default`) | `104.28.204.8` | `104.28.196.82` | no |

The one that differs is the client-nearest placement, and a caller on a different edge
colo is the expected explanation rather than a change at the relay. One probe per colo
cannot show stability over time; two probes twenty days apart on three named placements
show it for those three.

⚠ That is still two points and not a series. It does not cover `?spread=` within one
colo, and it does not show the addresses survive a relay redeploy.

⚠ A different egress address is not a different machine. This is a byte transport
and the compute is wherever the node runs.

## What this path does not establish

- **Not a serving path.** 64 MiB per session and 16,384 sessions a day is the
  arithmetic, and it is not a design a reader should build.
- **Not measured at the 720-minute cap.** No session was held for twelve hours.
  The idle close and the byte cap are both measured; the wall-clock cap is quoted.
- **Not the cause of the earlier forward failure.** The probe that now passes does not
  say which end was broken.
- **Not a throughput benchmark.** One object, one path, one network, one day. The
  9.605 MiB/s is that host's number.
- **Not IPv4 egress.** Every observed address was family 6. `?family=4` was not
  forced.
- **Not the `direct` road.** Every probe took `vpc`, so the road difference is
  unmeasured.
- **Not a price.** The specification says to check Cloudflare Workers, Durable
  Objects and Workers VPC pricing before changing scale assumptions, and publishes
  no figure of its own. The relay cost the caller nothing; what it costs whoever
  operates it is not recorded.

## Chaining

**The sealed-sandbox reach-in.** `dropbear in inetd mode -> an outbound WebSocket to
/v1/node -> a rendezvous that pairs by name -> an ssh client with a ProxyCommand`. The
scarce link is the 72-hour pair life and the fact that both tokens are bearer
credentials.

**The control channel.** `a node that speaks the relay's control protocol -> a
held WebSocket -> an operator that reads and writes raw bytes`. This needs no SSH
and no public port, and it is the shape to use when the payload is a command and
not a session.

Neither chain moves bulk bytes. The 64 MiB cap ends that discussion, and the lanes
that do move a day are in [`bulk-egress.md`](bulk-egress.md).

## What did not work

- **A relay as a serving path**: 64 MiB per session is 0.000006 per cent of a TiB
  in one session, and replacing sessions fast enough is the operation.
- **A forward path assumed broken because one client failed**: the negative result was
  a client result. A raw WebSocket client reached the same targets.
- **Reading the colo pool as a fleet**: 37 entries are 37 placements of one
  service, not 37 machines.
- **Counting a different egress address as capacity**: it changes who the target
  sees and nothing about what the path carries.

Evidence for every row above is in
[`dossier/egress/ajam-ssh-relay.json`](../../../dossier/egress/ajam-ssh-relay.json),
which carries the captures' digests. The captures themselves are probes, not
pages, so they are recorded in that record's `evidence[]` rather than in
`sources/`.
