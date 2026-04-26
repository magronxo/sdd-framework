# Design: tui-03 TUI Surface Header Consistency

## Context

The TUI client (`cmd/dashboard/internal/tui/client.go`) sends `X-AgenticOS-Surface: tui` and `X-AgenticOS-TUI-Secret` headers on `doPost` and `doPut` methods, but NOT on `doGet`. This causes the server's `DetectSurface` to return `SurfaceUnknown` for GET requests, which can cause handlers to reject or return degraded responses.

## Problem

`doGet` at line 48-77 only sets `Authorization` header if secret exists. It does NOT set:
- `X-AgenticOS-Surface: tui`
- `X-AgenticOS-TUI-Secret` (when env var is set)

Contrast with `doPut` (lines 99-102) and `doPost` (lines 305-308) which correctly set these headers.

## Solution

Centralize common header setting by extracting into a `setCommonHeaders(req)` helper method that both `doGet`, `doPost`, and `doPut` call. This ensures consistency across all HTTP methods.

## Changes

### cmd/dashboard/internal/tui/client.go

1. Add `setCommonHeaders(req *http.Request)` method after `NewClient()`:

```go
func (c *Client) setCommonHeaders(req *http.Request) {
    req.Header.Set("X-AgenticOS-Surface", "tui")
    if c.TUISecret != "" {
        req.Header.Set("X-AgenticOS-TUI-Secret", c.TUISecret)
    }
}
```

2. Call `c.setCommonHeaders(req)` in `doGet` after setting Authorization header (before `c.Client.Do(req)`)

3. Extract the common header setting from `doPut` and `doPost` to use the same helper (optional cleanup)

## Files Changed

| File | Change |
|------|--------|
| `cmd/dashboard/internal/tui/client.go` | Add `setCommonHeaders()`, call from `doGet` |

## Testing

1. Unit test `TestClient_DoGet_SetsSurfaceHeader` — verify doGet sets X-AgenticOS-Surface header
2. Unit test `TestClient_DoGet_SetsTUISecretHeader` — verify doGet sets X-AgenticOS-TUI-Secret when env var present
3. Existing TUI tests continue to pass

## Verification

```
go test ./cmd/dashboard/internal/tui -count=1
go test ./internal/api/... -count=1
```

## Risk Assessment

- **Risk**: Low — only adds missing headers, no logic change
- **Mitigation**: Existing tests validate no regression
- **Rollback**: `git checkout cmd/dashboard/internal/tui/client.go`