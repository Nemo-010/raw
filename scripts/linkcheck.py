#!/usr/bin/env python3
"""linkcheck.py -- every relative Markdown link in the tree resolves.

The failure this prevents: a document links to a file that is not there, and a
reader follows it. The gate checks the links out of `docs/README.md` and the
citation of every verified record; it does not check the thousands of relative
links inside the documents, and those rot every time a file moves.

It reads every `.md` under --root, resolves each `](target)` against the directory
the document lives in, and reports the ones that do not exist. Anchors are
stripped, absolute URLs and `mailto:` are skipped, and a target that is a
directory is accepted.

Exit codes: 0 every link resolves, 1 a link is broken, 2 usage.
"""
import argparse
import os
import re
import sys

SKIP_DIRS = {".tmp", ".git", "node_modules", "target", "dist", "__pycache__",
             # A capture in sources/ is a vendor page as received. Its relative
             # links point at the vendor's own site and are evidence about that
             # site, not links of ours; rewriting them would falsify the capture.
             "sources",
             # The fixtures are deliberately broken; that is their purpose.
             "fixtures"}
LINK = re.compile(r"\]\(([^)\s]+)")


def main():
    ap = argparse.ArgumentParser(
        description="every relative Markdown link in the tree resolves")
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    ap.add_argument("--json", action="store_true", help="machine output")
    ap.add_argument("--quiet", action="store_true", help="print the count only")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("linkcheck: --root is not a directory: %s" % root, file=sys.stderr)
        return 2

    broken = []
    checked = 0
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            for m in LINK.finditer(text):
                target = m.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#",
                                      "kimi-file:", "ftp://")):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                checked += 1
                resolved = os.path.normpath(os.path.join(dirpath, target))
                if not os.path.exists(resolved):
                    broken.append({
                        "file": os.path.relpath(path, root).replace("\\", "/"),
                        "target": target,
                        "line": text[:m.start()].count("\n") + 1,
                    })

    if args.json:
        import json
        print(json.dumps({"checked": checked, "broken": broken}, indent=2))
    elif args.quiet:
        print("%d relative link(s) checked, %d broken" % (checked, len(broken)))
    else:
        for b in broken:
            print("%s:%d  ->  %s" % (b["file"], b["line"], b["target"]))
        print("%d relative link(s) checked, %d broken" % (checked, len(broken)))

    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
