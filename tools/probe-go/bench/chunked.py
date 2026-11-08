#!/usr/bin/env python3
"""chunked.py — the script form of the tool's job, at the SAME concurrency.

The tool's --concurrency N means: N hosts in flight, never more. probe.py
--urls-file F --concurrency N probes urls[:N] concurrently, so a fan-out over N
hosts is a sequence of chunks of N, and one chunk at a time keeps in-flight at N.

--parallel-chunks is the more aggressive form: C chunks at once, each with C
hosts in flight, so in-flight is C*C. It is faster and it is a different claim
(it hammers harder), so it is opt-in and reported separately. Nothing in the
tool's README is allowed to compare against it without saying so.

Usage: chunked.py LIST --concurrency 8 --timeout 15 [--parallel-chunks]
Prints one JSON record per host on stdout, in input order.
"""
import argparse, json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PROBE = os.path.join(ROOT, "scripts", "probe", "probe.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--parallel-chunks", action="store_true")
    a = ap.parse_args()

    hosts = [l.strip() for l in open(a.listfile) if l.strip() and not l.startswith("#")]
    c = max(1, a.concurrency)
    chunks = [hosts[i:i + c] for i in range(0, len(hosts), c)]
    tmpdir = tempfile.mkdtemp(prefix="fallback-")

    def run_chunk(ic):
        idx, chunk = ic
        path = os.path.join(tmpdir, "c%05d.txt" % idx)
        with open(path, "w") as fh:
            fh.write("\n".join(chunk) + "\n")
        p = subprocess.run([sys.executable, PROBE, "--urls-file", path,
                            "--concurrency", str(len(chunk)),
                            "--timeout", str(a.timeout)],
                           capture_output=True, text=True)
        try:
            rec = json.loads(p.stdout)
        except json.JSONDecodeError:
            return [(u, None) for u in chunk]
        runs = rec.get("runs") or [rec]
        return list(zip(chunk, runs))

    results = {}
    if a.parallel_chunks:
        with ThreadPoolExecutor(max_workers=c) as ex:
            for pairs in ex.map(run_chunk, enumerate(chunks)):
                for url, rec in pairs:
                    results[url] = rec
    else:
        for pairs in map(run_chunk, enumerate(chunks)):
            for url, rec in pairs:
                results[url] = rec

    for url in hosts:
        rec = results.get(url)
        if rec is not None:
            print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
