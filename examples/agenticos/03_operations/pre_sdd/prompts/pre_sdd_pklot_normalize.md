# PRE-SDD Prompt — PKLot normalization (ordering + promotions + report)

Goal: normalize `00_project_documentation/04_PARKING_LOT.md` so PRE-SDD triage remains deterministic and the Parking Lot stays readable, and produce a persistent normalization report draft.

Hard rules (invariants):

- `SEED-*` IDs appear only in **SEEDS (PRE-SDD)**.
- Near-term backlog contains no `SEED-*`.
- Seeds use PRE-SDD fields: `Horizon`, `Estat (PRE-SDD)`, `Batch ref`.
- Non-seed backlog items keep the existing task schema (`⬜/✅/📋`) and do NOT add seed fields.
- Deployment notes live under **Deployments** and are not labeled as seeds.
- A missing `SEED-06` is NOT automatically a violation if it was intentionally renamed into a non-seed backlog ID (e.g. `DEP-01`) per `feat-024`.

Promotion rules:

- `ADR`: stable decisions (architecture/criteria) that should not live in PKLot.
- `CD`: stable + implemented/consolidated decisions (Completed Decisions) that should not live in PKLot.
- `VOLATILE/KEEP`: dated snapshots and frequently-changing facts (e.g., provider/model availability). These must NOT be promoted to ADR/CD by default.

Status rule (avoid false-completions):

- Do not mark a parent backlog item as `✅ Fet` if it still has pending sub-items. Prefer adding a short ADR/CD link (e.g. “baseline completed”) and keep the parent as `📋 Dissenyat` or `⬜ Pendent` as appropriate.

Input:

- `00_project_documentation/04_PARKING_LOT.md`

Output (strict format):

1) **Proposed PKLot INDEX block** (paste-ready)
2) **Violations found** (max 10 bullets)
3) **Promotion candidates** (table: `candidate`, `type` = ADR/CD/VOLATILE/KEEP, `rationale`, `already_in_adr_log?`)
   - Dedup rule: before proposing a new CD, search `00_project_documentation/05_ADR_DECISION_LOG.md` for the relevant ID/keyword.
4) **Proposed physical reordering plan**
   - moves/renames/splits to make PKLot match the required section order and invariants
5) **Normalization report draft** (ready to save as)
   - `00_project_documentation/SDD/artifacts/pre_sdd/pklot_normalization/normalize_YYYY-MM-DD.md`
   - Use `00_project_documentation/SDD/artifacts/pre_sdd/pklot_normalization/normalize_template.md` structure.
6) **Apply mode note**
   - Default: proposal/report only.
   - Apply physical edits only when explicitly requested.

Rules:

- Do not create SDD features, ADRs, specs, or tasks.
- Do not rewrite large text blocks; prefer surgical moves and field completion.
- If something is ambiguous (seed vs task), recommend a rename to a non-seed ID and explain the reasoning.
