# SDD Feature Format

> Human-readable overview. The machine-readable authority for feature-record fields and internal invariants is `contract/v1/feature-record.schema.json`. Workflow transitions and gates are authoritative only in `contract/v1/sdd-protocol.json`.

Every persisted feature is represented by one JSON record of type `SYSTEM_SPEC`.

## Lifecycle

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

`SEED` and `INTAKE` happen before record creation. `BLOCKED`, `VALIDATED`, and `VERIFIED` are derived conditions.

## Primary artifact paths

Each artifact-producing phase uses one singular field:

- `design_path`
- `spec_path`
- `task_path`
- `audit_report_path`

Canonical paths are repository-relative:

```text
docs/sdd/artifacts/...
```

`artifacts/...` is a tolerant legacy read and emits a warning. Any exact `..` segment is invalid.

## Results

Canonical values:

- validation: `PASS`, `FAIL`
- verification: `PASS`, `FAIL`
- audit: `PASS`, `WARN`, `FAIL`

Historical validation `PASS_WITH_FOLLOWUP` is a tolerant read with effective result `PASS`. Progression remains blocked when an open question is blocking. It is not valid under `verification_result`.

Active verification `PARTIAL` is invalid. Archived `PARTIAL` is tolerated only for read compatibility, emits `LEGACY_PARTIAL_AMBIGUOUS`, has no effective verification result, and requires migration review without modifying the record.

## Open questions

```json
{
  "id": "Q-001",
  "text": "Pregunta pendent",
  "blocking": true,
  "owner": "role-or-person",
  "status": "OPEN"
}
```

## Compatibility

Explicit tolerant reads:

- `feature_id` as alias of `id`
- `DONE` or `ARCHIVED` as aliases of `ARCHIVE`
- `tasks_path` as alias of `task_path`
- `artifacts/...`
- validation `PASS_WITH_FOLLOWUP`
- archived verification `PARTIAL`

Canonical writes reject all legacy forms. The validator never rewrites inspected records.

## Validation

See `contract/v1/README.md`.
