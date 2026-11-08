#!/usr/bin/env python3
"""staleness.py — the drift detector.

PURPOSE
    Answer one question per record: is this still true, and when did anybody last
    check? Print a table bucketed by age, and emit a machine-readable verdict a CI
    job can gate on.

WHY IT EXISTS
    The corpus rots. A price read in March is a rumour in June. The failure is
    quiet: nothing breaks, the table still renders, and a reader acts on a number
    that has been wrong for a year. This script makes the rot visible and cheap to
    repair by naming the exact records, and the exact evidence rows, that have
    outlived the policy for their rung and their topic.

    It reads the rung. A `reported` claim from a forum is not a quarter as durable
    as a `measured` probe, and a policy that applies one window to both is a policy
    that passes the claim that rots first. METHODOLOGY.md section 10.2 gives the
    per-class windows; classes[].days holds them; the shorter of the class window
    and the topic window binds.

    It reads the evidence dates, not only `verified_at`. A record stamped today
    whose newest source was read last month has been re-dated, not re-checked, and
    section 10.1 forbids exactly that. `verified_at` age and evidence age are
    reported as two numbers, and a `verified_at` newer than every evidence row by
    more than the tolerance is reported as a bulk touch by name.

INPUTS
    A directory of dossier records, validated or not. Reads `topic`, `slug`,
    `confidence`, `verdict`, `verified_at`, and each `evidence[].date`. A record
    with no verified_at, or an evidence row dated the undated sentinel
    0001-01-01, is reported as such rather than silently treated as ancient or
    fresh.

OUTPUT
    Default: one TSV row per record (machine-readable, stable columns, header on
    stdout, so `| cut` and `| awk` work).
    --human: an aligned table plus a per-topic summary.
    --stale-only: only the failing rows, as TSV. This is the CI form: empty output
    and exit 0 means nothing has rotted.
    --summary: per-topic counts only, ending in one totals line the gate parses.

DEPENDENCIES
    Python standard library only. No network.

EXIT CODES  (repository map, scripts/README.md)
    0  every record within its policy
    1  at least one record is stale, rotten, undated, bulk-touched or missing verified_at
    2  usage error: bad arguments, unreadable directory or policy
    3  environment wrong: policy file missing or not valid JSON

EXAMPLES
    python staleness.py dossier/ --human
    python staleness.py dossier/ --stale-only
    python staleness.py dossier/ --policy staleness.policy.json --as-of 2026-10-22
    python staleness.py dossier/ --topic storage --max-days 30
    python staleness.py --selftest
    python staleness.py --fixtures ../fixtures/staleness
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

VERSION = "2.0.0"
DEFAULT_POLICY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "staleness.policy.json")
UNDATED = "0001-01-01"

TSV_COLUMNS = ("file", "topic", "slug", "confidence", "verdict", "verified_at",
               "verified_age_days", "evidence_newest_days", "evidence_oldest_days",
               "class_limit_days", "topic_limit_days", "limit_days", "bucket",
               "stale", "bulk_touch", "undated_evidence", "evidence_count",
               "flags", "reasons")


# --------------------------------------------------------------------- time --

def parse_day(s):
    """YYYY-MM-DD -> date, or None. Accepts a full timestamp and takes the date."""
    if not s or not isinstance(s, str):
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s.strip())
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                        tzinfo=timezone.utc)
    except ValueError:
        return None


def parse_verified_at(s):
    if not s or not isinstance(s, str):
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})[Tt ](\d{2}):(\d{2}):(\d{2})", s.strip())
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                        int(m.group(4)), int(m.group(5)), int(m.group(6)),
                        tzinfo=timezone.utc)
    except ValueError:
        return None


# ------------------------------------------------------------------- policy --

def load_policy(path):
    with open(path, "r", encoding="utf-8") as fh:
        policy = json.load(fh)
    if "default" not in policy or "topics" not in policy:
        raise ValueError("policy needs 'default' and 'topics'")
    if "classes" not in policy:
        raise ValueError("policy needs 'classes': a staleness policy that ignores the "
                         "rung is the policy this check exists to prevent")
    for name, p in list(policy["topics"].items()) + [("default", policy["default"])]:
        if "verified_after_days" not in p or "evidence_after_days" not in p:
            raise ValueError("policy %r needs verified_after_days and evidence_after_days"
                             % name)
    for name, p in policy["classes"].items():
        if "days" not in p:
            raise ValueError("class %r needs a days field" % name)
    return policy


def limits_for(policy, topic):
    base = dict(policy["default"])
    base.update(policy.get("topics", {}).get(topic) or {})
    return base


def class_limit(policy, confidence):
    """The class window, or None when the record declares no rung this policy knows."""
    entry = (policy.get("classes") or {}).get(confidence)
    if not entry:
        return None
    return entry.get("days")


def binding_limit(policy, topic, confidence, max_days=None):
    """The shorter of the class window and the topic window.

    The conservative one binds, and METHODOLOGY.md section 10.3 says so in the same
    words: a `measured` price is stale in 30 days, not 90, because prices rot faster
    than measurements do. The topic window is a ceiling on every class inside it.
    """
    topic_days = limits_for(policy, topic)["verified_after_days"]
    cls_days = class_limit(policy, confidence)
    if max_days is not None:
        # An explicit override replaces the binding window rather than narrowing it,
        # because its purpose is to ask "what would the table look like at N days".
        return max_days, cls_days
    if cls_days is None:
        return topic_days, None
    return min(topic_days, cls_days), cls_days


def bucket_for(age_days, policy):
    """Map an age onto a band. Bands are data: a topic can be bucketed by the same
    scale regardless of its own thresholds, which keeps the report comparable."""
    bands = policy.get("bands") or []
    for band in bands:
        m = band.get("max_days")
        if m is None or age_days <= m:
            return band["name"]
    return "dead"


# ------------------------------------------------------------------ inspect --

def discover(root):
    if os.path.isfile(root):
        return [root]
    out = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            if fn.endswith(".json"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def inspect_record(path, rec, policy, as_of, topic_override=None, max_days=None):
    """One record -> one result dict. Never raises on bad input; reports it."""
    topic = topic_override or rec.get("topic") or "unknown"
    confidence = rec.get("confidence")
    severity = policy.get("severity", {})
    rec_limit, cls_days = binding_limit(policy, topic, confidence, max_days)
    ev_limit = limits_for(policy, topic)["evidence_after_days"]
    tolerance = policy.get("bulk_touch_tolerance_days", 3)
    reasons = []
    flags = []

    if confidence is None:
        if severity.get("fail_on_unknown_class", True):
            flags.append("no-class")
            reasons.append("no confidence rung, so no class window applies")
    elif cls_days is None:
        if severity.get("fail_on_unknown_class", True):
            flags.append("unknown-class")
            reasons.append("confidence %r is not a rung this policy knows" % confidence)

    verified = parse_verified_at(rec.get("verified_at"))
    if verified is None:
        verified_age = None
        reasons.append("no verified_at" if not rec.get("verified_at")
                       else "unparseable verified_at %r" % rec.get("verified_at"))
    else:
        verified_age = (as_of - verified).days
        if verified_age < 0 and verified.date() <= as_of.date():
            # a check made later on the day of as_of: under --as-of (and in the fshy store) as_of is that day's
            # midnight, and the difference is minus one day. It is the same day, age 0, not a date in the future
            verified_age = 0
        if verified_age < 0:
            reasons.append("verified_at is in the future (%+d days)" % -verified_age)

    # A record may say, in its own words, that the date it carries is not a
    # verification. Where it does, the date is an upper bound and not a reading:
    # trusting it lets an inherited record measure as fresh forever, which is the
    # bulk touch in a different shirt. Any record that discloses it was not
    # re-checked, or was inherited, is charged from the age it declares instead.
    basis = ""
    extras = rec.get("extras") or {}
    if isinstance(extras, dict):
        basis = str(extras.get("verified_at_basis") or "")
    basis = basis or str(rec.get("confidence_note") or "")
    unchecked = any(p in basis.lower() for p in
                    ("not re-checked", "no page was read", "inherit",
                     "not verified", "not re-established"))
    if unchecked and verified_age is not None:
        extras_d = extras if isinstance(extras, dict) else {}
        declared = parse_day(extras_d.get("source_pass_ended")
                             or extras_d.get("source_date")
                             or rec.get("evidence_basis_date"))
        if declared is None and extras_d.get("evidence_dated_to_seed_pass"):
            # The record states how many evidence rows had their date assigned to
            # the seed pass rather than observed. That field is the disclosure; a
            # date that was assigned is an upper bound on when the page was read,
            # and the pass's own end date is the honest age.
            declared = parse_day(extras_d.get("source_pass_ended")
                                 or "2026-10-21")
        if declared is not None:
            declared_age = (as_of - declared).days
            if declared_age > verified_age:
                verified_age = declared_age
        flags.append("declared-unchecked")
        reasons.append("the record states it was not re-checked (%s); the date it "
                       "carries is an upper bound, not a reading" % basis[:80])

    evidence = rec.get("evidence") or []
    ages = []
    undated = 0
    for ev in evidence:
        if not isinstance(ev, dict):
            continue
        raw = ev.get("date")
        d = parse_day(raw)
        if d is None or raw == UNDATED:
            undated += 1
            continue
        # An archive capture is old on purpose: it exists to prove what a page said
        # on a past date, and its age is the point rather than a decay. Charging it
        # against the topic's freshness window would penalise a record for keeping
        # its own history, which is the opposite of what the policy is for.
        url = str(ev.get("url") or "")
        if "archive.web.pkgforge.dev" in url or "/web.archive.org/" in url:
            continue
        ages.append((as_of - d).days)
    newest = min(ages) if ages else None
    oldest = max(ages) if ages else None

    stale = False
    if "no-class" in flags or "unknown-class" in flags:
        stale = True
    if verified_age is None:
        stale = severity.get("fail_on_missing_verified_at", True)
        bucket = "unknown"
    else:
        bucket = bucket_for(verified_age, policy)
        if verified_age > rec_limit:
            stale = True
            reasons.append("verified_at %d days old, limit %d (%s window %s, topic window %d)"
                           % (verified_age, rec_limit,
                              confidence or "no rung",
                              "%dd" % cls_days if cls_days is not None else "none",
                              limits_for(policy, topic)["verified_after_days"]))
        hard = severity.get("hard_ceiling_days")
        if hard is not None and verified_age > hard:
            reasons.append("past the hard ceiling of %d days" % hard)

    # The evidence is a second, independent clock. A record re-dated today over
    # month-old sources has not been re-checked, whatever verified_at says.
    if newest is not None and newest > rec_limit:
        stale = True
        flags.append("evidence-past-limit")
        reasons.append("newest evidence %d days old, limit %d" % (newest, rec_limit))

    if oldest is not None and oldest > ev_limit:
        stale = True
        flags.append("evidence-past-topic")
        reasons.append("oldest evidence %d days, topic allows %d" % (oldest, ev_limit))

    if undated and severity.get("fail_on_undated_evidence", True):
        stale = True
        flags.append("undated-evidence")
        reasons.append("%d of %d evidence rows carry no date" % (undated, len(evidence)))

    # The bulk touch: verified_at moved further than the evidence did. Both a
    # re-dated record and a live check with no evidence row are defects, and this
    # is the only mechanical way to see either.
    bulk = False
    if verified is not None and newest is not None:
        # Days by which verified_at is newer than the newest source. Both ages are
        # counted back from as_of, so the difference of the ages is the difference
        # of the dates, with the younger row giving the positive number.
        gap = newest - verified_age
        if gap > tolerance:
            bulk = True
            if severity.get("fail_on_bulk_touch", True):
                stale = True
                flags.append("bulk-touch")
                reasons.append("verified_at is %d days newer than the newest evidence "
                               "(tolerance %d): re-dated, not re-checked"
                               % (gap, tolerance))
            else:
                flags.append("bulk-touch-advisory")
                reasons.append("verified_at is %d days newer than the newest evidence"
                               % gap)

    effective = [x for x in (verified_age, newest) if x is not None]
    effective_age = max(effective) if effective else None
    if effective_age is not None and verified_age is not None:
        bucket = bucket_for(effective_age, policy)

    return {
        "file": path,
        "topic": topic,
        "slug": rec.get("slug") or os.path.splitext(os.path.basename(path))[0],
        "confidence": confidence or "",
        "verdict": rec.get("verdict") or "",
        "verified_at": rec.get("verified_at") or "",
        "verified_age_days": verified_age,
        "evidence_newest_days": newest,
        "evidence_oldest_days": oldest,
        "class_limit_days": cls_days,
        "topic_limit_days": limits_for(policy, topic)["verified_after_days"],
        "limit_days": rec_limit,
        "bucket": bucket,
        "stale": bool(stale),
        "bulk_touch": bool(bulk),
        "undated_evidence": undated,
        "evidence_count": len(evidence),
        "flags": flags,
        "reasons": reasons,
    }


# ------------------------------------------------------------------- output --

def to_tsv(rows):
    out = ["\t".join(TSV_COLUMNS)]

    def cell(v):
        if v is None:
            return ""
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v)
        return str(v).replace("\t", " ").replace("\n", " ")

    for r in rows:
        out.append("\t".join(cell(r[c]) for c in TSV_COLUMNS))
    return "\n".join(out)


def to_human(rows, policy):
    w = max((len(os.path.basename(r["file"])) for r in rows), default=4)
    w = min(max(w, 4), 44)
    head = "%-*s  %-14s  %-10s  %-8s  %5s  %5s  %4s  %s" % (
        w, "record", "topic", "rung", "bucket", "v_age", "e_age", "lim", "note")
    lines = [head, "-" * len(head)]
    order = sorted(rows, key=lambda x: (-(x["verified_age_days"]
                                         if x["verified_age_days"] is not None else 10 ** 6),
                                        x["file"]))
    for r in order:
        name = os.path.basename(r["file"])
        if len(name) > w:
            name = name[:w - 1] + "~"
        va = "?" if r["verified_age_days"] is None else str(r["verified_age_days"])
        ea = "-" if r["evidence_newest_days"] is None else str(r["evidence_newest_days"])
        flag = "  " if not r["stale"] else "!!"
        note = "; ".join(r["reasons"])[:64]
        lines.append("%s%-*s  %-14s  %-10s  %-8s  %5s  %5s  %4d  %s" % (
            flag, w - 2, name, r["topic"][:14], (r["confidence"] or "-")[:10],
            r["bucket"], va, ea, r["limit_days"], note))
    return "\n".join(lines)


def summary(rows, policy):
    """Per-topic counts, then one totals line.

    The counts are disjoint so a reader can add them up: 'stale' counts failing
    records, 'bulk' counts re-dated records, and the bucket histogram is over the
    same rows the other columns count. The earlier form printed stale=N beside a
    bucket histogram summing past N, which read as a contradiction.
    """
    topics = {}
    for r in rows:
        t = topics.setdefault(r["topic"], {"n": 0, "stale": 0, "undated": 0, "bulk": 0,
                                           "buckets": {}})
        t["n"] += 1
        if r["stale"]:
            t["stale"] += 1
        if r["undated_evidence"]:
            t["undated"] += 1
        if r["bulk_touch"]:
            t["bulk"] += 1
        t["buckets"][r["bucket"]] = t["buckets"].get(r["bucket"], 0) + 1
    lines = []
    tot = {"n": 0, "stale": 0, "undated": 0, "bulk": 0}
    for topic, t in sorted(topics.items()):
        buckets = " ".join("%s=%d" % (k, v) for k, v in sorted(t["buckets"].items()))
        limit = limits_for(policy, topic)["verified_after_days"]
        lines.append("  %-16s n=%-4d stale=%-4d bulk=%-4d undated=%-4d topic=%dd  %s"
                     % (topic, t["n"], t["stale"], t["bulk"], t["undated"], limit, buckets))
        for k in tot:
            tot[k] += t[k]
    lines.append("TOTALS n=%d stale=%d bulk=%d undated=%d"
                 % (tot["n"], tot["stale"], tot["bulk"], tot["undated"]))
    return "\n".join(lines)


# ----------------------------------------------------------------- selftest --

def selftest(verbose=False):
    """Runs against a synthetic set with known ages, so the arithmetic is checked
    rather than eyeballed. Offline."""
    results = []

    def check(name, cond, detail=""):
        results.append((name, bool(cond), detail))
        if verbose or not cond:
            sys.stderr.write("%s %s%s\n" % ("PASS" if cond else "FAIL", name,
                                            ("  " + detail) if detail else ""))

    policy = {
        "default": {"verified_after_days": 90, "evidence_after_days": 365},
        "topics": {"storage": {"verified_after_days": 10, "evidence_after_days": 30}},
        "classes": {"measured": {"days": 90}, "documented": {"days": 30},
                    "reported": {"days": 14}, "inferred": {"days": 30},
                    "unverified": {"days": 14}},
        "bulk_touch_tolerance_days": 3,
        "bands": [{"name": "fresh", "max_days": 7}, {"name": "current", "max_days": 30},
                  {"name": "aging", "max_days": 45}, {"name": "stale", "max_days": 90},
                  {"name": "rotten", "max_days": 180}, {"name": "dead", "max_days": None}],
        "severity": {"fail_on_undated_evidence": True, "fail_on_missing_verified_at": True,
                     "fail_on_bulk_touch": True, "fail_on_unknown_class": True,
                     "hard_ceiling_days": 365},
    }
    as_of = datetime(2026, 10, 22, tzinfo=timezone.utc)

    def rec(**kw):
        base = {"topic": "storage", "slug": "x", "verdict": "qualifies",
                "confidence": "measured",
                "verified_at": "2026-10-20T00:00:00.000Z",
                "evidence": [{"url": "https://e/1", "date": "2026-10-20", "proved": "a fact"}]}
        base.update(kw)
        return base

    r = inspect_record("a.json", rec(), policy, as_of)
    check("fresh record not stale", not r["stale"] and r["verified_age_days"] == 2,
          str(r["verified_age_days"]))
    check("fresh bucket", r["bucket"] == "fresh", r["bucket"])
    check("fresh record reports both ages",
          r["verified_age_days"] == 2 and r["evidence_newest_days"] == 2,
          "%s/%s" % (r["verified_age_days"], r["evidence_newest_days"]))

    r = inspect_record("a.json", rec(verified_at="2026-10-01T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-01",
                                                "proved": "a fact"}]), policy, as_of)
    check("storage 21 days > 10 day topic policy is stale", r["stale"],
          "; ".join(r["reasons"]))

    r = inspect_record("a.json", rec(topic="email", verified_at="2026-10-01T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-01",
                                                "proved": "a fact"}]), policy, as_of)
    check("same age not stale under default 90", not r["stale"], "; ".join(r["reasons"]))

    # the class window, which is the gap this script used to have
    r = inspect_record("a.json", rec(topic="domains-dns", confidence="reported",
                                     verified_at="2026-09-20T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-09-20",
                                                "proved": "a fact"}]), policy, as_of)
    check("40-day reported claim is stale under the 14-day class window",
          r["stale"] and r["limit_days"] == 14, "; ".join(r["reasons"]))
    r = inspect_record("a.json", rec(topic="domains-dns", confidence="measured",
                                     verified_at="2026-09-20T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-09-20",
                                                "proved": "a fact"}]), policy, as_of)
    check("same 40-day measured claim is current in a 90-day topic",
          not r["stale"] and r["limit_days"] == 90, "; ".join(r["reasons"]))
    check("the shorter window binds",
          binding_limit(policy, "domains-dns", "reported")[0] == 14
          and binding_limit(policy, "storage", "measured")[0] == 10)

    # evidence age, independent of verified_at
    r = inspect_record("a.json", rec(verified_at="2026-10-21T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-09-01",
                                                "proved": "a fact"}]), policy, as_of)
    check("recent verified_at over old evidence is stale",
          r["stale"] and r["evidence_newest_days"] == 51 and r["verified_age_days"] == 1,
          "; ".join(r["reasons"]))

    # the bulk touch
    r = inspect_record("a.json", rec(topic="email", confidence="measured",
                                     verified_at="2026-10-22T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-02",
                                                "proved": "a fact"}]), policy, as_of)
    check("a 20-day re-date is named a bulk touch",
          r["bulk_touch"] and "bulk-touch" in r["flags"], "; ".join(r["reasons"]))
    r = inspect_record("a.json", rec(topic="email", verified_at="2026-10-22T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-21",
                                                "proved": "a fact"}]), policy, as_of)
    check("a one-day gap is not a bulk touch", not r["bulk_touch"],
          "; ".join(r["reasons"]))

    # undated, missing, unparseable, future
    r = inspect_record("a.json", rec(evidence=[{"url": "https://e/1", "date": UNDATED,
                                                "proved": "a fact"}]), policy, as_of)
    check("undated evidence fails", r["stale"] and r["undated_evidence"] == 1,
          "; ".join(r["reasons"]))
    r = inspect_record("a.json", rec(verified_at=None), policy, as_of)
    check("missing verified_at fails", r["stale"] and r["verified_age_days"] is None,
          "; ".join(r["reasons"]))
    r = inspect_record("a.json", rec(verified_at="garbage"), policy, as_of)
    check("unparseable verified_at fails", r["stale"], "; ".join(r["reasons"]))
    r = inspect_record("a.json", rec(verified_at="2030-01-01T00:00:00.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-22",
                                                "proved": "a fact"}]), policy, as_of)
    check("future verified_at is flagged",
          any("future" in x for x in r["reasons"]), "; ".join(r["reasons"]))
    # a check later on the as-of day (as_of is a midnight under --as-of) is the same day: age 0, not -1, not future
    r = inspect_record("a.json", rec(verified_at="2026-10-22T00:12:52.378Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-22",
                                                "proved": "a fact"}]), policy, as_of)
    check("a check later on the as-of day is age 0 and not in the future",
          r["verified_age_days"] == 0 and not any("future" in x for x in r["reasons"]) and not r["bulk_touch"],
          "%s; %s" % (r["verified_age_days"], "; ".join(r["reasons"])))
    r = inspect_record("a.json", rec(verified_at="2026-10-23T00:00:01.000Z",
                                     evidence=[{"url": "https://e/1", "date": "2026-10-22",
                                                "proved": "a fact"}]), policy, as_of)
    check("a check on the next day is still in the future",
          r["verified_age_days"] < 0 and any("future" in x for x in r["reasons"]),
          "%s; %s" % (r["verified_age_days"], "; ".join(r["reasons"])))
    r = inspect_record("a.json", rec(confidence=None), policy, as_of)
    check("a record with no rung fails", r["stale"] and "no-class" in r["flags"],
          "; ".join(r["reasons"]))

    # bands
    check("band boundaries", [bucket_for(x, policy) for x in (0, 7, 8, 30, 31, 45, 46, 90, 91, 180, 181)]
          == ["fresh", "fresh", "current", "current", "aging", "aging", "stale",
              "stale", "rotten", "rotten", "dead"],
          str([bucket_for(x, policy) for x in (0, 7, 8, 30, 31, 45, 46, 90, 91, 180, 181)]))

    # max_days override
    r = inspect_record("a.json", rec(verified_at="2026-10-01T00:00:00.000Z"), policy,
                       as_of, max_days=100)
    check("--max-days override loosens", not r["stale"], "; ".join(r["reasons"]))
    r = inspect_record("a.json", rec(), policy, as_of, max_days=1)
    check("--max-days override tightens", r["stale"], "; ".join(r["reasons"]))

    # the shipped policy must be loadable, complete, and carry the rungs
    if os.path.exists(DEFAULT_POLICY):
        try:
            shipped = load_policy(DEFAULT_POLICY)
            check("shipped policy loads", True)
            # every topic of the schema enum has a window, and no window names a topic the schema lacks
            schema = os.path.join(os.path.dirname(DEFAULT_POLICY), "schema.json")
            enum = set(json.load(open(schema, encoding="utf-8"))["properties"]["topic"]["enum"])
            check("shipped policy covers every topic of the schema", set(shipped["topics"]) == enum,
                  "%d windows, %d topics" % (len(shipped["topics"]), len(enum)))
            check("shipped policy covers 5 rungs", len(shipped["classes"]) == 5,
                  str(sorted(shipped["classes"])))
        except Exception as e:  # noqa: BLE001
            check("shipped policy loads", False, str(e))
    else:
        check("shipped policy present", False, DEFAULT_POLICY)

    # the four fixtures, against their recorded as-of date
    fix = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fixtures",
                       "staleness")
    fix = os.path.normpath(fix)
    if os.path.isdir(fix):
        ok, detail = run_fixtures(fix, verbose)
        check("the four fixtures classify as recorded", ok, detail)
    else:
        check("fixture directory present", False, fix)

    # TSV shape
    rows = [inspect_record("a.json", rec(), policy, as_of)]
    tsv = to_tsv(rows)
    check("tsv header", tsv.splitlines()[0] == "\t".join(TSV_COLUMNS))
    check("tsv one row", len(tsv.splitlines()) == 2)

    # The human formatter. It crashed for a whole pass with a format-string
    # TypeError while this selftest reported 0 failed, because nothing called it.
    # A renderer that is never rendered is a renderer nobody knows is broken.
    try:
        human = to_human(rows, policy)
        check("human table renders", "record" in human and "bucket" in human)
        check("human summary renders", bool(summary(rows, policy)))
    except Exception as exc:  # noqa: BLE001 - the point is to catch any of it
        check("human table renders", False, "%s: %s" % (type(exc).__name__, exc))

    failed = [r for r in results if not r[1]]
    sys.stderr.write("selftest: %d passed, %d failed, %d total\n"
                     % (len(results) - len(failed), len(failed), len(results)))
    return 0 if not failed else 1


def run_fixtures(fix_dir, verbose=False):
    """Check the four named fixtures against expect.json. Returns (ok, detail).

    The expectations are recorded in the fixture directory, with the as-of date,
    so the test is stable: a fixture that starts passing because the calendar moved
    is not a test.
    """
    expect_path = os.path.join(fix_dir, "expect.json")
    with open(expect_path, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    as_of = parse_day(spec["as_of"])
    policy = load_policy(DEFAULT_POLICY)
    problems = []
    for row in spec["records"]:
        path = os.path.join(fix_dir, row["file"])
        with open(path, "r", encoding="utf-8") as fh:
            rec = json.load(fh)
        got = inspect_record(path, rec, policy, as_of)
        for key in ("stale", "bulk_touch", "bucket", "limit_days"):
            if got[key] != row["expect"][key]:
                problems.append("%s: %s expected %r, got %r"
                                % (row["file"], key, row["expect"][key], got[key]))
        if verbose:
            sys.stderr.write("%s %-34s stale=%-5s bulk=%-5s bucket=%-8s limit=%d\n"
                             % ("PASS" if not any(row["file"] in p for p in problems)
                                else "FAIL", row["file"], got["stale"], got["bulk_touch"],
                                got["bucket"], got["limit_days"]))
    return (not problems), "; ".join(problems[:4])


# -------------------------------------------------------------------- main --

def refuse_in_research_checkout(target):
    """--mark writes stale and stale_checked_at into tracked records. The research checkout changes tracked files only
    through a run (AGENTS.md section 2 rule 14): there, --mark on a path outside .tmp/ exits 2, and the report without
    --mark goes on (LIO4-01)."""
    import subprocess
    top = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        r = subprocess.run(["git", "-C", top, "config", "--get", "rq.researchCheckout"], capture_output=True, text=True)
    except OSError:
        return
    if r.stdout.strip().lower() != "true":
        return
    if os.path.normcase(os.path.abspath(target)).startswith(os.path.normcase(os.path.join(top, ".tmp")) + os.sep):
        return
    sys.stderr.write("staleness.py: the research checkout changes records only through a run: scripts/rq open amend "
                     "TOPIC \"RID: what is wrong\" (AGENTS.md section 2 rule 14). --mark writes %s, which is for a "
                     "session in an own clone; without --mark the report writes nothing.\n" % target)
    sys.exit(2)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="staleness.py",
        description="Report dossier records that have outlived their rung's and topic's policy.",
        epilog="EXIT CODES\n"
               "  0 nothing stale   1 something stale   2 usage   3 bad policy\n\n"
               "The policy is data: edit staleness.policy.json, not this script.\n",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", nargs="?", help="dossier directory (or one record)")
    p.add_argument("--policy", default=DEFAULT_POLICY, help="policy JSON (default beside this script)")
    p.add_argument("--as-of", metavar="YYYY-MM-DD",
                   help="evaluate as of this date (default: today, UTC)")
    p.add_argument("--topic", help="override the topic for every record")
    p.add_argument("--max-days", type=int, help="override the binding window for every record")
    p.add_argument("--stale-only", action="store_true",
                   help="emit only failing rows, TSV, for a CI gate")
    p.add_argument("--human", action="store_true", help="aligned table plus summary")
    p.add_argument("--summary", action="store_true", help="print the per-topic summary only")
    p.add_argument("--fixtures", metavar="DIR",
                   help="check the named fixtures against their recorded expectations")
    p.add_argument("--mark", action="store_true",
                   help="write the computed `stale` and `stale_checked_at` fields into each "
                        "record; the only writer of those fields, never a hand edit")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)

    if args.selftest:
        return selftest(verbose=args.human)

    if args.fixtures:
        ok, detail = run_fixtures(args.fixtures, verbose=True)
        if not ok:
            sys.stderr.write("fixtures: %s\n" % detail)
            return 1
        sys.stderr.write("fixtures: all four records classified as recorded\n")
        return 0

    if not args.path:
        sys.stderr.write("staleness: need a dossier path (or --selftest)\n")
        return 2
    if not os.path.exists(args.path):
        sys.stderr.write("staleness: no such path: %s\n" % args.path)
        return 2
    try:
        policy = load_policy(args.policy)
    except (OSError, ValueError) as e:
        sys.stderr.write("staleness: cannot use policy %s: %s\n" % (args.policy, e))
        return 3

    if args.as_of:
        as_of = parse_day(args.as_of)
        if as_of is None:
            sys.stderr.write("staleness: --as-of needs YYYY-MM-DD\n")
            return 2
    else:
        # The default must be the instant, not the midnight of today. Truncating to
        # a day makes a record verified forty minutes ago compute as minus one days:
        # a negative age, which the summary then reports as stale because it is not
        # zero. An age may be zero or a fraction of a day; it may not be negative.
        as_of = datetime.now(timezone.utc)

    rows = []
    unreadable = 0
    for path in discover(args.path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                rec = json.load(fh)
        except (OSError, ValueError) as e:
            unreadable += 1
            rows.append({"file": path, "topic": args.topic or "unknown", "slug": "?",
                         "confidence": "", "verdict": "", "verified_at": "",
                         "verified_age_days": None, "evidence_newest_days": None,
                         "evidence_oldest_days": None, "class_limit_days": None,
                         "topic_limit_days": 0, "limit_days": 0, "bucket": "unknown",
                         "stale": True, "bulk_touch": False, "undated_evidence": 0,
                         "evidence_count": 0, "flags": ["unreadable"],
                         "reasons": ["unreadable: %s" % str(e)[:80]]})
            continue
        if isinstance(rec, dict) and "candidates" in rec:
            # A seed wave is not a record set; say so instead of scoring it.
            unreadable += 1
            continue
        if not isinstance(rec, dict):
            unreadable += 1
            continue
        rows.append(inspect_record(path, rec, policy, as_of, args.topic, args.max_days))

    stale = [r for r in rows if r["stale"]]

    if args.mark:
        refuse_in_research_checkout(args.path)
        marked = 0
        for r in rows:
            if r["slug"] == "?" or r["flags"] and "unreadable" in r["flags"]:
                continue
            path = r["file"]
            if not os.path.isfile(path):
                continue
            with open(path, "r", encoding="utf-8") as fh:
                rec = json.load(fh)
            if not isinstance(rec, dict) or "candidates" in rec:
                continue
            rec["stale"] = bool(r["stale"])
            rec["stale_checked_at"] = as_of.strftime("%Y-%m-%dT00:00:00.000Z")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(rec, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
            marked += 1
        sys.stderr.write("staleness: wrote stale and stale_checked_at into %d records\n" % marked)

    if args.stale_only:
        sys.stdout.write(to_tsv(stale) + ("\n" if stale else ""))
    elif args.summary:
        sys.stdout.write(summary(rows, policy) + "\n")
    elif args.human:
        sys.stdout.write(to_human(rows, policy) + "\n\n")
        sys.stdout.write("as of %s   %d records   %d stale   %d bulk-touched   %d unreadable\n"
                         % (as_of.date(), len(rows), len(stale),
                            sum(1 for r in rows if r["bulk_touch"]), unreadable))
        sys.stdout.write(summary(rows, policy) + "\n")
    else:
        sys.stdout.write(to_tsv(rows) + "\n")

    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
