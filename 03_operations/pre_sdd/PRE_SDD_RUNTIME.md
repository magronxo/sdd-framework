# Pre-SDD Runtime

> **Mode Diátaxis**: Reference

## Purpose

Operational workflow for the **Pre-SDD phase**.

This document reduces the `PRE_SDD_CONTRACT.md` to an executable procedure.

---

## Phase Overview

```
CAPTURE (1) → CLASSIFY (2) → TRIAGE (3) → PRIORITIZE (4) → REFINE (5) → TRANSITION (6) → ARCHIVE (7)
```

---

## Phase 1: Capture

**Trigger**: A new idea, bug, feedback item, or risk is observed.

**Input**: Raw observation (Slack, email, meeting note, user report, monitoring alert).

**Procedure**:
1. Create a seed dossier from `templates/seed_dossier.md`
2. Name it: `seeds/{YYYY-MM-DD}_{type}_{short_description}.md`
3. Fill all required fields (provenance, description, context, impact, urgency, type)
4. Do NOT write solutions or implementation details
5. Save to `03_operations/pre_sdd/seeds/`

**Output**: A seed dossier file.

**Gate**: Must have provenance + description + impact. Otherwise, STOP and request more info.

---

## Phase 2: Classify

**Trigger**: A seed dossier exists and awaits classification.

**Input**: Seed dossier.

**Procedure**:
1. Read the seed dossier
2. Apply classification dimensions:
   - Type: `idea | bug | feedback | debt | spike | risk`
   - Scope: `frontend | backend | infra | docs | process | cross-cutting`
   - Urgency: `critical | high | medium | low`
   - Effort: `trivial | small | medium | large | unknown`
   - Confidence: `certain | likely | unclear | speculative`
3. Update the dossier with classification block
4. Save

**Output**: Classified seed dossier.

**Gate**: All 5 dimensions must have a value. Use `unknown` or `unclear` if necessary, but never leave blank.

---

## Phase 3: Triage

**Trigger**: Seeds are classified and ready for decision.

**Input**: One or more classified seed dossiers.

**Procedure**:
1. Gather seeds for review (use `templates/triage_batch.md` for batches)
2. For each seed, evaluate against triage criteria:
   - Well-understood?
   - Impact-validated?
   - Scope-appropriate? (check `PROJECT_MANIFEST.md` non-goals)
   - Resources-available?
   - Not-duplicate? (search existing seeds and features)
3. Record decision: `PROMOTE | DEFER | REJECT | MERGE | SPIKE`
4. Record rationale
5. If REJECT or DEFER, set review date

**Output**: Triage decision recorded in dossier or batch file.

**Gate**: Every seed must have a recorded decision with rationale.

---

## Phase 4: Prioritize

**Trigger**: Seeds have been promoted from triage.

**Input**: List of promoted seeds.

**Procedure**:
1. Assign priority relative to other pending features
2. Consider:
   - Urgency (user-facing vs internal)
   - Dependencies (what blocks what)
   - Strategic alignment (`PROJECT_MANIFEST.md`)
   - Effort vs impact
3. Sequence promoted seeds into a proposed order
4. Record priority in feature record (when created)

**Output**: Prioritized queue of seeds ready to become features.

---

## Phase 5: Refine

**Trigger**: A promoted seed is next in the priority queue.

**Input**: Promoted seed dossier.

**Procedure**:
1. Review the seed with Designer and Tech Lead
2. Clarify ambiguities
3. Confirm the problem (not the solution)
4. Identify boundaries (what is in/out of scope)
5. Estimate rough size (check `DECOMPOSITION_AND_SIZE_POLICY.md`)
6. If too large, split into multiple seeds before promotion

**Output**: Refined seed ready for feature record creation.

**Gate**: Must have clear boundaries and appropriate size.

---

## Phase 6: Transition

**Trigger**: A refined seed is approved to enter SDD.

**Input**: Refined seed dossier.

**Procedure**:
1. Create a feature record in `artifacts/features_for_specs/{feature_id}.json`
2. Feature ID format: `feat-{NNN}-{short-name}`
3. Copy seed provenance and context into feature record
4. Set initial state: `DESIGN`
5. Link back to seed dossier for traceability
6. Move seed dossier to `seeds/promoted/` (do not delete)

**Output**: Feature record + promoted seed archived.

**Gate**: Feature record must contain `seed_reference` linking back to original dossier.

---

## Phase 7: Archive

**Trigger**: A seed reaches a terminal state (rejected, deferred, merged, or promoted).

**Input**: Seed dossier with final decision.

**Procedure**:
1. Move dossier to appropriate subdirectory:
   - `seeds/promoted/` — entered SDD
   - `seeds/deferred/` — postponed with review date
   - `seeds/rejected/` — permanently closed
   - `seeds/merged/` — consolidated into another seed/feature
2. Ensure all decisions have rationale
3. Ensure cross-references are valid

**Output**: Organized archive of seed history.

---

## State Machine

```
          +-----------+
          |  CAPTURED |
          +-----+-----+
                |
                v
          +-----------+
          | CLASSIFIED|
          +-----+-----+
                |
                v
          +-----------+
          |  TRIAGED  |----------> DEFERRED
          +-----+-----+            (review later)
                |
    +-----------+-----------+
    |           |           |
    v           v           v
 PROMOTED    REJECTED    MERGED
    |                       |
    v                       v
  REFINED               (into other)
    |
    v
 TRANSITIONED
    |
    v
  SDD PIPELINE
```

---

## Roles

| Role | Phase | Authority |
|------|-------|-----------|
| **Reporter** | Capture | Creates seeds, cannot classify or triage own seeds alone |
| **Triage Owner** | Classify, Triage, Archive | Makes go/no-go decisions |
| **Product Owner** | Prioritize, Refine | Validates business impact and sequencing |
| **Tech Lead** | Refine | Validates technical feasibility and decomposition |
| **Designer** | Refine, Transition | Prepares seed for DESIGN phase |

---

## Anti-Patterns

- **Solutioneering in seeds** — capturing "use Redis" instead of "sessions are too slow"
- **Skipping classification** — triaging without dimensions leads to inconsistent decisions
- **Promoting without refinement** — sending unclear seeds to DESIGN wastes designer time
- **Deleting rejected seeds** — keep them for traceability and to prevent re-submission
- **Batch-promoting everything** — triage exists to say NO

---

## Related Documents

- `03_operations/pre_sdd/PRE_SDD_CONTRACT.md` — rules and definitions
- `03_operations/pre_sdd/templates/seed_dossier.md` — seed template
- `03_operations/pre_sdd/templates/triage_batch.md` — batch review template
- `04_project_governance/PROJECT_MANIFEST.md` — non-goals and constraints
- `02_policies/DECOMPOSITION_AND_SIZE_POLICY.md` — sizing and splitting rules
