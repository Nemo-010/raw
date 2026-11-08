# The 100 MB body cap is not a tunnel limit, and a 400 MiB body traversed a Quick Tunnel

- **When:** 2026-10-22T03:31:53Z
- **Status:** corrected
- **Supersedes:** `.tmp/work/recon-extras/EGRESS.md` section 3, the Cloudflare Tunnel and Quick
  Tunnel rows, and section 4 item 2
- **Superseded by:** `docs/egress/free/expose-a-local-port.md` section Cloudflare Quick Tunnel,
  and `dossier/egress/cloudflare-quick-tunnel.json`
- **Evidence:** a live Quick Tunnel probe on 2026-10-22, and
  `developers.cloudflare.com/workers/platform/limits/` (read 2026-10-22)
- **Confidence:** measured

## What we believed

The census named `per-object-cap`: 100 MB proxied request body as the binding constraint on
Cloudflare Tunnel, and cited `developers.cloudflare.com/cloudflare-one/account-limits/` for it.
It repeated the figure as the second of six constraints that "actually decide the egress lane".

## What we found

Two separate defects.

**The citation is wrong.** The account-limits page lists tunnels, routes, replicas, virtual
networks and certificates, and contains no request-body figure at all. The 100 MB figure lives on
the Workers limits page and applies to a request through the Cloudflare proxy on a zone plan, with
100 MB for Free and Pro, 200 MB for Business and up to 5 GB for Enterprise.

**The limit does not apply to a Quick Tunnel.** A `trycloudflare.com` hostname is not a zone on any
plan, and there is no proxy in the path that applies the zone's body cap. Measured: a 419,430,400
byte POST to a local sink through a live Quick Tunnel returned 200, the sink reported
`got=419430400`, and the SHA-256 matched the source file
(`d491a95debb39be6132754555606b04a4e16cd40b1f3e065903cea307d3a1839`, 77.1 s). A 150 MiB body and a
50 MiB body also passed.

The 100 MB figure is real for a named tunnel behind a proxied zone, and it belongs in that
record's `limits[]`. It was in the wrong record.

## How we found it

The rule is to probe the path rather than read about it. A local hashing upload sink and
`cloudflared tunnel --url` cost about two minutes, and the first 150 MiB POST that came back
byte-identical falsified the census row outright.

Three explanations were considered before the test. One, the cap is real and enforced: refuted by
the 400 MiB body. Two, the cap is real but the tunnel route does not meet it: consistent with
the reading of the Workers page. Three, the cap is not enforced on any proxied request: not
tested, because it needs a named tunnel on a zone this session did not have.

## What it cost us

Nothing yet. The cost would have been a design: a reader planning against a 100 MB object ceiling
shards a corpus into 100 MB pieces and pays for a CDN it does not need. The real ceiling on a Quick
Tunnel is the hostname's lifetime, and the real throughput ceiling is 6.27 MiB/s single-stream
falling to 3.79 MiB/s under 32-way concurrency with 522s.

## What a future session should do differently

**A cap has a scope, and the scope is part of the claim.** "100 MB" with no subject is the same
defect as "1 TB free" with no constraint. Record which layer enforces a limit before recording the
limit, and when a census cites a page, open that page and search it for the number.
