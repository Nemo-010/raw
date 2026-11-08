#!/usr/bin/env python3
"""own-hardware.py -- refuse a recommendation to acquire physical hardware.

The failure this prevents: the corpus recommended buying a 20 TB disk, with an
amortisation table and an electricity line, to a client who owns no hardware. The
arithmetic was right and the recommendation was unusable, which is the worst
combination available. A rule in prose did not stop it once, so it is a check.

⭐ **It requires a recommendation context, not just a verb.** "Own" and "build" are
ordinary English words -- "the records own the arithmetic", "serving your own
weights on a free machine", "a licence plus your own hardware" are all correct
sentences that are not advice. What this refuses is an acquisition verb in a
sentence that also prices or recommends: a currency figure, "cheaper", "best",
"recommend", "instead", or "should". Both must hold.

Precision over recall: a check that fires on legitimate prose is a check somebody
switches off, and then the rule has no enforcement at all.

Exit codes: 0 clean, 1 a recommendation found, 2 usage.
"""
import argparse
import os
import re
import sys

SKIP = {"sources", "fixtures", ".tmp", ".git", "node_modules", "target", "dist"}

# The acquisition: a verb that means "obtain or operate physical kit".
ACQUIRE = re.compile(
    r"\b(buy|buying|purchase|purchasing|own|owning|colocate|co-locate|"
    r"shuck|shucking|build|building)\b"
    r"[^.\n]{0,40}\b"
    r"(disk|disks|drive|drives|hdd|ssd|hardware|server|servers|machine|machines|"
    r"nas|homelab|home lab|mini-?pc)\b",
    re.IGNORECASE)

# The recommendation: the sentence prices it or advises it.
RECOMMEND = re.compile(
    r"(\b(usd|eur|gbp|rs|inr)\b\s*[0-9]|[$€£]\s*[0-9]|"
    r"\bcheaper\b|\bcheapest\b|\bbest\b|\brecommend|\binstead\b|\bshould\b|"
    r"\bthe answer is\b|\bworth it\b|\bgo with\b|\bchoose\b)",
    re.IGNORECASE)

# Correct writing names the option in order to exclude it.
EXEMPT = re.compile(
    r"never|not an option|do not|don't|cannot|can't|no hardware|"
    r"forbidden|out of scope|not available|not recommend|excluded|exclude|"
    r"not the recommendation|rather than|instead of|does not have|is not an option",
    re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser(
        description="refuse a recommendation to acquire physical hardware")
    ap.add_argument("--root", default="docs", help="tree to scan (default: docs)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print("own-hardware: not a directory: %s" % args.root, file=sys.stderr)
        return 2

    hits = []
    for dirpath, dirnames, files in os.walk(args.root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if not ACQUIRE.search(line):
                    continue
                if not RECOMMEND.search(line):
                    continue
                if EXEMPT.search(line):
                    continue
                # A quoted line is the vendor's words, not the author's advice.
                if "'" in line or "\u2018" in line or "\u201c" in line:
                    continue
                hits.append({
                    "file": path.replace("\\", "/"),
                    "line": lineno,
                    "text": line.strip()[:150],
                })

    if args.json:
        import json
        print(json.dumps({"checked": args.root, "hits": hits}, indent=2))
    elif args.quiet:
        print("%d recommendation(s) to acquire hardware" % len(hits))
    else:
        out = []
        for h in hits:
            out.append("%s:%d  %s" % (h["file"], h["line"], h["text"]))
        out.append("%d recommendation(s) to acquire hardware" % len(hits))
        # A document line can carry any character, and a Windows console defaults to
        # cp1252 and raises on the first marker glyph. Encode with a replacement
        # rather than crashing a gate check over a display problem.
        sys.stdout.write("\n".join(out).encode("ascii", "replace").decode("ascii") + "\n")

    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
