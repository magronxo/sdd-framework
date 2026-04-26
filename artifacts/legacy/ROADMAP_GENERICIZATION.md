# Roadmap: Conversió a SDD Framework Genèric

> **Nom:** `sdd-framework`
> **Format de configuració:** JSON
> **Decisions operatives:**
> - Backup: ✅ fet (`K:\SDD_project_BACKUP_2026-04-23`)
> - Visual Overview: de moment només a `examples/agenticos/`
> - Script d'inicialització: SÍ, amb **contingut complet** (no fitxers buits)
> - Prompts: genèrics amb placeholders clars

---

## 0. Preparació (no es toca codi de negoci)

- [x] Backup complet de `K:\SDD_project`
- [x] Crear estructura `examples/agenticos/`
- [x] Moure **TOT** el contingut actual a `examples/agenticos/`
- [x] Verificar integritat de l'arxivat

**Nota:** La estratègia és "moure primer, reescriure després". Així conservem sempre la referència exacta del sistema original.

---

## 1. Arxivat del Contingut Actual

Moure fitxers i carpetes existents a `examples/agenticos/`:

- [x] `00_core/` → `examples/agenticos/00_core/`
- [x] `01_execution/` → `examples/agenticos/01_execution/`
- [x] `02_policies/` → `examples/agenticos/02_policies/`
- [x] `03_operations/` → `examples/agenticos/03_operations/`
- [x] `90_transitional/` → `examples/agenticos/90_transitional/`
- [x] `artifacts/` → `examples/agenticos/artifacts/`
- [x] `templates/` → `examples/agenticos/templates/`
- [x] `AGENTS.md` → `examples/agenticos/AGENTS.md`
- [x] `README.md` → `examples/agenticos/README.md`
- [x] `SDD_VISUAL_OVERVIEW.md` → `examples/agenticos/SDD_VISUAL_OVERVIEW.md`
- [x] `01_MANIFEST.md` → `examples/agenticos/01_MANIFEST.md`
- [x] `02_GLOSSARY.md` → `examples/agenticos/02_GLOSSARY.md`
- [x] `03_PROJECT_MAP.md` → `examples/agenticos/03_PROJECT_MAP.md`
- [x] `04_PARKING_LOT.md` → `examples/agenticos/04_PARKING_LOT.md`
- [x] `05_ADR_DECISION_LOG.md` → `examples/agenticos/05_ADR_DECISION_LOG.md`
- [x] `06_USER_MANUAL.md` → `examples/agenticos/06_USER_MANUAL.md`

**Validació:**
- [x] Cap fitxer original queda fora de `examples/agenticos/`

---

## 2. Core Governance (`00_core/`)

Reescriure des de zero amb contingut genèric:

- [x] **Crear `sdd.config.json`** amb schema de configuració del projecte
- [x] **Crear `AGENTS.md`** (genèric) — contracte d'entrada per agents, sense `AgenticOS`/`Kernel`
- [x] **Crear `00_core/SDD_RUNTIME.md`** — pipeline canònic, paths parametritzats via `sdd.config.json`, treure secció "Tools: Context Engine"
- [x] **Crear `00_core/SDD_READING_CONTRACT.md`** — ordre de lectura genèrica, paths relatius a `sdd.config.json`
- [x] **Crear `00_core/SDD_HANDOFF_CONTRACT.md`** — handoffs entre rols, paths genèrics
- [x] **Crear `00_core/SDD_GUIDE.md`** — metodologia completa, treure `Kernel`, `gentle-ai`, `Orange Pi`, ADRs específics
- [x] **Revisar `00_core/SDD_FEATURE_FORMAT.md`** — ja és quasi genèric, només actualitzar paths
- [x] **Revisar `00_core/AGENT_DECISION_TABLE.md`** — ja és genèric, només revisar formats
- [x] **Generalitzar `00_core/EXTERNAL_AUDIT_HARNESS_CONTRACT.md`** — "harness extern" en lloc de `gentle-ai`/`AgenticOS`

**Criteri:** cap referència a `AgenticOS`, `Kernel`, `Ring 0`, `00_project_documentation`, `gentle-ai`, `context-engine`, `Orange Pi`.

---

## 3. Execution Layer (`01_execution/`)

- [x] **Crear `01_execution/prompts/designer.md`** — placeholder `{{PROJECT_NAME}}`, `{{SDD_ROOT}}`, hardware opcional
- [x] **Crear `01_execution/prompts/specifier.md`** — genèric, sense referències a stack concret
- [x] **Crear `01_execution/prompts/validator.md`** — genèric
- [x] **Crear `01_execution/prompts/planner.md`** — genèric
- [x] **Crear `01_execution/prompts/implementer.md`** — genèric, sense `go test` hardcodejat
- [x] **Crear `01_execution/prompts/verifier.md`** — genèric, surface gates genèriques
- [x] **Crear `01_execution/skills/README.md`** — contracte mínim de skill (trigger, inputs, outputs, scope, failure_mode). **Buit per defecte** — el projecte afegeix les seves.

**Criteri:** els prompts són plantilles amb placeholders; no assumeixen stack ni terminologia de projecte.

---

## 4. Policies (`02_policies/`)

Mantenir les genèriques, eliminar les específiques d'AgenticOS:

- [x] **Crear `02_policies/REPORT_ENVELOPE_POLICY.md`** — genèric (mantenir, ja ho és)
- [x] **Crear `02_policies/INTEGRATION_SURFACE_POLICY.md`** — genèric (mantenir, ja ho és)
- [x] **Crear `02_policies/LEGACY_SPECS_POLICY.md`** — genèric (mantenir, ja ho és)
- [x] **Crear `02_policies/TASKS_NORMALIZATION_POLICY.md`** — genèric (mantenir)
- [x] **Crear `02_policies/SPECS_REAUDIT_PRIORITIZATION_POLICY.md`** — genèric (mantenir)
- [x] **Crear `02_policies/SKILLS_SYSTEM.md`** — reescriure: treure `gentle-ai`, `AgenticOS`, Go/React concrets; mantenir taxonomia de skills
- [x] ~~Eliminar del base: `GENTLE_AI_ADOPTION_POLICY.md`~~ (quedarà a `examples/`)
- [x] ~~Eliminar del base: `FRAMEWORK_INTEGRATION_MAP.md`~~ (quedarà a `examples/`)
- [x] ~~Eliminar del base: `CONTEXT_INTEGRATION_POLICY.md`~~ (quedarà a `examples/`)

---

## 5. Operations (`03_operations/`)

- [x] **Crear `03_operations/WORKFLOW.md`** — flux de 6 fases genèric, treure `context-engine`, mantenir intake→consolidation
- [x] **Crear `03_operations/SPEC_REAUDIT_WORKFLOW.md`** — "auditoria externa" genèrica, no `gentle-ai`
- [x] **Crear `03_operations/AUDIT_STRATEGY.md`** — genèric (mantenir si existeix)
- [x] **Crear `03_operations/TASKS_NORMALIZATION_POLICY.md`** — genèric (mantenir)
- [x] ~~Moure `ROADMAP.md`, `ROADMAP_REALITY_CHECK_*.md`, `OPENCODE_EXTERNAL_TRIAGE_PROMPT.md`~~ (ja a `examples/`)

---

## 6. Templates (`templates/`)

- [x] **Crear `templates/design.md`** — treure `Orange Pi 5B`. Hardware budget opcional/parametritzat via `sdd.config.json`.
- [x] **Crear `templates/specs.md`** — treure exemples `LLM timeout`, `kernel.state.json`. Fer exemples genèrics.

---

## 7. Documentació i Entrypoint

- [x] **Crear `README.md`** — Getting Started del framework: què és, com instal·lar, quick start
- [x] **Crear `CHANGELOG.md`** — (buit o amb v0.0.1)
- [x] **Crear `init-sdd.ps1`** — script PowerShell que:
  1. Llegeix `sdd.config.json` (o el crea amb defaults)
  2. Genera estructura de carpetes d'artefactes
  3. Genera un feature record de mostra (opcional)
- [x] **Crear `init-sdd.sh`** — equivalent per a Linux/macOS

---

## 8. Validació Final (per fases)

Després de cada fase:
- [x] `grep -ri "AgenticOS" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → ha de retornar 0
- [x] `grep -ri "Kernel" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → ha de retornar 0 (excepte si és terme genèric en context diferent)
- [x] `grep -ri "Ring 0" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → 0
- [x] `grep -ri "00_project_documentation" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → 0
- [x] `grep -ri "gentle-ai" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → 0
- [x] `grep -ri "context-engine" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → 0
- [x] `grep -ri "Orange Pi" 00_core/ 01_execution/ 02_policies/ 03_operations/ templates/` → 0

Validació final:
- [x] `examples/agenticos/` conté còpia completa i funcional del sistema original
- [x] El framework base és operable per a un projecte nou (quick start funciona)

---

## Notes de Migració (per a futurs usuaris)

Aquest document servirà de guia per qui vulgui migrar el seu propi projecte:
- On eren els paths d'AgenticOS → com parametritzar-los via `sdd.config.json`
- Què s'ha generalitzat i què s'ha mogut a `examples/`
- Com afegir skills pròpies al sistema buit

---

## Post-Completat: Millores Genèriques Aplicades (2026-04-23)

A partir de l'experiència amb `hf-downloader`, s'han identificat i aplicat les següents millores al framework genèric:

### Prompts
- ✅ `validator.md`: Checklists operatives completades (Completeness, Determinism, Traceability, Implementability)
- ✅ `migration_auditor.md`: Nou rol per validar paritat en migracions de stack

### Templates
- ✅ `design.md`: Afegits I/O Budget, Concurrency Model, Integration Surface (obligatori)
- ✅ `specs.md`: Afegits Type Definitions, Concurrency Model, Performance Budget
- ✅ `adr.md`: Nova plantilla per decisions d'arquitectura estandarditzades

### Configuració
- ✅ `sdd.config.json`: Afegit bloc `migration` (enabled, source_stack, target_stack, parity_required, rollback_strategy)

### Polítiques
- ✅ `DECOMPOSITION_AND_SIZE_POLICY.md`: Límits de mida per features (descomposició/consolidació)

### Bootstrap
- ✅ `SDD_BOOTSTRAP_CHECKLIST.md`: Checklist pre-flight per evitar forats a la inicialització

---

*Generat el 2026-04-23. Estat: ✅ COMPLETAT + MILLORAT*
