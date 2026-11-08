"""Line endings: new files under scripts/research and scripts/rq are LF; an existing file keeps the
convention it has at HEAD. Run before a commit when an editor may have rewritten line endings."""
import os
import sys

from common import REPO, git_bytes, status_paths


def head_crlf(rel):
    b = git_bytes(REPO, "show", "HEAD:" + rel, check=False)
    return bool(b) and b.count(b"\r\n") * 2 > b.count(b"\n")


def main(paths):
    for rel in paths:
        p = os.path.join(REPO, rel)
        if not os.path.isfile(p):
            continue
        b = open(p, "rb").read()
        lf = b.replace(b"\r\n", b"\n")
        want = lf.replace(b"\n", b"\r\n") if head_crlf(rel) else lf
        if want != b:
            open(p, "wb").write(want)
            print("eol", rel, "crlf" if want is not lf else "lf")


if __name__ == "__main__":
    paths = sys.argv[1:] or [p for p in status_paths(REPO, "-uall") if p.endswith((".py", ".sh", ".md", ".json", ".tsv", ".yml", "rq"))]
    main(paths)
