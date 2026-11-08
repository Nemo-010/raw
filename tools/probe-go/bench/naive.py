#!/usr/bin/env python3
"""naive.py — the script a session actually writes when it has no tool.

One probe.py process per host, C at a time. This pays the interpreter start for
every host and is the form the tool is measured against when the question is
"what does a discovery wave cost without a compiler".
"""
import argparse, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PROBE = os.path.join(ROOT, "scripts", "probe", "probe.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=15.0)
    a = ap.parse_args()
    hosts = [l.strip() for l in open(a.listfile) if l.strip() and not l.startswith("#")]

    def one(u):
        p = subprocess.run([sys.executable, PROBE, u, "--timeout", str(a.timeout)],
                           capture_output=True, text=True)
        return p.stdout.strip()

    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        for s in ex.map(one, hosts):
            if s:
                print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
