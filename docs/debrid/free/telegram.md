# Telegram

Telegram is a retrieval path only if a bot or a channel can move bytes a reader
cannot fetch itself. It is also the one platform whose limits are published as a
platform rather than as a tier, which makes the arithmetic exact.

## The answer

⛔ **Telegram publishes no monthly byte allowance for a bot.** None of the Bot API
reference, the bot FAQ or the files page states one, and the limits page named in
some guides returns "Page not found" both live and in a 2025 archive.

⭐ **What breaks first is the per-object cap, not bandwidth.** A Bot-API-hosted
bot can download a file of **20 MB** at most: "For the moment, bots can download
files of up to 20MB in size." A hosted bot therefore cannot hand back a large
object it stored, which is why the free "file to link" bots exist at all.

## The platform caps

| cap | value | source |
| --- | --- | --- |
| bot download through `getFile` | 20 MB | Bot API reference |
| bot upload through the cloud Bot API | 50 MB | Bot API reference |
| bot upload through a local Bot API server | 2,000 MB | Bot API reference |
| account upload | 2 GB free, 4 GB Premium | Telegram FAQ |
| flood control | about 1 message a second per chat, 30 a second bulk | API limits |

⚠ **The 20 MB `getFile` cap is the wall, and it is a download cap.** A bot can
receive a 2 GB file from a user and store it, and still cannot serve it back to an
API client. That asymmetry is the whole design of the file-to-link bots.

## The bots that matter

| bot or app | what it does | free ceiling | note |
| --- | --- | --- | --- |
| @uploadbot | file to direct link | 500 MB a file, 1 GB a day | 18,717 monthly users at read |
| Deepbrid bot | sends host links | 5 links a day | a multi-hoster front end |
| PikPak bot | cloud fetch into a PikPak drive | 6 GB free, 3 tasks a day, 20 GB a day downstream | email gate |
| DebridMaster | sends a download link, not a file | 2 files a day at 512 MB, then USD 0.50/GB | states it does not use Telegram for the bytes |
| @MaxxLeech_Bot | claims 4 GB a file | reported, unmeasured | the bot's own channel only |

⭐ **The debrid bots in Telegram move zero bytes through Telegram.** DebridMaster
states it outright: "Does the bot send the file through Telegram? No. It sends a
download link to our verified copy." Telegram is the front end; the bytes come
from the service.

## What a `t.me` page proves

⚠ **A `t.me` page proves the directory entry, not the service.** Two handles that
directories still list now resolve to plain users with no Start button, and both
are recorded `dead` with that artefact. A third resolves with a description
despite a 2022 listing calling it unusable.

Liveness beyond "the handle is a bot today" needs a Telegram account and a phone.
Every bot record says so.

## Storage as a path

A Telegram channel can hold files indefinitely, and the 2 GB per-file cap with no
total is attractive. It is not a route for a reader:

- the Bot API cannot read back above 20 MB, so a bot cannot be the read path;
- an MTProto user session can, but that is a client the reader must run somewhere;
- `teldrive` and `telegram-drive` are self-hosted software, so they need a machine,
 which a reader does not have.

⚠ **A rented box running the self-hosted `teldrive` is the last resort**, after the
hosted fronts the next section names (Deepbrid, PikPak, DebridMaster): the hardware
is the provider's, the storage is Telegram's, and the cost is the box. It is
recorded as tooling, not as a free tier.

## How it composes

1. Use a bot only as a front end to a service that holds the bytes: Deepbrid,
 PikPak, DebridMaster.
2. Read the result over HTTPS, not through `getFile`, so the 20 MB cap does not
 apply.
3. Treat a channel as an archive only with an MTProto client on a rented machine.

⚠ **Flood control binds only for tiny objects.** At about 1 message a second per
chat, a 1 TiB month would need an average object under 424 KB, and at 30 a second
under 14 KB. For anything a debrid would fetch, the per-object cap arrives first.
