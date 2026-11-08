#!/bin/sh
# The heavy checks of one commit of this repository, as the public repository's workflow runs them
# (settings.json ci_repo and ci_workflow; scripts/research/ci.py). Its log is public, so each check writes its
# output to a file under $CI_LOGS and this prints one line per check: PASS NAME, FAIL NAME or SKIP NAME. The gate
# comparison also prints each gate check as "NAME base X head Y", without the detail. Never print a check's output
# here: a record, a quote or a path in a public log is a leak. A merge session reproduces a failed check in its own
# clone (for the gate: scripts/rq gatecmp --base origin/main).
#
# usage: sh scripts/research/ci-checks.sh linux|windows|parity|lock BASE
#   linux    the gate comparison against BASE, the full render check, the selftests, and the harness selftest when
#            the harness changed against BASE
#   windows  the harness's Windows cases, when the harness changed against BASE
#   parity   fr's twin of the public Worker (needs FSHY_PUBLIC, a checkout of the pinned public commit)
#   lock     scripts/fshy/public.lock holds the newest public change of the Worker rules
# Exit 0 when every check passed or was skipped.
set -u
mode=${1:?usage: ci-checks.sh linux|windows|parity|lock BASE}
base=${2:-}
CI_LOGS=${CI_LOGS:-${RUNNER_TEMP:-/tmp}/ci-logs}
mkdir -p "$CI_LOGS"
PY=${PYTHON:-python}
fail=0

check() {
  name=$1
  shift
  if "$@" > "$CI_LOGS/$name.log" 2>&1; then
    echo "PASS $name"
  else
    echo "FAIL $name"
    fail=1
  fi
}

# the paths whose change runs the harness selftest; the same list as the gate's own job had. baseline.tsv is data
# that every run's check --prune rewrites, not harness code, so a run that only prunes it runs no harness case
harness_changed() {
  git diff --name-only "$base" HEAD | grep -v '^scripts/research/baseline\.tsv$' |
    grep -qE '^scripts/research/|^scripts/fshy/(fr|build)\.py$|^scripts/report/render\.py$|^scripts/broker/broker\.sh$|^scripts/dossier/(validate\.py|schema\.json)$|^\.github/workflows/'
}

case $mode in
  linux)
    [ -n "$base" ] && git cat-file -e "$base^{commit}" 2>/dev/null || { echo "FAIL base (no base commit given or fetched)"; exit 1; }
    if "$PY" scripts/research/rq.py gatecmp --base "$base" > "$CI_LOGS/gate.log" 2>&1; then g=0; else g=1; fi
    # each gate check's name and its two results; the detail after them stays in the file
    awk '$2 == "base" && $4 == "head" { print $1, $2, $3, $4, $5 }
         /^GREEN against / { print "GREEN against", $3 }
         /^RED: newly failing / { print }' "$CI_LOGS/gate.log"
    if [ "$g" = 0 ]; then echo "PASS gate-comparison"; else echo "FAIL gate-comparison"; fail=1; fi
    check render "$PY" scripts/report/render.py --check
    check gate-selftest sh scripts/gate.sh --selftest
    check projection-selftest "$PY" scripts/fshy/test_projection.py
    check price-selftest "$PY" scripts/fshy/test_prices.py
    check derive-selftest "$PY" scripts/fshy/test_derive.py
    check entity-selftest "$PY" scripts/fshy/test_entity.py
    if harness_changed; then
      check harness-selftest "$PY" scripts/research/test_rq.py
    else
      echo "SKIP harness-selftest (the harness did not change)"
    fi
    # a change of the pin of the public Worker rules is checked against the public repository at once
    if git diff --name-only "$base" HEAD | grep -qE '^scripts/fshy/(public\.lock|check_lock_fresh\.py)$'; then
      check lock-selftest "$PY" scripts/fshy/check_lock_fresh.py --selftest
      check lock-fresh "$PY" scripts/fshy/check_lock_fresh.py
    fi
    ;;
  windows)
    [ -n "$base" ] && git cat-file -e "$base^{commit}" 2>/dev/null || { echo "FAIL base (no base commit given or fetched)"; exit 1; }
    if harness_changed; then
      # one check per case, so the public log names the case that failed and nothing more
      for c in primitives_case store_lock_case lock_case claim_case wipe_case no_cap_case one_tree_load_case; do
        check "harness-windows.$c" "$PY" scripts/research/test_rq.py --only "$c"
      done
    else
      echo "SKIP harness-windows (the harness did not change)"
    fi
    ;;
  parity)
    [ -n "${FSHY_PUBLIC:-}" ] || { echo "FAIL parity (FSHY_PUBLIC is not set)"; exit 1; }
    check parity env FSHY_REQUIRE_PARITY=1 "$PY" scripts/fshy/test_fr.py
    ;;
  lock)
    check lock-selftest "$PY" scripts/fshy/check_lock_fresh.py --selftest
    check lock-fresh "$PY" scripts/fshy/check_lock_fresh.py
    ;;
  *)
    echo "usage: ci-checks.sh linux|windows|parity|lock BASE" >&2
    exit 2
    ;;
esac
exit $fail
