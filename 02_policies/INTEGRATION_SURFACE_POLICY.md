# Policy: Integration Surface Gates (SPEC / VERIFY)

> **Status:** Active
> **Date:** 2026-04-10
> **Scope:** Any feature that exposes behavior via browser/FS/network/handlers

## Purpose

Prevent "false PASSes" when:

- `curl` works but the browser fails (CORS + preflight).
- Core logic is correct but the handler does not call it (wiring).
- Windows/ACLs or paths (spaces/quotes) break the real flow.

## Principle

**Surface-aware verification.**
The verdict can only be `PASS` if evidence exists for the affected surface.

## 1) Surface classification (SPEC)

When writing a SPEC, declare which surfaces apply (boolean):

- `browser`: web UI / Vite / cross-origin / cookies / storage
- `os_fs`: local filesystem, Windows paths, permissions, `ReadDir`, `os.Stat`
- `wiring`: handler → service/core, feature flags, routing, middleware order
- `network`: outbound HTTP, retries, timeouts, provider health
- `env_proxy`: proxies, secrets, ports, local dev constraints

**Rule:** if no surface is declared, `wiring=true` is assumed at minimum (every feature has some form of integration).

## 2) Required evidence (VERIFY)

### 2.1 `browser`

- Minimum evidence: screenshot/note from Network tab (or equivalent) + real result.
- If there is an `Authorization` header: must demonstrate that the server accepts `OPTIONS` preflight.
  - Example (curl):
    - `curl -i -X OPTIONS http://localhost:8080/api/v1/<route> -H "Origin: http://localhost:5173" -H "Access-Control-Request-Method: GET" -H "Access-Control-Request-Headers: authorization,content-type"`

**Rule:** `curl GET/POST` does not validate CORS.

### 2.2 `os_fs`

- Minimum evidence: tests (if possible) + one manual test with real path.
- Cases to cover if applicable:
  - path with spaces
  - path with quotes (`"K:\Path"` / `'K:\Path'`) → sanitize/trim
  - existing directory but not accessible (ACL)

### 2.3 `wiring`

Minimum evidence: a test (or equivalent evidence) demonstrating that the real entry point calls the core logic.

Examples:

- handler `handleRequest` uses `ServiceLayer` (not only `internal/` tests).
- router/middleware: `OPTIONS` does not go through auth, or CORS is applied before auth.

### 2.4 `network`

- Minimum evidence: tests with simulated errors (timeouts/5xx) and retry/backoff asserts.
- If there is a "deterministic fallback", it must be documented when it activates.

### 2.5 `env_proxy`

- Minimum evidence: environment note (relevant variables) or wrapper that stabilizes the case.
- If there are broken proxies (e.g. `127.0.0.1:9`), it must be documented how to reproduce and how to avoid it.

## 3) Verdict guidance

- If a surface applies and evidence is missing: `WARN` or `PARTIAL` (never `PASS`).
- If the environment is plan-only and prevents evidence: `PARTIAL` + `next_action: rerun in build/execute`.
