STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

This document is transitional context. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# External Kernel Development Layer

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** Desenvolupament extern del Kernel, governança SDD, context, skills i integracions agentiques

---

## 1. Propòsit

Aquest document defineix la capa de treball **externa al Kernel** per evolucionar AgenticOS sense contaminar Ring 0 ni barrejar runtime amb meta-desenvolupament.

No regula l'execució interna del Kernel. Regula:

- com es desenvolupa el Kernel des de fora
- com s'usa el context-engine en el flux de desenvolupament
- com encaixen skills i frameworks externs
- com s'audita i es complementa l'SDD existent

---

## 2. Principi Rector

**Problema actual:** El projecte té bones peces (`AGENTS.md`, SDD, context-engine, skills, auditories, referències externes), però encara no té una capa única que governi el desenvolupament extern del Kernel.

**Decisió:** Crear una capa explícita de **External Kernel Development** amb aquestes propietats:

- **Fora del Kernel:** cap decisió d'aquesta capa mou responsabilitats cap a Ring 0
- **SDD-first:** la font de veritat continua sent la spec pròpia del projecte
- **Framework-aware:** `gentle-ai`, `.opencode` i altres marcs s'analitzen i s'aprofiten com a complements, no com a autoritat
- **Audit-friendly:** tota integració externa ha de poder revisar-se, aïllar-se o desactivar-se

---

## 3. Fronteres de Responsabilitat

### 3.1 Què pertany a aquesta capa

- Governança de `AGENTS.md`
- Pipeline SDD extern al runtime
- Estratègia d'ús del `context-engine`
- Sistema de skills
- Auditories i re-auditories de specs
- Mapeig i adaptació de frameworks externs

### 3.2 Què NO pertany a aquesta capa

- Event loop del Kernel
- Ticket execution runtime
- Context builder intern del runtime
- Polítiques Fast-Path del Kernel
- Fluxos de producció multi-seed

### 3.3 Regla dura

**Si un problema és de desenvolupament extern, no s'arregla dins del Kernel.**

---

## 4. Objectius Prioritzats

L'ordre correcte no és arbitrari. Cada objectiu depèn de l'anterior.

1. **Refinar `SDD + AGENTS.md + flows`**
2. **Millorar integració de context**
3. **Millorar el sistema de skills**
4. **Mapar frameworks externs**
5. **Adaptar el que encaixi**
6. **Unificar i optimitzar el sistema global**

---

## 5. Ordre d'Execució (Obligatori)

### Fase 0. Delimitació

**Objectiu:** Separar producte i meta-sistema.

**Resultat esperat:**
- una definició clara del que és desenvolupament extern del Kernel
- una frontera clara entre runtime i governança externa

### Fase 1. Governança

**Objectiu:** Normalitzar la narrativa operativa.

**Inclou:**
- alinear `AGENTS.md`
- alinear `SDD_GUIDE.md`
- aclarir rols, estats i artefactes
- fixar regles d'auditoria externa

**Bloquejadors a resoldre aquí:**
- divergència entre pipeline descrit i pipeline real
- solapament entre SDD resumit i SDD complet
- manca d'una capa explícita de desenvolupament extern

### Fase 2. Context

**Objectiu:** Convertir el context en infraestructura fiable del procés.

**Inclou:**
- quan s'ha d'usar `context.ps1`
- quan n'hi ha prou amb lectura directa
- quin context és de desenvolupament i quin és de runtime
- com es documenten consultes semàntiques i limitacions

### Fase 3. Skills

**Objectiu:** Passar de col·lecció de prompts a sistema de capacitats.

**Inclou:**
- taxonomia de skills
- trigger, inputs i outputs esperats
- dependència amb context
- distinció entre skill de procés, skill d'auditoria, skill d'integració i skill d'implementació

### Fase 4. Mapping Extern

**Objectiu:** Entendre marcs externs sense importar-los a cegues.

**Inclou:**
- `gentle-ai`
- `.opencode`
- models externs d'engram/memòria
- workflows SDD aliens

### Fase 5. Adaptació

**Objectiu:** Dissenyar una capa d'adaptació, no una fusió naïf.

**Inclou:**
- quines parts es poden absorbir
- quines parts queden com a auditor extern
- quines parts NO encaixen amb AgenticOS

### Fase 6. Consolidació

**Objectiu:** Unificar quan la classificació ja està clara.

**Inclou:**
- reducció de duplicacions
- flux únic de desenvolupament extern
- criteris clars per re-auditar specs existents

---

## 6. Dependències entre Objectius

| Objectiu | Depèn de | Motiu |
|---------|----------|-------|
| Refinar SDD + AGENTS + flows | - | És la capa de governança |
| Millorar context | Governança | El context ha de servir un flux ja definit |
| Millorar skills | Governança + context | Una skill sense contracte ni context és soroll |
| Mapar frameworks externs | Governança + skills | Cal saber què pot absorbir el sistema |
| Adaptar frameworks | Mapping previ | No es pot adaptar allò que no s'ha modelat |
| Unificar sistema | Totes les anteriors | La unificació és el resultat, no el punt de partida |

---

## 7. Política sobre Frameworks Externs

### 7.1 `gentle-ai`

**Estat actual recomanat:** Referència externa, no autoritat del flux base.

**Aprofitable ara:**
- model d'engram / memòria persistent
- capacitat d'auditar o enriquir specs
- idees de workflow complementari

**No fer encara:**
- fusionar el seu SDD amb el SDD base d'AgenticOS
- deixar que governi el flux principal
- migrar primitives del Kernel per acomodar-lo

### 7.2 `.opencode`

**Estat actual recomanat:** Entorn/harness extern compatible amb la capa de desenvolupament.

**Rol:**
- canal d'execució
- suport a recerca, context i auditoria externa
- possible contenidor d'integracions

### 7.3 Engram extern vs Engram runtime

**Regla:** No barrejar memòria de runtime amb memòria de desenvolupament extern sense contracte.

- `Engram runtime`: memòria del sistema AgenticOS
- `Engram extern`: memòria d'auditories, processos, millores de specs i integracions

---

## 8. Riscos i Conflictes

### R1. Importació prematura de frameworks
- **Risc:** més processos, més vocabularis, menys coherència
- **Resposta:** primer mapping, després adaptació

### R2. `AGENTS.md` hipertrofiat
- **Risc:** convertir regles de governança en un prompt monolític
- **Resposta:** `AGENTS.md` governa; els detalls viuen en documents especialitzats

### R3. Context-engine utilitzat com a crossa universal
- **Risc:** substitueix modelatge en lloc de complementar-lo
- **Resposta:** definir usos obligatoris i usos opcionals

### R4. Skills sense contracte
- **Risc:** sistema difícil d'auditar, reusar i combinar
- **Resposta:** taxonomia i contracte mínim abans de créixer

### R5. Arreglar flux extern tocant Ring 0
- **Risc:** dilució de la separació de poders
- **Resposta:** qualsevol millora d'aquesta capa s'implementa fora del Kernel

---

## 9. Què NO s'ha de tocar encara

- Kernel runtime
- context builder intern del runtime
- multi-seed / enterprise
- refactors de producció per acomodar frameworks externs
- reescriptura massiva de totes les specs abans d'acabar Fase 1-3

---

## 10. Criteri d'Èxit

La capa externa està ben definida quan:

- `AGENTS.md` i SDD deixen de contradir-se
- el `context-engine` té un paper explícit i limitat
- les skills tenen tipus i contracte
- `gentle-ai` i altres marcs passen a ser complements modelats
- es pot re-auditar una spec sense tocar el Kernel

---

## 11. Següent Pas

Després d'aquest document, el següent pas obligatori és:

1. normalitzar governança (`AGENTS.md` + `SDD_GUIDE.md`)
2. definir taxonomia de skills
3. fer mapa d'integració de frameworks externs

Només després es decideix quina part d'aquests marcs entra com a complement real.
