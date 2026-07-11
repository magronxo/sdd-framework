# SDD Runtime Contract

> **Mode Diátaxis**: Reference

## Purpose

Define the minimal executable Spec-Driven Development flow for an installed SDD instance.

The machine-readable v1 authority is split between `contract/v1/feature-record.schema.json` for record shape and `contract/v1/sdd-protocol.json` for lifecycle, transitions, gates, blockers, and compatibility.

## Install context

Canonical installed location:

```text
docs/sdd/
```

Generated artifacts live under `docs/sdd/artifacts/`.

## Canonical pipeline

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

`SEED` and `INTAKE` are pre-record activities.

## Hard rules

- No implementation without effective validation `PASS`.
- Validation must be explicitly recorded.
- Blocking open questions deny progression.
- `TASKS -> IMPLEMENT` validates core semantic prerequisites.
- Human approval for `TASKS -> IMPLEMENT` is conditional on an active project, risk, or external governance policy.
- No role mixing or skipped states.
- Do not archive unresolved `AUDIT FAIL` without a valid owner waiver.
- No silent legacy normalization.

This phase does not integrate with Baranes Tècniques or wrappers.

## Result compatibility

### Validation

Canonical:

```text
PASS
FAIL
```

Historical `PASS_WITH_FOLLOWUP` is accepted only in tolerant reads:

- effective result `PASS`;
- warning `LEGACY_PASS_WITH_FOLLOWUP`;
- open blocking questions still deny `VALIDATION -> TASKS`;
- canonical writes reject it.

### Verification

Canonical:

```text
PASS
FAIL
```

`verification_result: PASS_WITH_FOLLOWUP` is invalid.

Active `PARTIAL` is invalid and produces `VERIFICATION_NOT_EXECUTED`.

Archived `PARTIAL` under `ARCHIVE`, `DONE`, or `ARCHIVED`:

- is a tolerant historical read;
- emits `LEGACY_PARTIAL_AMBIGUOUS`;
- has effective verification `null`;
- sets `migration_review_required: true`;
- must not be modified, reopened, or migrated automatically.

## Failure handling

- `VALIDATION FAIL -> SPEC`
- `VERIFY FAIL -> IMPLEMENT`
- `AUDIT FAIL` blocks archive unless waived and does not choose a repair phase automatically.

## Artifact paths

Canonical:

- `docs/sdd/artifacts/design/<feature>.md`
- `docs/sdd/artifacts/specs/<feature>.md`
- `docs/sdd/artifacts/tasks/<feature>.md`

Legacy `artifacts/...` is read relative to `sdd_root` with a warning.

Any exact path segment equal to `..` is invalid, including the first segment after the canonical or legacy prefix.

## Completion

A feature is complete when validation, implementation, verification, audit, and archival gates all permit completion and no blocking open question remains.
