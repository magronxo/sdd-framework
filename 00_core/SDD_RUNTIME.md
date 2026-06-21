# SDD Runtime Contract

> **Mode Diátaxis**: Reference

## Purpose

Define the minimal executable Spec-Driven Development flow for an installed SDD instance.

This document is the operational source of truth for agents. It does not replace `SDD_GUIDE`; it reduces it to an executable contract.

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

DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE

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

- Some existing feature records may still use `DONE` as a terminal state.
- Treat `DONE` as legacy alias of `ARCHIVE`; do not use it for new work.

---

## Roles

| Role | Responsibility | Default output |
|---|---|---|
| Designer | Defines WHAT | `docs/sdd/artifacts/design/<feature>.md` |
| Specifier | Defines HOW | `docs/sdd/artifacts/specs/<feature>.md` |
| Validator | Validates spec only | PASS / FAIL decision |
| Planner | Generates tasks from validated spec | `docs/sdd/artifacts/tasks/<feature>.md` |
| Implementer | Executes tasks | product code + tests |
| Verifier | Runs tests + SDT scenarios | PASS / FAIL decision |
| Auditor | Produces report and gate result | `docs/sdd/artifacts/audit_reports/<report>.md` |
| Archiver | Closes feature when gates allow closure | archived feature record |

---

## Hard Rules

- DO NOT implement without validated spec (`validation_result: PASS`).
- VALIDATION must be explicitly recorded in the feature record (`validation_result` + `validated_at`).
- DO NOT modify spec after validation without reopening state.
- DO NOT mix roles.
- DO NOT skip states.
- DO NOT generate tasks before validation.
- DO NOT archive if `audit_result: FAIL` is unresolved, unless an owner waiver is explicitly recorded.
- Legacy specs are non-authoritative unless explicitly promoted; see `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md`.

---

## Failure Handling

- VALIDATION FAIL -> back to SPEC.
- VERIFY FAIL -> back to IMPLEMENT.
- AUDIT FAIL -> corrective work may continue, but archive, final acceptance, and SDD-governed release/merge gates are blocked until PASS/WARN or explicit owner waiver.

---

## Inputs / Outputs

| Phase | Input | Output |
|------|------|--------|
| DESIGN | feature record | `docs/sdd/artifacts/design/<feature>.md` |
| SPEC | design doc | `docs/sdd/artifacts/specs/<feature>.md` |
| VALIDATION | spec doc | PASS / FAIL |
| TASKS | validated spec | `docs/sdd/artifacts/tasks/<feature>.md` |
| IMPLEMENT | tasks doc | product code + tests |
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

Canonical path format inside `docs/sdd/artifacts/features_for_specs/*.json` is repo-relative:

- `design_path`: `docs/sdd/artifacts/design/<feature>.md`
- `spec_path`: `docs/sdd/artifacts/specs/<feature>.md`
- `task_path`: `docs/sdd/artifacts/tasks/<feature>.md`

Legacy aliases are allowed only for traceability during migration: `/SDD/artifacts/...`, `artifacts/...`, or other historical prefixes.

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
- feature is archived without open contract issues

---

## Project Configuration

Agents must consult:

```text
docs/sdd/sdd.config.json
```

If this file is missing, agents must STOP and report the missing configuration.
