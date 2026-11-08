# netdisk-pan: the expansion plan

`docs/netdisk-pan/auto-discovery.md` contains the full specification for the
monthly loop: inputs ranked by measured yield, the four stages, the verification
gate, the dedupe key, the state store, the schedule, the alert, the retirement
rule, and the failure modes with evidence.

This plan does not restate it. It says what is left to build, what is unproven,
and what to do first.

**Read [`../netdisk-pan/auto-discovery.md`](../netdisk-pan/auto-discovery.md)
before this file.** This plan assumes it.

## What is already established

The population, measured on 2026-10-22:

| measurement | value | what it decides |
|---|---|---|
| hosts probed | 169 | the sample |
| answered as an AList/OpenList API | 33 | the addressable set |
| exposed a mount list | 30 | the useful set |
| advertised `write: true` | 14 | the set that lies |
| **accepted a verified write** | **1** | the real set |
| 2024 cohort still listing after 2.75 years | 7.6% | the rot rate |
| fitted half-life | **8.9 months** (9.0 on the earliest revision) | the cadence |

The mechanism, which matters more than the numbers: **`write` is `CanWrite`, a
negation, and it is not the gate.** The real gate is `CanWriteContent(bit 3) || a
per-path meta rule`. A host can advertise `write: false` and still accept a write,
and one can advertise `write: true` and refuse with a 403 inside an HTTP 200. That
is why the count of flagged hosts is worthless and the count of verified writes is
everything.

## What is left to build

| # | item | why it is not done | cost |
|---|---|---|---|
| 1 | `scripts/discover/netdisk-sweep.py` | not built. The logic exists as `scripts/discover/probe-alist.sh`; it has no scheduler, no state store, no alert. A tools change in a pull request of its own (issue #37) | one session |
| 2 | the state store | records hold `extras.observations[]`, but nothing writes the walk yet | with #1 |
| 3 | the two unverified channels | certificate transparency and `gh search code` for compose files — **never run** | two hours |
| 4 | 70 deferred providers | deferred by the storage research; a reconciliation is filling them | in progress |
| 5 | `pans/korea-japan.md` and `pans/western.md` | several `not established` rows: TeraBox serves a verification interstitial, PikPak serves pricing as binary | a session with a browser |
| 6 | direct-link extraction, measured | the document describes the mechanism; only a handful of resolvers were probed | a session |

## The one thing to do first

**Run the two unverified channels once, by hand, and record what they return.**
They are in the spec's input table marked `unverified`, and a loop built on them
would be built on a guess. Specifically:

```bash
# certificate transparency: does it find instances the index pages miss?
curl -qfsS "https://crt.sh/?q=%25.alist.%25&output=json"

# GitHub code search for the API path
gh search code '"/api/public/settings"' --limit 1000
```

For each: how many hostnames, how many were already known, how many were new, and
how many of the new ones pass the verification gate. If the yield is zero, delete
the row from the spec's table rather than leaving a channel that was never proven.
**A discovery channel with no measured yield is a liability**: it will be wired
into the loop, and the loop will find nothing.

## The verification gate, restated because it is the whole topic

A host is a candidate when `/api/public/settings` answers with a recognisable
AList/OpenList shape. It is *useful* when a mount list comes back. It is
*writable* only when all of these hold:

1. A `PUT` returns a body whose `code` is not a permission failure. The three
   shapes, from the corpus's own probes:
   - `{"code":403,"message":"file exists"}` from a zero-byte oracle at an existing
     directory with `Overwrite:false` means **the permission passed**.
   - `{"code":403,"message":"permission denied"}` **inside an HTTP 200** is the
     dominant lie — 12 of 13 flag-advertising hosts.
   - `{"code":200,"message":"success"}` followed by `GET` returning
     `{"code":401,"message":"expire missing"}` means the write landed and the
     bytes **cannot come out**.
2. A `GET` of the same bytes returns a matching SHA-256.
3. The bytes are the ones written, not a re-encode.

⛔ **No record is `measured` writable without a byte-identical readback.** That is
rule 1 and rule 3 of the methodology.

## Cadence, and what changes it

Monthly, because the measured turnover is 7.4% and the half-life is 8.9 months.
The alert is only for one event: a host whose `write_capability` becomes
`verified`. One host has done so.

**What would change the cadence:** if three consecutive monthly runs find no new
hosts, the index sources have gone stale rather than the population having
stabilised — the index is the bottleneck, not the market. Check the inputs before
lengthening the schedule.

## The trap that must not be repeated

`t.me/s/alistshare` has a yield of **zero**: the channel posts tools and pins a
notice about excess use. A loop that kept reading it would report "no new
instances" forever and look healthy.

⚠ **Every input in the table needs a measured yield, a rot rate, and a
false-positive rate. An input without them is a guess wearing a table row.**
