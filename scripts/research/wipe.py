"""rq wipe and rq sync: the merge session's last steps in the research checkout (AGENTS.md section 2 rule 8).

  scripts/rq wipe --dry-run          list what a wipe would delete and what blocks it; change nothing
  scripts/rq wipe [--drain]          delete all of .tmp/ when no run is open, no lease is live, no session folder is
                                     live, no merge is unfinished and no store build runs; --drain also stops new runs
                                     from opening until a wipe can complete
  scripts/rq wipe --undrain          let research open runs again without a wipe
  scripts/rq sync [--repair]         fast-forward the research checkout to origin/main, build the store of the new
                                     HEAD once, refresh the index, run git maintenance

Everything in .tmp/ lives in folders with unique ids, and nothing there is needed after a merge pass: records,
ledgers, captures and manifests are on main, open items are in issues, and the store is built again. The wipe never
holds a state.db transaction across a network call, and it holds no file under .tmp/ open when it renames .tmp/.
"""
import glob
import os
import shutil
import stat
import sys

import state
import units
from common import (BASE, DONE_PHASES, REMOTE, REPO, SETTINGS, Fail, FileLock, Locked, close_git, extra_worktrees, fetch,
                    git, git_run, has_remote, is_ancestor, live_runs, read_json, rev, short_ref, stamp, status_paths,
                    upstream, utc_now)


def _rmtree(path):
    """Delete a folder on Windows too, where git marks its objects read-only."""
    def again(func, p, *_):
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except OSError:
            pass
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=again)
    else:
        shutil.rmtree(path, onerror=again)


def _size(path):
    n = b = 0
    for root, _, files in os.walk(path):
        for f in files:
            n += 1
            try:
                b += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return n, b


def _real(p):
    # realpath on both sides: git prints a long path where the checkout's path can be an 8.3 short name on Windows
    return os.path.normcase(os.path.realpath(p))


def worktree_plan(repo):
    """Each linked worktree with what the wipe does with it (LIO7-01): "legacy" (the old harness's, under .tmp/rq/wt/,
    removed), "clean" (under .claude/worktrees/, a subagent's isolation copy with no change and a tip that a
    remote-tracking ref holds, so nothing is lost: removed), or "keep" (named, for the merge session to judge).
    -> [(path, branch, action, why)]"""
    wt_root = _real(os.path.join(repo, ".tmp", "rq", "wt"))
    agent_root = _real(os.path.join(repo, ".claude", "worktrees"))
    out = []
    for path, br in extra_worktrees(repo):
        rp = _real(path)
        if rp.startswith(wt_root + os.sep):
            out.append((path, br, "legacy", "the old harness"))
            continue
        if not rp.startswith(agent_root + os.sep):
            out.append((path, br, "keep", "outside .claude/worktrees/"))
            continue
        if not os.path.isdir(path):
            out.append((path, br, "clean", "its folder is gone"))
            continue
        rc, st, _ = git_run(path, "status", "--porcelain")
        tip = git(path, "rev-parse", "HEAD", check=False)
        on_remote = bool(tip) and bool(git(repo, "for-each-ref", "--contains", tip, "--count=1", "--format=%(refname)",
                                           "refs/remotes/", check=False))
        if rc != 0 or st.strip():
            out.append((path, br, "keep", "it has changes or untracked files"))
        elif not on_remote:
            out.append((path, br, "keep", "its tip %s is on no remote-tracking ref" % (tip or "-")[:10]))
        else:
            out.append((path, br, "clean", "no change, and its tip is on %s" % REMOTE))
    return out


def keep_line(path, br, why):
    return ("not removed, a worktree against rule 14: %s [%s] (%s); git worktree remove %s once its commits are pushed "
            "or judged dead, then git branch -D %s" % (path, br, why, path, br))


def find_runs(repo):
    """Every run of the checkout, the legacy ones of .tmp/rq/runs/ included: [(run.json, is_legacy)]."""
    out = [(r, False) for r in units.all_runs(repo)]
    for p in sorted(glob.glob(os.path.join(repo, ".tmp", "rq", "runs", "*", "run.json"))):
        r = read_json(p, None)
        if isinstance(r, dict) and r.get("run"):
            out.append((r, True))
    return out


def classify(repo, runs):
    """Step 1 and 2, holding nothing: ask GitHub (or, with no gh, the ancestry of the run's tip) about each run in
    review. -> {run: (class, run.json, note)} with class done, merged, closed, unfinished or open."""
    import land
    import track
    fetch(repo, [BASE])
    up = upstream(repo)
    have_gh = track.gh(["auth", "status"], repo) is not None
    out = {}
    for r, legacy in runs:
        run, phase = r["run"], r.get("phase")
        if phase in DONE_PHASES:
            out[run] = ("done", r, phase)
            continue
        if phase == "in-review":
            if have_gh:
                st = land.pr_state(r, repo)
                if st == "MERGED":
                    out[run] = ("merged", r, "merged") if land.merged_comment(r, repo) else \
                        ("unfinished", r, "merged, but rq merge did not finish: run scripts/rq merge %s" % run)
                elif st == "CLOSED":
                    out[run] = ("closed", r, "closed without a merge")
                else:
                    out[run] = ("open", r, "pull request %s %s" % (r.get("pr") or "-", st or "not found"))
                continue
            tip = rev(repo, units.ref_of(run))
            if tip and is_ancestor(repo, tip, up):
                out[run] = ("merged", r, "its tip is in %s (no gh)" % short_ref(up))
                continue
        d = os.path.dirname(os.path.join(repo, ".tmp", "rq", "runs", run, "run.json")) if legacy else \
            os.path.join(repo, ".tmp", run)
        if have_gh and phase != "in-review" and not legacy:
            # a land killed after gh pr create left the pull request open and run.json in its old phase; pr_state falls
            # back to the branch name (G3-03)
            st = land.pr_state(r, repo)
            if st == "OPEN":
                out[run] = ("open", r, "its pull request is open although run.json says phase %s (a land was killed after "
                                       "it opened the pull request): scripts/rq land %s finishes it, then merge it"
                            % (phase, run))
                continue
            if st == "MERGED":
                out[run] = ("merged", r, "merged") if land.merged_comment(r, repo) else \
                    ("unfinished", r, "merged, but rq merge did not finish: run scripts/rq merge %s" % run)
                continue
        out[run] = ("open", r, "phase %s, last change %s%s" % (phase, units.last_change(d), " (legacy)" if legacy else ""))
    return out


def wipe(repo=REPO, dry_run=False, drain=False, undrain=False, sessions_done=False):
    import land
    import track
    if undrain:
        if state.control(repo, "drain"):
            state.clear_control(repo, "drain")
            return ["the drain is lifted: research may open runs again; .tmp/ was not wiped"]
        return ["no drain was set"]
    # 1 and 2: ask first, holding nothing
    runs = find_runs(repo)
    cls = classify(repo, runs)
    live_s, idle_s = units.session_folders(repo) if not sessions_done else ([], [])
    known_folders = {f[0] for f in state.folders(repo)}
    blocks = []
    for run, (c, r, note) in sorted(cls.items()):
        if c == "open":
            blocks.append("run %s: %s, pull request %s, issue %s; %s" % (run, r.get("phase"), r.get("pr") or "-",
                                                                     r.get("research_issue") or r.get("issue") or "-", note))
        elif c == "unfinished":
            blocks.append("run %s: %s" % (run, note))
    if not dry_run:
        for run, (c, r, note) in cls.items():
            if c == "closed" and r.get("research_issue"):
                track.release(int(r["research_issue"]), run, "the pull request was closed without a merge", utc_now(),
                              int(SETTINGS.get("claim_hours", 24)), repo, r.get("topic"))
    # 3: one short transaction
    with state.Tx(repo) as db:
        if not dry_run:
            for run, (c, r, note) in cls.items():
                if c in ("merged", "closed", "done"):
                    db.execute("DELETE FROM lease WHERE run = ?", (run,))
                    db.execute("DELETE FROM pending_new WHERE run = ?", (run,))
        from common import now_ts
        now = now_ts()
        for key, run, unit, fence, expires, kind in db.execute("SELECT key, run, unit, fence, expires, kind FROM lease"):
            if kind != "work" or expires >= now:  # a held and a review lease do not expire (G5-02)
                if dry_run and cls.get(run, ("",))[0] in ("merged", "closed", "done"):
                    continue
                blocks.append("lease %s of run %s unit %s (%s%s)" % (
                    key, run, unit, kind, "" if kind != "work" else ", expires %s" % stamp_of(expires)))
        for fid, kind, created, holder, ended in db.execute("SELECT id, kind, created, holder, ended FROM folder"):
            if kind == "session" and not ended and not sessions_done and (fid in live_s or fid not in known_folders):
                blocks.append("session folder .tmp/%s/ is live (last change %s); wait for it, or scripts/rq wipe "
                              "--sessions-done when no research session runs" % (fid, units.last_change(os.path.join(repo, ".tmp", fid))))
        if drain and not dry_run and not db.execute("SELECT 1 FROM control WHERE what = 'drain'").fetchone():
            db.execute("INSERT OR REPLACE INTO control VALUES ('drain', ?, ?, ?)", (os.getpid(), stamp(), "rq wipe --drain"))
        if not blocks and not dry_run:
            db.execute("INSERT OR REPLACE INTO control VALUES ('wiping', ?, ?, ?)", (os.getpid(), stamp(), "rq wipe"))
    t0 = stamp()
    listing = entries(repo)
    wplan = worktree_plan(repo)
    if dry_run:
        return (["would delete .tmp/: %d entr%s, %d file(s), %d bytes" % (len(listing), "y" if len(listing) == 1 else "ies",
                                                                        sum(x[1] for x in listing), sum(x[2] for x in listing))]
                + ["  %s  %d file(s), %d bytes" % x for x in listing]
                + ["would remove worktree %s [%s] (%s)" % (p_, b_, w_) for p_, b_, a_, w_ in wplan if a_ != "keep"]
                + [keep_line(p_, b_, w_) for p_, b_, a_, w_ in wplan if a_ == "keep"]
                + (["blocked by:"] + ["  " + b for b in blocks] if blocks else ["nothing blocks a wipe"]))
    if blocks:
        lines = ["rq wipe refuses: nothing was deleted"] + ["  " + b for b in blocks]
        lines.append("the way out (docs/research-protocol.md section 13): a run in work lands, then you merge it; a pull "
                     "request waits for its merge or close; scripts/rq merge RUN finishes an unfinished merge; scripts/rq "
                     "close RUN --reason \"...\" closes a run whose session died; a live session folder ends or "
                     "--sessions-done%s" % ("; the drain stays until a wipe completes (scripts/rq wipe --undrain lifts it)"
                                            if drain else ""))
        raise Fail("\n".join(lines), 1)
    # 4: a store build holds the build lock: refuse rather than delete its file under it
    lk = FileLock(os.path.join(repo, ".tmp", "fshy", "build.lock"), wait=False, what="the store build")
    try:
        lk.acquire()
        lk.release()
    except Locked as e:
        state.clear_control(repo, "wiping")
        raise Fail("a store build runs (%s); run scripts/rq wipe again when it ends. Nothing was deleted" % e, 1)
    # 5: let go of .tmp/: every connection, process and lock handle of this process
    done_runs = [run for run, (c, r, note) in cls.items() if c in ("merged", "closed", "done")]
    state.close_all()
    units.close_stores()
    try:
        units.fr().close_stores()
    except Exception:
        pass
    close_git()
    os.chdir(repo)
    # 6: the worktrees of the old harness under .tmp/rq/wt/ (a done legacy run, or a gate base), and a subagent's
    # isolation worktree under .claude/worktrees/ that holds nothing a remote lacks; every other one is named (LIO7-01)
    removed_wt, gone_wt, kept_wt = 0, [], []
    for wt, br, action, why in wplan:
        if action == "keep":
            kept_wt.append(keep_line(wt, br, why))
            continue
        rc_wt = git_run(repo, "worktree", "remove", "--force", wt, merge_session=True)[0]
        if action == "legacy":
            removed_wt += 1
        elif rc_wt == 0 or not os.path.isdir(wt):
            gone_wt.append("removed worktree %s [%s] (%s); git branch -D %s deletes its branch" % (wt, br, why, br))
        else:
            kept_wt.append(keep_line(wt, br, "git worktree remove failed: a process may hold a file in it"))
    if removed_wt or gone_wt:
        git(repo, "worktree", "prune", check=False, merge_session=True)
    # 7: what an older wipe could not delete
    for old in glob.glob(os.path.join(repo, ".tmp.wipe-*")):
        _rmtree(old)
    # 8: one rename, then nothing under .tmp/ can be written by a late process
    target = os.path.join(repo, ".tmp.wipe-" + stamp().replace(":", "").replace("-", ""))
    try:
        os.rename(os.path.join(repo, ".tmp"), target)
    except OSError as e:
        state.clear_control(repo, "wiping")
        state.close_all()
        raise Fail("a process holds a file or has its working directory under .tmp/ (%s); stop it and run scripts/rq wipe "
                   "again. Nothing was deleted." % e, 1)
    # 9: a run folder made after the wipe began (a writer that bypassed the registry) goes back, and the wipe refuses
    if os.environ.get("RQ_TEST_PLANT"):
        p = os.path.join(target, os.environ["RQ_TEST_PLANT"], "run.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write('{"run": "%s", "created": "%s", "phase": "open"}\n' % (os.environ["RQ_TEST_PLANT"], stamp()))
    late = []
    for p in glob.glob(os.path.join(target, "*", "run.json")):
        r = read_json(p, {}) or {}
        # stamps have whole seconds: a run made in the second the wipe began is late too (an open run made before
        # the wiping row was written stopped the wipe at step 3)
        if (r.get("created") or "") >= t0:
            late.append(os.path.basename(os.path.dirname(p)))
    if late:
        os.makedirs(os.path.join(repo, ".tmp"), exist_ok=True)
        for fid in late:
            shutil.move(os.path.join(target, fid), os.path.join(repo, ".tmp", fid))
        raise Fail("run folder(s) %s were made after the wipe began, outside the registry (a defect); they are moved back "
                   "into .tmp/, and %s holds the rest. Run scripts/rq wipe again." % (", ".join(late), os.path.basename(target)), 1)
    files, size = _size(target)
    _rmtree(target)
    left = os.path.exists(target)
    if wplan:
        # a worktree of a done legacy run that step 6 could not name is gone with .tmp/: its registration goes too
        git(repo, "worktree", "prune", check=False, merge_session=True)
    # 10: the local refs of the runs that are done
    deleted, kept, tracking = [], [], 0
    import land as _land
    for run in sorted(done_runs):
        what = _land.drop_ref(repo, run)
        if what == "deleted":
            deleted.append(run)
        elif what == "kept":
            kept.append(run)
        if what != "kept":
            # the copy of origin's branch that a fetch or a push left: nothing reads it after the run is done, and one
            # ref per run would otherwise stay in the checkout for good (LIO3-05)
            name = "refs/remotes/%s/rq/%s" % (REMOTE, run)
            old = rev(repo, name)
            if old and git_run(repo, "update-ref", "-d", name, old, merge_session=True)[0] == 0:
                tracking += 1
    out = ["wiped .tmp/: %d entr%s, %d file(s), %d bytes%s" % (
        len(listing), "y" if len(listing) == 1 else "ies", files, size,
        "; %s could not be deleted completely, and the next wipe deletes it" % os.path.basename(target) if left else "")]
    out += ["  %s" % x[0] for x in listing]
    if removed_wt:
        out.append("removed %d worktree(s) of the old harness" % removed_wt)
    out += gone_wt + kept_wt
    out.append("local refs deleted: %s; %d remote-tracking ref(s) of done runs deleted"
               % (", ".join("rq/" + r for r in deleted) or "none", tracking))
    if kept:
        out.append("local refs kept, unpushed work: %s" % ", ".join("rq/" + r for r in kept))
    out.append("next: scripts/rq sync")
    return out


def stamp_of(ts):
    import datetime as dt
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def entries(repo):
    root = os.path.join(repo, ".tmp")
    out = []
    for name in sorted(os.listdir(root)) if os.path.isdir(root) else []:
        p = os.path.join(root, name)
        if os.path.isdir(p):
            n, b = _size(p)
        else:
            n, b = 1, os.path.getsize(p)
        out.append((name, n, b))
    return out


def sync(repo=REPO, repair=False):
    """Fast-forward the research checkout to origin/main at the end of a merge pass, whatever runs are open (runs
    never write the checkout), build the store of the new HEAD once, delete the stores of other commits, delete the
    local intake/fshy-<n> branches that main holds, refresh the index and, when no run is open, run git maintenance.
    The merge session only."""
    import time
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD", check=False)
    if branch != BASE:
        raise Fail("the checkout is on %s, not %s: the research checkout stays on %s" % (branch, BASE, BASE), 1)
    if state.control(repo, "wiping"):
        raise Fail("a wipe runs (scripts/rq status); run sync after it", 1)
    if not has_remote(repo):
        raise Fail("no remote %s to sync with" % REMOTE, 3)
    fetch(repo, [BASE])
    up = upstream(repo)
    head = git(repo, "rev-parse", "HEAD")
    if not is_ancestor(repo, head, up):
        raise Fail("HEAD %s is not in %s: commits that main lacks are in the research checkout. Nothing changed" % (
            head[:10], short_ref(up)), 1)
    changed = status_paths(repo, "--untracked-files=no")
    # an untracked file on a path the fast-forward writes stops it part way; name it before anything moves (LIO3-03)
    incoming = set(git(repo, "diff", "--name-only", "HEAD", up).splitlines()) if head != rev(repo, up) else set()
    blocking = sorted(p for p in git(repo, "ls-files", "--others", "--exclude-standard", check=False).splitlines()
                      if p in incoming)
    if blocking:
        raise Fail("untracked file(s) stand on paths that %s changes (a session wrote outside .tmp/, against AGENTS.md "
                   "section 2 rule 14): %s. Move or delete them, then run scripts/rq sync again. Nothing changed"
                   % (short_ref(up), ", ".join(blocking[:12])), 1)
    if changed and not repair:
        raise Fail("tracked files differ from HEAD (a session broke AGENTS.md section 2 rule 14): %s. Nothing changed"
                   % ", ".join(changed[:12]), 1)
    if changed and repair:
        ok = set(git(repo, "diff", "--name-only", "HEAD", up).splitlines())
        other = [p for p in changed if p not in ok]
        if other:
            raise Fail("--repair refuses: these tracked changes are not a part of the fast-forward: %s" % ", ".join(other[:12]), 1)
        git(repo, "reset", "--hard", up, merge_session=True)
    elif head != rev(repo, up):
        rc, out, err = git_run(repo, "merge", "--ff-only", "-q", up, merge_session=True)
        if rc != 0:
            raise Fail("the fast-forward stopped (git: %s). When git names a file that a process holds open (Windows), "
                       "stop that process and run scripts/rq sync --repair; when it names an untracked file, move it and "
                       "run scripts/rq sync again" % " ".join((err or out).split())[:600], 1)
    new = git(repo, "rev-parse", "HEAD")
    t0 = time.time()
    p = units.fr().ensure_store(repo)
    secs = time.time() - t0
    pruned = units.fr().prune_stores(repo)
    intake = drop_merged_intake(repo, up)
    git(repo, "update-index", "-q", "--refresh", check=False, merge_session=True)
    # git maintenance packs refs (pack-refs --all --prune), which takes each run ref's lock for a moment: an integrate
    # or a land that meets the lock stops. With a run open, the next sync runs it (G6-04).
    opened = live_runs(repo, fresh=True)
    if opened:
        maint = "git maintenance not run: %d run(s) open; the next sync with none open runs it" % len(opened)
    else:
        git(repo, "maintenance", "run", "--auto", check=False, merge_session=True)
        maint = "git maintenance run"
    return ["synced: HEAD %s -> %s" % (head[:10], new[:10]),
            "store %s ready (%.1f s); %d store file(s) of other commits deleted" % (os.path.relpath(p, repo).replace("\\", "/"),
                                                                                  secs, pruned),
            "local intake branches main holds, deleted: %s" % (", ".join(intake) or "none"), maint]


def drop_merged_intake(repo, up):
    """Delete each local refs/heads/intake/* whose tip main holds: its queue item merged, and the ref would make
    `rq review` report it as not merged and `rq intake` refuse a reopened report (G6-03). Compare-and-set on the old
    value, as land.drop_ref does for a run ref."""
    out = []
    for ln in git(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/intake/", check=False).splitlines():
        name, _, old = ln.strip().partition(" ")
        if name and old and is_ancestor(repo, old, up) and \
                git_run(repo, "update-ref", "-d", name, old, merge_session=True)[0] == 0:
            out.append(name[len("refs/heads/"):])
    return out
