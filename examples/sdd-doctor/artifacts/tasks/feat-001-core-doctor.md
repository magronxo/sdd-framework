# Tasks: feat-001 — sdd-doctor Core CLI Doctor

**Feature ID**: feat-001
**Date**: 2026-04-26
**Status**: COMPLETED

---

## 1. Implementation Tasks

### Task 1.1: Module Setup
- [ ] **1.1.1**: Create `go.mod` with module `github.com/magronxo/sdd-framework/examples/sdd-doctor` and Go version 1.25
- [ ] **1.1.2**: Create directory structure (`cmd/sdd-doctor/`, `internal/doctor/`)
- [ ] **1.1.3**: Verify `go build` produces no errors

### Task 1.2: CLI Entry Point
- [ ] **1.2.1**: Implement `cmd/sdd-doctor/main.go` with argument parsing
- [ ] **1.2.2**: Validate `check` subcommand presence
- [ ] **1.2.3**: Validate `<path>` argument presence
- [ ] **1.2.4**: Print usage to stderr on missing/invalid args
- [ ] **1.2.5**: Return exit code 2 on usage error

### Task 1.3: Doctor Core Logic
- [ ] **1.3.1**: Define exit code constants (ExitCodeOK=0, ExitCodeFindings=1, ExitCodeRuntime=2)
- [ ] **1.3.2**: Define Config struct matching sdd.config.json schema
- [ ] **1.3.3**: Define Paths struct
- [ ] **1.3.4**: Define Finding struct (Location, Severity, Code, Message)
- [ ] **1.3.5**: Define Severity constants (PASS, WARN, FAIL, BLOCKED)
- [ ] **1.3.6**: Define RuntimeError struct and error codes (E001, E002, E003)
- [ ] **1.3.7**: Implement `Run(args []string) int` function
- [ ] **1.3.8**: Implement `New(targetPath string) *Doctor` constructor

### Task 1.4: Path Validation
- [ ] **1.4.1**: Resolve absolute path from relative input
- [ ] **1.4.2**: Check path exists — E001 to stderr, exit 2 if not
- [ ] **1.4.3**: Check path is a directory — error to stderr, exit 2 if file
- [ ] **1.4.4**: Check path is readable — E003 to stderr, exit 2 if not

### Task 1.5: Config Validation
- [ ] **1.5.1**: Read `sdd.config.json` from target directory
- [ ] **1.5.2**: Handle file not found — FAIL (E004), continue
- [ ] **1.5.3**: Handle parse error — FAIL (E002), continue
- [ ] **1.5.4**: Validate `paths.root` field — FAIL (E005) if missing
- [ ] **1.5.5**: Validate `framework_version` field — FAIL (E006) if missing
- [ ] **1.5.6**: Add PASS finding on successful validation

### Task 1.6: Core Directory Validation
- [ ] **1.6.1**: Check required directories exist (00_core, 02_policies, 03_projects, 04_project_governance, 05_workflows, artifacts)
- [ ] **1.6.2**: Add FAIL (E007) for each missing required directory
- [ ] **1.6.3**: Add PASS for each existing required directory
- [ ] **1.6.4**: Check optional directories (01_docs, examples, .github)
- [ ] **1.6.5**: Add WARN (W001) for each missing optional directory

### Task 1.7: Artifact Directory Validation
- [ ] **1.7.1**: Check `artifacts` directory exists — FAIL (E008) if missing
- [ ] **1.7.2**: Check required subdirectories (design, specs, validation_reports, tasks)
- [ ] **1.7.3**: Add FAIL (E009) for each missing required subdirectory
- [ ] **1.7.4**: Add PASS for each existing required subdirectory
- [ ] **1.7.5**: Check optional subdirectories (features_for_specs, deltas)
- [ ] **1.7.6**: Add WARN (W002) for each missing optional subdirectory

### Task 1.8: Report Generation
- [ ] **1.8.1**: Implement `Report(output *os.File)` method
- [ ] **1.8.2**: Print "=== SDD Doctor Report ===" header
- [ ] **1.8.3**: Print all findings with icon, severity, location, message
- [ ] **1.8.4**: Use icons (✓ ⚠ ✗ ⊗) for severity levels
- [ ] **1.8.5**: Print summary count (PASS/WARN/FAIL/BLOCKED)

### Task 1.9: Exit Code Logic
- [ ] **1.9.1**: Implement `HasBlockingFindings() bool` method
- [ ] **1.9.2**: Return exit 0 when no FAIL/BLOCKED findings
- [ ] **1.9.3**: Return exit 1 when any FAIL/BLOCKED finding exists

---

## 2. Test Fixture Tasks

### Task 2.1: Valid Project Fixture
- [ ] **2.1.1**: Create `fixtures/valid-project/sdd.config.json` with valid structure
- [ ] **2.1.2**: Create all required core directories
- [ ] **2.1.3**: Create all optional core directories
- [ ] **2.1.4**: Create `artifacts/` with all required subdirectories
- [ ] **2.1.5**: Create `artifacts/features_for_specs/` and `artifacts/deltas/`

### Task 2.2: Invalid Project Fixtures
- [ ] **2.2.1**: Create `fixtures/invalid-project/missing-config/` (no sdd.config.json)
- [ ] **2.2.2**: Create `fixtures/invalid-project/unreadable-path/` (use permissions to test)

---

## 3. Verification Tasks

### Task 3.1: Build Verification
- [ ] **3.1.1**: Run `go build -o sdd-doctor.exe ./cmd/sdd-doctor`
- [ ] **3.1.2**: Verify binary exists and is runnable

### Task 3.2: Valid Project Test
- [ ] **3.2.1**: Run `sdd-doctor check fixtures/valid-project`
- [ ] **3.2.2**: Verify exit code is 0
- [ ] **3.2.3**: Verify report shows only PASS and WARN (no FAIL/BLOCKED)

### Task 3.3: Missing Config Test
- [ ] **3.3.1**: Run `sdd-doctor check fixtures/invalid-project/missing-config`
- [ ] **3.3.2**: Verify exit code is 1
- [ ] **3.3.3**: Verify FAIL finding for E004

### Task 3.4: Unreadable Path Test
- [ ] **3.4.1**: Run `sdd-doctor check fixtures/invalid-project/unreadable-path`
- [ ] **3.4.2**: Verify exit code is 2
- [ ] **3.4.3**: Verify E001 or E003 in stderr

### Task 3.5: Usage Error Test
- [ ] **3.5.1**: Run `sdd-doctor` with no args
- [ ] **3.5.2**: Verify exit code is 2
- [ ] **3.5.3**: Verify usage message to stderr

---

## 4. Sub-Tasks for Task 1.3 (Severity Enum Implementation)

### Task 1.3.5 Detail: Severity Constants
```go
const (
    SeverityPASS    Severity = "PASS"
    SeverityWARN    Severity = "WARN"
    SeverityFAIL    Severity = "FAIL"
    SeverityBLOCKED  Severity = "BLOCKED"
)
```

Icon mapping:
- PASS → ✓
- WARN → ⚠
- FAIL → ✗
- BLOCKED → ⊗

---

## 5. Task Dependencies

```
Task 1.1 (Module Setup)
  └─ Task 1.2 (CLI Entry Point)
       └─ Task 1.3 (Doctor Core Logic)
            ├─ Task 1.4 (Path Validation)
            ├─ Task 1.5 (Config Validation)
            ├─ Task 1.6 (Core Directory Validation)
            └─ Task 1.7 (Artifact Directory Validation)
                 └─ Task 1.8 (Report Generation)
                      └─ Task 1.9 (Exit Code Logic)

Tasks 2.x (Fixtures) can run in parallel with Tasks 1.x
Tasks 3.x (Verification) require Tasks 1.x and 2.x to complete first
```

---

## 6. Exit Criteria

Implementation is complete when:
- [ ] All implementation tasks (1.1–1.9) are checked off
- [ ] All test fixtures (2.1–2.2) are created
- [ ] All verification tests (3.1–3.5) pass
- [ ] `go build` succeeds without errors or warnings
- [ ] Binary runs deterministically on all three fixture types