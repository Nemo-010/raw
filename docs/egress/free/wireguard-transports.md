# Carrying a WireGuard datagram over a transport that is not UDP

WireGuard is UDP only. The kernel module, `wireguard-go` and BoringTun all send
and receive datagrams and nothing else. So a tunnel that forwards TCP or a
WebSocket cannot carry WireGuard unless something converts the datagram at one
end and converts it back at the other.

⭐ **That conversion needs a host at each end, and the host is the finding.** A
TCP-only hosted tunnel is therefore not a free WireGuard ingress provider on its
own. It becomes one only when the reader supplies a machine to terminate the wrapper, and
then the machine is the provider that matters.

The tools below are the converters. They are recorded as tools and not as
services: none of them gives a reader an address, a quota or an identity.

| tool | direction | needs at each end | maintained | what it unlocks |
| --- | --- | --- | --- | --- |
| `wgcf` (self-hosted) | registration | nothing; a CLI writes `wgcf-profile.conf` | yes | Cloudflare WARP as a standard `.conf` |
| `warp-plus` (self-hosted) | client | a device | yes | WARP over SOCKS5 or a TUN |
| `usque` (self-hosted) | MASQUE client | a device | yes | WARP over MASQUE, not WireGuard |
| `wstunnel` (self-hosted) | UDP to WebSocket | a host at each end | yes | any WebSocket-only edge |
| `udp2raw` (self-hosted) | UDP to fake TCP | root or `CAP_NET_RAW` at each end | yes | a path that drops UDP |
| `wireguard-proxy` (self-hosted) | UDP to TCP | userspace at each end | yes | a TCP-only relay |
| `wg-tcp-tunnel` (self-hosted) | UDP to TCP | a host at each end | yes | a TCP-only relay |
| `wireguard-over-wss` (self-hosted) | UDP to WSS | a host and a TLS terminator | recipe | a TLS-only edge |
| `tunelo` (self-hosted) | UDP to TCP | a host at each end | yes | a minimal TCP relay |
| `wormhole-vpn` (self-hosted) | UDP to WebSocket | a host plus a paid Workers plan | yes | a Worker as a hop |
| `gluetun` (self-hosted) | client | a device | yes | an egress VPN inside a container |
| `wireguard-go`, `boringtun` (self-hosted) | userspace implementation | a device | yes | WireGuard where the kernel module is absent |

## The registration tools

`wgcf` registers with Cloudflare's client API and writes a standard
`wgcf-profile.conf` (`documented`, read 2026-10-23). That is the clearest proof
that a commercial VPN can be reduced to a `.conf`, and it is why "no official
WireGuard config" is not the same as "no WireGuard".

⛔ **A `.conf` is transport and never ingress.** A WARP profile gives a device a
new exit address; it does not give a server an inbound one. The record for
Cloudflare WARP says the same and stays `qualifies-with-caveat` on that basis.

`usque` is worth naming for the opposite reason: it reimplements the WARP client
over MASQUE rather than WireGuard, so a `.conf` cannot reproduce it. `warp-plus`
consumes a profile and exposes SOCKS5 or a TUN, which is a client and not an
extractor.

## The converters

`wstunnel` carries UDP and TCP over WebSocket and ships a documented WireGuard
recipe. `udp2raw` disguises UDP as TCP and needs `CAP_NET_RAW` at both ends.
`wireguard-proxy`, `wg-tcp-tunnel` and `tunelo` are small userspace relays that
put a WireGuard datagram inside a TCP stream. `wireguard-over-wss` is a recipe
rather than a program and needs a TLS terminator in front.

⚠ **Every one of them costs throughput and adds head-of-line blocking**, because a
datagram is being carried by a stream. None was benchmarked, so no number is printed.

## What this means for the hosted TCP tunnels

A hosted tunnel that forwards an arbitrary TCP port can carry WireGuard through
`wstunnel` or `udp2raw`, and it then needs a host running the other end of the
wrapper. That is the same host a WireGuard listener needs anyway, so the tunnel
adds nothing a public port would not.

⭐ **The useful case is the opposite one: a network that blocks UDP but allows
443.** There, WireGuard over a WebSocket is the path: the hosted `wstunnel-demo`
relay first, and a self-run `wstunnel` server as the last resort. The cost is a
stream's head-of-line blocking rather than a byte quota.

## The tools that are not a path at all

`wireguard-go` and `boringtun` implement WireGuard and publish nothing. They are
recorded so a reader who finds them in a list of "WireGuard alternatives" learns
that an implementation is not a service.

`wormhole-vpn` is the closest prior art for WireGuard over a Worker, and it proves
the structural point: the Worker is a hop, and a local bridge terminates the
tunnel. It also needs a paid Workers plan (USD 5/month), so it is not a free path.

## The records

`dossier/egress/wgcf.json`, `warp-plus.json`, `usque.json`, `wstunnel.json`,
`udp2raw.json`, `wireguard-proxy.json`, `wg-tcp-tunnel.json`,
`wireguard-over-wss.json`, `tunelo.json`, `wormhole-vpn.json`, `gluetun.json`,
`boringtun.json`, `wireguard-go.json`, `cloudflare-warp.json`.

⚠ **No wrapper was benchmarked here.** The throughput cost of carrying a datagram
in a stream is real and unmeasured, and a reader who needs a number should run
`iperf3` through the wrapper rather than trust a table.
