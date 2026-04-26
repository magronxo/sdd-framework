# 04. Parking d'Idees i Gaps

> **Actualitzat:** 2026-04-12 (v32)
> **Estat:** Només pendents, seeds i futures. Tot el que ja és decisió presa o implementació completada s'ha de viure a l'ADR.

---

## INDEX + Invariants (OBLIGATORI)

Aquest document és un **INDEX** (punt d'accés). El detall llarg ha de viure a:

- PRE-SDD batch reports: `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/`
- PRE-SDD normalization reports: `00_project_documentation/SDD/artifacts/pre_sdd/pklot_normalization/`
- Decisions estables / implementacions consolidades: `00_project_documentation/05_ADR_DECISION_LOG.md`

**Ordre de seccions (fix)**

1. `🚨 0. Blockers`
2. `🌱 1. SEEDS (PRE-SDD)` (únic lloc on apareix `SEED-*`)
3. `📋 2. NOW backlog executable (proper 7-14 dies)` (feina concreta; mai `SEED-*`)
4. `📊 3. Deferred backlog` (feina no imminent; agrupada per domini)
5. `📦 4. Deployments` (notes operatives; decisions estables → ADR/CD)

**Definicions curtes**

- **Seeds (PRE-SDD)**: idees (`SEED-*`) amb `Horizon: NOW|NEXT|LATER`. No són tasques.
- **NOW backlog**: treball executable en 7–14 dies. Manté l'esquema de tasques (`⬜/✅/📋`).
- **Deferred backlog**: backlog útil però no imminent. Continua sent "feina", no "seed".
- **Blockers**: estat curt + links. Pot incloure **snapshots datats** (informació volàtil), però no s'ha de promoure a ADR/CD per defecte.
- **Deployments**: notes de desplegament. Decisions estables, si cal, a ADR/CD (el PKLot només enllaça).

---

## 📌 Format de tasques

| Camp | Descripció | Valors |
|------|------------|--------|
| **ID** | Identificador únic | `PREFIX-NNN` |
| **Descripció** | Què es fa | text |
| **Surface Impact** | On impacta | `none` / `dashboard` / `tui` / `telegram` / `all` |
| **Consumer** | Component que ho consumeix | nom del component o `none` |
| **Prioritat** | Urgència | `ALTA` / `MITJANA` / `BAIXA` |
| **Estat** | Estat actual | `⬜ Pendent` / `✅ Fet` / `📋 Dissenyat` |

**`all` = dashboard + tui + telegram**

---

## 🚨 0. Blockers

**Tots els blockers estan resolts.** Veure ADR Decision Log per detalls.

### LLM extern - Estat

**Estat:** ✅ RESOLT

**Snapshot (volatile)**
- **Data:** 2026-04-08
- Aquesta llista canvia amb el temps; no és ADR/CD per defecte.

**Models disponibles a OpenCode.ai (verificats):**
- gpt-5.4, gpt-5.4-pro, gpt-5.4-mini, gpt-5.4-nano
- glm-5, kimi-k2.5, minimax-m2.5, minimax-m2.5-free
- claude-3-5-haiku, big-pickle

---

## Com capturar seeds (PKLot Seed v1)

Quan capturis una seed nova, usa el template **PKLot Seed v1**:
`00_project_documentation/SDD/artifacts/pre_sdd/templates/pklot_seed_v1.md`

**Regla de detall:**
- Si la seed és **< 10 línies** d'anàlisi → queda al PKLot directament
- Si la seed necessita **> 10 línies** → crear Seed Dossier a `artifacts/pre_sdd/seed_dossiers/SEED-NN.md` i enllaçar des del camp `batch_ref`

**Camp `exploration_required`** — ha d'estar a `true` si:
- Estimació >2 dies
- ≥2 incògnites tècniques
- Afecta invariants/kernel/security

Veure [PRE_SDD_CONTRACT.md](./SDD/artifacts/pre_sdd/PRE_SDD_CONTRACT.md) per l'estat complet de pre-SDD.

---

## 🌱 1. SEEDS (PRE-SDD)

Quan surt una idea d'inspiració, no la converteixis encara en spec. Desa-la aquí com a `seed`.

| Camp | Descripció | Valors |
|------|------------|--------|
| **ID** | Identificador curt | `SEED-NNN` |
| **Títol** | Nom de la idea | text curt |
| **Trigger** | Què la va disparar | observació / bug / brainstorming / feedback |
| **Idea** | Què proposes | 1-3 frases |
| **Impacte potencial** | On podria afectar | `file tree` / `session tree` / `dashboard` / `context` / `workflow` / `all` |
| **Risc de drift** | Si es pot confondre amb contracte | `baix` / `mitjà` / `alt` |
| **Horizon** | Quan val la pena portar-la a triatge | `NOW` / `NEXT` / `LATER` |
| **Estat (PRE-SDD)** | Estat operatiu del triatge | `Captured` / `Classified` / `Analyzed` / `Selected` / `Triaged` / `Decomposed` / `Converted` / `Archived` |
| **Batch ref** | Link al batch de triatge (si aplica) | path canònic a `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/...` |
| **Destí probable** | On podria acabar | `parking lot` / `ADR` / `spec` / `task` |

**Regla d'or de les seeds**
- Si encara és inspiració, va al `parking lot`.
- Si ja hi ha decisió arquitectònica, va a `ADR`.
- Si canvia comportament observable, va a `spec` i `tasks`.
- Si només és un apunt d'implementació, queda com a `task`.

Nota: `SEED-06` es va renomenar a `DEP-01` (deployment validation) segons `00_project_documentation/SDD/artifacts/specs/feat-024-pklot-restructure.md`; el gap és intencional.

### Exemple

| Camp | Valor |
|------|-------|
| **ID** | `SEED-01` |
| **Títol** | Workspace roots al file tree |
| **Trigger** | Brainstorming de dashboard IDE |
| **Idea** | El file tree hauria de poder carregar múltiples roots, com un workspace de VS Code. |
| **Impacte potencial** | `file tree` / `dashboard` |
| **Risc de drift** | `mitjà` |
| **Horizon** | `NEXT` |
| **Estat (PRE-SDD)** | `Converted` |
| **Batch ref** | `SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-09.md` |
| **Destí probable** | `ADR` |

### Seeds estratègiques capturades

| Camp | Valor |
|------|-------|
| **ID** | `SEED-02` |
| **Títol** | HuggingFace Downloader com a actiu estratègic futur |
| **Trigger** | Brainstorming sobre models locals, hardware profiles i catàleg de models |
| **Idea** | Avaluar la connexió futura entre AgenticOS i un downloader/analitzador de repos de models que avui existeix en Python, amb possible reescriptura en Go més endavant. |
| **Impacte potencial** | `workflow` / `context` / `all` |
| **Risc de drift** | `mitjà` |
| **Horizon** | `LATER` |
| **Estat (PRE-SDD)** | `Captured` |
| **Batch ref** | (buit) |
| **Destí probable** | `ADR` |

| Camp | Valor |
|------|-------|
| **ID** | `SEED-03` |
| **Títol** | GitHub Actions i CI com a capa de professionalització |
| **Trigger** | Necessitat futura d'automatitzar validacions i reforçar qualitat |
| **Idea** | Integrar CI i GitHub Actions quan el core estigui més estable, per automatitzar tests, gates documentals i validacions bàsiques sense codificar caos massa aviat. |
| **Impacte potencial** | `workflow` |
| **Risc de drift** | `baix` |
| **Horizon** | `LATER` |
| **Estat (PRE-SDD)** | `Captured` |
| **Batch ref** | (buit) |
| **Destí probable** | `ADR` |

| Camp | Valor |
|------|-------|
| **ID** | `SEED-04` |
| **Títol** | User Shadow / Adversarial Co-Pilot |
| **Trigger** | Brainstorming sobre autonomia futura, HITL i modelatge del criteri de l'usuari |
| **Idea** | Explorar un agent observador que aprengui patrons de decisió i imaginari conceptual de l'usuari. Fase inicial: ombra observadora i conseller adversarial; fases posteriors eventuals: delegació parcial limitada. No plantejar-lo com a component de seguretat ni com a substitut del Zero Trust. |
| **Impacte potencial** | `workflow` / `context` / `all` |
| **Risc de drift** | `alt` |
| **Horizon** | `LATER` |
| **Estat (PRE-SDD)** | `Explored` |
| **Batch ref** | `SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12_addendum_02.md` |
| **Destí probable** | `ADR` |

Notes: veure `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-04.md` — entry_checklist 11/11 (2026-04-12); capabilities converted to 9 testable GIVEN/WHEN/THEN statements

| Camp | Valor |
|------|-------|
| **ID** | `SEED-05` |
| **Títol** | Execution Trace Contract + Flow Projection |
| **Trigger** | Brainstorming sobre observabilitat, Session Tree i representació visual d'execucions |
| **Idea** | Definir primer un contracte de traça d'execució per AgenticOS i només després projectar-la visualment al dashboard amb ReactFlow. La traça hauria de capturar passos reals, handoffs, decisions, eines usades, estat del ticket i punts HITL/auditoria. La vista flow no seria la font de veritat, sinó una projecció de la traça operativa. |
| **Impacte potencial** | `dashboard` / `workflow` / `all` |
| **Risc de drift** | `mitjà` |
| **Horizon** | `LATER` |
| **Estat (PRE-SDD)** | `Archived` |
| **Batch ref** | `SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12_addendum.md` |
| **Destí probable** | `spec` |

Notes: veure `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-05.md` — completed (2026-04-12), handoff to `feat-068`. Feature archived as `ARCHIVED` with PASS validation/verify/audit. Implementation: `02_implementation/internal/api/trace.go`.

| Camp | Valor |
|------|-------|
| **ID** | `SEED-07` |
| **Títol** | LLM Proxy hardening + capability study post-LiteLLM |
| **Trigger** | Revisió del proxy propi després d'abandonar LiteLLM per risc de compromís extern |
| **Idea** | Contrastar de manera estructurada el proxy propi actual amb les capacitats de valor afegit de LiteLLM per decidir quines funcions realment aporten robustesa a AgenticOS i quines serien sobreenginyeria o risc innecessari. La línia d'estudi hauria de separar clarament: gateway mínim segur, routing/resiliència, governança d'accés/cost i capacitats enterprise opcionals. |
| **Impacte potencial** | `workflow` / `context` / `all` |
| **Risc de drift** | `mitjà` |
| **Horizon** | `NEXT` |
| **Estat (PRE-SDD)** | `Converted` |
| **Batch ref** | `SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-09.md` |
| **Destí probable** | `ADR` |

Notes: veure `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-07.md`

| Camp | Valor |
|------|-------|
| **ID** | `SEED-08` |
| **Títol** | Provider connections contract (multi-provider connect) |
| **Trigger** | Model/provider discovery i dependència d'un catàleg extern (OpenCode) |
| **Idea** | Definir un contracte estable perquè l'usuari pugui connectar proveïdors principals (i llistar models) via configuració/API, i tractar "afegir un provider nou" com una extensió incremental verificable (no com una llista volàtil dins del PKLot). |
| **Impacte potencial** | `workflow` / `context` / `all` |
| **Risc de drift** | `mitjà` |
| **Horizon** | `NEXT` |
| **Estat (PRE-SDD)** | `Converted` |
| **Batch ref** | `SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-08.md` |
| **Destí probable** | `spec` |

| Camp | Valor |
|------|-------|
| **ID** | `SEED-09` |
| **Títol** | Chat → Ticket Promotion Contract |
| **Trigger** | Necessitat de distingir deterministicament resposta immediata vs creacio de ticket |
| **Idea** | Definir un contracte on `requested_mode` a `/api/v1/llm/chat` determini si la resposta es 200 (directa) o 201/202 (ticket creat). Comportament per defecte `auto` amb fallback a ticket. Errors deterministes reutilitzant codis existents. |
| **Impacte potencial** | `kernel` / `workflow` / `all` |
| **Risc de drift** | `baix` |
| **Horizon** | `NOW` |
| **Estat (PRE-SDD)** | `Captured` |
| **Batch ref** | `SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12_chat_ticket_promotion.md` |
| **Destí probable** | `feat-XXX` |

Notes: veure `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-09.md` — dossier v1 complet (2026-04-12); feature proposal a `SEED-09_feature_proposal.md`

---

## 📋 2. NOW backlog executable (proper 7-14 dies)

### Deployment - Pendent

| ID | Tasca | Surface | Consumer | Prioritat | Estat |
|----|-------|---------|----------|-----------|-------|
| **DEP-01** | Validar desplegament a OPI5B | none | none | ALTA | ⬜ Pendent |

**Completed (see ADR)**

- `CTX-02` → `05_ADR_DECISION_LOG.md` (CD-020)
- `TLS-01` → `05_ADR_DECISION_LOG.md` (CD-021)
- `feat-019` → ADR 024 + ADR 025 + `00_project_documentation/SDD/audit_reports/feat_019_manual_verification_2026-04-05.md`

Traçabilitat: CTX-02A està elevat a `00_project_documentation/SDD/artifacts/features_for_specs/feat-018.json`.

---

## 📊 3. Deferred backlog

### Scheduler i Reports

| ID | Tasca | Surface | Consumer | Prioritat | Estat |
|----|-------|---------|----------|-----------|-------|
| **RPT-03** | ReportExport (PDF pendent; MD via feat-020) | dashboard | RPT-02 | MITJANA | 📋 Dissenyat |

**Implementat:** SCHED-01 a SCHED-04, RPT-01 a RPT-02 i export Markdown mínim via `feat-020`. Veure ADR Decision Log.

### Session Tree - Pendent (Fase 2)

| ID | Tasca | Surface | Consumer | Prioritat | Estat |
|----|-------|---------|----------|-----------|-------|
| **SESS-06** | BranchContextBuilder | none | SESS-07 | MITJANA | ⬜ Pendent |
| **SESS-07** | Tags automàtics (I/O) | none | SESS-08 | MITJANA | ⬜ Pendent |
| **SESS-08** | ToolIndexer a Engrams | none | SESS-07 | MITJANA | ⬜ Pendent |
| **SESS-11** | SessionGraph (ReactFlow) | dashboard | SESS-10 | MITJANA | ⬜ Pendent |

**Endpoint pendents:**
- DELETE /api/v1/sessions/:id
- GET /api/v1/sessions/:id/nodes

**MVP (SESS-01 a SESS-05):** ✅ Completat - veure ADR Decision Log CD-012

### LLM: model híbrid (cloud + local)

| Agent | Model | Raó |
|-------|-------|-----|
| **Genesis** | Cloud (GPT-4o/Claude) | Decisions complexes |
| **IT Ops** | Local (Mistral/Llama) | Tasques rutinàries |
| **Dev** | Cloud per audits, local per altres | Qualitat crítica |
| **Guardian** | Cloud (Claude) | Auditoria seriosa |
| **Librarian** | Local | Cerca simple |
| **Researcher** | Cloud (uncensored) | Qualitat informació |

---

### 🔒 Security & Operations

### Security Model (SEC-01)

| ID | Component | Surface | Consumer | Prioritat | Estat |
|----|-----------|---------|----------|-----------|-------|
| **SEC-00** | Guardian hardening (heuristiques + args) → CD-022 + feat-047 | none | Guardian | ALTA | ✅ Implementat |
| **SEC-01** | Modes de seguretat (enforcement real) → ADR 028 + feat-049 | all | ModeSelector | ALTA | ✅ Implementat |
| **SEC-01b** | Kernel status invariants mínims (observability) → feat-050 | dashboard | KernelPanel | ALTA | ✅ Implementat |
| **SEC-01c** | Emergency overlays (SAFE_MODE/LOCKDOWN) → feat-051 | all | KernelPanel | ALTA | ✅ Implementat |

**Nota de traçabilitat externa**
- SEC-00 neix de l'avaluacio comparada amb claw-code.
- Objectiu: reforcar el Guardian sense moure AgenticOS cap a un model agent-centric.

**Baseline completat**
- Veure `05_ADR_DECISION_LOG.md` (CD-022) per les peces ja implementades (`SEC-00A/SEC-00B/SEC-00B2/SEC-00C`).
- `SEC-00D/E/F` implementats (feat-047, 2026-04-11).

**Desglossament operatiu de `SEC-00`**
- `SEC-00A`: corregir boundary enforcement de `ValidatePath` per evitar falsos positius per prefix textual ✅ Fet (2026-04-06)
- `SEC-00B`: afegir validacio semantica minima d'arguments per `execute_command` ✅ Fet (2026-04-06)
- `SEC-00C`: centralitzar el pas `guardian before execution` al punt d'entrada real d'execucio ✅ Fet (test existent validat el 2026-04-06)
- `SEC-00D`: definir classificacio inicial de comandes `read-only` vs `destructive` ✅ Fet (2026-04-11)
- `SEC-00E`: delimitar `http_request` i altres tools d'efecte amb rails basics abans d'execucio ✅ Fet (2026-04-11)
- `SEC-00F`: afegir tests end-to-end que provin que una tool perillosa no pot executar-se si falla la validacio ✅ Fet (2026-04-11)
- `SEC-00B2`: delimitar validacio minima d'URL per `http_request` com a peça separada de `execute_command` ✅ Fet (2026-04-06)

**Ordre recomanat**
1. `SEC-00A` ✅ Fet
2. `SEC-00C` ✅ Fet — test `TestReActLoop_ToolBlockedByGuardian` valida guardian before execution (2026-04-06)
3. `SEC-00B` ✅ Fet — hardening mínim d'`execute_command`
4. `SEC-00B2` ✅ Fet — hardening mínim d'`http_request` contra SSRF i esquemes perillosos (2026-04-06)
5. `SEC-00D` ✅ Fet (2026-04-11)
6. `SEC-00E` ✅ Fet (2026-04-11)
7. `SEC-00F` ✅ Fet (2026-04-11)

| **SEC-02** | Permisos mínims (surface authority + step-up local fort) → feat-059 + feat-064 | none | api-server | ALTA | ✅ Implementat |
| **SEC-03** | Kernel Mediation (no bypass FS) → feat-060 | none | api-server | ALTA | ✅ Implementat |
| **SEC-04** | Registre d'accions (MVP two-tier) → feat-055 | all | AuditPanel | ALTA | ✅ Implementat |
| **SEC-05** | Informes seguretat (MVP) → feat-065 | dashboard | ReportViewer | MITJANA | ✅ Implementat |

**Nota d'abast**
- `SEC-02` (autoritat per superfície) s'ha cobert amb un tall mínim: `feat-059` (surface authority) + `feat-064` (step-up local fort per FULL) + `feat-061` (clear overlay local fort). El bloc “permisos” complet (RBAC/ACL) continua fora d'abast per ara.
- `SEC-01e` (sortida d'emergència d'overlay quan l'API no respon) s'ha cobert amb `feat-062`.
- Backpressure kernel-side (no només API) s'ha cobert amb `feat-063` (admission control al kernel llegint `backpressure_state.json` i fusionant senyals). L'observabilitat i monitors continuen a `api-server` (veure `feat-052`, `feat-053`, `feat-054`).

### Mans virtuals (HITL)

| ID | Tasca | Surface | Consumer | Prioritat | Estat |
|----|-------|---------|----------|-----------|-------|
| **MAN-01** | Eina execute_direct | none | none | ALTA | ⬜ Pendent |
| **MAN-02** | Dashboard panel HITL | dashboard | ApprovalPanel | ALTA | ⬜ Pendent |
| **MAN-03** | Workflow complet HITL | all | MAN-01 + MAN-02 | ALTA | ⬜ Pendent |
| **MAN-04** | Config per agent | none | none | MITJANA | ⬜ Pendent |

### Operacions i infraestructura

| ID         | Tasca                       | Surface | Consumer | Prioritat | Estat     |
| ---------- | --------------------------- | ------- | -------- | --------- | --------- |
| **OPS-01** | systemd service             | none    | none     | ALTA      | ⬜ Pendent |
| **OPS-02** | Reverse proxy HTTPS         | none    | none     | ALTA      | ⬜ Pendent |
| **OPS-03** | Firewall ports 8080, 443    | none    | none     | MITJANA   | ⬜ Pendent |
| **OPS-04** | Perfils LLM (local + cloud) | none    | none     | ALTA      | ⬜ Pendent |
| **OPS-05** | Snapshots VM Proxmox        | none    | none     | MITJANA   | ⬜ Pendent |

---

### 🔌 Integrations

### LLM Providers - Pendent

| ID | Proveidor | Surface | Consumer | Prioritat | Estat |
|----|-----------|---------|----------|-----------|-------|
| **LLM-05** | OpenAI directe | none | none | Alta | ⬜ Pendent |
| **LLM-07** | DeepSeek | none | none | Alta | ⬜ Pendent |
| **LLM-08** | Groq | none | none | Mitjana | ⬜ Pendent |

---

### 🔮 Explore / Futures

No implementar ara. En estudi.

| ID | Descripció | Prioritat | Notes |
|----|-----------|-----------|-------|
| **MULTI-01** | Arquitectura pare-fill | ALTA | En estudi |
| **MULTI-02** | Protocol comunicacio inter-OS | ALTA | En estudi |
| **MULTI-03** | Dashboard multi-seed | MITJANA | En estudi |
| **MULTI-04** | Model negoci remot | MITJANA | En estudi |
| **FUT-01** | Semantic Cache | MITJANA | Dissenyat |
| **FUT-02** | Redis Cache | BAIXA | Sense disseny |
| **FUT-04** | Home Assistant Voice | BAIXA | Fase 3+ |
| **UNC-01** | Perfil LLM uncensored | MITJANA | Dissenyat |
| **UNC-02** | Selector proveidor al Dashboard | MITJANA | Dissenyat |
| **CTX-01** | High-Res Context (Model Large) | BAIXA | Re-indexar amb text-embedding-3-large en fites per a màxima precisio |
| **FLOW-01** | Adversarial audit gating | MITJANA | Inspirat en `claw-code`; aplicar quan el flux extern sigui estable |
| **CTX-03** | Semantic compression al Context Builder | MITJANA | No implementar ara; futur despres de consolidar `feat-018` i budgets reals |

---

### 📖 Manual d'usuari

| ID | Secció | Surface | Consumer | Prioritat | Estat |
|----|--------|---------|----------|-----------|-------|
| **DOC-01** | Introducció | none | Manual | ALTA | ⬜ Pendent |
| **DOC-02** | Instal·lació | none | Manual | ALTA | ⬜ Pendent |
| **DOC-03** | Dashboard | none | Manual | ALTA | ⬜ Pendent |
| **DOC-04** | TUI | none | Manual | ALTA | ⬜ Pendent |
| **DOC-05** | Configuració | none | Manual | ALTA | ⬜ Pendent |
| **DOC-06** | Seguretat | none | Manual | ALTA | ⬜ Pendent |
| **DOC-07** | Primers Passos | none | Manual | ALTA | ⬜ Pendent |
| **DOC-08** | Resolució Problemes | none | Manual | MITJANA | ⬜ Pendent |

---

## 📦 4. Deployments

### Estructura creada

```text
03_deployments/
├── setup.ps1
└── seed/
    ├── agents/
    │   ├── genesis.json
    │   ├── it_ops.json
    │   ├── dev.json
    │   └── librarian.json
    ├── departments/
    │   ├── genesis.json
    │   ├── it_ops.json
    │   ├── dev.json
    │   └── librarian.json
    └── policies/
        └── fastpath.json
```

### Decisions preses

**Traçabilitat:** veure `05_ADR_DECISION_LOG.md` (CD-006).

| Pregunta | Resposta |
|----------|----------|
| System prompts | Individuals, reemplacen codi, carrega lazy |
| Eines | Dins agents/*.json (camp tools) |
| Guardian | Component, no agent |
| Format | JSON (YAML prohibit) |
| API llegeix de | agenticos_data/ (copi via setup.ps1) |
