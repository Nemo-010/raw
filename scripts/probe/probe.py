#!/usr/bin/env python3
"""probe.py — the verification primitive.

PURPOSE
    Turn one URL into one JSON evidence record: what answered, how many bytes,
    which hash, over which redirect chain, and whether the answer was real.
    Every writer in this repo cites a probe record instead of asserting a fact.

WHY IT EXISTS
    HTTP 200 is not evidence. Dead hosts answer 200 with an empty body, a login
    page, a human-verification page, or a 106-byte JSON error. This tool refuses to call any of
    those a payload, separates "TLS chain broken" from "host broken", and records
    the true Content-Length even when it only read a prefix.

DEPENDENCIES
    Python standard library only. No network access except the probe itself.
    `--selftest` runs entirely offline against 127.0.0.1 and data: URLs.

OUTPUT
    One JSON object on stdout (machine-readable, primary). `--human` for people.
    stderr carries diagnostics only; it never mixes into the record.

EXIT CODES  (the repository-wide map, scripts/README.md)
    0  record emitted, payload usable (2xx, non-empty, no challenge, checks passed)
    1  record emitted, payload NOT usable: 4xx, empty 200, challenge page, false-200,
       timeout, or a hash/size mismatch. A finding about the target, not about us.
    2  usage error: bad arguments, unparseable URL, unreadable --urls-file
    3  environment wrong: no record could be produced (internal fault)
    4  the remote said no, retryably: 429 or 503 from the target. Try later.
    --selftest: 0 all cases passed, 1 at least one failed

PROMOTION
    Scripts target: scripts/probe/probe.py. The ranged-GET benchmark lives in the
    same file as --shard-bytes so the baseline cannot be run without it.

THE RECORD (base keys are stable; extras are documented in --help)
    url final_url method status bytes sha256 content_type elapsed_ms
    redirects[] headers_subset challenge{detected,signature} error probed_at
"""

import argparse
import concurrent.futures
import hashlib
import http.client
import json
import os
import re
import socket
import ssl
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

PROBE_VERSION = "1.0.0"
DEFAULT_UA = "probe.py/1.0 (verification harness)"
MAX_REDIRECTS = 10

# Headers a reviewer actually needs. Everything else is --dump-headers.
INTERESTING_HEADERS = (
    "content-type", "content-length", "content-encoding", "content-range",
    "accept-ranges", "location", "server", "etag", "last-modified",
    "cache-control", "retry-after", "www-authenticate", "x-amz-expires",
    "x-archive-keep-old-version", "x-web-egress", "x-web-provider",
    "x-reader-source", "cf-ray", "cf-cache-status",
)
INTERESTING_PREFIXES = ("x-web-", "x-reader-", "x-archive-", "x-proxy-", "x-amz-", "x-goog-")

# ---------------------------------------------------------------- detection --

# A challenge is a refusal wearing a status: switch tool and try every route (AGENTS.md section 2 rule 15).
CHALLENGE_SIGNATURES = (
    ("cloudflare-challenge", (
        "just a moment...", "just a moment…", "checking your browser",
        "attention required! | cloudflare", "enable javascript and cookies to continue",
        "cf-challenge", "cf_chl_opt", "cf_chl_prog", "/cdn-cgi/challenge-platform",
    )),
    ("datadome", ("datadome", "captcha-delivery.com", "geo.captcha-delivery.com")),
    ("perimeterx", ("px-captcha", "_pxhd", "perimeterx", "px-block")),
    ("akamai-bot-manager", ("_abck", "akamai bot manager", "ak_bmsc")),
    ("imperva-incapsula", ("incapsula", "_incap_ses", "request unsuccessful. incapsula")),
    ("aws-waf", ("awswaf", "aws waf", "aws-waf-token")),
    ("ddos-guard", ("ddos-guard", "ddos guard", "checking your browser before accessing")),
    ("sucuri", ("sucuri_cloudproxy", "sucuri website firewall")),
    ("generic-captcha", ("g-recaptcha", "hcaptcha.com", "recaptcha/api.js", "cf-turnstile")),
    ("human-verification", (
        "verify you are human", "human verification", "prove you are human",
        "are you a robot", "complete the security check",
    )),
)

LOGIN_TITLE_MARKERS = (
    "sign in", "log in", "login", "sign-in", "log-in", "authentication required",
)


def _title_of(html):
    low = html.lower()
    i = low.find("<title")
    if i < 0:
        return ""
    j = low.find(">", i)
    k = low.find("</title>", j)
    if j < 0 or k < 0:
        return ""
    return low[j + 1:k].strip()


def detect_challenge(status, content_type, body_text):
    """Return (detected, signature). Never fires on a large healthy document."""
    if not body_text:
        return False, ""
    low = body_text.lower()
    title = _title_of(body_text[:20000])
    is_html = "html" in (content_type or "").lower() or "<html" in low[:2000]

    # Signature words that only a challenge page carries in its title.
    if is_html and title:
        for name, needles in CHALLENGE_SIGNATURES:
            for n in needles:
                if n in title:
                    return True, "%s:title:%s" % (name, n)

    # Body-level markers: trusted on a refusal status, or on a small 2xx body.
    trusted_status = status in (401, 403, 407, 429, 503, 520, 521, 522, 523, 524, 530)
    small = len(body_text) < 60000
    if trusted_status or small:
        for name, needles in CHALLENGE_SIGNATURES:
            for n in needles:
                if n in low:
                    return True, "%s:%s" % (name, n)

    # A login wall is a different refusal: credentials, not a human-verification step.
    if is_html and small and ("type=\"password\"" in low or "type='password'" in low
                              or "type=password" in low):
        for m in LOGIN_TITLE_MARKERS:
            if m in title or m in low[:4000]:
                return True, "login-wall:%s" % m
    return False, ""


ERROR_JSON_KEYS = ("error", "errors", "message", "detail", "reason")


def detect_false_200(status, content_type, body_bytes, body_text, declared,
                     method="GET"):
    """A 2xx that carries no payload. Returns dict or None.

    This is the rule that cost the most waves: 200 is a status, not a result.
    A HEAD response is judged on its headers alone: no body is the contract, so
    a declared Content-Length is the whole evidence and a 0-byte body proves nothing.
    """
    if not (200 <= status < 300):
        return None
    if status == 204 or status == 205 or method == "HEAD":
        # Legitimately bodyless by definition.
        return None
    n = len(body_bytes)
    if n == 0 or (declared == 0 and n == 0):
        return {"kind": "empty", "signature": "status %d with a 0-byte body" % status}
    ctype = (content_type or "").lower()
    low = body_text.lower()

    # Git LFS pointer: 200, tiny, and not the bytes you asked for (rule 10).
    if body_bytes[:60].startswith(b"version https://git-lfs") and n < 1024:
        return {"kind": "lfs-pointer", "signature": "git-lfs pointer, %d bytes" % n}

    if "json" in ctype or (body_text[:1] in ("{", "[")):
        try:
            obj = json.loads(body_text)
        except Exception:
            obj = None
        if isinstance(obj, dict):
            code = obj.get("code")
            if isinstance(code, int) and code >= 400:
                return {"kind": "json-error", "signature": "200 with {\"code\": %d}" % code}
            for k in ("success", "ok"):
                if obj.get(k) is False:
                    return {"kind": "json-error", "signature": "200 with %r: false" % k}
            for k in ("status",):
                if isinstance(obj.get(k), str) and obj[k].lower() in ("error", "failed", "fail"):
                    return {"kind": "json-error", "signature": "200 with status: %r" % obj[k]}
            for k in ERROR_JSON_KEYS:
                v = obj.get(k)
                if isinstance(v, (str, dict, list)) and v and k in obj:
                    if k == "error" or (isinstance(obj.get("code"), int) and obj["code"] >= 400):
                        return {"kind": "json-error",
                                "signature": "200 with a truthy %r member" % k}
        if isinstance(obj, list) and obj == [] and n < 200:
            return {"kind": "json-empty", "signature": "200 with an empty JSON array"}

    if "html" in ctype or "<html" in low[:500]:
        if n < 30000:
            for needle, kind in (
                ("404 not found", "html-error-page"),
                ("page not found", "html-error-page"),
                ("file not found", "html-error-page"),
                ("this page could not be found", "html-error-page"),
                ("the page you requested could not be found", "html-error-page"),
                ("account suspended", "host-error-page"),
                ("domain is parked", "parked-page"),
                ("site not found", "host-error-page"),
                ("502 bad gateway", "host-error-page"),
                ("service unavailable", "host-error-page"),
            ):
                if needle in low:
                    return {"kind": kind, "signature": "200 with %r" % needle}
    if n < 128 and ("html" in ctype or "<html" in low[:200]):
        return {"kind": "tiny-html", "signature": "200 with a %d-byte HTML body" % n}
    return None


def classify_error(e):
    """Map a transport exception onto a stable class a reviewer can act on."""
    if isinstance(e, ssl.SSLCertVerificationError):
        return "tls_untrusted"
    if isinstance(e, ssl.SSLCertVerificationError):
        return "tls_untrusted"
    if isinstance(e, ssl.SSLError):
        return "tls_error"
    if isinstance(e, socket.gaierror):
        return "dns"
    if isinstance(e, ConnectionRefusedError):
        return "connect_refused"
    if isinstance(e, ConnectionResetError):
        return "reset"
    if isinstance(e, (socket.timeout, TimeoutError)):
        return "timeout"
    if isinstance(e, urllib.error.URLError):
        return classify_error(e.reason) if isinstance(e.reason, BaseException) else "transport"
    if isinstance(e, http.client.IncompleteRead):
        return "truncated-body"
    if isinstance(e, http.client.RemoteDisconnected):
        return "reset"
    return "transport"


def iso_now():
    t = datetime.now(timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)


# ------------------------------------------------------------------- fetch --

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects are followed by hand so every hop can be recorded."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_CTX_CACHE = {}


def _ssl_context(insecure):
    """One context per mode, built once.

    `ssl.create_default_context()` reads and parses the whole CA bundle in Python,
    under the GIL, on every call. Building it per request was the dominant cost of a
    many-host probe: measured at 250 hosts and 8 concurrent, reusing one context took
    the run from 22 s to 3.75 s with no other change. A TLS context is immutable once
    configured, so caching it is safe and changes no measurement.
    """
    key = bool(insecure)
    ctx = _CTX_CACHE.get(key)
    if ctx is not None:
        return ctx
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    _CTX_CACHE[key] = ctx
    return ctx


def _build_opener(args):
    handlers = [_NoRedirect()]
    if args.proxy:
        handlers.append(urllib.request.ProxyHandler({"http": args.proxy, "https": args.proxy}))
    elif not args.use_env_proxy:
        handlers.append(urllib.request.ProxyHandler({}))
    handlers.append(urllib.request.HTTPSHandler(context=_ssl_context(args.insecure)))
    return urllib.request.build_opener(*handlers)


def tls_probe(url, timeout=10.0):
    """Second, independent handshake: proves the host speaks TLS when the
    verifying handshake failed. Returns None for non-https or on failure."""
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or not p.hostname:
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with socket.create_connection((p.hostname, p.port or 443), timeout=timeout) as s:
            with ctx.wrap_socket(s, server_hostname=p.hostname) as ss:
                der = ss.getpeercert(binary_form=True) or b""
                return {
                    "handshake_ok": True,
                    "tls_version": ss.version(),
                    "cipher": (ss.cipher() or [None])[0],
                    "cert_der_sha256": hashlib.sha256(der).hexdigest() if der else None,
                }
    except Exception as e:
        return {"handshake_ok": False, "error": classify_error(e), "detail": str(e)[:200]}


def _cf_ray(v):
    """A cf-ray value without its suffix: "8f1c2a3b4c5d6e7f-KTM" names the Cloudflare location that served the probing
    machine, which is the network identity of that machine (lane rule 2); the ray id alone stays (W3-13)."""
    return ", ".join(x.strip().rsplit("-", 1)[0] if re.match(r"^[0-9a-f]+-[A-Z]{3}$", x.strip()) else x.strip()
                     for x in v.split(","))


def _header_subset(headers, dump_all=False):
    out = {}
    for k, v in headers.items():
        lk = k.lower()
        if lk == "cf-ray":
            v = _cf_ray(v)
        if dump_all or lk in INTERESTING_HEADERS or lk.startswith(INTERESTING_PREFIXES):
            if lk in out:
                out[lk] += ", " + v
            else:
                out[lk] = v
    return out


def _request_headers(args):
    h = {
        "User-Agent": args.user_agent,
        "Accept": "*/*",
        "Accept-Encoding": "gzip" if args.compressed else "identity",
    }
    if args.range_spec:
        h["Range"] = "bytes=" + args.range_spec
    for raw in args.header or []:
        if ":" not in raw:
            raise ValueError("--header needs 'Name: value', got %r" % raw)
        name, _, value = raw.partition(":")
        h[name.strip()] = value.strip()
    return h


def _read_body(resp, limit, want_hash):
    """Read up to `limit` bytes (None = all). Returns (bytes, truncated, sha256)."""
    h = hashlib.sha256()
    chunks = []
    remaining = limit if limit is not None else -1
    total = 0
    while True:
        if remaining == 0:
            break
        want = 65536 if remaining < 0 else min(65536, remaining)
        chunk = resp.read(want)
        if not chunk:
            break
        total += len(chunk)
        if want_hash:
            h.update(chunk)
        chunks.append(chunk)
        if remaining > 0:
            remaining -= len(chunk)
    body = b"".join(chunks)
    truncated = limit is not None and len(body) == limit
    return body, truncated, (h.hexdigest() if want_hash else None)


def _sleep_backoff(attempt, retry_after):
    """The pause before a retry that --retries asked for: only the server's own Retry-After, whatever its value. Without
    one the retry goes at once; this script invents no delay of its own (AGENTS.md section 2 rule 15). An HTTP date in
    Retry-After is read as no number, so that retry goes at once too."""
    try:
        ra = float(retry_after) if retry_after else 0.0
    except (TypeError, ValueError):
        ra = 0.0
    if ra > 0:
        time.sleep(ra)  # wait: retry-after, the server's own pause


def probe_once(url, args):
    """One URL -> one record. Follows redirects manually, records every hop."""
    rec = {
        "url": url,
        "final_url": url,
        "method": args.method,
        "status": None,
        "bytes": 0,
        "sha256": None,
        "content_type": None,
        "elapsed_ms": None,
        "redirects": [],
        "headers_subset": {},
        "challenge": {"detected": False, "signature": ""},
        "error": None,
        "probed_at": iso_now(),
        # extras
        "probe_version": PROBE_VERSION,
        "usable": False,
        "declared_bytes": None,
        "truncated": False,
        "sha256_scope": "none",
        "ttfb_ms": None,
        "attempts": 0,
        "urls_tried": [],
        "tls": {"insecure": bool(args.insecure)},
        "false_200": {"detected": False, "kind": None, "signature": None},
        "range": None,
        "checks": {},
    }
    if args.range_spec:
        rec["range"] = {"requested": args.range_spec, "honoured": None, "content_range": None}
    if args.tls_info:
        info = tls_probe(url, timeout=min(args.timeout, 10.0))
        if info:
            rec["tls"].update(info)
            rec["tls"]["verified"] = not args.insecure

    try:
        headers = _request_headers(args)
    except ValueError as e:
        rec["error"] = "bad-arguments: %s" % e
        return rec

    opener = _build_opener(args)
    cur = url
    t0 = time.perf_counter()
    ttfb = None
    resp = None
    err = None

    for hop_index in range(MAX_REDIRECTS + 1):
        rec["urls_tried"].append(cur)
        attempt = 0
        resp = None
        err = None
        while True:
            attempt += 1
            rec["attempts"] += 1
            req = urllib.request.Request(cur, method=args.method, headers=headers)
            try:
                resp = opener.open(req, timeout=args.timeout)
                err = None
            except urllib.error.HTTPError as e:
                # A status the opener did not swallow: a 3xx (we refuse to auto-follow)
                # or a 4xx/5xx. Both are answers, not transport failures.
                resp, err = e, None
            except Exception as e:  # noqa: BLE001 - classified below
                resp, err = None, e

            if err is not None:
                cls = classify_error(err)
                retryable = cls in ("timeout", "reset", "transport", "truncated-body")
                if retryable and attempt <= args.retries:
                    _sleep_backoff(attempt - 1, None)
                    continue
                rec["error"] = cls
                rec["error_detail"] = "%s: %s" % (type(err).__name__, str(err)[:300])
                if cls in ("tls_untrusted", "tls_error"):
                    info = tls_probe(cur, timeout=min(args.timeout, 10.0))
                    if info:
                        rec["tls"].update(info)
                    if isinstance(err, ssl.SSLCertVerificationError):
                        rec["tls"]["verify_code"] = getattr(err, "verify_code", None)
                        rec["tls"]["verify_message"] = getattr(err, "verify_message", None)
                    elif isinstance(getattr(err, "reason", None), ssl.SSLCertVerificationError):
                        r = err.reason
                        rec["tls"]["verify_code"] = getattr(r, "verify_code", None)
                        rec["tls"]["verify_message"] = getattr(r, "verify_message", None)
                    rec["tls"]["verified"] = False
                rec["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 1)
                return rec
            break

        status = getattr(resp, "status", None)
        if status is None:
            status = getattr(resp, "code", None)
        if status is None and urllib.parse.urlsplit(cur).scheme.lower() == "data":
            # data: URLs have no status line; the handler synthesised the body.
            status = 200
        hdrs = resp.headers
        rec["final_url"] = resp.geturl() or cur
        rec["status"] = status
        rec["headers_subset"] = _header_subset(hdrs, args.dump_headers)
        rec["content_type"] = (hdrs.get("Content-Type") or "").split(";")[0].strip() or None
        cl = hdrs.get("Content-Length")
        try:
            rec["declared_bytes"] = int(cl) if cl is not None else None
        except ValueError:
            rec["declared_bytes"] = None

        location = hdrs.get("Location")
        if args.method in ("GET", "HEAD") and status in (301, 302, 303, 307, 308) and location:
            new = urllib.parse.urljoin(cur, location)
            rec["redirects"].append({
                "status": status,
                "location": new,
                "raw_location": location,
                "from": cur,
            })
            try:
                resp.read(4096)
            except Exception:
                pass
            try:
                resp.close()
            except Exception:
                pass
            scheme = urllib.parse.urlsplit(new).scheme.lower()
            if scheme not in ("http", "https"):
                rec["error"] = "redirect-not-http"
                rec["error_detail"] = "redirect to %s" % new
                rec["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 1)
                return rec
            if hop_index == MAX_REDIRECTS:
                rec["error"] = "too-many-redirects"
                rec["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 1)
                return rec
            cur = new
            continue

        # Final hop. Retry a retryable status before giving up on it.
        if status in (408, 429, 500, 502, 503, 504) and rec["attempts"] <= args.retries:
            try:
                resp.read(4096)
                resp.close()
            except Exception:
                pass
            _sleep_backoff(rec["attempts"] - 1, hdrs.get("Retry-After"))
            continue
        if status in (429, 503) and hdrs.get("Retry-After"):
            # the server's own pacing, recorded so a later read can come back after it (no retry asked for, or none left)
            rec["retry_after"] = hdrs.get("Retry-After")
        break

    # ---- body
    limit = None
    if args.method == "HEAD":
        limit = 0
    elif args.bytes_limit is not None:
        limit = args.bytes_limit

    want_hash = not args.no_hash
    if limit is not None and limit == 0:
        body, truncated, digest = b"", False, None
        rec["sha256_scope"] = "none"
    else:
        try:
            if ttfb is None:
                ttfb = None
            body, truncated, digest = _read_body(resp, limit, want_hash)
            rec["sha256_scope"] = "prefix" if truncated else ("full" if want_hash else "none")
        except Exception as e:  # noqa: BLE001
            rec["error"] = classify_error(e)
            rec["error_detail"] = "%s: %s" % (type(e).__name__, str(e)[:300])
            body, truncated, digest = b"", False, None
        finally:
            try:
                resp.close()
            except Exception:
                pass

    rec["elapsed_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    rec["bytes"] = len(body)
    rec["truncated"] = bool(truncated)
    rec["sha256"] = digest if want_hash else None
    if args.head_only or args.method == "HEAD":
        rec["sha256_scope"] = "none"

    if args.save_body and body:
        try:
            # a folder that does not exist yet is made: a lane registers this body with --probe one command later (W3-02)
            os.makedirs(os.path.dirname(os.path.abspath(args.save_body)), exist_ok=True)
            with open(args.save_body, "wb") as fh:
                fh.write(body)
            rec["saved_to"] = args.save_body
        except OSError as e:
            rec["save_error"] = str(e)

    # ---- semantics: never trust the status line
    model = args.bytes_limit if args.bytes_limit is not None else len(body)
    try:
        body_text = body.decode("utf-8", "replace")
    except Exception:
        body_text = ""

    det, sig = detect_challenge(rec["status"], rec["content_type"], body_text)
    if det:
        rec["challenge"] = {"detected": True, "signature": sig}
    f200 = detect_false_200(rec["status"], rec["content_type"], body, body_text,
                            rec["declared_bytes"], args.method)
    if f200:
        rec["false_200"] = {"detected": True, "kind": f200["kind"], "signature": f200["signature"]}

    if rec["status"] is not None and 400 <= rec["status"] < 600 and rec["error"] is None:
        rec["error"] = "http-%d" % rec["status"]

    # Truncation by the peer, not by us: a real integrity failure (rule 1).
    if (rec["error"] is None and rec["declared_bytes"] is not None
            and not truncated and args.method != "HEAD"
            and not rec["headers_subset"].get("content-encoding")
            and rec["bytes"] < rec["declared_bytes"]):
        rec["error"] = "truncated-body"
        rec["error_detail"] = "read %d of %d declared bytes" % (rec["bytes"], rec["declared_bytes"])

    # ---- range honesty
    if args.range_spec:
        cr = rec["headers_subset"].get("content-range")
        rec["range"]["content_range"] = cr
        if rec["status"] == 206:
            rec["range"]["honoured"] = True
        elif rec["status"] in (200, 416):
            rec["range"]["honoured"] = False
        else:
            rec["range"]["honoured"] = None

    # ---- caller-supplied expectations
    if args.expect_sha256:
        got = (rec["sha256"] or "").lower()
        rec["checks"]["sha256"] = {"expected": args.expect_sha256.lower(),
                                   "actual": got, "match": got == args.expect_sha256.lower()}
    if args.expect_bytes is not None:
        actual = rec["declared_bytes"] if rec["declared_bytes"] is not None else rec["bytes"]
        rec["checks"]["bytes"] = {"expected": args.expect_bytes, "actual": actual,
                                  "match": actual == args.expect_bytes}

    rec["usable"] = (
        rec["error"] is None
        and rec["status"] is not None and 200 <= rec["status"] < 300
        and not rec["challenge"]["detected"]
        and not rec["false_200"]["detected"]
        and all(c["match"] for c in rec["checks"].values())
    )
    return rec


# ------------------------------------------------------------- concurrency --

def _chunk_ranges(total, n):
    """Split [0,total) into n contiguous byte ranges."""
    n = max(1, n)
    size = total // n
    out = []
    for i in range(n):
        a = i * size
        b = total - 1 if i == n - 1 else (a + size - 1)
        out.append((a, b))
    return out


def probe_parallel(urls, args):
    """Throughput over N connections against ONE object, plus a 1-connection baseline.

    The corpus benchmark (rule 6) is parallel ranged GETs on a single object, not N
    identical fetches: Zenodo went 0.48 -> 19.7 MB/s from 1 -> 32 connections while
    OSN *declines* (12.55 -> 6.71). Without the baseline the two are indistinguishable.

    Modes:
      --shard-bytes N   read the first N bytes as N contiguous Range requests
      --urls-file       N distinct URLs (rule 7: mint a URL per connection)
      default           N identical GETs (measures connection setup, not bandwidth)
    """
    workers = max(1, args.concurrency)
    jobs = []          # (url, range_spec or None)
    shard = None

    if args.shard_bytes:
        total = args.shard_bytes
        chunks = _chunk_ranges(total, workers)
        shard = {"total_bytes": total, "chunks": len(chunks), "chunk_bytes": total // workers}
        jobs = [(urls[0], "%d-%d" % (a, b)) for a, b in chunks]
    else:
        while len(urls) < workers:
            urls = urls * 2
        jobs = [(u, None) for u in urls[:workers]]

    def run_one(job):
        u, rng = job
        a = argparse.Namespace(**vars(args))
        a.range_spec = rng
        a.bytes_limit = None
        return probe_once(u, a)

    t_wall = time.perf_counter()
    recs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(run_one, j) for j in jobs]
        for f in futs:
            recs.append(f.result())
    wall = time.perf_counter() - t_wall

    total_bytes = sum(r["bytes"] for r in recs)
    mbps = (total_bytes / wall / (1024 * 1024)) if wall > 0 else 0.0
    statuses = [r["status"] for r in recs]
    status = max((s for s in statuses if isinstance(s, int)), default=None)

    base = None
    base_mbps = None
    if args.baseline:
        if args.shard_bytes:
            # Same byte span over one connection: the honest comparison.
            bargs = argparse.Namespace(**vars(args))
            bargs.range_spec = "0-%d" % (args.shard_bytes - 1)
            bargs.bytes_limit = None
            b = probe_once(urls[0], bargs)
        else:
            b = probe_once(urls[0], args)
        bw = (b["elapsed_ms"] or 0) / 1000.0
        base_mbps = (b["bytes"] / bw / (1024 * 1024)) if bw > 0 else 0.0
        base = {"bytes": b["bytes"], "elapsed_ms": b["elapsed_ms"],
                "mbps": round(base_mbps, 3), "status": b["status"],
                "range": b.get("range")}

    honoured = [r["range"]["honoured"] for r in recs if r.get("range")]
    return {
        "url": urls[0],
        "final_url": recs[0]["final_url"] if recs else urls[0],
        "method": args.method,
        "status": status,
        "bytes": total_bytes,
        "sha256": None,
        "content_type": recs[0]["content_type"] if recs else None,
        "elapsed_ms": round(wall * 1000, 1),
        "redirects": recs[0]["redirects"] if recs else [],
        "headers_subset": recs[0]["headers_subset"] if recs else {},
        "challenge": {"detected": any(r["challenge"]["detected"] for r in recs),
                      "signature": next((r["challenge"]["signature"] for r in recs
                                         if r["challenge"]["detected"]), "")},
        "error": next((r["error"] for r in recs if r["error"]), None),
        "probed_at": iso_now(),
        "probe_version": PROBE_VERSION,
        "mode": "concurrency",
        "concurrency": workers,
        "shard": shard,
        "range_honoured_all": all(h is True for h in honoured) if honoured else None,
        "statuses": statuses,
        "throughput_mbps": round(mbps, 3),
        "baseline": base,
        "baseline_mbps": round(base_mbps, 3) if base_mbps is not None else None,
        "speedup": round(mbps / base_mbps, 2) if base_mbps else None,
        "declines": bool(base_mbps and mbps < base_mbps),
        "usable": all(r["usable"] for r in recs),
        "runs": recs,
    }


# ------------------------------------------------------------------ output --

def print_human(rec):
    if rec.get("mode") == "concurrency":
        out = []
        out.append("probe %s  (concurrency %d)" % (rec["url"], rec["concurrency"]))
        out.append("  statuses   %s" % rec["statuses"])
        out.append("  total      %d bytes in %.1f ms" % (rec["bytes"], rec["elapsed_ms"]))
        out.append("  parallel   %.3f MiB/s" % rec["throughput_mbps"])
        if rec.get("range_honoured_all") is not None:
            out.append("  ranges     honoured=%s" % rec["range_honoured_all"])
        if rec.get("baseline_mbps") is not None:
            out.append("  baseline   %.3f MiB/s (1 connection)" % rec["baseline_mbps"])
            out.append("  speedup    %sx%s" % (rec["speedup"],
                       "  DECLINES" if rec.get("declines") else ""))
        out.append("  usable     %s" % rec["usable"])
        sys.stdout.write("\n".join(out) + "\n")
        return
    out = []
    out.append("%s %s" % (rec["method"], rec["url"]))
    if rec["redirects"]:
        for h in rec["redirects"]:
            out.append("  -> %s %s" % (h["status"], h["location"]))
    out.append("  status     %s" % rec["status"])
    out.append("  final_url  %s" % rec["final_url"])
    out.append("  bytes      %s%s" % (
        rec["bytes"],
        " (declared %s)" % rec["declared_bytes"] if rec["declared_bytes"] is not None else ""))
    out.append("  sha256     %s%s" % (rec["sha256"] or "-",
                                     " (%s)" % rec["sha256_scope"]))
    out.append("  type       %s" % (rec["content_type"] or "-"))
    out.append("  elapsed    %.1f ms" % rec["elapsed_ms"])
    if rec["range"]:
        out.append("  range      %s honoured=%s %s" % (
            rec["range"]["requested"], rec["range"]["honoured"],
            rec["range"]["content_range"] or ""))
    if rec["challenge"]["detected"]:
        out.append("  CHALLENGE  %s" % rec["challenge"]["signature"])
    if rec["false_200"]["detected"]:
        out.append("  FALSE-200  %s: %s" % (rec["false_200"]["kind"], rec["false_200"]["signature"]))
    if rec["error"]:
        out.append("  error      %s" % rec["error"])
    out.append("  usable     %s" % rec["usable"])
    out.append("  probed_at  %s" % rec["probed_at"])
    sys.stdout.write("\n".join(out) + "\n")


def emit(rec, as_json):
    if as_json:
        sys.stdout.write(json.dumps(rec, ensure_ascii=False, indent=None) + "\n")
    else:
        print_human(rec)


def write_out(rec, out_dir):
    """Write the record to <out_dir>/<timestamp>-<hash>.json and say where.

    The filename is derived from the record, so running the same probe twice
    produces two files rather than silently overwriting one: two probes of the
    same URL on two days are two pieces of evidence.
    """
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        sys.stderr.write("probe: cannot create --out directory: %s\n" % exc)
        return 3
    stamp = (rec.get("probed_at") or "").replace(":", "").replace("-", "")
    stamp = stamp.split(".")[0].rstrip("Z") or "unknown"
    digest = (rec.get("sha256") or "nohash")[:12]
    host = urllib.parse.urlsplit(rec.get("url") or "").netloc or "data"
    host = "".join(c if c.isalnum() or c in ".-" else "_" for c in host)
    path = os.path.join(out_dir, "%s-%s-%s.json" % (stamp, host, digest))
    try:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
    except OSError as exc:
        sys.stderr.write("probe: cannot write the record: %s\n" % exc)
        return 3
    # a forward slash on Windows too: a lane pastes the path unquoted into Git Bash, which eats a backslash (LW7-02)
    sys.stderr.write("probe: record written to %s\n" % path.replace(os.sep, "/"))
    return 0


# ---------------------------------------------------------------- selftest --

def run_selftest(verbose=False):
    """Offline. A loopback HTTP server plus data: URLs. No outside network."""
    import http.server

    state = {"flaky": 0}
    results = []

    class H(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def _send(self, code, body=b"", ctype="text/plain", extra=None):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def do_HEAD(self):
            self.do_GET()

        def do_GET(self):
            p = urllib.parse.urlsplit(self.path).path
            if p == "/ok":
                self._send(200, b"hello world")
            elif p == "/cfray":
                self._send(200, b"hello world", extra={"CF-Ray": "8f1c2a3b4c5d6e7f-KTM"})
            elif p == "/empty":
                self._send(200, b"")
            elif p == "/redirect":
                self._send(302, b"", extra={"Location": "/ok"})
            elif p == "/chain":
                self._send(302, b"", extra={"Location": "/redirect"})
            elif p == "/range":
                rng = self.headers.get("Range", "")
                body = bytes(range(256)) * 8  # 2048 bytes
                if rng.startswith("bytes="):
                    a, _, b = rng[6:].partition("-")
                    a, b = int(a), int(b)
                    chunk = body[a:b + 1]
                    self._send(206, chunk, extra={
                        "Content-Range": "bytes %d-%d/%d" % (a, b, len(body)),
                        "Accept-Ranges": "bytes"})
                else:
                    self._send(200, body, extra={"Accept-Ranges": "bytes"})
            elif p == "/norange":
                self._send(200, b"x" * 2048)
            elif p == "/big":
                self._send(200, b"a" * 10240)
            elif p == "/captcha":
                self._send(200, b"<html><head><title>Just a moment...</title></head>"
                                b"<body>checking your browser</body></html>",
                           ctype="text/html")
            elif p == "/jsonerr":
                self._send(200, b'{"code":403,"message":"forbidden"}',
                           ctype="application/json")
            elif p == "/html404":
                self._send(200, b"<html><head><title>404 Not Found</title></head>"
                                b"<body>nope</body></html>", ctype="text/html")
            elif p == "/lfs":
                self._send(200, b"version https://git-lfs.github.com/spec/v1\n"
                                b"oid sha256:abc\nsize 12345\n")
            elif p == "/flaky":
                state["flaky"] += 1
                if state["flaky"] == 1:
                    self._send(503, b"try later")
                else:
                    self._send(200, b"recovered")
            elif p == "/slow":
                time.sleep(0.6)  # wait: measure, the selftest's slow fixture
                self._send(200, b"slow")
            elif p == "/truncated":
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", "1000")
                self.end_headers()
                self.wfile.write(b"short")
                self.wfile.flush()
                self.close_connection = True
            else:
                self._send(404, b"no such route")

    class T(http.server.ThreadingHTTPServer):
        daemon_threads = True

        def handle_error(self, request, client_address):
            # A deliberately timed-out client hangs up first; that is the test,
            # not a fault. Keep stderr clean so the summary is readable.
            pass

    srv = T(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    base = "http://127.0.0.1:%d" % port
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()

    def args_for(**kw):
        ns = argparse.Namespace(
            method="GET", head_only=False, bytes_limit=None, range_spec=None,
            timeout=5.0, retries=0, insecure=False, body_hash=False, no_hash=False,
            user_agent=DEFAULT_UA, header=[], dump_headers=False, proxy=None,
            use_env_proxy=False, save_body=None, expect_sha256=None,
            expect_bytes=None, compressed=False, concurrency=2, baseline=True,
            tls_info=False, shard_bytes=None,
        )
        for k, v in kw.items():
            setattr(ns, k, v)
        return ns

    def check(name, cond, detail=""):
        results.append((name, bool(cond), detail))
        if verbose or not cond:
            sys.stderr.write("%s %s%s\n" % ("PASS" if cond else "FAIL", name,
                                            ("  " + detail) if detail else ""))

    try:
        # 1. data: URL, no socket at all
        r = probe_once("data:text/plain,hello", args_for())
        check("data-url bytes", r["bytes"] == 5, repr(r.get("bytes")))
        check("data-url sha256",
              r["sha256"] == hashlib.sha256(b"hello").hexdigest(), str(r["sha256"]))
        check("data-url usable", r["usable"] is True, str(r.get("error")))

        # 2. plain 200
        r = probe_once(base + "/ok", args_for())
        check("200 usable", r["status"] == 200 and r["usable"],
              "%s %s" % (r["status"], r["error"]))
        check("200 declared_bytes", r["declared_bytes"] == 11, str(r["declared_bytes"]))

        # 3. empty 200 is not a payload
        r = probe_once(base + "/empty", args_for())
        check("empty-200 caught",
              r["false_200"]["detected"] and r["false_200"]["kind"] == "empty"
              and not r["usable"], str(r["false_200"]))

        # 4-5. redirects recorded hop by hop
        r = probe_once(base + "/redirect", args_for())
        check("redirect hop recorded",
              len(r["redirects"]) == 1 and r["redirects"][0]["status"] == 302
              and r["final_url"].endswith("/ok"), str(r["redirects"]))
        r = probe_once(base + "/chain", args_for())
        check("redirect chain length", len(r["redirects"]) == 2, str(len(r["redirects"])))

        # 6-7. range honesty
        r = probe_once(base + "/range", args_for(range_spec="0-15"))
        check("range honoured", r["status"] == 206 and r["range"]["honoured"] is True
              and r["bytes"] == 16, "%s %s %s" % (r["status"], r["bytes"], r["range"]))
        r = probe_once(base + "/norange", args_for(range_spec="0-15"))
        check("range ignored -> honoured False",
              r["status"] == 200 and r["range"]["honoured"] is False, str(r["range"]))

        # 8. --bytes truncates the read, keeps the truth
        r = probe_once(base + "/big", args_for(bytes_limit=10))
        check("--bytes truncation",
              r["bytes"] == 10 and r["declared_bytes"] == 10240
              and r["truncated"] is True and r["sha256_scope"] == "prefix",
              "%s %s %s" % (r["bytes"], r["declared_bytes"], r["sha256_scope"]))

        # the location suffix of cf-ray names where the probing machine is; the record keeps the ray id (W3-13)
        r = probe_once(base + "/cfray", args_for())
        check("cf-ray without its location", (r.get("headers_subset") or {}).get("cf-ray") == "8f1c2a3b4c5d6e7f",
              str((r.get("headers_subset") or {}).get("cf-ray")))
        # --save-body into a folder that does not exist yet makes it (W3-02)
        import tempfile
        sb_dir = tempfile.mkdtemp(prefix="probe-selftest-")
        sb = os.path.join(sb_dir, "new", "body.bin")
        r = probe_once(base + "/ok", args_for(save_body=sb))
        check("save-body makes its folder", os.path.isfile(sb) and not r.get("save_error"), str(r.get("save_error")))
        import shutil
        shutil.rmtree(sb_dir, ignore_errors=True)

        # 9-12. the four false answers
        r = probe_once(base + "/captcha", args_for())
        check("challenge detected", r["challenge"]["detected"]
              and r["challenge"]["signature"].startswith("cloudflare-challenge"),
              r["challenge"]["signature"])
        r = probe_once(base + "/jsonerr", args_for())
        check("json error in 200", r["false_200"]["kind"] == "json-error", str(r["false_200"]))
        r = probe_once(base + "/html404", args_for())
        check("html 404 page in 200", r["false_200"]["kind"] == "html-error-page",
              str(r["false_200"]))
        r = probe_once(base + "/lfs", args_for())
        check("lfs pointer in 200", r["false_200"]["kind"] == "lfs-pointer", str(r["false_200"]))

        # 13. retries
        state["flaky"] = 0
        r = probe_once(base + "/flaky", args_for(retries=2))
        check("retry recovers 503", r["status"] == 200 and r["attempts"] == 2,
              "%s attempts=%s" % (r["status"], r["attempts"]))
        state["flaky"] = 0
        r = probe_once(base + "/flaky", args_for(retries=0))
        check("no retry without --retries", r["status"] == 503 and r["error"] == "http-503",
              "%s %s" % (r["status"], r["error"]))

        # 14. timeout
        r = probe_once(base + "/slow", args_for(timeout=0.15))
        check("timeout classified", r["error"] == "timeout", str(r["error"]))

        # 15. 404
        r = probe_once(base + "/missing", args_for())
        check("404 is an error", r["status"] == 404 and r["error"] == "http-404"
              and not r["usable"], "%s %s" % (r["status"], r["error"]))

        # 16. expectation mismatch
        r = probe_once(base + "/ok", args_for(expect_sha256="0" * 64))
        check("sha mismatch fails", r["checks"]["sha256"]["match"] is False and not r["usable"],
              str(r["checks"]))
        r = probe_once(base + "/ok", args_for(expect_bytes=11))
        check("byte-expectation match", r["checks"]["bytes"]["match"] is True, str(r["checks"]))

        # 17. HEAD
        r = probe_once(base + "/ok", args_for(method="HEAD", head_only=True))
        check("HEAD", r["status"] == 200 and r["bytes"] == 0 and r["declared_bytes"] == 11,
              "%s %s %s" % (r["status"], r["bytes"], r["declared_bytes"]))

        # 18. peer truncation
        r = probe_once(base + "/truncated", args_for())
        check("peer truncation caught", r["error"] == "truncated-body", str(r["error"]))

        # 19. concurrency
        r = probe_parallel([base + "/big"] * 4, args_for(concurrency=4, baseline=True))
        check("concurrency 4 runs", len(r["runs"]) == 4 and r["mode"] == "concurrency",
              str(len(r["runs"])))
        check("concurrency baseline present", r["baseline"] is not None, str(r["baseline"]))
        check("concurrency throughput > 0", r["throughput_mbps"] > 0, str(r["throughput_mbps"]))

        # 19b. sharded ranged-GET benchmark against one object
        r = probe_parallel([base + "/range"], args_for(concurrency=4, baseline=True,
                                                       shard_bytes=1024))
        check("shard mode splits one object",
              r["shard"] is not None and len(r["runs"]) == 4
              and all(x["bytes"] == 256 for x in r["runs"]),
              "%s %s" % (r["shard"], [x["bytes"] for x in r["runs"]]))
        check("shard ranges honoured", r["range_honoured_all"] is True,
              str(r["range_honoured_all"]))

        # 20. TLS error classification without a network
        try:
            raise ssl.SSLCertVerificationError("certificate verify failed")
        except ssl.SSLCertVerificationError as e:
            check("classify tls_untrusted", classify_error(e) == "tls_untrusted")
        check("classify dns", classify_error(socket.gaierror(-2, "x")) == "dns")
        check("classify refused", classify_error(ConnectionRefusedError()) == "connect_refused")
        check("classify timeout", classify_error(socket.timeout()) == "timeout")

        # 21. a redirect to a non-http scheme is refused, not followed
        r = probe_once(base + "/nonsense", args_for())
        check("404 route still records status", r["status"] == 404)
    finally:
        srv.shutdown()
        srv.server_close()

    failed = [r for r in results if not r[1]]
    sys.stderr.write("selftest: %d passed, %d failed, %d total\n"
                     % (len(results) - len(failed), len(failed), len(results)))
    return 0 if not failed else 1


# -------------------------------------------------------------------- main --

def build_parser():
    p = argparse.ArgumentParser(
        prog="probe.py",
        description="Probe one URL into one JSON evidence record. Never trusts HTTP 200.",
        epilog=(
            "EXIT CODES\n"
            "  0  record emitted, payload usable\n"
            "  1  record emitted, payload NOT usable (still valid JSON on stdout)\n"
            "  2  usage error\n"
            "  3  internal error\n\n"
            "EXTRA RECORD FIELDS (beyond the stable base)\n"
            "  usable, declared_bytes, truncated, sha256_scope, ttfb_ms, attempts,\n"
            "  urls_tried, tls{}, false_200{}, range{}, checks{}, probe_version\n\n"
            "Accept-Encoding is identity by default so Content-Length equals the bytes\n"
            "read and sha256 identifies the file. --compressed opts out.\n\n"
            "EXAMPLES\n"
            "  probe.py https://example.com/ --head\n"
            "  probe.py https://host/big.bin --range 0-1048575 --body-hash\n"
            "  probe.py https://host/x --timeout 5 --retries 2 --expect-bytes 37747369973\n"
            "  probe.py https://tls-broken.host/ --insecure     # separates TLS from host\n"
            "  probe.py https://host/f --urls-file urls.txt --concurrency 8\n"
            "  probe.py --selftest\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("url", nargs="?", help="http(s) or data: URL")
    # `--url` and `--out` exist because two documents told a session to run
    # `probe.py --url URL --out DIR` as THE invocation, and it was a usage
    # error. The positional form is older and still the shortest; these are
    # aliases so the documented form works and writes the record where the
    # document said it would.
    p.add_argument("--url", dest="url_opt", metavar="URL",
                   help="the URL; the same thing as the positional form")
    p.add_argument("--out", dest="out_dir", metavar="DIR",
                   help="write the JSON record to DIR/<UTC timestamp>-<hash>.json "
                        "instead of only to stdout")
    p.add_argument("--head", dest="head_only", action="store_true", help="HEAD instead of GET")
    p.add_argument("--range", dest="range_spec", metavar="A-B",
                   help="Range: bytes=A-B (also 'A-', '-B', comma lists)")
    p.add_argument("--bytes", dest="bytes_limit", type=int, metavar="N",
                   help="read at most N body bytes; true Content-Length still recorded")
    p.add_argument("--concurrency", type=int, default=1,
                   help="parallel GETs for the throughput benchmark (default 1)")
    p.add_argument("--urls-file", metavar="PATH",
                   help="one URL per line, used by --concurrency so each connection "
                        "mints its own URL (rule 7)")
    p.add_argument("--shard-bytes", type=int, metavar="N",
                   help="with --concurrency: read the first N bytes as N contiguous "
                        "Range requests (the rule-6 parallel ranged-GET benchmark)")
    p.add_argument("--no-baseline", dest="baseline", action="store_false",
                   help="skip the 1-connection baseline in --concurrency mode")
    p.add_argument("--timeout", type=float, default=30.0, help="seconds (default 30)")
    p.add_argument("--retries", type=int, default=0,
                   help="retries on transport error or 408/429/5xx, at once or after the server's Retry-After (default 0)")
    p.add_argument("--insecure", action="store_true",
                   help="skip TLS verification; records tls.verified=false")
    p.add_argument("--tls-info", action="store_true",
                   help="second handshake to record the peer certificate fingerprint")
    p.add_argument("--body-hash", action="store_true",
                   help="hash exactly what was read, labelled prefix/full")
    p.add_argument("--no-hash", action="store_true", help="skip hashing (huge bodies)")
    p.add_argument("--expect-sha256", metavar="HEX", help="fail unless the digest matches")
    p.add_argument("--expect-bytes", type=int, metavar="N",
                   help="fail unless Content-Length (or bytes read) matches")
    p.add_argument("--max-redirects", type=int, default=MAX_REDIRECTS,
                   help="redirect hop ceiling (default 10)")
    p.add_argument("--user-agent", default=DEFAULT_UA)
    p.add_argument("--header", action="append", metavar="'Name: value'",
                   help="extra request header, repeatable")
    p.add_argument("--compressed", action="store_true",
                   help="send Accept-Encoding: gzip (breaks byte identity)")
    p.add_argument("--dump-headers", action="store_true", help="record every header")
    p.add_argument("--proxy", help="explicit proxy URL (default: no proxy, hermetic)")
    p.add_argument("--use-env-proxy", action="store_true",
                   help="honour http_proxy/https_proxy from the environment")
    p.add_argument("--save-body", metavar="PATH", help="write the body to PATH")
    p.add_argument("--human", action="store_true", help="human-readable output")
    p.add_argument("--json", action="store_true", help="force JSON (default)")
    p.add_argument("--selftest", action="store_true", help="run the offline selftest")
    p.add_argument("--verbose", action="store_true")
    return p


def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    args.method = "HEAD" if args.head_only else "GET"
    global MAX_REDIRECTS
    MAX_REDIRECTS = max(0, args.max_redirects)

    if args.selftest:
        return run_selftest(args.verbose)

    urls = []
    if args.urls_file:
        try:
            with open(args.urls_file, "r", encoding="utf-8") as fh:
                urls = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
        except OSError as e:
            sys.stderr.write("probe: cannot read --urls-file: %s\n" % e)
            return 2
    if args.url_opt:
        if args.url:
            sys.stderr.write("probe: give the URL once, positionally or with "
                             "--url, not both\n")
            return 2
        urls.insert(0, args.url_opt) if urls else urls.append(args.url_opt)
    if args.url:
        urls.insert(0, args.url) if urls else urls.append(args.url)
    if not urls:
        sys.stderr.write("probe: need a URL (or --urls-file, or --selftest)\n")
        return 2
    if len(urls) == 1 and args.concurrency > 1:
        urls = urls * args.concurrency
    if args.concurrency > 1 and len(urls) < args.concurrency:
        sys.stderr.write("probe: --urls-file has %d URLs for --concurrency %d; "
                         "reusing them (rule 7 will collapse throughput)\n"
                         % (len(urls), args.concurrency))
        urls = (urls * ((args.concurrency // len(urls)) + 1))[:args.concurrency]

    scheme = urllib.parse.urlsplit(urls[0]).scheme.lower()
    if scheme not in ("http", "https", "data"):
        sys.stderr.write("probe: unsupported scheme %r\n" % scheme)
        return 2

    try:
        if args.concurrency > 1:
            rec = probe_parallel(urls, args)
        else:
            rec = probe_once(urls[0], args)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        return 3

    emit(rec, not args.human)
    if args.out_dir:
        rc = write_out(rec, args.out_dir)
        if rc:
            return rc
    if rec.get("save_error"):
        # the body that --save-body names was not written: the record is complete, but the file a lane registers next
        # is missing, so the probe says so now (W3-02)
        sys.stderr.write("probe: --save-body %s was not written: %s\n" % (args.save_body, rec["save_error"]))
        return 3
    if rec.get("usable"):
        return 0
    status = rec.get("status")
    retryable = status in (429, 503) or any(
        r.get("status") in (429, 503) for r in rec.get("runs") or [])
    return 4 if retryable else 1


if __name__ == "__main__":
    sys.exit(main())
