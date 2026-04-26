# Audit Report: feat-078-ci-sdd-audit-lint

## Goal

Add GitHub Actions CI workflow to invoke `sdd-audit-lint.ps1` on PRs that touch SDD feature records, eliminating governance drift.

## SURFACES

- `os_fs`: Write: `.github/workflows/sdd-audit-lint.yml` created
- `os_fs`: Read: `04_tools/sdd-audit-lint.ps1` (invoked, not modified)
- `env_gh_actions`: CI platform (workflow execution)

## INVOCATIONS

| # | Tool/Action | Purpose |
|---|-------------|---------|
| 1 | `mkdir -p .github/workflows` | Create workflow directory |
| 2 | Python YAML validation | Verify workflow syntax |

## EVIDENCE

### File created: `.github/workflows/sdd-audit-lint.yml`

```yaml
name: SDD Audit Lint
on:
  pull_request:
    paths:
      - '00_project_documentation/SDD/artifacts/features_for_specs/*.json'
  push:
    branches:
      - main
    paths:
      - '00_project_documentation/SDD/artifacts/features_for_specs/*.json'
jobs:
  sdd-audit-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: base
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            echo "sha=${{ github.event.pull_request.base.sha }}" >> $GITHUB_OUTPUT
          else
            echo "sha=${GITHUB_SHA}~1" >> $GITHUB_OUTPUT
          fi
      - id: changed
        run: |
          CHANGED=$(git diff --name-only ${{ steps.base.outputs.sha }} ${{ github.sha }} \
            | grep -E '^00_project_documentation/SDD/artifacts/features_for_specs/.*\.json$' \
            | tr '\n' ' ')
          echo "records=$CHANGED" >> $GITHUB_OUTPUT
          echo "Changed feature records: $CHANGED"
      - if: steps.changed.outputs.records == ''
        run: echo "No feature records changed; skipping"
      - if: steps.changed.outputs.records != ''
        shell: pwsh
        run: |
          $records = '${{ steps.changed.outputs.records }}' -split ' ' | Where-Object { $_ -ne '' }
          foreach ($record in $records) {
            Write-Host "Linting: $record"
            & pwsh -NoProfile -ExecutionPolicy Bypass -File ./04_tools/sdd-audit-lint.ps1 `
              -FeatureRecordPath $record `
              -Mode report `
              -UseGitDiff:$false
            if ($LASTEXITCODE -ne 0) {
              Write-Host "Lint failed for: $record (exit $LASTEXITCODE)"
              exit $LASTEXITCODE
            }
            Write-Host "Lint passed: $record"
          }
```

### YAML validation result

```
python -c "import yaml; yaml.safe_load(open('.github/workflows/sdd-audit-lint.yml')); print('YAML valid')"
â†’ YAML valid
```

## COMMANDS

| Command | Output |
|---------|--------|
| `mkdir -p .github/workflows` | Directory created |
| `python -c "import yaml; yaml.safe_load(open('.github/workflows/sdd-audit-lint.yml')); print('YAML valid')"` | YAML valid |

## VERDICT

**WARN** — Workflow created and YAML validated, but GitHub Actions execution evidence is not available in this environment.

### Spec compliance check

| Spec requirement | Status |
|-----------------|--------|
| Trigger on PR touching feature records | PASS (paths filter) |
| Trigger on push to main | PASS (paths filter) |
| Changed records via git diff | PASS |
| Filter to features_for_specs/*.json | PASS |
| Skip with exit 0 if none changed | PASS |
| Per-record lint invocation | PASS |
| Exit code propagation | PASS |
| No secrets | PASS |
| No external deps | PASS |

## ARTIFACTS CREATED

| Path | Purpose |
|------|---------|
| `.github/workflows/sdd-audit-lint.yml` | CI workflow |
| `00_project_documentation/SDD/artifacts/specs/feat-078-ci-sdd-audit-lint-spec.md` | Spec |
| `00_project_documentation/SDD/artifacts/design/feat-078-ci-sdd-audit-lint-design.md` | Design |
| `00_project_documentation/SDD/artifacts/tasks/feat-078-ci-sdd-audit-lint-tasks.md` | Tasks |
| `00_project_documentation/SDD/artifacts/features_for_specs/feat-078-ci-sdd-audit-lint.json` | Feature record |
| `00_project_documentation/SDD/audit_reports/audit_feat-078-ci-sdd-audit-lint_2026-04-18.md` | This report |

## NOTE

Workflow NOT executed in this environment (no GitHub Actions runner). Result marked WARN due to missing runtime evidence. Real execution evidence will come from the first PR that triggers the workflow.

