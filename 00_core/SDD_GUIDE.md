# SDD Guide – Spec-Driven Development (Simplificat)

> **Mode Diátaxis**: Explanation
> **Spec-Driven Development** per a sistemes d'agents.
> La **spec** és l'única font de veritat. El codi només implementa specs aprovades.

---

## Axiomes (innegociables)

1. **spec_as_source** – No hi ha comportament sense spec.
2. **no_ambiguity** – Termes vagues = spec invàlida.
3. **edge_cases_first** – Si no es defineix el fallback, el comportament és indefinit.
4. **hardware_aware** – Tota decisió ha de passar el filtre de recursos del projecte.
5. **no_direct_mutation** – Mai es modifica codi directament; sempre a través de documents de feature i specs.
6. **external_dev_first** – Els problemes de flux, governança, context i integració s'han de resoldre fora del nucli abans d'obrir canvis crítics.

---

## Pipeline SDD Simplificat amb Auditoria

Cada funcionalitat es representa amb un **document de tipus `SYSTEM_SPEC`** que avança pels següents estats:

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE
                              ↑______________↓ (si cal revisar)
```

### Implementació: SDT vs TDD

**Per components deterministes (Go, C, Rust, etc.):** Usem **TDD** (Test-Driven Development) durant la fase d'implementació.
- Escriure test → Implementar codi mínim → Refactoritzar
- Els tests deriven dels escenaris SDT definits a la spec

**Per components amb LLM (no deterministes):** Usem **SDT** (Spec-Driven Testing) com a validació final.
- Implementar segons spec → Validar contra escenaris SDT manualment/automàticament

**Fluxe híbrid:**
```
SDD (Documents) → TDD (Codi) → Validació SDT (Sistema complet) → Auditoria → Archive
```

| Estat | Rol | Prompt/Skill | Artifact | Descripció |
|-------|-----|--------------|----------|------------|
| **DESIGN** | Designer | `01_execution/prompts/designer.md` | `artifacts/design/<feature_id>.md` | Defineix el QUÈ: arquitectura, components, hardware budget. |
| **SPEC** | Specifier | `01_execution/prompts/specifier.md` | `artifacts/specs/<feature_id>.md` | Defineix el COM: inputs, outputs, errors, SDT scenarios, Gherkin. |
| **VALIDATION** | Validator | `01_execution/prompts/validator.md` | `validation_result` | Valida que l'spec és completa, determinista i sense ambigüitats. |
| **TASKS** | Planner | `01_execution/prompts/planner.md` | `artifacts/tasks/<feature_id>.md` | Genera una llista de tasques mínima i ordenada a partir d'una spec validada. |
| **IMPLEMENT** | Developer | TDD/SDT | Codi + Tests | Implementa segons spec, tests passen. |
| **VERIFY** | Verifier | `01_execution/prompts/verifier.md` | `verification_result` | Verifica que implementació compleix spec i SDT scenarios. |
| **AUDIT** | Auditor | `01_execution/skills/sdd-audit` (si configurat) | `audit_report` | Auditoria lleugera: spec-codi, tests, qualitat. |
| **ARCHIVE** | Archiver | `N/A (manual)` | `feature_archived` | Consolidació documental i tancament de feature. |

### Skills d'Auditoria

**sdd-audit (Lleugera):**
- **Trigger:** Automàtic després de VERIFY
- **Model:** Ràpid, econòmic (suficient per auditories lleugeres)
- **Abast:** Spec-codi coherence, tests, qualitat bàsica
- **Output:** Informe a `artifacts/audit_reports/audit_[feature]_[data].md`
- **Resultat:** PASS/WARN/FAIL
- **Acció:** Si FAIL → deep audit; Si WARN/PASS → Archive

**sdd-deep-audit (Profunda):**
- **Trigger:** Manual (`/audit-deep`) o cada N features (configurable)
- **Model:** Exhaustiu (necessari per anàlisi profund)
- **Abast:** Seguretat, arquitectura, consistència global
- **Output:** Informe a `artifacts/audit_reports/audit_batch_[n]_[data].md`
- **Resultat:** PASS/WARN/FAIL amb tickets generats
- **Acció:** Pot bloquejar release si FAIL o CRÍTIC

### Auditoria Externa vs Interna

**Externa (recomanada):**
- El nucli del sistema s'audita via skills externs
- Impossible auditar-se a si mateix (immutable, conflicte interessos)
- Més segur, més ràpid, més flexible

**Interna (opcional):**
- Equips o departaments poden tenir auditor intern
- Dashboard IDE permetrà desenvolupar des de dins
- Sistema autònom per a departaments, NO per al nucli crític

**Regla:** Auditoria del nucli crític sempre EXTERNA. Auditoria de departaments pot ser INTERNA.

### Re-auditoria SDD d'artefactes existents

Quan el que es revisa no és una feature nova sinó una spec ja existent, el flux canvia:

1. es llegeix la spec, el design, els tasks i el feature record
2. es fa auditoria interna estructural
3. opcionalment es contrasta amb frameworks d'auditoria externs
4. es triïn findings com `adoptar`, `adaptar` o `descartar`
5. es normalitzen els artefactes afectats
6. es tanca el cas amb un report inequívoc

La prioritat de re-auditoria es governa per:

- `03_operations/SPEC_REAUDIT_WORKFLOW.md`
- `90_transitional/SPEC_REAUDIT_PRIORITY_PLAN.md` (non-canonical priority planning, if still used)

**Regla:** una re-auditoria no és una implementació nova. Si detecta desalineació, es corregeix documentació i traçabilitat abans de tocar runtime.

### Frameworks externs

Els frameworks externs no substitueixen l'SDD propi:

- són complements d'auditoria, memòria externa i revisió de specs
- entorns/harness externs compatibles
- altres marcs: només després de mapping explícit

**Regla:** primer mapping, després adaptació; mai fusió directa.

### Regles de transició

- No es pot saltar cap estat.
- Si VALIDATION falla → torna a SPEC (mai es patch el codi directament).
- Si AUDIT falla → deep audit obligatori; NO archive fins PASS/WARN.
- Cap `[?]` obert pot sortir de DESIGN.
- **Auditoria no bloqueja però documenta:** Sempre es pot archive, però amb advertències si WARN.
- Si una re-auditoria obre inconsistències documentals, no s'ha de tocar el runtime fins que el tancament dels artefactes quedi explícit.

### Flux Complet amb Exemple

```
1. DESIGN:   Crear feat-010-worker-pool-v2.md
             ↓
2. SPEC:     Especificar requisits, SDT scenarios
             ↓
3. VALIDATION: Verificar completesa, determinisme
             ↓ [APROVAT]
4. IMPLEMENT: TDD → workerpool_v2.go + _test.go
             ↓
5. VERIFY:   go test ./... (12/12 PASS)
             ↓
6. AUDIT:    sdd-audit executa automàticament
             Resultat: WARN (Score: 75, 1 warning)
             Informe: audit_feat-010_2026-03-29.md
             Ticket: AUD-007 (millorar documentació)
             ↓
7. ARCHIVE:  Sync a specs main, update features_for_specs.
             ↓
```

### Informes d'Auditoria

**Ubicació:** `artifacts/audit_reports/`

**Nomenclatura:**
- Soft: `audit_[feature]_[YYYY-MM-DD].md`
- Deep: `audit_batch_[n]_[YYYY-MM-DD].md`

**Format:** Senzill, sense soroll. Taula d'issues + recomanacions + tickets.

### Comandes

```bash
/verify [feature]       # Verificar implementació
/audit [feature]        # Auditoria soft manual
/audit-deep             # Auditoria profunda batch
/audit-report           # Mostrar últim informe
```

---

## Formats obligatoris

### Nomenclatura de Fitxers (OBLIGATORI)

Tots els documents de feature HAN DE seguir el format:

```
feat_<seqüencial>_<nom-descriptiu>.md
```

**Regles:**
1. **seqüencial**: Número de 3 dígits (001, 002, ..., 012, ...)
2. **nom-descriptiu**: Paraules en minúscules separades per guions (`-`)
3. **Extensió**: `.md` per a tots els documents

**Exemples vàlids:**
```
feat-001-kernel-core.md
feat-006-api-server.md
feat-006-dashboard-react.md
feat-007-worker-pool.md
feat-012-kernel-status-api.md
```

**Mapeig de carpetes:**
| Carpeta | Contingut | Format |
|---------|-----------|--------|
| `artifacts/design/` | Documents de disseny (QUÈ) | `feat-XXX_nom.md` |
| `artifacts/specs/` | Especificacions (COM) | `feat-XXX_nom.md` |
| `artifacts/tasks/` | Desglossament de tasques | `feat-XXX_nom.md` |
| `artifacts/features_for_specs/` | JSON d'estat | `feat-XXX.json` |

**Renombrat:**
- `dashboard-backend.md` → `feat-006-api-server.md` (ja fet)
- **NO renombrar** `feat-006.md` (és el frontend React, diferenciat per `backend_` al JSON)

### Document de disseny (`artifacts/design/<feature_id>.md`)

Segueix la plantilla `templates/design.md` i inclou:

- Motivació i components afectats
- Data models (structs o JSON schemas)
- Diagrama Mermaid del flux
- Hardware budget (RAM, CPU, disc) — si aplica al projecte
- Preguntes obertes `[?]` (han de ser ZERO per passar a SPEC)

### Especificació funcional (`artifacts/specs/<feature_id>.md`)

Segueix la plantilla `templates/specs.md` i inclou:

- Requisits funcionals (RF) amb paraules clau RFC 2119 (DEURÀ / PODRÀ / NO DEURÀ)
- Inputs i outputs tipats
- Errors (codi, missatge, acció)
- SDT Scenarios (happy path, edge cases, failure modes)
- Criteris d'acceptació en Gherkin (Given/When/Then)
- Dependencies

### Format del document de feature

Segueix el format definit a `00_core/SDD_FEATURE_FORMAT.md`.

---

## Procés pas a pas

1. **Crear feature record**: Crea `artifacts/features_for_specs/<feature_id>.json` amb `state: DESIGN`
2. **Executar Designer**: Llegeix `01_execution/prompts/designer.md`, crea `artifacts/design/<feature_id>.md`, actualitza a `state: SPEC`
3. **Executar Specifier**: Llegeix `01_execution/prompts/specifier.md`, crea `artifacts/specs/<feature_id>.md`, actualitza a `state: VALIDATION`
4. **Executar Validator**: Llegeix `01_execution/prompts/validator.md`, valida:
   - PASS → actualitza a `state: TASKS`
   - FAIL → retorna a `state: SPEC` (sense modificar la spec)
5. **Executar Planner**: Llegeix `01_execution/prompts/planner.md`, crea `artifacts/tasks/<feature_id>.md`, actualitza a `state: IMPLEMENT`
6. **Implementer**: Executa `tasks/` amb TDD i implementa codi + tests
7. **Executar Verifier**: Llegeix `01_execution/prompts/verifier.md`, corre tests + SDT:
   - PASS → `state: AUDIT`
   - FAIL → torna a `state: IMPLEMENT`
8. **Executar Auditor + Archive**: Genera report a `artifacts/audit_reports/` i tanca la feature a `state: ARCHIVE`

---

## SDT (Spec-Driven Testing)

Integrat a l'estat SPEC. Cada spec ha de definir:

1. **Happy Path**: Comportament normal sota condicions ideals
2. **Edge Cases**: Límits físics (disc ple, timeout, memòria baixa)
3. **Failure Modes**: Com es recupera el sistema d'errors

Aquests escenaris es tradueixen en tests d'integració.

---

## Relació amb el codi

- **Spec**: Documenta QUÈ i COM (font de veritat)
- **Implementació**: Codi que compleix la spec
- **Tests**: Derivats dels criteris Gherkin i escenaris SDT

**Ordre correcte:**
1. Escriure spec (SDD)
2. Implementar segons spec
3. Testejar contra criteris d'acceptació
4. Si falla → corregir spec (no codi), tornar a 1

### Re-auditoria sobre codi existent

Quan la implementació ja existeix i el problema és de coherència documental:

1. no es reimplementa per defecte
2. es reconstrueix la cadena de veritat entre spec, design, tasks i feature record
3. es deixa constància del tancament al report d'auditoria
4. només després es permet continuar amb la següent spec del lot

---

## Actualització de Documents de Disseny (Obligatori)

**Quan:** Quan una feature es marca com a ARCHIVE (implementació completada)

**Què cal actualitzar:**
1. **Document de disseny** (`artifacts/design/*.md`): Afegir secció "Estat d'Implementació" amb:
   - ✅ Components implementats (amb fitxers i tests)
   - ⬜ Components pendents (amb notes)
   - Referències a specs i tests
   - Canvis respecte al disseny original (si n'hi ha)

2. **Project Map** (si existeix): Actualitzar:
   - Secció de features (ARCHIVE/PENDING)
   - Components implementats per feature
   - % de compliment respecte al disseny

3. **Altres documents** (si cal):
   - Manifest (si hi ha canvis filosòfics)
   - Parking lot (si s'eliminen features pendents)

**Per què:**
- La font de veritat ha de reflectir l'estat real
- Futures sessions no han de llegir tots els documents
- Mantenir coherència disseny-implementació
- Evitar confusió quan es torna al projecte

**Regla:** NO passar una feature a ARCHIVE sense actualitzar documents de disseny.

---

**Històric:** Versió simplificada (3 rols) per facilitar adopció.
**Actualitzat:** 2026-04-23 — Versió genèrica del framework.
