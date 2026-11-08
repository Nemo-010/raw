# The free ladder

The question is not which free tier is largest. It is how many bytes a reader with
no payment instrument can obtain in one month, and in the month after, by chaining
every free allowance the corpus found.

## The answer

⭐ **1,116 GB (1,039 GiB) in month one and 1,046 GB (974 GiB) in month two, from
fourteen signups and five anonymous endpoints, with no card.** Month one clears
1 TiB by 16.5 GB. Month two falls 5% short because the one-off allowances do not
return.

⚠ **Month one is a knife edge.** It clears only if three things hold: CloudPipe's
Drive churn, PikPak's 5 GB a day, and Cheapnews' "no credit card" claim. Any one
failing gives 666, 966 or 1,096 GB, and the last is 3.5 GB short.

## The arithmetic

PikPak's FAQ states "Free PikPak accounts have a daily Downstream limit of 20 GB,
which resets at 0:00 Singapore Time. All Connected Apps together can use up to 25%
of this daily limit, or 5 GB per day." A programmatic client gets 5 GB a day, or
150 GB a month.

| step | month one | month two | what it is |
| --- | --- | --- | --- |
| CloudPipe | 450 GB | 450 GB | 5 jobs a day, 3 GB each, into a 15 GB Drive |
| Deepbrid | 180 GB | 180 GB | 5 links a day at 1.2 GB |
| LeechPremium | 150 GB | 150 GB | 5 links a day at 1 GB |
| PikPak | 150 GB | 150 GB | 5 GB a day through connected apps |
| TorBox free | 100 GB | 100 GB | 10 downloads a month at 10 GB |
| DASAN | 15 GB | 15 GB | one free job a day at 500 MB |
| one-off usenet trials | 45 GB | 0 GB | Usenet.farm, UsenetAgency, Bulknews |
| other small steps | 26 GB | 1 GB | Zbigz, Bitport and the anonymous generators |
| **total** | **1,116 GB** | **1,046 GB** | |

⭐ **Two steps carry 70% of the month.** CloudPipe at 450 GB and Deepbrid at 180 GB
are 630 GB of the 1,116. Without them the ladder is about 250 GB a month.

## What each step costs in identity

| step | gate | repeats |
| --- | --- | --- |
| CloudPipe | email, and a Google Drive to receive the file | the daily counter, unstated reset |
| Deepbrid | email | 5 links a day |
| LeechPremium | none | 5 links a day |
| PikPak | email | 5 GB a day, resets 0:00 Singapore |
| TorBox free | email | 10 downloads a month |
| DASAN | none | one job a day |

⚠ **Only two services publish a reset sentence.** Simply-Debrid says "resets at
midnight UTC each day" and PikPak says 0:00 Singapore Time. CloudPipe, Deepbrid,
LeechPremium and TorBox publish a counter and no reset, so the month-two repeat is
an inference for the three largest multipliers.

## The object-size wall

⛔ **No recurring step accepts a 20 GiB object.** Every byte-committed free tier
caps a single file between 500 MB and 3 GB. The closest miss is Zbigz at 20 GB,
which is 1.47 GB short of 20 GiB. Two paths publish no object cap: Webtor, whose
free offer is a card-gated Patreon checkout, and the anonymous relays, which cap
at 256 MiB measured.

This is why the ladder answers a monthly total and not a workload. For a single
large object the answer is a paid plan, not a chain.

## What a card buys in one move

⭐ **A card buys an order of magnitude more than every free tier combined.**
Giganews' 14-day unlimited trial is 15.12 TB at 100 Mbps. UsenetBucket's EUR 1
two-day trial is 8.64 TB. The whole no-card ladder is 0.97 TB.

That is the trade: fourteen signups and three unproven
assumptions, or one card and one trial.

## What is dead

- **AllDebrid's 25 GB / 7-day SMS tryout is dead.** It is absent from the offers
 page, the home page and the FAQ on 2026-10-23, and the archive agrees. The
 paid-only trial record stands; the free 25 GB does not.
- **Bitport's 1 GB is a cloud-storage purchase, not a byte counter**, so it is the
 only row in the total that does not multiply.
- **Webtor carries zero, not one of the five largest steps.** Its "50 Mbps free
 for 7 days" is a Patreon checkout with `is_free_trial=true`, which is card-gated.
- **The 966 GB fallback needs 8 accounts and 2 anonymous endpoints**, not the 14
 accounts and 4 endpoints an earlier pass gave for that fallback.

## Repetition is identity-bound

⚠ **No vendor in the set states a per-address limit, and four state a per-person
limit.** USENEXT's terms say "The customer may take advantage of the free trial
period only once", and the same terms say the registration IP is stored and a
pre-authorisation of "less than $5.00 US" is taken. UsenetAgency refuses VPN and
proxy signups and multiple accounts. Cheapnews says "all first time users".

So a second month from the same person is a second identity, not a second address.

## How to run it

1. **Do CloudPipe first.** It is 40% of the month and the only number resting on
 an unproven operational assumption: a 15 GB free Drive cycled 30 times. One
 3 GB job proves or kills it.
2. **Then Deepbrid and LeechPremium**, the two link-count steps that need no card.
3. **Then PikPak**, which repeats monthly and is the only Chinese service with an
 email gate.
4. **Keep the usenet trials for the first month only.** They do not return.

⚠ **This ladder is documented, not measured.** Every ceiling is a published
counter. The one step whose throughput was measured,
Catbox, is not in the ladder because it caps small objects.
