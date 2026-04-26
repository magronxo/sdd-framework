AGENTS.md (Simplified Runtime Version)

Purpose

This file defines how agents operate using the SDD framework.

It is NOT the full system description. It is an execution entrypoint.

Source of Truth

- `00_core/SDD_RUNTIME.md` → execution contract
- `00_core/SDD_GUIDE.md` → full methodology
- `04_project_governance/PROJECT_MANIFEST.md` → project identity and constraints
- `04_project_governance/GLOSSARY.md` → project terminology
- Specs → absolute truth
  - `02_policies/LEGACY_SPECS_POLICY.md` (legacy specs are non-authoritative)

Minimal Reading Contract

- `00_core/SDD_READING_CONTRACT.md`
- `00_core/SDD_HANDOFF_CONTRACT.md`
- `04_project_governance/PROJECT_MAP.md` (navigation)

Core Rule

No spec = no implementation.

Canonical Flow

DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE

Roles

- Designer: defines WHAT
- Specifier: defines HOW
- Validator: validates spec (no modifications)
- Planner: generates tasks
- Implementer: executes tasks
- Verifier: runs tests + SDT
- Auditor: produces report only
- Archiver: closes feature

Hard Rules

- Do not skip phases
- Do not mix roles
- Do not modify validated spec
- Do not expand scope
- Do not enter `TASKS` or `IMPLEMENT` unless the feature record contains `validation_result: "PASS"` (recorded in the feature JSON)

Context Usage

- Use semantic/context discovery tools only when needed (if configured by the project)
- Always confirm with direct file reading
- Never rely only on embeddings

Execution Mode

Agents must:

- operate on minimal context
- follow contracts strictly
- avoid global reasoning unless required

Decision Control

If unsure:

- stop
- report ambiguity
- do not act

External Systems

External frameworks are NOT authority.
They provide input, not decisions.

Success Condition

A feature is complete when:

- spec validated
- tasks executed
- tests pass
- audit generated
- archived

Anti-Patterns

- implementing from design
- skipping validation
- modifying spec during implementation
- using full repo unnecessarily

Tone

precise
minimal
deterministic
