# ROADMAP vs REALITY CHECK — 2026-04-12

## Propòsit

Corregir drift detectat: "Fase 3 (robustesa operativa) no té archived features" és fals.
Revisar l'estat real de les features agrupades per fase segons el ROADMAP.

---

## Fase 0 — Delimitation

**Objectiu:** Separar product/runtime vs development concerns.

| Feature | Estat | Títol |
|---------|-------|-------|
| feat-040 | ARCHIVE | Enforcement Surfaces (VERIFY/AUDIT gates) |

**Estat real:** Una feature ARCHIVED (feat-040) que fa obligatori declarar SURFACES als reports VERIFY/AUDIT.
Fase 0 té 1 feature, no buida.

---

## Fase 1 — Governance Stabilization

**Objectiu:** Governança coherent i explícita.

| Feature | Estat | Títol |
|---------|-------|-------|
| feat-041 | ARCHIVE (WARN) | FileTree ACL/Permission Errors |
| feat-042 | ARCHIVE (WARN) | Dashboard migracio providers registry |
| feat-043 | ARCHIVE | Migracio secrets providers a secrets.providers.json |
| feat-044 | ARCHIVE | WS chat respeta LoadConfigLoader() |

**Estat real:** 4 features ARCHIVED. Dos amb verify PARTIAL / audit WARN (feat-041, feat-042) per limitacions del test harness Windows.
Fase 1 té contingut real.

---

## Fase 2 — Context Maturity

**Objectiu:** Context retrieval reliable and bounded.

| Feature | Estat | Títol |
|---------|-------|-------|
| feat-008 | ARCHIVE | Context Builder (MVP) |
| feat-009 | ARCHIVE (legacy) | Load Balancer |

**Estat real:** Dues features ARCHIVED (una legacy). Nota: feat-008 és Context Builder, no memòria persistent.
Fase 2 té 2 features.

---

## Fase 3 — Skills Maturity

**Objectiu:** De capabilities informals a skills controlades només on es justifiquen.

| Feature | Estat | Titol |
|---------|-------|-------|
| feat-045 | ARCHIVE | Skills Maturity Phase 3 (registry, vendor, enforcement) |
| feat-046 | ARCHIVE | Skills Enforcement Phase 4 (TASKS/VERIFY/AUDIT gates) |
| feat-048 | ARCHIVE | Skills Governance E2E Canary |

**Estat real:** 3 features ARCHIVED, totes PASS amb verification i audit complert. La cronologia és:
- feat-045: archived 2026-04-10 22:53
- feat-046: archived 2026-04-10 23:21
- feat-048: archived 2026-04-11 01:45

**Feat-047 (Guardian Hardening, SEC-00D/E/F) pertany a la seqüència de seguretat** (SEC-00A→B→B2→C→D→E→F→01→01b→02). No és Skills.
**Feat-047 no és part de Fase 3 segons el ROADMAP** — és Governance Stabilization o bé un grup paral·lel de seguretat.

---

## Fase 4 — External Framework Mapping

**Objectiu:** Entendre sistemes externs abans d'adaptar.

Cap feature ARCHIVED amb etiqueta "Phase 4" o similitud.

**Estat real:** Fase 4 buida en contingut arxivat.

---

## Fase 5 — Adaptation

**Objectiu:** Absorbir només el que sobreviu la traducció local.

Cap feature ARCHIVED.

**Estat real:** Fase 5 buida.

---

## Fase 6 — Consolidation

**Objectiu:** Reduir duplicació quan autoritat i execució son explícites.

Cap feature ARCHIVED.

**Estat real:** Fase 6 buida.

---

## Seqüència Security/TUI paral·lela (no al ROADMAP)

Aquestes features no apareixen al ROADMAP com a grup temàtic però formen una seqüència coherent de seguretat i robustesa operativa:

| Feature | Estat | Titol |
|---------|-------|-------|
| feat-047 | ARCHIVE | Guardian Hardening SEC-00D/E/F |
| feat-049 | ARCHIVE | SEC-01 Security Modes Enforcement |
| feat-050 | ARCHIVE | SEC-01b Kernel Status Invariants |
| feat-051 | ARCHIVE | SEC-02 Emergency Overlays |
| feat-052 | ARCHIVE | Backpressure Wiring Real |
| feat-053 | ARCHIVE | SEC-0x+1 Backpressure Admission Control |
| feat-054 | ARCHIVE | SEC-0x+2 Kernel Runtime Signals |
| feat-055 | ARCHIVE | SEC-04 Action Log MVP |
| feat-056 | ARCHIVE | SEC-06 Kernel Telemetry Wiring |
| feat-057 | ARCHIVE (doc-only) | UI-01 WebUI Shell Contract |
| feat-058 | ARCHIVE | TUI-01 API Baseline |
| feat-059 | ARCHIVE | SEC-02 Surface Authority Minimal |
| feat-060 | ARCHIVE | SEC-03 Kernel Mediation MVP |
| feat-061 | ARCHIVE | SEC-01d Overlay Clear Local Strong |
| feat-062 | ARCHIVE | SEC-01e Emergency Overlay Exit Fallback |
| feat-063 | ARCHIVE | BP-KERNEL-01 Kernel-side Backpressure Admission Control |
| feat-064 | ARCHIVE | SEC-02b Step-up Local Fort |
| feat-065 | ARCHIVE | SEC-05 Security Reports MVP |
| feat-066 | ARCHIVE | SKILLS-01 Skills Enforcement Canary |
| feat-067 | ARCHIVE | SEC-06 Approvals Backend MVP |
| feat-068 | ARCHIVE | Execution Trace Contract MVP |
| feat-069 | ARCHIVE | Trace Correlation |

**Força:** 22 features (feat-047 a feat-069, excloent feat-058 i feat-067 que són de TUI-01 i SKILLS respectivament).

**Agrupades per tema:**

**Robustesa operativa (backpressure, signals, mediation):**
- feat-052, feat-053, feat-054, feat-056, feat-063

**Seguretat (modes, overlays, authority, step-up, reports, approvals):**
- feat-047, feat-049, feat-050, feat-051, feat-059, feat-060, feat-061, feat-062, feat-064, feat-065, feat-067

**Execution traces:**
- feat-068, feat-069

**TUI baseline i UI shell:**
- feat-057 (doc-only), feat-058

---

## Gap Analysis: Què falta realment

### Crash Recovery
**Out of scope declarat a múltiples features:**
- feat-050 out: "Crash recovery"
- feat-052 out: "Crash recovery"
- feat-054 out: "Recovery semantics"

**Statu:** No hi ha feature per crash recovery. El kernel no persisteix estat crític a disk per recuperar-lo.

### kernel.state.json (persistència mode/overlay)
**Out of scope a:**
- feat-050 out: "Persisting emergency_overlay to kernel.state.json"
- feat-051 out: "Persisting overlay to kernel.state.json"
- feat-052 out: "Persisting backpressure state to kernel.state.json"
- feat-056 out: "kernel.state.json persistence"

**Statu:** Overlay sticky fins a restart (arxiu feat-051 nota: "Cannot clear via API per ADR-028. Sticky until restart").
Overlay clear via fitxer trigger implementat (feat-062) però no persistència.

### Retry semantics
**Out of scope a:**
- feat-053 out: "Rejection tracking in last_error"

**Statu:** feat-053 implementa backpressure admission amb Retry-After: 30, però no hi ha policy de retry amb backoff exponent, circuit breaker, o dead letter queue.

### kernel.ticket_id injection
**Out of scope a:**
- feat-069 out: "Kernel-side ticket_id injection (TBD)"

**Statu:** trace correlation funciona però kernel no injecta ticket_id als ActionEvents. Projecció nota que la correlació no pot funcionar sense això.

### ReactFlow projection (traces)
**Out of scope a:**
- feat-068 out: "ReactFlow projection (visual)"
- feat-069 out: "ReactFlow projection"

**Statu:** Contract MVP fet, correlació feta, projecció visual pendent.

---

## Conclusions

1. **Fase 3 NO està buida.** Té 3 features (feat-045, 046, 048) totes ARCHIVED i PASS.

2. **Fases 4, 5, 6 estan buides** en contingut arxivat. El ROADMAP preveu consolidació però no s'ha generat feature per a aquestes fases.

3. **La seqüència Security/Robustesa (feat-047 a feat-069) és el gruix real del treball** post Phase 3 segons el ROADMAP, però NO apareix com a grup temàtic al ROADMAP. Aquestes features pertanyen a una agrupació paral·lela que caldria documentar.

4. **Gaps confirmats sense feature activa:**
   - Crash recovery
   - kernel.state.json persistència (mode/overlay/backpressure)
   - Retry semantics amb backoff/circuit breaker
   - Kernel-side ticket_id injection (per a trace correlation)

5. **Fase 1 amb feat-041/042 en WARN** — no blocker però test harness Windows limita la verificació completa.

---

## Accions recomanades

| Acció | Prioritat | Descripció |
|-------|-----------|------------|
| 1 | P1 | Actualitzar ROADMAP per afegir grup "Security/Robustesa" com a fase paral·lela |
| 2 | P2 | Crear feature record per crash recovery si és requeriment |
| 3 | P2 | Crear feature record per kernel.state.json persistència si és requeriment |
| 4 | P3 | Revisar feat-041/042 (WARN) — possible gold test amb Task Scheduler |
