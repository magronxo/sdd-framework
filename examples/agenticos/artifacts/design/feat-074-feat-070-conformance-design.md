# Design: feat-074 — feat-070 Conformance (Errata + Deterministic Tests)

## Objective

Close drift detected in `feat-070` spec and make its SDT scenarios verifiable with deterministic tests. This is a **conformance-only** change: no modifications to production code, mode.go semantics, or feat-070 artifacts.

## Conformance Issues in feat-070

### Issue 1: Spec line 114 — Incorrect Expected Outcome

**Location**: `feat-070-chat-ticket-promotion-contract.md`, SDT Scenario "absent requested_mode defaults to auto (always)"

```
- GIVEN mode IT_OP i backpressure normal
- WHEN POST /api/v1/llm/chat amb {"content": "hello"} (sense requested_mode)
- THEN HTTP 200 (auto intenta interactive, reeixir en IT_OP)
```

**Problem**: This SDT contradicts the Surface Matrix defined in the same spec:

| Mode | llm_chat (Network) | ticket_create (Write) |
|------|---------------------|----------------------|
| IT_OP | DENIED | ALLOWED |

IT_OP deniega `llm_chat` (Network surface). Per `auto` mode logic (feat-070 design línia 21-22): "Si hi ha condicio que impedeix resposta inmediata (mode denega, overlay actiu, backpressure rejecting), MUST fer fallback a creacio de ticket".

**Correct Expected Outcome**: `HTTP 202 Accepted` (fallback to ticket, not HTTP 200)

**Note**: This is an **errata in the spec document**, not a runtime bug. The runtime behavior (handlers_dashboard.go línia 532: `w.WriteHeader(http.StatusAccepted)`) is correct. The spec line 114 is simply wrong.

### Issue 2: Tests Accept E_PATH_TRAVERSAL as Valid Outcome

**Location**: `handlers_llm_chat_test.go`, tests:
- `TestLLMChat_WithTicketedMode_Returns201Or400` (line 122)
- `TestLLMChat_WithAutoMode_ITOP_Returns202Or400` (line 151)
- `TestLLMChat_RequestedModeAbsent_DefaultsToAuto` (line 178)

**Problem**: These tests contain:
```go
if rr.Code == http.StatusBadRequest {
    var resp map[string]string
    json.Unmarshal(rr.Body.Bytes(), &resp)
    if resp["error"] == "E_PATH_TRAVERSAL" || resp["error"] == "E_WRITE_FAILED" {
        t.Logf("ticket creation blocked by path validation in test env (expected in CI/temp dir)")
        return  // TEST PASSES but didn't verify the contract!
    }
}
```

**Issue**: `E_PATH_TRAVERSAL` is returned when `AGENTICOS_DATA_DIR` is not set and `./agenticos_data` doesn't exist. This is a **test environment problem**, not a valid contract outcome. The tests "pass" but don't actually verify the SDT contract.

**Fix**: Set `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())` before ticket creation flows. Remove E_PATH_TRAVERSAL bypass patterns.

### Issue 3: Missing Test — Backpressure Rejecting Returns 429

**Location**: `handlers_llm_chat_test.go`

**Problem**: Spec SDT Scenario "backpressure rejecting returns 429" has no corresponding test:
```
- GIVEN backpressure_state rejecting, mode IT_OP
- WHEN POST /api/v1/llm/chat amb {"content": "hello", "requested_mode": "ticketed"}
- THEN HTTP 429 amb {"error": "E_BACKPRESSURE_REJECTING"} i header Retry-After: 30
```

**Fix**: Add `TestLLMChat_BackpressureRejecting_Returns429` that:
1. Creates a `BackpressureProvider` stub returning `BackpressureRejecting`
2. Injects it via `SetBackpressureProvider()`
3. Asserts: status 429, error `E_BACKPRESSURE_REJECTING`, header `Retry-After: 30`

## Implementation Approach (Tests Only)

### Files Modified

| File | Change |
|------|--------|
| `02_implementation/internal/api/handlers_llm_chat_test.go` | Setup AGENTICOS_DATA_DIR, remove E_PATH_TRAVERSAL bypass, add backpressure 429 test |

### No Production Code Changes

- `mode.go` — unchanged
- `handlers_dashboard.go` — unchanged (behavior is correct)
- `backpressure_guard.go` — unchanged
- Error contracts — unchanged

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `handlers_llm_chat_test.go` | Modify | Deterministic test setup + backpressure test |

## Testing Strategy

| Test | Setup | Expected |
|------|-------|----------|
| `TestLLMChat_WithTicketedMode_Returns201Or400` | `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`, mode IT_OP | 201 Created |
| `TestLLMChat_WithAutoMode_ITOP_Returns202Or400` | `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`, mode IT_OP | 202 Accepted |
| `TestLLMChat_RequestedModeAbsent_DefaultsToAuto` | `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())`, mode IT_OP | 202 Accepted |
| `TestLLMChat_BackpressureRejecting_Returns429` | Injected `BackpressureProvider` returning `BackpressureRejecting`, mode IT_OP | 429 + Retry-After |

## Dependencies

- feat-070 (base contract)
- feat-049 (Security Modes Enforcement)
- feat-051 (Emergency Overlays)
- feat-052/feat-053 (Backpressure)
- feat-055 (Action Log)
