# Pre-SDD Contract

> **Mode Diátaxis**: Reference

## Purpose

Define how **raw inputs** (ideas, bugs, feedback, technical debt) are captured, classified, and triaged **before** they enter the SDD pipeline.

This contract prevents:
- Premature specs (seeds that are not yet understood)
- Scope creep (unvetted ideas entering the pipeline)
- Lost context (feedback without provenance)

---

## What is a Seed?

A **seed** is any raw input that *might* become an SDD feature. It is **not** a feature yet.

### Valid Seed Types

| Type | Description | Example |
|------|-------------|---------|
| `idea` | New capability or enhancement | "Add dark mode" |
| `bug` | Something that does not work as spec'd | "Login fails on Safari" |
| `feedback` | User or stakeholder observation | "Users find the form confusing" |
| `debt` | Technical improvement without user-facing change | "Refactor auth middleware" |
| `spike` | Time-boxed research or exploration | "Evaluate SQLite vs PostgreSQL" |
| `risk` | Potential future problem | "Current rate limiter won't scale to 10k RPS" |

### What is NOT a Seed

- A task (tasks come from validated specs)
- A design document (designs come from approved features)
- A random thought without context (must have provenance)

---

## Capture Rules

### Where to Capture

All seeds live in `docs/sdd/03_operations/pre_sdd/seeds/` as individual dossiers.

File naming: `docs/sdd/03_operations/pre_sdd/seeds/{YYYY-MM-DD}_{type}_{short_description}.md`

Examples:
- `docs/sdd/03_operations/pre_sdd/seeds/2026-04-23_idea_dark_mode.md`
- `docs/sdd/03_operations/pre_sdd/seeds/2026-04-23_bug_safari_login.md`

### What to Capture

Every seed dossier **must** contain (use `docs/sdd/03_operations/pre_sdd/templates/seed_dossier.md`):

1. **Provenance** — Who reported it? Under what circumstances?
2. **Description** — What is the observation or request?
3. **Context** — Why does it matter now?
4. **Impact** — Who is affected and how?
5. **Urgency** — Is there a deadline or burning need?
6. **Type** — One of the valid types above

### What NOT to Capture

- Solutions ("We should use Redis") — capture the problem, not the fix
- Implementation details — those belong in the spec phase
- Unrelated feature bundles — one concern per seed

---

## Classification

After capture, each seed receives a **classification**:

| Dimension | Options | Description |
|-----------|---------|-------------|
| **Type** | `idea`, `bug`, `feedback`, `debt`, `spike`, `risk` | From capture |
| **Scope** | `frontend`, `backend`, `infra`, `docs`, `process`, `cross-cutting` | Which surface is affected |
| **Urgency** | `critical`, `high`, `medium`, `low` | Time sensitivity |
| **Effort** | `trivial`, `small`, `medium`, `large`, `unknown` | Rough size estimate |
| **Confidence** | `certain`, `likely`, `unclear`, `speculative` | How well understood is the need |

Classification is **best-effort** and may change during triage.

---

## Triage Criteria

A seed is promoted to a feature when it passes **all** of the following:

1. **Well-understood** — The problem (not the solution) is clearly described
2. **Impact-validated** — We know who is affected and why it matters
3. **Scope-appropriate** — It fits within the project's non-goals (see `docs/sdd/04_project_governance/PROJECT_MANIFEST.md`)
4. **Resources-available** — We have capacity to design and implement it
5. **Not-duplicate** — It does not duplicate an existing seed or feature

### Triage Decisions

| Decision | Next State | Action |
|----------|-----------|--------|
| **Promote** | Becomes a feature | Create a canonical DESIGN record in `docs/sdd/artifacts/features_for_specs/` and preserve provenance in the promoted seed dossier |
| **Defer** | Remains a seed | Move to `docs/sdd/03_operations/pre_sdd/seeds/deferred/` with reason and review date |
| **Reject** | Closed | Move to `docs/sdd/03_operations/pre_sdd/seeds/rejected/` with reason |
| **Merge** | Consolidated | Merge into an existing seed or feature and record the link in the dossier |
| **Spike** | Research task | Create a time-boxed spike feature |

---

## Responsibilities

| Role | Responsibility |
|------|---------------|
| **Reporter** | Captures seed with provenance and context |
| **Triage Owner** | Reviews seeds, applies classification, makes triage decisions |
| **Product Owner** | Validates impact and priority |
| **Tech Lead** | Validates technical feasibility and scope |

---

## Seed Lifecycle

```
CAPTURE → CLASSIFY → TRIAGE → PRIORITIZE → REFINE → TRANSITION → ARCHIVE
                                      ↓
                          {PROMOTE | DEFER | REJECT | MERGE | SPIKE}
```

- **TRIAGE** produces the decision: PROMOTE, DEFER, REJECT, MERGE, or SPIKE
- **PROMOTE** continues through PRIORITIZE → REFINE → TRANSITION before entering the SDD pipeline
- All other decisions (DEFER, REJECT, MERGE, SPIKE) go directly to ARCHIVE
- See `docs/sdd/03_operations/pre_sdd/PRE_SDD_RUNTIME.md` for the full 7-phase operational workflow
- Pre-SDD labels are domain-local and are not persistent feature-record states

---

## Related Documents

- `docs/sdd/03_operations/pre_sdd/PRE_SDD_RUNTIME.md` — operational workflow
- `docs/sdd/03_operations/pre_sdd/templates/seed_dossier.md` — seed template
- `docs/sdd/03_operations/pre_sdd/templates/triage_batch.md` — batch review template
- `docs/sdd/04_project_governance/PROJECT_MANIFEST.md` — non-goals and constraints
- `docs/sdd/02_policies/DECOMPOSITION_AND_SIZE_POLICY.md` — feature sizing guidelines
