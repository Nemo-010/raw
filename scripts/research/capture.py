"""rq capture: read a page once, keep its text by content hash, and print the hash a claim cites.

  scripts/rq capture URL --lane DIR             fetch through scripts/broker/broker.sh; returns at once
  scripts/rq capture URL --lane DIR --wait      the same, and when the broker asks for a pause, wait and read again
  scripts/rq capture URL --lane DIR --provider ID   the same read, pinned to one provider of the broker
  scripts/rq capture URL --lane DIR --from-file PAGE.md   register text your own tool fetched
  scripts/rq capture --check sha256:... "exact quote" --lane DIR      is the quote in that capture?
  scripts/rq capture probe:TARGET --lane DIR --probe RECORD.json     register a probe record (a `measured` claim)

DIR is your own folder under .tmp/: a lane's unit folder, your .tmp/session-<id>/, or a merge session's
.tmp/review-<run>/ (made and registered on first use). Every read is fresh: there is no page cache, no bucket and no
rate (AGENTS.md section 2 rule 15). When the broker answers 429 or 503 with Retry-After, capture prints
retry_after=N and retry_at=<UTC> and exits 4: read other pages and read that one again after retry_at, or run it with
--wait, which waits in the same command and repeats only the curl call.

A capture is evidence only after a change that cites it is integrated; then it is copied to sources/c/ on the run
branch. A probe record (the JSON that scripts/probe/probe.py, tcpprobe.py or cartcheck.py writes) is copied to
sources/p/; the evidence row that cites it has the URL probe:TARGET, the hash as `capture`, and a span of the record
as `quote`. Exit codes: 0 captured, 1 the origin refused (the page is still kept, with its status), 2 usage,
3 environment, 4 the broker refused, or answered with its own problem JSON in place of the page (nothing is stored
and nothing is established about the target; the message names the next route).
"""
import json
import os
import re
import shlex
import subprocess
import sys

from common import BASH, Fail, REPO, quote_found, read_capture, read_json, sha256_text, stamp, tmp_rel, write_json

FRONT = re.compile(r"^---\n(.*?)\n---\n?", re.S)


def parse_broker(out):
    meta, body = {}, out
    m = FRONT.match(out.replace("\r\n", "\n"))
    if m:
        body = out.replace("\r\n", "\n")[m.end():]
        for ln in m.group(1).split("\n"):
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta, body


def store(lane, url, text, meta):
    if not os.path.isdir(lane):
        # a lane folder that is gone (a wipe after the run merged) receives nothing: a capture that wakes late writes
        # no file outside an id folder
        raise Fail("no lane folder %s; a capture writes only into a folder that exists" % lane, 2)
    sha = sha256_text(text)
    h = sha.split(":", 1)[1]
    d = os.path.join(lane, "captures")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, h + ".md")
    if not os.path.exists(p):
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    # the broker sends the upstream status as a number, or as the text "null" when it has none: keep a known one only
    st = meta.get("upstream_status")
    st = int(st) if str(st).isdigit() else None
    info = {"url": url, "final_url": meta.get("final_url") or url, "status": st,
            "fetched_at": meta.get("fetched_at") or stamp(), "title": meta.get("title"), "via": meta.get("via", "broker read")}
    write_json(os.path.join(d, h + ".json"), info)
    return sha, p, info


RETRY_RE = re.compile(r"retry_after=(\d+)\s+retry_at=(\S+)")
BROKER_LINK = re.compile(r"^https?://(?:[a-z0-9-]+\.)*web\.pkgforge\.dev(?:[/?#]|$)", re.I)


def broker_problem(body):
    """The broker's own problem answer (RFC 9457 JSON with a `reason` and a `see` or `type` link to
    *.web.pkgforge.dev), which broker.sh passes through with its 4xx status as if the origin had sent it: it is not
    the page, and storing it would let a lane quote the broker's error as evidence about the target (W2-07).
    -> the parsed problem, or None."""
    t = (body or "").strip()
    if not t.startswith("{") or len(t) > 20000:
        return None
    try:
        d = json.loads(t)
    except ValueError:
        return None
    if not isinstance(d, dict) or "reason" not in d:
        return None
    if any(isinstance(d.get(k), str) and BROKER_LINK.match(d[k]) for k in ("see", "type", "instance")):
        return d
    return None


def read_providers(lane, repo=REPO, skip=None):
    """The ids of the broker's providers that serve `read` and are not failing, from `broker.sh status` (its
    `providers` list): the pins of rung 2 of the ladder (LW7-03). -> [id], or [] when the status could not be read."""
    tmp = os.path.join(lane, "tmp")
    os.makedirs(tmp, exist_ok=True)
    tmp = tmp.replace("\\", "/")
    env = dict(os.environ, PYTHON=sys.executable.replace("\\", "/"), TMPDIR=tmp, TMP=tmp, TEMP=tmp)
    try:
        r = subprocess.run([BASH, os.path.join(repo, "scripts", "broker", "broker.sh"), "status"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120, env=env)
        d = json.loads(r.stdout or "{}")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return []
    out = []
    for p in d.get("providers") or [] if isinstance(d, dict) else []:
        if isinstance(p, dict) and "read" in (p.get("caps") or []) and p.get("state") != "failing" and p.get("id") \
                and p["id"] != skip and re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", p["id"]):
            out.append(p["id"])
    return out


def next_route(url, lane, repo=REPO, provider=None):
    """The routes of the ladder as commands to paste: the URL quoted (an & splits a shell line), TMPDIR in the lane's
    folder (lane brief rule 10) (W6-03), and the provider ids the broker's status lists for read (LW7-03)."""
    rel = os.path.relpath(lane, repo).replace("\\", "/")
    q, ql = shlex.quote(url), shlex.quote(rel)
    ids = read_providers(lane, repo, skip=provider)
    pins = ("each of these ids in turn: %s" % ", ".join(ids)) if ids else (
        "each id whose caps hold read in the providers list of TMPDIR=%s/tmp sh scripts/broker/broker.sh status" % ql)
    return ("Next route: scripts/rq capture %s --lane %s --provider ID (a pinned provider), with ID %s; or TMPDIR=%s/tmp "
            "sh scripts/broker/broker.sh fetch %s --dump-headers > %s/tmp/page.txt, then scripts/rq capture %s --lane %s "
            "--from-file %s/tmp/page.txt; or TMPDIR=%s/tmp sh scripts/broker/broker.sh archive %s --at YYYY-MM"
            % (q, ql, pins, ql, q, ql, q, ql, ql, ql, q))


def fetch(url, lane, wait=False, repo=REPO, provider=None):
    """One read through broker.sh, pinned to one of the broker's providers with provider (rung 2 of the ladder in
    docs/crawler-scraper/free/broker.md). The retry on a broker 429 or 503 with Retry-After lives in broker.sh: with
    --wait (BROKER_WAIT=1) only the curl call repeats; without it the read exits 4 at once with retry_after and retry_at."""
    if not re.match(r"^https?://", url or ""):
        raise Fail("capture needs an http(s) URL", 2)
    if provider is not None and not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", provider):
        raise Fail("--provider takes a provider id of the broker (letters, digits, dot, dash, underscore)", 2)
    if not os.path.isdir(lane):
        raise Fail("no lane folder %s" % lane, 2)
    # the broker's temporary files (mktemp, and bash's here-document files) go into the lane folder, which the wipe
    # deletes, never into the system's temporary folder
    tmp = os.path.join(lane, "tmp")
    os.makedirs(tmp, exist_ok=True)
    tmp = tmp.replace("\\", "/")
    env = dict(os.environ, PYTHON=sys.executable.replace("\\", "/"), TMPDIR=tmp, TMP=tmp, TEMP=tmp,
               PYTHONPYCACHEPREFIX=os.path.join(repo, ".tmp", "rq", "pycache"))
    if wait:
        env["BROKER_WAIT"] = "1"
    broker = os.path.join(repo, "scripts", "broker", "broker.sh")
    try:
        # without --wait the read itself never waits, so a timeout guards a hung connection; with --wait the broker's
        # own Retry-After decides how long it takes
        r = subprocess.run([BASH, broker, "read", url] + (["--provider", provider] if provider else []),
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=None if wait else 120, env=env)
    except FileNotFoundError:
        raise Fail("sh is not on PATH; fetch the page with your own tool and use --from-file", 3)
    except subprocess.TimeoutExpired:
        raise Fail("the broker did not answer within 120 s; nothing is established about the target", 4)
    if r.returncode == 4:
        m = RETRY_RE.search(r.stderr or "")
        if m:
            raise Fail("retry_after=%s retry_at=%s: the broker asked for a pause. Read your other pages and read this one "
                       "again after %s, or run it with --wait. Nothing is established about the target"
                       % (m.group(1), m.group(2), m.group(2)), 4)
        raise Fail("the broker refused (exit 4): %s. Nothing is established about the target"
                   % (r.stderr.strip()[:200] or "an outage"), 4)
    if r.returncode in (2, 3):
        raise Fail("broker usage or environment error (exit %d): %s" % (r.returncode, r.stderr.strip()[:200]), 3)
    meta, body = parse_broker(r.stdout)
    if not body.strip():
        raise Fail("the broker returned an empty body for %s (exit %d); do not treat it as a finding" % (url, r.returncode), 4)
    prob = broker_problem(body)
    if prob is not None:
        raise Fail("the broker could not read %s (%s: %s; HTTP %s from the broker, upstream status %s). That answer is the "
                   "broker's, not the page, and nothing was stored; nothing is established about the target. %s"
                   % (url, prob.get("reason"), prob.get("title") or prob.get("detail") or "-", prob.get("status") or "-",
                      prob.get("upstream_status", "-"), next_route(url, lane, repo, provider)), 4)
    meta["via"] = "broker read" + (" --provider %s" % provider if provider else "")
    sha, p, info = store(lane, url, body, meta)
    # stored: exit 0 whatever the origin answered (the broker's exit 1 for an origin 4xx or 5xx); the printed status=
    # says what it answered, and a lane that chains commands goes on (W5-10)
    return sha, p, info, 0


# the Cloudflare location that served the reading machine, in a header dump (`broker.sh fetch URL --dump-headers`):
# the suffix of cf-ray ("a52755de7bfacc10-KTM") and the value of cf-placement ("local-KTM") name where that machine
# is, its network identity (lane rule 5); probe.py drops the same suffix (W3-13)
CF_RAY_RE = re.compile(r"(?im)^(\s*cf-ray\s*:\s*[0-9a-f]+)-[A-Z]{3}\b")
CF_PLACEMENT_RE = re.compile(r"(?im)^(\s*cf-placement\s*:)[^\r\n]*")


def scrub_location(text):
    """A registered file without the location of the machine that read it (W5-05)."""
    text = CF_RAY_RE.sub(r"\1-[redacted]", text)
    return CF_PLACEMENT_RE.sub(r"\1 [redacted]", text)


def from_file(url, lane, path):
    if not os.path.exists(path):
        raise Fail("no file %s" % path, 2)
    text = open(path, encoding="utf-8", errors="replace").read()
    if not text.strip():
        raise Fail("%s is empty" % path, 2)
    return store(lane, url, scrub_location(text), {"via": "registered from a file the lane fetched", "fetched_at": stamp()})


PROBE_MAX_BYTES = 1 << 20


def from_probe(target, lane, path):
    """A probe record: the text of the file as it is, hashed like a page, with a sidecar of kind probe. The
    integrator copies it to sources/p/, so the audit and a merge session can read what the probe saw."""
    if not os.path.isfile(path):
        raise Fail("no file %s" % path, 2)
    if os.path.getsize(path) > PROBE_MAX_BYTES:
        raise Fail("%s is larger than %d bytes; register the probe's JSON record, not a body it read" % (path, PROBE_MAX_BYTES), 2)
    try:
        text = open(path, encoding="utf-8").read()
    except UnicodeDecodeError:
        raise Fail("%s is not UTF-8 text; register the probe's JSON record" % path, 2)
    if not text.strip():
        raise Fail("%s is empty" % path, 2)
    target = target if target.startswith("probe:") else "probe:" + target
    if len(target) <= len("probe:"):
        raise Fail("--probe needs the target, for example probe:https://host/path or probe:smtp.host:587", 2)
    try:
        rec = json.loads(text)
    except ValueError:
        rec = None
    # a body that probe.py --save-body wrote, which a probe record beside it names by its full sha256: the measured
    # value is in the body (a DoH answer's "Status": 3), and the record proves when and from where it was read (W2-08)
    body_of = probe_body_of(path)
    if rec is not None and not looks_like_probe(rec) and not body_of:
        raise Fail("%s is JSON but not a probe record: it needs probe_version (probe.py), results of host, port and ok "
                   "(tcpprobe.py), warm and verdict (cartcheck.py), or probed_at (another probe tool). A body that "
                   "probe.py read is registered when it was saved with probe.py URL --save-body FILE --out DIR, the "
                   "record in the same folder as FILE" % path, 2)
    host = target_host(target)
    named = text if not body_of else open(os.path.join(os.path.dirname(os.path.abspath(path)), body_of[0]),
                                          encoding="utf-8").read()
    if host and host.lower() not in named.lower():
        raise Fail("the record never names %s, the host of %s: register it for the target it probed" % (host, target), 2)
    h = sha256_text(text).split(":", 1)[1]
    old = read_json(os.path.join(lane, "captures", h + ".json"), {}) or {}
    sha, p, info = store(lane, target, text, {"via": "probe record registered from a file", "fetched_at": stamp()})
    targets = [t for t in old.get("targets") or [] if t != target] + [target]
    info.update({"kind": "probe", "file": os.path.basename(path), "format": "text" if rec is None else "json",
                 "targets": targets})
    if body_of:
        # the record of the measurement is not stored beside the body, and the lane's folder goes with the wipe: the
        # sidecar keeps what the record says about the read (METHODOLOGY.md section 15 item 3; W4-09)
        info.update({"format": "body", "record": body_of[0], "probed_at": body_of[1]})
        info["measurement"] = {k: body_of[2].get(k) for k in PROBE_FIELDS if k in body_of[2]}
        if isinstance(body_of[2].get("status"), int):
            info["status"] = body_of[2]["status"]
    if isinstance(rec, dict) and isinstance(rec.get("status"), int):
        info["status"] = rec["status"]
    write_json(os.path.join(lane, "captures", h + ".json"), info)
    return sha, p, info


# the fields of a probe.py record that a body's sidecar keeps: the measurement, not the headers it saw
PROBE_FIELDS = ("probe_version", "url", "final_url", "method", "status", "bytes", "sha256", "sha256_scope",
                "content_type", "elapsed_ms", "error", "probed_at")


def probe_body_of(path):
    """(record file name, probed_at, record) of the probe.py record in the same folder whose sha256, taken over the
    whole body, is the hash of this file's bytes, or None. Only a file that probe.py --save-body wrote has such a
    record."""
    import hashlib
    try:
        with open(path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None
    d = os.path.dirname(os.path.abspath(path))
    for n in sorted(os.listdir(d)):
        p = os.path.join(d, n)
        if not n.endswith(".json") or os.path.abspath(p) == os.path.abspath(path) or os.path.getsize(p) > PROBE_MAX_BYTES:
            continue
        try:
            r = read_json(p, None)
        except Exception:
            continue
        if isinstance(r, dict) and r.get("probe_version") and r.get("sha256_scope") == "full" and \
                str(r.get("sha256") or "").lower() == h:
            return n, r.get("probed_at"), r
    return None


def looks_like_probe(rec):
    """The keys of the probe tools of scripts/probe/, or the probed_at instant every probe record carries."""
    if not isinstance(rec, dict):
        return False
    if "probe_version" in rec or "probed_at" in rec or ("warm" in rec and "verdict" in rec):
        return True
    rows = rec.get("results")
    return isinstance(rows, list) and bool(rows) and all(isinstance(x, dict) and {"host", "port", "ok"} <= set(x) for x in rows)


def target_host(target):
    """The host a probe: target names: probe:https://host/path -> host, probe:host:587 -> host, else None."""
    from urllib.parse import urlsplit
    rest = target[len("probe:"):]
    if re.match(r"^[a-z][a-z0-9+.-]*://", rest, re.I):
        return (urlsplit(rest).hostname or None)
    m = re.match(r"^\[?([A-Za-z0-9.:-]+?)\]?:\d+$", rest)
    if m and "." in m.group(1):
        return m.group(1)
    return None


def check(sha, quote, lane, repo=REPO):
    view = None
    if review_folder(repo, lane):
        # a merge session's .tmp/review-RUN/ reads the captures the run branch holds, also from origin (W-03)
        from common import run_or_ref_tree
        try:
            view, _ = run_or_ref_tree(repo, os.path.basename(lane.rstrip("/\\"))[len("review-"):])
        except Fail:
            view = None
    text = read_capture(sha, repo, lane, view)
    if text is None:
        raise Fail("no capture %s in %s, sources/c/ or sources/p/" % (sha, lane), 1)
    verdict, score = quote_found(quote, text)
    return verdict, score


def review_folder(repo, lane):
    """.tmp/review-<run>/ is a merge session's folder: made and registered on first use. -> True when lane is one."""
    rel = os.path.relpath(lane, os.path.join(repo, ".tmp")).replace("\\", "/")
    return bool(re.match(r"^review-[A-Za-z0-9._-]+$", rel))


def cmd(args):
    if not args.lane:
        raise Fail("--lane names your folder under .tmp/: your unit folder in a run, your .tmp/session-<id>/ "
                   "(scripts/rq folder session makes it), or .tmp/review-RUN/ in a merge session", 2)
    lane = os.path.abspath(args.lane)
    if not tmp_rel(lane, REPO):
        # a folder outside .tmp/<id>/ (docs, the repository root, .tmp/ itself, .tmp/rq/) would receive captures/ and
        # tmp/ that no wipe deletes, beside tracked files every research agent shares (LIO3-02)
        raise Fail("--lane must be your folder under .tmp/<id>/: your unit folder in a run, your .tmp/session-<id>/, or "
                   ".tmp/review-RUN/ in a merge session; %s is not (AGENTS.md section 2 rule 14)" % args.lane, 2)
    if args.check:
        verdict, score = check(args.check, args.url, lane)
        print("%s %.2f" % (verdict, score))
        return 0 if verdict != "miss" else 1
    if not os.path.isdir(lane) and review_folder(REPO, lane):
        import state
        state.register_folder(REPO, os.path.basename(lane), "review", drain=False)
        os.makedirs(os.path.join(lane, "captures"), exist_ok=True)
    if not os.path.isdir(lane):
        # a lane of a run is made by rq plan and a session folder by rq folder session; a missing one is a typing
        # mistake or a folder a wipe deleted, so it is refused and nothing is written (R3-B-09)
        raise Fail("--lane must name your folder, which exists already: %s does not" % args.lane, 2)
    if not args.url:
        raise Fail("capture needs a URL", 2)
    read = False
    if getattr(args, "probe", None):
        sha, p, info = from_probe(args.url, lane, args.probe)
        code = 0
    elif args.from_file:
        sha, p, info = from_file(args.url, lane, args.from_file)
        code = 0
    else:
        sha, p, info, code = fetch(args.url, lane, wait=getattr(args, "wait", False), provider=getattr(args, "provider", None))
        read = True
    st = info.get("status")
    if read:
        # a read whose answer carried no status says so: a lane cannot tell a 200 from an unknown answer otherwise
        # (LW7-10)
        status = " status=%s" % (st if st is not None else "unknown")
    else:
        status = (" status=%s" % st) if st is not None else ""
    print("%s %s%s via=%s" % (sha, os.path.relpath(p, os.getcwd()).replace("\\", "/"), status, info.get("via")))
    if read and isinstance(st, int) and st >= 400:
        # a stored 4xx or 5xx is the origin's answer, kept as evidence of it; a 401, 403 or 429 is a walled page, and
        # lane brief rule 4 says to try every route before the field is unverified (LW7-01)
        if st in (404, 410):
            print("capture: the origin answered HTTP %d: the page is gone (lane brief rule 4: probe it, and the field is "
                  "unverified: URL answered HTTP %d on DATE)" % (st, st), file=sys.stderr)
        else:
            print("capture: the origin answered HTTP %d, a walled page, not a gone one (lane brief rule 4): try every "
                  "route before you record unverified. %s" % (st, next_route(args.url, lane, REPO, getattr(args, "provider", None))),
                  file=sys.stderr)
    return code
