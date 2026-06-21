# SDD Bootstrap Checklist

> **Purpose:** Prevent initialization gaps when embedding SDD into an existing product repository.
> **When to use:** Before the first feature record is created, after `docs/sdd/init-sdd` runs.

---

## Canonical Install Location

- [ ] SDD is installed under `docs/sdd/`
- [ ] Product source code does not live under `docs/sdd/`
- [ ] Root-level SDD installation is not being used as the canonical model

---

## Configuration

- [ ] `docs/sdd/sdd.config.json` exists
- [ ] `project_name` is set to a meaningful value (not `Your Project Name`)
- [ ] `sdd_root` is set to `docs/sdd`
- [ ] `project_root` points to the product repository root
- [ ] `stack.languages` includes at least one language, or is intentionally empty
- [ ] `stack.frameworks` is accurate, or is intentionally empty
- [ ] `paths.artifacts.*` point to writable directories under `docs/sdd/artifacts/`
- [ ] `surfaces` declaration matches the project's actual integration surfaces
- [ ] `skills_registry` points under `docs/sdd/03_operations/skills/`

---

## Directory Structure

- [ ] `docs/sdd/00_core/` exists
- [ ] `docs/sdd/01_execution/` exists
- [ ] `docs/sdd/02_policies/` exists
- [ ] `docs/sdd/03_operations/` exists
- [ ] `docs/sdd/04_project_governance/` exists
- [ ] `docs/sdd/templates/` exists
- [ ] `docs/sdd/artifacts/features_for_specs/` exists and is writable
- [ ] `docs/sdd/artifacts/design/` exists and is writable
- [ ] `docs/sdd/artifacts/specs/` exists and is writable
- [ ] `docs/sdd/artifacts/tasks/` exists and is writable
- [ ] `docs/sdd/artifacts/audit_reports/` exists and is writable
- [ ] `docs/sdd/artifacts/adr/` exists and is writable
- [ ] `docs/sdd/03_operations/skills/` exists if using the skills registry

---

## Core Contracts

- [ ] `docs/sdd/AGENTS.md` is readable and points to the correct `docs/sdd/00_core/` location
- [ ] `docs/sdd/00_core/SDD_RUNTIME.md` exists and defines the canonical states
- [ ] `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md` exists and defines role boundaries
- [ ] `docs/sdd/00_core/SDD_READING_CONTRACT.md` exists and defines reading order
- [ ] `docs/sdd/00_core/SDD_FEATURE_FORMAT.md` exists and defines feature record format and naming

---

## Templates

- [ ] `docs/sdd/templates/design.md` exists and is adapted to the project's stack
- [ ] `docs/sdd/templates/specs.md` exists and is adapted to the project's stack
- [ ] Hardware budget sections reflect actual project constraints, or are marked optional

---

## Policies

- [ ] `docs/sdd/02_policies/REPORT_ENVELOPE_POLICY.md` exists
- [ ] `docs/sdd/02_policies/INTEGRATION_SURFACE_POLICY.md` exists
- [ ] `docs/sdd/02_policies/LEGACY_SPECS_POLICY.md` exists if the project has legacy code/docs

---

## Execution

- [ ] Role prompts exist in `docs/sdd/01_execution/prompts/` for designer, specifier, validator, planner, implementer, verifier, auditor, and archiver if that role is automated
- [ ] Prompts reference `docs/sdd/sdd.config.json` paths, not hardcoded absolute paths
- [ ] `docs/sdd/01_execution/skills/README.md` exists, even if no skills are registered yet

---

## First Feature Readiness

- [ ] A test feature record can be created under `docs/sdd/artifacts/features_for_specs/`
- [ ] A test design doc can be written using `docs/sdd/templates/design.md`
- [ ] A test spec doc can be written using `docs/sdd/templates/specs.md`
- [ ] The Validator prompt can be run against the test spec and produces a decision
- [ ] `AUDIT FAIL` is understood to block archive, final acceptance, and release/merge gates unless explicitly waived by the owner

---

## Common Gaps to Avoid

| Gap | Symptom | Fix |
|-----|---------|-----|
| Missing `docs/sdd/sdd.config.json` | Agents cannot resolve artifact paths | Copy `templates/sdd.config.json` to `docs/sdd/sdd.config.json` before feature work |
| Root install drift | SDD folders appear at project root | Reinstall under `docs/sdd/` and remove root-level SDD copy after review |
| Hardcoded paths in prompts | Agents write to wrong directories | Replace with config references or repo-relative `docs/sdd/...` paths |
| Empty Validator checklist | Validation always passes vacuously | Fill checklists in `validator.md` |
| Missing Integration Surface declaration | False PASS on surface-related bugs | Add surface section to design.md template |
| No migration config | Rewrites happen without parity checks | Set `migration.enabled` and `migration.parity_required` |
| Skills registry missing | TASKS declare skills but cannot validate | Create empty `skills_registry.json` with schema |

---

## Sign-Off

When this checklist is complete, the product repository is ready for its first SDD feature.

- [ ] Bootstrap completed by: [name/role]
- [ ] Date: [YYYY-MM-DD]
- [ ] First feature planned: [feature_id]
