# Retrospective: Fases C i D — Enterprise Policies i Migration Playbook

**Date**: 2026-04-23
**Scope**: 6 new documents (3 policies + 1 template + 1 playbook + 1 skill)
**Reviewer**: Framework self-audit

---

## Summary

Fases C i D aporten **polítiques enterprise**, **planificació estratègica**, i **suport per a migracions**. La qualitat és alta però hi ha **4 issues menor-mitjans** a corregir.

**Veredicte global**: ✅ **PASS with 4 issues to fix** (tots menors o mitjans, cap bloquejador)

---

## Findings

### 🟡 Issue 1: VALIDATION_BOUNDARIES — Scope expansion contradictori

**Location**: `02_policies/VALIDATION_BOUNDARIES_POLICY.md`, línia 79

**Problem**: "Scope expansion" apareix com a condició de reopening, però entre parèntesis diu "requires new seed → new feature, not reopening". Això és contradictori: o és una condició de reopening o no ho és.

**Impact**: Confusió sobre si es pot reobrir una spec per afegir scope.

**Fix proposat**: Separar en dues llistes clares:
- "Valid Reopening Conditions" (3 ítems)
- "What Is NOT Reopening" (scope expansion va aquí)

---

### 🟡 Issue 2: MIGRATION_PLAYBOOK — "All new features start as seeds" és imprecís

**Location**: `03_operations/MIGRATION_PLAYBOOK.md`, línia 73

**Problem**: Diu "All new features start as seeds in `03_operations/pre_sdd/`" però el `AGENT_DECISION_TABLE.md` i `DECOMPOSITION_AND_SIZE_POLICY.md` permeten "code adjustments" (< 50 línies, ≤ 2 RF) que NO passen per Pre-SDD.

**Impact**: Un equip podria forzar SDD complet per a canvis trivials.

**Fix proposat**: Canviar a "All new non-trivial features start as seeds. Trivial fixes use the code adjustment path."

---

### 🟡 Issue 3: MIGRATION_PLAYBOOK — No avisa sobre init scripts en repos existents

**Location**: `03_operations/MIGRATION_PLAYBOOK.md`, línia 44

**Problem**: Diu "Run `init-sdd.ps1` or `init-sdd.sh`" sense avisar que aquests scripts podrien sobreescriure fitxers existents (ex: `README.md`, `sdd.config.json`) si el repo ja existeix.

**Impact**: Pèrdua accidental de documentació existent.

**Fix proposat**: Afegir nota: "Run init scripts with caution on existing repos. Review generated files before committing. Prefer manual creation if the repo already has documentation."

---

### 🟢 Issue 4: ROADMAP_TEMPLATE — "SEED" no és un estat de feature vàlid

**Location**: `03_operations/ROADMAP_TEMPLATE.md`, línia 47

**Problem**: La taula "Feature Mapping" mostra `SEED` com a status, però els estats canònics de feature són: DESIGN, SPEC, VALIDATION, TASKS, IMPLEMENT, VERIFY, AUDIT, ARCHIVE. SEED és pre-SDD.

**Impact**: Confusió entre seeds i features.

**Fix proposat**: Canviar l'exemple a `DESIGN` o `PENDING`, o afegir una nota que els seeds no apareixen a la feature mapping fins que són promoguts.

---

## Qualitats Positives (Cal Preservar)

1. **EXTERNAL_FRAMEWORK_POLICY.md — "Authority inversion prevention"** és un concepte fort i ben explicat amb exemples concrets (React hooks, ORM, linter).

2. **MIGRATION_PLAYBOOK.md — Common Pitfalls** amb "Reality + Fix" és or pur per a l'adopció. Ataqua objeccions reals abans que sorgeixin.

3. **VALIDATION_BOUNDARIES_POLICY.md — Authority by Artifact Type** amb taules per cada tipus de document és extremadament clar. Un implementer sap exactament què pot/canviar i quan.

4. **ROADMAP_TEMPLATE.md — Reality Check** amb 5 preguntes i output estructurat converteix el roadmap en un document viu, no estàtic.

5. **hello-world-skill.md** és exactament el que cal: un exemple mínim que demostra contracte, surfaces, i errors sense complexitat.

---

## Recomanacions

1. Corregir els 4 issues abans de considerar les fases C i D tancades.

2. Considerar afegir un enllaç des de `GETTING_STARTED.md` al `MIGRATION_PLAYBOOK.md` per a usuaris que adopten SDD en un projecte existent (no passem directe de tutorial a migració).

---

## Checklist de Correccions

- [ ] Issue 1: Separar "Valid Reopening Conditions" de "What Is NOT Reopening" a VALIDATION_BOUNDARIES
- [ ] Issue 2: Precisar "All new non-trivial features start as seeds" a MIGRATION_PLAYBOOK
- [ ] Issue 3: Afegir avís sobre init scripts en repos existents a MIGRATION_PLAYBOOK
- [ ] Issue 4: Canviar "SEED" a "PENDING" o afegir nota a ROADMAP_TEMPLATE
