# SDD Feature Format

> Human-readable overview. The machine-readable authority for feature-record fields and internal invariants is `contract/v1/feature-record.schema.json`. Workflow transitions and gates are authoritative only in `contract/v1/sdd-protocol.json`.

Every persisted feature is represented by one JSON record of type `SYSTEM_SPEC`. The record is the traceability source for that feature; the v1 schema defines its valid shape.

## Canonical location

Installed SDD instances live under `docs/sdd/` and feature records live under:

```text
docs/sdd/artifacts/features_for_specs/
```

## Minimum canonical record

```json
{
  "id": "feat-001-example",
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",
  "title": "Brief description",
  "created_at": "2026-07-11T09:00:00Z",
  "updated_at": "2026-07-11T09:00:00Z",
  "open_questions": []
}
```

The persistent lifecycle is:

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

`SEED` and `INTAKE` happen before the feature record is created. Conditions such as `BLOCKED`, `VALIDATED`, and `VERIFIED` are derived and are not persistent states.

## Primary artifact paths

Each artifact-producing phase uses one singular path field:

- `design_path`
- `spec_path`
- `task_path`
- `audit_report_path`

Canonical paths are complete and repository-relative:

```text
docs/sdd/artifacts/...
```

Arrays such as `design_artifacts`, `spec_artifacts`, or `task_artifacts` are not part of the canonical record.

## Structured open questions

```json
{
  "id": "Q-001",
  "text": "Pregunta pendent",
  "blocking": true,
  "owner": "role-or-person",
  "status": "OPEN"
}
```

Blocking open questions are evaluated by workflow gates defined in the protocol, not by this document.

## Results

Canonical result values are:

- validation: `PASS`, `FAIL`
- verification: `PASS`, `FAIL`
- audit: `PASS`, `WARN`, `FAIL`

`PARTIAL` is not canonical verification evidence. `PASS_WITH_FOLLOWUP` is a tolerated historical read interpreted as `PASS` only when follow-up questions are non-blocking.

## Conditional human approval

The core transition `TASKS -> IMPLEMENT` validates the approved semantic prerequisites: validated spec, task artifact, and no blocking open questions.

Human approval is not universally required. A project profile, risk profile, or external governance layer may activate the `TASKS_TO_IMPLEMENT` checkpoint. When active and not recorded, the gate returns `HUMAN_REQUIRED`; otherwise a semantically valid transition returns `ALLOW`.

Profile resolution and external governance integrations are outside this phase.

## Explicit legacy reads

The v1 validator can read these historical forms with explicit warnings:

- `feature_id` as alias of `id`
- `DONE` or `ARCHIVED` as aliases of `ARCHIVE`
- `tasks_path` as alias of `task_path`
- `artifacts/...` interpreted relative to `sdd_root`

New writes must use canonical names and values. The validator never rewrites or silently normalizes an inspected record.

## Audit waiver

An `AUDIT FAIL` record can only transition to `ARCHIVE` when a valid owner waiver is present. The waiver shape is defined by the schema and the transition rule is defined by the protocol.

## Validation

See `contract/v1/README.md` for commands, exit codes, fixtures, and read-only guarantees.
