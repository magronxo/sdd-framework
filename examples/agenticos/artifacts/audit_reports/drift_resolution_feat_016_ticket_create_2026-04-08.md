# Drift Resolution — feat-016 (agent cannot create tickets) via `ticket_create` tool

**Date (UTC)**: 2026-04-08

## Drift observed
Operationally, agents could not create real tickets even though `feat-016` was archived as complete.

This was a surface mismatch:
- `feat-016` defines the REST contract and spool writes (`POST /api/v1/tickets` → `tickets/incoming/`).
- The runtime lacked an explicit agent tool entrypoint to create tickets without going through the dashboard REST path.

## Resolution
Add a kernel tool: `ticket_create`.

Tool behavior (summary):
- Accepts structured input (ticket fields)
- Writes the ticket JSON to `tickets/incoming/` (spool)
- Returns `{ ticket_id, path }`

## Traceability (implementation)
Implemented and merged on `main` as a tooling patch on 2026-04-08.

Files:
- `02_implementation/internal/kernel/ticket_tools.go` (new)
- `02_implementation/internal/kernel/executor.go` (dispatch)
- `02_implementation/internal/kernel/executor_test.go` (tests)
- `02_implementation/internal/contextbuilder/tool_registry.go` (registration)

## Governance stance
- This is a code adjustment / tooling addition to make an existing ticket contract operable by agents.
- It does not change the REST behavior defined by `feat-016`.
- `feat-016` remains `ARCHIVE`; we only record this drift fix for operational determinism.

