# The client stack

Rung 7: the upstream refuses the *client*, not the address. Buying addresses can
spend a budget on a problem that was never about the address.

**The question:** which client-stack changes let a Cloudflare Worker present a
non-Cloudflare fingerprint, and what do they cost?

**The answer:** a Worker cannot change its TLS ClientHello on `fetch()`, and it can
carry one over `env.EGRESS.connect()`. The tooling to do that is free and
MIT-licensed. **Nothing here needs an address purchase.**

---

## The incident behind this rung

A relay gateway's record, 2026-10-03:

> from 04:42:57Z the vendor refused `oc-free` with `403 FreeTierError` on every
> drawn way, and the decisive bisect put the discriminator at the connection. One
> source, byte-identical bodies, curl (Schannel) 403 against bun 1.4.0 200

⛔ **The address was already acceptable. The fingerprint was not.** Buying addresses
first would have spent the budget and left the block in place.

---

## The instrument: what each transport actually sends

Measured 2026-10-24 through `fetch.web.pkgforge.dev`, reading the `x-web-egress`
header and then fingerprinting against `tls.peet.ws/api/all`.

| transport | `__identity` | JA3 | JA4 | HTTP |
|---|---|---|---|---|
| `cf-fetch` | fixed | `67560f98d68783bd640246df3052c151` | `t13d1312h2_a44d0ee8b3cc_e381dae6da6b` | h2 |
| `cf-fetch` | browser | **the same JA3 and JA4** | — | h2 |
| `cf-fetch` | passthrough | **the same** | — | h2 |
| `cf-fetch` | edge | **the same** | — | h2 |
| `cf-sockets` | fixed | `0bc4716a1605ed6a3d1b981014690b8e` | `t13d1517h1_8daaf6152771_cb7bf5808d99` | **h1** |
| `cf-sockets` | browser | `a488a1ef9b7a37f1db86bf81141b0f5a` | same JA4, **ALPN `h1`** | **h1** |

⛔ **`__identity` changes nothing on `cf-fetch`.** All four values produce one JA3
and one JA4, because the ClientHello is the platform's and a Worker cannot set it.

⭐ **On `cf-sockets` it does change the JA3.** So the socket transport is where a
Worker gets any fingerprint control at all. Its JA4 always ends `h1`, never
`h2`, because the client offers ALPN `http/1.1` alone.

⚠ **Two of four `__egress` pins are set aside.** `cf-sockets` became `cf-vpc`
because the target's name is one `connect()` refuses, and `broker:socks5` became
`cf-fetch` because no proxy was configured. Only `cf-fetch` and `cf-vpc` ran as
named. Read the `x-web-egress` header, not the parameter sent.

---

## The tooling

| project | what it is | licence | Worker-native? |
|---|---|---|---|
| **`tunnelfetch`** | a `fetch`-shaped client with TLS in userland, for `workerd`; routes through HTTP CONNECT, HTTPS or SOCKS5 | **MIT** | ✅ yes |
| `curl-impersonate` (lexiforest) | patches curl to reproduce a browser's ClientHello byte for byte; 48 profiles | free | ❌ a native binary |
| `curl_cffi` | the Python binding for the above | free | ❌ needs Python |
| `utls` | the Go primitive everything else wraps | BSD-3 | ❌ Go |
| `tls-client` | a Go client with the same profiles | free | ❌ Go |

⭐ **`tunnelfetch` is the only Worker-native one**, and its own README caps the
promise:

> **`extensionOrder` arranges extensions; it cannot add them.** … Chromium sends
> five that it does not: `signed_certificate_compression` 27, `session_ticket` 35,
> `application_settings` 17613, `encrypted_client_hello` 65037 … So `profiles.chrome`
> presents a Chromium cipher list, group list and GREASE placement over an extension
> **set** that is curl's. A test reads that gap straight out of the committed
> Chromium capture and fails if it changes … but it is a real difference and a
> JA3/JA4 hash sees it.

⛔ **So `profiles.chrome` is not Chrome to a JA3 hash.** It is closer than the
platform's, and that is all it claims.

⚠ **Its own HTTP/2 result did not replicate.** The README records
`stackoverflow.com --http1.1 -> 403` and `--http2 -> 200`, then says: *"Re-measured
the same day this landed, from the same proxies, that site now challenges HTTP/2 as
well … Bot detection is adversarial and moves; a protocol is a window, not a
property."* Across its ten-site sample, HTTP/2 changed the outcome on **one** site.

⚠ **And it costs CPU.** TLS in userland is about 10 ms of CPU against about 0.9 ms
on an open connection, and h2 costs *more* than h1 on this runtime. At 599,000
requests a month a handshake per request is the dominant cost, so the client must
pool, which is what its `Client` does.

---

## The headers, which are a separate identity channel

| header | on `cf-fetch` | on `cf-sockets` / `cf-vpc` | removable? |
|---|---|---|---|
| `Cf-Worker` | the deployment's zone | absent | **only by leaving `cf-fetch`** |
| `Cf-Ray` | present, names the colo | absent | same |
| `Cdn-Loop` | present | absent | same |
| `Cf-Visitor` | present | absent | same |
| `Cf-Ew-Via` | present | absent | same |
| `X-Forwarded-For` | the caller's chain plus Cloudflare's | written by the transport | not on `cf-fetch` |

⛔ **A caller cannot overwrite them.** Measured: with `__strip-platform-headers=false`
**and** a caller-supplied `cf-worker: my-own-zone.example`, the origin received
`cf-worker: pkgforge.dev`. The value was overwritten, not appended.

⭐ **So the `fetch()` road carries a constant identity that no address rotation
changes**, and the socket and VPC roads carry none of it. That is a stronger reason
to prefer VPC than the address difference is.

⚠ **A relay on a second Cloudflare zone changes `Cf-Worker` and nothing else.**
Measured twice: AS14789 on both zones, 6 runs, 3 hosts.

---

## Where rung 7 splits

⭐ **There are two different things called "a block", and only one is spoofable.**

| the gate | spoofable by a ClientHello? | why |
|---|---|---|
| a **vendor's own gate** that reads the hello | ✅ yes | it is a string comparison |
| a **Cloudflare challenge** that runs JavaScript | ❌ no | a spoofed hello is not a JS-capable client |

⚠ **Measured:** `nowsecure.nl` returned a Turnstile challenge body through both
transports on 2026-10-24 (`cf-fetch` 178,528 bytes, `cf-sockets` 77,498 bytes, both
containing `turnstile` and `challenge`). A better ClientHello does not pass a
challenge that needs an interpreter.

## What is not measured

⛔ **Which ClientHello fields the OC-Free gate actually reads.** The gateway record
says so: *"Not measured: which ClientHello fields the vendor reads, and how
the profile varies by host or CLI build."* Settling it needs a bisect that varies
one field at a time. Vary GREASE on or off, extension order, ALPN `h1` versus
`h2`, and the cipher list, against the same body in one window, with a control
that the window is open.

⭐ **QUIC is not reachable through `connect()`**, which is TCP-only, so an HTTP/3
fingerprint cannot be presented from the runtime's socket. It can be done in wasm:
`quinn-proto` plus `rustls` compiled to `wasm32-unknown-unknown` carries QUIC over a
TCP stream, measured in a VPN client dashboard. That is the only route to an h3
fingerprint from a Worker, and it costs a wasm payload plus a far-side converter.
