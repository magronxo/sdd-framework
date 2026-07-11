# SDD Handoff Contract

> **Mode Diátaxis**: Reference

## Authority

This document summarizes role boundaries. Record fields are defined only by `docs/sdd/contract/v1/feature-record.schema.json`; transitions and gates are defined only by `docs/sdd/contract/v1/sdd-protocol.json`.

## Handoff chain

`SEED` and `INTAKE` are pre-record activities. Persistent handoffs follow:

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

Each role produces only its current-phase artifact or decision.

## Designer

Produces `docs/sdd/artifacts/design/<feature>.md` and records `design_path`. It does not define spec details, tasks, tests, or product code.

## Specifier

Produces `docs/sdd/artifacts/specs/<feature>.md` and records `spec_path`. It does not generate tasks or implementation.

## Validator

Produces one validation decision and does not modify the design or spec.

PASS summary:

```json
{
  "state": "TASKS",
  "validation_result": "PASS",
  "validated_at": "2026-07-11T09:20:00Z",
  "validation_details": "Spec is complete and deterministic."
}
```

FAIL summary:

```json
{
  "state": "SPEC",
  "validation_result": "FAIL",
  "validated_at": "2026-07-11T09:20:00Z",
  "validation_issues": [
    "Missing error-code behavior.",
    "Timeout outcome is ambiguous."
  ],
  "validation_details": "Return to specification."
}
```

The protocol, not this example, determines whether the transition is allowed. Effective validation and blocking open questions are evaluated independently.

## Planner

Reads the validated spec and produces `docs/sdd/artifacts/tasks/<feature>.md`, recorded in `task_path`. It does not redesign behavior.

## Implementer

Executes the bounded tasks against the validated spec. Any human checkpoint is conditional on active external policy input declared to the protocol; there is no universal approval requirement in this handoff document.

## Verifier

Produces one of these operational outcomes without modifying code or spec.

PASS summary:

```json
{
  "state": "AUDIT",
  "verification_result": "PASS",
  "verified_at": "2026-07-11T09:40:00Z",
  "verification_details": "Tests and applicable SDT scenarios passed with evidence."
}
```

FAIL summary:

```json
{
  "state": "IMPLEMENT",
  "verification_result": "FAIL",
  "verified_at": "2026-07-11T09:40:00Z",
  "verification_details": "SDT edge case failed; return to implementation."
}
```

Not executed summary:

```json
{
  "state": "VERIFY",
  "verification_details": "NOT EXECUTED: required commands are unavailable in this environment."
}
```

Not-executed verification remains in `VERIFY`; no verification result is recorded.

## Auditor and archiver

The auditor records `audit_result` and may produce `docs/sdd/artifacts/audit_reports/<report>.md`. `PASS` or `WARN` can permit archival when other gates pass. `FAIL` blocks `AUDIT -> ARCHIVE` unless a valid `owner_waiver` satisfies the protocol.

The waiver is limited to that documentary archival transition. The archiver does not retroactively rewrite specs or perform external operations.
