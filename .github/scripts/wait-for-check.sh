#!/usr/bin/env bash
set -euo pipefail

: "${BRANCH:?BRANCH is required}"

until WORKFLOW_RUN_ID=$(gh run list \
  --repo govuk-one-login/devplatform-demo-sam-app \
  --branch "$BRANCH" \
  --workflow "pre-merge-checks.yaml" \
  --json databaseId \
  --jq '.[0].databaseId') && [ -n "$WORKFLOW_RUN_ID" ]; do
  sleep 5
done

gh run watch "$WORKFLOW_RUN_ID" \
  --repo govuk-one-login/devplatform-demo-sam-app \
  --exit-status
