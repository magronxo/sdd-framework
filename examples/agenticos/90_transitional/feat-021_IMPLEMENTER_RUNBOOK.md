# Implementer Runbook (Sample) — feat-021 Session-Ticket Linkage
STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

# Redirect (archived)
**STATUS:** ARCHIVED (redirect header)
**AUTHORITY:** NON-CANONICAL
**ARCHIVED_AT:** 2026-04-09

Canonical role prompt: `00_project_documentation/SDD/01_execution/prompts/implementer.md`
Canonical tasks: `00_project_documentation/SDD/artifacts/tasks/feat-021-session-ticket-linkage.md`
Archived copy (with archive header): `00_project_documentation/SDD/90_transitional/archive/feat-021_IMPLEMENTER_RUNBOOK.md`

---

This is a per-feature runbook sample kept for traceability and as an example of how to brief external executors.
Canonical role prompt: `00_project_documentation/SDD/01_execution/prompts/implementer.md`.
Canonical work definition: `00_project_documentation/SDD/artifacts/tasks/feat-021-session-ticket-linkage.md`.

---

## Role

You are the **Implementer** for `feat-021`.

Do **NOT** modify spec/design/tasks. Do **NOT** redesign behavior. Do **NOT** expand scope.

## Read Only (strict)

1) `AGENTS.md`
2) `00_project_documentation/SDD/00_core/SDD_RUNTIME.md`
3) `00_project_documentation/SDD/00_core/SDD_HANDOFF_CONTRACT.md`
4) `00_project_documentation/SDD/artifacts/features_for_specs/feat-021-session-ticket-linkage.json`
5) `00_project_documentation/SDD/artifacts/specs/feat-021-session-ticket-linkage.md`
6) `00_project_documentation/SDD/artifacts/tasks/feat-021-session-ticket-linkage.md`

STOP reading after tasks are clear.

## Preconditions

- Confirm in the feature record: `validation_result: "PASS"`. If not present: STOP.

## Execute (ordered, no skipping)

Follow tasks T1–T9 exactly as written. Use this sequencing:

### Phase A — Implementation first (T1–T4)

- Implement schema/model change (`SessionNode.ticket_id` optional).
- Add the API handler and route:
  - `POST /api/v1/sessions/{session_id}/nodes/{node_id}/ticket`
- Implement error mapping per spec:
  - 404 `E_SESSION_NOT_FOUND`
  - 404 `E_NODE_NOT_FOUND`
  - 409 `E_NODE_ALREADY_LINKED`
  - 500 `E_TICKET_CREATION_FAILED`

### Phase B — Tests/SDT (T5–T9)

Add tests for:
- success path
- already linked (409)
- session not found (404)
- node not found (404)
- rollback on failure (ticket file removed when node update fails)

## Ticket Creation Mechanism (locked decision)

- Create ticket via **direct file write to** `tickets/incoming/` (same behavior as existing `/api/v1/tickets` implementation).
- Do **NOT** introduce an internal HTTP call.

## Shared Logic / Duplication Rule (reduce risk)

If your new endpoint would duplicate the existing ticket-file creation logic:
- Perform a **micro-refactor**: extract a helper function and reuse it in both endpoints.
- Keep behavior identical (same defaults, same validation, same ticket schema).

## Rollback Rule (SDT-5)

If ticket was created but linking to node fails:
- delete the newly-created ticket file
- return error
- if delete fails: log + still return error (do not hide failure)

## Verify

Run the smallest relevant test set first, then broader if needed:
- `go test ./internal/api -run Test.*NodeTicket.*`
- `go test ./internal/session -run Test.*`
- `go test ./...` (only if needed)

## Output

Open a PR and include:
- list of completed tasks (T1–T9)
- `go test` commands executed and whether they passed
- any deviations (should be none); if blocked, explain the blocker precisely

