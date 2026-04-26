# PRE-SDD artifacts

This folder contains durable PRE-SDD outputs (auditable artifacts).

## Canonical Contract

The PRE-SDD workflow is governed by:

- **[PRE_SDD_CONTRACT.md](./PRE_SDD_CONTRACT.md)** — canonical contract defining states, seed dossier format, triage batch contract, and handoff paths

## Templates

Standard templates for PRE-SDD artifacts:

- **[templates/seed_dossier_v1.md](./templates/seed_dossier_v1.md)** — standard seed dossier format (v1) — for seeds needing detailed analysis (>10 lines)
- **[templates/triage_batch_v1.md](./templates/triage_batch_v1.md)** — standard triage batch format (v1) — for periodic triage sessions
- **[templates/pklot_seed_v1.md](./templates/pklot_seed_v1.md)** — standard PKLot seed format (v1) — for new seeds captured in the Parking Lot

## PKLot Index

The Parking Lot (`00_project_documentation/04_PARKING_LOT.md`) is the entry point for all seeds. Seeds captured there use the [PKLot Seed v1 template](./templates/pklot_seed_v1.md).

## Dossier Index

Seed dossiers (long-form analysis, exceeds ~10 lines in PKLot):

- `seed_dossiers/SEED-NN.md`

## Triage Batches

Periodic triage sessions:

- `triage_batches/triage_YYYY-MM-DD.md` — batch reports that document selected seeds, minimal TRIAGE contract, DECOMPOSE decisions, and explicit HANDOFF paths (feature records and/or ADRs)

## Workflow Summary

```
PKLot (index, short entries)
  └── SEED-NN ──points to──> seed_dossiers/SEED-NN.md (dossier, v1 format)
                              └── TRIAGE contract
                                  └── referenced by triage_batches/triage_YYYY-MM-DD.md
                                      └── HANDOFF to SDD (feat-XXX.json) or ADR
```

## State Machine

```
Captured ───→ Explored ───→ Triaged ───→ Adopted ───→ (SDD)
              ↑                                     │
              └──────── Deferred ◄────────────────┘
```

See [PRE_SDD_CONTRACT.md](./PRE_SDD_CONTRACT.md) for full details.

