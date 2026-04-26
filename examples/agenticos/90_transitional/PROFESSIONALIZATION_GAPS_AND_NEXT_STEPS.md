STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

This document is transitional context. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# Professionalization Gaps and Next Steps

> **Purpose:** define what still blocks AgenticOS from being fully "pro" and what to do next without reopening the whole governance stack.

## Current Position

The project is no longer in the "foundation" phase.
The large normalization pass already aligned:

- external Kernel governance
- SDD workflow and lot re-audits
- context policy
- skill taxonomy and prompt-vs-skill boundaries
- external frameworks as complements, not sources of truth

What remains is not a rewrite.
What remains is professional-grade operating discipline.

## Remaining Gaps

### 1. Decision Traceability

We can explain what changed, but not every important choice has a durable decision record.

What is missing:

- explicit rationale for important doc changes
- clear adoption/adaptation/discard trail for external feedback
- a stable reference for why a rule exists

### 2. Cross-Environment Contracts

The repo can be handed between agents and tools, but the handoff contract is still too implicit.

What is missing:

- what each environment must receive
- what each environment must return
- which artifacts are authoritative after a handoff

### 3. Validation Boundaries

We have audits, but not every layer has a crisp validation boundary.

What is missing:

- when a document is authoritative
- when a change is only a proposal
- when a feature can be marked closed
- when a live spec must stay open

### 4. External-Auditor Integration

`gentle-ai` is useful as a critic, but the integration shape must stay disciplined.

What is missing:

- a repeatable way to compare its feedback with local truth
- a rule for when its feedback changes docs
- a rule for when it is only advisory

### 5. Skill Operationalization

The skill system is defined, but not yet fully used as a controlled operating layer.

What is missing:

- which tasks should be skills
- which tasks should remain plain prompts
- how skill outputs are validated before reuse

## What To Do Next

### Phase 1: Tighten the Operating Model

- keep `AGENTS.md` stable unless a real contradiction appears
- keep SDD governance docs stable unless a new rule is genuinely needed
- prefer small corrections over structural rewrites

### Phase 2: Add a Decision Record Layer

- record why important changes were made
- record what external feedback was adopted, adapted, or discarded
- keep that trace close to the governance docs, not buried in chat history

### Phase 3: Formalize Handoffs

- define minimal input/output contracts for Codex, OpenCode, Antigravity, and Gemini
- define which docs each agent should trust first
- define what "done" means at each handoff

### Phase 4: Operationalize External Review

- use `gentle-ai` only as an external auditor
- compare its findings against local SDD truth
- do not let it redefine the system by itself

### Phase 5: Make Skills Reusable, Not Decorative

- promote only capabilities that repeat
- keep one-off prompts out of the skill layer
- validate skill outputs before they become reusable practice

## What Not To Touch Yet

- Kernel runtime
- broad rewrites of `AGENTS.md`
- broad rewrites of the SDD foundation docs
- any live spec that is still legitimately open, such as `feat-013-session-tree`

## Practical Rule

If a change does not improve one of these three things, it should wait:

- traceability
- handoff clarity
- validation quality

That is the real remaining work.
