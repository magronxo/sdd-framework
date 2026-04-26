# Audit Report: feat-055 — SEC-04 Action Log MVP

## Feature Summary

**State**: ARCHIVE
**Validation**: PASS
**Verification**: PASS

## What Was Built

Runtime action log for tracking security enforcement DENY events across two-tier architecture (Kernel + API processes).

### New Files

| File | Purpose |
|------|---------|
| `internal/kernel/action_log.go` | RingBuffer, KernelEventExporter, event emission functions |
| `internal/kernel/action_log_test.go` | 6 tests for RingBuffer + exporter |
| `internal/api/action_log.go` | KernelEventReader, APIActionLog, GetFusedEvents |
| `internal/api/action_log_test.go` | 9 tests for reader + fusion |

### Modified Files

| File | Change |
|------|--------|
| `internal/kernel/executor.go` | Emit events on guardian validation failures |
| `internal/api/server.go` | Add kernelEventReader, apiActionLog fields; route events endpoint |
| `internal/api/handlers_kernel.go` | handleKernelEvents handler |
| `internal/api/handlers.go` | Emit BACKPRESSURE_REJECT event on rejection |

## Architecture Decisions

1. **Two-tier export via filesystem**: Kernel exports to `{dataDir}/runtime/kernel_events.json` every 10s; API reads and fuses
2. **Atomic write**: temp+rename prevents partial reads
3. **Staleness handling**: >30s old kernel snapshot ignored (not failed)
4. **Source attribution**: `source: "kernel"|"api"` field distinguishes event origin
5. **Separate buffers**: Kernel and API maintain independent ring buffers (200 events each)

## Event Codes Implemented

| Kind | Code | Source | Trigger |
|------|------|--------|---------|
| MODE_DENY | E_ACTION_DENIED_BY_MODE | kernel | Surface not allowed in mode |
| OVERLAY_DENY | E_ACTION_DENIED_BY_OVERLAY | kernel | Lockdown/SafeMode blocks |
| TOOL_RISK_DENY | E_TOOL_CLASS_MISSING | kernel | Tool has no risk class |
| BACKPRESSURE_REJECT | E_BACKPRESSURE_REJECTING | api | Ticket create rejected |
| OTHER | E_BLOCKED_PORT, E_REQUEST_TOO_LARGE | kernel | HTTP policy violation |

## API Endpoint

```
GET /api/v1/kernel/events?limit=50

Response:
{
  "events": [...],
  "total": N,
  "limit": 50
}
```

## Out of Scope (Not Implemented)

- Persisting events across restarts
- `kernel/status.last_error` mutation
- Real-time sync (eventual consistency only)
- ALLOW event logging
- Advanced filtering

## Verification Evidence

```
go test ./internal/kernel -count=1  → PASS (15.9s)
go test ./internal/api -count=1    → PASS (4.6s)
go build ./...                     → PASS
```

## Notes

- Surface field uses existing codebase values (read_only, write, execute, network) not aspirational values (browser, os_fs, etc.) from initial design
- Tests use kernelSignals pattern for file-based IPC verification
- Executor emissions use guardian's existing validation results (no new coupling introduced)
