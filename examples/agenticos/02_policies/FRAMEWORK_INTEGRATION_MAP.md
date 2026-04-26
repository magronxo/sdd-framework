# Framework Integration Map

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** `gentle-ai`, `.opencode`, models d'engram extern i workflows complementaris

---

## 1. Propòsit

Aquest document no integra frameworks externs. Els **modela** abans de decidir si s'aprofiten, s'aïllen o es descarten.

La regla és simple:

**Primer entendre. Després adaptar. Mai importar a cegues.**

---

## 2. Criteri d'Avaluació

Cada framework extern es valora segons:

1. **Compatibilitat filosòfica** amb el Manifest
2. **Compatibilitat operativa** amb l'SDD propi
3. **Valor real** per al desenvolupament extern del Kernel
4. **Risc de contaminació** del flux base
5. **Necessitat de migració interna** al Kernel

---

## 3. Matriu Inicial

| Sistema extern | Valor principal detectat | Compatibilitat | Risc principal | Decisió actual |
|---------------|--------------------------|----------------|----------------|----------------|
| `gentle-ai` | Engram, auditories, enriquiment de specs, ecosistema agentic | Mitjana | Voler substituir el flux base | **Referència externa** |
| `.opencode` | Harness/entorn d'execució extern, skills i auditories | Alta | Solapament amb regles locals si no es delimita | **Canal compatible** |
| Engram extern | Memòria de millores, decisions, auditories | Alta si es separa del runtime | Barreja de memòries | **Modelar separat** |

---

## 4. `gentle-ai`

### 4.1 Què és valuós

- model d'ecosistema agentic extern
- memòria persistent tipus engram
- capacitat de complementar o pressionar specs
- visió d'auditoria i workflow enriquit

### 4.2 Què NO s'ha d'absorbir ara

- la seva governança completa
- el seu SDD com a font de veritat principal
- qualsevol patró que exigeixi tocar el Kernel per encaixar-hi

### 4.3 Rol recomanat

`gentle-ai` s'ha de tractar com:

- **auditor/complement**
- **font d'idees de memòria externa**
- **motor de relectura crítica de specs** un cop el flux base sigui coherent

### 4.4 Regla

**`gentle-ai` pot complementar el teu SDD. No el substitueix.**

---

## 5. `.opencode`

### 5.1 Què és valuós

- entorn extern d'operació agentica
- possible suport per orquestració, recerca i skills
- encaix natural amb una capa fora del Kernel

### 5.2 Rol recomanat

`.opencode` es pot fer servir com:

- contenidor/harness d'eines externes
- canal d'auditoria i context
- entorn on provar integracions sense comprometre el runtime

### 5.3 Regla

**`.opencode` és infraestructura de treball extern, no política arquitectònica del Kernel.**

---

## 6. Engram com a component extern

### 6.1 Problema

El terme "engram" ja existeix dins d'AgenticOS com a memòria runtime. Si s'adopta un model extern d'engram sense separar dominis, el sistema es torna ambigu.

### 6.2 Decisió

Separar dues categories:

- **Engram Runtime**
  - decisions, errors i aprenentatges del sistema AgenticOS
  - consumit pel runtime i pels seus components

- **Engram de Desenvolupament**
  - millores de specs
  - auditories externes
  - decisions de governança
  - comparatives entre marcs externs

### 6.3 Regla

**Mateix concepte, domini diferent. No compartir repositori lògic sense contracte.**

---

## 7. Estratègia de Futur

### Ara

- no desinstal·lar `gentle-ai` per reflex
- no integrar-lo dins el flux base
- mantenir-lo com a referència externa

### Després de Fase 1-3

- usar-lo per re-auditar specs madures
- comparar troballes amb l'auditoria pròpia
- extreure patrons útils del seu engram

### Molt més endavant

- valorar si alguna part concreta mereix adaptador estable
- només si no força canvis dins del Kernel

---

## 8. Senyals de Perill

Atura la integració si passa qualsevol d'aquestes coses:

- cal reescriure el teu SDD per semblar-se al d'un framework extern
- una eina externa comença a dictar el comportament del Kernel
- no queda clar si una memòria és de runtime o de desenvolupament
- una skill externa entra sense contracte ni límits

---

## 9. Decisió Operativa Actual

**Decisió 2026-04-04:**

- `gentle-ai`: mantenir com a complement extern i eina de comparació
- `.opencode`: acceptable com a infraestructura externa de treball
- Engram extern: modelar-lo com a memòria de desenvolupament, no de runtime

No es fa cap migració interna al Kernel en aquesta fase.
