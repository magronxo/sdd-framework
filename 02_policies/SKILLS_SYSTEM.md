# Skills System

## Purpose

Define the unified model for prompts, skills, and reusable operational capabilities.

## Core Principle

El sistema usa un model híbrid:

- **prompts** per a rols vinculats a fases del flux SDD
- **skills** per a capacitats operatives reutilitzables i auditable

A capability should only be promoted to a skill when it has:

- clear trigger
- explicit inputs/outputs
- bounded scope
- reusable value across contexts
- meaningful failure modes

## Canonical Distinction

### Prompt

A prompt is a role instruction or execution template tied to a specific phase.

Use a prompt when the capability:

- belongs to one phase of the workflow
- primarily shapes reasoning or output form
- depends heavily on variable local context
- does not need a strong I/O contract

### Skill

A skill is a reusable operational capability with explicit contract.

Use a skill when the capability:

- is reused across multiple tasks or phases
- benefits from isolation and explicit activation
- can be audited as a unit
- has known inputs, outputs, scope, and failure modes

## Skill Taxonomy

### 1. Process Skills

Answer: what step of the flow applies now? Examples:

- sdd-design
- sdd-spec
- sdd-tasks
- sdd-verify

### 2. Audit Skills

Answer: does this survive serious review? Examples:

- sdd-audit
- sdd-deep-audit
- future spec re-audit skills

### 3. Analysis Skills

Answer: what must be understood before deciding? Examples:

- context discovery
- document consistency analysis
- artifact mapping

### 4. Integration Skills

Answer: how do we use an external framework without losing identity? Examples:

- external audit harness adapters
- framework comparison helpers
- development memory adapters

### 5. Implementation Skills

Answer: how do we implement well in this stack? Examples:

- language-specific patterns (Go, Python, TypeScript, Rust, etc.)
- testing patterns
- UI framework guidance

## Minimum Skill Contract

Every formal skill should declare:

- type
- trigger
- inputs
- outputs
- scope
- context_dependency
- failure_mode

If these fields cannot be stated clearly, the capability is not yet a skill.

## Current System Inventory

### Prompts currently canonical
- designer.md
- specifier.md
- validator.md
- planner.md
- implementer.md
- verifier.md

### Skills currently canonical
- None by default (added per project needs)

## Decision Tests: Prompt vs Skill

Before promoting a prompt to a skill, answer:

1. Reuse — can it be used in more than one place?
2. Contract — can inputs, outputs, scope, and failures be stated clearly?
3. Composition — does it benefit from combination with other capabilities?
4. Auditability — does it need to be reviewable as a unit?
5. Context Dependence — is it too context-heavy to be stabilized?

If most answers point to explicit reuse and contract clarity, promote to skill.

## Rules for External Frameworks

External frameworks do not define the taxonomy.

If an external framework packages something as a skill, the project only promotes it if it passes the local criteria above.

## Anti-Patterns

- turning every useful prompt into a skill
- creating skills that only repackage one workflow phase
- importing foreign taxonomy without translation
- creating skills with no scope boundaries
- mixing implementation and governance inside one skill

## Operational Decision

Current policy:

- keep process flow mostly prompt-based
- keep specialized audits as skills
- add new skills only when they are truly reusable and contractable
- preserve the hybrid model instead of pretending everything is a skill

## Next Steps

- keep validator under review
- adopt planner as a separate prompt if task generation remains independent
- add skills only for repeatable cross-context capabilities
- validate every new skill against this document before adoption
