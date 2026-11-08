#!/usr/bin/env python3
"""Selftest for the price parser (scripts/fshy/derive.py: price_claim, claims_for, headline_prices).

The rule under test: record.usd_per_tb_month is the price of one TB held or allowed for one month and nothing else.
An operations price, an egress or retrieval fee, a total bill, a per-minute, per-IP or per-domain price, a yearly price
shown as monthly, a lifetime deal spread over an assumed horizon and a credit never land there.

Four kinds of check, none of which types a price of its own: the exact cases of the review, each built from a frozen
text (FIXED, below: what claims_for reads of a record of dossier/, copied on 2026-10-31, keyed by the record id, and
the text a record held before a run corrected it, keyed rid@earlier); synthetic strings for each unit class; the
agreement of the parser with the per-TB figures that every frozen text states; and invariants over every record of
dossier/ that hold for any text (the shape of each claim and the claim kinds). The cases read no record of dossier/
and the exchange rates are frozen too (FX), so a record change never fails this selftest; a change of the parser does.

usage: python scripts/fshy/test_prices.py     exit 0 all pass, 1 a check failed
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import derive  # noqa: E402

FAILS = []
VERBOSE = "-v" in sys.argv
PATH = "$.price_per_tb_month"
TIB = 2 ** 40 / 1e12          # TB in a TiB: a price per TiB divided by this is the price per TB
GIB = 2 ** 30 / 1e12


def check(name, cond, detail=""):
    if not cond:
        FAILS.append(name)
    if VERBOSE or not cond:
        print("%s  %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + str(detail)[:400]) if detail and not cond else ""))
    return cond


def near(a, b, rel=0.005, absolute=0.0005):
    return a is not None and b is not None and abs(a - b) <= max(absolute, rel * abs(b))


def read_date(raw):
    """What build.py passes: the newest evidence date of the record (a frozen text carries its own)."""
    if "read_date" in raw:
        return raw["read_date"]
    dates = sorted(e["date"] for e in raw.get("evidence") or [] if isinstance(e, dict) and e.get("date"))
    return dates[-1] if dates else None


def priced(key):
    """(price claim row, usd_month, usd_per_tb_month) of a frozen text, through claims_for and headline_prices."""
    raw = FIXED[key]
    claims = derive.claims_for(key.split("@")[0], raw, read_date(raw), FX)
    um, ut = derive.headline_prices(claims)
    row = next(c for c in claims if c[1] == PATH)
    return row, um, ut


def synth(text, topic="storage", date="2026-10-24"):
    """The same for a string typed here."""
    row = derive.price_claim("%s/synthetic" % topic, topic, text, date, FX)
    um, ut = derive.headline_prices([row])
    return row, um, ut


def rate(ccy, key=None, date=None):
    usd, _ = derive.to_usd(1.0, ccy, date or (read_date(FIXED[key]) if key else None), FX)
    return usd


def text_of(key):
    return FIXED[key]["price_per_tb_month"]


# ------------------------------------------------------------------------------------------ the exact cases

# (the key of a frozen text, a string that text states, the USD per TB-month it must give). A record whose price a run
# corrected has two cases: its text now, and its text before the correction (rid@earlier), each with its own value.
STATED = [
    ("storage/cachefly-object-storage", "$25/TB stored", 25.0),
    ("storage/telnyx-object-storage", "USD 0.006 per GiB a month for US storage", 0.006 / GIB),
    ("storage/telnyx-object-storage@earlier", "$6.14/TB stored", 6.14),
    ("storage/utho-archive-storage-0-38-gb-mo-cold-tier-denominated-no", "$4.10/TB/mo", 4.10),
    ("storage/hosting-mammoth-object-storage", "$5.62/TB at 5 TB", 5.62),
    ("storage/datalix-s3-object-storage", "$4.44/TB at 5 TB", 4.44),
    ("storage/filen-pro-x", "$4.49/TB at 10 TiB", 4.49),
    ("storage/mega-s4", "$4.18/TB at 20 TB", 4.18),
    ("storage/kyun-host-bricks", "$5.62/TB/mo flat", 5.62),
    ("storage/hostbrr-storage-vps-hdd-block", "$5.00/TB/mo at the 1 TB block rate", 5.0),
    ("storage/prismdrive-10-tb-annual", "$2.075/TB/mo", 2.075),
    ("storage/pikpak", "$0.50/TB/mo on US Premium", 0.5),
    ("storage/sia-storage-app", "$2.00/TB at 10 TB tier", 2.0),
    ("storage/hetzner-object-storage", "storage beyond it EUR 0.0087 per TB-hour, about EUR 6.47 per TB", None),
    ("storage/hetzner-object-storage@earlier", "$8.06/TB at 5 TB stored", 8.06),
    ("storage/hetzner-storage-box", "$2.28/TB at 20 TB", 2.28),
    ("storage/ovhcloud-cold-archive", "USD 1.84 per TB per month (USD 0.001971 per GiB-month", 1.84),
    ("storage/ovhcloud-cold-archive@earlier", "$1.44/TB at 20 TB", 1.44),
    ("storage/blomp", "$1.00/TB/mo at 10 TB", 1.0),
    ("storage/drime", "$3.00/TB at 6 TB subscription", 3.0),
    ("storage/koofr", "$7.86/TB at 5 TB", 7.86),
    ("storage/pcloud-ultra-10-tb", "$2.999/TB/mo at 10 TB annual", 2.999),
    ("storage/time4vps-storage-vps", "$9.38/TB/mo at renewal", 9.38),
    ("storage/bunny-net-edge-storage", "$10/TB stored", 10.0),
    ("storage/cdn77-object-storage", "$20/TB stored", 20.0),
    ("storage/akamai-linode-object-storage", "USD 0.02 per GB a month (about USD 20 per TB)", 20.0),
    ("storage/akamai-linode-object-storage@earlier", "$20/TB stored", 20.0),
    ("storage/beget-s3-free-egress-s3-at-350-mbit-s-the-only-russian-o", "$26.04/TB/mo", 26.04),
    ("storage/storj-object-storage-standard", "USD 7.00 per TB-month of storage on the Standard plan", 7.0),
    ("storage/storj-object-storage-standard@earlier", "$7.00/TB at 5 TB and 20 TB for storage", 7.0),
    ("storage/file-kiwi-web-folder", "$30.36/TB/mo", 30.36),
    ("netdisk-pan/telnyx-cloud-storage-egress-view", "USD 6.14/TB/month", 6.14),
    ("netdisk-pan/hetzner-storage-share", "EUR 2.74/TB/month", 2.74 * 1.0),   # EUR: converted below
    ("storage/openai-files-api-per-project-file-storage", "$0.10/GB/day", 0.10 * 1000 * 30),
    ("databases-kv/cloudflare-d1", "USD 0.75/GB-month", 750.0),
    ("databases-kv/pinecone", "USD 0.33/GB-month storage", 330.0),
    ("databases-kv/dynamodb", "USD 0.25/GB-month", 250.0),
    ("databases-kv/upstash-redis", "USD 0.25/GB-month", 250.0),
    ("storage/together-ai-files-api", "$0.16/GiB/mo", 0.16 / GIB),
]
EUR_CASES = [   # stated in euro: the USD is the euro figure at the dated rate of the frozen FX rows
    ("storage/datalix-s3-compatible-object-storage", "€3.95/TB/mo", 3.95),
    ("storage/hetzner-storage-box-bx41", "€2.03/TB/mo at the 20 TB tier (€40.60/20)", 40.60 / 20),
    ("storage/hetzner-storage-box-bx21", "€2.18/TB/mo at 5 TB", 2.18),
    ("storage/pulsedmedia-m10g-storage-box", "€1.69/TB/mo at the 16 TB tier (€26.99/16)", 26.99 / 16),
    ("storage/pulsedmedia-m10g-storage-box-16tb", "€26.99 -> €1.69/TB/mo", 26.99 / 16),
    ("storage/hetzner-storage-box-bx11-bx21-bx31", "€2.03/TB", 2.03),
    ("storage/hostbrr-storagebox-16tb", "€2.00/TB/mo", 2.0),
]


def exact_cases():
    for rid, must, want in STATED:
        if rid not in FIXED:
            check("%s has a frozen text" % rid, False)
            continue
        t = text_of(rid)
        if not check("%s still states %r" % (rid, must), must in t, t):
            continue
        row, um, ut = priced(rid)
        if want is None:
            want = 6.47 * rate("EUR", rid)   # hetzner object storage, corrected: EUR 6.47 per TB beyond the base
        if rid == "netdisk-pan/hetzner-storage-share":
            want = 2.74 * rate("EUR", rid)
        ok = near(ut, want, 0.002)
        check("%s: usd_per_tb_month %s, wanted %.4f" % (rid, ut, want), ok, row)
        check("%s: its claim is price-per-tb, unit TB, period month" % rid,
              row[2] == "price-per-tb" and row[4] == "TB" and row[5] == "month", row)
    for rid, must, eur in EUR_CASES:
        t = text_of(rid)
        if not check("%s still states %r" % (rid, must), must in t, t):
            continue
        row, um, ut = priced(rid)
        want = eur * rate("EUR", rid)
        check("%s: usd_per_tb_month %s is EUR %.4f at the repository's rate (%.4f)" % (rid, ut, eur, want),
              near(ut, want, 0.006), row)
        check("%s: the claim keeps the euro figure" % rid, row[6] == "EUR" and row[3] is not None and near(row[3], eur, 0.006), row)
    # the worked cases whose text states the whole offer, not only a per-TB figure
    rid = "storage/hosting-mammoth-object-storage"
    row, um, ut = priced(rid)
    check("hosting-mammoth: EUR 4.99 a TB-month at the FX row is within 1%% of the stated $5.62 (%s)" % ut,
          near(ut, 4.99 * rate("EUR", rid), 0.01), row)
    for rid in ("storage/ovhcloud-cold-archive", "storage/ovhcloud-cold-archive@earlier"):
        row, um, ut = priced(rid)
        if "USD 1.84 per TB per month" in text_of(rid):
            check("ovh cold archive: not the EUR 5/TB retrieval fee (%s), the corrected storage rate, USD 1.84/TB" % ut,
                  ut is not None and ut < 2 and near(ut, 1.84, 0.002), row)
        else:
            check("ovh cold archive: not the EUR 5/TB retrieval fee (%s), the storage rate, EUR 0.00128/GB-month = EUR 1.28/TB" % ut,
                  ut is not None and ut < 2 and near(ut, 1.28 * rate("EUR", rid), 0.01), row)
    rid = "storage/hetzner-storage-box-bx41"
    row, um, ut = priced(rid)
    check("hetzner bx41: EUR 40.60 for 20 TB is about 2.27 a TB-month, not the monthly total", near(ut, 40.60 / 20 * rate("EUR", rid), 0.006) and ut < 3, row)
    for rid in ("storage/hetzner-object-storage", "storage/hetzner-object-storage@earlier"):
        row, um, ut = priced(rid)
        check("hetzner object storage%s: not the EUR 146.16 / $164.19 total of 20 TB" % (" (earlier text)" if "@" in rid else ""),
              ut is not None and ut < 10, row)
    rid = "storage/together-ai-files-api"
    row, um, ut = priced(rid)
    check("together-ai: $0.16 per GiB-month is %.2f per TB-month, a GiB is not a GB" % (0.16 / GIB), near(ut, 0.16 / GIB, 1e-4) and row[3] is not None, row)


def null_cases():
    """Records whose price text is not a TB-month price at all: usd_per_tb_month is NULL, and the claim says what it is."""
    for rid in ("storage/bright-data-residential-network", "storage/packetstream", "storage/frontproxy",
                "databases-kv/turso", "databases-kv/prisma-postgres", "databases-kv/tidb-cloud-starter",
                "storage/ieee-dataport-data-competition-module", "storage/load-network-load-s3",
                "storage/proxyrack-unlimited-residential", "storage/sellfy", "storage/upzur-premium",
                "compute/mitos", "egress/google-cloud-free-tier", "egress/aws-global-accelerator", "egress/cosmic-guard",
                "egress/upvpn", "egress/akamai-cloud-linode", "egress/azure-free-account", "egress/hyehost-ipv4-tunnels",
                "ip-proxy/oxylabs-isp-proxies", "ip-proxy/soax-mobile", "ip-proxy/proxidize-mobile",
                "debrid/bestdebrid", "debrid/turbobitpremium-org", "debrid/cubenet", "debrid/uploadflix",
                "debrid/blocknews", "debrid/usenet-farm", "debrid/nopremium-pl", "debrid/oxylabs", "debrid/decodo",
                "domains-dns/cloudflare-registrar", "domains-dns/porkbun", "domains-dns/spaceship",
                "ci-cd-runners/buildkite-free", "ci-cd-runners/github-actions-private"):
        row, um, ut = priced(rid)
        check("%s: usd_per_tb_month is NULL (%s)" % (rid, ut), ut is None, (row, text_of(rid)))
        check("%s: its claim is not shown as a TB-month price" % rid,
              not (row[2] == "price-per-tb" and row[3] is not None), row)
        check("%s: and is not a claim in unit TB per month" % rid, not (row[4] == "TB" and row[5] == "month"), row)
    # live walk 2 (W2-05): a flat plan divided by volumes the text picks has no price per TB; real tiers keep theirs
    row, um, ut = synth("$1.30/TB/mo at 10 TB, $0.65/TB/mo at 20 TB, $0.43/TB/mo at 30 TB (flat $12.99/mo 'Unlimited')")
    check("a flat plan divided by picked volumes is not a TB-month price; the flat monthly price is usd_month",
          ut is None and um == 12.99, row)
    row, um, ut = priced("storage/jottacloud")
    check("storage/jottacloud: the 'Unlimited' plan has no price per TB (was 0.43 at an assumed 30 TB)", ut is None, (row, text_of("storage/jottacloud")))
    row, um, ut = synth("$1.00/TB/mo at 10 TB ($9.99) and at 100 TB ($99.99); $1.50/TB/mo at 2 TB ($2.99)")
    check("tiers whose totals differ are real tiers: the cheapest per-TB tier stays", near(ut, 1.0), row)
    row, um, ut = priced("storage/hetzner-sx65-2-dedicated-storage-server")
    check("a server's price divided by its raw and its usable disks is a per-TB price of a fixed size, and stays",
          ut is not None and ut < 2, (row, text_of("storage/hetzner-sx65-2-dedicated-storage-server")))
    # lifetime deals: one price for ever is not a monthly price; the amortised figure of the record is never taken
    for rid in ("storage/internxt-lifetime", "storage/internxt-100-tb-lifetime", "storage/icedrive-lifetime-personal-2-tb",
                "storage/filelu", "storage/pcloud-premium-plus-2-tb-ultra-10-tb",
                "storage/scramble-cloud-premium-6-tb-lifetime", "storage/drime-secure-cloud-storage-10-tb-lifetime"):
        t = text_of(rid)
        row, um, ut = priced(rid)
        check("%s (lifetime): usd_per_tb_month is NULL, not an amortised figure (%s)" % (rid, ut), ut is None, (row, t))
        check("%s (lifetime): the claim keeps the one-time price, period once, parse partial" % rid,
              row[2] == "price" and row[5] == "once" and row[9] == "partial" and row[3] is not None, row)
        check("%s (lifetime): it does not feed usd_month" % rid, um is None, row)
    # records that state a lifetime figure next to a subscription: the subscription is the price
    for rid, want in (("storage/koofr", 7.86), ("storage/drime", 3.0), ("storage/icedrive-3-tb", 3.33)):
        row, um, ut = priced(rid)
        check("%s: the subscription price %.2f, not the lifetime deal (%s)" % (rid, want, ut), near(ut, want, 0.002), row)


def other_unit_cases():
    """The price is real, in its own unit: it feeds usd_month when it is a flat monthly price, otherwise nothing."""
    row, um, ut = priced("egress/upvpn")
    check("upvpn: USD 39.99 per year stays a yearly claim", row[2] == "price" and row[5] == "year" and um is None and ut is None, row)
    row, um, ut = priced("debrid/cubenet")
    check("cubenet: USD 4.17 with no period feeds nothing", row[2] == "price" and row[5] is None and um is None and ut is None, row)
    row, um, ut = priced("debrid/uploadflix")
    check("uploadflix: USD 10 per month claimed is a monthly price, not a TB-month one", near(um, 10.0) and ut is None, row)
    row, um, ut = priced("debrid/bestdebrid")
    check("bestdebrid: EUR 4.50/month subscription is usd_month at the dated rate",
          near(um, 4.50 * rate("EUR", "debrid/bestdebrid"), 0.002) and ut is None and row[2] == "price" and row[4] is None and row[5] == "month", row)
    row, um, ut = priced("debrid/turbobitpremium-org")
    check("turbobitpremium: USD 3.75 per month is usd_month", near(um, 3.75) and ut is None, row)
    row, um, ut = priced("egress/google-cloud-free-tier")
    check("google-cloud-free-tier: USD 0.005 an hour is not a TB-month price, USD 3.65 a month is the monthly one", ut is None and near(um, 3.65), row)
    row, um, ut = priced("egress/aws-global-accelerator")
    check("aws-global-accelerator: USD 18 a month is usd_month, the USD 0.015 per GB is not read as a price per TB-month", ut is None and near(um, 18.0), row)
    row, um, ut = priced("egress/cosmic-guard")
    check("cosmic-guard: USD 0.03 per average player per day keeps its unit", row[2] == "price" and row[4] == "average player" and row[5] == "day" and um is None, row)
    row, um, ut = priced("ip-proxy/oxylabs-isp-proxies")
    check("oxylabs-isp-proxies: USD 1.50/IP keeps unit IP", row[2] == "price" and row[4] == "IP", row)
    row, um, ut = priced("ci-cd-runners/buildkite-free")
    check("buildkite: USD 0.004 per vCPU-minute keeps its unit", row[2] == "price" and row[4] == "vCPU-minute" and row[3] == 0.004, row)
    row, um, ut = priced("ci-cd-runners/github-actions-private")
    check("github actions: USD 0.006 per Linux minute keeps unit and period", row[4] == "Linux" and row[5] == "minute" and row[3] == 0.006, row)
    row, um, ut = priced("domains-dns/cloudflare-registrar")
    check("cloudflare registrar: USD 10.46 per .com per year keeps unit and period", row[4] == ".com" and row[5] == "year" and row[3] == 10.46, row)
    row, um, ut = priced("egress/azure-free-account")
    check("azure free account: USD 200 of credit is a credit", row[4] == "credit" and um is None and ut is None, row)
    row, um, ut = priced("storage/bright-data-residential-network")
    check("bright data: $4096/TB (egress at $4/GB) is read and kept as a passed-over number, parse partial", row[9] == "partial" and ut is None and um is None, row)
    row, um, ut = priced("storage/blomp")
    check("blomp: not the $11.88 per year of the 500 GB plan", ut is not None and ut < 2, row)
    # usd_month is the price of the offer kept for a whole month (live walk 2, W2-02): the stated monthly list price,
    # else the machine run 24 hours a day, never the 10-hours-a-day figure and never the renewal price
    o = {"topic": "compute", "extras": {"m24h_usd": 5.5, "renewal_usd": 7.0, "monthly_usd": 9.0}}
    cl = derive.claims_for("compute/x", o, None, FX)
    um, ut = derive.headline_prices(cl)
    check("usd_month is the stated monthly list price, not a cheaper 24-hour figure", um == 9.0 and ut is None, (um, ut))
    o = {"topic": "compute", "extras": {"m10h_usd": 1.6, "m24h_usd": 116.8}}
    cl = derive.claims_for("compute/x", o, None, FX)
    um, ut = derive.headline_prices(cl)
    check("the 10-hours-a-day figure is never usd_month: the 24-hour month is", um == 116.8, (um, ut))
    check("the 10-hours-a-day claim carries its own unit", any(c[1] == "$.extras.m10h_usd" and c[4] == derive.M10H_UNIT for c in cl), cl)
    o = {"topic": "compute", "extras": {"m10h_usd": 0.875, "m24h_usd": 0.875, "price_on_page": "USD 1.4375/mo or USD 10.50/yr"}}
    cl = derive.claims_for("compute/x", o, None, FX)
    um, ut = derive.headline_prices(cl)
    check("the monthly price the vendor's page prints beats a yearly price divided by 12", um == 1.4375, (um, ut))
    check("price_violations: none when usd_month is the stated monthly price", derive.price_violations("compute/x", cl, um) == [])
    check("price_violations: a usd_month below the stated monthly price is one", len(derive.price_violations("compute/x", cl, 0.875)) == 1)
    cl = derive.claims_for("compute/x", {"topic": "compute", "extras": {"m10h_usd": 1.6, "m24h_usd": 116.8}}, None, FX)
    check("price_violations: the 10-hours-a-day figure as usd_month is one", len(derive.price_violations("compute/x", cl, 1.6)) == 1)
    o = {"topic": "compute", "price_per_tb_month": "USD 0.00 per TB (egress free)", "extras": {"m24h_usd": 17.4}}
    um, ut = derive.headline_prices(derive.claims_for("compute/x", o, None, FX))
    check("a price text does not disturb the extras price", um == 17.4 and ut is None, (um, ut))
    o = {"topic": "compute", "extras": {"m24h_usd": 2.0, "renewal_usd": 1.0}}
    um, ut = derive.headline_prices(derive.claims_for("compute/x", o, None, FX))
    check("the renewal price is not usd_month (the records write it per month and per year)", um == 2.0, (um, ut))


# ------------------------------------------------------------------------------------------ the PLN price

def pln_cases():
    """A price in PLN is read, converted exactly from GiB to TB, and its USD stays NULL until a PLN rate exists."""
    have_pln = any(c == "PLN" for c, _ in FX)
    row, um, ut = synth("Billed per GiB-hour at 0.00004861 PLN, shown as ~0.0354853 PLN/GiB/month over 730 h.")
    check("PLN per GiB-month is read as a PLN price per TB-month", row[2] == "price-per-tb" and row[6] == "PLN" and near(row[3], 0.0354853 / GIB, 1e-4), row)
    check("PLN: no rate is guessed", (row[7] is None and ut is None) if not have_pln else near(row[7], row[3] * rate("PLN", date="2026-10-24")), row)
    rid = "storage/ovhcloud-object-storage-one-zone-standard-flat-s3-with-c"
    stated = FIXED[rid]["free_tier"]["stated"]
    # the record quotes the Polish list with its decimal comma in free_tier.stated, which the price parser does not
    # read as a decimal (it is no price field: claims_for reads only a quantity there); its price field states the same
    # figure with a point, and that is the text the parser must read. The form with a point in free_tier.stated is the
    # synthetic case above
    if check("%s still states the PLN price per GiB-month" % rid, "0,0354853 PLN per GiB-month" in stated, stated):
        check("%s: the price field states the stated PLN figure with a decimal point" % rid,
              "PLN 0.0354853 per GiB-month" in text_of(rid), text_of(rid))
        row, um, ut = synth(text_of(rid))
        check("%s: its own text gives %.2f PLN per TB-month" % (rid, 0.0354853 / GIB), near(row[3], 0.0354853 / GIB, 1e-4) and row[6] == "PLN", row)
        check("%s: the USD is NULL until an FX row exists" % rid, (ut is None) if not have_pln else ut is not None, row)
    row, um, ut = synth("0.0354853 PLN per GiB-month")
    check("PLN per GiB-month, spelled out", near(row[3], 0.0354853 / GIB, 1e-4) and row[7] is None or have_pln, row)
    # the price text now and before a run corrected it (rid@earlier): each with its own value
    for key in (rid, rid + "@earlier"):
        row, um, ut = priced(key)
        if "PLN 33.05 per TB per month" in text_of(key):
            check("%s: the corrected price field states PLN 33.05 per TB-month, converted at the dated PLN rate" % rid,
                  row[6] == "PLN" and near(row[3], 33.05, 0.002) and
                  (ut is None if not have_pln else near(ut, 33.05 * rate("PLN", key), 0.006)), row)
        else:
            check("%s: the price field states the USD figures, and the PLN read-back fee is not the price" % rid,
                  near(ut, 4.55, 0.002), row)


# ------------------------------------------------------------------------------------------ unit classes

def unit_classes():
    """(text, topic) -> USD per TB-month, or None. A synthetic string for each way a unit can be written."""
    e = rate("EUR", date="2026-10-24")
    cases = [
        ("$25/TB/mo", "storage", 25.0),
        ("$25 per TB per month", "storage", 25.0),
        ("$25 per TB stored", "storage", 25.0),                       # the storage field's period is a month
        ("$25 per TB", "debrid", None),                               # elsewhere a per-TB price is not a month
        ("$25 per TB-month", "debrid", 25.0),
        ("$0.05/GB-month", "storage", 50.0),                          # GB x 1000
        ("USD 0.05 per GB per month", "databases-kv", 50.0),
        ("$0.05/GB", "databases-kv", None),                           # no period outside storage topics
        ("$0.05/GiB/mo", "storage", 0.05 / GIB),                      # GiB x 1e12/2^30
        ("$20/TiB/month", "storage", 20 / TIB),                       # a TiB price divided by 1.0995
        ("$20/TiB/month", "debrid", 20 / TIB),
        ("$120/TB/year", "storage", 10.0),                            # a year is 12 months
        ("$120/TB/yr", "debrid", 10.0),
        ("$30 per TB per 30 days", "debrid", 30.0),                   # a stated 30 days is a month
        ("$30 per TB per 31 days", "debrid", None),                   # 31 is not 30
        ("$0.10/GB/day", "storage", 3000.0),                          # a day is 1/30 of a month
        ("EUR 26.99 for 16 TB", "storage", 26.99 / 16 * e),           # a monthly price for a stated volume
        ("EUR 26.99 per month for 16 TB", "debrid", 26.99 / 16 * e),
        ("EUR 26.99 for 16 TB", "debrid", None),
        ("EUR 6.00 TTC for 300 Go = EUR 20/TB/month", "debrid", 20 * e),   # a stated figure beats the worked-out one
        ("$12/month for 100 GB; $7/TB/mo", "storage", 7.0),
        ("$99.99/yr for 10 TB", "storage", 99.99 / 12 / 10),
        ("$4.10/TB/mo; $20.53/TB/mo; $26.32/TB/mo", "storage", 4.10),   # the cheapest tier counts
        ("$2.00-2.50/TB/mo", "storage", 2.0),
        ("$0/TB/month storage on the Standard tier; $15/TB/mo Performance", "storage", 0.0),   # a free tier is not a price to rank by
        # what is not a storage price
        ("$25/TB stored + $5/TB egress beyond the included 1 TB", "storage", 25.0),
        ("$5/TB egress", "storage", None),
        ("$0.05/GB overage", "storage", None),
        ("$0.04-0.50 per million operations", "storage", None),
        ("$6.14/TB stored, $0.04 per million operations", "storage", 6.14),
        ("$20/TB stored with free egress", "storage", 20.0),
        ("$10/TB/mo, plus EUR 5/TB restore fee", "storage", 10.0),
        ("EUR 5/TB retrieval fee", "storage", None),
        ("$4096/TB (egress at $4/GB)", "storage", None),
        ("$120/TB EU/NA, $190/TB Asia", "storage", None),
        ("$27.00/TB one-time", "storage", None),
        ("One-time $27.00/TB at 10 TB. Amortised over 5 years: $0.45/TB/mo", "storage", None),
        ("Lifetime 1 TB $159.99 = $159.99/TB one-time, or $2.67/TB/mo over 5 years.", "storage", None),
        ("$3.00/TB subscription; one-time $36.00/TB lifetime, which amortises to $1.50/TB/mo over 2 years", "storage", 3.0),
        ("$4.68/TB/mo on the promo, $9.38/TB/mo at renewal", "storage", 9.38),
        ("Promotional: $4.17/TB/mo. Steady state: $8.35/TB/mo", "storage", 8.35),
        ("$2.50/TB/mo flat. At 5 TB workload: $5.70/TB all-in", "storage", 2.5),
        ("$25/TB/mo. Compare OVH at $9.34/TB/mo", "storage", 25.0),
        ("not a per-TB product: USD 9.99 per month", "storage", None),
        ("no per-TB figure exists; $3/TB/mo is a guess", "storage", None),
        ("USD 200 of credit", "storage", None),
        ("$10 per IP per month", "storage", None),
        ("$0.006 per Linux minute", "storage", None),
        ("USD 0.004 per vCPU-minute", "storage", None),
        ("USD 10.46 per .com per year", "storage", None),
        ("USD 5 per month per account", "storage", None),
    ]
    for text, topic, want in cases:
        row, um, ut = synth(text, topic)
        ok = (ut is None) if want is None else (ut is not None and near(ut, want, 0.0005, 1e-6) if want else (ut is None and row[3] == 0))
        check("%s [%s] -> usd_per_tb_month %s" % (text, topic, "NULL" if want is None else "%.4f" % want), ok, (row, ut))
        if want:
            check("%s [%s]: claim is price-per-tb, TB, month" % (text, topic), row[2] == "price-per-tb" and row[4] == "TB" and row[5] == "month", row)
    # monthly prices
    for text, topic, want in (("EUR 4.50/month subscription", "debrid", 4.5 * e), ("USD 9.99 per month", "egress", 9.99),
                              ("USD 15 per 30 days, no volume figure published", "debrid", 15.0),
                              ("USD 11.95 per month at the 1-month term; USD 6.25/month at the 1-year term", "debrid", 6.25),
                              ("USD 18 per month plus USD 0.015 per GB", "egress", 18.0),
                              ("USD 15 per month for 60 GB/day", "debrid", 15.0)):
        row, um, ut = synth(text, topic)
        check("%s [%s] -> usd_month %.4f, usd_per_tb_month NULL" % (text, topic, want), near(um, want, 0.0005, 1e-6) and ut is None, (row, um, ut))
    # a text with no money
    for text in ("n/a", "unverified", "paid cloud", "not applicable: dead"):
        row, um, ut = synth(text)
        check("%r is unparsed, every number NULL" % text, row[9] == "unparsed" and row[3] is None and um is None and ut is None, row)
    # exchange rates are not prices
    row, um, ut = synth("EUR 4.50/month subscription (USD 5.05 at 1.1205 EUR/USD, 0.8915 EUR per USD)", "debrid")
    check("an exchange rate is not a price", near(row[3], 4.5), row)


def headline_cases():
    claims = [("r", PATH, "price-per-tb", 5.0, "GB", "month", "USD", 5.0, None, "ok"),
              ("r", PATH + "2", "price-per-tb", 6.0, "TB", "year", "USD", 6.0, None, "ok"),
              ("r", PATH + "3", "price-per-tb", 7.0, "TB", "month", "USD", 7.0, None, "partial"),
              ("r", PATH + "4", "price-per-tb", 0.0, "TB", "month", "USD", 0.0, None, "ok"),
              ("r", PATH + "5", "price-per-tb", 8.0, "TB", "month", "USD", 8.0, None, "ok"),
              ("r", PATH + "6", "price-per-tb", 9.0, "TB", "month", "USD", 9.0, None, "ok"),
              ("r", PATH + "7", "price", 1.0, "GB", "month", "USD", 1.0, None, "ok"),
              ("r", PATH + "8", "price", 2.0, None, "year", "USD", 2.0, None, "ok"),
              ("r", PATH + "9", "price", 3.0, None, "month", "USD", 3.0, None, "partial"),
              ("r", PATH + "10", "price", 4.0, None, "month", "USD", 4.0, None, "ok"),
              ("r", "$.extras.m24h_usd", "price", 6.5, None, "month", "USD", 6.5, None, "ok")]
    check("headline_prices takes only unit TB per month for the TB column, no zero or partial number, and the 24-hour "
          "month before another monthly claim", derive.headline_prices(claims) == (6.5, 8.0), derive.headline_prices(claims))
    check("headline_prices: without a 24-hour month, the cheapest monthly claim", derive.headline_prices(claims[:-1]) == (4.0, 8.0),
          derive.headline_prices(claims[:-1]))
    check("headline_prices of nothing", derive.headline_prices([]) == (None, None))


# ------------------------------------------------------------------------------------------ every text

PER_TB = re.compile(r"(?P<c>USD|EUR|GBP|\$|€|£)\s?(?P<n>\d[\d,]*(?:\.\d+)?)(?:\s?[-–]\s?\d[\d,]*(?:\.\d+)?)?\s*(?:/|per\s)\s*(?P<u>TB|TiB)\b"
                    r"(?:\s?(?:-|/|per\s|a\s)?\s?(?P<p>mo(?:nth)?|yr|year)\b)?", re.I)
SYMBOL = {"$": "USD", "€": "EUR", "£": "GBP"}


def stated_per_tb(text, date, fx=None):
    """Every 'X/TB' the text states, as (USD at the given rates, the frozen ones by default, or None; has an explicit
    period)."""
    out = []
    for m in PER_TB.finditer(text):
        ccy = SYMBOL.get(m.group("c"), m.group("c").upper())
        amount = float(m.group("n").replace(",", ""))
        if m.group("u").lower() == "tib":
            amount /= TIB
        per = (m.group("p") or "").lower()
        if per.startswith(("yr", "year")):
            amount /= 12
        usd, _ = derive.to_usd(amount, ccy, date, FX if fx is None else fx)
        out.append((usd, bool(per)))
    return out


def disagreement(rid, raw, fx, month_default_only=True):
    """(usd_per_tb_month, the stated per-TB figures) when the text states X/TB and the value is none of them, else
    None; and whether the text states a figure the check counts. Where a per-TB figure with no period is not a month
    (debrid, egress ...) only a figure that states its period counts as stated, unless month_default_only is False."""
    date = read_date(raw)
    um, ut = derive.headline_prices(derive.claims_for(rid, raw, date, fx))
    month_default = raw["topic"] in derive.MONTH_DEFAULT_TOPICS
    st = [u for u, explicit in stated_per_tb(raw["price_per_tb_month"], date, fx)
          if explicit or month_default or not month_default_only]
    counted = bool(st and ut is not None and ut > 0)
    if counted and not any(u is not None and near(u, ut, 0.005, 0.01) for u in st):
        return (ut, [round(u, 4) for u in st if u is not None]), counted
    return None, counted


def frozen_agreement():
    """The parser against the per-TB figures each frozen text states: a text that states X/TB gives one of them."""
    n_stated, bad_stated, wrong = 0, [], []
    for key, raw in sorted(FIXED.items()):
        if not isinstance(raw.get("price_per_tb_month"), str):
            continue
        bad, counted = disagreement(key.split("@")[0], raw, FX)
        n_stated += counted
        if bad:
            bad_stated.append((key,) + bad)
        if raw["topic"] == "storage":
            bad, _ = disagreement(key.split("@")[0], raw, FX, month_default_only=False)
            if bad:
                wrong.append(key)
    check("the agreement check is not vacuous: %d frozen texts state a per-TB figure" % n_stated, n_stated > 80)
    check("every frozen text that states X/TB: usd_per_tb_month is one of the stated figures, converted (%d bad)" % len(bad_stated),
          not bad_stated, bad_stated[:8])
    # the storage records the review counted: 109 had a value, and for 22 of 89 that state a per-TB figure it matched none
    check("storage: no frozen text whose value matches none of the per-TB figures it states (%d)" % len(wrong), not wrong, wrong)


def whole_corpus():
    """Invariants over every record of dossier/ that hold for any text, so a record change cannot fail them: each
    non-NULL value has its claim, and no claim kind is new. The agreement with the stated figures is a value, so over
    the live records it is only counted and printed (frozen_agreement checks it on the frozen texts)."""
    records = {}
    for p in sorted(glob.glob(os.path.join(REPO, "dossier", "*", "*.json"))):
        with open(p, encoding="utf-8") as f:
            o = json.load(f)
        records[o["topic"] + "/" + o["slug"]] = o
    fx = derive.fx_table(list(records.values()))
    n_priced = n_values = n_live_bad = 0
    kinds = set()
    bad_shape = []
    for rid, raw in records.items():
        if not isinstance(raw.get("price_per_tb_month"), str):
            continue
        n_priced += 1
        claims = derive.claims_for(rid, raw, read_date(raw), fx)
        um, ut = derive.headline_prices(claims)
        for c in claims:
            kinds.add(c[2].split(":")[0])
        for c in claims:
            if c[2] == "price-per-tb" and c[3] is not None and not (c[4] == "TB" and c[5] == "month"):
                bad_shape.append((rid, c))
        row = next(c for c in claims if c[1] == PATH)
        if ut is not None:
            n_values += 1
            if not (row[2] == "price-per-tb" and row[4] == "TB" and row[5] == "month" and row[7] == ut):
                bad_shape.append((rid, "usd_per_tb_month %s has no claim in unit TB per month" % ut, row))
        if um is not None and ut is None and not (row[2] == "price" and row[4] is None and row[5] == "month"):
            if not any(c[1].startswith("$.extras.") for c in claims):
                bad_shape.append((rid, "usd_month %s without a monthly price claim" % um, row))
        n_live_bad += disagreement(rid, raw, fx)[0] is not None
    check("the corpus test is not vacuous: %d records with a price text, %d with a value" % (n_priced, n_values),
          n_priced > 600 and n_values > 100)
    check("every non-NULL usd_per_tb_month has a claim of kind price-per-tb in unit TB per month, and no such claim has another unit",
          not bad_shape, bad_shape[:5])
    check("no new claim kind: the public store reads price-per-tb, price, free-quota and limit:* only",
          kinds <= {"price-per-tb", "price", "free-quota", "limit"}, kinds)
    if VERBOSE or n_live_bad:
        print("info  %d record(s) of dossier/ state X/TB in their price text and get a value that is none of those figures "
              "(not a failure: a record's text is not this selftest's to pin)" % n_live_bad)


def main():
    exact_cases()
    null_cases()
    other_unit_cases()
    pln_cases()
    unit_classes()
    headline_cases()
    frozen_agreement()
    whole_corpus()
    if FAILS:
        print("%d check(s) failed" % len(FAILS))
        return 1
    print("test_prices: all checks passed")
    return 0


# ------------------------------------------------------------------------------------------ the frozen texts

# The dated exchange rates that the records of dossier/ cited on 2026-10-31 (derive.fx_table of every record then),
# (currency, date) -> (USD for one unit, source). Frozen with the texts, so a record that adds a rate changes no case.
# The texts: key -> what claims_for reads for the price row of the record (topic, price_per_tb_month, the price keys of
# extras) and read_date, the newest evidence date that build.py passes. Copied from dossier/ at main 1c90ad48 on
# 2026-10-31; a key rid@earlier is the text of that record at main 1df87d33, before a run corrected it.
FX = {
    ("BRL", "2026-10-24"): (0.1983009573970223, "open.er-api.com/v6/latest/USD"),
    ("CNY", "2026-10-23"): (0.14992054211268027, "ECB reference via frankfurter.app"),
    ("EUR", "2026-10-23"): (1.1193, "ECB reference via frankfurter.app"),
    ("EUR", "2026-10-24"): (1.1200917579168086, "open.er-api.com/v6/latest/USD"),
    ("GBP", "2026-10-23"): (1.3368269076519972, "ECB reference via frankfurter.app"),
    ("IDR", "2026-10-24"): (5.528e-05, "open.er-api.com/v6/latest/USD"),
    ("INR", "2026-10-24"): (0.010522273907163999, "open.er-api.com/v6/latest/USD"),
    ("JPY", "2026-10-24"): (0.0063759368674114235, "open.er-api.com/v6/latest/USD"),
    ("KRW", "2026-10-24"): (0.0007548866631318998, "open.er-api.com/v6/latest/USD"),
    ("PLN", "2026-10-23"): (0.2547056875780036, "ECB reference via frankfurter.app"),
    ("RUB", "2026-10-24"): (0.01230062, "open.er-api.com/v6/latest/USD"),
    ("TRY", "2026-10-23"): (0.020105, "frankfurter.app, derived from USD base 49.738 TRY"),
    ("TRY", "2026-10-24"): (0.02010724, "open.er-api.com/v6/latest/USD"),
    ("UAH", "2026-10-24"): (0.02212322, "open.er-api.com/v6/latest/USD"),
    ("USD", "2026-10-24"): (1.0, "not applicable"),
    ("VND", "2026-10-24"): (3.873e-05, "open.er-api.com/v6/latest/USD"),
}

FIXED = {
    "ci-cd-runners/buildkite-free": {
        "topic": "ci-cd-runners", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 0.004 per vCPU-minute"},
    "ci-cd-runners/github-actions-private": {
        "topic": "ci-cd-runners", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 0.006 per Linux minute beyond the allowance"},
    "compute/mitos": {
        "topic": "compute", "read_date": "2026-10-24",
        "price_per_tb_month": "USD 0.00 per TB (egress free)",
        "extras": {
            "m24h_usd": 42.34,
            "m10h_usd": 17.4}},
    "databases-kv/cloudflare-d1": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 0.75/GB-month beyond 5 GB on Workers Paid"},
    "databases-kv/dynamodb": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 0.25/GB-month beyond 25 GB"},
    "databases-kv/pinecone": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 0.33/GB-month storage; USD 0.10/GB egress"},
    "databases-kv/prisma-postgres": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 8 per million operations; storage USD 2.00/GB beyond 10 GB on Starter"},
    "databases-kv/tidb-cloud-starter": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 0.10 per million RUs beyond the allowance"},
    "databases-kv/turso": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 0.75/GB beyond 9 GB on Developer"},
    "databases-kv/upstash-redis": {
        "topic": "databases-kv", "read_date": "2026-10-22",
        "price_per_tb_month": "USD 0.20 per 100K commands; storage USD 0.25/GB-month beyond the first 1 GB"},
    "debrid/alfafile": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 14.99 per TiB-month on the 30-day 1 TB plan; the 90-day 4 TB plan is USD 10.00 per TiB-month"},
    "debrid/bestdebrid": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("EUR 4.50/month subscription; EUR 3 per 15 days one-time (USD 5.05 and USD 3.37 at the 2026-10-23 "
                               "ECB-derived rate of 0.8915 EUR per USD)")},
    "debrid/blocknews": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 39.99 per TB one-time"},
    "debrid/brfiles": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "BRL 49.90 per month for 2 TB included = BRL 24.95/TB (USD 4.95/TB at 5.0383)"},
    "debrid/cubenet": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 4.17 (unlimited, $50/year)"},
    "debrid/daofile": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 43.87 per TiB-month if the allowance is 50 GB per 3 days; USD 14.7 if it is 50 GB per day. The "
                               "page is ambiguous and the worse reading is recorded.")},
    "debrid/debridmaster": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 500/TB pay-as-you-go; USD 4.99/mo for 15 GB"},
    "debrid/decodo": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 2,048 per TiB (USD 2.00/GB at the 1,000 GB plan)"},
    "debrid/dropgalaxy": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 30.54 per TiB-month (USD 50 for a 1.64 TiB allowance); USD 20.6 per TiB-month at 365 days"},
    "debrid/evoseedbox": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 5 for 150 GB = USD 33.33/TB/month"},
    "debrid/ex-load": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 23.30 per TB-month on a 30-day pass; USD 7.22 per TB-month at the annual rate"},
    "debrid/fileboom": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 17.20 per TiB-month on Premium Max (USD 46.94 for 2.73 TiB); USD 26.8 on Premium Pro; USD 52.5 on "
                               "Premium")},
    "debrid/filefactory": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 13.00 per TiB-month if the 'unlimited bandwidth' claim holds; unverified because the vendor page "
                               "could not be read")},
    "debrid/filejoker": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 20.74 per TiB-month on VIP (USD 33.95 for 1.64 TiB of allowance); USD 22.95 buys only 0.33 TiB on "
                               "the base plan")},
    "debrid/fileq": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 20 per TB-month of additional storage"},
    "debrid/filesmonster": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 3.78 per TB per 30 days at the annual rate (USD 116 / 2.555 TB / 12 months)"},
    "debrid/high-way-premium": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("EUR 12.00 per TB per 30 days; EUR 9.17 per TB at 12 TB for one year (EUR 110.00); EUR 16.00 per TB at "
                               "3 TB for one year (EUR 47.99)")},
    "debrid/high-way-unlimited": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("EUR 15.99 per TB per 30 days at 750 GB for EUR 11.99; EUR 24.00 per TB at 3 TB for one year (EUR "
                               "71.99); usenet unmetered")},
    "debrid/iseedfast": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 3 for 50 GB = USD 60/TB/month"},
    "debrid/leechdrive": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 5 for 50 GB = USD 100/TB/month"},
    "debrid/multcloud": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 19.99 per 100 GB per month (about USD 199.90 per TB); USD 119/year unlimited"},
    "debrid/my-seedbox": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 6.00 TTC for 300 Go = EUR 20/TB/month"},
    "debrid/nopremium-pl": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "PLN 363 per TB (EUR 83 at 4.3695), prepaid, no expiry stated"},
    "debrid/oxylabs": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 2,560 per TiB (USD 2.50/GB at the 1,000 GB tier)"},
    "debrid/rapideo-net": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 10.99 per 600 GB / 30 days (EUR 18.32/TB); EUR 76.99 per 7200 GB / 360 days (EUR 10.69/TB)"},
    "debrid/seedbox-fr": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 12.00 HT per 1 To per month (EUR 12/TB/month; EUR 14.40 TTC at 20% VAT)"},
    "debrid/seedboxbay": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 5 for 100 GB = USD 50/TB/month"},
    "debrid/seedboxes-cc": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 14.35 for 2 TB = EUR 7.18/TB/month (USD ~7.8 at 1.09)"},
    "debrid/send-now": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 1.50 per TB-month of storage at Premium (EUR 14.99 for 10 TB); EUR 3 per TB of direct-link egress"},
    "debrid/sonicseedbox": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 0 for 4 GB; paid Basic USD 5.95 for 100 GB = USD 59.50/TB/month"},
    "debrid/turbobitpremium-org": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 9.95 per month at the 1-month term; USD 3.75/month at the 24-month term"},
    "debrid/uploadflix": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 10 per month claimed, USD 48 per year claimed (reported from the vendor page as indexed, not read "
                               "live)")},
    "debrid/uploadgig": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 7.33 per TiB-month at the 30-day plan (USD 20.00 for 2.73 TiB of allowance), USD 4.22 at 365 days"},
    "debrid/uploadhaven": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 8.99 per TiB-month on the stated 'Unlimited bandwidth', which no fair-use number contradicts that "
                               "was reachable")},
    "debrid/upstore": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 14.55 per TiB-month at the monthly rate (EUR 16 / 33 days) with no byte cap published"},
    "debrid/usenet-farm": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 30.00 per TB one-time (500 GB block)"},
    "debrid/yourseedbox": {
        "topic": "debrid", "read_date": "2026-10-23",
        "price_per_tb_month": "EUR 15.96/year for 200 GB = EUR 79.80/TB/year = EUR 6.65/TB/month"},
    "domains-dns/cloudflare-registrar": {
        "topic": "domains-dns", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 10.46 per .com per year, registration and renewal alike"},
    "domains-dns/porkbun": {
        "topic": "domains-dns", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 11.08 .com; USD 7.98 .org; USD 2.04 then USD 14.21 .xyz"},
    "domains-dns/spaceship": {
        "topic": "domains-dns", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 8.88 then USD 9.98 .com; USD 6.65 then USD 11.39 .org; USD 0.98 then USD 15.08 .online"},
    "egress/akamai-cloud-linode": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 100 of credit"},
    "egress/aws-global-accelerator": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 18 per month plus USD 0.015 per GB"},
    "egress/azure-free-account": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 200 of credit"},
    "egress/cloudflare-r2": {
        "topic": "egress", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 15 per TB-month of Standard storage beyond the free 10 GB-month (USD 0.015 / GB-month); egress "
                               "USD 0")},
    "egress/cosmic-guard": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 0.03 per average player per day, or USD 0.02 per GB transmit"},
    "egress/google-cloud-free-tier": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 0 for the instance; about USD 3.65 a month for the external IPv4 at USD 0.005 an hour"},
    "egress/hyehost-ipv4-tunnels": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": ("USD 1.50 per IPv4 address per month (USD 18 per year for a /32); USD 0.20 per Mbps per month above "
                               "the included 100 Mbps in UK and US")},
    "egress/upvpn": {
        "topic": "egress", "read_date": "2026-10-23",
        "price_per_tb_month": "USD 39.99/year"},
    "ip-proxy/brightdata-residential": {
        "topic": "ip-proxy", "read_date": "2026-10-24",
        "price_per_tb_month": ("$8/GB list, $4/GB with code RESIGB50 (= $8,192/TB and $4,096/TB by arithmetic); plans $499/month for "
                               "141 GB, $999 for 332 GB, $1,999 for 798 GB; ISP per IP $1.80 shared at 10 down to $1.30 at 1,000, "
                               "$3.50 dedicated at 10 down to $2.50 at 1,000")},
    "ip-proxy/oxylabs-isp-proxies": {
        "topic": "ip-proxy", "read_date": "2026-10-24",
        "price_per_tb_month": "not applicable: priced per address at USD 1.50/IP in the smallest band, bandwidth unmetered"},
    "ip-proxy/proxidize-mobile": {
        "topic": "ip-proxy", "read_date": "2026-10-24",
        "price_per_tb_month": ("not quoted per TB: USD 2.00 per GB flat metered, or USD 59 per proxy per month with a 50 GB fair-use "
                               "threshold")},
    "ip-proxy/soax-mobile": {
        "topic": "ip-proxy", "read_date": "2026-10-24",
        "price_per_tb_month": ("USD 5.00 per GB Tier 1 on Sandbox, USD 3.00 on Builder, USD 2.20 on Team, USD 1.50 on Scale, from USD "
                               "0.85 on Enterprise; the vendor prices per GB and publishes no per-TB figure")},
    "netdisk-pan/allsync": {
        "topic": "netdisk-pan", "read_date": "2026-10-22",
        "price_per_tb_month": ("From EUR 4/TB/month on the 1 to 10 TB pool, excluding any tax an EU resident pays; the per-tier "
                               "ladder above 1 TB is not published")},
    "netdisk-pan/danubedata-storage-share": {
        "topic": "netdisk-pan", "read_date": "2026-10-22",
        "price_per_tb_month": "EUR 4.99/TB/month at 1 TB falling to EUR 3.00/TB/month at 10 TB, read 2026-10-22"},
    "netdisk-pan/disroot-cloud": {
        "topic": "netdisk-pan", "read_date": "2026-10-21",
        "price_per_tb_month": "EUR 110/year for 60 GB, which is EUR 152/TB/year and therefore irrelevant"},
    "netdisk-pan/gopro-cloud-quik": {
        "topic": "netdisk-pan", "read_date": "2026-10-21",
        "price_per_tb_month": ("USD 59.99/yr Premium and USD 99.99/yr Premium+, which is about USD 120/TB/yr on the 500 GB non-GoPro "
                               "half and approaches zero on the GoPro half")},
    "netdisk-pan/hetzner-storage-share": {
        "topic": "netdisk-pan", "read_date": "2026-10-22",
        "price_per_tb_month": ("EUR 4.29/TB/month on NX11, falling to EUR 2.74/TB/month on NX31 at 10 TB, excluding VAT, read "
                               "2026-10-22")},
    "netdisk-pan/huawei-mobile-cloud": {
        "topic": "netdisk-pan", "read_date": "2026-10-21",
        "price_per_tb_month": ("2 TB at CNY 698/yr is about USD 4.1/TB/month, and it is often unpurchasable on a non-mainland HUAWEI "
                               "ID")},
    "netdisk-pan/nextfiles-one": {
        "topic": "netdisk-pan", "read_date": "2026-10-22",
        "price_per_tb_month": "EUR 4.99/TB/month at 1 TB rising to EUR 10.00/TB/month at 10 TB, including VAT, read 2026-10-22"},
    "netdisk-pan/quixicloud": {
        "topic": "netdisk-pan", "read_date": "2026-10-21",
        "price_per_tb_month": "USD 1.42/TB/month on the 2 TB plan at USD 33.99/yr, and USD 1.56/TB/month on 6 TB at USD 112.49/yr"},
    "netdisk-pan/serverdiscounter-next-share": {
        "topic": "netdisk-pan", "read_date": "2026-10-22",
        "price_per_tb_month": ("EUR 2.40/TB/month including VAT at 25 TB (EUR 59.95/month), rising to EUR 4.95/TB/month at 1 TB, read "
                               "2026-10-22")},
    "netdisk-pan/telnyx-cloud-storage-egress-view": {
        "topic": "netdisk-pan", "read_date": "2026-10-21",
        "price_per_tb_month": "USD 6.14/TB/month at USD 0.006/GiB, with no egress charge at any volume"},
    "netdisk-pan/xiaomi-cloud": {
        "topic": "netdisk-pan", "read_date": "2026-10-21",
        "price_per_tb_month": "2 TB at CNY 408/yr promotional is about USD 2.4/TB/month, and CNY 816/yr list about USD 4.8/TB/month"},
    "storage/1fichier-premium-gold": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("EUR 1.00/TB/month at the 10 TB cold tier on the 1-year list price of EUR 120; EUR 0.42/TB/month on "
                               "the 1-year sale price of EUR 50, offered until November 2; EUR 0.38/TB/month on the 10-year sale "
                               "price of EUR 450 (list EUR 1,200). Extra cold storage EUR 1/TB/month.")},
    "storage/advin-servers-kvm-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.50/TB/mo at both tiers ($25 for 10.24 TB, $50 for 20.48 TB). At 5 TB: the 5.12 TB rung at $15/mo = "
                               "$2.93/TB. Cheapest large-footprint option in the lane on paper, but not purchasable.")},
    "storage/akamai-linode-object-storage": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 5 a month flat, prorated, including 250 GB of storage and 1 TB of outbound transfer added to the "
                               "account's global transfer pool; storage beyond 250 GB USD 0.02 per GB a month (about USD 20 per TB), "
                               "and overages may vary by data center; outbound overage USD 0.005 per GB (about USD 5 per TB), USD "
                               "0.015 per GB in Jakarta and USD 0.007 per GB in São Paulo")},
    "storage/akamai-linode-object-storage@earlier": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$20/TB stored + $5/TB egress beyond the included 1 TB; entry $5/mo for 250 GB + 1 TB egress."},
    "storage/alphavps-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.74/TB/mo (€3.33). At 5 TB: not a ladder rung — cheapest 5 TB shape is 4 TB + 2 TB = €20.00/mo = "
                               "€3.33/TB = $3.74/TB. At 20 TB: exceeds the 16 TB per-VPS ceiling, so cheapest shape is 16 TB (€53.33) "
                               "+ 4 TB (€13.33) on a second VPS = €66.66/mo = €3.33/TB = $3.74/TB. Price is flat from 1 TB to 16 T…")},
    "storage/backblaze-b2": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 6.95 per TB per 30 days, pay-as-you-go, after the first 10 GB"},
    "storage/beget-s3-free-egress-s3-at-350-mbit-s-the-only-russian-o": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$26.04/TB/mo at both 5 TB and 20 TB (₽0.07/GB/day × 30 × 1024 GB × 0.012111), egress $0 and requests "
                               "$0. Compare OVH One-Zone at $9.34/TB/mo with the same free-egress structure — Beget is 2.8× the price "
                               "for geography.")},
    "storage/blomp": {
        "topic": "storage", "read_date": "2026-10-22",
        "price_per_tb_month": ("$1.00/TB/mo at 10 TB ($9.99) and at 100 TB ($99.99) — the flat $1/TB/mo floor makes it scale "
                               "linearly, unlike promo pricing; $1.50/TB/mo at 2 TB ($2.99); $1.98/TB/mo at 500 GB ($11.88/yr)")},
    "storage/borgbase-medium-large": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "2TB: $165/yr -> $6.88/TB/mo. 1TB: $90/yr -> $7.50/TB/mo. Marginal beyond plan: $6.00/TB/mo"},
    "storage/bright-data-residential-network": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$4096/TB (egress at $4/GB)"},
    "storage/bunny-net-edge-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$10/TB stored (HDD, 1 region); $20/TB (SSD); delivery +$10/TB EU/NA, +$30/TB Asia, +$5/TB on Volume "
                               "Network. 20 TiB stored + 30 TB/mo served EU/NA = $200 + $300 = $500/mo ≈ $25 per stored TB all-in.")},
    "storage/buyvm-block-storage-slabs": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$5.00/TB/mo flat, plus the base slice. At 5 TB: $25/mo slab + $3.50 slice = $28.50/mo = $5.70/TB "
                               "all-in. At 20 TB: 2x 10 TB slabs = $100/mo + $3.50 = $103.50/mo = $5.18/TB. The all-in figure is what "
                               "matters and it is worse than the headline because the slice is mandatory overhead.")},
    "storage/cachefly-object-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$25/TB stored with $0 egress/ingress/requests (object storage). CDN separately: free developer 100 "
                               "GB/mo; $0.05/GB overage.")},
    "storage/cdn77-object-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$20/TB stored; $90/TB egress outside CDN77; $0 egress through CDN77. Growth plan $990/mo for 250 TB "
                               "delivered (= $3.96/TB).")},
    "storage/cloud-ru-evolution-object-storage-cheapest-russian-objec": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$14.07/TB/mo at both 5 TB and 20 TB (₽1.1346/GiB × 1024 × 0.012111), storage only, egress "
                               "unpriced/unknown. If egress turns out metered at the Selectel-like ₽1.96/GB this becomes $38/TB/mo "
                               "total and fails; the figure above is storage-only.")},
    "storage/contabo-object-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("€9.96/TB/mo (€2.49 per 250 GB × 4) ≈ $11.55 — flat at 1, 5, 10 and 20 TB, no volume discount. Free "
                               "egress is real but does not rescue a 5× storage premium.")},
    "storage/contabo-storage-vps-30": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$13.44/TB/mo (Storage VPS 30). $17.60/TB (VPS 10 at $5.28/300GB). $17.14/TB (VPS 50). Every tier is "
                               "4–8× the Hetzner equivalent — the 'unlimited traffic' is real but the storage price is not "
                               "competitive at any tier.")},
    "storage/cyverse-data-store": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$10.42/TB/month single-copy ($125/TB/yr), $8.75/TB/month above 4 TB, $20.83/TB/month double-copy. "
                               "Above the wave-6 price floor of ~$5/TB/mo — not recommended.")},
    "storage/data-world": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("Community free (100 GB aggregate, 1-3 GB per unit). Professional Community plan $12/month for 20 "
                               "private projects — ~$120/TB/month against a 100 GB pool, though the per-unit 1 GB cap makes the pool "
                               "theoretical.")},
    "storage/datalix-s3-compatible-object-storage": {
        "topic": "storage", "read_date": "2026-10-22",
        "price_per_tb_month": ("€3.95/TB/mo flat at every tier (5 TB = €19.75, 20 TB = €79.00) ≈ $4.58/TB. No volume discount. "
                               "Cheapest genuine S3-API option in the EU with a sane egress ratio.")},
    "storage/datalix-s3-object-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$4.44/TB at 5 TB (EUR 19.75 = $22.19) and $4.44/TB at 20 TB (EUR 79.00 = $88.75). Cheapest true S3 "
                               "object storage in this survey.")},
    "storage/dataone-hosted-repository-the-price-anchor-for-managed-1": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$1,285.14 per TB per month (~$15,421/TB/year) - the ceiling of this market"},
    "storage/degoo-ultimate-5-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$2.00/TB at 5 TB ($9.99). No 20 TB tier exists — hard ceiling at 5 TB."},
    "storage/deluxhost-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.22/TB/mo at 20 TB (promo €39.59 = $44.48/mo), $2.47/TB at the steady €43.99 = $49.42/mo. At 5 TB: "
                               "€10.79 promo = $12.12/mo = $2.42/TB; steady €11.99 = $13.47/mo = $2.69/TB. At 2 TB: $2.02-2.24/TB. "
                               "This is the cheapest storage outside Europe that is actually orderable today.")},
    "storage/digitalocean-spaces": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$20.48/TB at 5 TB ($102.40) and $20.48/TB at 20 TB ($409.60), plus $10.24/TB on egress beyond 1 TiB."},
    "storage/drime": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.00/TB at 6 TB subscription (EUR 15.99 = $17.96); one-time $36.00/TB lifetime at 10 TB ($359.97), "
                               "which amortises to $1.50/TB/mo over 2 years and $0.50/TB/mo over 6 years")},
    "storage/drime-secure-cloud-storage-10-tb-lifetime": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-time: 10 TB at $359.97 = $36.00/TB once = $0.60/TB/mo over 5 years, $1.00/TB/mo over 3 years. 8 "
                               "TB at $279.97 = $35.00/TB. 5 TB workload: 6 TB SKU at $41.66/TB once. 20 TB workload: two 10 TB SKUs "
                               "= $719.94 = $36/TB. Matches BRIEF §1.1's ~$36/TB figure exactly. Cheapest *usable* lifetime on the…")},
    "storage/eveo-object-storage-s3-the-only-zero-egress-s3-endpoint": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$10.19/TB/mo at both 5 TB and 20 TB (strict per-GB, no tiers), egress $0. R$0.05/GB × 1024 GB/TB × "
                               "0.199082 USD/BRL = $10.19. Note this is per decimal GB on the vendor's wording; if billed per GiB the "
                               "figure is $10.96/TB.")},
    "storage/feral-hosting-radon": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "8TB: £60 -> £7.50/TB/mo (~$10.08). 4.5TB: £45 -> £10.00/TB. 1TB: £10 -> £10.00/TB"},
    "storage/file-kiwi-web-folder": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$6.99 per TB for a 7-day hold = $6.99 × (30.4/7) ≈ $30.36/TB/mo to hold 1 TB continuously. To hold 20 "
                               "TB: ~$607/mo. Roughly 30× the 1fichier/Blomp floor. Dead end for storage; only rational as a paid "
                               "download-enabler for a one-off link.")},
    "storage/filecoin-onchain-cloud": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$2.50/TiB storage + up to $14/TiB egress"},
    "storage/filelu": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$81/TB one-time at the 8 TB lifetime tier ($649) — amortised over 5 years that is $1.35/TB/mo; $56/TB "
                               "one-time at 4 TB ($449)")},
    "storage/filen-pro-x": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$4.49/TB at 10 TiB ($44.93); $4.49/TB at 20 TiB ($89.86)"},
    "storage/frontproxy": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$0.058/GB = $59/TB (egress)"},
    "storage/gcore-free-cdn": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$0 for the first 1 TB/mo; $10/TB beyond (€0.01/GB). Object storage €0.04/GiB/mo ≈ €40/TB ≈ $46/TB — "
                               "not a viable origin.")},
    "storage/greencloudvps-storage-kvm": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.33/TB/mo at the 2 TB rung ($80/yr = $6.67/mo). At 5 TB: 2x Storage-2 + 1x Storage-1 = $13.33 + "
                               "$3.75 = $17.08/mo = $3.42/TB. At 20 TB: 10x Storage-2 = $66.67/mo = $3.33/TB. Annual-only pricing; "
                               "the per-TB rate is already the annual rate.")},
    "storage/hetzner-object-storage": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("EUR 6.49 a month base price, billed at EUR 0.0104 an hour for every hour at least one bucket exists, "
                               "including 1 TB of storage (up to 744 TB-hours) and 1 TB of egress; storage beyond it EUR 0.0087 per "
                               "TB-hour, about EUR 6.47 per TB in a 744-hour month; egress beyond it EUR 1.0000 per TB; prices "
                               "exclude VAT")},
    "storage/hetzner-object-storage-2": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("EUR 6.49 a month base price, billed at EUR 0.0104 an hour for every hour at least one bucket exists, "
                               "including 1 TB of storage (up to 744 TB-hours) and 1 TB of egress; storage beyond it EUR 0.0087 per "
                               "TB-hour, about EUR 6.47 per TB in a 744-hour month; egress beyond it EUR 1.0000 per TB; prices "
                               "exclude VAT")},
    "storage/hetzner-object-storage@earlier": {
        "topic": "storage", "read_date": "2026-10-22",
        "price_per_tb_month": ("$8.06/TB at 5 TB stored + 5 TB egress (EUR 35.89 = $40.32); $8.21/TB at 20 TB stored + 20 TB egress "
                               "(EUR 146.16 = $164.19). Roughly 3.6x the Storage Box for the same bytes.")},
    "storage/hetzner-storage-box": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.28/TB at 20 TB (EUR 40.60 = $45.61); $2.45/TB at 5 TB (EUR 10.90 = $12.24); $3.59/TB at 1 TB (EUR "
                               "3.20 = $3.59). Cheapest genuine unlimited-egress storage found.")},
    "storage/hetzner-storage-box-bx11-bx21-bx31": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("1 TB €3.20/TB · 5 TB €2.18/TB · 10 TB €2.08/TB · 20 TB €2.03/TB (all excl. VAT, no setup, "
                               "hourly-billed)")},
    "storage/hetzner-storage-box-bx21": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "€2.18/TB/mo at 5 TB (€10.90)."},
    "storage/hetzner-storage-box-bx41": {
        "topic": "storage", "read_date": "2026-10-22",
        "price_per_tb_month": ("€2.03/TB/mo at the 20 TB tier (€40.60/20). 5 TB workload: BX21 = €2.18/TB/mo. 20 TB workload: BX41 = "
                               "€2.03/TB/mo. ~$2.19 and ~$2.19 at 1.08 USD/EUR. Non-EU buyers pay excl. VAT (the "
                               "€3.81/€12.97/€24.75/€48.31 figures circulating online are VAT-inclusive German prices — do not use "
                               "them).")},
    "storage/hetzner-sx135-2-dedicated-storage-server": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "€2.24/TB/mo at 128 TB raw (€287.30 ÷ 128); €2.56/TB at 112 TB RAID-6"},
    "storage/hetzner-sx65-2-dedicated-storage-server": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("€1.29/TB/mo at 64 TB raw (€82.30 ÷ 64) ≈ $1.49. €1.71/TB/mo at 48 TB RAID-5 usable (€82.30 ÷ 48). "
                               "SX65-1 at 88 TB raw: €272.30 ÷ 88 = €3.09/TB — worse, because the 22 TB config carries NVMe. The 16 "
                               "TB config is the outlier.")},
    "storage/hostbrr-storage-vps-hdd-block": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$5.00/TB/mo at the 1 TB block rate ($2.50/500 GB add-on, per LowEndSpirit thread 6258: 'additional "
                               "can be added for $2.5/month per 500 GB'). At 5 TB: Premium StorageBrr 2GB base ($7) + 4.5 TB of block "
                               "at $5/TB ($22.50) = $29.50/mo = $5.90/TB all-in. At 20 TB the block dominates: $7 + $97.50 = $104.…")},
    "storage/hostbrr-storagebox": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("16 TB €32.00 ÷ 16 = €2.00/TB/mo ≈$2.32 (best tier). 8 TB €2.06 · 4 TB €2.13 · 2 TB €2.25 · 1 TB €2.50 "
                               "· 500 GB €1.17/TB only when billed annually. Beats Hetzner BX41 on €/TB but gives 80 TB transfer "
                               "instead of unlimited — the trade is explicit.")},
    "storage/hostbrr-storagebox-16-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("List: $1.85/TB/mo at 16 TB ($355/yr), $1.93 at 8 TB. With BFBOX 40% recurring on yearly: 16 TB = "
                               "$213/yr = $1.11/TB/mo; 8 TB = $111/yr = $1.16/TB/mo; 4 TB = $57/yr = $1.19/TB/mo. 5 TB workload: 8 TB "
                               "plan = $1.16/TB/mo. 20 TB workload: two 16 TB boxes = $2.22/TB/mo (16 TB is their ceiling, so the di…")},
    "storage/hostbrr-storagebox-16tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("16TB: €32.00 -> €2.00/TB/mo ($2.22). 8TB: €16.50 -> €2.06/TB. 4TB: €8.50 -> €2.13/TB. 1TB: €2.50 -> "
                               "€2.50/TB")},
    "storage/hosthatch-storage-vm": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.80/TB/mo at 10 TB ($38/mo, 25 TB included). At 5 TB: $20/mo = $4.00/TB (12.5 TB included). At 20 "
                               "TB: two 10 TB VMs = $76/mo = $3.80/TB. Pricing is linear — no volume break — so the 10 TB rung is the "
                               "only sensible buy.")},
    "storage/hosting-by-design-app-hosting-24-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("24TB: €49.95 -> €2.08/TB/mo (~$2.39). 28TB: €59.95 -> €2.14/TB. 18TB: €39.95 -> €2.22/TB. 4TB: €10.95 "
                               "-> €2.74/TB. 1TB: €6.59 -> €6.59/TB")},
    "storage/hosting-mammoth-object-storage": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("$5.62/TB at 5 TB (EUR 24.99 = $28.07) and $5.62/TB at 20 TB (EUR 99.99 = $112.33), before the EUR "
                               "1/TB egress overage.")},
    "storage/hugging-face-storage-buckets-via-s3-gateway-as-an-annex": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 12 per TB-month public and USD 18 per TB-month private at the base tier; USD 10 and 16 from 50 "
                               "TB, USD 9 and 14 from 200 TB, USD 8 and 12 from 500 TB; public storage beyond a plan's base needs a "
                               "PRO, Team or Enterprise plan")},
    "storage/icedrive-3-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.33/TB/mo at 3 TB ($9.99). Lifetime 2 TB at $499 one-time = $1.04/TB/mo over 20 years, $2.08/TB/mo "
                               "over 10 years, $4.16/TB/mo over 5 years. 20 TB is not offered — the ladder stops at 3 TB, so this "
                               "cannot host the archive.")},
    "storage/icedrive-lifetime-personal-2-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-time $249.50/TB at 2 TB ($499). Over 5 years: $4.16/TB/mo. Over 10 years: $2.08/TB/mo. Expensive "
                               "relative to pCloud at the same capacity.")},
    "storage/idrive-e2": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 6 per TB per month pay-as-you-go, 1 TB minimum; yearly 10 TB plan USD 595.00 a year (USD 4.96 per "
                               "TB-month, derived: 595.00 / 10 / 12), half price in the first year")},
    "storage/ieee-dataport-data-competition-module": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("0 via Data Competition or IEEE Society membership. Otherwise the read side costs $480/yr for "
                               "unlimited datasets — at 2 TB that is $20/TB/year = $1.67/TB/month, which is below the wave-6 price "
                               "floor, and it is a read licence not a per-TB rate. Open Access publication is a flat $1,950 per "
                               "dataset, no…")},
    "storage/internxt-100-tb-lifetime": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-time: 100 TB at $999.99 = $10.00/TB once = $0.17/TB/mo amortised over 5 years. 50 TB at $699.99 = "
                               "$14.00/TB. 5 TB at $229.99 = $46.00/TB once = $0.77/TB/mo over 5 years. 5 TB workload: 5 TB SKU. 20 "
                               "TB workload: 50 TB SKU. Fails on programmatic access, not price.")},
    "storage/internxt-lifetime": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-time $27.00/TB at 10 TB ($269.97); $10.00/TB at 100 TB ($999.99). Amortised over 5 years: "
                               "$0.45/TB/mo at 10 TB, $0.17/TB/mo at 100 TB — nominally the cheapest number in this lane, and the "
                               "least trustworthy.")},
    "storage/interserver-storage-hosting-st-600": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.10/TB/mo at the 20 TB tier ($42) but with only 20 TB/mo of transfer. $2.50/TB/mo at the 10 TB tier "
                               "with 15 TB transfer. 5 TB workload: buy the 10 TB tier = $2.50/TB/mo. 20 TB workload: $2.10/TB/mo. "
                               "Cheap per TB, but egress = 1x storage makes it a trap for the 500 GB-1 TiB/day serving load.")},
    "storage/interserver-storage-st-600": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.10/TB/mo at 20 TB ($42). At 5 TB interpolating the 4 TB plan ($10, 10 TB transfer) → $2.50/TB/mo. "
                               "Egress is metered 1:1, which is the difference from Hetzner at the same price.")},
    "storage/interserver-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.00/TB/mo flat at 1, 5, 10, 20 TB — genuinely linear, no tier discount. Caveat: 2 TB transfer per "
                               "TB stored does not cover 30 TB/mo serving at 20 TB stored (40 TB included, so it does at 20 TB; it "
                               "fails at 10 TB stored where only 20 TB is included).")},
    "storage/ionos-cloud-object-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$4.99/TB at 5 TB and 20 TB for storage — but serving 20 TB/month costs $648 in egress alone (2 TB "
                               "free + 18 TB x $36/TB), i.e. effective $32/TB+.")},
    "storage/ionos-hidrive": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("2 TB $10/mo promo term = $5.00/TB, steady state unclear (the $10 is itself a 'Save 50%' off $20). 1 "
                               "TB $7/mo steady = $7.00/TB. Above 2 TB the product does not exist on the self-serve page, so it "
                               "cannot serve the 10 TiB hot tier.")},
    "storage/jottacloud": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$1.30/TB/mo at 10 TB, $0.65/TB/mo at 20 TB, $0.43/TB/mo at 30 TB (flat $12.99/mo 'Unlimited', "
                               "throttled above 5 TB)")},
    "storage/jottacloud-pro-20-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.20/TB at 20 TB ($64.01/mo); $3.20/TB at 30 TB ($96.08/mo); at 5 TB-equivalent the Pro 10 TB tier "
                               "is $6.39/TB")},
    "storage/keycdn-push-zone": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$120/TB stored (Push Zone, $0.12/GB); $40/TB delivered ($0.04/GB above 1 TB); Pull Zone storage $0."},
    "storage/kimsufi-ks-5": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$19.90 ÷ 8 TB = $2.49/TB/mo at the 2×4TB config; ÷ 12 TB (3×4TB) = $1.66/TB; ÷ 4 TB (2×2TB) = "
                               "$4.98/TB. Unlimited traffic, but 300 Mbps.")},
    "storage/koofr": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$7.86/TB at 5 TB (EUR 35 = $39.32); $7.86/TB at 2.5 TB; $11.23/TB at 1 TB. Lifetime 1 TB $159.99 = "
                               "$159.99/TB one-time, or $2.67/TB/mo over 5 years.")},
    "storage/kub-ua-file-cloud-nextcloud-backed-flat-per-tb-with-unli": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$8.16/TB/mo at 5 TB ($40.81/mo), $19.28/TB/mo at 1 TB ($19.28/mo). At 20 TB: $8.16/TB/mo if 4× the 5 "
                               "TB plan is allowed, derived. UAH at 0.022177 USD/UAH. Egress $0.")},
    "storage/kyun-host-bricks": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$5.62/TB/mo flat (€5). At 5 TB: €25 = $28.09/mo. At 20 TB: €100 = $112.34/mo. No volume break. The "
                               "caveats (20 TB total supply, price flagged to rise, provider's own no-SLA warning) make this a poor "
                               "primary and a reasonable third replica.")},
    "storage/load-network-load-s3": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$3.00 (0.003/GB/mo); permanent tier $11,900/TB one-time"},
    "storage/mail-ru-cloud-mail-1-tb-with-free-public-link-download": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$3.03/TB/mo at 1 TB steady state (₽3,000/yr = $36.33/yr). Trial year: $1.58/TB/mo (₽1,560 = $18.89). "
                               "At 5 TB and 20 TB: NOT AVAILABLE — the product ceiling is 4 TB, so no 5 TB or 20 TB price exists. "
                               "Egress free.")},
    "storage/mediafire": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$8.33/TB/mo (Pro, 1 TB)"},
    "storage/mediafire-pro-1-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$5.83/TB at 1 TB annual; cannot reach 5 TB or 20 TB on one plan — $29.15/TB/mo if you stacked five "
                               "Pro plans, which the ToS does not obviously permit")},
    "storage/mega-s4": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$4.94/TB at 5 TB (EUR 22.00 = $24.71); $4.18/TB at 20 TB (EUR 74.50 = $83.69)"},
    "storage/myqnapcloud-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$4.99/TB/mo with free egress (beta pricing for 1 TB)"},
    "storage/netcup-storage-space-local-block-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("Tariff C: €18.23 for the first 1 TB (€18.23/TB), then €0.024/GB = €24.58/TB for extra capacity — the "
                               "marginal TB is MORE expensive than the first, and the traffic cap freezes the volume. Local Block "
                               "Storage is €12.29/TB. Both are 6–12× Hetzner.")},
    "storage/netdynamics24-germany-backup-sftp": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("List: $6.00/TB/mo at 1 TB, $5.50/TB/mo at 2 TB. With LET50% on annual: 1 TB = $30/yr = $2.50/TB/mo; 2 "
                               "TB = $55/yr = $2.29/TB/mo. 5 TB workload: three 2 TB boxes = $2.29/TB/mo. 20 TB workload: same "
                               "$2.29/TB/mo but requires ten boxes. Unmetered 1 Gbit/s is the reason to care.")},
    "storage/novacloud-hosting-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$4.21/TB/mo at 2 TB (€7.50). At 5 TB: €3.50 base (2 TB) + 3 x €2 marginal = €9.50/mo = $10.67 for 5 "
                               "TB = $2.13/TB — the €2/TB marginal rate is the lowest of the storage providers compared, if the "
                               "provider will actually build the config. At 20 TB: €3.50 + 18 x €2 = €39.50/mo = $44.37 = $2.22/TB. "
                               "Sold out.")},
    "storage/openai-files-api-per-project-file-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("free (raw file storage); vector-store storage $0.10/GB/day after 1 GB — avoid attaching to vector "
                               "stores")},
    "storage/ovhcloud-cold-archive": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 1.84 per TB per month (USD 0.001971 per GiB-month x 931.32 GiB per TB); one rate at every volume"},
    "storage/ovhcloud-cold-archive@earlier": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$1.44/TB at 20 TB (EUR 25.60 = $28.76). Same rate at 5 TB ($1.44/TB). Lowest storage rate in the "
                               "entire survey — but archive-class, with a EUR 5/TB restore fee.")},
    "storage/ovhcloud-managed-private-registry": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 38.64 per TB per month on plan L (USD 212.43 a month for 5 TiB, which is 5.50 TB)"},
    "storage/ovhcloud-object-storage-one-zone-standard": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 7.55 per TB per month (USD 0.0081103 per GiB-month x 931.32 GiB per TB); one rate at every volume"},
    "storage/ovhcloud-object-storage-one-zone-standard-flat-s3-with-c": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": "PLN 33.05 per TB per month (PLN 0.0354853 per GiB-month x 931.32 GiB per TB); one rate at every volume",
        "free_tier": {
            "stated": ("No free tier: the Standard class in a 1-AZ (One Zone) region is billed from the first GiB at "
                       "0,00004861 PLN per GiB-hour (about 0,0354853 PLN per GiB-month) on the Polish price list, one rate at "
                       "every volume")}},
    "storage/ovhcloud-object-storage-one-zone-standard-flat-s3-with-c@earlier": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-Zone Standard: $9.34/TB/mo ($112.03/TB/yr) with free egress, free API calls, free retrieval — "
                               "identical at 5 TB and 20 TB because pricing is strictly per-GiB with no tiers. One-Zone Infrequent "
                               "Access: $4.55/TB/mo storage but +$2.27/TB per full read-back (0.01728 PLN/GiB) and a 30-day minimum, "
                               "s…")},
    "storage/ovhcloud-object-storage-standard": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": "USD 14.63 per TB per month for the first 50 TiB (USD 0.0157096 per GiB-month x 931.32 GiB per TB)"},
    "storage/packetstream": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$1024/TB (egress)"},
    "storage/pcloud-premium-plus-2-tb-ultra-10-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-time $249.50/TB at 2 TB ($499); $149.90/TB at 10 TB ($1,499). Amortised over 5 years: $4.16/TB/mo "
                               "at 2 TB, $2.50/TB/mo at 10 TB. At the $890 sale price for 10 TB: $1.48/TB/mo over 5 years.")},
    "storage/pcloud-ultra-10-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.999/TB/mo at 10 TB annual ($359.88/12). Monthly billing: $2.999/TB. Lifetime: €1499 one-time / 10 "
                               "TB; at a 3-year horizon that is €4.16/TB/mo, at 5 years €2.50/TB/mo.")},
    "storage/pikpak": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$0.50/TB/mo on US Premium ($4.99/mo for 10 TB); $1.00/TB/mo on Global Premium ($9.99/mo) — but capped "
                               "at 5 GB/day of egress through rclone, which dominates the economics")},
    "storage/pikpak-global-premium": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$0.833/TB/mo at 10 TB ($99.99/yr Global Premium). Looks like the cheapest per-TB number in this "
                               "dossier — and it is a trap. Usable programmatic egress is 1 TB/month (25% × 4 TB downstream). "
                               "Effective cost per TB actually retrievable per month is fine, but the ceiling makes it unusable for "
                               "serving o…")},
    "storage/prismdrive-10-tb-annual": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.075/TB/mo at 10 TB annual ($249/12). Cheapest-looking USD number after Blomp, but confidence is "
                               "low: unverifiable interface, lifetime-deal lineage, JS-gated pricing.")},
    "storage/proxyrack-unlimited-residential": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "n/a (egress only): $150/mo flat = $5/TB at 1 TiB/day"},
    "storage/pulsedmedia-m10g-storage-box": {
        "topic": "storage", "read_date": "2026-10-22",
        "price_per_tb_month": ("€1.69/TB/mo at the 16 TB tier (€26.99/16). 5 TB workload: buy the 8 TB tier = €1.87/TB/mo. 20 TB "
                               "workload: buy the 32 TB tier = €2.00/TB/mo. ~$1.83 / $2.02 / $2.16 at 1.08 USD/EUR. Black Friday "
                               "flash (8 TB, recurring, 15 units) = €1.02/TB/mo.")},
    "storage/pulsedmedia-m10g-storage-box-16tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("16TB: €26.99 -> €1.69/TB/mo (~$1.94). 32TB: €63.99 -> €2.00/TB. 8TB: €14.99 -> €1.87/TB. 4TB: €8.99 "
                               "-> €2.25/TB")},
    "storage/rollin-host-drive-empresarial-backup-storage-flat-per-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$7.56/TB/mo at 10 TB ($75.63/mo); $7.96/TB/mo at 5 TB ($39.80/mo); $15.91/TB/mo at 1 TB ($15.91/mo). "
                               "At 20 TB: $7.56/TB/mo if the 10 TB plan can be bought twice ($151.26/mo). BRL at 0.199082 USD/BRL. "
                               "Egress $0.")},
    "storage/rsync-net-standard": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("0-9TB: $15.00/TB/mo. 10-99TB: $12.50/TB. 100TB+: $7.50/TB. restic accounts: $10.00/TB (200 GB min). "
                               "openSUSE-developer Standard Single Region: $8.00/TB. openSUSE 500 GB tier is free-forever")},
    "storage/ruvds-russian-flat-rate-disk-vps-with-unlimited-traffic": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$11.50/TB/mo at 2 TB ($23.00/mo) and 4 TB ($46.00/mo); $12.39/TB/mo at 1 TB ($12.39/mo). At 20 TB: "
                               "~$11.50/TB/mo if two 10 TB-class configs are assembled ($230/mo), derived not quoted. Unlimited "
                               "traffic, $0 egress.")},
    "storage/scaleway-object-storage-glacier-class": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$2.85/TB at both 5 TB and 20 TB (EUR 2.54 = $2.85), plus EUR 10/TB on anything actually read out."},
    "storage/scramble-cloud-premium-6-tb-lifetime": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("One-time, so amortise: 6 TB at €279.95 = €46.66/TB once; over 5 years that is €0.78/TB/mo, over 3 "
                               "years €1.30/TB/mo. 20 TB SKU at $349.95 = $17.50/TB once = $0.29/TB/mo over 5 years. 5 TB workload: "
                               "the 6 TB SKU. 20 TB workload: the 20 TB SKU. The arithmetic is the best in the dossier and it is undo…")},
    "storage/seedhost-eu-hd-24": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("24TB: €55 -> €2.29/TB/mo (~$2.63). 18TB: €40.50 -> €2.25/TB. 12TB: €27 -> €2.25/TB. 4TB: €9 -> "
                               "€2.25/TB. 1TB: €3 -> €3.00/TB")},
    "storage/selectel-object-storage-coldest-tier-is-cheap-the-traffi": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("Ice: $11.04/TB/mo storage PLUS $24.31/TB for every full read-back (₽1.96/GB × 1024) — so one complete "
                               "retrieval costs 2.2 months of storage. Realistic cold-archive usage (store 1 TB, read 250 GB per "
                               "month): $11.04 + $6.08 = $17.12/TB/mo. At 50 % monthly read: $23.19/TB/mo. Identical at 5 TB and 20 …")},
    "storage/sellfy": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$22/mo on Starter; 20 GB/file, so ~$22 for unlimited-but-policed TB — priced per plan, not per TB. "
                               "Effectively $0/TB until policed.")},
    "storage/servarica-polar-bear-killer-whale-mammoth-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.50/TB/mo at 2 TB ($5/mo) and at 8 TB ($20/mo); $2.43/TB/mo at 3.5 TB. On yearly: Polar Bear $48/yr "
                               "= $2.00/TB/mo; Mammoth $220/yr = $2.29/TB/mo. 5 TB workload: 8 TB plan at $2.50/TB/mo (or 3x Polar "
                               "Bear at $2.00/TB/mo). 20 TB workload: 2.5x Mammoth = $2.29/TB/mo. Caveat: active billing outage, b…")},
    "storage/servarica-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.00-2.50/TB/mo. At 5 TB: Killer Whale 3.5 TB ($8.50) + Polar Bear 2 TB ($5) = $13.50/mo for 5.5 TB "
                               "= $2.45/TB. At 20 TB: 2x Mammoth 8 TB ($40) + Penguin 4 TB ($11.11) = $51.11/mo for 20 TB = $2.56/TB; "
                               "annual billing on the Mammoths drops it to $2.49/TB. Cheapest per-TB is Polar Bear at $2.00/TB o…")},
    "storage/sia-storage-app": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$2.00/TB at 10 TB tier; $4.99/TB above; 20 TiB = $69.89/mo"},
    "storage/snowflake-trial-account": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$40/TB/month storage after the trial (Standard). Above the wave-6 floor by ~8x."},
    "storage/spacebyte-cloud-150-tb-mo-claimed-the-lowest-credible-lo": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$1.58/TB/mo at 1 TB ($18.95/TB/yr) as advertised, $1.19/TB/mo on the ₹1,650/yr annual. At 5 TB and 20 "
                               "TB: NO PUBLISHED PLAN — the ladder stops at 1 TB and «Enterprise pooled storage» is quote-only, so "
                               "the 5 TB and 20 TB figures do not exist and the number cannot be used for the client's sizing.")},
    "storage/storadera-space-premium": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("€7.95/TB/mo flat at the 5 TB and 20 TB tiers ($8.59 at 1.08). 5 TB workload: €7.95/TB/mo. 20 TB "
                               "workload: €7.95/TB/mo. Priced like Wasabi, metered like InterServer — dominated on both axes.")},
    "storage/storj-object-storage-standard": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 7.00 per TB-month of storage on the Standard plan, plus USD 7.00 per TB of egress: USD 14.00 per "
                               "TB stored and read once in a month")},
    "storage/storj-object-storage-standard@earlier": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$7.00/TB at 5 TB and 20 TB for storage, plus $7.00/TB on every byte read — $14/TB effective at a 1:1 "
                               "read ratio.")},
    "storage/strato-hidrive-business": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("10 TB €90 ÷ 10 = €9.00/TB/mo. 5 TB €55 ÷ 5 = €11.00/TB. 3 TB €30 ÷ 3 = €10.00/TB. 1 TB €17.50/TB. "
                               "≈$10.44/TB at best. 4.4× Hetzner BX41 for the same capacity.")},
    "storage/synology-c2-object-storage": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$7.99/TB flat at both 5 TB and 20 TB"},
    "storage/systemfreaks-s3-compatible-object-storage-250-gb-free-du": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 6.00/TB/month on Standard (egress free up to 3x storage, then USD 1.00 per TB); USD 8.00/TB/month "
                               "on Unmetered (no egress fees)")},
    "storage/telnyx-cloud-storage": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 0.006 per GiB a month for US storage beyond the free 10 GiB (about USD 6.14 per TiB), USD 0.025 "
                               "per GiB a month in the EU (about USD 25.60 per TiB); beyond the free quotas, US operations cost USD "
                               "0.50 per million state-change and USD 0.04 per million read requests, EU operations USD 5.00 and USD "
                               "0.40 per million; minimum billable object size 4 KiB")},
    "storage/telnyx-object-storage": {
        "topic": "storage", "read_date": "2026-10-31",
        "price_per_tb_month": ("USD 0.006 per GiB a month for US storage beyond the free 10 GiB (about USD 6.14 per TiB), USD 0.025 "
                               "per GiB a month in the EU (about USD 25.60 per TiB); beyond the free quotas, US operations cost USD "
                               "0.50 per million state-change and USD 0.04 per million read requests, EU operations USD 5.00 and USD "
                               "0.40 per million; minimum billable object size 4 KiB")},
    "storage/telnyx-object-storage@earlier": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$6.14/TB stored (0.006/GiB), $0 egress, $0.04–0.50 per million operations."},
    "storage/thehost-ua-keepdata-10-tb-flat-with-traffic-included-web": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$5.95/TB/mo at 10 TB ($59.48/mo) and identically at 50 TB ($297.48/mo) — flat rate, unmetered "
                               "traffic, no volume discount at either end. Tier ladder is 25 GB / 100 GB / 500 GB / 1 TB / 10 TB / 50 "
                               "TB, so there is NO 5 TB SKU: 5 TB means buying 5× the 1 TB plan ($64.15/mo = $12.83/TB/mo, poor) or "
                               "1× …")},
    "storage/tigris": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 20.48 per TiB-month Standard, USD 10.24 Infrequent Access, USD 4.10 Archive or Archive Instant "
                               "Retrieval (USD 0.02, 0.01 and 0.004 per GB-month of 2^30 bytes, global or single-region); "
                               "multi-region USD 0.025, 0.015 and 0.006 per GB-month")},
    "storage/time4vps-storage-vps": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$4.68/TB/mo on the promo (€4.17), **$9.38/TB/mo at renewal (€8.35)**. At 5 TB: five 1 TB plans at "
                               "renewal = €41.75 = $46.90/mo = $9.38/TB. At 20 TB: €167 = $187.58/mo = $9.38/TB. This is the cleanest "
                               "example of the trial-vs-steady-state trap in the lane: the advertised €4.17 is a first-term rate ag…")},
    "storage/time4vps-storage-vps-1-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("Promotional: €4.17/TB/mo (24-mo term). Steady state: €8.35/TB/mo monthly; €9.28/TB/mo annual; "
                               "€11.99/TB list. Record the steady-state €8.35, not the €4.17.")},
    "storage/together-ai-files-api": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "$163.84 (Managed Storage at $0.16/GiB/mo) — 40-80x the cheap-paid floor; egress free"},
    "storage/uloz-to-disk": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$1.28/TB/mo at the 25 TB tier ($32) and at the 50 TB tier ($64). 5 TB workload: buy the 12 TB tier = "
                               "$1.33/TB/mo. 20 TB workload: buy the 25 TB tier = $1.28/TB/mo. Cheapest genuine $/TB/mo of anything "
                               "verified in this dossier.")},
    "storage/ultra-cc-platinum-28-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("28TB: €79.95 -> €2.86/TB/mo (~$3.28). 12TB: €38.95 -> €3.25/TB. 4TB: €13.95 -> €3.49/TB. 1TB: €6.50 "
                               "-> €6.50/TB")},
    "storage/upzur-premium": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$110/yr ÷ 12 = $9.17/mo for 'unlimited' — so there is no $/TB by construction, which is itself the "
                               "tell. If you value it at 20 TB it is $0.46/TB/mo and if you value it at 1 TB it is $9.17/TB/mo. "
                               "Priced per-account, capped by an unpublished bandwidth threshold, with hotlinking blocked by the "
                               "vendor's own rule and zero liabil…")},
    "storage/utho-archive-storage-0-38-gb-mo-cold-tier-denominated-no": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("Archive: $4.10/TB/mo at both 5 TB and 20 TB ($49.16/TB/yr), egress claimed $0. Standard object tier: "
                               "$20.53/TB/mo at 10 TB ($205.28/mo), $26.32/TB/mo at 5 TB, $37.73/TB/mo at 250 GB — so the standard "
                               "tier is 5× the archive tier at the same vendor. INR at 0.010527 USD/INR.")},
    "storage/wasabi-hot-cloud-storage": {
        "topic": "storage", "read_date": "2026-10-30",
        "price_per_tb_month": ("USD 7.99 per TB per month on Pay as You Go, billed per GB per day for actual usage, with a minimum "
                               "monthly charge tied to 1 TB of active storage per account and a 90-day minimum storage duration; "
                               "Reserved Capacity Storage is a fixed-rate block from 25 TB on a 1-, 3- or 5-year term, with discounts "
                               "set by capacity and term and a 30-day minimum storage duration")},
    "storage/webtropia-storage-server-ryz5-20": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("RYZ5-20 €109.99 ÷ 88 TB = €1.25/TB/mo raw ≈$1.45 — the lowest €/TB of the storage providers compared. "
                               "RYZ5-12 €79.99 ÷ 56 TB = €1.43/TB. RYZ7-20 €119.99 ÷ 88 = €1.36/TB. Caveat: egress term unpublished; "
                               "treat as unverified until confirmed in writing.")},
    "storage/whatbox-h3-22": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": "21.7TB: $64 -> $2.95/TB/mo. 15.8TB: $50 -> $3.16/TB. 9.9TB: $36 -> $3.64/TB. 3.9TB: $15 -> $3.85/TB"},
    "storage/yandex-360-3-tb-the-regional-price-floor-with-unlimited": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("RUB sheet (Russian card): $2.00/TB/mo at 3 TB ($5.99/mo); $3.83/TB/mo at 5 TB ($19.17/mo); "
                               "$7.27/TB/mo at 10 TB ($72.67/mo). USD sheet (foreign card — the client's real price): $4.17/TB/mo at "
                               "3 TB ($12.50/mo); $4.25/TB/mo at 5 TB ($21.25/mo); $3.17/TB/mo at 1 TB. Family variant: $3.03/TB/mo "
                               "per mem…")},
    "storage/zoolz-cloud-backup-12-tb": {
        "topic": "storage", "read_date": "2026-10-21",
        "price_per_tb_month": ("$2.78/TB at 12 TB ($399.99/yr = $33.33/mo); $2.86/TB at 7 TB ($239.99/yr); $2.67/TB at 2.5 TB "
                               "($79.99/yr). Cold tier only.")},
}


if __name__ == "__main__":
    sys.exit(main())
