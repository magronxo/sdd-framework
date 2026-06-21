# sdd-framework

![Status](https://img.shields.io/badge/status-0.1.0--beta-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
![Mode](https://img.shields.io/badge/mode-agent--first-purple)
![Governance](https://img.shields.io/badge/governance-human--approved-lightgrey)

**Agent-first Spec-Driven Development for human-governed AI engineering.**

> No spec = no implementation.

`sdd-framework` is a contract-based SDD framework for human–AI collaborative engineering. Humans capture intent and approve checkpoints. AI agents execute the development pipeline through explicit roles, artifacts, and validation gates.

---

## At a glance

| Area | Description |
|---|---|
| Core rule | No implementation without a validated spec |
| Default executor | AI agents |
| Governance model | Human approval at explicit gates |
| Pipeline | SEED → DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE |
| Main artifact | Feature record with phase state, ownership, and validation result |
| Install model | Embedded in product repositories under `docs/sdd/` |
| Best for | Human–AI collaborative software engineering |

---

## Why this exists

Most SDD, BDD, and RFC-style workflows are human-first: humans write the specification, humans validate it, and humans decide when implementation is safe.

`sdd-framework` is agent-first:

1. A human captures a seed: an intent, bug, idea, or requested change.
2. AI agents advance that seed through a governed pipeline.
3. Humans approve explicit checkpoints.
4. Implementation is blocked until the spec has passed validation.

The framework provides contracts, prompts, artifact formats, and gates so agents stay scoped, auditable, and aligned with the approved specification.

---

## Canonical installation model

SDD is installed as a self-contained governance and documentation system inside a product repository:

```text
repo/
  src/
  tests/
  README.md
  docs/
    sdd/
      AGENTS.md
      sdd.config.json
      00_core/
      01_execution/
      02_policies/
      03_operations/
      04_project_governance/
      templates/
      artifacts/
```

Rules:

- Product code stays outside `docs/sdd/`.
- SDD contracts, prompts, templates, configuration, and generated SDD artifacts live under `docs/sdd/`.
- `docs/sdd/sdd.config.json` is the live project SDD configuration.
- `templates/sdd.config.json` in this framework repository is a template, not a live product config.
- Root-level SDD installation is not the canonical model.

---

## Pipeline

```mermaid
flowchart LR
    A[SEED] --> B[DESIGN]
    B --> C[SPEC]
    C --> D[VALIDATION]
    D -->|validation_result: PASS| E[TASKS]
    D -->|FAIL / BLOCKED| C
    E --> F[IMPLEMENT]
    F --> G[VERIFY]
    G --> H[AUDIT]
    H --> I[ARCHIVE]

    U[Human] -. captures intent .-> A
    U -. approves design .-> B
    U -. reviews validation .-> D
    U -. reviews audit .-> H
```

> Hard rule: implementation is blocked unless the active feature record contains `validation_result: PASS`.

---

## Core idea

A feature starts as a lightweight human seed and becomes an auditable implementation through bounded agent roles.

```mermaid
sequenceDiagram
    participant H as Human
    participant D as Designer Agent
    participant S as Specifier Agent
    participant V as Validator Agent
    participant P as Planner Agent
    participant I as Implementer Agent
    participant Q as Verifier Agent
    participant A as Auditor Agent

    H->>D: Capture intent
    D->>H: Ask clarifying questions
    D->>S: Approved design
    S->>V: Specification
    V->>H: Validation result
    H->>P: Approve if PASS
    P->>I: Ordered tasks
    I->>Q: Code + tests
    Q->>A: Audit report
```

The human remains the governing authority. Agents are bounded executors.

---

## What you get

- **Role contracts** for designer, specifier, validator, planner, implementer, verifier, auditor, and archiver agents.
- **Validation gates** that block implementation until the spec is complete, deterministic, and implementable.
- **Traceable artifacts** for every phase of the feature lifecycle.
- **Handoff rules** that prevent role mixing and hidden state.
- **Prompt contracts** designed for agentic execution rather than manual ceremony.

---

## Who is this for?

| Role | How you use it |
|---|---|
| Solo developer | Use AI agents as disciplined pair programmers that cannot skip specs or drift into implementation. |
| Tech lead | Enforce validated specs before code reaches implementation. |
| Product manager | Capture seeds, triage ideas, and feed a governed engineering pipeline. |
| AI engineer | Provide autonomous agents with explicit roles, contracts, and validation gates. |
| Domain expert | Describe what you need; agents produce specs and implementation artifacts for human approval. |

---

## Canonical phases

| Phase | Owner | Purpose |
|---|---|---|
| SEED | Human | Capture intent, bug, idea, or requested change. |
| DESIGN | Designer Agent | Define goals, constraints, non-goals, and expected outcome. |
| SPEC | Specifier Agent | Define expected behavior, interfaces, errors, acceptance criteria, and scenario-driven tests (SDT). |
| VALIDATION | Validator Agent | Gate the spec for completeness, determinism, and implementability. |
| TASKS | Planner Agent | Break the validated spec into minimal ordered tasks. |
| IMPLEMENT | Implementer Agent | Execute tasks and write tests where applicable. |
| VERIFY | Verifier Agent | Run tests and SDT scenarios. Report PASS/FAIL with evidence. |
| AUDIT | Auditor Agent | Review spec-code alignment, risks, quality, and traceability. |
| ARCHIVE | Human / Archiver | Close the feature and preserve artifacts. |

---

## Quick start

### 1. Clone the framework

```bash
git clone https://github.com/magronxo/sdd-framework.git
cd sdd-framework
```

### 2. Copy the framework into your product repository

From the framework checkout:

```bash
mkdir -p /your/project/docs/sdd
cp -r 00_core 01_execution 02_policies 03_operations 04_project_governance templates docs AGENTS.md init-sdd.sh init-sdd.ps1 /your/project/docs/sdd/
cp templates/sdd.config.json /your/project/docs/sdd/sdd.config.json
```

The canonical installed location is:

```text
/your/project/docs/sdd/
```

### 3. Initialize artifact directories

From the product repository root:

```bash
bash docs/sdd/init-sdd.sh
```

On Windows PowerShell, from the product repository root:

```powershell
.\docs\sdd\init-sdd.ps1
```

### 4. Configure your project

Edit:

```text
docs/sdd/sdd.config.json
```

Set your project name, stack, test conventions, artifact directories, surfaces, and skill registry path.

### 5. Capture a seed

Create a seed from the seed template:

```text
docs/sdd/03_operations/pre_sdd/seeds/YYYY-MM-DD_idea_name.md
```

A seed can describe:

- a feature idea
- a bug
- a refactor
- an integration need
- a migration
- an operational change

### 6. Start the agent workflow

Point your AI agent to:

```text
docs/sdd/AGENTS.md
docs/sdd/00_core/SDD_RUNTIME.md
docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md
docs/sdd/00_core/SDD_READING_CONTRACT.md
docs/sdd/sdd.config.json
```

The agent should read the seed, ask clarifying questions, create or update the active feature record, and advance through the pipeline according to its assigned role.

---

## Agent entrypoint

If you are an AI agent reading an installed SDD instance:

1. Read `docs/sdd/AGENTS.md`.
2. Read `docs/sdd/00_core/SDD_RUNTIME.md`.
3. Read `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`.
4. Read `docs/sdd/00_core/SDD_READING_CONTRACT.md`.
5. Read `docs/sdd/sdd.config.json`.
6. Read the active feature record from `docs/sdd/artifacts/features_for_specs/`.
7. Operate only in your assigned role.
8. Stop if ambiguity exists. Report it. Do not guess.

---

## Installed project structure

| Path | Purpose |
|---|---|
| `docs/sdd/00_core/` | Runtime contracts, handoff rules, feature format, reading order. |
| `docs/sdd/01_execution/prompts/` | Agent role prompts for designer, specifier, validator, planner, implementer, verifier, auditor, and archiver. |
| `docs/sdd/01_execution/skills/` | Reusable agent skills. Empty by default; add your own. |
| `docs/sdd/02_policies/` | Governance rules, report envelopes, validation boundaries, and integration surfaces. |
| `docs/sdd/03_operations/` | Operational workflows, pre-SDD intake, re-audit flow, and audit strategy. |
| `docs/sdd/04_project_governance/` | Project identity, glossary, manifest, and project map. |
| `docs/sdd/templates/` | Templates for design docs, specs, ADRs, migration plans, and related artifacts. |
| `docs/sdd/docs/` | Human-facing SDD guides and project documentation. |
| `docs/sdd/artifacts/` | Generated SDD work: feature records, designs, specs, tasks, reports, ADRs, and audits. |
| `docs/sdd/sdd.config.json` | Live project SDD configuration. |
| `docs/sdd/AGENTS.md` | Main agent entrypoint and execution contract. |

---

## Key principles

| Principle | Meaning |
|---|---|
| Agent-first | The default executor is an AI agent, not a human. |
| Human-governed | Humans capture intent, approve gates, and review outcomes. |
| Specs are authority | Behavior must be backed by a validated spec. |
| No role mixing | Designer ≠ Specifier ≠ Implementer. Agents stay in lane. |
| Validation gate | `validation_result: PASS` is required before implementation. |
| Evidence-first | Verification and audit require execution evidence, not assumptions. |
| Minimal context | Agents use the smallest context needed for the current phase. |
| Deterministic handoffs | Each phase produces explicit artifacts; no hidden state. |

---

## Audit gate rule

`AUDIT FAIL` does not stop corrective work. It blocks archival, final acceptance, and release/merge gates unless explicitly waived by the project owner.

That means agents may continue rework, investigation, or corrective implementation, but they must not mark the feature as complete or archive it while unresolved audit failures remain.

---

## Comparison

| Framework | Human effort | Agent effort | Governance model | Best for |
|---|---:|---:|---|---|
| BDD / Cucumber | High | Low | Team-defined | Human teams with strong test discipline |
| MetaGPT / CrewAI | Low | High | Agent-driven | Rapid prototyping and autonomous workflows |
| Rust RFC / PEP | High | None | Committee / maintainer-governed | Language and platform evolution |
| `sdd-framework` | Medium | High | Contract-based, human-approved | Human–AI collaborative engineering |

---

## Example usage

Examples are educational only. They are not framework authority.

Use examples to understand possible artifact chains and project shapes, but resolve contradictions by following:

1. `docs/sdd/00_core/`
2. `docs/sdd/01_execution/`
3. `docs/sdd/02_policies/`
4. `docs/sdd/templates/`
5. `docs/sdd/sdd.config.json`

---

## Customization

### Adapting prompts

The prompts in `docs/sdd/01_execution/prompts/` are agent role contracts. Customize them for:

- your programming language
- your framework
- your test conventions
- your review process
- your organizational constraints

Keep the core structure, phase boundaries, and handoff rules intact.

### Adding skills

Skills are reusable agent capabilities.

Create:

```text
docs/sdd/01_execution/skills/SKILL_NAME.md
```

A skill should define:

- type
- trigger
- inputs
- outputs
- scope
- failure mode

Register the skill in the configured skill registry path from `docs/sdd/sdd.config.json`.

See:

```text
docs/sdd/01_execution/skills/README.md
```

---

## Non-goals

`sdd-framework` is not:

- a general-purpose agent framework
- a replacement for human engineering judgment
- a project management tool
- a guarantee that LLM output is correct
- a fully autonomous software factory

It is a governance and execution framework for keeping AI-assisted development scoped, validated, and auditable.

---

## Contributing

This is an early framework. Feedback is valuable, especially around:

- validation reports from real projects
- prompt adaptations for different stacks
- friction points encountered by agents
- new skills or role contracts
- use cases outside software engineering

See `CONTRIBUTING.md` for details.

---

## Status

Current version: `0.1.0-beta`

The framework is usable, but still early. Expect changes in:

- prompt contracts
- artifact schemas
- skill registration
- examples
- project initialization flow

---

## License

Licensed under the Apache License, Version 2.0.

See `LICENSE` for the full text.

Copyright © 2026 Oriol Coll.
