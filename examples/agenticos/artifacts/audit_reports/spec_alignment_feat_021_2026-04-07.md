# Spec/Runtime Alignment Check — feat-021 (Session-Ticket Linkage)

**Data:** 2026-04-07  
**Tipus:** Alignment check (spec/tasks vs runtime code)  
**Feature:** feat-021  

## Resultat

**Resultat:** FAIL (not implemented)  
**Risc:** Mitjà (documentació indicava implementació completa)  

## Què diu la spec/tasks

- Spec: `00_project_documentation/SDD/artifacts/specs/feat-021-session-ticket-linkage.md`
- Tasks: `00_project_documentation/SDD/artifacts/tasks/feat-021-session-ticket-linkage.md`
- Contracte esperat:
  - `SessionNode.ticket_id` (o equivalent)
  - `POST /api/v1/sessions/{session_id}/nodes/{node_id}/ticket`

## Què hi ha al codi (observació)

S’ha revisat el router i handlers de sessions:

- `02_implementation/internal/api/server.go`
- `02_implementation/internal/api/handlers_session.go`
- `02_implementation/internal/session/types.go`
- `02_implementation/internal/session/store.go`

No hi ha evidència de:
- camp `ticket_id` a `SessionNode`
- store update per enllaçar ticket a node
- route/handler per crear ticket des d’un node

## Acció recomanada

1) Mantenir feature record en estat `IMPLEMENT` (no passar a `VERIFY/AUDIT/ARCHIVE`).
2) Reobrir tasks com a plan (fet) i executar IMPLEMENT real segons spec.
3) Un cop implementat:
   - `VERIFY` (tests + SDT)
   - `AUDIT` i report final
   - `ARCHIVE`
