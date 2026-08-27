# Project Tour

> **Mode Diátaxis**: Reference

## Purpose

Provide a visual guide to Canonical SDD Model v1 in a product repository.

This file lives under `docs/` in the framework **source checkout**. Framework source paths such as `00_core/` and `01_execution/` are copied by the installer below the product repository's `docs/sdd/` root. Current-use paths in this guide are product-repository-relative installed paths.

---

## Installed Product Repository at a Glance

```text
product-repo/
├─ product source and tests/           Product-owned
└─ docs/
   └─ sdd/
      ├─ AGENTS.md                     Agent entrypoint
      ├─ sdd.config.json               Live configuration
      ├─ 00_core/                      Runtime and handoff contracts
      ├─ 01_execution/
      │  └─ prompts/                   Role prompts
      ├─ 02_policies/                  Governance policies
      ├─ 03_operations/
      │  └─ pre_sdd/                   Seed intake before feature records
      ├─ 04_project_governance/        Project identity and navigation
      ├─ templates/                    Reusable document templates
      ├─ contract/v1/                  Machine-readable authority
      ├─ tools/sdd_validate.py         Read-only validator/gate evaluator
      └─ artifacts/                    Generated SDD deliverables
         ├─ features_for_specs/        Feature records
         ├─ design/                    Design documents
         ├─ specs/                     Validated specifications
         ├─ tasks/                     Task breakdowns
         ├─ audit_reports/             Verification/audit evidence
         └─ adr/                       Architecture decisions
```

Product source remains outside `docs/sdd/`. Canonical feature-record paths are repository-relative and begin with `docs/sdd/artifacts/`.

---

## Quick Finder

| I need to... | Installed product path |
|---|---|
| Understand agent authority | `docs/sdd/AGENTS.md` then `docs/sdd/00_core/SDD_RUNTIME.md` |
| Find a feature spec | `docs/sdd/artifacts/specs/` |
| Check validation evidence | `docs/sdd/artifacts/features_for_specs/*.json` |
| Submit a new seed | `docs/sdd/03_operations/pre_sdd/templates/seed_dossier.md` |
| Know whether implementation may start | Read the canonical feature record and protocol gates; effective validation PASS is required |
| Write a design | `docs/sdd/templates/design.md` |
| Write a spec | `docs/sdd/templates/specs.md` |
| Record an ADR | `docs/sdd/templates/adr.md` and `docs/sdd/02_policies/ADR_POLICY.md` |
| Understand report format | `docs/sdd/02_policies/REPORT_ENVELOPE_POLICY.md` |
| Check feature size limits | `docs/sdd/02_policies/DECOMPOSITION_AND_SIZE_POLICY.md` |
| Find audit reports | `docs/sdd/artifacts/audit_reports/` |
| Understand project terminology | `docs/sdd/04_project_governance/GLOSSARY.md` |

---

## Role Reading Paths

### Developer

1. `docs/sdd/04_project_governance/GLOSSARY.md`
2. `docs/sdd/00_core/SDD_RUNTIME.md`
3. Validated spec and task document under `docs/sdd/artifacts/`

### Product Manager

1. `docs/sdd/04_project_governance/PROJECT_MANIFEST.md`
2. `docs/sdd/03_operations/pre_sdd/PRE_SDD_CONTRACT.md`
3. `docs/sdd/03_operations/pre_sdd/seeds/`

### Agent

1. `docs/sdd/AGENTS.md`
2. `docs/sdd/sdd.config.json`
3. `docs/sdd/00_core/SDD_RUNTIME.md`
4. `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`

### Auditor

1. `docs/sdd/02_policies/REPORT_ENVELOPE_POLICY.md`
2. `docs/sdd/02_policies/INTEGRATION_SURFACE_POLICY.md`
3. Canonical feature record, validated spec, implementation, and verification evidence

---

## Source-checkout Documentation Context

When maintaining the framework itself, these source files are not installed paths:

- `docs/GETTING_STARTED.md`
- `docs/SDD_PIPELINE_VISUAL.md`
- `docs/PROJECT_TOUR.md`

Their lifecycle examples nevertheless use installed product paths (`docs/sdd/...`) so users do not persist root-level artifact paths.

---

## Related Installed Documents

- `docs/sdd/04_project_governance/PROJECT_MAP.md`
- `docs/sdd/00_core/SDD_RUNTIME.md`
- `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`
