# Specification: feat-001 — sdd-doctor Core CLI Doctor

**Feature ID**: feat-001
**Type**: SYSTEM_SPEC
**Date**: 2026-04-26
**Status**: DRAFT

---

## 1. Introduction

### Context
sdd-doctor validates the structural integrity of SDD framework projects. It is a deterministic CLI tool that scans a target directory and reports findings about framework compliance.

### Goals
1. CLI accepts `check <path>` and returns appropriate exit codes
2. Validate presence and structure of `sdd.config.json`
3. Validate presence of required core directories
4. Validate presence of required artifact directories
5. Human-readable report with severity levels (PASS/WARN/FAIL/BLOCKED)
6. Deterministic behavior: same input always produces same output

### Non-Goals
- No auto-fix functionality
- No JSON or machine-readable output
- No web UI or TUI
- No network-based validation
- No multi-language support

---

## 2. Requirements

### Functional Requirements

#### RF-01: CLI Command Interface
The CLI MUST accept the following command format:
```
sdd-doctor check <path>
```
- `check` is a literal subcommand identifier
- `<path>` is a required argument specifying the target directory

#### RF-02: Usage on Missing Arguments
When arguments are missing or invalid:
- Print usage information to stderr
- Return exit code 2

#### RF-03: sdd.config.json Detection
The tool MUST check for the presence of `sdd.config.json` in the target directory.

#### RF-04: AGENTS.md Detection
**NOTE**: Deferred to feat-002 (Governance Checks).

#### RF-05: Core Directory Detection
The tool MUST check for the presence of these required directories:
- `00_core`
- `02_policies`
- `03_projects`
- `04_project_governance`
- `05_workflows`

Additionally:
- `artifacts` is required

Optional directories (WARN if missing):
- `01_docs`
- `examples`
- `.github`

#### RF-06: Artifact Directory Detection
The tool MUST check for the presence of the `artifacts` directory and its subdirectories.

Required subdirectories:
- `design`
- `specs`
- `validation_reports`
- `tasks`

Optional subdirectories (WARN if missing):
- `features_for_specs`
- `deltas`

#### RF-07: sdd.config.json Parsing
If `sdd.config.json` exists, the tool MUST parse it as JSON.
- On parse error: Add a FAIL finding with error code E002, continue validation.
- On success: Validate required fields.

#### RF-08: Path Field Verification
After successful parsing, the tool MUST verify these required fields:
- `paths.root` — must exist and be non-empty
- `framework_version` — must exist and be non-empty

If either field is missing or empty:
- Add a FAIL finding with error codes E005 or E006 respectively
- Continue validation

#### RF-09: Finding Model
All validation results MUST be represented as `Finding` records:
```go
type Finding struct {
    Location string
    Severity Severity
    Code     string
    Message  string
}

type Severity string

const (
    SeverityPASS    Severity = "PASS"
    SeverityWARN    Severity = "WARN"
    SeverityFAIL    Severity = "FAIL"
    SeverityBLOCKED  Severity = "BLOCKED"
)
```

Severity semantics:
- **PASS**: Check succeeded
- **WARN**: Suspicious but not blocking (optional items)
- **FAIL**: Contract missing or invalid (required items)
- **BLOCKED**: Governance violation

#### RF-10: Terminal Report
After all checks complete, the tool MUST print a human-readable report to stdout:
```
=== SDD Doctor Report ===

Findings:
  ✓ [PASS] sdd.config.json: sdd.config.json valid
  ✗ [FAIL] core:00_core: required directory missing: 00_core

Summary: 10 PASS, 2 WARN, 1 FAIL, 0 BLOCKED
```

#### RF-11: Exit Code 0 — Success
The tool MUST return exit code 0 when:
- All checks complete without runtime errors
- No FAIL or BLOCKED findings exist

#### RF-12: Exit Code 1 — Findings
The tool MUST return exit code 1 when:
- At least one FAIL or BLOCKED finding exists

#### RF-13: Exit Code 2 — Runtime Error
The tool MUST return exit code 2 when:
- Target path does not exist (E001)
- Target path is not readable (E003)
- Arguments are missing or invalid

### Non-Functional Requirements

#### NFR-01: Stdlib Only
The tool MUST use only Go standard library packages.
- No external dependencies
- `go build` produces a single static binary

#### NFR-02: Deterministic
The tool MUST produce identical output for identical input regardless of:
- Number of runs
- Time of day
- System load

---

## 3. Inputs and Outputs

### Command Input
```
sdd-doctor check <path>
```

### Outputs

#### Report (stdout)
```
=== SDD Doctor Report ===

[Errors section if runtime errors occurred]

Findings:
  [icon] [SEVERITY] location: message
  ...

Summary: X PASS, Y WARN, Z FAIL, W BLOCKED
```

#### Error Messages (stderr)
| Condition | Message |
|-----------|---------|
| Missing arguments | `Usage: sdd-doctor check <path>` |
| Path not exist | `[E001] target path does not exist` |
| Path not readable | `[E003] target path is not readable` |

#### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | No FAIL or BLOCKED findings |
| 1 | At least one FAIL or BLOCKED finding |
| 2 | Runtime error |

---

## 4. Error Codes

| Code | Type | Meaning | System Action |
|------|------|---------|---------------|
| E001 | Runtime | Target path does not exist | Print to stderr, exit 2 |
| E002 | Finding | sdd.config.json parse error | FAIL, continue |
| E003 | Runtime | Target path is not readable | Print to stderr, exit 2 |
| E004 | Finding | sdd.config.json not found | FAIL, continue |
| E005 | Finding | paths.root field missing | FAIL, continue |
| E006 | Finding | framework_version field missing | FAIL, continue |
| E007 | Finding | Required core directory missing | FAIL, continue |
| E008 | Finding | artifacts directory missing | FAIL, continue |
| E009 | Finding | Required artifacts subdirectory missing | FAIL, continue |
| W001 | Warning | Optional directory missing | WARN, no impact |
| W002 | Warning | Optional artifacts subdirectory missing | WARN, no impact |
| OK | Info | Check passed | No impact |

---

## 5. System Design

### Module Structure
```
github.com/magronxo/sdd-framework/examples/sdd-doctor
├── cmd/sdd-doctor/main.go
└── internal/doctor/doctor.go
```

### Public API

```go
const (
    ExitCodeOK        = 0
    ExitCodeFindings  = 1
    ExitCodeRuntime   = 2
)

func Run(args []string) int
```

### CLI Processing Flow

```
main()
  └─ doctor.Run(os.Args[1:])
       ├─ Parse "check" subcommand
       ├─ Validate path argument exists
       ├─ Resolve absolute path
       ├─ Check path is directory and readable
       ├─ doctor := New(absPath)
       ├─ doctor.Run()
       │    ├─ checkConfig()
       │    ├─ checkCoreDirectories()
       │    └─ checkArtifactDirectories()
       ├─ doctor.Report(os.Stdout)
       └─ Return exit code
```

### Validation Flow

#### checkConfig()
1. Read `sdd.config.json`
2. If not found → FAIL (E004), return
3. If parse error → FAIL (E002), return
4. Validate `paths.root` → if missing → FAIL (E005)
5. Validate `framework_version` → if missing → FAIL (E006)
6. If valid → PASS (OK)

#### checkCoreDirectories()
1. For each required dir: check exists → FAIL (E007) or PASS (OK)
2. For each optional dir: check exists → WARN (W001) or PASS (OK)

#### checkArtifactDirectories()
1. Check `artifacts` exists → FAIL (E008) if missing
2. For each required subdir: check exists → FAIL (E009) or PASS (OK)
3. For each optional subdir: check exists → WARN (W002) or PASS (OK)

---

## 6. Acceptance Criteria

### Gherkin Scenarios

```gherkin
Feature: sdd-doctor Core Validation

  Scenario: Valid SDD project passes validation
    Given a valid SDD project with all required directories and config
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the report should contain only PASS findings
    And no FAIL or BLOCKED findings should be present

  Scenario: Missing sdd.config.json fails validation
    Given a project without sdd.config.json
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 1
    And the report should contain a FAIL finding for "sdd.config.json"
    And the error code should be E004

  Scenario: Missing optional directories produce warnings
    Given a project missing some optional directories
    When I run "sdd-doctor check <project-path>"
    Then the exit code should be 0
    And the report should contain WARN findings for missing optional dirs
    And no FAIL findings should be present

  Scenario: Unreadable target path returns error
    Given a path that does not exist or is not accessible
    When I run "sdd-doctor check <invalid-path>"
    Then the exit code should be 2
    And an error message should be printed to stderr
    And the error code should be E001 or E003
```

---

## 7. Integration Surfaces

| Surface | Active | Purpose |
|---------|--------|---------|
| os_fs | Yes | Read directories, read config file |
| os_args | Yes | CLI argument parsing |
| stdout | Yes | Report output |
| stderr | Yes | Error messages |
| process_exit | Yes | Exit codes |
| network | No | N/A |
| time | No | N/A |
| random | No | N/A |

---

## 8. Traceability Matrix

| ID | Requirement | Test Scenario |
|----|-------------|---------------|
| RF-01 | CLI accepts `check <path>` | Valid SDD project passes |
| RF-02 | Usage on missing args | Unreadable path returns error |
| RF-03 | Config detection | Missing config fails |
| RF-04 | AGENTS.md detection | Deferred to feat-002 |
| RF-05 | Core dir validation | Valid project passes |
| RF-06 | Artifact dir validation | Valid project passes |
| RF-07 | Config parsing | Missing config fails |
| RF-08 | Path field validation | Missing config fails |
| RF-09 | Finding model | All scenarios |
| RF-10 | Terminal report | Valid project passes |
| RF-11 | Exit 0 conditions | Valid project passes |
| RF-12 | Exit 1 conditions | Missing config fails |
| RF-13 | Exit 2 conditions | Unreadable path returns error |
| NFR-01 | Stdlib only | Build produces single binary |
| NFR-02 | Deterministic | Repeated runs same result |