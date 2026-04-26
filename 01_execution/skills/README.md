# Skills System — Minimum Skill Contract

> **Location:** `01_execution/skills/`
> **Purpose:** Define reusable, auditable operational capabilities.

---

## Minimum Skill Contract

Every formal skill must declare:

| Field | Description |
|-------|-------------|
| `type` | Process / Audit / Analysis / Integration / Implementation |
| `trigger` | What activates this skill? (automatic, manual command, phase gate) |
| `inputs` | Expected input structure (JSON schema or description) |
| `outputs` | Expected output structure |
| `scope` | What this skill does and does NOT do |
| `context_dependency` | What project context it needs (stack, config, etc.) |
| `failure_mode` | What happens when the skill fails |

If these fields cannot be stated clearly, the capability is **not yet a skill**.

---

## Skill Taxonomy

### 1. Process Skills
Answer: what step of the flow applies now?
- `sdd-design`, `sdd-spec`, `sdd-tasks`, `sdd-verify`

### 2. Audit Skills
Answer: does this survive serious review?
- `sdd-audit`, `sdd-deep-audit`

### 3. Analysis Skills
Answer: what must be understood before deciding?
- context discovery, document consistency analysis, artifact mapping

### 4. Integration Skills
Answer: how do we use an external framework without losing identity?
- external audit harness adapters, framework comparison helpers

### 5. Implementation Skills
Answer: how do we implement well in this stack?
- Language/framework specific patterns (Go, React, Python, etc.)

---

## Prompt vs Skill

| Aspect | Prompt | Skill |
|--------|--------|-------|
| Scope | One phase of workflow | Reusable across phases/tasks |
| Contract | Loose (reasoning + form) | Strict (inputs, outputs, failures) |
| Auditability | Low | High |
| Context dependence | High (local) | Medium (configurable) |

Before promoting a prompt to a skill, answer:
1. Reuse — can it be used in more than one place?
2. Contract — can inputs, outputs, scope, and failures be stated clearly?
3. Composition — does it benefit from combination with other capabilities?
4. Auditability — does it need to be reviewable as a unit?
5. Context Dependence — is it too context-heavy to be stabilized?

If most answers point to explicit reuse and contract clarity, promote to skill.

---

## Anti-Patterns

- turning every useful prompt into a skill
- creating skills that only repackage one workflow phase
- importing foreign taxonomy without translation
- creating skills with no scope boundaries
- mixing implementation and governance inside one skill

---

## Current State

This project has **no default skills**. Add skills here as `.md` files when they pass the Minimum Skill Contract above.

Register canonical skills in the skills registry (path defined in `sdd.config.json`).
