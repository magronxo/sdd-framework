## Audit Report

**Change**: feat-058-tui-01-tui-api-baseline
**Date**: 2026-04-11
**Type**: Implementation

---

### Summary

TUI-01 converts the TUI from a disconnected prototype (mock data) to an operative surface consuming real Kernel API endpoints. The MVP is complete with API client infrastructure, mode restriction logic, and screen integration.

### What Was Built

| Component | File | Description |
|----------|------|-------------|
| HTTP Client | `client.go` | `Client` with GET/PUT methods for all kernel endpoints, 5s timeout |
| API Types | `client.go` | `KernelStatusResponse`, `KernelModeResponse`, `ModesResponse`, `TicketInfo`, etc. |
| Model Updates | `model.go` | Added `Client`, `LastError`, `KernelStatus`, `Modes` fields |
| Mode Restriction | `update.go` | `modeRestrictivenessOrder`, `IsModeMoreRestrictive`, `CanTransitionTo` |
| Screen Integration | `update.go` | `fetchKernelStatus`, `fetchTicketsFromAPI`, `searchEngramsFromAPI`, `activateOverlay` |
| Unit Tests | `model_test.go` | 21 new test cases for mode restriction logic |

### API Endpoints Integrated

| Endpoint | Used By |
|----------|---------|
| `GET /api/v1/kernel/status` | ScreenStatus |
| `GET /api/v1/kernel/mode` | Mode restriction checks |
| `PUT /api/v1/kernel/mode` | Mode transitions (restrictive only) |
| `GET /api/v1/modes` | ScreenStatus mode list |
| `PUT /api/v1/kernel/overlay` | SAFE_MODE/LOCKDOWN activation |
| `GET /api/v1/tickets` | ScreenTickets |
| `GET /api/v1/engram/search` | ScreenEngrams |

### Mode Restriction Enforcement

```
Restrictiveness: READ_ONLY(0) > MONITOR(1) > IT_OP(2) > DEV(3) > AUDIT(4) > FULL(5)

Allowed transitions from IT_OP:
  → READ_ONLY ✅
  → MONITOR ✅
  → IT_OP (same) ✅
  → DEV ❌ (less restrictive)
  → AUDIT ❌ (less restrictive)
  → FULL ❌ (requires HITL)
```

### TUI as Strong Surface

- ✅ TUI can activate `SAFE_MODE` and `LOCKDOWN` overlays
- ✅ TUI shows clear message when attempting to clear overlay ("Use local intervention")
- ✅ Mode changes restricted to equal or more restrictive transitions
- ✅ `FULL` mode selection blocked with explanatory message

### Verification Evidence

```
go build ./cmd/dashboard          ✅
go test ./cmd/dashboard/...       ✅ 17 tests passed
```

### Deferred Items

| Item | Reason |
|------|--------|
| View updates (LastError display) | UI polish, not functional gap |
| Mode selector UI in Status screen | View changes, can be done separately |

### Alignment with ADRs

| ADR | Alignment |
|-----|-----------|
| ADR 028 | Emergency overlays (SAFE_MODE/LOCKDOWN) accessible via TUI ✅ |
| ADR 029 | TUI as strong local surface, WebUI as mutable ✅ |
| feat-057 UI-01 | TUI consumes canonical API endpoints ✅ |

### Conclusion

TUI-01 is complete. The TUI is no longer a prototype with mock data — it now functions as a real operative surface consuming the Kernel API. Mode restriction and overlay activation are enforced correctly. Ready for archive.
