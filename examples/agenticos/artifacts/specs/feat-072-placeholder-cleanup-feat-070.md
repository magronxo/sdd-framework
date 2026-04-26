# Spec: feat-072 — Placeholder Cleanup feat-070 → TBD

## Overview

| Field | Value |
|-------|-------|
| **Feature ID** | feat-072 |
| **Title** | Placeholder Cleanup feat-070 → TBD |
| **Type** | MICRO_SPEC |
| **State** | SPEC |

## Problem

Diversos fitxers contenen `pending feat-070` quan feat-070 no existeix com a feature. Cal substituir per text neutre.

## Solution

Reemplaçar `pending feat-070` per `TBD: kernel ticket_id injection` a 6 fitxers.

## Files to Update

| File | Change |
|------|--------|
| `02_implementation/internal/api/trace.go` | Replace comment |
| `artifacts/design/feat-069-trace-correlation.md` | Replace 4 references |
| `artifacts/specs/feat-069-trace-correlation.md` | Replace 1 reference |
| `artifacts/features_for_specs/feat-069-trace-correlation.json` | Replace 2 JSON fields |
| `artifacts/audit_reports/audit_feat-069-trace-correlation_2026-04-12.md` | Replace 3 references |
| `artifacts/specs/feat-071-skills-structural-enforcement.md` | Replace 1 reference |

## Acceptance Criteria

| ID | Criteri |
|----|---------|
| AC-01 | Cap referència a `feat-070` al repo |
| AC-02 | Nou text: `TBD: kernel ticket_id injection` |
| AC-03 | Tests passen (si n'hi ha) |
