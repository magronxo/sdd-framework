# Design: feat-078-ci-sdd-audit-lint GitHub Actions

## Context

`feat-075` created `04_tools/sdd-audit-lint.ps1` as a standalone governance checker. `feat-077` added the `E_SEC_CONTROLS_MAP_REQUIRED` gate. Both features are archived. This change adds GitHub Actions CI to invoke the lint on PRs that touch feature records, eliminating governance drift between local development and CI.

## Approach

### CI Workflow Architecture

Single workflow file: `.github/workflows/sdd-audit-lint.yml`

Trigger matrix:
- `pull_request` (required): all PRs, filtered by changed-file step
- `push` to `main` (optional): catches merges, filtered by changed-file step

No `workflow_dispatch` (not needed for MVP).

No secrets, no action dependencies beyond `actions/checkout@v4`.

No matrix — runs serially per changed feature record (iterative `for_each` not needed at MVP scale).

### Step Breakdown

```
1. Checkout (fetch-depth: 0 for git diff)
2. Determine base ref for diff
3. Get changed files (git diff --name-only)
4. Filter to only features_for_specs/*.json
5. If empty → skip with log
6. For each record → pwsh sdd-audit-lint.ps1
```

### Changed Files Detection

PR context provides `${{ github.event.pull_request.base.sha }}` as the base.
Push to `main` uses `HEAD~1` as base (or `github.event.before` if available).

```bash
git diff --name-only $BASE_SHA $GITHUB_SHA
```

Filter: `00_project_documentation/SDD/artifacts/features_for_specs/*.json`

### Per-Record Lint Invocation

```yaml
- name: Run SDD audit lint
  shell: pwsh
  run: |
    $records = @(
        '00_project_documentation/SDD/artifacts/features_for_specs/feat-076.json',
        '00_project_documentation/SDD/artifacts/features_for_specs/feat-077.json'
    )
    foreach ($record in $records) {
        & pwsh -NoProfile -ExecutionPolicy Bypass -File ./04_tools/sdd-audit-lint.ps1 `
            -FeatureRecordPath $record `
            -Mode report `
            -UseGitDiff:$false
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
```

### Skip Logic

```yaml
if [ -z "$RECORDS" ]; then
    echo "No feature records changed; skipping"
    exit 0
fi
```

### Error Handling

- `exit 0` from lint → step succeeds
- `exit 1` (lint FAIL) → step fails, job fails
- `exit 2` (usage error, e.g. record not found) → step fails, job fails

### Why Not `-UseGitDiff:$true`?

The CI already computes changed files via `git diff`. Using `-UseGitDiff` would run a second git diff inside the script. Passing explicit paths via `-ImplementationFiles` is the right approach for CI determinism. The feature record itself already contains implementation paths, so the lint reads those from the record.

## Out of Scope

- Matrix strategy for parallel execution
- Artifact upload of lint JSON results
- `workflow_dispatch` manual trigger
- Enforcement of all features (only changed ones)
- Non-Ubuntu runners
