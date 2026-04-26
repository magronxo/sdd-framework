# Design: feat-076 — Dashboard Null-Safe Lists

## Overview

Fix null-safety per a arrays en API responses i UI panels. El problema és que el backend retorna `null` quan un slice és nil en Go, i el frontend crida `.filter()`/`.map()` sense guarding.

## Root Cause Analysis

### Backend: Go Nil Slice → JSON null

En Go, `json.Marshal(nilSlice)` → `null`. Un slice buit `[]any{}` → `[]`.

| Valor Go | JSON |
|----------|------|
| `nil` | `null` |
| `[]any{}` | `[]` |
| `make([]any, 0)` | `[]` |

Els handlers afectats no garantien que els slices fossin no-nil abans de retornar.

### Frontend: Missing null guards

Components que fan `.map()`/`.filter()` sobre dades d'API sense verificar que siguin arrays.

## Solution Architecture

### Backend Fix

**Estrategia**: Nil slice normalization

En cada handler, abans de retornar el JSON, aplicar:

```go
if slice == nil {
    slice = []T{}
}
```

**Arxius afectats**:
- `handlers_approvals.go` — `handleApprovalsList`
- `handlers_dashboard.go` — `handleTicketsList`, `handleLogs`
- `handlers_session.go` — `handleListSessions`, `handleSessionNodesList`

**Avantatge**: Minimitza canvis, no altera el contracte HTTP, només garanteix que `null` mai no surti en JSON.

### Frontend Fix

**Estrategia**: Helper `asArray<T>()` + optional chaining defensiva

```typescript
function asArray<T>(value: unknown): T[] {
  if (Array.isArray(value)) return value as T[];
  return [];
}
```

**Arxius afectats** (6 panels):
- `ApprovalPanel.tsx` — CRÍTIC (crash reportat anteriorment)
- `SessionTreePanel.tsx`
- `SessionSelector.tsx`
- `HealthBadge.tsx`
- `ReportViewer.tsx`
- `EngramPanel.tsx`
- `FlowCanvas.tsx`

**Arxiu nou**: `src/lib/arrays.ts`

## Endpoints Affected

| Endpoint | Camp | Handler | Risk |
|----------|------|---------|------|
| GET /api/v1/approvals | approvals | handlers_approvals.go | CRÍTIC (ja ha crashat) |
| GET /api/v1/tickets | tickets | handlers_dashboard.go | MEDIUM |
| GET /api/v1/logs | logs, log_files | handlers_dashboard.go | LOW |
| GET /api/v1/sessions | sessions | handlers_session.go | MEDIUM |
| GET /api/v1/sessions/{id}/nodes | nodes | handlers_session.go | MEDIUM |

## Implementation Order

1. **Backend fix** (5 handlers) — sempre fer primer perquè és la font del problema
2. **Frontend helper** — `src/lib/arrays.ts`
3. **Frontend panels** — 6 components
4. **Tests backend** — 3 test cases nous
5. **Verify & audit**

## Risk Assessment

| Component | Risk | Mitigació |
|-----------|------|-----------|
| Backend handlers | BAIX — canvis mínims, defensius | Cada handler ja retorna error abans si falla |
| Frontend helper | BAIX — funció pura, type-safe | Test type-level |
| Frontend panels | BAIX — refactor d'accés a dades | Build + lint TypeScript |

## No Breaking Changes

- Contracte HTTP: mateixos codis de resposta
- Format resposta: mateixa estructura (només que `null` → `[]`)
- Funcionalitat existent: cap alteració
- Dependències: no s'afegeixen noves

## Alternative Approaches Considered

### 1. Wrapper tipus per a respostes

Crear una struct `ListResponse<T>` que sempre inicialitzi arrays a `[]`.

```go
type ListResponse[T any] struct {
    Items []T `json:"items"`
    Total int `json:"total"`
}
```

**Rebutjada**: Massa refactor per a un canvi defensiu puntual.

### 2. Custom JSON encoder

Interceptor que converteix nil slices a `[]` automàticament.

**Rebutjada**: massa魔法 (magic), afectaria tot el servidor.

### 3. Zod schemas al frontend

Validar respostes amb Zod per garantir tipus.

**Rebutjada**: Out of scope per MVP (user request).
