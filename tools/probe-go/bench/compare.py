#!/usr/bin/env python3
"""compare.py — time probe-go against the script fallback on one host list.

This is the script that produced the numbers in ../README.md. It is committed so
the measurement can be re-run and, if it changes, corrected, rather than taken on
trust.

Two modes:

  --live LIST          real hosts from a file. Both arms pay the same RTT, so
                       this measures the network more than the tool. It is here
                       because it is the obvious benchmark and it should be shown.
  --modeled --hosts N  a loopback server that sleeps for --rtt. This is the
                       honest instrument: it holds the network constant and lets
                       the tool's own cost show.

Both arms emit one JSON record per host. A record counts as answered if it parses
and as usable if it says so, so the two arms are compared on output as well as
on time.

Usage:
  ./compare.py --modeled --hosts 250 --concurrency 8 --rtt 0.10 --rounds 3
  ./compare.py --live hosts.txt --concurrency 8 --timeout 15 --rounds 4
"""
import argparse, json, os, socket, socketserver, subprocess, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
GO = os.path.join(ROOT, "tools", "probe-go", "dist", "probe-go.exe")
SCRIPT = os.path.join(HERE, "script-fallback.py")

BODY = b'{"code":200,"data":{"items":[1,2,3]}}\n'


# ------------------------------------------------------------------ server --

def start_server(rtt):
    """A loopback HTTP/1.1 server that sleeps rtt/2 before the head and before
    the body, so one request costs one modelled round trip."""
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            conn = self.request
            try:
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(4096)
                    if not chunk:
                        return
                    data += chunk
                if rtt:
                    time.sleep(rtt / 2)
                head = (b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                        b"Content-Length: " + str(len(BODY)).encode() +
                        b"\r\nConnection: close\r\n\r\n")
                conn.sendall(head)
                if rtt:
                    time.sleep(rtt / 2)
                conn.sendall(BODY)
            except OSError:
                pass

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True
        request_queue_size = 4096

    srv = Server(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def write_list(path, port, n):
    with open(path, "w") as fh:
        for i in range(n):
            fh.write("http://127.0.0.1:%d/item/%d\n" % (port, i))


# ------------------------------------------------------------------- arms --

def count(out):
    n = ok = 0
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        n += 1
        ok += bool(d.get("usable"))
    return n, ok


def run_arm(arm, listfile, conc, timeout):
    if arm == "go":
        cmd = [GO, "--urls-file", listfile, "--concurrency", str(conc),
               "--timeout", str(timeout)]
    elif arm == "script":
        cmd = [sys.executable, SCRIPT, listfile, "--concurrency", str(conc),
               "--timeout", str(timeout)]
    elif arm == "script-noopener":
        # The same fallback WITHOUT the shared opener, to show what the fix is
        # worth. One environment variable, because that is a one-line change.
        env = dict(os.environ, PROBE_NO_SHARED_OPENER="1")
        cmd = [sys.executable, SCRIPT, listfile, "--concurrency", str(conc),
               "--timeout", str(timeout)]
        t = time.perf_counter()
        p = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return time.perf_counter() - t, *count(p.stdout)
    else:
        raise SystemExit("unknown arm %r" % arm)

    t = time.perf_counter()
    p = subprocess.run(cmd, capture_output=True, text=True)
    return time.perf_counter() - t, *count(p.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile", nargs="?")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--modeled", action="store_true")
    ap.add_argument("--hosts", type=int, default=250)
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--rtt", type=float, default=0.10)
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--arms", default="go,script")
    ap.add_argument("--json-out")
    a = ap.parse_args()

    if not (a.live or a.modeled):
        raise SystemExit("give --live LIST or --modeled")
    if not os.path.exists(GO):
        raise SystemExit("build it first: cd tools/probe-go && make build")

    srv = None
    if a.modeled:
        srv, port = start_server(a.rtt)
        listfile = os.path.join(HERE, ".compare-list.txt")
        write_list(listfile, port, a.hosts)
    else:
        listfile = a.listfile
        if not listfile:
            raise SystemExit("--live needs a list file")
        a.hosts = sum(1 for l in open(listfile)
                      if l.strip() and not l.startswith("#"))

    arms = a.arms.split(",")
    rounds = []
    try:
        # Warm-up: the first execution of a freshly built 7.7 MiB binary pays
        # page-cache misses that the script does not, because Python's interpreter
        # is already resident. Without this the first round measures the disk.
        for arm in arms:
            run_arm(arm, listfile, a.concurrency, a.timeout)
        print("warm-up done", file=sys.stderr)

        for r in range(a.rounds):
            order = arms if r % 2 == 0 else list(reversed(arms))
            row = {"round": r + 1, "order": order}
            for arm in order:
                wall, n, ok = run_arm(arm, listfile, a.concurrency, a.timeout)
                row[arm] = {"wall_s": round(wall, 3), "records": n, "usable": ok}
                print("%-13s %-8s %7.3fs  records %d/%d  usable %d"
                      % ("rtt=%.0fms" % (a.rtt * 1000) if a.modeled else "live",
                         arm, wall, n, a.hosts, ok), file=sys.stderr)
            for k in arms:
                if k != "go":
                    row["ratio_%s_vs_go" % k] = round(row[k]["wall_s"] / row["go"]["wall_s"], 2)
            rounds.append(row)
    finally:
        if srv:
            srv.shutdown()
            srv.server_close()

    out = {"mode": "modeled" if a.modeled else "live", "hosts": a.hosts,
           "concurrency": a.concurrency, "rtt_s": a.rtt if a.modeled else None,
           "rounds": rounds}
    print(json.dumps(out, indent=2))
    if a.json_out:
        with open(a.json_out, "w") as fh:
            json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
