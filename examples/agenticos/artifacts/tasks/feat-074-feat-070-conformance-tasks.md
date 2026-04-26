# Tasks: feat-074 — feat-070 Conformance (Errata + Deterministic Tests)

## Skills

- GLOBAL: `golang-testing` (loaded)

## Phase 1: VALIDATION

### V1: Validate design coherence

- [ ] Design at `artifacts/design/feat-074-feat-070-conformance-design.md`
- [ ] Three conformance issues identified (spec line 114, E_PATH_TRAVERSAL bypass, missing backpressure test)
- [ ] No production code changes planned
- [ ] Dependencies on feat-070, feat-049, feat-051, feat-052/053, feat-055

### V2: Validate spec coherence

- [ ] Errata correctly identifies contradiction (spec line 114 vs Surface Matrix)
- [ ] SDT scenarios are verifiable (deterministic setup)
- [ ] Test determinism requirements stated
- [ ] Out of scope respected

## Phase 2: TASKS → IMPLEMENT

### T1: Modify handlers_llm_chat_test.go

**File**: `02_implementation/internal/api/handlers_llm_chat_test.go`

#### T1.1: Add AGENTICOS_DATA_DIR setup helper

Add a helper function or setup block that sets `AGENTICOS_DATA_DIR=t.TempDir()` for tests that create tickets.

Pattern (apply to affected tests):
```go
func TestLLMChat_WithTicketedMode_Returns201Or400(t *testing.T) {
    t.Setenv("AGENTICOS_DATA_DIR", t.TempDir()) // ADD THIS
    // ... rest of test, REMOVE E_PATH_TRAVERSAL bypass
}
```

#### T1.2: Fix TestLLMChat_WithTicketedMode_Returns201Or400

- Add `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())` at start
- Remove lines 119-126 (E_PATH_TRAVERSAL bypass)
- Change `if rr.Code != http.StatusCreated` to `if rr.Code != http.StatusCreated`
- Assert: status 201, body contains ticket_id

#### T1.3: Fix TestLLMChat_WithAutoMode_ITOP_Returns202Or400

- Add `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())` at start
- Remove lines 148-155 (E_PATH_TRAVERSAL bypass)
- Change `if rr.Code != http.StatusAccepted && rr.Code != http.StatusCreated` to `if rr.Code != http.StatusAccepted`
- Assert: status 202, body contains status=accepted

#### T1.4: Fix TestLLMChat_RequestedModeAbsent_DefaultsToAuto

- Add `t.Setenv("AGENTICOS_DATA_DIR", t.TempDir())` at start
- Remove lines 175-182 (E_PATH_TRAVERSAL bypass)
- Change `if rr.Code != http.StatusAccepted && rr.Code != http.StatusCreated` to `if rr.Code != http.StatusAccepted`
- Assert: status 202, body contains status=accepted (IT_OP falls back to ticket)

#### T1.5: Add TestLLMChat_BackpressureRejecting_Returns429

New test function:

```go
func TestLLMChat_BackpressureRejecting_Returns429(t *testing.T) {
    eb := NewEventBus()
    auth := NewAuthMiddleware("super-secret-token")
    ws := NewWebSocketHandler()
    guardian := kernel.NewGuardian(&kernel.FastPathPolicy{})
    guardian.SetMode(kernel.ModeIT_OP)
    
    stubProvider := &mockBackpressureProvider{state: BackpressureRejecting}
    guard := NewBackpressureGuard(stubProvider)
    
    s := NewServer(eb, auth, ws, nil, nil, guardian)
    s.SetBackpressureGuard(guard)
    
    body := `{"content": "Hello backpressure test", "requested_mode": "ticketed"}`
    req, _ := http.NewRequest("POST", "/api/v1/llm/chat", strings.NewReader(body))
    req.Header.Set("Authorization", "Bearer super-secret-token")
    req.Header.Set("Content-Type", "application/json")
    rr := httptest.NewRecorder()
    
    s.router.ServeHTTP(rr, req)
    
    if rr.Code != http.StatusTooManyRequests {
        t.Errorf("expected 429 for backpressure rejecting, got %d: %s", rr.Code, rr.Body.String())
    }
    
    var resp map[string]interface{}
    json.Unmarshal(rr.Body.Bytes(), &resp)
    if resp["error"] != "E_BACKPRESSURE_REJECTING" {
        t.Errorf("expected error E_BACKPRESSURE_REJECTING, got %q", resp["error"])
    }
    
    retryAfter := rr.Header().Get("Retry-After")
    if retryAfter != "30" {
        t.Errorf("expected Retry-After: 30, got %q", retryAfter)
    }
}

type mockBackpressureProvider struct {
    state BackpressureState
}

func (m *mockBackpressureProvider) GetState() BackpressureState {
    return m.state
}
```

## Phase 3: VERIFY

### V1: Run tests

**Command**:
```powershell
cd 02_implementation; $env:GOTELEMETRY='off'; $env:GOCACHE="$PWD\.gocache"; go test ./internal/api -count=1
```

**Expected**:
- All `handlers_llm_chat_test.go` tests PASS
- No `E_PATH_TRAVERSAL` errors (test environment is correct)
- `TestLLMChat_BackpressureRejecting_Returns429` PASS

**Evidence**: Capture output showing all tests pass.

## Phase 4: AUDIT

### A1: Generate audit report

**File**: `00_project_documentation/SDD/audit_reports/audit_feat-074-feat-070-conformance_2026-04-18.md`

AUDIT validates:
1. Errata correctly identifies spec line 114 vs Surface Matrix contradiction
2. No production code changes (only test modifications)
3. Test determinism achieved (no E_PATH_TRAVERSAL bypass)
4. Backpressure 429 test added and passing
5. feat-070 artifacts unchanged (referenced, not modified)
6. Out of scope respected

## Phase 5: ARCHIVE

### ARCH-1: Update feature JSON

Update `feat-074-feat-070-conformance.json`:
- `state`: `ARCHIVED`
- `validation_result`: `PASS`
- `verification_result`: `PASS`
- `audit_result`: `PASS`
- `validated_at`, `verified_at`, `archived_at`: timestamps

## Dependencies

- feat-070 (Chat Ticket Promotion Contract) — conformance target
- feat-049 (Security Modes Enforcement)
- feat-051 (Emergency Overlays)
- feat-052/feat-053 (Backpressure)
- feat-055 (Action Log)
- `golang-testing` skill

## Notes

- This is a conformance-only change: runtime behavior was already correct
- The "fix" is in the spec documentation (errata) and test determinism
- No changes to mode.go, security semantics, or error contracts
