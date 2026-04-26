# Seed handoff — SEED-XX → SDD DESIGN

source_seed_id: SEED-XX  
triage_batch_path: `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_YYYY-MM-DD.md`

## Create feature record (DESIGN)

- `00_project_documentation/SDD/artifacts/features_for_specs/feat-XXX-<slug>.json`

Required fields:

- `id`, `type: SYSTEM_SPEC`, `state: DESIGN`, `title`, `created_at`, `updated_at`
- `design_path` (canonical path; file must exist)

Recommended metadata:

```json
{
  "pre_sdd": {
    "source_seed_id": "SEED-XX",
    "triage_batch_path": "00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_YYYY-MM-DD.md",
    "decomposition_status": "DECOMPOSED"
  }
}
```

## Create design artifact

- `00_project_documentation/SDD/artifacts/design/feat-XXX-<slug>.md`

Design must include:

- problem
- goals / non-goals
- intended contract boundaries (no spec-level detail yet)
- dependencies/ordering (if part of a decomposition)

