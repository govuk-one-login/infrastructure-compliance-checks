# infrastructure-compliance-checks
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The Security Checks repository holds a suite of custom policies designed to enforce security and compliance standards for application teams deploying through DevPlatform's Secure Pipelines.

The policies are written as [Checkov](https://www.checkov.io/) custom checks and are published as a reusable GitHub composite action so that any application repository can scan its own CloudFormation/SAM templates against them.

## What the action does

`actions/custom-checkov-policies` runs a Checkov scan of your templates using both the standard Checkov rule set and the custom DevPlatform checks in [`src/checks`](src/checks). In a single job step it:

1. Works out which `*.yaml` and `*.yml` files changed on the branch (`git diff --name-only origin/main...HEAD`) so only modified templates are scanned, excluding any files under `.github/`.
2. Installs Checkov on Python 3.12.
3. Runs Checkov against the changed files with custom DevPlatform checks, writing results to the console and to a uniquely named SARIF file.
4. Uploads `results-${{ github.run_id }}.sarif` to GitHub code scanning under the category `infrastructure-compliance-checks`. This runs on success or failure, so findings are always published.

A policy failure **fails the step and the pull request check**. Findings are printed in the job log and also appear in the repository's **Security → Code scanning** tab, annotated against the offending lines. To ship a template that a check flags, either fix the template or add a Checkov [inline suppression](https://www.checkov.io/2.Basics/). Teams should get security to review and sign off any inline suppressions (or [metadata](https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html#cloudformation-metadata)).

## Usage

Add the action as a step in an existing job that has already checked out your repository:

```yaml
jobs:
  pre-merge-checks:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write # required to upload the SARIF results
    steps:
      - name: Checkout
        uses: actions/checkout@v7
        with:
          fetch-depth: 0 # required so the action can diff against origin/main

      - name: Security checks
        uses: govuk-one-login/infrastructure-compliance-checks/actions/custom-checkov-policies@123456789ghsha # v1
        with:
          framework: cloudformation
```

### Inputs

| Input       | Required | Default          | Description                                                                                                     |
|-------------|----------|------------------|-----------------------------------------------------------------------------------------------------------------|
| `framework` | No       | `cloudformation` | The Checkov framework that matches your template type (e.g. `cloudformation` for SAM/CloudFormation templates). |
| `pull-repository` | No  | `false`          | Whether the action should checkout the calling repository before scanning. |

### Prerequisites

* `fetch-depth: 0` (or a fetch of `main`) is needed, otherwise the changed-files diff against `origin/main` cannot be resolved.
* `security-events: write` is needed for the SARIF upload. Without it the upload step fails even though the scan itself succeeded.

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest test/ -v
```

Each check lives in `src/checks` with shared template-parsing logic in `src/checks/helpers.py`. Tests live in `test/<check>/` with pass/fail CloudFormation fixtures under `fixtures/`; add a fixture per scenario and assert the expected `CheckResult`. To reproduce what the action runs, scan a template locally with:

```bash
checkov -f path/to/template.yaml \
  --framework cloudformation \
  --external-checks-dir src/checks/
```
