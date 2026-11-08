# The SSH relay measurement was handed to a topic that never received it

- **When:** 2026-10-22T04:07:07Z
- **Status:** restored
- **Supersedes:** `docs/compute/relay-egress.md:9` (which handed the relay to `egress` and did not carry it), and the absence of `dossier/egress/ajam-ssh-relay.json`
- **Superseded by:** `dossier/egress/ajam-ssh-relay.json`, `docs/egress/free/sealed-sandbox-reach-in.md`, and the corrected pointer at `docs/compute/relay-egress.md`
- **Evidence:** `tcp.ssh.relay.ajam.dev` measured from this host 2026-10-22; the seed files are `.tmp/seed/peli-cloud-nemo/docs/SSH-RELAY.md` (253 lines), `RELAY-FORWARD.md` (159), `research/verification/relay-forward-2026-10-02.md` (133), `research/verification/ssh-relay-2026-10-02.md` (113), `research/deep-reviews-relay-forward.md` (146) and `data/relay-colo-egress.json`
- **Confidence:** measured

## What we believed

That the relay belonged to the `egress` topic and that `egress` had it.
`docs/compute/relay-egress.md:9` said so in a marked line: "The relay itself is the
`egress` topic's. Its transports, tokens, colo pool and byte limits belong there and
this document does not repeat them." A reader who wanted the numbers was sent to a
topic that did not contain them.

## What we found

Neither topic had it. 804 lines of the nemo pass and one data artefact were in the
seed and nowhere in the tree:

| seed file | lines |
| --- | --- |
| `docs/SSH-RELAY.md` | 253 |
| `docs/RELAY-FORWARD.md` | 159 |
| `research/deep-reviews-relay-forward.md` | 146 |
| `research/verification/relay-forward-2026-10-02.md` | 133 |
| `research/verification/ssh-relay-2026-10-02.md` | 113 |
| `data/relay-colo-egress.json` | 78 |
| **total** | **882**, of which 804 are prose and 78 are the artefact |

`grep -rF "ajam.dev"` returned nothing over `docs/`, `dossier/`, `history/`,
`references/` and `sources/`. The `egress` topic held 37 records and five documents
and no relay of its own; `expose-a-local-port.md:253` mentioned the 72-hour pair life
in one sentence of prose, which was the only trace of the experiment in the tree.

The line was not a filing decision. It was a handoff with nothing on the far side,
and it read as a routing instruction to every later session, which is why the
material stayed lost through a review that counted 366 catalogue rows and found
zero missing providers. A provider inventory cannot see a lost measurement.

## How we found it

A completeness review (`RV-COMPLETE-COMPUTE`) diffed the seed's structured artefacts
against the destination and found two keys with no home: `tcp.ssh.relay.ajam.dev` and
`relay-forward`. Neither is a provider a reader can buy, so neither showed up as a
missing row.

The material was then read from the seed and **re-measured**, not copied. The relay
answers today and it has changed: the seed measured version `2026-10-01-r2` with a
four-entry pool, and this session found `2026-10-03-r2` with 37 entries.

## What it cost

One measured experiment, and one wrong answer inside it.

**The 64 MiB session cap and the 180-second idle close were documented in the seed
and never measured there.** Both are measured now. A 67,107,029-byte download through
`/connect/ftp.funet.fi/80` stopped at exactly 64.0 MiB with close `1009 session byte
cap` after 6.66 s, which is 9.605 MiB/s. A forward session held open after the
greeting closed at 180.7 s with close `1001 idle timeout`. Those are the two numbers
`docs/compute/relay-egress.md` argued about without carrying.

**The seed's central negative result does not reproduce, and it was wrong.** The seed
reported that the forward path delivers a target's first bytes and "cannot deliver
the client's bytes past that point, for any protocol", tested on `example.com:80`,
`neverssl.com:80` and `example.com:443`, all zero bytes back with a broken pipe. The
seed also recorded that it had never driven a raw WebSocket client at `/connect` and
that its failing probes contained no SSH. Review R25 named the missing control: the
same HTTP probe from a host whose client is not `dropssh` v0.2.3.

That control ran on 2026-10-22. A raw WebSocket client read 1,010 bytes of a full
HTTP response from `example.com:80` through the forward path, and read 824 bytes of
SSH key-exchange payload from `github.com:22` after sending its own identification
string. The forward path carries both directions.

Two explanations fit and this session did not separate them: the relay fixed the
path between versions, or the fault was always `dropssh`'s client. The second is the
likelier one, because the control that now passes is exactly the one R25 said would
settle it, and it settles it against the seed's framing.

**The reverse path is not SSH-specific.** The seed proved it with `dropbear` over
`dropssh` and a real login. This session proved it with a node that speaks nothing but
the relay's own control messages, and an operator that read its 44 bytes back. Both
results are now in one record instead of in a seed directory.

## What was decided, and why

The material belongs to `egress`. A relay is a byte transport, not a machine, and the
`egress` topic's own first split is signalling versus relaying. `compute` owns what a
machine costs once its network is accounted for; `egress` owns the relay's byte
limits. Those are two questions and the second is the one the 64 MiB cap answers.

So the record is `dossier/egress/ajam-ssh-relay.json`, the document is
`docs/egress/free/sealed-sandbox-reach-in.md`, and `docs/compute/relay-egress.md`
now cites the document by path instead of disclaiming it. The fault that produced
this entry was a cross-reference with no owner behind it; the repair is a
cross-reference to a file that exists, and a reader can check that in one click.

## What was not carried, and why

The seed's line-by-line reproduction scripts are not in this tree, because this
repository keeps no third-party tooling. The four configuration facts that make a
sealed host serve SSH (the `-Y` passwd file, the uid match, the non-world-writable
work directory and the client-side preload) are carried as prose in the document,
because they are the reusable part and they cost a wave to find.

The seed's seven "not established" limits are carried as the document's own limits
section. They are still not established: no session was held to the 720-minute cap,
no `direct` road was forced, no IPv4 egress was observed and no throughput beyond
one 64 MiB object was measured.
