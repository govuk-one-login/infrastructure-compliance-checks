#!/usr/bin/env bash
set -euo pipefail

: "${PR_URL:?PR_URL is required}"

gh pr close "$PR_URL" \
  --repo govuk-one-login/devplatform-demo-sam-app \
  --delete-branch \
  --comment "Closed by automated integration test." || true
