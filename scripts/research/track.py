"""The parent's own tracker: one GitHub issue per run, comments at each phase, labelled follow-up and
policy issues. Issues are for agents to keep track across sessions and harnesses, not a queue for a person.
Without `gh` (or off GitHub) every call writes to .tmp/<run>/issue.md instead, so nothing depends
on GitHub being reachable. Every gh call names the repository with --repo (settings.json github_repo), so gh never
resolves a remote of the checkout and never writes its configuration."""
import json
import os
import re
import shutil
import subprocess
import sys
import time

from common import GITHUB_REPO, REPO, Fail, no_close, run_dir, stamp

LABELS = {"rq:run": ("0e8a16", "a research run tracked by its parent agent"),
          "rq:followup": ("fbca04", "work a run found and left for a later run"),
          "rq:policy": ("d93f0b", "a rule question for a later methodology unit"),
          "rq:review": ("1d76db", "a run's pull request, waiting for a merge session that did not run it"),
          "rq:changes": ("e99695", "a run's pull request that a merge session sent back for changes"),
          "rq:baseline": ("5319e7", "a merge session reviewed the rows this pull request adds to the baseline"),
          "rq:active": ("c2e0c6", "an rq:research issue with a live claim (rq open --issue N; rq issues lists them)"),
          "rq:operator": ("b60205", "work only the operator can do")}
CLAIM, LANDED, RELEASED, MERGED = "rq claim:", "rq landed:", "rq released:", "rq merged:"
# the comment a merge session writes on an issue when it merges the issue's tools pull request
TOOL_MERGED = "rq tool merged:"
# the last Done-when line of an issue that is run once for each topic, and the words that keep a line from --meets
PER_TOPIC_LINE = "Every topic of the list has a merged run"
MERGE_ONLY = "a merge session ticks this line"
# labels of the public repository that intake relies on: the issue forms set "report", intake sets "queued"
PUBLIC_LABELS = {"report": ("c5def5", "a report from the issue forms"),
                 "queued": ("bfdadc", "queued for verification in the research repository")}


def _forge(args):
    """The broker's answer to a read shape, or None. forgeread refuses every shape that is not a read, so a write is
    never sent to it."""
    try:
        import forgeread
    except ImportError:
        return None
    return forgeread.read(with_repo(args, strip=True), GITHUB_REPO)


def gh_run(args, repo=REPO, input_text=None):
    """-> (exit code, stdout). gh exits non-zero for some answers that still carry JSON (8: checks pending), so
    a caller that reads such a command sees both. (None, "") without gh or with RQ_NO_GITHUB, unless the call is one
    of the read shapes forgeread serves: then the broker answers it with no token of the caller's, so a contributor
    with no account still reads the queue. A call that GitHub refuses with a 403 or a 429 that carries Retry-After
    (its secondary limit on writes) is repeated once after that many seconds, as broker.sh --wait does for the
    broker: the server's own pause, not a cap of the harness, which sets no pacing of its own (AGENTS.md section 2
    rule 15)."""
    if not shutil.which("gh") or os.environ.get("RQ_NO_GITHUB"):
        # read-only: a write has no fallback, and keeps the message its caller already writes
        got = _forge(args)
        return (0, got) if got is not None else (None, "")
    rc, out = gh_retry(with_repo(args), repo, input_text)
    if rc == 0 or out:
        return rc, out
    # gh is installed but answered nothing: a machine with no token of its own, or a token without the scope. A read
    # the broker serves must still answer there, or a contributor with no account cannot see the queue at all. A
    # write is not one of those shapes, so it keeps the failure its caller already reports.
    got = _forge(args)
    return (0, got) if got is not None else (rc, out)


def gh_once(args, repo=REPO, input_text=None):
    """One gh process. -> (exit code, stdout, stderr). GH_DEBUG=api puts the status and the headers of each answer on
    stderr (the token is masked there), where retry_after reads Retry-After; stderr is read, never printed or stored."""
    try:
        r = subprocess.run(["gh"] + args, cwd=repo, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", input=input_text, timeout=120, env=dict(os.environ, GH_DEBUG="api"))
    except subprocess.TimeoutExpired:
        return None, "", ""
    return r.returncode, r.stdout.strip(), r.stderr or ""


def gh_retry(args, repo=REPO, input_text=None, once=None):
    """gh_once, and once more after the Retry-After of a 403 or 429. -> (exit code, stdout)."""
    once = once or gh_once
    rc, out, err = once(args, repo, input_text)
    wait = retry_after(err) if rc not in (0, None) else None
    if wait is not None:
        print("rq: GitHub refused gh %s with Retry-After %d s; waiting that long once, as GitHub asks, then repeating "
              "the call" % (" ".join(args[:2]), wait), file=sys.stderr)
        time.sleep(wait)  # wait: retry-after, GitHub's own pause for a refused call (its secondary limit)
        rc, out, err = once(args, repo, input_text)
    return rc, out


def retry_after(err, now=None):
    """The seconds of the Retry-After header of gh's last answer when that answer is a 403 or a 429, from the
    GH_DEBUG=api log on stderr ("< HTTP/2.0 403 Forbidden", "< Retry-After: 60"): a number, or an HTTP date made into
    seconds. None for any other answer, and for a 403 or 429 without the header."""
    answers = []
    for ln in (err or "").splitlines():
        m = re.match(r"^< HTTP/\S+ (\d{3})\b", ln)
        if m:
            answers.append([m.group(1), None])
            continue
        m = re.match(r"^< retry-after:\s*(.+?)\s*$", ln, re.I)
        if m and answers:
            answers[-1][1] = m.group(1)
    if not answers or answers[-1][0] not in ("403", "429") or not answers[-1][1]:
        return None
    v = answers[-1][1]
    if re.match(r"^\d+$", v):
        return int(v)
    try:
        import email.utils
        when = email.utils.parsedate_to_datetime(v)
    except (TypeError, ValueError, IndexError):
        return None
    if when is None:
        return None
    import datetime as dt
    now = now or dt.datetime.now(dt.timezone.utc)
    return max(0, int((when - now).total_seconds() + 0.999))


def gh(args, repo=REPO, input_text=None):
    rc, out = gh_run(args, repo, input_text)
    if rc != 0:
        return None
    return out


# the noreply address of the account gh is signed in as, asked once per process: gh pr merge without --author-email
# makes the merge commit with the account's primary address, which is private
NOREPLY = {}
NOREPLY_RE = re.compile(r"\d+\+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\[bot\])?@users\.noreply\.github\.com")


def noreply_email(repo=REPO):
    """The GitHub noreply address of the signed-in account, ID+LOGIN@users.noreply.github.com, from gh api user. None
    when gh cannot answer or answers something else; only an address is kept, so a later call asks again."""
    if NOREPLY.get("addr"):
        return NOREPLY["addr"]
    out = (gh(["api", "user", "--jq", '"\\(.id)+\\(.login)@users.noreply.github.com"'], repo) or "").strip()
    if not NOREPLY_RE.fullmatch(out):
        return None
    NOREPLY["addr"] = out
    return out


LOGIN = {}


def login(repo=REPO):
    """The login of the account gh is signed in as, asked once per process. None when gh cannot answer."""
    if "login" in LOGIN:
        return LOGIN["login"]
    out = (gh(["api", "user", "--jq", ".login"], repo) or "").strip()
    LOGIN["login"] = out or None
    return LOGIN["login"]


def with_repo(args, strip=False):
    """gh issue, pr and label calls name this repository with --repo, unless they name one already. strip=True
    removes a --repo/--owner pair instead, for a caller that takes the repository as its own argument (forgeread)."""
    if strip:
        out, i = [], 0
        while i < len(args):
            if args[i] in ("--repo", "-R", "--owner") and i + 1 < len(args):
                i += 2
                continue
            out.append(args[i])
            i += 1
        return out
    if GITHUB_REPO and args[:1] and args[0] in ("issue", "pr", "label") and "--repo" not in args and "-R" not in args:
        return args[:2] + ["--repo", GITHUB_REPO] + args[2:]
    return args


def labels_key():
    return "labels:%s" % (GITHUB_REPO or "-")


def ensure_labels(repo=REPO):
    """The rq labels exist on the repository: one gh label list, then a gh label create for each label that is
    missing. The answer is kept for the checkout in .tmp/rq/state.db, not for the process, so thirty sessions that open
    runs at once list the labels once between them and create none that exists; a wipe clears it, and a write that
    fails on a label forgets it. -> True when every label exists."""
    import state
    key = labels_key()
    if state.memo(repo, key):
        return True
    out = gh(["label", "list", "--limit", "500", "--json", "name", "--jq", ".[].name"], repo)
    if out is None:
        return False
    have = {ln.strip() for ln in out.splitlines() if ln.strip()}
    made = True
    for name, (color, desc) in LABELS.items():
        if name not in have and gh(["label", "create", name, "--color", color, "--description", desc, "--force"],
                                   repo) is None:
            made = False
    if made:
        state.set_memo(repo, key, stamp())
    return made


def forget_labels(repo=REPO):
    import state
    state.drop_memo(repo, labels_key())


def ensure_public_labels(public, repo=REPO):
    """The labels intake writes on the public repository, created when they are missing."""
    out = gh(["label", "list", "--repo", public, "--limit", "200", "--json", "name", "--jq", ".[].name"], repo)
    if out is None:
        return False
    have = set(out.split())
    for name, (color, desc) in PUBLIC_LABELS.items():
        if name not in have:
            gh(["label", "create", name, "--repo", public, "--color", color, "--description", desc], repo)
    return True


def local(run, text, repo=REPO):
    p = os.path.join(run_dir(run, repo), "issue.md")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n## %s\n\n%s\n" % (stamp(), text))


def open_issue(r, repo=REPO):
    body = ("Request: %s\n\nRun `%s` (%s, topic `%s`). Opened %s.\n\nPhases: open, plan, lanes, collect, integrate, "
            "audit, land. `scripts/rq` comments here at each phase; the run lands as a PR that closes this issue.\n\n"
            "State on disk: `.tmp/%s/` and the git ref `rq/%s`. `scripts/rq status` reads them."
            % (r["request"], r["run"], r["kind"], r["topic"], r["created"], r["run"], r["run"]))
    title = no_close("rq %s %s: %s" % (r["kind"], r["topic"], r["request"][:80]))
    body = no_close(body)
    if ensure_labels(repo):
        out = gh(["issue", "create", "--title", title, "--label", "rq:run", "--body-file", "-"], repo, body)
        if out and "/issues/" in out:
            return int(out.rstrip("/").split("/")[-1])
        forget_labels(repo)  # a label deleted on GitHub fails the create: the next call lists the labels again
    local(r["run"], "# %s\n\n%s" % (title, body), repo)
    return None


def comment(r, text, repo=REPO):
    text = no_close(text)
    if r.get("issue") and gh(["issue", "comment", str(r["issue"]), "--body-file", "-"], repo, text) is not None:
        return
    local(r["run"], text, repo)


def parse_time(s):
    import datetime as dt
    return dt.datetime.strptime((s or "")[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)


def _words(body):
    """"rq claim: run R topic T started ..." -> (run, topic). A claim written before claims named a topic has none."""
    w = (body or "").replace(",", " ").split()
    run = w[3] if len(w) > 3 and w[2] == "run" else ("*" if len(w) > 3 and w[2:4] == ["every", "claim"] else None)
    topic = w[5] if len(w) > 5 and w[4] == "topic" else None
    return run, topic


def claim_events(comments):
    """The claims of an issue from its comments, oldest first. -> list of {"run", "topic", "at", "landed", "pr", "ended"}.
    "rq landed:" adds the pull request; "rq released:" and "rq merged:" end a claim ("rq released: every claim" ends all)."""
    runs = {}
    for c in comments:
        b, at = c.get("body") or "", c.get("createdAt") or ""
        if b.startswith(CLAIM):
            run, topic = _words(b)
            if run:
                runs[run] = {"run": run, "topic": topic, "at": at, "landed": None, "pr": None, "ended": None}
        elif b.startswith(LANDED):
            run, _ = _words(b)
            if run in runs:
                m = re.search(r"/pull/(\d+)", b)
                runs[run].update(landed=at, pr=int(m.group(1)) if m else None)
        elif b.startswith(RELEASED) or b.startswith(MERGED):
            run, _ = _words(b)
            for ev in runs.values():
                if (run == "*" or ev["run"] == run) and not ev["ended"]:
                    ev["ended"] = at
    return sorted(runs.values(), key=lambda e: e["at"])


def live_claims(comments, now, hours, pr_states=None):
    """-> (live, expired). A claim lives until it is released or merged; a landed claim lives while its pull request is
    open (or its state is not known), and ends when the pull request is closed without a merge or merged; a claim
    with no pull request expires after `hours`. pr_states: {pull request number: "OPEN" | "CLOSED" | "MERGED"}."""
    live, expired = [], []
    for ev in claim_events(comments):
        if ev["ended"]:
            continue
        if ev["landed"]:
            if (pr_states or {}).get(ev["pr"]) in ("CLOSED", "MERGED"):
                continue
            live.append(ev)
            continue
        ev = dict(ev, age=(now - parse_time(ev["at"])).total_seconds() / 3600.0)
        (live if ev["age"] < hours else expired).append(ev)
    return live, expired


def same_topic(ev, topic):
    return topic is None or ev.get("topic") is None or ev["topic"] == topic


def describe(ev, hours):
    t = " (topic %s)" % ev["topic"] if ev.get("topic") else ""
    if ev.get("landed"):
        return "run %s%s landed; its pull request %s waits for a merge session, which judges the issue" % (
            ev["run"], t, "#%d" % ev["pr"] if ev.get("pr") else "")
    return "run %s%s claimed it %.1f hours ago; the claim holds %d hours with no pull request" % (ev["run"], t, ev["age"], hours)


def claim_verdict(labels, comments, now, hours, topic=None, pr_states=None):
    """Is an rq:research issue free for a new run on `topic`? labels: names; comments: [{"body", "createdAt"}], oldest
    first; pr_states: see live_claims. -> (free, why). Only the claims of the same topic count, so an issue that is run
    once for each topic takes one run per topic at a time; a claim that names no topic counts for every topic. A claim
    lives in its `rq claim:` comment; the label rq:active is a convenience a contributor without triage rights cannot add."""
    live, expired = live_claims(comments, now, hours, pr_states)
    mine = [e for e in live if same_topic(e, topic)]
    if mine:
        return False, describe(mine[-1], hours)
    gone = [e for e in expired if same_topic(e, topic)]
    if gone:
        return True, "the claim of run %s expired (%.1f hours, no pull request)" % (gone[-1]["run"], gone[-1]["age"])
    return True, "no live claim" + (" for topic %s" % topic if topic and live else "")


def issue_state(n, repo=REPO):
    """-> {"state", "labels", "comments", "body"} of an issue, or None without gh."""
    out = gh(["issue", "view", str(n), "--json", "state,labels,comments,body"], repo)
    if not out:
        return None
    d = json.loads(out)
    return {"state": d.get("state"), "labels": [x["name"] for x in d.get("labels") or []], "body": d.get("body") or "",
            "comments": [{"body": c.get("body") or "", "createdAt": c.get("createdAt") or ""} for c in d.get("comments") or []]}


def pr_states_of(comments, repo=REPO, known=None):
    """The state of each pull request that a "rq landed:" comment names. -> {number: state}."""
    out = dict(known or {})
    for ev in claim_events(comments):
        if ev["pr"] and ev["pr"] not in out:
            s = gh(["pr", "view", str(ev["pr"]), "--json", "state", "--jq", ".state"], repo)
            if s:
                out[ev["pr"]] = s.strip()
    return out


def claim(n, run, hours, now, repo=REPO, topic=None, info=None):
    """Claim rq:research issue N for a run on `topic`: a comment with the run id, the topic and the UTC time, and,
    when the account may write it, the label rq:active. The comment is the claim, so another session, on the same
    GitHub account or not, sees that the issue is taken. -> (written,
    message). Refuses a live claim of the same topic. info, a dict, gets "per_topic" when the issue was read: True for
    an issue that is run once for each topic, whose run plans only its own topic's bullets (W5-01).

    Thirty sessions of one checkout that take a free issue at the same moment must not all claim it (F-01): the claim
    lock of the issue and topic (.tmp/rq/locks/) is held from the read of the issue to the read-back of the claim, and
    the local claims in .tmp/rq/state.db refuse a second claim of the same topic while a run of this checkout holds it.
    A session on another machine is not serialised by the lock: after the comment, the issue is read again, and a claim
    of the same topic that GitHub lists before this one wins; this one is given back and refused. Every write is
    checked (F-02): a failed one is undone and the claim refused, and open closes the run, still in phase opening."""
    import state
    from common import FileLock, rq_home

    def told(holder):
        print("rq: waiting for the claim lock of issue #%d topic %s (%s): another session of this checkout is claiming "
              "it" % (n, topic or "-", holder or "another process"), file=sys.stderr)
    name = "claim-%d-%s.lock" % (n, re.sub(r"[^A-Za-z0-9_.-]", "_", topic or "-"))
    with FileLock(os.path.join(rq_home(repo), "locks", name), wait=True, what="the claim lock of issue #%d" % n,
                  on_wait=told):
        held = local_holder(n, run, topic, hours, repo)
        if held:
            raise Fail("issue #%d is taken: run %s of this checkout (phase %s) holds topic %s. Take another free issue "
                       "from scripts/rq issues. A run whose session died is given back with scripts/rq close %s --reason "
                       "\"...\"" % (n, held[0], held[1], topic or "-", held[0]), 1)
        state.add_claim(repo, n, run, topic)
        try:
            return _claim(n, run, hours, now, repo, topic, info)
        except BaseException:
            state.drop_claim(repo, n, run)
            raise


def local_holder(n, run, topic, hours, repo=REPO):
    """The run of this checkout, other than `run`, that holds a live claim of issue N on `topic`. -> (run, phase) or
    None. A local claim lives while its run is not closed, merged or landed empty. A run that has not landed (any phase
    but in-review) holds it for `hours`, as a claim with no pull request holds on GitHub."""
    import state
    from common import DONE_PHASES, now_ts, read_json
    for other, t, at in state.claims(repo, n):
        if other == run or not same_topic({"topic": t}, topic):
            continue
        try:
            r = read_json(os.path.join(run_dir(other, repo), "run.json"), None)
        except (Fail, ValueError, OSError):
            r = None
        if not isinstance(r, dict) or r.get("phase") in DONE_PHASES:
            continue
        if r.get("phase") != "in-review" and now_ts() - float(at) >= hours * 3600:
            continue
        return other, r.get("phase") or "-"
    return None


def _claim(n, run, hours, now, repo, topic, info):
    """claim, under the claim lock of the issue and topic."""
    st = issue_state(n, repo)
    if st is not None and info is not None:
        info["per_topic"] = per_topic(st.get("body") or "")
    text = "%s run %s topic %s started at %s" % (CLAIM, run, topic or "-", stamp())
    if st is None:
        if os.environ.get("RQ_NO_GITHUB"):
            return False, "claim of issue #%d not written (RQ_NO_GITHUB)" % n
        return False, ("no gh: the claim of issue #%d is not written. Tell the operator, who writes it: gh issue edit %d "
                       "--add-label rq:active, and gh issue comment %d --body \"%s\"" % (n, n, n, text))
    if st["state"] != "OPEN":
        raise Fail("issue #%d is %s, not open" % (n, st["state"]), 1)
    if "rq:research" not in st["labels"]:
        raise Fail("issue #%d is not labelled rq:research" % n, 1)
    states = pr_states_of(st["comments"], repo)
    free, why = claim_verdict(st["labels"], st["comments"], now, hours, topic, states)
    if free and "rq:active" in st["labels"]:
        # a claim that expired with no "rq landed:" comment can belong to a land killed after gh pr create: the branch
        # has an open pull request, and the issue is still taken (G3-03)
        for ev in live_claims(st["comments"], now, hours, states)[1]:
            if same_topic(ev, topic) and (gh(["pr", "view", "rq/%s" % ev["run"], "--json", "state", "--jq", ".state"],
                                             repo) or "").strip() == "OPEN":
                free, why = False, ("run %s has an open pull request on rq/%s although its claim expired with no \"rq "
                                    "landed:\" comment (a land killed after it opened the pull request)" % (ev["run"], ev["run"]))
                break
    if not free:
        raise Fail("issue #%d is taken: %s. Take another free issue from scripts/rq issues" % (n, why), 1)
    again = "Run scripts/rq open again, or take another free issue from scripts/rq issues"
    if not ensure_labels(repo):
        raise Fail("issue #%d: the labels of the repository could not be listed or created (gh failed: a refused call, an "
                   "expired login or the network); nothing was written and the issue is not claimed. %s" % (n, again), 1)
    if gh(["issue", "comment", str(n), "--body-file", "-"], repo, no_close(
          "%s, in the research checkout. The claim holds until the run lands (its pull request says \"Part of #%d\") and a "
          "merge session merges or closes that pull request, or %d hours with no pull request.%s"
          % (text, n, hours, "" if why.startswith("no live claim") else " Note: %s." % why))) is None:
        # a call that failed after GitHub stored the comment (a timeout) leaves a claim behind: give it back
        late = issue_state(n, repo)
        note = ""
        if late and any(e["run"] == run for e in claim_events(late["comments"])):
            note = " The comment was stored all the same: %s." % give_back(n, run, topic, "gh reported the claim as failed", repo)
        raise Fail("issue #%d: the claim comment was not written (gh failed: a refused call, an expired login or the "
                   "network), so the issue is not claimed.%s %s" % (n, note, again), 1)
    from common import test_stop
    test_stop("claim")  # the selftest's kill after the claim comment: rq close of the run gives the claim back
    unlabelled = False
    if gh(["issue", "edit", str(n), "--add-label", "rq:active"], repo) is None:
        forget_labels(repo)
        # The comment is the claim. A contributor without triage rights cannot add the label; the
        # claim still names the run and the topic, and claim_verdict reads it.
        unlabelled = True
        if info is not None:
            info["claim_unlabelled"] = True
    back = issue_state(n, repo)
    if back is None:
        raise Fail("issue #%d: the claim could not be read back to look for a claim written at the same moment; it is "
                   "%s. %s" % (n, give_back(n, run, topic, "the claim could not be read back", repo), again), 1)
    first = earlier_claim(back["comments"], run, topic, now, hours, pr_states_of(back["comments"], repo, states))
    if first:
        raise Fail("issue #%d is taken: run %s claimed topic %s at the same moment, and GitHub lists its claim first; this "
                   "claim is %s. Take another free issue from scripts/rq issues"
                   % (n, first["run"], topic or "-", give_back(n, run, topic, "run %s claimed topic %s a moment earlier"
                                                               % (first["run"], topic or "-"), repo)), 1)
    note = "; the label rq:active could not be added, so the claim is the comment alone" if unlabelled else ""
    return True, "claimed issue #%d for topic %s (%s)%s" % (n, topic or "-", why, note)


def earlier_claim(comments, run, topic, now, hours, pr_states=None):
    """The live claim of `topic` by another run that GitHub lists before this run's claim, or None. Two sessions on
    different machines that read the issue as free at the same moment both write a claim; GitHub keeps the comments in
    the order it stored them, so both read the same order, and the second gives its claim back. When this run's claim
    is not among the comments, every other live claim of the topic counts as earlier."""
    pos = {}
    for i, c in enumerate(comments):
        if (c.get("body") or "").startswith(CLAIM):
            pos.setdefault(_words(c["body"])[0], i)
    mine = pos.get(run, len(comments))
    for ev in live_claims(comments, now, hours, pr_states)[0]:
        if ev["run"] != run and same_topic(ev, topic) and pos.get(ev["run"], -1) < mine:
            return ev
    return None


def give_back(n, run, topic, why, repo=REPO):
    """Take back a claim this run wrote and cannot keep: an "rq released:" comment. The label rq:active stays: another
    claim may rely on it, and an issue with the label and no live claim reads as free. -> words for the caller."""
    text = no_close("%s run %s topic %s at %s: %s" % (RELEASED, run, topic or "-", stamp(), why))
    if gh(["issue", "comment", str(n), "--body-file", "-"], repo, text) is None:
        return ("not given back, because the release comment failed too: scripts/rq release %d --run %s --reason \"%s\" "
                "gives it back" % (n, run, why))
    return "given back (an rq released: comment)"


def end_claim(n, run, why, prefix, now, hours, repo=REPO, topic=None):
    """End one claim (run) or every claim (run None) of issue N: a comment that starts with `prefix`, then the label
    rq:active comes off when no other claim lives. The local claim of the run (of every run, with run None) goes from
    .tmp/rq/state.db first, so this checkout can claim the topic again. -> a line for the caller."""
    import state
    state.drop_claim(repo, n, run)
    st = issue_state(n, repo)
    if run and not topic and st:
        topic = next((e["topic"] for e in claim_events(st["comments"]) if e["run"] == run), None)
    who = "run %s topic %s" % (run, topic or "-") if run else "every claim"
    text = no_close("%s %s at %s: %s" % (prefix, who, stamp(), why))
    if st is None:
        if os.environ.get("RQ_NO_GITHUB"):
            return "issue #%d: %s not written (RQ_NO_GITHUB)" % (n, prefix)
        return ("no gh: tell the operator, who writes it: gh issue comment %d --body \"%s\", and gh issue edit %d "
                "--remove-label rq:active when no other run holds a claim on it (scripts/rq issues)" % (n, text, n))
    if gh(["issue", "comment", str(n), "--body-file", "-"], repo, text) is None:
        return ("issue #%d: the %s comment was not written (gh failed: a refused call, an expired login or the network); "
                "run the same command again, or tell the operator, who writes it: gh issue comment %d --body \"%s\""
                % (n, prefix, n, text))
    comments = st["comments"] + [{"body": text, "createdAt": now.strftime("%Y-%m-%dT%H:%M:%SZ")}]
    live, _ = live_claims(comments, now, hours, pr_states_of(comments, repo))
    if not live:
        gh(["issue", "edit", str(n), "--remove-label", "rq:active"], repo)
        return "issue #%d: %s; no claim lives, rq:active removed" % (n, who)
    return "issue #%d: %s; rq:active stays for %s" % (n, who, ", ".join("run %s (topic %s)" % (e["run"], e["topic"] or "-")
                                                                     for e in live))


def release(n, run, reason, now, hours, repo=REPO, topic=None):
    """rq release: a claim that will not land (a dead session, a pull request closed without a merge) is given back."""
    return end_claim(n, run, reason, RELEASED, now, hours, repo, topic)


PER_TOPIC_RE = re.compile(r"run once for each topic|topics of the list have a merged run", re.I)


def per_topic(body):
    """An issue that is run once for each topic: its Done-when line PER_TOPIC_LINE, or a body that says so in other
    words ("This issue is run once for each topic", "Both topics of the list have a merged run")."""
    return any(ln.startswith(PER_TOPIC_LINE) for ln in done_lines(body)) or bool(PER_TOPIC_RE.search(body or ""))


def merge_only(line):
    """A Done-when line that no run ticks: a merge session ticks it (the tools pull request, every topic merged)."""
    return MERGE_ONLY in line.lower()


def list_issues(now, hours, repo=REPO):
    """rq issues: every open rq:research issue with its claim verdict. -> lines, or None without gh."""
    out = gh(["issue", "list", "--label", "rq:research", "--state", "open", "--limit", "200",
              "--json", "number,title,labels,body,comments"], repo)
    if out is None:
        return None
    lines = []
    for it in sorted(json.loads(out), key=lambda x: x["number"]):
        comments = [{"body": c.get("body") or "", "createdAt": c.get("createdAt") or ""} for c in it.get("comments") or []]
        live, _ = live_claims(comments, now, hours, pr_states_of(comments, repo))
        if per_topic(it.get("body") or ""):
            v = "per topic: every topic is free" if not live else "per topic: free except " + "; ".join(
                "%s (%s)" % (e["topic"] or "every topic", describe(dict(e, topic=None), hours)) for e in live)
        elif live:
            v = "taken: " + describe(live[-1], hours)
        else:
            v = "free"
        if waits_for_tool(it.get("body") or "", comments, repo):
            v += "; waits for a tool (its tools pull request is not merged: take another issue)"
        lines.append("#%d\t%s\t%s" % (it["number"], it["title"][:90], v))
    return lines


TOOL_PATH = re.compile(r"`(scripts/[A-Za-z0-9_./-]+\.(?:py|sh))`")


def waits_for_tool(body, comments, repo=REPO):
    """An issue whose Done-when has a "Tool:" line waits for its tool until the tool is merged: a path the line names
    is on main (or in this checkout's HEAD), or a merge session commented `rq tool merged:` on the issue. A research
    agent does not write a tool (docs/research-protocol.md section 2), so such an issue is not one to take yet."""
    tool = [ln for ln in done_lines(body) if ln.startswith("Tool:")]
    if not tool or re.search(r"does not wait for the tool", body, re.I):
        return False
    if any((c.get("body") or "").startswith(TOOL_MERGED) for c in comments):
        return False
    paths = TOOL_PATH.findall(" ".join(tool))
    if paths:
        from common import TreeView, rev, upstream
        for name in (upstream(repo), "HEAD"):
            if rev(repo, name):
                view = TreeView(repo, name)
                if all(view.exists(x) for x in paths):
                    return False
    return True


DONE_ITEM_RE = re.compile(r"^(?:- |\d+\. )(.*)$")
# the one Done-when line that a green CI proves: the comparison of CI's `gate` job with main. rq merge merges only a
# head whose CI is green, so land ticks it (W3-03). A line that asks for more than the comparison is not this line: one
# check of the gate (`sources`, red on main while any registry row is overdue, whatever the run diffed), or no new
# baseline row (the `baseline` job turns green with the label rq:baseline); the parent ticks such a line with --meets
# when it holds, and the merge session checks the tick (F-03).
CI_LINE_RE = re.compile(r"^CI's `gate` job is green on the (?:pull request that carries the work to `main`"
                        r"(?: \(the maintainer opens it when the work arrives as a zip\))?|pull request"
                        r"(?: \(it runs `scripts/rq check --gate`\))?)"
                        r"(?:: no (?:new error violation, and no )?check fails that passes on `main`)?\.?$")


def done_lines(body):
    """The items of the "## Done when" section of an issue body: bullets ("- ") or numbered ("1. ")."""
    out, inside = [], False
    for ln in (body or "").splitlines():
        if ln.startswith("## "):
            inside = ln.strip().lower() == "## done when"
            continue
        m = DONE_ITEM_RE.match(ln) if inside else None
        if m:
            out.append(m.group(1).strip())
    return out


def ci_line(line):
    """The Done-when line that CI's gate comparison on the pull request meets (and that no merge session ticks): "CI's
    `gate` job is green on the pull request", with nothing after it but what that job runs and the comparison."""
    return bool(CI_LINE_RE.match((line or "").strip())) and not merge_only(line)


def find_issue(title, label, repo=REPO):
    out = gh(["issue", "list", "--label", label, "--state", "all", "--search", title, "--json", "number,title", "--limit", "50"], repo)
    if not out:
        return None
    for it in json.loads(out):
        if it["title"] == title:
            return it["number"]
    return None


def open_labelled(title, body, label, repo=REPO, fallback_run=None):
    """Open an issue once per title (idempotent), with one label or a tuple of labels; the first label finds it again.
    -> issue number or None."""
    title, body = no_close(title), no_close(body)
    labels = [label] if isinstance(label, str) else list(label)
    if ensure_labels(repo):
        n = find_issue(title, labels[0], repo)
        if n:
            return n
        out = gh(["issue", "create", "--title", title] + [a for x in labels for a in ("--label", x)] + ["--body-file", "-"],
                 repo, body)
        if out and "/issues/" in out:
            return int(out.rstrip("/").split("/")[-1])
        forget_labels(repo)
    if fallback_run:
        local(fallback_run, "# %s\n\n%s" % (title, body), repo)
    return None
