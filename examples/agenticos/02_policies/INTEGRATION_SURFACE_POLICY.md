# Policy: Integration Surface Gates (SPEC / VERIFY)

> **Estat:** Actiu  
> **Data:** 2026-04-10  
> **Abast:** Qualsevol feature que exposi comportament via browser/FS/network/handlers

## Purpose

Evitar “PASS falsos” quan:

- `curl` funciona però el navegador falla (CORS + preflight).
- La lògica core és correcta però el handler no la crida (wiring).
- Windows/ACLs o paths (espais/cometes) trenquen el flux real.

## Principle

**Surface-aware verification.**  
El veredicte només pot ser `PASS` si existeix evidència per la superfície afectada.

## 1) Surface classification (SPEC)

Quan escrius una SPEC, declara quines surfaces aplica (boolean):

- `browser`: UI web / Vite / cross-origin / cookies / storage
- `os_fs`: filesystem local, paths Windows, permisos, `ReadDir`, `os.Stat`
- `wiring`: handler → service/core, feature flags, routing, middleware order
- `network`: outbound HTTP, retries, timeouts, provider health
- `env_proxy`: proxies, secrets, ports, local dev constraints

**Regla:** si no declares cap surface, s’assumeix `wiring=true` com a mínim (tota feature té alguna forma d’integració).

## 2) Required evidence (VERIFY)

### 2.1 `browser`

- Evidència mínima: captura/nota del Network tab (o equivalent) + resultat real.
- Si hi ha `Authorization` header: cal demostrar que el server accepta `OPTIONS` preflight.
  - Exemple (curl):
    - `curl -i -X OPTIONS http://localhost:8080/api/v1/<route> -H "Origin: http://localhost:5173" -H "Access-Control-Request-Method: GET" -H "Access-Control-Request-Headers: authorization,content-type"`

**Regla:** `curl GET/POST` no valida CORS.

### 2.2 `os_fs`

- Evidència mínima: tests (si possible) + una prova manual amb path real.
- Cases a cobrir si aplica:
  - path amb espais
  - path amb cometes (`"K:\Path"` / `'K:\Path'`) → sanitize/trim
  - directori existent però no accessible (ACL)

### 2.3 `wiring`

Evidència mínima: un test (o evidència equivalent) que demostri que el punt d’entrada real crida la lògica core.

Exemples:

- handler `handleLLMChat` usa `ProxyHardener` (no només tests de `internal/llm`).
- router/middleware: `OPTIONS` no passa per auth, o CORS s’aplica abans de auth.

### 2.4 `network`

- Evidència mínima: tests amb errors simulats (timeouts/5xx) i asserts de retry/backoff.
- Si hi ha “fallback determinista”, s’ha de documentar quan s’activa.

### 2.5 `env_proxy`

- Evidència mínima: nota d’entorn (variables rellevants) o wrapper que estabilitza el cas.
- Si hi ha proxies trencats (p.ex. `127.0.0.1:9`), cal documentar com reproduir i com evitar-ho.

## 3) Verdict guidance

- Si una surface aplica i falta evidència: `WARN` o `PARTIAL` (mai `PASS`).
- Si l’entorn és plan-only i impedeix evidència: `PARTIAL` + `next_action: rerun in build/execute`.

