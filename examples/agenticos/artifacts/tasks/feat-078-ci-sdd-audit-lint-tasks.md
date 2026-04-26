# Tasks: feat-078-ci-sdd-audit-lint

## Implementation Tasks

### Task 1: Create .github/workflows directory

- Create `.github/workflows/` directory structure
- Directory: `.github/workflows/`

### Task 2: Create sdd-audit-lint.yml workflow

- File: `.github/workflows/sdd-audit-lint.yml`
- Trigger: `pull_request` + `push` to `main`
- Steps:
  1. Checkout with `fetch-depth: 0`
  2. Determine base SHA (PR base vs HEAD~1 for push)
  3. `git diff --name-only` to get changed files
  4. Filter to `00_project_documentation/SDD/artifacts/features_for_specs/*.json`
  5. Skip if empty (log + exit 0)
  6. For each record: invoke `pwsh -NoProfile -ExecutionPolicy Bypass -File ./04_tools/sdd-audit-lint.ps1 -FeatureRecordPath $record -Mode report -UseGitDiff:$false`
  7. Propagate exit codes
- Runtime: `ubuntu-latest`, `pwsh`
- No secrets, no external action dependencies

## Verification Tasks

### Task 3: Validate YAML syntax

- Run YAML lint or validate workflow structure
- Confirm all required fields present

## Artifact Tasks

### Task 4: Create feature record JSON

- File: `00_project_documentation/SDD/artifacts/features_for_specs/feat-078-ci-sdd-audit-lint.json`
- State: ARCHIVED
- Results: all tasks completed

### Task 5: Create audit report

- File: `00_project_documentation/SDD/audit_reports/audit_feat-078-ci-sdd-audit-lint_2026-04-18.md`
- No verification report (no code changes to runtime)
