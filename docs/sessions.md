# Sessions

## Starting

Read `AGENTS.md` first. The work queue is the open issues labelled `rq:research`; `scripts/rq issues` lists
them. Claim one with `scripts/rq open KIND TOPIC "DETAILS" --issue N`.

## Ending

The pull request is the handover. `scripts/rq land RUN --meets N,N` opens it. A run does not edit `BRIEF.md`; its
handover is the pull request body and the follow-up issue that `scripts/rq merge` files.

## Resuming

A session that stops early leaves its run branch, and its pull request when it landed. `scripts/rq review`
lists the pull requests that wait for a merge session. A run whose session died with no pull request is closed
with `scripts/rq close RUN --reason "..."`.
