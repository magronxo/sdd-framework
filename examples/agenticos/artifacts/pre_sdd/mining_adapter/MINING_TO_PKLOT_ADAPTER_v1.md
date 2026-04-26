# Mining → PKLot Adapter v1

> Data: 2026-04-12  
> Font: corpus `design_mining_2026-04-09/*.mining.md` (19 fitxers)  
> Regla hard: **NO APPLY** — fase estrictament de proposta i registre, mai d'execució.

---

## A. Principis (Hard Rules)

1. **Mining docs = inputs/audit, NO backlog**  
   El mining documenta i proposa; no és font de veritat operativa.

2. **Seed candidate = proposta, revisable**  
   Qualsevol candidate'extreta del mining és una hipòtesi, no un commitment.

3. **NO APPLY (fase actual)**  
   Està absolutament prohibit executar res a PKLot o crear dossiers reals:
   - ❌ Editar `00_project_documentation/04_PARKING_LOT.md`
   - ❌ Crear fitxers `SEED-*.md` a `seed_dossiers/`
   - ❌ Crear `feat-*.json` nous
   - ❌ Executar SDD

4. **No assignar SEED-XX en aquesta fase**  
   `proposed_seed_id = TBD` sempre. L'assignació real és tasca del triage batch (futur).

---

## B. Inputs vàlids

### Corpus de referència

```
00_project_documentation/SDD/audit_reports/design_mining_2026-04-09/
```

| Fitxer | Rol |
|--------|-----|
| `00_SEED_INDEX.mining.md` | Índex canònic de totes les candidates detectades |
| `00_SUMMARY.mining.md` | Top seeds + drift-prone gaps |
| `00_CONTRAST_SDD.mining.md` | Contrast contra autoritats SDD/ADR |
| `00_ROADMAP.mining.md` | Redirect cap al roadmap canònic |
| `01_KERNEL.mining.md` | Anàlisi Kernel |
| `02_TICKET_SYSTEM.mining.md` | Anàlisi sistema de tickets |
| `03_FILESYSTEM_AND_DEPARTMENTS.mining.md` | Anàlisi filesystem |
| `04_SEED_AND_AGENT_ANATOMY.mining.md` | Anàlisi anatomia d'agents |
| `05_GUARDIAN.mining.md` | Anàlisi Guardian |
| `06_ORCHESTRATION_AND_ROLES.mining.md` | Anàlisi orquestació |
| `07_ENGRAM.mining.md` | Anàlisi memòria |
| `08_CONTEXT_BUILDER.mining.md` | Anàlisi context builder |
| `09_EXTENSIBILITY.mining.md` | Anàlisi extensibilitat |
| `10_OBSERVABILITY.mining.md` | Anàlisi observabilitat |
| `11_DASHBOARD_IDE.mining.md` | Anàlisi dashboard |
| `12_TELEGRAM_BRIDGE.mining.md` | Anàlisi bridge Telegram |
| `13_SECURITY_MODEL.mining.md` | Anàlisi model de seguretat |
| `14_MULTISEED_future.mining.md` | Anàlisi multi-seed |
| `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md` | Anàlisi transicions ticket |

**No usar:** fitxers `*.md.mining.md` (DRAFT/Gemini, no autoritatiu) ni `01_design/*.md` (legacy, no contracte).

### Tractament d'ambigüitats

Si un doc falta o és ambigu:
- `source_doc` → path real o `unknown`
- `source_anchor` → `unknown`
- Tots els camps pendents → `unknown`
- `recommended_action` → `NEEDS_REVIEW`

---

## C. Output Schema — Seed Candidate v1

Cada entrada del mining es tradueix a un **candidate** amb l'estructura següent:

```yaml
candidate_id: CAND-{NNN}        # ID intern seqüencial (CAND-001, CAND-002…)
title: "{curt, ≤ 10 paraules}"
source_doc: "{fitxer.mining.md}"
source_anchor: "{heading|section|line hint}"  # si es pot identificar
priority: P0 | P1 | P2 | P3     # preservat tal qual del mining
horizon: NOW | NEXT | LATER | null  # OPCIONAL — heurística, NO autoritat
trigger: drift_gap | design_gap | security_gap | unknown
problem: "{1-3 frases}"
intent: "{outcome, no solució}"
scope_hypothesis_in:
  - "{item}"
scope_hypothesis_out:
  - "{item}"
risks:
  - risk: "{descripció}"
    severity: High | Medium | Low
    mitigation: "{com es redueix}"
success_signals:
  - "{observable}"
exploration_required: true | false
exploration_reason: "{raó si true}"
possible_duplicate_of:
  - "{SEED-* | feat-* | ADR-*}"  # zero o més referències
evidence_refs:
  - "{path a artefacte real}"    # specs, ADR, features_for_specs, etc.
confidence: low | med | high
recommended_action: KEEP | DEFER | CONVERT_LATER | NEEDS_REVIEW
```

---

## D. Regles de Dedupe

### Regla 1 — Dedupe contra feat-XXX existent

Si existeix evidència d'un `feat-XXX` amb `state: ARCHIVE` o `state: DESIGN/SPEC/TASKS`:

```
possible_duplicate_of: ["feat-{NNN}"]
recommended_action: DEFER | DISCARD
evidence_refs: ["path/feat-{NNN}.json"]
```

### Regla 2 — Dedupe contra ADR existent

Si existeix una ADR que cobreix el concepte:

```
possible_duplicate_of: ["ADR-{NNN}"]
recommended_action: DEFER | DISCARD
evidence_refs: ["path/05_ADR_DECISION_LOG.md"]
```

### Regla 3 — Dedupe contra SEED existent

Si ja existeix un dossier real a `seed_dossiers/`:

```
possible_duplicate_of: ["SEED-{NN}"]
recommended_action: DEFER
evidence_refs: ["seed_dossiers/SEED-{NN}.md"]
```

### Regla 4 — Overlap parcial

Si hi ha col·lisió parcial però no total:

```
possible_duplicate_of: ["feat-{NNN}"]
recommended_action: NEEDS_REVIEW
evidence_refs: ["path/feat-{NNN}.json"]
```

### Regla 5 — No afirmar sense evidència

Mai assertar "duplicate_of X" sense un `evidence_refs` real.  
Si no es troba evidència però se sospeta col·lisió:

```
possible_duplicate_of: ["TBD"]  # marca que cal verificar manualment
recommended_action: NEEDS_REVIEW
```

---

## E. Mapping heurístic P0/P1 → horizon

### Regla de mapping (NO autoritat — heurística)

| Priority | Horizon per defecte | Excepcions |
|----------|---------------------|-----------|
| P0 | NOW | Quan la implementació ja existeix i no calnou feature |
| P1 | NEXT | Quan l'scoping és clar i no hi ha unknowns |
| P2 | LATER | Quan cal explorar abans |
| P3 | LATER | Sempre — "reserve now" |

**Important:** Aquest mapping és orientatiu. El `horizon` final s'assigna al triage real, no aquí.

El camp `horizon` a la candidate és **opcional i marcat explícitament com a heurística** derivata del mining.

---

## F. Pas futur — Apply (OUT OF SCOPE ara)

Aquest adapter descriu només la fase de proposta (dry-run). El pas d'apply (futur) seria:

1. Assignar IDs `SEED-XX` a les candidates amb `recommended_action: KEEP`
2. Crear el dossier `SEED-{NN}.md` a `seed_dossiers/`
3. Omplir camps reals del dossier (problem, intent, scope, capabilities, etc.)
4. Actualitzar PKLot (fitxer `04_PARKING_LOT.md`)
5. Crear entrada al triage batch per a la propera sessió

**Aquest pas NO està inclòs a la fase actual. És OUT OF SCOPE.**

---

## G. Output del adapter

L'output d'aquest adapter és:

```
mining_adapter/MINING_TO_PKLOT_ADAPTER_v1.md    ← Protocol (aquest fitxer)
mining_adapter/dryrun_extract_{YYYY-MM-DD}.md  ← Dry run d'avui
```

Cada dry run és un **snapshot autònom** (no es sobreescriu l'anterior). Tots porten data al nom per traçabilitat.

---

## H. Convencions finals

| Element | Format |
|---------|--------|
| ID intern de candidate | `CAND-{NNN}` (seqüencial) |
| Proposta SEED (NO aplicar ara) | `TBD` |
| Dossier real (NO crear) | `SEED-{NN}.md` sota `seed_dossiers/` |
| Feature record (NO crear) | `feat-{NNN}.json` sota `features_for_specs/` |

Tota criatura de noms és provisional i subjecte a revisió al triage real.
