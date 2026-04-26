# External SDD Triage Report — Batch 2026-04-08

## 1. Reading Contract Compliance Issues

1. **Path format inconsistent**: Múltiples features usen `/SDD/artifacts/...` (legacy alias) en comptes de `00_project_documentation/SDD/artifacts/...` (canonical). Afecta: feat-001, feat-002, feat-003, feat-005, feat-006, feat-007, feat-008, feat-009, feat-012, feat-014, feat-015, feat-016, feat-017, feat-019, feat-020.
2. **feat-004 sense SDD**: `design_path: null`, `spec_path: null`. Implementat abans de SDD. Cal classificar com a `legacy_record` o crear els artifacts.
3. **feat-005 usa spec de feat-001**: `spec_path` apunta a `feat-001-kernel-core.md` (spec d'altra feature). No és específic de Ticket System.
4. **State "DONE" vs "ARCHIVE"**: SDD_RUNTIME estableix `ARCHIVE` com a estat terminal. Totes les features amb `state: "DONE"` haurien de migrar a `ARCHIVE` (excloent feat-004, feat-013, feat-021).
5. **feat-017 amb estat no-canònic**: `state: "IMPLEMENTING"` no existeix al pipeline. Canonical: DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE.

## 2. Per-Feature Status Table

| feature_id | claimed_state | real_state_recommended | blocking issues | next 1–2 actions |
|------------|---------------|------------------------|-----------------|------------------|
| feat-001 | DONE | ARCHIVE | Validation PASS, SDT OK, tests OK | Migrar a ARCHIVE |
| feat-002 | DONE | ARCHIVE | Validation PASS, 3/10 tests pending | Migrar a ARCHIVE |
| feat-003 | DONE | ARCHIVE | Validation PASS, 4/10 tests pending | Migrar a ARCHIVE |
| feat-004 | DONE | LEGACY | No design/spec paths | Classificar legacy_record |
| feat-005 | DONE | ARCHIVE | Spec shared with feat-001 | Migrar a ARCHIVE |
| feat-006 | DONE | ARCHIVE | composite_feature, validation OK | Migrar a ARCHIVE |
| feat-007 | DONE | ARCHIVE | Validation PASS, 12 tests OK | Migrar a ARCHIVE |
| feat-008 | DONE | ARCHIVE | Validation OK, verification OK, audit OK | Migrar a ARCHIVE |
| feat-009 | DONE | LEGACY | legacy_record pointing to 01_design | Classificar legacy_record |
| feat-012 | DONE | ARCHIVE | validation OK, verification OK, audit OK | Migrar a ARCHIVE |
| feat-013 | VALIDATION | VALIDATION | Implementation exists but not validated | Run VALIDATION → TASKS |
| feat-014 | DONE | ARCHIVE | Verification PASS | Migrar a ARCHIVE |
| feat-015 | DONE | ARCHIVE | Validation OK, verification OK, audit OK | Migrar a ARCHIVE |
| feat-016 | DONE | ARCHIVE | Verification PASS | Migrar a ARCHIVE |
| feat-017 | IMPLEMENTING | LEGACY_RECORD | legacy_record, non-canonical state | Classificar legacy_record |
| feat-017-react-loop | DONE | ARCHIVE | Validation OK, verification OK, audit OK | Migrar a ARCHIVE |
| feat-018 | ARCHIVE | ARCHIVE | Correcte | — |
| feat-019 | DONE | ARCHIVE | Verification PASS | Migrar a ARCHIVE |
| feat-020 | DONE | ARCHIVE | — | Migrar a ARCHIVE |
| feat-021 | VALIDATION | VALIDATION | Note: implementation not present in code; tasks reopened | Run VALIDATION |

## 3. Required Fixes (Governance/Docs Only)

1. **Migrar features de DONE → ARCHIVE**: Features 001, 002, 003, 005, 006, 007, 008, 012, 014, 015, 016, 017-react-loop, 019, 020. Estat ja complert, només cal actualitzar el camp `state`.
2. **Normalitzar paths a format canònic**: Actualitzar `design_path`/`spec_path`/`task_path` a `00_project_documentation/SDD/artifacts/...` a totes les features afectades (substituir `/SDD/...`).
3. **Classificar feat-004 com a legacy_record**: Afegir `record_type: "legacy_record"` i documentar que és pre-SDD.
4. **Classificar feat-009 com a legacy_record**: Ja té `record_type: "legacy_record"`. Verificar que segueix les normes.
5. **Resoldre feat-013 i feat-021**:
   - feat-013: Executar VALIDATION (implementació existeix)
   - feat-021: Executar VALIDATION (implementació NO existeix segons note)

## 4. Next Triage Batch Suggestion

1. **Batch B**: Features amb Validation/Pending (feat-013, feat-021) → executar VALIDATION
2. **Batch C**: Revisar feat-017 (duplicat amb feat-017-react-loop) → consolidar o classificar
3. **Batch D**: Crear specs per a feat-004 (Dashboard TUI) → completar cadena SDD o classificar legacy

