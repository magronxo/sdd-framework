# Legacy Specs Policy (Kill Debt)

## Purpose

Allow legacy / non-normalized specs to exist for historical traceability **without** letting them leak into runtime decisions or implementation.

This policy is designed to prevent “paper complete” drift.

---

## Definitions

**Canonical spec**
A spec located under `artifacts/specs/` that is intended to govern behavior.

**Legacy spec / legacy content**
Any spec-like document that is:
- outside `artifacts/specs/`, or
- inside artifacts but not validated / not aligned with runtime, or
- known to be stale / incomplete / inconsistent with code.

Legacy content may be informative, but it is not authoritative.

---

## Hard Rules

1) **No validated canonical spec → no implementation.**
If a spec is legacy, it cannot be used to justify code changes.

2) **Legacy specs are read-only references.**
They can inform discussion and re-audit, but they do not define behavior.

3) **Promotion requires gates.**
A legacy spec becomes canonical authority only after:
- `VALIDATION = PASS`, and
- tasks exist (`TASKS`), and
- implementation is verified (`VERIFY`), and
- an audit report exists (`AUDIT`), then archive (`ARCHIVE`).

4) **If docs disagree with code, code wins until corrected.**
The correction must happen by:
- updating the spec to match reality (and re-validating), or
- implementing missing behavior to satisfy the spec (and verifying).

---

## Operational Enforcement (what agents must do)

When a task references a spec:

1) Resolve the *canonical* spec path under `artifacts/specs/`.
2) If the spec is not validated, STOP and request VALIDATION.
3) If a spec/tasks doc claims “implemented”, but the code lacks it:
   - open an alignment report under `artifacts/audit_reports/`
   - re-open the feature state to `IMPLEMENT` (or earlier)
   - remove any “paper complete” claims from the feature record (move `implemented` items back to `pending`)

---

## Minimal Cleanup Strategy (no mass refactor)

We do **not** rewrite all legacy docs immediately.
We instead:

- keep legacy docs as traceability,
- enforce the gates so they can’t cause wrong implementation,
- promote only the specs we actively work on via re-audit + validation.
