# When a machine cannot listen, and what a relay costs

Half the machines in this topic cannot answer an inbound connection. A sandbox
behind a NAT, a pubnix with no user ports, a Cloudflare Worker that can only
respond to a request it received: each one runs code and cannot be reached. The
question this document answers is not how to build a relay but whether the machine
is worth buying once its network is accounted for.

⭐ **The relay is the `egress` topic's, and it is measured there.**
[`docs/egress/free/sealed-sandbox-reach-in.md`](../egress/free/sealed-sandbox-reach-in.md)
carries the transports, the tokens, the 37-entry colo pool, the 64 MiB session cap,
the 180-second idle close, the 72-hour pair life and the forward-path result, with
`dossier/egress/ajam-ssh-relay.json` behind it. What belongs here is the effect of
the network on the compute choice, because a machine that cannot listen is a
different product from the same machine with a port.

⚠ **The forward path works.** An earlier probe reported that the relay delivered a
target's bytes and could not deliver the client's, for any protocol. A raw WebSocket
client that is not `dropssh` drove the same endpoint on 2026-10-22 and read a full HTTP
response and a full SSH key exchange. A reader acting on the earlier result would rule
out a path that carries bytes today.

## Which rows cannot listen

| Row | Inbound | Outbound | What that means |
| --- | --- | --- | --- |
| tilde.town | none: the vendor states no ports are opened for users | yes | a shell and a cron, reachable only outbound |
| tilde.club, tilde.green, tilde.guru, SDF, serv00, hashbang, ctrl-c.club, Blinkenshell | no user port is published | yes | the same: a client that pulls, not one that is pushed to |
| Cloudflare Workers | only through the edge | 50 subrequests, 6 connections | reachable, and unable to open a listening socket of its own |
| Cloudflare Durable Objects | through the edge, WebSocket yes | through the edge | reachable and stateful, no arbitrary binary |
| Google Colab, Kaggle Notebooks | no | yes | a notebook that calls out and cannot be called |
| GitHub Actions | no | yes | a job that calls out and is destroyed |
| E2B | not published; outbound is on by default and can be disabled or allowlisted | yes | a sandbox whose inbound policy the page does not state |
| Modal | tunnels and web endpoints | yes, with a CIDR or domain allowlist | reachable through a tunnel, and gated on 443 for a domain allowlist |
| boat | a public HTTPS URL per hosted port, plus raw TCP or UDP | yes, and egress is not billed | reachable without a relay |
| Lizard | previews | yes | reachable |
| Agent 37 | services on instance ports, through a preview | not published | reachable |
| Daytona | previews and SSH | yes | reachable |
| Vercel Sandbox | 15 open ports | yes | reachable |
| Oracle, Hetzner, Contabo, netcup | all ports, through a firewall or a security group | yes | a real address |

⭐ The table says three things worth separating. A shared shell has **no port**. A
serverless runtime has **a port it does not own**. A sandbox has **a port if the
vendor published one**, and half of them did not.

## What a relay does to the decision

A relay converts an outbound-only machine into a reachable one. It does not convert
it into a server. The distinction is the same one the corpus makes about link
handoff: the bytes travel over a path that somebody else holds, and when that
holder stops, the service stops.

⚠ A relay adds a second party to every request and a second clock. A machine behind
a relay inherits both failure modes, and the measured relay puts a 64 MiB session
cap, a 180-second idle close and a 72-hour token life on the path rather than on
the machine.

For the serving target assumed here, a relay is the wrong answer, and the arithmetic
has a number behind it. One day at 1 TiB is 16,384 sessions of 64 MiB, one new
session every 5.3 seconds for a day. A serving workload on a relay is a session
replacement problem before it is a bandwidth problem.

For an orchestration target it is the right answer: a pubnix shell that runs a cron
and publishes its output through an outbound connection does not need an inbound
port at all.

## The rows where the network decides the purchase

**boat** is the only cheap sandbox that publishes a port and does not bill egress.
That combination makes it the only row here that can serve without a relay, and it
is why the sandbox document leads with it for anything inbound.

**Oracle Cloud Always Free** gives a public IPv4 on the VNIC and 10 TB a month. It
is a real address and the only free one in this topic.

**Google's e2-micro** gives a public ephemeral IP and 1 GB of egress a month. The
address is real and the allowance is 0.0067 per cent of a day's 500 GB serving.

**Cloudflare Workers** answers a request and cannot listen. That is not a defect;
it is the shape of the product, and it means a Worker can front a service and
cannot be one.

## What did not work

- **A relay as a serving path**: 64 MiB per session measured, against 1 TiB a day
  wanted. The full arithmetic is in the egress document.
- **A pubnix as a web host**: no ports are opened for users on any row that states
  a policy.
- **A sandbox whose inbound policy is unpublished**: E2B states its outbound policy
  and not its inbound one. A reader should not assume a port exists because
  outbound works.
- **A notebook as a service**: Colab and Kaggle both call out and cannot be called.

## Chaining

The rule is one line: buy a port, not a relay, unless the workload is
orchestration. A box with a public address and an egress allowance is cheaper than
a box plus a relay plus the second clock, and it is the only shape that survives
the serving volume assumed here.
