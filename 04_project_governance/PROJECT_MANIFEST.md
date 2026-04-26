# Project Manifest

> **Mode Diátaxis**: Reference

## Purpose

Define the **identity, philosophy, and non-negotiable constraints** of this project.

This document is the **north star** for all technical and product decisions. When in doubt, consult the Manifest.

---

## Project Identity

| Field | Value |
|-------|-------|
| **Name** | `{PROJECT_NAME}` |
| **One-line purpose** | `{ONE_LINE_DESCRIPTION}` |
| **Version** | `{MAJOR.MINOR.PATCH}` |
| **Status** | `planning / active / maintenance / sunset` |

---

## Philosophy

### What we optimize for

1. **{FIRST_PRIORITY}** — e.g., correctness, speed, developer experience, user trust
2. **{SECOND_PRIORITY}** — e.g., simplicity, observability, portability
3. **{THIRD_PRIORITY}** — e.g., performance, cost, accessibility

### What we accept as trade-off

- `{TRADE_OFF_1}` → because `{REASON}`
- `{TRADE_OFF_2}` → because `{REASON}`

---

## Technology Stack

### Languages
- `{PRIMARY_LANGUAGE}` — `{RATIONALE}`
- `{SECONDARY_LANGUAGE}` — `{RATIONALE}`

### Frameworks & Libraries
- `{FRAMEWORK_1}` — `{USE_CASE}`
- `{FRAMEWORK_2}` — `{USE_CASE}`

### Infrastructure
- `{PLATFORM_1}` — `{PURPOSE}`
- `{PLATFORM_2}` — `{PURPOSE}`

### Constraints
- Minimum version: `{VERSION}`
- Target environments: `{ENV_LIST}`

---

## Non-Negotiables

These constraints are **immutable** without a formal Architecture Decision Record (ADR).

1. **{CONSTRAINT_1}** — e.g., "No external dependencies without security review"
2. **{CONSTRAINT_2}** — e.g., "All public APIs must be versioned"
3. **{CONSTRAINT_3}** — e.g., "Zero tolerance for unhandled panics in production"

---

## Success Criteria

How do we know this project is successful?

- **Functional**: `{CRITERION_1}`
- **Quality**: `{CRITERION_2}`
- **Operational**: `{CRITERION_3}`
- **Business**: `{CRITERION_4}`

---

## Non-Goals

Explicitly out of scope to prevent scope creep:

1. `{NON_GOAL_1}` — e.g., "Multi-tenancy in v1"
2. `{NON_GOAL_2}` — e.g., "Mobile native applications"
3. `{NON_GOAL_3}` — e.g., "Real-time collaboration"

---

## Change Policy

### How to modify this Manifest

1. Open an ADR (`templates/adr.md`) explaining **why** the change is necessary
2. Get explicit approval from `{DECISION_MAKER_ROLE}`
3. Update this document with a changelog entry
4. Update `sdd.config.json` if stack changes

### Changelog

| Date | Version | Change | ADR Reference |
|------|---------|--------|---------------|
| `{DATE}` | `{VERSION}` | `{DESCRIPTION}` | `{ADR_FILE}` |

---

## Related Documents

- `sdd.config.json` — machine-readable project configuration
- `04_project_governance/GLOSSARY.md` — project-specific terminology
- `04_project_governance/PROJECT_MAP.md` — repository navigation
- `02_policies/ADR_POLICY.md` — when and how to write ADRs
