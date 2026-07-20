# Design: feat-003 — sdd-doctor Artifact Envelope Checks

**Feature ID**: feat-003
**Type**: SYSTEM_SPEC
**Date**: 2026-04-26
**Status**: DRAFT

---

## 1. Context

### Purpose
sdd-doctor extends to validate SDD artifact envelopes: the structural completeness of specs, validation reports, and audit reports.

### Relationship to Previous Features
- feat-003 is additive to feat-001 (Core CLI Doctor) and feat-002 (Governance Checks)
- Both run within the same CLI tool via `sdd-doctor check <path>`
- New functionality: artifact envelope validation
- Existing functionality: core structure, config, governance checks

### Known Limitations from Previous Work

#### feat-001 Coverage Gaps (accepted risk)
- No unit test files yet
- E003 unreadable path scenario not exercised
- WARN scenario not exercised
- Fixture coverage estimated at 60%

#### feat-002 Process Deviation (recorded)
- Implementation proceeded without explicit human approval after validation
- Accepted because verification and audit passed successfully

### feat-003 Improvement: Testing Discipline
- feat-003 MUST include minimal Go unit tests
- Tests MUST cover core validation logic
- No feature shall be archived without passing tests
- This requirement applies to all future features as well

---

## 2. Goals

### Primary Goals
1. Validate spec documents have required sections
2. Validate validation reports have required sections
3. Validate audit reports have required sections
4. Cross-reference validation (e.g., spec references design path)
5. Report findings with severity levels (PASS/WARN/FAIL/BLOCKED)

### Non-Goals
- Deep content validation (only envelope/structure)
- Auto-fix functionality
- JSON or machine-readable output
- Network-based validation

---

## 3. Technical Approach

### Module Structure
```
github.com/CollSalvia-Org/sdd-framework/examples/sdd-doctor
├── cmd/sdd-doctor/main.go          (unchanged)
└── internal/doctor/
    ├── doctor.go                   (add checkEnvelopes call)
    ├── governance.go               (unchanged)
    └── envelope.go                 (NEW: envelope validation)
```

### Build
```bash
go build ./cmd/sdd-doctor
```

### CLI Interface

Same as feat-001 and feat-002:
```
sdd-doctor check <path>
```

New findings are appended to the existing report.

### Error Codes

| Code | Type | Meaning | System Action |
|------|------|---------|---------------|
| E010 | Finding | Spec document missing required section | FAIL, continue |
| E011 | Finding | Validation report missing required section | FAIL, continue |
| E012 | Finding | Audit report missing required section | FAIL, continue |
| E013 | Finding | Cross-reference mismatch | FAIL, continue |
| W003 | Warning | Optional section missing | WARN, no impact |

---

## 4. Artifact Envelope Definitions

### Spec Document Required Sections
A valid spec document MUST contain:
1. Introduction/Context section
2. Goals or Objectives
3. Requirements (RF-* numbered)
4. Inputs/Outputs section
5. Error Codes section
6. Acceptance Criteria (Gherkin scenarios)
7. Integration Surfaces table

### Validation Report Required Sections
A valid validation report MUST contain:
1. Completeness Checklist
2. Determinism Checklist
3. Traceability Checklist
4. Implementability Checklist
5. Validation Decision (PASS/FAIL)
6. Feature Record Update section

### Audit Report Required Sections
A valid audit report MUST contain:
1. Spec-Code Alignment section
2. Implementation Scope Check
3. Test Coverage Analysis
4. Final Assessment
5. Audit Decision (PASS/WARN/FAIL)

---

## 5. Cross-Reference Validation

For each feature:
- Spec's design_path must reference an existing design document
- Spec's validation_report_path must reference an existing validation report
- Feature record's spec_path must match actual spec location

---

## 6. Component Design

### `internal/doctor/envelope.go` (NEW FILE)

**Responsibilities**:
- Scan artifacts directory for specs, validation reports, audit reports
- Validate envelope sections for each artifact type
- Cross-reference validation
- Add findings to the Doctor instance

**Public API**:
```go
func (d *Doctor) checkEnvelopes()
```

**checkEnvelopes() Flow**:
1. Scan `artifacts/specs/*.md`
2. For each spec:
   a. Read file contents
   b. Check required sections present
   c. If missing section → FAIL (E010)
   d. Cross-reference validation
3. Scan `artifacts/validation_reports/*.md`
4. For each validation report:
   a. Read file contents
   b. Check required sections present
   c. If missing section → FAIL (E011)
5. Scan `artifacts/audit_reports/*.md`
6. For each audit report:
   a. Read file contents
   b. Check required sections present
   c. If missing section → FAIL (E012)

---

## 7. Finding Model

Same severity model as feat-001 and feat-002:
- PASS: Envelope check succeeded
- WARN: Optional section missing
- FAIL: Required section missing
- BLOCKED: Reserved for future use

---

## 8. Report Format

Same format as feat-001/feat-002, new findings appended:

```
=== SDD Doctor Report ===

Findings:

  [existing findings from feat-001 and feat-002]
  ...

  ✓ [PASS] envelope:artifacts/specs/feat-001.md: spec envelope valid
  ✗ [FAIL] envelope:artifacts/specs/feat-002.md: spec missing required section: Acceptance Criteria

Summary: X PASS, Y WARN, Z FAIL, W BLOCKED
```

---

## 9. Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No specs found | PASS (no envelopes to check) |
| Spec missing one required section | FAIL E010, continue |
| Spec missing multiple required sections | Multiple FAIL E010 |
| Validation report missing required section | FAIL E011 |
| Audit report missing required section | FAIL E012 |
| Cross-reference mismatch | FAIL E013 |
| Optional section missing | WARN W003 |

---

## 10. Integration Surfaces

| Surface | Used | Purpose |
|---------|------|---------|
| os_fs | Yes | Read spec, validation, audit report files |
| os_args | No | Already handled by feat-001 |
| stdout | Yes | Report output |
| stderr | Yes | Error messages |
| process_exit | Yes | Exit codes |

All other surfaces: **false**

---

## 11. Traceability

| Requirement | Component |
|-------------|-----------|
| Spec envelope validation | envelope.go:checkSpecEnvelopes() |
| Validation report envelope validation | envelope.go:checkValidationReportEnvelopes() |
| Audit report envelope validation | envelope.go:checkAuditReportEnvelopes() |
| Cross-reference validation | envelope.go:checkCrossReferences() |
| Error codes E010-E013 | envelope.go section validation |
| Error code W003 | envelope.go optional section check |

---

## 12. Dependencies

- feat-001: Must be implemented (base CLI and doctor infrastructure)
- feat-002: Must be implemented (governance checks)
- feat-003 is additive: does not modify feat-001 or feat-002

---

## 13. Testing Requirement

### Mandatory for feat-003

feat-003 MUST include Go unit tests covering:
1. Section presence validation (spec has required sections)
2. Section presence validation (validation report has required sections)
3. Section presence validation (audit report has required sections)
4. Cross-reference validation
5. Error code mapping

This requirement establishes precedent:
**All future features MUST include passing unit tests before archive.**

---

## 14. File Structure

```
examples/sdd-doctor/
├── go.mod
├── sdd.config.json
├── cmd/sdd-doctor/
│   └── main.go                     (unchanged)
├── internal/doctor/
│   ├── doctor.go                  (add checkEnvelopes call)
│   ├── governance.go              (unchanged)
│   └── envelope.go                (NEW)
├── internal/doctor/
│   └── envelope_test.go           (NEW - unit tests)
└── artifacts/
    ├── features_for_specs/
    │   ├── feat-001-core-doctor.json
    │   ├── feat-002-governance-checks.json
    │   └── feat-003-artifact-envelope-checks.json
    ├── design/
    ├── specs/
    ├── validation_reports/
    ├── audit_reports/
    └── tasks/
```

---

## 15. Known Limitations

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
- Unit tests are mandatory (establishing precedent)
- Deep content validation not performed (only envelope/structure)