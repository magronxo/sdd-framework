# Audit: feat-049 (SEC-01 Security modes enforcement)

**feature_id:** feat-049  
**date (UTC):** 2026-04-11T16:55:00Z  
**environment_mode:** execute  
**audit_result:** PASS  

## INVOCATIONS
- audit_engine: sdd-audit (manual inline execution)
- skill: none declared in TASKS

## INPUTS
- ADR:
  - `00_project_documentation/05_ADR_DECISION_LOG.md` (ADR 028)
- Spec:
  - `00_project_documentation/SDD/artifacts/specs/feat-049-sec-01-security-modes-enforcement.md`
- Code:
  - `02_implementation/internal/kernel/mode.go`
  - `02_implementation/internal/kernel/guardian.go`
  - `02_implementation/internal/kernel/executor.go`
  - `02_implementation/internal/api/server.go`
  - `02_implementation/internal/api/handlers_kernel.go`
  - `02_implementation/cmd/agenticos/main.go`
- Verify evidence:
  - `00_project_documentation/SDD/audit_reports/verify_feat-049-sec-01-security-modes-enforcement_2026-04-11.md`

## CHECKS

### 1) SDD coherència d'artefactes
- DESIGN/SPEC/TASKS existeixen ✅
- Feature record existeix i apunta a verify report ✅

### 2) ADR 028 → enforcement real
- Surfaces mínimes (`read_only`, `write`, `execute`, `network`) implementades ✅
- Matriu `mode -> surfaces` implementada ✅
- Enforcement pre-exec al runtime (no només UI/API) ✅

### 3) API contracte mínim
- `PUT /api/v1/kernel/mode` valida mode i rebutja `FULL` sense HITL (baseline) ✅
- Quan hi ha Guardian, `PUT /kernel/mode` sincronitza `guardian.mode` ✅
- Startup sync: `initGuardianMode()` al `Server.Start()` ✅

### 4) Determinisme i seguretat
- Error determinista: `E_ACTION_DENIED_BY_MODE` ✅
- Ordre d'enforcement al punt únic d'execució: mode→surface abans de risk class ✅

## VERDICT
- **audit_result:** PASS
- **notes:**
  - Out-of-scope mantingut: persistència del mode, HITL per activar `FULL`, overlays `SAFE_MODE/LOCKDOWN`.

