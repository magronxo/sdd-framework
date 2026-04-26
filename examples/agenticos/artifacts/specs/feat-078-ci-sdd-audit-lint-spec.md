# Delta for CI/CD — SDD Audit Lint GitHub Actions

## ADDED Requirements

### Requirement: CI Workflow Triggers

The system SHALL execute the SDD audit lint workflow on every pull request that modifies feature records, and on every push to `main`.

#### Scenario: PR touches feature records

- GIVEN a pull request is opened against `main`
- WHEN the PR modifies any file matching `00_project_documentation/SDD/artifacts/features_for_specs/*.json`
- THEN the lint workflow MUST trigger

#### Scenario: Push to main

- GIVEN a push event occurs on branch `main`
- WHEN any file is changed
- THEN the lint workflow MAY trigger (filter step applies)

### Requirement: Changed Feature Records Detection

The system MUST identify all changed feature record files using `git diff --name-only` against the PR base branch.

#### Scenario: PR with multiple changed feature records

- GIVEN a PR changes `feat-075.json` and `feat-076.json`
- WHEN the lint step executes
- THEN the workflow MUST run `sdd-audit-lint.ps1` once per changed record

### Requirement: Lint Execution Per Record

For each changed feature record, the system MUST execute:

```
pwsh -NoProfile -ExecutionPolicy Bypass \
  -File ./04_tools/sdd-audit-lint.ps1 \
  -FeatureRecordPath "<path>" \
  -Mode report \
  -UseGitDiff:$false
```

#### Scenario: Single feature record changed

- GIVEN exactly one feature record is changed
- WHEN the lint step runs
- THEN exactly one invocation of `sdd-audit-lint.ps1` occurs

#### Scenario: Feature record path contains spaces

- GIVEN a changed feature record path contains spaces
- WHEN the workflow executes the lint command
- THEN the path is passed correctly quoted

### Requirement: No Feature Records Changed — Skip with Pass

If no feature records are changed in the PR, the workflow MUST log a clear skip message and exit with status 0.

#### Scenario: PR touches only implementation files

- GIVEN a PR modifies only files under `02_implementation/`
- WHEN the lint workflow runs
- THEN the step outputs "No feature records changed; skipping" and exits 0

### Requirement: CI Exit Codes

The workflow MUST propagate lint exit codes to the GitHub Actions job.

- GIVEN `sdd-audit-lint.ps1` exits 0 for a feature record
- WHEN that record is linted
- THEN the workflow step succeeds

- GIVEN `sdd-audit-lint.ps1` exits 1 (lint failure) for any feature record
- WHEN that record is linted
- THEN the workflow step fails and the overall job fails

- GIVEN `sdd-audit-lint.ps1` exits 2 (usage error)
- WHEN that record is linted
- THEN the workflow step fails and the overall job fails

### Requirement: No External Dependencies

The workflow MUST NOT depend on GitHub Secrets, external actions requiring authentication, or any dependency installation step.

#### Scenario: Ubuntu runner with pwsh

- GIVEN the workflow runs on `ubuntu-latest`
- WHEN the lint step executes
- THEN only `pwsh` is required (installed via github hosted runner)

## REMOVED Requirements

None.

## MODIFIED Requirements

None.

## Acceptance Criteria

| ID | Criterion | Testable? |
|----|-----------|-----------|
| AC1 | Workflow triggers on PR touching `features_for_specs/*.json` | YES |
| AC2 | Workflow triggers on push to `main` | YES |
| AC3 | Changed feature records detected via `git diff --name-only` | YES |
| AC4 | Lint runs once per changed record | YES |
| AC5 | No changed records → "skip" log + exit 0 | YES |
| AC6 | Lint failure → workflow failure | YES |
| AC7 | No secrets, no external deps | YES |
