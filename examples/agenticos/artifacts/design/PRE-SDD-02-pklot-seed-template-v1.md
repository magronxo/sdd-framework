# Design: PRE-SDD-02 — PKLot Seed Template v1

## Technical Approach

Doc-only change that creates a minimal seed template for PKLot entries, ensuring consistency without refactoring existing seeds. Zero migration of existing content.

## Architecture Decisions

### Decision: PKLot template is shorter than Seed Dossier v1

**Choice**: PKLot template has 12 fields vs Seed Dossier v1's 11+ (triage_notes). PKLot template is index-first (shorter), dossier is analysis-first (longer).

**Alternatives considered**:
- Use identical format to Seed Dossier v1
- Create a completely different schema

**Rationale**: PKLot is a scannable index. Seeds here should be captured quickly. Detailed analysis lives in Seed Dossier (pointed to via `batch_ref` or `notes`). The two formats are aligned but serve different purposes.

### Decision: Template only applies to new seeds (no migration)

**Choice**: Existing PKLot entries remain as-is. Template governs how NEW seeds are captured.

**Alternatives considered**:
- Migrate all existing seeds to new format
- Deprecate existing PKLot format entirely

**Rationale**: Non-disruptive. Existing seeds already have context in dossiers or triage batches. Migrating would be noise without value.

### Decision: Align field names between PKLot template and Seed Dossier v1

**Choice**: `problem`, `intent`, `scope_in`, `scope_out`, `success_signals`, `unknowns`, `dependencies`, `exploration_required`, `entry_checklist` appear in both.

**Rationale**: Enables easy migration from PKLot entry → Seed Dossier when seed needs detailed analysis. Field mapping is trivial.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `artifacts/pre_sdd/templates/pklot_seed_v1.md` | Create | Minimal PKLot seed template |
| `04_PARKING_LOT.md` | Modify | Add "Com capturar seeds (PKLot Seed v1)" section |
| `artifacts/pre_sdd/README.md` | Modify | Reference PKLot template |

## PKLot Seed v1 Fields

| Field | Purpose | Aligns with Seed Dossier v1 |
|-------|---------|------------------------------|
| `seed_id` | Unique identifier (SEED-NN) | Yes — ID field |
| `title` | Short name | Yes — Titol field |
| `problem` | One-liner problem statement | Yes — problem field |
| `proposed_solution` | Brief proposed approach | No — Dossier uses `approach` (more detailed) |
| `scope_in` | Explicit in-scope items | Yes — scope_in field |
| `scope_out` | Explicit out-of-scope items | Yes — scope_out field |
| `success_signals` | How we know it worked | Yes — success_signals field |
| `unknowns` | Technical uncertainties | Yes — exploration_required section |
| `dependencies` | What must exist first | Yes — dependencies field |
| `exploration_required` | true/false + reason | Yes — exploration_required field |
| `entry_checklist` | Gate checklist before triage | Yes — entry_checklist field |
| `horizon` | NOW/NEXT/LATER | Yes — Horizon field |
| `status_pre_sdd` | Current state | Yes — Estat (PRE-SDD) field |
| `batch_ref` | Link to dossier or triage batch | Yes — Batch ref field |

## Data Flow

```
PKLot entry (PKLot Seed v1)
    │
    └─── (if needs >10 lines analysis) ──→ Seed Dossier v1
                                              │
                                              └─── (when triaged) ──→ Feature Record / ADR
```

## Open Questions

- None — all decisions defined in prompt.