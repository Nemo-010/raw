# Torrents and seedboxes

A torrent is fetched by somebody else's machine and handed back over HTTP, or it is
fetched by a rented machine the reader controls. The first is a service; the second
is a seedbox. Both turn a magnet into a file the reader can read without owning a
computer that stays up.

## The answer

⛔ **The free ceiling for a 20 GiB object is effectively zero.** Every free tier is
built for small files: Seedr 2 GB, Bitport and TorrentSafe 1 GB, CloudPipe 3 GB,
TorBox 10 GB, Zbigz 20 GB. A 20 GiB torrent is over all of them, and Zbigz misses by
1.47 GB.

⭐ **The cheapest path that holds a 20 GiB object is TorBox Essential at USD 3.00 a
month**: 200 GB per torrent, 3 slots, 300 GB Airlock, and files deleted 30 days
after the last download. AllDebrid at EUR 2.99 is the adjacent option and needs a
card recurring. Webtor Bronze at USD 2.00 offers a 50 GB vault.

## Torrent-to-cloud

| service | free ceiling | per-object cap | retention | verdict |
| --- | --- | --- | --- | --- |
| Seedr | 2 GB | 2 GB free | files kept indefinitely, over-cap files unreadable | qualifies-with-caveat |
| TorBox free | 10 downloads a month | 10 GB | 30 days after last download | qualifies-with-caveat |
| TorBox Essential | USD 3.00 | 200 GB | 30 days plus Airlock | qualifies |
| Zbigz | 20 GB | 20 GB | not stated | trial-only |
| Bitport | 1 GB | 1 GB | not stated | fails-quota |
| TorrentSafe | 1 GB | 1 GB | not stated | fails-quota |
| CloudPipe | 5 jobs a day at 3 GB | 3 GB | into a connected Drive | qualifies-with-caveat |
| put.io | none | 100 GB to 1 TB by plan | 15 days after deactivation | paid-only |
| Webtor | 50 Mbps for 7 days, card-gated | no published cap | 7 days | trial-only |

⭐ **TorBox publishes the retention clock most services hide**: files are deleted
"30 days after the last download", Airlock pins them, and the Free plan gets 0 GB
of Airlock. Its abuse floors are 5 TB a month on Free and 10 TB on Essential, the
only threshold in the corpus framed as "below this we will not flag you".

⚠ **put.io throttles before it cuts.** Its help page gives 1 TB a month of
downloads, then 1.5 MB/s, and 3 TB on the 1T plan.

## Seedboxes

A seedbox is a rented machine with a BitTorrent client and an HTTP or SFTP
endpoint. It is a service, not hardware the reader owns, so it belongs here.

| host | entry price | disk | traffic | apps |
| --- | --- | --- | --- | --- |
| PulsedMedia Eternal | EUR 1.99/month | 1 TB | 10,000 GiB, 10 Gbps then shaped | yes |
| YourSeedbox | EUR 1.33/month | small | unmetered | yes |
| Bytesized Appbox Lite | EUR 5.00/month | 500 GB | unmetered, 2 transcodes | yes |
| Ultra.cc | EUR 13.95/month | 4 TB | metered | yes |
| dediseedbox | USD 10/month | 750 GB | unlimited, 10 Gbps | yes |
| SeedHost | EUR 3.00/month | 1 TB | metered | bare |

⛔ **A traffic allowance is not a port speed.** 1 TB a month is 3.09 Mbit/s
sustained. A "1 TB at 1 Gbit/s" plan burns its allowance in 2.2 hours and spends
the remaining 718 shaped or idle. The allowance is what a buyer gets; the port is
marketing.

⚠ **PulsedMedia's free 50 GiB trial is real and out of stock.** Three vendor
counters agreed at 02:30Z on 2026-10-23: the page says `Available: 0`, the cart
says "Out of stock ... orders suspended", and `products.json` product 297 says
`stock: 0, available: false`. The only cadence statement is a 2023 forum post,
"several times per hour", and forum users report bots clearing it.

⚠ **Ultra.cc's cheap tiers forbid the apps that matter.** Both entry plans print
"Plex, Jellyfin or Emby: Not Allowed"; the app-inclusive floor is EUR 13.95.

## What is dead

- **seedbox.io** is dead as a brand: the apex and `www` both resolve to
 `hostingby.design`, which sells application hosting from EUR 6.59.
- **Seeding.io, SwiftSeedbox, EpikHost and Gigarapid** are recorded dead with the
 evidence of death.
- **dediseedbox is alive**, contrary to its storage record: the home page answers
 200 with "10Gbps Unlimited traffic" and a 50-application list.

## How it composes

A torrent-to-cloud service plus a public index is the whole pipeline: the index
returns a magnet, the service fetches it, the reader reads the result over HTTPS.
A seedbox replaces both when the reader wants a library rather than one file,
because it can run the indexer, the client and the player on the same rented box.

⚠ **Neither half is free.** The free tier of every torrent-to-cloud service caps
below a feature-length object, and the free seedbox trial is out of stock. The
realistic floor is USD 2 to 3 a month, which is the same floor as a multi-hoster
and buys a different shape.
