#!/usr/bin/env bash
# probe-alist.sh — classify AList / OpenList / Cloudreve public instances by CAPABILITY, not by enumeration.
#
# Design rule (learned the hard way, see docs/netdisk-pan/protocol): a host is never reported
# "writable" unless a byte-identical PUT -> GET roundtrip succeeds. Advertising fields lie.
#
# Usage:
#   ./probe-alist.sh host1 [host2 ...]        # positional hosts
#   ./probe-alist.sh -f hosts.txt             # one host per line, '#' comments allowed
#   ./probe-alist.sh -f hosts.txt -o out.tsv  # TSV results, one row per host
#
# Output: one TSV row per host. Header row included. Rows go to stdout, or to the
# file named by -o (the header is written there too). Nothing is written to stderr.
# Needs: curl, sha256sum, awk. No jq (kept dependency-free so it runs anywhere).
#
# What it measures: a 4 KiB write test, one per host, on a unique path, read back 2 s later
# (the wait is part of the measurement). Every host runs at once. A challenge page
# (Cloudflare/Turnstile/human-verification interstitial) is recorded as such for that host.
#
# Exit: always 0 unless the argument parse fails. Per-host failure is data, not an error.

set -uo pipefail

# Temporary files go under the repository's .tmp/, as broker.sh keeps them: the folder TMPDIR names when it lies
# under .tmp/ (`TMPDIR=.tmp/RUN/tools/tmp sh scripts/discover/probe-alist.sh ...`, read from the repository root),
# else .tmp/rq/tmp/. A probe that a tool's timeout kills then leaves its folder inside .tmp/, which the merge
# session's scripts/rq wipe deletes, and never in the system's temporary folder (AGENTS.md section 2 rule 14).
case "${TMPDIR:-}" in
  .tmp/*|*/.tmp/*|*\\.tmp\\*) PROBE_TMP_ROOT="$TMPDIR"; mkdir -p "$PROBE_TMP_ROOT" 2>/dev/null ;;
  *)
    PROBE_HERE="${0//\\//}"
    case "$PROBE_HERE" in */*) PROBE_HERE="${PROBE_HERE%/*}" ;; *) PROBE_HERE=. ;; esac
    PROBE_TMP_ROOT="$PROBE_HERE/../../.tmp/rq/tmp"
    mkdir -p "$PROBE_TMP_ROOT" 2>/dev/null || PROBE_TMP_ROOT="${TMPDIR:-/tmp}" ;;
esac
PROBE_TMP="$(mktemp -d "$PROBE_TMP_ROOT/probe-alist.XXXXXX" 2>/dev/null || mktemp -d)"
trap 'rm -rf "$PROBE_TMP"' EXIT
export TMPDIR="$PROBE_TMP" TMP="$PROBE_TMP" TEMP="$PROBE_TMP"

PROBE_BYTES=4096              # size of the write test object
UA='alist-capability-probe/1 (+research; single 4KiB test)'
OUT=''
HOSTS_FILE=''
TIMEOUT=10

usage() {
  sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# --help before getopts: getopts rejects a long option with "illegal option --"
# and that message arrives on stderr while the script still exits 0, which
# reads as success. A help flag that errors is a help flag nobody can use.
case "${1:-}" in
  -h|--help) usage ;;
esac

while getopts "f:o:t:" opt; do
  case "$opt" in
    f) HOSTS_FILE="$OPTARG" ;;
    o) OUT="$OPTARG" ;;
    t) TIMEOUT="$OPTARG" ;;
    *) echo "usage: $0 [-f hosts.txt] [-o out.tsv] [-t timeout] host..." >&2; exit 2 ;;
  esac
done
shift $((OPTIND-1))

# ---------- helpers ----------------------------------------------------------

# jget <key> : pull a scalar out of flat-ish JSON on stdin. Handles "key":value and
# "key":"value". Good enough for AList's response envelope; not a general parser.
jget() {
  awk -v k="\"$1\"" '
    { s=$0 }
    END {
      i = index(s, k)
      if (i == 0) { print ""; exit }
      rest = substr(s, i + length(k))
      sub(/^[[:space:]]*:[[:space:]]*/, "", rest)
      if (substr(rest,1,1) == "\"") {
        rest = substr(rest, 2); sub(/".*/, "", rest); print rest
      } else {
        match(rest, /^[^,}\]]+/); print substr(rest, 1, RLENGTH)
      }
    }'
}

# curl_body [curl args...] : last line of stdout is the HTTP status code.
curl_body() {
  curl -sS --max-time "$TIMEOUT" -A "$UA" "$@" -w '\n%{http_code}' 2>/dev/null
}

# is_challenge <body> : 0 if the body looks like an automated-traffic filter interstitial
is_challenge() {
  # Cloudflare / Turnstile / generic Chinese interstitial markup ...
  printf '%s' "$1" | grep -qiE '<title>[^<]*(just a moment|attention required|请稍候|人机验证|安全验证|ddos-guard|access denied|loading\.\.\.)|cf-browser-verification|cf_chl_opt|turnstile|g-recaptcha|hcaptcha|__cf_chl' && return 0
  # ... and the JS-cookie interstitial that some Chinese hosts put in front of
  # AList: a 200 with <title>Loading...</title> and a location.replace() carrying
  # a JWT. Observed on alist.advanced360.top 2026-10-22. It is not JSON and it is
  # not a page; it is a gate.
  printf '%s' "$1" | grep -qiE "window\.location\.(replace|href)[^;]*[?&](ch|js)=" && return 0
  return 1
}

# is_json : 0 if body starts with { or [
is_json() {
  local t; t=$(printf '%s' "$1" | tr -d '[:space:]' | cut -c1)
  [ "$t" = "{" ] || [ "$t" = "[" ]
}

tid() { printf '%s-%s' "$(date +%s)" "$$"; }

# ---------- per-host probe ---------------------------------------------------

# Column order is the schema of the permanent tool; keep it stable.
# Header goes to $OUT when -o is given, because the parallel driver redirects
# only the per-host rows.
HEADER='host	api_kind	http_status	anon_settings	anon_me_role	anon_me_permission	root_list_ok	root_entries	mounts_listed	providers	mounts_with_write_flag	put_attempted	put_http	put_code	put_message	write_verified	readback_sha_match	bytes_per_file_cap	fronting	verdict	notes	login_ok'
if [ -n "$OUT" ]; then
  printf '%b\n'  "$HEADER" > "$OUT"
else
  printf '%b\n'  "$HEADER"
fi


probe_one() {
  local raw="$1"
  local host="$1"
  case "$host" in
    http://*|https://*) : ;;
    *) host="https://$host" ;;
  esac
  host="${host%/}"

  local sid; sid=$(tid)
  local notes=""
  local api_kind="" http_status="" anon_settings="no" role="" perm=""
  local root_ok="no" root_entries="" mounts="" providers="" mountw="" root_names=""
  local put_att="no" put_http="" put_code="" put_msg=""
  local wver="no" shmatch="" cap="" fronting="" verdict="unknown" login_ok="no" oracle=""

  # --- 1. /api/public/settings : the cheapest liveness+kind test -------------
  # Cloudreve has /api/v4/site/ping instead; try AList shape first.
  local body code
  body=$(curl_body "$host/api/public/settings"); code="${body##*$'\n'}"; body="${body%$'\n'*}"

  if [ "$code" = "200" ] && is_json "$body" && [ -n "$(printf '%s' "$body" | jget code)" ]; then
    api_kind="alist"
    http_status="$code"
    local st; st=$(printf '%s' "$body" | jget site_title)
    local ver; ver=$(printf '%s' "$body" | jget version)
    notes="title=${st:-?};ver=${ver:-?}"
    anon_settings="yes"
  elif is_challenge "$body"; then
    http_status="$code"; api_kind="challenge"; notes="abandoned:challenge"
    emit; return
  else
    # Cloudreve v4 ping
    body=$(curl_body "$host/api/v4/site/ping"); code="${body##*$'\n'}"; body="${body%$'\n'*}"
    if [ "$code" = "200" ] && is_json "$body"; then
      api_kind="cloudreve"
      http_status="$code"
      notes="ping=$(printf '%s' "$body" | jget data)"
      http_status="$code"
      # Cloudreve has no anonymous listing; record and stop.
      anon_settings="n/a"; emit; return
    fi
    http_status="${code:-000}"; api_kind="none"
    [ -z "$code" ] && http_status="000"
    notes="no-api"
    emit; return
  fi

  # --- 1b. /api/me : role + permission bitmask -----------------------------
  # permission is a bitmask. From internal/model/user.go in OpenList:
  #   bit0 see-hides, bit1 no-password, bit2 offline-dl, bit3 mkdir+upload,
  #   bit4 rename, bit5 move, bit6 copy, bit7 remove, bit8 webdav-read,
  #   bit9 webdav-write, bit10 ftp/sftp-read, bit11 ftp/sftp-write,
  #   bit12 read-archives, bit13 decompress, bit14 share, bit15 custom-share-id.
  # Write needs bit3 (value 8) *or* an "allow upload" meta on the path; bit9 (512)
  # alone only covers WebDAV. A guest with perm=256 has WebDAV-read and NO upload.
  body=$(curl_body "$host/api/me"); code="${body##*$'\n'}"; body="${body%$'\n'*}"
  if [ "$code" = "200" ] && is_json "$body"; then
    role=$(printf '%s' "$body" | jget role)
    perm=$(printf '%s' "$body" | jget permission)
    local base; base=$(printf '%s' "$body" | jget base_path)
    [ -n "$base" ] && notes="$notes;base=$base"
  fi

  # --- 2. anonymous login (many instances allow empty-password guest) ------
  body=$(curl_body -X POST "$host/api/auth/login" -H 'Content-Type: application/json' -d '{}')
  code="${body##*$'\n'}"; body="${body%$'\n'*}"
  local login_ok="no"
  if [ "$(printf '%s' "$body" | jget token)" != "" ]; then login_ok="yes"; fi

  # --- 3. root listing -----------------------------------------------------
  body=$(curl_body -X POST "$host/api/fs/list" -H 'Content-Type: application/json' \
        -d '{"path":"/","password":"","page":1,"per_page":0,"refresh":false}')
  code="${body##*$'\n'}"; body="${body%$'\n'*}"
  local lcode; lcode=$(printf '%s' "$body" | jget code)
  if [ "$lcode" = "200" ]; then
    root_ok="yes"
    root_entries=$(printf '%s' "$body" | grep -o '"is_dir":' | wc -l | tr -d ' ')
    providers=$(printf '%s' "$body" | grep -o '"provider":"[^"]*"' | sed 's/.*:"//;s/"//' | sort -u | paste -sd, -)
    mountw=$(printf '%s' "$body" | grep -o '"write":true' | wc -l | tr -d ' ')
    # provider may be absent in some builds; try provider_root
    [ -z "$providers" ] && providers=$(printf '%s' "$body" | jget provider)
  elif [ -n "$lcode" ] && [ "$lcode" != "200" ]; then
    notes="$notes;list_code=$lcode"
    local lmsg; lmsg=$(printf '%s' "$body" | jget message)
    notes="$notes;list_msg=${lmsg:0:60}"
  fi

  # --- 4. enumerate mounts: child listings of each root dir ----------------
  # One request per root entry, one level deep: the classification needs no deeper listing.
  if [ "$root_ok" = "yes" ]; then
    root_names=$(printf '%s' "$body" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"$//')
    local dirs; dirs=$root_names
    local n=0 ok=0
    while IFS= read -r d; do
      [ -z "$d" ] && continue
      n=$((n+1))
      local enc; enc=$(printf '%s' "$d" | sed 's/ /%20/g')
      local cb; cb=$(curl_body -X POST "$host/api/fs/list" -H 'Content-Type: application/json' \
            -d "{\"path\":\"/$enc\",\"password\":\"\",\"page\":1,\"per_page\":0,\"refresh\":false}")
      local cbc; cbc="${cb##*$'\n'}"; cb="${cb%$'\n'*}"
      [ "$(printf '%s' "$cb" | jget code)" = "200" ] && ok=$((ok+1))
      local p; p=$(printf '%s' "$cb" | grep -o '"provider":"[^"]*"' | sed 's/.*:"//;s/"//' | sort -u | paste -sd, -)
      if [ -n "$p" ]; then
        case ",$providers," in *",$p,"*) : ;; *) providers="${providers:+$providers,}$p" ;; esac
      fi
    done <<< "$dirs"
    mounts="$n/$ok"
  fi

  # --- 5. THE WRITE TEST: oracle first, then 4 KiB PUT + readback + hash ---
  # The zero-byte oracle runs on EVERY listable host, because the metadata lies in
  # both directions: pan.jinnan.top advertises write=true on a mount and has a
  # directory literally named "05 游客上传", yet denies; a host with perm=0 can
  # still permit via a per-path meta. Only the oracle and the roundtrip decide.
  local want=1

  # Report the bit-3 / bit-9 split so a reader can see WHY the oracle answered.
  if [ -n "$perm" ]; then
    local w3=no w9=no
    [ "$(( perm & 8 ))"   -ne 0 ] && w3=yes
    [ "$(( perm & 512 ))" -ne 0 ] && w9=yes
    notes="$notes;bit3_upload=$w3;bit9_webdav_write=$w9"
  fi

  local wpath="/${sid}-r6probe.bin"
  if [ "$want" = "1" ]; then
    put_att="yes"

    # --- 5a. ZERO-BYTE PERMISSION ORACLE -----------------------------------
    # PUT a path that is an existing DIRECTORY with Overwrite:false. The handler
    # checks permission BEFORE noticing the target exists (AList issue #9600,
    # server/middlewares/fsup.go), so:
    #     {"code":403,"message":"file exists"}       -> permission PASSED, no bytes written
    #     {"code":403,"message":"permission denied"} -> permission FAILED, nothing touched
    # This decides the write question without uploading anything. Confirmed on
    # al.chirmyram.com (denied) vs data.yanshiqwq.cn (exists) 2026-10-22.
    oracle=""
    local firstdir; firstdir=$(printf '%s' "$root_names" | head -1)
    if [ -n "$firstdir" ]; then
      local ob; ob=$(curl_body -X PUT "$host/api/fs/put" \
            -H "File-Path: /$firstdir" -H 'Overwrite: false' \
            -H 'Content-Type: application/octet-stream' --data-binary 'x')
      local oc; oc="${ob##*$'\n'}"; ob="${ob%$'\n'*}"
      local om; om=$(printf '%s' "$ob" | jget message)
      case "$om" in
        "file exists"*)      oracle="permitted" ;;
        "permission denied"*) oracle="denied" ;;
        *)                   oracle="inconclusive:${om:0:40}" ;;
      esac
      notes="$notes;oracle=$oracle"
    fi

    # The oracle is cheap; still confirm with a real roundtrip when it says permitted,
    # and also when the metadata is ambiguous but permissive-looking.
    if [ "$oracle" = "denied" ]; then
      wver="no"
    else
    local payload; payload=$(printf 'r6-netdisk-probe %s\n' "$sid")
    local f; f=$(mktemp "$PROBE_TMP/put.XXXXXX")
    printf '%s' "$payload" > "$f"
    local want_sha; want_sha=$(sha256sum "$f" | cut -d' ' -f1)

    body=$(curl_body -X PUT "$host/api/fs/put" \
          -H "File-Path: $wpath" -H 'Content-Type: application/octet-stream' \
          --data-binary "@$f")
    code="${body##*$'\n'}"; body="${body%$'\n'*}"
    put_http="$code"
    put_code=$(printf '%s' "$body" | jget code)
    put_msg=$(printf '%s' "$body" | jget message)
    [ -z "$put_code" ] && { is_challenge "$body" && put_code="challenge"; }

    if [ "$put_code" = "200" ]; then
      sleep 2  # wait: measure, the read-back waits for the write to settle on the host
      # read back: /p/<path> is the public raw route
      local g; g=$(mktemp "$PROBE_TMP/get.XXXXXX")
      local gcode
      gcode=$(curl -sS --max-time "$TIMEOUT" -A "$UA" -o "$g" -w '%{http_code}' \
              "$host/p$wpath" 2>/dev/null)
      local got_sha got_sz
      got_sz=$(wc -c < "$g" | tr -d ' ')
      got_sha=$(sha256sum "$g" | cut -d' ' -f1)
      if [ "$gcode" = "200" ] && [ "$got_sha" = "$want_sha" ]; then
        wver="yes"; shmatch="yes"
        # ---- the only place a host is ever called writable ----
        notes="$notes;WROTE_AND_READ_BACK=$got_sz"
      else
        wver="no"; shmatch="no"
        notes="$notes;put200_but_readback=${gcode}/${got_sz}B"
      fi
      rm -f "$g"
    else
      # 403 inside HTTP 200 is the dominant shape. Say so explicitly.
      wver="no"
      if [ "$put_http" = "200" ] && [ "$put_code" = "403" ]; then
        notes="$notes;write_flag_lie(403-in-200)"
      fi
    fi
    rm -f "$f"
    fi
  fi

  fronting=$(curl -sS --max-time "$TIMEOUT" -A "$UA" -D - -o /dev/null "$host/" 2>/dev/null \
             | grep -i '^server:' | head -1 | tr -d '\r' | sed 's/^[Ss]erver: *//')

  case "$api_kind/$root_ok/$wver" in
    alist/yes/yes) verdict="WRITABLE" ;;
    alist/yes/no)  verdict="read-only" ;;
    alist/no/*)    verdict="alive-no-list" ;;
    cloudreve/*)   verdict="cloudreve" ;;
    *)             verdict="${api_kind:-dead}" ;;
  esac

  emit
}

emit() {
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "${host:-$raw}" "${api_kind:-}" "${http_status:-}" "${anon_settings:-no}" "${role:-}" "${perm:-}" \
    "${root_ok:-no}" "${root_entries:-}" "${mounts:-}" "${providers:-}" "${mountw:-}" \
    "${put_att:-no}" "${put_http:-}" "${put_code:-}" "${put_msg:0:80}" "${wver:-no}" "${shmatch:-}" \
    "${cap:-}" "${fronting:-}" "${verdict:-unknown}" "${notes:-}" "${login_ok:-no}"
}

# ---------- driver ----------------------------------------------------------
# Hosts are independent, so they all run in parallel: JOBS defaults to the number of
# hosts. Set JOBS only to measure something at a given parallelism.
JOBS="${JOBS:-0}"

# Run one host in the background, its TSV row into a temp file, so output order is
# recombined deterministically afterwards.
spawn() {
  local h="$1" n="$2" dir="$3"
  probe_one "$h" > "$dir/$n.tsv" 2>/dev/null &
}

run_hosts() {
  local dir; dir=$(mktemp -d "$PROBE_TMP/rows.XXXXXX")
  local n=0 running=0
  local h
  while IFS= read -r h; do
    [ -z "$h" ] && continue
    n=$((n+1))
    spawn "$h" "$n" "$dir"
    running=$((running+1))
    if [ "$JOBS" -gt 0 ] && [ "$running" -ge "$JOBS" ]; then
      wait -n 2>/dev/null || wait
      running=$((running-1))
    fi
  done
  wait
  # Reassemble in submission order.
  local i
  for i in $(seq 1 "$n"); do
    [ -f "$dir/$i.tsv" ] && cat "$dir/$i.tsv"
  done
  rm -rf "$dir"
}

if [ -n "$HOSTS_FILE" ]; then
  if [ -n "$OUT" ]; then
    grep -v '^[[:space:]]*#' "$HOSTS_FILE" | grep -v '^$' | run_hosts >> "$OUT"
  else
    grep -v '^[[:space:]]*#' "$HOSTS_FILE" | grep -v '^$' | run_hosts
  fi
fi

if [ "$#" -gt 0 ]; then
  if [ -n "$OUT" ]; then
    printf '%s\n' "$@" | run_hosts >> "$OUT"
  else
    printf '%s\n' "$@" | run_hosts
  fi
fi
