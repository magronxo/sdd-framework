# Security Controls Map (operational)

**STATUS:** ACTIVE  
**AUTHORITY:** CANONICAL (operational reference)  
**Purpose:** Documentar quins controls de seguretat són **policy-driven** i quins són **hardcoded**, per evitar assumptions incorrectes.

## SEC-00B2 — HTTP/URL validation (status: implemented)

### Capa A — Guardian (policy-driven)

- **Ubicació:** `02_implementation/internal/kernel/guardian.go` (`Guardian.ValidateHttpRequest`)
- **Controla:**
  - ports bloquejats (via policy)
  - limit de mida del body (via policy)
- **Configurabilitat:** ✅ Sí (policy/config)

### Capa B — Executor (hardcoded)

- **Ubicació:** `02_implementation/internal/kernel/executor.go` (`isBlockedURL`)
- **Controla:**
  - esquemes prohibits (no http/https)
  - protecció SSRF (localhost, link-local, metadata, rangs privats)
- **Configurabilitat:** ❌ No (hardcoded)

### Nota de governança

Si en el futur cal bloqueig dinàmic per domini/URL (policy-driven), llavors `isBlockedURL` s’hauria de promoure a Guardian i passar a ser configurable. Fins llavors, es considera un control estable i deliberadament hardcoded.

