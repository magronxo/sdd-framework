# Tasks: feat-003 — sdd-doctor Artifact Envelope Checks

**Feature ID**: feat-003
**Date**: 2026-04-26
**Status**: PENDING

---

## 1. Implementation Tasks

### Task 3.1: Create Envelope Validation Module
- [ ] **3.1.1**: Create `internal/doctor/envelope.go`
- [ ] **3.1.2**: Define `checkEnvelopes()` method on `Doctor`
- [ ] **3.1.3**: Implement `checkSpecEnvelopes()` to scan `artifacts/specs/*.md`
- [ ] **3.1.4**: Implement `checkValidationReportEnvelopes()` to scan `artifacts/validation_reports/*.md`
- [ ] **3.1.5**: Implement `checkAuditReportEnvelopes()` to scan `artifacts/audit_reports/*.md`
- [ ] **3.1.6**: Implement `checkCrossReferences()` to validate design path references
- [ ] **3.1.7**: Add findings with error codes E010-E013, W003-W004

### Task 3.2: Integrate with Doctor
- [ ] **3.2.1**: Add call to `checkEnvelopes()` in `Doctor.Run()`
- [ ] **3.2.2**: Ensure envelope findings appear in report output

### Task 3.3: Error Code Constants
- [ ] **3.3.1**: Define error code constants (E010, E011, E012, E013, W003, W004)

---

## 2. Unit Test Tasks

### Task 3.4: Create Unit Tests
- [ ] **3.4.1**: Create `internal/doctor/envelope_test.go`
- [ ] **3.4.2**: Test `checkSpecEnvelope_AllSectionsPresent`
- [ ] **3.4.3**: Test `checkSpecEnvelope_MissingSection`
- [ ] **3.4.4**: Test `checkValidationReportEnvelope_AllSectionsPresent`
- [ ] **3.4.5**: Test `checkValidationReportEnvelope_MissingSection`
- [ ] **3.4.6**: Test `checkAuditReportEnvelope_AllSectionsPresent`
- [ ] **3.4.7**: Test `checkAuditReportEnvelope_MissingSection`
- [ ] **3.4.8**: Test `checkCrossReferences_ValidReference`
- [ ] **3.4.9**: Test `checkCrossReferences_BrokenReference`
- [ ] **3.4.10**: Run `go test ./...` and verify all tests pass

---

## 3. SDT Scenario Mapping

| Scenario | Expected Result | Task |
|----------|---------------|------|
| Valid spec with all sections | PASS, exit 0 | 3.4.2 |
| Spec missing Acceptance Criteria | FAIL E010, exit 1 | 3.4.3 |
| Valid validation report | PASS, exit 0 | 3.4.4 |
| Validation report missing Completeness Checklist | FAIL E011, exit 1 | 3.4.5 |
| Valid audit report | PASS, exit 0 | 3.4.6 |
| Audit report missing Audit Decision | FAIL E012, exit 1 | 3.4.7 |
| Spec with broken cross-reference | FAIL E013, exit 1 | 3.4.9 |
| No spec files found | WARN W004, exit 0 | 3.1.3 |

---

## 4. Dependencies

- Task 3.1 requires feat-001 and feat-002 infrastructure
- Task 3.2 requires Task 3.1
- Task 3.3 can run in parallel with Task 3.1
- Task 3.4 requires Task 3.1

---

## 5. Exit Criteria

Implementation is complete when:
- [ ] Tasks 3.1-3.3 completed
- [ ] Tasks 3.4 unit tests created
- [ ] `go test ./...` passes
- [ ] All 8 SDT scenarios pass