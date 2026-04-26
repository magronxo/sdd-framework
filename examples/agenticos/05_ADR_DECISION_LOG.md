# 06. Architecture Decision Records (ADR)

> **Actualitzat:** 28 Març 2026 — Afegida ADR 009: Separació FastAuditor vs Verifier.
> **Actualitzat:** 2026-04-04 — Nova secció "Completed Decisions" per arxivar implementacions completades.

Aquest document és el "Cementiri d'Idees" i el registre de decisions estructurals. Documenta *per què* s'ha pres una decisió de disseny i *quines* alternatives es van descartar.

---

## Completed Decisions

Aquesta secció conté implementacions completades migrades del Parking Lot. Decisions que ja no están "en Parking" sinó plenament implementades.

---

### CD-001: Routing per Departament (v22)
- **Data:** 2026-04-02
- **Descripció:** Sistema de routing que assigna tickets a agents segons el departament seleccionat.
- **Flux:** Ticket → AgentRegistry.ResolveAgentForDepartment() → Agent → ContextBuilder.BuildPromptForAgent()
- **Departaments:** auto (genesis), genesis, dev, it_ops, librarian
- **Components afectats:** contextbuilder/agent_registry.go, cmd/agenticos/main.go, TicketCreator.tsx
- **Estat:** ✅ Implementat

---

### CD-002: Librarian Agent + Tools de Memòria (v23)
- **Data:** 2026-04-02
- **Descripció:** Agent Librarian amb eines de memòria (engram_save, engram_search, engram_list, engram_delete) i get_datetime.
- **Tools afegides (5):** get_datetime, engram_save, engram_search, engram_list, engram_delete
- **Catàleg total:** 17 tools (fs_read, fs_write, fs_list, git_*, docker_*, run_tests, system_*, general, memory)
- **Estat Agents:** Genesis (17), Dev (10), IT Ops (7), Librarian (5)
- **Estat:** ✅ Implementat

---

### CD-003: Ticket Panel amb Retry/Edit/Delete (v24)
- **Data:** 2026-04-02
- **Descripció:** TicketPanel com finestra apart amb funcionalitats completes.
- **Funcionalitats:** Retry (tots), Edit (PENDING), Delete, Agrupació per estat, Detail/Edit modals
- **Components:** TicketPanel.tsx, DockLayout.tsx, api.ts (put/delete)
- **Estat:** ✅ Implementat

---

### CD-004: Flow Visualization (FlowCanvas v2)
- **Data:** 2026-04-03
- **Descripció:** Nova visualització amb 5 columnes: PENDING, PROCESSING, COMPLETED, FAILED, QUARANTINE
- **Característiques:** Arestes animades, MiniMap, stats temps real, auto-refresh 5s + WebSocket
- **Estat:** ✅ Implementat

---

### CD-005: Guardian Path Validation Fix
- **Data:** 2026-04-03
- **Descripció:** Guardian valida paths relatius i absoluts, normalització Windows/Unix
- **Components:** guardian.go, fast_path.json
- **Estat:** ✅ Implementat

---

### CD-006: AgentRegistry + ToolRegistry (SEED-01, SEED-02, SEED-03)
- **Data:** 2026-04-02
- **Descripció:** Deprecar system_prompt.go, carrega lazy d'agents, Tool Registry llegeix de JSON
- **Funcionalitats:**
  - AgentRegistry: 4 noves funcions (ResolveAgentForDepartment, GetAgent, GetSystemPrompt, ListAgents)
  - ToolRegistry: Catàleg central de 17 tools
  - Carrega lazy: agents/*.json
- **Estat:** ✅ Implementat

---

### CD-007: Dashboard Endpoints Completats
- **Data:** 2026-03/2026-04
- **Endpoints implementats:**
  - `/api/v1/kernel/status`, `/api/v1/kernel/restart`, `/api/v1/kernel/mode` (KernelPanel)
  - `/api/v1/modes`, `/api/v1/tools` (ModeSelector, ToolManager)
  - `/api/v1/scheduler/tasks`, `/api/v1/scheduler/logs` (SchedulerPanel)
  - `/api/v1/tickets` CRUD, `/api/v1/config` GET/POST/PUT
  - `/api/v1/departments`, `/api/v1/agents` (SeedViewer)
  - `/api/v1/reports`, `/api/v1/engram`, `/api/v1/engram/search` (ReportViewer, EngramPanel)
  - `/api/v1/sessions/*` (SessionTree)
  - `/api/v1/searx/search` (Researcher)
- **Estat:** ✅ Implementat

---

### CD-008: LLM Health Check (feat-014)
- **Data:** 2026-04-02
- **Descripció:** HealthMonitor singleton, HealthBadge al dashboard, ping cada 30s
- **Endpoints:** GET /api/v1/health, /api/v1/llm/providers
- **Tests:** 8 tests passen
- **Estat:** ✅ Implementat

---

### CD-009: Chat Ticket Creator (feat-016)
- **Data:** 2026-04-02
- **Descripció:** CRUD complet de tickets des del dashboard
- **Operacions:** Create (POST), List (GET), Delete (DELETE), Edit (PUT)
- **Components:** handleTicketsCreate, handleTicketsList, handleTicketDelete, handleTicketUpdate
- **Estat:** ✅ Implementat

---

### CD-010: Telegram Bridge Completat (TGB-01 a TGB-05)
- **Data:** 2026-03/2026-04
- **Components:** Bot bàsic, sistema subtemes, integració Kernel, notificacions automàtiques, botons interactius HITL
- **Estat:** ✅ Implementat

---

### CD-011: Home Assistant Integration (HA-01, HA-02, HA-03)
- **Data:** 2026-03/2026-04
- **Components:** Client HA, AgenticOS integracio, Router intel·ligent
- **Estat:** ✅ Implementat

---

### CD-012: Session Tree MVP (SESS-01 a SESS-10)
- **Data:** 2026-04-02
- **Descripció:** SessionStore, CRUD sessions/branques/nodes, checkout branca, tags
- **Endpoits:** 6/8 implementats (falta DELETE, GET nodes)
- **Estat:** ✅ MVP Implementat (Fase 2 pendent)

---

### CD-013: Core Fixes (CORE-FIX-01 a CORE-FIX-07)
- **Data:** 2026-04-03
- **Fixes:**
  - CORE-FIX-01: Guardian valida paths relatius i absoluts
  - CORE-FIX-02: Normalització noms departaments (main.go)
  - CORE-FIX-03: Política paths Windows + Unix (fast_path.json)
  - CORE-FIX-04: WebSocket events minúscules (types.go)
  - CORE-FIX-05: Usage pointer opcional (LLM)
  - CORE-FIX-06: getBaseDir() i observer.go usaven archive/ enlloc de tickets/
  - CORE-FIX-07: GetConfigPath() i getWSConfigPath() cercaven config/ first
- **Estat:** ✅ Tots implementats

---

### CD-014: Technical Fixes (TECH-01 a TECH-10)
- **Data:** 2026-03/2026-04
- **CRÍTICS (Backend no funcional):**
  - TECH-01: HealthMonitor singleton inicialitzat
  - TECH-02: Scheduler amb SchedulerLogs
  - TECH-03: Ollama fallback integrat a handleLLMChat
- **IMPORTANTS (Frontend mock data):**
  - TECH-04: ReportViewer crida API real
  - TECH-05: EngramPanel crida API real
  - TECH-06: HealthBadge component creat
- **MENORS:**
  - TECH-07: Executor tests skip Windows
  - TECH-09: EventLoop scanExisting() per a Windows
  - TECH-10: LoadBalancer GetActiveTicketCount()
- **Estat:** ✅ Tots implementats

---

### CD-015: Accessibility Fixes (A11Y)
- **Data:** 2026-04-02
- **Descripció:** Formularis accessibilitat (id/name) - UI-FIX-01
- **Components:** TicketCreator.tsx, ChatPanel.tsx, TicketPanel.tsx
- **Estat:** ✅ Implementat

---

### CD-016: LLM Config Path Priority Fix
- **Data:** 2026-04-04
- **Descripció:** GetConfigPath() i getWSConfigPath() prioritzaven ./config/llm.json enlloc de agenticos_data/config/llm.json
- **Components:** llm/config.go, websocket.go
- **Estat:** ✅ Implementat

---

### CD-017: LLM Provider Field Fix
- **Data:** 2026-04-04
- **Descripció:** El camp `Provider` (json:"-") s'exclou ara de les peticions API per evitar errors "prompt_tokens"
- **Components:** llm/types.go (Provider field), llm/client.go (error handling)
- **Estat:** ✅ Implementat

---

### CD-018: AgentRegistry Initialization
- **Data:** 2026-04-04
- **Descripció:** InitAgentRegistry() cridat a cmd/agenticos/main.go per carregar configs de seed/agents/
- **Impacte:** allowedTools ara es carrega correctament, tool permissions funcionen
- **Components:** cmd/agenticos/main.go
- **Estat:** ✅ Implementat

---

### CD-019: Tools no enviades a LLM (Ticket Cognition Bug)
- **Data:** 2026-04-04
- **Descripcio:** Bug: ContextBuilder muntava prompt.Tools però processLLMAgentTicket NO les copiava a ChatCompletionRequest
- **Fix:**
  1. Afegit `Tools []any` a `ChatCompletionRequest` (llm/types.go)
  2. Copiat `prompt.Tools` → `llmReq.Tools` (cmd/agenticos/main.go)
- **Impacte:** LLM ara rep la llista de eines disponibles i pot fer tool calling
- **Estat:** ✅ Implementat

---

### CD-020: Context-engine resilient fallback (CTX-02)
- **Data:** 2026-04-06
- **Descripció:** Es considera consolidat el fallback resilient del `context-engine` (tancat com a base operativa via `feat-018` i ADR 026).
- **Regles operatives:**
  1. Si l'embedder falla, `Search()` ha de provar una cerca textual clàssica sobre el contingut indexat.
  2. Si la cerca textual també falla o no hi ha índex usable, el sistema ha de retornar un error llegible i una resposta buida, no un crash.
  3. Si `store.json` és absent o corrupte, el sistema no ha de reindexar de forma destructiva.
  4. El fallback ha de prioritzar operabilitat i traçabilitat, no perfecció semàntica.
- **Estat:** ✅ Implementat

---

### CD-021: Normalització d'aliases de tools (TLS-01)
- **Data:** 2026-04-06
- **Descripció:** Es dona per tancada la normalització d'aliases de tools al flux natural. La documentació i els prompts han de referenciar noms canònics (repo/runtime) i evitar aliases ambigus, excepte per traçabilitat durant migracions.
- **Estat:** ✅ Implementat

---

### CD-022: Guardian hardening baseline (SEC-00A/SEC-00B/SEC-00B2/SEC-00C)
- **Data:** 2026-04-06
- **Descripció:** Es considera implementat el baseline de hardening del Guardian:
  - `SEC-00A`: fix de falsos positius a `ValidatePath`
  - `SEC-00B`: validació mínima d'arguments per `execute_command`
  - `SEC-00B2`: validació mínima d'URL per `http_request` contra SSRF/esquemes perillosos
  - `SEC-00C`: "guardian before execution" cobert per test existent (veure ADR 026)
- **Estat:** ✅ Implementat

---

*Document actualitzat: 2026-04-04 (v25) - Nova secció "Completed Decisions" migrada del Parking Lot*

---

## ADR 020: Claw-Code com a font de patrons, no com a model a replicar
- **Data:** 2026-04-04
- **Context:** S'ha revisat l'anàlisi externa de `claw-code` a `00_project_documentation/external_refs/claw-code analysis for agenticosgen/` per identificar millores potencials per a AgenticOS i per al flux extern de desenvolupament.
- **Decisió Presa:** AgenticOS manté el seu model **kernel-centric, físico i determinista**. `claw-code` només s'adopta com a font de patrons locals per reforçar seguretat, context i gating del flux, sense copiar-ne el paradigma agent-centric ni la seva arquitectura líquida.
- **Integrar ara:**
  1. Hardening del Guardian amb heurístiques read-only vs destructiu i validació més rica d'arguments.
  2. Boundary enforcement més fort a execució i operacions de fitxers.
  3. Control de soroll i truncació de sortides on el Kernel ja és executor.
- **Integrar més endavant:**
  1. Gating més rígid al flux SDD.
  2. Compression semàntica del context.
  3. Tool registry / bridge més net i lifecycle tracking més ric.
- **Ignorar de moment:** Plugin system complex, MCP manual low-level, i qualsevol patró que desplaci la decisió fora del Kernel.

---

## ADR 021: Prioritat immediata de Guardian Hardening
- **Data:** 2026-04-04
- **Context:** L'avaluació comparada mostra que el major retorn amb menor impacte estructural és reforçar el Guardian abans de tocar registres dinàmics, bridges o compacció avançada.
- **Decisió Presa:** La primera adopció inspirada en `claw-code` serà **Guardian Hardening**, no un refactor de l'Executor ni del Context Builder.
- **Abast inicial:**
  1. Classificació bàsica de comandes read-only vs potencialment destructives.
  2. Validació d'arguments, no només de paths.
  3. Boundary enforcement més dur abans de qualsevol execució shell o tool amb efectes.
- **Desglossament mínim aprovat:**
  1. Fixar `ValidatePath` per evitar matching per prefix textual.
  2. Fer que el pas de validació no sigui només convenció, sinó enforcement real abans de l'execució.
  3. Cobrir `execute_command` i `http_request` com a superfícies d'alt risc.
  4. Tancar-ho amb proves end-to-end, no només unitàries.
- **Motiu:** És la millora amb millor relació risc/retorn per a un sistema encara en fase de professionalització. Reforça control i seguretat sense forçar un canvi de paradigma.

---

## ADR 022: L'automatització del flux professional no substitueix la governança documental
- **Data:** 2026-04-04
- **Context:** `claw-code` inspira un model més programàtic de gating i política d'execució. AgenticOS ja té `PROFESSIONAL_OPERATING_FLOW.md`, `AGENT_DECISION_TABLE.md` i el flux SDD com a governança overlay.
- **Decisió Presa:** L'automatització futura del flux professional s'ha de fer **per sobre** de la governança documental existent, no en lloc seu.
- **Aplicació futura:**
  1. Gating de dependències de tasks abans de tancar features o lots.
  2. Auditoria adversarial paral·lela per a fases d'audit profund.
  3. Validacions de transició programades entre fases del flux professional.
- **Límit explícit:** No es converteix el flux actual en una màquina d'estats rígida fins que la base documental i el comportament dels agents externs siguin estables.

---

## ADR 023: 3_deployments és bootstrap, no runtime viu
- **Data:** 2026-04-05
- **Context:** Hi ha confusió estructural entre el repo, 2_implementation/agenticos_data, 3_deployments/ i el lloc on hauria de viure una seed desplegada real.
- **Decisió Presa:** 3_deployments/ es defineix com a **kit de bootstrap i plantació**, no com a directori de runtime viu ni com a ubicació final d'una seed desplegada.
- **Separació adoptada:**
  1. 2_implementation/ = codi i runtime de desenvolupament.
  2. 2_implementation/agenticos_data = sandbox local i dades de prova per desenvolupament.
  3. 3_deployments/ = scripts, plantilles i llavor base per plantar una instància.
  4. Seed desplegada real = directori extern al repo, triat per l'usuari o per l'entorn.
- **Implicació:** El repo és el planter i el taller; la instància viva no ha de créixer dins del repo.
- **Nota actual:** 3_deployments/setup.ps1 encara arrossega topologia legacy (spool, archive, active) i s'haurà d'alinear més endavant amb el runtime vigent abans de considerar-lo un camí de desplegament fiable.

---

## ADR 024: El contracte vigent del ticket és el runtime mínim, no el model legacy complet
- **Data:** 2026-04-05
- **Context:** L'auditoria `SDD/audit_reports/ticket_contract_audit_2026-04-05.md` confirma una fractura entre el contracte ampliat del ticket descrit a `01_design/02_TICKET_SYSTEM.md` i el contracte executable real implementat a `02_implementation`.
- **Problema:** Avui conviuen dues veritats incompatibles:
  1. un model legacy ric del ticket com a màquina d'estats universal
  2. un model runtime curt però executable que és el que governa el producte real

- **Decisió Presa:** Fins a nova especificació formal, el **contracte vigent del ticket a AgenticOS és el contracte runtime mínim implementat**, no el model legacy complet.

- **Això implica:**
  1. La font de veritat immediata per al comportament del ticket és el runtime de `02_implementation`, especialment `cmd/agenticos/main.go` i `internal/kernel/router.go`.
  2. `01_design/02_TICKET_SYSTEM.md` queda classificat com a **baseline conceptual i target futur**, però no com a descripció fidel del contracte executable actual.
  3. Cap desenvolupament nou no ha d'assumir automàticament que els 11 estats, `steps[]`, `metadata/request/final_resolution/metrics`, delegació completa o HITL complet ja existeixen al runtime.
  4. Qualsevol ampliació del ticket system s'ha de fer en aquest ordre:
     - decisió de contracte
     - spec de schema/FSM
     - implementació

- **Contracte runtime mínim reconegut ara:**
  1. Ticket persistent JSON curt amb camps bàsics com `id`, `type`, `status`, `created_at`, `payload`, `result` i `error`.
  2. Flux operatiu real:
     `incoming -> processing -> success | failed`
  3. Capacitats actuals reals:
     - tickets directes amb `tool_name` i `tool_params`
     - tickets `llm_agent` amb loop ReAct en memòria
     - validació de tool/path via Guardian
     - tancament en `COMPLETED` o `FAILED`
  4. Elements explícitament diferits:
     - FSM persistent completa d'11 estats
     - traça persistent de `steps`
     - approvals/HITL connectats al kernel
     - delegació/callback universal entre departaments
     - recovery/staleness plenament alineat amb l'estructura runtime actual

- **Motiu de la decisió:**
  1. Evitar que la documentació empenyi implementacions sobre un contracte que encara no existeix.
  2. Tallar la deriva entre filosofia, design i runtime.
  3. Obrir una fase P0 neta per congelar schema mínim i FSM mínima abans d'afegir més comportament.

- **Conseqüències immediates:**
  1. El ticket system s'ha de tractar com a subsistema funcional però encara en normalització contractual.
  2. El següent treball correcte és una spec curta de:
     - schema mínim canònic del ticket
     - FSM persistent mínima suportada
     - llista explícita d'estats i camps diferits
  3. Fins que això no existeixi, s'han d'evitar expansions que depenguin del model legacy ric com si fos executable avui.

---

## ADR 025: El contracte mínim del ticket inclou mediació persistent, no HITL ni observability rica
- **Data:** 2026-04-05
- **Context:** Després de fixar a ADR 024 que el contracte vigent és el runtime mínim executable, encara quedava una ambigüitat arquitectònica important: on acaba exactament el contracte del ticket i on comencen Guardian, executor, HITL i observability.
- **Problema:** Sense aquesta frontera explícita, qualsevol millora de seguretat, traces o control humà corre el risc de presentar-se com a part del contracte base quan en realitat només és una extensió, una política operativa o una capa de robustesa.
- **Decisió Presa:** El contracte mínim d'execució del ticket a AgenticOS queda definit com una **unitat persistent mínima de treball** que el Kernel pot:
  1. adquirir
  2. validar abans d'efecte
  3. executar per la ruta corresponent
  4. tancar de manera terminal i traçable

- **Schema mínim reconegut:**
  1. Camps obligatoris: `id`, `type`, `status`, `created_at`, `payload`
  2. Camps de cicle de vida/terminal: `updated_at`, `result`, `error`

- **FSM mínima reconeguda:**
  1. `PENDING`
  2. `PROCESSING`
  3. `AUDITING`
  4. `EXECUTING`
  5. `COMPLETED`
  6. `FAILED`

- **Fronteres adoptades:**
  1. `AUDITING` forma part del contracte mínim perquè AgenticOS manté el principi Zero Trust: el Kernel valida abans de qualsevol efecte.
  2. Guardian **no és** el contracte del ticket; és la capa de mediació que opera dins la fase `AUDITING`.
  3. L'executor i les tools **no defineixen** el ticket; en són consumidors un cop el ticket ja ha passat admissió i validació.
  4. HITL / approvals **no formen part** del contracte mínim vigent; si entren, ho faran com a extensió explícita de la FSM.
  5. L'observability mínima sí depèn del contracte (`id`, estat, timestamps, `result`/`error`), però les traces riques, `steps[]` persistits i projeccions visuals no en formen part.
  6. Load balancing, worker pool, retries i stale handling són **robustesa operativa**, no definició del contracte mínim.

- **Elements explícitament diferits:**
  1. model ric d'11 estats
  2. `WAITING`, `REQUIRES_HUMAN`, `APPROVED`, `REJECTED`, `LOOPING`
  3. `steps[]` persistits
  4. HITL complet cablejat al kernel
  5. recovery/staleness contractual avançat
  6. observability rica embeguda al ticket

- **Motiu de la decisió:**
  1. Evitar que seguretat, HITL o observability inflin el contracte base abans de congelar-ne el nucli.
  2. Preservar una separació neta entre semàntica de runtime, polítiques de mediació i infraestructura operativa.
  3. Fer possible el debat posterior de seguretat/HITL sobre una base estable i no sobre intuïcions o llenguatge legacy.

---

## ADR 026: Modes d’execució del xat (interactive vs ticketed) i “ticket promotion” determinista
- **Data:** 2026-04-10
- **Context:** Un missatge de xat pot ser (1) una consulta simple (p. ex. `get_datetime`) o (2) una tasca amb efecte, multi-step o que requereix traçabilitat. Sense un criteri formal, es barregen rutes d’execució i apareix ambigüitat: quan es crea un ticket? qui decideix? què es pot considerar “PASS”?
- **Problema:** Si el model (o la UI) decideix de forma implícita, es pot trencar Zero Trust i/o perdre auditabilitat. També es pot acabar “forçant tickets” per consultes trivials, o a l’inrevés, executant efectes sense persistència i sense contracte de ticket.

- **Decisió Presa:** El **Kernel** és l’autoritat final sobre el mode d’execució del xat i aplica una **policy determinista** per decidir si una interacció és `interactive` (sense ticket) o `ticketed` (crea/usa ticket).

- **Regles adoptades:**
  1. **Autoritat (precedència):** Kernel policy > UI request > LLM suggestion.
     - La UI pot demanar `requested_mode: interactive|ticketed` (opcional).
     - L’LLM pot suggerir `should_create_ticket: true|false` + motiu (opcional).
     - El Kernel decideix sempre.
  2. **Mode `interactive` (sense ticket) NOMÉS si:**
     - la petició és read-only (cap tool amb side effects),
     - és curta (no multi-step llarg),
     - no requereix traça persistent, approvals ni reexecució.
  3. **Mode `ticketed` (amb ticket) si qualsevol és certa:**
     - l’usuari demana explícitament “fes un ticket / fes-ho en segon pla / recorda-ho”,
     - hi ha side effects (fs_write/move/exec/config/network amb efecte),
     - és multi-step o potencialment llarg,
     - requereix auditabilitat/traçabilitat o pot implicar approvals.
  4. **No-goal explícit:** “cada tool-call és un ticket nou” NO és el contracte vigent. El bucle ReAct (tool-calls) viu **en memòria dins d’un ticket `llm_agent`** segons ADR 024/025 i `feat-019`.

- **Conseqüències:**
  1. Es preserva Zero Trust: els efectes passen per ticket + `AUDITING` quan aplica.
  2. Es redueix ambigüitat: el sistema sap quan cal persistència i quan no.
  3. Es defineix un camí clar per futures millores (p. ex. “steps-lite” persistit) sense inflar el contracte base.

- **Alternatives descartades:**
  1. LLM decideix sempre (massa no determinista i fa mal a audit/seguretat).
  2. UI decideix sempre (trenca invariants de seguretat si la UI s’equivoca o és bypassed).
  3. Ticket per tool-call (canvi de semàntica/volum; requereix feature nova i contracte nou).

---

## ADR 027: Convenció de fitxers de secrets (`secrets.*.json`) i separació de registry/knobs
- **Data:** 2026-04-10
- **Context:** El contracte de config LLM i providers s’ha anat consolidant (registry vs secrets vs knobs). Sense una convenció explícita, és fàcil cometre drift: secrets dins fitxers committables, duplicació de fonts de veritat, o noms confusos com `llm.json` fent de “tot”.
- **Problema:** Necessitem una convenció escalable i consistent per:
  1) identificar fitxers que **mai** s’han de commitejar (secrets),
  2) separar “registry committable” de “secrets locals” i “knobs”,
  3) facilitar onboarding i reduir errors humans.

- **Decisió Presa:** Adoptar la convenció:
  1. `providers.json` = **registry committable** (cap secret).
  2. `secrets.providers.json` (i en general `secrets.*.json`) = **secrets locals** (no committable).
  3. `knobs.*.json` o `config.*.json` = **knobs no secrets** (committable o no segons política del repo), però mai “registry”.

- **Regles adoptades:**
  1. Cap fitxer `secrets.*.json` es commiteja. El repo ignora aquests fitxers via `.gitignore`.
  2. Les APIs mai retornen secrets; poden retornen com a màxim un flag `configured: true|false`.
  3. Si calen exemples, es fan via `*.example` o documentació (mai secrets reals).

- **Conseqüències:**
  1. `llm.json` deixa de ser un nom recomanable per “secrets only”; si existeix, s’ha d’acotar a knobs/secrets amb migració explícita.
  2. Escalabilitat: mateix patró per Telegram/SearX/altres integracions (`secrets.telegram.json`, `secrets.searx.json`, etc.).

- **Alternatives descartades:**
  1. Mantenir secrets dins `providers.json` (prohibit: registry committable).
  2. `.env` com a únic mecanisme (possible, però no substitueix necessàriament els secrets estructurats JSON).

---

## ADR 028: Security modes com a postura operativa del Kernel i emergency overlays
- **Data:** 2026-04-11
- **Context:** AgenticOS ja exposa `GET/PUT /api/v1/kernel/mode`, `GET /api/v1/modes` i `GET /api/v1/kernel/status` via `feat-012`, però el mining del model de seguretat detecta que els modes encara poden derivar entre API/UI, legacy design i enforcement real. Alhora, ADR 024/025 ja fixa que el contracte mínim del ticket no s'ha d'inflar amb HITL, observability rica ni un sistema gran de permisos.
- **Problema:** Si els modes són només UI/API, Zero Trust queda decoratiu. Si `SAFE_MODE` i `LOCKDOWN` es tracten com a modes normals, es pot confondre una postura de treball amb un estat d'emergència i fer massa fàcil sortir-ne per canals inadequats.

- **Decisió Presa:** Els `security modes` són la **postura operativa transitòria del Kernel** i governen quines superfícies d'acció poden passar de `AUDITING` a `EXECUTING`. `SAFE_MODE` i `LOCKDOWN` no són modes normals: són **emergency overlays** que restringeixen o bloquegen el Kernel per sobre del mode actual.

- **Modes normals reconeguts:**
  1. `READ_ONLY`: permet lectura local segura; bloqueja `write`, `execute` i xarxa amb efecte.
  2. `MONITOR`: permet lectura, mètriques/logs i observació; no permet mutacions.
  3. `IT_OP`: mode operatiu de producte per defecte actual; permet accions operatives limitades segons Guardian/policy.
  4. `DEV`: mode de desenvolupament controlat; pot permetre `write` i `execute` limitats.
  5. `AUDIT`: mode de verificació; ha de prioritzar visibilitat i lectura, no mutació automàtica.
  6. `FULL`: mode de màxim risc; no es pot activar sense HITL/confirmació forta definida. Mentre aquest mecanisme no existeixi, el canvi a `FULL` queda rebutjat.

- **Emergency overlays:**
  1. `SAFE_MODE`: pot ser activat manualment o automàticament per incident. Força una postura restrictiva, permet com a màxim lectura mínima de diagnòstic i bloqueja efectes.
  2. `LOCKDOWN`: pot ser activat per emergència crítica. Bloqueja tota execució no essencial i no s'ha de poder desactivar des de canals remots o UI lleugera.

- **Regles d'autoritat i enforcement:**
  1. El punt d'enforcement és Guardian/runtime abans d'execució, no el dashboard ni el canal que envia la petició.
  2. Les validacions de mode s'apliquen en temps real a l'hora de passar d'`AUDITING` a `EXECUTING`.
  3. Si el mode canvia mentre hi ha tickets actius, els tickets no tenen dret adquirit a executar: es revaliden contra el mode vigent.
  4. Si un canvi de mode fa que un ticket actiu ja no sigui admissible, el runtime ha de congelar-lo, retornar-lo a una cua segura o fallar-lo de manera determinista segons la spec de `SEC-01`.
  5. Qualsevol canal pot activar un mode més restrictiu o emergency overlay si està autenticat i autoritzat per fer-ho.
  6. Només canals locals/forts, com la TUI o un mecanisme equivalent d'operador local, poden sortir de `SAFE_MODE` o `LOCKDOWN`.
  7. Els modes poden afectar no només tools, sinó també el context exposat als agents; context global/host s'ha de tractar com a superfície sensible.

- **Taula mínima de superfícies:**
  1. `read_only`: lectura local segura i consultes sense efecte.
  2. `write`: escriptura o mutació de fitxers/dades.
  3. `execute`: execució de comandes, processos o accions amb efecte local.
  4. `network`: sortida de xarxa; en fases posteriors es podrà separar en `network_read` i `network_effect`.

- **Fora d'abast d'aquesta ADR:**
  1. Implementar `SEC-01`.
  2. Dissenyar HITL complet.
  3. Persistir històric de canvis de mode.
  4. Definir ACLs completes per usuari/agent/canal.
  5. Convertir `SAFE_MODE`/`LOCKDOWN` en UX final.

- **Conseqüències:**
  1. `feat-012` queda com a baseline d'API, però `SEC-01` haurà de formalitzar enforcement real.
  2. El frontend s'haurà d'alinear amb el contracte canònic `PUT /kernel/mode` i errors deterministes.
  3. `AUDIT` no s'ha d'interpretar com a "FULL amb més logs"; és una postura de verificació amb mutació restringida.
  4. `SAFE_MODE` i `LOCKDOWN` s'han de dissenyar com a estat d'emergència separat, no com a simple opció del selector normal.
  5. El debat de seguretat haurà de decidir la matriu exacta mode -> superfície, el tractament de tickets actius i la relació entre mode i context visible.

---

## ADR 029: Kernel immutable i superfícies UI mutables
- **Data:** 2026-04-11
- **Context:** AgenticOS ja disposa d'un dashboard React/Vite a `02_implementation/agentic-ide/`, una TUI amb vocació d'accés local fort, i diverses superfícies externes possibles. Alhora, han aparegut idees de dashboards tipus "mission control" més rics visualment i funcionalment. Cal evitar que l'evolució del dashboard arrossegui decisions del Kernel o que una UI concreta es confongui amb el contracte del sistema.
- **Problema:** Si el dashboard actual es tracta com a arquitectura canònica, el producte queda rígid i costa substituir-lo o complementar-lo. Si, al contrari, es permet que una seed o una UI mutin lliurement el comportament observable del sistema, es trenca la frontera de seguretat: la UI podria redefinir estats, accions, permisos o transicions que pertanyen al Kernel, Guardian o runtime.

- **Decisió Presa:** El **Kernel és immutable en els seus contractes operatius** i les **superfícies UI són mutables i substituïbles**. Dashboard, IDE web, mission control, TUI, Telegram o futures superfícies són projeccions i canals d'intenció; no són font de veritat del runtime.

- **Parts immutables del Kernel/runtime:**
  1. Contracte mínim del ticket i transicions canòniques.
  2. Enforcement de Guardian, security modes i emergency overlays.
  3. Execució de tools i classificació de superfícies d'acció.
  4. APIs canòniques, errors deterministes i invariants de status.
  5. Ownership de sessions, tickets, traces, context exposable i observability raw.

- **Parts mutables de la UI:**
  1. Layout, navegació, sidebar, panels, pestanyes i estètica.
  2. Separació futura entre `Mission Control` operatiu i `IDE` de desenvolupament dins la WebUI.
  3. Visualitzacions ReactFlow, dashboards alternatius, widgets i resums.
  4. Agrupacions, filtres, noms humans, vistes guardades i UX de consulta.
  5. Clients alternatius que consumeixin els mateixos contractes públics del Kernel.

- **Regles de frontera:**
  1. Una UI pot mostrar, resumir, agrupar o projectar estat; no pot redefinir el significat d'un estat.
  2. Una UI pot enviar intencions d'acció; no pot saltar Guardian ni decidir per si sola que una acció és segura.
  3. Una UI pot tenir permisos diferents segons canal; la sortida d'emergència (`SAFE_MODE`/`LOCKDOWN`) queda reservada a canals locals/forts com la TUI o equivalent.
  4. Les flows visuals no són font de veritat; són projeccions d'estat, traces o events produïts pel runtime.
  5. Una seed pot crear o substituir dashboards, però no pot mutar contractes Kernel sense passar per ADR/SDD.

- **Rol de la TUI:**
  1. La TUI es manté com a superfície local forta, orientada a operació directa i recuperació.
  2. Per defecte, la TUI no s'ha de tractar com a frontend exposat a Internet.
  3. Pot tenir més autoritat que el dashboard remot, especialment per activar o sortir de modes restrictius, sempre segons specs de seguretat.

- **Conseqüències:**
  1. No cal reconstruir ara el dashboard actual com a mission control.
  2. Es pot continuar estabilitzant el dashboard existent mentre es prepara una futura separació `Mission Control` / `IDE`.
  3. Les futures specs de UI han de declarar quin contracte Kernel consumeixen i quina part és només presentació.
  4. Qualsevol canvi visual que requereixi nou estat runtime ha d'obrir spec pròpia; no s'ha d'inferir estat nou dins del frontend.
  5. El següent debat arquitectònic recomanat és `UI Shell / Surface Model`: com s'organitzen WebUI, TUI, Mission Control, IDE, flows, sessions i settings sense desplaçar responsabilitats del Kernel.

- **Fora d'abast d'aquesta ADR:**
  1. Implementar un nou mission control.
  2. Redissenyar el dashboard actual.
  3. Definir una plugin architecture de UI.
  4. Tancar la UX final de TUI o de WebUI.
  5. Crear el contracte complet d'execution traces.

---

## ADR 001: Rebuig del "Fat Prompt" per a Skills
- **Data:** 21 Març 2026
- **Context:** Com dotem a un agent de coneixement expert (ex: "Com escriure un SDD impecable")?
- **Alternativa Descartada:** Injectar tota la teoria, problemes comuns i millores pràctiques directament al `system_prompt.md` de l'agent (creant un "Fat Prompt" de 3000+ tokens).
- **Motiu del Rebuig:**
  1. **Hardware:** Processar 3000 tokens extra per cada interacció saturaria la RAM de la Orange Pi i dispararia el *Time to First Token*.
  2. **Lost in the Middle:** Els models locals (8B) tendeixen a perdre instruccions quan el context és massa llarg.
- **Decisió Presa:** Utilitzar **"Just-In-Time Skills"**. Les skills són fitxers `.md` curts a la carpeta `/manuals/`. Només s'adjunten al context de l'LLM quan la tasca específica ho requereix.

---

## ADR 002: Rebuig del Polling Infinit per a la Lectura de Tickets
- **Data:** 21 Març 2026
- **Context:** Com sap el Kernel que un agent ha rebut un nou `.ticket` a la seva bústia (`/inbox/`)?
- **Alternativa Descartada:** Un bucle infinit que llegeix el directori cada X segons (Polling).
- **Motiu del Rebuig:** El polling constant manté la CPU desperta, consumint energia i cicles de rellotge innecessaris a la Orange Pi 5B.
- **Decisió Presa:** Utilitzar esdeveniments del sistema operatiu (Linux `inotify` via la llibreria `fsnotify` de Go). El Kernel dorm (0% CPU) fins que l'OS l'avisa que s'ha creat un fitxer.

---

## ADR 003: Rebuig del `fs_write` per a Mutacions del Sistema
- **Data:** 21 Març 2026
- **Context:** Com permetem que el sistema modifiqui el seu propi codi (autogeneració) sense risc de trencar-se?
- **Alternativa Descartada:** Permetre que un agent utilitzi l'eina estàndard d'escriptura de fitxers (`fs_write`) sobre els fitxers `.py` del sistema.
- **Motiu del Rebuig:** Un error de sintaxi (un simple *typo*) en el codi del Kernel o d'un departament aturaria el sistema completament. Com que l'agent necessita el Kernel per pensar, el sistema es "suïcidaria" sense capacitat de recuperar-se.
- **Decisió Presa:** Crear un intent específic `system_mutation`. Aquest intent no escriu al disc, sinó que envia el codi a un Pipeline d'Orquestració (QA -> Seguretat -> Quarantena -> Aprovació Humana). A més, s'implementa un servei de Rollback extern (script bash) que restaura un `.bak` si el nou codi falla en arrencar.

---

## ADR 004: Llenguatge del Kernel i Eines (Pure Go + WASM/MCP) [DECISIÓ PRESA]
- **Data:** 21 Març 2026
- **Context:** Quin llenguatge utilitzar per programar el Kernel (el "Bootloader" i router del sistema) i com executar eines dinàmiques tenint en compte que s'executarà en una Orange Pi 5B?
- **Opcions en debat:** Python, Go, Rust, Elixir/Node.js.
- **Motiu del Rebuig (Altres):**
  - *Rust:* Massa complexitat cognitiva i temps de compilació lent (dolent per a un sistema que ha de mutar ràpidament).
  - *Elixir:* Perfecte per a actors concurrency, però ecosistema massa nínxol.
  - *Node.js:* Alt consum de RAM (V8 engine) comparat amb llenguatges compilats.
  - *Python (com a Kernel i Eines):* Alt consum de RAM en IDLE, problemes amb el GIL per a concurrència massiva, gestió de dependències fràgil a producció. Llençar intèrprets de Python per a cada eina consumeix massa recursos.
- **Decisió Presa:** **Pure Go + Eines WASM/MCP.**
  - **El Kernel i els Agents es programaran en Go (Golang):** Actuarà com una "roca". Consum de RAM gairebé nul (<20MB), binari estàtic únic (zero dependències a la Orange Pi), i concurrència nativa (Goroutines) perfecta per llegir fitxers (`inotify`) i gestionar timeouts d'Ollama.
  - **Les Eines utilitzaran WASM o MCP:** Quan un agent necessiti executar codi dinàmic (ex: fer web scraping, processar dades), el Kernel (Go) executarà un mòdul WebAssembly (WASM) compilat o es connectarà a un servidor Model Context Protocol (MCP). Això garanteix un aïllament perfecte (sandboxing natiu) i un rendiment extremadament superior a llençar scripts de Python.

---

## ADR 005: Prohibició de YAML en Documentació del Sistema [DECISIÓ PRESA]
- **Data:** 27 Març 2026
- **Context:** Els fitxers de memòria (Engram) i altres documents del sistema utilitzen YAML com a llenguatge de metadades (frontmatter). El nucli d'AgenticOS està escrit en Go.
- **Problema:** YAML és un llenguatge amb una especificació complexa i múltiples implementacions. Les llibreries de YAML per a Go són pesades, insegures (vulnerabilitats d'injecció) i poden consumir molta RAM. A més, YAML permet característiques com alias i anchors que podrien portar a comportaments inesperats.
- **Alternatives Considerades:**
  - **YAML:** Llarg, complex, dependència pesada.
  - **TOML:** Més senzill però encara requereix llibreria externa.
  - **JSON:** Natiu a Go (`encoding/json`), lleuger, sense dependències externes.
- **Decisió Presa:** **Prohibir YAML en tots els documents del sistema.** Utilitzar **JSON frontmatter** (capçalera JSON) per a tots els fitxers Markdown (Engrams, Tickets, etc.).
- **Motiu:**
  1. **Zero Dependències:** `encoding/json` és part de la llibreria estàndard de Go.
  2. **Seguretat:** JSON no permet execució de codi ni injeccions.
  3. **Rendiment:** Parsing de JSON és extremadament ràpid i amb baix consum de RAM.
  4. **Consistència:** Els Tickets ja són JSON; els Engrams seran JSON frontmatter.
- **Conseqüències:**
  - S'ha actualitzat el disseny de l'Engram (`02_MEMORY_ENGRAM.md`) per utilitzar JSON frontmatter.
  - Tota documentació futura haurà d'utilitzar JSON frontmatter.
  - Les llibreries de YAML s'eliminen de les dependències del projecte.

---

## ADR 006: Sistema de Versions i Rollback d'Agents [DECISIÓ PRESA]
- **Data:** 27 Març 2026
- **Context:** Com gestionem les actualitzacions d'agents en producció sense trencar res? Si un canvi falla, com tornem enrere?
- **Alternatives Considerades:**
  - **Git History:** Utilitzar git per versionar cada canvi.
  - **Snapshots de Fitxers:** Fer còpies completes de l'estat de l'agent abans de cada canvi.
  - **Delta/Diff:** Guardar només les diferències entre versions.
- **Decisió Presa:** **Snapshots complets a `/versions/` amb rollback via ticket.**
  - Abans de cada canvi, el Kernel fa un snapshot complet de `identity.md`, `llm_config.json` i `/skills/`.
  - Màxim 10 versions per agent (configurable).
  - Rollback via ticket `SYSTEM_ROLLBACK` executable per Genesis o operador humà.
  - Auto-cleanup de versions antigues.
- **Motiu:**
  1. **Simplicitat:** Snapshot complet és més fàcil de gestionar que deltes.
  2. **Integritat:** Una versió inclou tot l'agent, evitant inconsistències parcials.
  3. **Seguretat:** Només Genesis pot crear versions; operador pot fer rollback.
  4. **Recuperació:** Si un agent falla (loop infinit), es pot recuperar ràpidament.
- **Conseqüències:**
  - Cada departament té una carpeta `/versions/` amb snapshots.
  - Configuració a `.version_config.json`.
  - El rollback és total (tots els fitxers), no selectiu.

---

## ADR 007: API REST i Autenticació del Dashboard [DECISIÓ PRESA]
- **Data:** 27 Març 2026
- **Context:** El Dashboard i la TUI necessiten comunicar-se amb el Kernel. Com ho fem? Com autentiquem?
- **Alternatives Considerades:**
  - **gRPC:** Més eficient però requereix proto files i generació de codi.
  - **GraphQL:** Flexible però complex per a un sistema local.
  - **REST API + JSON:** Simple, estàndard, fàcil de debugar.
  - **Autenticació:** OAuth (massa complex), LDAP (overkill), Sessions (stateful), Tokens (stateless).
- **Decisió Presa:** **API REST amb JSON + Token JWT simple.**
  - Base URL: `http://<orange-pi>:8080/api/v1`
  - 14 endpoints definits (mètriques, tickets, aprovacions, engrames, logs).
  - Autenticació per Bearer Token (generat en instal·lació).
  - Model single-user (no multi-tenant).
  - Rate limiting: 100 requests/minute.
- **Motiu:**
  1. **Simplicitat:** REST és universal i fàcil de consumir des de HTMX/fetch.
  2. **Stateless:** El token porta tota la informació, no cal sessió al servidor.
  3. **Seguretat:** Token emmagatzemat a `/etc/agenticos/auth.token` (chmod 600).
  4. **Escalabilitat:** Si en el futur cal multi-usuari, es pot afegir sense trencar l'API.
- **Conseqüències:**
  - El Kernel implementa un servidor HTTP lleuger (Go net/http).
  - Totes les peticions autenticades necessiten header `Authorization: Bearer <token>`.
  - Dos rols: `operator` (tot) i `viewer` (només lectura).

---

## ADR 008: Separació WASM vs MCP per Domini [DECISIÓ PRESA]
- **Data:** 27 Març 2026
- **Context:** Tenim dos mecanismes per eines: WASM (sandboxed) i MCP (protocol estàndard). Quan usem cadascun?
- **Alternatives Considerades:**
  - **Tot WASM:** Màxim aïllament però limitat a recursos interns.
  - **Tot MCP:** Flexible però menys determinista.
  - **WASM per locals, MCP per externs:** Separació geogràfica.
  - **WASM per Kernel, MCP per Departaments:** Separació per domini.
- **Decisió Presa:** **Separació per Domini: WASM al Kernel (Ring 0), MCP als Departaments (Ring 1+).**
  - **WASM:** Eines del Kernel (validadors, parsers, math) - deterministes, aïllades.
  - **MCP:** Eines dels departaments (DB, HTTP, Git, LLM) - poden ser no-deterministes.
- **Motiu:**
  1. **Seguretat:** El Kernel només executa codi WASM verificable (Ring 0).
  2. **Flexibilitat:** Departaments poden usar qualsevol servei extern via MCP.
  3. **Claredat:** Regla simple: "Si és core → WASM, si és tool → MCP."
  4. **Determinisme:** Validacions crítiques són sempre WASM (predictibles).
- **Conseqüències:**
  - `/departments/shared/wasm/` per a mòduls del Kernel.
  - `/departments/shared/mcp/` per a configuracions MCP de departaments.
  - El Kernel no executa MCP directament, només el client MCP ho fa.

---

## ADR 009: Separació FastAuditor (Kernel) vs Verifier (Guardian) [DECISIÓ PRESA]
- **Data:** 28 Març 2026
- **Context:** Inconsistència crítica detectada entre documents. Qui fa la validació de seguretat? On resideix? Quin anell de privilegi té?
  - `01_KERNEL.md` parla de `FastAuditor` com a mòdul del Kernel (Ring 0).
  - `05_GUARDIAN.md` parla del `Guardian` com a departament de Ring 1.
  - `06_ORCHESTRATION.md` posa `auditor` com a Ring 0 dins de `01_guardian`.
  - `04_SEED.md` menciona `auditor` (Ring 0) generador de polítiques.
- **Problema:** Tres versions contradictòries convivint. Els implementadors no saben si el Guardian és Ring 0 o Ring 1, ni si l'Auditor és el Kernel o un agent.

- **Alternatives Descartades:**
  1. **Guardian com a Ring 0:** Col·locar tota la seguretat dins del Kernel. Descartat perquè el Kernel ha de ser minimalista i determinista. Validacions semàntiques (que requereixen LLM) no poden estar al Kernel.
  2. **Auditor com a agent separat:** Tenir un agent `auditor` dins de `01_guardian` que generi polítiques. Descartat per redundància amb el Verifier i per confusió de nomenclatura.
  3. **Nomenclatura "Auditor" per al component de Ring 0:** Descartat perquè "Auditor" suggereix revisió profunda (comptable), quan en realitat és una validació ràpida determinista.

- **Decisió Presa:** **Separació Clara de Responsabilitats:**
  - **FastAuditor:** Mòdul intern del **Kernel** (Ring 0). Codi Go purament determinista. Validació per regex/patró en <1ms. Sense LLM.
  - **Guardian:** **Departament** sencer (Ring 1). Conté tres rols: Verifier (validació semàntica LLM), Tester (pentesting), Compliance (auditoria).
  - **Verifier:** **Agent** dins del departament Guardian. Únic que fa validacions semàntiques amb LLM (Slow-Path).

- **Jerarquia de Validació:**
  ```
  Intent proposat
       ↓
  [FastAuditor - Kernel Ring 0] → Regex/patró → APPROVED/REJECTED/FAST_FAIL
       ↓ (si dubte)
  [Verifier - Guardian Ring 1] → LLM semàntic → APPROVED/REJECTED/SLOW_PATH
       ↓ (si dubte greu)
  [Human] → HITL → APPROVED/REJECTED
  ```

- **Motiu:**
  1. **Separació de Poders:** El Kernel (Ring 0) és "cec" només veu patrons. El Guardian (Ring 1) és "savi" però més lent. Això evita que el Kernel esdevingui monolític.
  2. **Rendiment:** El 80% dels casos passen per FastAuditor (<1ms), només el 20% van al Verifier (~segons).
  3. **Claredat:** Cada component té un nom únic i una ubicació única.
  4. **Seguretat:** Ring 0 és immutable (codi Go compilat). Ring 1 és mutable (agents amb identity.md).

- **Conseqüències:**
  - **Canvis a `06_ORCHESTRATION.md`:** La matriu de rols canvia `auditor (Ring 0)` per `verifier (Ring 1)`.
  - **Canvis a `01_KERNEL.md`:** Confirmar que FastAuditor és un mòdul intern (no un agent separat).
  - **Canvis a `05_GUARDIAN.md`:** Confirmar que el Guardian és Ring 1 i conté el Verifier (no Auditor).
  - **Eliminar referències:** Totes les referències a `auditor` com a Ring 0 fora del Kernel s'han de corregir.
  - **Nomenclatura:** "Auditor" ja no s'usa. Usem "FastAuditor" (Kernel) o "Verifier" (Guardian).

---

## ADR 010: Integració de Gaps Crítics als Documents de Design [2026-03-28]

- **Context:** Hem resolt 7 gaps crítics durant la sessió de consolidació final (SEC-001, SEC-002, DEP-001, DEP-002, GAP-004, GAP-005, DEP-004).
- **Decisió Presa:** Integrar tots els continguts als documents de design originals en lloc de crear un document temporal separat.
- **Motiu:** Mantenir la documentació unificada, evitar redundàncies i facilitar la navegació.
- **Integracions Realitzades:**
  - SEC-001 (Validació polítiques 3 capes) → `05_GUARDIAN.md`
  - SEC-002 (Rate limiting 60req/min) → `05_GUARDIAN.md`
  - DEP-001 (Contracte MCP complet) → `08_CONTEXT_BUILDER.md`
  - DEP-002 (Fallback Librarian) → `08_CONTEXT_BUILDER.md`
  - GAP-004 (Prompt Storage) → `07_ENGRAM.md`
  - GAP-005 (Flux truncament context) → `08_CONTEXT_BUILDER.md`
  - DEP-004 (LiteLLM fallback) → `01_KERNEL.md`

---

## ADR 011: Format d'`agenticos_state.md` [2026-03-28]

- **Context:** El Context Builder necessita un format estàndard per l'estat global del sistema.
- **Decisió Presa:** Estructura JSON amb metadades, agents, tickets, system_health i recursos.
- **Motiu:** Proporcionar context complet als agents sobre l'estat del sistema.
- **Ubicació:** `08_CONTEXT_BUILDER.md` §4.1

---

## ADR 012: Substitució de LiteLLM per Proxy LLM Propi [2026-03-28]

- **Data:** 28 Març 2026
- **Context:** El sistema necessitava un intermediari per a models LLM al núvol (Ollama per a models locals no és suficient per a models com Gemini o els proveïts via OpenCode).
- **Alternativa Original:** Utilitzar **LiteLLM** com a proxy universal.
- **Motiu del Canvi (LiteLLM Rebutjat):**
  1. **Seguretat:** Vulnerabilitat crítica detectada (LiteLLM hackejat).
  2. **Dependència externa:** LiteLLM és un projecte tercer amb les seves pròpies actualitzacions i vulnerabilitats.
  3. **Recursos:** LiteLLM requereix ~500MB RAM i múltiples dependències (Redis, etc.) - massa per a Orange Pi 5B.
  4. **Control:** No tenim control sobre el codi de LiteLLM.

- **Decisió Presa:** **Proxy LLM Propi (feat-002)** escrit en Go pur.
  - **Ubicació:** `02_implementation/cmd/llm-proxy/main.go`
  - **Port:** `localhost:4000`
  - **Proveïdors suportats:** Go, Zen, Gemini (via OpenCode API)
  - **Funcionalitats:**
    - HTTP server minimalista (<50MB RAM)
    - OpenAI-compatible endpoint (`/v1/chat/completions`)
    - Health check endpoint (`/health`)
    - Timeout configurat (30s per defecte)
    - Logging de peticions

- **Arquitectura Resultant:**
  ```
  Agent → LLM Proxy (:4000) → OpenCode API → Go/Zen/Gemini
                  ↑
  Ollama (models locals :11434) ← Kernel
  ```

- **Motiu de la Decisió:**
  1. **Zero Dependències:** Només stdlib de Go (no cal Redis ni altres serveis).
  2. **Seguretat:** Codi propi, auditable, sense vulnerabilitats externes conegudes.
  3. **Rendiment:** <50MB RAM vs ~500MB de LiteLLM.
  4. **Control:** Tenim control total sobre el proxy.

- **Conseqüències:**
  - **LiteLLM eliminat** de tots els documents com a opció de fallback.
  - **01_KERNEL.md §3.7.3** actualitzat per utilitzar el proxy propi.
  - **09_EXTENSIBILITY.md §5.2** documenta el proxy propi com a única opció cloud.
  - **Configuració:** `config/llm.json` conté la configuració del proxy.
  - **Dependència eliminada:** `github.com/Berryai/LiteLLM` de qualsevol dependència.

- **Implementació:**
  - `cmd/llm-proxy/main.go` - Servidor HTTP
  - `internal/llm/client.go` - Client HTTP per a proveïdors
  - `internal/llm/config.go` - Configuració YAML/JSON
  - `internal/llm/types.go` - Estructures de request/response

---

## ADR 013: Substitució de HTMX+Mermaid per React+ReactFlow al Dashboard [2026-03-29]

- **Data:** 29 Març 2026
- **Context:** El Dashboard web necessitava visualitzar fluxos d'agents en temps real amb alta interactivitat (drag, zoom, pan, selecció de nodes).
- **Alternativa Original:** Utilitzar **HTMX + Mermaid.js** per al Dashboard.
- **Motiu del Canvi (HTXM+Mermaid Rebutjat):**
  1. **Interactivitat limitada:** Mermaid només ofereix visualització estàtica, no permet drag de nodes ni interacció avançada.
  2. **Updates inefficients:** HTMX requereix polling o re-render complet del SVG per actualitzacions.
  3. **Model d'estat:** El graf d'agents canvia dinàmicament i necessita un model d'estat client robust.
  4. **Experiència d'usuari:** Per a un "IDE Agentic", cal una UI professional i responsiva.

- **Decisió Presa:** **React + ReactFlow** per al Dashboard web.
  - **Ubicació:** `02_implementation/cmd/webui/`
  - **Stack:** React 18 + ReactFlow + Tailwind CSS + Vite
  - **Comunicació:** WebSocket per updates en temps real (no polling)
  - **Funcionalitats:**
    - Nodes interactius (drag, zoom, pan)
    - Actualitzacions incrementals via WebSocket
    - Chat integrat (missatges → tickets)
    - Inspector de nodes
    - Safata d'aprovacions HITL

- **Arquitectura Resultant:**
  ```
  Browser (React + ReactFlow)
           ↕ WebSocket
  Kernel Go (API REST + WS Server)
  ```

- **Motiu de la Decisió:**
  1. **Interactivitat:** ReactFlow ofereix drag, zoom, pan, selecció de nodes.
  2. **Updates en temps real:** WebSocket permet updates incrementals sense re-render.
  3. **Ecosistema madur:** React és estàndard de la indústria, ben documentat.
  4. **Separació de responsabilitats:** Frontend gestiona UI, backend gestiona lògica.

- **Conseqüències:**
  - **HTMX eliminat** del stack del Dashboard (es manté al Glossari per històric).
  - **Mermaid.js** ara només per a documentació i exports, no per UI principal.
  - **10_OBSERVABILITY.md §5.3** actualitzat a v8 amb React + ReactFlow.
  - **01_MANIFEST.md** actualitzat amb el nou stack.
  - **02_GLOSSARY.md** actualitzat amb React + ReactFlow.
  - **TUI Bubbletea** es manté com a "God Mode" via SSH (no es reemplaça).

- **Implementació:**
  - `cmd/webui/` - Projecte React amb Vite
  - `src/components/Dashboard.tsx` - Layout principal
  - `src/components/FlowCanvas.tsx` - ReactFlow wrapper
  - `src/hooks/useWebSocket.ts` - Client WebSocket amb reconnect
  - **Tests:** 13 tests passen (100%)

---

## ADR 014: Session Tree - Sistema de Control de Versions per Execucions d'Agents [2026-04-02]

- **Data:** 2 Abril 2026
- **Context:** El sistema actual de tickets és lineal: cada ticket és independent, no hi ha historial de branques ni capacitat de "time-travel". Quan un usuari fa una pregunta i l'agent suggereix dues alternatives, no hi ha manera d'explorar una alternativa sense perdre l'altra.
- **Problema:** Les converses d'agents són tírpicamente no-lineals: l'agent explora, suggereix opcions, fa forks mentals. El model lineal no reflecteix la realitat de com treballen els agents.
- **Alternatives Considerades:**
  - **Llista lineal de sessions:** Simple però no suporta branching.
  - **Git-like backend complet:** Massa complex per l'MVP.
  - **Event sourcing:** Massa infraestructura per l'MVP.
  - **Graf simple amb branching manual:** Just right per l'MVP.

- **Decisió Presa:** **Session Tree amb branching funcional.**
  - Cada sessió és un **DAG** (Directed Acyclic Graph), no una llista lineal.
  - Cada node és un **snapshot** de: missatge, context, tool_calls, resultats.
  - L'usuari pot **crear branques** ("forks") a qualsevol node.
  - Es pot fer **"checkout"** a qualsevol branca i continuar des d'allí.
  - El **Context Builder** pot ensamblar prompts des de qualsevol branca.

- **Arquitectura:**
  ```
  Session (DAG)
  ├── Branch "main"
  │   ├── Node 1 (user_message)
  │   ├── Node 2 (agent_response)
  │   ├── Node 3 (tool_call: fs_read)
  │   └── Node 4 (branch_point) → Branch "exploring-zustand"
  │
  └── Branch "exploring-zustand" (forked from Node 4)
      ├── Node 5 (user_message)
      └── Node 6 (agent_response)
  ```

- **Components:**
  - **SessionStore** (`internal/session/store.go`): CRUD de sessions, nodes, branques
  - **BranchContextBuilder**: Extensió del Context Builder per branques
  - **ToolIndexer**: Indexa tool_calls a Engrams per cerca semàntica
  - **SessionTreePanel**: React component amb ReactFlow per visualitzar l'arbre

- **Motiu de la Decisió:**
  1. **Reflecteix la realitat:** Els agents treballen de forma no-lineal.
  2. **Time-travel:** Permet tornar a estats anteriors i provar alternatives.
  3. **Cerca semàntica:** Els tags i l'indexació de tool_calls permeten cerques avançades.
  4. **Context management:** El branching permet gestió intel·ligent del context.

- **MVP Scope:**
  - **Inclòs:** SessionStore, CRUD bàsic, checkout de branca, tags automàtics
  - **Exclòs:** Time-travel real, cerca semàntica, multi-agent presence, context compaction

- **Conseqüències:**
  - **Nou document:** `SDD/design/feat-013-session-tree.md` (disseny complet)
  - **Nou feature:** `SDD/features_for_specs/feat-013.json`
  - **Nou mòdul:** `internal/session/` (a implementar)
  - **Integració:** Tickets, Context Builder, Engrams, Dashboard

---

*Document actualitzat: 2026-04-02*





---

## ADR 026: Consolidació del lot curt de validació SDD i hardening runtime [2026-04-06]

- **Data:** 2026-04-06
- **Context:** Després de validar el flux SDD amb peces curtes i de tancar el contracte mínim del ticket, s'han completat diverses peces petites de runtime, context i reporting que ja no han de continuar vivint com a "pendents" difusos al parking lot.
- **Decisió Presa:** Es dona per consolidat aquest lot curt:
  1. `feat-018` tanca la base resilient del `context-engine` (fallback textual, degradació segura i validació reforçada).
  2. `feat-020` implementa l'export Markdown mínim dels reports existents.
  3. `SEC-00C` queda cobert pel test existent `TestReActLoop_ToolBlockedByGuardian`.
  4. `SEC-00A` queda implementat amb fix de falsos positius a `ValidatePath`.
  5. `SEC-00B` queda implementat com a hardening mínim d'`execute_command`.
- **Conseqüències:**
  - `CTX-02` es considera tancat en la seva base resilient; només `CTX-02B` i `CTX-02C` continuen com a pendents futurs.
  - `TLS-01` queda absorbit per l'estabilització del ticket/runtime i no s'obre com a feature independent.
  - `RPT-03` queda parcialment cobert: Markdown implementat; PDF continua pendent.
  - El següent pas natural del bloc `SEC-00` passa a ser `SEC-00D` o `SEC-00E`, no reobrir `SEC-00A/B/B2/C`.
