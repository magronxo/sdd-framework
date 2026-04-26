# PRE-SDD Selected → Handoff

date: 2026-04-12  

## Seed adopted

- **SEED-04** — User Shadow / Adversarial Co-Pilot
- **SEED-05** — Execution Trace Contract + Flow Projection

## Decision reference

- SEED-04 batch addendum: `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12_addendum_02.md`
- SEED-04 dossier: `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-04.md`
- SEED-05 batch addendum: `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12_addendum.md`
- SEED-05 dossier: `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-05.md`

## Handoff targets (SDD)

- **Proposed feature**: `feat-073-user-shadow-mvp-contract-doc-only`
- **Feature record**: `00_project_documentation/SDD/artifacts/features_for_specs/feat-073-user-shadow-mvp-contract-doc-only.json`
- **Proposed feature**: `feat-068-execution-trace-contract-mvp`
- **Feature record**: `00_project_documentation/SDD/artifacts/features_for_specs/feat-068-execution-trace-contract-mvp.json`

## Scope guardrails

### SEED-04 (feat-073)
- Contract-first: User Shadow defined as contract; observation patterns documented, not implemented.
- No side effects: User Shadow observes via ActionLog; no new execution paths.
- No proactive suggestions: adversarial suggestions only on explicit user request.
- Transparency: consent manifest / status endpoint, no hidden capture.
- Doc-only: no runtime/kernel changes, no UI changes.

### SEED-05 (feat-068)
- Contract-first: traça definida com a contracte i API; UI és projecció, no font de veritat.
- No side effects: no s'introdueix lògica d'execució nova al kernel com a part d'aquest handoff; només observabilitat.
- Determinisme: schema estable, errors deterministes, i evidència de verify/audit.

## Dependencies

- `feat-055` (Action Log) — base per events/observabilitat (SEED-04 + SEED-05).
- `feat-067` (Approvals Backend HITL) — referència HITL existent per a SEED-04.
