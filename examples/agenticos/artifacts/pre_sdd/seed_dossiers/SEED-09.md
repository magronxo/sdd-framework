# SEED-09 — Chat → Ticket Promotion Contract

> Dossier v1 — PRE-SDD triage capture

---

## Dades de referència (del PKLot)

- **ID:** `SEED-09`
- **Titol:** Chat → Ticket Promotion Contract
- **Trigger:** Necessitat de distingir deterministicament "resposta immediata" vs "creacio de ticket"
- **Idea:** Definir un contracte on el chat rep un camp `requested_mode` que determina si la resposta es directa (200) o promou a ticket (201/202 + ticket_id + ubicacio seguiment)
- **Impacte potencial:** `kernel` / `workflow` / `all`
- **Risc de drift:** `baix`
- **Horizon:** `NOW`
- **Estat (PRE-SDD):** `Captured`
- **Batch ref:** (pending triage)
- **Desti probable:** `feat-XXX`

---

## problem

El sistema actual no té manera determinista de distingir entre una resposta immediata (chat interactiu) i una resposta que requereix creacio de ticket. Quan un usuari envia un missatge, no hi ha contracte clar sobre quin cami prendrà el sistema.

## intent

Unificar el contracte d'entrada del chat perquè el `requested_mode` determini el comportament de manera predictable: resposta directa (200) vs ticket creat (201/202). El sistema sempre retorna una resposta deterministicament sense ambigüitat.

## scope_in

- Camp d'entrada `requested_mode` a la request de chat (`interactive | ticketed | auto`)
- Comportament per defecte quan `requested_mode` no es proporcionat (assumir `auto`)
- Response API determinista: 200 (resposta immediata) o 201/202 (ticket creat + `{ticket_id}` + ubicacio seguiment)
- Errors deterministes: `requested_mode` invalid, denied by mode/overlay, backpressure rejecting
- Revalidacio en temps real quan el mode canvia durant l'execucio

## scope_out

- HITL complet (decisions humanes en loop)
- ACLs grans o complexos mes enlla del mode/overlay actual
- Implementacio de ReAct o agentic loop mes enlla del contracte
- Persistencia de tickets fora del contracte existent
- UI de chat mes enlla de la resposta API

## capabilities

El sistema ha de poder:

1. **Acceptar `requested_mode` a `/api/v1/llm/chat`** — El camp accepta `interactive`, `ticketed`, `auto`. Si no es proporcionat, el sistema assumeix `auto`.

2. **Retornar 200 amb resposta directa quan `requested_mode=interactive`** — La resposta arriba com un `ChatResponse` normal (codi 200) quan el sistema pot respondre sense crear ticket.

3. **Retornar 201/202 amb `ticket_id` i ubicacio quan `requested_mode=ticketed` o `requested_mode=auto` (fallback)** — Quan el sistema decideix crear un ticket, retorna `201 Created` o `202 Accepted` amb `{ticket_id, tracking_url}`.

4. **Retornar error deterministic quan `requested_mode` es invalid** — Codi `400 Bad Request` amb error `E_INVALID_REQUESTED_MODE` i els valors permesos.

5. **Retornar error deterministic quan el mode/overlay denega l'operacio** — Codi `403 Forbidden` amb error `E_ACTION_DENIED_BY_MODE` o `E_ACTION_DENIED_BY_OVERLAY`.

6. **Retornar error deterministic quan backpressure esta rejecting** — Codi `429 Too Many Requests` amb `Retry-After: 30` i error `E_BACKPRESSURE_REJECTING`.

7. **Revalidar en temps real quan el mode canvia durant execucio** — Si mentre s'executa un chat el mode del kernel canvia, el sistema revalida abans de completar la resposta (revalidacio en temps real).

8. **El `auto` mode aplica heuristica de fallback a ticket** — Quan `requested_mode=auto`, el sistema intenta resposta immediata; si el mode actual no permet `network` surface o la request conte certs senyals, promou a ticket.

## approach

Modificar el handler `handleLLMChat` (`handlers_dashboard.go`) per afegir el camp `requested_mode`. Mantenir la logica existent de chat.

El `requested_mode` es un enum string. Quan `ticketed` o `auto` (amb fallback), crear un ticket estructurat i retornar 201/202 amb el `ticket_id` seguint el mateix patro de creacio de tickets existent.

Els errors segueixen els codis existents (`E_ACTION_DENIED_BY_MODE`, `E_BACKPRESSURE_REJECTING`, etc.) — no cal nous codis.

La revalidacio en temps real es fa consultant `guardian.GetMode()` just abans de retornar la resposta.

## risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Conflicte amb contracte de chat existent | Low | Extensio backward-compatible (nou camp opcional) |
| Overlap amb feat-051 (overlay) o feat-049 (mode) | Low | Reutilitza codi existent, no es creen nous mecanismes |
| Retrocedir a chat sense mode conegut | Medium | `auto` default es conservative; sempre requereix evidencia per promote a ticket |

## success_signals

- [ ] `/api/v1/llm/chat` amb `requested_mode=interactive` retorna 200 i resposta ChatResponse
- [ ] `/api/v1/llm/chat` amb `requested_mode=ticketed` retorna 201/202 i `{ticket_id, tracking_url}`
- [ ] `/api/v1/llm/chat` amb `requested_mode=invalid` retorna 400 `E_INVALID_REQUESTED_MODE`
- [ ] `/api/v1/llm/chat` amb mode=READ_ONLY retorna 403 `E_ACTION_DENIED_BY_MODE`
- [ ] `/api/v1/llm/chat` amb backpressure rejecting retorna 429 `E_BACKPRESSURE_REJECTING`
- [ ] Canvi de mode durant execucio revalida abans de respondre
- [ ] Quan `requested_mode` absent, `auto` es el default

## dependencies

- `feat-049` — SEC-01 Security Modes Enforcement (per `E_ACTION_DENIED_BY_MODE`)
- `feat-051` — SEC-02 Emergency Overlays (per `E_ACTION_DENIED_BY_OVERLAY`)
- `feat-052/053` — Backpressure Admission Control (per `E_BACKPRESSURE_REJECTING`)
- `feat-055` — Action Log (per events de chat/ticket)
- `feat-058` — TUI-01 API Baseline (per tracking_url format)

## exploration_required

**`false`** — reason: contracte simple, extensions de handlers existents, sense unknowns tecnics complexos.

## entry_checklist

Before passing to triage, verify ALL:

- [x] `problem` is clear and non-circular
- [x] `intent` describes outcome, not solution
- [x] `scope_in` and `scope_out` are explicit and not empty
- [x] All `capabilities` are testable (observable outcomes)
- [x] `approach` references existing patterns/artifacts where possible
- [x] Risks have severity and mitigation
- [x] `exploration_required` is set with reason if true
- [x] All dependencies reference existing artifacts (feat-XXX)
- [x] Entry checklist is complete (all items checked)

---

## triage_notes

Requeriment identificat durant debat d'arquitectura de memoria (session 2026-04-12). No hi ha feature existent per aixo. Necessitat real del sistema: distingir chat interactiu vs treball estructurat en ticket.

El contracte es similar a `feat-051` (overlays) i `feat-053` (backpressure) en filosofia: errors deterministes, codis existents reutilitzats, no nous mecanismes.

---

## batch_handoff

| Date | Batch | Decision | Feature Record |
|------|-------|----------|----------------|
| 2026-04-12 | triage_2026-04-12_chat_ticket_promotion | PENDING | - |
