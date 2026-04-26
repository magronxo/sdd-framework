# SDD Handoff Contract (Minimal, Runtime-First)

> **Mode Diátaxis**: Reference

## Purpose

Define *deterministic handoffs* between SDD roles so agents (and external models) can collaborate without role overlap, hidden state, or implied authority.

This contract is **operational**. It complements:
- `00_core/SDD_RUNTIME.md`
- `00_core/SDD_READING_CONTRACT.md`

---

## Canonical Handoff Chain

DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE

Each phase must produce exactly one primary output artifact (or a decision object), and must not do work from later phases.

---

## Global Rules (apply to every role)

- **No spec (validated) → no implementation.**
- **No role mixing:** do not produce artifacts owned by another role.
- **No silent contract drift:** if something is unclear, STOP and report ambiguity.
- **Paths are explicit:** use `artifacts/...` as canonical artifact roots (configurable via `sdd.config.json`).

---

## Role Contracts (Inputs → Outputs → Stop)

### Designer (DESIGN)

**Must read**
- Feature record: `artifacts/features_for_specs/<feature_id>.json`
- Related legacy/consolidated design notes only if needed

**Must produce**
- Design doc: `artifacts/design/<feature_id>.md`
- Update feature record state → `SPEC` and set `design_path`

**Must NOT**
- Write spec details (HOW), task breakdowns, or tests.

**STOP if**
- Any `[?]` open question blocks determinism.

---

### Specifier (SPEC)

**Must read**
- Design doc: `artifacts/design/<feature_id>.md`
- Feature record (for traceability fields)

**Must produce**
- Spec doc: `artifacts/specs/<feature_id>.md`
- Update feature record state → `VALIDATION` and set `spec_path`

**Must NOT**
- Generate tasks.
- Modify runtime / code.

**STOP if**
- The design is ambiguous (contains unresolved `[?]`).

---

### Validator (VALIDATION)

**Must read**
- Design doc
- Spec doc

**Must produce**
- A single decision object (PASS or FAIL). No other outputs.
- Record the decision in the feature record as `validation_result` + `validated_at` (and `validation_issues` on FAIL).

PASS → handoff to Planner (TASKS)
```json
{
  "state": "TASKS",
  "validation_result": "PASS",
  "notes": "Spec complete and deterministic"
}
```

FAIL → return to Specifier (SPEC)
```json
{
  "state": "SPEC",
  "validation_result": "FAIL",
  "issues": [
    "Missing error code list",
    "Ambiguous behavior on timeout"
  ]
}
```

**Must NOT**
- Modify spec/design.
- Generate tasks.
- Mark “done”.

**STOP if**
- Any doubt exists → FAIL (do not “patch” the spec).

---

### Planner (TASKS)

**Must read**
- Validated spec
- Feature record (for ids/paths)

**Must produce**
- Tasks doc: `artifacts/tasks/<feature_id>.md`

**Must NOT**
- Redesign or change behavior.
- Modify spec.

**STOP if**
- The spec is ambiguous or incomplete for execution.

---

### Implementer (IMPLEMENT)

**Must read**
- Tasks doc
- Validated spec (for acceptance + SDT)

**Must produce**
- Minimal code + tests that satisfy the spec.

**Must NOT**
- Modify spec/design.
- Expand scope beyond tasks/spec.

**STOP if**
- A task requires guessing behavior not defined by the spec.

---

### Verifier (VERIFY)

**Must read**
- Validated spec
- Tasks doc (expected coverage)
- Code + tests

**Must produce**
- A single decision object (PASS/FAIL). No other outputs.

PASS → handoff to Audit (AUDIT)
```json
{
  "state": "AUDIT",
  "verification_result": "PASS",
  "notes": "Implementation matches spec and SDT scenarios."
}
```

FAIL → return to Implementer (IMPLEMENT)
```json
{
  "state": "IMPLEMENT",
  "verification_result": "FAIL",
  "issues": [
    "SDT edge case not covered by tests",
    "Mismatch between spec error code and implementation"
  ]
}
```

**Must NOT**
- Fix code or rewrite tasks/spec.

---

### Auditor (AUDIT)

**Must read**
- Spec + code + tests (+ verification output if present)

**Must produce**
- Audit report: `artifacts/audit_reports/<report>.md`

**Must NOT**
- Modify code/spec.

**STOP if**
- N/A (audit reports findings; it does not block by itself).

---

### Archiver (ARCHIVE)

**Must read**
- Audit report
- Feature record + artifacts

**Must produce**
- A closed/archived feature record (state → `ARCHIVE`) plus any required trace updates.

**Must NOT**
- Rewrite specs retroactively without reopening states.
