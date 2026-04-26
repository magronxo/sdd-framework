# Policy: Feature Decomposition and Size Limits

> **Diátaxis Mode**: Reference
> **Status:** Active
> **Date:** 2026-04-23
> **Scope:** All SDD features

---

## 1. Purpose

Prevent two extreme pathologies:

1. **Giant features**: A single feature spanning multiple capabilities, resulting in 500+ line specs, endless tasks, and audits that never finish.
2. **Microscopic features**: Every line change is a new feature, generating bureaucratic overhead that exceeds the value of the change.

This policy defines objective criteria for deciding when to decompose and when to consolidate.

---

## 2. Size Limits

### 2.1 Upper Limit (Decomposition Trigger)

A feature **MUST** be decomposed if it meets **any** of these criteria:

| Metric | Limit | What we count |
|--------|-------|---------------|
| **Spec lines** | > 300 lines | Entire file `specs/<feature>.md` |
| **FR count** | > 15 functional requirements | FR-01, FR-02, ... |
| **Task count** | > 12 tasks | All T1, T2, ... in `tasks/<feature>.md` |
| **Component count** | > 5 new components | In the "Components" section of the design |
| **Surface count** | > 3 active surfaces | browser + os_fs + wiring + network + env_proxy |
| **Implementation files** | > 8 new/modified files | Estimate in the design |
| **Estimated duration** | > 5 days of continuous work | Planner calculation |

**Action:** If a limit is exceeded, the Planner must propose decomposition before generating tasks.

### 2.2 Lower Limit (Consolidation Trigger)

A feature **MUST NOT** be independent if it meets **ALL** of these criteria:

| Metric | Limit | What we count |
|--------|-------|---------------|
| **Spec lines** | < 50 lines | Entire file |
| **FR count** | ≤ 2 requirements | |
| **Task count** | ≤ 2 tasks | |
| **Surface count** | 1 surface (wiring) | |
| **Estimated duration** | < 2 hours | |

**Action:** Consolidate as a sub-task of a larger feature, or treat as a "code adjustment" (see `AGENT_DECISION_TABLE.md`).

---

## 3. Decomposition Criteria

When a feature exceeds the upper limit, apply these criteria to cut:

### 3.1 By Layer
Separate by independent layers:
- API / Handler (surface: wiring)
- Business logic / Core (surface: os_fs or none)
- Persistence / Storage (surface: os_fs)
- Client / UI (surface: browser)

### 3.2 By Surface
Separate by integration surface:
- Feature A: backend (wiring + os_fs)
- Feature B: frontend (browser)
- Feature C: networking (network)

### 3.3 By State (State Machine)
Separate by independent lifecycle states:
- Feature A: Creation and validation
- Feature B: Processing
- Feature C: Archival and cleanup

### 3.4 By Actor
Separate by interacting role:
- Feature A: Human operator (HITL)
- Feature B: Automated system
- Feature C: External audit

---

## 4. Decomposition Rules

1. **Dependencies first**: The base feature (that others need) is done first.
2. **No circular deps**: If A depends on B and B depends on A, the cut is incorrect.
3. **Preserve contract**: Each sub-feature has its own complete spec (you cannot leave a spec "half-done").
4. **Shared design**: Sub-features may share a parent design doc if a `feat-XXX-parent-design.md` is created.
5. **Sequential IDs**: Sub-features use suffixes: `feat-007-a`, `feat-007-b`, or a new sequence `feat-008`, `feat-009`.

---

## 5. Anti-Patterns

- **Premature decomposition**: Cutting a 200-line feature "just in case" → unnecessary overhead
- **Artificial layer decomposition**: Creating "feature API" and "feature core" when they are actually inseparable
- **Lazy consolidation**: Merging 3 independent features to "save time" → oversized specs

---

## 6. Operational Decision

As of 2026-04-23:

- The Planner is responsible for detecting size limits and proposing decomposition
- The Designer can anticipate decomposition in the design doc (section "Proposed Sub-features")
- The Validator verifies that sub-features do not have circular dependencies
- A 320-line feature is not penalized if it has explicit justification in the design (but requires approval)
