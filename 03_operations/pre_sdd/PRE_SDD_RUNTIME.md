# Pre-SDD Runtime

> **Mode Diátaxis**: Reference

## Purpose

Operational workflow for Pre-SDD. Pre-SDD activities and labels are domain-local; they occur before the Canonical v1 persistent feature lifecycle.

## Phase Overview

```text
CAPTURE -> CLASSIFY -> TRIAGE -> PRIORITIZE -> REFINE -> TRANSITION -> ARCHIVE
```

## Phase 1: Capture

**Procedure**:

1. Create a seed dossier from `docs/sdd/03_operations/pre_sdd/templates/seed_dossier.md`.
2. Name it `docs/sdd/03_operations/pre_sdd/seeds/{YYYY-MM-DD}_{type}_{short_description}.md`.
3. Fill provenance, description, context, impact, urgency, and type.
4. Do not write solutions or implementation details.

**Gate**: Provenance, description, and impact must exist; otherwise stop for more information.

## Phase 2: Classify

Apply and record these dimensions in the seed dossier:

- Type: `idea | bug | feedback | debt | spike | risk`
- Scope: `frontend | backend | infra | docs | process | cross-cutting`
- Urgency: `critical | high | medium | low`
- Effort: `trivial | small | medium | large | unknown`
- Confidence: `certain | likely | unclear | speculative`

**Gate**: Every dimension has a value. Use `unknown` or `unclear` where necessary.

## Phase 3: Triage

1. Use `docs/sdd/03_operations/pre_sdd/templates/triage_batch.md` for batch review when useful.
2. Check understanding, impact, project scope, available resources, and duplicates.
3. Record `PROMOTE | DEFER | REJECT | MERGE | SPIKE` plus rationale in the dossier.
4. Record a review date for deferred seeds.

These decisions are Pre-SDD labels, not feature-record states.

## Phase 4: Prioritize

Sequence promoted seeds using urgency, dependencies, strategic alignment, and effort versus impact. Record priority in the promoted-seed dossier or domain-local queue, not in the closed-schema feature record.

## Phase 5: Refine

1. Clarify ambiguities while preserving the problem rather than prescribing a solution.
2. Confirm boundaries and rough size.
3. Consult `docs/sdd/02_policies/DECOMPOSITION_AND_SIZE_POLICY.md`.
4. Split oversized concerns into seeds before transition.

**Gate**: The seed has clear boundaries and appropriate size.

## Phase 6: Transition to Canonical SDD

1. Allocate a canonical ID such as `feat-123-short-name`.
2. Create `docs/sdd/artifacts/features_for_specs/{feature_id}.json` as a complete Canonical v1 record.
3. Use only fields declared by `docs/sdd/contract/v1/feature-record.schema.json`.
4. Set the initial persistent state to `DESIGN`.
5. Record the created feature ID and repository-relative record link in the seed dossier's `Linked to` field.
6. Preserve useful source context in the promoted dossier and, where appropriate, cite it in the human-readable design context.
7. Move the dossier to `docs/sdd/03_operations/pre_sdd/seeds/promoted/`; do not delete it.

**Minimal complete feature record example:**

```json
{
  "id": "feat-123-short-name",
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",
  "title": "Short feature title",
  "created_at": "2026-08-01T00:00:00Z",
  "updated_at": "2026-08-01T00:00:00Z"
}
```

**Gate**: The record is valid under canonical write mode, and the promoted seed dossier links to the feature. Provenance remains in the dossier; no private provenance field is added to the feature record.

## Phase 7: Archive Seed Material

Move the dossier to the appropriate installed path:

- `docs/sdd/03_operations/pre_sdd/seeds/promoted/`
- `docs/sdd/03_operations/pre_sdd/seeds/deferred/`
- `docs/sdd/03_operations/pre_sdd/seeds/rejected/`
- `docs/sdd/03_operations/pre_sdd/seeds/merged/`

Preserve rationale and cross-references.

## Boundary with the Persistent Lifecycle

Pre-SDD terminates when a valid DESIGN feature record is created. The persistent lifecycle then begins:

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

Pre-SDD labels do not extend or replace this lifecycle.

## Roles

| Role | Pre-SDD responsibility |
|---|---|
| Reporter | Captures seeds with provenance and context. |
| Triage Owner | Classifies, triages, and archives seed dossiers. |
| Product Owner | Prioritizes and validates impact. |
| Tech Lead | Validates feasibility and decomposition. |
| Designer | Receives the valid DESIGN record and promoted context. |

## Anti-Patterns

- solutioneering in seeds;
- skipping classification;
- promoting without refinement;
- deleting rejected or promoted seed evidence;
- adding Pre-SDD metadata to the closed-schema feature record;
- treating Pre-SDD labels as persistent SDD states.

## Related Documents

- `docs/sdd/03_operations/pre_sdd/PRE_SDD_CONTRACT.md`
- `docs/sdd/03_operations/pre_sdd/templates/seed_dossier.md`
- `docs/sdd/03_operations/pre_sdd/templates/triage_batch.md`
- `docs/sdd/04_project_governance/PROJECT_MANIFEST.md`
- `docs/sdd/02_policies/DECOMPOSITION_AND_SIZE_POLICY.md`
