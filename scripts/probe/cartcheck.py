#!/usr/bin/env python3
"""cartcheck.py -- read a WHMCS or Blesta cart without calling a live store dead.

PURPOSE
    Answer one question about one URL: does the vendor's cart price the plan its
    page advertises? Print the price it renders, or say plainly that the cart did
    not resolve and why.

WHY IT EXISTS
    This is the tool that a whole wave of research needed and did not have. On
    2026-10-24 two research lanes and the parent session each recorded VolpaByte's
    Ryzen KVM 8 GB as `verdict: dead`, because the store answered "Could not load
    any product groups." That store was healthy. WHMCS and Blesta both refuse to
    resolve a product group until the client has a session, and the broker drives
    curl with no cookie jar by design. Warming a jar from the vendor's own homepage
    and retrying the identical URL returns `cart.php?a=confproduct&i=0` with all
    four billing cycles priced.

    The same artefact hits AlphaVPS: `cart.php?a=add&pid=509` bounces to the store
    list without a jar and lands on the configurator with one. A cookieless read of
    either host is a statement about the tool, not about the vendor, and publishing
    it as a finding costs the corpus its best answer.

    So the rule is mechanical rather than remembered: a cart is only dead when it
    fails **with** a jar.

DEPENDENCIES
    Python standard library only (urllib, http.cookiejar). No broker, no curl, no
    network service of ours: a cart is read from the vendor directly, which is the
    only way to carry a session.

USAGE
    python scripts/probe/cartcheck.py URL
    python scripts/probe/cartcheck.py URL --warm https://vendor.example/
    python scripts/probe/cartcheck.py URL --json
    python scripts/probe/cartcheck.py URL --jar .tmp/session-<id>/x.jar --keep

    --warm defaults to the URL's own origin root, which is what a browser does.

OUTPUT
    Human form: a short header, then every price-looking string and every stock
    phrase found in the rendered body, then a verdict line.
    --json: {"url", "final_url", "status", "bytes", "title", "prices", "stock",
             "verdict", "note", "checked_at"}

    verdict is one of:
      priced      the cart rendered at least one price; read them yourself
      no-price    the page answered but carries no price string
      unresolved  the store says it cannot load the product group
      blocked     a bot challenge or a login wall, not a cart
      error       transport or HTTP failure

EXIT CODES
    0  priced
    1  no-price, unresolved, blocked or error -- the caller must look
    2  usage error
    3  environment wrong: no python ssl, or the URL is not http(s)
"""
import argparse
import http.cookiejar
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

PRICE_RE = re.compile(
    r"(?:USD|EUR|GBP|CHF|TRY|CNY|RUB|IDR|INR|PLN|BRL)\s?\d[\d.,]*"
    r"|[$€£₽¥]\s?\d[\d.,]*"
    r"|\d[\d.,]*\s?(?:USD|EUR|GBP|CHF|TRY|CNY|RUB|IDR)")
STOCK_RE = re.compile(
    r"out of stock|sold out|0 available|0 in stock|unavailable|"
    r"orders have been suspended|rupture de stock|nicht verfügbar|ausverkauft",
    re.I)
UNRESOLVED_RE = re.compile(
    r"could not load any product group|product group does not contain any visible product|"
    r"no products? (?:were )?found|invalid product", re.I)
BLOCK_RE = re.compile(
    r"just a moment|enable javascript and cookies|cf-chl|attention required|"
    r"performing security verification|access denied", re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def strip_tags(html):
    text = re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&#39;", "'").replace("&quot;", '"'))
    return re.sub(r"\s+", " ", text)


def fetch(opener, url, timeout):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with opener.open(req, timeout=timeout) as resp:
        raw = resp.read()
        return resp.geturl(), resp.status, raw


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("url")
    ap.add_argument("--warm", default=None,
                    help="URL to visit first so the session cookie is set "
                         "(default: the target's origin root)")
    ap.add_argument("--jar", default=None, help="cookie jar path")
    ap.add_argument("--keep", action="store_true", help="do not delete the jar")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv[1:])

    if not args.url.lower().startswith(("http://", "https://")):
        print("cartcheck: only http(s) URLs", file=sys.stderr)
        return 2
    try:
        ssl.create_default_context()
    except Exception:
        print("cartcheck: no usable ssl in this python", file=sys.stderr)
        return 3

    jar = http.cookiejar.LWPCookieJar(args.jar) if args.jar else http.cookiejar.CookieJar()
    if args.jar:
        try:
            jar.load(ignore_discard=True)
        except Exception:
            pass
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    warm = args.warm or "{0.scheme}://{0.netloc}/".format(urllib.parse.urlsplit(args.url))
    out = {"url": args.url, "warm": warm, "final_url": None, "status": None,
           "bytes": 0, "title": None, "prices": [], "stock": [],
           "verdict": "error", "note": "",
           "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")}

    # The warm request is what makes a WHMCS or Blesta store resolve at all. A
    # failure here is not fatal: some hosts set the cookie on any 200, and some
    # need none. It is recorded so a reader knows the session was attempted.
    try:
        fetch(opener, warm, args.timeout)
    except Exception as exc:
        out["note"] = "warm request failed (%s); continuing cold" % type(exc).__name__

    try:
        final, status, raw = fetch(opener, args.url, args.timeout)
    except urllib.error.HTTPError as exc:
        out.update(status=exc.code, verdict="error",
                   note="HTTP %d from the origin" % exc.code)
        return emit(out, args)
    except Exception as exc:
        out.update(verdict="error", note="%s: %s" % (type(exc).__name__, exc))
        return emit(out, args)

    html = raw.decode("utf-8", "replace")
    text = strip_tags(html)
    m = TITLE_RE.search(html)
    out.update(final_url=final, status=status, bytes=len(raw),
               title=(m.group(1).strip()[:160] if m else None))

    seen = []
    for hit in PRICE_RE.findall(text):
        hit = " ".join(hit.split())
        if hit not in seen:
            seen.append(hit)
    out["prices"] = seen[:40]
    out["stock"] = sorted({s.lower() for s in STOCK_RE.findall(text)})

    if BLOCK_RE.search(text) or BLOCK_RE.search(html[:4000]):
        out["verdict"] = "blocked"
        out["note"] = "a bot challenge or login wall answered, not a cart"
    elif UNRESOLVED_RE.search(text):
        out["verdict"] = "unresolved"
        out["note"] = ("the store refused to resolve the product group even with a "
                       "session; this is the only condition under which 'dead' is fair")
    elif seen:
        out["verdict"] = "priced"
    else:
        out["verdict"] = "no-price"
        out["note"] = "the page answered but carries no price string"

    if args.jar and not args.keep:
        try:
            jar.save(ignore_discard=True)
        except Exception:
            pass
    return emit(out, args)


def emit(out, args):
    if args.json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    else:
        print("url        %s" % out["url"])
        print("warm       %s" % out["warm"])
        print("final      %s" % out["final_url"])
        print("status     %s   bytes %d" % (out["status"], out["bytes"]))
        print("title      %s" % (out["title"] or "-"))
        print("prices     %s" % (", ".join(out["prices"]) if out["prices"] else "-"))
        print("stock      %s" % (", ".join(out["stock"]) if out["stock"] else "-"))
        print("verdict    %s" % out["verdict"])
        if out["note"]:
            print("note       %s" % out["note"])
    return 0 if out["verdict"] == "priced" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
