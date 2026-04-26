# Project Map

> **Mode Diátaxis**: Reference

## Purpose

Provide a **navigational guide** for the repository.

New contributors should read this document before exploring the codebase. It answers: *Where does truth live for each concern?*

---

## Repository Structure

```
{PROJECT_ROOT}/
├── 00_core/                    # SDD framework core
│   ├── SDD_RUNTIME.md          # Execution contract (agents)
│   ├── SDD_GUIDE.md            # Full methodology (humans)
│   ├── SDD_READING_CONTRACT.md # Minimal reading contract
│   └── SDD_HANDOFF_CONTRACT.md # Handoff rules between agents
│
├── 01_execution/               # Role definitions and prompts
│   ├── prompts/                # Agent role prompts
│   └── ...
│
├── 02_policies/                # Governance policies
│   ├── REPORT_ENVELOPE.md
│   ├── INTEGRATION_SURFACES.md
│   └── ...
│
├── 03_operations/              # Operational workflows
│   ├── WORKFLOW.md
│   ├── pre_sdd/                # Pre-SDD capture and triage
│   │   ├── seeds/              # Active seeds (awaiting triage)
│   │   ├── seeds/deferred/     # Postponed seeds
│   │   ├── seeds/rejected/     # Rejected seeds
│   │   ├── seeds/promoted/     # Seeds promoted to features
│   │   ├── seeds/merged/       # Consolidated seeds
│   │   ├── templates/
│   │   │   ├── seed_dossier.md
│   │   │   └── triage_batch.md
│   │   ├── PRE_SDD_CONTRACT.md
│   │   └── PRE_SDD_RUNTIME.md
│   └── ...
│
├── 04_project_governance/      # Project-specific governance
│   ├── PROJECT_MANIFEST.md     # Identity and philosophy
│   ├── GLOSSARY.md             # Terminology
│   └── PROJECT_MAP.md          # This file
│
├── templates/                  # Reusable document templates
│   ├── design.md
│   ├── specs.md
│   ├── adr.md
│   ├── migration_plan.md
│   └── ...
│
├── docs/                         # Human guides and tutorials
│   ├── GETTING_STARTED.md        # First feature tutorial
│   ├── SDD_PIPELINE_VISUAL.md    # Diagrams and flowcharts
│   └── PROJECT_TOUR.md           # Visual repository tour
│
├── artifacts/                  # Working deliverables (generated)
│   ├── features_for_specs/     # Feature records (JSON)
│   ├── design/                 # Design documents
│   ├── specs/                  # Validated specifications
│   ├── tasks/                  # Task breakdowns
│   └── audit_reports/          # Audit outputs
│
├── ROADMAP.md                  # Framework roadmap
├── sdd.config.json             # Project configuration
└── AGENTS.md                   # Agent entrypoint
```

---

## Where Truth Lives

| Concern | Source of Truth | Path |
|---------|----------------|------|
| **Execution contract** | `00_core/SDD_RUNTIME.md` | `00_core/SDD_RUNTIME.md` |
| **Full methodology** | `00_core/SDD_GUIDE.md` | `00_core/SDD_GUIDE.md` |
| **Agent behavior** | `AGENTS.md` | `AGENTS.md` |
| **Project configuration** | `sdd.config.json` | `sdd.config.json` |
| **Project philosophy** | `04_project_governance/PROJECT_MANIFEST.md` | `04_project_governance/PROJECT_MANIFEST.md` |
| **Terminology** | `04_project_governance/GLOSSARY.md` | `04_project_governance/GLOSSARY.md` |
| **Feature state** | `artifacts/features_for_specs/*.json` | `artifacts/features_for_specs/` |
| **Design documents** | `artifacts/design/*.md` | `artifacts/design/` |
| **Validated specs** | `artifacts/specs/*.md` | `artifacts/specs/` |
| **Task breakdowns** | `artifacts/tasks/*.md` | `artifacts/tasks/` |
| **Audit reports** | `artifacts/audit_reports/*.md` | `artifacts/audit_reports/` |
| **Policies** | `02_policies/*.md` | `02_policies/` |
| **Workflows** | `03_operations/*.md` | `03_operations/` |
| **Templates** | `templates/*.md` | `templates/` |
| **Architecture decisions** | `artifacts/adr/*.md` (or as configured) | `{adr_path}` |
| **Agent decision rules** | `00_core/AGENT_DECISION_TABLE.md` | `00_core/AGENT_DECISION_TABLE.md` |
| **Human guides** | `docs/*.md` | `docs/` |
| **Framework roadmap** | `ROADMAP.md` | `ROADMAP.md` |
| **Migration playbook** | `03_operations/MIGRATION_PLAYBOOK.md` | `03_operations/MIGRATION_PLAYBOOK.md` |
| **Roadmap planning** | `03_operations/ROADMAP_TEMPLATE.md` | `03_operations/ROADMAP_TEMPLATE.md` |
| **Skills reference** | `01_execution/skills/*.md` | `01_execution/skills/` |

---

## Navigation by Role

### I am a new developer
1. Read `04_project_governance/PROJECT_MANIFEST.md`
2. Read `04_project_governance/GLOSSARY.md`
3. Read `docs/PROJECT_TOUR.md`
4. Read `docs/GETTING_STARTED.md` (follow the tutorial)
5. Read `00_core/SDD_GUIDE.md`
6. Read `AGENTS.md`
7. Pick up a task from `artifacts/tasks/`

### I am a product manager
1. Read `04_project_governance/PROJECT_MANIFEST.md`
2. Read `03_operations/pre_sdd/PRE_SDD_CONTRACT.md`
3. Submit seeds to `03_operations/pre_sdd/`

### I am an agent (AI)
1. Read `AGENTS.md`
2. Read `00_core/SDD_RUNTIME.md`
3. Read `00_core/SDD_HANDOFF_CONTRACT.md`
4. Read `sdd.config.json`
5. Follow the canonical pipeline

### I am an auditor
1. Read `02_policies/REPORT_ENVELOPE.md`
2. Read `02_policies/INTEGRATION_SURFACES.md`
3. Read the feature spec + code
4. Produce report per envelope rules

---

## Related Documents

- `04_project_governance/PROJECT_MANIFEST.md` — project identity
- `04_project_governance/GLOSSARY.md` — terminology
- `sdd.config.json` — machine-readable paths and stack
