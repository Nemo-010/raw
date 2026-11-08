#!/usr/bin/env python3
"""script-fallback.py — the fallback documented in ../README.md, runnable.

This is the script probe-go has to beat. It is not a strawman and it is not
optimised beyond what a reader would write: it imports the repository's own
probe.py, so its records are identical by construction, and it runs C threads.

PROBE_NO_SHARED_OPENER=1 runs the same code without the one fix that matters, so
the cost of that fix can be measured rather than asserted.

Usage: ./script-fallback.py LIST --concurrency 8 --timeout 15
"""
import argparse, importlib.util, json, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PROBE = os.path.join(ROOT, "scripts", "probe", "probe.py")

spec = importlib.util.spec_from_file_location("probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=15.0)
    a = ap.parse_args()

    args = probe.build_parser().parse_args(
        ["--timeout", str(a.timeout), "--no-baseline"])
    # probe.main() derives this after parsing; probe_once reads it.
    args.method = "HEAD" if args.head_only else "GET"

    # THE FIX. probe_once() calls _build_opener() on every request, which builds
    # a fresh ssl.create_default_context() and parses the whole CA bundle in
    # Python. Under threads that serialises on the GIL, so --concurrency buys
    # nothing. One opener is safe for independent requests.
    if not os.environ.get("PROBE_NO_SHARED_OPENER"):
        shared = probe._build_opener(args)
        probe._build_opener = lambda _args: shared

    hosts = [l.strip() for l in open(a.listfile)
             if l.strip() and not l.startswith("#")]

    def one(u):
        try:
            return probe.probe_once(u, args)
        except Exception as e:  # noqa: BLE001 - one bad host must not stop a sweep
            return {"url": u, "usable": False, "error": "fallback: %s" % e}

    out = [None] * len(hosts)
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        for i, rec in enumerate(ex.map(one, hosts)):
            out[i] = rec
    for rec in out:
        if rec is not None:
            print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
