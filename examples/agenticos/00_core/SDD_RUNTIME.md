# SDD Runtime Contract

## Purpose

Define the minimal executable Spec-Driven Development flow.

This document is the **operational source of truth for agents**.
It does not replace SDD_GUIDE, it reduces it to an executable contract.

---

## Core Principle

- Specs are the only source of truth
- No implementation without validated spec
- No spec without validated design
- No silent contract changes

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
| AUDIT | External/internal audit |
| ARCHIVE | Feature completed |

Legacy note:
- Some existing feature records may still use `DONE` as a terminal state.
- Treat `DONE` as legacy-alias of `ARCHIVE` (do not use for new work).

---

## Roles

### Designer
- defines WHAT
- produces: `artifacts/design/<feature>.md`

### Specifier
- defines HOW
- produces: `artifacts/specs/<feature>.md`

### Validator
- validates spec only
- cannot modify spec
- cannot generate tasks

### Planner
- generates tasks from validated spec
- produces: `artifacts/tasks/<feature>.md`

### Implementer
- executes tasks
- follows TDD

### Verifier
- runs tests + SDT scenarios

### Auditor
- produces report
- cannot block execution
- cannot modify code/spec

---

## Hard Rules

- DO NOT implement without validated spec (VALIDATION = PASS)
- VALIDATION must be explicitly recorded in the feature record (`validation_result` + `validated_at`)
- DO NOT modify spec after validation without reopening state
- DO NOT mix roles
- DO NOT skip states
- DO NOT generate tasks before validation
- Legacy specs are non-authoritative (see `02_policies/LEGACY_SPECS_POLICY.md`)

---

## Inputs / Outputs

| Phase | Input | Output |
|------|------|--------|
| DESIGN | feature.json | artifacts/design/<feature>.md |
| SPEC | artifacts/design/<feature>.md | artifacts/specs/<feature>.md |
| VALIDATION | spec.md | PASS / FAIL |
| TASKS | artifacts/specs/<feature>.md (validated) | artifacts/tasks/<feature>.md |
| IMPLEMENT | artifacts/tasks/<feature>.md | code |
| VERIFY | code + tests | PASS / FAIL |
| AUDIT | spec + code | report |
| ARCHIVE | report | closed feature |

---

## Failure Handling

- VALIDATION FAIL → back to SPEC
- VERIFY FAIL → back to IMPLEMENT
- AUDIT FAIL → generate tickets, continue or rework

---

## Scope Control

- Every phase operates on minimal context
- No full-repo loading unless explicitly required
- Prefer contract over exploration

---

## Model Usage Guideline

- Strong model → design, validation, audit
- Medium model → spec, planning
- Weak model → implementation, refactor

---

## Anti-Patterns

- Implementing from design
- Generating tasks from incomplete spec
- Modifying spec during implementation
- Mixing audit with implementation
- Expanding scope implicitly

---

## Execution Mode

Agents must operate:

- deterministically
- contract-first
- minimal scope
- explicit state transitions

---

## Success Condition

A feature is complete when:

- spec is validated
- all tasks implemented
- SDT scenarios pass
- audit report generated
- archived without open contract issues

---

## Canonical Artifact Roots (Repo Reality)

Inside `00_project_documentation/SDD/`, the canonical working artifacts live under:

- `artifacts/features_for_specs/` (feature records / state)
- `artifacts/design/`
- `artifacts/specs/`
- `artifacts/tasks/`

Other folders (core / execution / policies / operations / transitional) govern and operate the flow, but they are not feature deliverables.

---

## Path Format (Feature Records)

Canonical path format inside `artifacts/features_for_specs/*.json` is repo-relative, full paths:

- `design_path`: `00_project_documentation/SDD/artifacts/design/<feature>.md`
- `spec_path`: `00_project_documentation/SDD/artifacts/specs/<feature>.md`
- `task_path`: `00_project_documentation/SDD/artifacts/tasks/<feature>.md`

Legacy alias (allowed only for traceability during migration):
- `/SDD/artifacts/...`

---

## Tools: Context Engine

El context-engine és un suport operatiu per **descobrir** i **validar evidència** (especialment docs/codi) quan cal, però **no és autoritat**: no confiïs només en embeddings; sempre confirma amb lectura directa dels fitxers.

Components canònics:

- Wrapper: `K:\AgenticOsGen\04_tools\context.ps1`
- Binari: `K:\AgenticOsGen\04_tools\context-engine\context-engine.exe`
- Store canònic: `K:\AgenticOsGen\04_tools\context-engine\data\store.json`

Exemples (wrapper):

- `K:\AgenticOsGen\04_tools\context.ps1 doctor`
- `K:\AgenticOsGen\04_tools\context.ps1 search "REPORT_ENVELOPE_POLICY" docs`
- `K:\AgenticOsGen\04_tools\context.ps1 search "feat-021" docs`
