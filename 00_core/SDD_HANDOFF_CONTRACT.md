# SDD Handoff Contract (Minimal, Runtime-First)

> **Mode Diátaxis**: Reference

## Purpose

Define deterministic handoffs between SDD roles so agents and external models can collaborate without role overlap, hidden state, or implied authority.

This contract is operational. It complements:

- `docs/sdd/00_core/SDD_RUNTIME.md`
- `docs/sdd/00_core/SDD_READING_CONTRACT.md`

---

## Install Context

Canonical installed location:

```text
docs/sdd/
```

Default generated artifacts:

```text
docs/sdd/artifacts/
```

Product source code lives outside `docs/sdd/`.

---

## Canonical Handoff Chain

DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE

Each phase must produce exactly one primary output artifact or decision object, and must not do work from later phases.

---

## Global Rules

- No validated spec → no implementation.
- No role mixing.
- No silent contract drift.
- Paths are explicit and resolved through `docs/sdd/sdd.config.json`.
- Examples are educational only and never authority.
- `AUDIT FAIL` blocks archive/final acceptance/release gates unless explicitly waived by the project owner.

---

## Role Contracts

### Designer (DESIGN)

**Must read**

- Feature record: `docs/sdd/artifacts/features_for_specs/<feature_id>.json`
- Related legacy/consolidated design notes only if needed

**Must produce**

- Design doc: `docs/sdd/artifacts/design/<feature_id>.md`
- Update feature record state → `SPEC` and set `design_path`

**Must NOT**

- Write spec details, task breakdowns, tests, or product code.

**STOP if**

- Any `[?]` open question blocks determinism.

---

### Specifier (SPEC)

**Must read**

- Design doc: `docs/sdd/artifacts/design/<feature_id>.md`
- Feature record for traceability fields

**Must produce**

- Spec doc: `docs/sdd/artifacts/specs/<feature_id>.md`
- Update feature record state → `VALIDATION` and set `spec_path`

**Must NOT**

- Generate tasks.
- Modify runtime or product code.

**STOP if**

- The design is ambiguous or contains unresolved `[?]`.

---

### Validator (VALIDATION)

**Must read**

- Design doc
- Spec doc

**Must produce**

- A single decision object: PASS or FAIL.
- Record the decision in the feature record as `validation_result` + `validated_at`, and `validation_issues` on FAIL.

PASS → handoff to Planner (TASKS):

```json
{
  "state": "TASKS",
  "validation_result": "PASS",
  "notes": "Spec complete and deterministic"
}
```

FAIL → return to Specifier (SPEC):

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
- Mark done.

**STOP if**

- Any doubt exists → FAIL. Do not patch the spec.

---

### Planner (TASKS)

**Must read**

- Validated spec
- Feature record for ids and paths

**Must produce**

- Tasks doc: `docs/sdd/artifacts/tasks/<feature_id>.md`

**Must NOT**

- Redesign or change behavior.
- Modify spec.

**STOP if**

- The spec is ambiguous or incomplete for execution.

---

### Implementer (IMPLEMENT)

**Must read**

- Tasks doc
- Validated spec for acceptance and SDT

**Must produce**

- Minimal product code + tests that satisfy the spec.

**Must NOT**

- Modify spec/design.
- Expand scope beyond tasks/spec.
- Write generated SDD artifacts unrelated to implementation evidence.

**STOP if**

- A task requires guessing behavior not defined by the spec.

---

### Verifier (VERIFY)

**Must read**

- Validated spec
- Tasks doc
- Code + tests

**Must produce**

- A single decision object: PASS or FAIL.

PASS → handoff to Audit (AUDIT):

```json
{
  "state": "AUDIT",
  "verification_result": "PASS",
  "notes": "Implementation matches spec and SDT scenarios."
}
```

FAIL → return to Implementer (IMPLEMENT):

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

- Fix code.
- Rewrite tasks/spec.

---

### Auditor (AUDIT)

**Must read**

- Spec + code + tests
- Verification output if present

**Must produce**

- Audit report: `docs/sdd/artifacts/audit_reports/<report>.md`
- Gate result: PASS, WARN, or FAIL

**Must NOT**

- Modify code/spec.
- Perform implementation work.

**Gate rule**

- PASS/WARN → archive may proceed if no other blockers remain.
- FAIL → corrective work may continue, but archive/final acceptance/release gates are blocked until PASS/WARN or explicit owner waiver.

---

### Archiver (ARCHIVE)

**Must read**

- Audit report
- Feature record + artifacts
- Any owner waiver if audit is FAIL

**Must produce**

- A closed/archived feature record (`state: ARCHIVE`) plus required trace updates.

**Must NOT**

- Rewrite specs retroactively without reopening states.
- Archive unresolved audit failures without an explicit owner waiver.
