# SDD Bootstrap Checklist

> **Purpose:** Prevent initialization gaps when embedding SDD into an existing project.
> **When to use:** Before the first feature record is created, after `init-sdd` runs.

---

## Pre-Flight Checks

### Configuration
- [ ] `sdd.config.json` exists at project root or `docs/sdd/`
- [ ] `project_name` is set to a meaningful value (not "Your Project Name")
- [ ] `stack.languages` includes at least one language
- [ ] `stack.frameworks` is accurate (empty array if none)
- [ ] `paths.artifacts.*` point to existing writable directories
- [ ] `surfaces` declaration matches the project's actual integration surfaces

### Directory Structure
- [ ] `artifacts/design/` exists and is writable
- [ ] `artifacts/specs/` exists and is writable
- [ ] `artifacts/tasks/` exists and is writable
- [ ] `artifacts/audit_reports/` exists and is writable
- [ ] `artifacts/features_for_specs/` exists and is writable
- [ ] `03_operations/skills/` exists (if using skills registry)

### Core Contracts
- [ ] `AGENTS.md` is readable and points to correct `00_core/` location
- [ ] `00_core/SDD_RUNTIME.md` exists and defines the 8 states
- [ ] `00_core/SDD_HANDOFF_CONTRACT.md` exists and defines role boundaries
- [ ] `00_core/SDD_READING_CONTRACT.md` exists and defines reading order
- [ ] `00_core/SDD_FEATURE_FORMAT.md` exists and defines JSON schema

### Templates
- [ ] `templates/design.md` exists and is adapted to project's stack
- [ ] `templates/specs.md` exists and is adapted to project's stack
- [ ] Hardware budget sections reflect actual project constraints (or are marked optional)

### Policies
- [ ] `02_policies/REPORT_ENVELOPE_POLICY.md` exists
- [ ] `02_policies/INTEGRATION_SURFACE_POLICY.md` exists
- [ ] `02_policies/LEGACY_SPECS_POLICY.md` exists (if project has legacy code/docs)

### Execution
- [ ] All 6 role prompts exist in `01_execution/prompts/`
- [ ] Prompts reference `sdd.config.json` paths, not hardcoded absolute paths
- [ ] `01_execution/skills/README.md` exists (even if no skills registered yet)

### First Feature Readiness
- [ ] A test feature record can be created manually
- [ ] A test design doc can be written using `templates/design.md`
- [ ] A test spec doc can be written using `templates/specs.md`
- [ ] The Validator prompt can be run against the test spec and produces a decision

---

## Common Gaps to Avoid

| Gap | Symptom | Fix |
|-----|---------|-----|
| Missing `sdd.config.json` | Agents cannot resolve artifact paths | Create config before any feature work |
| Hardcoded paths in prompts | Agents write to wrong directories | Replace with `{{SDD_ROOT}}` or config references |
| Empty Validator checklist | Validation always passes vacuously | Fill checklists in `validator.md` |
| Missing Integration Surface declaration | False PASS on surface-related bugs | Add surface section to design.md template |
| No migration config | Rewrites happen without parity checks | Set `migration.enabled` and `migration.parity_required` |
| Skills registry missing | TASKS declare skills but cannot validate | Create empty `skills_registry.json` with schema |

---

## Sign-Off

When this checklist is complete, the project is ready for its first SDD feature.

- [ ] Bootstrap completed by: [name/role]
- [ ] Date: [YYYY-MM-DD]
- [ ] First feature planned: [feature_id]
