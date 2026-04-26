# Spec Re-Audit Lot A

> **Data:** 2026-04-04
> **Lot:** A
> **Specs:** `feat-001-kernel-core`, `feat-008-context-builder`
> **Abast:** Auditoria interna estructural amb lectura directa i fallback documental

---

## 1. Context Operatiu

- s'ha intentat cerca semàntica prèvia amb `04_tools/context.ps1`
- la cerca ha fallat per incidència d'entorn:
  - `proxyconnect tcp: dial tcp 127.0.0.1:9`
- per tant aquesta ronda s'ha fet amb:
  - lectura directa
  - cerca textual
  - contrast de spec + design + task + feature record

---

## 2. `feat-001-kernel-core`

### Estat general

La spec és funcionalment forta i continua sent una bona primitive base, però arrossega traçabilitat documental antiga.

### Findings interns

1. **Desalineació de task reference**
   - el feature record no declarava `task_path`
   - el task file existent apuntava a `/specs/feat-001.md`, que no és el nom canònic actual
   - s'ha afegit `task_path` al feature record i s'ha corregit el task file

2. **Tensió entre MVP seqüencial i escenari de concurrència**
   - la spec fixa `1 worker` per v0.1
   - alhora manté SDT específic de dos workers simultanis
   - això és defensable com a prova d'atomicitat del router, però s'hauria d'explicar millor com a test de competició controlada, no com a model operatiu normal

3. **Disc full retry no està prou lligat a un contracte superior**
   - la spec introdueix `reintent automàtic cada 60s (fins 3 intents)`
   - però no defineix qui governa aquest retry ni com es reflecteix al ticket

### Valoració

- **Coherència funcional:** alta
- **Traçabilitat documental:** mitjana
- **Risc de reimplementació accidental:** baix

### Recomanació

- no reimplementar res
- considerar `feat-001` com a spec madura amb traçabilitat normalitzada
- deixar només pendent una explicació més explícita del cas de concurrència com a prova d'atomicitat, si es vol polir la narrativa

---

## 3. `feat-008-context-builder`

### Estat general

Aquesta spec era la més exposada a incoherències documentals dins del Lot A, però ara queda tancada com a cas normalitzat.

### Findings interns

1. **Estat de spec desalineat**
   - la spec deia `Estat: SPEC`
   - el feature record deia `DONE`
   - s'ha normalitzat la spec a `DONE`

2. **Design reference inconsistent**
   - la spec referenciava `01_design/08_CONTEXT_BUILDER.md`
   - aquest path no existia al repo actual
   - s'ha corregit al document canònic `SDD/design/feat-008-context-builder.md`

3. **Task file desalineat respecte a realitat**
   - el task file estava `PENDING`
   - el feature record declarava implementació completa, validada i auditada
   - a més referencia `SDD/specs/feat-008.md`, que no és el nom real del fitxer canònic
   - s'ha reescrit com a traça històrica alineada

4. **Inconsistència sobre nombre de capes**
   - context i goals parlaven de 5 capes
   - `RF-01` enumerava 4 capes i ometia `Tools`
   - el resum del feature record tornava a parlar de 5 capes
   - s'ha resolt el contracte: 5 capes conceptuals, `tools` com a canal separat

5. **System prompt base no està unificat**
   - el design mostrava un system prompt base
   - la spec en mostrava un altre, més rígid i orientat a sortida JSON
   - això no era només redacció diferent; era contracte diferent
   - s'ha unificat la lectura documental amb el runtime existent

### Valoració

- **Coherència funcional:** alta
- **Traçabilitat documental:** alta
- **Risc de relectura incorrecta:** baix

### Recomanació

- no reimplementar ara
- considerar `feat-008` com a cas tancat per traçabilitat documental
- usar aquest cas com a patró de normalització per a futures specs
- resoldre abans de qualsevol extensió important:
  - estat real de la spec
  - design path canònic
  - task file com a legacy o com a document a migrar
  - contracte final de capes
  - versió canònica del system prompt base

---

## 4. Resultat del Lot A (intern)

### Adoptar ara

- tractar `feat-001` com a spec madura amb traçabilitat ja normalitzada
- tractar `feat-008` com a spec central ja normalitzada i tancada

### Adaptar després

- quan s'usi `gentle-ai`, aplicar-lo a `feat-001` per pressionar edge cases i contracte de lifecycle
- després usar `feat-008` com a benchmark de normalització documental

### No fer encara

- no reobrir implementació del Kernel
- no forçar migració massiva de tasks
- no barrejar aquesta re-auditoria amb runtime fixes del `context-engine`

---

## 5. Conclusió

El Lot A confirma dues coses:

1. el sistema documental ja està prou sanejat per detectar problemes reals i no només soroll
2. `feat-008` ha passat de ser un cas crític a un patró tancat de normalització
