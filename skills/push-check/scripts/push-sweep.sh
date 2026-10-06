#!/usr/bin/env bash
# push-sweep.sh: look for the faults a push carries that nobody sees in a diff.
# Usage: bash push-sweep.sh [repo-dir]     exit 0 clean · 1 findings · 3 not measured
# Checks: secrets in what is about to leave, a tracked .env, your own home folder in a
# tracked file, files too big for GitHub, and README/doc links to files that do not exist.
set -u
cd "${1:-.}" 2>/dev/null || { echo "NOT MEASURED: no such folder ${1:-.}"; exit 3; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "NOT MEASURED: not a git repo"; exit 3; }

files=$(git ls-files)
[ -n "$files" ] || { echo "NOT MEASURED: no tracked files, so nothing was scanned"; exit 3; }
count=$(printf '%s\n' "$files" | wc -l | tr -d ' ')
found=0
flag() { found=$((found+1)); echo "  ✗ $1"; }

echo "Scanning $count tracked files in $(pwd)"

# 1. Secrets. Values are never printed, only the file and line.
KEYPAT='(sk-ant-[A-Za-z0-9_-]{20,}|sk-(proj-)?[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'
while IFS= read -r f; do
  [ -f "$f" ] || continue
  grep -IqE "$KEYPAT" "$f" 2>/dev/null || continue
  lines=$(grep -nIE "$KEYPAT" "$f" | cut -d: -f1 | head -5 | tr '\n' ' ')
  flag "SECRET: $f line $lines(value hidden)"
done <<< "$files"

# 2. A tracked .env file.
printf '%s\n' "$files" | grep -E '(^|/)\.env($|\.)' | grep -vE '\.example$|\.sample$|\.template$' |
  while IFS= read -r f; do echo "  ✗ TRACKED .env: $f"; done | tee /tmp/push-sweep-env.$$ 
found=$((found + $(wc -l < /tmp/push-sweep-env.$$ | tr -d ' '))); rm -f /tmp/push-sweep-env.$$

# 3. Your own home folder written into a tracked file.
while IFS= read -r f; do
  [ -f "$f" ] || continue
  grep -Iq "$HOME/" "$f" 2>/dev/null && flag "YOUR HOME FOLDER: $f mentions $HOME (other people do not have it)"
done <<< "$files"

# 4. Files GitHub refuses (over 100MB) or warns about (over 50MB).
while IFS= read -r f; do
  [ -f "$f" ] || continue
  size=$(wc -c < "$f" | tr -d ' ')
  [ "$size" -gt 52428800 ] && flag "TOO BIG: $f is $((size/1048576))MB (GitHub warns at 50MB, refuses at 100MB)"
done <<< "$files"

# 5. Links in markdown files that point at a file not in the repo.
while IFS= read -r md; do
  dir=$(dirname "$md")
  grep -oE '\]\([^) ]+' "$md" 2>/dev/null | sed 's/^](//; s/[#?].*$//' | grep -vE '^([a-z]+:|$)' |
  while IFS= read -r link; do
    [ -z "$link" ] && continue
    case "$link" in /*) target=".${link}";; *) target="$dir/$link";; esac
    [ -e "$target" ] || echo "  ✗ DEAD LINK: $md points at $link"
  done
done < <(printf '%s\n' "$files" | grep -iE '\.md$') | tee /tmp/push-sweep-links.$$
found=$((found + $(wc -l < /tmp/push-sweep-links.$$ | tr -d ' '))); rm -f /tmp/push-sweep-links.$$

if [ "$found" -eq 0 ]; then echo "CLEAN: $count files, 5 checks, nothing found"; exit 0; fi
echo "FOUND $found problem(s). Fix them before you push."; exit 1
