# Spec: feat-077 — sdd-audit-lint Security Controls Map Gate

## Purpose

Enforce that `SECURITY_CONTROLS_MAP.md` is reviewed when touching security-critical code paths. The `sdd-audit-lint.ps1` script (feat-075) gets a new check: `E_SEC_CONTROLS_MAP_REQUIRED`.

## Check: E_SEC_CONTROLS_MAP_REQUIRED

### Detection Sources (priority order)

1. **Explicit `-ImplementationFiles` parameter** (deterministic, highest priority)
   - `-ImplementationFiles @("path1","path2")`
   - If provided, use these paths directly

2. **`implementation_files` in feature record JSON** (fallback)
   - Read from `implementation_summary.implementation_files[]` if present
   - If absent, skip to step 3

3. **`-UseGitDiff` (PRO, optional)**
   - Run: `git diff --name-only <base>...HEAD`
   - Default base: `HEAD~1` (last commit)
   - If git fails (locks, permissions, no remote, detached HEAD), **SKIP the check silently** — do not block

### Security-Critical Path Heuristics

The following paths are considered security-critical (substring match):

| Pattern | Description |
|---------|-------------|
| `guardian.go` | Guardian policy enforcement |
| `executor.go` | Kernel execution |
| `handlers_security.go` | Security API handlers |
| `auth.go` | Authentication |
| `surface.go` | Surface authority |
| `handlers_kernel.go` | Kernel modes/overlays |
| `backpressure` | Backpressure/rejection logic |

Check applies if **any** implementation file path contains at least one of these patterns.

### Evidence Requirements

PASS if **at least one** is true:

1. **Verify report** contains `SECURITY_CONTROLS_MAP.md` in:
   - A `Files read` section, OR
   - A `## DOC UPDATES` section, OR
   - Any explicit reference to it

2. **Audit report** contains the same references to `SECURITY_CONTROLS_MAP.md`

3. **TASKS** contains a deterministic, parseable line:
   ```
   DOC: SECURITY_CONTROLS_MAP.md reviewed
   ```
   The detection is case-insensitive and the line must match the pattern `DOC:\s*SECURITY_CONTROLS_MAP\.md\s+reviewed` (regex).

### Check Result Values

| Value | Meaning |
|-------|---------|
| `PASS` | Check applies AND evidence found |
| `FAIL` | Check applies AND no evidence found |
| `SKIP` | Check does not apply (no security paths found, or cannot determine paths) |

### Global Lint Status

- `ok`: all checks are PASS or SKIP (no FAIL)
- `fail`: at least one check is FAIL
- Exit 0: all checks PASS or SKIP
- Exit 1: at least one FAIL
- Exit 2: usage/config error

## Implementation

### New Parameter

```powershell
param(
    [Parameter(ParameterSetName="ByPath")]
    [string]$FeatureRecordPath,

    [Parameter(ParameterSetName="ById")]
    [string]$FeatureId,

    [string]$RepoRoot = "",

    [ValidateSet("check", "report")]
    [string]$Mode = "report",

    [string[]]$ImplementationFiles = @(),   # NEW

    [switch]$UseGitDiff                         # NEW
)
```

### Security-Critical Patterns

```powershell
$securityPatterns = @(
    "guardian",
    "executor",
    "handlers_security",
    "auth",
    "surface",
    "handlers_kernel",
    "backpressure"
)
```

### Evidence Detection

```powershell
function Test-SecurityControlsMapEvidence {
    param([string]$VerifyContent, [string]$AuditContent, [string]$TasksContent)

    $patterns = @(
        "SECURITY_CONTROLS_MAP\.md",
        "DOC:\s*SECURITY_CONTROLS_MAP\.md\s+reviewed"
    )

    foreach ($content in @($VerifyContent, $AuditContent, $TasksContent)) {
        if ($content) {
            foreach ($pattern in $patterns) {
                if ($content -match $pattern) {
                    return $true, "Found evidence: $pattern"
                }
            }
        }
    }
    return $false, "No evidence found"
}
```

### New Check Addition

At the end of checks, add:

```powershell
$securityPaths = @()
foreach ($implFile in $implementationFiles) {
    foreach ($pattern in $securityPatterns) {
        if ($implFile -match $pattern) {
            $securityPaths += $implFile
            break
        }
    }
}

if ($securityPaths.Count -eq 0) {
    Add-Check $result "E_SEC_CONTROLS_MAP_REQUIRED" "SKIP" "No security-critical paths found"
} else {
    $found, $details = Test-SecurityControlsMapEvidence $verifyContent $auditContent $tasksContent
    if ($found) {
        Add-Check $result "E_SEC_CONTROLS_MAP_REQUIRED" "PASS" "$details (security paths: $($securityPaths -join ', '))"
    } else {
        Add-Check $result "E_SEC_CONTROLS_MAP_REQUIRED" "FAIL" "Security paths found but no SECURITY_CONTROLS_MAP.md evidence"
        Add-Error $result "E_SEC_CONTROLS_MAP_REQUIRED" "Feature touches security-critical paths ($($securityPaths -join ', ')) but no SECURITY_CONTROLS_MAP.md review evidence"
    }
}
```

## Test Fixtures

### Fixture 1: PASS case

**Feature JSON** (`fixtures/pass/feat-mock-sec.json`):
```json
{
  "feature_id": "feat-mock-sec",
  "title": "Mock security feature",
  "state": "ARCHIVED",
  "validation_result": "PASS",
  "verification_result": "PASS",
  "audit_result": "PASS",
  "implementation_summary": {
    "implementation_files": [
      "02_implementation/internal/kernel/guardian.go",
      "02_implementation/internal/api/handlers_security.go"
    ]
  },
  "verify_artifacts": ["fixtures/pass/verify_mock.md"],
  "audit_artifacts": ["fixtures/pass/audit_mock.md"]
}
```

**Verify report** (`fixtures/pass/verify_mock.md`):
```
...
## Files read
- SECURITY_CONTROLS_MAP.md
...
```

**Expected**: E_SEC_CONTROLS_MAP_REQUIRED → PASS

### Fixture 2: FAIL case

**Feature JSON** (`fixtures/fail/feat-mock-sec.json`):
```json
{
  "feature_id": "feat-mock-sec-fail",
  "title": "Mock security feature (no doc)",
  "state": "ARCHIVED",
  "validation_result": "PASS",
  "verification_result": "PASS",
  "audit_result": "PASS",
  "implementation_summary": {
    "implementation_files": [
      "02_implementation/internal/kernel/guardian.go"
    ]
  },
  "verify_artifacts": ["fixtures/fail/verify_mock.md"],
  "audit_artifacts": ["fixtures/fail/audit_mock.md"]
}
```

**Verify report** (`fixtures/fail/verify_mock.md`): no reference to SECURITY_CONTROLS_MAP.md

**Expected**: E_SEC_CONTROLS_MAP_REQUIRED → FAIL

### Fixture 3: SKIP case

**Feature JSON** (`fixtures/skip/feat-mock-normal.json`):
```json
{
  "feature_id": "feat-mock-normal",
  "title": "Mock normal feature",
  "state": "ARCHIVED",
  "validation_result": "PASS",
  "verification_result": "PASS",
  "audit_result": "PASS",
  "implementation_summary": {
    "implementation_files": [
      "02_implementation/internal/api/handlers_dashboard.go"
    ]
  },
  "verify_artifacts": ["fixtures/skip/verify_mock.md"]
}
```

**Expected**: E_SEC_CONTROLS_MAP_REQUIRED → SKIP (no security paths)

## Out of Scope

- Modifying `SECURITY_CONTROLS_MAP.md` itself
- Changes to existing lint checks
- GitHub Actions integration
- Non-PowerShell implementations

## Dependencies

- feat-075 (`sdd-audit-lint.ps1` baseline)
- `SECURITY_CONTROLS_MAP.md`
