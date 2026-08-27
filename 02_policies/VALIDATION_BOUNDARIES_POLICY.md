# Policy: Validation Boundaries

> **Mode Diátaxis**: Reference

## Purpose

Define when a document is **authoritative** (binding) versus **proposed** (draft) without adding feature-record fields or lifecycle transitions beyond Canonical SDD Model v1.

Machine-readable authority remains:

- `docs/sdd/contract/v1/feature-record.schema.json` for feature-record fields;
- `docs/sdd/contract/v1/sdd-protocol.json` for transitions, regressions, and gates.

This policy prevents:

- implementing from unvalidated specs;
- treating legacy specs as current truth;
- confusing documentary review status with persistent feature state.

---

## Documentary Status and Authority

Documentary labels such as Draft, Under Review, Superseded, and Legacy are document-local descriptions. They are not feature-record states.

| Documentary status | Authority | Mutation rule |
|---|---|---|
| **Draft / Under Review** | Proposed | May be revised by the role that owns the current canonical phase. |
| **Validated spec** | Authoritative for feature behavior | Implementation must follow it; do not silently revise it. |
| **Superseded / Legacy** | Historical, non-authoritative | Preserve for traceability; see `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md`. |

---

## Authority by Artifact Type

### Feature Records (`docs/sdd/artifacts/features_for_specs/*.json`)

- Fields must conform to the closed v1 schema.
- `state` changes only through protocol-declared transitions or regressions.
- Canonical writes use `id`, `task_path`, and `docs/sdd/artifacts/...` paths.
- No policy-local metadata may be added to a feature record.

### Design Documents (`docs/sdd/artifacts/design/*.md`)

- During DESIGN, the design is proposed and may be refined.
- `DESIGN -> SPEC` records the completed design as the WHAT input for specification.
- A later role must not silently rewrite the design.

### Spec Documents (`docs/sdd/artifacts/specs/*.md`)

- During SPEC, the spec is proposed and may be refined.
- `SPEC -> VALIDATION` submits it for validation.
- `VALIDATION PASS -> TASKS` makes the validated spec the behavioral authority for planning and implementation.
- `VALIDATION FAIL -> SPEC` is the declared correction regression.

### Task Documents (`docs/sdd/artifacts/tasks/*.md`)

- During TASKS, the Planner may refine the plan.
- `TASKS -> IMPLEMENT` hands the completed task document to the Implementer.
- Task documents do not authorize redesign or spec changes.

### Audit Reports (`docs/sdd/artifacts/audit_reports/*.md`)

- Reports provide evidence and findings; they do not mutate records by themselves.
- The standard Auditor records the canonical `audit_result` and `audited_at` on the feature record.
- `AUDIT PASS` or `AUDIT WARN` may satisfy the audit gate when all other requirements pass.
- `AUDIT FAIL` blocks `AUDIT -> ARCHIVE` unless a valid `owner_waiver` satisfies the protocol.
- `AUDIT FAIL` does not prevent corrective work, but v1 selects no automatic repair state.

---

## Correction and Reopening Boundary

Canonical v1 declares exactly these correction regressions:

- `VALIDATION FAIL -> SPEC`;
- `VERIFY FAIL -> IMPLEMENT`.

It does not declare a general transition from an arbitrary later state back to SPEC or DESIGN. Therefore:

1. Use the declared regression when its source state and trigger apply.
2. Do not write an undeclared state change or private reopening metadata.
3. If new scope or a missed requirement is discovered outside a declared regression, capture it as a new seed/feature or stop for an explicit future protocol decision.
4. Any future general reopening mechanism requires a protocol revision; policy prose alone cannot create it.

| Situation | Canonical v1 action |
|---|---|
| Validation finds a spec defect | Record FAIL evidence and use `VALIDATION -> SPEC`. |
| Verification finds an implementation mismatch | Record FAIL evidence and use `VERIFY -> IMPLEMENT`. |
| Scope expansion or new requirement | Capture a new seed and feature; do not silently alter the active validated spec. |
| AUDIT FAIL | Remain governed by the audit archive gate; no automatic repair state is selected. |

---

## Cross-Reference Integrity

When an authoritative document changes through an allowed workflow, review all dependent references for consistency. A policy review may identify needed follow-up, but it must not synthesize undeclared feature-state transitions.

---

## Anti-Patterns

- **Silent spec changes**: modifying a validated spec outside the declared workflow.
- **Private reopening fields**: adding policy-specific metadata not present in the schema.
- **Design drift**: changing the WHAT during IMPLEMENT.
- **Legacy override**: using an old spec as current authority.
- **Audit dismissal**: treating AUDIT FAIL as merely informational even though it blocks archival under the protocol.

---

## Related Documents

- `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md`
- `docs/sdd/02_policies/REPORT_ENVELOPE_POLICY.md`
- `docs/sdd/00_core/SDD_RUNTIME.md`
- `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`
