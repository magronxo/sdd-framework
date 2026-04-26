# Tasks: feat-077 — sdd-audit-lint Security Controls Map Gate

## PHASE 1: SPEC + DESIGN

- [x] SPEC: feat-077-sdd-audit-lint-security-controls-map-gate-spec.md
- [x] DESIGN: feat-077-sdd-audit-lint-security-controls-map-gate-design.md
- [x] TASKS: feat-077-sdd-audit-lint-security-controls-map-gate-tasks.md (this file)
- [ ] Feature record: feat-077-sdd-audit-lint-security-controls-map-gate.json

## PHASE 2: Implementation

### Task 2.1: Add new parameters to sdd-audit-lint.ps1

**File**: `04_tools/sdd-audit-lint.ps1`
**Change**: Afegir `[string[]]$ImplementationFiles = @()` i `[switch]$UseGitDiff` al param block

### Task 2.2: Add Get-SecurityCriticalPaths function

**File**: `04_tools/sdd-audit-lint.ps1`
**Content**: Funció que filtra paths per patterns de seguretat

### Task 2.3: Add Get-GitDiffPaths function

**File**: `04_tools/sdd-audit-lint.ps1`
**Content**: Executa `git diff --name-only` i retorna paths, SKIP si falla

### Task 2.4: Add Test-SecurityControlsMapEvidence function

**File**: `04_tools/sdd-audit-lint.ps1`
**Content**: Cerca evidencia en verify report, audit report, TASKS

### Task 2.5: Add E_SEC_CONTROLS_MAP_REQUIRED check

**File**: `04_tools/sdd-audit-lint.ps1`
**Content**: Block de check al final amb SKIP/PASS/FAIL

## PHASE 3: Test Fixtures

### Task 3.1: Create pass fixtures

**Path**: `04_tools/sdd-audit-lint/fixtures/pass/`
**Files**: feat-mock-sec.json, verify_mock.md, audit_mock.md, TASKS.md

### Task 3.2: Create fail fixtures

**Path**: `04_tools/sdd-audit-lint/fixtures/fail/`
**Files**: feat-mock-sec.json, verify_mock.md, audit_mock.md, TASKS.md

### Task 3.3: Create skip fixtures

**Path**: `04_tools/sdd-audit-lint/fixtures/skip/`
**Files**: feat-mock-normal.json, verify_mock.md

## PHASE 4: Verification

### Task 4.1: Test PASS fixture

```powershell
./sdd-audit-lint.ps1 -FeatureId feat-mock-sec -RepoRoot ..\..
# E_SEC_CONTROLS_MAP_REQUIRED → PASS
```

### Task 4.2: Test FAIL fixture

```powershell
./sdd-audit-lint.ps1 -FeatureId feat-mock-sec-fail -RepoRoot ..\..
# E_SEC_CONTROLS_MAP_REQUIRED → FAIL
```

### Task 4.3: Test SKIP fixture

```powershell
./sdd-audit-lint.ps1 -FeatureId feat-mock-normal -RepoRoot ..\..
# E_SEC_CONTROLS_MAP_REQUIRED → SKIP
```

### Task 4.4: Run lint on feat-077 feature record

```powershell
./sdd-audit-lint.ps1 -FeatureId feat-077-sdd-audit-lint-security-controls-map-gate -RepoRoot ..\..
# Tots checks PASS o SKIP
```

## PHASE 5: Audit + Archive

- [ ] Generate verify report
- [ ] Generate audit report
- [ ] Update feature record → status: ARCHIVED

## Skills

Cap skill nou necessari — PowerShell scripting, ja cobert per feat-075.

## Verification Commands

```powershell
# Run lint on pass fixture
.\sdd-audit-lint.ps1 -FeatureRecordPath "fixtures\pass\feat-mock-sec.json"

# Run lint on fail fixture  
.\sdd-audit-lint.ps1 -FeatureRecordPath "fixtures\fail\feat-mock-sec.json"

# Run lint on skip fixture
.\sdd-audit-lint.ps1 -FeatureRecordPath "fixtures\skip\feat-mock-normal.json"
```
