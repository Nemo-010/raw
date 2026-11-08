# What can I get with no account at all

An anonymous machine is one that identifies the caller by something already held,
usually an SSH key, and asks for no email, no card and no phone. The class is
nearly empty. Across two censuses of 26 and 23 rows, one lane needs nothing and
gives a persistent machine: Railway's `ssh railway.new`.

The answer: Railway gives a 2 vCPU, 2 GB VM with coding agents preinstalled, no
account and no card, on three boxes per IP per day, and deletes an unclaimed box
after 24 hours. It answers SSH from the probe host: a TCP connect to `railway.new:22`
succeeded in 116 ms and the host sent `SSH-2.0-Go`, and the same connect answered
again in 120 ms in the second saved run under `sources/2026-10-24/compute/`. What
is not established is whether a key is accepted once the connection is made,
because no key was offered. Two other live records reach a machine with no
identity, `the-vibe-hosting` and `mybinder`, and neither is a VM to keep. Every
other row wants an email, and the interesting ones want a card.

## The comparison

Sorted by what registration costs. `Reach` is what a probe established about
the endpoint, not what the vendor states.

| Provider | What it gives | Identity | Clock | Reach | Verdict |
| --- | --- | --- | --- | --- | --- |
| Railway `railway.new` | 2 vCPU / 2 GB, agents preinstalled | anonymous | 60 min to build, then 24 h to claim | port 22 answered in 116 ms and 120 ms, banner `SSH-2.0-Go` | trial-only |
| The Vibe Hosting | a root Ubuntu container on an HTTPS subdomain | anonymous: one unauthenticated POST issues the credential | 256 MB tier sleeps when idle; a phone raises it to 2 GB | not dialled | qualifies-with-caveat |
| Binder (mybinder.org) | a Jupyter session from a public repo, 1 to 2 GB RAM | anonymous: no account and no card | 6 hours or 1 CPU-hour; no storage | not dialled | fails-quota |
| hashbang | LXC, 512 MB, 50% CPU | email | 30 days without a login | TCP answered, no banner in 6 s | qualifies-with-caveat |
| tilde.green | shared Ubuntu, 1 GB soft and 1.5 GB hard | email | none; idle welcome | SSH banner read | qualifies-with-caveat |
| ctrl-c.club | shared Linux, 1 GB soft | email, and **signups are closed**: waitlist only | 5 years without a login | SSH banner read | qualifies-with-caveat |
| SDF Public Access UNIX | shared host, 20 MB x4 | email | 2 years without a login | SSH banner read | qualifies-with-caveat |
| tilde.zone | a host answering SSH; the site is a Mastodon instance | unknown | unknown | SSH banner read | qualifies-with-caveat, at `unverified` confidence |
| serv00 | shared FreeBSD, 3 GB | email | 90 days without a panel or SSH login | SSH banner read | qualifies-with-caveat |
| tilde.club | shared Unix, 3 GB hard | email | none found | SSH banner read | qualifies-with-caveat |
| tilde.town | shared Debian, no ports | email | none; no inbound | SSH banner read | qualifies-with-caveat |
| tilde.guru | shared FreeBSD | email | none documented | TCP answered; banner on 2026-10-24, none on 2026-10-22 | qualifies-with-caveat |
| Blinkenshell | shared, 128 MB | email, then an SMS to a mobile number and two human vouches | none published | port 2222 timed out on both runs | fails-identity |
| Play with Docker | was an anonymous Docker lab | anonymous | withdrawn | unavailable | dead |
| Killercoda | was a browser lab | email | 1 hour | not dialled | trial-only |
| Google Cloud Shell | ephemeral VM, 5 GB home | email | 12 hours a session, 50 hours a week | not dialled | qualifies-with-caveat |
| Browser Linux emulators (self-hosted) | a WASM Linux in the tab | anonymous | the tab | not a remote machine | dead |

## Railway's anonymous VM

`ssh railway.new` with any ed25519 key gives a Linux VM on Railway with no account
and no card. Railway identifies the caller by the SSH key, and the same key lands in
the same VM every time. The box is 2 vCPU and 2 GB, with coding agents
preinstalled (`documented`, `railway.com/free-vm.md`, read 2026-10-22). The
page states no boot time, and no probe records one.

The clocks are what make it a trial. A box has 60 minutes to build and then 24
hours to claim; unclaimed boxes are deleted with their files. There are up to 3
boxes per IP address per day. Compute for unclaimed boxes is free. The preview URL
answers only the IP address that created the box until it is claimed, and it is
IPv4 only.

⭐ From the probe host, TCP connect to `railway.new:22` answers. Two saved runs on
2026-10-24, `tcp-probe-20261024T040812.229Z.json` and
`tcp-probe-20261024T043117.200Z.json` under `sources/2026-10-24/compute/`,
connected in 116 ms and 120 ms to 66.33.22.2 and read the banner `SSH-2.0-Go`
(`measured`, 2026-10-24). The earlier run, saved as
`sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`, timed out at
8,134 ms, while nine of its twelve targets answered on the same machine. The
2026-10-22 timeout was a fact about that hour, not about the provider.

The banner is Railway's own SSH front end. It proves the port and the protocol
greeting. It does not prove that a key is accepted, that a VM is created, or that
the 24-hour claim window still exists, because no key was offered and no box was
requested. That test needs a key and a POST, and it is the one this document names.

The `banner-verified` state in the record came from a relay, not
from a direct connection. A relay's egress is not the reader's egress.

⚠ The vendor's own page allows the offer to be withdrawn under demand: anonymous
trials are capped per region and can be disabled.

Evidence: `railway.com/free-vm.md` (read 2026-10-22) for the offer, the clocks and
the per-IP cap; `probe:railway.new:22` (2026-10-24) for the answer. Verdict:
`trial-only`, and reachable from the probe host at the transport layer.

## The pubnix shells, which are not anonymous

Nine of the rows above are shared UNIX hosts run by individuals and small
communities. They answer SSH, they cost nothing, and each one asks for an email
address. They are in this document because the reachability measurement is worth
having and because a census of anonymous hosts tends to fold them into the anonymous
row. A tenth
row, `tilde.zone`, answers SSH and is not established as a shell, so it is counted
below as a measurement and not as a host.

Only one of the nine states that it opens no user port: `tilde.town`. Five more
publish no port policy at all, which is an absence of a statement rather than a
statement of absence, and `sdf` restricts the free level by tool instead of by
port. Two do offer a listener: `serv00` lets an account reserve a port from 1024 to
64000 with `devil port add`, and `blinkenshell` sells a custom TCP or UDP port as a
supporter feature. A shell here holds a cron job and a few gigabytes, and reaches
the outside without a port; tunnels are the `egress` topic's.

The clocks differ by two orders of magnitude: ctrl-c.club archives after 5 years,
SDF expires after 2 years, serv00 deletes after 90 days without a login, hashbang
sweeps after 30 days, and tilde.green states that idle accounts are welcome. That
spread is the reason this class needs a document rather than a line in a table.

Evidence: ten `probe:` records from the 2026-10-22 run, one per host, each with a
connect time and a banner where one arrived, and the same ten re-run on 2026-10-24.
Verdict: a free shell with a cron and between 20 MB and 3 GB of disk, reachable
outbound and, at `serv00`, on a reserved port.

## The rows that look anonymous and are not

⛔ **Browser Linux emulators are not remote compute.** WebVM is the strongest of
them: real Debian on x86 and real Tailscale networking. The processor is the
reader's own laptop and the machine dies with the tab.

**Killercoda** wants an account and gives a browser lab for one hour. It is a
learning environment, not a machine.

**Google Cloud Shell** wants a Google account and gives an ephemeral VM with a
5 GB home for at most 12 hours.

**hashbang** wants an email address and a registered SSH key. It was the closest
call in this class, and it is still an account.

**The Vibe Hosting** and **Binder** are the two rows that are anonymous and do
reach a machine. Neither is a VM to keep: Vibe Hosting's free tier sleeps when
idle unless a phone number is verified, and Binder gives one CPU-hour with no
storage at all. They are in the comparison table because a census that lists only
Railway understates the class.

## What did not work

- **Play with Docker**: the canonical anonymous free VM in every list older than
  2026-03, unavailable from 2026-03-01.
- **Tiny anonymous sandbox trials**: several providers advertise a card-free
  start, and each one, read, wanted an account before it would create a machine.
  The record set carries them by name rather than as a claim here.
- **Browser Linux emulators** (self-hosted): the cycles are the reader's own.

## Chaining

Railway's box takes an SSH key and comes with coding agents installed, so it can
be used as a one-shot build host: push, build, publish the artifact to storage,
and let the box expire. The 24-hour claim window is the whole budget and there is
no reason to claim.
