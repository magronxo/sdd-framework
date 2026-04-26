# SDD Feature Format

Every feature is represented by a document of type `SYSTEM_SPEC`. This document is the single source of truth for feature progress.

## Required Fields

```json
{
  "id": "feat-<seq>",                 // e.g.: feat-001
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",                  // canonical states: DESIGN, SPEC, VALIDATION, TASKS, IMPLEMENT, VERIFY, AUDIT, ARCHIVE (DONE = legacy alias)
  "title": "Brief description",
  "created_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-28T10:00:00Z"
}
```

## Canonical States

| State | Meaning |
|-------|---------|
| **DESIGN** | Feature defined at WHAT level, but not yet specified |
| **SPEC** | Spec written; may still have pending validation feedback |
| **VALIDATION** | Phase of completeness and determinism review |
| **TASKS** | Minimal, ordered work breakdown (derived from a validated spec) |
| **IMPLEMENT** | Implementation in progress or ready to start |
| **VERIFY** | Verification of compliance against spec and SDT |
| **AUDIT** | External quality, coherence, and risk audit |
| **ARCHIVE** | Documental closure and consolidation |

**Legacy:** `DONE` exists in old feature records. Treat it as a **legacy alias of `ARCHIVE`**. Do not use for new work.

## Optional Fields by State

| State | Additional Fields |
|-------|------------------|
| **DESIGN** | `design_path` (string), `open_questions` (array) |
| **SPEC** | `spec_path` (string), `acceptance_criteria` (array Gherkin) |
| **VALIDATION** | `validation_result` (PASS/FAIL), `validated_at` (ISO8601), `validation_issues` (array, only if FAIL), `validation_details` (string, legacy/freeform) |
| **TASKS** | `task_path` (string), `task_list` (array) |
| **IMPLEMENT** | `implementation_notes` (string) |
| **VERIFY** | `verification_result` (PASS/FAIL), `verification_details` (string) |
| **AUDIT** | `audit_result` (PASS/WARN/FAIL), `audit_reasons` (array) |
| **ARCHIVE** | `archived_at` (ISO8601), `archive_notes` (string) |

## Cross-cutting Fields

These fields may appear in more than one state if they provide traceability:

- `design_path`
- `spec_path`
- `task_path`
- `task_list`
- `sdt_scenarios`
- `dependencies`
- `audit_result`
- `validation_result`

## Complete Example

```json
{
  "id": "feat-001",
  "type": "SYSTEM_SPEC",
  "state": "ARCHIVE",
  "title": "Implement path validation",
  "created_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-28T14:30:00Z",
  "design_path": "artifacts/design/feat-001-path-validation.md",
  "spec_path": "artifacts/specs/feat-001-path-validation.md",
  "sdt_scenarios": [
    {
      "scenario": "Path traversal with ..",
      "expected_behavior": "Reject with E_PATH_TRAVERSAL"
    }
  ],
  "task_path": "artifacts/tasks/feat-001-path-validation.md",
  "task_list": [
    "Implement path validator",
    "Add unit test",
    "Document error E_PATH_TRAVERSAL"
  ],
  "validation_result": "PASS",
  "verification_result": "PASS",
  "audit_result": "PASS",
  "archived_at": "2026-03-28T14:00:00Z",
  "archive_notes": "Feature completed and consolidated."
}
```

## File Naming (MANDATORY)

All feature files MUST follow this format:

```
feat-{NNN}-{short-name}.md
```

**Examples:**
- `feat-001-kernel-core.md`
- `feat-006-api-server.md`
- `feat-007-worker-pool.md`
- `feat-012-kernel-status-api.md`

**Each JSON file must point to actual paths via:**
```json
{
  "design_path": "artifacts/design/feat-NNN-short-name.md",
  "spec_path": "artifacts/specs/feat-NNN-short-name.md"
}
```

**Legacy (allowed only for traceability during migration):**
```json
{
  "design_path": "/SDD/artifacts/design/feat-NNN-short-name.md",
  "spec_path": "/SDD/artifacts/specs/feat-NNN-short-name.md"
}
```

## Notes

- The `id` field must be unique and sequential within the project.
- The `state` field can only contain values from the defined enumeration.
- Documents are saved to `artifacts/features_for_specs/` (or the path configured in `sdd.config.json`).
- If there are legacy or composite cases, they must be marked explicitly. Do not normalize them via silent exceptions.
