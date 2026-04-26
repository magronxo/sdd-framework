# Design: PRE-SDD-01 — Unificació TRIAGE/Proposal + Seed Template

## Technical Approach

Doc-only change that creates a canonical pre-SDD contract, standardizes seed dossier format, and formalizes triage batch structure. No code changes.

## Architecture Decisions

### Decision: One canonical seed format (Seed Dossier v1)

**Choice**: Define `Seed Dossier v1` as the unified format for all seeds that are candidates for triage. Replaces the current loose format (free-form notes).

**Alternatives considered**:
- Extend PKLot entries with structured fields
- Keep current free-form dossier format

**Rationale**: PKLot is index-first (short entries). Seeds needing more than ~10 lines of analysis need a durable dossier. The dossier format must be structured enough for consistency but flexible enough for diverse seeds.

### Decision: Exploration gate is explicit (not automatic)

**Choice**: A seed requires `exploration_required: true` when ANY of: estimation >2 days, ≥2 technical unknowns, or affects invariants/kernel/security.

**Alternatives considered**:
- All seeds go through triage directly
- Exploration always required

**Rationale**: Gate keeps triage efficient for simple seeds while ensuring complex ones get proper scoping before triage. Explicit criteria prevent arbitrary decisions.

### Decision: Triage batch references dossiers (does not duplicate)

**Choice**: `triage_batch_v1.md` contains per-seed summaries and TRIAGE contract, but pointers to `seed_dossiers/` for full context.

**Alternatives considered**:
- Inline all dossier content into batch
- Keep batch as pure execution log with no TRIAGE contract

**Rationale**: Duplication causes drift when dossiers are updated. Pointer model preserves audit trail in batch while keeping dossiers as living documents.

### Decision: PKLot stays unchanged (referenced, not modified)

**Choice**: PKLot continues as index only. Seed entries point to dossier files when analysis exceeds index capacity.

**Rationale**: PKLot is a lightweight, scannable index. Changing its format or merging it with dossiers would reduce its usefulness as a quick overview tool.

## Data Flow

```
PKLot (index)
  └── SEED-NN ──points to──> seed_dossiers/SEED-NN.md (dossier)
                              └── TRIAGE contract
                                  └── referenced by triage_batches/triage_YYYY-MM-DD.md
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `artifacts/pre_sdd/PRE_SDD_CONTRACT.md` | Create | Canonical pre-SDD contract |
| `artifacts/pre_sdd/templates/seed_dossier_v1.md` | Create | Standard seed dossier template |
| `artifacts/pre_sdd/templates/triage_batch_v1.md` | Create | Standard triage batch template |
| `artifacts/pre_sdd/README.md` | Modify | Point to contract + templates |
| `artifacts/pre_sdd/seed_dossiers/SEED-04.md` | Modify | Migrate existing dossiers to v1 format |
| `artifacts/pre_sdd/seed_dossiers/SEED-05.md` | Modify | Migrate existing dossiers to v1 format |
| `artifacts/pre_sdd/seed_dossiers/SEED-07.md` | Modify | Migrate existing dossiers to v1 format |

## Seed Dossier v1 Schema

```
problem       — One-liner: what problem does this seed address?
intent        — What outcome do we want?
scope_in      — Explicit IN-scope items
scope_out     — Explicit OUT-of-scope items
capabilities  — What the feature must provide
approach      — How (brief, not a spec)
risks         — Known or suspected risks
success_signals — How we know it worked
dependencies  — What must exist first
exploration_required — true/false + reason if true
entry_checklist — Gate checklist before triage
```

## Exploration Gate Criteria

A seed MUST go through exploration before triage if ANY:
- Estimation >2 days
- ≥2 technical unknowns identified
- Affects kernel invariants, security model, or core wiring

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Doc consistency | Templates parse correctly | Manual checklist |
| Schema validation | All required fields present | Manual review |
| Backward compat | Existing seeds migrate cleanly | Read existing dossiers |

No automated tests needed for doc-only change.

## Open Questions

- None — all decisions were explicitly defined in the prompt.