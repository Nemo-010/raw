# Seedboxes and hosted stacks

A stack is the assembled product: a debrid key, an index, a front end and, if the
reader wants a library, a managed host running the applications. This document
prices the whole pipeline, because a component price is not a monthly total.

## The answer

⭐ **USD 3.00 a month is enough for a working retrieval pipeline with no hardware**:
TorBox Essential at USD 3.00, Torrentio's public manifest at USD 0, Stremio Web at
USD 0, and a public addon host at USD 0.

⚠ **USD 3 buys retrieval, not a library.** For Plex or Jellyfin plus Sonarr and
Radarr the monthly total is USD 18 to 27, because the managed host is the piece
that costs money.

## The components, verified

| component | claimed | verified | note |
| --- | --- | --- | --- |
| TorBox Essential | USD 3.00 | USD 3.00 | 200 GB per object, 3 slots, unlimited downloads |
| Torrentio manifest | USD 0 | USD 0 | HTTP 200, 1,019 bytes, digest stable across 15 minutes |
| Stremio Web | USD 0 | USD 0 | torrent playback needs the local Stremio Service |
| public addon host | USD 0 | undetermined | a public instance answered "rate-limit exceeded" as a 200 stream |

⭐ **Torrentio's manifest is genuinely anonymous**: 200, 1,019 bytes, sha256
`943adba9a49e4f8b9680c648871673a26f743e9ff4e669e712de0bb6dcf8cb80`, no
configuration required, and the same bytes on a second fetch fifteen minutes later.

⚠ **Stremio Web needs a machine for the torrent path.** Torrent playback and
browser transcoding require the local Stremio Service, which is free GPL-2.0
software for Windows, macOS and Linux, so the gap is hardware and not a licence.
A non-torrent stream is handed to an external player without it.

## TorBox's tiers, exactly

| tier | price | per object | slots | monthly downloads |
| --- | --- | --- | --- | --- |
| Free | USD 0 | 10 GB | 1 | 10, one every 24 hours |
| Essential | USD 3.00 | 200 GB | 3 | unlimited |
| Standard | USD 5.00 | 200 GB | 5 | unlimited |
| Pro | USD 10.00 | 500 GiB | 10 | unlimited |

⚠ **The free tier refuses an object over 10 GB in the vendor's own words**: "Torrents
downloaded can only have a max size of 10GB ... 10GiB = ~11GB which is too high so
your torrent will be deleted." It is not the first limit met; the 24-hour cooldown
and the 10-a-month count arrive first.

## The managed host

| host | cheapest media stack | what it includes |
| --- | --- | --- |
| ElfHosted | USD 24, Zurgling | bring a debrid subscription, so USD 3 is additive |
| EvoSeedbox | USD 15, Spidey | Plex streaming, 2 TB, 5 TB upload |
| Bytesized | EUR 5, Appbox Lite | 500 GB, unmetered, 2 transcodes |
| Ultra.cc | EUR 13.95 | the first tier where Plex is allowed at all |
| CoreHost | USD 1.50 per app | 49 apps, none of them Plex, Jellyfin, Sonarr or Radarr |

⛔ **The application licences are not the cost; the media applications are.** CoreHost
sells managed apps at USD 1.50 each across 49 apps and its catalogue contains no
media server and no *arr tool. The expensive part is the class of software, not the
hosting.

⚠ **Two ElfHosted stack products showed "Sold out"** at read, and the storefront's
"USD 19" is Tubeling, a YouTube archiver, not the media stack.

## The free-only floor

| step | free | what stops it |
| --- | --- | --- |
| browse an index | yes | a public addon or a JSON index |
| resolve a link | no | needs a debrid key |
| play a torrent in a browser | no | needs the local Stremio Service, so a machine |
| store a fetched object | no | free tiers cap at 2 to 10 GB |

⭐ **The honest floor is "browse for free, pay USD 3 to watch anything large".** The
one hosted addon that needed no key, WebStreamr, is dead: both public instances
serve the same 24,382-byte deprecation page with status 200.

## How it composes

1. **Start with TorBox Essential.** It is the cheapest component that removes the
 object-size wall, and its WebDAV endpoint means `rclone` can mount it.
2. **Add Torrentio's manifest and a front end** for discovery; both are free.
3. **Add a managed host only if a library is wanted.** The jump is USD 15 to 24,
 which is five to eight times the debrid.
4. **Do not buy a seedbox for one file.** At USD 3 for 200 GB per object, the debrid
 is cheaper than the cheapest seedbox that includes the applications.

⚠ **Every price here is documented, not purchased.** VAT, add-ons and currency
conversion at payment are unread.
