# Downloaders and link resolvers

A multi-site downloader takes a link, waits out the host's free tiers, and hands
back a file. The corpus assumes no machine that stays up, so the question is which
hosted instance or public endpoint does it with no install and no account.

## The answer

⭐ **The only hosted service that resolves a host link with no install and no
account and states its cap is LeechPremium**: "Free users can generate up to 5
links per day with a maximum file size of 1GB". That is about 150 GB a month,
ad-funded, with no API.

⚠ **The cap is the vendor's claim.** No generation was run against a real host
link, so the sentence is `documented` and the read path is not `measured`.

## The class, and what each member really is

| service | what it is | free ceiling | verdict |
| --- | --- | --- | --- |
| LeechPremium | hosted link generator | 5 links a day at 1 GB | qualifies-with-caveat |
| premium.to | paid link generator | none | paid-only |
| Premium-Leech, PremiumLink.site | hosted generators | no number published | unverified |
| debridr | hosted generator | daily limit, unquantified | unverified |
| Filecrypt | container resolver | none, links point at hosts | qualifies-with-caveat |
| MyJDownloader (self-hosted) | remote control for a JDownloader instance | none without a machine | fails-identity |
| pyLoad (self-hosted) | self-hosted, some public instances | instance-set | trial-only |
| MegaBasterd, megatools (self-hosted) | clients for one host | none, software | tooling |

## MyJDownloader is not a downloader

⛔ **Its own terms define it as a remote control**: access to "the program
JDownloader ... installed on a computer of the Customer". The API rejects an
unsigned `/my/connect` with HTTP 400, 49 bytes, and
`{"src":"MYJD","type":"BAD_PARAMETERS"}`. Device count is published nowhere; the
terms say only "limited scope of Service" for free accounts.

For a reader with no machine that stays up, this is not a service at all. It is a
tooling note, not a rejection of the provider's capacity.

## Public instances are private containers

Three public JDownloader instances were found, and none accepts anonymous input:

| instance | answer |
| --- | --- |
| `wojd.goip.de` | HTTP 200, 17,403 bytes, body "Credentials needed" |
| `jdownloader.markodj.com` | HTTP 530 |
| `jdownloader.stehuenet.selfhost.co` | HTTP 502 |

⚠ **The self-hosted pyLoad's default login is `pyload`/`pyload`, and anonymous add is
still impossible.** The JSON API opens with "First you need to authenticate", and the one
public instance found is login-walled, 14,235 bytes, with "Captcha waiting",
"Username" and "Password" in the page. A default password on a public instance is
a security fact, not a free tier.

## The false 200

⛔ **premium.to's public `getfile.php?link=` returns HTTP 200 with a zero-byte
body.** It has no free tier at all. A status check sees success; a reader sees
nothing.

## Containers resolve to host links

⚠ **Filecrypt answers 200 to an anonymous container GET** and yields host-page
links plus an optional "Security Check" captcha. It never returns a byte stream.
A reader who expects a direct link from a container will wait on a page it cannot
parse.

Linksave.in and linkcrypt.ws are dead: one redirects to a `ww17.` parking host and
the other no longer resolves.

## How it composes

1. Resolve the container to host links with Filecrypt, or take the host link
 directly.
2. Send the host link to a multi-hoster, which is cheaper per byte than any
 generator once the volume passes about 50 GiB a month.
3. Use a generator only for the free month, and only for objects under 1 GB.

⚠ **A generator that publishes no number is not a candidate.** Premium-Leech and
PremiumLink.site publish no cap, debridr admits an unquantified daily limit, and
premium.to has no free tier. The absence of a number is the finding.
