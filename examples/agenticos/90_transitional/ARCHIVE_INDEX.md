# 90_transitional — Archive index
**STATUS:** ACTIVE (index)
**AUTHORITY:** NON-CANONICAL

This folder contains transitional and legacy docs kept for traceability.

Archived docs are moved under `archive/` and replaced by stub redirect files at the original path to avoid breaking links.

## Archived (moved)

| Original path | New path | Reason | Canonical successor(s) |
|---|---|---|---|
| `SDD_PROMPT.md` | `archive/SDD_PROMPT.md` | Legacy orchestrator prompt (explicitly non-canonical). | `../00_core/SDD_RUNTIME.md`, `../01_execution/prompts/*` |
| `feat-021_IMPLEMENTER_RUNBOOK.md` | `archive/feat-021_IMPLEMENTER_RUNBOOK.md` | Per-feature sample runbook; replaced by canonical role prompt + tasks. | `../01_execution/prompts/implementer.md`, `../artifacts/tasks/feat-021-session-ticket-linkage.md` |
| `PROVISIONAL_IMPLEMENTATION_READINESS_WORKFLOW.md` | `archive/PROVISIONAL_IMPLEMENTATION_READINESS_WORKFLOW.md` | Provisional pre-flow; superseded by PRE-SDD runtime + prompts. | `../03_operations/pre_sdd/PRE_SDD_RUNTIME.md` |
| `FEATURES_NORMALIZATION_PLAN.md` | `archive/FEATURES_NORMALIZATION_PLAN.md` | Transitional plan; outcomes applied to `features_for_specs/`. | `../00_core/SDD_FEATURE_FORMAT.md` |
| `FEATURE_RECORD_TYPES.md` | `archive/FEATURE_RECORD_TYPES.md` | Transitional model note; outcomes applied to feature records. | `../00_core/SDD_FEATURE_FORMAT.md` |
| `SPEC_REAUDIT_PRIORITY_PLAN.md` | `archive/SPEC_REAUDIT_PRIORITY_PLAN.md` | Transitional plan; contains outdated status/paths. | `../03_operations/SPEC_REAUDIT_WORKFLOW.md`, `../03_operations/ROADMAP.md` |

## Still active (transitional)

| Path | Notes |
|---|---|
| `CONTEXT_ENGINE_ENVIRONMENT_DIAGNOSIS.md` | Environment incident note; not pipeline authority. |
| `EXTERNAL_KERNEL_DEVELOPMENT.md` | Transitional context for external kernel development layer. |
| `PROFESSIONALIZATION_GAPS_AND_NEXT_STEPS.md` | Transitional context; roadmap consolidated in `../03_operations/ROADMAP.md`. |

