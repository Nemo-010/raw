"""The read-only forge fallback: GitHub's REST API through forge.web.pkgforge.dev, for a contributor with no gh.

A caller with no GitHub account cannot authenticate gh, so every read of the issue queue used to fail and rq refused
with "needs gh". The forge broker answers GitHub's public reads from its own account with no token of the caller's
(https://forge.web.pkgforge.dev/llms.txt), which is enough to read the queue, an issue and its comments, and the state
of a pull request.

It answers reads only: a POST to the same host is a 405. That is the whole reason this module exists as a separate
thing rather than as a flag inside track.gh: a call that is not one of the four read shapes below is refused here, so
a write can never be sent to the broker by accident, and the write paths of the harness keep their own message.

Nothing here sets a pace: the broker answers 429 with Retry-After when it needs to, and this module repeats the call
after that pause once, as track.gh_retry does for gh (AGENTS.md section 2 rule 15).
"""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = "https://forge.web.pkgforge.dev"
TIMEOUT_S = 60


def _get(path, params=None):
    """-> (status, body text). A 429 is repeated once after its Retry-After, the server's own pause."""
    url = "%s/github/%s" % (HOST, path.lstrip("/"))
    if params:
        url += "?" + urllib.parse.urlencode(params)
    for attempt in (1, 2):
        req = urllib.request.Request(url, headers={"accept": "application/vnd.github+json",
                                                   "user-agent": "rq-forge-read"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            wait = e.headers.get("retry-after") if e.headers else None
            if e.code == 429 and attempt == 1 and wait:
                try:
                    time.sleep(max(0, int(wait)))
                except ValueError:
                    return e.code, body
                continue
            return e.code, body
        except (urllib.error.URLError, OSError):
            return None, ""
    return None, ""


def _json(path, params=None):
    st, body = _get(path, params)
    if st != 200 or not body:
        return None
    try:
        return json.loads(body)
    except ValueError:
        return None


def _issue_json(d):
    """The shape `gh issue view --json state,labels,comments,body` prints, from a REST issue object. gh prints the
    state in capitals ("OPEN"), and the harness compares against that, so the case is raised here and not at the
    caller."""
    return json.dumps({"state": str(d.get("state") or "").upper(),
                       "labels": [{"name": x.get("name")} for x in d.get("labels") or []],
                       "body": d.get("body") or "",
                       "comments": [{"body": c.get("body") or "",
                                     "createdAt": c.get("created_at") or "",
                                     "author": {"login": (c.get("user") or {}).get("login") or ""}}
                                    for c in d.get("comments") or []]}, sort_keys=True)


def read(args, repo):
    """Answer one of the harness's read-only gh calls, or None when this is not one of them.

    args is gh's argument list with --repo already removed; repo is "owner/name". None means "not a read this module
    serves", and the caller keeps its own behaviour for that."""
    if not args:
        return None
    a = list(args)

    def opt(name):
        if name in a:
            i = a.index(name)
            if i + 1 < len(a):
                return a[i + 1]
        return None

    if a[0] == "issue" and len(a) > 1 and a[1] == "list":
        label, state = opt("--label"), opt("--state") or "open"
        limit = opt("--limit") or "30"
        fields = (opt("--json") or "").split(",")
        if not label:
            return None
        items = _json("repos/%s/issues" % repo, {"labels": label, "state": state, "per_page": min(int(limit), 100)})
        if items is None:
            return None
        # gh's `issue list` leaves pull requests out; the REST issues route returns both
        items = [i for i in items if not i.get("pull_request")]
        out = []
        for i in items:
            row = {}
            if "number" in fields:
                row["number"] = i.get("number")
            if "title" in fields:
                row["title"] = i.get("title") or ""
            if "body" in fields:
                row["body"] = i.get("body") or ""
            if "labels" in fields:
                row["labels"] = [{"name": x.get("name")} for x in i.get("labels") or []]
            if "comments" in fields:
                # the list route carries no comment bodies; read them for the issues in the page
                got = _json("repos/%s/issues/%s/comments" % (repo, i.get("number"))) or []
                row["comments"] = [{"body": c.get("body") or "", "createdAt": c.get("created_at") or "",
                                    "author": {"login": (c.get("user") or {}).get("login") or ""}} for c in got]
            out.append(row)
        return json.dumps(out)

    if a[0] == "issue" and len(a) > 1 and a[1] == "view":
        n = a[2] if len(a) > 2 else None
        if not n or not str(n).isdigit():
            return None
        d = _json("repos/%s/issues/%s" % (repo, n))
        if d is None:
            return None
        if "comments" in d:
            d["comments"] = _json("repos/%s/issues/%s/comments" % (repo, n)) or []
        return _issue_json(d)

    if a[0] == "pr" and len(a) > 2 and a[1] == "view":
        n = a[2]
        if not str(n).isdigit():
            return None
        d = _json("repos/%s/pulls/%s" % (repo, n))
        if d is None:
            return None
        want = (opt("--json") or "").split(",")
        jq = opt("--jq") or ""
        if want == ["state"] and jq.strip() == ".state":
            return str(d.get("state") or "").upper()
        row = {}
        for f in want:
            if f == "state":
                row["state"] = str(d.get("state") or "").upper()
            elif f == "headRefName":
                row["headRefName"] = (d.get("head") or {}).get("ref") or ""
            elif f == "mergeable":
                row["mergeable"] = d.get("mergeable")
        return json.dumps(row)

    if a[0] == "label" and len(a) > 1 and a[1] == "list":
        d = _json("repos/%s/labels" % repo, {"per_page": 100})
        if d is None:
            return None
        jq = opt("--jq") or ""
        names = [x.get("name") for x in d if x.get("name")]
        if jq.strip() == ".[].name":
            return "\n".join(names)
        return json.dumps([{"name": n} for n in names])

    if a[0] == "api":
        path = a[1] if len(a) > 1 else ""
        if not path or path.startswith("-"):
            return None
        # a write is never served: --method anywhere, or a field flag that implies one, is refused here
        method = opt("--method") or opt("-X")
        if method and method.upper() != "GET":
            return None
        if any(x in a for x in ("-f", "--field", "--raw-field", "-F", "--input")):
            return None
        d = _json(path.lstrip("/"))
        if d is None:
            return None
        jq = opt("--jq")
        if jq:
            # only the two projections the harness asks for; anything else is refused rather than guessed
            if jq.strip() == ".state":
                return str(d.get("state") or "").upper()
            if "users.noreply.github.com" in jq:
                login, uid = d.get("login"), d.get("id")
                if login and uid:
                    return "%s+%s@users.noreply.github.com" % (uid, login)
                return None
            return None
        return json.dumps(d, sort_keys=True)

    return None
