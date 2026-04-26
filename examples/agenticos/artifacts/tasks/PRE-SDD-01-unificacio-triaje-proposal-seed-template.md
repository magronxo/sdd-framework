# Tasks: PRE-SDD-01 — Unificació TRIAGE/Proposal + Seed Template

## Task List

- [ ] **T-1**: Update `pre_sdd/README.md` to point to contract + templates
- [ ] **T-2**: Migrate existing `SEED-04.md` dossier to v1 format
- [ ] **T-3**: Migrate existing `SEED-05.md` dossier to v1 format
- [ ] **T-4**: Migrate existing `SEED-07.md` dossier to v1 format
- [ ] **T-5**: Verify all templates are internally consistent
- [ ] **T-6**: Verify PRE_SDD_CONTRACT.md covers all required fields
- [ ] **T-7**: Verify migration of existing dossiers maintains all information
- [ ] **T-8**: Generate verify report (checklist run)
- [ ] **T-9**: Generate audit report
- [ ] **T-10**: Create feature record JSON with PASS status

## Task Details

### T-1: Update pre_sdd/README.md

**Action**: Modify `00_project_documentation/SDD/artifacts/pre_sdd/README.md`
**Change**: Replace current content with pointer to `PRE_SDD_CONTRACT.md` and template directory

### T-2: Migrate SEED-04 to v1 format

**Action**: Rewrite `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-04.md`
**Change**: Map existing content to v1 schema fields; add missing required fields with placeholders

### T-3: Migrate SEED-05 to v1 format

**Action**: Rewrite `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-05.md`
**Change**: Map existing content to v1 schema fields; add missing required fields with placeholders

### T-4: Migrate SEED-07 to v1 format

**Action**: Rewrite `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-07.md`
**Change**: Map existing content to v1 schema fields; add missing required fields with placeholders

### T-5: Template consistency verification

**Action**: Manual review
**Check**:
- seed_dossier_v1.md has all 11 required fields
- triage_batch_v1.md references dossier paths, does not duplicate
- Both templates parse without errors

### T-6: Contract coverage verification

**Action**: Manual review
**Check**:
- PRE_SDD_CONTRACT.md defines all states (Captured/Explored/Triaged/Adopted/Deferred)
- Exploration gate criteria are explicit (est >2 days / ≥2 unknowns / affects kernel-security)
- TRIAGE contract minimum fields are defined (problem/objective/scope/non-scope/risks/success_signal)
- HANDOFF paths are defined (feat-XXX.json / ADR / Deferred)

### T-7: Dossier migration verification

**Action**: Manual review
**Check**:
- All information from original dossiers is preserved (no data loss)
- New v1 fields are present with reasonable values (no empty required fields)
- PKLot reference data (ID, title, trigger, impact, horizon) preserved

### T-8: Verify report

**Action**: Generate `verify_PRE-SDD-01.md`
**Content**: Checklist results from T-5, T-6, T-7
**Criteria**: All items pass → PASS

### T-9: Audit report

**Action**: Generate `audit_PRE-SDD-01.md`
**Content**: Summary of changes, decisions, compliance with MVP scope
**Criteria**: Doc-only, no SDD core changed, no tooling introduced

### T-10: Feature record creation

**Action**: Create `feat-XXX-pre-sdd-unification-seed-template.json`
**Content**: Standard feature record with validation_result/verification_result/audit_result = PASS
**Location**: `00_project_documentation/SDD/artifacts/features_for_specs/`

## Dependencies

- T-1: No dependencies
- T-2, T-3, T-4: Require T-1 and seed_dossier_v1.md template to exist
- T-5, T-6, T-7: Require all templates and contract written (T-1, T-2, T-3, T-4)
- T-8: Requires T-5, T-6, T-7
- T-9: Requires T-8
- T-10: Requires T-8, T-9

## Completion Criteria

All tasks complete when:
- README updated and points to contract + templates
- 3 existing dossiers migrated to v1 format
- All verification checks pass
- Verify and audit reports generated
- Feature record JSON created with PASS status