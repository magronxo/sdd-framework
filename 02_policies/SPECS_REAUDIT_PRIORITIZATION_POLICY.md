# Policy: Spec Re-Audit Prioritization

## Purpose

Avoid the high-risk pattern: **re-auditing all specs at once**.

Re-audit must be done in batches and by risk/impact order, to reduce:

- contamination of derived specs
- documental divergence
- audit noise (many conclusions, few actionable)

## Effective date

- 2026-04-09

## Core rule

It does not make sense to re-audit all specs at once.

Start with specs that:

- define central system primitives
- have the most impact radius
- can contaminate other specs if poorly defined
- combine structural risk with high reuse

## Application (operational)

When opening a re-audit round:

1) Define the batch (3–10 specs) with prioritization criteria.
2) Apply the canonical re-audit workflow:
   - `03_operations/SPEC_REAUDIT_WORKFLOW.md`
3) Document why the batch (1 paragraph) and the next candidate batch.

## Non-goals

- It does not redefine the SDD pipeline.
- It does not force the use of any external tool.
