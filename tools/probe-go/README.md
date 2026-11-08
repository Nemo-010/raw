# probe-go

Mass capability probing: one URL in, one JSON evidence record out, never trusting
HTTP 200. It is the compiled form of `scripts/probe/probe.py`'s single-probe
primitive, and its job is the fan-out `probe.py` cannot do: N distinct hosts, C at
a time, one record each.

**Read §The measurement first.** The measurement does not support the claim that
was made for this tool, and the honest conclusion is narrower than the plan. The
tool is here because it is correct, offline-testable and faster on a worklist that
is *readable* rather than because it is 20× faster on a discovery wave — it is not.

## What it does

```text
probe-go --urls-file hosts.txt --concurrency 8 --timeout 10
```

- Reads one URL per line, `#` comments allowed.
- Runs up to `--concurrency` hosts in flight. Unlike `probe.py --concurrency`, it
  does **not** stop at the first C URLs: every line is probed.
- Emits one JSON record per host on stdout, in input order.
- Writes a summary of what it could **not** evaluate to stderr.
- Exits `1` when any host was not evaluable, `0` when all were.

The record has `probe.py`'s keys, names and JSON types, so a reader or
`render.py` cannot tell the two apart except by `probe_version` and `tool`.

## The measurement that decides whether this tool should exist

`tools/README.md` says a tool is accepted only when "a script cannot do it", with
the bar at **2×**. That is a claim, so it was measured rather than assumed.

### The problem with the obvious measurement

The obvious benchmark — time `probe.py` against 46 live hosts, then time this
binary on the same 46 — is **not a measurement of the tool**. Both spend almost
all their wall clock waiting for the network. On this machine the 46 hosts had a
median round trip of **465 ms** and one host took 15 s to time out. A faster
prober cannot make a network faster, so that benchmark measures the internet.

It was run anyway, because a negative result is a deliverable. Hosts: `example.*`,
`iana.org`, `httpbin.org`, `jsonplaceholder`, `pypi`, `crates.io`,
`proxy.golang.org`, `cdn.jsdelivr.net`, `raw.githubusercontent.com`, two Debian and
Ubuntu mirrors, eight vendor sites, and five public AList instances that already
answered in the corpus's own sweep (`al.chirmyram.com`, `zhuifan.link`,
`lz.qaiu.top`, `189.qaiu.top`, `demo.cloudreve.org`). One GET per host per arm, no
host probed more than four times in total. Nothing was scanned.

### What the four script forms cost

`probe.py` has no fan-out mode, so "the script" is ambiguous, and the ratio depends
entirely on which form you pick. All four were built and timed, because the bar is
about what *a reader* can do:

| form | what it is | 250 hosts, 100 ms RTT, conc 8 |
|---|---|---|
| `naive.py` | one `probe.py` process per host | 41 s |
| `fallback.py` | N/C `probe.py` processes, chunks of C | 42 s |
| `driver.py` | **one** process, imports `probe_once`, C threads | 22 s |
| `driver_cached.py` | `driver.py` plus one shared `ssl` opener | **3.75 s** |

The last row is the honest competitor, and finding it changed the verdict. The
first three are slow for a reason that is **not** Python's runtime: `probe_once`
calls `_build_opener()` on every request, which calls
`ssl.create_default_context()` and parses the whole CA bundle *in Python*, under
the GIL. Reusing one opener is a three-line change. The bar says "a reader can fix
a script", and a reader can fix this one.

### The numbers

Same 250 hosts, concurrency 8, both arms run alternately so a slow machine window
penalises both, with a warm-up round so the newly built binary is not charged for
page-cache misses. Reproduce with:

```console
$ cd tools/probe-go && make build
$ python bench/compare.py --modeled --hosts 250 --concurrency 8 --rtt 0.10 --rounds 3
$ python bench/compare.py --live bench/hosts.txt --concurrency 8 --timeout 15 --rounds 4
```

| modelled RTT | `probe-go` | script (`bench/script-fallback.py`) | ratio |
|---|---|---|---|
| 5 ms | 0.43 s | 1.20 s | **2.8×** |
| 50 ms | 1.86 s | 2.29 s | **1.2×** |
| 100 ms (the spec's own workload) | 3.5–3.9 s | 4.1–5.2 s | **1.1–1.3×** |

At 2000 hosts and concurrency 256 the ratio reaches **2.0×**, and that is the only
regime where it does.

**Live internet, 46 real hosts:** 16.8 s vs 18.2 s, ratio **1.08×**. Excluding the
one host that burned a 15 s timeout on both arms: **1.89×**, and that number is
noise on 45 samples, not a property of the tool.

⚠ **A measurement trap worth recording.** The first version of this benchmark
pointed both arms at a closed port to remove the network and compare raw cost. It
produced a nonsensical 200–450× in the script's disfavour, and the cause was not
Python: on Windows a TCP connect to a closed local port takes **2050 ms** before
returning `ECONNREFUSED`, and a bare `socket.create_connection` pays it just as a
prober does. The instrument was measuring the kernel's SYN retry. That script was
deleted rather than published. A benchmark that has not been sanity-checked
against the platform underneath it is as likely to be wrong as the claim it was
built to test.

### The verdict

**The bar is not met for the job the plan named.** The justification was "the
Python primitive does not scale to a discovery wave". The Python primitive, once
its opener is reused, scales fine: it is within 10% of a compiled binary at the
latencies real hosts have, and within a factor of two even at zero latency.

The repair is a three-line change to `probe.py`, not a compiler. **The right
follow-up is to cache the opener inside `probe.py` itself**, which would make the
script 6× faster than it is today and make this tool's remaining advantage
approximately nothing. That is recorded here rather than done, because
`scripts/probe/probe.py` is owned by another session and changing its concurrency
behaviour mid-wave would move the evidence under a running measurement.

So why does this directory exist at all? Three reasons that survived the
measurement, none of which is speed:

1. **It can be tested offline, and provably fails when broken.** `probe.py`'s
   `--selftest` runs a loopback server but has no committed fixtures and no way to
   be shown a broken one. This tool's `--selftest` runs 66 cases against
   `fixtures/` and each fixture case exits `1` when the fixture is corrupted.
   §Verifying that, below, is the point.
2. **It classifies three shapes `probe.py` misses** (§What it does that `probe.py`
   does not).
3. **A single static binary runs where the interpreter is absent**, which the bar
   names as a legitimate reason on its own.

If the operator judges speed to be the only reason a tool may exist here, the
honest action is `rm -rf tools/probe-go` and the three-line `probe.py` patch. This
README exists so that decision can be made from numbers.

## What it does that `probe.py` does not

`probe.py` is correct and this tool follows it. These are additions, not
corrections:

| shape | why | where |
|---|---|---|
| `undeclared-gzip` | §5.1: a `200` whose first two bytes are `1f8b` is a gzip body with no `content-encoding`. Fires only on a textual content type, because a `.crate` or `.tgz` is legitimately gzip — that inverse error was caught live on `static.crates.io` and fixed. | `detect.go` |
| `range-mismatch` | Rule 13: a `206` can name a range it does not deliver. `probe.py` records `honoured: true` from the status alone; this compares `Content-Range` to the request. | `detect.go` |
| `length-mismatch` | A body **longer** than `Content-Length`. `probe.py` catches the short case as `truncated-body`; over-delivery was unclassified. | `detect.go` |
| `js-cookie-gate` | The `200` with `<title>Loading...</title>` and a `location.replace()` carrying a JWT in `ch=`/`js=`, measured on `alist.advanced360.top` and specified in `auto-discovery.md`. `probe.py` does not detect it; `probe-alist.sh` does. | `detect.go` |
| `zh-cn-interstitial` | `人机验证`, `请稍候`, `安全验证` and three more. This population is Chinese-language and `auto-discovery.md` names the first as a required needle. | `detect.go` |
| `integrity` field | One string that separates `bytes:<sha>`, `challenge`, `no-payload:<kind>`, `tls-broken`, `unreachable`, `refused`, `unverified`. A summary can count "answered" and "verifiable" as different numbers. | `fetch.go` |

## TLS broken is not host broken

The distinction is enforced and was verified live against
`https://expired.badssl.com/`, whose certificate expired in 2015:

```console
$ probe-go https://expired.badssl.com/ --tls-info
  error       tls_untrusted
  integrity   tls-broken
  usable      False
  tls         {'handshake_ok': True, 'tls_version': 'TLSv1.2',
               'cert_der_sha256': 'ba105ce0…', 'verified': False,
               'peer_not_after': '2015-04-12T23:59:59Z'}

$ probe-go https://expired.badssl.com/ --insecure
  status      200  bytes 494  usable True
```

`handshake_ok: true` with `error: tls_untrusted` is the whole point: the host is
alive and the chain is broken, which is a finding about the chain. A record with
`handshake_ok: false` is a host that did not answer.

## Build

There is **no dependency to fetch**. The prober uses only the Go standard library:
`net/http`, `crypto/tls`, `crypto/x509`, `crypto/sha256`, `encoding/json`. That is
why there is no `go.sum` — a module with no requirements has no sums to record.
It builds on a machine with Go installed and no network:

```console
$ cd tools/probe-go && GOPROXY=off make build
go build -trimpath -ldflags="-s -w" -o dist/probe-go.exe ./src/
built dist/probe-go.exe
size: 8099328 bytes
```

- **Clean build: 2.8–14.4 s** across six runs with `rm -rf dist` between each. The
  spread is this machine's scheduler, not the build: the same source produced both
  ends. Expect the low end on an idle machine.
- **Binary: 8,099,328 bytes** (7.7 MiB), static, `-trimpath -ldflags="-s -w"`.
- Toolchain: Go 1.27, recorded in `go.mod` as `go 1.27`.

Go was chosen over Rust and C because the job is stdlib HTTP and TLS, and Go's
`net/http`, `crypto/tls` and `crypto/x509` give the record every field it needs
with no crate to justify, no vendor directory and no `Cargo.lock` to keep in sync.
Rust would need `rustls` or `native-tls` plus a `Cargo.lock` for the same result;
C would mean vendoring an HTTP client. The one-line justification the bar asks for
each dependency is: **there are none.**

## Test

```console
$ make test          # go vet + selftest
go vet ./src/
./dist/probe-go.exe --selftest
selftest: 66 passed, 0 failed, 66 total
test: ok
```

`--selftest` runs **entirely offline**: a loopback HTTP server, a loopback TLS
server with a self-signed certificate generated in memory (never committed — a
committed private key is a secret in the tree), and the committed `fixtures/`.
No outside network is touched.

## The fallback: the same job with `probe.py`

Every tool here must be replaceable by a script. This is the worked equivalent,
and it is the version that was measured above:

```python
# fallback.py — one process, C threads, the same one-record-per-host output.
import importlib.util, json, sys
from concurrent.futures import ThreadPoolExecutor

spec = importlib.util.spec_from_file_location("probe", "scripts/probe/probe.py")
probe = importlib.util.module_from_spec(spec); spec.loader.exec_module(probe)

args = probe.build_parser().parse_args(["--timeout", "15"])
args.method = "GET"                       # probe.main() derives this after parse

# THE LINE THAT MATTERS. probe_once() builds a fresh opener -- and a fresh
# ssl.create_default_context(), which parses the whole CA bundle -- on every
# call. Under threads that work serialises on the GIL and concurrency buys
# nothing. One shared opener is safe for independent requests and is the
# difference between 20 s and 2.2 s for 250 hosts.
shared = probe._build_opener(args)
probe._build_opener = lambda _args: shared

def one(u):
    return probe.probe_once(u, args)       # one record, exactly as probe.py makes one

urls = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
with ThreadPoolExecutor(max_workers=8) as ex:
    for rec in ex.map(one, urls):
        print(json.dumps(rec))
```

That driver — with the shared opener — took **2.24 s** for 250 hosts at 100 ms RTT
against this binary's **2.02 s** on the same run. **Without** the shared opener the
same driver takes **20.0 s**, which is the whole gap between "the script is
adequate" and "the script is not".

**What the fallback does not give you:** the four extra classifications above, the
`integrity` field, and `fixtures/`-backed offline testing. It gives the same
records for the shapes `probe.py` already handles, which is most of them.

For a single host, no fallback is needed at all — `probe.py` is the primitive:

```console
$ python scripts/probe/probe.py https://example.com/ --tls-info
```

## Verifying that the selftest actually fails

A `--selftest` that cannot fail is not a test. Every fixture case exits `1` when
its fixture is corrupted, and that was proven in both directions:

```console
# direction 1: clean tree passes
$ ./dist/probe-go.exe --selftest ; echo "exit=$?"
selftest: 66 passed, 0 failed, 66 total
exit=0

# direction 2a: a byte in the empty-200 fixture
$ printf 'x' > fixtures/empty-200.txt && ./dist/probe-go.exe --selftest ; echo "exit=$?"
FAIL classify empty-200.txt -> empty  got kind=(none) sig=
selftest: 65 passed, 1 failed, 66 total
exit=1

# direction 2b: de-gzip the undeclared-gzip fixture
$ printf '<html><body>plain</body></html>' > fixtures/undeclared-gzip.dat
FAIL classify undeclared-gzip.dat -> undeclared-gzip  got kind=tiny-html sig=200 with a 31-byte HTML body
exit=1

# direction 2c: strip the challenge marker out of the cloudflare fixture
$ printf '<html><head><title>A normal page</title></head><body>hi</body></html>' \
    > fixtures/challenge-cloudflare.html
FAIL challenge challenge-cloudflare.html  detected=false sig=
exit=1

# direction 2d: delete a fixture
$ rm fixtures/json-error-200.json
FAIL fixture present: json-error-200.json  0 bytes, err=open ...: cannot find the file
exit=1
```

The false-positive direction is tested too: `clean-body.html`, `clean-body.json`
and `archive-declared-gzip.dat` must **not** be classified as anything, and the
`js-cookie-gate` case must not fire on an ordinary page.

## Exit codes

`scripts/README.md`'s map, verified by running each:

| code | meaning | verified with |
|---|---|---|
| 0 | all hosts usable | `probe-go https://example.com/` |
| 1 | a host was not usable (also: some hosts in a sweep were not) | `probe-go https://example.com/nothing-here-xyz` |
| 2 | usage error | no args; `ftp://…`; `--concurrency 0`; missing `--urls-file` |
| 3 | internal: nothing could be produced | encode/write failure |
| 4 | the remote said no, retryably | `https://httpbin.org/status/503`, `…/429` |

## Saying what it could not do

A sweep of 46 hosts where 6 could not be evaluated reports both numbers, on stderr,
in one line:

```console
$ probe-go --urls-file hosts.txt --concurrency 8 --timeout 10
probe-go: 46 probed, 40 usable, 6 NOT evaluable (unreachable 1 of which tls-broken 0, challenge 0, false-200 1, retryable 0) in 12.57s
```

`usable` and `NOT evaluable` are separate counts by construction, because
`scripts/README.md` rule 9 says a check that examined zero rows must not report
success.

## A write probe is not implemented, and this is where it goes

The task brief says a write probe must hash, because a byte-identical readback is
the only proof a write worked. **There is no write probe here**, and saying so is
required rather than optional.

The reason is that a write prober is not a variant of this program. It is a
protocol-specific state machine per service — `probe-alist.sh` already implements
the AList one in 385 lines: the zero-byte permission oracle, the `PUT`, the 2-second
wait, the read-back, the `sha256` compare, and the `{"code":403}` inside an HTTP
`200`. It costs 6 requests per host and it *leaves a file on a volunteer's disk
forever*, because delete is denied on the one writable host the corpus found.

A generic `--write` flag would be wrong in the way this repository cares about
most: it would report "write: succeeded" for a host that accepted a `PUT` and
refused the read-back, which is the dominant failure in `docs/netdisk-pan/` and the
exact shape that cost a wave. Folded into a fan-out prober it would also leave a
permanent file on every writable host it reached.

When it is built it belongs in `scripts/discover/`, driven by this tool for stage 3
and stopping at stage 3's boundary, and it must carry `readback_sha256` and
`written_sha256` as two fields that are compared rather than one `write: true`.

## Layout

```text
tools/probe-go/
  README.md       this file: the measurement, the verdict, the fallback
  Makefile        build, test, selftest, vet, bench, clean
  go.mod          module + toolchain; no dependencies, so no go.sum
  src/
    main.go       CLI, fan-out scheduler, summary accounting, exit codes
    fetch.go      one URL -> one record; redirects, TLS split, byte verdict
    detect.go     challenge and false-200 classification
    record.go     the JSON record, key-for-key with probe.py's
    selftest.go   66 offline cases; loopback HTTP and TLS servers
    tlsfixture.go a self-signed cert generated in memory, never committed
    util.go       small parsing wrappers
  fixtures/       offline inputs, 16 files, one per shape
  dist/           build output; gitignored, never committed
```

## What this tool is not

- **Not a scanner.** It probes URLs you give it. No ranges, no port scans.
- **No pacing of its own.** `--concurrency` sets how many hosts are in flight; set it to what the measurement
  needs (AGENTS.md section 2 rule 15). A retry of a transport error, or of a 408, 429 or 5xx, starts at once;
  the server's own `Retry-After`, whatever its size, is the only pause. There is no per-host delay.
- **Not a benchmark.** `probe.py --shard-bytes` does parallel ranged GETs with a
  baseline, which is the corpus's throughput measurement; do not reimplement it.
- **Not the only way.** See §The fallback.

## The measurement, in one paragraph, for the next session

`probe.py` with a cached opener is within 10% of this binary on real hosts and
within a factor of two at zero latency; the 2× bar is met only above ~2000 hosts
at concurrency above 128. The tool's remaining justification is offline fixtures,
four extra classifications and a static binary — not speed. **If speed was the
only reason, patch `probe.py` to reuse one opener and delete this directory**;
the measurement above says that patch is worth more than the compiler.
