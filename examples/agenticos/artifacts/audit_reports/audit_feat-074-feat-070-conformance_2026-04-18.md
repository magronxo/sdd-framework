# Audit Report: feat-074-feat-070-conformance

**Date**: 2026-04-18
**Feature**: feat-074-feat-070-conformance
**Target**: feat-070-chat-ticket-promotion-contract
**environment_mode**: execute
**audit_result**: PASS

## INVOCATIONS

- audit_engine: sdd-audit (manual)
- skill: none (doc-only audit)

## EVIDENCE

- Files read:
  - `00_project_documentation/SDD/artifacts/design/feat-074-feat-070-conformance-design.md`
  - `00_project_documentation/SDD/artifacts/specs/feat-074-feat-070-conformance-spec.md`
  - `00_project_documentation/SDD/artifacts/tasks/feat-074-feat-070-conformance-tasks.md`
  - `02_implementation/internal/api/handlers_llm_chat_test.go`
  - `00_project_documentation/SDD/audit_reports/verify_feat-074-feat-070-conformance_2026-04-18.md`
- Artefacts consulted:
  - feat-070 spec (conformance target)
  - feat-071 (Skills Structural Enforcement) - reference

## COMMANDS

- cwd: `02_implementation`
- command: `go test ./internal/api -count=1`
- status: EXECUTED
- raw_output: `ok  	agenticos/internal/api	4.931s`

## VERDICT

**PASS** — feat-074 successfully closes drift detected in feat-070.

1. Spec line 114 errata correctly documented (IT_OP auto mode → HTTP 202, not 200)
2. Tests now deterministic with t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())
3. Backpressure 429 test added with stub injection
4. Out of scope respected

## SURFACES

- browser: false
- os_fs: true
- wiring: false
- network: false
- env_proxy: true
- notes: Test environment uses t.Setenv for deterministic setup

## Conformance Issues Addressed

### Issue 1: Spec Line 114 Errata

**Location**: feat-070 spec, SDT "absent requested_mode defaults to auto (always)"

**Problem**: Spec stated "THEN HTTP 200" but IT_OP deniega llm_chat (Network). Per Surface Matrix, auto mode must fallback to ticket → HTTP 202.

**Resolution**: Documented in feat-074 spec as errata. Runtime behavior (handlers_dashboard.go:532) is correct.

**Audit Finding**: The feat-070 spec line 114 was incorrect. This is an errata, not a runtime bug.

### Issue 2: E_PATH_TRAVERSAL Bypass in Tests

**Location**: handlers_llm_chat_test.go lines 122, 151, 178

**Problem**: Tests "passed" by accepting E_PATH_TRAVERSAL as valid outcome.

**Resolution**: Removed bypass patterns. Added `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`.

**Audit Finding**: Tests are now deterministic and verify actual contract behavior.

### Issue 3: Missing Backpressure 429 Test

**Location**: handlers_llm_chat_test.go (no test for backpressure rejecting)

**Problem**: Spec SDT "backpressure rejecting returns 429" had no corresponding test.

**Resolution**: Added TestLLMChat_BackpressureRejecting_Returns429 with injected BackpressureProvider stub.

**Audit Finding**: Test passes, verifies 429 status, E_BACKPRESSURE_REJECTING error, and Retry-After header.

## Out of Scope Respected

- No changes to mode.go
- No changes to security semantics
- No changes to feat-070 validated/archived artifacts
- No new error codes or contract changes
- Production code unchanged (only test modifications)

## Dependencies Validated

| Dependency | Status | Notes |
|------------|--------|-------|
| feat-070 | PASS | Base contract (referenced, not modified) |
| feat-049 | PASS | guardian.SetMode works |
| feat-051 | PASS | guardian.SetEmergencyOverlay works |
| feat-052/feat-053 | PASS | Stub provider injects rejecting state |
| feat-055 | N/A | Not impacted |

## Files Modified

| File | Change |
|------|--------|
| `handlers_llm_chat_test.go` | Setup deterministic, remove E_PATH_TRAVERSAL bypass, add backpressure test |

## Compliance Matrix

| Check | Status |
|-------|--------|
| E_TASKS_SKILLS_SECTION | PASS |
| E_SKILLS_REGISTRY_EXISTS | PASS |
| E_DOCTOR_EVIDENCE | PASS (no skills declared) |
| E_REPORT_ENVELOPE | PASS |
| E_REPORT_SURFACES | PASS |
| E_FEATURE_RECORD_COHERENCE | PASS |
| E_PATHS_EXIST | PASS |
