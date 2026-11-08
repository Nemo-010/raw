# A review found 58 defects in the three answers, and the documents had hedged where a page had an answer

- **When:** 2026-10-24T03:20:00Z
- **Status:** corrected
- **Supersedes:** `docs/compute/paid/under-five.md`, `docs/compute/paid/under-one.md`, `docs/compute/free/no-card.md`, and the floor sentence of `docs/compute/paid/README.md`, as committed at `d498591`
- **Superseded by:** an adversarial document-against-record review (`.tmp/compute-2026-10-24/lanes/L21-review/report.md`), three per-document fix passes (`.tmp/compute-2026-10-24/fix/F1`, `F2`, `F3`), and three first-party page re-reads (`.tmp/compute-2026-10-24/fix/V1`)
- **Evidence:** `dossier/compute/{c-servers,cloudcone-ssd-vps-1,datalix,gullos-hosting-nat-128,hetzner-cloud,cheap-host-nat-start}.json`; the quotes are in each record's `evidence[]`
- **Confidence:** documented

## The review, and why it was needed

An independent reviewer checked **92 claims** across the three documents against the dossier
records they cite. **58 failed.** Three had already been fixed before the review returned; 55
were live. The method was document-against-record: it did not re-read any vendor page, and
said so, which is why a second pass was needed on the three claims that turned on what a page
actually says.

⛔ **The single worst defect was in the first sentence of `under-one.md`.** It called NATKVM at
USD 0.42 "the cheapest answer" while the same document priced luo_cloud at USD 0.22 two
paragraphs later, and while NATKVM's named company had been dissolved since 2023. A reader who
stopped after the opening bought from a dissolved company at the wrong price. The correction
that was supposed to remove this residual had already been written and had missed it.

## The three claims a page settled, and the record was the thing that was wrong

| claim | what the documents said | what the page says |
| --- | --- | --- |
| CloudCone's card hold | "about USD 1, refunded within 7 days", in two documents; the record said the order flow was never opened | **supported.** `help.cloudcone.com`: "an authorization fee of usually about $1 USD, will be placed against your card … automatically refunded within 7 days". The hold attaches to *adding a card*, not to signup, and the plan payment is separately non-refundable |
| C-Servers NAT forwards | "UDP forwarding not stated" | **they carry UDP.** The vendor's NAT article names a "UDP-exclusive port-range you have on your VPS for NAT IPv4" and gives a netcat UDP test. A WireGuard listener on 51820 is reachable with no vendor action |
| Datalix's payment rails | the record said "the terms and refund policy name no rails", and carried `identity_cost.kind: card` | **the rails are published on the product pages**: PayPal, Kreditkarte, Sofortüberweisung, Giropay, EPS, Paysafecard, Przelewy24, plus crypto and bank transfer. The signup fields are username, email and password. **No hold is stated anywhere.** The kind is now `email` |

## Three record-level contradictions, corrected

- ⛔ **`gullos-hosting-nat-128` contradicted itself.** `extras.payment_methods` said "not
  established on the page read" while `extras.payment_rails` quoted "PayPal or Credit Card".
  No `evidence[]` row carried that quote, and the order page re-read today has no
  payment-method section at all: 306 words, "Total Due Today: $3.50", nothing else. The
  `payment_rails` field was an unevidenced assertion and now says so.
- **`hetzner-cloud` and `hetzner-cx23` priced the same plan differently.** 6.49 is Hetzner's own
  USD conversion printed in its price-adjustment table; 6.70 is the corpus converting the
  published EUR 5.99 at the recorded 1.1193. The plan-level record is `hetzner-cx23` at 6.70;
  `hetzner-cloud` now carries 6.70 and keeps 6.49 in evidence with the gap named, rather than
  reading as a stale duplicate.
- **`c-servers` carried `out_of_pocket_usd` 2.69** — the NanoVPS-1024 three-month figure — on a
  monthly ExtraVPS-6144 record. Now 4.29. `paid/README.md` also said HostBrr's 2 GiB was USD
  2.24 where its record's ladder gives USD 2.15, in two places.

## The defect class that matters most for this operator

⭐ **A hiding negative.** `no-card.md` said "exactly one accepts prepaid in writing: Kamatera",
while the same page's Tencent row quoted "credit cards/debit cards/prepaid cards are
supported". This is the **third** hiding negative this topic has produced, after "no monthly
machine under USD 1" and "NATKVM is the answer". The count is now three refusers in writing
(Google, Oracle, Civo), two acceptors by name (Kamatera, Tencent), and three that publish
nothing either way (DigitalOcean, Scaleway, Alibaba).

The review started from a report that free tiers demand a card with about USD 50 held on it. The
corpus now answers that question per provider, and a tool reports the gap:
`scripts/dossier/card-hold.py` finds **204 compute records that require a card and only 17 that
state how much is held**. Every document that ranks registration cost can now say how much of
its ranking rests on a stated hold.

## What the fix passes found that the review missed

The review audited documents against records; these were in the records' silence, not their
contradiction:

- **GitHub Codespaces' shape and clock were invented** in `no-card.md`: "8 GB and 32 GB" and "a
  30-minute idle stop and a 12-hour cap" appear in no record. The record states 2 cores, 15
  GB-months of storage, and that RAM, disk and any wall-clock cap are not published.
- **Cloudfanatic's "published uptime SLA" and "five years of independent monitoring"** have no
  record behind them, and sat in `under-one.md`'s opening recommendation.
- **A correlation of "about -0.47, n=14"** in `under-five.md` had no computation behind it and
  the table it described has nine rows. Removed.
- **Time4VPS's "0.4 MB/s at 4k random read"** is in no record. Removed.
- **Noteable, Valohai, Quarto Pub and Observable** were presented in `no-card.md` as live free
  options; their records say dead, paid-only, dead, and 0 free compute.

## What is still open, stated rather than closed

- ⛔ **Nothing was measured.** No account was created and no machine was booted in this topic.
  Every row is `documented`; none is `measured`. A card hold, a NAT mapping and a UDP forward
  are all vendor prose until somebody signs up.
- **Six Q1 and Q2 rows publish no renewal price.** A lane is on it. Only AlphaVPS states its
  discount is locked at renewal.
- **`c-servers` `extras.payment_rails`** still has no evidence row. Flagged, not deleted.
- **Datalix's operator field** says "Florian Kolb trading as Datalix, a sole trader" while the
  order page's legal text refers to "die Datalix GmbH". Unresolved.
