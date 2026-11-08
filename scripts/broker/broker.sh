#!/usr/bin/env bash
# broker.sh — thin wrappers over the web-access broker.
#
# PURPOSE
#   One way to call web.pkgforge.dev, so no writer hand-rolls a curl and every
#   caller interprets a broker refusal the same way. The distinction that matters
#   is exit 1 vs exit 4: "the page said no" versus "the broker said no".

# WHY IT EXISTS
#   The corpus records a whole class of wasted wave caused by treating a broker
#   503/429 as a finding about the target. A host was recorded dead because the
#   broker's spend breaker was open. With this script a 503 from the broker is
#   exit 4 ("retry, the tool is unavailable") and a 404 from the origin is exit 1
#   ("the target refused"), and a caller can branch without reading prose.

# DEPENDENCIES
#   bash, curl, awk, sed, sort, coreutils. jq is NOT required; JSON is passed
#   through byte for byte unless a subcommand must reshape it, and where it must,
#   small Python helpers do the work (python is already required by the repo).

# OUTPUT
#   The broker's own bytes on stdout, unmodified, except:
#     search  --tsv   url <TAB> title <TAB> snippet
#     status          the broker's status JSON; status --human: a one-line-per-service table
#     (both exit 4 when a service is not ok)
#   Machine-readable first. Nothing decorative ever reaches stdout.

# EXIT CODES  (repository map, scripts/README.md)
#   0  the broker answered
#   1  the origin said no for a specific URL: an origin 4xx/5xx passed through
#   2  usage error: unknown subcommand, missing argument, non-http(s) URL
#   3  environment wrong: curl absent, DNS dead, transport failure, timeout
#   4  the broker said no: 503 disabled, 429 rate-limited, problem+json from the
#      broker itself, or a service that is down in /status. Nothing about the
#      target has been established. With a Retry-After header, stderr carries
#      retry_after=N retry_at=<UTC>: read again after that time. BROKER_WAIT=1
#      waits it out in the same call and repeats only the curl request.
#
# EXAMPLES
#   sh broker.sh read https://example.com/pricing
#   sh broker.sh fetch https://api.example.com/x --head
#   sh broker.sh search "unlimited storage" --domains reddit.com   (20 results, the most one request returns)
#   sh broker.sh archive https://example.com/ --at 2025-06
#   sh broker.sh crawl https://developers.cloudflare.com/            (100 pages, the most one job returns)
#   sh broker.sh research "vector database" --rank provider          (100 works, the most one request returns)
#   sh broker.sh research --next 'https://research.web.pkgforge.dev/works?...'   (an answer's next link)
#   sh broker.sh gh repos/cloudflare/workers-sdk
#   sh broker.sh status

# a bash script: `sh broker.sh` on a host whose sh is dash (Debian, Ubuntu) runs it again with bash (W3-05)
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

set -uo pipefail

BROKER_READ="${BROKER_READ:-https://read.web.pkgforge.dev}"
BROKER_FETCH="${BROKER_FETCH:-https://fetch.web.pkgforge.dev}"
BROKER_SEARCH="${BROKER_SEARCH:-https://search.web.pkgforge.dev}"
BROKER_ARCHIVE="${BROKER_ARCHIVE:-https://archive.web.pkgforge.dev}"
BROKER_CRAWL="${BROKER_CRAWL:-https://crawl.web.pkgforge.dev}"
BROKER_RESEARCH="${BROKER_RESEARCH:-https://research.web.pkgforge.dev}"
BROKER_GH="${BROKER_GH:-https://api.gh.pkgforge.dev}"
BROKER_STATUS="${BROKER_STATUS:-https://web.pkgforge.dev/status.json}"

CURL_TIMEOUT="${BROKER_TIMEOUT:-45}"
CURL_CONNECT_TIMEOUT="${BROKER_CONNECT_TIMEOUT:-10}"
# $PYTHON when set, else python3 when the shell finds one that is not the Windows Store stub (Debian, Ubuntu and
# macOS ship only python3), else python. No Python is started to test one: every start costs a process.
PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  p=$(command -v python3 2>/dev/null) && case "$p" in */WindowsApps/*) ;; *) PY=python3 ;; esac
  PY="${PY:-python}"
fi
# Windows Python defaults stdout to cp1252; a forum title or a Chinese provider
# name would be mangled into replacement characters in the TSV. Force UTF-8.
export PYTHONIOENCODING=utf-8

# Temporary files go under the repository's .tmp/: the lane's tmp/ when scripts/rq capture, or the brief's
# `TMPDIR={workspace}/tmp sh scripts/broker/broker.sh ...`, points TMPDIR there (a relative .tmp/... path is read from
# the repository root, where every command runs), else .tmp/rq/tmp/. A call that a tool's timeout kills then leaves
# its folder inside .tmp/, which the merge session's scripts/rq wipe deletes, and never in the system's temporary
# folder.
case "${TMPDIR:-}" in
  .tmp/*|*/.tmp/*|*\\.tmp\\*) BROKER_TMP_ROOT="$TMPDIR"; mkdir -p "$BROKER_TMP_ROOT" 2>/dev/null ;;
  *)
    BROKER_HERE="${0//\\//}"
    case "$BROKER_HERE" in */*) BROKER_HERE="${BROKER_HERE%/*}" ;; *) BROKER_HERE=. ;; esac
    BROKER_TMP_ROOT="$BROKER_HERE/../../.tmp/rq/tmp"
    mkdir -p "$BROKER_TMP_ROOT" 2>/dev/null || BROKER_TMP_ROOT="${TMPDIR:-/tmp}" ;;
esac
TMPDIR_BROKER="$(mktemp -d "$BROKER_TMP_ROOT/broker.XXXXXX" 2>/dev/null || mktemp -d)"
trap 'rm -rf "$TMPDIR_BROKER"' EXIT
# bash's here-document files and the Python helpers' files go into the same folder
export TMPDIR="$TMPDIR_BROKER" TMP="$TMPDIR_BROKER" TEMP="$TMPDIR_BROKER"

die() { local code="$1"; shift; printf 'broker: %s\n' "$*" >&2; exit "$code"; }

usage() {
  sed -n '2,49p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

need_curl() { command -v curl >/dev/null 2>&1 || die 3 "curl is not installed"; }

# urlencode <string> <var> — percent-encode every byte except the unreserved characters into the variable <var>,
# in bash: no process starts (a Python start and a fork per read cost more than the read on Windows, LIO7-02). The
# bytes of UTF-8 text are encoded one by one, as Python's urllib.parse.quote(s, safe="") does.
urlencode() {
  local LC_ALL=C s="$1" o="" c i
  for ((i = 0; i < ${#s}; i++)); do
    c="${s:i:1}"
    case "$c" in
      [A-Za-z0-9._~-]) o+="$c" ;;
      *) printf -v c '%%%02X' "'$c"; o+="$c" ;;
    esac
  done
  printf -v "$2" '%s' "$o"
}

require_http_url() {
  case "$1" in
    http://*|https://*) return 0 ;;
    *) die 2 "not an http(s) URL: $1" ;;
  esac
}

# classify_body <http-status> <body-file> <header-file>
# Returns 0 to pass through, or exits with the right code for a broker-side refusal.
# The broker's own refusals are RFC 9457 problem+json; an origin's are passed through.
classify_body() {
  local status="$1" body="$2" headers="$3" ctype
  ctype="$(awk 'BEGIN{IGNORECASE=1} /^content-type:/{sub(/^[^:]*:[ ]*/,"");print;exit}' "$headers" 2>/dev/null | tr -d '\r')"
  case "$status" in
    200|201|202|206|204|301|302|303|304|307|308|401|403|404|405|409|410|413|415|416|422|451)
      return 0 ;;
  esac
  if [ "$status" = "429" ] || [ "$status" = "503" ]; then
    # Broker-side when the body is problem+json naming a broker reason.
    if printf '%s' "$ctype" | grep -qi 'problem+json' && \
       grep -qiE '"(reason|title)"[[:space:]]*:[[:space:]]*"(rate-limited|disabled|none-configured|permanently-exhausted|held)' "$body" 2>/dev/null; then
      local reason ra at
      reason="$(sed -n 's/.*"reason"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$body" 2>/dev/null | head -1)"
      ra="$(retry_after "$headers")"
      if [ -n "$ra" ] && [ "${BROKER_WAIT:-0}" = "1" ]; then
        # the caller asked to wait (scripts/rq capture --wait): http_get waits the broker's own Retry-After and
        # repeats only the curl call
        printf 'broker: the broker said no (%s, HTTP %s); waiting %s s, as its Retry-After asks\n' \
          "${reason:-unknown}" "$status" "$ra" >&2
        return 2
      fi
      if [ -n "$ra" ]; then
        at="$(date -u -d "@$(( $(date -u +%s) + ra ))" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo unknown)"
        printf 'broker: the broker said no (%s, HTTP %s); the target was not judged; retry_after=%s retry_at=%s\n' \
          "${reason:-unknown}" "$status" "$ra" "$at" >&2
        exit 4
      fi
      printf 'broker: the broker said no (%s, HTTP %s); the target was not judged\n' \
        "${reason:-unknown}" "$status" >&2
      exit 4
    fi
    # An origin's own 429/503 passed through by fetch: that is about the target.
    return 0
  fi
  case "$status" in
    500|502|504|520|521|522|523|524|525|526|530)
      printf 'broker: broker-side failure (HTTP %s); nothing established about the target\n' "$status" >&2
      exit 4 ;;
    000|"")
      die 3 "transport failure: the broker is unreachable" ;;
  esac
  return 0
}

# retry_after <header-file> -> the seconds of a Retry-After header (a number, or an HTTP date made into seconds
# from now), or nothing when there is none. The only pacing of this script comes from the server.
retry_after() {
  local v then now
  v="$(awk 'BEGIN{IGNORECASE=1} /^retry-after:/{sub(/^[^:]*:[ ]*/,"");gsub(/\r/,"");print;exit}' "$1" 2>/dev/null)"
  [ -n "$v" ] || return 0
  case "$v" in
    *[!0-9]*) ;;
    *) printf '%s' "$v"; return 0 ;;
  esac
  then="$(date -u -d "$v" +%s 2>/dev/null)" || return 0
  now="$(date -u +%s)"
  if [ "$then" -gt "$now" ]; then printf '%s' "$((then - now))"; else printf '0'; fi
}

# http_get <url> [--out FILE] — one request, classified. Writes body to stdout. With BROKER_WAIT=1, a broker 429
# or 503 that carries Retry-After is waited out and only the curl call repeats, for as long as the broker answers
# that way: no attempt count and no wait limit of this script's own.
http_get() {
  local url="$1" out="${2:-}" hdr="$TMPDIR_BROKER/h"
  local status rc_c ra
  while :; do
    status="$(curl -q -sS -L --noproxy '*' \
        --connect-timeout "$CURL_CONNECT_TIMEOUT" --max-time "$CURL_TIMEOUT" \
        -D "$hdr" -w '%{http_code}' -o "${out:-$TMPDIR_BROKER/b}" "$url" 2>"$TMPDIR_BROKER/e")" || {
      local rc=$?
      if [ "$rc" = "6" ] || [ "$rc" = "7" ] || [ "$rc" = "28" ] || [ "$rc" = "35" ] || [ "$rc" = "52" ]; then
        printf 'broker: transport failure (%s): %s\n' "$rc" "$(head -1 "$TMPDIR_BROKER/e" 2>/dev/null)" >&2
        exit 3
      fi
      printf 'broker: curl failed (%s): %s\n' "$rc" "$(head -1 "$TMPDIR_BROKER/e" 2>/dev/null)" >&2
      exit 3
    }
    rc_c=0
    classify_body "$status" "${out:-$TMPDIR_BROKER/b}" "$hdr" || rc_c=$?
    if [ "$rc_c" = "2" ]; then
      ra="$(retry_after "$hdr")"
      sleep "${ra:-0}"  # wait: retry-after, the broker's own pause (BROKER_WAIT=1 only)
      continue
    fi
    break
  done
  [ "$rc_c" = "0" ] || return 1
  [ -n "$out" ] && return 0
  cat "$TMPDIR_BROKER/b"
  [ "$status" -ge 400 ] 2>/dev/null && return 1
  return 0
}

# ---------------------------------------------------------------- subcommands --

cmd_read() {
  local url="" provider="" mode="" fmt="markdown" urls_flag=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --provider) provider="${2:?--provider needs a value}"; shift 2 ;;
      --mode) mode="${2:?--mode needs a value}"; shift 2 ;;
      --json) fmt="json"; shift ;;
      --csv) urls_flag=1; shift ;;
      -h|--help) usage ;;
      --*) die 2 "read: unknown option $1" ;;
      *) url="$1"; shift ;;
    esac
  done
  [ -n "$url" ] || die 2 "read: need a URL"
  require_http_url "$url"
  local q="" enc
  urlencode "$url" enc
  # The ?url= form is mandatory when the target carries ? or #.
  case "$url" in
    *\?*|*\#*) q="?url=$enc" ;;
    *) q="/$enc" ;;
  esac
  local sep="?"
  [ -n "$q" ] && case "$q" in \?*) sep="&" ;; esac
  [ -n "$provider" ] && q="${q}${sep}__provider=${provider}" && sep="&"
  [ -n "$mode" ] && q="${q}${sep}__mode=${mode}" && sep="&"
  [ "$fmt" = "json" ] && q="${q}${sep}__format=json"
  [ "$urls_flag" = "1" ] && q="${q}${sep}__links=referenced"
  http_get "${BROKER_READ}${q}"
}

cmd_fetch() {
  local url="" head=0 provider="" egress="" dump=0
  local -a extra=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --head) head=1; shift ;;
      --dump-headers) dump=1; shift ;;
      --provider) provider="${2:?}"; shift 2 ;;
      --egress) egress="${2:?}"; shift 2 ;;
      --range) extra+=(--range "${2:?}"); shift 2 ;;
      --header) extra+=(-H "${2:?}"); shift 2 ;;
      -o|--output) extra+=(-o "${2:?}"); shift 2 ;;
      -h|--help) usage ;;
      --*) die 2 "fetch: unknown option $1" ;;
      *) url="$1"; shift ;;
    esac
  done
  [ -n "$url" ] || die 2 "fetch: need a URL"
  require_http_url "$url"
  local enc q
  urlencode "$url" enc
  case "$url" in
    *\?*|*\#*) q="?url=$enc" ;;
    *) q="/$enc" ;;
  esac
  # the first broker parameter after a path-form target opens the query with "?"
  local sep="?"
  case "$q" in \?*) sep="&" ;; esac
  [ -n "$provider" ] && q="${q}${sep}__provider=${provider}" && sep="&"
  [ -n "$egress" ] && q="${q}${sep}__egress=${egress}" && sep="&"
  [ "$dump" = "1" ] && q="${q}${sep}__strip-platform-headers=false"
  local -a cargs=()
  [ "$head" = "1" ] && cargs+=(-I)
  # fetch is the one subcommand that must emit raw bytes, so it drives curl
  # itself rather than going through http_get's captured-body path.
  local status
  status="$(curl -q -sS -L --noproxy '*' \
     --connect-timeout "$CURL_CONNECT_TIMEOUT" --max-time "$CURL_TIMEOUT" \
     "${cargs[@]}" "${extra[@]}" -D "$TMPDIR_BROKER/fh" \
     -w '%{http_code}' -o "$TMPDIR_BROKER/fb" "${BROKER_FETCH}${q}")" || exit 3
  classify_body "$status" "$TMPDIR_BROKER/fb" "$TMPDIR_BROKER/fh" || true
  if [ "$dump" = "1" ]; then
    cat "$TMPDIR_BROKER/fh"
    printf '\n'
  fi
  if [ "$head" = "1" ]; then
    # HEAD: emit the origin headers the proxy echoed, minus hop-by-hop noise.
    grep -viE '^(connection|transfer-encoding|keep-alive|date|content-length|content-encoding):' \
      "$TMPDIR_BROKER/fh" | tr -d '\r'
  else
    cat "$TMPDIR_BROKER/fb"
  fi
  [ "$status" -ge 400 ] 2>/dev/null && exit 1
  return 0
}

cmd_search() {
  # each default is the most one request to the broker returns (search 20, archive captures 1000, research 100, crawl
  # 100 pages): no client-side limit below the server's own (LW7-04)
  local query="" count=20 freshness="" domains="" excludes="" rank=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --count|-n) count="${2:?}"; shift 2 ;;
      --freshness|-f) freshness="${2:?}"; shift 2 ;;
      --domains|-d) domains="${2:?}"; shift 2 ;;
      --exclude-domains) excludes="${2:?}"; shift 2 ;;
      --rank) rank="${2:?}"; shift 2 ;;
      --tsv) TSV=1; shift ;;
      -h|--help) usage ;;
      --*) die 2 "search: unknown option $1" ;;
      *) query="${query:+$query }$1"; shift ;;
    esac
  done
  [ -n "$query" ] || die 2 "search: need a query"
  case "$count" in ''|*[!0-9]*) die 2 "search: --count must be an integer" ;; esac
  [ "$count" -ge 1 ] || die 2 "search: --count must be >= 1"
  [ "$count" -gt 20 ] && { printf 'broker: count %s clamped to 20 by the broker\n' "$count" >&2; count=20; }
  local q e
  urlencode "$query" e
  q="q=$e&count=$count"
  [ -n "$freshness" ] && case "$freshness" in
    day|week|month|year) q="$q&freshness=$freshness" ;;
    *) die 2 "search: --freshness must be day|week|month|year" ;;
  esac
  [ -n "$domains" ] && urlencode "$domains" e && q="$q&include_domains=$e"
  [ -n "$excludes" ] && urlencode "$excludes" e && q="$q&exclude_domains=$e"
  [ -n "$rank" ] && urlencode "$rank" e && q="$q&rank=$e"

  local body="$TMPDIR_BROKER/s"
  http_get "${BROKER_SEARCH}/search?${q}" "$body" || exit 1
  if [ "${TSV:-0}" = "1" ]; then
    "$PY" - "$body" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    sys.stderr.write("broker: search returned non-JSON: %s\n" % e)
    sys.exit(3)
for r in d.get("results") or []:
    def clean(s):
        return " ".join(str(s or "").split())
    print("\t".join([clean(r.get("url")), clean(r.get("title")), clean(r.get("snippet"))]))
PY
    return $?
  fi
  cat "$body"; printf '\n'
}

cmd_archive() {
  local url="" at="" action="captures" limit=1000 provider="" crawl_mode=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --at) at="${2:?}"; action="closest"; shift 2 ;;
      --captures) action="captures"; shift ;;
      --save) action="save"; shift ;;
      --limit) limit="${2:?}"; shift 2 ;;
      --provider) provider="${2:?}"; shift 2 ;;
      --crawl) crawl_mode=1; shift ;;
      -h|--help) usage ;;
      --*) die 2 "archive: unknown option $1" ;;
      *) url="$1"; shift ;;
    esac
  done
  [ -n "$url" ] || die 2 "archive: need a URL"
  require_http_url "$url"
  local q e
  urlencode "$url" e
  q="url=$e"
  [ -n "$at" ] && case "$at" in
    20[0-9][0-9]|20[0-9][0-9]-[01][0-9]|20[0-9][0-9]-[01][0-9]-[0-3][0-9]) ;;
    *) die 2 "archive: --at must be YYYY, YYYY-MM or YYYY-MM-DD" ;;
  esac
  [ -n "$at" ] && q="$q&at=$at"
  [ -n "$provider" ] && q="$q&provider=$provider"
  case "$action" in
    captures)
      [ "$limit" -gt 1000 ] && limit=1000
      http_get "${BROKER_ARCHIVE}/captures?${q}&limit=${limit}" ;;
    closest)
      http_get "${BROKER_ARCHIVE}/closest?${q}" ;;
    save)
      curl -q -sS --noproxy '*' --max-time "$CURL_TIMEOUT" -X POST \
        -D "$TMPDIR_BROKER/ah" -o "$TMPDIR_BROKER/ab" -w '%{http_code}' \
        "${BROKER_ARCHIVE}/save?${q}" > "$TMPDIR_BROKER/as" || exit 3
      classify_body "$(cat "$TMPDIR_BROKER/as")" "$TMPDIR_BROKER/ab" "$TMPDIR_BROKER/ah" || true
      cat "$TMPDIR_BROKER/ab"; printf '\n' ;;
  esac
}

# research QUERY [--count N] [--from YYYY] [--to YYYY] [--type T] [--oa true|false] [--rank R]
# research --next URL     the `next` link of an earlier answer (the cursor is bound to the query)
cmd_research() {
  local query="" count=100 from="" to="" type="" oa="" rank="" next=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --count|-n) count="${2:?}"; shift 2 ;;
      --from) from="${2:?}"; shift 2 ;;
      --to) to="${2:?}"; shift 2 ;;
      --type) type="${2:?}"; shift 2 ;;
      --oa) oa="${2:?}"; shift 2 ;;
      --rank) rank="${2:?}"; shift 2 ;;
      --next) next="${2:?}"; shift 2 ;;
      -h|--help) usage ;;
      --*) die 2 "research: unknown option $1" ;;
      *) query="${query:+$query }$1"; shift ;;
    esac
  done
  if [ -n "$next" ]; then
    case "$next" in
      "$BROKER_RESEARCH"/*) http_get "$next"; return $? ;;
      *) die 2 "research: --next takes a next link of $BROKER_RESEARCH" ;;
    esac
  fi
  [ -n "$query" ] || die 2 "research: need a query"
  case "$count" in ''|*[!0-9]*) die 2 "research: --count must be an integer" ;; esac
  local q e
  urlencode "$query" e
  q="q=$e&count=$count"
  [ -n "$from" ] && urlencode "$from" e && q="$q&from=$e"
  [ -n "$to" ] && urlencode "$to" e && q="$q&to=$e"
  [ -n "$type" ] && urlencode "$type" e && q="$q&type=$e"
  [ -n "$oa" ] && urlencode "$oa" e && q="$q&oa=$e"
  [ -n "$rank" ] && urlencode "$rank" e && q="$q&rank=$e"
  http_get "${BROKER_RESEARCH}/works?${q}"
}

cmd_crawl() {
  # the poll follows the job until its state is final; --max-wait S stops it earlier, and then exits 4 (W3-08)
  local url="" limit=100 depth="" render="" provider="" poll=1 interval=3 max_wait=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --limit|-n) limit="${2:?}"; shift 2 ;;
      --depth) depth="${2:?}"; shift 2 ;;
      --render) render="${2:?}"; shift 2 ;;
      --provider) provider="${2:?}"; shift 2 ;;
      --no-poll) poll=0; shift ;;
      --interval) interval="${2:?}"; shift 2 ;;
      --max-wait) max_wait="${2:?}"; shift 2 ;;
      -h|--help) usage ;;
      --*) die 2 "crawl: unknown option $1" ;;
      *) url="$1"; shift ;;
    esac
  done
  [ -n "$url" ] || die 2 "crawl: need a start URL"
  require_http_url "$url"
  case "$limit" in ''|*[!0-9]*) die 2 "crawl: --limit must be an integer" ;; esac
  case "$max_wait" in ''|*[!0-9]*) die 2 "crawl: --max-wait must be a whole number of seconds (0: until the job ends)" ;; esac
  [ "$limit" -ge 1 ] && [ "$limit" -le 100 ] || die 2 "crawl: --limit must be 1..100"

  local body
  body="$("$PY" - "$url" "$limit" "$depth" "$render" "$provider" <<'PY'
import json, sys
url, limit, depth, render, provider = sys.argv[1:6]
o = {"url": url, "limit": int(limit)}
if depth: o["depth"] = int(depth)
if render: o["render"] = render.lower() in ("1", "true", "yes")
if provider: o["provider"] = provider
print(json.dumps(o))
PY
)"
  local addp=""
  [ -n "$provider" ] && addp="?provider=$provider"
  local status
  status="$(curl -q -sS --noproxy '*' --max-time "$CURL_TIMEOUT" -X POST \
    -H 'content-type: application/json' -d "$body" \
    -D "$TMPDIR_BROKER/ch" -o "$TMPDIR_BROKER/cb" -w '%{http_code}' \
    "${BROKER_CRAWL}/crawl${addp}")" || exit 3
  classify_body "$status" "$TMPDIR_BROKER/cb" "$TMPDIR_BROKER/ch" || true
  if [ "$poll" = "0" ]; then cat "$TMPDIR_BROKER/cb"; printf '\n'; return 0; fi

  local loc
  loc="$(awk 'BEGIN{IGNORECASE=1} /^location:/{sub(/^[^:]*:[ ]*/,"");gsub(/\r/,"");print;exit}' "$TMPDIR_BROKER/ch")"
  if [ -z "$loc" ]; then
    "$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("job_id") or d.get("id") or "")' \
      "$TMPDIR_BROKER/cb" > "$TMPDIR_BROKER/loc" 2>/dev/null
    loc="$(cat "$TMPDIR_BROKER/loc")"
  fi
  [ -n "$loc" ] || { cat "$TMPDIR_BROKER/cb"; printf '\n'; die 3 "crawl: broker returned no job handle"; }
  case "$loc" in http*) poll_url="$loc" ;; /*) poll_url="${BROKER_CRAWL}${loc}" ;; *) poll_url="${BROKER_CRAWL}/crawl/${loc}" ;; esac

  local waited=0 state="" pause="$interval" ra
  while :; do
    sleep "$pause"; waited=$((waited + pause))  # wait: poll, the crawl job runs on the broker (its Retry-After when it sends one)
    status="$(curl -q -sS --noproxy '*' --max-time "$CURL_TIMEOUT" \
      -D "$TMPDIR_BROKER/ph" -o "$TMPDIR_BROKER/pb" -w '%{http_code}' "$poll_url")" || exit 3
    classify_body "$status" "$TMPDIR_BROKER/pb" "$TMPDIR_BROKER/ph" || true
    ra="$(retry_after "$TMPDIR_BROKER/ph")"
    pause="${ra:-$interval}"
    case "$status" in
      2??|429|503) ;;
      *) cat "$TMPDIR_BROKER/pb"; printf '\n'; die 4 "crawl: the poll of $poll_url answered HTTP $status" ;;
    esac
    state="$("$PY" -c 'import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: print(""); raise SystemExit
print(d.get("state") or d.get("status") or "")' "$TMPDIR_BROKER/pb" 2>/dev/null)"
    case "$state" in
      completed|failed|ended|done|error) break ;;
    esac
    if [ "$max_wait" -gt 0 ] && [ "$waited" -ge "$max_wait" ]; then break; fi
  done
  cat "$TMPDIR_BROKER/pb"; printf '\n'
  case "$state" in
    completed|ended|done) return 0 ;;
    failed|error) return 1 ;;
  esac
  printf 'broker: crawl: the job is %s after %s s (--max-wait %s); poll %s again\n' "${state:-in an unknown state}" \
    "$waited" "$max_wait" "$poll_url" >&2
  return 4
}

cmd_gh() {
  local path="" 
  while [ $# -gt 0 ]; do
    case "$1" in
      -h|--help) usage ;;
      --*) die 2 "gh: unknown option $1" ;;
      *) path="$1"; shift ;;
    esac
  done
  [ -n "$path" ] || die 2 "gh: need an API path, e.g. repos/OWNER/REPO"
  path="${path#/}"
  case "$path" in http*) die 2 "gh: give a path, not a URL (api.gh.pkgforge.dev is prepended)" ;; esac
  http_get "${BROKER_GH}/${path}"
}

cmd_status() {
  local human=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --human) human=1; shift ;;
      --json) human=0; shift ;;
      -h|--help) usage ;;
      *) die 2 "status: unknown option $1" ;;
    esac
  done
  local body="$TMPDIR_BROKER/st"
  http_get "$BROKER_STATUS" "$body" || exit 1
  if [ "$human" = "1" ]; then
    "$PY" - "$body" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print("overall  %s   read %s" % (d.get("overall"), d.get("readAt")))
for s in d.get("services") or []:
    lat = (s.get("traffic24h") or {}).get("latency") or {}
    print("  %-10s %-6s %-5s %s=%sms" % (s.get("service"), s.get("state"),
          s.get("status"), "p95", lat.get("p95Ms")))
PY
  else
    cat "$body"; printf '\n'
  fi
  local bad
  bad="$("$PY" -c 'import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
bad=[s.get("service") for s in d.get("services") or [] if s.get("state") not in ("ok",None)]
print(",".join(bad))' "$body" 2>/dev/null)"
  if [ -n "$bad" ]; then
    printf 'broker: these services are not ok: %s\n' "$bad" >&2
    return 4
  fi
  return 0
}

# -------------------------------------------------------------------- main --

[ $# -ge 1 ] || usage
sub="$1"; shift
[ "$sub" = "-h" ] || [ "$sub" = "--help" ] && usage
need_curl
case "$sub" in
  read)    cmd_read "$@" ;;
  fetch)   cmd_fetch "$@" ;;
  search)  cmd_search "$@" ;;
  archive) cmd_archive "$@" ;;
  crawl)   cmd_crawl "$@" ;;
  research) cmd_research "$@" ;;
  gh)      cmd_gh "$@" ;;
  status)  cmd_status "$@" ;;
  *) die 2 "unknown subcommand: $sub (read|fetch|search|archive|crawl|research|gh|status)" ;;
esac
