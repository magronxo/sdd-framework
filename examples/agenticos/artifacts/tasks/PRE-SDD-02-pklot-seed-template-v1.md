# Tasks: PRE-SDD-02 — PKLot Seed Template v1

## Task List

- [ ] **T-1**: Create `artifacts/pre_sdd/templates/pklot_seed_v1.md`
- [ ] **T-2**: Update `04_PARKING_LOT.md` — add "Com capturar seeds" section
- [ ] **T-3**: Update `artifacts/pre_sdd/README.md` — reference PKLot template
- [ ] **T-4**: Verify template fields align with Seed Dossier v1
- [ ] **T-5**: Verify PKLot "Com capturar seeds" section references template
- [ ] **T-6**: Generate verify report
- [ ] **T-7**: Generate audit report
- [ ] **T-8**: Create feature record JSON with PASS status

## Task Details

### T-1: Create PKLot Seed v1 Template

**Action**: Create `00_project_documentation/SDD/artifacts/pre_sdd/templates/pklot_seed_v1.md`
**Content**: Template with 13 fields (seed_id, title, problem, proposed_solution, scope_in, scope_out, success_signals, unknowns, dependencies, exploration_required, entry_checklist, horizon, status_pre_sdd, batch_ref)
**Guidelines**: Include rule about creating Seed Dossier when analysis exceeds ~10 lines

### T-2: Update PKLot with "Com capturar seeds" section

**Action**: Modify `00_project_documentation/04_PARKING_LOT.md`
**Change**: Add section "## Com capturar seeds (PKLot Seed v1)" after the INDEX section, before the SEEDS section
**Content**: Brief explanation + link to template. Do NOT rewrite existing seed tables.

### T-3: Update pre_sdd README to reference PKLot template

**Action**: Modify `00_project_documentation/SDD/artifacts/pre_sdd/README.md`
**Change**: Add PKLot template to Templates section
**Content**: Link to `templates/pklot_seed_v1.md`

### T-4: Template field alignment verification

**Action**: Manual review
**Check**: All fields in pklot_seed_v1.md align with fields in seed_dossier_v1.md where applicable
**Note**: `proposed_solution` in PKLot template corresponds to `approach` in Seed Dossier (PKLot is brief, Dossier is detailed)

### T-5: "Com capturar seeds" section verification

**Action**: Manual review
**Check**:
- Section references the template
- Section does NOT rewrite existing seed tables
- Section is placed before the SEEDS section
- Section explains when to create Seed Dossier vs stay in PKLot

### T-6: Verify report

**Action**: Generate `verify_PRE-SDD-02.md`
**Content**: Checklist results from T-4, T-5
**Criteria**: All items pass → PASS

### T-7: Audit report

**Action**: Generate `audit_PRE-SDD-02.md`
**Content**: Summary of changes, compliance with MVP scope
**Criteria**: Doc-only, no existing PKLot seeds migrated, no disruptive changes

### T-8: Feature record creation

**Action**: Create `pre-sdd-02-pklot-seed-template-v1.json`
**Location**: `00_project_documentation/SDD/artifacts/features_for_specs/`
**Content**: Standard feature record with validation_result/verification_result/audit_result = PASS

## Dependencies

- T-1: No dependencies
- T-2: Requires T-1 (template must exist first)
- T-3: Requires T-1
- T-4: Requires T-1, T-2, T-3
- T-5: Requires T-2
- T-6: Requires T-4, T-5
- T-7: Requires T-6
- T-8: Requires T-6, T-7

## Completion Criteria

All tasks complete when:
- Template created and referenced from PKLot and pre_sdd README
- PKLot updated with "Com capturar seeds" section (non-disruptive)
- All verification checks pass
- Verify and audit reports generated
- Feature record JSON created with PASS status