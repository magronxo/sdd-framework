# Audit Report: feat-068 — Execution Trace Contract MVP

**Date**: 2026-04-12
**Feature**: feat-068-execution-trace-contract-mvp
**Status**: ARCHIVED
**Validation**: PASS | **Verification**: PASS

## Schema

Trace Contract v1 (JSON):

```json
{
  "trace_id": "string (== ticket_id)",
  "ticket_id": "string",
  "generated_at": "RFC3339",
  "events": [
    {
      "timestamp": "RFC3339",
      "source": "ticket_lifecycle | action_log | kernel",
      "kind": "STATUS_CHANGE | TOOL_EXECUTION | SECURITY_EVENT | HITL_APPROVAL",
      "message": "string",
      "data": {}
    }
  ],
  "projection_note": "string | null"
}
```

## Endpoint

- `GET /api/v1/traces/{ticket_id}`
- Success: 200 with TraceResponse
- Error: 404 `E_TICKET_NOT_FOUND` | 500 `E_INTERNAL`

## Implementation

| File | Action |
|------|--------|
| `02_implementation/internal/api/trace.go` | Created |
| `02_implementation/internal/api/trace_test.go` | Created |
| `02_implementation/internal/api/server.go` | Modified (route registered) |

## Deterministes

- Handler és idempotent: lectura de ticket filesystem, cap side-effect
- `trace_id == ticket_id`: no nou ID, fàcil correlació
- Events ordenats DESC per timestamp, truncats a `limit` (default 50)
- Mateix input (mateix ticket file) → mateix output (ordres, truncaments)

## Limitacions (documentades, out of scope MVP)

1. **No correlació ActionLog→ticket**: El MVP no intenta llegir `kernel_events.json` per enriquiment. Retorna lifecycle-only amb `projection_note` descriptiu.
2. **ReactFlow projection**: OUT OF SCOPE MVP — contracte només
3. **No persistència primària**: El contracte és observacional; no s'introdueix DB nova

## Tests

```
go test ./internal/api/... -count=1
→ ok agenticos/internal/api 2.864s
```

Test coverage:
- `TestFindTicketFile_NotFound`
- `TestFindTicketFile_Found`
- `TestFindTicketFile_SearchesAllDirs`
- `TestExtractLifecycleEvents_Basic`
- `TestExtractLifecycleEvents_EmptyTicket`
- `TestSortEventsDesc`
- `TestTruncation`
- `TestProjectionNote_WhenNoCorrelation`
- `TestProjectionNote_WhenHasCorrelation`
- `TestTraceResponse_Structure`

## Verification Evidence

- **API unit tests**: PASS (10 tests, `ok agenticos/internal/api`)
- **Handler idempotency**: Read-only from ticket filesystem, no mutations
- **Determinism**: Sort + truncate ensures same output for same input
- **Error handling**: 404 for missing ticket, 500 for internal errors (logged)

## Out of Scope (contract-only)

- ReactFlow projection
- Real-time debug UI
- Ticket→ActionLog correlation implementation
- Persistence as primary data store

## Dependencies

- `feat-055` (Action Log): Font de `kernel_events.json` com a referència (no utilitzada en MVP per falta de correlació)