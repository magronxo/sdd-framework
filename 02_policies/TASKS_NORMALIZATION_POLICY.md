# Tasks Normalization Policy

> **Status:** Active
> **Date:** 2026-04-04
> **Scope:** `docs/sdd/artifacts/tasks/`

---

## 1. Purpose

The `docs/sdd/artifacts/tasks/` directory can have a mix of conventions:

- short files by `id` (`feat-001.md`, `feat-006.md`)
- files with slug (`feat-013-session-tree.md`)
- legacy files (`dashboard-backend.md`)

This makes it difficult to:

- trace between `design`, `spec`, `task`
- automate
- read the flow externally

This document fixes the model to move towards.

---

## 2. Canonical Decision

### Preferred future convention

New task files must follow:

```text
feat-XXX-descriptive-name.md
```

Examples:

- `feat-001-kernel-core.md`
- `feat-006-dashboard-react.md`
- `feat-006-api-server.md`
- `feat-017-react-loop.md`

---

## 3. Currently Accepted State

Meanwhile, the system accepts three categories:

### A. New canonical

Format: `feat-XXX-descriptive-name.md`

- ✅ Preferred for all new work
- ✅ Automatable
- ✅ Directly traceable from the feature record

### B. Old canonical (id only)

Format: `feat-XXX.md`

- ⚠️ Accepted for existing specs
- ⚠️ Recommended to rename when re-audited

### C. Legacy / not normalized

Format: any other (`dashboard-backend.md`, `old-spec-v1.md`, etc.)

- ❌ NOT accepted for new work
- ✅ May remain as historical reference in `90_transitional/`

---

## 4. Migration

### When to normalize?

- During TASKS, before the canonical `TASKS -> IMPLEMENT` handoff.
- During a documentary re-audit that does not mutate a historical feature record.
- When creating a new canonical task document that references historical material.

Canonical v1 has no general reopening transition. Do not rename an active historical task artifact by inventing a state change.

### How to normalize current TASKS work

1. Create the task file under `docs/sdd/artifacts/tasks/` with the canonical name.
2. Copy only relevant planned content.
3. Record the canonical repository-relative path in `task_path` before `TASKS -> IMPLEMENT`.
4. Preserve historical files for traceability; do not silently rewrite an archived record.

---

## 5. Relationship with Other Artifacts

| Artifact | Convention | Example |
|----------|------------|---------|
| Design | `feat-XXX-name.md` | `feat-013-session-tree.md` |
| Spec | `feat-XXX-name.md` | `feat-013-session-tree.md` |
| Tasks | `feat-XXX-name.md` | `feat-013-session-tree.md` |
| Feature Record | `feat-XXX.json` | `feat-013.json` |

**Note:** The canonical `id` in the JSON record must match the `.md` prefix.

---

## 6. Anti-Patterns

- creating `feat-013-tasks.md` when `feat-013.md` already exists
- leaving two task files for the same feature
- using generic names (`fix.md`, `update.md`) without `feat-XXX`

---

## 7. Operational Decision

As of 2026-04-04:

- all new work uses `feat-XXX-descriptive-name.md`
- old files are kept until re-audited
- no massive cleanup is done without a re-audit plan
