# Verify Report: feat-049 (SEC-01 Security modes enforcement)

**feature_id:** feat-049  
**date (UTC):** 2026-04-11T16:48:55Z  
**environment_mode:** execute  
**verification_result:** PASS  

## INVOCATIONS
- verify_engine: inline (manual execution)
- skill: none declared in TASKS

## EVIDENCE
- Files read:
  - `00_project_documentation/SDD/artifacts/design/feat-049-sec-01-security-modes-enforcement.md`
  - `00_project_documentation/SDD/artifacts/specs/feat-049-sec-01-security-modes-enforcement.md`
  - `00_project_documentation/SDD/artifacts/tasks/feat-049-sec-01-security-modes-enforcement.md`
  - `00_project_documentation/05_ADR_DECISION_LOG.md` (ADR 028)
  - `02_implementation/internal/kernel/mode.go`
  - `02_implementation/internal/kernel/guardian.go`
  - `02_implementation/internal/kernel/executor.go`
  - `02_implementation/internal/api/server.go`
  - `02_implementation/internal/api/handlers_kernel.go`
  - `02_implementation/cmd/agenticos/main.go`
- Feature record:
  - `00_project_documentation/SDD/artifacts/features_for_specs/feat-049-sec-01-security-modes-enforcement.json`

## COMMANDS

### Kernel tests (SEC-01)
```
cwd: K:\AgenticOsGen\02_implementation
command: go test ./internal/kernel -count=1
status: EXECUTED
exit_code: 0
raw_output_excerpt:
ok  	agenticos/internal/kernel	14.422s
```

### API tests (PUT /kernel/mode wiring to Guardian)
```
cwd: K:\AgenticOsGen\02_implementation
command: go test ./internal/api -count=1
status: EXECUTED
exit_code: 0
raw_output_excerpt:
ok  	agenticos/internal/api	2.258s
```

## SURFACES
- mode enforcement: true
- tool execution: true
- network: indirect (mode blocks/permits network surface)
- notes:
  - Enforcement pre-exec a `Executor.ExecuteTool()` amb `Guardian.ValidateModeSurface()`.
  - Wiring API: `PUT /api/v1/kernel/mode` actualitza `currentSecurityMode` i crida `guardian.SetMode(...)` quan hi ha guardian.
  - Wiring runtime: `cmd/agenticos/main.go` injecta `guardian` a `executor` via `executor.SetGuardian(guardian)`.

## VERDICT
- **verification_result:** PASS
- **raons:**
  1. Tests SEC-01 passen amb evidència EXECUTED + exit code 0.
  2. Wiring d'API i runtime cobreix el contracte mínim de `RF-049-F` i `RF-049-E`.
  3. Errors deterministes: `E_ACTION_DENIED_BY_MODE` quan surface no permesa.

