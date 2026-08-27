# Project Glossary

> **Mode Diátaxis**: Reference

## Purpose

Eliminate ambiguity by defining **project-specific terminology**.

This document is the **single source of truth for language**. If a term appears here, this definition overrides all external sources (including framework documentation).

---

## How to Use This Document

- **Before writing a spec**: check if your domain terms are defined here
- **Before reviewing code**: ensure the implementation uses the same vocabulary as the spec
- **During onboarding**: read this first to understand the project's dialect

---

## Adding a Term

1. Use the template below
2. Place the term in the correct section (or create a new one)
3. If the term conflicts with an external definition, add a **Disambiguation** note

### Entry Template

```markdown
### {TERM}

**Category**: `{technical | product | business | process}`

**Definition**: {One clear sentence.}

**In this project, it means**: {Specific nuance or constraint.}

**Not to be confused with**: {Related but different term.}

**Used in**: `{files, specs, or domains where this term appears}`
```

---

## Core Concepts

### {CORE_TERM_1}

**Category**: `{technical | product | business | process}`

**Definition**: `{DEFINITION}`

**In this project, it means**: `{PROJECT_SPECIFIC_MEANING}`

**Not to be confused with**: `{OTHER_TERM}`

**Used in**: `{docs/sdd/artifacts/specs/, product source, product docs}`

### {CORE_TERM_2}

*(Repeat as needed)*

---

## Technical Terms

### {TECH_TERM_1}

**Category**: `technical`

**Definition**: `{DEFINITION}`

**In this project, it means**: `{PROJECT_SPECIFIC_MEANING}`

**Not to be confused with**: `{OTHER_TERM}`

**Used in**: `{src/, tests/}`

---

## Product Terms

### {PRODUCT_TERM_1}

**Category**: `product`

**Definition**: `{DEFINITION}`

**In this project, it means**: `{PROJECT_SPECIFIC_MEANING}`

**Not to be confused with**: `{OTHER_TERM}`

**Used in**: `{docs/sdd/artifacts/design/, docs/sdd/04_project_governance/}`

---

## Process Terms

### SDD Feature

**Category**: `process`

**Definition**: A unit of work that flows through the Spec-Driven Development pipeline.

**In this project, it means**: A canonical feature record under `docs/sdd/artifacts/features_for_specs/` with an `id` and evidence accumulated through the persistent lifecycle.

**Not to be confused with**: A GitHub issue, a user story, or a seed.

**Used in**: `docs/sdd/00_core/SDD_RUNTIME.md`, `docs/sdd/01_execution/`

### Seed

**Category**: `process`

**Definition**: A raw idea, bug report, or feedback item captured before SDD triage.

**In this project, it means**: Any input to the system that has not yet passed through the Pre-SDD contract and been promoted to a feature.

**Not to be confused with**: A feature (a seed becomes a feature only after triage and approval).

**Used in**: `docs/sdd/03_operations/pre_sdd/`

### Validation

**Category**: `process`

**Definition**: The phase where a spec is verified for completeness, determinism, and implementability.

**In this project, it means**: A PASS/FAIL gate recorded in the feature record. No implementation may begin without VALIDATION = PASS.

**Not to be confused with**: Testing (verification happens after implementation; validation happens before).

**Used in**: `docs/sdd/00_core/SDD_RUNTIME.md`, `docs/sdd/01_execution/prompts/validator.md`

---

## Disambiguation Table

| Term | In General | In This Project |
|------|-----------|-----------------|
| `{TERM_A}` | `{GENERAL_MEANING}` | `{PROJECT_MEANING}` |
| `{TERM_B}` | `{GENERAL_MEANING}` | `{PROJECT_MEANING}` |

---

## Related Documents

- `docs/sdd/04_project_governance/PROJECT_MANIFEST.md` — project philosophy and constraints
- `docs/sdd/04_project_governance/PROJECT_MAP.md` — where to find specs, designs, and code
- `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md` — how terminology evolves across versions
