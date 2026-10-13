#!/usr/bin/env bash
set -euo pipefail

: "${BRANCH:?BRANCH is required}"
: "${RUN_ID:?RUN_ID is required}"
: "${REPOSITORY:?REPOSITORY is required}"
: "${SHA:?SHA is required}"

PR_URL=$(gh pr create \
  --repo govuk-one-login/devplatform-demo-sam-app \
  --title "DO NOT MERGE - FOR TESTING ONLY: checkov policies GitHub Action test #${RUN_ID}" \
  --body "Please do not merge. This is an an automated intergration test from ${REPOSITORY}@${SHA}." \
  --base main \
  --head "$BRANCH")
echo "pr_url=$PR_URL" >> "$GITHUB_OUTPUT"
