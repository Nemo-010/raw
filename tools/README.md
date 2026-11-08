# tools

Compiled tools, where a shell script is not fast enough or not portable enough.

This directory is small on purpose. A research repository's bottleneck is
judgement, not throughput, so a tool earns a place here only when a script is
genuinely the wrong shape: something that must hold a socket open across
thousands of concurrent probes, parse gigabytes of captures, or run on a machine
where the interpreter is not present.

## The bar

A tool is accepted when **all** of these hold:

- **A script cannot do it.** If `probe.py` with `--concurrency` is within 2× of
  the compiled version for the job, the script wins, because a reader can fix a
  script.
- **It builds hermetically.** One command, no network at build time beyond the
  dependency fetch, a pinned toolchain, and a `Cargo.lock`/`go.sum` in the tree.
  A tool that needs the operator to install a compiler toolchain by hand is a
  tool that will not be rebuilt in six months.
- **It is not the only way to do the job.** Every tool has a script fallback
  documented in its README, so a session without the toolchain still completes
  the work — more slowly.
- **It has fixtures.** Runs offline against committed inputs, and fails when the
  fixture is broken.

## The bar was tested, and the speed argument failed it

⭐ **Read this before proposing a third tool.** The first row of the table below
("the Python primitive does not scale to a discovery wave") was an assumption
when it was written. It has now been measured, on 2026-10-22, and it is **false**.

`tools/probe-go/README.md` carries the numbers and the method. The conclusion:

| claim | measured |
|---|---|
| a compiled prober is faster per probe | **true**: 0.42 ms vs 1.33 ms per probe at zero latency — **3.2×** |
| that speed matters for a discovery wave | **false**: at 100 ms round trip, 250 hosts, concurrency 8 → **1.1×**; live against 46 real hosts → **1.08×** |
| the 2× bar is met | **only** above ~2,000 hosts at concurrency > 128, which no run in the corpus's spec asks for |

The dominant cost in the Python primitive was never the interpreter: it was
`probe_once()` building a fresh `ssl` context on every request. One shared opener
is a three-line change and closes the gap.

⛔ **So the rule for this directory is now evidence-first: a proposed tool cites a
measured ratio against the script it replaces, in its README, or it is not
built.** A justification that begins "the script will not scale" is a guess until
somebody times it, and the guess was wrong here by an order of magnitude.

## What lives here

| tool | job | why compiled | measured? |
|---|---|---|---|
| [`probe-go/`](probe-go/README.md) | fan-out capability probing — N hosts, C at a time, one JSON record each, challenge and TLS-anomaly classification | a static binary that runs where the interpreter is absent, is testable against committed fixtures, and classifies three shapes `probe.py` misses. **Not speed.** | yes — 1.1× on the named job, 3.2× at zero latency |

### `capture` is not built

`capture` — normalize and deduplicate `sources/` captures by content hash — stays
unbuilt on the same principle. It has no measured job: nobody has timed
`scripts/sources/manifest.py --verify` over the current `sources/` tree and found
it slow, and the tree is small enough that a hash walk is not the bottleneck. When
it is, the measurement comes first and the tool second.

Nothing is added speculatively. A tool arrives when a script has been measured
and found inadequate, and its README records the measurement.

## Layout

```text
tools/
  README.md
  <tool>/
    README.md      what it does, the script it replaces, the measurement that justifies it
    Cargo.toml     or go.mod
    src/
    fixtures/
```

## Rules

- **No network at build time.** Vendored or locked dependencies only.
- **No secrets, ever.** A tool that needs a token takes it from the environment
  and never writes it.
- **`--help` prints an executable example**, not a synopsis. The example must be
  one a reader can paste.
- **Exit codes match `scripts/README.md`.** The two directories are one
  interface.
- **Build output is never committed.** `target/`, `dist/` and binaries are
  ignored; the tool is rebuilt by `make` in its own directory.
