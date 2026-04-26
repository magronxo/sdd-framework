# Portfolio de Candidates — Mining → PKLot

> Data: 2026-04-12  
> Font: `dryrun_extract_2026-04-12.md` (CAND-001..CAND-020)  
> Propòsit: Aflorar informació i preparar debat d'arquitectura **sense aplicar res al PKLot**  
> Regla hard: **NO APPLY** — Cap edició a 04_PARKING_LOT.md, cap creació de SEED dossiers.

---

## Resum executiu

| Total candidates | 20 |
|------------------|-----:|
| **Kernel/Ticket core** | 6 |
| **Robustesa operativa** | 3 |
| **Seguretat/autoritat/modes** | 5 |
| **Memòria/Context/Engram/Skills/Prompts** | 5 |
| **UI/Surfaces/Observabilitat** | 3 |

| Action | Count |
|--------|------:|
| KEEP | 4 |
| DEFER | 10 |
| NEEDS_REVIEW | 4 |
| CONVERT_LATER | 2 |

*(h) = heurístic, no autoritat — ordre suggerit segons P0→NOW, P1→NEXT, P2/P3→LATER*

---

## Cluster 1: Kernel/Ticket Core

Fonaments del sistema: contractes de comunicació, estat, i transicions.

| CAND | Què aporta | Action | Duplicat? | Deps | Risc principal | Ordre (h) |
|------|-----------|--------|-----------|------|----------------|-----------|
| **CAND-001** | Defineix `.ticket.json` com a únic contracte IPC amb FSM persistent. | DEFER | feat-019 (ARCHIVED), ADR 024/025 | — | Drift a múltiples protocols | NOW |
| **CAND-002** | Estableix jerarquia d'autoritat explícita (ADR→specs→codi→legacy). | DEFER | 00_CONTRAST_SDD.mining.md (intern) | — | Drift llegint docs legacy | NOW |
| **CAND-003** | FSM mínima amb transicions vàlides i semàntica state→folder. | DEFER | feat-019 (ARCHIVED) | feat-019 | Cost migratori alt | NOW |
| **CAND-004** | Schema JSON del ticket + política de quarantena per desviacions. | NEEDS_REVIEW | feat-019 (partial overlap) | feat-019 | Migracions futures de schema | NOW |
| **CAND-005** | Contracte de "system mutation": què és mutació vs no-mutació. | **KEEP** | feat-049 (partial), feat-067 (partial) | feat-019, feat-055, feat-049 | Scope creep a HITL complet | NOW |
| **CAND-006** | Modes de kernel (READ_ONLY/PROPOSE/EXECUTE_SAFE/FULL) + overlays emergència. | DEFER | feat-049 (ARCHIVED), feat-012 | feat-012, ADR-028 | Drift entre doc legacy i API | NOW |

**Notes cluster:**
- CAND-001/003 ja coberts per feat-019 (archivat) — DEFER.
- CAND-004 té overlap amb feat-019 però validació/quarantena no està clara — NEEDS_REVIEW.
- CAND-005 és diferent de feat-049 (enforcement) — defineix QUÈ és mutació, no COM s'enforsa. **Màxima prioritat dins cluster**.

---

## Cluster 2: Robustesa Operativa

Backpressure, crash recovery, quarantena — robustesa del runtime davant càrrega i fallades.

| CAND | Què aporta | Action | Duplicat? | Deps | Risc principal | Ordre (h) |
|------|-----------|--------|-----------|------|----------------|-----------|
| **CAND-009** | Crash recovery amb `kernel.state.json` + seqüència boot recovery. | **KEEP** | — | feat-019 | Compatibilitat arxius existents | NEXT |
| **CAND-010** | Load Balancer amb decisions Allow/Delay/Spool/Reject i llindars. | DEFER | feat-053 (ARCHIVED), feat-063 (ARCHIVED) | — | Impacte transversal | NEXT |
| **CAND-011** | Quarantena de tickets/engrams amb manifest.json i política recuperació. | **KEEP** | — | feat-019 | Filesystem bloat | NEXT |

**Notes cluster:**
- CAND-010 ja implementat (feat-053 + feat-063, arxivats) — DEFER.
- CAND-009 i CAND-011 són UNKNOWN al mining (Recovery Manager i Quarantine Manager no existeixen). **Prioritàries per robustesa**.

---

## Cluster 3: Seguretat / Autoritat / Modes

Zero Trust, rings, capacitats, i segregació de context.

| CAND | Què aporta | Action | Duplicat? | Deps | Risc principal | Ordre (h) |
|------|-----------|--------|-----------|------|----------------|-----------|
| **CAND-006** *(repetit)* | Modes de kernel + overlays SAFE_MODE/LOCKDOWN. | DEFER | feat-049, feat-012 | feat-012 | Drift doc vs API | NOW |
| **CAND-007** | Rings Architecture (Ring 0 bootstrap immutable, Ring 1 Guardian). | DEFER | — | — | Canvi de paradigma | NEXT |
| **CAND-008** | Zero tools per defecte + gating de capabilities a identity.md. | DEFER | — | feat-049 | Complexitat de permisos | NEXT |
| **CAND-013** | Context Segregation: agenticos_state només per IT/Sec + Auditor context especial. | **KEEP** | — | feat-008 | Complexitat permisos | NEXT |
| **CAND-018** | Regla "mai exposat a internet" + VPN com a canal operatiu. | DEFER | — | — | Operatiu | LATER |

**Notes cluster:**
- CAND-006 ja cobert (feat-049 arxivat) — DEFER.
- CAND-013 és drift-prone gap #1 del mining (format agenticos_state no especificat). **Prioritària**.

---

## Cluster 4: Memòria / Context / Engram / Skills / Prompts

*(Veure document separat: `memory_slice_2026-04-12.md` per anàlisi detallat)*

| CAND | Què aporta | Action | Duplicat? | Deps | Risc principal | Ordre (h) |
|------|-----------|--------|-----------|------|----------------|-----------|
| **CAND-012** | Context Builder: jerarquia multi-tier + budgets tokens/bytes (32KB/8KB). | NEEDS_REVIEW | feat-008 (SPEC DONE) | feat-008 | Complexitat truncament | NEXT |
| **CAND-013** *(repetit)* | Segregació IT/Sec del context global. | **KEEP** | — | feat-008 | Complexitat permisos | NEXT |
| **CAND-014** | Engram Format: `.engram.md` + JSON frontmatter + immutabilitat. | NEEDS_REVIEW | feat-003 (partial) | feat-003 | Migració corpus existent | LATER |
| **CAND-015** | Engram Index: SQLite FTS5 + WAL mode per cerca eficient. | NEEDS_REVIEW | feat-003 (partial) | feat-003 | Migracions schema | LATER |
| **CAND-016** | Librarian MCP Contract: memory_query/store amb timeout/fallback. | DEFER | — | feat-003, feat-008 | Drift de contracte | LATER |

**Notes cluster:**
- CAND-012, CAND-014, CAND-015 necessiten contrastar contra implementació real (feat-008, feat-003) — NEEDS_REVIEW.
- CAND-016 és contracte d'integració MCP — podria ser ADR en lloc de feature.

---

## Cluster 5: UI / Surfaces / Observabilitat

Dashboard, events, Telegram, i seguretat operacional.

| CAND | Què aporta | Action | Duplicat? | Deps | Risc principal | Ordre (h) |
|------|-----------|--------|-----------|------|----------------|-----------|
| **CAND-017** | Tool Registry data-driven amb discovery per rutes canòniques. | DEFER | — | — | Complexitat | LATER |
| **CAND-018** *(repetit)* | VPN-only exposure + regla no-internet. | DEFER | — | — | Operatiu | LATER |
| **CAND-019** | Event Contract amb schema, reconnect i backoff per dashboard. | NEEDS_REVIEW | feat-006 (partial) | feat-006 | Compatibilitat | LATER |
| **CAND-020** | Telegram Bridge: secrets fora de git + controls anti-abús. | DEFER | — | — | Operatiu | LATER |

**Notes cluster:**
- CAND-017 és extensibilitat, no estrictament UI — però afecta surfaces.
- CAND-019 té overlap amb feat-006 (Dashboard) — NEEDS_REVIEW.

---

## Top 5 Candidats per Discussió d'Arquitectura

*(No PKLot — només per debat intern)*

### 1. CAND-005 — System Mutation Contract + HITL Approval Primitive
**Per què:** És el gap més gran entre "tenim enforcement de modes" (feat-049) i "no sabem què és una mutació". La definició de system mutation és fonamental per governança. Sense aquest contracte, qualsevol canvi al sistema pot ser interpretat de formes inconsistents.

### 2. CAND-009 — Crash Recovery (kernel.state.json + Boot Recovery)
**Per què:** Robustesa crítica. El mining diu "UNKNOWN" per Recovery Manager. Sense crash recovery, un OOM o kill -9 trenca el sistema. Afecta tots els altres components (no pots construir sobre base inestable).

### 3. CAND-011 — Quarantine System (tickets/engrams manifest + recovery policy)
**Per què:** Seguretat operativa. Inputs corruptes contaminen tot el pipeline. Cal una política explícita de quarantena abans que el sistema processi dades no fiables en producció.

### 4. CAND-013 — Context Segregation (IT/Sec-only + Auditor context)
**Per què:** Drift-prone gap #1 del mining. El format d'`agenticos_state` no està especificat, i la segregació IT/Sec és Zero Trust real. Afecta totes les decisions de context futurament.

### 5. CAND-012 — Context Builder (multi-tier hierarchy + budgets)
**Per què:** Escalabilitat i determinisme. Sense pressupostos de tokens/bytes definits, el sistema és vulnerable a OOM. Cal definir jerarquia (Global→Dept→Agent→Tasca) abans que el context creixi incontroladament.

---

## Ordre Suggerit d'Implementació (Heurístic)

| Fase | Horizon | Candidates | Justificació |
|------|---------|------------|--------------|
| **NOW** | Immediat | CAND-005, CAND-006 | Contractes base de governança i seguretat. CAND-006 ja fet (DEFER). |
| **NEXT** | Curt termini | CAND-009, CAND-011, CAND-012, CAND-013, CAND-007, CAND-008 | Robustesa operativa + context + segregació. Fonamentals per estabilitat. |
| **LATER** | Mig/llarg termini | CAND-014, CAND-015, CAND-016, CAND-017, CAND-018, CAND-019, CAND-020 | Optimitzacions, UI, i integracions. Depenen dels NOW/NEXT. |

*(h) = heurístic, no autoritat. L'ordre real es decidirà al triage batch.*

---

## No Apply Confirmation

```
✅ No s'ha editat 00_project_documentation/04_PARKING_LOT.md
✅ No s'han creat fitxers SEED-*.md a seed_dossiers/
✅ No s'han creat feat-*.json nous
✅ Tots els proposed_seed_id = TBD (no assignats)
✅ Tots els horizon porten "(h)" = heurístic, no autoritat

Aquest document és proposta per a debat d'arquitectura.
Qualsevol aplicació al PKLot depèn d'un triage batch signat pel responsable.
```
