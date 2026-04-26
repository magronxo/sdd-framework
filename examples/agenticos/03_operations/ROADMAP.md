ROADMAP.md
Purpose

Define the current professionalization roadmap for the external Kernel development layer.

This document replaces fragmented roadmap-style docs by keeping one current planning view.

It does not redefine the core SDD runtime. It describes what still needs to mature around it.

Current Position

AgenticOS is no longer in the foundation phase.

The following are already materially established:

external Kernel governance
SDD workflow base
context policy
skills taxonomy direction
external frameworks as complements, not authorities

What remains is not a full rewrite. What remains is disciplined consolidation.

Strategic Principle

Do not reopen the whole governance stack unless a real contradiction is found. Prefer small corrections, explicit contracts, and stable execution.

Execution Order
Phase 0 — Delimitation

Goal:

keep product/runtime concerns separate from external development concerns

Success condition:

external development is clearly modeled as distinct from Kernel runtime
Phase 1 — Governance Stabilization

Goal:

keep governance coherent and explicit

Actions:

align AGENTS.md with core SDD truth
keep SDD docs stable unless contradiction is real
remove or mark conflicting legacy execution prompts

Main blockers:

divergence between described and real pipeline
coexistence of canonical vs legacy/provisional flow docs
Phase 2 — Context Maturity

Goal:

make context retrieval reliable and bounded

Actions:

clarify when semantic search is mandatory
clarify when direct reading is enough
preserve separation between development context and runtime context
document fallback behavior cleanly
Phase 3 — Skills Maturity

Goal:

move from informal capabilities to controlled reusable skills only where justified

Actions:

preserve prompt-vs-skill boundary
define minimal contracts for any formalized skills
keep the hybrid system explicit instead of pretending everything is skill-based
Phase 4 — External Framework Mapping

Goal:

understand external systems before adapting anything

Actions:

model gentle-ai, .opencode, external engrams, and related workflows
compare value vs contamination risk
keep them as complements until the base flow is stable
Phase 5 — Adaptation

Goal:

absorb only what survives local translation

Actions:

classify external contributions as adopt / adapt / discard / park
keep any adaptation outside Ring 0 unless explicitly justified
Phase 6 — Consolidation

Goal:

reduce duplication once authority and execution are explicit

Actions:

remove transitional docs no longer needed
collapse duplicated roadmap notes into stable policy or archive
keep one clear operating model for future work
Remaining Gaps
1. Decision Traceability

Still missing:

explicit rationale for important doc changes
clear adopt/adapt/discard records for external feedback
durable references for why a rule exists
2. Cross-Environment Contracts

Still missing:

what Codex, OpenCode, Antigravity, and other environments must receive
what they must return
which artifacts are authoritative after handoff
3. Validation Boundaries

Still missing:

when a document is authoritative
when a change is only a proposal
when a feature can be closed
when a live spec must remain open
4. External Auditor Integration

Still missing:

repeatable comparison between external findings and local truth
explicit rule for when feedback changes docs
explicit rule for when feedback remains advisory only
5. Skill Operationalization

Still missing:

which repeated tasks deserve skills
which remain prompts
how outputs are validated before reuse
What Not To Touch Yet
Kernel runtime
broad rewrites of AGENTS.md
broad rewrites of SDD foundation docs
legitimately live specs still under active evolution
Practical Rule

If a change does not improve one of these, it should wait:

traceability
handoff clarity
validation quality
Exit Conditions

This roadmap can be reduced or archived when:

governance is stable
runtime contract is explicit
skills system is stable
external auditor integration is repeatable
cross-environment handoffs are formalized
