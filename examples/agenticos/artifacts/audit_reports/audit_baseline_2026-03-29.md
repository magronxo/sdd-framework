# Deep Audit: Baseline 2026-03-29
**Data:** 2026-03-29  
**Tipus:** Deep audit baseline  
**Abast:** Codebase complet (`02_implementation`) + coherencia amb `00_project_documentation` / `01_design`  
**Resultat Global:** ✅ PASS (despres de fixes)  
**Risc Global:** Baix  

## Resum Executiu
**Status:** ✅ COMPLETAT - 10/10 fixes aplicats i verificats (2026-03-29)  
**Tests:** ✅ TOTS PASSEN (35+ tests: engram, api, kernel, llm, dashboard)  
**Build:** ✅ `go build ./...` OK  
**go vet:** ✅ PASS  
**golangci-lint:** ⚠️ No disponible a l'entorn  
**gosec:** ⚠️ No disponible a l'entorn  

Tots els 10 findings de l'auditoria baseline han estat resolts i verificats amb tests. El projecte es consistent amb la filosofia MANIFEST i te una base solida.

---

## Findings (TOTS RESOLTS)

### ✅ CRIT-001: Router atomicitat del ticket (FIXAT)
**Severitat:** Critica | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/kernel/router.go`  
**Solucio:** Patro atomic amb fitxer temporal + `os.Rename`  
**Tests:** `TestRouter_AtomicCompleteTicket`, `TestRouter_AtomicFailTicket`  
**Impacte:** Garantia d'atomicitat al sistema de fitxers (alineat amb MANIFEST §VI).

### ✅ CRIT-002: WebSocket mutacio sota RLock (FIXAT)
**Severitat:** Critica | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/api/websocket.go`  
**Solucio:** Snapshot pattern - copiar clients sota RLock, enviar fora del lock, eliminar sota Lock  
**Impacte:** Elimina data race potencial.

### ✅ HIGH-001: WorkerPool drop silencios (FIXAT)
**Severitat:** Alta | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/kernel/workerpool.go`  
**Solucio:** `Enqueue` ara bloqueja (no drop). Error return al contracte.

### ✅ HIGH-002: WorkerPool locking inconsistent (FIXAT)
**Severitat:** Alta | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/kernel/workerpool.go`  
**Solucio:** `checkWorkersHealth`, `recoverStalledTicket` fan servir `worker.mu` per lectura/escritura.

### ✅ HIGH-003: Auth hardcoded (FIXAT)
**Severitat:** Alta | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/api/auth.go`  
**Solucio:** `crypto/subtle.ConstantTimeCompare` contra secret configurat. `api-server` llegeix `AGENTICOS_API_SECRET`.

### ✅ HIGH-004: Engram format YAML no conforme (FIXAT)
**Severitat:** Alta | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/engram/store.go`  
**Solucio:** Format migrat a `---json ... ---` amb `encoding/json`. Parser actualitzat. Tests passen.

### ✅ MED-001: IDs no segurs (FIXAT)
**Severitat:** Mitja | **Estat:** ✅ RESOLT (inclòs a HIGH-004)  
**Solucio:** `github.com/google/uuid` per generar IDs thread-safe.

### ✅ MED-002: Cerques no usen FTS5 (FIXAT)
**Severitat:** Mitja | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/engram/search.go`  
**Solucio:** `Search` i `SearchByTopicKey` ara usen `engrams_fts MATCH ?` amb fallback LIKE.

### ✅ MED-003: CheckOrigin permissiu (FIXAT)
**Severitat:** Mitja | **Estat:** ✅ RESOLT  
**Evidencia:** `internal/api/websocket.go`, `cmd/api-server/main.go`  
**Solucio:** `NewWebSocketHandler(allowedOrigins...)` amb env var `AGENTICOS_WS_ORIGINS`.

### ✅ MED-004: LLM proxy sense auth (FIXAT)
**Severitat:** Mitja | **Estat:** ✅ RESOLT  
**Evidencia:** `cmd/llm-proxy/main.go`  
**Solucio:** Auth middleware amb `crypto/subtle.ConstantTimeCompare`. Env var `AGENTICOS_LLM_SECRET`.

---

## Punts Forts (post-fixes)
- 10/10 findings resolts amb tests verificats
- 35+ tests passant en tots els paquets
- Atomicitat garantida al Router (alineat amb MANIFEST §VI)
- Engram format conforme a JSON frontmatter (ADR-005)
- Seguretat configurable per env vars (no hardcoded)
- WebSocket amb CheckOrigin configurable
- Worker Pool sense drops ni data races

## Limitacions de l'Auditoria
- No s'ha pogut executar `golangci-lint` ni `gosec` (no presents a l'entorn)
- No s'ha pogut executar `go test -race` (requereix CGO)
- Re-audit recomanat amb eines estàtiques quan l'entorn ho permeti

## Veredicte Final
✅ **Aprovat com a baseline de qualitat.** Tots els 10 findings han estat resolts. El projecte es consistent amb la filosofia MANIFEST i te una base solida per continuar amb disciplina d'auditoria continua.
