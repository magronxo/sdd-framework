# Policy: Validation Boundaries

> **Mode Diátaxis**: Reference

## Purpose

Define when a document is **authoritative** (binding) vs **proposed** (draft) during the SDD lifecycle.

This prevents:
- Implementing from unvalidated specs
- Treating legacy specs as current truth
- Confusion about which version of a design is "the real one"

---

## Document States and Authority

| State | Authority | Can Modify | Who Can Modify |
|-------|-----------|------------|----------------|
| **Draft** | Proposed | Yes | Author, with feedback |
| **Under Review** | Proposed | Yes | Reviewers with comments |
| **Validated** | Authoritative | No | No one without reopening |
| **Superseded** | Non-authoritative | No | Archived for traceability |
| **Legacy** | Non-authoritative | No | Read-only, see `02_policies/LEGACY_SPECS_POLICY.md` |

---

## Authority by Artifact Type

### Feature Records (`artifacts/features_for_specs/*.json`)

| Field | Authority Rule |
|-------|---------------|
| `state` | Authoritative when current; may change via state transitions only |
| `validation_result` | Authoritative once `"PASS"`; changing it requires reopening to SPEC |
| `spec_path` | Authoritative once validated; path changes require traceability |
| `design_path` | Authoritative once DESIGN is complete |
| `implementation_notes` | Informational; does not override spec |

### Design Documents (`artifacts/design/*.md`)

| Phase | Authority | Notes |
|-------|-----------|-------|
| During DESIGN | Proposed | Designer can iterate freely |
| After DESIGN → SPEC | Authoritative for "WHAT" | Specifier uses it as input; cannot change the "WHAT" without reopening |
| After ARCHIVE | Non-authoritative | Historical reference only |

### Spec Documents (`artifacts/specs/*.md`)

| Phase | Authority | Notes |
|-------|-----------|-------|
| During SPEC | Proposed | Specifier can iterate freely |
| After VALIDATION = PASS | **Authoritative** | This is the contract. No implementation may deviate without reopening. |
| After VALIDATION = FAIL | Proposed | Return to SPEC for fixes |
| After ARCHIVE | Non-authoritative | New work requires a new feature/spec |

### Task Documents (`artifacts/tasks/*.md`)

| Phase | Authority | Notes |
|-------|-----------|-------|
| During TASKS | Proposed | Planner can iterate |
| After IMPLEMENT starts | Authoritative for execution | Implementer follows tasks; deviations require Planner approval |
| After VERIFY | Non-authoritative | Historical record |

### Audit Reports (`artifacts/audit_reports/*.md`)

| Phase | Authority | Notes |
|-------|-----------|-------|
| Always | Informational | Audits do not block by themselves; they generate findings and recommendations |
| If audit is FAIL | The findings are authoritative | Must be addressed, but the audit itself does not modify the spec |

---

## Reopening Rules

### Valid Reopening Conditions

A validated spec may be reopened only under these conditions:

1. **New information**: A requirement was missed during DESIGN
2. **Bug in spec**: The spec itself contains an error (not the implementation)
3. **External change**: A dependency or constraint changed after validation

### What Is NOT Reopening

| Situation | Correct Action |
|-----------|---------------|
| **Scope expansion** | The feature needs to do more → capture a new seed and create a new feature. Do not reopen the existing spec. |
| **New requirement** | Same as scope expansion: new seed → new feature. |
| **Implementation bug** | Fix the code, not the spec. The spec is authoritative. |

### Reopening Process

1. Capture the reason as a new seed or bug report
2. Set feature state back to `SPEC` (not DESIGN, unless the "WHAT" changes)
3. Modify the spec
4. Re-run VALIDATION
5. Record the reopening in the feature record (`reopened_at`, `reopened_reason`)

---

## Cross-Reference Integrity

When a document is authoritative, all documents that reference it must be consistent:

- If `spec.md` changes, `tasks.md` may need updating (re-run TASKS phase)
- If `design.md` changes, `spec.md` must be revalidated
- If `PROJECT_MANIFEST.md` changes, all active features must be reviewed for compliance

---

## Anti-Patterns

- **Silent spec changes**: Modifying a spec after VALIDATION without reopening
- **Design drift**: Changing the "WHAT" during IMPLEMENT without updating the design
- **Legacy override**: Using an old spec because "it was good enough"
- **Audit as veto**: Treating an audit FAIL as a block instead of a finding generator

---

## Related Documents

- `02_policies/LEGACY_SPECS_POLICY.md` — legacy spec handling
- `02_policies/REPORT_ENVELOPE_POLICY.md` — audit report format
- `00_core/SDD_RUNTIME.md` — canonical pipeline and states
- `00_core/SDD_HANDOFF_CONTRACT.md` — role boundaries and handoff rules
