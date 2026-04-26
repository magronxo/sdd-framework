# PRE-SDD Prompt — Selected → TRIAGE + DECOMPOSE + HANDOFF plan

Goal: for 1 selected seed, produce the minimal contract and decomposition needed to create SDD features in `DESIGN`.

Rules:

- Do not write specs or tasks.
- If the idea is still immature, recommend reverting it back to `Analyzed` with concrete missing inputs.
- Handoff must be explicit and list the exact paths to create (feature record + design artifact).

Input:

- One selected seed (SEED-XX) content from `00_project_documentation/04_PARKING_LOT.md`

Output:

1) TRIAGE (minimal contract): problem/objective/scope/non-scope/impact/risks/success signal
2) DECOMPOSE: 1 feature vs N features; boundaries + dependencies + order
3) HANDOFF plan: list exact paths to create:
   - `00_project_documentation/SDD/artifacts/features_for_specs/feat-XXX-<slug>.json`
   - `00_project_documentation/SDD/artifacts/design/feat-XXX-<slug>.md`
4) Parking Lot updates to apply after creation:
   - set `Batch ref`
   - set `Estat (PRE-SDD)` to `Converted`

