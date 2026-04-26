# SDD Minimal Reading Contract (Agents)

## Purpose

Define exactly what an agent must read (and in which order) to execute SDD deterministically with minimal context.

This is a *reading contract*, not a methodology document.

---

## Strict Reading Order (default)

Stop as soon as the phase you are executing is unblocked and deterministic.

1) `AGENTS.md`
2) `00_project_documentation/SDD/00_core/SDD_RUNTIME.md`
3) `00_project_documentation/SDD/00_core/AGENT_DECISION_TABLE.md` (only if classification/triage is needed)
4) Feature-local artifacts (only what you need for the current phase):
   - feature record: `00_project_documentation/SDD/artifacts/features_for_specs/<feature_id>.json`
   - design: `00_project_documentation/SDD/artifacts/design/<feature_id>.md`
   - spec: `00_project_documentation/SDD/artifacts/specs/<feature_id>.md`
   - tasks: `00_project_documentation/SDD/artifacts/tasks/<feature_id>.md`

---

## When to Stop Reading

You MUST stop reading further docs when:

- you have the current phase’s required input(s), and
- the next action is fully determined by `SDD_RUNTIME`, and
- there are no open ambiguities `[?]` blocking execution.

---

## When You Are Allowed to Read More

Read `00_project_documentation/SDD/00_core/SDD_GUIDE.md` only if:

- there is an explicit contradiction between governance docs, or
- you need a rationale / extended explanation to resolve ambiguity, or
- a user explicitly requests it.

Read `00_project_documentation/SDD/90_transitional/*` only if a user explicitly requests historical context.

---

## Non-Negotiables

- Specs are the only behavioral authority.
- No spec (validated) → no implementation.
- Never rely only on embeddings; always confirm with direct file reads.
