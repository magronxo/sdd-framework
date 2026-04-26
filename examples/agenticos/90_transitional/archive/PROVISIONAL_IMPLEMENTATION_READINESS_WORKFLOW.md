STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

# ARCHIVE HEADER
STATUS: ARCHIVED
AUTHORITY: NON-CANONICAL
ARCHIVED_AT: 2026-04-09
ARCHIVE_REASON: Provisional workflow; superseded by PRE-SDD runtime + prompts.
CANONICAL_SUCCESSOR: `00_project_documentation/SDD/03_operations/pre_sdd/PRE_SDD_RUNTIME.md`

This document is provisional workflow support. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# PROVISIONAL Implementation Readiness Workflow

> **Estat:** Provisional  
> **Data:** 2026-04-05  
> **Abast:** Triage previ a design/spec per preparar implementacions reals des del `parking lot`  
> **Nota:** Aquest document és temporal. S'ha de revisar, absorbir o eliminar quan el procediment s'hagi validat amb iteracions reals.

---

## 1. Propòsit

Aquest workflow defineix una capa curta de preparació abans d'entrar a
`design -> spec -> tasks -> implement`.

No substitueix l'SDD. El que fa és evitar entrar a spec amb peces:

- massa difuses
- mal delimitades
- recolzades en disseny legacy no validat
- o amb dependències encara no resoltes

La idea és simple:

**Abans d'especificar, aclarir si la peça realment està llesta per ser especificada.**

---

## 2. Quan s'ha d'usar

Fer servir aquest workflow quan:

- una peça surt del `parking lot`
- hi ha dubte entre aprofitar disseny existent o redissenyar
- la part a implementar toca més d'un document o component
- el runtime actual i la documentació poden no estar alineats
- es vol provar el flux real amb lots implementables i no amb idees borroses

No cal usar-lo quan:

- la peça ja té design vigent, spec clara i dependències tancades
- el canvi és local i inequívoc

---

## 3. Principi Rector

No tota idea del `parking lot` està preparada per entrar a SDD formal.

Abans, cal resoldre tres preguntes:

1. **Què és exactament aquesta peça?**
2. **On viu de debò?**
3. **Està prou tancada per merèixer spec?**

---

## 4. Inputs Mínims

Per cada peça triada del `parking lot`, llegir com a mínim:

- document o nota on apareix la peça
- documentació de disseny relacionada
- artifacts SDD relacionats, si existeixen
- estat real de `02_implementation/`, si ja hi ha runtime parcial

Si la peça és transversal o ambigua, és recomanat:

- usar lectura dirigida de documents
- usar `context.ps1 search "..."` només com a suport de descoberta
- confirmar sempre amb lectura directa

---

## 5. Preguntes de Triage

Per considerar una peça preparada, s'han de poder respondre aquestes preguntes.

### 5.1 Identitat

- quin problema resol exactament?
- quin és el resultat observable esperat?
- quin és el tall mínim implementable?

### 5.2 Domini correcte

- això és governança?
- és flux extern del Kernel?
- és runtime?
- és eina o infraestructura auxiliar?

**Regla:** si el problema és extern, no s'ha d'empènyer cap a Ring 0.

### 5.3 Font de veritat actual

- quin document la defineix avui?
- aquest document és vigent, legacy o només baseline?
- hi ha contradicció entre documents?
- hi ha contradicció entre documents i runtime?

### 5.4 Dependències

- de quines peces depèn?
- bloqueja alguna altra part més nuclear?
- es pot implementar sense obrir una cascada de redefinicions?

### 5.5 Estat de disseny

- el disseny actual encara serveix?
- s'ha d'aprofitar parcialment?
- s'ha de reobrir arquitectònicament abans de spec?

---

## 6. Classificació de Sortida

Cada peça ha d'acabar en una d'aquestes categories:

### `implementar tal com està`

Quan:

- el disseny és prou bo
- el domini està clar
- les dependències són assumibles
- el tall implementable és net

### `re-dissenyar abans d'especificar`

Quan:

- el disseny actual és ambigu, legacy o contradictori
- la peça encara no té frontera clara
- hi ha decisions arquitectòniques obertes que farien la spec artificial

### `aparcar`

Quan:

- depèn d'una altra peça encara no tancada
- és massa gran o massa transversal per a la ronda actual
- hi ha massa incertesa per produir una spec útil

---

## 7. Output Esperat

Per cada peça triada, el triatge ha de deixar una fitxa curta amb:

- `piece_id`
- `problem`
- `domain`
- `source_of_truth`
- `runtime_status`
- `design_status`
- `dependencies`
- `decision`
- `next_step`

---

## 8. Ordre Operatiu Recomanat

Per cada ronda:

1. triar 5-8 peces candidates del `parking lot`
2. fer triatge curt de cadascuna
3. reduir-les a 2-3 peces màxim per treball actiu
4. només aquestes entren a `design/spec/tasks`
5. executar una ronda curta d'implementació
6. fer retrospectiva del flux

---

## 9. Què s'ha d'observar en la prova

Aquest workflow no només serveix per preparar feina. Serveix per validar el flux.

Cal observar:

- si el pas cap a `design/spec` surt natural o forçat
- si hi ha massa dependència de prompts directrius
- si el context necessari és fàcil de localitzar
- si les tasks resulten accionables de veritat
- si l'auditoria posterior genera soroll o valor
- si hi ha friccions repetibles entre docs, runtime i eines

---

## 10. Relació amb la Governança Vigent

Aquest document complementa temporalment:

- `SDD_GUIDE.md`
- `EXTERNAL_KERNEL_DEVELOPMENT.md`
- `CONTEXT_INTEGRATION_POLICY.md`
- `SPEC_REAUDIT_WORKFLOW.md`

No els substitueix.

Si el procediment es valida en iteracions reals, llavors:

- s'integra al document canònic adequat
- o es reparteix entre checklist, workflow i guia SDD

Si no es valida:

- s'elimina sense arrossegar soroll estructural

---

## 11. Criteri d'Èxit

Aquest document haurà servit si aconsegueix:

- reduir entrada borrosa a SDD
- separar millor disseny vigent de disseny legacy
- prioritzar peces implementables de debò
- fer més fiable la prova del flux real

---

## 12. Condició de Caducitat

Aquest document és explícitament **provisional**.

S'ha de revisar quan passi una d'aquestes coses:

- després de 2-3 rondes reals d'ús
- si el procediment es consolida i mereix absorció canònica
- si es demostra redundant o inútil

La seva existència no és permanent.
