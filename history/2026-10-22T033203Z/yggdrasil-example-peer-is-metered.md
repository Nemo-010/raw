# The seed's flagship unmetered relay peer is labelled "Metered"

- **When:** 2026-10-22T03:32:03Z
- **Status:** corrected
- **Supersedes:** `.tmp/seed/storage-research/FINAL-REPORT.md` section 11b, the Yggdrasil
  arithmetic, and `METHODOLOGY.md` section 4.1 use of the same example
- **Superseded by:** `docs/egress/free/bulk-egress.md` section Yggdrasil public peers and
  `dossier/egress/yggdrasil-public-peers.json`
- **Evidence:** `raw.githubusercontent.com/yggdrasil-network/public-peers/master/north-america/united-states.md`
  (read 2026-10-22), the Virginia section
- **Confidence:** documented

## What we believed

The seed corpus built its rate-cap-versus-byte-quota argument on one example: an Oracle
Always Free node advertising 200 Mbit/s as a Yggdrasil peer, carrying 2.16 TiB/day "with no
quota". The argument is right and the example has become wrong.

## What we found

The Virginia section of the public-peers directory now reads:

```
* Ashburn, VA, Oracle Cloud VPS(Always Free Tier, 480Mbps, Metered), operated by [Twiztid].
```

Two changes. The rate is 480 Mbit/s, not 200. And the operator labels it **Metered**, because
Oracle's own 10 TB/month outbound quota sits behind the peer. It is the one case in the network
where a byte quota does apply, and it was the example chosen to prove that byte quotas do not
apply.

The directory also carries a second correction the seed did not have. The advertised rates vary by
an order of magnitude: one national file lists "up to 1000 Mbps", "100 Mbit/s", "1Gbit/s" and
"400 Mbit/s" on adjacent entries. A single peer's rate is not the network's rate.

## How we found it

The seed's own instruction was to pick a peer close by and read the directory, so the directory
was downloaded and grepped for the two numbers in the claim. Three of four sampled peers accepted a
TCP connection from this host on 2026-10-22, which confirms the mechanism; the Oracle Ashburn
address timed out.

## What it cost us

The conclusion survives, which is why the error lasted: a rate cap still does not bound a day's
volume and a byte quota still does. What does not survive is the specific number. 480 Mbit/s is
5.18 TB/day, not 2.16 TB, and it is metered at 10 TB/month, which is 333 GB/day. A reader who
planned 1.96 TiB/day against that peer would have met Oracle's quota on the second day.

The unit error is the second half. `METHODOLOGY.md` section 4.1 already records that 200 Mbit/s is 2.16 TB
and 1.96 TiB, and that the seed wrote the binary figure for a decimal computation. That correction
holds and is carried in the record's `notes`.

## What a future session should do differently

**A worked example rots faster than the principle it illustrates, and a rotted example is harder
to catch because the reasoning around it still reads true.** Re-read the source of any example
before reusing it, and prefer an example that does not depend on one volunteer's current
configuration. The durable form of this finding is arithmetic on a stated link rate, with the peer
named as a class rather than as one node.
