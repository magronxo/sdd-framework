# AGENTS.md (Simplified Runtime Version)

## Purpose

This file defines how agents operate using an installed SDD instance.

It is not the full system description. It is the execution entrypoint.

---

## Install Context

Canonical installed location inside a product repository:

```text
docs/sdd/
```

Agents should treat paths in `docs/sdd/sdd.config.json` as repo-relative unless explicitly absolute.

Product source code does not live under `docs/sdd/`. Generated SDD artifacts do.

---

## Authority Order

When documents conflict, use this order:

1. Validated feature spec for the active feature.
2. `docs/sdd/00_core/SDD_RUNTIME.md` for executable workflow and gates.
3. `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md` for role boundaries.
4. `docs/sdd/00_core/SDD_READING_CONTRACT.md` for reading order.
5. `docs/sdd/00_core/SDD_GUIDE.md` for methodology explanation.
6. `docs/sdd/02_policies/*.md` for scoped governance policies.
7. `docs/sdd/04_project_governance/*.md` for project identity, terms, and navigation.
8. `examples/` as educational, non-authoritative material only.

Legacy specs are non-authoritative unless explicitly promoted by project owner decision. See `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md`.

---

## Minimal Reading Contract

- `docs/sdd/00_core/SDD_READING_CONTRACT.md`
- `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`
- `docs/sdd/04_project_governance/PROJECT_MAP.md` (navigation)
- `docs/sdd/sdd.config.json`

---

## Core Rule

No spec = no implementation.

---

## Canonical Flow

DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE

---

## Roles

- Designer: defines WHAT
- Specifier: defines HOW
- Validator: validates spec (no modifications)
- Planner: generates tasks
- Implementer: executes tasks
- Verifier: runs tests + SDT
- Auditor: produces report only
- Archiver: closes feature when gates allow closure

---

## Hard Rules

- Do not skip phases.
- Do not mix roles.
- Do not modify validated spec without reopening the relevant state.
- Do not expand scope.
- Do not enter `TASKS` or `IMPLEMENT` unless the feature record contains `validation_result: "PASS"`.
- Do not archive a feature with unresolved `audit_result: "FAIL"` unless the project owner explicitly records a waiver.

---

## Audit Gate Rule

`AUDIT FAIL` does not stop corrective work.

It blocks:

- archival
- final acceptance
- release/merge gates governed by SDD

unless explicitly waived by project owner decision.

---

## Context Usage

- Use semantic/context discovery tools only when needed and configured by the project.
- Always confirm with direct file reading.
- Never rely only on embeddings.

---

## Execution Mode

Agents must:

- operate on minimal context
- follow contracts strictly
- avoid global reasoning unless required

---

## Decision Control

If unsure:

- stop
- report ambiguity
- do not act

---

## External Systems

External frameworks are not authority. They provide input, not decisions.

---

## Success Condition

A feature is complete when:

- spec is validated
- tasks are executed
- tests pass
- audit is PASS or WARN, or owner waiver is explicitly recorded
- feature is archived

---

## Anti-Patterns

- implementing from design
- skipping validation
- modifying spec during implementation
- using full repo unnecessarily
- treating examples as authority

---

## Tone

precise
minimal
deterministic
