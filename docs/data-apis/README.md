# data-apis

Free data APIs and their bulk downloads. The question: **which data APIs give free calls with no
card, how many, at what rate, and is there a dump that removes the call limit?**

The topic holds 155 records. No document yet; the records are in `dossier/data-apis/`.

## What the topic covers

| class | examples to research | the number that decides |
| --- | --- | --- |
| geocoding and maps | Mapbox, MapTiler, Nominatim, Geoapify, OpenCage | requests a day or a month, and whether results can be stored |
| IP geolocation | ipinfo, and the databases with a free download | requests a month, or the download licence |
| market data | Alpha Vantage, Finnhub, Twelve Data, Polygon | requests a minute and a day, history depth |
| weather and news | OpenWeather, NewsAPI, GDELT | requests a day, the delay on free data |
| open knowledge and scholarly data | Wikidata, Stack Exchange API, Unpaywall, OpenAlex, Crossref | requests a second, and the bulk dump |

Not in this topic: a model endpoint (`inference`), a page scraped because it has no API
(`crawler-scraper`), a data set kept only as stored bytes (`storage`).

⭐ **The bulk path often decides more than the call quota.** A data set with a dump, a torrent or
a public bucket has no call limit. Each record names its bulk path or says `no bulk path`.

## Records that sit in a neighbour topic

These records describe data APIs and sit under another topic. A record's `topic` and
`slug` do not change, so a duplicate is recorded as a relation: `src` the old record,
`kind` `duplicate_of`, `dst` the new one
([`../research-protocol.md`](../research-protocol.md) section 2). A record that stays
where it is carries the reason in its `notes`.

| record | verdict on 2026-10-28 |
| --- | --- |
| [`crawler-scraper/openalex`](../../dossier/crawler-scraper/openalex.json) | qualifies |
| [`debrid/crossref-rest-api`](../../dossier/debrid/crossref-rest-api.json) | qualifies |
| [`debrid/semantic-scholar`](../../dossier/debrid/semantic-scholar.json) | qualifies-with-caveat |
| [`debrid/core-ac-uk`](../../dossier/debrid/core-ac-uk.json) | qualifies-with-caveat |
| [`debrid/pmc-oa-opendata`](../../dossier/debrid/pmc-oa-opendata.json) | qualifies |
| [`storage/arxiv`](../../dossier/storage/arxiv.json) | fails-quota |

## What a record in this topic states

- The free allowance as a number, a unit and a period, quoted from a first-party page.
  `free_tier.unit` is `requests`, `credits` or `mixed` with the unit named in `stated`.
- The rate limit per second or per minute, when the page states one.
- The data fields on the free plan, when they differ from the paid plan.
- The bulk path: a dump URL, a torrent, a bucket, or `no bulk path`.
- Whether a key is necessary, whether a card is necessary, and the identity kind.
- A data licence as a one-line technical fact about what the free plan returns.

## Documents

None yet. Every record is in `dossier/data-apis/`.

## Staleness

`scripts/dossier/staleness.policy.json` sets 60 days for a verified record and 180 days for the
oldest evidence row in this topic.

## Records that no other document names

Each `measured` or `documented` record of this topic that no other document of `docs/` names.

<!-- generated:start topic=data-apis kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `abstract-api-ip-geolocation` | Abstract API IP Geolocation | fails-quota | documented |
| `airtel-ip` | Airtel IP | qualifies-with-caveat | measured |
| `allratestoday` | AllRatesToday | qualifies-with-caveat | documented |
| `allratestoday-open` | AllRatesToday (open keyless endpoints) | qualifies | documented |
| `alpha-vantage` | Alpha Vantage | qualifies-with-caveat | documented |
| `alphai` | AlphAI | qualifies-with-caveat | documented |
| `apiip` | Apiip | fails-quota | documented |
| `apogeoapi` | ApogeoAPI | trial-only | documented |
| `associated-press-media-api` | Associated Press (AP Media API) | paid-only | documented |
| `bigdatacloud` | BigDataCloud | qualifies | documented |
| `bls-public-data-api` | BLS Public Data API (Bureau of Labor... | qualifies | documented |
| `chronicling-america` | Chronicling America (Library of Congr... | qualifies-with-caveat | documented |
| `coincap` | CoinCap | qualifies-with-caveat | documented |
| `coingecko` | CoinGecko | qualifies-with-caveat | documented |
| `coinlore` | Coinlore | qualifies | documented |
| `coinmarketcap` | CoinMarketCap API | qualifies-with-caveat | documented |
| `coinpaprika` | Coinpaprika | qualifies | documented |
| `country-is` | Country (api.country.is) | qualifies | documented |
| `cryptocompare-coindesk-data` | CryptoCompare (CoinDesk Data) | trial-only | documented |
| `currencyapi-com` | currencyapi (currencyapi.com) | qualifies-with-caveat | documented |
| `currencyapi-net` | CurrencyApi (currencyapi.net) | qualifies-with-caveat | documented |
| `currencybeacon` | CurrencyBeacon (formerly CurrencyScoop) | qualifies-with-caveat | documented |
| `currencyfreaks` | CurrencyFreaks | qualifies-with-caveat | documented |
| `currencylayer` | currencylayer (APILayer) | fails-quota | documented |
| `currents-api` | Currents API | qualifies-with-caveat | documented |
| `db-ip` | DB-IP | qualifies | documented |
| `defillama` | DefiLlama | qualifies-with-caveat | documented |
| `disease-sh` | Open Disease API (disease.sh) | qualifies-with-caveat | documented |
| `earnings-feed` | Earnings Feed | qualifies-with-caveat | documented |
| `econdb` | Econdb | paid-only | documented |
| `eodhd` | EOD Historical Data (EODHD) | qualifies-with-caveat | documented |
| `exchange-rateapi` | Exchange Rate API (exchange-rateapi.com) | qualifies-with-caveat | documented |
| `exchangerate-api` | ExchangeRate-API (exchangerate-api.com) | qualifies-with-caveat | documented |
| `exchangerate-api-open` | ExchangeRate-API (open access endpoint) | qualifies-with-caveat | documented |
| `financial-data` | Financial Data | qualifies-with-caveat | documented |
| `financial-modeling-prep` | Financial Modeling Prep | qualifies-with-caveat | documented |
| `finlight` | finlight | qualifies-with-caveat | documented |
| `fiscal-data-treasury` | Fiscal Data (U.S. Treasury) | qualifies | documented |
| `fred` | FRED (Federal Reserve Bank of St. Louis) | qualifies | documented |
| `freeipapi` | FreeIPAPI | qualifies | documented |
| `fxratesapi` | FxRatesAPI | qualifies-with-caveat | documented |
| `geocodify` | Geocodify | qualifies-with-caveat | documented |
| `geocodio` | Geocodio | qualifies-with-caveat | documented |
| `geojs` | GeoJS | qualifies | documented |
| `geokeo` | Geokeo | qualifies-with-caveat | documented |
| `geolocated-io` | Geolocated.io | dead | documented |
| `geoplugin` | geoPlugin | paid-only | documented |
| `gnews` | GNews API | qualifies-with-caveat | documented |
| `graphhopper` | GraphHopper Directions API | qualifies-with-caveat | documented |
| `guardian-open-platform` | The Guardian Open Platform (Content API) | qualifies-with-caveat | documented |
| `hackmyip` | HackMyIP | qualifies | measured |
| `hirak-ip-to-country` | Hirak IP to Country | dead | measured |
| `ip-api` | ip-api | qualifies | documented |
| `ip-api-io` | IP-API.io | qualifies-with-caveat | documented |
| `ip-city` | IP.City | fails-quota | documented |
| `ip-fast-com` | ip-fast.com | dead | measured |
| `ip-location-db` | ip-location-db (sapics, GitHub) | qualifies | documented |
| `ip-vigilante` | IP Vigilante | dead | measured |
| `ip2country-info` | IP 2 Country (ip2country.info) | dead | measured |
| `ip2geo-dev` | ip2geo.dev | fails-quota | documented |
| `ip2location-io` | IP2Location.io | qualifies | documented |
| `ip2location-lite` | IP2Location LITE | qualifies | documented |
| `ip99` | IP99 | qualifies | documented |
| `ipapi-co` | ipapi (ipapi.co) | qualifies-with-caveat | documented |
| `ipapi-com` | ipapi.com (APILayer) | fails-quota | documented |
| `ipapi-is` | ipapi.is | qualifies | documented |
| `ipbase` | ipbase | fails-quota | documented |
| `ipdata` | ipdata (ipdata.free) | qualifies | documented |
| `ipfind-io` | ipfind.io | dead | measured |
| `ipgeo-techniknews` | IPGEO (api.techniknews.net) | qualifies-with-caveat | measured |
| `ipgeolocation-io` | IPGeolocation.io | qualifies | documented |
| `ipgeolocationapi-io` | ipgeolocationapi.io | qualifies-with-caveat | documented |
| `ipinfodb` | IPInfoDB | dead | documented |
| `ipkit-dev` | IPKit (ipkit.dev) | qualifies-with-caveat | measured |
| `iplocate` | IPLocate | qualifies | documented |
| `ipregistry` | Ipregistry | trial-only | documented |
| `ipstack` | ipstack (APILayer) | fails-quota | documented |
| `iptoasn` | IPtoASN | qualifies | measured |
| `iptrace-io` | IPTrace (iptrace.io) | dead | documented |
| `ipwho-org` | IPWho (ipwho.org) | qualifies | documented |
| `ipwhois-io` | ipwhois.io (ipwho.is) | qualifies | documented |
| `keycdn-ip-location-finder` | KeyCDN IP Location Finder | qualifies | measured |
| `latlng` | LatLng | qualifies-with-caveat | documented |
| `locationiq` | LocationIQ | qualifies | documented |
| `market-data-api` | Market Data API (marketdata.app) | qualifies-with-caveat | documented |
| `marketaux` | Marketaux | qualifies-with-caveat | documented |
| `marketstack` | Marketstack (APILayer) | fails-quota | documented |
| `massive` | Massive (formerly Polygon.io) | qualifies-with-caveat | documented |
| `maxmind-geolite` | MaxMind GeoLite | qualifies | documented |
| `mediastack` | mediastack (apilayer) | qualifies-with-caveat | documented |
| `mempool-space` | mempool.space API | qualifies | documented |
| `messari` | Messari (Blockworks Data API) | paid-only | documented |
| `met-norway` | MET Norway Weather API | qualifies | documented |
| `met-norway-frost` | MET Norway Frost API | qualifies-with-caveat | documented |
| `meteostat` | Meteostat | qualifies | measured |
| `meteostat-json-api` | Meteostat | qualifies-with-caveat | documented |
| `myiprightnow` | MyIPRightNow | qualifies-with-caveat | measured |
| `nasa-power` | NASA POWER | qualifies | measured |
| `nasdisks-drive-data-api` | NASdisks Drive Data API | qualifies | documented |
| `network-data-labs` | Network Data Labs | fails-quota | documented |
| `newsdata-io` | NewsData.io | qualifies-with-caveat | documented |
| `nws-api` | National Weather Service API | qualifies | documented |
| `oikolab` | Oikolab | qualifies-with-caveat | documented |
| `open-meteo` | Open-Meteo | qualifies | measured |
| `opengeocoding` | OpenGeocoding | qualifies-with-caveat | documented |
| `openrouteservice` | openrouteservice | qualifies | documented |
| `pirate-weather` | Pirate Weather | qualifies-with-caveat | documented |
| `positionstack` | positionstack | fails-quota | documented |
| `proxmint-geoip` | Proxmint GeoIP | qualifies | documented |
| `pubmed-central-open-access` | PubMed Central Open Access Subset | qualifies | documented |
| `roic-ai` | ROIC.ai | qualifies-with-caveat | documented |
| `sec-edgar-data` | SEC EDGAR Data APIs | qualifies | documented |
| `spaceflight-news-api` | Spaceflight News API (SNAPI) | qualifies | documented |
| `stack-exchange-api` | Stack Exchange API | qualifies-with-caveat | documented |
| `stadia-maps` | Stadia Maps | qualifies-with-caveat | documented |
| `stamen-map-tiles` | Stamen map tiles (maps.stamen.com) | qualifies-with-caveat | documented |
| `sthan-io-ip-geolocation` | sthan.io IP Geolocation | qualifies | documented |
| `telize` | Telize | paid-only | documented |
| `theipapi` | The IP API (theipapi.com) | qualifies | documented |
| `thenewsapi` | TheNews API | qualifies-with-caveat | documented |
| `tiingo` | Tiingo | qualifies-with-caveat | documented |
| `tomorrow-io` | Tomorrow.io | qualifies-with-caveat | documented |
| `tomtom` | TomTom | qualifies-with-caveat | documented |
| `trove-api` | Trove API (National Library of Austra... | qualifies-with-caveat | documented |
| `twelve-data` | Twelve Data | qualifies-with-caveat | documented |
| `unblock-master-ip` | Unblock Master IP | qualifies | measured |
| `unirateapi` | UniRateAPI | qualifies-with-caveat | documented |
| `unirateapi-widget-endpoint` | UniRateAPI public widget endpoint | qualifies-with-caveat | measured |
| `visual-crossing` | Visual Crossing | qualifies-with-caveat | documented |
| `waymorphic` | Waymorphic Map | qualifies-with-caveat | documented |
| `weatherapi` | WeatherAPI.com | qualifies-with-caveat | documented |
| `weatherbit` | Weatherbit | qualifies-with-caveat | documented |
| `weatherxu` | WeatherXu | qualifies-with-caveat | documented |
| `wolfram-alpha-api` | Wolfram/Alpha API | qualifies-with-caveat | documented |
| `osmnames` | OSMNames (self-hosted) | qualifies-with-caveat | documented |
<!-- generated:end -->
