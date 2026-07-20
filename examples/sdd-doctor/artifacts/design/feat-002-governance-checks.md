# Design: feat-002 — sdd-doctor Governance Checks

**Feature ID**: feat-002
**Type**: SYSTEM_SPEC
**Date**: 2026-04-26
**Status**: DRAFT

---

## 1. Context

### Purpose
sdd-doctor extends to validate SDD governance artifacts: feature records and validation gates. Ensures projects follow the framework's process contract.

### Relationship to feat-001
- feat-002 is additive to feat-001 (Core CLI Doctor)
- Both run within the same CLI tool
- New functionality: governance checks
- Existing functionality: core structure, config, artifact directory checks

### Constraints
- Same constraints as feat-001: Go stdlib only, single binary, human-readable output
- Deterministic behavior: same input produces same output

---

## 2. Goals

### Primary Goals
1. Detect feature records at `artifacts/features_for_specs/*.json`
2. Validate required fields in each feature record
3. Enforce validation gate: `validation_result = PASS` required when state is TASKS or later
4. Report findings with severity levels (PASS/WARN/FAIL/BLOCKED)

### Validation Gate Rule
```
If state is TASKS, IMPLEMENT, VERIFY, AUDIT, or ARCHIVE, then validation_result MUST equal "PASS".
```

### States Requiring validation_result = PASS:
- TASKS
- IMPLEMENT
- VERIFY
- AUDIT
- ARCHIVE

### States Not Requiring validation_result:
- DESIGN
- SPEC
- VALIDATION

---

## 3. Technical Approach

### Module Structure
```
github.com/CollSalvia-Org/sdd-framework/examples/sdd-doctor
├── cmd/sdd-doctor/main.go          (unchanged)
└── internal/doctor/
    ├── doctor.go                    (add checkGovernance method)
    └── governance.go                (NEW: governance validation logic)
```

### Build
```bash
go build ./cmd/sdd-doctor
```

### CLI Interface

Same as feat-001:
```
sdd-doctor check <path>
```

New findings are appended to the existing report.

### Error Codes

| Code | Type | Meaning | System Action |
|------|------|---------|---------------|
| G001 | Finding | Feature record JSON parse error | FAIL, continue |
| G002 | Finding | Missing required field | FAIL, continue |
| G003 | Finding | Validation gate violation (state requires validation_result=PASS) | FAIL, continue |
| G004 | Finding | Invalid or unknown state | FAIL, continue |
| G005 | Finding | Invalid field type | FAIL, continue |

---

## 4. Component Design

### `internal/doctor/governance.go` (NEW FILE)

**Responsibilities**:
- Scan `artifacts/features_for_specs/` directory
- Parse each JSON file
- Validate required fields
- Enforce validation gate rule
- Add findings to the Doctor instance

**Public API**:
```go
func (d *Doctor) checkGovernance()
```

**checkGovernance() Flow**:
1. Scan `artifacts/features_for_specs/*.json`
2. For each file:
   a. Read and parse JSON
   b. If parse error → FAIL (G001), continue
   c. Validate required fields (id, type, state, title, created_at, updated_at)
   d. Validate state is known
   e. If state is TASKS/IMPLEMENT/VERIFY/AUDIT/ARCHIVE:
      - Check validation_result == "PASS"
      - If not → FAIL (G003)
   f. If all valid → PASS

### Required Fields

Always required:
- `id` (string, non-empty)
- `type` (string, non-empty)
- `state` (string, one of allowed values)
- `title` (string, non-empty)
- `created_at` (string, ISO8601 format)
- `updated_at` (string, ISO8601 format)

Conditionally required:
- `validation_result` (string, must equal "PASS") when state is TASKS, IMPLEMENT, VERIFY, AUDIT, or ARCHIVE

### Allowed States
- DESIGN
- SPEC
- VALIDATION
- TASKS
- IMPLEMENT
- VERIFY
- AUDIT
- ARCHIVE

---

## 5. Finding Model

Same severity model as feat-001:
- PASS: Governance check succeeded
- WARN: Suspicious but not blocking
- FAIL: Governance violation
- BLOCKED: Reserved for future use

---

## 6. Report Format

Same format as feat-001, new findings appended:

```
=== SDD Doctor Report ===

Findings:

  [existing findings from feat-001 checks]
  ...

  ✓ [PASS] governance:artifacts/features_for_specs/feat-001.json: valid
  ✗ [FAIL] governance:artifacts/features_for_specs/feat-002.json: validation gate violation: state TASKS without validation_result=PASS

Summary: 18 PASS, 0 WARN, 2 FAIL, 0 BLOCKED
```

---

## 7. Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No feature records found | PASS (no governance to check) |
| Feature record with parse error | FAIL G001, continue |
| Feature record missing required field | FAIL G002, continue |
| Feature record in TASKS without validation_result | FAIL G003 |
| Feature record in TASKS with validation_result=PASS | PASS |
| Feature record with unknown state | FAIL G004 |
| Feature record with non-string type | FAIL G005 |

---

## 8. Integration Surfaces

| Surface | Used | Purpose |
|---------|------|---------|
| os_fs | Yes | Read feature record JSON files |
| os_args | No | Already handled by feat-001 |
| stdout | Yes | Report output |
| stderr | Yes | Error messages |
| process_exit | Yes | Exit codes |

All other surfaces: **false**

---

## 9. Traceability

| Requirement | Component |
|-------------|-----------|
| Feature record detection | governance.go:checkGovernance() |
| Schema validation | governance.go:validateFields() |
| Validation gate enforcement | governance.go:checkValidationGate() |
| State validation | governance.go:validateState() |
| Error code G001 | governance.go:handleParseError() |
| Error code G002 | governance.go:validateFields() |
| Error code G003 | governance.go:checkValidationGate() |
| Error code G004 | governance.go:validateState() |
| Error code G005 | governance.go:validateType() |

---

## 10. Dependencies

- feat-001: Must be implemented first (adds base CLI and doctor infrastructure)
- feat-002 is additive: does not modify feat-001 source

---

## 11. File Structure

```
examples/sdd-doctor/
├── go.mod
├── sdd.config.json
├── cmd/sdd-doctor/
│   └── main.go                 (unchanged)
├── internal/doctor/
│   ├── doctor.go               (add checkGovernance call)
│   └── governance.go           (NEW)
├── fixtures/
│   └── valid-project/          (update to include governance fixtures)
└── artifacts/
    ├── pre_sdd/
    │   └── seeds/
    │       └── 2026-04-26_governance_checks.md
    └── features_for_specs/
        ├── feat-001-core-doctor.json
        └── feat-002-governance-checks.json
```

---

## 12. Known Limitations

### From feat-001 (noted, not blocking):
- No unit test files yet
- E003 unreadable path scenario not exercised
- WARN scenario not exercised
- Fixture coverage estimated at 60%

### New in feat-002:
- Type validation is lenient (non-empty string only, not restricted to SYSTEM_SPEC)
- State transition history not validated
- ISO8601 format not validated (string presence only)