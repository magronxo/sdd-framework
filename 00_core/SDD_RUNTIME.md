# SDD Runtime Contract

> **Mode Diátaxis**: Reference

## Purpose

Define the minimal executable Spec-Driven Development flow for an installed SDD instance.

This is a human-readable runtime guide. The machine-readable v1 authority is split between `contract/v1/feature-record.schema.json` for record shape and `contract/v1/sdd-protocol.json` for lifecycle, transitions, gates, blockers, and compatibility behavior.

---

## Install Context

Canonical installed location inside a product repository:

```text
docs/sdd/
```

Live project configuration:

```text
docs/sdd/sdd.config.json
```

Paths in that config are repo-relative unless explicitly absolute.

Product code stays outside `docs/sdd/`. Generated SDD artifacts live under `docs/sdd/artifacts/` by default.

---

## Core Principle

- Specs are the feature source of truth.
- No implementation without validated spec.
- No spec without validated design.
- No silent contract changes.

---

## Canonical Pipeline

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

`SEED` and `INTAKE` are pre-record activities, not persistent states.

---

## States

| State | Description |
|------|------------|
| DESIGN | Feature defined conceptually |
| SPEC | Contract defined |
| VALIDATION | Spec verification |
| TASKS | Work breakdown |
| IMPLEMENT | Code execution |
| VERIFY | Tests + SDT validation |
| AUDIT | Audit report and gate result |
| ARCHIVE | Feature completed |

Legacy note:

- Existing feature records may use `DONE` or `ARCHIVED` as terminal states.
- Treat both as explicit read aliases of `ARCHIVE`; do not use them for new work.

---

## Roles

| Role | Responsibility | Default output |
|---|---|---|
| Designer | Defines WHAT | `docs/sdd/artifacts/design/<feature>.md` |
| Specifier | Defines HOW | `docs/sdd/artifacts/specs/<feature>.md` |
| Validator | Validates spec only | PASS / FAIL decision |
| Planner | Generates tasks from validated spec | `docs/sdd/artifacts/tasks/<feature>.md` |
| Implementer | Executes gated tasks | product code + tests |
| Verifier | Runs tests + SDT scenarios | PASS / FAIL decision |
| Auditor | Produces report and gate result | `docs/sdd/artifacts/audit_reports/<report>.md` |
| Archiver | Closes feature when gates allow closure | archived feature record |

---

## Hard Rules

- DO NOT implement without validated spec (`validation_result: PASS`).
- VALIDATION must be explicitly recorded in the feature record (`validation_result` + `validated_at`).
- `TASKS -> IMPLEMENT` must satisfy its semantic prerequisites.
- Human approval for `TASKS -> IMPLEMENT` applies only when an active project, risk, or external governance profile requires the `TASKS_TO_IMPLEMENT` checkpoint.
- DO NOT modify spec after validation without reopening state.
- DO NOT mix roles.
- DO NOT skip states.
- DO NOT generate tasks before validation.
- DO NOT archive if `audit_result: FAIL` is unresolved, unless an owner waiver is explicitly recorded.
- Legacy specs are non-authoritative unless explicitly promoted; see `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md`.

### Conditional checkpoint behavior

The core protocol does not resolve project or risk profiles. It accepts the resolved policy requirement as gate input:

- checkpoint not required + semantic prerequisites valid -> `ALLOW`;
- checkpoint required + approval absent -> `HUMAN_REQUIRED`;
- checkpoint required + approval recorded -> `ALLOW`.

No Baranes Tècniques or wrapper integration is implemented in this phase.

---

## Failure Handling

- VALIDATION FAIL -> back to SPEC.
- VERIFY FAIL -> back to IMPLEMENT.
- AUDIT FAIL -> corrective work may continue, but archive, final acceptance, and SDD-governed release/merge gates are blocked until PASS/WARN or explicit owner waiver.
- AUDIT FAIL does not select an automatic repair phase.

---

## Inputs / Outputs

| Phase | Input | Output |
|------|------|--------|
| DESIGN | feature record | `docs/sdd/artifacts/design/<feature>.md` |
| SPEC | design doc | `docs/sdd/artifacts/specs/<feature>.md` |
| VALIDATION | spec doc | PASS / FAIL |
| TASKS | validated spec | `docs/sdd/artifacts/tasks/<feature>.md` |
| IMPLEMENT | tasks doc satisfying active gate policy | product code + tests |
| VERIFY | code + tests | PASS / FAIL |
| AUDIT | spec + code + verification evidence | audit report + PASS/WARN/FAIL |
| ARCHIVE | report + gates | closed feature |

---

## Canonical Artifact Roots

Default generated SDD artifacts live under:

- `docs/sdd/artifacts/features_for_specs/`
- `docs/sdd/artifacts/design/`
- `docs/sdd/artifacts/specs/`
- `docs/sdd/artifacts/tasks/`
- `docs/sdd/artifacts/audit_reports/`
- `docs/sdd/artifacts/adr/`

Other folders under `docs/sdd/` govern and operate the flow, but they are not product source code.

---

## Path Format (Feature Records)

Canonical path format inside `docs/sdd/artifacts/features_for_specs/*.json` is repository-relative:

- `design_path`: `docs/sdd/artifacts/design/<feature>.md`
- `spec_path`: `docs/sdd/artifacts/specs/<feature>.md`
- `task_path`: `docs/sdd/artifacts/tasks/<feature>.md`

The only initial legacy path compatibility is `artifacts/...`, interpreted relative to `sdd_root` with an explicit warning. It must not be silently normalized.

---

## Scope Control

- Every phase operates on minimal context.
- No full-repo loading unless explicitly required.
- Prefer contract over exploration.

---

## Execution Mode

Agents must operate:

- deterministically
- contract-first
- minimal scope
- with explicit state transitions

---

## Success Condition

A feature is complete when:

- spec is validated
- all tasks are implemented
- SDT scenarios pass
- audit report is generated
- audit is PASS or WARN, or owner waiver is explicitly recorded
- feature is archived without blocking open questions

---

## Project Configuration

Agents must consult:

```text
docs/sdd/sdd.config.json
```

If this file is missing, agents must STOP and report the missing configuration.
