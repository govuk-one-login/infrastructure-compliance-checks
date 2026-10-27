#!/bin/bash
set -euo pipefail

# Finds changed *.yaml/*.yml files (vs origin/main, excluding .github/)
# and sets GITHUB_OUTPUT: changed=true|false plus file-args (space-separated
# --file list). A failed git diff fails loudly rather than silently skipping.

if ! DIFF_OUT=$(git diff --name-only origin/main...HEAD -- '*.yaml' '*.yml' ':!.github'); then
  echo "Failed to find changed files against origin/main" >&2
  exit 1
fi

if [ -z "$DIFF_OUT" ]; then
  echo "changed=false" >> "$GITHUB_OUTPUT"
  exit 0
fi

echo "changed=true" >> "$GITHUB_OUTPUT"

mapfile -t FILES <<< "$DIFF_OUT"
FILE_ARGS=""
for f in "${FILES[@]}"; do
  FILE_ARGS="$FILE_ARGS --file $f"
done
echo "file-args=${FILE_ARGS# }" >> "$GITHUB_OUTPUT"
