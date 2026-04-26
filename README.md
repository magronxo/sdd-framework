# sdd-framework — Agent-First Spec-Driven Development

> **No spec = no implementation.**
>
> **Built for AI agents. Governed by humans.**

A spec-driven development framework designed for **human-AI collaborative engineering**. The human captures intent; AI agents execute the pipeline.

---

## What Makes This Different?

Most SDD/BDD frameworks are **human-first**: you write specs, you validate, you implement.

This framework is **agent-first**:
- You capture a **seed** (intent, bug, idea)
- **AI agents** advance it through DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT
- You **govern** at checkpoints: approve designs, validate specs, review audits
- You never write a spec manually unless you want to

The framework provides the **contracts, prompts, and gates** so agents operate deterministically and don't drift.

---

## The Core Idea

```
HUMAN: "I need a health check endpoint"
    ↓
AGENT (Designer): "What should it do? Constraints?"
    ↓
HUMAN: "Lightweight, <100ms, returns JSON status"
    ↓
AGENT (Specifier): writes detailed spec with errors, SDT scenarios
    ↓
AGENT (Validator): checks completeness, determinism, implementability
    ↓
HUMAN: [reviews validation result] ✅
    ↓
AGENT (Planner): breaks into tasks
    ↓
AGENT (Implementer): writes code + tests
    ↓
AGENT (Verifier): runs tests, reports PASS/FAIL
    ↓
AGENT (Auditor): reviews spec-code alignment
    ↓
HUMAN: [reviews audit] ✅ → ARCHIVE
```

The human is the **sovereign**. Agents are the **executors**.

---

## Who Is This For?

| Role | How you use it |
|------|----------------|
| **Solo developer** | AI pair programmer that follows discipline: no skipping specs, no drift |
| **Tech lead** | Governance layer: enforce that features have validated specs before code |
| **Product manager** | Pre-SDD intake: capture seeds, triage, prioritize, feed the pipeline |
| **AI engineer** | Structured environment for autonomous agents with explicit contracts |
| **Non-coder** | Describe what you need; agents spec and build it; you approve checkpoints |

---

## Canonical Pipeline

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE
```

| Phase | Who | What happens |
|-------|-----|--------------|
| **DESIGN** | Agent (Designer) | Define WHAT. Constraints, goals, non-goals. |
| **SPEC** | Agent (Specifier) | Define HOW. Interfaces, errors, SDT scenarios. |
| **VALIDATION** | Agent (Validator) | Gate: spec complete? deterministic? implementable? |
| **TASKS** | Agent (Planner) | Break spec into ordered, minimal tasks. |
| **IMPLEMENT** | Agent (Implementer) | Execute tasks. TDD when applicable. |
| **VERIFY** | Agent (Verifier) | Run tests + SDT scenarios. PASS/FAIL. |
| **AUDIT** | Agent (Auditor) | Review spec-code consistency, risks, quality. |
| **ARCHIVE** | Human (Archiver) | Close feature. Preserve artifacts for traceability. |

**Hard rule**: No implementation without `validation_result: PASS`.

---

## Quick Start (Human Edition)

### 1. Bootstrap the framework

```bash
git clone https://github.com/magronxo/sdd-framework.git
cd sdd-framework

# Copy framework into your project
cp -r 00_core 01_execution 02_policies 03_operations templates sdd.config.json AGENTS.md /your/project/

# Initialize artifact directories
./init-sdd.sh  # or .\init-sdd.ps1 on Windows
```

### 2. Configure

Edit `sdd.config.json` for your project stack and paths.

### 3. Capture a seed

Create `03_operations/pre_sdd/seeds/2026-04-23_idea_health_check.md` using the seed template.

### 4. Let the agents work

Point your AI agent to `AGENTS.md` → `00_core/SDD_RUNTIME.md` → `00_core/SDD_HANDOFF_CONTRACT.md`.

The agent will read the seed, ask clarifying questions, and advance through the pipeline.

**You intervene at gates**: approve the design, validate the spec, review the audit.

---

## Quick Start (Agent Edition)

If you are an AI agent reading this:

1. Read `AGENTS.md` (entrypoint contract)
2. Read `00_core/SDD_RUNTIME.md` (execution contract)
3. Read `00_core/SDD_HANDOFF_CONTRACT.md` (role boundaries)
4. Read `sdd.config.json` (project paths and configuration)
5. Read the active feature record from `artifacts/features_for_specs/`
6. Operate in your assigned role only
7. STOP if ambiguity exists. Report it. Do not guess.

See `00_core/SDD_READING_CONTRACT.md` for the full reading order.

---

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `00_core/` | **Contracts**: runtime, handoffs, feature format, reading order |
| `01_execution/prompts/` | **Agent brains**: role prompts for designer, specifier, validator, planner, implementer, verifier, auditor |
| `01_execution/skills/` | **Capabilities**: reusable agent skills (empty by default — add your own) |
| `02_policies/` | **Governance**: report envelopes, integration surfaces, legacy specs, validation boundaries |
| `03_operations/` | **Workflows**: operational flow, re-audit, audit strategy, pre-SDD intake |
| `04_project_governance/` | **Project identity**: manifest, glossary, project map |
| `templates/` | **Document templates**: design, spec, ADR, migration plan |
| `docs/` | **Human guides**: getting started, visual pipeline, project tour |
| `artifacts/` | **Generated work**: feature records, designs, specs, tasks, audit reports |
| `sdd.config.json` | **Configuration**: paths, stack, surfaces, migration settings |

---

## Key Principles

- **Agent-first**: The default executor is an AI agent, not a human
- **Human-governed**: Humans capture intent, approve gates, and audit outcomes
- **Specs are authority**: No behavior exists without a validated spec
- **No role mixing**: Designer ≠ Specifier ≠ Implementer. Agents stay in lane.
- **Validation gate**: `validation_result: PASS` recorded before any implementation
- **Evidence-first**: Verification and audit require execution evidence, never assumptions
- **Minimal context**: Agents operate on the smallest context needed for the current phase
- **Deterministic handoffs**: Each phase produces exactly one artifact; no hidden state

---

## Comparison

| Framework | Human effort | Agent effort | Governance | Best for |
|-----------|-----------|-------------|------------|----------|
| **BDD / Cucumber** | High (write Gherkin, implement tests) | Low (run tests) | None | Human teams with test discipline |
| **MetaGPT / CrewAI** | Low (describe goal) | High (agents decide everything) | Weak | Rapid prototyping |
| **Rust RFC / PEP** | High (write proposal, discuss, implement) | None | Strong (core team) | Language standards |
| **This SDD** | Medium (capture intent, approve gates) | High (agents execute pipeline) | Strong (explicit contracts) | **Human-AI collaborative engineering** |

---

## Example: Real-World Usage

See `examples/agenticos/` for a **production example** of this framework in use. It contains:
- 70+ completed features with full artifact chains
- Historical evolution of the framework
- Demonstration of all pipeline phases
- Pre-SDD intake and triage batches

---

## Customization

### Adapting Prompts

The prompts in `01_execution/prompts/` are **agent role contracts**. Customize them for:
- Your stack (languages, frameworks)
- Your testing conventions
- Your organizational constraints

Keep the core structure and handoff rules intact.

### Adding Skills

Skills are reusable agent capabilities:

1. Create `01_execution/skills/<skill-name>.md`
2. Define: type, trigger, inputs, outputs, scope, failure_mode
3. Register in `skills_registry.json` (path set in `sdd.config.json`)

See `01_execution/skills/README.md` for the minimum skill contract.

---

## Contributing

This is a young framework. All feedback is valuable, especially:
- **Validation reports**: How does SDD work in your project? What frictions did agents hit?
- **Stack adaptations**: How did you adapt the prompts for your language/framework?
- **New domains**: Using SDD outside software? Tell us.

See `CONTRIBUTING.md` for details.

---

**Version:** 0.1.0-beta  
**License:** Apache-2.0  
**Copyright:** 2026 Oriol Coll

---

## License

Licensed under the Apache License, Version 2.0.  
See [LICENSE](LICENSE) for full text.
