# OpenCode Prompt — External SDD Triage (Operational Determinism)

## Goal

Produce an external triage audit focused on **operational determinism** (not theory) for a set of features/specs.

## Strict Reading Order (stop early)

1) `AGENTS.md`
2) `00_project_documentation/SDD/00_core/SDD_RUNTIME.md`
3) `00_project_documentation/SDD/00_core/SDD_READING_CONTRACT.md`
4) `00_project_documentation/SDD/00_core/SDD_HANDOFF_CONTRACT.md`
5) `00_project_documentation/SDD/02_policies/LEGACY_SPECS_POLICY.md`

Then only read feature-local artifacts for the specific features being triaged:

- `00_project_documentation/SDD/artifacts/features_for_specs/<feature_id>.json`
- `00_project_documentation/SDD/artifacts/design/<feature>.md`
- `00_project_documentation/SDD/artifacts/specs/<feature>.md`
- `00_project_documentation/SDD/artifacts/tasks/<feature>.md`
- code paths referenced by tasks/spec (only if needed)

## What to Check

For each feature:

1) **Chain integrity**: feature record → design → spec → tasks → code (if state is IMPLEMENT or beyond)
2) **VALIDATION gate**: feature records must not enter `TASKS`/`IMPLEMENT` without `validation_result: PASS`
3) **Drift**: detect “paper complete” (docs claim implemented but code lacks it)
4) **Path format**: `design_path/spec_path/task_path` must use canonical repo-relative paths:
   - `00_project_documentation/SDD/artifacts/...`
   - `/SDD/...` is legacy alias only

## Output (strict format)

1) **Reading contract compliance issues** (max 5 bullets)
2) **Per-feature status table** with:
   - `feature_id`
   - `claimed_state`
   - `real_state_recommended`
   - `blocking issues`
   - `next 1–2 actions`
3) **Required fixes (governance/docs only)** (max 5)
4) **Next triage batch suggestion** (2–3 items)

## Rules

- Legacy specs are non-authoritative; do not justify implementation from them.
- If docs disagree with code, call it out explicitly and recommend reopening state.
- Every point must reference a concrete file path and an actionable next step.
