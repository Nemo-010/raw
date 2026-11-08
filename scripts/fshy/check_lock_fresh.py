#!/usr/bin/env python3
"""check_lock_fresh.py: is scripts/fshy/public.lock behind the public Worker's rules?

public.lock pins the commit of Azathothas/fshy.ajam.dev that the Python twins (fr.py, build.py) are tested
against. When the public repository changes a rule file of the Worker or the parity fixture, the twins and the
pin move together (scripts/fshy/README.md, "Parity with the public Worker"). This asks the GitHub API for the
newest commit on the default branch of the public repository that touched each of those files, and fails when
the pin does not contain it. It decides by ancestry (the compare endpoint), never by date.

It needs the network, so the offline gate (scripts/gate.sh) does not run it; the job lock-fresh of the workflow
f-research-ci in Azathothas/fshy.ajam.dev does (scripts/research/ci-checks.sh lock).

usage:
  python scripts/fshy/check_lock_fresh.py              check the pin against the public repository
  python scripts/fshy/check_lock_fresh.py --selftest   offline: the decisions and the HTTP layer, on a local stub

  --lock FILE   the lock file (default: public.lock beside this script)
  --repo OWNER/NAME, --api URL   the public repository and the API root (default: the repository named above,
                $GITHUB_API_URL or https://api.github.com). GITHUB_TOKEN or GH_TOKEN, when set, raises the rate
                limit; it is sent only over https and never printed.

Exit codes: 0 fresh, 1 stale (the pin is behind or diverged from a change of a watched file), 2 cannot decide
(network or API failure, rate limit, an unreadable lock). A failure to ask is never reported as stale, and a
stale pin is never reported as a failure to ask.
"""
import argparse
import http.server
import io
import json
import os
import re
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.join(HERE, "public.lock")
REPO = "f-shy/fshy.ajam.dev"
API = "https://api.github.com"
# the files whose change obliges the twins and the pin to move: the rules the twins re-implement, and the fixture
# that proves they agree (test_fr.py reads exactly these from the pin)
PATHS = ("site/worker/guard.js", "site/worker/rank.js", "site/worker/text.js", "site/worker/test/parity.json")
PIN_LINE = re.compile(r"^commit ([0-9a-f]{40})\s*$")


class ApiError(Exception):
    """The answer is unknown: the network, the API or the lock failed. code is the HTTP status, or None. fatal: no
    other call can succeed either (network, a 5xx that outlasted the retries, a spent rate limit, refused
    credentials), so the check stops at once and does not ask once for each file."""

    def __init__(self, message, code=None, fatal=False):
        Exception.__init__(self, message)
        self.message, self.code, self.fatal = message, code, fatal


def read_pin(path):
    """The 40-hex commit of a 'commit <sha>' line (comment lines and blank lines are skipped)."""
    try:
        with open(path, encoding="utf-8") as f:
            for ln in f:
                m = PIN_LINE.match(ln)
                if m:
                    return m.group(1)
    except OSError as e:
        raise ApiError("cannot read %s: %s" % (path, e))
    raise ApiError("%s has no 'commit <40 hex>' line" % path)


class Api:
    """GET against the GitHub REST API: JSON out, ApiError for anything that is not an answer. A 5xx, a dropped
    connection and a timeout are retried at once, or after the server's own Retry-After; no delay is invented
    (backoff is 0 unless a caller sets one). A 4xx is the API's answer and is raised at once with its status."""

    def __init__(self, base=API, token=None, retries=2, backoff=0.0, timeout=20):
        self.base, self.token, self.retries, self.backoff, self.timeout = base.rstrip("/"), token, retries, backoff, timeout

    def headers(self):
        h = {"Accept": "application/vnd.github+json", "User-Agent": "f-research-check-lock-fresh",
             "X-GitHub-Api-Version": "2022-11-28"}
        if self.token and self.base.startswith("https://"):  # a credential is never sent in clear
            h["Authorization"] = "Bearer " + self.token
        return h

    def get(self, endpoint, **params):
        url = self.base + endpoint + ("?" + urllib.parse.urlencode(params) if params else "")
        last, wait = None, 0.0
        for attempt in range(self.retries + 1):
            if attempt and (wait or self.backoff):
                time.sleep(wait or self.backoff * attempt)  # wait: retry-after, the server's own pause
            wait = 0.0
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=self.headers()), timeout=self.timeout) as r:
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")
                try:
                    msg = json.loads(body).get("message") or body
                except (ValueError, AttributeError):
                    msg = body
                msg = str(msg)[:200]
                if e.code >= 500:
                    last = ApiError("HTTP %d from %s: %s" % (e.code, endpoint, msg), e.code, True)
                    ra = (e.headers.get("Retry-After") or "").strip() if e.headers else ""
                    wait = float(ra) if ra.isdigit() else 0.0
                    continue
                if e.code in (403, 429) and (e.headers.get("X-RateLimit-Remaining") == "0" or "rate limit" in msg.lower()):
                    raise ApiError("the GitHub API rate limit is spent (HTTP %d); set GITHUB_TOKEN, or wait" % e.code, e.code, True)
                raise ApiError("HTTP %d from %s: %s" % (e.code, endpoint, msg), e.code, e.code in (401, 403, 429))
            except (urllib.error.URLError, OSError, ValueError) as e:  # URLError, timeouts, resets, a body that is not JSON
                last = ApiError("%s: %s" % (endpoint, getattr(e, "reason", None) or e), None, True)
        raise last


def newest_touching(api, repo, path):
    """{sha, date, subject} of the newest commit of the default branch that changed path."""
    rows = api.get("/repos/%s/commits" % repo, path=path, per_page=1)
    try:
        c = rows[0]
        return {"sha": c["sha"], "date": c["commit"]["committer"]["date"],
                "subject": (c["commit"]["message"].splitlines() or [""])[0]}
    except (IndexError, KeyError, TypeError):
        raise ApiError("the API lists no commit of %s that changed %s; the file may have moved, and PATHS in this "
                       "script would need to follow" % (repo, path))


def relation(api, repo, latest, pin):
    """How the pin stands against a commit: identical, ahead (the pin contains it), behind or diverged."""
    if latest == pin:
        return "identical"
    try:
        d = api.get("/repos/%s/compare/%s...%s" % (repo, latest, pin), per_page=1)
    except ApiError as e:
        if e.code == 404 and "no common ancestor" in e.message.lower():
            return "diverged"
        raise
    st = d.get("status") if isinstance(d, dict) else None
    if st not in ("identical", "ahead", "behind", "diverged"):
        raise ApiError("the compare of %s and %s has no usable status: %r" % (latest[:10], pin[:10], st))
    return st


def check(api, repo, pin, paths=PATHS):
    """-> (rows, stale, errors): rows are (path, commit, relation); stale those whose relation is not identical or
    ahead; errors the messages of the paths that could not be decided. A fatal ApiError is raised, not collected."""
    rows, errors, seen = [], [], {}
    for p in paths:
        try:
            c = newest_touching(api, repo, p)
            if c["sha"] not in seen:
                try:
                    seen[c["sha"]] = relation(api, repo, c["sha"], pin)
                except ApiError as e:
                    if e.fatal:
                        raise
                    seen[c["sha"]] = e  # asked once for a commit that four files may share
            if isinstance(seen[c["sha"]], ApiError):
                raise seen[c["sha"]]
            rows.append((p, c, seen[c["sha"]]))
        except ApiError as e:
            if e.fatal:
                raise
            errors.append("%s: %s" % (p, e.message))
    return rows, [r for r in rows if r[2] not in ("identical", "ahead")], errors


def annotate(level, title, msg, out):
    if os.environ.get("GITHUB_ACTIONS") == "true":  # a line of the Actions log that shows on the run summary
        out.write("::%s title=%s::%s\n" % (level, title, msg.replace("%", "%25").replace("\r", "").replace("\n", " ")))


def main(argv=None, out=None, env=None):
    out = out or sys.stdout
    env = os.environ if env is None else env
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true", help="offline checks of this script")
    ap.add_argument("--lock", default=LOCK)
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--api", default=env.get("GITHUB_API_URL") or API)
    ap.add_argument("--retries", type=int, default=2, help="retries of a 5xx or a dropped connection (default 2)")
    ap.add_argument("--backoff", type=float, default=0.0, help="seconds before a retry that has no Retry-After, then one more "
                    "each time (default 0: a retry is at once, or after the server's Retry-After)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        pin = read_pin(a.lock)
        api = Api(a.api, env.get("GITHUB_TOKEN") or env.get("GH_TOKEN"), a.retries, a.backoff)
        rows, stale, errors = check(api, a.repo, pin)
    except ApiError as e:
        out.write("CANNOT DECIDE (not a stale pin): %s\n" % e.message)
        annotate("error", "lock-fresh: could not decide", e.message, out)
        return 2
    if not stale and not errors:
        out.write("fresh: the pin %s contains the newest change of each of the %d watched files of %s\n"
                  % (pin[:10], len(rows), a.repo))
        for p, c, rel in rows:
            out.write("  %-34s %s  %s  pin is %s\n" % (p, c["sha"][:10], c["date"], rel))
        return 0
    if stale:
        out.write("STALE: %s pins %s of %s, which does not contain the newest change of:\n"
                  % ("scripts/fshy/public.lock" if a.lock == LOCK else a.lock, pin[:10], a.repo))
        for p, c, rel in stale:
            out.write("  %s\n    changed in %s on %s: %s\n    the pin is %s that commit\n"
                      % (p, c["sha"], c["date"], c["subject"], rel))
        try:
            head = api.get("/repos/%s/commits" % a.repo, per_page=1)[0]["sha"]
        except (ApiError, IndexError, KeyError, TypeError):
            head = None
        out.write("fix, in one pull request: change the twins (scripts/fshy/fr.py, build.py) to give the public rule's "
                  "answers, run scripts/fshy/test_fr.py with FSHY_PUBLIC at the public commit you pin, and move the "
                  "pin there (scripts/fshy/README.md, \"Parity with the public Worker\"). The pin line:\n")
        if head:
            out.write("  sed -i 's/^commit [0-9a-f]*$/commit %s/' scripts/fshy/public.lock   # the head of the public "
                      "default branch; a merge commit of the public pull request that changed the rule also works\n" % head)
        else:
            out.write("  git ls-remote https://github.com/%s HEAD   # the head of the public default branch; write it "
                      "as 'commit <sha>' in scripts/fshy/public.lock\n" % a.repo)
        annotate("error", "lock-fresh: public.lock is stale",
                 "pin %s is %s the newest change of %s" % (pin[:10], stale[0][2], ", ".join(r[0] for r in stale)), out)
    if errors:
        out.write("CANNOT DECIDE %d of %d files (not a stale pin):\n" % (len(errors), len(rows) + len(errors)))
        for e in errors:
            out.write("  %s\n" % e)
        annotate("error", "lock-fresh: could not decide", "; ".join(errors), out)
    return 1 if stale else 2


# ------------------------------------------------------------------------------------------------ selftest

def selftest():
    fails = []
    proxy = {k: os.environ.get(k) for k in ("no_proxy", "NO_PROXY")}
    os.environ["no_proxy"] = os.environ["NO_PROXY"] = "127.0.0.1,localhost"  # the stub is local whatever the proxy settings

    def ok(name, cond, detail=""):
        if not cond:
            fails.append(name)
        print("%s  %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + str(detail)[:400]) if detail and not cond else ""))

    PIN, A, B, C = "a" * 40, "b" * 40, "c" * 40, "d" * 40
    HEAD = "e" * 40
    seen = []  # (path, query, Authorization header) of every request the stub got

    class Stub(http.server.BaseHTTPRequestHandler):
        route = None

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
            seen.append((u.path, q, self.headers.get("Authorization")))
            code, headers, body = Stub.route(u.path, q)
            raw = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(code)
            for k, v in headers.items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Stub)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]

    def commit(sha):
        return {"sha": sha, "commit": {"committer": {"date": "2026-10-29T01:02:03Z"}, "message": "worker: a rule\n\nbody"}}

    def route(latest, rel=None, head=HEAD, fail=None):
        """latest: path -> sha ([] lists nothing); rel: sha -> compare status or (code, message); fail: path -> a
        (code, headers, body) answered for that path."""
        rel = rel or {}

        def r(path, q):
            if path.endswith("/commits"):
                p = q.get("path")
                if p is None:
                    return 200, {}, [commit(head)]
                if fail and p in fail:
                    return fail[p]
                v = latest[p]
                return 200, {}, ([commit(v)] if v else [])
            m = re.search(r"/compare/([0-9a-f]{40})\.\.\.([0-9a-f]{40})$", path)
            x = rel[m.group(1)]
            if isinstance(x, tuple):
                return x[0], {}, {"message": x[1]}
            return 200, {}, {"status": x}
        return r

    def run(rt, token=None, lock=None, api=None, extra=()):
        Stub.route = rt
        del seen[:]
        tmp = None
        if lock is None:
            tmp = tempfile.NamedTemporaryFile("w", suffix=".lock", delete=False, encoding="utf-8")
            tmp.write("# a comment\ncommit %s\n" % PIN)
            tmp.close()
            lock = tmp.name
        out = io.StringIO()
        try:
            rc = main(["--lock", lock, "--api", api or base, "--backoff", "0"] + list(extra), out,
                      {"GITHUB_TOKEN": token} if token else {})
        finally:
            if tmp:
                os.unlink(tmp.name)
        return rc, out.getvalue()

    same = {p: A for p in PATHS}
    rc, o = run(route(same, {A: "ahead"}))
    ok("fresh: a pin ahead of the newest change of every file", rc == 0 and o.startswith("fresh:"), (rc, o))
    ok("fresh: one compare for four files that share a commit", sum(1 for s in seen if "/compare/" in s[0]) == 1, seen)
    rc, o = run(route({p: PIN for p in PATHS}))
    ok("fresh: a pin that is the newest change needs no compare", rc == 0 and not any("/compare/" in s[0] for s in seen), (rc, o))
    rc, o = run(route(dict(same, **{PATHS[1]: B}), {A: "identical", B: "behind"}))
    ok("stale: the pin is behind a change of one file; the path, the commit and the fix are printed",
       rc == 1 and PATHS[1] in o and B in o and "sed -i" in o and HEAD in o and "public.lock" in o and PATHS[0] not in o.split("fix,")[0],
       (rc, o))
    rc, o = run(route(dict(same, **{PATHS[3]: C}), {A: "ahead", C: "diverged"}))
    ok("stale: a pin diverged from a change of the fixture", rc == 1 and PATHS[3] in o and "diverged" in o, (rc, o))
    rc, o = run(route(same, {A: (404, "No common ancestor between %s and %s." % (A, PIN))}))
    ok("stale: no common ancestor is diverged", rc == 1, (rc, o))
    rc, o = run(route(same, {A: (404, "Not Found")}))
    ok("cannot decide: the pin or the commit is unknown to the API (404 Not Found), asked once for the shared commit",
       rc == 2 and "CANNOT DECIDE 4 of 4" in o and "STALE" not in o and sum(1 for x in seen if "/compare/" in x[0]) == 1, (rc, o, seen))
    rc, o = run(route(same, {A: "ahead"}, fail={PATHS[0]: (403, {"X-RateLimit-Remaining": "0"}, {"message": "API rate limit exceeded"})}))
    ok("cannot decide: a spent rate limit says to set GITHUB_TOKEN, and stops at the first answer",
       rc == 2 and "GITHUB_TOKEN" in o and len(seen) == 1, (rc, o, seen))
    rc, o = run(route(dict(same, **{PATHS[2]: []}), {A: "ahead"}))
    ok("cannot decide: a watched file with no commit", rc == 2 and PATHS[2] in o, (rc, o))
    rc, o = run(route(dict(same, **{PATHS[1]: B, PATHS[3]: []}), {A: "ahead", B: "behind"}))
    ok("stale wins over an undecided file, and both are printed", rc == 1 and "STALE" in o and "CANNOT DECIDE 1 of 4" in o, (rc, o))

    n = [0]

    def flaky(path, q):
        if q.get("path") == PATHS[0]:
            n[0] += 1
            if n[0] <= 2:
                return 502, {}, {"message": "bad gateway"}
        return route(same, {A: "ahead"})(path, q)
    rc, o = run(flaky)
    ok("a 502 twice is retried and the third answer is used", rc == 0 and n[0] == 3, (rc, n[0], o))
    rc, o = run(route(same, {A: "ahead"}, fail={PATHS[0]: (503, {}, {"message": "down"})}))
    ok("cannot decide: a 503 that never ends is not stale, and is asked 3 times, not 12", rc == 2 and "STALE" not in o and "503" in o and len(seen) == 3, (rc, o, seen))
    rc, o = run(route(same, {A: "ahead"}, fail={PATHS[0]: (200, {}, b"<html>not json</html>")}))
    ok("cannot decide: an answer that is not JSON", rc == 2, (rc, o))
    rc, o = run(route(same, {A: "ahead"}), token="s3cret")
    ok("the token is not sent over http", rc == 0 and all(s[2] is None for s in seen), seen)
    ok("the token is sent over https only, and never printed", Api("https://x", "s3cret").headers().get("Authorization") == "Bearer s3cret"
       and "Authorization" not in Api("http://x", "s3cret").headers() and "s3cret" not in o)

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    dead = "http://127.0.0.1:%d" % s.getsockname()[1]
    s.close()
    rc, o = run(route(same), api=dead, extra=["--retries", "1"])
    ok("cannot decide: a refused connection is a failure to ask, never a stale pin", rc == 2 and "STALE" not in o and "CANNOT DECIDE" in o
       and o.count("CANNOT DECIDE") == 1, (rc, o))
    tmp = tempfile.NamedTemporaryFile("w", suffix=".lock", delete=False, encoding="utf-8")
    tmp.write("# no commit line here\ncommit abc\n")
    tmp.close()
    rc, o = run(route(same), lock=tmp.name)
    os.unlink(tmp.name)
    ok("cannot decide: a lock with no 40-hex commit line", rc == 2 and "no 'commit" in o, (rc, o))
    rc, o = run(route(same), lock=os.path.join(HERE, "no-such.lock"))
    ok("cannot decide: a missing lock", rc == 2, (rc, o))
    try:
        ok("the real public.lock holds a 40-hex pin", len(read_pin(LOCK)) == 40)
    except ApiError as e:
        ok("the real public.lock holds a 40-hex pin", False, e.message)
    srv.shutdown()
    for k, v in proxy.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    print("%s: %d failed" % ("FAIL" if fails else "PASS", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
