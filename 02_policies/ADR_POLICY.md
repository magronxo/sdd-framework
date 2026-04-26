# Policy: Architecture Decision Records (ADR)

> **Mode Diátaxis**: Reference

## Purpose

Define when, how, and where to record **architecture decisions** that affect the project's structure, stack, or non-negotiable constraints.

An ADR is **not** for every code change. It is for decisions that:
- Are difficult or expensive to reverse
- Affect multiple features or teams
- Change a non-negotiable constraint (see `04_project_governance/PROJECT_MANIFEST.md`)
- Introduce or remove a significant dependency

---

## When to Write an ADR

### Must Write

| Situation | Example |
|-----------|---------|
| Changing the technology stack | "Switch from SQLite to PostgreSQL" |
| Adding a new integration surface | "Add WebSocket support for real-time updates" |
| Modifying a non-negotiable constraint | "Relax the 'no external dependencies' rule for auth" |
| Changing the SDD pipeline itself | "Add a new phase between DESIGN and SPEC" |
| Introducing a cross-cutting pattern | "Adopt CQRS across all services" |

### Should Write

| Situation | Example |
|-----------|---------|
| Significant refactor of core modules | "Split monolithic API into microservices" |
| Changing deployment strategy | "Move from VMs to Kubernetes" |
| New security model | "Implement mTLS for internal communication" |

### Do Not Write

| Situation | Example |
|-----------|---------|
| Routine library upgrades | "Upgrade React from 18.2 to 18.3" |
| Bug fixes | "Fix null pointer in login handler" |
| Small refactors within a single feature | "Extract helper function for validation" |
| Adding a new endpoint that follows existing patterns | "Add GET /users/{id}" |

---

## ADR Lifecycle

```
PROPOSED → REVIEWED → ACCEPTED | REJECTED | SUPERSEDED
```

| State | Meaning |
|-------|---------|
| **PROPOSED** | Draft written, awaiting review |
| **REVIEWED** | Reviewed by Tech Lead + stakeholders |
| **ACCEPTED** | Decision is active and binding |
| **REJECTED** | Decision was rejected, rationale recorded |
| **SUPERSEDED** | Replaced by a newer ADR (link to successor) |

---

## Where to Store ADRs

- **Location**: `artifacts/adr/` (or as configured in `sdd.config.json`)
- **Naming**: `adr-{NNN}-{short-description}.md`
- **Index**: `artifacts/adr/INDEX.md` — list of all ADRs with status and links

---

## Approval Process

1. **Author** writes ADR from `templates/adr.md`
2. **Tech Lead** reviews technical feasibility and alignment with `PROJECT_MANIFEST.md`
3. **Product Owner** reviews if it affects user-facing behavior or timeline
4. **Decision**: ACCEPTED (merge), REJECTED (close with rationale), or REVIEWED (request changes)

For changes to the Manifest's non-negotiables, add `{DECISION_MAKER_ROLE}` approval.

---

## Template

Use `templates/adr.md` for all new ADRs.

Required fields:
- Title and date
- Context (what forced the decision)
- Decision (what we chose)
- Consequences (positive and negative)
- Status

---

## Related Documents

- `templates/adr.md` — ADR template
- `04_project_governance/PROJECT_MANIFEST.md` — non-negotiable constraints and change policy
- `04_project_governance/PROJECT_MAP.md` — where ADRs live
