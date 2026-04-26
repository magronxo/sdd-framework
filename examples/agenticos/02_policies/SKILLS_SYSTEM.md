SKILLS_SYSTEM.md
Purpose

Define the unified model for prompts, skills, and reusable operational capabilities in the external Kernel development layer.

Core Principle

AgenticOS uses a hybrid system:

prompts for phase-bound roles inside the SDD flow
skills for reusable, auditable, explicit capabilities

A capability should only be promoted to a skill when it has:

clear trigger
explicit inputs/outputs
bounded scope
reusable value across contexts
meaningful failure modes
Canonical Distinction
Prompt

A prompt is a role instruction or execution template tied to a specific phase.

Use a prompt when the capability:

belongs to one phase of the workflow
primarily shapes reasoning or output form
depends heavily on variable local context
does not need a strong I/O contract
Skill

A skill is a reusable operational capability with explicit contract.

Use a skill when the capability:

is reused across multiple tasks or phases
benefits from isolation and explicit activation
can be audited as a unit
has known inputs, outputs, scope, and failure modes
Skill Taxonomy
1. Process Skills

Answer: what step of the flow applies now? Examples:

sdd-design
sdd-spec
sdd-tasks
sdd-verify
2. Audit Skills

Answer: does this survive serious review? Examples:

sdd-audit
sdd-deep-audit
future spec re-audit skills
3. Analysis Skills

Answer: what must be understood before deciding? Examples:

context-engine based discovery
document consistency analysis
artifact mapping
4. Integration Skills

Answer: how do we use an external framework without losing identity? Examples:

external audit harness adapters
framework comparison helpers
development engram adapters
5. Implementation Skills

Answer: how do we implement well in this stack? Examples:

golang-patterns
go-testing
react-flow
frontend React/TS guidance
Minimum Skill Contract

Every formal skill should declare:

type
trigger
inputs
outputs
scope
context_dependency
failure_mode

If these fields cannot be stated clearly, the capability is not yet a skill.

Current System Inventory
Prompts currently canonical
designer.md
specifier.md
validator.md
planner.md (if adopted)
Skills currently canonical
sdd-audit.md
sdd-deep-audit.md
Grey zone
validator.md
today it remains a prompt
later it may split into:
structural spec validation
post-implementation operational validation
Decision Tests: Prompt vs Skill

Before promoting a prompt to a skill, answer:

Reuse — can it be used in more than one place?
Contract — can inputs, outputs, scope, and failures be stated clearly?
Composition — does it benefit from combination with other capabilities?
Auditability — does it need to be reviewable as a unit?
Context Dependence — is it too context-heavy to be stabilized?

If most answers point to explicit reuse and contract clarity, promote to skill.

Rules for External Frameworks

External frameworks do not define the taxonomy.

If an external framework packages something as a skill, AgenticOS only promotes it if it passes the local criteria above.

gentle-ai

May contribute:

audit patterns
memory ideas
comparison workflows

May not impose:

sovereign skill taxonomy
full workflow replacement
runtime-facing governance
Anti-Patterns
turning every useful prompt into a skill
creating skills that only repackage one workflow phase
importing foreign taxonomy without translation
creating skills with no scope boundaries
mixing implementation and governance inside one skill
Operational Decision

Current policy:

keep process flow mostly prompt-based
keep specialized audits as skills
add new skills only when they are truly reusable and contractable
preserve the hybrid model instead of pretending everything is a skill
Next Steps
keep validator under review
adopt planner as a separate prompt if task generation remains independent
add skills only for repeatable cross-context capabilities
validate every new skill against this document before adoption