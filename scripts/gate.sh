#!/usr/bin/env bash
# Invoked as `sh gate.sh` on a system whose sh is not bash (dash on Debian and Ubuntu): re-run under bash.
# A shell reads a script one command at a time, so this line runs before any bash-only syntax is parsed.
if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi
# gate.sh — the definition of done, mechanically.
#
# PURPOSE
#   One command that answers "is this repository internally coherent?" and names
#   the defect when it is not. Six checks, each blind to the class the others catch.
#
# WHY IT EXISTS
#   Every rule in AGENTS.md that a human is asked to remember is a rule that will
#   eventually be forgotten on a Friday. The gate makes the checkable subset of
#   them non-optional: schema, drift, links, attribution, units, and a clean tree.
#   A gate that has never failed proves nothing, so fixtures/ carries one
#   deliberately broken case per check and --selftest runs them all.
#
# DEPENDENCIES
#   bash, coreutils, grep, sed, awk, find. Python only through the sibling scripts
#   (verify-dossier.py, staleness.py). No network. No jq, no ripgrep.
#
# OUTPUT
#   One line per check on stdout, then a summary. Machine-readable form with
#   --json (one JSON object). Human form is the default because this is the
#   command a person runs before committing.
#
# EXIT CODES  (repository map, scripts/README.md)
#   0  every check passed, or a check SKIPPED with a stated reason (never under --strict)
#   1  at least one check FAILED; the failing check names the defect
#   2  usage error: bad --root, unknown option
#   3  environment wrong: no Python 3.9 or later (python3 or python, or $PYTHON), or no grep or find
#   4  reserved for a broker/network refusal; the gate never uses it
#
# --strict turns a SKIP into a FAIL. CI should pass --strict, because there a
# missing tool means the install broke, not that the check was inapplicable.
# scripts/rq gatecmp counts a SKIP on the branch as not green, with or without it.
#
# --as-of YYYY-MM-DD runs the staleness check as of that day. staleness is the one
# check that depends on the clock: a clean tree turns red as its records age.
#
# EXAMPLES
#   sh gate.sh --root .              # the pre-commit run
#   sh gate.sh --root . --strict     # the CI run
#   sh gate.sh --root . --check units,attribution
#   sh gate.sh --selftest            # proves the gate fails on broken fixtures
#   sh gate.sh --root . --json
#   sh gate.sh --root . --as-of 2026-10-27 --check staleness

set -uo pipefail
export PYTHONIOENCODING=utf-8

HERE="$(cd "$(dirname "$0")" && pwd)"
# The interpreter: $PYTHON when set, else the first of python3 and python that runs Python 3.9 or later.
# Debian, Ubuntu and macOS ship only python3; Windows can have a python3 that is a Store stub and does not
# run. A $PYTHON that does not run is not replaced. A missing interpreter is exit 3 below, never a quiet
# SKIP of every Python check.
find_python() {
  local c cands="python3 python"
  [ -n "${PYTHON:-}" ] && cands="$PYTHON"
  for c in $cands; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
      printf '%s' "$c"; return
    fi
  done
}
PY="$(find_python)"

ROOT=""
STRICT=0
JSON=0
CHECK_SET=""
SELFTEST=0
QUIET=0
DETECT_ONLY=""
AS_OF=""

usage() { sed -n '2,48p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="${2:?--root needs a path}"; shift 2 ;;
    --strict) STRICT=1; shift ;;
    --json) JSON=1; QUIET=1; shift ;;
    --quiet|-q) QUIET=1; shift ;;
    --check) CHECK_SET="${2:?--check needs a list}"; shift 2 ;;
    --as-of) AS_OF="${2:?--as-of needs YYYY-MM-DD}"; shift 2 ;;
    --detect-only) DETECT_ONLY="${2:?}"; shift 2 ;;
    --selftest) SELFTEST=1; shift ;;
    -h|--help) usage ;;
    *) printf 'gate: unknown argument %s\n' "$1" >&2; exit 2 ;;
  esac
done

# AGENTS.md section 2 rule 14: research runs with 30 or more agents in one checkout, so the research checkout runs no
# gate. The gate runs once, in CI on the pushed head ($CI is set there: this repository's Actions), or in an own clone. --selftest builds only
# scratch trees and is not refused.
if [ "$SELFTEST" -eq 0 ] && [ -z "${CI:-}" ] && [ -n "$ROOT" ] && [ -e "$ROOT/.git" ]; then
  case "$(git -C "$ROOT" config --get rq.researchCheckout 2>/dev/null)" in
    [Tt][Rr][Uu][Ee])
      printf '%s\n' "gate: this is the research checkout (git config rq.researchCheckout is true). A research agent never runs the gate: it runs once, in CI on the pushed head (scripts/rq ci RUN), or in an own clone (AGENTS.md section 2 rule 14)." >&2
      exit 2 ;;
  esac
fi

# ---------------------------------------------------------------- check list --

ALL_CHECKS="schema staleness binding links attribution units tree rellinks sources projection selfhosted contradictions"

check_wanted() {
  [ -z "$CHECK_SET" ] && return 0
  case ",$CHECK_SET," in *",$1,"*) return 0 ;; esac
  return 1
}

RESULTS=""
N_PASS=0; N_FAIL=0; N_SKIP=0

record() {
  # record <name> <status> <detail>
  local name="$1" status="$2"; shift 2
  local detail="$*"
  RESULTS="${RESULTS}${name}|${status}|${detail}
"
  case "$status" in
    PASS) N_PASS=$((N_PASS+1)) ;;
    FAIL) N_FAIL=$((N_FAIL+1)) ;;
    SKIP) N_SKIP=$((N_SKIP+1)) ;;
  esac
  if [ "$QUIET" = "0" ]; then
    printf '%-4s %-13s %s\n' "$status" "$name" "$detail"
  fi
}

# ------------------------------------------------------------------- checks --

need_python() {
  [ -n "$PY" ] || return 1
  command -v "$PY" >/dev/null 2>&1 || return 1
  return 0
}

check_schema() {
  local schema="$ROOT/scripts/dossier/schema.json"
  [ -f "$schema" ] || schema="$ROOT/dossier.schema.json"
  local validator="$HERE/dossier/validate.py"
  [ -f "$validator" ] || validator="$HERE/verify-dossier.py"
  local dossier_dir="$ROOT/dossier"

  [ -d "$dossier_dir" ] || { record schema SKIP "no dossier/ directory"; return; }
  # A dossier tree that only holds its README has nothing to check yet.
  local njson
  njson="$(find "$dossier_dir" -name '*.json' -not -name '*.generated.json' 2>/dev/null | wc -l | tr -d ' ')"
  [ "$njson" = "0" ] && { record schema SKIP "dossier/ holds no .json records yet"; return; }

  [ -f "$schema" ] || { record schema FAIL "scripts/dossier/schema.json missing"; return; }
  [ -f "$validator" ] || { record schema SKIP "verify-dossier.py not beside gate.sh"; return; }
  need_python || { record schema SKIP "python not found"; return; }

  local out rc
  out="$("$PY" "$validator" --schema "$schema" "$dossier_dir" 2>&1)"; rc=$?
  if [ "$rc" = "0" ]; then
    record schema PASS "$njson records valid"
  elif [ "$rc" = "2" ] || [ "$rc" = "3" ]; then
    record schema SKIP "validator could not run (exit $rc)"
  else
    local first
    first="$(printf '%s' "$out" | "$PY" -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception: print("unparseable validator output"); raise SystemExit
e=d.get("errors") or []
print("%d defects; first: %s %s %s" % (len(e), e[0].get("file","?"), e[0].get("path",""),
      e[0].get("message","")) if e else "validator failed")' 2>/dev/null)"
    record schema FAIL "${first:-validator failed}"
  fi
}

check_staleness() {
  local script="$HERE/dossier/staleness.py"
  [ -f "$script" ] || script="$HERE/staleness.py"
  local dossier_dir="$ROOT/dossier"
  [ -d "$dossier_dir" ] || { record staleness SKIP "no dossier/ directory"; return; }
  local njson
  njson="$(find "$dossier_dir" -name '*.json' -not -name '*.generated.json' 2>/dev/null | wc -l | tr -d ' ')"
  [ "$njson" = "0" ] && { record staleness SKIP "dossier/ holds no .json records yet"; return; }
  [ -f "$script" ] || { record staleness SKIP "staleness.py not beside gate.sh"; return; }
  need_python || { record staleness SKIP "python not found"; return; }

  local out rc
  if [ -n "$AS_OF" ]; then
    out="$("$PY" "$script" "$dossier_dir" --summary --as-of "$AS_OF" 2>&1)"; rc=$?
  else
    out="$("$PY" "$script" "$dossier_dir" --summary 2>&1)"; rc=$?
  fi
  if [ "$rc" = "0" ]; then
    record staleness PASS "$(printf '%s' "$out" | grep '^TOTALS' | tr -s ' ')"
  elif [ "$rc" = "3" ]; then
    record staleness SKIP "policy unreadable"
  else
    # Read the script's own totals line. Summing the per-topic rows instead
    # double-counted once the summary grew a TOTALS line, and it could not
    # separate "past its window" from "re-dated without re-checking".
    local stale_n bulk_n undated_n
    stale_n="$(printf '%s' "$out" | sed -n 's/^TOTALS .*stale=\([0-9]*\).*/\1/p')"
    bulk_n="$(printf '%s' "$out" | sed -n 's/^TOTALS .*bulk=\([0-9]*\).*/\1/p')"
    undated_n="$(printf '%s' "$out" | sed -n 's/^TOTALS .*undated=\([0-9]*\).*/\1/p')"
    if [ -z "$stale_n" ]; then
      stale_n="$(printf '%s' "$out" | sed -n 's/.*stale=\([0-9]*\).*/\1/p' | awk '{s+=$1} END{print s+0}')"
    fi
    record staleness FAIL "${stale_n:-some} record(s) past their class or topic window (${bulk_n:-0} re-dated without re-checking, ${undated_n:-0} with undated evidence)"
  fi
}

check_binding() {
  # METHODOLOGY.md section 4.3 and the definition of done require the record to
  # name the constraint that fails first. The schema keeps `binding` optional so a
  # migrated record can land; this check is what makes it required where it counts.
  local dossier_dir="$ROOT/dossier"
  [ -d "$dossier_dir" ] || { record binding SKIP "no dossier/ directory"; return; }
  need_python || { record binding SKIP "python not found"; return; }
  local out rc
  out="$("$PY" - "$dossier_dir" <<'PYEOF'
import glob, json, os, sys
root = sys.argv[1]
missing, total = [], 0
for p in sorted(glob.glob(os.path.join(root, "**", "*.json"), recursive=True)):
    if p.endswith(".generated.json"):
        continue
    try:
        rec = json.load(open(p, encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(rec, dict) or "candidates" in rec:
        continue
    if rec.get("confidence") not in ("measured", "documented"):
        continue
    total += 1
    if not rec.get("binding"):
        missing.append(os.path.basename(p)[:-5])
print(json.dumps({"total": total, "missing": missing}))
PYEOF
)"
  rc=$?
  if [ "$rc" != "0" ]; then record binding SKIP "binding scan could not run"; return; fi
  local n m names
  n="$("$PY" -c 'import json,sys; print(json.load(sys.stdin)["total"])' <<< "$out" 2>/dev/null)"
  m="$("$PY" -c 'import json,sys; d=json.load(sys.stdin); print(len(d["missing"]))' <<< "$out" 2>/dev/null)"
  names="$("$PY" -c 'import json,sys; d=json.load(sys.stdin); print(" ".join(d["missing"][:4]))' <<< "$out" 2>/dev/null)"
  if [ "${n:-0}" = "0" ]; then
    record binding SKIP "no measured or documented records yet"
  elif [ "${m:-0}" -gt 0 ]; then
    record binding FAIL "$m of $n measured/documented record(s) name no binding constraint: $names"
  else
    record binding PASS "every measured/documented record names its binding constraint ($n records)"
  fi
}

check_links() {
  local docs="$ROOT/docs"
  local dossier_dir="$ROOT/dossier"
  [ -d "$docs" ] || { record links SKIP "no docs/ directory"; return; }
  local readme="$docs/README.md"
  local problems=0 detail="" advisory_links=0

  # (1) every doc referenced from docs/README.md exists.
  if [ -f "$readme" ]; then
    local targets t clean
    targets="$(sed -n 's/.*](\([^)]*\)).*/\1/p' "$readme" | sort -u)"
    while IFS= read -r t; do
      [ -z "$t" ] && continue
      case "$t" in http*|\#*|mailto:*) continue ;; esac
      clean="${t%%#*}"
      [ -z "$clean" ] && continue
      case "$clean" in
        /*) [ -e "$clean" ] || { problems=$((problems+1)); detail="${detail}missing:${t} "; } ;;
        *)  [ -e "$docs/$clean" ] || [ -e "$ROOT/$clean" ] || \
              { problems=$((problems+1)); detail="${detail}missing:${t} "; } ;;
      esac
    done <<< "$targets"
  fi

  # (2) every VERIFIED dossier record is cited by some document.
  # Set arithmetic with two sorts and one comm, not a grep per record: the
  # per-record form spawned two processes per dossier and took minutes once the
  # tree passed a few thousand records.
  #
  # Not every record needs a document. The catalogue's long tail exists to be
  # searched, not read: a provider graded `reported` that nobody would act on
  # tonight belongs in the dossier and not in a table. What must be cited is a
  # record whose evidence we stand behind, because an uncited `measured` or
  # `documented` claim has no reader to correct it and no table that would
  # contradict it. So: verified orphans fail, long-tail orphans are counted.
  if [ -d "$dossier_dir" ] && need_python; then
    local tmp_recs
    tmp_recs="$(mktemp)"
    find "$dossier_dir" -name '*.json' -not -name '*.generated.json' 2>/dev/null \
      | sed 's|.*/||; s|\.json$||' | grep -vE '^(_index|schema)' | sort -u > "$tmp_recs"
    local cls
    cls="$("$PY" - "$docs" "$dossier_dir" "$tmp_recs" <<'PYEOF'
import json, os, re, sys

docs_dir, dossier_dir, slug_file = sys.argv[1:4]
slugs = [ln.strip() for ln in open(slug_file, encoding="utf-8") if ln.strip()]

text = []
for dirpath, _, files in os.walk(docs_dir):
    for name in files:
        if name.endswith(".md"):
            try:
                with open(os.path.join(dirpath, name), encoding="utf-8",
                          errors="replace") as fh:
                    text.append(fh.read())
            except OSError:
                pass
text = "\n".join(text).lower()

# A record is cited when its slug appears as a whole token. The extractor this
# replaced was `grep -oE '[a-z0-9]+(-[a-z0-9]+)+'`, which requires a hyphen, so
# 689 single-word slugs could never be cited however often a document named
# them. One pass into a token set, then a set lookup: a regex per slug over the
# whole corpus is 2,300 full scans.
cited = set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text))

paths = {}
for topic in sorted(os.listdir(dossier_dir)):
    tdir = os.path.join(dossier_dir, topic)
    if not os.path.isdir(tdir):
        continue
    for name in os.listdir(tdir):
        if name.endswith(".json") and not name.endswith(".generated.json"):
            paths.setdefault(name[:-5], os.path.join(tdir, name))

verified, tail, unreadable = [], 0, 0
for slug in slugs:
    if slug in cited:
        continue
    path = paths.get(slug)
    if path is None:
        unreadable += 1
        continue
    try:
        rec = json.load(open(path, encoding="utf-8"))
    except Exception:
        unreadable += 1
        continue
    if rec.get("confidence") in ("measured", "documented"):
        verified.append(slug)
    else:
        tail += 1

print("%d %d %d %s" % (len(verified), tail, unreadable, " ".join(verified[:3])))
PYEOF
)"
    local nv nt nu names
    nv="$(printf '%s' "$cls" | cut -d' ' -f1)"
    nt="$(printf '%s' "$cls" | cut -d' ' -f2)"
    nu="$(printf '%s' "$cls" | cut -d' ' -f3)"
    names="$(printf '%s' "$cls" | cut -d' ' -f4-)"
    if [ "${nv:-0}" -gt 0 ]; then
      problems=$((problems+nv))
      detail="${detail}uncited-verified-record:${names} "
    fi
    [ "${nt:-0}" -gt 0 ] && advisory_links="${nt}"
    [ "${nu:-0}" -gt 0 ] && advisory_links="$((advisory_links+nu))"
    rm -f "$tmp_recs"
  fi

  if [ "$problems" = "0" ]; then
    record links PASS "docs/README.md references resolve; every verified record is cited (${advisory_links:-0} long-tail record(s) uncited, as intended)"
  else
    record links FAIL "$problems problem(s): $(printf '%s' "$detail" | cut -c1-160)"
  fi
}

# Banned words, chosen for one reason each: they are the register the operator
# forbids, or they are a claim word doing the work evidence should do.
BANNED_WORDS="revolutionary|game-chang|game chang|unparalleled|seamless|seamlessly|cutting-edge|cutting edge|world-class|best-in-class|effortless|effortlessly|leverage the power|robust solution|exciting"

check_attribution() {
  local docs="$ROOT/docs"
  [ -d "$docs" ] || { record attribution SKIP "no docs/ directory"; return; }
  local hits=0 detail="" banned=0 bdetail=""

  # One recursive grep per rule, not one per file. The per-file form spawned a
  # grep per document and dominated the gate's runtime on a large tree.
  local at bw
  # An author credit for this repository's own text, the shapes .githooks/commit-msg refuses in a commit: a credit
  # trailer; a line that is only a credit ("Built using GPT-4o", "Generated with [Claude Code](...)", "Code
  # written by Codex"); a sentence whose subject is this document or the change ("The fix, written with Claude,
  # adds a test."); and the robot emoji of a tool's footer. A sentence about a vendor's product is a finding and
  # passes ("Answers are generated by Gemini", "The page was reviewed by OpenAI"). The selftest case 14 holds both.
  local names='(claude|anthropic|chatgpt|gpt[-.0-9a-z]*|openai|gemini|bard|copilot|llama[-.0-9a-z]*|mistral|codex|cursor|kimi|opus|sonnet|haiku|an? (ai|llm)|ai (assistant|agent|model))([^[:alnum:]]|$)'
  local verbs='(generated|written|made|assisted|drafted|authored|co-?authored|reviewed|created|produced|built|powered|composed|coded|edited)'
  local preps='(with|by|using|via|through)'
  local self='(this[[:space:]]+(document|file|page|report|text|section|note|summary|record|commit|change|patch|fix)|the[[:space:]]+(commit|change|patch|fix))'
  at="$( { grep -rnEi --include='*.md' \
    "^[[:space:]>*-]*(co-authored-by|assisted-by|generated-by|generated-with|written-by|drafted-by|made-with|helped-by|ai-assisted-by)[[:space:]]*:|^[[:space:]>*-]*(reviewed-by|signed-off-by|tested-by|acked-by|suggested-by)[[:space:]]*:.*(^|[^[:alnum:]])$names|^[[:space:]>*_-]*(<[a-z]+>)?[[:space:]]*(($self|code|text|content|docs)[[:space:]]+((was|is|were|are|has been|have been)[[:space:]]+)?)?$verbs[[:space:]]+$preps[[:space:]]+(the[[:space:]]+)?((help|assistance|aid)[[:space:]]+of[[:space:]]+)?[[(]?$names([[:space:]]*[^[:space:],;]+){0,3}[[:space:]]*\$|(^|[^[:alnum:]])$self[[:space:]]*,?[[:space:]]+((was|is|were|are|has been|have been)[[:space:]]+)?([a-z]+ly[[:space:]]+)?$verbs[[:space:]]+$preps[[:space:]]+(.{0,40}[^[:alnum:]])?$names|as an ai (language )?model" \
    "$docs" 2>/dev/null
    grep -rnF --include='*.md' "$(printf '\360\237\244\226')" "$docs" 2>/dev/null; } | head -5)"
  if [ -n "$at" ]; then
    hits="$(printf '%s\n' "$at" | wc -l | tr -d ' ')"
    detail="$(printf '%s' "$at" | sed "s|$ROOT/||" | cut -c1-150 | tr '\n' ' ')"
  fi

  bw="$(grep -rnEi --include='*.md' "$BANNED_WORDS" "$docs" 2>/dev/null | head -5)"
  if [ -n "$bw" ]; then
    banned="$(printf '%s\n' "$bw" | wc -l | tr -d ' ')"
    bdetail="$(printf '%s' "$bw" | sed "s|$ROOT/||" | cut -c1-150 | tr '\n' ' ')"
  fi

  # Rule 9: never recommend acquiring hardware. The shape is an acquisition verb in a
  # sentence that also prices or advises, with no negation and no quote. A one-line
  # regex here was tried and fired on "keep-alive box", "build a box" and "own the
  # arithmetic", so the rule lives in a script with a fixture, not in this function.
  local own="" own_n=0
  if [ -f "$HERE/own-hardware.py" ] && need_python; then
    own="$("$PY" "$HERE/own-hardware.py" --root "$docs" 2>/dev/null | grep -v "recommendation(s) to acquire" | head -3)"
    own_n="$("$PY" "$HERE/own-hardware.py" --root "$docs" --quiet 2>/dev/null | sed "s/[^0-9].*//" | head -1)"
  fi
  if [ -n "$own" ] && [ "${own_n:-0}" != "0" ]; then
    banned=$((banned + ${own_n:-0}))
    bdetail="${bdetail}own-hardware:$(printf "%s" "$own" | tr "
" " " | cut -c1-170) "
  fi

  if [ "$hits" -gt 0 ]; then
    record attribution FAIL "AI-attribution line in ${hits} place(s): ${detail}"
  elif [ "$banned" -gt 0 ]; then
    record attribution FAIL "${banned} forbidden phrase(s): ${bdetail}"
  else
    record attribution PASS "no AI attribution, no marketing words, no own-hardware recommendation"
  fi
}

check_units() {
  local docs="$ROOT/docs"
  [ -d "$docs" ] || { record units SKIP "no docs/ directory"; return; }
  local kb=0 tc=0 detail=""

  # "KB|MB|GB|TB used where BINARY UNITS ARE REQUIRED" is the rule; the hard part is
  # the qualifier. Most cloud specs really are decimal — "12 GB of RAM" and "500 GB
  # a month" are the vendor's own phrasing — so a blanket grep is wrong, and a gate
  # that fires on legitimate prose is a gate somebody switches off. Four
  # contexts remain, each one a place where the binary reading is the correct one:
  #
  # 1. a binary multiple wearing a decimal suffix: "1024 GB" is 1 TiB misnamed.
  # 2. a per-object cap: "25 MB per file" is the exact confusion that cost a wave,
  #    because 25 MiB and not 25 MB is the Pages limit that actually binds.
  # 3. a MEASURED rate: "19.7 MB/s" is a byte count divided by a second, so it is
  #    MiB/s; the corpus compares these numbers across hosts, and mixing the two
  #    readings is how a 5% error becomes a wrong ranking.
  # 4. kbps, which is neither kbit/s nor KiB/s.
  #
  # Exemptions, each earned by a false positive on the first full-repo run:
  #   price   "USD 10 per GB", "EUR 5/TB" — a rate, decimal by definition
  #   quote   a line carrying a URL or a read date is evidence about a source
  #   code    an inline code span is quoting or teaching the rule
  #
  # One awk pass, because a sed+grep per file took over a minute under Git Bash.
  local out
  out="$(awk '
    /^$/ { }
    {
      line = $0
      gsub(/`[^`]*`/, "", line)
      if (line ~ /https?:\/\/|read 20[0-9][0-9]-|\((measured|documented|reported|inferred|unverified), ?20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\.?\)|\(, ?20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\.?\)|\(20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\)/) next
      price = (line ~ /(EUR|USD|GBP|CHF|€|\$|per TB|Per TB|\/TB|per GB|Per GB|\/GB|GB-month|GB-months|GB-hour|GB-hours|GB-s\b|GB-seconds)/)
      bad = 0
      adv = ""
      # 1. binary multiple with a decimal suffix
      if (line ~ /(^|[^0-9])(1024|2048|4096)[ \t]?(KB|MB|GB|TB)([^A-Za-z]|$)/) bad = 1
      # 2. per-object cap. ADVISORY, not a failure. conventions 4.1 says a decimal
      #    unit is correct when the provider states one, and most per-file caps are
      #    the decimal figure the vendor published; converting them would misquote
      #    the source, which is worse than the defect this check prevents. The
      #    author own arithmetic is still caught by rule 1, which has no ambiguity.
      if (!price && line ~ /[0-9][0-9.,]*[ \t]?(KB|MB|GB|TB)[ \t]?(per|\/) ?(file|object|record|upload|asset)/) adv = adv " " FILENAME ":" FNR
      # 3. a rate WE measured is a byte count over a second, so it is MiB/s. A
      #    rate a vendor states as "9.7 MB/s" is decimal and is not ours to convert:
      #    only a line that reports our own probe is a defect.
      if (!bad && line ~ /(measured|probe|probed|throughput|benchmark)/ && line ~ /[0-9][0-9.,]*[ \t]?(KB|MB|GB|TB)\/[[:space:]]?(s|sec|second)([^A-Za-z]|$)/) bad = 1
      # 4. kbps, and a local clock time
      if (!bad && line ~ /(^|[^A-Za-z])[0-9]+[ \t]?kbps/) { printf "TSR %s:%d: %s\n", FILENAME, FNR, $0; next }
      if (!bad && line ~ /(^|[^0-9])[0-9]{1,2}:[0-9]{2}[ \t]?(AM|PM)/) { printf "TSR %s:%d: %s\n", FILENAME, FNR, $0; next }
      if (bad) printf "%s:%d: %s\n", FILENAME, FNR, $0
      if (adv != "") { printf "ADV%s\n", adv; adv = "" }
    }
  ' $(find "$docs" -name '*.md' -type f 2>/dev/null | sort) 2>/dev/null)"

  if [ -n "$out" ]; then
    kb="$(printf '%s\n' "$out" | grep -v -e '^TSR ' -e '^ADV' | grep -c . | tr -d ' ')"
    tc="$(printf '%s\n' "$out" | grep -c '^TSR ' | tr -d ' ')"
    ac="$(printf '%s\n' "$out" | grep -c '^ADV' | tr -d ' ')"
    detail="$(printf '%s\n' "$out" | grep -v -e '^TSR ' -e '^ADV' | sed "s|$ROOT/||" | cut -c1-170 | tr '\n' ' ')"
  fi

  if [ "${kb:-0}" -gt 0 ] || [ "${tc:-0}" -gt 0 ]; then
    record units FAIL "$kb unit defect(s), $tc rate/timestamp defect(s), ${ac:-0} advisory: $detail"
  else
    record units PASS "binary units written KiB/MiB/GiB/TiB; timestamps UTC; ${ac:-0} advisory per-object decimal unit(s)"
  fi
}

check_tree() {
  local problems=0 detail=""
  # Required top-level paths from AGENTS.md, but only those that exist yet are
  # enforced. An empty repo must pass: the gate measures coherence, not progress.
  local required="AGENTS.md"
  local p
  for p in $required; do
    [ -e "$ROOT/$p" ] || { problems=$((problems+1)); detail="${detail}missing:$p "; }
  done

  # No .tmp content may be referenced from a committed document.
  if [ -d "$ROOT/docs" ]; then
    local refs
    refs="$(grep -rn --include='*.md' -E '\(\.tmp/|\.\./\.tmp/' "$ROOT/docs" 2>/dev/null | head -3)"
    [ -n "$refs" ] && { problems=$((problems+1)); detail="${detail}doc-links-into-.tmp "; }
  fi

  # A committed credential-shaped file is a hard failure.
  if [ -d "$ROOT" ]; then
    local creds
    creds="$(find "$ROOT" -maxdepth 3 -type f \( -name '.env' -o -name '*.pem' -o -name 'id_rsa' \) \
        -not -path '*/.git/*' -not -path '*/.tmp/*' 2>/dev/null | head -3)"
    [ -n "$creds" ] && { problems=$((problems+1)); detail="${detail}credential-file "; }
  fi

  if [ "$problems" = "0" ]; then
    record tree PASS "required paths present; no .tmp links; no credential files"
  else
    record tree FAIL "$problems problem(s): $detail"
  fi
}

check_rellinks() {
  local script="$HERE/linkcheck.py"
  [ -f "$script" ] || { record rellinks SKIP "linkcheck.py not beside gate.sh"; return; }
  need_python || { record rellinks SKIP "python not found"; return; }

  # Every relative Markdown link in the tree. The `links` check covers the ones
  # out of docs/README.md and the citation of each verified record; this covers the
  # thousands inside the documents, which rot whenever a file moves and which no
  # other check would notice.
  local out rc
  out="$("$PY" "$script" --root "$ROOT" --quiet 2>&1)"; rc=$?
  if [ "$rc" = "0" ]; then
    record rellinks PASS "$out"
  elif [ "$rc" = "2" ] || [ "$rc" = "3" ]; then
    record rellinks SKIP "linkcheck could not run (exit $rc)"
  else
    local first
    first="$("$PY" "$script" --root "$ROOT" 2>&1 | head -3 | tr '\n' ' ' | cut -c1-160)"
    record rellinks FAIL "$first"
  fi
}

check_sources() {
  local script="$HERE/sources/aggregator-diff.py"
  # The registry lives in the tree under test, not beside this script. A check
  # that read its own tree would pass an empty root and could not be tested.
  [ -f "$script" ] || { record sources SKIP "no aggregator-diff.py"; return; }
  need_python || { record sources SKIP "python not found"; return; }

  # One registry per topic. A tunnel list is diffed against the egress records
  # and a VPS list against compute, so a single registry would either mix the
  # two or force every topic to carry every other topic's watchlist.
  local registries reg found=0 total_active=0
  registries="$(find "$ROOT/scripts/sources" -maxdepth 1 -name '*aggregators*.tsv' 2>/dev/null | sort)"
  [ -n "$registries" ] || { record sources SKIP "no aggregator registry under $ROOT"; return; }

  # The corpus missed a whole market because one provider list was read and the
  # conclusion "the names are known" was drawn from it. The registry names every
  # source that lists other providers, and this check refuses an undiffed or
  # overdue one, so a source cannot be quietly forgotten again.
  local out rc first problems=""
  while IFS= read -r reg; do
    [ -z "$reg" ] && continue
    found=$((found+1))
    out="$("$PY" "$script" --root "$ROOT" --registry "$reg" --check 2>&1)"; rc=$?
    if [ "$rc" = "0" ]; then
      total_active=$((total_active + $(printf '%s' "$out" | head -1 | sed -n 's/.* \([0-9]*\) active.*/\1/p')))
    elif [ "$rc" = "3" ]; then
      problems="${problems}$(basename "$reg") unreadable; "
    else
      first="$(printf '%s' "$out" | sed -n '2,3p' | tr '\n' ' ' | cut -c1-110)"
      problems="${problems}$(basename "$reg"): ${first}; "
    fi
  done <<< "$registries"

  if [ -n "$problems" ]; then
    record sources FAIL "$(printf '%s' "$problems" | cut -c1-170)"
  else
    record sources PASS "$found registr$([ "$found" = 1 ] && echo y || echo ies), ${total_active:-0} active sources, all diffed and listed"
  fi
}

check_projection() {
  local script="$HERE/fshy/build.py"
  [ -f "$script" ] || { record projection SKIP "no scripts/fshy/build.py"; return; }
  [ -d "$ROOT/dossier" ] || { record projection SKIP "no dossier/ under the root"; return; }
  need_python || { record projection SKIP "python not found"; return; }

  # The public wiki, API and MCP serve a projection of dossier/, never the files.
  # Build that projection: every source value must receive exactly one disposition
  # (kept, rewritten, withheld or excluded), and the leak scan must find no
  # operator host, personal detail, process narrative or terms text in the output.
  local out rc
  out="$("$PY" "$HERE/fshy/test_projection.py" 2>&1)"; rc=$?
  if [ "$rc" != "0" ]; then
    record projection FAIL "rule selftest: $(printf '%s' "$out" | grep -m1 '^FAIL' | cut -c1-150)"
    return
  fi
  out="$("$PY" "$script" --repo "$ROOT" --check --quiet 2>&1)"; rc=$?
  if [ "$rc" = "0" ]; then
    record projection PASS "rule selftest passes; public store builds; every source value accounted for; leak scan and price check clean"
  else
    record projection FAIL "$(printf '%s' "$out" | grep -m2 -E 'LEAK|PRICE|accounting|Error|leak scan|price check' | tr '\n' ' ' | cut -c1-170)"
  fi
}

check_selfhosted() {
  local script="$HERE/self-hosted-last.py"
  [ -f "$script" ] || { record selfhosted SKIP "no scripts/self-hosted-last.py"; return; }
  [ -d "$ROOT/dossier" ] || { record selfhosted SKIP "no dossier/ under the root"; return; }
  need_python || { record selfhosted SKIP "python not found"; return; }

  # The operator's rule of 2026-10-29: a self-hosted record (self_hosted: true) is the last resort. Every list
  # in docs/ and every need puts it after every hosted record and never recommends it. The needs are read from
  # the public store that the projection check built just before; the script builds it only when it is stale.
  local out rc
  out="$("$PY" "$script" --root "$ROOT" 2>&1)"; rc=$?
  if [ "$rc" = "0" ]; then
    record selfhosted PASS "$(printf '%s' "$out" | tail -1 | sed 's/^0 list(s) or need(s) put[^;]*; //' | cut -c1-170)"
  else
    record selfhosted FAIL "$(printf '%s' "$out" | tail -1 | cut -d';' -f1 | cut -c1-90): $(printf '%s' "$out" | head -1 | cut -c1-110)"
  fi
}

check_contradictions() {
  local script="$HERE/research/rq.py"
  [ -f "$script" ] || { record contradictions SKIP "no scripts/research/rq.py"; return; }
  [ -d "$ROOT/dossier" ] || { record contradictions SKIP "no dossier/ under the root"; return; }
  need_python || { record contradictions SKIP "python not found"; return; }

  # Mechanical contradiction and invariant rules (scripts/research/checks.py). Existing
  # violations are in scripts/research/baseline.tsv; a commit fails only when it adds one,
  # so the corpus can only get cleaner. Evidence dated from 2026-10-28 on must carry a
  # capture whose text holds the quote, whichever tool wrote it.
  local out rc
  out="$("$PY" "$script" check --repo "$ROOT" --gate 2>&1)"; rc=$?
  if [ "$rc" = "0" ]; then
    record contradictions PASS "$(printf '%s' "$out" | tail -1 | sed 's/^PASS //' | cut -c1-170)"
  else
    record contradictions FAIL "$(printf '%s' "$out" | grep -m1 -E 'FAIL|rq:|Error' | sed 's/^FAIL //' | cut -c1-170)"
  fi
}

# -------------------------------------------------------------------- runner --

run_checks() {
  for c in $ALL_CHECKS; do
    check_wanted "$c" || continue
    "check_$c"
  done
}

emit_summary() {
  local total=$((N_PASS+N_FAIL+N_SKIP))
  if [ "$JSON" = "1" ]; then
    "$PY" - "$RESULTS" "$N_PASS" "$N_FAIL" "$N_SKIP" "$ROOT" "$STRICT" <<'PYEOF'
import json, sys
raw, p, f, s, root, strict = sys.argv[1:7]
checks = []
for line in raw.splitlines():
    if not line.strip():
        continue
    # A result row is `name|status|detail`. Splitting on "|" and indexing blindly
    # raises IndexError on any line that is not a row, and gate detail text can
    # itself contain the separator, so partition twice and never index.
    name, _, rest = line.partition("|")
    status, _, detail = rest.partition("|")
    if not status:
        continue
    checks.append({"check": name, "status": status, "detail": detail})
print(json.dumps({"ok": int(f) == 0 and (strict != "1" or int(s) == 0), "root": root, "checks": checks,
                  "pass": int(p), "fail": int(f), "skip": int(s)}, ensure_ascii=False))
PYEOF
  else
    printf '\n%d checks: %d pass, %d fail, %d skip\n' "$total" "$N_PASS" "$N_FAIL" "$N_SKIP"
    if [ "$N_FAIL" -gt 0 ]; then
      printf 'gate: FAILED\n'
    elif [ "$N_SKIP" -gt 0 ] && [ "$STRICT" = "1" ]; then
      printf 'gate: FAILED under --strict (%d skipped check(s))\n' "$N_SKIP"
    elif [ "$N_SKIP" -gt 0 ]; then
      printf 'gate: PASSED with %d skipped check(s)\n' "$N_SKIP"
    else
      printf 'gate: PASSED\n'
    fi
  fi
}

# ------------------------------------------------------------------- selftest --

selftest() {
  local fails=0
  # Keep this in step with the cases below; it is the only number in the summary
  # that is not derived, and a wrong one reads as a case that never ran.
  local ncases=15
  local fix="$HERE/fixtures"
  printf 'gate selftest — every case below must produce the stated verdict\n\n'

  # 1. empty directory must pass
  local empty
  empty="$(mktemp -d "${TMPDIR:-/tmp}/gate-empty.XXXXXX")"
  touch "$empty/AGENTS.md"
  if sh "$0" --root "$empty" --quiet >/dev/null 2>&1; then
    printf 'PASS empty directory passes\n'
  else
    printf 'FAIL empty directory should pass\n'; fails=$((fails+1))
  fi
  rm -rf "$empty"

  # 2. broken dossier must fail the schema check
  local tmpd
  tmpd="$(mktemp -d "${TMPDIR:-/tmp}/gate-schema.XXXXXX")"
  mkdir -p "$tmpd/dossier/storage" "$tmpd/docs" "$tmpd/scripts/dossier"
  touch "$tmpd/AGENTS.md"
  cp "$fix/dossier-broken/fixture-broken.json" "$tmpd/dossier/storage/"
  # Lay the schema out where a real root keeps it. The gate looks for
  # scripts/dossier/schema.json, so a fixture root that put it at the top level
  # tested a path no repository has and the case failed for the wrong reason.
  cp "$HERE/dossier/schema.json" "$tmpd/scripts/dossier/" \
    || { printf 'FAIL selftest fixture missing: scripts/dossier/schema.json\n'
         fails=$((fails+1)); }
  cp "$fix/dossier-broken/fixture-broken.json" "$tmpd/dossier/storage/" \
    || { printf 'FAIL selftest fixture missing: fixtures/dossier-broken\n'
         fails=$((fails+1)); }
  # "non-zero exit" is not the assertion. A missing schema, a missing validator
  # and a caught record all exit non-zero, and only the third is a catch. Assert
  # the failure names counted defects, which only the validator produces.
  local dout
  dout="$(sh "$0" --root "$tmpd" --check schema 2>&1)"
  if printf '%s' "$dout" | grep -q '^FAIL schema' \
     && printf '%s' "$dout" | grep -q 'defects'; then
    printf 'PASS broken dossier fails schema on the record, not on a missing input\n'
  else
    printf 'FAIL broken dossier should fail schema on the record, got: %s\n' \
      "$(printf '%s' "$dout" | head -1)"
    fails=$((fails+1))
  fi

  # 3. stale dossier must fail the staleness check
  local tmps
  tmps="$(mktemp -d "${TMPDIR:-/tmp}/gate-stale.XXXXXX")"
  mkdir -p "$tmps/dossier/storage" "$tmps/docs"
  touch "$tmps/AGENTS.md"
  cp "$fix/dossier-stale/fixture-stale-host.json" "$tmps/dossier/storage/"
  if sh "$0" --root "$tmps" --quiet --check staleness >/dev/null 2>&1; then
    printf 'FAIL stale dossier should fail staleness\n'; fails=$((fails+1))
  else
    printf 'PASS stale dossier fails staleness\n'
  fi
  rm -rf "$tmps"

  # 4. KB-where-KiB-belongs must fail the units check
  local tmpu
  tmpu="$(mktemp -d "${TMPDIR:-/tmp}/gate-units.XXXXXX")"
  mkdir -p "$tmpu/docs"
  touch "$tmpu/AGENTS.md"
  cp "$fix/docs-broken/free/units-and-attribution.md" "$tmpu/docs/units.md"
  if sh "$0" --root "$tmpu" --quiet --check units >/dev/null 2>&1; then
    printf 'FAIL KB-instead-of-KiB should fail units\n'; fails=$((fails+1))
  else
    printf 'PASS KB-instead-of-KiB fails units\n'
  fi
  rm -rf "$tmpu"

  # 6. an undiffed research source must fail the sources check, and a diffed one
  #    must pass it. Without this pair, the check could refuse everything and look
  #    identical to a working one.
  local tmpg
  tmpg="$(mktemp -d "${TMPDIR:-/tmp}/gate-sources.XXXXXX")"
  mkdir -p "$tmpg/docs/compute" "$tmpg/scripts/sources"
  touch "$tmpg/AGENTS.md"
  printf '%s\n' '# test' 'slug	url	kind	cadence_days	last_diff	covered	missing	pattern	status	note' \
    'src	https://example.test/	provider-index	30		1	0		pending	x' \
    > "$tmpg/scripts/sources/aggregators.tsv"
  cp "$HERE/sources/aggregator-diff.py" "$tmpg/scripts/sources/" 2>/dev/null
  if sh "$0" --root "$tmpg" --quiet --check sources >/dev/null 2>&1; then
    printf 'FAIL undiffed source should fail sources\n'; fails=$((fails+1))
  else
    printf 'PASS undiffed source fails sources\n'
  fi
  printf '%s\n' '# test' 'slug	url	kind	cadence_days	last_diff	covered	missing	pattern	status	note' \
    'src	https://example.test/	provider-index	30	2099-01-01	1	0		active	x' \
    > "$tmpg/scripts/sources/aggregators.tsv"
  printf '%s\n' 'https://example.test/' > "$tmpg/docs/compute/watchlist.md"
  if sh "$0" --root "$tmpg" --quiet --check sources >/dev/null 2>&1; then
    printf 'PASS a diffed, listed source passes sources\n'
  else
    printf 'FAIL a diffed, listed source should pass sources\n'; fails=$((fails+1))
  fi
  rm -rf "$tmpg"

  # 5. an AI-attribution line must fail the attribution check
  local tmpa
  tmpa="$(mktemp -d "${TMPDIR:-/tmp}/gate-attr.XXXXXX")"
  mkdir -p "$tmpa/docs"
  touch "$tmpa/AGENTS.md"
  cp "$fix/docs-broken/free/units-and-attribution.md" "$tmpa/docs/attr.md"
  if sh "$0" --root "$tmpa" --quiet --check attribution >/dev/null 2>&1; then
    printf 'FAIL AI attribution should fail attribution\n'; fails=$((fails+1))
  else
    printf 'PASS AI attribution fails attribution\n'
  fi
  rm -rf "$tmpa"

  # 14. every credit line: the commit hook refuses it in a message, and the attribution check refuses it in a
  # document (R3-B-05). A sentence about a vendor's product is a finding: the attribution check passes it (I-03).
  local tmph hook="$HERE/../.githooks/commit-msg" missed=""
  tmph="$(mktemp -d "${TMPDIR:-/tmp}/gate-hook.XXXXXX")"
  mkdir -p "$tmph/docs"
  touch "$tmph/AGENTS.md"
  printf '%s\n' \
    "$(printf '\360\237\244\226') Generated with [Claude Code](https://claude.com/claude-code)" \
    "$(printf '\360\237\244\226')" \
    'Generated with [Claude Code](https://claude.com/claude-code)' \
    'Co-Authored-By: Claude Opus <noreply@anthropic.com>' 'Co-authored-by: Claude <noreply@anthropic.com>' \
    'Built using GPT-4o' 'Powered by Gemini' 'Assisted-by: Copilot' 'Written with the help of ChatGPT' \
    'Drafted via Llama 3.1' 'The fix, written with Claude, adds a test.' \
    'This commit was generated by an AI assistant.' 'Code written by Codex' 'Signed-off-by: Cursor agent' \
    'Made with Claude' 'Assisted-by: Claude' 'Generated using Claude' 'Written with the help of Claude Opus' \
    'Reviewed-by: Claude' 'Generated with Claude Code' 'Drafted with ChatGPT' 'Produced by an AI model' \
    > "$tmph/variants.txt"
  while IFS= read -r v; do
    printf 'docs: a subject\n\n%s\n' "$v" > "$tmph/msg"
    sh "$hook" "$tmph/msg" >/dev/null 2>&1 && missed="${missed}hook:[$v] "
    printf '# a page\n\n%s\n' "$v" > "$tmph/docs/attr.md"
    sh "$0" --root "$tmph" --quiet --check attribution >/dev/null 2>&1 && missed="${missed}gate:[$v] "
  done < "$tmph/variants.txt"
  # the link of a tool's credit line is refused in a commit; in a document it may cite the product
  printf 'docs: a subject\n\nsee https://claude.com/claude-code\n' > "$tmph/msg"
  sh "$hook" "$tmph/msg" >/dev/null 2>&1 && missed="${missed}hook:[a credit link] "
  printf '%s\n' \
    'The Claude Pro plan is USD 20 a month, and Cursor Pro moved to usage pricing.' \
    'The answer engine is powered by AI and reads the web.' 'Keys are created in AI Studio and shown once.' \
    'Answers are generated by Gemini or by Claude depending on the plan.' \
    'The page was reviewed by OpenAI before launch.' 'Free credits are created via Cursor Pro referrals.' \
    'The SDK is written in Rust and built using LLM tooling.' 'the free models made by Mistral and Meta' \
    'the models built by OpenAI are listed' \
    > "$tmph/products.txt"
  while IFS= read -r v; do
    printf '# a page\n\n%s\n' "$v" > "$tmph/docs/attr.md"
    sh "$0" --root "$tmph" --quiet --check attribution >/dev/null 2>&1 || missed="${missed}gate refused:[$v] "
  done < "$tmph/products.txt"
  if [ -z "$missed" ]; then
    printf 'PASS the hook and the attribution check refuse every credit line; vendor sentences pass the check\n'
  else
    printf 'FAIL attribution variants: %s\n' "$(printf '%s' "$missed" | cut -c1-200)"; fails=$((fails+1))
  fi
  rm -rf "$tmph"

  # 6. a dangling link from docs/README.md must fail the links check
  local tmpl
  tmpl="$(mktemp -d "${TMPDIR:-/tmp}/gate-links.XXXXXX")"
  mkdir -p "$tmpl/docs"
  touch "$tmpl/AGENTS.md"
  printf '# docs\n\n| topic |\n|---|\n| [storage](storage/README.md) |\n' > "$tmpl/docs/README.md"
  if sh "$0" --root "$tmpl" --quiet --check links >/dev/null 2>&1; then
    printf 'FAIL dangling doc link should fail links\n'; fails=$((fails+1))
  else
    printf 'PASS dangling doc link fails links\n'
  fi
  rm -rf "$tmpl"

  # 7. the clean doc + good record must PASS every check runnable here
  local tmpg
  tmpg="$(mktemp -d "${TMPDIR:-/tmp}/gate-good.XXXXXX")"
  mkdir -p "$tmpg/dossier/storage" "$tmpg/docs/free" "$tmpg/scripts/dossier"
  touch "$tmpg/AGENTS.md"
  cp "$fix/dossier-good/fixture-good-host.json" "$tmpg/dossier/storage/"
  cp "$HERE/dossier/schema.json" "$tmpg/scripts/dossier/"
  cp "$fix/docs-good/free/clean-doc.md" "$tmpg/docs/free/"
  printf '# docs\n\n| topic |\n|---|\n| [clean-doc](free/clean-doc.md) |\n' > "$tmpg/docs/README.md"
  if sh "$0" --root "$tmpg" --quiet --check schema,links,attribution,units,tree >/dev/null 2>&1; then
    printf 'PASS clean fixture passes schema, links, attribution, units, tree\n'
  else
    printf 'FAIL clean fixture should pass\n'
    sh "$0" --root "$tmpg" --check schema,links,attribution,units,tree 2>&1 | sed 's/^/     /'
    fails=$((fails+1))
  fi

  # 9. a planted contradiction (GB stated under a GiB unit, and an evidence row dated after the
  #    capture rule with no capture) must fail the contradictions check, and the clean record must
  #    pass it. The temporary root has no baseline, so every error violation is new there.
  local tmpc cout
  tmpc="$(mktemp -d "${TMPDIR:-/tmp}/gate-contra.XXXXXX")"
  mkdir -p "$tmpc/dossier/storage"
  touch "$tmpc/AGENTS.md"
  cp "$fix/dossier-good/fixture-good-host.json" "$tmpc/dossier/storage/"
  if sh "$0" --root "$tmpc" --quiet --check contradictions >/dev/null 2>&1; then
    printf 'PASS clean record passes contradictions\n'
  else
    printf 'FAIL clean record should pass contradictions\n'
    sh "$0" --root "$tmpc" --check contradictions 2>&1 | sed 's/^/     /'
    fails=$((fails+1))
  fi
  cp "$fix/dossier-broken/fixture-contradiction.json" "$tmpc/dossier/storage/"
  cout="$(sh "$0" --root "$tmpc" --check contradictions 2>&1)"
  if printf '%s' "$cout" | grep -q '^FAIL contradictions' && printf '%s' "$cout" | grep -q -e C07 -e C21; then
    printf 'PASS planted contradiction fails contradictions on the rule\n'
  else
    printf 'FAIL planted contradiction should fail contradictions, got: %s\n' "$(printf '%s' "$cout" | head -1)"
    fails=$((fails+1))
  fi
  rm -rf "$tmpc"

  # 15. the self-hosted check refuses a self-hosted row above a hosted one, and a self-hosted row that
  #     recommends it, and passes the clean list (its own fixtures, planted in a temporary tree)
  if "$PY" "$HERE/self-hosted-last.py" --selftest >/dev/null 2>&1; then
    printf 'PASS self-hosted-last refuses every planted defect and passes the clean list\n'
  else
    printf 'FAIL self-hosted-last selftest\n'
    "$PY" "$HERE/self-hosted-last.py" --selftest 2>&1 | grep '^FAIL' | sed 's/^/     /'
    fails=$((fails+1))
  fi

  # 8. --strict turns a skip into a failure
  local tmpskip
  tmpskip="$(mktemp -d "${TMPDIR:-/tmp}/gate-skip.XXXXXX")"
  touch "$tmpskip/AGENTS.md"
  if ! sh "$0" --root "$tmpskip" --quiet >/dev/null 2>&1; then
    printf 'FAIL empty dir should pass without --strict\n'; fails=$((fails+1))
  elif sh "$0" --root "$tmpskip" --quiet --strict >/dev/null 2>&1; then
    printf 'FAIL --strict should fail a skipped check\n'; fails=$((fails+1))
  else
    printf 'PASS --strict fails on a skipped check\n'
  fi
  rm -rf "$tmpskip" "$tmpd" "$tmpg"

  # 10. no Python interpreter must exit 3. It used to SKIP seven checks, the leak scan and the contradiction
  #     ratchet among them, and pass.
  local tmpp prc
  tmpp="$(mktemp -d "${TMPDIR:-/tmp}/gate-nopy.XXXXXX")"
  mkdir -p "$tmpp/dossier/storage"
  touch "$tmpp/AGENTS.md"
  cp "$fix/dossier-good/fixture-good-host.json" "$tmpp/dossier/storage/"
  PYTHON=no-such-python sh "$0" --root "$tmpp" --quiet >/dev/null 2>&1; prc=$?
  if [ "$prc" = "3" ]; then
    printf 'PASS no Python interpreter exits 3, not a pass with skipped checks\n'
  else
    printf 'FAIL no Python interpreter should exit 3, got %s\n' "$prc"; fails=$((fails+1))
  fi
  rm -rf "$tmpp"

  printf '\n'
  if [ "$fails" = "0" ]; then
    printf 'gate selftest: %d cases, 0 failed\n' "$ncases"
    return 0
  fi
  printf 'gate selftest: %d cases, %d failed\n' "$ncases" "$fails"
  return 1
}

# ---------------------------------------------------------------------- main --

if [ "$SELFTEST" = "1" ]; then
  selftest
  exit $?
fi

if [ -z "$ROOT" ]; then
  printf 'gate: --root is required (use --root .)\n' >&2
  exit 2
fi
if [ ! -d "$ROOT" ]; then
  printf 'gate: --root is not a directory: %s\n' "$ROOT" >&2
  exit 2
fi
ROOT="$(cd "$ROOT" && pwd)"

command -v grep >/dev/null 2>&1 || { printf 'gate: grep is required\n' >&2; exit 3; }
command -v find >/dev/null 2>&1 || { printf 'gate: find is required\n' >&2; exit 3; }
# Without an interpreter, seven checks (the leak scan and the contradiction ratchet among them) would SKIP and
# the gate would pass. That is a broken environment, not an inapplicable check.
if [ -z "$PY" ]; then
  for c in schema staleness binding links rellinks sources projection selfhosted contradictions; do
    if check_wanted "$c" || [ "$JSON" = "1" ]; then
      printf 'gate: no Python 3.9 or later found (tried python3 and python; set PYTHON); %s needs it\n' "$c" >&2
      exit 3
    fi
  done
fi

run_checks
emit_summary

if [ "$N_FAIL" -gt 0 ]; then exit 1; fi
if [ "$STRICT" = "1" ] && [ "$N_SKIP" -gt 0 ]; then exit 1; fi
exit 0
