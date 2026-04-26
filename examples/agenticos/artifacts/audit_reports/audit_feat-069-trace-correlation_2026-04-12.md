# Audit Report: feat-069 — Trace Correlation (ActionLog → Ticket)

**Date**: 2026-04-12
**Feature**: feat-069-trace-correlation
**Status**: ARCHIVED
**Validation**: PASS | **Verification**: PASS

## Correlation Rule

**Exact match only**: Un event es correla a un ticket si i nomÃ©s si:
- `event.context.ticket_id == ticket_id` (string equality, case-sensitive)
- **NO** fuzzy match, **NO** prefix match, **NO** heuristic
- Events sense `ticket_id` a context → NO incloure (no inventar)

## Schema Changes

### TraceEvent — add `correlation_exact`

```json
{
  "timestamp": "RFC3339",
  "source": "ticket_lifecycle | action_log | kernel",
  "kind": "STATUS_CHANGE | TOOL_EXECUTION | SECURITY_EVENT | HITL_APPROVAL",
  "message": "string",
  "data": {},
  "correlation_exact": true | null
}
```

### ActionEventContext — add `TicketID`

```go
type ActionEventContext struct {
  ToolName  string `json:"tool_name,omitempty"`
  Surface   string `json:"surface,omitempty"`
  Mode      string `json:"mode,omitempty"`
  Overlay   string `json:"overlay,omitempty"`
  Endpoint  string `json:"endpoint,omitempty"`
  TicketID  string `json:"ticket_id,omitempty"`  // NEW
}
```

## Implementation

| File | Change |
|------|--------|
| `02_implementation/internal/kernel/action_log.go` | Added `TicketID` to `ActionEventContext` |
| `02_implementation/internal/api/action_log.go` | Added `TicketID` to `ActionEventContext` |
| `02_implementation/internal/api/trace.go` | Added `CorrelationExact` field, `readKernelEventsForTicket()`, correlation filtering |
| `02_implementation/internal/api/trace_test.go` | Added 5 correlation tests |

## Correlation Logic

```go
func readKernelEventsForTicket(ticketID, dataDir string) ([]TraceEvent, error) {
  kernelPath := filepath.Join(dataDir, ActionLogRuntimeDir, TraceKernelEventsFile)
  // ...
  for _, event := range snapshot.Events {
    if event.Context.TicketID == ticketID && ticketID != "" {
      // Only include if ticket_id matches AND is non-empty
      trueVal := true
      correlatedEvents = append(correlatedEvents, TraceEvent{
        // ...
        CorrelationExact: &trueVal,
      })
    }
  }
  return correlatedEvents, nil
}
```

## Tests

```
go test ./internal/api/... -count=1 → ok 3.625s
go test ./internal/kernel/... -count=1 → ok 29.113s
```

### Correlation Tests

| Test | Description | Result |
|------|-------------|--------|
| `TestCorrelation_ExactMatch` | Event amb context.ticket_id == ticketID | âœ… PASS |
| `TestCorrelation_NoMatch` | Event amb context.ticket_id != ticketID → NO inclÃ²s | âœ… PASS |
| `TestCorrelation_NoTicketID` | Event amb context.ticket_id = "" → NO inclÃ²s | âœ… PASS |
| `TestCorrelation_MixedEvents` | Events mesclats (2 match, 1 no-match) | âœ… PASS |
| `TestSortAndTruncate_PreserveCorrelation` | Ordre + flags preservats post-truncament | âœ… PASS |

## MVP Limitation

**Kernel-side ticket_id injection NO estÃ  implementada.** Fins que no s'implementi (TBD), quan el kernel executa eines dins un ticket, no injecta `ticket_id` a l'`ActionEventContext`. AixÃ² significa:
- Tots els events del kernel tindran `context.ticket_id = ""`
- No hi haurÃ  correlaciÃ³ automÃ tica

**Workaround**: El projection_note documenta aquesta limitaciÃ³:
`"No ActionLog correlation found for ticket {id}. Events derived from ticket lifecycle only (kernel ticket_id injection TBD)."`

## Out of Scope

- Kernel-side ticket_id injection (TBD)
- ReactFlow projection
- Fuzzy matching
- New DB/persistence

## Verification Evidence

- **API unit tests**: PASS (5 correlation tests + all existing tests)
- **Kernel tests**: PASS (action_log compatibilitat verificada)
- **Determinism**: Sort + truncate ensures same output for same input
- **No invention**: Events without ticket_id are NOT included

## Dependencies

- `feat-068` (Execution Trace Contract MVP)
- `feat-055` (Action Log)
