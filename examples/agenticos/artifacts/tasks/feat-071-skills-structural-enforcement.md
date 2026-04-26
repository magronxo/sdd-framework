# Tasks: feat-071 — Skills Structural Enforcement v1

## Skills
| Task | Skills |
|---|---|
| GLOBAL | golang-patterns |
| T1.1 | golang-patterns |
| T2.1 | golang-patterns |

## Phase 1: Validation (DESIGN → SPEC review)

### V1: Validate design coherence

Design existent i coherent:
- [ ] Design té DD-01 a DD-07
- [ ] Regles de patrons definides (Go only MVP)
- [ ] Secció `## Skills` amb justificacions definida
- [ ] Feature record amb `structural_enforcement_rules`
- [ ] Dependències amb feat-066

## Phase 2: IMPLEMENT

### T1.1: Create skillsStructuralCheck.ps1

**File**: `04_tools/skillsStructuralCheck.ps1`

**Paràmetres**:
- `-ImplementationFiles` (string array): llista de paths de fitxers de la implementació
- `-TasksPath` (string): path al TASKS .md

**Regles de patrons** (MVP):
```
golang-testing  → **/*_test.go
golang-patterns → 02_implementation/internal/**/*.go
```

**Lògica**:
1. Avaluar cada fitxer de `ImplementationFiles` contra les regles de patrons
2. Agregar skills requerits (únics)
3. Llegir TASKS i extreure la secció `## Skills`
4. Detectar skills declarats i justificacions (`JUSTIFIED:` prefix)
5. Comparar: skills requerits vs. declarats vs. justificats
6. Generar resultat JSON

**Output JSON**:
```json
{
  "status": "PASS|FAIL",
  "timestamp": "RFC3339",
  "check_type": "structural_enforcement",
  "triggered_rules": [
    { "pattern": "**/*_test.go", "skill_required": "golang-testing" }
  ],
  "declared_skills": ["golang-testing"],
  "justifications": [],
  "missing_skills": [],
  "promoted_count": 1
}
```

**Verification**: El script existeix i responde amb JSON vàlid.

### T1.2: Create structural check tests

**File**: `04_tools/skillsStructuralCheck_test.ps1`

**Escenaris de test**:
1. Skill declarat → PASS
2. Skill justificat → PASS
3. Skill mancant → FAIL amb `missing_skills`
4. Cap patró detectat → PASS amb `triggered_rules` buit
5. Skills parcials (un cobert, l'altre no) → FAIL

**Verification**:
```powershell
cd 04_tools
./skillsStructuralCheck_test.ps1
```

Tots els tests de l'script han de passar.

### T2.1: Executar structural check manual

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\04_tools\skillsStructuralCheck.ps1 -ImplementationFiles @("internal/api/action_log_test.go", "internal/kernel/worker.go") -TasksPath "SDD/artifacts/tasks/feat-000.md"
```

Hauria de retornar JSON amb status vàlid.

## Phase 3: VERIFY

### V-071-1: Execute structural check

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\04_tools\skillsStructuralCheck.ps1 -ImplementationFiles @("internal/api/handlers_approvals.go", "internal/api/approvals_store.go") -TasksPath "00_project_documentation/SDD/artifacts/tasks/feat-071-skills-structural-enforcement.md"
```

Capture JSON output.

### V-071-2: Generate verify report

**File**: `00_project_documentation/SDD/audit_reports/verify_feat-071-skills-structural-enforcement_2026-04-12.md`

Ha d'incloure:
- Secció `## COMMANDS` amb l'execució del structural check
- JSON output complet
- `verification_result: PASS`

## Phase 4: AUDIT

### A-071-1: Generate audit report

**File**: `00_project_documentation/SDD/audit_reports/audit_feat-071-skills-structural-enforcement_2026-04-12.md`

AUDIT valida:
1. Structural check implementat correctament
2. Regles de patrons coincideixen amb la spec
3. Justificacions funcionals
4. Feature record enrichit amb `skills_doctor`

## Phase 5: ARCHIVE

### ARCH-1: Update feature JSON

Update `feat-071-skills-structural-enforcement.json`:
- `state`: `ARCHIVED`
- `validation_result`: `PASS`
- `verification_result`: `PASS`
- `audit_result`: `PASS`
- Timestamps: `validated_at`, `verified_at`, `implemented_at`, `archived_at`

## Dependencies

- feat-066 (SKILLS-01 Skills Enforcement Canary) — doctor check existent
- feat-045/046 — sistema de skills
- `skills_registry.json` — registry canònic

## Files to Create

| Path | Task |
|------|------|
| `04_tools/skillsStructuralCheck.ps1` | T1.1 |
| `04_tools/skillsStructuralCheck_test.ps1` | T1.2 |
| `00_project_documentation/SDD/artifacts/design/feat-071-skills-structural-enforcement.md` | (ja creat) |
| `00_project_documentation/SDD/artifacts/specs/feat-071-skills-structural-enforcement.md` | (ja creat) |
| `00_project_documentation/SDD/artifacts/tasks/feat-071-skills-structural-enforcement.md` | (ja creat) |
| `00_project_documentation/SDD/artifacts/features_for_specs/feat-071-skills-structural-enforcement.json` | (ja creat) |

## Notes

- Structural enforcement és procedural, no canvia runtime
- L'script és idempotent: pot executar-se múltiples vegades
- Justificacions prefixades amb `JUSTIFIED:` permeten flexiblitat sense trencar traçabilitat
