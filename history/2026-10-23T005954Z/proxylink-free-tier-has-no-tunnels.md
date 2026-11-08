# The adversarial re-read found a free tier with no tunnels

- **When:** 2026-10-23T00:59:54Z
- **Status:** corrected
- **Supersedes:** `dossier/egress/proxylink-dev.json` `verdict: qualifies-with-caveat` and the `binding_note` sentence "no port count is published"; `dossier/egress/openport-pw.json` `free_tier.unit: requests` and `metered_on: request-count`; and the ProxyLink rows in `docs/egress/README.md` and `docs/egress/free/wireguard-ingress.md`
- **Superseded by:** the same records, with ProxyLink at `trial-only` and its `limits_note` carrying the plan grid, and `openport-pw` at `unit: none` with `metered_on: unstated`
- **Evidence:** `proxylink.dev/pricing` read 2026-10-23: Free is "3 proxy links (HTTP/HTTPS only)", "No tunnels"; Developer is "EUR 17 / month" with "5 tunnels"; the FAQ says "TCP links, browser SSH/RDP/VNC, and LAN access all require a tunnel (Developer plan or above)". `openport.pw` read 2026-10-23 states no request count anywhere on the page
- **Confidence:** documented

## What we believed

That ProxyLink's early-access offer was a free path with TCP and UDP, and that
openport.pw metered requests.

## What took the old claim away

A verifier that did not write these records opened `proxylink.dev/pricing`, which
the original pass never read, and found the same vendor publishing a free plan
with zero tunnels and TCP behind EUR 17 a month. The early-access sentence is
still true today, which is why the old verdict was not false; it was incomplete in
the one direction that decides what a reader builds.

For openport.pw, no page states a request count. The unit asserted a meter the
vendor does not publish, and it contradicted the record's own `limits[]`.

## What the records say now

- ProxyLink: `trial-only`, with the grid in `limits_note` and the pricing page in
  `evidence`. Nothing measured was withdrawn.
- openport.pw: `unit: none`, `metered_on: unstated`, and the offer restated as one
  permanent port with no published limit.

## What this says about the pass

Eight of the ten records held exactly as written. The verifier also recorded two
extraction traps that look like page changes: the broker's text extractor drops
Oracle's "10 TB per month" sentence and portmap.io's "unlimited" support-page
sentence, and both are present in the raw HTML. A future pass that reads only the
extractor will report both missing. That note is in
`.tmp/egress/verify-top/review.md`, which is scratch and not committed.
