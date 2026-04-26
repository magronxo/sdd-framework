# PRE-SDD Prompt — Batch scan (Classify + Short analysis + Select candidates)

Goal: scan the Parking Lot seeds and propose a bounded batch for triage.

Rules:

- Do not create feats, ADRs, or specs in this step.
- Keep outputs short and deterministic.
- Respect WIP limits (selected: 1–3; NOW target: ≤ 5–10).

Input:

- `00_project_documentation/04_PARKING_LOT.md` (seed section)

Output:

1) Proposed `Horizon` for seeds that are ambiguous or overloaded
2) Short analysis for NOW candidates (problem/overlaps/maturity/recommendation)
3) A proposed `Selected` list (1–3 seeds) for the next batch report
4) Notes on duplicates/merges between seeds (if any)

