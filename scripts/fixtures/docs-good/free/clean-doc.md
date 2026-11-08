# Clean fixture document

Binary units are written as KiB, MiB, GiB and TiB. The per-object cap is 25 MiB
per file, the drive is 1 TiB, and a 20 TiB archive fits in twenty drives.

Throughput was measured at 19.7 MiB/s over 32 parallel ranged GETs, with a
single-connection baseline of 0.48 MiB/s. Both numbers are stated because either
one alone cannot distinguish a slow host from one that collapses under load.

The evidence is a ranged GET on 2026-10-21 that returned 206 and 1 MiB, with the
sha256 recorded in the probe output. Read at 2026-10-21T09:15:00.000Z.

This document cites `fixture-good-host`, which exists.
