#!/usr/bin/env python3
"""Promote raw wave findings into dossier records.

The research waves write findings to `.tmp/wave2/<agent>/findings.json` because a
half-written record inside `dossier/` fails the gate for every agent still
running. This script is the second half: it turns those findings into records
that satisfy `scripts/dossier/schema.json`, and it refuses to touch a record that
already exists.

Usage:

    python scripts/dossier/promote.py --findings .tmp/wave2 --out dossier/compute --dry-run
    python scripts/dossier/promote.py --findings .tmp/wave2 --out dossier/compute

Exit codes:

    0   wrote, or dry run found nothing to refuse
    1   one or more findings could not be mapped; the report names them
    2   usage
    3   environment: a findings file is unparseable or the schema is missing
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

MARKERS = ("\u26d4", "\u2b50", "\u26a0", "\u2705", "\u274c")

# The category vocabulary already in dossier/compute. A finding that names a new
# shape is mapped onto the nearest one; the finding's own wording is parked in
# extras.wave2.category_as_written so nothing is lost.
CATEGORY_RULES = [
    ("national hpc", "national HPC allocation"),
    ("hpc", "national HPC allocation"),
    ("quantum", "quantum compute"),
    ("sandbox", "container and VM sandbox"),
    ("container and vm", "container and VM sandbox"),
    ("container host", "container and VM sandbox"),
    ("agent vm", "container and VM sandbox"),
    ("kubernetes", "container and VM sandbox"),
    ("macos", "macOS host"),
    ("windows", "Windows host"),
    ("browser", "browser host"),
    ("shared shell", "shared shell"),
    ("pubnix", "shared shell"),
    ("shell account", "shared shell"),
    ("serverless", "serverless runtime"),
    ("paas", "platform host"),
    ("platform host", "platform host"),
    ("cloud-ide", "platform host"),
    ("cloud ide", "platform host"),
    ("notebook", "notebook runtime"),
    ("dev environment", "dev environment"),
    ("student", "dev environment"),
    ("education", "dev environment"),
    ("ci runner", "CI runner"),
    ("ci-runner", "CI runner"),
    ("ci as", "CI runner"),
    ("inference", "inference API"),
    ("database", "managed database"),
    ("startup credit", "cloud VM"),
    ("research", "GPU cloud"),
    ("academic", "GPU cloud"),
    ("grant", "GPU cloud"),
    ("student-p", "GPU cloud"),
    ("gpu", "GPU cloud"),
    ("spot", "GPU cloud"),
    ("decentralized", "GPU cloud"),
    ("vps", "cloud VM"),
    ("cloud vm", "cloud VM"),
    ("regional", "cloud VM"),
    ("hosting", "cloud VM"),
    ("compute", "cloud VM"),
]

IDENTITY_KINDS = {
    "anonymous": "anonymous",
    "email": "email",
    "any-phone": "any-phone",
    "card": "card",
    "national-id": "national-id",
    "institution": "institution",
    "country-phone": "country-phone",
}

VALID_VERDICTS = {
    "qualifies",
    "qualifies-with-caveat",
    "fails-egress",
    "fails-quota",
    "fails-identity",
    "trial-only",
    "paid-only",
    "dead",
}

BINDINGS = {
    "request-rate",
    "pull-count",
    "per-ip-shaping",
    "per-object-cap",
    "write-gated",
    "retention-clamped",
    "volume-quota",
}


def ascii_only(text: str) -> str:
    """Fold a dossier sentence to ASCII.

    Dossier records are data, and 1,226 of them already carry non-Latin text: a
    vendor quote in Japanese, Korean, Persian, Russian or Chinese is evidence, and
    stripping it left empty quotation marks in seven records when this function was
    applied to `free_tier.stated`. It is now used only for fields that never carry a
    quotation, and `keep_original` is the path for the rest.
    """
    if not isinstance(text, str):
        return text
    text = text.replace("\u2014", " - ").replace("\u2013", " - ")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2026", "...").replace("\u00a0", " ")
    out = []
    for ch in text:
        if ch in MARKERS or ord(ch) < 128:
            out.append(ch)
        else:
            out.append(" ")
    text = "".join(out)
    return re.sub(r" {2,}", " ", text).strip()


def keep_original(text: str) -> str:
    """Fold dashes and quotes but preserve every other character.

    Use this for any field that may carry a vendor's own wording.
    """
    if not isinstance(text, str):
        return text
    return (
        text.replace("—", " - ")
        .replace("–", " - ")
        .replace("‘", "'")
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace(" ", " ")
        .strip()
    )


def normalise_date(raw: str, fallback: str):
    """Coerce a partial date to the schema's YYYY-MM-DD without inventing a day.

    A capture dated "2026-10" becomes 2026-10-01 and the loss of precision is
    written into the evidence sentence, so a reader can see the day is a
    placeholder rather than a reading.
    """
    s = str(raw or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s, None
    m = re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-01", "month precision"
    m = re.fullmatch(r"(\d{4})", s)
    if m:
        return f"{m.group(1)}-01-01", "year precision"
    return fallback, "no date stated"


def is_http(url: str) -> bool:
    return bool(re.match(r"^https?://", str(url or "")))


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:80] or "unknown"


STOPWORDS = {
    "the", "a", "an", "and", "or", "on", "in", "at", "of", "with", "for", "which",
    "is", "was", "are", "its", "no", "not", "free", "via", "from", "by", "to",
    "that", "this", "but", "when", "how", "what", "one", "two", "three",
}


def provider_key(name: str) -> str:
    """The vendor name inside a finding's title-shaped `provider` string.

    Wave agents wrote labels such as
    "Buildkite: free 2,000 Linux vCPU minutes a month and the agent is yours",
    so the raw string is a sentence. The vendor is what precedes the colon, or
    the leading words up to the first stopword.
    """
    s = (name or "").strip()
    s = re.split(r"\s*[:\u2014]\s*", s)[0]
    s = re.split(r"\s+-\s+", s)[0]
    s = re.sub(r"\s*\([^)]*\)\s*", " ", s)
    words = s.split()
    keep = []
    for w in words:
        if w.lower().strip(",.;") in STOPWORDS and keep:
            break
        keep.append(w)
        if len(keep) == 3:
            break
    out = " ".join(keep).strip(" ,.;-")
    return out or s[:60]


def norm_provider(name: str) -> str:
    s = provider_key(name).lower()
    s = re.sub(r"\b(inc|llc|ltd|gmbh|the)\b", " ", s)
    return re.sub(r"[^a-z0-9]", "", s)


def pick(value, default):
    return value if value not in (None, "", [], {}) else default


def canon_category(raw: str) -> str:
    low = (raw or "").lower()
    for needle, canon in CATEGORY_RULES:
        if needle in low:
            return canon
    return "cloud VM"


def canon_identity(raw: str, detail: str):
    low = (raw or "").strip().lower()
    country = None
    if low.startswith("country-phone"):
        m = re.search(r"\((.*?)\)", raw or "")
        if m:
            country = m.group(1).strip()
        return {"kind": "country-phone", "detail": ascii_only(detail), "country": country}
    if low in IDENTITY_KINDS:
        return {"kind": IDENTITY_KINDS[low], "detail": ascii_only(detail), "country": None}
    if "institution" in low or "university" in low or "tenant" in low:
        return {"kind": "institution", "detail": ascii_only(detail), "country": None}
    if "card" in low or "payment" in low:
        return {"kind": "card", "detail": ascii_only(detail), "country": None}
    if "phone" in low:
        m = re.search(r"\((.*?)\)", raw or "")
        return {
            "kind": "country-phone",
            "detail": ascii_only(detail),
            "country": m.group(1).strip() if m else None,
        }
    if "anonymous" in low or low == "none":
        return {"kind": "anonymous", "detail": ascii_only(detail), "country": None}
    if "email" in low:
        return {"kind": "email", "detail": ascii_only(detail), "country": None}
    # An unclassifiable gate is recorded as the strictest reachable kind rather
    # than guessed downward: unknown never becomes "anonymous".
    return {"kind": "institution", "detail": ascii_only(detail), "country": None}


def canon_unit(offer: str, evidence: list) -> str:
    hay = " ".join([offer or ""] + [e.get("proved", "") for e in evidence or []])
    hay = hay.lower()
    for pattern, unit in (
        (r"\b(gpu|gpu-|core|node|v?cpu)[- ]?hours?\b", "hours"),
        (r"\d[\d,.]*\s*(hours?|hrs?)\b", "hours"),
        (r"\d[\d,.]*\s*(minutes?|mins?)\b", "minutes"),
        (r"\d[\d,.]*\s*seconds?\b", "seconds"),
        (r"\d[\d,.]*\s*(tokens?|million tokens)\b", "tokens"),
        (r"\d[\d,.]*\s*(requests?|calls?|invocations?)\b", "requests"),
        (r"\d[\d,.]*\s*(gib|gb)\b", "GiB"),
        (r"\d[\d,.]*\s*(tib|tb)\b", "TiB"),
        (r"\bunlimited\b", "unlimited"),
        (r"\d[\d,.]*\s*(users?|seats?)\b", "users"),
    ):
        if re.search(pattern, hay):
            return unit
    return "none"


def infer_interface(finding: dict) -> list:
    hay = " ".join(
        [str(finding.get(k) or "") for k in
         ("tooling", "interface_detail", "notes", "offer", "chaining", "binding_note")]
        + [str(e.get("proved") or "") for e in (finding.get("evidence") or []) if isinstance(e, dict)]
    ).lower()
    out = []
    if re.search(r"\bssh\b|\bssh key\b", hay):
        out.append("ssh")
    if re.search(r"\brest\b|api", hay):
        out.append("rest")
    if re.search(r"\bcli\b|command line|\bterraform\b", hay):
        out.append("cli")
    if re.search(r"\bgit\b", hay):
        out.append("git")
    if re.search(r"jupyter|notebook", hay):
        out.append("rest")
    if re.search(r"\bs3", hay):
        out.append("s3-compatible")
    seen, uniq = set(), []
    for i in out:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    return uniq or ["unknown"]


def egress_block(finding: dict, url: str) -> dict:
    """Egress terms, from the field if the agent set one, else from the evidence.

    Agents often put the traffic-out sentence in `notes` or in an evidence
    sentence rather than in a field. Losing it makes the record assert nothing
    about the one term that decides whether a workload can leave.
    """
    explicit = finding.get("egress")
    if explicit:
        # An agent may write `egress` as a nested block rather than a sentence.
        # That shape used to pass straight through `ascii_only`, which returns a
        # non-string unchanged, and the schema then rejected the record after the
        # wave had finished. Flatten it here so a nested block is a supported
        # input rather than a gate failure three steps later.
        if isinstance(explicit, dict):
            terms = explicit.get("terms") or explicit.get("stated") or ""
            metered = explicit.get("metered")
            allowance = explicit.get("free_allowance")
            per_tb = explicit.get("price_per_tb")
            src = explicit.get("source_url") or url
        else:
            terms = explicit
            metered = finding.get("egress_metered")
            allowance = finding.get("egress_allowance")
            per_tb = finding.get("egress_price_per_tb")
            src = url
        if allowance is not None and not isinstance(allowance, str):
            allowance = str(allowance)
        if allowance is not None and not isinstance(allowance, str):
            allowance = str(allowance)
        # The schema types this field as a described price ("USD 3 per TB"), not a
        # number, because a bare number loses the currency. A lane that writes a
        # number would fail the gate after the wave finished, so the number is
        # kept in `terms` where its currency already is, and the field goes null.
        if per_tb is not None and not isinstance(per_tb, str):
            terms = f"{terms} [price per TB recorded as a bare number: {per_tb}]"
            per_tb = None
        return {
            "terms": ascii_only(terms) if str(terms).strip() else "not stated in the finding",
            "metered": bool(metered),
            "free_allowance": allowance,
            "price_per_tb": per_tb,
            "source_url": src,
        }
    needles = re.compile(r"egress|bandwidth|traffic out|outbound|data transfer", re.I)
    hits = []
    for e in finding.get("evidence") or []:
        if not isinstance(e, dict):
            continue
        proved = e.get("proved") or ""
        if needles.search(proved):
            hits.append((e.get("url") or url, proved))
    for key in ("notes", "binding_note"):
        text = str(finding.get(key) or "")
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if needles.search(sentence):
                hits.append((url, sentence.strip()))
    if hits:
        src, sentence = hits[0]
        metered = not re.search(r"\b(zero|free|included|no egress|not metered|unmetered)\b", sentence, re.I)
        return {
            "terms": ascii_only(sentence),
            "metered": bool(metered),
            "free_allowance": None,
            "price_per_tb": None,
            "source_url": src,
        }
    return {
        "terms": "not published on the page read: no egress term was found, so nothing is asserted",
        "metered": False,
        "free_allowance": None,
        "price_per_tb": None,
        "source_url": url,
    }


def build_record(finding: dict, slug: str, today: str) -> dict:
    offer = keep_original(pick(finding.get("offer"), "not stated on the page read"))
    url = finding.get("url") or ""
    evidence = finding.get("evidence") or []
    clean_evidence = []
    for e in evidence:
        if not isinstance(e, dict):
            continue
        proved = keep_original(e.get("proved") or "recorded, no sentence captured")
        date, precision = normalise_date(e.get("date"), today)
        if precision:
            proved = f"{proved} [date precision: {precision}]"
        url_e = e.get("url")
        if not is_http(url_e):
            # A non-HTTP receipt such as an ssh endpoint is evidence, but it is
            # not a URL the schema accepts. It moves into the sentence.
            if url_e:
                proved = f"{proved} [receipt: {url_e}]"
            url_e = url
        if not is_http(url_e):
            continue
        clean_evidence.append({"url": url_e, "date": date, "proved": proved})
    if not clean_evidence and url:
        clean_evidence = [
            {"url": url, "date": today, "proved": "the finding cites this page without a quoted sentence"}
        ]

    binding = (finding.get("binding") or "none").strip().lower()
    if binding not in BINDINGS and binding != "none":
        binding = "write-gated"
    binding_note = ascii_only(
        pick(finding.get("binding_note"), "no binding constraint identified in this pass")
    )

    identity_raw = finding.get("identity_cost") or "email"
    identity_detail = ascii_only(
        pick(
            finding.get("identity_detail") or finding.get("identity_note"),
            "as stated by the provider's signup page",
        )
    )

    limits = []
    if binding != "none":
        limits.append({"kind": binding, "value": binding_note, "source": url or "unstated"})
    for extra in finding.get("limits") or []:
        if isinstance(extra, dict) and extra.get("kind") in BINDINGS and extra.get("value"):
            limits.append(
                {
                    "kind": extra["kind"],
                    "value": ascii_only(str(extra["value"])),
                    "source": extra.get("source") or url or "unstated",
                }
            )

    retention_stated = (
        binding_note
        if binding == "retention-clamped"
        else "not applicable: the unit is a machine or an account, not stored bytes"
    )

    record = {
        "topic": "compute",
        "slug": slug,
        "provider": ascii_only(provider_key(pick(finding.get("provider"), slug))),
        "url": url,
        "category": canon_category(finding.get("category")),
        "free_tier": {
            "stated": offer,
            "unit": canon_unit(offer, clean_evidence),
            "metered_on": "wall-clock",
            "source_url": url,
            "read_on": (clean_evidence[0]["date"] if clean_evidence else today),
            "notes": ascii_only(pick(finding.get("free_tier_kind"), "kind not stated")),
        },
        "per_object_cap": {
            "stated": "not applicable: the unit is a machine, not an object",
            "bytes": None,
            "source_url": url,
            "notes": "the ceiling that matters is the machine shape, parked in extras.wave2.shape",
        },
        "retention": {
            "stated": retention_stated,
            "days": None,
            "source_url": url,
            "notes": "a machine record: what is lost is the running process, not a stored object",
        },
        "egress": egress_block(finding, url),
        "interface": infer_interface(finding),
        "interface_detail": ascii_only(
            pick(
                finding.get("interface_detail"),
                "inferred from the tooling the provider documents; not probed",
            )
        ),
        "tooling": ascii_only(
            pick(finding.get("tooling"), "not stated in the finding; the provider documents no client")
        ),
        "chaining": ascii_only(pick(finding.get("chaining"), "not established in this pass")),
        "limits": limits,
        "limits_note": binding_note,
        "binding": binding,
        "binding_note": binding_note,
        "identity_cost": canon_identity(identity_raw, identity_detail),
        "reliability_note": ascii_only(
            pick(finding.get("reliability_note"), "no reliability event observed in this session")
        ),
        "confidence": pick(finding.get("confidence"), "documented"),
        "evidence": clean_evidence,
        "verdict": pick(finding.get("verdict"), "unverified"),
        "verified_at": f"{today}T00:00:00.000Z",
        "notes": ascii_only(pick(finding.get("notes"), "no open question recorded")),
        "extras": {
            "wave2": {
                "provider_as_written": ascii_only(finding.get("provider") or ""),
                "class": finding.get("class"),
                "category_as_written": finding.get("category"),
                "free_tier_kind": finding.get("free_tier_kind"),
                "shape": finding.get("shape"),
                "seen_routes": finding.get("seen_routes"),
                "agents": sorted(set(finding.get("_agents") or [])),
                "promoted_from": ".tmp/wave2",
            }
        },
    }
    if finding.get("tier"):
        record["tier"] = ascii_only(str(finding["tier"]))
    return record


def score(finding: dict) -> int:
    """Which duplicate to keep: the one carrying the most usable detail."""
    n = 0
    n += len(finding.get("evidence") or []) * 3
    n += len(str(finding.get("offer") or "")) // 80
    n += 2 if finding.get("chaining") else 0
    n += 2 if finding.get("shape") else 0
    n += 2 if finding.get("binding_note") else 0
    n += len(finding.get("seen_routes") or [])
    return n


def lint(args) -> int:
    """Invariants a record can break against its own fields.

    The first is the one that cost four records a wrong verdict: a record whose
    free tier is `none` cannot be `qualifies` or `qualifies-with-caveat`, because
    docs/conventions/README.md defines paid-only as "it was never free".
    """
    bad = 0
    checked = 0
    for path in sorted(glob.glob(os.path.join(args.out, "*.json"))):
        rec = json.load(open(path, encoding="utf-8"))
        checked += 1
        stated = str(rec.get("free_tier", {}).get("stated", "")).lower()
        verdict = rec.get("verdict")
        # The defect is a record whose own free_tier sentence says there is no
        # free tier and whose verdict says it qualifies. A paid spot lane uses
        # `qualifies` to mean "the cheapest paid shape", which is a different
        # claim and is not caught here.
        if stated.startswith("no free tier") and verdict in ("qualifies", "qualifies-with-caveat"):
            print(f"  VIOLATION {rec['slug']}: free_tier_kind none with verdict {verdict}")
            bad += 1
        if verdict == "dead" and rec.get("free_tier", {}).get("stated", "").lower().startswith("merged into"):
            continue
        if verdict in ("qualifies", "qualifies-with-caveat") and not (rec.get("evidence") or []):
            print(f"  VIOLATION {rec['slug']}: a qualifying verdict with no evidence row")
            bad += 1
    print(f"lint: {checked} records, {bad} violation(s)")
    return 1 if bad else 0


def apply_merges(args) -> int:
    """Append incoming evidence to records that already exist.

    A merge whose incoming verdict disagrees with the stored one is skipped and
    reported: a verdict is the conclusion of the record, and a second pass
    flipping it without review is how a corpus acquires two answers to one
    question.
    """
    queue_path = os.path.join(args.findings, "merge-queue.json")
    if not os.path.exists(queue_path):
        print(f"no merge queue at {queue_path}", file=sys.stderr)
        return 2
    queue = json.load(open(queue_path, encoding="utf-8"))
    applied = skipped = 0
    for item in queue:
        path = item["existing_path"]
        rec = json.load(open(path, encoding="utf-8"))
        if (item.get("incoming_verdict") or "") != rec.get("verdict"):
            print(
                f"  SKIP {item['existing_slug']:28} stored={rec.get('verdict')} "
                f"incoming={item.get('incoming_verdict')}"
            )
            skipped += 1
            continue
        seen = {(e.get("url"), e.get("proved")) for e in rec.get("evidence") or []}
        added = 0
        for e in item.get("incoming_evidence") or []:
            if not isinstance(e, dict) or not e.get("url"):
                continue
            date, precision = normalise_date(e.get("date"), args.today)
            proved = ascii_only(e.get("proved") or "")
            if precision:
                proved = f"{proved} [date precision: {precision}]"
            key = (e["url"], proved)
            if key in seen:
                continue
            rec.setdefault("evidence", []).append({"url": e["url"], "date": date, "proved": proved})
            seen.add(key)
            added += 1
        if added:
            extras = rec.setdefault("extras", {})
            w2 = extras.setdefault("wave2", {})
            w2["merged_agents"] = sorted(set((w2.get("merged_agents") or []) + (item.get("agents") or [])))
            w2["merged_evidence_rows"] = (w2.get("merged_evidence_rows") or 0) + added
            w2["merged_note"] = ascii_only(item.get("incoming_offer") or "")[:600]
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(rec, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            print(f"  MERGED {item['existing_slug']:28} +{added} evidence row(s)")
            applied += 1
    print(f"\nmerged {applied}, skipped {skipped}")
    return 0


def apply_verdict(args) -> int:
    """slug=verdict. Kept dumb on purpose: the reason goes in a history entry."""
    slug, _, verdict = args.apply_verdict.partition("=")
    if verdict not in VALID_VERDICTS:
        print(f"{verdict} is not a schema verdict", file=sys.stderr)
        return 2
    path = os.path.join(args.out, slug + ".json")
    rec = json.load(open(path, encoding="utf-8"))
    old = rec.get("verdict")
    rec["verdict"] = verdict
    rec["verified_at"] = f"{args.today}T00:00:00.000Z"
    log = rec.setdefault("extras", {}).setdefault("wave2", {})
    log["verdict_change"] = f"{old} -> {verdict} on {args.today}"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"{slug}: {old} -> {verdict}")
    return 0


def refuse_in_research_checkout(target):
    """The research checkout changes tracked files only through a run (AGENTS.md section 2 rule 14): there, a write to
    a path outside .tmp/ exits 2. This script is for a session in an own clone; a run does the same work with
    scripts/rq. A dry run, a check and a write under .tmp/ go on."""
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
    sys.stderr.write("%s: the research checkout changes records only through a run: scripts/rq open amend TOPIC "
                     "\"RID: what is wrong\" (AGENTS.md section 2 rule 14). This script writes %s, which is for a "
                     "session in an own clone.\n" % (os.path.basename(__file__), target))
    sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--findings", default=".tmp/wave2")
    ap.add_argument("--out", default="dossier/compute")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--today", default=None)
    ap.add_argument(
        "--merge",
        action="store_true",
        help="apply merge-queue entries whose verdict agrees with the existing record",
    )
    ap.add_argument(
        "--skip-other-topics",
        action="store_true",
        help="refuse to create a record for a provider already recorded under another topic",
    )
    ap.add_argument(
        "--lint",
        action="store_true",
        help="assert that a record with no free tier does not carry a qualifies verdict",
    )
    ap.add_argument(
        "--apply-verdict",
        default=None,
        help="slug=verdict; change one record's verdict after a verified conflict",
    )
    args = ap.parse_args()

    today = args.today or os.environ.get("TODAY")
    if not today:
        print("set --today YYYY-MM-DD or TODAY; a record must not invent a date", file=sys.stderr)
        return 2

    if args.lint:
        return lint(args)
    if args.merge:
        return apply_merges(args)
    if args.apply_verdict:
        return apply_verdict(args)

    files = sorted(glob.glob(os.path.join(args.findings, "*", "findings.json")))
    if not files:
        print(f"no findings.json under {args.findings}", file=sys.stderr)
        return 3

    raw, unparseable = [], []
    for path in files:
        agent = os.path.basename(os.path.dirname(path))
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            unparseable.append((path, str(exc)))
            continue
        if isinstance(data, dict):
            data = [data]
        for r in data:
            if not isinstance(r, dict) or not r.get("provider"):
                continue
            r.setdefault("_agents", [])
            r["_agents"] = list(set(r["_agents"] + [agent]))
            raw.append(r)

    if unparseable:
        for path, err in unparseable:
            print(f"UNPARSEABLE {path}: {err}", file=sys.stderr)
        return 3

    # Group duplicates by normalised provider, keep the richest, union the evidence.
    groups: dict[str, list] = {}
    for r in raw:
        groups.setdefault(norm_provider(r["provider"]), []).append(r)

    merged = []
    for key, items in groups.items():
        items.sort(key=score, reverse=True)
        head = json.loads(json.dumps(items[0]))
        seen = {(e.get("url"), e.get("proved")) for e in head.get("evidence") or []}
        for other in items[1:]:
            for e in other.get("evidence") or []:
                if (e.get("url"), e.get("proved")) not in seen:
                    head.setdefault("evidence", []).append(e)
                    seen.add((e.get("url"), e.get("proved")))
            head["_agents"] = list(set(head.get("_agents", []) + other.get("_agents", [])))
            if other.get("verdict") and other.get("verdict") != head.get("verdict"):
                head.setdefault("_verdict_conflict", []).append(
                    f"{other.get('verdict')} via {','.join(other.get('_agents', []))}"
                )
        merged.append(head)

    # Collapse groups whose key words are a strict prefix of another's, but only
    # when the shorter key carries at least two words: "miracleplus compute" and
    # "miracleplus compute support" are one vendor, while "google" and
    # "google tpu research" are not.
    def words_of(name):
        return [w for w in re.split(r"[^a-z0-9]+", provider_key(name).lower()) if w]

    buckets = {}
    for f in merged:
        buckets[norm_provider(f["provider"])] = f
    keys = sorted(buckets, key=lambda k: len(words_of(buckets[k]["provider"])))
    absorbed = set()
    for i, short in enumerate(keys):
        sw = words_of(buckets[short]["provider"])
        if len(sw) < 2 or short in absorbed:
            continue
        for long_key in keys[i + 1:]:
            if long_key in absorbed:
                continue
            lw = words_of(buckets[long_key]["provider"])
            if lw[: len(sw)] == sw and len(lw) > len(sw):
                head, tail = buckets[long_key], buckets[short]
                if score(tail) > score(head):
                    head, tail = tail, head
                seen_ev = {(e.get("url"), e.get("proved")) for e in head.get("evidence") or []}
                for e in tail.get("evidence") or []:
                    if (e.get("url"), e.get("proved")) not in seen_ev:
                        head.setdefault("evidence", []).append(e)
                head["_agents"] = list(set(head.get("_agents", []) + tail.get("_agents", [])))
                buckets[long_key] = head
                absorbed.add(short)
                break
    merged = [v for k, v in buckets.items() if k not in absorbed]

    other_topic = {}
    if args.skip_other_topics:
        here = os.path.normpath(args.out)
        for path in glob.glob(os.path.join(os.path.dirname(here), "*", "*.json")):
            topic_dir = os.path.normpath(os.path.dirname(path))
            if topic_dir == here:
                continue
            try:
                d = json.load(open(path, encoding="utf-8"))
            except Exception:
                continue
            other_topic.setdefault(norm_provider(d.get("provider", "")), []).append(
                (os.path.basename(topic_dir), d.get("slug"))
            )

    # Existing records, by normalised provider name.
    existing = {}
    for path in glob.glob(os.path.join(args.out, "*.json")):
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        existing[norm_provider(d.get("provider", ""))] = (d.get("slug"), path)

    used_slugs = set()
    for _, path in existing.values():
        used_slugs.add(os.path.basename(path)[:-5])
    for path in glob.glob(os.path.join(args.out, "*.json")):
        used_slugs.add(os.path.basename(path)[:-5])

    NON_PROVIDER_CLASSES = {"chain", "chaining", "composition", "composed-credits"}

    new_records, merge_queue, refused, non_provider, unresolved = [], [], [], [], []
    cross_topic = []
    for f in merged:
        if (f.get("class") or "").strip().lower() in NON_PROVIDER_CLASSES:
            non_provider.append(
                {
                    "provider": f.get("provider"),
                    "class": f.get("class"),
                    "offer": f.get("offer"),
                    "chaining": f.get("chaining"),
                    "evidence": f.get("evidence"),
                    "agents": f.get("_agents"),
                    "note": "a composition, not a provider: it belongs in a document, not in dossier/",
                }
            )
            continue
        key = norm_provider(f["provider"])
        base = slugify(provider_key(f["provider"]))
        if len(base) < 2:
            base = slugify(provider_key(f["provider"])) + "-host"
        if args.skip_other_topics and key in other_topic:
            cross_topic.append(
                {
                    "provider": f.get("provider"),
                    "url": f.get("url"),
                    "recorded_at": other_topic[key],
                    "offer": f.get("offer"),
                    "verdict": f.get("verdict"),
                    "evidence": f.get("evidence"),
                    "note": "the provider already has a record under another topic; this finding "
                    "must be merged into that record, not given a second home",
                }
            )
            continue
        if key in existing:
            merge_queue.append(
                {
                    "provider": f["provider"],
                    "existing_slug": existing[key][0],
                    "existing_path": existing[key][1],
                    "incoming_verdict": f.get("verdict"),
                    "incoming_evidence": f.get("evidence"),
                    "incoming_offer": f.get("offer"),
                    "agents": f.get("_agents"),
                    "verdict_conflict": f.get("_verdict_conflict"),
                }
            )
            continue
        slug = base
        n = 2
        while slug in used_slugs:
            slug = f"{base}-{n}"
            n += 1
        used_slugs.add(slug)
        if not is_http(f.get("url")):
            refused.append((f.get("provider"), "no absolute http URL, so the record could not be cited"))
            continue
        if (f.get("verdict") or "").strip().lower() not in VALID_VERDICTS:
            unresolved.append(
                {
                    "provider": f.get("provider"),
                    "verdict_as_written": f.get("verdict"),
                    "offer": f.get("offer"),
                    "evidence": f.get("evidence"),
                    "agents": f.get("_agents"),
                    "note": "the agent recorded no verdict from the schema's enum; a verifier must settle it",
                }
            )
            continue
        try:
            rec = build_record(f, slug, today)
        except Exception as exc:
            refused.append((f.get("provider"), str(exc)))
            continue
        if f.get("_verdict_conflict"):
            rec["notes"] = (
                rec["notes"]
                + " Conflicting verdicts across agents: "
                + "; ".join(f["_verdict_conflict"])
                + ". The one recorded is the better-evidenced."
            )
        new_records.append(rec)

    new_records.sort(key=lambda r: (r["category"], r["slug"]))
    print(f"findings read        {len(raw)}")
    print(f"unique providers     {len(merged)}")
    print(f"new records          {len(new_records)}")
    print(f"merge queue          {len(merge_queue)}")
    print(f"refused              {len(refused)}")
    print(f"compositions held    {len(non_provider)}")
    print(f"unresolved verdicts  {len(unresolved)}")
    print(f"cross-topic held     {len(cross_topic)}")

    if args.dry_run:
        for r in new_records:
            print(f"  NEW  {r['slug']:44} {r['category']:26} {r['verdict']}")
        for m in merge_queue:
            print(f"  MERGE {m['existing_slug']:42} <- {m['provider']}")
        for n in non_provider:
            print(f"  COMPOSE {n['provider'][:70]}")
        for prov, err in refused:
            print(f"  REFUSED {prov}: {err}")
        return 1 if refused else 0

    refuse_in_research_checkout(args.out)
    refuse_in_research_checkout(os.path.join(args.findings, "x"))
    os.makedirs(args.out, exist_ok=True)
    for rec in new_records:
        path = os.path.join(args.out, rec["slug"] + ".json")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(rec, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    if non_provider:
        np_path = os.path.join(args.findings, "non-provider.json")
        with open(np_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(non_provider, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"compositions written to {np_path}")
    if cross_topic:
        cp = os.path.join(args.findings, "cross-topic.json")
        with open(cp, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(cross_topic, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"cross-topic written to {cp}")
    if unresolved:
        up = os.path.join(args.findings, "unresolved.json")
        with open(up, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(unresolved, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"unresolved written to {up}")
    if merge_queue:
        mq = os.path.join(args.findings, "merge-queue.json")
        with open(mq, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(merge_queue, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"merge queue written to {mq}")
    print(f"wrote {len(new_records)} records into {args.out}")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
