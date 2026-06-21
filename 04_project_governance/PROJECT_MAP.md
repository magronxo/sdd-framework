# Project Map

> **Mode Diátaxis**: Reference

## Purpose

Provide a navigational guide for an installed SDD instance inside a product repository.

New contributors and agents should read this document before exploring the SDD area. It answers: *Where does truth live for each concern?*

---

## Canonical Repository Structure

```text
{PRODUCT_REPO_ROOT}/
├── src/                         # Product source code, if applicable
├── tests/                       # Product tests, if applicable
├── README.md                    # Product README
│
└── docs/
    └── sdd/
        ├── AGENTS.md            # Agent entrypoint
        ├── sdd.config.json      # Live SDD project configuration
        │
        ├── 00_core/             # SDD framework core
        │   ├── SDD_RUNTIME.md
        │   ├── SDD_GUIDE.md
        │   ├── SDD_READING_CONTRACT.md
        │   └── SDD_HANDOFF_CONTRACT.md
        │
        ├── 01_execution/        # Role definitions, prompts, and skills
        │   ├── prompts/
        │   └── skills/
        │
        ├── 02_policies/         # Governance policies
        │   ├── REPORT_ENVELOPE_POLICY.md
        │   ├── INTEGRATION_SURFACE_POLICY.md
        │   └── ...
        │
        ├── 03_operations/       # Operational workflows
        │   ├── pre_sdd/
        │   │   ├── seeds/
        │   │   ├── seeds/deferred/
        │   │   ├── seeds/rejected/
        │   │   ├── seeds/promoted/
        │   │   ├── seeds/merged/
        │   │   ├── templates/
        │   │   ├── PRE_SDD_CONTRACT.md
        │   │   └── PRE_SDD_RUNTIME.md
        │   └── ...
        │
        ├── 04_project_governance/
        │   ├── PROJECT_MANIFEST.md
        │   ├── GLOSSARY.md
        │   └── PROJECT_MAP.md
        │
        ├── templates/           # Reusable document templates
        │   ├── design.md
        │   ├── specs.md
        │   ├── adr.md
        │   ├── migration_plan.md
        │   └── ...
        │
        ├── docs/                # Human SDD guides and tutorials
        │   ├── GETTING_STARTED.md
        │   ├── SDD_PIPELINE_VISUAL.md
        │   └── PROJECT_TOUR.md
        │
        └── artifacts/           # Generated SDD deliverables
            ├── features_for_specs/
            ├── design/
            ├── specs/
            ├── tasks/
            ├── audit_reports/
            └── adr/
```

---

## Where Truth Lives

| Concern | Source of Truth | Path |
|---------|----------------|------|
| Execution contract | `SDD_RUNTIME.md` | `docs/sdd/00_core/SDD_RUNTIME.md` |
| Full methodology | `SDD_GUIDE.md` | `docs/sdd/00_core/SDD_GUIDE.md` |
| Agent behavior | `AGENTS.md` | `docs/sdd/AGENTS.md` |
| Project SDD configuration | `sdd.config.json` | `docs/sdd/sdd.config.json` |
| Project philosophy | `PROJECT_MANIFEST.md` | `docs/sdd/04_project_governance/PROJECT_MANIFEST.md` |
| Terminology | `GLOSSARY.md` | `docs/sdd/04_project_governance/GLOSSARY.md` |
| Feature state | feature record JSON | `docs/sdd/artifacts/features_for_specs/` |
| Design documents | design markdown | `docs/sdd/artifacts/design/` |
| Validated specs | spec markdown | `docs/sdd/artifacts/specs/` |
| Task breakdowns | task markdown | `docs/sdd/artifacts/tasks/` |
| Audit reports | audit markdown | `docs/sdd/artifacts/audit_reports/` |
| Policies | policy markdown | `docs/sdd/02_policies/` |
| Workflows | operation docs | `docs/sdd/03_operations/` |
| Templates | reusable templates | `docs/sdd/templates/` |
| Architecture decisions | ADR markdown | `docs/sdd/artifacts/adr/` |
| Agent decision rules | decision table | `docs/sdd/00_core/AGENT_DECISION_TABLE.md` |
| Human SDD guides | guide markdown | `docs/sdd/docs/` |
| Migration playbook | migration workflow | `docs/sdd/03_operations/MIGRATION_PLAYBOOK.md` |
| Roadmap planning | roadmap template | `docs/sdd/03_operations/ROADMAP_TEMPLATE.md` |
| Skills reference | skills docs | `docs/sdd/01_execution/skills/` |

---

## Navigation by Role

### I am a new developer

1. Read `docs/sdd/04_project_governance/PROJECT_MANIFEST.md`.
2. Read `docs/sdd/04_project_governance/GLOSSARY.md`.
3. Read `docs/sdd/docs/PROJECT_TOUR.md` if present.
4. Read `docs/sdd/docs/GETTING_STARTED.md` if present.
5. Read `docs/sdd/00_core/SDD_GUIDE.md`.
6. Read `docs/sdd/AGENTS.md`.
7. Pick up a task from `docs/sdd/artifacts/tasks/` only after validation has passed.

### I am a product manager

1. Read `docs/sdd/04_project_governance/PROJECT_MANIFEST.md`.
2. Read `docs/sdd/03_operations/pre_sdd/PRE_SDD_CONTRACT.md`.
3. Submit seeds to `docs/sdd/03_operations/pre_sdd/seeds/`.

### I am an agent (AI)

1. Read `docs/sdd/AGENTS.md`.
2. Read `docs/sdd/00_core/SDD_RUNTIME.md`.
3. Read `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`.
4. Read `docs/sdd/sdd.config.json`.
5. Follow the canonical pipeline.

### I am an auditor

1. Read `docs/sdd/02_policies/REPORT_ENVELOPE_POLICY.md`.
2. Read `docs/sdd/02_policies/INTEGRATION_SURFACE_POLICY.md`.
3. Read the feature spec + code + verification evidence.
4. Produce a report per envelope rules.
5. Remember that `AUDIT FAIL` blocks archive/final acceptance/release gates unless explicitly waived by the owner.

---

## Related Documents

- `docs/sdd/04_project_governance/PROJECT_MANIFEST.md` — project identity
- `docs/sdd/04_project_governance/GLOSSARY.md` — terminology
- `docs/sdd/sdd.config.json` — machine-readable paths and stack

---

## Examples

`examples/` content is educational only and never framework authority.
