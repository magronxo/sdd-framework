# Getting Started

> **Mode Diátaxis**: Tutorial

## Purpose

Take you from **zero** to your **first completed SDD feature** in one guided walkthrough.

This document assumes you have read `04_project_governance/PROJECT_MANIFEST.md` and `04_project_governance/GLOSSARY.md`. If you have not, start there.

---

## Before You Begin

### Prerequisites

1. You understand the project's philosophy and constraints (`PROJECT_MANIFEST.md`)
2. You know the terminology (`GLOSSARY.md`)
3. You have access to the repository

### What You Need

- A text editor
- Git (or equivalent version control)
- The ability to run the project's test suite (if applicable)

---

## Tutorial: Your First Feature

We will implement a trivial but complete feature: **"Add a health check endpoint"**. This demonstrates every phase of the SDD pipeline without overwhelming complexity.

---

## Step 0: Check the Seed (Pre-SDD)

Before any feature exists, someone captures a seed.

**Check**: Is there already a seed for this? Look in `03_operations/pre_sdd/seeds/`.

If not, the Product Owner or Reporter creates one using `templates/seed_dossier.md`.

For this tutorial, assume the seed has been **promoted** and a feature record exists.

---

## Step 1: Create the Feature Record

Create `artifacts/features_for_specs/feat-001-health-check.json`:

```json
{
  "id": "feat-001",
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",
  "title": "Add health check endpoint",
  "created_at": "2026-04-23T10:00:00Z",
  "updated_at": "2026-04-23T10:00:00Z",
  "seed_reference": "seeds/2026-04-23_idea_health_check.md"
}
```

**Checkpoint**: The file exists and `state` is `"DESIGN"`.

---

## Step 2: DESIGN — Define WHAT

**Role**: Designer

Create `artifacts/design/feat-001-health-check.md` using `templates/design.md`.

```markdown
# Design: Health Check Endpoint

## Problem
The system currently has no way for external monitors to verify it is alive.

## Goal
Provide a lightweight endpoint that returns the system's health status.

## Constraints
- Must not depend on external services (self-contained)
- Must respond in < 100ms
- Must return JSON

## Out of Scope
- Deep health checks (database connectivity, disk space)
- Authentication

## Acceptance Criteria
- [ ] GET /health returns 200 with `{ "status": "ok" }`
- [ ] Response time is < 100ms under normal load

## Open Questions
- None
```

Update the feature record:

```json
{
  "state": "SPEC",
  "design_path": "artifacts/design/feat-001-health-check.md"
}
```

**Checkpoint**: Design doc exists, feature record state is `"SPEC"`.

---

## Step 3: SPEC — Define HOW

**Role**: Specifier

Create `artifacts/specs/feat-001-health-check.md` using `templates/specs.md`.

```markdown
# Specification: Health Check Endpoint

## Requirements

### Functional
- **RF-01**: The system SHALL expose `GET /health`
- **RF-02**: The endpoint SHALL return HTTP 200
- **RF-03**: The response body SHALL be JSON: `{ "status": "ok" }`
- **RF-04**: The endpoint SHALL respond in < 100ms

### Non-Functional
- **RNF-01**: No external dependencies
- **RNF-02**: No authentication required

## Interface

```
GET /health

Response:
  Status: 200 OK
  Body: { "status": "ok" }
  Content-Type: application/json
```

## Error Handling
- None (endpoint always returns 200)

## SDT Scenarios

```gherkin
Scenario: Health check returns ok
  When I send GET /health
  Then the response status is 200
  And the response body is { "status": "ok" }
  And the response time is < 100ms
```

## Dependencies
- None
```

Update the feature record:

```json
{
  "state": "VALIDATION",
  "spec_path": "artifacts/specs/feat-001-health-check.md"
}
```

**Checkpoint**: Spec doc exists, feature record state is `"VALIDATION"`.

---

## Step 4: VALIDATION — Verify the Spec

**Role**: Validator

The Validator reads the design and spec, then produces a decision.

**Validation Checklist**:
- [ ] Completeness: All requirements traceable to acceptance criteria
- [ ] Determinism: No ambiguous behavior (e.g., what happens under load?)
- [ ] Implementability: Can be built with current stack
- [ ] No open questions: All `[?]` resolved

For this feature, all checks pass.

Update the feature record:

```json
{
  "state": "TASKS",
  "validation_result": "PASS",
  "validated_at": "2026-04-23T11:00:00Z"
}
```

**Checkpoint**: `validation_result` is `"PASS"`. **Do not proceed without this.**

---

## Step 5: TASKS — Break Down the Work

**Role**: Planner

Create `artifacts/tasks/feat-001-health-check.md`.

```markdown
# Tasks: Health Check Endpoint

## T1 — Add route handler
- Create `GET /health` handler in the router
- Return `{ "status": "ok" }` with `Content-Type: application/json`

## T2 — Add unit test
- Test that `GET /health` returns 200
- Test that response body matches `{ "status": "ok" }`
- Test that response time is < 100ms (mocked)

## T3 — Run tests
- Execute unit tests
- Verify all pass

## T4 — Update feature record
- Set state to `VERIFY`
```

Update the feature record:

```json
{
  "state": "IMPLEMENT",
  "task_path": "artifacts/tasks/feat-001-health-check.md",
  "task_list": [
    "Add route handler",
    "Add unit test",
    "Run tests",
    "Update feature record"
  ]
}
```

**Checkpoint**: Tasks doc exists, feature record state is `"IMPLEMENT"`.

---

## Step 6: IMPLEMENT — Write Code

**Role**: Implementer

Follow the tasks. Write minimal code that satisfies the spec.

Example (pseudo-code):

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}, 200, {"Content-Type": "application/json"}
```

Example test:

```python
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
```

Update the feature record:

```json
{
  "state": "VERIFY"
}
```

**Checkpoint**: Code exists, tests pass locally, feature record state is `"VERIFY"`.

---

## Step 7: VERIFY — Run Tests

**Role**: Verifier

Run the test suite and verify against the spec.

**Evidence**:
- All unit tests pass
- SDT scenario passes (manually or automated)
- No regressions in existing tests

Update the feature record:

```json
{
  "state": "AUDIT",
  "verification_result": "PASS",
  "verification_details": "All tests pass. Response time < 100ms verified."
}
```

**Checkpoint**: `verification_result` is `"PASS"`, feature record state is `"AUDIT"`.

---

## Step 8: AUDIT — External Review

**Role**: Auditor

The Auditor reads the spec, code, and tests, then produces a report.

Create `artifacts/audit_reports/audit_feat-001.md` following `02_policies/REPORT_ENVELOPE_POLICY.md`.

```markdown
# Audit Report: feat-001

- **feature_id**: feat-001
- **date**: 2026-04-23T12:00:00Z
- **environment_mode**: execute
- **audit_result**: PASS

## INVOCATIONS
- audit_engine: inline

## EVIDENCE
- Read: `artifacts/specs/feat-001-health-check.md`
- Read: `artifacts/tasks/feat-001-health-check.md`
- Read: implementation code
- Read: test code

## COMMANDS
- `pytest tests/test_health.py` — EXECUTED — all pass

## VERDICT
- **Result**: PASS
- **Reasons**: Spec is complete, implementation matches, tests cover SDT scenario.
- **next_action**: Archive feature

## SURFACES
- browser: false
- os_fs: false
- wiring: true
- network: false
- env_proxy: false
```

Update the feature record:

```json
{
  "state": "ARCHIVE",
  "audit_result": "PASS",
  "audit_reasons": ["Spec complete", "Implementation matches", "Tests cover SDT"]
}
```

**Checkpoint**: Audit report exists, `audit_result` is `"PASS"`, feature record state is `"ARCHIVE"`.

---

## Step 9: ARCHIVE — Close the Feature

**Role**: Archiver

Final state update:

```json
{
  "state": "ARCHIVE",
  "archived_at": "2026-04-23T13:00:00Z",
  "archive_notes": "Feature completed. Health check endpoint is live."
}
```

**Checkpoint**: Feature record is closed. All artifacts are preserved.

---

## Summary

You have now completed a full SDD feature:

| Phase | Artifact | State |
|-------|----------|-------|
| DESIGN | `artifacts/design/feat-001-health-check.md` | Done |
| SPEC | `artifacts/specs/feat-001-health-check.md` | Done |
| VALIDATION | Decision: PASS | Done |
| TASKS | `artifacts/tasks/feat-001-health-check.md` | Done |
| IMPLEMENT | Code + tests | Done |
| VERIFY | Decision: PASS | Done |
| AUDIT | `artifacts/audit_reports/audit_feat-001.md` | Done |
| ARCHIVE | Closed feature record | Done |

---

## Common Mistakes

### "I want to skip VALIDATION because the spec is obvious"

**Don't.** VALIDATION is a gate, not a formality. The Validator might catch:
- Missing error handling
- Ambiguous edge cases
- Dependencies you forgot

### "The spec needs a small fix during IMPLEMENT"

**Stop.** Reopen the spec, update it, and re-run VALIDATION. Never modify a validated spec during implementation.

### "I'll write the tests after I finish coding"

**Don't.** The Verifier needs tests to verify. Write tests as part of IMPLEMENT (TDD if your stack supports it).

### "This feature is too small for all this ceremony"

Check `02_policies/DECOMPOSITION_AND_SIZE_POLICY.md`. If it's truly trivial (< 50 lines, ≤ 2 requirements), it may be a "code adjustment" rather than a feature. But most work should flow through the pipeline.

---

## Next Steps

1. Read `docs/SDD_PIPELINE_VISUAL.md` to see the pipeline as diagrams
2. Read `docs/PROJECT_TOUR.md` for a visual overview of the repository
3. Pick up your second feature from `artifacts/tasks/` or `03_operations/pre_sdd/seeds/`

---

## Related Documents

- `04_project_governance/PROJECT_MAP.md` — full navigation guide
- `00_core/SDD_RUNTIME.md` — execution contract
- `00_core/SDD_GUIDE.md` — full methodology
- `AGENTS.md` — agent entrypoint
- `02_policies/REPORT_ENVELOPE_POLICY.md` — report format
- `02_policies/DECOMPOSITION_AND_SIZE_POLICY.md` — when to split/consolidate
