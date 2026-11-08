#!/usr/bin/env python3
"""manifest.py -- verify that sources/MANIFEST.tsv and sources/ agree.

The failure this prevents: a manifest that names captures that are not there, or
that states a sha256 the file no longer has. Either one lets a document cite
evidence that does not exist, which is the one thing this repository must never
do. A manifest that looks authoritative and is stale is worse than no manifest.

Exit codes: 0 every row checks out, 1 defects found, 2 usage, 3 environment.
"""
import argparse
import csv
import gzip
import hashlib
import json
import os
import re
import sys

COLUMNS = ["captured_at", "url", "final_url", "status", "bytes", "sha256",
           "media_type", "via", "path", "note"]
VIAS = {"fetch", "read", "archive", "crawl", "gh", "probe", "manual"}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


CAPTURE = re.compile(r"^([0-9a-f]{64})\.(md\.gz|json)$")


def check_capture(dirpath, name, verify):
    """sources/c/<aa>/<sha>.md.gz and <sha>.json: a page text a run's evidence cites and its sidecar, indexed by
    the sidecar (scripts/research/capture.py writes both) and not by MANIFEST.tsv. -> a list of problems."""
    sha, kind = CAPTURE.match(name).groups()
    body, side = os.path.join(dirpath, sha + ".md.gz"), os.path.join(dirpath, sha + ".json")
    out = []
    if kind == "json" and not os.path.isfile(body):
        return [("capture-pair", side, "sidecar with no .md.gz beside it")]
    if kind == "md.gz" and not os.path.isfile(side):
        return [("capture-pair", body, "capture with no .json sidecar")]
    if kind == "json" or not verify:
        return out
    try:
        text = gzip.open(body).read()
        meta = json.load(open(side, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [("capture-read", body, str(e)[:120])]
    if hashlib.sha256(text).hexdigest() != sha:
        out.append(("capture-sha256", body, "the page text does not hash to its name"))
    if (meta.get("sha256") or "").replace("sha256:", "") != sha:
        out.append(("capture-sha256", side, "the sidecar names another sha256"))
    if isinstance(meta.get("bytes"), int) and meta["bytes"] != len(text):
        out.append(("capture-size", side, "sidecar states %s bytes, the text has %d" % (meta["bytes"], len(text))))
    return out


PROBE = re.compile(r"^([0-9a-f]{64})((?:\.[a-z0-9]+)?\.gz|\.json)$")


def check_probe(dirpath, name, verify):
    """sources/p/<aa>/<sha><ext>.gz with a sidecar <sha>.json: a probe record a run's `measured` evidence cites,
    copied by the integrator (scripts/research/common.py) and indexed by its sidecar, like sources/c/. A file of
    sources/p/ with no sidecar needs a MANIFEST.tsv row, as before. -> a list of problems, or None when the file
    is not a sidecar pair and so needs a manifest row."""
    sha, tail = PROBE.match(name).groups()
    side = os.path.join(dirpath, sha + ".json")
    bodies = sorted(f for f in os.listdir(dirpath) if f.startswith(sha + ".") and f.endswith(".gz"))
    if tail == ".json":
        if not bodies:
            return [("probe-pair", side, "sidecar with no <sha>.<ext>.gz beside it")]
        return []
    if not os.path.isfile(side):
        return None
    if not verify:
        return []
    body = os.path.join(dirpath, name)
    try:
        data = gzip.open(body).read()
        meta = json.load(open(side, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [("probe-read", body, str(e)[:120])]
    out = []
    if hashlib.sha256(data).hexdigest() != sha:
        out.append(("probe-sha256", body, "the probe record does not hash to its name"))
    if (meta.get("sha256") or "").replace("sha256:", "") != sha:
        out.append(("probe-sha256", side, "the sidecar names another sha256"))
    if isinstance(meta.get("bytes"), int) and meta["bytes"] != len(data):
        out.append(("probe-size", side, "sidecar states %s bytes, the record has %d" % (meta["bytes"], len(data))))
    return out


def resolve(entry, base):
    """Manifest paths are repository-relative; resolve them against the root.

    The first version joined the entry to the working directory, so a run from
    anywhere but the repository root reported every listed capture as absent
    and every present capture as unlisted — ten false problems, exit 1.
    """
    if os.path.isabs(entry):
        return entry
    return os.path.join(base, entry)


def manifest_base(root):
    """The tree the manifest's `path` column is relative to.

    Rows read `sources/2026-10-22/...`, so the base is the directory that
    contains `sources/`, not `sources/` itself.
    """
    root = os.path.abspath(root)
    if os.path.basename(root) == "sources":
        return os.path.dirname(root)
    return root


def main():
    ap = argparse.ArgumentParser(
        description="verify sources/MANIFEST.tsv against the files on disk")
    ap.add_argument("root", nargs="?", default="sources",
                    help="the sources directory (default: sources)")
    ap.add_argument("--verify", action="store_true",
                    help="check hashes and sizes, not just presence")
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each defect is caught and a correct manifest passes")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    root = args.root
    manifest = os.path.join(root, "MANIFEST.tsv")
    if not os.path.isfile(manifest):
        print("manifest: no MANIFEST.tsv at %s" % manifest, file=sys.stderr)
        return 2
    base = manifest_base(root)

    problems = []
    rows = []
    with open(manifest, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames != COLUMNS:
            problems.append({
                "kind": "header",
                "detail": "expected %r, found %r" % (COLUMNS, reader.fieldnames)})
        for i, row in enumerate(reader, start=2):
            rows.append(row)
            for col in COLUMNS:
                if col not in row or row[col] is None:
                    problems.append({"kind": "missing-column", "line": i,
                                     "detail": col})
            via = row.get("via", "")
            if via and via not in VIAS:
                problems.append({"kind": "bad-via", "line": i,
                                 "detail": "%r not in %r" % (via, sorted(VIAS))})
            path = row.get("path") or ""
            if not path:
                continue
            full = resolve(path, base)
            if not os.path.isfile(full):
                problems.append({"kind": "absent", "line": i, "path": path,
                                 "detail": "row names a file that is not there"})
                continue
            if not args.verify:
                continue
            size = os.path.getsize(full)
            stated = str(row.get("bytes", "")).strip()
            if stated.isdigit() and int(stated) != size:
                problems.append({"kind": "size", "line": i, "path": path,
                                 "detail": "stated %s, on disk %d" % (stated, size)})
            digest = sha256_of(full)
            if row.get("sha256", "").strip() not in ("", "-", digest):
                problems.append({"kind": "sha256", "line": i, "path": path,
                                 "detail": "stated %s…, on disk %s…"
                                           % (row["sha256"][:12], digest[:12])})

    listed = {os.path.normcase(os.path.abspath(resolve(r.get("path"), base)))
              for r in rows if r.get("path")}
    for dirpath, _, files in os.walk(root):
        for name in files:
            if name in ("MANIFEST.tsv", "MANIFEST.md", "README.md", "SEED.md"):
                continue
            full = os.path.abspath(os.path.join(dirpath, name))
            if os.path.normcase(full) in listed:
                continue
            rel = os.path.relpath(full, os.path.abspath(root)).replace("\\", "/")
            if rel.startswith("c/") and CAPTURE.match(name):
                for kind, path, detail in check_capture(dirpath, name, args.verify):
                    problems.append({"kind": kind, "path": os.path.relpath(path, base).replace("\\", "/"),
                                     "detail": detail})
                continue
            if rel.startswith("p/") and PROBE.match(name):
                got = check_probe(dirpath, name, args.verify)
                if got is not None:
                    for kind, path, detail in got:
                        problems.append({"kind": kind, "path": os.path.relpath(path, base).replace("\\", "/"),
                                         "detail": detail})
                    continue
            problems.append({"kind": "unlisted",
                             "path": os.path.relpath(full, base).replace("\\", "/"),
                             "detail": "file present but no manifest row"})

    if args.json:
        import json
        print(json.dumps({"rows": len(rows), "problems": problems}, indent=2))
    else:
        for p in problems:
            where = p.get("path") or ("line %s" % p.get("line", "?"))
            print("%-14s %-60s %s" % (p["kind"], where, p["detail"]))
        print("%d row(s), %d problem(s)" % (len(rows), len(problems)))

    return 0 if not problems else 1


# -------------------------------------------------------------------- proof --

def selftest():
    """Each defect is planted, then removed. A check that cannot fail is off."""
    import shutil
    import tempfile

    fails = 0

    def say(ok, name):
        nonlocal fails
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails += 1

    tmp = tempfile.mkdtemp(prefix="manifest-selftest.")
    try:
        root = os.path.join(tmp, "sources")
        os.makedirs(os.path.join(root, "2026-10-22", "topic"))
        body = b"a captured page\n"
        rel = "sources/2026-10-22/topic/capture.txt"
        full = os.path.join(tmp, rel.replace("/", os.sep))
        with open(full, "wb") as fh:
            fh.write(body)
        digest = sha256_of(full)

        def write_manifest(rows):
            with open(os.path.join(root, "MANIFEST.tsv"), "w",
                      encoding="utf-8", newline="") as fh:
                fh.write("\t".join(COLUMNS) + "\n")
                for row in rows:
                    fh.write("\t".join(row.get(c, "") for c in COLUMNS) + "\n")

        good = {"captured_at": "2026-10-22T00:00:00.000Z", "url": "https://x/",
                "final_url": "-", "status": "200", "bytes": str(len(body)),
                "sha256": digest, "media_type": "text/plain", "via": "read",
                "path": rel, "note": "n"}

        write_manifest([good])
        rc = run_check(root, verify=True)
        say(rc == 0, "a correct manifest passes")

        write_manifest([dict(good, path="sources/2026-10-22/topic/gone.txt")])
        say(run_check(root, verify=True) == 1, "a row naming a missing file fails")

        write_manifest([dict(good, bytes="999")])
        say(run_check(root, verify=True) == 1, "a wrong byte count fails --verify")

        write_manifest([dict(good, sha256="0" * 64)])
        say(run_check(root, verify=True) == 1, "a wrong sha256 fails --verify")

        write_manifest([dict(good, via="telepathy")])
        say(run_check(root, verify=False) == 1, "a via outside the vocabulary fails")

        write_manifest([good])
        with open(os.path.join(root, "2026-10-22", "topic", "stray.txt"), "wb") as fh:
            fh.write(b"x")
        say(run_check(root, verify=False) == 1, "an unlisted file fails")
        os.remove(os.path.join(root, "2026-10-22", "topic", "stray.txt"))

        # sources/c/: a capture and its sidecar are indexed by the sidecar, so they need no manifest row
        text = b"page text a run cites\n"
        csha = hashlib.sha256(text).hexdigest()
        cdir = os.path.join(root, "c", csha[:2])
        os.makedirs(cdir)
        with gzip.open(os.path.join(cdir, csha + ".md.gz"), "wb") as fh:
            fh.write(text)
        with open(os.path.join(cdir, csha + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"sha256": "sha256:" + csha, "bytes": len(text)}, fh)
        say(run_check(root, verify=True) == 0, "a sources/c capture with its sidecar passes")
        with open(os.path.join(cdir, csha + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"sha256": "sha256:" + "0" * 64, "bytes": len(text)}, fh)
        say(run_check(root, verify=True) == 1, "a sources/c sidecar that names another hash fails --verify")
        os.remove(os.path.join(cdir, csha + ".json"))
        say(run_check(root, verify=False) == 1, "a sources/c capture with no sidecar fails")
        shutil.rmtree(os.path.join(root, "c"))

        # sources/p/: a probe record the integrator copied is indexed by its sidecar too
        rec = b'{"url": "https://x/", "status": 200, "bytes": 12}\n'
        psha = hashlib.sha256(rec).hexdigest()
        pdir = os.path.join(root, "p", psha[:2])
        os.makedirs(pdir)
        with gzip.open(os.path.join(pdir, psha + ".json.gz"), "wb") as fh:
            fh.write(rec)
        with open(os.path.join(pdir, psha + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"sha256": "sha256:" + psha, "bytes": len(rec), "kind": "probe"}, fh)
        say(run_check(root, verify=True) == 0, "a sources/p probe record with its sidecar passes")
        with open(os.path.join(pdir, psha + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"sha256": "sha256:" + "0" * 64, "bytes": len(rec)}, fh)
        say(run_check(root, verify=True) == 1, "a sources/p sidecar that names another hash fails --verify")
        os.remove(os.path.join(pdir, psha + ".json"))
        say(run_check(root, verify=False) == 1, "a sources/p file with no sidecar and no manifest row fails")
        shutil.rmtree(os.path.join(root, "p"))

        # The defect that made this selftest worth writing: resolve paths
        # against the root, not the working directory.
        write_manifest([good])
        cwd = os.getcwd()
        try:
            os.chdir(tempfile.gettempdir())
            say(run_check(root, verify=True) == 0,
                "paths resolve from any working directory")
        finally:
            os.chdir(cwd)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nmanifest selftest: %s"
          % ("0 failed" if not fails else "%d failed" % fails))
    return 0 if not fails else 1


def run_check(root, verify):
    """Run main() against <root> and return its exit code, quietly."""
    import contextlib
    import io as _io
    argv = sys.argv
    sys.argv = ["manifest.py", root] + (["--verify"] if verify else [])
    try:
        with contextlib.redirect_stdout(_io.StringIO()), \
                contextlib.redirect_stderr(_io.StringIO()):
            return main()
    finally:
        sys.argv = argv


if __name__ == "__main__":
    sys.exit(main())
