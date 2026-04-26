# Design: feat-070 — Chat Ticket Promotion Contract (requested_mode MVP)

## Technical Approach

Extensió backward-compatible del handler `handleLLMChat` a `02_implementation/internal/api/handlers_dashboard.go`. Es modifica el handler per avaluar `requested_mode` abans de decidir si fer chat directe (200) o crear ticket (201/202). El handler actual ja fa tota la lògica LLM; només cal afegir un switch al principi i rails de revalidació.

## Architecture Decisions

### Decision: requested_mode com a camp opcional a ChatRequest

**Choice**: Afegir `RequestedMode string` a `ChatRequest` amb valors `interactive | ticketed | auto`
**Alternatives considered**: Nou endpoint `/api/v1/llm/chat/ticketed` — rebutjat per duplicar logica
**Rationale**: Un sol endpoint amb camp diferenciador es mes simple i backward-compatible

### Decision: default `auto` quan absent

**Choice**: Si `requested_mode` no es present o buit, assumir `auto`
**Alternatives considered**: Retornar 400 si absent — rebutjat perque trenca compatibilitat
**Rationale**: `auto` es el comportament existent (chat directe) pero ara amb fallback explícit a ticket

### Decision: 201 vs 202 per ticket creat

**Choice**: `ticketed` → 201 Created, `auto` fallback → 202 Accepted
**Alternatives considered**: Tots 201 o tots 202 — cap es neutre
**Rationale**: 201 = resource created (ticketed explícit), 202 = accepted for processing (auto promocio implícita)

### Decision: Revalidació en temps real abans de cada camí

**Choice**: Revalidar guardian i backpressure abans de cridar LLM (interactive/auto) i també abans de crear ticket (ticketed/auto fallback)
**Alternatives considered**: Revalidar només abans de crear ticket — rebutjat perquè l'interactive també té side-effects de xarxa
**Rationale**: Manté determinisme i coherència amb SEC-01/SEC-02 (mode/overlay) i backpressure

### Decision: Errors existents reutilitzats

**Choice**: Reutilitzar `E_ACTION_DENIED_BY_MODE`, `E_ACTION_DENIED_BY_OVERLAY`, `E_BACKPRESSURE_REJECTING`
**Alternatives considered**: Nous codis `E_MODE_FORBIDDEN_CHAT`, `E_BACKPRESSURE_CHAT` — rebutjat per duplicar语义
**Rationale**: El contracte d'errors ja existeix; simplement es reutilitza

## Data Flow

```
POST /api/v1/llm/chat {content, requested_mode}
       │
       ▼
Decode ChatRequest
       │
       ▼
requested_mode == ""? ──→ auto
       │
       ▼
requested_mode valid? ──no──→ 400 E_INVALID_REQUESTED_MODE
       │
       │yes
       ▼
requested_mode == "interactive"?
       │yes
       ▼
Check mode/overlay/backpressure ──denied──→ 403/429
       │
       │allowed
       ▼
200 ChatResponse (direct LLM call)
       │
else (ticketed | auto)
       │
       ▼
Revalidate guardian.GetMode() + backpressure
       │denied
       ▼
403/429 (revalidation failure)
       │allowed
       ▼
Create ticket via handleTicketsCreate logic
       │
       ▼
201 (ticketed) / 202 (auto) + {ticket_id, tracking_url, status, timestamp}
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `02_implementation/internal/api/types.go` | Modify | Afegir `RequestedMode string` a `ChatRequest` + `TicketPromotionResponse` |
| `02_implementation/internal/api/handlers_dashboard.go` | Modify | Afegir logica requested_mode a `handleLLMChat` |
| `02_implementation/internal/api/handlers_llm_chat_test.go` | Modify | Afegir tests per cada camí de requested_mode (sense crides LLM reals) |

## Interfaces / Contracts

### Request (modificat)

```go
type ChatRequest struct {
    Content       string `json:"content"`
    Department    string `json:"department,omitempty"`
    Provider      string `json:"provider,omitempty"`
    Model         string `json:"model,omitempty"`
    RequestedMode string `json:"requested_mode,omitempty"` // NOUVOUs: interactive | ticketed | auto
}
```

### Response — 200 (interactive / auto fallback possible)

```go
type ChatResponse struct {
    ID        string `json:"id"`
    Sender    string `json:"sender"`
    Content   string `json:"content"`
    Done      bool   `json:"done"`
    Timestamp string `json:"timestamp"`
}
```

### Response — 201/202 (ticket created)

```go
type TicketPromotionResponse struct {
    TicketID    string `json:"ticket_id"`
    TrackingURL string `json:"tracking_url"`
    Status      string `json:"status"` // "created" | "accepted"
    Timestamp   string `json:"timestamp"`
}
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | requested_mode parsing, default auto, invalid mode 400 | Table-driven tests |
| Unit | interactive path (200), ticketed path (201/202) | Mock LLM provider |
| Integration | 403 when mode denies, 429 when backpressure rejecting | Use feat-049/051/052 infra |
| Integration | Revalidation in real-time | Mock guardian state change |

## Migration / Rollout

No migration required. Backward-compatible: clients sense `requested_mode` obtenir comportament `auto` (equivalent a l'actual).

## Open Questions

- [x] 201 vs 202 distinction — resolved: ticketed=201, auto=202
- [x] Error code per invalid requested_mode — resolved: E_INVALID_REQUESTED_MODE (nou codi)
- [ ] WS Chat (websocket.go) — deferred a futur expansion
