# Design: feat-071 — Skills Structural Enforcement v1

## 1. Motivació / Gap

El sistema de skills (feat-045/046/066) té gates a VERIFY i AUDIT:

- VERIFY: si TASKS declara skills → exigir `doctor check` EXIT=0
- AUDIT: si TASKS té secció `## Skills` → exigir skills al registry

**Gap**: Els gates només evalúen si TASKS *declara* skills. No detecten quan *hauria de* declarar-los però no ho fa.

Quan una feature canvia `**/*_test.go` o `**/*.go` a `02_implementation/internal/`, el sistema hauria de detectar automàticament que cal `golang-testing` o `golang-patterns`.

## 2. Decisions de Disseny

### DD-01: Feature ID i tipus

- `feat-071` — Skills Structural Enforcement v1
- Tipus: `SYSTEM_SPEC` (governança/procedural)
- Estat inicial: `DESIGN`

### DD-02: Regles mínimes de detecció de patrons

Les regles defineixen quin **skill** es requereix quan es toquen certs patrons de fitxers:

| Patró de fitxer | Skill requerit | Justificació mínima |
|------------------|----------------|---------------------|
| `**/*_test.go` | `golang-testing` | Cal evidència de testing real |
| `**/*.go` sota `02_implementation/internal/` | `golang-patterns` | Cal adherència a convencions Go |

**Regla**: Si la implementació toca algun fitxer que matcheja un patró, TASKS ha de:
1. Declarar el skill associat, **o**
2. Posar `JUSTIFIED` amb una raó explícita (p.ex. `"comentari", "refactoring sense patrons nous", "rollback"`)

### DD-03: On implementar l'enforcement

L'enforcement és **procedural**, no canvia runtime.

Ubicació: script de verificació a `04_tools/skillsStructuralCheck.ps1` (nou, petit).

Aquest script:
1. Llegeix el diff/paths de la feature (des de TASKS o des del feature record)
2. Avalua els patrons de fitxers tocats
3. Compara amb la secció `## Skills` del TASKS
4. Retorna PASS (skills presents o justificats) o FAIL (patrons sense skill ni justificació)

### DD-04: Enriquiment del feature record

Afegir camp `skills_doctor` al feature record JSON quan s'executa el check:

```json
"skills_doctor": {
  "status": "PASS|FAIL",
  "timestamp": "2026-04-12T...",
  "check_type": "structural_enforcement",
  "triggered_skills": ["golang-testing"],
  "declared_skills": ["golang-testing"],
  "justifications": [],
  "promoted_count": 1
}
```

Si TASKS no té secció `## Skills`, i el check detecta patrons que requereixen skill → `status: FAIL`.

### DD-05: TASKS — secció `## Skills` existent

El feat-066 ja defineix la secció `## Skills` al TASKS:

```
## Skills
| Task | Skills |
|---|---|
| GLOBAL | golang-testing, golang-patterns |
| T1.1 | golang-testing |
| T2.1 | JUSTIFIED: "comentari només" |
```

Feat-071 amplia l'obligatorietat: no només cal declarar, sinó que si el check detecta patrons, cal skill o justificació.

### DD-06: Ampliació del VERIFY gate

El gate existent (feat-066) diu: "si TASKS declara skills → exigir `doctor check` EXIT=0".

Feat-071 amplia: "si **structural check detecta patrons** que requereixen skill, TASKS ha de tenir skill declarat o justificació".

Ordre d'execució al VERIFY:
1. `structural check` → PASS/FAIL (patrons vs TASKS `## Skills`)
2. Si structural = FAIL → `verification_result: FAIL`
3. Si structural = PASS i TASKS declara skills → `doctor check` (exigit per feat-066)
4. Si structural = PASS i TASKS no declara skills → OK (res a fer)

### DD-07: Relació amb feat-066

feat-066 ja estableix el gate de `doctor check` quan TASKS declara skills.

feat-071 afegeix la capa **pre-gate**: Structural Enforcement.

El `structural check` és un pas anterior al `doctor check`.

## 3. Arxius a crear/modificar

| Arxiu | Acció |
|-------|-------|
| `00_project_documentation/SDD/artifacts/design/feat-071-skills-structural-enforcement.md` | Create |
| `00_project_documentation/SDD/artifacts/specs/feat-071-skills-structural-enforcement.md` | Create |
| `00_project_documentation/SDD/artifacts/tasks/feat-071-skills-structural-enforcement.md` | Create |
| `00_project_documentation/SDD/artifacts/features_for_specs/feat-071-skills-structural-enforcement.json` | Create |
| `04_tools/skillsStructuralCheck.ps1` | Create |
| `04_tools/skillsStructuralCheck_test.go` o script de test | Create |

## 4. Out of Scope

- Sistema expert complet de "qualsevol skill per a qualsevol patró"
- Autoinstal·lació o promoció de skills
- Canvis a `skills.ps1 doctor` (ja funciona)
- Canvis a `verifier.md` o `sdd-audit.md` (s'amplia el comportament, no el contracte)
- Runtime changes (kernel, API, TUI)
- Verificació de React/TS (futur: `react-flow-*`, `vercel-react-*`)

## 5. Resultat esperat

- `validation_result`: PASS
- `verification_result`: PASS
- `audit_result`: PASS
- Feature archived amb evidència de structural check executat
- El check queda disponible per a futures features

## 6. Referències

- feat-066 (SKILLS-01 Canary) — gates existents de doctor check
- feat-045/046 — sistema de skills
- `00_project_documentation/SDD/02_policies/SKILLS_SYSTEM.md` — taxonomy de skills
- `00_project_documentation/SDD/03_operations/skills/skills_registry.json` — registry canònic
