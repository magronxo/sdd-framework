# Tasks: feat-002 — sdd-doctor Governance Checks

**Feature ID**: feat-002
**Date**: 2026-04-26
**Status**: PENDING

---

## 1. Implementation Tasks

### Task 2.1: Create Governance Validation Module
- [ ] **2.1.1**: Create `internal/doctor/governance.go`
- [ ] **2.1.2**: Define `checkGovernance()` method on `Doctor`
- [ ] **2.1.3**: Implement `scanFeatureRecords()` to read `artifacts/features_for_specs/*.json`
- [ ] **2.1.4**: Implement `parseFeatureRecord()` to unmarshal JSON
- [ ] **2.1.5**: Implement `validateRequiredFields()` for id, type, state, title, created_at, updated_at
- [ ] **2.1.6**: Implement `validateState()` with allowed states list
- [ ] **2.1.7**: Implement `validateType()` (non-empty string check)
- [ ] **2.1.8**: Implement `checkValidationGate()` rule
- [ ] **2.1.9**: Add findings with error codes G001-G005

### Task 2.2: Integrate with Doctor
- [ ] **2.2.1**: Add call to `checkGovernance()` in `Doctor.Run()`
- [ ] **2.2.2**: Ensure governance findings appear in report output

### Task 2.3: Error Code Constants
- [ ] **2.3.1**: Define error code constants (G001, G002, G003, G004, G005)

---

## 2. Fixture Tasks

### Task 2.4: Governance Fixtures
- [ ] **2.4.1**: Create `fixtures/governance-test/valid-design/` with feature record in DESIGN state
- [ ] **2.4.2**: Create `fixtures/governance-test/valid-tasks/` with feature record in TASKS state and validation_result=PASS
- [ ] **2.4.3**: Create `fixtures/governance-test/invalid-gate/` with feature record in TASKS without validation_result=PASS
- [ ] **2.4.4**: Create `fixtures/governance-test/invalid-json/` with malformed JSON
- [ ] **2.4.5**: Create `fixtures/governance-test/missing-fields/` with missing required fields
- [ ] **2.4.6**: Create `fixtures/governance-test/invalid-state/` with unknown state

---

## 3. Verification Tasks

### Task 2.5: Build Verification
- [ ] **2.5.1**: Run `go build ./cmd/sdd-doctor`
- [ ] **2.5.2**: Verify binary exists

### Task 2.6: Governance Tests
- [ ] **2.6.1**: Test valid DESIGN record → exit 0, PASS
- [ ] **2.6.2**: Test valid TASKS with validation_result PASS → exit 0, PASS
- [ ] **2.6.3**: Test TASKS without validation_result PASS → exit 1, FAIL G003
- [ ] **2.6.4**: Test IMPLEMENT without validation_result PASS → exit 1, FAIL G003
- [ ] **2.6.5**: Test invalid JSON → exit 1, FAIL G001
- [ ] **2.6.6**: Test missing required field → exit 1, FAIL G002
- [ ] **2.6.7**: Test unknown state → exit 1, FAIL G004

---

## 4. SDT Scenario Mapping

| Scenario | Expected Result | Task |
|----------|---------------|------|
| Valid record in DESIGN | PASS, exit 0 | 2.6.1 |
| Valid record in TASKS with validation_result PASS | PASS, exit 0 | 2.6.2 |
| Record in TASKS without validation_result PASS | FAIL G003, exit 1 | 2.6.3 |
| Record in IMPLEMENT without validation_result PASS | FAIL G003, exit 1 | 2.6.4 |
| Invalid JSON | FAIL G001, exit 1 | 2.6.5 |
| Missing required field | FAIL G002, exit 1 | 2.6.6 |
| Unknown state | FAIL G004, exit 1 | 2.6.7 |

---

## 5. Dependencies

- Task 2.1 requires feat-001 doctor infrastructure
- Task 2.2 requires Task 2.1
- Tasks 2.4-2.6 require Tasks 2.1-2.2

---

## 6. Exit Criteria

Implementation is complete when:
- [ ] Tasks 2.1-2.3 completed
- [ ] Tasks 2.4 fixtures created
- [ ] Tasks 2.5-2.6 verification passed
- [ ] All 7 SDT scenarios pass