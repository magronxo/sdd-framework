# PRE-SDD Runtime (Parking Lot Intake / Triage)

Purpose: provide a deterministic pre-flow that turns seeds into SDD-ready work without inflating premature specs.

PRE-SDD sits **before** the canonical SDD pipeline and does not add SDD states.

Canonical SDD pipeline:

`DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE`

---

## Inputs

- `00_project_documentation/04_PARKING_LOT.md` (seeds only: `SEED-XX`)

## Outputs

- Batch triage reports:
  - `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_YYYY-MM-DD.md`
- Handoff results:
  - ADR (decision-only), and/or
  - SDD feature records in `DESIGN` (+ design artifact), ready to enter SDD.

---

## Hard rules

- Seeds are capture-light. Do not write specs inside the Parking Lot.
- Each triage batch must have an explicit WIP limit:
  - `Selected` seeds per batch: 1–3
  - `NOW` horizon target: ≤ 5–10 seeds
- No “handoff” unless the batch report includes TRIAGE + DECOMPOSE + explicit created paths.

---

## Phases (contract)

1) **CAPTURE**
   - Create/update seed entry in the Parking Lot with minimal fields.

2) **CLASSIFY**
   - Assign `Horizon: NOW | NEXT | LATER`.
   - Set `Estat (PRE-SDD): Classified`.

3) **SHORT_ANALYSIS** (NOW only)
   - Problem (1 line)
   - Duplicates/overlaps (links)
   - Maturity missing pieces
   - Recommendation (keep/move/arch)

4) **SELECT**
   - Choose 1–3 seeds for this batch.
   - Record in the batch report scope.

5) **TRIAGE (minimal contract)**
   - Problem, Objective, Scope, Non-scope, Impact, Risks, Success signal.

6) **DECOMPOSE**
   - Decide: 1 feature vs N features.
   - Define boundaries + dependencies + order.

7) **HANDOFF**
   - If decision-only: create/update ADR and mark seed `Converted` with ADR reference.
   - If behavior/contract change: create new `feat-XXX` feature records in `DESIGN` plus design artifacts.
   - Update the seed with `Batch ref` and set `Converted` only once handoff paths exist.

---

## Agent operating guidance

- Produce a triage batch report draft first.
- Human approves:
  - selected seeds
  - decomposition plan
  - which feats to create
- Only after approval: create `feat-XXX` records and design docs.

This keeps external input (including `gentle-ai`) advisory and preserves local governance.

