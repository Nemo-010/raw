# Yggdrasil has no exit nodes, so its 2.16 TB a day reaches no reader

- **When:** 2026-10-22T05:29:00Z
- **Status:** corrected
- **Supersedes:** `docs/egress/README.md` §the opening answer; `docs/egress/free/bulk-egress.md` §Yggdrasil public peers and the bulk table; `dossier/egress/yggdrasil-public-peers.json` in its previous `qualifies-with-caveat` form; `docs/egress/free/bulk-egress.md` §Chaining, the `Oracle VM -> Yggdrasil peer` lane
- **Superseded by:** `docs/egress/free/bulk-egress.md` §Yggdrasil public peers; `docs/egress/README.md` §the opening answer; `dossier/egress/yggdrasil-public-peers.json`
- **Evidence:** `https://yggdrasil-network.github.io/about.html` and `https://yggdrasil-network.github.io/faq.html`, read 2026-10-22. Quoted in the record's `evidence[]`
- **Confidence:** documented

## What we believed

A Yggdrasil public peer advertising 200 Mbit/s carries 2.16 TB per day with no
quota, because the protocol has no byte meter. The topic opened with that sentence.
It was the only free lane in the topic that cleared 500 GB to 1 TiB per day, and
`docs/egress/free/bulk-egress.md` sorted it first in a table titled "which free path
actually moves 500 GB to 1 TiB a day". The record's `chaining` field said it was
"the only free lane in this topic that carries a day's volume".

The arithmetic was right. `200 Mbit/s x 86,400 s / 8` is 2.16 TB, or 1.96 TiB, and a
previous correction had already fixed the unit from TiB to TB. That correction
still holds.

## What we found

The project's own about page states:

> Yggdrasil has **no native exit nodes**, nor does it have any concept of exit
> nodes, for providing access to the public Internet or to other networks. This can
> be achieved using proxies or other tunnelling solutions on top of Yggdrasil but
> this is not something we explicitly aim to provide.

The FAQ adds that the network transports only IPv6 internally and routes inside
`0200::/7`, a range the IETF deprecated in 2004.

So 2.16 TB per day is capacity **between two Yggdrasil nodes**. It is not capacity
between an origin and a reader, and the workload is 500 GB to
1 TiB per day of HTTP serving to the public. No part of that traffic can traverse a
Yggdrasil peer. The subject of the sentence was wrong while every number in it was
right.

## How we found it

An adversarial review re-read the vendor pages and quoted the exit-node sentence.
This session fetched `about.html` and `faq.html` directly and confirmed both
paragraphs verbatim before changing anything.

The same review asked whether the error appears elsewhere in the topic. Every record
now carries `extras.bytes_transit`, one of `yes`, `no`, `conditional` or
`self-hosted`. Thirty of 38 relay to the public internet, three relay only when a
direct path fails, three never transit anything, and two transit only the operator's
own host. The three that never transit are Yggdrasil, Headscale and serveo; the
corpus had already recorded Headscale and serveo correctly, so Yggdrasil was the
only record making this claim.

## What it cost us

The topic's headline answer. A reader who opened `docs/egress/README.md` met "a
volunteer relay peer at 200 Mbit/s carries 2.16 TB per day with no quota" as the
first substantive sentence, and that reader would have chosen Yggdrasil for serving
on the strength of it.

The verdict moves from `qualifies-with-caveat` to `fails-egress`, and the row leaves
the "what carries a day" table. The `qualifies` tier also required a probe of the
read path, which this record never had.

Two dependencies had to move with it. The bulk document's opening paragraph named
the peer as the only lane, and its chaining section proposed
`Oracle Always Free VM -> Yggdrasil peer` as the bulk chain. Both are corrected, and
the rejected-chain note now says why.

## What a future session should do differently

**Check what a relay connects to before checking how fast it goes.** A rate is a
property of a link; a path is a property of the network at both ends. Every number
in the Yggdrasil claim was measurable, verifiable and true, and the sentence was
still wrong because nobody asked where the far end was. The question that catches
this costs one page: what does this network reach?

⭐ **The topic's own rule already said it and was not applied.** "A relay that only
coordinates is not a relay that transits bytes" was stated in the same README that
carried the error. It needs a second clause, which every record now carries as a
field rather than a sentence: a relay that transits bytes inside an overlay is not a
relay that transits bytes to the public internet. Signalling, overlay routing and
public relaying are three roles, not two, and a two-row table collapsed the third
into the first.
