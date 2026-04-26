# Project Tour

> **Mode Diátaxis**: Reference

## Purpose

A **visual, scannable guide** to the repository.

If you are lost, start here. If you know what you need but not where it is, check the **Quick Finder** below.

---

## Repository at a Glance

```
sdd-framework/
│
├─ 📁 00_core/                        ← Start here for rules
│   ├─ SDD_RUNTIME.md                 Execution contract (agents)
│   ├─ SDD_GUIDE.md                   Full methodology (humans)
│   ├─ SDD_HANDOFF_CONTRACT.md        Who does what, when
│   ├─ SDD_READING_CONTRACT.md        Minimal reading guide
│   ├─ SDD_FEATURE_FORMAT.md          Feature record schema
│   └─ AGENT_DECISION_TABLE.md        When agents can decide
│
├─ 📁 01_execution/                   ← Agent brains
│   └─ prompts/
│       ├─ designer.md
│       ├─ specifier.md
│       ├─ validator.md
│       ├─ planner.md
│       ├─ implementer.md
│       ├─ verifier.md
│       └─ migration_auditor.md
│
├─ 📁 02_policies/                    ← Governance rules
│   ├─ ADR_POLICY.md                  When to write ADRs
│   ├─ DECOMPOSITION_AND_SIZE_POLICY.md  Feature size limits
│   ├─ INTEGRATION_SURFACE_POLICY.md  Surface definitions
│   ├─ LEGACY_SPECS_POLICY.md         Old specs are non-authoritative
│   ├─ REPORT_ENVELOPE_POLICY.md      Report format
│   ├─ SKILLS_SYSTEM.md               Skills registry rules
│   ├─ SPECS_REAUDIT_PRIORITIZATION_POLICY.md  Re-audit rules
│   └─ TASKS_NORMALIZATION_POLICY.md  Task format rules
│
├─ 📁 03_operations/                  ← Operational playbooks
│   ├─ WORKFLOW.md                    End-to-end workflow
│   ├─ SPEC_REAUDIT_WORKFLOW.md       Re-audit procedure
│   ├─ AUDIT_STRATEGY.md              Audit planning
│   └─ 📁 pre_sdd/                    ← Idea intake system
│       ├─ seeds/                     Active seeds
│       ├─ seeds/deferred/            Postponed
│       ├─ seeds/rejected/            Closed
│       ├─ seeds/promoted/            Became features
│       ├─ seeds/merged/              Consolidated
│       ├─ templates/
│       │   ├─ seed_dossier.md
│       │   └─ triage_batch.md
│       ├─ PRE_SDD_CONTRACT.md        Rules
│       └─ PRE_SDD_RUNTIME.md         Procedure
│
├─ 📁 04_project_governance/          ← Project identity
│   ├─ PROJECT_MANIFEST.md            Philosophy and constraints
│   ├─ GLOSSARY.md                    Terminology
│   └─ PROJECT_MAP.md                 Navigation (this is not it)
│
├─ 📁 templates/                      ← Reusable blanks
│   ├─ design.md
│   ├─ specs.md
│   └─ adr.md
│
├─ 📁 docs/                           ← Human guides
│   ├─ GETTING_STARTED.md             First feature tutorial
│   ├─ SDD_PIPELINE_VISUAL.md         Diagrams and flowcharts
│   └─ PROJECT_TOUR.md                This file
│
├─ 📁 artifacts/                      ← Generated work (DO NOT EDIT MANUALLY)
│   ├─ features_for_specs/            Feature records (JSON)
│   ├─ design/                        Design documents
│   ├─ specs/                         Validated specifications
│   ├─ tasks/                         Task breakdowns
│   ├─ audit_reports/                 Audit outputs
│   └─ adr/                           Architecture decisions
│
├─ sdd.config.json                    ← Project configuration
├─ AGENTS.md                          ← Agent entrypoint
├─ README.md                          ← Project overview
└─ init-sdd.ps1 / init-sdd.sh         ← Bootstrap scripts
```

---

## Quick Finder

| I need to... | Go to |
|-------------|-------|
| Understand how agents work | `AGENTS.md` → `00_core/SDD_RUNTIME.md` |
| Find the spec for a feature | `artifacts/specs/` |
| Check if a feature is validated | `artifacts/features_for_specs/*.json` → look for `validation_result` |
| Submit a new idea | `03_operations/pre_sdd/templates/seed_dossier.md` |
| Know if I can start coding | Feature record must have `validation_result: "PASS"` |
| Write a design document | `templates/design.md` |
| Write a spec | `templates/specs.md` |
| Record an architecture decision | `templates/adr.md` → `02_policies/ADR_POLICY.md` |
| Understand report format | `02_policies/REPORT_ENVELOPE_POLICY.md` |
| Check feature size limits | `02_policies/DECOMPOSITION_AND_SIZE_POLICY.md` |
| Find audit reports | `artifacts/audit_reports/` |
| See the pipeline as a diagram | `docs/SDD_PIPELINE_VISUAL.md` |
| Do my first feature | `docs/GETTING_STARTED.md` |
| Know what "seed" means | `04_project_governance/GLOSSARY.md` |
| Change the project philosophy | `04_project_governance/PROJECT_MANIFEST.md` → requires ADR |

---

## Color Code

| Icon | Meaning |
|------|---------|
| 📁 | Directory |
| 📄 | Document (human-readable) |
| ⚙️ | Configuration |
| 🔒 | Generated / do not edit manually |
| 🚀 | Entrypoint / start here |

---

## For Different Roles

### 👩‍💻 Developer
1. `docs/GETTING_STARTED.md`
2. `04_project_governance/GLOSSARY.md`
3. `artifacts/tasks/` → pick a task
4. `00_core/SDD_RUNTIME.md` → understand the gates

### 🧑‍💼 Product Manager
1. `04_project_governance/PROJECT_MANIFEST.md`
2. `03_operations/pre_sdd/PRE_SDD_CONTRACT.md`
3. `03_operations/pre_sdd/seeds/` → submit seeds

### 🤖 Agent (AI)
1. `AGENTS.md`
2. `00_core/SDD_RUNTIME.md`
3. `00_core/SDD_HANDOFF_CONTRACT.md`
4. `sdd.config.json`

### 🔍 Auditor
1. `02_policies/REPORT_ENVELOPE_POLICY.md`
2. `02_policies/INTEGRATION_SURFACE_POLICY.md`
3. Feature spec + code + tests

---

## Related Documents

- `04_project_governance/PROJECT_MAP.md` — detailed navigation with "Where Truth Lives"
- `docs/GETTING_STARTED.md` — first feature tutorial
- `docs/SDD_PIPELINE_VISUAL.md` — pipeline diagrams
