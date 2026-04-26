# Scope Split — feat-013 backend vs dashboard

**Date (UTC)**: 2026-04-08

## Decision
Split `feat-013` into:
- `feat-013`: **backend-only** (store + REST API + backend tests) → eligible for closure
- `feat-022`: **dashboard UI** (SessionTreePanel + ReactFlow) → new feature, separate lifecycle

## Rationale
Backend is implementable/verifiable independently; dashboard work is higher-variance and would block ARCHIVE of the backend if kept in the same feature.

## Traceability
- Original full spec (historical): `00_project_documentation/SDD/artifacts/specs/feat-013-session-tree.md`
- New backend canonical spec/tasks:
  - `00_project_documentation/SDD/artifacts/specs/feat-013-session-tree-backend.md`
  - `00_project_documentation/SDD/artifacts/tasks/feat-013-session-tree-backend.md`
- New dashboard feature:
  - `00_project_documentation/SDD/artifacts/features_for_specs/feat-022-session-tree-dashboard.json`

