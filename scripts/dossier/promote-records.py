#!/usr/bin/env python3
"""Promote a wave of raw dossier records into a topic directory.

PURPOSE
    Research lanes write candidate records under `.tmp/` because a half-written
    record inside `dossier/` fails the gate for every lane still running. This is
    the second half: it takes the finished records, refuses the ones that would
    duplicate a provider already in the dossier, validates the rest against the
    schema, and only then writes them into `dossier/<topic>/`.

WHY IT EXISTS
    The egress wave and the compute wave each needed a one-off script, and a
    one-off script is a rule nobody can re-run. This one is topic-agnostic: the
    topic comes from the argument, and the duplicate rule is the whole dossier,
    because one provider gets one record whatever topic it arrived under.

DEPENDENCIES
    Python standard library. `scripts/dossier/validate.py` beside it, and
    `scripts/dossier/schema.json` at the repository root.

OUTPUT
    JSON by default: {"ok":bool,"accepted":N,"refused":[{file,reason}],"out":...}
    One line per accepted file with --human.

EXIT CODES
    0  every candidate was accepted, or a dry run found nothing to refuse
    1  one or more candidates were refused; the report names them
    2  usage error
    3  environment wrong: schema or validator missing, or the source is unreadable

EXAMPLES
    python scripts/dossier/promote-records.py --source .tmp/debrid \
        --topic debrid --out dossier/debrid --dry-run
    python scripts/dossier/promote-records.py --source .tmp/debrid \
        --topic debrid --out dossier/debrid
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# Typographic punctuation a research lane picks up when it copies a sentence
# from a rendered page. The conventions ban the dash and allow ASCII only, with
# the five markers; the vendor's words survive the substitution, the character
# does not. Non-Latin text is left alone: it is evidence, and 1,226 existing
# records already carry it.
TYPOGRAPHIC = {
    "\u2014": "-", "\u2013": "-", "\u2212": "-",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2026": "...", "\u00a0": " ",
}


def normalise(value):
    if isinstance(value, str):
        for bad, good in TYPOGRAPHIC.items():
            value = value.replace(bad, good)
        return value
    if isinstance(value, list):
        return [normalise(item) for item in value]
    if isinstance(value, dict):
        return {key: normalise(item) for key, item in value.items()}
    return value


def write_json(path, payload):
    """Two-space JSON with a LF terminator, whatever the host platform does by
    default. A CRLF record is a record the corpus's line-ending rule refuses."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def fail(code: int, message: str) -> "NoReturn":
    print(message, file=sys.stderr)
    raise SystemExit(code)


def collect(source: str) -> list[str]:
    """Every candidate record under a lane tree.

    A lane may write `records/*.json` or drop a flat `*.json` beside its
    findings. Both are accepted; anything else is ignored so a `sources.json`
    or a `findings.json` is never mistaken for a record.
    """
    paths = sorted(glob.glob(os.path.join(source, "**", "records", "*.json"),
                             recursive=True))
    if not paths:
        paths = sorted(glob.glob(os.path.join(source, "**", "*.json"),
                                 recursive=True))
    keep = []
    for path in paths:
        base = os.path.basename(path)
        if base in ("sources.json", "findings.json", "summary.json"):
            continue
        keep.append(path)
    return keep


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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Promote raw dossier records into a topic directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True,
                        help="directory holding the lanes' candidate records")
    parser.add_argument("--topic", required=True,
                        help="docs/ topic the records belong to")
    parser.add_argument("--out", required=True,
                        help="target dossier directory, e.g. dossier/debrid")
    parser.add_argument("--schema", default=os.path.join(
        ROOT, "scripts", "dossier", "schema.json"))
    parser.add_argument("--validator", default=os.path.join(
        HERE, "validate.py"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--human", action="store_true")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.source):
        fail(3, "promote: source is not a directory: %s" % args.source)
    if not os.path.isfile(args.schema):
        fail(3, "promote: schema missing: %s" % args.schema)
    if not os.path.isfile(args.validator):
        fail(3, "promote: validator missing: %s" % args.validator)

    existing = {}
    dossier_root = os.path.join(ROOT, "dossier")
    for path in glob.glob(os.path.join(dossier_root, "**", "*.json"),
                          recursive=True):
        if path.endswith(".generated.json"):
            continue
        existing.setdefault(os.path.basename(path)[:-5], path)

    candidates = collect(args.source)
    if not candidates:
        fail(2, "promote: no candidate records under %s" % args.source)

    accepted, refused = [], []
    staged = tempfile.mkdtemp(prefix="promote-records.")
    seen = {}
    try:
        for path in candidates:
            try:
                with open(path, encoding="utf-8") as handle:
                    rec = json.load(handle)
            except Exception as exc:  # noqa: BLE001 - the reason is the report
                refused.append({"file": path, "reason": "unparseable: %s" % exc})
                continue
            if not isinstance(rec, dict):
                refused.append({"file": path, "reason": "not an object"})
                continue
            slug = rec.get("slug") or ""
            if not slug:
                refused.append({"file": path, "reason": "no slug"})
                continue
            if os.path.basename(path)[:-5] != slug:
                refused.append({"file": path,
                                "reason": "filename does not match slug %r" % slug})
                continue
            if rec.get("topic") != args.topic:
                refused.append({"file": path,
                                "reason": "topic is %r, expected %r"
                                          % (rec.get("topic"), args.topic)})
                continue
            if slug in existing:
                refused.append({"file": path,
                                "reason": "duplicate provider: %s" % existing[slug]})
                continue
            if slug in seen:
                refused.append({"file": path,
                                "reason": "duplicate inside this wave: %s" % seen[slug]})
                continue
            seen[slug] = path
            target = os.path.join(staged, slug + ".json")
            # Copy through the normaliser, not byte for byte: a lane that wrote
            # its JSON with Python's text mode on Windows leaves CRLF, and the
            # conventions require LF in every tracked file.
            with open(path, encoding="utf-8") as handle:
                write_json(target, normalise(json.load(handle)))
            accepted.append({"file": path, "slug": slug})

        if accepted:
            result = subprocess.run(
                [sys.executable, args.validator, "--schema", args.schema, staged],
                capture_output=True, text=True)
            if result.returncode != 0:
                try:
                    report = json.loads(result.stdout)
                except Exception:  # noqa: BLE001
                    report = {"errors": [{"message": result.stderr[:400]}]}
                bad = {}
                for err in report.get("errors", []):
                    bad.setdefault(os.path.basename(err.get("file", "?")), []).append(
                        "%s %s" % (err.get("path", ""), err.get("message", "")))
                for item in list(accepted):
                    name = item["slug"] + ".json"
                    if name in bad:
                        refused.append({"file": item["file"],
                                        "reason": "; ".join(bad[name])[:300]})
                        accepted.remove(item)
                        os.remove(os.path.join(staged, name))
            if not accepted:
                fail(1, json.dumps(
                    {"ok": False, "accepted": 0, "refused": refused,
                     "out": args.out}, indent=2))

        if not args.dry_run and accepted:
            refuse_in_research_checkout(args.out)
            os.makedirs(args.out, exist_ok=True)
            for item in accepted:
                shutil.copyfile(os.path.join(staged, item["slug"] + ".json"),
                                os.path.join(args.out, item["slug"] + ".json"))
    finally:
        shutil.rmtree(staged, ignore_errors=True)

    summary = {"ok": not refused, "accepted": len(accepted),
               "refused": refused, "out": args.out,
               "dry_run": bool(args.dry_run)}
    if args.human:
        for item in accepted:
            print("accepted %s" % item["slug"])
        for item in refused:
            print("refused  %s: %s" % (item["file"], item["reason"]))
        print("%d accepted, %d refused" % (len(accepted), len(refused)))
    else:
        print(json.dumps(summary, indent=2))
    return 0 if not refused else 1


if __name__ == "__main__":
    sys.exit(main())
