# Dry Run Extract — Mining → PKLot

> Data: 2026-04-12  
> Font: corpus `design_mining_2026-04-09/*.mining.md` (19 fitxers)  
> Autoritat: `00_SEED_INDEX.mining.md` (índex canònic)  
> Regla hard: **NO APPLY** — Cap edició a PKLot, cap creació de SEED dossiers.

---

## A. Metadata

| Camp | Valor |
|------|-------|
| Data del dry run | 2026-04-12 |
| Corpus escanejat | 19 fitxers `*.mining.md` sota `design_mining_2026-04-09/` |
| Criteri de filtre | Totes les entrades de `00_SEED_INDEX.mining.md` (P0/P1/P2/P3 inclosos) |
| Schema usat | Seed Candidate v1 (MINING_TO_PKLOT_ADAPTER_v1.md) |
| IDs proposats | Tots `TBD` (no assignats — regla NO APPLY) |

---

## B. Resultats — Taula de candidates

| CAND | Title | Priority | Horizon | Source doc | Problem (1 línia) | possible_duplicate_of | recommended_action | exploration_required | confidence |
|------|-------|--------:|--------|------------|-------------------|----------------------|--------------------|:-------------------:|------------|
| CAND-001 | Ticket Runtime Contract (IPC + FSM persistent) | P0 | NOW (h) | `00_SEED_INDEX.mining.md`, `02_TICKET_SYSTEM.mining.md` | Múltiples canals generen inconsistències d'estat i auditories incompletes. | `feat-019` (ARCHIVED), `ADR 024/025` | DEFER | false | high |
| CAND-002 | Authority List — Contracte vs Codi vs Docs | P0 | NOW (h) | `00_SEED_INDEX.mining.md`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md` | Conflictes entre documentació i codi generen múltiples "veritats". | `00_CONTRAST_SDD.mining.md` (document intern) | DEFER | false | high |
| CAND-003 | Ticket State Machine — Transicions Mínimes + Router Semantics | P0 | NOW (h) | `00_SEED_INDEX.mining.md`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md` | Estats impossibles i drift operatiu quan les transicions no estan definides formalment. | `feat-019` (ARCHIVED) | DEFER | false | high |
| CAND-004 | Ticket JSON Validation + Quarantine Policy | P0 | NOW (h) | `00_SEED_INDEX.mining.md`, `02_TICKET_SYSTEM.mining.md` | Sense validació estricta, el ticket es converteix en "bag of fields" i trenca compatibilitat. | `feat-019` (partial overlap) | NEEDS_REVIEW | false | med |
| CAND-005 | System Mutation Contract + HITL Approval Primitive | P0 | NOW (h) | `00_SEED_INDEX.mining.md`, `02_TICKET_SYSTEM.mining.md` | Mutacions directes de sistema creen bypassos de seguretat i drift. | `feat-049` (partial overlap), `feat-067` (ARCHIVED, partial) | KEEP | true | med |
| CAND-006 | Kernel Security Modes + SAFE_MODE/LOCKDOWN Overlays | P0 | NOW (h) | `00_SEED_INDEX.mining.md`, `13_SECURITY_MODEL.mining.md` | Sense contracte de modes, cada component implementa la seva pròpia semàntica de seguretat. | `feat-049` (ARCHIVED), `feat-012` (SPEC DONE) | DEFER | false | high |
| CAND-007 | Rings Architecture — Ring 0 Bootstrap + Immutability | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `04_SEED_AND_AGENT_ANATOMY.mining.md` | Sense boundary clar entre anells, el sistema no pot garantir aïllament. | — | DEFER | true | low |
| CAND-008 | Agent Capabilities — Zero Tools Default + Kernel Gating | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `05_GUARDIAN.mining.md` | Agent amb eines per defecte o que veu eines que no pot usar genera superfície d'atac. | — | DEFER | false | med |
| CAND-009 | Crash Recovery — kernel.state.json + Boot Recovery Sequence | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `01_KERNEL.mining.md` | Tickets orfes, dobles execucions o pèrdua d'auditoria post-crash (OOM/kill -9/pànic). | — | KEEP | true | med |
| CAND-010 | Load Balancer Backpressure — Allow/Delay/Spool/Reject Thresholds | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `01_KERNEL.mining.md` | Sense llindars i decisions deterministes, el sistema entra en allau (OOM). | `feat-053` (ARCHIVED), `feat-063` (ARCHIVED) | DEFER | false | high |
| CAND-011 | Quarantine System — Tickets/Engrams Manifest + Recovery Policy | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `03_FILESYSTEM_AND_DEPARTMENTS.mining.md` | Sense quarantena, inputs corruptes o sospitosos entren al pipeline i contaminen memòria/auditoria. | — | KEEP | true | med |
| CAND-012 | Context Builder — Multi-Tier Hierarchy + Token/Byte Budgets | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `08_CONTEXT_BUILDER.mining.md` | Sense pressupost estable i jerarquia, el sistema cau per OOM/latència. | `feat-008` (spec existent) | NEEDS_REVIEW | false | med |
| CAND-013 | Context Segregation — IT/Sec-Only Global State + Auditor Context | P1 | NEXT (h) | `00_SEED_INDEX.mining.md`, `08_CONTEXT_BUILDER.mining.md` | Agents de baixa confiança veuen estat global/host = reconeixement intern i vector d'atac. | — | KEEP | true | low |
| CAND-014 | Engram Format — .engram.md + JSON Frontmatter + Immutability | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `07_ENGRAM.mining.md` | Sense format definit, la memòria deriva i trenca auditabilitat. | `feat-003` (partial overlap) | NEEDS_REVIEW | false | med |
| CAND-015 | Engram Index — SQLite FTS5 + WAL Mode | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `03_FILESYSTEM_AND_DEPARTMENTS.mining.md` | Sense decisió estable, el sistema canvia d'estratègia constantment. | `feat-003` (partial overlap) | NEEDS_REVIEW | false | med |
| CAND-016 | Librarian MCP Contract — memory_query + memory_store | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `07_ENGRAM.mining.md` | Sense contracte, cada consumer inventa una API i apareix drift. | — | DEFER | false | med |
| CAND-017 | Tool Registry — Data-Driven + Canonical Discovery | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `09_EXTENSIBILITY.mining.md` | Sense registry, les eines no es poden descobrir ni versionar dinàmicament. | — | DEFER | false | low |
| CAND-018 | Observability Security — No Internet Exposure + VPN Rule | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `10_OBSERVABILITY.mining.md` | Sistema exposat a internet perd el model de seguretat. | — | DEFER | false | med |
| CAND-019 | Event Contract — reconnect/backoff + observability | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `10_OBSERVABILITY.mining.md` | Sense contracte, el dashboard deriva i falla sovint. | `feat-006` (partial overlap) | NEEDS_REVIEW | false | med |
| CAND-020 | Telegram Bridge — Secrets Management + Anti-Abuse | P2 | LATER (h) | `00_SEED_INDEX.mining.md`, `12_TELEGRAM_BRIDGE.mining.md` | Secrets a git + absència de controls generen risc d'abús. | — | DEFER | false | med |

*(h) = heurístic, no autoritat — horizon proposat segons regla P0→NOW, P1→NEXT, P2/P3→LATER*

---

## C. Resum executiu

### Comptes per priority

| Priority | Total |
|----------|------:|
| P0 | 6 |
| P1 | 7 |
| P2 | 7 |
| P3 | 0 |
| **Total** | **20** |

### Comptes per recommended_action

| Action | Total |
|--------|------:|
| KEEP | 3 |
| DEFER | 11 |
| NEEDS_REVIEW | 4 |
| CONVERT_LATER | 0 |
| DISCARD | 2* |

*Els 2 DISCARD anteriors (CAND-001, CAND-003) s'han reclasificat a DEFER per consistència amb el nou schema (no hi ha DISCARD com a opció vàlida — tota candidate amb evidence_refs real rep DEFER, no DISCARD).

### Top 5 candidates més prometedores (KEEP)

| Rank | CAND | Title | Why |
|-----:|------|-------|-----|
| 1 | CAND-005 | System Mutation Contract + HITL Approval Primitive | Diferent de feat-049 (enforcement) — aquí es tracta el QUÈ és mutació, no el COM. Cap feat existent cobreix el contracte. |
| 2 | CAND-009 | Crash Recovery — kernel.state.json + Boot Recovery Sequence | 01_KERNEL.mining.md marca Recovery Manager com UNKNOWN. Prou important per prioritzar. |
| 3 | CAND-011 | Quarantine System — Tickets/Engrams Manifest + Recovery Policy | 03_FILESYSTEM_AND_DEPARTMENTS.mining.md:75 diu quarantine manager UNKNOWN. Protecció crítica. |
| 4 | CAND-013 | Context Segregation — IT/Sec-Only + Auditor Context | drift-prone gap #1 de 00_SUMMARY.mining.md (format agenticos_state no especificat). |

---

## D. Detall de candidates (format complet)

---

### CAND-001

```
candidate_id: CAND-001
title: Ticket Runtime Contract (IPC + FSM persistent)
source_doc: 00_SEED_INDEX.mining.md, 02_TICKET_SYSTEM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:11"
priority: P0
horizon: NOW (h) — heurístic, no autoritat
trigger: design_gap
problem: Múltiples canals (REST/gRPC/queues) generen inconsistències d'estat i auditories incompletes.
intent: Tenir .ticket.json com l'únic contracte de comunicació interna, amb màquina d'estats persistent.
scope_hypothesis_in:
  - Schema mínim del ticket
  - FSM persistent
  - Atomicitat via rename
  - Transicions mínimes
scope_hypothesis_out:
  - Implementació d'agent autònom
  - Crawlers historic
risks:
  - risk: Drift cap a múltiples protocols
    severity: High
    mitigation: Definir autoritat única (ADR 024/025)
success_signals:
  - Kernel llegeix ticket com a font única
  - No existeixen altres canals IPC actius
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-019
  - ADR-024
  - ADR-025
evidence_refs:
  - artifacts/features_for_specs/feat-019.json (state: ARCHIVE)
  - 05_ADR_DECISION_LOG.md (ADR 024/025)
confidence: high
recommended_action: DEFER
```

**Nota**: Cobert per feat-019 (Ticket Runtime Contract Normalization, ARCHIVED). El mining ho detectava com a P0 abans de l'arxivament. No calnou feature — mantindre DEFER.

---

### CAND-002

```
candidate_id: CAND-002
title: Authority List — Contracte vs Codi vs Docs
source_doc: 00_SEED_INDEX.mining.md, TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:12"
priority: P0
horizon: NOW (h)
trigger: governance_gap
problem: Conflictes entre documentació i codi generen múltiples "veritats" al sistema.
intent: Definir jerarquia d'autoritat explícita (ADR → specs SDD → codi → legacy docs).
scope_hypothesis_in:
  - Autoritat de contractes
  - Regles de resolució de conflicts
scope_hypothesis_out:
  - Implementació tècnica
risks:
  - risk: Drift si es llegeixen docs legacy sense contrastar
    severity: High
    mitigation: Mantenir authority list actualitzada
success_signals:
  - Authority list documentada i accessible
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - 00_CONTRAST_SDD.mining.md (document intern del mining)
evidence_refs:
  - audit_reports/design_mining_2026-04-09/00_CONTRAST_SDD.mining.md
confidence: high
recommended_action: DEFER
```

**Nota**: No és una feature — és un document de governança. Consolida el que ja fa 00_CONTRAST_SDD.mining.md.

---

### CAND-003

```
candidate_id: CAND-003
title: Ticket State Machine — Transicions Mínimes + Router Semantics
source_doc: 00_SEED_INDEX.mining.md, TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:13"
priority: P0
horizon: NOW (h)
trigger: design_gap
problem: Estats impossibles i drift operatiu quan les transicions no estan definides formalment.
intent: Definir FSM mínima amb transicions vàlides i semàntica de state→folder.
scope_hypothesis_in:
  - Estats vàlids
  - Transicions permeses
  - Rename atòmic
  - Semàntica Router
scope_hypothesis_out:
  - FSM completa (11 estats legacy)
risks:
  - risk: Cost migratori alt
    severity: High
    mitigation: Definir frontera amb model ric
success_signals:
  - FSM mínima implementada
  - Transicions il·legals bloquegades
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-019
evidence_refs:
  - artifacts/features_for_specs/feat-019.json (state: ARCHIVE)
confidence: high
recommended_action: DEFER
```

**Nota**: Cobert per feat-019. feat-019 ja tanca explícitament el cas "E_LOAD_REJECTED".

---

### CAND-004

```
candidate_id: CAND-004
title: Ticket JSON Validation + Quarantine Policy
source_doc: 00_SEED_INDEX.mining.md, 02_TICKET_SYSTEM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:14"
priority: P0
horizon: NOW (h)
trigger: security_gap
problem: Sense validació estrict a, el ticket es converteix en "bag of fields" i trenca compatibilitat.
intent: Tenir un schema formal i política de quarantena per desviacions.
scope_hypothesis_in:
  - Schema JSON del ticket
  - Validació
  - Quarantena
  - Camps core
scope_hypothesis_out:
  - Implementació de quarantena manager
risks:
  - risk: Migracions de schema futures
    severity: High
    mitigation: Compatibilitat enrere
success_signals:
  - Schema formal existent
  - Desviacions detectades i quarantineades
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-019
evidence_refs:
  - artifacts/features_for_specs/feat-019.json (state: ARCHIVE)
  - audit_reports/design_mining_2026-04-09/03_FILESYSTEM_AND_DEPARTMENTS.mining.md:78 ("UNKNOWN — No especificat")
confidence: med
recommended_action: NEEDS_REVIEW
```

**Nota**: overlap parcial amb feat-019. 03_FILESYSTEM_AND_DEPARTMENTS.mining.md:78 diu "Límit de mida per identity/tickets (filesystem) — No especificat". Cal verificar si la validació JSON i quarantena ja estan implementades o cal feature separada. **needs_manual_review: contrastar amb feat-019 spec i implementació real.**

---

### CAND-005

```
candidate_id: CAND-005
title: System Mutation Contract + HITL Approval Primitive
source_doc: 00_SEED_INDEX.mining.md, 02_TICKET_SYSTEM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:15"
priority: P0
horizon: NOW (h)
trigger: security_gap
problem: Mutacions directes de sistema creen bypassos de seguretat i drift.
intent: Definir què és mutació vs no mutació; mutacions passen per ticket auditat.
scope_hypothesis_in:
  - Definició de "system mutation"
  - Contracte .approval.json
  - Estat de ticket associat
scope_hypothesis_out:
  - Dashboard UI
  - Implementació de Guardian
  - Autodoc
risks:
  - risk: Scope creep cap a HITL complet
    severity: High
    mitigation: Definir frontera MVP
success_signals:
  - Mutacions passen per ticket
  - .approval.json consultable
exploration_required: true
exploration_reason: Diferent de feat-049 (enforcement de modes) — aquí es defineix QUÈ cal marcar com a mutació, no COM s'enforsa. Múltiples unknowns pendents.
possible_duplicate_of:
  - feat-049 (SEC-01 Security Modes — partial)
  - feat-067 (approvals backend MVP — ARCHIVED — partial)
evidence_refs:
  - artifacts/features_for_specs/feat-049-sec-01-security-modes-enforcement.json (state: ARCHIVE)
  - artifacts/features_for_specs/feat-067-sec-06-approvals-backend-mvp.json (state: ARCHIVE)
confidence: med
recommended_action: KEEP
```

**Nota**: El contracte de "system mutation" és diferent de l'enforcement de modes (feat-049). Ja existeix feat-067 (approvals backend MVP, ARCHIVED) però el contracte de què és una mutació no està formalitzat. **CAND-005 és la candidate de més alta prioritat segons el mining.**

---

### CAND-006

```
candidate_id: CAND-006
title: Kernel Security Modes + SAFE_MODE/LOCKDOWN Overlays
source_doc: 00_SEED_INDEX.mining.md, 13_SECURITY_MODEL.mining.md
source_anchor: "00_SEED_INDEX.mining.md:16"
priority: P0
horizon: NOW (h)
trigger: security_gap
problem: Sense contracte de modes, cada component implementa la seva pròpia semàntica de seguretat.
intent: Definir modes (READ_ONLY/PROPOSE/EXECUTE_SAFE/FULL) i overlay d'emergència (SAFE_MODE/LOCKDOWN).
scope_hypothesis_in:
  - Modes de kernel
  - Transicions
  - Canals de notificació
  - Overlay semantics
scope_hypothesis_out:
  - Persistència de mode entre reinicis
  - HITL per activar FULL
risks:
  - risk: Drift entre doc legacy i API/spec
    severity: High
    mitigation: Contrastar amb feat-012 i feat-049
success_signals:
  - Modes definits
  - Transicions validades
  - API exposa mode
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-049
  - feat-012
evidence_refs:
  - artifacts/features_for_specs/feat-049-sec-01-security-modes-enforcement.json (state: ARCHIVE)
  - artifacts/specs/feat-012-kernel-status-api.md (SPEC DONE)
  - 05_ADR_DECISION_LOG.md (ADR-028)
confidence: high
recommended_action: DEFER
```

**Nota**: Cobert per feat-049 (SEC-01, ARCHIVED) + feat-012 (Kernel Status API, SPEC DONE). ADR-028 és la font. El mining ho identificava com a P0 abans d'implementar-se.

---

### CAND-007

```
candidate_id: CAND-007
title: Rings Architecture — Ring 0 Bootstrap + Immutability
source_doc: 00_SEED_INDEX.mining.md, 04_SEED_AND_AGENT_ANATOMY.mining.md
source_anchor: "00_SEED_INDEX.mining.md:17"
priority: P1
horizon: NEXT (h)
trigger: architecture_gap
problem: Sense boundary clar entre anells, el sistema no pot garantir aïllament.
intent: Definir la jerarquia de rings (Ring 0 = bootstrap immutable) i les seves propietats.
scope_hypothesis_in:
  - Ring 0 bootstrap
  - Ring 1 Guardian
  - Immutabilitat
  - Isolament
scope_hypothesis_out:
  - Implementació de ring scheduler
risks:
  - risk: Canvi de paradigma
    severity: Medium
    mitigation: Documentar bé
success_signals:
  - Rings definits
  - No-calcular boot executat primer
exploration_required: true
exploration_reason: Conceptuat al mining però sense dossier existent. P1, "reserve now" — cal explorar abans de proposar feature.
possible_duplicate_of: []
evidence_refs: []
confidence: low
recommended_action: DEFER
```

---

### CAND-008

```
candidate_id: CAND-008
title: Agent Capabilities — Zero Tools Default + Kernel Gating
source_doc: 00_SEED_INDEX.mining.md, 05_GUARDIAN.mining.md
source_anchor: "00_SEED_INDEX.mining.md:18"
priority: P1
horizon: NEXT (h)
trigger: security_gap
problem: Agent amb eines per defecte o que veu eines que no pot usar genera superfície d'atac.
intent: Un agent neix amb zero eines; les capacitats es concedeixen explícitament a identity.md.
scope_hypothesis_in:
  - Zero tools default
  - Gating a identity.md
  - Kernel amaga eines no disponibles
scope_hypothesis_out:
  - identity.md structure detallat
  - UI de permisos
risks:
  - risk: Complexitat de permisos
    severity: Medium
    mitigation: Mantenir simple
success_signals:
  - Agent amb zero tools funciona
  - Eines no autoritzades invisibles
exploration_required: false
exploration_reason: N/A
possible_duplicate_of: []
evidence_refs:
  - artifacts/features_for_specs/feat-049-sec-01-security-modes-enforcement.json (state: ARCHIVE)
  - artifacts/features_for_specs/feat-047-guardian-hardening-sec-00d-e-f.json
confidence: med
recommended_action: DEFER
```

**Nota**: P1 important però no blocant. Cal explorar relació amb feat-047 (Guardian hardening). No urgent.

---

### CAND-009

```
candidate_id: CAND-009
title: Crash Recovery — kernel.state.json + Boot Recovery Sequence
source_doc: 00_SEED_INDEX.mining.md, 01_KERNEL.mining.md
source_anchor: "00_SEED_INDEX.mining.md:19"
priority: P1
horizon: NEXT (h)
trigger: design_gap
problem: Tickets orfes, dobles execucions o pèrdua d'auditoria post-crash (OOM/kill -9/pànic).
intent: Tenir estat persistent del kernel + seqüència de recovery definida al boot.
scope_hypothesis_in:
  - kernel.state.json fields mínims
  - Heartbeat periòdic
  - Boot recovery sequence
  - Ticket orphan re-routing
scope_hypothesis_out:
  - Crash prevention
  - Persistència d'altres components
risks:
  - risk: Compatibilitat amb arxius existents
    severity: High
    mitigation: Disseny retrocompatible
success_signals:
  - Post-crash: tickets actius recuperats
  - No dobles execucions
exploration_required: true
exploration_reason: 01_KERNEL.mining.md:78 marca "Recovery Manager" com UNKNOWN. Sense implementació existent coneguda. Múltiples unknowns tècnics (quins camps en kernel.state.json? com detectar instància prèvia? com fer re-routing segur?).
possible_duplicate_of: []
evidence_refs:
  - audit_reports/design_mining_2026-04-09/01_KERNEL.mining.md:78 ("Recovery Manager — UNKNOWN")
confidence: med
recommended_action: KEEP
```

**Nota**: P1 crítica — sense crash recovery, qualsevol fallada trenca el sistema. 01_KERNEL.mining.md diu "UNKNOWN" per Recovery Manager. **Cal verificar codi: kernel.state.json existeix a l'actual codebase?**

---

### CAND-010

```
candidate_id: CAND-010
title: Load Balancer Backpressure — Allow/Delay/Spool/Reject Thresholds
source_doc: 00_SEED_INDEX.mining.md, 01_KERNEL.mining.md
source_anchor: "00_SEED_INDEX.mining.md:20"
priority: P1
horizon: NEXT (h)
trigger: design_gap
problem: Sense llindars i decisions deterministes, el sistema entra en allau (OOM, loadavg fora de control).
intent: Kernel monitoritza mètriques i decideix Allow/Delay/Spool/Reject amb llindars explícits.
scope_hypothesis_in:
  - Llindars configurables
  - Decisió SPOOL = retard (no pèrdua)
  - LoadBalancer al Kernel
scope_hypothesis_out:
  - Implementació scheduler
  - UX de retry
risks:
  - risk: Impacte transversal
    severity: Medium
    mitigation: Provar bé
success_signals:
  - Loadavg estable
  - OOM evitades
  - Spool retrasa (no rebutja)
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-053
  - feat-063
evidence_refs:
  - artifacts/features_for_specs/feat-053-sec-0x-plus-1-backpressure-admission-control.json (state: ARCHIVE)
  - artifacts/features_for_specs/feat-063-bp-kernel-01-kernel-side-backpressure-admission-control.json (state: ARCHIVE)
confidence: high
recommended_action: DEFER
```

**Nota**: Cobert per feat-053 i feat-063. 00_SEED_INDEX del mining és del 2026-04-09; des d'aleshores s'han implementat ambdós feat (ARCHIVED). Confirmat com a duplicat.

---

### CAND-011

```
candidate_id: CAND-011
title: Quarantine System — Tickets/Engrams Manifest + Recovery Policy
source_doc: 00_SEED_INDEX.mining.md, 03_FILESYSTEM_AND_DEPARTMENTS.mining.md
source_anchor: "00_SEED_INDEX.mining.md:21"
priority: P1
horizon: NEXT (h)
trigger: security_gap
problem: Sense quarantena, inputs corruptes o sospitosos entren al pipeline i contaminen memòria/auditoria.
intent: Quarantena classifica per motiu/severitat, registra en manifest.json, defineix política de recuperació.
scope_hypothesis_in:
  - Quarantena manager
  - manifest.json
  - Classificació per severitat
  - Política NO auto-recuperar
scope_hypothesis_out:
  - UI de quarantine viewer
  - Cleanup automàtic
risks:
  - risk: Filesystem bloat
    severity: Medium
    mitigation: TTL al manifest
success_signals:
  - Tickets corruptes a quarantine/
  - Manifest actualitzat
  - No auto-recuperació
exploration_required: true
exploration_reason: 03_FILESYSTEM_AND_DEPARTMENTS.mining.md:75 diu "Quarantine manager + manifest.json — UNKNOWN". No hi ha feat-xxx existent. Cal explorar abans de proposar.
possible_duplicate_of: []
evidence_refs:
  - audit_reports/design_mining_2026-04-09/03_FILESYSTEM_AND_DEPARTMENTS.mining.md:75 ("Quarantine manager — UNKNOWN")
confidence: med
recommended_action: KEEP
```

**Nota**: No existeix feat encara per aquesta funcionalitat. P1 important.

---

### CAND-012

```
candidate_id: CAND-012
title: Context Builder — Multi-Tier Hierarchy + Token/Byte Budgets
source_doc: 00_SEED_INDEX.mining.md, 08_CONTEXT_BUILDER.mining.md
source_anchor: "00_SEED_INDEX.mining.md:22"
priority: P1
horizon: NEXT (h)
trigger: design_gap
problem: Sense pressupost estable i jerarquia, el sistema cau per OOM/latència.
intent: Límit global (32KB/8.192 tokens) i jerarquia (Global → Dept → Agent → Tasca) + política de truncament.
scope_hypothesis_in:
  - Jerarquia multi-tier
  - Pressupostos (32KB global, 8KB tools)
  - Truncament per prioritat
scope_hypothesis_out:
  - Implementació de sliding window
  - UI de budget viewer
risks:
  - risk: Complexitat de truncament
    severity: Medium
    mitigation: Simple fallback
success_signals:
  - Prompts estabilitzats
  - OOM evitades
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-008
evidence_refs:
  - artifacts/specs/feat-008-context-builder.md (SPEC DONE)
  - audit_reports/design_mining_2026-04-09/08_CONTEXT_BUILDER.mining.md (drift-prone gap: "Algorisme baseline de sliding window — no especificat")
confidence: med
recommended_action: NEEDS_REVIEW
```

**Nota**: **needs_manual_review**: feat-008 existeix (SPEC DONE) però "SPEC DONE" no implica implementat. Cal verificar codi. 08_CONTEXT_BUILDER.mining.md diu que l'algorisme de sliding window "no especificat" — podria ser un feat separat o part de CAND-012.

---

### CAND-013

```
candidate_id: CAND-013
title: Context Segregation — IT/Sec-Only Global State + Auditor Context
source_doc: 00_SEED_INDEX.mining.md, 08_CONTEXT_BUILDER.mining.md
source_anchor: "00_SEED_INDEX.mining.md:23"
priority: P1
horizon: NEXT (h)
trigger: security_gap
problem: Agents de baixa confiança veuen estat global/host = reconeixement intern i vector d'atac.
intent: agenticos_state visible només per IT/Sec; Auditor rep "intenció d'acció" + constitució/diff/risc.
scope_hypothesis_in:
  - Restricció agenticos_state a IT/Sec
  - Auditor context especialitzat
  - Zero Trust segregation
scope_hypothesis_out:
  - Implantació detallada
  - UI
risks:
  - risk: Complexitat de permisos
    severity: Medium
    mitigation: Mantenir simple
success_signals:
  - IT/Sec veuen context
  - Altres no
  - Auditor audita sense exposure
exploration_required: true
exploration_reason: drift-prone gap #1 identificat a 00_SUMMARY.mining.md: "Format mínim del context global (agenticos_state)". Cal explorar bé abans de proposar feature.
possible_duplicate_of: []
evidence_refs:
  - audit_reports/design_mining_2026-04-09/00_SUMMARY.mining.md:33 ("drift-prone gap #1")
confidence: low
recommended_action: KEEP
```

**Nota**: context_gap important. La segregació IT/Sec va més enllà del "format mínim" — és una política de seguretat. P1.

---

### CAND-014

```
candidate_id: CAND-014
title: Engram Format — .engram.md + JSON Frontmatter + Immutability
source_doc: 00_SEED_INDEX.mining.md, 07_ENGRAM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:24"
priority: P2
horizon: LATER (h)
trigger: design_gap
problem: Sense format definit, la memòria deriva i trenca auditabilitat.
intent: Engram és .engram.md llegible, metadades JSON (no YAML), immutable post-tancat.
scope_hypothesis_in:
  - Format .engram.md
  - Frontmatter JSON
  - Immutabilitat
  - Correcció via nou engram
scope_hypothesis_out:
  - Indexació
  - Cerca
  - UI
risks:
  - risk: Migració corpus existent
    severity: Medium
    mitigation: Backward compatible
success_signals:
  - Engrams amb format correcte
  - No edits post-tancat
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-003
evidence_refs:
  - artifacts/features_for_specs/feat-003.json
  - artifacts/specs/feat-003-engram-memory.md (unknown state)
confidence: med
recommended_action: NEEDS_REVIEW
```

**Nota**: **needs_manual_review**: contrastar amb feat-003. Verificar estat d'implementació.

---

### CAND-015

```
candidate_id: CAND-015
title: Engram Index — SQLite FTS5 + WAL Mode
source_doc: 00_SEED_INDEX.mining.md, 03_FILESYSTEM_AND_DEPARTMENTS.mining.md
source_anchor: "00_SEED_INDEX.mining.md:25"
priority: P2
horizon: LATER (h)
trigger: design_gap
problem: Sense decisió estable, el sistema canvia d'estratègia constantment.
intent: engram.db usa FTS5 i opera en WAL; existeix índex global.
scope_hypothesis_in:
  - FTS5
  - WAL mode
  - Índex global
  - Crash safety
scope_hypothesis_out:
  - Vector search
  - Embeddings
risks:
  - risk: Migracions
    severity: Medium
    mitigation: Mantenir schema estable
success_signals:
  - FTS5 funcional
  - WAL actiu
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-003
evidence_refs:
  - artifacts/features_for_specs/feat-003.json
confidence: med
recommended_action: NEEDS_REVIEW
```

**Nota**: P2, "reserve now". **needs_manual_review**: contrastar amb feat-003. Decisió de producte/infra ja presa al mining (FTS5+WAL) però cal formalitzar.

---

### CAND-016

```
candidate_id: CAND-016
title: Librarian MCP Contract — memory_query + memory_store
source_doc: 00_SEED_INDEX.mining.md, 07_ENGRAM.mining.md
source_anchor: "00_SEED_INDEX.mining.md:26"
priority: P2
horizon: LATER (h)
trigger: integration_gap
problem: Sense contracte, cada consumer inventa una API i apareix drift.
intent: Eines MCP memory_query i memory_store amb schema, timeout 5s, fallback [].
scope_hypothesis_in:
  - Schema de memory_query/memory_store
  - Timeout
  - Fallback a buit
scope_hypothesis_out:
  - Implementació Librarian
  - UI
risks:
  - risk: Drift contracte
    severity: Medium
    mitigation: Versionar
success_signals:
  - Contracte respectat
  - Timeout actiu
  - Fallback retornant [] en error
exploration_required: false
exploration_reason: N/A
possible_duplicate_of: []
evidence_refs:
  - artifacts/specs/feat-003-engram-memory.md
  - artifacts/specs/feat-008-context-builder.md
confidence: med
recommended_action: DEFER
```

**Nota**: P2. No existeix feat específicament per al contracte MCP encara. Només esmentat a feat-003 i feat-008. Potser candidat a ADR.

---

### CAND-017

```
candidate_id: CAND-017
title: Tool Registry — Data-Driven + Canonical Discovery
source_doc: 00_SEED_INDEX.mining.md, 09_EXTENSIBILITY.mining.md
source_anchor: "00_SEED_INDEX.mining.md:27"
priority: P2
horizon: LATER (h)
trigger: design_gap
problem: Sense registry, les eines no es poden descobrir ni versionar dinàmicament.
intent: Registry data-driven on tools es registren dinàmicament; discovery per rutes canòniques.
scope_hypothesis_in:
  - Registry format
  - Discovery mechanism
  - Rutes canòniques
scope_hypothesis_out:
  - Implementació runtime
  - UI
risks:
  - risk: Complexity
    severity: Low
    mitigation: Mantenir simple
success_signals:
  - Registry funcional
exploration_required: false
exploration_reason: N/A
possible_duplicate_of: []
evidence_refs: []
confidence: low
recommended_action: DEFER
```

**Nota**: P3 candidacy. Caldrà explorar bé abans de tirar endavant.

---

### CAND-018

```
candidate_id: CAND-018
title: Observability Security — No Internet Exposure + VPN Rule
source_doc: 00_SEED_INDEX.mining.md, 10_OBSERVABILITY.mining.md
source_anchor: "00_SEED_INDEX.mining.md:28"
priority: P2
horizon: LATER (h)
trigger: security_gap
problem: Sistema exposat a internet perd el model de seguretat.
intent: "Mai exposat a internet" + VPN com a regla operativa.
scope_hypothesis_in:
  - Regla no-internet
  - VPN com a canal
  - Configuració
scope_hypothesis_out:
  - Implementació xarxa
  - UI
risks:
  - risk: Operatiu
    severity: Medium
    mitigation: Documentar bé
success_signals:
  - No endpoints accesibles des d'internet
exploration_required: false
exploration_reason: N/A
possible_duplicate_of: []
evidence_refs: []
confidence: med
recommended_action: DEFER
```

**Nota**: P2. Constitució operativa — candidat a ADR.

---

### CAND-019

```
candidate_id: CAND-019
title: Event Contract — reconnect/backoff + observability
source_doc: 00_SEED_INDEX.mining.md, 10_OBSERVABILITY.mining.md
source_anchor: "00_SEED_INDEX.mining.md:29"
priority: P2
horizon: LATER (h)
trigger: design_gap
problem: Sense contracte, el dashboard deriva i falla sovint.
intent: Contracte d'esdeveniments amb reconnect/backoff.
scope_hypothesis_in:
  - Schema d'events
  - Reconnect logic
  - Backoff
scope_hypothesis_out:
  - Implementació dashboard
risks:
  - risk: Compatibility
    severity: Medium
    mitigation: Versionar
success_signals:
  - Dashboard rep events sense drift
exploration_required: false
exploration_reason: N/A
possible_duplicate_of:
  - feat-006
evidence_refs:
  - artifacts/features_for_specs/feat-006.json (state: ARCHIVE)
  - artifacts/specs/feat-006-api-server.md
confidence: med
recommended_action: NEEDS_REVIEW
```

**Nota**: **needs_manual_review**: contrastar amb feat-006 (Dashboard). Verificar si el contracte d'events ja existeix o cal definir-lo.

---

### CAND-020

```
candidate_id: CAND-020
title: Telegram Bridge — Secrets Management + Anti-Abuse
source_doc: 00_SEED_INDEX.mining.md, 12_TELEGRAM_BRIDGE.mining.md
source_anchor: "00_SEED_INDEX.mining.md:30"
priority: P2
horizon: LATER (h)
trigger: security_gap
problem: Secrets a git + absència de controls generen risc d'abús.
intent: Secrets fora de git + controls anti-abús.
scope_hypothesis_in:
  - Secrets fora de git
  - Controls anti-abús
  - Configuració segura
scope_hypothesis_out:
  - UI de gestió de secrets
risks:
  - risk: Operatiu
    severity: Medium
    mitigation: Documentar
success_signals:
  - Secrets fora git
  - Controls implementats
exploration_required: false
exploration_reason: N/A
possible_duplicate_of: []
evidence_refs: []
confidence: med
recommended_action: DEFER
```

**Nota**: P2. Candidat a feature o ADR segons scoping. Molt dependent de contexto operatiu.

---

## E. No Apply Confirmation

```
✅ No s'ha editat 00_project_documentation/04_PARKING_LOT.md
✅ No s'han creat fitxers SEED-*.md a seed_dossiers/
✅ No s'han creat feat-*.json nous
✅ No s'ha executat cap fase SDD
✅ Tots els proposed_seed_id = TBD (no assignats)
✅ Tots els horizon porten "(h)" = heurístic, no autoritat

Aquest fitxer és una proposta per a revisió humana.
Qualsevol aplicació depèn d'un triage batch signat pel responsable.
```

---

*Adapter v1 + dry run generats amb data 2026-04-12. Propera evolució: triage batch real (OUT OF SCOPE d'aquesta fase).*
