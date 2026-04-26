# Spec: feat-075 — sdd-audit-lint-readonly

## Purpose

Automated, deterministic governance lint for SDD features. Read-only checks that fail when skills gates, report envelope, or feature record coherence are violated.

## Interface

### Parameters

```
.\04_tools\sdd-audit-lint.ps1 -FeatureRecordPath <path> [-RepoRoot <path>] [-Mode check|report]
.\04_tools\sdd-audit-lint.ps1 -FeatureId <feat-XXX> [-RepoRoot <path>] [-Mode check|report]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `-FeatureRecordPath` | Yes (or FeatureId) | Path to feature JSON (absolute or repo-relative) |
| `-FeatureId` | Yes (or FeatureRecordPath) | Feature ID (resolves to `features_for_specs/feat-{id}.json`) |
| `-RepoRoot` | No | Defaults to script's parent parent |
| `-Mode` | No | `check` (errors only) or `report` (full JSON). Default: `report` |

### Output Format

```json
{
  "status": "ok|fail",
  "feature_id": "feat-XXX",
  "checks": [
    { "code": "E_TASKS_SKILLS_SECTION", "status": "PASS|FAIL", "details": "..." },
    { "code": "E_SKILLS_REGISTRY_EXISTS", "status": "PASS|FAIL", "details": "..." },
    { "code": "E_DOCTOR_EVIDENCE", "status": "PASS|FAIL", "details": "..." },
    { "code": "E_REPORT_ENVELOPE", "status": "PASS|FAIL", "details": "..." },
    { "code": "E_REPORT_SURFACES", "status": "PASS|FAIL", "details": "..." },
    { "code": "E_FEATURE_RECORD_COHERENCE", "status": "PASS|FAIL", "details": "..." },
    { "code": "E_PATHS_EXIST", "status": "PASS|FAIL", "details": "..." }
  ],
  "errors": [
    { "code": "E_XXX", "message": "..." }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed (`status: ok`) |
| 1 | Governance violation(s) found (`status: fail`) |
| 2 | Usage or configuration error (missing paths, invalid arguments) |

## Checks

### E_TASKS_SKILLS_SECTION

**What**: TASKS file contains `## Skills` section with valid table  
**Valid table**: `| Task | Skills |` header + at least one data row  
**Skipped if**: TASKS declares no skills (empty table is OK)  
**FAIL if**: TASKS exists but `## Skills` section missing or malformed

### E_SKILLS_REGISTRY_EXISTS

**What**: All skills declared in TASKS `## Skills` table exist in `skills_registry.json`  
**Registry**: `00_project_documentation/SDD/03_operations/skills/skills_registry.json`  
**SKIP if**: TASKS has no declared skills  
**FAIL if**: Any declared skill not in registry

### E_DOCTOR_EVIDENCE

**What**: If TASKS declares skills, verify report contains `skills.ps1 doctor check` evidence with exit code 0  
**Condition**: Only checks if TASKS `## Skills` table has at least one non-JUSTIFIED, non-empty skill  
**Evidence needed**: Verify report contains:
- Command: `powershell -NoProfile -ExecutionPolicy Bypass -File .\04_tools\skills.ps1 doctor check`
- Exit code: 0 (success)
- Or equivalent JSON output excerpt showing `status: ok`

**SKIP if**: TASKS declares no skills  
**FAIL if**: Skills declared but no doctor evidence, or exit code ≠ 0

### E_REPORT_ENVELOPE

**What**: Verify and audit reports contain required sections per `REPORT_ENVELOPE_POLICY.md`  
**Required sections**:
- `## INVOCATIONS`
- `## EVIDENCE`
- `## COMMANDS`
- `## VERDICT`
- `## SURFACES` (if surfaces apply)

**SKIP if**: No verify or audit reports exist (not required for all features)  
**FAIL if**: Report exists but missing critical section

### E_REPORT_SURFACES

**What**: Reports include `## SURFACES` when the feature has surface declarations  
**Check**: If feature JSON has `surfaces` array or TASKS mentions surfaces, verify report has `## SURFACES`  
**SKIP if**: Feature declares no surfaces  
**FAIL if**: Surfaces declared but `## SURFACES` section missing from report

### E_FEATURE_RECORD_COHERENCE

**What**: Feature record JSON is internally consistent  
**Rules**:
1. `validation_result` ∈ {PASS, FAIL, null}
2. `verification_result` ∈ {PASS, PARTIAL, FAIL, null}
3. `audit_result` ∈ {PASS, WARN, FAIL, null}
4. `state` ∈ {IN_PROGRESS, VALIDATED, VERIFIED, AUDITED, ARCHIVED}
5. If `state` = ARCHIVED → all three results should be non-null
6. If `state` = IN_PROGRESS → all three results should be null

**FAIL if**: Any rule violated

### E_PATHS_EXIST

**What**: All file paths in feature record exist on disk  
**Paths checked**:
- `design_artifacts[]`
- `spec_artifacts[]`
- `task_artifacts[]`
- `verify_artifacts[]`
- `audit_artifacts[]`
- `implementation.files_created[]`
- `implementation.files_modified[]`

**FAIL if**: Any referenced path does not exist

## Surfaces

| Surface | Applies | Evidence |
|---------|---------|----------|
| os_fs | Read-only file access for lint | All file reads are Get-Content/Test-Path |
| env_proxy | None required | Script has no external dependencies |

## SDT Scenarios

### SDT-075-01: All checks pass (PASS scenario)

- GIVEN a feature with proper TASKS ## Skills, skills in registry, doctor evidence, coherent JSON, existing paths
- WHEN lint runs
- THEN status = "ok", exit code 0, all checks PASS

### SDT-075-02: Skills declared but no doctor evidence (FAIL)

- GIVEN a feature with skills declared in TASKS but verify report missing doctor evidence
- WHEN lint runs
- THEN status = "fail", E_DOCTOR_EVIDENCE = FAIL, exit code 1

### SDT-075-03: Unknown skill in registry (FAIL)

- GIVEN a feature with TASKS declaring skill "unknown-skill-xyz" not in registry
- WHEN lint runs
- THEN status = "fail", E_SKILLS_REGISTRY_EXISTS = FAIL, exit code 1

### SDT-075-04: Report missing SURFACES (FAIL)

- GIVEN a feature that declares surfaces but verify report missing ## SURFACES
- WHEN lint runs
- THEN status = "fail", E_REPORT_SURFACES = FAIL, exit code 1

### SDT-075-05: Feature record incoherent (FAIL)

- GIVEN a feature with state=ARCHIVED but validation_result=null
- WHEN lint runs
- THEN status = "fail", E_FEATURE_RECORD_COHERENCE = FAIL, exit code 1

### SDT-075-06: Paths don't exist (FAIL)

- GIVEN a feature referencing non-existent paths
- WHEN lint runs
- THEN status = "fail", E_PATHS_EXIST = FAIL, exit code 1

### SDT-075-07: Usage error (exit 2)

- GIVEN invalid FeatureId or non-existent FeatureRecordPath
- WHEN lint runs
- THEN status = "fail", exit code 2

## Out of Scope

- Modifying sdd-audit.md or verifier.md
- Changing skills.ps1 doctor contract
- GitHub Actions integration
- Writing or modifying other feature artifacts
- Network calls or external dependencies
