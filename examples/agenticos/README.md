# SDD - Spec-Driven Development per a AgenticOS

Aquesta carpeta conte els artefactes i la metodologia per gestionar el desenvolupament basat en especificacions.

## Pipeline canonic

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

1. **DESIGN**: defineix que s'implementa
2. **SPEC**: defineix com ho fa i quins escenaris s'han de validar
3. **VALIDATION**: comprova que la spec es implementable
4. **TASKS**: desglossament minim i ordenat del treball
5. **IMPLEMENT**: execucio segons tasks i TDD/SDT
6. **VERIFY**: comprovacio contra spec i escenaris
7. **AUDIT**: auditoria lleugera, profunda o re-auditoria
8. **ARCHIVE**: consolidacio documental

La fase `VALIDATION` no implica que la feature estigui acabada. Nomes implica que la spec ja es apta per implementar.

## Contracte operatiu

La font operativa i executable per agents es:

- `00_core/SDD_RUNTIME.md`
- `00_core/SDD_READING_CONTRACT.md`
- `00_core/SDD_HANDOFF_CONTRACT.md`

El document complet de metodologia (mes llarg) es:

- `00_core/SDD_GUIDE.md`

## Relacio entre governanca i prompts

Els fitxers de `prompts/` son **ajudes operatives** del flux SDD.

No son la font de veritat del sistema.

La font de veritat continua sent:

- `00_core/SDD_RUNTIME.md`
- `00_core/SDD_GUIDE.md`
- `00_core/AGENT_DECISION_TABLE.md`
- `03_operations/WORKFLOW.md`
- `03_operations/SPEC_REAUDIT_WORKFLOW.md`
- la cadena `feature record -> design -> spec -> tasks`

Si un prompt entra en contradiccio amb aquesta governanca, s'ha d'arreglar el prompt, no la governanca.

## Contingut

- `00_core/`: contractes i governanca base (inclou `SDD_RUNTIME.md`)
- `01_execution/prompts/`: prompts per rols/fases del flux
- `01_execution/skills/`: skills (sobretot d'auditoria) amb contracte
- `02_policies/`: normes (context, skills, frameworks)
- `03_operations/`: workflows operatius (intake, discovery, gap detection, etc.)
- `90_transitional/`: documents no canònics / legacy (NO font de veritat)
- `templates/`: plantilles de documents
- `artifacts/features_for_specs/`: estat i tracabilitat de features
- `artifacts/design/`: documents de disseny
- `artifacts/specs/`: especificacions aprovades o en progres
- `artifacts/tasks/`: llistes de treball
- `audit_reports/`: informes d'auditoria i re-auditoria

## Quick start

1. Crear o localitzar `artifacts/features_for_specs/<feature>.json`
2. Escriure o revisar `artifacts/design/<feature>.md`
3. Escriure o revisar `artifacts/specs/<feature>.md`
4. Generar o confirmar `artifacts/tasks/<feature>.md`
5. Consultar `00_core/SDD_RUNTIME.md` per executar el flux

## Principis

- **Spec as source of truth**: no hi ha comportament de producte sense spec
- **No ambiguity**: termes vagues impliquen spec incompleta
- **Edge cases first**: els limits i fallbacks s'han d'explicitar
- **No contract drift**: els canvis de contracte tornen a spec/design

## Capa externa del Kernel

L'SDD no viu aillat. El desenvolupament extern del Kernel es governa tambe amb:

- `03_operations/ROADMAP.md`
- `03_operations/WORKFLOW.md`
- `02_policies/CONTEXT_INTEGRATION_POLICY.md`
- `02_policies/SKILLS_SYSTEM.md`
- `02_policies/FRAMEWORK_INTEGRATION_MAP.md`
- `02_policies/LEGACY_SPECS_POLICY.md`
- `03_operations/TASKS_NORMALIZATION_POLICY.md`

Aquest conjunt defineix com evolucionar el sistema des de fora sense barrejar governanca externa amb runtime del Kernel.
