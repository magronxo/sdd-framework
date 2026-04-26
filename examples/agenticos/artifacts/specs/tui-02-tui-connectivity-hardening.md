# Spec: TUI-02 — TUI Connectivity Hardening

## 1. Overview

**Feature ID:** TUI-02
**Type:** SYSTEM_SPEC (TUI enhancement)
**State:** SPEC
**Goal:** Substituir dades demo i msgFSNotifyEvent per crides API reals a tots els screens pendents.

## 2. Requisits Funcionals

### RF-TUI2-01: Client - mètodes nous

```go
// GET /api/v1/logs
GetLogs(limit int) (*LogsResponse, error)
type LogsResponse struct {
    Logs      []string `json:"logs"`        // línies de log
    LogFiles  []string `json:"log_files"`
    Count     int      `json:"count"`
}

// GET /api/v1/kernel/events
GetKernelEvents(limit int) (*KernelEventsResponse, error)
type KernelEventsResponse struct {
    Events []ActionEvent `json:"events"`
    Total  int           `json:"total"`
    Limit  int           `json:"limit"`
}

// GET /api/v1/approvals
GetApprovals() (*ApprovalsResponse, error)
type ApprovalsResponse struct {
    Approvals []ApprovalInfo `json:"approvals"`
    Total     int            `json:"total"`
}
type ApprovalInfo struct {
    ID        string `json:"id"`
    TicketID  string `json:"ticket_id"`
    Action    string `json:"action"`
    Reason    string `json:"reason"`
    RequestedAt string `json:"requested_at"`
}

// GET /api/v1/security/report
GetSecurityReport(limit int) (*SecurityReportResponse, error)
type SecurityReportResponse struct {
    GeneratedAt   string            `json:"generated_at"`
    Posture       SecurityPosture  `json:"posture"`
    Summary       ReportSummary    `json:"summary"`
    Highlights    []SecurityEvent  `json:"highlights"`
    Events        []SecurityEvent  `json:"events,omitempty"`
}
```

### RF-TUI2-02: Logs screen API-only

- Entrar a ScreenLogs → cridar `GetLogs(100)`
- Render: Matrix style (mateix que ara però dades reals)
- Tecles: R = refresh (crida GetLogs), C = clear (neteja local), A = auto-scroll toggle
- Errors: mostrar `m.LastError` si la crida falla

### RF-TUI2-03: Event Loop → Recent Events (API)

- Canviar nom: "⚡ Event Loop" → "⚡ Recent Events"
- Entrar a ScreenEventLoop → cridar `GetKernelEvents(50)`
- Render: llistar events amb timestamp i kind
- Tecles: R = refresh, C = clear

### RF-TUI2-04: Kill Switch API amb fallback

- Eliminar demo data (`PendingApprovals = []ApprovalRequest{{...}}`) de navigateToScreen
- Entrar a ScreenKillSwitch → cridar `GetApprovals()`
- Si `err == "not_found"`: mostrar "Approvals endpoint not available" (determinista)
- Si array buit: mostrar "No pending approvals" (no demo)
- Si dades: mostrar llista amb A/R per approve/reject

### RF-TUI2-05: Navegació amb stack + ESC

Afegir a Model:
```go
ScreenStack []Screen  // stack per back navigation
```

Regles:
- ENTER a MainMenu → `push CurrentScreen, navigate`
- ESC → `pop Stack, restore previous screen`
- 'q' → `if len(stack) > 0 { pop } else { quit }`
- Stack buit a Welcome → 'q' quit

### RF-TUI2-06: Step-up per FULL des de Status

Canviar `CanTransitionTo` (update.go):
```go
func CanTransitionTo(current, target string) (bool, string) {
    if target == "FULL" {
        // FULL requereix step-up flow; denegar directament
        return false, "Use step-up to request FULL mode"
    }
    if !IsModeMoreRestrictive(current, target) && current != target {
        return false, "Cannot change to less restrictive mode"
    }
    return true, ""
}
```

A renderStatus: afegir opció "Press [U] to request FULL mode" quan mode != FULL.

### RF-TUI2-07: Security Report screen

Afegir ScreenSecurityReport:
- GET /api/v1/security/report?limit=100
- Render: posture (mode, overlay, health) + summary (by severity) + highlights (max 20)
- Tecles: R refresh, Q/ESC back

### RF-TUI2-08: MainMenu - afegir Security Report

7 opcions en lloc de 6:
1. 🎫 Tickets Router
2. ⚡ Recent Events
3. 📜 System Logs
4. 🛑 Kill Switch (HITL)
5. 🧠 Engrams Explorer
6. 🛡️ Security Report  ← NOU
7. 📊 System Status

NumOptions = 7

## 3. Out of Scope

- No backend nous (endpoints ja existeixen)
- No polling/auto-refresh
- No canvis d'estil visual
- No noves dependencies

## 4. Resultat esperat

- validation_result: PASS
- verification_result: PASS
- audit_result: PASS
- go test + go build passen