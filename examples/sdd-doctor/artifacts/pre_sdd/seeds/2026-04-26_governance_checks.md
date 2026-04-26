# SEED: feat-002 — sdd-doctor Governance Checks

**Date**: 2026-04-26
**Type**: NEW_FEATURE
**Status**: DRAFT

---

## 1. Concept & Vision

Extends sdd-doctor to validate SDD governance artifacts: feature records and validation gates. Ensures projects follow the framework's process contract, not just structural conventions.

Governance validation answers: "Does this project follow the SDD process rules?"

---

## 2. Problem Statement

SDD framework requires specific process compliance:
- Feature records must have required fields and valid state transitions
- Validation gates require `validation_result: PASS` before entering TASKS or later states
- No feature should skip validation

Currently, these rules are not automatically enforced.

---

## 3. Feature Overview

### feat-002: Governance Checks
- Feature record detection and parsing
- Feature record schema validation (required fields)
- Validation gate enforcement (validation_result = PASS when state is TASKS or later)
- State validation

---

## 4. Constraints

Same as feat-001:
- Go 1.25, stdlib only
- Single static binary
- Human-readable output only
- Deterministic behavior

---

## 5. Dependencies

- feat-001: Core CLI Doctor (base functionality)
- feat-002 is additive; does not modify feat-001

---

## 6. Known Limitations from Previous Work

### feat-001 Coverage Gaps (accepted risk):
- No unit test files yet
- E003 unreadable path scenario not exercised
- WARN scenario not exercised
- Fixture coverage estimated at 60%

These gaps are recorded as known limitations and do not block feat-002 work.

---

## 7. Next Step

Author the **DESIGN** artifact following the SDD template.