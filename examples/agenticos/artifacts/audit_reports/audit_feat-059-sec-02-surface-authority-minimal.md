# Audit Report: feat-059 — SEC-02 Surface Authority Minimal

## Canvi

**feat-059-sec-02-surface-authority-minimal** — SEC-02 Surface Authority MVP

## Resum Executiu

Implementat sistema de "surface authority" per distingir peticions TUI (operador local) de WebUI (remot) i aplicar regles diferencials per a canvis de mode i overlay.

## Decisions d'Arquitectura

| Decisió | Elecció | Justificació |
|---------|---------|--------------|
| Surface Detection | Header `X-AgenticOS-Surface` | Simple, explícit, determinista |
| TUI Auth | localhost IP o secret separat | Separa TUI local de remot sense complicar |
| Mode Restriction | Ordenació lineal FULL→READ_ONLY | Generalitzable, fàcil d'entendre |
| AuthZ WebUI | Només canvis restrictius | WebUI és mutable, no font de veritat |

## Fitxers Canviats

| Fitxer | Acció | Descripció |
|--------|--------|------------|
| `internal/api/surface.go` | Creado | Surface authority types, DetectSurface, mode restriction logic |
| `internal/api/handlers_kernel.go` | Modificado | Checks de surface abans de canvis de mode/overlay |
| `internal/api/action_log.go` | Modificado | AUTH_DENY event kind + helper |
| `cmd/dashboard/internal/tui/client.go` | Modificado | Envia X-AgenticOS-Surface i TUI secret |
| `internal/api/handlers_kernel_test.go` | Modificado | 13 tests nous per surface authority |

## Evidència d'Implementació

### Mode Restriction Direction
```
FULL (index 0) ──→ AUDIT (1) ──→ DEV (2) ──→ IT_OP (3) ──→ MONITOR (4) ──→ READ_ONLY (5, màxima restricció)

WebUI: pot anar cap a la dreta (més restrictiu) ✅
WebUI: NO pot anar cap a l'esquerra (menys restrictiu) ❌
TUI: pot anar en qualsevol direcció ✅
```

### Surface Detection Rules
```
TUI Surface vàlid si:
  1. Header: X-AgenticOS-Surface: tui
  2. I (IP localhost O secret vàlid)

WebUI Surface vàlid si:
  1. Header: X-AgenticOS-Surface: webui
  2. (auth middleware ja valida API_SECRET)
```

## Tests Cobertura

| Categoria | Tests | Estat |
|-----------|-------|-------|
| DetectSurface | 6 | ✅ Tots passen |
| Mode Restriction | 3 | ✅ Tots passen |
| Handler Mode | 5 | ✅ Tots passen |
| Handler Overlay | 5 | ✅ Tots passen |
| TUI Client | 3 | ✅ Tots passen |

## SDT Compliance

| Escenari | Resultat |
|----------|----------|
| WebUI pot restringir mode (IT_OP→READ_ONLY) | ✅ PASS |
| WebUI NO pot relaxar mode (IT_OP→DEV) | ✅ PASS |
| TUI pot relaxar mode (IT_OP→DEV) | ✅ PASS |
| WebUI pot activar SAFE_MODE | ✅ PASS |
| Clear overlay denegat (webui i tui) | ✅ PASS |
| Deny genera AUTH_DENY event | ✅ PASS |

## Proves d'Integració

- `go test ./internal/api/...` → **PASS** (2.569s)
- `go test ./cmd/dashboard/internal/tui/...` → **PASS** (1.040s)
- `go build ./internal/api/...` → **PASS**
- `go build ./cmd/dashboard/...` → **PASS**

## Observacions

1. **Header obligatori**: A partir d'ara, totes les peticions PUT a `/kernel/mode` i `/kernel/overlay` han d'incloure `X-AgenticOS-Surface`. Els clients existents (webui, altres) s'hauran d'actualitzar per enviar aquest header.

2. **Sticky overlay**: L'aclariment del prompt confirmava que clear overlay segueix denegat a l'API. Això és consistent amb el disseny original.

3. **TUI secret**: El secret separat `AGENTICOS_TUI_SECRET` és opcional — si TUI s'executa desde localhost, funciona sense secret.

## Veredicte

**APROVAT PER A ARCHIVE**

- Totes les tasques implementades
- Tots els tests passen
- SDT compliant
- Build reeixit
- Documentació completa
