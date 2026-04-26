# Design: TUI-02 — TUI Connectivity Hardening

## 1. Motivació

feat-058 (TUI-01 TUI-API Baseline) va introduir la TUI amb client API. però:
- Logs screen usa `msgFSNotifyEvent` (event local de filesystem) que mai s'activa
- Event Loop screen igual — depèn de `msgFSNotifyEvent`
- Kill Switch mostra dades demo hardcodedades
- feat-064 (step-up) existeix al client però `CanTransitionTo` el denega per FULL
- feat-065 (Security Report) existeix al backend però no hi ha vista TUI
- Navegació sense stack: només 'q' per sortir, ESC no torna enrere

**Objectiu**: Fer la TUI operativa substituint dades demo i events fsnotify per crides API reals.

## 2. Decisions de Disseny

### DD-01: Client - afegir mètodes nous

Afegir a `client.go`:

```go
GetLogs(limit int) (*LogsResponse, error)         // GET /api/v1/logs
GetKernelEvents(limit int) (*KernelEventsResponse, error) // GET /api/v1/kernel/events
GetApprovals() (*ApprovalsResponse, error)        // GET /api/v1/approvals
GetSecurityReport(limit int) (*SecurityReportResponse, error) // GET /api/v1/security/report
```

### DD-02: Logs screen → API-only

- Eliminar dependència de `msgFSNotifyEvent`
- `update.go` - ScreenLogs: carregar logs via `client.GetLogs()` a l'entrar
- Render: mateix estil Matrix, ara amb dades de l'API
- Tecles: R refresh, C clear, A auto-scroll

### DD-03: Event Loop → Recent Events (GET /api/v1/kernel/events)

- Canviar `msgFSNotifyEvent` per `GetKernelEvents()` del client
- Screen 1: "Event Loop" → "Recent Events" (semàntica més precisa)
- Dades: events recents del kernel+API fusionats
- Tecles: R refresh, C clear

### DD-04: Kill Switch → API amb fallback

- Eliminar demo data hardcodedada a `update.go:navigateToScreen`
- Carregar `GetApprovals()` en entrar a ScreenKillSwitch
- Si API torna array buit → mostrar "No pending approvals" (no demo)
- Si endpoint no existeix (404) → mostrar missatge determinista "Approvals not available"

### DD-05: Navegació amb stack

Afegir a `model.go`:
```go
ScreenStack []Screen  // stack per back navigation
```

Actualitzar `update.go`:
- ESC → pop stack i tornar a Screen anterior
- ENTER a MainMenu → push current screen abans de navegar
- 'q' → només quit si stack buit, sinó pop

### DD-06: Step-up per FULL

`CanTransitionTo` (update.go:289-291) denega FULL directament. Canviar per:
- Si current mode no és ja FULL i target és FULL → verificar si `StepupWithChallenge()` falla
- En cas contrari, permetre canvi normal (per modes no-FULL)
- Modificar `renderStatus` per mostrar opció "Request FULL" quan mode != FULL

### DD-07: Security Report screen

Afegir ScreenSecurityReport:
- `GET /api/v1/security/report?limit=N`
- Render: posture summary + highlights (CRITICAL/WARN) + events
- Accessible des de MainMenu (nou ítem "🛡️ Security Report")
- Tecles: R refresh, Q/ESC back

### DD-08: MainMenu - afegir Security Report

Options actuals (6): Tickets, Event Loop, Logs, KillSwitch, Engrams, Status
Nous (7): afegir "🛡️ Security Report" abans de Status

## 3. Arxius a modificar

| Arxiu | Canvis |
|-------|--------|
| `client.go` | Afegir GetLogs, GetKernelEvents, GetApprovals, GetSecurityReport + response structs |
| `model.go` | Afegir ScreenStack, ScreenSecurityReport, ScreenPrevious, SecurityReport a Model |
| `view.go` | Afegir renderSecurityReport, actualitzar renderMainMenu (7 opcions) |
| `update.go` | Substituir demo per crides API, afegir ESC navigation, modificar CanTransitionTo, handleStepupRequest |

## 4. Out of Scope

- No crear缠 backend nou (endpoints ja existeixen)
- No implementar polling/auto-refresh
- No canviar estil visual (Matrix logs seguirà igual)
- No adquirir нов dependencies

## 5. Resultat esperat

- Totes les pantalles operatives via API (no demo, no fsnotify)
- Navegació ESC back funcional
- Step-up flow accessible des de Status
- Security Report visible