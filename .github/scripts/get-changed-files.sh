#!/bin/bash
set -euo pipefail

# Outputs a newline-separated list of changed *.yaml files against origin/main.
# Sets GITHUB_OUTPUT: changed=true|false, and file args suitable for checkov.

mapfile -t FILES < <(git diff --name-only origin/main...HEAD -- '*.yaml')

if [ ${#FILES[@]} -eq 0 ]; then
  echo "changed=false" >> "$GITHUB_OUTPUT"
  exit 0
fi

echo "changed=true" >> "$GITHUB_OUTPUT"

FILE_ARGS=""
for f in "${FILES[@]}"; do
  FILE_ARGS="$FILE_ARGS --file \"$f\""
done

echo "file-args=${FILE_ARGS# }" >> "$GITHUB_OUTPUT"
