# Access: payment, identity and address class

Three gates stand between a price and a download, and none of them is on the
pricing page. This document records what each costs, in the order a reader meets
them.

## The answer

⭐ **Ten of fourteen services can be paid with crypto alone, with no card and no
bank.** TorBox Essential at USD 3.00 is the cheapest of them. Two accept a card
or PayPal only, one accepts a country-gated cash voucher, and one could not be
read at all.

⚠ **A local payment rail is not a cardless rail.** iDEAL, giropay, EPS, P24, SEPA,
UPI and Bancontact are all bank-funded, which is a harder gate than a card for a
reader with no bank account in that country. The only genuinely cashless and
cardless local rail is a cash voucher: Neosurf, Paysafecard or CashtoCode.

## The payment rails

| service | card | crypto | other | note |
| --- | --- | --- | --- | --- |
| TorBox | yes | 20 named coins | gift cards from USD 20, mailed cash to Dover DE, Telegram Stars, UPI, ACH, Patreon | widest list in the corpus; crypto runs through Sellix |
| AllDebrid | yes | yes, surcharge unpublished | vouchers, resellers | EUR 2.50 a month on the 300-day plan, EUR 3.99 first payment |
| Real-Debrid | yes | named, stale | vouchers | its rail text still names Coinbase |
| Premiumize | yes | yes | none recorded | |
| Debrid-Link | yes | yes | reseller vouchers | |
| Simply-Debrid | cash voucher | no | Neosurf, Paysafecard, CashtoCode | the only voucher-only route |
| put.io | yes | prepaid only | Apple Pay, Google Pay, iDEAL | no PayPal |
| Utop | yes | yes | voucher reseller | +15% on TorBox, flat |
| account.us | yes | yes | voucher reseller | +34% on Debrid-Link |
| 24instant | yes | yes | voucher reseller | +400% on Real-Debrid, every SKU out of stock |

⛔ **Coinbase Commerce closed for merchants outside the US and Singapore on
2026-03-31.** Any service whose rail text still names it has a decayed claim, and
Real-Debrid is one of them.

## The voucher markup

A reseller that sells a key for crypto is a route to a card-only service without a
card. It is not a saving:

| route | markup over the vendor |
| --- | --- |
| Utop, TorBox | +15%, flat on every tier |
| account.us, Debrid-Link | +34% |
| 24instant, Real-Debrid | +400%, and out of stock |
| key resellers, general | 1.3x to 5.0x |

⚠ **A shared account is not a subscription.** It costs 1.04 to 1.11 times the
vendor rate, the buyer gets credentials by email, cannot re-key them, and the
mailbox belongs to the seller. The same product copy appears on several
storefronts, which is the signature of one wholesale source.

## The address class

Five of the nine best-known services refuse the address class a reader without
local hardware must use. The full table is in
[`multi-hosters.md`](multi-hosters.md#the-address-class); the operational facts
are here.

⭐ **TorBox is the only one of the nine that states any address may call it.** Its
knowledge base says "TorBox doesn't track your IP at all ... There is no restriction
on where you log in and download files from", and its API documentation says IP
whitelisting was removed because limits are per token. Its 33-code error table
contains no address refusal.

⚠ **Real-Debrid's allowed-VPN list existed until about September 2026.** The
2026-08-29 archive of its `/vpn` page holds a 113-row table; the 2026-10-20
capture and both live reads render a zero-row table. The page still answers per
address, so the question is not "is the class allowed" but "is this address on
the current list", and the list is not published.

⚠ **The refusal can be a support ticket rather than a wall.** A dedicated-server
user was told "Dedicated servers are not allowed" and answered two days later "I
did, they sorted it, it is working now". A 2024 thread shows the same error firing
on home wifi while mobile data worked, which means the signal is unreliable in
both directions.

## Identity

Identity is the binding constraint on almost every large quota in this corpus,
and it is distinct from payment:

| kind | what it costs | where it is the gate |
| --- | --- | --- |
| anonymous | nothing | relays, public indexes, anonymous hosts |
| email | an address | TorBox, PikPak, most Western services |
| any-phone | any number that receives a code | Xunlei, some trials |
| country-phone | a number in a named country | 115, Quark, Baidu, Aliyun, 123pan, Tianyi, Taobao, Fshare |
| card | a payment instrument | AllDebrid trial, Giganews, UsenetBucket |

⭐ **PikPak is the only Chinese service in the corpus with an email gate**, which
makes it the only one a registrant without a PRC identity can reach: 6 GB free, 10 TB on a plan
at roughly USD 20 to 58 a year.

## How to read a verdict

A record's `verdict` describes the reader's reach including resellers and cash
codes; `identity_cost.kind` describes the vendor's own gate. Where the two
disagree, the record says which one it used. Most records in this topic carry
`binding: none` with a note that the gate is a payment rail, because the seven
constraint kinds in the schema do not name a payment method.
