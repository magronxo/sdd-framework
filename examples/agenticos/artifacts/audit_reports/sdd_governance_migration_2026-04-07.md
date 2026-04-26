# SDD Governance Migration (runtime-first) — 2026-04-07

**Type:** governance patch (docs only)  
**Goal:** make the SDD flow deterministic and executable for agents by removing authority/path ambiguity.  
**Non-goals:** no Kernel/runtime code changes.

---

## Final Source of Truth (after migration)

**Execution contract (agents):**
- `00_project_documentation/SDD/00_core/SDD_RUNTIME.md`

**Full methodology reference:**
- `00_project_documentation/SDD/00_core/SDD_GUIDE.md`

**Operational overlay (intake -> discovery -> gap -> decision -> execution -> validation -> consolidation):**
- `00_project_documentation/SDD/03_operations/WORKFLOW.md`

**Ticket runtime contract (minimum, executable):**
- `00_project_documentation/05_ADR_DECISION_LOG.md` (ADR 024, ADR 025)
- `00_project_documentation/SDD/artifacts/specs/feat-019-ticket-runtime-contract.md`
- Runtime: `02_implementation/internal/kernel/router.go`

---

## Canonical Artifact Roots (repo reality)

Canonical working artifacts are under:

- `00_project_documentation/SDD/artifacts/features_for_specs/`
- `00_project_documentation/SDD/artifacts/design/`
- `00_project_documentation/SDD/artifacts/specs/`
- `00_project_documentation/SDD/artifacts/tasks/`

---

## Mapping of key changes

### Contract + navigation

- Updated SDD runtime contract to point to `SDD/artifacts/*` (no more implicit `design/`, `specs/`, `tasks/`).
- Updated SDD README pipeline to include `TASKS` and to point to `00_core/SDD_RUNTIME.md`.

### Execution prompts and skills

- Updated `01_execution/prompts/*` to create artifacts under `SDD/artifacts/*`.
- Updated `01_execution/skills/sdd-audit.md` references to use `SDD/artifacts/specs/*` and `SDD/artifacts/tasks/*`.

### Feature records + live artifacts

- Normalized `artifacts/features_for_specs/*.json` paths from `/SDD/{design|specs|tasks}/...` to `/SDD/artifacts/{design|specs|tasks}/...`.
- Updated live spec/task headers that referenced `/SDD/design` or `/SDD/specs` to `/SDD/artifacts/design` and `/SDD/artifacts/specs`.
- Re-encoded `artifacts/features_for_specs/feat-020.json` to valid UTF-8 while applying the same path normalization.

### Transitional authority

- Added a consistent header to all docs under `SDD/90_transitional/`:
  - `STATUS: TRANSITIONAL`
  - `AUTHORITY: NON-CANONICAL`
- Marked `SDD/90_transitional/SDD_PROMPT.md` as legacy:
  - `STATUS: LEGACY`
  - `DO NOT USE AS PIPELINE SOURCE`

### Ticket transitions (explicitly NOT SDD)

- Added derived note: `01_design/TICKET_RUNTIME_TRANSITIONS_MINIMUM.md`
- Converted `00_project_documentation/SDD/TICKET_TRANSITIONS.md` into a redirect stub pointing to the derived note and ADR/spec/runtime authority.
- Updated `01_design/02_TICKET_SYSTEM.md` to explicitly declare the runtime-minimum authority and to avoid implying it is the runtime contract.

---

## Verification checklist

- No canonical doc/prompt points to `SDD/design/`, `SDD/specs/`, `SDD/tasks/` as active artifact roots.
- Transitional docs are clearly marked non-canonical, and `SDD_PROMPT.md` is clearly marked legacy.
- Ticket transitions are no longer presented as SDD source of truth.

