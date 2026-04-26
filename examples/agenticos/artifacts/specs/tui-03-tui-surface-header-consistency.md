# Spec: tui-03 TUI Surface Header Consistency

## Overview

| Field | Value |
|-------|-------|
| **ID** | tui-03 |
| **Type** | bugfix |
| **Status** | SPEC |
| **Created** | 2026-04-12 |

## Problem Statement

The TUI client sends surface headers (`X-AgenticOS-Surface`, `X-AgenticOS-TUI-Secret`) on POST/PUT requests but NOT on GET requests. This causes `DetectSurface` on the server to return `SurfaceUnknown`, leading to rejected or degraded API responses.

## Solution

Add a `setCommonHeaders()` helper method that both `doGet`, `doPost`, and `doPut` call. This ensures all TUI HTTP requests carry the correct surface identification headers.

## Requirements

### REQ-01: doGet must send surface header
- When `doGet` is called, the request MUST include header `X-AgenticOS-Surface: tui`
- This applies regardless of whether `TUISecret` is set

### REQ-02: doGet must send TUI secret when available
- When `AGENTICOS_TUI_SECRET` env var is set, `doGet` request MUST include header `X-AgenticOS-TUI-Secret: <value>`
- When env var is empty, `X-AgenticOS-TUI-Secret` header MUST NOT be sent

### REQ-03: doPost and doPut behavior unchanged
- `doPost` and `doPut` continue to send both headers as they currently do
- No changes to their request construction logic

### REQ-04: Authorization header unaffected
- `Authorization: Bearer <secret>` header continues to be set when `AGENTICOS_API_SECRET` is set
- This is orthogonal to surface headers

## Implementation

### New Method: setCommonHeaders

```go
func (c *Client) setCommonHeaders(req *http.Request) {
    req.Header.Set("X-AgenticOS-Surface", "tui")
    if c.TUISecret != "" {
        req.Header.Set("X-AgenticOS-TUI-Secret", c.TUISecret)
    }
}
```

### doGet Changes

Add call to `c.setCommonHeaders(req)` after the Authorization header check, before `c.Client.Do(req)`.

```go
func (c *Client) doGet(path string, result interface{}) error {
    // ... existing code ...
    if c.Secret != "" {
        req.Header.Set("Authorization", "Bearer "+c.Secret)
    }
    c.setCommonHeaders(req) // ADD THIS LINE
    // ... rest of method ...
}
```

## Test Cases

| ID | Scenario | Expected |
|----|----------|----------|
| TC-01 | doGet called with TUISecret set | Request has `X-AgenticOS-Surface: tui` AND `X-AgenticOS-TUI-Secret: <value>` |
| TC-02 | doGet called without TUISecret | Request has `X-AgenticOS-Surface: tui` only, no TUI-Secret header |
| TC-03 | doGet called with API secret | Request has both Authorization and surface headers |
| TC-04 | doPost behavior | Unchanged — already sends both headers |
| TC-05 | doPut behavior | Unchanged — already sends both headers |

## Files

| File | Change |
|------|--------|
| `cmd/dashboard/internal/tui/client.go` | Add `setCommonHeaders()`, call from `doGet` |

## Verification

Run:
```
go test ./cmd/dashboard/internal/tui -count=1
go test ./internal/api/... -count=1
```

All tests must pass.