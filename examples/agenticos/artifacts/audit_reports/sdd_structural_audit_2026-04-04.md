# SDD Structural Audit

**Data:** 2026-04-04  
**Tipus:** Auditoria estructural de governança SDD  
**Abast:** `AGENTS.md`, `SDD/README.md`, `SDD_GUIDE.md`, `SDD_FEATURE_FORMAT.md`, `features_for_specs/`, `design/`, `specs/`, `tasks/`  
**Objectiu:** detectar incoherències que degraden el flux extern de qualitat

---

## Resum Executiu

L'SDD actual és funcional però **no està normalitzat**. El problema no és que falti documentació; el problema és que conviuen diverses versions del model.

### Resultat global

**Resultat:** WARN  
**Risc:** Mitjà-Alt a nivell de procés  
**Impacte:** El sistema és usable per a qui ja coneix el projecte, però és ambigu per a automatització, integració externa i re-auditories sistemàtiques.

### Diagnòstic curt

Hi ha quatre tensions estructurals:

1. **Divergència de pipeline**
2. **Divergència d'esquemes de `features_for_specs/*.json`**
3. **Desalineació entre `features`, `specs`, `tasks` i nomenclatura**
4. **Model híbrid no explicitat fins ara (`prompts + skills`)**

Les tres primeres afecten directament el flux SDD. La quarta ja ha començat a quedar resolta amb la nova capa documental creada el 2026-04-04.

---

## Findings

### F-001. Pipeline simplificat vs pipeline complet

**Severitat:** Alta

**Evidència**

- `SDD/README.md` defineix un pipeline simplificat: `DESIGN -> SPEC -> VALIDATION -> DONE`
- `SDD_GUIDE.md` defineix un pipeline complet: `DESIGN -> SPEC -> VALIDATION -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE -> DONE`

**Impacte**

- no queda clar quin pipeline governa realment el sistema
- l'automatització externa pot tancar massa aviat una feature a `DONE`
- es desdibuixa la frontera entre aprovació de spec i feature realment completada

**Decisió recomanada**

- mantenir el pipeline complet com a model canònic
- deixar el pipeline curt només com a vista resumida, no com a contracte normatiu

---

### F-002. Enumeració d'estats del `SDD_FEATURE_FORMAT` no alineada amb el guide

**Severitat:** Alta

**Evidència**

`SDD_FEATURE_FORMAT.md` enumera:

- `DESIGN, IMPACT, SDT, SPEC, AUDIT, TASKS, VALIDATION, DONE`

Però `SDD_GUIDE.md` treballa amb:

- `DESIGN, SPEC, VALIDATION, IMPLEMENT, VERIFY, AUDIT, ARCHIVE, DONE`

**Impacte**

- dos models d'estat diferents dins del mateix sistema
- impossibilitat de validar JSONs de feature amb un únic esquema coherent
- confusió sobre si `TASKS`, `IMPACT`, `SDT`, `IMPLEMENT`, `VERIFY` i `ARCHIVE` són estats o artefactes/fases auxiliars

**Decisió recomanada**

- triar un únic conjunt d'estats canònics
- relegar `IMPACT`, `SDT`, `TASKS` a camps o artefactes, no a estats, si aquest és el model real

---

### F-003. `DONE` s'està fent servir amb semàntiques diferents

**Severitat:** Alta

**Evidència**

- a `README.md`, `DONE` sembla significar "spec aprovada"
- a `SDD_GUIDE.md`, `DONE` significa "feature completada, auditada i arxivada"
- a `AGENTS.md` es diu: "feature ja especificada (`specs/*.md` estat `DONE`)"

**Impacte**

- el mateix estat representa dos moments diferents del procés
- risc de començar implementació sobre un `DONE` que només vol dir "spec validada"
- debilita qualsevol auditoria automàtica

**Decisió recomanada**

- separar explícitament:
  - `SPEC_DONE` lògic o equivalent documental
  - `FEATURE_DONE` com a final del cicle

O bé:

- mantenir `DONE` només per al final real
- i usar `VALIDATION: PASS` + `task_list` per indicar "spec llesta per implementar"

---

### F-004. `features_for_specs/*.json` no segueixen un únic esquema

**Severitat:** Crítica

**Evidència**

Exemples observats:

- `feat-006.json` usa camps compostos com `backend_spec_path`, `backend_design_path`, `backend_tasks_path`
- `feat-015.json` està a `DONE` però gairebé només conté paths i `sdt_scenarios`
- `feat-017.json` té `type: TOOL_SPEC` i estat `IMPLEMENTING`
- `feat-017-react-loop.json` no segueix l'esquema general: usa `name`, `description`, `priority` i ni tan sols té `type` o `title`
- `feat-009.json` apunta el `design_path` a una secció dins `01_design/01_KERNEL.md`, no a `SDD/design/...`

**Impacte**

- el format de feature no és validable de forma robusta
- la governança no pot saber què és "normal" i què és excepcional
- qualsevol integració externa haurà de programar excepcions per casos especials

**Decisió recomanada**

- definir un esquema canònic mínim obligatori
- classificar les excepcions actuals:
  - compostes
  - legacy
  - incompletes
  - fora d'esquema

---

### F-005. Existeixen fitxers orfes o nomenclatures desalineades entre `tasks/` i la resta

**Severitat:** Alta

**Evidència**

- `tasks/dashboard-backend.md` encara existeix amb referències a `SDD/specs/dashboard-backend.md` i `SDD/design/dashboard-backend.md`
- però el sistema actual parla de `feat-006-api-server.md`
- diverses tasks usen noms curts (`feat-001.md`, `feat-002.md`, `feat-006.md`) mentre `design/` i `specs/` usen noms descriptius (`feat-001-kernel-core.md`, etc.)

**Impacte**

- la traçabilitat entre design/spec/task no és directa
- obliga a coneixement tribal per saber què correspon a què
- afegeix fricció a auditories i eines externes

**Decisió recomanada**

- normalitzar la relació entre `task` i `spec`
- decidir si `tasks/` seguirà:
  - nom curt per `id`
  - o nom descriptiu complet

Però no una barreja dels dos.

---

### F-006. Features compostes i dobles identificadors no modelats formalment

**Severitat:** Alta

**Evidència**

- `feat-006` representa alhora frontend dashboard i backend API
- `feat-017` existeix en dues versions: `feat-017.json` i `feat-017-react-loop.json`

**Impacte**

- el sistema no sap distingir "feature composta" de "feature duplicada" o "subfeature"
- això contamina planning, estat i auditoria

**Decisió recomanada**

- introduir explícitament un model per:
  - `feature composta`
  - `subfeature`
  - `legacy record`

Sense això, cada cas especial trencarà l'esquema.

---

### F-007. Estat `IMPLEMENTING` i tipus `TOOL_SPEC` apareixen fora del format canònic

**Severitat:** Mitjana-Alta

**Evidència**

- `feat-017.json` usa `state: IMPLEMENTING`
- `feat-017.json` usa `type: TOOL_SPEC`
- `SDD_FEATURE_FORMAT.md` només defineix `SYSTEM_SPEC`

**Impacte**

- l'ontologia de documents no està tancada
- no queda clar si hi ha més d'un tipus de feature formal

**Decisió recomanada**

- o bé ampliar formalment el model (`SYSTEM_SPEC`, `TOOL_SPEC`, etc.)
- o bé eliminar aquests casos fora d'esquema

---

### F-008. El sistema híbrid `prompts + skills` no estava explicitat

**Severitat:** Mitjana

**Evidència**

- `prompts/designer.md`, `prompts/specifier.md`, `prompts/validator.md` governen el procés base
- `skills/` només conté `sdd-audit` i `sdd-deep-audit`

**Impacte**

- fàcil confondre "tenir poques skills" amb "tenir poc sistema"
- un framework extern més empaquetat sembla més madur del que és

**Estat**

Aquest finding ja ha començat a quedar mitigat amb:

- `SKILLS_TAXONOMY.md`
- `SKILLS_INVENTORY.md`
- `PROMPT_VS_SKILL_POLICY.md`

---

## Ordre Recomanat de Correcció

### Fase A. Normalització de governança

1. Declarar el `SDD_GUIDE.md` com a model canònic de pipeline
2. Reescriure `SDD/README.md` perquè no contradigui el guide
3. Fixar el significat únic de `DONE`

### Fase B. Normalització del format de feature

4. Reescriure `SDD_FEATURE_FORMAT.md` segons el pipeline real
5. Definir model formal per excepcions:
   - feature composta
   - subfeature
   - legacy record
   - tipus de spec addicionals

### Fase C. Sanejament de `features_for_specs/`

6. Classificar cada JSON existent:
   - canònic
   - incomplet però recuperable
   - legacy
   - fora d'esquema
7. Normalitzar primer els casos crítics:
   - `feat-006.json`
   - `feat-017.json`
   - `feat-017-react-loop.json`
   - `feat-009.json`
   - `feat-015.json`

### Fase D. Traçabilitat entre artefactes

8. Normalitzar la convenció de noms a `tasks/`
9. decidir què fer amb `dashboard-backend.md`

---

## Què NO s'ha de tocar encara

- runtime del Kernel
- implementació Go
- context builder intern
- multi-seed
- integració operativa de `gentle-ai`

Aquestes incoherències són de governança SDD i s'han de tancar fora del Kernel.

---

## Veredicte Final

L'SDD d'AgenticOS és potent però **massa permissiu estructuralment**.

Ara mateix el sistema funciona perquè hi ha coneixement implícit del projecte.  
Si es vol portar a:

- auditoria externa seriosa
- re-auditoria sistemàtica de specs
- integració amb `gentle-ai` com a complement
- automatització més fiable del flux extern

cal primer normalitzar pipeline, estats i esquemes de feature.

**Recomanació:** iniciar Fase A immediatament abans d'intentar re-auditories a escala.
