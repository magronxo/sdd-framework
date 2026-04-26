# PRE-SDD Triage Batch — triage_2026-04-12_addendum

date: 2026-04-12  
scope: SEED-05 adoption decision + handoff to SDD  
triage_lead: codex-review (post-batch)  

## 1) Context

- Base batch: `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12.md`
- Since that batch, `SEED-05` has completed `entry_checklist` (11/11) and is ready for adoption.
- Note: a previous draft referenced `feat-031`, but `feat-031` already exists in this repo (workspace path access). This addendum allocates a new feature ID.

## 2) Selected (Adopted)

- **SEED-05** — Execution Trace Contract + Flow Projection → **Adopted**

## 3) TRIAGE contract (minimal)

- problem: no contracte de traça d'execució; el dashboard no pot projectar executions reals sense inventar estat
- objective: definir contracte de traça i una projecció visual consultable (ReactFlow) sense convertir la UI en font de veritat
- scope (candidates to spec — SDD):
  - schema de traça (events/handoffs/decisions/tools/ticket state/HITL markers)
  - endpoint API per obtenir una traça per `trace_id`
  - projecció ReactFlow com a vista (read-only)
- non-scope:
  - persistència com a dada primària / DB pròpia
  - debug UI en temps real
  - agent autònom / lògica d'execució nova
- impact: observabilitat + audit + flows; desbloqueja Mission Control futur sense drift
- risks: scope creep i confusió traça vs visualització
- success_signal: trace contract aprovat + kernel emet traça + dashboard pot renderitzar-la

## 4) DECOMPOSE

- decision: 1 feature
- proposed feature:
  - `feat-068` — Execution Trace Contract MVP
- dependencies/order:
  1. `feat-055` (exists): Action Log
  2. `feat-068` (new): Execution Trace Contract MVP

## 5) HANDOFF (created paths)

- feature_records_created:
  - `00_project_documentation/SDD/artifacts/features_for_specs/feat-068-execution-trace-contract-mvp.json`
- notes:
  - `SEED-05` dossier updated to `Adopted` and references this addendum.

