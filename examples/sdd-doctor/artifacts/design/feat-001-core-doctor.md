# Design: feat-001 — sdd-doctor Core CLI Doctor

**Feature ID**: feat-001
**Type**: SYSTEM_SPEC
**Date**: 2026-04-26
**Status**: DRAFT

---

## 1. Context

### Purpose
sdd-doctor is a diagnostic CLI tool that validates SDD framework project structure. It scans a target directory and reports findings about compliance with framework conventions.

### Problem Being Solved
Manual validation of SDD framework conventions is error-prone. This tool automates the audit with deterministic, CI-friendly output.

### Constraints
- Go 1.25, stdlib only
- Single static binary
- Human-readable terminal output (no JSON)
- Deterministic behavior

---

## 2. Goals

### Primary Goals
1. CLI accepts `check <path>` command
2. Validates presence and structure of `sdd.config.json`
3. Validates presence of required core directories
4. Validates presence of required artifact directories
5. Reports findings with severity levels
6. Returns appropriate exit codes (0, 1, 2)

### Non-Goals
- No auto-fix functionality
- No JSON or machine-readable output
- No web UI or TUI
- No network-based validation

---

## 3. Technical Approach

### Architecture

```
cmd/sdd-doctor/main.go     → Entry point, argument parsing
internal/doctor/doctor.go  → Core logic, all checks, reporting
```

### Module
`github.com/CollSalvia-Org/sdd-framework/examples/sdd-doctor`

### Build
```bash
go build ./cmd/sdd-doctor
```

### CLI Interface

**Usage**:
```
sdd-doctor check <path>
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| `check`  | Yes      | Subcommand identifier |
| `<path>` | Yes      | Target directory to validate |

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0    | No FAIL or BLOCKED findings |
| 1    | At least one FAIL or BLOCKED finding |
| 2    | Runtime error (path not found, etc.) |

**Error Messages to stderr**:
| Code | Condition |
|------|-----------|
| E001 | Target path does not exist |
| E003 | Target path is not readable |

### Data Structures

```go
type Config struct {
    Version          string `json:"version"`
    Name             string `json:"name"`
    Paths            Paths  `json:"paths"`
    FrameworkVersion string `json:"framework_version"`
}

type Paths struct {
    Root       string `json:"root"`
    Core       string `json:"core"`
    Artifacts  string `json:"artifacts"`
    Policies   string `json:"policies"`
    Governance string `json:"governance"`
}

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

### Severity Semantics

| Severity | Meaning | Exit Code Impact |
|----------|---------|-----------------|
| PASS     | Check succeeded | No impact |
| WARN     | Suspicious but not blocking | No impact |
| FAIL     | Contract missing or invalid | Causes exit 1 |
| BLOCKED  | Governance violation | Causes exit 1 |

### Error Codes

| Code | Type | Meaning | Action |
|------|------|---------|--------|
| E001 | Runtime | Target path does not exist | Exit 2 |
| E002 | Finding | sdd.config.json parse error | FAIL, continue |
| E003 | Runtime | Target path is not readable | Exit 2 |
| E004 | Finding | sdd.config.json not found | FAIL, continue |
| E005 | Finding | paths.root field missing | FAIL, continue |
| E006 | Finding | framework_version field missing | FAIL, continue |
| E007 | Finding | Required core directory missing | FAIL, continue |
| E008 | Finding | artifacts directory missing | FAIL, continue |
| E009 | Finding | Required artifacts subdirectory missing | FAIL, continue |
| W001 | Warning | Optional directory missing | WARN, no impact |
| W002 | Warning | Optional artifacts subdirectory missing | WARN, no impact |
| OK   | Info | Check passed | No impact |

---

## 4. Component Design

### `cmd/sdd-doctor/main.go`

**Responsibilities**:
- Parse CLI arguments
- Validate argument count
- Dispatch to `doctor.Run()`

**Interface**:
```go
func main() {
    os.Exit(doctor.Run(os.Args[1:]))
}
```

**Error Handling**:
- Missing args → print usage to stderr, exit 2
- Unknown subcommand → print usage to stderr, exit 2

---

### `internal/doctor/doctor.go`

**Public API**:
```go
const (
    ExitCodeOK       = 0
    ExitCodeFindings = 1
    ExitCodeRuntime  = 2
)

func Run(args []string) int
func New(targetPath string) *Doctor
func (d *Doctor) Run()
func (d *Doctor) Report(output *os.File)
func (d *Doctor) HasBlockingFindings() bool
```

**Run() Flow**:
1. Parse and validate arguments
2. Resolve absolute path
3. Check path exists and is readable
4. Create Doctor instance and call Run()
5. Print report
6. Return exit code

**Run() Internal Flow**:
1. checkConfig()
2. checkCoreDirectories()
3. checkArtifactDirectories()

**checkConfig()**:
- Read `sdd.config.json` from target
- If missing → FAIL (E004), return
- If parse error → FAIL (E002), return
- Validate required fields:
  - `paths.root` → if missing → FAIL (E005)
  - `framework_version` → if missing → FAIL (E006)
- If valid → PASS (OK)

**checkCoreDirectories()**:
Required directories:
- `00_core`
- `02_policies`
- `03_projects`
- `04_project_governance`
- `05_workflows`
- `artifacts`

Optional directories (WARN if missing):
- `01_docs`
- `examples`
- `.github`

For each required dir: if missing → FAIL (E007), else PASS (OK)
For each optional dir: if missing → WARN (W001), else PASS (OK)

**checkArtifactDirectories()**:
- Check `artifacts` directory exists → if missing → FAIL (E008), return
- If exists → PASS (OK)

Required subdirectories:
- `design`
- `specs`
- `validation_reports`
- `tasks`

Optional subdirectories (WARN if missing):
- `features_for_specs`
- `deltas`

For each required subdir: if missing → FAIL (E009), else PASS (OK)
For each optional subdir: if missing → WARN (W002), else PASS (OK)

---

## 5. Report Format

```
=== SDD Doctor Report ===

[Errors (if any)]
Runtime Errors:
  [E001] target path does not exist

Findings:

  ✓ [PASS] sdd.config.json: sdd.config.json valid
  ✓ [PASS] core:00_core: directory exists: 00_core
  ✗ [FAIL] core:01_docs: required directory missing: 01_docs
  ⚠ [WARN] core:.github: optional directory missing: .github
  ...

Summary: 12 PASS, 2 WARN, 1 FAIL, 0 BLOCKED
```

### Icons
| Severity | Icon |
|----------|------|
| PASS | ✓ |
| WARN | ⚠ |
| FAIL | ✗ |
| BLOCKED | ⊗ |

---

## 6. Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| No arguments | Print usage to stderr, exit 2 |
| Only `check` (no path) | Print usage to stderr, exit 2 |
| Path does not exist | E001 to stderr, exit 2 |
| Path is a file (not dir) | "target must be a directory" to stderr, exit 2 |
| No read permissions | E003 to stderr, exit 2 |
| Empty sdd.config.json | E002 (parse error), exit 1 |
| sdd.config.json missing required fields | Multiple FAILs, exit 1 |
| All required present | PASS findings only, exit 0 |
| Mixed PASS/WARN | WARN allowed, exit 0 |
| Any FAIL/BLOCKED | Exit 1 |

---

## 7. Integration Surfaces

| Surface | Used | Purpose |
|---------|------|---------|
| os_fs | Yes | Read directories, read config file |
| os_args | Yes | CLI argument parsing |
| stdout | Yes | Report output |
| stderr | Yes | Error messages |
| process_exit | Yes | Exit codes |

All other surfaces: **false**

---

## 8. File Structure

```
examples/sdd-doctor/
├── go.mod
├── sdd.config.json
├── cmd/
│   └── sdd-doctor/
│       └── main.go
├── internal/
│   └── doctor/
│       └── doctor.go
└── fixtures/
    ├── valid-project/
    │   ├── sdd.config.json
    │   ├── 00_core/
    │   ├── 02_policies/
    │   ├── 03_projects/
    │   ├── 04_project_governance/
    │   ├── 05_workflows/
    │   ├── 01_docs/
    │   ├── examples/
    │   ├── .github/
    │   └── artifacts/
    │       ├── design/
    │       ├── specs/
    │       ├── validation_reports/
    │       ├── tasks/
    │       ├── features_for_specs/
    │       └── deltas/
    └── invalid-project/
        ├── missing-config/
        └── unreadable-path/
```

---

## 9. Traceability

| Requirement | Component |
|-------------|-----------|
| RF-01: CLI check command | main.go |
| RF-02: Usage on missing args | main.go |
| RF-03: Config detection | doctor.go:checkConfig() |
| RF-04: AGENTS.md detection | (deferred to feat-002) |
| RF-05: Core dir validation | doctor.go:checkCoreDirectories() |
| RF-06: Artifact dir validation | doctor.go:checkArtifactDirectories() |
| RF-07: Config parsing | doctor.go:checkConfig() |
| RF-08: Path field validation | doctor.go:checkConfig() |
| RF-09: Finding model | doctor.go:Finding,Severity |
| RF-10: Terminal report | doctor.go:Report() |
| RF-11: Exit 0 conditions | doctor.go:Run() |
| RF-12: Exit 1 conditions | doctor.go:Run() |
| RF-13: Exit 2 conditions | main.go |
| NFR-01: Stdlib only | go.mod |
| NFR-02: Deterministic | All components |