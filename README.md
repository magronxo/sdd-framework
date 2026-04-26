# sdd-framework — Spec-Driven Development Framework

A generic, minimal Spec-Driven Development (SDD) framework for any software project.

> **No spec = no implementation.**

---

## What is SDD?

Spec-Driven Development is a methodology where:
- **Specs are the only source of truth** for product behavior
- **No implementation** happens without a validated spec
- **Roles are strictly separated**: Designer, Specifier, Validator, Planner, Implementer, Verifier, Auditor, Archiver
- Every feature flows through a canonical pipeline with explicit state transitions

---

## Canonical Pipeline

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE
```

1. **DESIGN**: define WHAT to implement
2. **SPEC**: define HOW, with inputs/outputs/errors and SDT scenarios
3. **VALIDATION**: verify the spec is complete and deterministic
4. **TASKS**: break down into minimal, ordered tasks
5. **IMPLEMENT**: execute tasks with TDD (or project-specific methodology)
6. **VERIFY**: run tests against spec and SDT scenarios
7. **AUDIT**: review spec-code consistency, quality, and risks
8. **ARCHIVE**: close the feature and consolidate documentation

---

## Quick Start

### 1. Copy the framework into your project

Copy these folders/files into your project root:

```
sdd-framework/
├── 00_core/          # Core contracts (runtime, handoff, guide)
├── 01_execution/     # Role prompts + skills system
├── 02_policies/      # Governance policies
├── 03_operations/    # Operational workflows
├── templates/        # Design and spec templates
├── sdd.config.json   # Project configuration
└── AGENTS.md         # Agent entrypoint contract
```

### 2. Configure your project

Edit `sdd.config.json`:

```json
{
  "project_name": "My Awesome Project",
  "project_description": "A system that does amazing things",
  "sdd_root": ".",
  "paths": { ... },
  "stack": {
    "languages": ["Go", "TypeScript"],
    "frameworks": ["React", "Gin"],
    "hardware": null
  },
  "surfaces": ["browser", "os_fs", "wiring", "network"]
}
```

### 3. Initialize artifact directories

Run the init script for your platform:

```bash
# PowerShell (Windows)
.\init-sdd.ps1

# Bash (Linux/macOS)
./init-sdd.sh
```

Or create them manually:
```bash
mkdir -p artifacts/{design,specs,tasks,audit_reports,features_for_specs}
```

### 4. Start your first feature

1. Create a feature record: `artifacts/features_for_specs/feat-001-my-feature.json`
2. Write a design doc: `artifacts/design/feat-001-my-feature.md`
3. Follow the pipeline — see `00_core/SDD_RUNTIME.md`

---

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `00_core/` | **Source of truth**: runtime contract, handoff rules, feature format, decision table |
| `01_execution/prompts/` | Role prompts: designer, specifier, validator, planner, implementer, verifier |
| `01_execution/skills/` | Skills system (empty by default — add your own) |
| `02_policies/` | Governance: report envelopes, integration surfaces, legacy specs, skills taxonomy |
| `03_operations/` | Workflows: operational flow, re-audit strategy, audit strategy |
| `templates/` | Document templates for design and spec |
| `artifacts/` | Feature deliverables: design docs, specs, tasks, audit reports, feature records |
| `sdd.config.json` | Project configuration: paths, stack, surfaces |

---

## Key Principles

- **Specs are authority**: No behavior exists without a spec
- **No role mixing**: A Designer does not write specs; an Implementer does not redesign
- **Validation gate**: `validation_result: PASS` must be recorded before TASKS or IMPLEMENT
- **Evidence-first**: Verification and audit require execution evidence, never assumptions
- **Minimal context**: Agents operate on the smallest context needed for the current phase

---

## Example

See `examples/agenticos/` for a **real-world example** of this framework in use. It contains:
- 70+ completed features with design, spec, tasks, and audit reports
- Historical evolution of the framework
- Demonstration of all pipeline phases

---

## Customization

### Adding Skills

1. Create a skill file in `01_execution/skills/<skill-name>.md`
2. Define: type, trigger, inputs, outputs, scope, context_dependency, failure_mode
3. Register it in your skills registry (path set in `sdd.config.json`)

See `01_execution/skills/README.md` for the minimum skill contract.

### Adapting Prompts

The prompts in `01_execution/prompts/` are templates. Customize them for your:
- Stack (languages, frameworks)
- Testing conventions
- Organizational roles

Keep the core structure and handoff contracts intact.

---

## Files for Agents

When an agent starts working, it must read in this order:

1. `AGENTS.md`
2. `00_core/SDD_RUNTIME.md`
3. `00_core/SDD_READING_CONTRACT.md`
4. Feature-local artifacts (as needed)

See `00_core/SDD_READING_CONTRACT.md` for the full reading contract.

---

## Contributing

This is a framework template. Fork it, adapt it, and evolve it for your project's needs.

---

**Version:** 0.1.0-beta
**License:** Apache-2.0

---

## License

Copyright 2026 Oriol Coll

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
