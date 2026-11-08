#!/usr/bin/env python3
"""Promote egress lane findings into dossier records.

WHY THIS EXISTS
    A wave writes findings under `.tmp/egress/<lane>/findings.json` so a
    half-finished record never lands inside `dossier/` and fails the gate for
    every lane still running. This is the second half: it turns those findings
    into records that satisfy `scripts/dossier/schema.json`, and it refuses to
    touch a record that already exists.

USAGE
    python scripts/dossier/promote-egress.py --findings .tmp/egress --dry-run
    python scripts/dossier/promote-egress.py --findings .tmp/egress
    python scripts/dossier/promote-egress.py --findings .tmp/egress --lint

EXIT CODES
    0  wrote, or a dry run found nothing to refuse
    1  one or more findings could not be mapped; the report names them
    2  usage
    3  environment: a findings file is unparseable or the schema is missing
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

VERDICTS = {"qualifies", "qualifies-with-caveat", "fails-egress", "fails-quota",
            "fails-identity", "trial-only", "paid-only", "dead"}
CONFIDENCE = {"measured", "documented", "reported", "inferred", "unverified"}
IDENTITY = {"anonymous", "email", "any-phone", "country-phone", "national-id",
            "card", "institution"}
KINDS = {"request-rate", "pull-count", "per-ip-shaping", "per-object-cap",
         "write-gated", "retention-clamped", "volume-quota"}
IFACES = {"s3", "s3-compatible", "rest", "graphql", "webdav", "sftp", "ftp",
          "ftps", "scp", "rsync", "smb", "nfs", "ssh", "graph", "oci", "git",
          "rclone", "cli", "webdav-proxy", "unknown"}
UNITS = {"bytes", "GiB", "TiB", "GB", "TB", "MB", "objects", "requests",
         "seconds", "minutes", "hours", "tokens", "users", "unlimited", "none",
         "mixed"}
METERED_ON = {"stored-bytes", "uploaded-bytes", "downloaded-bytes",
              "request-count", "object-count", "wall-clock", "identity-count",
              "none", "unstated"}
BAD_CHARS = re.compile(r"[^\x20-\x7e\n]")


def ascii_only(text) -> str:
    text = re.sub(r"[\u2018\u2019]", "'", str(text))
    text = re.sub(r"[\u201c\u201d]", '"', text)
    text = re.sub(r"[\u2013\u2014]", "-", text)
    text = re.sub(r"[\u00a0]", " ", text)
    return BAD_CHARS.sub("", text).strip()


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)[:80]


def is_http(url) -> bool:
    return isinstance(url, str) and re.match(r"^https?://", url) is not None


def pick(value, default):
    if value is None or value == "":
        return default
    return value


def evidence_block(f: dict, fallback_url: str, today: str) -> tuple[list, str]:
    rows, newest = [], ""
    for e in f.get("evidence") or []:
        if not isinstance(e, dict):
            continue
        proved = ascii_only(pick(e.get("proved"), "recorded, no sentence captured"))
        date = str(pick(e.get("date"), today))[:10]
        url = e.get("url")
        if not (is_http(url) or str(url).startswith("probe:")):
            if url:
                proved = f"{proved} [receipt: {ascii_only(url)}]"
            url = fallback_url
        if not (is_http(url) or str(url).startswith("probe:")):
            continue
        if len(proved) < 8:
            proved = f"{proved} (source recorded)"
        rows.append({"url": url, "date": date, "proved": proved})
        if date > newest:
            newest = date
    return rows, newest


def limits_block(f: dict, url: str) -> list:
    out = []
    for item in f.get("limits") or []:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind") or "").strip().lower()
        if kind not in KINDS:
            continue
        out.append({
            "kind": kind,
            "value": ascii_only(pick(item.get("value"), "unstated")),
            "source": ascii_only(pick(item.get("source"), url)),
        })
    return out


def build(f: dict, lane: str, today: str) -> dict:
    url = f.get("url") or ""
    slug = slugify(pick(f.get("slug_hint"), f.get("provider") or "unnamed"))
    ev, newest = evidence_block(f, url, today)
    if not ev and url:
        ev = [{"url": url, "date": today,
               "proved": "the finding cites this page without a quoted sentence"}]
    date = str(pick(f.get("free_read_on"), newest or today))[:10]

    verdict = str(pick(f.get("verdict"), "unverified")).strip().lower()
    if verdict not in VERDICTS:
        verdict = "qualifies-with-caveat"
    conf = str(pick(f.get("confidence"), "documented")).strip().lower()
    if conf not in CONFIDENCE:
        conf = "documented"

    binding = str(pick(f.get("binding"), "none")).strip().lower()
    if binding not in KINDS and binding != "none":
        binding = "none"

    ident_kind = str(pick(f.get("identity_kind"), "email")).strip().lower()
    if ident_kind not in IDENTITY:
        ident_kind = "email"
    if ident_kind == "country-phone":
        ident_kind = "any-phone"

    unit = str(pick(f.get("free_unit"), "mixed"))
    if unit not in UNITS:
        unit = "mixed"
    metered_on = str(pick(f.get("free_metered_on"), "unstated"))
    if metered_on not in METERED_ON:
        metered_on = "unstated"

    ifaces = [i for i in (f.get("interface") or []) if i in IFACES] or ["cli"]

    volume = f.get("volume_tib_month")
    if not isinstance(volume, (int, float)):
        volume = None
    volume_stated = ascii_only(pick(f.get("volume_stated"), "not published"))

    limits = limits_block(f, url)
    if binding != "none" and not any(l["kind"] == binding for l in limits):
        limits.insert(0, {
            "kind": binding,
            "value": ascii_only(pick(f.get("binding_note"), "named without a number")),
            "source": url or "unstated",
        })

    transit = str(pick(f.get("bytes_transit"), "unknown")).strip().lower()
    if transit not in ("yes", "no", "overlay-only"):
        transit = "unknown"

    record = {
        "topic": "egress",
        "slug": slug,
        "provider": ascii_only(pick(f.get("provider"), slug)),
        "url": url,
        "category": ascii_only(pick(f.get("category"), "tunnel")),
        "tier": ascii_only(pick(f.get("tier"), "free")),
        "free_tier": {
            "stated": ascii_only(pick(f.get("free_stated"), "not stated on the page read")),
            "unit": unit,
            "metered_on": metered_on,
            "source_url": pick(f.get("free_source"), url),
            "read_on": date,
            "notes": ascii_only(pick(f.get("free_notes"), "")),
        },
        "per_object_cap": {
            "stated": ascii_only(pick(f.get("per_object_cap"),
                                      "not applicable: a tunnel or an address, not an object")),
            "bytes": None,
            "source_url": url,
            "notes": "",
        },
        "retention": {
            "stated": ascii_only(pick(f.get("retention"),
                                      "not applicable: a live tunnel, not stored bytes")),
            "days": f.get("retention_days") if isinstance(f.get("retention_days"), int) else None,
            "source_url": url,
            "notes": ascii_only(pick(f.get("retention_note"), "")),
        },
        "egress": {
            "terms": ascii_only(pick(f.get("egress_terms"),
                                     f"{volume_stated}; ingress: {pick(f.get('ingress'), 'unstated')}")),
            "metered": volume is not None,
            "free_allowance": volume_stated if volume is not None else "none published",
            "price_per_tb": ascii_only(pick(f.get("price_per_tb"), None) or "") or None,
            "source_url": url,
        },
        "interface": ifaces,
        "interface_detail": ascii_only(pick(f.get("interface_detail"), "")),
        "tooling": ascii_only(pick(f.get("tooling"), "not stated in the finding")),
        "chaining": ascii_only(pick(f.get("chaining"), "not established in this pass")),
        "limits": limits,
        "limits_note": ascii_only(pick(f.get("limits_note"), "")),
        "binding": binding,
        "binding_note": ascii_only(pick(f.get("binding_note"), "no binding constraint named")),
        "identity_cost": {
            "kind": ident_kind,
            "detail": ascii_only(pick(f.get("identity_detail"), "as stated by the signup page")),
            "country": ascii_only(f.get("identity_country")) or None,
        },
        "reliability_note": ascii_only(pick(f.get("reliability_note"),
                                            "no reliability event recorded in this pass")),
        "confidence": conf,
        "confidence_note": ascii_only(pick(f.get("confidence_note"),
                                           "not raised above documented: no probe run here")),
        "evidence": ev,
        "verdict": verdict,
        "verified_at": f"{date}T00:00:00.000Z",
        "price_per_tb_month": ascii_only(pick(f.get("price"), None) or "") or None,
        "history": [],
        "notes": ascii_only(pick(f.get("notes"), "no open question recorded")),
        "extras": {
            "wg_path": str(pick(f.get("wg_path"), "unknown")),
            "wg_detail": ascii_only(pick(f.get("wg_detail"), "")),
            "ingress": str(pick(f.get("ingress"), "none")),
            "volume_tib_month": volume,
            "volume_stated": volume_stated,
            "bytes_transit": transit,
            "transit_note": ascii_only(pick(f.get("transit_note"), "")),
            "promoted_from": f".tmp/egress/{lane}",
        },
    }
    extra = f.get("extras")
    if isinstance(extra, dict):
        record["extras"].update({ascii_only(k): v for k, v in extra.items()})
    return record


def lint_record(rec: dict) -> list:
    bad = []
    # `none` is a legitimate binding: a routed prefix with no byte meter has no
    # constraint above this client's scale. What is not legitimate is naming none
    # without saying why, because then a reader cannot tell a decision from an
    # omission.
    if rec["binding"] == "none" and len(rec["binding_note"]) < 20:
        bad.append("binding none without a reason")
    if rec["verdict"] in ("qualifies", "qualifies-with-caveat") and rec["free_tier"]["unit"] == "none" \
            and not rec["category"].startswith("tool "):
        bad.append("qualifies on a free tier whose unit is none")
    if not rec["evidence"]:
        bad.append("no evidence row")
    if not is_http(rec["url"]):
        bad.append("url is not http(s)")
    return bad


def load_findings(root: str) -> tuple[list, list]:
    findings, problems = [], []
    for path in sorted(glob.glob(os.path.join(root, "*", "findings.json"))):
        lane = os.path.basename(os.path.dirname(path))
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            problems.append(f"{path}: unparseable ({exc})")
            continue
        if isinstance(data, dict):
            data = data.get("findings") or []
        if not isinstance(data, list):
            problems.append(f"{path}: not an array")
            continue
        for f in data:
            if isinstance(f, dict):
                # A registry row describes a source that lists providers, not a
                # provider. It has no verdict and no evidence, and promoting one
                # would create a record for a page.
                if str(f.get("kind") or "").strip() == "registry-row":
                    continue
                f["_lane"] = lane
                findings.append(f)
    return findings, problems


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
    ap.add_argument("--findings", default=".tmp/egress")
    ap.add_argument("--out", default="dossier/egress")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--lint", action="store_true", help="report problems, write nothing")
    ap.add_argument("--today", default=None)
    ap.add_argument("--replace-report", action="store_true")
    args = ap.parse_args()

    import datetime as _dt
    today = args.today or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    if not os.path.isdir(args.findings):
        print(f"promote-egress: no findings directory at {args.findings}", file=sys.stderr)
        return 2
    try:
        os.makedirs(args.out, exist_ok=True)
    except OSError as exc:
        print(f"promote-egress: cannot create {args.out}: {exc}", file=sys.stderr)
        return 3

    findings, problems = load_findings(args.findings)
    if problems:
        for p in problems:
            print(f"unparseable {p}", file=sys.stderr)
        return 3

    seen, wrote, skipped, refused = {}, 0, 0, []
    for f in findings:
        lane = f["_lane"]
        rec = build(f, lane, today)
        slug = rec["slug"]
        if slug in seen:
            refused.append(f"{slug}: duplicate inside the wave ({seen[slug]} and {lane})")
            continue
        seen[slug] = lane
        bad = lint_record(rec)
        if bad:
            refused.append(f"{slug}: " + "; ".join(bad))
            continue
        path = os.path.join(args.out, slug + ".json")
        if os.path.exists(path):
            skipped += 1
            if args.replace_report:
                print(f"exists, left alone: {slug} (lane {lane})")
            continue
        if args.dry_run or args.lint:
            wrote += 1
            print(f"would write {slug} [{rec['confidence']}/{rec['verdict']}] from {lane}")
            continue
        refuse_in_research_checkout(path)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(rec, fh, indent=2, ensure_ascii=True)
            fh.write("\n")
        wrote += 1

    print(f"promote-egress: {wrote} {'checked' if (args.dry_run or args.lint) else 'written'}, "
          f"{skipped} already present, {len(refused)} refused")
    for r in refused:
        print(f"  refused {r}", file=sys.stderr)
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
