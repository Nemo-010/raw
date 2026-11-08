#!/bin/sh
# The commit the gate compares a pushed or dispatched head with, printed on stdout. The rule: a push to the default
# branch compares with the head it replaced, and a push to any other branch (a run branch) compares with the
# merge-base of the default branch and the head, so the comparison covers only the branch's own change. A dispatch
# names its base; when it names none, the same rule applies.
#
# The inputs come from the workflow: INPUT_BASE (a dispatch's base, 40 hex or empty), BEFORE (github.event.before),
# GITHUB_REF, GITHUB_EVENT_NAME. A base that is not a commit of this clone is never used: a shallow or force-pushed
# branch falls back to the rule's next candidate, and never to HEAD, which would compare a head with itself.
set -u
base=${INPUT_BASE:-}
main=$(git rev-parse --verify --quiet refs/remotes/origin/main || git rev-parse --verify --quiet HEAD)

is_commit() {
  [ -n "$1" ] && git cat-file -e "$1^{commit}" 2> /dev/null
}

if ! is_commit "$base"; then
  base=""
  if [ "${GITHUB_EVENT_NAME:-}" = push ] && [ "${GITHUB_REF:-}" = "refs/heads/main" ] && is_commit "${BEFORE:-}"; then
    base=$BEFORE
  fi
fi
if [ -z "$base" ] && [ "${GITHUB_REF:-}" != "refs/heads/main" ] && is_commit "$main"; then
  base=$(git merge-base "$main" HEAD 2> /dev/null)
fi
if ! is_commit "$base"; then
  base=$(git rev-parse --verify --quiet HEAD~1) || base=$(git rev-list --max-parents=0 HEAD)
fi
if ! is_commit "$base"; then
  echo "no base commit: the clone has no history to compare with" >&2
  exit 1
fi
printf '%s\n' "$base"
