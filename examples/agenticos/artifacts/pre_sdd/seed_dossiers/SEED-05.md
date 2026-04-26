# SEED-05 — Execution Trace Contract + Flow Projection

> Dossier v1 — updated 2026-04-12 for next triage

---

## Dades de referència (del PKLot)

- **ID:** `SEED-05`
- **Títol:** Execution Trace Contract + Flow Projection
- **Trigger:** Brainstorming sobre observabilitat, Session Tree i representació visual d'execucions
- **Idea:** Definir primer un contracte de traça d'execució per AgenticOS i només després projectar-la visual al dashboard amb ReactFlow. La traça hauria de capturar passos reals, handoffs, decisions, eines usades, estat del ticket i punts HITL/auditoria. La vista flow no seria la font de veritat, sinó una projecció de la traça operativa.
- **Impacte potencial:** `dashboard` / `workflow` / `all`
- **Risc de drift:** `mitjà`
- **Horizon:** `LATER`
- **Estat (PRE-SDD):** `Adopted` — seed adoptada per SDD (2026-04-12)
- **Batch ref:** triage_2026-04-12_addendum.md
- **Destí probable:** `ADR` (contracte, no feature)

---

## problem

El dashboard actual no té manera de representar executions passades d'una manera consultable i visual. No existeix traçabilitat entre "què ha passat" i "com es mostra al flow".

## intent

Definir un contracte de traça d'execució que capturi passos reals, handoffs, decisions, eines usades, estat del ticket i punts HITL/auditoria. Després projectar aquesta traça al dashboard com a visualització, sense que la visualització sigui la font de veritat.

## scope_in

- Schema de traça: passos, handoffs, decisions, eines, estat, HITL/auditoria
- Contracte entre kernel i dashboard (comunicació de traça)
- Projecció visual ReactFlow (quan hi hagi traça disponible)
- Relació traça/flow/plan/state machine (separar clarament)

## scope_out

- Implementació d'agent autònom que generi traces (només el contracte)
- Crawler de logs historic
- Persistència de traces com a dada primària (el contracte, no l'emmagatzematge)
- UI de debug en temps real (fora de scope MVP)

## capabilities

El sistema ha de poder:

1. **Generar traça estructurada per cada execució significativa** — cada event de traça conté: timestamp, component emissor, tipus event, payload, trace_id correlatiu
2. **Capturar handoffs entre components** — quan un agent passa control a un altre, la traça registra: source_component, target_component, reason, control_transfer
3. **Registrar decisions preses** — cada decisió inclou: context, options_considered, chosen_option, rationale, agent_id
4. **Incloure estat del ticket associat** — cada event de traça referencia el ticket_id i l'estat en aquel moment
5. **Marcar punts HITL/auditoria** — quan una decisió requereix aprovació humana, la traça registra: hitl_trigger, approval_status, approver_id, timestamp
6. **Projectar traça al dashboard via API** — el dashboard pot fer GET /api/v1/traces/{trace_id} i rebre la traça completa en JSON

## approach

### Home Assistant Study — Mini Analysis

Home Assistant (HA) automations tracció sistema com a referència:

**Què COPIEM (patrons útils):**
- **Trace-as-event-stream**: HA tracta traces com una seqüencia d'esdeveniments amb timestamp i source. Agafem: events amb timestamp, component, payload.
- **Branching visualization**: HA mostra automations com grafs amb nodes i edges. Agafem: visualització de flow com graph, no com timeline lineal.
- **Debug operatiu**: HA permet veure "per què va passar açò" amb traces navegables. Agafem: trace viewer amb cerca per component/tipus.
- **Confidence visual**: HA usa colors per indicar estat d'entitats. Agafem: colors segons estat (success/warning/error) a la projecció ReactFlow.

**Què NO COPIEM (no aplicable):**
- **Entitats internes HA**: HA traccia dispositius i estats d'entitats. NO copiem Açò — AgenticOS no té "entities" similars.
- **Service calls com a trace units**: HA traccia service calls. NO — les nostres unitats son agents/tools/handoffs, no services.
- **Persistencia automàtica a DB**: HA guarda tot a MariaDB. NO — AgenticOS genera traces a Action Log (feat-055), no té DB pròpia.
- **Timeline view per defecte**: HA mostra traces en timeline vertical. NO — AgenticOS ja té ReactFlow; preferim graph view.

**Conclusió**: Copiem el patró de trace-com-events + graph visualization, adaptat a agents (no entities) i Action Log (no DB).

## risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scope creep cap a implementació d'agent complet | High | Contracte de traça només; no inclou lògica d'agent |
| Confondre traça amb visualització | Medium | Contracte explícito que dashboard és projecció, no font |
| Performance en generar traces per cada acció | Low | Només execucions "significatives", no cada pas atòmic |

## success_signals

- [ ] El contracte de traça està documentat i aprovat
- [ ] El kernel pot generar traça seguint el contracte
- [ ] El dashboard pot rebre traça i projectar-la visualment
- [ ] La separació traça/flow/plan/state machine és coherent i s'entén

## dependencies

- `feat-055` — Action Log (per registre d'esdeveniments que composen la traça)
- ReactFlow — per la projecció visual (no és una dependència de codi, sinó de visualització)

## exploration_required

**`true`** — reason: ≥2 technical unknowns (com fer que traça no afecti performance? com estructurar la separació traça/flow/plan sense sobreenginyeria?)

### Exploration Notes (when required)

**Technical unknowns:**
1. Com generar traça sense afectar performance de l'agent? — hipòtesi: async, només esdeveniments significatius, no cada crida
2. Com estructurar la separació traça/flow/plan sense sobreenginyeria? — hipòtesi: cada element té responsabilitat clara i interface petit; no cal que Flow conegui Plan internament

**Dependency graph:**
```
Kernel ──generates──> Trace Contract ──projects to──> ReactFlow Dashboard
                       │
                       └──→ Plan (what was intended)
                       └──→ State Machine (what was possible)
```

## entry_checklist

Before passing to triage, verify ALL:

- [x] `problem` is clear and non-circular
- [x] `intent` describes outcome, not solution
- [x] `scope_in` and `scope_out` are explicit and not empty
- [x] `capabilities` are testable (observable outcomes)
- [x] `approach` references existing patterns/artifacts where possible (Home Assistant study completat)
- [x] Risks have severity and mitigation
- [x] `exploration_required` is set with reason if true
- [x] All dependencies reference existing artifacts
- [x] Entry checklist is complete (ready for triage)

---

## triage_notes

Inspiració externa: Estudiar la implementació de traces d'automatitzacions de Home Assistant com a referència externa per extreure patrons útils de UX, navegació de flux, lectura temporal de passos i relació entre runtime i visualització. No copiar el producte ni el contracte intern de Home Assistant: només observar com resol traces, branques, debug operatiu i confiança visual per adaptar-ne idees al model propi d'AgenticOS.

---

## next_triage_decision

**Proposta de feature(s) candidates:**

- `feat-068` — Execution Trace Contract MVP: Defineix schema de traça, endpoint API GET /api/v1/traces/{trace_id}, i projecció ReactFlow bàsica. Dependency: feat-055 (Action Log).

**No crear feature record encara** — esperar següent triage batch on es farà DECOMPOSE i es crearà el feature record si esduit adoption.

---

## batch_handoff

| Date | Batch | Decision | Feature Record |
|------|-------|----------|----------------|
| 2026-04-12 | triage_2026-04-12 | `Deferred` (entry_checklist incomplet) | - |
| 2026-04-12 | triage_2026-04-12_addendum | `Adopted` | `00_project_documentation/SDD/artifacts/features_for_specs/feat-068-execution-trace-contract-mvp.json` |
