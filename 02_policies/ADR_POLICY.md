# Policy: Architecture Decision Records (ADRs)

> **Diátaxis Mode**: Reference
> **Status:** Active
> **Date:** 2026-04-26
> **Scope:** All architectural and philosophical decisions affecting the project

---

## 1. Purpose

Define when, how, and by whom an Architecture Decision Record (ADR) must be written.

An ADR is a document that captures a significant architectural decision along with its context and consequences. It is the single source of truth for why the project is built the way it is.

This policy prevents:
- **Decision amnesia**: Nobody remembers why a critical choice was made
- **Authority drift**: Decisions are made implicitly without traceability
- **Repeated debates**: The same architectural questions are rehashed because the rationale was not recorded

---

## 2. When to Write an ADR

Write an ADR when ANY of the following conditions apply:

| Condition | Example |
|-----------|---------|
| **New dependency** | Adding a database, framework, or external service |
| **Structural pattern change** | Moving from monolith to microservices, changing API style |
| **Technology replacement** | Switching from Python to Go, from REST to gRPC |
| **Philosophy change** | Modifying `PROJECT_MANIFEST.md` priorities or non-goals |
| **Breaking contract** | Changing a validated spec's public interface or behavior |
| **Cross-cutting concern** | Affecting more than 2 features or the entire pipeline |

Do **NOT** write an ADR for:
- Routine library updates (patch/minor versions)
- Code refactoring within an existing pattern
- Feature-level decisions already covered by the feature's design doc
- Bug fixes (unless the fix reveals a structural flaw)

---

## 3. Who Can Propose an ADR

| Role | Can Propose | Can Approve |
|------|-------------|-------------|
| **Tech Lead** | ✅ Yes | ✅ Yes |
| **Architect** | ✅ Yes | ✅ Yes |
| **Senior Engineer** | ✅ Yes | ❌ No (requires Tech Lead or Architect approval) |
| **Product Owner** | ✅ Yes (philosophy/scope only) | ❌ No (technical ADRs) |

---

## 4. Approval Process

1. **Propose**: Create a draft ADR using `docs/sdd/templates/adr.md`
2. **Review**: At least one reviewer from a different role must approve
3. **Record**: Save the approved ADR to `docs/sdd/artifacts/adr/`
4. **Link**: Reference the ADR in `docs/sdd/04_project_governance/PROJECT_MANIFEST.md` changelog and any affected specs

---

## 5. Where ADRs Live

- **Draft**: Any branch or working directory
- **Approved**: `docs/sdd/artifacts/adr/ADR-{NNN}-{short-name}.md`
- **Superseded**: Keep in place; mark status as `SUPERSEDED by ADR-XXX`

---

## 6. ADR Lifecycle

```
PROPOSED → REVIEW → ACCEPTED → [SUPERSEDED]
   ↓          ↓
REJECTED   CHANGES_REQUESTED
```

- **PROPOSED**: Draft exists, under discussion
- **REVIEW**: Under explicit review by at least one other role
- **ACCEPTED**: Approved and recorded
- **SUPERSEDED**: A newer ADR replaces this one (old one remains for traceability)
- **REJECTED**: Explicitly rejected with rationale recorded

---

## 7. Relationship with SDD

| Scenario | Action |
|----------|--------|
| ADR affects feature behavior | Capture follow-up through the current protocol; do not synthesize an undeclared transition for an already-advanced feature |
| ADR changes project philosophy | Update `PROJECT_MANIFEST.md`; review all active features for compliance |
| ADR introduces a new pattern | Update `templates/` and notify all active implementers |
| ADR is superseded | Review all features that reference the old ADR; update or validate |

---

## 8. Minimum Content

Every ADR MUST contain:

1. **Context** — What forces are at play? What problem does this solve?
2. **Decision** — The concrete decision in one sentence
3. **Consequences** — Positive, negative, and neutral outcomes
4. **Alternatives Considered** — At least one alternative with pros/cons
5. **Implications for SDD** — Which specs or features are affected?

Use `docs/sdd/templates/adr.md` as the starting point.

---

## 9. Anti-Patterns

- **ADR as spec**: An ADR explains WHY, not HOW. The spec explains HOW.
- **ADR without consequences**: Every decision has tradeoffs. If there are no negatives, the decision was not significant enough for an ADR.
- **ADR without alternatives**: If there was no alternative, the decision was either trivial or the exploration was insufficient.
- **Silent ADR updates**: Never modify an ACCEPTED ADR without creating a new one or explicitly superseding it.

---

## 10. Related Documents

- `docs/sdd/templates/adr.md` — ADR template
- `docs/sdd/04_project_governance/PROJECT_MANIFEST.md` — project philosophy and constraints
- `docs/sdd/02_policies/VALIDATION_BOUNDARIES_POLICY.md` — canonical correction boundaries
- `docs/sdd/00_core/AGENT_DECISION_TABLE.md` — when a change requires an ADR vs. a code adjustment
