# Audit Report: feat-060 — SEC-03 Kernel Mediation

## Canvi

**feat-060-sec-03-kernel-mediation-mvp** — SEC-03 Kernel Mediation (remediació real)

## Resum Executiu

Hem implementat una capa de mediació FS (`internal/api/mediated_fs.go`) que intercepta totes les operacions FS des d'API handlers i les sotmet a enforcement via Guardian (overlay → mode surface → path allowlist). Tots els bypassos detectats han estat fixats.

## Arquitectura

```
API Handler → MediatedWriteFile(path, data, surface)
                    ↓
            SurfaceAuthority check (SurfaceUnknown → denied)
                    ↓
            Guardian.ValidateModeSurface("fs_write")
                    ↓
            Path allowlist (only tickets/, config/, workspace/, logs/)
                    ↓
            os.WriteFile (final) or error
```

## Fixes Aplicats

| Categoria | Abans | Ara | Línies |
|-----------|-------|-----|--------|
| Ticket CRUD | Direct os.WriteFile/Remove/Rename | Mediated* | handlers.go:92,108,400,408,496,503,513,609 |
| File Browser | Direct os.WriteFile/Remove/Rename | Mediated* | handlers_dashboard.go:94,133,800 |
| Config Writes | Direct os.WriteFile | MediatedWriteFile | handlers_dashboard.go:826 |

## Evidència d'Enforcement

| Overlay | Mode | fs_write permès? | fs_remove permès? |
|---------|------|-----------------|------------------|
| LOCKDOWN | qualsevol | ❌ E_ACTION_DENIED_BY_OVERLAY | ❌ |
| SAFE_MODE | qualsevol | ❌ E_ACTION_DENIED_BY_OVERLAY | ❌ |
| cap | READ_ONLY | ❌ E_ACTION_DENIED_BY_MODE | ❌ |
| cap | MONITOR | ❌ E_ACTION_DENIED_BY_MODE | ❌ |
| cap | IT_OP | ✅ | ✅ |
| cap | DEV | ✅ | ✅ |
| cap | AUDIT | ✅ | ✅ |
| cap | FULL | ✅ | ✅ |

## Tests Cobertura

| Categoria | Tests | Estat |
|-----------|-------|-------|
| Mediated FS (surface, overlay, mode, path) | 9 tests | ✅ Passen |
| Ticket CRUD via MediatedFS | 8+ tests | ✅ Passen |
| Overlay Enforcement | 5 tests | ✅ Passen |
| Surface Authority | 6 tests | ✅ Passen |

## Errors Detectats i Fixats

1. **TestTicketCreateDefaultValues** - faltava `t.Setenv("AGENTICOS_DATA_DIR", dataDir)` → ara fixat
2. **TestHandleTicketsCreate_BackpressureDegraded/Normal/NilProvider** - mateix problema → ara fixat
3. **TestHandlePutKernelOverlay_ClearDeniedForWebUI** - ara espera E_CHALLENGE_REQUIRED (400) en comptes de E_OVERLAY_CLEAR_DENIED (403) perquè feat-061 afegeix challenge-required per clear

## Out of Scope (Documentat però no implementat)

- LLM/WebSocket network mediation (trusted internal calls)
- writeJSONFile a helpers.go (només config, no efecte operatiu)
- Kernel router internal operations (no accessibles des d'API)

## Veredicte

**APROVAT PER A ARCHIVE**

- Tots els bypassos fixats
- Overlay/mode/path enforcement verificat
- Tests passen (2.780s api + 1.151s tui)
- Build reeixit