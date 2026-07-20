# Specification: feat-003 — sdd-doctor Artifact Envelope Checks

**Feature ID**: feat-003
**Type**: SYSTEM_SPEC
**Date**: 2026-04-26
**Status**: DRAFT

---

## 1. Introduction

### Context
sdd-doctor extends to validate SDD artifact envelopes: the structural completeness of specs, validation reports, and audit reports. Ensures artifacts follow the framework's envelope conventions.

### Relationship to Previous Features
- feat-003 is additive to feat-001 (Core CLI Doctor) and feat-002 (Governance Checks)
- Both run within the same CLI tool via `sdd-doctor check <path>`
- New functionality: artifact envelope validation
- Existing functionality: core structure, config, governance checks

### Goals
1. Validate spec documents have required sections
2. Validate validation reports have required sections
3. Validate audit reports have required sections
4. Cross-reference validation (e.g., spec references design path)
5. Report findings with severity levels (PASS/WARN/FAIL/BLOCKED)
6. Deterministic behavior: same input produces same output

### Non-Goals
- Deep content validation (only envelope/structure)
- Auto-fix functionality
- JSON or machine-readable output
- Network-based validation

### Testing Requirement
**feat-003 SHOULD include Go unit tests.** For sdd-doctor, future features SHOULD include unit tests before archive. Exceptions must be explicitly documented in the audit report.

---

## 2. Artifact Envelope Definitions

### Spec Document Required Sections

A valid spec document MUST contain ALL of the following sections:

| Section | Description |
|---------|-------------|
| Introduction/Context | Explains the purpose and problem being solved |
| Goals or Objectives | Measurable goals the feature must achieve |
| Requirements | Numbered RF-* requirements |
| Inputs/Outputs | Command input format, expected outputs, exit codes |
| Error Codes | All error codes with meanings and system actions |
| Acceptance Criteria | Gherkin-formatted test scenarios |
| Integration Surfaces | Table of active/inactive surfaces |

### Validation Report Required Sections

A valid validation report MUST contain ALL of the following sections:

| Section | Description |
|---------|-------------|
| Completeness Checklist | Checks that all requirements are defined |
| Determinism Checklist | Checks for undefined behavior or vague terms |
| Traceability Checklist | Checks that RFs map to acceptance criteria |
| Implementability Checklist | Checks that implementation is feasible |
| Validation Decision | PASS or FAIL with reasoning |
| Feature Record Update | JSON snippet showing updated state |

### Audit Report Required Sections

A valid audit report MUST contain ALL of the following sections:

| Section | Description |
|---------|-------------|
| Spec-Code Alignment | Checks that implementation matches spec |
| Implementation Scope Check | Checks that scope was not exceeded |
| Test Coverage Analysis | Analyzes what was tested vs. required |
| Final Assessment | Summary of findings |
| Audit Decision | PASS/WARN/FAIL with recommendation |

---

## 3. Requirements

### Functional Requirements

#### RF-01: Spec Envelope Validation
For each `.md` file in `artifacts/specs/`:
- Read file contents
- Check for required sections (Context, Goals, Requirements, Inputs/Outputs, Error Codes, Acceptance Criteria, Integration Surfaces)
- If any required section is missing: Add FAIL finding with error code E010
- If all required sections present: Add PASS finding

#### RF-02: Validation Report Envelope Validation
For each `.md` file in `artifacts/validation_reports/`:
- Read file contents
- Check for required sections (Completeness Checklist, Determinism Checklist, Traceability Checklist, Implementability Checklist, Validation Decision, Feature Record Update)
- If any required section is missing: Add FAIL finding with error code E011
- If all required sections present: Add PASS finding

#### RF-03: Audit Report Envelope Validation
For each `.md` file in `artifacts/audit_reports/`:
- Read file contents
- Check for required sections (Spec-Code Alignment, Implementation Scope Check, Test Coverage Analysis, Final Assessment, Audit Decision)
- If any required section is missing: Add FAIL finding with error code E012
- If all required sections present: Add PASS finding

#### RF-04: Cross-Reference Validation
For each spec file:
- Extract design_path reference from spec
- Verify the referenced design file exists
- If reference is broken: Add FAIL finding with error code E013

#### RF-05: Finding Model
All envelope validation results MUST be represented as `Finding` records (same model as feat-001/feat-002):
```go
type Finding struct {
    Location string
    Severity Severity
    Code     string
    Message  string
}
```

Severity semantics:
- **PASS**: Envelope check succeeded
- **WARN**: Optional section missing (no required sections)
- **FAIL**: Required section missing
- **BLOCKED**: Reserved for future use

#### RF-06: Terminal Report
Envelope findings are appended to the existing report from feat-001 and feat-002 checks.

---

## 4. Error Codes

| Code | Type | Meaning | System Action |
|------|------|---------|---------------|
| E010 | Finding | Spec document missing required section | FAIL, continue to next section |
| E011 | Finding | Validation report missing required section | FAIL, continue to next section |
| E012 | Finding | Audit report missing required section | FAIL, continue to next section |
| E013 | Finding | Cross-reference mismatch (broken link) | FAIL, continue |
| W003 | Warning | Optional section missing | WARN, no impact |
| W004 | Warning | No matching artifact files found | WARN, no impact |

---

## 5. Inputs and Outputs

### Command Input
```
sdd-doctor check <path>
```

### Outputs

#### Report (stdout)
Same format as feat-001/feat-002 with envelope findings appended:
```
=== SDD Doctor Report ===

Findings:

  [existing findings from feat-001 and feat-002]
  ...

  ✓ [PASS] envelope:artifacts/specs/feat-001.md: spec envelope valid
  ✗ [FAIL] envelope:artifacts/specs/feat-002.md: spec missing required section: Acceptance Criteria

Summary: X PASS, Y WARN, Z FAIL, W BLOCKED
```

#### Exit Codes
Same as feat-001 and feat-002:
| Code | Meaning |
|------|---------|
| 0 | No FAIL or BLOCKED findings |
| 1 | At least one FAIL or BLOCKED finding |
| 2 | Runtime error |

---

## 6. System Design

### Module Structure
```
github.com/CollSalvia-Org/sdd-framework/examples/sdd-doctor
├── cmd/sdd-doctor/main.go               (unchanged)
└── internal/doctor/
    ├── doctor.go                        (add checkEnvelopes call)
    ├── governance.go                    (unchanged)
    ├── envelope.go                      (NEW)
    └── envelope_test.go                 (NEW - unit tests)
```

### Public API (additions)

```go
func (d *Doctor) checkEnvelopes()
func checkSpecEnvelope(content string) (bool, []string)
func checkValidationReportEnvelope(content string) (bool, []string)
func checkAuditReportEnvelope(content string) (bool, []string)
```

### CLI Processing Flow

```
main()
  └─ doctor.Run(os.Args[1:])
       ├─ [existing feat-001 checks...]
       │    ├─ checkConfig()
       │    ├─ checkCoreDirectories()
       │    └─ checkArtifactDirectories()
       ├─ [existing feat-002 checks...]
       │    └─ checkGovernance()
       └─ checkEnvelopes()               (NEW)
            ├─ Scan artifacts/specs/*.md
            │    ├─ For each: checkSpecEnvelope()
            │    └─ Add findings
            ├─ Scan artifacts/validation_reports/*.md
            │    ├─ For each: checkValidationReportEnvelope()
            │    └─ Add findings
            ├─ Scan artifacts/audit_reports/*.md
            │    ├─ For each: checkAuditReportEnvelope()
            │    └─ Add findings
            └─ Return
```

---

## 7. Acceptance Criteria

### Gherkin Scenarios

```gherkin
Feature: sdd-doctor Artifact Envelope Validation

  Scenario: Valid spec with all required sections
    Given a spec document with all required sections
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the envelope finding should be PASS for the spec

  Scenario: Spec missing Acceptance Criteria section
    Given a spec document missing "Acceptance Criteria"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the envelope finding should be FAIL
    And the error code should be E010

  Scenario: Valid validation report with all required sections
    Given a validation report with all required sections
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the envelope finding should be PASS for the validation report

  Scenario: Validation report missing Completeness Checklist
    Given a validation report missing "Completeness Checklist"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the envelope finding should be FAIL
    And the error code should be E011

  Scenario: Valid audit report with all required sections
    Given an audit report with all required sections
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the envelope finding should be PASS for the audit report

  Scenario: Audit report missing Audit Decision
    Given an audit report missing "Audit Decision"
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the envelope finding should be FAIL
    And the error code should be E012

  Scenario: Spec with broken cross-reference
    Given a spec that references a non-existent design document
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the envelope finding should be FAIL
    And the error code should be E013

  Scenario: No spec files found
    Given a project with no spec files
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the envelope finding should be WARN W004
    And the message should contain "no matching artifact files"
```

---

## 8. Unit Test Requirements

### Mandatory Tests for feat-003

The following unit tests MUST be implemented in `internal/doctor/envelope_test.go`:

1. **Test checkSpecEnvelope_AllSectionsPresent**
   - Input: spec content with all required sections
   - Expected: returns true, empty missing sections list

2. **Test checkSpecEnvelope_MissingSection**
   - Input: spec content missing "Acceptance Criteria"
   - Expected: returns false, contains "Acceptance Criteria" in missing list

3. **Test checkValidationReportEnvelope_AllSectionsPresent**
   - Input: validation report content with all required sections
   - Expected: returns true, empty missing sections list

4. **Test checkValidationReportEnvelope_MissingSection**
   - Input: validation report content missing "Completeness Checklist"
   - Expected: returns false, contains "Completeness Checklist" in missing list

5. **Test checkAuditReportEnvelope_AllSectionsPresent**
   - Input: audit report content with all required sections
   - Expected: returns true, empty missing sections list

6. **Test checkAuditReportEnvelope_MissingSection**
   - Input: audit report content missing "Audit Decision"
   - Expected: returns false, contains "Audit Decision" in missing list

7. **Test checkCrossReferences_ValidReference**
   - Input: spec content referencing existing design file
   - Expected: returns true

8. **Test checkCrossReferences_BrokenReference**
   - Input: spec content referencing non-existent design file
   - Expected: returns false

This is a local sdd-doctor quality convention. Exceptions must be explicitly documented in the audit report.

---

## 9. Integration Surfaces

| Surface | Active | Purpose |
|---------|--------|---------|
| os_fs | Yes | Read spec, validation, audit report files |
| os_args | No | Already handled by feat-001 |
| stdout | Yes | Report output |
| stderr | Yes | Error messages |
| process_exit | Yes | Exit codes |
| network | No | N/A |
| time | No | N/A |
| random | No | N/A |

---

## 10. Traceability Matrix

| ID | Requirement | Test Scenario |
|----|-------------|---------------|
| RF-01 | Spec envelope validation | Spec with all sections; Spec missing Acceptance Criteria |
| RF-02 | Validation report envelope validation | Validation report with all sections; Missing Completeness Checklist |
| RF-03 | Audit report envelope validation | Audit report with all sections; Missing Audit Decision |
| RF-04 | Cross-reference validation | Valid reference; Broken reference |
| RF-05 | Finding model | All scenarios |
| RF-06 | Terminal report | All scenarios |

---

## 11. Dependencies

- feat-001: Must be implemented (base CLI and doctor infrastructure)
- feat-002: Must be implemented (governance checks)
- feat-003 is additive: does not modify feat-001 or feat-002

---

## 12. Known Limitations

### From feat-001 (noted, not blocking):
- No unit test files yet
- E003 unreadable path scenario not exercised
- WARN scenario not exercised
- Fixture coverage estimated at 60%

### From feat-002 (noted, not blocking):
- Process deviation: implementation proceeded without explicit approval
- No unit tests
- IMPLEMENT-state fixture not created

### New in feat-003:
- Unit tests are encouraged but not mandatory (local sdd-doctor convention)
- Deep content validation not performed (only envelope/structure)