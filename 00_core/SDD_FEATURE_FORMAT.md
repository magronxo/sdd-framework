# SDD Feature Format

Every feature is represented by a document of type `SYSTEM_SPEC`. This document is the single source of truth for feature progress.

---

## Canonical Location

Installed SDD instances live under:

```text
docs/sdd/
```

Feature records live under:

```text
docs/sdd/artifacts/features_for_specs/
```

---

## Required Fields

```json
{
  "id": "feat-001",
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",
  "title": "Brief description",
  "created_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-28T10:00:00Z"
}
```

---

## Canonical States

| State | Meaning |
|-------|---------|
| DESIGN | Feature defined at WHAT level, but not yet specified |
| SPEC | Spec written; may still have pending validation feedback |
| VALIDATION | Phase of completeness and determinism review |
| TASKS | Minimal, ordered work breakdown derived from a validated spec |
| IMPLEMENT | Implementation in progress or ready to start |
| VERIFY | Verification of compliance against spec and SDT |
| AUDIT | Quality, coherence, risk, and traceability audit |
| ARCHIVE | Documental closure and consolidation |

Legacy: `DONE` exists in old feature records. Treat it as a legacy alias of `ARCHIVE`. Do not use it for new work.

---

## Optional Fields by State

| State | Additional Fields |
|-------|------------------|
| DESIGN | `design_path` (string), `open_questions` (array) |
| SPEC | `spec_path` (string), `acceptance_criteria` (array Gherkin) |
| VALIDATION | `validation_result` (PASS/FAIL), `validated_at` (ISO8601), `validation_issues` (array, only if FAIL), `validation_details` (string, legacy/freeform) |
| TASKS | `task_path` (string), `task_list` (array) |
| IMPLEMENT | `implementation_notes` (string) |
| VERIFY | `verification_result` (PASS/FAIL), `verification_details` (string) |
| AUDIT | `audit_result` (PASS/WARN/FAIL), `audit_reasons` (array), `audit_report_path` (string), `owner_waiver` (object, only if FAIL is waived) |
| ARCHIVE | `archived_at` (ISO8601), `archive_notes` (string) |

---

## Cross-cutting Fields

These fields may appear in more than one state if they provide traceability:

- `design_path`
- `spec_path`
- `task_path`
- `task_list`
- `sdt_scenarios`
- `dependencies`
- `audit_result`
- `audit_report_path`
- `validation_result`

---

## Complete Example

```json
{
  "id": "feat-001",
  "type": "SYSTEM_SPEC",
  "state": "ARCHIVE",
  "title": "Implement path validation",
  "created_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-28T14:30:00Z",
  "design_path": "docs/sdd/artifacts/design/feat-001-path-validation.md",
  "spec_path": "docs/sdd/artifacts/specs/feat-001-path-validation.md",
  "sdt_scenarios": [
    {
      "scenario": "Path traversal with ..",
      "expected_behavior": "Reject with E_PATH_TRAVERSAL"
    }
  ],
  "task_path": "docs/sdd/artifacts/tasks/feat-001-path-validation.md",
  "task_list": [
    "Implement path validator",
    "Add unit test",
    "Document error E_PATH_TRAVERSAL"
  ],
  "validation_result": "PASS",
  "verification_result": "PASS",
  "audit_result": "PASS",
  "audit_report_path": "docs/sdd/artifacts/audit_reports/audit_feat-001_2026-03-28.md",
  "archived_at": "2026-03-28T14:00:00Z",
  "archive_notes": "Feature completed and consolidated."
}
```

---

## File Naming (MANDATORY)

All feature markdown documents MUST follow this format:

```text
feat-{NNN}-{short-name}.md
```

Feature record JSON files MUST follow this format:

```text
feat-{NNN}-{short-name}.json
```

Examples:

- `feat-001-kernel-core.md`
- `feat-006-api-server.md`
- `feat-007-worker-pool.md`
- `feat-012-kernel-status-api.md`
- `feat-001-kernel-core.json`

Each JSON file must point to actual repo-relative paths via:

```json
{
  "design_path": "docs/sdd/artifacts/design/feat-NNN-short-name.md",
  "spec_path": "docs/sdd/artifacts/specs/feat-NNN-short-name.md",
  "task_path": "docs/sdd/artifacts/tasks/feat-NNN-short-name.md"
}
```

Legacy paths are allowed only for traceability during migration:

```json
{
  "design_path": "artifacts/design/feat-NNN-short-name.md",
  "spec_path": "/SDD/artifacts/specs/feat-NNN-short-name.md"
}
```

Do not normalize legacy paths via silent exceptions. Mark migration status explicitly.

---

## Audit Gate Field

If `audit_result` is `FAIL`, the feature MUST NOT move to `ARCHIVE` unless one of these is true:

1. A later audit result changes the gate to PASS/WARN.
2. An explicit owner waiver is recorded in `owner_waiver`.

Example waiver field:

```json
{
  "owner_waiver": {
    "waived_by": "project owner",
    "waived_at": "2026-03-28T15:00:00Z",
    "reason": "Accepted risk for non-release internal prototype"
  }
}
```

---

## Notes

- The `id` field must be unique and sequential within the project.
- The `state` field can only contain values from the defined enumeration.
- Documents are saved to configured paths in `docs/sdd/sdd.config.json`.
- Default feature records live under `docs/sdd/artifacts/features_for_specs/`.
- Examples are educational only and never authority.
