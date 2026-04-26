# Tasks: feat-073 — User Shadow MVP Contract (Doc-Only)

## Skills
N/A (doc-only)

## Phase 1: VALIDATION

### V1: Validate design coherence

- [ ] Design existent a `artifacts/design/feat-073-user-shadow-mvp-contract-doc-only.md`
- [ ] Contracte d'inputs/outputs definit (REQ-073-2, REQ-073-3, REQ-073-4)
- [ ] Anti-Drift rules documentades (REQ-073-5)
- [ ] Dependències amb feat-055, feat-067, feat-019

### V2: Validate spec coherence

- [ ] Spec cobreix CAP-01..CAP-09 del dossier SEED-04 (SDT-073-01..SDT-073-09)
- [ ] Acceptance criteria completes (AC-01..AC-07)
- [ ] Out of scope explícit

## Phase 2: TASKS → VERIFY (doc-only, no implementation)

### T1: Create verify report

**File**: `00_project_documentation/SDD/audit_reports/verify_feat-073-user-shadow-mvp-contract-doc-only_2026-04-12.md`

Doc-only: no tests a executar. Verify valida coherència docs.

## Phase 3: AUDIT

### A1: Generate audit report

**File**: `00_project_documentation/SDD/audit_reports/audit_feat-073-user-shadow-mvp-contract-doc-only_2026-04-12.md`

AUDIT valida:
1. Contracte coherent amb SEED-04 dossier (CAP-01..CAP-09)
2. Out of scope respectat (cap implementació)
3. Anti-drift rules presents

## Phase 4: ARCHIVE

### ARCH-1: Update feature JSON

Update `feat-073-user-shadow-mvp-contract-doc-only.json`:
- `state`: `ARCHIVED`
- `validation_result`: `PASS`
- `verification_result`: `PASS`
- `audit_result`: `PASS`
- Timestamps

## Dependencies

- SEED-04 dossier: `artifacts/pre_sdd/seed_dossiers/SEED-04.md`
- feat-055 (Action Log MVP)
- feat-067 (Approvals Backend MVP)
- feat-019 (Ticket Runtime Contract)

## Notes

- Aquest és un contracte doc-only: defineix QUÈ és User Shadow i QUÈ NO ÉS, més els inputs/outputs
- No hi ha codi a implementar en aquesta fase MVP
- Qualsevol implementació futura vindrà com a feat separat amb la mateixa autoritat contractual
