# debrid watchlist

The reading list behind `scripts/sources/debrid-aggregators.tsv`. A source is
here because it lists providers this topic would otherwise miss. Its value is
the names, never the numbers: a comparison site is a lead, and the provider's
own page is the evidence.

## Comparison sites

| source | what it is good for | what it omits |
| --- | --- | --- |
| `https://github.com/fynks/debrid-services-comparison` | nine multi-hosters across price, hosts, usenet and tooling, with a live page | the nine are the Western well-known set; no free-only service, no regional service |
| `https://topdebrid.com/best-debrid-services/` | a dated 2026 table with bandwidth model, IP concurrency and affiliate disclosure | five services, and the affiliate row is the reason some are absent |
| `https://debridrank.com/` | a ranked index with host counts per service | scoring is site-relative and it ranks its own picks |
| `https://realbox.info/` | cached-torrent quality per service | no price, no limits |
| `https://world-debrid.com/` | a newer entrant at EUR 2.79 with a free plan, and a comparison against the two leaders | the site sells the service it ranks first |
| `https://debridcompare.pages.dev/` | the interactive form of the comparison repository, with host search | same nine services |
| `https://firestick.io/blog/best-debrid-services-list-for-july-full-comparison-guide/` | connections and caching per plan, tested over weeks | streaming-device audience, so it prices by convenience |
| `https://cooltechzone.com/best-debrid-services` | a second dated list, useful for cross-checking a price | affiliate ranking |
| `https://www.stremioguide.com/addons/best-debrid-service-stremio/` | the Stremio addon view, which is how most users reach a debrid | one ecosystem only |
| `https://torentio.com/best-debrid-service-for-torrentio/` | day, week and 90-day pricing, which exposes the short-plan premium | written to sell one integration |
| `https://www.usenet.org/` | 500+ usenet plans across 60+ providers, with backbone and retention per plan | a reseller index, so plan names drift from the provider's own |
| `https://nzbhydra.com/providers/` | usenet providers grouped by backbone with retention and price | a reader companion, not a price feed |
| `https://www.usenetproviderguide.com/best/best-usenet-providers.html` | provider, backbone, owner and retention in one table | affiliate ranking |
| `https://www.bestusenetreviews.com/rankings/` | retention, connections, money-back window and entry price | affiliate ranking |
| `https://4usenet.com/` | providers grouped by backbone, which is the fact a brand list hides | small set |
| `https://www.hostandproxy.com/best-usenet-providers-2026` | a dated 2026 table with example prices and retention | affiliate ranking |
| `https://usenetreviewhub.com/usenet-deals/` | deal prices with the retention beside them | deal prices are not renewal prices |
| `https://www.cogipas.com/compare-usenet-providers/` | an old but methodical comparison, useful for a baseline | last updated years ago |

## Trackers and indexes

| source | what it is good for | what it omits |
| --- | --- | --- |
| `https://vpspricetracker.com/providers` | the host list a seedbox or a VPS entry price comes from | no debrid or usenet facet |
| `https://www.serverhunter.com/` | plan-level search with a NAT and an IPv6 facet | renders plan names, not provider names, for some rows |
| `https://lowendbox.com/feed/` | one offer per post, dated | never a table, so a diff is a reading exercise |
| `https://lowendtalk.com/categories/offers` | forum offers, including seedbox and storage deals | Cloudflare-walled, readable through search snippets |

## Forums

| source | what it is good for | what it omits |
| --- | --- | --- |
| `https://www.reddit.com/r/debrid/` | enforcement reports, host-coverage changes, service deaths | posts are moments, not policies |
| `https://www.reddit.com/r/usenet/` | provider and indexer experience, including shutdowns | the wiki is more current than the threads |
| `https://www.reddit.com/r/seedboxes/` | entry prices and provider behaviour | vendor participation is heavy |
| `https://www.reddit.com/r/DataHoarder/` | retrieval workflows and service limits at volume | not a provider list |
| `https://hostloc.com/` | Chinese host and pan discussion, including per-GB fetch services | Chinese only, and the search is weak |
| `https://www.nodeseek.com/` | Chinese pan and VPS offers with dates | Cloudflare-walled, snippets only |
| `https://v2ex.com/` | Chinese pan acceleration and membership reports | threads expire from attention quickly |
| `https://www.52pojie.cn/` | Chinese client and parser releases, which show what still works | software, not services |

## How a source earns its place

A source is added when it names a provider this topic did not have. It is
retired when it stops answering, when its list is software rather than
services, or when it has not changed in a year. The gate refuses an active
source that is overdue for a diff or absent from this page.

## Registered sources

Every source in `scripts/sources/debrid-aggregators.tsv`, with the reason it earns
a row. A source is registered when it lists other providers; a single vendor page
is cited in a record instead.

| source | kind | what it is good for |
| --- | --- | --- |
| `https://4usenet.com/articles/best-free-usenet` | price-index | Dated 2026-09-26. Honest framing that 'free' mostly means a 7-to-14-day retail trial; no per-provider table. |
| `https://debrid.pl/` | price-index | Polish calculator that prices five native services by monthly GB need: TwojLimit, Pobierz.biz, RapidTraffic, NoPremium, Rapideo. Prices stamped 12.10. |
| `https://debridrank.com/cheapest-debrid-services/` | price-index | Price-per-day ranking across debrid services. Carries the daily-cap numbers that decide binding, but not payment rails. |
| `https://debridrank.com/real-debrid-vs-torbox/` | price-index | Comparison prose, claims '36 hosts with no per-host link counter' against a '100 GB ceiling on a single host transfer'. The 100 GB figure matches TorB |
| `https://firestick.io/blog/best-kodi-addons-for-movies-2026/` | price-index | Dated 2026-02-09. Real-Debrid price table that matches the vendor's own 2020-02-01 capture to the euro. Useful only because it carries a date; four te |
| `https://gist.github.com/zakkak/ca34bc1820a227b546a07debc57e4a5c` | corpus | An old but still-cited list of ephemeral services with CLI availability, max size, direct access, expiry and download limits. Its value is the CLI col |
| `https://github.com/FahadBinHussain/awesome-file-hosts` | provider-index | A curated markdown list rather than a table. Snippet search surfaced it for its 'no-auth HTTP API' notation, which is the property this lane selects o |
| `https://github.com/Hampelmen/Extensive-Usenet-Indexer-List` | corpus | Markdown table of moderated and public indexers with registration status, API/day, NZB/day and lifetime price. Broadest name list found; no dates, so |
| `https://github.com/Stremio/stremio-service` | corpus | The licence and the installer list for the local streaming server: GPL-2.0, packages for Windows, macOS, Debian, Red Hat and Flatpak. Free software; t |
| `https://github.com/SushyDev/real_debrid_ex` | corpus | Elixir client whose README states the Real-Debrid API limit as 250 requests per minute. Third-party and not in the vendor's documentation, so the reco |
| `https://github.com/anasty17/mirror-leech-telegram-bot` | corpus | The most-copied open-source mirror/leech bot, and the ancestor of most hosted instances in this lane. Useful as the reference for what a leech bot can |
| `https://github.com/archlinux/archinstall/issues/4396` | corpus | An issue titled 'Is 0x0.st dead? What file hoster should we use now', opened 2026-04-08, carrying the exact 503 body. A good model for enforcement rep |
| `https://github.com/debridmediamanager/awesome-debrid` | corpus | Curated tool list. Strong on clients, WebDAV bridges and media-server wiring; it lists no provider prices and no rate li |
| `https://github.com/milahu/debrid-services` | corpus | The one list that records API endpoints and wrapper libraries per debrid service instead of prices. That makes it the right starting point for a progr |
| `https://github.com/openlemmy/reddit-backups/wiki/Indexers` | corpus | A snapshot of a reddit wiki that no longer exists on reddit. Valuable as an archive of what communities believed; every number in it is months or year |
| `https://github.com/safelinking/Safelinking` | corpus | Official API changelog and documentation for Safelinking: protect and check endpoints, container outputs. The only container service in the set with |
| `https://github.com/topics/debrid` | corpus | GitHub topic page. The fastest way to find new debrid clients, MCP servers and API wrappers, and it names the comparison repositories: fynks/debrid-se |
| `https://github.com/xmicro/Debrid-Compare` | provider-index | Host-by-service compatibility matrix in code form. Useful for coverage questions, not for prices; not opened in depth. |
| `https://lowendbox.com/blog/black-friday-torbox-the-all-in-one-seeding-p2p-and-usenet-service-is-on-s` | offer-feed | Second write-up of the same TorBox promotion, with plan limits restated. Useful for cross-checking the BitTorrent seeding windows and slot counts against the ven |
| `https://lowendbox.com/category/seedbox-offers/` | offer-feed | Newest post is November 2024 (TorBox). LowEndBox no longer covers seedboxes in 2026; the category is a museum and treating it as a live feed wastes a |
| `https://lowendtalk.com/discussion/176835/concerns-about-debrid-service-like-alldebrid-on-greencloudvps` | corpus | Enforcement report from a VPS host: AllDebrid bans for downloading from multiple IPs on a GreenCloudVPS instance. The best evidence that the terms are |
| `https://lowendtalk.com/discussion/198214/celebrate-torboxs-birthday-with-30-off-giveaways` | offer-feed | the vendor's own forum post carrying the TorBox free-plan limits in 2024 ('One active slot, Ten downloads per month, 10GB max download size'). The c |
| `https://nzbhydra.com/indexers/` | price-index | The best single breadth table found: per indexer it lists type, free tier, API support, registration state, price and a claimed retention/size line. G |
| `https://torentio.com/free-debrid-services-for-torrentio/` | offer-feed | Compares the free tiers only. Says Debrid-Link's free tier is ongoing and resets daily at about 5 GB/day, which contradicts another page's 4 GB/day; b |
| `https://usenetreviewhub.com/usenet-backbone-comparison-guide/` | price-index | Compares usenet at the backbone level rather than by reseller, which is the distinction that decides completion rate. Pairs with the same site's reten |
| `https://world-debrid.com/guide` | price-index | A vendor's own comparison, so treat the rankings as advertising; its price rows (AllDebrid EUR 2.99/30d, Real-Debrid EUR 4/30d, World-Debrid from EUR |
| `https://www.reddit.com/r/debridmediamanager/` | corpus | The one place with a measured block rate for the Real-Debrid filter per release tag. One author, self-reported methodology. |
| `https://www.reddit.com/r/usenet/wiki/providerdeals` | price-index | Live and unpublished deals, plus a free-trials table (provider, retention, length, GB) that no vendor publishes in one place. Prices are promotional a |
| `https://www.reddit.com/r/usenet/wiki/providers` | provider-index | The backbone map: which storefronts share a spool, which ASNs are involved, and the only place that records binary retention separately from text. Bes |
| `https://www.stremioguide.com/pt/addons/best-debrid-service-stremio/` | price-index | Portuguese-language comparison of Real-Debrid, TorBox, AllDebrid and Premiumize with a 30-day price row, host counts and a multi-IP column. Useful bec |
| `https://www.usenet.org/providers/usenetfarm` | price-index | Per-provider review with the trial sentence repeated verbatim from the vendor; confirms the 10 GB no-card trial. Carries no enforcement data. |
| `https://www.usenetproviderguide.com/best/best-usenet-block-accounts.html` | price-index | Block ladders normalised to a 1 TB price, which is the only way to compare 25 GB and 5 TB products. Its CubeNet line (25 GB for $0.99) is stale agains |
| `https://www.usenetproviderguide.com/reviews/newshosting.html` | price-index | Usenet provider reviews with an explicit payment-method table per provider ('No crypto, no Wero, no SEPA payments' for Newshosting). Good for the usen |
