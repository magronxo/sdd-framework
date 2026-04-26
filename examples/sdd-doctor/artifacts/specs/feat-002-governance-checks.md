# Specification: feat-002 — sdd-doctor Governance Checks

**Feature ID**: feat-002
**Type**: SYSTEM_SPEC
**Date**: 2026-04-26
**Status**: DRAFT

---

## 1. Introduction

### Context
sdd-doctor extends to validate SDD governance artifacts: feature records and validation gates. Ensures projects follow the framework's process contract, not just structural conventions.

### Relationship to feat-001
- feat-002 is additive to feat-001 (Core CLI Doctor)
- Both run within the same CLI tool via `sdd-doctor check <path>`
- New functionality: governance checks
- Existing functionality: core structure, config, artifact directory checks

### Goals
1. Detect feature records at `artifacts/features_for_specs/*.json`
2. Validate required fields in each feature record
3. Enforce validation gate: `validation_result = PASS` required when state is TASKS or later
4. Report findings with severity levels (PASS/WARN/FAIL/BLOCKED)
5. Deterministic behavior: same input produces same output

### Non-Goals
- Auto-fix functionality
- State transition history validation
- Restricted type values (SYSTEM_SPEC only)
- ISO8601 format validation (presence only)
- JSON schema validation
- Network-based validation

---

## 2. Requirements

### Functional Requirements

#### RF-01: Feature Record Detection
The tool MUST check for the presence of JSON files in `artifacts/features_for_specs/`.
- If no files found: Add PASS finding for governance, continue
- If files found: Process each file

#### RF-02: Feature Record Parsing
For each JSON file in `artifacts/features_for_specs/`:
- Read file contents
- Parse as JSON
- On parse error: Add FAIL finding with error code G001, continue to next file

#### RF-03: Required Fields Validation
After successful parsing, validate these required fields are present and non-empty:
- `id` (string, non-empty)
- `type` (string, non-empty)
- `state` (string, non-empty)
- `title` (string, non-empty)
- `created_at` (string, non-empty)
- `updated_at` (string, non-empty)

If any required field is missing or empty:
- Add FAIL finding with error code G002
- Continue processing remaining fields

#### RF-04: State Validation
After required fields validation, validate `state` is one of the allowed values:
- DESIGN
- SPEC
- VALIDATION
- TASKS
- IMPLEMENT
- VERIFY
- AUDIT
- ARCHIVE

If state is unknown or invalid:
- Add FAIL finding with error code G004

#### RF-05: Type Validation
The `type` field MUST be a non-empty string.
- If type is empty string: Add FAIL finding with error code G005
- Note: No restriction on specific type values (SYSTEM_SPEC is conventional but not enforced)

#### RF-06: Validation Gate Enforcement
After state and type validation:

If state is TASKS, IMPLEMENT, VERIFY, AUDIT, or ARCHIVE:
- `validation_result` MUST exist and equal "PASS"
- If missing or not "PASS": Add FAIL finding with error code G003

If state is DESIGN, SPEC, or VALIDATION:
- `validation_result` is optional
- No failure if missing

#### RF-07: Finding Model
All governance validation results MUST be represented as `Finding` records (same model as feat-001):
```go
type Finding struct {
    Location string
    Severity Severity
    Code     string
    Message  string
}

type Severity string

const (
    SeverityPASS    Severity = "PASS"
    SeverityWARN    Severity = "WARN"
    SeverityFAIL    Severity = "FAIL"
    SeverityBLOCKED  Severity = "BLOCKED"
)
```

Severity semantics:
- **PASS**: Governance check succeeded
- **WARN**: Reserved for future use
- **FAIL**: Governance violation detected
- **BLOCKED**: Reserved for future use

#### RF-08: Terminal Report
Governance findings are appended to the existing report from feat-001 checks.

---

## 3. Error Codes

| Code | Type | Meaning | System Action |
|------|------|---------|---------------|
| G001 | Finding | Feature record JSON parse error | FAIL, continue to next file |
| G002 | Finding | Missing required field | FAIL, continue |
| G003 | Finding | Validation gate violation: state requires validation_result=PASS | FAIL, continue |
| G004 | Finding | Invalid or unknown state value | FAIL, continue |
| G005 | Finding | Invalid field type (empty string) | FAIL, continue |

---

## 4. Validation Gate Rule

```
IF state IN (TASKS, IMPLEMENT, VERIFY, AUDIT, ARCHIVE)
THEN validation_result MUST equal "PASS"
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

## 5. Inputs and Outputs

### Command Input
```
sdd-doctor check <path>
```

### Outputs

#### Report (stdout)
Same format as feat-001 with governance findings appended:
```
=== SDD Doctor Report ===

Findings:

  [existing findings from feat-001]
  ...

  ✓ [PASS] governance:artifacts/features_for_specs/feat-001.json: valid
  ✗ [FAIL] governance:artifacts/features_for_specs/feat-002.json: validation gate violation

Summary: X PASS, Y WARN, Z FAIL, W BLOCKED
```

#### Exit Codes
Same as feat-001:
| Code | Meaning |
|------|---------|
| 0 | No FAIL or BLOCKED findings |
| 1 | At least one FAIL or BLOCKED finding |
| 2 | Runtime error |

---

## 6. System Design

### Module Structure
```
github.com/magronxo/sdd-framework/examples/sdd-doctor
├── cmd/sdd-doctor/main.go          (unchanged)
└── internal/doctor/
    ├── doctor.go                   (modified: call checkGovernance)
    └── governance.go               (NEW: governance validation)
```

### Public API (additions)

```go
func (d *Doctor) checkGovernance()
```

### CLI Processing Flow

```
main()
  └─ doctor.Run(os.Args[1:])
       ├─ [existing feat-001 checks...]
       ├─ checkConfig()
       ├─ checkCoreDirectories()
       ├─ checkArtifactDirectories()
       └─ checkGovernance()        (NEW)
            ├─ Scan artifacts/features_for_specs/*.json
            ├─ For each file:
            │    ├─ Parse JSON
            │    ├─ Validate required fields
            │    ├─ Validate state
            │    ├─ Validate type
            │    ├─ Check validation gate
            │    └─ Add finding
            └─ Return
```

### Governance Validation Flow

```
checkGovernance()
  ├─ ReadDir(artifacts/features_for_specs/)
  ├─ If no files → add PASS finding, return
  └─ For each .json file:
       ├─ Read file
       ├─ json.Unmarshal()
       ├─ If error → FAIL (G001), continue
       ├─ Validate required fields
       │    └─ If missing → FAIL (G002), continue
       ├─ Validate state
       │    └─ If unknown → FAIL (G004), continue
       ├─ Validate type
       │    └─ If empty → FAIL (G005), continue
       ├─ If state IN (TASKS, IMPLEMENT, VERIFY, AUDIT, ARCHIVE):
       │    ├─ Check validation_result == "PASS"
       │    └─ If not → FAIL (G003)
       └─ If all valid → PASS
```

---

## 7. Acceptance Criteria

### Gherkin Scenarios

```gherkin
Feature: sdd-doctor Governance Validation

  Scenario: Valid feature record in DESIGN without validation_result
    Given a feature record with state DESIGN
    And no validation_result field
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the governance finding should be PASS

  Scenario: Valid feature record in TASKS with validation_result PASS
    Given a feature record with state TASKS
    And validation_result equals "PASS"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the governance finding should be PASS

  Scenario: Feature record in TASKS without validation_result PASS
    Given a feature record with state TASKS
    And validation_result is missing or not "PASS"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the governance finding should be FAIL
    And the error code should be G003

  Scenario: Feature record in IMPLEMENT without validation_result PASS
    Given a feature record with state IMPLEMENT
    And validation_result is missing or not "PASS"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the governance finding should be FAIL
    And the error code should be G003

  Scenario: Invalid feature record JSON
    Given a malformed JSON file in artifacts/features_for_specs/
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the governance finding should be FAIL
    And the error code should be G001

  Scenario: Feature record missing required field
    Given a feature record missing the "id" field
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the governance finding should be FAIL
    And the error code should be G002

  Scenario: Feature record with unknown state
    Given a feature record with state "INVALID_STATE"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the governance finding should be FAIL
    And the error code should be G004
```

---

## 8. Integration Surfaces

| Surface | Active | Purpose |
|---------|--------|---------|
| os_fs | Yes | Read feature record JSON files |
| os_args | No | Already handled by feat-001 |
| stdout | Yes | Report output |
| stderr | Yes | Error messages |
| process_exit | Yes | Exit codes |
| network | No | N/A |
| time | No | N/A |
| random | No | N/A |

---

## 9. Traceability Matrix

| ID | Requirement | Test Scenario |
|----|-------------|---------------|
| RF-01 | Feature record detection | Valid record in DESIGN |
| RF-02 | Feature record parsing | Invalid JSON |
| RF-03 | Required fields validation | Missing required field |
| RF-04 | State validation | Unknown state |
| RF-05 | Type validation | Empty type field |
| RF-06 | Validation gate enforcement | TASKS without validation_result=PASS |
| RF-07 | Finding model | All scenarios |
| RF-08 | Terminal report | All scenarios |

---

## 10. Dependencies

- feat-001: Must be implemented first (base CLI and doctor infrastructure)
- feat-002 is additive: does not modify feat-001 source

---

## 11. Known Limitations

### From feat-001 (noted, not blocking):
- No unit test files yet
- E003 unreadable path scenario not exercised
- WARN scenario not exercised
- Fixture coverage estimated at 60%

### New in feat-002:
- Type validation is lenient (non-empty string only)
- State transition history not validated
- ISO8601 format not validated (string presence only)
- No restrictions on specific type values