# Relays and anonymous file transfer

A relay accepts a file or pulls a URL, holds it, and hands it back over HTTPS with
no account. It is the smallest possible retrieval service, and unlike a debrid it
can be measured end to end without paying anything.

## The answer

⭐ **Nothing re-encoded or truncated.** Fourteen uploads were read back and hashed,
including 256 MiB round trips through filebin.net and temp.sh, and every read-back
that returned bytes returned a matching SHA-256.

⛔ **The failure is HTTP 200 with an HTML landing page instead of the file**, and it
arrives by four different mechanisms: a Referer gate, a POST gate, a User-Agent
gate, and a false 200 with a zero-length body.

## What was measured

| service | cap | retention | read-back |
| --- | --- | --- | --- |
| filebin.net | 256 MiB measured | 7 days by its API, 6 on its page | exact bytes with a curl User-Agent, HTML with a browser one |
| temp.sh | 256 MiB measured | 3 days | exact bytes with POST, HTML with GET |
| crafterbin | 512 MiB | 7 to 365 days by size | exact bytes after a server-side URL pull |
| `catbox-moe` | 200 MiB | permanent | 6,585,929 bytes twice, 0.315 MiB/s |
| 1fichier | 300 GB stated | 15 days unregistered | remote-URL console redirects to login |
| qu.ax | 1,024 KiB measured | not stated | exact bytes only with a Referer |
| x0.at | not measured | not stated | the surviving 0x0-shaped host |

⭐ **The largest stated anonymous cap is 1fichier at 300 GB per file for 15 days,
and its remote-URL console redirects to a login page.** The largest cap that is
script-reachable and measured is **256 MiB byte-exact**. The gap between a stated
cap and a usable one is the finding.

## The four gates

**Referer.** `qu.ax/x/<id>.txt` returns 200 with 8,254 bytes of HTML when no
Referer is sent, and 200 with the exact 1,048,576 bytes when one is. Its upload is
extension-gated too: the same bytes return 400 as `.bin` and 200 as `.txt`.

**Method.** temp.sh returns 200 with a 3,188-byte page reading "Click here to
download" on a GET, and the exact bytes on a POST. Verified at 1 MiB and at 256 MiB.

**User-Agent.** filebin.net returns the exact bytes to curl and a 5,392-byte HTML
page to a browser User-Agent, both 200. `Accept` changes nothing. Its API also says
`expired_at - created_at = 7.000 days` while its page says 6.

**False 200.** Filemail answers `200 OK` with a zero-length body and no link.
premium.to's `getfile.php` does the same. A status check sees success.

⚠ **A client that checks only the status will store HTML as a payload.** A relay is
where that mistake is easiest to make.

## Server-side pull

⭐ **crafterbin is the one account-free server-side URL pull that works.** It takes
a documented `url` field alongside `file`, caps at 512 MiB, and sets retention by
size from 7 to 365 days. A pull from a Catbox link returned an identical digest,
which proves the server got the bytes; it does not prove whether it stored or
proxied them.

That distinction matters: a proxy is not storage, and a link that dies when the
source dies is not a copy.

## What is dead

| service | state |
| --- | --- |
| 0x0.st | uploads disabled, HTTP 503, "no ETA" |
| envs.sh | parked |
| ttm.sh | no TCP |
| transfer.sh | timed out |
| bashupload.com | NXDOMAIN |
| oshi.at | self-signed TLS |
| file.io | 405 on a second date |
| Filemail | 200 with a zero-length body |

## How it composes

1. Use a relay for an object under 256 MiB when no account is available.
2. Use crafterbin when the bytes must be pulled server-side rather than uploaded.
3. Use 1fichier's free tier when the object is large and a 15-day life is enough,
 and expect the remote-URL console to need a login.
4. Never treat a relay as an archive. The longest measured retention is about a
 year, and the free ones measured are days.

⚠ **Retention is the constraint, not capacity.** A 256 MiB object that lives three
days is a transfer, not a store.
