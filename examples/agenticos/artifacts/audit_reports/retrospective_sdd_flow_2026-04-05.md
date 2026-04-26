# Retrospectiva de Flux SDD

**Data:** 2026-04-05  
**Lot / Features:** `feat-018`, `feat-020`  
**Objectiu del lot:** validar si el flux SDD real d’AgenticOS aguanta tant en una feature ja especificada com en una peça que surt del `parking lot` i s’ha de madurar abans.

## 1. Tipus de peces

- `feat-018`: peça ja especificada
- `feat-020`: peça pujada des de `parking lot` a SDD formal

## 2. Què ha funcionat bé

- El flux respon bé quan la peça entra amb `design/spec/tasks` clars.
- OpenCode en `plan/build` ha seguit millor el procés que no pas un mode més “sobirà”.
- El pas `parking lot -> design/spec/tasks -> implementació` ha funcionat sense forçar.
- L’auditoria externa posterior ha aportat valor com a crítica de definició i cobertura, no com a substitut del flux.

## 3. On hi ha hagut fricció

- El `context-engine` encara no és una font fiable de descobriment per a preguntes abstractes; la base real ha continuat sent lectura directa + runtime.
- Alguns punts del runtime/API encara tenen rigidesa de testabilitat.
- Hi ha risc de solapament quan una peça toca fitxers del `ticket spine`.
- Sense prompts directrius, encara no està clar fins a quin punt el flux aguanta igual de bé.

## 4. Resultat per peça

### `feat-018`

- **Estat final:** implementada i validada
- **Tests:** passen els tests nous rellevants
- **Auditoria:** `COMPLIANT` amb warnings no blockings
- **Notes:** bona prova d’una feature que ja entrava madura; els findings externs han estat útils sobretot en buits de spec i gaps de tests

### `feat-020`

- **Estat final:** pujada a SDD, implementada amb tall mínim i validada
- **Tests:** tests nous passant; failures restants preexistents i fora d’abast
- **Auditoria:** encara no necessària immediatament
- **Notes:** molt bona prova del camí `parking lot -> SDD -> implementació`; ha quedat un gap petit de testabilitat (`getBaseDir` injectable) però no bloquejant

## 5. Lliçons sobre el flux

- El flux SDD funciona millor amb peces petites, acotades i amb frontera clara.
- No cal tenir tota l’arquitectura tancada per avançar; cal només no entrar en peces que obrin drift.
- `gentle-ai`/`sdd-orchestrator` aporta més valor com a auditor extern que com a executor principal, almenys ara.
- El `ticket` s’ha de tractar com a spine/runtime, no com a banc principal per validar metodologia.
- Hi ha dos camins vàlids de prova del flux:
  - feature ja especificada
  - peça que necessita ser madurada des del backlog

## 6. Decisions

- **Continuar igual en:**
  - ús d’OpenCode en `plan/build` per execució
  - auditoria externa només després, com a contrast
  - selecció de peces petites i no crítiques per provar el flux
- **Ajustar:**
  - anotar millor gaps de testabilitat quan apareguin
  - definir més endavant proves específiques de qualitat del `context-engine`
- **Aparcar:**
  - integració activa de `gentle-ai` dins el loop principal
  - peces que toquin `SEC/HITL`, `Session/Engram/Context`, `LLM providers`, `multi-seed`
- **Derivar al fil d’arquitectura:**
  - contracte de traça d’execució vs visualització en flows
  - frontera observability / session tree / context / memòria

## 7. Següent pas recomanat

- fer una tercera peça de prova només si és igual de petita i no entra en frontera grossa
- si no apareix una bona peça, fer una ronda curta de normalització documental del que hem après
- mantenir el fil d’arquitectura treballant fronteres, però sense bloquejar el flux per debat teòric

## Conclusió

El flux SDD no només “sembla” funcionar: ja ha aguantat dues rondes reals diferents. Encara depèn de disciplina i de bones peces d’entrada, però ja no estem validant una idea; estem validant un procediment operatiu.
