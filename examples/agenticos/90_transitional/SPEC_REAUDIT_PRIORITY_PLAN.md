STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

# Redirect (archived)
**STATUS:** ARCHIVED (redirect header)
**AUTHORITY:** NON-CANONICAL
**ARCHIVED_AT:** 2026-04-09

Canonical workflow: `00_project_documentation/SDD/03_operations/SPEC_REAUDIT_WORKFLOW.md`
Roadmap: `00_project_documentation/SDD/03_operations/ROADMAP.md`
Policy (priorització): `00_project_documentation/SDD/02_policies/SPECS_REAUDIT_PRIORITIZATION_POLICY.md`
Archived copy (with archive header): `00_project_documentation/SDD/90_transitional/archive/SPEC_REAUDIT_PRIORITY_PLAN.md`

---

This document is transitional context. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# Spec Re-Audit Priority Plan

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** Priorització de re-auditoria de specs amb flux propi + complement extern (`gentle-ai`)

---

## 1. Propòsit

No té sentit re-auditar totes les specs alhora.

Cal començar per les que:

- defineixen primitives centrals del sistema
- tenen més radi d'impacte
- poden contaminar altres specs si estan mal definides
- combinen risc estructural amb alta reutilització

---

## 2. Criteri de Priorització

Cada spec es valora segons cinc factors:

1. **Centralitat arquitectònica**
2. **Radi d'impacte sobre altres features**
3. **Sensibilitat a ambigüitat**
4. **Acoblament amb runtime o flux extern**
5. **Valor de re-auditoria amb `gentle-ai`**

---

## 3. Ordre Recomanat

### TIER 1 — Re-auditoria immediata

Aquestes són les primeres que s'han de revisar.

#### 1. `feat-001-kernel-core`

**Per què va primera**

- defineix primitives base del sistema
- condiciona tickets, execució, errors i lifecycle
- qualsevol ambigüitat aquí es replica a mig repositori

**Fitxer**

- [feat-001-kernel-core.md](K:\AgenticOsGen\00_project_documentation\SDD\specs\feat-001-kernel-core.md)

#### 2. `feat-008-context-builder`

**Per què va segona**

- és la frontissa entre identitat, memòria, eines i prompt
- està molt a prop del tipus de millores que `gentle-ai` pot detectar bé
- és crítica per qualitat cognitiva del sistema

**Fitxer**

- [feat-008-context-builder.md](K:\AgenticOsGen\00_project_documentation\SDD\specs\feat-008-context-builder.md)

#### 3. `feat-006-api-server`

**Per què va tercera**

- és la interfície principal entre sistema i surfaces externes
- barreja REST, WebSocket, auth i observabilitat
- pot arrossegar incoherències de contracte si es deixa per més endavant

**Fitxer**

- [feat-006-api-server.md](K:\AgenticOsGen\00_project_documentation\SDD\specs\feat-006-api-server.md)

#### 4. `feat-017-react-loop`

**Per què va quarta**

- és una de les specs més sensibles a qualitat de reasoning
- toca loop, context, límits, seguretat i tool feedback
- és candidata ideal perquè un auditor extern trobi buits subtils

**Fitxer**

- [feat-017-react-loop.md](K:\AgenticOsGen\00_project_documentation\SDD\specs\feat-017-react-loop.md)

---

### TIER 2 — Re-auditoria de consolidació

Aquestes venen després del TIER 1.

#### 5. `feat-002-llm-proxy`
- perquè toca providers, fallback conceptual i contracte de model extern

#### 6. `feat-003-engram-memory`
- perquè defineix memòria persistent i és clau si després volem explotar memòria externa

#### 7. `feat-004-ticket-system`
- perquè el model de ticket és una primitive crítica i ha de quadrar amb el nucli i l'API

#### 8. `feat-012-kernel-status-api`
- perquè consolida contractes de control i observabilitat

#### 9. `feat-015-ollama-fallback`
- perquè és extensió important del món LLM, però menys central que el proxy i el context builder

---

### TIER 3 — Re-auditoria funcional / de superfície

Aquestes es poden re-auditar després.

#### 10. `feat-006-dashboard-react`
#### 11. `feat-014-llm-healthcheck`
#### 12. `feat-016-chat-ticket-creator`

**Per què van més tard**

- tenen molt valor d'ús
- però no són les primitives més profundes del sistema
- és millor arribar-hi un cop el nucli documental estigui més ferm

---

### TIER 4 — Re-auditoria d'expansió o futur

#### 13. `feat-013-session-tree`

**Per què va més tard**

- està encara en una zona mixta entre MVP parcial i extensió futura
- es beneficiarà molt més de re-auditar-se després que TIER 1 i TIER 2 estiguin sòlids

---

## 4. Ordre Recomanat de Lots

### Lot A

- feat-001
- feat-008

**Estat actual**

- `feat-008` ja està normalitzada i tancada documentalment
- `feat-001` ja està normalitzada amb traçabilitat corregida

### Lot B

- feat-006-api-server
- feat-017-react-loop

**Estat actual**

- `feat-006-api-server` ja esta normalitzada i tancada documentalment
- `feat-017-react-loop` ja esta normalitzada i tancada documentalment

**Lot B**

- tancat

### Lot C

- feat-002
- feat-003
- feat-004

**Estat actual**

- `feat-002` ja està normalitzada i tancada documentalment
- `feat-003` ja està normalitzada i tancada documentalment
- `feat-004` es tracta com a cas pre-SDD sense traçabilitat canònica completa

**Lot C**

- tancat

### Lot D

- feat-012
- feat-015

**Estat actual**

- `feat-012` ja esta normalitzada i tancada documentalment
- `feat-015` ja esta normalitzada i tancada documentalment

**Lot D**

- tancat

### Lot E

- feat-006-dashboard-react
- feat-014
- feat-016
- feat-013

**Estat actual**

- `feat-006-dashboard-react` ja esta normalitzada i tancada documentalment
- `feat-014` ja esta normalitzada i tancada documentalment
- `feat-016` ja estava alineada i es manté tancada documentalment
- `feat-013` continua actiu com a proper cas del bloc

**Lot E**

- parcialment tancat

---

## 5. Regla d'Execució

No passar al lot següent si el lot anterior obre:

- contradiccions sistèmiques
- redefinició de primitives
- canvis que obliguin a revisar el criteri del lot següent
- artefactes tancats amb referències antigues encara actives

---

## 6. Paper de `gentle-ai`

`gentle-ai` és especialment valuós als lots:

- **A**
- **B**
- **C**

Perquè aquí pot aportar:

- detecció de buits subtils
- millores de definició de memòria i context
- pressió extra sobre escenaris i límits

---

## 7. Criteri d'Èxit

El pla de priorització funciona si:

- es revisen primer les specs amb més radi d'impacte
- `gentle-ai` s'usa on pot aportar més valor
- no es malgasta temps re-auditant superfícies abans de primitives
