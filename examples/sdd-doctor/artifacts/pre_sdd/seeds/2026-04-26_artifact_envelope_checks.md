# SEED: feat-003 — sdd-doctor Artifact Envelope Checks

**Date**: 2026-04-26
**Type**: NEW_FEATURE
**Status**: DRAFT

---

## 1. Concept & Vision

Extends sdd-doctor to validate SDD artifact envelopes: the required sections and consistency rules for specs, validation reports, and audit reports. Ensures artifact quality and completeness.

Envelope validation answers: "Does this artifact contain all required sections?"

---

## 2. Problem Statement

SDD framework artifacts (specs, validation reports, audit reports) have required sections that must be present for the artifact to be valid. Currently, these are not automatically validated.

---

## 3. Feature Overview

### feat-003: Artifact Envelope Checks
- Spec document envelope validation (required sections)
- Validation report envelope validation
- Audit report envelope validation
- Cross-reference validation (e.g., spec references design path)

---

## 4. Dependencies

- feat-001: Core CLI Doctor (base functionality)
- feat-002: Governance Checks (feature record validation)
- feat-003 is additive; does not modify feat-001 or feat-002

---

## 5. Known Limitations from Previous Work

### feat-001 Coverage Gaps (accepted risk):
- No unit test files yet
- E003 unreadable path scenario not exercised
- WARN scenario not exercised
- Fixture coverage estimated at 60%

### feat-002 Process Deviation (recorded):
- Implementation proceeded without explicit human approval after validation
- Accepted because verification and audit passed successfully

### feat-003 Improvement: Testing Discipline
- feat-003 MUST include minimal Go unit tests
- Tests MUST cover core validation logic
- No feature shall be archived without passing tests

---

## 6. Constraints

Same as feat-001 and feat-002:
- Go 1.25, stdlib only
- Single static binary
- Human-readable output only
- Deterministic behavior

---

## 7. Non-Goals

- Auto-fix functionality
- JSON or machine-readable output
- Network-based validation
- Deep content validation (only envelope/structure)

---

## 8. Next Step

Author the **DESIGN** artifact following the SDD template.