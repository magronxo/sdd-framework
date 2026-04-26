# Tasks: tui-03 TUI Surface Header Consistency

## Implementation Tasks

### TASK-01: Add setCommonHeaders helper method
**File**: `cmd/dashboard/internal/tui/client.go`
**Description**: Add a new method `setCommonHeaders(req *http.Request)` that sets `X-AgenticOS-Surface: tui` and conditionally sets `X-AgenticOS-TUI-Secret` when the env var is present.
**Verification**: Method compiles correctly

### TASK-02: Call setCommonHeaders in doGet
**File**: `cmd/dashboard/internal/tui/client.go`
**Description**: Add `c.setCommonHeaders(req)` call in `doGet` after the Authorization header check, before `c.Client.Do(req)`
**Verification**: `go build ./cmd/dashboard/internal/tui` succeeds

### TASK-03: Add unit tests for header verification
**File**: `cmd/dashboard/internal/tui/client_test.go` (create if not exists)
**Description**: Add `TestClient_DoGet_SetsSurfaceHeader` and `TestClient_DoGet_SetsTUISecretHeader` to verify headers are set correctly
**Verification**: `go test ./cmd/dashboard/internal/tui -count=1 -v` passes

### TASK-04: Run full TUI test suite
**Description**: Run `go test ./cmd/dashboard/internal/tui -count=1` to ensure no regression
**Verification**: All tests pass

### TASK-05: Run API tests
**Description**: Run `go test ./internal/api/... -count=1` to ensure no regression
**Verification**: All tests pass

## Task Checklist

- [ ] TASK-01: Add setCommonHeaders helper
- [ ] TASK-02: Call from doGet
- [ ] TASK-03: Add unit tests
- [ ] TASK-04: Run TUI tests
- [ ] TASK-05: Run API tests