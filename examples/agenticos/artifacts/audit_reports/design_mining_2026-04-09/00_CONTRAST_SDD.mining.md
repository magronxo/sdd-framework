# Design Mining — Contrast contra autoritats SDD/ADR (global)

Data: 2026-04-09  
Entrada: `00_SEED_INDEX.mining.md` + `*.mining.md` (canònics)  
Objectiu: Marcar, per cada seed P0/P1, **on viu l’autoritat avui** (ADR / SDD spec / feature record) i si el legacy `01_design/` està alineat o fa drift.

## Autoritats canòniques que ja existeixen (observades al repo)

- ADR: `00_project_documentation/05_ADR_DECISION_LOG.md`
  - ADR 024/025 defineixen el “contracte mínim vigent” del ticket (vs model legacy ric).
- SDD spec: `00_project_documentation/SDD/artifacts/specs/feat-019-ticket-runtime-contract.md`
  - Normalitza schema mínim + FSM persistent mínima + fronteres (Guardian/HITL/observability fora del contracte mínim).
- Nota d’autoritat explícita (REDIRECT): `00_project_documentation/SDD/TICKET_TRANSITIONS.md`
  - Declara non-canonical i apunta ADR 024/025 + spec feat-019 + runtime router.
- Auditoria que explica el gap legacy↔runtime: `00_project_documentation/SDD/audit_reports/ticket_contract_audit_2026-04-05.md`

## Contrast per seeds P0/P1 (mapa “on mana”)

### 1) Ticket com a contracte d’IPC + FSM mínima persistent
- Seed (mining): `02_TICKET_SYSTEM.mining.md`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md`
- Autoritat actual:
  - ADR 024/025 a `00_project_documentation/05_ADR_DECISION_LOG.md`
  - Spec a `00_project_documentation/SDD/artifacts/specs/feat-019-ticket-runtime-contract.md`
  - Runtime: `02_implementation/internal/kernel/router.go` (referenciat per `01_design/TICKET_RUNTIME_TRANSITIONS_MINIMUM.md`)
- Alineament:
  - **Alineat en direcció** (ticket mínim + FSM mínima).
  - **Drift**: `01_design/02_TICKET_SYSTEM.md` descriu un contracte més ric; l’auditoria del 2026-04-05 diu explícitament que això NO governa el runtime.
- Nota clau: ADR 025 marca **frontera**: HITL/observability rica/steps[] no formen part del contracte mínim vigent.

### 2) Precedència d’autoritat (authority list)
- Seed (mining): `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md`
- Autoritat actual:
  - `00_project_documentation/SDD/TICKET_TRANSITIONS.md` (REDIRECT) ja fixa les autoritats.
  - ADR 024/025 + spec feat-019.
- Alineament:
  - **Ja resolt a nivell de governança**: hi ha fonts canòniques explícites.
- Risc restant:
  - Evitar que el legacy `01_design/*` sigui rellegit com a contracte (això és exactament el risc que descriu `ticket_contract_audit_2026-04-05.md`).

### 3) Governança de mutacions (SYSTEM_MUTATION + aprovació humana)
- Seed (mining): `02_TICKET_SYSTEM.mining.md`, `04_SEED_AND_AGENT_ANATOMY.mining.md`, `06_ORCHESTRATION_AND_ROLES.mining.md`
- Autoritat actual (indicis):
  - ADR 003 (system_mutation) a `00_project_documentation/05_ADR_DECISION_LOG.md` (apareix com a decisió presa; pipeline QA→Seguretat→Quarantena→Aprovació).
  - Feature record composite UI/API (HITL approvals) indicat a `00_project_documentation/SDD/artifacts/features_for_specs/feat-006.json`.
- Alineament:
  - **Concepte alineat** (mutació i aprovació existeixen com a governança).
  - **Frontera en tensió amb ADR 025**: HITL és fora del contracte mínim del ticket (pot existir com extensió; no s’ha d’injectar dins “mínim”).

### 4) Modes de seguretat (READ_ONLY/… + SAFE_MODE/LOCKDOWN) i kernel mediation
- Seed (mining): `13_SECURITY_MODEL.mining.md`
- Autoritat actual (indicis):
  - El dashboard/API exposa endpoints de mode segons “Completed Decisions” a `00_project_documentation/05_ADR_DECISION_LOG.md` (CD-007).
  - Spec d’API de kernel status/mode a `00_project_documentation/SDD/artifacts/specs/feat-012-kernel-status-api.md` (menciona GET/PUT `/kernel/mode` i llista de modes).
- Alineament:
  - **Alineat en principi**: modes i mediació són “kernel-centric”.
  - **Drift potencial**: els modes del legacy `01_design/13_SECURITY_MODEL.md` poden no coincidir exactament amb els modes “producte” definits a spec feat-012.

### 5) Crash recovery + backpressure (LoadBalancer/spool/reject)
- Seed (mining): `01_KERNEL.mining.md`
- Autoritat actual (indicis):
  - `ticket_contract_audit_2026-04-05.md` descriu el flux real i inclou LoadBalancer decisions (ALLOW/DELAY/SPOOL/REJECT).
  - Spec feat-019 marca explícitament el cas “load rejected” com a cas a tancar (E_LOAD_REJECTED) i que no pot quedar com TODO.
- Alineament:
  - **Alineat**: backpressure és robustesa operativa clau; però ADR 025 ho classifica com robustesa (no definició del contracte mínim).

### 6) Memòria/Context Builder (FTS5+WAL, MCP Librarian, budgets)
- Seeds (mining): `07_ENGRAM.mining.md`, `08_CONTEXT_BUILDER.mining.md`, `09_EXTENSIBILITY.mining.md`
- Autoritat actual (indicis):
  - Existeixen specs SDD dedicades (p.ex. `feat-003-engram-memory.md`, `feat-008-context-builder.md`) sota `00_project_documentation/SDD/artifacts/specs/`.
  - ADR log conté decisions “Librarian + tools de memòria” com a implementades (CD-002).
- Alineament:
  - **Alineat en idea** (memòria i context són components separats i governats).
  - **Gaps reals**: el mining identifica contractes encara “no especificats” (format exacte `agenticos_state`, algorisme sliding window).

## Lectura executiva (cap on tirar)

- Si una pregunta d’arquitectura toca el **contracte mínim del ticket**, la resposta ha de sortir d’ADR 024/025 + spec `feat-019` (no de `01_design/02_TICKET_SYSTEM.md`).
- Si toca **HITL/observability rica/steps[]**, és una extensió: decidir-la sobre una base estable (ADR 025 ho separa explícitament).
- Si toca **seguretat/modes**, contrastar `01_design/13_SECURITY_MODEL.md` amb la realitat d’API/spec (`feat-012`) i decisions completades (CDs).

