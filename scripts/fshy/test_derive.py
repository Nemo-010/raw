#!/usr/bin/env python3
"""test_derive.py: the identity flags, the identity basis, the free-allowance claim, the build-minute quota and the
check dates (checked_on, stale_on) of scripts/fshy/derive.py.

The cases are frozen texts (FIXED, below: the fields derive reads of a record of dossier/, copied on 2026-10-31 and
keyed by the record id) and a few synthetic details for the classes. No case reads a record of dossier/, so a record
change never fails this selftest; a change of derive.py or of the projection rules does. Standard library only. Exit 0
when every case passes, 1 otherwise.

  python scripts/fshy/test_derive.py [-v]
"""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import derive  # noqa: E402

RULES = json.load(open(os.path.join(HERE, "rules", "projection.json"), encoding="utf-8"))
FAILED = []
PASSED = [0]
VERBOSE = "-v" in sys.argv


def check(name, cond, detail=None):
    if cond:
        PASSED[0] += 1
        if VERBOSE:
            print("ok    " + name)
    else:
        FAILED.append(name)
        print("FAIL  %s%s" % (name, ("  -- " + str(detail)[:300]) if detail is not None else ""))
    return cond


def record(rid):
    """The frozen text of a record: a deep copy, so a case cannot change another's input."""
    return json.loads(json.dumps(FIXED[rid]))


def ident(rid):
    r = derive.identity(record(rid), RULES)
    return r["identity_basis"], r["needs_card"], r["needs_phone"]


def synthetic(kind, detail, **extras):
    return {"identity_cost": {"kind": kind, "detail": detail}, "extras": extras}


def main():
    # F-17: an unverified requirement is NULL, an upgrade-only requirement is not the offer's, a stated no is 0
    check("groq: a card is for the upgrade only, the phone step is not stated", ident("inference/groq") == ("stated", 0, None), ident("inference/groq"))
    check("gemini api: billing is for a paid tier, the phone step is not stated",
          ident("inference/google-gemini-api") == ("stated", 0, None), ident("inference/google-gemini-api"))
    check("openrouter: the phone step is unverified", ident("inference/openrouter-free-ids")[2] is None, ident("inference/openrouter-free-ids"))
    check("mistral: free mode needs no credit card, the phone step is not stated",
          ident("inference/mistral-la-plateforme") == ("stated", 0, None), ident("inference/mistral-la-plateforme"))
    check("netlify ai gateway: card and phone at signup are unverified, so both are NULL",
          ident("inference/netlify-ai-gateway") == ("stated", None, None), ident("inference/netlify-ai-gateway"))
    check("webshare: the free plan needs no card although the paid plans do", ident("debrid/webshare")[1] == 0, ident("debrid/webshare"))
    # review of #166: a free plan that is not the record's own offer does not make the record card-free
    def kind_flags(rid):
        r = derive.identity(record(rid), RULES)
        return r["identity_kind"], r["needs_card"], r["needs_phone"]
    check("webshare static residential: paid-only, and its free plan is 'a separate datacenter offer and not this "
          "product': card, needs_card 1", kind_flags("ip-proxy/webshare-static-residential") == ("card", 1, 0),
          kind_flags("ip-proxy/webshare-static-residential"))
    check("sst: paid-only; only the Console sign-up is card-free, the capacity needs a card: card, needs_card 1",
          kind_flags("compute/sst") == ("card", 1, 0), kind_flags("compute/sst"))
    check("cloudvps: a trial that needs only a form, with the card for the paid catalogue: email, no card",
          kind_flags("compute/cloudvps") == ("email", 0, 0), kind_flags("compute/cloudvps"))
    paid = derive.identity({"verdict": "paid-only", "identity_cost": {"kind": "card", "detail": "card for paid plans. The free plan needs no card."}}, RULES)
    check("guard 1: a paid-only record keeps the card kind and needs_card 1 whatever its free plan says",
          (paid["identity_kind"], paid["needs_card"]) == ("card", 1), paid)
    other = derive.identity({"verdict": "qualifies", "identity_cost": {"kind": "card", "detail": (
        "card for this plan. The account's free plan needs no card, but it is a separate datacenter offer and not this product.")}}, RULES)
    check("guard 2: a free plan that the clause calls another offer or product is not this record's: card, needs_card 1",
          (other["identity_kind"], other["needs_card"]) == ("card", 1), other)
    check("guard 2 reads 'another product' and 'a separate ... offer', not a plan of the same offer",
          derive.OTHER_OFFER.search("the free plan is another product") and derive.OTHER_OFFER.search("a separate datacenter offer")
          and not derive.OTHER_OFFER.search("The free plan needs no card, the paid plans do."))
    for rid in ("compute/chutes", "inference/api-airforce", "ip-proxy/mullvad-vpn"):
        check("%s: an anonymous record that says no card and no phone has neither flag" % rid, ident(rid)[1:] == (0, 0), ident(rid))
    check("a card kind is a card", derive.identity(synthetic("card", "card"), RULES)["needs_card"] == 1)
    check("a phone kind is a phone", derive.identity(synthetic("any-phone", "a phone number"), RULES)["needs_phone"] == 1)
    check("a stated card requirement is 1", derive.identity(synthetic("email", "an email and a credit card on file"), RULES)["needs_card"] == 1)
    check("a stated phone requirement is 1", derive.identity(synthetic("email", "an email and an SMS code"), RULES)["needs_phone"] == 1)
    check("'no card hold is stated' makes the hold unknown, not required",
          derive.identity(synthetic("email", "an email only. A card hold is not stated."), RULES)["needs_card"] is None)
    check("'no card-free path' is a card requirement",
          derive.identity(synthetic("card", "USD 5 of credit is offered after adding a card; the pricing page states no card-free path"), RULES)["needs_card"] == 1)
    check("a detail that never names a card or a phone is 0 for both, as before",
          ident_of(synthetic("email", "an email address and a password")) == ("stated", 0, 0))

    # blind test 2 (F-03): the flags agree with the record's own words
    def full(rid):
        r = derive.identity(record(rid), RULES)
        return r["identity_kind"], r["identity_basis"], r["needs_card"], r["needs_phone"]
    check("stepfun: 'a phone number is not required' is no phone; no free route, so the card kind is a card",
          full("coding-subs/stepfun-step-plan") == ("card", "stated", 1, 0), full("coding-subs/stepfun-step-plan"))
    check("brevo: 'whether a phone number ... is also required is unverified' is unknown, whatever the forum reports",
          full("email/brevo") == ("email", "stated", 0, None), full("email/brevo"))
    check("bitbucket pipelines: 'whether the Free sign-up form asks for a card is unverified' is unknown",
          full("compute/bitbucket-pipelines") == ("email", "stated", None, 0), full("compute/bitbucket-pipelines"))
    check("mailgun: the free plan needs no card and a mobile phone: the published kind is the free plan's, not card",
          full("email/mailgun") == ("any-phone", "stated", 0, 1), full("email/mailgun"))
    check("webshare: the free plan needs no card: the published kind is email, never 'card' beside 'no card'",
          full("debrid/webshare") == ("email", "stated", 0, 0), full("debrid/webshare"))
    # an inferred kind alone stays stated, with the flags the detail states; an inferred card or phone fact is inferred
    check("botkeep: only the email kind is inferred ('the email kind is inferred ... rather than read'): stated",
          full("compute/botkeep") == ("email", "stated", 0, None), full("compute/botkeep"))
    check("cratedb cloud: the email requirement is inferred, the vendor's 'no credit card required' is read: stated, no card",
          full("compute/cratedb-cloud") == ("email", "stated", 0, 0), full("compute/cratedb-cloud"))
    check("iranget: 'email as the minimum is inferred' is an inferred kind: stated",
          full("debrid/iranget")[1] == "stated", full("debrid/iranget"))
    check("ouicu: 'email is inferred from the absence of any phone or card requirement' infers the kind: stated, no card, "
          "no phone", full("egress/ouicu") == ("email", "stated", 0, 0), full("egress/ouicu"))
    check("venice ai: 'the card kind is inferred from the credit purchase rather than quoted' is an inferred card: inferred",
          full("compute/venice-ai") == ("card", "inferred", None, None), full("compute/venice-ai"))
    check("github actions: 'No card and no hold, but this half is inferred rather than quoted' is an inferred card: inferred",
          full("compute/github-actions")[1:] == ("inferred", None, None), full("compute/github-actions"))
    check("sunny usenet: '... a payment method is captured at signup ... That is inferred' points back to the card: inferred",
          full("debrid/sunny-usenet")[1:] == ("inferred", None, None), full("debrid/sunny-usenet"))
    ir = derive.inferred_requirement
    check("a phone requirement inferred is an inferred requirement", ir("an email; the phone requirement is inferred from the region"))
    check("an account inferred is not", not ir("The signup fields are not quoted, so the email requirement is inferred rather than read"))
    check("google cloud run: 'not an account without a card' says a card is needed",
          full("egress/google-cloud-run") == ("card", "stated", 1, 0), full("egress/google-cloud-run"))
    check("gitlab runners: free with no card, 'but the free compute minutes sit behind a card', is a card",
          full("compute/gitlab-runners")[0::2] == ("card", 1), full("compute/gitlab-runners"))
    check("sambanova: a no-card free tier that a page 'still describes, which contradicts the plans page' is not the offer",
          full("compute/sambanova-cloud")[0::2] == ("card", 1), full("compute/sambanova-cloud"))
    for rid in FIXED:
        if "identity_cost" in FIXED[rid]:
            k, b, c, _ = full(rid)
            check("%s: the published kind is never card beside needs_card 0" % rid, not (k == "card" and c == 0), full(rid))
    syn = lambda kind, det: ident_of(synthetic(kind, det))[1:]
    check("'is not required' and 'are not needed' are negations",
          syn("email", "an email; a credit card is not required and SMS codes are not needed") == (0, 0))
    check("'does not ask for a phone' and 'no mobile number field' are negations",
          syn("email", "the form does not ask for a phone") == (0, 0) and syn("email", "No mobile number field appears") == (0, 0))
    check("'cannot be used without a credit card' is a card requirement, not a negation",
          syn("email", "an email; the service cannot be used without a credit card") == (1, 0))
    check("a hedge on a detail of the card, not on the requirement, leaves a stated requirement",
          syn("email", "a credit card is required at signup. Whether debit cards are accepted is unverified") == (1, 0))
    d = derive.identity(synthetic("card", "card for paid plans. The free plan needs no card; a phone number verified by SMS is required"), RULES)
    check("a card kind whose free plan needs no card but a phone publishes the phone kind",
          (d["identity_kind"], d["needs_card"], d["needs_phone"]) == ("any-phone", 0, 1), d)

    # F-08: a kind worked out from the prose or a category is not a stated identity
    check("an identity derived from the record's prose is inferred, with unknown flags",
          derive.identity(synthetic("institution", "derived from the record's prose, not from an identity field, and no signup was executed: x"), RULES)
          == {"identity_kind": "institution", "identity_basis": "inferred", "needs_card": None, "needs_phone": None,
              "needs_id": None, "needs_institution": None, "country": None})
    check("storage/internet-archive: institution is inferred, not stated", ident("storage/internet-archive")[0] == "inferred", ident("storage/internet-archive"))
    check("storage/filebase: institution is inferred, not stated", ident("storage/filebase")[0] == "inferred", ident("storage/filebase"))
    check("an identity inferred from a category is not a stated one",
          derive.identity(synthetic("institution", "inferred from the category 'academic'; the source record states no identity cost, so this is a class assumption, not evidence"), RULES)["identity_basis"] != "stated")
    d = derive.identity(synthetic("institution", "x", identity_cost_defaulted=True), RULES)
    check("a defaulted identity has unknown flags, the institution kind included",
          (d["identity_basis"], d["needs_institution"], d["needs_card"]) == ("defaulted", None, None), d)
    check("storage/mega: email defaulted keeps NULL flags", ident("storage/mega") == ("defaulted", None, None), ident("storage/mega"))
    check("the vocabulary names the three bases", {t for dom, t, _ in derive.VOCAB if dom == "identity_basis"} == {"stated", "inferred", "defaulted"})

    # U-03: the free allowance of a record
    fa = derive.free_allowance
    check("paid-only has no free allowance, whatever unit its offer is denominated in",
          fa({"verdict": "paid-only", "free_tier": {"unit": "GiB"}}, "EUR 3.90/month for 20 GB") == 0)
    check("a summary that opens with 'no free tier' says there is none",
          fa({"verdict": "qualifies-with-caveat", "free_tier": {"unit": "none"}}, "No free tier; the plans start at JPY 460") == 0)
    check("'no published free tier' and 'no perpetual free tier' say there is none",
          fa({"verdict": "qualifies", "free_tier": {"unit": "none"}}, "no published free tier") == 0
          and fa({"verdict": "qualifies", "free_tier": {"unit": "none"}}, "no perpetual free tier") == 0)
    check("a dead offer has no free allowance now", fa({"verdict": "dead", "free_tier": {"unit": "GB"}}, "5 GB free") == 0)
    check("a named unit is a free allowance", fa({"verdict": "qualifies", "free_tier": {"unit": "GB"}}, "5 GB free") == 1)
    check("a facet that names a free allowance counts when the unit is none",
          fa({"verdict": "qualifies", "free_tier": {"unit": "none"}, "extras": {"facets": {"free_tier_kind": "one-time-credit"}}}, "USD 5 credit") == 1)
    check("a facet that says none is none",
          fa({"verdict": "qualifies", "free_tier": {"unit": "GB"}, "extras": {"facets": {"free_tier_kind": "none"}}}, "5 GB") == 0)
    check("unit none and nothing said is unknown, not no",
          fa({"verdict": "qualifies", "free_tier": {"unit": "none"}}, "free for individual developers; bring your own API key") is None)
    check("the unit of a free tier is not said to be free: a pan drive with no free tier but a TiB unit",
          fa({"verdict": "qualifies", "free_tier": {"unit": "TiB"}}, "No free tier. Pay-as-you-go in two pools") == 0)

    # live walk 2 (W2-01): the claim is 1 only where a free allowance is stated; a paid plan's size is not one
    def fr(rid):
        r = record(rid)
        return fa(r, r["free_tier"]["stated"], r)
    check("storage/hetzner-sx65-2-dedicated-storage-server: a dedicated server's disks are not a free allowance",
          fr("storage/hetzner-sx65-2-dedicated-storage-server") is None, fr("storage/hetzner-sx65-2-dedicated-storage-server"))
    check("storage/pulsedmedia-m10g-storage-box: a price ladder filed as a paid offer is not a free allowance",
          fr("storage/pulsedmedia-m10g-storage-box") is None)
    check("storage/blomp: a paid record whose free tier text says '40 GB free' has a free allowance", fr("storage/blomp") == 1)
    check("storage/jottacloud-unlimited: 'Free 5 GB tier exists' on a paid plan is a free allowance", fr("storage/jottacloud-unlimited") == 1)
    check("databases-kv/cloudflare-d1: a free tier stated in its own units, with an overage price elsewhere, is a free allowance",
          fr("databases-kv/cloudflare-d1") == 1)
    plan = lambda stated, **kw: fa({"verdict": "qualifies", "free_tier": {"unit": "TB", "stated": stated}}, stated,
                                   {"verdict": "qualifies", "free_tier": {"unit": "TB", "stated": stated}, "extras": kw})
    check("a free tier text that prices its own sizes is a priced plan: unknown", plan("250 GB $3/mo, 500 GB $4/mo, 1 TB $6/mo") is None)
    check("a record filed as a paid offer, with no free word, is unknown",
          plan("1 / 2 / 4 / 8 TB HDD", target_document="docs/storage/paid/storage-boxes.md") is None)
    check("a price after 'then' is an overage beyond a free allowance", plan("10 GB of storage, then USD 0.02 per GB-month") == 1)
    check("free egress on a priced plan is not a free allowance", plan("16 TB with free egress, EUR 26.99/month") is None)
    check("a free trial is not a free allowance", plan("a 7-day free trial, then EUR 4/month") is None)
    check("a trial with no free word is unknown", plan("A 7-day trial of every plan") is None)
    check("a credit given is a free allowance", plan("USD 90 of one-time credit, then USD 5/month") == 1)
    check("a zero price is free", plan("Hobby is USD 0 a month with 100 GB") == 1 and plan("Trial edition, 0 yuan per year: 1 G a month") == 1)
    check("'not free' is not free", plan("50 GB on Starter, but Starter is $35/month, NOT free") is None)
    check("a summary that answers 'None.' says there is none", fa({"verdict": "qualifies", "free_tier": {"unit": "GB"}}, "None. Vouchers only.") == 0)
    check("a facet that says the programme is closed is none",
          fa({"verdict": "qualifies", "free_tier": {"unit": "hours"}, "extras": {"facets": {"free_tier_kind": "closed"}}}, "x") == 0)
    check("a facet that names a paid arrangement is not a free allowance",
          fa({"verdict": "qualifies", "free_tier": {"unit": "none"}, "extras": {"facets": {"free_tier_kind": "paid-fellowship"}}}, "x") is None)

    # blind test 2 (F-02): a free quantity that the record states is a free allowance; a trial, a credit-only text, a
    # priced plan and a text that says there is nothing stay as the rules above keep them
    def frs(rid):
        r = record(rid)
        st = r["free_tier"]["stated"]
        return fa(r, (st[:157] + "...") if len(st) > 160 else st, r)
    check("storage/tigris: 5 GB a month 'on every account ... before anything is metered', filed as a paid document, is a free allowance",
          frs("storage/tigris") == 1, frs("storage/tigris"))
    check("compute/sillydev-free: unit none, but its own free_tier_kind is always-free", frs("compute/sillydev-free") == 1)
    check("compute/coalbyte-free: unit none, but its text says 'kostenlos' of a stated quantity", frs("compute/coalbyte-free") == 1)
    check("compute/opus-host-free: unit none, '0,00 € dauerhaft kostenlos' of 1 vCPU, 1 GB RAM", frs("compute/opus-host-free") == 1)
    check("egress/pagekite: a trial of 2.5 GB is not a free allowance (the trial rule keeps it unknown)", frs("egress/pagekite") is None)
    check("debrid/megaseed-kz: a free tier text that opens 'Withdrawn.' says there is none", frs("debrid/megaseed-kz") == 0)
    check("compute/alibaba-ack: a free_tier_kind of allowance over a text that opens 'not stated' is not a free allowance",
          frs("compute/alibaba-ack") is None)
    check("netdisk-pan/lanzou-premium: 'No free-quota figure is published' is not a free allowance", frs("netdisk-pan/lanzou-premium") is None)
    check("compute/zo-computer: a free_tier_kind of trial is not read as a free plan", frs("compute/zo-computer") is None)
    plain = lambda stated, unit="none", **kw: fa({"verdict": "qualifies", "free_tier": {"unit": unit, "stated": stated}}, stated,
                                                 {"verdict": "qualifies", "free_tier": {"unit": unit, "stated": stated}, "extras": kw})
    check("a free_tier_kind of allowance over a priced plan is not a free allowance",
          plain("25 hours a month included with a membership of USD 99 a year", "hours", free_tier_kind="allowance") is None)
    check("unit none and a text that opens 'none reachable for this client' stays unknown",
          plain("none reachable for this client: the free plan is 5 GB/day") is None)
    check("unit none and a free text with no quantity stays unknown", plain("free for individual developers") is None)
    check("'no trial' is not a trial", derive._trial("No card, no trial, no expiry") is False and derive._trial("a 7-day trial") is True)

    # blind test 2 (F-08): a free allowance counted in build or CI minutes is a free-quota claim in 'build minutes',
    # the unit the CI need reads; general compute minutes and hours are not
    def quota(stated):
        c = [x for x in derive.claims_for("compute/x", {"free_tier": {"stated": stated}}, None, {}) if x[2] == "free-quota"]
        return tuple(c[0][3:6]) if c else None
    for stated, want, what in (
            ("2,500 build-minutes a month per billing account on e2-standard-2 (2 vCPU, 8 GB memory) in the default pool, "
             "stated as a promotional free tier whose limit is subject to change; the first 100 GB of worker SSD is free",
             (2500.0, "build minutes", "month"), "compute/google-cloud-build: '2,500 build-minutes a month', not its 8 GB of memory"),
            ("50 build minutes a month on the Free plan, at $0 for up to 5 users, with 1 GB of Git LFS storage in total, up to 100 "
             "steps per pipeline and up to 10 concurrent steps; no overage protection on Free",
             (50.0, "build minutes", "month"), "compute/bitbucket-pipelines: '50 build minutes a month', not its 1 GB of LFS"),
            ("100 total build minutes per month on general1.small or arm1.small (on-demand EC2), and 6,000 total build seconds "
             "per month on lambda.arm.1GB or lambda.x86-64.1GB (on-demand Lambda)",
             (100.0, "build minutes", "month"), "compute/aws-codebuild: '100 total build minutes per month', not a 1GB in a SKU"),
            ("2,000 CI minutes per month", (2000.0, "build minutes", "month"), "CI minutes are build minutes"),
            ("idle apps scale to zero after 30 minutes", (30.0, "minutes", None), "a plain minute stays a minute, not a build minute"),
            ("40 GPU hours a month", (40.0, "GPU hours", "month"), "GPU hours keep their unit")):
        check(what, quota(stated) == want, quota(stated))

    # live walk 2 (W2-13): every class of a public unknown row has a meaning in the vocabulary, boilerplate among them
    terms = {t for dom, t, _, _ in derive.vocab_rows(RULES) if dom == "unknown_class"}
    used = set(RULES["templates"]["meaning"]) | {"boilerplate", "private-url", "withheld", "partly-held", "interface-unknown",
                                                 "egress-unknown", "identity-defaulted"}
    check("every unknown class the projection and the build write has a meaning in vocab", used <= terms, used - terms)

    freshness_cases()

    print("%d checks, %d failed" % (PASSED[0] + len(FAILED), len(FAILED)))
    return 1 if FAILED else 0


def freshness_cases():
    """blind test 2 (F-01): checked_on is the UTC date of verified_at, never after the data date, and stale_on counts
    from it. The records are synthetic; the windows are the shipped policy's, read back from the result."""
    fresh = derive.Freshness(os.path.join(HERE, "..", ".."))
    as_of = dt.date(2026, 10, 31)

    def of(verified_at, evidence=("2026-10-30",), **extras):
        raw = {"topic": "inference", "confidence": "documented", "verified_at": verified_at, "extras": extras,
               "evidence": [{"url": "https://example.invalid/%d" % i, "date": d, "proved": "a fact"} for i, d in enumerate(evidence)]}
        return fresh.of("x.json", raw, as_of)

    def after(day, n):
        return (dt.date.fromisoformat(day) + dt.timedelta(days=n)).isoformat()
    f = of("2026-10-31T00:12:52.378Z")
    check("a check made on the data date, after midnight, is checked on that date, not the next (inference/groq)",
          f["checked_on"] == "2026-10-31" and f["stale_on"] == after("2026-10-31", f["limit_days"] + 1), f)
    f = of("2026-10-25T13:00:00.000Z")
    check("a check with a time of day is checked on its own UTC date", f["checked_on"] == "2026-10-25"
          and f["stale_on"] == after("2026-10-25", f["limit_days"] + 1), f)
    f = of("2026-10-25T00:00:00.000Z")
    check("a check at midnight is checked on its date", f["checked_on"] == "2026-10-25", f)
    f = of("2026-11-02T08:00:00.000Z")
    check("a verified_at after the data date is never a checked_on after it", f["checked_on"] == "2026-10-31", f)
    f = of("2026-10-30T12:00:00.000Z", verified_at_basis="not re-checked in this pass", source_pass_ended="2026-10-20")
    check("a record that says it was not re-checked is checked on the date it declares",
          f["checked_on"] == "2026-10-20" and f["basis"] == "inherited", f)
    f = of("2026-10-30T12:00:00.000Z", evidence=("2026-10-30", "2026-01-15"))
    check("the oldest evidence binds stale_on from its own date",
          f["stale_on"] == min(after("2026-01-15", f["evidence_budget_days"] + 1), after("2026-10-30", f["limit_days"] + 1)), f)


def ident_of(raw):
    r = derive.identity(raw, RULES)
    return r["identity_basis"], r["needs_card"], r["needs_phone"]


# ------------------------------------------------------------------------------------------ the frozen texts

# rid -> the fields of the record that derive reads for its case: identity_cost (and extras.identity_cost_defaulted)
# for the identity cases; verdict, free_tier and the extras free_allowance reads (facets.free_tier_kind,
# target_document) for the free-allowance cases. Copied from dossier/ at main 1c90ad48 on 2026-10-31.
FIXED = {
    "inference/groq": {
        "identity_cost": {
            "kind": "email",
            "detail": ("an account and an API key; a payment method (credit card, US bank account or SEPA debit account) is "
                       "required to upgrade from the Free tier to the Developer tier. unverified: the sign-in methods and any "
                       "phone requirement are not stated on the docs pages"),
            "country": None}},
    "inference/google-gemini-api": {
        "identity_cost": {
            "kind": "email",
            "detail": ("a default Google Cloud project and API key are created by AI Studio when a new user accepts the Terms "
                       "of Service; billing must be set up to move from the Free tier to a paid tier; available only in the "
                       "countries and territories listed on the available-regions page. unverified: the sign-in method and "
                       "any phone requirement are not stated on those pages"),
            "country": None}},
    "inference/openrouter-free-ids": {
        "identity_cost": {
            "kind": "email",
            "detail": ("an account and an API key. An unauthenticated call is refused with 'No cookie auth credentials "
                       "found'. Free-model requests are available below 10 credits purchased at 50 requests per day. "
                       "unverified: the account sign-in methods and any card or phone step are not stated on the docs pages"),
            "country": None}},
    "inference/mistral-la-plateforme": {
        "identity_cost": {
            "kind": "email",
            "detail": ("a Mistral account and an API key; Free mode needs no credit card. unverified: whether account "
                       "creation or key activation asks for a phone number is not stated on the docs pages"),
            "country": None}},
    "inference/netlify-ai-gateway": {
        "identity_cost": {
            "kind": "email",
            "detail": ("a Netlify account on the Free plan, which is '$0 forever'; card and phone at signup are unverified on "
                       "the pages read here"),
            "country": None}},
    "debrid/webshare": {
        "identity_cost": {
            "kind": "card",
            "detail": "Account at the dashboard; card. The free plan needs no card, the paid plans do.",
            "country": None}},
    # the record's wording at main 3fe98bf1 (2026-10-31), which names the free plan another product
    "ip-proxy/webshare-static-residential": {
        "verdict": "paid-only",
        "identity_cost": {
            "kind": "card",
            "detail": ("Card: a plan is paid with a card (Visa, Mastercard, American Express, Discover, Diners, China "
                       "UnionPay, JCB, Cartes Bancaires or Interac) or with Google Pay or Apple Pay on a mobile device, and "
                       "the vendor names no other payment method. The account is opened with an email and a password or with "
                       "a Google account. An ID check through Stripe Identity is not a purchase gate, but it may be "
                       "requested later to confirm the payment method or a use case. The account’s free plan needs no "
                       "card, but it is a separate datacenter offer and not this product."),
            "country": None}},
    "compute/sst": {
        "verdict": "paid-only",
        "identity_cost": {
            "kind": "card",
            "detail": ("the card belongs to the AWS account, not to the Console: the record's own limits row reads that \"the "
                       "capacity itself is gated by the AWS account behind it, which needs a card\", while the docs state "
                       "\"the Console is completely free to get started and an account can be created without a credit "
                       "card\", with billing details needed only above 350 active resources a month, where production and "
                       "deployed stages block until they are added. So signing up for the free Console tier takes no card "
                       "and no hold exists there, and no compute is obtained either, because the Console contributes no "
                       "runtime; the record does not state what the Console signup asks for — an email or a GitHub "
                       "account — nor the AWS account's card terms, debit or prepaid acceptance"),
            "country": None}},
    "compute/cloudvps": {
        "verdict": "trial-only",
        "identity_cost": {
            "kind": "card",
            "detail": ("the free seven-day test needs an application form and nothing else that is stated: the trial page "
                       "says choose a configuration and fill in a simple form, with credentials arriving by email once the "
                       "application is checked, and it names no card, phone or identity document. The card statement "
                       "belongs to the paid catalogue, where payment \"is accepted by international and Russian cards in any "
                       "currency\"; no hold or authorisation is stated, whether debit or prepaid cards are accepted is not "
                       "stated, and whether the trial repeats once per person is not established"),
            "country": None}},
    "compute/chutes": {
        "identity_cost": {
            "kind": "anonymous",
            "detail": ("nothing beyond a chosen username: 'You can sign up with Google or GitHub, or just pick a username and "
                       "Chutes mints a fingerprint credential', and 'Connecting a Bittensor wallet is optional; you do not "
                       "need one to use the platform'. No email, no phone, no card and no ID is required on that path, which "
                       "is why the kind is anonymous rather than email. No hold exists because no payment method is taken at "
                       "signup; debit and prepaid acceptance are not stated, and paying for tokens afterwards is not "
                       "described."),
            "country": None}},
    "inference/api-airforce": {
        "identity_cost": {
            "kind": "anonymous",
            "detail": ("a free account with a username and a password: no email and no card required to start, and the API "
                       "key is generated in the dashboard. The g4f.dev provider page states the free tier is available "
                       "without an API key and its JavaScript example sends no Authorization header; a keyless completion was "
                       "not exercised"),
            "country": None}},
    "ip-proxy/mullvad-vpn": {
        "identity_cost": {
            "kind": "anonymous",
            "detail": ("No email is asked for at signup: the pricing page says 'Start with one click to generate an account. "
                       "You'll immediately get an account number and be able to choose a payment option.' Payment runs from "
                       "cash by post to card - 'We accept cash, Bitcoin, Bitcoin Cash, Monero, bank wire, credit card, "
                       "PayPal, Swish, Eps transfer, Bancontact, iDEAL | Wero, and Przelewy24' - and 'Our accepted "
                       "cryptocurrencies are discounted at 10% due to lower fees and less administration.' No card is "
                       "required: a card is one option among many, and the anonymous paths cost nothing extra; the crypto "
                       "paths cost 10% less."),
            "country": None}},
    "storage/internet-archive": {
        "identity_cost": {
            "kind": "institution",
            "detail": ("derived from the record's prose, not from an identity field, and no signup was executed: ems (zip "
                       "counts as 1); recommended <=10,000 files/item but API accepts 250,000; DELETE bucket not allowed; S3 "
                       "Range headers ignored; only HTTP/1.1 REST, no ACLs; every upload enters"),
            "country": None}},
    "storage/filebase": {
        "identity_cost": {
            "kind": "institution",
            "detail": ("derived from the record's prose, not from an identity field, and no signup was executed: th, object "
                       "egress free. Pro $7.50/mo: 500 GB pooled. S3 API held up live: the public gateway served the test CID "
                       "at 200 (414,201 bytes, Server: Filebase) but throttled during a ra"),
            "country": None}},
    "storage/mega": {
        "identity_cost": {
            "kind": "email",
            "detail": ("no identity_cost field and no identity statement in the source record; defaulted to email and "
                       "flagged, not evidence"),
            "country": None},
        "extras": {
            "identity_cost_defaulted": True}},
    # blind test 2 (F-03): copied from dossier/ at main 3fe98bf1 on 2026-10-31
    "coding-subs/stepfun-step-plan": {
        "identity_cost": {
            "kind": "card",
            "detail": ("registration takes an email address with an emailed verification code, or a Google account; the "
                       "platform sign-in form offers 'Continue with Google' and 'Email verification code login', and a phone "
                       "number is not required. There is no free route: use needs a paid subscription, and the checkout "
                       "offers 'Pay with Stripe' (credit or debit card; the Step Plan page FAQ names Visa and Mastercard, the "
                       "console subscription page FAQ names Alipay, UnionPay, Visa and Mastercard, plus corporate bank "
                       "transfer for enterprises) or 'Pay with balance' (the account balance, topped up by credit or debit "
                       "card). Whether the checkout asks for a billing address, a country or an identity check: unverified: "
                       "behind a sign-up"),
            "country": None}},
    "email/brevo": {
        "identity_cost": {
            "kind": "email",
            "detail": ("Signup asks for an email and a password, or a Google or Apple sign-in, with no card; the account then "
                       "verifies the email and asks for basic business information. Whether a mobile phone number with an SMS "
                       "code is also required is unverified: behind a sign-up; users on the vendor's community forum report a "
                       "phone number and SMS code step during registration. A sender on a free domain such as gmail.com cannot "
                       "be authenticated, and the vendor states that mail from a free address is rejected or filtered to spam, "
                       "so delivery needs a domain the sender controls."),
            "country": None}},
    "compute/bitbucket-pipelines": {
        "identity_cost": {
            "kind": "email",
            "detail": ("an Atlassian account; the Free plan covers up to 5 users, and the billing documentation charges a "
                       "credit card on file only for monthly Standard or Premium plans after a 30-day evaluation; whether the "
                       "Free sign-up form asks for a card is unverified: the form renders client-side"),
            "country": None}},
    "email/mailgun": {
        "identity_cost": {
            "kind": "card",
            "detail": ("Signup asks for a work email, a full name and a company; every account is then activated by an email "
                       "link and a mobile phone number verified by an SMS one-time password, and VoIP, virtual and landline "
                       "numbers are refused. No card is needed to open a Free plan account, but without a card on file it "
                       "sends only to authorized recipients; a card on file unlocks custom domains, which send to any "
                       "recipient."),
            "country": None}},
    "compute/botkeep": {
        "identity_cost": {
            "kind": "email",
            "detail": ("an account is required and the free plan 'is for new signups', with the terms allowing 'up to two "
                       "server slots per account'. What the account requires is not quoted in any evidence row: no email, "
                       "phone, card or ID requirement is stated, and the email kind is inferred from an account-based signup "
                       "rather than read. The record's notes assert there is no card. No hold, debit or prepaid term is "
                       "stated."),
            "country": None}},
    "egress/google-cloud-run": {
        "identity_cost": {
            "kind": "card",
            "detail": ("A Google Cloud billing account with a payment method; the free tier is a billing discount, not an "
                       "account without a card."),
            "country": "None"}},
    "compute/gitlab-runners": {
        "identity_cost": {
            "kind": "card",
            "detail": ("A card, for the thing this record is about. The account itself is free and the pricing page says 'No "
                       "credit card required' for the Free plan, but the free compute minutes sit behind a card: "
                       "'credit/debit card details are required if you choose to use GitLab.com shared runners'. The card is "
                       "verified by 'a one-dollar authorization transaction' and 'No charge will be made and no money will "
                       "transfer', so the hold is USD 1.00 authorised and released, not captured. GitLab's "
                       "identity-verification page adds a second, independent gate that is risk-scored: 'All users - Email "
                       "verification. Medium-risk users - Phone number verification. High-risk users - Credit card "
                       "verification.' Whether a new account lands in the medium or high band is not published. Debit "
                       "acceptance is not stated on any page read; the pages say 'credit/debit card' without "
                       "distinguishing."),
            "country": None}},
    "compute/sambanova-cloud": {
        "identity_cost": {
            "kind": "card",
            "detail": ("a payment method and purchased credits before the first request: the plans page reads \"Add a "
                       "payment method and purchase credits to run your first requests\", and the previous USD 5 no-card "
                       "grant was dropped on 2026-08-14. The record does not name which payment methods are accepted, whether "
                       "a card is required rather than another rail, any hold, debit or prepaid acceptance, or whether signup "
                       "asks for an email or a phone. The rate-limit documentation still describes a \"Free Tier: Applied "
                       "when there is no payment method linked with your account\", which contradicts the plans page"),
            "country": None}},
    "compute/cratedb-cloud": {
        "identity_cost": {
            "kind": "email",
            "detail": ("no card: the pricing page states 'Free plan with 2 vCPUs, 2 GB RAM, and 8 GB storage (no credit card "
                       "required)'. No hold exists because no payment method is taken on the free plan. The signup fields are "
                       "not quoted, so the email requirement is inferred rather than read, and debit and prepaid acceptance "
                       "are not stated."),
            "country": None}},
    "compute/venice-ai": {
        "identity_cost": {
            "kind": "card",
            "detail": ("an account for the Free plan ('Sign Up for Free', 10 text prompts and 15 image prompts a day) and "
                       "credits for API calls: the docs state 'API requests are pay-per-use at the rates on this page. There "
                       "is no unmetered API tier. A Free account can call the API, and those requests are billed at the same "
                       "rates', and the plan grid marks API access 'pay with credits'. No evidence row states that a card is "
                       "required to buy those credits, and no hold, debit or prepaid term is stated, so the card kind is "
                       "inferred from the credit purchase rather than quoted. The record's notes add that the "
                       "pay-per-request-in-USDC lane needs no account at all."),
            "country": None}},
    "compute/github-actions": {
        "identity_cost": {
            "kind": "email",
            "detail": ("'To get started with GitHub.com, you need to have a personal account and a verified email address.' "
                       "No phone: 'If you have been selected for mandatory 2FA, that does not mean you have to provide GitHub "
                       "with your phone number.' No card and no hold, but this half is inferred rather than quoted, and the "
                       "inference is stated: GitHub never writes 'no payment method is needed for public-repo Actions'. What "
                       "the pages do say is that the card block is conditional on a quota being used up ('If your account "
                       "does not have a valid payment method on file, usage is blocked once you use up your quota'), that "
                       "public-repo standard runners are not billed at all, and that the always-charged products are the "
                       "exception ('Larger runners are always charged for' and 'Usage of larger runners is always blocked "
                       "until you set up a payment method'). A product that bills nothing has no quota to exhaust, so no "
                       "card is demanded to use it. That is a documented absence, not a documented exemption, and it is one "
                       "signup away from being settled."),
            "country": None}},
    "debrid/sunny-usenet": {
        "identity_cost": {
            "kind": "card",
            "detail": ("The free week is delivered through a signup product named 'SunnyUNLAnnualRecurringWithTrial', which "
                       "is an annual recurring subscription with a trial attached, so a payment method is captured at signup "
                       "even though the first week is free. That is inferred from the product id, not observed at checkout."),
            "country": None}},
    "egress/ouicu": {
        "identity_cost": {
            "kind": "email",
            "detail": ("an Account page exists and ouicu whoami is documented, and the free plan is stated to need no card; "
                       "the signup mechanism itself was not observed, so email is inferred from the absence of any phone or "
                       "card requirement"),
            "country": "None"}},
    "debrid/iranget": {
        "identity_cost": {
            "kind": "email",
            "detail": "A customer account on the shop; the registration form was not read, so email as the minimum is inferred.",
            "country": "Iran"}},
    # blind test 2 (F-02): copied from dossier/ at main 3fe98bf1 on 2026-10-31
    "storage/tigris": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "GB",
            "stated": ("5 GB of Standard-tier storage, 10,000 Class A requests (PUT, COPY, POST, LIST) and 100,000 Class B "
                       "requests (GET, SELECT and all other) a month on every account; the allowance resets monthly, covers "
                       "the Standard tier only and applies before anything is metered")},
        "extras": {
            "target_document": "docs/storage/paid/object-storage.md"}},
    "compute/sillydev-free": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "none",
            "stated": ("'25% of a CPU core, 256 MB of memory, and 512 MB of disk', 'No card, no trial, no expiry', 'We do not "
                       "sleep idle containers and we do not cap how many hours a month you run.' Plus '2 databases per "
                       "account, 50 MB each' on MariaDB or PostgreSQL.")},
        "extras": {
            "free_tier_kind": "always-free"}},
    "compute/coalbyte-free": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "none",
            "stated": ("'Starte deinen garantierten kostenlosen Server mit 3 GB RAM, 1 vCPU und 8 GB Speicher in unter 60 "
                       "Sekunden'; '100% Dauerhaft kostenlos'; 'Keine Kreditkarte nötig'. The Discord-bot page states a "
                       "different free allocation: '1024 MB RAM · 1 vCPU Dedicated' with '1.1 GB / 5 GB NVMe'.")}},
    "compute/opus-host-free": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "none",
            "stated": ("'1 vCPU, 1 GB RAM und 20 GB SSD - kostenlos nach Admin-Freigabe' and '0,00 € dauerhaft kostenlos'. "
                       "The page's own plan object gives cores 1, memory_mb 1024, disk_gb 20, ipv4 1, ipv6 1, runtime_days "
                       "30, price_cents 0, is_free true, is_free_unique 1.")}},
    "egress/pagekite": {
        "verdict": "trial-only",
        "free_tier": {
            "unit": "GB",
            "stated": "Trial period: 31 days & 2.5 GB"}},
    "debrid/megaseed-kz": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "none",
            "stated": ("Withdrawn. The free-seedbox page still describes it (20 GB HDD, 3 active torrents, limited speed, no "
                       "FTP) but opens with 'Выдача бесплатных сидбоксов остановлена!' (issuance of free seedboxes has "
                       "stopped).")}},
    "compute/alibaba-ack": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "none",
            "stated": "not stated: https://www.alibabacloud.com/product/kubernetes prints no free allowance, credit or price for ACK"},
        "extras": {
            "free_tier_kind": "allowance"}},
    "netdisk-pan/lanzou-premium": {
        "verdict": "fails-quota",
        "free_tier": {
            "unit": "none",
            "stated": ("Smaller than legacy Lanzou. The product is the paid successor to the free tier, and the per-file cap "
                       "is above the legacy 100 MB. No free-quota figure is published")}},
    "compute/zo-computer": {
        "verdict": "trial-only",
        "free_tier": {
            "unit": "none",
            "stated": ("a 14-day free trial with limited usage and 100 GB of cloud storage, holding 1 unit; after the trial "
                       "the account drops to recovery only, and paid plans from $10 keep Zo awake with memory across sessions")},
        "extras": {
            "free_tier_kind": "trial"}},
    "storage/hetzner-sx65-2-dedicated-storage-server": {
        "verdict": "qualifies",
        "free_tier": {
            "unit": "TB",
            "stated": "4× 16 TB SATA = 64 TB raw; 48 TB usable at RAID-5 (4× 22 TB = 88 TB raw available as SX65-1/-3)"},
        "extras": {
            "target_document": "docs/storage/paid/storage-boxes.md"}},
    "storage/pulsedmedia-m10g-storage-box": {
        "verdict": "qualifies",
        "free_tier": {
            "unit": "TB",
            "stated": "4 / 8 / 16 / 32 TB tiers. 16 TB = €26.99/month, monthly billing. 32 TB = €63.99/month."},
        "extras": {
            "target_document": "docs/storage/paid/lifetime-and-deals.md"}},
    "storage/blomp": {
        "verdict": "qualifies",
        "free_tier": {
            "unit": "GB",
            "stated": ("40 GB free on signup, advertised and confirmed as 'Get Up to 400 GB for Free' — +40 GB per friend who "
                       "joins and stays active, i.e. 40 GB x 10 referrals = 400 GB. Referral ceiling 400 GB is a hard stop on "
                       "a single account; past that you buy (500 GB $11.88/yr, 2 TB $2.99/mo, 10 TB $9.99/mo).")},
        "extras": {
            "target_document": "docs/storage/free/media-and-archives.md"}},
    "storage/jottacloud-unlimited": {
        "verdict": "qualifies-with-caveat",
        "free_tier": {
            "unit": "GB",
            "stated": "Unlimited storage; 1 user. Free 5 GB tier exists."},
        "extras": {
            "target_document": "docs/storage/paid/lifetime-and-deals.md"}},
    "databases-kv/cloudflare-d1": {
        "verdict": "qualifies",
        "free_tier": {
            "unit": "mixed",
            "stated": ("10 databases; 500 MB per database; 5 GB per account; 5 million rows read per day; 100,000 rows "
                       "written per day")}},
}


if __name__ == "__main__":
    sys.exit(main())
