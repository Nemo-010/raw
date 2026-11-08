# Self-hosted ingress is not a free service

- **When:** 2026-10-23T00:32:18Z
- **Status:** corrected
- **Supersedes:** `dossier/egress/frp.json` `verdict: qualifies`; `headscale.json` and `zrok-selfhost.json` `verdict: qualifies-with-caveat`; `pangolin.json`, `wiredoor.json` and `wireport.json` `verdict: qualifies-with-caveat`; and the rows in `docs/egress/free/expose-a-local-port.md` and `docs/egress/free/signalling.md` that rendered them as free tunnels
- **Superseded by:** the same six records at `verdict: paid-only` with `binding: volume-quota` and `extras.hosting_requirement`, and the document rows that now name the host as the provider
- **Evidence:** each record's own fields: `free_tier.unit` is `none` or `unlimited`, `chaining` says it composes only with a server that is paid for, and `frp`'s `reliability_note` says every "free frp server" lead was a VPS advertisement; read 2026-10-22 and 2026-10-23
- **Confidence:** measured

## What we believed

That software which forwards a port was a free tunnel. Six records carried a
qualifying verdict for `frp`, `headscale`, `zrok-selfhost`, `pangolin`,
`wiredoor` and `wireport`, and a reader who stopped at a table took them for
services anybody can use.

## What took the old claim away

The records contradicted their own verdicts. The free tier is the software, and every
one of these paths needs a host with a public address; the software supplies no
host. `frp`'s 42.91 MiB/s probe measured the software on one host, so it
establishes that frp works and not that somebody offers it.

The operator's rule for this session states the precedence: a hosted service
first, a rented or free compute service second, and self-hosted software only on
that compute service.

## What the records say now

- `verdict`: `paid-only`, because none was ever a free service.
- `binding`: `volume-quota`, because the host's monthly egress allowance is what
  runs out first.
- `extras.hosting_requirement`: a rented or free compute service.

Every probe, digest and throughput figure is untouched. Nothing measured was
withdrawn.

## What would reopen one

A hosted control plane that publishes a quota, issues a `.conf` and does not
require a server to be run. That would be a provider, and it would get its
own record. `NetBird` and `Nekotopia` are the two records that already meet that
description, and both carry the caveat their own pages state.
