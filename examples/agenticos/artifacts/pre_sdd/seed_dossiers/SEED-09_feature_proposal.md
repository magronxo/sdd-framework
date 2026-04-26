# Feature Proposal: feat-070 — Chat Ticket Promotion Contract

> Status: PRE-SDD / triage adopted
> SEED: SEED-09
> Batch: triage_2026-04-12_chat_ticket_promotion

---

## Feature Summary

Afegir camp `requested_mode` (`interactive | ticketed | auto`) a `POST /api/v1/llm/chat` per distingir resposta immediata (200) vs ticket creat (201/202 + ticket_id).

---

## Minimal Implementable Cut (MVP)

Una sola feature que toca un sol handler (`handleLLMChat`) + tipus existents.

**In scope MVP:**

1. Nou camp `requested_mode` a `ChatRequest` (tipus `string`, opcional)
2. Default: `auto` quan absent
3. `interactive` → 200 ChatResponse
4. `ticketed` → 201/202 + `{ticket_id, tracking_url}`
5. `auto` → heuristica: intenta 200, si no pot (mode/overlay/backpressure) → fallback a ticket
6. Error 400 `E_INVALID_REQUESTED_MODE` si valor no permes
7. Errors existents reutilitzats (403 mode/overlay, 429 backpressure)
8. Revalidacio temps real: consulta `guardian.GetMode()` abans de retornar

**Out of scope:**

- HITL
- ACLs nous
- ReAct / agentic loop
- Nova persistencia mes enlla del contracte
- Modificacio de UI (només contracte API)

---

## API Contract

### Request

```json
POST /api/v1/llm/chat
{
  "content": "string",
  "department": "string (optional)",
  "provider": "string (optional)",
  "model": "string (optional)",
  "requested_mode": "interactive | ticketed | auto"  // optional, default: auto
}
```

### Response — 200 (interactive / auto fallback possible)

```json
{
  "id": "string",
  "sender": "agent",
  "content": "string",
  "done": true,
  "timestamp": "RFC3339"
}
```

### Response — 201/202 (ticket created)

```json
{
  "ticket_id": "string",
  "tracking_url": "/api/v1/tickets/{ticket_id}",
  "status": "created | accepted",
  "timestamp": "RFC3339"
}
```

### Errors

| Codi | Error | Condicio |
|------|-------|----------|
| 400 | `E_INVALID_REQUESTED_MODE` | valor no `interactive\|ticketed\|auto` |
| 403 | `E_ACTION_DENIED_BY_MODE` | mode denega surface |
| 403 | `E_ACTION_DENIED_BY_OVERLAY` | overlay actiu |
| 429 | `E_BACKPRESSURE_REJECTING` | backpressure rejecting |

---

## Error Codes (reutilitzats)

No nous codis d'error. Reutilitzar existents:

- `E_ACTION_DENIED_BY_MODE` (feat-049)
- `E_ACTION_DENIED_BY_OVERLAY` (feat-051)
- `E_BACKPRESSURE_REJECTING` (feat-052/053)

---

## Revalidacio en Temps Real

Quan `requested_mode` es `ticketed` o `auto` (amb fallback a ticket), just abans de crear el ticket:

1. Consultar `guardian.GetMode()`
2. Verificar surfaces permeses pel mode actual
3. Si denegat → retornar 403
4. Si permes → procedir amb creacio de ticket

Això fa que el canvi de mode durant una execucio en curs resulti en resposta 403 en lloc de crear ticket invalid.

---

## Dependencies

| Dependency | What it provides |
|------------|-----------------|
| feat-049 | SEC-01 Security Modes Enforcement (`E_ACTION_DENIED_BY_MODE`) |
| feat-051 | SEC-02 Emergency Overlays (`E_ACTION_DENIED_BY_OVERLAY`) |
| feat-052/053 | Backpressure Admission Control (`E_BACKPRESSURE_REJECTING`) |
| feat-055 | Action Log (events de chat/ticket) |
| feat-058 | TUI-01 API Baseline (tracking_url format) |

---

## Files to Modify

| File | Change |
|------|--------|
| `internal/api/types.go` | Afegir `RequestedMode string` a `ChatRequest` |
| `02_implementation/internal/api/handlers_dashboard.go` | Modificar `handleLLMChat` per avaluar `requested_mode` |
| `02_implementation/internal/api/handlers_llm_chat_test.go` | Afegir/actualitzar tests per cada camí (interactive/ticketed/auto + errors) |

---

## Tests (MVP)

1. `TestChat_WithRequestedModeInteractive_Returns200`
2. `TestChat_WithRequestedModeTicketed_Returns201Or202`
3. `TestChat_WithRequestedModeAuto_FallbackToTicket_WhenDenied`
4. `TestChat_WithInvalidRequestedMode_Returns400`
5. `TestChat_WithModeDenied_Returns403`
6. `TestChat_WithBackpressureRejecting_Returns429`
7. `TestChat_RequestedModeAbsent_DefaultsToAuto`

---

## Out of Scope (MVP)

- No cal modificar WS Chat (websocket.go) — futur expansion
- No cal persistencia nova mes enlla del ticket creat
- No cal HITL en loop
- No cal UI nova
