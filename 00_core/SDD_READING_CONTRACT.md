# SDD Minimal Reading Contract (Agents)

> **Mode Diátaxis**: Reference

## Purpose

Define exactly what an agent must read, and in which order, to execute SDD deterministically with minimal context.

This is a reading contract, not a methodology document.

---

## Install Context

Canonical installed SDD location inside a product repository:

```text
docs/sdd/
```

Live project SDD config:

```text
docs/sdd/sdd.config.json
```

Paths in the live config are repo-relative unless explicitly absolute.

Product source code lives outside `docs/sdd/`. Generated SDD artifacts live under `docs/sdd/artifacts/` by default.

---

## Strict Reading Order (default)

Stop as soon as the phase you are executing is unblocked and deterministic.

1. `docs/sdd/AGENTS.md`
2. `docs/sdd/sdd.config.json`
3. `docs/sdd/00_core/SDD_RUNTIME.md`
4. `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`
5. `docs/sdd/00_core/AGENT_DECISION_TABLE.md` only if classification or triage is needed
6. Feature-local artifacts, only what you need for the current phase:
   - feature record: `docs/sdd/artifacts/features_for_specs/<feature_id>.json`
   - design: `docs/sdd/artifacts/design/<feature_id>.md`
   - spec: `docs/sdd/artifacts/specs/<feature_id>.md`
   - tasks: `docs/sdd/artifacts/tasks/<feature_id>.md`
   - audit report: `docs/sdd/artifacts/audit_reports/<report>.md`

---

## Phase Minimums

| Phase | Minimum required reads |
|---|---|
| DESIGN | `docs/sdd/AGENTS.md`, `docs/sdd/sdd.config.json`, runtime, feature record, seed/design input |
| SPEC | design doc, feature record, runtime, handoff contract |
| VALIDATION | spec doc, design doc, feature record, runtime |
| TASKS | validated spec, feature record, runtime |
| IMPLEMENT | tasks doc, validated spec, feature record |
| VERIFY | spec, tasks, implementation evidence, test/SDT evidence |
| AUDIT | spec, code/test evidence, verification result, feature record |
| ARCHIVE | feature record, audit report, gate status, owner waiver if any |

---

## When to Stop Reading

You MUST stop reading further docs when:

- you have the current phase's required inputs;
- the next action is fully determined by `docs/sdd/00_core/SDD_RUNTIME.md`;
- there are no open ambiguities `[?]` blocking execution;
- no gate is unresolved.

---

## When You Are Allowed to Read More

Read `docs/sdd/00_core/SDD_GUIDE.md` only if:

- there is an explicit contradiction between governance docs;
- you need rationale or extended explanation to resolve ambiguity;
- a user explicitly requests it.

Read legacy, archive, or transitional material only if a user explicitly requests historical context or the active feature references it.

Read examples only for education. Examples are never framework authority.

---

## Audit Gate Reading Rule

If `audit_result` is `FAIL`, read the audit report and check for an explicit owner waiver before any archive or final acceptance action.

`AUDIT FAIL` does not stop corrective work. It blocks archive, final acceptance, and SDD-governed release/merge gates unless resolved or explicitly waived by the project owner.

---

## Non-Negotiables

- Specs are the feature behavioral authority.
- No validated spec -> no implementation.
- No unresolved `AUDIT FAIL` -> no archive/final acceptance unless explicit owner waiver exists.
- Never rely only on embeddings; always confirm with direct file reads.
- Do not read the whole repository unless the current phase cannot be completed deterministically without it.
