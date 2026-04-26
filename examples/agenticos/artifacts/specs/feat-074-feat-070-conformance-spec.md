# Spec: feat-074 — feat-070 Conformance (Errata + Deterministic Tests)

## Purpose

This spec documents the conformance corrections for `feat-070-chat-ticket-promotion-contract`. It does **not** modify feat-070 artifacts — it provides the correct interpretation and verifiable SDT scenarios.

## Conformance Target

**feat-070**: `00_project_documentation/SDD/artifacts/specs/feat-070-chat-ticket-promotion-contract.md`

## Errata: feat-070 Spec Line 114

### Original (INCORRECT)

```
### Scenario: absent requested_mode defaults to auto (always)

- GIVEN mode IT_OP i backpressure normal
- WHEN POST /api/v1/llm/chat amb {"content": "hello"} (sense requested_mode)
- THEN HTTP 200 (auto intenta interactive, reeixir en IT_OP)
```

### Corrected (THIS SPEC)

```
### Scenario: absent requested_mode defaults to auto (always)

- GIVEN mode IT_OP i backpressure normal
- WHEN POST /api/v1/llm/chat amb {"content": "hello"} (sense requested_mode)
- THEN HTTP 202 (auto fallback a ticket perque IT_OP denega llm_chat/Network)
```

### Rationale

The Surface Matrix in feat-070 spec clearly shows:

| Mode | llm_chat (Network) | ticket_create (Write) |
|------|---------------------|----------------------|
| IT_OP | DENIED | ALLOWED |

`auto` mode logic (feat-070 design): "Si hi ha condicio que impedeix resposta inmediata (mode denega, overlay actiu, backpressure rejecting), MUST fer fallback a creacio de ticket".

Since IT_OP deniega `llm_chat` (Network), `auto` MUST fallback to `ticket_create` (Write) → HTTP 202.

**The runtime behavior in `handlers_dashboard.go:532` (`w.WriteHeader(http.StatusAccepted)`) is correct. The spec line 114 is wrong.**

## SDT Scenarios (Verifiable)

### Scenario: absent requested_mode defaults to auto in IT_OP

- GIVEN mode IT_OP, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello"} (sense requested_mode)
- THEN HTTP 202 amb TicketPromotionResponse (status=accepted)

**Surface**: `os_fs` (MediatedWriteFile), `env_proxy` (AGENTICOS_DATA_DIR)

**Test setup**: `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`

### Scenario: auto fallback returns 202 in IT_OP

- GIVEN mode IT_OP, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "auto"}
- THEN HTTP 202 amb TicketPromotionResponse (status=accepted)

**Surface**: `os_fs` (MediatedWriteFile), `env_proxy` (AGENTICOS_DATA_DIR)

**Test setup**: `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`

### Scenario: ticketed returns 201 in IT_OP

- GIVEN mode IT_OP, backpressure normal, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "ticketed"}
- THEN HTTP 201 amb TicketPromotionResponse (ticket_id, tracking_url, status=created)

**Surface**: `os_fs` (MediatedWriteFile), `env_proxy` (AGENTICOS_DATA_DIR)

**Test setup**: `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`

### Scenario: backpressure rejecting returns 429

- GIVEN mode IT_OP, backpressure_state rejecting, no overlay
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "ticketed"}
- THEN HTTP 429 amb {"error": "E_BACKPRESSURE_REJECTING"} i header Retry-After: 30

**Surface**: `env_proxy` (backpressure state injection)

**Test setup**: Inject `BackpressureProvider` stub returning `BackpressureRejecting` via `SetBackpressureProvider()`

## Surface Matrix (from feat-070, unchanged)

| Mode | llm_chat (Network) | ticket_create (Write) | Notes |
|------|---------------------|----------------------|-------|
| READ_ONLY | DENIED | DENIED | No network, no write |
| MONITOR | DENIED | DENIED | No network, no write |
| IT_OP | DENIED | ALLOWED | No network, write allowed — auto falls back to ticket |
| DEV | ALLOWED | ALLOWED | Full execution |
| AUDIT | ALLOWED | ALLOWED | Network + Write |
| FULL | ALLOWED | ALLOWED | Everything |

## Error Contracts (from feat-070, unchanged)

| HTTP | Code | Used by |
|------|------|---------|
| 400 | E_INVALID_REQUESTED_MODE | interactive/ticketed/auto |
| 403 | E_ACTION_DENIED_BY_MODE | interactive (mode blocks Network), auto fallback |
| 403 | E_ACTION_DENIED_BY_OVERLAY | interactive, ticketed, auto fallback |
| 429 | E_BACKPRESSURE_REJECTING | interactive, ticketed, auto fallback |

## Test Determinism Requirements

Tests MUST NOT accept `E_PATH_TRAVERSAL` or `E_WRITE_FAILED` as valid contract outcomes. These errors indicate **test environment misconfiguration** (missing `AGENTICOS_DATA_DIR`), not contract behavior.

**Correct setup**:
```go
func TestXXX(t *testing.T) {
    t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())
    // ... test body
}
```

## Out of Scope

- Changes to mode.go or security semantics
- Changes to feat-070 runtime behavior (already correct)
- Modifications to feat-070 validated/archived artifacts
- New error codes or contract changes
