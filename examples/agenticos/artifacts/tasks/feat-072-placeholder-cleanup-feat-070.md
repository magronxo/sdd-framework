# Tasks: feat-072 — Placeholder Cleanup feat-070 → TBD

## Skills
N/A (micro cleanup)

## T1: Replace strings in 6 files

### Files:
1. `02_implementation/internal/api/trace.go` — 1 replace
2. `artifacts/design/feat-069-trace-correlation.md` — 4 replaces
3. `artifacts/specs/feat-069-trace-correlation.md` — 1 replace
4. `artifacts/features_for_specs/feat-069-trace-correlation.json` — 2 replaces
5. `artifacts/audit_reports/audit_feat-069-trace-correlation_2026-04-12.md` — 3 replaces
6. `artifacts/specs/feat-071-skills-structural-enforcement.md` — 1 replace

**Pattern**: `pending feat-070` → `TBD: kernel ticket_id injection`

## T2: Verify

```bash
grep -r "feat-070" --include="*.go" --include="*.md" --include="*.json"
```

Ha de tornar 0 resultats.
