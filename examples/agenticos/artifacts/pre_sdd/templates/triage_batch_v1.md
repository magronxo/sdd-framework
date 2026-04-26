# PRE-SDD Triage Batch — triage_{YYYY-MM-DD}

> Replace `{YYYY-MM-DD}` with the date of the triage session.

---

## Metadata

```yaml
date: {YYYY-MM-DD}
scope: seeds {SEED-NN} and {SEED-MM} selected for handoff
wip_limit_selected: {N}  # max seeds to adopt this batch
triage_lead: {name or agent identifier}
```

## 1) Scan

Parking Lot source:

- `{path to PKLot file}`

Scanned seed IDs:

- {SEED-01}, {SEED-02}, {SEED-03}
- ({SEED-04} already {Converted/Discarded} — excluded)

## 2) Selected (this batch)

- **{SEED-NN}** — {Short one-liner title}
- **{SEED-MM}** — {Short one-liner title}

## 3) Per-seed analysis and contract

### SEED-{NN} — {Title}

**Short analysis**

- problem: {one-liner from dossier}
- overlaps: {any overlap with existing features}
- maturity: {how concrete/detailed the dossier is}
- recommendation: {triar ara / explorar primero / diferir}

**TRIAGE (minimal contract)**

- problem: {what we're solving}
- objective: {desired outcome}
- scope (candidates to spec — SDD):
  - {item 1}
  - {item 2}
- non-scope:
  - {item 1}
- impact:
  - {who benefits and how}
- risks:
  - {risk 1}
  - {risk 2}
- success_signal:
  - {observable outcome 1}
  - {observable outcome 2}

**EXPLORATION GATE** (if applicable)

- exploration_required: `true` — reason: {estimation >2 days / ≥2 unknowns / affects kernel}
- unknowns identified:
  1. {Unknown 1}
  2. {Unknown 2}
- hypotheses:
  1. {Hypothesis 1}
  2. {Hypothesis 2}
- status: `Passed` / `In Progress`

**DECOMPOSE**

- decision: {1 feature / N features}
- proposed features:
  - `{feat-XXX}` — {brief description} (depends on {dep})
  - `{feat-YYY}` — {brief description}
- dependencies/order:
  1. `{feat-000}` (exists/new): {what it provides}
  2. `{feat-XXX}` (new): {what it provides}

**HANDOFF (created paths)**

- feature_records_created:
  - `{path/to/feat-XXX.json}`
- design_artifacts_created:
  - `{path/to/design.md}`
- adr_created:
  - `{path/to/ADR-NNNN.md}`
- notes: {any additional handoff notes}

---

### SEED-{MM} — {Title}

(same structure as above for each selected seed)

## 4) Deferred (this batch)

- **{SEED-YY}** — {reason: needs exploration / out of scope / depends on X}
- **{SEED-ZZ}** — {reason}

## 5) Discarded / Archived

- **{SEED-WW}** — {reason: duplicate / infeasible / out of scope}

## 6) Batch decision summary

```yaml
adopted: [SEED-01, SEED-02]
adapted: []
deferred: [SEED-03]
discarded: []
```

## 7) Next triage

- Scheduled: {next triage date or "TBD"}
- Parking Lot scan due: {date}
- Open items to resolve before next batch:
  - [ ] {item 1}
  - [ ] {item 2}