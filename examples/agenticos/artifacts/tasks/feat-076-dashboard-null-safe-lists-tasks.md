# Tasks: feat-076 — Dashboard Null-Safe Lists

## PHASE 1: Backend Fixes

### Task 1.1: Fix handleApprovalsList — nil slice normalization

**File**: `02_implementation/internal/api/handlers_approvals.go`
**Lines**: ~22-32
**Change**: Afegir `if approvals == nil { approvals = []Approval{} }` abans de l'Encode

**Verification**: `go test ./internal/api -count=1 -run TestHandleApprovalsList`

### Task 1.2: Fix handleTicketsList — nil slice normalization

**File**: `02_implementation/internal/api/handlers_dashboard.go`
**Lines**: ~826-852
**Change**: Afegir `if tickets == nil { tickets = []map[string]interface{}{} }` abans de sendOK

**Verification**: Nou test `TestHandleTicketsList/empty_returns_empty_array`

### Task 1.3: Fix handleLogs — nil slice normalization per a logs i log_files

**File**: `02_implementation/internal/api/handlers_dashboard.go`
**Lines**: ~878-917
**Change**: Afegir nil checks per `logFiles` i `lines` abans de sendOK

**Verification**: Nou test `TestHandleLogs/no_logs_dir_returns_empty_arrays`

### Task 1.4: Fix handleListSessions — nil slice normalization

**File**: `02_implementation/internal/api/handlers_session.go`
**Lines**: ~32-40
**Change**: Afegir `if sessions == nil { sessions = []*session.Session{} }` abans de sendOK

**Verification**: Test existent `TestHandleListSessions` (si existeix)

### Task 1.5: Fix handleSessionNodesList — nil slice normalization

**File**: `02_implementation/internal/api/handlers_session.go`
**Lines**: ~256-264
**Change**: Simplificar a només `nodes = []*session.SessionNode{}` quan nil o error

**Verification**: Test existent `TestHandleSessionNodesList` (si existeix)

## PHASE 2: Frontend Helper

### Task 2.1: Create asArray helper

**File**: `02_implementation/agentic-ide/src/lib/arrays.ts` (NOU)
**Content**: Funció `asArray<T>(value: unknown): T[]`

**Verification**: `cd 02_implementation/agentic-ide && npm run build`

## PHASE 3: Frontend Panels

### Task 3.1: Fix ApprovalPanel.tsx

**File**: `02_implementation/agentic-ide/src/features/approvals/ApprovalPanel.tsx`
**Lines**: ~36
**Change**: `setApprovals(asArray(data.approvals))`

### Task 3.2: Fix SessionTreePanel.tsx

**File**: `02_implementation/agentic-ide/src/features/sessions/SessionTreePanel.tsx`
**Line**: ~135
**Change**: `asArray(sessions).map(...)`

### Task 3.3: Fix SessionSelector.tsx

**File**: `02_implementation/agentic-ide/src/features/session-tree/SessionSelector.tsx`
**Line**: ~32
**Change**: `asArray(sessions).map(...)`

### Task 3.4: Fix HealthBadge.tsx

**File**: `02_implementation/agentic-ide/src/features/kernel/HealthBadge.tsx`
**Lines**: ~55-57, ~123, ~145
**Change**: `asArray(health.providers).filter(...)` i `.map(...)`

### Task 3.5: Fix ReportViewer.tsx

**File**: `02_implementation/agentic-ide/src/features/reports/ReportViewer.tsx`
**Line**: ~44
**Change**: `asArray(reports).filter(...)`

### Task 3.6: Fix EngramPanel.tsx

**File**: `02_implementation/agentic-ide/src/features/engram/EngramPanel.tsx`
**Lines**: ~59, ~145, ~195, ~218, ~253
**Change**: `asArray(engrams).filter(...)`, `asArray(engram.topic_keys).map(...)`

### Task 3.7: Fix FlowCanvas.tsx

**File**: `02_implementation/agentic-ide/src/features/flow/FlowCanvas.tsx`
**Lines**: ~30-34
**Change**: `asArray(tickets).filter(...)` per a cada instància

## PHASE 4: Tests

### Task 4.1: Add backend test — empty approvals

**File**: `02_implementation/internal/api/handlers_approvals_test.go`
**Subtest**: `TestHandleApprovalsList/empty_store_returns_empty_array_not_null`
**Verification**: `go test ./internal/api -count=1 -run TestHandleApprovalsList/empty`

### Task 4.2: Add backend test — empty tickets

**File**: `02_implementation/internal/api/handlers_dashboard_test.go` (o crear si no existeix)
**Subtest**: Nou test per a handleTicketsList buit
**Verification**: `go test ./internal/api -count=1 -run TestHandleTicketsList`

### Task 4.3: Add backend test — empty logs

**File**: `02_implementation/internal/api/handlers_dashboard_test.go`
**Subtest**: Nou test per a handleLogs amb directori buit
**Verification**: `go test ./internal/api -count=1 -run TestHandleLogs`

## PHASE 5: Verify

### Task 5.1: Run backend tests

```bash
go test ./internal/api -count=1
```

### Task 5.2: Build frontend

```bash
cd 02_implementation/agentic-ide && npm run build
```

## PHASE 6: Audit + Archive

### Task 6.1: Generate verify report

### Task 6.2: Generate audit report

### Task 6.3: Update feature record — status: ARCHIVED
