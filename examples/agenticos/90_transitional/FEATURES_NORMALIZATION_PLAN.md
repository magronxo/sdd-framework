STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

# Redirect (archived)
**STATUS:** ARCHIVED (redirect header)
**AUTHORITY:** NON-CANONICAL
**ARCHIVED_AT:** 2026-04-09

Canonical format reference: `00_project_documentation/SDD/00_core/SDD_FEATURE_FORMAT.md`
Archived copy (with archive header): `00_project_documentation/SDD/90_transitional/archive/FEATURES_NORMALIZATION_PLAN.md`

---

This document is transitional context. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# Features Normalization Plan

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** `00_project_documentation/SDD/features_for_specs/*.json`

---

## 1. Propòsit

Després de l'auditoria estructural, cal classificar els `features_for_specs` segons el seu grau d'alineació amb el model canònic.

Aquest document no els corregeix encara tots. Els **tria**.

---

## 2. Categories

### A. Canònic

Feature que segueix prou bé el model base:

- `id`
- `type`
- `state`
- `title`
- `design_path`
- `spec_path`

I no introdueix excepcions estructurals greus.

### B. Incomplet però recuperable

Feature usable però amb camps insuficients per l'estat actual.

### C. Legacy

Feature que reflecteix una etapa anterior del sistema i s'ha de mantenir per històric, però no com a exemple canònic.

### D. Fora d'esquema

Feature que no encaixa amb el model actual:

- tipus no documentat
- estat no canònic
- esquema diferent
- feature duplicada o composta sense model formal

---

## 3. Classificació Inicial

### A. Canònic o gairebé canònic

- `feat-001.json`
- `feat-002.json`
- `feat-003.json`
- `feat-004.json`
- `feat-007.json`
- `feat-013.json`
- `feat-014.json`
- `feat-016.json`

**Nota:** alguns poden requerir enriquiment de camps, però no trenquen el model.

### B. Incomplet però recuperable

- `feat-008.json`
- `feat-012.json`
- `feat-015.json`

**Motiu:**
- estat `DONE` amb pocs camps finals
- manca de `task_path`, `completed_at`, `audit_result` o altres camps de traçabilitat

### C. Legacy

- `feat-009.json`

**Motiu:**
- usa `design_path` apuntant a `01_design/01_KERNEL.md §4.9`
- reflecteix una forma anterior o informal de documentar implementació

### D. Fora d'esquema

- `feat-006.json`
- `feat-017.json`
- `feat-017-react-loop.json`

**Motius:**

#### `feat-006.json`
- feature composta sense model formal
- camps especials `backend_*`

#### `feat-017.json`
- `type: TOOL_SPEC` no formalitzat
- `state: IMPLEMENTING` no canònic

#### `feat-017-react-loop.json`
- esquema diferent
- duplicació de `feat-017`
- camps `name`, `description`, `priority` en lloc del model habitual

---

## 4. Ordre de Correcció Recomanat

### Pas 1. Tancar el model

Abans de tocar JSONs individuals, ja s'ha començat a fer:

- normalitzar `README.md`
- normalitzar `SDD_FEATURE_FORMAT.md`

### Pas 2. Recuperar casos simples

Corregir primer els incomplets però recuperables:

- `feat-008.json`
- `feat-012.json`
- `feat-015.json`

### Pas 3. Marcar legacy explícit

No "arreglar" `feat-009.json` fingint que sempre ha estat canònic.

Cal decidir:

- mantenir-lo com a `legacy_record`
- o reescriure'l del tot

### Pas 4. Tractar excepcions estructurals

Casos que requereixen modelar millor el sistema:

- `feat-006.json` -> feature composta
- `feat-017.json` + `feat-017-react-loop.json` -> duplicació / subfeature / transició de model

---

## 5. Regla de Treball

No s'han de corregir tots els JSONs d'una tirada.

L'ordre correcte és:

1. model canònic
2. classificació
3. recuperables
4. legacy
5. excepcions estructurals

---

## 6. Següent Pas Recomanat

El següent pas útil és corregir els casos recuperables, perquè són els que netegen més soroll amb menys risc:

1. `feat-008.json`
2. `feat-012.json`
3. `feat-015.json`

Després d'això ja es pot entrar als casos més delicats (`feat-006`, `feat-017`, `feat-009`).
