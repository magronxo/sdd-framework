# Spec: feat-071 — Skills Structural Enforcement v1

## Overview

| Field | Value |
|-------|-------|
| **Feature ID** | feat-071 |
| **Title** | Skills Structural Enforcement v1 |
| **Type** | SYSTEM_SPEC |
| **State** | SPEC |
| **Created** | 2026-04-12 |

## Problem Statement

El sistema de skills (feat-045/046/066) té gates a VERIFY i AUDIT que exigeixen `doctor check` i secció `## Skills` a TASKS. Tanmateix, aquests gates només s'activen quan TASKS *declara* skills. No detecten quan s'haurien de declarar però TASKS és buida.

## Solution

Structural Enforcement: regles de detecció de patrons de fitxers que exigeixen skill o justificació explícita.

---

## Requirements

### REQ-071-1: Structural Check Script

**Script**: `04_tools/skillsStructuralCheck.ps1`

**Funcions**:
- Llegeix els fitxers de la implementació des del feature record (`implementation_files` array)
- Avalua cada fitxer contra les regles de patrons
- Llegeix la secció `## Skills` del TASKS
- Compara: skills requerits vs. declarats vs. justificats
- Retorna resultat estructurat

**Regles de patrons** (MVP):

| Patró | Skill requerit |
|-------|---------------|
| `**/*_test.go` | `golang-testing` |
| `**/*.go` sota `02_implementation/internal/` | `golang-patterns` |

**Excepcions deterministes**:
- Si cap fitxer de la implementació matcheja cap patró → PASS (res a fer)
- Si el fitxer és `*_test.go` buit (només skeleton generat automàticament) → JUSTIFIED amb raó `"auto-skeleton"`

**Resultats possible**:
- `PASS`: tots els patrons detectats tenen skill declarat o justificació
- `FAIL`: patrons detectats sense skill ni justificació

### REQ-071-2: Format de justificació a TASKS

A la secció `## Skills`, una tasca pot tenir:

```
## Skills
| Task | Skills |
|---|---|
| GLOBAL | golang-testing |
| T1.1 | JUSTIFIED: "només comentaris, cap lògica nova" |
```

El prefix `JUSTIFIED:` activa mode justificació. Qualsevol text darrera és la raó.

**Justificacions vàlides** (MVP):
- `JUSTIFIED: "comentari"` — canvi de comentaris/strings
- `JUSTIFIED: "auto-skeleton"` — codi generat automàticament
- `JUSTIFIED: "rollback"` — revert de canvi previ
- `JUSTIFIED: "refactoring sense patrons nous"` — refactor sense nova lògica

### REQ-071-3: Feature Record — camp `skills_doctor`

Quan el structural check s'executa, el feature record s'enriqueix amb:

```json
"skills_doctor": {
  "status": "PASS|FAIL",
  "timestamp": "2026-04-12T10:00:00Z",
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

### REQ-071-4: Ampliació del VERIFY gate

Workflow al VERIFY:

1. **Structural check** (`skillsStructuralCheck.ps1`)
   - Llegeix `implementation_files` del feature record
   - Avalua patrons → llista de skills requerits
   - Llegeix TASKS `## Skills` → skills declarats + justificacions
   - Compara i determina PASS o FAIL

2. **Si structural = FAIL**
   - `verification_result: FAIL`
   - Genera evidència amb els patrons detectats i quins falten

3. **Si structural = PASS** i TASKS declara skills
   - Executa `doctor check` (gate existent feat-066)
   - `verification_result` depèn del doctor check

4. **Si structural = PASS** i TASKS no declara skills
   - No cal doctor check per aquesta feature
   - `verification_result: PASS` (només structural)

---

## SDT Scenarios

### SDT-071-01: Structural PASS — skill declarat

**Given** TASKS té `## Skills` amb `GLOBAL: golang-testing`  
**And** la implementació inclou `**/*_test.go`  
**When** s'executa el structural check  
**Then** el resultat és `PASS`  
**And** `triggered_rules` conté `golang-testing`  
**And** `declared_skills` conté `golang-testing`  
**And** `missing_skills` és buit

### SDT-071-02: Structural PASS — skill justificat

**Given** TASKS té `## Skills` amb `GLOBAL: JUSTIFIED: "comentari"`  
**And** la implementació inclou `**/*.go` sota `02_implementation/internal/`  
**When** s'executa el structural check  
**Then** el resultat és `PASS`  
**And** `triggered_rules` conté `golang-patterns`  
**And** `justifications` conté la raó

### SDT-071-03: Structural FAIL — skill mancant

**Given** TASKS té `## Skills` buida (només capçalera)  
**And** la implementació inclou `**/*_test.go`  
**When** s'executa el structural check  
**Then** el resultat és `FAIL`  
**And** `missing_skills` conté `golang-testing`

### SDT-071-04: Structural PASS — cap patró detectat

**Given** TASKS no té cap skill declarat  
**And** la implementació només canvia `.md` i configs  
**When** s'executa el structural check  
**Then** el resultat és `PASS`  
**And** `triggered_rules` és buit

### SDT-071-05: Structural PASS — skill parcial

**Given** TASKS té `## Skills` amb `GLOBAL: golang-testing`  
**And** la implementació inclou `**/*_test.go` i `**/*.go` sota `02_implementation/internal/`  
**When** s'executa el structural check  
**Then** el resultat és `PASS` (ambdós skills coberts)

---

## Acceptance Criteria

| ID | Criteri |
|----|---------|
| AC-01 | `skillsStructuralCheck.ps1` existeix a `04_tools/` |
| AC-02 | El script accepta `implementation_files` i `tasks_path` com a paràmetres |
| AC-03 | El script avalua `**/*_test.go` → `golang-testing` |
| AC-04 | El script avalua `**/*.go` sota `02_implementation/internal/` → `golang-patterns` |
| AC-05 | El script llegeix la secció `## Skills` del TASKS i detecta justificacions |
| AC-06 | El script retorna JSON amb `status: PASS|FAIL`, `triggered_rules`, `missing_skills` |
| AC-07 | El feature record s'enriqueix amb `skills_doctor` block |
| AC-08 | Tests executen: `skillsStructuralCheck.ps1` amb diversos escenarios |

---

## Files

| File | Change |
|------|--------|
| `04_tools/skillsStructuralCheck.ps1` | New — structural enforcement script |
| `00_project_documentation/SDD/artifacts/design/feat-071-skills-structural-enforcement.md` | New |
| `00_project_documentation/SDD/artifacts/specs/feat-071-skills-structural-enforcement.md` | New |
| `00_project_documentation/SDD/artifacts/tasks/feat-071-skills-structural-enforcement.md` | New |
| `00_project_documentation/SDD/artifacts/features_for_specs/feat-071-skills-structural-enforcement.json` | New |

---

## Out of Scope

- Regles per a React, TypeScript, altres stacks (MVP només Go)
- Autoinstal·lació de skills
- Canvis a `skills.ps1 doctor`
- Canvis a `verifier.md` o `sdd-audit.md` (només ampliació del comportament)
- Sistema expert de detecció automàtica de patterns complexos

---

## Deferred / Future

- Extensió a regles React (`**/*.tsx`, `**/*.ts`)
- Extensió a `go-testing` i `go-patterns` (diferenciació entre skill i patró)
- Estat `expired` i `approved/denied` per approvals (TBD)
- Detecció automàtica de justificacions vàlides vs inventades
