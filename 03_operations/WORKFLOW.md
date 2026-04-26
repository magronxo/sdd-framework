WORKFLOW.md
Purpose

Provide the operational flow for meaningful work in the project.

This document merges:

the professional operating flow
the practical checklist used before meaningful work

It is an operational overlay, not a replacement for the SDD core documents.

What This Is

This workflow is:

logically above agents
practically embedded in the SDD process
applicable to docs, governance, validation, and implementation work

It coordinates the system. It does not replace:

SDD core pipeline
AGENTS.md
context policy
skills policy
framework integration policy

Core Sequence

Every meaningful task should pass through:

intake
context discovery
gap detection
decision
execution
validation
consolidation

If a task skips these stages, the system is drifting into ad hoc prompting.

Phase 0 — Intake

Ask:

what problem are we solving?
is this docs, governance, validation, or implementation?
does it touch core runtime or only external development?
is the task open, closed, or ambiguous?

If the work is still an idea/seed (not yet an SDD feature), use PRE-SDD process (if defined by the project).

Output:

task classification
scope boundary
first decision on whether docs, code, or both may change

Hard rule:

do not implement during intake

Phase 1 — Context Discovery

Actions:

use semantic/context discovery first when the task is large or unclear (if project has such tools configured)
use rg / textual search for exact location checks
read the authoritative docs for the layer involved
confirm whether the task already has a spec, audit trail, or related feature record

Output:

verified context map
authoritative file set
known contradictions or unknowns

Hard rules:

do not rely on memory alone
do not treat a single agent output as final truth

Phase 2 — Gap Detection

Compare:

spec
design
tasks
feature record
audit report

Ask:

is the issue real or only textual noise?
is it structural, semantic, or just a path/reference mismatch?
does it change the contract or only implementation?

Use AGENT_DECISION_TABLE.md if classification is unclear.

Output:

short gap list
severity assessment
decision on whether change is justified

Hard rules:

do not rewrite because of cosmetic inconsistency
do not force live specs into DONE

Phase 3 — Decision

Possible decisions:

adopt
adapt
discard
defer

Actions:

compare external feedback with local truth
choose the minimum valid change
preserve foundational docs unless contradiction is real

Output:

decision record
minimal action plan

Hard rules:

do not merge external opinion automatically
do not modify foundational docs without justification

Phase 4 — Execution

Actions:

change the smallest artifact that owns the contract
keep write scope narrow
preserve historical truth where needed
avoid collateral edits

Output:

localized change with bounded scope

Hard rules:

do not rewrite the ecosystem for one local issue
do not touch core runtime unless the task explicitly requires it

Phase 5 — Validation

Actions:

reread changed artifact
check references and paths
confirm the gap is actually closed
confirm no new contradiction was introduced

Output:

validated change
explicit remaining risk if any

Hard rules:

do not assume a successful patch means a correct result
do not mark a block closed if active contradictions remain

Phase 6 — Consolidation

Actions:

update audit reports if needed
update lot status if needed
record the decision trail
note whether governance is affected

Output:

durable memory of the change
stable baseline for the next task

Hard rules:

do not leave important decisions only in chat history
do not leave half-audited states

Quick Checklist

Before any meaningful task:

Intake
What problem are we solving?
What layer owns it?
Does it touch runtime?

Context
Did we search semantically first if the task is large or unclear?
Did we read the authoritative docs?
Did we verify exact locations with textual search?

Gaps
Did we compare spec, design, tasks, feature record, and audit report?
Is the issue structural, semantic, or only cosmetic?

Decision
Adopt / adapt / discard / defer?

Execution
Are we changing the smallest contract-owning artifact?
Are we avoiding unnecessary runtime edits?

Validation
Did we reread the changed files?
Did we verify paths, references, and closure of the gap?

Consolidation
Did we record the decision trail?
Did we update audit/lot status if needed?

Practical Rule

If a change does not improve at least one of these, it should wait:

traceability
handoff clarity
validation quality
