# Tasks: feat-075 — sdd-audit-lint-readonly

## Phase 1: VALIDATION

### V1: Validate design coherence

- [ ] Design at `artifacts/design/feat-075-sdd-audit-lint-readonly-design.md`
- [ ] 7 lint checks defined (E_TASKS_SKILLS_SECTION through E_PATHS_EXIST)
- [ ] Output format and exit codes defined
- [ ] Dependencies on feat-071, REPORT_ENVELOPE_POLICY, skills registry

### V2: Validate spec coherence

- [ ] Spec at `artifacts/specs/feat-075-sdd-audit-lint-readonly-spec.md`
- [ ] All 7 checks have severity, SKIP conditions, FAIL conditions
- [ ] SDT scenarios cover PASS and FAIL cases (6 scenarios)
- [ ] Out of scope respected

## Phase 2: TASKS → IMPLEMENT

### T1: Create sdd-audit-lint.ps1

**File**: `04_tools/sdd-audit-lint.ps1`

Script must implement:

#### T1.1: Parameter parsing

```powershell
param(
    [Parameter(ParameterSetName="ByPath")]
    [string]$FeatureRecordPath,
    
    [Parameter(ParameterSetName="ById")]
    [string]$FeatureId,
    
    [string]$RepoRoot = "",
    
    [ValidateSet("check", "report")]
    [string]$Mode = "report"
)
```

Resolve FeatureId to path: `features_for_specs/feat-{id}.json`

#### T1.2: Helper functions

- `New-LintResult()` → ordered hashtable with status, feature_id, checks[], errors[]
- `Add-Check()` → add check to results
- `Add-Error()` → add error
- `Get-RepoRoot()` → resolve repo root
- `Test-PathExists()` → check path exists relative to repo root
- `Get-TasksSkills()` → parse TASKS ## Skills section
- `Get-SkillsFromRegistry()` → get all skill names from registry
- `Get-ReportSections()` → parse report for required sections
- `Test-DoctorEvidence()` → check for doctor evidence in verify report
- `Test-ReportEnvelope()` → validate report has required sections
- `Test-ReportSurfaces()` → validate SURFACES section exists when applicable
- `Test-FeatureRecordCoherence()` → validate JSON consistency
- `Test-PathsExist()` → validate all referenced paths exist

#### T1.3: Implement E_TASKS_SKILLS_SECTION

- Read TASKS file
- Parse for `## Skills` section
- Validate table format: `| Task | Skills |` header + data rows
- If TASKS has skills in table → record declared skills

#### T1.4: Implement E_SKILLS_REGISTRY_EXISTS

- Load `00_project_documentation/SDD/03_operations/skills/skills_registry.json`
- Extract all `name` fields from skills[]
- Compare against declared skills from TASKS
- FAIL if any declared skill not in registry

#### T1.5: Implement E_DOCTOR_EVIDENCE

- If TASKS has declared skills (non-JUSTIFIED, non-empty):
  - Read verify report
  - Search for: `skills.ps1 doctor check`
  - Extract exit code or `status: ok` from JSON output
  - FAIL if not found or exit code ≠ 0

#### T1.6: Implement E_REPORT_ENVELOPE

- For each verify/audit report:
  - Read content
  - Check for required sections: INVOCATIONS, EVIDENCE, COMMANDS, VERDICT
  - FAIL if any missing

#### T1.7: Implement E_REPORT_SURFACES

- If feature JSON has `surfaces` array (non-empty):
  - Check verify report for `## SURFACES` section
  - FAIL if missing

#### T1.8: Implement E_FEATURE_RECORD_COHERENCE

- Validate state machine rules (see spec)
- Check validation_result, verification_result, audit_result values
- Check ARCHIVED → all results non-null
- Check IN_PROGRESS → all results null

#### T1.9: Implement E_PATHS_EXIST

- For each path in design_artifacts, spec_artifacts, etc.:
  - Resolve relative to RepoRoot
  - Check Test-Path exists
  - FAIL if any missing

#### T1.10: Output and exit

```powershell
$json = $result | ConvertTo-Json -Depth 10
Write-Output $json

if ($result.status -eq "ok") { exit 0 }
if ($result.status -eq "fail") {
    if ($result.errors.Count -gt 0 -and $result.errors[0].code -eq "E_USAGE") { exit 2 }
    exit 1
}
exit 2
```

### T2: Create golden tests (as markdown in verify report)

Document 4 test scenarios:

#### T2.1: PASS scenario (feat-074 as example)

Run lint against feat-074 (well-formed feature with skills + doctor evidence)

#### T2.2: FAIL scenario (skills declared, no doctor)

Create test TASKS with `GLOBAL: golang-testing` but no doctor evidence → E_DOCTOR_EVIDENCE fails

#### T2.3: FAIL scenario (unknown skill)

Create test TASKS with `GLOBAL: unknown-skill-xyz` → E_SKILLS_REGISTRY_EXISTS fails

#### T2.4: FAIL scenario (report missing SURFACES)

Feature with surfaces but verify report missing ## SURFACES → E_REPORT_SURFACES fails

## Phase 3: VERIFY

### V1: Run lint on feat-074 (PASS case)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\04_tools\sdd-audit-lint.ps1 -FeatureId feat-074 -Mode report
```

**Expected**: status = "ok", exit 0

### V2: Test FAIL scenarios

Test each FAIL scenario documented in T2.

### V3: Run full test

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\04_tools\sdd-audit-lint.ps1 -FeatureId feat-075 -Mode report
```

Verify all checks pass for the lint script itself.

## Phase 4: AUDIT

Generate audit report validating:
1. Script implements all 7 checks correctly
2. Exit codes are deterministic
3. No false positives or negatives
4. Golden tests demonstrate all scenarios

## Phase 5: ARCHIVE

Update feature JSON with timestamps and results.

## Skills

N/A — this is PowerShell scripting, no golang-testing skill needed.

## Dependencies

- feat-071 (Skills Structural Enforcement)
- REPORT_ENVELOPE_POLICY.md
- INTEGRATION_SURFACE_POLICY.md
- skills_registry.json
- feat-074 (used as PASS example in golden tests)
