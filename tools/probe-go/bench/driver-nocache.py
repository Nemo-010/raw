#!/usr/bin/env python3
"""driver-nocache.py — one process, C threads, WITHOUT the shared opener.

probe.py has no fan-out mode: --concurrency probes urls[:N] and stops. So the
script alternatives are:

  naive.py    one process per host            -> startup cost per host
  fallback.py N/C processes, chunks of N      -> startup cost per chunk
  driver.py   ONE process, imports probe_once -> startup cost once, then workers

driver.py is the strongest form and therefore the only fair competitor. If a
compiled tool cannot beat this by 2x, the tool is not justified, because this is
what a reader can actually write in twelve lines with nothing installed.

It imports the repository's own primitive rather than reimplementing it, so the
records are identical by construction.

Usage: driver-nocache.py LIST --concurrency 8 --timeout 15
"""
import argparse, importlib.util, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PROBE = os.path.join(ROOT, "scripts", "probe", "probe.py")

spec = importlib.util.spec_from_file_location("probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def make_args(timeout):
    args = probe.build_parser().parse_args(
        ["--timeout", str(timeout), "--no-baseline"])
    # probe.main() derives these two after parsing; probe_once needs them.
    args.method = "HEAD" if args.head_only else "GET"
    return args


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=15.0)
    a = ap.parse_args()

    hosts = [l.strip() for l in open(a.listfile) if l.strip() and not l.startswith("#")]
    args = make_args(a.timeout)

    # probe.py builds its opener per call, which is correct and slightly wasteful;
    # running it as-is is the point: this arm must not be optimised beyond what a
    # reader would write.
    def one(u):
        try:
            return probe.probe_once(u, args)
        except Exception as e:  # noqa: BLE001
            return {"url": u, "usable": False, "error": "driver: %s" % e}

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
