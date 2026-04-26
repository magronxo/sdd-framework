# Spec: feat-076 — Dashboard Null-Safe Lists

## Purpose

Backend i frontend han de retornar/utilitzar arrays de forma segura. Quan un camp array és absent o null, el contracte diu `[]` i el frontend no fa crash amb `.map()`/`.filter()`.

## Problem Statement

- Backend `handlers_*.go` retornen `null` en lloc de `[]` per a camps array quan no hi ha dades
- Frontend fa `.filter()`/`.map()` directament sobre dades de l'API sense guarding contra null
- Resultat: UI crash en produir-se dades buides o errònies

## Contracte: List Responses Are Never Null

### Regla

Per a tots els endpoints REST que retornen arrays:

| Situació | HTTP | Payload |
|----------|------|---------|
| Dades existents | 200 | `{"aprovals": [...], "total": N}` |
| Cap dada | 200 | `{"aprovals": [], "total": 0}` |
| Error (sense dades) | 5xx | `{"error": "E_...", "message": "..."}` |

**Mai**: `{"aprovals": null, "total": 0}` o qualsevol camp array amb valor `null`.

### Endpoints afectats

| Endpoint | Camp array | Notes |
|----------|------------|-------|
| GET /api/v1/approvals | `approvals` | Normalitzar nil → [] |
| GET /api/v1/tickets | `tickets` | Normalitzar nil → [] |
| GET /api/v1/logs | `logs`, `log_files` | Normalitzar nil → [] |
| GET /api/v1/sessions | `sessions` | Normalitzar nil → [] |
| GET /api/v1/sessions/{id}/nodes | `nodes` | Normalitzar nil → [] |
| GET /api/v1/reports | `reports` | (si aplica) |

## Backend: Normalització de Nil Slices

### Principi

En Go, un **nil slice** es marshaleja a JSON com `null`, mentre qualsevol slice amb zero elements (`[]any{}` o `make([]any, 0)`) es marshaleja a `[]`.

**Tots els handlers** que retornen arrays han de garantir que mai no retornin un nil slice a JSON.

### Canvis requerits

#### 1. `handlers_approvals.go` — handleApprovalsList

**Abans** (possible nil):
```go
approvals, err := store.List(status, limit)
if err != nil {
    s.writeError(...)
    return
}
w.Header().Set("Content-Type", "application/json")
json.NewEncoder(w).Encode(map[string]interface{}{
    "approvals": approvals,  // pot ser nil si store.List retorna nil, nil
    "total":     len(approvals),
})
```

**Després** (sempre []):
```go
approvals, err := store.List(status, limit)
if err != nil {
    s.writeError(...)
    return
}
if approvals == nil {
    approvals = []Approval{}
}
w.Header().Set("Content-Type", "application/json")
json.NewEncoder(w).Encode(map[string]interface{}{
    "approvals": approvals,
    "total":     len(approvals),
})
```

#### 2. `handlers_dashboard.go` — handleTicketsList

**Abans**:
```go
var tickets []map[string]interface{}
for _, dirInfo := range ticketDirs {
    if entries, err := os.ReadDir(dirInfo.Path); err == nil {
        for _, entry := range entries {
            // ...
        }
    }
}
// Si cap directori existeix o tots buits, tickets és nil → null en JSON
sendOK(w, map[string]interface{}{
    "tickets":   tickets,
    "total":     len(tickets),
})
```

**Després**:
```go
var tickets []map[string]interface{}
for _, dirInfo := range ticketDirs {
    if entries, err := os.ReadDir(dirInfo.Path); err == nil {
        for _, entry := range entries {
            // ...
        }
    }
}
if tickets == nil {
    tickets = []map[string]interface{}{}
}
sendOK(w, map[string]interface{}{
    "tickets":   tickets,
    "total":     len(tickets),
    "by_status": collectTicketStats(dataDir).ByStatus,
})
```

#### 3. `handlers_dashboard.go` — handleLogs

**Abans**:
```go
var logFiles []string
// ...
var lines []string
// ...
sendOK(w, map[string]interface{}{
    "logs":      lines,       // nil → null
    "log_files": logFiles,    // nil → null
    "count":     len(lines),
})
```

**Després**:
```go
var logFiles []string
var lines []string
// ...
if logFiles == nil {
    logFiles = []string{}
}
if lines == nil {
    lines = []string{}
}
sendOK(w, map[string]interface{}{
    "logs":      lines,
    "log_files": logFiles,
    "count":     len(lines),
})
```

#### 4. `handlers_session.go` — handleListSessions

**Abans** (ja força `[]` en error, però no en èxit):
```go
sessions, err := s.sessionStore.ListSessions()
if err != nil {
    sessions = []*session.Session{}  // correcte en error
}
// PERÒ si err == nil i sessions és nil → null
sendOK(w, map[string]interface{}{
    "sessions": sessions,
    "total":    len(sessions),
})
```

**Després**:
```go
sessions, err := s.sessionStore.ListSessions()
if err != nil {
    sessions = []*session.Session{}
}
if sessions == nil {
    sessions = []*session.Session{}
}
sendOK(w, map[string]interface{}{
    "sessions": sessions,
    "total":    len(sessions),
})
```

#### 5. `handlers_session.go` — handleSessionNodesList

**Abans**:
```go
nodes, err := s.sessionStore.ListNodes(id, sess.ActiveBranchID)
if err != nil || nodes == nil {
    nodes = []*session.SessionNode{}
}
// PERÒ si err == nil i nodes nil → null
sendOK(w, map[string]interface{}{
    "nodes": nodes,
    "total": len(nodes),
})
```

**Després**:
```go
nodes, err := s.sessionStore.ListNodes(id, sess.ActiveBranchID)
if err != nil || nodes == nil {
    nodes = []*session.SessionNode{}
}
sendOK(w, map[string]interface{}{
    "nodes": nodes,
    "total": len(nodes),
})
```

## Frontend: Robustesa UI

### Principi

El frontend no ha de dependre exclusivament del backend per a la seguretat de tipus. Encara que el backend bugi, la UI no ha de fer crash.

### Helper: asArray

**Ubicació**: `02_implementation/agentic-ide/src/lib/arrays.ts` (NOU)

```typescript
export function asArray<T>(value: unknown): T[] {
  if (Array.isArray(value)) {
    return value as T[];
  }
  return [];
}
```

### Canvis a panels

#### ApprovalPanel.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/approvals/ApprovalPanel.tsx`

**Abans** (crash si `data.approvals` és null):
```typescript
const data = await response.json();
setApprovals(data.approvals);
```

**Després**:
```typescript
import { asArray } from '../../lib/arrays';

const data = await response.json();
setApprovals(asArray(data.approvals));
```

#### SessionTreePanel.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/sessions/SessionTreePanel.tsx`

Buscar: `sessions.map(`
Replegar amb `asArray` o `|| []`:
```typescript
{(asArray(sessions).map(session => (
```

#### SessionSelector.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/session-tree/SessionSelector.tsx`

Buscar: `sessions.map(`
Replegar:
```typescript
{asArray(sessions).map((session) => (
```

#### HealthBadge.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/kernel/HealthBadge.tsx`

**Abans** (crash si providers és null):
```typescript
{health.providers.filter(p => p.status === 'healthy').length}/{health.providers.length}
```

**Després**:
```typescript
{asArray(health.providers).filter(p => p.status === 'healthy').length}/{asArray(health.providers).length}
```

#### ReportViewer.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/reports/ReportViewer.tsx`

Buscar: `reports.filter(`
Replegar:
```typescript
const filteredReports = asArray(reports).filter((report) => {
```

#### EngramPanel.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/engram/EngramPanel.tsx`

Buscar: `engrams.filter(`
Replegar:
```typescript
const filteredEngrams = asArray(engrams).filter((engram) => {
```

#### FlowCanvas.tsx

**Ubicació**: `02_implementation/agentic-ide/src/features/flow/FlowCanvas.tsx`

Buscar: `tickets.filter(`
Replegar cada instància:
```typescript
const filteredTickets = asArray(tickets)
```

## Tests: Backend

### Test: GET /api/v1/approvals retorna [] mai null

**Arxiu**: `02_implementation/internal/api/handlers_approvals_test.go`

Nou test subtest dins `TestHandleApprovalsList`:

```go
t.Run("empty store returns empty array not null", func(t *testing.T) {
    tmpDir, err := os.MkdirTemp("", "approvals_empty_test")
    if err != nil {
        t.Fatal(err)
    }
    defer os.RemoveAll(tmpDir)

    // NO crear cap fitxer d'aprovació

    oldDataDir := os.Getenv("AGENTICOS_DATA_DIR")
    os.Setenv("AGENTICOS_DATA_DIR", tmpDir)
    defer func() {
        if oldDataDir != "" {
            os.Setenv("AGENTICOS_DATA_DIR", oldDataDir)
        } else {
            os.Unsetenv("AGENTICOS_DATA_DIR")
        }
    }()

    req := httptest.NewRequest(http.MethodGet, "/api/v1/approvals", nil)
    w := httptest.NewRecorder()

    server := &Server{}
    server.handleApprovalsList(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("status = %d, want %d", w.Code, http.StatusOK)
    }

    var resp map[string]interface{}
    json.Unmarshal(w.Body.Bytes(), &resp)

    approvals, ok := resp["approvals"].([]interface{})
    if !ok {
        t.Fatalf("approvals is not an array: %T", resp["approvals"])
    }
    if len(approvals) != 0 {
        t.Errorf("len(approvals) = %d, want 0", len(approvals))
    }
    total, ok := resp["total"].(float64)
    if !ok {
        t.Errorf("total is not a number: %T", resp["total"])
    }
    if int(total) != 0 {
        t.Errorf("total = %d, want 0", int(total))
    }
})
```

### Test: GET /api/v1/tickets retorna [] mai null

**Arxiu**: Nou o existent a `handlers_dashboard_test.go`

```go
t.Run("no tickets returns empty array not null", func(t *testing.T) {
    tmpDir, err := os.MkdirTemp("", "tickets_empty_test")
    if err != nil {
        t.Fatal(err)
    }
    defer os.RemoveAll(tmpDir)

    oldDataDir := os.Getenv("AGENTICOS_DATA_DIR")
    os.Setenv("AGENTICOS_DATA_DIR", tmpDir)
    defer func() {
        if oldDataDir != "" {
            os.Setenv("AGENTICOS_DATA_DIR", oldDataDir)
        } else {
            os.Unsetenv("AGENTICOS_DATA_DIR")
        }
    }()

    req := httptest.NewRequest(http.MethodGet, "/api/v1/tickets", nil)
    w := httptest.NewRecorder()

    server := &Server{}
    server.handleTicketsList(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("status = %d, want %d", w.Code, http.StatusOK)
    }

    var resp map[string]interface{}
    json.Unmarshal(w.Body.Bytes(), &resp)

    tickets, ok := resp["tickets"].([]interface{})
    if !ok {
        t.Fatalf("tickets is not an array: %T (got %v)", resp["tickets"], resp["tickets"])
    }
    if len(tickets) != 0 {
        t.Errorf("len(tickets) = %d, want 0", len(tickets))
    }
})
```

### Test: GET /api/v1/logs retorna [] per a logs i log_files

**Arxiu**: `handlers_dashboard_test.go`

```go
t.Run("no logs dir returns empty arrays not null", func(t *testing.T) {
    tmpDir, err := os.MkdirTemp("", "logs_empty_test")
    if err != nil {
        t.Fatal(err)
    }
    defer os.RemoveAll(tmpDir)

    oldDataDir := os.Getenv("AGENTICOS_DATA_DIR")
    os.Setenv("AGENTICOS_DATA_DIR", tmpDir)
    defer func() {
        if oldDataDir != "" {
            os.Setenv("AGENTICOS_DATA_DIR", oldDataDir)
        } else {
            os.Unsetenv("AGENTICOS_DATA_DIR")
        }
    }()

    req := httptest.NewRequest(http.MethodGet, "/api/v1/logs", nil)
    w := httptest.NewRecorder()

    server := &Server{}
    server.handleLogs(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("status = %d, want %d", w.Code, http.StatusOK)
    }

    var resp map[string]interface{}
    json.Unmarshal(w.Body.Bytes(), &resp)

    logs, ok := resp["logs"].([]interface{})
    if !ok {
        t.Fatalf("logs is not an array: %T", resp["logs"])
    }
    logFiles, ok := resp["log_files"].([]interface{})
    if !ok {
        t.Fatalf("log_files is not an array: %T", resp["log_files"])
    }
})
```

## Tests: Frontend

### NOT EXECUTED

El frontend (`agentic-ide`) no disposa de framework de test (no Vitest, no Jest). Els canvis de frontend es validen manualment o mitjançant linting tipus TypeScript.

**Type-level test**: El helper `asArray<T>` és type-safe. Es valida que:
- `asArray(null)` → `[]`
- `asArray(undefined)` → `[]`
- `asArray([1,2,3])` → `[1,2,3]`
- `asArray("string")` → `[]` (comportament defensiu)

## Verify

### Backend

```bash
go test ./internal/api -count=1 -run "TestHandleApprovalsList|TestHandleTicketsList|TestHandleLogs"
```

### Frontend

```bash
cd 02_implementation/agentic-ide && npm run build
```

## Out of Scope

- Refactor d'estat global UI
- Canvis a l'arquitectura de persistència (ApprovalStore, TicketStore)
- Nous endpoints
- Modificació de contractes HTTP existents (codis d'error, etc.)
- Frontend test execution (no hi ha harness)

## Dependencies

- `feat-067` (Approvals Backend MVP) — base per al handler d'approvals
- `feat-058` (TUI API Baseline) — base per als handlers de dashboard

## Surface Matrix

| Operació | Surface | Notes |
|----------|---------|-------|
| Read approvals | os_fs | Només lectura de fitxers JSON |
| Read tickets | os_fs | Només lectura |
| Read logs | os_fs | Només lectura |
| Read sessions | os_fs | Només lectura |

No nous surfaces. Canvis defensius en handlers existents.
