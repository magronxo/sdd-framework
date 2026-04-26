# Design: feat-072 — Placeholder Cleanup feat-070 → TBD

## Context

El trace.go i diversos artefactes SDD contenen referències a "feat-070" com si fos una feature planificada. En realitat feat-070 no existeix com a feature amb design/spec. Les referències indiquen "kernel ticket_id injection pending feat-070".

## Decisions de Disseny

### DD-01: Feature ID
- `feat-072` — Placeholder Cleanup feat-070 → TBD

### DD-02: Neteja de referències
Substituir `feat-070` a:
1. `02_implementation/internal/api/trace.go:109` — codi
2. `artifacts/design/feat-069-trace-correlation.md` — design (comentari)
3. `artifacts/specs/feat-069-trace-correlation.md` — spec (nota)
4. `artifacts/features_for_specs/feat-069-trace-correlation.json` — feature record
5. `artifacts/audit_reports/audit_feat-069-trace-correlation_2026-04-12.md` — audit report
6. `artifacts/specs/feat-071-skills-structural-enforcement.md` — deferred list

### DD-03: Nou text
`"pending feat-070"` → `"TBD: kernel ticket_id injection"`

## Out of Scope
- No crear feat-070 (només netejar placeholders)
- No canviar lògica de codi (només comentaris/text)

## Resultat esperat
- `validation_result`: PASS
- `verification_result`: PASS
- `audit_result`: PASS
