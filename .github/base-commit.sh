#!/bin/sh
# The commit the gate compares a pushed or dispatched head with, printed on stdout. The rule: a push to the default
# branch compares with the head it replaced; a push to any other branch (a run branch) compares with the merge-base of
# the default branch and the head, so the comparison covers only the branch's own change. A dispatch names its base;
# when it names none, the same rule applies.
#
# The inputs come from the workflow: INPUT_BASE (a dispatch's base, 40 hex or empty), BEFORE (github.event.before),
# GITHUB_REF, GITHUB_EVENT_NAME. A base that is not a commit of this clone is never used, and HEAD is never a base:
# a check against itself proves nothing. A push to the default branch with no usable base fails here instead of
# comparing with its own parent, which would hide a check that an earlier commit of the same push broke.
set -u
base=${INPUT_BASE:-}
head=$(git rev-parse --verify --quiet HEAD) || { echo "no HEAD: not a checkout" >&2; exit 1; }
main=$(git rev-parse --verify --quiet refs/remotes/origin/main) || main=""

is_commit() {
  [ -n "$1" ] && git cat-file -e "$1^{commit}" 2> /dev/null
}

on_main=0
[ "${GITHUB_REF:-}" = "refs/heads/main" ] && on_main=1

if ! is_commit "$base"; then
  base=""
  if [ "$on_main" = 1 ] && [ "${GITHUB_EVENT_NAME:-}" = push ] && is_commit "${BEFORE:-}"; then
    base=$BEFORE
  fi
fi
if [ -z "$base" ] && [ "$on_main" = 0 ] && is_commit "$main"; then
  # a branch's own change: its merge-base with the default branch, read without a pager and never multi-line
  base=$(git merge-base "$main" "$head" 2> /dev/null | head -n 1)
fi
if [ -z "$base" ] && [ "$on_main" = 0 ]; then
  # a clone with no origin/main (a fetch depth that dropped it): the commit before the head is the branch's change
  base=$(git rev-parse --verify --quiet "$head~1" || true)
fi
if ! is_commit "$base"; then
  echo "no base commit: a push to the default branch must name the commit before it (github.event.before), and this" >&2
  echo "clone holds no such commit; a shallow clone cannot compare the push, so the run fails rather than pass." >&2
  exit 1
fi
if [ "$base" = "$head" ]; then
  echo "the head $head is its own base: the branch carries no commit that main lacks, so there is nothing to compare" >&2
  exit 1
fi
printf '%s\n' "$base"
