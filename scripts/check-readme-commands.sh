#!/usr/bin/env bash
# verify-readme-commands.sh -- run every command scripts/README.md documents.
#
# WHY: a README that has never been executed is a README that documents a
# repository that does not exist. This is the mechanical version of "run what
# you wrote": it extracts each line from the bash blocks in the README, runs it,
# and records the exit code. A command that exits 2 is a usage error and is
# reported as a defect whatever the README claims. When the comment after a
# command names its exit codes ("# 0: 10 cases", "# 0 usable, 1 not, 4
# retryable", "# 0, or 1 while staleness is red"), any other code is a defect.
#
# Usage: sh scripts/check-readme-commands.sh [scripts/README.md]
#
# Exit: 0 every documented command exited with an acceptable code, 1 otherwise.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
README="${1:-$HERE/README.md}"

# The README's commands are relative to the repository root, which is the tree
# that holds scripts/. Find it from the README, not from this harness: the
# harness may live anywhere.
ROOT="$(cd "$(dirname "$README")" && pwd)"
case "$ROOT" in
  */scripts) ROOT="$(cd "$ROOT/.." && pwd)" ;;
esac
[ -d "$ROOT/scripts" ] || { echo "verify: no scripts/ under $ROOT" >&2; exit 2; }

# AGENTS.md section 2 rule 14: this evals every command the README documents (probe runs, broker reads, selftests),
# so it runs in CI or in an own clone, never in the research checkout, where 30 agents share one tree.
if [ -z "${CI:-}" ] && [ -e "$ROOT/.git" ]; then
  case "$(git -C "$ROOT" config --get rq.researchCheckout 2>/dev/null)" in
    [Tt][Rr][Uu][Ee])
      printf '%s\n' "check-readme-commands: this is the research checkout (git config rq.researchCheckout is true). It runs every command of the README, so it runs in CI or in an own clone, never here (AGENTS.md section 2 rule 14)." >&2
      exit 2 ;;
  esac
fi

# Rule 7: a script writes only inside .tmp/, sources/, dossier/ or a generated
# file. The transcript is scratch, so it goes under a folder of its own in .tmp/
# (an id folder, AGENTS.md section 2 rule 14), and never the tree.
WS_REL=".tmp/readme-check-$(date -u +%Y%m%dT%H%M%SZ)-$$"
WS="$ROOT/$WS_REL"
mkdir -p "$WS/probe"
OUT="${OUT:-$WS/exitcodes.txt}"
mkdir -p "$(dirname "$OUT")"
SC="$WS/verify.out"
SE="$WS/verify.err"

ok=0
bad=0
: > "$OUT"

in_block=0
while IFS= read -r line; do
  case "$line" in
    '```bash') in_block=1; continue ;;
    '```'*)    in_block=0; continue ;;
  esac
  [ "$in_block" = "1" ] || continue
  # Strip the comment that states the expected verdict; keep the command. The
  # codes the comment names are the codes this line may exit with.
  cmd="$(printf '%s' "$line" | sed 's/[[:space:]]*#.*$//')"
  note="$(printf '%s' "$line" | sed -n 's/^[^#]*#[[:space:]]*//p')"
  want="$(printf '%s' "$note" | grep -oE '(^|, |or )[0-4]([ :,]|$)' | grep -oE '[0-4]' | tr '\n' ' ')"
  printf '%s' "$cmd" | grep -q '[^[:space:]]' || continue

  # A URL placeholder is not runnable; substitute something hermetic.
  run="$(printf '%s' "$cmd" | sed 's/\bURL\b/https:\/\/example.com\//g; s/\bN\b/1024/g; s|\bDIR\b|'"$WS_REL"'/probe|g')"

  # This file's own invocation is in the README, because a reader should be able
  # to run the thing that checks the README. Running it from here recurses until
  # the disk fills, so it is checked structurally instead: does the documented
  # path exist and is it executable?
  case "$run" in
    *check-readme-commands.sh*)
      if [ -f "$ROOT/scripts/check-readme-commands.sh" ]; then
        printf '%-4s %s (not run: this harness)\n' "0" "$run" | tee -a "$OUT" >/dev/null
        ok=$((ok+1))
      else
        printf 'BAD  %-3s %s (documented script absent)\n' "2" "$run"
        bad=$((bad+1))
      fi
      continue ;;
  esac

  ( cd "$ROOT" && eval "$run" ) >"$SC" 2>"$SE"
  rc=$?
  printf '%-4s %s\n' "$rc" "$run" | tee -a "$OUT" >/dev/null

  # The contract's non-zero codes 1..4 are legitimate answers for some
  # commands (1 = a defect was found, 4 = the remote refused). 2 is not: it
  # means the command rejected its own arguments, so the README is wrong.
  if [ -n "$want" ]; then
    case " $want" in
      *" $rc "*) ok=$((ok+1)) ;;
      *) printf 'BAD  %-3s %s (the README names %s)\n' "$rc" "$run" "$want"
         printf '     %s\n' "$(head -2 "$SE" | tr '\n' ' ')"
         bad=$((bad+1)) ;;
    esac
    continue
  fi
  case "$rc" in
    0|1|3|4) ok=$((ok+1)) ;;
    *) printf 'BAD  %-3s %s\n' "$rc" "$run"
       printf '     %s\n' "$(head -2 "$SE" | tr '\n' ' ')"
       bad=$((bad+1)) ;;
  esac
done < "$README"

printf '\n%d command(s) answered with an acceptable exit code, %d did not\n' "$ok" "$bad"
printf 'exit codes recorded in %s\n' "$OUT"
[ "$bad" -eq 0 ] || exit 1
exit 0
