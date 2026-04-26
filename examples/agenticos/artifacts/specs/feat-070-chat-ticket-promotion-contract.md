# Spec: feat-070 — Chat Ticket Promotion Contract

## Purpose

Afegir el camp `requested_mode` a `POST /api/v1/llm/chat` per distingir resposta immediata (200) vs ticket creat (201/202).

---

## ADDED Requirements

### Requirement: requested_mode field

**ChatRequest MUST accept `requested_mode`** — camp opcional string a `POST /api/v1/llm/chat` en JSON body. Valors permesos: `interactive`, `ticketed`, `auto`. Quan absent o buit, el sistema assumeix `auto`.

El sistema MUST retornar `400 Bad Request` amb error `E_INVALID_REQUESTED_MODE` si el valor no es cap de `interactive`, `ticketed`, `auto`.

### Requirement: interactive mode returns 200

**ChatRequest amb `requested_mode=interactive` MUST retornar `200 OK`** amb `ChatResponse` body (id, sender, content, done, timestamp) quan el sistema pot processar el chat sense crear ticket.

El sistema MUST revalidar en temps real abans de processar: si mode o overlay denega la surface `network` per `llm_chat`, MUST retornar 403 `E_ACTION_DENIED_BY_MODE` o `E_ACTION_DENIED_BY_OVERLAY`. Si backpressure rejecting, MUST retornar 429 `E_BACKPRESSURE_REJECTING`.

### Requirement: ticketed mode returns 201

**ChatRequest amb `requested_mode=ticketed` MUST crear ticket** i retornar `201 Created` amb `TicketPromotionResponse` body (ticket_id, tracking_url, status, timestamp).

El sistema REVALIDA en temps real abans de crear el ticket: si mode o overlay denega surface necessaria (`write` per ticket_create), MUST retornar 403. Si backpressure rejecting, MUST retornar 429.

### Requirement: auto mode uses heuristic fallback

**ChatRequest amb `requested_mode=auto` MUST intentar resposta inmediata (equivalent a interactive)**. Si hi ha condicio que impedeix resposta inmediata (mode denega, overlay actiu, backpressure rejecting), MUST fer fallback a creacio de ticket com si fos `ticketed`.

El sistema Retorna `202 Accepted` quan fa auto-promotion a ticket (diferent codi que ticketed 201 per distingir).

### Requirement: backward compatibility

**Quan `requested_mode` es absent o buit**, el sistema MUST assumir `auto` (sempre, independentment de si hi ha provider).

---

## Surface Matrix

| Mode | llm_chat (Network) | ticket_create (Write) | Notes |
|------|---------------------|----------------------|-------|
| READ_ONLY | DENIED | DENIED | No network, no write |
| MONITOR | DENIED | DENIED | No network, no write |
| IT_OP | DENIED | ALLOWED | No network, write allowed — auto falls back to ticket |
| DEV | ALLOWED | ALLOWED | Full execution |
| AUDIT | ALLOWED | ALLOWED | Network + Write |
| FULL | ALLOWED | ALLOWED | Everything |

---

## SDT Scenarios

### Scenario: interactive returns 200

- GIVEN mode FULL o AUDIT, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "interactive"}
- THEN HTTP 200 amb ChatResponse (sender=agent, done=true)

### Scenario: ticketed returns 201

- GIVEN mode IT_OP, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "ticketed"}
- THEN HTTP 201 amb TicketPromotionResponse (ticket_id, tracking_url, status=created)

### Scenario: auto returns 200 when interactive allowed

- GIVEN mode FULL o AUDIT, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "auto"}
- THEN HTTP 200 (auto intenta interactive, reeixir)

### Scenario: auto fallback returns 202 (mode blocks network but allows write)

- GIVEN mode IT_OP, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "auto"}
- THEN HTTP 202 amb TicketPromotionResponse (status=accepted) perquè IT_OP denega llm_chat (Network) i el sistema fa fallback a ticket_create (Write)

### Scenario: auto returns 403 when both paths denied

- GIVEN mode READ_ONLY o MONITOR, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "auto"}
- THEN HTTP 403 (both llm_chat i ticket_create denegats)

### Scenario: invalid requested_mode returns 400

- GIVEN qualsevol mode
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "invalid_value"}
- THEN HTTP 400 amb {"error": "E_INVALID_REQUESTED_MODE", "allowed": ["interactive", "ticketed", "auto"]}

### Scenario: mode denies interactive returns 403

- GIVEN mode READ_ONLY, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "interactive"}
- THEN HTTP 403 amb {"error": "E_ACTION_DENIED_BY_MODE"} (llm_chat requires Network)

### Scenario: overlay denies returns 403

- GIVEN mode IT_OP, emergency_overlay SAFE_MODE
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "interactive"}
- THEN HTTP 403 amb {"error": "E_ACTION_DENIED_BY_OVERLAY"} (SAFE_MODE blocks Network)

### Scenario: backpressure rejecting returns 429

- GIVEN backpressure_state rejecting, mode IT_OP
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "ticketed"}
- THEN HTTP 429 amb {"error": "E_BACKPRESSURE_REJECTING"} i header Retry-After: 30

### Scenario: absent requested_mode defaults to auto (always)

- GIVEN mode IT_OP i backpressure normal
- WHEN POST /api/v1/llm/chat amb {"content": "hello"} (sense requested_mode)
- THEN HTTP 200 (auto intenta interactive, reeixir en IT_OP)

---

## Error Contracts

| HTTP | Code | Used by |
|------|------|---------|
| 400 | E_INVALID_REQUESTED_MODE | interactive/ticketed/auto |
| 403 | E_ACTION_DENIED_BY_MODE | interactive (mode blocks Network), auto fallback |
| 403 | E_ACTION_DENIED_BY_OVERLAY | interactive, ticketed, auto fallback |
| 429 | E_BACKPRESSURE_REJECTING | interactive, ticketed, auto fallback |
| 429 | E_PROVIDER_COOLDOWN | interactive (existing) |
| 429 | E_RATE_LIMITED | interactive (existing) |
| 429 | E_PROVIDER_DEGRADED | interactive (existing) |

---

## Out of Scope

- HITL
- WS Chat (websocket.go)
- ReAct / agentic loop
- Persistencia mes enlla del ticket creat
