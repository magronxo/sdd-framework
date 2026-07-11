# SDD Runtime Contract

> **Mode Diátaxis**: Reference

## Purpose and authority

This document summarizes the installed runtime. Machine-readable authority is:

- `docs/sdd/contract/v1/feature-record.schema.json` for feature-record shape and invariants;
- `docs/sdd/contract/v1/sdd-protocol.json` for lifecycle, transitions, gates, blockers, regressions, and checkpoints.

No Markdown file overrides those contracts.

## Install context

The installed root is `docs/sdd/`. Generated artifacts use `docs/sdd/artifacts/`. Product source remains outside the installed root.

## Persistent lifecycle

`SEED` and `INTAKE` are pre-record activities.

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

## Core rules

- No implementation without effective validation `PASS`.
- Blocking open questions deny progression independently of result interpretation.
- `TASKS -> IMPLEMENT` validates semantic prerequisites.
- Human approval is conditional on an active external policy requesting a protocol-declared checkpoint.
- The core does not resolve profiles or integrate wrappers.
- No role mixing, skipped states, or silent normalization.

## Results

Canonical validation and verification results are `PASS` or `FAIL`. Canonical audit results are `PASS`, `WARN`, or `FAIL`.

Historical validation `PASS_WITH_FOLLOWUP` is a tolerant read with effective validation `PASS` only when no open question is blocking. Canonical writes reject it.

Active verification `PARTIAL` is invalid and produces `VERIFICATION_NOT_EXECUTED`. Archived `PARTIAL` is an ambiguous tolerant read with effective verification `null` and `migration_review_required: true`; it must not be changed automatically.

## Failure handling

- `VALIDATION FAIL -> SPEC`
- `VERIFY FAIL -> IMPLEMENT`
- `AUDIT FAIL` blocks `AUDIT -> ARCHIVE` unless a valid owner waiver is recorded.
- Audit failure does not select an automatic repair phase.

An owner waiver has no effect outside the archival transition.

## Paths

Canonical artifact paths begin with `docs/sdd/artifacts/`. The explicit legacy prefix is interpreted only as declared by the schema and validator. Exact `..` path segments are invalid.
