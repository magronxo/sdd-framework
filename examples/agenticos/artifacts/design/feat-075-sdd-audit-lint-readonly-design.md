# Design: feat-075 — sdd-audit-lint-readonly

## Objective

Create a read-only PowerShell lint script (`sdd-audit-lint.ps1`) that deterministically checks governance compliance for a given feature, without modifying any artifacts.

## Problem

Currently, skills enforcement and report envelope compliance depend on human review or "following the prompt". There's no automated, deterministic gate that fails when:
- TASKS is missing `## Skills` section
- Skills declared don't exist in the registry
- Doctor evidence is missing when skills are declared
- Reports are missing required sections or SURFACES
- Feature record JSON is incoherent

## Solution

A read-only lint script that:
1. Accepts `-FeatureRecordPath` or `-FeatureId` (resolves to path)
2. Reads the feature JSON
3. Performs all governance checks
4. Outputs JSON result + exits with deterministic exit code

## Architecture

### Input

Either:
- `-FeatureRecordPath <path/to/feat-XXX.json>` (absolute or repo-relative)
- `-FeatureId feat-XXX` (resolves to `features_for_specs/feat-XXX.json`)

Optional:
- `-RepoRoot <path>` (defaults to script's parent parent)
- `-Mode check|report` (check = errors only, report = full JSON output)

### Output

```json
{
  "status": "ok|fail",
  "feature_id": "feat-XXX",
  "checks": [
    { "code": "E_TASKS_SKILLS_SECTION", "status": "PASS", "details": "..." },
    { "code": "E_SKILLS_REGISTRY_EXISTS", "status": "PASS", "details": "..." },
    ...
  ],
  "errors": [
    { "code": "E_XXX", "message": "..." }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Governance violation(s) found |
| 2 | Usage/config error (missing paths, invalid args) |

## Checks

### C1: TASKS Skills Section

**Check**: TASKS file exists and contains `## Skills` with valid table  
**Severity**: FAIL if missing  
**Evidence**: Parse TASKS for `## Skills` section, validate table format

### C2: Skills Registry Existence

**Check**: All skills declared in TASKS exist in `skills_registry.json`  
**Severity**: FAIL if unknown skill  
**Evidence**: Compare declared skills against registry names

### C3: Doctor Evidence (conditional)

**Check**: If TASKS declares skills, verify report contains doctor check evidence with exit 0  
**Severity**: FAIL if declared but no evidence  
**Condition**: Only applies if TASKS has `## Skills` with non-empty skills  
**Evidence**: Parse verify report for `skills.ps1 doctor check` command + exit code 0

### C4: Report Envelope

**Check**: Verify and audit reports contain required sections  
**Required sections** (per REPORT_ENVELOPE_POLICY):
- Header (feature_id, date, environment_mode, *_result)
- INVOCATIONS
- EVIDENCE
- COMMANDS
- VERDICT
- SURFACES

**Severity**: FAIL if critical section missing

### C5: Report SURFACES

**Check**: Reports include `## SURFACES` when applicable  
**Severity**: FAIL if surface applies but SURFACES missing  
**Evidence**: Check if feature declares surfaces and if report has SURFACES section

### C6: Feature Record Coherence

**Check**: JSON has consistent state machine:
- `validation_result` ∈ {PASS, FAIL, null}
- `verification_result` ∈ {PASS, PARTIAL, FAIL, null}
- `audit_result` ∈ {PASS, WARN, FAIL, null}
- `state` ∈ {IN_PROGRESS, VALIDATED, VERIFIED, AUDITED, ARCHIVED}
- If `state` = ARCHIVED → all three results should be non-null

**Severity**: FAIL if incoherent

### C7: Paths Exist

**Check**: All file paths referenced in feature record exist  
**Severity**: FAIL if any path missing  
**Evidence**: Resolve paths relative to RepoRoot, check existence

## File Structure

| File | Change |
|------|--------|
| `04_tools/sdd-audit-lint.ps1` | New — lint script |
| `artifacts/design/feat-075-sdd-audit-lint-readonly.md` | New |
| `artifacts/specs/feat-075-sdd-audit-lint-readonly.md` | New |
| `artifacts/tasks/feat-075-sdd-audit-lint-readonly.md` | New |

## No External Dependencies

The script runs locally without external dependencies:
- Reads JSON files (native PowerShell)
- Reads markdown files (native PowerShell)
- No network calls
- No external tools required

## Out of Scope

- Modifying sdd-audit.md or verifier.md
- Changing skills.ps1 doctor contract
- GitHub Actions integration
- Writing or modifying other feature artifacts
