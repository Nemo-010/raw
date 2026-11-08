"""Derived columns and side tables: identity flags, parsed numbers, FX, freshness,
history and ledger parsing, duplicate drift, vocabularies. Standard library only.
No number is ever typed here: FX rates come from records' own extras.fx rows. What a price text may become
(a price per TB-month, a monthly price, or a claim in its own unit) is the rule in price_claim().
"""
import collections
import datetime as dt
import json
import os
import re
import sys

VORDER = {"qualifies": 0, "qualifies-with-caveat": 1, "trial-only": 2, "paid-only": 3,
          "fails-identity": 4, "fails-egress": 5, "fails-quota": 6, "dead": 7}
GROUP = {"qualifies": "usable", "qualifies-with-caveat": "usable", "trial-only": "trial",
         "paid-only": "paid", "dead": "dead"}

QTY = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(KiB|MiB|GiB|TiB|PiB|KB|MB|GB|TB|PB|GPU[- ]hours?|"
                 r"(?:total\s+)?(?:(?:container\s+)?build|CI|pipelines?|(?:GitHub\s+)?Actions)[- ]minutes?|"
                 r"hours?|hrs?|minutes?|requests?|calls|tokens?|credits?)\b"
                 r"(?:\s*(?:/|per|a|an|each)\s*(day|week|month|year|hour|minute))?", re.I)
# a quantity of build or CI minutes ('2,500 build-minutes', '100 total build minutes', '2,000 GitHub Actions minutes'):
# its claim unit is 'build minutes', the unit the CI need reads
BUILD_MINUTES = re.compile(r"(?:total\s+)?(?:(?:container\s+)?build|CI|pipelines?|(?:GitHub\s+)?Actions)[- ]minutes?$", re.I)
BUILD_MINUTES_UNIT = "build minutes"


def qty_unit(u):
    """The unit of a quantity that QTY read: 'build minutes' for any form of build or CI minutes, else as written."""
    return BUILD_MINUTES_UNIT if u and BUILD_MINUTES.match(u) else u
USD_KEYS = ("m24h_usd", "monthly_usd", "m10h_usd", "renewal_usd")
# the unit of the claim of extras.m10h_usd: a machine run 10 hours a day, so a month of it is 300 hours
M10H_UNIT = "10 hours a day"
# the claims that state a monthly list price of the offer (stated_monthly)
STATED_MONTH_PATHS = ("$.extras.monthly_usd", "$.extras.price_on_page", "$.price_per_tb_month")
CRYPTO = re.compile(r"\b(crypto(?:currency|currencies)?|bitcoin|BTC|monero|XMR|USDT|USDC|ethereum|ETH|litecoin|LTC|TRON|TRX)\b")


CARD_WORDS = re.compile(r"\b(credit card|debit card|card (?:on file|required|verification|hold)|payment method)\b", re.I)
PHONE_WORDS = re.compile(r"\b(phone|SMS|mobile number)\b", re.I)
# a requirement said not to apply: "no card", "without a card", "a phone number is not required", "the phone field is
# not marked required", "does not ask for a card", "the absence of any phone or card requirement"
_NOT_REQUIRED = r"(?:is|are)\s+not\s+(?:marked\s+|strictly\s+)?(?:required|needed|mandatory|asked\s+for|requested)\b"
_NO_LIST = r"(?:[\w-]+,\s*|[\w-]+\s+(?:or|and)\s+)*"


def _negations(thing, end):
    """end follows 'no X' and 'without X': (?!-) for a card, so that 'no card-free path' is not a negation."""
    return re.compile(r"\bno\s+%s%s\b%s|\bwithout (?:a |any )?%s\b%s|\b%s(?:\s+[\w-]+){0,2}?\s+%s|"
                      r"\b(?:does|do|did)\s+not\s+(?:require|ask\s+for|need)\s+(?:a\s+|any\s+)?%s\b|"
                      r"\babsence of (?:a |any )?%s%s\b"
                      % (_NO_LIST, thing, end, thing, end, thing, _NOT_REQUIRED, thing, _NO_LIST, thing), re.I)


NO_CARD = re.compile(_negations(r"(?:(?:credit|debit) )?(?:card|payment method)", "(?!-)").pattern +
                     r"|\bnot? (?:credit )?card (?:is )?(?:needed|required)\b", re.I)
NO_PHONE = _negations(r"(?:phone|SMS|mobile number)", "")
# a negation that is itself negated says the thing is needed: "not an account without a card", "cannot be used
# without a card"
_NEGATED_BEFORE = re.compile(r"\b(?:not|cannot|can't|never|no longer|nor)\b[^.;,:]{0,40}$", re.I)
# a clause that says the requirement is not known, or applies to a paid tier and not to the offer
HEDGED = re.compile(r"\b(?:unverified|unconfirmed|not (?:stated|read|tested|established|confirmed|verified|published|documented|"
                    r"known|exercised|asked|quoted|mentioned|walked|listed|seen|checked|recorded)|is not stated|unknown|undetermined|could not be (?:confirmed|verified|read)|"
                    r"may (?:ask|require))\b", re.I)
# a hedged clause that asks whether the requirement itself applies ("whether the sign-up form asks for a card is
# unverified"): the question is open, and a mention of the thing elsewhere does not answer it
WHETHER = re.compile(r"\bwhether\b[^.;]*?\b(?:requir\w*|asks?\s+(?:for\s+)?|needs?\b|mandatory|takes)", re.I)
UPGRADE_ONLY = re.compile(r"\b(?:upgrad\w*|to move (?:from|to)|paid (?:tier|plan)|beyond the free|unlock\w*)\b", re.I)
CLAUSES = re.compile(r"(?<=[.;])\s+|;\s*|\s—\s")
FREE_WORD = re.compile(r"\bfree\b", re.I)
# a clause that reports a statement as contradicted or past: a free plan with no card that a source "still describes,
# which contradicts the plans page", or one that "was dropped", is not the offer now
SUPERSEDED = re.compile(r"\b(?:contradict\w*|no longer|(?:was|were|has been|have been) (?:dropped|withdrawn|removed)|"
                        r"formerly|previously|used to)\b", re.I)
CONTRAST = re.compile(r",?\s+but\s+", re.I)
# a clause that says the free plan it describes is another product or offer than the record's: "The account's free
# plan needs no card, but it is a separate datacenter offer and not this product"
OTHER_OFFER = re.compile(r"\b(?:separate|different|another|other)\s+(?:[\w-]+\s+){0,3}?(?:offer|product|service)s?\b|"
                         r"\bnot (?:this|the same) (?:product|offer|service)\b", re.I)


LOOSE_CARD = re.compile(r"\bcard\b|\bpayment method", re.I)


def negation(negated, cl):
    """The first match of negated in a clause that says the thing is not needed. A 'without' that follows a negation
    in the same phrase is not one: 'not an account without a card' says a card is needed."""
    for m in negated.finditer(cl):
        if m.group(0).lower().startswith("without") and _NEGATED_BEFORE.search(cl[:m.start()]):
            continue
        return m
    return None


def requirement(det, words, negated, loose=None):
    """1, 0 or None for one thing an identity detail may require (a card, a phone). A plain negation anywhere makes
    it 0, as it always did ('no card', 'a phone number is not required'); a hedged clause that asks whether the
    thing is required ('whether a phone number is also required is unverified') makes it unknown, whatever another
    clause says of it; a clause that names it and says it is not stated, not quoted or unverified makes it unknown
    unless another clause states it; a clause that names it for an upgrade only does not count; with no mention at
    all it is 0, as it always was for a detail that was read."""
    yes = no = hedged = open_ = False
    for cl in CLAUSES.split(det):
        neg = negation(negated, cl)
        if not words.search(cl) and not neg and not (loose and HEDGED.search(cl) and loose.search(cl)):
            continue
        if HEDGED.search(cl):
            hedged = True
            open_ = open_ or bool(WHETHER.search(cl))
        elif neg:
            no = True
        elif not UPGRADE_ONLY.search(cl):
            yes = True
    if no:
        return 0
    if open_:
        return None
    return 1 if yes else (None if hedged else 0)


def free_says_no(det, negated, loose=LOOSE_CARD):
    """True when a clause says that the free plan needs none of it: the kind of a record may name the paid plans. A
    clause that hedges, that reports the statement as contradicted or past, that says the free plan is another product
    or offer ('a separate datacenter offer and not this product'), or that goes on 'but ...' to put the thing back
    ('free with no card, but the build minutes sit behind a card') does not say it."""
    for cl in CLAUSES.split(det):
        m = negation(negated, cl)
        if not m or not FREE_WORD.search(cl) or HEDGED.search(cl) or SUPERSEDED.search(cl) or OTHER_OFFER.search(cl):
            continue
        tail = CONTRAST.split(cl[m.end():], 1)
        if len(tail) > 1 and loose.search(tail[1]) and not negation(negated, tail[1]) and not UPGRADE_ONLY.search(tail[1]):
            continue
        return True
    return False


_INFERRED_AT = re.compile(r"\b(?:is|was|are|were) inferred\b", re.I)
# where the subject of 'is inferred' starts: after a comma, a colon or a joining word
_SUBJECT_START = re.compile(r"[,:]|\b(?:so|but|and|because|since|which|while)\b", re.I)
# a subject that points back ('this half is inferred', 'That is inferred'): the thing it names is before it
_ANAPHOR = re.compile(r"(?:this|that|it|these|those)(?:\s+(?:half|part|one|step))?", re.I)
# the requirements whose flags a filter reads
_FLAG_WORDS = re.compile(r"\bcard|\bpayment method|\bphone\b|\bSMS\b|\bmobile number", re.I)


def inferred_requirement(det):
    """True when an identity detail says that its card or phone requirement was inferred, not read: 'the card
    requirement is inferred from the absence of any published rail', 'so a card is inferred', 'No card and no hold, but
    this half is inferred rather than quoted', '... a payment method is captured at signup. That is inferred from the
    product id'. The subject of 'is inferred' decides; a subject that points back ('this half', 'That') names the
    thing before it, in the same clause or the one before. An inferred kind alone is not one: 'the email kind is
    inferred from an account-based signup', 'email as the minimum is inferred', 'email is inferred from the absence
    of any phone or card requirement' infer the account, and the card and phone facts the detail states stay."""
    cls = CLAUSES.split(det or "")
    for i, cl in enumerate(cls):
        for m in _INFERRED_AT.finditer(cl):
            before = cl[:m.start()]
            starts = [x.end() for x in _SUBJECT_START.finditer(before)]
            subject = before[starts[-1] if starts else 0:].strip()
            if not subject or _ANAPHOR.fullmatch(subject):
                ctx = before[:len(before) - len(before.lstrip()) + (starts[-1] if starts else 0)] if starts else ""
                if not ctx.strip() and i:
                    ctx = cls[i - 1]
                if _FLAG_WORDS.search(ctx):
                    return True
            elif _FLAG_WORDS.search(subject):
                return True
    return False


def identity(raw, rules):
    """The identity columns of a record. identity_basis says how far the kind and the flags can be trusted:
    stated    the requirement was read from a source: the flags are 1, 0 or NULL where the text says it is unverified.
              A kind inferred in the detail's own words ('the email kind is inferred from an account-based signup')
              stays stated: the account is assumed, and the card and phone facts the detail states are read;
    inferred  the kind was worked out from the record's prose or its category, or the detail says that its card or
              phone requirement was inferred, not read (inferred_requirement). The flags are unknown (NULL), and a
              filter that wants stated facts excludes the record on purpose;
    defaulted the kind is a placeholder: the flags are unknown (NULL).

    A record of kind card whose detail says that the free plan needs no card (the card is for the paid plans) has
    needs_card 0, and its identity_kind here is the kind of that free plan: any-phone (country-phone with a country)
    when the detail states a phone requirement, email otherwise. The record's own kind stays in its document; the
    published kind and the published flag describe the same plan, never 'card' beside 'no card'. A paid-only record
    has no free allowance, so a free plan its detail names is another offer: it keeps the card kind and needs_card 1."""
    ic = raw.get("identity_cost") or {}
    kind = ic.get("kind")
    det = ic.get("detail") or ""
    defaulted = bool((raw.get("extras") or {}).get("identity_cost_defaulted")) or bool(
        re.search(rules["derive"]["identity_defaulted_re"], det, re.I))
    inferred = not defaulted and (bool(re.search(rules["derive"].get("identity_inferred_re", "(?!)"), det, re.I))
                                  or inferred_requirement(det))
    free_no_card = kind == "card" and raw.get("verdict") != "paid-only" and free_says_no(det, NO_CARD)
    if kind == "card":
        card = 0 if free_no_card else 1
    else:
        card = requirement(det, CARD_WORDS, NO_CARD, LOOSE_CARD)
    if kind in ("any-phone", "country-phone"):
        phone = 1
    else:
        phone = requirement(det, PHONE_WORDS, NO_PHONE)
    nid = 1 if kind == "national-id" else 0
    inst = 1 if kind == "institution" else 0
    if defaulted or inferred:
        card = phone = nid = inst = None
    country = ic.get("country")
    if country in ("None", "", "none", "null"):
        country = None
    if free_no_card and not (defaulted or inferred):
        kind = ("country-phone" if country else "any-phone") if phone == 1 else "email"
    return {"identity_kind": kind, "identity_basis": "defaulted" if defaulted else ("inferred" if inferred else "stated"),
            "needs_card": card, "needs_phone": phone, "needs_id": nid, "needs_institution": inst, "country": country}


def crypto_flag(raw):
    hay = " ".join([json.dumps((raw.get("extras") or {}).get("payment_methods"), ensure_ascii=False),
                    (raw.get("identity_cost") or {}).get("detail") or "", raw.get("notes") or ""])
    return 1 if CRYPTO.search(hay) else None


def fx_table(raws):
    """Collect dated rates the records themselves cite: extras.fx {pair, rate, date, source}."""
    rows = {}
    for raw in raws:
        fx = (raw.get("extras") or {}).get("fx")
        items = fx if isinstance(fx, list) else [fx]
        for f in items:
            if not isinstance(f, dict):
                continue
            pair, rate, date = f.get("pair"), f.get("rate"), f.get("date")
            if not (isinstance(pair, str) and isinstance(rate, (int, float)) and isinstance(date, str)):
                continue
            m = re.fullmatch(r"([A-Z]{3})/USD", pair.strip())
            if m and rate > 0:
                rows[(m.group(1), date[:10])] = (float(rate), f.get("source"))
            m = re.fullmatch(r"USD/([A-Z]{3})", pair.strip())
            if m and rate > 0:
                rows[(m.group(1), date[:10])] = (1.0 / float(rate), f.get("source"))
    return rows


def to_usd(amount, ccy, date, fx):
    if amount is None or ccy is None:
        return None, None
    if ccy == "USD":
        return amount, None
    cands = sorted(d for (c, d) in fx if c == ccy and (date is None or d <= date))
    if not cands:
        cands = sorted(d for (c, d) in fx if c == ccy)
    if not cands:
        return None, None
    d = cands[-1]
    return round(amount * fx[(ccy, d)][0], 4), d


# ---------------------------------------------------------------------------------------------- prices
# The price field of a record is free text. price_claim() reads it into ONE claim row; claims_for() adds
# the other claim kinds; headline_prices() chooses what lands in record.usd_month and
# record.usd_per_tb_month. The rule is in the docstring of price_claim(), and in scripts/fshy/README.md.

TB_OF = {  # how many TB (10^12 bytes) one of the unit is: a price per unit divides by it
    "TB": 1.0, "PB": 1000.0, "GB": 1e-3, "MB": 1e-6,
    "TiB": 2 ** 40 / 1e12, "PiB": 2 ** 50 / 1e12, "GiB": 2 ** 30 / 1e12, "MiB": 2 ** 20 / 1e12,
}
MONTHS_OF = {"month": 1.0, "year": 12.0, "day": 1.0 / 30}   # a day is 1/30 of a month, as the rule says
# a topic whose price field is, by definition, the price of a stored TB: a per-TB figure with no period is monthly
MONTH_DEFAULT_TOPICS = ("storage", "netdisk-pan")

_CCY = r"USD|EUR|GBP|CNY|RMB|JPY|INR|BRL|RUB|PLN|KRW|TWD|IDR|CHF|CAD|AUD|HKD|SGD|VND|TRY|UAH|CZK|SEK|NOK|DKK|THB"
_SYMS = r"US\$|R\$|\$|€|£|¥|₹|₽|₩|₺|₴|฿"
SYM = {"US$": "USD", "R$": "BRL", "$": "USD", "€": "EUR", "£": "GBP", "¥": "CNY", "RMB": "CNY",
       "₹": "INR", "₽": "RUB", "₩": "KRW", "₺": "TRY", "₴": "UAH", "฿": "THB"}
_NUM = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"
_MONEY = re.compile(
    r"(?<![A-Za-z\d])(?:(?P<c1>%s|%s)\s?(?P<n1>%s)|(?P<n2>%s)\s?(?P<c2>%s)(?![A-Za-z]))"
    r"(?:(?:\s?[-–]\s?|\s+to\s+)(?:(?:%s|%s)\s?)?(?P<hi>%s)(?![\d]))?" % (_CCY, _SYMS, _NUM, _NUM, _CCY, _CCY, _SYMS, _NUM))
_RATE = re.compile(r"\s*(?:/|per\b)\s*(?:%s)\b" % _CCY)           # 1.08 USD/EUR, 0.89 EUR per USD: an exchange rate

_TAX = r"(?:\s*(?:HT|TTC|HTVA|excl\.? VAT|incl\.? VAT))?"
_SEP = r"(?:/|\bper\b|\bpar\b|\ban?\b|\beach\b|\bevery\b)"
_VOLU = r"TB|TiB|PB|PiB|GB|GiB|MB|MiB|tb|gb|To|Go"
_PW = r"months?|mos?|mths?|monthly|years?|yrs?|annum|annually|days?|weeks?|wks?|hours?|hrs?|minutes?|mins?|seconds?|secs?"
_VOLUME = {"tb": "TB", "gb": "GB", "to": "TB", "go": "GB"}
_RE_VOL = re.compile(r"%s\s*%s\s*(?:(?P<q>\d[\d,]*(?:\.\d+)?)\s*)?(?P<u>%s)\b" % (_TAX, _SEP, _VOLU))
_RE_PERIOD = re.compile(r"\s*(?:[-/]\s*|\bper\s+|\ba\s+|\bin\s+|\bevery\s+)?(?:(?P<n>\d+)[-\s]?)?(?P<w>%s)\b" % _PW, re.I)
_RE_FLAT = re.compile(r"%s\s*%s\s*(?:(?P<n>\d+)[-\s]?)?(?P<w>%s)\b" % (_TAX, _SEP, _PW), re.I)
_RE_OTHER = re.compile(r"%s\s*%s\s*(?:(?P<q>\d[\d,]*)\s*)?(?P<u>[A-Za-z.][\w.+-]*)(?:\s+(?P<u2>[A-Za-z][\w.-]*))?" % (_TAX, _SEP))
_RE_FOR = re.compile(r"\s*(?:[,(]\s*)?\b(?:for|incl\w*|with|gives|buys)\s+(?:up to\s+|the\s+|an?\s+)?(?P<q>\d[\d,]*(?:\.\d+)?)\s*(?P<u>%s)\b"
                     r"(?P<rate>\s*(?:/|per)\s*(?:day|week|hour|sec|s|min)\b)?" % _VOLU)
_RE_CREDIT = re.compile(r"\s*(?:(?:a|per) month\s+)?(?:of|in)\s+(?:[\w-]+\s+){0,2}credits?\b", re.I)
_STOP = {"per", "a", "an", "for", "at", "on", "of", "and", "with", "in", "to", "plus", "beyond", "after", "or", "the",
         "if", "then", "but", "is", "are", "as", "by", "from", "up", "than", "i.e", "not", "no", "so", "which"}

_SENT = re.compile(r"(?<=[.!?])\s+|\s[—–|]\s|\n+")
_SOFT = re.compile(r";|,\s|\s\+\s|\s?≈\s?|\s(?:plus|but|with|while|whereas|so|which|then)\s|\s[—–]\s", re.I)
_USAGE = (r"egress|ingress|outbound|inbound|bandwidth|traffic|transfers?|deliver\w*|downloads?|uploads?|"
          r"reads?[- ]?back|read[- ]?out|(?:byte|full|every|each|per)\s+reads?|reads|retriev\w*|restor\w*|requests?|"
          r"operations?|api calls?|serv(?:ed|ing)|CDN|overage|hotlink\w*|per[- ]object|million")
_USAGE_CHAIN = re.compile(r"\b(?:%s)(?:\s*(?:/|,|&|and|or)\s*(?:%s))*\b" % (_USAGE, _USAGE), re.I)
_NEG_BEFORE = re.compile(r"(?:\bfree|\bno|\bzero|\bunlimited|\bunmetered|\bincluded|\bwithout|\bnor|\$0(?:\.0+)?|€0|\b0)\s*$", re.I)
_NEG_AFTER = re.compile(r"\s*(?:is |are |at |[:=] ?)?(?:free|included|\$0|€0|unlimited|unmetered|0\b|not metered|unpriced|unknown)", re.I)
_ONCE = (r"one[- ]?time|\bonce\b|lifetime|one[- ]off|amorti[sz]\w*|prepaid|non[- ]recurring|"
         r"\bover \d+ (?:years|yrs)\b|\d+[- ]years? horizon\b")
_PROMO = (r"promo(?:tion(?:al)?)?\b|coupon|\bflash\b|black friday|cyber monday|\bsale\b|first[- ](?:term|year|month|order)|"
          r"introductory|\bintro\b|(?<!after the )(?<!after a )\btrial\b|\bLET ?\d+%|BFBOX|campaign|new[- ]customer|"
          r"limited[- ]time|early[- ]bird")
_DERIVED = r"all-in|\beffective(?:ly)?\b|\bworkload\b|\btotal\b|\brealistic\b"
_COMPARE = (r"\bcompare\b|\bversus\b|\bvs\b|\bthan\b|price floor|floor of|(?:price|market) ceiling|ceiling of (?:this|the|that) market|"
            r"\bbeats\b|dominated|priciest")
_OTHER_PERIOD = r"\bfor (?:a |an )?\d+[- ]?(?:day|week|hour)s?\b"   # "$6.99 per TB for a 7-day hold" is not a month
_ONCE_RE = re.compile(_ONCE, re.I)
_CUE = re.compile(r"%s|%s|%s|%s|%s" % (_ONCE, _PROMO, _DERIVED, _COMPARE, _OTHER_PERIOD), re.I)
# a per-TB price followed by a region is a delivery price: "$120/TB EU/NA, $190/TB Asia"
_REGION = re.compile(r"\s*(?:EU/NA|NA/EU|Asia|Africa|APAC|Oceania)\b")
_INCR = re.compile(r"(?:\+|\bplus\b)\s*[~≈]?\s*$", re.I)
# "at 30 TB" after a per-TB figure: the volume the figure was worked out at
# a text that says its plan has one price for any volume
_FLAT_PLAN = re.compile(r"\bunlimited\b|\bflat\b|\bmarginal cost\b", re.I)
_AT_VOLUME = re.compile(r"\s*(?:\(|,)?\s*at\s+(\d[\d,]*(?:\.\d+)?)\s*(TB|TiB|GB|GiB|PB)\b")
# a text that says it has no per-TB price: every number in it is something else
_NO_PER_TB = re.compile(
    r"(?:\b(?:no|not|nor)\b[\w ,/-]{0,40}?per[- ]?(?:TB|TiB|terabyte|byte)\b|\bno \$/TB\b"
    r"|per-terabyte price meaningless|^\s*(?:n/a|not applicable))", re.I)


def _period(n, w):
    """('30', 'days') -> 'month'; only the periods that convert exactly get a name the rule can use."""
    w = w.lower()
    n = int(n) if n else 1
    if w.startswith(("mo", "mth")) or w == "monthly":
        return "month" if n == 1 else ("year" if n == 12 else "%d months" % n)
    if w.startswith(("year", "yr", "annum", "annual")):
        return "year" if n == 1 else "%d years" % n
    if w.startswith("day"):
        return "month" if n == 30 else ("day" if n == 1 else "%d days" % n)
    if w.startswith(("week", "wk")):
        return "week" if n == 1 else "%d weeks" % n
    if w.startswith(("hour", "hr")):
        return "hour" if n == 1 else "%d hours" % n
    return w.rstrip("s") if n == 1 else "%d %s" % (n, w)


def _unit(u):
    return _VOLUME.get(u.lower(), u) if u in ("To", "Go", "tb", "gb") else u


def _spec(tail):
    """What a money amount is quoted per. -> dict(kind, unit, qty, period, end): kind is vol (per TB, per GiB-month,
    per 500 GB), flat (per month, per year), forvol (EUR 26.99 for 16 TB), credit, other (per IP, per domain, per
    million operations) or bare (nothing follows). end is how many characters of the tail it used."""
    m = _RE_CREDIT.match(tail)
    if m:
        return {"kind": "other", "unit": "credit", "qty": 1.0, "period": None, "end": m.end()}
    m = _RE_VOL.match(tail)
    if m:
        unit = _unit(m.group("u"))
        qty = float(m.group("q").replace(",", "")) if m.group("q") else 1.0
        end, per = m.end(), None
        p = _RE_PERIOD.match(tail, end)
        if p:
            per, end = _period(p.group("n"), p.group("w")), p.end()
        return {"kind": "vol", "unit": unit, "qty": qty, "period": per, "end": end}
    m = _RE_FLAT.match(tail)
    if m:
        per, end = _period(m.group("n"), m.group("w")), m.end()
        f = _RE_FOR.match(tail, end)
        if f and not f.group("rate"):
            return {"kind": "forvol", "unit": _unit(f.group("u")), "qty": float(f.group("q").replace(",", "")),
                    "period": per, "end": f.end()}
        if f:  # "per month for 60 GB/day": a cap on the traffic, not a stored volume
            end = f.end()
        return {"kind": "flat", "unit": None, "qty": 1.0, "period": per, "end": end}
    m = _RE_OTHER.match(tail)
    if m and m.group("u").lower() not in _STOP:
        unit = m.group("u")
        end = m.end("u")
        u2 = m.group("u2")
        per = None
        if u2 and u2.lower() not in _STOP and not re.fullmatch(_PW, u2, re.I):
            unit, end = unit + " " + u2, m.end("u2")
        elif u2 and re.fullmatch(_PW, u2, re.I) and not re.fullmatch(_PW, unit, re.I):   # "per Linux minute"
            per, end = _period(None, u2), m.end("u2")
        p = re.compile(r"\s*(?:/|\bper\b|\ba\b)\s*(?:(?P<n>\d+)[-\s]?)?(?P<w>%s)\b" % _PW, re.I).match(tail, end)
        if p:
            per, end = _period(p.group("n"), p.group("w")), p.end()
        if re.fullmatch(_PW, unit, re.I):   # per month written as a unit word: "per vCPU-minute" is not, "per hour" is
            return {"kind": "flat", "unit": None, "qty": 1.0, "period": _period(None, unit), "end": end}
        return {"kind": "other", "unit": unit, "qty": float(m.group("q").replace(",", "")) if m.group("q") else 1.0,
                "period": per, "end": end}
    f = _RE_FOR.match(tail)
    if f and not f.group("rate"):
        return {"kind": "forvol", "unit": _unit(f.group("u")), "qty": float(f.group("q").replace(",", "")),
                "period": None, "end": f.end()}
    return {"kind": "bare", "unit": None, "qty": 1.0, "period": None, "end": 0}


def _usage_cue(window):
    """True when the window prices usage (egress, retrieval, operations ...) and does not say it is free."""
    for m in _USAGE_CHAIN.finditer(window):
        if _NEG_BEFORE.search(window[max(0, m.start() - 14):m.start()]) or _NEG_AFTER.match(window[m.end():m.end() + 25]):
            continue
        return True
    return False


def price_quotes(text, topic=None):
    """Every money amount in a price text with what it is quoted per and why it is not a storage price, if it is not.
    -> list of dict(amount, currency, kind, unit, qty, period, start, end, reject, once, approx), in text order.
    reject is None or a short reason; it is what price_claim() uses, and what a reviewer reads to see why a number was
    passed over. once marks a one-time or lifetime price, approx a figure written as "~" or "≈" (a conversion of another
    figure)."""
    s = text
    depth, d = [], 0
    for ch in s:
        depth.append(d)
        d += (ch == "(") - (ch == ")")
    depth.append(d)
    sents, pos = [], 0
    for m in _SENT.finditer(s):
        sents.append((pos, m.start()))
        pos = m.end()
    sents.append((pos, len(s)))
    quotes = []
    for m in _MONEY.finditer(s):
        if _RATE.match(s, m.end()):
            continue
        ccy = m.group("c1") or m.group("c2")
        ccy = SYM.get(ccy, ccy)
        amount = float((m.group("n1") or m.group("n2")).replace(",", ""))
        sp = _spec(s[m.end():m.end() + 90])
        end = m.end() + sp["end"]
        unit = sp["unit"].rstrip(".") if sp["unit"] else None
        quotes.append({"amount": amount, "currency": ccy, "kind": sp["kind"], "unit": unit, "qty": sp["qty"],
                       "period": sp["period"], "start": m.start(), "end": end, "reject": None, "once": False,
                       "approx": bool(re.search(r"(?:[≈~]|\babout|\bapprox\.?)\s*\(?\s*$", s[max(0, m.start() - 12):m.start()], re.I))})
    once_seen = False   # a sentence that opens with "one-time" or "lifetime" makes the sentences after it one-time too
    for q in quotes:
        a, b = next((x, y) for x, y in sents if x <= q["start"] <= y)
        first = next(m for m in _MONEY.finditer(s, a, b) if not _RATE.match(s, m.end()))
        why = cue = None
        head = s[a:first.start()]
        hc = _CUE.search(head)
        if hc:
            cue = hc.group(0).strip().lower()
            why = "the sentence opens with " + cue
            q["once"] = bool(_ONCE_RE.search(cue))
            once_seen = once_seen or q["once"]
        elif once_seen and q["period"] is None:
            why, q["once"] = "after a one-time or lifetime price, with no period", True
        if why is None:
            lo = a
            for m in _SOFT.finditer(s, a, q["start"]):
                if depth[m.start()] <= depth[q["start"]]:
                    lo = m.end()
            before = s[lo:q["start"]]
            hi, dq = b, depth[q["end"]]
            for m in _SOFT.finditer(s, q["end"], b):
                if depth[m.start()] <= dq:
                    hi = m.start()
                    break
            after, cur = s[q["end"]:hi][:80], dq
            for k, ch in enumerate(after):
                cur += (ch == "(") - (ch == ")")
                if cur < dq:
                    after = after[:k]
                    break
            win = before + "#" + after
            c = _CUE.search(win)
            if c:
                why = "near " + c.group(0).strip().lower()
                q["once"] = bool(_ONCE_RE.search(c.group(0)))
                once_seen = once_seen or q["once"]
            elif q["kind"] != "flat" and _usage_cue(win):   # a plan price per month stays one when its plan names egress
                why = "prices usage, not storage"
            elif _REGION.match(after) and q["kind"] == "vol":
                why = "a delivery price by region"
            elif q["kind"] == "vol" and q["period"] is None and re.match(r"\s*(?:beyond|above)\b", after, re.I):
                why = "an overage with no period"
            elif _INCR.search(s[max(0, q["start"] - 8):q["start"]]):
                why = "an add-on"
        q["reject"] = why
    # "$1.30/TB/mo at 10 TB, $0.65/TB/mo at 20 TB, $0.43/TB/mo at 30 TB (flat $12.99/mo 'Unlimited')": one flat price of
    # an unlimited plan divided by volumes the text picks. Two or more per-TB figures "at N TB" whose totals are the same
    # price, in a text that calls the plan flat or unlimited, are not a price per TB of the offer (live walk 2, W2-05):
    # the plan has no per-TB price, and the cheapest of them is only the largest volume picked. A server's price divided
    # by its raw and its usable disks ("at 64 TB raw ... at 48 TB RAID-5") is a price per TB of a fixed size, and stays
    if not _FLAT_PLAN.search(s):
        return quotes
    at = []
    for q in quotes:
        m = _AT_VOLUME.match(s, q["end"])
        if m and not q["reject"] and q["kind"] == "vol" and q["qty"] == 1 and q["unit"] in TB_OF:
            n = float(m.group(1).replace(",", "")) * TB_OF[m.group(2) if m.group(2) in TB_OF else "TB"] / TB_OF[q["unit"]]
            at.append((q, q["amount"] * n))
    if len(at) >= 2 and max(t for _, t in at) <= min(t for _, t in at) * 1.03:
        for q, _ in at:
            q["reject"] = "a flat price divided by a volume the text picks"
    return quotes


def _storage_month(q, month_default):
    """Price per TB-month of one quote in its own currency, or None when the quote is not a volume per month."""
    if q["kind"] not in ("vol", "forvol") or q["unit"] not in TB_OF:
        return None
    per = q["period"] or ("month" if month_default else None)
    if per not in MONTHS_OF:
        return None
    return q["amount"] / (q["qty"] * TB_OF[q["unit"]]) / MONTHS_OF[per]


def price_claim(rid, topic, text, read_date, fx):
    """The claim row of a record's price text: (rid, path, kind, num, unit, per, currency, usd, fx_date, parse).

    THE RULE. record.usd_per_tb_month is the price of one TB held or allowed for one month, in USD, and nothing else.
      * It is taken from a price the text states per TB (per TiB, divided by 1.0995) per month. The cheapest stated tier
        counts, and a stated per-TB figure beats one worked out from another unit.
      * Without one it is worked out exactly, from a price per GB or GiB-month (GB x 1000, GiB x 1e12/2^30), from a
        monthly price for a stated volume ("EUR 26.99 for 16 TB"), from a yearly one (divided by 12), from "30 days"
        (a month) and from a daily one (x 30). A figure with no period counts as monthly only in the topics whose price
        field is the price of a stored TB (storage, netdisk-pan); in the others it is a one-off price per TB, not a month.
      * It is converted with the dated rate of extras.fx for that currency. With no rate the claim keeps its currency
        and the USD is NULL: no rate is ever guessed.
      * It is never an operations price, an egress or retrieval fee, a total bill, a credit, a price per minute, hour,
        IP, domain, vCPU or account, a lifetime or one-time price (one price for ever is not a monthly price, and the
        horizon it would be spread over is the author's guess: a lifetime deal gets NULL), a promotional price (the
        text names the steady one), another vendor's price, a figure the text itself calls workload, all-in or
        effective, or a number in a text that says it has no per-TB price. A cheapest tier of zero is a free tier, and
        the headline skips a zero.
    Where the price is not a TB-month price the claim keeps its own unit and period, and never shows as TB-month:
      * kind 'price-per-tb' always means unit TB and period month, and feeds usd_per_tb_month;
      * kind 'price', unit None, period month, feeds usd_month (a monthly subscription; the extras prices of the same
        kind do too), when the text states a flat price per month (or per 30 days) and no TB-month price;
      * kind 'price' with any other unit or period (per GB, per IP, per year, a credit, no period at all) is only a
        claim: it feeds neither headline;
      * a number that was read but passed over (an egress fee, a lifetime price) is kind 'price' with parse 'partial',
        period 'once' for a one-time price, and feeds nothing;
      * a text with no money amount is kind 'price-per-tb', parse 'unparsed', every number NULL.
    """
    path = "$.price_per_tb_month"
    quotes = price_quotes(text, topic)
    if not quotes:
        return (rid, path, "price-per-tb", None, None, None, None, None, None, "unparsed")
    month_default = topic in MONTH_DEFAULT_TOPICS

    def usd_of(amount, ccy):
        return to_usd(amount, ccy, read_date, fx)

    def row(kind, q, num, unit, per, parse="ok"):
        usd, fxd = usd_of(num, q["currency"])
        return (rid, path, kind, round(num, 6), unit, per, q["currency"], usd, fxd, parse)

    good = [q for q in quotes if not q["reject"]]
    if not _NO_PER_TB.search(text):
        cands = []
        for q in good:
            v = _storage_month(q, month_default)
            if v is not None:
                tier = 1 if (q["kind"] == "vol" and q["unit"] in ("TB", "TiB") and q["qty"] == 1) else (
                    2 if q["kind"] == "vol" else 3)
                usd, fxd = usd_of(v, q["currency"])
                cands.append((tier, q["approx"], usd is None, usd if usd is not None else 0.0, len(cands), q, v))
        if cands:
            best = min(cands, key=lambda c: c[:5])
            return row("price-per-tb", best[5], best[6], "TB", "month")
    flats = []
    for q in good:
        if q["kind"] == "flat" and q["period"] == "month" and q["amount"] > 0:
            usd, _ = usd_of(q["amount"], q["currency"])
            flats.append((usd is None, usd if usd is not None else 0.0, len(flats), q))
    if flats:
        q = min(flats, key=lambda c: c[:3])[3]
        return row("price", q, q["amount"], None, "month")
    q = next((x for x in good if x["amount"] > 0), None) or next(iter(good), None)
    parse = "ok"
    if q is None:   # every number in the text was passed over: keep the first, marked as not the price of the record
        q = next((x for x in quotes if x["amount"] > 0), quotes[0])
        parse = "partial"
    unit = q["unit"]
    if unit and q["qty"] != 1:
        unit = "%s %s" % (("%d" % q["qty"]) if q["qty"] == int(q["qty"]) else ("%g" % q["qty"]), unit)
    return row("price", q, q["amount"], unit, "once" if q["once"] else q["period"], parse)


def claims_for(rid, o, read_date, fx):
    out = []
    ft = o.get("free_tier") or {}
    st = ft.get("stated")
    if isinstance(st, str):
        q = QTY.search(st)
        out.append((rid, "$.free_tier.stated", "free-quota", float(q.group(1).replace(",", "")) if q else None,
                    qty_unit(q.group(2)) if q else None, (q.group(3) or None) if q else None, None, None, None, "ok" if q else "unparsed"))
    pp = o.get("price_per_tb_month")
    if isinstance(pp, str):
        out.append(price_claim(rid, o.get("topic") or rid.split("/")[0], pp, read_date, fx))
    ex = o.get("extras") or {}
    for k in USD_KEYS:
        v = ex.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            # m10h_usd is the price of a machine run 10 hours a day (300 hours at the hourly rate): its own unit, so it
            # never reads as the price of a month
            out.append((rid, "$.extras." + k, "price", float(v), M10H_UNIT if k == "m10h_usd" else None, "month", "USD",
                        float(v), None, "ok"))
        elif v is not None:
            out.append((rid, "$.extras." + k, "price", None, None, None, None, None, None, "unparsed"))
    pop = ex.get("price_on_page")
    if isinstance(pop, str):
        # the monthly price the vendor's page prints ("EUR 4.99/mo or EUR 50.90/yr"): the cheapest flat price per month
        best = None
        for q in price_quotes(pop, o.get("topic")):
            if q["kind"] == "flat" and q["period"] == "month" and q["amount"] > 0 and not q["reject"]:
                usd, fxd = to_usd(q["amount"], q["currency"], read_date, fx)
                key = (usd is None, usd if usd is not None else 0.0)
                if best is None or key < best[0]:
                    best = (key, q, usd, fxd)
        if best:
            q = best[1]
            out.append((rid, "$.extras.price_on_page", "price", q["amount"], None, "month", q["currency"], best[2], best[3], "ok"))
    for i, lim in enumerate(o.get("limits") or []):
        val = lim.get("value") if isinstance(lim, dict) else None
        if not isinstance(val, str):
            continue
        q = QTY.search(val)
        out.append((rid, "$.limits[%d].value" % i, "limit:" + str(lim.get("kind")),
                    float(q.group(1).replace(",", "")) if q else None, qty_unit(q.group(2)) if q else None,
                    (q.group(3) or None) if q else None, None, None, None, "ok" if q else "unparsed"))
    return out


# a summary that opens by saying there is no free allowance: "no free tier", "no published free plan", the bare
# answer "None." or "No." to the question the field asks, or "Withdrawn." / "Discontinued." for an offer that ended
NO_FREE = re.compile(r"^\W*(?:no (?:published |perpetual )?free\b|(?:none|no|withdrawn|discontinued)\.(?:\s|$))", re.I)
# a text that says there is no free allowance anywhere in it: "states no free allowance", "with no free tier", "no
# free-quota figure", and a text that opens with a negation or a hedge
NEG_FREE = re.compile(r"\b(?:no|not|without|never)\s+(?:a\s+|any\s+)?(?:published\s+|perpetual\s+|recurring\s+)?free[\s-]+"
                      r"(?:tier|plan|allowance|quota|usage|offer|option)\b", re.I)
_OPENS_NEGATIVE = re.compile(r"^\W*(?:none|no|not|unverified|unknown)\b", re.I)
# the values of the compute records' extras.free_tier_kind that name a free plan: the facet of a record that has no
# extras.facets.free_tier_kind. A credit, a grant, a trial and 'none' are not read from it: there the free tier text
# decides, as before
FACET_FREE_PLAN = re.compile(r"^(?:free\b|always-free|perpetual|renewable(?:-free)?$|allowance$|monthly-(?:resource-)?allowance|"
                             r"monthly-vcpu-minute|capped-free|one-free-instance|fair-use-hosted)", re.I)
# a quantity that every account gets before anything is billed, in words other than 'free': "5 GB ... a month on every
# account; the allowance ... applies before anything is metered"
_ALLOWANCE = re.compile(r"\b(?:on|for|to|with) (?:every|each|all) accounts?\b|\bevery account (?:gets|has|includes|receives)\b|"
                        r"\bbefore anything is (?:metered|billed|charged)\b", re.I)
# a facet free_tier_kind that says there is nothing free now, and one that names a paid arrangement, not an allowance
FACET_NONE = re.compile(r"^(?:none|closed|dead)\b", re.I)
FACET_PAID = re.compile(r"^(?:paid-|prepaid|money-back|monthly-spending-discount)", re.I)
# words that state that something costs nothing: free, gratis, at no cost, a zero price, and the same in the languages
# the records quote. A free trial, a free period and a free transfer are not a free allowance of the offer: a trial is
# the verdict trial-only, and free egress on a paid plan is a property of that plan
_FREE_WORD = re.compile(
    r"\bfree\b|\bgratis\b|\bgratuit\w*|\bkostenlos\w*|\bno[- ]cost\b|\bzero[- ]cost\b|\bat no (?:charge|cost)\b|"
    r"\bcomplimentary\b|\bwithout charge\b|\bcosts? nothing\b|免费|無料|무료|бесплатн\w*|\bdarmow\w*|"
    r"(?<![\w.])(?:US)?[$€£¥]\s?0(?:[.,]0+)?(?![.,]?\d)|\b(?:USD|EUR|GBP|CNY|RMB|JPY|INR)\s?0(?:[.,]0+)?(?![.,]?\d)|"
    r"(?<![\w.,])0(?:[.,]0+)?\s?(?:yuan|元|USD|EUR|dollars?|euros?)\b", re.I)
_NOT_ALLOWANCE_AFTER = re.compile(
    r"\s*(?:trial|test\b|evaluation|for (?:the first )?\d+[- ]?(?:days?|weeks?|months?)\b|(?:of charge\s+)?"
    r"(?:egress|ingress|outbound|inbound|downloads?|traffic|bandwidth|transfers?|public[- ]link|api calls?|requests?)\b)", re.I)
_NOT_ALLOWANCE_BEFORE = re.compile(
    r"(?:\b(?:no|not|without|never|nor)\s+(?:a\s+|any\s+)?|(?:egress|ingress|outbound|inbound|download|traffic|bandwidth|transfer)s?"
    r"\s+(?:is\s+|are\s+)?)$", re.I)
# a trial: a time-boxed or one-time test of a paid plan, not a recurring allowance (the verdict trial-only)
_TRIAL = re.compile(r"\btrials?\b|\btest period\b", re.I)
# a sum of money given, not charged: a credit, a grant, a voucher
_GIVEN = re.compile(r"\bcredits?\b|\bgrants?\b|\bvouchers?\b|\bbonus\b|\bstipends?\b|\bfunding\b|\bsponsor\w*|\bprizes?\b|"
                    r"\bawards?\b|\bfellowship\b", re.I)
# a price that follows these words is an overage or an add-on beyond the allowance, not the price of the offer
_OVERAGE = re.compile(r"\b(?:then|beyond|after|extra|additional|over|above|add-?ons?|top-?ups?|overage|more|thereafter|"
                      r"plus|each)\b[^.;]*$", re.I)


def states_free(text):
    """True when a text says that something of the offer costs nothing: a free word that is not a trial, a free
    period or free traffic of a paid plan, and is not negated."""
    for m in _FREE_WORD.finditer(text or ""):
        if _NOT_ALLOWANCE_AFTER.match(text, m.end()) or _NOT_ALLOWANCE_BEFORE.search(text[max(0, m.start() - 30):m.start()]):
            continue
        return True
    return False


def priced_plan(stated, raw):
    """True when the headline offer of a record is a priced plan: the record is filed as a paid offer
    (extras.target_document under a paid/ folder), or its free tier text prices its own quantity (a price per month or
    per volume that is not an overage, an add-on, a credit or a grant)."""
    td = ((raw or {}).get("extras") or {}).get("target_document")
    if isinstance(td, str) and "/paid/" in td:
        return True
    if not stated or _GIVEN.search(stated):
        return False
    for q in price_quotes(stated):
        if q["amount"] > 0 and q["kind"] in ("flat", "vol", "forvol") and q["period"] \
                and not _OVERAGE.search(stated[max(0, q["start"] - 60):q["start"]]):
            return True
    return False


def free_allowance(o, summary, raw=None):
    """1, 0 or None: does the offer have a free allowance? The claim row 'has-free-tier' of the store says it, and
    a free list or a page template reads that row, not free_unit: free_unit is the unit of the HEADLINE offer, and
    a paid plan carries one too (the dossier schema says free_tier is "the headline offer", and the paid storage
    plans hold their plan size there). The claim is 1 only where a free allowance is stated.

      0     the verdict is paid-only (no free allowance, listed for its price) or dead; the record says so itself
            (its summary opens with 'no free ...', 'None.', 'No.' or 'Withdrawn.'; its facet free_tier_kind is none,
            closed or dead)
      1     the facet free_tier_kind names a free allowance; or the free tier names a unit other than none, and its
            text states that something costs nothing (states_free), that a credit or a grant is given, or that every
            account gets it before anything is billed, or the offer is neither a priced plan nor a trial; or the unit
            is none and the text states that a quantity costs nothing (a free word and a parsed quantity), says
            nowhere that there is no free tier, and is neither a priced plan nor a trial
      None  (unknown, no row) otherwise: the unit is none and the record does not say that there is nothing, or the
            headline offer is a priced plan (priced_plan) or a trial whose text states nothing free

    The facet is extras.facets.free_tier_kind of the projected record, or, where a record has none, the
    extras.free_tier_kind that the compute records carry in the same vocabulary. o is the projected record (its facets
    are extras.facets there); raw is the record as it is in dossier/, for the free tier text before projection and the
    filing of the record. Without raw the projected record is read."""
    if o.get("verdict") in ("paid-only", "dead"):
        return 0
    if NO_FREE.search(summary or ""):
        return 0
    src = raw if raw is not None else o
    facet = ((o.get("extras") or {}).get("facets") or {}).get("free_tier_kind")
    facet = facet.strip() if isinstance(facet, str) else ""
    if facet and FACET_NONE.match(facet):
        return 0
    if facet and not FACET_PAID.match(facet):
        return 1
    ft = src.get("free_tier") or {}
    unit = ft.get("unit")
    stated = ft.get("stated") if isinstance(ft.get("stated"), str) else ""
    kind = (src.get("extras") or {}).get("free_tier_kind")
    if not facet and isinstance(kind, str) and FACET_FREE_PLAN.match(kind.strip()) and not says_nothing_free(stated) \
            and not priced_plan(stated, src) and not (_trial(stated) and not states_free(stated)):
        return 1
    if unit and unit != "none":
        if states_free(stated) or _GIVEN.search(stated) or _ALLOWANCE.search(stated) or \
                not (priced_plan(stated, src) or _TRIAL.search(stated)):
            return 1
    elif unit == "none" and states_free(stated) and QTY.search(stated) and not says_nothing_free(stated) \
            and not (priced_plan(stated, src) or _trial(stated)):
        return 1
    return None


def says_nothing_free(stated):
    """True when a free tier text opens with a negation or a hedge ('none reachable for this client: ...', 'not
    stated: ...', 'unverified: ...', 'no multiplied allowance: ...') or says anywhere that there is no free tier."""
    return bool(_OPENS_NEGATIVE.match(stated or "") or NEG_FREE.search(stated or ""))


def _trial(stated):
    """A trial named in the text, and not as 'no trial'."""
    return any(not re.search(r"\b(?:no|not a|without a?)\s+(?:free\s+)?$", stated[max(0, m.start() - 12):m.start()], re.I)
               for m in _TRIAL.finditer(stated or ""))


def _usable(c):
    return c[9] == "ok" and c[7] is not None and c[7] > 0   # a zero is not a price to rank by: it comes from "unlimited" or "free" written as a rate


def stated_monthly(claims):
    """The monthly list prices a record states for its offer, in USD: extras.monthly_usd, the monthly price of
    extras.price_on_page, and a flat monthly price of the price text. usd_month is never below the cheapest of them."""
    return [c[7] for c in claims if _usable(c) and c[1] in STATED_MONTH_PATHS and c[2] == "price" and c[4] is None
            and c[5] == "month"]


def headline_prices(claims):
    """(usd_month, usd_per_tb_month): a zero never.

    usd_per_tb_month is the cheapest claim of kind price-per-tb in unit TB per month.
    usd_month is the price of the offer kept for a whole month: the cheapest monthly list price the record states
    (stated_monthly); without one, the price of the machine run 24 hours a day for a month (extras.m24h_usd); without
    that, the cheapest other claim of kind price, no unit, per month. The 10-hours-a-day figure (extras.m10h_usd) has
    its own unit and is never a monthly price, and the renewal price (extras.renewal_usd) is not one either: the
    records write it per month and per year."""
    usd_month = usd_tb = None
    for c in claims:
        if not _usable(c):
            continue
        if c[2] == "price-per-tb" and c[4] == "TB" and c[5] == "month":
            usd_tb = c[7] if usd_tb is None else min(usd_tb, c[7])
    stated = stated_monthly(claims)
    if stated:
        usd_month = min(stated)
    else:
        month = [c for c in claims if _usable(c) and c[2] == "price" and c[4] is None and c[5] == "month"
                 and c[1] != "$.extras.renewal_usd"]
        m24 = [c[7] for c in month if c[1] == "$.extras.m24h_usd"]
        rest = [c[7] for c in month if c[1] != "$.extras.m24h_usd"]
        usd_month = min(m24) if m24 else (min(rest) if rest else None)
    return usd_month, usd_tb


def price_violations(rid, claims, usd_month):
    """[(rid, text)]: usd_month is below a monthly list price that the record states, or it is the 10-hours-a-day
    figure. build.py --check fails on any."""
    out = []
    stated = stated_monthly(claims)
    if usd_month is not None and stated and usd_month < min(stated) - 1e-6:
        out.append((rid, "usd_month %s is below the monthly list price %s that the record states" % (usd_month, min(stated))))
    m10 = [c[7] for c in claims if c[1] == "$.extras.m10h_usd" and _usable(c)]
    m24 = [c[7] for c in claims if c[1] == "$.extras.m24h_usd" and _usable(c)]
    if usd_month is not None and m10 and m24 and abs(usd_month - m10[0]) < 1e-9 and m10[0] < m24[0] - 1e-6:
        out.append((rid, "usd_month %s is the 10-hours-a-day figure, below the 24-hours one %s" % (usd_month, m24[0])))
    return out


class Freshness:
    """Uses scripts/dossier/staleness.py so the store agrees with the gate by construction."""

    def __init__(self, repo):
        own = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dossier")
        sys.path.insert(0, own)
        import staleness  # noqa: E402
        self.s = staleness
        pol = os.path.join(repo, "scripts", "dossier", "staleness.policy.json")
        self.policy = staleness.load_policy(pol if os.path.exists(pol) else os.path.join(own, "staleness.policy.json"))

    def day(self, stamp, as_of):
        """The midnight UTC of the date of a verified_at, as an aware datetime; as_of when it does not parse."""
        v = self.s.parse_verified_at(stamp)
        return dt.datetime(v.year, v.month, v.day, tzinfo=dt.timezone.utc) if v else as_of

    def of(self, path, raw, as_of_date):
        as_of = dt.datetime(as_of_date.year, as_of_date.month, as_of_date.day, tzinfo=dt.timezone.utc)
        r = self.s.inspect_record(path, raw, self.policy, as_of)
        ev_limit = self.s.limits_for(self.policy, raw.get("topic"))["evidence_after_days"]
        lim = r["limit_days"]
        checked = None
        stale_on = None
        # stale_on is the first day a record is past its window: the gate counts a record stale when its age is
        # more than the window, so a record checked on day C with a window of L days is stale from C + L + 1.
        # "Stale on day D when stale_on <= D" then names the same day as the gate (R3-B-12)
        if r["verified_age_days"] is not None:
            # checked_on is a date: the UTC date of verified_at, or the older date a record that says it was not
            # re-checked declares, never after as_of. as_of minus the age is not it: the age is whole days between
            # as_of's midnight and an instant, one less than the days between the dates when verified_at has a time
            # of day, and that put checked_on one day after verified_at (a check on the day of the data read as the
            # next day)
            checked = min(as_of - dt.timedelta(days=max(r["verified_age_days"], 0)), self.day(raw.get("verified_at"), as_of))
            if lim is not None:
                stale_on = checked + dt.timedelta(days=lim + 1)
        if r["evidence_oldest_days"] is not None and ev_limit is not None:
            ev_stale = as_of - dt.timedelta(days=r["evidence_oldest_days"]) + dt.timedelta(days=ev_limit + 1)
            stale_on = ev_stale if stale_on is None else min(stale_on, ev_stale)
        basis = "inherited" if "declared-unchecked" in r["flags"] else "live"
        return {"limit_days": lim, "evidence_budget_days": ev_limit,
                "checked_on": checked.date().isoformat() if checked else None,
                "stale_on": stale_on.date().isoformat() if stale_on else None, "basis": basis}


HFIELD = re.compile(r"^\s*-\s+\*\*(When|Status|Supersedes|Superseded by|Evidence|Confidence):?\*\*:?\s*(.*)$")
NARRATIVE_H2 = re.compile(r"(?i)^#{2,3}\s+(what (?:it cost|a future session|is still open)|the transferable point|how we found it)")
DOSSREF = re.compile(r"(?:\.\./)*dossier/([a-z0-9-]+)/([a-z0-9-]+)(?:\.json)?")


def parse_history(repo, clean):
    """-> rows (hid, when, status, confidence, title, supersedes, body), links [(hid, rid)]."""
    rows, links = [], []
    base = os.path.join(repo, "history")
    for root, _, files in os.walk(base):
        for fn in sorted(files):
            if not fn.endswith(".md") or fn in ("README.md", "INDEX.md"):
                continue
            p = os.path.join(root, fn)
            txt = open(p, encoding="utf-8").read().replace("\r\n", "\n")
            hid = os.path.relpath(p, repo).replace("\\", "/")
            fields, title, body, keep = {}, None, [], True
            cur = None
            for ln in txt.split("\n"):
                if title is None and ln.startswith("# "):
                    title = ln[2:].strip()
                    continue
                m = HFIELD.match(ln)
                if m:
                    cur = m.group(1)
                    fields[cur] = m.group(2).strip()
                    continue
                if cur and ln.startswith("  ") and ln.strip() and not ln.lstrip().startswith("-"):
                    fields[cur] += " " + ln.strip()
                    continue
                cur = None
                if ln.startswith("## ") or ln.startswith("### "):
                    keep = not NARRATIVE_H2.match(ln)
                if keep:
                    body.append(ln)
            if not fields.get("When"):
                d = os.path.basename(root)
                m = re.match(r"(\d{4}-\d\d-\d\d)T(\d\d)(\d\d)(\d\d)Z", d)
                if m:
                    fields["When"] = "%sT%s:%s:%sZ" % m.groups()
            text = "\n".join(body).strip()
            text = re.sub(r"\]\((?:\.\./)*(?:history|\.tmp)/[^)]*\)", "]", text)
            ctext, _ = clean(text, "history.body") if text else (None, [])
            ctitle, _ = clean(title or "", "history.title")
            def first(k):
                w = (fields.get(k) or "").split()
                return (w[0].strip("`*.,") or None) if w else None
            rows.append((hid, fields.get("When"), first("Status"), first("Confidence"),
                         ctitle or os.path.splitext(fn)[0].replace("-", " ").capitalize(),
                         fields.get("Supersedes"), ctext))
            for m in sorted({(a, b) for a, b in DOSSREF.findall(txt)}):
                links.append((hid, "%s/%s" % m))
    return rows, links


def parse_ledger(repo):
    """history/ledger.jsonl (fr amend) plus history/ledger/<run>/<unit>.jsonl (one file per research unit)."""
    import glob
    paths = [os.path.join(repo, "history", "ledger.jsonl")] +         sorted(glob.glob(os.path.join(repo, "history", "ledger", "**", "*.jsonl"), recursive=True))
    rows = []
    for p in paths:
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            ev = o.get("evidence") or {}
            reason = o.get("reason")
            if o.get("op") and o.get("op") not in ("set",):
                reason = "%s%s" % (o["op"], (": " + reason) if reason else "")
            # the last column is the op of the line (set, confirm, append_evidence, drop_evidence, add_record, dead,
            # relate, undo, undo_skipped, basis); a line of fr amend, add or dead names none, and its op is NULL
            rows.append((o.get("at"), o.get("rid"), o.get("path"), json.dumps(o.get("old"), ensure_ascii=False),
                         json.dumps(o.get("new"), ensure_ascii=False), o.get("rung"), ev.get("url"), ev.get("date"),
                         ev.get("proved"), reason, o.get("op")))
    return rows


def parse_relations(repo):
    """registry/relations.tsv (fr relate) plus registry/relations.d/*.tsv (one file per research unit)."""
    import glob
    dup, edges = {}, []
    for p in [os.path.join(repo, "registry", "relations.tsv")] +             sorted(glob.glob(os.path.join(repo, "registry", "relations.d", "*.tsv"))):
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8"):
            if not ln.strip() or ln.startswith("#") or ln.startswith("src\t"):
                continue
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 3:
                edges.append((c[0], c[2], c[1]))
                if c[1] == "duplicate_of":
                    dup[c[0]] = c[2]
    return dup, edges


def captures(repo):
    p = os.path.join(repo, "sources", "MANIFEST.tsv")
    rows = []
    if os.path.exists(p):
        lines = open(p, encoding="utf-8").read().splitlines()
        hdr = lines[0].split("\t")
        for ln in lines[1:]:
            c = dict(zip(hdr, ln.split("\t")))
            if c.get("url") and "pkgforge" not in c["url"] and "ajam" not in c["url"]:
                rows.append((c["url"], c.get("captured_at"), c.get("path"), c.get("sha256")))
    return rows


VOCAB = [
    ("verdict", "qualifies", "usable as stated; the read path was probed"),
    ("verdict", "qualifies-with-caveat", "usable, with a named limit or an unprobed read path"),
    ("verdict", "trial-only", "a time-boxed or one-time trial, not a recurring allowance"),
    ("verdict", "paid-only", "no free allowance; listed for its price"),
    ("verdict", "fails-identity", "the identity required is not reachable without it"),
    ("verdict", "fails-egress", "data cannot be read back out at a usable rate or price"),
    ("verdict", "fails-quota", "the free allowance is too small to matter"),
    ("verdict", "dead", "the offer or the service no longer exists"),
    ("grp", "usable", "verdict qualifies or qualifies-with-caveat"),
    ("grp", "trial", "verdict trial-only"),
    ("grp", "paid", "verdict paid-only"),
    ("grp", "rejected", "verdict fails-identity, fails-egress or fails-quota"),
    ("grp", "dead", "verdict dead"),
    ("self_hosted", "0", "a hosted offer: free, trial or paid"),
    ("self_hosted", "1", "the user installs, runs and maintains it; every list puts it after every hosted record"),
    ("confidence", "measured", "a live request was made and its output kept"),
    ("confidence", "documented", "a first-party page was read and the sentence quoted"),
    ("confidence", "reported", "a third party said so"),
    ("confidence", "inferred", "reasoned from other evidence"),
    ("confidence", "unverified", "asserted and not checked"),
    ("binding", "request-rate", "requests per unit of time"),
    ("binding", "pull-count", "number of downloads or pulls"),
    ("binding", "per-ip-shaping", "bandwidth shaped per address or port"),
    ("binding", "per-object-cap", "largest single object"),
    ("binding", "write-gated", "writes need approval, payment or a gate"),
    ("binding", "retention-clamped", "data is deleted after a period"),
    ("binding", "volume-quota", "total stored or transferred volume"),
    ("binding", "none", "no named constraint binds"),
    ("identity_kind", "anonymous", "nothing is asked for"),
    ("identity_kind", "email", "an email address"),
    ("identity_kind", "any-phone", "a phone number from any country"),
    ("identity_kind", "country-phone", "a phone number from a named country"),
    ("identity_kind", "national-id", "a government identity document"),
    ("identity_kind", "card", "a payment card"),
    ("identity_kind", "institution", "membership of a university, lab or company"),
    ("identity_basis", "stated", "the identity requirement was read from a source"),
    ("identity_basis", "defaulted", "the identity kind is a placeholder; card and phone are unknown"),
    ("identity_basis", "inferred", "the kind, or the card or phone requirement, was inferred, not read; card and phone are unknown"),
    ("verified_basis", "live", "the record was checked against the service"),
    ("verified_basis", "inherited", "carried from an earlier source; checked_on is an upper bound"),
]


def vocab_rows(rules):
    rows = []
    order = collections.Counter()
    for d, t, m in VOCAB:
        rows.append((d, t, order[d], m))
        order[d] += 1
    for cls, meaning in rules["templates"]["meaning"].items():
        rows.append(("unknown_class", cls, order["unknown_class"], meaning))
        order["unknown_class"] += 1
    # every class that the public unknown rows use has a meaning here: a page prints the meaning, not the bare word
    for cls, meaning in (("private-url", "the source is a private copy and its public address is not known"),
                         ("withheld", "the value held no technical content and is not published"),
                         ("partly-held", "a clause of the value is not published; the rest is"),
                         ("boilerplate", "the value was a sentence repeated across many records with no finding of its own, and is not published"),
                         ("interface-unknown", "the access interface was not established"),
                         ("egress-unknown", "egress metering was not published"),
                         ("identity-defaulted", "the identity kind is a placeholder")):
        rows.append(("unknown_class", cls, order["unknown_class"], meaning))
        order["unknown_class"] += 1
    return rows
