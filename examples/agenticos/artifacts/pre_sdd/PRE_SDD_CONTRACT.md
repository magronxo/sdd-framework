# PRE-SDD Canonical Contract

## Purpose

This contract defines the canonical pre-SDD workflow: how seeds are captured, matured, gated, and triaged into SDD features.

## Glossary

| Term | Definition |
|------|------------|
| PKLot | Parking Lot — lightweight seed index (short entries, high-scannability) |
| Seed | Early idea, pattern, or problem statement pre-SDD |
| Seed Dossier | Durable, structured document for seeds needing detailed analysis |
| Triage Batch | Periodic session where seeds are evaluated and handed off to SDD |
| Exploration | Structured investigation gate before triage (when required) |
| Feature Record | JSON artifact that formally hands off a seed to SDD |

## Pre-SDD States

```
Captured ───→ Explored ───→ Triaged ───→ Adopted ───→ (SDD)
              ↑                                     │
              └──────── Deferred ◄────────────────┘
```

| State | Meaning |
|-------|---------|
| `Captured` | Seed exists in PKLot with initial notes |
| `Explored` | Exploration gate passed; dossier complete |
| `Triaged` | Evaluated in triage batch; decision pending |
| `Adopted` | Accepted for SDD; feature record created |
| `Deferred` | Not adopted this batch; can re-enter later |

## Seed Dossier v1 (Canonical Format)

Every seed that needs more than ~10 lines of analysis MUST have a dossier at:

```
artifacts/pre_sdd/seed_dossiers/SEED-NN.md
```

### Required Fields

| Field | Purpose | When Required |
|-------|---------|---------------|
| `problem` | One-liner: what problem does this seed address? | Always |
| `intent` | Desired outcome (not a solution) | Always |
| `scope_in` | Explicitly in-scope items | Always |
| `scope_out` | Explicitly out-of-scope items | Always |
| `capabilities` | What the feature MUST provide | Always |
| `approach` | How (brief, not a full spec) | Always |
| `risks` | Known or suspected risks | Always |
| `success_signals` | How we know it worked | Always |
| `dependencies` | What must exist first | Always |
| `exploration_required` | `true` or `false` + reason if true | Always |
| `entry_checklist` | Gate checklist before triage | Always |
| `triage_notes` | Long-form analysis (migrated from PKLot) | When applicable |

## Exploration Gate

A seed MUST go through exploration before triage if ANY of:

- **Estimation >2 days** of work
- **≥2 technical unknowns** identified
- **Affects invariants/kernel/security** directly

### Exploration Outputs

When `exploration_required: true`, the dossier MUST include:
- List of technical unknowns and initial hypotheses
- Dependency graph (what must exist first)
- Risk assessment with severity

## Triage Batch Contract

Triage batches live at:

```
artifacts/pre_sdd/triage_batches/triage_YYYY-MM-DD.md
```

Each batch MUST contain:

| Section | Description |
|---------|-------------|
| `scan` | Which seeds were reviewed and from what source |
| `selected` | Seeds adopted in this batch |
| `per-seed TRIAGE contract` | Minimal contract (problem/objective/scope/non-scope/risks/success_signal) |
| `decompose` | Decision: 1 feature vs N features |
| `handoff` | Paths created (ADR and/or feature records) |
| `decision_summary` | adopted/adapted/deferred/discarded counts |

### TRIAGE Contract (Minimal)

For each seed, TRIAGE contract MUST include:

```
- problem: what we're solving
- objective: desired outcome
- scope (candidates to spec — SDD): items that could become requirements
- non-scope: explicit exclusions
- impact: who benefits and how
- risks: known risks
- success_signal: how we know the feature worked
```

## HANDOFF Paths

| Destí | Format | When Used |
|-------|--------|-----------|
| Feature Record | `feat-XXX.json` in `artifacts/features_for_specs/` | Seeds adopted for SDD implementation |
| ADR | `00_project_documentation/SDD/artifacts/adr/NNNN-*.md` | Architectural decisions independent of features |
| Deferred | Remains in PKLot with updated `horizon` | Not ready for SDD this cycle |

## Rules

1. PKLot is index-first: short entries, no long analysis
2. Seeds needing >10 lines of notes get a dossier
3. Dossier is the living document; batch references it
4. Exploration gate MUST be passed before triage for complex seeds
5. TRIAGE contract is minimal (~10 fields); full analysis lives in dossier
6. Feature records created at triage use canonical SDD paths
7. Batch decisions are final for that cycle; seeds can be re-evaluated later