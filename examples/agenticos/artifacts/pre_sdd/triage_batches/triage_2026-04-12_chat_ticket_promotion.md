# TRIAGE BATCH — triage_2026-04-12_chat_ticket_promotion

> Date: 2026-04-12
> Scope: seeds SEED-09
> WIP limit selected: 1
> Triage lead: sdd-propose agent

---

## 1) Scan

Parking Lot source:

- `00_project_documentation/04_PARKING_LOT.md`

Scanned seed IDs:

- SEED-09 (new — Chat → Ticket Promotion Contract)

---

## 2) Selected (this batch)

- **SEED-09** — Chat → Ticket Promotion Contract

---

## 3) Per-seed analysis and contract

### SEED-09 — Chat → Ticket Promotion Contract

**Short analysis**

- problem: El sistema no té manera determinista de distingir resposta immediata vs creacio de ticket en chat
- overlaps: cap duplicacio amb feat-XXX existent
- maturity: dossier v1 complet amb 8 capabilities testables
- recommendation: triage ara / explorar primero / diferir

**TRIAGE (minimal contract)**

- problem: Necessitem un contracte on `requested_mode` determini si chat retorna 200 (resposta directa) o 201/202 (ticket creat)
- objective: Unificar l'entrada de chat amb un camp `requested_mode` que faci el comportament predictable
- scope (candidates to spec — SDD):
  - Camp `requested_mode` a `POST /api/v1/llm/chat` (`interactive | ticketed | auto`)
  - 200 per resposta immediata (`interactive`)
  - 201/202 + `{ticket_id}` per resposta amb ticket creat (`ticketed` o `auto` fallback)
  - Errors deterministes (400 invalid mode, 403 mode/overlay denied, 429 backpressure)
  - Revalidacio en temps real quan mode canvia durant execucio
- non-scope:
  - HITL complet
  - ACLs complexos
  - Implementacio ReAct
  - Persistencia mes enlla del contracte
- impact:
  - Kernel i workflow: permet predictibilitat en chat
  - UI passiva: pot mostrar estat de ticket despres
- risks:
  - Risc baix: extensio backward-compatible de handlers existents
  - Risc mitja: fallback `auto` es conservador
- success_signal:
  - 200 per interactive, 201/202 per ticketed
  - 400/403/429 per errors deterministes
  - Revalidacio en temps real funciona

**EXPLORATION GATE**

- exploration_required: `false` — reason: contracte simple, extensions de handlers existents

**DECOMPOSE**

- decision: 1 feature
- proposed features:
  - `feat-070` — Chat Ticket Promotion Contract (depends on feat-049, feat-051, feat-052/053, feat-055, feat-058)

**HANDOFF (created paths)**

- seed_dossier: `00_project_documentation/SDD/artifacts/pre_sdd/seed_dossiers/SEED-09.md`
- feature_records_created: pending SDD execution
- design_artifacts_created: pending SDD execution
- notes: output PRE-SDD complet — seed dossier v1 + triage batch entry + feature proposal ready

---

## 4) Deferred (this batch)

(none)

---

## 5) Discarded / Archived

(none)

---

## 6) Batch decision summary

```yaml
adopted: [SEED-09]
adapted: []
deferred: []
discarded: []
```

---

## 7) Next triage

- Scheduled: TBD
- Parking Lot scan due: 2026-04-19
- Open items to resolve before next batch:
  - [x] SEED-09 → SDD execution COMPLETED (feat-070 archived)
