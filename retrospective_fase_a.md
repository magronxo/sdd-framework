# Retrospective: Fase A — Project Governance & Pre-SDD

**Date**: 2026-04-23
**Scope**: 7 new documents + 2 updated files
**Reviewer**: Framework self-audit

---

## Summary

Fase A aporta una **capa de projecte operativa i un sistema d'intake pre-SDD** que el framework no tenia. La qualitat general és alta: els documents són coherents, els templates són usables, i les regles de triatge són explícites.

**Veredicte global**: ✅ **PASS with 6 issues to fix** (tots menors o mitjans, cap bloquejador)

---

## Findings

### 🔴 Issue 1: Broken Reference — ADR_POLICY.md no existeix

**Location**: `04_project_governance/PROJECT_MANIFEST.md`, línia 93

**Problem**: El Manifest referencia `02_policies/ADR_POLICY.md` dins de "How to modify this Manifest" i a la secció "Related Documents". Aquest fitxer **no existeix** al framework.

**Impact**: Un usuari que vulgui modificar el Manifest seguirà un enllaç trencat.

**Fix proposat**:
- Opció A: Crear `02_policies/ADR_POLICY.md` (contingut mínim: quan cal un ADR, qui l'aprova, on es guarden)
- Opció B: Eliminar la referència i substituir-la per `templates/adr.md` (que sí existeix)

**Recomanació**: Opció A, perquè un framework enterprise necessita una política d'ADRs explícita. A més, PROJECT_MAP.md ja assumeix que existeix (`artifacts/adr/`).

---

### 🟡 Issue 2: Path Inconsistency — `artifacts/adr/` no està a `sdd.config.json`

**Location**: `04_project_governance/PROJECT_MAP.md`, línia 77; `sdd.config.json`

**Problem**: PROJECT_MAP.md mostra `artifacts/adr/*.md` com a lloc per a ADRs, però `sdd.config.json` no té aquest path a la secció `artifacts`.

**Impact**: Els agents que consultin `sdd.config.json` per resoldre paths no trobaran la ubicació dels ADRs.

**Fix proposat**: Afegir `"adr": "artifacts/adr"` a `sdd.config.json` → `paths.artifacts`.

---

### 🟡 Issue 3: PROJECT_MAP.md Tree no mostra `pre_sdd/` subdirectoris

**Location**: `04_project_governance/PROJECT_MAP.md`, secció "Repository Structure"

**Problem**: L'arbre de directoris mostra `03_operations/pre_sdd/` però no mostra les subcarpetes operatives (`seeds/`, `seeds/deferred/`, `seeds/rejected/`, `seeds/promoted/`, `seeds/merged/`, `templates/`). Això és crític perquè és una guia de navegació.

**Impact**: Un nou usuari no sap on van les seeds ni on trobar-les.

**Fix proposat**: Ampliar l'arbre:

```
├── 03_operations/pre_sdd/
│   ├── seeds/              # Seeds actives (pendents de triatge)
│   ├── seeds/deferred/     # Seeds ajornades
│   ├── seeds/rejected/     # Seeds rebutjades
│   ├── seeds/promoted/     # Seeds promogudes a features
│   ├── seeds/merged/       # Seeds consolidades
│   ├── templates/
│   │   ├── seed_dossier.md
│   │   └── triage_batch.md
│   ├── PRE_SDD_CONTRACT.md
│   └── PRE_SDD_RUNTIME.md
```

---

### 🟡 Issue 4: Inconsistència de nomenclatura — IDs de feature

**Location**: `03_operations/pre_sdd/PRE_SDD_RUNTIME.md`, línia 133

**Problem**: El runtime diu `feat-{NNN}-{short-name}` però `00_core/SDD_FEATURE_FORMAT.md` mostra tant `feat_<seqüencial>_<nom-descriptiu>.md` (amb guions baixos) com `feat-001-kernel-core.md` (amb guionets). Hi ha inconsistència al propi framework.

**Impact**: Confusió sobre el format exacte dels IDs.

**Fix proposat**: Estandaritzar a `feat-{NNN}-{short-name}` (guionets) perquè:
- És el que usa SDD_RUNTIME.md
- És més llegible en URLs i paths
- És el format dels exemples de SDD_FEATURE_FORMAT.md

A més, afegir una nota a `SDD_FEATURE_FORMAT.md` per corregir la referència amb guions baixos.

---

### 🟡 Issue 5: `AGENT_DECISION_TABLE.md` absent de PROJECT_MAP.md

**Location**: `04_project_governance/PROJECT_MAP.md`, secció "Where Truth Lives"

**Problem**: `00_core/AGENT_DECISION_TABLE.md` no apareix a la taula de "On viu la veritat". És un document core que defineix com els agents prenen decisions operatives (p. ex., quan una feature és massa petita per ser independent).

**Impact**: Un agent nou no sap que aquest document existeix.

**Fix proposat**: Afegir a la taula:
| **Agent decision rules** | `00_core/AGENT_DECISION_TABLE.md` | `00_core/AGENT_DECISION_TABLE.md` |

---

### 🟢 Issue 6: Seed Lifecycle Contract vs Runtime mismatch

**Location**: `03_operations/pre_sdd/PRE_SDD_CONTRACT.md`, línia 120

**Problem**: El contracte mostra `CAPTURE → CLASSIFY → TRIAGE → {PROMOTE | DEFER | REJECT | MERGE | SPIKE}` però el runtime té 7 fases (`CAPTURE → CLASSIFY → TRIAGE → PRIORITIZE → REFINE → TRANSITION → ARCHIVE`). El contracte no reflecteix PRIORITIZE, REFINE ni TRANSITION.

**Impact**: El contracte (la "norma") no coincideix amb el runtime (el "procediment"). Això viola el principi del framework de que el runtime redueix el contracte a un procediment executable.

**Fix proposat**: Actualitzar el lifecycle del contracte per mostrar les 7 fases, o almenys afegir una nota que el runtime defineix el flux complet.

---

## Qualitats Positives (Cal Preservar)

1. **GLOSSARY.md té termes pre-omplerts** (SDD Feature, Seed, Validation). Això dóna valor immediat sense esperar que un equip ompli el glossari.

2. **Seed dossier template** té les 6 seccions obligatòries clarament separades i amb explicacions. Un reporter nou sap exactament què omplir.

3. **Triage batch template** inclou "Capacity Check" i "Themes & Patterns". Això evita el patró de "promoure tot per defecte".

4. **PROJECT_MAP.md té navegació per rol**. Això és or pur per a l'onboarding: un developer, un PM, un agent i un auditor tenen camins diferents i explícits.

5. **PRE_SDD_CONTRACT.md prohibeix "solutioneering"** amb claredat: "capture the problem, not the fix". Això ataca una de les causes principals de specs prematures.

6. **Cross-references són exhaustius**. Cada document apunta als relacionats. La xarxa de navegació és densa i útil.

---

## Recomanacions per a Fase B

1. **Corregir els 6 issues abans de continuar**. Cap és bloquejador, però tots degraden la qualitat.

2. **Quan creïs `GETTING_STARTED.md`**, usa el camí de navegació del "new developer" de PROJECT_MAP.md com a estructura del tutorial.

3. **Per als diagrames Mermaid**, inclou el state machine de PRE_SDD_RUNTIME.md i el pipeline canònic de SDD_RUNTIME.md. Són visuals que expliquen més que 100 paraules.

4. **Considera afegir un `seeds/README.md`** dins de `03_operations/pre_sdd/seeds/` que expliqui l'estructura de subcarpetes. PROJECT_MAP.md ho mostra però un README local és més descobrible.

---

## Checklist de Correccions

- [ ] Issue 1: Crear `02_policies/ADR_POLICY.md` o corregir referència
- [ ] Issue 2: Afegir `adr` path a `sdd.config.json`
- [ ] Issue 3: Ampliar PROJECT_MAP.md tree amb subcarpetes pre_sdd
- [ ] Issue 4: Estandaritzar format IDs de feature
- [ ] Issue 5: Afegir AGENT_DECISION_TABLE.md a PROJECT_MAP.md
- [ ] Issue 6: Sincronitzar lifecycle del contracte amb el runtime
