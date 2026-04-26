# Gentle AI Adoption Policy

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** Ús de `gentle-ai` com a complement extern de qualitat

---

## 1. Propòsit

Aquest document fixa com s'ha d'aprofitar `gentle-ai` dins d'AgenticOS sense convertir-lo en el sistema rector del flux.

La premissa és:

**`gentle-ai` és útil, però no és la font de veritat del projecte.**

---

## 2. Decisió Central

`gentle-ai` s'adopta com a:

- complement extern de qualitat
- font de comparació de workflow
- suport de memòria externa / engram
- eina de re-auditoria de specs

No s'adopta com a:

- substitut del SDD base
- governança principal
- motor de decisions dins del Kernel

---

## 3. Valor Detectat

Segons l'experiència observada al projecte, `gentle-ai` ha demostrat valor sobretot en:

- trobar millores no òbvies a specs
- pressionar qualitat de definició
- aportar un model d'engram/memòria interessant

Això el fa valuós en fases de:

- revisió de qualitat
- contrast entre marcs
- relectura de specs madures

---

## 4. Moment Correcte d'Adopció

### Ara

Ús permes:

- com a referència externa
- com a comparador conceptual
- com a input per definir criteris de qualitat

Ús no recomanat encara:

- integrar-lo al flux base diari
- deixar que intervingui en cada feature
- fusionar el seu model d'engram amb el runtime d'AgenticOS

### Després de Fase 1-3

Ús recomanat:

- re-auditar specs importants
- comparar resultats d'auditoria pròpia vs externa
- extreure patrons útils de memòria i qualitat

### Més endavant

Només si el flux base és estable:

- dissenyar un adaptador estable
- definir protocols d'entrada/sortida
- aïllar el seu engram com a memòria de desenvolupament extern

---

## 5. Modes d'Ús Autoritzats

### Mode A. Referència

S'utilitza `gentle-ai` per entendre un patró o una capacitat, però no es trasllada directament al sistema.

### Mode B. Auditor extern

S'utilitza per revisar una spec o conjunt de specs i generar suggeriments o observacions.

### Mode C. Comparador

S'utilitza per comparar:

- qualitat de spec
- exhaustivitat de riscos
- cobertura de casos límit

### Mode D. Font d'idees de memòria

S'utilitza per inspirar una memòria externa de desenvolupament, separada del runtime.

---

## 6. Modes No Autoritzats per Ara

- integrar-lo dins del cicle principal de cada feature
- assumir que la seva estructura substitueix l'SDD propi
- reutilitzar el seu engram directament com a engram runtime
- redissenyar `AGENTS.md` perquè s'hi adapti
- tocar el Kernel per acomodar-lo

---

## 7. Regla d'Or

Si `gentle-ai` troba millores bones, aquestes:

1. s'analitzen
2. es tradueixen al model documental propi
3. s'incorporen només si encaixen amb el Manifest i amb l'SDD base

**No s'importen literalment.**

---

## 8. Relació amb l'Engram

### Engram de `gentle-ai`

Es considera:

- memòria externa de desenvolupament
- material de revisió i comparació

### Engram d'AgenticOS

Es considera:

- memòria runtime del sistema
- part del producte

**Regla:** no unir aquests dos dominis sense adaptador explícit.

---

## 9. Workflow Recomanat de Futur

Quan la base estigui madura, el workflow recomanat és:

1. crear o revisar spec amb el flux SDD propi
2. validar internament
3. passar auditoria pròpia
4. opcionalment re-auditar amb `gentle-ai`
5. comparar diferències
6. incorporar només les millores que encaixin

---

## 10. Criteri d'Èxit

La relació amb `gentle-ai` és correcta quan:

- millora qualitat sense desplaçar la governança pròpia
- troba buits reals en specs
- no obliga a redissenyar el flux base
- la seva memòria queda separada del runtime

---

## 11. Decisió Operativa Actual

Des de 2026-04-04:

- `gentle-ai` es manté present com a complement extern
- no es desinstal·la per reflex
- no entra al camí crític del flux base
- es reserva especialment per a re-auditoria i comparativa de specs
