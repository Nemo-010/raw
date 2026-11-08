#!/usr/bin/env python3
"""tcpprobe.py -- TCP reachability: one connect and one banner read per endpoint.

PURPOSE
    One connect and one banner read per endpoint, written to a dated JSON file
    that a record can cite. The file is the measurement; a number in a document
    that is not in the file is a number nobody can check.

WHY IT EXISTS
    Nine records in `dossier/compute/` were at the `measured` rung and quoted
    connect times that were not in the probe output that was saved. The topic's
    own `measurement.md` explained the gap as "the probe ran twice", and the
    first run was never written to disk. A `measured` claim with no saved run is
    the defect the rung exists to prevent, so this script writes one file per run
    and the records cite the run that is on disk.

WHAT A TIMEOUT MEANS
    A timeout is a fact about the path from this host, not about the provider. It
    is recorded as `ok: false` with the error, and a record citing it says
    `unverified: no TCP answer from this host` rather than `dead`.

    Without --endpoint it probes the fourteen SSH endpoints of the compute topic.
    With --endpoint HOST:PORT (repeatable) it probes only those, for example the
    SMTP submission port (587) or the IMAP port (143) of a mail host. A server
    that speaks TLS first (993, 465) sends no banner, so `banner` is empty there.

DEPENDENCIES
    Python standard library only. Network access to the endpoints only.

OUTPUT
    `<--out>/tcp-probe-<UTC>.json`, plus one JSON object per line on stdout. The
    path is printed on stderr so a shell can capture it. A research lane writes
    it into its workspace and registers it with
    `scripts/rq capture probe:HOST:PORT --lane WS --probe FILE`.

EXIT CODES  (repository map, scripts/README.md)
    0  every endpoint answered and sent a banner
    1  at least one endpoint timed out or sent no banner; the file is still written
    2  usage error
    3  the output file could not be written

USAGE
    python scripts/probe/tcpprobe.py --out .tmp/session-<id>/probe
    python scripts/probe/tcpprobe.py --endpoint smtp.example.org:587 --out WS/probe
"""
import argparse
import datetime
import json
import os
import socket
import sys
import time

TARGETS = [
    ("railway.new", 22),
    ("envs.net", 22),
    ("shells.efn.lt", 22),
    ("sdf.org", 22),
    ("tilde.town", 22),
    ("tilde.club", 22),
    ("tilde.guru", 22),
    ("tilde.green", 22),
    ("hashbang.sh", 22),
    ("blinkenshell.org", 2222),
    ("blinkenshell.org", 22),
    ("ctrl-c.club", 22),
    ("serv00.com", 22),
    ("tilde.zone", 22),
]


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def probe(host, port, timeout=8, wait=6):
    t0 = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
    except Exception as exc:
        return {"host": host, "port": port, "ok": False, "err": repr(exc),
                "ms": int((time.time() - t0) * 1000), "banner": None,
                "probed_at": now_iso()}
    ms = int((time.time() - t0) * 1000)
    sock.settimeout(wait)
    try:
        banner = sock.recv(128).decode("utf-8", "replace").strip()
    except Exception:
        banner = ""
    try:
        peer = sock.getpeername()[0]
    except Exception:
        peer = None
    sock.close()
    return {"host": host, "port": port, "ok": True, "ms": ms, "peer": peer,
            "banner": banner, "probed_at": now_iso()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True,
                    help="directory for the run file: your workspace's probe/ under .tmp/ (no default, so a call never "
                         "writes into the repository root)")
    ap.add_argument("--timeout", type=int, default=8,
                    help="connect timeout in seconds (default 8)")
    ap.add_argument("--endpoint", action="append", default=[], metavar="HOST:PORT",
                    help="probe this endpoint instead of the built-in list; repeatable")
    args = ap.parse_args()

    targets = TARGETS
    if args.endpoint:
        targets = []
        for e in args.endpoint:
            host, _, port = e.rpartition(":")
            if not host or not port.isdigit() or not 0 < int(port) < 65536:
                print("tcpprobe: --endpoint must be HOST:PORT, not %r" % e, file=sys.stderr)
                return 2
            targets.append((host.strip("[]"), int(port)))
    rows = [probe(h, p, timeout=args.timeout) for h, p in targets]

    stamp = now_iso()
    name = "tcp-probe-%s.json" % stamp.replace(":", "").replace("-", "")
    path = os.path.join(args.out, name)
    try:
        os.makedirs(args.out, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"probed_at": stamp, "targets": len(rows), "results": rows},
                      fh, indent=2)
            fh.write("\n")
    except OSError as exc:
        print("tcpprobe: cannot write %s: %s" % (path, exc), file=sys.stderr)
        return 3

    for row in rows:
        print(json.dumps(row))
    # a forward slash on Windows too: a lane pastes the path unquoted into Git Bash, which eats a backslash (LW7-02)
    print("tcpprobe: %s" % path.replace(os.sep, "/"), file=sys.stderr)

    bad = [r for r in rows if not r["ok"] or not r.get("banner")]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
