# Tasks: TUI-02 — TUI Connectivity Hardening

## Skills
| Task | Skills |
|---|---|
| GLOBAL | golang-patterns |
| T1.1 | golang-patterns |
| T2.1 | golang-patterns |
| T3.1 | golang-patterns |
| T4.1 | golang-patterns |
| T5.1 | golang-patterns |
| T6.1 | golang-patterns |

## Phase 1: Client - afegir mètodes API (RF-TUI2-01)

### T1.1: Afegir response structs i mètodes a client.go

**File**: `02_implementation/cmd/dashboard/internal/tui/client.go`

**Add structs**:
```go
type LogsResponse struct {
    Logs     []string `json:"logs"`
    LogFiles []string `json:"log_files"`
    Count    int      `json:"count"`
}

type KernelEventsResponse struct {
    Events []ActionEvent `json:"events"`
    Total  int           `json:"total"`
    Limit  int           `json:"limit"`
}

type ApprovalsResponse struct {
    Approvals []ApprovalInfo `json:"approvals"`
    Total     int            `json:"total"`
}

type ApprovalInfo struct {
    ID         string `json:"id"`
    TicketID   string `json:"ticket_id"`
    Action     string `json:"action"`
    Reason     string `json:"reason"`
    RequestedAt string `json:"requested_at"`
}

type SecurityReportResponse struct {
    GeneratedAt string          `json:"generated_at"`
    Posture     SecurityPosture `json:"posture"`
    Summary     ReportSummary  `json:"summary"`
    Highlights  []SecurityEvent `json:"highlights"`
    Events      []SecurityEvent `json:"events,omitempty"`
}

type SecurityPosture struct {
    Mode              string `json:"mode"`
    Overlay           string `json:"overlay"`
    RuntimeHealth     string `json:"runtime_health"`
    GuardianStatus    string `json:"guardian_status"`
    BackpressureState string `json:"backpressure_state"`
}

type ReportSummary struct {
    TotalEvents int            `json:"total_events"`
    ByKind      map[string]int `json:"by_kind"`
    BySeverity  map[string]int `json:"by_severity"`
}

type SecurityEvent struct {
    Timestamp string `json:"timestamp"`
    Source    string `json:"source"`
    Kind      string `json:"kind"`
    Severity  string `json:"severity"`
    Code      string `json:"code"`
    Message   string `json:"message"`
}
```

**Add methods**:
```go
func (c *Client) GetLogs(limit int) (*LogsResponse, error) { ... }
func (c *Client) GetKernelEvents(limit int) (*KernelEventsResponse, error) { ... }
func (c *Client) GetApprovals() (*ApprovalsResponse, error) { ... }
func (c *Client) GetSecurityReport(limit int) (*SecurityReportResponse, error) { ... }
```

**Constraints**:
- limit capped a 200 per a logs, 50 per a events
- GetApprovals: si status 404, retorna array buit (no error)

## Phase 2: Model - afegir ScreenStack i ScreenSecurityReport (RF-TUI2-05, RF-TUI2-07)

### T2.1: Modificar model.go

**File**: `02_implementation/cmd/dashboard/internal/tui/model.go`

**Add to const**:
```go
ScreenSecurityReport Screen = iota  // after ScreenStatus
```

**Add to Model struct**:
```go
ScreenStack    []Screen
```

**Update NewModel**:
```go
ScreenStack: []Screen{},
```

## Phase 3: Update - navegar with stack + ESC + API calls (RF-TUI2-02, RF-TUI2-03, RF-TUI2-04, RF-TUI2-05, RF-TUI2-06)

### T3.1: Substituir navigateToScreen demo per API calls

**File**: `02_implementation/cmd/dashboard/internal/tui/update.go`

**ScreenLogs** (case 2):
```go
case 2:
    m.Screen = ScreenLogs
    m.Cursor = 0
    m.Logs, m.LastError = fetchLogsFromAPI(m.Client)
```

**ScreenKillSwitch** (case 3):
- Eliminar demo data block (lines 173-184)
- Replace with: `m.PendingApprovals, m.LastError = fetchApprovalsFromAPI(m.Client)`

### T3.2: Afegir ESC key handling i stack navigation

**handleKeyMsg**:
```go
case msg.Type == tea.KeyEsc:
    if len(m.ScreenStack) > 0 {
        prev := m.ScreenStack[len(m.ScreenStack)-1]
        m.ScreenStack = m.ScreenStack[:len(m.ScreenStack)-1]
        m.Screen = prev
        m.Cursor = 0
    }
```

**navigateToScreen**: push current screen before navigating
```go
func navigateToScreen(m Model, cursor int) Model {
    // Push current screen to stack
    m.ScreenStack = append(m.ScreenStack, m.Screen)
    // ... rest unchanged
}
```

### T3.3: Modificar CanTransitionTo per step-up

```go
func CanTransitionTo(current, target string) (bool, string) {
    if target == "FULL" {
        return false, "Use step-up to request FULL mode"
    }
    if !IsModeMoreRestrictive(current, target) && current != target {
        return false, "Cannot change to less restrictive mode"
    }
    return true, ""
}
```

### T3.4: Afegir handler per step-up request

**ScreenStatus** key handler:
```go
case len(runes) > 0 && runes[0] == 'u':
    if m.KernelStatus != nil && m.KernelStatus.Mode != "FULL" {
        if err := m.Client.StepupWithChallenge(); err == nil {
            m.KernelStatus, m.Modes, m.LastError = fetchKernelStatus(m.Client)
        } else {
            m.LastError = fmt.Sprintf("Step-up failed: %v", err)
        }
    }
```

### T3.5: Afegir fetch helper functions

```go
func fetchLogsFromAPI(client *Client) ([]LogEntry, string) {
    resp, err := client.GetLogs(100)
    if err != nil {
        return nil, fmt.Sprintf("Logs API error: %v", err)
    }
    entries := make([]LogEntry, len(resp.Logs))
    for i, line := range resp.Logs {
        entries[i] = parseLogLine(line)
    }
    return entries, ""
}

func fetchApprovalsFromAPI(client *Client) ([]ApprovalRequest, string) {
    resp, err := client.GetApprovals()
    if err != nil {
        if err.Error() == "not_found" {
            return nil, "Approvals not available"
        }
        return nil, fmt.Sprintf("Approvals API error: %v", err)
    }
    requests := make([]ApprovalRequest, len(resp.Approvals))
    for i, a := range resp.Approvals {
        requests[i] = ApprovalRequest{...}
    }
    return requests, ""
}

func fetchKernelEventsFromAPI(client *Client) ([]Event, string) {
    resp, err := client.GetKernelEvents(50)
    if err != nil {
        return nil, fmt.Sprintf("Events API error: %v", err)
    }
    events := make([]Event, len(resp.Events))
    for i, e := range resp.Events {
        events[i] = Event{Type: e.Kind, Path: e.Message, Time: ...}
    }
    return events, ""
}
```

## Phase 4: View - afegir renderSecurityReport i actualitzar MainMenu (RF-TUI2-07, RF-TUI2-08)

### T4.1: Modificar view.go per 7 opcions MainMenu

**renderMainMenu**: options array to 7 items, NumOptions = 7

### T4.2: Afegir renderSecurityReport

```go
func renderSecurityReport(m Model) string {
    var sb strings.Builder
    sb.WriteString(TitleStyle.Render("🛡️ Security Report"))
    sb.WriteString("\n\n")

    if m.SecurityReport == nil {
        sb.WriteString(HelpStyle.Render("Press R to fetch..."))
    } else {
        // Posture section
        sb.WriteString(fmt.Sprintf("  Mode: %s | Overlay: %s | Health: %s\n",
            m.SecurityReport.Posture.Mode,
            m.SecurityReport.Posture.Overlay,
            m.SecurityReport.Posture.RuntimeHealth))
        sb.WriteString("\n")

        // Summary
        sb.WriteString("  Summary:\n")
        sb.WriteString(fmt.Sprintf("    Total: %d | CRITICAL: %d | WARN: %d | INFO: %d\n",
            m.SecurityReport.Summary.TotalEvents,
            m.SecurityReport.Summary.BySeverity["CRITICAL"],
            m.SecurityReport.Summary.BySeverity["WARN"],
            m.SecurityReport.Summary.BySeverity["INFO"]))
        sb.WriteString("\n")

        // Highlights
        if len(m.SecurityReport.Highlights) > 0 {
            sb.WriteString("  Highlights:\n")
            for _, h := range m.SecurityReport.Highlights[:min(10, len(m.SecurityReport.Highlights))] {
                sevColor := getSeverityColor(h.Severity)
                sb.WriteString(fmt.Sprintf("    %s [%s] %s: %s\n",
                    sevColor.Render(h.Severity),
                    h.Kind, h.Code, h.Message))
            }
        }
    }

    sb.WriteString("\n")
    sb.WriteString(HelpStyle.Render("R refresh • Q/ESC back"))
    return lipgloss.Place(m.Width, m.Height, lipgloss.Left, lipgloss.Top, sb.String())
}
```

### T4.3: Afegir getSeverityColor helper

```go
func getSeverityColor(severity string) lipgloss.Style {
    switch severity {
    case "CRITICAL": return ErrorStyle
    case "WARN": return WarningStyle
    default: return LogInfoStyle
    }
}
```

## Phase 5: Implement fetch + navigate per Security Report

### T5.1: Afegir ScreenSecurityReport a switch de view i update

**view.go View()**: add `case ScreenSecurityReport: return renderSecurityReport(m)`

**update.go navigateToScreen**: add case 5 for ScreenSecurityReport (after Engrams, before Status)

### T5.2: Afegir fetchSecurityReportFromAPI

```go
func fetchSecurityReportFromAPI(client *Client) (*SecurityReportResponse, string) {
    resp, err := client.GetSecurityReport(100)
    if err != nil {
        return nil, fmt.Sprintf("Security Report API error: %v", err)
    }
    return resp, ""
}
```

## Verification Tasks

### V-TUI2-1: go build

```bash
cd 02_implementation/cmd/dashboard && go build ./...
```

### V-TUI2-2: go test

```bash
cd 02_implementation && go test ./cmd/dashboard/... -v
```

### V-TUI2-3: go vet

```bash
cd 02_implementation && go vet ./cmd/dashboard/...
```

## Audit Tasks

### A-TUI2-1: Generate verify report
### A-TUI2-2: Generate audit report

## Dependencies

- feat-058 (TUI-01 TUI-API Baseline)
- feat-064 (SEC-02b Step-up Local Fort) - client.StepupWithChallenge
- feat-065 (SEC-05 Security Reports MVP) - GET /api/v1/security/report

## Out of Scope

- No backend nous
- No polling
- No canvis d'estil visual